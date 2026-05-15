# marketing-01 · Demo-State 루트 콜즈 분석 및 수정 계획

> created: 2026-05-15 (heartbeat L0 prepare)
> 근거: implementation.md, post-push-verify 리포트, PostHog 신호

---

## 1. 현상

`https://virtue.oracle.shdkej.com` 첫 페이지 HTML에 `641덕`, 2026-05-13 날짜 샘플 deed 14건이
신규 방문자에게도 보인다. PostHog 신호에서 activation event가 거의 없음(deed_judged=1, deed_saved=0)에도
불구하고 덕력 수치가 높게 노출되어, 사용자가 앱을 "내 것"으로 느끼지 못할 가능성이 있다.

---

## 2. 루트 콜즈

### A. store.ts 초기화 로직 (확인된 원인)

`implementation.md` 기록:
> "상태 영속화: useSyncExternalStore 기반 store, 키 4종. **첫 로드 시 MOCK_DEEDS 14건 시드.**"

`mock-data.ts`에 정의된 `MOCK_DEEDS(14)`는 `INITIAL_VIRTUE`(641덕)를 포함하는 14개 시드 데이터.
localStorage에 `virtue.rebirth.v1` 키가 없을 때(신규 방문자) store가 MOCK_DEEDS로 초기화됨.

### B. NEXT_PUBLIC_SHOW_DEMO 가드 미배포 (주요 원인)

커밋 `dfaaf4e` (2026-05-15, "UX 개선 배치 정리 및 목업 제외")에서 `src/lib/store.ts`가 변경됨.
이 커밋에 `NEXT_PUBLIC_SHOW_DEMO` 가드가 추가된 것으로 추정:
> "production should start empty unless NEXT_PUBLIC_SHOW_DEMO=1" — marketing-01 신호

그러나 `post-push-verify` 리포트(2026-05-15T11:07Z) 기준:
- dfaaf4e는 origin/master에 push 완료
- **Oracle 서버 배포에는 반영되지 않음** (5개 페이지 응답 바이트·ETag가 push 전과 동일)
- `x-nextjs-cache: HIT`, `s-maxage=31536000` → 엣지가 구버전 빌드 서빙 중

### C. PM2 ecosystem.config.js 환경변수 미설정 (2차 위험)

현재 ecosystem.config.js에 `NEXT_PUBLIC_SHOW_DEMO` 항목이 없을 가능성이 높음.
가드가 배포되어도 환경변수 미설정 시 기본값이 falsy이면 정상 동작.
그러나 명시적으로 `NEXT_PUBLIC_SHOW_DEMO=0`을 설정해야 안전.

---

## 3. 수정 계획

### 단계 1 — Oracle 서버 배포 (dfaaf4e 반영)

```bash
# oracle 서버에서 실행
cd /srv/virtue-rebirth-app   # 실제 배포 경로 확인 필요
git pull origin master       # dfaaf4e 포함
pnpm install --frozen-lockfile
pnpm build
pm2 restart virtue
```

예상 결과: 신규 방문자에게 빈 상태로 시작. MOCK_DEEDS 미노출.

### 단계 2 — NEXT_PUBLIC_SHOW_DEMO 명시 설정

```js
// ecosystem.config.js
env: {
  NODE_ENV: "production",
  NEXT_PUBLIC_SCORING_MODE: "mock",
  NEXT_PUBLIC_SHOW_DEMO: "0",   // ← 추가: 명시적으로 demo 비활성화
}
```

### 단계 3 — 배포 후 검증 (LocalStorage 초기화 + HTTP 프로브)

```bash
# 1. 배포 버전 확인
curl -s https://virtue.oracle.shdkej.com | grep -o '"buildId":"[^"]*"'

# 2. 신규 방문자 시뮬레이션 (incognito + DevTools)
# - localStorage 비어있는 상태에서 / 접근
# - 덕력이 0이고 deed가 없어야 함
# - "아직 덕을 쌓은 기록이 없어요" 빈 상태 메시지 노출 확인
```

---

## 4. 배포 권한 분류

| 작업 | 권한 레벨 | 근거 |
|------|-----------|------|
| 배포 검증 (read-only) | L0 | 상태 확인만 |
| Oracle 서버 git pull + pnpm build | L1 | 허용된 로컬 빌드 |
| pm2 restart virtue | L2 (agent-approved 가능) | 되돌림 가능, 비용 없음, prod 영향 있으나 소범위 |
| ecosystem.config.js 수정 | L1 | 파일 수정 |

L2 자체 승인 조건 검토:
- ✅ 목표 Intent와 직접 연결
- ✅ pm2 restart는 되돌림 가능 (pm2 restart 재실행 또는 rollback)
- ✅ 예상 비용 발생 없음
- ✅ 시크릿 변경 없음 (NEXT_PUBLIC_SHOW_DEMO=0는 비밀이 아님)
- ✅ 타인에게 알림 없음
- ✅ 실행 전 현재 상태 확인 완료 (post-push-verify 리포트)
- ✅ 검증 방법: curl + incognito 테스트

→ **agent-approved L2 적용 가능** (로컬 Claude Code 위임 시 명시)

---

## 5. 리스크

- `dfaaf4e`의 `store.ts` 실제 변경 내용이 예상과 다를 수 있음 (직접 파일 열람 불가)
  → 로컬 실행 시 `git show dfaaf4e -- src/lib/store.ts`로 확인 필수
- Oracle 서버 배포 경로가 `/srv/virtue-rebirth-app`이 아닐 수 있음
  → `deployment-guide.md`의 "pnpm build → PM2" 가이드 참조 + `pm2 list`로 확인
