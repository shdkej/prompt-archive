# wiki-03: agent-wiki 모바일 네비게이션 개선

> Intent: wiki-03 | 작성: 2026-04-19T04:00 | L2 승인 대기

## 문제 분석

Docsify + vue.css 기본 테마에서 모바일(≤768px) 화면의 사이드바 토글 버튼은:
1. **위치**: 좌하단 고정, 초기 방문자가 발견하기 어려움
2. **시각적 약함**: 배경이 투명하고 크기가 작아 터치 타깃으로 부족
3. **오버레이 없음**: 사이드바가 열려도 콘텐츠 영역과 구분이 안 됨
4. **링크 클릭 후 미닫힘**: 링크 클릭 후 사이드바가 그대로 남아 화면을 가림

## 개선 방향

- 토글 버튼을 더 크고 눈에 띄게 (흰 배경 + 그림자 + 녹색 아이콘)
- 사이드바 열릴 때 반투명 오버레이 → 콘텐츠 영역 클릭으로도 닫기 가능
- 링크 클릭 시 사이드바 자동 닫힘 (Docsify의 `close` class 활용)
- 기존 설정(`loadSidebar`, `search depth:3`, `auto2top`) 100% 유지

---

## 배포할 파일: `index.html` (루트)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Agent Wiki</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
  <style>
    /* 모바일 네비게이션 개선 */
    @media screen and (max-width: 768px) {
      .sidebar-toggle {
        width: 44px;
        height: 44px;
        padding: 10px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        bottom: 20px;
        left: 20px;
      }
      .sidebar-toggle span {
        background-color: #42b983;
        display: block;
        height: 2px;
        margin: 5px 0;
        width: 24px;
        transition: all 0.2s;
      }
    }
    #mobile-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.45);
      z-index: 20;
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <div id="mobile-overlay"></div>
  <script>
    window.$docsify = {
      name: 'Agent Wiki',
      repo: 'shdkej/agent-wiki',
      loadSidebar: true,
      subMaxLevel: 3,
      auto2top: true,
      search: {
        placeholder: '검색...',
        noData: '결과 없음',
        depth: 3
      },
      plugins: [
        function(hook) {
          hook.doneEach(function() {
            if (window.innerWidth > 768) return;
            var overlay = document.getElementById('mobile-overlay');

            // 오버레이 표시/숨김: body.close 여부 관찰
            var observer = new MutationObserver(function() {
              overlay.style.display = document.body.classList.contains('close') ? 'none' : 'block';
            });
            observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });

            // 오버레이 클릭 → 사이드바 닫기
            overlay.addEventListener('click', function() {
              document.body.classList.add('close');
            });

            // 사이드바 링크 클릭 → 사이드바 자동 닫기
            document.querySelectorAll('.sidebar-nav a').forEach(function(link) {
              link.addEventListener('click', function() {
                document.body.classList.add('close');
              });
            });
          });
        }
      ]
    }
  </script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="//cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
</body>
</html>
```

---

## 배포 절차 (L2 승인 후 실행)

```bash
# 1. agent-wiki 클론
git clone https://github.com/shdkej/agent-wiki.git /tmp/agent-wiki-wiki03
cd /tmp/agent-wiki-wiki03

# 2. index.html 교체 (위 내용으로)
# (위 HTML을 index.html에 덮어쓰기)

# 3. 커밋 & 푸시
git add index.html
git commit -m "improve mobile navigation: bigger toggle, overlay, auto-close sidebar"
git push origin main

# 4. 배포 확인 (수 분 후)
# https://shdkej.github.io/agent-wiki/ 모바일 브라우저에서 확인
```

---

## 기존 파일과의 차이점 요약

| 항목 | 기존 (ba2f28a) | 변경 후 |
|------|--------------|---------|
| 토글 버튼 크기 | 기본 (작음) | 44×44px, 흰 배경, 그림자 |
| 토글 아이콘 색 | 기본 (회색) | #42b983 (Docsify 녹색) |
| 오버레이 | 없음 | 반투명 검정 (#mobile-overlay) |
| 링크 클릭 후 사이드바 | 열린 채 유지 | 자동 닫힘 |
| 기존 기능 | — | 100% 유지 (loadSidebar, search, auto2top) |

---

## 주의사항

- `#mobile-overlay`의 `z-index: 20` → Docsify 사이드바(z-index: 25)보다 낮게 설정해야 사이드바가 오버레이 위에 보임
- `MutationObserver`는 사이드바 토글 시마다 실행. 성능 문제 없음 (모바일 전용, 단순 class 체크)
- `.sidebar-nav a` 이벤트 등록은 `hook.doneEach` 안에서 이루어지므로 페이지 이동 시마다 재등록됨 → 중복 등록 가능성 없음 (매번 새 DOM)
