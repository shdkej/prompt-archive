# Sam Samuel Design System

> 참조: BRAND.md
> "생산자를 만든다" - 모든 사용자가 생산자가 된다

이 디자인 시스템은 Sam Samuel 브랜드의 **범용 기반**입니다. 각 앱은 이 시스템을 계승하고, 키 컬러만 오버라이드합니다.

---

## 설계 원칙

1. **선택지 최소화** - 고민을 줄인다. 타이포 4단계, 간격 5단계, 컬러 7종이면 충분하다
2. **의미 중심** - "이게 무슨 색이냐"가 아니라 "이 색은 언제 쓰는가"가 드러나야 한다
3. **UI는 배경으로** - 사용자의 콘텐츠가 주인공. 도구는 느껴지지 않아야 한다

### 절대 하지 않는 것

- Atomic Design 풀세트
- blue-100 ~ blue-900 팔레트 중심 토큰
- ghost, outline, subtle, link 등 과잉 변형
- UX 패턴 대백과
- Figma 50장

---

## 1. 컬러 토큰

의미 중심(semantic) 토큰만 사용한다. 기본은 뉴트럴이며, 각 앱에서 `--color-primary` 계열을 오버라이드한다.

### 라이트 모드 (기본)

```css
:root {
  /* 배경 */
  --color-bg:             #F0EEE9;
  --color-surface:        #F7F6F3;
  --color-surface-hover:  #EDEAE4;

  /* 텍스트 */
  --color-text-primary:   #1A1A1A;
  --color-text-secondary: #6B6B6B;
  --color-text-muted:     #9A9A9A;

  /* 포인트 (앱별 오버라이드 대상) */
  --color-primary:        #1A1A1A;
  --color-primary-hover:  #333333;
  --color-primary-muted:  rgba(26, 26, 26, 0.08);

  /* 상태 (앱 간 통일) */
  --color-danger:         #C44536;
  --color-danger-hover:   #A83A2E;
  --color-success:        #2D5A27;
  --color-warning:        #D4A026;

  /* 경계/구분 */
  --color-border:         rgba(0, 0, 0, 0.08);
  --color-border-focus:   rgba(0, 0, 0, 0.20);
  --color-overlay:        rgba(0, 0, 0, 0.4);

  /* 그림자 (자연적 조명 효과) */
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md:  0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.12);
}
```

### 다크 모드

완전 검은색(`#000`)을 피한다. 따뜻한 차콜 기반.

```css
[data-theme="dark"] {
  --color-bg:             #1C1B19;
  --color-surface:        #2A2926;
  --color-surface-hover:  #343330;

  --color-text-primary:   #E8E6E1;
  --color-text-secondary: #A0A0A0;
  --color-text-muted:     #6B6B6B;

  --color-primary:        #E8E6E1;
  --color-primary-hover:  #D0CEC9;
  --color-primary-muted:  rgba(232, 230, 225, 0.10);

  --color-danger:         #E05545;
  --color-success:        #4A9E42;
  --color-warning:        #E8B84A;

  --color-border:         rgba(255, 255, 255, 0.08);
  --color-border-focus:   rgba(255, 255, 255, 0.20);
  --color-overlay:        rgba(0, 0, 0, 0.6);

  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-md:  0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.4);
}
```

### 앱별 키 컬러 오버라이드

각 앱은 `--color-primary` 계열 3개만 재정의하면 된다.

```css
/* 예: 녹색 계열 앱 */
:root {
  --color-primary:       #2D5A27;
  --color-primary-hover: #244B20;
  --color-primary-muted: rgba(45, 90, 39, 0.12);
}
```

키 컬러 선택 기준:
- 채도: 중-저채도 (Muted). 고채도 네온 금지
- 색상: 자연에서 발견되는 색 (세이지 그린, 인디고, 테라코타, 머스타드 등)
- 적용 비율: 전체 화면의 10% 이내 (CTA, 활성 상태에만)

---

## 2. 타이포그래피

Pretendard 단일 폰트. 굵기 3단계(400, 600, 700)만 사용한다.

```
font-family: 'Pretendard Variable', 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif
```

### 4단계 스케일

| 토큰 | 모바일 | 데스크톱 (md+) | 굵기 | 행간 | 용도 |
|------|--------|----------------|------|------|------|
| heading-lg | 28px (1.75rem) | 36px (2.25rem) | 700 | 1.2 | 페이지 타이틀 |
| heading-md | 20px (1.25rem) | 24px (1.5rem) | 600 | 1.3 | 섹션 제목 |
| body | 16px (1rem) | 16px (1rem) | 400 | 1.6 | 본문 |
| caption | 13px (0.8125rem) | 14px (0.875rem) | 400 | 1.4 | 보조 텍스트 |

사용 규칙:
- heading-lg: 페이지당 최대 1개
- caption: 단독으로 주요 정보 전달 금지

### 폰트 로딩

- `font-display: swap` 필수
- subset 폰트 생성 (한글 2350자 + 영숫자)
- 시스템 폰트 metric 매칭으로 FOUT 최소화

---

## 3. 간격 & 곡률

