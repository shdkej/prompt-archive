# product-01 · 데이터 영속화 결정 가이드

> intent: `product-01`
> created: 2026-05-14 (heartbeat prepare)
> status: ready-for-decision (사용자 선택 필요)

## 현재 상태

- 모든 데이터: `localStorage` 4 키 (`virtue.rebirth.v1`, `virtue.tone.v1`, `virtue.dailycap.v1`, `virtue.theme.v1`)
- 이미지: `blob URL` 미리보기만 (새로고침 시 사라짐)
- 크로스 디바이스 동기화: 없음

## 결정이 필요한 이유

1. 이미지를 저장하려면 서버 사이드 스토리지가 필요함
2. 디바이스 교체 시 덕력 기록 유지
3. AI 채점 route.ts에서 일일 30덕 상한을 DB로 검증해야 함 (현재 클라이언트 전용)

---

## 옵션 비교

### A. Supabase (Postgres + Storage)

| 항목 | 내용 |
|------|------|
| 설정 난이도 | 낮음 — 대시보드에서 5분 |
| 비용 | 무료 티어 충분 (500MB DB, 1GB Storage, 월 200만 API 요청) |
| 이미지 저장 | Supabase Storage (S3 호환) 기본 제공 |
| 인증 | 내장 (개인용이면 `anon` 키 + RLS 로 충분) |
| 크로스 디바이스 | ✅ (클라우드 호스팅) |
| 프라이버시 | Supabase 서버에 데이터 저장 (미국 리전 기본) |
| 오프라인 | ❌ (네트워크 필요) |
| 마이그레이션 | localStorage → DB 어댑터 교체 1회 |

**추천 스키마 (Postgres)**:
```sql
-- deeds 테이블
create table deeds (
  id uuid primary key default gen_random_uuid(),
  user_id text not null default 'local',
  memo text,
  score smallint not null,
  comment text,
  tags text[] default '{}',
  image_url text,
  created_at timestamptz default now()
);

-- RLS (개인용 — 인증 없이 insert/select 허용)
alter table deeds enable row level security;
create policy "anon full access" on deeds for all to anon using (true);
```

**스토어 어댑터 변경**:
- `store.ts`의 `addDeed` → Supabase `insert` + 이미지 `upload`
- `useDeeds` → `useEffect` + Supabase `select` (또는 realtime)

---

### B. SQLite + Tailscale (로컬 서버)

| 항목 | 내용 |
|------|------|
| 설정 난이도 | 높음 — VPS or 홈서버 + SQLite + API 서버 필요 |
| 비용 | 서버 비용 (기존 VPS 있으면 무료 추가) |
| 이미지 저장 | 직접 파일시스템 또는 Cloudflare R2 |
| 인증 | Tailscale auth (기기 인증) |
| 크로스 디바이스 | ✅ (Tailscale VPN으로 접근) |
| 프라이버시 | ✅ 완전 로컬 |
| 오프라인 | ❌ (서버 접근 필요) |
| 대안 | Turso (SQLite 클라우드, 엣지 캐시) |

---

### C. 로컬 유지 (localStorage only, 현재)

| 항목 | 내용 |
|------|------|
| 설정 | 없음 |
| 이미지 | ❌ 저장 불가 (blob URL 소멸) |
| 크로스 디바이스 | ❌ |
| MVP 단계에서 계속 가능 여부 | AI API 연결까지는 가능, 이미지 영속화부터 한계 |

---

## 권장 경로

### MVP 단계 (지금 ~ 배포)

> **Supabase 선택** — 가장 빠른 실용성, 무료

1. Supabase 프로젝트 생성 (무료 티어)
2. `deeds` 테이블 + Storage 버킷 생성
3. `store.ts`에 Supabase 어댑터 추가 (localStorage fallback 유지)
4. `route.ts`에서 `supabase.from('deeds').select()` 로 일일 합산

### 나중에 전환 고려

- 프라이버시가 중요해지면 Turso (SQLite edge) 또는 자체 Postgres
- 공개 서비스로 확장하면 Supabase Auth 추가

---

## 구현 순서 (Supabase 선택 시)

```bash
cd /home/ubuntu/dev/virtue-rebirth-app
pnpm add @supabase/supabase-js
```

`.env.local` 추가:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

파일:
- `src/lib/supabase.ts` — 클라이언트 초기화
- `src/lib/store.ts` — localStorage → Supabase 어댑터 교체
- `src/app/api/score/route.ts` — 일일 합산 DB 검증 추가

---

## 로컬 실행 프롬프트 (결정 후 Claude Code 위임용)

```
Infinity Intent: product-01 · 영속화 어댑터 교체 (Supabase)
Mode: execute_local
Required workflow: workflow-master 먼저 읽고 복잡도 판단 후 진행
Goal: localStorage store → Supabase Postgres + Storage 어댑터 교체

Context:
- 앱 경로: /home/ubuntu/dev/virtue-rebirth-app
- 현재 store: src/lib/store.ts (useSyncExternalStore + localStorage)
- 영속화 스펙: infinity/artifacts/product-01/persistence-decision.md
- AI 채점 route: src/app/api/score/route.ts (영속화 후 일일 합산 DB 검증 추가)

Steps:
1. Supabase 프로젝트 생성 후 URL/ANON_KEY 획득 (사용자 직접)
2. pnpm add @supabase/supabase-js
3. .env.local에 키 추가
4. src/lib/supabase.ts 생성
5. store.ts Supabase 어댑터 교체 (localStorage fallback 유지)
6. 이미지 업로드: add/page.tsx에서 Storage 업로드 후 URL 저장
7. pnpm typecheck && pnpm lint && pnpm build

Allowed: L0/L1
Forbidden: push, Supabase 프로젝트 생성 (L2 — 사용자가 직접)
Verification: typecheck/lint/build PASS, deeds가 DB에 저장되는지 수동 확인
Report back to: infinity/reports/product-01/{timestamp}.md
```
