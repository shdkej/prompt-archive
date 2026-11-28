---
name: photo-decision
description: 사진·스크린샷을 Decisions 방식의 명시적 기준으로 가볍게 분류해 추억 기록, 회고 관찰, 반복 인사이트, 적용 후보 중 어디에 둘지 판단한다. 사진을 분류하거나 기록 가치·후속 처리를 물을 때 사용한다.
---

# Photo Decision

**목차**

- [분류 순서](#분류-순서)
- [네 가지 기록 경로](#네-가지-기록-경로)
- [후속 활용 점수](#후속-활용-점수)
- [출력](#출력)
- [Decisions API 호출 및 기록 실행](#decisions-api-호출-및-기록-실행)

사용자가 준 사진을 **OpenAI Decisions API로 실제 분류**해 무엇을 기록할지 결정합니다. `POST /v1/decisions`에 이미지와 최소 맥락을 보내고, 반환된 경로·범주·점수·신뢰도를 기준으로 기록합니다. 사진 한 장만으로 개인의 성향이나 반복 패턴을 단정하지 않습니다.

## 분류 순서

1. 사진과 사용자가 함께 준 말, 현재 대화 맥락을 증거로 삼습니다. OCR·수치·장소·사람·행동은 보이는 범위에서만 기술하고 불확실하면 `확인 불가`라고 씁니다.
2. 과거 기록 중 반복 가능성이 있는 항목은 원문에서 날짜와 짧은 근거 발췌를 확인합니다. 아래 네 판단을 API의 독립된 질문으로 보냅니다.
   - `회고 관찰인가?` — 오늘/이번 주 회고에 쓸 구체적인 생활 신호, 변화, 선택, 불편, 성취가 실제로 보이는가? (`predicate`)
   - `반복 인사이트인가?` — 과거 기록에서 같은 패턴이 확인되는가? 사진 한 장의 인상만으로는 예라고 하지 않습니다. 기록을 확인할 수 없으면 `미확인`입니다. (`predicate`)
   - `기록 경로는 무엇인가?` — 아래 네 가지 중 주된 경로를 하나 고릅니다. (`choice`)
   - `후속 활용 가치는 어느 정도인가?` — 아래 순서형 기준으로 평가합니다. (`score`)
3. `route`, `category`, `follow_up_score`, `confidence_band`는 API 응답을 그대로 사용합니다. API의 선택을 SAM 판단으로 덮어쓰지 않습니다. API는 분류 근거의 자연어 설명을 생성하지 않으므로, 설명 문장만 사진에서 직접 보이는 사실로 작성합니다.
4. 판단을 짧게 반환하고, API 응답에 따라 기록합니다. API가 거부하거나 오류가 나면 일반 모델 판단으로 대체하지 않고 분류·기록을 중단해 오류를 알립니다.

## 네 가지 기록 경로

- **추억 기록 (`memory`)**: 의미는 개인적이지만 당장 재사용할 관찰이나 선택은 보이지 않습니다. 날짜와 한 줄 맥락이면 충분합니다. 분석을 덧붙이지 않습니다.
- **회고 관찰 (`observation`)**: 하루·주간 회고에 쓸 만한 구체 신호가 있습니다. 예: 수면/사용시간 수치, 반복된 불편의 한 장면, 중요한 선택·성취. 관찰은 사실 묘사로 남기고 해석과 분리합니다.
- **반복 인사이트 (`insight`)**: 한 장면이 기존 기록의 반복 신호를 보강하거나, 기록 간 연결을 드러냅니다. 근거가 된 날짜/기록을 찾을 수 있을 때만 승격합니다. 가설은 검증 전까지 가설로 표시합니다.
- **적용 후보 (`application`)**: 관찰/가설을 회고, 작업 방식, 제품·콘텐츠 아이디어, 개선 과제에 연결할 구체적이고 작은 다음 변화가 있습니다. 이는 후보일 뿐 실행·발행 승인이 아닙니다.

`memory`는 낮은 가치라는 뜻이 아닙니다. 나중에 다시 보고 싶은 장면도 충분히 보존할 이유가 있습니다. `insight`는 사진의 멋짐·특이함·감정 강도만으로 선택하지 않습니다.

## 후속 활용 점수

0–3의 ordered score를 씁니다. 점수는 가치의 절대 측정이 아니라 다음 행동의 구체성입니다.

- `0 — 보존`: 개인적인 장면이나 맥락은 있으나 회고/후속 행동 근거는 거의 없음.
- `1 — 회고`: 오늘 또는 주간 회고에 쓸 구체 관찰이 하나 있음.
- `2 — 검증`: 기존 기록과 연결되거나 다시 확인할 가치가 있는 가설이 있음. 근거 기록 또는 재관찰 조건을 명시.
- `3 — 적용`: 결과물·작업·제품·콘텐츠에 연결할 구체적인 작은 적용 후보가 있음.

## 출력

짧고 구조적으로 답합니다.

```text
분류: {memory | observation | insight | application | 보류}
보이는 근거: {사진에서 확인한 사실 한 문장}
판단: {왜 이 경로인지; insight는 반복 근거 날짜/기록 포함}
활용 점수: {0–3} / 신뢰도: {낮음·보통·높음}
기록/다음 처리: {기록할 최소 내용 또는 추가 맥락 질문; 없으면 없음}
```

기록을 확인하지 못했는데 반복성을 주장하지 말고 `반복 여부 미확인`이라고 밝힙니다. 사진에 민감한 개인 정보가 있으면 필요한 최소 내용만 요약하고 원문 OCR을 복제하지 않습니다. 타인에 대한 추론, 의료 진단, 재무 판단을 사진만으로 확정하지 않습니다.

## Decisions API 호출 및 기록 실행

- 사용자가 분류 후 보관을 선택했으므로, 사진이 입력되면 기존 이미지 수집 흐름에 따라 원본을 R2에 업로드하고 공개 HTTPS URL을 확보한 뒤 판단하고 기록합니다. Slack 이미지의 `image_topics` 주제/태그 저장도 기존 규칙대로 수행하며, 이 스킬은 그 흐름을 대체하지 않습니다. OpenClaw 내부 `media://` 참조를 API에 직접 보내지 않습니다.
- `record_photo_decision.py` CLI가 기록 전에 Decisions API를 한 번 호출합니다. 지원 모델은 `gpt-6-luna`이며, 이미지가 공개 접근 가능한 HTTPS URL이어야 합니다. File ID와 `media://`는 API 입력으로 지원되지 않습니다. 이 API 호출은 유료 사용량을 발생시킬 수 있으며 사진마다 요청 한 번을 보냅니다.
- API 키는 Gateway 실행 환경의 `OPENAI_API_KEY`로 제공되어야 합니다(보호 Secret Store 주입도 가능). 반드시 `gateway_exec`에서 스크립트를 실행합니다. 일반 로컬 셸에서 실행하거나 키를 명령행·파일·로그에 복사하지 않습니다. 키가 없으면 설정된 안전한 입력 흐름으로 요청하고, 직접 대체 인증이나 로컬 모델 fallback을 하지 않습니다.
- API 입력에는 이미지, 사용자가 제공한 맥락, 검증한 과거 기록의 짧은 발췌만 포함합니다. 과거 근거는 `data/` 내 실제 파일·날짜·원문 발췌가 모두 확인되어야 하며 사진보다 이전이어야 합니다. 근거가 없으면 요청 선택지에서 `insight`를 제외합니다.
- API 질문은 주 분류 `choice`, 내용 범주 `choice`, 후속 활용 `score`, 신뢰도 수준 `choice`입니다. 순서형 점수는 API가 반환한 0–3 사이의 가중 평균(소수 가능)을 그대로 기록합니다. API가 거부·오류·유효하지 않은 응답을 반환하면 기록을 만들지 않습니다. 재호출은 자동 반복하지 않습니다.
- 사용자가 인사이트·카드뉴스·공유용 콘텐츠를 명시했거나 이미 카드뉴스 제작 맥락이 활성화된 경우에는 일일 분류만으로 종료하지 말고 `DATA_CAPTURE_RULES.md`의 Photo To Shareable Output과 `insight-card-maker` 경로를 따릅니다. 이 스킬에서 사진을 기록하는 선택 자체는 카드뉴스 업로드·배포 승인이 아닙니다.
- 모든 사진은 `data/daily-tracking/YYYY-MM-DD.md`에 URL, 가벼운 범주, 핵심 맥락, 분류 결과를 기록합니다. 같은 사진/메시지는 중복 기록하지 않습니다.
- `memory`는 일일 기록만 남기며 분석을 덧붙이지 않습니다. `observation`은 회고에 쓸 관찰일 때만 `photo-insights/insight-log.md`에 승격합니다. `insight`는 반복을 뒷받침하는 과거 기록이 확인된 경우에만 가설을 `hypotheses.md`에 추가하고, 단일 사진이면 가설로 만들지 않습니다. `application`은 구체적인 작은 변경 제안이 있을 때 `application-candidates.md`에도 후보로 추가합니다.
- 기록은 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/record_photo_decision.py`를 호출합니다. 이 스크립트가 중복 확인 → Decisions API 호출 → API 선택값 적용 → 로컬 기록을 수행합니다. `source_id`는 재처리 때도 같은 Slack 메시지 ID나 media ID를 씁니다. 촬영일을 모르면 `recorded_at`을 생략해 현재 KST로 기록합니다.

```json
{
  "source_id": "<stable-message-or-media-id>",
  "image_url": "<verified-original-image-url>",
  "visual_evidence": "<one concise, directly visible fact>",
  "context": "<user-provided context or empty string>",
  "observation": "<required for observation, insight, or application>",
  "next_action": "<small internal next step or empty string>",
  "application": "<required only for application>",
  "application_target": "<daily_review|weekly_review|Infinity|agent-wiki|output; required only for application>",
  "repetition_evidence": [{"path": "<verified relative path under data/>", "date": "<YYYY-MM-DD>", "excerpt": "<exact short excerpt from that file>"}]
}
```

`route`, `category`, `confidence`, `score`는 입력하지 않습니다. Decisions API 응답에서 가져옵니다. JSON에는 위 입력 필드만 전달하고, `record_photo_decision.py`는 Gateway에서 실행해야 합니다. `insight`의 `repetition_evidence`는 실제 존재하는 과거 파일이어야 하며, 날짜와 발췌가 파일 내용과 일치해야 합니다.

JSON을 Base64로 인코딩한 뒤 Gateway 실행 도구의 `env`에 `PHOTO_DECISION_INPUT_B64`로 전달합니다. `command`는 다음처럼 지정합니다. 키 값을 명령에 넣지 않으며, Gateway 환경의 `OPENAI_API_KEY`를 상속받습니다.

```sh
printf '%s' "$PHOTO_DECISION_INPUT_B64" | base64 --decode | python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/record_photo_decision.py
```

- JSON 출력의 `status`와 `route`를 확인합니다. `promotion_suppressed_daily_limit: true`면 승격 대신 일일 기록만 남긴 것이므로 그 사실을 응답에 짧게 밝혀줍니다. API 요청이 전송된 뒤 타임아웃 등으로 결과가 불명확하면 자동 재실행하지 않습니다. 요청 ID·사용량을 확인하거나 사용자에게 확인한 뒤 재시도합니다.
- 민감한 원문/OCR은 필요한 최소 요약만 저장합니다. 사진 자체나 URL을 새 정본 위치에 복제하지 않습니다.
- 외부 공개, 콘텐츠 발행, 타인에게 메시지 발송, 비용 발생, 권한 변경은 기록 후보로 남길 뿐 이 분류만으로 실행하지 않습니다.
- 사용자가 명시적으로 `분류만`, `저장하지 마`라고 하면 이번 요청에서는 추가 기록을 생략합니다.

API 계약 근거: [OpenAI Decisions 가이드](https://developers.openai.com/api/docs/guides/decisions), [Create a decision API reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)
