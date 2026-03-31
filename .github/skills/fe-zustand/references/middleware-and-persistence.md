# Middleware and Persistence

## 목표

Zustand v5에서 middleware와 persistence를 현재 upstream 문서 기준으로 안전하게 조합한다. 이 문서는 `devtools`, `persist`, `immer`, `subscribeWithSelector`, storage adapter, migration, hydration control, `setState` replace semantics를 한 번에 다룬다.

---

## 1. middleware는 combined store 레벨에서 조합한다

slice 내부에 각각 middleware를 붙이지 말고, combined store를 만드는 가장 바깥쪽에서 한 번 조합한다.

```ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'

type AppStore = {
  theme: 'light' | 'dark' | 'system'
  sidebarOpen: boolean
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  toggleSidebar: () => void
}

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      immer((set) => ({
        theme: 'system',
        sidebarOpen: true,
        setTheme: (theme) =>
          set(
            (state) => {
              state.theme = theme
            },
            false,
            'ui/setTheme',
          ),
        toggleSidebar: () =>
          set(
            (state) => {
              state.sidebarOpen = !state.sidebarOpen
            },
            false,
            'ui/toggleSidebar',
          ),
      })),
      {
        name: 'app-ui',
      },
    ),
    {
      name: 'AppStore',
      enabled: process.env.NODE_ENV === 'development',
    },
  ),
)
```

## 2. `devtools`는 여러 middleware를 섞을 때 가장 바깥쪽에 둔다

Zustand의 TypeScript 가이드는 `devtools`를 가능한 마지막 wrapper로 둘 것을 권장한다. 이유는 `devtools`가 `setState`를 확장하고 타입 정보를 붙이기 때문이다. 다른 middleware가 앞에서 `setState`를 다시 변형하면 그 타입 정보가 흐려질 수 있다.

### 권장

```ts
devtools(persist(immer((set) => ({ ... }))))
devtools(subscribeWithSelector(immer((set) => ({ ... }))))
```

### 피해야 할 패턴

```ts
immer(devtools((set) => ({ ... })))
subscribeWithSelector(devtools((set) => ({ ... })))
```

### 빠른 판단 기준

- 여러 middleware를 섞으면 `devtools(...)`를 outermost 후보로 본다
- slice 내부마다 `persist`, `immer`, `devtools`를 각각 감싸고 있으면 combined store에서 재정렬한다

---

## 3. `persist`는 durable한 값만 저장한다

`persist`를 붙였다고 모든 state를 저장할 필요는 없다. UI toggles, loading flags, transient error, toasts, auth token, session-specific draft까지 전부 localStorage에 넣으면 stale state와 보안 문제가 커진다.

### `partialize`

```ts
persist(
  (set) => ({
    theme: 'system' as const,
    notificationsEnabled: true,
    sidebarOpen: true,
    loading: false,
  }),
  {
    name: 'preferences',
    partialize: (state) => ({
      theme: state.theme,
      notificationsEnabled: state.notificationsEnabled,
    }),
  },
)
```

### storage 선택

- localStorage: cross-tab durable preference
- sessionStorage: tab-scoped draft or wizard progress
- custom storage 또는 IndexedDB: 큰 데이터나 custom persistence

```ts
import { createJSONStorage, persist } from 'zustand/middleware'

persist(
  (set) => ({ step: 0 }),
  {
    name: 'checkout-draft',
    storage: createJSONStorage(() => sessionStorage),
  },
)
```

---

## 4. persisted schema가 바뀌면 `version`과 `migrate`를 같이 둔다

persisted shape를 바꾸고 migration을 생략하면 이전 저장값이 조용히 무시되거나 잘못 해석될 수 있다.

```ts
persist(
  (set) => ({
    theme: 'light' as const,
    fontSize: 14,
  }),
  {
    name: 'settings',
    version: 2,
    migrate: (persisted, version) => {
      const state = persisted as Record<string, unknown>

      if (version === 1) {
        return {
          ...state,
          fontSize: 14,
        }
      }

      return state
    },
  },
)
```

### 빠른 판단 기준

