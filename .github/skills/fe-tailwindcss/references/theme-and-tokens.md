# Tailwind v4 설정과 토큰

Tailwind v4는 JavaScript 설정 파일을 CSS-first 설정으로 대체한다. `@theme` 블록에서 디자인 토큰을 직접 정의하고, OKLCH 색공간을 활용해 지각적으로 균일한 색상 체계를 만든다.

---

## 1. 기본 설정 구조

```css
/* app.css */
@import "tailwindcss";

@theme {
  /* Semantic color tokens — OKLCH */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);
  --color-ring-offset: oklch(100% 0 0);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
  }
}
```

- `@import "tailwindcss"`로 시작한다 (`@tailwind base/components/utilities` 대신)
- `@theme` 블록에서 `--color-*`, `--radius-*`, `--spacing-*` 등을 정의한다
- OKLCH는 HSL보다 지각적 균일성이 뛰어나다 — 같은 lightness 값이 실제로 같은 밝기로 보인다

---

## 2. 토큰 계층

```
Brand Tokens (abstract)
    └── Semantic Tokens (purpose)
        └── Component Tokens (specific)

예시:
    oklch(45% 0.2 260) → --color-primary → bg-primary
```

- raw value(`#2563eb`)를 컴포넌트에 직접 쓰지 않는다
- semantic token(`bg-primary`)을 통해 접근한다
- 토큰 이름은 용도와 역할이 드러나야 한다 (`--color-primary`, `--color-muted-foreground`)

---

## 3. @theme 변형

### `@theme inline` — 다른 CSS variable 참조 시

```css
@theme inline {
  --font-sans: var(--font-inter), system-ui;
  --color-background: var(--background);
}
```

### `@theme static` — 미사용 토큰도 항상 출력

```css
@theme static {
  --color-brand: oklch(65% 0.15 240);
}
```

### Namespace override — 기본값 초기화 후 재정의

```css
@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-black: #000;
  --color-primary: oklch(45% 0.2 260);
}
```

---

## 4. Semi-transparent 색상 변형

```css
@theme {
  --color-primary-50: color-mix(in oklab, var(--color-primary) 5%, transparent);
  --color-primary-100: color-mix(in oklab, var(--color-primary) 10%, transparent);
  --color-primary-200: color-mix(in oklab, var(--color-primary) 20%, transparent);
}
```

---

## 5. Container query 토큰

```css
@theme {
  --container-xs: 20rem;
  --container-sm: 24rem;
  --container-md: 28rem;
  --container-lg: 32rem;
}
```

---

## 6. Animation 토큰

```css
@theme {
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-out: fade-out 0.2s ease-in;
  --animate-slide-in: slide-in 0.3s ease-out;

  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes fade-out {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }

  @keyframes slide-in {
    from {
      transform: translateY(-0.5rem);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
}
```

---

## v3 → v4 마이그레이션 체크리스트

- [ ] `tailwind.config.ts` → CSS `@theme` 블록으로 이동
- [ ] `@tailwind base/components/utilities` → `@import "tailwindcss"`
- [ ] `theme.extend.colors` → `@theme { --color-*: value }`
- [ ] `darkMode: "class"` → `@custom-variant dark`
- [ ] `@keyframes`를 `@theme` 블록 안으로 이동
- [ ] `require("tailwindcss-animate")` → native CSS animations
- [ ] `h-10 w-10` → `size-10` (새 shorthand)
- [ ] OKLCH 색상 도입 검토
- [ ] custom plugin → `@utility` directive로 교체
- [ ] arbitrary values → `@theme` 확장으로 교체

---

## 빠른 체크리스트

- `tailwind.config.ts`가 남아 있는가? `@theme`으로 옮겼는가?
- raw color가 컴포넌트에 반복되는가? semantic token으로 바꿔야 하는가?
- 토큰 이름이 용도와 역할을 설명하는가?
- OKLCH를 사용하고 있는가?
- `@theme inline`/`static` 구분이 맞는가?
