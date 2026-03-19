# Agent Guidelines

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.

AGENTS.md의 역할은 항상 보이는 passive context로서 이 저장소의 철학, ownership boundary, 그리고 최소 owner map만 고정하는 것이다.

스킬 discovery의 source of truth는 [.github/instructions/skill-index.instructions.md](.github/instructions/skill-index.instructions.md)다.


## Core Principles

- 근거가 필요하면 pre-training 기반 추측보다 relevant skill나 자료조사를 진행한다.
- shared rule은 instructions, long-form reference는 docs, local contract는 agents, domain execution guidance는 skills에 둔다.

## Owner Map

- workflow core와 artifact precedence: [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)
- caller-side packet schema와 subagent selection: [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)
- workspace skill discovery registry: [.github/instructions/skill-index.instructions.md](.github/instructions/skill-index.instructions.md)
- `.agent.md` authoring rule: [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md)
- `SKILL.md` authoring rule: [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md)
