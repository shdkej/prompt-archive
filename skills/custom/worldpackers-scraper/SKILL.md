---
name: worldpackers-scraper
description: Parse Worldpackers search/result pages into structured opportunity data using Scrapling. Use when extracting volunteer/work-exchange listings from Worldpackers URLs, especially search pages like /search/.../skill_web_development, and when the agent should output concise summaries or save JSON/CSV from those listings.
---

# Worldpackers Scraper

**목차**

- [Workflow](#workflow)
- [EU Dev Monitor Cron](#eu-dev-monitor-cron)
- [Command](#command)
- [Output fields](#output-fields)
- [Notes](#notes)

Use the bundled script for deterministic extraction from Worldpackers result pages.

## Workflow

1. Ensure the Python venv exists at `/home/ubuntu/.openclaw/workspace-hj/.venv-scrapling`.
2. Run `scripts/extract_worldpackers.py` with the target URL.
3. Prefer JSON output for downstream automation.
4. If the user wants a human summary, summarize the JSON rather than reparsing the page.

## EU Dev Monitor Cron

The recurring Worldpackers EU development monitor must use the deterministic command script, not an agentTurn prompt:

```bash
cd /home/ubuntu/.openclaw/workspace-hj
. .venv-scrapling/bin/activate
python skills/worldpackers-scraper/scripts/monitor_worldpackers_eu_dev.py
```

Cron contract:

- Output only concise bullets for newly qualifying listings.
- Output exactly `NO_REPLY` when no new qualifying listings exist.
- Exit non-zero on search extraction failure or total detail-fetch failure; do not hide scraper/runtime failures behind `NO_REPLY`.
- Keep newly announced listings in `pendingNew`/`pendingAnnouncements`; only promote them to `seen` on a later run after the previous cron delivery is confirmed as delivered.
- Keep state in `memory/worldpackers-eu-dev-seen.json` and latest debug data in `memory/worldpackers-eu-dev-latest.json`.
- Delivery is intentionally handled by OpenClaw cron, not by the script.

## Command

```bash
. /home/ubuntu/.openclaw/workspace-hj/.venv-scrapling/bin/activate
python /home/ubuntu/workspace/prompt-archive/skills/custom/worldpackers-scraper/scripts/extract_worldpackers.py "https://www.worldpackers.com/search/europe/skill_web_development"
```

## Output fields

Each item includes:

- `category`
- `location`
- `title`
- `hours_per_week`
- `duration`
- `accommodation`
- `meals`
- `skills`
- `rating`
- `badges`
- `url`

## Notes

- This skill targets search/result cards, not full position detail pages.
- If Worldpackers changes card markup, update selector logic in the script.
- If simple fetch stops working for a specific page type, try swapping the script to a different Scrapling fetcher rather than rewriting the whole workflow.
