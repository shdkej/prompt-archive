---
name: insight-card-maker
description: 공용 카드뉴스(세로 6장) 제작 스킬. insight 모드(사진/스크린샷 + 인사이트·관찰·여행 노트·발행 앵글)와 news 모드(daily-news 출력, GeekNews/AI Trends 기사, 기사 요약)를 모두 처리하며, 문체 선정(humanize-korean) → 렌더링 → 업로드 → 검증 → 카드뉴스 라이브러리 발행까지 담당한다. 사용 시기 - (1) "카드뉴스 만들어줘", Instagram/Threads 카드 요청, (2) 사진과 함께 인사이트/문구 발행 요청, (3) 뉴스 기사를 카드로 만들 때, (4) 카드뉴스 라이브러리 추가/재빌드/배포. Card 1 제목은 반드시 keyword-title 스킬 게이트를 거친다.
---

# Insight Card Maker

공용 카드뉴스 제작 스킬입니다. 두 가지 모드를 모두 처리합니다.

- `insight` 모드: 사진/스크린샷과 함께 인사이트, 문구, 관찰, 여행 노트, 발행 앵글, 또는 Instagram/Threads 스타일 카드 요청.
- `news` 모드: 선별된 뉴스 기사, AI Trends 항목, GeekNews 항목, `daily-news` 마크다운, 기사 요약, 또는 `뉴스용 카드뉴스` 같은 요청.

뉴스용으로 별도의 비주얼 파이프라인을 만들지 마세요. 공용 카드뉴스 렌더러, 업로드 흐름, 검증, 공개 라이브러리를 재사용하고, 모드별로는 스토리/체크리스트 규칙만 분리합니다.

뉴스 기반 카드뉴스는 내용 추출과 시각화를 분리합니다. 기사, GeekNews, AI Trends, `daily-news` 목록, 또는 사용자가 고른 뉴스 번호로 카드뉴스를 만들 때는 먼저 `daily-news` 스킬의 톤과 구조로 출처 사실, 한줄 요약, 주요 내용, 독자 관점 함의를 뽑고, 그 결과를 이 스킬의 뉴스 모드 6장 시퀀스로 압축합니다. 단순히 원문 링크만 보고 바로 카드 문구를 쓰지 않습니다.

아래 규칙에서 "기본"은 모두 같은 예외를 가집니다: 사용자가 명시적으로 다르게 요청하면 그 요청이 우선합니다.

## Hard Defaults (모든 모드 공통)

- 초안 작성 전에 항상 모드를 먼저 선택: `insight` 또는 `news`.
- Card 1 제목은 반드시 아래 "Card 1 Title Gate"를 통과해야 합니다 (`keyword-title` 스킬 필수).
- 카드 문구를 config에 넣기 전에 반드시 아래 "Copy Humanize Gate"를 통과해야 합니다 (`humanize-korean` 스킬 필수).
- 기본 장수는 정확히 6장의 세로 카드.
- Card 6은 고정 CTA/FOLLOW 엔딩 카드 (아래 "Card 6 CTA Rule" 참조).
- 완성된 세트는 항상 카드뉴스 라이브러리에 추가.
- `AI NEWS`, `World Note` 같은 좌측 하단 브랜드 뱃지 금지.
- 카드 안의 작은 보조 설명, 하단 캡션, 부제, 출처를 가장한 설명문, 미세 노트 문장은 기본 금지입니다. 작은 글씨로 맥락을 덧붙여 완성도를 보완하지 않습니다. 필요한 정보는 메인 제목/본문 크기로 올리거나, 카드 밖의 라이브러리 메타데이터·완료 보고·본문 글로 보냅니다.
- Card 1 표지는 제목이 혼자 서야 합니다. 사용자가 명시적으로 요청하지 않은 하단 설명문/body/subtitle은 넣지 않습니다. 뉴스 출처 표기가 꼭 필요할 때도 매체명/출처명만 아주 짧게 두고, 설명 문장으로 늘리지 않습니다.
- Card 1 표지는 기본적으로 사용자의 오리지널 이미지 풀에서 고릅니다. 허용 출처는 `upload.shdkej.com/random`, `img.shdkej.com/original/`, `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/cache/card-news-r2-selections/`, `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/r2-selections/`처럼 `original/` 소속 또는 사용자 원본으로 검증된 이미지뿐입니다. Card 1에는 생성 이미지, 뉴스 원문 이미지, 스크린샷, 내부 제작 배경, `derived/` 카드뉴스 에셋을 쓰지 않습니다. 오리지널 이미지를 찾지 못하면 대체 이미지로 진행하지 말고 발행 전 중단하고 보고합니다. 단, 사용자가 내부 제작 표지나 샘 캐릭터 표지를 명시적으로 승인한 경우에만 예외를 허용하고, `image_policy`에 `Card 1 USER_ORIGINAL_PHOTO exception approved by user`와 승인 근거를 남깁니다.
- 카드 2-5에는 실제 사진이나 명확한 비주얼 에셋을 첨부. 생성 이미지보다 `upload.shdkej.com` / `img.shdkej.com` 저장소의 사용자 원본 사진을 우선 검토하되, 뉴스/샘 캐릭터/내부 제작 배경 규칙이 있는 경우 해당 모드의 에셋 규칙을 따릅니다.
- 최근 카드뉴스에서 샘(Saem) 캐릭터 방향이 승인된 흐름이거나 사용자가 샘을 언급한 뒤 만드는 뉴스형 카드뉴스는, 카드 2-5의 생성/내부 제작 배경에 샘 캐릭터 세트를 기본 후보로 둡니다. 추상 배경이나 중립 건축 배경으로 대체하려면 사용자가 명시적으로 원했거나 주제상 샘이 방해된다는 이유를 `image_policy`에 남깁니다. 이 규칙은 Card 1 표지의 `USER_ORIGINAL_PHOTO` 요구를 덮어쓰지 않습니다.
- 사용자가 뉴스 카드에서 "샘 어디 갔냐", "샘 넣어", "이미지에 샘"처럼 피드백하면, 이후 같은 세트의 Cards 2-5에는 샘 캐릭터가 실제로 보이는 이미지를 사용해야 합니다. 중립 추상 배경이나 샘이 거의 보이지 않는 배경은 발행 전 하드 블로커입니다. Card 1까지 샘 캐릭터를 쓰는 것은 사용자가 내부 제작 표지를 명시적으로 승인한 예외일 때만 허용하고, 그 경우 `image_policy`에 `Card 1 USER_ORIGINAL_PHOTO exception approved by user`와 승인 근거를 남깁니다.
- 사용자가 도식 요소를 제거하거나 더 이상 신경 쓰지 말라고 정리한 뒤에는, 도식/설명 기호를 복구 과제로 취급하지 않습니다. 카드 의미는 샘의 자세, 빛, 공간, 여백, 재료감으로만 전달하고, 원·선·화살표·네트워크·아이콘·차트·라벨·UI 같은 도식 요소는 하드 금지입니다.
- 같은 날 사진이 여러 장이면 카드 1-5에 서로 다른 사진을 최대한 배치. 지도/스크린샷/메모 캡처처럼 반복 배경으로 약한 이미지는 라이브러리 `source_urls`와 작업 근거로 보존하되, 시각 배경으로는 그날의 다른 사진을 우선.
- 사진/비주얼이 눈에 띄게 드러나도록. 카드가 텍스트 전용으로 보이게 만드는 불투명 오버레이 금지.
- 이미지 전체 블러와 과한 어둡게 처리 모두 기본 금지입니다. 특히 Card 1 표지는 사진 자체가 첫 인상을 결정하므로 배경 이미지를 블러 처리하거나 검은 그라데이션으로 누르지 않습니다. 제목 가독성이 부족하면 먼저 사진 선택, crop/zoom, 빈 영역 배치, 밝은 종이 톤의 얇은 보정, 아주 얇은 비네트/그라데이션으로 해결합니다.
- Card 1에서 실제 Gaussian blur를 쓰지 않았더라도, `paper_fill` 같은 전체 오버레이가 강해서 사진이 뿌옇게 보이거나, `top_alpha`/`bottom_alpha`가 강해서 사진이 어둡게 눌려 보이면 이미지 노출 규칙 위반으로 봅니다. 표지의 `paper_fill`은 이미지가 살아 보이는 낮은 알파를 먼저 쓰고, 검은 덮개보다 밝은 종이 톤 보정과 위치 조정으로 해결합니다.
- Cards 2-5도 카드 전체를 흐리게 만드는 전면 블러를 쓰지 않습니다. 꼭 필요한 경우에도 텍스트 바로 뒤의 좁은 국소 영역만 약하게 처리하고, 카드마다 crop/zoom, 본문 위치, 그라데이션 범위/방향, 여백형/풀블리드형을 섞어 이미지 노출과 레이아웃 다양성을 유지합니다.
- 텍스트 뒤로 사진 질감, 선, 아이콘, UI 목업, 강한 명암 경계가 지나가면 발행 금지. 해결 순서: (1) 배경 crop/zoom을 조정해 빈 영역에 텍스트 배치 → (2) 부드러운 그라데이션/비네트/얇은 텍스트 스트로크로 대비 확보. 둥근 박스형 텍스트 패널은 시각적으로 무거우므로 기본 금지에 가깝게 취급하고, 다른 방식으로 해결이 불가능할 때만 최후 수단으로.
- 표지는 예쁜 사진보다 제목이 놓일 빈 공간과 5초 안의 정지력을 우선.
- 발행/보고 전에 최종 단일 카드 이미지 파일 수를 세고 필요한 페이지가 모두 존재하는지 확인. 콜라주, 프리뷰, 컨택트 시트, 뷰어 스크린샷을 최종 카드 대신 절대 보내지 않기.

