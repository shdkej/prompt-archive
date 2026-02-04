---
description: 오늘 전체 세션의 작업 내용을 요약하여 Confluence에 업로드
argument-hint: (선택) 추가 메모
allowed-tools: ["Read", "Grep", "Glob", "Bash", "mcp__plugin_atlassian_atlassian__*"]
---

# 퇴근 - 작업 요약 Confluence 업로드

> 상세 워크플로우: `daily_work_feedback_system_prompt/daily_workflow.md` 참조
> 설정: `daily_work_feedback_system_prompt/_config.md` 참조

## 실행 순서

1. 설정 확인 (`_config.md`의 `mode` 값)
2. 모드에 따라 처리:
   - `session`: 세션 파일 자동 추출
   - `conversation`: 대화 기반 회고
3. Confluence 업로드 (업무용만)
4. 전체 요약 출력

## 빠른 참조

### Confluence 설정
- Space Key: `~63561b381cc605b1fd15aca2`
- Parent Page ID: `182943745`

### 프로젝트 분류
- **업무** (`~/dev/`): Confluence 업로드
- **개인** (`~/workspace/`): 로컬 요약만

### 세션 파일 위치
`~/.claude/projects/*/`

## 사용 예시
```
사용자: 퇴근할게
또는: /finish-work
또는: /finish-work 오늘 PR 리뷰도 했음
```

## 에러 처리
- 세션 파일 없음: "오늘 작업한 세션이 없습니다"
- Confluence 연결 실패: 로컬에 요약 출력
- 설정 파일 없음: 기본값 사용
