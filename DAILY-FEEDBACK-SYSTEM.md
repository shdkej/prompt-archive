---
description: 출근, 퇴근 시 일일 회고 관리 시스템. 일일 업무 대화 관리 및 Obsidian/Google Drive 자동 문서화
argument-hint: (선택) 추가 메모 또는 "어제"
allowed-tools:
  ["Read", "Grep", "Glob", "Bash"]
---

# Daily Feedback System

하루를 관리하고 자동 문서화하는 스킬입니다.

---

## 설정

```yaml
mode: session # session | conversation
```

| 항목           | 값                                     |
| -------------- | -------------------------------------- |
| 사용자명       | seonghonoh                             |

### 프로젝트 분류

| 분류 | 경로 패턴      |
| ---- | -------------- |
| 업무 | `~/dev/`       |
| 개인 | `~/workspace/` |

> 설정 파일: `~/.claude/project-categories.json`

### Obsidian

| 항목       | 값                               |
| ---------- | -------------------------------- |
| Vault      | Obsidian (로컬)                  |
| Vault 경로 | `~/Obsidian`                     |
| 다이어리   | `~/Obsidian/diary/`              |
| 파일 형식  | `YYYY-MM.md` (월별 단일 파일)    |
| 항목 형식  | `## MM-DD` 헤더 아래 불릿 리스트 |
| 불릿 인덴트 | 스페이스 4칸                     |

### Google Drive

| 항목       | 값                                        |
| ---------- | ----------------------------------------- |
| CLI 도구   | `gog` (gogcli via Homebrew)               |
| 계정       | `shdkej@gmail.com`                        |
| 폴더       | `diary`                                   |
| 폴더 ID    | `1NiKzp9l9IHbQ2dOAN6cUd7qDDSyGyvDa`      |
| 업로드 내용 | 당일 리뷰 내용만 (전체 다이어리 파일 아님) |
| 파일 형식  | `YYYY-MM.md` (월별 단일 파일)             |

**업로드 방식**:

> **주의**: `gog drive download`는 `-o` 플래그를 지원하지 않음. 기본 다운로드 경로: `~/Library/Application Support/gogcli/drive-downloads/<fileId>_<filename>`

1. `/tmp/diary-YYYY-MM.md`에 당일 리뷰 내용만 추출하여 임시 파일 생성
2. Google Drive `diary` 폴더에 해당 월 파일(`YYYY-MM.md`)이 있는지 확인
   - 있으면: `gog drive download <파일ID>` → 기본 경로에서 파일 읽기 → 당일 내용 추가하여 `/tmp/diary-YYYY-MM.md` 생성 → `gog drive delete <파일ID> --force` → `gog drive upload /tmp/diary-YYYY-MM.md --parent <폴더ID> --name YYYY-MM.md`
   - 없으면: 당일 내용으로 `/tmp/diary-YYYY-MM.md` 생성 → `gog drive upload /tmp/diary-YYYY-MM.md --parent <폴더ID> --name YYYY-MM.md`
3. 임시 파일 및 다운로드 파일 삭제

### 도구

- Obsidian vault는 마크다운 파일 직접 읽기/쓰기로 접근합니다.
- Google Drive는 `gog` CLI를 사용하여 업로드합니다.

### 오프라인 데이터 소스

#### 1. Obsidian 모바일 Inbox (수동 캡처)

| 항목      | 값                                      |
| --------- | --------------------------------------- |
| 경로      | `~/Obsidian/diary/inbox.md`             |
| 캡처 방식 | 모바일에서 한 줄씩 빠르게 메모          |
| 형식      | 자유 형식 불릿 리스트 (타임스탬프 선택) |

**퇴근 시 처리**:

1. inbox.md 내용 읽기
2. 각 항목을 분류: 결정/인사이트/메모/TODO
3. 데일리 로그의 해당 섹션에 통합
4. 처리 완료 후 inbox 내용 비우기 (헤더만 남김)

#### 2. YouTube 시청 기록 (자동 수집)

