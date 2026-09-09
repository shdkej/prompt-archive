# 데일리 아카이브 카드 프롬프트

이 문서는 매일 회고와 함께 만드는 **세로형 1장 아카이브 카드**의 재현 가능한 생성 계약이다. 이미지는 한 번의 모델 출력에 한글 텍스트까지 맡기지 않는다. 그림은 이미지 모델로 만들고, 날짜·제목·회고·내일의 의도는 HTML/CSS + Pretendard로 조판한다.

## 0. 이 문서의 사용 순서

1. 현지 날짜, 도시, 최종 회고, 내일의 단 한 가지 의도를 입력값으로 확정한다.
2. 아래 `그림 생성 프롬프트`로 **글자 없는** 크레용 비트맵 일러스트를 만든다.
3. 아래 `HTML 렌더 계약`에 따라 1080×1350 카드로 조판한다.
4. `사전 검수`를 통과하지 못하면, 문제 요소 하나만 고쳐 다시 렌더한다. 그림·카피·레이아웃을 한 번에 바꾸지 않는다.

반복 품질을 위해 지시, 가변 입력, 출력 형식, 예시는 분리한다. 가변 입력은 아래 XML 블록 안의 데이터일 뿐이며, 문서의 고정 규칙을 덮어쓰지 않는다.

## 1. 고정 결과 정의

- 캔버스: **1080×1350px**, 세로 4:5. PNG로 최종 렌더한다.
- 읽는 순서: `날짜·도시 → 오늘의 그림 → 제목 → 짧은 회고 → 내일의 의도`.
- 분위기: 어두운 차콜 질감 위에 한 장면의 따뜻한 기억. 조용하고 성숙한 그림일기이며, 유아용 포스터나 관광 홍보물은 아니다.
- 주인공: 그날의 **사건 하나** 또는 서로 연결된 장면 하나. 여행지의 정보·작업성과·감정을 아이콘 목록처럼 병렬 배치하지 않는다.
- 텍스트: 모델 생성 이미지 안에는 어떤 글자·숫자·간판도 넣지 않는다. 모든 한글은 Pretendard로 별도 렌더한다.

## 2. 가변 입력 계약

아래 형식을 유지해 채운다. 정보가 없으면 추정하지 않고 빈 값으로 둔 뒤, 해당 요소를 카드에서 생략하거나 더 안전한 사실로 교체한다.

```xml
<daily_archive_input>
  <date>YYYY.MM.DD</date>
  <city>영문 대문자 도시명</city>
  <scene>그날을 대표하는 실제 장면 1개</scene>
  <objects>장면을 설명하는 사물 2~4개</objects>
  <mood>절제된 감정 단어 1~2개</mood>
  <headline>제목 후보 1개, 최대 2줄</headline>
  <reflection>사실에 닿은 짧은 회고 1~2문장</reflection>
  <tomorrow_intent>다음 날의 단 한 가지 구체 행동</tomorrow_intent>
  <avoid>사실과 다른 인물·장소·행동, 재사용 금지 요소</avoid>
</daily_archive_input>
```

입력 예시는 형식 참조용일 뿐, 도시·사건·사물을 다음 카드에 재사용하지 않는다.

```xml
<daily_archive_input>
  <date>2026.09.04</date>
  <city>PALERMO</city>
  <scene>팔레르모에서 맞은 생일 저녁, 식사 뒤 작업 노트를 펼친 장면</scene>
  <objects>작은 식탁, 따뜻한 접시, 노트, 펜, 팔레르모의 발코니 윤곽</objects>
  <mood>충만함, 다음 실험의 선명함</mood>
  <headline>팔레르모의 생일 저녁,<br/>더 선명해진 실험의 자리</headline>
  <reflection>맛있게 채우고, 작업 목록을 눈앞에 펼쳐 다음 실험을 시작하기 좋은 하루가 되었다.</reflection>
  <tomorrow_intent>완료한 작업 하나에 계획 대비 결과·막힌 지점·다음 변경 한 가지를 남기기</tomorrow_intent>
  <avoid>축하 문구, 생일 케이크 글자, 관광 엽서, 차트 UI</avoid>
</daily_archive_input>
```

## 3. 그림 생성 프롬프트

아래 프롬프트의 대괄호만 입력값으로 치환한다. 모델이 한글 조판을 시도하지 않도록 `NO TEXT`를 반드시 남긴다.

