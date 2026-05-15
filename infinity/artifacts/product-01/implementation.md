# product-01 · 스캐폴드 + 디벨롭 구현 메모

> intent: `product-01`
> created: 2026-05-13
> last update: 2026-05-13 (Vision API wave)
> status: MVP UI + AI 채점 API 경로 존재 (현재 운영은 mock · 2026-05-15 사용자 결정: 활성화 후보는 Gemini 기준으로 전환 · 모든 페이지 store 연결 · 빌드 통과)

## 결정 사항

- **레포 위치**: 신규 분리 → `/home/ubuntu/dev/virtue-rebirth-app` (로컬 전용, push 없음).
- **스택**: Next.js 15.1.6 (App Router) + React 19 + TypeScript + Tailwind CSS v4 + lucide-react.
- **디자인 시스템 차용원**: `/home/ubuntu/dev/pt` (purplemux) — OKLCH 9채널 토큰, `--brand=ui-purple`, `--positive=ui-teal`, Pretendard Variable. purplemux 원본 무수정.
- **상태 관리**: 외부 의존성 무추가. `useSyncExternalStore` 기반 자체 store (`src/lib/store.ts`) + localStorage 4 키.

## 구조 (현재)

```
virtue-rebirth-app/
├── package.json            # next 15.1.6 / react 19 / tailwind v4 (외부 의존 신규 없음)
├── tsconfig.json · next.config.ts · postcss.config.mjs · eslint.config.mjs
├── README.md               # 디벨롭 후 동기화 (스크립트/메뉴/상태 흐름/폴더 구조)
├── docs/
│   ├── design-system-notes.md   # OKLCH·Pretendard 차용 정리
│   └── copy-spec.md             # 신규 — 한국어 카피 델타 + 톤 가이드 + 금지어
├── public/fonts/PretendardVariable.woff2
└── src/
    ├── styles/globals.css       # OKLCH 토큰 + @theme inline + 키프레임 6종 (virtue-pop, soft-fade, sheet-up, sparkle-rise, count-bounce, shine)
    ├── lib/
    │   ├── cn.ts
    │   ├── format.ts            # formatTimeAgo, formatDateLabel, formatRelativeDay
    │   ├── species.ts           # 11 단계 + trait/evolutionLine/nextHint + getSpeciesFor/getRecentlyUnlocked
    │   ├── judge.ts             # 키워드 라우팅 + 톤(soft/casual) + 50+ 코멘트 + pickWeightedScore
    │   ├── mock-data.ts         # IDeed/MOCK_DEEDS(14)/INITIAL_VIRTUE/DAILY_CAP + computeToday/Yesterday/MonthTotal
    │   ├── store.ts             # 신규 — useDeeds/useVirtueStats/addDeed/clearDeeds/exportJson/useTone/useDailyCapEnabled/useTheme
    │   └── greeting.ts          # 신규 — 시간대(아침/낮/저녁/밤) × 톤별 인사
    ├── components/
    │   ├── bottom-nav.tsx · card.tsx · progress-bar.tsx (기존)
    │   ├── animated-number.tsx · score-pill.tsx · empty-state.tsx (신규)
    │   ├── tag-chip.tsx · sparkle-glow.tsx (신규)
    │   ├── sheet.tsx · level-up-sheet.tsx (신규)
    │   ├── toast.tsx · greeting.tsx (신규)
    └── app/
        ├── layout.tsx           # 테마 플래시 방지 inline script + ToastViewport 마운트
        ├── page.tsx             # 1. 덕력 (dashboard) — store 기반, 인사/카운트업/SparkleGlow
        ├── add/page.tsx         # 2. 덕 쌓기 — addDeed + LevelUpSheet + 일일 캡 차단 + 재채점 3회 제한
        ├── deeds/page.tsx       # 3. 덕행록 — useDeeds + 일자 그룹 + EmptyState
        ├── dex/page.tsx         # 4. 환생도감 — useVirtueStats + 잠긴 단계 ??? 다음 생의 비밀.
        └── me/page.tsx          # 5. 나 — useTone/useDailyCapEnabled/useTheme + JSON export + clearDeeds
```

## Vision API wave (2026-05-13)

| 영역 | 변경 |
|------|------|
| 의존성 | `zod@4.4.3` + `@anthropic-ai/sdk@0.96.0` 추가. |
| 서버 라우트 | `src/app/api/score/route.ts` (Node runtime, dynamic). 현재 구현은 `ANTHROPIC_API_KEY` 없으면 503 + `scoring_disabled`. 단, 다음 활성화 방향은 사용자 결정에 따라 Gemini Vision 계열로 전환. SDK 호출 → 텍스트 응답에서 JSON 추출 → `ScoreResultSchema.safeParse` 구조는 재사용 가능. |
| 스키마 | `src/lib/score-schema.ts` — `ScoreRequestSchema` (image base64 ≤ 7.5MB, mime jpeg/png/gif/webp, memo ≤ 500자, toneMode soft/casual) + `ScoreResultSchema` (score 0-10, comment ≤ 120자, tags ≤ 2). |
| 시스템 프롬프트 | `src/lib/score-prompt.ts` — `ai-scoring-prompt.md` 원문 그대로, `{{toneMode}}` 치환. |
| 클라이언트 | `src/lib/score-client.ts` — `judgeWithFallback({file, memo, tone})`. 사진 없거나 mime 미허용 → mock. fetch 실패/비-200 → mock. 성공 → `source: "ai"` + model 표기. |
| Add 페이지 | `mockJudge` 직접 호출 제거. `File` state 추가. 결과 카드 배지가 `source` 따라 "AI"(positive 색) / "mock"(muted) 동적 표시. 하단 안내 한 줄 업데이트. |
| 환경 변수 | 현재 `.env.example`: `ANTHROPIC_API_KEY`, `SCORING_MODEL` (기본 `claude-sonnet-4-6`). Gemini 전환 시 `GEMINI_API_KEY`/모델명 기준으로 갱신 필요. |
| 문서 | `README.md` — `/api/score` 요청/응답 스펙, 상태 코드, 환경 변수 표 추가. |
| 검증 | `pnpm typecheck` ✅ · `pnpm lint` ✅ (warning 0) · `pnpm build` ✅ (8 routes, `/api/score`는 dynamic). |
| 톤 보존 | 도덕적 칭찬/설교 금지 룰은 시스템 프롬프트에 그대로. mock 폴백 코멘트는 기존 `judge.ts` 풀 그대로. |

