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
- 현재 role boundary를 흐리지 않는다. Mate는 planning, Coordinator는 롤 기반 validation & 리뷰, Commander는 orchestration, Deep Execution Agent는 implementation, Reviewer는 review를 맡는다. Git Tail과 Memory Tail은 dedicated subagent가 아니라 execution owner가 처리한다.
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

- Planning → Execution: approved plan, passed coordinator-reviewed quality gate, askQuestions 응답으로 handoff 실행 허용 상태가 성립하고 current `handoff.md`가 준비된 뒤 user가 handoff를 직접 실행해야 한다.
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

- planning quality gate pass + askQuestions 응답으로 handoff 실행 허용 상태가 성립한 뒤에만 생성하거나 갱신한다.
- 실행 agent를 위한 handoff-path-specific operations brief를 담는다.
- execution-ready `implementation_handoff_packet`을 포함한다.
- approved scope, verification contract, context & rationale, escalation policy를 잃지 않아야 한다.
- static handoff surface visibility는 workflow gate가 아니다. handoff 실행 허용 상태와 최신 `handoff.md`가 공식 기준이다.

### `/memories/session/references.md`

- plan에서 참조하는 evidence의 상세 내용을 보관한다.
- Explore, Librarian, Mate 자체 조사 결과를 여기에 정리한다.
- plan.md의 References & Evidence 섹션이 resource index로 이 파일을 가리킨다.

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
이 단계는 구현이 아니라, scope를 고정하고 EARS requirements와 다차원 커버리지로 verification 가능한 spec-first plan을 만드는 단계다.
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
- context gap, evidence gap, reference need가 보이면 Explore 또는 Librarian를 연다.
- 조사 결과는 `references.md`에 정리한다.
- Mate는 discovery를 무조건 넓게 돌리지 않고 현재 revision을 sharpen하는 데 의미 있는 조사와 질문을 우선한다.

#### 2. EARS 다차원 커버리지 체크

- 작업에 해당하는 차원(functional, visual-design, UX, technical, content)을 식별한다.
- 해당하는데 빠진 차원이 있으면 askQuestions로 확인한다.
- 핵심: 빠진 차원이 없는 것 > EARS 구문 완벽함.

#### 3. Council Checkpoint

- Mate는 작업 성격에 맞는 coordinator lane을 최소 2개 동적으로 선택해 병렬로 호출한다.
- lane 선택 기준: 작업 성격에 맞는 전문 영역 (예: UI → product + visual-design, 아키텍처 → manager + technical).
- Coordinator는 coord-roles/{role}.md를 동적으로 로드해 role-specific 검토를 수행한다.
- same-wave 안에서 Explore 또는 Librarian도 병렬로 붙일 수 있다.
- coordinator feedback은 raw 상태로 user에게 넘기지 않고 Mate가 합성한다.

#### 4. Coordinator 개선 루프

- green → pass, 다음 단계로.
- yellow → 해당 항목 수정. Mate가 자체 판단으로 재검토 여부 결정.
- red → 해당 항목 수정 후 재검토 필수.

#### 5. Design

- execution-ready spec을 EARS 템플릿으로 쓴다.
- Context & Rationale, Requirements (EARS), Product Spec, Design Approach, References & Evidence, Implementation Outline, Verification Contract를 채운다.
- downstream implementer가 채팅을 다시 읽지 않아도 실행할 수 있을 정도의 file and symbol specificity를 유지한다.

#### 6. Refinement

- user feedback, new evidence, coordinator verdict를 반영해 plan을 다듬는다.
- askQuestions는 어떤 시점에서든 반복해서 사용할 수 있다. 마지막 gate까지 미루지 않는다.
- 현재 revision을 바꾸는 증거가 생기면 필요한 lane만 다시 검증한다.

#### 7. Quality Gate, Handoff Choice, Handoff

- planning quality gate를 먼저 통과시킨다.
- pass 기준은 latest revision이 coordinator-reviewed 상태이고, total 88 이상이며, critical blocker가 없는 것이다.
- pass 후 approved plan briefing을 user에게 보여준다.
- askQuestions로 handoff path(Fleet Mode / Open in Editor)를 확인한다.
- handoff path가 확인되면 handoff 실행 가능으로 보고 static handoff surface visibility를 노출한다.
- 확인된 handoff path 기반으로 `handoff.md`를 작성한다.

### planning inputs

