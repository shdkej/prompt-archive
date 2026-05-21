# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

<!-- marketing-08 candidate 2026-05-21T10:01Z
제목: Virtue PMF 응답 분석 루브릭 작성
소스 노트: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
근거: Superhuman/Sean Ellis 방식은 40% 숫자보다 "매우 아쉽다" 응답자의 persona·benefit·대체재 언어를 분리해 high-expectation customer를 찾는 데 핵심이 있다. Virtue에는 이미 PMF 질문 초안과 MVA 기준표가 있으나, 응답을 J1~J4·benefit·대체재·다음 카피 가설로 태깅하는 분석 루브릭은 없다.
예상 임팩트: 첫 10명 prelaunch 학습이 평균 만족도 판단으로 흐르지 않고, 강한 반응자의 언어를 다음 포지셔닝/온보딩 문서로 연결할 수 있다.
권한 수준: L1 내부 문서 작성. 외부 설문 발송, DM/메일, 공개 모집, PostHog 설정 변경은 Waiting/approval-needed.
Owner route: Marketer 주도, Planner 검수, Developer/Operator는 기존 이벤트(deed_saved, deed_judged) 참조만 확인. 코드/트래킹 변경 없음.
성공 기준: docs/pmf-response-analysis-rubric.md 1개 추가; PMF-1~4 응답 태깅 표, J1~J4 매핑 규칙, "매우 아쉽다" 그룹 우선 분석 규칙, 작은 표본 과대해석 금지선, 외부 발송 approval-needed 경계 포함.
첫 검증 게이트: docs/first-impression-positioning-snapshot.md의 PMF 질문과 docs/minimum-viable-audience-brief.md의 J1~J4/MVA 기준을 변경 없이 계승했는지 확인하고, copy-spec 금지어를 사용자 노출 카피로 새로 쓰지 않았는지 grep으로 점검.
Routing: Inbox
-->

## Active

### marketing-08 · Virtue PMF 응답 분석 루브릭 작성

- id: marketing-08
- status: in_progress
- priority: high
- permission: L1
- created: 2026-05-21T10:10Z
- detail: infinity/intents/active/marketing-08.md

**Goal**: PMF-1~4 응답을 J1~J4·benefit·대체재·다음 카피 가설로 태깅하는 분석 루브릭 작성
**Cloud draft**: 완료 → infinity/artifacts/marketing-08/pmf-response-analysis-rubric.md
**Next**: 로컬 Claude Code에서 source note 보완 후 docs/pmf-response-analysis-rubric.md 저장

## Waiting

<!-- 사용자 결정, 외부 조건, 안전 확인 대기. 같은 질문을 반복하지 않고 상태만 보존한다. -->

## Archive

<!-- marketing-07 completed 2026-05-20T22:07Z → infinity/intents/archive/marketing-07.md (Virtue 최소 생존 오디언스 기준표: J1~J4 잡을 그대로 계승해 첫 10명 후보 조건·첫 문장/약속·첫 세션 가치 순간·관찰 질문·승인 필요 외부 액션 경계 6칸으로 매핑, 컬럼별 Planner/Marketer/Developer/Operator 렌즈. Seth Godin 밀도>규모 + Paul Graham do-things-that-dont-scale 학습 루프, "문안까지 L1·발송부터 Waiting" 경계 명시. 활성화 이벤트 계승(J1/J2/J4=deed_saved, J3=deed_judged) 신규 0. copy-spec/first-session-jtbd-matrix 충돌 0건; docs/minimum-viable-audience-brief.md 추가) -->

<!-- marketing-06 completed 2026-05-20T10:07Z → infinity/intents/archive/marketing-06.md (Virtue 첫 세션 JTBD 매트릭스: J1 기록형/J2 누적형/J3 AI 호기심형/J4 회고형 4잡을 첫 화면 약속·첫 행동·성공 지표·마찰 위험·근거 문서 5칸으로 매핑, J3=deed_judged·나머지=deed_saved 활성화, good/bad 마찰 구분, 기존 6 이벤트 재사용·신규 0, 선행 3문서+copy-spec 충돌 0건; docs/first-session-jtbd-matrix.md sha 38af1be) -->

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
