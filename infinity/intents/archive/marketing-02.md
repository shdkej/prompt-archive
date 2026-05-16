# marketing-02 · Virtue /add 활성화 마찰 감사

- id: marketing-02
- status: archived
- priority: high
- permission: L0/L1
- project: virtue-rebirth-app
- created: 2026-05-16T13:30Z (inbox)
- promoted_to_active: 2026-05-16T14:00Z
- completed_at: 2026-05-16T14:00Z

## Goal

/add 방문자가 deed_judge_attempted 전에 이탈하는 마찰점 식별 +
UX/텔레메트리 개선 후보 초안 작성.

## Result Summary

PostHog 신호(deed_judged=1, deed_saved=0) 기반으로 핵심 갭 특정 완료.
마찰점 4개 식별, 개선 후보 3개 초안 작성.

- 핵심 원인: 채점 완료 후 저장 CTA 미완료 (저장 버튼 가시성 부족)
- 부가 원인: 퍼널 이벤트 부재 (add_flow_started, deed_judge_attempted, add_flow_abandoned 미구현)
- 부가 원인: mock 배지 노출로 결과 신뢰도 저하

## Artifacts

- `infinity/artifacts/marketing-02/activation-friction-audit.md`
  - 마찰점 분석 (P0~P3)
  - 개선 후보 3개 (저장 버튼 개선 / 이벤트 3종 추가 / 배지 교체)
  - 로컬 실행 프롬프트

## Reports

- `infinity/reports/marketing-02/2026-05-16T14-00.md` — heartbeat 실행 로그

## Next Actions

1. 사용자 확인 후 로컬 Claude Code 위임:
   - `infinity/artifacts/marketing-02/activation-friction-audit.md` §5 실행 프롬프트 사용
   - 예상 소요: 1시간
2. 7일 후 PostHog 점검: deed_saved ≥ 1 → marketing-03 트리거
3. marketing-03: AI 채점 모드 전환 (ANTHROPIC_API_KEY 설정) 검토
