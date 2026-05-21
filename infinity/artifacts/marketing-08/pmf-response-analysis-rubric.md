---
작성일: 2026-05-21
Intent: marketing-08
Mode: 내부 기획 L1 (cloud draft — 로컬 검증 후 virtue-rebirth-app/docs/에 canonical 저장)
Status: cloud-draft
Owner: Marketer (Planner 검수, Developer/Operator 기존 이벤트 참조만)
Canonical target: /home/ubuntu/dev/virtue-rebirth-app/docs/pmf-response-analysis-rubric.md
Source note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
---

> 본 파일은 Infinity Artifact 레이어의 cloud 초안이다.
> 로컬 Claude Code가 source note를 직접 읽어 내용을 보완하고,
> first-impression-positioning-snapshot.md·minimum-viable-audience-brief.md 충돌 확인 후
> canonical 경로에 저장한다. 최종본과 충돌 시 canonical(virtue-rebirth-app 레포)이 우선이다.

# Virtue PMF 응답 분석 루브릭

## 0. 목적

Virtue prelaunch 첫 10명의 PMF 설문 응답을 **평균 만족도로 묵히지 않고**, "매우 아쉽다"
응답자의 persona·benefit·대체재 언어를 구조적으로 분리해 **high-expectation customer**를
찾는 것이 이 루브릭의 목적이다.

분석 결과는 다음 두 산출물로 직접 연결된다.

1. 다음 포지셔닝 문서 (`docs/first-impression-positioning-snapshot.md`) 업데이트 후보
2. 다음 온보딩 초안 (`docs/minimum-viable-audience-brief.md`) J1~J4 가중치 조정 후보

본 문서는 분석 체계를 정의하는 것까지만 한다. 응답 수집, 발송, 모집, 결과 정리는
별도 승인(§7)이 필요하다.

---

## 1. 분석 대상 및 전제 조건

### 분석 대상

`docs/first-impression-positioning-snapshot.md §4`에 정의된 PMF-1~4 설문의 응답.

| 질문 | 형식 | 분석 목적 |
|---|---|---|
| PMF-1 | 4지선다 (①매우 아쉽다/②조금 아쉽다/③아쉽지 않다/④이미 안 쓰고 있다) | 1차 필터 — ①을 격리 |
| PMF-2 | 자유 응답 (누구에게 가장 잘 맞을 것 같나요) | Persona 언어 수집 |
| PMF-3 | 자유 응답 (가장 마음에 든 점) | Benefit 언어 수집 |
| PMF-4 | 자유 응답 (사라지면 대신 뭘 쓸 건가요) | 대체재 카테고리 확인 |

### 전제 조건

- 설문 대상: `deed_saved` ≥ 1회 발생한 사용자 (seven-day-deed-loop.md §1 기준)
- 분석 시작 시점: PMF-1 ①응답자가 **2명 이상** 확보된 이후 (그 전에는 숫자 해석 보류)
- 분석 단위: PMF-2~4는 **①응답자만** 별도 분리해 본다. ②~④와 평균을 섞지 않는다

---

## 2. 1단계: PMF-1 분리 필터

### 분리 규칙

| PMF-1 응답 | 처리 방법 |
|---|---|
| ① 매우 아쉽다 | → **고기대 그룹**으로 분리. PMF-2~4 자유 응답 전체 태깅 |
| ② 조금 아쉽다 | → 보조 그룹. PMF-3만 참조(benefit 힌트). J1~J4 매핑은 선택적 |
| ③ 아쉽지 않다 | → 이탈 단서 그룹. PMF-4만 참조(대체재 확인). 포지셔닝 반면교사 |
| ④ 이미 안 쓰고 있다 | → 이탈 확정. PMF-4만 참조. 별도 메모. 평균에 포함 금지 |

### 집계 유의사항

- ① 비율을 40% 임계치 기준으로 판단하는 것은 **표본 ≥ 10명 이후**로 연기
- 표본 10명 미만에서는 응답자 1인당 카드를 만들어 패턴을 보는 방식 사용 (§5 참조)
- "40%를 넘겼다/못 넘겼다"가 아니라 ①응답자의 **언어 패턴**을 보는 것이 우선

---

## 3. 2단계: 고기대 고객 태깅 표

> 대상: PMF-1 ①응답자 전원. 응답 카드 1장씩 작성.

### 태깅 표 (응답 카드 포맷)

