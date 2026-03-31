---
name: fe-tanstack-query
description: "TanStack Query v5 server-state patterns for React applications, covering query key design, queryOptions-based organization, caching defaults, mutations, dynamic and infinite queries, SSR hydration, offline persistence, and domain-level .query.ts module structure. Use this skill when building or refactoring React server-state code with useQuery, useInfiniteQuery, useMutation, useQueries, QueryClient, HydrationBoundary, prefetching, or query module files. Always consult this skill for React server-state work, even if the user only asks to fetch API data, structure query files, fix stale UI, or wire SSR hydration. For client-only state use fe-zustand. Triggers on: TanStack Query, React Query, queryOptions, infiniteQueryOptions, mutationOptions, QueryClient, query keys, invalidation, optimistic update, prefetch, useQueries, useInfiniteQuery, HydrationBoundary, server state, .query.ts, 서버 상태, 쿼리 키, 캐시, 뮤테이션, 하이드레이션."
disable-model-invocation: false
user-invocable: false
---

# TanStack Query 서버 상태 패턴

## 목표

TanStack Query v5를 React의 server state 계층으로 일관되게 사용한다. query key 설계, queryOptions 기반 재사용, QueryClient 기본값, mutation과 invalidation, parallel/infinite fetching, SSR hydration, offline persistence, 그리고 도메인별 .query.ts 구조를 한 흐름으로 맞추는 것이 핵심이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 구현에 들어가기 전에는 아래 reference 문서를 직접 읽고 현재 작업이 query key 설계, 캐시 설정, mutation 설계, fetching 구조, SSR, offline/tooling, query module organization 중 어디에 속하는지 먼저 좁힌 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## Quick Reference

이 섹션은 본문 요약이 아니라 reference로 바로 점프하기 위한 인덱스다. 아래 항목과 현재 작업이 맞으면, 해당 reference를 먼저 읽고 그 다음에 구현이나 리뷰를 진행한다.

### Query Keys & Query Options

- query key shape, key factory, queryOptions, invalidation prefix, hierarchical key가 문제면 `references/query-keys.md`부터 읽는다
- `.query.ts` 구조, key와 prefetch 재사용, 도메인별 query module 정리가 필요하면 `references/query-module-organization.md`를 바로 같이 읽는다

### Cache & Defaults

- staleTime, gcTime, placeholderData, initialData, QueryClient defaults를 정하거나 리뷰할 때는 `references/caching-and-defaults.md`를 먼저 읽는다

### Mutations

- mutation invalidation, optimistic update, rollback, mutation state, mutationOptions가 핵심이면 `references/mutations-and-invalidation.md`부터 읽는다

### Dynamic Fetching

- useQueries, useInfiniteQuery, getNextPageParam, cancellation, select transform, parallel fetching 구조가 핵심이면 `references/fetching-and-parallel.md`를 먼저 읽는다
- 같은 작업에서 도메인별 query 파일 정리까지 필요하면 `references/query-module-organization.md`를 이어서 읽는다

### SSR & Prefetch

- HydrationBoundary, prefetch, App Router SSR, server/client QueryClient 경계, advanced SSR streaming이 핵심이면 `references/ssr-and-prefetching.md`부터 읽는다

### Offline & Tooling

- networkMode, persistence, query error boundary reset, Devtools, ESLint plugin query, testing 전략이 핵심이면 `references/offline-and-tooling.md`를 먼저 읽는다

---

## 핵심 패턴

### 1. TanStack Query 경계를 먼저 정한다

TanStack Query는 서버에서 권위 source를 갖는 데이터를 다룰 때 가장 강하다. 목록, detail, pagination, background refetch, optimistic update, hydration처럼 서버와 동기화되는 상태를 여기에 두고, purely local UI state는 Zustand나 local state 쪽으로 보낸다.

