---
description: "Guidelines for when and how the main agent should invoke subagents for specialized tasks like internal code exploration, external research, execution orchestration, and review. This document helps ensure that subagent calls are made strategically to maximize efficiency, relevance, and result quality while minimizing unnecessary overhead and context pollution."
applyTo: "**"
---

# 서브에이전트 호출 계약

이 문서는 caller-side delegation contract다.
메인 에이전트나 orchestrator가 서브에이전트를 고를 때 왜 그 역할이 필요한지, 어떤 packet을 써야 하는지, 어떤 evidence gap에서 호출 가치가 생기는지를 한곳에 정리한다.

이 문서는 phase detail을 모두 설명하는 문서가 아니다.
runtime behavior와 phase-local workflow는 각 `.agent.md`와 필요한 `.github/agents/workflows/` 문서가 owner다.
이 문서는 caller-side packet schema와 selection rule만 다룬다.

## 핵심 원칙

- 한 번의 호출에는 한 가지 목표만 준다.
- caller는 raw transcript가 아니라 reuse 가능한 synthesis를 기대해야 한다.
- Explore나 Librarian에 같은 질문을 위임했으면 caller는 동일 탐색을 다시 직접 반복하지 않는다. delegated result가 필요하면 non-overlapping work만 하거나 결과 대기로 전환한다.
- context gap, evidence gap, reference need, reusable pattern value, skill/reference value가 보이면 조사 lane을 여는 쪽을 먼저 검토한다.
- delegation은 verification을 대체하지 않는다. completion claim은 evidence로 닫는다.
- conflict나 version ambiguity는 숨기지 않고 packet과 결과에 남긴다.
- caller는 결과를 그대로 복붙하지 말고 현재 phase 맥락에 맞게 합성한다.

## Canonical task_packet

모든 서브에이전트 호출은 XML packet으로 구조화한다.
`CONTEXT:` 같은 자유형 대문자 섹션을 임의로 늘리지 않고, canonical XML tag를 사용한다.

### task_packet

```xml

<task_packet>
	<PHASE>{planning|execution|review|git|memory}</PHASE>
	<TASK>{single atomic goal}</TASK>
	<EXPECTED_OUTCOME>{concrete deliverables and success criteria}</EXPECTED_OUTCOME>
	<MUST_DO>{non-negotiable requirements}</MUST_DO>
	<MUST_NOT_DO>{forbidden actions and safety rails}</MUST_NOT_DO>
	<CONTEXT>{relevant background, patterns, rationale, and constraints}</CONTEXT>
	<ARTIFACTS>
		<REF_1>/memories/session/prd.md</REF_1>
		<REF_2>/memories/session/**.md</REF_2>
		<REF_3>{optional additional artifact path}</REF_3>
	</ARTIFACTS>
	<ROLE>{optional role anchor for role-aware agents}</ROLE>
	<CURRENT_DATE>{optional freshness anchor for Librarian}</CURRENT_DATE>
	<SEARCH_STRATEGY>{optional retrieval order, narrowing, and stopping rules for Explore}</SEARCH_STRATEGY>
	<SCOPE>
		<INCLUDED>{optional implementation task included scope}</INCLUDED>
		<EXCLUDED>{optional implementation task excluded scope}</EXCLUDED>
	</SCOPE>
	<EXECUTION_PLAN>{optional implementation task strategy, assigned work breakdown, verification contract}</EXECUTION_PLAN>
</task_packet>
```

이 packet은 모든 subagent 호출의 공통 언어다.
호출 대상 agent는 caller가 먼저 선택하고, optional field는 그 agent의 해석을 sharpen하는 데만 사용한다.

### Shared core

- `PHASE`: 현재 호출이 어느 phase 판단 위에 있는지 잠근다.
- `TASK`: 한 번에 끝내야 할 단일 목표를 적는다.
- `EXPECTED_OUTCOME`: deliverable, success criteria, done-definition을 적는다.
- `MUST_DO`: 누락되면 안 되는 요구사항, verification expectation, safety-critical rule을 적는다.
- `MUST_NOT_DO`: scope expansion, shortcut, forbidden action을 적는다.
- `CONTEXT`: 배경, 파일/심볼 anchor, 관련 패턴, rationale, non-obvious constraint를 적는다.
- `ARTIFACTS`: caller가 현재 phase에서 receiver에게 의도적으로 열어 준 artifact/evidence ref bundle을 적는다.

### Optional fields

- `ROLE`: Coordinator나 Reviewer처럼 role-aware agent가 추가 관점을 해석할 때만 사용한다.
- `CURRENT_DATE`: Librarian의 freshness-sensitive research에서만 사용한다.
- `SEARCH_STRATEGY`: Explore의 retrieval order, narrowing, stopping rule에서만 사용한다.
- `SCOPE`: implementation task의 included/excluded scope를 잠근다.
- `EXECUTION_PLAN`: implementation task의 slice, dependency, verification expectation을 잠근다.

### Packet field semantics

