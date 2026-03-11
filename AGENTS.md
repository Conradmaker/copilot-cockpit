# Agent Harness Guidelines

IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.

이 저장소는 오래 재사용할 에이전트 하네스 템플릿이다.
AGENTS.md의 역할은 모든 세부 규칙을 직접 품는 것이 아니라, 항상 보이는 passive context로서 현재 운영 철학과 참조 우선순위를 고정하는 것이다.

## 이 문서가 맡는 역할

- planning → execution → review → git tail → memory tail 흐름의 핵심 요약을 항상 보이게 유지한다.
- 어떤 세부 문서를 왜 먼저 읽어야 하는지 reasoned nudging을 제공한다.
- instruction, skill, reference, agent를 분리된 목록이 아니라 하나의 retrieval index로 정리한다.
- current workflow와 role boundary를 바꾸지 않는 전역 불변식을 유지한다.

이 문서는 decision tree를 늘리는 문서가 아니다.
상세 process는 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)에, caller-side 위임 계약은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)에, agent-local behavior는 각 [.github/agents](.github/agents) 파일에 둔다.

## 전역 불변식

- planning quality gate와 explicit user approval이 없으면 implementation으로 넘어가지 않는다.
- broad review를 통과하기 전에는 git tail이나 memory tail을 기본 경로로 취급하지 않는다.
- invalidated lane만 다시 검증하고, 모든 lane을 기계적으로 재실행하지 않는다.
- Mate, Coordinator, Commander, Deep Execution Agent, Reviewer, Git Master, Memory Synthesizer의 ownership 경계를 섞지 않는다.
- frontmatter는 영어로 유지하고, 서술형 본문은 AI가 이해하기 쉬운 간결한 한국어로 작성한다.
- 도구 사용과 위임 판단은 현재 코드베이스와 문서를 먼저 조회한 뒤 내린다.

## 워크플로우 핵심 요약

### Planning

- Mate가 execution-ready plan을 만든다.
- Mate는 추측보다 Explore, Librarian, askQuestions를 우선해 user intent와 plan/spec을 예리하게 다듬는다.
- planning checkpoint가 열리면 `manager-coord`, `product-coord`, Explore, Librarian를 같은 wave에서 병렬로 돌릴 수 있다.
- Coordinator는 invalidated 된 planning lane 또는 milestone만 검증한다.
- latest coordinator-reviewed revision이 quality gate를 통과해 `handoff.md`가 준비되면 approved plan briefing과 함께 implementation handoff surface를 노출할 수 있다. actual implementation 시작은 explicit user approval 이후다.
- 만약 quality gate를 통과했어도, user intent clarification, evidence gap, risk mitigation이 필요하면 user approval 전에 먼저 필요한 정보를 구조화해서 user에게 askQuestions를 보낸다.

### Execution

- Fleet Mode에서는 Commander가 orchestration을 맡고 Deep Execution Agent가 coding worker가 된다.
- Rush Mode에서는 Deep Execution Agent가 단일 implementer로 실행을 끌고 간다.
- 두 모드 모두 major milestone마다 Coordinator validation을 사용하고, verdict에 따라 todo 또는 progress를 sync한다.

### Review

- Reviewer가 broad quality gate를 맡는다.
- review failure는 implementer rework로 되돌리고, spec-level failure는 planning으로 되돌린다.

### Tail

- Git Master는 validated change가 git workflow 정리를 필요로 할 때만 부른다.
- Memory Synthesizer는 durable signal이 충분할 때만 memory tail을 연다.

상세 단계, gate, escalation, drift signal은 반드시 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 먼저 따른다.

## 작업 전 참조 순서

1. 이 문서로 현재 하네스의 operating philosophy와 ownership boundary를 잡는다.
2. process detail이 필요하면 [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md)를 읽는다.
3. 서브에이전트를 고르거나 XML packet을 만들어야 하면 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)를 읽는다.
4. agent file을 새로 만들거나 고칠 때는 [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md)를 읽는다.
5. 도메인별 구현이나 리뷰 품질을 올려야 하면 아래 통합 인덱스에서 맞는 skill 또는 reference를 고른다.

## 통합 인덱스

### Instructions

| 리소스 | 왜 먼저 읽어야 하는가 |
| --- | --- |
| [.github/instructions/product-workflow.instructions.md](.github/instructions/product-workflow.instructions.md) | planning, execution, review, git, memory tail의 상세 process를 한곳에서 유지해 workflow drift를 막는다. |
| [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md) | caller-side delegation contract와 canonical packet schema를 관리해 위임 품질과 합성 일관성을 유지한다. |
| [.github/instructions/create-agent.instructions.md](.github/instructions/create-agent.instructions.md) | agent file을 수정할 때 frontmatter 호환성, 공통 섹션 구조, local workflow 책임을 지키게 만든다. |
| [.github/instructions/create-skills.instructions.md](.github/instructions/create-skills.instructions.md) | skill file을 만들거나 다듬을 때 retrieval-friendly 구조와 trigger 품질을 안정화한다. |
| [.github/instructions/typescript.instructions.md](.github/instructions/typescript.instructions.md) | TypeScript 5.x와 ES2022 기준을 흔들지 않고 코드와 설명을 맞추게 만든다. |

