# 워크플로 플레이북

이 문서는 하네스에서 Planning부터 Tail 단계까지 이어지는 흐름을 사람이 읽기 쉽게 정리한 참조 문서다.
에이전트의 실제 동작 규칙은 `.github/instructions/subagent-invocation.instructions.md`, 각 `.agent.md`, 필요한 `.github/agents/workflows/` 문서가 맡는다. `task_packet` schema의 정확한 정의는 `.github/instructions/subagent-invocation.instructions.md`가, execution/review output contract의 최종 기준은 각 `.agent.md`가 담당한다.

## 이 문서가 필요한 때

- phase 사이 전이 규칙이나 관문 해석이 필요할 때
- 산출물 수명 주기나 인계 시점을 길게 확인해야 할 때
- workflow 자체를 수정하거나 책임 경계를 다시 설계할 때
- 개별 agent workflow만으로는 답이 닫히지 않는 Planning, Execution, Review, Tail 질문이 생겼을 때

## 상태 모델

하네스의 기본 상태는 아래 여섯 단계다.

1. Planning
2. Downstream Definition
3. Execution
4. Review
5. Git Tail
6. Memory Tail

기본 재진입 반복은 아래 네 가지다.

- Planning 안의 refinement 반복
- Downstream Definition 안의 refinement 반복
- Execution 또는 Review 안의 rework 반복
- implementation 또는 review가 product/spec failure를 드러냈을 때 Planning으로 돌아가는 반복

상태 전환 원칙은 아래와 같다.

- Planning → Downstream Definition: 승인된 `prd.md`, Coordinator 검토를 통과한 품질 관문, 명시적 사용자 합의가 모두 있어야 한다.
- Downstream Definition → Execution: 승인된 `prd.md`, 최신 `artifacts.md`, 필요한 downstream 문서, 명시적 사용자 승인이 모두 있어야 한다. execution brief는 downstream 흐름이 실제로 만든 경우에만 진입 맥락에 포함한다.
- Execution → Review: implementation 결과와 verification evidence가 준비되어야 한다.
- Review → Git Tail: review verdict가 승인 가능한 수준이어야 한다.
- Review → Memory Tail: 검증된 작업이나 durable signal이 있을 때만 이동한다.
- Review → Planning: 국소 수정으로 덮으면 안 되는 product/spec failure가 드러날 때 되돌아간다.

## 공통 산출물

### `/memories/session/prd.md`

- Planning 단계의 기준 문서다.
- findings, Coordinator verdict, PRD 구조가 크게 바뀔 때마다 갱신한다.
- downstream에서 채팅을 다시 읽지 않아도 시작할 수 있을 정도로 문서 자체만으로 이해 가능해야 한다.

### `/memories/session/artifacts.md`

- session-wide generated document index다.
- `prd.md`가 존재하면 첫 번째 entry로 고정한다.
- 실제로 생성된 session 문서만 적고, 각 문서의 path, owner, status, 짧은 설명, open guidance를 남긴다.
- Mate는 planning phase에서 이 문서를 반드시 만들고 최신 상태로 맞춘다.

### 선택적 downstream 문서

- `/memories/session/design.md`: 승인된 PRD를 바탕으로 시각, UX, 상호작용 결정을 확장한 문서다. 보통 Mate가 승인된 PRD 요약을 보여준 뒤 사용자 승인을 확인하고 Designer가 만든다.
- `/memories/session/technical.md`: 승인된 PRD를 바탕으로 architecture, integration, technical constraint를 확장한 문서다. 보통 Mate가 승인된 PRD 요약 뒤 downstream mode를 확인하고, 사용자 승인이 있으면 Architector가 만든다.
- `/memories/session/handoff.md` 또는 같은 역할의 execution brief: Downstream Definition 단계가 Execution 진입을 위해 만든 문서다.

### 산출물 공유 원칙

