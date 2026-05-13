# 바이럴 키워드 추천 AgentSkill 설계 분석

> research-06 | 작성일: 2026-05-05 | 작성자: Heartbeat Agent

---

## 1. 개요

사용자가 글을 쓸 때 바이럴될 가능성이 높은 키워드를 자동으로 추천해 주는 OpenClaw AgentSkill을 설계하기 위한 분석 자료다. 기존 키워드 추천 시스템을 조사하고, 바이럴 가능성 판단 신호를 정리하며, 실제 구현 가능한 스킬 설계 초안까지 포함한다.

---

## 2. 기존 키워드 추천 시스템 사례 분석

### 2-1. Google Keyword Planner (검색량 기반)

| 항목 | 내용 |
|------|------|
| 특징 | 월간 검색량, 경쟁도, 입찰가 범위 제공 |
| 강점 | 공식 구글 데이터, 지역/언어 필터 |
| 약점 | 광고 목적 설계, 트렌드 모멘텀 신호 없음 |
| 접근 | Google Ads API (유료) |
| 바이럴 적합도 | ★★☆☆☆ — 볼륨은 있지만 상승세 감지 약함 |

### 2-2. Google Trends (트렌드 모멘텀)

| 항목 | 내용 |
|------|------|
| 특징 | 검색 관심도 시계열, 지역별 인기도, 관련 쿼리 |
| 강점 | 무료, 상승 중인 키워드 5000%+ 성장 감지 가능 |
| 약점 | 절대 검색량 미제공, 알파 API 제한적 |
| 접근 | Google Trends API (alpha, 2025.07 출시) 또는 PyTrends (비공식) |
| 바이럴 적합도 | ★★★★★ — 트렌드 속도(velocity) 측정에 최적 |

### 2-3. SEMrush / Ahrefs (종합 SEO)

| 항목 | 내용 |
|------|------|
| 특징 | Keyword Magic Tool, Keyword Difficulty, SERP 분석 |
| 강점 | 대규모 DB, 경쟁도 분석, 롱테일 발굴 |
| 약점 | 유료 (월 $119+), API 호출 비용 |
| 접근 | SEMrush API, Ahrefs API |
| 바이럴 적합도 | ★★★☆☆ — 경쟁도 분석 탁월, 바이럴 속도 감지는 보통 |

### 2-4. Exploding Topics (상승 트렌드 전문)

| 항목 | 내용 |
|------|------|
| 특징 | AI로 폭발적 성장 중인 키워드 사전 감지, 시즌 스파이크 예측 |
| 강점 | 계절 키워드 스파이크 3개월 전 85% 정확도 예측 |
| 약점 | 영어권 중심, 한국어 지원 약함 |
| 접근 | Exploding Topics API (Pro) |
| 바이럴 적합도 | ★★★★☆ — 바이럴 전 조기 감지에 특화 |

### 2-5. TikTok Creative Center (소셜 트렌드)

| 항목 | 내용 |
|------|------|
| 특징 | 플랫폼 내 해시태그 분석, 게시물 수, 뷰 트렌드, 인구통계 |
| 강점 | TikTok 공식 트렌드, 크리에이터 타깃 정밀도 |
| 약점 | TikTok 외 플랫폼 적용 불가, 공식 API 제한적 |
| 접근 | TikTok Research API (공개 데이터 한정) |
| 바이럴 적합도 | ★★★★☆ — 소셜 바이럴에 강함, SNS 콘텐츠에 최적 |

### 2-6. vidIQ / TubeBuddy (YouTube 특화)

| 항목 | 내용 |
|------|------|
| 특징 | YouTube 검색량, 경쟁도, 기회 점수(Opportunity Score) 통합 |
| 강점 | YouTube 알고리즘 맞춤, 소형 채널 공략 가능 키워드 발굴 |
| 약점 | YouTube에 한정, 블로그/뉴스 미적용 |
| 접근 | vidIQ API, TubeBuddy API |
| 바이럴 적합도 | ★★★★☆ — YouTube 콘텐츠에 매우 적합 |

