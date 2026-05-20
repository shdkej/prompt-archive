---
작성일: 2026-05-20
Intent: marketing-06
Mode: 내부 기획 L1 (cloud draft — 로컬 검증 후 virtue-rebirth-app/docs/에 canonical 저장)
Status: prepare_draft
Owner: Marketer (Planner/Operator/Developer 관점 포함)
Canonical target: /home/ubuntu/dev/virtue-rebirth-app/docs/jtbd-first-session-matrix.md
---

> 본 파일은 Infinity Artifact 레이어의 cloud 초안이다.  
> 로컬 Claude Code가 virtue-rebirth-app 파일을 직접 확인한 후 canonical 경로에 최종본을 저장한다.  
> 최종본과 충돌 시 canonical(Virtue 앱 레포)이 우선이다.

# Virtue 첫 세션 JTBD 매트릭스

## 0. 목적

ProductLed/Ramli John 온보딩 관점: 활성화 지표는 사용자가 제품을 "고용"하는 동기(Jobs to Be Done)에 묶여야 한다. Virtue는 prelaunch 상태라 실제 세그먼트를 확정할 수 없지만, **현재 첫 화면·빈 상태·첫 7일 루프 문서가 어떤 Job을 약속하는지 한 장으로 연결**하면 이후 카피/인터뷰/측정 후보의 기준점이 생긴다.

본 문서는 카피 변경 지시서가 아니다. 변경 적용은 별도 Intent에서 합의 후 진행한다.

## 1. JTBD 정의 원칙

- Job은 "제품 기능"이 아니라 사용자가 달성하고 싶은 **결과 + 맥락 + 동기**다 (Christensen 식 정의)
- 한 사람이 여러 Job을 동시에 가질 수 있지만, 첫 세션의 "고용 결정"은 **지배적 Job 1개**가 주도한다
- 본 매트릭스는 현재 Virtue 첫 화면·첫 행동·참조 문서가 어떤 Job을 약속하는지 한 장으로 연결해, 메시지 정합도의 공백을 드러낸다

## 2. Job 후보 4개 정의 (요약 표)

| Job ID | Job 명 (사용자 언어) | 대안 카테고리 | 지배적 트리거 |
|---|---|---|---|
| J1 | "오늘 괜찮은 하루를 사진으로 담아두고 싶다" | 감사일기, 무드 트래커, 사진 다이어리 | 오늘 하루 지나치기 전에 뭔가 남기고 싶은 순간 |
| J2 | "게임처럼 내 행동이 캐릭터로 쌓이는 걸 보고 싶다" | Habitica, Finch, 출석체크 앱 | 작은 습관을 RPG 방식으로 즐기고 싶을 때 |
| J3 | "AI가 내 일상 한 컷을 짧게 평가해주는 루틴이 필요하다" | Replika, AI 코칭 챗봇, 셀프체크 앱 | 대화 길게 하기 싫지만 외부 시선이 필요할 때 |
| J4 | "도덕적 부담 없이 나를 가볍게 돌아보는 루틴이 필요하다" | 명상 앱, 저널 앱, 아무것도 안 씀 | 자기 인식 욕구 + 무거운 성찰 피로감이 동시에 있을 때 |

## 3. Job별 5칸 매핑

### J1 — "오늘 괜찮은 하루를 사진으로 담아두고 싶다"

| 항목 | 현재 상태 |
|---|---|
| **첫 화면 약속** | 최근 덕행 빈 상태 카피 `오늘 사소한 거 하나, 카메라로 콕.`이 J1에 가장 강하게 대응한다. 단, 현재 기본 Greeting(`오늘 1덕만 쌓아볼까요?`)의 "1덕"이 즉시 해석되지 않아 약속이 한 박자 늦게 전달된다. |
| **첫 행동** | `오늘 덕 쌓기` CTA → 갤러리/카메라 선택 → 사진 선택 → (선택적) 텍스트 메모 → AI/mock 채점 → `deed_saved` 이벤트 발생 |
| **성공 지표** | 첫 세션 `deed_saved` ≥ 1 (seven-day-deed-loop §1 정의와 동일). `add_flow_started → deed_saved` 전환율 |
| **마찰 위험** | **R1** "덕"의 추상도 (first-impression §3): 신규 방문자가 "일기 앱 맞나?"를 추리하는 사이 이탈. **ES-4** 사진 슬롯 빈 상태(`오늘의 한 컷`) 도달 전 이탈 리스크 (empty-state-audit §2.4) |
| **현재 근거 문서** | first-impression-positioning-snapshot.md §2A, §5 후보 1; empty-state-first-action-audit.md §2.1 ES-1, §2.4 ES-4 |

### J2 — "게임처럼 내 행동이 캐릭터로 쌓이는 걸 보고 싶다"

