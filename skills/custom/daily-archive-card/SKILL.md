---
name: daily-archive-card
description: 확정된 하루 회고로 비공개 데일리 아카이브 카드 한 장을 만들거나 검수한다. 책 페이지형 HTML/CSS 조판과 1080×1350 PNG가 필요할 때 사용한다.
---

# 데일리 아카이브 카드

1. [카드 제작 규격](references/card_layout.md) 전문을 읽는다. 현지 날짜와 최종 회고에서 Keep, Problem, 내일의 행동 하나, 그 행동에서 확인할 신호를 뽑는다. 도시는 확인된 경우에만 적는다.
2. [keyword-title](../keyword-title/SKILL.md)의 blog 모드로 그날의 실제 장면에서 제목 후보를 세 개 이상 만든다. 한눈에 읽히는 제목을 고르고, 이미 확정된 제목은 문구를 보존한다.
3. 네 섹션을 책 한 페이지처럼 HTML/CSS로 조판해 HTML과 1080×1350 PNG를 만든다. 규격 §4의 여백·정렬·한글 줄바꿈 기준을 적용한다.
4. Knowledge Lab 체크아웃에서 아래 검증기를 실행한다. Python 3와 Pillow가 필요하다. 두 인수에는 방금 만든 파일의 경로를 순서대로 넣는다.

   ```sh
   python3 scripts/reviews/validate_daily_archive_card.py FINAL_PNG INDEX_HTML
   ```

   위 명령의 작업 디렉터리는 Knowledge Lab의 `source/openclaw-system/`이다. 검증 통과 후 최종 PNG를 직접 열어 §6의 일곱 항목을 확인하고 렌더 파일·뷰어·현지 확인 시각·판정을 기록한다. 실패하면 해당 요소를 고쳐 다시 렌더한다.

카드 단독 요청의 산출물은 HTML, 최종 PNG, 검수 기록이다. 일일 회고 마감 중에 호출됐다면 이 산출물을 마감 단계로 돌려준다.
