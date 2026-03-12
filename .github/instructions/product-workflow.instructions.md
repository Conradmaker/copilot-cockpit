---
name: "Product Workflow Playbook"
description: "Canonical planning-to-tail workflow for the agent harness. Applies to all tasks so planning, execution, review, git, and memory phases stay aligned."
applyTo: "**"
---

# 제품 워크플로우 플레이북

이 문서는 이 하네스 템플릿의 canonical workflow playbook이다.
현재 planning, execution, review, git tail, memory tail 흐름을 바꾸지 않고, 여러 파일에 흩어진 process detail을 한곳에 정리한다.

이 문서의 목적은 세 가지다.

- phase 간 전환 조건과 ownership을 흔들리지 않게 유지한다.
- 메인 에이전트와 서브에이전트가 같은 guardrail과 gate를 공유하게 만든다.
- 세부 workflow를 AGENTS.md나 개별 agent 파일에 중복해서 늘리지 않게 만든다.

AGENTS.md는 항상 보이는 요약과 통합 인덱스를 맡고, 개별 `.agent.md` 파일은 receiver-side local workflow를 맡는다.
이 문서는 그 사이에서 하네스 전체가 따라야 하는 상세 process를 정의한다.

## 핵심 운영 철학

- Prefer retrieval-led reasoning over pre-training-led reasoning.
- evidence가 부족하면 추측보다 조회를 먼저 한다.
- planning quality gate와 user gate를 통과하기 전에는 implementation으로 넘어가지 않는다.
- broad review를 건너뛰고 tail work로 바로 넘어가지 않는다.
- 현재 role boundary를 흐리지 않는다. Mate는 planning, Coordinator는 validation, Commander는 orchestration, Deep Execution Agent는 implementation, Reviewer는 review, Git Master는 git tail, Memory Synthesizer는 memory tail을 맡는다.
- process detail은 이 문서에서 관리하고, agent-local behavior는 각 `.agent.md`에서 관리한다.

## 워크플로우 상태 모델

하네스의 상태는 아래 다섯 단계로 본다.

1. Planning
2. Execution
3. Review
4. Git Tail
5. Memory Tail

재진입 루프는 아래 세 가지를 기본으로 둔다.

- Planning 안의 refinement loop
- Execution 또는 Review 안의 rework loop
- implementation 또는 review가 spec 실패를 드러냈을 때의 back-to-planning loop

각 state는 아래 원칙으로 넘어간다.

- Planning → Execution: approved plan, passed coordinator-reviewed quality gate, explicit user approval이 모두 있어야 한다.
- Execution → Review: implementation 결과와 verification evidence가 준비되어야 한다.
- Review → Git Tail: review verdict가 승인 가능 수준이어야 한다.
- Review → Memory Tail: validated work나 반복 가치가 있는 signal이 있을 때만 간다.
- Review → Planning: local fix로 덮으면 안 되는 spec-level failure가 드러날 때 되돌린다.

## 전역 불변식

아래 규칙은 phase를 가로질러 항상 유지한다.

- explicit user gate와 passed planning quality gate가 없으면 implementation을 시작하지 않는다.
- evidence가 충분하지 않으면 결론을 고정하지 않는다.
- context gap, evidence gap, reference need가 보이면 retrieval lane을 먼저 연다.
- user intent gap, preference gap, success criteria gap이 보이면 askQuestions로 alignment를 먼저 회수한다.
- invalidated planning lane만 다시 검증하고, 모든 lane을 기계적으로 재실행하지 않는다.
- 만약 quality gate를 통과했어도, user intent clarification, evidence gap, risk mitigation이 필요하면 user approval 전에 먼저 필요한 정보를 구조화해서 user에게 askQuestions를 보낸다.
- approved handoff chain을 우회하는 shadow workflow를 만들지 않는다.
- downstream phase가 시작되기 전에는 `plan.md`와 `handoff.md`를 최신 상태로 맞춘다.
- 역할 경계를 넘는 ownership theft를 허용하지 않는다.
- raw subagent output을 그대로 전달하지 않고 현재 phase 맥락에 맞게 합성한다.
- nested delegation 은 허용하지만 각 레이어는 context 를 압축하고 final verification owner 를 명시해야 한다.

## 공유 산출물과 수명주기

### `/memories/session/plan.md`

- execution-ready plan의 source of truth다.
- findings, coordinator verdict, plan structure가 materially change될 때마다 갱신한다.
- downstream execution consumer가 채팅을 다시 읽지 않고도 시작할 수 있을 정도로 구체적이어야 한다.

