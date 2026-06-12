# prompt-archive

개인 프롬프트/스킬/가이드 자산 아카이브.

## Skills 색인

| 스킬 | 설명 | 언제 쓰는가 |
| --- | --- | --- |
| `skills/daily-news` | GeekNews(news.hada.io) 기사를 정리해 AI 뉴스레터(마크다운)를 생성. 취향 기반 자동 선별과 피드백 학습 포함 | GeekNews URL을 던질 때, "오늘 AI 뉴스 골라줘" |
| `skills/keyword-title` | 시드(주제·초안·제품 컨셉)를 받아 모드별(blog/threads/app-name/product-name) 후보를 발산·선별하는 네이밍·제목 스킬 | 글 제목·서비스 이름을 뽑아야 할 때 |

전체 자산 목록과 설치 대상은 `scripts/setup.sh`가 단일 출처(source of truth)입니다. 단일 파일 스킬과 가이드 문서(DAILY-FEEDBACK-SYSTEM.md, OMC.md, WORKFLOW-MASTER.md 등)는 그 링크 목록을 참조하세요.

## 설치

```bash
git clone https://github.com/shdkej/prompt-archive ~/workspace/prompt-archive
~/workspace/prompt-archive/scripts/setup.sh
```

`setup.sh`는 `~/.claude/` 하위에 심볼릭 링크를 일괄 생성합니다. 디렉토리형 스킬(`skills/daily-news` 등)은 디렉토리째 링크됩니다.
