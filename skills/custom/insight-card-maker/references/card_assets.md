# 카드 이미지 선택과 제작

**목차** · [News Mode Image Classes](#news-mode-image-classes) · [Cards 2-5 Generated Asset Direction](#cards-2-5-generated-asset-direction) · [Saem Character Rule](#saem-character-rule)

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
  - provenance: `asset.json`의 출처를 확인한 뒤 해당 환경에서 PNG를 실제로 열 수 있을 때만 사용합니다. ignored `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/card-news/runs/` 산출물은 생성 당시 참고 로그로만 남기고, 스킬이나 새 config의 필수 `source_reference`로 쓰지 않습니다.
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
