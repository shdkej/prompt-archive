# marketing-08 · Virtue PMF 응답 분석 루브릭 작성

- id: marketing-08
- status: in_progress
- priority: high
- permission: L1 (내부 문서 작성 only)
- project: virtue-rebirth-app
- created: 2026-05-21T10:10Z
- promoted_to_active: 2026-05-21T10:10Z (Inbox에서 이동)

## Goal

Virtue prelaunch 첫 10명의 PMF 설문 응답을 평균 만족도로 묵히지 않고,
"매우 아쉽다" 응답자의 persona·benefit·대체재 언어를 구조적으로 분리해
high-expectation customer를 찾을 수 있는 분석 루브릭 작성.

## Success Criteria

- [ ] `docs/pmf-response-analysis-rubric.md` 1개 추가 (canonical)
  - PMF-1~4 응답 태깅 표 (J·benefit·대체재·다음 카피 가설)
  - J1~J4 매핑 규칙 (PMF-2~4 응답 → J 추론 단서)
  - "매우 아쉽다" 그룹 우선 분석 규칙
  - 작은 표본 과대해석 금지선
  - 외부 발송 approval-needed 경계
- [ ] `docs/first-impression-positioning-snapshot.md` PMF 질문 원문 수정 없이 계승 확인
- [ ] `docs/minimum-viable-audience-brief.md` J1~J4/MVA 기준 수정 없이 계승 확인
- [ ] copy-spec 금지어 충돌 0건

## Context

- source note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
- refs:
  - virtue-rebirth-app/docs/first-impression-positioning-snapshot.md (PMF-1~4 원문, §4)
  - virtue-rebirth-app/docs/minimum-viable-audience-brief.md (J1~J4 기준, §2)
  - virtue-rebirth-app/docs/copy-spec.md (금지어 명단)
- cloud draft: infinity/artifacts/marketing-08/pmf-response-analysis-rubric.md

## Route

- mode: draft (cloud) → execute_local
- cloud draft: 완료 (2026-05-21T10:10Z)
- local execution: 대기 중 (source note 보완 + 검증 + canonical 저장)

## Next Actions

1. 로컬 Claude Code에 위임: `infinity/artifacts/marketing-08/pmf-response-analysis-rubric.md`의 local 실행 게이트 섹션 참조
2. source note 읽어 내용 보완 후 `docs/pmf-response-analysis-rubric.md`에 canonical 저장
3. rg 검증 게이트 통과 확인
4. 커밋/푸시 후 INTENTS.md Archive 이관
