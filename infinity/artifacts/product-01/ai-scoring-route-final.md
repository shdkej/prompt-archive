# product-01 · AI 채점 Route — 최종 통합 구현

> intent: `product-01`
> created: 2026-05-14T15:00 (heartbeat merge)
> status: ready-to-execute
> 적용 레포: `/home/ubuntu/dev/virtue-rebirth-app`
> 이 파일은 `score-api-implementation.md`(prompt caching)와 `ai-scoring-route-complete.md`(extractJson 방어)를 하나로 합친 최종본입니다.

---

## 0. 선행 작업

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm add @anthropic-ai/sdk zod
```

`.env.local` (git ignore 필수 — `.gitignore`에 `.env.local` 포함 여부 먼저 확인):
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 1. `src/app/api/score/route.ts` (최종 통합본)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { NextRequest } from "next/server";
import { z } from "zod";

// ── 입력 스키마 ──────────────────────────────────────────────────────
const RequestSchema = z.object({
  imageBase64: z.string().min(1).optional(),
  mimeType: z.enum(["image/jpeg", "image/png", "image/gif", "image/webp"]).optional(),
  memo: z.string().max(200).optional(),
  toneMode: z.enum(["soft", "casual"]).default("soft"),
});

// ── 출력 스키마 ──────────────────────────────────────────────────────
const ScoreSchema = z.object({
  score: z.number().int().min(0).max(10),
  comment: z.string().max(80),
  tags: z.array(z.string().max(10)).max(2),
});

// ── 시스템 프롬프트 — 고정 부분 (캐시 대상) ─────────────────────────
const SYSTEM_PROMPT_BASE = `\
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

## 출력 형식 (반드시 JSON만, 마크다운 코드블록 없이)
{"score": <int 0-10>, "comment": "<한 문장, 40자 이내>", "tags": ["<태그1>", "<태그2>"]}

## 공통 말투 규칙
- 사실 묘사 위주. 가벼운 유머 1줄 허용.
- 절대 금지: "훌륭하십니다", "좋은 분이세요", 교훈, 격언, 도덕적 훈계.
- 사진에서 선행 단서를 못 찾으면 솔직하게 0점.

## 예시
입력: [버스 정류장에서 할머니 짐 들어주는 사진] "할머니 가방 들어드렸어요"
출력: {"score": 4, "comment": "짐 무거워 보이는데 잘 잡아드렸네요.", "tags": ["배려", "일상"]}

입력: [카페 커피 사진] "커피 마심"
출력: {"score": 0, "comment": "음, 이건 그냥 커피 한 잔인 것 같은데요.", "tags": []}`;

// ── JSON 추출 — 코드블록 wrapping + 순수 JSON 모두 방어 ───────────
function extractJson(text: string): string {
  const codeBlock = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (codeBlock) return codeBlock[1].trim();
  const braceStart = text.indexOf("{");
  const braceEnd = text.lastIndexOf("}");
  if (braceStart !== -1 && braceEnd !== -1) return text.slice(braceStart, braceEnd + 1);
  return text.trim();
}

const client = new Anthropic();

// ── API 핸들러 ────────────────────────────────────────────────────────
export async function POST(req: NextRequest) {
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

  const toneInstruction =
    toneMode === "casual"
      ? "지금부터 답변은 반말로. 친한 친구 말투."
      : "지금부터 답변은 부드러운 존댓말로.";

  const userContent: Anthropic.MessageParam["content"] = [
    ...(imageBase64 && mimeType
      ? [
          {
            type: "image" as const,
            source: { type: "base64" as const, media_type: mimeType, data: imageBase64 },
          },
        ]
      : []),
    {
      type: "text" as const,
      text: memo ?? "(사진 없음, 텍스트 설명만)",
    },
  ];

  let rawText: string;
  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 256,
      system: [
        {
          type: "text",
          text: SYSTEM_PROMPT_BASE,
          // @ts-expect-error — cache_control is a beta field not yet in SDK types
          cache_control: { type: "ephemeral" },
        },
        { type: "text", text: toneInstruction },
      ],
      messages: [{ role: "user", content: userContent }],
    });

    rawText = response.content[0]?.type === "text" ? response.content[0].text : "";
  } catch (err) {
    console.error("[score] Anthropic error:", err);
    return Response.json({ error: "AI service error" }, { status: 502 });
  }

  try {
    const result = ScoreSchema.parse(JSON.parse(extractJson(rawText)));
    return Response.json(result);
  } catch (err) {
    console.error("[score] Parse error:", rawText, err);
    return Response.json({ error: "Invalid AI response" }, { status: 500 });
  }
}
```

---

## 2. `src/app/add/page.tsx` 수정 포인트

### 2-a. Base64 변환 유틸

```typescript
async function fileToBase64(file: File): Promise<{ base64: string; mimeType: string }> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      const [header, base64] = dataUrl.split(",");
      const mimeType = header.match(/data:([^;]+)/)?.[1] ?? "image/jpeg";
      resolve({ base64, mimeType });
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
```

