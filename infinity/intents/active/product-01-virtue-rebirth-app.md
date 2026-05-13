# [product-01] 덕 쌓기 · 환생 모바일 웹앱 기획

- id: product-01
- status: in_progress
- priority: medium
- permission: L1 (prompt-archive 내 산출물 작성), 구현 레포는 별도 확인 필요
- project: virtue-rebirth-app
- created: 2026-05-13

## Goal

드라마 *Brush Up Life* 컨셉을 차용한 "덕을 쌓는 모바일 웹앱" 기획. 사용자가 선행을 한 뒤 인증 사진을 올리면 AI가 `덕력`을 채점하고, 누적된 덕력에 따라 **환생종**이 진화하는 가벼운 라이프 게임.

## Current State

- 제품 컨셉 / IA / 메인 화면 / AI 채점 UX / 환생종 진행 / 데이터 모델 / MVP 범위를 `infinity/artifacts/product-01/design.md`에 정리.
- **2026-05-13**: 사용자가 "신규 레포 분리" 옵션을 선택. 로컬 경로 `/home/ubuntu/dev/virtue-rebirth-app`에 Next.js 15 + App Router + Tailwind v4 + TS 스캐폴드 완료 (mock 데이터 기반 5탭 모바일 MVP). `dev/pt`의 OKLCH 토큰과 Pretendard 폰트를 차용. 로컬 git 초기 커밋만, push 없음.
- 구현 산출물 메모: `infinity/artifacts/product-01/implementation.md`.

## Artifacts

- `infinity/artifacts/product-01/design.md` — 제품/디자인 기획서 (한국어)
- `infinity/artifacts/product-01/implementation.md` — 스캐폴드 구현 메모 (경로/파일/검증 결과)

## Next Actions

1. mock 채점을 진짜 Claude Sonnet 4.6 vision API로 교체 (zod 스키마 강제, §5 톤 가이드 적용).
2. 영속화 결정: Supabase vs 로컬 SQLite + Tailscale. 개인용이면 후자 가벼움.
3. shadcn/ui base-nova `Drawer`/`Sheet`를 도입해 업로드 흐름을 모달 UX로 통일.
4. 다크 모드 실제 적용 (현재는 토글 UI만).
5. 배포 결정 — Vercel vs `virtue.oracle.shdkej.com`.

## Open Questions

- 구현 레포 위치 (신규 vs `dev/pt` 모바일 라우트).
- AI 채점은 클라이언트 직접 호출 vs 자체 백엔드 경유.
- 인증 (개인용 vs 공개). 개인용이면 로그인 생략 가능.
- 데이터 영속화: Supabase / Firebase / 로컬 SQLite + Tailscale.
