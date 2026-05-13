# Infinity Artifact / Path Rules

> 의도(Intent), 산출물(Artifact), 실행 로그(Report)의 위치와 책임을 명확히 분리한다.
> 모든 Heartbeat 및 Local 실행은 이 규칙을 따르며, 완료 시 archive intent를 canonical index로 만든다.

## 디렉터리 책임

| 경로 | 역할 | 수명 |
|------|------|------|
| `infinity/intents/active/{id}.md` | 활성 Intent의 **현재 상태와 다음 액션만** | 진행 중 |
| `infinity/intents/archive/{id}.md` | 완료된 Intent의 **canonical final index** (결과 요약 + 산출물·리포트·커밋·URL 링크) | 영구 |
| `infinity/artifacts/{id}/...` | **결과로서 가치 있는 산출물** (research 결과, 설계 초안, 구현 산출물, 데이터) | 영구 |
| `infinity/reports/{id}/{timestamp}.md` | 단일 실행 로그 (heartbeat run 결과, 진행 보고) | 누적 |
| `infinity/reports/heartbeat/` | **전역** heartbeat 요약만 (intent 결과 보고서가 아님) | 누적 |

## 핵심 원칙

1. **Reports는 실행 로그이고 결과물이 아니다.** 동일한 결론을 두 번 찾기 위해 사람이 reports 디렉터리를 뒤져야 하면 운영 실패다. 결과는 archive intent에 요약하고, 산출물은 `artifacts/{id}/`로 옮긴다.
2. **Active intent는 짧게 유지한다.** 분석/결과를 본문에 누적하지 말고, 산출물은 `artifacts/{id}/`에 만들고 active intent에서는 참조만 한다.
3. **완료 시 archive intent가 canonical index가 된다.** 사용자가 "그래서 뭐 했더라"를 찾을 때 한 파일만 봐도 산출물 / 리포트 / 커밋 / URL 까지 한 번에 도달해야 한다.
4. **`drafts/`는 폐기.** 과거 drafts 산출물은 모두 `artifacts/{id}/`로 이동했다. 모든 신규 detail 링크는 `artifacts/{id}/` 또는 `intents/archive/{id}.md`만 가리킨다.

## Archive Intent 표준 포맷

완료된 Intent를 archive로 옮길 때 최소 아래 필드를 포함한다.

```md
# [intent-id] 제목

- id: {intent-id}
- status: archived
- completed_at: YYYY-MM-DDTHH:MM
- result_summary: 한 줄 결과
- artifacts:
  - path: infinity/artifacts/{id}/foo.md
    role: design | research | implementation | data
    note: 짧은 설명
- reports:
  - path: infinity/reports/{id}/{timestamp}.md
    role: final | run | heartbeat
- commits:
  - repo: prompt-archive | space | ...
    sha: 894c3f8
    note: 짧은 설명
- urls:
  - url: https://...
    note: 라이브/배포 위치
- next_actions:
  - 후속 작업 / 권장 다음 Intent
```

기존 archive 문서(`build-01.md`, `research-06.md` 등)는 형식이 일관되지 않지만 이 패스에서는 마이그레이션하지 않는다. **신규 archive부터** 이 포맷을 따른다.

## Heartbeat가 지켜야 할 흐름

1. 실행 결과를 `infinity/reports/{id}/{timestamp}.md`로 남긴다 — 이것은 **로그**다.
2. 의미 있는 산출물이 생기면 `infinity/artifacts/{id}/...`로 만든다. active intent 본문에 두지 않는다.
3. Intent가 완료되면:
   - `infinity/intents/active/{id}.md` → `infinity/intents/archive/{id}.md`로 이동
   - 위 표준 포맷으로 재작성하면서 artifacts / reports / commits / urls 링크
   - `INTENTS.md`의 Active 블록 제거, 완료 코멘트 추가 (`<!-- {id} completed YYYY-MM-DDTHH:MM → infinity/intents/archive/{id}.md -->`)
4. 대시보드 등 외부 도구가 detail 링크를 기대하면 archive 경로가 유효한지 확인한다.

## Migration Note (현 상태)

- `infinity/drafts/` → `infinity/artifacts/{id}/`로 전부 이관 완료. archive intent 참조 경로도 함께 갱신했다.
- `infinity/reports/` 하위 디렉터리는 그대로 둔다. 신규 final 결과는 reports가 아니라 archive intent + artifacts 조합으로 표현한다.
- 대시보드는 archive intent 본문과 `artifacts/{id}/` 디렉토리를 우선 로드하고, 마지막 fallback으로 reports 최신 1건을 표시한다.
