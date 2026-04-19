# wiki-02: agent-wiki GitHub Pages 구현

- status: archived
- priority: medium
- permission: L2
- created: 2026-04-18T09:00
- approved_at: 2026-04-18T13:13
- unblocked_at: 2026-04-19T02:40 (`/infinity 승인`)
- completed_at: 2026-04-19T02:45 (initial) / 2026-04-19T03:07 (content navigation fix)
- goal: shdkej/agent-wiki 레포에 Docsify 설정 추가 후 GitHub Pages 활성화
- context: infinity/drafts/agent-wiki-pages-design.md, infinity/drafts/wiki-02-implementation.md, github:shdkej/agent-wiki

## Result (최종 구성)
- shdkej/agent-wiki @ ba2f28a
  - `/index.html` — Docsify 엔트리포인트 (loadSidebar, search depth:3, auto2top)
  - `/_sidebar.md` — 탐색 구조 (Home, 다이어리, Sources, Mapped, 개념, 종합, 유지보수)
  - `/.nojekyll` — Jekyll 변환 비활성화
- GitHub Pages 활성화: `source.path: /` (root) — 초기 `/docs` 구성에서 이동
- 배포 확인 (ba2f28a 기준):
  - https://shdkej.github.io/agent-wiki/ → 200 OK, `<title>Agent Wiki</title>`
  - https://shdkej.github.io/agent-wiki/diary/2026-04-19.md → 200 (raw markdown)
  - https://shdkej.github.io/agent-wiki/_sidebar.md → 200
  - https://shdkej.github.io/agent-wiki/mapped/Fundamental/Architecture.md → 200
  - https://shdkej.github.io/agent-wiki/sources/Fundamental.md → 200

## 진화 경로 (문제 → 원인 → 수정)
1. 445acf6 — `/docs` 아래 Docsify 배포. 사이트는 뜨지만 `diary/` 등 루트 콘텐츠 접근 불가
2. b7a8d27 — index.html을 루트로 이동, `_sidebar.md` 추가
3. Pages source `/docs` → `/` 변경 시 직전 push 빌드가 소스 변경 전에 시작되어 1회 실패. `POST /pages/builds`로 재트리거
4. b255a48 — `.nojekyll` 추가. Jekyll이 `.md`→`.html` 변환하고 `_sidebar.md` 배제해서 Docsify가 raw markdown fetch 실패. Jekyll 끄고 정적 서빙
5. ba2f28a — `_sidebar.md` 확장 (sources 7개 + mapped 10개 하위 폴더 대표 노트)

## Lesson
- `gh api -X POST /repos/{owner}/{repo}/pages -f "source[branch]=main" -f "source[path]=/docs"` 한 줄로 GitHub Pages 활성화 가능. **웹 UI 필수 절차가 아님** — 설계안의 전제 오류
- GitHub MCP 제약은 gh CLI(repo scope)로 우회 가능
- User-level custom domain(shdkej.com)이 있으면 project Pages의 `html_url`이 그 하위 경로로 반환됨
- **Docsify + GitHub Pages 조합의 필수 파일**: `index.html`, `_sidebar.md`, **`.nojekyll`**. .nojekyll 없으면 Jekyll이 `.md`→`.html` 변환 + 언더스코어 파일 배제로 Docsify가 완전히 깨짐. 설계 문서에 빠진 핵심 디테일
- Pages source 변경(PUT)과 소스 코드 push가 거의 동시일 때 과도기 빌드가 1회 실패할 수 있음. `POST /pages/builds`로 재트리거하면 해결
- `_sidebar.md`에 모든 파일 나열은 확장성 부족. 카테고리 개요/대표 노트 수준이 유지 가능. 완전 자동화 필요 시 `ls`로 생성하는 sidebar-gen 스크립트를 diary-sync.sh에 결합 고려

## Next
- diary-sync.sh가 30분 주기로 agent-wiki에 push → 다이어리 파일은 자동 반영
- **단, `_sidebar.md`의 "다이어리" 섹션은 수동 갱신 필요** — 최근 3개 항목만 하드코딩. diary-sync.sh에 sidebar 재생성 로직 추가 시 완전 자동화 가능 (후속 Intent 후보)
- `index.md`는 Obsidian `[[wiki-link]]` 문법이라 Docsify에 그대로 렌더링 안 됨. 점진적으로 markdown link로 마이그레이션하거나 Docsify plugin 추가 고려 (후속 Intent 후보)
