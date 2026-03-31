# Query Module Organization

## 목표

쿼리를 화면 단위로 흩뿌리지 않고 도메인별 `.query.ts` 파일에 모아 관리한다. 같은 도메인의 key, fetcher, reusable options, prefetch, hooks를 한 파일에 두어 discoverability와 invalidation 일관성을 높이는 것이 핵심이다.

이 문서는 도메인별 query module을 정리하는 독립 reference다. 같은 패턴이 다른 reference 안에 중복되어 나타나도 이 파일을 canonical reusable note로 본다.

---

## 권장 구조

도메인별로 아래 흐름을 한 파일 안에서 정리한다.

1. `keys`
2. fetcher 또는 low-level request helper
3. `queryOptions` / `infiniteQueryOptions`
4. prefetch helper
5. `use...Query` / `use...InfiniteQuery`

파일명은 `<domain>.query.ts`, 타입은 인접한 `<domain>.type.ts` 또는 기존 type 모듈에 둔다.

## 왜 이 구조가 좋은가

- key와 queryFn이 가까이 있어 cache reasoning이 쉬워진다
- prefetch와 hook이 같은 source를 공유하기 쉬워진다
- list/detail/infinite/prefetch를 도메인 단위로 묶어 탐색 비용이 줄어든다
- invalidation 대상을 찾을 때 도메인 파일 하나에서 대부분 추적 가능하다

---

## 패턴 예시에서 가져갈 점

아래처럼 한 도메인의 query module이 이미 이런 역할을 갖고 있다고 가정하고 구조를 설계한다.

- `contentKeys` 같은 key factory를 한곳에 모은다
- fetcher를 hook 밖으로 분리한다
- prefetch 함수와 useQuery/useInfiniteQuery 훅을 같은 파일에 둔다
- type은 인접한 `.type.ts` 또는 기존 type 모듈로 분리한다

새 스킬에서는 이 배치를 유지하되, v5 기준으로 raw hook 옵션 중복을 줄이기 위해 options source를 더 먼저 둔다.

## v5 친화적 권장 형태

```ts
import {
  infiniteQueryOptions,
  QueryClient,
  queryOptions,
  useInfiniteQuery,
  useQuery,
} from "@tanstack/react-query"

export const contentKeys = {
  channelList: (locale: string) => ["contents/channel", locale] as const,
  youtubeList: (handles: string[], locale: string) =>
    ["contents/youtube", locale, handles] as const,
}

export const contentQueries = {
  channelList: (locale: string) =>
    queryOptions({
      queryKey: contentKeys.channelList(locale),
      queryFn: () => fetchChannelList(locale),
      staleTime: 30 * 60 * 1000,
      gcTime: 31 * 60 * 1000,
    }),
  youtubeList: (handles: string[], locale: string) =>
    infiniteQueryOptions({
      queryKey: contentKeys.youtubeList(handles, locale),
      queryFn: ({ pageParam }) => fetchYoutubeList({ handles, locale, page: pageParam }),
      initialPageParam: 1,
      getNextPageParam: (lastPage) =>
        lastPage.hasNextPage ? lastPage.currentPage + 1 : undefined,
    }),
}

export const prefetchChannelList = (queryClient: QueryClient, locale: string) =>
  queryClient.prefetchQuery(contentQueries.channelList(locale))

export const useChannelListQuery = (locale: string) =>
  useQuery(contentQueries.channelList(locale))

export const useYoutubeListQuery = (handles: string[], locale: string) =>
  useInfiniteQuery(contentQueries.youtubeList(handles, locale))
```

이 예시의 포인트는 실제 파일명 자체가 아니라 배치 방식이다. 도메인별 `.query.ts` 파일 하나에서 key, options, prefetch, hooks를 같이 발견할 수 있어야 하고, 인접 type 모듈은 데이터 shape를 분리해 추적 가능하게 만들어야 한다.

## 분류 기준

같은 도메인 안에서는 최소 아래 단위로 묶는다.

- list
- detail
- infinite
- prefetch
- mutation이 많아지면 같은 도메인의 `.mutation.ts` 분리 여부를 검토

## 빠른 체크리스트

- 도메인별 `.query.ts` 파일이 있는가
- key, fetcher, options, prefetch, hook이 같은 파일에 정리되는가
- raw hook 옵션 중복 대신 queryOptions를 재사용하는가
- type이 인접 file 또는 인접 module에서 함께 탐색 가능한가