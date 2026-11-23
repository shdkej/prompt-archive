#!/usr/bin/env python3
"""오늘(또는 지정 날짜)의 Claude Code 및 Codex 세션 요약 스크립트

사용법:
  python3 daily-sessions.py          # 오늘
  python3 daily-sessions.py 2026-02-20  # 특정 날짜
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"
CATEGORIES_FILE = Path.home() / ".claude" / "project-categories.json"

# 기본 분류 규칙
DEFAULT_CATEGORIES = {
    "~/dev/": "업무",
    "~/workspace/": "개인",
}


def load_categories():
    if CATEGORIES_FILE.exists():
        with open(CATEGORIES_FILE) as f:
            data = json.load(f)
        # project-categories.json 실제 구조 지원
        if "categories" in data:
            result = {}
            for key, val in data["categories"].items():
                label = val.get("description", key)
                for p in val.get("patterns", []):
                    result[p] = label
            return result
        return data
    return DEFAULT_CATEGORIES


def dir_to_path(project_dir_name):
    """디렉토리명을 원래 경로로 복원 (DFS + 실제 경로 검증)
    -Users-seongho-noh-workspace-prompt-archive → /Users/seongho-noh/workspace/prompt-archive
    """
    parts = project_dir_name.lstrip("-").split("-")

    def dfs(idx, current_path):
        if idx == len(parts):
            if Path(current_path).exists():
                return current_path
            return None
        segment = parts[idx]
        # 선택 1: 새 디렉토리로 분리 (/)
        new_path = current_path + "/" + segment
        if Path(new_path).exists() or Path(new_path).parent.exists():
            result = dfs(idx + 1, new_path)
            if result:
                return result
        # 선택 2: 현재 세그먼트에 이어붙이기 (-)
        concat_path = current_path + "-" + segment
        result = dfs(idx + 1, concat_path)
        if result:
            return result
        return None

    result = dfs(1, "/" + parts[0])  # 첫 세그먼트는 루트
    return result or ("/" + "-".join(parts))


def classify_path(path):
    categories = load_categories()
    home = str(Path.home())
    for pattern, category in categories.items():
        expanded = pattern.replace("~", home)
        if expanded in path:
            return category
    return "기타"


def extract_user_messages(filepath, max_messages=10):
    """세션 파일에서 사용자 메시지 추출"""
    messages = []
    with open(filepath) as f:
        for line in f:
            try:
                d = json.loads(line)
                role = d.get("message", {}).get("role", "")
                if role != "user":
                    continue
                content = d["message"].get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            t = c["text"].strip()
                            if t and not t.startswith("<"):
                                messages.append(t[:200])
                elif isinstance(content, str):
                    t = content.strip()
                    if t and not t.startswith("<"):
                        messages.append(t[:200])
            except (json.JSONDecodeError, KeyError):
                continue
            if len(messages) >= max_messages:
                break
    return messages


DIARY_SYNC_MARKER = "너는 일일 활동 로그 유지자"


def is_diary_sync_session(filepath):
    """diary-sync.sh가 claude -p로 만든 세션인지 판별"""
    try:
        with open(filepath) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    if d.get("message", {}).get("role") != "user":
                        continue
                    content = d["message"].get("content", "")
                    if isinstance(content, list):
                        text = " ".join(
                            c.get("text", "")
                            for c in content
                            if isinstance(c, dict) and c.get("type") == "text"
                        )
                    else:
                        text = content if isinstance(content, str) else ""
                    return DIARY_SYNC_MARKER in text
                except (json.JSONDecodeError, KeyError):
                    continue
    except OSError:
        pass
    return False


def find_claude_sessions(target_date):
    """대상 날짜에 수정된 세션 파일 탐색"""
    sessions = []
    if not CLAUDE_PROJECTS.exists():
        return sessions

    start = datetime.strptime(target_date, "%Y-%m-%d")
    end = start + timedelta(days=1)

    for project_dir in CLAUDE_PROJECTS.iterdir():
        if not project_dir.is_dir():
            continue
        for f in project_dir.glob("*.jsonl"):
            if "subagents" in str(f):
                continue
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if start <= mtime < end:
                if is_diary_sync_session(f):
                    continue
                sessions.append(
                    {
                        "file": f,
                        "path": dir_to_path(project_dir.name),
                        "source": "Claude",
                        "mtime": mtime,
                    }
                )

    sessions.sort(key=lambda s: s["mtime"])
    return sessions


def codex_session(filepath, day):
    """한 세션의 현지 날짜별 실제 사용자 이벤트만 모은다."""
    messages = []
    last_time = None
    cwd = None
    first_request = True
    pending = {}
    with filepath.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if not isinstance(record, dict):
                continue
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            if record.get("type") == "session_meta":
                source = payload.get("source")
                if isinstance(source, dict) and "subagent" in source:
                    return None
                cwd = payload.get("cwd")
                continue
            if record.get("type") != "event_msg":
                continue
            kind = payload.get("type")
            if kind == "task_started":
                pending.clear()
                continue
            if kind == "user_message":
                msg = payload.get("message")
            elif kind == "item_completed":
                item = payload.get("item")
                if not isinstance(item, dict) or item.get("type") != "UserMessage":
                    continue
                msg = "\n".join(
                    part["text"] for part in item.get("content", [])
                    if isinstance(part, dict) and part.get("type") == "text"
                    and isinstance(part.get("text"), str)
                )
            else:
                continue
            if not isinstance(msg, str):
                continue
            msg = msg.strip()
            if not msg or msg.startswith(("# AGENTS.md instructions for ", "<environment_context>",
                                          "<INSTRUCTIONS>", "<subagent_notification>")):
                continue
            if first_request:
                if DIARY_SYNC_MARKER in msg:
                    return None
                first_request = False
            try:
                stamp = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00")).astimezone()
            except (KeyError, ValueError, AttributeError):
                continue
            if stamp.date() != day:
                continue
            # 일부 버전은 동일 턴에서 두 이벤트 형식으로 같은 발화를 남긴다.
            other = "item_completed" if kind == "user_message" else "user_message"
            if pending.get((msg, other), 0):
                pending[msg, other] -= 1
                continue
            pending[msg, kind] = pending.get((msg, kind), 0) + 1
            last_time = stamp.replace(tzinfo=None)
            if len(messages) < 5:
                messages.append(msg[:200])
    if messages and isinstance(cwd, str):
        return {"path": cwd, "source": "Codex", "mtime": last_time, "messages": messages}


def find_codex_sessions(target_date):
    day = datetime.strptime(target_date, "%Y-%m-%d")
    root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    sessions = []
    for folder in ("sessions", "archived_sessions"):
        for filepath in (root / folder).rglob("rollout-*.jsonl"):
            try:
                # 시작 디렉터리가 전날이어도 오늘 재개한 세션을 포함한다.
                if filepath.stat().st_mtime < day.timestamp():
                    continue
                session = codex_session(filepath, day.date())
            except FileNotFoundError:
                continue  # 실행 중 보관 폴더로 이동된 경우
            if session:
                sessions.append(session)
    return sessions


def main():
    if len(sys.argv) > 1:
        target_date = sys.argv[1]
    else:
        target_date = datetime.now().strftime("%Y-%m-%d")

    print(f"# 세션 요약 - {target_date}\n")

    sessions = find_claude_sessions(target_date) + find_codex_sessions(target_date)
    sessions.sort(key=lambda s: s["mtime"])
    if not sessions:
        print("세션 없음")
        return

    by_category = {}
    for s in sessions:
        cat = classify_path(s["path"])
        by_category.setdefault(cat, []).append(s)

    for cat, items in by_category.items():
        print(f"## {cat}\n")
        for i, s in enumerate(items, 1):
            project_name = Path(s["path"]).name or s["path"]
            time_str = s["mtime"].strftime("%H:%M")
            messages = s["messages"] if s["source"] == "Codex" else extract_user_messages(s["file"])
            if s["source"] == "Codex":
                project_name += " [Codex]"

            print(f"**{i}. {project_name}** ({time_str})")
            if messages:
                for m in messages[:5]:
                    # 긴 메시지는 첫 줄만
                    first_line = m.split("\n")[0][:120]
                    print(f"  - {first_line}")
            else:
                print("  - (메시지 없음)")
            print()

    print(f"---\n총 {len(sessions)}개 세션")


if __name__ == "__main__":
    main()
