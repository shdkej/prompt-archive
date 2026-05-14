---
name: keyword-title
description: >
  시드(주제·경험 조각·초안·제품 컨셉)를 받아 모드별로 후보를 뽑는다.
  지원 모드: blog (블로그 제목), threads (Threads 첫 줄), app-name (앱·서비스 이름), product-name (제품·기능 이름).
  공통 흐름: 시드 깊이 추출 → Divergent 생성 → Convergent 선별 → 자가 체크.
  Sam Samuel 톤 강제. research-06 점수 산식 + Content_Strategy 매트릭스(콘텐츠 모드) / naming 신호·카테고리(이름 모드).
  트리거: "키워드 뽑아줘", "제목 후보", "앱 이름 후보", "/keyword-title", "블로그 제목", "Threads 첫 줄"
---

# Keyword & Title

## 한 줄 정의

시드를 받아 **모드에 맞는 산출물(콘텐츠 제목 또는 제품 이름)**을 Sam Samuel 톤으로 뽑는다.

## 반드시 먼저 읽을 문서

**공통**
- `references/tone.md` — 톤 절대 규칙 + 자가 체크 6항목

**콘텐츠 모드 (blog · threads)**
- `references/signals-content.md` — 바이럴 신호 7종 + Personal Depth 0.30 산식
- `references/matrix.md` — 깊이×희소성 4사분면 + 만다라트 8축

**이름 모드 (app-name · product-name)**
- `references/signals-naming.md` — 네이밍 신호 6종 + 점수 산식
- `references/naming-categories.md` — 10개 카테고리 + Divergent-Convergent 흐름

위 문서를 안 읽으면 출력 품질 보장 안 됨.

---

## 트리거 + 모드 자동 추론

| 트리거 신호 | 모드 |
|---|---|
| "블로그 제목", "글 제목" | `blog` |
| "Threads 첫 줄", "스레드 시드" | `threads` |
| "앱 이름", "서비스 이름", "프로덕트 이름" | `app-name` |
| "기능 이름", "메뉴 이름" | `product-name` |
| 시드가 디렉토리·README·앱 컨셉이면 | `app-name` (자동 추론) |
| 시드가 1인칭 경험·회고이면 | `blog` (자동 추론) |
| 사용자 명시 우선 (`--mode=app-name` 등) | 강제 |

---

## 입력

```yaml
required:
  seed: |
    자유 형식 텍스트 또는 파일 경로.
    파일 경로면 자동으로 읽어 컨텍스트 추출.

optional:
  mode: blog | threads | app-name | product-name (기본값: 자동 추론)
  count: 3~10 (기본값: 모드별 디폴트 — blog 3·threads 3·app-name 5·product-name 5)
  platform: blog | threads | both (콘텐츠 모드 전용)
  include_low: boolean (기본값: false, 컷오프 미달도 표시)
```

---

## 처리 흐름 (공통 + 모드별 분기)

```
[0] 모드 결정
    ├── 사용자 명시 모드 우선
    └── 없으면 시드 텍스트 분석으로 자동 추론

[1] 시드 깊이 추출 ★ (신규)
    ├── 1인칭 경험 신호 (수치·도구·날짜·고유명사)
    ├── 핵심 메타포: 이 시드는 무엇을 닮았는가 (수첩? 도감? 거울? 게임?)
    ├── 반대축: 거부하는 것 (예: 도덕 설교·차가운 기업톤·무거움)
    ├── 영감원: 시드에 명시된 레퍼런스 (예: 드라마·책·앱)
    └── 사용 순간: 언제·어디서 호출되는가

[2] 모드별 분기

  [콘텐츠 모드 — blog · threads]
    ├── 만다라트 축 매핑
    ├── PersonalDepth 산정
    ├── 시드 키워드 5~15개 생성 (tone.md 통과 필터)
    ├── signals-content.md 점수 → 70/50/<50 컷오프
    ├── matrix.md 사분면 매핑
    └── 제목 후보 생성 (결론형·이야기형·선택의 순간형 / 회고형·발견형)

  [이름 모드 — app-name · product-name] ★ 강화
    ├── [Divergent] naming-categories.md 10개 카테고리로 20~30개 후보 생성
    │   ├── 시드 특성에 따라 카테고리 가중 (categories §5)
    │   ├── ★ 카테고리(1·3·6): 각 3개
    │   ├── ◆ 카테고리(2·4·7): 각 2~3개
    │   └── △ 카테고리(5·8·9): 각 1~2개
    ├── [클러스터링] 의미·음 비슷한 후보 묶고 대표 1개만
    ├── [Convergent] signals-naming.md 점수 계산 → 75/60/<60 컷오프
    ├── 자동 폐기 조건 적용 (signals-naming.md §5)
    └── 카테고리 다양성 룰 적용 (categories §3) — 최소 4개 카테고리에서 출력

[3] 자가 체크
    ├── tone.md 6항목 통과
    ├── 콘텐츠 모드: 기존 글 중복 80%+ 여부
    ├── 이름 모드: 카테고리 분산 ≥ 4개 / 자동 폐기 조건 통과
    └── 통과 못한 후보는 재생성 1회 후 폐기

[4] 출력 + outputs/ 저장
    └── outputs/YYYY-MM-DD-{slug}.md
```

---

## 출력 포맷

### 콘텐츠 모드 (blog · threads)

