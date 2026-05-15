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

- 대상 intent: 2026-04-18 Inbox의 wiki-01 설계/구현 연속 요청
- 평가: 선행 설계를 완료한 직후 이미 Inbox에 있던 후속 구현 요청을 다시 사용자 재등록 과제로 돌리면 pickup은 회복돼도 intent 연속성이 끊긴다.
- 근거: heartbeat는 wiki-01 설계를 completed로 닫으면서 "구현 원하면 Inbox에 추가 요청 필요"라고 적었지만, 현재 INTENTS.md Inbox에는 이미 `[구현] wiki-01 구현 진행` 항목이 남아 있다.
- 다음에 유지할 것: 서로 다른 프로젝트의 리서치와 설계를 같은 heartbeat에서 병렬 처리한 판단은 적절했다.
- 다음에 바꿀 것: Inbox에 같은 프로젝트의 후속 단계가 이미 있으면 완료 보고에서 재등록을 요구하지 말고, 즉시 구조화해 blocked/active 후속 intent로 연결하거나 최소한 다음 heartbeat 인계 대상으로 명시해야 한다.

- 대상 intent: 2026-04-18 Heartbeat의 Inbox 3건 처리
- 평가: 실행 동시성 제한과 별개로 pickup 단계에서는 Inbox 전체를 구조화해야 하는데, 3건 중 2건만 Active로 옮기고 1건을 원문 Inbox에 남기면 시스템이 실행 대기와 미등록 상태를 구분하지 못한다.
- 근거: heartbeat report는 research-05와 wiki-01만 Inbox→Active 전환했다고 기록했고, 현재 INTENTS.md Inbox에는 같은 시점에 들어와 있던 `[구현] wiki-01 구현 진행` 항목이 그대로 남아 있다.
- 다음에 유지할 것: 서로 다른 프로젝트 2건만 실제 실행한 병렬도 판단은 보수적이고 안정적이다.
- 다음에 바꿀 것: Heartbeat 시작 시 Inbox 항목은 실행 여부와 무관하게 전부 구조화 등록하고, 같은 프로젝트 후속 작업은 Active의 declared/blocked 대기열로 남겨 실행 스케줄링 단계에서만 보류해야 한다.

- 대상 intent: 2026-04-18의 wiki-01 설계 완료 후 구현 인계
- 평가: 설계 intent를 archive에서 `wiki-02` 같은 신규 번호 후속으로 넘기겠다고 적고 실제 Inbox에는 `[구현] wiki-01`이 남아 있으면, 후속 실행보다 먼저 식별자 연속성이 깨져 pickup과 보고를 다시 헷갈리게 만든다.
- 근거: archive/wiki-01.md의 Next는 `wiki-02 Intent 등록`을 말하지만, 현재 INTENTS.md Inbox에는 이미 `[구현] wiki-01 구현 진행`이 존재한다.
- 다음에 유지할 것: 설계와 구현을 분리해 권한 단계와 산출물을 나눈 판단은 좋다.
- 다음에 바꿀 것: 같은 프로젝트의 후속 단계는 새 번호를 만들지 기존 번호의 phase를 이어갈지 한 규칙으로 고정하고, archive의 Next와 Inbox/Active 표기를 항상 같은 식별자로 맞춰야 한다.

- 대상 intent: 2026-04-18 Heartbeat 이후 wiki-01 구현 대기 상태
- 평가: 같은 시점 산출물인 heartbeat report, archive Next, INTENTS Inbox가 서로 다른 다음 행동을 말하면 사용자는 물론 다음 heartbeat도 무엇을 pickup해야 하는지 다시 해석해야 해서 운영비용이 커진다.
- 근거: heartbeat report는 `신규 Inbox 항목 대기`와 `사용자가 Inbox에 추가 요청 필요`를 적었지만, archive/wiki-01.md는 `wiki-02 Intent 등록`을 말하고 실제 INTENTS.md Inbox에는 이미 `[구현] wiki-01 구현 진행`이 남아 있다.
- 다음에 유지할 것: heartbeat report와 intent archive에 다음 단계 메모를 남기는 습관 자체는 좋다.
- 다음에 바꿀 것: 완료 시점의 단일 진실 원천을 INTENTS.md로 고정하고, report/archive의 다음 단계 문구는 반드시 현재 registry 상태를 참조해 자동 생성하거나 복사해 쓰도록 제한해야 한다.

- 대상 intent: 2026-04-18 wiki-02 승인 대기 추적
- 평가: 승인 대기 intent는 heartbeat report에서 blocked로 반복 보고되는데 INTENTS.md가 in_progress로 남아 있으면, 승인 흐름과 실행 가능 상태를 다음 루프가 정확히 판단하기 어려워진다.
- 근거: 09:00·11:00·12:00 heartbeat report는 모두 `wiki-02 blocked 유지`로 적었지만 현재 INTENTS.md Active의 wiki-02 status는 `in_progress`다.
- 다음에 유지할 것: 승인 미수신 시간을 누적해 재알림 여부를 판단하는 heartbeat 보고 방식은 유용하다.
- 다음에 바꿀 것: 승인 대기 같은 운영상 핵심 상태는 report 서술이 아니라 INTENTS.md status에 먼저 반영하고, heartbeat는 그 상태 변화만 읽어 보고하게 해야 한다.

- 대상 intent: 2026-04-18 wiki-02 승인 재알림 추적
- 평가: 승인 흐름에서 '재알림 발송' 자체보다 실제 전달 성공 여부가 기록의 기준이 되어야 다음 heartbeat가 사용자 응답 부재와 알림 실패를 구분할 수 있다.
- 근거: 12:00 heartbeat report는 Telegram 재알림 발송을 적었지만 13:00 wiki-02 report는 외부 호스트 차단으로 알림 미발송 중이라고 적어, 같은 승인 대기 상태의 사용자 무응답과 채널 실패가 뒤섞여 보인다.
- 다음에 유지할 것: 승인 대기 시간을 누적해 재알림 필요성을 판단하는 루프 자체는 유용하다.
- 다음에 바꿀 것: 알림 관련 보고는 '시도'와 '전달 성공'을 분리하고, 외부 채널 실패 시에는 승인 미수신이 아니라 notification blocked 상태를 별도로 남겨 후속 heartbeat가 다른 알림 경로를 선택하게 해야 한다.

- 대상 intent: 2026-04-18 wiki-02 승인 대기와 완료 기준 정합성
- 평가: 승인 대기 intent의 현재 상태와 완료 조건이 실제 실행 경계와 어긋나 있으면, 다음 heartbeat가 무엇을 기다리는지보다 무엇이 이미 준비됐고 무엇이 사용자 수동 단계인지 다시 해석해야 한다.
- 근거: INTENTS.md의 wiki-02는 status가 `in_progress`이고 success_criteria에 `https://shdkej.github.io/agent-wiki/ 접속 가능`까지 포함하지만, 12:00 heartbeat와 13:00 wiki-02 report는 모두 승인 대기 blocked 상태로 설명하고 GitHub Pages 활성화는 사용자의 GitHub UI 수동 작업(L3)이라고 적고 있다.
- 다음에 유지할 것: 구현 파일 준비 완료와 사용자 수동 단계 존재를 개별 report에서 분리해 적는 습관은 좋다.
- 다음에 바꿀 것: 승인 대기 intent는 INTENTS.md에서 blocked로 먼저 반영하고, success criteria는 에이전트가 끝낼 수 있는 범위와 사용자 수동 후속 단계를 분리해 적어 heartbeat 종료 조건을 한눈에 보이게 해야 한다.

- 대상 intent: 2026-04-18 wiki-02 승인 대기 이후 알림 실패 상태
- 평가: 승인 대기 intent에서 외부 알림 실패가 확인됐으면, 그 시점부터는 단순 blocked가 아니라 사용자 접점이 끊긴 stalled 상태로 승격해 다음 heartbeat가 다른 전달 경로를 우선 선택하게 해야 한다.
- 근거: 12:00 heartbeat는 Telegram 재알림 발송으로 기록했지만 13:00 wiki-02 report는 Telegram 외부 호스트 차단으로 알림 미발송 중이라고 적었고, 현재 INTENTS.md Active의 wiki-02는 여전히 `in_progress`라 채널 실패가 운영 상태에 반영되지 않았다.
- 다음에 유지할 것: 구현 준비 완료 여부와 승인 미수신 시간을 지속 추적한 점은 좋다.
- 다음에 바꿀 것: 승인 요청 전달 실패가 확인되면 INTENTS.md status를 notification_blocked 같은 명시 상태로 바꾸고, 다음 heartbeat 보고도 재알림 반복 대신 대체 채널 선택 또는 수동 확인 요청으로 전환해야 한다.

- 대상 intent: 2026-04-18 wiki-02 오후 승인 대기 구간 전체
- 평가: blocked intent를 몇 시간째 그대로 둘 때는 같은 내용의 대기 보고보다 "다음 heartbeat가 언제 다시 볼지"와 "그 전까지 누가 액션 가능한지"를 고정해 두는 편이 운영 비용을 더 줄인다.
- 근거: 12:00 heartbeat는 승인 재알림 발송을 적었고 13:00 wiki-02 report는 Telegram 미발송 상태를 확인했지만, 17:57 현재 registry는 여전히 `in_progress`이며 이후 heartbeat 흔적 없이 운영 주체와 재확인 시점이 비어 있다.
- 다음에 유지할 것: 구현 준비 완료와 승인 의존성을 분리해 적어 실제 미해결 항목이 승인뿐임을 분명히 한 점.
- 다음에 바꿀 것: blocked가 1회 이상 반복되면 INTENTS.md에 next_check_at과 owner_action/user_action을 함께 남겨 heartbeat 공백이 생겨도 다음 pickup 판단이 문서만으로 이어지게 해야 한다.

- 대상 intent: 2026-04-18 wiki-02 승인 대기 장기화
- 평가: 승인 요청 전달 실패가 확인된 뒤에도 같은 blocked 보고만 반복되면, 시스템은 사용자 무응답과 알림 채널 장애를 구분하지 못한 채 멈춘다.
- 근거: 12:00 heartbeat는 Telegram 재알림 발송으로 기록했지만 13:00 wiki-02 report는 외부 호스트 차단으로 알림 미발송을 확인했고, 18:57 현재까지 후속 heartbeat나 대체 전달 경로 기록이 없다.
- 다음에 유지할 것: 구현 준비 완료와 승인 필요 여부를 분리해 실제 대기 원인을 좁혀 둔 점.
- 다음에 바꿀 것: 승인 알림이 실패하면 상태를 단순 blocked가 아니라 channel_blocked로 승격하고, 같은 루프 안에서 대체 채널 선택 또는 수동 점검 요청까지 남겨 stalled 상태를 숨기지 않게 해야 한다.

