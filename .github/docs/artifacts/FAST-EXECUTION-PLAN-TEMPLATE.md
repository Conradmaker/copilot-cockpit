# Fast Execution Plan Template

## 1. How to Create This Plan

- approved `prd.md`와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact를 먼저 읽는다.
- 이 template는 구조적으로 연결된 변경을 한 워커가 한 번에 밀고 갈 수 있을 때 우선 사용한다.
- Fast mode의 핵심은 병렬화가 아니라 context continuity다. 같은 feature slice, page-context, route flow, integration surface는 가능한 한 한 워커에게 묶는다.
- task를 micro-step으로 쪼개지 않는다. Fast mode의 task는 작은 구현 조각이 아니라 worker가 end-to-end로 책임질 execution bundle이어야 한다.
- split은 예외다. acceptance outcome이 둘 이상으로 갈라지거나, owned files가 명확히 분리되거나, 한 워커가 들고 가기 어려울 정도로 scope가 비대해질 때만 bundle을 나눈다.
- data contract가 필요하면 bundle을 시작하기 전에 최소 contract를 먼저 고정하되, contract를 고정한 뒤 같은 surface의 구현, 연결, 검증은 같은 bundle에 남기는 쪽을 우선한다.
- page-context-heavy UI, shared state flow, backend-to-frontend integration처럼 맥락 공유 이점이 큰 작업은 억지로 단계 분리하지 않는다.
- generated asset requirement는 blocking item일 때만 execution 안에 포함하고, optional visual polish는 기본 fast path 밖으로 민다.
- review는 기본적으로 self-check와 final `board` gate를 기준으로 잡고, specialist reviewer는 hotspot이 분명할 때만 추가한다.
- worker handoff는 짧은 task title보다 풍부한 execution brief가 더 중요하다. owned outcome, included scope, excluded scope, invariants, references, risks, validation, quality bar를 빠짐없이 적는다.
- nested handoff나 재하청식 분해를 피한다. 이미 한 bundle로 밀 수 있는 일을 중간 단계로 잘게 나누지 않는다.
- Fast mode가 맞는지 먼저 판단한다. multi-subsystem split이 필요하거나, contract ambiguity가 크거나, specialist review가 여러 개 필요하거나, one-worker ownership이 불가능하면 기본 `EXECUTION-PLAN-TEMPLATE.md`로 되돌린다.

## 2. Plan Checklist & Cautions

- [ ] approved `prd.md`와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact를 기준으로 작성했다.
- [ ] Fast mode가 실제로 맞는지 먼저 판단했고, 부적합 조건이 보이면 기본 execution plan으로 되돌리도록 기록했다.
- [ ] PRD를 다시 쓰지 않고 approved scope를 큰 execution bundle 단위로 변환했다.
- [ ] 각 bundle이 하나의 명확한 acceptance outcome을 가진다.
- [ ] 같은 feature slice나 구조적으로 연결된 surface를 불필요하게 여러 task로 쪼개지 않았다.
- [ ] split이 있다면 file ownership, outcome, or technical boundary가 분명히 갈라진다.
- [ ] 모든 task에 `depends_on`과 `validation`이 있다.
- [ ] 모든 task가 worker brief 역할을 할 만큼 충분한 지시와 reference를 포함한다.
- [ ] included scope, excluded scope, invariants, key risks, quality bar가 task 수준에서 명시된다.
- [ ] review 기본값을 self-check + final `board`로 두었고, specialist review는 hotspot 기반으로만 켰다.
- [ ] phase와 task 수를 최소화했고, process가 구현보다 더 커지지 않는다.
- [ ] risks, rollback, testing이 빠지지 않았다.
- [ ] 코딩 세부 구현까지 내려가지 않았고, 문서는 dispatch-ready execution brief 수준에 머문다.

## 3. Plan Template

