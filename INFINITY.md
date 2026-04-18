---
name: infinity
description: Agent-First 의도 등록 스킬. 자유 형식으로 의도를 선언하면 infinity/INTENTS.md에 추가하고 push한다. 사용 시기 - (1) "이거 해줘", "모니터링 해줘" 등 에이전트에게 맡길 일, (2) "/infinity 뭐뭐 해줘", (3) Intent 상태 확인, (4) Gate 승인
---

# Infinity — Agent-First Workflow

> "내가 에이전트를 돌리는게 아니라 에이전트가 돌다가 나한테 알려주게 해야한다"

> 운영 시 `infinity/OPERATING_LESSONS.md`가 있으면 함께 읽고, 누적된 운영 교훈을 현재 intent 처리 방식에 반영한다.

## 스킬 동작

**중요: 이 스킬은 Intent 등록과 상태 관리만 수행한다. Intent의 실제 작업 실행은 절대 하지 않는다. 실행은 원격 Heartbeat Agent가 담당한다.**

### 1. Intent 추가 (`/infinity <자유 형식>`) — 기본 동작

사용자가 자유 형식으로 의도를 말하면:

1. `infinity/INTENTS.md`의 `## Inbox`에 `- {입력 내용}` 한 줄 추가
2. 커밋 & 푸시
3. "Intent 등록 완료. 다음 Heartbeat에서 처리됩니다." 응답
4. **여기서 끝. 분석, 구조화, 실행 등 추가 작업을 하지 않는다.**

예시:
- `/infinity layer2 안 돼`
- `/infinity 보안교육 PA Flow 이번달까지`
- `/infinity KOP 빌드 실패하면 알려줘`

### 2. 상태 확인 (`/infinity status`)

- `infinity/INTENTS.md`의 Active 섹션 표시
- `infinity/GATES.md`의 대기 중 항목 표시

### 3. 승인 (`/infinity 승인` 또는 `/infinity approve`)

- `infinity/GATES.md` 대기 중 항목을 처리 완료로 이동
- `infinity/INTENTS.md`에서 blocked → in_progress로 변경
- 커밋 & 푸시

### 4. 즉시 실행 (`/infinity run`)

- RemoteTrigger로 `trig_01Fubp8g8UDKQtvuSkFofPuM` 즉시 실행

---

# 설계 문서

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
│  GitHub Action       푸시 감지 → Telegram 알림 발송      │
│  infinity/reports/   실행 결과 로그 (영구 저장)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Intent 설계

### 구조

```markdown
## [intent-id] 의도 이름
- status: declared | active | in_progress | blocked | completed
- priority: critical | high | medium | low
- heartbeat: 30m | 1h | 4h | daily | weekly
- permission: L0 | L1 | L2
- project: 프로젝트 경로 또는 이름
- deadline: YYYY-MM-DD (선택)
- goal: 이 의도가 달성되면 어떤 상태인지 한 줄로
- success_criteria:
  - 측정 가능한 기준
- context: 관련 파일, URL, 참고 정보
- constraints: 하지 말아야 할 것, 제약 조건
```

### 생명주기

```
declared ──→ active ──→ in_progress ──→ completed ──→ archive/로 이관
                │              │
                │              └──→ blocked (승인 대기) ──→ in_progress
                │
                └──→ cancelled
```

## Heartbeat 동작 흐름

```
[Heartbeat 기상 (매 시간)]
    │
    ├── 1. Inbox 확인 → 자유 형식을 구조화하여 Active로 이동
    │
    ├── 2. Active에서 활성 Intent 필터링
    │   └── critical > high > medium > low, deadline 임박 우선
    │
    ├── 3. 각 Intent별 상태 점검
    │   ├── 이전 리포트 확인 (infinity/reports/)
    │   └── 다음 액션 결정
    │
    ├── 4. 권한 레벨 확인
    │   ├── L0/L1 → 자율 실행
    │   └── L2 → GATES.md 등록 + Telegram 승인 요청
    │
    ├── 5. 실행 (한 번에 하나의 Intent만)
    │   ├── 간단 → 단일 에이전트
    │   └── 복잡 → workflow-master 호출
    │
    ├── 6. 결과 기록 → infinity/reports/{intent-id}/{timestamp}.md
    │
    ├── 7. completed → infinity/intents/archive/로 이관
    │
    └── 8. 커밋 & 푸시 → GitHub Action → Telegram 알림
```