```markdown
# Keyword & Title — {시드 요약 15자}

## 시드
{원문}

## 깊이 분석
- 만다라트 축: {1~8}
- Personal Depth: {0.0~1.0}
- 메타포: {시드에서 추출한 1줄}
- 반대축: {거부하는 것}

## 키워드 후보 ({N}개)
| 순위 | 키워드 | 사분면 | Viral Score | 핵심 신호 |
| ... |

## 블로그 제목 후보 / Threads 첫 줄 후보
- (결론형/이야기형/선택의순간형 또는 회고형/발견형)

## 자가 체크 / 다음 액션
```

### 이름 모드 (app-name · product-name)

```markdown
# Naming — {시드 요약 15자}

## 시드
{원문 / 파일 경로}

## 깊이 분석
- 핵심 메타포: {수첩·도감·거울·게임 등}
- 반대축: {거부하는 것 — 예: 도덕 설교·차가운 기업톤}
- 영감원: {드라마·책·기존 앱 등}
- 사용 순간: {언제 어디서 호출}

## Divergent (생성 후보 — 카테고리별)
> Convergent 추리기 전 brainstorm. 점수 미부여.

| 카테고리 | 후보 |
|---|---|
| 1.의태어 | a, b, c |
| 3.메타포 | d, e, f |
| ... | ... |

## Convergent — 최종 후보 ({N}개)

| # | 이름 | 카테고리 | Naming Score | 강점 | 약점 |
|---|---|---|---|---|---|
| 1 | ... | 3.메타포 | 84 | ... | ... |
| 2 | ... | 6.펀 | 79 | ... | ... |
| ... |

> **다양성 체크**: 최종 {N}개가 {카테고리 수}개 카테고리에 분포 ✓/✗

## 추천 조합
- **메인 후보**: ... (이유 1줄)
- **반박 1순위**: ... (다른 톤이 좋다면)
- **버려도 되는 것**: ... + 이유

## 자가 체크
- [ ] tone.md 6항목 통과 ({N}/N)
- [ ] 자동 폐기 조건 통과 (signals-naming.md §5)
- [ ] 카테고리 분산 ≥ 4개 ({실제 분포})
- [ ] 자극/차가운 기업 톤 단어 없음

## 결정 시 사용자가 직접 확인할 것
1. 도메인 가용성: {이름}.app / {이름}.com / {이름}.co.kr
2. 앱스토어 검색: 동명/유사명 충돌
3. SNS 핸들: Instagram/Threads에서 {이름} 사용 가능 여부
4. 1주일 후에도 입에 붙는지 (시간 테스트)
```

---

## 출력 후 자동 저장

```
outputs/2026-05-14-{slug}.md
```

slug는 시드에서 핵심 명사 2~3개 추출 → kebab-case.
같은 날 동일 slug면 `-2`, `-3` 자동 부여.

---

## 제약

- **외부 API 호출 안 함** (MVP). LLM 추론만으로 평가.
- 콘텐츠 모드: 시드에 1인칭 경험 신호 없으면 (PersonalDepth ≤ 0.2) 출력 거부 + 시드 보강 요청.
- 이름 모드: 카테고리 분산이 3개 이하면 재추림 1회. 그래도 안 되면 출력하되 "다양성 부족" 경고.
- 톤 자가 체크 4/6 이하면 출력 거부 + 시드 재요청.
- 이름 모드는 LLM 자가 판단으로 끝. 도메인·상표·SNS 핸들 실측은 **사용자 책임** (출력에 체크리스트만 제공).

---

## infinity와의 관계

- 시드 처리 못하면 `INBOX.md`에 한 줄 추가하고 종료 (infinity 패턴).
- Heartbeat이 깨어나면 `INBOX.md`에서 위에서부터 처리.
- 처리 결과는 `outputs/`에 저장 + `INBOX.md`의 Done 섹션에 링크.

---

## 측정 / 피드백 루프

### 콘텐츠 모드
발행 후 사용자가 수동으로 `outputs/{slug}.md` 하단에 append:
- 발행일·매체·반응(좋아요/댓글/저장)·후속 인사이트

### 이름 모드 ★ 신규
이름 후보 중 어느 걸 선택했는지 1주일 후 기록:
```
## Post-decision (1주일 후)
- 선택: 덕수첩
- 사유: 1주일 동안 자기 자신에게 호명해보니 입에 가장 잘 붙음
- 1주일 시간 테스트 통과: 예/아니오
- 도메인: deoksoochop.app 확보
```

월간 리뷰에서 outputs/ 디렉토리를 훑어 어떤 카테고리·점수대 후보가 실제로 선택되는지 본다.
→ **카테고리 가중치·점수 산식을 데이터 기반으로 개선**.

---

## 변경 정책

- 톤 규칙이 바뀌면 → `references/tone.md` 수정 + THREADS_STYLE_HISTORY에 누적
- 콘텐츠 신호 가중치가 바뀌면 → `references/signals-content.md` 수정
- 네이밍 신호 가중치가 바뀌면 → `references/signals-naming.md` 수정
- 카테고리 추가/삭제는 → `references/naming-categories.md` 수정
- 사분면 정의가 바뀌면 → `references/matrix.md` 수정 (Content_Strategy.md와 동기화)
- 이 SKILL.md 자체는 트리거·모드·흐름·출력 포맷만 다룬다. 세부 기준은 references에.
