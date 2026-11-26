# 공용 스킬

스킬 원본과 지원 파일은 이 저장소에서 Git으로 관리한다. 실행 도구에는 원본 폴더를 연결한다. 두 PC가 같은 커밋을 받으면 같은 스킬 파일을 읽는다. Git pull과 실제 스킬 인식은 별도로 확인한다.

## 위치와 범위

| 위치 | 역할 |
| --- | --- |
| `<스킬명>/` | 공용·역할별 스킬 원본을 같은 깊이에 보관. 실제 설치 범위는 `catalog.json`의 `scope`·`agent`로 구분 |
| `catalog.json` | 패키지 원본, 기존 OpenClaw 경로, Codex/Claude 프로필, 외부 출처의 설치 목록 |

마케팅 에이전트의 53개 연결은 `marketingskills/skills`를 함께 참조한다. 외부 패키지는 라이선스·지원 파일을 포함한 내부 구조를 보존한다. `frontend-design/`은 공용·main이 함께 사용하는 단일 원본이다. 공용 버전의 타이포·색·배치 기준과 main 버전의 계획·검토·UI 문구·접근성 지침을 통합했다. 사용자 요구와 기존 브랜드를 우선하며, 라이선스는 원문 그대로 유지한다. 카탈로그의 shared·main 항목은 같은 원본에 대한 설치 연결이며 별도 스킬이 아니다. `deep-research/`도 한 원본에 main·genie 연결을 유지한다.

2026-11-26 사용자 요청으로 기존 `shared/`와 `agents/main/`·`agents/hj/`의 원본을 `skills/<스킬명>/`으로 모았다. `archive/main-workshop/daily-review-closeout`의 유효한 절차는 [`daily-review-closeout/SKILL.md`](daily-review-closeout/SKILL.md)에 통합하고 보관본과 카탈로그 중복 항목은 제거했다. 본문 선발송·크레용 카드·Tomorrow Expectation의 명언 대체 등 현행 정본과 충돌하는 과거 지침은 채택하지 않았다. 과거 원문은 Git 이력에서 확인한다. 이어서 `native/`의 7개 원본도 같은 깊이로 옮기고 빈 `native/`를 제거했다. 기존 `codex-home/skills` 실행 경로와 역할별 범위는 유지한다.

OpenClaw 번들·플러그인 패키지의 스킬, Codex `.system`, 설치 캐시, 폐기된 Workshop 제안 이력은 각 도구가 관리한다. 이 저장소의 스킬로 복제하지 않는다. 활성 Workshop 파일은 해당 워크스페이스 스킬로 승격했다. Workshop은 루트 밖 링크를 허용하지 않으므로 그 경로에 외부 링크를 만들지 않는다. Workshop 자동 학습 설정은 변경하지 않았다.

## 새 스킬 설치·추가

새 사용자 스킬도 이 저장소를 원본으로 사용한다. 직접 만든 스킬과 GitHub·ClawHub 등에서 가져온 스킬에 같은 기준을 적용한다. 사용자가 별도 설치 위치를 지정하면 그 요청을 우선한다.

1. `catalog.json`과 기존 파일에서 같은 이름·출처가 있는지 확인한다. 기존 항목의 업데이트인지 새 설치인지 구분하고, 이름만 같은 다른 변형을 덮어쓰지 않는다.
2. 기본 원본 위치는 공용·역할 전용 모두 `skills/<스킬명>`이다. 역할 범위는 폴더가 아니라 카탈로그로 지정한다. 동명 스킬은 기존 내용과 비교해 통합 여부를 판단하고, 역할별 설치만을 이유로 원본을 복제하지 않는다. 원본 위치 통합을 설치 범위 확대로 해석하지 않는다.
3. 설치기의 목적지 옵션을 명시한다. Codex `skill-installer`의 GitHub 다운로드 스크립트는 `--dest <이-PC의-prompt-archive>/skills`를 지원한다. 자체 위치에만 설치하는 도구는 설치 결과를 검토한 뒤 필요한 지원 파일·라이선스·출처 버전과 함께 공용 원본으로 편입한다. 공개 가능한 소스만 Git에 넣으며 인증·사용자 데이터·실행 산출물은 로컬에 둔다.
4. `catalog.json`의 `packages`에 원본 `path`, 설치 `scope`, OpenClaw 연결 경로와 필요한 Codex/Claude 등록을 추가한다. `agent` 필드는 OpenClaw 역할 전용 연결에만 넣는다. 외부 패키지 출처와 고정 버전·커밋도 함께 기록한다. `codex` 목록은 Codex와 Claude 설치에 공통으로 사용한다.
5. `scripts/setup.sh` 또는 `scripts/setup.ps1`로 필요한 도구만 미리보기·적용·`--check`한다. 기존 파일은 비교·백업 후 연결하며, 에이전트의 `codex-home/skills`도 새 복사본 대신 원본 링크를 사용한다.
6. 대상 도구에서 새 스킬이 실제로 발견되는지 확인하고, 원본·목록·문서의 요청 변경만 main에 commit/push한다. 완료 보고에 원본 경로, 설치 범위, 발견 여부와 커밋을 남긴다. 다른 PC는 작업 시작 전에 같은 커밋을 받아 연결을 갱신한다.

