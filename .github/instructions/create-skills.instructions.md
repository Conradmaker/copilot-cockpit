---
description: "Guidelines for creating high-quality Agent Skills for GitHub Copilot"
applyTo: "**/.github/skills/**/SKILL.md, **/skills/**"
---

# Agent Skills 작성 가이드

GitHub Copilot용 Agent Skill을 portable하게 만들되, 이 저장소의 fe-/ds- 계열 스킬처럼 빠르게 판단 가능한 요약 가이드와 references 중심 구조로 작성하기 위한 규칙이다.

## 목표

좋은 스킬은 세 가지를 동시에 만족해야 한다.

- description만 읽어도 언제 이 스킬을 호출해야 하는지 분명하다.
- 본문은 빠른 판단용 요약 가이드 역할을 한다.
- 상세 근거와 구현 예시는 references, templates, scripts 같은 로컬 리소스로 위임한다.

스킬은 문서를 길게 복붙하는 저장소가 아니다. 모델이 적절한 순간에 스킬을 트리거하고, 필요한 로컬 근거를 먼저 읽은 뒤, 예측 가능한 결과를 내게 만드는 작업 단위다.

## 핵심 원칙

### 1. description이 자동 호출을 결정한다

Copilot은 discovery 단계에서 사실상 `name`과 `description`만 보고 스킬을 로드할지 판단한다. 그래서 "언제 써야 하는가"에 대한 정보는 본문이 아니라 description에 몰아넣는다.

본문에 `## When to Use This Skill` 섹션을 길게 두는 방식은 권장하지 않는다. 그 정보는 description에 있어야 실제 트리거 품질이 올라간다.

### 2. 본문은 빠른 판단용 요약 가이드다

SKILL.md 본문은 모든 세부사항을 담는 백과사전이 아니라, 모델이 지금 무엇을 만들고 어떤 순서로 판단해야 하는지 빠르게 잡게 하는 안내문이어야 한다.

이 저장소의 fe-/ds- 계열 스킬처럼 목표를 먼저 두고, 핵심 패턴과 빠른 판단 기준을 앞쪽에 배치하고, 상세 구현은 references로 넘기는 구조를 기본값으로 둔다.

### 3. retrieval-led reasoning을 기본값으로 둔다

스킬이 로컬 reference, example, template, script를 갖고 있다면 훈련 데이터 기반 추측보다 그 리소스를 먼저 읽도록 유도해야 한다.

가능하면 아래 맥락이 스킬 본문에 자연스럽게 드러나게 작성한다.

```markdown
Prefer retrieval-led reasoning over pre-training-led reasoning.
```

또는 한국어 중심 스킬이라면 다음처럼 풀어서 써도 된다.

```markdown
훈련 데이터 기반으로 추측하지 말고, 작업을 시작하기 전에 관련 reference 문서를 먼저 읽고 적용한다.
```

### 4. 상세 구현은 resources로 분리한다

세부 절차, 긴 예시, 버전별 문서, 스크립트 사용법은 `references/`, `templates/`, `scripts/`로 분리한다. 본문은 어디를 왜 읽어야 하는지만 안내한다.

### 5. 결과물은 portable하고 predictable해야 한다

스킬은 VS Code, Copilot CLI, Copilot coding agent에서 재사용될 수 있어야 한다. 특정 대화 문맥이 없어도 작동하도록 구조와 링크, 용어를 명확하게 유지한다.

## 작성 절차

skill-creator 방법론을 기준으로 아래 순서를 기본 작성 흐름으로 둔다.

### 1. 의도 파악

먼저 이 스킬이 무엇을 가능하게 해야 하는지 정의한다.

- 어떤 작업을 더 잘하게 만들 스킬인가
- 어떤 표현이나 상황에서 트리거되어야 하는가
- 결과물은 어떤 형태여야 하는가
- 평가 가능한 작업인가, 아니면 정성 판단이 필요한 작업인가