- 대상 intent: 2026-04-18 저녁 시점의 wiki-02 승인 대기
- 평가: blocked intent를 장시간 유지할수록 핵심 품질은 재알림 횟수가 아니라 registry가 현재 대기 이유와 다음 점검 시각을 한 줄로 보존하는지에 달려 있다.
- 근거: 13:00 report는 Telegram 차단을 확인했지만 19:57 현재 INTENTS.md의 wiki-02는 여전히 `in_progress`이고 next_check_at, owner_action, channel_blocked 같은 운영 상태가 없어 다음 heartbeat가 문서만 보고 즉시 판단하기 어렵다.
- 다음에 유지할 것: 구현 준비 완료와 사용자 승인 필요를 별도 report에서 분리해 둔 점.
- 다음에 바꿀 것: 승인 대기나 채널 장애가 확인되면 INTENTS.md를 단일 진실 원천으로 즉시 갱신해 status, blocked_reason, next_check_at, owner_action/user_action을 남기고 heartbeat report는 그 상태만 읽어 요약하게 해야 한다.

- 대상 intent: 2026-04-18 20:57 기준 wiki-02 장기 승인 대기
- 평가: heartbeat 공백이 길어질수록 별도 report에만 남은 blocked 맥락은 사실상 사라지므로, Active registry가 마지막 heartbeat 없이도 다음 행동을 복원할 수 있어야 운영이 계속 쉬워진다.
- 근거: wiki-02의 최신 heartbeat/report 흔적은 13:00에서 멈췄는데 20:57 현재 INTENTS.md는 여전히 `in_progress`만 표시하고 있어 승인 대기, Telegram 차단, 다음 확인 시각을 registry 단독으로는 복원할 수 없다.
- 다음에 유지할 것: 구현 준비 완료와 승인 필요를 intent report에 분리해 둔 점.
- 다음에 바꿀 것: report가 몇 시간 비어도 운영이 이어지도록 INTENTS.md Active 항목에 blocked_reason, channel_state, next_check_at, resume_condition을 필수 필드로 남겨 마지막 heartbeat 의존도를 줄여야 한다.

- 대상 intent: 2026-04-18 22:57 기준 wiki-02 승인 대기 지속
- 평가: 승인 대기 intent는 오래 멈춰도 핵심 상태가 registry에 먼저 반영돼야 하는데, 반나절 가까이 지난 뒤에도 `in_progress`로 남아 있으면 다음 heartbeat가 실행 재개보다 상황 재구성에 시간을 쓴다.
- 근거: 최신 heartbeat는 12:00, 최신 wiki-02 report는 13:00에서 멈췄고 그 안에는 승인 미수신과 Telegram 차단이 적혀 있지만 22:57 현재 INTENTS.md Active의 wiki-02는 여전히 `in_progress`이며 blocked 이유나 재확인 시각이 없다.
- 다음에 유지할 것: 승인 전 구현 산출물을 준비 완료 상태로 분리해 둔 점.
- 다음에 바꿀 것: 승인 미수신이나 알림 실패가 확인되는 즉시 INTENTS.md를 `blocked` 또는 `channel_blocked`로 갱신하고, heartbeat가 없어도 다음 루프가 바로 행동할 수 있게 last_checked_at과 next_check_at을 함께 남겨야 한다.

- 대상 intent: 2026-04-24 idle 이후 새 Inbox 1건 장기 미pickup
- 평가: 모든 Intent 완료 뒤 idle로 끝난 운영일수록 다음 heartbeat 예정 시각이나 pickup freshness 기준이 없으면, 새 Inbox가 생긴 뒤 며칠씩 아무 루프에도 들어가지 않는 공백이 다시 생긴다.
- 근거: 최신 heartbeat report는 2026-04-24T00:00에 `Inbox 비어있음 / Active 비어있음`으로 종료했고, 현재 INTENTS.md Inbox에는 모바일 네비게이션 개선 1건이 있으나 2026-05-03 06:57 UTC 기준 Active 전환 흔적이 없다.
- 다음에 유지할 것: Active가 없을 때 조용히 종료하는 간결한 보고 형식 자체는 적절하다.
- 다음에 바꿀 것: idle 종료에도 `next_heartbeat_at` 또는 최대 pickup 지연 SLA를 남겨, 완료 직후 들어온 신규 Inbox가 다음 정기 루프 부재 때문에 방치되지 않게 해야 한다.

- 대상 intent: 2026-04-19 00:57 기준 wiki-02 장기 승인 대기
- 평가: 승인 대기 intent를 report에만 누적 기록하고 registry 상태를 갱신하지 않으면, 시간이 지날수록 운영이 쉬워지기는커녕 다음 루프가 같은 사실을 다시 판독하는 비용만 커진다.
- 근거: 최신 heartbeat는 2026-04-18 12:00, 최신 wiki-02 report는 13:00인데 여기엔 승인 미수신과 Telegram 차단이 이미 적혀 있다. 하지만 2026-04-19 00:57 현재 INTENTS.md의 wiki-02는 여전히 `in_progress`이고 blocked reason, channel 상태, next check가 없어 단일 진실 원천 역할을 못 한다.

- 대상 intent: 2026-04-24 이후 Inbox의 `agent-wiki` 모바일 네비게이션 개선 요청
- 평가: Active가 비어 idle 상태가 된 뒤에도 Heartbeat가 새 Inbox 유입을 다시 pickup하는 주기 신뢰성을 유지하지 못하면, 시스템은 "모든 Intent 완료" 직후 새 일을 장기간 방치하는 맹점을 가진다.
- 근거: 최신 heartbeat report는 2026-04-24T00:00에 `Inbox 비어있음 / Active 비어있음`으로 종료했지만, 같은 날 12:54 UTC에 INTENTS.md에 새 Inbox 항목이 추가됐고 2026-05-03 00:57 UTC 현재까지 이를 pickup한 더 최신 heartbeat 흔적이 없다.
- 다음에 유지할 것: Active가 비었을 때 idle로 짧게 종료하는 보고 형식 자체는 간결하다.
- 다음에 바꿀 것: "현재 idle"과 "이후 새 Inbox 유입 감시"를 분리해, idle 이후에도 Heartbeat 스케줄 누락·정지 여부를 감지하는 감시선(최대 무응답 시간 또는 마지막 heartbeat age 기준 경보)을 둬야 한다.
- 다음에 유지할 것: 구현 준비 완료와 사용자 승인 필요를 별도 report로 분리해 실제 남은 일이 좁혀져 있는 점.
- 다음에 바꿀 것: 장기 대기 intent는 매 heartbeat 보고를 늘리기보다 INTENTS.md를 우선 갱신하도록 강제해 `status`, `blocked_reason`, `channel_state`, `next_check_at`만 봐도 다음 pickup 판단이 끝나게 해야 한다.

- 대상 intent: 2026-04-19 01:57 기준 wiki-02 환경 제약 blocked 유지
- 평가: registry를 `blocked`와 구체적 `blocked_reason`으로 바로잡은 점은 개선이지만, 이후 heartbeat가 매시간 같은 blocked 보고만 누적하면 상태 표현은 좋아져도 운영 결정 비용은 여전히 줄지 않는다.
- 근거: 현재 INTENTS.md의 wiki-02는 승인 대기 대신 `agent-wiki 접근 불가`를 blocked_reason으로 명확히 적고 있다. 반면 2026-04-18 23:00, 2026-04-19 00:00 report는 16, 17번째 blocked를 반복하며 같은 A/B/C 결정을 다시 요구하지만 registry에는 `next_check_at`이나 `owner_action/user_action`이 없어 반복 보고를 멈출 기준이 없다.
- 다음에 유지할 것: 승인 미수신이 아니라 환경 제약이라는 실제 차단 원인을 registry에 반영한 수정.
- 다음에 바꿀 것: 장기 blocked intent는 반복 heartbeat 생성보다 registry에 재확인 시각과 필요한 결정 주체를 남기고, 그 시각 전에는 중복 report를 생략하거나 변화가 있을 때만 쓰게 해야 한다.

- 대상 intent: 2026-04-19 02:45 wiki-02 완료 처리
- 평가: 실행 자체보다 더 중요한 운영 품질은 막히던 intent를 대안 경로로 즉시 끝낸 뒤 registry, archive, 완료 report를 한 번에 정합시킨 점이다.
- 근거: wiki-02는 gh CLI와 `gh api` 경로를 쓰자 5분 안에 완료됐고, 현재 INTENTS.md Active는 비어 있으며 archive/wiki-02.md와 02:45 완료 report가 같은 식별자와 완료 시점을 공유한다.
- 다음에 유지할 것: 완료 시 registry 정리, archive 이관, 배포 검증 결과를 같은 턴에 닫아 다음 heartbeat가 과거 상태를 재해석하지 않게 한 흐름.
- 다음에 바꿀 것: 수동 세션에서만 가능했던 대안 경로 탐색과 완료 정합화 규칙을 heartbeat 기본 프로토콜로 끌어올려, 장기 blocked intent도 사람 개입 전 자동으로 같은 수준까지 수습되게 해야 한다.

- 대상 intent: 2026-04-19 wiki-02 초기 완료 후 콘텐츠 탐색 실패 재수정
- 평가: registry와 archive를 빨리 닫은 정합성은 좋았지만, 실제 노트 탐색 검증 없이 완료 처리해 곧바로 후속 수정이 열린 점은 완료 기준이 아직 사용자 관점에 충분히 맞지 않았다는 신호다.
- 근거: 02:45 완료 report는 루트 진입과 title 확인만으로 complete 처리했지만, 03:07 후속 report에서 Pages source가 `/docs`만 서빙해 `diary/`, `sources/`, `mapped/` 접근이 모두 깨져 있었음이 확인됐다.
- 다음에 유지할 것: 문제 제기 직후 원인 진단, Pages source 전환, `.nojekyll` 추가, sidebar 확장까지 한 번에 수습한 실행력.
- 다음에 바꿀 것: 배포형 intent의 완료 검증은 진입 URL 200이 아니라 실제 핵심 콘텐츠 경로 2~3개까지 포함한 사용자 시나리오 기준으로 통과시켜야 한다.

