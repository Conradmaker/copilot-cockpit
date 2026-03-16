---
name: "Product Workflow Core"
description: "Always-on workflow core for the agent harness. Applies to all tasks so global guardrails, artifact precedence, and workflow loading rules stay aligned."
applyTo: "**"
---

# 제품 워크플로우 코어

이 문서는 항상 로드되는 workflow core다.
장문의 phase detail, rationale, failure pattern은 `.github/docs/workflow/WORKFLOW-PLAYBOOK.md`를 필요할 때 읽는다.
receiver-local workflow는 각 `.agent.md`가, caller-side packet contract는 `.github/instructions/subagent-invocation.instructions.md`가 맡는다.

## 이 문서가 맡는 것

- global guardrail
- phase ownership과 gate의 최소 규칙
- artifact precedence와 최소 lifecycle
- workflow loading rule

## 이 문서가 맡지 않는 것

- 장문의 planning-to-tail narrative
- agent-local workflow
- packet schema의 상세 정의
- plan template 같은 artifact formatting detail

## Workflow Loading Rule

- 기본 판단 순서는 `AGENTS.md` → 관련 `.agent.md` → 필요한 instruction 순서다.
- cross-phase state transition, gate rationale, workflow redesign이 필요하면 `.github/docs/workflow/WORKFLOW-PLAYBOOK.md`를 읽는다.
- plan template, style guide, report rubric처럼 artifact format이 필요하면 `.github/docs/artifacts/` 아래 문서를 읽는다.
- simple ask나 좁은 작업은 이 문서와 관련 agent file만으로 충분하면 playbook까지 읽지 않는다.

## Global Invariants

- explicit user gate와 passed planning quality gate 없이는 planning을 approved PRD 상태로 닫지 않는다.
- approved `prd.md`와 필요한 downstream execution-entry artifacts 없이는 implementation을 시작하지 않는다.
- evidence가 충분하지 않으면 결론을 고정하지 않는다.
- context gap, evidence gap, reference need가 보이면 retrieval lane을 먼저 연다.
- user intent gap, preference gap, success criteria gap이 보이면 askQuestions로 alignment 또는 steering을 먼저 회수한다.
- invalidated lane만 다시 검증하고, 모든 lane을 기계적으로 재실행하지 않는다.
- approved handoff chain을 우회하는 shadow workflow를 만들지 않는다.
- downstream phase가 시작되기 전에는 `prd.md`와 relevant downstream artifacts를 최신 상태로 맞춘다.
- 역할 경계를 넘는 ownership theft를 허용하지 않는다.
- raw subagent output을 그대로 전달하지 않고 현재 phase 맥락에 맞게 합성한다.

## Phase Summary

### Planning

- owner: Mate
- goal: user intent를 approved PRD와 downstream seed로 수렴시킨다.
- planning 종료 전까지 quality gate와 explicit user alignment를 세운다.

### Downstream Definition

- owner: dedicated downstream owner가 각 문서에서 정의한다.
- goal: approved PRD를 기반으로 `design.md`, `technical.md`, `handoff.md` 또는 equivalent execution brief를 만든다.

### Execution

- owner: Commander
- coding worker: Deep Execution Agent
- approved scope 안에서 구현과 verification evidence를 만든다.

### Review

- owner: Reviewer
- correctness, regression risk, security, design consistency, release readiness를 broad gate로 검토한다.

### Tail

- Git Tail과 Memory Tail은 review 뒤에만 열린다.
- dedicated subagent가 아니라 current execution owner가 relevant skill을 inline으로 읽고 처리한다.

## Gate Summary

- Planning → Downstream Definition: approved `prd.md`, coordinator-reviewed quality gate pass, explicit user alignment가 있어야 한다.
- Downstream Definition → Execution: approved `prd.md`, relevant downstream artifacts, explicit user gate가 모두 있어야 한다.
- Execution → Review: implementation 결과와 verification evidence가 준비되어야 한다.
- Review → Git Tail: review verdict가 승인 가능한 수준이어야 한다.
- Review → Memory Tail: validated work 또는 durable signal이 있을 때만 간다.
- Review → Planning: local fix로 덮으면 안 되는 spec-level failure가 드러날 때 되돌린다.

## Shared Artifact Core

### `/memories/session/prd.md`

- planning phase의 source of truth다.
- materially change가 생길 때마다 갱신한다.

### `/memories/session/references.md`

- PRD에서 참조하는 evidence의 상세 보관소다.

### `/memories/session/notepad.md`

- planning scratchpad다.
- 공식 planning source로 취급하지 않는다.

### Optional downstream artifacts

- `/memories/session/design.md`
- `/memories/session/technical.md`
- `/memories/session/handoff.md` 또는 equivalent execution brief

### Reading Order

- planning 또는 planning validation agent는 먼저 active `prd.md`를 읽는다.
- downstream definition agent는 `prd.md`를 먼저 읽고 relevant downstream artifact를 그 다음에 읽는다.
- execution agent는 current execution brief가 있으면 먼저 읽고, 그 다음에 `prd.md`와 relevant downstream artifact를 읽는다.
- artifact 사이에 충돌이 있으면 충돌 사실부터 명시한다.

## Escalation Summary

- unresolved user choice가 PRD approval 또는 downstream entry gate를 막는다.
- external contract나 version evidence가 충돌한다.
- approved scope expansion이 필요하다.
- downstream execution-entry artifact가 current scope를 충분히 덮지 못한다.

## Maintenance Rule

- 이 문서는 짧고 안정적인 core만 유지한다.
- 장문의 workflow narrative는 `.github/docs/workflow/WORKFLOW-PLAYBOOK.md`에 둔다.
- artifact template와 style guide는 `.github/docs/artifacts/`에 둔다.
- agent-local behavior는 각 `.agent.md`에 둔다.
