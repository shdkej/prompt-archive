# Agent-First Workflow Architecture

> "내가 에이전트를 돌리는게 아니라 에이전트가 돌다가 나한테 알려주게 해야한다"

## 핵심 전환

```
[AS-IS] User-Driven (반응형)
  사용자 → 트리거 → workflow-master → 에이전트 할당 → 실행 → 보고

[TO-BE] Agent-First (자율형)
  사용자 → 의도 선언 → 일상 복귀
  에이전트 → Heartbeat 기상 → 의도 확인 → 자율 실행 → 결과 알림
                                                ↑
                                    (판단 필요시만 사용자 호출)
```

사용자는 **의도(Intent)와 판단(Gate)**만 담당한다.
에이전트는 **실행, 진행, 보고**를 허용된 권한 안에서 자율적으로 수행한다.

## 설계 원칙

| 원칙 | 설명 | 출처 |
|------|------|------|
| Heartbeat Loop | 에이전트가 스케줄에 따라 깨어나서 일감 확인→실행→보고→수면 | Paperclip |
| Plan-Based Autonomy | 검증된 계획 안에서 수시간 자율 작업 가능 | Superpowers |
| Context Chaining | 각 단계의 산출물이 다음 단계의 입력으로 자동 전달 | gstack |
| Verifiable Criteria | 모호한 목표 대신 측정 가능한 성공 기준 | Karpathy |
| Permission Boundary | 자율성은 무제한이 아니라 등급별 경계 안에서 작동 | 공통 |
| Reuse Before Create | 새 컴포넌트 생성 전 기존 리소스 활용 가능 여부를 먼저 확인 | Lesson Learn |

## 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    USER LAYER                           │
│                                                         │
│  INTENTS.md          의도 선언 (목표, 우선순위, 제약)     │
│  Telegram            승인/거부, 진행 상황 수신           │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    CONTROL LAYER                        │
│                                                         │
│  Heartbeat Agent     스케줄 기반으로 깨어남              │
│    ├── Intent 읽기   INTENTS.md에서 활성 의도 확인       │
│    ├── State 확인    현재 상태 점검 (git, files, etc.)   │
│    ├── Dispatch      적절한 실행 에이전트에 작업 할당     │
│    └── Gate Check    권한 레벨에 따라 자율 실행/승인 요청 │
│                                                         │
│  PERMISSIONS.md      권한 경계 정의                      │
│  GATES.md            승인 대기 큐                        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    EXECUTION LAYER                      │
│                                                         │
│  기존 workflow-master   복잡한 작업 시 4-role 오케스트레이션 │
│  단일 에이전트 실행      간단한 작업 시 focused 실행       │
│  OMC 스킬               autopilot, ralph 등 활용         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    NOTIFICATION LAYER                   │
│                                                         │
│  Telegram Bot        진행 알림, 완료 보고, 승인 요청     │
│  .agent/reports/     실행 결과 로그 (영구 저장)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Intent (의도) 설계

### INTENTS.md 구조

```markdown
## [intent-id] 의도 이름

- status: declared | active | in_progress | blocked | completed | archived
- priority: critical | high | medium | low
- heartbeat: 30m | 1h | 4h | daily | weekly
- permission: L0 | L1 | L2
- project: 프로젝트 경로 또는 이름
- deadline: YYYY-MM-DD (선택)
- goal: 이 의도가 달성되면 어떤 상태인지 한 줄로
- success_criteria:
  - 측정 가능한 기준 1
  - 측정 가능한 기준 2
- context: 관련 파일, URL, 참고 정보
- constraints: 하지 말아야 할 것, 제약 조건
```

### Intent 생명주기

```
declared ──→ active ──→ in_progress ──→ completed ──→ archived
                │              │
                │              └──→ blocked (승인 대기) ──→ in_progress
                │
                └──→ cancelled
```

