---
작성일: 2026-05-20
Intent: marketing-07
Mode: 내부 기획 L1 (cloud draft — 로컬 검증 후 virtue-rebirth-app/docs/에 canonical 저장)
Status: prepare_draft
Owner: Marketer
Canonical target: /home/ubuntu/dev/virtue-rebirth-app/docs/minimum-viable-audience-brief.md
Source note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-20-minimum-viable-audience.md
---

> 본 파일은 Infinity Artifact 레이어의 cloud 초안이다.
> 로컬 Claude Code가 source note를 직접 읽어 내용을 보완하고, copy-spec.md 및
> first-session-jtbd-matrix.md 충돌 확인 후 canonical 경로에 저장한다.
> 최종본과 충돌 시 canonical(virtue-rebirth-app 레포)이 우선이다.

# Virtue 최소 생존 오디언스 기준표

## 0. 목적

대중 홍보 이전, **JTBD 4잡 기준으로 "처음 보여줄 10명"의 조건을 명시한다.** prelaunch
상태에서 공개 런칭보다 먼저 오디언스·문장·관찰 질문을 맞춰, 작은 실사용 신호가 생겼을 때
포지셔닝과 활성화 해석을 선명하게 만드는 것이 목적이다.

본 문서는 오디언스 모집·초대·연락 지시서가 아니다. 외부 액션은 별도 L2 승인 후 진행한다.

## 1. 오디언스 범위 정의

- **범위**: Virtue 앱 내부 초대 또는 직접 관계 기반 비공개 공유 (공개 런칭 전)
- **목표**: Job별 최소 2–3명 관찰 가능한 실사용 신호 수집
- **기준**: 첫 화면 → 첫 행동 → 채점 결과의 전체 흐름을 1회 이상 경험하는 세션

## 2. JTBD 4잡별 기준표

### J1 기록형 — "오늘 괜찮은 하루를 사진으로 담아두고 싶다"

| 항목 | 내용 |
|---|---|
| **첫 10명 후보 조건** | 스마트폰 카메라로 일상 기록 습관 있음(주 3회+), 모먼트·구글포토·일기앱 사용 경험, SNS 공유보다 개인 보관 선호, 가볍게 기록하고 잊는 패턴, 복잡한 도구에 피로감 |
| **첫 문장** | `"오늘 사소한 거 하나, 카메라로 콕."` (현재 빈 상태 카피 — 수정 없이 J1에 가장 적합) |
| **첫 세션 가치 순간** | 첫 사진 추가 후 `deed_saved`, 홈 화면에서 방금 기록이 카드로 남는 것을 보는 순간 |
| **관찰 질문** | "오늘 찍은 게 뭐예요?" / "내일 다시 열어볼 것 같나요?" / "일기 앱이랑 뭐가 다른 것 같았어요?" / "부담스러운 부분이 있었나요?" |
| **승인 필요 외부 액션 경계** | DM·이메일 초대, 카메라·일기앱 커뮤니티 홍보, 인터뷰 일정 잡기 → L2 승인 필요 |

### J2 누적형 — "게임처럼 내 행동이 캐릭터로 쌓이는 걸 보고 싶다"

| 항목 | 내용 |
|---|---|
| **첫 10명 후보 조건** | Habitica·Duolingo·Finch 등 게임화 앱 사용 경험, 레벨업·streak·출석체크 동기 강함, 숫자·진행률 바에서 만족감, 캐릭터 성장 개념에 반응, 연속 기록을 끊지 않으려는 성향 |
| **첫 문장** | `"오늘 행동 하나, 환생종이 기억한다."` (캐릭터 신호 강조 변형 — copy-spec 충돌 로컬 확인 필요) |
| **첫 세션 가치 순간** | `deed_saved` 후 홈 화면 AnimatedNumber 변화·레벨 진행률 바 업데이트를 확인하는 순간 |
| **관찰 질문** | "숫자가 올라갈 때 어떤 느낌이었나요?" / "캐릭터가 변한 게 보였나요?" / "내일 또 쌓고 싶은 마음이 들었나요?" / "streak이 있으면 더 좋겠다는 생각이 들었나요?" |
| **승인 필요 외부 액션 경계** | 게임화·자기관리 커뮤니티 홍보, Habitica 포럼 링크 공유, 유저 초대 DM → L2 승인 필요 |

### J3 AI 호기심형 — "AI가 내 일상 한 컷을 짧게 평가해주는 루틴이 필요하다"

| 항목 | 내용 |
|---|---|
| **첫 10명 후보 조건** | ChatGPT·Claude 등 AI 도구 일상 사용, AI 코칭·피드백 서비스 관심, 긴 대화보다 짧은 인터랙션 선호, 외부 시선이 필요하지만 챗봇은 부담, AI 얼리어답터 성향 |
| **첫 문장** | `"오늘 한 컷, AI가 한 줄로 읽는다."` (현재 카피에 없음 — 첫 화면 AI 신호 추가 여부는 별도 Intent) |
| **첫 세션 가치 순간** | `deed_judged` 시점 — AI 채점 코멘트가 "생각지 못한 관점" 또는 "가볍게 맞다"는 반응을 일으키는 순간 |
| **관찰 질문** | "AI 코멘트가 맞았나요?" / "놀랍거나 뜻밖인 말이 있었나요?" / "챗봇이랑 어떻게 다른 것 같아요?" / "다른 사진으로도 해보고 싶은 마음이 들었나요?" |
| **승인 필요 외부 액션 경계** | AI 사용자·얼리어답터 커뮤니티 공유, Product Hunt 티저, AI 뉴스레터 언급 → L2 승인 필요 |

### J4 회고형 — "도덕적 부담 없이 나를 가볍게 돌아보는 루틴이 필요하다"

