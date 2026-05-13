# 덕 쌓기 · 환생 모바일 웹앱 — 제품/디자인 기획서

> intent: `product-01`
> status: draft (2026-05-13)
> 영감: 드라마/영화 *Brush Up Life* — 다시 태어날 때 어떤 종으로 환생할지가 누적된 선행으로 결정된다는 컨셉.

## 1. 제품 컨셉

평범한 일상 속 선행(`덕`)을 사진으로 기록하면 AI가 "덕력"을 채점하고, 누적 덕력에 따라 다음 생에 환생할 **종(種)**이 변화하는 가벼운 라이프 로그 게임.

- 톤: 진지·교훈적이 아닌 **장난스럽고 따뜻한** 분위기. "도덕적으로 옳다"가 아니라 "오늘 좀 괜찮은 인간이었나" 정도의 자기 만족.
- 핵심 가치: 하루 1~2회 30초 안에 끝나는 마이크로 액션. 강박 없는 누적 만족감.
- 타겟: 본인 (개인용 라이프 로그). 추후 가족/친구 공유 옵션은 후순위.

## 2. 코어 루프

```
선행 발생
  ↓
인증 사진 촬영 (또는 갤러리 선택)
  ↓
짧은 한 줄 메모 (선택)
  ↓
AI 덕력 채점 (0 ~ 10 덕)
  ↓
덕력 누적 → 환생종 진행
  ↓
대시보드에서 현재 환생종/누적 덕력 확인
```

- 1회 채점은 0~10 덕 (1자리 정수). 일일 상한 30덕 정도로 가벼운 캡.
- AI는 채점 + **한 문장 코멘트**만. 설교 금지.
- 동일/유사 사진 반복 방지를 위해 최근 N장과 임베딩 유사도 비교 (MVP 이후).

## 3. 메뉴 IA (최대 5개)

| # | 메뉴 | 아이콘(lucide) | 역할 |
|---|------|----------------|------|
| 1 | **덕력** (대시보드) | `sparkles` | 메인. 나의 덕력 + 환생종 |
| 2 | **덕 쌓기** | `camera` | 인증 사진 업로드 + AI 채점 |
| 3 | **덕행록** | `book-open` | 누적된 선행 타임라인 |
| 4 | **환생도감** | `bird` | 환생종 컬렉션/진화 단계 |
| 5 | **나** | `user-round` | 설정, 데이터 내보내기, 톤 설정 |

> 1번이 진입 화면(`/`). 하단 탭 네비게이션(`Tabs` 컴포넌트 기반)로 고정.

추천 근거:
- **덕행록**은 "내가 뭘 했지" 회상 동기를 유지 — 게임에서 도장 깨기와 같은 역할.
- **환생도감**은 누적 보상 시각화. 새 종 발견 자체가 보상 이벤트.
- **나** 탭은 톤/난이도 조정과 데이터 export를 한 곳에 모아 다른 탭을 가볍게 유지.

## 4. 메인 화면 (`덕력`) 콘텐츠 계층

```
┌─────────────────────────────────┐
│ 헤더: 오늘 날짜 · 인사 한 줄    │  (예: "오늘 1덕만 쌓아볼까요?")
├─────────────────────────────────┤
│                                 │
│      나의 덕력  ★ 1,247         │  (큰 숫자, 단위 "덕")
│      이번 달 +83 · 어제 +4      │
│                                 │
├─────────────────────────────────┤
│   환생종: 🦔 고슴도치 (Lv.3)    │  (일러스트/이모지 + 종명)
│   ━━━━━━━━━━━━░░░░ 73%         │  (다음 종까지 진행 바)
│   다음: ??? (잠금)              │
├─────────────────────────────────┤
│   [📷 오늘 덕 쌓기]              │  (대형 primary 버튼)
├─────────────────────────────────┤
│ 최근 덕행 (3개 미리보기)         │
│ · 09:12  +2  지하철 자리 양보   │
│ · 어제   +3  이웃 택배 받아줌   │
│ · ...                           │
└─────────────────────────────────┘
```

- 숫자는 셀 수 있는 단위로 표현: `1,247덕`.
- "다음 환생종"은 일부 잠금/티저로 — 진행 동기.
- CTA 버튼은 항상 화면 중앙 근처. 한 손 도달 영역.

