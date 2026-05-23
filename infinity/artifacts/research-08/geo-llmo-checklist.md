# GEO/LLMO 설정 조사 및 우선순위 체크리스트

> research-08 | 작성: 2026-05-23T10:00Z  
> 대상 프로젝트: Virtue, Knowledge Lab, Infinity

---

## 1. 개요

**GEO (Generative Engine Optimization)** / **LLMO (Large Language Model Optimization)**는 SEO의 AI 검색·답변엔진 버전이다. Google AI Overviews, ChatGPT Search, Perplexity, Bing Copilot 등 LLM 기반 검색엔진이 콘텐츠를 발견·인용·요약하는 방식을 최적화하는 것이 목표다.

기존 SEO와 차이:
- 클릭 유도가 아닌 **인용·출처로서의 신뢰성** 확보
- 키워드 밀도보다 **구조화된 답변 형식**
- PageRank보다 **출처 권위성 (E-E-A-T)**
- 메타 태그보다 **기계 가독형 마크업 (schema.org, llms.txt)**

---

## 2. llms.txt

### 개념
- Jeremy Howard (fast.ai)가 2024년 제안한 표준
- `robots.txt`처럼 도메인 루트에 위치 (`yourdomain.com/llms.txt`)
- LLM이 사이트 전체를 크롤하지 않고도 핵심 내용을 파악할 수 있도록 Markdown 요약 제공

### 형식
```markdown
# [사이트 이름]

> [한 줄 설명 — LLM이 이 사이트를 어떻게 소개해야 하는지]

## 주요 섹션

- [페이지 제목](URL): 한 줄 설명
- [페이지 제목](URL): 한 줄 설명

## 관련 정보

- [외부 링크](URL): 맥락
```

### 보완 파일
- `llms-full.txt`: 전체 문서 텍스트 (AI가 RAG 등으로 직접 읽을 때)
- 마크다운 버전 페이지: 각 URL에 `.md` 접미사로 Markdown 원문 제공

### 프로젝트별 적용 우선순위
| 프로젝트 | 적용 필요성 | 이유 |
|---------|-----------|------|
| Virtue | 중 | 공개 서비스이나 콘텐츠 사이트 아님 |
| Knowledge Lab | 높음 | 지식/문서 콘텐츠 → AI 인용 대상 |
| Infinity | 중 | 내부 시스템 → 공개 필요성 낮음 |

---

## 3. robots.txt / AI 크롤러 정책

### 주요 AI 크롤러 User-Agent 목록

| 크롤러 | User-Agent | 소속 | 목적 |
|-------|-----------|------|------|
| GPTBot | `GPTBot` | OpenAI | ChatGPT 학습 데이터 수집 |
| OAI-SearchBot | `OAI-SearchBot` | OpenAI | ChatGPT Search 실시간 인덱싱 |
| ClaudeBot | `ClaudeBot` | Anthropic | Claude 학습 데이터 수집 |
| anthropic-ai | `anthropic-ai` | Anthropic | Claude 웹 검색 |
| Google-Extended | `Google-Extended` | Google | Bard/Gemini 학습용 |
| PerplexityBot | `PerplexityBot` | Perplexity | Perplexity 검색 인덱싱 |
| CCBot | `CCBot` | Common Crawl | 오픈 크롤 (다수 AI 학습에 사용) |
| Amazonbot | `Amazonbot` | Amazon | Alexa/AWS AI 학습 |

### 정책 결정 기준
```
공개 콘텐츠 서비스 → 기본적으로 허용 (인용 기회 확보)
개인정보/민감정보 포함 → 명시적 차단
학습용만 차단, 검색은 허용 → GPTBot/ClaudeBot 차단, OAI-SearchBot/PerplexityBot 허용
```

### 권장 robots.txt 템플릿 (공개 콘텐츠 프로젝트)
```
User-agent: *
Allow: /

# AI 크롤러 — 검색/답변엔진용 허용
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

# 민감 경로 차단
Disallow: /admin/
Disallow: /api/private/
Disallow: /user/
```

---

## 4. Sitemap / Schema.org

### Sitemap
- XML 사이트맵은 AI 크롤러도 참조
- `<lastmod>` 태그로 최신 콘텐츠를 우선 인덱싱 유도
- 이미지·비디오 사이트맵 별도 제공 시 멀티모달 인덱싱에 유리