- 대상 intent: 2026-04-19 wiki-02 완료 직후 동일 deliverable 재오픈
- 평가: 완료 직후 발견된 결함을 새 번호로 분리하지 않고 같은 intent 식별자 안에서 수정 이력까지 합쳐 닫은 점은 후속 pickup 비용을 낮췄다.
- 근거: 02:45 완료 후 03:07 재수정이 발생했지만 현재 archive/wiki-02.md는 initial 완료와 content navigation fix를 같은 wiki-02 이력으로 정리하고, INTENTS.md도 활성 항목 없이 정합하게 비워져 있다.
- 다음에 유지할 것: 같은 deliverable의 즉시 후속 버그는 신규 intent를 만들지 말고 기존 intent를 reopen 또는 동일 식별자 연장선에서 마감하는 방식.
- 다음에 바꿀 것: 완료 후 짧은 유예 구간의 수정은 report만 추가하지 말고 registry/archive에 `reopened_at` 또는 `post-complete fix` 같은 상태 전이를 명시해, 한 intent 안에서 다시 열렸다 닫혔다는 사실이 더 선명하게 남게 해야 한다.

- 대상 intent: 2026-04-19 wiki-02의 02:45 초기 완료와 03:07 재수정 구간
- 평가: 실행력은 매우 좋았지만 완료 선언이 사용자 시나리오 검증보다 빨라서, 결과적으로 좋은 수습이 초기 완료 품질의 빈틈을 가렸다.
- 근거: 02:45 report는 루트 진입과 title 확인만으로 complete 처리했지만 22분 뒤 03:07 report에서 `diary/`, `sources/`, `mapped/`, `_sidebar.md` 접근 실패를 한 번에 수정했다. archive에는 최종 상태가 잘 정리됐지만 초기 완료가 왜 premature였는지는 registry 관점에서 드러나지 않는다.
- 다음에 유지할 것: 차단 해소 뒤 gh CLI, Pages API, 재빌드까지 짧은 시간에 연속 실행한 수습 속도.
- 다음에 바꿀 것: 배포형 intent는 완료 직전 `진입 URL + 핵심 콘텐츠 경로 2~3개 + 런타임 필수 파일(_sidebar.md, API 응답 등)`을 체크리스트로 통과해야만 complete로 닫고, 실패 시엔 완료 대신 같은 intent의 verification_failed 또는 post-deploy-fix 단계로 남겨야 한다.

- 대상 intent: 2026-04-19 wiki-02의 초기 archive 후 즉시 재수정
- 평가: archive를 너무 빨리 확정하면 후속 수정이 같은 intent 안에 잘 정리돼도, 다음 heartbeat 기준의 현재 상태는 한동안 registry 밖에서 떠다니게 된다.
- 근거: 02:45에 INTENTS.md Active에서 wiki-02를 제거하고 archive로 이관했지만, 03:07에 같은 deliverable의 핵심 결함 수정이 바로 이어졌다. 최종 archive에는 합쳐졌지만 그 사이 상태 전이는 Active registry에서 보이지 않았다.
- 다음에 유지할 것: 같은 deliverable의 후속 버그를 새 번호로 분리하지 않고 동일 식별자로 정리한 점.
- 다음에 바꿀 것: 사용자 확인 전에는 archive 확정보다 `completed_pending_verification` 같은 짧은 유예 상태를 두고, 그 창구 안의 수정은 Active registry에서 이어서 추적하게 해야 한다.

- 대상 intent: 2026-04-19 Inbox의 `agent-wiki` 모바일 네비게이션 개선
- 평가: 같은 프로젝트의 후속 개선 요청이 Inbox에 이미 등록됐는데도 최신 heartbeat 기준선이 여전히 2026-04-18의 `Inbox 비어 있음`에 머물러 있으면, 완료 이후 새 루프 진입 신뢰성이 다시 떨어진다.
- 근거: 현재 INTENTS.md Inbox에는 wiki-02와 연속선상인 모바일 네비게이션 개선 1건이 존재하지만, heartbeat report 최신본은 2026-04-18T12:00이며 그 이후 pickup/구조화 흔적이 없다.
- 다음에 유지할 것: wiki-02 자체는 archive와 결과 정합성을 잘 맞춰 닫은 점.
- 다음에 바꿀 것: 특정 intent를 막 끝낸 직후에는 같은 프로젝트 키워드의 신규 Inbox를 우선 재스캔해 연속 작업을 놓치지 않게 하고, heartbeat 공백이 하루 이상 생기면 `마지막 pickup 시각` 자체를 품질 경고로 취급해야 한다.

- 대상 intent: 2026-04-19 wiki-02 완료 직후 Inbox의 `agent-wiki` 모바일 네비게이션 개선
- 평가: 같은 프로젝트 deliverable을 막 닫은 직후 새 개선 요청이 Inbox에 들어왔을 때 pickup이 수 시간 멈추면, 이전 intent를 잘 끝낸 실행력보다 후속 연속 작업을 자연스럽게 이어받는 운영 품질이 더 크게 훼손된다.
- 근거: wiki-02는 03:07에 최종 수정까지 archive 정합성을 맞춰 닫혔지만, 11:57 현재 INTENTS.md Inbox의 모바일 네비게이션 개선은 아직 구조화되지 않았고 heartbeat 측 pickup 흔적도 없다.
- 다음에 유지할 것: 동일 deliverable의 완료 이력과 archive 정리는 깔끔하게 유지된 점.
- 다음에 바꿀 것: 어떤 intent를 completed/archived로 닫을 때 같은 프로젝트 관련 신규 Inbox가 있으면 같은 턴 또는 다음 heartbeat 첫 단계에서 강제 pickup하게 해, 완료 직후의 운영 공백이 새 요청 누락으로 이어지지 않게 해야 한다.

- 대상 intent: 2026-04-19 wiki-03 승인 수신 후 실행 재개 지연
- 평가: 승인 게이트가 해소된 순간이 blocked 종료 시점인데, GATES.md만 resolved로 바뀌고 Intent와 보고가 몇십 분째 그대로면 승인 흐름의 마지막 구간이 자동화되지 않은 셈이다.
- 근거: wiki-03은 06:00 report까지 `blocked (L2 승인 대기)`였고 현재 GATES.md에는 12:36 승인 완료가 기록돼 있지만, 12:57 현재 INTENTS.md는 여전히 실행 전 상태로 남아 있고 승인 후 실행/재구조화 흔적이 없다.
- 다음에 유지할 것: 승인 전 드래프트를 먼저 완성해 두고, 승인만 오면 바로 push 가능한 준비 상태를 만든 점.
- 다음에 바꿀 것: GATES.md가 resolved 되면 다음 heartbeat를 기다리지 말고 같은 루프에서 해당 intent를 즉시 resume 후보로 끌어올리거나, 최소한 INTENTS.md에 `approved_waiting_execution`과 `approved_at`을 남겨 승인 이후 정지와 승인 미수신을 구분해야 한다.

- 대상 intent: 2026-04-19 wiki-03 승인 후 2시간+ 무재개 상태
- 평가: 승인 수신 뒤에도 최신 heartbeat와 실행 report가 생기지 않으면, 게이트 시스템은 작동해도 실제 resume 루프가 끊겨 승인 흐름이 운영 성과로 이어지지 않는다.
- 근거: GATES.md의 wiki-03는 12:36 approved인데 14:57 현재 최신 wiki-03 report는 여전히 06:00 승인 대기본이고, heartbeat 최신본도 2026-04-18T12:00에 멈춰 있어 승인 이후 실행 흔적이 전혀 없다.
- 다음에 유지할 것: 승인 전 배포 드래프트를 완성해 둬 재개 즉시 실행 가능한 준비 상태를 만든 점.
- 다음에 바꿀 것: gate resolved 이벤트를 heartbeat 주기와 분리된 즉시 재개 트리거로 취급하고, 최소한 INTENTS.md에 `approved_at`, `resumed_at`, `last_progress_at`을 남겨 승인 후 정체가 문서만으로 바로 보이게 해야 한다.

- 대상 intent: 2026-04-19 15:57 기준 wiki-03 승인 완료 후 미실행 지속
- 평가: 승인 게이트를 해제해도 Active intent가 여전히 `in_progress` 한 줄로만 남아 있으면, 다음 루프는 실행할 준비가 된 일과 이미 돌고 있는 일을 구분하지 못해 resume 우선순위를 놓치기 쉽다.
- 근거: GATES.md에는 wiki-03가 12:36 approved로 닫혀 있지만 INTENTS.md Active의 wiki-03는 `approved_at`, `blocked 해제 시각`, `last_progress_at` 없이 그대로 `in_progress`이며, 최신 report도 06:00 승인 대기본에서 멈춰 있다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 계획을 미리 완성해 둔 구조.
- 다음에 바꿀 것: gate 해제 시 INTENTS.md를 즉시 `ready_to_execute` 또는 `approved_waiting_execution`으로 갱신하고, heartbeat는 그 상태를 최우선 pickup 대상으로 강제해 승인 직후 정체를 문서상으로 숨기지 말아야 한다.

- 대상 intent: 2026-04-19 17:57 기준 wiki-03 승인 후 장시간 무진행
- 평가: 승인 수신 뒤 실제 실행이 수시간 비면 문제는 승인 대기 자체가 아니라 승인 이벤트가 실행 재개로 연결되지 않는 운영 단절이다.
- 근거: GATES.md의 wiki-03는 12:36 approved인데 17:57 현재도 INTENTS.md Active는 단순 `in_progress`이고, 최신 wiki-03 report는 여전히 06:00 승인 대기본이라 승인 후 실행·보고 흔적이 없다.
- 다음에 유지할 것: 승인 전 드래프트를 완성해 실행 준비물을 미리 만들어 둔 점.
- 다음에 바꿀 것: gate resolved를 heartbeat 주기 의존 이벤트로 두지 말고 즉시 resume 트리거로 연결하며, 최소한 registry에 `approved_at`, `resume_by`, `last_progress_at`을 남겨 승인 후 정체가 자동으로 드러나게 해야 한다.

- 대상 intent: 2026-04-19 20:57 기준 wiki-03 승인 후 야간까지 미재개
- 평가: 승인 자체는 제때 기록됐지만 그 이후 Active intent와 실행 report가 갱신되지 않으면, 좋은 승인 흐름도 실제 처리량으로 전환되지 못한 채 '승인 완료처럼 보이지만 실행은 멈춘' 상태를 만든다.