## 5. AI 채점 UX

업로드 흐름:

1. **사진 입력** — 카메라 또는 갤러리. 한 번에 1장. 추후 멀티 사진.
2. **한 줄 메모** (선택) — placeholder "뭐 했어요?" (없으면 AI가 사진만으로 추정).
3. **AI 채점 카드** — 등장 애니메이션 후 다음 3 요소만 표시:
   - 점수: `+3 덕` (큰 숫자, brand 색)
   - 한 줄 코멘트: "지하철에서 자리를 양보한 듯한 장면이네요. 조용히 잘했어요." (1~2문장)
   - 작은 태그: `#배려`, `#일상`
4. **확정/되돌리기** — 저장 / "한 번 더 채점" / 취소.

톤 가이드라인 (시스템 프롬프트에 명시):

- 채점은 너무 후하거나 박하지 않게. 평균 2~3덕에 분포.
- **금지**: "훌륭한 일을 하셨군요", "당신은 좋은 사람입니다" 같은 도덕적 칭찬, 교훈, 격언.
- **권장**: 사실 묘사 + 가벼운 농담 1줄. 한국어 반말/존댓말은 사용자 설정값을 따른다 (기본 부드러운 존댓말).
- 사진에서 선행 단서를 못 찾으면 `0덕 — 음, 이건 그냥 사진인 것 같은데요` 식으로 솔직하게.

악용 방지 (MVP 이후):

- 인터넷 짤/스크린샷 감지 → 0덕.
- 동일 사진 재업로드 → 차감.
- 일일 30덕 상한.

## 6. 환생종 진행 (예시)

레벨이 아닌 **누적 덕력 임계치**로 진화. 톤은 귀엽고 살짝 위트.

| 단계 | 누적 덕 | 종 | 한 줄 |
|------|---------|-----|-------|
| 0 | 0 ~ 49 | 🪨 돌 | "출발은 무생물부터." |
| 1 | 50 ~ 199 | 🐛 송충이 | "꿈틀거리기 시작했어요." |
| 2 | 200 ~ 499 | 🐌 달팽이 | "느리지만 어쨌든 동물." |
| 3 | 500 ~ 999 | 🦔 고슴도치 | "이제 포유류!" |
| 4 | 1,000 ~ 1,999 | 🐈 길고양이 | "이웃에 사랑받는 단계." |
| 5 | 2,000 ~ 3,999 | 🐕 진돗개 | "충직하고 멋짐." |
| 6 | 4,000 ~ 6,999 | 🐬 돌고래 | "지능 + 사회성." |
| 7 | 7,000 ~ 9,999 | 🐘 코끼리 | "기억하고 슬퍼할 줄 안다." |
| 8 | 10,000+ | 🧑 인간(다시) | "한 번 더 인간으로." |
| 보너스 | 20,000+ | ✨ 미정 | "?" |

원칙:
- 0단계가 무생물이라 진입 장벽이 낮음 — 처음부터 부담 없이 시작.
- 거꾸로 진화도 가능하게 할지(악행 차감)는 후속 결정.
- 종 일러스트는 1차로 이모지, 2차로 단색 SVG 일러스트.

## 7. 데이터 모델 스케치

```
User {
  id, displayName, toneMode: 'soft' | 'casual', dailyCapEnabled: bool
}

Deed {
  id, userId,
  createdAt,
  photoUrl,
  memo: string?,
  score: int,        // 0..10
  comment: string,   // AI 한줄평
  tags: string[],
  modelVersion: string
}

VirtueSnapshot {
  userId, total: int, monthTotal: int, todayTotal: int,
  speciesStage: int, speciesProgress: float
}

SpeciesDef {
  stage, name, emoji, minVirtue, maxVirtue, blurb
}
```

- 합계는 매 Deed 적재 시 derive (단순 합). 별도 캐시 테이블은 후순위.
- 사진은 외부 스토리지(Supabase Storage / Cloudflare R2), 메타만 DB.

## 8. MVP 범위

**Cut**:
- 친구/공유, 도전 과제, 푸시 알림, 캘린더 위젯, 다국어.