| 항목 | 내용 | 태깅 가이드 |
|---|---|---|
| **응답자 ID** | 익명 번호 (예: R01, R02) | — |
| **J 분류** | J1·J2·J3·J4 중 하나 (복수 가능) | §4 매핑 규칙 참조 |
| **Benefit 언어** | PMF-3 원문 발췌 + 핵심 단어 태그 | 예: `#사소한기록`, `#가벼운루틴`, `#AI피드백` |
| **대체재** | PMF-4 원문 발췌 + 카테고리 태그 | 예: `#감사일기앱`, `#Habitica`, `#없다` |
| **Persona 단서** | PMF-2 원문 발췌 + 직업/관심사/습관 키워드 | 예: `#일상기록러`, `#게임화선호`, `#AI얼리어답터` |
| **다음 카피 가설** | 이 응답자의 언어로 만들 수 있는 포지셔닝 후보 한 줄 | 기존 카피 후보(snapshot §5)와 거리 메모 |
| **온보딩 문서 연결** | 해당 J의 첫 문장·관찰 질문과 일치하는지 여부 | brief §2 참조 |

### 태깅 예시 (가상)

| 항목 | 예시 값 |
|---|---|
| 응답자 ID | R01 |
| J 분류 | J1 (기록형) |
| Benefit 언어 | "사진으로 하루가 정리되는 느낌" → `#일상정리`, `#시각기록` |
| 대체재 | "일기 앱이나 메모장을 쓸 것 같다" → `#일기앱`, `#메모장` |
| Persona 단서 | "사진 찍는 걸 좋아하는 친구" → `#일상기록러` |
| 다음 카피 가설 | "오늘 하루를 사진 한 장으로 정리한다" — snapshot 후보 1과 방향 일치, 단어 강화 후보 |
| 온보딩 문서 연결 | brief J1 첫 문장 `오늘 사소한 거 하나, 카메라로 콕.` 과 일치 |

---

## 4. J1~J4 매핑 규칙

> PMF-2·PMF-3·PMF-4 자유 응답에서 J를 추론하는 1차 단서 목록.
> 단서가 복수 J에 걸치면 가장 강한 신호 1개를 primary, 나머지를 secondary로 기록.

| J | PMF-2 persona 단서 | PMF-3 benefit 단서 | PMF-4 대체재 단서 |
|---|---|---|---|
| **J1 기록형** | "사진 찍는 것 좋아함", "일상 기록 습관", "공유보다 보관 선호" | "정리되는 느낌", "남는 게 있다", "사소한 게 쌓인다" | 일기 앱, 메모장, 모먼트, 구글포토, 없다 |
| **J2 누적형** | "게임 좋아함", "숫자·진행률 바 좋아함", "streak 동기" | "캐릭터가 자라는 게 좋다", "숫자가 올라가는 게 재밌다" | Habitica, Duolingo, Finch, 출석체크 앱 |
| **J3 AI 호기심형** | "AI 도구 일상 사용", "AI 얼리어답터", "챗봇 써봤지만 대화 길다" | "AI가 뭐라고 하는지 궁금하다", "생각지 못한 코멘트" | ChatGPT에게 물어봄, Replika, Pi, 없다 |
| **J4 회고형** | "명상·저널 시도했지만 압박감에 중단", "자기계발 피로", "도덕 언어 거부감" | "부담 없다", "설교 없이 확인되는 느낌", "칭찬도 설교도 없어서 좋다" | 명상 앱, 저널 앱, 안 썼을 것 같다, 없다 |

### 매핑 우선순위 규칙

1. PMF-4 대체재 카테고리가 가장 강한 J 단서다 — 대체재가 명확하면 J 분류가 따라온다
2. PMF-3 benefit 언어가 대체재와 일치하면 J 확정. 불일치하면 "혼합" 태그
3. PMF-2 persona는 J 가중치를 높이는 보조 단서 (단독으로 J를 확정하지 않음)
4. 어느 J에도 맞지 않는 응답은 `J-unknown` 태그 후 패턴이 보이면 J5 후보로 메모

---

## 5. 작은 표본 과대해석 금지선

표본이 작을 때 루브릭을 쓰는 목적은 **숫자 결론이 아니라 언어 패턴 수집**이다.

### 표본 단계별 해석 한계

| 표본 수 | 허용 해석 | 금지 해석 |
|---|---|---|
| 1~2명 | 개별 언어 패턴 기록 (카드 1~2장) | J 분포 집계 금지, 포지셔닝 확정 금지 |
| 3~5명 | 2건 이상 겹치는 benefit/대체재 언어 → "가설 신호"로 메모 | "우리 사용자는 J1이다" 단정 금지 |
| 6~9명 | J 분포 1차 윤곽, benefit 키워드 반복 2회+ → "포지셔닝 후보 강화 신호" | 40% 계산 후 통계적 유의미성 주장 금지 |
| 10명 이상 | ① 비율 40% 기준 1차 검토 허용 | "PMF 달성" 단정 금지. 외부 설문 확대 전 별도 Intent + 승인 |