## Copy Humanize Gate

카드뉴스 문구는 렌더링 설정을 만들기 전에 먼저 문체를 고릅니다. 제목 게이트가 Card 1의 정지력을 담당한다면, 이 게이트는 카드 1-6 전체의 한국어 리듬과 AI 문체 제거를 담당합니다.

필수 흐름:

1. `humanize-korean`의 `SKILL.md`와 `references/quick-rules.md`를 먼저 읽으세요.
2. Card 1 title, Cards 2-5 title/body, Card 6 title/CTA를 한 번에 모아 `copy_draft`로 정리하세요. Card 1 body와 Card 6 subtitle은 기본으로 비우고, 명시 예외가 있을 때만 포함합니다.
3. `humanize-korean` 기준으로 문체를 먼저 고릅니다. 사실·수치·날짜·고유명사·직접 인용은 보존하고, 번역투, 기계적 병렬, AI식 관용구, 과한 접속사, 불필요한 불릿식 리듬만 줄입니다.
4. 변경률은 30% 이하를 기본 상한으로 두고, 정보형·뉴스형 카드에서는 의미가 흔들릴 만한 의역을 하지 않습니다.
5. Card 1 title은 `keyword-title` 게이트의 선택 결과로 잠그고, humanize 단계에서는 읽기 전용으로 둡니다. 제목을 바꿔야 할 만큼 어색하면 직접 윤문하지 말고 `keyword-title` 후보 단계로 돌아가 다시 선택합니다.
6. 윤문 뒤에는 카드별로 `fact_lock`을 점검합니다: 장소, 날짜, 가격, 예매 여부, 출처명, 사람/회사/제품명, 수치, URL, 직접 인용이 초안과 일치해야 합니다.
7. 강조어(`body_highlight_terms`)는 윤문된 최종 본문에 실제로 존재하는 단어만 고릅니다. 초안에만 있던 단어를 강조어로 남기면 실패입니다.
8. 렌더 config를 만들 때 `quality_notes.copy_humanize_gate`에 먼저 기록하고, 라이브러리 항목을 만들 때 같은 내용을 `quality_notes.copy_humanize_gate`로 복사합니다. 최소 포함값: `source_skill: humanize-korean`, `fact_lock: pass`, `changed_focus`, `highlight_terms_checked`.
9. 문체 게이트를 통과한 최종 문구만 렌더 config에 넣습니다. config 작성 후 문장을 고치면 이 게이트를 다시 실행합니다.

예외:

- 사용자가 원문 그대로, OCR 원문, 법률/계약/증빙 원문, 비교용 before 텍스트를 요청한 경우에는 문체를 고치지 않습니다. 이때도 `copy_humanize_gate`에는 `skipped`와 이유를 남깁니다.
- 카드가 한글이 아닌 언어로만 구성되면 `humanize-korean`을 적용하지 않고, 카드 언어에 맞는 별도 문체 점검만 수행합니다.

## Page Role Gate

렌더링 config를 쓰기 전에 Card 1, Cards 2-5, Card 6의 역할을 먼저 분리해서 잠가야 합니다. 사용자가 이미 알고 있는 포맷을 짧게 요청했더라도, 이 게이트를 생략하지 않습니다.

- Card 1은 표지입니다. `keyword-title` 게이트를 통과한 후크, 5초 안의 정지력, 제목 안전영역이 우선입니다. 작은 설명/body/subtitle로 제목을 보완하지 않고, Card 2-5의 설명 카드 규칙을 Card 1에 그대로 복사하지 않습니다.
- Cards 2-5는 본문 카드입니다. 뉴스 모드에서는 각각 `무엇이 바뀌었나`, `왜 중요한가/어떻게 작동하나`, `위험/제약/긴장`, `실용적 함의` 중 하나를 맡습니다. 샘 캐릭터 세트에서는 이 네 장이 샘의 자세, 빛, 공간, 여백으로 의미를 보여줘야 하며, 중립 배경만 깔고 텍스트로 설명하는 방식은 실패입니다.
- Card 6은 CTA/FOLLOW 엔딩입니다. 추가 뉴스 요약이나 체크리스트 카드로 쓰지 않습니다.
- Cards 2-5의 긴 설명 요청은 본문 카드에만 적용합니다. 사용자가 명시적으로 표지도 같은 포맷으로 통일하라고 말하지 않았다면, Card 1의 표지 역할을 먼저 지킵니다.
- config 작성 전 `page_role_notes` 또는 `quality_notes`에 `Card 1 표지`, `Cards 2-5 샘/본문`, `본문 오버레이 적용 범위`를 짧게 남깁니다.

## Layout Variety Rule

카드뉴스가 한 가지 구성만 반복되지 않도록, 카드 1-5에는 사진 안전영역과 문장 성격에 맞춰 여러 레이아웃을 섞습니다. 단, 다양성은 가독성과 사진의 존재감을 해치지 않는 범위에서만 허용합니다.

허용/권장 레이아웃:

- `paper` 상단 제목형: Card 1 표지의 기본형입니다. 처음 카드뉴스 계열처럼 제목은 상단 고정 템플릿 영역에 크게 두고, 흰색/크림색/밝은 종이 톤 위에서는 검은색 또는 짙은 올리브 잉크를 씁니다. 하단 작은 설명은 기본으로 두지 않습니다. 표지는 제목 중심 구조가 기본입니다.
- 상단/중앙 여백형: 사진의 빈 공간에 짧은 제목 또는 메인 문장 하나를 얹는 보조형. 작은 보조 설명은 붙이지 않습니다.
- 본문 오버레이형: Cards 2-5의 기본형입니다. 상단에는 Card 1 표지 제목과 같은 `paper` 제목 스타일의 짧은 항목 제목을 남기고, 본문은 사진 위에 흰색 굵은 글자, 얇은 어두운 스트로크, 하단 어두운 그라데이션으로 배치합니다. 본문 핵심어는 색상 또는 볼드로 강조합니다. 사진과 샘을 덮는 흰색/크림색 패널을 만들지 않습니다.
- 좌우 여백형: 피사체가 한쪽에 몰린 사진에서 반대쪽 빈 영역에 문장을 배치.
- 풀블리드 짧은 문장형: 사진을 크게 살리고 제목 또는 한 문장만 얹는 리듬 전환용.

`paper` 상단 제목형 세부 기준:

- Card 1 표지의 기본 `variant`는 `paper`입니다. `paper_fill`, `paper_ink`, `paper_sub`, `paper_line` 팔레트를 사용하고, 밝은/흰 배경 위 제목은 검은색 또는 짙은 올리브 잉크여야 합니다.
- 제목은 상단 고정 템플릿 영역에 둡니다. 1080x1350 기준 `title_y`는 대략 250-270, `title_size`는 68-78px 범위를 우선합니다. 표지(Card 1)도 제목을 하단으로 내리지 않습니다.
- Card 1 body는 기본으로 비웁니다. `body_y`, `body_size`, `body_chars`를 써서 하단 작은 설명을 자동 생성하지 않습니다.
- Card 1 표지는 `상단 큰 제목` 구조가 기본입니다. `bottom_white`, 하단 제목 패널, 제목을 사진 아래에 깔아두는 구조, 하단 작은 설명문은 사용자가 명시적으로 요구하지 않으면 쓰지 않습니다.
- Cards 2-5에는 `paper` 하단 짧은 설명 규칙을 자동 복사하지 않습니다. Cards 2-5의 body는 아래 본문 오버레이형 규칙을 따르되, 작은 캡션처럼 보이면 실패입니다.

본문 오버레이형 세부 기준:

