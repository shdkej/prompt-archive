# Power Automate 작업 가이드

## 기본 규칙

PA(Power Automate) Flow 작업 시 아래 규칙을 따릅니다:

- 산출물 구성:
  - **코드 보기용 JSON** (flow-N-codeview.json): PA 디자이너 "코드" 보기 참조용 (직접 붙여넣기는 동작하지 않음)
  - **단계별 구축 가이드** (step-by-step-guide.md): 디자이너에서 수동 구축용
  - **원본 정의 JSON** (flow-N-\*.json): 전체 연결정보 포함 참조용
- 코드 보기 JSON 포맷 (definition 부분만):
  ```json
  {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "contentVersion": "1.0.0.0",
    "triggers": { ... },
    "actions": { ... }
  }
  ```
- ZIP 패키지 가져오기는 PA에서 직접 내보낸 것만 인식하므로 사용하지 않음

## 배포

- **PA 생성 완료 후 배포**:
  - Microsoft Graph API를 사용할 수 있는 작업은 최대한 Graph API로 자동화 (Flow 생성, 커넥션 설정 등)
  - Graph API로 불가능한 작업 (UI 전용 설정, 커넥터 인증 등)은 브라우저(claude-in-chrome)로 직접 수행
- **PA Flow Management API를 통한 직접 배포**:
  - Playwright로 PA 디자이너 로그인 세션에서 localStorage의 MSAL 토큰(`service.flow.microsoft.com` 스코프) 추출
  - `api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments/{env}/flows/{flowId}` 엔드포인트 사용
  - GET으로 flow definition 전체 조회 -> JSON 수정 -> PATCH로 저장
  - **API로 추가/수정 가능**: InitializeVariable, SetVariable, Http, If(Condition), Foreach, Compose 등 빌트인 액션
  - **API로 추가 불가 -> UI에서 추가**: ApiConnection 타입 액션 (Teams, SharePoint, Outlook 등 커넥터 액션). 커넥션 인증 구조가 복잡하여 API로 신규 생성 불가. 단, UI에서 추가한 후 파라미터 수정은 API로 가능
  - 액션 간 실행 순서(runAfter) 변경, 파라미터 값 변경, 동적 콘텐츠 식 삽입 등은 API로 자유롭게 가능
  - `authentication: "@parameters('$authentication')"` 필드가 모든 ApiConnection 액션에 필요 (PA 새 디자이너 형식)
  - Copilot이 있는 환경에서는 Copilot 채팅으로도 액션 추가 시도 가능 (단, Premium 커넥터 제약 동일)

## 운영 원칙 (외부화)

PA Flow는 개발자가 만들지만 **비기술 운영자가 일상적으로 사용**합니다.
Flow 내부에 프롬프트, 이메일 템플릿, 출력 포맷, 수신자 목록 등을 하드코딩하지 않습니다.
운영자가 변경할 수 있는 값은 SharePoint 리스트/라이브러리로 외부화하여, Flow 수정 없이 동작을 변경할 수 있는 구조로 설계합니다.

### 외부화 패턴

- **SharePoint 리스트**: 키-값 쌍 (프롬프트, 설정값, 수신자 목록, 분기 조건값)
  - Flow에서 "Get items" 액션으로 로드
- **SharePoint 라이브러리**: 파일 기반 (HTML 이메일 템플릿, JSON Adaptive Card 템플릿)
  - Flow에서 "Get file content" 액션으로 로드
- 두 액션 모두 Standard 커넥터이므로 E3 라이선스로 사용 가능

### 설정 리스트 설계 원칙

PA Flow별 설정을 하나의 SharePoint 리스트로 관리할 때, 아래 원칙을 따릅니다.

#### 리스트 이름에 워크플로우 prefix 부여

여러 PA Flow가 같은 SharePoint 사이트를 공유하므로, 리스트 이름에 `[워크플로우명]` prefix를 붙여 소속을 명확히 합니다.

```
[법무배분] 플로우설정
[법무배분] 담당자풀
[사건검색] 설정
```

#### Description 컬럼: 비기술자가 이해할 수 있는 설명

설정 리스트에는 반드시 `Description` (설명) 컬럼을 추가하고, 기본 보기에 노출합니다. 설명은 기술 용어 대신 **운영자가 바로 이해할 수 있는 문장**으로 작성합니다.

