# marketing-03 · Virtue 첫 7일 덕행 루프 정의서

> created: 2026-05-18T22:00Z (Heartbeat L1 draft)
> 근거: Inbox 의도 + marketing-02 퍼널 분석 + product-01 UX 가이드 + Duolingo/BJ Fogg/Calm 사례
> 대상: prelaunch 단계의 Virtue 앱, deed_saved 기반 리텐션 설계

---

## 0. 사전 확인 (First Verification Gate)

> ⚠️ **로컬 실행 전 확인 필요**: virtue-rebirth-app의 README, copy-spec, PostHog 초기화 코드를 읽고
> 아래 이벤트명과 카피 톤이 기존 코드와 충돌하지 않는지 검증한다.

현재 확인된 기존 이벤트명 (marketing-02 기반):
- `deed_judged` · `deed_saved` · `add_flow_started` · `add_flow_abandoned` · `deed_judge_attempted`

현재 확인된 카피 톤 (product-01 기반):
- 격식: "N일 연속이에요." / "이번 달 N덕" / "N일 동안 덕을 쌓았어요"
- 캐주얼: "N일 연속 굿." / "벌써 N일!" / "오늘의 첫 덕!"
- 앱 용어: 덕행, 덕, 덕을 쌓다, 덕행록, 환생, 종(species)

---

## 1. Streak 행동 정의 (deed_saved 중심)

### 핵심 정의

> **Streak = deed_saved가 발생한 날짜의 연속 일수**

| 규칙 | 내용 | 근거 |
|------|------|------|
| 카운팅 단위 | 1일 1회 이상 deed_saved → streak +1 | Duolingo: 하루에 여러 수업을 해도 streak는 1씩 증가 |
| 하루 경계 | 로컬 타임존 자정~자정 | product-01 computeStreak() 방식과 일치 |
| 최소 조건 | deed_saved ≥ 1건/일 (점수·내용 무관) | BJ Fogg: 가장 작은 행동으로 습관 진입 |
| 복수 기록 | 하루에 여러 번 기록해도 streak는 +1만 증가 | 과도한 게이미피케이션 방지 |
| 결측일 | deed_saved가 없는 날은 streak를 끊음 | 연속성 의미 보존 |

### computeStreak() 호환성

product-01 UX 가이드에 설계된 `computeStreak()` 함수는 이 정의와 완전히 호환된다.
- 중복 날짜 제거 후 역순 정렬 → 연속성 체크
- 하루라도 gap이 있으면 중단

**deed_saved가 선택된 이유**: deed_judged(채점)는 완료, deed_saved는 사용자의 의지 확인. "기록한다"는 행동이 덕행 습관의 핵심이며, 현재 deed_judged→deed_saved 전환율 0%(marketing-02)를 개선하는 지표이기도 하다.

---

## 2. 첫 1/3/7일 마일스톤 카피 후보

### 마일스톤 발화 시점

| 마일스톤 | 발화 조건 | 표시 위치 (후보) |
|---------|-----------|----------------|
| Day 1 | 최초 deed_saved (lifetime 첫 번째) | 저장 완료 직후 토스트 |
| Day 3 | streak = 3 달성 직후 | 대시보드 귀환 시 배너 또는 토스트 |
| Day 7 | streak = 7 달성 직후 | LevelUpSheet 병행 또는 전용 카드 |

### Day 1 — 첫 번째 덕행 저장

> 목적: "잘 했다"는 확인, 다음 방문 이유 심기 (부담 없이)

| 번호 | 톤 | 카피 |
|------|-----|------|
| A | 격식 | "첫 번째 덕행을 기록했어요. 좋은 시작이에요." |
| B | 캐주얼 | "첫 덕! 오늘 좋은 일 하나를 남겼군요." |
| C | 격려 | "시작이 반이에요. 내일도 하나만 더해봐요." |

**주의**: Day 1에는 "연속"·"streak" 언급 금지. 압박감 없이 행동 자체를 긍정한다 (Calm 원칙).

### Day 3 — 3일 연속

> 목적: 습관 형성의 임계점 도달 인식, "해볼 만하다" 감각 강화

