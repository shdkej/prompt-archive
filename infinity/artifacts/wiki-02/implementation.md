# wiki-02: agent-wiki GitHub Pages 구현 파일

> Intent: wiki-02 | 작성: 2026-04-18 | 상태: L2 승인 대기
> wiki-01 설계안(agent-wiki-pages-design.md) 기반 실제 구현 파일

---

## 구현 방법: Docsify + GitHub Pages (옵션 A+C 조합)

설계 결정: `shdkej/agent-wiki` 레포에 직접 `docs/` 폴더를 추가하고
GitHub Pages를 `/docs` 폴더로 설정.

---

## 생성할 파일 1: `docs/index.html`

```html
<!DOCTYPE html>
<html lang="ko">
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
      subMaxLevel: 2,
      search: {
        placeholder: '검색...',
        noData: '결과 없음',
      },
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
</body>
</html>
```

---

## 생성할 파일 2: `docs/README.md` (홈페이지)

```markdown
# Agent Wiki

세션 기록 및 학습 다이어리. 30분마다 자동 업데이트.

## 최근 다이어리

[diary/](diary/) 디렉토리에서 날짜별 기록을 확인하세요.

---

*이 사이트는 diary-sync.sh에 의해 자동으로 업데이트됩니다.*
```

---

## 배포 절차 (L2 승인 후 실행)

### 1단계: 파일 생성 및 커밋

GitHub MCP 또는 직접 push:

```bash
# shdkej/agent-wiki 체크아웃 후 실행
mkdir -p docs
# docs/index.html 내용 붙여넣기 (위 파일 1)
# docs/README.md 내용 붙여넣기 (위 파일 2)
git add docs/
git commit -m "add Docsify for GitHub Pages"
git push origin main
```

### 2단계: GitHub Pages 활성화

```
GitHub 웹 > shdkej/agent-wiki > Settings > Pages
Source: "Deploy from a branch"
Branch: main
Folder: /docs
→ Save
```

### 3단계: 배포 확인

수 분 후:
```
https://shdkej.github.io/agent-wiki/
```

---

## 주의사항

- **공개 레포 필수**: GitHub Pages 무료 플랜은 public 레포에서만 동작
- **diary 경로 확인**: Docsify basePath가 레포 루트 기준이므로, `diary/` 폴더가
  레포 루트에 있어야 사이드바 없이도 `diary/YYYY-MM-DD` URL로 접근 가능
- **CDN 캐시**: Pages 배포 후 최대 10분 소요
- **민감 콘텐츠**: diary가 공개되므로 개인 정보 포함 여부 사전 확인 권장

---

## GitHub MCP로 파일 생성하는 방법 (대안)

`mcp__github__create_or_update_file` 도구를 사용해 직접 생성 가능:

1. `shdkej/agent-wiki` 레포에 `docs/index.html` 생성
2. `shdkej/agent-wiki` 레포에 `docs/README.md` 생성
3. GitHub Settings에서 Pages 활성화 (API로는 `mcp__github__*` 도구 미지원 → 웹 UI 필요)

승인 후 에이전트가 MCP 도구로 파일 2개를 자동 생성합니다.
Pages 활성화는 사용자가 GitHub 웹 UI에서 직접 수행해야 합니다.
