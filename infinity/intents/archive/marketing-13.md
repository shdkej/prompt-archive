# marketing-13 Intent 원장

- id: marketing-13
- title: Virtue 경쟁 대안 기반 포지셔닝 브리프 작성
- status: archived
- created_at: 2026-05-23T22:07Z
- completed_at: 2026-05-23T22:14Z (산출물 커밋 dc0ce55 시각, 직전 실행)
- verified_at: 2026-05-23T22:07Z (본 실행의 검증·보고 시각)
- mode: execute_local
- route: Infinity router -> local Claude Code (workflow-master: 간단~중간 분류 → 4역할 병렬 재합성으로 교차검증 → 산출물 기존재 확인 후 검증·마감 모드)
- permission: L1 internal docs only + Infinity 리포트/상태 갱신(prompt-archive matching origin push)
- result_summary: J1 기록형/J2 누적형/J3 AI 호기심형/J4 회고형 × 5축(① 경쟁 대안 ② Virtue 차별 속성 ③ 고객 가치 ④ 현재 첫 화면 신호 ⑤ 첫 10명 검증 질문)을 한 표로 정리한 L1 내부 포지셔닝 브리프를 추가했다. April Dunford("고객이 우리 없이 실제로 무엇을 할지" = 경쟁 대안에서 출발) + Seth Godin(smallest viable audience) 렌즈. 핵심: J1·J4의 최강 경쟁 대안은 유사 앱이 아니라 "아무것도 안 하기"(do nothing)이고, 첫 화면(`/`=`src/app/page.tsx`) 신호는 J2(덕력·환생종) 최강·J3는 `/add` 진입 전 사실상 부재(코드 file:line 근거 + `INITIAL_VIRTUE` 베이스값/`mock` 라벨 주의 명시). §6 후보 positioning 문구 4종은 internal draft로 앱 미반영·copy-spec 금지어 0. 기존 6개 이벤트(`add_flow_started`/`deed_judged`/`deed_saved`/`level_up_viewed`/`deed_rerolled`/`deed_save_capped`)만 인용, 신규 이벤트·속성·코드·카피·대시보드·외부발송·비용·시크릿·권한 변경 0건. 7개 선행 문서(copy-spec/first-session-jtbd-matrix/pmf-response-analysis-rubric/minimum-viable-audience-brief/activation-milestone-ladder/activation-path-friction-audit/time-to-value-observation-brief) 충돌 0.
- execution_note: 2단계 처리(marketing-12와 동일 패턴). (1) cloud Heartbeat(prompt-archive `e7e4d35`)가 Inbox 자유텍스트를 구조화해 Active(in_progress)로 올리고 `infinity/artifacts/marketing-13/competitive-alternatives-positioning-brief.md` 초안 + report `2206Z` 작성 후 execute_local 위임(source note는 cloud 접근 불가로 local 보강 명시). (2) 직전 local Claude Code 실행이 source note·코드를 읽어 실제 문서를 `apps/web/docs/...`로 작성·커밋(virtue-rebirth-app `dc0ce55`, author shdkej)·origin/master push 후 무응답 종료. (3) 본 실행은 동일 문서를 재생성/수정하지 않고 workflow-master 4역할(Planner/Developer/Marketer/Operator) 병렬 패스로 내용을 독립 재합성해 기존 문서와 결론이 수렴함을 교차검증한 뒤, 검증 게이트 4종 PASS 확인 + Infinity 리포트/상태(Active→Archive) 보완으로 마감했다(본 커밋은 cloud `e7e4d35` 위에 rebase). virtue-rebirth-app 레포에는 본 실행의 새 변경/푸시 없음.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/apps/web/docs/competitive-alternatives-positioning-brief.md
  role: planning (marketing/positioning)
  note: 첫 10~20명 관찰 *전*의 포지셔닝 앵커. 성패 판정·전환율 판정·세그먼트 확정용 아님. 레지스트리는 `docs/`로 약칭하나 정본 경로는 형제 문서들과 같은 `apps/web/docs/`(marketing-10 선례 일치).

## Reports

- path: infinity/reports/marketing-13/2026-05-23T2207Z.md
  role: final
  note: provenance(직전 dc0ce55 push 확인), 경로 약칭 해소, workflow-master 4역할 교차검증, 검증 게이트 4종 결과, push 범위(prompt-archive 3파일) 기록.
- path: infinity/reports/marketing-13/2026-05-23T2206Z.md
  role: cloud draft 단계 (Heartbeat)
  note: Inbox→Active 구조화, cloud draft artifact 작성, source note cloud 접근 불가로 local 보강 위임 기록.

## Cloud draft artifact

