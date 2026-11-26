# prompt-archive

개인 프롬프트/스킬/가이드 자산 아카이브.

## 재사용 프롬프트

- [`YOUTUBE_EXPLAINER_MOTION_PROMPT.md`](./YOUTUBE_EXPLAINER_MOTION_PROMPT.md) — 1~3초 유튜브 설명 모션(Remotion) 제작·검수 계약
- [`DAILY_ARCHIVE_CARD_PROMPT.md`](./DAILY_ARCHIVE_CARD_PROMPT.md) — 데일리 아카이브 카드 그림·조판·검수 계약

## 공용 스킬

스킬 원본은 [`skills/`](skills/), 설치 범위와 연결 목록은 [`skills/catalog.json`](skills/catalog.json)이 소유합니다. OpenClaw 공용·워크스페이스·Codex native 폴더의 스킬을 여기서 관리하고, 각 실행 경로에는 링크를 둡니다. 공용·역할별 원본은 `skills/<스킬명>/`으로 모으고 설치 범위는 카탈로그로 구분합니다. native 스킬도 같은 위치에서 관리하며, 내용이 다른 동명 변형만 `frontend-design-main`처럼 폴더 이름으로 구분합니다.

[설치·Windows 연결·갱신·복구 안내](skills/README.md)를 먼저 읽으세요. Python 3.10+가 필요하며 기본 실행은 미리보기입니다.

```bash
git clone https://github.com/shdkej/prompt-archive ~/workspace/prompt-archive
cd ~/workspace/prompt-archive
bash scripts/setup.sh --targets openclaw,codex
bash scripts/setup.sh --targets openclaw,codex --apply
bash scripts/setup.sh --targets openclaw,codex --check
```

Windows Codex는 `py -3 scripts/setup_skills.py --targets codex --apply` 또는 `scripts/setup.ps1`을 사용합니다. Claude 연결은 `--targets claude`로 선택합니다. 기존 파일이 있으면 비교 후 백업을 만드는 `--replace`를 명시합니다.

## 검증과 한계

```bash
python3 -m unittest discover -s scripts -p 'test_setup_skills.py' -v
bash -n scripts/setup.sh
```

설치기는 기존 설정과 원본 백업, 링크 대상, 반복 실행을 검증합니다. API 키·대화 DB·개발 캐시는 공유하지 않습니다. 각 스킬의 외부 도구·인증·OS 의존성은 해당 PC에서 별도로 준비해야 하며, Git 갱신과 스킬 연결만으로 모든 실행 환경이 같아지지는 않습니다.