### 2-7. Pytrends + SerpApi (무료/저비용 조합)

| 항목 | 내용 |
|------|------|
| 특징 | PyTrends로 Google 트렌드 무료 스크래핑 + SerpApi로 SERP 분석 |
| 강점 | 비용 최소화 가능, 오픈소스 |
| 약점 | 비공식 API 불안정, SerpApi 유료 ($50/월~) |
| 접근 | GitHub: GeneralMills/pytrends, SerpApi REST API |
| 바이럴 적합도 | ★★★☆☆ — 비용 효율적, 신뢰도는 낮음 |

---

## 3. 바이럴 가능성 판단 신호 (Virality Signals)

### 3-1. 핵심 신호 목록

| 신호 | 설명 | 측정 방법 | 가중치 |
|------|------|-----------|--------|
| **검색 속도 (Velocity)** | 검색량 증가 속도. 절대 볼륨보다 모멘텀이 중요 | Google Trends 주간 변화율 | 높음 |
| **검색량 (Volume)** | 월간 절대 검색량 | Google KP / SEMrush | 중간 |
| **경쟁도 (Competition)** | 랭킹 어렵기. 낮을수록 초기 포착 용이 | KD (Keyword Difficulty) 0~100 | 중간 |
| **트렌드 방향 (Direction)** | 상승 / 안정 / 하락 중 어느 단계인지 | Trends 시계열 분석 | 높음 |
| **플랫폼 맥락 (Platform)** | Google vs YouTube vs TikTok vs 뉴스 | 플랫폼별 검색량 비교 | 중간 |
| **롱테일 여부 (Long-tail)** | 3단어 이상, 구체적 의도. 경쟁도 낮고 전환율 높음 | 단어 수, 검색 의도 분류 | 중간 |
| **소셜 증폭 (Social Amplification)** | 해시태그 사용량, 게시물 수, 공유 가능성 | TikTok CC, Twitter Trends | 높음 |
| **감성/감정 어필 (Emotional Trigger)** | 분노·공감·놀라움 등 강한 감성 반응 유도 여부 | 제목 감성 분석 | 중간 |
| **기사/이슈 연결성 (News Hook)** | 현재 뉴스 사이클과 연결 여부 | Google News, RSS 모니터링 | 높음 |
| **시즌성 (Seasonality)** | 특정 계절/이벤트 기반 스파이크 예측 | Exploding Topics, KP 계절 데이터 | 낮음 (상황별) |

### 3-2. 종합 바이럴 점수 산식 (예시)

```
Viral Score = 
  (Velocity × 0.30) +
  (Volume_normalized × 0.15) +
  ((1 - Competition_normalized) × 0.20) +
  (Direction_score × 0.15) +
  (Social_Amplification × 0.15) +
  (News_Hook × 0.05)
```

- 각 항목 0~1 정규화
- 최종 점수 0~100으로 변환

---

## 4. OpenClaw AgentSkill 설계 초안

### 4-1. SKILL.md 구조

```markdown
---
name: viral-keyword-recommender
description: >
  사용자가 작성 중인 글의 주제/초안을 입력하면,
  바이럴 가능성이 높은 키워드를 검색량·트렌드·경쟁도·플랫폼별 맥락을 분석하여
  우선순위화된 추천 목록과 사용 방법을 반환한다.
  Trigger: 사용자가 "키워드 추천", "바이럴 키워드 찾아줘", "제목 키워드", "/viral-keywords" 언급 시
---

# Viral Keyword Recommender Skill

## 역할
사용자의 글 주제로부터 바이럴 가능성이 높은 키워드를 추천한다.

## 입력 (Input)
...

## 처리 흐름 (Workflow)
...

## 출력 (Output)
...
```

### 4-2. 입력 스키마 (Input)