- 서버 데이터 fetch, cache, invalidation, mutation lifecycle은 TanStack Query를 우선 검토한다
- local-only form draft, modal open state, tab state는 local state나 Zustand가 더 단순한지 먼저 본다
- 같은 서버 데이터를 여러 화면과 훅에서 공유해야 하면 query key와 queryOptions를 먼저 설계한다

#### 빠른 판단 기준

- source of truth가 서버면 TanStack Query 후보다
- stale data, duplicate fetch, invalidation 문제가 보이면 TanStack Query 구조부터 점검한다
- client-only UI state까지 같이 넣고 있으면 경계를 다시 본다

→ 상세: references/query-keys.md, references/caching-and-defaults.md

### 2. query key와 queryOptions를 같이 설계한다

v5에서는 query key만 흩어져 있으면 금방 invalidation이 불안정해진다. key factory와 queryOptions를 같은 도메인 안에서 같이 설계하면 prefetch, hook, cache update가 같은 source를 공유할 수 있다.

- top-level query key는 항상 array로 둔다
- queryFn이 의존하는 값은 모두 key에 포함한다
- entity -> scope -> params 순서의 hierarchical key를 기본값으로 둔다
- queryOptions와 infiniteQueryOptions를 reusable source로 삼고 hook과 prefetch가 이를 공유하게 만든다

#### 빠른 판단 기준

- queryKey에 string이나 object 단독값이 보이면 수정 대상이다
- 같은 도메인에서 key 문자열이 제각각이면 key factory를 먼저 본다
- prefetch와 useQuery가 같은 key/queryFn을 따로 적고 있으면 queryOptions로 모을 수 있는지 본다

→ 상세: references/query-keys.md, references/query-module-organization.md

### 3. QueryClient 기본값과 freshness를 데이터 특성에 맞춘다

staleTime, gcTime, placeholderData, initialData, targeted invalidation은 한 묶음으로 봐야 한다. 모든 쿼리에 같은 값 하나를 박아 넣는 방식은 보통 과하거나 부족하다.

- volatile data와 reference data의 staleTime을 분리한다
- gcTime은 persistence 여부와 inactive cache 유지 전략에 맞춘다
- placeholderData와 initialData의 캐시 의미 차이를 구분한다
- broad invalidation보다 hierarchical key 기반 targeted invalidation을 우선한다

#### 빠른 판단 기준

- staleTime이 전부 기본값 0이면 네트워크 비용과 mount refetch를 다시 본다
- incomplete data를 initialData로 넣고 있으면 cache 오염 가능성을 본다
- invalidateQueries가 너무 넓거나 너무 좁으면 key 설계와 함께 다시 본다

→ 상세: references/caching-and-defaults.md

### 4. mutation은 invalidation과 rollback까지 같이 설계한다

mutationFn만 정의하고 끝내면 stale UI가 남기 쉽다. 성공 후 어떤 query를 invalidate할지, optimistic update가 필요한지, rollback context가 필요한지, cross-component pending state를 어떻게 노출할지까지 함께 설계한다.

- mutationOptions를 재사용 가능한 기준점으로 둘 수 있다
- optimistic update는 cache 조작과 UI 변수 방식 중 맞는 쪽을 고른다
- rollback context와 onError 복구 경로를 준비한다
- useMutationState와 mutationKey로 cross-component pending 상태를 추적한다

#### 빠른 판단 기준

- mutation 후 invalidateQueries가 없으면 거의 항상 보완 대상이다
- optimistic update가 있으면 cancelQueries와 rollback이 같이 있는지 본다
- 여러 컴포넌트가 같은 mutation 상태를 알아야 하면 useMutationState를 먼저 본다

→ 상세: references/mutations-and-invalidation.md

### 5. fetching 구조는 waterfall 대신 reusable options와 dynamic queries로 푼다

dynamic parallel fetching, infinite query, cancellation, select transform은 한 화면에서 같이 엮여 나오는 경우가 많다. useEffect 루프나 hook 반복 대신 useQueries, useSuspenseQueries, useInfiniteQuery를 쓴다.