- Planning 인계를 열면 기본 discovery surface로 `artifacts.md`를 함께 공유한다. `artifacts.md`에는 `prd.md`, `design.md`, `technical.md`, `handoff.md`, `execution-plan.md` 같은 session 문서 중 실제로 존재하는 파일만 포함한다.
- Commander는 Execution 진입에서 `artifacts.md`를 먼저 읽어 실행 맥락을 확보할 수 있지만, implementation/review 작업을 넘길 때는 broad artifact set을 그대로 worker에게 전달하지 않는다.
- implementation/review task packet은 generic artifact bag을 쓰지 않는다. Commander가 필요한 upstream context를 packet의 `CONTEXT`와 `EXECUTION_PLAN`에 digest로 압축한다.
- worker와 reviewer는 broad session artifact set을 다시 discovery하지 않고, packet과 current execution state만으로 시작하는 것이 기본값이다.

### 공통 읽기 순서

- Planning 또는 Planning 검증 agent는 먼저 현재 `prd.md`를 읽고, 필요하면 `artifacts.md`로 generated session 문서 상태를 확인한다.
- Downstream Definition agent는 먼저 `artifacts.md`를 읽고, 그 안에서 listed된 `prd.md`를 먼저 연다. 이후 필요한 existing downstream 문서를 읽는다.
- Execution 담당은 먼저 `artifacts.md`를 읽는다. listed된 execution brief가 있으면 그것을 우선 읽고, 없으면 listed된 `prd.md`와 필요한 downstream 문서를 Execution 계획에 필요한 만큼 읽는다. current `execution-plan.md`가 있으면 그다음에 읽는다.
- implementation worker는 current `execution-plan.md`와 packet 본문, 코드 근거만 사용한다.
- review agent는 current `execution-plan.md`를 먼저 읽고, 그다음 review task packet의 changed surface, validation focus, evidence digest를 role에 맞게 읽는다. broad session artifact set은 receiver contract가 직접 요구할 때만 연다.
- PRD, downstream 문서, execution brief, packet digest 사이에 충돌이 있으면 충돌 사실부터 먼저 적는다.

## Planning 단계

상세 Planning 다이어그램과 mode 분기는 [PLANNING-WORKFLOW.md](PLANNING-WORKFLOW.md)로 분리했다.

### 목적

Planning의 목적은 사용자 의도를 승인 가능한 PRD로 정리하는 것이다.
이 단계는 구현이 아니라 문제 정의, 대상 사용자, 범위, 성공 지표, 제외 범위, 위험, 후속 단계의 출발점을 고정하는 데 집중한다. 디자인 상세, 기술 상세, 세부 실행 계획까지 직접 내려가지 않는다.
Planning은 strict linear flow가 아니라 checkpoint-driven iteration이다. Alignment, Discovery, Draft Sync는 필요할 때마다 다시 왕복할 수 있다.

### 담당 주체

- 주 담당: Mate
- 보조 역할: Explore, Librarian, Coordinator

### 진입 조건

- 사용자 요청이 들어왔을 때
- 기존 계획이 무효화됐을 때
- Execution 또는 Review 결과로 Planning으로 돌아와야 할 때

### 상세 흐름

1. Discovery
   - 로컬 패턴, 재사용 가능한 template, 프로젝트 규칙, 가까운 skill/reference를 먼저 찾는다.
   - 범위, non-goal, 성공 기준, 사용자 의도가 흐리면 초기에 askQuestions를 사용한다.
   - 맥락 공백, 근거 공백, reference 필요가 보이면 Explore 또는 Librarian를 연다.
2. 확인 질문과 조정 질문
   - 초기에 합의가 필요하면 askQuestions로 빈칸을 먼저 메운다.
   - 초안 작성 중에도 문제 정의, tone, priority, 범위, tradeoff를 더 잘 맞출 수 있으면 steering question을 사용한다.
   - steering question은 진입 지점이나 checkpoint에 묶이지 않고 Planning 중 언제든 사용할 수 있다.
3. EARS 다차원 점검
   - functional, visual-design, UX, technical, content 중 어떤 차원이 필요한지 식별한다.
   - 필요한데 빠진 차원이 있으면 askQuestions로 회수한다.
4. PRD 작성
   - Planning의 승인 산출물은 execution-ready plan이 아니라 PRD다.
   - `Executive Summary`, `Problem & Evidence`, `Users`, `Strategic Context`, `Solution Overview`, `Experience Goals`, `Metrics`, `Requirements`, `Scope`, `Risks`, `Open Questions`, `Downstream Seeds`를 채운다.
   - requirement section에서는 EARS를 필요한 만큼 사용하되 PRD 전체를 execution spec처럼 만들지 않는다.
