#!/usr/bin/env python3
"""
네이버 데이터랩 검색어트렌드 → keyword-title 스킬용 Velocity/Direction 신호.

종속성 0 (표준 라이브러리만). keyword-title 스킬의 콘텐츠/유튜브 모드가
Velocity·Direction을 LLM 추정 대신 실측으로 교체할 때 호출한다.

키가 없으면 ok=false 를 반환하고, 스킬은 기존 LLM 추론으로 fallback 한다.

사용:
  python3 datalab_trend.py --keywords "신혼여행,세계여행" [--months 6] [--unit week]

키 위치 (우선순위):
  1) 환경변수 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET
  2) skills/keyword-title/.env  (NAVER_CLIENT_ID=... / NAVER_CLIENT_SECRET=...)

출력: JSON (stdout). 신호는 0.0~1.0 으로 정규화되어 signals-*.md 산식에 바로 투입.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date, timedelta
from pathlib import Path

API_URL = "https://openapi.naver.com/v1/datalab/search"


def load_keys():
    cid = os.environ.get("NAVER_CLIENT_ID")
    secret = os.environ.get("NAVER_CLIENT_SECRET")
    if cid and secret:
        return cid, secret
    # .env fallback (스킬 디렉토리 기준)
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            v = v.strip().strip('"').strip("'")
            if k.strip() == "NAVER_CLIENT_ID" and not cid:
                cid = v
            elif k.strip() == "NAVER_CLIENT_SECRET" and not secret:
                secret = v
    return cid, secret


def call_datalab(cid, secret, keywords, start, end, unit):
    groups = [{"groupName": kw, "keywords": [kw]} for kw in keywords[:5]]
    body = json.dumps(
        {"startDate": start, "endDate": end, "timeUnit": unit, "keywordGroups": groups}
    ).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, method="POST")
    req.add_header("X-Naver-Client-Id", cid)
    req.add_header("X-Naver-Client-Secret", secret)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_signals(series):
    """ratio 시계열 → Velocity/Direction 신호 (signals-*.md 매핑)."""
    ratios = [pt["ratio"] for pt in series]
    n = len(ratios)
    if n < 4:
        return {
            "velocity_signal": 0.5,
            "direction_signal": 0.3,
            "note": "데이터 포인트 부족(노이즈 큼) — LLM 추론 병행 권장",
            "avg_ratio": round(sum(ratios) / n, 2) if n else 0,
        }
    half = n // 2
    prev_avg = sum(ratios[:half]) / half
    recent_avg = sum(ratios[half:]) / (n - half)
    change = (recent_avg - prev_avg) / prev_avg if prev_avg > 0 else 0.0

    # Velocity (signals-content.md §3): 명확 상승 1.0 / 모호 0.5 / 하락·포화 0.2
    if change >= 0.15:
        velocity = 1.0
    elif change >= -0.05:
        velocity = 0.5
    else:
        velocity = 0.2

    # Direction (signals-content.md §3): 상승 초기 1.0 / 중기 0.6 / 정체 0.3 / 하락 0.1
    if change >= 0.30:
        direction = 1.0
    elif change >= 0.10:
        direction = 0.6
    elif change >= -0.05:
        direction = 0.3
    else:
        direction = 0.1

    avg_ratio = sum(ratios) / n
    return {
        "velocity_signal": velocity,
        "direction_signal": direction,
        "change_ratio": round(change, 3),
        "recent_avg": round(recent_avg, 2),
        "prev_avg": round(prev_avg, 2),
        "avg_ratio": round(avg_ratio, 2),
        # 평균 ratio가 너무 낮으면(<5) 검색량 자체가 적어 신호 신뢰도 낮음
        "low_volume_warning": avg_ratio < 5,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", required=True, help="콤마 구분, 최대 5개")
    ap.add_argument("--months", type=int, default=6, help="조회 기간(개월), 기본 6")
    ap.add_argument("--unit", default="week", choices=["date", "week", "month"])
    args = ap.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not keywords:
        print(json.dumps({"ok": False, "reason": "no_keywords"}, ensure_ascii=False))
        return

    cid, secret = load_keys()
    if not cid or not secret:
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "no_api_key",
                    "hint": "NAVER_CLIENT_ID/SECRET 환경변수 또는 skills/keyword-title/.env 필요. "
                    "키 없으면 스킬은 LLM 추론(signals 기본값)으로 진행.",
                },
                ensure_ascii=False,
            )
        )
        return

    end = date.today()
    start = end - timedelta(days=args.months * 30)
    try:
        raw = call_datalab(cid, secret, keywords, start.isoformat(), end.isoformat(), args.unit)
    except urllib.error.HTTPError as e:
        print(
            json.dumps(
                {"ok": False, "reason": "http_error", "status": e.code, "body": e.read().decode("utf-8", "ignore")[:300]},
                ensure_ascii=False,
            )
        )
        return
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": "request_failed", "error": str(e)}, ensure_ascii=False))
        return

    out = {"ok": True, "period": {"start": start.isoformat(), "end": end.isoformat(), "unit": args.unit}, "keywords": []}
    for result in raw.get("results", []):
        series = result.get("data", [])
        out["keywords"].append(
            {"keyword": result.get("title"), "points": len(series), "signals": to_signals(series)}
        )
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
