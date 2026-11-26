---
name: travel-content-feedback
description: Generate one daily Instagram/Threads travel-content test image from the user's current travel location and progress, upload it to the Cloudflare/R2 image endpoint, send it to Telegram with like/dislike feedback controls, and record feedback for preference learning. Use when the user asks for daily travel content experiments, Instagram test images, content feedback loops, preference-learning image posts, or when Telegram callback data starts with travel_feedback:.
---

# Travel Content Feedback

## 개요

마스터의 현재 여행 위치와 진행도를 바탕으로 매일 **이미지 1장짜리 콘텐츠 가설**을 빠르게 만들고, Telegram에서 `좋아요 / 안돼요` 피드백을 받아 취향을 학습한다.

목표는 완성형 카드뉴스가 아니라 빠른 선호도 실험이다. 매 회차는 한 장만 만들고, 반응이 쌓인 뒤 좋은 방향만 Instagram carousel, Threads 글, YouTube 소재로 승격한다.

## 운영 원칙

- 여행 위치·예약·진행도는 SAM이 추측하지 않는다. 먼저 `hj` 에이전트에게 공개 가능한 현재 위치와 진행도를 확인한다.
- 결과물은 이미지 1장만 만든다. 여러 장, 긴 카드뉴스, 게시 자동화로 확장하지 않는다.
- 공개 게시가 아니라 테스트 전송이다. Instagram 실제 게시, 광고, 외부 권한 변경은 별도 승인 전에는 하지 않는다.
- 피드백은 단순 이진 신호로 시작한다: `like` 또는 `dislike`.
- 평가 단위는 이미지 전체가 아니라 `angle`, `title`, `copy`, `visual_style`, `travel_context` 필드를 함께 저장한다.
- 이미지는 Cloudflare/R2 업로드 엔드포인트 `https://upload.shdkej.com?kind=derived`에 올린다. 토큰은 환경변수 `CLOUDFLARE_IMAGE_UPLOAD_TOKEN`에서만 읽고 출력하지 않는다.

## 매일 실행 흐름

1. 먼저 공개 여행 대시보드 원장을 확인한다.
   - 1순위 로컬 파일: `/home/ubuntu/workspace/space/infra-aws-static-sites/sites/travel/dist/travel-data.json`
   - 2순위 공개 URL: `https://travel.aws.shdkej.com/travel-data.json`
   - 필요한 값: `generatedAt`, `current.date`, `current.location`, `current.mapQuery`, 진행도.
   - `generatedAt`이 36시간 이내이고 `current`가 오늘 또는 최신 공개 일정으로 잡혀 있으면 `location_source=travel-dashboard`, `location_confidence=confirmed-public-safe`로 둔다.
2. 그 다음 `hj`에게 민감 정보 제거와 공개 가능성만 확인시킨다.
   - `hj`는 대시보드 값을 검증하거나 민감정보 위험을 지적하는 역할이다.
   - 대시보드가 없거나 오래됐을 때만 `hj` 메모리/상태를 fallback으로 쓴다.
   - 모르면 `location_confidence: low`로 두고 추정하지 않는다.
3. 최근 피드백 원장을 확인한다.
   - 기본 경로: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/feedback.jsonl`
   - 좋아요가 많은 `angle`, `title_pattern`, `visual_style`을 우선한다.
   - 싫어요가 누적된 패턴은 같은 주에 반복하지 않는다.
4. 오늘의 콘텐츠 가설 1개를 정한다.
   - 예: `여행은 휴가가 아니라 기준을 만드는 실험이다.`
   - 제목은 짧게, 본문은 한 문장만 둔다.
   - 2026-08-20 이후 기본 템플릿은 `black-reels-type`이다. 검은 배경, 청록 제목, 흰색 본문만 남기고 날짜·위치·계정명·설명 라벨 같은 불필요한 글자는 이미지 안에 넣지 않는다.
5. 확인된 context JSON을 만든 뒤 `scripts/run_daily_test.py`를 실행한다.
6. runner가 렌더링, R2 업로드, URL 확인, Telegram 전송, 피드백 컨트롤 전송, pending 원장 기록을 한 번에 수행한다.
7. 사용자의 선택이 확인되면 피드백 원장에 한 줄 추가한다.

`run_daily_test.py`는 `location_source`가 `travel-dashboard`, `hj`, `hj:travel-dashboard` 중 하나이고 `location_confidence: confirmed-public-safe` 또는 `high`가 있으면 위치형 테스트를 생성한다. 위치·이동·진행도 노출 위험 때문에 high가 나오지 않더라도, 오늘의 여행 감각·행동·인사이트를 도시명 없이 쓸 수 있으면 `location_source: locationless-safe`, `location_confidence: locationless-safe`로 비위치형 테스트를 생성한다. 이 fallback context에는 `location`, `previous_move`, 실시간 진행도, 숙소·예약·이동 정보가 들어가면 안 된다. 사용자에게 보이는 캡션에도 위치를 쓰지 않는다. 정말 만들 근거가 없거나 사용자 안전을 해칠 위험이 남을 때만 skip한다.

## 렌더링 스크립트

기본 실행:

```bash
python3 /home/ubuntu/workspace/prompt-archive/skills/custom/travel-content-feedback/scripts/run_daily_test.py \
  --context-json /path/to/context.json