- Cards 2-5의 기본입니다. `title`은 비우지 않고, Card 1 표지의 `paper` 제목 스타일과 동일한 계열로 둡니다. 즉 상단 고정 템플릿 영역, 짙은 잉크/올리브 계열, 굵은 글자, 스트로크 없는 깨끗한 제목 처리를 기본값으로 씁니다. 예: `모델 조합`, `온디바이스 AI`, `추론 칩 투자`, `추론 비용`. title을 하단 본문 자리에 깔거나 body처럼 쓰지 않습니다. 본문용 어두운 스트로크, 하단 그라데이션, 강조색 설정을 제목에 같이 적용하지 않습니다. 어두운 사진 위에서만 가독성을 위해 흰색 제목을 허용하되, 이때도 크기/굵기/위치/스트로크 없음은 표지 제목 스타일을 유지합니다.
- 사용자가 제목 스타일 자체를 바꾸라고 하지 않았다면, 가독성이나 본문 수정을 하면서 Card 1 제목 스타일, Cards 2-5 상단 제목 스타일, CTA 제목 스타일을 함께 바꾸지 않습니다. 수정 요청이 본문 크기, 블러, 오버레이, 이미지 노출에 관한 것이면 해당 요소만 조정합니다.
- 사용자가 Cards 2-5 제목을 "표지처럼" 또는 "표지 스타일로" 맞추라고 하면, 위 기본값을 재확인한 것으로 처리합니다. 별도 예외를 만들지 말고 Card 1의 `paper` 제목 스타일을 그대로 적용합니다.
- 이때 Card 1 자체의 제목/본문 스타일은 절대 새로 바꾸지 않습니다. 먼저 Card 1을 표지 역할의 최종 승인 스타일로 잠그고, Cards 2-5에는 `title_fill`, `title_size`, `title_y`, `title_spacing`, `title_stroke_width`, `title_stroke_fill`처럼 제목 관련 값만 복사합니다. Card 1의 `variant`, `paper_fill`, `body_*`, `text_stroke_*`, `crop`, `zoom`을 Cards 2-5 동기화를 위해 함께 바꾸면 실패입니다.
- Cards 2-5의 `body`는 작은 보조 설명이 아니라 메인 본문입니다. 2줄 고정이 아니며, 필요한 만큼 길어도 됩니다. 단, 모바일 프리뷰에서 읽기 흐름이 무너지면 글자를 작게 줄이지 말고 문장을 줄이거나 카드 분할을 검토합니다.
- 기본 스타일은 1080x1350 기준 `body_size` 40-46px, `body_bold: true`, 흰색 또는 크림색 본문, `text_stroke_width` 3-4px, 어두운 스트로크, `bottom_alpha` 150-180 안팎입니다. 배경이 어두우면 스트로크를 줄이고, 배경이 밝으면 그라데이션/스트로크를 강화합니다.
- body에는 핵심 단어 1-2개를 반드시 강조 후보로 잡습니다. 전체 본문이 이미 bold라면 `body_highlight_terms` + `body_highlight_fill`로 레몬/연두 계열 포인트 컬러를 쓰고, 밝은 `paper` 배경에서는 연한 레몬보다 `body_highlight_fill: [205,255,0,255]`처럼 실제 프리뷰에서 보이는 진한 레몬을 우선합니다. 강조어는 의미 단어만 고르고 조사·접속사는 포함하지 않습니다.
- 본문은 사진과 샘을 해치지 않는 낮은 위치에 둡니다. 샘 얼굴, 핵심 피사체, 손짓/자세를 가리면 실패입니다. 해결 순서는 문장 줄이기, `body_y` 조정, crop/zoom 조정, `bottom_alpha` 조정입니다.
- 본문 가독성 때문에 블러가 필요해 보여도 Cards 2-5 전체 배경을 흐리게 만들지 않습니다. 카드별로 본문 위치와 크롭을 바꾸고, 필요한 카드에만 텍스트 주변 여백 20-40px 안팎의 좁은 후면 국소 블러 또는 더 짧은 그라데이션을 적용합니다. 블러 강도는 주요 피사체와 사진 질감이 식별되는 수준으로 제한합니다. 네 장 모두 같은 불투명도, 범위, 위치의 어두운/흐린 하단 처리가 기계적으로 반복되면 실패입니다.
- Card 5는 세트의 마무리, 여운, 실용적 프레임, 테이크어웨이 역할을 맡는 경우가 많으므로 Cards 2-4보다 더 부드러운 흐림을 허용합니다. 단, 사진 전체를 무의미하게 지우는 블러가 아니라 마무리 감정을 만드는 배경 정리여야 하며, 주요 피사체나 장소감이 완전히 사라지면 실패입니다.
- 사용자가 "2-5페이지는 하단 본문 빼고 최초/전버전으로"처럼 말하면, Cards 2-5의 제목·크롭·배경·상단 고정 템플릿은 최초 `paper` 템플릿 값으로 되돌리고, **하단 body 문장/강조 처리만** 현재 승인된 본문 오버레이 계열로 남깁니다. 이 경우 body는 화면 중간이 아니라 1080x1350 기준 `body_y` 980-1040 근처의 맨 아래 영역에 둡니다.
- 흰색/크림색 하단 패널이나 넓은 밝은 그라데이션으로 사진을 덮는 방식은 쓰지 않습니다.
- body를 60px 이상으로 키우거나 하단 제목처럼 보이게 만들지 않습니다. 제목은 상단 title, 설명은 하단 body라는 역할이 깨지면 실패입니다.
- 발행 전 실제 렌더 파일과 216px contact sheet를 열어 ①Card 1 표지가 상단 제목 중심이고 하단 작은 설명이 없는지 ②Cards 2-5 title이 상단 고정 템플릿 영역에 있는지 ③흰색/밝은 title 배경에서는 제목이 검은색/짙은 잉크인지 ④title이 하단에 깔리지 않았는지 ⑤Cards 2-5 본문 오버레이가 읽히는지 ⑥본문 강조어가 보이는지 ⑦본문이 사진/샘을 과하게 덮지 않는지 ⑧흰 패널이 생기지 않았는지 확인합니다.

## Card 1 Title Gate

첫 카드가 세트를 열어볼 가치를 결정합니다. 일반적인 요약 제목으로 취급하지 마세요.

Card 1 제목 생성에는 `keyword-title` 스킬이 필수입니다. 유일한 예외는 스킬 파일이나 도구 접근이 실제로 불가능한 경우이며, 이때도 같은 구조의 수동 제목 게이트를 수행하고 보고에 `keyword-title 대체 수행`과 이유를 명시합니다. 단순 요약 제목을 Card 1에 바로 쓰는 것은 금지입니다.

필수 흐름:

1. `keyword-title`의 `SKILL.md`와 필요한 reference를 먼저 읽으세요.
2. 카드뉴스의 실제 출처/시드를 한 문장으로 압축하세요.
3. Card 1 제목 후보를 최소 5개 생성하세요.
4. 구체적 키워드 명료성, 낚시가 아닌 호기심, 사용자 톤 적합성, 세트 전체를 끌고 갈 힘으로 점수를 매기세요.
5. 후보마다 `대상 명사`, `변화 동사`, `내 일과의 접점`, `14자 안 핵심`, `멈춤 이유 한 줄`을 확인하세요. 총론형보다 `대상 명사 + 변화 동사 + 내 일과의 접점`이 드러나는 구체 변화형을 기본 승자로 봅니다.
6. 정확하지만 내부자 표현이면 (예: `검증 레이어`, `운영 책임`, `전문성 이동`) 표지 후보에서 감점하고, 더 쉽게 풀거나 원문/사용자 표현의 생활어 훅을 되살리세요. 원문 제목이나 사용자 표현에 `나의`, `하는 법`, `무엇으로 남을까`처럼 자기 질문을 여는 문장이 있으면 기술적 재해석보다 그 표현을 우선 검토하세요. 출처 제목 자체가 충분히 강하면 억지로 기술 프레임으로 바꾸지 마세요.
7. 제목이 총론형이면 body로 보완하지 말고 후보를 다시 뽑거나 더 구체적인 대상/변화로 좁히세요.
8. 나머지 시퀀스를 작성하기 전에 최종 Card 1 제목 하나를 확정하세요.
9. 작업 보고에 Card 1 제목이 `keyword-title` 게이트를 통과했다는 사실을 반드시 포함하세요.

Card 1 body 규칙:

- body는 약한 제목을 구제하는 용도가 아닙니다. Card 1 body는 기본으로 제거하고 제목이 세트를 끌고 가게 하세요.
- 사용자가 표지 본문을 명시적으로 요청한 경우에만 body를 씁니다. 이때도 작은 하단 설명으로 붙이지 말고, 표지 구성 안에서 충분히 읽히는 메인 카피 크기로 처리하거나 별도 본문 카드로 넘깁니다.
- `이 발표`, `이 기사`, `이 자료`처럼 표지만 보면 지시 대상이 불분명한 표현 금지. `하용호님의 발표자료`, `GeekNews 요약`, `OpenAI 발표`처럼 실제 출처명/발표자를 직접 적으세요.
- Card 1과 Card 6이 같은 총론을 반복하면 앞뒤 리듬이 죽습니다. Card 1은 한 문장의 변화/후크, Card 6은 읽고 난 뒤 남는 판단/CTA 요약으로 역할을 분리하세요.

