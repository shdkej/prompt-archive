# virtue-rebirth-app 스캐폴드 준비 계획

> intent: `product-01`
> status: ready-to-execute (레포 결정 후 즉시 실행 가능)
> 작성: 2026-05-13

## 전제 조건

- 레포 결정: **신규 `virtue-rebirth-app`** 권장 (purplemux와 도메인 분리)
- 디자인 토큰 출처: `/home/ubuntu/dev/pt` (purplemux) shadcn/ui base-nova 설정 차용

---

## Step 1. 프로젝트 초기화

```bash
# 위치: /home/ubuntu/dev/ 또는 /home/ubuntu/workspace/
pnpm create next-app virtue-rebirth-app \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-git  # 별도 git init 예정
cd virtue-rebirth-app

# shadcn/ui base-nova 초기화 (purplemux 동일 설정)
pnpm dlx shadcn@latest init
# → style: base-nova, baseColor: neutral, CSS vars: yes
```

## Step 2. 의존성 설치

```bash
pnpm add \
  @anthropic-ai/sdk \
  vaul \
  sonner \
  dayjs \
  zustand \
  zod \
  next-themes \
  tw-animate-css

pnpm add -D @types/node
```

## Step 3. shadcn 컴포넌트 추가

```bash
pnpm dlx shadcn@latest add \
  button card sheet drawer tabs progress skeleton badge
```

## Step 4. 디렉토리 구조

```
src/
  app/
    (tabs)/
      layout.tsx          ← 하단 탭 네비게이션 (고정)
      page.tsx            ← 덕력 대시보드 (/)
      deed/
        page.tsx          ← 덕 쌓기 (사진 업로드)
      history/
        page.tsx          ← 덕행록
      profile/
        page.tsx          ← 나 (설정)
    api/
      score/
        route.ts          ← Claude Sonnet 4.6 vision API
    globals.css
    layout.tsx            ← RootLayout (next-themes Provider)
  components/
    species-card.tsx      ← 환생종 진행 카드
    deed-upload.tsx       ← 사진 업로드 + vaul Drawer
    score-card.tsx        ← AI 채점 결과 카드
    deed-list.tsx         ← 덕행 타임라인
  lib/
    species.ts            ← SpeciesDef 상수 테이블
    db.ts                 ← DB 클라이언트 (Supabase or SQLite)
    utils.ts              ← cn() 등
  types/
    index.ts              ← Deed, VirtueSnapshot 타입
```

## Step 5. 핵심 파일 초안

### `src/lib/species.ts`

```typescript
export const SPECIES: SpeciesDef[] = [
  { stage: 0, name: "돌",     emoji: "🪨", min: 0,     max: 49,    blurb: "출발은 무생물부터." },
  { stage: 1, name: "송충이", emoji: "🐛", min: 50,    max: 199,   blurb: "꿈틀거리기 시작했어요." },
  { stage: 2, name: "달팽이", emoji: "🐌", min: 200,   max: 499,   blurb: "느리지만 어쨌든 동물." },
  { stage: 3, name: "고슴도치",emoji:"🦔", min: 500,   max: 999,   blurb: "이제 포유류!" },
  { stage: 4, name: "길고양이",emoji:"🐈", min: 1000,  max: 1999,  blurb: "이웃에 사랑받는 단계." },
  { stage: 5, name: "진돗개", emoji: "🐕", min: 2000,  max: 3999,  blurb: "충직하고 멋짐." },
  { stage: 6, name: "돌고래", emoji: "🐬", min: 4000,  max: 6999,  blurb: "지능 + 사회성." },
  { stage: 7, name: "코끼리", emoji: "🐘", min: 7000,  max: 9999,  blurb: "기억하고 슬퍼할 줄 안다." },
  { stage: 8, name: "인간(다시)",emoji:"🧑",min: 10000, max: 19999, blurb: "한 번 더 인간으로." },
  { stage: 9, name: "???",    emoji: "✨", min: 20000, max: Infinity, blurb: "?" },
];

export function getSpecies(total: number): SpeciesDef {
  return [...SPECIES].reverse().find(s => total >= s.min) ?? SPECIES[0];
}

export function getProgress(total: number): number {
  const s = getSpecies(total);
  if (s.max === Infinity) return 1;
  return (total - s.min) / (s.max - s.min + 1);
}
```

### `src/app/(tabs)/layout.tsx` (하단 탭)

```tsx
import { Sparkles, Camera, BookOpen, Bird, UserRound } from "lucide-react";

export default function TabsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-dvh max-w-md mx-auto">
      <main className="flex-1 overflow-y-auto pb-16">{children}</main>
      <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto border-t bg-background
                      pb-[env(safe-area-inset-bottom)]">
        {/* 탭 구현 — next/navigation usePathname 기반 active 강조 */}
      </nav>
    </div>
  );
}
```

## Step 6. DB 선택지 (결정 대기)

| 옵션 | 장점 | 단점 |
|------|------|------|
| **Supabase** (권장) | 관리형, Storage 포함, 무료 tier | 외부 의존성 |
| **SQLite + Tailscale** | 완전 로컬, 인터넷 불필요 | 서버 직접 관리 |
| **Vercel KV + Blob** | Vercel 배포에 최적 | 비용 발생 가능 |

> 개인용 + oracle 인스턴스 배포 → **Supabase** 권장 (Storage 이미지 + Postgres 메타)

## Step 7. 배포 설정

oracle 인스턴스 nginx 신규 서버 블록 (기존 infinity-kanban 패턴):

```nginx
server {
    listen 80;
    server_name virtue.oracle.shdkej.com;
    location / {
        proxy_pass http://localhost:3001;  # Next.js standalone
    }
}
```

PM2 또는 `next start -p 3001`.

---

## 실행 준비 체크리스트 (레포 결정 후)

- [ ] 레포 위치 확정 (신규 vs dev/pt)
- [ ] DB 선택 (Supabase vs SQLite)
- [ ] AI 호출 방식 확정 (route.ts 서버사이드 = 권장)
- [ ] `ANTHROPIC_API_KEY` 환경변수 설정
- [ ] Supabase 프로젝트 생성 (해당 시)
- [ ] pnpm 설치 및 스캐폴드 실행
- [ ] nginx 서버 블록 추가 (L2: oracle 인스턴스 접근)