| 번호 | 톤 | 카피 |
|------|-----|------|
| A | 격식 | "3일 연속 덕을 쌓고 있어요. 습관이 시작되는 순간이에요." |
| B | 캐주얼 | "벌써 3일! 이 정도면 습관 아닐까요?" |
| C | 격려 | "3일 연속이에요. 작지만 꾸준한 게 제일 어렵잖아요." |

**주의**: "3일 연속이면 21일까지 해야 한다"는 식의 압박 언급 금지. 현재를 칭찬하되 미래를 강요하지 않는다.

### Day 7 — 7일 연속

> 목적: "나는 덕을 쌓는 사람"이라는 정체성 강화 (BJ Fogg: 정체성→행동)

| 번호 | 톤 | 카피 |
|------|-----|------|
| A | 격식 | "7일 연속 덕을 쌓았어요. 한 주를 덕으로 채웠네요." |
| B | 캐주얼 | "7일 스트릭! 이 주는 완전 덕 주간이었네요." |
| C | 격려 | "일주일 연속이에요. 작은 선행이 쌓여 당신이 되어가고 있어요." |

**권장**: Day 7에는 LevelUpSheet(환생 달성 여부 무관)에 별도 섹션으로 표시 가능. 덕수가 기준에 미달하더라도 streak 축하를 표시한다.

---

## 3. 유연성/실패 처리 원칙

### 원칙 1 — "내일이 있다" (No-Shame Forgiveness)

> 실패는 종료가 아니라 재시작의 시작점이다.

**적용 규칙:**
- streak가 끊겨도 "이전 최고 기록(best_streak)"은 삭제하지 않는다.
- 끊김 직후 앱 진입 시 벌칙 UI (빨간 경고, 슬픈 이모지 등) 사용 금지.
- 대신: 중립~긍정 재시작 카피를 표시한다.

**재시작 카피 후보:**
| 조건 | 카피 |
|------|------|
| 1일 쉬고 복귀 | "어제는 쉬었군요. 오늘 다시 시작해요." |
| 3일 이상 쉬고 복귀 | "잠깐 멀어졌지만 다시 왔네요." |
| 오랜 공백 후 복귀 | "오랜만이에요. 오늘부터 다시 세어볼게요." |

**이유**: Duolingo의 streak 실패 알림은 효과적이지만 스트레스를 유발한다는 비판이 있다. Virtue는 prelaunch 단계로 MAU가 적고, 이탈 방지보다 "부담 없는 앱"이라는 인식 형성이 더 중요하다.

### 원칙 2 — "하나면 충분" (Minimum Viable Deed)

> BJ Fogg의 "Tiny Habit": 행동의 장벽을 최소화해야 루틴이 된다.

**적용 규칙:**
- deed_saved 1건 = streak 유지 (내용·점수·사진 첨부 여부 무관).
- "오늘은 뭘 써야 하지?"라는 불안을 없애기 위해 "아무 선행이나 괜찮아요" 힌트 플레이스홀더 유지.
- 하루 1건을 달성하면 "충분해요" 확인 카피 표시 (두 번째 기록 강요 금지).

**Day 1 이후 재방문 프롬프트 (앱 내 카피):**

```
어제 기록한 덕이 있어요.
오늘도 하나만 남겨볼까요?
```

**이유**: Ability(능력)가 낮으면 행동이 줄어든다(B=MAP). 기록 부담을 최소화하면 Motivation이 낮은 날에도 행동이 발생한다.

---

## 4. PostHog 이벤트 후보 및 Verification Gate

### 신규 추가 후보 이벤트

| 이벤트명 | 발생 시점 | 주요 프로퍼티 |
|---------|-----------|-------------|
| `streak_milestone_achieved` | streak가 1, 3, 7, 14, 30에 도달하는 순간 deed_saved 직후 | `streak: number`, `milestone: 1\|3\|7\|14\|30` |
| `streak_broken` | 이전에 streak ≥ 2인 상태에서 1일 이상 gap이 생기고 다시 deed_saved가 발생할 때 | `previous_streak: number`, `gap_days: number` |
| `retention_day` | 앱 첫 사용일 기준 D+1, D+3, D+7에 deed_saved가 발생할 때 | `day_since_first_deed: number` |

> **주의**: `streak_broken`은 deed_saved 시점에만 발생시킨다. "streak가 끊겼다"는 부정적 이벤트를 실시간으로 발생시키면 앱 여는 것 자체가 죄책감을 주는 트리거가 될 수 있다.

