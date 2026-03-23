# Workflow Playbook

이 문서는 하네스의 planning-to-tail 흐름을 인간용으로 설명하는 on-demand workflow reference다.
agent runtime behavior는 `.github/instructions/subagent-invocation.instructions.md`, 각 `.agent.md`, 그리고 필요한 `.github/agents/workflows/` 문서가 owner다.

## Use This Doc When

- cross-phase state transition이나 gate 해석이 필요할 때
- artifact lifecycle이나 handoff timing을 길게 확인해야 할 때
- workflow 자체를 수정하거나 ownership 경계를 재설계할 때
- local agent workflow만으로는 충분하지 않은 planning, execution, review, tail 질문이 생겼을 때

## State Model

하네스의 기본 상태는 아래 여섯 단계다.

1. Planning
2. Downstream Definition
3. Execution
4. Review
5. Git Tail
6. Memory Tail

기본 재진입 루프는 아래 네 가지다.

- Planning 안의 refinement loop
- Downstream Definition 안의 refinement loop
- Execution 또는 Review 안의 rework loop
- implementation 또는 review가 product/spec failure를 드러냈을 때의 back-to-planning loop

상태 전환 원칙은 아래와 같다.

- Planning → Downstream Definition: approved `prd.md`, coordinator-reviewed quality gate pass, explicit user alignment가 모두 있어야 한다.
- Downstream Definition → Execution: approved `prd.md`, relevant downstream artifacts, current execution brief, explicit user gate가 모두 있어야 한다.
- Execution → Review: implementation 결과와 verification evidence가 준비되어야 한다.
- Review → Git Tail: review verdict가 승인 가능한 수준이어야 한다.
- Review → Memory Tail: validated work 또는 durable signal이 있을 때만 이동한다.
- Review → Planning: local fix로 덮으면 안 되는 product/spec failure가 드러날 때 되돌아간다.

## Shared Artifacts

### `/memories/session/prd.md`

- planning phase의 source of truth다.
- findings, coordinator verdict, PRD structure가 materially change될 때마다 갱신한다.
- downstream consumer가 채팅을 다시 읽지 않고도 시작할 수 있을 정도로 self-contained 해야 한다.

### `/memories/session/references.md`

- PRD에서 참조하는 evidence의 상세 보관소다.
- Explore, Librarian, Mate 자체 조사 결과를 정리한다.

### `/memories/session/notepad.md`

- planning scratchpad다.
- 계획 초안, revision fragment, open issue를 임시로 적을 때만 쓴다.
- 공식 planning source로 취급하지 않는다.

### Optional downstream artifacts

- `/memories/session/design.md`: approved PRD를 바탕으로 visual, UX, interaction 결정을 확장한 문서다. 보통 Mate가 approved PRD briefing 뒤 user gate를 확인한 다음 Designer가 만든다.
- `/memories/session/technical.md`: approved PRD를 바탕으로 architecture, integration, technical constraint를 확장한 문서다. 보통 Mate가 approved PRD briefing 뒤 downstream mode를 확인하고, user gate가 있으면 Architector가 만든다.
- `/memories/session/handoff.md` 또는 equivalent execution brief: downstream definition phase가 execution entry를 위해 만든 문서다.

### Common Reading Order

- planning 또는 planning validation agent는 먼저 active `prd.md`를 읽는다.
- downstream definition agent는 `prd.md`를 먼저 읽고 relevant downstream artifact를 그 다음에 읽는다.
- execution agent는 current execution brief가 있으면 먼저 읽고, current `execution-plan.md`가 있으면 그 다음에 읽는다. 그 뒤 `prd.md`와 relevant downstream artifact를 읽는다.
- review agent는 current `execution-plan.md`를 먼저 읽고, 그 다음 `prd.md`, current execution brief, relevant downstream artifact(`design.md`, `technical.md`)를 reviewer_role과 changed surface에 맞게 읽는다.
- PRD, downstream artifact, execution brief 사이에 충돌이 있으면 충돌 사실부터 명시한다.

## Planning Phase

### Purpose

Planning의 목적은 user intent를 approved PRD로 바꾸는 것이다.
구현이 아니라 problem framing, target user, scope, success metric, non-goal, risks, downstream seed를 고정하는 단계다. 이 단계는 디자인 상세, technical 상세, detailed execution planning까지 직접 내려가지 않는다.

### Owner

- primary owner: Mate
- support lanes: Explore, Librarian, Coordinator

### Entry Conditions

- user request가 들어왔을 때
- 기존 plan이 invalidated 되었을 때
- execution 또는 review 결과로 back-to-planning이 필요할 때

