# Sam Samuel Design System

이 문서는 Sam Samuel 제품을 **어떻게 만드는가**를 정의한다. 브랜드의 왜는 [BRAND.md](./BRAND.md), 화면이 맞게 느껴지는지에 대한 판단은 [DESIGN.md](./DESIGN.md)를 따른다.

## 사용 원칙

- 이 문서는 범용 기반이다. 각 앱은 계승하되, **유연** 항목은 제품 맥락에 맞게 재해석할 수 있다.
- **고정** 항목은 반드시 지킨다.
- 외부 스타일 제안이 고정 항목과 충돌하면 이 문서를 우선한다.
- 디자인 작업 전에는 `BRAND.md`, `DESIGN.md`, 이 문서를 실제로 열어 확인한다.

## 디자인 정의

Sam Samuel의 제품 디자인은 **Calm Technology 기반의 Warm Minimalism**이다.

```text
Calm Technology x Warm Minimalism x Human-Centered x Reflective x Cyclical UX
```

- **Calm Technology**: 필요한 순간에만 정보를 전면에 보여준다.
- **Warm Minimalism**: 웜 뉴트럴, 부드러운 곡선, 촉각적 표면, 자연광 같은 깊이로 차갑지 않은 명료함을 만든다.
- **Human-Centered**: AI와 자동화는 사용자의 판단을 대체하지 않는다.
- **Reflective Design**: 사용자가 자기 상태와 패턴을 돌아볼 수 있게 한다.
- **Cyclical UX**: 다시 이어갈 가치가 있는 흐름에서 다음 재진입점을 남긴다.

판단 우선순위:

1. 사용자의 주의와 주도권을 지키는가?
2. 지금 필요한 정보만 남겼는가?
3. 사용자가 자기 상태를 이해할 수 있는가?
4. 다음 행동과 재진입점이 남아 있는가?
5. 위 원칙을 해치지 않는 범위에서 따뜻한 촉감과 개성을 더했는가?

`Zen Design`, `Neumorphism`, `Glassmorphism`, `Soft UI`는 정체성 이름이 아니다. 필요할 때 일부 표현 기법으로만 쓴다.

## 자유도 프레임워크

| 영역 | 고정 | 유연 |
| --- | --- | --- |
| 철학 | Calm Technology 기반 Warm Minimalism | 없음 |
| 텍스처 | Warm Tool 정신 | 그림자, 표면 처리, 세부 수치 |
| 컬러 | semantic 토큰, warm neutral 기본 | 앱별 primary 색 |
| 타이포 | Pretendard, 4단계 스케일 | 구체 사이즈 |
| 간격 | 토큰 기반 그리드 | 값과 단계 수 |
| 곡률 | 용도별 radius 토큰 | 구체 px |
| 컴포넌트 | 핵심 8종, 접근성 | variant, API, 시각 표현 |
| 제품 패턴 | 역할, 접근성, 승격 기준 | 조합, 밀도, 배치 |
| 마이크로카피 | 동반자, 행동 유도, 간결 | 실제 문구 |
| 접근성 | WCAG AAA 목표, 키보드, 시맨틱 | 없음 |

## 설계 원칙

1. **선택지 최소화**: 고민을 줄인다.
2. **의미 중심**: 색과 형태의 역할이 드러나야 한다.
3. **UI는 배경**: 사용자의 콘텐츠가 주인공이다.
4. **컨셉이 레이아웃을 이긴다**: 제품 본질을 가장 잘 전달하는 UI가 최선이다.
5. **자연에서 가져온다**: 곡선, 색감, 여백 모두 자연을 기준으로 한다.

그리드, 섹션 순서, 네비게이션 위치, 화면 전환은 필요하면 깰 수 있다. semantic 토큰 구조와 접근성 규칙은 깨지 않는다.

## UX 실행 규칙

### 정제된 화면 구성

- 한 화면에서 요구하는 주요 행동은 하나다.
- 첫 진입 기준 입력 필드는 1~3개를 기본으로 한다.
- 상세 정보는 접고, 먼저 `상태 / 다음 행동`만 보여준다.
- 홈은 모든 정보를 모은 대시보드가 아니라 현재 상태판이다.

### 사용자 주권

- 사용자가 선택, 수정, 거절, 되돌리기를 할 수 있어야 한다.
- AI 결과는 판정문이 아니라 검토 가능한 관점, 요약, 제안으로 표현한다.
- 자동 제안에는 수정·거부 경로를 둔다.

