---
description: "Guidelines for when and how the main agent should invoke subagents for specialized tasks like internal code exploration, external research, execution orchestration, and review. This document helps ensure that subagent calls are made strategically to maximize efficiency, relevance, and result quality while minimizing unnecessary overhead and context pollution."
applyTo: "**"
---

# 서브에이전트 호출 계약

이 문서는 caller-side delegation contract다.
메인 에이전트나 orchestrator가 서브에이전트를 고를 때 왜 그 역할이 필요한지, 어떤 packet을 써야 하는지, 어떤 evidence gap에서 호출 가치가 생기는지를 한곳에 정리한다.

이 문서는 phase detail을 모두 설명하는 문서가 아니다.
always-on workflow guardrail과 loading rule은 [product-workflow.instructions.md](product-workflow.instructions.md)를 따르고, planning, execution, review, git, memory tail의 장문 설명은 [../docs/workflow/WORKFLOW-PLAYBOOK.md](../docs/workflow/WORKFLOW-PLAYBOOK.md)를 필요할 때 읽는다.

## 핵심 원칙

- 한 번의 호출에는 한 가지 목표만 준다.
- caller는 raw transcript가 아니라 reuse 가능한 synthesis를 기대해야 한다.
- context gap, evidence gap, reference need, reusable pattern value, skill/reference value가 보이면 조사 lane을 여는 쪽을 먼저 검토한다.
- 근거가 부족하면 더 센 주장보다 더 좋은 조회를 우선한다.
- conflict나 version ambiguity는 숨기지 않고 packet과 결과에 남긴다.
- caller는 결과를 그대로 복붙하지 말고 현재 phase 맥락에 맞게 합성한다.

## caller-side packet 표준

모든 서브에이전트 호출은 XML packet으로 구조화한다.
`CONTEXT:` 같은 자유형 대문자 섹션을 임의로 늘리지 않고, canonical XML tag를 사용한다.

canonical packet family는 두 개만 둔다.

- `task_packet`: Explore, Librarian, Designer, Architector, Coordinator, Reviewer용 공통 packet
- `implementation_handoff_packet`: Commander, Deep Execution Agent용 execution handoff packet

### task_packet

```xml

<task_packet>
	<PHASE>{planning|execution|review|git|memory}</PHASE>
	<TASK_TYPE>{explore|research|design-definition|technical-definition|role-review|broad-review}</TASK_TYPE>
	<TASK>{single atomic goal}</TASK>
	<EXPECTED_OUTCOME>{concrete deliverables and success criteria}</EXPECTED_OUTCOME>
	<MUST_DO>{non-negotiable requirements}</MUST_DO>
	<MUST_NOT_DO>{forbidden actions and safety rails}</MUST_NOT_DO>
	<CONTEXT>{relevant background, patterns, rationale, and constraints}</CONTEXT>
	<ARTIFACTS>
		<ACTIVE_PLAN_REF>/memories/session/prd.md</ACTIVE_PLAN_REF>
		<HANDOFF_REF>/memories/session/handoff.md</HANDOFF_REF>
		<REFERENCES_REF>/memories/session/references.md</REFERENCES_REF>
	</ARTIFACTS>
	<CURRENT_DATE>{optional freshness anchor for Librarian}</CURRENT_DATE>
	<SEARCH_STRATEGY>{optional retrieval order, narrowing, and stopping rules for Explore}</SEARCH_STRATEGY>
</task_packet>
```

`ACTIVE_PLAN_REF`라는 field name은 legacy 이름이지만, current planning workflow에서는 planning source of truth인 `prd.md`를 가리키는 것으로 해석한다.

이 packet은 비실행 호출의 공통 언어다.
`TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS`가 shared core이고, `PHASE`와 `TASK_TYPE`은 최소 라우팅 메타다.
`CURRENT_DATE`와 `SEARCH_STRATEGY`는 모든 호출의 공통 필드는 아니며, 각각 Librarian와 Explore에서만 필요할 때 쓰는 optional hint다.
receiver-side field interpretation은 각 `.agent.md`에서 정의한다.

이 구조의 목적은 field fan-out을 줄이면서도 아래 정보를 잃지 않는 것이다.

- 지금 어떤 phase에 있는가
- 왜 이 호출이 필요한가
- 어떤 artifact를 먼저 읽어야 하는가
- 지금 반드시 해야 하는 것과 하면 안 되는 것이 무엇인가
- 어떤 형태의 결과를 기대하는가

### implementation_handoff_packet

downstream execution-planning owner가 Fleet Mode handoff로 execution에 넘길 때 쓴다.

