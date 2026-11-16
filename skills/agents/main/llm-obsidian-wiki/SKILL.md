---
name: llm-obsidian-wiki
description: LLM이 지속 유지보수하는 Markdown/Obsidian 지식 Wiki(source/ → wiki/ 3레이어)를 다루는 스킬. 사용 시기 - (1) 지식 베이스 초기화 또는 원자료(기사·논문·독서 노트·인터뷰·회의록) 임포트, (2) 출처/엔티티/개념/종합/비교/질의 페이지와 index.md·log.md 갱신, (3) Wiki 기반 질문 답변과 장기 가치 답변 아카이브, (4) 감사 - 깨진 링크, 고아 페이지, 중복 개념, 낡은 결론, 인코딩 손상 점검.
---

# LLM Wiki

## Goal

축적 가능하고, 링크 가능하며, 발전 가능한 Markdown / Obsidian Wiki를 유지합니다. 자료를 임포트하거나 질문에 답할 때 단순히 요약을 생성하는 데 그치지 않습니다. 대신 새로운 지식을 기존 페이지에 편입합니다. 엔티티, 개념, 종합된 판단, 비교, 질의 아카이브를 갱신하여 Wiki가 계속 사용될수록 더 가치 있게 만듭니다.

## Default Three-Layer Structure

```text
source/          # Raw material layer: factual sources, read-only by default
wiki/            # Knowledge compilation layer: structured Wiki maintained by the LLM
schema/SKILL.md  # Convention layer: this skill / schema
```

### source/

- 원자료는 기본적으로 읽기 전용입니다. 본문 텍스트를 다시 쓰지 마세요.
- 원본 제목, 저자, URL, 날짜, 클리핑 메타데이터, 이미지 참조 등 출처 정보를 보존하세요.
- 원자료의 이름을 변경하거나 메타데이터를 보충해야 한다면 먼저 사용자에게 확인을 요청하세요.

### wiki/

기본 디렉터리 구조는 영어를 사용합니다:

```text
wiki/
  index.md      # Main index
  log.md        # Operation log
  README.md     # Wiki documentation
  sources/
  entities/
  concepts/
  syntheses/
  comparisons/
  queries/
```

규칙:

- `index.md`, `log.md`, `README.md`, `schema/SKILL.md`와 같이 합의된 관례 파일을 제외하고는, 디렉터리와 파일에 가능한 한 읽기 쉬운 영어 이름을 사용하세요.
- 용어성 고유명사는 적절할 경우 원어를 유지하거나 혼합 명명을 사용할 수 있습니다. 예를 들어 `AI Agent.md`, `OpenClaw.md`, `Claude Code.md`, `Harness Engineering.md` 등입니다.
- `concept/`와 `concepts/`, 또는 `entity/`와 `entities/`처럼 중복되는 병렬 디렉터리를 만들지 마세요. 과거에 만들어진 빈 중복 디렉터리를 발견하면 정리하세요. 내용이 들어 있다면 그 내용을 정규 디렉터리로 이전하고 링크를 갱신하세요.
- 파일 이름은 읽기 쉽고, 클릭 가능하며, 장기적으로 유지보수 가능해야 합니다. `source-*`, `concept-*`, `synthesis-*` 같은 기계식 접두어는 피하세요.

## Page Types

### Source Pages: `wiki/sources/`

출처 페이지는 단일 출처를 요약하고 위치를 파악하는 데 사용합니다. 출처 페이지에는 다음이 포함되어야 합니다:

- 출처 정보: 원본 파일, URL, 저자, 날짜.
- 한 문장 요약.
- 이 출처가 답하는 데 도움을 주는 질문.
- 핵심 구조 / 섹션 단서.
- 보존할 가치가 있는 지식 포인트.
- 관련 개념 / 엔티티 / 종합 페이지.
- 후속 정독 작업.

### Entity Pages: `wiki/entities/`

엔티티 페이지는 인물, 조직, 제품, 프로젝트, 도구 등의 대상에 사용합니다. 엔티티 페이지는 사실과 배경을 담으며, 지나치게 긴 논증을 담아서는 안 됩니다.

- 엔티티 페이지는 지식 대상에 대해서만 만드세요. 인물, 조직, 제품, 프로젝트, 도구 등은 그것들 자체가 분석 대상이거나 재사용 가능한 사실을 담을 때에만 엔티티 레이어에 들어가야 합니다. 단지 누군가가 어떤 출처의 저자라는 이유만으로 엔티티 페이지를 만들지 마세요. 엔티티 페이지에서 기사 저자 목록을 유지하지 마세요. 저자 정보는 출처 페이지의 출처 정보나 `source/` 메타데이터에 보관하세요.

