# product-01 · AI 채점 API 구현 준비

> intent: `product-01`
> created: 2026-05-13 (heartbeat prepare)
> status: ready-to-execute (로컬 Claude Code에서 실행)
> 적용 레포: `/home/ubuntu/dev/virtue-rebirth-app`

## 개요

mock 채점(`mockJudge`) → Claude Sonnet 4.6 Vision API 실 연결.
시스템 프롬프트는 `ai-scoring-prompt.md` 그대로, prompt caching 추가.

---

## 1. 패키지 설치

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm add @anthropic-ai/sdk zod
```

---

## 2. 환경 변수

`.env.local` 파일 생성 (없으면):

```
ANTHROPIC_API_KEY=sk-ant-...
```

> Tailscale 배포 시에도 서버사이드에서만 사용 → 클라이언트 노출 없음.

---

## 3. `src/app/api/score/route.ts` (신규 생성)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { NextResponse } from "next/server";

const ScoreSchema = z.object({
  score: z.number().int().min(0).max(10),
  comment: z.string().max(80),
  tags: z.array(z.string()).max(2),
});

const RequestSchema = z.object({
  imageBase64: z.string(),
  mimeType: z.enum(["image/jpeg", "image/png", "image/gif", "image/webp"]),
  memo: z.string().optional(),
  toneMode: z.enum(["soft", "casual"]).default("soft"),
});

// 캐시 대상: 고정 시스템 프롬프트 (채점 기준 + 말투 룰 + 예시)
const SYSTEM_PROMPT_BASE = `당신은 "덕력 채점관"입니다. 사용자가 일상 속 선행(덕)을 인증하는 사진과 짧은 메모를 보내면, 그 선행의 진정성과 맥락을 판단해 점수를 매기는 역할입니다.

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
  "tags": ["<태그1>", "<태그2>"]
}

## 말투 공통 규칙

- 사실 묘사 위주 + 가벼운 유머 1줄 허용
- **절대 금지**: "훌륭하십니다", "좋은 분이세요", 교훈, 격언, 도덕적 훈계
- 사진에서 선행 단서를 못 찾으면 솔직하게 0점 처리

## 예시

입력: [버스 정류장에서 할머니 짐 들어주는 사진] "할머니 가방 들어드렸어요"
출력: {"score": 4, "comment": "짐 무거워 보이는데 잘 잡아드렸네요.", "tags": ["배려", "일상"]}

입력: [카페 커피 사진] "커피 마심"
출력: {"score": 0, "comment": "음, 이건 그냥 커피 한 잔인 것 같은데요.", "tags": []}`;

const client = new Anthropic();

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { imageBase64, mimeType, memo, toneMode } = RequestSchema.parse(body);

    // toneMode는 요청마다 달라지므로 캐시 밖에 둠
    const toneInstruction =
      toneMode === "casual"
        ? "지금부터 답변은 반말로 해줘. (친한 친구 말투)"
        : "지금부터 답변은 부드러운 존댓말로 해주세요.";

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 256,
      system: [
        {
          type: "text",
          text: SYSTEM_PROMPT_BASE,
          // @ts-expect-error — cache_control is a beta field, not yet in SDK types
          cache_control: { type: "ephemeral" },
        },
        { type: "text", text: toneInstruction },
      ],
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

    const raw =
      response.content[0].type === "text" ? response.content[0].text : "{}";

    // 모델이 JSON 앞뒤에 설명을 붙이는 경우 방어
    const jsonMatch = raw.match(/\{[\s\S]*?\}/);
    if (!jsonMatch) throw new Error(`Unexpected model response: ${raw}`);

    const parsed = ScoreSchema.parse(JSON.parse(jsonMatch[0]));
    return NextResponse.json(parsed);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ error: "Invalid request", detail: error.flatten() }, { status: 400 });
    }
    console.error("[score] error:", error);
    return NextResponse.json(
      { error: "채점 실패. 다시 시도해 주세요." },
      { status: 500 }
    );
  }
}
```

> **타입 에러 우회**: `@anthropic-ai/sdk`의 `system` 배열 내 `cache_control`은 beta 기능이라 TypeScript 타입에 아직 없을 수 있음. `@ts-expect-error` 주석으로 처리하거나, SDK 버전에 따라 이미 포함되어 있으면 제거해도 됨.

---

## 4. `src/app/add/page.tsx` 수정 패치

### 4-a. 추가할 헬퍼 함수 (파일 상단 또는 별도 `src/lib/image.ts`)

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

### 4-b. state 추가

```typescript
const [isScoring, setIsScoring] = useState(false);
```

### 4-c. mockJudge 호출 → API 호출로 교체

기존:
```typescript
import { mockJudge } from "@/lib/judge";
// ...
const result = mockJudge(memo, tone);
```

교체:
```typescript
// mockJudge import 제거
// ...
const scoreResult = async (file: File, memo: string, toneMode: "soft" | "casual") => {
  const { base64, mimeType } = await fileToBase64(file);
  const res = await fetch("/api/score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ imageBase64: base64, mimeType, memo, toneMode }),
  });
  if (!res.ok) throw new Error("채점 API 오류");
  return res.json() as Promise<{ score: number; comment: string; tags: string[] }>;
};
```