## Card 6 CTA Rule

Card 6은 변경 없이 복사하는 정적 이미지가 아니라, 동적 가운데 카피를 갖는 고정 CTA/FOLLOW 템플릿입니다. SAM/Infinity 루프 설명, 요약 체크리스트, 추가 콘텐츠 카드로 쓰지 마세요.

고정 유지 (명시적 변경 요청 전까지):

- 페이지 구조: `6/6`, 상단 라인, 가운데 헤드라인, 구분선, CTA 라인, 연락처. 가운데 서브타이틀은 기본으로 비우고 명시 예외에서만 씁니다. 하단 중앙의 6개 점/불릿/페이지 인디케이터는 넣지 않습니다.
- 연락처: `Threads @minimal_collector`, `Archive library.aws.shdkej.com`.
- 비주얼: 현재 승인된 화이트/레몬 CTA 아트 디렉션 — 상단은 밝은 레몬 계열, 아래로 갈수록 흰색/크림 배경으로 빠지는 방향을 기본으로 한다. 위가 흰색/크림이고 아래가 레몬으로 끝나는 뒤집힌 세로 그라데이션은 쓰지 않는다. 짙은 올리브 잉크/라인을 쓰고, 카피 뒤에 짙은/회색/올리브/검정 그림자 영역은 금지. 그라데이션은 그늘진 느낌이 아니라 가벼운 느낌.
- 더 강한 세트 특화 라인이 없을 때의 CTA 라인: `AI와 일하는 방식을 계속 정리합니다`.
- 이미 발행된 세트를 수정할 때는 기존에 승인된 CTA 라인을 우선 보존합니다. 기본 CTA 문구가 바뀌었더라도, 사용자가 명시적으로 CTA 변경을 요청하지 않았다면 현재 세트의 마지막 카드 CTA를 기본값으로 덮어쓰지 않습니다.
- 기존 CTA 이미지를 변형할 때는 배경 영역만 다시 색칠하고 텍스트, 라인 아트, 레이아웃, 연락처는 보존.
- 다른 CTA 배경색은 사용자가 명시적으로 요청하거나 출처 브랜드/아트 디렉션이 명백히 요구할 때만.
- 과거 템플릿에 `show_dots`, `dots`, `active_dot`, `dot_*` 설정이 남아 있어도 Card 6 출력에는 반영하지 않습니다. 사용자가 명시적으로 점 인디케이터 복원을 요청한 경우에만 별도 예외로 다룹니다.

세트마다 변경:

- `follow_card.title`: 세트 전체의 핵심 주장을 요약하는 짧은 한국어 2-4줄.
- `follow_card.subtitle`: 기본으로 비웁니다. 사용자가 명시적으로 CTA 부제나 설명을 요청했거나 세트 이해에 반드시 필요할 때만 해당 세트의 주요 긴장, 메커니즘, 함의를 1줄로 짧게 둡니다. 작은 설명문처럼 보이면 실패입니다.
- 서로 무관한 세트들에 동일한 일반 가운데 카피를 재사용하지 마세요. 좋은 예: `오늘의 AI 흐름은 / 에이전트와 / 인프라로 모입니다`. 나쁜 예 (세트가 실제로 기록/발행에 관한 것이 아닌 한 금지): `기록을 / 쌓아두지 말고 / 다음 결과물로 / 바꾸세요`, `저장하고 / 나중에 써먹으세요`.

## News Mode Image Classes

뉴스 모드의 이미지 에셋 분류는 엄격합니다. 렌더링 전에 각 `images` 항목을 아래 중 하나로 분류하세요.

- `USER_ORIGINAL_PHOTO`: `upload.shdkej.com/random`, `img.shdkej.com/original/`, `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/cache/card-news-r2-selections/`, `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/r2-selections/`에서 선택한 사진. 사용자의 오리지널 이미지 풀이며 Card 1 표지의 유일한 허용 클래스입니다.
- `GENERATED_CARD_ASSET`: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/generated-assets/` 또는 작업별 generated-assets 디렉터리의 AI 생성/수동 제작 카드 비주얼. 기본적으로 카드 2-5에서 허용.
- `NEUTRAL_DESIGN_ASSET`: 출처 뉴스에서 비롯되지 않은 내부 제작 추상 텍스처, UI 목업, 다이어그램, 아이콘 필드 등. 예외 클래스이며 기본값이 아님. 해당 파일의 출처가 config나 라이브러리 메타데이터에 문서화된 경우에만 사용.
- `SOURCE_NEWS_MEDIA`: 기사 페이지, Reddit 게시물, 출처 사이트, OG/프리뷰 이미지, 출처 스크린샷, 다운로드된 뉴스 미디어에서 온 모든 파일/URL. 기본적으로 모든 카드에서 금지. 출처 수집 중 다운로드한 이미지는 로컬 캐시에 있어도 `SOURCE_NEWS_MEDIA`입니다.

기본 이미지 맵: Card 1 = `USER_ORIGINAL_PHOTO` 정확히 한 장만 허용; 카드 2-5 = `GENERATED_CARD_ASSET` 또는 모드상 허용된 사용자 원본/샘 캐릭터 에셋; Card 6 = CTA 템플릿. Card 1용 `USER_ORIGINAL_PHOTO`를 확보하지 못하면 생성 이미지나 출처 이미지로 대체하지 말고 중단합니다.

뉴스/출처 이미지 사용은 발행을 막는 강력한 차단 요인입니다. 카드 1-5의 에셋이 `SOURCE_NEWS_MEDIA`로 판정되면 업로드/라이브러리 발행 전에 멈추고 교체하세요.

## Cards 2-5 Generated Asset Direction

카드 2-5의 내부 생성 에셋은 사용자가 승인한 차분하고 단정한 건축/자연광 톤을 기본값으로 삼습니다. 단, Sam Samuel 캐릭터 비주얼을 쓰는 세트에서는 아래 "Saem Character Rule"이 이 섹션보다 우선합니다. 뉴스 주제가 특별히 다른 시각 언어를 요구하지 않는 한, 차트·네트워크·아이콘·미래형 UI 그래픽보다 아래 톤을 우선하세요.

### Reusable Internal Backgrounds

- `steel background`: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/generated-assets/steel-background-2026-07-19/steel-background-wallpaper.png`
  - 분류: `NEUTRAL_DESIGN_ASSET`
  - 크기: 1080x1920
  - 용도: 배경화면, 카드뉴스 시안 배경, 카드 2-5 내부 제작 배경.
  - 특징: 텍스트 없는 브러시드 메탈 질감, 원본 철제 카드뉴스 표지의 상단 바/얇은 분리선/측면 엣지 레이아웃 유지.
  - provenance: tracked `asset.json`과 tracked PNG 자체가 재사용 근거입니다. ignored `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/runs/` 산출물은 생성 당시 참고 로그로만 남기고, 스킬이나 새 config의 필수 `source_reference`로 쓰지 않습니다.
  - 제한: 기본 발행 규칙의 Card 1 `USER_ORIGINAL_PHOTO` 요구를 대체하지 않습니다. 사용자가 내부 제작 표지를 명시한 경우에만 표지 후보로 검토합니다.

기본 아트 디렉션:

- 따뜻한 화이트/크림 벽, 옅은 석재 바닥, 라이트 우드, 부드러운 자연광, 긴 그림자.
- 정돈된 건축선과 큰 여백. 텍스트가 올라갈 넓은 빈 벽/바닥/공간을 확보.
- 식물은 포인트만. 오브젝트는 최소화하고, 복잡한 책상/기기/소품은 피함.
- 완성도는 높되 디테일은 과하지 않게. 제품 렌더처럼 빽빽한 미세 묘사보다 러프한 큰 면, 부드러운 질감, 절제된 구성을 우선.
- 팔레트는 화이트/크림/석재/우드 중심. 레몬 또는 올리브 포인트는 아주 작게만 허용.
- 세트 안에서는 같은 공간·빛·재료 패밀리로 묶되, 카드마다 crop/시점/빈 영역 위치를 달리해 반복감을 줄임.

생성 프롬프트에 반드시 넣을 금지 조건:

- 이미지 안에 텍스트, 한글/영문 글자, 숫자, 로고, 워터마크, UI 아이콘, 글리프, 차트, 읽히는 상징을 절대 넣지 않기.
- 뉴스 원문/출처 사이트/OG/프리뷰/스크린샷을 참고 이미지나 배경으로 쓰지 않기.
- 미래형 네온, 보라/파랑 그라데이션, 사이버풍 인터페이스, 과한 3D 아이콘, 복잡한 네트워크 선, 고대비 어두운 영역 금지.

예시 프롬프트 골격:

```text
Calm, tidy editorial background for a Korean card-news slide, warm white plaster walls, pale limestone floor, light oak, soft natural daylight, long gentle shadows, minimal greenery accent, organized architectural lines, broad clean negative space for future text overlay, refined but slightly rough and not hyper-detailed, no clutter. Absolutely no text, no letters, no numbers, no logos, no watermark, no UI icons, no glyphs, no charts, no readable symbols.
```

