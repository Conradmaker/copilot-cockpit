# 컴포지션 패턴

React 컴포넌트를 설계할 때 사용하는 합성(Composition) 패턴들을 정리한 문서다. "설정(Configuration)보다 조합(Composition)"이라는 핵심 철학을 구체적인 패턴과 코드 예제로 설명한다.

---

## 1. Boolean Props 지양

### 왜 피해야 하나?

Boolean prop이 추가될 때마다 가능한 상태 조합은 **2배**로 늘어난다. `isThread`, `isEditing`, `isDMThread`, `isForwarding` 같은 prop이 4개만 있어도 16가지 조합이 생긴다. 대부분의 조합은 의미가 없거나 불가능한 상태(impossible state)다.

### ❌ Before: Boolean props로 커스터마이징

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  dmId,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField id={dmId} />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? <EditActions /> : isForwarding ? <ForwardActions /> : <DefaultActions />}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

### ✅ After: Composition으로 대체

```tsx
// 채널 컴포저
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 스레드 컴포저 - "채널에도 전송" 필드 추가
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// 편집 컴포저 - 다른 Footer 액션
function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

각 variant가 무엇을 렌더링하는지 명시적이다. 공유 가능한 내부 컴포넌트를 조합하면서도 하나의 거대한 부모 컴포넌트를 공유하지 않는다.

---

## 2. Compound Components 패턴

### 핵심 개념

복잡한 컴포넌트를 공유 컨텍스트를 가진 여러 하위 컴포넌트로 구조화하는 패턴이다. 각 하위 컴포넌트는 props가 아닌 context를 통해 공유 상태에 접근한다. 소비자(consumer)는 필요한 조각만 조합해서 사용한다.

### ❌ Before: 모놀리식 컴포넌트 (render props)

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
  showAttachments,
  showFormatting,
  showEmojis,
}: Props) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {showAttachments && <Attachments />}
      {renderFooter ? (
        renderFooter()
      ) : (
        <Footer>
          {showFormatting && <Formatting />}
          {showEmojis && <Emojis />}
          {renderActions?.()}
        </Footer>
      )}
    </form>
  )
}
```

### ✅ After: Compound Components

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return <ComposerContext value={{ state, actions, meta }}>{children}</ComposerContext>
}

function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

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

// Compound component로 export
const Composer = {
  Provider: ComposerProvider,
  Frame: ComposerFrame,
  Input: ComposerInput,
  Submit: ComposerSubmit,
  Header: ComposerHeader,
  Footer: ComposerFooter,
  Attachments: ComposerAttachments,
  Formatting: ComposerFormatting,
  Emojis: ComposerEmojis,
}
```

**사용 예시:**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

소비자가 필요한 것만 명시적으로 조합한다. 숨겨진 조건문이 없다. state, actions, meta는 부모 Provider에서 의존성 주입되어서 같은 컴포넌트 구조를 여러 곳에서 재사용할 수 있다.

---

## 3. Explicit Variants (명시적 Variant 컴포넌트)

### 핵심 개념

하나의 컴포넌트에 많은 boolean props를 추가하는 대신, 명시적인 variant 컴포넌트를 만든다. 각 variant는 필요한 조각만 조합한다. 코드 자체가 문서화된다.

### ❌ Before: 하나의 컴포넌트, 많은 모드

```tsx
// 이 컴포넌트가 실제로 무엇을 렌더링하는지 알 수 없음
<Composer isThread isEditing={false} channelId="abc" showAttachments showFormatting={false} />
```

### ✅ After: 명시적 Variant

```tsx
// 즉시 무엇을 렌더링하는지 알 수 있음
<ThreadComposer channelId="abc" />
<EditMessageComposer messageId="xyz" />
<ForwardMessageComposer messageId="123" />
```

**구현:**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <EditMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditMessageProvider>
  )
}
```

각 variant는 다음을 명시적으로 보여준다:

- 어떤 Provider/상태를 사용하는지
- 어떤 UI 요소를 포함하는지
- 어떤 액션을 제공하는지

Boolean prop 조합을 추론할 필요가 없다. 불가능한 상태가 없다.

---

## 4. Children over Render Props

### 핵심 개념

`renderX` props 대신 `children`으로 조합한다. children은 더 읽기 쉽고, 자연스럽게 조합되며, 콜백 시그니처를 이해할 필요가 없다.

### ❌ Before: Render Props

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode
  renderFooter?: () => React.ReactNode
  renderActions?: () => React.ReactNode
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  )
}

// 사용이 어색하고 유연하지 않음
<Composer
  renderHeader={() => <CustomHeader />}
  renderFooter={() => (
    <>
      <Formatting />
      <Emojis />
    </>
  )}
  renderActions={() => <SubmitButton />}