- persisted field를 추가, 삭제, rename했으면 `version`을 올린다
- migration이 없으면 이전 저장값을 어떻게 처리하는지 명시할 수 없다

---

## 5. hydration lifecycle을 제어한다

SSR이나 async storage가 있는 환경에서는 hydration timing을 명시적으로 다루는 편이 안전하다.

### 기본 hydration hook

```ts
persist(
  (set) => ({ count: 0 }),
  {
    name: 'counter',
    onRehydrateStorage: () => (state, error) => {
      if (error) {
        console.error('rehydration failed', error)
      }
    },
  },
)
```

### `skipHydration`

```ts
export const usePreferencesStore = create(
  persist(
    () => ({ theme: 'system' as const }),
    {
      name: 'preferences',
      skipHydration: true,
    },
  ),
)

useEffect(() => {
  void usePreferencesStore.persist.rehydrate()
}, [])
```

### hydration listeners

`persist` API는 `hasHydrated`, `onHydrate`, `onFinishHydration`를 제공한다. SSR mismatch를 피하거나 boot splash를 제어할 때 유용하다.

```ts
const unsub = usePreferencesStore.persist.onFinishHydration(() => {
  console.log('preferences hydrated')
})
```

---

## 6. `immer`는 nested update가 진짜 이득일 때만 쓴다

깊은 객체와 배열 갱신이 많을 때 `immer`는 읽기 쉬운 업데이트를 만든다. 하지만 단순한 평면 상태만 다룰 때까지 기본 옵션으로 둘 필요는 없다.

```ts
import { immer } from 'zustand/middleware/immer'

type TodoStore = {
  todos: Array<{ id: string; done: boolean }>
  toggle: (id: string) => void
}

export const useTodoStore = create<TodoStore>()(
  immer((set) => ({
    todos: [],
    toggle: (id) =>
      set((state) => {
        const todo = state.todos.find((item) => item.id === id)
        if (todo) todo.done = !todo.done
      }),
  })),
)
```

### 빠른 판단 기준

- shallow object update 몇 개뿐이면 plain `set`가 더 단순하다
- nested tree update와 array mutation이 자주 나오면 `immer` 후보로 본다

---

## 7. `subscribeWithSelector`는 React 바깥 구독에 쓴다

외부 시스템 동기화, DOM side effect, analytics, theme sync 같은 케이스에서 특정 slice만 구독할 수 있다.

```ts
import { subscribeWithSelector } from 'zustand/middleware'

export const useThemeStore = create(
  subscribeWithSelector(() => ({
    theme: 'light' as const,
  })),
)

const unsubscribe = useThemeStore.subscribe(
  (state) => state.theme,
  (theme) => {
    document.documentElement.dataset.theme = theme
  },
  { fireImmediately: true },
)
```

---

## 8. action naming과 `setState` replace semantics를 명시한다

`devtools`와 함께 쓸 때는 action name을 붙여 timeline을 읽기 쉽게 만든다. 전체 상태를 대체할 때는 `replace=true` semantics를 이해하고 써야 한다.

```ts
set(
  (state) => ({ count: state.count + 1 }),
  false,
  'counter/increment',
)

useCounterStore.setState({ count: 0 }, true)
```

특히 primitive state나 array state, 전체 reset에서 `replace`가 중요하다.

---

## 9. custom equality가 필요하면 traditional API를 쓴다

v5의 `create`는 equality function customization을 기본 지원하지 않는다. comparator가 필요한 경우 `zustand/traditional`과 `use-sync-external-store` peer dependency를 전제로 둔다.

```bash
npm install use-sync-external-store
```

```ts
import { createWithEqualityFn } from 'zustand/traditional'
import { shallow } from 'zustand/shallow'

const useFilteredStore = createWithEqualityFn<{ a: number; b: number }>()(
  () => ({ a: 0, b: 0 }),
  shallow,
)
```

### 빠른 판단 기준

- `useShallow`로 해결되면 traditional API까지 늘리지 않는다
- comparator가 store hook 수준에서 반복적으로 필요할 때만 traditional API를 검토한다