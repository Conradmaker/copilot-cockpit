---
name: writing-readme
description: "README writing and review workflow for creating, updating, expanding, and auditing README files with audience-aware structure, project-type selection, template choice, and source-of-truth verification. Use this skill when writing a new README, adding a section, refreshing stale project docs, checking whether a README still matches the repository, choosing sections by project type, or turning repo context into project-facing documentation. Always consult this skill for README tasks, even if the user only says 'document this repo', 'write project docs', 'update docs', or 'check our README'. For broader prose polish use writing-clearly-and-concisely. For browser screenshots or demo capture use agent-browser. Triggers on: README, readme, project documentation, document this repo, update README, review README, docs for project, 리드미, README 작성, README 업데이트, README 리뷰, 프로젝트 문서화, 저장소 문서, 프로젝트 소개 문서, 문서 최신화."
disable-model-invocation: false
user-invocable: false
---

# README 작성 가이드 (writing-readme)

## 목표

README를 대상 독자와 프로젝트 맥락에 맞는 첫 문서로 만든다. 이 스킬은 새 README 작성, 섹션 추가, 오래된 내용 갱신, 정확성 리뷰까지 한 흐름으로 다루며, 프로젝트 유형에 맞는 템플릿 선택과 실제 저장소 상태 검증까지 포함한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 README를 작성하거나 수정하기 전에는 아래 reference 문서를 직접 읽고, 현재 작업에 맞는 템플릿과 체크리스트를 먼저 고른 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 6대 핵심 원칙

### 1. 먼저 독자와 첫 질문을 고정한다

좋은 README는 모든 것을 설명하는 문서가 아니라, 해당 독자가 가장 먼저 확인할 질문에 답하는 문서다. 같은 저장소라도 오픈소스 사용자, 팀 동료, 미래의 나에게 필요한 정보는 다르다.

- README를 쓰기 전에 누가 읽는지부터 특정한다
- 독자가 첫 30초 안에 확인할 질문 3개를 적고 그 순서대로 구조를 잡는다
- README 언어와 톤은 프로젝트의 실제 독자와 배포 맥락에 맞춘다

#### 빠른 판단 기준

- 독자를 한 문장으로 설명할 수 없으면 바로 초안을 쓰지 않는다
- 제목과 한 줄 설명만 보고도 "이게 나와 무슨 상관인지" 드러나지 않으면 다시 쓴다
- README가 사용자용인지, 기여자용인지, 운영자용인지 섞여 있으면 우선순위를 다시 나눈다

→ 상세: [references/01-readme-role-and-audience.md](references/01-readme-role-and-audience.md)

### 2. 작업 종류를 먼저 구분한다

README 작업은 새로 작성하기, 섹션 추가하기, 기존 내용 갱신하기, 정확성 리뷰하기로 나뉜다. 작업 종류를 섞으면 필요 이상으로 문서를 다시 쓰거나, 반대로 오래된 내용을 놓치기 쉽다.

- create, add, update, review 중 어떤 작업인지 먼저 고른다
- update와 review는 기존 README와 실제 저장소 상태를 대조하는 단계가 반드시 먼저 온다
- add 작업은 새 섹션을 넣을 위치와 독자를 함께 확인한다

#### 빠른 판단 기준

- 기존 README가 있는데 바로 새로 쓰려고 하면 update나 review가 아닌지 먼저 확인한다
- 바뀐 기능 하나만 설명하면 되는데 README 전체를 다시 쓰고 있으면 범위를 줄인다
- 정확성 확인 요청인데 실제 파일이나 설정을 안 본 상태라면 아직 초안을 쓰지 않는다

→ 상세: [references/02-task-types-and-project-fit.md](references/02-task-types-and-project-fit.md)

### 3. 프로젝트 유형에 맞는 템플릿을 먼저 고른다

오픈소스, 개인 프로젝트, 내부 서비스, 설정 디렉터리는 필요한 섹션과 문서 톤이 다르다. 범용 README를 억지로 맞추기보다 먼저 유형을 고르고 그에 맞는 템플릿을 출발점으로 삼는다.

- OSS, personal, internal, config 중 가장 가까운 유형을 고른다
- 템플릿은 시작점일 뿐이며, 불필요한 섹션은 삭제하고 필요한 섹션은 추가한다
- README 언어와 섹션 제목은 대상 독자에 맞춰 번역하거나 유지한다

#### 빠른 판단 기준

- 내부 서비스인데 License와 공개 기여 안내가 핵심처럼 보이면 템플릿이 잘못된 것이다
- 설정 디렉터리인데 파일 구조와 gotcha가 없다면 나중에 다시 읽을 때 가치가 떨어진다
- 오픈소스인데 설치와 사용 예제가 약하면 README의 핵심 역할을 못 한다

→ 상세: [references/02-task-types-and-project-fit.md](references/02-task-types-and-project-fit.md)
→ 템플릿: [templates/oss.md](templates/oss.md), [templates/personal.md](templates/personal.md), [templates/internal.md](templates/internal.md), [templates/xdg-config.md](templates/xdg-config.md)

### 4. README에는 가장 먼저 필요한 정보만 남긴다

