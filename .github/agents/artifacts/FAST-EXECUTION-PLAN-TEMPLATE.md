# Fast Execution Plan Template

## 1. How to Create This Plan

- approved `prd.md` 와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact 를 먼저 읽는다.
- 이 template 는 구조적으로 연결된 변경을 한 워커가 한 번에 밀고 갈 수 있을 때 우선 사용한다.
- Fast mode 의 핵심은 병렬화가 아니라 context continuity 다. 같은 feature slice, page-context, route flow, integration surface 는 가능한 한 한 워커에게 묶는다.
- task 를 micro-step 으로 쪼개지 않는다. Fast mode 의 task 는 작은 구현 조각이 아니라 worker 가 end-to-end 로 책임질 execution bundle 이어야 한다.
- split 은 예외다. acceptance outcome 이 둘 이상으로 갈라지거나, owned files 가 명확히 분리되거나, 한 워커가 들고 가기 어려울 정도로 scope 가 비대해질 때만 bundle 을 나눈다.
- data contract 가 필요하면 bundle 을 시작하기 전에 최소 contract 를 먼저 고정하되, contract 를 고정한 뒤 같은 surface 의 구현, 연결, 검증은 같은 bundle 에 남기는 쪽을 우선한다.
- page-context-heavy UI, shared state flow, backend-to-frontend integration 처럼 맥락 공유 이점이 큰 작업은 억지로 단계 분리하지 않는다.
- generated asset requirement 는 blocking item 일 때만 execution 안에 포함하고, optional visual polish 는 기본 fast path 밖으로 민다.
- review 는 기본적으로 self-check 와 final `board` gate 를 기준으로 잡고, specialist reviewer 는 hotspot 이 분명할 때만 추가한다.
- Fast mode 가 맞는지 먼저 판단한다. multi-subsystem split 이 필요하거나, contract ambiguity 가 크거나, specialist review 가 여러 개 필요하거나, one-worker ownership 이 불가능하면 기본 `EXECUTION-PLAN-TEMPLATE.md`로 되돌린다.

## 2. Plan Checklist & Cautions

- [ ] approved `prd.md` 와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact 를 기준으로 작성했다.
- [ ] Fast mode 가 실제로 맞는지 먼저 판단했고, 부적합 조건이 보이면 기본 execution plan 으로 되돌리도록 기록했다.
- [ ] PRD 를 다시 쓰지 않고 approved scope 를 큰 execution bundle 단위로 변환했다.
- [ ] 각 bundle 이 하나의 명확한 acceptance outcome 을 가진다.
- [ ] 같은 feature slice 나 구조적으로 연결된 surface 를 불필요하게 여러 task 로 쪼개지 않았다.
- [ ] split 이 있다면 file ownership, outcome, or technical boundary 가 분명히 갈라진다.
- [ ] 모든 task 에 `depends_on`과 appropriate validation field 가 있다. implementation bundle task 는 `verification_expectation`, review task 는 `validation`을 사용한다.
- [ ] 모든 task 가 worker brief 역할을 할 만큼 충분한 지시와 reference 를 포함한다.
- [ ] implementation bundle task 의 `artifacts` 는 `string[]` 로 직접 기술했고, packet 본문만으로 충분하면 `[]` 로 유지해 context isolation 을 지켰다.
- [ ] review task 의 `artifacts` 는 `string[]` 로 직접 기술했고, 각 review 에 최소 1개 이상의 relevant `/memories/session/**.md` 또는 evidence ref 를 넣었다.
- [ ] implementation bundle task 는 self-contained 하다 — task-local field 만으로 구현 scope 와 done-definition 이 명확하다.
- [ ] review 기본값을 self-check + final `board`로 두었고, specialist review 는 hotspot 기반으로만 켰다.
- [ ] phase 와 task 수를 최소화했고, process 가 구현보다 더 커지지 않는다.
- [ ] risks, rollback, testing 이 빠지지 않았다.
- [ ] 코딩 세부 구현까지 내려가지 않았고, 문서는 dispatch-ready execution brief 수준에 머문다.

## 3. Packet Type Definitions

### ImplementationTaskPacket

각 구현 task 가 사용하는 패킷 타입이다. 모든 필드를 직접 기술한다.

