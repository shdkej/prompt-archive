# marketing-01 · Virtue 활성화 감사

- id: marketing-01
- status: completed
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

- [x] PostHog 텔레메트리 코드 적용 + push
  - commit: `a10ff0e` (`Improve PostHog activation telemetry`)
  - report: `infinity/reports/marketing-01/2026-05-15T19-07-local-claude.md`
- [x] 사용자 Telegram 승인 수신 후 로컬 Claude Code 실행
  - approved_at: 2026-05-16T06:02Z
  - commit: `148b1cc` (`deed_judged 이벤트를 채점 완료 시점으로 통일`)
  - deployment: Kubernetes rollout completed, `virtue-rebirth-6bff5598d-5w6d4` ready
  - verification: `https://virtue.oracle.shdkej.com` ETag `"w3v1o6fzvocvu"`, `641`/`MOCK` marker 미노출
  - report: `infinity/reports/marketing-01/2026-05-16T06-14-local-execution.md`
- [x] 사용자 Telegram 승인 수신 후 add-flow telemetry 머지/푸시/배포
  - approved_at: 2026-05-21T09:49Z
  - commit: `b28d01f` (`add-flow 퍼널 텔레메트리 추가 (marketing-01)`)
  - deployment: Kubernetes rollout completed, `virtue-rebirth-6b6656cd8b-6w6gn` ready
  - verification: GitHub `master`와 배포 pod `/app` HEAD 모두 `b28d01f719db344f4e76c5c7d32934617a2d0f28`; `https://virtue.oracle.shdkej.com` HTTP 200, ETag `"60azsylmbqcvu"`, `641`/`MOCK` marker 미노출
  - report: `infinity/reports/marketing-01/2026-05-21T0950Z-approved-deploy.md`

## Context

- PostHog project 424014 — 7일 31 pageviews / 3 users / 1 deed_judged / 0 deed_saved
- 배포 URL: https://virtue.oracle.shdkej.com (Kubernetes deployment `virtue-rebirth`)
- 앱 repo: shdkej/virtue-rebirth-app (master, 최신 푸시 b28d01f)
- 운영 모드: NEXT_PUBLIC_SCORING_MODE=mock / ANTHROPIC_API_KEY 미설정
- store: localStorage 기반 / 첫 로드 시 MOCK_DEEDS 14건 시드 (guard는 dfaaf4e에 추가됨)
- 핵심 참조 파일:
  - infinity/artifacts/product-01/implementation.md
  - infinity/artifacts/product-01/ux-improvement-guide.md
  - infinity/artifacts/product-01/deployment-guide.md
  - infinity/reports/product-01/2026-05-15T11-07-post-push-verify.md

## Final Result

- 완료: demo-state guard 배포, PostHog 이벤트 정리, add-flow started/abandoned 텔레메트리 배포, 신규 배포 검증.
- 후속: 7일 후 PostHog 지표를 `improvement-expectation.md` 기준으로 점검.
