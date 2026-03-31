# Next.js and SSR

## 목표

Next.js와 SSR 환경에서 Zustand를 안전하게 쓴다. 이 문서는 per-request store, App Router client boundary, scoped provider, hydration mismatch, persisted state와 SSR의 충돌을 다룬다.

---

## 1. 안정적인 원칙부터 적용한다

upstream Next.js 가이드는 갱신 중일 수 있으므로 experimental guidance보다 안정적인 핵심 원칙을 기준으로 삼는다.

- 서버 환경에서 module-level global store를 요청 간 source of truth처럼 공유하지 않는다
- React Server Components는 Zustand store를 읽고 쓰지 않는다
- store는 client provider나 request-scoped factory에서 만든다
- 서버와 클라이언트가 같은 초기 상태를 보게 만들지 못하면 hydration mismatch가 난다

---

## 2. App Router에서는 client provider에 store를 둔다

### store factory

```ts
import { createStore } from 'zustand/vanilla'

export type CounterState = {
  count: number
}

export type CounterActions = {
  increment: () => void
  decrement: () => void
}

export type CounterStore = CounterState & CounterActions

export const defaultInitState: CounterState = {
  count: 0,
}

export const createCounterStore = (
  initState: CounterState = defaultInitState,
) => {
  return createStore<CounterStore>()((set) => ({
    ...initState,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
  }))
}
```

### client provider

```tsx
'use client'

import { createContext, useContext, useState, type ReactNode } from 'react'
import { useStore } from 'zustand'
import { createCounterStore, type CounterStore } from '@/stores/counter-store'

type CounterStoreApi = ReturnType<typeof createCounterStore>

const CounterStoreContext = createContext<CounterStoreApi | undefined>(undefined)

export function CounterStoreProvider({ children }: { children: ReactNode }) {
  const [store] = useState(() => createCounterStore())
  return (
    <CounterStoreContext.Provider value={store}>
      {children}
    </CounterStoreContext.Provider>
  )
}

export function useCounterStore<T>(selector: (state: CounterStore) => T): T {
  const context = useContext(CounterStoreContext)

  if (!context) {
    throw new Error('useCounterStore must be used within CounterStoreProvider')
  }

  return useStore(context, selector)
}
```

### App Router 연결

```tsx
import { CounterStoreProvider } from '@/providers/counter-store-provider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <CounterStoreProvider>{children}</CounterStoreProvider>
      </body>
    </html>
  )
}
```

---

## 3. per-request store가 필요한 이유

Next.js 서버는 여러 요청을 동시에 처리한다. module scope의 shared store를 두면 request A가 쓴 상태가 request B에 비칠 수 있다. 서버 캐싱과 RSC 조합에서는 이런 전역 mutable state가 특히 위험하다.

### 빠른 판단 기준

- SSR과 Next.js에서 module scope store를 만들었다면 request isolation이 깨질 수 있다
- route별 또는 request별 초기 상태가 다르면 factory와 provider 구조를 사용한다

---

## 4. RSC에서 store를 읽거나 쓰지 않는다

React Server Components는 hook과 context를 쓰는 장소가 아니다. server action이나 RSC에서 Zustand store를 source of truth처럼 만지면 아키텍처가 흔들린다.

- RSC는 props와 서버 fetch 결과를 계산해 client component로 넘긴다
- client component에서만 Zustand hook을 읽는다
- 서버에서 계산한 initial state가 필요하면 provider 생성 시점으로 넘긴다

---

## 5. persisted client state는 hydration mismatch를 유발할 수 있다

브라우저 storage 값이 서버가 렌더한 초기 HTML과 다르면 Next.js는 mismatch warning을 낼 수 있다.

### 전략 A: 지연된 client read

클라이언트 mount 이후에 selector 결과를 반영하는 wrapper를 둔다.

```tsx
'use client'

import { useEffect, useState } from 'react'

export function useHydratedStore<TState, TSlice>(
  storeHook: (selector: (state: TState) => TSlice) => TSlice,
  selector: (state: TState) => TSlice,
) {
  const value = storeHook(selector)
  const [hydratedValue, setHydratedValue] = useState<TSlice | undefined>(undefined)

  useEffect(() => {
    setHydratedValue(value)
  }, [value])

  return hydratedValue
}
```

### 전략 B: `skipHydration` + manual `rehydrate`

```ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const usePreferencesStore = create(
  persist(
    () => ({ theme: 'system' as const }),
    {
      name: 'preferences',
      skipHydration: true,
    },
  ),
)
```

```tsx
useEffect(() => {
  void usePreferencesStore.persist.rehydrate()
}, [])
```

### 빠른 판단 기준

- 서버 첫 렌더와 브라우저 storage 값이 다를 수 있으면 hydration 전략이 필요하다
- theme, locale, collapsed sidebar처럼 persisted UI preference는 mismatch 후보가 된다

---

## 6. route마다 다른 store가 필요하면 page 단위 provider로 내린다

모든 페이지가 같은 store를 공유할 필요는 없다. route별 독립 상태가 필요하면 layout이 아니라 page 또는 segment 수준에서 provider를 생성한다.

```tsx
import { DashboardStoreProvider } from '@/providers/dashboard-store-provider'
import { DashboardPage } from '@/components/dashboard-page'

export default function Page() {
  return (
    <DashboardStoreProvider>
      <DashboardPage />
    </DashboardStoreProvider>
  )
}
```

---

## 7. 실전 체크리스트

- store factory가 `createStore` 기반으로 분리되어 있는가
- provider가 client component인가
- `useStore` 호출이 client component 안에만 있는가
- RSC가 Zustand store를 직접 읽거나 쓰지 않는가
- persisted UI state가 hydration mismatch를 만들 가능성이 없는가
- route-scoped state가 필요하면 provider 위치가 적절한가

---

## 8. 실험적 API는 기본 권장으로 두지 않는다

예를 들어 SSR-safe middleware 같은 실험적 API는 upstream에서도 논의 중일 수 있다. 팀이 명시적으로 채택하지 않았다면 기본 패턴은 factory + provider + client boundary로 유지하는 편이 안전하다.