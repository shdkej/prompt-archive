# KOP 배포 자동화 설정 가이드

## 개요

KOP 프로젝트의 배포 프로세스를 자동화하기 위한 설정 가이드입니다.

## 구성 요소

1. **Slack Bot** (`purple-vertical-bot`) - 배포 명령어 처리
2. **GitLab CI** - MR 머지 시 Jenkins 빌드 트리거
3. **Asana** - 배포 태스크 관리
4. **ArgoCD** - 배포 동기화

## 환경 변수 설정

### Slack Bot (.env)

```bash
# 기존 설정
SLACK_BOT_TOKEN=xoxb-xxx
SLACK_SIGNING_SECRET=xxx
SLACK_APP_TOKEN=xapp-xxx

# GitLab 설정
GITLAB_URL=https://gitlab.kolonfnc.com
GITLAB_TOKEN=xxx
GITLAB_HYBRIS_PROJECT_ID=123
GITLAB_CMS_PROJECT_ID=456
GITLAB_WEB_PROJECT_ID=789
GITLAB_API_PROJECT_ID=101

# Asana 설정
ASANA_API_TOKEN=xxx
ASANA_WORKSPACE_ID=xxx
ASANA_DEPLOY_PROJECT_ID=xxx

# Slack 채널
SLACK_DEPLOY_CHANNEL_ID=C12345678
```

### GitLab CI Variables

각 프로젝트에 다음 CI/CD Variables를 설정:

| Variable | Description |
|----------|-------------|
| `JENKINS_URL` | Jenkins 서버 URL |
| `JENKINS_USER` | Jenkins 사용자 ID |
| `JENKINS_API_TOKEN` | Jenkins API 토큰 |
| `BUILD_TOKEN` | Jenkins 빌드 트리거 토큰 |

## Slack 명령어

### `/배포준비`

배포 준비 워크플로우를 시작합니다.

**동작:**
1. 모달에서 배포 정보 입력 (프로젝트, 등급, DB 업데이트)
2. GitLab MR에서 배포 내역 자동 추출
3. Asana 태스크 생성
4. 배포 채널에 메시지 전송

### `/배포내역 [프로젝트]`

특정 프로젝트의 배포 내역을 조회합니다.

```
/배포내역 hybris
/배포내역 cms
```

### `/빌드상태 [프로젝트]`

프로젝트의 최신 빌드 상태를 조회합니다.

```
/빌드상태 web
```

## 배포 설정 파일

`deploy-config.yml`에서 배포 설정을 관리합니다.

```yaml
projects:
  hybris:
    gitlab_project_id: ${GITLAB_HYBRIS_PROJECT_ID}
    deploy_tag_pattern: "deploy-*"
    trigger_branch: main

settings:
  gitlab_url: ${GITLAB_URL}
  asana_deploy_project_id: ${ASANA_DEPLOY_PROJECT_ID}
```

## 워크플로우

```
1. /배포준비 실행
   ↓
2. 모달에서 정보 입력
   - 프로젝트 선택 (hybris, cms, web)
   - 배포등급 선택 (A~E)
   - DB 업데이트 여부
   ↓
3. 자동 처리
   - MR 기반 배포 내역 추출
   - Asana 태스크 생성
   - 배포 메시지 전송
   ↓
4. 배포 진행
   ↓
5. 배포완료 처리
```

## 트러블슈팅

### GitLab API 오류

- `GITLAB_TOKEN`이 올바른지 확인
- 프로젝트 접근 권한 확인

### Asana 태스크 생성 실패

- `ASANA_API_TOKEN` 유효성 확인
- `ASANA_DEPLOY_PROJECT_ID`가 올바른 프로젝트인지 확인

### 배포 내역이 비어있음

- 마지막 배포 태그 이후 머지된 MR이 없을 수 있음
- 태그 패턴(`deploy_tag_pattern`)이 올바른지 확인