5. Council 검토 지점
   - Mate는 작업 성격에 맞는 Coordinator 관점을 최소 2개 고른 뒤, 각 role을 분리된 Coordinator 호출로 연다.
   - Coordinator는 role별 기준으로 PRD 명확성, 범위 통제, metric 품질, requirement 품질, downstream 모호성을 검토한다.
   - 필요하면 Explore, Librarian를 같은 wave에 붙일 수 있다.
6. Coordinator 개선 반복
   - green이면 통과한다.
   - yellow면 해당 항목을 고친 뒤 재검토가 필요한지 판단한다.
   - red면 수정 뒤 재검토가 필수다.
7. 다듬기
   - 사용자 feedback, 새로운 근거, Coordinator verdict를 반영해 PRD를 다듬는다.
   - 새로운 근거가 특정 축만 무효화하면 필요한 축만 다시 연다.
8. 품질 관문과 PRD 승인
   - 품질 관문을 통과해야 한다.
   - 통과 기준은 최신 revision이 Coordinator 검토 상태이고 total 88 이상이며 치명적 차단 요소가 없는 것이다.
   - 통과 뒤에는 승인된 PRD 요약을 사용자에게 보여주고, 추가 refinement 필요 여부를 확인한다.
   - downstream mode는 Mate가 `디자인만`, `기술설계만`, `둘 다` 중 하나로 auto-decision 한다.
   - Coordinator 검토를 마친 PRD가 준비되면 관련 안내형 인계를 다음 단계에 사용할 수 있다. 인계를 열면 최신 `artifacts.md`도 함께 공유된다.
   - 다듬기가 끝나면 `prd.md`와 `artifacts.md`를 최신 승인본으로 맞춘다.

### 출력

- 갱신된 `prd.md`
- 갱신된 `artifacts.md`
- 사용자에게 보여주는 승인된 PRD 요약
- 인계를 열었을 때 함께 전달되는 `artifacts.md`

### 제한 규칙

- implementation 파일 편집을 시작하지 않는다.
- raw Coordinator output을 그대로 사용자에게 전달하지 않는다.
- 질문이 필요한데도 마지막 관문까지 미루지 않는다.
- 더 나은 초안으로 이어질 질문을 놓치면서도, 반대로 과도한 질문으로 흐름을 흐리지 않는다.
- PRD를 design spec, technical design, task plan으로 비대하게 만들지 않는다.

### 상위 판단이 필요한 신호

- unresolved user choice가 품질 관문을 막는다.
- 외부 contract나 version evidence가 서로 충돌한다.
- PRD가 현재 범위와 downstream seed를 충분히 덮지 못한다.

### 이탈 신호

- PRD가 최신 사용자 의도와 어긋난다.
- EARS 다차원 점검에서 필요한 차원이 빠져 있다.
- success metric, 범위 경계, non-goal, 위험 중 핵심 축이 다시 흐려진다.

## Downstream Definition 단계

### 목적

Downstream Definition의 목적은 승인된 PRD를 바탕으로 Execution 진입에 필요한 문서를 분리해 만드는 것이다.
대표적으로 `design.md`, `technical.md`, `handoff.md` 또는 같은 역할의 execution brief가 여기에 속한다. execution brief는 선택 사항이며, `artifacts.md`를 대체하는 필수 문서는 아니다.

### 담당 주체

- 각 문서에서 정의한 전담 downstream 담당이 맡는다.

### 진입 조건

- 승인된 `prd.md`가 있다.
- 사용자가 downstream 상세화를 원하거나 Execution 진입을 준비해야 한다.
- Planning 흐름이 무효화된 상태가 아니다.

