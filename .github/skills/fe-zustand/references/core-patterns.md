# Core Patterns

## 목표

일반적인 Zustand v5 store 설계 패턴을 빠르게 고른다. 이 문서는 hook store와 vanilla store의 기본 생성 방식, selector 전략, slices, scoped store, reset과 testing의 기본 뼈대를 다룬다.

---

## 1. `create`와 `createStore`를 구분한다

### Hook store

일반적인 React app의 공용 client state는 `create<T>()(...)` 패턴을 기본값으로 둔다.

```ts
import { create } from 'zustand'

type CounterStore = {
  count: number
  increment: () => void
  reset: () => void
}

const initialCounterState = { count: 0 }

export const useCounterStore = create<CounterStore>()((set) => ({
  ...initialCounterState,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set(initialCounterState),
}))
```

### Vanilla store

React 바깥에서 구독하거나, instance를 여러 개 만들어야 하거나, provider 스코프를 명시해야 하면 `createStore<T>()(...)`를 사용한다.

```ts
import { createStore } from 'zustand/vanilla'

type CounterStoreState = { count: number }
type CounterStoreActions = {
  increment: () => void
}

export type CounterStore = CounterStoreState & CounterStoreActions

export const createCounterStore = (
  initState: CounterStoreState = { count: 0 },
) => {
  return createStore<CounterStore>()((set) => ({
    ...initState,
    increment: () => set((state) => ({ count: state.count + 1 })),
  }))
}
```

### 빠른 판단 기준

- React hook처럼 바로 쓰는 전역 client state면 `create`
- provider마다 다른 인스턴스가 필요하면 `createStore`
- 탭별, route별, request별 상태면 `createStore` 쪽이 더 자연스럽다

---

## 2. selector는 한 값씩 읽는 방식을 기본으로 둔다

### 기본 selector

```ts
const count = useCounterStore((state) => state.count)
const increment = useCounterStore((state) => state.increment)
```

### 피해야 할 broad subscription

```ts
const store = useCounterStore()
const { count, increment } = useCounterStore()
```

### 여러 값은 `useShallow`

여러 값을 한 번에 읽어야 한다면 stable output을 만든다.

```ts
import { useShallow } from 'zustand/react/shallow'

const { count, increment } = useCounterStore(
  useShallow((state) => ({
    count: state.count,
    increment: state.increment,
  })),
)
```

### `useShallow`와 `shallow`의 역할을 구분한다

- `useShallow`는 selector output reference를 안정화할 때 쓴다
- `shallow` comparator 자체가 필요하면 `zustand/shallow`를 쓴다
- custom equality가 필요한 경우는 `createWithEqualityFn` 또는 `useStoreWithEqualityFn`으로 다룬다

```ts
import { createWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

type PositionStore = {
  position: { x: number; y: number }
  setPosition: (position: { x: number; y: number }) => void
}

export const usePositionStore = createWithEqualityFn<PositionStore>()(
  (set) => ({
    position: { x: 0, y: 0 },
    setPosition: (position) => set({ position }),
  }),
  shallow,
)
```

### 빠른 판단 기준

- selector가 새 객체와 배열을 매 render에 만들면 stable output인지 본다
- 여러 값을 읽을 때는 `useShallow`를 먼저 검토한다
- comparator가 반복적으로 필요할 때만 traditional API를 검토한다

---

## 3. v5에서는 unstable selector output을 그대로 두지 않는다

v5는 React 기본 동작과 더 가깝게 맞춰져 있어서 selector가 매번 새 reference를 반환하면 무한 루프성 re-render를 만들 수 있다.

```ts
const [searchValue, setSearchValue] = useStore(
  useShallow((state) => [state.searchValue, state.setSearchValue]),
)
```

fallback action이나 default object도 stable reference를 사용한다.

```ts
const FALLBACK_ACTION = () => {}

const action = useMainStore((state) => state.action ?? FALLBACK_ACTION)
```

---

## 4. slices는 combined store에서 조합한다

공용 store가 커지면 도메인별 slice로 나누고, combined store에서 spread로 합친다.

```ts
import { create, StateCreator } from 'zustand'

type AuthSlice = {
  user: { id: string; email: string } | null
  login: (user: { id: string; email: string }) => void
  logout: () => void
}

type CartSlice = {
  items: Array<{ id: string; quantity: number }>
  addItem: (item: { id: string; quantity: number }) => void
  clearCart: () => void
}

type AppStore = AuthSlice & CartSlice

const createAuthSlice: StateCreator<AppStore, [], [], AuthSlice> = (set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
})

const createCartSlice: StateCreator<AppStore, [], [], CartSlice> = (
  set,
  get,
) => ({
  items: [],
  addItem: (item) => {
    if (!get().user) return
    set((state) => ({ items: [...state.items, item] }))
  },
  clearCart: () => set({ items: [] }),
})

export const useAppStore = create<AppStore>()((...args) => ({
  ...createAuthSlice(...args),
  ...createCartSlice(...args),
}))
```

### 규칙

- slice는 한 도메인 책임만 가진다
- cross-slice read는 `get()`로 처리한다
- middleware는 slice 안이 아니라 combined store에 둔다

---

## 5. scoped vanilla store는 provider와 함께 쓴다

Next.js, multi-instance UI, tab별 state처럼 store instance가 분리되어야 할 때는 context로 감싼다.

```tsx
'use client'

import { createContext, useContext, useState, type ReactNode } from 'react'
import { useStore } from 'zustand'
import { createStore } from 'zustand/vanilla'

type PositionStore = {
  position: { x: number; y: number }
  setPosition: (position: { x: number; y: number }) => void
}

const createPositionStore = () =>
  createStore<PositionStore>()((set) => ({
    position: { x: 0, y: 0 },
    setPosition: (position) => set({ position }),
  }))

const PositionStoreContext = createContext<ReturnType<
  typeof createPositionStore
> | null>(null)

export function PositionStoreProvider({ children }: { children: ReactNode }) {
  const [store] = useState(() => createPositionStore())
  return (
    <PositionStoreContext.Provider value={store}>
      {children}
    </PositionStoreContext.Provider>
  )
}

export function usePositionStore<T>(selector: (state: PositionStore) => T) {
  const store = useContext(PositionStoreContext)

  if (!store) {
    throw new Error('usePositionStore must be used within PositionStoreProvider')
  }

  return useStore(store, selector)
}
```

---

## 6. reset과 testing 경로를 먼저 만든다

store는 테스트에서 이전 상태가 새 테스트로 새지 않게 해야 한다. 초기 상태를 상수 또는 factory로 뽑아 두고 reset 액션을 같이 둔다.

```ts
const createInitialTodoState = () => ({
  todos: [] as Array<{ id: string; done: boolean }>,
})

type TodoStore = ReturnType<typeof createInitialTodoState> & {
  reset: () => void
}

export const useTodoStore = create<TodoStore>()((set) => ({
  ...createInitialTodoState(),
  reset: () => set(createInitialTodoState()),
}))
```

테스트에서는 `getState()`와 `setState()`를 직접 사용하고, 테스트 사이에 reset을 호출한다.

```ts
beforeEach(() => {
  useTodoStore.getState().reset()
})
```

### 빠른 판단 기준

- 테스트가 store 상태를 공유하면 reset 경로부터 만든다
- 초기 상태가 코드 여러 곳에 복제되면 factory로 뽑아낸다