현재 대화 안에 이미 답이 있으면 먼저 그 맥락을 재사용한다. 이미 드러난 도구, 절차, 입력 형식, 수정 피드백이 있으면 다시 묻기 전에 그것부터 정리한다.

### 2. 조사와 범위 분리

스킬이 다루는 도메인과 다루지 않는 도메인을 나눈다.

- 같은 저장소 안에 이미 비슷한 스킬이 있으면 description과 범위 섹션에서 역할을 분리한다.
- 워크스페이스 skill surface를 materially 바꾸면 `.github/instructions/skill-index.instructions.md`의 category, trigger, path도 함께 갱신한다.
- 상세 규칙이 길어질수록 본문에 쌓지 말고 references로 내린다.
- 로컬 자료가 충분하면 그 자료를 우선 쓰고, 외부 링크는 보조 자료로만 둔다.

### 3. SKILL.md 초안 작성

frontmatter는 영문으로 작성한다. 본문은 한국어 중심으로 작성하되, 기술 키워드와 코드, 파일명, 명령어는 필요한 범위에서 영문을 유지한다.

### 4. 리소스 계층 정리

본문에서 바로 읽어야 하는 내용과, 필요할 때만 읽어도 되는 내용을 분리한다.

- 핵심 판단 기준은 SKILL.md 본문에 둔다.
- 상세 구현, 버전별 문서, 긴 워크플로우는 `references/`로 둔다.
- reference 포인터는 마크다운 링크를 쓰고, 짧은 링크 라벨만으로도 어떤 상세 레퍼런스 자료인지 드러나게 적는다.
- 반복 가능하고 결정적인 작업은 `scripts/`로 둔다.
- 수정 가능한 시작점은 `templates/`로 둔다.
- 결과물에 그대로 쓰는 정적 리소스는 `assets/`로 둔다.

### 5. 검증과 반복

초안을 만든 뒤에는 최소한 다음을 점검한다.

- description만 읽어도 언제 트리거해야 하는지 분명한가
- 본문만 읽어도 지금 어떤 판단을 먼저 해야 하는지 보이는가
- references 링크가 실제 작업 흐름과 연결되는가
- 길이가 길어져서 오히려 본문이 흐려지지 않았는가

객관적으로 평가 가능한 스킬이면 test prompt와 평가 루프를 추가해 반복 개선한다.

## 디렉터리 구조

스킬은 아래 위치 중 하나에 둔다.

| 위치                             | 범위            | 권장도      |
| -------------------------------- | --------------- | ----------- |
| `.github/skills/<skill-name>/`   | 프로젝트/저장소 | 기본 권장   |
| `.claude/skills/<skill-name>/`   | 프로젝트/저장소 | 레거시 호환 |
| `~/.github/skills/<skill-name>/` | 사용자 전역     | 개인 스킬용 |
| `~/.claude/skills/<skill-name>/` | 사용자 전역     | 레거시 호환 |

각 스킬은 최소한 `SKILL.md`를 포함하는 독립 디렉터리여야 한다.

```text
.github/skills/my-skill/
├── SKILL.md
├── LICENSE.txt
├── references/
├── scripts/
├── templates/
└── assets/
```

`LICENSE.txt`는 선택 사항이지만 공개 배포하거나 재사용 가능성을 염두에 둔다면 포함하는 편이 안전하다.

## Frontmatter 규칙

### 필수 예시

```yaml
---
name: webapp-testing
description: Toolkit for testing local web applications using Playwright. Use this skill when asked to verify frontend functionality, debug UI behavior, capture browser screenshots, check for visual regressions, or inspect browser console logs. Always consult this skill for local web testing tasks, even if the user only asks to "check the page" or "see what's wrong in the browser." Triggers on: Playwright, browser testing, screenshot, UI regression, console log, 웹 테스트, 브라우저 확인, 스크린샷.
license: Complete terms in LICENSE.txt
---
```

