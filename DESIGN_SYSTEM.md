# Sam Samuel Design System

> 참조: BRAND.md
> "생산자를 만든다" - 모든 사용자가 생산자가 된다

이 디자인 시스템은 Sam Samuel 브랜드의 **범용 기반**입니다. 각 앱은 이 시스템을 계승하되, 아래에서 "유연" 표시된 항목은 앱/프로젝트 특성에 맞게 재해석할 수 있습니다.

---

## 자유도 프레임워크

모든 항목은 두 단계로 나뉜다. **고정**은 반드시 지킨다. **유연**은 브랜드 정신 안에서 자유롭게 해석한다.

| 구분 | 고정 (DNA) | 유연 (해석 가능) |
|------|-----------|-----------------|
| **철학** | 설계 원칙 4가지 | - |
| **텍스처** | Warm Tool 정신 (촉감, 따뜻함) | 구현 방식 (그림자 레이어 수, 구체 수치) |
| **컬러** | semantic 토큰 구조, **무채색 기본 팔레트** | 테마 적용 시 톤 변경 가능 |
| **타이포** | 4단계 스케일 구조, 한글 지원, **Pretendard** | 굵기 구성, 구체 사이즈 |
| **간격** | 일관된 그리드 시스템 사용 | 기본 단위(4px/8px), 단계 수 |
| **곡률** | 용도별 구분 (sm/md/lg/full) | 구체 px 값 |
| **컴포넌트** | 8종 목록, 접근성 규칙 | variant 수, 사이즈, 시각적 스타일, API 형태 |
| **마이크로카피** | 톤 원칙 (동반자, 행동유도, 간결) | 구체 문구 |
| **접근성** | WCAG AA, 키보드, 시맨틱 마크업 | - (전부 고정) |

**외부 도구(ui-ux-pro-max 등)가 추천하는 스타일이 있을 때:**
1. "고정" 항목과 충돌하면 → 고정을 따른다
2. "유연" 항목이면 → 외부 추천을 적극 수용한다
3. 판단이 애매하면 → 사용자에게 묻는다

---

## 설계 원칙 (고정)

1. **선택지 최소화** — 고민을 줄인다
2. **의미 중심** — "이 색은 언제 쓰는가"가 드러나야 한다
3. **UI는 배경으로** — 사용자의 콘텐츠가 주인공
4. **컨셉이 레이아웃을 이긴다** — 제품의 본질을 가장 잘 전달하는 UI가 최선이다
5. **자연에서 가져온다** — 인공적이고 기계적인 느낌을 경계한다. 곡선, 색감, 여백 모두 자연이 기준이다

### 혁신적 UI 허용 원칙

디자인 시스템은 **제약이 아니라 도구**다.

**깰 수 있는 것:** 그리드 배치, 섹션 순서, 네비게이션 위치, 화면 전환 패턴

**반드시 지키는 것:** semantic 토큰 구조, 접근성 규칙

### 절대 하지 않는 것

- Atomic Design 풀세트
- blue-100 ~ blue-900 팔레트 중심 토큰
- ghost, outline, subtle, link 등 과잉 변형
- UX 패턴 대백과

---

## 브랜드 텍스처: Warm Tool (고정=정신, 유연=구현)

> 참조: Braun(도구의 촉감), 교보문고(따뜻한 공간감), 츠타야(큐레이션된 경험)

Sam Samuel의 시각적 서명은 **"따뜻한 도구"**다. 미니멀하지만 밋밋하지 않고, 모든 요소가 물리적 촉감을 가진다. "빨리 끝내고 나가는 도구"가 아니라 **"머물며 만드는 공간"**이어야 한다.

### 핵심 원칙 (고정)

