# Execution Plan Template

이 문서는 execution phase에서 Commander가 `/memories/session/execution-plan.md`를 작성할 때 따르는 artifact template다.
Commander가 primary owner지만, Coordinator가 execution plan quality를 검토하거나 Deep Execution Agent가 자신의 scope를 확인할 때도 읽을 수 있다.

## Use This Doc When

- `implementation_handoff_packet`을 받아 execution plan을 처음 만들 때
- 기존 execution plan을 rework 후 갱신할 때
- execution plan의 구조적 품질을 검토할 때
- plan의 dependency graph나 parallel wave 안전성을 확인할 때

## Mandatory Rules

- execution plan은 approved `prd.md`와 relevant downstream artifacts를 전제로 한다.
- execution plan은 PRD나 downstream artifact를 다시 쓰지 않고, approved scope를 task 단위 실행 구조로 변환한다.
- 모든 task에는 `depends_on`과 `validation`이 있어야 한다.
- `depends_on`이 빈 task끼리는 같은 wave에서 병렬 실행할 수 있다.
- dependency cycle이 생기면 plan을 확정하지 않는다.
- approved scope를 넘는 task를 추가하지 않는다.
- 코딩 세부 구현(코드 블록, 함수 시그니처)은 넣지 않는다. 구현 판단은 Deep Execution Agent의 책임이다.
- Phase 안에서 각 task는 독립적으로 위임 가능한 atomic work unit이어야 한다.
- plan이 영향받는 파일 scope를 File Structure Map에서 먼저 정리해야 task의 file overlap과 interface boundary를 판단할 수 있다.
- plan 작성 후 gotcha/risk를 식별하고, 발견된 위험이 plan 수정을 필요로 하면 갱신한다.
- execution plan은 session 동안 실행 상태의 source of truth로서 task 상태를 갱신하며 유지한다.

## Template

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
- Execution brief: {path or N/A}
- Architecture overview: {접근 전략 1-2문장}

## 1. File Structure Map

영향받는 파일과 각 파일의 책임을 task 정의 전에 정리한다.
이 map이 task의 file scope, overlap, interface boundary 판단의 기초가 된다.

| File | Responsibility | Action |
|------|---------------|--------|
| {path} | {이 파일이 맡는 책임} | {create / modify / delete} |

## 2. Scope Check

- 독립적인 서브시스템이 여러 개면 별도 plan으로 분리하는 것을 권장한다.
- 단일 plan으로 진행하는 경우 그 판단 근거를 적는다.

Scope decision: {single plan / split into N plans — 근거}

## 3. Phases & Tasks

### Phase 1: {Name}

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

### Phase 2: {Name}

**Goal**: {이 phase가 달성하는 것}
**Demo/Validation**: {이 phase 완료 시 검증 방법}

#### T4: {Task name}
- **depends_on**: [T2, T3]
- ...

{필요한 만큼 Phase와 Task를 확장한다.}

## 4. Dependency Graph

{ASCII 또는 텍스트로 task 간 의존 관계를 시각화한다.}

```
T1 ──┬── T3 ──┐
     │        ├── T5 ── T6
T2 ──┴── T4 ──┘
```

## 5. Parallel Execution Waves

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T1, T2 | Immediately |
| 2 | T3, T4 | Wave 1 complete |
| 3 | T5 | T3, T4 complete |
| ... | ... | ... |

## 6. Risks & Gotchas

- **RISK-{N}**: {위험 요소} — mitigation: {완화 방법}
- **GOTCHA-{N}**: {놓치기 쉬운 edge case 또는 pitfall}

## 7. Rollback Plan

- {실패 시 복구 방법}
- {어떤 단계에서 stop할지}

## 8. Testing Strategy

- {전체 검증 전략}
- {Phase별 검증 포인트}
```

## Review Checklist

- dependency graph에 순환이 없는가
- `depends_on`이 빈 task끼리 같은 wave에 안전하게 묶였는가 (file overlap, interface conflict 없음)
- 모든 task에 `validation`이 있는가
- task scope이 approved PRD와 downstream artifact의 범위를 벗어나지 않는가
- File Structure Map의 파일과 task의 location이 일치하는가
- Phase가 논리적 순서로 배열되고 각 Phase가 검증 가능한 increment를 만드는가
- gotcha/risk가 식별되었는가
- rollback plan이 현실적인가
- plan이 PRD 수준으로 비대하지 않은가 (orchestration 구조이지 spec이 아님)