```yaml
input:
  required:
    - topic: "글의 주제 또는 초안 (자유 형식 텍스트, 최소 10자)"
  optional:
    - platform: "대상 플랫폼 (blog|youtube|tiktok|twitter|all, 기본값: all)"
    - language: "언어 (ko|en|ja, 기본값: ko)"
    - content_type: "콘텐츠 유형 (article|short|thread|video, 기본값: article)"
    - target_audience: "타깃 독자 설명 (예: '20대 직장인', '스타트업 창업자')"
    - max_keywords: "반환할 키워드 수 (기본값: 10)"
```

### 4-3. 도구 흐름 (Tool Flow)

```
[1] 주제 분석 (LLM)
    └── 핵심 개념 추출, 의도 분류 (정보성/감성/구매/행동)

[2] 시드 키워드 생성 (LLM)
    └── 5~15개 초기 후보 키워드 생성

[3] 트렌드 조회 (Google Trends API / PyTrends)
    └── 각 키워드의 최근 30일 트렌드 지수, 속도(velocity) 계산

[4] 검색량·경쟁도 조회 (선택적, 캐시 우선)
    └── SEMrush API 또는 Google Keyword Planner API 호출
    └── 캐시 히트 시 API 건너뜀 (24시간 TTL)

[5] 플랫폼별 소셜 신호 조회 (조건부)
    └── platform == tiktok → TikTok CC 데이터
    └── platform == youtube → vidIQ/SerpApi 데이터

[6] 바이럴 점수 계산 (LLM + 룰)
    └── 신호 가중합 → Viral Score 0~100

[7] 결과 랭킹 + 사용법 생성 (LLM)
    └── 상위 N개 키워드에 사용 가이드 포함

[8] 출력 포맷팅
    └── 구조화된 추천 결과 반환
```

### 4-4. 출력 스키마 (Output)

```yaml
output:
  summary:
    topic_intent: "분류된 글 의도 (정보성/감성/구매/행동)"
    recommended_primary: "메인 키워드 1개"
    viral_confidence: "높음|보통|낮음"
  
  keywords:
    - rank: 1
      keyword: "AI 에이전트 자동화"
      viral_score: 87
      signals:
        volume_monthly: 14400
        trend_velocity: "+340% (30일)"
        competition: "낮음 (KD: 23)"
        platforms: ["Google", "YouTube"]
        news_hook: "GPT-5 출시 이슈와 연결"
      usage_tip: "제목에 앞부분에 배치. '...하는 AI 에이전트 자동화 방법' 형식 권장"
      
  templates:
    title_options:
      - "[키워드]로 바뀌는 [분야] — [년도] 실전 가이드"
      - "[타깃]이 [키워드]를 써야 하는 이유 [숫자]가지"
      - "[키워드] 완전 정복: [기간] 만에 [결과]"
    
  metadata:
    data_freshness: "2026-05-05T08:00Z"
    sources_used: ["Google Trends", "SEMrush (캐시)", "LLM 추론"]
    cache_used: true
    api_calls_made: 2
```

---

## 5. 데이터 소스 권장 조합

### 5-1. 무료/저비용 스택 (추천: 초기 구현)

| 용도 | 도구 | 비용 |
|------|------|------|
| 트렌드 속도 | Google Trends API (alpha) + PyTrends 폴백 | 무료 |
| 키워드 기본 메트릭 | Google Keyword Planner | 무료 (Google Ads 계정 필요) |
| 소셜 신호 | TikTok Creative Center (수동/스크래핑) | 무료 |
| SERP 분석 | SerpApi (무료 100회/월) | 무료 tier |

### 5-2. 프로덕션 스택 (확장 시)

| 용도 | 도구 | 비용 |
|------|------|------|
| 종합 SEO | SEMrush API | $119+/월 |
| 트렌드 조기 감지 | Exploding Topics Pro API | $39+/월 |
| SERP 상세 | SerpApi Pro | $50+/월 |
| YouTube 특화 | vidIQ API | $7.50+/월 |

