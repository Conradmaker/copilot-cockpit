# 상태 관리 패턴

React 컴포넌트의 상태를 효과적으로 관리하고 공유하기 위한 패턴들을 정리한 문서다.
Provider를 활용한 상태 끌어올리기, 구현 분리, 제네릭 Context 인터페이스 설계를 다룬다.

---

## 1. State Lifting (상태 끌어올리기)

### 핵심 개념

상태 관리를 전용 Provider 컴포넌트로 끌어올린다.
이렇게 하면 메인 UI 바깥에 있는 형제 컴포넌트도 prop drilling이나 ref 없이 상태에 접근할 수 있다.

### ❌ Before: 컴포넌트 안에 갇힌 상태

```tsx
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState);
  const forwardMessage = useForwardMessage();

  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer />
    </Composer.Frame>
  );
}

// 문제: 이 버튼이 어떻게 Composer 상태에 접근하나요?
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* Composer 상태가 필요 */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* submit을 호출해야 함 */}
      </DialogActions>
    </Dialog>
  );
}
```

### ❌ 잘못된 해결법: useEffect로 상태 동기화

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState("");
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  );
}

function ForwardMessageComposer({onInputChange}) {
  const [state, setState] = useState(initialState);
  useEffect(() => {
    onInputChange(state.input); // 매번 변경할 때마다 동기화 😬
  }, [state.input]);
}
```

### ❌ 잘못된 해결법: ref로 상태 읽기

```tsx
function ForwardMessageDialog() {
  const stateRef = useRef(null);
  return (
    <Dialog>
      <ForwardMessageComposer stateRef={stateRef} />
      <ForwardButton onPress={() => submit(stateRef.current)} />
    </Dialog>
  );
}
```

### ✅ After: Provider로 상태 끌어올리기

```tsx
function ForwardMessageProvider({children}: {children: React.ReactNode}) {
  const [state, setState] = useState(initialState);
  const forwardMessage = useForwardMessage();
  const inputRef = useRef(null);

  return (
    <Composer.Provider
      state={state}
      actions={{update: setState, submit: forwardMessage}}
      meta={{inputRef}}
    >
      {children}
    </Composer.Provider>
  );
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview /> {/* 상태에 접근 가능 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* submit 액션에 접근 가능 */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  );
}

function ForwardButton() {
  const {actions} = use(Composer.Context);
  return <Button onPress={actions.submit}>Forward</Button>;
}
```

**핵심 인사이트:** 공유 상태가 필요한 컴포넌트들이 시각적으로 서로 안에 중첩될 필요는 없다.
같은 Provider 안에만 있으면 된다.

---

## 2. Implementation Decoupling (상태 구현 분리)

### 핵심 개념

Provider 컴포넌트가 상태 관리 방법을 아는 **유일한 곳**이어야 한다.
UI 컴포넌트는 Context 인터페이스만 소비하고, 상태가 useState에서 오는지, Zustand에서 오는지, 서버 동기화에서 오는지 알 필요가 없다.

### ❌ Before: UI가 상태 구현에 결합됨

```tsx
function ChannelComposer({channelId}: {channelId: string}) {
  // UI 컴포넌트가 전역 상태 구현을 직접 알고 있음
  const state = useGlobalChannelState(channelId);
  const {submit, updateInput} = useChannelSync(channelId);

  return (
    <Composer.Frame>
      <Composer.Input value={state.input} onChange={(text) => updateInput(text)} />
      <Composer.Submit onPress={() => submit()} />
    </Composer.Frame>
  );
}
```

### ✅ After: Provider에 상태 구현 격리

```tsx
// Provider가 모든 상태 관리 상세를 처리
function ChannelProvider({
  channelId,
  children,
}: {
  channelId: string;
  children: React.ReactNode;
}) {
  const {state, update, submit} = useGlobalChannel(channelId);
  const inputRef = useRef(null);

  return (
    <Composer.Provider state={state} actions={{update, submit}} meta={{inputRef}}>
      {children}
    </Composer.Provider>
  );
}

// UI 컴포넌트는 Context 인터페이스만 알면 됨
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  );
}

// 사용
function Channel({channelId}: {channelId: string}) {
  return (
    <ChannelProvider channelId={channelId}>
      <ChannelComposer />
    </ChannelProvider>
  );
}
```

### 다른 Provider, 같은 UI

```tsx
// Provider A: 일시적 폼을 위한 로컬 상태
function ForwardMessageProvider({children}) {
  const [state, setState] = useState(initialState);
  const forwardMessage = useForwardMessage();

  return (
    <Composer.Provider state={state} actions={{update: setState, submit: forwardMessage}}>
      {children}
    </Composer.Provider>
  );
}