자주 쓰는 경로 중 하나는 Mate가 승인된 PRD 요약과 coordinator signal을 바탕으로 design elaboration 필요성을 auto-decision 하고 Designer를 호출해 `design.md`를 만드는 것이다.
또 다른 자주 쓰는 경로는 Mate가 승인된 PRD 요약 뒤 downstream mode를 `디자인만`, `기술설계만`, `둘 다` 중 하나로 auto-decision 하고, 그 판단에 따라 Designer, Architector, 또는 둘 다를 여는 것이다.
`기술설계만` 또는 `둘 다`가 결정됐는데 technical seed가 약하거나 architecture ambiguity가 남아 있으면, Mate가 clarification 또는 research 흐름을 먼저 다시 열고 그 뒤 Architector를 호출한다.

### 출력

- 필요한 downstream definition 문서
- 필요한 경우의 execution brief
- 최신 `artifacts.md`와 충돌하지 않는 Execution 진입 맥락

### 제한 규칙

- 승인된 PRD의 product direction을 임의로 다시 쓰지 않는다.
- Downstream Definition 문서를 PRD와 충돌하게 만들지 않는다.
- unresolved conflict가 생기면 Planning으로 되돌리거나 상위 판단으로 넘긴다.

## 조사 역할

### Explore

- 로컬 근거, symbol flow, 재사용 패턴, 프로젝트 고유 제약을 모을 때 쓴다.
- read-only를 유지한다.
- 얻는 근거가 더 이상 크지 않으면 멈춘다.

### Librarian

- official docs, source code, public issue/PR/discussion, 일반 웹 자료 순으로 외부 근거를 모을 때 쓴다.
- 우선순위는 `official > source > web`이다.
- 버전이 중요하면 ambiguity를 숨기지 않는다.

### 병렬 조사 원칙

- 서로 독립적인 근거 필요가 있을 때만 병렬화한다.
- Explore나 Librarian에 같은 질문을 맡긴 뒤 caller가 같은 탐색을 직접 반복하지 않는다. 맡긴 결과가 필요하면 겹치지 않는 작업만 하거나 결과를 기다린다.
- 결과는 raw transcript가 아니라 synthesis로 합친다.
- 현재 revision을 더 정확하게 만드는 데 실질 가치가 있을 때만 조사 흐름을 유지한다.

## Execution 단계

### 진입 조건

- 승인된 `prd.md`가 있다.
- 최신 `artifacts.md`가 있다.
- 필요한 downstream 문서가 준비돼 있다.
- 사용자 승인이 성립했다.
- execution brief가 있으면 Execution 진입 맥락으로 사용한다.
- 필요한 Planning 흐름이 무효화되지 않았다.

### 진행 경로

승인된 execution은 Mate handoff에 따라 두 경로 중 하나로 진행한다.

- `Fleet Mode`: Commander가 `.github/agents/artifacts/EXECUTION-PLAN-TEMPLATE.md`를 사용해 실행 계획을 만들고, Deep Execution Agent와 Reviewer를 오케스트레이션한다.
- `Rush Mode`: Mate가 built-in `Agent`로 직접 handoff한다. listed된 relevant artifacts를 함께 읽고 구현, 검증, 후속 조치를 직접 수행한다.
- Fleet Mode 담당: Commander
- Fleet Mode 구현 담당 worker: Deep Execution Agent
- Fleet Mode 선택적 asset worker: Painter
- Fleet Mode 최종 review 오케스트레이션: Commander

### 진행 순서

아래 단계는 Fleet Mode를 설명한다. Rush Mode는 built-in `Agent` direct path라 이 세부 오케스트레이션을 거치지 않는다.