### Agents

| 에이전트 | 왜 이 역할이 필요한가 |
| --- | --- |
| [.github/agents/Mate.agent.md](.github/agents/Mate.agent.md) | 구현 전에 scope, evidence, askQuestions, verification을 execution-ready spec으로 고정하고 planning loop를 반복해 premature execution을 막는다. |
| [.github/agents/Explore.agent.md](.github/agents/Explore.agent.md) | local evidence를 빠르게 모아 추측 기반 수정과 불필요한 수동 탐색을 줄인다. |
| [.github/agents/Librarian.agent.md](.github/agents/Librarian.agent.md) | external contract를 공식 근거 중심으로 검증해 outdated memory나 블로그 요약 의존을 줄인다. |
| [.github/agents/Coordinator.agent.md](.github/agents/Coordinator.agent.md) | planning lane과 milestone의 fidelity를 검증해 plan drift와 verification gap을 드러낸다. |
| [.github/agents/Commander.agent.md](.github/agents/Commander.agent.md) | Fleet Mode에서 orchestration과 review/tail ownership을 분리해 coding worker와 책임 충돌을 막는다. |
| [.github/agents/Deep-execution.agent.md](.github/agents/Deep-execution.agent.md) | approved scope 안에서 구현과 verification을 끝까지 밀어 실행 continuity를 유지한다. |
| [.github/agents/Reviewer.agent.md](.github/agents/Reviewer.agent.md) | broad quality gate를 통해 correctness, regression, security, product risk를 release 전에 드러낸다. |
| [.github/agents/Git-master.agent.md](.github/agents/Git-master.agent.md) | validated change를 GitHub Flow와 팀 convention에 맞게 정리해 git tail 실수를 줄인다. |
| [.github/agents/Memory-synthesizer.agent.md](.github/agents/Memory-synthesizer.agent.md) | durable signal만 memory에 남겨 future task 품질을 높이고 memory pollution을 줄인다. |

### Skills

