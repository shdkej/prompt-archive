---
name: tool-curator
description: ClawHub·Product Hunt 등에서 사용자 워크플로우에 맞는 AI 도구와 에이전트 스킬을 찾아 비교한다. 도구 추천, 개방성·확장성 평가, 반복 큐레이션이나 발견 작업의 cron 설계를 요청할 때 사용한다.
---

# Tool Curator

**목차**

- [정본 구조](#정본-구조)
- [핵심 아이디어와 평가 기준](#핵심-아이디어와-평가-기준)
- [소스 역할](#소스-역할)
- [소스 접근 플레이북](#소스-접근-플레이북)
- [반복 실행 계약](#반복-실행-계약)
- [출력 스타일](#출력-스타일)
- [저장 산출물](#저장-산출물)

이 skill은 단순히 "도구를 찾는" 작업이 아니라 "이 사용자의 작업 방식과 운영 기준에 맞는 적절한 도구를 찾는" 작업일 때 사용하세요.

## 정본 구조

반복 실행이 따르는 규칙 원본은 아래와 같이 한 곳씩만 둔다. 규칙을 고칠 때는 정본만 고치고, 다른 위치에 같은 규칙을 복제하지 않는다.

- **실행 규칙 정본: 이 파일** — 소스, 선별, 상한, 발송, 단언, 최종 라인까지 반복 실행의 전 계약.
- **시각 템플릿 정본**: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/tool-curator/fixed-template-email.html` (canonical HTML) + `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/tool-curator/fixed-template.md` (잠금 규칙 요약). 색·구조·잔디 체계·모바일 padding 등 시각 디테일은 저 두 파일이 정답이며 여기 복제하지 않는다.
- **사건 이력**: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/content/TOOL_CURATION_WORKFLOW.md` — 목적과 날짜별 장애/복구 기록. 규칙이 아니라 근거 보관소다.
- **점수 차원/저장된 워크플로우 형태**: `references/criteria.md`, `references/workflow.md`.

## 핵심 아이디어와 평가 기준

도구 발견을 검색 문제가 아니라 큐레이션 문제로 다루세요.

사용자가 중요하게 보는 것:
- 연결 및 확장 잠재력 (API + MCP + 플러그인/확장성 + 채팅방 통합)
- 문서 품질
- 비용
- 유지보수성 / 배포 표면(deployment surface)
- 보안
- 코드 단순성
- 접근성
- 수익화 가능 표면
- 차별적 강점

사용자는 특히 AI 도구를 더 쉽게 발견하고 실생활에서 실제로 더 쉽게 사용하도록 만드는 제품에 관심이 많습니다.

### 기본 선별 모드: 현실 모드

핵심 4축은 연결성과 확장성, 보안, 수익화 가능성, 특장점이다. 4개 중 3개 이상이 `높음`이고 나머지 1개가 최소 `중간`일 때 후보를 통과시키세요. 목록이 부족하게 채워지기 전에 더 많은 목록·랭킹·페이징·집중 쿼리로 더 넓은 검색 패스를 수행하고, 그 뒤에도 빈약하다면 약한 항목으로 채우기보다 더 나은 항목을 적게 보내는 쪽을 선호하세요.

## 소스 역할

- **ClawHub**: 에이전트와 운영 워크플로우를 위한 실용적인 skill/스토어 레이어 → 설치 가능한 운영 역량에 가까움
- **ClawSkills**: `https://clawskills.sh`의 OpenClaw/에이전트 skill 발견 표면 → OpenClaw 호환 skill 후보에 가까움. ClawHub와 중복되면 억지로 채우지 말고 설치 가능성/문서/보안 근거가 나은 쪽만 남긴다.
- **LobeHub Skills**: `https://lobehub.com/skills`의 skill/플러그인 패턴 소스 → 패키징된 skill UX, 카테고리, 재사용 패턴. 사용자의 OpenClaw/Infinity/Knowledge Lab 워크플로우에 실제 연결될 때만 추천.
- **OpenHunt**: 새 AI 제품 발견/피드 레이어 → AI 네이티브 트렌드와 제품 스카우팅
- **Product Hunt**: 주류 출시/랭킹 레이어 → 트랙션, 포지셔닝, 메이커/커뮤니티 신호. 단독 인기보다 현실 모드 기준 통과 후보만.

## 소스 접근 플레이북

발견과 근거를 분리하세요. 후보는 피드, CLI, 랭킹 페이지, 검색 결과에서 발견될 수 있지만, 읽을 수 있는 웹 근거 소스를 최소 하나 열어 본 뒤에야 추천이 됩니다.

- **ClawHub**
  - 발견: `clawhub explore --sort newest --limit 30 --json`, 실패하면 `trending`으로 1회 재시도, 필요 시 `search` 최대 2회. ClawHub CLI v0.5.0의 유효한 sort 값은 `newest`, `downloads`, `rating`, `installs`, `installsAllTime`, `trending`이며 `--sort latest`는 유효하지 않다.
  - 상세 URL: 소스가 제공한 URL을 우선 사용하고, 없으면 `https://www.clawhub.io/skill/<slug>`. `clawhub.run`은 절대 쓰지 않는다.
  - 대체 근거: 상세/소스 메타데이터의 저장소/홈페이지/문서/패키지 URL.
  - 검증: 엄격한 TLS가 실패하지만 제한된(bounded) 완화 리다이렉트가 HTTP 200을 반환하면 `link_verified=tls-relaxed`로 기록하고 정규 URL 사용 가능.
  - 보류 조건: CLI JSON만 있고 열 수 있는 상세/문서/저장소 근거가 없을 때. `clawhub explore --json` 메타데이터(`slug`, `displayName`, `summary`, `description`, `stats`, `latestVersion.changelog`)는 발견에는 유용하지만 최종 추천 근거로는 부족하다.
  - 후보별 `inspect --files --json` 반복은 금지, 기본 `inspect --json` 또는 리스트 메타데이터를 우선.
- **ClawSkills**
  - 발견: `https://clawskills.sh`의 카테고리/검색/목록 페이지를 제한된 fetch나 검색 스니펫으로.
  - 상세 URL: 개별 skill 페이지. 대체 근거: 연결된 GitHub/문서/홈페이지/소스 패키지 페이지.
  - 보류 조건: 홈페이지/카테고리 개수만 보이고 항목 단위 근거를 열 수 없을 때.
- **LobeHub Skills**
  - 발견: `https://lobehub.com/skills`의 목록/카테고리 페이지와 집중 검색.
  - 상세 URL: 특정 skill 페이지. 대체 근거: manifest, 플러그인 페이지, 저장소, 문서.
  - 보류 조건: 넓은 목록 메타데이터만 읽히고 후보 상세를 검증할 수 없을 때.
- **OpenHunt**
  - 발견: `https://openhunt.dev/` (→ `https://www.openhunt.dev/` 정상 리다이렉트), Launch Calendar, Upcoming Products, Weekly Rankings. `https://openhunt.ai/`는 반복 타임아웃, `www.openhunt.ai`는 DNS 미해석, `https://openhunts.com/`은 별개 사이트이므로 쓰지 않는다.
  - 상세 URL: 개별 제품 페이지. 대체 근거: 공식 제품 사이트, GitHub/문서, 메이커/소스 페이지.
  - 보류 조건: 스켈레톤/앱 셸만 렌더링되고 공식 근거를 열 수 없을 때.
- **Product Hunt**
  - 발견: 랭킹/검색 페이지, 가벼운 검색 스니펫, 접근 가능한 제품 URL.
  - 상세 URL: 차단되지 않았다면 Product Hunt 제품 페이지. 대체 근거: 공식 제품 사이트, 문서, GitHub, 변경 로그, 메이커/회사 페이지.
  - 보류 조건: Cloudflare 차단 + 도달 가능한 공식 근거 없음.

소스가 차단되면 cron 예산 전체를 들여 무리하게 뚫지 마세요. `source_blocked=<source>: <reason>`을 기록하고, 대체 근거 경로를 한두 번 시도한 뒤, 열어 본 대체 근거를 바탕으로 추천하거나 보류 카드로 강등하세요.

검색 규율: 얕은 결과 한 세트에서 멈추지 말고, 목록/랭킹 페이지와 더 깊은 페이징을 쓰며, 강한 후보가 안 보이면 소스가 약하다고 결론짓기 전에 집중 쿼리 클러스터로 스캔을 넓히세요.

## 반복 실행 계약

반복(cron) 실행이 따르는 전 계약이다. 기본 모드는 `NORMAL_BOUNDED`.

### 소스 패스와 상한

1. ClawHub를 먼저 확인한다.
2. skill 소스(ClawSkills 또는 LobeHub) 최소 1개를 가볍게 확인한다.
3. 제품/소스 신호(OpenHunt 또는 Product Hunt) 최소 1개를 가볍게 확인한다.
- 총 최종 추천 최대 6개, 실용 목표 3~5개. ClawHub 최대 3개, ClawSkills/LobeHub 각 최대 1개, OpenHunt/Product Hunt 합산 최대 2개.
- 보류 카드는 메일을 보낼 때만 최대 3개. 모든 소스가 약하면 보류 카드만 모아 보내지 말고 `NO_REPLY`.
- 리서치 예산 약 4분, 전체 실행 약 6분. HTML 작성 전 리서치가 4분을 넘기면 후보 수를 줄이고 작성/발송으로 넘어간다.

### 실행 안전 규칙

- `python`, `python3`, `node`, `ruby`, `perl`, heredoc(`<<`), 생성된 임시 스크립트, 여러 줄 스크립트 조립, `npx`를 반복 실행 안에서 쓰지 않는다. HTML 조립은 고정 템플릿 복사와 작은 직접 편집만 사용한다. 그 방식으로 안전하게 끝낼 수 없으면 `SKIPPED`나 `NO_REPLY`로 마무리한다.
- 웹페이지 원문 전체를 컨텍스트에 덤프하지 않는다. 제한된 fetch/검색/페이지 스니펫만 사용한다.
- 어떤 도구 호출이 실패하더라도 크론 실패로 전파하지 말고, 남은 근거로 작게 마무리하거나 `NO_REPLY`를 반환한다.

### 웹 근거 규칙 (링크 검증 canonical)

- CLI/JSON/검색/랭킹 메타데이터는 발견과 1차 필터링에만 사용한다.
- 모든 최종 추천에는 열어 본 웹 근거 소스가 최소 하나 있어야 한다: 상세 페이지, 공식 문서, 저장소, README, 변경 로그, 제품 페이지, 출처 기사, 또는 이에 준하는 읽을 수 있는 소스.
- 추천 본문에는 그 근거에서 학습한 내용이 담겨야 하며, 피드/CLI 요약 필드 복사만으로 채우지 않는다.
- 열 수 있는 근거가 없는 후보는 `hold_reason=<candidate>: no opened web evidence`로 보류 카드/실행 노트에 내리고 추천으로 승격하지 않는다.

### 부분 소스 실패

- Product Hunt Cloudflare 차단, OpenHunt 약한 근거, ClawSkills/LobeHub 접근 실패 같은 단일 보조 소스 문제는 전체 메일 스킵 사유가 아니다.
- 어느 소스든 열린 웹 근거를 가진 강한 후보가 하나라도 있으면 고정 템플릿 메일을 보내고, 막힌 소스는 같은 HTML 톤의 보류 카드나 run note로 남긴다.
- `SKIPPED`는 강한 후보가 0개이거나 Gmail 발송 경로가 막혔거나 고정 템플릿을 안전하게 쓸 수 없을 때만 사용한다.

### 발송 경로와 산출물

- 기본 반복 출력은 채팅이 아니라 HTML 이메일이다. 발송 경로: `gog gmail send --to shdkej@gmail.com --subject "<subject>" --body-html-file <html_file> --no-input --json`. 사용자가 명시적으로 허용하지 않는 한 일반 텍스트 대체(fallback) 메일을 보내지 않는다.
- HTML 파일과 run note는 이메일 발송 전에 먼저 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/tool-curator/runs/`에 타임스탬프 프리픽스로 저장한다. 발송 실패 시에도 산출물 경로를 남기고 반복 재시도하지 않는다.
- run note 필수 필드: `mode=`, 확인한 소스, 보류/차단 소스와 사유, 선정 후보, 링크 검증 상태, 모든 추천의 `evidence_url=<candidate>: <url>` + `evidence_note=<candidate>: <요지>`, 산출물 경로, 발송 시 Gmail messageId.

### 발송 전 단언 (assert)

- 최종 HTML을 발송 전에 직접 점검한다.
- 최종 추천 수 = 클릭 가능한 제목 링크 수 = run note에 기록된 opened evidence URL 수. 하나라도 어긋나면 발송하지 않고 `SKIPPED: web evidence assertion failed`로 끝낸다.
- 포맷 점검: HTML, 잔디 존재, `잔디 → 특장점 → 본문` 순서, 실용적 밀도, 얕은 압축 없음. 요구 구조와 시각적 풍부함을 충족하지 못하면 저하된 이메일을 보내지 말고 충족할 때까지 다듬거나 `NO_REPLY`로 건너뛴다.

### 완료 계약

- 반복 실행의 최종 응답은 반드시 아래 중 하나의 단일 라인으로 끝낸다. 도구 호출 후 최종 응답 없이 멈추지 않으며, 불확실하거나 시간이 부족하면 즉시 `SKIPPED` 또는 `NO_REPLY`를 선택한다.
  - `SENT: <제목> | ClawHub N, ClawSkills N, LobeHub N, OpenHunt N, ProductHunt N | mode <모드> | artifacts <경로> | gmail <messageId 또는 json 경로>`
  - `SKIPPED: <짧은 이유> | mode <모드> | artifacts <경로(있으면)>`
  - `NO_REPLY`

### 복구 모드 (RECOVERY_MINIMAL)

실제 실패 직후에만 임시로 쓴다. 폭보다 종료 신뢰성 우선: 최종 추천 최대 3개(ClawHub 최대 2, skill 소스 합산 1, 제품 소스 합산 1), 상세 확인 최대 2개, 보류 카드 최대 1개, 브라우저/`npx` 금지, 리서치 2분/전체 4분 이내. 3회 연속 정상 종료(`SENT`/`SKIPPED`/`NO_REPLY`) 후에는 다음 실행부터 `NORMAL_BOUNDED`로 복귀해야 하며, 그 뒤에도 복구 모드를 계속 쓰는 것은 운영 버그다. 진입/종료 근거는 run note에 남긴다.

## 출력 스타일

한국어로 답하세요. 반복 출력은 서비스 설명 메모가 아니라 큐레이션 전달물이어야 합니다.

구조:
1. 무엇을 검색했는지 아주 짧은 요약
2. 소스별 추천 (각 최대 5개, 반복 실행은 위 상한 우선)
3. 각 항목은 이 순서로: 신뢰할 수 있는 URL이 있을 때는 링크된 제목 → 잔디/블록 지표 → 차별적 강점 → 본문
4. 보안은 모든 항목에 대해 항상 명시적으로 확인. 보안 단락은 `웹 근거 확인`, `제한적 근거`, `보류`를 구분하고, 메타데이터만으로 완전한 검토를 암시하지 않는다.
5. 다음 의사결정에 도움이 될 때만 짧은 종합

잔디/지표:
- 잔디는 기준별 상/중/하 레벨을 나타내는 작은 정사각형 블록 표시다. 텍스트 라벨이나 다른 시각 비유로 재해석하지 않고, 잔디 박스 안에 `상`/`중`/`하` 글자를 쓰지 않는다.
- `문서화의 정도`는 고정 지표로 포함하고, 신뢰할 근거가 있을 때 접근성, 비용, 코드 단순성/품질을 추가해 대략 5~6개 실용 지표를 보여준다. HTML에서는 잔디를 시각적으로 렌더링하고 plain text 나열로 퇴화시키지 않는다.
- 높음/중간/낮음/불명의 단순한 레벨 체계를 쓰고, 불확실한 차원은 불명으로 표시한다.

제목/링크:
- 신뢰할 수 있는 소스/상세 URL이 있으면 보이는 제목을 `<a href="..." target="_blank" rel="noopener noreferrer">`로 클릭 가능하게 만든다. URL을 지어내지 않으며, 보류 카드나 불확실한 항목은 plain text로 둔다.

템플릿:
- 시각 체계(배경, 헤더, 카드 계층, 잔디, 모바일 density)는 정본 `fixed-template-email.html` / `fixed-template.md`를 그대로 따른다. 매 실행 새 템플릿을 발명하지 말고 후보 내용만 갈아끼운다.
- OpenHunt/Product Hunt 근거가 약한 날도 섹션을 없애거나 모호한 산문으로 대체하지 말고, 같은 HTML 스타일의 짧은 보류 카드를 명시한다.

톤:
- 각 항목은 짧지만 지나치게 얕지 않게: 왜 중요한지, 어떤 적합성인지, 어떤 불확실성이 남는지. 특장점 노트는 점수가 아니라 말로 최소 하나.
- "통합 개방성" 같은 기술적 포괄 라벨 대신 "연결성과 확장성"처럼 비개발자도 이해하는 표현을 쓴다.
- 사용자가 명시적으로 전략/서비스 설계를 요청하지 않는 한 전달물을 넓은 개념 에세이로 만들지 않는다.
- 동일한 추천을 너무 자주 반복하지 않고, 사용자의 현재 워크플로우에 연결되는 도구를 선호하며, 의미 있게 좋은 것이 없으면 `NO_REPLY`.

## 저장 산출물

- 실행 노트 / 스냅샷 / 발송 HTML: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/tool-curator/` (반복 실행은 `runs/` 하위)
- 지속적인 큐레이션 기준이나 재사용 가능한 점수 노트: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/`