### 시각적 위계

가장 중요한 원칙이다. 위계가 무너지면 다른 디테일은 보지 않는다.

- 5초 안에 가장 중요한 메시지가 보여야 한다.
- 한 화면의 주인공은 하나다.
- 모든 요소를 같은 무게로 배치하지 않는다.
- 크기, 굵기, 대비, 여백, 위치, 그룹핑, 깊이, 움직임을 조합해 보는 순서를 설계한다.
- 설계 순서: 컨셉 -> 설계 -> 구도 -> 배치 -> 색감.
- 여백은 장식이 아니라 관계를 표현하는 구조다.

### 점진적 완성

- 핵심 뼈대부터 만들고 피드백으로 정제한다.
- 빠르게 시도하고 안 되는 방법을 제거한다.
- 처음부터 캘린더 연동, 상세 통계, 긴 히스토리, 소셜 공유, streak, 수십 개 태그를 넣지 않는다.

### 복잡성의 환원

- 내부 로직이 복잡해도 사용자에게는 직관적으로 마무리된 경험을 준다.
- 깊은 이해는 복잡함이 아니라 명료함으로 드러난다.

## 순환 UX 패턴

기본 검토 루프:

```text
Capture -> Reflect -> Rebalance -> Next -> Return
남기기 -> 돌아보기 -> 균형 -> 다음 손잡이 -> 이어서 시작
```

이 루프는 모든 제품에 강제하지 않는다.

- `Capture`: 최소 입력을 우선한다.
- `Reflect`: 원본보다 짧은 패턴과 관찰을 먼저 제안한다.
- `Rebalance`: 실제 비교할 두 축이 있을 때만 쓴다.
- `Next`: 이어갈 가치가 있는 흐름에서 다음 행동을 남긴다.
- `Return`: 재방문이 유용한 제품에서만 직전 시작점을 우선 노출한다.

컴포넌트 후보:

- `One Primary Button`: 화면의 메인 버튼은 하나.
- `Progressive Disclosure`: 원본, 히스토리, 설정은 필요할 때 연다.
- `Small Input`: 입력 영역은 넉넉하게, 필드는 적게.
- `Balance Bar`: 2축 쌍만. 3개 이상은 보조 상태 칩으로 분리.
- `Tilt Indicator`: 점수보다 기울기를 말한다.
- `Pair Cards`: 관계를 쌍으로 보여준다.
- `Loop Ring`: 루프의 현재 위치를 보여준다.
- `Next Handle`: 세션 끝에 남기는 다음 행동 한 줄.
- `Resume Card`: 재진입이 핵심인 제품에서만 쓴다.

## Warm Tool

Sam Samuel의 시각적 서명은 **따뜻한 도구**다.

고정 원칙:

- 그림자에 순수 검정을 쓰지 않는다.
- 버튼은 누를 수 있는 물리적 피드백을 가진다.
- 입력 필드는 오목한 리세스 느낌을 가질 수 있다.
- 표면은 깨끗하되 그림자로 깊이를 만든다.
- 다크모드도 순수 검정이 아닌 따뜻한 차콜이다.
- 넓은 배경에는 미세한 명도 변화를 준다.

기본 배경 그래디언트:

```css
--gradient-surface: linear-gradient(
  180deg,
  var(--color-surface) 0%,
  var(--color-bg) 50%,
  var(--color-surface-hover) 100%
);
```

## 시그니처 훅

모든 앱은 기억에 남는 3D/모션 모먼트 하나를 가질 수 있다. 단, 훅은 하나만 둔다.

고정 원칙:

- 한 화면의 임팩트 모먼트는 1개.
- 기반 색, 레이아웃, 가독성을 훅이 흔들지 않는다.
- 깊이는 과한 베벨이나 네온이 아니라 빛, 반사, 시차로 만든다.
- `prefers-reduced-motion`을 존중한다.
- 콘텐츠 가독성이 항상 우선이다.

앱별 예:

- 데이터/대시보드: 3D 카드 틸트, 스튜디오 조명 반사
- 히어로/랜딩: 거대 타이포 시차, 스크롤 reveal
- 제품/갤러리: 부유 패널, 호버 스포트라이트
- 도구/유틸: 스프링, 자석 스냅 같은 물리감 있는 micro motion

