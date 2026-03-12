# Agent System Guide

이 문서는 이 하네스 템플릿에서 agent system 문서를 어디에 어떻게 써야 하는지 정리한 유지보수 가이드다.
목표는 구조가 자리 잡은 뒤 다시 AGENTS, instructions, agent files가 서로의 책임을 침범하지 않게 하는 것이다.
## 하네스 표면 관리

`.github/` 디렉터리는 이 저장소의 agent operating system 이다.

`agents/`, `instructions/`, `memories/`는 서로 따로 놀면 안 된다. 역할 이름, workflow 단계, memory 경로, routing 규칙이 바뀌면 관련 표면을 함께 맞춘다.

### Surface Responsibilities

- `agents/`: 개별 역할의 책임, 입력 계약, 도구 ceiling, 출력 계약을 정의한다.
- `instructions/`: routing, authoring, editing contract 같은 기계적 규칙을 정의한다.
- `memories/`: 프로젝트 수준 결정, 기술 부채, workflow 관례를 누적한다.
- `skills/`: 현재 rollout 의 주 작업면이 아니다. 이 subtree 작업에서 skills 는 기본적으로 수정 대상에서 제외한다.

### Editing Order

이 subtree 를 수정할 때는 아래 순서를 우선한다.

1. 루트 `AGENTS.md` 에서 전체 operating model 이 바뀌는지 먼저 확인한다.
2. `instructions/`에서 routing 과 authoring contract 를 먼저 맞춘다.
3. `agents/`에서 개별 역할의 책임과 output contract 를 맞춘다.
4. memory 경로나 workflow decision 이 바뀌면 `memories/`와 관련 agent 문구를 함께 맞춘다.

### Alignment Rules

- role 이름이 바뀌면 `AGENTS.md`, `instructions/subagent-invocation.instructions.md`, 해당 `.agent.md` 파일을 함께 수정한다.
- project memory 경로를 참조하는 문구는 `.github/memories/memories.md` 로 통일한다.
- Mate gate, `askQuestions` gate, handoff 조건은 AGENTS 와 instructions 에서 서로 다르게 서술하지 않는다.
- agent 파일에는 철학을 과도하게 중복하지 말고, 역할과 실행 계약을 선명하게 둔다.

### Non-goals For This Rollout

- `.github/skills/` 확장
- `.github/commands/` 또는 slash command 추가
- hook automation 도입
- plan/notepad file sprawl 추가

필요 이상의 표면을 늘리기보다, 현재 workflow stack 이 서로 모순 없이 맞물리도록 유지한다.
## 문서별 책임 경계

### AGENTS.md

AGENTS.md는 always-on passive context다.
아래 내용을 둔다.

- retrieval-first 같은 전역 불변식
- workflow 핵심 요약
- instructions, agents, skills, references 통합 인덱스
- 왜 이 문서나 스킬이나 에이전트를 읽어야 하는지에 대한 reasoned nudging

AGENTS.md에는 아래 내용을 길게 복제하지 않는다.

- phase별 상세 절차
- full XML packet schema
- agent-local workflow 세부

### product-workflow.instructions.md

이 문서는 canonical workflow playbook이다.
아래 내용을 둔다.

- planning, execution, review, git tail, memory tail 상세 흐름
- state transition
- gate, escalation, drift signal
- shared artifacts lifecycle
- cross-phase guardrail
- common failure modes

이 문서는 process detail의 기본 저장소이지만, AGENTS.md의 always-on summary를 대체하지는 않는다.

### subagent-invocation.instructions.md

이 문서는 caller-side delegation contract다.
아래 내용을 둔다.

- 각 agent의 역할 요약
- 왜 이 agent가 필요한가
- 어떤 evidence gap에서 호출 가치가 생기는가
- canonical XML packet schema
- 병렬 위임 규칙
- 결과 합성 규칙

