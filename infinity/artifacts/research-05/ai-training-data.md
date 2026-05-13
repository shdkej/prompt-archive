# AI 회사별 모델 학습 데이터 현황 조사

> 작성: 2026-04-23 | Intent: research-05
> 범례: [공개] = 공식 발표/테크리포트 근거, [추정] = 간접 증거/유추

---

## 1. OpenAI (GPT 시리즈)

### 학습 데이터 유형

| 데이터 유형 | 내용 | 근거 |
|------------|------|------|
| 웹 크롤 | CommonCrawl (대규모 웹 스냅샷) | [공개] GPT-3 technical report |
| 책 | Books1, Books2 (수십억 토큰) — 저작권 논란 | [공개] + [공개: 소송] |
| 코드 | GitHub 공개 레포지토리, The Stack | [추정] Codex/Copilot 학습 근거 |
| 백과사전 | Wikipedia (영어 외 다국어) | [공개] GPT-3 report |
| 토론/Q&A | Reddit, Stack Overflow 등 추정 | [추정] |
| RLHF | Scale AI 및 내부 인력의 인간 피드백 | [공개] InstructGPT 논문 |

### 규모 및 특이사항

- GPT-4: 약 **13조 토큰**으로 학습 (유출 정보 기반, 미공식)
- 데이터 구성 세부 사항은 "경쟁 및 안전 이유"로 비공개 (GPT-4 technical report 명시)
- 2023~2024년 다수의 저작권 소송 피소: 저자, 출판사, 뉴욕타임스 등
- Books 데이터 일부 삭제 정황 (피라시 사이트 출처 의혹)

---

## 2. Google (Gemini 시리즈)

### 학습 데이터 유형

| 데이터 유형 | 내용 | 근거 |
|------------|------|------|
| 웹 텍스트 | C4 기반 웹 문서 (~12.5%), 영어/비영어 각 6.5% | [공개] Gemini 3 Pro model card |
| 코드 | GitHub, Stack Overflow, CodeSearchNet, 프로그래밍 튜토리얼 (~12.5%) | [공개] Gemini model card |
| 이미지 | LAION-400M, ImageNet 등 | [공개] Gemini 1.0 report |
| 동영상 | YouTube 등 영상 세그먼트 | [추정] Google 자사 서비스 활용 가능 |
| 오디오 | 음성 + 일반 오디오 | [공개] Gemini 1.0 report |
| 책 | Books3, 위키피디아 | [공개] Gemini 학습 커리큘럼 설명 |

### 규모 및 특이사항

- **멀티모달 네이티브**: 텍스트/이미지/오디오/비디오를 처음부터 통합 학습
- Google 자사 서비스(검색, YouTube, Gmail 등) 데이터 활용 가능 — 다만 공식 확인 제한적
- robots.txt 준수, 중복 제거, CSAM 필터링 등 데이터 품질 프로세스 [공개]
- Gemini 2.5 기준 1M+ 토큰 컨텍스트 — 롱폼 문서 데이터 대규모 학습 추정

---

## 3. Anthropic (Claude 시리즈)

### 학습 데이터 유형

| 데이터 유형 | 내용 | 근거 |
|------------|------|------|
| 웹 데이터 | 공개 웹 문서 (CommonCrawl **미사용** — 자체 수집) | [공개] 일부 보고서 언급 |
| 라이선스 데이터 | 라이선스 취득 데이터셋 포함 | [공개] 개요 수준 언급 |
| 사용자 데이터 | 사용자 상호작용 일부 (비영어 약 10%) | [공개] Claude 통계 자료 |
| RLHF | 인간 피드백 선호도 데이터 (HH-RLHF 공개 배포) | [공개] Hugging Face 배포 |
| Constitutional AI | AI가 생성한 비평으로 반복 정제 (RLAIF) | [공개] CAI 논문 (2022) |

### Constitutional AI (CAI) — 차별화 포인트

