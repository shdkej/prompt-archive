# [product-01] 덕 쌓기 · 환생 모바일 웹앱 기획

- id: product-01
- status: archived
- priority: medium
- permission: L1 (prompt-archive 내 산출물 작성)
- project: virtue-rebirth-app
- repo: https://github.com/shdkej/virtue-rebirth-app
- local_repo: /home/ubuntu/dev/virtue-rebirth-app
- deployment: https://virtue.oracle.shdkej.com
- created: 2026-05-13
- completed_at: 2026-05-15T11:44Z

## Goal

드라마 *Brush Up Life* 컨셉을 차용한 "덕을 쌓는 모바일 웹앱" 기획. 사용자가 선행을 한 뒤 인증 사진을 올리면 AI가 `덕력`을 채점하고, 누적된 덕력에 따라 **환생종**이 진화하는 가벼운 라이프 게임.

## Current State

- 사용자 피드백: 2026-05-13 초안 방향 승인. "마음에 들어, 디벨롭 해보자."
- 제품 컨셉 / IA / 메인 화면 / AI 채점 UX / 환생종 진행 / 데이터 모델 / MVP 범위는 `infinity/artifacts/product-01/design.md`에 정리.
- **구현 레포 확정**: `/home/ubuntu/dev/virtue-rebirth-app` (Next.js 15 + App Router + Tailwind v4 + TS). GitHub origin = `https://github.com/shdkej/virtue-rebirth-app`, `master` ↔ `origin/master` 동기.
- **배포 완료**: `https://virtue.oracle.shdkej.com` 공개 (HTTP 200, title `덕 쌓기 · 환생`). 인프라는 `space` 레포의 `ff7e1ab` (deploy virtue rebirth app), `da46a90` (fix pod startup path) 적용.
- **현재 운영 모드**: 채점은 mock 고정 (`2217c27` "배포 기본값을 mock 채점으로 고정", `NEXT_PUBLIC_SCORING_MODE=mock`). 영속화는 localStorage(자체 store, `useSyncExternalStore`). 사진 외부 저장 없음 (기기 메모리에만 머묾).
- **AI 채점 코드 경로 존재 (현재는 비활성)**: `/api/score` route + Claude Sonnet 4.6 vision 호출 경로 구현 완료. 다만 2026-05-15 사용자 결정으로 실제 AI 채점 활성화 후보는 **Gemini Vision 계열로 전환**한다. 운영 빌드는 여전히 mock 모드라 이 분기는 실사용에서 타지 않음.
- MVP 디벨롭 1회차 완료 (2026-05-14): 50+ 코멘트 톤(soft/casual) 채점, 11단계 환생종 + 진화 시 `LevelUpSheet`, 일일 30덕 차단, 재채점 3회 제한, 글로벌 토스트, JSON 내보내기/기록 초기화 실작동. `pnpm typecheck/lint/build` 모두 통과.
- 가장 최근 검증: `2026-05-14T17-07-followup.md` — 로컬 미커밋 UX/code-quality 배치 기준 typecheck/lint/build PASS, 5 페이지 HTTP 200. `format.ts` 고정 mock 시간 제거 + Next 16 lint 경로 복구.
- **2026-05-15T10-13 사용자 확인 후 push 완료**: UX 개선 배치 11개 파일 + `.gitignore`(design-mockups 제외)를 단일 커밋 `dfaaf4e`(`UX 개선 배치 정리 및 목업 제외`)로 묶고, `origin/master`에 push 완료. typecheck/lint/build 모두 PASS. `design-mockups/`은 `.gitignore` 19행에 등재되어 영구 untracked-ignored. 배포 확인은 별도 사이클. 상세는 `infinity/reports/product-01/2026-05-15T09-11-user-decision-commit.md`.
- **2026-05-15 완료 처리**: 사용자 확인 기준 Virtue는 더 배포할 항목 없이 최신 상태로 간주한다. `product-01`은 여기서 완료/아카이브하고, 이후 UX 개선·Gemini 채점 전환·영속화 등은 별도 Intent로 분리한다.
- 운영 결정 (2026-05-14, 사용자 확정):
  - 배포: 완료.
  - 외부 사진/스토리지: 도입 안 함, 나중에 재검토.
  - AI 채점: 당분간 mock 유지. 활성화 시 Claude Vision이 아니라 **Gemini 기준으로 재구현/전환**.
  - 도메인: `virtue.oracle.shdkej.com`.