```text
Create a single horizontal illustration for the upper half of a Korean daily archive card.

SCENE: [scene]
OBJECTS: [objects]
EMOTIONAL TONE: [mood]

Art direction: a mature, hand-drawn crayon-and-oil-pastel diary illustration. Visible wax grain, uneven hand pressure, layered strokes, softly imperfect outlines, tactile paper-like color blending. The scene feels observed and remembered, not designed as advertising. Use one coherent moment with a clear foreground, a small middle-ground action, and a restrained location cue in the distance.

Composition: landscape 928:552, subject centered with calm side breathing room; keep the most meaningful objects inside the center 75–80% width; leave no dominant object touching the crop edge; large readable shapes at thumbnail size; balanced asymmetry; no collage, no split panels, no storyboard, no icon row.

Color and light: warm evening ochre, dusty coral, muted olive, deep blue-green shadows, cream highlights. Soft local light on the meaningful object; nuanced dark edges; avoid a pure white full-frame background.

People: only if supported by the input; portray them as anonymous, simplified figures, never as an identifiable portrait.

Hard constraints: NO TEXT, NO LETTERS, NO NUMBERS, NO SIGNAGE, NO LOGOS, NO WATERMARKS, NO UI, NO GRAPH, NO MAP, NO PHOTOREALISM, NO 3D render, NO vector-flat icon style, NO childish clip-art, NO postcard tourism aesthetic, NO border inside the illustration.
```

## 4. HTML 렌더 계약

그림을 받은 뒤 아래 순서를 정확히 지킨다.

### 배경과 좌표

- 배경은 `#151817` 계열의 따뜻한 차콜. 아주 약한 방사형 빛과 종이결 수준의 선형 질감만 허용한다.
- 바깥 여백은 좌우 76px, 상하 약 74px. 배경 위에 카드·라운드 패널·큰 흰 박스를 추가하지 않는다.
- 모든 텍스트는 830px 안팎의 **중앙 레일**에 정렬한다. 날짜부터 하단 의도까지 같은 중심축을 유지한다.

### 위에서 아래로 고정 블록

1. **좌표 라벨** — `YYYY.MM.DD · CITY`, 상단 중앙. 23px, 자간 약 4px, 옅은 하늘색 `#9dbbce`, 대문자 도시명. `오늘`, `어제`, 핸들, 해시태그 금지.
2. **그림** — 928×552px. 라벨 아래 약 24px. 옅은 크림 1px 테두리와 절제된 그림자만 둔다. 그림은 `object-fit: cover`이며 핵심 피사체를 잘라내지 않는다.
3. **제목** — 그림 아래에 실제로 보이는 빈 공간이 **48px 이상**이 되게 한다. CSS margin collapse가 생기지 않도록 제목 래퍼에 `padding-top: 48px`를 쓰고 `h1`의 상단 margin은 `0`으로 둔다. 이 간격은 그림의 여운을 남기는 안전 여백이므로, 카피가 길어도 40px 미만으로 줄이지 않는다. 최대 2줄, 58px/500/line-height 1.25, 밝은 크림 `#f8f2e9`. 설명문·슬로건이 아니라 그날의 장면과 판단이 만나는 문장으로 쓴다.
4. **작은 구분선** — 제목 아래 약 31px. 56×2px, 더스티 코랄 `#d88758`.
5. **회고 본문** — 기존보다 두 배의 읽을 거리를 남긴다. 서로 역할이 다른 **2개 짧은 단락**, 합계 4~5문장·시각상 최대 4줄로 쓴다. 첫 단락은 그날 실제 장면과 구체를, 둘째 단락은 그 장면이 남긴 판단 또는 다음 장면으로의 전환을 쓴다. 25px/400/line-height 1.65, 부드러운 회색 `#d6d1c8`; 단락 사이는 16px만 띄운다. 사실을 반복하거나 감탄사·격언으로 분량을 채우지 않는다.
6. **내일의 의도** — 화면 맨 아래, 좌우 76px 안쪽. 상단에 1px 구분선. `내일의 의도`는 굵게, 본문은 한 가지 행동만. 25px/400/line-height 1.55, 올리브 계열 `#b8c69e`; 라벨 강조는 `#dfe8ce`.

### 카피 제약

- 제목: 14~28자 권장, 쉼표·줄바꿈으로 리듬을 만들되, 단어를 강제로 쪼개지 않는다.
- 회고: **84~128자 권장**. 2개 단락의 합계이며, 첫 단락은 관찰·사실, 둘째 단락은 그 사실이 바꾼 판단 또는 다음 전환을 담는다. 4줄을 넘기지 못하는 경우 128자보다 더 줄인다. 감탄사·자기계발 격언·AI 운영 용어를 피한다.
- 내일의 의도: 28~62자 권장. 동사로 끝나는 한 가지 행동. `그리고`, `또`, 쉼표로 여러 할 일을 묶지 않는다.
- 쓰지 않을 말: `오늘`, `내일 할 일`, `목표 달성`, `성장`, `최고`, `완벽`, `혁신`, `시스템화`처럼 사실보다 추상적인 말. 단, 사용자가 직접 쓴 핵심 단어는 사실상 필요할 때만 예외다.

