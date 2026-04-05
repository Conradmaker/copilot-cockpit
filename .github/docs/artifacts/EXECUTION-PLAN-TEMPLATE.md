# Execution Plan Template

## 1. How to Create This Plan

- approved `prd.md`와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact를 먼저 읽는다.
- data contract가 필요하면 type, schema, query contract부터 먼저 고정한다.
- full-stack feature는 backend contract를 먼저 고정하고, backend implementation과 frontend mock integration을 가능한 범위에서 병렬화한다.
- 영향을 받는 파일과 scope split 여부를 먼저 정리한다.
- task는 하나의 명확한 outcome으로 나누고, 병렬 task는 file overlap이 낮고 interface와 validation이 독립적일 때만 분리한다.
- frontend stateful work는 data layer를 먼저, page-context-heavy UI는 shared layout context를 먼저, design-system work는 primitive나 component unit을 먼저 고정한다.
- 같은 페이지 안에서 레이아웃, 카피, 모션, 시각적 위계가 강하게 엮여 있으면 한 context로 밀고, isolated widget이나 micro interaction만 뒤에서 분리한다.
- generated asset requirement가 있으면 dedicated asset generation phase를 추가하고, 마지막에 review, risks, rollback, testing을 채워 plan을 orchestration 구조로 유지한다.

## 2. Plan Checklist & Cautions

- [ ] approved `prd.md`와 `references.md`, `design.md`, `technical.md` 와 같은 relevant downstream artifact를 기준으로 작성했다.
- [ ] PRD를 다시 쓰지 않고 approved scope를 atomic task 단위 구조로 변환했다.
- [ ] data contract가 필요한 경우 type, schema, query contract가 먼저 고정되었다.
- [ ] full-stack feature라면 backend contract와 frontend integration boundary가 먼저 합의되었다.
- [ ] 모든 task에 `depends_on`과 `validation`이 있다.
- [ ] 병렬 task끼리 file overlap이 낮고 cross-task interface가 명확하다.
- [ ] 각 task의 validation이 독립적이고, 한 task의 실패가 무관한 work를 불필요하게 막지 않는다.
- [ ] page-context-heavy UI를 과도하게 잘게 쪼개지 않았고, design-system or isolated widget work는 독립 unit으로 분리했다.
- [ ] 병렬화 이득보다 coordination cost가 큰 구간은 한 context로 유지했다.
- [ ] review lane과 board gate가 같은 dependency model 안에 들어가 있다.
- [ ] risks, rollback, testing과 selected reviewer roles가 빠지지 않았다.
- [ ] 코딩 세부 구현까지 내려가지 않았고, plan이 spec 수준으로 비대하지 않다.

## 3. Plan Template