### `/memories/session/handoff.md`

- latest coordinator-reviewed revision이 planning quality gate를 통과한 뒤에만 생성하거나 갱신한다.
- handoff surface가 열린 뒤에도 latest `plan.md`와 sync 상태를 유지한다.
- execution-ready `implementation_handoff_packet`을 담는다.
- approved scope, verification contract, open questions, escalation policy를 잃지 않아야 한다.

### `/memories/session/notepad.md`

- Mate의 concise scratchpad다.
- 계획 초안, open issue, revision fragment를 임시로 적을 때만 쓴다.
- 공식 handoff source로 취급하지 않는다.

### phase 공통 규칙

- validation 또는 execution에 들어가는 agent는 먼저 active plan을 읽는다.
- 관련 handoff가 있으면 그 다음에 읽는다.
- plan과 handoff의 내용이 충돌하면 충돌 사실부터 명시한다.

## Planning Phase

### 목적

Planning의 목적은 user intent를 execution-ready spec으로 바꾸는 것이다.
이 단계는 구현이 아니라, scope를 고정하고 verification 가능한 plan을 만드는 단계다.
Mate는 사용자를 제외한 planning phase의 주도권을 갖고, 사용자 의도와 목적을 정확히 파악해 상세하고 구현 가능한 spec으로 수렴시킨다.

### owner

- primary owner: Mate
- support lanes: Explore, Librarian, Coordinator

### entry conditions

- user request가 들어왔거나
- 기존 plan이 invalidated 되었거나
- review 또는 execution 결과로 back-to-planning이 필요해졌을 때

### planning loop

#### 1. Discovery

- local pattern, entry point, constraint, reusable template, 가까운 rules와 skill/reference를 찾는다.
- scope, success criteria, non-goal, user intent, preference가 덜 선명하면 early askQuestions를 사용한다.
- context gap, evidence gap, reference need, reusable pattern 또는 skill/reference value가 보이면 Explore 또는 Librarian를 편하게 연다.
- Mate는 discovery를 무조건 넓게 돌리지 않고 현재 revision을 sharpen하는 데 의미 있는 조사와 질문을 우선한다.

#### 2. Council Checkpoint

- Mate는 current revision에 독립적인 검토 가치가 있으면 `manager-coord`와 `product-coord`를 같은 wave에서 병렬로 연다.
- `product-coord`는 디자이너, 개발자의 관점에서 결과물 완성도, product quality, validation, feedback, idea, 필요한 reference support를 본다.
- `manager-coord`는 plan, spec, procedure, sequencing, scope, risk, verification quality를 본다.
- same-wave 안에서 current revision을 더 예리하게 만들 independent supporting evidence가 있으면 Explore 또는 Librarian도 편하게 병렬로 붙일 수 있다.
- coordinator feedback은 raw 상태로 user에게 넘기지 않고 Mate가 합성한다.

#### 3. Design

- execution-ready spec을 쓴다.
- objective, user intent summary, included scope, excluded scope, hard constraints, evidence, steps, verification contract, risks, unresolved choices를 채운다.
- downstream implementer가 채팅을 다시 읽지 않아도 실행할 수 있을 정도의 file and symbol specificity를 유지한다.

#### 4. Refinement

- user feedback, new evidence, coordinator verdict를 반영해 plan을 다듬는다.
- critical ambiguity뿐 아니라 user intent, preference, success criteria, execution recommendation 근거가 덜 선명하면 마지막 gate까지 미루지 말고 바로 askQuestions로 정리한다.
- 현재 revision을 바꾸는 증거가 생기면 필요한 lane만 다시 검증한다.

#### 5. Quality Gate And User Gate

- planning quality gate를 먼저 통과시킨다.
- pass 기준은 latest revision이 coordinator-reviewed 상태이고, total 88 이상이며, critical blocker가 없는 것이다.
- pass 전에는 `handoff.md`를 만들지 않는다.
- pass 후에는 `handoff.md`를 만들거나 갱신하고 approved plan briefing과 함께 surfaced handoff를 연다.
- user가 명시적으로 승인하기 전에는 implementation을 시작하지 않는다.

### planning inputs

- user request
- current repository evidence
- local and external research outputs
- coordinator lane verdicts
- existing session memories if they affect scope or behavior

### planning outputs

- updated `plan.md`
- optional `notepad.md`
- `handoff.md` only after pass, surfaced when handoff-ready
- approved plan briefing shown to user

### planning role boundaries