/>
```

### ✅ After: Children으로 조합

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className="flex">{children}</footer>
}

// 유연한 사용
<Composer.Frame>
  <CustomHeader />
  <Composer.Input />
  <Composer.Footer>
    <Composer.Formatting />
    <Composer.Emojis />
    <SubmitButton />
  </Composer.Footer>
</Composer.Frame>
```

### Render Props가 적절한 경우

부모가 자식에게 데이터를 전달해야 할 때는 render props가 적절하다:

```tsx
<List data={items} renderItem={({ item, index }) => <Item item={item} index={index} />} />
```

**원칙:** 정적 구조를 조합할 때는 `children`, 데이터/상태를 자식에게 전달해야 할 때는 render props.

---

## 5. Props Drilling → Composition 패턴

### 문제

Props Drilling은 부모 컴포넌트와 자식 컴포넌트 사이에 결합도가 생겼다는 명확한 신호다. prop 이름이 변경되면 해당 prop을 참조하는 **모든 컴포넌트**를 수정해야 한다.

### ❌ Before: Props Drilling

```tsx
function ItemEditModal({ open, items, recommendedItems, onConfirm, onClose }) {
  const [keyword, setKeyword] = useState("")

  return (
    <Modal open={open} onClose={onClose}>
      <ItemEditBody
        items={items}
        keyword={keyword}
        onKeywordChange={setKeyword}
        recommendedItems={recommendedItems}
        onConfirm={onConfirm}
        onClose={onClose}
      />
    </Modal>
  )
}

function ItemEditBody({ keyword, onKeywordChange, items, recommendedItems, onConfirm, onClose }) {
  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Input value={keyword} onChange={(e) => onKeywordChange(e.target.value)} />
        <Button onClick={onClose}>닫기</Button>
      </div>
      <ItemEditList
        keyword={keyword}
        items={items}
        recommendedItems={recommendedItems}
        onConfirm={onConfirm}
      />
    </>
  )
}
```

### ✅ After (단계 A): Composition 패턴으로 depth 줄이기

```tsx
function ItemEditModal({ open, items, recommendedItems, onConfirm, onClose }) {
  const [keyword, setKeyword] = useState("")

  return (
    <Modal open={open} onClose={onClose}>
      <ItemEditBody keyword={keyword} onKeywordChange={setKeyword} onClose={onClose}>
        <ItemEditList
          keyword={keyword}
          items={items}
          recommendedItems={recommendedItems}
          onConfirm={onConfirm}
        />
      </ItemEditBody>
    </Modal>
  )
}

function ItemEditBody({ children, keyword, onKeywordChange, onClose }) {
  return (
    <>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Input value={keyword} onChange={(e) => onKeywordChange(e.target.value)} />
        <Button onClick={onClose}>닫기</Button>
      </div>
      {children}
    </>
  )
}
```

`children`을 사용해서 불필요한 Props Drilling(`items`, `recommendedItems`, `onConfirm`)을 줄인다.

### ✅ After (단계 B): Context API로 완전 해결

Composition만으로 해결되지 않고 트리가 깊다면 Context API를 활용한다:

```tsx
function ItemEditModal({ open, onConfirm, onClose }) {
  const [keyword, setKeyword] = useState("")

  return (
    <Modal open={open} onClose={onClose}>
      <ItemEditBody keyword={keyword} onKeywordChange={setKeyword} onClose={onClose}>
        <ItemEditList keyword={keyword} onConfirm={onConfirm} />
      </ItemEditBody>
    </Modal>
  )
}

function ItemEditList({ keyword, onConfirm }) {
  // Context에서 데이터를 직접 가져옴
  const { items, recommendedItems } = useItemEditModalContext()
  // ...
}
```

### Props Drilling 해결 우선순위

1. **`children` prop으로 depth 줄이기** — 단순히 값을 전달하기 위한 중간 컴포넌트가 있다면 먼저 시도
2. **Composition 패턴으로 구조 변경** — 불필요한 중간 추상화를 제거
3. **Context API 사용** — 위 방법으로 해결이 안 될 때 최후의 수단으로 사용

> ⚠️ 컴포넌트의 역할과 의도를 담고 있는 props라면 Drilling이 되더라도 문제가 되지 않을 수 있다.

---

## 6. 컴포넌트 분리 전략

> 이 패턴들은 `fe-code-conventions`의 가독성/결합도 원칙에서도 다루지만, 여기서는 React 컴포넌트 관점에서 설명한다.

### 6-1. 동시에 실행되지 않는 코드 분리하기

동시에 실행되지 않는 코드가 하나의 컴포넌트에 있으면, 코드를 읽는 사람이 한 번에 고려해야 하는 맥락이 많아진다.

#### ❌ Before: 분기가 섞인 컴포넌트

```tsx
function SubmitButton() {
  const isViewer = useRole() === "viewer"

  useEffect(() => {
    if (isViewer) {
      return
    }
    showButtonAnimation()
  }, [isViewer])

  return isViewer ? <TextButton disabled>Submit</TextButton> : <Button type="submit">Submit</Button>
}
```

