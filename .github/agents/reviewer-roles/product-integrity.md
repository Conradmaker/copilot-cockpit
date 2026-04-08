# product-integrity-review

구현된 결과물 또는 planning artifact가 approved `prd.md`가 요구한 기능과 product outcome을 실제로 충족하는지 검토하는 hotspot 역할이다.

## 활성화 기준

- `prd.md`의 acceptance criteria, 핵심 사용자 플로우, 결과 수락 기준이 중요할 때
- `prd.md`, `design.md`, `technical.md` 사이의 기능적 alignment risk가 있을 때
- approved 또는 near-approved `prd.md`와 downstream artifact를 handoff 전에 더 엄격하게 검증해야 할 때
- release readiness가 사용자가 의도한 과업을 끝까지 완료할 수 있는지에 직접 달려 있을 때

## Must-check

- review surface가 `prd.md`의 acceptance criteria와 핵심 사용자 시나리오를 충족하거나, planning review라면 downstream artifact에서 이를 일관되게 설명하는가
- required empty, loading, success, error, fallback state가 기능 완료나 수락 기준 충족을 막지 않는가. planning review라면 그 state가 PRD 또는 downstream seed에 빠지지 않았는가
- `design.md`와 `technical.md`가 있을 때 review surface가 기능적 expectation이나 contract를 충돌시키지 않는가
- feature 또는 spec artifact가 의도한 product outcome을 내는지 available evidence로 설명할 수 있는가
- evidence가 부족하면 어떤 verification evidence가 더 필요한지 명확히 적을 수 있는가

## Pass Criteria

- 핵심 acceptance criteria와 핵심 user flow가 충족되거나, planning review라면 downstream artifact에서 일관되게 풀린다
- required states가 기능 완료나 결과 수락을 막지 않는다
- product outcome alignment를 깨는 drift가 남아 있지 않다
- 남은 우려가 있으면 blocker인지 follow-up인지 명확히 설명할 수 있다

## Evidence Requirement

- `prd.md`와 relevant downstream artifact
- changed surface 또는 planning review surface와 verification evidence
- runtime behavior를 직접 입증하지 못하면 그 evidence gap

## Retrieval Order

1. `prd.md`와 current review surface를 먼저 읽어 acceptance target과 non-goal을 맞춘다. execution review면 current execution brief와 changed surface를, planning review면 downstream artifact를 함께 읽는다.
2. relevant `design.md`, `technical.md`가 있으면 intended experience, contract, constraint를 기능 완결성 기준으로 다시 정리한다.
3. validation evidence와 upstream browser findings가 있으면 acceptance proof로 먼저 읽는다.
4. acceptance ambiguity가 남을 때만 `.github/instructions/skill-index.instructions.md`에서 relevant category를 좁힌다.

## Scope Boundaries

- visual polish나 표현 품질 판단은 직접 소유하지 않는다.
- runtime evidence collection은 `browser`가 소유한다.
- generic maintainability나 style critique로 확장하지 않는다.

## Quality Lift 관점

- acceptance criteria 누락 또는 애매한 success state 식별
- incomplete flow, blocked state, artifact drift 식별
- release-blocking product risk와 follow-up ticket 후보 정리