| 필드          | 필수 여부 | 규칙                                                             |
| ------------- | --------- | ---------------------------------------------------------------- |
| `name`        | 예        | 소문자와 하이픈 사용, 64자 이하                                  |
| `description` | 예        | 기능, 트리거 상황, 키워드를 함께 담는다. 1024자 이하를 권장한다. |
| `license`     | 아니오    | `LICENSE.txt` 참조 문구 또는 SPDX identifier                     |

### description 작성 규칙

description은 아래 순서로 작성하는 것을 기본값으로 둔다.

1. 이 스킬이 무엇을 하는지 한 문장으로 말한다.
2. 언제 이 스킬을 써야 하는지 구체적인 상황을 적는다.
3. 사용자가 명시적으로 말하지 않아도 개입해야 하는 문맥을 약간 pushy하게 적는다.
4. 겹치는 도메인이 있으면 어떤 스킬로 보내야 하는지 짧게 적는다.
5. 마지막에 `Triggers on:` 형식으로 영문과 한글 키워드를 함께 적는다.

description은 애매하면 안 된다. "도와주는 헬퍼", "유틸리티 모음" 같은 표현은 자동 호출에 거의 도움이 되지 않는다.

좋은 예시는 아래와 같다.

```yaml
description: Product UX principles for UX writing, CTA labels, loading, feedback, confirmation, destructive actions, share and selection flows, navigation, motion, inclusive design, and dark pattern prevention. Use this skill when designing or reviewing product-level user flows, button labels, error messages, empty states, loading states, confirmation dialogs, delete flows, share flows, selection flows, or navigation behavior. Always consult this skill for UX decisions that affect what users read, expect, choose, recover from, or trust, even if the user only asked for copy polish. For implementation-level accessibility use fe-a11y. Triggers on: UX writing, CTA copy, error message, empty state, loading UX, confirmation dialog, delete flow, 공유, 삭제, 버튼 문구, 제품 UX.
```

나쁜 예시는 아래와 같다.

```yaml
description: Helpers for product experience.
```

이 예시는 무엇을 하는지, 언제 써야 하는지, 어떤 키워드에 반응해야 하는지가 전혀 드러나지 않는다.

## 본문 구조 표준

이 저장소의 스킬 결과물과 일관성을 맞추려면 아래 구조를 기본값으로 둔다.

| 섹션 | 역할 | 권장도 |
| --- | --- | --- |
| `# 제목` | 사람이 바로 이해할 수 있는 짧은 제목 | 필수 |
| `## 목표` | 이 스킬이 만들어야 할 좋은 결과와 판단 기준 | 필수 |
| 도입 문단 | "빠른 판단용 요약 가이드"라는 성격과 references 사용 방식을 설명 | 강력 권장 |
| `## 핵심 패턴` 또는 `## 핵심 단계` | 3~7개의 주요 원칙 또는 단계 | 필수 |
| `#### 빠른 판단 기준` | 지금 적용할지 말지 빠르게 체크하는 항목 | 강력 권장 |
| `## 엣지케이스` | 버전 차이, 예외, 흔한 실패 패턴 | 선택 |
| `## references/ 가이드` | 어떤 파일을 언제 읽어야 하는지 연결 | references가 있으면 권장 |
| `## 응답 패턴` | 리뷰/UX/분석 스킬처럼 답변 형식까지 고정해야 할 때 | 선택 |
| `## 범위` | 다른 스킬과의 경계 명시 | 겹치는 도메인이 있으면 권장 |

본문 기본 뼈대는 아래와 같이 작성하면 된다.

```markdown
# 스킬 제목

## 목표

이 스킬이 무엇을 더 잘하게 만드는지 먼저 설명한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 작업을 시작하기 전에는 아래 reference 문서를 직접 읽고 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 패턴

### 1. 첫 번째 원칙

무엇을 해야 하는지보다 왜 이 원칙이 필요한지 먼저 설명한다.

#### 빠른 판단 기준

- 지금 바로 체크할 수 있는 기준을 둔다.
- 모호한 표현보다 예/아니오로 판단 가능한 문장을 쓴다.

실제 적용 전에는 [예시와 기준 문서](references/example.md)를 먼저 읽고 기준과 예시를 확인한 뒤 반영한다.

---

## references/ 가이드

| 파일                  | 언제 읽는가                     |
| --------------------- | ------------------------------- |
| references/example.md | 구현 전에 상세 예시를 확인할 때 |

## 범위

- 다른 스킬로 위임할 주제를 적는다.
```

