# 리렌더 최적화

**우선순위: 🟢 MEDIUM — 불필요한 리렌더를 줄여 UI 반응성 개선**

불필요한 리렌더를 줄이고, 상태 관리를 최적화하는 12개 규칙이다.

> **참고:** 프로젝트에 [React Compiler](https://react.dev/learn/react-compiler)가 활성화되어 있다면, `memo()`, `useMemo()`, `useCallback()`의 수동 메모이제이션이 자동화된다. 하지만 함수형 setState, 파생 상태 등의 패턴은 여전히 수동 적용이 필요하다.

---

## 1. 단순 표현식에 useMemo 사용 금지

결과가 원시 타입(boolean, number, string)인 간단한 표현식은 `useMemo`로 감싸지 않는다. `useMemo` 호출과 의존성 비교가 표현식 자체보다 비용이 클 수 있다.

**❌ 잘못된 예:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading
  }, [user.isLoading, notifications.isLoading])
  if (isLoading) return <Skeleton />
}
```

**✅ 올바른 예:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading
  if (isLoading) return <Skeleton />
}
```

---

## 2. 비용이 큰 작업을 memo() 컴포넌트로 분리

비싼 연산을 메모이즈된 컴포넌트로 추출하면, 로딩 상태 등에서 조기 반환이 가능하다.

**❌ 잘못된 예 (로딩 중에도 avatar 계산):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user)
    return <Avatar id={id} />
  }, [user])
  if (loading) return <Skeleton />
  return <div>{avatar}</div>
}
```

**✅ 올바른 예 (로딩 시 연산 건너뛰기):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  )
}
```

---

## 3. 비원시 타입 기본값을 상수로 호이스팅

메모이즈된 컴포넌트의 비원시 타입 기본값(배열, 함수, 객체)은 매 리렌더마다 새 인스턴스가 생성되어 메모이제이션이 깨진다.

**❌ 잘못된 예 (onClick이 매 리렌더마다 다른 값):**

```tsx
const UserAvatar = memo(function UserAvatar({ onClick = () => {} }: Props) {
  // ...
})
```

**✅ 올바른 예 (안정적인 기본값):**

```tsx
const NOOP = () => {}

const UserAvatar = memo(function UserAvatar({ onClick = NOOP }: Props) {
  // ...
})
```

---

## 4. 파생 상태는 렌더 중 계산 (Effect 사용 금지)

현재 props/state에서 계산할 수 있는 값은 상태에 저장하거나 Effect에서 업데이트하지 않는다. 렌더링 중 직접 계산하면 추가 리렌더와 상태 동기화 문제를 피할 수 있다.

**❌ 잘못된 예 (불필요한 상태와 Effect):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState("First")
  const [lastName, setLastName] = useState("Last")
  const [fullName, setFullName] = useState("")

  useEffect(() => {
    setFullName(firstName + " " + lastName)
  }, [firstName, lastName])
}
```

**✅ 올바른 예 (렌더 중 계산):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState("First")
  const [lastName, setLastName] = useState("Last")
  const fullName = firstName + " " + lastName
}
```

---

## 5. 파생 boolean 구독으로 리렌더 빈도 줄이기

연속적으로 변하는 값 대신 파생된 boolean 상태를 구독하면 리렌더 빈도를 줄일 수 있다.

**❌ 잘못된 예 (매 픽셀 변경마다 리렌더):**

```tsx
function Sidebar() {
  const width = useWindowWidth() // 지속적으로 업데이트
  const isMobile = width < 768
  return <nav className={isMobile ? "mobile" : "desktop"} />
}
```

**✅ 올바른 예 (boolean 전환 시에만 리렌더):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery("(max-width: 767px)")
  return <nav className={isMobile ? "mobile" : "desktop"} />
}
```

---

## 6. 함수형 setState로 안정적 콜백

상태를 현재 값 기반으로 업데이트할 때 함수형 업데이트를 사용하면, stale closure를 방지하고 안정적인 콜백 참조를 만들 수 있다.

**❌ 잘못된 예 (items 변경마다 콜백 재생성):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)

  const addItems = useCallback(
    (newItems: Item[]) => {
      setItems([...items, ...newItems])
    },
    [items],
  ) // items 의존성으로 매번 재생성

  const removeItem = useCallback((id: string) => {
    setItems(items.filter((item) => item.id !== id))
  }, []) // items 누락 → stale closure 버그!
}
```

