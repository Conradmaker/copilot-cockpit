# Execution Plan Template

## 1. How to Create This Plan

- `/memories/session/artifacts.md`를 먼저 읽고, listed된 task-relevant existing 문서만 연다. approved `prd.md`가 있으면 planning anchor로 먼저 확인하되, execution requirement input은 relevant listed artifacts를 함께 본다.
- data contract가 필요하면 type, schema, query contract부터 먼저 고정한다.
- full-stack feature는 backend contract를 먼저 고정하고, backend implementation과 frontend mock integration을 가능한 범위에서 병렬화한다.
- 영향을 받는 파일과 scope split 여부를 먼저 정리한다.
- task는 하나의 명확한 outcome으로 나누고, 병렬 task는 file overlap이 낮고 interface와 validation이 독립적일 때만 분리한다.
- frontend stateful work는 data layer를 먼저, page-context-heavy UI는 shared layout context를 먼저, design-system work는 primitive나 component unit을 먼저 고정한다.
- 같은 페이지 안에서 레이아웃, 카피, 모션, 시각적 위계가 강하게 엮여 있으면 한 context로 밀고, isolated widget이나 micro interaction만 뒤에서 분리한다.
- generated asset requirement가 있으면 dedicated asset generation phase를 추가하고, 마지막에 review, risks, rollback, testing을 채워 plan을 orchestration 구조로 유지한다.

## 2. Plan Checklist & Cautions

- [ ] `/memories/session/artifacts.md`를 먼저 읽고, approved `prd.md`가 있으면 planning anchor로 확인했으며, task-relevant listed artifacts를 함께 기준으로 작성했다.
- [ ] PRD 를 다시 쓰지 않고 approved scope 를 atomic task 단위 구조로 변환했다.
- [ ] data contract 가 필요한 경우 type, schema, query contract 가 먼저 고정되었다.
- [ ] full-stack feature 라면 backend contract 와 frontend integration boundary 가 먼저 합의되었다.
- [ ] 모든 task 에 `depends_on`과 appropriate validation field 가 있다. implementation task 는 optional `verification_expectation`(task-specific 추가 검증 필요시), review/asset task 는 `validation`을 사용한다. Deep Execution Agent의 default verification은 codebase-level essential check(typecheck, lint on modified files, syntax check)이다.
- [ ] 병렬 task 끼리 file overlap 이 낮고 cross-task interface 가 명확하다.
- [ ] 각 task 의 validation 이 독립적이고, 한 task 의 실패가 무관한 work 를 불필요하게 막지 않는다.
- [ ] page-context-heavy UI 를 과도하게 잘게 쪼개지 않았고, design-system or isolated widget work 는 독립 unit 으로 분리했다.
- [ ] 병렬화 이득보다 coordination cost 가 큰 구간은 한 context 로 유지했다.
- [ ] review lane 과 final-review gate 가 같은 dependency model 안에 들어가 있다.
- [ ] risks, rollback, testing 과 selected reviewer roles 가 빠지지 않았다.
- [ ] implementation task 는 generic artifact bag 없이도 self-contained 하다.
- [ ] review task 의 `evidence_inputs` 는 changed surface, validation output, prior findings, 필요한 session doc reference를 concise digest로 기술했다.
- [ ] implementation task 는 self-contained 하다 — task-local field 만으로 구현 scope 와 done-definition 이 명확하다.
- [ ] 코딩 세부 구현까지 내려가지 않았고, plan 이 spec 수준으로 비대하지 않다.

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
| `verification_expectation` | `string \| 'N/A'` | No | Deep Execution Agent는 default로 codebase-level essential verification(typecheck, modified files lint, syntax check)을 수행한다. full build/test는 Phase 3 build-verification role이 담당한다. task-specific 추가 검증이 필요하면 기술한다. |
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
| `review_role` | `string \| 'final-review' \| 'self-check'` | Yes | reviewer role |
| `review_surface` | `string` | Yes | changed files, hotspot surface, findings summary |
| `validation` | `string` | Yes | findings 기록과 verdict 판단 방법 |
| `evidence_inputs` | `string` | Yes | review에 필요한 change summary, validation output, prior findings, 필요한 doc 또는 command reference digest |
| `review_goal` | `string \| 'N/A'` | No | 검토 목적 |
| `review_constraints` | `string` | No | review 가 넓히지 말아야 하는 scope boundary |
| `known_risks` | `string \| 'N/A'` | No | risk hotspot |
| `escalation_triggers` | `string` | No | review 중 Commander packet refresh 조건 |
| `verdict_bar` | `string` | No | approve/approve-with-risks/rework-required 판단 기준 |
| `local_overrides` | `string \| 'none'` | No | shared default 를 이 task 에서만 바꿀 때 |
| `status` | `'not-started' \| 'in-progress' \| 'completed' \| 'blocked'` | Yes | runtime tracking |
| `log` | `string` | No | 실행 후 기록 |

## 4. Plan Template