- `Mate` 는 planning-only 역할이며, handoff 뒤에는 종료된다.
- `Mate` 가 만드는 plan 과 spec 은 downstream implementation consumer 가 문서만 읽고도 높은 품질 결과를 낼 수 있을 정도로 자세하고 정교해야 한다.
- planning 은 execution-ready spec 작성뿐 아니라 사용자 intent, scope, success condition 을 특정하는 단계다.

### planning guardrails

- implementation file edit를 시작하지 않는다.
- raw coordinator question을 그대로 user에게 전달하지 않는다.
- Mate가 final recommendation owner라는 점을 잊지 않는다.
- 질문이 필요한데도 추측으로 메우거나 마지막 gate까지 askQuestions를 미루지 않는다.
- quality gate 전에 execution mode 선택 질문으로 바로 가지 않는다.
- file path, symbol, verification이 vague해지면 refinement로 되돌린다.

### planning escalation signals

- unresolved user choice가 quality gate를 막는다.
- external contract나 version evidence가 충돌한다.
- previously passed lane을 invalidation시키는 큰 변경이 생긴다.
- verification contract가 현재 scope를 커버하지 못한다.

### planning drift signals

- spec이 latest user intent와 어긋난다.
- file and symbol specificity가 사라진다.
- verification이 선언형 문장만 있고 실제 check 방법이 없다.
- risks와 excluded scope가 비어 있다.

## Research Lane Rules

### Explore

Explore는 local evidence를 모을 때 쓴다.

- 구현 위치
- 재사용 가능한 패턴
- symbol flow
- project rules
- 가까운 AGENTS, rules, skill 문서
- planning revision을 sharpen하는 데 바로 도움이 되는 reference

Explore는 read-only를 유지한다.
새 evidence gain이 낮아지면 멈춘다.

### Librarian

Librarian는 external evidence를 모을 때 쓴다.

- 공식 문서
- migration guide
- source code reference
- public issue, PR, discussion
- general web only as supporting evidence

우선순위는 `official > source > web`이다.
버전이 중요하면 version ambiguity를 숨기지 않는다.

### 병렬 조사 규칙

- 서로 독립적인 evidence need일 때만 병렬화한다.
- 중복 검색이나 strongly dependent 단계는 순차로 둔다.
- 결과는 raw transcript가 아니라 synthesis로 합친다.
- planning wave에서는 `manager-coord`, `product-coord`, Explore, Librarian를 같은 wave로 병렬화할 수 있다. 단, 각 lane의 검토 가치와 evidence need가 독립적이고 current revision을 sharpen할 실질 가치가 있을 때만 그렇다.
- Mate는 coordinator 대기 중에도 Explore와 Librarian 결과를 합성해 다음 revision을 sharpen할 수 있다.
- Mate나 implementer가 현재 revision에 바로 반영할 수 있는 evidence만 남긴다.

## Execution Phase

### entry conditions

- approved `plan.md`가 있다.
- explicit user approval이 있다.
- current `handoff.md`가 있다.
- required planning lanes가 invalidated 상태가 아니다.

### execution modes

#### Fleet Mode

- owner: Commander
- coding worker: Deep Execution Agent
- final review orchestration: Commander

Fleet Mode는 split 또는 merge orchestration이 품질에 의미 있게 도움이 될 때 선택한다.

#### Rush Mode

- owner: Deep Execution Agent
- final review orchestration: Deep Execution Agent

Rush Mode는 context continuity와 단일 implementer 흐름이 유리할 때 선택한다.

### execution role boundaries

- `Commander` 는 Fleet Mode 의 main implementation owner 이자 execution orchestrator 다.
- `Deep Execution Agent` 는 Rush Mode 의 primary implementer 이거나 Fleet Mode 의 coding worker 다.
- `Commander` 와 `Deep Execution Agent` 는 Mate 를 제외한 필요한 서브에이전트를 호출할 수 있다.

### execution 공통 규칙

- 먼저 plan과 handoff를 읽는다.
- approved scope를 임의로 넓히지 않는다.
- missing context는 Explore 또는 Librarian로 보강한다.
- major milestone마다 Coordinator validation을 요청한다.
- Coordinator verdict 뒤에는 현재 milestone의 todo 또는 progress를 sync한다.
- verification evidence 없는 completion claim을 하지 않는다.
- final broad review를 건너뛰지 않는다.

### Fleet Mode workflow