```xml
<implementation_handoff_packet>
	<TASK>{execution objective}</TASK>
	<EXPECTED_OUTCOME>{expected execution summary and success criteria}</EXPECTED_OUTCOME>
	<MUST_DO>{non-negotiable execution requirements and escalation triggers}</MUST_DO>
	<MUST_NOT_DO>{forbidden behavior such as scope expansion or skipped verification}</MUST_NOT_DO>
	<CONTEXT>{why this task exists, user intent, context and rationale}</CONTEXT>
	<ARTIFACTS>
		<ACTIVE_PLAN_REF>/memories/session/prd.md</ACTIVE_PLAN_REF>
		<REFERENCES_REF>/memories/session/references.md</REFERENCES_REF>
	</ARTIFACTS>
	<SCOPE>
		<INCLUDED>{included scope}</INCLUDED>
		<EXCLUDED>{excluded scope}</EXCLUDED>
	</SCOPE>
	<EXECUTION_PLAN>{implementation strategy, work breakdown, verification contract}</EXECUTION_PLAN>
</implementation_handoff_packet>
```

이 packet의 목적은 implementer나 orchestrator가 채팅을 다시 읽지 않고도 시작하게 만드는 것이다.
execution handoff는 shared core 위에 `SCOPE`, `EXECUTION_PLAN`만 추가로 두고, execution safety에 필요한 구조를 유지한다.

### migration quick map

- old `objective`, `review_goal`, `goal` → `TASK`
- old `expected_output` or `deliverable` variants → `EXPECTED_OUTCOME`
- old `task_inputs` fan-out → `TASK`, `CONTEXT`, optional hints such as `CURRENT_DATE` or `SEARCH_STRATEGY`
- old `constraints` fan-out → `MUST_DO`, `MUST_NOT_DO`, and `CONTEXT`
- old `active_plan_ref`, `handoff_ref`, `references_ref` → `ARTIFACTS`
- old `execution_mode` → dropped (Fleet Mode path is implicit in the Commander handoff)
- old `included_scope`, `excluded_scope` → `SCOPE`
- old `implementation_strategy`, `work_breakdown`, `verification_contract` → `EXECUTION_PLAN`

## Skill-first tail work

현재 harness에서 Git Tail과 Memory Tail은 dedicated subagent surface가 아니다.

- Git Tail: current execution owner가 `.github/skills/git-workflow`와 `.github/skills/gh-cli`를 inline으로 읽고 수행한다.
- Memory Tail: current execution owner가 `.github/skills/memory-synthesizer/SKILL.md`를 inline으로 읽고 수행한다.

subagent를 새로 만들기보다, 현재 owner가 이미 가진 tool ceiling과 기존 skill surface를 우선 사용한다.

## 조사 lane 사용 원칙

### Explore

- local evidence, reusable pattern, symbol flow, project rule을 확보할 때 쓴다.
- 추측 기반 구현이나 과도한 수동 탐색을 줄이는 데 가치가 크고, planning loop 초반에 plan/spec을 sharpen하는 데도 편하게 쓸 수 있다.
- `TASK`에는 찾고 싶은 atomic question을, `EXPECTED_OUTCOME`에는 필요한 evidence shape를 적는다.
- `MUST_DO`와 `MUST_NOT_DO`에는 반드시 확인할 것과 하지 말아야 할 것을 적는다.
- `CONTEXT`에는 scope, desired thoroughness, 관련 배경을 적는다.
- `SEARCH_STRATEGY`가 필요하면 retrieval order, narrowing sequence, stopping rule을 적는다.

### Librarian

- external contract, official doc, source-level reference를 확보할 때 쓴다.
- outdated memory보다 현재 버전의 근거를 우선하게 만든다.
- `TASK`에는 research goal을, `EXPECTED_OUTCOME`에는 원하는 deliverable과 success criteria를 적는다.
- `MUST_DO`에는 `official > source > web` 같은 evidence policy와 freshness-sensitive requirement를 적는다.
- `CONTEXT`에는 target, version, relevant background를 적는다.
- 최신성 판단이 중요하면 `CURRENT_DATE`를 명시해 recency anchor를 제공한다.

### 병렬 조사

- independent evidence need일 때만 병렬화한다.
- 같은 파일과 같은 질문을 중복 조사하지 않는다.
- planning checkpoint에서는 작업 성격에 맞는 coordinator lane, Explore, Librarian를 같은 wave로 묶을 수 있다. 단, review와 evidence need가 독립적이고 current revision을 sharpen할 가치가 있을 때만 그렇다.
- coordinator lane과 research lane은 현재 revision을 sharpen할 때만 같은 wave로 묶는다.

## 에이전트 선택 인덱스

이 인덱스는 caller-side invocation 기준만 다룬다.
packet field의 세부 해석과 local workflow는 각 `.agent.md`가 owner다.

### Explore

- 역할: local codebase exploration과 evidence gathering
- 왜 필요한가: 구현 위치, 재사용 패턴, symbol flow를 빠르게 찾아 planning과 execution의 추측 비용을 줄인다.
- caller가 강조할 입력: `TASK_TYPE=explore`, shared core, 필요 시 `SEARCH_STRATEGY`
- 기대 결과: Outcome, Evidence, Implication, Open items, Next step