- path: infinity/artifacts/marketing-13/competitive-alternatives-positioning-brief.md
  role: cloud 초안 (참조용, 정본 아님)
  note: 정본은 virtue-rebirth-app `apps/web/docs/competitive-alternatives-positioning-brief.md`(dc0ce55). 본 초안은 cloud 단계 산출물로 보존만 함.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-23-competitive-alternatives-positioning.md
- April Dunford, "A Quickstart Guide to Positioning" / "Positioning and Competition"
- Seth Godin, "The smallest viable audience" / "The MVP and fear" / "Big scale, big impact"
- /home/ubuntu/dev/virtue-rebirth-app/apps/web/docs/{copy-spec,first-session-jtbd-matrix,pmf-response-analysis-rubric,minimum-viable-audience-brief,activation-milestone-ladder,activation-path-friction-audit,time-to-value-observation-brief}.md
- /home/ubuntu/dev/virtue-rebirth-app/apps/web/src/app/page.tsx, src/app/add/page.tsx

## Success Criteria Coverage

| 성공 기준 | 충족 위치 |
|---|---|
| J1~J4 각각 경쟁 대안·차별 속성·고객 가치·첫 화면 신호·첫 10명 검증 질문 한 표 | §1 메인 표 (J1~J4 × ①~⑤) |
| 첫 화면 신호 코드 근거 | §3 (file:line) + 주의 1~3 |
| Dunford/Godin 렌즈 | §0 + §4(Godin SVA) + §5(Dunford 프레임 긴장) |
| copy-spec/jtbd-matrix/pmf-rubric/mva-brief 충돌 0 | §6 copy-spec 대조 + §9 정합 확인(7문서) |
| 신규 이벤트/속성/코드/카피/대시보드/외부발송/비용 0 | §7(기존 이벤트만) + §8 가드레일·외부발송 경계 |
| prelaunch 해석 금지선 | §0 + §8 |

## Verification

- `rg '<<<<<<<|=======|>>>>>>>' apps/web/docs/competitive-alternatives-positioning-brief.md || true` -> 출력 없음(clean, PASS).
- copy-spec 금지어 grep 4매치 전부 오탐/메타맥락: line 22·52·95 = "선행 문서"(이전 문서, 금지어 "선행"≠좋은 행동 의미), line 91 = copy-spec 준수 점검 노트의 금지어 명단 나열. 후보 user-facing 카피: §6 4종은 "internal draft, not approved copy"로 명시(앱 미반영), 금지어 0. → 앱 반영 user-facing 카피 none.
- 커밋 dc0ce55 scope: 문서 1개(+114)만 변경. 코드/설정/대시보드/트래킹/외부발송/권한/시크릿/비용 변경 0건.
- `git -C /home/ubuntu/dev/virtue-rebirth-app status --short` -> clean. HEAD == origin/master == dc0ce55(이미 push).

## Commits

- repo: virtue-rebirth-app
  commit: dc0ce55 (직전 실행, author shdkej)
  note: `apps/web/docs/competitive-alternatives-positioning-brief.md` 추가(+114), `origin/master` 비-force push 완료. 본 실행의 추가 커밋/푸시 없음.
- repo: prompt-archive
  cloud_stage: e7e4d35 [marketing-13] Inbox→Active cloud draft (artifact + report 2206Z + INTENTS 구조화). 본 실행 커밋은 이 위에 rebase.
  note: `infinity/reports/marketing-13/2026-05-23T2207Z.md`, `infinity/intents/archive/marketing-13.md`, `infinity/INTENTS.md`(Active→Archive) 3파일만 커밋·matching origin/main push(비-force). 레포에 사전 존재하던 무관 변경(EVALUATION_INDEX/NOTES, marketing-10 report)은 stash로 보존·제외.

## Next Actions

- §6 후보 문구를 사용자 노출 카피로 승격하려면 별도 카피 검수 + 앱 톤(`~요`/`~네요`) 재작성 + copy-spec 금지어 재대조가 선행되어야 한다(별도 Intent).
- 첫 10~20명 실사용 관찰 후 ①~③ 가설(경쟁 대안·차별 속성·이기는 가치) 검증과 메인 프레임(J2 우세) 확정은 차기 positioning audit 입력으로 재검토.
- §3 주의1의 `INITIAL_VIRTUE` 베이스값 vs `first-session-jtbd-matrix.md:47` "count===0 누적감 부재" 가정 불일치 — 다음 audit 재확인 항목으로 큐잉(본 Intent에서 판정 안 함).
- §1 ⑤ 검증 질문의 외부 발송(DM/메일/설문/SNS)은 forbidden/Waiting(approval-needed). 질문 정의가 신규 외부 접촉을 정당화하지 않는다.
