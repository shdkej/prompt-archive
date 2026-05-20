# marketing-06 Intent 원장

- id: marketing-06
- title: Virtue 첫 세션 JTBD 매트릭스 작성
- status: archived
- created_at: 2026-05-20T10:00Z
- completed_at: 2026-05-20T10:07Z
- mode: draft (cloud) → execute_local (local Claude Code)
- route: Infinity router → local Claude Code (workflow-master classification: 단일 내부 기획 문서 1장, 단일 역할 Marketer 지배, 4역할 관점은 매트릭스 컬럼에 압축, 문서 작성은 marketer 서브에이전트 위임)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repos
- result_summary: Virtue 첫 세션 JTBD를 한 장의 매트릭스로 정리한 단일 내부 문서를 추가했다. source note의 4개 후보 진술을 그대로 채택해 J1 기록형·J2 누적형·J3 AI 호기심형·J4 회고형으로 정의하고, 각 잡을 `첫 화면 약속 → 첫 행동 → 성공/활성화 지표 후보 → 마찰 위험(good/bad) → 현재 근거 문서` 5칸으로 매핑했다. 지표는 기존 PostHog 이벤트 6종(`deed_judge_attempted`/`deed_judged`/`deed_rerolled`/`deed_save_capped`/`deed_saved`/`level_up_viewed`)만 재사용하며 신규 이벤트 0. J3에 한해 `deed_judged`를 가치 순간으로 보고, J1/J2/J4는 `deed_saved`를 활성화로 본다. good/bad 마찰 구분 원칙(같은 마찰이 잡에 따라 부호가 뒤집힘)과 `job_hint` 속성 보류를 명시. `first-impression-positioning-snapshot.md`/`empty-state-first-action-audit.md`/`seven-day-deed-loop.md`/`copy-spec.md` 충돌 0건. 외부 발송·배포·트래킹·코드·시크릿·권한·공개 액션 0건.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
  role: canonical
  note: Virtue 앱 레포 내 정식 산출물. caller 명시 파일명 채택(cloud draft의 `jtbd-first-session-matrix.md`와 어순만 다름). 카피 변경 지시서가 아니라 가설 매트릭스.
- path: infinity/artifacts/marketing-06/jtbd-first-session-matrix.md
  role: cloud-draft
  note: cloud prepare 단계 초안(`ba148f5`). 본문에 "최종본과 충돌 시 canonical 우선" 명시. canonical과 매핑은 동일, J4 정의만 다름(draft: 부담 없는 자기 인식 / canonical: 회고형 개인 로그 — source note 원문 4후보 충실).

## Reports

- path: infinity/reports/marketing-06/2026-05-20T1007Z.md
  role: final (execute_local)
  note: 로컬 실행 1회 로그. workflow-master 분류, 위임 결정, L2 체크리스트, rg 게이트 결과, 커밋/푸시 정책.
- path: infinity/reports/marketing-06/2026-05-20T1010Z.md
  role: prepare (cloud)
  note: cloud draft 단계 로그.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-20-jtbd-onboarding-segmentation.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-impression-positioning-snapshot.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/empty-state-first-action-audit.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/app/add/page.tsx

## Success criteria coverage

| 성공 기준 | 충족 위치 |
|---|---|
| 1. job 후보 3-4개 표 정의 | matrix §1 (J1~J4 표) |
| 2. 잡별 5칸 매핑(첫 화면 약속/첫 행동/성공 지표/마찰 위험/근거 문서) | matrix §2 (4-Job 매트릭스 표) |
| 3. 선행 3문서 충돌 0건 | matrix §6 (no-conflict 표) + 본 ledger Verification |
| 4. 외부 발송·트래킹·코드 변경 0건 명시 | matrix "Out of scope" + matrix §5 측정 후보 + §6 |

## Verification

- 필수 리터럴 7종 존재 확인(rg): `J1 기록형`, `J2 누적형`, `J3 AI 호기심형`, `J4 회고형`, `deed_saved`, `deed_judged`, `Out of scope`.
- `git diff --check` 공백 오류 0건. virtue-rebirth-app 변경 파일은 `docs/first-session-jtbd-matrix.md` 1개뿐, 코드/트래킹 0건.
- 실제 코드(`src/app/add/page.tsx`)에서 6개 이벤트 발화 확인 → 매트릭스 지표 후보가 기존 이벤트 재사용에 한정됨을 코드로 검증.
- copy-spec 금지어 명단은 matrix §6 메타 설명 1회만 등장, 사용자 카피 본문에는 0건.

## Commits

- repo: virtue-rebirth-app
  sha: 38af1be
  note: `docs/first-session-jtbd-matrix.md` 추가. `ca2e007..38af1be` origin/master push 완료.
- repo: prompt-archive
  content+bookkeeping: 단일 커밋 (report + 본 ledger + INTENTS.md Active→Archive). 원격 `ba148f5` 위로 ff-only pull 후 push. sha는 최종 caller 응답에 기록.

## URLs

- 외부 URL 게시 없음. 모든 변경은 내부 문서 및 사내 리포(virtue-rebirth-app, prompt-archive) 한정.

## Next Actions

- J3: 첫 화면에 AI 신호 노출 여부 결정 → 별도 Intent (R3 고려).
- J2: 첫 세션 `count===0` 누적감 공백 보강 → 별도 Intent.
- 실 사용자 확보 후 J1~J4 → 인터뷰/PMF 질문/`job_hint` 속성 후보 분해 → 별도 Intent (트래킹 승인 필요).
