# product-01 · UX 개선 가이드

> intent: `product-01`
> created: 2026-05-14 (heartbeat prepare)
> 대상: development-notes 우선순위 1·3·4번 (보상감 강화 / 환생도감 연출 / 덕행록 일기화)
> 적용 레포: `/home/ubuntu/dev/virtue-rebirth-app`

---

## 1. 대시보드 보상감 강화 (`app/page.tsx`)

### 1-1. 스트릭(연속 덕 쌓기 일수) 표시

기존 대시보드에 연속 기록 일수를 추가하면 "매일 조금씩"의 동기가 생긴다.

**추가할 store 함수** (`src/lib/store.ts`):
```typescript
export function computeStreak(deeds: Deed[]): number {
  if (deeds.length === 0) return 0;
  const days = [...new Set(deeds.map(d => d.createdAt.slice(0, 10)))].sort().reverse();
  let streak = 0;
  let expected = new Date();
  for (const day of days) {
    const d = new Date(day);
    const diff = Math.round((expected.getTime() - d.getTime()) / 86_400_000);
    if (diff > 1) break;
    streak++;
    expected = d;
  }
  return streak;
}
```

**UI 추가** (`app/page.tsx` 덕력 카드 아래):
```tsx
const streak = computeStreak(deeds);
// ...
{streak > 0 && (
  <div className="flex items-center gap-1.5 text-sm text-[var(--ui-amber)]">
    <span>🔥</span>
    <span className="font-semibold">{streak}일 연속</span>
    <span className="text-muted-foreground">덕을 쌓는 중</span>
  </div>
)}
```

### 1-2. 이번 달 누적 모멘텀 표시

기존 `monthTotal`을 활용해 전달 대비 성장률을 보여준다.

```tsx
// 이번 달 vs 지난달 비교 — store에서 직접 파생
const thisMonth = deeds.filter(d => d.createdAt.startsWith(new Date().toISOString().slice(0,7))).reduce((s, d) => s + d.score, 0);
const lastMonth = deeds.filter(d => {
  const m = new Date(); m.setMonth(m.getMonth() - 1);
  return d.createdAt.startsWith(m.toISOString().slice(0,7));
}).reduce((s, d) => s + d.score, 0);
const growth = lastMonth > 0 ? Math.round(((thisMonth - lastMonth) / lastMonth) * 100) : null;

// 표시
{growth !== null && (
  <span className="text-xs text-muted-foreground">
    지난달보다 {growth > 0 ? `+${growth}%` : `${growth}%`}
  </span>
)}
```

### 1-3. "오늘의 첫 덕" 피드백 강화

오늘 첫 번째 덕을 쌓을 때만 나오는 특별 토스트:

```tsx
// addDeed 이후
const todayCount = deeds.filter(d => d.createdAt.startsWith(today)).length;
if (todayCount === 1) showToast('🌱 오늘의 첫 덕! 시작이 반이에요.');
```

### 1-4. 인사말 다양화

기존 `greeting.ts`를 확장하여 시즌/날씨 대신 스트릭 기반 인사 추가:

```typescript
// greeting.ts에 추가
export function getStreakGreeting(streak: number, tone: Tone): string {
  if (streak === 0) return '';
  if (streak >= 30) return tone === 'casual' ? `${streak}일째잖아, 진짜다.` : `${streak}일 연속이에요. 대단해요.`;
  if (streak >= 7)  return tone === 'casual' ? `${streak}일 연속 굿.` : `${streak}일 연속이네요.`;
  if (streak >= 3)  return tone === 'casual' ? `벌써 ${streak}일!` : `${streak}일째 함께하고 있어요.`;
  return '';
}
```

---

## 2. 환생도감 연출 개선 (`app/dex/page.tsx`)

### 2-1. 잠긴 종의 티저(실루엣) 표시

현재 잠긴 종은 "???"로만 표시. 이모지를 흐리게 보여주면 수집욕 유발.

```tsx
// 잠긴 종
<div className="relative">
  <span className="text-4xl opacity-20 blur-[2px] select-none" aria-hidden>
    {species.emoji}
  </span>
  <div className="absolute inset-0 flex items-center justify-center">
    <span className="text-xs font-medium text-muted-foreground">???</span>
  </div>
</div>
```

### 2-2. 잠금 해제 진행률 표시

현재 단계의 진행률을 각 종 카드에 표시:

```tsx
// 현재 종 카드에만 progress 표시
{stage.index === currentStage && (
  <div className="mt-2">
    <div className="h-1 rounded-full bg-muted">
      <div
        className="h-1 rounded-full bg-[var(--ui-teal)] transition-all"
        style={{ width: `${progressPercent}%` }}
      />
    </div>
    <p className="text-xs text-muted-foreground mt-1">
      다음까지 {nextThreshold - totalVirtue}덕
    </p>
  </div>
)}
```

### 2-3. 해금 시 파티클 연출 강화

기존 `LevelUpSheet`에 해금 종 이모지 3연속 팡파레 추가:

```tsx
// level-up-sheet.tsx 내부
<div className="flex justify-center gap-4 my-4">
  {[0, 1, 2].map(i => (
    <span
      key={i}
      className="text-5xl animate-virtue-pop"
      style={{ animationDelay: `${i * 0.15}s` }}
    >
      {newSpecies.emoji}
    </span>
  ))}
</div>
<p className="text-center text-sm text-muted-foreground mt-2">
  {newSpecies.blurb}
</p>
```

### 2-4. 덕성 태그 연결 (species.ts 확장)

각 환생종에 대표 덕성 태그를 붙여 일관성 부여:

