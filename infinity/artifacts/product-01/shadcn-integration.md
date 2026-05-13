# product-01 · shadcn/ui base-nova 도입 검토

> intent: `product-01`
> created: 2026-05-14 (heartbeat prepare)
> mode: research/prepare

## 결론 (TL;DR)

**Drawer 하나만 선택 도입 권장.**

base-nova 전체 테마 교체는 기존 OKLCH 토큰 시스템과 충돌 위험이 커서 이점 대비 비용이 높다. 업로드 흐름에 쓸 `Drawer` 컴포넌트만 선택적으로 추가하면 swipe-to-dismiss + 접근성을 얻으면서 기존 디자인 시스템을 유지할 수 있다.

---

## 현재 상태

| 항목 | 현황 |
|------|------|
| CSS | Tailwind v4 + `@theme inline` OKLCH 9채널 토큰 (purplemux 차용) |
| 폰트 | Pretendard Variable (`public/fonts/`) |
| 바텀시트 | 자체 `sheet.tsx` + `level-up-sheet.tsx` (animate-sheet-up 키프레임) |
| 업로드 모달 | `add/page.tsx` 내 인라인 상태 관리 (별도 Drawer 없음) |
| 외부 UI deps | lucide-react만 (Radix 없음) |

---

## shadcn/ui base-nova 전체 도입 분석

### 이점
- Radix Primitives 기반 접근성 (focus-trap, ARIA) 자동 제공
- base-nova 테마의 CSS 변수가 OKLCH 기반 → 철학적으로 유사
- Dialog/Sheet/Toast 등 반복 패턴을 라이브러리로 대체 가능

### 위험/비용
- shadcn/ui의 `@layer base` CSS 변수 이름 (`--background`, `--foreground`, `--radius` 등)이 purplemux 토큰과 **이름 충돌 가능성**
- `globals.css`에 shadcn/ui `@import "tw-animate-css"` + `@custom-variant dark` 추가 시 기존 키프레임 6종과 순서 충돌 가능
- 기존 커스텀 `card.tsx`, `sheet.tsx` 등을 shadcn/ui 버전으로 전면 교체하면 MVP 단계에서 불필요한 리팩터
- Tailwind v4 + shadcn/ui 2.x의 호환성은 2025년 말 기준 안정화됐으나 `next.config.ts`에서 `@tailwindcss/postcss` 구성 필요 여부 재확인 필요

**판정: 전체 도입은 MVP 이후 리팩터 시점에 검토.**

---

## Drawer 단독 도입 분석

### 왜 Drawer인가

현재 `add/page.tsx`의 업로드 흐름은 페이지 내 조건부 렌더링이다. 모바일 UX에서는 바텀 Drawer(swipe gesture 포함)가 훨씬 자연스럽다.

| 항목 | 현재 | Drawer 도입 후 |
|------|------|----------------|
| 이미지 업로드 트리거 | 페이지 내 버튼 → 인라인 표시 | FAB → Drawer 슬라이드업 |
| swipe-to-dismiss | ❌ | ✅ (Vaul 기본 제공) |
| 접근성 | 기본 | ARIA dialog role |
| 기존 sheet.tsx 영향 | 없음 (별개) | level-up-sheet는 유지, upload만 Drawer로 교체 |

### 설치 (선택 도입 방식)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm add vaul
```

shadcn/ui Drawer 소스를 직접 `components/ui/drawer.tsx`로 복사 (registry fetch 방식):
```bash
npx shadcn@latest add drawer
```

> `shadcn add`는 `globals.css`와 `components.json`을 자동 수정한다.
> `components.json`이 없으면 첫 실행 시 init 질문을 한다.
> **Tailwind v4** 프로젝트이므로 init 시 `style: default`, `tailwind.config: none` 선택.

### globals.css 충돌 방지

shadcn/ui init이 `@layer base { :root { ... } }` 를 삽입할 경우, 기존 OKLCH 변수와 다른 이름이면 무해하다. 단, 다음 변수들은 확인 필요:

```
--background   → purplemux에 없으면 충돌 없음
--foreground   → 동상
--radius       → 동상 (purplemux는 --radius-* 패턴 사용 가능)
```

추가 후 `pnpm typecheck && pnpm build` 로 즉시 확인.

### 적용 예시 (add/page.tsx)

```tsx
import { Drawer, DrawerContent, DrawerTrigger } from "@/components/ui/drawer";

export default function AddPage() {
  return (
    <Drawer>
      <DrawerTrigger asChild>
        <button className="fixed bottom-20 right-4 ...">+ 덕 쌓기</button>
      </DrawerTrigger>
      <DrawerContent>
        {/* 기존 업로드 폼 내용 */}
      </DrawerContent>
    </Drawer>
  );
}
```

---

## 권장 실행 순서

1. **이번 Wave (우선)**: AI 채점 API 연결 + 영속화 어댑터 (핵심 기능)
2. **다음 Wave**: `npx shadcn@latest add drawer` → upload 흐름 Drawer 전환
3. **MVP 이후**: 전체 shadcn/ui base-nova 도입 여부 재평가

---

## 로컬 실행 프롬프트 (Claude Code 위임용)

```
Infinity Intent: product-01 · Drawer 도입 (upload 흐름)
Mode: execute_local
Required workflow: workflow-master 먼저
Goal: add/page.tsx 업로드 흐름을 shadcn/ui Drawer로 래핑

Steps:
1. npx shadcn@latest add drawer (또는 pnpm add vaul + 수동 복사)
2. globals.css 변수 충돌 확인
3. add/page.tsx: Drawer + DrawerTrigger + DrawerContent 래핑
4. pnpm typecheck && pnpm lint && pnpm build

Allowed: L0/L1
Forbidden: 기존 level-up-sheet.tsx 수정, push
Verification: build PASS, 모바일 뷰포트에서 swipe-to-dismiss 확인
Report back to: infinity/reports/product-01/{timestamp}.md
```
