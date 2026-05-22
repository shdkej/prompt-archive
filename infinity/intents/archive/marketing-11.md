# marketing-11 Intent 원장

- id: marketing-11
- title: Virtue 첫 실제 사용자 기준선 템플릿 작성
- status: archived
- created_at: 2026-05-22T22:07Z
- completed_at: 2026-05-22T22:17Z
- mode: execute_local
- route: Infinity router -> local Claude Code (workflow-master classification: medium scope, 4-role Planner/Developer/Marketer/Operator synthesis)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repo
- result_summary: Virtue 첫 10~20명 실사용자 기준선을 한 명당 한 행으로 적는 내부 문서를 추가했다. 문서는 J1~J4 분류, 유입 문장, first/second value 기록칸, synthetic/test traffic 제외 기준, prelaunch 해석 금지선, 주간 리뷰 리듬, 기존 이벤트 근거를 포함한다. 핵심 이벤트는 기존 `add_flow_started`, `deed_judged`, `deed_saved`, `level_up_viewed`만 사용하고, 신규 이벤트·속성·코드·대시보드·외부 발송·비용 작업은 0건이다. `activation-milestone-ladder.md`와 `time-to-value-observation-brief.md`의 역할을 재정의하지 않고 계승하며 충돌 점검을 통과했다.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/first-real-user-baseline-template.md
  role: planning (marketing/first-user-baseline)
  note: 첫 실사용자 기준선 수기 기록용 L1 내부 문서. 자동화·대시보드·외부 모집 지시서가 아니다.

## Reports

- path: infinity/reports/marketing-11/2026-05-22T2207Z.md
  role: final
  note: workflow-master 실행 로그, 검증 게이트, 커밋/푸시 결과, 금지 항목 준수 기록.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-22-own-baseline-onboarding-metrics.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/time-to-value-observation-brief.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/activation-milestone-ladder.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/add/page.tsx

## Success Criteria Coverage

| 성공 기준 | 충족 위치 |
|---|---|
| 첫 10~20명 기준선 표 | `first-real-user-baseline-template.md` §2 |
| J1~J4 분류 | §2-1 |
| 유입 문장 기록 | §2, §3 |
| 기존 이벤트 4개만 핵심 사용 | §0, §2-1, §7 |
| first/second value 기록칸 | §2, §2-1 |
| synthetic/test traffic 제외 기준 | §2, §4 |
| prelaunch 해석 금지선 | §0, §1, §5 |
| ladder/TTV 충돌 0 | §8 |

## Verification

- `rg -n "add_flow_started|deed_judged|deed_saved|level_up_viewed|synthetic|test traffic|prelaunch|J1|J2|J3|J4" docs/first-real-user-baseline-template.md` -> PASS.
- `rg -n "first real user|baseline|prelaunch|J1|J2|J3|J4" docs/time-to-value-observation-brief.md docs/activation-milestone-ladder.md || true` -> 선행 문서와 용어/역할 일관, 충돌 0.
- 코드 근거 read-only 확인: `add_flow_started` at `src/app/add/page.tsx:72`, `deed_judged` at `:106`, `deed_saved` at `:183`, `level_up_viewed` at `:199`.
- 앱 코드, 설정, 대시보드, 트래킹, 외부 발송, 권한, 시크릿, 비용 변경 0건.

## Commits

- repo: virtue-rebirth-app
  commit: ebd5781
  note: `docs/first-real-user-baseline-template.md` 추가, `origin/master` 비force push 완료.
- repo: prompt-archive
  note: `infinity/reports/marketing-11/2026-05-22T2207Z.md`, `infinity/intents/archive/marketing-11.md`, `infinity/INTENTS.md` 갱신 대상.

## Next Actions

- post-launch 실제 대시보드/자동 집계/정기 알림은 별도 approval-needed Intent로만 진행.
- marketing-10의 `time-to-value-observation-brief.md`는 별도 waiting intent 소관이며 본 intent에서 처리하지 않았다.