- 대상 intent: 2026-04-24 이후 Inbox의 `agent-wiki` 후속 개선 1건
- 평가: 최신 heartbeat가 `Inbox 비어있음`으로 종료한 뒤 실제 Inbox에 동일 프로젝트 후속 intent가 남아 있으면, 완료 직후 연속 작업을 이어받는 pickup 루프가 다시 끊긴다.
- 근거: 2026-04-24T00:00 heartbeat report는 `Inbox: 비어있음`으로 idle 종료했지만 현재 INTENTS.md Inbox에는 `[개선] agent-wiki 모바일 네비게이션 ... 전체 문서 구조 기반으로 재구성` 1건이 남아 있다.
- 다음에 유지할 것: Active/Gates가 없을 때 불필요한 알림 없이 종료하는 간결한 heartbeat 형식.
- 다음에 바꿀 것: heartbeat 종료 직전 INTENTS.md Inbox를 재검증하고, 같은 프로젝트의 신규 후속 intent가 있으면 idle 종료 대신 즉시 pickup하거나 최소한 `completed project follow-up detected` 경고를 남겨 연속 작업 누락을 막아야 한다.
- 근거: GATES.md에는 wiki-03 승인 완료가 12:36으로 남아 있는데 20:57 현재 INTENTS.md Active의 wiki-03에는 `approved_at`이나 `last_progress_at`이 없고, 최신 실행 흔적도 06:00 승인 대기 report에서 멈춰 있다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 계획을 먼저 준비해 둔 구조.
- 다음에 바꿀 것: 승인 완료가 기록되면 같은 턴에 INTENTS.md를 `approved_waiting_execution` 또는 `ready_to_execute`로 바꾸고, heartbeat가 비더라도 다음 루프가 즉시 resume 우선순위를 잡게 하는 상태 전이를 표준화해야 한다.

- 대상 intent: 2026-04-19 22:57 기준 wiki-03 승인 후 당일 미실행 지속
- 평가: 승인 게이트를 잘 닫아도 실행 재개가 같은 날 안에 이어지지 않으면, Infinity의 병목은 승인 획득이 아니라 승인 이벤트를 실제 작업으로 연결하는 resume 자동화 부재다.
- 근거: GATES.md의 wiki-03는 12:36 approved인데 22:57 현재 INTENTS.md Active는 여전히 `in_progress`만 표시하고 있고, latest report도 06:00 승인 대기본에서 멈춰 있어 승인 후 10시간 넘게 pickup·실행·보고가 모두 비어 있다.
- 다음에 유지할 것: 승인 전에 배포 드래프트를 완성해 실행 준비물을 앞당겨 둔 운영 방식.
- 다음에 바꿀 것: gate resolved 시점을 별도 이벤트로 취급해 INTENTS.md에 `approved_at`, `resume_deadline`, `last_progress_at`를 즉시 기록하고, 그 시한 내 실행 흔적이 없으면 heartbeat가 일반 순회보다 resume escalation을 우선하도록 바꿔야 한다.

- 대상 intent: 2026-04-19 23:29 승인 완료 직후 wiki-03 야간 Heartbeat
- 평가: 승인 상태의 단일 진실 원천이 GATES.md라면, Heartbeat가 그 파일을 읽고도 직전 승인 반영에 실패해 `blocked 지속` 리포트를 남기는 순간 승인 흐름 전체 신뢰도가 무너진다.
- 근거: GATES.md에는 `[wiki-03] GPG 서명 없이 agent-wiki 커밋 허용`이 23:29 resolved로 기록돼 있는데, 23:00 wiki-03 report는 같은 Gate를 10h+ 미승인으로 적어 두었고 현재 INTENTS.md도 여전히 `in_progress`라 승인 후 즉시 resume 가능한 상태와 장기 blocked 상태가 문서 간에 갈라져 있다.
- 다음에 유지할 것: 승인 전 드래프트를 보존하고 실행 명령까지 구체화해 둔 준비 수준.
- 다음에 바꿀 것: Gate 판단은 보고 시점의 스냅샷이 아니라 report 작성 직전 GATES.md 재검증으로 확정하고, 승인 시각이 report 시각보다 이르면 blocked 보고 대신 `approved_waiting_execution` 또는 즉시 실행으로 전환하게 해야 한다.

- 대상 intent: 2026-04-20 00:57 기준 wiki-03 승인 후 무재개 지속
- 평가: 승인 기록이 남았는데도 다음 실행 흔적이 한 번도 생기지 않으면, 승인 흐름 품질의 핵심 병목은 `승인 받기`가 아니라 `승인 이벤트가 작업 재개를 깨우지 못하는 것`이다.
- 근거: GATES.md에는 wiki-03의 두 번째 Gate가 2026-04-19 23:29 approved로 닫혀 있고 INTENTS.md에는 여전히 wiki-03만 Active로 남아 있지만, 2026-04-20 00:57 시점까지 후속 report나 상태 전이(`approved_waiting_execution`, `completed`)가 없다.
- 다음에 유지할 것: 드래프트와 실행 절차를 미리 준비해 승인만 오면 바로 끝낼 수 있게 만든 구조.
- 다음에 바꿀 것: GATES.md resolved 항목은 다음 정시 Heartbeat를 기다리지 말고 즉시 wake 또는 resume 큐로 연결하고, 최소한 INTENTS.md에 `approved_at`과 `resume_deadline`을 자동 기록해 승인 후 정지가 문서에서 바로 보이게 해야 한다.

- 대상 intent: 2026-04-20 02:57 기준 wiki-03 승인 후 새벽까지 미재개
- 평가: 승인 자체는 기록됐지만 Active registry와 최신 report가 승인 전 상태에 머물면, 다음 루프는 실행보다 먼저 "지금 blocked인가, 승인됐나"를 다시 판독하느라 시간을 잃는다.
- 근거: GATES.md에는 wiki-03 Gate 2가 2026-04-19 23:29 approved로 닫혀 있지만, 2026-04-20 02:57 현재 INTENTS.md의 wiki-03는 여전히 `in_progress`이고 최신 per-intent report는 23:00 blocked 본이다.
- 다음에 유지할 것: 승인 전 드래프트 보존과 실행 커맨드 준비를 끝내 둔 점.
- 다음에 바꿀 것: Gate resolved 직후 INTENTS.md를 `approved_waiting_execution` 같은 명시 상태로 먼저 갱신하고, 그 상태가 일정 시간 넘게 지속되면 heartbeat가 일반 순회 대신 resume 실행이나 escalation을 최우선으로 잡게 해야 한다.

- 대상 intent: 2026-04-20 04:57 기준 wiki-03 승인 후 최신 보고 정체
- 평가: 승인 후 실행이 늦어지는 것 자체보다 더 큰 문제는 "가장 최근 문서"가 여전히 승인 전 blocked 서술이라 다음 pickup이 현재 상태 대신 오래된 판단을 기본값으로 삼게 되는 점이다.
- 근거: GATES.md는 2026-04-19 23:29에 wiki-03 Gate 2를 approved로 닫았지만, 2026-04-20 04:57 현재 최신 wiki-03 report는 여전히 23:00 blocked 본이고 heartbeat 최신본도 16:00 blocked 요약이라 승인 이후 상태를 반영한 최신 스냅샷이 없다.
- 다음에 유지할 것: blocked 중에도 드래프트와 즉시 실행 절차를 문서화해 둔 준비 수준.
- 다음에 바꿀 것: Gate가 해소되면 실행 성공 여부와 무관하게 1회성 "post-approval status refresh"를 강제해 INTENTS, per-intent report, heartbeat 중 최소 하나는 항상 최신 승인 이후 상태를 대표하게 해야 한다.

- 대상 intent: 2026-04-20 05:57 기준 wiki-03 승인 후 문서 정합성 붕괴
- 평가: 승인 이벤트를 GATES.md만 알고 INTENTS·heartbeat·per-intent report가 모두 승인 전 상태에 머물면, 다음 루프는 실행보다 먼저 "지금 막혔는지 이미 풀렸는지"를 재판독하느라 시간을 잃는다.
- 근거: GATES.md에는 wiki-03 Gate 2가 2026-04-19 23:29 approved로 닫혀 있지만, 2026-04-20 05:57 현재 INTENTS.md의 wiki-03는 여전히 `in_progress`이고 최신 heartbeat는 16:00 blocked, 최신 wiki-03 report는 23:00 blocked다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 명령을 미리 준비해 둔 점.
- 다음에 바꿀 것: Gate resolved 순간 INTENTS를 `approved_waiting_execution` 같은 별도 상태로 즉시 갱신하고, 그 상태 갱신 없이는 blocked heartbeat/report를 더 쓰지 못하게 막아야 한다.

- 대상 intent: 2026-04-19 23:00 wiki-03 Heartbeat의 detached HEAD 복구
- 평가: 실행이 막혀 있을 때도 Heartbeat가 기록을 detached HEAD에 쌓으면 승인 재개 이전의 운영 흔적 자체가 main 기준선에서 사라질 수 있어, 상태 판단보다 먼저 브랜치 정합성 보장이 선행돼야 한다.
- 근거: wiki-03의 23:00 report는 Gate 2 대기 자체보다 `detached HEAD`에서 생성된 41개 커밋을 main으로 fast-forward 복구한 일을 핵심 이슈로 적고 있다. 즉, 문서와 리포트가 존재해도 브랜치에 안 붙어 있으면 다음 pickup은 최신 운영 상태를 못 본다.
- 다음에 유지할 것: 복구 후 report, draft, archive, registry를 한 번에 main으로 되돌려 정합성을 회복한 대응.
- 다음에 바꿀 것: Heartbeat 시작과 종료에 현재 브랜치, upstream, HEAD 부착 여부를 필수 점검하고, detached 상태면 새 report 작성 전에 즉시 복구하거나 쓰기를 중단하게 해야 한다.

- 대상 intent: 2026-04-19 wiki-03 Gate 2 승인 후 2026-04-21 새벽까지 미재개 상태
- 평가: 승인 이벤트를 받았는데도 이틀 가까이 실행 재개가 없으면, Infinity의 병목은 승인 획득이 아니라 승인 이후 intent를 즉시 resume 큐로 승격하는 연결이 비어 있는 데 있다.
- 근거: GATES.md에는 wiki-03 Gate 2가 2026-04-19 23:29 approved로 닫혀 있지만, 현재 INTENTS.md의 wiki-03는 여전히 `in_progress`이고 최신 per-intent report도 23:00 blocked 본에서 멈춰 있어 승인 이후 상태 갱신과 실행 흔적이 전혀 없다.
- 다음에 유지할 것: 승인 전 드래프트를 완성해 즉시 실행 가능한 준비 상태를 만들어 둔 점.
- 다음에 바꿀 것: GATES.md resolved를 단순 기록으로 끝내지 말고 같은 턴에 INTENTS.md를 `approved_waiting_execution` 또는 `ready_to_execute`로 바꾸고, 일정 시간 내 실행이 없으면 heartbeat가 일반 순회보다 resume escalation을 먼저 하게 해야 한다.

