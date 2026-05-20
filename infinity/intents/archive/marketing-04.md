# marketing-04 Intent 원장

- id: marketing-04
- title: Virtue 첫인상 포지셔닝 스냅샷 작성
- status: archived
- created_at: 2026-05-19T10:00Z
- completed_at: 2026-05-19T10:07Z
- mode: execute_local
- route: Infinity router → local Claude Code (workflow-master classification: 단일 스냅샷 문서 + Infinity 기록, 4역할 관점 문서 내부 임베드)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repos
- result_summary: Virtue 첫 화면·README·copy-spec·seven-day-deed-loop를 검수해 3개 포지셔닝 가설(A 자기관찰 게임 / B 라이프 RPG / C AI 셀프 거울), NN/g 첫인상 리스크 R1–R4, Sean Ellis/Superhuman 식 PMF 질문 4개 초안, 가설별 헤드라인·보조문구 후보 3개를 한 문서로 정리했다. 카피-스펙 금지선 충돌 0건, 외부 발송/배포/트래킹/생산/시크릿/권한/공개 액션 0건임을 §6.1/§6.3에서 명시했다.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/first-impression-positioning-snapshot.md
  role: design
  note: Virtue 앱 레포 내 정식 산출물(첫인상 포지셔닝 스냅샷). 카피 변경 지시서가 아니며 가설·질문·후보 까지만 둠.
- path: infinity/artifacts/marketing-04/first-impression-positioning-snapshot.md
  role: design
  note: Virtue 레포 산출물의 Infinity 미러. 외부 도구가 prompt-archive 만 읽고도 동일 스냅샷을 그대로 활용할 수 있게 둠.

## Reports

- path: infinity/reports/marketing-04/2026-05-19T1007Z.md
  role: final
  note: 본 실행 1회의 로그. workflow-master 분류, L2 체크리스트, 검증 단계, 커밋/푸시 SHA 기록.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-19-prelaunch-positioning-pmf.md
- /home/ubuntu/dev/virtue-rebirth-app/README.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/lib/greeting.ts
- /home/ubuntu/.openclaw/workspace/external-repos/prompt-archive/infinity/intents/archive/marketing-03.md

## Success criteria coverage

| 성공 기준 | 충족 위치 |
|---|---|
| 3 포지셔닝 가설 | snapshot §2 (A/B/C + 비교 표) |
| 첫인상 리스크 | snapshot §3 (R1–R4 + 요약) |
| PMF 질문 4개 초안 | snapshot §4 (PMF-1 ~ PMF-4) |
| 헤드라인/보조문구 후보 3개 | snapshot §5 (후보 1/2/3 + 비교 표) |
| copy-spec 금지선과 충돌 없음 | snapshot §6.1 |
| 외부 발송/배포/트래킹 변경 없음 | snapshot §6.3 (+ 본 ledger 아래 진술) |
| Out of scope 명시 | snapshot §7 |

## Verification

- README, copy-spec, seven-day-deed-loop, 대시보드 `src/app/page.tsx`, `src/lib/greeting.ts`를 작성 전에 직접 읽었다.
- 작성된 snapshot 문서 본문을 grep으로 직접 점검(필수 섹션 헤더 §2/§3/§4/§5/§6.1/§6.3 존재 및 카피-스펙 금지선 텍스트 일치 확인).
- 본 Intent로 코드/배포/시크릿/권한/트래킹/공개 액션은 한 건도 수행하지 않았다. git push는 사내 내부 리포(`virtue-rebirth-app`, `prompt-archive`)로 한정했고, L2 체크리스트는 report 본문에 기록.

## Commits

- repo: virtue-rebirth-app
  sha: 1145a9dd465be3b2fd62a89ba8ec6a910a62b297
  note: docs/first-impression-positioning-snapshot.md 추가
- repo: prompt-archive
  sha: c417242
  note: infinity/artifacts/marketing-04/ + report + archive ledger + INTENTS 업데이트. 후속 bookkeeping: d5cafd8, 44e863c.

## URLs

- 외부 URL 게시 없음. 모든 변경은 내부 문서 및 사내 리포 한정.

## Next Actions

- 헤드라인 후보 1을 첫 화면 Greeting 폴백 한 줄 후보로 카피-스펙에 정식 등재 (Marketer + Planner 합의 후, 별도 Intent).
- 코어 경험 사용자가 임계치(`deed_saved` ≥ 1 사용자 N명) 도달 시 PMF-1 내부 폼 초안 의도 분리 — 외부 발송은 별도 승인 전까지 Waiting.
- 후보 1/3 A/B 가능 시점에 첫 세션 성공률(기존 `deed_saved`/`add_flow_started` + candidate `first_session_deed_saved`)을 가설별로 본다 — 별도 Intent.
