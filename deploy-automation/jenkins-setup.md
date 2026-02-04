# Jenkins 설정 가이드

## 개요

GitLab MR 머지 시 자동으로 Jenkins 빌드를 트리거하기 위한 설정 가이드입니다.

## Jenkins 설정

### 1. 빌드 원격으로 유발 활성화

각 Jenkins job에서 다음 설정을 활성화합니다:

1. Job 설정 → "빌드 유발" 섹션
2. "빌드를 원격으로 유발" 체크
3. "Authentication Token" 설정 (예: `build-trigger-token-xxx`)

### 2. API 토큰 생성

1. Jenkins → 사용자 설정 → API Token
2. "Add new Token" 클릭
3. 토큰 이름 입력 후 "Generate"
4. 생성된 토큰 저장 (GitLab CI Variables에 사용)

### 3. Job 명명 규칙

GitLab CI 템플릿과 호환되도록 job 이름을 설정합니다:

| 프로젝트 | Jenkins Job 이름 |
|----------|------------------|
| hybris | `hybris-build` |
| kop-cms | `kop-cms-build` |
| kop-web | `kop-web-build` |
| kop-api | `kop-api-build` |

## GitLab CI 설정

### CI/CD Variables

프로젝트 → Settings → CI/CD → Variables에 추가:

```
JENKINS_URL = https://jenkins.example.com
JENKINS_USER = your-jenkins-username
JENKINS_API_TOKEN = 11xxxxxxxxxxxxxx
BUILD_TOKEN = build-trigger-token-xxx
```

### .gitlab-ci.yml

`deploy-automation/gitlab-ci-template.yml` 내용을 프로젝트의 `.gitlab-ci.yml`에 추가합니다.

## 빌드 트리거 확인

### cURL로 직접 테스트

```bash
curl -X POST \
  "https://jenkins.example.com/job/hybris-build/build?token=build-trigger-token-xxx" \
  --user "username:api-token"
```

### GitLab Pipeline에서 확인

1. GitLab → CI/CD → Pipelines
2. `trigger_jenkins_*` job 로그 확인

## 트러블슈팅

### 401 Unauthorized

- `JENKINS_USER`와 `JENKINS_API_TOKEN` 확인
- API 토큰이 만료되지 않았는지 확인

### 403 Forbidden

- 사용자에게 job 빌드 권한이 있는지 확인
- "빌드를 원격으로 유발" 옵션이 활성화되어 있는지 확인

### 404 Not Found

- Job 이름이 올바른지 확인
- Jenkins URL이 올바른지 확인

### Connection Refused

- Jenkins 서버가 실행 중인지 확인
- 방화벽 설정 확인
- GitLab Runner에서 Jenkins 서버에 접근 가능한지 확인

## 보안 권장사항

1. **토큰 관리**: API 토큰과 빌드 토큰을 정기적으로 갱신
2. **접근 제한**: Jenkins job에 특정 IP만 접근 허용
3. **HTTPS**: Jenkins와 GitLab 간 통신에 HTTPS 사용
4. **최소 권한**: Jenkins 사용자에게 필요한 최소 권한만 부여
