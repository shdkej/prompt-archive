# Virality Signals (한국어 1인 개발자 블로그 맥락 재가공)

> 출처: `infinity/artifacts/research-06/viral-keyword-skill.md` §3
> research-06은 글로벌 SEO/소셜 바이럴 기준이었고, 여기서는 **한국어 텍스트 콘텐츠 1인 운영** 맥락에 맞게 가중치와 측정 방법을 조정했다.
>
> 핵심 차이: 외부 API 없이 **LLM 추론만으로 평가 가능한 신호**로 좁힌다 (MVP 단계).
> 정량 검증이 필요해지면 그때 Google Trends API를 붙인다.

---

## 1. 신호 목록 (10종 → 7종으로 압축)

research-06의 10개 중 1인 운영에서 의미 있게 다룰 수 있는 7개만 남긴다.
나머지 3개(Volume·Competition·Seasonality)는 **외부 API가 있어야 진짜 측정 가능**해서 MVP에선 제외하거나 LLM 추정값으로만 처리한다.

| 신호 | 의미 | 측정 (MVP — LLM 추론) | 가중치 |
|---|---|---|---|
| **Velocity** | 최근 3~6개월간 관심도 상승 추세 | LLM이 본인 학습 컷오프 기준으로 "최근 들어 자주 언급되는지" 판단 | 0.20 |
| **Direction** | 상승·정체·하락 단계 | "지금 시작하기에 늦었는지" 판단 (상승 초기/중기/말기) | 0.10 |
| **News Hook** | 현재 이슈 사이클과의 연결성 | LLM이 알고 있는 최근 화제 사건과의 연결 가능성 | 0.10 |
| **Emotional Trigger** | 공감·놀라움·논쟁 유발 | 감성 점수 (제목 후보 단위로 평가) | 0.10 |
| **Long-tail** | 3단어 이상 구체적 키워드 | 단어 수 + 의도 구체성 | 0.10 |
| **Platform Fit** | 대상 매체(블로그·Threads·뉴스레터)와 어울리는지 | 매체별 콘텐츠 패턴 적합도 | 0.10 |
| **Personal Depth** | 내가 직접 겪은 경험 비중 | 시드 텍스트에서 "1인칭 경험" 신호 추출 | **0.30** |

> **Personal Depth를 최상위 가중치(0.30)로 두는 이유**: BRAND/Content_Strategy의 콘텐츠 철학이 "인터넷에 널린 이야기 말고, 내가 겪은 이야기". 바이럴 점수가 아무리 높아도 내 경험이 안 묻어 있으면 발행하지 않는다.

---

## 2. 점수 산식

```
Viral Score (0~100) =
  100 × (
    0.30 · PersonalDepth
  + 0.20 · Velocity
  + 0.10 · Direction
  + 0.10 · NewsHook
  + 0.10 · EmotionalTrigger
  + 0.10 · LongTail
  + 0.10 · PlatformFit
  )

각 신호는 0.0 ~ 1.0
```

### 컷오프
- **70점 이상**: 발행 추천 (블로그/Threads 둘 다)
- **50~69점**: Threads에서 가설 검증 후 반응 보고 결정
- **50점 미만**: 출력 목록에서 제외 (단, 사용자가 `--include-low`로 강제 시 표시)

---

## 3. 각 신호의 LLM 평가 가이드 (프롬프트용)

### PersonalDepth
- 시드 텍스트에 1인칭 경험이 명시되어 있는가?
- 구체적 수치·고유명사·날짜·도구명이 있는가?
- "내가 ~했다" 톤이 30% 이상 차지하는가?
- → 셋 다 만족: 1.0 / 둘: 0.7 / 하나: 0.4 / 없음: 0.1

### Velocity
- 학습 컷오프 6개월 이내에 관심도가 상승했다고 판단되는가?
- "사람들이 검색하기 시작한" 신호인가, "이미 다 안" 신호인가?
- → 명확히 상승: 1.0 / 모호: 0.5 / 하락 또는 포화: 0.2