## WebGL / 3D

진짜 입체 상호작용이 제품 가치라면 Three.js로 구현한다. 다만 stage 감각만 필요하거나 성능·접근성·일정상 full 3D가 과하면 video, image sequence, CSS parallax, static image fallback을 쓸 수 있다. fallback은 핵심 데이터를 숨기는 장식 루프가 아니라 같은 공간 감각을 더 가볍게 전달하는 대체 경로여야 한다.

원칙:

- 단일 HTML 실험은 importmap으로 three ESM을 CDN 로드할 수 있다.
- 3D 색은 CSS 변수에서 읽는다.
- 장식용 3D보다 제품 데이터를 입체로 옮긴다.
- 모션 문법은 진입 -> 유휴 -> 조작 -> 물러남.
- 모바일 캔버스는 `touch-action: pan-y`를 유지한다.
- WebGL 실패 시 레이아웃은 유지하고 fallback을 보여준다.
- 라이트/다크 x 데스크탑/모바일 4조합 스크린샷으로 검증한다.

## 상태 변형

모든 인터랙티브 컴포넌트는 기본 상태를 가진다.

| 상태 | 느낌 |
| --- | --- |
| default | 안정된 표면 |
| hover | 떠오르는 느낌 |
| active | 눌리는 느낌 |
| disabled | 비활성 |

Form 계열은 `focus`, `error`를 추가한다. loading 상태에서는 버튼 너비가 흔들리면 안 된다.

## 컬러 토큰

semantic 토큰만 사용한다.

```css
:root {
  --color-bg: #f0eee9;
  --color-surface: #faf8f4;
  --color-surface-hover: #e7e4dd;
  --color-text-primary: #211f1c;
  --color-text-secondary: #6e6a63;
  --color-text-muted: #9b968d;
  --color-primary: #211f1c;
  --color-danger: #c44536;
  --color-success: #2d5a27;
  --color-warning: #d4a026;
  --color-border: rgba(45, 40, 30, 0.08);
  --color-border-focus: rgba(45, 40, 30, 0.2);
  --color-overlay: rgba(30, 27, 22, 0.4);
}

[data-theme="dark"] {
  --color-bg: #201e1b;
  --color-surface: #2a2724;
  --color-surface-hover: #343029;
  --color-text-primary: #e9e6e0;
  --color-text-secondary: #a39e95;
  --color-text-muted: #6e6a63;
  --color-primary: #e9e6e0;
  --color-danger: #e05545;
  --color-success: #4a9e42;
  --color-warning: #e8b84a;
  --color-border: rgba(255, 250, 240, 0.08);
  --color-border-focus: rgba(255, 250, 240, 0.2);
  --color-overlay: rgba(15, 13, 10, 0.6);
}
```

규칙:

- 기본은 warm neutral, `#F0EEE9` 계열이다.
- 순수 `#FFFFFF`, 순수 `#000000`은 넓은 면적에 쓰지 않는다.
- 주요 액션 색은 앱별 하나만 고른다.
- 키 컬러는 중-저채도 자연색이고 화면의 10% 이내로 쓴다.

## 타이포그래피

Pretendard 단일 폰트를 쓴다.

