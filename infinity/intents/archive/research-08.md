# research-08 Intent Ledger

- id: research-08
- title: GEO/LLMO 적용 체크리스트 조사
- status: archived
- priority: medium
- permission: L0/L1
- mode: research
- created_at: 2026-05-23T00:07Z
- completed_at: 2026-05-23T00:07Z

## Goal

`llms.txt` 등 GEO/LLMO(SEO의 AI 검색/답변엔진 대응 버전)에서 실제로 설정해야 할 항목을 조사하고, Virtue/Knowledge Lab/Infinity에 적용 가능한 우선순위 체크리스트로 정리한다.

## Result

Internal research artifact created:

- `infinity/artifacts/research-08/geo-llmo-checklist.md`

The artifact covers:

- `llms.txt`
- `robots.txt` and AI crawler policy
- sitemap and schema.org/structured data
- canonical and metadata
- LLM answer visibility
- content structure
- source/author trust signals
- major AI search/answer engine differences
- project-specific priorities for Virtue, Knowledge Lab, and Infinity

## Key Findings

- `llms.txt` is useful as a curated inference-time reading map, especially for documentation-style sites, but remains voluntary and does not replace robots, sitemaps, canonical metadata, structured data, or source quality.
- OpenAI separates `OAI-SearchBot` for ChatGPT search visibility from `GPTBot` for training.
- Google `Google-Extended` is a robots token for Gemini training/grounding use and does not affect normal Google Search inclusion or ranking.
- Knowledge Lab is the strongest first implementation target for `/llms.txt`.
- Virtue should first clarify public crawlable explainer pages versus user-state app screens.
- Infinity should stay private-by-default unless a deliberately public information surface is created.

## Reports

- `infinity/reports/research-08/2026-05-23T0007Z.md`