공용 스킬 한 개의 목록 예시는 다음과 같다. `<스킬명>`은 실제 `SKILL.md`의 `name`과 맞춘다. 같은 스킬을 여러 역할에 연결할 때는 동일한 원본 `path`를 사용한다. `codex[].name`과 실행 경로의 마지막 이름도 원래 스킬 이름을 유지한다.

```json
{
  "path": "skills/<스킬명>",
  "scope": "shared",
  "openclaw": ["skills/<스킬명>"],
  "codex": [{"name": "<스킬명>", "path": "skills/<스킬명>"}]
}
```

이것은 에이전트의 설치 규칙이다. 외부 설치 명령을 자동으로 가로채거나 목적지를 강제로 바꾸는 기능은 아니다. 현재 설치기의 `--check`는 목록에 등록된 연결을 확인하므로, 목록 밖에 새로 생긴 파일까지 자동 탐지한다고 간주하지 않는다. 외부 설치·업데이트 후에는 실제 생성 경로도 확인한다. 도구가 관리하는 `.system`·번들·플러그인 내부 스킬은 위 예외를 유지한다.

## 설치

Python 3.10+와 Git이 필요하다. 스크립트는 저장소 위치를 자동으로 계산한다. 도구 바이너리, 브라우저, 인증, API 키는 설치하지 않는다.

Linux/WSL에서 먼저 미리보기한다.

```bash
bash scripts/setup.sh --targets openclaw,codex
bash scripts/setup.sh --targets openclaw,codex --apply
bash scripts/setup.sh --targets openclaw,codex --check
```

기존 실파일·다른 링크가 있으면 적용을 중단한다. 내용을 비교한 뒤 `--apply --replace`를 사용하면 원본을 백업하고 연결한다. `--apply`가 없으면 쓰지 않는다. 같은 설정으로 다시 적용하면 변경 0건이어야 한다.

Windows PowerShell에서 Codex용 공용 스킬을 연결한다.

```powershell
git clone https://github.com/shdkej/prompt-archive "$env:USERPROFILE\workspace\prompt-archive"
cd "$env:USERPROFILE\workspace\prompt-archive"
py -3 scripts/setup_skills.py --targets codex
py -3 scripts/setup_skills.py --targets codex --apply
py -3 scripts/setup_skills.py --targets codex --check
# PowerShell 스크립트 실행이 허용된 환경에서는 같은 인자를 전달할 수 있다.
.\scripts\setup.ps1 --targets codex --check
```

디렉터리는 Windows junction을 사용하므로 Developer Mode가 필요하지 않다. OS 실행 정책은 변경하지 않는다. WSL의 Codex를 쓰면 WSL 안에 clone하고 Bash 진입점을 사용한다. Windows와 WSL의 사용자 홈은 서로 다르다.

Codex·Claude의 기본 프로필은 `shared`다. 특정 역할 스킬까지 쓰려면 `--profile main`, `--profile hj`, `--profile design`, `--profile genie`, `--profile marketing`을 지정한다. 역할 프로필은 공용 스킬과 해당 역할의 스킬을 함께 연결한다. `frontend-design`은 어느 프로필에서도 같은 원본을 사용한다. 프로필 전환 시 기존 연결이 다르면 백업을 동반한 `--replace`가 필요하며, 이전 프로필만의 링크는 자동 삭제하지 않는다. OpenClaw와 같은 사용자 홈에서 역할 프로필을 전역 설치하면 OpenClaw의 개인 스킬 검색에도 보일 수 있으므로, 이 서버는 `shared`만 전역 연결한다.

OpenClaw는 기존 `openclaw.json`의 다른 값을 보존하면서 `skills.load.extraDirs`의 옛 원본 `prompt-archive/skills/shared` 항목을 `<openclaw-state>/skills`로 교체하고, `allowSymlinkTargets`에 이 저장소의 `skills`를 등록한다. 공용 검색은 카탈로그에 등록된 런타임 연결만 읽는다. 통합 원본 루트 `prompt-archive/skills`를 `extraDirs`에 넣으면 역할 전용 스킬까지 전역 노출되므로 등록하지 않는다. 기존 워크스페이스와 native 경로는 `catalog.json`에 따라 연결한다. 역할별 연결은 해당 에이전트가 `agents.entries`에 등록된 경우에만 만든다. 현재 기본 워크스페이스 배치용 목록이며 사용자 지정 워크스페이스로 바꿀 때는 목록도 확인한다. `OPENCLAW_STATE_DIR` 또는 `--openclaw-dir`로 별도 state 위치를 선택할 수 있다. 설정 파일은 JSON 형식을 사용하며 JSON5를 자동 변환하지 않는다.