- `REF_{N}`는 caller가 선택한 ordinal slot이다. field name 자체에 semantic meaning을 싣지 않고, receiver는 순서보다 현재 packet 안에 잠긴 artifact set 자체를 읽는다.
- `ARTIFACTS`에는 `/memories/session/**.md`나 review evidence처럼 현재 packet에 정말 필요한 ref만 넣는다. broad artifact bundle을 기본값으로 다시 열지 않는다.
- `ROLE`은 role-aware agent에서만 의미가 있다. current workflow에서는 Coordinator와 Reviewer가 사실상 필수 field로 해석하고, 그 외 agent는 기본적으로 무시한다.

receiver-side field interpretation은 각 `*.agent.md`에서 정의한다.

이 구조의 목적은 field fan-out을 줄이면서도 아래 정보를 잃지 않는 것이다.

- 지금 어떤 phase에 있는가
- 왜 이 호출이 필요한가
- caller가 어떤 artifact를 열어 두었는가
- 지금 반드시 해야 하는 것과 하면 안 되는 것이 무엇인가
- 어떤 형태의 결과를 기대하는가

`task_packet`은 caller가 receiver에게 작업을 전달하는 공통 입력 계약이다.

## 병렬 위임 규칙

- 2개이상의 독립적인 호출은 병렬화한다.
- 동일한 결과를 놓고 경쟁하는 병렬 호출은 만들지 않는다.
- sequential dependency가 강하면 병렬보다 순차가 낫다.
- caller는 병렬 호출 수를 줄이는 대신 packet 품질을 높인다.
- independent evidence need일 때도 병렬화한다.
- 같은 파일과 같은 질문을 중복 조사하지 않는다.
- planning checkpoint에서는 작업 성격에 맞는 reviewer lane, coordinator lane, Explore, Librarian를 같은 wave로 묶을 수 있다.

## 결과 합성 규칙

- local research는 현재 상태, 핵심 evidence, 바로 다음 액션 순으로 합성한다.
- external research는 핵심 결론, 근거 계층, 현재 작업 영향 순으로 합성한다.
- planning council은 verdict, required changes, quality lift, user gate 필요 여부 순으로 합성한다.
- execution과 review 결과는 검증 근거, 남은 리스크, next checkpoint를 숨기지 않고 남긴다.
- path, URL, version, uncertainty는 필요한 범위에서 함께 보존한다.
## 중단 조건

- 추가 호출이 결론을 바꾸지 않을 정도로 evidence가 충분하면 멈춘다.
- 반복되는 정보만 늘어나면 멈춘다.
- caller가 현재 phase의 다음 결정을 내릴 수 있으면 직접 마무리한다.
- delegated exploration 결과가 필요하지만 non-overlapping work가 더 이상 없으면, 추측으로 밀어붙이지 말고 결과 대기 상태로 전환한다.

## 에이전트 선택 인덱스

이 인덱스는 caller-side routing 기준만 다룬다.
호출 대상 agent가 receiver choice를 결정하고, optional field는 그 agent의 interpretation을 보강하는 데만 사용한다.
packet field의 세부 해석과 local workflow는 각 `*.agent.md`가 owner다.

### Explore

- 역할: 현재 워크스페이스 내부에서 local codebase evidence, reusable pattern, symbol flow, project-specific rule을 모으는 internal grep lane이다.
- 이럴 때 쓴다: 구현 위치를 찾아야 할 때, 기존 패턴을 재사용해야 할 때, 프로젝트 내부 규칙과 진입점을 검증해야 할 때.
- packet에서 강조할 것: `TASK`에는 atomic local question을, `EXPECTED_OUTCOME`에는 필요한 evidence shape를, `CONTEXT`에는 scope와 desired thoroughness를 적는다. `SEARCH_STRATEGY`는 narrowing order가 필요할 때만 붙인다. caller가 이미 본 path, symbol, failed assumption이 있으면 같이 잠가 redundant 탐색을 줄인다.
- critical guardrail: internal boundary를 벗어나지 않는다. 같은 질문을 Explore에 위임한 뒤 caller가 동일 탐색을 다시 직접 반복하지 않는다. 막연한 broad theme보다 local question을 잠가 보낸다.
- 기대 결과: `Outcome`, `Evidence`, `Implication`, `Open items`.

### Librarian

- 역할: 현재 워크스페이스 밖의 official docs, 외부 코드베이스,  source-level reference, OSS example, current public guidance를 모으는 external reference grep lane이다.
- 이럴 때 쓴다: 외부 라이브러리나 프레임워크 동작을 확인해야 할 때, official API나 migration note가 중요할 때, OSS reference나 public issue/PR/discussion이 필요할 때. 최신 외부 근거에 의해 바뀔 수 있을수록 가치가 커진다.
- packet에서 강조할 것: `TASK`에는 research goal을, `EXPECTED_OUTCOME`에는 deliverable과 success criteria를, `CONTEXT`에는 target과 version을 적는다. 최신성이 중요하면 `CURRENT_DATE`를 붙이고, `MUST_DO`에는 `official > source > web` 같은 evidence policy를 잠근다. caller가 이미 확인한 version, unresolved ambiguity, 원하는 evidence tier를 같이 잠가야 한다.
- critical guardrail: 블로그 요약이 공식 문서를 대체하지 않게 한다. external evidence tier를 섞어 신뢰도를 흐리지 않는다. vague web summary 대신 source-backed question으로 보낸다.
- 기대 결과: `Outcome`, `Evidence`, `Implication`, `Open items`.

