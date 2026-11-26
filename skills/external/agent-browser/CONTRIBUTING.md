# Agent Browser 스킬 기여 가이드

이 스킬은 agent-browser CLI를 감쌉니다. 이슈를 보고하기 전에 문제가 어디에 있는지 파악하세요.

## 이슈 보고 가이드

### 이 저장소에 이슈를 등록해야 하는 경우

- 스킬 문서가 불명확하거나 누락된 경우
- SKILL.md의 예시가 동작하지 않는 경우
- 이 스킬 래퍼로 CLI를 사용하는 데 도움이 필요한 경우
- 스킬에 명령이나 기능이 빠진 경우

### agent-browser 저장소에 이슈를 등록해야 하는 경우

- CLI가 크래시하거나 오류를 발생시키는 경우
- 명령이 문서대로 동작하지 않는 경우
- 브라우저 자동화에서 버그를 발견한 경우
- CLI에 새 기능이 필요한 경우

## 이슈를 열기 전에

1. 최신 버전 설치
   ```bash
   npm install -g agent-browser@latest
   ```

2. 문제를 분리하기 위해 터미널에서 명령을 테스트

## 이슈 보고 템플릿

필요한 정보를 제공하려면 이 템플릿을 사용하세요.

```markdown
### Description
[Provide a clear and concise description of the bug]

### Reproduction Steps
1. [First Step]
2. [Second Step]
3. [Observe error]

### Expected Behavior
[Describe what you expected to happen]

### Environment Details
- **Skill Version:** [e.g. 1.0.2]
- **agent-browser Version:** [output of agent-browser --version]
- **Node.js Version:** [output of node -v]
- **Operating System:** [e.g. macOS Sonoma, Windows 11, Ubuntu 22.04]

### Additional Context
- [Full error output or stack trace]
- [Screenshots]
- [Website URLs where the failure occurred]
```

## 스킬에 새 명령 추가하기

상위 CLI에 새 명령이 추가되면 SKILL.md를 업데이트하세요.
- Installation 섹션은 유지합니다
- 새 명령을 올바른 카테고리에 추가합니다
- 사용 예시를 포함합니다
