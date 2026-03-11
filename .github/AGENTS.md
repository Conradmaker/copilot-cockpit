# .github Workflow Surface

이 디렉터리는 이 저장소의 agent operating system이다.

`agents/`, `instructions/`, `memories/`는 서로 따로 놀면 안 된다. 역할 이름, workflow 단계, memory 경로, routing 규칙이 바뀌면 관련 표면을 함께 맞춘다.

## Surface Responsibilities

- `agents/`: 개별 역할의 책임, 입력 계약, 도구 ceiling, 출력 계약을 정의한다.
- `instructions/`: routing, authoring, editing contract 같은 기계적 규칙을 정의한다.
- `memories/`: 프로젝트 수준 결정, 기술 부채, workflow 관례를 누적한다.
- `skills/`: 현재 rollout의 주 작업면이 아니다. 이 subtree 작업에서 skills는 기본적으로 수정 대상에서 제외한다.

## Editing Order

이 subtree를 수정할 때는 아래 순서를 우선한다.

1. 루트 [AGENTS.md](../AGENTS.md)에서 전체 operating model이 바뀌는지 먼저 확인한다.
2. `instructions/`에서 routing과 authoring contract를 먼저 맞춘다.
3. `agents/`에서 개별 역할의 책임과 output contract를 맞춘다.
4. memory 경로나 workflow decision이 바뀌면 `memories/`와 관련 agent 문구를 함께 맞춘다.

## Workflow Invariants

- `Mate`는 사용자-facing front door다.
- `Mate`는 planning-only 역할이며, handoff 뒤에는 종료된다.
- `Mate`는 latest coordinator-reviewed revision이 planning quality gate를 통과해 `handoff.md`가 준비되면 approved plan briefing과 함께 handoff surface를 노출할 수 있다. implementation 시작은 user gate 뒤에만 열린다.
- `Mate`가 만드는 plan과 spec은 downstream implementation consumer가 문서만 읽고도 높은 품질 결과를 낼 수 있을 정도로 자세하고 정교해야 한다.
- planning은 execution-ready spec 작성뿐 아니라 사용자 intent, scope, success condition을 특정하는 단계다.
- implementation handoff 표면은 `Fleet Mode`, `Rush Mode`, `Open in Editor` 세 가지다.
- `Coordinator`는 planning-only council이자 major milestone plan validator다.
- `Commander`는 Fleet Mode의 main implementation owner이자 execution orchestrator다.
- `Deep Execution Agent`는 명시적 implementation handoff 뒤에만 구현을 시작한다.
- `Deep Execution Agent`는 Rush Mode의 primary implementer이거나 Fleet Mode의 coding worker다.
- 구현 전 루프는 `Mate`가 사용자 intent와 scope를 특정하면서 추측보다 `manager-coord`, `product-coord`, 조사, `askQuestions`를 같은 흐름에서 반복할 수 있다.
- `manager-coord`, `product-coord`, Explore, `Librarian`는 독립적인 가치가 있으면 같은 planning wave로 병렬 호출될 수 있다.
- `Mate`, `Commander`, `Deep Execution Agent`는 자료, 레퍼런스등 정보를 얻기위해 `Explore`와 `Librarian`를 직접 호출할 수 있다.
- 구현 중에는 `Reviewer`가 기본적으로 전체 작업 종료 후 broad review를 맡고, `Coordinator`는 큰 milestone과 plan drift를 보며 execution phase milestone validation 호출일 때 해당 milestone todo/progress를 verdict에 따라 sync한다.
- `Commander`와 `Deep Execution Agent`는 Mate를 제외한 필요한 서브에이전트를 호출할 수 있다.
- `Memory-synthesizer`는 durable signal이 충분하면 사용자 확인 없이 저장할 수 있다.
- nested delegation은 허용하지만 각 레이어는 context를 압축하고 final verification owner를 명시해야 한다.
- 서브에이전트 호출 패킷은 XML로 구조화한다.

## Alignment Rules

- role 이름이 바뀌면 `AGENTS.md`, `instructions/subagent-invocation.instructions.md`, 해당 `.agent.md` 파일을 함께 수정한다.
- project memory 경로를 참조하는 문구는 `.github/memories/memories.md`로 통일한다.
- Mate gate, `askQuestions` gate, handoff 조건은 AGENTS와 instructions에서 서로 다르게 서술하지 않는다.
- agent 파일에는 철학을 과도하게 중복하지 말고, 역할과 실행 계약을 선명하게 둔다.

## Non-goals For This Rollout

- `.github/skills/` 확장
- `.github/commands/` 또는 slash command 추가
- hook automation 도입
- plan/notepad file sprawl 추가

필요 이상의 표면을 늘리기보다, 현재 workflow stack이 서로 모순 없이 맞물리도록 유지한다.
