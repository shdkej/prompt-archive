# [pages-01] agent-wiki GitHub Pages 설계 및 구현안

- id: pages-01
- status: archived
- priority: medium
- permission: L0/L1
- created: 2026-04-20
- completed_at: 2026-04-20T00:00
- goal: shdkej/agent-wiki 내용을 공개 웹 뷰어로 배포하는 구조와 작업 순서 설계
- success_criteria:
  - [x] 현실적인 배포 구조 제안 (새 레포 vs 기존 Pages 자산 활용)
  - [x] GitHub Pages 제약 분석
  - [x] 작업 순서 (step-by-step) 제안
  - [x] 구현안 문서 작성
- context: shdkej/agent-wiki (GitHub 레포), shdkej/prompt-archive

## result

- 산출물:
  - 설계 리포트: `infinity/reports/pages-01/2026-04-20T00-00.md`
  - 구현안 초안: `infinity/drafts/agent-wiki-pages-plan.md`
- 추천 방안: Option A — agent-wiki 레포에 MkDocs-Material + GitHub Actions 직접 활성화
- 배포 후 URL: `https://shdkej.github.io/agent-wiki/`
- 사용자 직접 수행 필요: GitHub Pages 활성화 (Settings → Pages → Source: GitHub Actions)

## lesson

- MkDocs Material + `docs_dir: diary` 설정으로 기존 diary/ 구조 변경 없이 웹 뷰어 구축 가능
- diary-sync.sh push → GitHub Actions 자동 트리거로 별도 배포 단계 불필요
- GitHub Pages 활성화는 웹 UI 필수 → Agent가 자동화할 수 없는 L3 작업
