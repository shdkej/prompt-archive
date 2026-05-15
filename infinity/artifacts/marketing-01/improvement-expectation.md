# marketing-01 · 수정 후 7일 개선 기대치

> created: 2026-05-15 (heartbeat L0 prepare)
> 기반: PostHog 7일 베이스라인 + demo-state-fix + telemetry-fix 적용 가정

---

## 1. 현재 베이스라인 (수정 전, 7일)

| 지표 | 수치 |
|------|------|
| pageviews | 31 |
| unique users | 3 |
| deed_judged | 1 |
| deed_saved | 0 |
| deed_saved / deed_judged 비율 | 0% |
| $exception (message null) | 4건 |

---

## 2. 수정 내용 요약

| 수정 | 기대 효과 |
|------|-----------|
| demo-state 제거 (MOCK_DEEDS → 빈 시작) | 신규 방문자가 앱을 "내 것"으로 인식 ↑ |
| error.tsx + captureException | $exception 디버그 가능 상태 전환 |
| deed_judged/deed_saved 프로퍼티 확장 | 이탈 단계 추적 가능 |
| add_flow_started/abandoned 이벤트 추가 | 퍼널 진입률 측정 가능 |

---

## 3. 7일 기대치 설정

### 보수적 시나리오 (같은 트래픽 유지)

- 방문자 3명 중 add 페이지 도달: 2명 (현재 추정 1명 이하)
- deed_judged: 2건 (현재 1건 → +100%)
- deed_saved: 1건 → **deed_saved / deed_judged ≥ 50%**
- 근거: demo-state 제거로 "내 행동을 기록할 공간"이라는 인식이 생기면
  판단(judged)까지 도달한 사람의 절반 이상은 저장까지 완료할 것으로 추정

### 낙관 시나리오 (데모가 주요 이탈 원인인 경우)

- deed_saved / deed_judged ≥ 80%
- add_flow_abandoned 이벤트 0건 (데모 데이터에 혼란이 없어짐)

### 최소 목표 (실패 기준)

- deed_saved ≥ 1건 (현재 0 → 최소 한 명은 전체 플로우 완료)
- $exception의 message/type이 null이 아닌 실제 값으로 노출

---

## 4. 측정 계획

### 7일 후 점검 항목 (PostHog project 424014)

| 항목 | 목표 | 실패 시 액션 |
|------|------|------------|
| deed_saved / deed_judged | ≥ 30% | add_flow_abandoned 분석 → UX 개선 |
| add_flow_started 이벤트 존재 | ≥ 1건 | 진입 경로 부재 → CTA 개선 |
| $exception.message != null | 100% | SDK 설정 재확인 |
| ETag 변경 확인 | 배포 후 즉시 | 배포 재시도 |

### 신규 가설 (7일 후 검증)

- H1: demo-state가 제거되면 deed_judged 이벤트가 2배 이상 증가한다
- H2: $exception이 디버그 가능해지면 숨겨진 에러 패턴이 발견된다
- H3: add_flow_abandoned 비율이 50% 이하이면 UX는 수용 가능 수준이다

---

## 5. 다음 Intent 연결

7일 후 데이터 기반으로 다음 Intent를 생성:
- `marketing-02`: 활성화 갭 분석 2차 — add_flow_abandoned 비율이 높으면 UX 개선
- `marketing-03`: AI 채점 모드 전환 — deed_saved가 목표 달성 시 ANTHROPIC_API_KEY 설정 검토
