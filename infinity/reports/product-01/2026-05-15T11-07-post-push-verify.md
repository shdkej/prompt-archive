---
intent: product-01
title: 푸시 후 배포 반영 검증 (UX 배치 dfaaf4e)
mode: verify_local
timestamp_utc: 2026-05-15T11-07
operator: claude-opus-4-7
---

## 요약 (Verdict)

- **dfaaf4e는 origin/master까지 푸시 완료, 하지만 배포된 앱에는 아직 반영되지 않음.**
- 배포 URL의 모든 페이지가 푸시 전 베이스라인과 **바이트·응답 헤더 모두 동일**.
- 위반/리스크: 없음. 소스 변경·배포·강제 조작 모두 수행하지 않음 (read-only/probe만 사용).
- 분류: verify-only 하트비트 (workflow-master 게이트 통과).

## 워크플로우 분류 (Workflow-master gate)

App repo `/home/ubuntu/dev/virtue-rebirth-app/`에는 WORKFLOW.md / AGENTS.md / CLAUDE.md 어느 것도 존재하지 않음.
→ 지침에 따라 **verify-only 하트비트**로 분류, 단일 직접 실행자(executor) 아닌 read-only 검증 경로로만 진행.

## 1. 레포 상태

| 항목 | 값 |
|------|----|
| 로컬 HEAD | `dfaaf4ea9d8f381956cf60122604ee5cb9da2c86` |
| origin/master | `dfaaf4ea9d8f381956cf60122604ee5cb9da2c86` |
| upstream track | `(none)` — sync 상태 |
| working tree | clean (변경 없음) |
| 최신 커밋 메시지 | "UX 개선 배치 정리 및 목업 제외" |
| Author date | 2026-05-15 09:14:03 +0000 (~2시간 전) |

**최근 5개 커밋:**
```
dfaaf4e UX 개선 배치 정리 및 목업 제외
a12aeab Next 16 업그레이드 및 PostHog 분석 통합
4cce250 하단 네비를 환생 오브 HUD로 개편
70268fd pin pnpm for deployment install
2217c27 배포 기본값을 mock 채점으로 고정
```

## 2. 배포 페이지 HTTP 프로브 결과 (https://virtue.oracle.shdkej.com)

측정 시각: 2026-05-15 11:08 UTC

| 경로 | HTTP | bytes (now) | bytes (pre-push baseline) | Δ | ETag | x-nextjs-cache |
|------|------|-------------|---------------------------|---|------|----------------|
| `/` | 200 | 17289 | 17289 | 0 | `"i2iryr9siud0r"` | HIT |
| `/add` | 200 | 15859 | 15859 | 0 | `"17wuacz0u76bz5"` | HIT |
| `/deeds` | 200 | 31251 | 31251 | 0 | `"1506zyo9js8n5s"` | HIT |
| `/dex` | 200 | 20643 | 20643 | 0 | `"uhoxye6jgcfir"` | HIT |
| `/me` | 200 | 17162 | 17162 | 0 | `"17echqvrgmdcws"` | HIT |
| `POST /api/score` | 503 | 107 | (503) | 0 | — | — |

**`/api/score` 본문:**
```json
{"error":"scoring_disabled","message":"ANTHROPIC_API_KEY 미설정. 클라이언트는 mock으로 폴백."}
```
→ mock 채점 모드 유지 정책과 일치 (정상).

응답 헤더 특성: `cache-control: s-maxage=31536000`, `x-nextjs-cache: HIT`.
ETag 5개 모두 안정값. 즉, 엣지/Next 캐시가 동일 빌드를 서빙 중.

## 3. UX 배치 마커 확인

dfaaf4e 변경 파일 (12개): `src/app/{add,deeds,dex,me,page,layout}.tsx`, `src/components/bottom-nav.tsx`, `src/lib/{format,store}.ts`, `eslint.config.mjs`, `package.json`, `.gitignore`.

배포 HTML 검사:
- 새로운 UX-batch 특유 문자열("환생 오브" 등) 탐색 → 일부는 HUD 개편(4cce250, 이전 배포본에 이미 포함)과 구분이 어려워 결정적 마커로 부적합.
- `<title>덕 쌓기 · 환생</title>`은 모든 페이지에서 정상.
- buildId는 HTML에 직접 노출되지 않음 (Next 16 SSG 출력 특성). `/_next/static/chunks/` 경로 해시는 marshalling되어 단일 비교 불가.

→ 결정적 시그널은 **바이트 일치 + ETag 안정 + cache HIT**. HTML 내 텍스트 마커는 부차적.

## 4. 판정 근거

- 5개 페이지 응답 바이트가 푸시 전 베이스라인과 **0바이트 차이**.
- ETag 5개 모두 안정값(이전 측정과 동일 빌드의 캐시 객체로 보임).
- `x-nextjs-cache: HIT` + `s-maxage=31536000` → 새 빌드를 트리거할 신호 없음.
- 푸시 후 2시간 경과했으나 수동 배포 미실행 + 자동 CI/CD 트리거 흔적도 응답에 없음.

→ **결론: dfaaf4e가 prod에 반영되지 않음.** 이는 의도된 상태(수동 배포 미실행)이며 정책 위반이 아님.

## 5. 한계 (Limits)

- buildId 또는 빌드 해시가 HTML에 직접 노출되지 않아, 바이트·ETag 비교에 의존했음.
- 무거운 헤드리스 브라우저 검사(JS 실행 후 DOM 비교)는 verify-only 범위를 벗어나므로 미수행.
- CI/CD 파이프라인 로그/배포 시스템 직접 조회는 수행하지 않음 (정책상 forbidden 항목은 아니나, 이 검증 게이트의 범위 밖).
- 운영자가 의도적으로 배포를 미루는 중인지, 자동 배포가 막혀 있는지 여부는 본 리포트로 단정할 수 없음.

## 6. 다음 액션 제안 (정보 제공, 강제 아님)

1. **배포 의사결정**: dfaaf4e를 prod로 올릴지 결정 필요. 올린다면 외부 명령(수동 배포 또는 CI 트리거)을 운영자가 수행.
2. **배포 후 재검증**: 이 리포트와 동일한 5개 페이지 + `/api/score` 프로브로 ETag·바이트 변동 확인.
3. **배포 트리거 흔적 부재**: 향후 dfaaf4e처럼 푸시-only 커밋이 prod에 자동 반영되지 않는 것을 명시적으로 문서화하면 다음 하트비트가 혼동 없이 통과 가능.

## 7. 수행 명령 로그 (read-only)

- `git rev-parse HEAD`, `git rev-parse origin/master`, `git log --oneline -5`, `git status --short`, `git for-each-ref ... refs/heads/master`, `git show --stat dfaaf4e`
- `ls` (workflow files presence check, .next/BUILD_ID 확인)
- `curl -sS -o <tmp> -w "..." --max-time 20 <url>` (5 GET + 1 POST)
- `curl -sSI --max-time 10/15 <url>` (5 HEAD)
- 로컬 `/home/ubuntu/dev/virtue-rebirth-app/.next/BUILD_ID` 읽기 (참고용; 배포 빌드와 비교 불가)

위반: 없음. 모든 동작은 L0/L1 read-only 범위.
