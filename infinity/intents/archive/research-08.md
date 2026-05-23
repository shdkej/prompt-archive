# research-08 Intent 원장

- id: research-08
- title: GEO/LLMO 적용 체크리스트 조사
- status: archived
- priority: medium
- permission: L0/L1
- mode: research
- created_at: 2026-05-23T00:07Z
- completed_at: 2026-05-23T10:30Z

## Goal

`llms.txt` 등 GEO/LLMO(SEO의 AI 검색/답변엔진 대응 버전)에서 실제로 설정해야 할 항목을 조사하고, Virtue/Knowledge Lab/Infinity에 적용 가능한 우선순위 체크리스트로 정리한다.

## Result Summary

llms.txt, robots.txt AI 크롤러 정책, sitemap/schema.org, canonical/metadata, LLM 답변 노출 최적화, 콘텐츠 구조, E-E-A-T 신뢰 신호, 주요 AI 엔진별 차이를 망라한 GEO/LLMO 조사 문서 작성 완료. Virtue/Knowledge Lab/Infinity 프로젝트별 우선순위 체크리스트(P0~P2)와 실행 후보 목록 포함. 공개 사이트 변경 0.

## Artifacts

- `infinity/artifacts/research-08/geo-llmo-checklist.md` — 전체 조사 문서 + 프로젝트별 체크리스트

## Key Findings

- `llms.txt`는 추론용 큐레이션 제안이며 robots/sitemap/schema/canonical/source quality를 대체하지 않는다.
- OpenAI는 `OAI-SearchBot`(ChatGPT 검색 노출)과 `GPTBot`(학습용)을 분리한다.
- Google `Google-Extended`는 Gemini 학습/grounding 전용이며 일반 Google 검색 랭킹에 영향 없다.
- Knowledge Lab은 `/llms.txt` 1순위 적용 대상.
- Virtue는 공개 explainer 페이지 vs 앱 화면 구분 먼저 정리 필요.
- Infinity는 private-default 권고 (내부 시스템).

## Reports

- `infinity/reports/research-08/2026-05-23T0007Z.md`
- `infinity/reports/research-08/2026-05-23T1000Z.md`

## Next Actions

- [ ] Knowledge Lab에 llms.txt 생성 (별도 Intent)
- [ ] Virtue robots.txt AI 크롤러 정책 명시 (별도 Intent)
- [ ] Virtue 랜딩페이지 schema.org JSON-LD 추가 (별도 Intent)
