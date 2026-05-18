# marketing-03 Intent 원장

- title: Virtue 첫 7일 덕행 루프 정의서 작성
- status: archived
- created: 2026-05-18T22:00Z
- archived: 2026-05-18T22:20Z
- permission: L1 internal planning, with agent-approved L2 push checks
- route: Infinity router -> local Claude Code document execution

## Goal

Virtue 정식 출시 전 첫 7일 재방문 루프를 내부 문서로 정의한다. 구현은 하지 않고, streak로 셀 행동, 첫 1/3/7일 마일스톤 카피, 유연성/실패 처리 원칙, PostHog 확인 후보만 정리한다.

## Result

Virtue 앱 레포에 `docs/seven-day-deed-loop.md`를 추가했다. 핵심 루프는 방문이 아니라 `deed_saved` 중심으로 정의했고, D1/D3/D7 카피 후보, 죄책감 없는 유연성 원칙 2개, 기존 PostHog 이벤트와 신규 후보 이벤트를 분리해 정리했다.

## Artifact

- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/.openclaw/workspace/external-repos/prompt-archive/infinity/artifacts/marketing-03/first-7-day-virtue-loop.md

## Report

- /home/ubuntu/.openclaw/workspace/external-repos/prompt-archive/infinity/reports/marketing-03/2026-05-18T2207Z.md

## Source

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-19-habit-streak-flexibility.md

## Verification

- Virtue README, copy spec, PostHog setup report, and PostHog client/server event files were inspected before drafting.
- The artifact includes a first verification gate confirming no conflict with existing README/copy-spec/PostHog assumptions.
- Changed docs were directly inspected with grep/sed.
- Git status was checked before committing and after pushing.
- Commits pushed:
  - virtue-rebirth-app: `9adb000d87a71aee53de7db3853f86d68d409404`
  - prompt-archive: `a70808429892e57186f7bdcca6174bca1c6c0fa1`

## Next Actions

- If the user wants implementation later, create a separate Intent to choose final D1/D3/D7 copy and add it to the relevant product copy/spec surface.
- Keep external push/email/SMS/reminder work in Waiting until explicitly approved.
