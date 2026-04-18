# wiki-01: agent-wiki GitHub Pages 배포 구조 설계

- status: archived
- priority: medium
- permission: L1
- created: 2026-04-18T06:13
- completed_at: 2026-04-18T06:13
- goal: shdkej/agent-wiki 내용을 GitHub Pages로 공개하는 현실적인 배포 구조 설계
- context: infinity/drafts/agent-wiki-pages-design.md, github:shdkej/agent-wiki

## Result
- 3가지 배포 옵션 분석 완료 (직접 Pages / shdkej.github.io 통합 / Docsify)
- 권장 구조: Docsify + agent-wiki 레포 직접 Pages 활성화
- 구현 체크리스트 및 코드 예시 포함 설계안 작성
- 산출물: infinity/drafts/agent-wiki-pages-design.md

## Lesson
- Docsify는 빌드 없이 마크다운을 직접 렌더링해 GitHub Actions 없이도 배포 가능
- diary-sync와 완전 자동화 파이프라인 연결 시 별도 작업 없음
- 구현 단계(agent-wiki push)는 L2 권한 필요 → 별도 Intent로 진행 권장

## Next
- 실제 구현은 사용자 요청 시 wiki-02 Intent 등록
- shdkej/agent-wiki에 docs/index.html 추가 + GitHub Pages 활성화
