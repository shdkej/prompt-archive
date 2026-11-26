---
name: trustedhousesitters-scraper
description: Parse TrustedHousesitters assignment listing pages into structured sitting opportunities using Scrapling. Use when extracting pet/house-sitting listings from TrustedHousesitters country or global listing URLs, filtering by country or keywords, or saving structured JSON/CSV for later review.
---

# TrustedHousesitters Scraper

Use the bundled script to extract assignment cards from TrustedHousesitters listing pages.

## Workflow

1. Ensure the Scrapling venv exists at `/home/ubuntu/.openclaw/workspace-hj/.venv-scrapling`.
2. Run the bundled script with either a direct listing URL or a country slug.
3. Optionally filter results by keyword.
4. Prefer JSON output for automation and CSV for spreadsheet review.

## Commands

Global listings:

```bash
. /home/ubuntu/.openclaw/workspace-hj/.venv-scrapling/bin/activate
python /home/ubuntu/workspace/prompt-archive/skills/custom/trustedhousesitters-scraper/scripts/extract_trustedhousesitters.py \
  --country united-kingdom
```

Direct URL:

```bash
python /home/ubuntu/workspace/prompt-archive/skills/custom/trustedhousesitters-scraper/scripts/extract_trustedhousesitters.py \
  --url "https://www.trustedhousesitters.com/house-and-pet-sitting-assignments/united-kingdom/"
```

Keyword filter + file output:

```bash
python /home/ubuntu/workspace/prompt-archive/skills/custom/trustedhousesitters-scraper/scripts/extract_trustedhousesitters.py \
  --country united-kingdom \
  --keyword london \
  --keyword dog \
  --json-out /home/ubuntu/.openclaw/workspace-hj/ths-uk.json \
  --csv-out /home/ubuntu/.openclaw/workspace-hj/ths-uk.csv
```

## Parameters

- `--country <slug>`: country listing slug like `united-kingdom`, `spain`, `portugal`
- `--url <listing-url>`: use a direct TrustedHousesitters listing page instead of a country slug
- `--pages <n>`: fetch multiple listing pages using the site's encoded pagination links when available
- `--keyword <text>`: repeatable keyword filter against title/location/date/pet text
- `--json-out <path>`: save JSON
- `--csv-out <path>`: save CSV

## Output fields

Each item includes:

- `title`
- `location`
- `date_range`
- `status`
- `pet_summary`
- `tags`
- `url`

## Notes

- This skill targets assignment listing pages, not full sit detail pages.
- Country/feature changes should usually be done by changing CLI args, not editing the script.
- If the site changes pagination or card markup, update the selectors and text parsing heuristics in the script.
