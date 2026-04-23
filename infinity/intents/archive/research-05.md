# research-05: AI 모델 학습 데이터 비교 리서치

## 2026-04-18 처리 (1차)

- status: archived
- priority: medium
- permission: L0
- completed_at: 2026-04-18T06:13
- goal: Google, OpenAI, Anthropic 각사의 AI 모델 학습 데이터 유형 비교 분석 문서 작성
- context: infinity/drafts/ai-training-data-research.md

### Result
- 각 회사별 학습 데이터 유형 정리 완료
- 공개 근거와 추정 명확히 구분
- 코딩 포함 도메인별 강점 추론 완료
- 산출물: infinity/drafts/ai-training-data-research.md

### Lesson
- 세 회사 모두 학습 데이터 구성을 대부분 비공개로 유지하므로, 논문/모델 카드가 주요 공개 근거
- SWE-bench 같은 벤치마크가 실제 데이터 차이를 간접적으로 반영
- Anthropic의 CAI는 합성 데이터를 대규모로 활용한 최초 사례로 독보적

---

## 2026-04-21 처리 (2차 - Inbox 재요청)

- status: completed
- priority: medium
- permission: L0
- completed_at: 2026-04-21T00:00
- goal: Google, OpenAI, Anthropic의 AI 모델 학습 데이터를 공개 정보 기준으로 조사하고 비교 분석 문서 작성
- success_criteria:
  - 각 회사별 학습 데이터 유형(웹, 코드, 책, 라이선스 데이터, 사용자 상호작용, RLHF 등) 정리
  - 학습 데이터 차이가 특정 주제 강점에 미치는 영향 분석
  - 코딩 등 주제별 강점 추론 포함
  - 확인된 사실과 추정을 명확히 구분하여 작성
- context: infinity/drafts/research-05-ai-training-data.md
- project: research

### Result
- infinity/drafts/research-05-ai-training-data.md 작성 완료
- 3사 학습 데이터 유형 비교, 도메인별 강점 분석, 확인 사실/추정 구분 포함
- 벤치마크 수치(HumanEval, MMLU, MGSM) 포함한 상세 비교

### Lesson
- 공개 기술 보고서와 벤치마크 데이터가 충분히 존재하여 단일 Heartbeat에서 완료 가능한 리서치 유형
- 향후 유사 AI 리서치 Intent도 L0/단일 Heartbeat로 계획 가능

---

## 2026-04-23 처리 (3차 - main 브랜치 Inbox 재처리)

- status: archived
- priority: medium
- permission: L0
- completed_at: 2026-04-23T10:00
- note: local main이 origin/main보다 뒤처진 상태에서 Inbox 항목을 재처리. 새 웹 리서치로 2026년 최신 벤치마크 데이터 반영.
- context: infinity/drafts/research-05/ai-training-data.md

### Result
- infinity/drafts/research-05/ai-training-data.md 작성 완료 (2026년 기준 최신 벤치마크 반영)
- 회사별 학습 데이터 비교표, 코딩/멀티모달/안전성/장문처리 강점 분석, 투명성 비교 포함
- 공개 근거 vs 추정 명확히 구분

### Lesson
- local main이 origin/main을 따라가지 못하면 Inbox가 이전 상태로 보여 중복 처리 발생
- Heartbeat 시작 시 반드시 `git fetch && git status` 선행 필요
- 중복 처리는 최신 데이터로 문서 보완 효과가 있으므로 완전한 낭비는 아님