- dynamic parallel fetch는 useQueries 또는 useSuspenseQueries를 쓴다
- infinite query는 initialPageParam과 getNextPageParam을 반드시 같이 둔다
- queryFn에는 signal을 전달해 cancellation을 살린다
- select는 component 소비 형태에 맞는 lightweight transform에 쓴다

#### 빠른 판단 기준

- userIds.map 안에서 useQuery를 호출하고 있으면 구조를 바꾼다
- fetch 루프가 sequential이면 useQueries 후보다
- queryFn에서 signal을 무시하고 있으면 cancellation 누락을 본다

→ 상세: references/fetching-and-parallel.md

### 6. SSR, offline, tooling은 나중이 아니라 설계 시점에 같이 본다

HydrationBoundary, per-request QueryClient, prefetching, networkMode, persistence, error boundary, Devtools, ESLint plugin query는 뒤늦게 붙이면 구조를 다시 뒤집게 된다.

- SSR에서는 per-request QueryClient와 HydrationBoundary를 기본으로 둔다
- Server Components에서는 prefetch phase와 application phase를 섞지 않는다
- offline persistence가 있으면 networkMode, persisted query 범위, resume 전략을 같이 본다
- Suspense query에는 Query error boundary reset 경로를 둔다

#### 빠른 판단 기준

- SSR에서 module-scope QueryClient를 공유하면 구조를 바꾼다
- persisted cache가 있는데 gcTime과 maxAge가 맞지 않으면 보완한다
- Suspense query가 있는데 error boundary reset이 없으면 빠뜨린 것이다

→ 상세: references/ssr-and-prefetching.md, references/offline-and-tooling.md

---

## references/ 가이드

아래 문서는 실제 구현 전에 읽어야 하는 작업 가이드다. 본문은 방향을 잡는 용도고, 세부 예시와 version-sensitive 주의사항은 references에서 확인한다.

| 파일 | 언제 읽는가 |
| --- | --- |
| references/query-keys.md | query key 설계, key factory, queryOptions, invalidation 기준점을 잡을 때 |
| references/caching-and-defaults.md | staleTime, gcTime, placeholderData, initialData, QueryClient defaults를 정할 때 |
| references/mutations-and-invalidation.md | mutation, optimistic update, rollback, mutation state, invalidation 범위를 설계할 때 |
| references/fetching-and-parallel.md | useQueries, useInfiniteQuery, cancellation, select transform, dynamic fetch 구조를 설계할 때 |
| references/ssr-and-prefetching.md | SSR hydration, prefetch, HydrationBoundary, Next.js App Router, advanced SSR streaming을 다룰 때 |
| references/offline-and-tooling.md | networkMode, persistence, error boundaries, Devtools, ESLint plugin query, testing을 볼 때 |
| references/query-module-organization.md | 도메인별 .query.ts 구조와 queryOptions 기반 모듈 정리를 그대로 재사용하고 싶을 때 |

### 추천 로드 순서

- 새 query 도입: query-keys -> caching-and-defaults -> query-module-organization
- stale cache나 invalidation bug 수정: query-keys -> caching-and-defaults -> mutations-and-invalidation
- infinite/parallel fetching 구조화: fetching-and-parallel -> query-module-organization
- SSR 도입: ssr-and-prefetching -> query-keys -> caching-and-defaults
- offline/persistence 도입: offline-and-tooling -> caching-and-defaults -> mutations-and-invalidation

---

## 범위

- client-only state와 UI orchestration -> fe-zustand
- React component architecture와 state ownership -> fe-react-patterns
- broad rendering과 waterfall 성능 최적화 -> fe-react-performance
- REST API contract와 응답 모델 설계 -> be-api-design

이 스킬은 TanStack Query를 어디에 쓰고 어떻게 구조화할지에 집중한다. generic React architecture나 backend API contract까지 한 스킬에 넣지 않는다.