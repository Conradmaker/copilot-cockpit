---
name: fe-tailwindcss
description: "Tailwind CSS v4 styling patterns for utility-class UI implementation, theme tokens, layout helpers, and override-safe class composition. Use this skill when writing or refactoring Tailwind classes, styling components or screens, building responsive stacks or grids, defining variants with cva, merging className with cn()/tailwind-merge, or working on dark mode, animations, @theme, @utility, or CSS-to-Tailwind migration. Always consult this skill for any change to Tailwind classes or Tailwind-authored CSS, even if the user only asks to polish spacing, fix responsiveness, or clean up className conflicts. For visual direction use ds-visual-design or ds-ui-patterns; for shared component APIs use fe-ui-element-components; for accessibility use fe-a11y. Triggers on: Tailwind CSS, utility classes, className, cn(), tailwind-merge, cva, @theme, @utility, responsive styling, dark mode, animation, CSS to Tailwind, 테일윈드, 유틸리티 클래스, 클래스네임 병합, 반응형, 다크모드, 디자인 토큰."
---

# Tailwind CSS 스타일링 패턴

## 목표

Tailwind CSS v4의 CSS-first 설정, 유틸리티 클래스, 커스텀 유틸리티, 반응형/다크모드/애니메이션을 일관된 패턴으로 사용한다. `className` 병합 순서를 고정하고, variant를 선언형으로 관리하며, 토큰 기반 설계로 브랜드 교체와 테마 변경에 견디는 스타일을 만든다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 스타일링 작업을 할 때는 각각의 해당하는 reference 문서를 직접 읽고 코드 예시를 확인한 뒤 적용한다.

---

## 핵심 패턴

### 1. Tailwind v4 설정과 토큰

Tailwind v4는 `tailwind.config.ts` 대신 CSS 파일에서 직접 `@theme`으로 설정한다. 색상은 OKLCH를 사용하면 지각적 균일성이 HSL보다 좋다.

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);
  --radius-md: 0.375rem;
}
```

- `@import "tailwindcss"`로 시작한다 (`@tailwind base/components/utilities` 대신)
- `@theme` 블록에서 색상, radius, spacing, animation 토큰을 정의한다
- raw value(`#2563eb`) 대신 semantic token(`--color-primary`)을 쓴다
- `@theme inline`은 다른 CSS variable을 참조할 때, `@theme static`은 미사용 토큰도 출력할 때 쓴다

#### 빠른 판단 기준

- `bg-blue-500` 같은 raw color가 컴포넌트마다 반복되면 semantic token으로 바꿀지 먼저 본다

→ 상세: [references/theme-and-tokens.md](references/theme-and-tokens.md)

### 2. 레이아웃 유틸리티

`flex flex-col` 대신 `v-stack`, `flex flex-row` 대신 `h-stack` 같은 커스텀 유틸리티를 정의해 사용하면 의미가 더 잘 드러나고 일관성이 높아진다.

```tsx
// ❌ raw flex classes
<div className="flex flex-col gap-4">

// ✅ semantic stack utility
<div className="v-stack gap-4">
```

- `v-stack`, `h-stack`, `z-stack`, `center`, `spacer`, `circle` 유틸리티를 `@utility`로 정의한다
- 자식 요소의 `margin` 대신 부모의 `gap-*`으로 간격을 제어한다
- 반응형 방향 전환은 `v-stack lg:h-stack`으로 처리한다

#### 빠른 판단 기준

- `flex flex-col`이 보이면 `v-stack`으로 교체할지 검토한다
- 자식에 `mb-4`가 반복되면 부모의 `gap-4`로 교체한다
- 모바일/데스크톱 방향이 다르면 responsive stack 패턴을 적용한다

→ 상세: [references/layout.md](references/layout.md)

### 3. className 병합과 CVA

#### 병합 순서

모든 컴포넌트에서 `className` 병합 순서를 고정한다:

1. base styles
2. variant styles
3. state styles
4. user overrides (`className`) ← 항상 마지막

```tsx
className={cn(
  "inline-flex items-center rounded-md font-medium",  // base
  buttonVariants({ variant }),                         // variant
  disabled && "pointer-events-none opacity-50",        // state
  className,                                           // user override ← 마지막!
)}
```

#### `cn` 유틸리티

