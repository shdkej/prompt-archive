# EVALUATION_INDEX

Infinity evaluator가 매 실행마다 `EVALUATION_NOTES.md` 전체를 다시 읽지 않도록 유지하는 요약 인덱스다.

## 읽기 규칙
- 정기 evaluator는 이 파일과 `EVALUATION_NOTES.md`의 최근 80줄만 읽는다.
- `EVALUATION_NOTES.md` 전체 재독해는 사용자가 명시적으로 감사/audit를 요청하거나, 최근 80줄과 이 인덱스가 서로 충돌할 때만 허용한다.
- 새 평가가 기존 패턴을 바꾸는 수준이면 이 인덱스도 짧게 갱신한다.

## 현재 반복 패턴
- **Registry 우선**: `INTENTS.md`가 단일 진실 원천이어야 한다. report/archive/heartbeat의 다음 단계 문구는 registry 상태와 맞아야 한다.
- **Blocked는 상태 필드로**: 장기 blocked, 승인 대기, 채널 실패는 report 누적보다 `status`, `blocked_reason`, `channel_state`, `next_check_at`, `owner_action/user_action` 같은 필드로 남기는 편이 낫다.
- **승인 해소 후 resume**: `GATES.md`가 resolved 되었으면 다음 정시 heartbeat를 기다리지 말고 `approved_at`, `resume_deadline`, `last_progress_at`을 남기거나 즉시 resume 후보로 올려야 한다.
- **완료 검증**: 배포형 intent는 URL 200만으로 닫지 말고 핵심 콘텐츠 경로 2~3개와 사용자 시나리오 기준 검증을 통과해야 한다.
- **후속 intent 연속성**: 같은 프로젝트의 후속 Inbox가 이미 있으면 재등록을 요구하지 말고 기존 식별자/phase 또는 명확한 새 번호 규칙으로 이어받아야 한다.
- **Idle 감시**: Active가 비어도 새 Inbox 유입과 마지막 heartbeat age를 감시해 pickup 공백이 며칠씩 생기지 않게 해야 한다.
- **반복 평가 억제**: 같은 blocked/승인/idle 문제를 새 근거 없이 반복 append하지 않는다. 새로운 운영 결정을 바꿀 때만 평가 노트를 추가한다.

## 토큰 예산
- 정기 실행 목표: 총 토큰 3만 이하.
- `EVALUATION_NOTES.md` 읽기 한도: 최근 80줄 기본, 최대 120줄.
- 추가 파일 탐색은 최근 heartbeat/report 1~2개로 제한한다.
