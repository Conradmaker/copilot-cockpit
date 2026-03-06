# 렌더링 성능

**우선순위: 🟢 MEDIUM — 하이드레이션, 조건부 렌더링, CSS/SVG 최적화**

렌더링 관련 성능을 최적화하는 9개 규칙이에요.

---

## 1. 조건부 렌더링에 삼항 연산자 사용

`&&` 대신 명시적 삼항 연산자(`? :`)를 사용하세요. 조건이 `0`, `NaN` 등 falsy 값일 때 의도치 않게 렌더링될 수 있어요.

**❌ 잘못된 예 (count가 0이면 "0" 렌더링):**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count && <span className="badge">{count}</span>}</div>
}
// count = 0 → <div>0</div>
```

**✅ 올바른 예 (count가 0이면 아무것도 렌더링하지 않음):**

```tsx
function Badge({ count }: { count: number }) {
  return <div>{count > 0 ? <span className="badge">{count}</span> : null}</div>
}
```

---

## 2. content-visibility로 오프스크린 렌더링 지연

`content-visibility: auto`를 적용하면 화면 밖 요소의 레이아웃/페인트를 건너뛰어요.

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

1000개 메시지 기준, 브라우저가 ~990개 오프스크린 항목의 레이아웃/페인트를 건너뛰어요 (10배 빠른 초기 렌더).

---

## 3. 하이드레이션 불일치 없이 플리커 방지

클라이언트 전용 스토리지(localStorage, 쿠키)에 의존하는 콘텐츠는 인라인 스크립트로 React 하이드레이션 전에 DOM을 업데이트하세요.

**❌ 잘못된 예 (SSR 실패):**

```tsx
function ThemeWrapper({ children }: Props) {
  const theme = localStorage.getItem('theme') || 'light' // 서버에서 에러
  return <div className={theme}>{children}</div>
}
```

**❌ 잘못된 예 (시각적 플리커):**

```tsx
function ThemeWrapper({ children }: Props) {
  const [theme, setTheme] = useState('light')
  useEffect(() => {
    const stored = localStorage.getItem('theme')
    if (stored) setTheme(stored)
  }, [])
  // 하이드레이션 후 깜빡임 발생
}
```

**✅ 올바른 예 (플리커 없음, 하이드레이션 불일치 없음):**

```tsx
function ThemeWrapper({ children }: Props) {
  return (
    <>
      <div id="theme-wrapper">{children}</div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

**활용:** 테마 토글, 사용자 선호 설정, 인증 상태 등 클라이언트 전용 데이터

---

## 4. 예상된 하이드레이션 불일치 억제

서버와 클라이언트에서 의도적으로 다른 값(랜덤 ID, 날짜, 로케일 포맷)에는 `suppressHydrationWarning`을 사용하세요. 실제 버그를 숨기는 데 사용하지 마세요.

**❌ 잘못된 예 (불필요한 경고):**

```tsx
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}
```

**✅ 올바른 예 (예상된 불일치만 억제):**

```tsx
function Timestamp() {
  return <span suppressHydrationWarning>{new Date().toLocaleString()}</span>
}
```

---

## 5. SVG 좌표 정밀도 최적화

SVG 좌표 정밀도를 줄여 파일 크기를 줄이세요.

**❌ 과도한 정밀도:**

```svg
<path d="M 10.293847 20.847362 L 30.938472 40.192837" />
```

**✅ 적절한 정밀도 (소수 1자리):**

```svg
<path d="M 10.3 20.8 L 30.9 40.2" />
```

**SVGO로 자동화:**

```bash
npx svgo --precision=1 --multipass icon.svg
```

---

## 6. SVG 애니메이션은 래퍼 div에 적용

많은 브라우저가 SVG 요소에 CSS3 애니메이션의 하드웨어 가속을 지원하지 않아요. SVG를 `<div>`로 감싸고 래퍼에 애니메이션을 적용하세요.

**❌ 잘못된 예 (SVG에 직접 애니메이션 — 하드웨어 가속 없음):**

```tsx
function LoadingSpinner() {
  return (
    <svg className="animate-spin" width="24" height="24" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  )
}
```

**✅ 올바른 예 (래퍼 div 애니메이션 — GPU 가속):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  )
}
```

`transform`, `opacity`, `translate`, `scale`, `rotate` 등 모든 CSS 변환/전환에 적용돼요.

---

## 7. 정적 JSX를 컴포넌트 외부로 호이스팅

정적 JSX를 컴포넌트 밖으로 추출하면 매 렌더마다 재생성하는 것을 방지해요. 특히 큰 정적 SVG 노드에 유용해요.

**❌ 잘못된 예 (매 렌더마다 요소 재생성):**

```tsx
function Container() {
  return <div>{loading && <div className="animate-pulse h-20 bg-gray-200" />}</div>
}
```

**✅ 올바른 예 (동일 요소 재사용):**

```tsx
const loadingSkeleton = <div className="animate-pulse h-20 bg-gray-200" />

function Container() {
  return <div>{loading && loadingSkeleton}</div>
}
```

> **참고:** React Compiler가 활성화되어 있으면 정적 JSX 호이스팅이 자동으로 처리돼요.

---

## 8. useTransition으로 로딩 상태 관리

수동 `useState` 대신 `useTransition`을 사용하면 내장 `isPending` 상태와 자동 전환 관리를 받을 수 있어요.

**❌ 잘못된 예 (수동 로딩 상태):**

```tsx
function SearchResults() {
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (value: string) => {
    setIsLoading(true)
    const data = await fetchResults(value)
    setResults(data)
    setIsLoading(false)
  }
}
```

**✅ 올바른 예 (useTransition):**

```tsx
import { useTransition, useState } from 'react'

function SearchResults() {
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (value: string) => {
    startTransition(async () => {
      const data = await fetchResults(value)
      setResults(data)
    })
  }
  // isPending으로 로딩 표시
}
```

**장점:** 자동 pending 상태, 에러 시에도 올바른 리셋, 더 나은 반응성, 인터럽트 처리

---

## 9. Activity 컴포넌트로 상태 보존하며 토글

React의 `<Activity>`를 사용하면 비용이 큰 컴포넌트의 상태/DOM을 보존하면서 가시성을 토글할 수 있어요.

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

비용이 큰 리렌더와 상태 손실을 방지해요.
