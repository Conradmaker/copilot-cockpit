# Query Keys

## 목표

query key를 cache identity이자 invalidation surface로 설계한다. key factory와 queryOptions를 같은 도메인에서 같이 관리해 hook, prefetch, invalidateQueries가 한 source를 공유하게 만드는 것이 핵심이다.

이 문서는 기존 `qk-array-structure`, `qk-include-dependencies`, `qk-hierarchical-organization`, `qk-serializable`, `qk-factory-pattern` rule을 합쳐 둔 reference다.

---

## 핵심 규칙

### qk-array-structure

- top-level query key는 항상 array로 둔다
- string/object 단독 key는 쓰지 않는다
- object는 array 안의 stable params slot으로 넣는다

### qk-include-dependencies

- queryFn이 읽는 외부 값은 전부 query key에 넣는다
- userId, filters, locale, sort, page를 queryFn이 쓰면 key에도 반영한다
- 의존성이 key에 없으면 stale collision로 본다

### qk-hierarchical-organization

- entity -> scope -> params 순서를 기본값으로 둔다
- `all`, `lists`, `list(filters)`, `detail(id)` 같은 단계형 key factory를 선호한다
- broad invalidation은 상위 prefix에서, targeted invalidation은 detail key에서 하게 만든다

### qk-serializable

- key에는 JSON-serializable 값만 넣는다
- class instance, function, Date object 원본, unstable reference는 피한다
- 필요한 경우 string, number, plain object로 normalize한다

### qk-factory-pattern

- query 종류가 늘어나면 key factory를 도메인별로 분리한다
- v5에서는 key factory와 queryOptions를 같이 두는 구성이 가장 다루기 쉽다
- invalidation은 factory를 통해 호출하고 raw literal을 반복하지 않는다

---

## v5 권장 패턴

`queryOptions`와 `infiniteQueryOptions`를 key source와 같이 둔다.

```ts
import { infiniteQueryOptions, queryOptions } from "@tanstack/react-query"

export const contentKeys = {
  all: ["contents"] as const,
  channels: (locale: string) => [...contentKeys.all, "channels", locale] as const,
  youtube: (handles: string[], locale: string) =>
    [...contentKeys.all, "youtube", locale, handles] as const,
}

export const contentQueries = {
  channels: (locale: string) =>
    queryOptions({
      queryKey: contentKeys.channels(locale),
      queryFn: () => fetchChannels(locale),
      staleTime: 30 * 60 * 1000,
    }),
  youtube: (handles: string[], locale: string) =>
    infiniteQueryOptions({
      queryKey: contentKeys.youtube(handles, locale),
      queryFn: ({ pageParam }) => fetchYoutube({ handles, locale, page: pageParam }),
      initialPageParam: 1,
      getNextPageParam: (lastPage) =>
        lastPage.hasNextPage ? lastPage.currentPage + 1 : undefined,
    }),
}
```

이렇게 두면 다음이 같은 source를 공유한다.

- `useQuery(contentQueries.channels(locale))`
- `useInfiniteQuery(contentQueries.youtube(handles, locale))`
- `queryClient.prefetchQuery(contentQueries.channels(locale))`
- `queryClient.prefetchInfiniteQuery(contentQueries.youtube(handles, locale))`

---

## 저장소 패턴 연결

[query module organization](query-module-organization.md) 패턴을 같이 쓰면, 도메인별 .query.ts 파일 안에 key factory와 query options를 함께 둘 수 있다. 핵심은 특정 저장소 파일을 참조하는 것이 아니라, 한 도메인의 key 설계와 reusable options source가 같은 모듈 안에서 같이 움직이도록 만드는 것이다.

## 빠른 체크리스트

- key가 array인가
- queryFn 의존성이 key에 모두 들어갔는가
- hierarchical prefix invalidation이 가능한가
- key literal이 여러 파일에 흩어지지 않았는가
- queryOptions와 prefetch가 같은 source를 공유하는가