```css
font-family: 'Pretendard Variable', 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

스케일은 4단계다.

| 토큰 | 역할 | 굵기 |
| --- | --- | --- |
| heading-lg | 페이지 타이틀 | 700 |
| heading-md | 섹션 제목 | 600 |
| body | 본문 | 400 |
| caption | 보조 텍스트 | 400 |

규칙:

- `heading-lg`는 페이지당 최대 1개.
- `caption`만으로 주요 정보를 전달하지 않는다.
- `font-display: swap` 필수.
- 굵기는 400, 600, 700만 사용한다.
- viewport width에 따라 폰트 크기를 스케일하지 않는다.

## 간격과 곡률

간격은 토큰으로 관리한다.

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| xs | 4px | 아이콘-텍스트 사이 |
| sm | 8px | 관련 요소 간 |
| md | 16px | 카드 내부 |
| lg | 24px | 그룹 간 |
| xl | 32px | 섹션 간 |
| 2xl | 48px | 페이지 상하단 |

곡률:

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| radius-sm | 6px | 버튼, 입력, 뱃지 |
| radius-md | 10px | 카드, 드롭다운 |
| radius-lg | 16px | 모달, 바텀시트 |
| radius-full | 9999px | 아바타, 태그 |

카드는 8px 안팎을 기본으로 하되, 기존 제품 시스템이 다르면 그 시스템을 따른다. 과한 라운딩으로 장난감처럼 보이면 실패다.

## 핵심 컴포넌트

새 UI는 먼저 이 8종으로 해결한다.

| 컴포넌트 | 역할 | 필수 variant |
| --- | --- | --- |
| Button | 액션 | primary, secondary, danger |
| Input | 텍스트 입력 | default, textarea |
| Select | 옵션 선택 | default |
| Modal | 오버레이 | dialog, sheet |
| Toast | 비차단 알림 | default, success, error |
| Badge | 상태/라벨 | default, success, warning |
| InputGroup | Label + Input | default |
| Card | Header + Content + Footer | default |

행동 규칙:

- Button은 `<button>`을 사용한다. loading 시 너비를 고정한다.
- Input은 `<label>`과 연결한다. placeholder는 label을 대체하지 않는다.
- Select는 키보드 탐색을 지원한다.
- Modal은 focus trap, ESC 닫기, `role="dialog"`, `aria-modal="true"`를 갖는다.
- Toast는 3~5초 표시, 최대 동시 3개.
- Badge는 짧게 쓰고 색만으로 의미를 전달하지 않는다.

## 제품 패턴

반복되는 화면 조합은 제품 패턴으로 승격한다. 아래 중 2개 이상이면 문서화한다.

- 여러 제품이나 화면에서 반복된다.
- 첫 행동, 저장, 승인, 복귀 같은 전환을 담당한다.
- 빈 상태, 오류, 권한, 로딩처럼 품질을 좌우한다.
- AI/자동화의 판단을 사용자가 이해하거나 거절하는 표면이다.
- 운영자가 매일 쓰는 화면이라 밀도와 동선 일관성이 필요하다.

기본 패턴과 필수 규칙:

- `CharacterStage / FloatingHUD`: 3D/canvas/video/parallax stage 위에 조작층을 얹는다. stage는 장식 배경이 아니라 제품 상태나 성격을 드러내야 하며, 전면 조작층은 대비·포커스·터치 영역을 보장한다.
- `AppShell / Navigation`: PageHeader, Topbar, Sidebar, MobileBottomNav, BackAction. 현재 위치, 대표 액션 1개, 안전한 귀환 경로가 보여야 한다.
- `Status / Ops Surface`: StatusDot, MetricPill, HealthBadge, ActivityFeed, TreeRow. 색만으로 상태를 말하지 말고, 원인이나 다음 행동으로 이어준다.
- `Data & List Interaction`: SearchBox, FilterBar, Tabs, SortableRow, CompactTable, LoadMore. 모바일에서는 핵심 필드 3개 이하를 우선 노출하고, table은 비교·스캔이 핵심일 때만 쓴다.
- `Creation Flow`: FormSection, DraftPanel, PreviewPanel, DiffPreview, InspectorSheet, ConfirmDialog. 공개·외부 반영 작업은 작성 -> 미리보기/차이 확인 -> 영향 범위 확인을 기본으로 한다.
- `State Components`: Empty, Loading, Error, Permission, Offline, DirtyState. 빈 상태는 다음 행동 1개, 로딩은 레이아웃 점프 방지, 에러는 원인·재시도·대체 경로를 제공한다.
- `AI / Result Surface`: ResultCard, ReasonBlock, LimitationNote, Accept/Edit/Retry. 결론·근거·한계를 분리하고, 사용자가 저장·수정·거절·다시 시도할 수 있어야 한다.
- `Content / Card-News`: EditorialCard, CoverCard, StepCard, GalleryViewer, ThreadDraftBlock. 관찰 -> 인사이트 -> 적용 후보가 보존되어야 하며, 긴 문장은 카드나 문단을 나눈다.

운영 화면은 조용하고 밀도 있게 만든다. 랜딩처럼 큰 히어로와 장식 카드로 풀지 않는다.

## 모션

모션은 기다려주는 느낌을 만든다. 불필요한 지연은 금지다.

| 토큰 | 값 | 용도 |
| --- | --- | --- |
| motion-fast | 120~160ms | hover, icon, focus |
| motion-base | 180~240ms | sheet, toast, row expand |
| motion-slow | 280~360ms | page reveal, modal |
| press-scale | 0.97~0.99 | 버튼/카드 눌림 |
| hover-lift | 1~3px | 클릭 가능한 표면 |

`prefers-reduced-motion`에서는 위치 이동과 scale을 줄이고 opacity 또는 instant state로 대체한다.

## 아이콘과 미디어

- 아이콘은 lucide를 기본으로 쓴다.
- familiar symbol이 있는 버튼은 텍스트보다 아이콘을 우선한다.
- 낯선 아이콘은 tooltip 또는 `aria-label`을 제공한다.
- 사진은 실제 맥락을 보여줄 때 쓴다.
- 흐릿한 분위기용 stock-like 이미지는 금지한다.
- 스크린샷은 제품 판단이나 before/after를 보여줄 때 쓴다.
- 빈 상태 이미지는 장식보다 시작 예시가 우선이다.

## 컴포넌트 계약

제품 패턴을 코드로 만들 때 최소 계약을 남긴다.

```ts
type ComponentContract = {
  role: string;
  requiredProps: string[];
  variants: string[];
  states: Array<"default" | "hover" | "active" | "disabled" | "focus" | "error" | "loading">;
  accessibility: string[];
  forbidden: string[];
};
```

각 패턴 또는 구현에는 다음을 포함한다.

- 역할
- 필수 props
- 최소 variant
- 필요한 states
- accessibility
- forbidden
- 실제 화면에 가까운 예시 1개

## 마이크로카피

톤 정본은 `BRAND.md > 톤앤매너`다. UI에서는 다음만 기억한다.

- 선생님이 아니라 옆자리 선배처럼 쓴다.
- 상태 설명이 아니라 다음 행동을 안내한다.
- 한 문장이면 충분한 곳에 두 문장을 쓰지 않는다.
- 버튼은 "확인"보다 "저장하기"처럼 행동을 구체화한다.
- 에러는 사용자 탓으로 말하지 않는다.
- 빈 상태에는 다음 행동 1개를 둔다.

## 접근성

전부 고정이다.

- 일반 텍스트 명암비 7:1 목표.
- 컬러만으로 의미 전달 금지.
- 모든 인터랙티브 요소는 Tab으로 도달 가능해야 한다.
- 포커스 인디케이터는 명확해야 한다.
- 스크린리더 호환은 필수다. 이름, 역할, 상태가 보조기술에 전달되어야 한다.
- `prefers-reduced-motion` 대응 필수.
- Button은 `<button>`, Input은 `<label>` 연결, Modal은 `role="dialog"`와 focus trap, Toast는 `role="status"` 또는 `role="alert"`를 사용한다.

## 대시보드 레이아웃

Desktop 1440x900 기준:

- Sidebar: 260px 고정.
- Main: header 72px + content padding 32px.
- 하단 복합 영역: 주요 차트 fill + 활동 리스트 360px.

Mobile 402px 기준:

- Sidebar는 제거하고 하단 플로팅 탭바로 전환한다.
- Metric card는 2x2 grid, gap 12px.
- 차트와 활동 리스트는 세로 스택.
- 탭바는 floating pill + 상단 fade.

## 검증 체크리스트

완료 전 반드시 확인한다.

- 세 디자인 정본을 실제로 열었는가?
- 첫 화면에서 5초 안에 목적, 주인공, 다음 행동이 보이는가?
- semantic 토큰 외 하드코딩 컬러가 없는가?
- spacing/radius가 토큰 체계를 따르는가?
- 한 화면의 주인공이 하나인가?
- loading/empty/error/disabled/focus 상태가 있는가?
- 모바일에서 가로 넘침, 텍스트 겹침, 터치 영역 문제가 없는가?
- 데스크탑에서 위계와 밀도가 맞는가?
- 접근성 대비, aria, keyboard, reduced motion을 확인했는가?
- 공개/배포 화면이면 라이브 URL에서 실제 반영을 확인했는가?

## 벤치마크

- Braun: 잘 만들어진 도구의 촉감
- 교보문고: 따뜻한 공간감
- 츠타야: 큐레이션된 흐름
- Notion: 빈 상태와 콘텐츠 중심 UI
- Linear: 마이크로 인터랙션 품질
- Muji: 철학이 스며든 소재감

핵심은 **100에서 10을 남기는 편집**이다. 남은 것은 명료하고, 자연스럽고, 따뜻해야 한다.
