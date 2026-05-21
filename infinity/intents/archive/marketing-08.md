---
id: marketing-08
title: Virtue PMF 응답 분석 루브릭 작성
status: archived
completed_at: 2026-05-21T10:07Z
permission: L1 document creation, L2 normal git push agent-approved
source_note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
artifact: /home/ubuntu/dev/virtue-rebirth-app/docs/pmf-response-analysis-rubric.md
report: /home/ubuntu/.openclaw/workspace/external-repos/prompt-archive/infinity/reports/marketing-08/2026-05-21T10-07.md
---

# Intent 원장: marketing-08 Virtue PMF 응답 분석 루브릭

## Result Summary

Virtue prelaunch PMF 응답을 평균 만족도나 40% 통과/실패로 읽지 않도록, PMF-1~PMF-4 수기 태깅 표와 J1~J4 매핑 규칙을 담은 내부 루브릭을 추가했다. 핵심은 "매우 아쉽다" 응답자의 persona·benefit·대체재 언어를 먼저 분리해 high-expectation customer 후보를 찾고, 작은 표본에서는 숫자 판정을 보류하는 것이다.

## Artifact

- /home/ubuntu/dev/virtue-rebirth-app/docs/pmf-response-analysis-rubric.md

## Source Context

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-impression-positioning-snapshot.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/minimum-viable-audience-brief.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-session-jtbd-matrix.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md

## Success Criteria Mapping

| 기준 | 결과 |
|---|---|
| docs/pmf-response-analysis-rubric.md 1개 추가 | 완료 |
| PMF-1~4 응답 태깅 표 | 문서 §1 |
| J1~J4 매핑 규칙 | 문서 §2 |
| "매우 아쉽다" 그룹 우선 분석 규칙 | 문서 §3 |
| 작은 표본 과대해석 금지선 | 문서 §4 |
| benefit/대체재 언어 추출 | 문서 §5 |
| 외부 발송 approval-needed 경계 | 문서 §6 |

## Verification

- PMF 질문과 J1~J4 정의는 선행 문서에서 계승했고, 선행 문서를 수정하지 않았다.
- 기존 이벤트만 사용했다: deed_saved, deed_judged, level_up_viewed, deed_rerolled.
- 신규 PostHog 이벤트, 코드 변경, 배포, 외부 발송, DM/메일, 공개 모집, 시크릿/권한 변경은 수행하지 않았다.
- copy-spec 금지어는 사용자 노출 카피로 새로 쓰지 않았고, 검증 메타맥락에서만 다루었다.

## Permission Notes

- L1: 내부 문서 추가, Infinity 원장/리포트/상태 업데이트.
- L2: 일반 git push는 PERMISSIONS.md의 자체 승인 조건을 확인한 뒤 agent-approved로 처리했다. force-push, 배포, 비용, 운영 데이터, 시크릿/권한, 타인 메시징 없음.

## Follow-up Candidates

- 실제 사용자 응답이 생기면 별도 Intent로 응답 원문을 수기 태깅한다.
- "매우 아쉽다" 그룹의 반복 benefit 언어가 2명 이상에서 겹칠 때 첫 화면 카피 후보 재작성 Intent를 분리한다. 외부 발송 또는 앱 반영은 별도 승인 후 진행한다.