### Concept Pages: `wiki/concepts/`

개념 페이지는 방법, 패턴, 이론, 문제 프레이밍, 프레임워크 등의 아이디어에 사용합니다. 동의어 중복을 피하기 위해 기존 개념 페이지를 재사용하고 갱신하는 것을 우선하세요.

### Synthesis Pages: `wiki/syntheses/`

종합 페이지는 출처 간 판단, 프레임워크, 주제 개관, 사례 매트릭스, 아키텍처 분석 등 편입된 지식에 사용합니다.

### Comparison Pages: `wiki/comparisons/`

비교 페이지는 개념, 제품, 패러다임, 솔루션을 비교하는 데 사용합니다. 예를 들어 `Reasoner vs Agent.md`입니다.

### Query Pages: `wiki/queries/`

장기적 가치가 있는 질의응답 결과물을 재사용 가능한 페이지로 아카이브합니다. 질의 페이지는 명확한 질문에 답하고 관련 출처, 개념, 종합 페이지로 다시 링크해야 합니다.

## Core Workflows

### Initialize the Wiki

1. `source/` 아래의 디렉터리, 파일 유형, 출처 그룹을 스캔합니다.
2. `wiki/index.md`, `wiki/log.md`, `wiki/README.md`를 생성하거나 갱신합니다.
3. 첫 번째 자료 묶음에 대한 출처 페이지를 생성합니다.
4. 엔티티, 개념, 종합, 비교 페이지를 추출합니다.
5. 인덱스와 로그를 갱신합니다.
6. 깨진 링크, 인코딩 손상, 중복 디렉터리, 빈 디렉터리를 점검합니다.

### Import Materials

1. 먼저 `wiki/index.md`를 읽어 기존 관련 페이지의 위치를 파악합니다.
2. 새 출처를 읽고 요약, 핵심 구조, 엔티티, 개념, 재사용 가능한 판단을 추출합니다.
3. 출처 페이지를 생성하거나 갱신합니다.
4. 기존 엔티티 페이지, 개념 페이지, 종합 페이지를 갱신합니다. 기존 페이지 갱신을 우선하고, 중복 개념을 함부로 만들지 마세요.
5. 관계를 표시합니다: supports, supplements, revises, contradicts, needs verification.
6. `wiki/index.md`와 `wiki/log.md`를 갱신합니다.
7. 깨진 링크 및 인코딩 손상 점검을 실행합니다.

### Answer Questions Based on the Wiki

1. 먼저 `wiki/index.md`를 읽습니다.
2. 그다음 관련 페이지를 읽습니다. 기본적으로 Wiki 전체를 스캔하지 마세요.
3. 답변에 Wiki 페이지 링크를 인용합니다.
4. 답변이 장기적 가치가 있다면 `wiki/queries/` 아래에 아카이브하거나 종합 페이지를 갱신합니다.
5. `wiki/log.md`를 갱신합니다.

## `index.md` Specification

`wiki/index.md`는 내비게이션 진입점입니다. 권장 구조:

```markdown
# Knowledge Wiki Index

## Quick Links

## Sources

## Entities

## Concepts

## Syntheses

## Comparisons

## Queries
```

각 레코드에는 가급적 다음을 포함하세요:

```markdown
- [[Knowledge/wiki/concepts/Context Engineering]] -- one-sentence description; status: evolving.
```

## `log.md` Specification

`wiki/log.md`는 단계 수준의 변경을 위한 날짜 기반 타임라인이며, 지나치게 세분화된 작업 장부가 아닙니다. 갱신 원칙:

- **날짜별로 병합**: 같은 날 수행한 임포트, 리팩터, 질의, 유지보수는 가능한 한 `## YYYY-MM-DD | Topic Overview` 아래로 병합하고, `###`로 주제별로 묶으세요.
- **단계 수준 결과 기록**: 핵심 출처, 새로 생성하거나 갱신한 핵심 페이지, 핵심 결론, 중요한 유지보수 결정을 보존하세요. 모든 작은 작업마다 별도 항목을 추가하지 마세요.
- **필요 시 별도 상세 페이지 생성**: 대량 매핑, 긴 감사 체크리스트, 이미지 이전 표, 복잡한 실험 로그 등의 세부 사항은 `wiki/maintenance/`, `wiki/queries/`, 또는 관련 종합 페이지 아래에 두세요. `log.md`는 요약으로만 링크해야 합니다.
- **하루에 여러 번 갱신할 때 같은 날 섹션을 다시 작성**: 단편적인 항목을 추가하기보다는 그날의 기존 섹션을 편집하고 병합하는 것을 우선하세요.
- **후속 방향 보존**: 끝부분에 짧은 "Current To-Dos / Follow-Up Directions" 목록을 유지할 수 있지만, 간결하게 유지하세요.