### 과대해석 방지 점검 질문

루브릭 사용 시 아래 질문으로 자기 점검한다.

- "이 결론은 ①응답자만의 언어에서 온 것인가, 아니면 전체 응답 평균에서 온 것인가?"
- "이 J 분류가 응답자 본인의 말에서 나왔는가, 아니면 우리가 바라는 J에서 역추론한 것인가?"
- "이 benefit 단어를 카피에 쓴다면, 실제 응답에 그 단어가 2회 이상 등장했는가?"
- "표본이 10명 미만인데 '패턴'이라고 쓰고 있지는 않은가?"

---

## 6. 분석 결과 → 다음 문서 연결 규칙

태깅이 완료된 카드들에서 2건 이상 겹치는 패턴이 보이면 아래 기준으로 후속 문서에 연결한다.

### 포지셔닝 스냅샷 업데이트 트리거

| 조건 | 업데이트 대상 | 방법 |
|---|---|---|
| 특정 J의 benefit 언어가 ①응답자 2명+ 겹침 | snapshot §5 헤드라인/보조문구 후보 | 새 후보 1줄 추가 (기존 후보 삭제 금지, 추가만) |
| 현재 snapshot 후보 카피에 없는 새 단어가 2명+ 등장 | snapshot §5 비고 셀 | "응답 언어 기반 후보" 표시로 추가 |
| 특정 J가 ①응답자에서 과반 | snapshot §2 가설 우선순위 | Marketer + Planner 합의 후 가설 순서 조정 (별도 Intent) |

### MVA 기준표 업데이트 트리거

| 조건 | 업데이트 대상 | 방법 |
|---|---|---|
| 예상 J와 실제 J가 다른 응답이 2명+ | brief §2 해당 J 관찰 질문 | 새 관찰 질문 추가 |
| 예상 밖 대체재가 2명+ 등장 | brief §2 해당 J 첫 10명 후보 조건 | 조건 1줄 추가 (기존 조건 삭제 금지) |
| J-unknown 응답이 3명+ | brief §2 신규 J 후보 메모 | 별도 Intent 제안 (J 추가는 Planner 합의 필요) |

### 절대 연결 금지

- 응답 언어를 **앱 코드, 트래킹, UI 텍스트에 직접 반영하는 것**은 이 루브릭의 범위 밖이다.
  → 별도 Intent + L1/L2 분류 필요
- copy-spec.md 금지어는 응답 언어에 등장해도 카피 후보로 사용할 수 없다.
  → 응답자가 쓴 단어가 금지어이면 "금지어 대응 단어" 메모만 남긴다

---

## 7. 외부 발송 경계 (Out of scope / approval-needed)

| 액션 | L1 허용 | L2 승인 필요 |
|---|---|---|
| 루브릭 초안 작성 · 커밋 | ✅ | |
| 루브릭 기반 태깅 카드 작성 (응답 수집 후) | ✅ | |
| PMF 설문 문항 내부 초안 확정 | ✅ | |
| 설문 발송 (이메일·DM·인앱 노출 어느 채널이든) | | ✅ |
| 인터뷰 일정 요청 발송 | | ✅ |
| PostHog 설문 팝업·플래그 추가 | | ✅ |
| 응답 기반 포지셔닝 문서 공개 게시 | | ✅ |
| 응답 기반 카피 앱 반영 (코드 변경) | | ✅ |

---

## 8. First verification gate (선행 문서 충돌 점검)

### 8.1 PMF 질문 계승 점검

본 루브릭은 `docs/first-impression-positioning-snapshot.md §4`의 PMF-1~4 원문을 **수정 없이 계승**한다.

| 항목 | 충돌 여부 | 근거 |
|---|---|---|
| PMF-1 질문 원문 | 없음 | §2 필터 표에서 그대로 인용 |
| PMF-1 옵션 4개 | 없음 | §2 분리 규칙에 ①~④ 원문 그대로 사용 |
| PMF-2 질문 원문 | 없음 | §3 태깅 표 "Persona 언어" 항목이 PMF-2에 대응 |
| PMF-3 질문 원문 | 없음 | §3 태깅 표 "Benefit 언어" 항목이 PMF-3에 대응 |
| PMF-4 질문 원문 | 없음 | §3 태깅 표 "대체재" 항목이 PMF-4에 대응 |

### 8.2 J1~J4 / MVA 계승 점검

본 루브릭은 `docs/minimum-viable-audience-brief.md §2`의 J1~J4 정의를 **수정 없이 계승**한다.

