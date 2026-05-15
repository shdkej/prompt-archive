# marketing-01 · Virtue 활성화 감사

- id: marketing-01
- status: in_progress
- priority: high
- permission: L0/L1 (research · prepare · fix plan 문서)
- project: virtue-rebirth-app
- repo: https://github.com/shdkej/virtue-rebirth-app
- deployment: https://virtue.oracle.shdkej.com
- created: 2026-05-15T13:32Z
- promoted_to_active: 2026-05-15T(heartbeat)

## Goal

Virtue 앱의 초기 활성화 갭(activation gap)을 좁히기 위한 경계 감사.
PostHog 신호 기반으로 demo-state 원인, add-flow 마찰, 텔레메트리 품질 세 가지를 분석하고
로컬 실행 가능한 수정 계획을 만든다.

## Success Criteria

- [ ] 프로덕션 HTML demo-state(641덕·MOCK_DEEDS) 원인 특정 + 수정 방법 확인
- [ ] 모바일 add-flow(landing → add → judge → save) 마찰점 목록 작성
- [ ] PostHog `$exception` 텔레메트리 개선 코드 초안 작성
- [ ] 위 세 가지를 반영한 로컬 실행 위임 프롬프트 완성
- [ ] 수정 후 7일간 `deed_saved / deed_judged` 비율 개선 기대치 설정

## Context

- PostHog project 424014 — 7일 31 pageviews / 3 users / 1 deed_judged / 0 deed_saved
- 배포 URL: https://virtue.oracle.shdkej.com (PM2 + Nginx, oracle 서버)
- 앱 repo: shdkej/virtue-rebirth-app (master, 최신 푸시 dfaaf4e)
- 운영 모드: NEXT_PUBLIC_SCORING_MODE=mock / ANTHROPIC_API_KEY 미설정
- store: localStorage 기반 / 첫 로드 시 MOCK_DEEDS 14건 시드 (guard는 dfaaf4e에 추가됨)
- 핵심 참조 파일:
  - infinity/artifacts/product-01/implementation.md
  - infinity/artifacts/product-01/ux-improvement-guide.md
  - infinity/artifacts/product-01/deployment-guide.md
  - infinity/reports/product-01/2026-05-15T11-07-post-push-verify.md

## Next Actions

1. (L0) demo-state 루트 콜즈 확인 + 수정 계획 초안 → `infinity/artifacts/marketing-01/demo-state-fix.md`
2. (L0) PostHog 텔레메트리 개선 코드 초안 → `infinity/artifacts/marketing-01/telemetry-fix.md`
3. (L0/L1) 로컬 실행 위임 프롬프트 작성 → `infinity/artifacts/marketing-01/local-execution-prompt.md`
4. (L2 agent-approved) Oracle 서버 배포 트리거 — dfaaf4e 반영 (자체 승인 조건 재확인 필요)
