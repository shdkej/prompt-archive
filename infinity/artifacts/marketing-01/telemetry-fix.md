# marketing-01 · PostHog 텔레메트리 개선안

> created: 2026-05-15 (heartbeat L0 prepare)
> 근거: PostHog project 424014 신호, marketing-01 inbox 분석

---

## 1. 현상

PostHog 7일 기준:
- `$exception` 4건 — message/type 모두 null → 디버그 불가
- `deed_judged` 1건 — 활성화 이벤트 시작점
- `deed_saved` 0건 — 사용자 여정이 완료되지 않음
- `deed_scored` 0건 / `deed_score_failed` 0건 — mock 모드이므로 예상됨

---

## 2. $exception 누락 루트 콜즈

### 가능성 A — React Error Boundary 누락 or 미통합

Next.js App Router는 `error.tsx` boundary를 통해 에러를 처리.
boundary가 에러를 catch하면 `window.onerror`가 트리거되지 않아 PostHog 기본 SDK가 놓침.

`error.tsx`가 없거나, 있어도 PostHog `captureException` 호출을 포함하지 않으면 누락 발생.

### 가능성 B — Promise rejection이 Error 객체가 아님

`fetch` 실패나 API route 에러가 `throw "string"` 형태이면 message/type이 null로 캡처됨.
PostHog SDK는 `error.message`, `error.name`을 읽는데, plain string rejection은 이 프로퍼티가 없음.

### 가능성 C — PostHog SDK 버전 / 설정 이슈

`a12aeab` (PostHog 통합 커밋)의 초기 설정에서 `capture_exceptions: true` 옵션 미포함 가능성.
또는 `posthog.init` 시 `loaded` 콜백 이전에 exception이 발생해서 누락.

---

## 3. 수정안

### 3-1. error.tsx에 captureException 추가

```tsx
// src/app/error.tsx
'use client';
import { useEffect } from 'react';
import posthog from 'posthog-js';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    posthog.captureException(error, {
      flow: 'app-error-boundary',
      digest: error.digest,
    });
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
      <p className="text-muted-foreground">앗, 문제가 생겼어요.</p>
      <button onClick={reset} className="text-sm underline">
        다시 시도
      </button>
    </div>
  );
}
```

### 3-2. deed 이벤트에 디버그 프로퍼티 추가

현재 `deed_judged` 이벤트는 최소 정보만 담긴 것으로 추정.
아래 프로퍼티를 추가해야 퍼널 단계별 원인 파악 가능:

```ts
// add/page.tsx의 deed 저장 성공 시
posthog.capture('deed_saved', {
  score: outcome.score,
  source: outcome.source,           // 'ai' | 'mock'
  has_photo: !!file,
  tone: currentTone,
  memo_length: memo.trim().length,
  species_stage: currentStage,      // 환생 단계
  daily_deed_count: todayCount,
});

// deed_judged 이벤트 (채점 직후)
posthog.capture('deed_judged', {
  source: outcome.source,
  score: outcome.score,
  fallback_reason: outcome.fallbackReason ?? null,
  has_photo: !!file,
  tone: currentTone,
  retry_count: retryCount,
});
```

### 3-3. 퍼널 시작/종료 이벤트 추가

```ts
// add/page.tsx 진입 시 (useEffect)
posthog.capture('add_flow_started', {
  entry_point: document.referrer || 'direct',
  species_stage: currentStage,
});

// 저장 없이 뒤로 나갈 때 (beforeunload 또는 router push 감지)
posthog.capture('add_flow_abandoned', {
  had_photo: !!file,
  had_memo: memo.trim().length > 0,
  had_judgment: !!outcome,
});
```

### 3-4. exception 캡처 옵션 명시

```ts
// providers.tsx or layout.tsx PostHog init
posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
  api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? 'https://us.i.posthog.com',
  capture_exceptions: true,       // ← 명시 추가
  autocapture: true,
});
```

---

## 4. 구현 우선순위

| 항목 | 우선순위 | 예상 시간 | 효과 |
|------|---------|-----------|------|
| error.tsx captureException | 최고 | 15분 | $exception에 stack/message 보임 |
| deed_judged 프로퍼티 확장 | 높음 | 20분 | 퍼널 단계 분석 가능 |
| deed_saved 프로퍼티 확장 | 높음 | 20분 | 저장 성공 조건 파악 |
| add_flow_started/abandoned | 중간 | 30분 | 진입/이탈 지점 분석 |
| capture_exceptions: true | 낮음 | 5분 | 보험성, 효과 미확인 |

---

## 5. 측정 계획 (7일 후)

- Primary: `deed_saved / deed_judged` 비율 ≥ 30% 목표
- Secondary: `$exception` 이벤트에 message/type 필드 존재 → 디버그 가능 상태
- Tertiary: `add_flow_abandoned` 이벤트 발생 여부 → 이탈 지점 특정
