# 워크플로우 디버깅 가이드

워크플로우 실행 과정을 추적하고 문제를 진단하기 위한 가이드입니다.

## 전체 플로우차트

```
┌─────────────────────────────────────────────────────────────────┐
│                        새로운 작업 요청                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  [판단] 복합적 협업 필요한가?                                      │
│  - 새 프로젝트/기능?                                              │
│  - 중요한 의사결정?                                               │
│  - 트레이드오프 상황?                                             │
└─────────────────────────────────────────────────────────────────┘
                    │                       │
                   YES                      NO
                    │                       │
                    ▼                       │
┌───────────────────────────┐               │
│  패널 토론 / 브레인스토밍   │               │
│  (4개 역할 동시 참여)       │               │
└───────────────────────────┘               │
                    │                       │
                    ▼                       │
┌───────────────────────────┐               │
│  통합 방향 도출            │               │
└───────────────────────────┘               │
                    │                       │
                    ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    순차 실행 시작                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  1. Planner │ ──────▶ │ 2. Developer│ ──────▶ │ 3. Marketer │
│  (기획)     │         │  (개발)      │         │  (마케팅)    │
└─────────────┘         └─────────────┘         └─────────────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ 크로스리뷰   │         │ 크로스리뷰   │         │ 크로스리뷰   │
└─────────────┘         └─────────────┘         └─────────────┘
                                                       │
                                                       ▼
                                                ┌─────────────┐
                                                │ 4. Operator │
                                                │  (운영)      │
                                                └─────────────┘
```

---

## 단계별 디버깅 체크리스트

### 0단계: 복합적 협업 판단

**입력:**
- 사용자 요청 내용
- 현재 PRODUCT_CONTEXT.md 상태

**판단 기준:**
| 조건 | 패널 토론 | 브레인스토밍 | 바로 순차 실행 |
|------|----------|-------------|---------------|
| 새 프로젝트 시작 | ✅ | ✅ | |
| 기존 기능 수정 | | | ✅ |
| 방향 전환/피벗 | ✅ | | |
| 새 아이디어 탐색 | | ✅ | |
| 단순 버그 수정 | | | ✅ |
| 트레이드오프 결정 | ✅ | | |

**디버그 로그 형식:**
```
[WORKFLOW:JUDGE] 요청: "{요청 내용 요약}"
[WORKFLOW:JUDGE] 판단 조건: {해당 조건}
[WORKFLOW:JUDGE] 결정: {PANEL_DISCUSSION | BRAINSTORM | SEQUENTIAL}
```

---

### 패널 토론 (Panel Discussion)

**입력:**
- 토론 주제 (명확한 질문 형태)

**실행 순서:**
1. 주제 설정
2. 4개 역할 순회하며 관점 수집
3. 교집합/충돌 분석
4. 통합 방향 도출

**각 역할별 응답 템플릿:**
```
🎯 Planner 관점:
- [구조적 접근 방법]
- [사용자 인지 부하 고려사항]
- [Stateless/회복가능성 관점]

🛠 Developer 관점:
- [기술적 실현 가능성]
- [숨은 복잡도/기술 부채]
- [인프라/성능 고려사항]

📣 Marketer 관점:
- [고객 가치/소구 포인트]
- [포지셔닝/차별화]
- [첫 사용 경험]

🔧 Operator 관점:
- [운영 부담/리스크]
- [장애 시나리오]
- [모니터링 지표]
```

**디버그 로그 형식:**
```
[PANEL:START] 주제: "{토론 주제}"
[PANEL:PLANNER] 관점 3개 수집 완료
[PANEL:DEVELOPER] 관점 3개 수집 완료
[PANEL:MARKETER] 관점 3개 수집 완료
[PANEL:OPERATOR] 관점 3개 수집 완료
[PANEL:ANALYZE] 교집합: {공통 키워드}
[PANEL:ANALYZE] 충돌: {충돌 지점}
[PANEL:RESULT] 통합 방향: "{도출된 방향}"
```

**체크포인트:**
- [ ] 4개 역할 모두 응답했는가?
- [ ] 각 역할이 최소 2개 이상 관점을 제시했는가?
- [ ] 통합 방향이 명확한 한 문장으로 정리되었는가?

---

### 브레인스토밍 (Idea Harvest)

**입력:**
- 브레인스토밍 주제