```markdown
## Fast Execution Plan: {Title (2-10 words)}

{TL;DR - 무엇을 구현하는지, 어떤 connected work bundle을 어떤 one-worker strategy로 밀고 갈지 1-2문장.}

**Generated**: {Date}
**Estimated Complexity**: {Low / Medium / High}
**Status**: {planned / in-progress / completed / blocked}

**Execution Context**

- Source PRD: {path or title}
- Design ref: {path or N/A}
- Technical ref: {path or N/A}
- Additional refs: {path or N/A, ...}
- Fast mode goal: {가장 빨리 닫아야 하는 outcome}
- Why fast mode fits: {왜 이 작업이 one-worker bundle 전략에 맞는지}
- Primary worker model: {한 워커가 어떤 connected surface를 끝까지 책임지는지}
- Fallback trigger: {어떤 신호가 보이면 기본 execution plan으로 되돌리는지}
- Architecture overview: {접근 전략 1-2문장}
- Handoff quality bar: {worker가 지켜야 할 결과물 품질 기준}

## 1. File Structure Map

{영향받는 파일과 각 파일의 책임을 bundle 정의 전에 정리한다.}
이 map은 bundle ownership, context continuity, fallback trigger 판단의 기초가 된다.

| File | Responsibility | Action |
|------|---------------|--------|
| {path} | {이 파일이 맡는 책임} | {create / modify / delete} |

## 2. Scope Check

- {Fast mode는 single-worker ownership을 우선한다. 한 bundle 안에서 끝낼 수 있는 connected work는 가능한 한 붙인다.}
- {split은 file ownership, acceptance outcome, technical boundary가 분명히 갈릴 때만 허용한다.}
- {High complexity도 가능하지만, 왜 one-worker bundle이 더 유리한지와 stop condition이 명확해야 한다.}

Scope decision: {single fast bundle / fast plan with limited secondary bundle / escalate to default execution plan — 근거}

Bundle strategy:
- Primary bundle: {bundle name} — {owned outcome} — {왜 이 범위를 한 워커가 들고 가야 하는지}
- Secondary bundle: {optional, truly independent일 때만} — {owned outcome} — {왜 분리해도 context 손실이 작은지}

## 3. Review Setup

- review target surface: {어떤 변경 surface를 self-check와 final board가 볼지 요약}
- default review path: {S1 self-check -> B1 final board}
- mandatory final reviewer: `board`

### 3.1 Reviewer Role Activation

Fast mode의 기본값은 reviewer_role 생략이다.
이 section은 security, performance, frontend, design, product-integrity, code-quality hotspot이 명확할 때만 채운다.
specialist reviewer가 여러 개 필요해지면 기본 execution plan으로 전환하는 것을 우선 검토한다.

| role | Why activated for this plan | Scope | Mapped review task |
|------|------------------------------|-------|--------------------|
| {optional role or N/A} | {왜 꼭 필요한지} | {리뷰 범위} | {R1 or N/A} |

### 3.2 Final Board Gate

- inputs: {self-check evidence, optional specialist findings, residual risks}
- success criteria: {어떤 상태면 approve / approve-with-risks / rework-required인지}

## 4. Phases & Tasks
{**아래 Phase와 Task는 예시일 뿐이다. Fast mode에서는 task를 worker brief로 보고, micro-step chain 대신 큰 execution bundle을 우선한다.**}

### Phase 1: Bundle Lock

**Goal**: {가장 큰 context continuity를 유지할 primary bundle을 고정하고, worker handoff에 필요한 계약과 품질 기준을 확정한다}
**Demo/Validation**: {bundle ownership, included scope, excluded scope, fallback trigger가 명확하다}

#### T1: Lock primary execution bundle
- **depends_on**: []
- **location**: {artifact paths, primary file paths}
- **owned_outcome**: {이 bundle이 끝내야 하는 하나의 acceptance outcome}
- **included_scope**: {같이 밀고 갈 파일, surface, flow}
- **excluded_scope**: {이번 bundle에서 다루지 않을 파일, flow, polish}
- **worker_brief**: {한 워커가 어떤 순서와 관점으로 이 connected work를 밀고 가야 하는지}
- **references**: {반드시 읽어야 할 artifact와 참고 파일}
- **invariants**: {깨지면 안 되는 contract, UX, API, state rule}
- **known_risks**: {미리 알고 있는 위험과 주의점}
- **quality_bar**: {결과물 완성도 기준}
- **validation**: {bundle 정의와 contract가 handoff-ready 상태인지 확인하는 방법}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 2: Chunky Execution

**Goal**: {한 워커가 primary bundle을 end-to-end로 구현하고 연결하며 핵심 결과를 닫는다}
**Demo/Validation**: {핵심 outcome이 bundle 단위로 동작하고 관련 surface가 함께 정리된다}

#### T2: Execute primary bundle
- **depends_on**: [T1]
- **location**: {primary file paths}
- **owned_outcome**: {핵심 결과}
- **included_scope**: {같이 수정할 파일, contract, state flow, UI surface}
- **excluded_scope**: {이번 pass에서 다루지 않을 것}
- **worker_brief**: {구현, 연결, cleanup, proof gathering까지 어떤 기준으로 한 번에 처리해야 하는지}
- **references**: {artifact, existing pattern, prior precedent}
- **invariants**: {preserve해야 할 behavior와 interfaces}
- **known_risks**: {integration, regression, drift 포인트}
- **quality_bar**: {단순 동작이 아니라 어느 수준까지 매끈하게 마쳐야 하는지}
- **validation**: {bundle outcome이 성립했다는 증거}
- **status**: not-started
- **log**: {실행 후 기록}

#### T3: Execute secondary bundle (Optional)
- **depends_on**: [T2]
- **location**: {secondary file paths}
- **owned_outcome**: {primary bundle과 분리 가능한 좁은 후속 outcome}
- **included_scope**: {진짜 독립적인 후속 범위}
- **excluded_scope**: {primary bundle에 남겨야 하는 것}
- **worker_brief**: {왜 이 bundle이 따로 존재하는지와 어떤 기준으로 마무리하는지}
- **references**: {관련 artifact와 proof}
- **invariants**: {primary bundle을 깨지 않는 조건}
- **known_risks**: {bundle 간 drift 포인트}
- **quality_bar**: {추가 bundle이어도 지켜야 할 완성도 기준}
- **validation**: {secondary bundle의 결과를 확인하는 방법}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 3: Review & Validation

**Goal**: {bundle completeness를 점검하고 final board gate를 통과한다}
**Demo/Validation**: {self-check evidence와 final board verdict가 기록된다}

#### S1: Self-check
- **depends_on**: {[T2] or [T2, T3]}
- **location**: {changed files, validation outputs}
- **description**: {bundle outcome이 실제로 닫혔는지, worker brief를 충족했는지, drift와 rollback risk가 없는지 점검한다}
- **validation**: {핵심 검증 evidence, known risk, rollback readiness가 기록된다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R1: {Optional reviewer role} review
- **depends_on**: [S1]
- **location**: {hotspot surface}
- **description**: {fast mode를 유지하면서도 꼭 필요한 단일 specialist review를 수행한다}
- **validation**: {blocking issue 여부가 명확하다}
- **status**: not-started
- **log**: {실행 후 기록}

#### B1: Final board gate
- **depends_on**: {[S1] or [S1, R1]}
- **location**: {self-check summary, optional review findings, changed surface}
- **description**: {bundle outcome과 residual risk를 기준으로 final broad quality gate를 닫는다}
- **validation**: {final verdict가 approve, approve-with-risks, or rework-required로 기록된다}
- **status**: not-started
- **log**: {실행 후 기록}

{Fast mode에서는 새로운 task를 추가하기 전에 먼저 이 일이 기존 bundle 안에서 닫히는지 검토한다. 새 task는 context continuity보다 ownership clarity가 더 중요할 때만 만든다.}

## 5. Dependency Graph

{ASCII 또는 텍스트로 bundle 간 의존 관계를 시각화한다. Fast mode에서는 primary bundle이 중심이고, secondary bundle은 truly independent일 때만 추가한다.}


T1 ──> T2 ──> T3 (optional) ──> S1 ──┬──> B1
                                      └──> R1 (optional) ──> B1


## 6. Parallel Execution & Review Waves

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T1 | Immediately |
| 2 | T2 | T1 complete |
| 3 | T3 (optional) | Only if a truly independent secondary bundle remains |
| 4 | S1, R1 (optional) | Execution bundles complete |
| 5 | B1 | S1 complete and optional reviewer done |
| ... | ... | ... |

Fast mode에서 병렬화는 목표가 아니다.
같은 connected surface를 여러 워커에게 나누는 것보다, 한 워커가 context를 유지하며 끝까지 밀고 가는 편이 기본값이다.

## 7. Risks & Gotchas

- **RISK-{N}**: {위험 요소} — mitigation: {완화 방법}
- **GOTCHA-{N}**: {놓치기 쉬운 edge case 또는 pitfall}
- **FAST-EXIT-{N}**: {이 신호가 보이면 기본 execution plan으로 전환}

## 8. Rollback Plan

- {실패 시 복구 방법}
- {어떤 단계에서 fast mode를 중단하고 기본 execution plan으로 되돌릴지}
- {bundle이 실제로는 둘 이상의 subsystem으로 갈라진다는 것이 드러날 때의 대응}

## 9. Testing Strategy

- {bundle outcome을 빠르게 증명하는 검증부터 적는다: targeted run, smoke test, narrow automated test, manual proof}
- {개별 micro-step보다 end-to-end bundle completeness를 우선 검증한다}
- {high complexity인 경우 최소 하나의 stronger verification을 추가한다}
- {cheap verification조차 불가능하거나 bundle proof가 약하면 fast mode 적합성을 다시 평가한다}
```
