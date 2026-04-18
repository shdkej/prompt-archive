---
description: 출근, 퇴근 시 일일 회고 관리 시스템. 일일 업무 대화 관리 및 Google Drive 자동 문서화, 추가 메모 또는 "어제", "퇴근", "회고", "리뷰", "정리", "좋은 아침" 등 트리거
argument-hint: (선택) 추가 메모 또는 "어제", "퇴근", "회고", "리뷰", "정리", "좋은 아침"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "AskUserQuestion"]
---

# Daily Feedback System

하루를 관리하고 자동 문서화하는 스킬.

> **저장 정책**: 회고/주간/월간 산출물은 **Google Drive에만 저장**. Obsidian diary 파일에는 쓰지 않는다.
> **Obsidian 읽기 정책**: Obsidian은 단순 맥락 보완용이 아니라 **하루 업무 내역·고민·결정 맥락을 파악하는 핵심 입력**이다. 퇴근 회고 시 당일 다이어리·inbox·관련 노트를 **반드시** 읽고 반영한다 (전일 회고 참조, 리마인드 검색, inbox 캡처, 업무 내역, 고민/결정 포인트, 기타/인사이트 수집).

## 설정

### 프로젝트 분류

- 업무: `~/dev/` / 개인: `~/workspace/`
- 설정 파일: `~/.claude/project-categories.json`

### Obsidian (읽기 전용, 적극 활용)

- Vault: `~/Obsidian` (로컬), 다이어리: `~/Obsidian/diary/`
- 파일: `YYYY-MM.md` (월별 단일), 항목: `## MM-DD` 헤더 + 스페이스 4칸 불릿
- **쓰기 금지** (inbox.md 비우기만 예외)
- **읽기는 회고 품질의 핵심 입력** — 다음을 반드시 수집:
  - 당일 `## MM-DD` 섹션: 업무 진행 내역, 작업 메모, 진행 중 고민
  - inbox.md: 모바일에서 캡처한 결정/인사이트/TODO
  - 연결된 노트 (필요 시): 오늘 수정되거나 당일 업무와 관련된 Obsidian 노트
  - 전일/과거 회고: 리마인드·이어가야 할 맥락

### Google Drive (주 저장소)

- CLI: `gog` (gogcli via Homebrew), 계정: `shdkej@gmail.com`
- 폴더: `diary` (`1NiKzp9l9IHbQ2dOAN6cUd7qDDSyGyvDa`)
- 파일 형식: `YYYY-MM.md` (월별 단일), 당일/주간/월간 내용 모두 포함

**업로드 절차** (퇴근 12번 참조):

> `gog drive download`는 `-o` 미지원. 기본 경로: `~/Library/Application Support/gogcli/drive-downloads/<fileId>_<filename>`

1. `gog drive ls --parent <폴더ID>`로 월 파일 존재 여부 확인
2. **있음**: `download` → 기본 경로 읽기 → 당일 내용 append(또는 주간/월간 인라인 삽입) → `/tmp/diary-YYYY-MM.md` 저장 → `delete <파일ID> --force` → `upload /tmp/diary-YYYY-MM.md --parent <폴더ID> --name YYYY-MM.md`
3. **없음**: 당일 내용으로 `/tmp/diary-YYYY-MM.md` 생성 → `upload`
4. 임시 파일/다운로드 파일 정리

### 날짜 판별

한국 시간대(`Asia/Seoul`). 주말이면 전날=금요일.

- 오전(09-12) / 새벽(00-06): 전날 가능성 높음
- 오후/저녁(12-24): 당일 가능성 높음
- 애매하면 `AskUserQuestion`으로 "어제 / 오늘" 선택지 제시

### 오프라인 데이터 소스

#### 1. Obsidian 모바일 Inbox

- 경로: `~/Obsidian/diary/inbox.md`
- 모바일에서 자유 형식 불릿 메모 (타임스탬프 선택)

**처리 절차** (퇴근 1번, 11번 참조):

1. inbox.md 읽기
2. 결정/인사이트/메모/TODO 분류
3. 당일 Google Drive 로그 해당 섹션에 통합
4. 처리 완료 후 inbox 비우기 (헤더만 남김) — **예외적으로 허용되는 Obsidian 쓰기**

#### 2. 미디어 시청 기록 (Chrome 히스토리 — YouTube, Netflix 통합)