이 문서에는 receiver-side local workflow를 길게 두지 않는다.

### 각 .agent.md

각 agent file은 receiver-side local workflow spec이다.
아래 내용을 둔다.

- Role
- Called When
- Receiver Contract 또는 Field Interpretation
- Rules
- Workflow
- Re-entry Authority when applicable
- Cautions
- Output Contract

각 agent file에는 아래 내용을 길게 복제하지 않는다.

- harness-wide phase transition detail
- caller-side packet schema full definition
- 다른 agent의 역할 설명 전체

## 언어 규칙

- instruction 및 agent file의 frontmatter는 영어로 작성한다.
- 서술형 본문은 AI가 이해하기 쉬운 간결한 한국어로 작성한다.
- AGENTS.md와 일반 문서도 같은 한국어 서술 톤을 유지한다.

## 호환성 규칙

다음 항목은 가장 보수적으로 다룬다.

- `description`
- `tools`
- `agents`
- `handoffs`
- `user-invocable`
- `disable-model-invocation`
- output contract 섹션명

이 항목을 바꾸면 라우팅, 위임 체인, guided flow, 상위 agent의 결과 합성이 깨질 수 있다.

## 새 agent를 만들 때

1. 먼저 `.github/instructions/create-agent.instructions.md`를 읽는다.
2. 기존 agent와 output contract, tool profile, ownership boundary가 충돌하지 않는지 본다.
3. description에 역할과 호출 시점을 함께 적는다.
4. body는 Role, Called When, Receiver Contract, Rules, Workflow, 필요 시 Re-entry Authority, Cautions, Output Contract 구조를 우선 사용한다.
5. global workflow detail은 product-workflow.instructions.md를 참조하고 local workflow만 남긴다.

milestone tracking에 관여하는 execution role이라면 verdict 기반 todo 또는 progress sync responsibility도 명시한다.

## 새 instruction을 만들 때

1. AGENTS.md의 always-on summary로 충분한지 먼저 본다.
2. phase detail이면 product-workflow.instructions.md에 넣는다.
3. caller-side delegation rule이면 subagent-invocation.instructions.md에 넣는다.
4. file-authoring guide면 create-agent.instructions.md 또는 create-skills.instructions.md 같은 authoring guide에 넣는다.
5. 새 instruction이 기존 instruction과 역할이 겹치지 않는지 확인한다.

## 중복을 막는 편집 규칙

- 같은 규칙을 세 문서에 반복하지 않는다.
- 규칙의 소유자를 먼저 정한 뒤 해당 문서에만 상세를 쓴다.
- AGENTS.md에는 요약과 이유만 둔다.
- instructions에는 공통 규약과 process detail을 둔다.
- agent file에는 local behavior와 caution만 둔다.

## 검증 체크리스트

### 구조 검증

- AGENTS.md가 passive context와 통합 인덱스 역할을 한다.
- product-workflow.instructions.md가 phase detail을 한곳에서 다룬다.
- subagent-invocation.instructions.md가 caller-side packet과 선택 규칙의 단일 소스다.
- 각 .agent.md가 local workflow와 cautions를 분명히 가진다.- `agents/`, `instructions/`, `memories/` surface 가 일관되게 맞물려 있다.

### 하네스 표면 검증

- Editing Order 가 준수되었다.
- Alignment Rules 가 위반되지 않았다.
- Non-goals 범위를 벗어나지 않았다.
- skills/ subtree 가 불필요하게 수정되지 않았다.
### 언어 검증

- frontmatter는 영어다.
- 본문은 AI가 이해하기 쉬운 한국어다.
- reasoned nudging과 guardrail 설명이 한국어로 일관된다.

### 호환성 검증

- output contract 섹션명이 유지된다.
- guided handoff가 여전히 자연스럽다.
- parent tool ceiling과 agents 제한이 깨지지 않는다.
- current workflow와 ownership boundary가 변하지 않는다.