## Saem Character Rule

사용자가 Sam Samuel, Sam/Saem/샘, 또는 Sam Samuel 브랜드 캐릭터를 명시하면 카드 2-5의 기본 비주얼은 `샘(Saem)` 캐릭터 기반 생성 에셋으로 전환합니다. 단순히 조약돌/이끼가 등장하는 다른 주제에는 자동 적용하지 않습니다. 외부 브랜드/뉴스 출처/다른 창작물의 캐릭터를 다루는 카드에서도 자동 적용하지 않습니다.

샘은 Sam Samuel의 정본 캐릭터입니다. 자세와 행동은 바꿀 수 있지만, 캐릭터 정체성은 바꾸지 않습니다.

샘의 외형은 아래 불변 요소를 따릅니다. 이미지 대조에는 작업공간의 `space/apps/control-center-cms/public/assets/saem-character/saem-system-signature.png`를 사용합니다.

정본 불변 요소:

- 손바닥 크기의 둥글게 닳은 조약돌 캐릭터.
- 따뜻한 회베이지색 매트 스톤 질감.
- 머리 위쪽의 부드러운 올리브색 이끼 패치와 작은 새싹.
- 작고 담담한 점 두 개의 눈. 입은 없거나 거의 보이지 않음.
- 부드러운 3D 클레이 렌더, 미니멀 젠 스타일, 낮은 채도, 넉넉한 여백.
- 크림/웜그레이/올리브/아침빛 계열 팔레트.

금지 요소:

- 카드마다 다른 캐릭터처럼 보이는 형태 변경.
- 사람형, 로봇형, 동물형, 과한 마스코트형 전환.
- 큰 반짝이 눈, 과장된 표정, 말풍선, 팔다리 과장, 귀여움 과잉.
- 텍스트, 한글/영문 글자, 숫자, 로고, 워터마크, UI 아이콘, 글리프, 차트, 읽히는 상징.
- 보라/파랑 AI 그라데이션, 네온, 사이버풍, 고대비 어두운 배경.

카드 2-5 구성 방식:

- 카드별 행동을 고정된 역할표로 미리 정하지 않습니다.
- 먼저 해당 세트의 실제 뉴스/인사이트를 읽고, Card 2-5 각각의 문장과 기능을 정합니다.
- 각 카드의 비주얼은 그 카드가 말하는 변화, 원인, 긴장, 사례, 함의, 다음 행동 중 무엇을 맡는지에 맞춰 샘의 자세/행동/빛/물결/이끼/새싹/주변 자연물로 새로 설계합니다.
- 샘 캐릭터 세트는 같은 물가/같은 카메라/같은 배경을 반복하지 않습니다. 샘의 정체성은 유지하되 카드 2-5의 공간, 카메라 거리, 샘의 크기와 위치를 바꿉니다. 예: 테이블 정물, 얕은 물, 실내 문턱, 창가 바닥, 석재 정원, 낮은 측면 구도, 넓은 원경, 오버헤드 구도처럼 장면 리듬을 분리합니다.
- 샘은 배경 장식으로만 서 있으면 안 됩니다. 카드의 핵심 포인트를 조용히 수행하거나 견디는 장면이어야 합니다. 예: 무게중심·비용 판단은 작은 저울 위의 샘, 선택·전환은 갈림길이나 디딤돌 앞의 샘, 비용 하락·완화는 낮아지는 물결 옆의 샘, 위험·제약은 좁아진 빛이나 낮은 자세의 샘, 실용적 함의는 정돈된 돌길을 건너는 샘처럼 카드 문장과 1:1로 연결합니다.
- 샘의 행동이나 소품은 이미지 생성 프롬프트 단계에서 장면 안에 자연스럽게 포함해야 합니다. 렌더링 후 PIL/캔버스/편집 도구로 선, 원, 저울, 화살표, 디딤돌 같은 도형을 덧붙이는 방식은 금지합니다. 그렇게 하면 샘 장면이 아니라 도식/스티커처럼 보입니다.
- 샘은 설명을 대신하는 도식이나 아이콘이 아니라, 카드의 의미를 조용히 연기하는 동일 캐릭터입니다. 추상 도식, 라벨, 차트, 경고 아이콘, 네트워크 선, UI 그래픽으로 의미를 직접 설명하지 않습니다.
- 사용자가 도식 요소 제거를 승인한 세트에서는 도식 부재를 다시 문제 삼지 않습니다. 검증 기준은 "도식이 있는가"가 아니라 "샘 캐릭터 정체성, 여백, 텍스트 안전영역, 금지 기호 부재, 카드 의미와 장면의 느슨한 연결이 유지되는가"입니다.
- 위험/제약/긴장도 공포 장면이나 고대비 어둠으로 만들지 말고, 흐린 빛, 멈춘 물결, 축소된 여백, 낮아진 자세처럼 정본 팔레트 안의 작은 상태 변화로 표현합니다.
- 다음 행동/실용적 함의는 새싹, 정돈된 돌길, 따뜻한 아침빛, 맑아지는 수면처럼 카드 주제에 맞는 자연 상태와 샘의 행동으로 표현합니다.

생성 프롬프트는 매 카드마다 같은 캐릭터 기준 문장을 반복하고, 카드별 행동만 추가하세요. `same character, same pebble body, same moss patch, same tiny sprout, same calm dot eyes`처럼 동일성 고정 문구를 넣습니다. 이미지 생성 결과가 정본과 다르면 업로드/렌더링 전에 재생성합니다.

샘 캐릭터 기반 카드도 텍스트는 이미지 생성 단계에서 넣지 않습니다. 카드 문구는 렌더링 단계에서만 얹습니다.

## Mode Rules

### Insight Mode

입력이 사진/스크린샷과 함께 인사이트, 개인적 관찰, 메모, 여행 노트, 발행 앵글일 때.

사용자가 카드뉴스 맥락에서 "사진만 보내도 인사이트 카드뉴스", "감성 넘치게", "사진 보고 카드뉴스"처럼 지시한 뒤에는, 후속 사진에 별도 캡션이 없어도 막히지 말고 `insight` 모드로 진행합니다. 이때 사진은 단순 일일 트래킹이 아니라 카드뉴스 입력으로 취급하고, 장면에서 보이는 공간감·빛·거리감·감정의 여백을 바탕으로 짧은 감성 인사이트를 작성합니다. 단, 사용자가 명시적으로 기록/보관만 원하거나 카드뉴스 맥락이 없으면 `DATA_CAPTURE_RULES.md`의 Daily Photos 기본값이 우선입니다.

사진 단독 인사이트 카드뉴스의 기본 자막 스타일:

- 사용자가 첨부한 Instagram 여행 표지 레퍼런스처럼 화면 중앙 또는 피사체 주변의 빈 공간에 자막을 둡니다.
- 한 줄 또는 두 줄 구조를 쓰되, 둘 다 사진의 주인공으로 읽히는 크기여야 합니다. 작은 serif/italic 보조 설명 라인은 기본으로 쓰지 않습니다. 예: `KAZAKHSTAN`, `Welcome to Mars`.
- 위쪽 장소 표현을 쓰는 경우에도 설명문이나 인사이트 문장이 아니라 `Welcome to Mars`처럼 짧은 제목 조각으로 처리합니다. 12-18자 감각 설명을 작은 글씨로 덧붙이지 않습니다.
- 아래쪽 장소명은 사진 속 장소를 알면 구체 장소명, 모르면 국가명이나 도시명만 씁니다. 모르는 장소를 추정해서 세부 지명으로 쓰지 않습니다.
- 이 레퍼런스형 카드에서는 기존 카드뉴스식 상단 페이지 번호, 라인, 하단 본문, 라벨, 작은 설명을 기본으로 제거하고, 사진 중앙의 큰 자막만 남깁니다.
- 텍스트는 흰색 또는 따뜻한 크림색, 얇은 그림자/스트로크만 사용하고 둥근 박스·반투명 캡션 패널은 쓰지 않습니다.
- 자막 위치는 1080x1350 기준 대략 `y=560~720`의 중앙권을 먼저 시도하되, 인물·건축물·핵심 피사체를 가리면 빈 하늘/벽/바닥 쪽으로 살짝 옮깁니다.
- 문장은 설명보다 여운을 우선합니다. 예: `Welcome to ...`, `도시/감정/장면 키워드`처럼 한 단어 또는 짧은 명사구를 메인 자막으로 씁니다.
- 사진 내부에 이미 UI, 자막, 워터마크, 스크린샷 프레임이 있는 경우에는 원본 사진으로 쓰기 어렵다고 보고, 실제 원본 사진을 요청하거나 UI를 잘라낼 수 있는지 먼저 판단합니다.