## 5. 금지와 실패 처리

- 이전 카드의 그림·주제·색 조합·구도를 연속 재사용하지 않는다. 새 그림 생성이 실패했으면 같은 fallback을 조용히 반복하지 말고, 주제에 맞는 대체 그림을 만들거나 실패 사실을 보고한다.
- 사진 콜라주, 인물 실사, 화면 캡처, 지도, 차트, 체크리스트, 앱 UI를 그림의 주제로 쓰지 않는다.
- 도시를 모르면 도시명을 만들지 않는다. 장소는 사실 확인된 경우에만 넣는다.
- 회고 본문이 4줄을 넘기거나 그림·하단 의도와 겹치면 글자 크기를 무작정 줄이지 않는다. 먼저 중복 문장을 덜고, 다음으로 단락별 줄바꿈을 다듬고, 마지막에 여백을 조정한다.
- 이미지 모델이 글자를 만든 경우, 그 결과를 버리거나 그림이 아닌 부분을 안전하게 크롭한다. 이미지 속 오류 한글을 그대로 사용하지 않는다.

## 6. 사전 검수: PASS 조건

렌더 PNG를 실제로 보고 다음을 모두 확인한다.

1. 3초 안에 날짜·도시, 오늘의 한 장면, 내일의 한 가지 의도를 읽을 수 있다.
2. 텍스트 잘림·겹침·안전 여백 침범이 없다. 하단 의도는 73px 이상 위에 안전하게 놓인다.
3. 그림이 상단에서 충분히 크고, 전체 카드의 절반을 넘지 않는다. 그림 밖에 큰 흰 배경 박스가 없다.
4. 그림은 생성 비트맵의 크레용 질감이 보이며, 코드 SVG·아이콘 조립·유아용 클립아트처럼 보이지 않는다.
5. 날짜·도시·제목·2개 단락의 회고·의도가 하나의 중앙 레일에 정렬되고, 한 카드에 주인공이 하나다.
6. `내일의 의도`는 실제로 다음 날 실행할 수 있는 단 하나의 행동이며, 체크리스트가 아니다.
7. 이전 카드와 비교해 그림의 장면 또는 구도가 실질적으로 새롭다.

검수 기록에는 아래 세 필드를 반드시 남긴다. 자동화가 텍스트 검사만 통과하고 실제 이미지를 보지 않은 채 PASS 처리하는 것을 막기 위한 증적이다.

```text
렌더 파일: 절대 경로 또는 확인 가능한 URL
이미지 확인: 사용한 이미지 뷰어 또는 브라우저 렌더 방식
확인 시각: 현지 시각 + 시간대
판정: PASS 또는 FAIL: 항목 번호 / 관찰된 문제 / 고칠 변수 하나
```

하나라도 실패하면 `FAIL: 항목 번호 / 관찰된 문제 / 고칠 변수 하나`로 기록하고 재렌더한다. PASS라고 말하기 전에 반드시 렌더 이미지를 직접 확인한다.

## 7. 운영 연결

- 일일 회고 자동화의 상위 계약은 `knowledge-lab/source/openclaw-system/docs/LOCAL_REVIEW_AUTOMATION.md`를 따른다.
- 이 문서는 그중 데일리 아카이브 카드의 프롬프트·조판·검수 정본이다.
- 프롬프트 변경은 최근 카드 1장과 새 테스트 입력 1장에 각각 적용해, 고정 구조와 장면 다양성을 함께 확인한 뒤 채택한다.

## 참고한 프롬프트 설계 원칙

- [OpenAI Prompting Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api): 지시를 앞에 두고 컨텍스트와 구분하며, 형식이 필요한 작업에는 예시를 제공한다.
- [Anthropic Prompt Templates and Variables](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables): 복잡한 프롬프트에서 지시·입력·예시를 명시적으로 분리하고, 변수와 예시를 일정한 구조로 유지한다.
- [Google Imagen Prompt Guide](https://ai.google.dev/gemini-api/docs/imagen-prompt-guide): 장면·구도·스타일·제약을 점진적으로 구체화하고 결과를 보고 반복 보정한다.