- 대상 intent: 2026-04-19 23:29 승인 완료 후 wiki-03 최신 상태 반영 실패
- 평가: 승인 직후 최신 리포트가 여전히 `blocked`를 남기면, 실제 미실행보다 더 먼저 현재 상태 관측이 틀어져 다음 루프가 오래된 판단을 재사용하게 된다.
- 근거: GATES.md에는 wiki-03 Gate 2가 2026-04-19 23:29 approved로 기록돼 있는데, 최신 wiki-03 report는 같은 23:00 시각의 `blocked (Gate 2 승인 대기 지속)`이고 INTENTS.md도 `in_progress`만 남아 있어 승인 완료 사실을 대표하는 최신 문서가 없다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 구체적으로 준비해 둔 점.
- 다음에 바꿀 것: Gate가 resolve되면 실행 성공 여부와 별개로 즉시 `post-approval status refresh`를 강제해 INTENTS.md나 per-intent report 중 최소 하나는 항상 승인 이후 상태를 최신 기준선으로 남기게 해야 한다.

- 대상 intent: 2026-04-21 04:57 기준 wiki-03 승인 후 장기 미재개
- 평가: Gate 승인 후 이틀 가까이 실행이 재개되지 않았는데도 Active intent가 여전히 단순 `in_progress`이면, 승인 흐름의 품질 문제를 넘어 resume 큐 자체가 없는 운영 결함으로 봐야 한다.
- 근거: GATES.md에는 wiki-03의 두 L2 Gate가 모두 approved로 닫혀 있고 마지막 승인 시각은 2026-04-19 23:29인데, 현재 INTENTS.md Active의 wiki-03는 `approved_at`, `last_progress_at`, `resume_deadline` 없이 그대로 `in_progress`이며 최신 per-intent report도 2026-04-19 23:00 blocked 본에서 멈춰 있다.
- 다음에 유지할 것: 승인 전 드래프트를 완성해 즉시 실행 가능한 준비물을 만들어 둔 점.
- 다음에 바꿀 것: Gate resolve를 단순 기록이 아니라 `resume_queue` 등록 이벤트로 취급해 같은 턴에 INTENTS.md를 `approved_waiting_execution`으로 바꾸고, 일정 시간 내 실행 흔적이 없으면 일반 heartbeat 순회보다 resume escalation을 우선하게 해야 한다.

- 대상 intent: 2026-04-21 05:57 기준 wiki-03 Active 상태와 Heartbeat 최신성
- 평가: Active intent가 남아 있는데 Heartbeat 최신본이 하루 이상 비어 있으면, 문제는 개별 blocked 판단이 아니라 "살아 있는 intent를 감시하는 루프" 자체가 멈췄다는 점이다.
- 근거: 현재 INTENTS.md Active에는 wiki-03가 남아 있지만 heartbeat report 최신본은 2026-04-19 16:00이고, 그 이후 Gate 2 승인(2026-04-19 23:29)과 wiki-03 per-intent report 정체가 모두 Heartbeat 기준선에 반영되지 않았다.
- 다음에 유지할 것: intent별 report와 heartbeat report를 분리해 남기는 관측 구조 자체.
- 다음에 바꿀 것: Active가 1건 이상이면 `last_heartbeat_at` 신선도 자체를 운영 규칙으로 관리해 일정 시간 초과 시 idle/blocked 판단보다 먼저 Heartbeat 공백 경고와 강제 상태 새로고침을 실행해야 한다.

- 대상 intent: 2026-04-21 09:57 기준 wiki-03 승인 후 장기 미재개
- 평가: 승인된 Gate가 모두 닫힌 뒤에도 Active intent가 `in_progress`로만 남아 있으면, 승인 흐름은 끝났는데 resume 큐가 없어 실행 우선순위가 문서상에서 사라진다.
- 근거: GATES.md에는 wiki-03의 두 승인 항목이 모두 resolved이고 마지막 승인 시각은 2026-04-19 23:29인데, INTENTS.md의 wiki-03는 여전히 `in_progress`이며 최신 per-intent report도 같은 날 23:00 blocked 문맥에 머물러 있다.
- 다음에 유지할 것: 승인 전 드래프트를 미리 완성해 재개 즉시 실행 가능 상태를 만든 점.
- 다음에 바꿀 것: Gate resolved 즉시 INTENTS.md를 `approved_waiting_execution` 같은 상태로 승격하고, 그 상태가 일정 시간 남아 있으면 heartbeat가 일반 순회보다 resume 실행 또는 에스컬레이션을 먼저 하게 해야 한다.

- 대상 intent: 2026-04-21 11:57 기준 wiki-03 승인 후 미재개와 Heartbeat 우선순위 규칙
- 평가: 현재 프로토콜은 `blocked 중 승인된 항목`만 최우선으로 올리는데, 실제 registry가 승인 후 intent를 계속 `in_progress`로 두면 승인 이벤트가 있어도 우선순위 규칙이 작동할 자리가 사라진다.
- 근거: workflows/heartbeat.md는 우선순위 1순위를 `blocked 중 승인된 항목`으로 정의하지만, GATES.md의 wiki-03는 2026-04-19 23:29에 이미 resolved이고 INTENTS.md는 아직 `in_progress`, 최신 heartbeat 흔적도 2026-04-19 16:00 기준선에 머물러 있어 승인 후 재개 대상을 규칙상으로도 자동 식별하지 못한다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 점.
- 다음에 바꿀 것: Gate resolved 시 intent를 반드시 `blocked` 밖의 별도 재개 상태로 전이시키고, Heartbeat 우선순위 규칙도 `approved_waiting_execution`을 1순위로 읽게 바꿔 승인 이벤트가 문서 구조만으로 즉시 pickup되게 해야 한다.

- 대상 intent: 2026-04-21 14:57 기준 wiki-03 단독 Active 장기 정체
- 평가: Active가 1건뿐인데도 최신 heartbeat가 이틀 가까이 비고 per-intent 최신 문서가 승인 전 blocked 상태에 머무르면, 개별 intent 실패가 아니라 "살아 있는 일을 최신 상태로 다시 써 주는 감시 루프" 자체가 고장난 것이다.
- 근거: 현재 INTENTS.md Active에는 wiki-03만 남아 있지만 heartbeat 최신본은 2026-04-19 16:00, per-intent 최신본은 2026-04-19 23:00 blocked, 반면 GATES.md는 2026-04-19 23:29에 승인 완료로 닫혀 있다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 점.
- 다음에 바꿀 것: Active가 비지 않았는데 `last_heartbeat_at`이나 `last_status_refresh_at`이 임계시간을 넘으면 일반 상태 점검보다 먼저 최신 상태 재기록을 강제하고, 최신 문서가 승인 전 상태면 새 heartbeat 없이도 stale 경고를 띄우게 해야 한다.

- 대상 intent: 2026-04-21 15:57 기준 wiki-03 승인 후 장기 미실행
- 평가: 승인 자체는 모두 정리됐는데 Heartbeat와 intent 문서가 계속 승인 전/실행 중간 상태에 머물러 있으면, 실제 병목은 실행 능력이 아니라 `승인됨 → 즉시 재개 후보`로 상태를 승격시키는 연결 부재다.
- 근거: GATES.md에는 wiki-03의 두 Gate가 모두 resolved이고 마지막 승인은 2026-04-19 23:29인데, INTENTS.md는 여전히 `in_progress`, heartbeat 최신본은 2026-04-19 16:00 blocked, per-intent 최신본은 2026-04-19 23:00 blocked로 남아 있다.
- 다음에 유지할 것: 승인 전에 드래프트와 실행 절차를 준비해 둔 구조.
- 다음에 바꿀 것: Gate가 resolved 되는 즉시 INTENTS.md를 `approved_waiting_execution` 같은 별도 상태로 전이하고, 그 상태가 일정 시간 지속되면 일반 heartbeat 순회보다 resume 실행 또는 에스컬레이션을 먼저 트리거해야 한다.

- 대상 intent: 2026-04-19 23:29 승인 직후부터 2026-04-21 19:57까지의 wiki-03 상태 반영
- 평가: 브랜치 복구는 잘했어도 복구 직후 최신 상태 새로고침이 없으면, main에는 "복구된 과거 blocked 문서"만 남아 승인 완료 이후 현실보다 더 낡은 기준선이 고착된다.
- 근거: 2026-04-19 23:00 wiki-03 report는 detached HEAD 복구와 함께 main에 반영됐지만 내용은 여전히 Gate 2 미승인 기준이고, 실제 GATES.md는 같은 날 23:29 resolved인데 2026-04-21 19:57 현재까지 이를 덮는 post-approval report나 heartbeat가 없다.
- 다음에 유지할 것: detached HEAD를 발견했을 때 report, draft, registry를 main으로 복구한 대응 속도.
- 다음에 바꿀 것: 브랜치 복구나 대량 fast-forward 직후에는 실행 여부와 무관하게 `state refresh`를 한 번 강제해, main에 올리는 최신 문서가 과거 blocked 스냅샷으로 끝나지 않게 해야 한다.

- 대상 intent: 2026-04-21 21:57 기준 wiki-03 승인 후 재개 우선순위 규칙
- 평가: 현재 Heartbeat 프로토콜은 승인된 일을 최우선으로 재개하겠다고 쓰면서도, 어떤 상태명을 그 대상으로 삼는지는 서로 충돌해 승인 이벤트가 문서 구조 안에서 자동 pickup되지 않는다.
- 근거: workflows/heartbeat.md는 우선순위 1순위를 `blocked 중 승인된 항목`으로 정의하지만, 같은 문서의 생명주기 규칙은 승인 후 상태를 `blocked → in_progress`로 옮기게 적고 있다. 실제 wiki-03도 Gate는 모두 resolved인데 INTENTS.md에는 `in_progress`로만 남아 있어 우선순위 규칙상 특별 취급 대상에서 사라졌다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 운영 방식.
- 다음에 바꿀 것: 승인 직후 상태명을 `approved_waiting_execution` 같은 단일 재개 상태로 고정하고, Heartbeat 우선순위도 그 상태를 1순위로 읽게 맞춰 프로토콜 내부 충돌부터 없애야 한다.

