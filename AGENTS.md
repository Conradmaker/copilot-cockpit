# Agent Harness Guidelines

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.

AGENTS.md의 역할은 항상 보이는 passive context로서 전역 불변식, 얇은 workflow 요약, retrieval index를 고정하는 것이다.

always-on workflow core는 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)에, 장문의 workflow playbook과 artifact template는 [.github/docs](.github/docs)에, caller-side 위임 계약은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)에, agent-local behavior는 각 [.github/agents](.github/agents) 파일에 둔다.

## 전역 불변식

- approved PRD와 required downstream execution-entry artifacts가 없으면 implementation으로 넘어가지 않는다.
- broad review를 통과하기 전에는 git tail이나 memory tail을 기본 경로로 취급하지 않는다.
- invalidated lane만 다시 검증하고, 모든 lane을 기계적으로 재실행하지 않는다.
- Mate, Designer, Architector, Coordinator, Commander, Deep Execution Agent, Reviewer의 subagent ownership 경계를 섞지 않는다.
- AGENTS.md에는 요약만 두고, 상세 workflow, packet schema, receiver-local behavior는 owner 문서에 둔다.
- frontmatter는 영어로 유지하고, 서술형 본문은 AI가 이해하기 쉬운 간결한 한국어로 작성한다.
- 도구 사용과 위임 판단은 현재 코드베이스와 문서를 먼저 조회한 뒤 내린다.


always-on guardrail과 artifact precedence는 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 따르고, 장문의 phase detail, rationale, failure pattern은 [.github/docs/workflow/WORKFLOW-PLAYBOOK.md](.github/docs/workflow/WORKFLOW-PLAYBOOK.md)를 필요할 때 읽는다.
caller-side packet과 subagent 선택은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)를 따른다.
agent/skill authoring rule은 [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md)와 [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md)를 따른다.

## 작업 전 참조 순서

1. 이 문서로 현재 하네스의 operating philosophy와 ownership boundary를 잡는다.
2. cross-phase process detail이나 rationale이 필요하면 [.github/docs/workflow/WORKFLOW-PLAYBOOK.md](.github/docs/workflow/WORKFLOW-PLAYBOOK.md)를 읽는다.
3. always-on guardrail, artifact precedence, workflow loading rule을 확인하거나 수정할 때 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 읽는다.
4. 서브에이전트를 고르거나 XML packet을 만들어야 하면 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)를 읽는다.
5. `.agent.md` 또는 `SKILL.md`를 수정할 때만 [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md) 또는 [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md)를 읽는다.
6. 도메인별 구현이나 리뷰 품질을 올려야 하면 아래 통합 인덱스에서 맞는 skill 또는 reference를 고른다.

## 통합 인덱스

### Instructions

- [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md): always-on workflow core, artifact precedence, loading rule의 단일 owner다.
- [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md): `TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS`, `task_packet`, `implementation_handoff_packet`, subagent selection의 단일 owner다.
- [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md): `.agent.md` authoring rule을 수정할 때만 읽는다.
- [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md): `SKILL.md` authoring rule을 수정할 때만 읽는다.
- [.github/instructions/typescript.instructions.md](.github/instructions/typescript.instructions.md): TypeScript 변경 시 언어 기준을 고정한다.

### Docs

- [.github/docs/workflow/WORKFLOW-PLAYBOOK.md](.github/docs/workflow/WORKFLOW-PLAYBOOK.md): planning-to-tail long-form workflow reference다.
- [.github/docs/artifacts/PRD-TEMPLATE.md](.github/docs/artifacts/PRD-TEMPLATE.md): Mate PRD artifact의 구조와 rubric을 정의한다.
- [.github/docs/artifacts/DESIGN-TEMPLATE.md](.github/docs/artifacts/DESIGN-TEMPLATE.md): Designer design artifact의 구조와 design-to-dev bridge 기준을 정의한다.
- [.github/docs/artifacts/TECHNICAL-TEMPLATE.md](.github/docs/artifacts/TECHNICAL-TEMPLATE.md): Architector technical artifact의 구조와 architecture-to-execution bridge 기준을 정의한다.
- [.github/docs/artifacts/EXECUTION-PLAN-TEMPLATE.md](.github/docs/artifacts/EXECUTION-PLAN-TEMPLATE.md): Commander execution plan artifact의 구조와 rubric을 정의한다.
- [.github/docs/AGENT-SYSTEM-GUIDE.md](.github/docs/AGENT-SYSTEM-GUIDE.md): `.github` surface ownership과 alignment rule을 정리한다.

### Agents