Claude는 `--targets claude`로 선택한다. 기존 가이드 연결도 유지한다. Windows에서 Claude의 단일 파일 링크는 OS의 심볼릭 링크 권한이 추가로 필요할 수 있다. Codex 기본 설치는 디렉터리 junction만 사용한다.

## 두 PC의 갱신

1. 변경은 이 저장소 원본에서 한다. 미반영 변경을 확인하고 요청 변경만 검증·commit/push한다.
2. 다른 PC는 작업 시작 전 `git status --short`로 미반영 변경을 확인한다. 있으면 먼저 보존·통합하고 진행한다.
3. `git pull --ff-only` 후 설치 미리보기·적용·`--check`를 실행한다. 이번 경로 이전으로 기존 링크 대상이 달라진 PC에서는 미리보기의 충돌이 옛 원본 링크인지 확인한 뒤 `bash scripts/setup.sh --targets openclaw,codex --apply --replace`로 백업·재연결한다. Codex만 쓰는 PC는 `--targets codex`를 사용한다. 자동 reset, 강제 덮어쓰기, 작업 도중 갱신을 하지 않는다.
4. 같은 작업을 인계할 때 `git rev-parse HEAD`를 기록한다. 새 스킬이 도구 목록에 나타나는지도 확인한다. Codex가 변경을 반영하지 않으면 새 세션 또는 재시작으로 확인한다.

이 설치기는 Git pull·push나 예약 작업을 자동으로 실행하지 않는다. SAM-PC가 오프라인이면 갱신되지 않은 상태를 최신으로 보고하지 않는다.

## 이동·복구·검증

충돌 원본과 설정 백업은 `<openclaw-state>/backups/shared-skills/<UTC시각>/`에 보관한다. `receipt.json`에 기존 경로·원본 경로·백업 위치가 있으며 설정 백업은 비공개 권한으로 쓴다. 설치 도중 실패하면 교체한 링크와 원본을 되돌린다. 이후 수동 복구할 때는 현재 연결을 확인해 링크만 제거하고 해당 백업을 원래 경로로 돌린다. 설정은 나중 변경을 비교한 뒤 필요한 스킬 설정만 복원한다. 링크를 따라 원본 폴더를 재귀 삭제하지 않는다.

```bash
python3 -m unittest discover -s scripts -p 'test_setup_skills.py' -v
bash -n scripts/setup.sh
bash scripts/setup.sh --targets openclaw,codex --check
openclaw config validate --json
openclaw skills --agent main list --json
```

설치 검증은 링크·원본·설정·발견 여부를 검증한다. 개별 스킬의 외부 API 호출·배포·메시지 발송을 실행하지 않는다. 기존 스킬의 절대 경로와 OS별 실행 의존성은 원문에 남아 있다. 공유된다고 Windows 네이티브에서 모든 스크립트가 실행되는 것은 아니다. 새 스킬은 지원 파일을 상대 경로로 참조하고 PC별 작업 경로·인증은 로컬 설정으로 주입한다.

2026-11-26 이전 검증: 이동한 1,448개 파일을 기존 Git 원본과 대조해 `daily-review-closeout/SKILL.md` 외 내용이 동일함을 확인했다. 저장소 스크립트 테스트 15개, OpenClaw·Codex 연결 165개, 설정 유효성 검사를 통과했고 재적용은 변경 0건이었다. main에서 회고 스킬, hj에서 여행 스크레이퍼를 발견했으며 역할 스킬이 다른 에이전트의 공용 목록으로 확장되지 않음을 확인했다. 통합 회고 지침은 기존 날짜 수정·명언 검증·Slack 단일 전달 시나리오로 검토했다. 실제 회고 발송·캘린더 쓰기와 다른 PC 적용은 이 이전 검증에 포함하지 않았다.

native 추가 이전에서는 204개 파일의 내용·실행 권한과 카탈로그의 호출 이름·역할 범위가 그대로임을 확인했다. 설치 테스트 12개, 여섯 프로필의 경로 해석, native 실행 경로의 `SKILL.md` 이름 확인을 통과했다. 링크 8개만 재연결했고 전체 165개 연결 검사와 재적용 변경 0건을 확인했다. 개별 스킬 실행과 다른 PC 적용은 별도다.