1. 그림자에 순수 검정 금지 — 따뜻한 톤으로 자연광 아래의 그림자처럼
2. 버튼은 "누를 수 있는" 물리적 피드백을 가진다
3. 입력 필드는 "오목한" 리세스 느낌을 가진다
4. 표면은 깨끗하되 그림자로 깊이감을 만든다
5. 다크모드에서도 완전 검정 금지 — 따뜻한 차콜 기반
6. 단색 배경 금지 — 미세한 warm 그라데이션으로 자연스러운 톤 변화를 준다

### 표현 방식 (유연)

아래는 **레퍼런스 구현**이다. 프로젝트 특성이나 외부 스타일 추천에 따라 변형 가능하다.

- **그림자**: 다층(2~3 layer) warm shadow 권장. 레이어 수, blur/offset 값은 자유
- **표면 처리**: gradient, inner shadow, flat 등 Warm Tool 정신이 느껴지는 방식이면 OK
- **인터랙션**: hover→떠오름, active→눌림의 촉감. 구체 구현(transform, shadow, opacity 등)은 자유

#### 배경 그래디언트 (기본 레퍼런스)

surface 토큰 3종을 조합한 그래디언트. 히어로, 랜딩 페이지 등에 기본 배경으로 사용한다. 토큰 값에 따라 자동으로 톤이 결정된다.

```css
--gradient-warm-surface: linear-gradient(
  180deg,
  var(--color-surface) 0%,
  var(--color-bg) 50%,
  var(--color-surface-hover) 100%
);
```

### 상태 변형 원칙 (고정=패턴, 유연=구현)

모든 인터랙티브 컴포넌트는 4가지 상태를 가진다: `default` / `hover` / `active` / `disabled`

| 상태 | 느낌 | 구현은 자유 |
|------|------|------------|
| default | 안정된 표면 | gradient, flat, shadow 등 |
| hover | 떠오르는 느낌 | shadow 확대, 밝기 변화, scale 등 |
| active | 눌리는 느낌 | inner shadow, scale down, 어두워짐 등 |
| disabled | 비활성 | opacity 낮춤 (0.3~0.5 범위) |

- Form(Input/Select) 추가 상태: `focus` (집중 강조), `error` (위험 강조)
- focus glow는 warm 톤 권장 — 차가운 파란색 기본값 지양

---

## 1. 컬러 토큰 (고정=구조, 유연=값)

### 토큰 구조 (고정)

semantic 토큰만 사용한다. 아래 토큰 이름과 역할은 고정이다.

| 토큰 | 역할 |
|------|------|
| `--color-bg` | 페이지 배경 |
| `--color-surface` | 카드/컴포넌트 배경 |
| `--color-surface-hover` | 호버 시 표면 |
| `--color-text-primary` | 주요 텍스트 |
| `--color-text-secondary` | 보조 텍스트 |
| `--color-text-muted` | 비활성 텍스트 |
| `--color-primary` | 주요 액션 (앱별 오버라이드) |
| `--color-danger` | 파괴적 액션/에러 |
| `--color-success` | 성공/완료 |
| `--color-warning` | 주의/대기 |
| `--color-border` | 경계선 |
| `--color-border-focus` | 포커스 경계선 |
| `--color-overlay` | 오버레이 배경 |

### 컬러 기조 (고정)

- **기본 모드는 라이트모드** — 밝고 따뜻한 첫인상이 브랜드의 출발점이다
- **기본은 무채색** — 테마가 없을 때 뉴트럴 그레이 기반. 어떤 콘텐츠든 방해하지 않는다
- **저채도** — 고채도 네온 금지. 자연에서 발견되는 색 (따뜻한 베이지, 크림, 올리브 등)
- **단색 금지** — 배경, 카드 등 넓은 면적에 순수 단색을 쓰지 않는다. 미세한 warm 그라데이션으로 자연스러운 톤 변화를 준다
- **라이트모드**: 밝은 그레이/화이트 기반. 순수 `#FFFFFF` 지양
- **다크모드**: 차콜 기반. 순수 `#000000` 금지
- **테마 적용 시**: 외부 스타일 추천(ui-ux-pro-max 등)에 따라 warm/cool/craft 등 톤 변경 가능. 단, 배경은 극단적 색상(핑크, 블루 등) 지양하고 뉴트럴 범위 내에서 조정

