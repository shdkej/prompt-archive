#!/usr/bin/env python3
import argparse
import importlib.util
import json
import logging
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from scrapling.fetchers import Fetcher


logging.getLogger("scrapling").setLevel(logging.WARNING)

ROOT = Path("/home/ubuntu/.openclaw/workspace-hj")
SKILL_DIR = ROOT / "skills/worldpackers-scraper"
EXTRACTOR = SKILL_DIR / "scripts/extract_worldpackers.py"
TMP = ROOT / "tmp-worldpackers-run/current"
STATE = ROOT / "memory/worldpackers-eu-dev-seen.json"
LATEST = ROOT / "memory/worldpackers-eu-dev-latest.json"
CRON_JOB_ID = "38c3f9fa-e5b8-4d7d-9392-3ff9f32c170e"

SEARCH_URLS = [
    "https://www.worldpackers.com/search/europe/skill_web_development",
    "https://www.worldpackers.com/search/europe/skill_web_development?order_by=newest",
    "https://www.worldpackers.com/search/europe/1000/skill_web_development",
    "https://www.worldpackers.com/search/europe/1000/skill_web_development?order_by=newest",
]
SEARCH_URLS.extend(
    f"https://www.worldpackers.com/search/europe/skill_web_development?page={page}"
    for page in range(2, 6)
)
SEARCH_URLS.extend(
    f"https://www.worldpackers.com/search/europe/skill_web_development?order_by=newest&page={page}"
    for page in range(2, 6)
)

DEV_RE = re.compile(
    r"\b(word\s*press|wordpress|woocommerce|website|web\s*(site|dev|developer|development|design|designer)|"
    r"coding|programming|software|app\s*(dev|development)?|information technology|network engineer|"
    r"router|internet system|seo|google optimisation|google optimization|tech(nical)?)\b",
    re.I,
)
GENERIC_BAD_RE = re.compile(
    r"\b(clean|cleaner|housekeep|farm|gardening|kitchen|art retreat|child|animal|reception|bartend|painting|decorating)\b",
    re.I,
)


