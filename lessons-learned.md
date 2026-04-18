# Lessons Learned

워크플로우 실행 중 발생한 재사용 가능한 교훈을 누적 기록합니다.
각 항목의 `[WORKFLOW:LEARNING]` 태그는 해당 로그 파일에서 추출된 것입니다.

---

## #PA (Power Automate)

### Excel List rows의 Filter Query는 고급 매개변수에 숨겨져 있음 (치명적)

- 출처: `workflow_2026-04-17_excel-mail-notifier.log`
- 교훈: Excel Online "List rows present in a table" 액션의 **Filter Query 필드는 기본 UI에 노출되지 않고 "고급 매개 변수 0/6 표시 중" 섹션 안에 숨겨져 있음**. 필터 미입력 시 전체 행을 반환하여 조건 상관없이 모든 행이 처리됨
- 적용: Filter Query가 필요한 Flow는 반드시 **"모두 보기" 클릭 → Filter Query 필드 확인**. 구축 가이드에 해당 단계를 명시적으로 기록. 배포 전 검증 시 고급 매개변수 표시 상태(`n/6 표시 중`의 n값)로 설정 여부 확인

### Monaco 에디터에 외부 텍스트 입력 불가

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: PA New Designer의 Expression 다이얼로그는 Monaco 에디터를 사용하며, `insertText()`, `type()`, `execCommand`, `ClipboardEvent` 모두 Monaco TextModel에 반영되지 않음
- 적용: 리터럴 값이 포함된 식은 **PA Copilot**으로 입력하거나, **PA 함수 목록/동적 콘텐츠에서 클릭**으로만 입력 가능

### PA Copilot으로 리터럴 파라미터 식 입력

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: `addHours(field, 1)` 같이 리터럴 파라미터가 포함된 식은 PA Copilot만으로 입력 가능
- 적용: 필드 클릭 → "/" → "Insert expression" → "Create an expression with Copilot" → 자연어 요청 → 확인 후 "OK" → "Add"

### OData 필터에서 한글 컬럼명 사용 불가

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: SharePoint OData API의 `$filter`는 **내부 컬럼명(InternalName)**만 인식. PA GetItems 커넥터도 한글 표시명을 자동 변환하지 않음
- 적용: `$filter`에서는 항상 `OData__xXXXX_` 형태의 내부 컬럼명 사용. 내부 컬럼명은 `/_api/web/lists/getbytitle('리스트명')/fields` REST API로 조회

### PA 한글 컬럼명이 동작하는 경우 vs 안 하는 경우

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: GetItems `$filter`에서는 **실패**, PatchItem `item/상태`에서는 **정상** (PA 자동 매핑), 동적 콘텐츠/Condition에서도 **정상**
- 적용: OData `$filter`만 내부 컬럼명 필수, 나머지는 한글 표시명 사용 가능

### PA 조건 카드에서 null 비교 신뢰 불가

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: PA 조건 카드의 `!= null` (expression) 비교는 실제로 문자열 "null"과 비교하여 의도와 다르게 동작함
- 적용: null 체크 시 **`empty()` 함수** 사용 → `empty(field) == false` (리터럴) 패턴으로 "비어있지 않을 때만" 통과시킴

### V4CalendarPostItem date-no-tz 형식 불일치

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: SharePoint DateTime 필드는 `String/date-time` 형식(타임존 포함)이지만, Create event V4의 `start`/`end` 파라미터는 `String/date-no-tz` 요구
- 적용: 동적 콘텐츠 직접 참조 대신 `formatDateTime(field, 'yyyy-MM-ddTHH:mm:ss')`로 타임존 제거

### PA 세션 토큰 만료

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: 장시간 브라우저 자동화(3+ 세션)로 PA 세션 토큰이 만료되면 저장 시 400 Bad Request 발생 (authorization 빈 토큰)
- 적용: 장시간 작업 시 중간에 페이지 새로고침(F5)으로 세션 토큰 갱신. 저장 전에 Flow Checker로 Errors: 0 확인

