# agent-wiki GitHub Pages 배포 구조 설계

- 작성일: 2026-04-21
- Intent: build-01
- 작성자: Heartbeat Sub-Agent
- 권한 레벨: L0 (설계 문서 작성)

---

## 현황 분석

### agent-wiki 레포 구조

- **레포**: `shdkej/agent-wiki` (GitHub)
- **로컬 경로**: `~/workspace/agent-wiki/`
- **주요 디렉토리**: `diary/YYYY-MM-DD.md` 형태의 일별 마크다운 파일
- **자동 동기화**: `diary-sync.sh`가 30분 주기로 오늘 날짜 diary를 갱신하고 `main` 브랜치에 push
- **파일 보존 정책**: 7일 이상 경과한 diary 파일은 자동 삭제됨
- **파일 포맷**: YAML 프론트매터(`date`, `type`, `last_sync`) + 마크다운 본문

```
agent-wiki/
├── index.html          ← Docsify 엔트리포인트 (wiki-02/03에서 추가됨)
├── _sidebar.md         ← Docsify 탐색 구조
├── .nojekyll           ← Jekyll 비활성화 (Docsify 필수)
└── diary/
    ├── 2026-04-15.md
    ├── 2026-04-16.md
    └── ...  (최근 7일치)
```

### 기존 GitHub Pages 현황 — 이미 배포 완료

**중요**: 이 Intent(build-01)보다 먼저 실행된 `wiki-01` → `wiki-02` → `wiki-03` Intent 체인을 통해 **GitHub Pages가 이미 구현 완료**됨.

| 항목 | 현황 |
|------|------|
| 배포 URL | `https://shdkej.github.io/agent-wiki/` |
| 렌더링 방식 | Docsify (빌드 없이 런타임 마크다운 렌더링) |
| 배포 브랜치 | `main` 브랜치 루트(`/`) |
| 자동화 | diary-sync.sh → main push → 즉시 반영 (GitHub Actions 불필요) |
| 모바일 지원 | 사이드바 토글 버튼 + 오버레이 (wiki-03에서 개선) |
| 마지막 확인 커밋 | `d52641c` (2026-04-20) |

**구현 이력**:
- `wiki-01` (2026-04-18): 3가지 옵션 분석, Docsify + 직접 Pages 권장안 설계
- `wiki-02` (2026-04-19): Docsify 파일(`index.html`, `_sidebar.md`, `.nojekyll`) 추가, Pages 활성화. 200 OK 확인
- `wiki-03` (2026-04-20): 모바일 사이드바 UI 개선, 최종 배포 확인

### 기존 shdkej.github.io 현황

- **레포**: `shdkej/shdkej.github.io` (GitHub Pages 사용자 페이지)
- **접근 URL**: `https://shdkej.github.io` (사용자 페이지)
- **상태**: 이미 활성화된 사이트. agent-wiki 페이지와 별도로 운영 중.

**GitHub Pages 계정 제약**:
- `username.github.io` 사용자 페이지는 계정당 1개만 허용 → `shdkej.github.io` 기 사용 중
- `shdkej.github.io/agent-wiki`는 프로젝트 페이지로 사용자 페이지와 독립적으로 운영 가능

---

## 옵션 비교

> **참고**: 아래 3개 옵션은 wiki-01 설계 당시의 검토 내용. 현재는 옵션 A(Docsify 변형)로 이미 구현 완료됨.

### 옵션 A: agent-wiki 레포에 직접 GitHub Pages 활성화 — 현재 채택

**상태**: 구현 완료 (Docsify 방식으로)

**접근 URL**: `https://shdkej.github.io/agent-wiki`

**선택 이유**:
- Docsify는 빌드 단계 없이 브라우저에서 직접 마크다운을 렌더링 → GitHub Actions 불필요
- diary-sync.sh가 main에 push → 즉시 반영 (파이프라인 추가 없음)
- Jekyll, Hugo 등 정적 사이트 생성기 대비 설정 최소화

**핵심 파일 구성** (wiki-02 Lesson):
```
index.html    ← Docsify 로더 (loadSidebar, search, auto2top)
_sidebar.md   ← 탐색 트리 (수동 관리)
.nojekyll     ← Jekyll 비활성화 필수 (없으면 _sidebar.md 배제로 Docsify 깨짐)
```

**장점**:
- `shdkej.github.io` 레포를 건드리지 않아 독립적
- GitHub Actions 없이 실시간 반영
- 설정이 agent-wiki 레포 내에 자기 완결적

**단점/미해결 과제**:
- `_sidebar.md`는 수동 갱신 필요 (다이어리 최근 3개 항목 하드코딩)
- Obsidian `[[wiki-link]]` 문법이 Docsify에서 렌더링 안 됨
- 7일 파일 삭제 정책 시 sidebar 자동 갱신 안 됨