- DB: `~/Library/Application Support/Google/Chrome/Profile 1/History`
- 추출 방식: DB를 `/tmp`에 복사 후 SQLite 쿼리 (Chrome 잠금 회피)

**추출 쿼리**:

```sql
SELECT
  CASE
    WHEN url LIKE '%youtube.com/watch%' THEN 'YouTube'
    WHEN url LIKE '%netflix.com/watch%' THEN 'Netflix'
  END AS platform,
  title, url,
  datetime(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') as visit_time
FROM urls
WHERE (url LIKE '%youtube.com/watch%' OR url LIKE '%netflix.com/watch%')
  AND date(last_visit_time/1000000-11644473600, 'unixepoch', 'localtime') = date('now', 'localtime')
ORDER BY last_visit_time DESC;
```

**처리 절차** (퇴근 1번 참조):

1. 당일 시청 기록 추출 (플랫폼별 자동 분류)
2. 제목으로 주제 분류 (학습/뉴스/엔터테인먼트 등)
3. Netflix title이 "넷플릭스"만 나오면 같은 날 `?jbv=` browse 페이지에서 작품명 매칭, 실패 시 "Netflix 시청"
4. 당일 로그 "오늘 본 것"에 플랫폼별 그룹핑

> 플랫폼 추가: CASE + WHERE 절에 `url LIKE '%{도메인}%'` 추가

---

## 트리거

### 출근 — "좋은 아침~"