1. Commander가 approved plan과 handoff를 읽고 execution strategy를 확정한다.
2. 필요하면 Explore 또는 Librarian로 context augmentation을 한다.
3. dependency, file overlap, interface clarity, verification cost를 기준으로 work unit을 split 또는 merge한다.
4. Deep Execution Agent worker에게 coding work를 위임한다.
5. major milestone마다 Coordinator에게 plan fidelity와 milestone boundary를 검증받고, 그 verdict에 따라 todo 또는 progress를 sync한다.
6. implementation 완료 후 Reviewer broad review를 실행한다.
7. review failure면 relevant implementer에게 focused rework를 위임하고 review를 다시 돌린다.
8. review pass 뒤 Git Tail 또는 Memory Tail 필요 여부를 판단한다.

### Rush Mode workflow

1. Deep Execution Agent가 approved plan과 handoff를 읽는다.
2. 필요하면 Explore 또는 Librarian로 missing evidence를 보강한다.
3. approved scope 안에서 직접 구현한다.
4. major milestone마다 Coordinator validation을 요청하고, 그 verdict에 따라 todo 또는 progress를 sync한다.
5. implementation 완료 후 Reviewer broad review를 실행한다.
6. review failure면 직접 수정하고 review를 다시 돈다.
7. review pass 뒤 Git Tail 또는 Memory Tail 필요 여부를 판단한다.

### execution inputs

- `handoff.md`
- `plan.md`
- latest evidence
- relevant local or external references
- coordinator milestone verdicts
- current milestone todo or progress state when validation affects tracking

### execution outputs

- changes made summary
- verification summary
- reviewer outcomes
- coordinator milestone verdicts
- todo sync status
- tail action decision
- open blockers or remaining risks

### execution guardrails

- approved scope 밖으로 나가면 escalation한다.
- Commander와 Deep Execution Agent 사이의 ownership을 섞지 않는다.
- review 전에 done이라고 선언하지 않는다.
- validated evidence 없이 tail work로 점프하지 않는다.

### execution escalation signals

- scope expansion이 필요하다.
- local evidence만으로 blocker를 풀 수 없다.
- user choice가 필요하다.
- milestone validation이 not-ready 또는 severe drift를 반환한다.

### execution drift signals

- implementation이 handoff spec과 달라진다.
- milestone completion claim에 verification이 없다.
- split strategy가 context fragmentation을 만든다.
- Commander 또는 worker가 서로의 ownership을 가져온다.

## Review Phase

### 목적

Review는 implementation 뒤의 broad quality gate다.
스타일보다 correctness, regression risk, security, design consistency, product impact, release readiness를 먼저 본다.

### owner

- Reviewer
- orchestration owner는 mode에 따라 Commander 또는 Deep Execution Agent다.

### review inputs

- `plan.md`
- `handoff.md` when present
- changed surface
- available evidence
- validation focus

### review outputs

- verdict
- validation evidence
- code and security review
- design and product review
- residual risks
- release recommendation
- follow-up needed

### review outcomes

- `approve`
- `approve-with-risks`
- `rework-required`

### review guardrails

- review 안에서 직접 구현하지 않는다.
- validation focus에 없는 영역으로 scope를 불필요하게 넓히지 않는다.
- evidence가 부족하면 부족한 evidence를 명시한다.
- orchestration ownership을 Reviewer가 가져오지 않는다.

### rework and re-entry

- `rework-required`면 main implementer로 돌린다.
- local patch보다 planning rework가 필요한 spec failure면 back-to-planning으로 보낸다.
- `approve-with-risks`는 residual risk를 숨기지 않고 release recommendation에 남긴다.

### review drift signals

- changed surface와 validation evidence가 서로 맞지 않는다.
- review가 style feedback에 과도하게 치우친다.
- residual risk가 있는데 release recommendation이 과도하게 낙관적이다.

## Git Tail Phase

### entry conditions

- implementation과 review가 git workflow action을 할 정도로 validated 되었다.
- review가 통과했거나 explicit exception이 승인되었다.

### owner

- Git Master

### git tail workflow

1. 작업 타입을 분류한다. branch, commit, PR, merge, 그 외 gh workflow task로 나눈다.
2. 관련 skill references를 먼저 읽는다.
3. 현재 git state를 먼저 확인한다.
4. GitHub Flow 규칙과 팀 convention을 확인한다.
5. branch naming, commit message, PR shape를 검증한다.
6. 작업을 실행한다.
7. 결과를 검증하고 follow-up 필요 여부를 보고한다.

### git tail inputs

- current repo state
- validated changes
- branch strategy constraints
- commit or PR requirements
- gh task requirements when relevant

### git tail outputs