### 간격 (8px 그리드)

| 토큰 | 값 | 용도 |
|------|-----|------|
| xs | 4px | 아이콘-텍스트 사이 |
| sm | 8px | 관련 요소 간 |
| md | 16px | 카드 내부 패딩 |
| lg | 24px | 그룹 간 간격 |
| xl | 32px | 섹션 간 구분 |
| 2xl | 48px | 페이지 상하단 여백 |

spacing 토큰 외 임의 margin/padding 금지.

### 곡률 (Border Radius)

AI 기본 스타일의 과도한 곡선을 피하고, 자연스럽게.

| 토큰 | 값 | 용도 |
|------|-----|------|
| radius-sm | 6px | 버튼, 입력, 뱃지 |
| radius-md | 10px | 카드, 드롭다운 |
| radius-lg | 16px | 모달, 바텀시트 |
| radius-full | 9999px | 아바타, 태그 |

---

## 4. 핵심 컴포넌트

5개만 만든다. 새 UI는 이 컴포넌트로 먼저 시도한다.

모든 컴포넌트는 **Compound + Flat 하이브리드** 패턴을 따른다:
- **Flat API**: 단순한 경우. props만으로 완결
- **Compound API**: 복잡한 경우. 내부 구조 재배치 가능
- 내부 로직(스타일, 상태, 접근성)은 공유하고 외부 인터페이스만 분기

### 4-1. Button

| variant | 용도 |
|---------|------|
| primary | 주요 액션 (저장, 확인) |
| secondary | 보조 액션 (취소, 뒤로) |
| danger | 파괴적 액션 (삭제) |

size: `sm` (32px) / `md` (40px)
state: `default` / `hover` / `active` / `disabled` / `loading`

- loading 시 버튼 너비 고정 (레이아웃 점프 방지)
- 클릭 후 즉시 시각적 피드백 (100ms 이내)
- `<button>` 태그 필수. `<div onclick>` 금지

```tsx
// Flat
<Button variant="primary" size="md" loading={isSubmitting}>저장하기</Button>

// Compound
<Button variant="primary" size="md">
  <Button.Icon><SaveIcon /></Button.Icon>
  <Button.Label>저장하기</Button.Label>
</Button>
```

### 4-2. Input

| variant | 용도 |
|---------|------|
| default | 한 줄 입력 |
| textarea | 여러 줄 입력 |

size: `sm` (32px) / `md` (40px)
state: `default` / `focus` / `error` / `disabled`

- placeholder는 label 대체 금지 (사라지면 맥락 소실)
- 유효성 검사는 포커스 아웃 시 권장 (타이핑 중 빨간색 = 인지 방해)
- `<label>` 연결 필수. 에러 시 `aria-invalid` + `aria-describedby`

```tsx
// Flat
<Input label="이메일" placeholder="you@example.com" error="형식을 확인해주세요" />

// Compound
<Input>
  <Input.Label>이메일</Input.Label>
  <Input.Field placeholder="you@example.com" />
  <Input.Error>형식을 확인해주세요</Input.Error>
</Input>
```

### 4-3. Select

size: `sm` (32px) / `md` (40px)
state: `default` / `open` / `disabled` / `error`

- 키보드: 화살표 탐색, Enter 선택, Escape 닫기
- 옵션 5개 이상 시 타이핑 필터링 제공
- 모바일에서는 네이티브 `<select>` 우선 고려

```tsx
// Flat
<Select label="카테고리" options={categories} value={selected} onChange={setSelected} />

// Compound
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>
    <Select.Value placeholder="선택하세요" />
  </Select.Trigger>
  <Select.Content>
    <Select.Item value="work">업무</Select.Item>
    <Select.Item value="personal">개인</Select.Item>
  </Select.Content>
</Select>
```

### 4-4. Modal

| variant | 용도 |
|---------|------|
| dialog | 확인/취소 대화상자 |
| sheet | 바텀시트 (모바일 우선) |

size: `sm` (max 400px) / `md` (max 520px)

- ESC 키, 배경 클릭으로 닫기 (파괴적 행동 Modal 제외)
- 포커스 트랩 필수 (Tab 키가 모달 밖으로 나가지 않음)
- 열릴 때 포커스 이동, 닫힐 때 트리거 요소로 포커스 복귀
- `role="dialog"` + `aria-modal="true"` + `aria-labelledby`

```tsx
// Flat
<Modal
  open={isOpen}
  title="비우시겠습니까?"
  description="이 작업은 되돌릴 수 없습니다."
  onConfirm={handleDelete}
  confirmLabel="비우기"
  confirmVariant="danger"
/>

// Compound
<Modal open={isOpen} onOpenChange={setOpen}>
  <Modal.Header>
    <Modal.Title>프로필 편집</Modal.Title>
    <Modal.Close />
  </Modal.Header>
  <Modal.Body>...</Modal.Body>
  <Modal.Footer>
    <Button variant="secondary">취소</Button>
    <Button variant="primary">저장하기</Button>
  </Modal.Footer>
</Modal>
```

### 4-5. Toast