가로 사진 기반 여행 카드뉴스의 고정 규칙:

- 사용자가 "가로 사진", "원본 비율", "위아래 검은색", "자막은 아래쪽"을 요청하면 공용 렌더러의 `travel_letterbox` 스타일을 우선 사용합니다.
- 가로 사진은 세로 카드에 꽉 채우기 위해 크롭하지 않고 원본 비율을 유지합니다. 남는 위아래 영역은 검은색 또는 거의 검은색 여백으로 둡니다.
- 좌측 상단 네비는 3요소를 기본으로 합니다: `로고/브랜드`, `페이지 번호`, `페이지 제목`. 예: `SS | 2/6 | SEASON`.
- 핵심 자막은 하단 가운데에 둡니다. 사진 위를 덮지 않고, 검은 하단 여백 안에서 읽히게 합니다.
- 정보형 여행 카드에서는 정보칩을 쓰지 않습니다. `장소`, `계절감`, `시간대`, `최근성`, `예매 여부`, `비용`은 화면 안 작은 노트로 넣지 말고, 필요한 경우 메인 문장 또는 라이브러리 메타데이터로 보냅니다.
- 정보는 많이 넣되, 한 장이 표처럼 보이면 실패입니다. 한 카드에는 중심 판단 1개만 메인 문장으로 남기고, 보조 정보는 본문 글·마지막 CTA 카드·라이브러리 메타데이터로 분산합니다.
- 비용·예매·영업시간처럼 최근성이 중요한 여행 정보는 카드 config나 라이브러리 메타데이터에 `확인일`, `출처 URL`, `카드별 정보 축`을 남깁니다. 카드 화면에 하단 작은 노트(`확인 2026.07.26`)로 넣지 않습니다.
- 둥근 큰 박스형 본문 패널은 쓰지 않습니다. 필요한 대비는 검은 여백, 얇은 스트로크, 하단 본문 위치 조정으로 해결합니다.

기본 6장 시퀀스:

- Card 1: Title Gate를 통과한 후크 또는 주장.
- Card 2: 관련 있을 때 출처/맥락 또는 경로/공간 맥락; 아니면 인사이트 하나.
- Card 3: 첫 번째 핵심 인사이트.
- Card 4: 두 번째 핵심 인사이트, 대비, 또는 메커니즘.
- Card 5: 실용적 프레임, 루틴, 함의, 또는 재사용 가능한 루프/테이크어웨이.
- Card 6: 고정 CTA/FOLLOW 엔딩 카드.

사진과 GPX가 있는 여행 기억 세트: `대표 장면 → 경로 지도 → 관찰된 디테일 → 의미/인사이트 → 재사용 가능한 여행 기록 프레임 → 고정 CTA 엔딩` 순서를 우선.

### News Mode

출처가 뉴스 항목, 기사, `daily-news` 출력, AI Trends/GeekNews 항목, 기사 요약일 때.

뉴스 모드의 내용 추출은 `daily-news` 스킬을 선행 단계로 결합합니다. 사용자가 이미 발송된 `[AI 뉴스 N]` 목록에서 번호를 고르면, 해당 번호의 요약과 원문 링크를 `daily-news` 방식으로 다시 정리한 뒤 카드 문구를 작성합니다. 이때 `daily-news` 결과는 최종 뉴스레터가 아니라 카드뉴스 입력 메모로 저장하거나 라이브러리 메타데이터에 연결할 수 있습니다.

기본 6장 시퀀스:

- Card 1: Title Gate를 통과한 구체적 후크 또는 뉴스 주장.
- Card 2: 무엇이 바뀌었는가.
- Card 3: 어떻게 작동하는가 또는 왜 중요한가.
- Card 4: 위험, 제약, 또는 긴장.
- Card 5: 독자/사용자를 위한 실용적 함의.
- Card 6: 고정 CTA/FOLLOW 엔딩 카드 (화이트 레몬 기본).

추가 규칙:

- 뉴스 세트 초안은 반드시 `Card 1 표지 규칙`과 `Cards 2-5 본문 규칙`을 분리해서 작성합니다. Card 1은 전체 세트의 후크이고, Cards 2-5는 각 뉴스/논점의 본문 카드입니다.
- 사용자가 뉴스 세트에서 샘 캐릭터 방향을 이미 승인했거나 샘을 언급한 경우, Cards 2-5는 기본적으로 샘 캐릭터 카드입니다. 각 장은 뉴스의 의미와 연결된 샘 장면이어야 하며, 중립 추상 배경으로 대체하려면 사용자 명시 승인 없이는 발행하지 않습니다.
- 사용자가 "1~5번으로 카드뉴스"처럼 여러 뉴스 항목을 지정하면, Card 1은 첫 뉴스이면서 동시에 세트 표지 역할을 해야 합니다. Cards 2-5는 나머지 뉴스 항목 또는 핵심 논점을 맡고, Card 6은 CTA로 닫습니다. 표지 역할 때문에 Card 1의 제목/이미지 규칙을 약화시키지 않습니다.
- 이미지는 위 "News Mode Image Classes"를 그대로 따르세요. 텍스트 전용 카드 금지.
- 카드 내부에 출처를 남기세요. 최소한 Card 1의 `kicker`나 작은 출처 라인에 `GeekNews`, 매체명, 발표자/원 출처명처럼 사용자가 출처를 바로 알 수 있는 정보를 넣습니다. 라이브러리 메타데이터의 `source_urls`만으로 대체 금지. 단, 출처 표기는 후크 제목을 밀어내지 않도록 짧고 작게.
- 인사이트 카드와 동일한 공용 비주얼 템플릿 패밀리를 사용하되 6장 뉴스 구조를 따르세요.
- 라이브러리 추가 시 `format: "news"`로, 6장 카드 URL 모두 포함.

## Canonical Files

- 공용 렌더러: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/make_insight_cards.py`
- 저장된 사진 무작위 선택기: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/select_r2_card_photo.py`
- 공용 템플릿/config 디렉터리: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/templates/`
- 출력 루트: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/runs/`
- 카드뉴스 라이브러리 데이터: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/library/items.json`
- 카드뉴스 라이브러리 빌더: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/build_card_news_library.py`
- 카드뉴스 라이브러리 페이지: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/library/index.html`
- 배포된 카드뉴스 라이브러리: `https://library.aws.shdkej.com`
- 배포 복사 대상: `/home/ubuntu/workspace/space/infra-aws-static-sites/sites/library/dist/index.html`
- 업로드 엔드포인트: `/home/ubuntu/.openclaw/workspace/TOOLS.md`에 문서화됨
- 라이브러리 상세의 다중 카드 저장은 모바일 브라우저 호환을 위해 클라이언트 즉석 ZIP 생성이 아니라 빌드 시 만들어진 정적 ZIP 파일 링크로 제공한다.

## Workflow

1. 모드 결정: `insight` 또는 `news`.
2. 출처 자료 수집.
   - 인사이트: 출처 사진을 찾거나 저장. Telegram 인바운드 사진은 보통 `/home/ubuntu/.openclaw/media/inbound/` 아래.
   - 뉴스: 출처 기사/뉴스 항목을 확인하고 `daily-news` 스킬 방식으로 사실 핵심과 독자 관점 함의를 먼저 추출. 기사/뉴스레터/AI 뉴스 번호 기반 카드뉴스는 이 추출 메모를 만든 뒤, 비주얼 카드를 위해 이 스킬로 돌아오기.
   - Card 1 배경은 이미지를 생성하기 전에 저장된 사진 무작위 선택기를 먼저 시도:

```bash
python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/select_r2_card_photo.py --json
```

   - 선택기는 먼저 `UPLOAD_IMAGE_RANDOM_URL` 또는 `https://upload.shdkej.com/random`을 호출합니다. 엔드포인트는 기본적으로 `original/` 이미지 폴더로 향해야 하며 (카드뉴스 렌더 등 가공 에셋은 `derived/` 소속), JSON 또는 공개 `302 Location` 리다이렉트 둘 다 유효합니다. 업로드 토큰이 거부되면 인증 없이 재시도. 엔드포인트 불가 시 `R2_PHOTO_MANIFEST_URL`, 또는 `R2_PHOTO_BUCKET` + `R2_PHOTO_ENDPOINT_URL` / `CLOUDFLARE_R2_ENDPOINT_URL`로 대체. 모두 불가하거나 선택된 파일이 사용자 오리지널 이미지로 검증되지 않으면 Card 1 대체 이미지를 만들지 말고 발행 전 중단합니다.
   - 선택된 Card 1 URL/path가 `original/` 소속이 아니고 manifest/metadata에도 사용자 원본 검증값이 없으면 실패로 처리합니다. `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/cache/card-news-r2-selections/` 또는 `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/r2-selections/`에서 왔다는 사실만으로는 통과시키지 않습니다.