---

## #SharePoint

### OData 내부 컬럼명 매핑 참조표

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: 한글 컬럼명과 OData 내부명의 매핑은 프로젝트별로 다를 수 있음
- 적용: 새 SharePoint 리스트 작업 시 항상 REST API로 내부 컬럼명부터 조회
  ```
  GET {SITE_URL}/_api/web/lists/getbytitle('리스트명')/fields?$filter=Hidden eq false&$select=Title,InternalName,TypeAsString
  ```

### SharePoint 리스트 이전 시 주의사항

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: 사이트 간 리스트 이전 시 OData 내부 필드명이 달라질 수 있음 (새 리스트에서 다른 InternalName 생성)
- 적용: 리스트 이전 후 모든 PA Flow의 `$filter` 쿼리에서 내부 필드명 재확인 필수

---

## #Browser-Automation

### Playwright MCP 브라우저 연결 끊김

- 출처: `workflow_2026-02-19_pa-flow-build.log`
- 교훈: 기존 Chrome 세션과 동일 user-data-dir 충돌로 Playwright MCP 연결이 끊어질 수 있음
- 적용: 다음 세션 시작 시 자동 복구되지만, 장시간 작업 시 브라우저 상태를 중간에 점검

---

## #Architecture

### 새로 만들기 전 기존 도구 우선 검토

- 출처: `workflow_2026-02-10_universal-inbox.log`
- 교훈: "입력 소스 통합 관리" 요구에 대해 4역할 패널 토론 + 개발 계획까지 진행했으나, 사용자가 "기존 도구 활용" 방향으로 전환. 기존 도구(Notion, Obsidian 등)로 80% 커버 가능하다는 결론
- 적용: 신규 프로젝트 제안 전 **"기존 도구로 어느 정도 해결 가능한가?"** 리서치를 먼저 수행. "기존 도구로 1-2주 사용 → 마찰 포인트 기록 → 판단 분기" 패턴 활용

### "마찰 포인트 기반 MVP 우선순위" 패턴

- 출처: `workflow_2026-02-10_universal-inbox.log`
- 교훈: 기존 도구를 쓰다가 마찰이 크면 그 마찰 포인트가 곧 PRD 우선순위가 됨. 추상적으로 기능을 나열하는 것보다 실제 불편을 기반으로 스코프를 잡는 것이 정확함
- 적용: 기존 도구 사용 → 마찰 포인트 기록 → 마찰이 크면 MVP 스코프로, 견딜만하면 개발 불필요

---

## #MS365

### MS 365 E3 라이선스 제약

- 출처: `workflow_2026-02-05_security-automation.log`, `workflow_2026-02-19_pa-flow-build.log`
- 교훈: E3 라이선스에서는 Standard 커넥터만 사용 가능. HTTP(Premium), AI Builder(Premium) 사용 불가. 처음 NestJS + PostgreSQL 스택으로 설계했다가 "MS 도구만 사용" 제약으로 전환
- 적용: 사내 시스템 자동화 시 **라이선스 제약**을 가장 먼저 확인. E3 기준 Standard 커넥터 목록 사전 점검

### 코딩 없는 자동화의 ROI

- 출처: `workflow_2026-02-05_security-automation.log`
- 교훈: MS 365 도구만으로 (Power Automate + SharePoint + Forms + Word→PDF) 구현 시간 약 4시간, 코딩 없음. 연간 42~138시간 절감 추정
- 적용: 코딩 스택 제안 전에 "MS 365 도구 조합만으로 가능한가?" 먼저 검토. 특히 내부 업무 자동화는 코딩 없는 접근이 유지보수 비용도 낮음

---

## #Workflow

### 프로젝트 리브랜딩 시 연속성 관리