- 단순 RLHF 대신 **원칙 기반 자가 비평** 사용
- 원칙 출처: UN 인권 선언, Apple ToS, DeepMind Sparrow Principles, 비서구권 관점 등
- 인간 피드백 의존도 낮추고 안전성/정직성 확보 목표
- 결과: 거절 패턴이 덜 과도하고 맥락 이해 깊음

---

## 4. 학습 데이터 차이가 강점에 미치는 영향

### 코딩 영역

| 회사 | 코딩 데이터 강점 요인 | 코딩 벤치마크 |
|------|---------------------|--------------|
| **Anthropic** | 코드 컨텍스트 이해 깊음, 테스트 케이스 생성 강점, 엣지 케이스 파악 | SWE-bench Verified 1위 (80.9%, Claude Opus 4.x 기준) |
| **OpenAI** | API 문서 대규모 학습, 서드파티 통합에 강점 | SWE-bench Pro 1위 (57.7%), Terminal-Bench 우세 |
| **Google** | 자사 코드 + GitHub + StackOverflow 멀티소스 | Gemini Code Assist 전용 파인튜닝 |

**인사이트**: Anthropic의 코딩 강점은 단순 코드량보다 Constitutional AI로 인한 **정확하고 신중한 추론**에서 기인할 가능성 높음. OpenAI는 **API/통합 코드** 문서 풍부함이 강점.

### 멀티모달 영역

- **Google > OpenAI ≥ Anthropic**: Google은 멀티모달 네이티브 학습으로 이미지·영상·오디오 이해 우세
- YouTube, Google Images 등 자사 자산이 독보적 멀티모달 경쟁력의 원천 [추정]

### 안전성/정직성

- **Anthropic > Google > OpenAI** (일반 평가 기준): CAI 방식이 과도한 거절 없이 원칙 준수
- Anthropic의 비서구권 관점 포함 노력 → 문화적 다양성 있는 응답

### 장문 문서 처리

- **Google > Anthropic ≈ OpenAI**: Gemini 2.5의 1M 토큰 컨텍스트 + 롱폼 학습 데이터

---

## 5. 투명성 비교

| 항목 | OpenAI | Google | Anthropic |
|------|--------|--------|-----------|
| 데이터 소스 공개 수준 | 낮음 (GPT-4 이후 거의 비공개) | 중간 (모델카드 일부 공개) | 낮음~중간 |
| 저작권 이슈 | 다수 소송 피소 | 상대적으로 적음 | 비교적 적음 |
| RLHF 데이터 공개 | 제한적 | 미공개 | HH-RLHF 공개 (Hugging Face) |
| 파인튜닝 데이터 | 비공개 | Vertex AI 문서 일부 | 비공개 |

---

## 6. 불확실한 부분 (추정/미확인)

- OpenAI가 실제로 YouTube 자막이나 Reddit 전체를 사용했는지 → 소송으로 일부 공개 예정
- Google이 Gmail·Docs·검색 쿼리를 훈련에 활용했는지 → 공식 부인, 독립 검증 없음
- Anthropic의 정확한 토큰 수 및 데이터 비율 → 미공개
- GPT-4 이후 모델들의 합성 데이터(Synthetic Data) 비중 → 점차 증가 추세이나 비율 불명확

---

## 참고 자료

- [GPT-4 Technical Report (OpenAI)](https://cdn.openai.com/papers/gpt-4.pdf)
- [Gemini: A Family of Highly Capable Multimodal Models](https://arxiv.org/abs/2312.11805)
- [Constitutional AI: Harmlessness from AI Feedback (Anthropic)](https://arxiv.org/pdf/2204.05862)
- [Anthropic HH-RLHF Dataset (Hugging Face)](https://huggingface.co/datasets/Anthropic/hh-rlhf)
- [Best AI for Coding 2026 (MorphLLM)](https://www.morphllm.com/best-ai-model-for-coding)
- [LLM Leaderboard 2026 (Klu)](https://klu.ai/llm-leaderboard)