### 핵심 Schema.org 마크업 (JSON-LD)

**기본 (모든 사이트)**
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "사이트 이름",
  "url": "https://yourdomain.com",
  "description": "사이트 설명",
  "author": {
    "@type": "Person",
    "name": "작성자 이름"
  }
}
```

**문서/블로그 페이지**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "제목",
  "datePublished": "2026-05-23",
  "dateModified": "2026-05-23",
  "author": {"@type": "Person", "name": "저자"},
  "publisher": {"@type": "Organization", "name": "조직명"}
}
```

**FAQ 페이지** (AI 인용 확률 높음)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "질문",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "답변"
    }
  }]
}
```

**SpeakableSpecification** (음성 AI 대응)
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".summary", "#key-findings"]
  }
}
```

---

## 5. Canonical / Metadata

### Canonical
```html
<link rel="canonical" href="https://yourdomain.com/definitive-url" />
```
- AI 모델이 중복 콘텐츠를 하나의 URL로 집약하도록 유도
- www vs non-www, trailing slash, 쿼리 파라미터 처리 일관성 필수

### 핵심 메타 태그
```html
<!-- 기본 -->
<meta name="description" content="150자 이내 핵심 요약 — AI 스니펫 소스">
<meta name="author" content="저자명">

<!-- Open Graph (ChatGPT, Perplexity 미리보기에 활용) -->
<meta property="og:title" content="페이지 제목">
<meta property="og:description" content="설명">
<meta property="og:type" content="article">
<meta property="og:url" content="https://...">

<!-- 날짜 (최신성 신호) -->
<meta name="article:published_time" content="2026-05-23T10:00:00Z">
<meta name="article:modified_time" content="2026-05-23T10:00:00Z">
```

---

## 6. LLM Answer Visibility (AI 답변 노출 최적화)

### 콘텐츠 작성 원칙

**Answer-First 구조**
- 문서 상단에 핵심 답변을 1-3문장으로 요약
- H1 → 짧은 정의/요약 → 상세 설명 순서
- 결론 먼저, 근거 나중 (AI가 답변 생성 시 앞부분을 우선 활용)

**AI가 자주 인용하는 형식**
- 번호 목록 / 불릿 목록 (단계별 절차, 비교)
- 표 (비교 분석, 속성 나열)
- FAQ 섹션 (질문-답변 쌍)
- 짧은 단락 (3-5문장 이내)
- 코드 블록 (기술 문서)
- 정의: `**용어**: 설명` 형식

**피해야 할 패턴**
- 긴 서론 (결론 전 배경 설명 3단락 이상)
- JavaScript 렌더링 의존 콘텐츠 (크롤러가 실행 못함)
- 이미지에만 존재하는 핵심 정보
- 로그인 필수 콘텐츠

---

## 7. 출처·저자 신뢰 신호 (E-E-A-T)

### E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

Google AI Overviews와 Perplexity 모두 출처 신뢰성을 반영.

| 신호 | 구현 방법 |
|------|---------|
| **경험 (Experience)** | 사용 후기, 실제 사례, 구체적 수치 포함 |
| **전문성 (Expertise)** | 저자 소개 페이지, 자격증/이력, byline |
| **권위성 (Authoritativeness)** | 외부 사이트의 인용/링크, 전문 기관 언급 |
| **신뢰성 (Trustworthiness)** | About 페이지, 연락처, 편집 정책, 마지막 수정일 |

### 구체적 구현
```
/about — 저자/조직 소개, 전문 분야
/author/[name] — 개인 저자 프로필
콘텐츠 내 참고문헌/출처 링크
주장에 날짜·수치·출처 병기
```

---

## 8. 주요 AI 검색·답변 엔진별 차이

| 엔진 | 인덱싱 방식 | 크롤러 | 최적화 포인트 |
|-----|-----------|-------|------------|
| **Google AI Overviews** | Google 기존 인덱스 활용 | Googlebot + Google-Extended | schema.org, E-E-A-T, 기존 SEO 연속 |
| **ChatGPT Search** | Bing 인덱스 + OAI-SearchBot | OAI-SearchBot | Bing SEO 최적화, robots.txt OAI 허용 |
| **Perplexity** | 자체 크롤 + 실시간 검색 | PerplexityBot | 출처 표기 명확성, 인용 가능한 문장 구조 |
| **Bing Copilot** | Bing 인덱스 | Bingbot | 기존 Bing SEO, schema.org |
| **Claude (web search)** | 실시간 검색 | anthropic-ai | 구조화된 콘텐츠, llms.txt |
| **Gemini** | Google 인덱스 | Google-Extended | Google SEO와 동일 |