기본적으로 `## When to Use This Skill`, `## Prerequisites`, `## Troubleshooting`를 모든 스킬의 표준 섹션처럼 복제하지 않는다. 정말 필요한 경우에만 좁은 범위의 소제목으로 추가한다.

## 리소스 설계와 retrieval 패턴

### Progressive loading 구조

스킬은 세 단계로 로드된다.

| 단계         | 로드되는 것                                        | 목적                       |
| ------------ | -------------------------------------------------- | -------------------------- |
| Discovery    | `name`, `description`                              | 스킬을 로드할지 결정       |
| Instructions | `SKILL.md` 본문                                    | 빠른 판단과 실행 방향 제공 |
| Resources    | `references/`, `scripts/`, `templates/`, `assets/` | 필요할 때만 추가 근거 제공 |

이 구조 때문에 discovery 정보는 짧고 강해야 하고, 본문은 압축되어 있어야 하며, 상세 자료는 리소스로 밀어 넣어야 한다.

### 리소스 종류

| 폴더          | 역할                           | 언제 쓰는가                          |
| ------------- | ------------------------------ | ------------------------------------ |
| `references/` | 모델이 읽고 판단하는 상세 문서 | 구현 규칙, 긴 가이드, 버전별 문서    |
| `scripts/`    | 실행 가능한 자동화             | 반복적이고 결정적인 작업             |
| `templates/`  | 수정 가능한 시작점             | 스캐폴드, 예제 프로젝트, 템플릿 코드 |
| `assets/`     | 결과물에 그대로 쓰는 정적 파일 | 로고, 이미지, 정적 문서 껍데기       |

판단 기준은 단순하다.

- 모델이 읽고 수정하거나 확장해야 하면 `templates/`다.
- 결과물에 그대로 복사되거나 삽입되면 `assets/`다.

### references 설계 규칙

- SKILL.md가 500줄에 가까워지면 상세 내용은 `references/`로 내린다.
- 5단계 이상 긴 워크플로우는 reference 문서로 분리하고 본문에는 링크만 둔다.
- 300줄이 넘는 reference는 목차 또는 읽기 순서를 넣는다.
- 본문에서 reference 링크를 줄 때는 왜 읽어야 하는지도 함께 적는다.

예:

```markdown
실제 적용 전에는 references/state-management.md를 직접 읽고 Provider 분리 예시를 확인한다.
```

### 고급 패턴: 압축형 docs index

도메인이 크고 버전 민감도가 높다면 전체 문서를 본문에 넣지 말고 경로 인덱스만 둔다. 이 패턴은 최신 API나 버전별 차이가 중요할 때 특히 유용하다.

```text
[Framework Docs Index]|root: ./references/docs|IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.|01-core/01-basics:{intro.md,setup.md}|02-advanced/01-latest-api:{new-api.md}
```

이 패턴을 쓸 때는 아래를 지킨다.

- 인덱스에는 전체 문서가 아니라 파일 경로만 넣는다.
- 버전 정보를 함께 적는다.
- 최신 API나 학습 데이터에 없을 가능성이 높은 섹션을 앞쪽에 둔다.
- 가능하면 8KB 이하로 유지한다.

모든 스킬에 이 패턴이 필요한 것은 아니다. 큰 reference 세트와 버전 차이가 있을 때만 선택적으로 사용한다.

## 문체 규칙

### 기본 말투

- frontmatter는 영문으로 쓴다.
- 본문은 한국어 중심으로 쓴다.
- 말투는 ~다 체로 쓴다.
- 명령만 나열하지 말고 왜 중요한지 설명한다.

### 작성 방식

