# AI 채점 Route — 완성 구현 초안

> intent: `product-01`
> prepared: 2026-05-13 (heartbeat)
> 적용 대상: `/home/ubuntu/dev/virtue-rebirth-app/src/app/api/score/route.ts`
> 의존 패키지: `@anthropic-ai/sdk` (신규), `zod` (기존 없으면 추가)

## 0. 선행 작업

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm add @anthropic-ai/sdk zod
```

`.env.local` (git ignore 필수):
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 1. `src/app/api/score/route.ts` (완성본)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { NextRequest } from "next/server";
import { z } from "zod";

// ── 입력 스키마 ──────────────────────────────────────────────
const RequestSchema = z.object({
  imageBase64: z.string().min(1),
  mimeType: z.enum(["image/jpeg", "image/png", "image/gif", "image/webp"]),
  memo: z.string().max(200).optional(),
  toneMode: z.enum(["soft", "casual"]).default("soft"),
});

// ── 출력 스키마 ──────────────────────────────────────────────
const ScoreSchema = z.object({
  score: z.number().int().min(0).max(10),
  comment: z.string().max(80),
  tags: z.array(z.string().max(10)).max(2),
});

// ── 시스템 프롬프트 ─────────────────────────────────────────
const SYSTEM_PROMPT = (toneMode: "soft" | "casual") => `\
당신은 "덕력 채점관"입니다. 사용자가 일상 속 선행(덕)을 인증하는 사진과 짧은 메모를 보내면, 그 선행의 진정성과 맥락을 판단해 점수를 매깁니다.

## 채점 기준
- 점수 범위: 0 ~ 10 (정수)
- 평균 분포: 2~4덕. 특별한 경우에만 7덕 이상.
- 0: 선행 증거 없음 (카페/음식/풍경 사진 등)
- 1~2: 소소한 배려 (엘리베이터 버튼, 분리수거)
- 3~4: 일상 속 가시적 도움 (자리 양보, 이웃 도움)
- 5~6: 상당한 노력이 필요한 선행 (봉사활동, 헌혈)
- 7~9: 희생이 동반된 선행
- 10: 극히 드문 경우만

## 말투 규칙
${
  toneMode === "casual"
    ? "- 친한 친구처럼 반말. 장난스럽고 가볍게."
    : "- 부드러운 존댓말. 따뜻하되 가볍게."
}
- 사실 묘사 위주. 가벼운 유머 1줄 허용.
- 절대 금지: "훌륭하십니다", "좋은 분이세요", 교훈, 격언, 도덕적 훈계.
- 사진에서 선행 단서를 못 찾으면 솔직하게 0점.

## 출력 형식 (반드시 JSON만, 마크다운 코드블록 없이)
{"score": <int 0-10>, "comment": "<한 문장, 40자 이내>", "tags": ["<태그1>", "<태그2>"]}

## 예시
입력: [버스 정류장에서 할머니 짐 들어주는 사진] "할머니 가방 들어드렸어요"
출력: {"score": 4, "comment": "짐 무거워 보이는데 잘 잡아드렸네요.", "tags": ["배려", "일상"]}

입력: [카페 커피 사진] "커피 마심"
출력: {"score": 0, "comment": "음, 이건 그냥 커피 한 잔인 것 같은데요.", "tags": []}`;

// ── JSON 추출 (코드블록 wrapping 방어) ──────────────────────
function extractJson(text: string): string {
  const match = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (match) return match[1].trim();
  const braceStart = text.indexOf("{");
  const braceEnd = text.lastIndexOf("}");
  if (braceStart !== -1 && braceEnd !== -1) {
    return text.slice(braceStart, braceEnd + 1);
  }
  return text.trim();
}

// ── API 핸들러 ───────────────────────────────────────────────
export async function POST(req: NextRequest) {
  // 1. 입력 검증
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const parsed = RequestSchema.safeParse(body);
  if (!parsed.success) {
    return Response.json(
      { error: "Bad request", details: parsed.error.flatten() },
      { status: 400 }
    );
  }
  const { imageBase64, mimeType, memo, toneMode } = parsed.data;

  // 2. Anthropic 호출
  const client = new Anthropic();
  let rawText: string;
  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 256,
      system: SYSTEM_PROMPT(toneMode),
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

    const block = response.content[0];
    rawText = block.type === "text" ? block.text : "";
  } catch (err) {
    console.error("[score] Anthropic error", err);
    return Response.json({ error: "AI service error" }, { status: 502 });
  }

  // 3. JSON 파싱 + 스키마 검증
  try {
    const json = extractJson(rawText);
    const result = ScoreSchema.parse(JSON.parse(json));
    return Response.json(result);
  } catch (err) {
    console.error("[score] Parse error", rawText, err);
    return Response.json({ error: "Invalid AI response" }, { status: 500 });
  }
}
```

