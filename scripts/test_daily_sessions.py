import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


COLLECTOR = Path(__file__).with_name("daily-sessions.py")


class DailySessionsTest(unittest.TestCase):
    def test_combined_daily_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            project = home / "workspace" / "example"
            project.mkdir(parents=True)
            codex = home / "custom-codex"
            folder = codex / "sessions/2026/02/19"
            folder.mkdir(parents=True)
            before = "2026-02-19T14:59:59Z"
            after = "2026-02-19T15:00:00Z"

            def event(kind, **fields):
                return {"type": "event_msg", "timestamp": after,
                        "payload": {"type": kind, **fields}}

            def meta(source):
                return {"type": "session_meta", "payload": {"cwd": str(project), "source": source}}

            def write(path, records):
                path.write_text("".join(json.dumps(r) + "\n" for r in records) + "{")

            def run():
                return subprocess.check_output(
                    [sys.executable, str(COLLECTOR), "2026-02-20"], text=True,
                    env={**os.environ, "HOME": tmp, "CODEX_HOME": str(codex), "TZ": "Asia/Seoul"},
                )

            request = event("user_message", message="repeat")
            completed = event("item_completed", item={"type": "UserMessage",
                              "content": [{"type": "text", "text": "repeat"}]})
            write(folder / "rollout-main.jsonl", [
                meta("vscode"), event("user_message", message="# AGENTS.md instructions for example"),
                {**event("user_message", message="yesterday"), "timestamp": before},
                request, completed, event("task_started"), completed,
                event("item_completed", item={"type": "AgentMessage", "text": "internal"}),
                *[event("user_message", message=f"extra-{i}") for i in range(4)],
            ])
            write(folder / "rollout-child.jsonl", [meta({"subagent": {}}), request])
            write(folder / "rollout-diary.jsonl", [
                meta("cli"), {**event("user_message", message="너는 일일 활동 로그 유지자"), "timestamp": before},
                request,
            ])
            archive = codex / "archived_sessions"
            archive.mkdir()
            write(archive / "rollout-old.jsonl", [meta("cli"), event("user_message", message="archived")])
            output = run()
            self.assertIn("총 2개 세션", output)
            self.assertIn("## 개인", output)
            self.assertEqual(output.count("example [Codex]"), 2)
            self.assertEqual(output.count("  - repeat\n"), 2)
            self.assertIn("  - archived", output)
            for excluded in ("AGENTS.md", "yesterday", "internal", "extra-3"):
                self.assertNotIn(excluded, output)

            claude = home / ".claude/projects" / str(project).replace("/", "-")
            claude.mkdir(parents=True)
            transcript = claude / "example.jsonl"
            write(transcript, [{"message": {"role": "user", "content": "claude request"}}])
            os.utime(transcript, (1771513200, 1771513200))  # 2026-02-20 00:00 KST
            output = run()
            self.assertIn("총 3개 세션", output)
            self.assertIn("  - claude request", output)


if __name__ == "__main__":
    unittest.main()