| 항목 | 현재 상태 |
|---|---|
| **첫 화면 약속** | 환생종 카드(이모지 + Lv.N + 진행률 바) + `나의 덕력` 큰 숫자(AnimatedNumber)가 J2 신호를 가장 강하게 전달한다. 단, 첫 방문 시 숫자 0·Lv.1이라 "진행 가능성"보다 "아직 시작 안 됨"이 먼저 노출된다. |
| **첫 행동** | 환생종 카드 → 진행률 확인 → `오늘 덕 쌓기` → `deed_saved` → 대시보드 복귀 → AnimatedNumber 변화 확인 (행동 피드백 루프 완성) |
| **성공 지표** | `deed_saved` 이후 대시보드 복귀 시 숫자 변화 관찰 (피드백 루프 완성). D3 기준 `deed_saved` ≥ 2 (seven-day-deed-loop §2 D3 마일스톤) |
| **마찰 위험** | **R2** "환생"이 종교/게임 중 어느 쪽인지 모호 (first-impression §3). 첫 방문 빈 대시보드(ES-1)에서 Lv.1 + 0덕이 "아직 아무것도 없음" 신호로 읽혀 J2 사용자의 참여 의지를 약화시킬 수 있음. |
| **현재 근거 문서** | first-impression-positioning-snapshot.md §2B, §1(요소 2·3); seven-day-deed-loop.md §2 D3 마일스톤; empty-state-first-action-audit.md §2.1 ES-1 |

### J3 — "AI가 내 일상 한 컷을 짧게 평가해주는 루틴이 필요하다"

| 항목 | 현재 상태 |
|---|---|
| **첫 화면 약속** | **현재 첫 화면에 AI 신호 없음.** AI 채점 기능은 `/add` 페이지의 채점 단계에서 처음 노출된다. J3 사용자는 첫 화면만 보고 "AI 피드백 앱"임을 알 수 없어 인지 진입 장벽이 있다 (first-impression §2C 취약점). |
| **첫 행동** | `오늘 덕 쌓기` → 사진 선택 → (이 시점에 AI 시그널 최초 노출) → AI 채점 대기 → 점수·코멘트 확인 → `deed_judged` → `deed_saved` |
| **성공 지표** | `deed_saved` 이후 채점 결과 페이지 체류(추정). `deed_judged` 이벤트 발생 (seven-day-deed-loop §3 신규 이벤트 후보) |
| **마찰 위험** | **인지 불일치**: 다른 Job을 기대하고 들어왔다가 AI 채점에서 뒤늦게 제품 본질을 인식하는 경우. **채점 신뢰**: "AI 점수가 믿을 만한가?" 의심이 첫 채점 결과 확인 시 발생. mock 모드에서 동일 톤 유지 여부 확인 필요. |
| **현재 근거 문서** | first-impression-positioning-snapshot.md §2C, §5 후보 3; empty-state-first-action-audit.md §2.4 ES-4, §2.5 ES-5 |

### J4 — "도덕적 부담 없이 나를 가볍게 돌아보는 루틴이 필요하다"

| 항목 | 현재 상태 |
|---|---|
| **첫 화면 약속** | `오늘 사소한 거 하나, 카메라로 콕.` 카피가 "부담 없는" 톤을 가장 직접적으로 약속한다. copy-spec.md 금지어 명단(도덕 칭찬·설교어 일체 금지)이 제품 전체에서 이 약속을 보호하는 가드레일 역할을 한다. |
| **첫 행동** | 빈 상태 카피 읽기 → `오늘 덕 쌓기` → 사소한 행동 사진 → (mock/AI) 채점 → `deed_saved`. 핵심은 채점 결과가 "사실 묘사 + 가벼운 농담"(도덕 판단 없음)임을 첫 채점에서 확인하는 것. |
| **성공 지표** | `deed_saved` ≥ 1 + 채점 결과 페이지에서 "칭찬·설교 없음" 인식 (현재 계측 불가, 정성적). D7 내 `deed_saved` ≥ 3 (seven-day-deed-loop §2 D7 마일스톤) |
| **마찰 위험** | **R1 심층**: "덕(德)" 어휘 자체가 도덕 언어로 읽혀 "또 무거운 앱이네" 첫인상. copy-spec 금지어는 Greeting 한 줄을 보호하지만 `덕력`·`덕행` 카드 레이블이 J4 사용자에게 무게감을 줄 수 있음. |
| **현재 근거 문서** | copy-spec.md (금지어 명단 전체); first-impression-positioning-snapshot.md §3 R1; seven-day-deed-loop.md §3 유연성 원칙; empty-state-first-action-audit.md §4 톤 위험 등록부 T1–T5 |

## 4. Job-메시징 정합도 요약 표

| Job | 첫 화면 약속 강도 | 첫 행동 명확도 | 성공 지표 계측 가능 | 가장 큰 마찰 |
|---|---|---|---|---|
| J1 자기관찰·기록 | 중 ("1덕" 모호, 빈 상태 카피는 강함) | 높음 | 높음 (`deed_saved`) | R1 ("덕" 해석 지연) |
| J2 게임화·진행 | 중 (환생종 카드 강함, 0덕 빈 시작) | 중 (피드백 루프까지 1단계 더) | 중 (AnimatedNumber 관찰 불가) | R2 (환생 모호 + 빈 시작점) |
| J3 AI 피드백 | 낮음 (첫 화면에 AI 신호 없음) | 중 (AI는 `/add`에서 등장) | 중 (`deed_judged` 신규 이벤트 필요) | AI 인지 불일치 |
| J4 부담 없는 자기 인식 | 높음 ("사소한" 카피가 가장 직접적) | 높음 | 낮음 (정성적) | R1 심층 ("덕" 도덕 언어) |

