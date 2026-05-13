# AI 모델 학습 데이터 비교 분석

> 작성일: 2026-04-21 | Intent: research-05
> 공개 정보 기준. 확인된 사실(✅)과 추정(⚠️)을 명확히 구분.

---

## I. 각 회사별 학습 데이터 유형

### OpenAI (GPT-3 / GPT-4)

#### GPT-3 학습 데이터 구성 ✅ (공식 논문)
| 데이터 소스 | 비율 | 토큰 수 |
|------------|------|---------|
| Common Crawl | 60% | 410억 |
| WebText2 (Reddit 큐레이션) | 22% | 190억 |
| Books1 | 8% | 120억 |
| Books2 | 8% | 550억 |
| Wikipedia | 3% | - |

- 전체 데이터: 2016~2019년 수집, 압축 후 570GB
- 언어: 영어 93%, 프랑스어 1.8%, 독일어 1.5% 등

#### GPT-4 학습 데이터 ⚠️ (비공개, 부분 추정)
- 공개 인터넷 데이터 + 제3자 라이선스 데이터 조합
- 기술 보고서에서 경쟁·안전 이유로 구체적 구성 미공개

#### 피드백 데이터 (InstructGPT/ChatGPT) ✅
- OpenAI API 사용자 제출 프롬프트
- 인간 라벨러의 응답 시연 데이터
- 모델 출력 순위 데이터 (Human Preference Ranking)
- 6B 파라미터 리워드 모델 사용

---

### Google (PaLM / Gemini)

#### PaLM 학습 데이터 ✅
- 필터링된 웹페이지, Wikipedia, 뉴스 기사
- GitHub 오픈 소스 소스코드
- LaMDA 학습 데이터셋 기반

#### PaLM 2 추가 ✅
- 과학 논문
- 수학 표현이 포함된 웹페이지 (수학 성능 강화 목적 명시)

#### Gemini 학습 데이터 ✅ (기술 보고서)
- 웹 문서 (robots.txt 준수), 오픈 소스 코드
- 상업적 라이선스 계약 데이터
- Google 직원 생성 데이터
- **멀티모달**: 이미지, 오디오(음성), 비디오, 문서
- Google 제품/서비스 사용자 데이터 (이용약관 준수)

---

### Anthropic (Claude)

#### 사전 학습 데이터 ✅
- 2023년 8월 이전 공개 인터넷 데이터
- 라이선스 데이터 + 내부 생성 합성 데이터
- 사용자 제출 프롬프트/출력 **제외** (명시)
- robots.txt 준수 크롤링

#### Constitutional AI (CAI) ✅ (공식 연구 논문)
- UN 세계 인권 선언 등에서 영감받은 "헌법" 사용
- **합성 데이터 생성 과정**:
  1. 모델 샘플링 → 자기 비판 생성 → 개선된 응답으로 미세 조정
  2. RLAIF(RL from AI Feedback): 인간 대신 AI 선호도 평가 사용
- 다양한 언어 번역 + 탈옥 패턴 스타일 변환으로 강건성 확보

---

## II. 데이터 차이가 모델 강점에 미치는 영향

### 코딩 / 프로그래밍

| 모델 | HumanEval | 원인 |
|------|-----------|------|
| GPT (최신) | 93.1% ✅ | Common Crawl 내 방대한 코드, 기술 문서 |
| Claude Opus | 90.4% ✅ | 대규모 공개 인터넷 수집 |
| Gemini Flash | 71.5% ✅ | GitHub 라이선스 제약으로 코드 데이터 상대적 제한 |

### 수학

| 모델 | MGSM | 원인 |
|------|------|------|
| GPT-4o mini | 87.0% ✅ | 고도 필터링 + 기술 콘텐츠 우선 |
| Gemini Flash | 75.5% ✅ | PaLM 2부터 과학 논문·수학 표현 명시 포함 |
| Claude Haiku | 71.7% ✅ | - |

### 일반 지식 (MMLU)

| 모델 | MMLU | 비고 |
|------|------|------|
| Claude Opus 4.6 | 92.1% ✅ | Constitutional AI의 정확성 강조 |
| GPT-5.4 | 91.8% ✅ | Books + Common Crawl 조합 |
| Gemini 3.1 Ultra | 90.4% ✅ | 멀티모달 지식 포함 |

### 멀티모달 (Vision / Audio / Video)

- **Google Gemini**: 절대 우위 ✅
  - 기본 아키텍처부터 멀티모달 (원래 설계)
  - 각 Transformer 레이어에서 크로스모달 Attention
  - Gemini Embedding 2: 텍스트·이미지·비디오·오디오를 단일 임베딩 공간에 통합
- **OpenAI/Anthropic**: GPT-4o, Claude 3 Vision은 텍스트 모델에 Vision 후속 추가

---

## III. 도메인별 강점 종합 추론

| 도메인 | 강점 순위 | 이유 |
|--------|----------|------|
| 코딩 | OpenAI > Claude > Google | 방대한 코드 포함, 기술 문서 집중 |
| 수학 | OpenAI ≈ Google > Claude | 수학 표현 명시 포함, 필터링 품질 |
| 일반 지식 | Claude > OpenAI ≈ Google | 정확성 강조 합성 데이터, 광범위 수집 |
| 멀티모달 | Google >> OpenAI > Claude | 원천 멀티모달 아키텍처 |
| 안전·윤리 응답 | Claude > OpenAI > Google | Constitutional AI 명시적 가치 내재화 |
| 창작·글쓰기 | OpenAI ≈ Claude > Google | ⚠️ 추정 (명확한 벤치마크 부족) |

---

## IV. 법적·라이선스 현황

- 미국 저작권청(2025): AI 학습 목적 사용만으로 공정 사용 자동 인정 어려움 ✅
- HarperCollins + Microsoft: 논픽션 도서당 $5,000/3년 계약 체결 (2024년 11월) ✅
- OpenAI Books1/2: 라이선스 명확하지 않음 (소송 진행 중) ✅
- Google: 상업적 라이선싱 계약 명시 ✅
- Anthropic: 라이선싱 세부사항 비공개 ⚠️

---

## V. 확인 사실 vs 추정 요약

### 확인된 사실 ✅
- GPT-3 데이터 구성 비율 (공식 논문)
- PaLM/Gemini 멀티모달 학습 방식 (기술 보고서)
- Anthropic Constitutional AI 방식 (연구 논문)
- Claude 데이터 커트오프 2023년 8월 (공식 지원 문서)
- 벤치마크 성능 수치 (MindStudio, Artificial Analysis)

### 추정 ⚠️
- GPT-4 정확한 학습 데이터 구성 (비공개)
- 각 회사 RLHF 데이터 규모
- Claude 코드 데이터 포함 정도
- 창작·글쓰기 도메인 우위 관계

---

## 출처

- GPT-4 Technical Report: https://arxiv.org/abs/2303.08774
- GPT-3 학습 데이터: https://en.wikipedia.org/wiki/GPT-3
- Gemini Technical Report: Google DeepMind 공식 보고서
- Constitutional AI: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- Claude 학습 데이터: https://support.claude.com/en/articles/8114494
- 저작권청 AI 보고서: U.S. Copyright Office Part 3 (2025)
- 벤치마크 비교: https://www.mindstudio.ai/blog/gpt-54-vs-claude-opus-46-vs-gemini-31-pro-benchmarks