| 항목      | 값                                                            |
| --------- | ------------------------------------------------------------- |
| 소스      | Chrome 브라우저 히스토리 DB                                     |
| DB 경로   | `~/Library/Application Support/Google/Chrome/Profile 1/History` |
| 추출 방식 | DB 복사 후 SQLite 쿼리 (Chrome 잠금 회피)                     |

**추출 쿼리**:

```sql
-- /tmp에 DB 복사 후 실행
SELECT title, url,
  datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time
FROM urls
WHERE url LIKE '%youtube.com/watch%'
  AND date(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') = date('now', 'localtime')
ORDER BY last_visit_time DESC;
```

**퇴근 시 처리**:

1. 당일 YouTube 시청 목록 추출
2. 영상 제목으로 주제 분류 (학습/뉴스/엔터테인먼트 등)
3. 데일리 로그의 "오늘 본 것" 섹션에 요약 추가

#### 3. Netflix 시청 기록 (자동 수집)

| 항목      | 값                                                            |
| --------- | ------------------------------------------------------------- |
| 소스      | Chrome 브라우저 히스토리 DB (YouTube와 동일)                   |
| 추출 방식 | DB 복사 후 SQLite 쿼리 (Chrome 잠금 회피)                     |

**추출 쿼리**:

```sql
-- /tmp에 DB 복사 후 실행
SELECT title, url,
  datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time
FROM urls
WHERE url LIKE '%netflix.com/watch%'
  AND date(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') = date('now', 'localtime')
ORDER BY last_visit_time DESC;
```

**퇴근 시 처리**:

1. 당일 Netflix 시청 기록 추출
2. title이 "넷플릭스"만 표시되는 경우, 같은 날 browse 페이지(`?jbv=`)의 title에서 작품명 매칭 시도
3. 작품명을 알 수 없으면 "Netflix 시청"으로만 기록
4. 데일리 로그의 "오늘 본 것" 섹션에 추가

---

## 트리거

### 출근

**트리거**: "좋은 아침~"

**동작**:

1. 새 하루 업무 시작 인식
2. 어제 회고 검색 (두 소스를 확인, 어느 쪽이든 있으면 표시)
   - **Obsidian**: `~/Obsidian/diary/YYYY-MM.md`에서 어제 날짜(`## MM-DD`) 항목의 `#### 회고` 섹션 읽기
   - 없으면 생략 (에러 아님)
3. **미완료 TODO 및 리마인드 검색**: 최근 3일간 다이어리 항목에서 미체크 TODO(`- [ ]`)와 '기타' 섹션의 생활 메모(예: "컵 들고오기") 중 아직 유효한 항목을 리마인드
4. 이전 대화는 참고용으로만 (과도한 참조 금지)
5. 오늘 주요 업무/목표 확인

**응답 형식**:

```markdown
## 좋은 아침!

### 어제 회고 ({날짜})

- Cut: {제거/위임한 것 또는 할 것}
- Core: {핵심 원인 한 줄}
- Logic: {적용 중인 새 규칙} `L-MMDD-순번`

### 리마인드
- {미완료 TODO 또는 기타 메모 중 유효한 항목}

### 오늘 어떤 작업을 할 예정인가요?
```

> 어제 회고 문서가 없으면 "어제 회고" 섹션은 생략하고 바로 오늘 목표를 물어본다.
> 리마인드 항목이 없으면 "리마인드" 섹션은 생략한다.

---

### 어제 업무 이어가기

**트리거**:

- "어제 업무에 이어서", "어제 작업 이어서"
- "어제 문서 확인해줘", "어제 업무 요약해줘"

**동작**:

1. 어제 날짜 계산 (주말 시 금요일로)
2. Obsidian 다이어리에서 어제 항목 검색
3. 요약 제공

**응답 형식**:

```markdown
## 어제 ({날짜}) 업무 요약

### 어제의 주요 내용

{요약}

### 오늘 이어갈 내용

{다음 액션}
```

---

### 퇴근

**트리거**:

- "퇴근할게~", "퇴근한다", "오늘 업무 끝"
- `/daily-feedback-system`

**지연 퇴근 트리거**:

- "어제 퇴근할게~", "퇴근 정리 깜빡했네"
- `/daily-feedback-system 어제`

#### 날짜 판별

| 시간대              | 판별            |
| ------------------- | --------------- |
| 오전 (09-12시)      | 전날 가능성 95% |
| 새벽 (00-06시)      | 전날 가능성 90% |
| 오후/저녁 (12-24시) | 당일 가능성 80% |

**애매한 경우**:

```
어느 날 업무 정리를 도와드릴까요?
1 - 어제({날짜}) 업무 정리
2 - 오늘({날짜}) 업무 정리
```

**금요일 퇴근 시 추가 제안**:
- 요일 판별 후 금요일이면 퇴근 처리 완료 후 1회 제안: "이번 주 정리도 할까요?"
- "응" → 주간 요약 실행
- "아니" / 무시 → 넘어감

---

### 주기별 요약

| 트리거             | 동작      |
| ------------------ | --------- |
| "이번 주 정리해줘" | 주간 요약 |
| "이번 달 정리해줘" | 월간 요약 |

---

## 퇴근 처리 모드

### Mode: session

**세션 수집 스크립트**: `~/workspace/prompt-archive/.agent/scripts/daily-sessions.py`

**처리**:

1. **오프라인 소스 수집**
   - Obsidian inbox (`~/Obsidian/diary/inbox.md`) 읽기 → 항목 분류 (결정/인사이트/메모/TODO)
   - Chrome 히스토리에서 당일 YouTube 시청 목록 추출 → 주제별 분류
2. 스크립트 실행하여 세션 목록 수집
   - 오늘: `python3 ~/workspace/prompt-archive/.agent/scripts/daily-sessions.py`
   - 어제: `python3 ~/workspace/prompt-archive/.agent/scripts/daily-sessions.py {어제날짜}`
   - 특정일: `python3 ~/workspace/prompt-archive/.agent/scripts/daily-sessions.py YYYY-MM-DD`
3. 스크립트 출력(프로젝트명, 분류, 사용자 메시지)을 기반으로 각 세션의 핵심 작업 요약
4. 필요시 개별 세션 JSONL 파일을 읽어 상세 내용 보강
5. **다이어리 '기타' 섹션 수집**: 당일 Obsidian 다이어리의 '기타' 항목을 읽어 인사이트(업무 외 깨달음, 아이디어)와 리마인드(생활 메모, 미완료 TODO)로 분류. 인사이트는 `#### 인사이트` 섹션에, 생활 메모는 `#### 리마인드` 섹션에 반영
6. **결정 맥락 추출 (Decision Context Extraction)**
   - 세션 대화 + Obsidian inbox 메모에서 의사결정 패턴 탐지: "A vs B", "고민", "선택", "결정", "트레이드오프", "이유는", "왜냐면", "대신" 등
   - 탐지된 결정마다 Context/Options/Decision/Reasoning/Trade-off 구조로 정리
   - **업무/개인 분류**: 세션의 프로젝트 분류(`~/dev/` → 업무, `~/workspace/` → 개인)를 기준으로 결정도 자동 분류. inbox 메모는 내용으로 판단
   - 결정이 없는 루틴 작업 세션은 "새로운 결정 없음"으로 표기
6. **회고 추출 - Minimalist Feedback Loop** (AI가 세션 내용 분석하여 초안 자동 생성)
   - **Cut** (Noise Reduction): 오늘 에너지를 갉아먹은 불필요한 변수 식별 → 내일 제거/위임 대상
   - **Core** (Data Extraction): 오늘 발생한 결과 중 인과관계가 가장 명확한 핵심 사건 → 성공/실패 원인을 한 줄로 정의
   - **Logic** (System Upgrade): 위 원인을 바탕으로 내일부터 적용할 시스템 규칙 업데이트 (Leverage 또는 Antifragile)
     - 새 Logic에 자동 ID 부여: `L-MMDD-순번` (예: `L-0309-1`)
     - MMDD는 해당 날짜, 순번은 당일 내 1부터 증가
