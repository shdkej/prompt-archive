---
name: agent-browser
description: agent-browser CLI로 헤드리스 브라우저를 조작하는 명령어 레퍼런스. 사용 시기 - (1) 웹 페이지 탐색·클릭·폼 입력·스크린샷 등 브라우저 자동화가 필요할 때, (2) 렌더링된 페이지에서 구조화된 데이터를 추출할 때, (3) 로그인 세션 유지가 필요한 웹 작업, (4) 웹 UI 동작 확인/테스트. curl로 충분한 정적 페이지 요청에는 쓰지 않는다.
read_when:
  - 웹 상호작용 자동화
  - 페이지에서 구조화된 데이터 추출
  - 프로그래밍 방식으로 폼 채우기
  - 웹 UI 테스트
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","npm"]}}}
allowed-tools: Bash(agent-browser:*)
---

# agent-browser를 이용한 브라우저 자동화

## 설치

### npm 권장

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

### 소스에서 설치

```bash
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install
pnpm build
agent-browser install
```

## 빠른 시작

```bash
agent-browser open <url>        # 페이지로 이동
agent-browser snapshot -i       # ref가 포함된 상호작용 요소 가져오기
agent-browser click @e1         # ref로 요소 클릭
agent-browser fill @e2 "text"   # ref로 입력 채우기
agent-browser close             # 브라우저 닫기
```

## 핵심 워크플로우

1. 이동: `agent-browser open <url>`
2. 스냅샷: `agent-browser snapshot -i` (`@e1`, `@e2` 같은 ref가 포함된 요소를 반환)
3. 스냅샷에서 얻은 ref를 사용해 상호작용
4. 페이지 이동이나 상당한 DOM 변경 후에는 다시 스냅샷

## 명령어

### 내비게이션

```bash
agent-browser open <url>      # URL로 이동
agent-browser back            # 뒤로 가기
agent-browser forward         # 앞으로 가기
agent-browser reload          # 페이지 새로고침
agent-browser close           # 브라우저 닫기
```

### 스냅샷 (페이지 분석)

```bash
agent-browser snapshot            # 전체 접근성 트리
agent-browser snapshot -i         # 상호작용 요소만 (권장)
agent-browser snapshot -c         # 간결한 출력
agent-browser snapshot -d 3       # 깊이를 3으로 제한
agent-browser snapshot -s "#main" # CSS 선택자로 범위 지정
```

### 상호작용 (스냅샷에서 얻은 @ref 사용)

```bash
agent-browser click @e1           # 클릭
agent-browser dblclick @e1        # 더블 클릭
agent-browser focus @e1           # 요소 포커스
agent-browser fill @e2 "text"     # 지우고 입력
agent-browser type @e2 "text"     # 지우지 않고 입력
agent-browser press Enter         # 키 입력
agent-browser press Control+a     # 키 조합
agent-browser keydown Shift       # 키 누르고 있기
agent-browser keyup Shift         # 키 떼기
agent-browser hover @e1           # 호버
agent-browser check @e1           # 체크박스 체크
agent-browser uncheck @e1         # 체크박스 체크 해제
agent-browser select @e1 "value"  # 드롭다운 선택
agent-browser scroll down 500     # 페이지 스크롤
agent-browser scrollintoview @e1  # 요소를 화면에 보이도록 스크롤
agent-browser drag @e1 @e2        # 드래그 앤 드롭
agent-browser upload @e1 file.pdf # 파일 업로드
```

### 정보 가져오기

```bash
agent-browser get text @e1        # 요소 텍스트 가져오기
agent-browser get html @e1        # innerHTML 가져오기
agent-browser get value @e1       # 입력 값 가져오기
agent-browser get attr @e1 href   # 속성 가져오기
agent-browser get title           # 페이지 제목 가져오기
agent-browser get url             # 현재 URL 가져오기
agent-browser get count ".item"   # 일치하는 요소 개수 세기
agent-browser get box @e1         # 바운딩 박스 가져오기
```

### 상태 확인

```bash
agent-browser is visible @e1      # 보이는지 확인
agent-browser is enabled @e1      # 활성화되어 있는지 확인
agent-browser is checked @e1      # 체크되어 있는지 확인
```

### 스크린샷 및 PDF

```bash
agent-browser screenshot          # stdout으로 스크린샷
agent-browser screenshot path.png # 파일로 저장
agent-browser screenshot --full   # 전체 페이지
agent-browser pdf output.pdf      # PDF로 저장
```

### 동영상 녹화

```bash
agent-browser record start ./demo.webm    # 녹화 시작 (현재 URL + 상태 사용)
agent-browser click @e1                   # 동작 수행
agent-browser record stop                 # 중지하고 동영상 저장
agent-browser record restart ./take2.webm # 현재 녹화 중지 + 새 녹화 시작
```

녹화는 새로운 컨텍스트를 생성하지만 세션의 쿠키/스토리지는 유지합니다. URL을 제공하지 않으면 자동으로 현재 페이지로 돌아갑니다. 매끄러운 데모를 위해서는 먼저 탐색한 뒤 녹화를 시작하세요.

### 대기