### 기본 팔레트 (고정 — 테마 미적용 시 기본값)

테마가 지정되지 않았을 때 사용하는 기본 팔레트다.

```css
/* 라이트 모드 기본값 */
:root {
  --color-bg: #f5f5f5;
  --color-surface: #eeeeee;
  --color-surface-hover: #e0e0e0;
  --color-text-primary: #1a1a1a;
  --color-text-secondary: #6b6b6b;
  --color-text-muted: #9a9a9a;
  --color-primary: #1a1a1a;
  --color-danger: #c44536;
  --color-success: #2d5a27;
  --color-warning: #d4a026;
  --color-border: rgba(0, 0, 0, 0.08);
  --color-border-focus: rgba(0, 0, 0, 0.2);
  --color-overlay: rgba(0, 0, 0, 0.4);
}

/* 다크 모드 기본값 */
[data-theme="dark"] {
  --color-bg: #1a1a1a;
  --color-surface: #2a2a2a;
  --color-surface-hover: #333333;
  --color-text-primary: #e5e5e5;
  --color-text-secondary: #a0a0a0;
  --color-text-muted: #6b6b6b;
  --color-primary: #e5e5e5;
  --color-danger: #e05545;
  --color-success: #4a9e42;
  --color-warning: #e8b84a;
  --color-border: rgba(255, 255, 255, 0.08);
  --color-border-focus: rgba(255, 255, 255, 0.2);
  --color-overlay: rgba(0, 0, 0, 0.6);
}
```

### 앱별 오버라이드

각 앱은 `--color-primary` 계열을 재정의할 수 있다. 키 컬러 선택 기준: 중-저채도, 자연색, 화면의 10% 이내.

---

## 2. 타이포그래피 (고정=폰트/구조, 유연=사이즈)

### 폰트 (고정)

Pretendard 단일 폰트. 브랜드 일관성을 위해 변경하지 않는다.

```
font-family: 'Pretendard Variable', 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif
```

> **Pencil 호환성 노트**: Pencil(.pen) 에디터에서 Pretendard를 지원하지 않으므로 Inter로 대체하여 작업한다. 코드 구현 시에는 반드시 Pretendard를 사용할 것.

### 스케일 구조 (고정)

4단계 스케일을 사용한다. 단계를 늘리지 않는다.

| 토큰 | 역할 | 굵기 기조 |
|------|------|----------|
| heading-lg | 페이지 타이틀 | Bold (700) |
| heading-md | 섹션 제목 | Semi-bold (600) |
| body | 본문 | Regular (400) |
| caption | 보조 텍스트 | Regular (400) |

### 사용 규칙 (고정)

- heading-lg: 페이지당 최대 1개
- caption: 단독으로 주요 정보 전달 금지
- `font-display: swap` 필수
- 굵기는 400, 600, 700만 사용

### 사이즈 레퍼런스 (유연)

```
heading-lg: 28~36px, line-height 1.2
heading-md: 20~24px, line-height 1.3
body:       16px, line-height 1.6
caption:    13~14px, line-height 1.4
```

---

## 3. 간격 & 곡률 (고정=체계, 유연=값)

### 간격

일관된 그리드 시스템을 사용한다. 임의 값 금지.

| 토큰 | 레퍼런스 값 | 용도 |
|------|------------|------|
| xs | 4px | 아이콘-텍스트 사이 |
| sm | 8px | 관련 요소 간 |
| md | 16px | 카드 내부 패딩 |
| lg | 24px | 그룹 간 간격 |
| xl | 32px | 섹션 간 구분 |
| 2xl | 48px | 페이지 상하단 여백 |

기본 단위(4px/8px)와 단계 수는 프로젝트에 따라 조정 가능하나, 반드시 토큰으로 관리한다.