---

## 2. `src/app/add/page.tsx` 수정 포인트

현재 `addDeed` 를 호출하는 `handleScore` 함수에서 mock judge 대신 fetch 호출로 교체.

```typescript
// 기존: const result = mockJudge(memo, tone);
// 교체:
async function handleScore() {
  if (!imageFile) return;

  setIsScoring(true);
  try {
    const base64 = await toBase64(imageFile);            // 아래 유틸 참조
    const res = await fetch("/api/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        imageBase64: base64,
        mimeType: imageFile.type,
        memo,
        toneMode: tone,                                  // store의 useTone()
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const { score, comment, tags } = await res.json();
    addDeed({ score, comment, tags, memo, imageUrl: URL.createObjectURL(imageFile) });
  } catch (err) {
    showToast("채점 중 문제가 생겼어요. 다시 시도해볼까요?");
    console.error(err);
  } finally {
    setIsScoring(false);
  }
}

// Base64 변환 유틸 (add/page.tsx 상단에 추가)
function toBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      resolve(result.split(",")[1]);                     // "data:image/jpeg;base64," 제거
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
```

---

## 3. `src/lib/store.ts` 타입 보강

`IDeed` 에 `imageUrl?: string` 필드가 없다면 추가 (blob URL 미리보기용):

```typescript
export type IDeed = {
  id: string;
  score: number;
  comment: string;
  tags: string[];
  memo?: string;
  imageUrl?: string;   // blob URL (영속화 전까지 브라우저 세션 한정)
  createdAt: string;   // ISO
};
```

---

## 4. 검증 체크리스트 (로컬 실행)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app

# 패키지 설치 확인
pnpm list @anthropic-ai/sdk zod

# 타입 체크
pnpm typecheck

# 린트
pnpm lint

# 빌드
pnpm build

# 실서버 기동 후 API probe
pnpm start &
curl -s -X POST http://localhost:3000/api/score \
  -H 'Content-Type: application/json' \
  -d '{"imageBase64":"<tiny_test_b64>","mimeType":"image/jpeg","memo":"테스트","toneMode":"soft"}' \
  | jq .

# 5 페이지 상태 확인
for p in / /add /deeds /dex /me; do
  curl -o /dev/null -sw "%{http_code} $p\n" http://localhost:3000$p
done
```

---

## 5. 비용 참고

| 항목 | 수치 |
|------|------|
| 입력 (시스템 ~420토큰 + 이미지 ~1,000토큰 + 메모 ~50토큰) | ~1,470 tokens |
| 출력 (~80토큰) | ~80 tokens |
| 건당 비용 (Sonnet 4.6) | ~$0.005 |
| 일 10회 기준 월간 | ~$1.5 |

---

## 6. 다음 단계 (이 구현 이후)

1. `imageUrl` 영속화 — R2 또는 Supabase Storage에 업로드 후 signed URL 저장.
2. 서버사이드 일일 30덕 rate limit — DB 쿼리로 오늘 총 덕력 합산 후 초과 시 429.
3. 배포 (`virtue.oracle.shdkej.com`) — Vercel 또는 로컬 Tailscale 뒤.