| 항목 | 충돌 여부 | 근거 |
|---|---|---|
| J1 기록형 정의 | 없음 | §4 매핑 표에서 brief J1 첫 10명 조건·대체재 동일 출처 사용 |
| J2 누적형 정의 | 없음 | §4 매핑 표에서 brief J2 첫 10명 조건·대체재 동일 출처 사용 |
| J3 AI 호기심형 정의 | 없음 | §4 매핑 표에서 brief J3 첫 10명 조건·대체재 동일 출처 사용 |
| J4 회고형 정의 | 없음 | §4 매핑 표에서 brief J4 첫 10명 조건·대체재 동일 출처 사용 |
| 활성화 이벤트 | 없음 | 루브릭은 deed_saved/deed_judged를 참조만 함, 신규 이벤트 정의 없음 |

### 8.3 copy-spec 금지선 점검

| copy-spec 금지선 | 본 문서 충돌 여부 | 근거 |
|---|---|---|
| 도덕적 칭찬 / 인격 평가 단어 | 없음 | 카피 후보 없음, 루브릭·태깅 체계 문서 |
| 격언·명언 인용 | 없음 | 없음 |
| 무거운 단어 (미덕/선행/베풂 등) | 없음 | 없음 |
| 사용자 직접 칭찬 | 없음 | 없음 |

### 8.4 외부 발송/배포/트래킹/코드/시크릿/권한/공개 액션 비수행 명시

본 루브릭 초안 작성 및 커밋 과정에서 다음 액션은 단 한 건도 수행하지 않았다.

- 외부 발송: 설문·이메일·DM·푸시 어떤 채널로도 사용자/지인/외부에 메시지를 보내지 않았다.
- PostHog: 새 이벤트·속성·플래그 추가/수정 없음.
- 코드: `src/`·`api/`·런타임 설정 변경 없음. 변경은 `docs/`·infinity 문서 한정.
- 배포: 프로덕션 환경에 새 빌드 없음.
- 시크릿/권한: `.env*`·시크릿·API 키·권한 변경 없음.

---

## 로컬 실행 게이트 (local Claude Code 필요)

cloud 초안을 canonical 문서로 전환하기 전에 아래 순서를 따른다.

```
Infinity Intent: marketing-08 Virtue PMF 응답 분석 루브릭 작성
Mode: execute_local
Required workflow: Use workflow-master first. Read .agent/workflows/workflow-master.md before implementation.
Goal: docs/pmf-response-analysis-rubric.md에 PMF-1~4 태깅 체계, J1~J4 매핑 규칙,
      "매우 아쉽다" 그룹 우선 분석 규칙, 작은 표본 과대해석 금지선,
      외부 발송 approval-needed 경계를 작성
Context:
  - source_note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-21-pmf-response-engine.md
  - cloud_draft: prompt-archive/infinity/artifacts/marketing-08/pmf-response-analysis-rubric.md
  - refs: virtue-rebirth-app/docs/copy-spec.md
          virtue-rebirth-app/docs/first-impression-positioning-snapshot.md (PMF-1~4 원문)
          virtue-rebirth-app/docs/minimum-viable-audience-brief.md (J1~J4 기준)
Prepared findings: cloud draft 완료. source note 읽어 내용 보완 후 저장 권장.
                   PMF-1~4 원문·J1~J4 정의는 기존 문서에서 수정 없이 계승.
                   copy-spec 금지어 검사 필요.
Allowed: L0/L1 actions only
Forbidden: L2/L3 without approval (외부 발송·배포·트래킹·코드 변경 0건 유지)
Verification:
  rg "PMF-1|PMF-2|PMF-3|PMF-4" docs/pmf-response-analysis-rubric.md
  rg "J1 기록형|J2 누적형|J3 AI 호기심형|J4 회고형" docs/pmf-response-analysis-rubric.md
  rg "매우 아쉽다|고기대|과대해석" docs/pmf-response-analysis-rubric.md
  rg "approval-needed|L2 승인" docs/pmf-response-analysis-rubric.md
  git diff --name-only → docs/pmf-response-analysis-rubric.md 1개만 확인
Report back to: infinity/reports/marketing-08/{timestamp}.md
```

1. source note 읽기 → cloud 초안 내용 보완 (Sean Ellis/Superhuman 방법론 보강)
2. first-impression-positioning-snapshot.md PMF-1~4 원문 원본 그대로 계승 확인
3. minimum-viable-audience-brief.md J1~J4 정의 원본 그대로 계승 확인
4. copy-spec.md 금지어 명단 vs 루브릭 카피 충돌 검사
5. `virtue-rebirth-app/docs/pmf-response-analysis-rubric.md` 저장
6. rg 검증 게이트 통과 확인
7. 커밋/푸시 후 prompt-archive INTENTS.md Archive 이관 + 리포트 기록