자연의 여백 원칙: 콘텐츠 사이에 숨 쉴 수 있는 넉넉한 간격을 유지하고, 밀집 영역과 트인 영역이 교차하는 리듬을 만든다. 모든 간격이 균일한 기계적 배치를 피한다.

### 곡률 (Border Radius)

| 토큰 | 레퍼런스 값 | 용도 |
|------|------------|------|
| radius-sm | 6px | 버튼, 입력, 뱃지 |
| radius-md | 10px | 카드, 드롭다운 |
| radius-lg | 16px | 모달, 바텀시트 |
| radius-full | 9999px | 아바타, 태그 |

구체 값은 스타일에 따라 조정 가능하나, 자연의 곡률 원칙을 따른다:

| O (이렇게)                            | X (이렇게 안 함)                      |
|---------------------------------------|---------------------------------------|
| 모서리에 부드러운 라운딩               | 직각 모서리                            |
| 카드마다 미세하게 다른 곡률 허용        | 모든 요소에 동일한 border-radius 강제  |
| 유기적인 둥근 형태                     | 완벽한 정원, 정사각형                   |
| 구분선 대신 여백과 곡면으로 영역 분리   | 직선 구분선(hr)으로 영역 자르기         |

---

## 4. 핵심 컴포넌트 (고정=목록/행동, 유연=시각 표현)

8종을 기본으로 한다. 새 UI는 이 컴포넌트로 먼저 시도한다.

### 컴포넌트 목록 (고정)

| 컴포넌트 | 역할 | 필수 variant |
|----------|------|-------------|
| **Button** | 액션 트리거 | primary, secondary, danger |
| **Input** | 텍스트 입력 | default, textarea |
| **Select** | 옵션 선택 | - |
| **Modal** | 오버레이 대화상자 | dialog, sheet |
| **Toast** | 비차단 알림 | default, success, error |
| **Badge** | 상태/라벨 표시 | default, success, warning |
| **InputGroup** | Label + Input 조합 | - |
| **Card** | Header + Content + Footer 컨테이너 | - |

### 행동 규칙 (고정)

- Button: `<button>` 태그 필수. loading 시 너비 고정. 즉시 시각적 피드백
- Input: `<label>` 연결 필수. placeholder는 label 대체 금지
- Select: 키보드 탐색(화살표, Enter, Escape) 필수
- Modal: 포커스 트랩, ESC 닫기, `role="dialog"` + `aria-modal="true"`
- Toast: 하단 중앙, 3~5초 표시, 최대 동시 3개
- Badge: 짧은 텍스트(최대 2단어), 색상+텍스트로 의미 전달

### 시각 표현 (유연)

variant 수, 사이즈 옵션, Compound/Flat API 선택, 시각 스타일(그림자 강도, border 유무, gradient 여부 등)은 프로젝트와 스타일 추천에 따라 자유롭게 결정한다.

### 레퍼런스 구현: Editorial Style (메인)

아래는 공식 레퍼런스 스타일이다. 새 프로젝트는 이 스타일을 기본으로 사용한다.
쇼케이스: `sam-samuel-design-system.pen`
- 디자인 시스템: "Main — Dark Mode" / "Main — Light Mode"
- 대시보드 예제 (Desktop): "Dashboard — Dark Mode" / "Dashboard — Light Mode" (1440×900)
- 대시보드 예제 (Mobile): "Dashboard Mobile — Dark Mode" / "Dashboard Mobile — Light Mode" (402×auto)

#### 컴포넌트별 다크/라이트 패턴

**Button**

| variant | Light Mode | Dark Mode |
|---------|-----------|-----------|
| primary | bg=#1a1a1a, text=#ffffff | bg=#e5e5e5, text=#1a1a1a |
| secondary | bg=transparent, border=#d0d0d0, text=#1a1a1a | bg=transparent, border=#4a4a4a, text=#e5e5e5 |
| danger | bg=#c44536, text=#ffffff | bg=#c44536, text=#ffffff |