1. Commander는 handoff나 user prompt를 받으면 먼저 `artifacts.md`를 읽고 listed된 execution brief가 있으면 그것을 우선 연다. execution brief가 없으면 listed된 approved PRD와 필요한 downstream 문서를 읽어 실행 맥락을 확보한다.
2. 독립적인 하위 시스템이 여러 개면 separate plan으로 나눌지 범위를 점검한다.
3. 필요하면 Explore 또는 Librarian로 맥락을 보강한다.
4. 영향받는 파일과 책임을 file structure map으로 정리한다.
5. `.github/agents/artifacts/EXECUTION-PLAN-TEMPLATE.md`에 맞춰 실행 계획을 만들고 `/memories/session/execution-plan.md`에 저장한다. plan에는 implementation task 구조, 검토 전략, packet에 압축할 digest 필드를 함께 남긴다. implementation task와 review task 모두 generic artifact bag 없이 self-contained해야 한다. plan의 각 task는 todo 항목으로 만든다.
6. `design.md`나 execution brief에 generated image asset list가 있으면 dedicated asset generation phase를 plan에 추가한다.
7. plan을 만든 뒤 gotcha와 risk를 표면화하고, Coordinator에 `execution` role review를 위임한다. review 결과를 반영해 plan과 todo를 함께 갱신한다.
8. dependency wave를 기준으로 task를 배분한다. code task는 Deep Execution Agent에, asset task는 Painter에 넘긴다. worker와 reviewer는 packet 본문과 current execution state만 사용한다. 독립 task는 같은 wave 안에서 병렬로 돌릴 수 있다.
9. worker 결과를 합성하고 todo와 `execution-plan.md`를 갱신한다.
10. 구현 방향에 대한 확신이 흔들리거나 drift가 의심되면 Coordinator에 role-based review를 요청할 수 있다.
11. implementation과 asset task가 정리되면 changed surface와 verification evidence를 기준으로 검토 전략을 갱신한다. 필요한 Reviewer role 호출을 열고 마지막에 `final-review`로 닫는다.
12. role review 결과가 모이면 Commander가 lane findings, verification evidence, residual risk를 종합해 `final-review` packet을 준비하고 마지막에 Reviewer `final-review` role로 닫는다.
13. review 실패가 나오면 무효화된 task나 wave만 다시 열어 rework하고, 관련 Reviewer role 호출과 `final-review` 관문을 다시 연다.
14. review를 통과하면 Git Tail 또는 Memory Tail이 필요한지 판단한다.
15. orchestration summary와 todo 기준 진행률, 남은 위험을 합성해 반환한다.

상세 Execution 다이어그램은 [EXECUTION-WORKFLOW.md](EXECUTION-WORKFLOW.md)로 분리했다.

### 제한 규칙

- 승인된 범위를 임의로 넓히지 않는다.
- verification evidence 없이 완료를 주장하지 않는다.
- 마지막 전반 검토를 건너뛰지 않는다.

### 상위 판단이 필요한 신호

- scope expansion이 필요하다.
- 로컬 근거만으로 blocker를 풀 수 없다.
- 사용자 선택이 필요하다.
- Coordinator review가 심한 drift를 드러낸다.

### 이탈 신호

- implementation이 execution brief나 승인된 PRD와 달라진다.
- milestone 완료 주장에 verification이 없다.
- 실행 계획의 task 상태와 실제 구현 결과가 일치하지 않는다.
- split strategy가 context fragmentation을 만든다.

## Review 단계

### 목적

Review는 implementation 뒤에 두는 넓은 품질 관문이다.
Commander가 review role wave를 orchestration하고, Reviewer가 role-aware review와 최종 `final-review` 관문을 수행한다.
스타일보다 correctness, regression risk, security, design consistency, product impact, release readiness를 먼저 본다.

### 담당 주체

- Review 담당: Reviewer
- 오케스트레이션 담당: Commander

### 입력

- current `execution-plan.md`
- review task packet이 잠근 changed surface와 evidence digest
- `prd.md`, `design.md`, `technical.md`, 그리고 execution brief가 receiver contract나 packet context에서 직접 요구되는 경우
- `review role`
- changed surface
- available evidence
- validation focus
- `ROLE=final-review`일 때의 lane findings

### 출력

- verdict
- findings
- evidence
- risks
- next step

### 결과 판정

- `approve`
- `approve-with-risks`
- `rework-required`

### 제한 규칙

- review 안에서 직접 구현하지 않는다.
- validation focus 밖으로 범위를 불필요하게 넓히지 않는다.
- evidence가 부족하면 부족하다는 사실을 명시한다.
- `final-review`는 병렬 검토 축이 아니라 최종 종합과 관문 역할이다.

### 재진입 규칙

- `rework-required`면 implementer rework로 되돌린다.
- spec failure면 Planning으로 되돌린다.
- `approve-with-risks`면 residual risk를 숨기지 않는다.

## Tail 단계

### Git Tail