7. **사용자 확인**: 결정 로그 + 회고 초안 + 오늘 본 영상을 함께 보여주고 "추가할 내용 있어?" 한 번만 물어봄
   - "없어" / "빠르게 넘어갈게" → 초안 그대로 사용
   - 추가 입력 → 반영
8. **기술 교훈 연동** (선택): 기술적 배움이 있으면 `lessons-learned.md` 적재 제안
   - "이 배움을 lessons-learned에 기록할까요?" → "응" → 적재
   - 강제 아님, 자연스럽게 제안만
9. **Obsidian 저장**: `~/Obsidian/diary/YYYY-MM.md`의 해당 날짜 항목에 작업 요약 + 회고 추가
   - 해당 날짜 항목(`## MM-DD`)이 이미 있으면 기존 내용 아래에 추가
   - 없으면 파일 최상단에 새 항목 생성
   - 헤드라인은 `#### 헤드라인` 하위에 하루를 한 줄로 요약 (예: "SSR 전환 결정한 날 — 속도가 전환율이다")
   - `#### 업무` 하위에 업무 세션 요약 + 업무 결정
   - `#### 개인` 하위에 개인 세션 요약 + 개인 결정
   - `#### 인사이트` 하위에 다이어리 '기타' 섹션의 업무 외 인사이트/메모 중 의미 있는 것 정리 (업무와 무관한 생활 메모는 `#### 리마인드`로 분류)
   - 오늘 본 영상은 `#### 오늘 본 것` 하위에 주제별 그룹핑 (개인 섹션에 포함)
   - 회고는 `#### 회고` 하위에 Cut/Core/Logic 형식으로 작성 (하루 전체 통합)
   - Logic에는 반드시 ID 포함: `Logic: {내용} \`L-MMDD-순번\``
   - **inbox.md 비우기**: 처리 완료 후 헤더만 남기고 내용 삭제
10. **Google Drive 업로드**: 당일 리뷰 내용(헤드라인 + 업무/개인 요약 + 회고)만 추출하여 `diary` 폴더에 월별 파일로 업로드
    - `gog drive ls --parent 1NiKzp9l9IHbQ2dOAN6cUd7qDDSyGyvDa`로 해당 월 파일 존재 여부 확인
    - 있으면: `gog drive download <파일ID>` (기본 경로: `~/Library/Application Support/gogcli/drive-downloads/`) → 기본 경로에서 파일 읽어 당일 내용 추가 → `gog drive delete <파일ID> --force` → `gog drive upload /tmp/diary-YYYY-MM.md --parent 1NiKzp9l9IHbQ2dOAN6cUd7qDDSyGyvDa --name YYYY-MM.md`
    - 없으면: 당일 내용으로 `/tmp/diary-YYYY-MM.md` 생성 → `gog drive upload /tmp/diary-YYYY-MM.md --parent 1NiKzp9l9IHbQ2dOAN6cUd7qDDSyGyvDa --name YYYY-MM.md`
    - 임시 파일 삭제
11. 전체 요약 터미널 출력

**스크립트가 없는 경우 수동 절차**:

1. `~/.claude/projects/*/` 에서 대상 날짜에 수정된 `.jsonl` 파일 탐색 (subagents 제외)
2. 각 JSONL 파일에서 `role: user`인 메시지의 텍스트 추출 (시스템 태그 `<` 시작 제외)
3. 프로젝트 디렉토리명에서 원래 경로 복원 (예: `-Users-seongho-noh-dev-kop-web` → `/Users/seongho-noh/dev/kop-web`)
4. `~/.claude/project-categories.json`의 patterns로 업무/개인 분류

**제외**: 코드 변경사항(git diff), 상세 코드

**출력**:

```markdown
# 오늘 작업 요약 - YYYY-MM-DD

## 업무 (Confluence 업로드됨)

- kop-web: 기능 A 구현

## 개인

- my-telegram-bot: 아키텍처 문서화
```

