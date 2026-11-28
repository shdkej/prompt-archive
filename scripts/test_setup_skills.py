import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name('setup_skills.py')


def installer_module():
    spec = importlib.util.spec_from_file_location('setup_skills', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SetupSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repository with spaces'
        self.home = self.root / 'home'
        self.home.mkdir()
        self.skill = self.repo / 'skills/example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\ndescription: Example\n---\n')
        self.catalog = {'version': 1, 'packages': [
            {'path': 'skills/example', 'scope': 'shared',
             'openclaw': ['skills/example'],
             'codex': [{'name': 'example', 'path': 'skills/example'}]}
        ]}
        self.save_catalog()

    def save_catalog(self):
        (self.repo / 'skills/catalog.json').write_text(json.dumps(self.catalog))

    def run_setup(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo),
                               '--user-dir', str(self.home), *args], text=True, capture_output=True)

    def test_preview_writes_nothing(self):
        r = self.run_setup('--targets', 'openclaw,codex')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_apply_merges_config_and_second_run_is_noop(self):
        config = self.home / '.openclaw/openclaw.json'
        config.parent.mkdir()
        config.write_text(json.dumps({'sentinel': {'keep': 'value'}, 'skills': {
            'load': {'extraDirs': ['/existing'], 'watch': False},
            'entries': {'disabled': {'enabled': False}}}}))
        args = ('--targets', 'openclaw,codex', '--apply')
        r = self.run_setup(*args)
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(config.read_text())
        self.assertEqual(data['sentinel'], {'keep': 'value'})
        self.assertFalse(data['skills']['load']['watch'])
        self.assertEqual(data['skills']['load']['extraDirs'][0], '/existing')
        for path in ['.openclaw/skills/example', '.agents/skills/example']:
            self.assertEqual((self.home / path).resolve(), self.skill)
        before = config.read_bytes()
        r = self.run_setup(*args)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(config.read_bytes(), before)
        self.assertIn('"changed": 0', r.stdout)
        self.assertEqual(self.run_setup('--targets', 'openclaw,codex', '--check').returncode, 0)

    def test_conflict_requires_replace_and_keeps_backup(self):
        old = self.home / '.agents/skills/example'
        old.mkdir(parents=True)
        (old / 'local.txt').write_text('unpublished local work')
        r = self.run_setup('--targets', 'codex', '--apply')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual((old / 'local.txt').read_text(), 'unpublished local work')
        r = self.run_setup('--targets', 'codex', '--apply', '--replace')
        self.assertEqual(r.returncode, 0, r.stderr)
        backups = list((self.home / '.openclaw/backups/shared-skills').rglob('local.txt'))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), 'unpublished local work')

    def test_openclaw_migrates_discovery_without_exposing_role_skills(self):
        state = self.home / 'custom-openclaw'
        state.mkdir()
        config = state / 'openclaw.json'
        config.write_text(json.dumps({'agents': {'entries': {'main': {}}}, 'skills': {
            'load': {'extraDirs': ['/existing', str(self.repo / 'skills/shared')],
                     'watch': False}}}))
        private = self.repo / 'skills/review'
        private.mkdir()
        (private / 'SKILL.md').write_text('---\nname: review\ndescription: Review\n---\n')
        self.catalog['packages'].append({'path': 'skills/review', 'scope': 'main',
            'agent': 'main', 'openclaw': ['workspace/skills/review'], 'codex': []})
        self.save_catalog()
        args = ('--targets', 'openclaw', '--openclaw-dir', str(state))
        r = self.run_setup(*args, '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        load = json.loads(config.read_text())['skills']['load']
        self.assertEqual(load['extraDirs'], ['/existing', str(state / 'skills')])
        self.assertFalse(load['watch'])
        self.assertEqual((state / 'skills/example').resolve(), self.skill)
        self.assertFalse((state / 'skills/review').exists())
        self.assertEqual((state / 'workspace/skills/review').resolve(), private)
        self.assertEqual(self.run_setup(*args, '--check').returncode, 0)

    def test_relocation_repairs_dangling_link_and_preserves_backup(self):
        target = self.home / '.agents/skills/example'
        target.parent.mkdir(parents=True)
        legacy = self.repo / 'skills/shared/example'
        target.symlink_to(legacy, target_is_directory=True)
        r = self.run_setup('--targets', 'codex', '--apply')
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(target.is_symlink())
        self.assertEqual(target.readlink(), legacy)
        r = self.run_setup('--targets', 'codex', '--apply', '--replace')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(target.resolve(), self.skill)
        receipts = list((self.home / '.openclaw/backups/shared-skills').rglob('receipt.json'))
        self.assertEqual(len(receipts), 1)
        saved = Path(json.loads(receipts[0].read_text())['links'][0]['backup'])
        self.assertTrue(saved.is_symlink())
        self.assertEqual(saved.readlink(), legacy)
        self.assertEqual(self.run_setup('--targets', 'codex', '--check').returncode, 0)

    def test_missing_source_prevents_all_mutations(self):
        self.catalog['packages'].append({'path': 'skills/missing', 'scope': 'shared',
                                        'openclaw': ['skills/missing'], 'codex': []})
        self.save_catalog()
        r = self.run_setup('--targets', 'openclaw', '--apply')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_default_codex_does_not_expose_agent_skills(self):
        private = self.repo / 'skills/travel'
        private.mkdir(parents=True)
        (private / 'SKILL.md').write_text('---\nname: travel\ndescription: Travel\n---\n')
        self.catalog['packages'].append({'path': 'skills/travel', 'scope': 'hj',
                                        'openclaw': ['workspace-hj/skills/travel'],
                                        'codex': [{'name': 'travel', 'path': 'skills/travel'}]})
        self.save_catalog()
        r = self.run_setup('--targets', 'codex', '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.home / '.agents/skills/travel').exists())
        r = self.run_setup('--targets', 'codex', '--profile', 'hj', '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.home / '.agents/skills/travel').resolve(), private)

    def test_profile_rename_retires_only_selected_tools_managed_binding(self):
        previous_source = self.repo / 'skills/previous'
        self.catalog['packages'].append({
            'path': 'skills/example', 'scope': 'main', 'codex': [{
                'name': 'current', 'path': 'skills/example',
                'previous_binding': {'name': 'previous', 'path': 'skills/previous'},
            }],
        })
        self.save_catalog()
        codex = self.home / '.agents/skills/previous'
        claude = self.home / '.claude/skills/previous'
        for target in (codex, claude):
            target.parent.mkdir(parents=True)
            target.symlink_to(previous_source, target_is_directory=True)

        self.assertEqual(self.run_setup('--targets', 'codex', '--apply').returncode, 0)
        self.assertTrue(codex.is_symlink())
        args = ('--targets', 'codex', '--profile', 'main')
        preview = self.run_setup(*args)
        self.assertIn('"operation": "retire"', preview.stdout)
        self.assertTrue(codex.is_symlink())
        self.assertEqual(self.run_setup(*args, '--check').returncode, 1)
        installed = self.run_setup(*args, '--apply')
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertFalse(codex.is_symlink())
        self.assertTrue(claude.is_symlink())
        self.assertEqual(codex.with_name('current').resolve(), self.skill)
        backup = Path(json.loads(installed.stdout)['backup'])
        receipt = json.loads((backup / 'receipt.json').read_text())
        retired = [r for r in receipt['links'] if r.get('retired')]
        self.assertEqual(len(retired), 1)
        self.assertEqual(Path(retired[0]['backup']).readlink(), previous_source)
        self.assertEqual(self.run_setup(*args, '--check').returncode, 0)
        self.assertEqual(json.loads(self.run_setup(*args, '--apply').stdout)['changed'], 0)

        # A custom link (even an indirect link to the previous source) survives.
        indirect = self.home / 'alias'
        indirect.symlink_to(previous_source, target_is_directory=True)
        claude.unlink()
        claude.symlink_to(indirect, target_is_directory=True)
        args = ('--targets', 'claude', '--profile', 'main')
        self.assertEqual(self.run_setup(*args, '--apply', '--replace').returncode, 0)
        self.assertEqual(claude.readlink(), indirect)
        claude.unlink()
        claude.mkdir()
        (claude / 'local.txt').write_text('keep')
        self.assertEqual(self.run_setup(*args, '--check').returncode, 0)
        self.assertEqual((claude / 'local.txt').read_text(), 'keep')

    def test_retired_link_is_restored_after_later_failure(self):
        module = installer_module()
        old = self.home / 'previous'
        source = self.repo / 'skills/previous'
        old.symlink_to(source, target_is_directory=True)
        config = self.home / 'openclaw.json'
        config.write_bytes(b'concurrent edit')
        action = {'target': old, 'source': source, 'conflict': False, 'retire': True}
        with self.assertRaisesRegex(ValueError, 'changed'):
            module.apply_plan([action], config, None, {}, True, self.home / 'backup')
        self.assertEqual(old.readlink(), source)
        # Revalidate ownership between preview and execution.
        old.unlink()
        old.write_text('user file')
        with self.assertRaisesRegex(ValueError, 'Previous binding changed'):
            module.apply_plan([action], config, None, {}, False, self.home / 'backup')
        self.assertEqual(old.read_text(), 'user file')

    def test_bad_catalog_path_is_rejected(self):
        self.catalog['packages'][0]['openclaw'] = ['../../outside']
        self.save_catalog()
        self.assertNotEqual(self.run_setup('--targets', 'openclaw', '--apply').returncode, 0)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_failure_restores_existing_directory(self):
        module = installer_module()
        old = self.home / '.agents/skills/example'
        old.mkdir(parents=True)
        (old / 'local.txt').write_text('keep me')
        config = self.home / '.openclaw/openclaw.json'
        with patch.object(module, 'make_link', side_effect=OSError('simulated failure')):
            with self.assertRaises(OSError):
                module.apply_plan([{'target': old, 'source': self.skill, 'conflict': True}],
                                  config, None, {}, False, self.home / 'backup')
        self.assertEqual((old / 'local.txt').read_text(), 'keep me')
        self.assertFalse(config.exists())

    def test_windows_directory_uses_junction_with_quoted_paths(self):
        module = installer_module()
        target = self.home / 'skills with spaces/example'
        with patch.object(module.os, 'name', 'nt'), patch.object(module.subprocess, 'run') as run:
            module.make_link(self.skill, target)
        command = run.call_args.args[0]
        # A list would let Python apply CRT escaping (\") to cmd's inner quotes.
        self.assertIsInstance(command, str)
        self.assertIn('/v:off /s /c', command)
        self.assertIn(f'mklink /J "{target}" "{self.skill}"', command)

    def test_codex_only_ignores_unrelated_openclaw_json5(self):
        config = self.home / '.openclaw/openclaw.json'
        config.parent.mkdir()
        original = b'{ // unrelated JSON5 config\n enabled: true,\n}'
        config.write_bytes(original)
        r = self.run_setup('--targets', 'codex', '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(config.read_bytes(), original)

    def test_concurrent_config_edit_aborts_and_restores_links(self):
        module = installer_module()
        config = self.home / '.openclaw/openclaw.json'
        config.parent.mkdir()
        original = b'{"sentinel": 1}'
        concurrent = b'{"sentinel": 2, "new": true}'
        config.write_bytes(original)
        target = self.home / '.agents/skills/example'
        real_link = module.make_link

        def concurrent_link(source, destination):
            real_link(source, destination)
            config.write_bytes(concurrent)

        with patch.object(module, 'make_link', side_effect=concurrent_link):
            with self.assertRaisesRegex(ValueError, 'changed'):
                module.apply_plan([{'target': target, 'source': self.skill, 'conflict': False}],
                                  config, original, {'sentinel': 1, 'skills': {}}, True,
                                  self.home / 'backup')
        self.assertEqual(config.read_bytes(), concurrent)
        self.assertFalse(target.exists())


class CatalogDiscoveryTests(unittest.TestCase):
    def test_native_skills_are_also_discoverable_by_openclaw(self):
        # OpenClaw does not discover CODEX_HOME/skills. Every native binding
        # needs the same source in a shared root or its own workspace root.
        catalog = json.loads((SCRIPT.parent.parent / 'skills/catalog.json').read_text())
        packages = catalog['packages']
        shared_sources = {
            entry['path']
            for package in packages if package['scope'] == 'shared'
            for entry in package.get('codex', [])
        }
        shared_sources.update(
            package['path'] for package in packages
            if any(target.startswith('skills/') for target in package.get('openclaw', []))
        )
        for package in packages:
            if not any('/codex-home/skills/' in target
                       for target in package.get('openclaw', [])):
                continue
            agent = package['agent']
            workspace = 'workspace' if agent == 'main' else f'workspace-{agent}'
            discoverable = package['path'] in shared_sources or any(
                other['path'] == package['path'] and other.get('agent') == agent
                and any(target.startswith(f'{workspace}/skills/')
                        for target in other.get('openclaw', []))
                for other in packages
            )
            with self.subTest(agent=agent, source=package['path']):
                self.assertTrue(discoverable, 'native-only link is invisible to OpenClaw')


if __name__ == '__main__':
    unittest.main()