**실행 순서:**
1. **발산**: 각 역할이 3가지씩 아이디어 제시 (비판 없이)
2. **분석**: 교집합, 보완점, 충돌 식별
3. **수렴**: 우선순위 결정

**디버그 로그 형식:**
```
[BRAINSTORM:START] 주제: "{주제}"
[BRAINSTORM:DIVERGE] Planner 아이디어 3개
[BRAINSTORM:DIVERGE] Developer 아이디어 3개
[BRAINSTORM:DIVERGE] Marketer 아이디어 3개
[BRAINSTORM:DIVERGE] Operator 아이디어 3개
[BRAINSTORM:ANALYZE] 총 12개 아이디어 수집
[BRAINSTORM:ANALYZE] 교집합: {n}개
[BRAINSTORM:ANALYZE] 충돌: {n}개
[BRAINSTORM:CONVERGE] 최종 선정: {선정된 아이디어들}
[BRAINSTORM:CONVERGE] 연기: {v1.1로 미룬 것들}
```

**체크포인트:**
- [ ] 각 역할이 정확히 3개 아이디어를 냈는가?
- [ ] 교집합 분석이 수행되었는가?
- [ ] 충돌 항목에 대한 해결 방안이 제시되었는가?

---

### 순차 실행: Planner 단계

**입력:**
- 패널 토론/브레인스토밍 결과 (있는 경우)
- 기존 PRODUCT_CONTEXT.md

**산출물:**
- 기획서 (요구사항, UX 플로우)
- PRODUCT_CONTEXT.md Planner Section 업데이트

**디버그 로그 형식:**
```
[PLANNER:START] 작업: "{작업 내용}"
[PLANNER:CONTEXT] PRODUCT_CONTEXT.md 읽기 완료
[PLANNER:WORK] 요구사항 구조화 중...
[PLANNER:WORK] UX 플로우 설계 중...
[PLANNER:OUTPUT] 기획서 작성 완료
[PLANNER:UPDATE] PRODUCT_CONTEXT.md 업데이트 완료
[PLANNER:REVIEW] 크로스 리뷰 시작
```

**크로스 리뷰 체크:**
```
[REVIEW:PLANNER] Developer 검토: {PASS|WARN|FAIL} - "{코멘트}"
[REVIEW:PLANNER] Marketer 검토: {PASS|WARN|FAIL} - "{코멘트}"
[REVIEW:PLANNER] Operator 검토: {PASS|WARN|FAIL} - "{코멘트}"
[REVIEW:PLANNER] 수정 필요 항목: {n}개
```

**체크포인트:**
- [ ] MECE하게 구조화되었는가?
- [ ] 불필요한 요소가 제거되었는가?
- [ ] 크로스 리뷰에서 FAIL 없는가?

---

### 순차 실행: Developer 단계

**입력:**
- Planner 기획서
- 크로스 리뷰 피드백

**산출물:**
- 구현된 코드
- PRODUCT_CONTEXT.md Developer Section 업데이트

**디버그 로그 형식:**
```
[DEVELOPER:START] 작업: "{작업 내용}"
[DEVELOPER:SPEC] 기획서 분석 완료
[DEVELOPER:PLAN] 구현 계획 수립
[DEVELOPER:CODE] 코드 작성 중... {파일명}
[DEVELOPER:TEST] 테스트 실행: {PASS|FAIL}
[DEVELOPER:OUTPUT] 구현 완료
[DEVELOPER:UPDATE] PRODUCT_CONTEXT.md 업데이트 완료
[DEVELOPER:REVIEW] 크로스 리뷰 시작
```

**크로스 리뷰 체크:**
```
[REVIEW:DEVELOPER] Planner 검토: {PASS|WARN|FAIL} - "{기획 의도 반영 여부}"
[REVIEW:DEVELOPER] Marketer 검토: {PASS|WARN|FAIL} - "{릴리즈 준비 상태}"
[REVIEW:DEVELOPER] Operator 검토: {PASS|WARN|FAIL} - "{모니터링 준비 상태}"
```

**체크포인트:**
- [ ] Stateless 아키텍처 준수?
- [ ] 비동기 처리 적용?
- [ ] 에러 복구 로직 포함?
- [ ] 테스트 통과?

---

### 순차 실행: Marketer 단계

**입력:**
- Developer 구현 결과
- 제품 핵심 가치

**산출물:**
- 마케팅 콘텐츠 (카피, 릴리즈 노트 등)
- PRODUCT_CONTEXT.md Marketer Section 업데이트

