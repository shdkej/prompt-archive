# LLM Bootstrap Contract

이 문서는 모든 에이전트가 먼저 읽는 **얇은 공용 부팅 계약**이다. 사용자 정체성·서비스 목록·문서 검색 절차의 상세는 Knowledge Lab 정본에만 둔다.

## 시작 순서

1. `/home/ubuntu/workspace/knowledge-lab/context-routes.json`에서 요청 route를 고른다.
2. Context Pack의 공통 문서와 route 필수 문서를 읽는다.
3. 지식 조회·추천·판단은 먼저 `agent-wiki/README.md`의 중앙 목차와 컴파일 문서를 확인한다. 근거·최신성·원문 확인이 필요할 때만 허용된 KL raw source를 ingest 상태와 함께 확인한다.
4. Intent 또는 작업 기록에 Context Pack, 실제 읽은 문서, 검색 근거를 남긴다. Infinity 실행자는 동일 Pack을 재확인한다.

## 정본 연결

- 사용자 장기 맥락: `knowledge-lab/source/openclaw-system/docs/USER_CONTEXT.md`
- 서비스·저장소 연결: `knowledge-lab/source/openclaw-system/docs/SERVICE_REGISTRY.md`
- 문서 검색·인계·승격 절차: `knowledge-lab/source/openclaw-system/docs/DOCUMENT_SEARCH_PIPELINE.md`
- 원본·ingest·agent-wiki 경계: `knowledge-lab/README.md`, `knowledge-lab/schema/agent-rules.md`
- 도메인 워크플로우·스킬·설계 가이드: Prompt Archive의 관련 문서
- 반복 실행·트리거·테스트 기준: `OPERATING_REFERENCE.md`

## 공통 행동 기준

- 한국어 존댓말로 결과와 근거를 명확히 전달한다.
- 검증되지 않은 raw 자료를 확정 지식처럼 쓰지 않는다.
- 서비스별 실제 저장소와 운영 정본을 우선한다.
- 외부 공개, 비용, 권한, 자격증명, 파괴적 작업은 별도 승인 경계를 지킨다.
