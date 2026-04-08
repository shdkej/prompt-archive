# Agent Permissions

> Heartbeat Agent의 자율 실행 범위를 정의한다.
> 에이전트는 이 문서에 명시된 범위 안에서만 자율적으로 행동한다.

## L0 - 자율 실행 (변화 있을 때만 알림)

- 파일 읽기, 코드 검색, 구조 분석
- 웹 리서치, 문서 참조, 라이브러리 문서 조회
- 상태 체크 (git status, 파이프라인 상태, 서비스 헬스체크)
- 문서 드래프트 작성 (infinity/drafts/ 하위에만)
- 읽기 전용 테스트 실행 (기존 테스트 수트)
- 로그 분석, 에러 패턴 탐지

## L1 - 실행 후 결과 알림

- 소스 코드 수정
- 새 파일 생성 (프로젝트 디렉토리 내)
- git 브랜치 생성
- 테스트 작성 및 실행
- 로컬 빌드
- lint, format 자동 수정
- INTENTS.md status 업데이트
- infinity/reports/ 결과 기록
- infinity/ 내 변경사항 커밋 & 푸시 (리포트, 상태 업데이트, GATES.md 등)
- prompt-archive 레포 내 파일 수정 후 커밋 & 푸시

## L2 - 승인 후 실행

- 다른 레포에 git push (monitoring_personal, space 등)
- PR/MR 생성
- 외부 서비스 API 호출 (Slack, Teams, Graph API, SharePoint)
- 배포 트리거 (ArgoCD, GitLab CI)
- SharePoint 리스트/라이브러리 생성 또는 수정
- 다른 사람에게 메시지 발송

## L3 - 금지 (사용자가 직접 수행)

- git push --force, reset --hard
- 브랜치 삭제, 파일 삭제 (rm -rf)
- 프로덕션 환경 변경
- 비용 발생 작업 (클라우드 리소스 생성/삭제)
- 인증 정보 변경, 시크릿 수정
- 다른 사용자 권한 변경