3. Card 1 Title Gate 실행 (위 섹션의 필수 흐름 그대로).
   - 비교에 유용할 때 후보 제목 5개를 로컬 노트나 라이브러리 메타데이터에 보관.
   - 라이브러리 메타데이터에 `title_gate`를 남길 때 가능하면 선택 이유, 탈락한 총론형 후보, `stopping_power`, `density`, `cta_separation` 메모 포함.
4. 선택한 모드의 시퀀스 규칙으로 6장 초안 작성.
   - Card 6의 세트 특화 `title`/CTA를 이 초안에 포함합니다. `subtitle`은 기본으로 비우고, 사용자가 명시적으로 요청했거나 이해에 반드시 필요한 경우에만 씁니다. Copy Humanize Gate 뒤에 새 Card 6 문구를 만들지 않습니다.
5. Copy Humanize Gate 실행 (위 섹션의 필수 흐름 그대로).
   - Card 1 제목 게이트 결과는 읽기 전용으로 유지하고, 제목이 너무 AI식 총론으로 보이면 `keyword-title` 후보 단계로 돌아가 다시 고릅니다.
   - 윤문 결과에서 장소·날짜·가격·예매 여부·출처명·사람/회사/제품명·수치·URL·직접 인용이 바뀌지 않았는지 카드별로 확인합니다.
   - 강조어는 최종 문장 안에 실제 존재하는 단어로만 다시 고릅니다.
6. 공용 템플릿/config 디렉터리에 JSON config 생성/업데이트.
   - 텍스트는 짧게. 긴 텍스트는 글자를 줄이기보다 여러 카드로 분할.
   - Card 1 표지는 처음 카드뉴스 계열의 `paper` 상단 제목형입니다. 제목을 상단 고정 템플릿 영역에 두고, 하단 짧은 설명/body/subtitle은 기본으로 비웁니다.
   - Cards 2-5는 상단 짧은 title + 하단 본문 오버레이형이 기본입니다. title은 Card 1 표지 제목과 동일한 `paper` 제목 스타일(상단 고정 영역, 짙은 잉크/올리브, 굵은 글자, 스트로크 없음)을 씁니다. body는 흰색/크림색 굵은 메인 본문 + 얇은 어두운 스트로크 + 하단 어두운 그라데이션으로 읽히게 하고, 핵심어는 색상 또는 볼드로 강조합니다. 작은 보조 설명처럼 보이는 body는 쓰지 않습니다.
   - Card 1 배경 이미지는 블러하지 않습니다. Cards 2-5도 전면 블러를 쓰지 않고, 필요한 카드에만 좁은 텍스트 후면 국소 처리로 제한합니다.
   - Card 5가 세트의 마무리/테이크어웨이를 맡을 때는 Cards 2-4보다 블러와 그라데이션을 더 부드럽게 써도 됩니다. 이때도 장소감과 주요 피사체 식별은 남깁니다.
   - 단조로운 구성을 피하려면 crop/zoom, 이미지 시점, 제목 줄바꿈, 본문 위치와 길이, 그라데이션 방향을 조정합니다. Cards 2-5의 body를 Card 1처럼 하단 짧은 paper 설명으로 되돌리지 않습니다. 사용자가 명시적으로 “본문도 예전 짧은 설명으로”라고 요청할 때만 예외입니다.
   - 좌측 하단 뱃지를 원하지 않을 때는 `label`을 비워 두기.
   - 뉴스 모드: 각 `images` 항목을 이미지 클래스로 분류·점검.
   - Card 6: Copy Humanize Gate를 통과한 세트 특화 `title`과 필요한 경우에만 쓴 `subtitle`을 그대로 반영합니다. config 작성 중 새로 쓰거나 기본 CTA 문구로 되돌리지 않습니다.
7. 공용 렌더러로 렌더링:

```bash
python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/make_insight_cards.py \
  --config /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/templates/<name>.json \
  --out /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/runs/<name>
```

8. 최소한 card 1과 card 6을 시각적으로 검사.
   - 확인: 한국어 텍스트 가독성, 대비, 이미지 충돌, 원치 않는 좌측 하단 뱃지 부재, 작은 보조 설명/캡션 부재, 마지막 카드 배경색, Card 6 가운데 카피가 일반 CTA 반복이 아니라 세트 요약인지.
   - 샘 캐릭터 세트에서는 Card 2-5도 함께 펼쳐 보고, 같은 캐릭터로 보이는지, 넓은 텍스트 안전영역이 있는지, 이미지 내부에 텍스트/숫자/로고/도식 기호가 없는지 확인. 이 중 하나라도 실패하면 업로드/전송 전에 재생성합니다.
   - 이미지만 먼저 전달하는 중간 산출물이라도, 각 파일을 실제로 열어보고 검수하지 않은 상태로 "완료"라고 말하지 않습니다.
   - 배경이 제목/본문을 침범하면 발행 전에 crop/zoom, `top_alpha`/`bottom_alpha`, `text_stroke_width`/`text_stroke_fill`을 먼저 조정. `text_panel`은 박스가 디자인을 망치지 않는 경우에만 최후 수단.
9. 각 최종 이미지를 `https://upload.shdkej.com?kind=derived`에 업로드.
   - `CLOUDFLARE_IMAGE_UPLOAD_TOKEN`은 로컬 env에서만 로드. 토큰을 절대 출력하거나 저장하지 않기.
10. 반환된 모든 URL을 `curl -I` 등으로 검증하고 HTTP 200을 반환하는 URL만 사용.
11. 완성된 카드 세트를 카드뉴스 라이브러리에 추가.
    - `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/data/card-news/library/items.json`에 항목 추가/업데이트.
    - `id`, `date`, `format`, `title`, `subtitle`, `category`, `source`, `tags`, `cover`, 모든 카드 URL, `takeaway`, `thread`, 로컬 config/output 경로 포함.
    - config의 `quality_notes.copy_humanize_gate`를 라이브러리 항목의 `quality_notes.copy_humanize_gate`에도 반드시 복사.
    - 디자인 학습에 유용하면 `quality_notes`에 `정지력`, `밀도`, `CTA 분리`, `사진 안전영역` 중 실제로 판단한 항목을 짧게 기록.
12. 라이브러리 재빌드 및 배포:

```bash
python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/build_card_news_library.py
python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/build_card_news_library.py --check-stage
```

- `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/library/index.html`을 `/home/ubuntu/workspace/space/infra-aws-static-sites/sites/library/dist/index.html`로 복사.
- commit/push 전 `--check-stage`가 통과해야 합니다. `items.json`만 stage되고 공개 HTML이 unstaged로 남았거나, 같은 slug의 템플릿/library 최종본이 staged/unstaged에 동시에 걸리면 완료 처리하지 말고 최종 library·template·source-assets·HTML을 한 세트로 다시 stage합니다.
- 로컬 워크스페이스(`openclaw-backups`) 커밋/푸시는 배포가 아닙니다. `space` repo의 `sites/library/dist/` 갱신, S3/CloudFront 반영, 원격 URL 검증까지 완료되어야 카드뉴스 작업이 끝난 것으로 봅니다.
- 배포가 GitHub Actions를 통하면 정적 사이트 변경을 커밋하고 push.
- 수동 배포라면 `s3://static-library-aws-shdkej-com`으로 동기화하고, CloudFront 배포 `E3H9I5GVQBIEUL`을 무효화하며, HTTP 200 검증.
- 완료 보고 전 반드시 원격 공개 페이지에서 새 카드뉴스의 `id` 또는 제목을 직접 확인하세요:

```bash
curl -L --max-time 20 -s https://library.aws.shdkej.com/ | rg '<card-news-id>|<title>'
curl -I -L --max-time 20 -s https://library.aws.shdkej.com/downloads/<card-news-id>.zip
```

13. 라이브러리 발행 후 전달 기본값:
    - 개별 카드 이미지를 채팅으로 보내지 않고, 라이브러리 URL, format, 장수, 체크리스트 하이라이트, 검증 상태를 담은 간결한 완료 보고를 전송.
    - 채팅으로 카드 이미지를 보내는 경우는 셋뿐: 사용자가 명시적으로 요청, 라이브러리 발행 전 프리뷰 요청, 라이브러리 업로드/배포가 막혀 있어 에셋이 필요할 때.
    - 채팅 전달 시 각 최종 단일 카드 에셋을 순서대로 따로 첨부하고, 첫 메시지/캡션 텍스트에 제목(뉴스면 뉴스 제목) 포함.
14. 장수, CTA 가운데 카피, 뱃지, 라이브러리, 색, 제목 캡션, 전달 동작, 템플릿 동작에 관한 사용자 수정 사항은 같은 실행 안에서 스킬/문서 업데이트로 취급.

## Pre-Publish Checklist

