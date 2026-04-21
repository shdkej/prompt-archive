# wiki-01: agent-wiki GitHub Pages 배포 구조 설계

## 2026-04-18 처리 (1차)

- status: archived
- priority: medium
- permission: L1
- completed_at: 2026-04-18T06:13
- goal: shdkej/agent-wiki 내용을 GitHub Pages로 공개하는 현실적인 배포 구조 설계
- context: infinity/drafts/agent-wiki-pages-design.md, github:shdkej/agent-wiki

### Result
- 3가지 배포 옵션 분석 완료 (직접 Pages / shdkej.github.io 통합 / Docsify)
- 권장 구조: Docsify + agent-wiki 레포 직접 Pages 활성화
- 구현 체크리스트 및 코드 예시 포함 설계안 작성
- 산출물: infinity/drafts/agent-wiki-pages-design.md

### Lesson
- Docsify는 빌드 없이 마크다운을 직접 렌더링해 GitHub Actions 없이도 배포 가능
- diary-sync와 완전 자동화 파이프라인 연결 시 별도 작업 없음
- 구현 단계(agent-wiki push)는 L2 권한 필요 → 별도 Intent로 진행 권장

### Next (from 1차)
- 실제 구현은 사용자 요청 시 wiki-02 Intent 등록
- shdkej/agent-wiki에 docs/index.html 추가 + GitHub Pages 활성화

---

## 2026-04-21 처리 (2차 - Inbox 재요청)

- status: completed
- priority: medium
- permission: L0
- completed_at: 2026-04-21T00:00
- goal: agent-wiki 콘텐츠를 공개 웹 뷰어로 제공하기 위한 GitHub Pages 배포 구조 및 작업 순서 제안
- success_criteria:
  - 새 GitHub Pages 레포/브랜치 방향 검토 (우선)
  - 기존 Pages 자산 활용 대안 포함
  - 가장 현실적인 배포 구조와 작업 순서를 문서로 작성
- context: infinity/drafts/wiki-01-github-pages-plan.md
- project: wiki

### Result
- infinity/drafts/wiki-01-github-pages-plan.md 작성 완료
- prompt-archive 레포 현황 확인 (Pages 미설정, main 브랜치만)
- 옵션 A(기존 prompt-archive 레포 활용)를 권장안으로 제시 (Reuse Before Create 원칙)
- agent-wiki/ 디렉토리 없음 확인 → 신규 생성 필요
- 단계별 작업 순서 포함

### Lesson
- 레포 현황 확인 선행이 중요 (Pages 설정 여부, 브랜치 현황)
- agent-wiki가 별도 레포(shdkej/agent-wiki)로 존재 가능 → 다음 요청 시 확인 필요
- 사용자는 GitHub UI에서 Pages 활성화만 하면 됨 (최소 수동 작업)