---

### Mode: conversation

**데이터 소스**: 당일 대화 내용

**Step 1**: 하루 요약

```markdown
## 오늘 하루 요약

- **주요 작업**: {핵심 업무}
- **완료사항**: {완료된 것}
- **진행사항**: {진행 중}
- **이슈/도전**: {문제점}
```

**Step 2**: Minimalist Feedback Loop (선택적)

1. **Cut**: "오늘 에너지를 갉아먹은 불필요한 변수가 있었어? 내일 제거하거나 위임할 건?"
2. **Core**: "오늘 결과 중 인과관계가 가장 명확한 핵심 사건은? 성공/실패 원인을 한 줄로 정리하면?"
3. **Logic**: "그 원인을 바탕으로 내일부터 적용할 새 규칙이 있어?"

> "빠르게 넘어갈게" → 회고 생략

---

## 문서 템플릿

### 일일 업무

**제목 형식**: `[MM/DD] {프로젝트1 주요작업} 및 {프로젝트2 주요작업}`

- 예: `[02/04] AI Legal Advisor UI 개선 및 Hybris 파일처리 로직 개선`

```markdown
# [MM/DD] {프로젝트1 주요작업} 및 {프로젝트2 주요작업}

## 오늘의 주요 논의사항

- {토픽}

## 오늘의 결정 (Decision Log) — 업무

> 무엇을 했는지보다 **어떤 고민 끝에 무엇을 결정했는지**가 미래의 나에게 더 가치 있다.

### 결정 1: {결정 제목} `#태그`

- **상황(Context)**: 어떤 문제/갈림길을 만났는가
- **선택지(Options)**: 어떤 대안들이 있었는가
- **결정(Decision)**: 무엇을 선택했는가
- **근거(Reasoning)**: 왜 이것을 선택했는가
- **트레이드오프(Trade-off)**: 이 결정으로 포기한 것, 감수한 리스크

<!-- 결정이 여러 개면 ### 결정 2, 3... 으로 추가 -->
<!-- 결정이 없는 날은 "오늘은 루틴 작업 위주, 새로운 결정 없음" 한 줄이면 충분 -->
<!-- Confluence에는 업무 결정만 포함. 개인 결정은 Obsidian에만 기록 -->

**태그 분류**:
| 태그 | 의미 |
|------|------|
| `#architecture` | 기술 구조, 설계 방향 |
| `#prioritization` | 우선순위, 무엇을 먼저/나중에 |
| `#tooling` | 도구, 라이브러리, 기술 선택 |
| `#process` | 프로세스, 워크플로우 변경 |
| `#communication` | 커뮤니케이션, 협업 방식 |
| `#scope` | 범위 결정, 커팅/확장 |
| `#tradeoff` | 성능 vs 편의 등 트레이드오프 |

<!-- 필요시 태그 추가 가능. AI가 대화 맥락에서 자동 제안 -->

## 진행 상황

- 완료: {완료 항목}
- 진행 중: {진행 항목}
- 이슈: {이슈}

## 다음 액션 아이템

- [ ] 단기 (1-3일)
- [ ] 중기 (1-2주)
- [ ] 장기 (1개월+)

## 내일 이어갈 내용

- {다음 주제}

## 오늘의 헤드라인

> **{하루를 한 줄로 요약하는 문장}**

## 오늘의 회고 (Cut - Core - Logic)

### Cut (Noise Reduction)

- {에너지를 갉아먹은 불필요한 변수} → **내일 액션**: {제거 또는 위임}

### Core (Data Extraction)

- {인과관계가 가장 명확한 핵심 사건}
- **원인 한 줄 정의**: {성공/실패의 근본 원인}

### Logic (System Upgrade)

- **새 규칙**: {내일부터 적용할 시스템 규칙} `L-MMDD-순번`
- **유형**: {Leverage(성공 복제) | Antifragile(실패 방어)}

---

**작성자**: seonghonoh
**작성일**: {날짜}
```

### 지연 정리

```markdown
# [MM/DD] {업무 내용} (늦은 정리)