**Badge — 틴트 배경 접근법**

semantic 컬러의 저채도 틴트를 배경으로 사용한다.

| variant | Light Mode (bg / text) | Dark Mode (bg / text) |
|---------|----------------------|---------------------|
| default | #eeeeee / #1a1a1a | #333333 / #e5e5e5 |
| success | #e8f5e6 / #2d5a27 | #1a3a18 / #4a9e42 |
| warning | #fef3cd / #8a6d14 | #3d3015 / #e8b84a |
| error | #fde8e6 / #c44536 | #3a1a18 / #e05545 |

**Input / Select**

| 속성 | Light Mode | Dark Mode |
|------|-----------|-----------|
| 필드 bg | #ffffff | #0f0f0f |
| border | #e0e0e0 | #333333 |
| placeholder | #d0d0d0 | #4a4a4a |
| label | #6b6b6b (600) | #9a9a9a (600) |

**Card**

| 속성 | Light Mode | Dark Mode |
|------|-----------|-----------|
| bg | #ffffff | #0f0f0f |
| border | #e8e8e8 | #2a2a2a |
| divider | #eeeeee | #2a2a2a |
| action text | #6b6b6b | #9a9a9a |

**Toast — 도트 인디케이터 + 틴트 배경**

| variant | Light Mode | Dark Mode |
|---------|-----------|-----------|
| default | bg=#eeeeee, dot=#9a9a9a, text=#1a1a1a | bg=#2a2a2a, dot=#6b6b6b, text=#e5e5e5 |
| success | bg=#e8f5e6, border=#2d5a27, text=#2d5a27 | bg=#1a2e18, border=#2d5a27, text=#4a9e42 |
| error | bg=#fde8e6, border=#c44536, text=#c44536 | bg=#2e1a18, border=#c44536, text=#e05545 |

**Modal**

| 속성 | Light Mode | Dark Mode |
|------|-----------|-----------|
| overlay | #e0e0e0 | #0a0a0a |
| dialog bg | #ffffff | #1f1f1f |
| dialog border | #e8e8e8 | #333333 |

#### 섹션 레이아웃 패턴

- 대형 섹션 넘버 (01~05): 라이트=#e8e8e8, 다크=#252525 — 배경에 녹아드는 워터마크 역할
- 섹션 bg 교차: 라이트=#ffffff↔#f5f5f5, 다크=#181818↔#141414
- 컴포넌트 카드: 라이트=#f5f5f5, 다크=#1a1a1a + border=#2a2a2a

---

## 5. 마이크로카피 톤 가이드 (고정=원칙, 유연=구체 문구)

### 톤 원칙 (고정)

| 원칙 | 설명 |
|------|------|
| 동반자 톤 | 선생님이 아니라 조금 더 아는 옆자리 선배. 존댓말 부드러운 체 ("~해보세요", "~돼요") |
| 행동 유도 | 상태 설명이 아니라 다음 행동 안내 |
| 간결함 | 한 문장이면 충분 |

### 패턴 (고정)

- 버튼: 행동을 구체적으로 ("확인" → "저장하기")
- 에러: 사용자 탓 하지 않기 ("잘못된" → "확인해주세요")
- 빈 상태: 끝이 아니라 시작 (다음 행동 제안 필수)
- "~되었습니다"(수동) 대신 "~했어요"(능동)

---

## 6. 접근성 규칙 (전부 고정)

선택이 아니라 강제. "모든 사용자가 생산자가 된다"에서 "모든"이 진짜 모든이려면.

- 명암비: 일반 텍스트 7:1 이상 목표 (WCAG AAA)
- 컬러 독립성: 컬러만으로 의미 전달 금지. 추가 시각적 단서 제공
- 키보드: 모든 인터랙티브 요소 Tab 도달 가능, 포커스 인디케이터 명확하게
- 스크린리더 호환
- `prefers-reduced-motion` 대응 필수
- 시맨틱 마크업: Button→`<button>`, Input→`<label>` 연결, Modal→`role="dialog"` + 포커스 트랩, Toast→`role="status"`/`role="alert"`