| 항목 | 내용 |
|---|---|
| **첫 10명 후보 조건** | 명상·저널앱 시도했지만 압박감에 중단한 경험, 자기계발 피로감·완벽주의 피로 있음, 도덕 언어·성찰 설교에 거부감, "이미 충분히 잘 하고 있음"을 확인받고 싶음, 가볍고 즐거운 루틴 원함 |
| **첫 문장** | `"어제보다 나아지지 않아도 된다. 오늘 사소한 거 하나만."` (현재 카피 확장 후보 — copy-spec 충돌 로컬 확인 필요) |
| **첫 세션 가치 순간** | AI 채점 코멘트에서 "칭찬·설교 없음"을 처음 경험하는 순간, 또는 `deed_saved` 후 "이 정도면 됐다"는 가벼운 완료감 |
| **관찰 질문** | "부담스럽지 않았나요?" / "AI 코멘트가 설교처럼 느껴진 부분이 있었나요?" / "다른 자기관리 앱이랑 분위기가 다른가요?" / "내일도 하고 싶나요?" |
| **승인 필요 외부 액션 경계** | 명상·자기계발·번아웃 커뮤니티 홍보, 인플루언서 접촉, 트위터·뉴스레터 공개 게시 → L2 승인 필요 |

## 3. 외부 액션 경계 요약 (전체 Job 공통)

| 액션 유형 | L1 허용 | L2 승인 필요 |
|---|---|---|
| 앱 내부 공유 링크 생성 | ✅ | |
| 직접 아는 사람에게 1:1 개인 공유 | ✅ | |
| DM·이메일 초대 발송 | | ✅ |
| 커뮤니티·포럼·SNS 공개 홍보 | | ✅ |
| 인터뷰·설문 일정 요청 발송 | | ✅ |
| 인플루언서·언론 접촉 | | ✅ |
| 공개 포스트·트윗·뉴스레터 기고 | | ✅ |

## 4. 첫 세션 학습 루프 (관찰 체계)

각 Job 후보자를 관찰할 때 아래 흐름을 기준으로 메모한다.

```
첫 화면 인상 → 첫 행동 결정 시간 → deed_saved 도달 여부
→ 가치 순간 자연 발화 여부 → 재방문 의향 발화 여부
```

관찰 후 기록:
- 어느 Job에 해당하는 것 같았는가 (사후 분류 가능)
- 가치 순간이 실제로 예측한 시점과 일치했는가
- 예상 밖의 반응이 있었는가 → 포지셔닝 가설 수정 신호

## 5. 선행 문서 충돌 점검 (로컬 검증 필요)

| 참조 문서 | 충돌 예상 | 로컬 확인 항목 |
|---|---|---|
| copy-spec.md | J2/J4 첫 문장 후보 검토 필요 | 금지어 명단 대비 첫 문장 3종 검사 |
| first-session-jtbd-matrix.md | 없음 (예상) | J1~J4 정의·마찰 위험·지표 참조 일치 확인 |

## 6. Out of scope

- 오디언스 모집·초대·DM·설문 실제 발송 (L2 승인 필요)
- J2/J4 첫 문장이 copy-spec 위반 시 수정 (별도 Intent)
- J3 첫 화면 AI 신호 추가 여부 결정 (별도 Intent, R3 고려)
- 인터뷰 가이드 전문 작성 (별도 Intent)
- 모집 채널·채널별 메시지 전략 설계 (별도 Intent + L2 승인)

---

## 로컬 실행 게이트 (local Claude Code 필요)

cloud 초안을 canonical 문서로 전환하기 전에 아래 순서를 따른다.

```
Infinity Intent: marketing-07 Virtue 최소 생존 오디언스 기준표 작성
Mode: execute_local
Required workflow: Use workflow-master first. Read .agent/workflows/workflow-master.md before implementation.
Goal: docs/minimum-viable-audience-brief.md에 JTBD 4잡별 첫 10명 후보 조건, 첫 문장,
      첫 세션 가치 순간, 관찰 질문, 승인 필요 외부 액션 경계를 표로 정리
Context:
  - source_note: /home/ubuntu/dev/knowledge-lab/source/external-links/marketing/2026-05-20-minimum-viable-audience.md
  - cloud_draft: prompt-archive/infinity/artifacts/marketing-07/minimum-viable-audience-brief.md
  - refs: virtue-rebirth-app/docs/copy-spec.md
          virtue-rebirth-app/docs/first-session-jtbd-matrix.md
Prepared findings: cloud draft 완료. J2/J4 첫 문장 copy-spec 충돌 확인 필요.
                   source note 읽어 내용 보완 후 저장.
Allowed: L0/L1 actions only
Forbidden: L2/L3 without approval (외부 발송·배포·트래킹·코드 변경 0건 유지)
Verification:
  rg "J1 기록형|J2 누적형|J3 AI 호기심형|J4 회고형" docs/minimum-viable-audience-brief.md
  rg "첫 10명|첫 문장|첫 세션|관찰 질문|승인 필요" docs/minimum-viable-audience-brief.md
  git diff --name-only → docs/minimum-viable-audience-brief.md 1개만 확인
Report back to: infinity/reports/marketing-07/{timestamp}.md
```

1. source note 읽기 → cloud 초안 내용 보완
2. copy-spec.md 금지어 명단 vs J2·J4 첫 문장 충돌 검사
3. first-session-jtbd-matrix.md J1~J4 정의와 일치 확인
4. `virtue-rebirth-app/docs/minimum-viable-audience-brief.md` 저장
5. rg 검증 게이트 통과 확인
6. 커밋/푸시 후 prompt-archive INTENTS.md Archive 이관 + 리포트 기록
```