---

### 옵션 B: shdkej.github.io에 agent-wiki 섹션 추가 — 비채택

**비채택 근거**:
- 크로스 레포 push(L2) + PAT 관리 복잡도
- `shdkej.github.io` 레포 구조 수정 필요
- 기존 사이트 빌드 파이프라인과 결합 위험
- 옵션 A가 이미 독립적으로 잘 작동하므로 불필요

---

### 옵션 C: 대안 호스팅 — 비채택

**비채택 근거**:
- Reuse Before Create 원칙 위반 (기존 GitHub Pages 자산으로 해결됨)
- 외부 서비스 의존성 추가
- 유료 서비스(Obsidian Publish 등)는 비용 발생

---

## 추천 방안

### 선택한 옵션과 근거

**현재 구현(옵션 A - Docsify)을 유지하되, 미해결 과제 개선에 집중**

현재 `https://shdkej.github.io/agent-wiki/`는 정상 운영 중. 추가 옵션 검토보다 기존 구현의 자동화 완성도를 높이는 것이 우선.

---

### 구현 작업 순서

#### 현재 완료 상태 요약

- [x] `index.html` (Docsify 엔트리포인트) 추가
- [x] `_sidebar.md` (탐색 구조) 추가
- [x] `.nojekyll` (Jekyll 비활성화) 추가
- [x] GitHub Pages 활성화 (`source.path: /`, main 브랜치)
- [x] 배포 URL 200 OK 확인
- [x] 모바일 사이드바 UI 개선

#### 다음 단계 개선안 (미해결 과제)

**개선 1. `_sidebar.md` 자동 갱신** (우선순위: 높음)

**문제**: 현재 sidebar의 "다이어리" 섹션은 최근 3개 항목 하드코딩. diary-sync.sh가 파일을 추가/삭제해도 sidebar는 갱신 안 됨.

**해결 방안**: diary-sync.sh 마지막에 sidebar 재생성 로직 추가:

```bash
# diary-sync.sh 끝 부분에 추가
generate_sidebar() {
  local diary_dir="$REPO/diary"
  local sidebar="$REPO/_sidebar.md"

  # 최근 7일 diary 파일을 날짜 역순으로 나열
  DIARY_ENTRIES=""
  for f in $(ls "$diary_dir"/*.md 2>/dev/null | sort -r | head -7); do
    fname=$(basename "$f" .md)
    DIARY_ENTRIES="${DIARY_ENTRIES}  - [${fname}](diary/${fname}.md)\n"
  done

  cat > "$sidebar" <<SIDEBAR
- [홈](/)
- **다이어리**
${DIARY_ENTRIES}
- **도구**
  - [소스](sources/)
  - [개념](mapped/)
SIDEBAR
  log "sidebar regenerated"
}

generate_sidebar
git add _sidebar.md
```

**작업**: diary-sync.sh 수정 + commit & push (L1 범위, prompt-archive 레포)
단, agent-wiki 레포의 `_sidebar.md`에도 반영이 필요하므로 diary-sync.sh의 push 로직에 포함됨.

---

**개선 2. Obsidian `[[wiki-link]]` 호환성** (우선순위: 중간)

**문제**: agent-wiki 내 일부 파일이 Obsidian `[[파일명]]` 문법 사용 → Docsify에서 링크가 깨짐.

**해결 방안**:

(a) Docsify 플러그인 추가 (`docsify-wikilink`):
```html
<!-- index.html에 추가 -->
<script src="//unpkg.com/docsify-wikilink@latest/dist/docsify-wikilink.min.js"></script>
```

(b) diary-sync.sh의 Claude 프롬프트에 "Obsidian 링크를 마크다운 링크로 변환" 지시 추가

**권장**: (a) 플러그인 추가가 더 간단. `index.html` 수정 → agent-wiki 레포 push (L2)

---

**개선 3. 7일 삭제 정책 연동** (우선순위: 낮음)

**문제**: diary-sync.sh가 7일 이전 파일을 `git rm`할 때 `_sidebar.md`도 자동 갱신하지 않아 사이드바에 삭제된 링크가 남을 수 있음.

**해결 방안**: 개선 1의 `generate_sidebar()` 함수가 현재 존재하는 파일만 나열하므로, 삭제 후 자동으로 해결됨. 즉, 개선 1 구현 시 이 문제도 함께 해결.

---

### GitHub Actions 자동화 방안

**현재 구성**: GitHub Actions 불필요 (Docsify가 런타임 렌더링)

**장점**: GitHub 무료 플랜 Actions 분 소비 없음, 빌드 지연 없음

**선택적 추가 고려 사항**:

향후 사이드바 자동화를 diary-sync.sh 외부(서버리스)로 처리하고 싶다면:

```yaml
# .github/workflows/sidebar.yml (참고용, 현재 불필요)
name: Auto-update sidebar

on:
  push:
    branches: [main]
    paths: ['diary/**']

jobs:
  update-sidebar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate sidebar
        run: |
          echo "- [홈](/)" > _sidebar.md
          echo "- **다이어리**" >> _sidebar.md
          for f in $(ls diary/*.md | sort -r | head 7); do
            date=$(basename $f .md)
            echo "  - [$date](diary/$date.md)" >> _sidebar.md
          done
      - name: Commit
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Action"
          git add _sidebar.md
          git diff --cached --quiet || git commit -m "sidebar: auto-update"
          git push
```

단, 현재는 diary-sync.sh 내에서 처리하는 방식이 더 단순하므로 이 워크플로는 대안으로만 보존.

---

## 제약 및 주의사항

### 기술적 제약

1. **Docsify + `.nojekyll` 필수 조합**: `.nojekyll` 없으면 Jekyll이 `_sidebar.md`를 언더스코어 파일로 인식해 배제 + `.md` → `.html` 변환으로 Docsify가 완전히 깨짐 (wiki-02 Lesson)

2. **Pages source 변경과 push 타이밍**: Pages source 경로 변경과 소스 push가 동시에 발생하면 과도기 빌드 1회 실패 가능. `gh api -X POST /repos/{owner}/{repo}/pages/builds`로 재트리거 가능 (wiki-02 Lesson)

3. **사용자 도메인 영향**: `shdkej.com` 등 사용자 레벨 custom domain 설정 시 project Pages의 URL이 그 하위 경로로 변경될 수 있음

4. **Heartbeat 환경 제약**: prompt-archive 레포 외 레포에 Heartbeat 에이전트가 직접 push 불가 (wiki-03 Lesson → OPERATING_LESSONS 기록 예정)

### 프라이버시 고려사항

- diary 파일에는 개인 세션 정보, YouTube/Netflix 시청 기록이 포함됨
- `https://shdkej.github.io/agent-wiki/diary/`는 공개 URL
- 현재 `shdkej/agent-wiki` 레포가 Public이면 diary 내용이 전체 공개됨
- 민감 정보 필터링이 필요하다면 diary-sync.sh의 Claude 프롬프트에 "개인 정보 제거" 지시 추가 고려

### 비용

- GitHub 무료 플랜: Public 레포 GitHub Pages 무료
- GitHub Actions: Docsify 방식은 Actions 빌드 불필요 → 분 소비 없음

---

## 다음 단계 (L2 승인 필요 사항)

현재 GitHub Pages는 정상 운영 중. 추가 개선을 위해 다음 L2 액션이 필요할 수 있음:

| 순서 | 액션 | 대상 | 영향 | 우선순위 |
|------|------|------|------|---------|
| 1 | diary-sync.sh에 `generate_sidebar()` 추가 | prompt-archive 레포 (L1) | sidebar 자동화 | 높음 |
| 2 | agent-wiki `index.html`에 wikilink 플러그인 추가 | shdkej/agent-wiki (L2) | Obsidian 링크 호환 | 중간 |

**선행 확인 필요**:
- [ ] 현재 `https://shdkej.github.io/agent-wiki/` 접근 가능 여부 재확인 (d52641c 커밋 기준)
- [ ] `shdkej/agent-wiki` 레포 Public/Private 여부 → 프라이버시 결정에 영향
- [ ] `_sidebar.md` 현재 상태 확인 (수동 갱신이 최근에 이루어졌는지)

---

## 아키텍처 요약 (현재 상태)

```
[로컬 macOS - 30분마다]
diary-sync.sh
  ├── Claude로 diary 정제
  ├── agent-wiki/diary/YYYY-MM-DD.md 갱신
  ├── 7일 이전 파일 git rm
  └── git push origin main
              │
              ▼
[GitHub - shdkej/agent-wiki - main 브랜치]
  ├── index.html        (Docsify 로더)
  ├── _sidebar.md       (탐색 구조, 수동 갱신)
  ├── .nojekyll         (Jekyll 비활성화)
  └── diary/
      └── YYYY-MM-DD.md (최근 7일치)
              │
              ▼
[GitHub Pages - 정적 서빙]
https://shdkej.github.io/agent-wiki/
  ├── /           → index.html (Docsify UI)
  └── /diary/     → 마크다운 파일 → Docsify 런타임 렌더링
```

---

*이 문서는 Heartbeat Agent Sub-Agent가 build-01 Intent 실행 중 작성한 설계 문서입니다.*
*wiki-01/02/03 Intent의 선행 구현을 반영하여 현황 기반으로 작성되었습니다.*
*실제 추가 구현은 각 단계별 L1/L2 승인 후 진행합니다.*