```markdown
## Execution Plan: {Title (2-10 words)}

{TL;DR - 무엇을 구현하는지, 어떤 전략으로 접근하는지 1-2문장.}

**Generated**: {Date}
**Estimated Complexity**: {Low / Medium / High}
**Status**: {planned / in-progress / completed / blocked}

**Execution Context**

- Source PRD: {path or title}
- Design ref: {path or N/A}
- Technical ref: {path or N/A}
- Additional refs: {path or N/A, ...}
- Architecture overview: {접근 전략 1-2문장}

## 1. File Structure Map

{영향받는 파일과 각 파일의 책임을 task 정의 전에 정리한다.}
이 map이 task의 file scope, overlap, interface boundary 판단의 기초가 된다.

| File | Responsibility | Action |
|------|---------------|--------|
| {path} | {이 파일이 맡는 책임} | {create / modify / delete} |

## 2. Scope Check

- {독립적인 서브시스템이 여러 개면 별도 plan으로 분리하는 것을 권장한다.}
- {단일 plan으로 진행하는 경우 그 판단 근거를 적는다.}

Scope decision: {single plan / split into N plans — 근거}

## 3. Review Setup

- review target surface: {어떤 변경 surface를 어떤 review role이 볼지 요약}
- mandatory final reviewer: `board`

### 3.1 Reviewer Role Activation

Reviewer role activation logic의 source of truth는 `.github/agents/reviewer-roles/_index.md`다.
이 section에는 이번 execution plan에서 활성화할 review role을 기록한다.
`board`는 병렬 review role이 아니라 Final Board Gate에서 다룬다.

| role | Why activated for this plan | Scope | Mapped review task |
|------|------------------------------|-------|--------------------|
| {role} | {왜 이 role을 켜는가} | {리뷰 범위} | {R1 / R2 / R3} |
| {role} | {왜 이 role을 켜는가} | {리뷰 범위} | {R1 / R2 / R3} |

### 3.2 Final Board Gate

- inputs: {lane findings, verification evidence, residual risks}
- success criteria: {어떤 상태면 approve / approve-with-risks / rework-required인지}

## 4. Phases & Tasks
{**아래 Phase와 Task는 예시일 뿐이다. 필요에 따라 Phase를 추가하거나 빼고, Task를 추가하거나 빼거나 병렬화한다.**}

### Phase 1: Asset Generation

**Goal**: {design.md의 image requirement list에 있는 asset item들을 Painter로 생성한다}
**Demo/Validation**: {각 output_path가 생성되고 asset_id별 결과가 확인된다}

#### T-IMG1: Generate {asset_id}
- **depends_on**: [{design-ready task id or []}]
- **location**: {/memories/session/design.md, {output_path}}
- **description**: {Generate one required asset item with explicit asset_id and output_path}
- **validation**: {output_path exists, generated file matches asset_id, rough tone fits design.md}
- **status**: not-started
- **log**: {실행 후 기록}

### Phase 2: {Name}

**Goal**: {이 phase가 달성하는 것}
**Demo/Validation**: {이 phase 완료 시 검증 방법}

#### T1: {Task name}
- **depends_on**: []
- **location**: {file paths}
- **description**: {무엇을 하는가}
- **validation**: {어떻게 검증하는가}
- **status**: not-started
- **log**: {실행 후 기록}

#### T2: {Task name}
- **depends_on**: []
- **location**: {file paths}
- **description**: {무엇을 하는가}
- **validation**: {어떻게 검증하는가}
- **status**: not-started
- **log**: {실행 후 기록}

#### T3: {Task name}
- **depends_on**: [T1]
- **location**: {file paths}
- **description**: {무엇을 하는가}
- **validation**: {어떻게 검증하는가}
- **status**: not-started
- **log**: {실행 후 기록}

#### T4: {Task name}
- **depends_on**: [T2, T3]
- ...

### Phase 3: Review & Validation

**Goal**: {implementation output을 review role별로 검증하고 final board gate를 통과시킨다}
**Demo/Validation**: {review findings와 final board verdict가 기록된다}

#### R1: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- **location**: {changed files or review surface}
- **description**: {Review the assigned surface from one reviewer role perspective}
- **validation**: {findings are recorded and blocking issue 여부가 명확하다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R2: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- **location**: {changed files or review surface}
- **description**: {Review the assigned surface from one reviewer role perspective}
- **validation**: {findings are recorded and blocking issue 여부가 명확하다}
- **status**: not-started
- **log**: {실행 후 기록}

#### R3: {Reviewer role} review
- **depends_on**: [{relevant implementation task ids}]
- **location**: {changed files or review surface}
- **description**: {Review the assigned surface from one reviewer role perspective}
- **validation**: {findings are recorded and blocking issue 여부가 명확하다}
- **status**: not-started
- **log**: {실행 후 기록}

#### B1: Final board gate
- **depends_on**: [R1, R2, R3]
- **location**: {review findings summary or changed surface}
- **description**: {Synthesize lane findings and decide the final board verdict}
- **validation**: {final verdict is recorded as approve, approve-with-risks, or rework-required}
- **status**: not-started
- **log**: {실행 후 기록}

{필요한 만큼 Phase와 Task를 확장한다.}

## 5. Dependency Graph

{ASCII 또는 텍스트로 task 간 의존 관계를 시각화한다. asset generation이 optional이면 required한 task에만 branch를 연결한다.}


T-IMG1 ──┐
         ├── T1 ──┬── T3 ──┐
         │        │        ├── R1 ──┐
         └── T2 ──┴── T4 ──┼── R2 ──┼── B1
                           └── R3 ──┘


## 6. Parallel Execution & Review Waves

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T-IMG1 | Immediately |
| 2 | T1, T2 | Asset generation phase complete or independent |
| 3 | T3, T4 | Wave 2 complete |
| 4 | R1, R2, R3 | Relevant implementation tasks complete |
| 5 | B1 | R1, R2, R3 complete |
| ... | ... | ... |

## 7. Risks & Gotchas

- **RISK-{N}**: {위험 요소} — mitigation: {완화 방법}
- **GOTCHA-{N}**: {놓치기 쉬운 edge case 또는 pitfall}

## 8. Rollback Plan

- {실패 시 복구 방법}
- {어떤 단계에서 stop할지}

## 9. Testing Strategy

- {전체 검증 전략}
- {Phase별 검증 포인트}
```

