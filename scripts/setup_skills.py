#!/usr/bin/env python3
"""Connect this checkout to local agent tools. Preview unless --apply is given."""
import argparse
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def relative(root, value):
    part = Path(value)
    if part.is_absolute() or '..' in part.parts or not part.parts:
        raise ValueError(f'Unsafe catalog path: {value}')
    return root / part


def linked_to(target, source):
    try:
        return target.exists() and target.resolve() == source.resolve()
    except OSError:
        return False


def make_link(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if os.name == 'nt' and source.is_dir():
        # Junctions work without Windows Developer Mode or administrator rights.
        if any(c in str(source) + str(target) for c in '"%\r\n'):
            raise ValueError('Windows junction paths cannot contain quotes, %, or newlines')
        # cmd parses quotes itself; a list would introduce CRT backslash escaping.
        # /s removes only the enclosing quotes, /v:off keeps ! in paths literal.
        command = f'cmd.exe /d /v:off /s /c "mklink /J "{target}" "{source}""'
        subprocess.run(command, check=True, capture_output=True, text=True)
    else:
        target.symlink_to(source, target_is_directory=source.is_dir())


def remove_link(path):
    if os.name == 'nt' and not path.is_symlink() and path.is_dir():
        path.rmdir()  # Remove the junction, never traverse/delete its contents.
    else:
        path.unlink()


def write_atomic(path, content, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.shared-skills-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def build_plan(repo, user_dir, targets, profile, openclaw_dir):
    catalog = json.loads((repo / 'skills/catalog.json').read_text(encoding='utf-8'))
    if catalog['version'] != 1:
        raise ValueError('Unsupported catalog version')
    packages = catalog['packages']
    profiles = {'shared'} | {p['scope'] for p in packages if p['scope'] != 'archive'}
    if profile not in profiles:
        raise ValueError(f'Unknown profile: {profile}; choices: {sorted(profiles)}')
    config_path = openclaw_dir / 'openclaw.json'
    config_bytes = config_path.read_bytes() if 'openclaw' in targets and config_path.exists() else None
    config = json.loads(config_bytes) if config_bytes else {}
    changed_config = copy.deepcopy(config)
    configured_agents = set(config.get('agents', {}).get('entries', {}))
    # Do not create agents merely to install a skill on a fresh machine.
    links = {}
    portable = {}
    for package in packages:
        source = relative(repo, package['path'])
        if not source.is_dir() or not source.resolve().is_relative_to(repo.resolve()):
            raise ValueError(f'Missing or external skill source: {package["path"]}')
        if 'openclaw' in targets:
            for value in package.get('openclaw', []):
                target = relative(openclaw_dir, value)
                agent = package.get('agent')
                if agent and agent not in configured_agents:
                    continue
                if target in links and links[target] != source:
                    raise ValueError(f'Duplicate runtime binding: {target}')
                links[target] = source
        if package['scope'] in {'shared', profile}:
            for skill in package.get('codex', []):
                source_skill = relative(repo, skill['path'])
                if not (source_skill / 'SKILL.md').is_file():
                    raise ValueError(f'Missing SKILL.md: {source_skill}')
                # Named profiles intentionally override shared variants by name.
                if skill['name'] not in portable or package['scope'] == profile:
                    portable[skill['name']] = source_skill
    for tool, folder in [('codex', '.agents'), ('claude', '.claude')]:
        if tool in targets:
            for name, source in portable.items():
                links[relative(user_dir / folder / 'skills', name)] = source
    if 'claude' in targets:
        # Keep existing guide/agent mappings; only existing source files are used.
        for value in catalog.get('claude_files', []):
            source = relative(repo, value['source'])
            if not source.is_file():
                raise ValueError(f'Missing Claude guide: {source}')
            links[relative(user_dir / '.claude', value['target'])] = source
    if 'openclaw' in targets:
        load = changed_config.setdefault('skills', {}).setdefault('load', {})
        # Discover only the shared runtime bindings, across both source groups.
        # Loading the source root would expose every role's skills globally.
        for key, roots in [('extraDirs', [openclaw_dir / 'skills']),
                           ('allowSymlinkTargets', [repo / 'skills'])]:
            values = load.setdefault(key, [])
            if not isinstance(values, list):
                raise ValueError(f'skills.load.{key} must be an array')
            if key == 'extraDirs':
                legacy = str(repo / 'skills/shared')
                values[:] = [value for value in values if value != legacy]
            for root in roots:
                resolved = str(root)
                if resolved not in values:
                    values.append(resolved)
    actions = []
    for target, source in links.items():
        if linked_to(target, source):
            continue
        # Refuse a parent symlink escaping the user's declared tool directories.
        root = openclaw_dir if target.is_relative_to(openclaw_dir) else user_dir
        if not target.parent.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Target parent escapes tool directory: {target}')
        actions.append({'target': target, 'source': source,
                        'conflict': os.path.lexists(target)})
    update_config = changed_config != config
    return actions, config_path, config_bytes, changed_config, update_config, links


def apply_plan(actions, config_path, config_bytes, config, update_config, backup_root):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    backup = backup_root / stamp
    backup.mkdir(parents=True, mode=0o700)
    records = []
    journal = {'version': 1, 'links': [], 'config': None}
    journal_path = backup / 'receipt.json'

    def save():
        write_atomic(journal_path, (json.dumps(journal, indent=2) + '\n').encode())

    try:
        for index, action in enumerate(actions):
            target, source = action['target'], action['source']
            saved = None
            if action['conflict']:
                saved = backup / f'{index:03d}-{target.name}'
                shutil.move(str(target), str(saved))
            records.append((target, saved))
            journal['links'].append({'target': str(target), 'source': str(source),
                                     'backup': str(saved) if saved else None})
            save()
            make_link(source, target)
        if update_config:
            saved_config = backup / 'openclaw.json'
            if config_bytes is not None:
                write_atomic(saved_config, config_bytes)
            journal['config'] = {'target': str(config_path),
                                 'backup': str(saved_config) if config_bytes is not None else None}
            save()
            mode = config_path.stat().st_mode & 0o777 if config_path.exists() else 0o600
            if (config_path.read_bytes() if config_path.exists() else None) != config_bytes:
                raise ValueError('OpenClaw configuration changed during link installation; retry')
            write_atomic(config_path, (json.dumps(config, ensure_ascii=False, indent=2) + '\n').encode(), mode)
    except Exception:
        for target, saved in reversed(records):
            if os.path.lexists(target):
                remove_link(target)
            if saved is not None and os.path.lexists(saved):
                shutil.move(str(saved), str(target))
        journal['rolled_back'] = True
        save()
        raise
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--user-dir', type=Path, default=Path.home())
    parser.add_argument('--openclaw-dir', type=Path,
                        help='Default: OPENCLAW_STATE_DIR or <user-dir>/.openclaw')
    parser.add_argument('--targets', default='openclaw,codex', help='Comma-separated: openclaw,codex,claude')
    parser.add_argument('--profile', default='shared', help='Codex/Claude: shared or named agent profile')
    parser.add_argument('--replace', action='store_true', help='Back up conflicts before replacing them')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    repo, user_dir = args.repo.expanduser().resolve(), args.user_dir.expanduser().resolve()
    openclaw_dir = (args.openclaw_dir or Path(os.environ.get('OPENCLAW_STATE_DIR', user_dir / '.openclaw'))).expanduser().absolute()
    targets = set(args.targets.split(','))
    if not targets or not targets <= {'openclaw', 'codex', 'claude'}:
        parser.error('Invalid --targets')
    try:
        actions, path, before, config, update, links = build_plan(repo, user_dir, targets, args.profile, openclaw_dir)
        conflicts = [str(a['target']) for a in actions if a['conflict']]
        if args.check:
            print(json.dumps({'ok': not actions and not update, 'pending_links': len(actions),
                              'pending_config': update, 'conflicts': conflicts}, ensure_ascii=False))
            return 1 if actions or update else 0
        if not args.apply:
            print(json.dumps({'mode': 'preview', 'links': [
                {'target': str(a['target']), 'source': str(a['source']), 'conflict': a['conflict']}
                for a in actions], 'config_update': update}, ensure_ascii=False, indent=2))
            return 0
        if conflicts and not args.replace:
            raise ValueError('Existing files require --replace (backup first): ' + ', '.join(conflicts))
        if not actions and not update:
            print(json.dumps({'changed': 0, 'verified_links': len(links)}))
            return 0
        # Re-check immediately before mutating so a concurrently edited config is not lost.
        if 'openclaw' in targets and (path.read_bytes() if path.exists() else None) != before:
            raise ValueError('OpenClaw configuration changed during setup; retry')
        backup = apply_plan(actions, path, before, config, update,
                            openclaw_dir / 'backups/shared-skills')
        if not all(linked_to(t, s) for t, s in links.items()):
            raise ValueError('Post-install link verification failed')
        print(json.dumps({'changed': len(actions) + int(update), 'verified_links': len(links),
                          'backup': str(backup)}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'Setup failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
