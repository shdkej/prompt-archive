# GitHub Pages 배포 구조 설계 - agent-wiki

> Intent: wiki-01 | 작성: 2026-04-18 | 상태: 설계안 완료
> `shdkej/agent-wiki` 마크다운 콘텐츠를 공개 웹 뷰어로 배포하는 구조 설계

---

## 1. 현황 분석

### 1.1 agent-wiki 구조
- **저장소**: `shdkej/agent-wiki` (GitHub)
- **콘텐츠**: 마크다운 파일들 (diary 디렉토리 중심)
- **생성 방식**: `diary-sync.sh` 스크립트로 30분 주기 자동 생성/업데이트
- **현재 상태**: 마크다운 원본 저장 전용, 공개 웹 뷰어 없음

### 1.2 diary-sync 파이프라인
```
로컬 세션 노트 → claude -p 정제 → agent-wiki/diary/YYYY-MM-DD.md → git push
```
- 출력 경로: `~/workspace/agent-wiki/diary/`
- 자동 커밋 & 푸시: 30분 주기

### 1.3 요구사항
- 마크다운을 읽기 좋은 HTML로 자동 변환
- 자동 배포 (diary 업데이트 시 자동 반영)
- 유지보수 최소화

---

## 2. 배포 옵션 분석

### 옵션 A: agent-wiki 레포에 직접 GitHub Pages 활성화 ⭐ 권장

#### 구조
```
shdkej/agent-wiki/
├── diary/                         # 마크다운 원본 (diary-sync.sh로 생성)
├── docs/
│   └── index.md                   # 홈페이지
├── mkdocs.yml                     # MkDocs 설정
└── .github/
    └── workflows/
        └── deploy-pages.yml       # 자동 배포 워크플로우
```

#### 자동화 흐름
```
diary-sync.sh (30분 마다)
    ↓
main 브랜치 push
    ↓
GitHub Actions 자동 트리거
    ↓
mkdocs build (마크다운 → HTML)
    ↓
GitHub Pages 자동 배포
    ↓
https://shdkej.github.io/agent-wiki/ (공개 접속)
```

#### 장점
- **단순성**: 추가 레포/동기화 스크립트 불필요
- **일관성**: 원본과 배포가 같은 레포에 위치
- **완전 자동화**: diary-sync 후 수동 작업 없음
- **독립성**: 다른 Pages 레포와 URL 충돌 없음

#### 단점
- HTML 빌드 산출물이 Git 이력에 포함 (gh-pages 브랜치로 분리 시 해결 가능)

---

### 옵션 B: shdkej.github.io에 서브디렉토리로 통합

#### 구조
```
shdkej.github.io/
├── index.html                     # 기존 Pages 홈
├── agent-wiki/                    # 서브디렉토리로 추가
│   ├── index.html
│   └── diary/
└── ...
```

#### 장점
- 기존 Pages 인프라 재사용 (Reuse Before Create)
- 개인 사이트와 통합 관리

#### 단점
- 레포 간 동기화 스크립트 필요 (추가 복잡성)
- Personal Access Token 관리 필요
- 두 레포 간 의존성 발생

---

### 옵션 C: Docsify (빌드 불필요, 더 가벼움)

별도 빌드 없이 마크다운을 브라우저에서 직접 렌더링:

```html
<!-- docs/index.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Agent Wiki</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      repo: 'shdkej/agent-wiki',
      loadSidebar: true,
      subMaxLevel: 2,
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4"></script>
</body>
</html>
```

#### 장점
- **빌드 단계 없음**: index.html 하나로 동작
- **GitHub Actions 불필요**: Pages 활성화 + index.html만 추가
- **즉각 반영**: push 후 CDN 캐시 시간 내 반영

#### 단점
- JavaScript 의존성 (CDN 다운 시 문제)
- 검색 기능 제한적

---

## 3. 권장 옵션: A + Docsify 조합

### 이유
- **옵션 A의 구조** + **옵션 C(Docsify)의 단순성** 결합
- GitHub Actions 없이 `docs/index.html` 하나로 배포 가능
- diary-sync push → Pages 즉시 반영 (빌드 대기 없음)

### 구현 작업 순서

#### 1단계: agent-wiki 로컬에서 Docsify 설정 추가
```bash
cd ~/workspace/agent-wiki

# docs 디렉토리 생성 및 index.html 추가
mkdir -p docs
cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Agent Wiki</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: 'Agent Wiki',
      repo: 'shdkej/agent-wiki',
      loadSidebar: false,
      basePath: '/',
      homepage: 'diary/',
      subMaxLevel: 2,
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
</body>
</html>
EOF

# 홈페이지용 index.md
cat > docs/index.md << 'EOF'
# Agent Wiki

세션 기록 및 학습 다이어리. 30분마다 자동 업데이트.

## 최근 다이어리
- [diary/](diary/) 디렉토리에서 날짜별 기록 확인
EOF

git add docs/
git commit -m "add Docsify for GitHub Pages"
git push origin main
```

#### 2단계: GitHub Pages 활성화
```
GitHub 웹 > shdkej/agent-wiki > Settings > Pages
Source: "Deploy from a branch"
Branch: main / docs 폴더 선택
저장
```

#### 3단계: 배포 확인 (수 분 후)
```
https://shdkej.github.io/agent-wiki/
```

---

## 4. MkDocs 옵션 (더 풍부한 UI 원할 때)

기본 Docsify로 충분하지 않으면 MkDocs 적용:

```yaml
# mkdocs.yml
site_name: Agent Wiki
docs_dir: diary
theme:
  name: material
  features:
    - navigation.instant
    - search.suggest
plugins:
  - search
  - git-revision-date-localized
nav:
  - Home: index.md
```

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin
      - run: mkdocs build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site/
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v3
        id: deployment
```

---

## 5. 구현 체크리스트

### 사전 확인 (L2 - 사용자 직접 확인)
- [ ] `shdkej/agent-wiki` 레포 GitHub Pages 현재 상태 확인
- [ ] diary 마크다운 파일 구조 확인 (`diary/YYYY-MM-DD.md` 형식)
- [ ] `shdkej/shdkej.github.io` 레포 존재 여부 (옵션 B 필요 시)

### 구현 (L2 - agent-wiki 레포에 push 필요)
- [ ] `docs/index.html` 생성 (Docsify)
- [ ] `docs/index.md` 홈페이지 생성
- [ ] agent-wiki 레포에 커밋 & 푸시
- [ ] GitHub Pages 활성화 (Settings > Pages)

### 검증
- [ ] `https://shdkej.github.io/agent-wiki/` 접속 가능 확인
- [ ] diary 최신 파일 웹에 표시 확인
- [ ] 다음 diary-sync 실행 후 자동 업데이트 확인

---

## 6. 주의사항

- **공개 레포 필수**: GitHub Pages 무료 플랜은 public 레포에서만 동작
- **CDN 캐시**: GitHub Pages는 약 1시간 CDN 캐시 → diary 업데이트 후 최대 1시간 지연
- **민감 콘텐츠**: diary가 공개되므로 개인 정보 포함 여부 사전 확인 필요
- **L2 승인 필요**: agent-wiki 레포 push는 다른 레포 push로 L2 권한 필요

---

## 7. 결론

**Docsify + GitHub Pages (옵션 A + C 조합)** 를 1차 권장합니다.

- 구현 난이도: 매우 낮음 (30분 이내)
- 유지보수: 자동 (diary-sync 후 자동 배포)
- 비용: 무료

이 작업은 `shdkej/agent-wiki` 레포에 직접 push가 필요하므로 **L2 승인** 후 진행합니다.