- [.github/agents/Mate.agent.md](.github/agents/Mate.agent.md): planning owner이며 approved PRD와 references를 만든다.
- [.github/agents/Designer.agent.md](.github/agents/Designer.agent.md): approved PRD 뒤 user-gated downstream design work를 맡아 `design.md`를 만든다.
- [.github/agents/Architector.agent.md](.github/agents/Architector.agent.md): approved PRD 뒤 user-gated downstream technical work를 맡아 `technical.md`를 만든다.
- [.github/agents/Explore.agent.md](.github/agents/Explore.agent.md), [.github/agents/Librarian.agent.md](.github/agents/Librarian.agent.md): local evidence와 external evidence를 분리해 조회 품질을 올린다.
- [.github/agents/Coordinator.agent.md](.github/agents/Coordinator.agent.md): role-based planning/execution review를 제공한다.
- [.github/agents/Commander.agent.md](.github/agents/Commander.agent.md), [.github/agents/Deep-execution.agent.md](.github/agents/Deep-execution.agent.md): execution plan 수립, dependency-aware orchestration, todo 기반 진행 추적, delegated implementation을 분리한다.
- [.github/agents/Reviewer.agent.md](.github/agents/Reviewer.agent.md): broad quality gate를 맡는다.

### Skills

- Design & UX: [.github/skills/ds-product-ux/SKILL.md](.github/skills/ds-product-ux/SKILL.md), [.github/skills/ds-visual-design/SKILL.md](.github/skills/ds-visual-design/SKILL.md), [.github/skills/ds-ui-patterns/SKILL.md](.github/skills/ds-ui-patterns/SKILL.md), [.github/skills/refero-design/SKILL.md](.github/skills/refero-design/SKILL.md)
	화면 구조, UX writing, visual craft, reference-led UI research가 필요할 때 읽는다.
- Frontend engineering: [.github/skills/fe-a11y/SKILL.md](.github/skills/fe-a11y/SKILL.md), [.github/skills/fe-code-conventions/SKILL.md](.github/skills/fe-code-conventions/SKILL.md), [.github/skills/fe-code-review/SKILL.md](.github/skills/fe-code-review/SKILL.md), [.github/skills/fe-react-patterns/SKILL.md](.github/skills/fe-react-patterns/SKILL.md), [.github/skills/fe-react-performance/SKILL.md](.github/skills/fe-react-performance/SKILL.md), [.github/skills/fe-tailwindcss/SKILL.md](.github/skills/fe-tailwindcss/SKILL.md), [.github/skills/fe-ui-element-components/SKILL.md](.github/skills/fe-ui-element-components/SKILL.md)
	접근성, clean code, review, React architecture, performance, Tailwind, shared UI API를 다룰 때 읽는다.
- Workflow & tooling: [.github/skills/agent-browser/SKILL.md](.github/skills/agent-browser/SKILL.md), [.github/skills/brainstorming/SKILL.md](.github/skills/brainstorming/SKILL.md), [.github/skills/crafting-effective-readmes/SKILL.md](.github/skills/crafting-effective-readmes/SKILL.md), [.github/skills/file-creator/SKILL.md](.github/skills/file-creator/SKILL.md), [.github/skills/gh-cli/SKILL.md](.github/skills/gh-cli/SKILL.md), [.github/skills/git-workflow/SKILL.md](.github/skills/git-workflow/SKILL.md), [.github/skills/pdf/SKILL.md](.github/skills/pdf/SKILL.md), [.github/skills/seo-audit/SKILL.md](.github/skills/seo-audit/SKILL.md), [.github/skills/skill-creator/SKILL.md](.github/skills/skill-creator/SKILL.md)
	browser automation, quick ideation, README, file scaffolding, git/gh, PDF, SEO, skill maintenance가 필요할 때 읽는다.
- Memory & context: [.github/skills/memory-synthesizer/SKILL.md](.github/skills/memory-synthesizer/SKILL.md)
	durable signal 판별, memory scope 선택, memory pollution 방지가 필요할 때 읽는다.

### References

- Workflow/meta references: [ref/AGENTS.md](ref/AGENTS.md), [ref/rule-guide.md](ref/rule-guide.md), [ref/project-concept.md](ref/project-concept.md)
	운영 철학, 규칙 해석, 장기 방향을 다시 확인할 때 읽는다.
- Authoring examples: [ref/agent-ref](ref/agent-ref), [ref/create-agent-ref](ref/create-agent-ref), [ref/create-skill-ref](ref/create-skill-ref)
	agent/skill 구조와 표현 방식을 비교할 때 읽는다.
- Design and harness comparators: [ref/design.md](ref/design.md), [ref/hooks-ref](ref/hooks-ref), [ref/other-harness](ref/other-harness)
	설계 언어, hook 개념, 다른 harness의 tradeoff를 참고할 때 읽는다.

## 유지보수 규칙

- workflow 상세를 AGENTS.md에 다시 길게 복제하지 않는다.
- caller-side packet schema와 delegation rule은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)에 둔다.
- receiver-side local workflow와 cautions는 각 agent file에 둔다.
- authoring-specific 규칙은 create-agent/create-skills가 owner이므로 여기서 다시 상세화하지 않는다.
- AGENTS index는 grouped retrieval surface를 유지하되, 항상-on 문서라는 점을 고려해 summary level을 넘기지 않는다.
