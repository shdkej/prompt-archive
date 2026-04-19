# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

<!-- 비어 있음 -->

## Active

<!-- Heartbeat가 관리하는 구조화된 Intent -->

### wiki-02: agent-wiki GitHub Pages 구현
- id: wiki-02
- status: in_progress
- priority: medium
- permission: L2
- created: 2026-04-18T09:00
- unblocked: 2026-04-19T02:40 — 사용자 `/infinity 승인`으로 재진행 지시. 다음 Heartbeat에서 재시도
- prior_block: L2 승인 수신(13:13) 후 실행 시도했으나 환경 제약 — GitHub MCP가 prompt-archive 전용이며 로컬에 agent-wiki 클론 없음
- goal: shdkej/agent-wiki 레포에 Docsify 설정 추가 후 GitHub Pages 활성화
- success_criteria:
  - docs/index.html 생성 완료
  - shdkej/agent-wiki 레포에 커밋 & 푸시 완료
  - https://shdkej.github.io/agent-wiki/ 접속 가능
- context: infinity/drafts/agent-wiki-pages-design.md, infinity/drafts/wiki-02-implementation.md, github:shdkej/agent-wiki
- depends_on: wiki-01 (완료)
