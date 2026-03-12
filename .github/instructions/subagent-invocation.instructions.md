---
description: "Guidelines for when and how the main agent should invoke subagents for specialized tasks like internal code exploration, external research, Git operations, and memory synthesis. This document helps ensure that subagent calls are made strategically to maximize efficiency, relevance, and result quality while minimizing unnecessary overhead and context pollution."
applyTo: "**"
---

# 서브에이전트 호출 계약

이 문서는 caller-side delegation contract다.
메인 에이전트나 orchestrator가 서브에이전트를 고를 때 왜 그 역할이 필요한지, 어떤 packet을 써야 하는지, 어떤 evidence gap에서 호출 가치가 생기는지를 한곳에 정리한다.

이 문서는 phase detail을 모두 설명하는 문서가 아니다.
planning, execution, review, git, memory tail의 상세 흐름은 [product-workflow.instructions.md](product-workflow.instructions.md)를 따른다.

## 적용 범위

- `.github/agents/` 아래 일반 서브에이전트 호출 판단에 적용한다.
- `Explore`, `Librarian`, `Coordinator`, `Commander`, `Deep Execution Agent`, `Reviewer`, `Git Master`, `Memory Synthesizer`를 다룬다.
- `.github/skills/skill-creator/agents/*` 같은 스킬 전용 에이전트는 해당 스킬 문서가 우선한다.

## 핵심 원칙

- 한 번의 호출에는 한 가지 목표만 준다.
- caller는 raw transcript가 아니라 reuse 가능한 synthesis를 기대해야 한다.
- context gap, evidence gap, reference need, reusable pattern value, skill/reference value가 보이면 조사 lane을 여는 쪽을 먼저 검토한다.
- 근거가 부족하면 더 센 주장보다 더 좋은 조회를 우선한다.
- conflict나 version ambiguity는 숨기지 않고 packet과 결과에 남긴다.
- caller는 결과를 그대로 복붙하지 말고 현재 phase 맥락에 맞게 합성한다.

## caller-side packet 표준

모든 서브에이전트 호출은 XML packet으로 구조화한다.
`CONTEXT:` 같은 자유형 대문자 섹션을 새 표준으로 쓰지 않는다.

### 공통 envelope

```xml
<packet>
	<phase>{planning|execution|review|git|memory}</phase>
	<mode>{mode-name}</mode>
	<objective>{why this call exists}</objective>
	<relevant_context>{concise context only}</relevant_context>
	<active_plan_ref>/memories/session/plan.md</active_plan_ref>
	<current_state>{current state summary}</current_state>
	<latest_evidence>{latest evidence summary}</latest_evidence>
	<request>{the concrete request}</request>
	<expected_output>{expected return shape}</expected_output>
</packet>
```

이 envelope는 phase, 현재 상태, 기대 결과를 공통 언어로 맞춘다.
receiver-side field interpretation은 각 `.agent.md`에서 정의한다.

### planning_review_packet

Mate가 Coordinator에 planning lane 검토를 요청할 때 쓴다.

```xml
<planning_review_packet>
	<phase>planning</phase>
	<mode>plan-review</mode>
	<coordinator_type>{product|manager|visual-design|technical|...}</coordinator_type>
	<planning_goal>{what this revision is trying to solve}</planning_goal>
	<current_plan_summary>{current plan summary}</current_plan_summary>
	<current_spec_state>{spec completeness state}</current_spec_state>
	<relevant_evidence>{key evidence}</relevant_evidence>
	<decision_focus>{what to critique}</decision_focus>
	<known_risks>{known risks}</known_risks>
	<unresolved_items>{unresolved user choices only}</unresolved_items>
	<recommendation_request>{what recommendation is needed}</recommendation_request>
	<expected_output>{planning review response}</expected_output>
</planning_review_packet>
```

이 packet의 목적은 coordinator에게 현재 revision의 무엇을 비판적으로 봐야 하는지 명확히 주는 것이다.
Mate는 planning checkpoint가 열리면 작업 성격에 맞는 coordinator type을 최소 2개 동적으로 선택해 병렬로 호출할 수 있다.

### implementation_handoff_packet

Mate가 Fleet Mode 또는 Rush Mode execution으로 넘길 때 쓴다.

```xml
<implementation_handoff_packet>
	<phase>execution</phase>
	<execution_mode>{fleet-mode|rush-mode}</execution_mode>
	<objective>{execution objective}</objective>
	<why_this_task_exists>{why now}</why_this_task_exists>
	<user_intent_summary>{condensed user intent}</user_intent_summary>
	<context_and_rationale>{background, purpose, scope boundary}</context_and_rationale>
	<active_plan_ref>/memories/session/plan.md</active_plan_ref>
	<spec_digest>{execution-ready spec digest}</spec_digest>
	<included_scope>{included scope}</included_scope>
	<excluded_scope>{excluded scope}</excluded_scope>
	<hard_constraints>{must not break}</hard_constraints>
	<implementation_strategy>{chosen strategy}</implementation_strategy>
	<work_breakdown>{ordered work units}</work_breakdown>
	<verification_contract>{required verification}</verification_contract>
	<latest_evidence>{latest evidence}</latest_evidence>
	<open_questions>{only user-choice items}</open_questions>
	<escalation_policy>{when to escalate}</escalation_policy>
	<expected_output>{expected execution summary}</expected_output>
</implementation_handoff_packet>
```

이 packet의 목적은 implementer나 orchestrator가 채팅을 다시 읽지 않고도 시작하게 만드는 것이다.

