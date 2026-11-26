#!/usr/bin/env python3
import argparse
import datetime as dt
import fcntl
import json
from pathlib import Path


DEFAULT_FEEDBACK_PATH = Path("/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/feedback.jsonl")
DEFAULT_RUNS_DIR = Path("/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/runs")


def read_events(path):
    if not path.exists():
        return []
    events = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def load_run_metadata(run_id):
    metadata_path = DEFAULT_RUNS_DIR / f"{run_id}.json"
    if not metadata_path.exists():
        return {}
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--signal", required=True, choices=["like", "dislike"])
    parser.add_argument("--source", default="telegram")
    parser.add_argument("--feedback-path", default=str(DEFAULT_FEEDBACK_PATH))
    parser.add_argument("--note", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = Path(args.feedback_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    idempotency_key = f"feedback:{args.run_id}"

    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.touch()
    with lock_path.open("r+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        events = read_events(path)

        for event in events:
            if event.get("idempotency_key") == idempotency_key:
                print(json.dumps({
                    "ok": True,
                    "deduped": True,
                    "idempotency_key": idempotency_key,
                    "existing_signal": event.get("signal"),
                }, ensure_ascii=False))
                return

        prior = next((event for event in reversed(events) if event.get("run_id") == args.run_id), {})
        run_metadata = load_run_metadata(args.run_id)
        context = run_metadata.get("context", {})
        record = {
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
            "run_id": args.run_id,
            "status": "resolved",
            "signal": args.signal,
            "source": args.source,
            "idempotency_key": idempotency_key,
            "angle": prior.get("angle") or context.get("angle"),
            "title": prior.get("title") or context.get("title"),
            "visual_style": prior.get("visual_style") or context.get("visual_style"),
            "url": prior.get("url") or run_metadata.get("image_url") or run_metadata.get("upload_url"),
            "location": prior.get("location") or context.get("location"),
            "progress": prior.get("progress") or context.get("progress"),
        }
        if args.note:
            record["note"] = args.note

        if not args.dry_run:
            with path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(json.dumps({"ok": True, "deduped": False, "idempotency_key": idempotency_key, "record": record}, ensure_ascii=False))


if __name__ == "__main__":
    main()
