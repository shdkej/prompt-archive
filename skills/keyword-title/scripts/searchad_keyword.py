#!/usr/bin/env python3
"""
네이버 검색광고 키워드도구 API → keyword-title 콘텐츠 모드용 절대 검색량 + 연관 키워드.

데이터랩(상대값 0~100)과 달리 **월 절대 검색량 + 경쟁도(compIdx)**를 준다.
콘텐츠 모드(blog·threads)의 Searchability·LongTail 신호를 절대값으로 보강하고,
연관 키워드 추천으로 시드 키워드 발굴도 한다.

종속성 0 (표준 라이브러리만). 키 없으면 ok=false → 스킬은 LLM 추론 fallback.

사용:
  python3 searchad_keyword.py --keywords "신혼여행,세계여행" [--related 10]

키 위치 (우선순위): 환경변수 → skills/keyword-title/.env
  NAVER_SEARCH_ACCESS_LICENSE
  NAVER_SEARCH_SECRET_KEY
  NAVER_SEARCH_CUSTOMER_ID   ← 검색광고 > 도구 > API 사용관리 의 고객 ID(숫자)
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

BASE = "https://api.searchad.naver.com"
URI = "/keywordstool"

KEYS = ("NAVER_SEARCH_ACCESS_LICENSE", "NAVER_SEARCH_SECRET_KEY", "NAVER_SEARCH_CUSTOMER_ID")


def load_keys():
    vals = {k: os.environ.get(k) for k in KEYS}
    if all(vals.values()):
        return vals
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            if k in vals and not vals[k]:
                vals[k] = v.strip().strip('"').strip("'")
    return vals


def sign(secret, timestamp, method, uri):
    msg = f"{timestamp}.{method}.{uri}"
    digest = hmac.new(secret.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def call(vals, hint_keywords):
    ts = str(int(time.time() * 1000))
    sig = sign(vals["NAVER_SEARCH_SECRET_KEY"], ts, "GET", URI)
    # 검색광고 API는 공백 없는 키워드를 콤마로
    q = urllib.parse.urlencode({"hintKeywords": ",".join(hint_keywords), "showDetail": "1"})
    req = urllib.request.Request(f"{BASE}{URI}?{q}", method="GET")
    req.add_header("X-Timestamp", ts)
    req.add_header("X-API-KEY", vals["NAVER_SEARCH_ACCESS_LICENSE"])
    req.add_header("X-Customer", vals["NAVER_SEARCH_CUSTOMER_ID"])
    req.add_header("X-Signature", sig)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_int(v):
    """monthlyXxxQcCnt 는 숫자거나 '< 10' 문자열일 수 있다."""
    if isinstance(v, int):
        return v
    s = str(v).replace("<", "").replace(",", "").strip()
    try:
        return int(s)
    except ValueError:
        return 0


def volume_signal(total):
    if total >= 100_000:
        return 1.0
    if total >= 30_000:
        return 0.8
    if total >= 10_000:
        return 0.6
    if total >= 1_000:
        return 0.4
    return 0.2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", required=True, help="콤마 구분, hint 키워드")
    ap.add_argument("--related", type=int, default=10, help="연관 키워드 추천 상위 N")
    args = ap.parse_args()

    hints = [k.strip().replace(" ", "") for k in args.keywords.split(",") if k.strip()]
    if not hints:
        print(json.dumps({"ok": False, "reason": "no_keywords"}, ensure_ascii=False))
        return

    vals = load_keys()
    missing = [k for k in KEYS if not vals.get(k)]
    if missing:
        print(json.dumps({"ok": False, "reason": "no_api_key", "missing": missing,
                          "hint": "검색광고 > 도구 > API 사용관리 의 고객 ID(NAVER_SEARCH_CUSTOMER_ID) 포함 3개 필요. "
                                  "없으면 스킬은 LLM 추론으로 진행."}, ensure_ascii=False))
        return

    try:
        raw = call(vals, hints)
    except urllib.error.HTTPError as e:
        print(json.dumps({"ok": False, "reason": "http_error", "status": e.code,
                          "body": e.read().decode("utf-8", "ignore")[:400]}, ensure_ascii=False))
        return
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "reason": "request_failed", "error": str(e)}, ensure_ascii=False))
        return

    rows = raw.get("keywordList", [])
    hint_set = {h.upper() for h in hints}

    exact, related = [], []
    for r in rows:
        kw = r.get("relKeyword", "")
        pc = to_int(r.get("monthlyPcQcCnt", 0))
        mo = to_int(r.get("monthlyMobileQcCnt", 0))
        total = pc + mo
        item = {"keyword": kw, "monthly_total": total, "pc": pc, "mobile": mo,
                "comp": r.get("compIdx", ""), "volume_signal": volume_signal(total)}
        if kw.replace(" ", "").upper() in hint_set:
            exact.append(item)
        else:
            related.append(item)

    related.sort(key=lambda x: x["monthly_total"], reverse=True)
    print(json.dumps({"ok": True, "exact": exact, "related_top": related[: args.related]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