| 나쁜 예 | 좋은 예 |
|---------|---------|
| GPT 시스템 프롬프트 | AI에게 역할을 알려주는 첫 번째 지시문입니다. "JSON 형식으로 응답하세요" 부분을 삭제하면 오류가 발생합니다. |
| GPT max_completion_tokens | AI 응답의 최대 길이입니다. 변경할 필요 없습니다. |
| Teams Channel ID | 알림을 보낼 Teams 채널 ID입니다. 테스트할 때 테스트 채널 ID로 바꾸세요. |

작성 기준:
- **무엇인지** 한 문장으로 설명
- **주의사항**이 있으면 이어서 (삭제하면 안 되는 것, 변경 불필요 등)
- 기술 용어(API Key, Token, JSON 등)는 꼭 필요한 경우에만, 맥락과 함께 사용

#### Category 컬럼: 설정의 성격별 분류

설정 항목이 많아질수록 한눈에 파악하기 어려우므로 Choice 타입의 `Category` (분류) 컬럼으로 그룹화합니다.

권장 분류:
- **프롬프트**: AI 지시문 관련
- **템플릿**: 메시지/이메일 형식 관련
- **기타**: 모델명, 채널 ID, 수치 설정 등

#### 기본 보기 구성

설정 리스트의 기본 보기에는 최소한 다음 컬럼을 노출합니다:

```
Title (설정키) | Description (설명) | Category (분류) | IsActive (활성여부)
```

설정값(ConfigValue/ConfigLongValue)은 목록에서 보기 어려우므로, 항목을 클릭해서 상세 보기로 확인하도록 합니다.

### 외부화 체크리스트

Flow 설계/구현 시 아래 항목을 점검합니다:

| 항목 | 외부화 대상 | 권장 저장소 |
|------|-------------|-------------|
| AI 프롬프트 | Compose/HTTP 액션 안의 프롬프트 텍스트 | SharePoint 리스트 (항목별 1행) |
| 이메일 템플릿 | Send Email 액션의 본문 HTML | SharePoint 라이브러리 (.html 파일) |
| Teams 메시지 템플릿 | Adaptive Card JSON | SharePoint 라이브러리 (.json 파일) |
| 출력 포맷/구조 | 결과물의 형식 정의 | SharePoint 리스트 (포맷 컬럼) |
| 수신자/채널 목록 | 하드코딩된 이메일/채널 ID | SharePoint 리스트 |
| 분기 조건값 | If/Switch의 임계값, 키워드 | SharePoint 리스트 |
| 스케줄/주기 | Recurrence 트리거 설정 | 외부화 불가 -- Developer 요청 필요 |

## 역할별 가이드

### Developer

- Flow 설계 시 외부화 체크리스트를 적용하여, 운영자가 변경할 값을 SharePoint로 분리
- SharePoint 리스트/라이브러리를 Flow보다 먼저 생성 (Lesson Learn 참조)
- Flow 완성 후 Operator에게 외부화 항목 목록을 전달하여 운영 가이드 작성 지원

### Operator

- PA Flow 크로스 리뷰 시 외부화 체크리스트를 점검하고, 하드코딩된 값이 있으면 Developer에게 외부화 요청
- Flow별 운영 가이드(`PA_OPERATIONS.md`) 작성:
  - Flow 개요 (무엇을 하는 Flow인지 한 줄 설명)
  - 외부 설정 위치 (SharePoint URL + 컬럼/파일 설명)
  - 변경 가능 항목 (운영자가 Flow 수정 없이 변경할 수 있는 것들)
  - 변경 불가 항목 (Developer에게 요청해야 하는 것들)
  - 트러블슈팅 (자주 발생하는 오류와 대응법)
  - 모니터링 (Flow 실행 이력 확인 방법)

### 크로스 리뷰

PA Flow 설계/구현 시:

| 역할 | 체크 관점 |
|------|-----------|
| Planner | 사용자 시나리오와 Flow 로직 일치 여부 |
| Operator | 외부화 체크리스트 적용, 운영자가 수정 가능한 구조인지 |
| Marketer | 고객 커뮤니케이션 템플릿의 톤앤매너 |

## Lesson Learn

