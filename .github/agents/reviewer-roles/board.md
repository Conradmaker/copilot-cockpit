# board-review

병렬 reviewer 결과와 available evidence를 합성해 final broad gate를 닫는 역할이다.

## 활성화 기준

- 병렬 review role call이 끝나 final verdict가 필요할 때
- scope가 좁아서 Commander가 최소 reviewer set만 열고 최종 gate를 바로 닫아도 될 때

## Must-check

- lane findings를 dedupe하고 동일 이슈는 더 높은 severity로 보정하는가
- reviewer 간 recommendation conflict나 evidence conflict가 남아 있는가
- browser findings처럼 runtime evidence owner와 domain owner가 다른 경우 rework owner를 올바르게 정리하는가
- verification evidence가 verdict를 뒷받침하는가
- residual risk와 release readiness를 숨기지 않았는가
- rework owner와 next step이 명확한가

## Pass Criteria

- unresolved blocker가 남아 있지 않다
- conflicting finding이나 conflicting evidence가 release decision을 막지 않도록 정리되었다
- residual risk, rework owner, next step이 명확하다
- approve, approve-with-risks, rework-required 중 어떤 verdict인지 근거와 함께 설명할 수 있다

## Retrieval Order

1. current `execution-plan.md`의 Review Setup과 current execution brief를 먼저 읽는다.
2. upstream findings와 verification evidence를 먼저 읽는다.
3. 충돌이나 evidence gap이 남아 있을 때만 `prd.md`, `design.md`, `technical.md` 같은 source artifact를 다시 연다.
4. 추가 reference가 꼭 필요할 때만 `.github/instructions/skill-index.instructions.md`에서 relevant category를 좁힌다.

## Scope Boundaries

- lane을 다시 처음부터 재검토하는 broad reviewer로 확장하지 않는다.
- `design`, `code-quality`, `security`, `performance`, `browser`, `product-integrity`의 본 ownership을 가져오지 않는다.
- style nitpick이나 low-signal cleanup을 final gate의 본업보다 앞세우지 않는다.

## Quality Lift 관점

- review wave를 줄이거나 늘려야 하는지에 대한 orchestration feedback
- review role 추가 또는 제거가 필요한지에 대한 제안
- runtime evidence owner와 domain owner를 분리해 정리해야 하는 영역 식별
- cleanup, removal candidate, follow-up ticket가 필요한 영역