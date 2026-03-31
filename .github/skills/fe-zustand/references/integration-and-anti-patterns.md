# Integration and Anti-Patterns

## 목표

Zustand를 다른 상태 계층과 안전하게 나눈다. 이 문서는 TanStack Query와의 역할 분리, forms와의 경계, testing과 reset, 그리고 반복적으로 문제를 만드는 anti-pattern을 한 번에 정리한다.

---

## 1. TanStack Query와 Zustand의 경계를 분명히 둔다

### 권장 역할 분리

- **TanStack Query**: 서버 데이터 fetch, cache, invalidation, mutation lifecycle
- **Zustand**: local UI state, multi-step flow, view preference, optimistic UI orchestration, client-only selection state

```ts
import { create } from 'zustand'

type UIStore = {
  sidebarOpen: boolean
  selectedUserId: string | null
  toggleSidebar: () => void
  selectUser: (id: string | null) => void
}

export const useUIStore = create<UIStore>()((set) => ({
  sidebarOpen: false,
  selectedUserId: null,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  selectUser: (id) => set({ selectedUserId: id }),
}))
```

```tsx
import { useQuery } from '@tanstack/react-query'

function UserPanel() {
  const selectedUserId = useUIStore((state) => state.selectedUserId)

  const userQuery = useQuery({
    queryKey: ['user', selectedUserId],
    queryFn: () => fetchUser(selectedUserId!),
    enabled: Boolean(selectedUserId),
  })

  if (!selectedUserId) return null
  if (userQuery.isPending) return <div>Loading...</div>

  return <div>{userQuery.data?.name}</div>
}
```

### 빠른 판단 기준

- 서버 응답을 그대로 cache하고 invalidation해야 하면 Query 계층이다
- 사용자 로컬 선택, 탭 상태, wizard step이면 Zustand 쪽이다
- mutation 결과를 여러 component UI가 즉시 반응해야 하면 Query와 Zustand를 함께 쓸 수 있다

---

## 2. derived state는 저장하지 말고 selector에서 계산한다

### 피해야 할 패턴

```ts
const useCartStore = create((set) => ({
  items: [],
  total: 0,
}))
```

### 권장

```ts
type CartStore = {
  items: Array<{ id: string; price: number; quantity: number }>
}

const useCartStore = create<CartStore>()(() => ({
  items: [],
}))

export const useCartTotal = () =>
  useCartStore((state) =>
    state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
  )
```

---

## 3. form state는 global store로 과도하게 끌어올리지 않는다

단일 form의 field editing까지 전부 전역 store로 보내면 validation, dirty tracking, touched state가 복잡해진다.

- 단일 페이지 form은 local state 또는 form library를 먼저 검토한다
- wizard처럼 단계 간 공유가 필요하면 submission-ready slice만 Zustand에 둔다
- autosave draft가 진짜 필요할 때만 persisted store를 붙인다

### 빠른 판단 기준

- 모든 input change를 전역 store로 보내고 있다면 범위가 과한지 본다
- form completion 이후에도 여러 화면에서 같은 draft를 재사용해야 할 때만 전역화를 검토한다

---

## 4. full-store destructuring은 anti-pattern이다

```ts
const { count, increment } = useCounterStore()
```

이 패턴은 store의 어떤 필드가 바뀌어도 컴포넌트를 흔들 수 있다. selector 단위 구독으로 쪼갠다.

---

## 5. server entity fetch를 store action에 넣을 때는 경계를 의식한다

client-only side effect나 bridge 성격의 action은 store에 둘 수 있다. 하지만 entity fetching, stale cache 관리, retry, invalidation까지 store action이 전부 떠안으면 Query 계층과 책임이 겹친다.

```ts
const useUsersStore = create((set) => ({
  users: [],
  fetchUsers: async () => {
    const users = await api.getUsers()
    set({ users })
  },
}))
```

이 패턴은 서버 데이터를 client state처럼 취급하기 쉬우므로 경계를 재검토한다.

---

## 6. persistence에 secret을 넣지 않는다

- access token
- refresh token
- raw personal data snapshot
- 민감한 query result

특히 localStorage persistence는 브라우저 세션 너머로 남고 XSS surface에도 노출된다.

---

## 7. testing에서는 reset과 direct store access를 적극적으로 쓴다

### shared hook store 테스트

```ts
beforeEach(() => {
  useAppStore.getState().reset()
})

it('increments count', () => {
  useAppStore.getState().increment()
  expect(useAppStore.getState().count).toBe(1)
})
```

### context와 vanilla store 테스트

store creator를 export해 두면 per-test fresh instance를 만들 수 있다.

```ts
const store = createCounterStore({ count: 10 })
expect(store.getState().count).toBe(10)
store.getState().increment()
expect(store.getState().count).toBe(11)
```

### 빠른 판단 기준

- 테스트가 순서에 따라 깨지면 reset path부터 본다
- fresh instance가 필요하면 createStore factory 테스트가 더 단순하다

---

## 8. review에서 자주 보는 anti-pattern 목록

| 안티패턴 | 왜 문제인가 | 권장 방향 |
| --- | --- | --- |
| 전체 store destructuring | broad re-render | selector 단위 구독 |
| derived state 저장 | sync drift | selector 계산 |
| server state 저장 | invalidation과 staleness 복잡 | TanStack Query 분리 |
| per-slice middleware | 조합과 typing 혼란 | combined store에서 한 번만 적용 |
| unstable selector output | v5 re-render 문제 | `useShallow`, stable reference |
| secret persistence | 보안 리스크 | memory-only 또는 안전한 별도 전략 |
| giant monolithic store | merge conflict, 낮은 응집도 | typed slices |

---

## 9. integration 결정 표

| 상황 | 우선 선택 |
| --- | --- |
| 다중 컴포넌트가 공유하는 UI state | Zustand |
| 서버 목록 또는 상세 데이터 cache | TanStack Query |
| 단일 form editing | local state 또는 form library |
| route 또는 provider마다 다른 store instance | `createStore` + context |
| selector re-render bug | `useShallow` 또는 equality 검토 |
| 테스트용 isolated state | initial state factory + reset 또는 fresh vanilla store |