- SharePoint 리스트/라이브러리 사용 시, 해당 리소스가 미생성 상태라면 반드시 먼저 생성한 후 워크플로우를 작성할 것
- PA 디자이너 "코드" 보기에 JSON을 직접 붙여넣는 방식은 동작하지 않음 -> 단계별 가이드로 수동 구축하거나 Flow Management API로 배포할 것
- **SharePoint REST API + Playwright 배포 패턴**: Playwright로 SharePoint에 로그인된 세션에서 `page.evaluate()` → `fetch()`로 REST API 호출. PnP PowerShell 없이 리스트 생성/컬럼 추가/데이터 입력/보기 수정 가능. 한글 리스트명은 `ListItemEntityTypeFullName`이 `SP.Data.ListNListItem` 형식으로 자동 생성되므로 반드시 조회 후 사용. `[]` 등 특수문자 포함 리스트명은 `getbytitle` 대신 GUID(`lists(guid'...')`)로 접근
- PA Flow Management API에서 HTTP 커넥터 사용 시 Premium 라이선스 필요 (E3만으로는 불가)
- **Flow Management API PATCH 시 OpenApiConnection 인증 처리**: GET으로 조회한 flow definition에는 각 액션 inputs에 `authentication: "@parameters('$authentication')"` 필드가 포함되어 있으나, PATCH 시에는 이 필드를 **모든 액션에서 제거**하고 대신 `properties.connectionReferences`를 PATCH body에 함께 포함해야 함. authentication 포함하면 `InvalidProperty`, 제거만 하고 connectionReferences 없으면 `MissingProperty` 에러 발생
- **Adaptive Card 동적 콘텐츠 JSON 이스케이프**: Adaptive Card의 messageBody JSON 문자열 안에 동적 변수를 삽입할 때, 변수 값에 `"`, `\`, 줄바꿈 등이 포함되면 JSON 파싱이 깨짐 (`InvalidJsonInBotAdaptiveCard` 에러). `replace()` + `decodeUriComponent('%5C')`로 이스케이프 처리 필요. 예: `@{replace(replace(replace(variables('var'),'"',concat(decodeUriComponent('%5C'),'"')),decodeUriComponent('%0D'),''),decodeUriComponent('%0A'),' ')}`
- **Solution-aware Flow도 API PATCH 가능** (이전 Lesson 정정): authentication 제거 + connectionReferences 포함하면 OpenApiConnection 액션(SharePoint Get items 등)도 API로 추가 가능. 단, SharePoint 리스트는 display name이 아닌 **GUID**로 참조해야 함 (display name 사용 시 `List not found` 에러)
- **이메일 액션 파라미터명 주의**: Outlook `SendEmailV2`의 본문 파라미터는 `emailMessage/Body` (Teams의 `body/messageBody`와 다름)
- **PA 식에서 coalesce + HTML 폴백 주의**: `coalesce(replace(...), '<html>폴백</html>')` 형태의 식에서 HTML 안의 특수문자가 파싱 에러를 유발할 수 있음. HTML 폴백이 필요하면 별도 Compose로 분리하거나 변수에 저장 후 참조
- **`@식` vs `@{식}` 차이 (중요)**: `@{}`는 string interpolation이므로 결과가 항상 **문자열**이 됨. 정수 필드(`max_completion_tokens`)에는 `@int(...)`, null 허용 날짜 필드(`DueDate`)에는 `@if(empty(...), null, ...)` 처럼 `@{}` 없이 사용해야 타입이 보존됨. `@{if(..., null, ...)}`는 null을 빈 문자열 `""`로 변환하여 날짜 파싱 에러 발생
- **replace() 치환값 null 방어 필수**: `replace(template, '{{key}}', value)` 에서 value가 null이면 런타임 에러 발생 (`expects its third parameter 'new string' to be a string`). 모든 치환값을 `coalesce(value, '')` 또는 `coalesce(value, '(없음)')` 으로 감싸야 함
- **Flow Management API 연속 PATCH 시 반드시 최신 GET 먼저**: 한 Flow를 여러 번 PATCH할 때, 이전에 GET한 definition을 재사용하면 앞선 PATCH의 수정이 롤백됨. 매 PATCH 전에 최신 definition을 GET한 후 수정해야 함. 예: 1차 PATCH로 Teams 중복 수정 → 2차 PATCH에서 수정 전 원본 기반으로 Planner만 수정 → Teams 중복이 다시 복원되는 사고 발생