```

렌더링만 따로 확인할 때:

```bash
python3 /home/ubuntu/workspace/prompt-archive/skills/custom/travel-content-feedback/scripts/render_daily_test.py \
  --context-json /path/to/context.json \
  --out-dir /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/travel-content-feedback
```

위치형 `context.json` 예시:

```json
{
  "date": "2026-08-06",
  "location": "카파도키아",
  "progress": "터키 여행 중반",
  "previous_move": "이스탄불을 지나 카파도키아로 이동",
  "angle": "여행은 휴가가 아니라 기준을 만드는 실험이다",
  "title": "세계여행은 휴가가 아니었습니다",
  "copy": "낯선 도시를 지날 때마다, 내가 뭘 좋아하고 뭘 남기고 싶은지 더 선명해졌습니다.",
  "visual_style": "black-reels-type"
}
```

비위치형 fallback `context.json` 예시:

```json
{
  "date": "2026-08-21",
  "angle": "여행은 장소보다 가능한 행동을 넓히는 일이다",
  "title": "여행의 폭이 넓어졌다",
  "copy": "새로운 행동을 하나 배울 때마다, 다음 도시에서 할 수 있는 선택이 늘어났습니다.",
  "visual_style": "black-reels-type",
  "location_source": "locationless-safe",
  "location_confidence": "locationless-safe",
  "safety_note": "도시명, 숙소, 이동, 진행도를 이미지와 캡션에 넣지 않는다."
}
```

출력 JSON은 `image_path`, `upload_url`, `metadata_path`를 포함한다.

## Telegram 피드백

가능하면 rich presentation inline button을 먼저 시도한다. Telegram callback 값은 64 bytes 제한을 넘기지 않도록 짧은 ASCII 토큰만 쓴다. 이 워크플로우는 OpenClaw의 Telegram callback bridge가 raw `callback_data`를 직접 해석하므로 `action: {"type":"callback",...}`가 아니라 legacy `value` 필드를 사용한다. `action:callback`은 `tgcb1:...` opaque wrapper로 포장되어 `tf:...` 매칭을 우회한다.

- `좋아요`: `tf:l:{short_id}`
- `안돼요`: `tf:d:{short_id}`

`short_id`는 run_id 마지막 해시 조각이다. 예: `2026-08-06-카파도키아-8ea9bae0` → `8ea9bae0`.

inline button이 지원되지 않거나 실패하면 Telegram poll로 대체한다.

- 질문: `오늘 테스트 이미지 어때요?`
- 선택지: `좋아요`, `안돼요`

현재 OpenClaw Telegram `message poll`은 생성 결과의 `pollId`만 돌려주며, CLI/세션 기록에서 poll 선택 결과를 안정적으로 조회할 수 없다. poll fallback을 쓴 경우에는 마스터가 채팅으로 `좋아요` 또는 `안돼요`라고 답한 값을 신뢰 가능한 결과로 기록한다.

poll로 대체한 경우에도 run metadata에는 `feedback_mode: poll_fallback`을 기록한다.

버튼 callback이나 사용자의 명시 답변을 받으면 아래 스크립트로 기록한다.

```bash
python3 /home/ubuntu/workspace/prompt-archive/skills/custom/travel-content-feedback/scripts/record_feedback.py \
  --run-id 2026-08-06-kapadokya-001 \
  --signal like \
  --source telegram-button