- **declared**: 사용자가 선언만 한 상태. Heartbeat가 다음 기상 시 확인
- **active**: Heartbeat가 실행 가능하다고 판단, 계획 수립 중
- **in_progress**: 실행 중. 마일스톤 단위로 진행
- **blocked**: 사용자 승인이 필요한 Gate에 도달
- **completed**: 성공 기준 충족. 사용자에게 완료 알림
- **archived**: 사용자가 확인 후 보관

### Intent 예시

```markdown
## [monitor-01] KOP 스테이지 배포 모니터링

- status: active
- priority: high
- heartbeat: 30m
- permission: L1
- project: kop-web
- goal: GitLab 파이프라인 성공/실패를 실시간으로 파악하고 실패 시 원인 분석까지 자동 수행
- success_criteria:
  - 파이프라인 상태 변화 감지 후 2분 내 알림
  - 실패 시 에러 로그 요약 포함
- context: GitLab CI/CD, Slack 배포 채널 C07K6SXSU8Z
- constraints: 직접 배포하지 않음. 알림만.

## [dev-01] 보안교육 PA Flow 구현

- status: declared
- priority: medium
- heartbeat: 4h
- permission: L2
- project: security-automation
- deadline: 2026-04-30
- goal: 신규입사자 보안교육 자동 배분 PA Flow가 실제 동작
- success_criteria:
  - SharePoint 리스트 생성 완료
  - PA Flow 정의 JSON 생성
  - 단계별 구축 가이드 작성
- context: security-automation/PRODUCT_CONTEXT.md, PA.md
- constraints: Premium 커넥터 사용 금지 (E3 라이선스)
```

## Permission (권한) 설계

### 4단계 권한 레벨

| 레벨 | 이름 | 행동 | 사용자 관여 | 예시 |
|------|------|------|------------|------|
| **L0** | 자율 (Free) | 실행 후 요약 알림 | 없음 | 코드 분석, 리서치, 문서 드래프트, 상태 체크 |
| **L1** | 알림 (Notify) | 실행 후 결과 알림 | 사후 확인 | 코드 작성, 테스트 실행, 브랜치 생성, 파일 수정 |
| **L2** | 승인 (Approve) | 실행 전 승인 요청 | 사전 승인 | git push, PR 생성, 외부 API 호출, 배포 트리거 |
| **L3** | 금지 (Block) | 실행하지 않음 | 직접 수행 | force push, 삭제, 비용 발생 작업, 프로덕션 변경 |

### PERMISSIONS.md 구조

```markdown
# Agent Permissions

## L0 - 자율 실행 (알림만)
- 파일 읽기, 코드 검색, 구조 분석
- 웹 리서치, 문서 참조
- 상태 체크 (git status, 파이프라인, 모니터링)
- 문서 드래프트 작성 (.agent/drafts/ 하위)
- 테스트 실행 (읽기 전용)

## L1 - 실행 후 알림
- 소스 코드 수정
- 새 파일 생성
- 브랜치 생성
- 테스트 작성 및 실행
- 로컬 빌드

## L2 - 승인 후 실행
- git push
- PR/MR 생성
- 외부 서비스 API 호출 (Slack, Teams, Graph API)
- 배포 트리거
- SharePoint 리스트/라이브러리 생성

## L3 - 금지 (사용자 직접)
- force push, reset --hard
- 브랜치/파일 삭제
- 프로덕션 환경 변경
- 비용 발생 작업 (클라우드 리소스 생성)
- 인증 정보 변경
```

## Heartbeat Agent 설계

### 동작 흐름

