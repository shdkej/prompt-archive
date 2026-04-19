# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

## Active

<!-- Heartbeat가 관리하는 구조화된 Intent -->

<!-- wiki-02 completed 2026-04-19T02:45 → infinity/intents/archive/wiki-02.md -->

### wiki-03: agent-wiki 모바일 네비게이션 개선

- status: blocked
- priority: medium
- permission: L1 (드래프트 준비) + L2 (agent-wiki push)
- created: 2026-04-19T04:00
- project: agent-wiki
- goal: GitHub Pages(Docsify) 모바일 화면에서 사이드바 탐색 구조를 명확히 드러내기
- context: shdkej/agent-wiki (index.html), wiki-02 흐름과 충돌 없이 진행
- success_criteria:
  - 모바일(≤768px)에서 사이드바 토글 버튼이 명확히 보임
  - 사이드바 열릴 때 배경 오버레이 표시
  - 링크 클릭 시 사이드바 자동 닫힘
  - 기존 loadSidebar / search / auto2top 설정 유지