| Field | Type | Required | Meaning |
|------|------|----------|---------|
| `depends_on` | `TaskId[]` | Yes | 선행 dependency |
| `owned_outcome` | `string` | Yes | 이 task 가 닫아야 하는 단일 결과 |
| `worker_brief` | `string` | Yes | 구현 worker 가 따라야 하는 순서와 관점 |
| `exact_file_scope` | `FilePath[]` | Yes | 수정 가능한 file paths |
| `exact_symbol_scope` | `string[] \| 'N/A'` | Yes | 핵심 함수, 컴포넌트, 타입, route, schema |
| `included_scope` | `string` | Yes | 허용된 수정 범위 |
| `excluded_scope` | `string` | Yes | 이번 task 에서 건드리지 않을 범위 |
| `verification_expectation` | `string` | Yes | 필수 검증과 evidence expectation |
| `artifacts` | `string[]` | Yes | task-essential artifact refs, 기본값은 `[]` 이며 packet 본문만으로 충분하면 비운다. 정말 필요시 `/memories/session/**.md` 양식으로 나열한다. |
| `functional_digest` | `string \| 'N/A'` | No | 기능 요구 핵심 |
| `design_digest` | `string \| 'N/A'` | No | design/UX 요구 |
| `technical_digest` | `string \| 'N/A'` | No | technical constraint |
| `invariants` | `string` | No | 깨지면 안 되는 규칙 |
| `forbidden_edits` | `string` | No | 금지하는 수정 |
| `known_risks` | `string \| 'N/A'` | No | regression risk, gotcha, edge case |
| `escalation_triggers` | `string` | No | Commander packet refresh 조건 |
| `quality_bar` | `string` | No | 기본 마감 기준 |
| `local_overrides` | `string \| 'none'` | No | shared default 를 이 task 에서만 바꿀 때 |
| `status` | `'not-started' \| 'in-progress' \| 'completed' \| 'blocked'` | Yes | runtime tracking |
| `log` | `string` | No | 실행 후 기록 |

### ReviewTaskPacket

각 review task 가 사용하는 패킷 타입이다. 모든 필드를 직접 기술한다.

| Field | Type | Required | Meaning |
|------|------|----------|---------|
| `depends_on` | `TaskId[]` | Yes | 선행 dependency |
| `review_role` | `string \| 'board' \| 'self-check'` | Yes | reviewer role |
| `review_surface` | `string` | Yes | changed files, hotspot surface, findings summary |
| `validation` | `string` | Yes | findings 기록과 verdict 판단 방법 |
| `artifacts` | `string[]` | Yes | review-essential artifact or evidence refs, 최소 1개 이상 넣는다. `/memories/session/**.md` 양식으로 나열한다. |
| `review_goal` | `string \| 'N/A'` | No | 검토 목적 |
| `evidence_inputs` | `string \| 'N/A'` | No | change summary, validation output, prior findings |
| `review_constraints` | `string` | No | review 가 넓히지 말아야 하는 scope boundary |
| `known_risks` | `string \| 'N/A'` | No | risk hotspot |
| `escalation_triggers` | `string` | No | review 중 Commander packet refresh 조건 |
| `verdict_bar` | `string` | No | approve/approve-with-risks/rework-required 판단 기준 |
| `local_overrides` | `string \| 'none'` | No | shared default 를 이 task 에서만 바꿀 때 |
| `status` | `'not-started' \| 'in-progress' \| 'completed' \| 'blocked'` | Yes | runtime tracking |
| `log` | `string` | No | 실행 후 기록 |

## 4. Plan Template

