---
name: infinity
description: Agent-First 의도 등록 스킬. 자유 형식으로 의도를 선언하면 infinity/INTENTS.md에 추가하고 push한다. 사용 시기 - (1) "이거 해줘", "모니터링 해줘" 등 에이전트에게 맡길 일, (2) "/infinity 뭐뭐 해줘", (3) Intent 상태 확인, (4) Gate 승인
---

# Infinity — Agent-First Workflow

> "내가 에이전트를 돌리는게 아니라 에이전트가 돌다가 나한테 알려주게 해야한다"

## 스킬 동작

### 1. Intent 추가 (`/infinity <자유 형식>`)

사용자가 자유 형식으로 의도를 말하면:

1. `infinity/INTENTS.md`의 `## Inbox`에 추가
2. 커밋 & 푸시
3. "Intent 등록 완료. 다음 Heartbeat에서 처리됩니다." 응답

예시:
- `/infinity layer2 안 돼`
- `/infinity 보안교육 PA Flow 이번달까지`
- `/infinity KOP 빌드 실패하면 알려줘`

### 2. 상태 확인 (`/infinity status`)

- `infinity/INTENTS.md`의 Active 섹션 표시
- `infinity/GATES.md`의 대기 중 항목 표시
- 최근 리포트 요약

### 3. 승인 (`/infinity 승인` 또는 `/infinity approve`)

- `infinity/GATES.md`에 대기 중인 항목을 승인 처리
- status: blocked → in_progress로 변경
- 커밋 & 푸시

### 4. 즉시 실행 (`/infinity run`)

- 원격 Heartbeat 트리거를 즉시 실행
- 트리거 ID: `trig_01Fubp8g8UDKQtvuSkFofPuM`

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
