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

- [x] 프로덕션 HTML demo-state(641덕·MOCK_DEEDS) 원인 특정 + 수정 방법 확인 → artifacts/marketing-01/demo-state-fix.md
- [x] 모바일 add-flow(landing → add → judge → save) 마찰점 목록 작성 → telemetry-fix.md §3-3 참조 (live 페이지 접근 불가로 부분 완료)
- [x] PostHog `$exception` 텔레메트리 개선 코드 초안 작성 → artifacts/marketing-01/telemetry-fix.md
- [x] 위 세 가지를 반영한 로컬 실행 위임 프롬프트 완성 → artifacts/marketing-01/local-execution-prompt.md
- [x] 수정 후 7일간 `deed_saved / deed_judged` 비율 개선 기대치 설정 → artifacts/marketing-01/improvement-expectation.md

## Local Execution Status

- [ ] **대기 중**: 사용자가 `local-execution-prompt.md`를 로컬 Claude Code에 실행
  - Oracle 서버 배포 (git pull + pnpm build + pm2 restart)
  - PostHog 텔레메트리 코드 적용 + push
  - 배포 검증 (ETag 확인 + 신규 방문자 시뮬레이션)

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

1. **[사용자 액션 필요]** `infinity/artifacts/marketing-01/local-execution-prompt.md` 내용을 로컬 Claude Code에 실행
   - Oracle 서버 배포 + PostHog 텔레메트리 적용
2. (L0) 로컬 실행 완료 후 결과 리포트 수신 → status 재평가
3. 7일 후 PostHog 지표 점검 (improvement-expectation.md 기준)