- 대상 intent: 2026-04-22 03:57 기준 wiki-03 승인 후 장기 정체
- 평가: 승인 기록은 남았는데 Heartbeat 최신성까지 함께 멈추면, 문제는 개별 blocked 판단이 아니라 "승인 해제된 Active intent를 다시 깨우는 루프"가 없다는 데 있다.
- 근거: GATES.md에는 wiki-03의 두 Gate가 모두 resolved이고 마지막 승인은 2026-04-19 23:29인데, 2026-04-22 03:57 현재 INTENTS.md Active의 wiki-03는 여전히 `in_progress`이고 heartbeat 최신본은 2026-04-19 16:00, per-intent 최신본은 2026-04-19 23:00 blocked 상태에 머물러 있다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 점.
- 다음에 바꿀 것: Gate resolved를 상태 기록으로 끝내지 말고 `approved_waiting_execution` 등록 + 즉시 status refresh + 재개 deadline 부여를 한 묶음으로 강제해, Active가 남아 있는데 최신 heartbeat가 멎는 일이 승인 후 장기 정체를 숨기지 못하게 해야 한다.

- 대상 intent: 2026-04-22 09:57 기준 wiki-03 단독 Active 장기 방치
- 평가: Active가 1건뿐인데도 Heartbeat가 이틀 넘게 멈춘 채 intent 상태가 `in_progress`로만 남아 있으면, 현재 프로토콜의 우선순위 규칙은 사실상 작동하지 않고 살아 있는 일을 영구히 보이지 않게 만들 수 있다.
- 근거: INTENTS.md에는 wiki-03만 Active로 남아 있고 Inbox는 비어 있지만, heartbeat 최신본은 2026-04-19 16:00이며 GATES.md의 wiki-03 관련 승인 2건은 모두 2026-04-19 안에 resolved다. 그런데 workflows/heartbeat.md의 1순위는 `blocked 중 승인된 항목`이라 현재처럼 승인 후 상태가 `in_progress`에 머무르면 재개 우선순위 큐에서 빠진다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 구조.
- 다음에 바꿀 것: Heartbeat 프로토콜에 `Active가 남아 있는데 last_heartbeat_at이 임계시간을 넘으면 무조건 상태 새로고침` 규칙을 추가하고, 승인 후 intent는 `in_progress` 대신 별도 resume 상태로 전이시켜 우선순위 규칙이 문서상으로도 계속 보이게 해야 한다.

- 대상 intent: 2026-04-22 11:57 기준 wiki-03 단독 Active와 빈 Gate 큐
- 평가: Inbox와 대기 중 Gate가 모두 비어 있어도 Active의 오래된 `in_progress` 1건이 남아 있으면 시스템은 겉보기에 한가해 보이면서 실제론 stranded intent를 숨긴다.
- 근거: 현재 INTENTS.md는 Inbox 비어 있음 + Active wiki-03 1건, GATES.md는 대기 중 비어 있음, 최신 wiki-03 report는 2026-04-19 23:00 blocked 본, heartbeat 기준선도 2026-04-19 16:00에 멈춰 있다.
- 다음에 유지할 것: Inbox/Active/GATES를 분리해 운영 표면을 나눈 기본 구조.
- 다음에 바꿀 것: `Inbox=0 && pending_gates=0`를 healthy 신호로 쓰지 말고, Active 각 항목의 `last_progress_at` 신선도를 함께 본 뒤 stale Active가 있으면 idle 대신 `resume_needed` 경고와 상태 새로고침을 강제해야 한다.

- 대상 intent: 2026-04-22 14:57 기준 wiki-03 승인 완료 후 stranded Active 지속
- 평가: 승인된 일을 최우선 재개하겠다는 규칙이 있어도 승인 후 상태명이 계속 `in_progress`면 우선순위 엔진이 그 일을 다시 집지 못해, 시스템은 실제론 멈췄는데도 정상 진행처럼 보인다.
- 근거: GATES.md의 wiki-03 관련 Gate 2건은 모두 resolved인데 INTENTS.md는 여전히 `in_progress`, 최신 wiki-03 report는 2026-04-19 23:00 blocked, heartbeat 최신 기준선도 2026-04-19 16:00에 멈춰 있다. 반면 workflows/heartbeat.md의 1순위는 `blocked 중 승인된 항목`이라 현재 표기 상태와 충돌한다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 구조.
- 다음에 바꿀 것: 승인 직후 상태를 `approved_waiting_execution` 같은 단일 이름으로 강제하고, Heartbeat 우선순위 규칙도 그 상태를 1순위로 읽게 맞춰 stale Active가 정상 진행으로 위장되지 않게 해야 한다.

- 대상 intent: 2026-04-22 16:57 기준 wiki-03 단독 Active 장기 방치
- 평가: Inbox와 pending Gate가 모두 비어 있더라도 stale Active 1건과 오래된 heartbeat만 남아 있으면 시스템은 `할 일 없음`처럼 보이면서 실제로는 재개가 필요한 intent를 숨긴다.
- 근거: 현재 INTENTS.md는 Inbox 비어 있음 + Active wiki-03 1건(`in_progress`), GATES.md 대기 중 비어 있음, 최신 heartbeat는 2026-04-19 16:00, 최신 wiki-03 report는 2026-04-19 23:00 blocked 본이다.
- 다음에 유지할 것: Inbox/Active/GATES를 분리해 운영 표면을 나눈 구조.
- 다음에 바꿀 것: 건강 상태 판단을 `Inbox=0 && pending_gates=0`가 아니라 `stale Active 존재 여부 + last_heartbeat_at 신선도`까지 포함해 계산하고, stale Active가 있으면 idle 대신 강제 status refresh 또는 resume escalation으로 전환해야 한다.

- 대상 intent: 2026-04-22 17:57 기준 wiki-03 승인 후 stranded Active
- 평가: 승인 항목을 GATES.md의 `처리 완료`로 옮기는 순간 Heartbeat 우선순위 1번(`blocked 중 승인된 항목`)이 더는 그 intent를 집지 못하므로, 승인 이벤트가 실제 재개 큐로 복제되지 않으면 승인 성공이 오히려 pickup 근거를 지워 버린다.
- 근거: wiki-03의 두 Gate는 모두 GATES.md `처리 완료`에 있고 대기 중은 비어 있는데, INTENTS.md는 아직 `in_progress`, 최신 heartbeat는 2026-04-19 16:00 blocked 기준, 최신 per-intent report도 2026-04-19 23:00 blocked 기준이라 승인 이후 상태를 자동 pickup할 문서 표지가 사라졌다.
- 다음에 유지할 것: 승인 기록을 별도 Gate ledger에 남겨 의사결정 이력 자체는 보존한 점.
- 다음에 바꿀 것: Gate를 `처리 완료`로 옮길 때 같은 턴에 intent도 `approved_waiting_execution` 같은 재개 전용 상태로 강제 전이하거나 resume 큐에 등록해, 승인 완료가 pickup 조건을 없애는 구조를 끊어야 한다.

- 대상 intent: 2026-04-22 19:57 기준 wiki-03 승인 완료 후 장기 미재개
- 평가: 승인 흐름 자체보다 더 큰 실패는 승인 직후 상태 새로고침이 없어, 최신 문서 묶음이 여전히 `blocked`·`in_progress`를 대표값으로 남긴 점이다.
- 근거: GATES.md에는 wiki-03 Gate 2가 2026-04-19 23:29 resolved로 닫혀 있지만 heartbeat 최신본은 2026-04-19 16:00, per-intent 최신본은 2026-04-19 23:00 blocked, INTENTS.md는 2026-04-22 19:57 현재도 `in_progress`라 승인 이후 기준선이 한 번도 생성되지 않았다.
- 다음에 유지할 것: 승인 전 드래프트와 실행 절차를 미리 준비해 둔 점.
- 다음에 바꿀 것: Gate resolved 직후 실행 성공 여부와 무관하게 INTENTS.md + heartbeat/per-intent 중 최소 1개에 `post-approval status refresh`를 강제해, 최신 문서 세트가 항상 승인 이후 현실을 대표하게 해야 한다.

- 대상 intent: 2026-04-22 20:58 기준 wiki-03 승인 후 stranded Active
- 평가: 승인된 일을 최우선 재개하겠다는 규칙이 있어도, 프로토콜의 우선순위 조건(`blocked 중 승인됨`)과 생명주기 전이(`승인 후 in_progress`)가 서로 충돌하면 승인 성공이 오히려 pickup 표지를 지워 장기 방치를 만든다.
- 근거: workflows/heartbeat.md는 1순위를 `blocked` 중 승인 항목으로 정의하지만 같은 문서는 승인 후 `blocked → in_progress` 전이를 지시한다. 실제 wiki-03도 GATES.md에서는 2026-04-19 23:29 승인 완료, INTENTS.md에서는 여전히 `in_progress`, heartbeat 최신본은 2026-04-19 16:00에 멈춰 있어 승인 후 재개 대상을 규칙상 자동 식별하지 못했다.
- 다음에 유지할 것: 승인 전 드래프트를 남겨 재개 즉시 실행 가능한 준비 상태를 만든 점.
- 다음에 바꿀 것: 승인 직후 상태를 `approved_waiting_execution` 같은 단일 재개 상태로 고정하고, Heartbeat 우선순위 규칙도 그 상태를 1순위로 읽게 맞춰 승인 이벤트가 문서 구조만으로 계속 보이게 해야 한다.

- 대상 intent: 2026-04-22 21:58 기준 wiki-03 단독 Active 장기 방치
- 평가: Active 1건만 남은 단순한 상태에서도 Heartbeat와 per-intent 최신화가 함께 멈추면, 문제는 개별 intent 판단이 아니라 `stale Active를 자동으로 드러내는 감시 규칙`이 없다는 데 있다.
- 근거: 현재 INTENTS.md에는 wiki-03만 `in_progress`로 남아 있고 Inbox와 대기 중 Gate는 비어 있지만, heartbeat 최신본은 2026-04-19 16:00, per-intent 최신본은 승인 직전 blocked 상태인 2026-04-19 23:00에 멈춰 있다. 즉 `할 일 없음`처럼 보이는 표면과 실제 stranded Active가 계속 어긋난다.
- 다음에 유지할 것: Inbox, Active, GATES, per-intent report를 분리해 어디서 상태가 멈췄는지 역추적 가능한 구조.
- 다음에 바꿀 것: `Inbox=0 && pending_gates=0`이면 건강하다고 보지 말고, Active 각 항목의 `last_progress_at`·`last_report_at`·`last_heartbeat_at` 신선도를 함께 검사해 stale Active가 있으면 idle 대신 강제 status refresh 또는 resume escalation을 일으켜야 한다.

