# Approval Gates

> L2 권한이 필요한 액션의 승인 대기 큐.
> Heartbeat Agent가 추가하고, 사용자가 Telegram으로 응답한다.

## 대기 중

### [wiki-03] GPG 서명 없이 agent-wiki 커밋 허용
- requested: 2026-04-19 13:00
- action: `git -c commit.gpgsign=false commit -m "improve mobile navigation: bigger toggle, overlay, auto-close sidebar"` 후 `git push origin main`
- reason: 서명 서버(/tmp/code-sign)가 외부 레포 커밋에 대해 "missing source" 오류 반환. index.html은 완성·스테이징 상태.
- impact: shdkej/agent-wiki main 브랜치에 index.html 1개 파일 변경

## 처리 완료

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
