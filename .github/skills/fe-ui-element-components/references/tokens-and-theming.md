# 토큰과 테마 아키텍처

디자인 시스템은 색을 잘 고르는 문제가 아니라, 값을 어떻게 추상화할지 결정하는 문제다. raw value를 직접 컴포넌트에 박아 넣지 않고 semantic token을 통해 읽게 만들어야 브랜드와 제품군이 바뀌어도 시스템이 버틴다.

---

## 1. Raw value보다 semantic token을 먼저 둔다

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
}
```

- `#2563eb` 같은 raw color는 theme layer 아래에 숨긴다
- 컴포넌트는 `--color-primary` 같은 semantic token을 읽는다
- 토큰 이름은 usage와 role이 드러나야 한다

---

## 2. light/dark를 포함한 theme layer를 분리한다

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
}
```

- light/dark는 동일 semantic token에 다른 raw value를 매핑하는 문제로 다룬다
- 토큰 이름 자체를 `--light-background`, `--dark-background`처럼 theme에 묶지 않는다
- multi-brand가 필요하면 brand layer를 별도로 둔다

---

## 3. 컴포넌트는 토큰 소비자여야 한다

```tsx
function Button(props: ButtonProps) {
  return (
    <button
      className="bg-[var(--color-primary)] text-[var(--color-primary-foreground)]"
      {...props}
    />
  );
}
```

- 버튼 구현이 특정 브랜드 color를 직접 알 필요는 없다
- spacing, radius, shadow도 같은 방식으로 토큰화할 수 있다
- component prop으로 해결하려는 문제와 theme token으로 해결해야 하는 문제를 구분한다

---

## 빠른 체크리스트

- raw color, radius, spacing 값이 컴포넌트마다 반복되는가?
- 같은 visual meaning을 여러 컴포넌트가 공유하는가?
- light/dark 또는 brand 변경이 예상되는가?
- 컴포넌트 코드가 theme value의 원천을 알지 않고 semantic token만 읽는가?

> **Tailwind v4 설정 상세** — `@theme`, `@import "tailwindcss"`, OKLCH, `@custom-variant`, v3→v4 마이그레이션 등 Tailwind 구현 관련 상세는 `fe-tailwindcss`를 참조한다.