```tsx
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

- `clsx`는 조건부 class 조합, `tailwind-merge`는 같은 utility 충돌 정리를 담당한다
- 컴포넌트에서 `className`을 받을 때 반드시 `cn()`으로 병합한다
- 여러 element를 가진 컴포넌트는 `ClassNameRecord<"root" | "label" | "input">` 타입을 활용한다

#### CVA (Class Variance Authority)

variant 조합이 4~5개를 넘어가면 `cva`로 선언형 관리한다:

```tsx
const buttonVariants = cva("inline-flex items-center justify-center rounded-md font-medium", {
  variants: {
    variant: {
      primary: "bg-primary text-primary-foreground hover:bg-primary/90",
      secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
      ghost: "hover:bg-accent hover:text-accent-foreground",
    },
    size: {
      sm: "h-8 px-3 text-sm",
      md: "h-9 px-4 text-sm",
      lg: "h-10 px-6 text-base",
    },
  },
  defaultVariants: { variant: "primary", size: "md" },
})
```

#### 반복 패턴 추출

여러 컴포넌트에 반복되는 focus/disabled 규칙은 상수로 추출한다:

```tsx
export const focusRing =
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
export const disabledStyles = "disabled:pointer-events-none disabled:opacity-50"
```

#### 빠른 판단 기준

- `className` merge 순서를 설명할 수 없으면 스타일 계약이 약한 상태로 본다
- variant 조합이 5개 이상 늘어나면 `cva` 도입을 검토한다
- `cn()` 없이 className을 그대로 넘기면 Tailwind utility 충돌이 정리되지 않는다
- user override가 안 먹어서 `!important`를 고민하게 되면 merge 순서부터 다시 본다
- `focusRing`, `disabledStyles`가 3곳 이상 반복되면 상수로 추출한다

→ 상세: [references/classname-and-variants.md](references/classname-and-variants.md)

### 4. 애니메이션과 트랜지션

Tailwind v4는 `@theme` 안에서 `@keyframes`를 정의하고 `--animate-*` 변수로 연결한다.

```css
@theme {
  --animate-fade-in: fade-in 0.2s ease-out;

  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
}
```

```html
<div class="animate-fade-in">콘텐츠</div>
```

- built-in: `animate-spin`, `animate-ping`, `animate-pulse`, `animate-bounce`
- transition은 변경되는 속성만 지정한다 (`transition-colors`, `transition-transform`)
- `transition-all`은 피한다 — 성능에 불리하다
- GPU 가속 속성(`transform`, `opacity`)을 우선 사용한다
- `motion-safe:`/`motion-reduce:`로 사용자 선호를 존중한다

#### 빠른 판단 기준

- 스켈레톤 로더면 `animate-pulse`, 로딩 스피너면 `animate-spin`을 먼저 검토한다
- 300ms 이상의 UI 피드백 트랜지션은 너무 느린 것으로 본다
- `transition-all` 대신 변경되는 속성만 transition한다
- `will-change`는 정말 필요한 곳에만 — 남용하면 오히려 성능이 나빠진다

→ 상세: [references/animations.md](references/animations.md)

### 5. 다크 모드

Tailwind v4에서는 `@custom-variant`로 class-based 다크모드를 설정한다:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

- `.dark` 클래스를 root element에 토글하면 `dark:` prefix가 동작한다
- system preference와 수동 전환을 모두 지원하려면 `.system` 클래스도 추가한다
- theme color token은 light/dark에서 같은 semantic 이름, 다른 값을 매핑한다

```css
:root {
  --color-background: oklch(1 0 0);
}
.dark {
  --color-background: oklch(0.145 0 0);
}
```

#### 빠른 판단 기준

- `dark:bg-gray-900` 같은 inline override가 반복되면 CSS variable 기반 토큰으로 바꿀지 본다
- 토큰 이름에 `--light-*`, `--dark-*`를 붙이면 안 된다 — semantic name만 쓴다
- 페이지 로드 시 FOUC(flash of unstyled content)가 발생하면 ThemeProvider 구현을 확인한다

→ 상세: [references/dark-mode.md](references/dark-mode.md)

### 6. 반응형 디자인

Tailwind는 mobile-first 방식이다. base가 모바일이고, 큰 화면에서 덧붙인다.

| Prefix | Min Width | 용도                |
| ------ | --------- | ------------------- |
| `sm:`  | 640px     | 큰 폰 / 작은 태블릿 |
| `md:`  | 768px     | 태블릿              |
| `lg:`  | 1024px    | 작은 노트북         |
| `xl:`  | 1280px    | 데스크톱            |
| `2xl:` | 1536px    | 대형 화면           |

- 반응형 텍스트: `text-2xl md:text-3xl lg:text-4xl`
- show/hide: `hidden md:block`, `md:hidden`
- 입력 capability: `pointer-coarse:h-12` (터치), `hover:bg-gray-100` (hover 기기만)
- 특정 디바이스 이름("모바일", "데스크톱")보다 capability(`pointer-coarse`, `hover`)로 생각한다

#### 빠른 판단 기준

- breakpoint를 device 이름으로 부르면 capability 기반으로 다시 생각한다
- 터치 대상은 최소 44×44px을 확보한다 — `pointer-coarse:h-12 pointer-coarse:w-12`
- 텍스트가 모든 화면에서 같은 크기면 반응형 text scale을 검토한다

→ 상세: [references/responsive.md](references/responsive.md)

### 7. Affordance 클래스

element 종류와 무관하게 같은 시각적 패턴을 적용해야 할 때 `@utility`로 affordance 클래스를 정의한다:

```css
@utility ui-button {
  :where(&) {
    @apply inline-flex items-center gap-2 rounded-md px-4 py-2 text-sm font-semibold;
    @apply bg-primary text-primary-foreground shadow-sm;

    @variant hover {
      @apply bg-primary/90;
    }
    @variant focus-visible {
      @apply outline-2 outline-offset-2 outline-primary;
    }
  }
}
```

```tsx
// <button>이든 <label>이든 <a>이든 같은 모양
<label className="ui-button" htmlFor="upload">
  Choose file