frontend-design 통합 후에도 설치 테스트 12개와 전체 연결 검사를 통과했다. 여섯 프로필이 단일 원본을 참조하고 OpenClaw main에서 통합 스킬 한 개를 발견했다. 기존 브랜드의 작은 수정·새 주제의 디자인·모바일/감소 모션 개선 세 상황에 지침을 적용해 충돌·누락을 검토했다. 실제 웹 제작이나 렌더 품질 실험은 수행하지 않았다.

## 외부 패키지 갱신

### 디자인 지원 스킬

2026-11-18 아래 저장소의 고정 커밋에서 스킬을 가져왔다. Hallmark·OpenPencil은 각 프로젝트의 공식 스킬이며, Blender 묶음은 커뮤니티 프로젝트다. 원본 `SKILL.md`·지원 파일·MIT 라이선스를 보존했고, 정확한 커밋은 `catalog.json`의 `upstream`에 기록한다.

| 스킬 | 공용 원본 | 사용 경계 |
| --- | --- | --- |
| [Hallmark](https://github.com/Nutlope/hallmark/tree/04977e15f3dfd6ee4b74c887dac3eb52665d6c92/skills/hallmark) | [`hallmark/SKILL.md`](hallmark/SKILL.md) | 기존 디자인에서는 [DESIGN_SYSTEM.md의 Hallmark 라이트 프로필](../DESIGN_SYSTEM.md#hallmark-라이트-프로필)을 먼저 적용한다. `audit`·`study`의 보조 진단만 사용하며, 자동 테마·스탬프·훅 설치를 하지 않는다. 이미지 생성 API·렌더 브라우저 등 선택 기능의 실행 의존성은 별도다. |
| [OpenPencil](https://github.com/open-pencil/open-pencil/tree/367a2b95d34d505ecccb7e36a83d17e5ff972b5d/skills/open-pencil) | [`open-pencil/SKILL.md`](open-pencil/SKILL.md) | `.fig` 검사·변환 또는 실행 중인 에디터 조작에 사용한다. 스킬 설치는 앱·CLI·MCP 설치나 열린 문서 연결을 뜻하지 않는다. 실제 도구 스키마와 문서를 확인하고 변경 뒤 export로 검증한다. |
| [Blender Skills](https://github.com/EL4CTEO/blender-skills/tree/9e7e04a603c125a0d17447ab97112fa70a865067) | [`blender-skills/skills/blender-core/SKILL.md`](blender-skills/skills/blender-core/SKILL.md) | Blender 공식 배포물이 아닌 MIT 커뮤니티 스킬 묶음이다. 전체 소스를 보존하고 Codex에는 core·hardsurface-modeling·pbr-materials·export-pipelines·asset-qa·lighting-lookdev 6개만 등록한다. 원본은 Blender 5.2+/5.3을 대상으로 하므로 다른 버전에서는 API·엔진 enum을 확인해 작업 스크립트를 조정한다. |

Blender 검증 진입점은 `blender-skills/skills/blender-core/scripts/env_report.py`, `blender-asset-qa/scripts/qa_check.py`, `blender-asset-qa/scripts/review_shots.py`다. 뒤의 두 경로는 같은 `blender-skills/skills/` 아래에 있다. 먼저 환경을 확인하고 해당 `SKILL.md`를 읽는다. 스킬 연결 검증만으로 Blender 버전 호환성·모델 품질·렌더 성공을 확인했다고 보고하지 않는다. Headless CLI 사용에는 Blender MCP 데몬이 필요하지 않다.

Codex만 설치하려면 `bash scripts/setup.sh --targets codex --apply`와 `--targets codex --check`를 사용한다. 이 경우 OpenClaw 설정은 변경하지 않는다. OpenClaw에도 설치하려면 `--targets openclaw,codex`를 선택한다. 세 패키지는 기존 공용 검색 범위를 유지하도록 카탈로그에 OpenClaw 공용 연결도 등록되어 있다. 다음 Codex 턴 또는 새 세션에서 발견 여부를 확인한다. 캐시·실행 산출물·API 키는 이 원본에 넣지 않는다.

### 기존 외부 패키지

`marketingskills`는 원래 저장소의 전체 소스와 MIT 라이선스를 보존한 스냅샷이다. 출처와 커밋은 `catalog.json`에 있다. `.git`·의존성·캐시는 제외했다. gstack은 설치된 OpenClaw 전용 생성 스킬과 라이선스를 보존하며, 별도 `~/.gstack` 런타임은 그대로 필요하다. gstack의 OpenClaw 전용 진입점은 Codex 기본 목록에 등록하지 않는다.

외부 설치기·ClawHub·gstack 업그레이드는 기존 연결을 실파일로 바꿀 수 있다. 갱신은 별도 위치에서 검토하고 라이선스·지원 파일을 포함해 공용 원본을 갱신한 뒤 다시 `--check`한다. 카탈로그의 설치 범위와 기존 내용을 확인하고, 같은 이름만 보고 원본을 덮어쓰지 않는다.
