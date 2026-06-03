#!/usr/bin/env python3
"""
YouTube Data API v3 → keyword-title 유튜브 모드용 Searchability 신호.

종속성 0 (표준 라이브러리만). 키워드별로 상위 영상의 조회수·규모·신선도를 측정해
유튜브 제목 후보의 Searchability(실제로 검색·소비되는 말인지)를 실측한다.

키가 없으면 ok=false 를 반환하고, 스킬은 LLM 추론으로 fallback 한다.

사용:
  python3 youtube_keyword.py --keywords "신혼여행,세계여행" [--region KR] [--max 10]

키 위치 (우선순위):
  1) 환경변수 GOG_YOUTUBE_API_KEY
  2) skills/keyword-title/.env  (GOG_YOUTUBE_API_KEY=...)

쿼터 주의: search.list = 100 units/호출, videos.list = 1 unit. 일일 기본 10,000 units.
"""

import argparse
import json
import os
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from statistics import median

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def load_key():
    key = os.environ.get("GOG_YOUTUBE_API_KEY")
    if key:
        return key
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GOG_YOUTUBE_API_KEY="):
                return line.partition("=")[2].strip().strip('"').strip("'")
    return None


def _get(url, params):
    full = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, method="GET")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_videos(key, kw, region, maxn):
    data = _get(
        SEARCH_URL,
        {"part": "snippet", "q": kw, "type": "video", "regionCode": region,
         "maxResults": maxn, "order": "relevance", "key": key},
    )
    ids = [it["id"]["videoId"] for it in data.get("items", []) if it.get("id", {}).get("videoId")]
    total = data.get("pageInfo", {}).get("totalResults", 0)
    return ids, total


def video_stats(key, ids):
    if not ids:
        return []
    data = _get(VIDEOS_URL, {"part": "statistics,snippet", "id": ",".join(ids), "key": key})
    out = []
    for it in data.get("items", []):
        views = int(it.get("statistics", {}).get("viewCount", 0))
        pub = it.get("snippet", {}).get("publishedAt", "")
        out.append({"views": views, "publishedAt": pub})
    return out


def searchability_signal(median_view):
    """상위 영상 조회수 중앙값 → Searchability 0.0~1.0."""
    if median_view >= 100_000:
        return 1.0
    if median_view >= 30_000:
        return 0.8
    if median_view >= 10_000:
        return 0.6
    if median_view >= 3_000:
        return 0.4
    return 0.2


def recent_ratio(stats):
    """최근 365일 이내 발행 비율 (주제 활성도)."""
    if not stats:
        return 0.0
    cutoff = datetime.now(timezone.utc) - timedelta(days=365)
    recent = 0
    for s in stats:
        try:
            dt = datetime.fromisoformat(s["publishedAt"].replace("Z", "+00:00"))
            if dt >= cutoff:
                recent += 1
        except (ValueError, KeyError):
            pass
    return round(recent / len(stats), 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", required=True, help="콤마 구분")
    ap.add_argument("--region", default="KR")
    ap.add_argument("--max", type=int, default=10, help="키워드당 검색 영상 수")
    args = ap.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not keywords:
        print(json.dumps({"ok": False, "reason": "no_keywords"}, ensure_ascii=False))
        return

    key = load_key()
    if not key:
        print(json.dumps({"ok": False, "reason": "no_api_key",
                          "hint": "GOG_YOUTUBE_API_KEY 환경변수 또는 skills/keyword-title/.env 필요. "
                                  "키 없으면 스킬은 LLM 추론으로 진행."}, ensure_ascii=False))
        return

    out = {"ok": True, "region": args.region, "keywords": []}
    for kw in keywords:
        try:
            ids, total = search_videos(key, kw, args.region, args.max)
            stats = video_stats(key, ids)
        except urllib.error.HTTPError as e:
            print(json.dumps({"ok": False, "reason": "http_error", "status": e.code,
                              "body": e.read().decode("utf-8", "ignore")[:400]}, ensure_ascii=False))
            return
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"ok": False, "reason": "request_failed", "error": str(e)}, ensure_ascii=False))
            return

        views = sorted(s["views"] for s in stats)
        med = int(median(views)) if views else 0
        out["keywords"].append({
            "keyword": kw,
            "total_results": total,           # 대략 규모 (YouTube 추정치, 부정확)
            "sampled": len(stats),
            "median_view": med,
            "max_view": max(views) if views else 0,
            "recent_ratio": recent_ratio(stats),
            "searchability_signal": searchability_signal(med),
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
