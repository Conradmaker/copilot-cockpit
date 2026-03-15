# Agent System Guide

이 문서는 `.github/` 표면을 유지보수할 때 어느 문서가 무엇을 소유하는지 정리하는 보조 가이드다.
authoring 세부 규칙을 다시 쓰지 않고, AGENTS / instructions / agents / memories가 서로 충돌하지 않게 맞추는 데만 집중한다.

## Surface Responsibilities

- `AGENTS.md`: always-on passive context. 전역 불변식, 얇은 workflow 요약, grouped retrieval index를 둔다.
- `instructions/`: shared workflow, packet schema, editing contract 같은 공통 규칙을 둔다.
- `agents/`: receiver-local workflow, cautions, output contract를 둔다.
- `memories/`: project memory 경로와 durable project facts를 둔다.
- `skills/`: reusable capability가 skill-owned surface일 때 수정한다.

## Source Of Truth Map

- phase, gate, artifact lifecycle: `.github/instructions/product-workflow.instructions.md`
- caller-side packet schema (`TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS`, `task_packet`, `implementation_handoff_packet`)와 subagent selection: `.github/instructions/subagent-invocation.instructions.md`
- `.agent.md` authoring rule: `.github/instructions/create-agent.instructions.md`
- `SKILL.md` authoring rule: `.github/instructions/create-skills.instructions.md`
- repo-wide operating summary: `AGENTS.md`
- memory path conventions: `.github/memories/memories.md`

## Editing Order

1. `AGENTS.md`에서 always-on 요약과 owner 문서 링크가 맞는지 먼저 확인한다.
2. `instructions/`에서 shared rule owner를 맞춘다.
3. `agents/`에서 local contract만 남기도록 정리한다.
4. memory 경로나 workflow artifact가 바뀌면 `memories/`와 관련 agent 문구를 함께 맞춘다.

## Alignment Rules

- role 이름이나 역할 분담이 바뀌면 `AGENTS.md`, `instructions/subagent-invocation.instructions.md`, 해당 `.agent.md`를 함께 수정한다.
- gate, handoff, artifact lifecycle 표현은 AGENTS, workflow instruction, agent file 사이에서 충돌하면 안 된다.
- project memory 경로를 참조하는 문구는 `.github/memories/memories.md`와 맞춘다.
- 이 문서에서 create-agent/create-skills의 authoring 규칙을 다시 상세화하지 않는다.

## Out Of Scope

- unrelated `.github/skills/` 확장
- `.github/commands/` 또는 slash command 추가
- hook automation 도입
- non-`.github/` 문서 정리

agent-owned capability를 skill-owned surface로 옮기는 작업은 예외적으로 이 문서의 직접 수정 대상이 된다.

## Maintenance Checklist

- 한 규칙군에 한 개의 상세 owner만 남는다.
- `AGENTS.md`는 summary/index 수준을 넘지 않는다.
- `instructions/`는 shared rule만, `agents/`는 local behavior만 설명한다.
- `description`, `tools`, `agents`, `handoffs`, `user-invocable`, `disable-model-invocation`, output contract 섹션명은 보수적으로 다룬다.
- 수정 후에는 guided handoff, parent tool ceiling, output contract, ownership boundary가 유지되는지 확인한다.