- 중요한 정보부터 앞에 둔다. 모델이 읽는 순서가 곧 우선순위다.
- 대문자 강조는 최소화한다. `ALWAYS`, `NEVER`보다 이유 설명이 우선이다.
- 예시는 2~3개면 충분하다. 예시가 많아질수록 references로 분리한다.
- 같은 내용을 description과 본문에 반복하지 않는다.
- 섹션 이름은 역할이 분명한 짧은 제목을 쓴다.

### 길이 기준

- `SKILL.md` 본문은 500줄 이하를 목표로 둔다.
- 긴 예시, 긴 워크플로우, 상세 도메인 규칙은 `references/`로 분리한다.
- 본문이 길어질수록 quick guide 역할이 약해진다는 점을 항상 의식한다.

## 스크립트와 보안 규칙

### 스크립트를 둘 때

아래 조건이면 `scripts/` 도입을 우선 검토한다.

- 같은 코드를 매번 다시 생성하게 될 때
- 파일 조작, API 호출처럼 결정성이 중요할 때
- 테스트 가능성과 재사용성이 중요할 때
- 시간이 지나며 복잡해질 가능성이 높을 때

가능하면 cross-platform 언어를 우선 사용한다.

| 언어       | 적합한 용도                |
| ---------- | -------------------------- |
| Python     | 복잡한 자동화, 데이터 처리 |
| pwsh       | PowerShell Core 스크립트   |
| Node.js    | JavaScript 기반 툴링       |
| Bash/Shell | 짧고 단순한 자동화         |

### 스크립트 품질 기준

- 도움말 또는 사용 예시가 있어야 한다.
- 실패 시 메시지가 명확해야 한다.
- 비밀정보를 저장하지 않는다.
- 파괴적 작업은 사용자 의도를 분명히 요구한다.
- 네트워크 호출이 있으면 문서에 적는다.

## 재사용 패턴

### 파라미터 표 패턴

```markdown
| Parameter   | Required | Default | Description                  |
| ----------- | -------- | ------- | ---------------------------- |
| `--input`   | Yes      | -       | Input file or URL to process |
| `--action`  | Yes      | -       | Action to perform            |
| `--verbose` | No       | `false` | Enable verbose output        |
```

### 멀티스텝 워크플로우 패턴

긴 절차를 본문에 다 넣지 말고 TODO와 reference 링크로 연결한다.

```markdown
## TODO

- [ ] Step 1: Configure environment - see references/workflow-setup.md
- [ ] Step 2: Build project - see references/workflow-build.md
- [ ] Step 3: Validate results - see references/workflow-validation.md
```

## 검증 체크리스트

스킬을 저장하거나 배포하기 전에 아래를 확인한다.

- [ ] `SKILL.md`에 유효한 frontmatter가 있고 `name`, `description`이 들어 있다.
- [ ] frontmatter는 영문이고, 본문은 한국어 중심으로 작성되어 있다.
- [ ] `description`이 기능, 트리거 상황, pushy한 호출 문맥, `Triggers on:` 키워드를 포함한다.
- [ ] "언제 써야 하는가" 정보가 본문이 아니라 description에 모여 있다.
- [ ] 본문이 목표 → 핵심 패턴/단계 → references/범위 순으로 읽히게 구성되어 있다.
- [ ] 본문이 빠른 판단용 요약 가이드 역할을 하고, 상세 구현은 references로 분리되어 있다.
- [ ] 스킬에 로컬 reference나 example이 있다면 retrieval-led reasoning 맥락이 드러난다.
- [ ] `SKILL.md` 본문이 500줄 이하이거나, 길 경우 추가 계층과 포인터로 분리되어 있다.
- [ ] relative path 링크만 사용하고, 리소스 링크가 실제 작업 흐름과 연결된다.
- [ ] scripts가 있다면 도움말, 오류 처리, 보안 원칙을 갖춘다.
- [ ] 겹치는 도메인이 있다면 `## 범위` 또는 description에서 다른 스킬과의 경계를 설명한다.