```

동일 `run_id`는 피드백을 한 번만 확정한다. 같은 버튼을 여러 번 누르거나 재전송된 컨트롤을 눌러도 `feedback:{run_id}` idempotency key로 중복 기록하지 않는다.

`tf:{signal_code}:{short_id}` 형식의 callback이 이 세션으로 들어오면 `runs/*.json`의 `callback_map`에서 원래 `run_id`와 `signal`을 찾은 뒤 즉시 위 스크립트를 실행한다. 버튼 전송 후에는 Gateway 로그에 callback 수신과 `travel feedback callback recorded`가 남는지 확인한다. Gateway가 재시작·drain 중인 동안 클릭하면 Telegram에서 클릭 처리는 되더라도 OpenClaw가 받을 수 없으므로, `gateway ready` 이후에 다시 보내고 클릭해야 한다. 예:

```bash
python3 /home/ubuntu/workspace/prompt-archive/skills/custom/travel-content-feedback/scripts/record_feedback.py \
  --run-id 2026-08-06-카파도키아-8ea9bae0 \
  --signal like \
  --source telegram-callback
```

## 피드백 저장 형식

`/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/feedback.jsonl`에 한 줄씩 쓴다.

```json
{"ts":"2026-08-06T21:00:00+09:00","run_id":"2026-08-06-kapadokya-001","status":"resolved","signal":"like","angle":"...","title":"...","visual_style":"warm-minimal-travel-note","url":"https://..."}
```

피드백을 자동으로 확인할 수 없으면, 다음 대화에서 사용자가 누른 값이나 답변한 값을 보고 SAM이 같은 형식으로 기록한다.

## Cron 등록 증거

cron을 만들거나 바꾸면 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/cron-job.json`에 최소 정보를 저장한다.

```json
{"job_id":"...","name":"Travel content feedback daily test","schedule":"20 9 * * *","tz":"Asia/Seoul","next_run_at_ms":1786062000000}
```

cron payload에는 다음 조건을 반드시 포함한다.

- 실행 시작 시 먼저 `/home/ubuntu/workspace/space/infra-aws-static-sites/sites/travel/dist/travel-data.json`을 읽고, 없을 때만 `https://travel.aws.shdkej.com/travel-data.json`을 확인한다. `hj`에게 먼저 묻지 않는다.
- 대시보드에서 최신 공개 위치·직전 이동·진행도를 만든 뒤 `hj`에게 민감정보 제거/공개 가능성만 확인시킨다. `hj` 메모리는 대시보드가 없거나 stale일 때만 fallback으로 쓴다.
- 확인 실패 또는 low confidence면 먼저 비위치형 fallback context를 만든다. 이 context는 도시명·숙소·이동·진행도를 모두 제거하고 `location_source=locationless-safe`, `location_confidence=locationless-safe`로 `run_daily_test.py`를 호출한다. 비위치형으로도 안전하게 만들 수 없을 때만 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/travel-content-feedback/runs/YYYY-MM-DD-skipped.json`에 확인한 source, `generatedAt`, 중단 사유를 남긴다.
- 확인 성공 시 context JSON을 저장하고 `run_daily_test.py --context-json <context>`를 호출한다. 이때 `location_source`는 `travel-dashboard` 또는 `hj:travel-dashboard`, `location_confidence`는 `confirmed-public-safe`를 쓴다.
- 실행 후 `runs/{run_id}.json`에 `image_url`, Telegram image/control message id, callback value, URL 확인 결과를 남긴다.

## 품질 기준

- 1080x1350 PNG를 기본으로 한다.
- 한 화면에 주인공 문장은 하나만 둔다.
- 제목은 16자 안팎, 본문은 1문장만 둔다.
- 기본 시각 스타일은 `black-reels-type`이다.
  - 검은 배경.
  - 제목은 굵은 청록색.
  - 본문은 흰색 중심, 핵심 한 줄만 청록색으로 강조.
  - 인스타 UI, 계정명, 날짜, 위치, 진행도, `TRAVEL TEST`, 핸들, 푸터 문구를 이미지 안에 넣지 않는다.
  - 카드 테두리, 종이 질감, 장식 도형, 설명 라벨은 쓰지 않는다.
- 이미지 안에 민감한 위치, 숙소, 예약, 비용, 얼굴 정보는 넣지 않는다.
- 자동 생성 문구가 마스터의 실제 고민과 어긋나면 실패로 본다.