### 2-b. State 추가

```typescript
const [isScoring, setIsScoring] = useState(false);
```

### 2-c. mockJudge → API 호출로 교체

```typescript
const handleScore = async () => {
  if (!selectedFile || isCapExceeded) return;
  if (rescoreCount >= 3 && hasScored) return;

  setIsScoring(true);
  try {
    const { base64, mimeType } = await fileToBase64(selectedFile);
    const res = await fetch("/api/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        imageBase64: base64,
        mimeType,
        memo,
        toneMode: tone,
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const { score, comment, tags } = await res.json();
    setPendingResult({ score, comment, tags });
    setHasScored(true);
    setRescoreCount((c) => c + 1);
  } catch {
    showToast("채점 중 오류가 생겼어요. 다시 시도해볼까요?");
  } finally {
    setIsScoring(false);
  }
};
```

### 2-d. 채점 버튼 로딩 상태

```tsx
<button
  onClick={handleScore}
  disabled={isScoring || !selectedFile || isCapExceeded || (rescoreCount >= 3 && hasScored)}
  className="..."
>
  {isScoring
    ? "채점 중..."
    : hasScored
    ? `재채점 (${3 - rescoreCount}회 남음)`
    : "채점하기"}
</button>
```

---

## 3. `src/lib/store.ts` 타입 보강

```typescript
export type IDeed = {
  id: string;
  score: number;
  comment: string;
  tags: string[];
  memo?: string;
  imageUrl?: string;   // blob URL (영속화 전) 또는 Supabase Storage URL (영속화 후)
  createdAt: string;
};
```

---

## 4. 검증 체크리스트 (로컬 실행)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm list @anthropic-ai/sdk zod
pnpm typecheck
pnpm lint
pnpm build

pnpm dev
# → /add 에서 이미지 업로드 + 채점 (soft/casual 톤 모두)
# → 재채점 3회 제한 확인
# → 0점 케이스: 음식/풍경 사진

curl -s -X POST http://localhost:3000/api/score \
  -H 'Content-Type: application/json' \
  -d '{"memo":"할머니 짐 들어드렸어요","toneMode":"soft"}' \
  | jq .
```

---

## 5. 비용 참고

| 항목 | 수치 |
|------|------|
| 시스템 프롬프트 (고정, 캐시 적용) | ~480 tokens |
| 이미지 (모바일 390px 기준) | ~1,000 tokens |
| 메모 | ~50 tokens |
| 출력 | ~80 tokens |
| 캐시 HIT 시 입력 비용 | ~$0.0003 |
| 캐시 MISS 시 (첫 호출) | ~$0.0044 입력 + $0.0012 출력 |
| 일 10회 기준 월간 | ~$0.5~1.5 |

---

## 6. 이 파일 vs 이전 파일 비교

| 기능 | score-api-implementation | ai-scoring-route-complete | **이 파일 (최종)** |
|------|------|------|------|
| prompt caching | ✅ | ❌ | ✅ |
| extractJson (코드블록 방어) | ❌ | ✅ | ✅ |
| 이미지 없는 텍스트 전용 | ✅ | ❌ | ✅ |
| NextRequest + Response.json | ❌ | ✅ | ✅ |
| safeParse 에러 처리 | ❌ | ✅ | ✅ |

---

## 7. 로컬 실행 프롬프트 (Claude Code 위임용)

```
Infinity Intent: product-01 · AI 채점 API 연결 (최종 통합본)
Mode: execute_local
Required workflow: workflow-master 먼저 읽고 복잡도 판단 후 진행
Goal: mockJudge → Claude Sonnet 4.6 Vision API 실 연결 (prompt caching + extractJson 방어)

Context:
- 앱 경로: /home/ubuntu/dev/virtue-rebirth-app
- 현재 mock: src/lib/judge.ts의 mockJudge()
- 채점 페이지: src/app/add/page.tsx
- 구현 스펙: infinity/artifacts/product-01/ai-scoring-route-final.md (이 파일)
- 이전 파일 참고 불필요: 이 파일이 score-api-implementation.md + ai-scoring-route-complete.md 통합본

Steps:
1. pnpm add @anthropic-ai/sdk zod
2. .env.local에 ANTHROPIC_API_KEY 확인 (사용자가 이미 설정했는지 먼저 체크)
3. src/app/api/score/route.ts 생성 (§1 코드 그대로)
4. src/app/add/page.tsx 수정 — handleScore 교체 (§2 패치 적용)
5. src/lib/store.ts IDeed 타입에 imageUrl?: string 추가 (§3)
6. pnpm typecheck && pnpm lint && pnpm build

Allowed: L0/L1 (파일 생성/수정, 패키지 설치, 빌드)
Forbidden: push, 외부 배포, API 키 커밋
Verification: typecheck/lint/build PASS, 개발서버에서 사진 업로드 채점 확인

Report back to: infinity/reports/product-01/{timestamp}.md
```
