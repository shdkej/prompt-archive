"""Publish physical line counts at each KST change date on the main branch."""

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLES = ("planner", "developer", "marketer", "operator")
PATHS = [f".agent/workflows/{role}.md" for role in ROLES]
KST = timezone(timedelta(hours=9))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def build():
    if git("rev-parse", "--is-shallow-repository").strip() == b"true":
        raise RuntimeError("Full main branch history is required.")
    changes = git("log", "--first-parent", "--reverse", "--format=%H %ct", "HEAD", "--", *PATHS)
    snapshots = {}
    line_counts = {}
    for revision in changes.decode().splitlines():
        sha, timestamp = revision.split()
        when = datetime.fromtimestamp(int(timestamp), KST)
        files = {}
        for entry in git("ls-tree", "-z", sha, "--", *PATHS).split(b"\0"):
            if not entry:
                continue
            meta, path = entry.split(b"\t", 1)
            blob = meta.split()[2].decode()
            if blob not in line_counts:
                content = git("cat-file", "blob", blob)
                line_counts[blob] = content.count(b"\n") + int(bool(content) and not content.endswith(b"\n"))
            files[path.decode()] = line_counts[blob]
        snapshots[when.date().isoformat()] = [files.get(path) for path in PATHS]
    if not snapshots:
        raise RuntimeError("No workflow file history found.")
    return {
        "version": 1,
        "roles": ROLES,
        "sourceCommit": sha,
        "updatedAt": when.isoformat(),
        "snapshots": [{"date": day, "counts": counts} for day, counts in sorted(snapshots.items())],
    }


if __name__ == "__main__":
    out = ROOT / "data" / "workflow-line-counts.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(build(), ensure_ascii=False, separators=(",", ":")) + "\n")
