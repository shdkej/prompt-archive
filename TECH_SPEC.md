#### 코드레벨 아키텍처 마스터피스

# Clean Architecture 설계 가이드

다음 아키텍처 패턴을 사용하여 코드를 설계해주세요.

## 최초 세팅 시 가이드

만약 프로젝트 최초 생성 시 요구사항이라면 각 레이어를 폴더 구조가 아니라 레이어별 단일 파일로 생성해주세요.

- 기본 스택
  - typescript 기반 nextjs
  - 서버리스 우선
    - 서버 필요할 경우 AWS ECS
  - upstash redis
- SEO, GEO(Generative Engine Optimization) 적용 고려
  - SSG 사용
- 인증
  - OAuth google로 세팅. httponly 쿠키 설정
  - 로컬에서는 /api/mock을 통해 인증 통과하도록 설정
  - upstash redis 를 이용해 백엔드 세션 관리
- FailOver, Recovery 되도록
- 비동기 가능한 부분은 비동기 처리
- 모니터링 계측 추가
  - 로그 처리
  - prometheus metric 처리
- 필수 기능에 대한 간단한 테스트 작성
- 피처플래그를 통한 관리
- 인프라 관련
  - CI/CD github workflows로 설정
  - dockerize
    - 작은 컨테이너 이미지, 빠른 스타트
  - stateless 우선

## 📋 아키텍처 원칙

### 1. Controller (Lambda Handler)

- **목적**: API 엔드포인트 역할, 비즈니스 플로우를 책처럼 읽히도록 구성
- **규칙**:
  - 1단계 if문만 허용 (간단한 조건문만)
  - 함수명만으로 전체 비즈니스 흐름이 이해되도록 작성
  - 각 줄이 하나의 완성된 비즈니스 액션을 나타냄
  - 구현 세부사항은 완전히 숨김

```
// ✅ 올바른 예시
exports.createUserHandler = async (event) => {
    const request = JSON.parse(event.body);

    await validateUserRequest(request);
    await checkEmailAvailability(request.email);
    await verifyUserPermissions(request);
    const userData = await createNewUser(request);
    await sendWelcomeEmail(userData);

    return buildSuccessResponse(userData);
};
```

### 2. Facade (선택적 - 복잡한 에러 처리 필요시에만)

- **목적**: Controller와 Service 사이의 에러 처리 및 복합 로직 관리
- **규칙**:
  - 단순한 CRUD는 생략 가능 (유연성 확보)
  - 복잡한 비즈니스 로직이나 다양한 에러 처리가 필요할 때만 사용
  - 모든 예외를 적절한 비즈니스 예외로 변환

```
// ✅ 복잡한 경우에만 사용
const UserFacade = {
    async validateUserRequest(request) {
        try {
            await UserService.validateRequest(request);
        } catch (error) {
            throw new ValidationError('사용자 요청 검증 실패', error);
        }
    }
};
```

### 3. Service

- **목적**: 비즈니스 로직들을 조합하여 하나의 완성된 기능 구현
- **규칙**:
  - 간단한 유닛 함수들을 묶어서 비즈니스 로직 구성
  - Domain의 순수 함수들을 조합하여 사용
  - 외부 시스템과의 연동 관리

```
// ✅ 유닛 함수들의 조합
const UserService = {
    async createUser(request) {
        UserDomain.validateEmailFormat(request.email);
        const hashedPassword = UserDomain.hashPassword(request.password);
        const userData = UserDomain.buildUserData({...request, password: hashedPassword});
        return await UserRepository.save(userData);
    }
};
```

### 4. Domain

- **목적**: 순수한 비즈니스 로직을 담은 유닛 함수들
- **규칙**:
  - 외부 의존성 없는 순수 함수들만 포함
  - 각 함수는 하나의 명확한 비즈니스 규칙만 담당
  - 테스트하기 쉬운 작은 단위로 구성

```
// ✅ 순수 함수들
const UserDomain = {
    validateEmailFormat(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            throw new Error('INVALID_EMAIL_FORMAT');
        }
    },

    hashPassword(password) {
        return `hashed_${password}`;
    }
};
```

### 5. Entity/Model

- **목적**: 데이터 구조와 기본 검증을 담당하는 래퍼 클래스
- **규칙**:
  - 리턴값과 데이터를 감싸주는 래퍼 역할
  - 기본적인 데이터 검증 포함
  - 데이터 변환 및 직렬화 담당

## 🎯 설계 요청 가이드

### 요청할 때 포함해야 할 정보:

1. **비즈니스 요구사항**: 구체적인 기능 설명
2. **API 스펙**: 엔드포인트, 요청/응답 형식
3. **복잡도**: 단순한 CRUD인지, 복잡한 비즈니스 로직인지
4. **플랫폼**: Node.js Lambda, Express, 기타

### 설계 시 고려사항:

- **가독성 우선**: Controller에서 비즈니스 플로우가 한눈에 보이도록
- **함수명의 명확성**: 각 함수명이 정확한 비즈니스 의미를 담도록
- **책임 분리**: 각 계층이 명확한 단일 책임을 가지도록
- **유연성**: 복잡도에 따라 Facade 포함/제외 결정
- **에러 처리**: 일관된 에러 처리 전략

## 📝 설계 요청 템플릿

[비즈니스 요구사항]

- 기능: 사용자 주문 생성
- 복잡도: 재고 확인, 결제 처리, 알림 발송 등 다단계 처리
- 플랫폼: Node.js Lambda

[API 스펙]

- POST /orders
- Request: { userId, items, paymentInfo }
- Response: { orderId, status, estimatedDelivery }

[특별 요구사항]

- 재고 부족 시 대안 상품 제안
- 결제 실패 시 자동 재시도
- 실시간 알림 발송

위 아키텍처 패턴으로 설계해주세요.

## 추가 설계 체크 포인트:

아래 내용에 대한 필요 여부를 묻고 필요하다면 생성해주세요

- docs 처리 (openapi)
- 고도화 된 test 처리
- MCP, API Endpoint 처리
- 플러그인 제공 가능한 방식

## ⚠️ 주의사항

1. **함수명과 실제 동작 일치**: 함수명이 단순해 보여도 내부 동작이 복잡하면 안됨
2. **숨겨진 상태 변화 금지**: 함수 간 데이터 전달은 명시적으로
3. **에러 추적 가능**: 각 단계별로 명확한 에러 처리
4. **과도한 추상화 지양**: 불필요한 래핑 함수 생성 금지

이 가이드를 참고하여 **책처럼 읽히는 코드**를 만들어주세요!
