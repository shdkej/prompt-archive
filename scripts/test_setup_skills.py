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
        self.skill = self.repo / 'skills/shared/example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\ndescription: Example\n---\n')
        self.catalog = {'version': 1, 'packages': [
            {'path': 'skills/shared/example', 'scope': 'shared',
             'openclaw': ['skills/example'],
             'codex': [{'name': 'example', 'path': 'skills/shared/example'}]}
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

    def test_missing_source_prevents_all_mutations(self):
        self.catalog['packages'].append({'path': 'skills/missing', 'scope': 'shared',
                                        'openclaw': ['skills/missing'], 'codex': []})
        self.save_catalog()
        r = self.run_setup('--targets', 'openclaw', '--apply')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_default_codex_does_not_expose_agent_skills(self):
        private = self.repo / 'skills/agents/hj/travel'
        private.mkdir(parents=True)
        (private / 'SKILL.md').write_text('---\nname: travel\ndescription: Travel\n---\n')
        self.catalog['packages'].append({'path': 'skills/agents/hj/travel', 'scope': 'hj',
                                        'openclaw': ['workspace-hj/skills/travel'],
                                        'codex': [{'name': 'travel', 'path': 'skills/agents/hj/travel'}]})
        self.save_catalog()
        r = self.run_setup('--targets', 'codex', '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((self.home / '.agents/skills/travel').exists())
        r = self.run_setup('--targets', 'codex', '--profile', 'hj', '--apply')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual((self.home / '.agents/skills/travel').resolve(), private)

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


if __name__ == '__main__':
    unittest.main()
