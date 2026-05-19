# marketing-05 Intent 원장

- id: marketing-05
- title: Virtue 빈 상태/첫 행동 감사표 작성
- status: archived
- created_at: 2026-05-19T22:00Z
- completed_at: 2026-05-19T22:07Z
- mode: execute_local
- route: Infinity router → local Claude Code (workflow-master classification: medium scope product audit doc 한 장, 4역할 관점은 산출물 내부에 압축)
- permission: L1 internal docs only, with agent-approved L2 normal-push to internal repos
- result_summary: Virtue 빈 상태 6개(ES-1 ~ ES-6)를 `상태 설명 → 기대 결과 → 첫 행동 CTA → 톤 위험 → 계측 후보` 다섯 칸으로 정리한 단일 감사 문서를 추가했다. 대시보드 최근 덕행 카드 내부 CTA에 대한 후보 A(현재 유지)/B(보조 CTA 추가) 두 안과 라벨 후보 3종, 톤 위험 등록부 T1–T5, PostHog `empty_state_seen` 외 2종의 신규 이벤트 정의 후보까지 한 장에 담았다. `docs/copy-spec.md` 금지어 명단(훌륭한·본받을·모범적인·귀감·인성·미덕·선행·베풂·봉사정신·마음이 따뜻한·좋은 사람·멋진 인격) 충돌 0건. 외부 발송·배포·트래킹·생산·시크릿·권한·공개 액션 0건.

## Artifacts

- path: /home/ubuntu/dev/virtue-rebirth-app/docs/empty-state-first-action-audit.md
  role: design
  note: Virtue 앱 레포 내 정식 product audit 산출물. 카피 변경 지시서가 아니며 후보·결정 가이드까지만 둠.

## Reports

- path: infinity/reports/marketing-05/2026-05-19T2207Z.md
  role: final
  note: 본 실행 1회의 로그. workflow-master 분류, L2 체크리스트, 검증 grep 결과, 커밋/푸시 정책 기록.

## Sources

- /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-19-empty-state-activation.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/copy-spec.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/seven-day-deed-loop.md
- /home/ubuntu/dev/virtue-rebirth-app/docs/first-impression-positioning-snapshot.md
- /home/ubuntu/dev/virtue-rebirth-app/src/app/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/app/deeds/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/app/add/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/app/dex/page.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/components/empty-state.tsx
- /home/ubuntu/dev/virtue-rebirth-app/src/lib/store.ts

## Success criteria coverage

| 성공 기준 | 충족 위치 |
|---|---|
| 대시보드/덕행록/add 전후 빈 상태별 표 | audit §1 (인벤토리) + §2.1 ~ §2.6 (감사) |
| `상태 설명` / `기대 결과` / `첫 행동 CTA` / `톤 위험` / `계측 후보` 다섯 칸 | audit §2.1 ~ §2.6 (각 ES마다 다섯 칸 모두 채움) |
| 카피 후보가 `copy-spec.md` 금지선을 위반하지 않음 | audit §4 위험 등록부 + §6 검증 게이트 + 본 report §5 grep 결과 |
| 도감(`/dex`) 빈 상태(잠긴 단계)도 포함 | audit §2.6 (ES-6) |
| `/add` 진입 전후 빈 상태 분리 | audit §2.4 (ES-4 사진 슬롯) + §2.5 (ES-5 미시도 안내) |

## Verification

- `docs/copy-spec.md` 금지어 명단을 본 audit의 카피 후보와 비교했고, 신규로 들어간 카피(§3 후보 B 라벨 3종: `여기에 한 컷 넣기`, `한 컷 골라보기`, `사진 하나 골라보기`)도 한 글자도 위반하지 않는다.
- Intent 요구 grep 게이트 실행 완료 (본 report §5).
- `src/lib/store.ts`의 `SHOW_DEMO` 기본 off → 첫 방문 시 정말로 빈 상태에서 시작함을 코드로 확인. 즉 audit의 ES-1/ES-2 가정이 현실과 정합.
- 코드/배포/시크릿/권한/트래킹/공개 액션 변경 0건. `docs/` 한 파일만 신규 추가.

## Commits

- repo: virtue-rebirth-app
  sha: ca2e007
  note: docs/empty-state-first-action-audit.md 추가, origin/master push 완료
- repo: prompt-archive
  content sha: eeda81a
  note: infinity/reports/marketing-05/2026-05-19T2207Z.md + infinity/intents/archive/marketing-05.md + INTENTS.md 갱신. Bookkeeping commit으로 본 ledger의 SHA 부기 후 origin/main push.

## URLs

- 외부 URL 게시 없음. 모든 변경은 내부 문서 및 사내 리포 한정.

## Next Actions

- ES-2 카드 내부 CTA: 후보 A vs B 결정 + 실제 적용은 별도 Intent로 분리 (Marketer + Planner 합의 → Developer 위임).
- PostHog `empty_state_seen` 외 신규 이벤트 도입 — 프라이버시 영향 점검과 PostHog 대시보드 변경 승인 후 별도 Intent.
- `/me`에서 `clearDeeds()` 직후 빈 상태(회수 시나리오) 카피 추가 — 별도 감사 Intent.
- 정식 출시 후 실 데이터 기반으로 ES-2 결정 재평가 + 본 감사표 갱신.