```markdown
## Fast Execution Plan: {Title (2-10 words)}

{TL;DR - 무엇을 구현하는지, 어떤 전략으로 접근하는지 1-2 문장.}

**Generated**: {Date}
**Estimated Complexity**: {Low / Medium / High}
**Status**: {planned / in-progress / completed / blocked}

**Execution Context**

- Source PRD: {path or title}
- Design ref: {path or N/A}
- Technical ref: {path or N/A}
- Additional refs: {path or N/A, ...}
- Architecture overview: {접근 전략 1-2 문장}

## 1. File Structure Map

{영향받는 파일과 각 파일의 책임을 bundle 정의 전에 정리한다.}

| File | Responsibility | Action |
|------|---------------|--------|
| {path} | {이 파일이 맡는 책임} | {create / modify / delete} |

## 2. Scope Check

- {Fast mode 는 single-worker ownership 을 우선한다. 한 bundle 안에서 끝낼 수 있는 connected work 는 가능한 한 붙인다.}
- {split 은 file ownership, acceptance outcome, technical boundary 가 분명히 갈릴 때만 허용한다.}

## 3. Review Setup

- review target surface: {어떤 변경 surface 를 self-check 와 final board 가 볼지 요약}
- default review path: {S1 self-check -> B1 final board}
- mandatory final reviewer: `board`

### 3.1 Reviewer Role Activation

Fast mode 의 기본값은 review role 생략이다.
이 section 은 design, code-quality, security, performance, product-integrity, browser hotspot 이 명확할 때만 채운다.
specialist reviewer 가 여러 개 필요해지면 기본 execution plan 으로 전환하는 것을 우선 검토한다.

| role | Why activated for this plan | Scope | Mapped review task |
|------|------------------------------|-------|--------------------|
| {optional role or N/A} | {왜 꼭 필요한지} | {리뷰 범위} | {R1 or N/A} |

### 3.2 Final Board Gate

- inputs: {self-check evidence, optional specialist findings, residual risks}
- success criteria: {어떤 상태면 approve / approve-with-risks / rework-required 인지}

## 4. Phases & Tasks

{**아래 Phase 와 Task 는 예시일 뿐이다. Fast mode 에서는 task 를 worker brief 로 보고, micro-step chain 대신 큰 execution bundle 을 우선한다.**}

### Phase 1: Bundle Lock

**Goal**: {가장 큰 context continuity 를 유지할 primary bundle 을 고정하고, worker handoff 에 필요한 계약과 품질 기준을 확정한다}
**Demo/Validation**: {bundle ownership, included scope, excluded scope, fallback trigger 가 명확하다}

#### T1: Lock primary execution bundle
- **depends_on**: []
- {ImplementationTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 특별한 필요가 없으면 `[]` 로 둔다}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 2: Chunky Execution

**Goal**: {한 워커가 primary bundle 을 end-to-end 로 구현하고 연결하며 핵심 결과를 닫는다}
**Demo/Validation**: {핵심 outcome 이 bundle 단위로 동작하고 관련 surface 가 함께 정리된다}

#### T2: Execute primary bundle
- **depends_on**: [T1]
- {ImplementationTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 특별한 필요가 없으면 `[]` 로 둔다}
- **status**: not-started
- **log**: {실행 후 기록}

#### T3: Execute secondary bundle (Optional)
- **depends_on**: [T2]
- {ImplementationTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 특별한 필요가 없으면 `[]` 로 둔다}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 3: Review & Validation

**Goal**: {bundle completeness 를 점검하고 final board gate 를 통과한다}
**Demo/Validation**: {self-check evidence 와 final board verdict 가 기록된다}

#### S1: Self-check
- **depends_on**: {[T2] or [T2, T3]}
- **review_role**: `self-check`
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 최소 1개 이상의 relevant ref 를 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R1: {Optional reviewer role} review
- **depends_on**: [S1]
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 최소 1개 이상의 relevant ref 를 넣는다}
- **log**: {실행 후 기록}

#### B1: Final board gate
- **depends_on**: {[S1] or [S1, R1]}
- **review_role**: `board`
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `artifacts` 는 최소 1개 이상의 relevant ref 를 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

{Fast mode 에서는 새로운 task 를 추가하기 전에 먼저 이 일이 기존 bundle 안에서 닫히는지 검토한다. 새 task 는 context continuity 보다 ownership clarity 가 더 중요할 때만 만든다.}

## 5. Dependency Graph

{ASCII 또는 텍스트로 bundle 간 의존 관계를 시각화한다. Fast mode 에서는 primary bundle 이 중심이고, secondary bundle 은 truly independent 일 때만 추가한다.}

\`\`\`
T1 ──> T2 ──> T3 (optional) ──> S1 ──┬──> B1
                                      └──> R1 (optional) ──> B1
\`\`\`

## 6. Parallel Execution & Review Waves

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T1 | Immediately |
| 2 | T2 | T1 complete |
| 3 | T3 (optional) | Only if a truly independent secondary bundle remains |
| 4 | S1, R1 (optional) | Execution bundles complete |
| 5 | B1 | S1 complete and optional reviewer done |

Fast mode 에서 병렬화는 목표가 아니다. 같은 connected surface 를 여러 워커에게 나누는 것보다, 한 워커가 context 를 유지하며 끝까지 밀고 가는 편이 기본값이다.

## 7. Risks & Gotchas

- **RISK-{N}**: {위험 요소} — mitigation: {완화 방법}
- **GOTCHA-{N}**: {놓치기 쉬운 edge case 또는 pitfall}

## 8. Rollback Plan

- {실패 시 복구 방법}
- {bundle 이 실제로는 둘 이상의 subsystem 으로 갈라진다는 것이 드러날 때의 대응}

## 9. Testing Strategy

- {bundle outcome 을 빠르게 증명하는 검증부터 적는다: targeted run, smoke test, narrow automated test, manual proof}
- {개별 micro-step 보다 end-to-end bundle completeness 를 우선 검증한다}
- {high complexity 인 경우 최소 하나의 stronger verification 을 추가한다}
```
