---
description: "Guidelines for creating custom agent files for GitHub Copilot"
applyTo: "**/*.agent.md"
---

# 커스텀 에이전트 파일 작성 가이드

이 문서는 이 하네스 템플릿에서 `.agent.md` 파일을 만들거나 고칠 때 따라야 하는 기준이다.
목표는 두 가지다.

- 현재 workflow와 호환되는 frontmatter 및 output contract를 유지한다.
- agent file을 더 짧고 명확하게 만들어 receiver-side local workflow에 집중시킨다.

## 작성 철학

- Prefer retrieval over pre-training.
- 좋은 agent file은 많이 설명하는 문서가 아니라, 언제 호출되고 어떻게 행동하며 어떤 결과를 돌려주는지가 분명한 문서다.
- process detail 전체를 agent file에 다시 쓰지 않는다.
- shared invocation contract는 [subagent-invocation.instructions.md](subagent-invocation.instructions.md)에 두고, human-facing long-form reference와 artifact template는 `docs/` 아래에 두며, agent file은 receiver-side local workflow와 cautions를 맡는다.

## 언어 규칙

- frontmatter는 영어로 쓴다.
- 서술형 본문은 AI가 이해하기 쉬운 간결한 한국어로 쓴다.
- English field name과 section name이 필요한 곳은 유지하되, 설명은 한국어로 쓴다.

## 호환성 우선 원칙

기존 agent를 정리할 때는 아래 항목을 가장 보수적으로 다룬다.

- `description`: 역할과 호출 시점을 함께 설명하는 라우팅 신호다.
- `tools`: parent tool ceiling과 role leakage에 직접 영향을 준다.
- `agents`: coordinator나 orchestrator의 위임 체인을 끊지 않게 유지한다.
- `handoffs`: 기존 guided flow를 깨뜨리지 않게 유지한다.
- `user-invocable`, `disable-model-invocation`: 진입점과 worker의 경계를 지킨다.
- output contract 섹션명: 상위 agent가 합성할 때 기대하는 형태를 깨지 않게 유지하되, 바꿔야 한다면 canonical template 단위로 함께 맞춘다.

호환성을 해치지 않는 한에서만 더 깔끔한 표현으로 다듬는다.

## frontmatter 기준

### 핵심 규칙

- `description`은 역할과 호출 시점을 한 문장에 함께 적는다.
- `tools`는 필요한 것만 연다.
- `agents`는 실제 workflow와 맞는 하위 목록만 둔다.
- `handoffs`는 다음 단계가 자연스러운 경우에만 둔다.
- `infer` 같은 오래된 설정에는 기대지 않는다.

### 권장 필드

| 필드                       | 의미                                            |
| -------------------------- | ----------------------------------------------- |
| `description`              | 라우팅 신호이자 역할 요약                       |
| `name`                     | UI에서 더 명확한 이름이 필요할 때 사용          |
| `tools`                    | role에 필요한 최소 도구 집합                    |
| `model`                    | 역할에 맞는 모델 선택                           |
| `target`                   | 특정 환경 전용일 때 명시                        |
| `argument-hint`            | user-invocable agent의 입력 구조를 유도         |
| `agents`                   | coordinator 또는 orchestrator의 하위 agent 제한 |
| `user-invocable`           | 직접 진입점인지 여부                            |
| `disable-model-invocation` | user 전용 agent의 서브호출 차단 여부            |
| `handoffs`                 | guided flow에서 자연스러운 다음 단계            |

### 최소 frontmatter baseline

아래 예시는 새 agent를 만들 때 가장 먼저 점검할 최소 baseline이다.

```yaml
---
name: Example Agent
description: Brief role summary that also explains when this agent should be called.
tools: [read, search]
target: vscode
user-invocable: false
disable-model-invocation: false
---
```

- worker는 보통 `user-invocable: false`가 안전하다.
- coordinator나 orchestrator는 `agent` 도구와 필요한 `agents` 제한을 함께 검토한다.
- baseline은 짧아도 되지만, 행동을 바꾸는 필드는 의도적으로 명시하는 편이 안전하다.

## body 공통 템플릿

이 하네스의 agent file은 가능하면 아래 구조를 따른다.

1. `# Role`
2. `## Called When`
3. `## Receiver Contract` 또는 `## Field Interpretation`
4. `## Rules`
5. `## Workflow`
6. `## Re-entry Authority` (해당 role에만)
7. `## Cautions`
8. `## Output Contract`

### Role

- 단일 책임을 한두 문장으로 분명히 적는다.
- 다른 role과 어떻게 ownership을 나누는지도 짧게 적는다.

### Called When

