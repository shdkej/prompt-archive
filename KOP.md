# KOP 업무 가이드

프로젝트별 KOP 업무를 위한 가이드입니다.

## 프로젝트

- kop-web
  - 역할: kolonmall 및 vertical 사이트 화면 영역 개발
  - 기술 스택: nextjs 9, typescript, styled-components, tailwindcss, storybook
  - 특이사항:
    - kop-api에서 존재하는 graphql 쿼리를 사용하여 개발
    - 커밋 전 변경된 파일에 대해 lint 체크 필수 (`npx eslint {파일경로}` 또는 `npx eslint --fix {파일경로}`)
- kop-api
  - 역할: kolonmall 및 vertical 사이트 API 개발
  - 기술 스택: nodejs, hasura (graphql), typescript, express
  - 특이사항: sofa-api를 사용하여 hybris에 있는 enpoint도 graphql 쿼리로 호출 가능
- kop-cms
  - 역할: kolonmall 및 vertical 사이트 CMS 개발
  - 기술 스택: nodejs, typescript, styled-components, tailwindcss
  - 특이사항: kop-api에서 kop-admin-api 영역의 api를 호출하여 사용중
- hybris
  - 역할: kolonmall 및 vertical 사이트 백엔드 서버 및 일부 페이지는 hbs를 통해 개발
  - 기술 스택: hybris, java, spring, hbs, jquery
  - 템플릿 구조 (`kopstorefront/web/webroot/WEB-INF/views/`):
    - `kop/`: **공통 전체 사이트** 템플릿. 사이트별 수정 시 반드시 kop 폴더를 먼저 확인하고 작업
    - `kolonsport/`, `thecartgolf/`, `gfore/` 등: 개별 사이트 전용 템플릿
  - 특이사항: 사이트별 템플릿이 없으면 kop 폴더의 공통 템플릿이 사용됨

## 안내사항

- 각 프로젝트 루트에 AGENTS.md 파일이 있다면 참고하여 프로젝트 별로 작업을 진행한다

## 작업흐름

- 아사나
- 깃랩 브랜치
- 깃랩 MR 생성
- 빌드 확인 후 배포

## 주요 규칙

- 아사나 본문에서 gitlab 이슈번호 확인
- 브랜치 태그 - gitlab 이슈번호를 앞에 적고 브랜치명 생성 `ex: #2463-add-new-page`
- 작업 PLAN 생성
- 검토 후 작업 진행 후 커밋 생성
- 커밋은 한글로 작성
- MR 생성

## Slack 설정

- 배포 채널 ID: `C07K6SXSU8Z`
- Webhook URL: 환경변수 `KOP_SLACK_WEBHOOK_URL` 참조

## 작업 후 테스트 자동화

- 빌드 단계 완료 되면 슬랙으로 argocd에 deploy를 할 수 있고 deploy가 되면 해당 ingress의 주소로 가서 수정 내용을 체크할 수 있다
  - gitlab 백그라운드 모니터링
  - 슬랙 메시지 보내기
  - playwright 테스트 시나리오 생성
  - 테스트 후 알림

#### 테스트 시나리오

- playwright로 테스트 시나리오 생성
