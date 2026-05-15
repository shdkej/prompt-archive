# marketing-01 · 로컬 실행 위임 프롬프트

> created: 2026-05-15 (heartbeat prepare)
> 용도: 사용자가 로컬 Claude Code에 붙여넣어 실행

---

## 프롬프트

```markdown
Infinity Intent: marketing-01 · Virtue 활성화 감사 (demo-state + 텔레메트리)
Mode: execute_local
Required workflow: workflow-master 먼저 실행. 복잡도 판단 후 진행.
Goal: demo-state 수정 배포 + PostHog 텔레메트리 개선 코드 적용
Allowed: L0/L1 자율 실행, L2(pm2 restart)는 아래 agent-approved 조건 충족 시 실행 가능
Forbidden: force push, 프로덕션 데이터 삭제, ANTHROPIC_API_KEY/시크릿 변경

---

## 작업 1: Demo-State 루트 콜즈 확인

레포 경로: /home/ubuntu/dev/virtue-rebirth-app

1. `git show dfaaf4e -- src/lib/store.ts` 실행하여 NEXT_PUBLIC_SHOW_DEMO 가드가
   실제로 추가되었는지 확인.
   - 가드가 있으면: 단계 2로 진행
   - 가드가 없으면: 아래 가드 코드를 직접 추가

2. 가드 코드 예시 (없는 경우에만 추가):
   ```ts
   // src/lib/store.ts 초기화 부분
   const showDemo = process.env.NEXT_PUBLIC_SHOW_DEMO === '1';
   const initialDeeds: Deed[] = showDemo ? MOCK_DEEDS : [];
   const initialVirtue: number = showDemo ? INITIAL_VIRTUE : 0;
   ```

3. Oracle 서버 배포:
   ```bash
   # Oracle 서버 SSH 접속 후
   cd /srv/virtue-rebirth-app   # 실제 경로: pm2 list로 확인
   git pull origin master
   pnpm install --frozen-lockfile
   pnpm build
   pm2 restart virtue
   ```
   (L2 agent-approved — 되돌림 가능, 비용 없음, 검증 방법 있음)

4. ecosystem.config.js에 환경변수 추가:
   ```js
   NEXT_PUBLIC_SHOW_DEMO: "0",
   ```

5. 배포 후 검증:
   ```bash
   curl -sI https://virtue.oracle.shdkej.com | grep etag
   curl -s https://virtue.oracle.shdkej.com | grep -o '덕\|641\|MOCK'
   ```
   예상: 641 미노출, ETag 변경

---

## 작업 2: PostHog 텔레메트리 개선

참조: infinity/artifacts/marketing-01/telemetry-fix.md

우선순위 순으로 적용:

1. `src/app/error.tsx` 생성 — captureException 포함 (파일 없는 경우)
2. `src/app/add/page.tsx` — deed_judged / deed_saved 이벤트 프로퍼티 확장
3. `pnpm typecheck && pnpm lint && pnpm build` 통과 확인

코드 초안은 telemetry-fix.md §3 참조.

---

## 검증 게이트

| 항목 | 기준 |
|------|------|
| pnpm typecheck | PASS (0 errors) |
| pnpm lint | PASS (0 errors) |
| pnpm build | PASS |
| 신규 방문자 시뮬레이션 | localStorage 비우고 접근 시 0덕·빈 화면 |
| PostHog 이벤트 | deed_judged에 source/score/has_photo 필드 존재 |
| $exception | message 필드 null이 아닌 실제 값 |

---

## Report back to

infinity/reports/marketing-01/{YYYY-MM-DDTHH-MM}-local-execution.md

최소 포함 항목:
- 배포 전후 ETag 비교
- 가드 코드 실제 존재 여부 (git show 결과)
- typecheck/lint/build 결과
- 신규 방문자 테스트 결과 스크린샷 또는 HTML 발췌
```