**디버그 로그 형식:**
```
[MARKETER:START] 작업: "{작업 내용}"
[MARKETER:ANALYZE] 제품 가치 분석
[MARKETER:CREATE] 콘텐츠 작성 중...
[MARKETER:OUTPUT] 마케팅 콘텐츠 완료
[MARKETER:UPDATE] PRODUCT_CONTEXT.md 업데이트 완료
[MARKETER:REVIEW] 크로스 리뷰 시작
```

**크로스 리뷰 체크:**
```
[REVIEW:MARKETER] Planner 검토: {PASS|WARN|FAIL} - "{핵심 가치 왜곡 여부}"
[REVIEW:MARKETER] Developer 검토: {PASS|WARN|FAIL} - "{기술적 오류 여부}"
[REVIEW:MARKETER] Operator 검토: {PASS|WARN|FAIL} - "{CS 유발 요소}"
```

**체크포인트:**
- [ ] 핵심 가치가 정확히 전달되는가?
- [ ] 기술적으로 틀린 내용 없는가?
- [ ] 과장/오해 소지 없는가?

---

### 순차 실행: Operator 단계

**입력:**
- 전체 진행 결과
- 배포된 시스템 정보

**산출물:**
- 운영 가이드
- 모니터링 설정
- PRODUCT_CONTEXT.md Operator Section 업데이트

**디버그 로그 형식:**
```
[OPERATOR:START] 작업: "{작업 내용}"
[OPERATOR:MONITOR] 모니터링 설정 확인
[OPERATOR:PREPARE] 장애 대응 시나리오 수립
[OPERATOR:OUTPUT] 운영 가이드 완료
[OPERATOR:UPDATE] PRODUCT_CONTEXT.md 업데이트 완료
```

**체크포인트:**
- [ ] 모니터링 지표 정의?
- [ ] 장애 대응 플로우 수립?
- [ ] 롤백 절차 준비?

---

## 전체 실행 로그 예시

```
============================================================
[WORKFLOW:START] 2024-01-15 10:30:00
[WORKFLOW:REQUEST] "AI 기반 일정 관리 앱 개발"
============================================================

[WORKFLOW:JUDGE] 요청: "AI 기반 일정 관리 앱 개발"
[WORKFLOW:JUDGE] 판단 조건: 새 프로젝트 시작
[WORKFLOW:JUDGE] 결정: PANEL_DISCUSSION + BRAINSTORM

------------------------------------------------------------
[PANEL:START] 주제: "AI 기반 일정 관리 앱의 핵심 방향은?"
[PANEL:PLANNER] 관점 3개 수집 완료
[PANEL:DEVELOPER] 관점 3개 수집 완료
[PANEL:MARKETER] 관점 3개 수집 완료
[PANEL:OPERATOR] 관점 3개 수집 완료
[PANEL:ANALYZE] 교집합: 심플함, 신뢰성, 오프라인
[PANEL:ANALYZE] 충돌: 기능 풍부함 vs 경량화
[PANEL:RESULT] 통합 방향: "오프라인 우선, AI는 조용한 비서처럼 제안만"
------------------------------------------------------------

------------------------------------------------------------
[BRAINSTORM:START] 주제: "MVP에 꼭 들어가야 할 기능은?"
[BRAINSTORM:DIVERGE] 총 12개 아이디어 수집
[BRAINSTORM:ANALYZE] 교집합: 3개 (자연어 입력, 로컬 우선, 빠른 온보딩)
[BRAINSTORM:ANALYZE] 충돌: 2개 (위젯, 주간 리포트)
[BRAINSTORM:CONVERGE] 최종 선정: 자연어 입력, 로컬+동기화, 3탭 온보딩
[BRAINSTORM:CONVERGE] 연기: 위젯(v1.1), 주간리포트(앱 내 요약으로 축소)
------------------------------------------------------------

============================================================
[SEQUENTIAL:START] 순차 실행 시작
============================================================

[PLANNER:START] 작업: "MVP 기획서 작성"
[PLANNER:OUTPUT] 기획서 작성 완료
[PLANNER:UPDATE] PRODUCT_CONTEXT.md 업데이트 완료
[REVIEW:PLANNER] Developer: WARN - "3초 연동 불가, 3탭으로 수정"
[REVIEW:PLANNER] Marketer: WARN - "차별점 섹션 추가 필요"
[REVIEW:PLANNER] Operator: WARN - "AI 거부 피드백 UI 필요"
[PLANNER:REVISE] 수정 항목 3개 반영 완료

[DEVELOPER:START] 작업: "MVP 구현"
[DEVELOPER:CODE] 코드 작성 중... src/calendar/...
[DEVELOPER:TEST] 테스트 실행: PASS
[DEVELOPER:OUTPUT] 구현 완료
[REVIEW:DEVELOPER] Planner: PASS
[REVIEW:DEVELOPER] Marketer: PASS
[REVIEW:DEVELOPER] Operator: PASS

[MARKETER:START] 작업: "릴리즈 노트 작성"
[MARKETER:OUTPUT] 마케팅 콘텐츠 완료
[REVIEW:MARKETER] Planner: PASS
[REVIEW:MARKETER] Developer: PASS
[REVIEW:MARKETER] Operator: PASS

[OPERATOR:START] 작업: "운영 준비"
[OPERATOR:OUTPUT] 운영 가이드 완료

============================================================
[WORKFLOW:END] 2024-01-15 14:30:00
[WORKFLOW:STATUS] SUCCESS
[WORKFLOW:SUMMARY]
- 패널 토론: 핵심 방향 도출
- 브레인스토밍: MVP 기능 3개 확정
- 기획: 수정 3회 후 완료
- 개발: 테스트 통과
- 마케팅: 릴리즈 노트 준비 완료
- 운영: 모니터링 설정 완료
============================================================
```