### Detailed Loop

1. Discovery
   - local pattern, reusable template, project rule, 가까운 skill/reference를 먼저 찾는다.
   - scope, non-goal, success criteria, user intent가 흐리면 early askQuestions를 사용한다.
   - context gap, evidence gap, reference need가 보이면 Explore 또는 Librarian를 연다.
2. Clarification & Steering Questions
   - early alignment가 필요하면 askQuestions로 먼저 빈칸을 메운다.
   - drafting 중간에도 framing, tone, priority, scope, tradeoff를 더 잘 맞출 수 있으면 steering question을 쓴다.
   - steering question은 entry나 checkpoint에 묶이지 않고 planning 중 언제든 사용할 수 있다.
3. EARS 다차원 커버리지 체크
   - functional, visual-design, UX, technical, content 중 해당 차원을 식별한다.
   - 해당하는데 빠진 차원이 있으면 askQuestions로 회수한다.
4. PRD Drafting
   - approved planning output은 execution-ready plan이 아니라 PRD다.
   - Executive Summary, Problem & Evidence, Users, Strategic Context, Solution Overview, Experience Goals, Metrics, Requirements, Scope, Risks, Open Questions, Downstream Seeds를 채운다.
   - requirement section에서는 EARS를 필요한 만큼 사용하되 PRD 전체를 execution spec처럼 쓰지 않는다.
5. Council Checkpoint
   - Mate는 작업 성격에 맞는 coordinator lane을 최소 2개 동적으로 선택하고, 각 role을 분리된 Coordinator 호출로 연다.
   - Coordinator는 role-specific 기준으로 PRD clarity, scope discipline, metric quality, requirement quality, downstream ambiguity를 검토한다.
   - 필요한 경우 Explore, Librarian를 같은 wave에 붙일 수 있다.
6. Coordinator 개선 루프
   - green이면 pass한다.
   - yellow면 해당 항목을 고치고 재검토 여부를 판단한다.
   - red면 수정 후 재검토가 필수다.
7. Refinement
   - user feedback, new evidence, coordinator verdict를 반영해 PRD를 다듬는다.
   - 새로운 증거가 특정 lane만 invalidation하면 필요한 lane만 다시 연다.
8. Quality Gate & PRD Approval
   - quality gate를 통과해야 한다.
   - pass 기준은 latest revision이 coordinator-reviewed 상태이고 total 88 이상이며 critical blocker가 없는 것이다.
   - pass 후 approved PRD briefing을 user에게 보여주고 추가 refinement 필요 여부와 downstream mode를 askQuestions로 회수한다.
   - downstream mode 선택지는 `디자인만`, `기술설계만`, `둘 다`다.
   - coordinator-reviewed PRD가 준비된 시점부터 relevant guided handoff는 다음 단계로 사용할 수 있다.
   - refinement가 끝나면 `prd.md`와 `references.md`를 latest approved version으로 동기화한다.

### Outputs

- updated `prd.md`
- updated `references.md`
- optional `notepad.md`
- approved PRD briefing shown to user

### Guardrails

- implementation file edit를 시작하지 않는다.
- raw coordinator output을 그대로 user에게 전달하지 않는다.
- 질문이 필요한데도 마지막 gate까지 미루지 않는다.
- 질문이 더 좋은 draft로 이어질 수 있는데도 과질문으로 흐리지 않는다.
- PRD를 design spec, technical design, task plan으로 비대하게 만들지 않는다.

### Escalation Signals

- unresolved user choice가 quality gate를 막는다.
- external contract나 version evidence가 충돌한다.
- PRD가 current scope와 downstream seed를 충분히 덮지 못한다.

### Drift Signals

- PRD가 latest user intent와 어긋난다.
- EARS 다차원 커버리지에서 해당 차원이 빠져 있다.
- success metric, scope boundary, non-goal, risks 중 핵심 축이 다시 흐려진다.

## Downstream Definition Phase

### Purpose

Downstream Definition의 목적은 approved PRD를 기반으로 execution entry에 필요한 문서를 분리해 만드는 것이다.
대표적으로 `design.md`, `technical.md`, `handoff.md` 또는 equivalent execution brief가 여기에 속한다.

### Owner

- dedicated downstream owner가 각 문서에서 정의한다.

### Entry Conditions

- approved `prd.md`가 있다.
- user가 downstream elaboration을 원하거나 execution entry를 준비해야 한다.
- planning lane이 invalidated 상태가 아니다.

