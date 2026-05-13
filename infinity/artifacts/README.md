# Infinity Artifacts

> Intent별 **결과 산출물**의 영구 보관 위치. 실행 로그가 아니라 결과로서 가치 있는 산출물만 둔다.

규칙 상세: `infinity/ARTIFACT_RULES.md`

## 경로 규칙

```
infinity/artifacts/{intent-id}/{filename}
```

- `intent-id`: archive intent와 동일 ID (예: `build-02`, `research-07`)
- 한 Intent에서 여러 파일이 나올 수 있다 (예: `design.md`, `implementation.md`, `data.csv`)

## artifact role 분류

| role | 예 |
|------|---|
| `research` | 비교·조사 문서, 시장 리서치 |
| `design` | 설계안, 아키텍처 다이어그램, SKILL.md 초안 |
| `implementation` | 코드 패치/스크립트 초안, 매니페스트 사본 |
| `data` | 분석 데이터, 실험 결과 |

## 등록 방법

1. 산출물 파일을 `infinity/artifacts/{id}/` 아래에 둔다.
2. 해당 Intent의 archive 문서(`infinity/intents/archive/{id}.md`)의 `artifacts:` 섹션에 path/role/note를 기재한다.
3. Reports에는 실행 로그만 남기고 산출물을 reports에 두지 않는다.

## Legacy 안내

`infinity/drafts/`는 폐기되었다. 과거 drafts 산출물은 모두 본 `infinity/artifacts/{id}/`로 이관 완료. 모든 archive intent도 새 경로를 참조한다.