```markdown
## Execution Plan: {Title (2-10 words)}

{TL;DR - 무엇을 구현하는지, 어떤 전략으로 접근하는지 1-2 문장.}

**Generated**: {Date}
**Estimated Complexity**: {Low / Medium / High}
**Status**: {planned / in-progress / completed / blocked}

**Execution Context**

- Artifact index: {path or N/A}
- Source PRD: {path or title}
- Design ref: {path or N/A}
- Technical ref: {path or N/A}
- Additional refs: {path or N/A, ...}
- Architecture overview: {접근 전략 1-2 문장}

## 1. File Structure Map

{영향받는 파일과 각 파일의 책임을 task 정의 전에 정리한다.}

| File | Responsibility | Action |
|------|---------------|--------|
| {path} | {이 파일이 맡는 책임} | {create / modify / delete} |

## 2. Scope Check

- {독립적인 서브시스템이 여러 개면 별도 plan 으로 분리하는 것을 권장한다.}
- {단일 plan 으로 진행하는 경우 그 판단 근거를 적는다.}

## 3. Review Setup

- review target surface: {어떤 변경 surface 를 어떤 review role 이 볼지 요약}
- mandatory final reviewer: `final-review`

### 3.1 Reviewer Role Activation

Reviewer role activation logic 의 source of truth 는 `.github/agents/reviewer-roles/_index.md` 다.
이 section 에는 이번 execution plan 에서 활성화할 review role 을 기록한다.
`final-review`는 병렬 review role 이 아니라 Final Review Gate 에서 다룬다.

사용 가능한 role: `design-ex`, `code-quality`, `interface-contract`, `security`, `performance`, `runtime-verification`, `build-verification`. (`final-review`는 Final Review Gate 전용)

| role | Why activated for this plan | Scope | Mapped review task |
|------|------------------------------|-------|--------------------|
| {role} | {왜 이 role 을 켜는가} | {리뷰 범위} | {R1 / R2 / R3} |
| {role} | {왜 이 role 을 켜는가} | {리뷰 범위} | {R1 / R2 / R3} |

필요한 만큼 행을 추가한다.

### 3.2 Final Review Gate

- inputs: {lane findings, verification evidence, residual risks}
- success criteria: {어떤 상태면 approve / approve-with-risks / rework-required 인지}

## 4. Phases & Tasks

{**아래 Phase 와 Task 는 예시일 뿐이다. 필요에 따라 Phase 를 추가하거나 빼고, Task 를 추가하거나 빼거나 병렬화한다.**}

### Phase 1: Asset Generation (Optional)

**Goal**: {design.md 의 image requirement list 에 있는 asset item 들을 Painter 로 생성한다}
**Demo/Validation**: {각 output_path 가 생성되고 asset_id 별 결과가 확인된다}

#### T-IMG1: Generate {asset_id}
- **depends_on**: [{design-ready task id or []}]
- **location**: {/memories/session/design.md, {output_path}}
- **description**: {Generate one required asset item with explicit asset_id and output_path}
- **validation**: {output_path exists, generated file matches asset_id, rough tone fits design.md}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 2: {Name}

**Goal**: {이 phase 가 달성하는 것}
**Demo/Validation**: {이 phase 완료 시 검증 방법}

#### T1: {Task name}
- **depends_on**: []
- {ImplementationTaskPacket 의 required field 를 모두 기술한다}
- **status**: not-started
- **log**: {실행 후 기록}

#### T2: {Task name}
- **depends_on**: []
- {ImplementationTaskPacket 의 required field 를 모두 기술한다}
- **status**: not-started
- **log**: {실행 후 기록}

#### T3: {Task name}
- **depends_on**: [T1]
- {ImplementationTaskPacket 의 required field 를 모두 기술한다}
- **status**: not-started
- **log**: {실행 후 기록}

#### T4: {Task name}
- **depends_on**: [T2, T3]
- {ImplementationTaskPacket 의 required field 를 모두 기술한다}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 3: Review & Validation

**Goal**: {implementation output 을 review role 별로 검증하고 final-review gate 를 통과시킨다}
**Demo/Validation**: {review findings 와 final-review verdict 가 기록된다}

#### R1: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `evidence_inputs` 에 review에 필요한 change summary와 prior findings를 압축해 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R2: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `evidence_inputs` 에 review에 필요한 change summary와 prior findings를 압축해 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R3: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `evidence_inputs` 에 review에 필요한 change summary와 prior findings를 압축해 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

#### B1: Final review gate
- **depends_on**: [R1, R2, R3]
- **review_role**: `final-review`
- {ReviewTaskPacket 의 required field 를 모두 기술한다. `evidence_inputs` 에 lane findings와 residual risk를 압축해 넣는다}
- **status**: not-started
- **log**: {실행 후 기록}

{필요한 만큼 Phase 와 Task 를 확장한다.}

## 5. Dependency Graph

{ASCII 또는 텍스트로 task 간 의존 관계를 시각화한다. asset generation 이 optional 이면 required 한 task 에만 branch 를 연결한다.}

\`\`\`
T-IMG1 ──┐
         ├── T1 ──┬── T3 ──┐
         │        │        ├── R1 ──┐
         └── T2 ──┴── T4 ──┼── R2 ──┼── B1
                           └── R3 ──┘
\`\`\`

## 6. Parallel Execution & Review Waves

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T-IMG1 | Immediately |
| 2 | T1, T2 | Asset generation phase complete or independent |
| 3 | T3, T4 | Wave 2 complete |
| 4 | R1, R2, R3 | Relevant implementation tasks complete |
| 5 | B1 | R1, R2, R3 complete |

## 7. Risks & Gotchas

- **RISK-{N}**: {위험 요소} — mitigation: {완화 방법}
- **GOTCHA-{N}**: {놓치기 쉬운 edge case 또는 pitfall}

## 8. Rollback Plan

- {실패 시 복구 방법}
- {어떤 단계에서 stop 할지}

## 9. Testing Strategy

- {전체 검증 전략}
- {Phase 별 검증 포인트}
```