#### ✅ After: 역할별 분리

```tsx
function SubmitButton() {
  const isViewer = useRole() === "viewer"
  return isViewer ? <ViewerSubmitButton /> : <AdminSubmitButton />
}

function ViewerSubmitButton() {
  return <TextButton disabled>Submit</TextButton>
}

function AdminSubmitButton() {
  useEffect(() => {
    showButtonAnimation()
  }, [])

  return <Button type="submit">Submit</Button>
}
```

- 분기가 한 곳에서 단 하나로 합쳐짐
- 각 컴포넌트는 하나의 역할만 담당

### 6-2. 구현 상세 추상화하기 (HOC / Wrapper 패턴)

한 사람이 코드를 읽을 때 동시에 고려할 수 있는 맥락은 제한되어 있다. 구현 상세를 추상화해 읽는 사람이 한 번에 고려해야 하는 맥락을 줄인다.

#### ❌ Before: 구현 상세가 노출된 컴포넌트

```tsx
function LoginStartPage() {
  useCheckLogin({
    onChecked: (status) => {
      if (status === "LOGGED_IN") {
        location.href = "/home"
      }
    },
  })

  /* ... 로그인 관련 로직 ... */
  return <>{/* ... 로그인 관련 컴포넌트 ... */}</>
}
```

#### ✅ After (옵션 A): Wrapper 컴포넌트

```tsx
function App() {
  return (
    <AuthGuard>
      <LoginStartPage />
    </AuthGuard>
  )
}

function AuthGuard({ children }) {
  const status = useCheckLoginStatus()

  useEffect(() => {
    if (status === "LOGGED_IN") {
      location.href = "/home"
    }
  }, [status])

  return status !== "LOGGED_IN" ? children : null
}

function LoginStartPage() {
  /* ... 로그인 관련 로직만 ... */
  return <>{/* ... 로그인 관련 컴포넌트 ... */}</>
}
```

#### ✅ After (옵션 B): HOC

```tsx
function LoginStartPage() {
  /* ... 로그인 관련 로직만 ... */
  return <>{/* ... 로그인 관련 컴포넌트 ... */}</>
}

export default withAuthGuard(LoginStartPage)

function withAuthGuard(WrappedComponent) {
  return function AuthGuard(props) {
    const status = useCheckLoginStatus()

    useEffect(() => {
      if (status === "LOGGED_IN") {
        location.href = "/home"
      }
    }, [status])

    return status !== "LOGGED_IN" ? <WrappedComponent {...props} /> : null
  }
}
```

### 6-3. 관련 로직과 UI를 함께 추상화하기

자주 함께 수정되는 로직과 UI가 멀리 떨어져 있으면 함께 수정되지 못할 위험이 있다. 관련된 로직과 UI를 하나의 컴포넌트로 묶어서 응집도를 높인다.

#### ❌ Before: 로직과 UI가 분리됨

```tsx
function FriendInvitation() {
  const { data } = useQuery(/* ... */)

  const handleClick = async () => {
    const canInvite = await overlay.openAsync(({ isOpen, close }) => (
      <ConfirmDialog
        title={`${data.name}님에게 공유해요`}
        cancelButton={
          <ConfirmDialog.CancelButton onClick={() => close(false)}>닫기</ConfirmDialog.CancelButton>
        }
        confirmButton={
          <ConfirmDialog.ConfirmButton onClick={() => close(true)}>
            확인
          </ConfirmDialog.ConfirmButton>
        }
      />
    ))

    if (canInvite) {
      await sendPush()
    }
  }

  return (
    <>
      <Button onClick={handleClick}>초대하기</Button>
      {/* 다른 UI ... */}
    </>
  )
}
```

#### ✅ After: 관련 로직을 함께 추상화

```tsx
function FriendInvitation() {
  const { data } = useQuery(/* ... */)

  return (
    <>
      <InviteButton name={data.name} />
      {/* 다른 UI ... */}
    </>
  )
}

function InviteButton({ name }) {
  return (
    <Button
      onClick={async () => {
        const canInvite = await overlay.openAsync(({ isOpen, close }) => (
          <ConfirmDialog
            title={`${name}님에게 공유해요`}
            cancelButton={
              <ConfirmDialog.CancelButton onClick={() => close(false)}>
                닫기
              </ConfirmDialog.CancelButton>
            }
            confirmButton={
              <ConfirmDialog.ConfirmButton onClick={() => close(true)}>
                확인
              </ConfirmDialog.ConfirmButton>
            }
          />
        ))

        if (canInvite) {
          await sendPush()
        }
      }}
    >
      초대하기
    </Button>
  )
}
```

버튼과 클릭 후 실행되는 로직이 아주 가까이에 있어서, 한 번에 인지해야 하는 맥락이 줄어들고 응집도가 높아진다.
