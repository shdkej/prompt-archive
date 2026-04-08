Infinity Agent-First 시스템 명령입니다. INFINITY.md를 읽고 아래 동작을 수행하세요.

사용자 입력: $ARGUMENTS

## 동작 분기

입력이 없거나 "status"면:
- infinity/INTENTS.md의 Inbox와 Active 표시
- infinity/GATES.md의 대기 중 항목 표시

입력이 "승인" 또는 "approve"면:
- infinity/GATES.md 대기 중 항목을 처리 완료로 이동
- infinity/INTENTS.md에서 blocked → in_progress로 변경
- 커밋 & 푸시

입력이 "run"이면:
- RemoteTrigger 도구로 trig_01Fubp8g8UDKQtvuSkFofPuM 즉시 실행

그 외 모든 입력은 Intent 추가:
- infinity/INTENTS.md의 ## Inbox에 `- {입력 내용}` 추가
- 커밋 & 푸시
- "Intent 등록 완료. 다음 Heartbeat에서 처리됩니다." 응답
