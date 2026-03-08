# 애니메이션과 트랜지션

CSS 기반 애니메이션을 Tailwind 유틸리티로 제어한다. built-in → custom @keyframes → entry/leave 순으로 검토하고, 접근성과 성능을 항상 고려한다.

---

## 1. Built-in 애니메이션

| 클래스           | 용도                       | 예시             |
| ---------------- | -------------------------- | ---------------- |
| `animate-spin`   | 로딩 스피너                | SVG 회전         |
| `animate-ping`   | 알림 뱃지, 레이더 효과     | 상대 위치 원     |
| `animate-pulse`  | 스켈레톤 로더, 대기 상태   | 회색 배경 페이드 |
| `animate-bounce` | 주의 끌기, 스크롤 안내     | 화살표 바운스    |

```html
<!-- Spinner -->
<svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
</svg>

<!-- Ping 뱃지 -->
<span class="relative flex h-3 w-3">
  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-3 w-3 bg-sky-500"></span>
</span>

<!-- Skeleton -->
<div class="animate-pulse flex space-x-4">
  <div class="rounded-full bg-gray-200 h-10 w-10"></div>
  <div class="flex-1 space-y-2 py-1">
    <div class="h-2 bg-gray-200 rounded"></div>
    <div class="h-2 bg-gray-200 rounded w-5/6"></div>
  </div>
</div>
```

---

## 2. 트랜지션 유틸리티

### 속성 지정 (권장: 필요한 것만)

| 클래스                 | 대상               |
| ---------------------- | ------------------- |
| `transition-colors`    | color, background, border |
| `transition-opacity`   | opacity             |
| `transition-transform` | transform           |
| `transition-shadow`    | shadow              |
| `transition-all`       | 모든 속성 (지양)    |

### Duration / Timing / Delay

```html
<!-- Duration: 75 100 150 200 300 500 700 1000 -->
<button class="transition-colors duration-200 hover:bg-blue-700">

<!-- Timing: ease-linear ease-in ease-out ease-in-out -->
<div class="transition-transform ease-out duration-300 hover:scale-105">

<!-- Delay: delay-75 delay-100 delay-150 delay-200 delay-300 delay-500 -->
<div class="transition-opacity delay-100 duration-300">
```

UI 피드백용 트랜지션은 100~200ms가 적당하다. 300ms를 넘기면 느리게 느껴진다.

---

## 3. 인터랙션 패턴

### Hover Card Lift

```html
<div class="transition-all duration-200 hover:-translate-y-1 hover:shadow-lg rounded-lg p-6 shadow">
  Card
</div>
```

### Button Press

```html
<button class="transition-transform duration-100 active:scale-95">
  Click
</button>
```

### Group Hover

```html
<div class="group cursor-pointer p-4 border rounded-lg hover:border-blue-500">
  <h3 class="transition-colors group-hover:text-blue-600">Title</h3>
  <span class="inline-block transition-transform group-hover:translate-x-1">→</span>
</div>
```

### Named Group Hover

```html
<div class="group/card">
  <div class="group/image relative overflow-hidden">
    <img class="transition-transform duration-300 group-hover/image:scale-110" />
  </div>
  <h3 class="transition-colors group-hover/card:text-blue-600">Title</h3>
</div>
```

---

## 4. Custom @keyframes (v4)

`@theme`에 `--animate-*`로 등록하면 `animate-*` 클래스로 사용할 수 있다.

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.4s ease-out;
  --animate-scale-in: scale-in 0.2s ease-out;
  --animate-shake: shake 0.5s ease-in-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
