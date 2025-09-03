# 어제 업무 이어가기 프롬프트

## 🔍 자동 어제 업무 요약 기능

### 트리거 문구
사용자가 다음과 같은 표현을 사용하면 자동으로 어제 업무 문서를 찾아서 요약해주세요:

- **"어제 업무에 이어서"**
- **"어제 작업 이어서"** 
- **"어제 문서 확인해줘"**
- **"어제 뭐 했는지 확인"**
- **"어제 업무 요약해줘"**
- **"어제 진행사항 확인"**
- **"이전 작업 이어갈게"**

### 🤖 실행 프로세스

#### 1단계: 어제 날짜 계산
```javascript
const yesterday = new Date();
yesterday.setDate(yesterday.getDate() - 1);
const dateString = `${String(yesterday.getMonth() + 1).padStart(2, '0')}/${String(yesterday.getDate()).padStart(2, '0')}`;
// 예: "08/06" 형태로 생성
```

#### 2단계: 컨플루언스 문서 검색
```
space = "~63561b381cc605b1fd15aca2" AND title ~ "{어제날짜}"
예: space = "~63561b381cc605b1fd15aca2" AND title ~ "08/06"
```

#### 3단계: 문서 내용 분석 및 요약 제공
- 📋 주요 논의사항
- 🎯 주요 결정사항 및 배운점  
- 📊 진행 상황
- 🔄 다음 액션 아이템
- 💡 오늘 이어갈 내용

### 📝 요약 템플릿

```markdown
## 어제 ({날짜}) 업무 요약 📋

어제 컨플루언스에서 "{문서제목}"을 확인했습니다.

### 🎯 어제의 주요 내용
{주요 논의사항과 결정사항 요약}

### 🔄 오늘 이어갈 내용
{다음 액션 아이템과 계속할 작업들}

오늘은 어떤 부분부터 작업을 시작하시겠습니까?
```

### 🚫 예외 상황 처리

#### 어제 문서가 없는 경우
```markdown
어제({날짜}) 날짜의 업무 문서를 찾을 수 없습니다. 

가장 최근 문서들을 확인해보겠습니다:
- 최근 3일간의 문서 목록 제공
- 또는 새로운 작업 계획 수립 제안
```

#### 여러 문서가 있는 경우  
```markdown
어제({날짜}) 날짜로 여러 문서가 있습니다:
1. [문서1 제목]
2. [문서2 제목] 
3. [문서3 제목]

모든 문서를 요약해서 통합 정리해드리겠습니다.
```

## 🔧 구현 상세사항

### Confluence 검색 쿼리 최적화
```
기본 검색: space = "~63561b381cc605b1fd15aca2" AND title ~ "MM/DD"
확장 검색: space = "~63561b381cc605b1fd15aca2" AND title ~ "MM/DD" OR title ~ "[MM/DD]"
날짜 범위: modifiedTime >= "YYYY-MM-DD" AND modifiedTime < "YYYY-MM-DD+1"
```

### 사용자 설정 정보 활용
- **스페이스**: seonghonoh (~63561b381cc605b1fd15aca2)
- **폴더**: 업무일지
- **문서 제목 형식**: "[MM/DD] 제목" 또는 "MM/DD 제목"

### 스마트 날짜 처리
```javascript
// 한국 시간대 고려
const koreaTime = new Date().toLocaleString("en-US", {timeZone: "Asia/Seoul"});
const yesterday = new Date(koreaTime);
yesterday.setDate(yesterday.getDate() - 1);

// 주말/휴일 처리
if (yesterday.getDay() === 0) { // 일요일이면 금요일 문서 찾기
    yesterday.setDate(yesterday.getDate() - 2);
} else if (yesterday.getDay() === 6) { // 토요일이면 금요일 문서 찾기
    yesterday.setDate(yesterday.getDate() - 1);
}
```

## 🎯 사용 예시

### 사용자 입력
```
좋은 아침~ 어제 업무에 이어서 작업할게
```

### AI 응답 프로세스
1. "어제 업무에 이어서" 키워드 감지
2. 어제 날짜(08/06) 계산
3. 컨플루언스에서 "[08/06]" 포함 문서 검색
4. 발견된 문서들 내용 읽기
5. 구조화된 요약 제공
6. 오늘 작업 방향 제안

### 완성된 응답 형태
```markdown
좋은 아침입니다! 어제 업무를 이어가시는군요.

## 어제 (08/06) 업무 요약 📋

어제 컨플루언스에서 "[08/06] 쿠버네티스 멀티 클러스터 관리 및 복잡성 논의"를 확인했습니다.

### 🎯 어제의 주요 내용
- 쿠버네티스 복잡성 관리와 스케일링 한계 논의
- ArgoCD + ApplicationSets를 통한 멀티 클러스터 관리 방안
- kubectx/kubens 도구 검토 및 정책 결정 필요성

### 🔄 오늘 이어갈 내용
- G4 수거배송조회 메뉴 확인 (최우선)
- 버전 관리 자동화 검토
- AI 에이전트 토론 시스템 설계

오늘은 G4 수거배송조회 메뉴 확인부터 시작하시겠습니까?
```

## 🔄 지속적 개선사항

### 학습 기능
- 자주 사용하는 문서 패턴 학습
- 사용자 선호 요약 스타일 적응
- 프로젝트별 연관성 파악

### 확장 기능
- 주간/월간 요약 자동 생성 연계
- 관련 아사나 태스크 자동 연결
- GitLab 이슈와의 매핑

---

**사용 환경**: macOS M4, 개발 도구(asdf, terraform, AWS), 협업 도구(asana, gitlab, confluence)  
**문서 위치**: purpleio.atlassian.net > seonghonoh 스페이스 > 업무일지 폴더