</label>
```

- `@utility`로 정의하면 tree-shaking과 IntelliSense가 동작한다
- `:where()`로 감싸서 specificity를 0으로 유지한다 — utility class로 override 가능
- `ui-` prefix로 affordance임을 표시한다

→ 상세: [references/affordance-classes.md](references/affordance-classes.md)

---

## Tailwind v3 → v4 주요 변경

| v3 패턴 | v4 패턴 |
| ------ | ------ |
| `tailwind.config.ts`                  | CSS `@theme` 블록                    |
| `@tailwind base/components/utilities` | `@import "tailwindcss"`              |
| `darkMode: "class"`                   | `@custom-variant dark (...)`         |
| `theme.extend.colors`                 | `@theme { --color-*: value }`        |
| `require("tailwindcss-animate")`      | CSS `@keyframes` + `@starting-style` |
| `h-10 w-10`                           | `size-10`                            |

마이그레이션 상세 체크리스트는 [references/theme-and-tokens.md](references/theme-and-tokens.md) 참조.

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 적용 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 변경을 시작하기 전에 해당 문서를 직접 읽는다.

| 파일 | 내용 |
| --- | --- |
| `references/theme-and-tokens.md` | `@theme` 설정, OKLCH 색상, semantic token, `@theme inline`/`static`, v3→v4 마이그레이션 체크리스트 |
| `references/layout.md` | v-stack/h-stack/center/spacer `@utility` 정의, gap-first 원칙, responsive stack 패턴 |
| `references/classname-and-variants.md` | `cn()` 정의, `ClassName`/`ClassNameRecord` 타입, `cva`/`VariantProps`, 병합 순서, focusRing/disabledStyles 추출 |
| `references/animations.md` | built-in 4종, custom `@keyframes` + `--animate-*`, `@starting-style`, reduced motion, UI 애니메이션 패턴, 성능 팁 |
| `references/dark-mode.md` | `@custom-variant dark` 정의, `.dark` CSS variable override, ThemeProvider 구현, meta `theme-color` |
| `references/responsive.md` | breakpoints 테이블, responsive text scale, show/hide, spacing/sizing, `pointer-coarse`/`hover` capability |
| `references/affordance-classes.md` | `@utility` 정의 패턴, `:where()` zero specificity, `@variant` state 선언, `ui-` prefix 규칙 |

---

## 범위

- 이 스킬은 Tailwind CSS 도구와 유틸리티의 사용법을 다룬다
- UI element component API 설계 (as/asChild, prop typing, data-state, data-slot) → `fe-ui-element-components`
- React 컴포넌트 아키텍처 (composition, state management) → `fe-react-patterns`
- 접근성 (ARIA, 키보드, 시맨틱 HTML) → `fe-a11y`
- 성능 최적화 (메모이제이션, 번들, 렌더링) → `fe-react-performance`
- 일반 코드 품질 (네이밍, 파일 구조) → `fe-code-conventions`