### review and tail phase field expectations

- review phase는 common envelope에 `change_surface`, `validation_focus`, `available_evidence`를 함께 준다.
- execution milestone validation은 current milestone 상태와 관련 todo 또는 progress 상태를 함께 주고, 결과에는 `todo_sync_status`를 기대한다.
- git tail은 common envelope에 `goal`, `repo_state`, `constraints`, `deliverable`을 분명히 준다.
- memory tail은 common envelope에 `candidates`, `save_target`, `deliverable`을 분명히 준다.

## 조사 lane 사용 원칙

### Explore

- local evidence, reusable pattern, symbol flow, project rule을 확보할 때 쓴다.
- 추측 기반 구현이나 과도한 수동 탐색을 줄이는 데 가치가 크고, planning loop 초반에 plan/spec을 sharpen하는 데도 편하게 쓸 수 있다.
- packet에서는 `question`, `scope`, `thoroughness`, `deliverable`을 또렷하게 주는 것이 중요하다.

### Librarian

- external contract, official doc, source-level reference를 확보할 때 쓴다.
- outdated memory보다 현재 버전의 근거를 우선하게 만든다.
- packet에서는 `target`, `version`, `goal`, `deliverable`, `evidence_policy`를 분명히 주는 것이 좋다.

### 병렬 조사

- independent evidence need일 때만 병렬화한다.
- 같은 파일과 같은 질문을 중복 조사하지 않는다.
- planning checkpoint에서는 작업 성격에 맞는 coordinator lane, Explore, Librarian를 같은 wave로 묶을 수 있다. 단, review와 evidence need가 독립적이고 current revision을 sharpen할 가치가 있을 때만 그렇다.
- coordinator lane과 research lane은 현재 revision을 sharpen할 때만 같은 wave로 묶는다.
- coordinator lane과 research lane은 현재 revision을 sharpen할 때만 같은 wave로 묶는다.

## 에이전트 선택 인덱스

### Explore

- 역할: local codebase exploration과 evidence gathering
- 왜 필요한가: 구현 위치, 재사용 패턴, symbol flow를 빠르게 찾아 planning과 execution의 추측 비용을 줄인다.
- caller가 강조할 입력: 찾고 싶은 질문, scope, 필요한 thoroughness, 원하는 deliverable
- 기대 결과: Answer, Evidence, Reusable patterns, Next decision support, Open uncertainties

### Librarian

- 역할: official-first external research
- 왜 필요한가: 외부 계약과 버전 의존 동작을 현재 시점 근거로 검증해 잘못된 가정을 줄인다.
- caller가 강조할 입력: target, version, goal, deliverable, evidence policy
- 기대 결과: Answer, Evidence by tier, Recommended usage or implication, Decision impact, Open uncertainties

### Coordinator

- 역할: dynamic planning council과 major milestone validator
- 왜 필요한가: plan fidelity, verification gap, decomposition risk를 독립적으로 점검해 planning drift를 줄인다. coord-types/{type}.md를 동적 로드해 type-specific 검토를 수행한다.
- caller가 강조할 입력: `coordinator_type` (product, manager, visual-design, technical 등), current plan summary, decision focus, known risks, unresolved items, execution milestone일 때는 current todo 또는 progress state
- 기대 결과: Council verdict, Required changes, Quality lift ideas, Evidence, Questions for main agent or user, milestone-related sections, Todo sync status

### Commander

- 역할: Fleet Mode execution orchestrator
- 왜 필요한가: coding worker와 orchestration ownership을 분리해 split, merge, review, tail 판단을 더 안정적으로 수행한다.
- caller가 강조할 입력: approved plan, implementation strategy, work breakdown, verification contract, escalation policy
- 기대 결과: Execution verdict, Orchestration summary, Worker results, Reviewer outcomes, Coordinator milestone verdicts, Tail actions

### Deep Execution Agent

- 역할: Rush Mode primary implementer 또는 Fleet worker
- 왜 필요한가: approved scope 안에서 continuity를 유지하며 구현과 verification을 끝까지 밀어붙인다.
- caller가 강조할 입력: execution mode, assigned scope, verification contract, open questions, escalation policy
- 기대 결과: Status, Changes made, Verification, Reviewer outcomes, Coordinator milestone verdicts, Need from Commander, Coordinator, or main agent

### Reviewer

- 역할: broad quality gate reviewer
- 왜 필요한가: correctness, regression risk, security, design consistency, product impact를 구현 후 단계에서 독립적으로 확인한다.
- caller가 강조할 입력: changed surface, validation focus, available evidence
- 기대 결과: Verdict, Validation evidence, Code and security review, Design and product review, Residual risks, Release recommendation, Follow-up needed

### Git Master

- 역할: git tail specialist
- 왜 필요한가: validated change를 GitHub Flow, commit convention, gh workflow 기준에 맞게 정리해 git 실수를 줄인다.
- caller가 강조할 입력: goal, current repo state, branch or PR constraints, deliverable
- 기대 결과: branch or commit or PR result, verification summary, follow-up needed for conflicts or failures

### Memory Synthesizer

- 역할: memory tail specialist
- 왜 필요한가: durable signal만 personal 또는 project memory에 남겨 future task 품질을 높이고 memory pollution을 줄인다.
- caller가 강조할 입력: candidate items, save target intent, why these signals seem durable
- 기대 결과: saved items summary, skipped items summary, chosen scope and rationale

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
