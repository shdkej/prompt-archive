# marketing-01 · 로컬 실행 리포트

- 실행 시각: 2026-05-21T08:07Z (execute_local)
- 대상 레포: /home/ubuntu/dev/virtue-rebirth-app
- 시작 HEAD: `99bf53b` (master, origin/master와 동일)
- 변경 위치: 브랜치 `marketing-01-add-flow-telemetry` (`b28d01f`) — **푸시 안 함**
- 라이브: https://virtue.oracle.shdkej.com

## 상태 요약

**부분 완료 (로컬 코드 작업 + 검증 완료, 배포/푸시는 승인 대기).**
준비된 감사(2026-05-15)의 지적 사항 대부분은 이미 코드에 반영되어 있었고,
남아있던 유일한 텔레메트리 공백(퍼널 진입/이탈 이벤트)만 최소 범위로 추가했다.

## 0. Workflow-master 게이트

대상 레포에 `.agent/workflows/workflow-master.md` / `WORKFLOW-MASTER.md`가 **없음**(prompt-archive에는 존재).
의도 지시대로 약식 게이트만 수행:

- **복잡도**: 간단~중간 (가드 검증 + 단일 파일 소규모 편집 + 표준 검사)
- **계획**: ①가드 현황 확인 ②라이브 HTML 데모상태 검증 ③남은 최소 텔레메트리만 추가 ④typecheck/lint/build ⑤리포트
- **검증**: 아래 §4 게이트
- 4-에이전트 병렬 오케스트레이션은 생략. 근거: 단일 파일 소규모 변경이라 병렬 분담 시 동일 파일 충돌·무관 파일 수정 위험이 이득보다 큼. 의도가 "약식 게이트"를 명시 허용함.

## 1. Demo-state 가드 — 검증 결과: **정상 (수정 불필요)**

가드는 `dfaaf4e`에서 추가되어 현재 HEAD에도 유지됨:

```
src/lib/store.ts:30  const SHOW_DEMO = process.env.NEXT_PUBLIC_SHOW_DEMO === "1";
src/lib/store.ts:31  const SEED_DEEDS: IDeed[] = SHOW_DEMO ? MOCK_DEEDS : [];
```

모든 스냅샷 읽기/SSR 폴백이 `MOCK_DEEDS`가 아닌 `SEED_DEEDS`를 사용 → 프로덕션(`NEXT_PUBLIC_SHOW_DEMO` 미설정)에서는 빈 스토어로 시작.

라이브 HTML 검증 (`curl https://virtue.oracle.shdkej.com`, 17,086 bytes, `x-nextjs-cache: HIT`, ETag `"10thb068fctcvu"`):

| 시그널 | 결과 | 판정 |
|---|---|---|
| `641` (= INITIAL_VIRTUE 612 + MOCK 29) 노출 | **0건** | 시드 총합 미노출 ✓ |
| `MOCK` 노출 | **0건** | ✓ |
| 빈 상태 카피 렌더 | "아직 비어있어요. 오늘 1덕만 시작해볼까요?" / "아직 기록이 없어요." | `stats.count === 0` ✓ |
| `덕` 등장 15건 | 전부 UI 카피(타이틀·메타·버튼) | 데이터 아님 ✓ |

**주의(설계 뉘앙스)**: 신규 방문자 총합은 `0덕`이 아니라 **`612덕`** (`INITIAL_VIRTUE`, mock-data.ts:132)으로 표시됨.
이는 시드된 가짜 *기록(MOCK_DEEDS)*이 아니라 환생 컨셉의 의도된 시작 베이스라인이며 가드 대상이 아님.
준비 프롬프트의 "0덕" 기대치와는 다르지만, 데모 기록 노출 버그는 해소됨. 612 베이스라인의 활성화 영향 여부는 별도 마케팅/제품 판단 사항으로 남김.

## 2. 텔레메트리 현황 — 준비안 대비 대부분 이미 반영됨

| 준비안(telemetry-fix.md) 항목 | HEAD 현황 |
|---|---|
| §3-1 error.tsx captureException | **이미 적용** — `src/app/error.tsx:15` |
| §3-4 capture_exceptions: true | **이미 적용** — `src/instrumentation-client.ts:7` |
| §3-2 deed_judged 프로퍼티 확장 | **이미 적용** — score/source/fallback_reason/model/has_photo/tone/memo_length/retry_count/duration_ms (초안보다 풍부) |
| §3-2 deed_saved 프로퍼티 확장 | **이미 적용** — +tags/tag_count/level_up/new_species/total_after |
| deed-judge 예외 캡처 | **이미 적용** — `add/page.tsx:90` |
| §3-3 add_flow_started / add_flow_abandoned | **누락** → 이번에 추가 |