### Coordinator

- 역할: planning과 execution에서 role-aware second opinion을 제공하는 council lane이다.
- 이럴 때 쓴다: PRD clarity, scope discipline, metric quality, execution drift, decision quality를 특정 관점에서 점검해야 할 때.
- packet에서 강조할 것: 이 agent에서는 `ROLE`이 사실상 필수다. `ROLE`에는 단일 role만 넣고, `CONTEXT`에는 current artifact state, decision focus, known risks, unresolved items를 적는다. caller는 어떤 verdict가 필요한지와 아직 잠기지 않은 tradeoff를 같이 잠가야 한다.
- critical guardrail: 한 호출에 role 하나만 준다. 역할 혼합이 필요하면 분리 호출한다. role 상세 기준은 `.github/agents/coord-roles/_index.md`가 owner다. 막연한 `한번 봐줘`보다 decision focus를 명시한다.
- 기대 결과: `Verdict`, `Findings`, `Evidence`, `Risks`, `Next step`.

### Designer

- 역할: approved PRD를 downstream `design.md`로 확장하는 UI+UX design-definition lane이다.
- 이럴 때 쓴다: 화면 구조, UX flow, visual system, interaction specification을 execution 전에 잠가야 할 때.
- packet에서 강조할 것: `CONTEXT`에는 platform, existing tone evidence, current UI surface, desired depth, reference direction을 적는다. 관련 design artifact는 `ARTIFACTS`로 보낸다. caller는 fixed constraint와 아직 열어 둔 UX question을 같이 넘겨야 한다.
- critical guardrail: PRD의 product direction을 다시 쓰지 않는다. technical architecture나 code implementation ownership을 가져오지 않는다. design decision 없이 code shape만 대신 정해 달라고 보내지 않는다.
- 기대 결과: `Status`, `Work summary`, `Evidence`, `Open items`.

### Architector

- 역할: approved PRD를 downstream `technical.md`로 확장하는 technical-definition lane이다.
- 이럴 때 쓴다: architecture pattern, integration boundary, data contract, stack choice, NFR mapping을 execution 전에 정리해야 할 때.
- packet에서 강조할 것: `CONTEXT`에는 current system baseline, technical seed, integration constraint, execution pressure를 적는다. local precedent가 약하면 그 사실을 명시한다. caller는 integration hotspot과 non-negotiable constraint를 같이 잠가야 한다.
- critical guardrail: PRD를 다시 쓰지 않는다. execution ownership과 task breakdown ownership을 가져오지 않는다. 막연한 tech review보다 잠가야 할 decision을 명시한다.
- 기대 결과: `Status`, `Work summary`, `Evidence`, `Open items`.

### Deep Execution Agent

- 역할: scoped implementation work를 실제 코드 변경과 self-verification evidence로 끝내는 implementation lane이다.
- 이럴 때 쓴다: implementation-ready brief가 있고, approved scope 안에서 actual code change를 끝내야 할 때.
- packet에서 강조할 것: `TASK`에는 atomic goal, `CONTEXT`에는 exact file/symbol anchor, `EXPECTED_OUTCOME`에는 done-definition, `MUST_DO`에는 verification expectation을 잠근다. `SCOPE`와 `EXECUTION_PLAN`은 이 agent에서는 사실상 필수다. caller는 missing scope나 spec ambiguity를 worker에게 떠넘기지 않는다.
- critical guardrail: smallest correct diff를 우선하고, explicit dispatch 없이 구현하지 않는다. verification evidence 없이 completion을 선언하지 않는다. brief가 self-contained하지 않으면 아직 dispatch-ready가 아니다.
- 기대 결과: `Status`, `Work summary`, `Verification`, `Open items`, `Next step`.

### Reviewer

- 역할: role-aware broad review와 final board gate를 담당하는 review lane이다.
- 이럴 때 쓴다: security, code-quality, design, performance, product-integrity, browser, board gate 관점의 independent review가 필요할 때.
- packet에서 강조할 것: 이 agent에서는 `ROLE`이 사실상 필수다. `ROLE`에는 단일 review role을 넣고, `CONTEXT`에는 changed surface, validation focus, available evidence를 적는다. caller는 available evidence와 risk hotspot을 같이 잠가 generic review 요청을 줄인다.
- critical guardrail: role 하나당 한 호출을 유지한다. evidence gap이 있으면 승인 대신 gap을 findings나 risks에 남긴다. `board`는 final synthesis gate로만 쓴다. evidence 없이 broad approval을 기대하지 않는다.
- 기대 결과: `Verdict`, `Findings`, `Evidence`, `Risks`, `Next step`.