권장 형식:

```markdown
## YYYY-MM-DD | Topic Overview

### Topic One

- Import/update scope: ...
- Created/updated: [[Knowledge/wiki/...]], [[Knowledge/wiki/...]]
- Key conclusion: ...

### Topic Two

- ...

## Current To-Dos / Follow-Up Directions

- [ ] ...
```

일반적인 주제:

- 초기화 및 구조 조정.
- 주제 기반 출처 임포트.
- 개념 / 종합 페이지 심화.
- 질의 아카이브.
- 감사 및 유지보수.
- 스키마 / 스킬 규칙 갱신.

## Frontmatter Recommendations

출처 페이지:

```yaml
---
type: source
tags: [source-summary]
source_file: "[[Knowledge/source/...]]"
source_name:
author:
url:
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: initialized
---
```

엔티티 페이지:

```yaml
---
type: entity
tags: [entity]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

개념 페이지:

```yaml
---
type: concept
tags: [concept]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

종합 페이지:

```yaml
---
type: synthesis
tags: [synthesis]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

비교 페이지:

```yaml
---
type: comparison
tags: [comparison]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: evolving
---
```

질의 페이지:

```yaml
---
type: query
tags: [query]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: archived
---
```

## Link Rules

- Obsidian Wiki 링크를 사용하세요: `[[Knowledge/wiki/concepts/Context Engineering]]`.
- vault 파일에 링크할 때는 vault 루트 기준 상대 경로를 사용하세요. 절대 경로를 사용하지 마세요.
- 파일 이름을 변경한 후에는 모든 `[[...]]` 링크를 일괄 갱신하세요.
- 사용자에게 응답할 때는 가능한 한 클릭 가능한 Wiki 링크를 우선하세요.

## Encoding Safety Rules

영어 콘텐츠는 UTF-8로 작성해야 합니다. Windows / PowerShell 환경에서는 PowerShell here-string, `Add-Content`, `Set-Content`로 비ASCII 텍스트를 직접 쓰면 대체 문자(replacement character)나 기타 인코딩 손상이 발생할 수 있습니다.

다음을 우선하세요:

- `apply_patch`를 사용해 Markdown을 수정하기;
- 또는 `.py` 스크립트를 만들어 `Path.write_text(..., encoding="utf-8")`로 텍스트를 쓰기;
- 또는 Python `read_text(..., encoding="utf-8")`로 파일 내용을 검증하기.

다음을 피하세요:

- PowerShell 명령 문자열 내부에 큰 비ASCII 블록을 직접 쓰기;
- 터미널 표시 출력만으로 파일 손상 여부를 판단하기.

매번 일괄 쓰기 후 다음을 점검하세요:

- 반복되는 물음표;
- 유니코드 대체 문자;
- 전형적인 모지바케(mojibake) 표식;
- 깨진 링크.

## Images and Attachments

- 사용자가 요청하거나 이미지가 장기적 이해에 결정적이지 않은 한, 기본적으로 `source/`의 외부 이미지를 일괄 다운로드하지 마세요.
- 이미지를 로컬화해야 한다면 vault 첨부 위치로 다운로드하고 Markdown 이미지 구문을 Obsidian 이미지 임베드로 변환하세요: `![[image.png]]`.
- 원자료 레이어는 기본적으로 읽기 전용입니다. 이미지를 로컬화하거나 원자료를 다시 쓰기 전에 확인하세요.

## Safety Principles

- 사용자의 원자료를 덮어쓰지 마세요.
- 내용이 이전되었음을 확인했거나 사용자가 명시적으로 삭제를 요청하지 않은 한, 비어 있지 않은 디렉터리를 삭제하지 마세요.
- 대량 이동이나 이름 변경 전에 매핑을 만드세요. 실행 후 깨진 링크를 점검하세요.
- 디렉터리 명명, 보고서 보존 여부, `README.md`의 영어 이름 유지 여부 등 사용자의 명시적 선호는 이 스키마보다 우선합니다.