- 대상 intent: 2026-04-22 22:59 기준 wiki-03 장기 정체와 평가 루프 자체
- 평가: 같은 운영 결함이 하루 넘게 반복 관측되는데도 평가가 notes에만 누적되면, Infinity는 intent를 못 집는 것뿐 아니라 `평가 결과를 운영 규칙으로 승격하는 루프`도 없는 상태가 된다.
- 근거: wiki-03의 승인 후 stranded Active 문제는 여러 차례 같은 결론으로 평가됐지만, OPERATING_LESSONS와 workflows/heartbeat.md의 우선순위·상태 전이 규칙은 아직 그대로여서 현재 INTENTS.md의 `in_progress` 장기 방치가 계속 재현되고 있다.
- 다음에 유지할 것: 반복 평가를 통해 문제 패턴과 재현 조건을 충분히 명확히 축적한 점.
- 다음에 바꿀 것: 같은 유형 평가가 N회 이상 반복되면 EVALUATION_NOTES에만 더하지 말고, OPERATING_LESSONS 또는 workflows/heartbeat.md 수정 필요 항목으로 자동 승격해 실제 프로토콜 변경 여부를 추적해야 한다.

- 대상 intent: 2026-04-23 01:01 기준 wiki-03 단독 Active와 평가 중복 누적
- 평가: Active 1건이 승인 완료 뒤 `in_progress`로 오래 남아 있는데 Inbox·pending Gate가 비어 있으면 시스템은 겉으로 정상처럼 보이고, 평가도 같은 지적만 반복 생산하게 된다.
- 근거: 현재 INTENTS.md는 wiki-03만 `in_progress`로 남아 있고 GATES.md 대기 중은 비어 있으며 마지막 heartbeat는 2026-04-19 16:00, 최신 wiki-03 report는 2026-04-19 23:00 blocked 문맥에 머물러 있다. 그 사이 승인 완료는 GATES.md에만 기록돼 있어 현재 상태를 다시 쓰는 루프와 평가를 운영 규칙으로 승격하는 루프가 둘 다 비어 있다.
- 다음에 유지할 것: Inbox, Active, GATES, per-intent report를 분리해 어디서 상태가 끊겼는지 추적 가능한 구조.
- 다음에 바꿀 것: `Active>0 && pending_gates=0 && Inbox=0`일 때는 idle로 간주하지 말고 stale Active 검사와 최신 상태 재기록을 강제하며, 같은 평가 포인트가 반복되면 notes 추가 대신 프로토콜 수정 작업을 직접 생성해야 한다.

- 대상 intent: 2026-04-23 03:02 기준 wiki-03 stranded Active와 평가 루프
- 평가: 같은 stranded Active를 하루 넘게 다시 확인했다면, 평가의 다음 역할은 또 한 줄 더 쓰는 것이 아니라 해당 결함을 고치는 운영 변경 작업을 직접 만들게 강제하는 데 있어야 한다.
- 근거: 현재도 INTENTS.md에는 wiki-03만 `in_progress`, GATES.md 대기 중은 비어 있음, 최신 heartbeat는 2026-04-19 16:00, 최신 wiki-03 report는 2026-04-19 23:00 blocked 상태다. 승인 완료 이후 상태 반영 실패와 stale Active 문제는 이미 EVALUATION_NOTES에 반복 축적됐지만 아직 프로토콜 변경 흔적이 없다.
- 다음에 유지할 것: stranded Active를 registry/Gate/report 불일치로 교차 확인하는 평가 관점.
- 다음에 바꿀 것: 동일 평가가 반복 임계치를 넘기면 EVALUATION_NOTES append 대신 `OPERATING_LESSONS` 수정 또는 관련 workflow/intent 생성 여부를 체크하는 승격 절차를 의무화해야 한다.

- 대상 intent: 2026-04-23 12:58 기준 wiki-03 단독 Active와 평가-only 운영
- 평가: 실행·heartbeat·status refresh는 멈췄는데 평가 문서만 계속 늘어나는 상태라면, Infinity는 intent 처리 시스템이 아니라 정지 상태를 기록만 하는 시스템으로 퇴행한다.
- 근거: 현재도 INTENTS.md Active는 wiki-03 하나뿐이고 GATES.md 대기 중은 비어 있으며 최신 heartbeat는 2026-04-19 16:00, 최신 wiki-03 report는 2026-04-19 23:00, 승인 완료는 GATES.md 2026-04-19 23:29에만 남아 있다. 그 뒤 최신성 있는 실행 문서는 없고 EVALUATION_NOTES만 같은 실패를 누적 중이다.
- 다음에 유지할 것: Active/Gates/report/heartbeat를 교차 대조해 운영 정지 지점을 정확히 짚는 평가 방식.
- 다음에 바꿀 것: `stale Active + empty Inbox + empty pending Gates`가 보이면 평가 append보다 먼저 상태 새로고침 또는 프로토콜 수정 intent 생성을 강제해, 평가 문서가 실행 부재를 가리는 대체물로 쓰이지 않게 해야 한다.

- 대상 intent: 2026-04-23 17:02 기준 wiki-03 승인 완료 후 미재개 지속
- 평가: 승인 기록이 Gate 문서에만 남고 Intent·heartbeat·per-intent report가 끝내 승인 후 기준선으로 갱신되지 않으면, 승인 흐름은 성공해도 실행 재개 흐름은 사실상 없는 것과 같다.
- 근거: GATES.md에는 wiki-03의 Gate 2가 2026-04-19 23:29 approved로 닫혀 있지만, 2026-04-23 17:02 현재 INTENTS.md Active는 여전히 `in_progress`, 최신 heartbeat는 2026-04-19 16:00, 최신 wiki-03 report는 2026-04-19 23:00 blocked 상태에 멈춰 있다.
- 다음에 유지할 것: 승인 시각과 결정을 Gate ledger에 정확히 남긴 점.
- 다음에 바꿀 것: gate 승인 직후 같은 턴에 INTENTS.md를 `approved_waiting_execution` 또는 `ready_to_execute`로 강제 전이하고, 일정 시간 내 실행 report가 없으면 heartbeat가 승인 후 stranded 상태를 별도 오류로 승격해야 한다.

- 대상 intent: 2026-04-23 20:57 기준 wiki-03 stranded Active와 평가 문서 누적
- 평가: 같은 stranded Active가 며칠째 그대로인데도 workflow/lessons 수정 없이 평가만 계속 append되면, 평가는 교정 장치가 아니라 중복 로그가 된다.
- 근거: wiki-03는 여전히 INTENTS.md에서 `in_progress`, GATES.md는 모두 resolved, 최신 heartbeat는 2026-04-19 16:00, 최신 per-intent report는 2026-04-19 23:00에 멈춰 있다. 반면 EVALUATION_NOTES에는 같은 결론이 여러 차례 반복됐지만 OPERATING_LESSONS와 workflows/heartbeat.md의 상태 전이 규칙 충돌은 그대로다.
- 다음에 유지할 것: registry·gate·report를 교차 대조해 stranded 상태를 정확히 짚는 평가 방식.
- 다음에 바꿀 것: 동일 유형 평가가 반복 임계치를 넘기면 evaluator는 notes 추가보다 먼저 `OPERATING_LESSONS` 또는 workflow 수정 필요 여부를 확인하고, 변경이 없으면 중복 append를 멈춘 채 프로토콜 수정 작업 생성 여부만 판단하게 해야 한다.

- 대상 intent: 2026-04-24 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: stale Active를 정리한 뒤 Active를 비워 둔 것은 좋지만, 그 직후 Inbox 1건이 하루 넘게 구조화되지 않았다면 운영 실패가 `재개 누락`에서 `pickup 누락`으로만 형태를 바꾼 것이다.
- 근거: 현재 INTENTS.md는 Active가 비어 있는데 Inbox에는 `agent-wiki` 모바일 네비게이션 개선 1건이 남아 있고, heartbeat 최신 기준선은 여전히 2026-04-19에 머물러 있다. 즉 stalled Active는 사라졌지만 최신 요청을 Active/blocked 어디에도 올리지 못해 실행 대기열이 다시 문서 밖으로 밀려났다.
- 다음에 유지할 것: 완료된 intent들을 Active에서 정리해 registry 표면을 단순하게 만든 점.
- 다음에 바꿀 것: `Active=0`은 healthy 신호가 아니라 `Inbox pickup 확인 필요` 신호로 취급하고, heartbeat 공백 상태에서 Inbox가 남아 있으면 evaluator도 중복 관찰 대신 pickup 실패 경보와 구조화 작업 생성 여부를 먼저 보게 해야 한다.

- 대상 intent: 2026-04-24 idle heartbeat 이후 2026-04-27까지 남아 있는 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: stale Active를 치운 뒤에도 Heartbeat가 실제 Inbox 존재를 놓친 채 idle로 닫히고 그 상태가 며칠 유지되면, 시스템은 `정리 완료`처럼 보이면서 새 intent pickup 실패를 장기 은닉한다.
- 근거: 최신 heartbeat report(2026-04-24T00:00)는 `Inbox: 비어있음 / Active: 비어있음`으로 종료했지만 현재 INTENTS.md Inbox에는 동일한 `agent-wiki` 모바일 네비게이션 개선 1건이 그대로 남아 있다.
- 다음에 유지할 것: Active와 Gate를 비워 registry 표면을 단순하게 유지한 점.
- 다음에 바꿀 것: idle 종료 직전 INTENTS.md 원문을 다시 세어 `Inbox=0`을 재검증하고, 실제 Inbox가 남아 있으면 idle 보고 대신 pickup failure로 기록하며 같은 턴에 최소 1건 구조화 또는 구조화 실패 사유를 강제해야 한다.

- 대상 intent: 2026-04-27 시점까지 구조화되지 않은 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 같은 pickup 실패를 3일 넘게 방치했는데도 평가만 누적되고 구조화나 프로토콜 수정으로 승격되지 않으면, evaluator도 운영 복구 장치가 아니라 정지 상태 로그가 된다.
- 근거: 2026-04-24T00:00 heartbeat가 `Inbox 비어있음`으로 idle 종료한 뒤 2026-04-27 03:57 현재까지 INTENTS.md Inbox의 동일 항목이 그대로 남아 있고, 그 사이 새 heartbeat나 구조화 흔적은 없다.
- 다음에 유지할 것: idle heartbeat와 registry 원문을 대조해 pickup 실패를 잡아내는 평가 관점.
- 다음에 바꿀 것: 동일 pickup 실패가 하루 이상 지속되면 EVALUATION_NOTES 추가보다 먼저 `pickup failure` 자체를 운영 변경 필요 항목으로 승격하고, 최소한 다음 heartbeat가 구조화 또는 실패 사유 기록 없이 idle 종료하지 못하게 막아야 한다.