---

## 6. 캐시 및 비용 절약 전략

### 6-1. 캐시 레이어 설계

```
[요청] → [로컬 캐시 확인]
            ├── 히트 (TTL 유효): 캐시 반환 (API 0회)
            └── 미스: API 호출 → 결과 캐시 저장

TTL 정책:
  - 검색량/경쟁도: 24시간 (변화 느림)
  - 트렌드 속도: 6시간 (변화 중간)
  - 소셜 신호: 3시간 (실시간성 필요)
  - LLM 추론 결과: 1시간 (동일 주제 재요청 시)
```

### 6-2. LLM 우선 추론 전략

API 비용 절감을 위해 LLM이 먼저 추론하고, 검증이 필요한 경우에만 외부 API를 호출한다.

```
단계 1: LLM만으로 초안 생성 (비용: 0)
  → 지식 컷오프 내 트렌드는 LLM이 직접 평가

단계 2: 트렌드 API로 최신성 검증 (비용: 소)
  → 지식 컷오프 이후 키워드만 API 호출

단계 3: SEO 메트릭 API (비용: 중, 캐시 최대화)
  → 사용자가 명시적으로 "정확한 수치 필요" 시에만
```

### 6-3. 배치 처리

동일 사용자의 키워드 요청을 배치로 묶어 1회 API 호출로 처리한다.
- 단일 요청: 10 키워드 → API 10회 → 비용 10x
- 배치 처리: 10 키워드 → API 1~2회 → 비용 80% 절감

---

## 7. 실사용 키워드 추천 결과 템플릿

### 7-1. 블로그/아티클용 템플릿

```
🔑 바이럴 키워드 추천 결과
━━━━━━━━━━━━━━━━━━━━
주제 의도: 정보성 | 플랫폼: 블로그
바이럴 신뢰도: 높음

TOP 키워드
━━━━━━━━━━━━━━━━━━━━
1위. AI 에이전트 자동화  [점수: 87/100]
   📈 트렌드: +340% (30일)  🔍 월 검색: 14,400  🥊 경쟁도: 낮음
   💡 사용법: 제목 앞부분 배치. "AI 에이전트 자동화로 업무 90% 줄이는 법"
   🔗 뉴스 훅: GPT-5 출시 이슈와 시너지

2위. 업무 자동화 AI  [점수: 79/100]
   📈 트렌드: +180% (30일)  🔍 월 검색: 22,000  🥊 경쟁도: 중간
   💡 사용법: 소제목 또는 본문 강조 키워드로 활용
   🔗 뉴스 훅: 기업 AI 도입 뉴스 증가

제목 조합 아이디어:
• "AI 에이전트 자동화 실전 가이드 — 2026년 버전"
• "업무 자동화 AI가 바꿔놓은 직장인의 하루"
• "AI 에이전트 자동화 안 하면 뒤처지는 이유"

⚡ 데이터 기준: 2026-05-05 | 캐시 사용: 예 | API 호출: 2회
```

### 7-2. 짧은 포맷 (SNS/스레드용)

```
🔑 키워드: AI 에이전트 자동화 [87점]
📈 +340% 급상승 | 경쟁도: 낮음
💡 훅: "이거 안 하면 뒤처진다" 프레임 권장
#AI자동화 #에이전트 #업무효율
```

---

## 8. 구현 우선순위 로드맵

| 단계 | 내용 | 난이도 | 소요 시간 |
|------|------|--------|-----------|
| MVP | LLM만으로 키워드 추천 (API 없음) | 낮음 | 1 Heartbeat |
| v1.0 | Google Trends + PyTrends 연동 | 낮음 | 2 Heartbeat |
| v1.5 | 캐시 레이어 + 배치 처리 추가 | 중간 | 1 Heartbeat |
| v2.0 | SEMrush/Ahrefs API 연동 | 높음 | 2 Heartbeat (L2 승인 필요) |
| v2.5 | 플랫폼별 분기 (TikTok/YouTube 특화) | 중간 | 2 Heartbeat |