→ 준비 감사는 사실상 stale. "still needed"에 해당하는 최소 개선은 §3-3 퍼널 진입/이탈 이벤트뿐이며, 이는 의도(landing→add→judge→save 드롭오프 특정)에 직접 부합.

## 3. 적용한 변경

**파일**: `src/app/add/page.tsx` (1 file, +33 lines)

- `add_flow_started`: /add 마운트 시 capture (`scoring_mode`)
- `add_flow_abandoned`: 저장 없이 언마운트 시 capture (`had_photo`/`had_memo`/`had_judgment`)
- `savedRef`로 저장 성공 시 이탈 이벤트 억제, `engagementRef`로 언마운트 시점 최신 참여 상태 전달
- 기존 `deed_judge_attempted → deed_judged → deed_saved`와 짝을 이뤄 퍼널 완성

선택 근거: $pageview(autocapture)는 진입을 대략 잡지만 "진입 후 저장 없이 이탈"하는 누수 신호는 현재 전무했음. abandon 이벤트가 활성화 갭의 핵심 누락 신호.
구현은 `beforeunload`(플래키) 대신 언마운트 cleanup 사용. (dev StrictMode에서는 effect 이중 호출로 중복 발생 가능 — 프로덕션 빌드는 영향 없음.)

## 4. 검증 게이트

| 항목 | 명령 | 결과 |
|---|---|---|
| 타입 | `pnpm typecheck` | **PASS** (exit 0, 0 errors) |
| 린트 | `pnpm lint` | **PASS** (0 errors, 4 warnings — toast/greeting의 기존 set-state-in-effect, 본 변경과 무관) |
| 빌드 | `pnpm build` | **PASS** (Next 16.2.6, 11.7s 컴파일, 7/7 static, exit 0) |
| 라이브 데모상태 | `curl` | **PASS** (641·MOCK 0건, 빈 상태 렌더) |

내 추가 effect는 setState를 호출하지 않으므로 lint warning을 늘리지 않음.

## 5. 배포 / 푸시 / 승인 상태

- **푸시: 하지 않음.** `master`·`origin/master` 모두 `99bf53b` 그대로. 변경은 로컬 브랜치 `marketing-01-add-flow-telemetry`(`b28d01f`)에만 존재.
- **이유**: 푸시는 L2이며 의도상 "푸시가 배포/프로덕션에 영향 없음을 먼저 입증"해야 함. CI/Dockerfile은 `643b39d`에서 제거되어 GitHub Actions 자동배포는 없으나, Oracle 서버측 webhook 부재를 로컬에서 단정할 수 없어 "애매하면 푸시 금지" 원칙에 따라 보류.
- **배포(L2/L3) 차단 유지**: `git pull + pnpm build + pm2 restart`(작업1의 §3), `ecosystem.config.js`에 `NEXT_PUBLIC_SHOW_DEMO=0` 추가는 프로덕션 변경이므로 **명시적 사용자 승인 필요**. 본 실행에서 미수행.
- 가드는 이미 라이브에서 동작 중이므로(641·MOCK 미노출) 데모상태 관련 긴급 배포 필요성은 없음. 텔레메트리 변경 배포는 다음 사용자 승인 배포 사이클에 포함하면 됨.

## 6. 다음 액션

1. (사용자) 브랜치 리뷰 후 머지 결정: `git diff master..marketing-01-add-flow-telemetry` → 문제 없으면 master 머지 + 푸시 승인.
2. (사용자 승인 시, L2) Oracle 서버 배포 — git pull + build + pm2 restart. 데모상태는 이미 정상이므로 텔레메트리만을 위한 배포.
3. (7일 후) PostHog 424014에서 `add_flow_started` 대비 `add_flow_abandoned`/`deed_saved` 비율로 드롭오프 지점 확인 (improvement-expectation.md 기준 `deed_saved/deed_judged ≥ 30%`).
4. (선택) 신규 방문자 `612덕` 베이스라인이 활성화에 주는 인상 — 마케터 검토 항목으로 분리.
