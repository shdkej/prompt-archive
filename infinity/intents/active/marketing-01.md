# marketing-01 · Virtue 활성화 감사

- id: marketing-01
- status: waiting
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

- [x] 프로덕션 HTML demo-state(641덕·MOCK_DEEDS) 원인 특정 + 수정 방법 확인 → artifacts/marketing-01/demo-state-fix.md
- [x] 모바일 add-flow(landing → add → judge → save) 마찰점 목록 작성 → telemetry-fix.md §3-3 참조 (live 페이지 접근 불가로 부분 완료)
- [x] PostHog `$exception` 텔레메트리 개선 코드 초안 작성 → artifacts/marketing-01/telemetry-fix.md
- [x] 위 세 가지를 반영한 로컬 실행 위임 프롬프트 완성 → artifacts/marketing-01/local-execution-prompt.md
- [x] 수정 후 7일간 `deed_saved / deed_judged` 비율 개선 기대치 설정 → artifacts/marketing-01/improvement-expectation.md

## Local Execution Status

- [x] 로컬 Claude Code 실행 완료 → `infinity/reports/marketing-01/2026-05-21T0807Z-local-execution.md`
  - demo-state 가드와 라이브 HTML 검증 완료: 641/MOCK 미노출, 빈 상태 렌더 확인
  - PostHog 텔레메트리 중 남은 공백(`add_flow_started` / `add_flow_abandoned`)만 로컬 브랜치 `marketing-01-add-flow-telemetry`에 적용
  - `pnpm typecheck`, `pnpm lint`, `pnpm build` 통과
- [ ] **승인 대기**: `GATES.md`의 `[marketing-01] Virtue add-flow telemetry 머지/푸시 및 배포 승인`
  - 로컬 브랜치 `marketing-01-add-flow-telemetry`(`b28d01f`) → master 머지/push
  - 필요 시 Oracle 서버 배포 (git pull + pnpm build + pm2 restart)

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

1. **[사용자 승인 필요]** `GATES.md`의 `[marketing-01]` 머지/푸시 및 배포 승인 여부 결정
2. 승인 시 로컬 브랜치 `marketing-01-add-flow-telemetry`를 master에 머지/push하고, 배포 범위까지 승인되면 Oracle 서버 배포
3. 배포 후 7일간 PostHog 지표 점검 (improvement-expectation.md 기준)
