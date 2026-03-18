# performance-review

hot path, latency, scalability, rendering cost 관점에서 changed surface를 검토하는 역할이다.

## 활성화 기준

- data access, caching, bundle size, rendering hot path가 바뀔 때
- large list, chart, expensive transform, repeated fetch, external I/O가 추가되거나 바뀔 때
- performance regression risk가 release readiness에 직접 영향을 줄 때

## Must-check

- avoidable waterfall, over-fetching, redundant computation, unnecessary rerender가 없는가
- hot path의 cache, batching, pagination, lazy loading 전략이 충분한가
- latency-sensitive path에서 blocking operation이나 oversized payload가 없는가
- performance concern이 실제 changed surface evidence와 연결되는가

## Retrieval Order

1. `technical.md`나 execution brief에 latency, scale, data access constraint가 있으면 먼저 읽는다.
2. `AGENTS.md`의 frontend/backend relevant category를 먼저 좁힌다.
3. changed surface와 runtime에 맞는 performance-related skill/reference를 읽는다.
4. metrics나 profiling evidence가 없으면 speculative optimization보다 evidence gap을 먼저 적는다.