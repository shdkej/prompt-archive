# Virtue Time-to-Value 관찰 기준표

> prelaunch 단계 관찰 전용. 성패 판정 금지.
> cloud draft — 최종본은 virtue-rebirth-app/docs/time-to-value-observation-brief.md (canonical)

## 0. 전제

- prelaunch 단계이므로 어떤 time gap도 "빠르다/느리다" 성패 판정 금지.
- 기존 이벤트(`add_flow_started`, `deed_judged`, `deed_saved`, `level_up_viewed`)만 사용. 신규 이벤트/속성/코드/대시보드 변경 0.
- 수기 관찰 또는 PostHog raw event 조회만 허용. PostHog 대시보드 신규 생성은 Waiting.
- 이 문서는 `activation-milestone-ladder.md`의 setup→aha→habit 프레임을 계승하고, `first-session-jtbd-matrix.md`의 J1~J4 정의를 재사용한다. 재정의 없음.

## 1. Time-to-Value 개념 정의

| 개념 | 정의 |
|---|---|
| First value | 해당 job에서 처음으로 의미 있는 출력을 경험하는 순간 (기존 이벤트 발화 기준) |
| Second value | 첫 경험 이후 같은 job 맥락에서 재방문·반복·심화를 확인하는 다음 이벤트 |
| Time gap | second value 이벤트 timestamp − first value 이벤트 timestamp (분 또는 일 단위) |

## 2. J1~J4 Time-to-Value 매트릭스

| Job | First value 이벤트 | First value 관찰 기준 | Second value 이벤트 | Second value 관찰 기준 | Time gap 단위 | Time gap 계산 방식 | 정성 확인 질문 | prelaunch 해석 금지선 |
|---|---|---|---|---|---|---|---|---|
| **J1 기록형** | `deed_saved` | 첫 덕행 저장 완료 | `deed_saved` (2번째) | 같은 세션 또는 다음 방문에서 두 번째 저장 | 분 (동일 세션) / 일 (재방문) | `deed_saved[1].ts − deed_saved[0].ts` | "두 번째 기록은 첫 번째와 맥락이 달랐나?" / "같은 덕목인가, 다른 덕목인가?" | 두 번째 기록 속도로 습관화 판정 금지 |
| **J2 누적형** | `deed_saved` | 첫 덕행 저장 (누적 카운터 1) | `level_up_viewed` | 첫 레벨업 — 누적의 첫 가시화 | 일 (레벨업까지) | `level_up_viewed.ts − deed_saved[0].ts` | "레벨업을 봤을 때 누적이 실감됐나?" / "레벨업이 의미 있는 피드백이었나?" | 레벨업 속도로 engagement 판정 금지 |
| **J3 AI 호기심형** | `deed_judged` | 첫 AI 판정 경험 (저장과 독립) | `deed_judged` (2번째) | AI 판정 재경험 — 호기심 반복 여부 | 분 (동일 세션) / 일 (재방문) | `deed_judged[1].ts − deed_judged[0].ts` | "AI 판정 결과에 동의했나, 반발했나?" / "두 번째 판정을 요청한 이유가 뭔가?" | 판정 횟수·속도로 AI 기능 성공 판정 금지 |
| **J4 회고형** | `deed_saved` | 첫 기록 (회고 소재 확보) | `deed_saved` (distinct day 2) | 다음 날 이상에서 재기록 — 시간 축 생성 | 일 (재방문 간격) | `deed_saved[distinct_day=2].ts − deed_saved[distinct_day=1].ts` | "어제 기록을 오늘 다시 봤나?" / "과거 기록이 오늘 행동에 영향을 줬나?" | 재방문 간격으로 retention 판정 금지 |

## 3. 기존 이벤트 TTV 역할 요약

| 이벤트 | 발화 조건 | TTV 역할 |
|---|---|---|
| `add_flow_started` | add flow 페이지 진입 | setup 입구 — TTV 카운트 시작 전 의도 포착 |
| `deed_saved` | 덕행 저장 완료 | J1/J2/J4 first value; J1/J4 second value |
| `deed_judged` | AI 판정 완료 (저장 전·독립 발화) | J3 first & second value |
| `level_up_viewed` | 레벨업 화면 노출 | J2 second value |

> `deed_save_capped` (캡 초과 early-return)은 저장 미집계 → TTV 계산에서 제외.

## 4. Time Gap 계산 방식

- **분 단위**: PostHog raw event `timestamp` 필드 직접 비교. 동일 세션(30분 기준) 내이면 분 단위 사용.
- **일 단위**: `distinct_id` 기준 calendar day(`YYYY-MM-DD`) 정렬 후 날짜 차이 계산.
- **prelaunch 수기 관찰**: 첫 10명은 PostHog raw 조회 + 직접 대화로 보완. 자동 집계 대시보드 신규 생성 불필요.

## 5. 정성 확인 질문 (공통)

| 질문 | 목적 |
|---|---|
| "첫 번째 경험 이후 다시 앱을 열게 된 이유가 뭔가?" | second value로 이어지는 동기 파악 |
| "첫 경험에서 기대와 달랐던 점은?" | first value 품질 신호 수집 |
| "다음에도 같은 방식으로 사용할 것 같나?" | second value 자발성 예측 |

## 6. Prelaunch 해석 금지선

- time gap이 짧다 ≠ 제품이 좋다. 성패 판정 금지.
- time gap이 길다 ≠ 이탈. 단정 금지.
- second value 미발생 = retention 실패 판정 금지 (n<10 표본).
- 40% 이상/이하 임계값 적용 금지.
- 이 기준표는 관찰 체계화 도구이며, 출시 전 성패 기준이 아님.

## 7. 선행 문서 충돌 점검

| 문서 | 관계 | 충돌 여부 |
|---|---|---|
| `activation-milestone-ladder.md` | setup→aha→habit 프레임 원천. TTV first/second value는 aha moment에 해당 | 충돌 없음. 계승 |
| `first-session-jtbd-matrix.md` | J1~J4 정의 원천. 활성화 이벤트(J1/J2/J4=deed_saved, J3=deed_judged, J2 보조=level_up_viewed) | 충돌 없음. 재사용 |
| `minimum-viable-audience-brief.md` | 첫 10명 관찰 맥락. 수기 관찰 우선 원칙 공유 | 충돌 없음 |
| `pmf-response-analysis-rubric.md` | 작은 표본 40% 판정 금지선 계승 | 충돌 없음 |

## Out of scope

- 신규 PostHog 이벤트/속성 구현 금지
- PostHog 대시보드 신규 생성 → Waiting
- 외부 인터뷰 공개 모집/DM/발송 → approval-needed
- 프로덕션 tracking 코드 변경 → approval-needed
- 비용 발생 작업 없음
