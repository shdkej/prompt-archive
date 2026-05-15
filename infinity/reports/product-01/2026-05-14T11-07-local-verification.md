# product-01 Heartbeat Report
- timestamp: 2026-05-14T11:07Z
- status_before: in_progress
- status_after: in_progress
- mode: verify_local (L0/L1 only · no secrets · no paid API calls)

## actions_taken
- **workflow-master 분류**: 검증 게이트 (typecheck/lint/build + 키 없는 상태의 폴백 계약 확인). 새 코드/설계 없음 · 결정적 단계 4개 · 사용자가 L0/L1 + 시크릿 금지로 범위 명확화 → **trivial**로 기록하고 단일 실행자로 진행. 4-role 관점은 본 보고서에 통합 반영 (planner = 게이트 단계 정합, developer = 코드 경로 정합, marketer = 폴백 카피 노출 확인, operator = 키 누락 시 CS 노이즈 통제).
- App repo (`/home/ubuntu/dev/virtue-rebirth-app`) 상태 기록:
  - working tree clean (수정/언트래킹 0건).
  - HEAD `70268fde10d65eea13f10b33a8ffdbd108dd2c1c` (`pin pnpm for deployment install`).
  - origin `https://github.com/shdkej/virtue-rebirth-app.git`, `master` ↔ `origin/master` 동기 (커밋 동일).
- Build/lint/typecheck (앱 레포 루트, 모두 비밀값 없이 실행):
  - `pnpm typecheck` ✅ PASS (출력 0줄).
  - `pnpm lint` ✅ PASS (`No ESLint warnings or errors`).
  - `pnpm build` ✅ PASS — 8 routes 정적 prerender, `/api/score`만 `ƒ Dynamic`. First Load JS 105–139 kB. `/add` 25.2 kB → 139 kB (이전 wave와 동일).
- 로컬 `pnpm start` 후 비밀값 없이 HTTP probe (port 8030):
  - `GET /` → 200
  - `GET /add` → 200 (HTML에 ToastViewport 마운트 청크 `5:I[3304,...,"ToastViewport"]` 포함 · 안내 카피 `사진은 이 기기에만 잠시 머물러요. 키가 설정돼 있으면 AI가, 없으면 mock이 채점해요.` 렌더 확인)
  - `GET /deeds` → 200
  - `GET /dex` → 200
  - `GET /me` → 200
- `/api/score` 폴백 계약 (키 미설정) 검증:
  - `POST /api/score` (빈 바디) → **503** `{"error":"scoring_disabled","message":"ANTHROPIC_API_KEY 미설정. 클라이언트는 mock으로 폴백."}`
  - `POST /api/score` (`imageBase64`/`mimeType`/`toneMode` 포함된 valid-shape 바디) → **동일 503** — 키 가드(`route.ts:12-18`)가 스키마 파싱(`ScoreRequestSchema.safeParse`)보다 앞서서 호출 비용 0으로 단락. `Anthropic` 클라이언트 인스턴스화·호출 분기는 진입조차 안 됨.
- 토스트 발화 경로 정적 정합 확인:
  - 서버 503 → 클라이언트 `fetch.res.ok === false` → `score-client.ts:53-55` `mock + fallbackReason: "api_error"` 반환.
  - `add/page.tsx:63-67` `runJudge` 결과의 `outcome.fallbackReason` 분기에서 `showToast("AI가 잠깐 졸고 있어요. 임시 판정으로 보여드릴게요.")` 1회 호출. 결과 카드 배지는 `source === "mock"` 경로로 muted 표기.
- 서버 종료(`pkill -f 'next start -p 8030'`) 후 포트 8030 해제 확인.

## verification

| 항목 | 결과 |
|------|------|
| `pnpm typecheck` | ✅ PASS |
| `pnpm lint` | ✅ PASS (warning 0) |
| `pnpm build` | ✅ PASS (8 routes) |
| `pnpm start` × 5 페이지 HTTP probe | ✅ 200 × 5 |
| `POST /api/score` (키 없음, 빈 바디) | ✅ 503 `scoring_disabled` |
| `POST /api/score` (키 없음, valid-shape) | ✅ 503 `scoring_disabled` (가드 우선) |
| 폴백 토스트 코드 경로 정합 | ✅ `score-client.ts:53` → `add/page.tsx:65-67` 직결 |
| working tree clean / origin 동기 | ✅ HEAD = origin/master = `70268fd` |

## deployment defaults — 검증되지 않은 분기(설명)
- 운영 빌드 기본값은 `.env.example`의 `NEXT_PUBLIC_SCORING_MODE=mock`. 이 값은 **빌드 타임에 인라인**되므로 배포된 번들에서는 클라이언트가 `/api/score`를 **호출하지 않고 항상 `mockJudge` 직접 경로**를 탑니다 → 결과 카드 배지 `mock`, 폴백 토스트 미발화 (의도된 동작).
- 폴백 토스트는 **`NEXT_PUBLIC_SCORING_MODE=ai`로 빌드한 환경**에서 키 누락/네트워크 실패 시에만 발화. 본 검증은 운영 빌드(503 → 클라이언트 폴백)와 정확히 같은 서버 응답을 직접 POST로 재현해 계약을 확인한 형태 — 토스트 발화는 클라이언트 측 1행 분기(`fallbackReason` truthy → `showToast`)라 회귀 위험 매우 낮음.

