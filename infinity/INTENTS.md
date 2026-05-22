# Intent Registry

> Heartbeat Agent가 주기적으로 읽고 실행하는 의도 목록.

## Inbox

## Active

## Waiting

<!-- 사용자 결정, 외부 조건, 안전 확인 대기. 같은 질문을 반복하지 않고 상태만 보존한다. -->

### marketing-10 Virtue Time-to-Value 관찰 기준표 작성

- id: marketing-10
- title: Virtue Time-to-Value 관찰 기준표 작성
- status: waiting
- priority: medium
- permission: L1 (내부 문서 작성. 외부발송/대시보드/프로덕션 tracking 변경은 Waiting)
- mode: execute_local (클라우드 단계 완료)
- created_at: 2026-05-22T10:00Z
- waiting_since: 2026-05-22T10:30Z
- wait_reason: 로컬 환경 필요 — virtue-rebirth-app/docs/에 파일 생성 후 커밋/푸시. 클라우드 환경에서는 push 불가(SSH/token 미설정). 로컬에서 아래 execute_local 프롬프트 실행 필요.
- goal: J1-J4별 first value · second value · time gap 계산 방식 · 정성 확인 질문 · prelaunch 해석 금지선을 표로 정리한 내부 기획 문서 작성
- success_criteria: docs/time-to-value-observation-brief.md에 J1-J4별 first/second value 이벤트·time gap 계산·정성 질문·해석 금지선 표 포함. 신규 이벤트/코드/외부발송/비용 0. activation-milestone-ladder 및 first-session-jtbd-matrix 충돌 0.
- context:
  - source: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-22-time-to-value-second-value.md
  - prior: activation-milestone-ladder.md, first-session-jtbd-matrix.md
  - events: add_flow_started, deed_judged, deed_saved, level_up_viewed
- cloud_draft: infinity/artifacts/marketing-10/time-to-value-observation-brief.md
- execute_local_prompt: |
    Infinity Intent: marketing-10 Virtue Time-to-Value 관찰 기준표 작성
    Mode: execute_local
    Goal: virtue-rebirth-app/docs/time-to-value-observation-brief.md 생성 후 커밋/푸시
    Cloud draft: prompt-archive/infinity/artifacts/marketing-10/time-to-value-observation-brief.md
    Allowed: L0/L1 only (docs 파일 추가, 커밋, 푸시)
    Forbidden: 신규 이벤트/코드/대시보드/외부발송/비용
    Verification:
      rg -n "deed_judged|deed_saved|add_flow_started|level_up_viewed" docs/time-to-value-observation-brief.md
      grep -v "time-to-value-observation-brief" docs/ — 기존 파일 수정 없음 확인
    Report back to: prompt-archive/infinity/reports/marketing-10/{timestamp}.md

## Archive

<!-- marketing-09 completed 2026-05-21T22:07Z → infinity/intents/archive/marketing-09.md (Virtue 활성화 마일스톤 사다리: 활성화를 setup→aha→habit 사다리로 재정의, J1~J4를 setup/aha/habit moment·기존 이벤트·해석 주의·prelaunch 판정 보류 6칸으로 매핑. setup=add_flow_started(진입=의도), aha=deed_saved(J1/J2/J4)·deed_judged(J3 저장 전·독립), habit=반복 deed_saved(distinct-day 계산형)+level_up_viewed. deed_save_capped early-return 코드 사실 반영. prelaunch 단계 도달률은 성패 아닌 관찰 기준(전환율 판정·judged−saved 갭 이탈 단정·40% 임계값 금지). 선행 4문서(jtbd-matrix/seven-day-loop/pmf-rubric/mva-brief) 매핑 계승, 신규 이벤트·속성·카피·코드·대시보드·외부발송 0. workflow-master 4역할 병렬 후 통합. grep 게이트 55매치 PASS, copy-spec 금지어 충돌 0건; docs/activation-milestone-ladder.md 추가) -->

<!-- marketing-01 completed 2026-05-21T10:17Z → infinity/intents/archive/marketing-01.md (Virtue add-flow telemetry 승인 처리: `marketing-01-add-flow-telemetry` b28d01f를 master에 fast-forward 머지/push, Kubernetes `deployment/virtue-rebirth` rollout restart 완료. GitHub master와 배포 pod HEAD 모두 b28d01f, 라이브 HTTP 200, `641`/`MOCK` 미노출, 빈 상태 카피 렌더 확인. 후속은 7일 PostHog `add_flow_started` 대비 `add_flow_abandoned`/`deed_saved` 점검) -->