### 기존 이벤트 활용 (신규 추가 불필요)

| 지표 | 쿼리 방법 |
|------|----------|
| 첫 7일 리텐션 | `deed_saved`를 가진 유저의 D+1, D+3, D+7 재방문률 |
| Streak 분포 | `streak_milestone_achieved`의 milestone별 카운트 |
| 실패율 | `streak_broken`의 `previous_streak` 중앙값 |

### Verification Gate (로컬 실행 시)

```
체크리스트:
[ ] virtue-rebirth-app/src/ 에서 기존 posthog.capture() 호출 목록 추출
[ ] 위 3개 이벤트명이 기존 이벤트명과 중복되지 않는지 확인
[ ] copy-spec 또는 i18n 파일에서 기존 카피 톤 확인 (격식/캐주얼 구분)
[ ] computeStreak()가 이미 구현됐는지 확인 (product-01에서 설계됨)
[ ] streak_milestone_achieved 트리거 위치: deed_saved 직후 (add/page.tsx 저장 핸들러)
```

---

## 5. 로컬 실행 프롬프트

```markdown
Infinity Intent: marketing-03 · 첫 7일 덕행 루프 구현
Mode: execute_local
Required workflow: workflow-master 먼저 실행. 복잡도 판단 후 진행.
Goal:
  1. streak_milestone_achieved / streak_broken / retention_day 이벤트 추가 (add/page.tsx)
  2. Day 1/3/7 마일스톤 카피를 토스트 또는 배너로 표시 (computeStreak() 기반)
  3. 재시작 카피 표시 (앱 진입 시 streak === 0이고 이전 best_streak ≥ 2인 경우)
Context:
  - 레포: /home/ubuntu/dev/virtue-rebirth-app
  - 정의서: infinity/artifacts/marketing-03/first-7-day-virtue-loop.md (이 파일)
  - 참고: infinity/artifacts/product-01/ux-improvement-guide.md §1 (computeStreak, streak 표시)
  - 참고: infinity/artifacts/marketing-02/activation-friction-audit.md §3 (이벤트 패턴)
Prepared findings:
  - streak = deed_saved 날짜 연속 일수 (computeStreak() 호환)
  - 마일스톤 카피는 격식/캐주얼 쌍으로 구현, tone 상태 변수로 분기
  - Verification Gate: posthog 이벤트명 중복 확인 필수
Allowed: L0/L1 only (파일 수정, 테스트, 커밋, push)
Forbidden: 배포 트리거, 프로덕션 환경 변경 (별도 승인 필요)
Verification:
  - pnpm typecheck && pnpm lint && pnpm build 통과
  - /add 페이지에서 deed_saved 후 Day 1 토스트 확인
  - DevTools에서 streak_milestone_achieved 이벤트 확인
  - streak === 0 상태에서 앱 진입 시 재시작 카피 확인
Report back to: infinity/reports/marketing-03/{timestamp}.md
```

---

## 6. 측정 계획 (7일 후 PostHog 검증)

| 지표 | 기준 | 목표 |
|------|------|------|
| D+1 재방문 후 deed_saved | 현재 측정 불가 | ≥ 30% |
| D+3 streak_milestone_achieved | 현재 측정 불가 | ≥ 15% of D+1 유저 |
| D+7 streak_milestone_achieved | 현재 측정 불가 | ≥ 5% of D+1 유저 |
| streak_broken 이후 복귀율 | 현재 측정 불가 | ≥ 40% (within 7 days) |

> **선결 조건**: marketing-02의 deed_saved 0% 문제가 해결되어야 이 지표가 의미를 가진다.
> marketing-02 로컬 실행 (저장 버튼 개선 + 이벤트 추가)을 먼저 완료하는 것을 권장한다.

---

## 7. 범위 외 (이번 Intent 제외)

- 푸시 알림 / 리마인더 발송: L2 승인 필요, 별도 Intent
- 이메일 리텐션 캠페인: 별도 Intent
- 유료 광고 기반 D+7 리텐션 측정: 프로덕션 트래픽 필요, 별도 Intent
- deed_saved 미발생 사용자 대상 in-app 압박 메시지: 원칙 1 위반이므로 금지