common path 중 하나는 Mate가 approved PRD briefing 뒤 askQuestions로 downstream design 필요 여부를 확인하고, user gate가 있으면 Designer를 호출해 `design.md`를 만드는 것이다.
다른 common path는 Mate가 approved PRD briefing 뒤 askQuestions로 downstream mode를 `디자인만`, `기술설계만`, `둘 다` 중 하나로 회수하고, user gate에 따라 Designer, Architector, 또는 둘 다를 다음 단계로 여는 것이다.
`기술설계만` 또는 `둘 다`가 선택되었는데 technical seed가 약하거나 architecture ambiguity가 남아 있으면 Mate가 clarification 또는 research lane을 먼저 다시 열고, 그 뒤 Architector를 호출한다.

### Outputs

- relevant downstream definition documents
- execution brief when needed

### Guardrails

- approved PRD의 product direction을 임의로 다시 쓰지 않는다.
- downstream definition 문서를 PRD와 충돌하게 만들지 않는다.
- unresolved conflict가 생기면 planning으로 되돌리거나 escalation한다.

## Research Lanes

### Explore

- local evidence, symbol flow, reusable pattern, project-specific constraint를 모을 때 쓴다.
- read-only를 유지한다.
- evidence gain이 낮아지면 멈춘다.

### Librarian

- official docs, source code, public issue/PR/discussion, 일반 웹 자료 순으로 외부 evidence를 모을 때 쓴다.
- 우선순위는 `official > source > web`이다.
- 버전이 중요하면 ambiguity를 숨기지 않는다.

### Parallel Research Rule

- 서로 독립적인 evidence need일 때만 병렬화한다.
- 결과는 raw transcript가 아니라 synthesis로 합친다.
- current revision을 sharpen하는 데 실질 가치가 있을 때만 research lane을 유지한다.

## Execution Phase

### Entry Conditions

- approved `prd.md`가 있다.
- relevant downstream artifacts가 있다.
- user gate가 성립했다.
- current execution brief가 있다.
- required planning lanes가 invalidated 상태가 아니다.

### Path

Approved execution은 Fleet Mode 경로를 따른다.

- owner: Commander
- coding worker: Deep Execution Agent
- final review orchestration: Commander

### Workflow

1. Commander가 current execution brief를 읽고, 그 다음 approved PRD와 relevant downstream artifacts를 읽어 execution context를 확보한다.
2. 독립적인 서브시스템이 여러 개면 별도 plan으로 분리할지 scope check를 한다.
3. 필요하면 Explore 또는 Librarian로 context augmentation을 한다.
4. 영향받는 파일과 책임을 file structure map으로 정리한다.
5. `.github/docs/artifacts/EXECUTION-PLAN-TEMPLATE.md`를 따라 dependency-aware execution plan을 수립하고 `/memories/session/execution-plan.md`에 저장한다. plan에는 implementation task 구조와 review strategy를 함께 남긴다. plan의 각 task를 todo 항목으로 생성한다.
6. user에게 plan verification 방식을 물어본다 (Coordinator execution role review / 자체 검증 / 건너뛰기).
7. gotcha/risk를 식별하고 필요하면 plan을 갱신한다.
8. dependency wave 기반으로 Deep Execution Agent에게 coding work를 배분한다. todo를 `in-progress`로 전환한다.
9. worker 결과를 합성하고 todo와 execution-plan.md를 갱신한다.
10. 구현 방향에 대한 확신이 흔들리거나 drift가 의심되면 Coordinator에 role-based review를 요청할 수 있다.
11. implementation 완료 후 review strategy에 따라 필요한 Reviewer `reviewer_role` call을 병렬로 열고, 마지막에 Reviewer `board` role로 final broad review를 닫는다.
12. review failure면 targeted rework를 하고 relevant reviewer_role call과 `board` gate를 다시 연다.
13. review pass 뒤 Git Tail 또는 Memory Tail 필요 여부를 판단한다.
14. orchestration summary와 todo 기반 진행률, 남은 리스크를 합성해 반환한다.

### Guardrails

- approved scope를 임의로 넓히지 않는다.
- verification evidence 없는 completion claim을 하지 않는다.
- final broad review를 건너뛰지 않는다.

### Escalation Signals

- scope expansion이 필요하다.
- local evidence만으로 blocker를 풀 수 없다.
- user choice가 필요하다.
- Coordinator 리뷰가 severe drift를 드러낸다.

### Drift Signals

- implementation이 execution brief나 approved PRD와 달라진다.
- milestone completion claim에 verification이 없다.
- execution plan의 task 상태와 실제 구현 결과가 일치하지 않는다.
- split strategy가 context fragmentation을 만든다.

## Review Phase

### Purpose

