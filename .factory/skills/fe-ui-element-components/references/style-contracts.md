# 스타일과 상태 계약

디자인 시스템 컴포넌트는 내부 구현을 모두 공개할 필요는 없지만, 소비자가 styling hook을 안정적으로 잡을 수 있어야 한다. `data-state`와 `data-slot`은 prop을 늘리지 않고 상태와 구조를 외부에 드러내는 계약이다.

---

## 1. `data-state`로 시각 상태를 노출한다

```tsx
function Dialog({ open, className, ...props }: DialogProps) {
  return (
    <div
      data-state={open ? "open" : "closed"}
      className={cn("transition-all", className)}
      {...props}
    />
  );
}
```

```tsx
<Dialog className="data-[state=open]:opacity-100 data-[state=closed]:opacity-0" />
```

- open/closed, active/inactive, checked/unchecked 같은 visual state에 적합하다
- `openClassName`, `closedClassName` 같은 prop 증가를 막아준다
- DevTools에서 상태를 바로 확인할 수 있다

---

## 2. `data-slot`으로 조합 구조를 식별한다

```tsx
function Card({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="card"
      className={cn(
        "rounded-lg border p-4",
        "[&_[data-slot=card-header]]:mb-4",
        "[&_[data-slot=card-footer]]:mt-4",
        className,
      )}
      {...props}
    />
  );
}
```

- parent가 child slot을 안정적으로 target할 수 있다
- class selector나 tag selector보다 구현 변경에 강하다
- kebab-case와 역할 기반 이름을 사용한다

---

## 3. `className` 하나로 override를 열어둔다

- 상태별 className prop을 여러 개 두기보다 `className`과 data attribute 기반 contract를 우선한다
- override는 component 내부에서 허용되는 공식 경로여야 한다
- consumer가 `!important`를 쓰게 만들면 계약이 약한 상태다

---

## 빠른 체크리스트

- 상태마다 별도 className prop이 늘어나고 있지 않은가?
- parent가 child role을 안정적으로 target해야 하는가?
- data attribute 이름이 styling이 아니라 역할과 상태를 설명하는가?
- `className` override와 data attribute contract가 함께 동작하는가?