```typescript
// species.ts 추가 필드
export interface Species {
  stage: number;
  emoji: string;
  name: string;
  blurb: string;
  minVirtue: number;
  maxVirtue: number;
  trait: string;        // 기존
  evolutionLine: string; // 기존
  nextHint: string;     // 기존
  tags: string[];       // 신규: 대표 덕성 태그
}

// 예시
{ stage: 3, emoji: '🦔', name: '고슴도치', tags: ['#가족', '#배려', '#일상'] },
{ stage: 5, emoji: '🐕', name: '진돗개',  tags: ['#충직', '#동물', '#이웃'] },
{ stage: 6, emoji: '🐬', name: '돌고래',  tags: ['#환경', '#사회', '#공감'] },
```

---

## 3. 덕행록 일기화 (`app/deeds/page.tsx`)

### 3-1. 날짜별 그룹 헤더를 "일기 스타일"로

기존 날짜 라벨을 일기 느낌의 헤더로 교체:

```tsx
function DiaryDateHeader({ date }: { date: string }) {
  const d = new Date(date);
  const label = formatDateLabel(date); // "오늘", "어제", "4월 30일"
  const weekday = d.toLocaleDateString('ko-KR', { weekday: 'long' }); // "수요일"
  return (
    <div className="flex items-baseline gap-2 py-2 border-b border-muted mb-3">
      <span className="text-base font-semibold">{label}</span>
      <span className="text-xs text-muted-foreground">{weekday}</span>
    </div>
  );
}
```

### 3-2. 날짜별 소계 표시

각 날짜 그룹에 그날 합계 표시:

```tsx
const dayTotal = dayDeeds.reduce((s, d) => s + d.score, 0);
// 헤더 오른쪽에:
<span className="ml-auto text-sm text-[var(--ui-amber)] font-medium">
  +{dayTotal}덕
</span>
```

### 3-3. 덕행 카드에 태그 칩 표시

기존 카드에 `tags` 배열을 `TagChip` 컴포넌트로 표시 (컴포넌트 이미 존재):

```tsx
<div className="flex flex-wrap gap-1 mt-1.5">
  {deed.tags.map(tag => <TagChip key={tag} label={tag} />)}
</div>
```

### 3-4. 빈 상태 카피 개선

기존 `EmptyState`에 더 일기스러운 메시지:

```tsx
<EmptyState
  icon="book-open"
  title="아직 기록이 없어요"
  description="오늘 선행 한 가지를 사진으로 남겨보세요. 나중에 다시 봤을 때 뿌듯할 거예요."
/>
```

### 3-5. 월별 요약 카드 (상단 고정)

덕행록 최상단에 이번 달 요약:

```tsx
function MonthSummaryCard({ deeds }: { deeds: Deed[] }) {
  const thisMonthDeeds = deeds.filter(d => d.createdAt.startsWith(new Date().toISOString().slice(0,7)));
  const total = thisMonthDeeds.reduce((s, d) => s + d.score, 0);
  const days = new Set(thisMonthDeeds.map(d => d.createdAt.slice(0,10))).size;
  return (
    <div className="rounded-xl bg-muted/40 p-4 mb-4">
      <p className="text-xs text-muted-foreground mb-1">이번 달</p>
      <p className="text-2xl font-bold">{total}<span className="text-sm font-normal text-muted-foreground ml-1">덕</span></p>
      <p className="text-xs text-muted-foreground mt-0.5">{days}일 동안 덕을 쌓았어요</p>
    </div>
  );
}
```

---

## 4. 로컬 실행 프롬프트

```markdown
Infinity Intent: product-01 · UX 개선 (보상감·도감·덕행록)
Mode: execute_local
Required workflow: workflow-master 먼저 실행. 복잡도 판단 후 진행.
Goal: development-notes 우선순위 1·3·4번 구현
  1. 대시보드: 스트릭 표시 + 이번달 모멘텀 + 첫덕 토스트 + 스트릭 인사말
  2. 환생도감: 잠긴 종 실루엣 + 단계 내 진행률 + LevelUpSheet 파티클 강화 + 덕성 태그
  3. 덕행록: 날짜 헤더 일기화 + 날짜별 소계 + 태그 칩 + 빈 상태 카피 + 월별 요약 카드
Context:
  - 레포: /home/ubuntu/dev/virtue-rebirth-app
  - 설계: infinity/artifacts/product-01/ux-improvement-guide.md (이 파일)
  - 기존 컴포넌트: TagChip, EmptyState, AnimatedNumber, LevelUpSheet 이미 존재
  - 기존 유틸: formatDateLabel, formatRelativeDay (format.ts), computeStreak 미구현
Allowed: L0/L1 only
Forbidden: L2/L3 without approval
Verification: pnpm typecheck && pnpm lint && pnpm build → 5 페이지 시각 확인
Report back to: infinity/reports/product-01/{timestamp}.md
```

---

## 5. 예상 난이도

| 항목 | 난이도 | 예상 시간 |
|------|--------|-----------|
| 스트릭 + 첫덕 토스트 | 쉬움 | 30분 |
| 이번달 모멘텀 | 쉬움 | 15분 |
| 스트릭 인사말 | 쉬움 | 10분 |
| 환생도감 실루엣 | 쉬움 | 20분 |
| 도감 진행률 | 보통 | 30분 |
| LevelUpSheet 파티클 | 쉬움 | 20분 |
| 덕성 태그 연결 | 보통 | 30분 |
| 덕행록 일기화 | 보통 | 45분 |
| 월별 요약 카드 | 쉬움 | 20분 |
| **합계** | | **~3.5시간** |