**우선순위 권장**: J1·J4가 현재 첫 화면과 가장 정합하고 약속이 명확하다. J2는 첫 화면 진입 메시지 보강, J3는 `/add` 이전 AI 신호 노출 여부를 먼저 결정한 뒤 별도 Intent로 처리한다.

## 5. 기존 문서 충돌 점검 (필수 게이트)

| 기존 문서 | 충돌 여부 | 근거 |
|---|---|---|
| first-impression-positioning-snapshot.md | **없음** | 본 매트릭스의 J1~J4는 가설 A/B/C를 사용자 동기 언어로 재표현. 어떤 가설도 부정하거나 재정의하지 않음. §부록에 Job-가설 대응 표 첨부. |
| empty-state-first-action-audit.md | **없음** | ES-1~ES-6 분류가 그대로 인용됨. 빈 상태 레이블·순서·카피 후보를 변경하지 않음. |
| seven-day-deed-loop.md | **없음** | D1/D3/D7 마일스톤 정의를 성공 지표 섹션에서 그대로 인용. `deed_saved` 중심 루프 정의를 바꾸지 않음. |

## 6. 외부 발송·트래킹 변경·코드 변경 비수행 명시 (필수)

본 산출물 작성 과정에서 다음 액션은 단 한 건도 수행하지 않았다:

- 외부 발송 (이메일·SMS·푸시·DM·설문·SNS) 0건
- 트래킹 변경 (PostHog 이벤트·속성·플래그 추가/수정) 0건
- 코드 변경 (`src/`, `api/`, `public/`, 런타임 설정) 0건
- 배포 0건, 시크릿/권한 변경 0건, 공개 액션 0건

## 7. Out of scope

- 각 Job별 첫 화면 카피 실제 변경 (별도 Intent + Marketer/Planner 합의)
- J2 개선: 환생종 카드 진입 메시지 보강 (별도 Intent)
- J3 개선: 첫 화면에 AI 신호 추가 여부 결정 (별도 Intent, R3 리스크 고려)
- PostHog `deed_judged`·`first_session_deed_saved` 신규 이벤트 추가 (별도 Intent + 승인)
- 인터뷰 설계, 사용자 세그먼트 모집, 외부 설문 발송 (별도 승인 필요)
- 각 Job 세그먼트별 A/B 헤드라인 테스트 (코어 경험 사용자 임계치 도달 후 별도 Intent)

## 부록: Job-포지셔닝 가설 대응 표

| Job | 대응 가설 (first-impression-snapshot.md §2) | 비고 |
|---|---|---|
| J1 자기관찰·기록 | 가설 A (자기관찰 게임) | 현재 첫 화면과 가장 강한 정합도 |
| J2 게임화·진행 | 가설 B (라이프 RPG) | 환생종 카드에서 강하게 읽힘 |
| J3 AI 피드백 | 가설 C (AI 셀프 거울) | 현재 첫 화면 신호 가장 약함 |
| J4 부담 없는 자기 인식 | 가설 A+B 교차 (copy-spec 보호) | 단일 가설보다 톤 레이어에 가까움 |

---

## 로컬 검증 게이트 (local Claude Code 실행 필요)

본 cloud 초안을 canonical 문서로 전환하기 전에 아래를 순서대로 확인한다.

1. 파일 읽기:
   - `virtue-rebirth-app/src/app/page.tsx` → 첫 화면 요소(Greeting·덕력 카드·환생종 카드·CTA) 최신 상태 확인
   - `virtue-rebirth-app/src/app/add/page.tsx` → AI 채점 시그널 첫 등장 위치 확인
   - `virtue-rebirth-app/docs/first-impression-positioning-snapshot.md`
   - `virtue-rebirth-app/docs/empty-state-first-action-audit.md`
   - `virtue-rebirth-app/docs/seven-day-deed-loop.md`

2. 필요 시 Job 정의 또는 마찰 위험 내용을 업데이트한 뒤 `virtue-rebirth-app/docs/jtbd-first-session-matrix.md`에 저장

3. rg 검증 (산출물에 아래 항목 존재 확인):
   ```
   rg "J1|J2|J3|J4" docs/jtbd-first-session-matrix.md
   rg "deed_saved" docs/jtbd-first-session-matrix.md
   rg "deed_judged" docs/jtbd-first-session-matrix.md
   rg "Out of scope" docs/jtbd-first-session-matrix.md
   ```

4. 완료 후 `prompt-archive`의 본 파일과 `INTENTS.md`를 갱신하고 커밋/푸시
