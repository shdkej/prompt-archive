#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import urllib.request
from pathlib import Path


LOCAL_DASHBOARD = Path("/home/ubuntu/workspace/space/infra-aws-static-sites/sites/travel/dist/travel-data.json")
PUBLIC_DASHBOARD_URL = "https://travel.aws.shdkej.com/travel-data.json"
DATA_DIR = Path("/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback")


def parse_datetime(value):
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_dashboard():
    if LOCAL_DASHBOARD.exists():
        return json.loads(LOCAL_DASHBOARD.read_text(encoding="utf-8")), str(LOCAL_DASHBOARD)
    with urllib.request.urlopen(PUBLIC_DASHBOARD_URL, timeout=20) as response:
        return json.loads(response.read().decode("utf-8")), PUBLIC_DASHBOARD_URL


def find_current_route(route, current):
    if not isinstance(route, list) or not current:
        return None, None
    current_label = current.get("location")
    current_query = current.get("mapQuery", "")
    for index, stop in enumerate(route):
        city = stop.get("city") or stop.get("name")
        country = stop.get("country")
        if city == current_label or (city and city in current_query and country and country in current_query):
            return index, stop
    return None, None


def build_previous_move(route, current_index, current_stop):
    if current_index is None or current_index <= 0 or not current_stop:
        return ""
    previous = route[current_index - 1]
    previous_label = ", ".join(part for part in [previous.get("city"), previous.get("country")] if part)
    current_label = ", ".join(part for part in [current_stop.get("city"), current_stop.get("country")] if part)
    transport = current_stop.get("transportIn")
    if transport:
        return f"{transport} 이동 후 {current_label} 체류 중"
    return f"{previous_label}에서 {current_label}로 이동"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--out", default=None)
    parser.add_argument("--max-age-hours", type=int, default=36)
    parser.add_argument("--title", default="오늘의 여행 기준")
    parser.add_argument("--copy", default="지금 있는 도시에서 오늘의 선택 기준이 조금 더 선명해졌습니다.")
    parser.add_argument("--angle", default="여행은 장소를 지나는 일이 아니라 기준을 조정하는 일이다")
    parser.add_argument("--visual-style", default="warm-minimal-travel-note")
    args = parser.parse_args()

    data, source = load_dashboard()
    generated_at = parse_datetime(data.get("generatedAt"))
    now = dt.datetime.now(dt.timezone.utc)
    if not generated_at:
        raise SystemExit(json.dumps({"ok": False, "reason": "missing_generatedAt", "source": source}, ensure_ascii=False))
    age_hours = (now - generated_at.astimezone(dt.timezone.utc)).total_seconds() / 3600
    if age_hours > args.max_age_hours:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "reason": "stale_travel_dashboard",
                    "source": source,
                    "generatedAt": data.get("generatedAt"),
                    "age_hours": round(age_hours, 2),
                },
                ensure_ascii=False,
            )
        )

    current = data.get("current") or {}
    route = data.get("route") or []
    current_index, current_stop = find_current_route(route, current)
    location = current.get("mapQuery") or ", ".join(
        part for part in [(current_stop or {}).get("city"), (current_stop or {}).get("country")] if part
    ) or current.get("location")
    total = len(route)
    segment_number = current_index + 1 if current_index is not None else None
    progress = f"세계여행 {segment_number}/{total} 구간" if segment_number and total else "세계여행 진행 중"

    context = {
        "date": args.date,
        "location": location,
        "progress": progress,
        "previous_move": build_previous_move(route, current_index, current_stop),
        "angle": args.angle,
        "title": args.title,
        "copy": args.copy,
        "visual_style": args.visual_style,
        "location_source": "travel-dashboard",
        "location_confidence": "confirmed-public-safe",
        "source_checked": source,
        "dashboard_generated_at": data.get("generatedAt"),
        "dashboard_current": current,
    }

    out = Path(args.out) if args.out else DATA_DIR / f"{args.date}-context.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "context_path": str(out), "context": context}, ensure_ascii=False))


if __name__ == "__main__":
    main()
