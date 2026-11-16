#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests


WORKSPACE = Path("/home/ubuntu/.openclaw/workspace")
DATA_DIR = Path("/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback")
REPORT_DIR = Path("/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/travel-content-feedback")
RUNS_DIR = DATA_DIR / "runs"
FEEDBACK_PATH = DATA_DIR / "feedback.jsonl"
RENDER_SCRIPT = WORKSPACE / "skills/travel-content-feedback/scripts/render_daily_test.py"


def load_env_file(path):
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def run_json(argv):
    completed = subprocess.run(argv, check=True, text=True, capture_output=True)
    try:
        return json.loads(completed.stdout.strip().splitlines()[-1])
    except Exception as exc:
        raise RuntimeError(f"command did not return JSON: {' '.join(argv)}\n{completed.stdout}\n{completed.stderr}") from exc


def run_text(argv):
    completed = subprocess.run(argv, check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def require_public_safe_context(context):
    confidence = context.get("location_confidence")
    source = context.get("location_source")
    allowed_sources = {"travel-dashboard", "hj", "hj:travel-dashboard", "locationless-safe"}
    allowed_confidence = {"confirmed-public-safe", "high", "locationless-safe"}
    if source not in allowed_sources or confidence not in allowed_confidence:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "status": "skipped",
                    "reason": "location_context_not_confirmed_public_safe",
                    "location_source": source,
                    "location_confidence": confidence,
                },
                ensure_ascii=False,
            )
        )
    if confidence == "locationless-safe" and context.get("location"):
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "status": "skipped",
                    "reason": "locationless_safe_context_must_not_include_location",
                    "location_source": source,
                    "location_confidence": confidence,
                },
                ensure_ascii=False,
            )
        )


def verify_url(url):
    if not url:
        raise RuntimeError("upload_url is empty")
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type"),
        "content_length": response.headers.get("content-length"),
    }


def extract_message_id(result_text):
    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        return None
    for key in ("messageId", "message_id", "id"):
        if data.get(key):
            return str(data[key])
    if isinstance(data.get("message"), dict):
        for key in ("messageId", "message_id", "id"):
            if data["message"].get(key):
                return str(data["message"][key])
    return None


def append_pending_feedback(run_id, context, upload_url, feedback_mode):
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    pending_key = f"pending:{run_id}"
    if FEEDBACK_PATH.exists():
        for line in FEEDBACK_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("idempotency_key") == pending_key:
                return

    record = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "run_id": run_id,
        "status": "pending",
        "signal": "pending",
        "source": "daily-runner",
        "idempotency_key": pending_key,
        "angle": context.get("angle"),
        "title": context.get("title"),
        "visual_style": context.get("visual_style"),
        "url": upload_url,
        "location": context.get("location"),
        "progress": context.get("progress"),
        "feedback_mode": feedback_mode,
    }
    with FEEDBACK_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def callback_token(run_id, signal):
    short_id = run_id.rsplit("-", 1)[-1]
    signal_code = {"like": "l", "dislike": "d"}[signal]
    token = f"tf:{signal_code}:{short_id}"
    # Telegram callback_data is limited to 64 UTF-8 bytes.
    if len(token.encode("utf-8")) > 64:
        raise ValueError(f"Telegram callback token exceeds 64 bytes: {len(token.encode('utf-8'))}")
    return token