---

## 문제 진단 가이드

### 증상별 원인 추적

| 증상 | 확인할 로그 | 가능한 원인 |
|------|------------|-------------|
| 방향이 산만함 | `[PANEL:RESULT]` | 패널 토론 통합 실패 |
| 기획-개발 불일치 | `[REVIEW:PLANNER]` | 크로스 리뷰 스킵 |
| 구현 복잡도 폭발 | `[BRAINSTORM:CONVERGE]` | 충돌 해결 없이 전부 수용 |
| 마케팅 메시지 부정확 | `[REVIEW:MARKETER]` | Developer/Planner 리뷰 스킵 |
| 운영 이슈 빈발 | `[OPERATOR:PREPARE]` | 장애 시나리오 미수립 |

### 자주 발생하는 문제

**1. 패널 토론 건너뜀**
```
문제: 새 프로젝트인데 바로 Planner로 시작
원인: [WORKFLOW:JUDGE] 단계 누락
해결: 복합적 협업 판단 단계 강제 실행
```

**2. 크로스 리뷰 형식적 수행**
```
문제: 리뷰 결과가 모두 PASS인데 나중에 문제 발생
원인: 각 역할 관점에서 실제 검토 안 함
해결: 각 리뷰어가 최소 1개 이상 구체적 피드백 필수
```

**3. 브레인스토밍 수렴 실패**
```
문제: 12개 아이디어가 모두 MVP에 포함
원인: [BRAINSTORM:CONVERGE] 단계에서 우선순위 결정 안 함
해결: 교집합 기준으로 3개 이하로 제한
```

---

## 추가 태그

기존 태그 외에 상황에 맞게 사용합니다.

| 태그 | 언제 |
|------|------|
| `[WORKFLOW:CONTEXT]` | 환경/제약/이전 워크플로우 관계가 있을 때. `CONTINUES_FROM:`으로 이전 로그 연결 |
| `[WORKFLOW:DECISION]` | 방향전환(Pivot) 시 상황, 선택지, 결정, 근거 기록 |
| `[WORKFLOW:LEARNING]` | 재사용 가능한 교훈 발생 시. `#{카테고리}` 태깅. `lessons-learned.md`에 적재 |
| `[WORKFLOW:METRICS]` | 종료 시 정량 요약 (소요시간, 산출물 수, 리뷰 건수 등) |
| `[WORKFLOW:NEXT]` | INCOMPLETE로 끝날 때 다음 세션 인수인계. INCOMPLETE 시 필수 |
| `[VERIFY:{TYPE}]` | 빌드/테스트/수동검증 결과 (PASS/FAIL) |

---

## 디버그 모드 활성화

워크플로우 실행 시 상세 로그를 남기려면:

```markdown
<!-- PRODUCT_CONTEXT.md 상단에 추가 -->
## Debug Mode
- enabled: true
- log_level: VERBOSE
- log_location: .agent/logs/workflow_{date}.log
```

이 설정이 있으면 workflow_maker가 각 단계마다 위 형식의 로그를 남깁니다.