## Artifacts

- `infinity/artifacts/product-01/design.md` — 제품/디자인 기획서 (한국어)
- `infinity/artifacts/product-01/implementation.md` — 디벨롭 후 구현 메모
- `infinity/artifacts/product-01/ai-scoring-prompt.md` — 채점 시스템 프롬프트 초안
- `infinity/artifacts/product-01/score-api-implementation.md` — AI 채점 route.ts + prompt caching + 로컬 실행 프롬프트
- `infinity/artifacts/product-01/ai-scoring-route-complete.md` — AI 채점 route.ts (extractJson 방어 버전)
- `infinity/artifacts/product-01/ai-scoring-route-final.md` — AI 채점 route 최종형
- `infinity/artifacts/product-01/persistence-decision.md` — Supabase 영속화 스펙 (현재 보류)
- `infinity/artifacts/product-01/photo-storage-guide.md` — Supabase Storage 사진 영속화 (현재 보류)
- `infinity/artifacts/product-01/shadcn-integration.md` — Drawer 단독 도입 분석 (현재 보류)
- `infinity/artifacts/product-01/deployment-guide.md` — oracle 서버 배포 가이드 (적용 완료)
- `infinity/artifacts/product-01/ux-improvement-guide.md` — UX 개선 가이드
- `infinity/reports/product-01/2026-05-14T00-50.md` — 디벨롭 세션 리포트
- `infinity/reports/product-01/2026-05-13T22-07-vision-api.md` — Vision API 통합 리포트
- `infinity/reports/product-01/2026-05-13T23-07-fallback-ux.md` — 키 미설정 폴백 UX 리포트
- `infinity/reports/product-01/2026-05-14T11-07-local-verification.md` — 로컬 검증 게이트 리포트 (typecheck/lint/build/HTTP)
- `infinity/reports/product-01/2026-05-14T13-07-mobile-ux.md` — 모바일 UX 마찰점 분석 리포트
- `infinity/reports/product-01/2026-05-14T15-07-ux-fixes.md` — no-approval UX fix 로컬 적용 리포트
- `infinity/reports/product-01/2026-05-14T17-07-followup.md` — format 고정 시간 제거 + Next 16 lint 복구 후속 리포트
- `infinity/reports/product-01/2026-05-15T09-11-user-decision-commit.md` — 사용자 결정 기반 UX 배치 단일 커밋(`dfaaf4e`) + design-mockups ignore 처리 리포트

## Deferred Follow-up Candidates

이 Intent에서는 더 실행하지 않는다. 아래 항목은 사용자가 별도 작업으로 요청할 때 새 Intent로 분리한다.

1. **실기기/실사용 UX 패스**: `https://virtue.oracle.shdkej.com`을 실제 모바일에서 써보며 add 흐름·결과 카드·도감·덕행록 마찰점 기록.
2. **add 플로우 카피/마찰 조정**: 카피 어색함·버튼 위치·재채점 안내 등 작은 마찰 수정.
3. **외부 사진/데이터 영속화**: localStorage + 사진 미저장 운영을 유지하다가 필요성이 생기면 재검토.
4. **Gemini 기반 AI 채점 전환**: mock 한계가 분명해질 때 별도 Intent로 기존 Claude Vision route를 Gemini Vision 계열로 전환.
5. **UI 폴리시**: 필요가 보일 때만 shadcn Drawer 도입 또는 도감/덕행록 디테일 개선.

## Closed / Deferred Questions

구현 레포 위치, 배포 여부, 도메인, 채점 호출 위치는 이 Intent 기준으로 확정/종료한다. 남은 항목은 모두 후속 Intent 후보로만 유지한다.

- **외부 사진/데이터 영속화 도입 시점**: 사용 데이터가 어느 정도 쌓이고 사용자 본인이 멀티 디바이스/유실 우려를 실제로 느낄 때 결정. 현재는 보류.
- **Gemini AI 채점 활성화 트리거**: mock 코멘트의 한계가 실사용 중 분명하게 느껴질 때 켠다. Gemini 키 주입과 운영 모드 전환의 운영 리스크는 별도 결정 필요.
- **공개/비공개 운영 범위**: 현재 사실상 개인용 공개 URL. 친구 공유·인증·피드 도입 여부는 후속 의사결정.