- 출처: `workflow_2025-02-03_total-tracker.log` → `workflow_2026-02-05_total-tracker.log` → `workflow_2026-02-05_tally.log`
- 교훈: total-tracker가 tally로 리브랜딩되면서 3개 로그가 관계를 갖지만, 로그 간 연결이 암시적임
- 적용: 리브랜딩/계승 시 `[WORKFLOW:CONTEXT]`에 `이전 워크플로우: workflow_{날짜}_{이름}.log` 명시

### 크로스 리뷰의 가치

- 출처: `workflow_2025-02-03_total-tracker.log`, `workflow_2026-02-05_total-tracker.log`
- 교훈: 크로스 리뷰에서 평균 2-4건의 WARN이 발생하고, 대부분 실제 구현에 반영됨 (total-tracker에서 총 11건 반영). 특히 Operator의 "데이터 백업/복원" 지적, Marketer의 "야행성→새벽형 인간" 리네이밍 등은 사전에 발견하지 못했을 이슈
- 적용: 크로스 리뷰를 생략하지 말 것. 특히 UX 관련 이름/표현은 Marketer 리뷰에서 잡히는 경우가 많음

---

## #Brand

### 루트 브랜드 계승 패턴

- 출처: `workflow_2026-02-04_todo-app.log`, `workflow_2026-02-05_tally.log`, `workflow_2026-02-08_design-system.log`
- 교훈: Sam Samuel 루트 브랜드(`~/.claude/BRAND.md`)에서 프로젝트별 BRAND.md로 계승하는 패턴이 일관적으로 동작함. 컬러(#F0EEE9), 폰트(Pretendard), 톤앤매너가 모든 프로젝트에서 통일됨
- 적용: 신규 프로젝트 시작 시 루트 브랜드 참조를 Marketer 단계 첫 작업으로 실행

---

## #Monitoring

### 대시보드 No Data 시 기존 파이프라인 동기화부터 확인

- 출처: `.agent/intents/archive/monitor-01.md` (2026-04-08)
- 교훈: Grafana 패널에 데이터가 없을 때 새 exporter나 mock을 만들기 전에 기존 수집 파이프라인의 설정 동기화 상태를 먼저 확인해야 함. monitor-01에서는 로컬 YACE config(yace/config.yml)에는 AWS/RUM job이 존재했지만 k8s ConfigMap(yace-config.yaml)에 누락된 것이 원인이었음. 새 컴포넌트 0개로 해결.
- 적용: No Data 디버깅 순서 → ① 로컬 설정 vs k8s 설정 동기화 확인 → ② Prometheus targets 상태 확인(`/targets`) → ③ 대시보드 쿼리 메트릭명과 실제 수집 메트릭명 일치 확인 → ④ 모두 정상이면 새 exporter 고려

### 로컬-k8s 설정 drift 함정

- 출처: `.agent/intents/archive/monitor-01.md` (2026-04-08)
- 교훈: 로컬 개발 설정(docker-compose.yml, yace/config.yml)과 k8s 배포 설정(ConfigMap, Deployment)은 독립적으로 관리되므로 drift가 발생하기 쉬움. 로컬에서 정상 동작하더라도 k8s 환경에서 No Data일 수 있음.
- 적용: 모니터링 설정 변경 시 로컬 파일과 k8s 파일을 항상 함께 수정. 코드 리뷰 시 "k8s ConfigMap과 로컬 설정이 동기화되어 있는가?" 체크리스트 포함 권장.

---

## #UX

### 인지 부하 줄이기 3원칙

- 출처: `workflow_2026-02-08_design-system.log`
- 교훈: 선택지 최소화, 일관성, 의미 중심. 디자인 시스템 패널 토론에서 4역할이 교집합으로 도출한 원칙
- 적용: UI 설계 시 이 3원칙을 체크리스트로 활용

---

*마지막 업데이트: 2026-04-08*
*추출 대상 로그: 8개 (2025-02-03 ~ 2026-02-19) + Heartbeat Agent 실행 결과 1건 (monitor-01)*