알려진 한계 (다음 단계):
- 사진은 여전히 blob URL preview만, 영속화 미구현.
- 일일 30덕 캡은 클라이언트 가드만 — 서버 검증 없음.
- 동일 사진 중복 업로드 감지/차감 미구현.
- ~~AI 실패 → mock 폴백 시 사용자에게 별도 안내 없음 (배지로만 구분).~~ ✅ 해소 (2026-05-13 Fallback UX wave).

## Fallback UX wave (2026-05-13)

| 영역 | 변경 |
|------|------|
| 클라이언트 | `IJudgeOutcome`에 `fallbackReason?: "api_error" \| "network_error"` 추가. `res.ok === false` → `api_error`, `catch` → `network_error`. 사진 없음/미허용 mime는 의도된 mock이라 `fallbackReason` 미설정. |
| Add 페이지 | `runJudge` 결과에 `fallbackReason`이 있으면 토스트 1회: `AI가 잠깐 졸고 있어요. 임시 판정으로 보여드릴게요.` 배지(AI/mock)는 그대로. |
| 카피 | `docs/copy-spec.md`의 Operator 마이크로카피 표에 "AI 응답 실패 → mock 폴백" 행 추가, 기존 재시도 유도 카피와 분리. |
| 검증 | `pnpm typecheck` ✅ · `pnpm lint` ✅ · `pnpm build` ✅. |

## 디벨롭 핵심 (이번 wave)

| 영역 | 변경 |
|------|------|
| 상태 영속화 | `useSyncExternalStore` 기반 store, 키 4종 (`virtue.rebirth.v1` / `virtue.tone.v1` / `virtue.dailycap.v1` / `virtue.theme.v1`). 첫 로드 시 `MOCK_DEEDS` 14건 시드. 크로스탭 sync. |
| 채점 톤 | `mockJudge(memo, tone)`로 시그니처 확장. 메모 키워드 라우팅(배려/이웃/환경/동물/가족/동료/일반) × soft/casual × 50+ 코멘트. 점수 가중 분포 2~3 중심. |
| 환생 진화 | `getRecentlyUnlocked(prev, next)` 통과 시 `LevelUpSheet` 바텀시트 ( `animate-virtue-pop` 이모지 + `animate-sparkle-rise` ✨ × 7). |
| 일일 30덕 상한 | 차단 방식(클램프 X). 토스트 "오늘은 충분히 쌓았어요. 내일 또 봐요." |
| 재채점 제한 | 한 사이클 3회. 버튼에 잔여 횟수 칩 노출 + 0회 시 비활성화. |
| 테마 적용 | layout `<head>`에 inline 스크립트로 hydration 전에 `dark` 클래스 토글 → 플래시 없음. |
| 카피 | `docs/copy-spec.md` 가이드 적용. 도덕적 칭찬/설교/격언 금지 룰 준수. |
| 글로벌 토스트 | `showToast(msg)` 임의 호출 (`useToast` 훅 없이 모듈 싱글톤). 자동 디스미스 2.4s. |

## 검증 결과 (2026-05-14)

| 검증 | 결과 |
|------|------|
| `pnpm typecheck` | ✅ PASS |
| `pnpm lint` | ✅ PASS (warning 0) |
| `pnpm build` | ✅ PASS (8/8 static prerender, First Load JS 105–122 kB) |
| `pnpm start` + 5 페이지 HTTP probe | ✅ 200 × 5 |
| 헤드리스 스크린샷 | ✅ 5 페이지 (`infinity/reports/product-01/2026-05-14T00-50-screens/`) |

## 로컬 git

- `45a5cf3` — 초기 스캐폴드 (2026-05-13)
- `6ba58a8` — MVP 디벨롭: 로컬 상태 / 판정 / 환생 진화 인터랙션 강화 (2026-05-14)
- 사용자 컨펌 없이는 origin 미설정, push 없음.

## Next Actions

1. ~~mock judge → Claude Sonnet 4.6 vision API 연결~~ ✅ 완료 (2026-05-13).
2. 실제 API 키로 end-to-end 검증 (현재는 build/typecheck/lint만 통과, 실호출 미검증). 키 없는 상태에서 503 응답이 오면 fallback 토스트가 한 번만 뜨는지도 같이 확인.
3. 서버 측 일일 30덕 캡 검증 (DB 또는 stateless 카운트).
4. 영속화 결정 — Supabase Postgres + Storage 또는 SQLite + Tailscale. store 어댑터 패턴으로 교체.
5. shadcn/ui base-nova 도입 검토 — Drawer/Sheet으로 업로드 흐름 통합.
6. 사진 영속화: 현재 blob URL preview만. 저장 시 server-side로 업로드.
7. 다국어/공유/도전 과제 — MVP 후 단계.
8. 배포 도메인 결정 (`virtue.oracle.shdkej.com`).