### 4-d. 제출 핸들러 내 교체 예시

```typescript
const handleSubmit = async () => {
  if (!selectedFile || isCapExceeded) return;
  if (rescoreCount >= 3 && hasScored) return;

  setIsScoring(true);
  try {
    const result = await scoreResult(selectedFile, memo, tone);
    // result.score, result.comment, result.tags 사용
    setPendingResult(result);
    setHasScored(true);
    setRescoreCount((c) => c + 1);
  } catch {
    showToast("채점 중 오류가 발생했어요. 다시 시도해 주세요.");
  } finally {
    setIsScoring(false);
  }
};
```

### 4-e. 로딩 UI

채점 버튼에 `isScoring` 상태 반영:
```tsx
<button
  onClick={handleSubmit}
  disabled={isScoring || !selectedFile || isCapExceeded || (rescoreCount >= 3 && hasScored)}
  className="..."
>
  {isScoring ? "채점 중..." : hasScored ? `재채점 (${3 - rescoreCount}회 남음)` : "채점하기"}
</button>
```

---

## 5. 이미지 없는 경우 fallback

이미지 선택 전 텍스트 메모만 제출하는 케이스가 있을 수 있음.
현재 route.ts는 이미지 필수(`imageBase64` required). 옵션:
- A. 이미지 없으면 기본 placeholder 이미지(1×1 투명 PNG) 전송 → 간단하지만 불정확
- B. 이미지가 없을 때 route.ts에서 텍스트 전용 분기 처리 (권장)

텍스트 전용 분기 (route.ts에 추가):
```typescript
const RequestSchema = z.object({
  imageBase64: z.string().optional(),
  mimeType: z.enum(["image/jpeg", "image/png", "image/gif", "image/webp"]).optional(),
  memo: z.string().optional(),
  toneMode: z.enum(["soft", "casual"]).default("soft"),
});

// messages content 구성 시
const imageContent = imageBase64 && mimeType
  ? [{ type: "image" as const, source: { type: "base64" as const, media_type: mimeType, data: imageBase64 } }]
  : [];

const userContent = [
  ...imageContent,
  ...(memo ? [{ type: "text" as const, text: memo }] : [{ type: "text" as const, text: "(사진 없음, 텍스트 설명만)" }]),
];
```

---

## 6. 검증 체크리스트 (로컬 실행 후)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app

# 1. 타입 검사
pnpm typecheck

# 2. 린트
pnpm lint

# 3. 빌드 (ANTHROPIC_API_KEY 없어도 빌드는 통과해야 함)
pnpm build

# 4. 개발서버 실행 후 수동 테스트
pnpm dev
# → http://localhost:3000/add 에서 이미지 업로드 후 채점 테스트
# → soft/casual 톤 전환 후 comment 말투 확인
# → 재채점 3회 제한 확인
# → 일일 30덕 상한 확인
```

---

## 7. 비용 추정 (재확인)

| 항목 | 값 |
|------|---|
| 모델 | claude-sonnet-4-6 |
| 시스템 프롬프트 | ~500토큰 (캐싱 적용 시 재사용) |
| 이미지 | ~1,000토큰 (mobile 390px 기준) |
| 메모 | ~50토큰 |
| 출력 | ~80토큰 |
| 캐시 HIT 시 입력 비용 | ~$0.0003 (캐시 읽기 요금) |
| 캐시 MISS 시 (첫 호출) | ~$0.0044 입력 + $0.0012 출력 |
| 일 10회 기준 (대부분 HIT) | 월 ~$0.5~1.5 |

---

## 8. 로컬 실행 프롬프트 (Claude Code 위임용)

```
Infinity Intent: product-01 · AI 채점 API 연결
Mode: execute_local
Required workflow: workflow-master 먼저 읽고 복잡도 판단 후 진행
Goal: mockJudge → Claude Sonnet 4.6 Vision API 실 연결

Context:
- 앱 경로: /home/ubuntu/dev/virtue-rebirth-app
- 현재 mock: src/lib/judge.ts의 mockJudge()
- 채점 페이지: src/app/add/page.tsx
- 시스템 프롬프트: infinity/artifacts/product-01/ai-scoring-prompt.md
- 구현 스펙: infinity/artifacts/product-01/score-api-implementation.md (이 파일)

Steps:
1. pnpm add @anthropic-ai/sdk zod
2. .env.local에 ANTHROPIC_API_KEY 확인/추가
3. src/app/api/score/route.ts 생성 (스펙 §3 코드 그대로)
4. src/app/add/page.tsx 수정 (스펙 §4 패치 적용)
5. pnpm typecheck && pnpm lint && pnpm build

Allowed: L0/L1 (파일 생성/수정, 패키지 설치, 빌드)
Forbidden: push, 외부 배포, API 키 커밋
Verification: typecheck PASS, lint PASS, build PASS, 개발서버 수동 확인

Report back to: infinity/reports/product-01/{timestamp}.md
```
