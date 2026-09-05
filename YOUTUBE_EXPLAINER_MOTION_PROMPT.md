# 유튜브 설명 모션 프롬프트

이 문서는 유튜브 영상 중간에 삽입하는 **1~3초 설명용 모션 그래픽**을 Remotion으로 반복 제작하는 계약이다. 한 장면은 한 개념만 설명한다. 이미지 모델은 필요할 때만 글자 없는 보조 일러스트를 만들고, 모든 한글·도형·배치·애니메이션은 Remotion + Pretendard로 렌더한다.

## 0. 사용 순서

1. 아래 `<motion_input>`의 빈칸을 채운다.
2. `제작 프롬프트` 전체와 입력 블록을 구현 에이전트에 전달한다.
3. MP4를 렌더하고 시작·중간·마지막 프레임을 실제로 본다.
4. 검수에 실패하면 한 번에 하나의 변수만 수정해 다시 렌더한다.

입력값은 장면의 재료일 뿐이다. 아래 고정 규칙을 덮어쓰지 않는다.

## 1. 고정 결과 정의

- 출력: **1920×1080, 30fps, H.264 MP4**, 기본 2.4초(72프레임). 1.2~3초 범위에서만 조정한다.
- 용도: 편집 타임라인의 설명 컷. 영상 자체에는 자막을 넣지 않으며, 하단 18%는 편집 자막용 안전 영역으로 비워 둔다.
- 화면: 오프화이트(`#F8FAF8`) 바탕, 48px 격자, 검은 선과 제한된 검정 면. 라이트·정돈·차분한 인포그래픽이다.
- 주인공: **개념 하나 + 객체 관계 하나 + 결론 라벨 하나**. 장면마다 카드/아이콘을 무작정 늘리지 않는다.
- 텍스트: Pretendard. 이미지 생성 모델에게 한글 조판을 맡기지 않는다.
- 기본 등장 순서: `상단 문장 → 왼쪽 출발 객체 → 연결선/관계 라벨 → 오른쪽 결과 객체 → 하단 결론`.

## 2. 가변 입력 계약

```xml
<motion_input>
  <topic>한 문장으로 말할 설명 주제</topic>
  <headline>상단에 보일 14~26자 문장</headline>
  <source_label>왼쪽 객체 안의 짧은 라벨, 최대 7자</source_label>
  <source_object>왼쪽을 상징하는 객체: 사람, 도구, 장소, 생각 등</source_object>
  <relation_label>연결선 위의 짧은 관계 문구, 최대 8자</relation_label>
  <result_label>오른쪽 객체 안의 결론 라벨, 최대 2줄·각 9자</result_label>
  <result_object>오른쪽을 상징하는 객체: 도시, 선택, 변화, 결과 등</result_object>
  <takeaway>하단에 밑줄로 강조할 결론, 최대 12자</takeaway>
  <accent>black | moss | cobalt 중 하나. 기본 black</accent>
  <duration_sec>1.8~3.0. 기본 2.4</duration_sec>
  <avoid>넣으면 안 되는 요소·표현·사실</avoid>
</motion_input>
```

### 여행 예시

```xml
<motion_input>
  <topic>여행은 이동 그 자체보다 새로운 감각을 만나는 과정이다</topic>
  <headline>여행은 이동보다, 새로운 감각을 만나는 일</headline>
  <source_label>나의 출발</source_label>
  <source_object>단순 선형 종이비행기</source_object>
  <relation_label>낯선 곳으로</relation_label>
  <result_label>새로운 도시\n새로운 나</result_label>
  <result_object>단순 선형 지도 핀</result_object>
  <takeaway>여행의 진짜 목적</takeaway>
  <accent>black</accent>
  <duration_sec>2.4</duration_sec>
  <avoid>실제 위치명, 관광 사진, 지도 타일, 화면 자막, 로고</avoid>
</motion_input>
```

## 3. 제작 프롬프트

아래 코드 블록 전체를 사용하고, 끝에 `<motion_input>`을 붙인다.