**In**:
- 5 메뉴 중 `덕력` / `덕 쌓기` / `덕행록`만. `환생도감`은 인라인으로 메인에 표시. `나`는 톤 + export만.
- 사진 1장 + 메모 + AI 채점 + 저장.
- 누적 덕력 + 환생종 진행도 표시.
- 로컬 우선 (단일 사용자, 인증 생략 또는 비밀번호 1개).

## 9. 구현 플랜

1. **레포 결정** (사용자 확인 필요) — 신규 `virtue-rebirth-app` 권장. `dev/pt` 위 모바일 라우트는 purplemux와 도메인이 너무 다름.
2. **스캐폴드** — `pnpm create next-app`, Next.js 16 + App Router + Tailwind 4 + shadcn/ui base-nova. components.json은 `dev/pt`와 동일 설정 사용.
3. **레이아웃** — `app/(tabs)/layout.tsx`에서 하단 5 탭 고정. `vaul` Drawer로 사진 업로드 모달.
4. **AI 호출** — `app/api/score/route.ts`에서 Claude Sonnet 4.6 vision API. 시스템 프롬프트에 §5 톤 가이드 그대로 박는다. 결과 JSON 강제 (zod 스키마).
5. **저장** — Supabase (Storage + Postgres) 또는 로컬 SQLite + Tailscale.
6. **환생종 진행** — `SpeciesDef` 테이블/상수 + 누적 합계 기반 단계 산출.
7. **배포** — Vercel 또는 oracle 인스턴스 (`infinity.oracle.shdkej.com` 옆에 `virtue.oracle.shdkej.com`).

## 10. Open Questions

- 구현 레포 위치 (신규 vs `dev/pt` 내 모바일 라우트)?
- AI 호출은 클라이언트 직접 (API 키 노출) vs 자체 backend? 개인용이면 Tailscale 뒤 단순 Node로 충분.
- 악행/차감 메커닉을 넣을지?
- 종 일러스트를 직접 그릴지, 이모지로 시작할지?
- 친구 공유 기능 우선순위 (MVP 후 단계)?

## 11. 디자인 시스템 적용 노트

발견 사항 (lightweight scan):

- `/home/ubuntu/dev/pt` (purplemux) — Next.js 16 + React 19 + shadcn/ui (style **base-nova**, baseColor neutral) + Tailwind 4 + Pretendard 한국어 폰트 + lucide-react + base-ui + zustand + zod + sonner + vaul + dayjs. 색상 토큰은 OKLCH 기반으로 `--ui-blue/teal/coral/amber/purple/pink/green/gray/red` 9채널 정의, `--brand: var(--ui-purple)`, `--positive: var(--ui-teal)`, `--negative: var(--ui-red)`.
- `/home/ubuntu/workspace/space/apps/infinity-kanban` — 정적 nginx + GitHub raw fetch 패턴. 디자인 시스템 없음.
- `dev/knowledge-lab`, `dev/team-ax-holdings` — 콘텐츠/문서 중심, UI 코드 없음.

적용 권고:

- **컴포넌트 출처**: shadcn/ui base-nova를 동일하게 초기화. `Button`, `Card`, `Sheet`(상세), `Drawer`(촬영 모달, vaul), `Tabs`(하단 네비), `Progress`(진행 바), `Skeleton`(채점 로딩), `Sonner`(피드백 토스트).
- **타이포**: Pretendard 그대로. `dev/pt/src/styles/pretendard.css` 동일 import.
- **컬러**: `--brand: var(--ui-purple)`를 메인 CTA에. 환생종 진행 바는 `--ui-teal`. 점수 강조는 `--ui-amber`(따뜻한 톤). 다크 모드는 next-themes로 토글.
- **아이콘**: lucide-react (purplemux와 동일).
- **레이아웃**: 모바일 폭 우선 (`max-w-md mx-auto`). 하단 탭은 `position: sticky bottom-0` + `pb-[env(safe-area-inset-bottom)]`.
- **모션**: tw-animate-css의 fade-in / slide-up을 점수 카드에. 과도한 confetti는 지양.
- **빌드/배포**: pnpm + tsx, oracle 인스턴스 nginx ingress (purplemux/infinity-kanban 패턴 차용).
