# [research-04] AI 모델 학습 데이터 비교 리서치

- id: research-04
- status: archived
- priority: medium
- permission: L0/L1
- created: 2026-04-11
- completed_at: 2026-04-11T12:30
- goal: Google, OpenAI, Anthropic의 AI 모델 학습 데이터를 공개 정보 기준으로 조사하여 정리
- success_criteria:
  - [x] 각 회사별 학습 데이터 유형 정리 (웹, 코드, 책, 라이선스 데이터, 사용자 상호작용, RLHF 등)
  - [x] 학습 데이터 차이가 특정 주제 강점에 미치는 영향 분석
  - [x] 코딩 등 특정 영역에서 어떤 모델이 더 강점을 보일지 추론
  - [x] 불확실한 부분과 공개 근거 명확히 구분
- context: 공개된 논문, 기술 블로그, 발표 자료 기반

## result

- 산출물: `infinity/reports/research-04/2026-04-11T12-30.md`
- 주요 발견:
  1. GPT-3은 Common Crawl 60%, WebText2 22%, Books 16%, Wikipedia 3% 비율로 학습 (가장 상세하게 공개)
  2. GPT-4 이후 OpenAI는 데이터 비율 비공개로 전환, 합성 데이터 대규모 활용
  3. Claude는 Constitutional AI(CAI) + RLHF로 차별화, 사전 학습 데이터 구성 비공개
  4. Gemini는 처음부터 멀티모달 통합 설계 (텍스트+이미지+오디오+비디오)
  5. SWE-bench 기준 코딩 순위: Claude Opus 4.6 (80.8%) > Claude 4 Sonnet (77.2%) > GPT-5 (74.9%) > Gemini 2.5 Pro (73.1%)

## lesson

- 학습 데이터 구성 비율은 점점 비공개화 추세 → 벤치마크 결과로 역추론하는 방법이 현실적
- 합성 데이터(AI-generated)가 학습 데이터의 핵심으로 부상 중 — 실제 인터넷 데이터의 질과 양 한계 극복
- 멀티모달 통합 여부가 장기 경쟁력을 가름할 핵심 변수
- 불확실성 표기를 ✅/⚠️ 방식으로 명시하면 리서치 품질 관리에 효과적