---

## 7. 사용 규칙

| 규칙 | 강제 방법 |
|------|----------|
| semantic 토큰 외 하드코딩 컬러 금지 | lint |
| spacing 토큰 외 임의 margin 금지 | lint |
| 새 UI는 기존 8종 컴포넌트로 먼저 시도 | PR 리뷰 |
| 새 컴포넌트 추가 시 사유 명시 | PR 리뷰 |

---

## 8. 대시보드 레이아웃 패턴 (유연)

대시보드 구축 시 참고하는 레이아웃 패턴이다. 디자인 토큰 기반으로 다크/라이트 테마 자동 전환을 지원한다.

### Desktop (1440×900)

사이드바 + 메인 콘텐츠 구조.

```
┌──────────┬────────────────────────────────┐
│ Sidebar  │  Header (검색, 알림, 프로필)    │
│  260px   ├────────────────────────────────┤
│  Logo    │  Section Header + Period Badge  │
│  Nav     │  ┌──────┐┌──────┐┌──────┐┌──┐ │
│  Items   │  │ KPI  ││ KPI  ││ KPI  ││KPI│ │
│          │  └──────┘└──────┘└──────┘└──┘ │
│          │  ┌─────────────┐┌───────────┐  │
│          │  │ Chart Card  ││ Activity   │  │
│          │  │ (bar chart) ││ List       │  │
│          │  └─────────────┘└───────────┘  │
└──────────┴────────────────────────────────┘
```

- 사이드바: 고정 260px, 로고 + 네비게이션
- 메인: fill_container, 헤더(72px) + 콘텐츠(padding 32px)
- 하단: 차트(fill) + 활동 리스트(360px) 가로 배치

### Mobile (402×auto)

사이드바 제거 → 하단 플로팅 탭바 전환.

```
┌──────────────────────┐
│  Header (인사+타이틀)  │
├──────────────────────┤
│  ┌────────┐┌────────┐│
│  │ KPI 1  ││ KPI 2  ││
│  └────────┘└────────┘│
│  ┌────────┐┌────────┐│
│  │ KPI 3  ││ KPI 4  ││
│  └────────┘└────────┘│
│  ┌──────────────────┐│
│  │   Chart Card     ││
│  └──────────────────┘│
│  ┌──────────────────┐│
│  │  Activity List   ││
│  └──────────────────┘│
│  ░░ gradient fade ░░ │
│  ╭──────────────────╮│
│  │ 🏠  🔍  📅  👤  ││
│  ╰──────────────────╯│
└──────────────────────┘
```

- 메트릭 카드: 2×2 그리드 (gap 12px)
- 차트/활동: 세로 스택
- 탭바: 플로팅 필(pill) + 상단 그라디언트 페이드
- 탭바 그라디언트: 테마별 대응 필요 (다크=#1C1B19, 라이트=#F0EEE9)

---

## 벤치마크

| 브랜드 | 참고 포인트 |
|--------|------------|
| Braun | 잘 만들어진 도구의 촉감, 정제된 미니멀리즘 |
| 교보문고 | 따뜻한 공간감, 머물고 싶어지는 서재의 분위기 |
| 츠타야 | 큐레이션된 경험, 맥락을 보여주는 배치 |
| Notion | 빈 상태 설계, 콘텐츠 중심 UI |
| Linear | 마이크로 인터랙션 품질, 속도감 |
| Muji | 브랜드 철학의 일관된 시각적 침투, 소재감 |

핵심: **"빠진 것"으로 브랜딩**한다. 넣은 것이 아니라 뺀 것이 디자인이다. 그리고 남은 것은 자연처럼 따뜻해야 한다.
