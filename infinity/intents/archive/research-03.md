# research-03: 최근 GitHub 트렌드 크롤링/데이터 수집 툴 재조사 (OpenClaw 기준)

- id: research-03
- status: archived
- priority: medium
- permission: L0
- project: research
- created: 2026-04-11
- completed_at: 2026-04-11T10:00
- goal: 최근 GitHub에서 주목받는 크롤링/데이터 수집 툴을 OpenClaw와의 궁합 중심으로 심층 재조사. 고전 툴(Scrapy, Beautiful Soup) 제외, 신규 트렌드 툴 중심. 단순 스타 수 대신 실제 유지보수성, 동적 페이지 대응, anti-bot 대응, 운영 난이도 분석.
- success_criteria:
  - 최근 GitHub 트렌드 크롤링 툴 5개 이상 신규 발굴 (research-02 대비 추가) ✅ (7개 신규)
  - 유지보수성, 동적 페이지, anti-bot, 운영 난이도, OpenClaw 궁합 항목별 심층 비교 ✅
  - 상황별 추천 가이드 업데이트 ✅

## result

모든 성공 기준 충족. research-02 대비 7개 신규 도구 발굴 및 심층 분석 완료.

- 산출물: `infinity/reports/research-03/2026-04-11T10-00.md`
- 신규 발굴 도구: Scrapling, Camoufox, Nodriver, browser-use, Stagehand, ScrapeGraphAI, Spider.cloud
- 핵심 변화 3가지:
  1. Scrapling MCP 서버 → OpenClaw와 직접 anti-bot 통합 가능
  2. SeleniumBase UC Mode 유지보수 중단 → Nodriver가 후계자
  3. ScrapeGraphAI MCP 서버 → LLM 네이티브 스크래핑이 OpenClaw 에이전트와 통합
- 업데이트 OpenClaw 궁합 2위: Scrapling (이전 research-02: Firecrawl)

## lesson

- Scrapling의 MCP 서버 패턴이 중요: 스크래핑 도구가 MCP 서버를 제공하면 OpenClaw와의 통합이 코드 없이 가능해짐
- anti-bot 도구의 수명 주기가 짧아짐 (SeleniumBase UC Mode 약 1년 만에 중단) → 주기적 재조사 필요
- C++ 레벨 지문 조작(Camoufox)이 JavaScript 레이어 조작보다 탐지 우회 효과 월등
- Cloudflare 우회는 오픈소스만으로 한계 → Scrapling(무료)+관리형 서비스(유료) 계층화 전략이 현실적
