#!/usr/bin/env python3
"""Validate Telegram AI news formatting before sending."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ITEM_RE = re.compile(r"^\s*(?:#{1,3}\s*)?\d+\.\s+\S")
SEPARATOR_RE = re.compile(r"^\s*---\s*$")
ITEM_RE = re.compile(r"^\s*(?:#{1,3}\s*)?(\d+)\.\s+(\S.*)$")
LINK_RE = re.compile(r"^\s*(?:링크|원문)\s*:\s*(https?://\S+)")
def validate_geeknews_links(lines: list[str], errors: list[str]) -> None:
    for line_number, line in enumerate(lines, start=1):
        link_match = LINK_RE.match(line)
        if not link_match:
            continue
        url = link_match.group(1).rstrip(")],.")
        parsed = urlparse(url)
        if parsed.netloc.lower() not in {"news.hada.io", "www.news.hada.io"}:
            continue
        topic_id = parse_qs(parsed.query).get("id", [""])[0]
        if not topic_id.isdigit():
            errors.append(f"line {line_number}: GeekNews URL has no numeric topic id: {url}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_ai_news_format.py <news-file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL: file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    item_lines = [idx for idx, line in enumerate(lines) if ITEM_RE.match(line)]
    separator_lines = [idx for idx, line in enumerate(lines) if SEPARATOR_RE.match(line)]

    errors: list[str] = []
    item_count = len(item_lines)
    expected_min = max(item_count - 1, 0)

    if item_count < 2:
        errors.append(f"expected at least 2 news items, found {item_count}")

    if len(separator_lines) < expected_min:
        errors.append(
            f"expected at least {expected_min} standalone '---' separators "
            f"between {item_count} items, found {len(separator_lines)}"
        )

    for left, right in zip(item_lines, item_lines[1:]):
        has_between_separator = any(left < idx < right for idx in separator_lines)
        if not has_between_separator:
            errors.append(
                f"missing standalone '---' separator between item lines "
                f"{left + 1} and {right + 1}"
            )

    for idx in separator_lines:
        prev_blank = idx == 0 or lines[idx - 1].strip() == ""
        next_blank = idx == len(lines) - 1 or lines[idx + 1].strip() == ""
        if not (prev_blank and next_blank):
            errors.append(
                f"separator on line {idx + 1} must have blank lines before and after"
            )

    validate_geeknews_links(lines, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {item_count} items, {len(separator_lines)} standalone separators",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
