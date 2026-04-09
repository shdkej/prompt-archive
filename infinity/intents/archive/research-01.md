# research-01: APM 주요 기업 문제 해결 방식 정리

- id: research-01
- status: archived
- priority: medium
- permission: L1
- created: 2026-04-09
- completed_at: 2026-04-09T11:00
- goal: APM 주요 기업들(Datadog, New Relic, AppDynamics, Dynatrace, Elastic APM, Grafana, Honeycomb, Sentry, Splunk Observability, OpenTelemetry)이 어떤 문제를 어떻게 해결했는지 정리. 기업별 핵심 문제 / 기존 방식의 한계 / 해결 방식 / 결과 / 지금 배울 포인트 문서화. 마지막에 공통 패턴 3~5개 도출.
- success_criteria:
  - 10개 기업/프로젝트 각각 분석 완료 ✅
  - 기업별 5가지 항목(핵심 문제, 기존 방식 한계, 해결 방식, 결과, 배울 포인트) 작성 ✅
  - 공통 패턴 5개 정리 ✅
  - infinity/drafts/apm-companies-research.md 파일로 저장 ✅

## result

모든 성공 기준 충족. 10개 기업/프로젝트를 각 5개 항목으로 분석하고, 공통 패턴 5개 도출.

- 산출물: `infinity/drafts/apm-companies-research.md`
- 분석 대상: Datadog, New Relic, AppDynamics, Dynatrace, Elastic APM, Grafana, Honeycomb, Sentry, Splunk Observability, OpenTelemetry
- 공통 패턴:
  1. 사일로 → 통합 플랫폼
  2. 운영자 중심 → 개발자 중심 (PLG)
  3. 사후 대응 → 사전 예방 + AI 자동화
  4. 벤더 종속 → 오픈소스 표준화
  5. 메트릭 중심 → 풍부한 컨텍스트

## lesson

- APM 시장은 "단순 모니터링 → 통합 관찰가능성 플랫폼"으로 수렴 중
- 오픈소스 표준(OpenTelemetry, Grafana)이 벤더 종속을 해소하는 방향
- 개발자 경험(DX) 우선 + 오픈소스 신뢰 구축 → 기업 판매 연결이 검증된 GTM 전략
- AI를 통한 알림 피로 해소가 엔터프라이즈 세일즈 핵심 포인트
