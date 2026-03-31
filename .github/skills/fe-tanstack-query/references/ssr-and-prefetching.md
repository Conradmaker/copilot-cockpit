# SSR And Prefetching

## 목표

SSR에서는 prefetch, dehydrate, HydrationBoundary, per-request QueryClient를 한 묶음으로 본다. Next.js App Router와 Server Components에서는 prefetch phase와 client application phase를 섞지 않는 것이 핵심이다.

이 문서는 기존 `ssr-dehydration`, `pf-intent-prefetch` rule과 최신 v5 advanced SSR 보강을 합친 reference다.

---

## 핵심 규칙

### ssr-dehydration

- 서버에서 필요한 query를 prefetch한 뒤 dehydrate한다
- 클라이언트는 HydrationBoundary 안에서 같은 query options를 다시 쓴다
- request 간 state 오염을 막기 위해 QueryClient는 per-request로 만든다
- server-side staleTime은 0보다 크게 두는 편이 보통 안전하다

### prefetching

- route transition, hover, focus, loader 단계에서는 prefetch를 검토한다
- v5에서는 queryOptions source가 있으면 prefetchQuery와 useQuery가 쉽게 일치한다
- 조건부 preload에는 ensureQueryData도 검토할 수 있다

---

## Next.js App Router 메모

- Server Components는 prefetch phase처럼 다루고, query 결과를 서버 UI와 client query 양쪽 truth로 동시에 쓰지 않는다
- provider 안의 browser QueryClient는 render 중 재생성되지 않게 안정적으로 유지한다
- prefetch된 query는 client에서 `useQuery` 또는 `useSuspenseQuery`로 소비할 수 있다

## advanced SSR 보강

- v5.40+에서는 pending query도 dehydration에 포함할 수 있다
- 이 경우 `defaultShouldDehydrateQuery(query) || query.state.status === "pending"` 패턴을 쓴다
- streaming SSR에서는 prefetch-less experimental path보다 prefetch 기반 경로를 기본 권장으로 둔다
- persist adapter와 streaming을 같이 쓸 때는 pending promise를 storage에 저장하지 않게 successful query만 persist해야 한다

## 빠른 체크리스트

- QueryClient가 per-request인가
- HydrationBoundary 안팎의 query source가 일치하는가
- server와 client에서 같은 데이터를 이중 ownership으로 쓰고 있지 않은가
- pending dehydration이나 persist adapter 조합이 필요한가