# Mutations And Invalidation

## 목표

mutation은 mutationFn 하나로 끝내지 않는다. invalidation 범위, optimistic update 방식, rollback context, cross-component pending state, mutation option 재사용까지 한 번에 설계한다.

이 문서는 기존 `mut-invalidate-queries`, `mut-optimistic-updates`, `mut-mutation-state` rule과 source skill의 quick reference에만 있었던 rollback/loading/error 내용을 함께 정리한 reference다.

---

## 핵심 규칙

### mut-invalidate-queries

- 성공 후 stale가 될 수 있는 query를 모두 invalidation 대상으로 잡는다
- detail, list, summary, related entity surface를 같이 본다
- hierarchical key가 있으면 broad invalidation을 단순하게 유지할 수 있다

### mut-optimistic-updates

- user-facing 반응성이 중요하면 optimistic update를 먼저 검토한다
- cache 조작 방식은 여러 화면에 반영될 때, UI 변수 방식은 한 컴포넌트에서만 보일 때 유리하다
- optimistic update 전에는 관련 query를 cancelQueries로 멈추고 snapshot을 저장한다

### rollback, loading, error

- `onMutate`에서 rollback context를 반환한다
- `onError`에서 context 기반 복구 경로를 둔다
- `isPending`을 loading state의 기본값으로 쓴다
- `onSettled`에서 eventual consistency invalidate를 검토한다

### mut-mutation-state

- 여러 컴포넌트가 같은 mutation 진행 상태를 알아야 하면 `mutationKey`와 `useMutationState`를 쓴다
- optimistic row나 global pending badge처럼 mutation caller 밖에서 상태를 읽을 때 특히 유용하다

---

## v5 권장 패턴

`mutationOptions`로 재사용 가능한 mutation definition을 만들 수 있다.

```ts
import { mutationOptions } from "@tanstack/react-query"

export const todoMutations = {
  update: () =>
    mutationOptions({
      mutationKey: ["todos", "update"],
      mutationFn: updateTodo,
    }),
}
```

이 위에 UI별 `onSuccess`, `onError`, optimistic logic을 얹는다.

## mutation scope

- 같은 종류의 mutation을 serialize해야 하면 `scope: { id }`를 검토한다
- offline queue와 결합될 때 ordering 요구가 있는 쓰기 작업에 특히 유용하다

## mutate vs mutateAsync

- fire-and-forget UI action이면 `mutate`
- 후속 side effect를 순차 compose해야 하면 `mutateAsync`

## 빠른 체크리스트

- success 후 invalidateQueries가 있는가
- optimistic update면 cancelQueries, snapshot, rollback이 같이 있는가
- mutation caller 밖에서 pending state를 읽어야 하는가
- mutationKey와 scope 설계가 필요한가