# Intent Archive: research-06

## 기본 정보
- id: research-06
- status: completed → archived
- priority: medium
- permission: L0/L1
- created_at: 2026-05-05T07:44:23Z
- completed_at: 2026-05-05T08:00

## 원문 의도 (Inbox)
"[리서치/스킬화] 바이럴 키워드 추천 스킬 분석자료 만들기 — 사용자가 글을 쓸 때 적절히 바이럴될 만한 키워드를 찾아주는 AgentSkill을 만들 수 있도록, 기존 키워드 추천/트렌드 분석 시스템을 조사·비교하고 스킬 설계 자료로 정리한다."

## 목표
바이럴 키워드 추천 OpenClaw AgentSkill 설계를 위한 분석 자료 + 스킬 설계 초안 작성

## Success Criteria 달성 여부
- [x] 기존 키워드 추천 시스템/도구 5개 이상 사례 분석 (7개 분석 완료)
- [x] 바이럴 가능성 판단 신호 목록 정리 (10종 + 점수 산식)
- [x] OpenClaw AgentSkill 입력/출력 포맷, 도구 흐름, 데이터 소스, 비용 전략 설계
- [x] 실사용 가능한 키워드 추천 결과 템플릿 제안 (블로그용/SNS용)
- [x] 분석 문서 + 스킬 설계 초안 작성 (SKILL.md 초안 포함)

## 결과 요약
- 분석 문서: `infinity/drafts/research-06-viral-keyword-skill.md`
- 기존 도구 7종 비교 분석 (바이럴 적합도 별점 포함)
- 바이럴 신호 10종 + 종합 점수 산식 설계
- OpenClaw AgentSkill 완전한 SKILL.md 초안 (입/출력 스키마, 도구 흐름, 출력 포맷 포함)
- 무료/저비용 vs 프로덕션 데이터 소스 스택 비교
- 캐시 레이어 + LLM 우선 추론 전략 (비용 80%+ 절감)
- 구현 로드맵 5단계 (MVP → v2.5)

## 핵심 인사이트
1. 바이럴의 핵심은 **트렌드 속도(velocity)** — 절대 볼륨보다 상승 모멘텀이 중요
2. Google Trends API (alpha, 2025.07) 가 무료 트렌드 데이터의 최선 선택
3. **MVP는 LLM만으로** 즉시 구현 가능. 외부 API는 v1.0부터 단계적 추가
4. 캐시 TTL 계층화 (24h/6h/3h)로 API 비용 대폭 절감 가능
5. OpenClaw SKILL.md는 YAML frontmatter + Markdown 본문의 단순 구조

## 교훈 (Lessons Learned)
1. 키워드 리서치 도구는 SEO용(경쟁도 중심) vs 바이럴용(속도 중심)으로 목적이 다름 — 혼용 주의
2. 단일 Heartbeat에서 리서치 → 설계 초안까지 완성 가능한 유형
3. LLM 기반 초안 + 외부 API 검증 조합이 비용-품질 최적 균형

## 상세 보고서
infinity/reports/research-06/2026-05-05T0800.md

## 산출물
infinity/drafts/research-06-viral-keyword-skill.md
