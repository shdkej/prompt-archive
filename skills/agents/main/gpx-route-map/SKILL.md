---
name: gpx-route-map
description: GPX 트랙을 Mapbox 경로 이미지/여행 추억 포스터로 렌더링하는 스킬. 원시 GPX XML을 채팅 컨텍스트에 불러오지 않는 것이 핵심 규칙. 사용 시기 - (1) 사용자가 GPX/XML 경로 파일을 보낼 때, (2) 경로 지도·여행 경로 비주얼(YouTube/Threads/일일 회고/세계 여행 추억용) 요청, (3) insight-card-maker의 여행 카드에 공간 맥락 이미지가 필요할 때.
---

# GPX Route Map

사용자가 GPX/XML 경로 파일을 보내거나, 한 장짜리 경로 지도를 요청하거나, Mapbox로 경로를 렌더링할 수 있는지 묻거나, YouTube·Threads·일일 회고·세계 여행 추억용 여행 경로 비주얼을 원할 때 사용합니다.

핵심 규칙: 큰 GPX XML을 채팅에 붙여넣거나 다시 읽지 마세요. `/home/ubuntu/.openclaw/media/inbound/` 아래의 로컬 파일 경로나 이미 저장된 GPX 경로를 우선 사용하고, 요약 수치와 출력 이미지만 보고합니다.

`insight-card-maker`와 함께 사용할 때는 경로 지도를 두 번째 카드의 공간 맥락 이미지로 렌더링합니다. 카드 1이 감정적으로 후킹하고 카드 3-5가 인사이트를 전달할 수 있도록, 시각적으로 차분한 지도/포스터와 최소한의 텍스트를 우선합니다. 카드뉴스 경로 페이지에서는 시작과 끝이 시각적으로 분명히 드러나게 하세요. 지도에 큰 S/E 핀을 쓰고, 하단 패널에 시작/끝 정보 카드를 별도로 배치합니다.

## Canonical Files

- Renderer: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/render_gpx_mapbox_route.py`
- Output root: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/mapbox-route-tests/`
- World travel ledger: `/home/ubuntu/workspace/knowledge-lab/source/openclaw-system/docs/WORLD_TRAVEL_PROJECT.md`

## Workflow

1. GPX 파일을 찾습니다.
   - 대화 컨텍스트에 복사된 전체 XML이 아니라 첨부된 미디어 파일 경로를 우선합니다.
   - 파일이 트랜스크립트 일부에만 있다면, 원본 문서를 다시 요청하거나 부분 샘플임을 명확히 표시해 렌더링합니다.
2. 스크립트로 렌더링합니다.

```bash
python3 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/scripts/render_gpx_mapbox_route.py \
  /path/to/source.gpx \
  --out /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/reports/mapbox-route-tests/<slug>.png \
  --theme atlas \
  --format poster \
  --locale ko \
  --title "Route Memory" \
  --subtitle "Yul GPX route rendered with Mapbox"
```

3. 테마를 선택합니다.
   - `atlas`: 편집 디자인풍 여행 추억 룩, 무난한 기본값.
   - `night`: 다크 네온 경로, 모션/영상 무드에 적합.
   - `satellite`: 지형/실제 지형 검토용.
   - `clean`: 단순한 실무용 지도.
   - 한국어 포스터 라벨에는 `--locale ko`를 사용합니다. 이는 카드/포스터 정보 레이어를 한국어로 처리하며, 기반이 되는 Mapbox 지명 라벨까지 바꾸지는 않습니다.
   - 한국어 지도 지명 라벨을 완전히 적용하려면 Mapbox Studio에서 한국어/로컬 라벨 커스텀 스타일이 필요합니다. 스타일 id가 존재하면 렌더링 전에 커스텀 테마로 추가합니다.
4. 결과 PNG를 간결한 한국어 요약과 함께 보냅니다.
   - 원본/필터/렌더링 포인트 수, 시작/끝, 거리, 시각 범례를 포함합니다.
   - 원시 XML은 포함하지 않습니다.
5. 결과가 상시 여행 워크플로우에 영향을 준다면, 재사용 가능한 교훈을 일일 메모나 `WORLD_TRAVEL_PROJECT.md`에 업데이트합니다.

## Notes

- 로컬 환경에 `MAPBOX_API_KEY` 또는 `MAPBOX_ACCESS_TOKEN`이 필요합니다.
- 스크립트는 중복/지터 포인트를 필터링하고, Mapbox URL 길이에 맞게 경로를 솎아내며, 거리를 계산하고, 이미지 옆에 `.txt` 메타데이터 파일을 작성합니다.
- 포스터 출력은 기본적으로 더 큰 Mapbox 시작/끝 핀과 포스터 패널의 시작/끝 카드로 경로 종단점을 강조합니다.
- 경로에 GPS 점프가 있으면 `--max-jump-meters`를 조정하고, 거리가 인증된 주행 거리계가 아니라 필터링된 값임을 언급합니다.