```bash
agent-browser wait @e1                     # 요소 대기
agent-browser wait 2000                    # 밀리초 단위 대기
agent-browser wait --text "Success"        # 텍스트 대기
agent-browser wait --url "/dashboard"    # URL 패턴 대기
agent-browser wait --load networkidle      # 네트워크 유휴 상태 대기
agent-browser wait --fn "window.ready"     # JS 조건 대기
```

### 마우스 제어

```bash
agent-browser mouse move 100 200      # 마우스 이동
agent-browser mouse down left         # 버튼 누르기
agent-browser mouse up left           # 버튼 떼기
agent-browser mouse wheel 100         # 휠 스크롤
```

### 시맨틱 로케이터 (ref의 대안)

```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find first ".item" click
agent-browser find nth 2 "a" text
```

### 브라우저 설정

```bash
agent-browser set viewport 1920 1080      # 뷰포트 크기 설정
agent-browser set device "iPhone 14"      # 기기 에뮬레이트
agent-browser set geo 37.7749 -122.4194   # 위치 정보 설정
agent-browser set offline on              # 오프라인 모드 전환
agent-browser set headers '{"X-Key":"v"}' # 추가 HTTP 헤더
agent-browser set credentials user pass   # HTTP 기본 인증
agent-browser set media dark              # 색상 구성표 에뮬레이트
```

### 쿠키 및 스토리지

```bash
agent-browser cookies                     # 모든 쿠키 가져오기
agent-browser cookies set name value      # 쿠키 설정
agent-browser cookies clear               # 쿠키 지우기
agent-browser storage local               # 모든 localStorage 가져오기
agent-browser storage local key           # 특정 키 가져오기
agent-browser storage local set k v       # 값 설정
agent-browser storage local clear         # 전체 지우기
```

### 네트워크

```bash
agent-browser network route <url>              # 요청 가로채기
agent-browser network route <url> --abort      # 요청 차단
agent-browser network route <url> --body '{}'  # 응답 모킹
agent-browser network unroute [url]            # 라우트 제거
agent-browser network requests                 # 추적된 요청 보기
agent-browser network requests --filter api    # 요청 필터링
```

### 탭 및 윈도우

```bash
agent-browser tab                 # 탭 목록
agent-browser tab new [url]       # 새 탭
agent-browser tab 2               # 탭 전환
agent-browser tab close           # 탭 닫기
agent-browser window new          # 새 윈도우
```

### 프레임

```bash
agent-browser frame "#iframe"     # iframe으로 전환
agent-browser frame main          # 메인 프레임으로 복귀
```

### 다이얼로그

```bash
agent-browser dialog accept [text]  # 다이얼로그 수락
agent-browser dialog dismiss        # 다이얼로그 닫기
```

### JavaScript

```bash
agent-browser eval "document.title"   # JavaScript 실행
```

### 상태 관리

```bash
agent-browser state save auth.json    # 세션 상태 저장
agent-browser state load auth.json    # 저장된 상태 불러오기
```

## 예시: 폼 제출

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# 출력 예시: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # 결과 확인
```

## 예시: 저장된 상태로 인증

```bash
# 한 번 로그인
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "/dashboard"
agent-browser state save auth.json

# 이후 세션: 저장된 상태 불러오기
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## 세션 (병렬 브라우저)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

## JSON 출력 (파싱용)

기계가 읽을 수 있는 출력을 위해 `--json`을 추가하세요:

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## 디버깅

```bash
agent-browser open example.com --headed              # 브라우저 창 표시
agent-browser console                                # 콘솔 메시지 보기
agent-browser console --clear                        # 콘솔 지우기
agent-browser errors                                 # 페이지 오류 보기
agent-browser errors --clear                         # 오류 지우기
agent-browser highlight @e1                          # 요소 강조 표시
agent-browser trace start                            # 트레이스 기록 시작
agent-browser trace stop trace.zip                   # 중지하고 트레이스 저장
agent-browser record start ./debug.webm              # 현재 페이지에서 녹화
agent-browser record stop                            # 녹화 저장
agent-browser --cdp 9222 snapshot                    # CDP로 연결
```

## 문제 해결

- Linux ARM64에서 명령을 찾을 수 없으면 bin 폴더의 전체 경로를 사용하세요.
- 요소를 찾을 수 없으면 snapshot으로 올바른 ref를 찾으세요.
- 페이지가 로드되지 않으면 이동 후 wait 명령을 추가하세요.
- 디버깅을 위해 브라우저 창을 보려면 --headed를 사용하세요.

## 옵션

- --session <name> 은 격리된 세션을 사용합니다.
- --json 은 JSON 출력을 제공합니다.
- --full 은 전체 페이지 스크린샷을 찍습니다.
- --headed 는 브라우저 창을 표시합니다.
- --timeout 은 명령 타임아웃을 밀리초 단위로 설정합니다.
- --cdp <port> 는 Chrome DevTools Protocol로 연결합니다.

## 참고

- ref는 페이지 로드 단위로 안정적이지만 이동 시 변경됩니다.
- 새 ref를 얻으려면 이동 후 항상 스냅샷하세요.
- 입력 필드에서는 기존 텍스트가 지워지도록 type 대신 fill을 사용하세요.

## 이슈 보고

- 스킬 이슈: https://github.com/TheSethRose/Agent-Browser-CLI 에서 이슈를 등록하세요
- agent-browser CLI 이슈: https://github.com/vercel-labs/agent-browser 에서 이슈를 등록하세요