### Direction
- 상승 초기 (블로그 잠재 독자가 늘어나는 중): 1.0
- 상승 중기 (이미 좋은 글이 몇 개 있음): 0.6
- 상승 말기/정체 (검색 결과 1페이지에 양질 글 5개+): 0.3
- 하락: 0.1

### NewsHook
- 최근 6개월 내 화제 사건과 직접 연결되는가? → 1.0
- 간접 연결 가능 (해당 분야 일반 트렌드): 0.5
- 무관: 0.2

### EmotionalTrigger
- 제목 후보가 "공감·놀라움·논쟁" 중 하나를 명확히 유발하는가?
- 단, BRAND 톤(담백·차분)을 깨면 안 됨 — 자극적 후크는 감점.
- 자연스러운 감정 유발: 1.0 / 약함: 0.5 / 무미건조: 0.2

### LongTail
- 키워드가 3단어 이상이고 검색 의도가 구체적인가? → 1.0
- 2단어: 0.6
- 1단어 (예: "쿠버네티스"): 0.2

### PlatformFit
- 블로그: 깊이·맥락이 있는 키워드 → 1.0
- Threads: 짧게 끊어 말할 수 있는 인사이트 → 1.0
- 둘 다 어울림: 1.0 / 한쪽만: 0.6 / 어느 쪽도 어색: 0.3

---

## 4. research-06 대비 변경 요약

| 항목 | research-06 (원본) | keyword-title (수정) |
|---|---|---|
| 신호 개수 | 10개 | 7개 (Volume·Competition·Seasonality 제외) |
| Velocity 가중치 | 0.30 | 0.20 (Personal Depth로 일부 이동) |
| Personal Depth | 없음 | **0.30 (최상위)** |
| 측정 방법 | 외부 API + LLM 하이브리드 | LLM 추론 only (MVP) |
| 컷오프 | 50점 | 70/50/<50 3단계 |
| 자극적 후크 | 가중치 자체 (Social Amplification) | EmotionalTrigger에 포함하되 톤 위반 시 감점 |

---

## 5. 외부 API 연동 — 네이버 데이터랩 (구현됨)

`scripts/datalab_trend.py`가 네이버 데이터랩 검색어트렌드를 호출해 **Velocity·Direction을 실측으로 교체**한다. (youtube 모드와 공유)

```
python3 scripts/datalab_trend.py --keywords "키워드1,키워드2" --months 6 --unit week
```

- **교체되는 신호**: `Velocity`, `Direction` (나머지 5개는 LLM 추론 유지)
- **반환**: 키워드별 `velocity_signal`·`direction_signal` (이미 0.0~1.0, 산식에 바로 투입)
- **매핑 규칙** (스크립트 `to_signals`):
  - change = (최근 절반 평균 ratio − 이전 절반 평균) / 이전 절반
  - Velocity: change ≥ +0.15 → 1.0 / −0.05~+0.15 → 0.5 / < −0.05 → 0.2
  - Direction: change ≥ +0.30 → 1.0 / +0.10 → 0.6 / 정체 → 0.3 / 하락 → 0.1
- **신뢰도 주의**: `low_volume_warning=true`(평균 ratio<5)거나 `points<4`면 검색량이 적어 노이즈가 크다 → LLM 추론을 병행.

### Fallback
- `ok=false`(키 없음/HTTP 오류)면 **기존 LLM 추정값으로 그대로 진행**. 외부 API는 정확도 보강일 뿐, 없어도 스킬은 동작한다.
- 키는 `NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET` 환경변수 또는 `skills/keyword-title/.env` (gitignore됨).

> 데이터랩은 **상대값(0~100)**만 준다. 절대 검색량이 필요하면 네이버 검색광고 키워드도구 API를 추가로 붙인다(서명 로직 필요, 별도 스크립트).
