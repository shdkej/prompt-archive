# marketing-12 Intent 원장

- id: marketing-12
- title: Virtue 활성화 경로 마찰 감사표 작성
- status: archived
- created_at: 2026-05-23T10:07Z
- completed_at: 2026-05-23T10:18Z (산출물 커밋 fc08cf4 시각, 동시/선행 실행)
- verified_at: 2026-05-23T10:07Z (본 실행의 검증·보고 시각)
- mode: execute_local
- route: Infinity router -> local Claude Code (workflow-master: 최초 중간 분류 → 산출물 기존재 확인 후 검증·보고 모드로 축소)
- permission: L1 internal docs only + Infinity 리포트/상태 갱신(prompt-archive matching origin push)
- result_summary: 활성화 경로 `/`(첫 화면) → `/add`(입력) → 채점(`deed_judged`) → 저장·누적 피드백(`deed_saved`·`level_up_viewed`)을 4스텝(S1~S4)으로 고정하고, 그 위 마찰을 J1~J4 잡별로 좋은 마찰/나쁜 마찰/보류/마찰 거의 없음으로 분류한 L1 내부 감사표를 추가했다. 같은 마찰이 잡에 따라 부호가 뒤집힘(예: AI 채점 대기는 J3엔 좋은 마찰, J1·J4엔 나쁜 마찰)을 핵심으로 하고, prelaunch용 제3분류 "보류"를 명시했다. 핵심 이벤트는 기존 `add_flow_started`/`deed_judged`/`deed_saved`/`level_up_viewed`(+보조 `deed_rerolled`/`deed_save_capped`)만 인용하고 신규 이벤트·속성·코드·카피·대시보드·외부발송·비용은 0건이다. 선행 6문서(activation-milestone-ladder/first-session-jtbd-matrix/first-real-user-baseline-template/seven-day-deed-loop/time-to-value-observation-brief/empty-state-first-action-audit)와 copy-spec 금지어 충돌 0.
- execution_note: 산출물은 동시/선행 실행이 커밋 `fc08cf4`로 이미 생성·origin/master push 완료한 상태였다. 본 실행은 동일 문서를 재생성하지 않고, 검증 게이트 3종 PASS 확인 + 누락된 Infinity 리포트/상태 보완으로 마무리했다. virtue-rebirth-app 레포에는 본 실행의 새 변경/푸시 없음.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/activation-path-friction-audit.md
  role: planning (marketing/activation-friction-audit)
  note: 첫 10명 관찰 시 사람이 *읽는* 동반 참조표. 마찰 *분류* 렌즈이지 마찰 *처분* 결정문이 아니며 자동화·대시보드·외부 모집 지시서가 아니다.

## Reports

- path: infinity/reports/marketing-12/2026-05-23T1007Z.md
  role: final
  note: 검증·보고 모드 결정 근거, 검증 게이트 3종 결과, 선행 커밋(fc08cf4) 확인, push 범위(prompt-archive 3파일만) 기록.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-23-outcome-based-onboarding.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/activation-milestone-ladder.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-real-user-baseline-template.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/time-to-value-observation-brief.md (읽기 전용 참조, marketing-10 소관)
- /home/ubuntu/dev/virtue-rebirth-app/docs/empty-state-first-action-audit.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/add/page.tsx, src/app/page.tsx

## Success Criteria Coverage

| 성공 기준 | 충족 위치 |
|---|---|
| `/`→`/add`→채점→저장/누적 피드백을 J1-J4별로 나눈 감사표 | §1 경로 4스텝 + §2 J1~J4 × 경로 매트릭스 + §3 잡별 보충 |
| 좋은/나쁜/보류 분류 | §2 분류 셀 + §4 분류 원칙 |
| 선행 문서 충돌 0 | §0 + §8 충돌 점검(선행 6문서 + copy-spec) |
| 신규 이벤트/속성/코드/카피/대시보드/외부발송/비용 0 | §0 전제2 + §5 + §7 + Out of scope |
| prelaunch 판정 보류 경계 | §0 전제1 + §6 |

## Verification

- `rg -n "deed_judged|deed_saved|add_flow_started|J1|J2|J3|J4" docs/activation-path-friction-audit.md` -> PASS (4개 이벤트 + J1~J4 모두 매칭).
- `rg -n "신규 이벤트|외부 발송|대시보드|코드|비용" docs/activation-path-friction-audit.md` -> PASS (전부 "0/하지 않음" 맥락).
- `rg -n "<<<<<<<|=======|>>>>>>>" docs/activation-path-friction-audit.md || true` -> 출력 없음(clean).
- 코드 근거 라인번호(`add/page.tsx:72/106/183/199/149/167`)가 ladder·baseline과 드리프트 0.
- 앱 코드/설정/대시보드/트래킹/외부발송/권한/시크릿/비용 변경 0건.

## Commits

- repo: virtue-rebirth-app
  commit: fc08cf4 (동시/선행 실행)
  note: `docs/activation-path-friction-audit.md` 추가(+155), `origin/master` 비-force push 완료. 본 실행의 추가 푸시 없음.
- repo: prompt-archive
  note: `infinity/reports/marketing-12/2026-05-23T1007Z.md`, `infinity/intents/archive/marketing-12.md`, `infinity/INTENTS.md`(inbox→archive) 3파일만 커밋·matching origin push. 타 에이전트 미커밋 파일은 제외.

## Next Actions

- post-launch 실제 funnel/대시보드/자동 집계/정기 알림은 별도 approval-needed Intent로만 진행.
- 마찰 제거/완화 실행은 실 사용자 데이터로 패턴 확인 후 별도 Intent에서 결정(§6 경계).
- marketing-10 `time-to-value-observation-brief.md`는 별도 waiting intent 소관, 본 intent에서 처리하지 않았다.