README는 첫 진입 문서다. 모든 배경 설명과 세부 설계를 한곳에 몰아넣는 대신, 지금 이 저장소를 이해하고 시작하는 데 필요한 정보만 남기고 깊은 내용은 별도 문서로 연결한다.

- 모든 README에는 최소한 이름, 설명, 사용 시작점이 있어야 한다
- 자주 묻는 설정, 설치, 실행, 예제는 README에 남기고 긴 배경 설명은 분리한다
- 별도 문서가 있다면 README에서 링크를 통해 진입 경로를 명확히 준다

#### 빠른 판단 기준

- README를 보지 않고도 설치나 실행을 시작할 수 없다면 핵심 정보가 빠진 것이다
- 장문의 설계 설명 때문에 가장 기본적인 사용법이 아래로 밀리면 분리한다
- 링크만 있고 이 링크가 왜 필요한지 설명이 없으면 README의 탐색 품질이 떨어진다

→ 상세: [references/03-section-patterns.md](references/03-section-patterns.md)

### 5. 수정 전에 저장소의 실제 상태를 검증한다

README의 신뢰는 코드보다 느리게 깨진다. 그래서 update와 review 작업에서는 실제 엔트리포인트, 스크립트, 환경 변수, 폴더 구조를 먼저 확인하고 README와 대조해야 한다.

- 설치, 실행, 테스트 명령은 실제 저장소에서 확인된 것만 적는다
- package metadata, 스크립트, 예제 파일, env 문서, 디렉터리 구조를 source of truth로 본다
- 바뀐 기능이 README 어디에 반영돼야 하는지 섹션 단위로 찾고 고친다

#### 빠른 판단 기준

- README에 적힌 명령을 저장소 어디에서도 찾을 수 없으면 stale 문서로 본다
- 환경 변수 설명은 있는데 어디서 구하는지 없으면 온보딩 문서로서 불완전하다
- 리뷰 결과에 문제점만 있고 수정 제안이 없으면 작업이 반쯤 끝난 것이다

→ 상세: [references/04-update-and-review-workflow.md](references/04-update-and-review-workflow.md)

### 6. 읽는 순서를 기준으로 문장을 압축한다

사람은 README를 정독하기보다 스캔한다. 좋은 README는 제목, 한 줄 설명, 섹션 제목, 코드 블록만 훑어도 흐름이 잡히게 만든다.

- 한 줄 설명은 짧고 구체적으로 쓴다
- 표, 리스트, 짧은 단락, 작은 코드 예제로 정보 밀도를 높인다
- 유지보수 계획이 필요하면 last reviewed, project status, troubleshooting 같은 섹션을 의도적으로 둔다

#### 빠른 판단 기준

- 긴 문단이 연속으로 2개 이상 이어지면 표나 리스트로 바꿀 수 있는지 본다
- 코드 예제가 있는데 예상 입력이나 결과가 전혀 없으면 설명을 보완한다
- 유지보수 책임이 중요한 README인데 검토 시점이나 상태 표시가 전혀 없으면 추가를 검토한다

→ 상세: [references/05-style-and-maintenance.md](references/05-style-and-maintenance.md)
→ 상세: [references/06-oss-standards-and-examples.md](references/06-oss-standards-and-examples.md)

---

## references 가이드

아래 문서는 README 작업 전에 실제로 읽어야 하는 구현 가이드다. 현재 작업 종류에 맞는 reference를 먼저 고르고, 필요한 템플릿을 함께 연다.

| 파일 | 읽을 때 |
| --- | --- |
| [references/01-readme-role-and-audience.md](references/01-readme-role-and-audience.md) | README의 독자, 톤, 언어, 첫 질문을 정할 때 |
| [references/02-task-types-and-project-fit.md](references/02-task-types-and-project-fit.md) | create/add/update/review 작업을 구분하고 프로젝트 유형과 템플릿을 고를 때 |
| [references/03-section-patterns.md](references/03-section-patterns.md) | 어떤 섹션을 넣고, 무엇을 README 밖으로 뺄지 결정할 때 |
| [references/04-update-and-review-workflow.md](references/04-update-and-review-workflow.md) | 기존 README를 저장소 상태와 대조하고 stale 섹션을 찾을 때 |
| [references/05-style-and-maintenance.md](references/05-style-and-maintenance.md) | 문장 압축, 스캔 가능성, 유지보수성을 점검할 때 |
| [references/06-oss-standards-and-examples.md](references/06-oss-standards-and-examples.md) | 오픈소스 README의 필수 섹션, 표준 순서, 다국어 naming 규칙을 확인할 때 |

### 추천 로드 순서

- 새 README 작성: `01 → 02 → 03 → 템플릿`
- README 섹션 추가: `02 → 03 → 05`
- 오래된 README 갱신: `02 → 04 → 03 → 05`
- README 정확성 리뷰: `04 → 03 → 05`
- 오픈소스 README 정리: `01 → 02 → 06 → 템플릿`

---

## 범위

- 일반적인 문장 다듬기와 산문 품질 향상 → `writing-clearly-and-concisely`
- 브라우저 기반 데모 확인, 스크린샷 수집, UI 캡처 → `agent-browser`
- API 전용 레퍼런스 문서 작성 → `write-api-reference`