| variant | 용도 |
|---------|------|
| default | 일반 알림 |
| success | 성공 피드백 |
| error | 오류 알림 |

- 위치: 하단 중앙, safe-area 위
- 지속: 3초 (error는 5초). 호버 시 타이머 일시정지
- 최대 동시 3개, 스택 형태
- `role="status"` (일반) / `role="alert"` (긴급)

```tsx
toast("저장했어요")
toast.success("완료했어요")
toast.error("저장에 실패했습니다. 다시 시도해주세요")
```

---

## 5. 마이크로카피 톤 가이드

### 톤 원칙

| 원칙 | 설명 |
|------|------|
| 동반자 톤 | 가르치지 않고 함께한다. 선생님이 아니라 옆자리 동료 |
| 행동 유도 | 상태 설명에 그치지 않고 다음 행동을 안내 |
| 간결함 | 한 문장이면 충분. 느낌표 최소화 |

### 버튼 카피

| 지양 | 지향 | 이유 |
|------|------|------|
| 확인 | 저장하기 | 행동을 구체적으로 |
| 제출 | 공유하기 | 사용자 관점의 결과 |
| 삭제 | 비우기 | 덜 공격적 |

### 에러 메시지

| 지양 | 지향 |
|------|------|
| 오류가 발생했습니다 | 잠깐, 문제가 생겼어요. 다시 시도해주세요 |
| 잘못된 입력입니다 | 형식을 확인해주세요 (예: example@mail.com) |
| 네트워크 오류 | 연결이 불안정해요. 잠시 후 다시 시도해주세요 |

사용자 탓을 하지 않는다. "잘못된" 대신 "확인해주세요".

### 빈 상태 (가장 중요한 브랜딩 접점)

| 화면 | 지양 | 지향 |
|------|------|------|
| 목록 | 항목이 없습니다 | 첫 항목을 만들어보세요 |
| 검색 | 결과 없음 | 다른 키워드로 찾아볼까요? |
| 알림 | 알림이 없습니다 | 조용한 하루예요 |

빈 상태에는 반드시 다음 행동을 제안하는 버튼이 따른다. 빈 상태는 끝이 아니라 시작.

### 로딩/완료

| 상황 | 지양 | 지향 |
|------|------|------|
| 로딩 | 로딩 중... | 준비하고 있어요 |
| 완료 | 저장되었습니다 | 저장했어요 |

"~되었습니다"(수동) 대신 "~했어요"(능동). 사용자가 주체.

---

## 6. 접근성 규칙

선택이 아니라 강제.

### 명암비
- 일반 텍스트: 4.5:1 이상 (WCAG AA)
- 대형 텍스트: 3:1 이상
- `#F0EEE9` 배경 위 텍스트 색상은 반드시 명암비 검증 후 확정

### 컬러 독립성
- 컬러만으로 의미를 전달하지 않는다
- error = 빨간색 + 아이콘 + 텍스트 (색맹 대응)

### 키보드
- 모든 인터랙티브 요소는 Tab으로 도달 가능
- 포커스 링은 숨기지 않는다
- `prefers-reduced-motion` 미디어 쿼리 대응 필수

### 시맨틱 마크업

| 컴포넌트 | 필수 |
|----------|------|
| Button | `<button>` 태그. loading 시 `aria-busy="true"` |
| Input | `<label>` 연결. 에러 시 `aria-invalid` + `aria-describedby` |
| Modal | `role="dialog"` + `aria-modal="true"` + 포커스 트랩 |
| Select | 커스텀 시 `role="listbox"` + `role="option"` |
| Toast | `role="status"` 또는 `role="alert"` + `aria-live` |

---

## 7. 사용 규칙 (코드 제약으로 강제)

문서가 아니라 코드/설정으로 강제한다.

| 규칙 | 강제 방법 |
|------|-----------|
| Button은 이 컴포넌트만 사용 | 새 컴포넌트 추가 시 PR에 사유 명시 |
| spacing 토큰 외 margin 금지 | ESLint 커스텀 룰 |
| 새 UI는 기존 컴포넌트로 먼저 시도 | PR 리뷰 체크리스트 |
| 하드코딩 컬러 금지 | Tailwind arbitrary value 경고 |
| 폰트 굵기 400/600/700 외 금지 | tailwind.config에 fontWeight 제한 |

---

## 운영 체크리스트 (월간)

- [ ] 다크모드 전체 화면 육안 검수
- [ ] Lighthouse 접근성 점수 95점 이상 확인
- [ ] 폰트 로딩 P95 1초 이내 확인
- [ ] 디자인 토큰 변경 이력 기록
- [ ] axe-core 자동 테스트 커버리지 확인

---

## 벤치마크

| 브랜드 | 참고 포인트 |
|--------|------------|
| Notion | 빈 상태 설계, 콘텐츠 중심 UI |
| Linear | 마이크로 인터랙션 품질, 속도감 |
| Muji | 브랜드 철학의 일관된 시각적 침투, 소재감 |

핵심: 세 브랜드 모두 **"빠진 것"으로 브랜딩**한다. 넣은 것이 아니라 뺀 것이 디자인이다.
