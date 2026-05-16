# marketing-02 · /add 활성화 마찰 감사

> created: 2026-05-16T14:00Z (Heartbeat L0 prepare)
> 근거: PostHog project 424014 신호, marketing-01 아카이브, product-01 코드 구조

---

## 1. 퍼널 현황 (7일 기준, 2026-05-16)

```
/add 페이지 진입   : 7 pageviews / 2 users
deed_judge_attempted : 알 수 없음 (이벤트 미구현)
deed_judged          : 1건
deed_saved           : 0건   ← 핵심 갭
```

**핵심 지표**: deed_judged→deed_saved 전환율 = **0%** (1건 judged, 0건 saved)

---

## 2. 마찰점 분석

### [P0] 채점 완료 후 저장 CTA 미완료

**가장 유력한 원인.**

코드 구조(add/page.tsx) 기준 흐름:

```
사용자 입력(메모/사진)
    → 채점 버튼 클릭
    → judgeWithFallback() 실행  → deed_judged 이벤트 발생
    → 결과 카드 표시 (score + comment + 배지)
    → [저장 버튼 or LevelUpSheet] 별도 액션 필요  → deed_saved 발생
```

deed_judged=1, deed_saved=0이라는 데이터는 채점 결과를 보고도 저장하지 않은 사용자가 있음을 의미한다.

**가능한 이탈 이유:**
- a) 저장 버튼이 결과 카드 아래에 위치해 스크롤 없이 보이지 않음
- b) 채점 완료 = 저장 완료로 오해 (UI가 완료 상태처럼 보임)
- c) LevelUpSheet가 표시되는 경우(환생 단계 달성 시) 시트 내 저장 확인 흐름이 불명확
- d) 결과를 확인하고 앱을 닫아 세션 종료

### [P1] deed_judge_attempted 이벤트 부재

현재 채점 시작 이벤트가 없어 다음을 측정할 수 없다:
- /add 진입 → 채점 시도 전환율
- 채점 시도 → 채점 완료 전환율 (API/mock 오류 감지)

marketing-01의 telemetry-fix.md에 `add_flow_started` / `add_flow_abandoned` 추가 계획이 있었으나 commit 148b1cc 내용을 보면 deed_judged 타이밍 통일만 포함됐을 가능성이 높다.

### [P2] add_flow_started / add_flow_abandoned 미구현

진입~이탈 측정 이벤트가 없어 다음 질문에 답할 수 없다:
- 2 users가 /add에 들어왔는데 채점 버튼을 눌렀는가?
- 눌렀다면 결과를 보았는가?
- 결과를 보았다면 저장 버튼을 찾지 못했는가?

### [P3] mock 배지 노출의 심리적 마찰

현재 채점 결과 카드에 "mock" 배지가 표시된다 (AI 없이 로컬 판정).
사용자가 "이건 가짜 결과"로 인식해 저장을 건너뛸 가능성이 있다.

### [P4] 사진 선택의 모호성

`judgeWithFallback`은 사진 없이도 작동하지만, UI 상 사진 추가 CTA가 첫 번째로 표시될 경우 사용자가 "사진 없으면 안 되나?"라는 의문으로 이탈할 수 있다.

---

## 3. 개선 후보 (우선순위 순)

### 후보 A — 저장 버튼 고정 + 자동 스크롤 [권장, P0 해결]

**변경**: 채점 완료 후 저장 버튼을 화면 하단에 고정(sticky) 표시하거나, 결과 카드 노출 시 자동 스크롤하여 저장 버튼이 반드시 뷰포트에 보이게 한다.

```tsx
// add/page.tsx — 결과 나타난 직후
useEffect(() => {
  if (outcome) {
    saveButtonRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}, [outcome]);

// 저장 버튼 텍스트 변경: "저장" → "덕으로 기록하기 ✓"
// 또는 sticky bottom bar로 이동
```

**예상 효과**: deed_judged→deed_saved 전환율 +30~50%p

**구현 시간**: 20분
**범위**: add/page.tsx 1파일, 스타일 변경 없음

---

### 후보 B — deed_judge_attempted + add_flow_started/abandoned 이벤트 추가 [P1,P2 해결]

**변경**: 아래 3개 이벤트를 add/page.tsx에 추가.