| 스킬 | 왜 먼저 참고해야 하는가 |
| --- | --- |
| [.github/skills/agent-browser/SKILL.md](.github/skills/agent-browser/SKILL.md) | 브라우저 상호작용을 설명이 아니라 재현 가능한 절차로 다루게 만든다. |
| [.github/skills/crafting-effective-readmes/SKILL.md](.github/skills/crafting-effective-readmes/SKILL.md) | README를 대상 독자에 맞게 구조화해 문서 품질을 높인다. |
| [.github/skills/ds-product-ux/SKILL.md](.github/skills/ds-product-ux/SKILL.md) | CTA, 빈 상태, 로딩, 확인 흐름 같은 product UX 결정을 일관되게 만든다. |
| [.github/skills/fe-a11y/SKILL.md](.github/skills/fe-a11y/SKILL.md) | interactive UI에서 accessibility를 나중 패치가 아니라 기본 설계로 끌어올린다. |
| [.github/skills/fe-code-conventions/SKILL.md](.github/skills/fe-code-conventions/SKILL.md) | naming, cohesion, readability 같은 code quality 기준을 구현 초반부터 고정한다. |
| [.github/skills/fe-code-review/SKILL.md](.github/skills/fe-code-review/SKILL.md) | frontend review를 style discussion이 아니라 correctness, pattern, a11y, performance 순으로 정리한다. |
| [.github/skills/fe-react-performance/SKILL.md](.github/skills/fe-react-performance/SKILL.md) | render cost, bundle, waterfall 문제를 뒤늦은 최적화가 아니라 설계 시점 판단으로 바꾼다. |
| [.github/skills/fe-tailwindcss/SKILL.md](.github/skills/fe-tailwindcss/SKILL.md) | Tailwind 기반 스타일링을 token, layout, merge 규칙과 함께 일관되게 유지한다. |
| [.github/skills/fe-ui-element-components/SKILL.md](.github/skills/fe-ui-element-components/SKILL.md) | shared UI component를 one-off 화면 코드와 다른 기준으로 설계하게 만든다. |
| [.github/skills/file-creator/SKILL.md](.github/skills/file-creator/SKILL.md) | memory, command, template 계열 파일을 하네스 구조에 맞게 생성하게 돕는다. |
| [.github/skills/gh-cli/SKILL.md](.github/skills/gh-cli/SKILL.md) | GitHub CLI 작업을 추측이 아닌 명시적 명령 흐름으로 바꾸어 git tail 실패를 줄인다. |
| [.github/skills/git-workflow/SKILL.md](.github/skills/git-workflow/SKILL.md) | branch, commit, PR 규칙을 팀 convention과 GitHub Flow에 맞춰 고정한다. |
| [.github/skills/pdf/SKILL.md](.github/skills/pdf/SKILL.md) | PDF 작업을 도구별 우회가 아닌 검증 가능한 변환 절차로 다룬다. |
| [.github/skills/seo-audit/SKILL.md](.github/skills/seo-audit/SKILL.md) | SEO 요청을 바로 구현하지 않고 먼저 audit 관점으로 구조화하게 만든다. |
| [.github/skills/skill-creator/SKILL.md](.github/skills/skill-creator/SKILL.md) | skill의 생성, 개선, 평가를 단순 글쓰기 대신 measurable artifact로 다루게 만든다. |
| copilot-skill:/agent-customization/SKILL.md | instruction, prompt, agent, skill 파일 자체를 다룰 때 구조와 적용 범위를 안정화한다. |
| /Users/wongeun/.vscode/extensions/github.vscode-pull-request-github-0.133.2026031004/src/lm/skills/summarize-github-issue-pr-notification/SKILL.md | issue, PR, notification 내용을 빠르게 합성해야 할 때 review context 비용을 낮춘다. |
| /Users/wongeun/.vscode/extensions/github.vscode-pull-request-github-0.133.2026031004/src/lm/skills/suggest-fix-issue/SKILL.md | issue 해결 방향을 빠르게 도출해야 할 때 initial fix space를 정리한다. |
| /Users/wongeun/.vscode/extensions/github.vscode-pull-request-github-0.133.2026031004/src/lm/skills/form-github-search-query/SKILL.md | issue나 PR 검색 요청을 정확한 GitHub query로 변환해 탐색 비용을 줄인다. |
| /Users/wongeun/.vscode/extensions/github.vscode-pull-request-github-0.133.2026031004/src/lm/skills/show-github-search-result/SKILL.md | GitHub search 결과를 human-readable table로 정리해 다음 판단을 빠르게 만든다. |
| /Users/wongeun/.vscode/extensions/ms-windows-ai-studio.windows-ai-studio-0.30.1-darwin-arm64/resources/skills/agent-workflow-builder_ai_toolkit/SKILL.md | AI agent application과 workflow 작업을 Microsoft Agent Framework 기준으로 정리한다. |

### References

| 참조 경로 | 왜 읽을 가치가 있는가 |
| --- | --- |
| [ref/AGENTS.md](ref/AGENTS.md) | reference set 내부에서 agent instruction을 어떻게 조직했는지 비교할 수 있다. |
| [ref/design.md](ref/design.md) | UI와 시스템 표현을 더 나은 설계 언어로 바꾸는 힌트를 준다. |
| [ref/project-concept.md](ref/project-concept.md) | 이 하네스가 다루려는 문제와 장기 방향을 재확인하게 만든다. |
| [ref/rule-guide.md](ref/rule-guide.md) | 규칙 충돌처럼 보이는 상황에서 보조 판단 근거를 제공한다. |
| [ref/agent-ref](ref/agent-ref) | 다양한 agent prompt 샘플을 비교해 role granularity와 workflow 표현을 개선할 수 있다. |
| [ref/create-agent-ref](ref/create-agent-ref) | create-agent 관련 예시와 서브에이전트 설계 샘플을 모아 agent authoring의 기준점을 제공한다. |
| [ref/create-skill-ref](ref/create-skill-ref) | skill authoring을 retrieval-friendly 구조로 바꾸는 예시를 제공한다. |
| [ref/hooks-ref](ref/hooks-ref) | Copilot hook과 주변 자동화 개념을 참고할 때 출발점이 된다. |
| [ref/other-harness](ref/other-harness) | 다른 harness 사례와 tradeoff를 비교해 현재 구조 결정을 검증하게 만든다. |

## 유지보수 규칙

- workflow 상세를 AGENTS.md에 다시 길게 복제하지 않는다.
- caller-side packet schema와 delegation rule은 [.github/instructions/subagent-invocation.instructions.md](.github/instructions/subagent-invocation.instructions.md)에 둔다.
- receiver-side local workflow와 cautions는 각 agent file에 둔다.
- agent와 instruction 파일의 frontmatter는 영어로, 본문은 간결한 한국어로 작성한다.
- instruction, skill, agent, reference의 인덱스는 단순 나열이 아니라 왜 필요한지 설명하는 방향으로 유지한다.