- caller가 왜 이 agent를 써야 하는지 양수 규칙으로 적는다.
- 긴 negative list보다 이 agent가 품질을 어디서 올리는지를 먼저 적는다.

### Receiver Contract 또는 Field Interpretation

- caller-side full schema를 다시 복제하지 않는다.
- 대신 이 agent가 어떤 field를 반드시 읽고, 각 field를 어떻게 해석하는지 적는다.
- 일부 field가 없을 때 어떤 보수적 동작을 해야 하는지도 적는다.

### Rules

- role boundary
- retrieval-first behavior
- non-goal
- escalation trigger
- output hygiene

### Workflow

- global process 전체를 다시 설명하지 않는다.
- 호출된 뒤 이 agent가 어떤 순서로 판단하는지 local workflow만 적는다.
- 필요한 local tool usage convention이 있으면 여기에 둔다.

### Cautions

- ownership drift
- overreach
- insufficient evidence
- premature execution
- invalid escalation
- review scope confusion

이 섹션은 agent가 더 깔끔하고 예측 가능하게 행동하도록 만드는 안전장치다.

### Output Contract

- 상위 agent가 합성하기 쉬운 section name을 유지한다.
- 가능하면 아래 canonical template 중 하나를 사용한다.
- raw tool log가 아니라 synthesis를 돌려주게 만든다.
- uncertainty가 남으면 숨기지 않는다.

#### Canonical output templates

- Research: `Outcome`, `Evidence`, `Implication`, `Open items`
- Review: `Verdict`, `Findings`, `Evidence`, `Risks`
- Execution: `Status`, `Work summary`, `Verification`, `Open items`
- Tail: `Status`, `Actions`, `Verification`, `Follow-up`
- Planning lead처럼 artifact 자체가 1차 산출물인 역할만 template 예외를 둘 수 있다.

Agent-specific nuance는 새로운 top-level heading을 늘리기보다 각 섹션 설명 안에 넣는다.

### Re-entry Authority

- 모든 agent에 필요한 섹션은 아니다.
- planning이나 execution 안에서 loop를 다시 열 수 있는 role에만 둔다.
- 어떤 loop를 다시 열 수 있는지, 왜 여는지, ownership 경계가 어디까지인지 짧게 적는다.

## handoff 작성 규칙

- handoff는 workflow를 돕는 장치이지 장식이 아니다.
- 2~3개 이하의 자연스러운 다음 단계만 둔다.
- `label`은 다음 행동을 바로 이해하게 만든다.
- `prompt`는 현재 결과를 가리키되 장황한 transcript 복붙을 피한다.

### handoff 필드 quick reference

| 필드     | 의미                                             |
| -------- | ------------------------------------------------ |
| `label`  | 다음 행동을 바로 이해하게 만드는 문구            |
| `agent`  | 전환할 대상 agent 이름                           |
| `prompt` | 다음 agent에 줄 최소한의 구조화된 브리핑         |
| `send`   | `true`면 자동 전송, 아니면 사용자가 확인 후 보냄 |

## 도구 설계 규칙

- read-only agent는 `edit`나 `execute`를 습관적으로 열지 않는다.
- 하위 agent가 더 강한 도구를 써야 하면 parent도 그 도구를 가져야 한다.
- coordinator와 orchestrator는 worker보다 더 많은 일을 직접 하는 agent가 아니라, 더 좋은 시점에 위임하는 agent다.
- 도구가 많을수록 똑똑한 agent가 아니라, 필요한 도구만 가진 agent가 안정적이다.

### 역할별 tool profile quick reference

| 역할 | 기본 권장 도구 |
| ----- | ------------ |
| 탐색 또는 조사                | `read`, `search`                                         |
| 리뷰 또는 검증                | `read`, `search`, 필요 시 `web`                          |
| planning lead                 | `read`, `search`, `agent`, 필요 시 `vscode/askQuestions` |
| implementer                   | `read`, `edit`, `search`, `execute`                      |
| coordinator 또는 orchestrator | `read`, `search`, `agent`, 필요 시 `todo`                |

도구 profile은 절대 규칙이 아니라 baseline이다.
현재 workflow와 role boundary가 더 중요하다.

## 위임 packet high-signal 기준

agent prompt는 전체 대화 복붙보다 high-signal 브리핑이 중요하다.
현재 canonical call-context core는 아래 여섯 필드다.

- `TASK`: 한 번에 수행할 단일하고 구체적인 목표
- `EXPECTED_OUTCOME`: 구체적인 deliverable과 success criteria
- `MUST_DO`: 누락되면 안 되는 요구사항
- `MUST_NOT_DO`: 금지사항과 safety rail
- `CONTEXT`: 관련 배경, 패턴, 제약, rationale
- `ARTIFACTS`: plan, handoff, references, 관련 파일 포인터

