# research-02: 크롤링 툴 조사 및 비교 분석

- id: research-02
- status: archived
- priority: medium
- permission: L0
- project: research
- created: 2026-04-11
- completed_at: 2026-04-11T00:00
- goal: 현대적 크롤링 툴들을 OpenClaw 환경 기준으로 조사, 비교, 추천
- success_criteria:
  - 브라우저 자동화, 정적/동적 페이지 수집, anti-bot 대응, 유지보수성, 운영 난이도, OpenClaw 궁합 기준 비교표 작성 ✅
  - 상황별 툴 추천 정리 완료 ✅

## result

모든 성공 기준 충족. 비교표 및 상황별 추천 정리 완료.

- 산출물: `infinity/reports/research-02/2026-04-11T0000.md`
- OpenClaw 궁합 랭킹: 1위 Playwright, 2위 Firecrawl, 3위 Crawlee, 4위 Scrapy, 5위 Puppeteer
- 상황별 추천:
  - 일반 동적 페이지: Playwright (OpenClaw 내부 엔진)
  - LLM 파이프라인: Firecrawl (공식 OpenClaw 연동 지원)
  - anti-bot 강한 사이트: Crawlee + Residential 프록시
  - 대규모 정적 수집: Scrapy + scrapy-playwright

## lesson

- OpenClaw는 Playwright를 내부 CDP 엔진으로 사용하므로, Playwright를 기본 스택으로 삼는 것이 최적
- LLM 파이프라인에는 Firecrawl 공식 연동(docs.firecrawl.dev/developer-guides/openclaw) 활용
- anti-bot 대응은 오픈소스 stealth < Crawlee < 관리형 서비스 순으로 강도가 높아짐
- Cloudflare 강보호 사이트는 Residential 프록시 없이는 오픈소스 도구가 한계
