# 렌더링 성능

**우선순위: 🟢 MEDIUM — 하이드레이션, 조건부 렌더링, CSS/SVG 최적화**

렌더링 관련 성능을 최적화하는 9개 규칙이다.

---

## 1. 조건부 렌더링에 삼항 연산자 사용

`&&` 대신 명시적 삼항 연산자(`? :`)를 사용한다. 조건이 `0`, `NaN` 등 falsy 값일 때 의도치 않게 렌더링될 수 있다.

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

`content-visibility: auto`를 적용하면 화면 밖 요소의 레이아웃/페인트를 건너뛴다.

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
      {messages.map((msg) => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  )
}
```

1000개 메시지 기준, 브라우저가 ~990개 오프스크린 항목의 레이아웃/페인트를 건너뛴다 (10배 빠른 초기 렌더).

### 대형 리스트는 virtualization을 먼저 검토한다

반복 행이 많은 리스트를 전부 mount하면 paint보다 mount 비용이 먼저 커질 수 있다. visible range만 렌더하는 virtualization을 먼저 검토한다.

```tsx
import { VList } from "virtua"

<VList style={{ height: 400 }}>
  {items.map((item) => (
    <Row key={item.id} data={item} />
  ))}
</VList>
```

- 50개 이상 반복 렌더되는 행이나 카드 리스트는 virtualization 후보로 본다.
- virtualization이 과할 정도로 단순한 경우에는 `content-visibility: auto` 같은 CSS 전략이 더 단순할 수 있다.
- 스크롤 컨테이너 높이와 예상 item height를 함께 고려한다.

---

## 3. 하이드레이션 불일치 없이 플리커 방지

클라이언트 전용 스토리지(localStorage, 쿠키)에 의존하는 콘텐츠는 인라인 스크립트로 React 하이드레이션 전에 DOM을 업데이트한다.

**❌ 잘못된 예 (SSR 실패):**

```tsx
function ThemeWrapper({ children }: Props) {
  const theme = localStorage.getItem("theme") || "light" // 서버에서 에러
  return <div className={theme}>{children}</div>
}
```

**❌ 잘못된 예 (시각적 플리커):**

```tsx
function ThemeWrapper({ children }: Props) {
  const [theme, setTheme] = useState("light")
  useEffect(() => {
    const stored = localStorage.getItem("theme")
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

서버와 클라이언트에서 의도적으로 다른 값(랜덤 ID, 날짜, 로케일 포맷)에는 `suppressHydrationWarning`을 사용한다. 실제 버그를 숨기는 데 사용하지 않는다.

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

SVG 좌표 정밀도를 줄여 파일 크기를 줄인다.

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

많은 브라우저가 SVG 요소에 CSS3 애니메이션의 하드웨어 가속을 지원하지 않는다. SVG를 `<div>`로 감싸고 래퍼에 애니메이션을 적용한다.

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

`transform`, `opacity`, `translate`, `scale`, `rotate` 등 모든 CSS 변환/전환에 적용된다.

---

## 7. 정적 JSX를 컴포넌트 외부로 호이스팅

정적 JSX를 컴포넌트 밖으로 추출하면 매 렌더마다 재생성하는 것을 방지한다. 특히 큰 정적 SVG 노드에 유용하다.

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

> **참고:** React Compiler가 활성화되어 있으면 정적 JSX 호이스팅이 자동으로 처리된다.

---

## 8. useTransition으로 로딩 상태 관리

수동 `useState` 대신 `useTransition`을 사용하면 내장 `isPending` 상태와 자동 전환 관리를 받을 수 있다.

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
import { useTransition, useState } from "react"

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

React의 `<Activity>`를 사용하면 비용이 큰 컴포넌트의 상태/DOM을 보존하면서 가시성을 토글할 수 있다.

```tsx
import { Activity } from "react"

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? "visible" : "hidden"}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

비용이 큰 리렌더와 상태 손실을 방지한다.

---

## 10. 모션은 축소 가능하고 합성 가능한 속성만 애니메이션

애니메이션은 `transform`과 `opacity` 중심으로 구성하고, 사용자의 모션 축소 선호를 존중한다. `transition: all`은 레이아웃·페인트 비용이 큰 속성까지 전부 감시하므로 피한다.

**❌ 잘못된 예 (불필요한 속성까지 전환):**

```css
.card {
  transition: all 200ms ease;
}
```

**✅ 올바른 예 (명시적 전환 + reduced motion 대응):**

```css
.card {
  transition:
    transform 200ms ease,
    opacity 200ms ease;
}

.card:hover {
  transform: translateY(-2px);
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition-duration: 0ms;
  }

  .card:hover {
    transform: none;
  }
}
```

- 애니메이션은 가능하면 `transform`, `opacity`만 사용한다. width, height, top, left는 레이아웃 재계산을 유발한다.
- `transition: all` 대신 실제로 바뀌는 속성만 나열한다.
- 로딩 스피너, 카드 호버, 탭 전환처럼 빈도가 높은 인터랙션일수록 `prefers-reduced-motion` 대응을 함께 넣는다.

---

## 11. 레이아웃 읽기와 쓰기를 섞지 않기

렌더 중 또는 이벤트 핸들러에서 DOM 읽기와 쓰기를 번갈아 수행하면 강제 리플로우가 발생한다. 레이아웃 측정은 한 번에 읽고, 스타일 변경은 한 번에 적용한다.

**❌ 잘못된 예 (레이아웃 스래싱):**

```tsx
function resizePanel(panel: HTMLDivElement) {
  panel.style.width = "320px"
  const height = panel.offsetHeight
  panel.style.height = `${height + 40}px`
}
```

**✅ 올바른 예 (읽기/쓰기 분리):**

```tsx
function resizePanel(panel: HTMLDivElement) {
  const nextHeight = panel.offsetHeight + 40
  panel.classList.add("panel-expanded")
  panel.style.height = `${nextHeight}px`
}
```

- `getBoundingClientRect()`, `offsetWidth`, `offsetHeight`, `scrollTop` 같은 레이아웃 읽기는 렌더 함수 안에서 호출하지 않는다.
- DOM 측정이 필요하면 `useLayoutEffect`나 이벤트 핸들러에서 읽기를 먼저 모으고, 클래스 토글이나 style 변경은 뒤에서 한 번에 적용한다.
- 가능하면 JS 측정보다 flex, grid, `aspect-ratio`, `minmax()` 같은 CSS 레이아웃 기능으로 해결한다.

---

## 12. 이미지 레이아웃 시프트 방지와 지연 로드

이미지는 화면에 그려지기 전에 크기를 예측할 수 있어야 CLS가 줄어든다. 즉시 보이지 않는 이미지는 지연 로드하고, 첫 화면 핵심 이미지는 우선순위를 높인다.

**❌ 잘못된 예 (크기 미지정):**

```tsx
<img src="/hero.png" alt="제품 미리보기" />
```

**✅ 올바른 예 (크기 지정 + 로딩 전략 분리):**

```tsx
<img
  src="/gallery/item-1.png"
  alt="갤러리 썸네일"
  width="320"
  height="240"
  loading="lazy"
/>

<img
  src="/hero.png"
  alt="제품 미리보기"
  width="1440"
  height="900"
  fetchPriority="high"
/>
```

- 모든 `<img>`에는 `width`와 `height`를 명시해 레이아웃 시프트를 줄인다.
- 첫 화면 아래 이미지에는 `loading="lazy"`를 사용한다.
- LCP 후보가 되는 히어로 이미지에는 `fetchPriority="high"` 또는 프레임워크의 우선 로드 옵션을 사용한다.
