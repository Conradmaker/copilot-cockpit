# React 19 변경사항

React 19에서 도입된 주요 API 변경사항과 마이그레이션 가이드다.

> ⚠️ **React 19 이상에서만 적용된다.** React 18 이하를 사용하고 있다면 이 문서를 건너뛴다.

---

## 1. forwardRef 제거 → ref를 props로 직접 전달

### 변경 이유

React 19에서 `ref`가 일반 prop이 됐다. 더 이상 `forwardRef` 래퍼가 필요 없다.
컴포넌트 정의가 더 깔끔해지고, 타입도 단순해진다.

### ❌ Before (React 18): forwardRef 사용

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

### ✅ After (React 19): ref를 일반 prop으로 전달

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

### 마이그레이션 체크리스트

- [ ] `forwardRef` 래퍼 제거
- [ ] `ref`를 컴포넌트 props 타입에 직접 추가
- [ ] 구조 분해 할당에서 `ref` 추출

---

## 2. use() 도입 → useContext 대체

### 변경 이유

`use()`는 `useContext()`를 대체하는 새로운 API다.
가장 큰 차이점은 `use()`가 **조건부로 호출**될 수 있다는 점이다. `useContext()`는 훅 규칙(Rules of Hooks)에 따라 항상 컴포넌트 최상위에서만 호출 가능했지만, `use()`는 조건문이나 반복문 안에서도 사용할 수 있다.

### ❌ Before (React 18): useContext 사용

```tsx
const value = useContext(MyContext)
```

### ✅ After (React 19): use 사용

```tsx
const value = use(MyContext)
```

### use()의 조건부 호출

```tsx
function ComposerInput({ variant }: { variant: "simple" | "rich" }) {
  // 조건부로 Context 사용 가능
  if (variant === "rich") {
    const { state } = use(RichEditorContext)
    return <RichTextInput value={state.input} />
  }

  const { state } = use(ComposerContext)
  return <TextInput value={state.input} />
}
```

### Compound Components에서 use() 활용

```tsx
function ComposerInput() {
  const {
    state,
    actions: { update },
    meta: { inputRef },
  } = use(ComposerContext)

  return (
    <TextInput
      ref={inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}

function ComposerSubmit() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Send</Button>
}
```

### Context Provider의 새로운 문법

React 19에서 Context Provider도 간소화됐다:

```tsx
// Before (React 18)
<ComposerContext.Provider value={{ state, actions, meta }}>
  {children}
</ComposerContext.Provider>

// After (React 19)
<ComposerContext value={{ state, actions, meta }}>
  {children}
</ComposerContext>
```

---

## 3. 마이그레이션 요약

| 항목 | React 18 | React 19 |
| ----- | ----- | ----- |
| ref 전달 | `forwardRef((props, ref) => ...)` | `function Comp({ ref, ...props })` |
| Context 읽기 | `useContext(MyContext)`  | `use(MyContext)` |
| Context Provider | `<Ctx.Provider value={...}>` | `<Ctx value={...}>` |
| 조건부 Context | 불가능  | `use()`로 가능  |

### 주의사항

- `use()`는 React 19에서만 사용 가능하다. 프로젝트의 React 버전을 먼저 확인한다.
- `forwardRef`는 React 19에서 deprecated이지만 아직 동작한다. 점진적으로 마이그레이션한다.
- Context Provider의 새 문법은 React 19에서만 동작한다.
