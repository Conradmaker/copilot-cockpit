---
name: zustand
description: Zustand adapter for json-render's StateStore interface using @json-render/zustand. Use this skill when integrating json-render with a Zustand vanilla store, selecting a state slice for StateProvider, wiring updater logic for nested state, or replacing another json-render StateStore backend with Zustand. Always consult this skill for json-render state backend work involving Zustand, even if the user only asks to connect state, use Zustand here, bind a store to StateProvider, or sync a form or UI slice through json-render. For general Zustand application architecture outside json-render integration, use broader state-management guidance instead. Triggers on: @json-render/zustand, json-render, StateStore, StateProvider, Zustand vanilla store, zustand/vanilla, selector, updater, 상태 어댑터, 스토어 연결.
---

# @json-render/zustand

Zustand adapter for json-render's `StateStore` interface. Wire a Zustand vanilla store as the state backend for json-render.

## Installation

```bash
npm install @json-render/zustand @json-render/core @json-render/react zustand
```

Requires Zustand v5+. Zustand v4 is not supported due to breaking API changes in the vanilla store interface.

## Usage

```tsx
import { createStore } from "zustand/vanilla"
import { zustandStateStore } from "@json-render/zustand"
import { StateProvider } from "@json-render/react"

// 1. Create a Zustand vanilla store
const bearStore = createStore(() => ({
  count: 0,
  name: "Bear",
}))

// 2. Create the json-render StateStore adapter
const store = zustandStateStore({ store: bearStore })

// 3. Use it
<StateProvider store={store}>{/* json-render reads/writes go through Zustand */}</StateProvider>
```

### With a Nested Slice

```tsx
const appStore = createStore(() => ({
  ui: { count: 0 },
  auth: { token: null },
}))

const store = zustandStateStore({
  store: appStore,
  selector: (s) => s.ui,
  updater: (next, s) => s.setState({ ui: next }),
})
```

## API

### `zustandStateStore(options)`

Creates a `StateStore` backed by a Zustand store.

| Option | Type | Required | Description |
| --- | --- | --- | --- |
| `store` | `StoreApi<S>` | Yes | Zustand vanilla store (from `createStore` in `zustand/vanilla`) |
| `selector` | `(state) => StateModel` | No | Select the json-render slice. Defaults to entire state. |
| `updater` | `(nextState, store) => void` | No | Apply next state to the store. Defaults to shallow merge. Override for nested slices, or use `(next, s) => s.setState(next, true)` for full replacement. |
