# LLM Bootstrap Contract

이 문서는 모든 에이전트가 먼저 읽는 **얇은 공용 부팅 계약**이다. 사용자 정체성·서비스 목록·문서 검색 절차의 상세는 Knowledge Lab 정본에만 둔다.

## 에이전트 절대 행동 방침

1. **문서를 먼저 확인한다.** `zg`와 메모리를 활용해 현재 작업의 맥락·기존 결정·관련 운영 기준을 확인한다.
2. **행동 후 문서를 업데이트한다.** 작업 결과와 새로 확인된 운영 기준을 관련 정본 문서에 반영한다.
3. **검증한다.** 변경 결과와 실제 동작을 확인하고, 검증 근거·남은 문제·다음 조치를 기록한다.

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

## 완료 판정과 진행 보고

문서의 원칙을 기억에 의존하지 않고 실행 결과로 판정한다.

- 작업을 시작하기 전에 목적, 산출물, 범위·제외, 성공 증거와 승인 경계를 짧게 확정한다. 하나라도 열려 있으면 가장 큰 불확실성 하나를 먼저 묻는다.
- “하겠다”, “확인하겠다”, “푸시하겠다”고 사용자에게 알렸으면 완료 조건을 충족할 때까지 작업을 이어간다. 중간에 멈추거나 부분 결과를 완료처럼 보고하지 않는다.
- 작업 단계가 바뀔 때마다 현재 확인 결과, 다음 조치, 남은 검증을 짧게 공유한다. 최초 원인 가설이 틀리면 즉시 정정하고, 미검증 상태에서는 해결됐다고 말하지 않는다.
- 완료 전에는 대상 저장소의 경로·Git 여부·원격·현재 브랜치·작업 트리를 실제 명령으로 확인한다. “푸시 완료”는 `git push`의 성공 문구가 아니라 `git rev-parse HEAD`와 `git ls-remote origin <ref>`의 SHA가 일치할 때만 인정한다.
- 위 Git 완료 게이트는 직접 재현하지 말고 `scripts/verify-completion.sh <저장소 경로> [브랜치 또는 ref]`를 실행한다. 스크립트가 `PASS`를 내기 전에는 푸시 완료나 최종 완료를 보고하지 않는다.
- 소스 변경은 build·test·diff를 통과해야 하며, 웹·앱·이미지처럼 사용자가 보는 결과물은 실제 렌더 또는 동작을 확인해야 한다. 배포 작업은 라이브 주소와 실제 동작까지 확인한다.
- 최종 보고에는 상태, 검증 결과, 원격 commit·배포 revision, 남은 리스크, 문서 변경 경로를 포함한다. 이 증거 중 하나라도 없으면 완료 보고를 보류하고 계속 확인한다.