## 미수행 — 의도된 한계
- 헤드리스 브라우저로 `/add`에서 실제 파일 업로드 → 채점 → 토스트 캡처는 미수행. 본 빌드는 `NEXT_PUBLIC_SCORING_MODE=mock` 기본이라 클라이언트 폴백 분기에 진입하지 않고, 그 분기를 자극하려면 `NEXT_PUBLIC_SCORING_MODE=ai`로 **재빌드**가 필요. 본 verify_local 범위에서는 (a) 빌드 산출물 변경 회피, (b) 운영 기본값 검증 가치 보존을 우선해, API 계약 + 정적 코드 경로 검증으로 갈음. `chromium` 바이너리는 환경에 존재(`/snap/bin/chromium`)하지만 playwright/puppeteer 설치 없이 파일 업로드 자동화는 비용 대비 가치가 낮다고 판단.
- 실제 `ANTHROPIC_API_KEY` end-to-end 호출은 forbidden(외부 유료 API 금지) — 미수행. `implementation.md` Next Actions #2가 그대로 다음 단계.

## stale intent — 보고만 (수정 안 함)
- `infinity/intents/active/product-01-virtue-rebirth-app.md` 라인 20: `로컬 git 6ba58a8까지, push 없음.` → 현재 `70268fd` · origin 설정 · 4 커밋 추가 push 완료 (`70268fd`/`2217c27`/`ee7f8d0`/`b015ec8`).
- 같은 파일 Next Actions:
  - #1 `mock 채점을 진짜 Claude Sonnet 4.6 vision API로 교체` → 완료 (커밋 `b015ec8`).
  - #6 `사용자 컨펌 시 app 레포 origin 설정 + 첫 push` → 완료.
- Artifacts 섹션이 신규 리포트 두 건(`2026-05-13T22-07-vision-api.md`, `2026-05-13T23-07-fallback-ux.md`)을 누락.
- 본 verify_local 작업 범위 외라 **수정하지 않음**. prompt-archive에 사전 변경 파일들(INFINITY.md / THREADS_STYLE_HISTORY.md / EVALUATION_NOTES.md / PERMISSIONS.md / artifacts/implementation.md / workflows/heartbeat.md)이 다수 staged-modified 상태라 동일 PR/브랜치에 무관 변경을 묶지 않음.

## changed_files
- `infinity/reports/product-01/2026-05-14T11-07-local-verification.md` (prompt-archive, 본 보고서 · 신규)
- 앱 레포 변경 없음 · prompt-archive 사전 변경 파일들 그대로 보존.

## local_commit
- 없음 (앱 코드 무변경 · 보고서는 prompt-archive에만 작성, 별도 commit/push 미수행).

## blockers
- 운영 기본값(`NEXT_PUBLIC_SCORING_MODE=mock`) 하에서는 클라이언트가 `/api/score`를 호출하지 않으므로, 사용자가 직접 키 미설정 + AI 모드 빌드를 한 번 만들어 토스트 노출까지 확인해야 폴백 UX 회귀 보호가 끝까지 닫힘. 본 검증은 그 분기를 자극하는 서버 측 503 응답을 확정했고 클라이언트 분기는 1행이라 위험은 낮음.
- 헤드리스 자동화 도구(playwright/puppeteer)가 앱 레포에 설치되어 있지 않음 — 향후 회귀 가드(특히 토스트 1회 발화)는 단위 테스트 또는 e2e 도구 도입을 별도 결정 필요.

## next_actions
1. (사용자 손이 필요한 1회 확인) 로컬에서 `NEXT_PUBLIC_SCORING_MODE=ai`만 켜고 `ANTHROPIC_API_KEY`는 비운 채 `pnpm build && pnpm start` → `/add`에서 사진 1장 채점 → 결과 카드 배지 `mock` + 토스트 `AI가 잠깐 졸고 있어요. 임시 판정으로 보여드릴게요.` 1회 노출 확인. (실패 시: 토스트가 안 뜨는지/두 번 뜨는지 보고)
2. 이후 실키로 한 번만 end-to-end 채점 — `source: "ai"` + `model: claude-sonnet-4-6` 응답·결과 카드 배지 `AI` 전환·코멘트 한국어 톤(soft/casual) 준수 + 일일 30덕 클라 가드 동작 확인. `implementation.md` Next Actions #2의 잔여 점.
3. `infinity/intents/active/product-01-virtue-rebirth-app.md` 리프레시 (git 상태/Next Actions/Artifacts 라인) — 다른 prompt-archive 변경과 분리해서 별도 커밋으로.
4. 회귀 가드: 키 미설정 빌드에서도 `/api/score` 503 응답이 변하지 않도록 단위/integration 테스트 1개라도 추가 검토 (현재 무테스트). 도입 비용/가치 판단 필요.
5. (운영) 배포 환경에서 `NEXT_PUBLIC_SCORING_MODE`와 `ANTHROPIC_API_KEY` 페어링 매트릭스 명시 — `README.md`에 표 한 줄로 정리하면 운영 실수 (키 없이 AI 모드 켜기, 키 있는데 mock 모드 유지) 가시화에 도움.