**✅ 올바른 예 (안정적 콜백, stale closure 없음):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems)

  const addItems = useCallback((newItems: Item[]) => {
    setItems((curr) => [...curr, ...newItems])
  }, []) // 의존성 불필요

  const removeItem = useCallback((id: string) => {
    setItems((curr) => curr.filter((item) => item.id !== id))
  }, []) // 안전하고 안정적
}
```

**함수형 업데이트 사용 시기:** 현재 상태 기반 setState, useCallback 내 상태 참조, 이벤트 핸들러, 비동기 작업

**직접 업데이트가 괜찮은 경우:** `setCount(0)`, `setName(newName)` 등 이전 값에 의존하지 않을 때

---

## 7. useState 지연 초기화

비용이 큰 초기값은 함수 형태로 `useState`에 전달한다. 함수 형태가 아니면 매 렌더마다 초기화 코드가 실행된다.

**❌ 잘못된 예 (매 렌더마다 실행):**

```tsx
const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items))
const [settings, setSettings] = useState(JSON.parse(localStorage.getItem("settings") || "{}"))
```

**✅ 올바른 예 (초기 렌더 시에만 실행):**

```tsx
const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items))
const [settings, setSettings] = useState(() => {
  const stored = localStorage.getItem("settings")
  return stored ? JSON.parse(stored) : {}
})
```

**지연 초기화 사용 시기:** localStorage/sessionStorage 읽기, 데이터 구조 빌드(인덱스, 맵), DOM 읽기, 무거운 변환

---

## 8. startTransition으로 비긴급 업데이트 처리

빈번하고 비긴급한 상태 업데이트를 transition으로 표시하면 UI 반응성을 유지할 수 있다.

**❌ 잘못된 예 (매 스크롤에 UI 블로킹):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY)
    window.addEventListener("scroll", handler, { passive: true })
    return () => window.removeEventListener("scroll", handler)
  }, [])
}
```

**✅ 올바른 예 (비차단 업데이트):**

```tsx
import { startTransition } from "react"

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0)
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY))
    }
    window.addEventListener("scroll", handler, { passive: true })
    return () => window.removeEventListener("scroll", handler)
  }, [])
}
```

---

## 9. Effect 의존성 좁히기

객체 대신 원시 타입 의존성을 지정하여 Effect 재실행을 최소화한다.

**❌ 잘못된 예 (user의 아무 필드 변경에도 재실행):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user])
```

**✅ 올바른 예 (id 변경 시에만 재실행):**

```tsx
useEffect(() => {
  console.log(user.id)
}, [user.id])
```

**파생 상태로 의존성 최적화:**

```tsx
// ❌ width=767, 766, 765... 매번 실행
useEffect(() => {
  if (width < 768) enableMobileMode()
}, [width])

// ✅ boolean 전환 시에만 실행
const isMobile = width < 768
useEffect(() => {
  if (isMobile) enableMobileMode()
}, [isMobile])
```

---

## 10. 콜백에서만 쓰는 상태는 구독하지 않기

동적 상태(searchParams, localStorage)를 콜백 내에서만 읽는다면, 구독하지 말고 필요할 때 직접 읽는다.

**❌ 잘못된 예 (모든 searchParams 변경에 구독):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams()
  const handleShare = () => {
    const ref = searchParams.get("ref")
    shareChat(chatId, { ref })
  }
  return <button onClick={handleShare}>Share</button>
}
```

**✅ 올바른 예 (온디맨드 읽기, 구독 없음):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search)
    const ref = params.get("ref")
    shareChat(chatId, { ref })
  }
  return <button onClick={handleShare}>Share</button>
}
```

---

## 11. 상호작용 로직은 이벤트 핸들러에

특정 사용자 액션(submit, click)에 의해 트리거되는 부수 효과는 해당 이벤트 핸들러에서 실행한다. state + effect 패턴으로 모델링하면 관련 없는 변경에도 Effect가 재실행된다.

**❌ 잘못된 예 (이벤트를 state + effect로 모델링):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false)
  const theme = useContext(ThemeContext)

  useEffect(() => {
    if (submitted) {
      post("/api/register")
      showToast("Registered", theme)
    }
  }, [submitted, theme]) // theme 변경에도 재실행!
}
```

**✅ 올바른 예 (핸들러에서 직접 실행):**

```tsx
function Form() {
  const theme = useContext(ThemeContext)
  function handleSubmit() {
    post("/api/register")
    showToast("Registered", theme)
  }
  return <button onClick={handleSubmit}>Submit</button>
}
```

---

## 12. 자주 변하는 일시적 값에 useRef 사용

자주 변하지만 리렌더가 필요 없는 값(마우스 트래커, 인터벌, 일시적 플래그)은 `useRef`에 저장한다.

**❌ 잘못된 예 (매 업데이트마다 렌더):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0)
  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX)
    window.addEventListener("mousemove", onMove)
    return () => window.removeEventListener("mousemove", onMove)
  }, [])
  return <div style={{ left: lastX }} />
}
```

**✅ 올바른 예 (리렌더 없이 DOM 직접 업데이트):**

```tsx
function Tracker() {
  const lastXRef = useRef(0)
  const dotRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX
      if (dotRef.current) {
        dotRef.current.style.transform = `translateX(${e.clientX}px)`
      }
    }
    window.addEventListener("mousemove", onMove)
    return () => window.removeEventListener("mousemove", onMove)
  }, [])

  return <div ref={dotRef} style={{ transform: "translateX(0px)" }} />
}
```