---

## 9. 참고 자료

- [OpenClaw Skills 공식 문서](https://docs.openclaw.ai/tools/skills)
- [Best Keyword Research Tools 2026](https://topicalmap.ai/blog/auto/best-keyword-research-tools-2026)
- [Google Trends API (alpha)](https://developers.google.com/search/blog/2025/07/trends-api)
- [AI Agent Skills Guide 2026 - Nevo](https://nevo.systems/blogs/nevo-journal/what-are-ai-agent-skills)
- [Viral Content Keyword Signals - SEMrush](https://www.semrush.com/kb/257-keyword-overview)
- [TikTok Hashtag Strategy 2026 - Sprout Social](https://sproutsocial.com/insights/tiktok-hashtags/)
- [Exploding Topics - 키워드 조기 감지](https://zoomyourtraffic.com/130-seo-statistics-every-marketer-must-know-in-2026-exploding-topics/)
- [PyTrends GitHub](https://github.com/GeneralMills/pytrends)
- [ASO Skills AgentSkill 예시](https://github.com/Eronred/aso-skills)

---

## 10. 스킬 구현을 위한 즉시 사용 가능한 SKILL.md 초안

```markdown
---
name: viral-keyword-recommender
description: >
  사용자의 글 주제나 초안을 입력받아 바이럴 가능성이 높은 키워드를
  검색량·트렌드 속도·경쟁도·플랫폼 맥락 기준으로 분석하여 우선순위화된
  추천 목록과 제목 조합 아이디어를 반환한다.
  트리거: "키워드 추천", "바이럴 키워드", "/viral-keywords", "제목 키워드 찾아줘"
---

# Viral Keyword Recommender

## 맥락
너는 콘텐츠 마케터와 글쓴이를 돕는 키워드 분석 전문 에이전트다.
사용자의 글이 더 많이 읽히고 공유될 수 있도록, 지금 이 순간 가장
바이럴 가능성이 높은 키워드를 찾아 추천한다.

## 입력 처리
1. 사용자의 주제/초안에서 핵심 개념 3~5개 추출
2. 글의 의도 분류: 정보성 / 감성 / 실용 / 논쟁성
3. 대상 플랫폼 확인 (미입력 시: 블로그 기본값)

## 키워드 생성 및 평가
1. 시드 키워드 10~15개 생성
2. 각 키워드에 대해:
   - 트렌드 속도 추정 (최근 급상승 여부)
   - 검색 의도 적합도 평가
   - 경쟁도 추정 (콘텐츠 포화도)
   - 소셜 공유 가능성 평가 (감성 트리거, 논쟁성)
   - 뉴스 사이클 연결성 확인
3. 바이럴 점수 계산 후 상위 10개 선택

## 출력 형식
아래 형식으로 출력한다:

```
🔑 바이럴 키워드 추천 — [주제 요약]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
의도: [분류] | 플랫폼: [플랫폼]

TOP [N] 키워드
━━━━━━━━━━━━
[순위]. [키워드]  [점수/100]
   📈 트렌드: [상승률]  🔍 월 검색: [추정값]  🥊 경쟁도: [낮음/중간/높음]
   💡 사용법: [제목/본문 배치 팁]
   🔗 연결 이슈: [뉴스/트렌드 연결점]

제목 조합 아이디어:
• [제목 예시 1]
• [제목 예시 2]
• [제목 예시 3]
```

## 제약
- 검색량 수치는 추정값임을 명시. 실시간 API 미연결 시 "(추정)" 표기
- 경쟁도가 높음인 키워드는 "차별화 앵글 필요" 경고 포함
- 바이럴 점수 50점 미만 키워드는 목록에서 제외
- 트렌드 데이터가 오래됐을 경우 "데이터 갱신 필요" 알림
```