- 대상 intent: 2026-04-27 10:59 기준 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 같은 프로젝트의 직전 완료 산출물(`wiki-03` archive + draft)이 이미 있는데도 후속 개선 요청을 Inbox에 그대로 방치하면, pickup 실패는 단순 지연이 아니라 기존 문맥 재사용 기회를 통째로 버리는 운영 손실이 된다.
- 근거: 현재 INTENTS.md Inbox에는 `agent-wiki` 모바일 네비게이션 개선 1건이 남아 있고, archive/wiki-03.md와 drafts/wiki-03-mobile-nav.md에는 동일 표면 영역의 직전 구현 이력과 수정 초안이 이미 정리돼 있다. 그런데 이를 잇는 Active 구조화 흔적은 없다.
- 다음에 유지할 것: 같은 deliverable의 구현 이력과 초안을 archive/draft로 남겨 둔 점.
- 다음에 바꿀 것: Inbox 항목이 최근 완료 intent와 프로젝트·표면 영역이 겹치면 heartbeat는 새 일인지 후속 확장인지 먼저 판정해 기존 intent lineage와 draft를 연결한 상태로 구조화하고, 그 전까지는 idle 종료를 금지해야 한다.

- 대상 intent: 2026-04-24 12:54 이후 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 이번 핵심 실패는 `idle heartbeat가 Inbox를 오판했다`가 아니라, 새 Inbox가 등록된 뒤 며칠째 heartbeat가 다시 돌지 않아 pickup SLA 자체가 비어 있는 점이다.
- 근거: git 기록상 최신 heartbeat commit은 2026-04-24 10:18(`활성 Intent 없음`)이고, 현재 Inbox 항목 추가 commit은 그 이후인 2026-04-24 12:54다. 즉 00:00 heartbeat의 `Inbox 비어있음` 보고 자체보다, 그 뒤 새 intent 유입 후 상태 새로고침이 전혀 없다는 최신성 공백이 실제 문제다.
- 다음에 유지할 것: Inbox 변경을 별도 commit으로 남겨 유입 시점을 추적 가능하게 한 점.
- 다음에 바꿀 것: 평가와 heartbeat 모두 registry 스냅샷만 보지 말고 `마지막 heartbeat 시각 vs 마지막 Inbox 변경 시각`을 함께 비교해, 오판과 미실행을 구분하고 `새 Inbox 유입 후 N시간 내 pickup` 규칙을 명시해야 한다.

- 대상 intent: 2026-04-28 기준 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 같은 Inbox 항목이 4일째 구조화되지 않았는데도 평가가 여전히 notes에만 머물면, pickup 실패는 이미 관측 문제가 아니라 `평가→프로토콜 수정` 승격이 없는 운영 결함이다.
- 근거: 최신 heartbeat commit은 2026-04-24 idle이고 현재 INTENTS.md Inbox에는 동일 항목이 그대로 남아 있다. 동시에 archive/wiki-03.md에는 같은 프로젝트의 직전 모바일 네비게이션 작업 맥락이 이미 있어, 이번 지연은 단순 미실행이 아니라 기존 문맥 재사용 기회까지 놓치고 있다.
- 다음에 유지할 것: archive와 Inbox를 함께 읽으면 후속 개선 요청의 lineage를 즉시 복원할 수 있는 기록 구조.
- 다음에 바꿀 것: 동일 Inbox pickup 실패가 하루 이상 지속되면 evaluator는 notes 추가를 반복하지 말고 `heartbeat 프로토콜 수정 필요` 또는 `pickup 복구 intent 생성 필요` 여부를 먼저 확인하게 해, 평가가 정지 로그로만 남지 않게 해야 한다.

- 대상 intent: 2026-04-29 기준 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 이제 핵심 실패는 pickup 누락 자체보다, 그 누락이 5일째 지속되는데도 OPERATING_LESSONS와 heartbeat 프로토콜이 전혀 갱신되지 않아 평가가 운영 변경으로 연결되지 않는 점이다.
- 근거: 최신 heartbeat report는 여전히 2026-04-24 idle이고 현재 INTENTS.md Inbox에는 동일 항목이 남아 있다. 또한 관련 git 기록상 2026-04-24 이후 변경은 Inbox 항목 추가뿐이며 OPERATING_LESSONS.md와 workflows/heartbeat.md에는 후속 수정 커밋이 없다.
- 다음에 유지할 것: Inbox 유입 시각과 heartbeat 기준선을 git 기록으로 대조해 `오판`이 아니라 `상태 새로고침 부재`임을 분리해 보는 평가 방식.
- 다음에 바꿀 것: 같은 pickup 실패가 5일 이상 지속되면 evaluator는 notes append보다 먼저 `프로토콜 수정 미반영` 자체를 실패로 판정하고, OPERATING_LESSONS 또는 workflows/heartbeat.md 수정 여부를 필수 체크포인트로 승격해야 한다.

- 대상 intent: 2026-04-30 기준 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 현재 병목은 미처리 Inbox가 아니라, `새 Inbox 유입 후 heartbeat가 다시 돌지 않아 pickup SLA 자체가 사라졌는데도` 이를 복구하는 운영 트리거가 없는 점이다.
- 근거: git 기준 최신 heartbeat 관련 커밋은 2026-04-24 10:18 idle이고, 현재 HEAD의 최신 변경은 같은 날 12:54 Inbox 항목 추가뿐이다. 2026-04-30 현재까지 INTENTS.md Inbox에는 그 항목이 그대로 남아 있으며 OPERATING_LESSONS.md와 heartbeat 프로토콜 수정 흔적도 없다.
- 다음에 유지할 것: Inbox 유입 시각과 마지막 heartbeat 시각을 git으로 대조해 pickup 누락을 상태 스냅샷 오류와 구분하는 관점.
- 다음에 바꿀 것: `last_inbox_change_at > last_heartbeat_at`가 일정 시간 이상 지속되면 evaluator도 중복 notes 추가를 멈추고, heartbeat 재가동 또는 프로토콜 수정 작업 생성 여부를 우선 점검하게 해야 한다.

- 대상 intent: 2026-05-01 기준 Inbox의 `agent-wiki` 모바일 네비게이션 개선 1건
- 평가: 이제 핵심 실패는 pickup 지연이 아니라, 같은 실패가 1주일째 이어지는데도 heartbeat·workflow·lessons 어느 쪽에도 복구 커밋이 없어 평가가 운영 변경으로 전혀 연결되지 않는 점이다.
- 근거: 최신 heartbeat 커밋은 2026-04-24 10:18, Inbox 추가는 2026-04-24 12:54, 현재 INTENTS.md Inbox에는 동일 항목이 그대로 남아 있다. 동시에 workflows/heartbeat.md 최신 커밋은 2026-04-10, OPERATING_LESSONS.md 최신 커밋은 2026-04-19라 반복 평가 이후 프로토콜 수정 흔적이 없다.
- 다음에 유지할 것: heartbeat 시각, Inbox 변경 시각, 프로토콜 문서 커밋 시각을 함께 비교해 `pickup 실패`와 `교정 루프 부재`를 분리해 보는 평가 방식.
- 다음에 바꿀 것: 같은 pickup 실패가 주 단위로 지속되면 evaluator는 notes 누적 대신 `heartbeat 재가동 또는 프로토콜 수정 intent 생성 여부`를 먼저 판정하게 하고, 그 둘 다 없으면 추가 평가 append를 중단해야 한다.

- 대상 intent: 2026-05-10 기준 Inbox의 `바이럴 키워드 추천 스킬 분석자료 만들기` 1건
- 평가: 2026-05-05 00:00 heartbeat가 idle로 닫힌 뒤 같은 날 07:44 새 Inbox가 등록됐는데도 5일째 Active 구조화가 없으므로, heartbeat는 `마지막 heartbeat 이후 Inbox 등록 시각`을 SLA 기준으로 삼아 idle 보고와 실제 pickup 공백을 분리해야 한다.
- 근거: 현재 INTENTS.md Inbox에는 해당 리서치/스킬화 요청이 남아 있고 Active는 비어 있으며, 최신 heartbeat report는 2026-05-05T00:00의 `Inbox 비어있음` 상태다.
- 다음에 바꿀 것: 새 Inbox 등록 후 N시간 내 구조화가 없으면 평가 notes 반복이 아니라 pickup 재가동 또는 구조화 실패 사유 기록을 강제하는 체크를 heartbeat 시작 조건에 넣어야 한다.

- 대상 intent: 2026-05-13 기준 Empty registry와 6일째 갱신되지 않은 heartbeat
- 평가: Inbox/Active가 비어 있어도 마지막 heartbeat가 며칠 전이면 idle 상태가 아니라 heartbeat liveness 공백으로 본다. 다음부터 evaluator는 새 Inbox 유무와 별개로 `last_heartbeat_age`가 임계치를 넘는지 확인해 재가동 또는 스케줄 실패 점검으로 승격해야 한다.

- 대상 intent: 2026-05-15 기준 product-01 사용자 결정 대기 상태
- 평가: 미커밋 UX 배치가 사용자 결정(커밋 분할, design-mockups 처리)을 기다리는 상태라면 `in_progress`만 유지하며 반복 read-only heartbeat/probe를 쌓기보다, registry/active 본문에 `status: waiting_user_decision` 또는 `owner_action`을 명시해 다음 heartbeat가 같은 검증을 중복하지 않게 해야 한다.
- 근거: 최신 리포트 `2026-05-15T04-07-heartbeat.md`는 직전 검증과 로컬/배포 상태가 동일하고 새 결정사항이 없다고 판단했지만, INTENTS.md와 active intent는 여전히 단순 `in_progress`로 남아 있어 사용자 결정 대기 상태가 구조화 필드로 드러나지 않는다.
- 다음에 바꿀 것: L2를 실행하지 않기로 한 이유가 사용자 선택 대기라면 리포트 문장뿐 아니라 registry 상태 필드와 next_check 조건에 반영해, 이후 heartbeat는 상태 변화나 사용자 응답이 있을 때만 깊은 검증으로 들어가게 한다.
