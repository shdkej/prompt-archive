# marketing-10 Intent 원장

- id: marketing-10
- title: Virtue Time-to-Value 관찰 기준표 작성
- status: archived
- created_at: 2026-05-22T10:00Z
- completed_at: 2026-05-23T16:07Z
- mode: execute_local
- route: Infinity router -> local Claude Code (`claude --dangerously-skip-permissions`) -> heartbeat completion after Claude hung post-write
- permission: L1 internal docs + agent-approved L2 push
- project: `/home/ubuntu/dev/virtue-rebirth-app`
- final artifact: `/home/ubuntu/dev/virtue-rebirth-app/docs/time-to-value-observation-brief.md`
- result_summary: J1-J4별 first value, second value, time gap 계산 방식, 정성 확인 질문, prelaunch 해석 금지선을 정리한 내부 관찰 기준표를 추가했다. 기존 이벤트 `add_flow_started`, `deed_judged`, `deed_saved`, `level_up_viewed`만 사용했고 신규 이벤트·속성·코드·대시보드·외부발송·비용·시크릿·권한 변경은 0건이다.
- execution_note: Claude Code가 문서 초안을 작성한 뒤 응답 없이 장시간 대기해 프로세스를 종료했다. Heartbeat가 금지된 보조 이벤트 언급을 제거하고 검증·커밋·push·Infinity bookkeeping을 완료했다.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/time-to-value-observation-brief.md
  role: internal observation brief
  note: 첫 10명 prelaunch 관찰 시 first value/second value 시간 간격을 같은 기준으로 기록하기 위한 문서. 성패/retention/PMF 판정 기준이 아니다.

## Reports

- path: infinity/reports/marketing-10/2026-05-23T1607Z.md
  role: final
  note: Claude Code 위임, L2 push 자체 승인 근거, 검증 결과, 커밋 정보를 기록했다.

## Sources

- /home/ubuntu/.openclaw/workspace/external-repos/prompt-archive/infinity/artifacts/marketing-10/time-to-value-observation-brief.md
- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-22-time-to-value-second-value.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/activation-milestone-ladder.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/minimum-viable-audience-brief.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/pmf-response-analysis-rubric.md

## Success Criteria Coverage

| 성공 기준 | 충족 위치 |
|---|---|
| J1-J4별 first/second value 정의 | `docs/time-to-value-observation-brief.md` §1 |
| time gap 계산 방식 | §1, §2, §3 |
| 정성 확인 질문 | §1, §3 |
| prelaunch 해석 금지선 | §0, §1, §2, Out of scope |
| 기존 이벤트만 사용 | §0, §1, §2, 검증 매핑 |

## Verification

- `rg -n "deed_judged|deed_saved|add_flow_started|level_up_viewed" docs/time-to-value-observation-brief.md` -> PASS.
- `rg -n "<<<<<<<|=======|>>>>>>>" docs/time-to-value-observation-brief.md || true` -> 출력 없음(clean).
- `git status --short` before commit showed only `?? docs/time-to-value-observation-brief.md` in `virtue-rebirth-app`.
- Forbidden scope check: code/runtime/PostHog/dashboard/event/property/external-send/production/cost/secret/permission changes 0건.

## Commits

- repo: virtue-rebirth-app
  commit: c32033f
  note: `docs/time-to-value-observation-brief.md` 추가(+80), `origin/master` non-force push 완료.
- repo: prompt-archive
  note: `INTENTS.md`, `infinity/intents/archive/marketing-10.md`, `infinity/reports/marketing-10/2026-05-23T1607Z.md` bookkeeping만 커밋·push 대상. 기존 미커밋 evaluation 파일은 제외.

## Next Actions

- PostHog 대시보드, 신규 이벤트/속성, 외부 인터뷰/DM/공개 모집은 별도 approval-needed Intent에서만 처리한다.