- user request
- current repository evidence
- local and external research outputs
- coordinator lane verdicts
- existing session memories if they affect scope or behavior

### planning outputs

- updated `plan.md`
- updated `references.md`
- optional `notepad.md`
- `handoff.md` only after gate pass + handoff-enabled path confirmation
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
- 유저가 handoff path를 선택하면 반드시 handoff surface를 노출하고, handoff.md를 작성한다.
- file path, symbol, verification이 vague해지면 refinement로 되돌린다.

### planning escalation signals

- unresolved user choice가 quality gate를 막는다.
- external contract나 version evidence가 충돌한다.
- previously passed lane을 invalidation시키는 큰 변경이 생긴다.
- verification contract가 현재 scope를 커버하지 못한다.

### planning drift signals

- spec이 latest user intent와 어긋난다.- EARS 다차원 커버리지에서 해당 차원이 빠져 있다.- file and symbol specificity가 사라진다.
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
- planning wave에서는 작업 성격에 맞는 coordinator lane, Explore, Librarian를 같은 wave로 병렬화할 수 있다. 단, 각 lane의 검토 가치와 evidence need가 독립적이고 current revision을 sharpen할 실질 가치가 있을 때만 그렇다.
- Mate는 coordinator 대기 중에도 Explore와 Librarian 결과를 합성해 다음 revision을 sharpen할 수 있다.
- Mate나 implementer가 현재 revision에 바로 반영할 수 있는 evidence만 남긴다.

## Execution Phase

### entry conditions

- approved `plan.md`가 있다.
- askQuestions 응답으로 handoff 실행 허용 상태가 성립했다.
- current `handoff.md`가 있다.
- required planning lanes가 invalidated 상태가 아니다.

### execution path

Approved execution always follows the Fleet Mode path.

- owner: Commander
- coding worker: Deep Execution Agent
- final review orchestration: Commander

이 경로는 모든 구현 작업에서 orchestration ownership과 coding execution을 분리해 유지한다.

### execution role boundaries

- `Commander` 는 main implementation owner 이자 execution orchestrator 다.
- `Deep Execution Agent` 는 Commander가 지휘하는 coding worker 다.
- `Commander` 와 `Deep Execution Agent` 는 Mate 를 제외한 필요한 서브에이전트를 호출할 수 있다.

### execution 공통 규칙

- 먼저 plan과 handoff를 읽는다.
- approved scope를 임의로 넓히지 않는다.
- missing context는 Explore 또는 Librarian로 보강한다.
- 구현 방향에 대한 확신이 흔들리거나 drift가 의심될 때 Coordinator에 롤을 지정해 리뷰를 요청할 수 있다.
- verification evidence 없는 completion claim을 하지 않는다.
- final broad review를 건너뛰지 않는다.

### execution workflow

1. Commander가 approved plan과 handoff를 읽고 execution strategy를 확정한다.
2. 필요하면 Explore 또는 Librarian로 context augmentation을 한다.
3. dependency, file overlap, interface clarity, verification cost를 기준으로 work unit을 split 또는 merge한다.
4. Deep Execution Agent worker에게 coding work를 위임한다.
5. 구현 방향에 대한 확신이 흔들리거나 drift가 의심될 때 Coordinator에 롤을 지정해 리뷰를 요청할 수 있다.
6. implementation 완료 후 Reviewer broad review를 실행한다.
7. review failure면 relevant implementer에게 focused rework를 위임하고 review를 다시 돌린다.
8. review pass 뒤 Git Tail 또는 Memory Tail 필요 여부를 판단한다.

### execution inputs

- `handoff.md`
- `plan.md`
- latest evidence
- relevant local or external references
- coordinator review feedback when available

### execution outputs

- status
- work summary
- verification
- open items
- next step

### execution guardrails

- approved scope 밖으로 나가면 escalation한다.
- Commander와 Deep Execution Agent 사이의 ownership을 섞지 않는다.
- review 전에 done이라고 선언하지 않는다.
- validated evidence 없이 tail work로 점프하지 않는다.

### execution escalation signals

- scope expansion이 필요하다.
- local evidence만으로 blocker를 풀 수 없다.
- user choice가 필요하다.
- Coordinator 리뷰가 severe drift를 드러낸다.

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
- orchestration owner는 Commander다.

### review inputs

- `plan.md`
- `handoff.md` when present
- changed surface
- available evidence
- validation focus

### review outputs