- 진입 조건: implementation과 review가 충분히 검증됐을 때
- 담당: 판단은 Commander, 실제 git 작업은 Deep Execution Agent
- 흐름: git 상태 확인, relevant skill 로드, action 실행, 결과 검증
- 제한 규칙: `main`에 직접 commit하지 않는다. diff와 workflow 안전성을 확인한다.

### Memory Tail

- 진입 조건: durable signal 또는 재사용 가능한 project fact가 확인됐을 때
- 담당: Commander
- 흐름: memory skill을 읽고, signal을 분류하고, 중복을 피한 뒤 저장 여부를 결정한다.
- 제한 규칙: secret, credential, 민감 정보, temporary task state는 저장하지 않는다.

## Packet 경계

- subagent 호출은 `task_packet`을 쓴다.
- packet의 shared core는 `TASK`, `EXPECTED_OUTCOME`, `MUST_DO`, `MUST_NOT_DO`, `CONTEXT`다. 필요한 경우에만 `ROLE`, `CURRENT_DATE`, `SEARCH_STRATEGY`, `SCOPE`, `EXECUTION_PLAN`을 추가한다.
- planning과 downstream definition agent는 receiver contract에 따라 `artifacts.md`를 먼저 읽을 수 있지만, 이것은 generic packet field가 아니라 agent-local discovery 규칙이다.
- implementation dispatch는 Deep Execution Agent용 `task_packet`과 필요한 `SCOPE`, `EXECUTION_PLAN`을 포함한다. supporting context는 packet 안의 digest로 압축한다.
- role-based review는 Reviewer용 `task_packet`, 단일 `ROLE`, changed surface, validation focus, evidence digest를 포함한다.
- Git Tail과 Memory Tail은 별도 subagent packet 없이 현재 Execution 담당이 관련 skill을 바로 읽는다.

전체 packet schema와 표준 field definition의 기준 문서는 `.github/instructions/subagent-invocation.instructions.md`다.

## 품질 관문

### Planning

- total 88 이상
- 치명적 차단 요소 없음
- 최신 revision이 Coordinator 검토 상태여야 함
- 그 뒤 명시적 사용자 합의가 따라와야 함

### Downstream Definition

- 필요한 downstream 문서가 승인된 PRD와 충돌하지 않아야 한다.
- Execution 진입이 필요하면 `artifacts.md`가 최신 상태로 맞춰져 있어야 한다.
- execution brief가 필요한 경로라면 준비돼 있어야 한다.

### Execution

- Coordinator `execution` review verdict가 반영돼야 한다.
- verification completeness가 완료 주장을 뒷받침해야 한다.

### Review

- release readiness가 verdict와 residual risk에 맞아야 한다.

### Tail

- Git Tail은 workflow 안전성과 규칙 준수가 확보돼야 한다.
- Memory Tail은 durable signal과 중복 회피가 확보돼야 한다.

## 자주 생기는 실패 패턴

### premature execution

- Planning 품질 관문이나 사용자 승인 전에 implementation을 시작하는 경우다.
- Planning으로 되돌리고 관문을 다시 세운다.

### raw review forwarding

- Coordinator나 subagent 결과를 합성 없이 그대로 사용자에게 전달하는 경우다.
- 현재 phase 문맥에 맞는 synthesis로 다시 정리한다.

### scope drift by convenience

- 근거보다 편의 때문에 범위를 넓히는 경우다.
- 승인된 범위로 돌아가거나 상위 판단으로 넘긴다.

### skipped review

- 구현이 끝나 보인다는 이유로 전반 review를 건너뛰는 경우다.
- Review 단계를 다시 연다.

### premature git tail

- 검증이 충분하지 않은데 branch, commit, PR 작업부터 시작하는 경우다.
- Review 또는 Execution verification으로 되돌린다.

### memory pollution

- session에만 필요한 메모를 durable memory로 저장하는 경우다.
- 저장하지 않고 durability 기준을 다시 확인한다.

### fragmented evidence

- 병렬 subagent를 너무 많이 열어 synthesis 비용이 커진 경우다.
- 서로 독립적인 조사만 병렬화하고 핵심 근거만 합친다.
