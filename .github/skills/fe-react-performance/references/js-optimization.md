# JavaScript 마이크로 최적화 & 고급 패턴

**우선순위: 🔵 LOW-MEDIUM — 핫 패스에서 누적 효과, 일반 코드에서는 우선순위 낮음**

JavaScript 성능 최적화 6개 규칙과 고급 패턴 3개를 포함한다.
비동기 병렬 처리(`Promise.all`)는 [async-waterfall.md](async-waterfall.md)를 참고한다.

---

## JavaScript 성능 최적화

### 1. Set/Map으로 O(1) 조회

동일한 키로 여러 번 `.find()`나 `.includes()`를 호출하면 Map/Set으로 인덱스를 만든다.

**❌ 잘못된 예 (조회당 O(n)):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map((order) => ({
    ...order,
    user: users.find((u) => u.id === order.userId),
  }))
}
```

**✅ 올바른 예 (조회당 O(1)):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map((u) => [u.id, u]))
  return orders.map((order) => ({
    ...order,
    user: userById.get(order.userId),
  }))
}
```

1000 orders × 1000 users: 1,000,000 ops → 2,000 ops

**멤버십 체크에도 Set을 사용한다:**

```typescript
// ❌ 체크당 O(n)
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))

// ✅ 체크당 O(1)
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```

---

### 2. 조기 반환으로 불필요한 연산 회피

결과가 결정되면 즉시 반환하여 불필요한 처리를 건너뛴다.

**❌ 잘못된 예 (에러 발견 후에도 모든 항목 처리):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  for (const user of users) {
    if (!user.email) {
      hasError = true
    }
    // 에러 후에도 계속...
  }
  return hasError ? { valid: false } : { valid: true }
}
```

**✅ 올바른 예 (첫 에러에서 즉시 반환):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) return { valid: false, error: "Email required" }
    if (!user.name) return { valid: false, error: "Name required" }
  }
  return { valid: true }
}
```

---

### 3. 반복 함수 호출 결과를 Map으로 캐싱

동일한 입력으로 반복 호출되는 함수는 모듈 레벨 Map으로 결과를 캐싱한다.

**❌ 잘못된 예 (같은 이름에 대해 100번+ slugify):**

```typescript
function ProjectList({ projects }: Props) {
  return (
    <div>
      {projects.map(project => {
        const slug = slugify(project.name)
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**✅ 올바른 예 (고유 이름당 1회만 계산):**

```typescript
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) return slugifyCache.get(text)!
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}
```

Map(hook 아닌)을 사용하면 유틸리티, 이벤트 핸들러 등 어디서든 동작한다.

---

### 4. RegExp를 루프 밖으로 호이스팅

렌더 내에서 RegExp를 생성하지 않는다. 모듈 스코프로 호이스팅하거나 `useMemo()`로 메모이즈한다.

**❌ 잘못된 예 (매 렌더마다 새 RegExp):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, 'gi')
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**✅ 올바른 예 (호이스팅 또는 메모이즈):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, 'gi'),
    [query]
  )
  const parts = text.split(regex)
  return <>{parts.map((part, i) => ...)}</>
}
```

**⚠️ 글로벌 정규식은 mutable `lastIndex` 상태가 있다:**

```typescript
const regex = /foo/g
regex.test("foo") // true, lastIndex = 3
regex.test("foo") // false, lastIndex = 0
```

---

### 5. 레이아웃 스래싱 방지 (DOM/CSS 배치)

스타일 쓰기와 레이아웃 읽기를 번갈아 하면 동기 리플로우가 강제된다. 쓰기를 모아서 하고, 읽기는 한 번에 한다.

**❌ 잘못된 예 (읽기/쓰기 인터리빙 → 리플로우 강제):**

```typescript
function layoutThrashing(element: HTMLElement) {
  element.style.width = "100px"
  const width = element.offsetWidth // 강제 리플로우
  element.style.height = "200px"
  const height = element.offsetHeight // 또 다른 강제 리플로우
}
```

**✅ 올바른 예 (쓰기 일괄 처리 후 읽기):**

```typescript
function updateElement(element: HTMLElement) {
  element.style.width = "100px"
  element.style.height = "200px"
  // 모든 쓰기 후 읽기 (단일 리플로우)
  const { width, height } = element.getBoundingClientRect()
}
```

**더 좋은 방법: CSS 클래스 사용:**

```tsx
// React에서
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return <div className={isHighlighted ? "highlighted-box" : ""}>Content</div>
}
```

인라인 스타일보다 CSS 클래스를 선호한다. 브라우저가 캐싱하고 유지보수가 쉽다.

---

### 6. toSorted()로 불변 정렬

`.sort()`는 배열을 직접 변이하여 React 상태/props 버그를 유발한다. `.toSorted()`를 사용한다.

**❌ 잘못된 예 (원본 배열 변이):**

```typescript
const sorted = useMemo(() => users.sort((a, b) => a.name.localeCompare(b.name)), [users])
```

**✅ 올바른 예 (새 배열 생성):**

```typescript
const sorted = useMemo(() => users.toSorted((a, b) => a.name.localeCompare(b.name)), [users])
```

**이전 브라우저 대응:**

```typescript
const sorted = [...items].sort((a, b) => a.value - b.value)
```

**기타 불변 배열 메서드:** `.toReversed()`, `.toSpliced()`, `.with()`

---

## 고급 패턴

### 7. 앱 초기화는 모듈 레벨에서 1회만

앱 전체 초기화를 `useEffect([])`에 넣지 않는다. 컴포넌트가 리마운트되면 Effect가 재실행된다. 모듈 레벨 가드를 사용한다.

**❌ 잘못된 예 (dev에서 2번 실행, 리마운트 시 재실행):**

```tsx
function Comp() {
  useEffect(() => {
    loadFromStorage()
    checkAuthToken()
  }, [])
}
```

**✅ 올바른 예 (앱 로드당 1회):**

```tsx
let didInit = false

function Comp() {
  useEffect(() => {
    if (didInit) return
    didInit = true
    loadFromStorage()
    checkAuthToken()
  }, [])
}
```

---

### 8. 이벤트 핸들러를 ref에 저장

콜백이 변경될 때 Effect가 재구독하는 것을 방지하려면 ref에 저장한다.

**❌ 잘못된 예 (매 렌더마다 재구독):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}
```

**✅ 올바른 예 (안정적 구독):**

```tsx
function useWindowEvent(event: string, handler: (e) => void) {
  const handlerRef = useRef(handler)
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const listener = (e) => handlerRef.current(e)
    window.addEventListener(event, listener)
    return () => window.removeEventListener(event, listener)
  }, [event])
}
```

**대안: useEffectEvent 사용 (최신 React):**

```tsx
import { useEffectEvent } from "react"

function useWindowEvent(event: string, handler: (e) => void) {
  const onEvent = useEffectEvent(handler)
  useEffect(() => {
    window.addEventListener(event, onEvent)
    return () => window.removeEventListener(event, onEvent)
  }, [event])
}
```

---

### 9. useEffectEvent로 안정적 콜백 참조

의존성 배열에 추가하지 않고도 최신 값에 접근할 수 있다. stale closure를 방지하면서 Effect 재실행을 막는다.

**❌ 잘못된 예 (콜백 변경마다 Effect 재실행):**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("")
  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300)
    return () => clearTimeout(timeout)
  }, [query, onSearch])
}
```

**✅ 올바른 예 (useEffectEvent 사용):**

```tsx
import { useEffectEvent } from "react"

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("")
  const onSearchEvent = useEffectEvent(onSearch)

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300)
    return () => clearTimeout(timeout)
  }, [query])
}
```