```ts
// 1. 페이지 진입 시 (useEffect [])
posthog.capture('add_flow_started', {
  entry_point: document.referrer || 'direct',
  species_stage: currentStage,
});

// 2. 채점 버튼 클릭 직전 (runJudge 함수 시작)
posthog.capture('deed_judge_attempted', {
  has_photo: !!file,
  has_memo: memo.trim().length > 0,
  memo_length: memo.trim().length,
  tone: currentTone,
});

// 3. 저장 없이 이탈 시 (beforeunload or router.back)
// 이미 deed_saved가 발생했다면 실행하지 않음
posthog.capture('add_flow_abandoned', {
  had_photo: !!file,
  had_memo: memo.trim().length > 0,
  had_judgment: !!outcome,
  stage: outcome ? 'post_judgment' : (memo.trim().length > 0 || file ? 'mid_entry' : 'no_input'),
});
```

**예상 효과**: 퍼널 가시성 확보, 다음 마케팅 의사결정 근거 생성
**구현 시간**: 30분
**범위**: add/page.tsx 1파일

---

### 후보 C — mock 배지를 긍정적 언어로 교체 [P3 해결]

**변경**: "mock" 배지 → "빠른 판정" 또는 배지 제거 후 AI 판정 시에만 "AI 채점" 뱃지 표시.

```tsx
// 현재: source === 'mock' → "mock" 배지
// 변경: source === 'ai' → "AI 채점" 뱃지만 표시, mock 배지 제거
{outcome.source === 'ai' && (
  <span className="text-xs px-1.5 py-0.5 rounded-full bg-positive/10 text-positive">
    AI 채점
  </span>
)}
```

**예상 효과**: 결과 신뢰도 인식 개선 → 저장율 소폭 상승
**구현 시간**: 10분
**범위**: add/page.tsx (결과 카드 배지 부분)

---

## 4. 권장 실행 순서

| 순서 | 항목 | 목적 | 예상 시간 |
|------|------|------|-----------|
| 1 | 후보 B (이벤트 3개 추가) | 퍼널 측정 기반 확보 | 30분 |
| 2 | 후보 A (저장 버튼 개선) | 즉각 전환율 개선 | 20분 |
| 3 | 후보 C (mock 배지 교체) | UX 완성도 | 10분 |

**합계**: ~1시간, 단일 로컬 실행으로 완료 가능

---

## 5. 로컬 실행 프롬프트

```markdown
Infinity Intent: marketing-02 · /add 활성화 마찰 제거
Mode: execute_local
Required workflow: workflow-master 먼저 실행. 복잡도 판단 후 진행.
Goal:
  1. add/page.tsx에 3개 PostHog 이벤트 추가 (add_flow_started, deed_judge_attempted, add_flow_abandoned)
  2. 저장 버튼 자동 스크롤 또는 sticky 개선 (채점 완료 시 버튼이 뷰포트에 확실히 보이도록)
  3. mock 배지 제거 (AI 판정 시에만 AI 채점 배지 표시)
Context:
  - 레포: /home/ubuntu/dev/virtue-rebirth-app
  - 주요 파일: src/app/add/page.tsx
  - 참고 이벤트 스펙: infinity/artifacts/marketing-02/activation-friction-audit.md §3
  - PostHog 초기화: providers.tsx or layout.tsx
Allowed: L0/L1 only (파일 수정, 테스트, 커밋, push)
Forbidden: 배포 트리거, 프로덕션 환경 변경 (별도 승인 필요)
Verification:
  - pnpm typecheck && pnpm lint && pnpm build 통과
  - /add 페이지에서 메모 입력 → 채점 → 저장 버튼이 스크롤 없이 보이는지 확인
  - 브라우저 DevTools Network에서 posthog capture 요청 3종 확인
Report back to: infinity/reports/marketing-02/{timestamp}.md
```

---

## 6. 측정 계획

7일 후 PostHog 지표로 검증:

| 지표 | 현재 | 목표 |
|------|------|------|
| deed_saved / deed_judged | 0% | ≥ 30% |
| add_flow_abandoned 비율 | 측정 불가 | < 50% |
| deed_judge_attempted 존재 | 없음 | 측정 가능 |
| add_flow_started 존재 | 없음 | 측정 가능 |

첫 번째 `deed_saved` 이벤트가 확인되면 → `marketing-03` (AI 채점 모드 전환 검토) 트리거 조건 충족.

---

## 7. 제약 (이번 Intent 범위 외)

- 프로덕션 코드 변경: 사용자 승인 후 로컬 실행으로 처리
- AI 채점 활성화 (ANTHROPIC_API_KEY 설정): marketing-03에서 별도 처리
- 광고/공개 게시물: deed_saved ≥ 1 달성 후 검토
