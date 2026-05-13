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

- 사용자 피드백: 2026-05-13 초안 방향 승인. "마음에 들어, 디벨롭 해보자."

- 제품 컨셉 / IA / 메인 화면 / AI 채점 UX / 환생종 진행 / 데이터 모델 / MVP 범위를 `infinity/artifacts/product-01/design.md`에 정리.
- **2026-05-13**: 사용자가 "신규 레포 분리" 옵션을 선택. 로컬 경로 `/home/ubuntu/dev/virtue-rebirth-app`에 Next.js 15 + App Router + Tailwind v4 + TS 스캐폴드 완료. `dev/pt`의 OKLCH 토큰과 Pretendard 폰트를 차용.
- **2026-05-14**: MVP 디벨롭 1회차 완료. `useSyncExternalStore` + localStorage 자체 store, 50+ 코멘트의 톤(soft/casual) 채점, 11단계 환생종 + 진화 시 `LevelUpSheet`, 일일 30덕 차단, 재채점 3회 제한, 카피 톤 가이드 적용, 글로벌 토스트, JSON 내보내기/기록 초기화 실작동. `pnpm typecheck/lint/build` 모두 통과. 로컬 git `6ba58a8`까지, push 없음.
- 구현 산출물 메모: `infinity/artifacts/product-01/implementation.md`.
- 리포트: `infinity/reports/product-01/2026-05-14T00-50.md` (+ 5 페이지 스크린샷 폴더).

## Artifacts

- `infinity/artifacts/product-01/design.md` — 제품/디자인 기획서 (한국어)
- `infinity/artifacts/product-01/implementation.md` — 디벨롭 후 구현 메모
- `infinity/artifacts/product-01/ai-scoring-prompt.md` — 채점 시스템 프롬프트 초안
- `infinity/artifacts/product-01/score-api-implementation.md` — AI 채점 route.ts + prompt caching + 로컬 실행 프롬프트
- `infinity/artifacts/product-01/ai-scoring-route-complete.md` — AI 채점 route.ts (extractJson 방어 버전)
- `infinity/artifacts/product-01/persistence-decision.md` — Supabase 영속화 스펙 + 로컬 실행 프롬프트
- `infinity/artifacts/product-01/shadcn-integration.md` — Drawer 단독 도입 분석 + 로컬 실행 프롬프트
- `infinity/artifacts/product-01/deployment-guide.md` — oracle 서버 배포 가이드
- `infinity/artifacts/product-01/photo-storage-guide.md` — Supabase Storage 사진 영속화 + 로컬 실행 프롬프트
- `infinity/reports/product-01/2026-05-14T00-50.md` — 디벨롭 세션 리포트

## Next Actions (로컬 실행 순서)

1. **[선결]** `.env.local`에 `ANTHROPIC_API_KEY` 설정 (사용자 직접)
2. **(우선)** AI 채점 API 연결: `score-api-implementation.md` §8 프롬프트 → Claude Code
3. **[선결]** Supabase 프로젝트 생성 + URL/ANON_KEY 획득 (사용자 직접, L2)
4. 영속화 어댑터 교체: `persistence-decision.md` 로컬 실행 프롬프트 → Claude Code
5. 사진 영속화: `photo-storage-guide.md` §9 프롬프트 → Claude Code
6. Drawer 도입: `shadcn-integration.md` 로컬 실행 프롬프트 → Claude Code
7. 사용자 컨펌 시 GitHub origin + 첫 push (L2)
8. oracle 서버 배포: `deployment-guide.md` 참조

## Open Questions

- 구현 레포 위치 (신규 vs `dev/pt` 모바일 라우트).
- AI 채점은 클라이언트 직접 호출 vs 자체 백엔드 경유.
- 인증 (개인용 vs 공개). 개인용이면 로그인 생략 가능.
- 데이터 영속화: Supabase / Firebase / 로컬 SQLite + Tailscale.
