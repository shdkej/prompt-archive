# 공용 스킬

스킬 원본과 지원 파일은 이 저장소에서 Git으로 관리한다. 실행 도구에는 원본 폴더를 연결한다. 두 PC가 같은 커밋을 받으면 같은 스킬 파일을 읽는다. Git pull과 실제 스킬 인식은 별도로 확인한다.

## 위치와 범위

| 위치 | 역할 |
| --- | --- |
| `daily-news/`, `image-upload/`, `keyword-title/`, `workflow-master/` | 기존 공용 스킬. 기존 참조 경로 유지 |
| `shared/` | OpenClaw 공용 라이브러리에서 가져온 스킬·외부 패키지 |
| `agents/main/`, `agents/hj/` | 해당 OpenClaw 워크스페이스의 스킬. 공용 저장소에 두되 역할별 설치 범위 유지 |
| `native/<agent>/` | 에이전트의 Codex native 스킬. 기존 agent home 연결 유지 |
| `archive/` | 같은 이름의 우선순위 낮은 Workshop 변형. 보관만 하고 설치하지 않음 |
| `catalog.json` | 패키지 원본, 기존 OpenClaw 경로, Codex/Claude 프로필, 외부 출처의 설치 목록 |

`deep-research`의 main·genie 연결은 같은 원본을 사용한다. 마케팅 에이전트의 53개 연결도 `shared/marketingskills/skills`를 함께 참조한다. 서로 다른 `frontend-design` 변형은 합치지 않고 공용·main native 범위를 유지한다.

OpenClaw 번들·플러그인 패키지의 스킬, Codex `.system`, 설치 캐시, 폐기된 Workshop 제안 이력은 각 도구가 관리한다. 이 저장소의 스킬로 복제하지 않는다. 활성 Workshop 파일은 해당 워크스페이스 스킬로 승격했다. Workshop은 루트 밖 링크를 허용하지 않으므로 그 경로에 외부 링크를 만들지 않는다. Workshop 자동 학습 설정은 변경하지 않았다.

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

Codex·Claude의 기본 프로필은 `shared`다. 특정 역할 스킬까지 쓰려면 `--profile main`, `--profile hj`, `--profile design`, `--profile genie`, `--profile marketing`을 지정한다. 같은 이름은 선택한 역할의 변형을 연결한다. 프로필 전환 시 기존 연결이 다르면 백업을 동반한 `--replace`가 필요하며, 이전 프로필만의 링크는 자동 삭제하지 않는다. OpenClaw와 같은 사용자 홈에서 역할 프로필을 전역 설치하면 OpenClaw의 개인 스킬 검색에도 보일 수 있으므로, 이 서버는 `shared`만 전역 연결한다.

OpenClaw는 기존 `openclaw.json`의 다른 값을 보존하면서 `skills.load.extraDirs`에 `skills/shared`, `allowSymlinkTargets`에 이 저장소의 `skills`만 추가한다. 기존 워크스페이스와 native 경로는 `catalog.json`에 따라 연결한다. 역할별 연결은 해당 에이전트가 `agents.entries`에 등록된 경우에만 만든다. 현재 기본 워크스페이스 배치용 목록이며 사용자 지정 워크스페이스로 바꿀 때는 목록도 확인한다. `OPENCLAW_STATE_DIR` 또는 `--openclaw-dir`로 별도 state 위치를 선택할 수 있다. 설정 파일은 JSON 형식을 사용하며 JSON5를 자동 변환하지 않는다.

Claude는 `--targets claude`로 선택한다. 기존 가이드 연결도 유지한다. Windows에서 Claude의 단일 파일 링크는 OS의 심볼릭 링크 권한이 추가로 필요할 수 있다. Codex 기본 설치는 디렉터리 junction만 사용한다.

## 두 PC의 갱신

1. 변경은 이 저장소 원본에서 한다. 미반영 변경을 확인하고 요청 변경만 검증·commit/push한다.
2. 다른 PC는 작업 시작 전 `git status --short`로 미반영 변경을 확인한다. 있으면 먼저 보존·통합하고 진행한다.
3. `git pull --ff-only` 후 설치 미리보기·적용·`--check`를 실행한다. 자동 reset, 강제 덮어쓰기, 작업 도중 갱신을 하지 않는다.
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

## 외부 패키지 갱신

`shared/marketingskills`는 원래 저장소의 전체 소스와 MIT 라이선스를 보존한 스냅샷이다. 출처와 커밋은 `catalog.json`에 있다. `.git`·의존성·캐시는 제외했다. gstack은 설치된 OpenClaw 전용 생성 스킬과 라이선스를 보존하며, 별도 `~/.gstack` 런타임은 그대로 필요하다. gstack의 OpenClaw 전용 진입점은 Codex 기본 목록에 등록하지 않는다.

외부 설치기·ClawHub·gstack 업그레이드는 기존 연결을 실파일로 바꿀 수 있다. 갱신은 별도 위치에서 검토하고 라이선스·지원 파일을 포함해 공용 원본을 갱신한 뒤 다시 `--check`한다. 공용 폴더와 에이전트별 변형을 이름만 보고 합치지 않는다.
