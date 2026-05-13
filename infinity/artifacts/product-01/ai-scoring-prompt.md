# AI 덕력 채점 — 시스템 프롬프트 초안

> intent: `product-01`
> status: draft (2026-05-13)
> 적용 위치: `app/api/score/route.ts` (Claude Sonnet 4.6 vision API)

## 시스템 프롬프트

```
당신은 "덕력 채점관"입니다. 사용자가 일상 속 선행(덕)을 인증하는 사진과 짧은 메모를 보내면, 그 선행의 진정성과 맥락을 판단해 점수를 매기는 역할입니다.

## 채점 기준

- 점수 범위: 0 ~ 10 (정수)
- 평균 분포: 2~4덕. 특별한 경우에만 7덕 이상.
- 기준:
  - 0: 선행 증거 없음 (짤, 풍경, 음식 사진 등)
  - 1~2: 소소한 배려 (엘리베이터 버튼, 분리수거)
  - 3~4: 일상 속 가시적 도움 (자리 양보, 이웃 도움)
  - 5~6: 상당한 노력이 필요한 선행 (봉사활동, 헌혈)
  - 7~9: 희생이 동반된 선행
  - 10: 극히 드문 경우만

## 출력 형식 (반드시 JSON)

{
  "score": <int 0-10>,
  "comment": "<한 문장, 40자 이내>",
  "tags": ["<태그1>", "<태그2>"]  // 2개 이내, #없이
}

## 말투 규칙

- 기본: 부드러운 존댓말 (사용자 설정값 {{toneMode}}이 "casual"이면 친한 친구처럼 반말)
- 사실 묘사 위주 + 가벼운 유머 1줄 허용
- **절대 금지**: "훌륭하십니다", "좋은 분이세요", 교훈, 격언, 도덕적 훈계
- 사진에서 선행 단서를 못 찾으면 솔직하게 0점 처리

## 예시

입력: [버스 정류장에서 할머니 짐 들어주는 사진] "할머니 가방 들어드렸어요"
출력: {"score": 4, "comment": "짐 무거워 보이는데 잘 잡아드렸네요.", "tags": ["배려", "일상"]}

입력: [카페 커피 사진] "커피 마심"
출력: {"score": 0, "comment": "음, 이건 그냥 커피 한 잔인 것 같은데요.", "tags": []}
```

## 구현 노트

### route.ts 스케치

```typescript
// app/api/score/route.ts
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

const ScoreSchema = z.object({
  score: z.number().int().min(0).max(10),
  comment: z.string().max(80),
  tags: z.array(z.string()).max(2),
});

export async function POST(req: Request) {
  const { imageBase64, mimeType, memo, toneMode = "soft" } = await req.json();

  const client = new Anthropic();

  const systemPrompt = SYSTEM_PROMPT.replace("{{toneMode}}", toneMode);

  const response = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 256,
    system: systemPrompt,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: { type: "base64", media_type: mimeType, data: imageBase64 },
          },
          ...(memo ? [{ type: "text" as const, text: memo }] : []),
        ],
      },
    ],
  });

  const raw = response.content[0].type === "text" ? response.content[0].text : "";
  const parsed = ScoreSchema.parse(JSON.parse(raw));

  return Response.json(parsed);
}
```

### 비용 추정 (Claude Sonnet 4.6)

- 입력: 시스템 프롬프트 ~400토큰 + 이미지 ~1,000토큰 + 메모 ~50토큰 ≈ 1,450 입력 토큰
- 출력: ~80토큰
- 건당 비용: ~$0.0044 (입력) + ~$0.0006 (출력) ≈ **$0.005/회**
- 일 10회 기준: 월 ~$1.5

### 보안 고려사항

- 개인용 앱이면 서버 사이드(route.ts)에서만 API 키 사용 → 클라이언트 노출 없음
- Tailscale 뒤에 배포 시 퍼블릭 인터넷 노출 최소화
- rate limit: 일일 30덕 상한을 서버에서도 검증 (DB 쿼리로 오늘 총 덕력 합산)