### 공통 최적화 전략
Bing 인덱싱이 여전히 중요 (ChatGPT Search, Copilot 동시 커버).
Bing Webmaster Tools 등록 + sitemap 제출 권장.

---

## 9. 프로젝트별 우선순위 체크리스트

### 공통 (모든 프로젝트)

**P0 — 즉시 (공수 1-2시간)**
- [ ] robots.txt에 주요 AI 크롤러 명시적 허용/차단 정책 추가
- [ ] `<meta name="description">` 콘텐츠 최신화 (150자 이내 핵심 요약)
- [ ] Canonical 태그 일관성 점검

**P1 — 단기 (공수 반나절)**
- [ ] llms.txt 초안 작성 및 배포 (공개 서비스만)
- [ ] 주요 페이지에 `WebSite`, `WebPage` schema.org JSON-LD 추가
- [ ] sitemap.xml 최신화 + `<lastmod>` 태그 추가

**P2 — 중기 (공수 1-2일)**
- [ ] About 페이지 / 저자 페이지 정비 (E-E-A-T 강화)
- [ ] FAQ 섹션 추가 + FAQPage schema 마크업
- [ ] 핵심 문서 Answer-First 구조로 재작성
- [ ] llms-full.txt 또는 페이지별 .md 버전 제공

### Virtue (virtue.oracle.shdkej.com)

현재 상태: 실사용자 온보딩 단계. AI 검색 인용보다 사용자 직접 유입 위주.

| 항목 | 우선순위 | 비고 |
|------|--------|------|
| robots.txt AI 크롤러 허용 | P1 | 현재 정책 확인 필요 |
| llms.txt (앱 소개) | P2 | 공개 페이지 대상 |
| WebSite schema | P1 | 랜딩 페이지에 추가 |
| FAQ (서비스 소개) | P2 | 주요 Q&A 구성 후 |

### Knowledge Lab (knowledge-lab)

현재 상태: 지식 문서 저장소. AI 인용 가능성 가장 높음.

| 항목 | 우선순위 | 비고 |
|------|--------|------|
| llms.txt | P0 | 핵심 문서 목록 + 설명 |
| llms-full.txt or .md variants | P1 | 문서 AI 직접 접근 |
| Article schema | P1 | 각 문서 페이지 |
| Answer-First 구조 | P1 | 기존 문서 점진적 개선 |
| 저자 정보 강화 | P2 | About 섹션 |

### Infinity (infinity.oracle.shdkej.com)

현재 상태: 내부 에이전트 시스템 대시보드. 외부 AI 인용 필요성 낮음.

| 항목 | 우선순위 | 비고 |
|------|--------|------|
| robots.txt AI 크롤러 차단 | P1 | 내부 시스템 → 학습 데이터 제외 권장 |
| llms.txt | 불필요 | 공개 인용 대상 아님 |

---

## 10. 실행 후보 목록 (승인 필요 항목)

> 아래 항목들은 실제 사이트 변경이 필요하므로 별도 승인 후 실행.

### 즉시 실행 가능 (L1 — 파일/코드 수정)
1. `knowledge-lab` robots.txt AI 크롤러 정책 추가
2. `knowledge-lab` llms.txt 생성 (문서 목록 Markdown)
3. `virtue-rebirth-app` 랜딩페이지 schema.org JSON-LD 추가

### 검토 후 실행 (L2 — 배포 필요)
4. 각 프로젝트 sitemap.xml `<lastmod>` 태그 업데이트 후 배포
5. Bing Webmaster Tools에 sitemap 제출

### 사용자 직접 판단 필요
6. Knowledge Lab 공개 여부 결정 (llms.txt 범위 결정에 영향)
7. Virtue 마케팅 방향 — AI 검색 유입 vs 직접 유입 우선순위

---

## 참고

- [llms.txt 제안 원문](https://llmstxt.org)
- [Google E-E-A-T 가이드라인](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Schema.org](https://schema.org)
- [GPTBot 정책](https://platform.openai.com/docs/gptbot)
- [Google-Extended 안내](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)
