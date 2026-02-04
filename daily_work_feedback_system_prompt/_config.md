# 공통 설정

## 퇴근 처리 모드

```yaml
mode: session  # session | conversation

# session: 세션 파일(JSONL)에서 자동 추출 (기본값)
#   - ~/.claude/projects/*/ 세션 파일 분석
#   - 업무/개인 프로젝트 자동 분류
#   - 회고 질문 없음, 빠른 처리
#
# conversation: 대화 기반 처리
#   - 당일 대화 내용에서 추출
#   - 3가지 회고 질문 (선택)
#   - 사용자 상호작용 중심
```

## 사용자 정보
- **사용자명**: seonghonoh
- **스페이스 ID**: ~63561b381cc605b1fd15aca2
- **폴더**: 업무일지
- **플랫폼**: purpleio.atlassian.net
- **Parent Page ID**: 182943745

## 프로젝트 분류
```json
{
  "categories": {
    "work": {
      "patterns": ["/Users/seongho-noh/dev/"],
      "confluence": true
    },
    "personal": {
      "patterns": ["/Users/seongho-noh/workspace/"],
      "confluence": false
    }
  }
}
```
> 설정 파일: `~/.claude/project-categories.json`

## 문서 형식
- **제목 형식**: `[MM/DD] 제목` 또는 `작업일지 - YYYY-MM-DD`
- **지연 정리 시**: `[MM/DD] 제목 (늦은 정리)`

## Confluence 검색 쿼리
```
기본: space = "~63561b381cc605b1fd15aca2" AND title ~ "MM/DD"
확장: space = "~63561b381cc605b1fd15aca2" AND title ~ "[MM/DD]"
날짜: modifiedTime >= "YYYY-MM-DD" AND modifiedTime < "YYYY-MM-DD+1"
```

## 날짜 계산 로직
```javascript
// 한국 시간대
const koreaTime = new Date().toLocaleString("en-US", {timeZone: "Asia/Seoul"});

// 주말/휴일 처리: 전날 계산 시
// 일요일(0) → 금요일로 (-2일 추가)
// 토요일(6) → 금요일로 (-1일 추가)
```

## 사용 환경
- **OS**: macOS M4
- **개발 도구**: asdf, terraform, AWS
- **협업 도구**: Asana, GitLab, Confluence
