# product-01 인증 전략 분석

## 결론 (권장)

**MVP: 인증 없음 (개인용 단일 사용자)**

이후 공개 전환 시: **Clerk + Next.js 15 App Router**

---

## 시나리오별 비교

| 시나리오 | 난이도 | 기간 | 권장 방식 | 비고 |
|----------|--------|------|-----------|------|
| 개인용 (로그인 없음) | ✅ 없음 | 0h | — | MVP 즉시 사용 가능 |
| 개인용 (간단 PIN) | 낮음 | 2h | 환경변수 비교 | 외부 노출 시 최소 보안 |
| 공개 소셜 로그인 | 중간 | 4-6h | Clerk | App Router 공식 지원 |
| 공개 이메일+비번 | 중간 | 8h+ | NextAuth v5 | 설정 복잡, MVP에 과함 |

---

## MVP 결정: 인증 없음

MVP 단계에서는 인증 제거를 강권함:
- `개인용`으로 사용하면 로그인 불필요
- 데이터는 localStorage (이미 구현됨)
- 배포 시 URL 비공개로 운영

**추가 보안이 필요하다면**: Nginx에서 Basic Auth 한 줄로 처리
```nginx
auth_basic "덕 쌓기";
auth_basic_user_file /etc/nginx/.htpasswd;
```

---

## 공개 전환 시: Clerk 권장

### 왜 Clerk인가?

- Next.js 15 App Router 공식 지원 (`@clerk/nextjs` v6)
- Server Component에서 `auth()` 직접 호출 가능
- `middleware.ts` 한 파일로 라우트 보호
- 소셜 로그인 (Google/Kakao) 기본 제공
- 무료 플랜: MAU 10,000명

### 최소 통합 코드

```bash
pnpm add @clerk/nextjs
```

```ts
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
const isProtected = createRouteMatcher(["/(.*)"]];
export default clerkMiddleware((auth, req) => {
  if (isProtected(req)) auth().protect();
});
```

```ts
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";
export default function RootLayout({ children }) {
  return <ClerkProvider>{children}</ClerkProvider>;
}
```

```tsx
// 어디서든 사용자 정보
import { auth, currentUser } from "@clerk/nextjs/server";
const { userId } = await auth(); // Server Component / Route Handler
```

### Supabase 연동 시 userId 활용

Supabase 영속화와 Clerk을 연동하면 `userId`를 Row Level Security 키로 사용:
```sql
-- RLS 정책
CREATE POLICY "사용자 본인 데이터만" ON deeds
  USING (auth_user_id = current_setting('app.user_id'));
```

Route Handler에서:
```ts
const { userId } = await auth();
supabase.rpc('set_user_id', { user_id: userId });
```

---

## 로컬 실행 프롬프트 (Clerk 도입 시)

```
Infinity Intent: product-01 auth
Mode: execute_local
Required workflow: Use workflow-master first.
Goal: Clerk 소셜 로그인 도입 (Google + Kakao)
Context: /home/ubuntu/dev/virtue-rebirth-app (Next.js 15 App Router)
Steps:
  1. pnpm add @clerk/nextjs
  2. .env.local에 NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY 추가
  3. middleware.ts 생성 (전체 라우트 보호)
  4. app/layout.tsx에 ClerkProvider 래핑
  5. 기존 mock userId를 auth().userId로 교체
  6. SignIn/SignUp 페이지: app/sign-in/[[...sign-in]]/page.tsx
Verification: pnpm typecheck && pnpm build 통과
Report back to: infinity/reports/product-01/{timestamp}.md
```

---

## 권장 실행 순서

```
현재 MVP (인증 없음)
    ↓ 공개 전환 결정 시
Clerk 도입 (4-6h)
    ↓
Supabase RLS에 userId 연동
```

## 결론 재확인

1. **지금은 인증 생략** — MVP를 빠르게 사용하고 피드백 수집
2. **공개 전환 결정 시** — `auth-guide.md`의 Clerk 프롬프트 사용
3. **Nginx Basic Auth** — 배포 후 즉시 최소 보안 적용 가능 (5분)