- verdict
- findings
- evidence
- risks
- next step

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
- `approve-with-risks`는 residual risk를 숨기지 않고 `Risks`와 `Next step`에 남긴다.

### review drift signals

- changed surface와 evidence가 서로 맞지 않는다.
- review가 style feedback에 과도하게 치우친다.
- residual risk가 있는데 verdict나 next step이 과도하게 낙관적이다.

## Git Tail Phase

### entry conditions

- implementation과 review가 git workflow action을 할 정도로 validated 되었다.
- review가 통과했거나 explicit exception이 승인되었다.

### owner

- decision owner: Commander
- actual git action owner: Deep Execution Agent

### git tail workflow

1. 작업 타입을 분류한다. branch, commit, PR, merge, 그 외 gh workflow task로 나눈다.
2. `.github/skills/git-workflow`와 `.github/skills/gh-cli`를 먼저 읽는다.
3. Commander가 현재 git state와 제약을 정리한다.
4. Commander가 actual git actions를 Deep Execution Agent에게 넘긴다.
5. branch naming, commit message, PR shape를 검증한다.
6. actual git action owner가 작업을 실행한다.
7. 결과를 검증하고 follow-up 필요 여부를 보고한다.

### git tail inputs

- current repo state
- validated changes
- branch strategy constraints
- commit or PR requirements
- gh task requirements when relevant

### git tail outputs

- status
- actions
- verification
- follow-up

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

- Commander

### memory tail authority

- current execution owner는 `.github/skills/memory-synthesizer/SKILL.md` 기준상 durable signal이 충분하면 사용자 확인 없이 저장할 수 있다.

### memory tail workflow

1. `.github/skills/memory-synthesizer/SKILL.md`와 필요한 reference를 읽는다.
2. session context를 분석한다.
3. candidate를 personal vs project memory로 분류한다.
4. durability와 reuse 기준으로 적격성을 판단한다.
5. weak or temporary signal은 건너뛴다.
6. 기존 memory를 읽고 duplication을 방지한다.
7. signal이 충분히 강할 때만 저장한다.

### memory tail inputs

- session outcomes
- stable user preferences
- stable project facts
- existing memory contents

### memory tail outputs

- status
- actions
- verification
- follow-up

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

- `task_packet`과 `implementation_handoff_packet`은 공통으로 `TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`, `ARTIFACTS` shared core를 쓴다.
- execution을 제외한 서브에이전트 호출은 `task_packet`을 쓴다.
- planning과 execution에서 Coordinator 롤 기반 리뷰는 `task_packet`에 `TASK_TYPE=role-review`로 보낸다.
- execution handoff는 `implementation_handoff_packet`을 쓴다.
- broad review는 `task_packet`에 `TASK_TYPE=broad-review`로 보낸다.
- git tail과 memory tail은 dedicated subagent packet을 만들지 않고, current execution owner가 관련 skill을 inline으로 읽어 수행한다.
- freshness-sensitive Librarian 호출에는 `CURRENT_DATE`를, retrieval planning이 중요한 Explore 호출에는 `SEARCH_STRATEGY`를 선택적으로 포함할 수 있다.
- receiver는 packet 내부의 artifact ref와 자기 `.agent.md`에 정의된 field interpretation을 함께 읽는다.
- caller는 packet을 만들고, receiver는 자기 `.agent.md`에 정의된 field interpretation으로 읽는다.

## 단계별 quality gate

### Planning

- plan score total 88 이상
- no critical blocker
- latest revision coordinator-reviewed
- pass 후 askQuestions로 mode를 확인하고 handoff 실행 허용 상태를 성립시킨 뒤 `handoff.md`를 작성한다.

### Execution

- Coordinator 리뷰 결과가 있으면 해당 verdict가 반영되어야 한다.
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

### ignored coordinator feedback

- Coordinator 리뷰 verdict를 받았지만 반영하지 않아 drift가 커진 경우다.
- Coordinator verdict를 받은 직후 해당 피드백을 구현에 반영하고 다음 단계로 넘어간다.

## 이 문서의 작성 원칙

- 규칙만 적지 말고 왜 필요한지 함께 적는다.
- negative decision tree보다 positive heuristic을 우선한다.
- ownership을 항상 드러낸다.
- phase 간 전환 조건과 escalation 신호를 숨기지 않는다.
- AGENTS.md와 개별 agent 파일이 담당할 범위를 넘겨받지 않는다.