```
[Heartbeat 기상 (cron schedule)]
    │
    ├── 1. INTENTS.md 읽기
    │   └── status가 declared/active/in_progress인 의도 필터링
    │
    ├── 2. 우선순위 정렬
    │   └── critical > high > medium > low
    │   └── deadline 임박 항목 우선
    │
    ├── 3. 각 Intent별 상태 점검
    │   ├── 이전 실행 결과 확인 (.agent/reports/)
    │   ├── 현재 상태 확인 (git, files, external)
    │   └── 다음 액션 결정
    │
    ├── 4. 권한 레벨 확인
    │   ├── L0/L1 → 자율 실행
    │   └── L2 → Telegram 승인 요청 → status: blocked
    │
    ├── 5. 실행
    │   ├── 간단한 작업 → 단일 에이전트
    │   └── 복잡한 작업 → workflow-master 호출
    │
    ├── 6. 결과 기록
    │   └── .agent/reports/{intent-id}/{timestamp}.md
    │
    └── 7. 알림 발송
        ├── L0: 요약 알림 (변화 있을 때만)
        ├── L1: 결과 알림 (항상)
        ├── L2: 승인 요청
        └── 완료: 성공 기준 달성 알림
```

### Heartbeat 주기 가이드

| 주기 | 용도 | 예시 |
|------|------|------|
| 30m | 실시간 모니터링 | 파이프라인 상태, 서비스 헬스체크, 브랜드 모니터링 |
| 1h | 진행 중 작업 체크 | 코드 리뷰 상태, PR 머지 대기 |
| 4h | 개발 작업 진행 | 기능 구현, 리팩토링, 문서 작성 |
| daily | 루틴 업무 | 일일 리포트, 보안 스캔, 데이터 수집 |
| weekly | 장기 과제 | 아키텍처 개선, 기술 부채 정리 |

## Gate (승인 게이트) 설계

### Telegram 알림 포맷

```
📋 [Intent: monitor-01] KOP 스테이지 배포 모니터링

상태: 파이프라인 실패 감지
원인: ESLint 에러 (src/pages/main.tsx:42)
분석: import 순서 위반. 자동 수정 가능.

다음 액션: eslint --fix 후 커밋 & 푸시
권한 레벨: L2 (승인 필요)

✅ 승인  |  ❌ 거부  |  💬 수정 지시
```

### Gate 승인 흐름

```
에이전트: L2 액션 필요 → Telegram 승인 요청 발송 + GATES.md 대기 등록
    │
    └── Intent status → blocked

사용자: Telegram 알림 수신 (어디서든)
    │
    └── Claude Code 세션에서 응답
        ├── "승인해" → GATES.md 업데이트 → 즉시 또는 다음 Heartbeat에서 실행
        ├── "거부" → Intent에 사유 기록, 대안 탐색
        └── "이렇게 바꿔: ..." → 방향 조정 후 재실행
```

**Phase별 승인 채널:**
- Phase 0-1: Telegram = 알림, Claude Code 세션 = 승인 (실용적 MVP)
- Phase 2+: Telegram Bot 양방향 (inline keyboard + webhook)

## 기존 시스템 통합

### workflow-master와의 관계

```
Heartbeat Agent (새로운 상위 레이어)
    │
    ├── 간단한 Intent → 단일 에이전트 직접 실행
    │
    └── 복잡한 Intent → workflow-master 호출
                            │
                            ├── 4-role 병렬 실행
                            ├── 크로스 리뷰
                            └── PRODUCT_CONTEXT.md 업데이트
```

Heartbeat Agent는 workflow-master의 **상위 계층**이다.
기존 워크플로우를 대체하는 것이 아니라, **언제 어떤 워크플로우를 실행할지 결정하는 지휘관**이다.

### 기존 스킬 활용

| 기존 스킬 | Agent-First에서의 역할 |
|-----------|----------------------|
| `/schedule` | Heartbeat cron 등록 |
| `/loop` | 짧은 주기 모니터링 (30m) |
| `/kop-workflow` | KOP Intent 실행 시 호출 |
| `/brand-monitor` | 브랜드 모니터링 Intent 실행 시 호출 |
| `/daily-feedback-system` | daily heartbeat에서 자동 호출 |
| `/press-capture` | 언론 모니터링 Intent 실행 시 호출 |

## 실제 시뮬레이션: [monitor-01] Grafana Layer2 프로덕트 품질 지표 수집 복구

