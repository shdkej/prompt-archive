# marketing-09 Intent 원장

- id: marketing-09
- title: Virtue 활성화 마일스톤 사다리 문서화
- status: archived
- created_at: 2026-05-21T22:00Z
- completed_at: 2026-05-21T22:07Z
- mode: execute_local
- route: Infinity router → local Claude Code (workflow-master classification: medium scope, 단일 문서이나 선행 4문서 종합 + 4역할 렌즈 필요. Planner/Developer/Marketer/Operator 병렬 실행 후 workflow-master가 공통 파일 중재 통합)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repos
- result_summary: 활성화를 한 이벤트가 아니라 setup→aha→habit 사다리로 재정의한 단일 내부 문서를 추가했다. J1 기록형/J2 누적형/J3 AI 호기심형/J4 회고형 4잡을 `setup moment · aha moment · habit moment · 기존 이벤트 · 해석 주의(+prelaunch 판정 보류)` 6칸 매트릭스로 매핑하고, 단계별 공통 정의 + 코드 근거 표(`src/app/add/page.tsx` 라인)를 붙였다. 매핑은 setup=`add_flow_started`(페이지 진입=의도 진입), aha=`deed_saved`(J1/J2/J4)·`deed_judged`(J3, 저장 전·독립 발화), habit=반복 `deed_saved`(distinct-day 계산형) + 누적형 보조 `level_up_viewed`. `deed_save_capped` early-return으로 캡 차단 시도는 저장 미집계라는 코드 사실 반영. prelaunch라 어떤 단계 도달률도 성패가 아니라 관찰 기준임을 못박고(setup→aha/aha→habit 전환율 판정 금지, judged−saved 갭 이탈 단정 금지, 40% 임계값 미적용), 첫 10명 이름·상황 단위 수기 관찰만 L1로 허용. 선행 매핑(first-session-jtbd-matrix / seven-day-deed-loop / pmf-response-analysis-rubric / minimum-viable-audience-brief)을 재정의 없이 계승. 신규 이벤트·속성·카피·코드·대시보드·외부발송 0건. copy-spec 금지어 충돌 0건.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/activation-milestone-ladder.md
  role: planning (marketing/activation)
  note: Virtue 앱 레포 내 내부 L1 기획 산출물. 측정/대시보드 구현 지시서가 아니며 관찰 기준 정의까지만 둠.

## Reports

- path: infinity/reports/marketing-09/2026-05-21T2207Z.md
  role: final
  note: 본 실행 1회 로그. workflow-master 4역할 병렬 분류, L2 체크리스트, 검증 게이트 4종(PASS), 커밋/푸시 정책 기록.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-activation-milestone-ladder.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/pmf-response-analysis-rubric.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/minimum-viable-audience-brief.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/add/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/lib/species.ts

## Success criteria coverage

| 성공 기준 | 충족 위치 |
|---|---|
| J1~J4 각각 setup/aha/habit moment | ladder §2 (심장 매트릭스 4행) + §3 (단계별 공통 정의) |
| 기존 이벤트 매핑 (신규 0) | ladder §2 "기존 이벤트" 컬럼 + §3 코드 근거 표 + §5 측정 후보 표 |
| 해석 주의점 | ladder §1 "왜 한 이벤트만 보면 안 되는가" + §2 "해석 주의" 컬럼 |
| prelaunch 판정 금지선 | ladder §0 전제 + §4 "아직 판정하지 않는다" |
| first-session-jtbd-matrix / seven-day-deed-loop / pmf-response-analysis-rubric 충돌 0 | ladder §6 충돌 점검 |

## Verification

- grep gate: `rg -n "deed_judged|deed_saved|add_flow_started|level_up_viewed" docs/activation-milestone-ladder.md docs/first-session-jtbd-matrix.md docs/seven-day-deed-loop.md` → 55매치(신규 35 / jtbd 11 / 7day 9). 이벤트명 일관.
- 7개 이벤트 발화를 `src/app/add/page.tsx`에서 라인 근거로 확인(add_flow_started:72, deed_judged:106, deed_saved:183, level_up_viewed:199, deed_rerolled:149, deed_save_capped:167, deed_judge_attempted:135).
- 신규 이벤트/속성/대시보드/카피/코드/배포/CI/시크릿/권한/비용/외부발송 변경 0건. `docs/` 한 파일만 신규 추가.
- copy-spec 금지어 미검출. 선행 문서 미수정(계승만).

## Commits

- repo: virtue-rebirth-app
  note: docs/activation-milestone-ladder.md 추가, origin/master 비force push.
- repo: prompt-archive
  note: infinity/reports/marketing-09/2026-05-21T2207Z.md + infinity/intents/archive/marketing-09.md + INTENTS.md 갱신. push 전 fetch→rebase 후 origin/main 비force push.

## URLs

- 외부 URL 게시 없음. 모든 변경은 내부 문서 및 사내 리포 한정.

## Next Actions

- 첫 10명 "가치 단계 도달" 수기 관찰표 양식 작성 — L1 내부 문서로 가능(별도 Intent).
- PostHog 사다리 단계별 도달 대시보드 — tracking/privacy 점검 + 대시보드 변경 승인 후 Waiting.
- 외부 설문/모집/DM 발송 — approval-needed/Waiting 유지.
- 정식 출시 후 실 데이터로 사다리 칸 도달률 해석 기준 재평가 + 본 문서 갱신.
