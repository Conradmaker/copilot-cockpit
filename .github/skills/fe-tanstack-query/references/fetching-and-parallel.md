# Fetching And Parallel

## 목표

dynamic parallel fetch, infinite query, cancellation, select transform을 waterfall 없이 구성한다. useEffect 루프와 hook 반복 대신 TanStack Query의 구조를 그대로 쓴다.

이 문서는 기존 `parallel-use-queries`, `inf-page-params`, `query-cancellation`, `perf-select-transform` rule을 합친 reference다.

---

## 핵심 규칙

### parallel-use-queries

- query 수가 동적이면 `useQueries` 또는 `useSuspenseQueries`를 쓴다
- hook을 loop 안에서 직접 호출하지 않는다
- combine 옵션으로 result array를 domain shape로 합칠 수 있다

### inf-page-params

- infinite query에는 `initialPageParam`과 `getNextPageParam`을 함께 둔다
- cursor 기반이면 cursor를, offset 기반이면 next page number를 명시적으로 반환한다
- page flatten은 component boundary에서만 하고 cache shape는 pages 구조를 유지한다

### query-cancellation

- queryFn의 `signal`을 fetch나 axios에 반드시 전달한다
- search-as-you-type, fast navigation, optimistic mutation 전에 cancellation 누락을 특히 주의한다

### perf-select-transform

- `select`는 component가 바로 소비할 lightweight transform에 쓴다
- expensive reshape를 매 컴포넌트에서 반복하지 않게 한다
- cache schema를 바꾸는 용도가 아니라 consumer projection 용도로 본다

---

## 저장소 패턴 연결

도메인별 `.query.ts` 파일 안에 list/detail/infinite/prefetch를 같이 두는 패턴은 dynamic fetching과 잘 맞는다. [query module organization](query-module-organization.md) 패턴을 따르되, 새 구현에서는 raw hook마다 중복 options를 적기보다 reusable options source를 앞에 두는 쪽을 권장한다.

예를 들면 한 도메인의 query module에서 key factory, prefetch helper, infinite query hook이 함께 관리되고 있다고 가정하고, 다음처럼 options source를 먼저 둘 수 있다.

```ts
export const contentQueries = {
  youtubeList: (handles: string[], locale: string) =>
    infiniteQueryOptions({
      queryKey: contentKeys.youtubeList(handles, locale),
      queryFn: ({ pageParam }) => youtubeListFetcher({ handles, locale, page: pageParam }),
      initialPageParam: 1,
      getNextPageParam: (lastPage) =>
        lastPage.hasNextPage ? lastPage.currentPage + 1 : undefined,
    }),
}
```

## 빠른 체크리스트

- dynamic query를 useEffect loop로 처리하고 있지 않은가
- infinite query에 getNextPageParam이 있는가
- queryFn이 signal을 전달하는가
- select가 consumer projection 용도로만 쓰이고 있는가