### Librarian

- 역할: official-first external research
- 왜 필요한가: 외부 계약과 버전 의존 동작을 현재 시점 근거로 검증해 잘못된 가정을 줄인다.
- caller가 강조할 입력: `TASK_TYPE=research`, shared core, 필요 시 `CURRENT_DATE`
- 기대 결과: Outcome, Evidence, Implication, Open items, Next step

### Coordinator

- 역할: planning council 겸 롤 기반 리뷰 카운슬
- 왜 필요한가: PRD clarity, scope discipline, requirement quality, downstream ambiguity를 독립적으로 점검해 planning drift를 줄인다. execution에서는 구현 방향에 대한 확신이 흔들리거나 drift가 의심될 때 롤 관점의 리뷰를 제공한다. coord-roles/{role}.md를 동적 로드해 role-specific 검토를 수행한다.
- caller가 강조할 입력: `TASK_TYPE=role-review`, shared core, `CONTEXT` 안의 단일 `coordinator_role`, current PRD or implementation state, decision focus, known risks, unresolved items
- 기대 결과: Verdict, Findings, Evidence, Risks, Next step

#### Coordinator 롤 선택 기준

- role 의미와 선택 기준의 상세는 `.github/agents/coord-roles/_index.md`가 owner다.
- planning에서는 Mate가 작업 성격에 맞는 role을 최소 2개 동적으로 선택하고, 각 role마다 별도 Coordinator 호출을 연다.
- 다른 phase에서는 현재 uncertainty나 drift에 직접 관련된 role만 좁게 선택한다. (병렬 호출 가능)

### Designer

- 역할: approved PRD를 `design.md`로 확장하는 downstream UI+UX design owner
- 왜 필요한가: PRD를 다시 쓰지 않고, 기존 톤앤매너와 레퍼런스를 바탕으로 visual, UX, interaction 결정을 execution 이전 문서로 구체화한다.
- caller가 강조할 입력: `TASK_TYPE=design-definition`, shared core, `CONTEXT` 안의 platform, existing tone evidence, current UI surface, current `design.md` path if present, desired depth, reference direction, user gate 상태
- 기대 결과: Status, Work summary, Evidence, Open items

### Architector

- 역할: approved PRD를 `technical.md`로 확장하는 downstream technical design owner
- 왜 필요한가: PRD를 다시 쓰지 않고, architecture, integration, stack choice, library search, technical constraints, NFR mapping을 execution 이전 문서로 구체화한다.
- caller가 강조할 입력: `TASK_TYPE=technical-definition`, shared core, `CONTEXT` 안의 current system baseline, technical seed, integration constraints, execution pressure, user gate 상태
- caller는 local precedent가 충분한지 먼저 적고, 부족하면 stack/library comparison과 evidence tier 사용을 명시한다.
- 기대 결과: Status, Work summary, Evidence, Open items

### Deep Execution Agent

- 역할: Commander-directed implementation worker
- 왜 필요한가: approved scope 안에서 focused delegated execution과 verification을 안정적으로 수행한다.
- caller가 강조할 입력: `implementation_handoff_packet`의 shared core, `SCOPE`, `EXECUTION_PLAN`
- 기대 결과: Status, Work summary, Verification, Open items, Next step

### Reviewer

- 역할: broad quality gate reviewer
- 왜 필요한가: correctness, regression risk, security, design consistency, product impact를 구현 후 단계에서 독립적으로 확인한다.
- caller가 강조할 입력: `TASK_TYPE=broad-review`, shared core, `CONTEXT` 안의 changed surface, validation focus, available evidence
- 기대 결과: Verdict, Findings, Evidence, Risks, Next step

## 병렬 위임 규칙

- 2~3개의 독립적인 호출만 병렬화한다.
- 동일한 결과를 놓고 경쟁하는 병렬 호출은 만들지 않는다.
- sequential dependency가 강하면 병렬보다 순차가 낫다.
- caller는 병렬 호출 수를 줄이는 대신 packet 품질을 높인다.

## 결과 합성 규칙

- local research는 현재 상태, 핵심 evidence, 바로 다음 액션 순으로 합성한다.
- external research는 핵심 결론, 근거 계층, 현재 작업 영향 순으로 합성한다.
- planning council은 verdict, required changes, quality lift, user gate 필요 여부 순으로 합성한다.
- execution과 review 결과는 verification, residual risk, next checkpoint를 숨기지 않고 남긴다.
- path, URL, version, uncertainty는 필요한 범위에서 함께 보존한다.

## 중단 조건

- 추가 호출이 결론을 바꾸지 않을 정도로 evidence가 충분하면 멈춘다.
- 반복되는 정보만 늘어나면 멈춘다.
- caller가 현재 phase의 다음 결정을 내릴 수 있으면 직접 마무리한다.