// Provider B: 채널을 위한 전역 동기화 상태
function ChannelProvider({channelId, children}) {
  const {state, update, submit} = useGlobalChannel(channelId);

  return (
    <Composer.Provider state={state} actions={{update, submit}}>
      {children}
    </Composer.Provider>
  );
}
```

같은 `Composer.Input` 컴포넌트가 두 Provider 모두에서 동작한다.
Context 인터페이스에만 의존하고, 구현에는 의존하지 않기 때문이다.

---

## 3. Context Interface 패턴 (의존성 주입을 위한 제네릭 인터페이스)

### 핵심 개념

컴포넌트 Context에 **state, actions, meta** 세 부분으로 구성된 **제네릭 인터페이스**를 정의한다.
이 인터페이스는 어떤 Provider든 구현할 수 있는 계약(contract)이다.
같은 UI 컴포넌트가 완전히 다른 상태 구현과 함께 동작할 수 있게 한다.

**핵심 원칙:** 상태를 끌어올리고, 내부를 조합하고, 상태를 의존성 주입 가능하게 만든다.

### ❌ Before: 특정 상태 구현에 결합된 UI

```tsx
function ComposerInput() {
  // 특정 훅에 강하게 결합됨
  const {input, setInput} = useChannelComposerState();
  return <TextInput value={input} onChangeText={setInput} />;
}
```

### ✅ After: 제네릭 인터페이스로 의존성 주입

```tsx
// 어떤 Provider든 구현할 수 있는 제네릭 인터페이스 정의
interface ComposerState {
  input: string;
  attachments: Attachment[];
  isSubmitting: boolean;
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void;
  submit: () => void;
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>;
}

interface ComposerContextValue {
  state: ComposerState;
  actions: ComposerActions;
  meta: ComposerMeta;
}

const ComposerContext = createContext<ComposerContextValue | null>(null);
```

### UI 컴포넌트는 인터페이스만 소비

```tsx
function ComposerInput() {
  const {
    state,
    actions: {update},
    meta,
  } = use(ComposerContext);

  // 이 컴포넌트는 인터페이스를 구현하는 어떤 Provider와도 동작
  return (
    <TextInput
      ref={meta.inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({...s, input: text}))}
    />
  );
}
```

### 다른 Provider들이 같은 인터페이스 구현

```tsx
// Provider A: 일시적 폼을 위한 로컬 상태
function ForwardMessageProvider({children}: {children: React.ReactNode}) {
  const [state, setState] = useState(initialState);
  const inputRef = useRef(null);
  const submit = useForwardMessage();

  return (
    <ComposerContext
      value={{
        state,
        actions: {update: setState, submit},
        meta: {inputRef},
      }}
    >
      {children}
    </ComposerContext>
  );
}

// Provider B: 채널을 위한 전역 동기화 상태
function ChannelProvider({channelId, children}: Props) {
  const {state, update, submit} = useGlobalChannel(channelId);
  const inputRef = useRef(null);

  return (
    <ComposerContext
      value={{
        state,
        actions: {update, submit},
        meta: {inputRef},
      }}
    >
      {children}
    </ComposerContext>
  );
}
```

### Provider 경계 안의 커스텀 UI

Provider 경계가 중요하다. 시각적 중첩이 아니다.
`Composer.Frame` 바깥에 있는 컴포넌트도 Provider 안에만 있으면 상태와 액션에 접근할 수 있다.

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* Composer UI */}
        <Composer.Frame>
          <Composer.Input placeholder="메시지를 추가하세요." />
          <Composer.Footer>
            <Composer.Formatting />
            <Composer.Emojis />
          </Composer.Footer>
        </Composer.Frame>

        {/* Composer 바깥이지만 Provider 안에 있는 커스텀 UI */}
        <MessagePreview />

        {/* 다이얼로그 하단의 액션 */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  );
}

// Composer.Frame 바깥에 있지만 submit 가능!
function ForwardButton() {
  const {
    actions: {submit},
  } = use(ComposerContext);
  return <Button onPress={submit}>Forward</Button>;
}

// Composer.Frame 바깥에 있지만 상태 읽기 가능!
function MessagePreview() {
  const {state} = use(ComposerContext);
  return <Preview message={state.input} attachments={state.attachments} />;
}
```

**요약:** UI는 조합해서 사용하는 재사용 가능한 조각이다. 상태는 Provider가 의존성 주입한다. Provider를 바꾸면 UI는 그대로 유지된다.
