#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

from scrapling.fetchers import Fetcher

BASE = "https://www.trustedhousesitters.com"
LISTING_ROOT = f"{BASE}/house-and-pet-sitting-assignments/"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def normalize_country_url(country: str) -> str:
    country = country.strip().strip("/")
    return f"{LISTING_ROOT}{country}/"


def looks_like_listing(href: str) -> bool:
    return "/house-and-pet-sitting-assignments/" in href and "/l/" in href


def parse_card(anchor):
    href = anchor.attrib.get("href", "")
    texts = [clean(t) for t in anchor.css("::text").getall()]
    texts = [t for t in texts if t]

    tags = []
    while texts and texts[0] in {"New", "Last Min"}:
        tags.append(texts.pop(0))

    title = texts[0] if texts else None
    date_range = next((t for t in texts if re.search(r"\b20\d{2}\b", t) and " - " in t), None)
    status = next((t for t in texts if t in {"reviewing", "confirmed"}), None)
    location = next((t for t in texts if ", " in t and len(t) < 80 and t != date_range), None)

    pet_parts = []
    for i, t in enumerate(texts):
        if re.fullmatch(r"\d+", t) and i + 1 < len(texts):
            nxt = texts[i + 1]
            if nxt in {"dog", "dogs", "cat", "cats", "fish", "bird", "birds", "horse", "horses", "rabbit", "rabbits"}:
                pet_parts.append(f"{t} {nxt}")
        elif t in {"dog", "dogs", "cat", "cats", "fish", "bird", "birds", "horse", "horses", "rabbit", "rabbits"}:
            if not pet_parts or not pet_parts[-1].endswith(t):
                pet_parts.append(t)

    return {
        "title": title,
        "location": location,
        "date_range": date_range,
        "status": status,
        "pet_summary": ", ".join(dict.fromkeys(pet_parts)) if pet_parts else None,
        "tags": tags,
        "url": urljoin(BASE, href),
    }


def extract_page(url: str):
    page = Fetcher.get(url, timeout=30)
    items = []
    seen = set()
    for a in page.css('a[href*="/house-and-pet-sitting-assignments/"]'):
        href = a.attrib.get("href", "")
        if not looks_like_listing(href) or href in seen:
            continue
        seen.add(href)
        items.append(parse_card(a))
    return items, page


def find_next_pages(page, current_url: str, limit: int):
    urls = []
    current_path = urlparse(current_url).path.rstrip("/")
    for a in page.css('a[href*="/house-and-pet-sitting-assignments/"]'):
        href = a.attrib.get("href", "")
        full = urljoin(BASE, href)
        if "?q=" not in full:
            continue
        if urlparse(full).path.rstrip("/") != current_path:
            continue
        if full not in urls:
            urls.append(full)
        if len(urls) >= limit:
            break
    return urls


def apply_keywords(rows, keywords):
    if not keywords:
        return rows
    keywords = [k.lower() for k in keywords]
    filtered = []
    for row in rows:
        hay = " ".join(str(row.get(k) or "") for k in ["title", "location", "date_range", "status", "pet_summary", "tags"]).lower()
        if all(k in hay for k in keywords):
            filtered.append(row)
    return filtered


def write_csv(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "location", "date_range", "status", "pet_summary", "tags", "url"])
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["tags"] = ", ".join(row.get("tags") or [])
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Extract TrustedHousesitters listing cards with Scrapling")
    parser.add_argument("--country", help="Country slug, e.g. united-kingdom, spain, portugal")
    parser.add_argument("--url", help="Direct listing URL")
    parser.add_argument("--pages", type=int, default=1, help="Number of listing pages to fetch (default: 1)")
    parser.add_argument("--keyword", action="append", default=[], help="Repeatable keyword filter")
    parser.add_argument("--json-out")
    parser.add_argument("--csv-out")
    args = parser.parse_args()

    if not args.url and not args.country:
        parser.error("Provide either --url or --country")

    start_url = args.url or normalize_country_url(args.country)
    page_urls = [start_url]
    all_rows = []
    seen_urls = set()

    rows, first_page = extract_page(start_url)
    all_rows.extend(rows)
    seen_urls.update(r["url"] for r in rows)

    if args.pages > 1:
        for next_url in find_next_pages(first_page, start_url, args.pages - 1):
            rows, _ = extract_page(next_url)
            for row in rows:
                if row["url"] in seen_urls:
                    continue
                seen_urls.add(row["url"])
                all_rows.append(row)

    all_rows = apply_keywords(all_rows, args.keyword)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_out:
        write_csv(Path(args.csv_out), all_rows)

    print(json.dumps({"count": len(all_rows), "items": all_rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