## 작성 노트

> 이 문서는 {작성일}에 작성된 {업무일} 업무 정리입니다.

{일반 템플릿 내용}

---

**업무일**: {업무일} (늦은 정리)
```

### 주간 요약

**저장 위치**: Obsidian 월별 파일(`~/Obsidian/diary/YYYY-MM.md`) 내 인라인 삽입
- 해당 주의 마지막 일별 항목 바로 아래에 `## Week {주차}` 헤더로 삽입

**데이터 수집**: 해당 주의 일별 Obsidian 다이어리 항목들에서 헤드라인, 결정, 회고(Logic 포함)를 수집

```markdown
## Week {주차} ({시작일} ~ {종료일})

### 헤드라인 모음

| 날짜    | 헤드라인          |
| ------- | ----------------- |
| {MM/DD} | {그날의 헤드라인} |

### Logic 리뷰

> 이번 주 생성된 Logic이 실제로 적용되었는지 간단히 검증.

| ID | 규칙 | 실제 적용? | 계속? |
|----|------|-----------|-------|

**판정**: **유지** 또는 **폐기** (2단계만)

### 결정 돌아보기 (Decision Review)

> 1~2주 전 내린 결정 중 결과가 나온 것을 평가한다.

| 결정 (날짜)           | 당시 근거              | 결과                 | 평가                  |
| --------------------- | ---------------------- | -------------------- | --------------------- |
| {결정 제목} ({MM/DD}) | {왜 그렇게 결정했는지} | {실제 어떻게 됐는지} | {Good/Adjust/Reverse} |

### 이번 주 배움

- {내용}

### 다음 주 이어갈 것

- [ ] ...
```

**결정 패턴 분석** (월간 요약으로 이동):
- 태그 분포, 반복 패턴은 월간 요약에서 통합 분석

### 월간 요약

**저장 위치**: Obsidian 월별 파일(`~/Obsidian/diary/YYYY-MM.md`) 최하단에 인라인 삽입

**데이터 수집**: 해당 월의 주별 요약 + 일별 항목에서 Logic, 결정, Cut을 종합 수집

```markdown
## {년월} 월간 요약

### 이달의 헤드라인 Top 3

1. {가장 임팩트 있었던 하루의 헤드라인}
2. {두 번째}
3. {세 번째}

### Logic 현황

- 이달 생성: {N}개
- 유지 중: {목록}
- 폐기: {목록}

### 결정 패턴

- 태그 분포: {예: #architecture 8건, #prioritization 5건, ...}
- Good/Adjust/Reverse 비율: {N}% / {N}% / {N}%

### 다음 달 핵심 목표 Top 3

1. ...
2. ...
3. ...
```

---

## 예외 상황

### 기존 문서 존재 시

```
어제({날짜}) 문서가 이미 존재합니다.
1 - 기존 문서에 업데이트
2 - 새 문서로 생성
3 - 취소
```

### 연휴 후 복귀

```
며칠간 대화가 없었습니다. 어느 날 업무를 정리하시겠습니까?
- 1: {날짜1}
- 2: {날짜2}
- 3: 모두 넘어가기
```

---

## 날짜 계산

```javascript
// 한국 시간대
const koreaTime = new Date().toLocaleString("en-US", {
  timeZone: "Asia/Seoul",
});

// 주말 처리: 전날 계산 시
// 일요일(0) → 금요일로 (-2일 추가)
// 토요일(6) → 금요일로 (-1일 추가)
```

---

## 대화 관리 원칙

- **당일 대화**: 상세하게 기억, 지속 참조
- **이전 날**: 필요시만 간략 참조
- **문서화**: 당일 중심, 액션 지향, 간결성, 연속성

---

## 에러 처리

| 상황                 | 처리                          |
| -------------------- | ----------------------------- |
| 세션 파일 없음       | "오늘 작업한 세션이 없습니다" |
| Confluence 연결 실패 | 로컬에 요약 출력              |
| 설정 파일 없음       | 기본값 사용                   |
