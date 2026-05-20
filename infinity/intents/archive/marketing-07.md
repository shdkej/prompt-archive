# marketing-07 Intent 원장

- id: marketing-07
- title: Virtue 최소 생존 오디언스 기준표 작성
- status: archived
- created_at: 2026-05-20T22:00Z
- completed_at: 2026-05-20T22:07Z
- mode: execute_local (local Claude Code)
- route: Infinity router → local Claude Code (workflow-master 분류: 단일 내부 기획 문서 1장, 지배 역할 Marketer, 4역할 관점은 표 6컬럼에 압축, 작성은 marketer 서브에이전트 위임 / 검증은 master 레인 분리)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repos
- result_summary: Virtue 정식 출시 전 "처음 보여줄 10명"을 좁히는 단일 내부 MVA 기준표를 추가했다. `first-session-jtbd-matrix.md`의 J1 기록형·J2 누적형·J3 AI 호기심형·J4 회고형을 그대로 계승하고, 각 잡을 `첫 10명 후보 조건 → 첫 문장/약속 → 첫 세션 가치 순간 → 관찰 질문 → 승인 필요 외부 액션 경계` 6컬럼으로 매핑했다(각 컬럼에 Planner/Marketer/Developer/Operator 렌즈 명시). source note의 4개 오디언스 후보(감사·사진일기 이탈자/라이프 RPG 취향/AI 코멘트 호기심/개인 로그 수집형)를 4잡에 자연 연결. 활성화 이벤트는 기존 정의 계승(J1/J2/J4=`deed_saved`, J3=`deed_judged`, J2 부가=`level_up_viewed`)으로 신규 0. Seth Godin MVA(밀도>규모) + Paul Graham "do things that don't scale"(콘시어지 학습 루프) 원칙과 "문안 작성까지 L1, 보내는 순간부터 Waiting" 외부 액션 경계를 못박았다. `first-session-jtbd-matrix.md`/`copy-spec.md` 충돌 0건. 외부 발송·트래킹·코드·배포·시크릿·권한·공개 액션 0건.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/minimum-viable-audience-brief.md
  role: canonical
  note: Virtue 앱 레포 내 정식 산출물. JTBD 4잡 × MVA 6컬럼 기준표. "첫 문장/약속"은 수동 초대 후보 카피 초안일 뿐 앱 미반영. 최종본과 충돌 시 canonical 우선.
- path: infinity/artifacts/marketing-07/minimum-viable-audience-brief.md
  role: cloud-draft
  note: cloud prepare 단계 초안(`88bdfef`). 본문에 "최종본과 충돌 시 canonical 우선" 명시. canonical과 매핑 동일. 로컬 실행이 source note 직접 정독 + copy-spec 검증을 거쳐 canonical로 확정.

## Reports

- path: infinity/reports/marketing-07/2026-05-20T2207Z.md
  role: final (execute_local)
  note: 로컬 실행 1회 로그. workflow-master 분류, 위임 결정, L2 체크리스트, 검증 게이트 결과, 커밋/푸시 정책.
- path: infinity/reports/marketing-07/2026-05-20T2300Z.md
  role: prepare (cloud)
  note: cloud draft 단계 로그(`88bdfef`).

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-20-minimum-viable-audience.md (Seth Godin MVA + Paul Graham do-things-that-dont-scale)
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md (J1~J4 잡 정의 단일 출처, 계승)
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md (금지어 명단)

## Success criteria coverage

| 성공 기준 | 충족 위치 |
|---|---|
| 1. JTBD 4잡 표 + 첫 10명 후보 조건 | brief §1 (J1~J4 행 + `첫 10명 후보 조건` 컬럼) |
| 2. 첫 문장/약속 컬럼 | brief §1 (잡별 후보 카피 4개) |
| 3. 첫 세션 가치 순간 컬럼 | brief §1 (`deed_saved`/`deed_judged` 매핑) |
| 4. 관찰 질문 컬럼 | brief §1 (잡별 1~2개) |
| 5. 승인 필요 외부 액션 경계 컬럼 + 종합 표 | brief §1 컬럼 6 + §3 표 |
| 6. copy-spec / first-session-jtbd-matrix 충돌 0건 | brief §4 (no-conflict 표) + 본 ledger Verification |

## Verification

- 필수 리터럴 14종 존재(rg): `J1 기록형`/`J2 누적형`/`J3 AI 호기심형`/`J4 회고형`, `deed_saved`/`deed_judged`/`level_up_viewed`, 6컬럼명, `Out of scope`, `do things that don't scale`.
- 6컬럼 헤더 1행 확인. 활성화 이벤트 매핑이 `first-session-jtbd-matrix.md` §2~§3과 일치.
- copy-spec 금지어는 §4 no-conflict 메타맥락 1곳(line 68)만 등장, 후보 카피 4개에는 0건.
- `git diff --check` 공백 오류 0. virtue-rebirth-app 변경은 `docs/minimum-viable-audience-brief.md` 1개뿐.
- 작업 전 양 레포 clean → unrelated dirty 파일 없음, 건드린 것 없음.

## Commits

- repo: virtue-rebirth-app
  note: `docs/minimum-viable-audience-brief.md` 추가. `origin/master`에 normal push. sha는 caller 최종 응답에 기록.
- repo: prompt-archive
  note: report + 본 ledger + INTENTS.md Inbox→Archive 단일 커밋. `origin/main`에 ff-only normal push. sha는 caller 최종 응답에 기록.

## URLs

- 외부 URL 게시 없음. 모든 변경은 내부 문서 및 사내 레포(virtue-rebirth-app, prompt-archive) 한정.

## Next Actions

- 수동 첫 세션 관찰 스크립트 초안(15분 흐름 + 질문 5개) → 별도 Intent (외부 발송 없음, L1).
- 외부 초대 승인 요청 템플릿(실발송 없이 승인 조건·리스크만 분리) → 별도 Intent (Waiting 후보).
- 실 사용자 신호 확보 후 첫 10명 후보 조건 → 실제 세그먼트 확정 → 별도 Intent (트래킹 승인 필요).
