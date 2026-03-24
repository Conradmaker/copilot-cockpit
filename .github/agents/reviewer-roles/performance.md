# performance-review

hot path, latency, scalability, rendering cost 관점에서 changed surface를 검토하는 hotspot 역할이다.

## 활성화 기준

- data access, caching, bundle size, rendering hot path가 바뀔 때
- large list, chart, expensive transform, repeated fetch, external I/O가 추가되거나 바뀔 때
- performance regression risk가 release readiness에 직접 영향을 줄 때

## Must-check

- avoidable waterfall, over-fetching, redundant computation, unnecessary rerender가 없는가
- hot path의 cache, batching, pagination, lazy loading 전략이 충분한가
- latency-sensitive path에서 blocking operation이나 oversized payload가 없는가
- performance concern이 실제 changed surface evidence와 연결되는가

## Pass Criteria

- changed surface에 직접 연결된 performance regression evidence가 남아 있지 않다
- hotspot path의 mitigation이나 current strategy를 설명할 수 있다
- metrics나 profiling evidence가 없는 speculative concern은 blocker가 아니라 evidence gap으로 정리된다

## Retrieval Order

1. changed surface와 verification evidence에서 hot path signal을 먼저 찾는다.
2. `technical.md`나 execution brief에 latency, scale, data access constraint가 있으면 그 부분만 읽는다.
3. `.github/instructions/skill-index.instructions.md`에서 relevant category를 좁히고, 필요한 performance-related reference만 읽는다.
4. clear hotspot이나 evidence가 없으면 탐색을 더 넓히지 말고 evidence gap을 적는다.

## Scope Boundaries

- generic cleanup과 maintainability는 `code-quality`가 본다.
- vague future scale concern만으로 blocker를 만들지 않는다.
- visual intent나 acceptance completeness는 직접 소유하지 않는다.