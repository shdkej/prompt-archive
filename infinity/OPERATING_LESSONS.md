# OPERATING_LESSONS

Infinity 운영 중 intent 처리 방식에 실제로 영향을 주는 규칙만 기록한다.

## 기록 원칙
- 단순한 작업 기록이 아니라 다음 intent 처리 방식을 바꾸는 교훈만 남긴다.
- 승인 흐름, 병렬도, pickup 방식, 보고 방식처럼 운영 레벨의 규칙을 우선한다.
- 재사용 가치가 낮은 일회성 메모는 쓰지 않는다.

## 현재 규칙
- Infinity는 즉시 실행 도구라기보다 intent를 등록해 heartbeat가 구조화·실행·보고하는 운영 루프다.
- 병렬 실행은 무한 확장보다 제한된 동시성으로 제어하는 편이 안정적이다.
- 사용자가 Infinity에 등록하라고 한 내용은 적절한 repo/workflow 위치에 정확히 남기는 것이 중요하다.
- intent 처리 시스템은 실행 자체보다 pickup, 구조화, 승인, 보고 흐름을 더 잘 설계할수록 품질이 좋아진다.
- "환경 제약"으로 blocked 처리하기 전에 대안 경로를 최소 2개 이상 확인한다(예: MCP 실패 → gh CLI → git+PAT). 한 가지 도구의 한계를 전체 환경의 한계로 일반화하지 않는다. (wiki-02: MCP 실패만 보고 18회 blocked 반복, 실제로는 gh CLI로 5분 내 실행 가능했음)
- "웹 UI 필수"처럼 운영 수단을 제약하는 주장은 실제 시도 결과나 공식 문서 근거 없이 믿지 않는다. 설계 문서에 그렇게 적혀 있어도 실행 단계에서 재검증한다. (wiki-02: 설계안은 "Pages 활성화는 웹 UI 필수"였으나 `gh api POST /repos/.../pages`로 해결됨)
- 같은 Intent가 연속 N회 이상 동일 사유로 blocked 리포트만 쌓이면, heartbeat는 자동 실행 재시도가 아니라 사용자에게 "대안 경로 요약 + 결정 요청"으로 에스컬레이션한다.
- 배포가 "build success"라도 실제 콘텐츠 탐색이 되는지 사용자 관점에서 검증하기 전에 Intent를 complete로 닫지 않는다. URL 200 응답은 필요조건일 뿐 충분조건이 아니다. (wiki-02: 초기 배포는 200 OK였으나 `/docs` 외부 콘텐츠는 모두 접근 불가 → 사용자가 직접 발견해서야 수정)
- 사용자가 Infinity 승인을 요청하면, 승인 처리 전에 먼저 `prompt-archive` 최신 변경을 `git pull`로 받아 현재 gate/intent 상태를 기준으로 승인한다.
- Infinity evaluator는 `EVALUATION_NOTES.md` 전체를 매번 읽지 않는다. 정기 평가는 `EVALUATION_INDEX.md`와 최근 80줄만 읽고, 전체 재독해는 명시 감사나 요약 충돌 때만 허용한다.
- Research/prepare Intent를 완료 처리할 때는 `INTENTS.md` 아카이브만 하지 말고, 산출물 경로와 다음 실행 선택지를 사용자에게 도달 가능한 채널로 보고한다. 완료됐지만 사용자가 산출물을 못 봤다면 운영 실패로 본다.
- Intent 결과물이 `drafts/`, `reports/`, active intent 본문에 흩어지면 사용자가 같은 결론을 다시 찾기 위해 운영자처럼 디렉터리를 뒤져야 한다. 운영 규칙: 산출물은 `infinity/artifacts/{id}/`, 실행 로그는 `infinity/reports/{id}/`, **canonical 결과는 `infinity/intents/archive/{id}.md`에 링크 인덱스로** 모은다. 자세한 규칙은 `infinity/ARTIFACT_RULES.md`. `drafts/`는 2026-05-13에 폐기되어 `artifacts/{id}/`로 이관 완료.
- Archive intent는 짧은 회고문서가 아니라 **canonical index**다. artifacts / reports / commits / urls / next_actions 링크가 모두 한 문서에 모여 있어야 다음 Heartbeat나 사용자가 한 번에 도달 가능하다.
