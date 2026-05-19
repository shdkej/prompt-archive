# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

### marketing-05: Virtue 빈 상태/첫 행동 감사표 작성
- Source: `/home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-19-empty-state-activation.md`
- Rationale: NN/g와 Smashing Magazine은 빈 상태를 초기 온보딩과 핵심 행동 경로의 중요한 접점으로 본다. Virtue는 prelaunch라 지표 판단보다 첫 사용자의 `기록 없음 -> 덕 쌓기` 경로가 명확한지 문서로 점검하는 편이 맞다.
- Expected impact: 첫 방문자가 빈 화면에서 길을 잃지 않고 `add 진입 -> deed_judged -> deed_saved` 활성화 흐름으로 이동할 가능성을 높인다.
- Permission level: L1 내부 문서/카피 감사. 코드 변경, 공개 발송, 생산 트래킹 변경 없음.
- Owner route: Infinity router -> Claude Code 문서 작업 후보. Required workflow: Use workflow-master first.
- Success criteria: `/home/ubuntu/dev/virtue-rebirth-app/docs/empty-state-first-action-audit.md`에 대시보드/덕행록/add 전후 빈 상태별 `상태 설명`, `기대 결과`, `첫 행동 CTA`, `톤 위험`, `계측 후보`가 정리된다. 카피 후보는 기존 `docs/copy-spec.md`의 설교/도덕적 칭찬 금지 원칙을 위반하지 않는다.
- First verification gate: 문서 생성 후 `rg -n "설교|칭찬|empty_state_seen|덕 쌓기|최근 덕행|덕행록" docs/empty-state-first-action-audit.md docs/copy-spec.md src/app src/components`로 근거와 금지선 충돌을 확인한다.

## Active

## Waiting

<!-- 사용자 결정, 외부 조건, 안전 확인 대기. 같은 질문을 반복하지 않고 상태만 보존한다. -->

## Archive

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
