# product-01 · Supabase Storage 사진 영속화 가이드

> intent: `product-01`
> created: 2026-05-13 (heartbeat prepare)
> status: ready-to-execute
> 적용 레포: `/home/ubuntu/dev/virtue-rebirth-app`

## 개요

현재 상태: 사진 선택 시 `blob URL` 로 미리보기만 표시, 새로고침 시 소멸.
목표: Supabase Storage에 업로드 → 영구 URL을 `deeds.image_url`에 저장.

### 실행 흐름 결정

```
[사용자 사진 선택]
       ↓
[/api/score 호출] — base64 전송 (AI 채점용, 빠름)
       ↓
[채점 결과 표시] ← 재채점 가능
       ↓
[사용자 "덕 기록" 확정 클릭]
       ↓
[Supabase Storage 업로드] — File 객체 → 영구 URL 획득
       ↓
[addDeed(score, comment, tags, imageUrl)] — DB 저장
```

> AI 채점과 스토리지 업로드를 분리하는 이유: 재채점 시 불필요한 스토리지 용량 낭비 방지.

---

## 1. Supabase Storage 버킷 설정

Supabase 대시보드 → Storage → New Bucket:
- 이름: `deed-photos`
- Public: **ON** (RLS로 제어, 공개 URL 필요)

Storage Policies (SQL 편집기에서 실행):

```sql
-- deed-photos 버킷에 anon 업로드 허용
create policy "anon upload"
  on storage.objects for insert
  to anon
  with check (bucket_id = 'deed-photos');

-- deed-photos 버킷 공개 읽기 허용
create policy "public read"
  on storage.objects for select
  to public
  using (bucket_id = 'deed-photos');
```

---

## 2. `src/lib/supabase-storage.ts` (신규 생성)

```typescript
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function uploadDeedPhoto(file: File): Promise<string | null> {
  const ext = file.name.split(".").pop() ?? "jpg";
  const path = `${Date.now()}-${Math.random().toString(36).slice(2)}.${ext}`;

  const { error } = await supabase.storage
    .from("deed-photos")
    .upload(path, file, { contentType: file.type, upsert: false });

  if (error) {
    console.error("[storage] upload failed:", error.message);
    return null;
  }

  const { data } = supabase.storage.from("deed-photos").getPublicUrl(path);
  return data.publicUrl;
}
```

---

## 3. `src/app/add/page.tsx` 수정

### 3-a. 추가 import

```typescript
import { uploadDeedPhoto } from "@/lib/supabase-storage";
```

### 3-b. 상태 추가

```typescript
const [isUploading, setIsUploading] = useState(false);
```

### 3-c. "덕 기록" 확정 핸들러 수정

기존 `handleConfirm` (또는 `addDeed` 호출 지점):

```typescript
// 기존
addDeed({ ...pendingResult, memo, createdAt: new Date().toISOString() });

// 교체
const handleConfirm = async () => {
  if (!pendingResult || !selectedFile) return;

  setIsUploading(true);
  let imageUrl: string | undefined;
  try {
    const url = await uploadDeedPhoto(selectedFile);
    imageUrl = url ?? undefined;
  } catch {
    // 업로드 실패해도 텍스트 기록은 이어감
    showToast("사진 저장 중 오류가 났어요. 덕행은 기록할게요.");
  } finally {
    setIsUploading(false);
  }

  addDeed({
    ...pendingResult,
    memo,
    imageUrl,
    createdAt: new Date().toISOString(),
  });
  // 다음 단계로 이동 (navigate or reset)
};
```

### 3-d. 확정 버튼 로딩 상태

```tsx
<button
  onClick={handleConfirm}
  disabled={isUploading || !pendingResult}
  className="..."
>
  {isUploading ? "기록 중..." : "덕 기록하기"}
</button>
```

---

## 4. `src/lib/store.ts` 타입 수정

`IDeed` 타입에 `imageUrl` 필드 추가:

```typescript
export interface IDeed {
  id: string;
  memo: string;
  score: number;
  comment: string;
  tags: string[];
  imageUrl?: string;   // ← 추가 (Supabase Storage URL or undefined)
  createdAt: string;
}
```

---

## 5. `src/app/deeds/page.tsx` 이미지 표시

덕행록에서 `imageUrl`이 있을 때 썸네일 표시:

```tsx
{deed.imageUrl && (
  <img
    src={deed.imageUrl}
    alt="덕행 인증"
    className="w-14 h-14 rounded-xl object-cover flex-shrink-0"
    loading="lazy"
  />
)}
```

---

## 6. 검증 체크리스트 (로컬 실행 후)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app

pnpm typecheck
pnpm lint
pnpm build

# 수동 테스트
pnpm dev
# 1. /add 에서 이미지 업로드 + 채점 → "덕 기록하기" 클릭
# 2. Supabase Storage 대시보드에서 deed-photos 버킷에 파일 생성 확인
# 3. /deeds 에서 썸네일 표시 확인
# 4. 새로고침 후에도 이미지 유지 확인
```

---

## 7. Fallback 전략

업로드 실패 시에도 덕행 기록은 유지 (imageUrl만 없는 상태):
- 토스트: "사진 저장 중 오류가 났어요. 덕행은 기록할게요."
- 기록 화면에서 이미지 없는 카드는 빈 공간 없이 렌더링 (조건부 렌더링으로 처리)

---

## 8. 전제 조건

- `persistence-decision.md` §구현 순서 먼저 실행 완료 (Supabase 클라이언트 초기화)
- `.env.local`에 `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` 설정 완료

---

## 9. 로컬 실행 프롬프트 (Claude Code 위임용)

```
Infinity Intent: product-01 · 사진 영속화 (Supabase Storage)
Mode: execute_local
Required workflow: workflow-master 먼저 읽고 복잡도 판단 후 진행
Goal: 덕행 사진을 Supabase Storage에 업로드하고 URL을 deeds에 저장

Context:
- 앱 경로: /home/ubuntu/dev/virtue-rebirth-app
- 현재: add/page.tsx에서 blob URL 미리보기만
- 영속화 스펙: infinity/artifacts/product-01/photo-storage-guide.md (이 파일)
- 전제: persistence-decision.md 실행 완료 (Supabase 클라이언트 초기화 완료)

Steps:
1. Supabase Storage 대시보드에서 deed-photos 버킷 생성 + RLS 정책 설정 (§1)
2. src/lib/supabase-storage.ts 생성 (§2 코드 그대로)
3. src/lib/store.ts IDeed 타입에 imageUrl?: string 추가 (§4)
4. src/app/add/page.tsx 수정 — 확정 시 uploadDeedPhoto 호출 (§3)
5. src/app/deeds/page.tsx 이미지 썸네일 추가 (§5)
6. pnpm typecheck && pnpm lint && pnpm build

Allowed: L0/L1
Forbidden: push, Supabase 버킷 삭제
Verification: typecheck/lint/build PASS, 업로드 후 deeds에 imageUrl 저장 확인

Report back to: infinity/reports/product-01/{timestamp}.md
```
