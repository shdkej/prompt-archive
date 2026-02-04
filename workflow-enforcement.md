---
name: workflow-enforcement
description: 프로젝트 진행 시 Planner -> Developer -> Marketer -> Operator 4단계 워크플로우를 준수하고 관련 문서를 업데이트하도록 강제합니다.
---

# 전체 워크플로우 준수 및 문서화 규칙 (Full Lifecycle Rule)

이 규칙은 에이전트가 프로젝트를 수행할 때, **기획부터 운영까지** 이어지는 4단계 워크플로우를 순차적으로 따르고, 필수 문서를 최신 상태로 유지하도록 강제합니다.

## 0. 복합적 협업 우선 (Collaborative First)

순차적 실행 전에, **패널 토론 또는 브레인스토밍이 필요한지** 먼저 판단합니다.

### 패널 토론 트리거
다음 상황에서는 4개 역할이 **동시에** 관점을 제시합니다:
- 새 프로젝트/기능 시작 시 방향 설정
- 중요한 트레이드오프 의사결정
- 피벗이나 큰 방향 전환

### 브레인스토밍 트리거
다음 상황에서는 모든 역할의 아이디어를 **먼저 수집**합니다:
- 새로운 문제 해결 방안 탐색
- 사용자 경험 개선 아이디어
- 차별화 포인트 발굴

**참조**: `.agent/workflows/workflow_maker.md`의 "복합적 협업 메커니즘" 섹션

---

## 1. 워크플로우 실행 순서 (The 4-Step Cycle)

복합적 협업으로 방향이 정해진 후, 다음 순서로 실행합니다. 각 단계는 이전 단계의 산출물을 입력으로 받아 작업을 수행합니다.

### 1단계: Planner 모드 (기획)

- **참조 파일**: `.agent/workflows/planner.md`
- **목표**: 미니멀하고 회복 가능한(Recoverable) 스펙 확정.
- **행동**:
  - 요구사항 구조화 (MECE).
  - 핵심 가치 정의 및 불필요한 요소 제거.
- **산출물**: `PRODUCT_CONTEXT.md`의 **Planner Section** 내용 업데이트.
- **크로스 리뷰**: Developer(구현 가능성), Marketer(시장성), Operator(운영 리스크) 관점 검토.

### 2단계: Developer 모드 (개발)

- **참조 파일**: `.agent/workflows/developer.md`
- **목표**: 기획된 스펙을 실제 동작하는 코드로 구현.
- **행동**:
  - Stateless & Async 패턴 적용.
  - 코드 구현 및 테스트.
- **산출물**: `PRODUCT_CONTEXT.md`의 **Developer Section** 업데이트 및 배포.
- **크로스 리뷰**: Planner(기획 의도 반영), Marketer(릴리즈 준비), Operator(모니터링 준비) 관점 검토.

### 3단계: Marketer 모드 (홍보/전파)

- **참조 파일**: `.agent/workflows/marketer.md`
- **목표**: 구현된 가치를 고객(또는 사용자)에게 전달.
- **행동**:
  - 기술 가치 제안(Value Proposition) 정의.
  - 릴리즈 노트나 안내 문구 작성.
- **산출물**: `PRODUCT_CONTEXT.md`의 **Marketer Section** 업데이트.
- **크로스 리뷰**: Planner(핵심 가치 왜곡 없는지), Developer(기술 오류 없는지), Operator(CS 유발 요소) 관점 검토.

### 4단계: Operator 모드 (운영/피드백)

- **참조 파일**: `.agent/workflows/operator.md`
- **목표**: 안정적인 서비스 유지 및 피드백 루프 형성.
- **행동**:
  - 배포 후 모니터링 요령 파악.
  - 예상되는 이슈 및 대응 방안 수립.
- **산출물**: `PRODUCT_CONTEXT.md`의 **Operator Section** 업데이트.

## 2. 필수 문서 업데이트 (Artifact Management)

- **`PRODUCT_CONTEXT.md`**:
  - 모든 단계의 진행 상황과 의사결정을 누적하여 기록합니다.
  - 팀원(다른 에이전트 모드) 간의 소통 창구 역할을 합니다.

- **`API_SERVICE_LIST.md`**:
  - 새로운 서비스/API 추가 시 즉시 업데이트합니다.

## 3. 예외 상황

- 매우 긴급한 핫픽스(Hotfix)의 경우 `Operator -> Developer -> Operator`의 단축 경로를 사용할 수 있으나, 사후에 `Planner/Marketer` 관점의 회고를 남겨야 합니다.
