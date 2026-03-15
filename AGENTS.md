# Agent Harness Guidelines

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.

AGENTS.md의 역할은 항상 보이는 passive context로서 전역 불변식, 얇은 workflow 요약, retrieval index를 고정하는 것이다.

상세 process는 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)에, caller-side 위임 계약은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)에, agent-local behavior는 각 [.github/agents](.github/agents) 파일에 둔다.

## 전역 불변식

- planning quality gate와 handoff-enabled user gate가 없으면 implementation으로 넘어가지 않는다.
- broad review를 통과하기 전에는 git tail이나 memory tail을 기본 경로로 취급하지 않는다.
- invalidated lane만 다시 검증하고, 모든 lane을 기계적으로 재실행하지 않는다.
- Mate, Coordinator, Commander, Deep Execution Agent, Reviewer의 subagent ownership 경계를 섞지 않는다.
- AGENTS.md에는 요약만 두고, 상세 workflow, packet schema, receiver-local behavior는 owner 문서에 둔다.
- frontmatter는 영어로 유지하고, 서술형 본문은 AI가 이해하기 쉬운 간결한 한국어로 작성한다.
- 도구 사용과 위임 판단은 현재 코드베이스와 문서를 먼저 조회한 뒤 내린다.

## 워크플로우 핵심 요약

### Planning

- Mate가 EARS requirements와 다차원 커버리지 체크로 spec-first plan을 만든다.
- Mate는 추측보다 Explore, Librarian, askQuestions를 우선해 user intent와 plan/spec을 예리하게 다듬는다.
- planning checkpoint에서 Mate는 작업 성격에 맞는 coordinator lane을 최소 2개 동적으로 선택해 병렬로 돌린다. 같은 wave에 Explore, Librarian를 붙일 수 있다.
- Coordinator는 coord-roles/{role}.md를 동적 로드해 role-specific 검토를 수행한다.
- quality gate 통과 후 approved plan briefing을 보여주고, askQuestions로 handoff path를 확인한다. handoff 실행 허용 상태가 성립하면 확인된 path 기반으로 handoff.md를 작성한다.
- 만약 quality gate를 통과했어도, user intent clarification, evidence gap, risk mitigation이 필요하면 user approval 전에 먼저 필요한 정보를 구조화해서 user에게 askQuestions를 보낸다.
- user가 handoff를 직접 실행할 때만 execution으로 넘어간다.

### Execution

- 승인된 execution은 Fleet Mode 경로로만 진행되며 Commander가 orchestration을 맡고 Deep Execution Agent가 coding worker가 된다.
- Commander와 Deep Execution Agent는 구현 방향에 대한 확신이 흔들리거나 drift가 의심될 때 Coordinator에 롤을 지정해 리뷰를 요청할 수 있다.

### Review

- Reviewer가 broad quality gate를 맡는다.
- review failure는 implementer rework로 되돌리고, spec-level failure는 planning으로 되돌린다.

### Tail

- Memory Tail은 durable signal이 충분할 때 `.github/skills/memory-synthesizer/SKILL.md`를 execution owner가 inline으로 사용한다.

상세 단계, gate, escalation, drift signal은 반드시 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 먼저 따른다.
caller-side packet과 subagent 선택은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)를 따른다.
agent/skill authoring rule은 [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md)와 [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md)를 따른다.

## 작업 전 참조 순서

1. 이 문서로 현재 하네스의 operating philosophy와 ownership boundary를 잡는다.
2. process detail이 필요하면 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 읽는다.
3. 서브에이전트를 고르거나 XML packet을 만들어야 하면 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)를 읽는다.
4. `.agent.md` 또는 `SKILL.md`를 수정할 때만 [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md) 또는 [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md)를 읽는다.
5. 도메인별 구현이나 리뷰 품질을 올려야 하면 아래 통합 인덱스에서 맞는 skill 또는 reference를 고른다.

## 통합 인덱스

### Instructions

- [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md): phase, gate, artifact lifecycle의 단일 owner다.
- [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md): `TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS`, `task_packet`, `implementation_handoff_packet`, subagent selection의 단일 owner다.
- [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md): `.agent.md` authoring rule을 수정할 때만 읽는다.
- [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md): `SKILL.md` authoring rule을 수정할 때만 읽는다.
- [.github/instructions/typescript.instructions.md](.github/instructions/typescript.instructions.md): TypeScript 변경 시 언어 기준을 고정한다.

### Agents

- [.github/agents/Mate.agent.md](.github/agents/Mate.agent.md): planning owner이며 execution-ready plan과 handoff를 만든다.
- [.github/agents/Explore.agent.md](.github/agents/Explore.agent.md), [.github/agents/Librarian.agent.md](.github/agents/Librarian.agent.md): local evidence와 external evidence를 분리해 조회 품질을 올린다.
- [.github/agents/Coordinator.agent.md](.github/agents/Coordinator.agent.md): role-based planning/execution review를 제공한다.
- [.github/agents/Commander.agent.md](.github/agents/Commander.agent.md), [.github/agents/Deep-execution.agent.md](.github/agents/Deep-execution.agent.md): execution orchestration과 delegated implementation을 분리한다.
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
