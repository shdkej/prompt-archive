# prompt-archive

개인 프롬프트/스킬/가이드 자산 아카이브.

**목차**

- [콘텐츠 문서](#콘텐츠-문서)
- [작업 판단](#작업-판단)
- [브랜드와 제품 디자인](#브랜드와-제품-디자인)
- [운영과 개발](#운영과-개발)
- [공용 스킬](#공용-스킬)
- [검증과 한계](#검증과-한계)

## 콘텐츠 문서

| 작업 | 관리 문서 |
| --- | --- |
| 소재 고르기, 글·댓글·회고 쓰기, 말투 다듬기, 발행 전 검수 | [글쓰기](WRITING.md) |
| 첫 이미지 고르기, 회고 카드·유튜브 설명 모션 만들기 | [시각·영상](VISUAL_MEDIA.md) |

콘텐츠 기준이 바뀌면 해당 항목을 현재 적용할 문장으로 고친다. 날짜별 변경 경위는 Git 기록에서 확인한다.

## 작업 판단

도구 선택, 측정, 운영 판단에 쓰는 기준은 [작업 판단 기준](DECISIONS.md)에서 관리한다.

## 브랜드와 제품 디자인

| 작업 | 관리 문서 |
| --- | --- |
| 제품이 누구에게 어떤 약속을 하는지 정하기 | [브랜드](BRAND.md) |
| 화면의 인상과 상호작용 방향 정하기 | [디자인](DESIGN.md) |
| 색상·서체·컴포넌트 기준 적용하기 | [디자인 시스템](DESIGN_SYSTEM.md) |

## 운영과 개발

| 작업 | 관리 문서 |
| --- | --- |
| 에이전트 작업 시작과 운영 판단 | [LLM 시작 지침](LLM.md) · [운영 기준](OPERATING_REFERENCE.md) |
| Intent 접수·상태 확인 | [Infinity](INFINITY.md) |
| 로컬 Claude 출퇴근 회고 | [Daily Feedback System](DAILY_FEEDBACK_SYSTEM.md) |
| 구현 구조와 테스트 순서 결정 | [코드 아키텍처](TECH_SPEC.md) · [TDD](TDD.md) |

## 공용 스킬

스킬 원본은 [`skills/`](skills/), 설치 범위와 연결 목록은 [`skills/catalog.json`](skills/catalog.json)이 소유합니다. OpenClaw 공용·워크스페이스·Codex native 폴더의 스킬을 여기서 관리하고, 각 실행 경로에는 링크를 둡니다. 직접 제작 원본은 `skills/custom/`, 외부 원본은 `skills/external/`에 두고 설치 범위는 카탈로그로 구분합니다. native 스킬도 같은 위치에서 관리하며, 같은 스킬의 역할별 연결은 하나의 원본을 참조합니다.

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
