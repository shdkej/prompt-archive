# Operating Reference

`LLM.md`에서 분리한 Prompt Archive 소유의 반복 실행 규칙이다. 사용자 맥락·서비스 목록·문서 검색은 Knowledge Lab 정본을 따른다.

## 작업 기본값

- 작업 변경은 계획 → 실행 → 측정 → 개선의 피드백 루프로 남긴다.
- 프로덕트 제작처럼 기획·구현·마케팅·운영이 얽히면 `/workflow-master`를 사용한다. 단순 질문·조회·단일 스킬은 예외다.
- 테스트 안내가 없으면 가장 작은 성공 사례를 실행한다. PRD가 있으면 PRD별 성공 사례를 둔다.
- 설계/아키텍처 작업은 `TECH_SPEC.md`, 복잡한 오케스트레이션은 관련 OMC 가이드를 필요한 경우에만 읽는다.

## 트리거와 도구

- 출근·어제 업무·퇴근 표현은 Daily Feedback 워크플로우의 입력이다.
- 사진·스크린샷·생성 이미지 업로드와 문서 이미지 링크는 image-upload 절차를 따른다. 원본은 `original`, 가공 산출물은 `derived`로 보관하고 URL 확인 후 연결한다.
- 스킬 생성은 측정·평가·피드백 루프를 포함하고 전후 비교로 검증한다.

## 환경·참고

- 프로젝트별 런타임과 가상환경은 해당 저장소의 README를 우선한다.
- 인프라·배포는 Space, 모니터링은 Monitoring Personal, OpenClaw 운영은 Knowledge Lab의 route별 문서를 따른다.
