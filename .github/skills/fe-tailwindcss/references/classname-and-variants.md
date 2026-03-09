# className 병합과 Variant API

Tailwind CSS 컴포넌트에서 className 병합 순서를 고정하고, `cn()` 유틸리티로 충돌을 정리하고, `cva`로 variant를 선언형으로 관리한다.

---

## 1. `cn` 유틸리티 정의

```ts
import type { ClassValue } from "clsx";
import type { CSSProperties } from "react";

import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export type ClassName = ClassValue;
export type ClassNameRecord<Key extends string> = { [K in Key]?: ClassName };

type Style = CSSProperties & { [key: `--${string}`]: string };
export type StyleRecord<Key extends string> = { [K in Key]?: Style };

export function cn(...classes: ClassName[]): string {
  return twMerge(clsx(...classes));
}
```

- `clsx`: 조건부 class 조합을 처리한다 (객체, 배열, 문자열, undefined 모두 지원)
- `tailwind-merge`: 같은 Tailwind utility 충돌을 정리한다 (`px-4` + `px-6` → `px-6`)
- 둘을 합친 `cn` 유틸을 공유하면 호출부가 단순해진다

---

## 2. 병합 순서 (고정)

모든 컴포넌트에서 아래 순서를 지킨다:

1. **base** — 항상 적용되는 기본 스타일
2. **variant** — variant prop에 따라 적용
3. **state** — boolean/data attribute에 따라 적용
4. **user override** — `className` prop (항상 마지막)

```tsx
function Button({ variant = "primary", className, disabled, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        // 1. base
        "inline-flex items-center rounded-md font-medium",
        // 2. variant
        buttonVariants({ variant }),
        // 3. state
        disabled && "pointer-events-none opacity-50",
        // 4. user override — 항상 마지막!
        className,
      )}
      disabled={disabled}
      {...props}
    />
  );
}
```

- `className`이 마지막이 되지 않으면 consumer override가 예측 불가능해진다
- `!important`를 쓰게 되면 merge 순서를 먼저 점검한다

---

## 3. 조건부 클래스 패턴

### 객체 구문 (선호)

```tsx
className={cn(
  "base",
  {
    "active-class": isActive,
    "disabled-class": isDisabled,
    "error-class": hasError,
  },
)}
```

### Logical AND

```tsx
className={cn(
  "base",
  isActive && "active-class",
  isDisabled && "disabled-class",
)}
```

### Ternary

```tsx
className={cn(
  "base",
  isOpen ? "opacity-100" : "opacity-0",
)}
```

---

## 4. className Prop 타입

### 단일 element 컴포넌트

```tsx
import type { ClassName } from "~/lib/cn";

type Props = {
  className?: ClassName;
};

function Button({ className }: Props) {
  return <button className={cn("base", className)} />;
}
```

### 다중 element 컴포넌트

```tsx
import type { ClassNameRecord } from "~/lib/cn";

type Props = {
  className?: ClassNameRecord<"root" | "label" | "input" | "error">;
};

function TextField({ className }: Props) {
  return (
    <div className={cn("v-stack gap-1", className?.root)}>
      <label className={cn("text-sm font-medium", className?.label)}>{label}</label>
      <input className={cn("rounded-lg border px-3 py-2", className?.input)} />
      {error && <p className={cn("text-sm text-destructive", className?.error)}>{error}</p>}
    </div>
  );
}

// 사용
<TextField className={{ root: "w-full", label: "text-muted-foreground", input: "border-destructive" }} />
```

---

## 5. CVA (Class Variance Authority)

variant 조합이 4~5개를 넘어가면 `cva`로 선언형 관리한다.

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-border bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-9 px-4 text-sm",
        lg: "h-10 px-6 text-base",
        icon: "size-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

type ButtonProps = React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>;
```

- `defaultVariants`를 명시하면 호출부 판단 비용이 줄어든다
- `VariantProps<typeof buttonVariants>`로 variant prop 타입을 자동 추출한다
- variant가 구조까지 바꾸면 component split이 필요한지 먼저 본다 (visual variant만 `cva`로 관리)

---

## 6. 반복 패턴 추출

여러 컴포넌트에 반복되는 focus/disabled 규칙은 상수로 추출한다:

```tsx
export const focusRing = cn(
  "focus-visible:outline-none focus-visible:ring-2",
  "focus-visible:ring-ring focus-visible:ring-offset-2",
);

export const disabledStyles = "disabled:pointer-events-none disabled:opacity-50";
```

```tsx
className={cn(
  "inline-flex items-center",
  focusRing,
  disabledStyles,
  className,
)}
```

- 버튼, 입력, 토글 등 3곳 이상에서 반복되면 추출을 검토한다
- 너무 이른 추상화로 의미를 잃지 않도록 한다

---

## 빠른 체크리스트

- `className`이 항상 마지막에 병합되는가?
- `cn()` 없이 className을 그대로 넘기고 있지 않은가?
- variant 조합이 5개 이상인데 if 분기로 처리하고 있는가? → `cva` 검토
- variant가 시각 계약만 담당하는가? 구조가 달라지면 component split 우선
- focus/disabled 패턴이 3곳 이상 반복되는가? → 상수 추출
- 다중 element 컴포넌트에서 `ClassNameRecord`를 활용하고 있는가?
