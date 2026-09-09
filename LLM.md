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
- 앱·웹앱을 만들거나 변경할 때는 대상 소스 저장소에 `README.md`를 반드시 작성·갱신한다. README는 최소한 목적, 사용자 문제, 핵심 기능, 실행/개발 방법, 데이터·외부 의존성, 테스트·배포 방법, 알려진 한계를 담는다.
- 프로젝트 안내와 README의 정보 구조는 MECE하게 만든다. 같은 설명을 여러 섹션에 반복하지 않고, 서로 겹치지 않는 범주로 전체를 빠짐없이 설명한다. 구현 중 결정·범위·완료 기준은 KL 중앙 문서에, 소스별 사용법과 기술 상세는 해당 프로젝트 README에 둔다.

## 배포 소유권과 저장소 경계

배포 유형은 구현 저장소와 배포 저장소의 책임을 먼저 분리한다. `Space`는 인프라·배포 선언·GitOps만 소유하며, 서비스 코드의 임시 보관소가 아니다.

- **정적 사이트**: `space/infra-aws-static-sites/sites/<app>/` 안에서 소스/정적 산출물과 AWS 배포를 함께 관리한다. `registry.json` 등록 → Terraform 인프라 반영 → `dist/` 변경 push가 기본 경로다.
- **Lambda**: 함수 코드와 테스트·패키징은 `/home/ubuntu/workspace/services/<service>/`의 **독립 Git 저장소**가 소유한다. Space에는 그 배포에 필요한 IAM·Lambda·API Gateway/Function URL·CloudFront 연결 Terraform만 둔다.
- **Next.js**: 앱 코드, `package.json`, lockfile, `Dockerfile`, 테스트와 앱 README는 `/home/ubuntu/workspace/apps/<app>/`의 **독립 Git 저장소**가 소유한다. Space에는 이미지 참조, Kubernetes `Deployment`/`Service`/`Ingress`, Argo CD 애플리케이션 같은 배포 선언만 둔다.

신규 Lambda·Next.js 작업 또는 기존 항목의 실질적 수정은 Space 안에 코드를 추가하는 것으로 끝내지 않는다. SAM은 먼저 독립 워크스페이스 폴더와 저장소를 만들고, 목적·로컬 실행·빌드·테스트·배포 계약을 담은 README 및 표준 실행 명령을 구성한 뒤 Space의 배포 선언을 연결할 책임이 있다. 현재 `space/infra-aws-static-sites/lambda/`와 `space/apps/`의 코드는 레거시 배치이므로, 새 항목의 본보기가 아니다. 해당 항목을 다음에 크게 수정할 때도 같은 경계로 이전한다.

## 반복 가능한 운영 기록

배포·모니터링·운영 경로를 새로 만들거나 바꾸거나 확인한 작업은, 구현 저장소와 연결된 배포 저장소의 문서에 **소스 정본, 구성요소 관계, 배포·검증 순서, 사용하지 않는 레거시 경로**를 함께 갱신한다. 완료 보고에는 수정한 문서 경로와 바뀐 규칙을 반드시 명시하고, source commit·배포 revision·실제 검증 결과·남은 검증 경계를 구분해 적는다. 문서가 없는 상태에서 구두 보고만으로 반복 가능한 운영 절차를 완료 처리하지 않는다.