- branch result
- commit result
- PR or merge result
- follow-up needed for conflict, auth, or CI blockers

### git tail guardrails

- `main`에 직접 커밋하지 않는다.
- 작업 전에 현재 상태를 확인한다.
- 가능하면 커밋 전에 diff를 다시 본다.
- 팀 convention과 GitHub Flow를 어기지 않는다.

### git tail escalation signals

- merge conflict
- permission or auth failure
- CI blocker or workflow uncertainty
- branch strategy conflict

## Memory Tail Phase

### entry conditions

- validated work 뒤에 durable signal이 남아 있거나
- 반복 가치가 높은 user preference 또는 project fact가 확인되었을 때

### owner

- Memory Synthesizer

### memory tail authority

- `Memory-synthesizer` 는 durable signal 이 충분하면 사용자 확인 없이 저장할 수 있다.

### memory tail workflow

1. session context를 분석한다.
2. candidate를 personal vs project memory로 분류한다.
3. durability와 reuse 기준으로 적격성을 판단한다.
4. weak or temporary signal은 건너뛴다.
5. 기존 memory를 읽고 duplication을 방지한다.
6. signal이 충분히 강할 때만 저장한다.

### memory tail inputs

- session outcomes
- stable user preferences
- stable project facts
- existing memory contents

### memory tail outputs

- saved items summary
- skipped items summary
- chosen scope and rationale

### memory tail guardrails

- secret, credential, sensitive data를 저장하지 않는다.
- temporary task state를 durable memory로 저장하지 않는다.
- low-confidence write보다 skip를 우선한다.
- memory pollution과 duplication을 피한다.

### memory tail escalation signals

- personal vs project classification이 모호하다.
- candidate가 current task에만 묶여 있다.
- signal strength가 약하거나 불안정하다.

## Packet And Communication Boundary

이 문서는 phase별 packet 사용 위치와 의미를 설명한다.
full packet schema와 caller-side canonical field definition은 `.github/instructions/subagent-invocation.instructions.md`에 둔다.

phase별 기본 원칙은 아래와 같다.

- planning에서 Mate는 `manager-coord`와 `product-coord` review에 `planning_review_packet`을 쓴다.
- execution handoff는 `implementation_handoff_packet`을 쓴다.
- execution milestone validation은 common envelope를 쓰되, verdict 뒤 `todo sync status`를 남길 수 있는 request와 expected output을 유지한다.
- review와 tail phase는 full schema를 복제하지 않고, 필요한 evidence fields와 expected downstream artifact만 유지한다.
- caller는 packet을 만들고, receiver는 자기 `.agent.md`에 정의된 field interpretation으로 읽는다.

## 단계별 quality gate

### Planning

- plan score total 88 이상
- no critical blocker
- latest revision coordinator-reviewed
- pass 뒤 `handoff.md`가 준비되면 mode handoff surface를 노출할 수 있다.
- explicit user approval 전에는 implementation을 시작하지 않는다.

### Execution

- milestone validation이 ready 수준이어야 한다.
- milestone verdict에 대응하는 todo sync가 최신 상태여야 한다.
- verification completeness가 completion claim을 뒷받침해야 한다.

### Review

- release readiness가 verdict와 residual risk에 맞아야 한다.

### Git Tail

- workflow safety와 rule compliance가 확보되어야 한다.

### Memory Tail

- durable signal이 충분하고 duplication avoidance가 가능해야 한다.

## 공통 실패 패턴과 대응

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
- review 또는 execution verification로 되돌린다.

### memory pollution

- session-only note를 durable memory로 저장하는 경우다.
- skip를 선택하고 durability 기준을 다시 확인한다.

### fragmented evidence

- 병렬 subagent를 너무 많이 열어 synthesis cost가 커진 경우다.
- 독립적인 조사만 병렬화하고, 핵심 evidence만 합친다.

### dropped todo sync

- execution milestone review 뒤 verdict에 맞는 todo나 progress sync를 하지 않아 추적 상태가 어긋난 경우다.
- Coordinator verdict를 받은 직후 tracking state를 먼저 맞추고 다음 단계로 넘어간다.

## 이 문서의 작성 원칙

- 규칙만 적지 말고 왜 필요한지 함께 적는다.
- negative decision tree보다 positive heuristic을 우선한다.
- ownership을 항상 드러낸다.
- phase 간 전환 조건과 escalation 신호를 숨기지 않는다.
- AGENTS.md와 개별 agent 파일이 담당할 범위를 넘겨받지 않는다.
