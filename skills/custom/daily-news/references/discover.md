# 모드 2: 자동 발견

**목차**

- [Step 1: 취향 프로필 로드](#step-1-취향-프로필-로드)
- [Step 2: GeekNews 최신글 수집](#step-2-geeknews-최신글-수집)
- [Step 3: 중복 필터링](#step-3-중복-필터링)
- [Step 4: AI/기술 관련 기사 선별](#step-4-ai기술-관련-기사-선별)
- [Step 5: 선별 결과 확인](#step-5-선별-결과-확인)
- [Step 6: 뉴스 생성](#step-6-뉴스-생성)
- [Step 7: preferences.md 업데이트](#step-7-preferencesmd-업데이트)

URL 입력 없이 GeekNews에서 자동으로 AI/기술 관련 기사를 찾아 뉴스를 생성합니다.

### Step 1: 취향 프로필 로드

`$NEWS_DIR/preferences.md` 파일을 읽어 현재 취향을 파악합니다.

확인할 항목:
- 관심 주제와 가중치 (높음/중간/낮음)
- 제외 주제 목록
- 이미 다룬 Topic ID 목록
- 선호 스타일 (깊이, 대상, 분량)
- 최근 피드백 히스토리 2~3건 (가장 최근 피드백 맥락 반영)

### Step 2: GeekNews 최신글 수집

다음 두 페이지를 가져옵니다 (병렬 실행).

**주의**: GeekNews 목록 수집은 아래와 같이 TLS 검증을 유지하는 `curl -fsSL`을 사용합니다. 403이면 브라우저 User-Agent와 재시도를 적용하며, TLS 검증 우회(`-k`)는 사용하지 않습니다.

**페이지 1: GeekNews 최신글**
```bash
curl -fsSL --retry 2 --retry-delay 1 -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36' https://news.hada.io/new
```

**페이지 2: GeekNews GN+ (양질의 긴 글)**
```bash
curl -fsSL --retry 2 --retry-delay 1 -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36' https://news.hada.io/plus
```

HTML에서 `topic_row` div를 파싱하여 각 글의 topic ID, 제목, 원본 URL, 포인트 수, 댓글 수를 추출합니다.

`/plus`의 GN+ 항목은 AI/LLM/에이전트/개발자 도구/인프라 주제에서 우선 후보군으로 봅니다. 최신 `GN+`에 좋은 AI 후보가 있으면 외부 뉴스(AITimes, AITrends 등)보다 먼저 검토하고, 적어도 1개는 포함 가능한지 판단합니다. 포함하지 않는 경우에는 "이미 다룸", "AI 관련성 낮음", "중복", "출처 신뢰/접근 문제" 중 하나로 제외 이유를 남깁니다.

**개별 기사 상세 내용 조회:**
```bash
curl -fsSL --retry 2 --retry-delay 1 -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36' 'https://news.hada.io/topic?id={topic_id}'
```
(zsh에서 `?`가 glob으로 해석되므로 반드시 URL을 따옴표로 감싸야 합니다)

### Step 3: 중복 필터링

Step 1에서 로드한 "이미 다룬 Topic ID" 목록과 비교하여 이미 다룬 글을 제외합니다.

추가로 `$NEWS_DIR/output/` 디렉토리의 기존 뉴스 파일들에서 GeekNews URL을 grep하여 혹시 누락된 topic ID도 확인합니다:

```bash
grep -ohP 'topic\?id=\d+' \
  "$NEWS_DIR/output"/daily-news-*.md | sort -u
```

전날 뉴스와의 중복은 하드 블로커입니다. `daily-news-{어제 날짜}*.md`에 나온 Topic ID, 원문 URL, 제목과 겹치는 후보는 선별 점수와 무관하게 제외합니다. GeekNews가 아닌 외부 뉴스 URL도 기존 출력 파일에서 같은 URL이나 제목이 발견되면 제외합니다. 제목 비교는 소문자화, 연속 공백 1개로 정리, 말미 매체명/괄호 설명 제거 후 비교합니다.

점수 선별 전에 `전날 중복 제외 후 남은 GeekNews/GN+ AI 후보 수`와 `그중 GN+ 후보 수`를 확인합니다. 이 수가 1개 이상인데 외부 뉴스만 선택되면 선별 실패로 보고 다시 고릅니다.

### Step 4: AI/기술 관련 기사 선별

남은 글들 중에서 preferences.md의 관심 주제와 매칭하여 점수를 매깁니다.

**점수 계산 규칙**:
- 관심 주제 "높음" 매칭: +3점
- 관심 주제 "중간" 매칭: +2점
- 관심 주제 "낮음" 매칭: +1점
- 제외 주제 매칭: -10점 (사실상 제외)
- GN+의 AI/LLM/에이전트/AI 코딩/개발자 도구/인프라 운영 주제: +3점
- `loop engineering`, 에이전트 자율성, AI 코딩 운영법, 컨텍스트/메모리/검증/하네스/테스트 루프처럼 AI를 실제 워크플로우에 붙이는 방법론: +3점. 단, 제목/요약/본문 핵심 중 2곳 이상에서 확인될 때만 부여합니다.
- GeekNews 포인트 20 이상: +1점 보너스
- GeekNews 댓글 5개 이상: +1점 보너스
- GN+ 우선 가산과 방법론 가산이 동시에 맞아도 둘의 합산 보너스는 최대 +4점으로 제한합니다.

**선별 기준**:
- 점수 상위 1~3개 기사 선택
- 최소 점수 2점 이상인 기사만 포함
- AI/기술과 무관한 기사는 제외
- GeekNews/GN+에 점수 3점 이상의 새 AI 후보가 있으면 외부 뉴스만으로 리스트를 채우지 않습니다.
- 같은 날 AI 뉴스 10개를 구성하는 경우에도 GeekNews/GN+의 강한 후보를 먼저 채우고, 외부 뉴스는 남은 슬롯을 보강하는 용도로 씁니다.

### Step 5: 선별 결과 확인

선별된 기사 목록을 사용자에게 보여주고 확인을 받습니다:

```
GeekNews에서 다음 기사를 선별했습니다:

1. [제목1] (topic ID: XXXXX, 점수: X점)
   - 매칭 주제: AI 코딩 도구
2. [제목2] (topic ID: XXXXX, 점수: X점)
   - 매칭 주제: LLM/AI 모델 동향

이 기사들로 뉴스를 생성할까요? (Y/변경사항)
```

선별 결과 아래에는 사후 검증용으로 `포함 후보`, `제외 후보`, `제외 사유`를 3~5줄 남깁니다. GN+ 강한 후보를 제외한 경우 제외 사유는 반드시 "이미 다룸", "AI 관련성 낮음", "중복", "출처 신뢰/접근 문제", "더 강한 후보에 밀림" 중 하나로 씁니다.

### Step 6: 뉴스 생성

사용자가 확인하면, 선별된 기사의 GeekNews URL을 구성하여 **모드 1(뉴스 생성)의 Step 1.5~6을 그대로 실행**합니다.

각 기사의 URL 형식: `https://news.hada.io/topic?id={topic_id}`

실행 단계:
- Step 1.5: 중복 뉴스 차단
- Step 2: GeekNews 페이지 수집
- Step 3: 원본 문서 수집
- Step 4: 뉴스 콘텐츠 작성
- Step 5: 전체 뉴스레터 조립
- Step 6: 파일 저장

### Step 7: preferences.md 업데이트

뉴스 생성 완료 후, 사용한 topic ID를 `$NEWS_DIR/preferences.md`의 "이미 다룬 Topic ID" 목록에 추가합니다.

Edit 도구로 preferences.md의 Topic ID 줄에 새 ID를 append합니다.