- [ ] Card 1 제목이 `keyword-title` 게이트로 생성/검토된 후보 중에서 선택되었다 (수동 대체 시 예외와 이유를 보고에 명시).
- [ ] Card 1 제목 후보를 `대상 명사`, `변화 동사`, `내 일과의 접점`, `14자 안 핵심`, `멈춤 이유 한 줄`로 점검했고, 총론형보다 구체 변화형을 우선했다.
- [ ] 카드 문구가 config 작성 전에 `humanize-korean` 기준으로 윤문되었고, `copy_humanize_gate` 메모에 `source_skill`, `fact_lock`, `changed_focus`, `highlight_terms_checked`가 남아 있다.
- [ ] 윤문 뒤에도 장소·날짜·가격·예매 여부·출처명·사람/회사/제품명·수치·URL·직접 인용이 유지된다.
- [ ] 모든 `body_highlight_terms`가 윤문된 최종 본문 안에 실제로 존재한다.
- [ ] Page Role Gate를 통과했다: Card 1은 표지, Cards 2-5는 본문, Card 6은 CTA로 역할이 분리되어 있으며 `quality_notes`나 config 메모에 적용 범위를 남겼다.
- [ ] Card 1 body/subtitle/하단 작은 설명은 기본으로 비워져 있다. 사용자가 명시적으로 요청한 예외가 있다면 작은 글씨가 아니라 읽히는 메인 카피 크기로 처리했고, 지시 대상이 불분명한 표현(`이 발표` 등)이 없다.
- [ ] 카드 1-5에 눈에 띄는 사진/비주얼 에셋이 있고, 텍스트 전용으로 읽히지 않는다.
- [ ] Card 1 표지는 `USER_ORIGINAL_PHOTO` 한 장만 사용했다. 생성 이미지, 뉴스 원문 이미지, 스크린샷, 내부 제작 배경, `derived/` 카드뉴스 에셋으로 대체하지 않았다.
- [ ] 선택된 Card 1 URL/path가 `original/` 소속이거나 manifest/metadata에 사용자 원본 검증값이 있다. 선택기/cache/manifest 경유만으로 통과시키지 않았다.
- [ ] Card 1 표지 이미지를 블러하지 않았다. 제목 가독성은 사진 선택, crop/zoom, 빈 영역, 얇은 비네트/그라데이션, 스트로크로 해결했다.
- [ ] Cards 2-5에 전면 블러를 쓰지 않았다. 필요한 경우에도 텍스트 주변 여백 20-40px 안팎의 좁은 국소 처리만 적용했고, 주요 피사체와 사진 질감이 식별된다. 네 장 모두 같은 불투명도, 범위, 위치의 흐린/어두운 하단 처리로 반복되지 않게 crop/zoom, 본문 위치, 그라데이션 범위/방향을 섞었다.
- [ ] Card 5가 마무리/테이크어웨이 역할이라 더 강한 흐림을 쓴 경우, 그것이 여운과 정리를 만드는 의도적 처리이며 장소감과 주요 피사체 식별을 완전히 지우지 않는다.
- [ ] 제목/본문 뒤에 복잡한 배경 요소가 겹치지 않는다 (crop/zoom → 그라데이션/스트로크 순으로 해결, 박스 패널은 최후 수단).
- [ ] Card 1 표지는 처음 카드뉴스 계열의 `paper` 상단 제목형이다: 제목은 상단 고정 템플릿 영역, 흰/밝은 바탕에서는 검은색 또는 짙은 잉크, 하단 작은 설명/body/subtitle 없음. Card 1 제목을 하단에 깔지 않았다.
- [ ] Cards 2-5는 상단 짧은 title + 하단 본문 오버레이형이다. title은 Card 1 표지 제목과 동일한 `paper` 제목 스타일(상단 고정 영역, 짙은 잉크/올리브, 굵은 글자, 스트로크 없음)을 유지하고, body는 읽기 좋은 흰색/크림색 메인 본문 + 어두운 스트로크/그라데이션 + 핵심어 강조를 사용한다. Cards 2-5 body를 작은 보조 설명이나 Card 1처럼 하단 짧은 paper 설명으로 되돌리지 않았다.
- [ ] Cards 2-5 제목 스타일을 맞추는 과정에서 Card 1 표지의 제목/본문 스타일이 바뀌지 않았다. Card 1은 표지용 `paper` 스타일과 비어 있는 body를 유지했고, Cards 2-5에는 제목 관련 값만 동기화했다.
- [ ] Card 1 배경은 제목 안전영역과 정지력을 우선해 crop/zoom을 잡았다.
- [ ] 샘 캐릭터 세트: 카드 2-5의 샘이 같은 캐릭터로 보이며 조약돌 몸체, 이끼 패치, 작은 새싹, 점눈, 회베이지 질감이 유지된다. 각 카드에는 넓은 텍스트 안전영역이 있고, 렌더링 후 도형을 덧붙인 흔적이 없다. 이미지 내부에 텍스트, 숫자, 로고, 원·선·화살표·네트워크·아이콘·차트·글리프·UI 요소가 없다. 사용자가 도식 제거를 승인한 뒤에는 도식 부재를 결함으로 보지 않는다.
- [ ] Cards 2-5 본문 요청은 Card 1 표지에 복사하지 않았다. Card 1은 표지형, Cards 2-5는 본문 오버레이형으로 분리했다. `title` 비움, title 하단 배치, 표지 하단 제목 패널, 80px대 하단 제목형 body, Cards 2-5의 paper식 짧은 하단 설명 회귀를 쓰지 않았다.
- [ ] 뉴스 모드: 각 `images` 항목을 이미지 클래스로 분류했고, Card 1은 유일하게 `USER_ORIGINAL_PHOTO`, 카드 2-5는 `GENERATED_CARD_ASSET` 또는 명시 허용된 에셋(모든 `NEUTRAL_DESIGN_ASSET`은 예외로 문서화), `SOURCE_NEWS_MEDIA` 없음.
- [ ] 뉴스 모드: 카드 내부 출처 표기가 꼭 필요하면 매체명/원 출처/발표자 중 하나만 짧게 남겼고, 작은 설명문으로 늘리지 않았다.
- [ ] 정확히 6개의 최종 카드 파일이 존재한다.
- [ ] Card 6은 고정 CTA/FOLLOW 엔딩 카드로, 고정 레이아웃/연락처/화이트 레몬 스타일을 유지하되 세트 특화 가운데 헤드라인을 쓴다. 서브타이틀은 기본으로 비웠고, 쓴 경우에도 작은 설명문처럼 보이지 않는다. 추가 콘텐츠/체크리스트/무관한 SAM 설명이 아니며, 하단 중앙 6개 점/불릿/페이지 인디케이터가 없다.
- [ ] 좌측 하단 브랜드 뱃지가 없다.
- [ ] 업로드된 URL이 모두 HTTP 200을 반환한다.
- [ ] 라이브러리 항목에 6장 카드 URL이 모두 포함된다.
- [ ] `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/library/index.html`을 `/home/ubuntu/workspace/space/infra-aws-static-sites/sites/library/dist/index.html`로 복사했고, 정적 ZIP도 `sites/library/dist/downloads/`에 있다.
- [ ] commit/push 직전 `python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/build_card_news_library.py --check-stage`가 통과했다. `items.json`, slug별 template/source-assets, 공개 HTML, red-team 반영 후 최종 library 변경이 staged/unstaged로 갈라져 있지 않다.
- [ ] `library.aws.shdkej.com` 원격 배포까지 완료했다. `openclaw-backups` 커밋만으로 완료 처리하지 않았고, S3/CloudFront 또는 GitHub Actions 배포 후 공개 HTML에서 새 `id`/제목을 `curl`로 확인했다.
- [ ] 공개 다운로드 ZIP URL이 HTTP 200을 반환한다.
- [ ] 라이브러리 발행 성공 시 카드 이미지를 채팅으로 보내지 않았다 (명시 요청 예외). 채팅 전달 시 6장이 순서대로, 첫 첨부 텍스트에 제목 포함.

## Reporting

한국어 존댓말로 답하세요. 완성된 카드뉴스 작업 보고에 포함할 것:

- 사용한 모드 (`news` / `insight`)와 최종 장수, 핵심 체크리스트 하이라이트 (예: `6장`, `마지막 카드 포함`, `좌측하단 뱃지 없음`).
- Card 1 제목이 `keyword-title` 게이트를 거쳤다는 확인 (수동 대체 시 이유와 절차).
- 카드 문구가 `humanize-korean` 게이트를 거쳤고 사실·수치·고유명사 보존과 강조어 재점검을 마쳤다는 확인.
- Card 6 가운데 헤드라인이 세트를 요약하도록 맞춤화되었고, 작은 서브타이틀/하단 중앙 점/불릿이 없다는 확인. 관련 있을 때 CTA/마지막 카드 색상.
- 최종 URL 검증 완료, 카드뉴스 라이브러리 추가 여부, 페이지 업데이트 시 배포 URL(`https://library.aws.shdkej.com`).
- 로컬 경로는 사용자가 재현성에 대해 물을 때만 언급.