아래는 Intent 하나가 Heartbeat를 통해 자율 실행되는 실제 흐름이다.
사용자가 하는 일은 **의도 선언 1회 + L2 승인 1회** 뿐이다.

### 컨텍스트

- Layer 2 = "프로덕트 품질 모니터링" Grafana 대시보드 (`layer-product.json`)
- 기대 메트릭: `http_request_duration_seconds`, `web_vitals_*`, `frontend_error_total`, `aws_rum_*`
- 현재 문제: 이 메트릭을 제공하던 Mock Exporter가 docker-compose.yml에서 제거됨
- 스택: Prometheus(:9090), Grafana(:3050), docker-compose 기반

### Heartbeat 1회차: declared → active (L0 자율)

```
1. INTENTS.md 읽기 → monitor-01 발견, status: declared
2. 첫 실행이므로 상황 파악 (L0)
   ├── docker-compose.yml 분석 → Mock Exporter 서비스 없음 확인
   ├── prometheus.yml 분석 → mock exporter scrape job 없음 확인
   ├── layer-product.json 분석 → 패널별 기대 메트릭 목록 추출
   └── 진단: 메트릭 소스(exporter)가 없어서 대시보드 전체 No Data
3. 해결 방안 수립
   ├── 방안 A: Mock Exporter 복원 (데모 데이터)
   ├── 방안 B: 실제 서비스 연동 (RUM, 프론트엔드 에이전트)
   └── 판단: 현재 환경은 로컬 모니터링 → 방안 A (Mock Exporter 복원)
4. .agent/reports/monitor-01/2026-04-08T10-00.md 기록
5. status: declared → active
6. Telegram 알림:

   📋 [monitor-01] Layer2 프로덕트 품질 지표 복구
   
   상태: 초기 분석 완료
   원인: Mock Exporter 서비스가 docker-compose에서 제거됨
         → 대시보드 전체 패널 No Data
   
   계획:
   1. Mock Exporter 코드 작성 (L1)
   2. docker-compose.yml에 서비스 추가 (L1)
   3. prometheus.yml에 scrape job 추가 (L1)
   4. docker-compose up 실행 (L2 - 승인 필요)
```

### Heartbeat 2회차: active → in_progress (L1 자율 실행)

```
1. 이전 리포트 읽기 → 계획 확인, 방안 A 진행
2. L1 자율 실행:
   ├── Mock Exporter 코드 작성 (Python/Go)
   │   - http_request_duration_seconds (histogram)
   │   - http_requests_total (counter)
   │   - frontend_error_total (counter)
   │   - web_vitals_lcp_seconds, web_vitals_fid_seconds, web_vitals_cls (gauge)
   ├── docker-compose.yml에 mock-exporter 서비스 추가
   └── prometheus.yml에 scrape job 추가
3. status: active → in_progress
4. L2 필요 → GATES.md에 등록, status → blocked
5. Telegram 승인 요청:

   🔐 [monitor-01] 승인 요청
   
   액션: docker-compose up -d (모니터링 스택 재시작)
   변경 내용:
   - mock-exporter 서비스 추가 (:9101)
   - prometheus scrape job 추가
   영향: 모니터링 스택 재시작 (약 30초)
   
   ✅ 승인  |  ❌ 거부  |  💬 수정 지시
```

### Heartbeat 3회차: 승인 후 실행 → completed

```
1. GATES.md 확인 → 승인됨
2. L2 실행:
   └── cd ~/workspace/monitoring_personal && docker-compose up -d
3. 검증 (L0):
   ├── docker ps → mock-exporter 컨테이너 Running ✓
   ├── curl localhost:9101/metrics → 메트릭 노출 확인 ✓
   ├── Prometheus targets API → mock-exporter job UP ✓
   └── Grafana API → layer-product 대시보드 패널 데이터 존재 ✓
4. success_criteria 3개 모두 충족
5. status: in_progress → completed
6. Telegram 완료 알림:

   ✅ [monitor-01] 완료
   
   결과: Layer 2 프로덕트 품질 대시보드 정상화
   원인: Mock Exporter 누락
   조치: exporter 복원 + scrape config 추가 + 스택 재시작
   소요: Heartbeat 3회
   
   교훈: docker-compose 서비스 제거 시 관련 대시보드 영향도 체크 필요
```

