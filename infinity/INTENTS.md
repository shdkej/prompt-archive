# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

## Active

### marketing-06 — Virtue 첫 세션 JTBD 매트릭스 작성

- id: marketing-06
- status: in_progress
- priority: medium
- permission: L1 internal docs only
- created_at: 2026-05-20T10:00Z
- mode: draft (cloud) → execute_local (verification)
- route: Infinity router → local Claude Code (workflow-master 분류 필요)
- goal: 현재 Virtue 첫 화면·빈 상태·첫 7일 루프 문서가 어떤 JTBD Job을 약속하는지 한 장으로 연결해, 카피/인터뷰/측정 후보의 기준점을 만든다.
- success_criteria:
  1. job 후보 3-4개를 표로 정의
  2. 각 job별 첫 화면 약속/첫 행동/성공 지표/마찰 위험/현재 근거 문서 5칸 매핑
  3. first-impression-positioning-snapshot.md, empty-state-first-action-audit.md, seven-day-deed-loop.md와 충돌 0건
  4. 외부 발송·트래킹 변경·코드 변경 0건 명시
- context:
  - source: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-20-jtbd-onboarding-segmentation.md
  - cloud_artifact: infinity/artifacts/marketing-06/jtbd-first-session-matrix.md
  - local_target: /home/ubuntu/dev/virtue-rebirth-app/docs/jtbd-first-session-matrix.md
  - ref: infinity/artifacts/marketing-04/first-impression-positioning-snapshot.md
  - ref: /home/ubuntu/dev/virtue-rebirth-app/docs/empty-state-first-action-audit.md
  - ref: /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- verification_gate: virtue-rebirth-app에서 docs/와 src/app/page.tsx, src/app/add/page.tsx를 읽은 후 rg로 job 후보명·deed_saved·deed_judged·Out of scope 존재를 확인
- next_action: 로컬 Claude Code가 virtue-rebirth-app 파일 검토 후 canonical 문서 작성 및 커밋

## Waiting

<!-- 사용자 결정, 외부 조건, 안전 확인 대기. 같은 질문을 반복하지 않고 상태만 보존한다. -->

## Archive

<!-- marketing-05 completed 2026-05-19T22:07Z → infinity/intents/archive/marketing-05.md (Virtue 빈 상태/첫 행동 감사표: ES-1~ES-6 다섯 칸 표, 대시보드 최근 덕행 카드 내부 CTA 후보 A/B + 라벨 3종, 톤 위험 T1–T5, 계측 후보 3종 정의, copy-spec 금지선 충돌 0건) -->

<!-- marketing-04 completed 2026-05-19T10:07Z → infinity/intents/archive/marketing-04.md (Virtue 첫인상 포지셔닝 스냅샷: 3가설 A/B/C, 첫인상 리스크 R1–R4, PMF 질문 4개, 헤드라인 후보 3개, copy-spec 금지선 충돌 0건) -->

<!-- marketing-03 completed 2026-05-18T22:20Z → infinity/intents/archive/marketing-03.md (Virtue 첫 7일 deed_saved 루프 정의서 작성, D1/D3/D7 카피·유연성 원칙·PostHog 후보 정리) -->

<!-- marketing-02 completed 2026-05-16T14:00Z → infinity/intents/archive/marketing-02.md (마찰점 4개 특정, 개선 후보 3개 초안, 로컬 실행 프롬프트 작성) -->

<!-- marketing-01 completed 2026-05-16T06:14Z → infinity/intents/archive/marketing-01.md (Virtue 배포/검증 완료, 641/MOCK 미노출 확인) -->

<!-- research-07 completed 2026-05-13T12:00 → infinity/intents/archive/research-07.md -->

<!-- product-01 completed 2026-05-15T11:44Z → infinity/intents/archive/product-01.md (Virtue 최신 상태, 후속 개선은 별도 Intent로 분리) -->

<!-- build-02 completed 2026-05-13 → infinity/intents/archive/build-02.md (https://infinity.oracle.shdkej.com 배포 완료) -->

<!-- research-06 completed 2026-05-05T08:00 → infinity/intents/archive/research-06.md -->

<!-- wiki-05 completed 2026-04-25T09:00 → infinity/intents/archive/wiki-05.md -->

<!-- wiki-04 completed 2026-04-25T10:15 → infinity/intents/archive/wiki-04.md -->

<!-- wiki-02 completed 2026-04-19T02:45 → infinity/intents/archive/wiki-02.md -->
<!-- wiki-03 completed 2026-04-20T13:30 → infinity/intents/archive/wiki-03.md -->
<!-- research-05 completed 2026-04-21T00:00 → infinity/intents/archive/research-05.md -->
<!-- wiki-01 completed 2026-04-21T00:00 → infinity/intents/archive/wiki-01.md -->
<!-- build-01 completed 2026-04-21T00:30 → infinity/intents/archive/build-01.md -->
<!-- research-05 re-run completed 2026-04-23T10:00 → infinity/intents/archive/research-05.md (3차) -->
