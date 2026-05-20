# router-maintenance · 2026-05-16T07:07Z · marketing-01 stale inbox cleanup

## 분류

- 유형: Infinity 의도 레지스트리 bookkeeping
- 워크플로우 마스터 판정: **trivial** (L0/L1)
  - 4-역할 패널 미적용. 코드/사용자 인터페이스/자동화/외부 시스템 영향 없음.
  - `.agent/workflows/workflow-master.md` §29 "충돌 중재 시 Edit 1-2건 + plan/리포트 작성" 조항에 해당.
- 진입 의도: Infinity 라우터가 다음 heartbeat에서 완료 처리된 `marketing-01`을 다시 Inbox 항목으로 처리하지 않도록 정합성 회복.

## 문제 정의

- `infinity/INTENTS.md`: Inbox / Active / Waiting 모두 비어 있음. Archive 주석에 `marketing-01` 완료(2026-05-16T06:14Z) 기록 존재.
- `infinity/intents/archive/marketing-01.md`: 정본. `status: completed`, 배포 commit `148b1cc`, 검증 리포트 `infinity/reports/marketing-01/2026-05-16T06-14-local-execution.md`.
- `infinity/intents/inbox/marketing-01.md`: 정본과 충돌. 본문은 여전히 `Status: Inbox`. 2026-05-15T19:07 마지막 수정 이후 그대로 트래킹됨.
- `infinity/GATES.md`: 대기 중인 게이트 없음.
- 사전 git status: clean.

## 조치

1. 정본(`archive/marketing-01.md`) 보존 — 손대지 않음.
2. 중복 stale 파일 `infinity/intents/inbox/marketing-01.md`를 `git rm`으로 제거. 복구 가능(reflog · 동일 내용은 정본 archive와 별개 시점 스냅샷이지만, 운영 의미상 정본이 진실).
3. 본 리포트 신규 생성 — `infinity/reports/router-maintenance/2026-05-16T07-07-stale-inbox-cleanup.md`.
4. 단일 커밋으로 prompt-archive 부킹 수정.
5. origin/main 푸시.

## L2 승인 체크리스트 (agent-approved)

| 항목 | 결과 |
| --- | --- |
| 영향 범위 | prompt-archive 의도 레지스트리만 (정본 미변경) |
| 가역성 | git revert / restore로 즉시 복구 가능 |
| 비용 | 없음 |
| 프로덕션 영향 | 없음 (Virtue 배포물 미관여) |
| 시크릿/권한 | 미변경 |
| 제3자 메시지 | 없음 |
| 강제 푸시/reset | 사용 안 함 |

→ 푸시 진행 적합.

## 검증

- `git status`: 커밋 후 clean.
- `find infinity/intents/inbox -maxdepth 1 -type f`: stale `marketing-01.md` 부재.
- `infinity/INTENTS.md`: Inbox/Active/Waiting empty 유지, marketing-01은 Archive 주석에만 잔존.
- `infinity/intents/archive/marketing-01.md`: 미변경.

## 후속

- 다음 heartbeat 시 추가 액션 불필요. 활성 Intent 없음 상태 유지.
- 향후 동일 패턴 방지를 위해 라우터 측에서 "intent 완료 시 inbox 파일 자동 삭제 또는 status 동기화" 규칙을 검토할 수 있으나, 본 정리에서는 범위 외로 둔다.
