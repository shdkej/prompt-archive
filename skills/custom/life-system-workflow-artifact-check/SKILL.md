---
name: life-system-workflow-artifact-check
description: 나·목표·에이전트·문서의 4레이어 운영 흐름을 점검한다. 일일·주간 회고나 cron·heartbeat에서 목표가 실행·산출물로 이어졌는지, 레이어 경계와 블록 타임이 지켜졌는지 확인할 때 사용한다.
---

# life-system-workflow-artifact-check

**목차**

- [언제 쓰나](#언제-쓰나)
- [핵심 모델](#핵심-모델)
- [방화벽 규칙](#방화벽-규칙)
- [먼저 읽을 것](#먼저-읽을-것)
- [절차](#절차)
- [판정 기준](#판정-기준)
- [금지](#금지)

## 언제 쓰나

사용자의 나-목표-에이전트-문서(디테일) 4레이어 운영 구조가 실제로 돌고 있는지 점검할 때 사용한다.

트리거:

- 사용자가 `4레이어`, `나 목표 에이전트 문서`, `삶 시스템 워크플로우 아티팩트`, `PDCA`, `오늘 목표`, `시스템 점검`, `흐름이 잘 도는지 봐줘`라고 말할 때
- 일일/주간 회고에서 목표와 실제 실행, Knowledge Lab/Infinity/문서/코드 산출물, workflow-master 적용 여부를 함께 봐야 할 때
- cron 또는 heartbeat가 하루 운영 루프를 점검할 때

## 핵심 모델

네 레이어를 섞지 않고 본다.

1. `나` — 가설을 세우고 검증하며, 지표로 성과를 확인하고, 성공/실패를 성장 기록으로 남기는 층. 대표 지표는 `learning_loop_closed`.
2. `목표` — 오늘 무엇을 성공으로 볼지 정한 한 문장. 대표 지표는 `goal_clarity`.
3. `에이전트` — SAM, 서브에이전트, cron, workflow-master 실행층. 대표 지표는 `agent_followthrough`.
4. `문서(디테일)` — Knowledge Lab, 코드, 리포트, 대시보드, 카드뉴스, 원장. 대표 지표는 `detail_reusability`.

기본 피드백 흐름:

`가설 설정 → 검증 지표 선택 → 목표 1문장 → 에이전트 실행/검증 → 문서(디테일) 갱신 → 성과 판정/배운 점 기록 → 사용자 피드백`

## 방화벽 규칙

### L1 나 ↔ L2 목표

상태만 전달한다.

허용:

- 오늘의 가설
- 검증 방법
- 확인할 지표
- 성공/실패 판정
- 배운 점과 내일 조정
- 내일 조정

금지:

- 카피 문구, 광고 세팅, 문서 구조, 오타, 작업 순서 같은 원시 디테일을 나 레이어로 올리기
- 나 레이어에서 목표를 작업 목록으로 쪼개기

### L2 목표 ↔ L3 에이전트

목표만 전달한다.

- 목표는 한 문장으로 둔다.
- 에이전트는 실행, 검증, 다음 액션까지 닫는다.
- 에이전트 내부 로그와 명령 출력은 목표 레이어로 역류시키지 않는다.

### L3 에이전트 ↔ L4 문서

일방향 흐름을 지킨다.

- 문서는 에이전트 실행의 근거와 디테일 저장층이다.
- 현재 목표와 관련된 문서만 연다.
- 문서 디테일이 에이전트 실행 목표를 흔들면 중단한다.
- 문서를 닫기 전 `다음 에이전트 실행의 첫 행동 1줄`을 남긴다.

## 먼저 읽을 것

필수:

- `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/reviews/LIFE_SYSTEM_WORKFLOW_ARTIFACT.md`
- `/home/ubuntu/.openclaw/workspace/USER.md`
- `/home/ubuntu/.openclaw/workspace/AGENTS.md`

상황별:

- 산출물/기획/구현/마케팅/운영 판단이면 `/home/ubuntu/workspace/prompt-archive/.agent/workflows/workflow-master.md`
- 필요한 관점 파일:
    - `/home/ubuntu/workspace/prompt-archive/.agent/workflows/planner.md`
    - `/home/ubuntu/workspace/prompt-archive/.agent/workflows/developer.md`
    - `/home/ubuntu/workspace/prompt-archive/.agent/workflows/marketer.md`
    - `/home/ubuntu/workspace/prompt-archive/.agent/workflows/operator.md`
- 장기 프로젝트나 지식 근거가 필요하면 Knowledge Lab/agent-wiki 관련 문서
- 하루 흐름 점검이면 최근 daily review, memory/YYYY-MM-DD.md, relevant /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs

## 절차

### 1. 범위 확정

점검 대상이 하루, 특정 프로젝트, 특정 산출물, 시스템 설정 중 무엇인지 정한다.

- 하루 점검: 나와 목표를 먼저 본다.
- 산출물 점검: 에이전트와 문서를 먼저 본다.
- 시스템 변경 점검: 에이전트 실행 경계와 문서 정본 반영을 본다.
- Knowledge Lab/Infinity 관련 점검: 문서 근거와 push/대시보드 가시성을 확인한다.

### 2. 나 확인

확인할 것:

- 오늘의 가설이 보이는가?
- 검증 방법과 확인할 지표가 있는가?
- 성과가 성공/실패/보류 중 하나로 판정됐는가?
- 성과 판정의 근거 출처가 있는가?
- 결과가 배운 점으로 기록됐는가?
- 업무 디테일이 나 레이어로 올라오지 않았는가?

없으면:

- 가설, 검증 지표, 성과 판정 중 하나만 묻거나 `null`로 보류한다.
- 성과 판정의 근거 출처가 없으면 성공 처리하지 않는다.

### 3. 목표 확인

확인할 것:

- 오늘 목표가 한 문장인가?
- 완료/부분 완료/보류/차단 중 하나로 닫혔는가?
- 다음 조정이 사용자의 일을 줄이는가?

없으면:

- 상세 작업 목록 대신 목표 한 문장만 제안한다.

### 4. 에이전트 확인

확인할 것:

- 에이전트가 목표를 실행했는가?
- 검증 결과가 있는가?
- 다음 액션이 남았는가?
- 산출물 작업이면 workflow-master가 실제로 참견했는가?
- Planner/Developer/Marketer/Operator 최소 체크가 수행되었는가?
- 4관점이 산출물을 키우기보다 누락을 줄였는가?

요약 기준:

- Planner: 목표, 맥락, 완료 기준, 줄일 범위
- Developer: 구현 경로, 데이터/파일 경계, 테스트·검증
- Marketer: 이름, 카피, 첫인상, 가치 전달
- Operator: 배포, 롤백, 로그, 보안, 비용, 반복 운영, 원격 가시성

### 5. 문서 확인

확인할 것:

- 실제로 바뀌거나 검증된 표면은 무엇인가?
- Knowledge Lab/Infinity/프로젝트 문서와 연결되는가?
- 사용자가 직접 확인할 수 있는 링크, 파일, 대시보드, 커밋, report가 있는가?
- 문서를 닫기 전 다음 에이전트 실행 액션 1줄이 남았는가?

주의:

- 문서는 결론이 아니라 근거다. 최종 판단은 에이전트 실행과 SAM 검증을 거쳐 사용자에게 돌아가야 한다.
- 문서의 지저분함이나 주변 TODO가 현재 목표를 끌고 다니면 방화벽 실패로 본다.

### 5.5 Bottom-Up 압축 확인

하위 레이어의 원시 디테일이 상위 레이어로 그대로 올라가지 않았는지 확인한다.

- 문서 → 에이전트: `다음 액션 1줄`로 압축됐는가?
- 에이전트 → 목표: `완료 / 부분 완료 / 보류 / 차단`으로 압축됐는가?
- 목표 → 나: `성과 판정 / 배운 점 / 내일 조정`으로 압축됐는가?

### 6. Feedback 작성

Telegram/OpenClaw 출력은 짧은 섹션 + 불릿으로 작성한다. 표는 쓰지 않는다.

기본 형식:

```text
4레이어 점검

나:
- 오늘 가설:
- 검증 지표:
- 성과 판정/배운 점:

목표:
- 오늘 목표 1문장:
- 완료 상태:
- 다음 조정:

에이전트:
- 실행/검증:
- 남은 blocker:
- 다음 액션:

문서:
- 갱신/검증된 디테일:
- 재사용 가능성:

다음 손잡이:
- 내일 블록 조정:
```

- 점검을 마치면 4지표 판정을 확인하되, `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/quality-gates/layer-check.jsonl`의 당일 라인은 밤 데일리 리뷰(23:00)만 append한다. 07:00 리캡/아침 점검은 당일 라인을 쓰지 않고, 어제 라인이 비어 있을 때만 정본 문서 기준으로 백필한다. 기록 형식의 정본은 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/reviews/LIFE_SYSTEM_WORKFLOW_ARTIFACT.md`의 필수 품질 게이트 섹션이다.
- 이어서 지연 게이트(E1~E4)를 판정해 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/quality-gates/effectiveness.jsonl`에 append한다. 절차의 정본은 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/reviews/LIFE_SYSTEM_WORKFLOW_ARTIFACT.md`의 지연 게이트 소절이다.

## 판정 기준

좋은 상태:

- 나의 상태가 보이고, 목표가 한 문장으로 잡혀 있다.
- 목표가 완료/부분 완료/보류/차단 중 하나로 닫힌다.
- 에이전트가 실행, 검증, 다음 액션까지 닫는다.
- 문서(디테일)가 Knowledge Lab/코드/리포트 등 실제 표면으로 남았고 다음 액션 1줄이 있다.
- SAM의 피드백이 완료 상태, 성과 판정, 배운 점, 내일 조정으로 압축되어 사용자의 다음 행동을 줄인다.

주의 상태:

- 목표 없이 산출물만 늘었다.
- 목표가 상세 작업 목록으로 쪼개졌다.
- 에이전트 내부 로그와 문서 디테일이 나/목표 레이어로 올라왔다.
- 새 규칙이 memory나 대화에만 남았다.
- workflow-master를 말로만 언급하고 역할 파일을 보지 않았다.
- 문서 오타/정리 욕구가 오늘 핵심 워크플로우를 밀어냈다.
- Knowledge Lab 근거 없이 새 해석만 늘었다.
- 검증, push, 대시보드 확인 없이 완료 보고했다.

## 금지

- 사용자의 나 상태, 목표, 에이전트 실행, 문서 디테일을 한 덩어리로 뭉개서 보고하지 않는다.
- 밤 PDCA에 문서/카피/광고/코드 디테일을 그대로 올리지 않는다.
- 블록 타임 밖에서 작업 순서와 문서 디테일을 계속 계산하게 만들지 않는다.
- cron 실행 중 새 작업을 크게 벌리지 않는다.
- 사용자 승인 없이 외부 발송, 공개 게시, 비용 발생, 자격증명 변경, 배포를 하지 않는다.
- 부족한 점을 과장하거나 사용자의 할 일을 늘리는 방향으로 끝내지 않는다.