def send_to_telegram(run_id, context, upload_url, target, dry_run):
    if context.get("location_confidence") == "locationless-safe":
        caption = (
            "오늘 여행 콘텐츠 테스트 1장입니다.\n"
            "- 위치 노출을 피한 비위치형 버전입니다.\n"
            "- 마음에 들면 좋아요, 아니면 안돼요를 눌러주세요."
        )
    else:
        caption = (
            "오늘 여행 콘텐츠 테스트 1장입니다.\n"
            f"- 맥락: {context.get('progress')} · {context.get('location')}\n"
            "- 마음에 들면 좋아요, 아니면 안돼요를 눌러주세요."
        )
    presentation = {
        "title": "오늘 콘텐츠 테스트",
        "tone": "info",
        "blocks": [
            {"type": "text", "text": "이 방향이 마스터 계정에 맞는지 한 번만 판정해주세요."},
            {
                "type": "buttons",
                "buttons": [
                    {
                        "label": "좋아요",
                        # The feedback bridge matches Telegram's raw callback_data.
                        # action:callback is wrapped by OpenClaw as tgcb1:... .
                        "value": callback_token(run_id, "like"),
                        "style": "success",
                    },
                    {
                        "label": "안돼요",
                        "value": callback_token(run_id, "dislike"),
                        "style": "danger",
                    },
                ],
            },
        ],
    }
    if dry_run:
        return {
            "image_message_id": "dry-run",
            "feedback_message_id": "dry-run",
            "feedback_controls": "presentation-inline-buttons",
            "caption": caption,
            "presentation": presentation,
        }

    image_result = run_text(
        [
            "openclaw",
            "message",
            "send",
            "--channel",
            "telegram",
            "--target",
            target,
            "--media",
            upload_url,
            "--message",
            caption,
            "--json",
        ]
    )
    control_result = run_text(
        [
            "openclaw",
            "message",
            "send",
            "--channel",
            "telegram",
            "--target",
            target,
            "--message",
            "피드백을 선택해주세요.",
            "--presentation",
            json.dumps(presentation, ensure_ascii=False),
            "--json",
        ]
    )
    return {
        "image_message_id": extract_message_id(image_result),
        "feedback_message_id": extract_message_id(control_result),
        "feedback_controls": "presentation-inline-buttons",
        "image_send_result": image_result,
        "feedback_send_result": control_result,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-json", required=True)
    parser.add_argument("--target", default="433493318")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_env_file(WORKSPACE / ".env")
    load_env_file(Path("/home/ubuntu/.env"))

    context_path = Path(args.context_json)
    context = json.loads(context_path.read_text(encoding="utf-8"))
    require_public_safe_context(context)

    render_out_dir = Path(tempfile.mkdtemp(prefix="travel-content-feedback-dry-run-")) if args.dry_run else REPORT_DIR
    render_result = run_json(
        [
            sys.executable,
            str(RENDER_SCRIPT),
            "--context-json",
            str(context_path),
            "--out-dir",
            str(render_out_dir),
        ]
        + (["--no-upload"] if args.dry_run else [])
    )
    upload_url = render_result.get("upload_url")
    url_check = {"status": "dry-run"} if args.dry_run else verify_url(upload_url)
    send_result = send_to_telegram(render_result["run_id"], context, upload_url, args.target, args.dry_run)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_metadata = {
        "run_id": render_result["run_id"],
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "context_path": str(context_path),
        "context": context,
        "image_path": render_result["image_path"],
        "metadata_path": render_result["metadata_path"],
        "upload_url": upload_url,
        "image_url": upload_url,
        "url_check": url_check,
        "telegram": send_result,
        "callback_values": [
            callback_token(render_result["run_id"], "like"),
            callback_token(render_result["run_id"], "dislike"),
        ],
        "callback_map": {
            callback_token(render_result["run_id"], "like"): {
                "run_id": render_result["run_id"],
                "signal": "like",
            },
            callback_token(render_result["run_id"], "dislike"): {
                "run_id": render_result["run_id"],
                "signal": "dislike",
            },
        },
    }
    if args.dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "run_id": render_result["run_id"], "metadata": run_metadata}, ensure_ascii=False))
        return

    run_path = RUNS_DIR / f"{render_result['run_id']}.json"
    run_path.write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    append_pending_feedback(render_result["run_id"], context, upload_url, send_result["feedback_controls"])

    send_log_path = DATA_DIR / f"{context.get('date', dt.date.today().isoformat())}-send-log.json"
    send_log_path.write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "run_id": render_result["run_id"], "run_path": str(run_path), "send_log_path": str(send_log_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
