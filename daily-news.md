---
description: 이 워크플로우는 사용자가 입력한 키워드를 기반으로 최신 뉴스를 검색하고, 이를 구조화(JSON)하여 중복을 제거한 뒤 요약 보고서를 생성합니다.
---

# Daily News Summary Workflow

이 워크플로우는 사용자가 입력한 키워드를 기반으로 최신 뉴스를 검색하고, 이를 구조화(JSON)하여 중복을 제거한 뒤 요약 보고서를 생성합니다.

## 1. Input Processing

사용자가 제공한 콤마(,)로 구분된 키워드를 파싱합니다.
만약 사용자가 입력한 내용이 없다면 기본 키워드 **"보안, 침해"** 를 사용합니다.
예: "HR, 노무, 직무" -> ["HR", "노무", "직무"]
예: (입력 없음) -> ["보안", "침해"]

## 2. Information Retrieval (Loop per Keyword)

각 키워드별로 https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR
형태의 RSS를 조회하고, RSS item 단위로 결과를 수집하는 구조로 바꿔주세요. (한글뉴스를 검색해야되서 ko, KR파라미터가 있어야 합니다.)

- **Action**: 각 키워드별 검색 결과를 수집합니다.

## 3. Data Structuring (JSON)

검색 결과를 아래와 같은 JSON 포맷으로 정리합니다. (메모리에 저장해도 되고 결과와 함께 저장해도 됩니다.)

[
{
"keyword": "HR",
"articles": [
{
"title": "기사 제목",
"link": "https://...",
"snippet": "기사 요약 내용...",
"source": "언론사명",
"published_date": "YYYY-MM-DD"
}
]
},
...
]

## 4. Analyze & Summarize

구조화된 데이터를 바탕으로 LLM이 다음 작업을 수행합니다:

1. **Deduplication**: url이나 제목이 유사한 중복 기사를 제거합니다.
2. **Clustering**: 유사한 주제끼리 그룹핑합니다.
3. **Summarization**: 각 그룹별 핵심 내용을 3줄 이내로 요약합니다.

## 5. Report Generation

최종 결과를 Markdown 파일로 생성하고, 이를 사용자의 로컬 폴더로 저장합니다.

**Action**:

1. 리포트 파일을 아티팩트로 생성합니다.
2. `run_command`를 사용하여 `news_output` 폴더를 생성하고(없을 경우), 아티팩트 파일과 JSON 데이터를 해당 폴더로 복사합니다.
   - 예: `mkdir -p news_output && cp {artifact_path} ./news_output/DAILY_NEWS_REPORT_{YYYYMMDD}`

**Format**:

```markdown
# 📰 일일 뉴스 요약 보고서 (YYYY-MM-DD)

## 1. {Keyword}

### 📌 {Topic / Group Title}

- **요약**: 기사 내용을 종합하여 핵심 내용을 서술합니다.
- **관련 기사**:
  - [기사 제목](링크) - _언론사 (소스)_
  - [기사 제목](링크) - _언론사 (소스)_

> 소스 라벨 예시: `_GQ korea (구글)_`, `_mk (네이버)_`, `_전자신문 (전자뉴스RSS)_`
```

## 주의사항

### ⚠️ 링크 정확성 (중요)

모든 기사 링크는 **해당 기사의 정확한 고유 URL**이어야 합니다. 언론사 메인 페이지 URL을 사용하면 안 됩니다.

- ✅ 올바른 예: `https://www.etnews.com/20260211000336` (기사 고유 URL)
- ❌ 잘못된 예: `https://www.etnews.com` (언론사 메인 페이지)
- ❌ 잘못된 예: `https://m.boannews.com` (모바일 메인 페이지)

**소스별 링크 처리 방법:**

1. **네이버 API**: `naver_news.py`의 출력에서 `link` 필드(기사 URL)와 `source` 필드(예: `mk (네이버)`)를 사용합니다.
2. **구글 RSS**: RSS item의 `<link>` 태그 URL을 사용하고, `<source>` 태그의 텍스트에 `(구글)`을 붙여 라벨링합니다. 예: `_GQ korea (구글)_`
3. **전자뉴스 RSS**: RSS item의 `<link>` 태그 URL을 사용하고, 소스는 `_전자신문 (전자뉴스RSS)_`로 표기합니다.

### 기타

- 요청 날짜의 전일자 기사에서만 가져옵니다.

---

# Parsing Site

전일자기준으로 아래 사이트들을 읽어서 뉴스기사를 가져옵니다

## 전자뉴스 보안 RSS

https://rss.etnews.com/04045.xml

## 구글

각 키워드별로 https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR
형태의 RSS를 조회하고, RSS item 단위로 결과를 수집하는 구조로 바꿔주세요. (한글뉴스를 검색해야되서 ko, KR파라미터가 있어야 합니다.)

## 네이버

Python 스크립트(`scripts/naver_news.py`)를 `run_command`로 호출하여 네이버 뉴스를 가져옵니다.

// turbo

```bash
python3 scripts/naver_news.py "키워드1,키워드2" --display 10 --sort date
```

```

- `--display`: 키워드당 결과 수 (기본 10, 최대 100)
- `--sort`: `date`(날짜순, 기본) 또는 `sim`(유사도순)
- 출력: JSON 배열 (`[{ "keyword": "...", "count": N, "articles": [...] }]`)
- 이 결과를 Step 3의 데이터 구조화에 포함시킵니다.
```