```

```html
<div class="animate-fade-in">Fades in</div>
<div class="animate-slide-up">Slides up</div>
<div class="animate-shake">Error shake</div>
```

### Custom Easing

```css
@theme {
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

```html
<div class="transition-transform ease-bounce duration-300 hover:scale-110">Bouncy</div>
```

---

## 5. Staggered Animation

### 인라인 delay

```html
<div class="animate-slide-up" style="animation-delay: 0ms">1</div>
<div class="animate-slide-up" style="animation-delay: 100ms">2</div>
<div class="animate-slide-up" style="animation-delay: 200ms">3</div>
```

### React 패턴

```tsx
{items.map((item, index) => (
  <div
    key={item.id}
    className="animate-slide-up opacity-0"
    style={{ animationDelay: `${index * 100}ms`, animationFillMode: "forwards" }}
  >
    {item.content}
  </div>
))}
```

---

## 6. Entry/Leave 애니메이션

### @starting-style (CSS-only entry)

popover, dialog 등 display가 전환되는 요소의 entry 애니메이션에 사용한다:

```css
[popover] {
  transition: opacity 0.2s, transform 0.2s, display 0.2s allow-discrete;
  opacity: 0;
  transform: scale(0.95);
}

[popover]:popover-open {
  opacity: 1;
  transform: scale(1);
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    transform: scale(0.95);
  }
}
```

### Headless UI Transition (JS)

JS 기반 enter/leave가 필요하면 Headless UI `Transition`을 사용한다:

```tsx
import { Transition } from "@headlessui/react";

function Modal({ isOpen, children }: { isOpen: boolean; children: React.ReactNode }) {
  return (
    <Transition
      show={isOpen}
      enter="transition-opacity duration-300"
      enterFrom="opacity-0"
      enterTo="opacity-100"
      leave="transition-opacity duration-200"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
    >
      {children}
    </Transition>
  );
}
```

### data-state 기반 (Radix 등)

```html
<div class="data-[state=open]:animate-fade-in data-[state=closed]:animate-fade-out">
  Dialog
</div>
```

---

## 7. Loading 패턴

### Shimmer Skeleton

```css
@utility skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 25%,
    var(--color-gray-300) 50%,
    var(--color-gray-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Bounce Dots

```html
<div class="flex space-x-1">
  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
  <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
</div>
```

---

## 8. 접근성: Reduced Motion

사용자가 `prefers-reduced-motion: reduce`를 설정한 경우 애니메이션을 비활성화한다.

### Tailwind variant

```html
<div class="motion-safe:animate-bounce motion-reduce:animate-none">
  Respects preferences
</div>

<button class="motion-safe:transition-all motion-safe:duration-200 motion-reduce:transition-none">
  Accessible
</button>
```

### 전역 리셋 (CSS)

```css
@media (prefers-reduced-motion: reduce) {
  *,
  ::before,
  ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 9. 성능 가이드

### GPU 가속 속성 사용

```html
<!-- 권장: GPU 가속 -->
<div class="transition-transform hover:translate-x-2">

<!-- 지양: reflow/repaint 유발 -->
<div class="transition-all hover:w-64">
```

GPU 가속되는 속성: `transform`, `opacity`
지양할 속성: `width`, `height`, `top`, `left`, `margin`, `padding`

### 구체적 트랜지션 지정

```html
<!-- 권장 -->
<div class="transition-colors duration-200 hover:bg-blue-500">

<!-- 지양: transition-all은 불필요한 속성까지 영향 -->
<div class="transition-all duration-200 hover:bg-blue-500">
```

### will-change는 신중하게

```html
<!-- 복잡하고 자주 재생되는 애니메이션에만 -->
<div class="will-change-transform animate-spin">Spinner</div>
```

---

## 빠른 체크리스트

- `transition-all` 대신 `transition-colors`, `transition-transform` 등 구체적 속성을 지정했는가?
- UI 피드백 트랜지션 duration이 100~200ms 범위인가?
- `motion-safe:` / `motion-reduce:` 또는 전역 리셋으로 reduced motion을 존중하는가?
- custom 애니메이션을 `@theme`에 `--animate-*`로 등록했는가?
- width/height/top/left를 직접 애니메이션하고 있지 않은가? → transform으로 대체