Review는 implementation 뒤의 broad quality gate다.
Commander가 reviewer_role wave를 orchestration하고, Reviewer가 role-aware review와 final `board` gate를 수행한다.
스타일보다 correctness, regression risk, security, design consistency, product impact, release readiness를 먼저 본다.

### Owner

- Reviewer
- orchestration owner는 Commander

### Inputs

- `prd.md`
- current execution brief when present
- current `execution-plan.md`
- `design.md` when present
- `technical.md` when present
- `reviewer_role`
- relevant downstream artifacts when present
- changed surface
- available evidence
- validation focus
- lane findings when `reviewer_role=board`

### Outputs

- verdict
- findings
- evidence
- risks
- next step

### Outcomes

- `approve`
- `approve-with-risks`
- `rework-required`

### Guardrails

- review 안에서 직접 구현하지 않는다.
- validation focus 밖으로 scope를 불필요하게 넓히지 않는다.
- evidence가 부족하면 부족한 evidence를 명시한다.
- `board`는 parallel lane가 아니라 final synthesis and gate 역할이다.

### Re-entry Rule

- `rework-required`면 implementer rework로 되돌린다.
- spec failure면 planning으로 되돌린다.
- `approve-with-risks`면 residual risk를 숨기지 않는다.

## Tail Phases

### Git Tail

- entry conditions: implementation과 review가 충분히 validated 되었을 때
- owner: decision owner는 Commander, actual git action owner는 Deep Execution Agent
- workflow: git state 확인, relevant skill 로드, action 실행, 결과 검증
- guardrails: `main`에 직접 커밋하지 않는다. diff와 workflow safety를 확인한다.

### Memory Tail

- entry conditions: durable signal 또는 reusable project fact가 확인되었을 때
- owner: Commander
- workflow: memory skill을 읽고, signal을 분류하고, duplication을 피한 뒤 저장 여부를 결정한다.
- guardrails: secret, credential, 민감정보, temporary task state는 저장하지 않는다.

## Packet Boundary

- subagent 호출은 `task_packet`을 쓴다.
- implementation dispatch는 `TASK_TYPE=implementation`과 required `SCOPE`, `EXECUTION_PLAN`을 포함한 `task_packet`을 쓴다.
- broad review는 `TASK_TYPE=broad-review`와 `CONTEXT` 안의 단일 `reviewer_role`를 사용한다.
- git tail과 memory tail은 dedicated subagent packet 없이 current execution owner가 관련 skill을 inline으로 읽는다.

planning source of truth는 `prd.md`다. packet field name에 legacy plan terminology가 남아 있어도 current workflow에서는 approved PRD를 가리키는 것으로 해석한다.

full packet schema와 canonical field definition은 `.github/instructions/subagent-invocation.instructions.md`가 owner다.

## Quality Gates

### Planning

- total 88 이상
- no critical blocker
- latest revision coordinator-reviewed
- explicit user alignment가 뒤따라야 한다.

### Downstream Definition

- relevant downstream artifacts가 approved PRD와 충돌하지 않아야 한다.
- execution entry가 필요하면 current execution brief가 준비되어야 한다.

### Execution

- Coordinator verdict가 있으면 반영되어야 한다.
- verification completeness가 completion claim을 뒷받침해야 한다.

### Review

- release readiness가 verdict와 residual risk에 맞아야 한다.

### Tail

- Git Tail은 workflow safety와 rule compliance가 확보되어야 한다.
- Memory Tail은 durable signal과 duplication avoidance가 확보되어야 한다.

## Common Failure Patterns

### premature execution

- planning quality gate나 user gate 전 implementation을 시작하는 경우다.
- planning으로 되돌리고 gate를 다시 세운다.

### raw review forwarding

- coordinator나 subagent 결과를 합성 없이 그대로 user에게 보여주는 경우다.
- current phase 문맥에 맞는 synthesis로 다시 정리한다.

### scope drift by convenience

- 근거보다 편의 때문에 scope를 넓히는 경우다.
- approved scope로 돌아가거나 escalation한다.

### skipped review

- 구현이 끝나 보인다는 이유로 broad review를 건너뛰는 경우다.
- review phase를 다시 연다.

### premature git tail

- validation이 불충분한데 branch, commit, PR 작업부터 시작하는 경우다.
- review 또는 execution verification으로 되돌린다.

### memory pollution

- session-only note를 durable memory로 저장하는 경우다.
- skip를 선택하고 durability 기준을 다시 확인한다.

### fragmented evidence

- 병렬 subagent를 너무 많이 열어 synthesis cost가 커진 경우다.
- 독립적인 조사만 병렬화하고 핵심 evidence만 합친다.