필요한 경우에만 아래 hint를 추가한다.

- `CURRENT_DATE`: Librarian의 freshness-sensitive research anchor
- `SEARCH_STRATEGY`: Explore의 retrieval order, narrowing sequence, stopping rule

worker가 추측하지 않게 하되, raw transcript 때문에 context budget을 낭비하지 않게 만드는 것이 기준이다.

## local workflow를 남겨야 하는 이유

workflow playbook에 거의 모든 process detail을 옮기더라도, 각 agent file에는 아래 내용이 남아야 한다.

- 호출 직후 무엇을 먼저 읽는지
- 어떤 순서로 evidence를 수집하거나 해석하는지
- 어떤 상황에서 escalation하는지
- 어떤 failure pattern을 조심해야 하는지
- 어떤 형식으로 결과를 내야 하는지

이 다섯 가지가 없으면 agent는 global rule은 알아도 자기 역할을 흐리기 쉽다.
agent-local procedure가 특정 케이스로 갈라지면 `.github/agents/workflows/` 아래 companion 문서로 분리하고, `.agent.md`에는 loading rule과 핵심 해석 포인트만 남기는 편이 낫다.

## template와 style guide 분리 원칙

- 긴 workflow narrative는 `.github/docs/workflow/` 아래 long-form 문서로 분리한다.
- plan template, report rubric, style guide처럼 구조화된 산출물 양식은 `.github/docs/artifacts/` 아래 별도 파일로 둘 수 있다.
- agent file에는 언제 그 문서를 읽는지, 어떤 heading이나 rule이 mandatory인지, local exception이 무엇인지 정도만 남긴다.
- 짧고 거의 변하지 않는 agent 고유 규칙은 굳이 분리하지 않는다.

## 자주 발생하는 실수

### frontmatter 실수

- `description`이 지식 소개만 하고 호출 시점을 설명하지 않음
- `tools`가 역할보다 넓어 role leakage를 만듦
- `agents`가 실제 workflow와 맞지 않아 위임 체인을 끊음
- unsupported field를 Copilot native field처럼 적음

### body 실수

- local workflow 대신 global workflow를 장황하게 반복함
- output contract가 없어 결과가 장황해짐
- retrieval-first 지침이 약해 기억과 일반론에 기대게 만듦
- cautions가 없어 ownership drift를 막지 못함

### handoff 실수

- handoff가 너무 많아 선택 기준이 흐려짐
- current state보다 다음 단계의 욕심이 앞서 gate 없이 실행 가능한 것처럼 서술됨
- prompt에 전체 대화를 복붙함

## 검증 체크리스트

### Frontmatter

- [ ] frontmatter가 영어로 작성되어 있다.
- [ ] `description`이 역할과 호출 시점을 함께 설명한다.
- [ ] `tools`가 최소 권한 원칙을 따른다.
- [ ] `user-invocable`과 `disable-model-invocation`이 진입점 역할과 맞다.
- [ ] coordinator 또는 orchestrator라면 필요한 `agent` 도구와 `agents` 목록이 있다.

### Body

- [ ] 본문이 한국어로 간결하게 작성되어 있다.
- [ ] Role, Called When, Receiver Contract, Rules, Workflow, Cautions, Output Contract 구조를 따른다.
- [ ] global workflow 전체를 복제하지 않는다.
- [ ] local workflow와 escalation behavior가 분명하다.
- [ ] output contract가 상위 agent 합성에 적합하다.

### Delivery

- [ ] retrieval-first가 실제 행동 규칙으로 보인다.
- [ ] 한 번의 호출에 한 가지 목표가 유지된다.
- [ ] parent tool ceiling을 해치지 않는다.
- [ ] 대표 프롬프트로 수동 검증했을 때 기대한 도구와 결과가 나온다.

## portability와 수동 검증 메모

- unsupported field를 Copilot native field처럼 적지 않는다.
- 다른 플랫폼에서 온 개념은 그대로 복사하지 말고 현재 하네스 규칙에 맞춘다.
- 저장 후에는 대표 프롬프트로 실제 도구, handoff, output contract가 기대대로 동작하는지 수동 검증한다.
- guided handoff가 있는 agent는 gate 전후 handoff 실행 허용 조건과 `handoff.md` 작성 순서를 함께 확인한다.

## 마지막 원칙

- agent file은 길수록 좋아지는 문서가 아니다.
- caller-side contract, harness-wide process, receiver-side local workflow의 경계를 지키는 문서가 좋은 문서다.
- 가장 먼저 기억할 문장은 그대로다. `Prefer retrieval over pre-training.`