```text
Create a reusable Remotion composition for a short Korean YouTube explainer insert.

OUTPUT CONTRACT
- Render one H.264 MP4 at 1920x1080, 30fps, using duration_sec from the input.
- The scene must still read clearly when paused at the final frame.
- Use Pretendard for all Korean type. Render all text in HTML/React; never generate text inside a raster image.
- Do not include burned-in captions. Reserve the bottom 18% of the canvas as an empty subtitle-safe area, except for the small takeaway centered above its lower boundary.

VISUAL SYSTEM
- Canvas: warm off-white #F8FAF8 with a subtle 48px square grid (#DCE4DE at low opacity). No gradients, photos, glass UI, shadows, or 3D effects.
- Color: #161616 for type and linework. Use the selected accent only for the result object fill or a small emphasis, never as a second competing visual system.
- Type: one bold headline at the top center; labels must be short and have clear hierarchy. Use a Korean-friendly weight 700–800, tight but readable tracking.
- Shapes: thin 3px black strokes, 24–30px corner radius, calm breathing room. Use simple original line icons made from SVG paths; no emoji, stock icon sets, logos, maps, or screenshots.
- Layout: place the object relationship group in the visual center. Keep a minimum 90px gap between the lowest object edge and the takeaway. Keep at least 110px horizontal outer margins. Center the *whole group*, not each individual object.

COMPOSITION
1. Headline: top-center, approximately y=120–170.
2. Source object: left-center, around x=380, y=420. A white outlined object, 300–360px wide.
3. Relation: a horizontal connecting line through the group center with a short label floating above it. The label must never touch either object.
4. Result object: right-center, around x=1450, y=420. It may use the selected accent fill, 320–390px wide.
5. Takeaway: centered around y=875–925, with a 3–4px underline. It must not overlap the object group or subtitle-safe area.

MOTION TIMELINE
- 0.00–0.18s: grid is already visible; headline fades upward by 12–18px.
- 0.18–0.55s: source object scales from 0.94 to 1.0 and fades in with a restrained spring.
- 0.50–0.95s: connector line draws from left to right; relation label fades in after the line passes it.
- 0.78–1.25s: result object fades/scales in. Its icon appears 3–5 frames after its surface.
- 1.35–1.70s: takeaway rises 10px and underlines itself.
- Hold the complete composition for at least 0.55s. No looping, bouncing, camera movement, blur, or exit animation.

IMPLEMENTATION RULES
- Create one composition with named input props corresponding to motion_input. Do not hard-code the example copy into reusable logic.
- Derive frames from duration_sec × fps. Keep animation offsets proportional for shorter or longer renders.
- Use only CSS/SVG/React unless a source image is explicitly supplied. If a supplied image is used, treat it as one context object and keep it free of text.
- Use interpolation with clamp and restrained spring settings (no overshoot visible at normal playback).
- Keep the layout responsive to 16:9 output and expose headline, labels, accent, and icon choices as props.

DO NOT
- Do not use a card-grid dashboard, multiple parallel ideas, generic AI imagery, over-decoration, thick black frames, or excessive rounded boxes.
- Do not place a large object, rule, or text inside the bottom subtitle-safe area.
- Do not let labels collide, wrap awkwardly, or touch the connector line.
- Do not imitate a named creator, video, or brand. Apply only the abstract visual principles in this prompt.

VALIDATION
Before declaring done, render and inspect frames at 0.0s, 0.8s, 1.5s, and the final frame. Confirm: (1) the relationship is readable in 3 seconds, (2) every Korean string is legible, (3) objects are centered as a group, (4) takeaway has clear separation, and (5) the MP4 duration and resolution match the input.
```

## 4. GPT Image 보조 이미지 프롬프트 (선택)

객체가 단순 선형 아이콘으로 부족할 때만 사용한다. 생성 결과에는 글자를 넣지 않고, Remotion에서 원형/사각 프레임과 한글 라벨을 따로 붙인다.

```text
Create one isolated editorial object for a minimal Korean YouTube explainer motion graphic.

SUBJECT: [result_object or source_object]
STYLE: clean black ink line drawing with one restrained [accent] area, quiet editorial diagram object, warm off-white background.
COMPOSITION: one centered subject, 1:1 square, generous empty margins on all sides, strong silhouette at small size.
HARD CONSTRAINTS: NO TEXT, NO LETTERS, NO NUMBERS, NO LOGOS, NO WATERMARKS, NO UI, NO MAPS, NO PHOTOREALISM, NO 3D, NO gradients, NO busy background, NO decorative frame.
```

## 5. 사전 검수

렌더 MP4를 재생하고 최종 프레임 이미지를 실제로 본 뒤 아래를 모두 통과해야 한다.

1. 3초 안에 `무엇이 무엇으로 연결되는지`와 하단 결론을 읽을 수 있다.
2. 전체 객체 그룹이 가로·세로 기준 시각적 중앙에 있고, 하단 결론과 최소 90px 이상 떨어져 있다.
3. 상단 문장, 관계 라벨, 객체 라벨, 하단 결론 간에 겹침·잘림·과도한 줄바꿈이 없다.
4. 각 객체는 0.2~0.5초 간격으로 순차 등장하며, 과장된 bounce·zoom·카메라 이동이 없다.
5. 하단 18% 자막 안전 영역에 큰 객체나 라인이 침범하지 않는다.
6. 모델 생성 이미지가 쓰였다면 이미지 속 글자·로고·워터마크가 없고, 한국어 텍스트는 모두 HTML/Pretendard로 렌더됐다.
7. MP4는 1920×1080, 30fps이고 요청한 길이에서 ±0.1초 안이다.

실패하면 다음 형식으로 하나의 변수만 바꾼다.

```text
FAIL: [검수 번호] / [관찰된 문제] / [바꿀 변수 하나]
예: FAIL: 2 / 오른쪽 객체가 하단 결론에 너무 가까움 / result object top을 70px 올리기
```

## 6. 다음 사용 방식

주제와 위 XML만 보내면 됩니다. 기본값은 2.4초·16:9·오프화이트 격자·검정 선형 객체·하단 자막 안전 영역입니다.
