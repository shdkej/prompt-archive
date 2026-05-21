# Approval Gates

> L2 권한이 필요한 액션의 승인 대기 큐.
> Heartbeat Agent가 추가하고, 사용자가 Telegram으로 응답한다.

## 대기 중

### [marketing-01] Virtue add-flow telemetry 머지/푸시 및 배포 승인
- requested: 2026-05-21 08:07 UTC
- action: `/home/ubuntu/dev/virtue-rebirth-app`의 로컬 브랜치 `marketing-01-add-flow-telemetry`(`b28d01f`)를 `master`에 머지 후 push하고, 승인 범위에 포함되면 Oracle 서버에서 `git pull + pnpm build + pm2 restart` 배포까지 진행
- reason: `add_flow_started` / `add_flow_abandoned` 텔레메트리를 배포해야 landing → add → judge → save 드롭오프 측정이 시작됨
- impact: GitHub 원격 repo 및 프로덕션 Virtue 배포에 영향 가능. Push의 자동 배포 여부와 Oracle 서버 배포는 로컬에서 안전하게 단정할 수 없어 명시 승인 필요
- prepared_report: infinity/reports/marketing-01/2026-05-21T0807Z-local-execution.md

## 처리 완료

### [wiki-04] shdkej/agent-wiki에 자동 사이드바 파일 추가 및 푸시 (JS)
- requested: 2026-04-24 09:00
- resolved: 2026-04-25 (사용자 `/infinity 승인`)
- decision: approved
- note: JS 버전으로 진행. 다음 Heartbeat에서 실행
- draft: infinity/artifacts/wiki-04/auto-navigation.md

### [build-01] agent-wiki GitHub Pages 구현 (Jekyll 방식) — 취소
- requested: 2026-04-21 00:00
- resolved: 2026-04-21 00:30
- decision: cancelled
- note: build-01 완료 시 wiki-02/03에서 이미 Docsify로 GitHub Pages 구현 완료 확인. Jekyll 전환 불필요. Intent completed 처리.

### [wiki-03] 로컬 환경에서 agent-wiki push 수행
- requested: 2026-04-20 11:00 (T11:00 에스컬레이션)
- resolved: 2026-04-20 13:30
- decision: approved
- note: 사용자 `/infinity 승인 후 여기서 진행` — 로컬 SSH 인증으로 index.html push 완료 (commit d52641c). Intent completed → archive 이관

### [wiki-02] 재진행 승인 (환경 제약 blocked 해제)
- requested: 2026-04-19 02:40
- resolved: 2026-04-19 02:40
- decision: approved
- note: 사용자 `/infinity 승인` — wiki-02 blocked 해제, in_progress 전환. 다음 Heartbeat에서 실행 재시도

### [doc-01] lessons-learned.md 변경사항 푸시
- requested: 2026-04-08 13:00
- resolved: 2026-04-08 13:05
- decision: approved
- note: 사용자 승인

### [monitor-01] monitoring_personal 변경사항 커밋 & 푸시
- requested: 2026-04-08 11:00
- resolved: 2026-04-08 11:15
- decision: approved
- note: 사용자 승인

### [wiki-02] shdkej/agent-wiki 레포에 Docsify 파일 추가 및 GitHub Pages 활성화
- requested: 2026-04-18 09:00
- resolved: 2026-04-18 13:13
- decision: approved
- note: Telegram에서 사용자 승인

### [wiki-03] shdkej/agent-wiki index.html 교체 및 푸시
- requested: 2026-04-19 04:00
- resolved: 2026-04-19 12:36
- decision: approved
- note: Telegram에서 사용자 승인

### [wiki-03] GPG 서명 없이 agent-wiki 커밋 허용
- requested: 2026-04-19 13:00
- resolved: 2026-04-19 23:29
- decision: approved
- note: Telegram에서 사용자 승인