### 사용자가 한 일: 총 2가지

1. **Intent 선언**: "Layer2 미동작, 지표 수집되게 해줘" → INTENTS.md에 작성
2. **L2 승인**: Telegram에서 ✅ 한 번 탭

나머지 — 원인 분석, exporter 코드 작성, 설정 수정, 배포, 검증, 보고 — 전부 에이전트 자율 수행.

## 구현 로드맵

### Phase 0: 증명 — monitor-01로 E2E 검증

**목표**: Intent 선언 → Heartbeat 실행 → Telegram 알림까지 한 사이클 동작 증명

- [x] INTENTS.md 생성 + monitor-01 Intent 선언
- [x] PERMISSIONS.md 생성
- [x] GATES.md 생성
- [ ] Telegram Bot 알림 연동 (기존 Bot 활용)
- [ ] Heartbeat Agent 스킬 작성 (.agent/workflows/heartbeat.md)
- [ ] Heartbeat 1회 수동 실행 → monitor-01 분석 → Telegram 알림 수신 확인
- [ ] Heartbeat 2회 수동 실행 → Mock Exporter 코드 작성 → L2 승인 요청 확인
- [ ] 승인 후 Heartbeat 3회 → 배포 → 검증 → 완료 알림 확인

### Phase 1: 자동화 (Phase 0 증명 후)
- [ ] `/schedule`로 Heartbeat cron 등록
- [ ] .agent/reports/ 로깅 자동화
- [ ] 두 번째 Intent 추가 (다른 유형의 작업)

### Phase 2: Gate 시스템 (2-3일)
- [ ] L2 승인 흐름 구현 (Telegram → GATES.md → 다음 Heartbeat 실행)
- [ ] 승인/거부 응답 처리 로직
- [ ] blocked 상태 관리

### Phase 3: 복합 실행 (1주)
- [ ] workflow-master 연동 (복잡한 Intent → 4-role 실행)
- [ ] Intent 간 의존성 처리
- [ ] 자동 학습 루프 (실행 결과 → lessons-learned.md → 에이전트 개선)

### Phase 4: 자가 진화 (지속)
- [ ] Intent 성공률 추적
- [ ] Heartbeat 주기 자동 조정
- [ ] 권한 레벨 승격 제안 (L2 → L1로 자동화 가능한 패턴 감지)
- [ ] 새로운 Intent 자동 제안 (반복 패턴 감지)

## 측정 지표

| 지표 | 설명 | 목표 |
|------|------|------|
| 자율 실행률 | L0+L1 실행 / 전체 실행 | 70% 이상 |
| Gate 응답 시간 | L2 요청 → 사용자 응답 | 30분 이내 |
| Intent 완료율 | 완료 / 선언된 전체 | 주간 추적 |
| 사용자 개입 횟수 | Heartbeat당 사용자가 직접 개입한 횟수 | 감소 추세 |
| 에이전트 정확도 | 에이전트 실행 결과의 품질 | 상승 추세 |

---

## 레퍼런스

- [Paperclip](https://github.com/paperclipai/paperclip) — Heartbeat 아키텍처, 예산 제어, 조직 계층
- [Superpowers](https://github.com/obra/superpowers) — Plan 기반 자율성, 2단계 리뷰, 서브에이전트
- [gstack](https://news.hada.io/topic?id=27756) — Think→Ship 파이프라인, 컨텍스트 체이닝, 자동 회고
- [Karpathy Guidelines](https://github.com/forrestchang/andrej-karpathy-skills) — 가정 명시화, 검증 가능한 기준, 최소 변경
