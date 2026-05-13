# product-01 · 스캐폴드 구현 메모

> intent: `product-01`
> created: 2026-05-13
> status: scaffold complete (MVP UI shell, mock data only)

## 결정 사항

- **레포 위치**: 신규 분리 → `/home/ubuntu/dev/virtue-rebirth-app` (로컬 전용, push 없음).
- **스택**: Next.js 15.1.6 (App Router) + React 19 + TypeScript + Tailwind CSS v4 + lucide-react.
- **디자인 시스템 차용원**: `/home/ubuntu/dev/pt` (purplemux) — OKLCH 9채널 토큰, `--brand=ui-purple`, `--positive=ui-teal`, Pretendard Variable. purplemux 원본 무수정.

## 구조

```
virtue-rebirth-app/
├── package.json            # next 15.1.6 / react 19 / tailwind v4
├── tsconfig.json
├── next.config.ts
├── postcss.config.mjs
├── eslint.config.mjs       # FlatCompat → next/core-web-vitals + next/typescript
├── README.md
├── docs/
│   └── design-system-notes.md
├── public/fonts/PretendardVariable.woff2   # pt에서 복사
└── src/
    ├── styles/globals.css   # OKLCH 토큰 + @theme inline + animate-virtue-pop
    ├── lib/
    │   ├── cn.ts
    │   ├── format.ts
    │   ├── species.ts       # 환생종 10단계 정의 + getSpeciesFor()
    │   ├── judge.ts         # mock AI 채점 결과 풀
    │   └── mock-data.ts     # 6건 데이터 + 누적값
    ├── components/
    │   ├── bottom-nav.tsx   # 하단 5탭 sticky + safe-area
    │   ├── card.tsx
    │   └── progress-bar.tsx
    └── app/
        ├── layout.tsx       # max-w-md mobile shell
        ├── page.tsx         # 1. 덕력 (대시보드)
        ├── add/page.tsx     # 2. 덕 쌓기 (사진+메모+mock 채점)
        ├── deeds/page.tsx   # 3. 덕행록 (일자별 타임라인)
        ├── dex/page.tsx     # 4. 환생도감 (10단계 잠금/현재 표시)
        └── me/page.tsx      # 5. 나 (톤/캡/테마/export 토글)
```

## 검증 결과

| 검증 | 결과 |
|------|------|
| `pnpm install` | 성공 |
| `pnpm typecheck` (`tsc --noEmit`) | 통과 |
| `pnpm lint` (`next lint`) | 통과, warning 1건 (add 페이지의 `<img>` — Image 컴포넌트 권장, mock 단계 OK) |
| `pnpm build` (`next build`) | 통과, 정적 prerender 8 routes, First Load JS 105 kB 공유 |

## 로컬 git

- 초기 커밋 `45a5cf3` — `초기 스캐폴드: 덕 쌓기 · 환생 모바일 웹앱` (작성자: `Local Scaffold`).
- 사용자가 push 명령 줄 때까지 origin 미설정.

## 톤/디자인 노트 (요약)

- CTA 한 곳에만 `--brand` (보라). 누적/긍정은 `--positive` (teal). 채점 점수는 `--ui-amber`로 따뜻하게 강조.
- 채점 결과 카드는 `animate-virtue-pop` (420ms ease-out-back). confetti 등 과한 모션 배제.
- 환생도감의 잠긴 종은 `❓` + `opacity-60`. 현재 종은 `ring-2 var(--brand)`.
- 모든 텍스트 한국어. 도덕적 칭찬/설교 금지 가이드라인을 mock judge 코멘트에 미리 반영 ("음, 이건 그냥 사진인 것 같은데요" 등).

## Open Questions → 후속에서 결정

- AI 호출 위치 (`/app/api/score/route.ts` server-side? vs 외부 워커?)
- 사진 영속화 (Supabase Storage vs R2 vs 로컬)
- 다크 모드 토글의 실제 동작 (`next-themes` 도입 시점)
- shadcn/ui base-nova 풀 도입 vs 현재 hand-roll 컴포넌트 유지
- 배포 도메인 결정 (`virtue.oracle.shdkej.com` 권장)

## Next Actions

1. mock judge → Claude Sonnet 4.6 vision API (zod 스키마 강제, §5 톤 가이드 시스템 프롬프트).
2. SQLite + better-sqlite3 또는 Supabase 도입해 첫 진짜 deed 저장.
3. shadcn/ui base-nova 초기화 → 업로드를 vaul Drawer로 옮기기.
4. 다크 모드 실 적용 + 톤(soft/casual) 토글이 mock judge에도 반영되게 연결.
