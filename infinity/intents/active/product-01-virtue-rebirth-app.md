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
- 사용자 디자인 시스템 후보로 `dev/pt` (purplemux) 의 shadcn/ui base-nova + Tailwind 4 + Pretendard 토큰을 채택 권고. 단, purplemux는 데스크톱 멀티플렉서이므로 신규 모바일 웹앱은 별도 Next.js 프로젝트로 분리하고 토큰/컴포넌트만 차용.

## Artifacts

- `infinity/artifacts/product-01/design.md` — 제품/디자인 기획서 (한국어)

## Next Actions

1. 구현 레포 결정: 신규 `virtue-rebirth-app` 레포를 만들지, `dev/pt` 위 mobile route로 붙일지 사용자 확인.
2. 결정 후 Next.js 15/16 + shadcn/ui base-nova 스캐폴드 + 메인 대시보드 wireframe.
3. AI 채점 모델 선택 (Claude Sonnet 4.6 vision API vs 별도) 및 톤 가이드라인 확정.
4. 환생종 테이블 (브론즈→다이아 식의 단계와 종 매핑) 초안 → 사용자 리뷰.

## Open Questions

- 구현 레포 위치 (신규 vs `dev/pt` 모바일 라우트).
- AI 채점은 클라이언트 직접 호출 vs 자체 백엔드 경유.
- 인증 (개인용 vs 공개). 개인용이면 로그인 생략 가능.
- 데이터 영속화: Supabase / Firebase / 로컬 SQLite + Tailscale.