## Gate 승인 흐름

```
에이전트: L2 필요 → GATES.md 대기 등록 + Telegram 승인 요청
    │
    └── Intent status → blocked

사용자: Telegram 알림 수신 → /infinity 승인 (Claude Code에서)
    │
    ├── 승인 → 다음 Heartbeat에서 실행
    ├── 거부 → 대안 탐색
    └── 수정 → 방향 조정 후 재실행
```

## 기존 시스템 통합

Heartbeat Agent는 workflow-master의 **상위 계층**.
기존 워크플로우를 대체하지 않고, 언제 어떤 워크플로우를 실행할지 결정하는 지휘관.

| 기존 스킬 | Agent-First에서의 역할 |
|-----------|----------------------|
| `/workflow-master` | 복잡한 Intent 실행 시 4-role 오케스트레이션 |
| `/kop-workflow` | KOP Intent 실행 시 호출 |
| `/brand-monitor` | 브랜드 모니터링 Intent 실행 시 호출 |
| `/daily-feedback-system` | daily heartbeat에서 자동 호출 |

## 측정 지표

| 지표 | 설명 | 목표 |
|------|------|------|
| 자율 실행률 | L0+L1 실행 / 전체 실행 | 70% 이상 |
| Gate 응답 시간 | L2 요청 → 사용자 응답 | 30분 이내 |
| Intent 완료율 | 완료 / 선언된 전체 | 주간 추적 |
| 사용자 개입 횟수 | Heartbeat당 사용자 개입 | 감소 추세 |

## 시스템 구조

```
infinity/
├── INTENTS.md          # Inbox(자유 형식) + Active(구조화)
├── PERMISSIONS.md      # L0~L3 권한 경계
├── GATES.md            # 승인 대기 큐
├── workflows/
│   └── heartbeat.md    # Heartbeat Agent 프로토콜
├── reports/            # 실행 리포트
├── intents/archive/    # 완료 Intent 보관
└── scripts/notify.sh   # Telegram 알림 (로컬용)
```

## 권한 레벨

| 레벨 | 이름 | 에이전트 행동 |
|------|------|-------------|
| L0 | 자율 | 실행 후 변화 있을 때만 알림 |
| L1 | 알림 | 실행 후 결과 알림 |
| L2 | 승인 | GATES.md 등록 + Telegram 승인 요청 |
| L3 | 금지 | 실행하지 않음 |

## Heartbeat

- 스케줄: 매 시간 (원격 트리거, claude-sonnet-4-6)
- Telegram 알림: KST 08~22시만, 08시에 아침 리캡
- 원격 에이전트 = 관제탑 (계획, 분석, 파일 수정, 커밋)
- 로컬 실행 필요 시 Telegram으로 안내

## 핵심 원칙

- **Reuse Before Create**: 새 컴포넌트 전에 기존 리소스 활용 확인
- **Inbox 자유 형식**: 사용자는 양식 신경 쓰지 않음, 에이전트가 구조화
- **완료 아카이브**: INTENTS.md는 활성만, 완료는 intents/archive/로 이관

## 레퍼런스

- [Paperclip](https://github.com/paperclipai/paperclip) — Heartbeat 아키텍처
- [Superpowers](https://github.com/obra/superpowers) — Plan 기반 자율성
- [gstack](https://news.hada.io/topic?id=27756) — Think→Ship 파이프라인
- [Karpathy Guidelines](https://github.com/forrestchang/andrej-karpathy-skills) — 검증 가능한 기준