def load_extractor():
    spec = importlib.util.spec_from_file_location("worldpackers_extractor", EXTRACTOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load extractor: {EXTRACTOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc


def latest_cron_delivery_status():
    try:
        result = subprocess.run(
            ["openclaw", "cron", "runs", "--id", CRON_JOB_ID, "--limit", "1"],
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    try:
        entries = json.loads(result.stdout).get("entries") or []
    except Exception:
        return None
    if not entries:
        return None
    return entries[0]


def promote_delivered_pending(state, seen):
    pending = [str(item) for item in state.get("pendingNew", [])]
    if not pending:
        return []

    latest = latest_cron_delivery_status()
    if latest and latest.get("delivered") is True and latest.get("status") == "ok":
        seen.update(pending)
        state["pendingNew"] = []
        state["pendingAnnouncements"] = []
        state.pop("pendingNewSinceUtc", None)
        state["lastPendingPromotedUtc"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        return pending
    return []


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def card_id(url):
    match = re.search(r"/positions/(\d+)", url or "")
    return match.group(1) if match else url


def safe_name(url):
    without_scheme = re.sub(r"^https?://", "", url)
    return re.sub(r"[^A-Za-z0-9]+", "_", without_scheme).strip("_") + ".json"


def fetch_cards(extractor):
    TMP.mkdir(parents=True, exist_ok=True)
    rows = []
    failures = []

    for url in SEARCH_URLS:
        try:
            items = extractor.extract(url)
            if not isinstance(items, list):
                raise RuntimeError(f"unexpected extractor result: {type(items).__name__}")
            rows.extend(items)
            write_json(TMP / safe_name(url), items)
        except Exception as exc:
            failures.append(f"{url}: {exc!r}")

    if failures:
        raise RuntimeError("Search extraction failed: " + " | ".join(failures[:3]))

    unique = {}
    for row in rows:
        url = row.get("url") or ""
        if "/positions/" in url:
            unique[url] = row
    if not unique:
        raise RuntimeError("Search extraction returned zero position cards")
    return list(unique.values())


def parse_json_ld(page):
    for raw in page.css('script[type="application/ld+json"]::text').getall():
        try:
            data = json.loads(raw)
        except Exception:
            continue
        if isinstance(data, dict):
            return data
    return {}


def enrich_detail(row):
    out = dict(row)
    out["id"] = card_id(row.get("url"))

    page = Fetcher.get(row["url"], timeout=30)
    texts = [clean(t) for t in page.css("::text").getall()]
    texts = [t for t in texts if t]
    json_ld = parse_json_ld(page)

    out["summary"] = clean(json_ld.get("title")) or out.get("title")
    out["roleSummary"] = clean(json_ld.get("description"))
    out["responsibilities"] = clean(json_ld.get("responsibilities"))

    address = ((json_ld.get("jobLocation") or {}).get("address") or {})
    out["city"] = clean(address.get("addressLocality"))
    out["region"] = clean(address.get("addressRegion"))
    out["country"] = clean(address.get("addressCountry"))

    if not out.get("roleSummary") and "The Experience" in texts:
        index = texts.index("The Experience")
        if index + 1 < len(texts):
            out["roleSummary"] = texts[index + 1]

    joined = " | ".join(texts[:260])
    count_match = re.search(r"\((\d+) reviews?\)", joined, re.I) or re.search(r"\b(\d+) Reviews\b", joined)
    if count_match:
        out["reviewCount"] = int(count_match.group(1))

    score = None
    if row.get("rating"):
        try:
            score = float(row["rating"])
        except Exception:
            score = None
    if score is None:
        for text in texts:
            if re.fullmatch(r"\d+(?:\.\d)?", text):
                value = float(text)
                if 0 <= value <= 5:
                    score = value
                    break
    if score is not None:
        out["reviewScore"] = score

    for text in texts:
        if text.startswith("Hosted by "):
            out["host"] = clean(text.replace("Hosted by ", "", 1))
            break

    return out


def is_dev(item):
    haystack = " ".join(str(item.get(key, "") or "") for key in ("summary", "roleSummary", "responsibilities", "title"))
    if not DEV_RE.search(haystack):
        return False
    if GENERIC_BAD_RE.search(haystack) and not re.search(
        r"\b(wordpress|website|web|woocommerce|coding|software|app|network|router|internet|seo|google optim)",
        haystack,
        re.I,
    ):
        return False
    return True


def classify(item, seen):
    score = item.get("reviewScore")
    count = item.get("reviewCount")
    if not is_dev(item):
        return "excluded-not-clearly-dev"
    if score is None or count is None or float(score) < 4.5 or int(count) < 5:
        return "excluded-low-or-insufficient-reviews"
    if str(item.get("id")) in seen:
        return "previously-reported"
    return "new-qualifying"


def format_item(item):
    place = ", ".join(part for part in (item.get("country"), item.get("city") or item.get("location")) if part)
    host = item.get("host") or "Host not shown"
    summary = item.get("summary") or item.get("title") or "Development opportunity"
    score = item.get("reviewScore")
    count = item.get("reviewCount")
    rating = f"{score:.1f}/5, {count} reviews" if score is not None and count is not None else "reviews not parsed"
    return f"- {place} - {host}: {summary} - {rating} - {item.get('url')}"


def run(dry_run=False):
    extractor = load_extractor()
    state = load_json(STATE, {"seen": []})
    seen = set(map(str, state.get("seen", [])))
    promoted = promote_delivered_pending(state, seen)

    cards = fetch_cards(extractor)
    detailed = []
    detail_errors = []

    for row in cards:
        try:
            item = enrich_detail(row)
            item["status"] = classify(item, seen)
        except Exception as exc:
            item = dict(row)
            item["id"] = card_id(row.get("url"))
            item["status"] = "detail-error"
            item["error"] = repr(exc)
            detail_errors.append(f"{row.get('url')}: {exc!r}")
        detailed.append(item)
        time.sleep(0.2)

    if detail_errors:
        raise RuntimeError("Detail fetch failed: " + " | ".join(detail_errors[:3]))

    detailed.sort(
        key=lambda item: (
            item.get("status") != "new-qualifying",
            -(item.get("reviewScore") or 0),
            -(item.get("reviewCount") or 0),
            item.get("country") or "",
            item.get("city") or item.get("location") or "",
        )
    )
    new = [item for item in detailed if item.get("status") == "new-qualifying"]
    stored_pending = state.get("pendingAnnouncements", [])
    stored_pending_by_id = {str(item.get("id")): item for item in stored_pending if item.get("id")}
    pending_ids = set(map(str, state.get("pendingNew", []))) | set(stored_pending_by_id)
    current_by_id = {str(item.get("id")): item for item in detailed if item.get("id")}
    pending_items = [current_by_id.get(item_id) or stored_pending_by_id[item_id] for item_id in sorted(pending_ids) if current_by_id.get(item_id) or stored_pending_by_id.get(item_id)]
    to_announce = pending_items + [item for item in new if str(item.get("id")) not in pending_ids]

    if to_announce and not dry_run:
        state["pendingNew"] = [str(item["id"]) for item in to_announce]
        state["pendingAnnouncements"] = to_announce
        state["pendingNewSinceUtc"] = state.get("pendingNewSinceUtc") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    elif not pending_ids and not dry_run:
        state["pendingNew"] = []
        state["pendingAnnouncements"] = []
        state.pop("pendingNewSinceUtc", None)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    state.update(
        {
            "seen": sorted(seen, key=lambda value: int(value) if str(value).isdigit() else 10**12),
            "lastRunUtc": now,
            "lastNew": [item["id"] for item in new],
            "lastAnnounced": [item["id"] for item in to_announce],
            "lastPromotedSeen": promoted,
            "notes": (
                f"{now} run: checked {len(cards)} unique Worldpackers Europe web-development cards. "
                f"Strict filter: clearly dev/IT/web task, rating >=4.5, review count >=5. "
                f"New qualifying: {len(new)}. Pending announcement: {len(to_announce)}. "
                f"Promoted after delivery: {len(promoted)}. Detail errors: {len(detail_errors)}."
            ),
            "lastCandidates": detailed,
        }
    )

    if not dry_run:
        write_json(STATE, state)
        write_json(
            LATEST,
            {
                "lastRunUtc": now,
                "totalUnique": len(cards),
                "new": new,
                "announced": to_announce,
                "promotedSeen": promoted,
                "detailErrors": len(detail_errors),
                "candidates": detailed,
            },
        )

    return to_announce


def main():
    parser = argparse.ArgumentParser(description="Monitor Worldpackers Europe development opportunities")
    parser.add_argument("--dry-run", action="store_true", help="Do not update state files")
    args = parser.parse_args()

    try:
        new = run(dry_run=args.dry_run)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not new:
        print("NO_REPLY")
        return 0

    print("\n".join(format_item(item) for item in new))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