<!-- marketing-08 completed 2026-05-21T10:07Z → infinity/intents/archive/marketing-08.md (Virtue PMF 응답 분석 루브릭: PMF-1~4 수기 태깅 표, J1~J4 benefit/대체재/다음 카피 가설 매핑, "매우 아쉽다" 그룹 우선 분석, 작은 표본 40% 과대해석 금지선, 기존 이벤트만 사용(deed_saved/deed_judged/level_up_viewed/deed_rerolled), 외부 설문·DM·공개 모집·PostHog·코드·배포는 Waiting 경계; docs/pmf-response-analysis-rubric.md 추가) -->

<!-- marketing-07 completed 2026-05-20T22:07Z → infinity/intents/archive/marketing-07.md (Virtue 최소 생존 오디언스 기준표: J1~J4 잡을 그대로 계승해 첫 10명 후보 조건·첫 문장/약속·첫 세션 가치 순간·관찰 질문·승인 필요 외부 액션 경계 6칸으로 매핑, 컬럼별 Planner/Marketer/Developer/Operator 렌즈. Seth Godin 밀도>규모 + Paul Graham do-things-that-dont-scale 학습 루프, "문안까지 L1·발송부터 Waiting" 경계 명시. 활성화 이벤트 계승(J1/J2/J4=deed_saved, J3=deed_judged) 신규 0. copy-spec/first-session-jtbd-matrix 충돌 0건; docs/minimum-viable-audience-brief.md 추가) -->

<!-- marketing-06 completed 2026-05-20T10:07Z → infinity/intents/archive/marketing-06.md (Virtue 첫 세션 JTBD 매트릭스: J1 기록형/J2 누적형/J3 AI 호기심형/J4 회고형 4잡을 첫 화면 약속·첫 행동·성공 지표·마찰 위험·근거 문서 5칸으로 매핑, J3=deed_judged·나머지=deed_saved 활성화, good/bad 마찰 구분, 기존 6 이벤트 재사용·신규 0, 선행 3문서+copy-spec 충돌 0건; docs/first-session-jtbd-matrix.md sha 38af1be) -->

<!-- marketing-05 completed 2026-05-19T22:07Z → infinity/intents/archive/marketing-05.md (Virtue 빈 상태/첫 행동 감사표: ES-1~ES-6 다섯 칸 표, 대시보드 최근 덕행 카드 내부 CTA 후보 A/B + 라벨 3종, 톤 위험 T1–T5, 계측 후보 3종 정의, copy-spec 금지선 충돌 0건) -->

<!-- marketing-04 completed 2026-05-19T10:07Z → infinity/intents/archive/marketing-04.md (Virtue 첫인상 포지셔닝 스냅샷: 3가설 A/B/C, 첫인상 리스크 R1–R4, PMF 질문 4개, 헤드라인 후보 3개, copy-spec 금지선 충돌 0건) -->

<!-- marketing-03 completed 2026-05-18T22:20Z → infinity/intents/archive/marketing-03.md (Virtue 첫 7일 deed_saved 루프 정의서 작성, D1/D3/D7 카피·유연성 원칙·PostHog 후보 정리) -->

<!-- marketing-02 completed 2026-05-16T14:00Z → infinity/intents/archive/marketing-02.md (마찰점 4개 특정, 개선 후보 3개 초안, 로컬 실행 프롬프트 작성) -->

<!-- research-07 completed 2026-05-13T12:00 → infinity/intents/archive/research-07.md -->

<!-- product-01 completed 2026-05-15T11:44Z → infinity/intents/archive/product-01.md (Virtue 최신 상태, 후속 개선은 별도 Intent로 분리) -->

<!-- build-02 completed 2026-05-13 → infinity/intents/archive/build-02.md (https://infinity.oracle.shdkej.com 배포 완료) -->

<!-- research-06 completed 2026-05-05T08:00 → infinity/intents/archive/research-06.md -->

<!-- wiki-05 completed 2026-04-25T09:00 → infinity/intents/archive/wiki-05.md -->

<!-- wiki-04 completed 2026-04-25T10:15 → infinity/intents/archive/wiki-04.md -->

<!-- wiki-02 completed 2026-04-19T02:45 → infinity/intents/archive/wiki-02.md -->
<!-- wiki-03 completed 2026-04-20T13:30 → infinity/intents/archive/wiki-03.md -->
<!-- research-05 completed 2026-04-21T00:00 → infinity/intents/archive/research-05.md -->
<!-- wiki-01 completed 2026-04-21T00:00 → infinity/intents/archive/wiki-01.md -->
<!-- build-01 completed 2026-04-21T00:30 → infinity/intents/archive/build-01.md -->
<!-- research-05 re-run completed 2026-04-23T10:00 → infinity/intents/archive/research-05.md (3차) -->
