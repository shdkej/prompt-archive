---
name: infinity
description: 자유 형식 요청을 Infinity Intent로 접수하거나 /infinity로 상태·승인·실행을 요청할 때 현재 운영 절차를 찾는다.
---

# Infinity — Agent-First Workflow

사용자는 원하는 결과와 제약을 전달한다. 에이전트는 같은 Intent에 진행 상태와 완료 증거를 연결하고, 판단이 필요하면 대기 이유와 재개 조건을 남긴다.

**목차** · [스킬 동작](#스킬-동작) · [설계 원칙](#설계-원칙) · [레퍼런스](#레퍼런스)

## 스킬 동작

| 요청 | 확인할 대상과 행동 |
| --- | --- |
| `/infinity <요청>` | 기존 Intent와 중복되는지 확인한다. 새 요청은 목표와 완료 기준을 정리해 현재 YAML 원장의 Inbox에 접수한다. [접수·라우팅 기준](https://github.com/shdkej/knowledge-lab/blob/main/source/openclaw-system/docs/INFINITY_OPERATING_RULES.md) |
| `/infinity status` | [현재 원장](https://github.com/shdkej/infinity/blob/main/INTENTS.yaml)의 `lanes`에서 상태와 다음 행동을 읽는다. Waiting은 대기 담당과 재개 조건을 함께 확인한다. |
| `/infinity 승인`, `/infinity approve` | 대상 Intent와 [승인 항목](https://github.com/shdkej/infinity/blob/main/GATES.md)을 특정하고, [권한 기준](https://github.com/shdkej/infinity/blob/main/PERMISSIONS.md)에 따라 승인 주체와 범위를 확인한다. |
| `/infinity run` | [Heartbeat](https://github.com/shdkej/infinity/blob/main/heartbeat.md)에서 실행 선행 조건을 확인하고 [명령 실행 절차](https://github.com/shdkej/infinity/blob/main/docs/command-execution.md)를 따른다. |

완료 처리에는 산출물과 보고서를 연결하고 원격 Archive 카드에서 결과 링크를 확인한다. 세부 절차는 [산출물 기준](https://github.com/shdkej/infinity/blob/main/ARTIFACT_RULES.md), 운영 품질 점검은 [Evaluator](https://github.com/shdkej/infinity/blob/main/docs/infinity-evaluator.md)를 따른다.

## 설계 원칙

| 원칙 | 설명 | 출처 |
|------|------|------|
| Heartbeat Loop | 에이전트가 스케줄에 따라 깨어나서 일감 확인→실행→보고→수면 | Paperclip |
| Plan-Based Autonomy | 검증된 계획 안에서 수시간 자율 작업 가능 | Superpowers |
| Context Chaining | 각 단계의 산출물이 다음 단계의 입력으로 자동 전달 | gstack |
| Verifiable Criteria | 모호한 목표 대신 측정 가능한 성공 기준 | Karpathy |
| Permission Boundary | 자율성은 무제한이 아니라 등급별 경계 안에서 작동 | 공통 |
| Reuse Before Create | 새 컴포넌트 생성 전 기존 리소스 활용 가능 여부를 먼저 확인 | Lesson Learn |
| Cloud-Prep-First | 클라우드는 로컬 실행을 대체하지 않고 조사·정리·초안·순서화로 로컬 부담을 줄인다 | Infinity |


클라우드는 조사·비교·초안처럼 미리 할 수 있는 일을 맡고, 로컬 세션은 파일·브라우저·테스트처럼 실제 환경과 권한이 필요한 일을 맡는다. 실행 위치를 고를 때는 현재 환경에서 결과를 직접 검증할 수 있는지 확인한다.

로컬 Claude Code에 복잡한 Intent, 단순하지 않은 코드 작업, 또는 규모와 관계없이 공통 동작을 바꾸는 작업을 맡길 때는 목표·제약·완료 기준·검증 대상을 전달한다. 대상 저장소의 workflow-master 지침을 먼저 확인하고, 별도 지침이 없으면 [공용 워크플로우 마스터](skills/custom/workflow-master/SKILL.md)를 따른다.

## 레퍼런스

- [Paperclip](https://github.com/paperclipai/paperclip) — Heartbeat 아키텍처
- [Superpowers](https://github.com/obra/superpowers) — Plan 기반 자율성
- [gstack](https://news.hada.io/topic?id=27756) — Think→Ship 파이프라인
- [Karpathy Guidelines](https://github.com/forrestchang/andrej-karpathy-skills) — 검증 가능한 기준
