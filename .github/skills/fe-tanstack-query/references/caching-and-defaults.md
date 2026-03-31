# Caching And Defaults

## 목표

staleTime, gcTime, placeholderData, initialData, QueryClient defaults를 데이터 특성에 맞게 정한다. default를 기계적으로 복붙하지 않고, data volatility와 UX 목표에 따라 조절하는 것이 핵심이다.

이 문서는 기존 `cache-stale-time`, `cache-gc-time`, `cache-placeholder-vs-initial`, `cache-invalidation` rule과 기본 QueryClient 설정 보강을 합친 reference다.

---

## 핵심 규칙

### cache-stale-time

- default staleTime 0을 무심코 그대로 두지 않는다
- profile, config, taxonomy 같은 low-volatility data는 더 길게 둔다
- SSR route는 immediate client refetch를 막기 위해 server-side staleTime을 0보다 크게 두는 편이 안전하다

### cache-gc-time

- inactive cache retention은 persistence 여부와 navigation pattern에 맞춘다
- persisted cache가 있으면 기본 5분보다 긴 gcTime이 더 자연스럽다
- offline/persistence 없이 긴 gcTime만 늘리면 메모리 비용만 커질 수 있다

### cache-placeholder-vs-initial

- `initialData`는 cached truth처럼 취급된다
- `placeholderData`는 temporary display 용도다
- SSR이나 완전한 authoritative data에는 initialData를, list preview나 keep previous 화면에는 placeholderData를 쓴다

### cache-invalidation

- broad invalidation이 필요하면 prefix-friendly key를 먼저 설계한다
- raw string key 대신 key factory로 invalidateQueries를 호출한다
- setQueryData와 invalidateQueries를 혼합할 때는 즉시성 UI와 eventual consistency를 구분한다

---

## QueryClient 기본값

```ts
import { QueryClient } from "@tanstack/react-query"

export function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        gcTime: 30 * 60 * 1000,
        refetchOnWindowFocus: false,
      },
    },
  })
}
```

기본값은 baseline일 뿐이다. 실제 freshness는 각 도메인별 queryOptions에서 override하는 쪽이 보통 낫다.

## v5 메모

- `gcTime`은 예전 `cacheTime` 자리에 온 이름이다
- `placeholderData: keepPreviousData`는 pagination/filter UX에 여전히 유용하다
- `select`는 cache shape를 바꾸는 용도가 아니라 component consumption shape를 가볍게 바꾸는 용도로 본다

## 빠른 체크리스트

- data volatility에 맞는 staleTime인가
- persistence 유무와 gcTime이 맞는가
- placeholderData와 initialData를 혼동하지 않았는가
- invalidateQueries 범위가 key hierarchy와 맞물리는가