1. 새 하루 시작 인식
2. **전일 리뷰 존재 확인**
   - **Google Drive** `YYYY-MM.md` 다운로드 → 어제 `## MM-DD` → `#### 회고` 확인
   - 보조 참조: `~/Obsidian/diary/YYYY-MM.md` (읽기 전용, 있으면 참고)
   - **없으면**: "어제({날짜}) 리뷰가 아직 없네요. 먼저 정리하고 시작할게요." → [§ 퇴근 처리](#퇴근-처리)를 어제 날짜로 실행 (지연 정리 모드: 제목 "(늦은 정리)") → 사용자 확인은 간소화 (`AskUserQuestion` 1~2개 또는 "패스" 선택지) → Google Drive 저장 후 3번 진행
   - **있으면**: 그대로 응답에 포함
3. **리마인드**: 최근 3일 Google Drive(+ Obsidian 보조)의 미체크 TODO(`- [ ]`) 및 '기타' 섹션 생활 메모 중 유효한 항목
4. 이전 대화는 참고용만 (과도한 참조 금지)
5. 오늘 주요 업무/목표 확인

**응답 형식**:

```markdown
## 좋은 아침!

### 어제 회고 ({날짜})

- Cut: {반복 패턴 — 있을 때만}
- Core: {어떤 상황에서 어떤 판단}
- Logic: {삶에 남기는 규칙 — 있을 때만} `L-MMDD-순번`

### 리마인드

- {미완료 TODO 또는 유효한 생활 메모}

### 오늘 계획

> 다이어리에 오늘 할 일이 있으면 테이블로, 없으면 "오늘 어떤 작업을 할 예정인가요?"

| #   | 작업     | 완료 상태        | 예상 시간 |
| --- | -------- | ---------------- | --------- |
| 1   | {작업명} | {Done 정의}      | {소요}    |

- 블로커(외부 의존/확인) 작업은 오전 우선 제안
- 합계 시간 표시로 하루 분량 감각 제공
```

> 리마인드 없으면 해당 섹션 생략.

### 퇴근

- **일반**: "퇴근할게~", "퇴근한다", "오늘 업무 끝", "오늘 리뷰", "오늘 정리", `/daily-feedback-system`
- **지연**: "어제 퇴근할게~", "퇴근 정리 깜빡했네", `/daily-feedback-system 어제`
- **금요일 추가 제안**: 퇴근 처리 완료 후 1회 `AskUserQuestion`으로 "이번 주 정리도 할까요?" 제시 (예→주간 요약, 아니오→넘어감)

### 주기별 요약

- "이번 주 정리해줘" → 주간 요약
- "이번 달 정리해줘" → 월간 요약

---

## 퇴근 처리

**세션 수집 스크립트**: `~/workspace/prompt-archive/scripts/daily-sessions.py`

1. **오프라인 소스 수집** ([§ 오프라인 데이터 소스](#오프라인-데이터-소스) 참조) — Obsidian inbox 처리 + Chrome 미디어 시청 기록 추출
2. **세션 수집 스크립트 실행**
   - 오늘: `python3 ~/workspace/prompt-archive/scripts/daily-sessions.py`
   - 어제/특정일: `python3 ~/workspace/prompt-archive/scripts/daily-sessions.py YYYY-MM-DD`
3. **Session Log 기록**: 출력(프로젝트명/분류/사용자 메시지) 기반 핵심 작업 요약을 일일 템플릿 "오늘의 작업 목록" 테이블(업무/개인/기타)에 **반드시 포함**. Google Drive 업로드 대상에 포함.
4. 필요 시 개별 JSONL 읽어 상세 보강
5. **Obsidian 다이어리 전체 읽기** (읽기 전용, 필수): 당일 `~/Obsidian/diary/YYYY-MM.md`의 `## MM-DD` 섹션 + `inbox.md` + 당일 수정된 관련 노트를 읽어서 다음을 모두 수집·반영:
   - **업무 내역**: 세션 로그에 빠진 작업/메모를 "오늘의 작업 목록" 보강
   - **고민/질문**: 진행 중이던 의사결정, 미결 고민 → `#### 논의사항` 또는 결정 로그 Context로 반영
   - **결정 포인트**: 다이어리에 적힌 결정/선택 → 결정 로그에 병합 (6번 Decision Context와 병행)
   - **인사이트**: 업무 외 깨달음/아이디어 → `#### 인사이트`
   - **생활 메모/리마인드**: `#### 리마인드`
   - Obsidian에 아무것도 없으면 "Obsidian 입력 없음"으로 기록하고 넘어감
6. **결정 맥락 추출 (Decision Context Extraction)**
   - 패턴 탐지: "A vs B", "고민", "선택", "결정", "트레이드오프", "이유는", "왜냐면", "대신"
   - 각 결정마다 Context/Options/Decision/Reasoning/Trade-off 정리
   - 업무/개인은 프로젝트 경로(`~/dev/` 업무, `~/workspace/` 개인). inbox는 내용으로 판단
   - 없으면 "새로운 결정 없음"
7. **회고 추출 (Life Feedback Loop)** — 헤드라인/Cut/Core/Logic 초안. 품질 기준은 [§ 회고 품질 기준](#회고-품질-기준) 참조
8. **Planner Agent 리뷰**: `Agent(subagent_type="planner", prompt=...)`
   - 전달: `~/workspace/prompt-archive/review-patterns.md` (톤/취향 패턴 — **먼저 읽기**), 회고 초안, 최근 7일 회고
   - planner가 Good/Bad 기준으로 검증·개선. "충분히 좋다"면 통과
9. **사용자 확인 (AskUserQuestion 선택창)**: 결정 로그 + planner 개선 회고 + 오늘 본 영상을 먼저 보여준 뒤, `AskUserQuestion` 도구로 맥락 질문 2~4개를 한 번에 제시

   **질문 생성 가이드**:
   - **빠뜨린 결정**: 세션의 선택지 논의 중 결정 로그 미반영 (예: "첨부파일 방식 결론이 났나요?")
   - **후속 맥락**: 완료 작업의 다음 단계 (예: "배포는 언제 예정?")
   - **감정/에너지**: 하루 흐름 소감 (예: "컨텍스트 스위칭 부담됐나요?")
   - **연결 인사이트**: 세션 간 연결점 (예: "A 메모와 B 설계가 연결되는 것 같은데 의도한 건가요?")

   **각 질문 구성**:
   - `header`: 질문 주제 짧게 (예: "첨부파일 결정")
   - `question`: 실제 질문 문장
   - `multiSelect`: false (대개 단일 선택)
   - `options`: 2~4개 선택지 + 필요 시 자유 입력은 Other 활용
     - 예: `[{label: "네, 결정됨", description: "..."}, {label: "아직 고민 중"}, {label: "해당 없음"}]`

   **저장 선택 질문**(마지막에 항상 포함):
   - `header`: "저장 방식"
   - `question`: "이대로 저장할까요?"
   - `options`: `[{label: "이대로 저장"}, {label: "회고 수정 후 저장"}]`

   **처리**:
   - 맥락 질문 답변 → 결정 로그/회고/인사이트에 반영
   - "이대로 저장" → planner 초안을 Good 패턴으로 `review-patterns.md`에 추가
   - "회고 수정 후 저장" → 수정 내용 입력받고 원본=Bad, 수정본=Good, 거부 이유를 `review-patterns.md`에 기록
10. **Workflow Log Lesson-Learned**: `~/.claude/logs/`에서 당일 로그 수집
    - 패턴: `workflow_YYYY-MM-DD_*.log`, `troubleshooting_YYYY-MM-DD_*.log`
    - workflow → `[WORKFLOW:LEARNING]` 섹션, troubleshooting → 문제/원인/해결
    - 분류: **도구/프레임워크 TIL**, **프로세스 개선**, **실수 방지**
    - CLAUDE.md Lesson Learn에 추가할 만하면 별도 제안
    - 로그 없으면 단계 생략
11. **Obsidian inbox.md 비우기** (헤더만 남김) — Obsidian 쓰기 중 예외적으로 허용되는 유일한 동작
12. **Google Drive 업로드** — 당일 리뷰(Session Log + 결정 + 회고 + Lesson-Learned) 전체를 [§ Google Drive](#google-drive-주-저장소) 절차로 월별 파일에 반영
13. 전체 요약 터미널 출력 (lesson-learned 포함)
14. 업무 외 항목(영상 경향/인사이트, 일상 리듬/생활 회고)도 가능하면 회고에 반영

**스크립트 없을 때 수동**:

1. `~/.claude/projects/*/`에서 대상 날짜 수정된 `.jsonl` 탐색 (subagents 제외)
2. `role: user` 메시지 텍스트 추출 (시스템 태그 `<` 시작 제외)
3. 디렉토리명에서 경로 복원 (예: `-Users-seongho-noh-dev-kop-web` → `/Users/seongho-noh/dev/kop-web`)
4. `~/.claude/project-categories.json` patterns로 업무/개인 분류

**제외**: 코드 변경사항(git diff), 상세 코드

---

## 회고 품질 기준

> **핵심 원칙**: 기술 디테일이 아니라 **상황-판단-결과의 맥락**을 기록.
> **Good/Bad 예시·톤 패턴**: `~/workspace/prompt-archive/review-patterns.md` (planner 리뷰 시 필독)

- **헤드라인**: 상황(갈등/도전) + 대응. 작업 나열 X
- **Cut**: 행동/판단의 반복 패턴. 기술 실수 나열 X. 없는 날 생략
- **Core**: 의사결정 전환점(상황→판단→결과). 작업 후기 X
- **Logic**: 진짜 배운 것만. 매일 강제 X. ID: `L-MMDD-순번`

---

## 문서 템플릿

> 모든 산출물의 최종 저장소는 **Google Drive** `YYYY-MM.md`.

### 일일 업무

**제목**: `[MM/DD] {프로젝트1 주요작업} 및 {프로젝트2 주요작업}`

- 예: `[02/04] AI Legal Advisor UI 개선 및 Hybris 파일처리 로직 개선`

```markdown
# [MM/DD] {프로젝트1 주요작업} 및 {프로젝트2 주요작업}

## 오늘의 작업 목록 (Session Log)

> `daily-sessions.py` 출력 기반. 프로젝트별/분류별 세션과 핵심 메시지 1~2줄. 무엇을 했는지 추적 가능하도록 **반드시 포함**.

### 업무

| # | 프로젝트 | 시간 | 주요 작업 |
|---|---------|------|----------|
| 1 | {프로젝트} | {HH:MM} | {1줄 요약} |

### 개인

| # | 프로젝트 | 시간 | 주요 작업 |
|---|---------|------|----------|
| 1 | {프로젝트} | {HH:MM} | {1줄 요약} |

### 기타

- {HH:MM} — {작업 요약}

## 오늘의 주요 논의사항

- {토픽}

## 오늘의 결정 (Decision Log) — 업무

> 무엇을 했는지보다 **어떤 고민 끝에 무엇을 결정했는지**가 미래의 나에게 더 가치 있다.

### 결정 1: {결정 제목} `#태그`

- **상황(Context)**: 어떤 문제/갈림길
- **선택지(Options)**: 어떤 대안들
- **결정(Decision)**: 무엇을 선택
- **근거(Reasoning)**: 왜
- **트레이드오프(Trade-off)**: 포기한 것/리스크

<!-- 여러 개면 ### 결정 2, 3... -->
<!-- 결정 없는 날: "오늘은 루틴 작업 위주, 새로운 결정 없음" -->

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

<!-- 필요 시 태그 추가 가능. AI가 맥락에서 자동 제안 -->

## 진행 상황

- 완료: {항목}
- 진행 중: {항목}
- 이슈: {이슈}

## 다음 액션 아이템

- [ ] 단기 (1-3일)
- [ ] 중기 (1-2주)
- [ ] 장기 (1개월+)

## 내일 이어갈 내용

- {다음 주제}

## 오늘의 헤드라인

> [§ 회고 품질 기준](#회고-품질-기준) 참조

## 오늘의 회고 (Cut - Core - Logic)

> planner 리뷰를 거쳐 작성.

### Cut (반복되는 나의 패턴)

- {상황에서 드러난 행동/판단 패턴} → **다음 액션**: {패턴을 깨기 위한 행동}
- 반복 패턴 없으면 섹션 생략

### Core (오늘의 진짜 성과)

- {어떤 상황/갈등 → 판단 → 결과}
- 루틴 날은 간략히

### Logic (삶에 남기는 규칙)

- {진짜 배운 게 있을 때만} `L-MMDD-순번`
- 없으면 "오늘은 새로운 Logic 없음"

## Lesson-Learned (from Workflow Logs)

> `~/.claude/logs/` 당일 로그에서 자동 추출. 로그 없으면 섹션 생략.

### 도구/프레임워크 TIL

- {도구}: {배운 것}

### 프로세스 개선

- {개선점}

### 실수 방지

- {반복하지 않을 실수와 대응법}

> CLAUDE.md Lesson Learn 추가 제안: {있으면 표시}
```

### 주간 요약

**저장 위치**: Google Drive 월별 파일(`YYYY-MM.md`) 해당 주 마지막 일별 항목 바로 위에 `## Week {주차}` 인라인 삽입
**데이터**: 해당 주 일별 항목의 헤드라인/결정/회고(Logic 포함) — Google Drive 기준, 보조로 Obsidian 읽기 가능

```markdown
## Week {주차} ({시작일} ~ {종료일})

### 헤드라인 모음

| 날짜 | 헤드라인 |
|------|----------|
| {MM/DD} | {헤드라인} |

### Logic 리뷰

> 이번 주 Logic이 실제 적용되었는지 검증.

| ID | 규칙 | 실제 적용? | 계속? |
|----|------|-----------|-------|

**판정**: **유지** 또는 **폐기** (2단계)

### 결정 돌아보기 (Decision Review)

> 1~2주 전 결정 중 결과가 나온 것을 평가.

| 결정 (날짜) | 당시 근거 | 결과 | 평가 |
|-------------|-----------|------|------|
| {제목} ({MM/DD}) | ... | ... | Good/Adjust/Reverse |

### 이번 주 배움

- {내용}

### 다음 주 이어갈 것

- [ ] ...
```

### 월간 요약

**저장 위치**: Google Drive 월별 파일 최상단 `## {년월} 월간 요약` 인라인 삽입
**데이터**: 해당 월 주별 요약 + 일별 Logic/결정/Cut 종합

```markdown
## {년월} 월간 요약

### 이달의 헤드라인 Top 3

1. {가장 임팩트 있었던 하루}
2. {두 번째}
3. {세 번째}

### Logic 현황

- 이달 생성: {N}개
- 유지 중: {목록}
- 폐기: {목록}

### 결정 패턴

- 태그 분포: {예: #architecture 8건, #prioritization 5건}
- Good/Adjust/Reverse 비율: {%} / {%} / {%}

### 다음 달 핵심 목표 Top 3

1. ...
2. ...
3. ...
```

---

## 예외 상황

- **기존 문서 존재**: `AskUserQuestion`으로 선택지 제시 (업데이트 / 새 문서 / 취소)
- **연휴 후 복귀**: 빈 날짜 목록을 `AskUserQuestion` 선택지로 제시 (또는 "모두 넘어가기")
- **지연 정리**: 제목에 "(늦은 정리)" 표기, 작성일/업무일 명시

## 기타 규칙

- 대화 참조: 당일은 상세, 이전 날은 필요시만 간략히
- 에러 시: 세션 없음 → 안내, 외부 연결 실패 → 로컬 출력, 설정 없음 → 기본값
- **Obsidian 쓰기 금지 원칙**: inbox.md 비우기(§ 오프라인 데이터 소스 1번 4단계)를 제외한 모든 Obsidian 쓰기 동작은 금지. 모든 회고 산출물은 Google Drive에만 저장.
