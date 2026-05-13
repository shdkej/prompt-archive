# agent-wiki GitHub Pages 배포 구조 설계

> 작성일: 2026-04-21 | Intent: wiki-01
> agent-wiki 콘텐츠를 공개 웹 뷰어로 제공하기 위한 배포 구조 및 작업 순서 제안.

---

## 현황 분석

- **현재 레포**: `shdkej/prompt-archive` (main 브랜치만 존재)
- **GitHub Pages 설정**: 현재 _config.yml 없음 → Pages 미설정 상태
- **agent-wiki 콘텐츠**: 현재 디렉토리 없음 → 신규 생성 필요
- **결론**: Pages 제약 없음. 가장 자유로운 방식 선택 가능.

---

## 옵션 비교

### 옵션 A: 기존 레포(prompt-archive)에 GitHub Pages 추가 ⭐ 권장

**방식**: `prompt-archive` 레포의 `main` 브랜치 또는 별도 `gh-pages` 브랜치에서 Pages 활성화

**구조**:
```
prompt-archive/
├── agent-wiki/          ← 마크다운 문서 모음
│   ├── index.md
│   ├── heartbeat.md
│   ├── workflow-master.md
│   └── ...
├── _config.yml          ← Jekyll 설정 (또는 없이 기본 Pages 사용)
└── docs/                ← Pages 루트 디렉토리로 지정 가능
```

**Pages 설정 경로**:
- GitHub → Settings → Pages → Source: `main` 브랜치, `/docs` 폴더 또는 루트

**장점**:
- 가장 단순. 레포 추가 없음.
- 마크다운 파일이 그대로 웹 페이지로 렌더링.
- GitHub Pages 기본 Jekyll 테마 적용 가능 (추가 설정 최소).

**단점**:
- prompt-archive 레포가 wiki용이 아닌 혼합 용도가 됨.
- URL: `https://shdkej.github.io/prompt-archive/agent-wiki/`

---

### 옵션 B: 새 레포 `agent-wiki` 생성

**방식**: `shdkej/agent-wiki` 전용 레포 생성 → main 브랜치에서 Pages 활성화

**장점**:
- 깔끔한 분리. URL도 단순: `https://shdkej.github.io/agent-wiki/`
- wiki만을 위한 레포 → 유지보수 명확

**단점**:
- 레포 생성 필요 (L2 수준 작업 없음, GitHub UI에서 직접 가능)
- prompt-archive와 내용 동기화 필요 시 이중 관리

---

### 옵션 C: `gh-pages` 브랜치 방식

**방식**: 빌드 자동화(GitHub Actions)로 main 브랜치 마크다운을 gh-pages 브랜치로 배포

**장점**: CI/CD 파이프라인 통합, 고급 빌드 가능 (Docusaurus, MkDocs 등)

**단점**:
- 초기 설정 복잡성 높음
- 단순 마크다운 뷰어 목적에 과한 구성

---

## 권장 배포 구조 (옵션 A - 기존 레포 활용)

### 디렉토리 구조

```
prompt-archive/
├── agent-wiki/
│   ├── index.md              ← 목차 및 소개
│   ├── agents/
│   │   ├── heartbeat.md      ← Heartbeat Agent
│   │   ├── workflow-master.md
│   │   └── ...
│   ├── concepts/
│   │   ├── intent.md         ← Intent 설계
│   │   ├── permissions.md    ← 권한 모델
│   │   └── ...
│   └── guides/
│       ├── getting-started.md
│       └── ...
└── _config.yml               ← Jekyll 설정 (선택)
```

### _config.yml (최소 구성)

```yaml
title: Agent Wiki
theme: minima
baseurl: "/prompt-archive"
url: "https://shdkej.github.io"
```

---

## 작업 순서

### 1단계: 콘텐츠 준비 (L1 - 즉시 실행 가능)
1. `agent-wiki/` 디렉토리 생성
2. 기존 `infinity/workflows/`, `infinity/PERMISSIONS.md`, `INFINITY.md` 등에서 콘텐츠 추출
3. `agent-wiki/index.md` (목차) 작성
4. 핵심 에이전트 문서 3~5개 초안 작성

### 2단계: GitHub Pages 활성화 (L0/L2 혼합)
1. `_config.yml` 생성 → commit & push (L1)
2. GitHub → `shdkej/prompt-archive` → Settings → Pages 활성화 (사용자 직접 수행, L3에 해당)
   - Source: `main` 브랜치, `/(root)` 또는 `/docs` 선택
3. Pages 빌드 완료 확인 (보통 1~3분)

### 3단계: 검증 (L0)
- `https://shdkej.github.io/prompt-archive/agent-wiki/` 접속 확인
- 마크다운 링크 정상 렌더링 확인
- 모바일 가독성 확인

---

## 대안: 새 레포(`shdkej/agent-wiki`) 선호 시 작업 순서

1. GitHub에서 `agent-wiki` 레포 생성 (사용자 직접, L3)
2. `_config.yml` + 초기 콘텐츠 커밋 & 푸시
3. Settings → Pages → main 브랜치 활성화
4. URL: `https://shdkej.github.io/agent-wiki/`

---

## 결론 및 권장사항

**가장 현실적인 경로**: **옵션 A** (기존 `prompt-archive` 레포 활용)

- 즉시 시작 가능 (레포 생성 불필요)
- GitHub Pages 설정은 사용자가 UI에서 1회 클릭
- Heartbeat Agent가 콘텐츠 작성 및 커밋/푸시 자율 수행 가능 (L1)
- 추후 별도 레포로 분리가 필요하면 마이그레이션 용이

**Heartbeat가 자율 수행 가능한 작업**:
- `agent-wiki/` 디렉토리 및 마크다운 파일 작성 (L1)
- `_config.yml` 작성 및 커밋 (L1)

**사용자가 직접 해야 하는 작업**:
- GitHub Settings → Pages 활성화 (UI 작업, 1회성)
