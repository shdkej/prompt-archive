# Power Automate 작업 가이드

PA(Power Automate) Flow 작업의 **단일 출처**는 `power-automate` 스킬이다.

- 스킬 본체: `~/dev/ai/kolon/ax-examples/power-automate/SKILL.md`
- 활성화 링크: `~/.claude/skills/power-automate`, `~/.openclaw/skills/power-automate`
- 트리거: "PA Flow 만들어줘", "Flow Management API로 배포", "SharePoint 외부화" 등

상세 워크플로우(산출물 구성, 외부화 체크리스트, SharePoint 설정 리스트 설계, Flow Management API 배포 패턴, 역할별 가이드, Lesson Learn)는 모두 스킬에서 관리한다. 이 문서는 정책 포인터만 유지한다.

## 핵심 정책

1. **운영자 외부화**: 프롬프트·이메일/Teams 템플릿·수신자·임계값은 SharePoint 리스트/라이브러리로 분리한다. Flow에 하드코딩 금지.
2. **API 우선 배포**: Microsoft Graph API → Flow Management API (PATCH) → Playwright UI 순으로 자동화 강도를 선택한다.
3. **표준 산출물 3종**: `flow-N-codeview.json` + `step-by-step-guide.md` + `flow-N-{name}.json`. ZIP 패키지 임포트는 PA가 직접 내보낸 것만 인식하므로 사용하지 않는다.
4. **운영 가이드 동반**: Flow별로 Operator가 `PA_OPERATIONS.md`를 작성한다 (외부 설정 위치, 변경 가능/불가 항목, 트러블슈팅).

## 변경 정책

- **PA 작업 절차/패턴/Lesson Learn 추가**: 스킬(`SKILL.md` 또는 `references/`)에 기록한다. 이 문서는 수정하지 않는다.
- **AX 프로젝트 전반의 정책 변경**: 이 문서를 갱신한다.

## 참고

- 스킬 references:
  - `references/lessons-learned.md` — 함정과 회피 패턴
  - `references/deployment-patterns.md` — Flow Management API PATCH 실전
  - `references/expression-cookbook.md` — `@식` vs `@{식}`, null 안전 치환
- 관련 스킬: `ms-graph` (M365 자원 조회), `security-checklist` (외부 유출 점검 시 PA는 사내 승인 SaaS로 분류)
