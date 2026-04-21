# EVALUATION_NOTES

Infinity intent 처리 품질을 평가해 다음 pickup/구조화/실행에서 참고하기 위한 문서.

## 평가 원칙
- intent를 어떻게 다뤘는지가 다음 운영 판단에 도움 되는 경우만 남긴다.
- pickup 방식, 병렬도, 승인 흐름, 결과 보고 품질을 본다.
- 단순 완료 여부보다 운영 흐름 적합성을 평가한다.

## 기록 템플릿
- 대상 intent:
- 평가:
- 근거:
- 다음에 유지할 것:
- 다음에 바꿀 것:

## 현재 기준
- intent 시스템은 실행 자체보다 구조화와 운영 흐름의 품질이 더 중요하다.
- 동시성은 많을수록 좋은 게 아니라 안정성과 품질을 해치지 않는 수준이어야 한다.
- 보고는 자세함보다 사용자가 다음 판단을 하기 쉽게 만드는 쪽으로 평가한다.

- 대상 intent: Inbox의 신규 2건 전체
- 평가: pickup 이전 단계가 멈추면 구조화·병렬도·승인 흐름 품질을 평가할 기회 자체가 사라지므로, Heartbeat의 최우선 품질 지표는 최신 Inbox를 Active로 옮기는 주기 신뢰성이다.
- 근거: 최신 heartbeat report는 2026-04-14에 idle인데 현재 INTENTS.md Inbox에는 아직 구조화되지 않은 신규 intent 2건이 남아 있다.
- 다음에 유지할 것: Active가 비었을 때 조용히 종료하는 보고 방식 자체는 간결하다.
- 다음에 바꿀 것: 최근 heartbeat 부재나 Inbox 잔류를 즉시 드러내는 감시 규칙을 추가해 pickup 누락이 며칠간 숨지 않게 한다.

- 대상 intent: Inbox의 신규 2건 전체
- 평가: 최신 Heartbeat가 "Inbox 비어있음"으로 기록했는데 실제 Inbox에는 항목이 남아 있으면, pickup 품질 문제를 넘어 운영 상태 관측 자체가 신뢰 불가가 된다.
- 근거: 2026-04-14T09:00 heartbeat report는 Inbox 비어있음으로 종료했지만 현재 INTENTS.md에는 리서치/구축 intent 2건이 그대로 남아 있다.
- 다음에 유지할 것: Idle heartbeat도 단계별 판단 근거를 짧게 남기는 형식은 좋다.
- 다음에 바꿀 것: Heartbeat 종료 직전에 INTENTS.md Inbox/Active 개수를 다시 검증해 보고 내용과 실제 상태가 다르면 idle로 끝내지 말고 pickup 실패로 기록해야 한다.

- 대상 intent: Inbox의 리서치/구축/구현 3건 전체
- 평가: pickup 누락이 며칠간 지속된 상태에서 Inbox 항목이 늘어나면 개별 intent 품질 이전에 시스템이 새 일을 받아도 처리 단계로 진입하지 못하는 것이 핵심 실패다.
- 근거: 최신 heartbeat report는 여전히 idle인데 현재 INTENTS.md Inbox에는 기존 2건에 더해 [구현] wiki-01까지 추가되어 Active는 비어 있고 backlog만 증가했다.
- 다음에 유지할 것: Active를 분리해 구조화 이후 상태를 명확히 나누는 레지스트리 틀 자체는 유효하다.
- 다음에 바꿀 것: Inbox가 연속 heartbeat 1회 이상 남아 있으면 idle 종료를 금지하고, 최소 1건을 Active로 옮기거나 pickup 실패 사유와 재시도 계획을 강제로 남기게 해야 한다.
