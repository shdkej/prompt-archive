# agent-wiki GitHub Pages 구현안

> 작성일: 2026-04-20 | Intent: pages-01
> 목표: `shdkej/agent-wiki` 내용을 공개 웹으로 볼 수 있는 배포 구조 설계

---

## 현황 파악

### agent-wiki 레포 구조 (확인된 사항)
- **레포**: `shdkej/agent-wiki` (GitHub 공개 레포)
- **주요 디렉토리**: `diary/YYYY-MM-DD.md` — 30분마다 자동 커밋
- **자동화**: `diary-sync.sh`가 로컬 → GitHub 자동 push

### GitHub Pages 제약
- 사용자 계정(`shdkej`)당 **`shdkej.github.io`** 레포 1개만 user/org Pages 가능
- 프로젝트 Pages는 각 레포마다 별도 활성화 가능 (`shdkej.github.io/agent-wiki/`)
- 제약 여부에 따라 2가지 경로 검토

---

## 방안 A: agent-wiki 레포에 직접 Pages 활성화 (권장)

### 구조
```
shdkej/agent-wiki
├── diary/
│   ├── 2026-04-20.md
│   └── ...
├── docs/                  ← (신규) MkDocs 소스 or Jekyll 루트
│   └── index.md
├── mkdocs.yml             ← (신규) MkDocs 설정
└── .github/
    └── workflows/
        └── pages.yml      ← (신규) GitHub Actions 배포
```

### 배포 URL
`https://shdkej.github.io/agent-wiki/`

### 장점
- 별도 레포 불필요
- diary 파일과 같은 레포에서 관리
- 자동 배포 (push → build → Pages)

### 구현 단계

#### 1단계: MkDocs 설정 파일 추가
```yaml
# mkdocs.yml
site_name: Agent Wiki
site_url: https://shdkej.github.io/agent-wiki/
docs_dir: diary
nav:
  - Home: index.md
theme:
  name: material
  palette:
    primary: indigo
plugins:
  - search
  - blog:
      blog_dir: .
```

> ⚠️ diary/ 디렉토리를 docs로 직접 사용하므로 별도 복사 불필요

#### 2단계: GitHub Actions 워크플로우
```yaml
# .github/workflows/pages.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
    paths:
      - 'diary/**'
      - 'mkdocs.yml'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install mkdocs-material
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    needs: build
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

#### 3단계: GitHub 레포 설정
1. `agent-wiki` 레포 → Settings → Pages
2. Source: **GitHub Actions** 선택 (branch 방식 아님)
3. 첫 push 후 자동 배포 확인

---

## 방안 B: 기존 Pages 제약 시 — shdkej.github.io에 서브디렉토리 추가

### 구조
```
shdkej/shdkej.github.io   ← 이미 존재하는 user Pages 레포
└── agent-wiki/            ← agent-wiki 컨텐츠를 여기에 추가
    ├── diary/
    └── index.html
```

### 구현 방법: Git Submodule 방식
```bash
# shdkej.github.io 레포에서
git submodule add https://github.com/shdkej/agent-wiki agent-wiki-src

# GitHub Actions에서 submodule 포함 빌드
```

### 단점
- 두 레포 동기화 관리 필요
- diary-sync.sh 수정 필요 (추가 push 트리거)
- 더 복잡한 CI/CD 설정

---

## 방안 C: 독립 레포 + GitHub Pages (최소 변경)

```
shdkej/agent-wiki-site     ← 신규 레포 (Pages 전용)
```

- agent-wiki 레포의 diary/ 파일을 GitHub Actions로 자동 복사
- 완전히 분리된 구조, 그러나 레포 수 증가

---

## 권장 결론

**방안 A (agent-wiki 직접 활성화)** 가 가장 현실적:

| 기준 | 방안 A | 방안 B | 방안 C |
|------|--------|--------|--------|
| 구현 복잡도 | 낮음 | 높음 | 중간 |
| 레포 추가 여부 | 없음 | 없음 | 있음 |
| 유지보수 | 쉬움 | 복잡 | 중간 |
| 기존 시스템 영향 | 없음 | 있음 | 없음 |

---

## 작업 순서 (방안 A 기준)

- [ ] 1. `shdkej/agent-wiki` 레포에 `mkdocs.yml` 추가
- [ ] 2. `.github/workflows/pages.yml` 추가
- [ ] 3. GitHub 레포 Settings → Pages → Source: GitHub Actions 변경
- [ ] 4. diary/ 중 index.md 없으면 간단한 `index.md` 추가
- [ ] 5. 첫 push 후 빌드 로그 확인
- [ ] 6. `https://shdkej.github.io/agent-wiki/` 접속 확인

**예상 소요 시간**: 30분~1시간

---

## 주의사항

- `mkdocs-material` 테마가 가장 Markdown 친화적 (설치: `pip install mkdocs-material`)
- diary/ 파일명이 YYYY-MM-DD.md 형식 → MkDocs nav 자동 인식 잘됨
- diary-sync.sh는 수정 불필요 (agent-wiki 레포 push 시 Pages 자동 트리거)
- Private 레포는 GitHub Pages 무료 플랜에서 공개 불가 (공개 레포 확인 필요)
