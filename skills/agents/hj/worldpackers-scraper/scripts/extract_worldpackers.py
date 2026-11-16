#!/usr/bin/env python3
import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from scrapling.fetchers import Fetcher

BASE_URL = "https://www.worldpackers.com"
SKILL_SET = {
    "Content Writer",
    "Web Developer",
    "Web Designer",
    "Social Media",
    "Photography",
    "Teaching Languages",
    "Arts",
    "Kitchen Hand",
    "Farming",
    "Gardening",
    "Reception",
    "Housekeeping",
    "Bartending",
    "Child Care",
    "Animal Care",
    "Tour Guide",
    "Music",
    "Video Making",
    "SEO",
    "Marketing",
}
BADGE_HINTS = {
    "Top Host",
    "Higher approval",
    "Sustainable project",
    "Trending",
    "New host",
}


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def parse_card(card):
    texts = [clean(t) for t in card.css("::text").getall()]
    texts = [t for t in texts if t]
    href = urljoin(BASE_URL, card.attrib.get("href", ""))

    category = texts[0] if len(texts) > 0 else None
    location = texts[1] if len(texts) > 1 else None
    title = texts[2] if len(texts) > 2 else None

    hours = next((t for t in texts if re.fullmatch(r"\d+h/week", t)), None)
    duration = next((t for t in texts if re.search(r"week|month", t, re.I) and not re.fullmatch(r"\d+h/week", t)), None)
    accommodation = next((t for t in texts if any(x in t for x in ["Dorm", "Room", "Tent", "Cabin", "House"])), None)
    meals = next((t for t in texts if re.fullmatch(r"\d+ meals?", t, re.I)), None)
    rating = next((t for t in texts if re.fullmatch(r"\d(?:\.\d)?", t)), None)

    skills = [t for t in texts if t in SKILL_SET]
    badges = [t for t in texts if t in BADGE_HINTS]

    return {
        "category": category,
        "location": location,
        "title": title,
        "hours_per_week": hours,
        "duration": duration,
        "accommodation": accommodation,
        "meals": meals,
        "skills": skills,
        "rating": rating,
        "badges": badges,
        "url": href,
    }


def extract(url: str):
    page = Fetcher.get(url, timeout=30)
    cards = page.css('a.main-thumb.vp-card.block[href*="/positions/"]')
    return [parse_card(card) for card in cards]


def write_csv(path: Path, rows):
    fieldnames = [
        "category",
        "location",
        "title",
        "hours_per_week",
        "duration",
        "accommodation",
        "meals",
        "skills",
        "rating",
        "badges",
        "url",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row = dict(row)
            row["skills"] = ", ".join(row["skills"])
            row["badges"] = ", ".join(row["badges"])
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Extract Worldpackers search cards with Scrapling")
    parser.add_argument("url", help="Worldpackers search/results URL")
    parser.add_argument("--json-out", help="Optional output path for JSON")
    parser.add_argument("--csv-out", help="Optional output path for CSV")
    args = parser.parse_args()

    rows = extract(args.url)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_out:
        write_csv(Path(args.csv_out), rows)

    print(json.dumps({"count": len(rows), "items": rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
