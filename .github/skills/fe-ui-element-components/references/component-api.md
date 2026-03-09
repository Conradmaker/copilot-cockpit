# 재사용 가능한 컴포넌트 API 패턴

공유 컴포넌트의 API는 호출부에서 바로 읽혀야 한다. `value`와 `defaultValue`를 함께 지원할지, 어떤 HTML 속성을 그대로 통과시킬지, `as` 또는 `asChild`를 허용할지 같은 결정이 모호하면 컴포넌트는 빠르게 예외 투성이가 된다.

---

## 1. Controlled와 Uncontrolled를 구분해 설계한다

입력, 아코디언, 탭처럼 상위 상태가 개입할 수 있는 컴포넌트는 controlled/uncontrolled 양쪽 시나리오를 먼저 검토한다.

### ❌ Before: internal state만 지원

```tsx
function Stepper() {
  const [value, setValue] = useState(0);

  return (
    <div>
      <button onClick={() => setValue((current) => current - 1)}>-</button>
      <span>{value}</span>
      <button onClick={() => setValue((current) => current + 1)}>+</button>
    </div>
  );
}
```

상위 폼 상태, URL 상태, 서버 동기화 상태와 연결하려면 바로 한계가 생긴다.

### ✅ After: controlled/uncontrolled 둘 다 지원

```tsx
type StepperProps = {
  value?: number;
  defaultValue?: number;
  onValueChange?: (value: number) => void;
};

function Stepper({
  value: controlledValue,
  defaultValue = 0,
  onValueChange,
}: StepperProps) {
  const [uncontrolledValue, setUncontrolledValue] = useState(defaultValue);
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : uncontrolledValue;

  const setValue = (nextValue: number) => {
    if (!isControlled) {
      setUncontrolledValue(nextValue);
    }
    onValueChange?.(nextValue);
  };

  return (
    <div>
      <button type="button" onClick={() => setValue(value - 1)}>-</button>
      <span>{value}</span>
      <button type="button" onClick={() => setValue(value + 1)}>+</button>
    </div>
  );
}
```

- 상위 상태와 동기화해야 하는 시나리오가 있으면 `value`/`open` + `onChange` 계열을 연다.
- uncontrolled 기본값은 `defaultValue`, `defaultOpen`처럼 한 번만 적용되는 이름으로 둔다.
- stateless wrapper라면 controlled/uncontrolled API를 억지로 만들지 않는다.

---

## 2. Native props를 그대로 확장한다

wrapper 컴포넌트는 underlying element의 속성을 숨기지 않는 편이 낫다.

### ✅ 기본 패턴

```tsx
type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "secondary";
};

function Button({ variant = "primary", className, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant }), className)} {...props} />;
}
```

- `<button>` wrapper면 `type`, `disabled`, `aria-*`, `name`을 자연스럽게 그대로 받게 한다.
- `<a>` wrapper면 `href`, `target`, `rel`을 막지 않는다.
- native props를 숨기고 custom prop으로 재정의하면 HTML 의미론이 깨지기 쉽다.

### 피해야 할 패턴

```tsx
type ButtonProps = {
  isDisabled?: boolean;
  onPress?: () => void;
};
```

이런 API는 이미 브라우저가 제공하는 `disabled`, `onClick`, `type`과 어긋난다.

---

## 3. Prop type을 export한다

공유 컴포넌트는 소비자가 감싸서 다시 쓰게 된다. 따라서 prop type export는 선택이 아니라 계약의 일부에 가깝다.

```tsx
export type ButtonProps = React.ComponentProps<"button"> & {
  variant?: "primary" | "secondary";
};

export function Button(props: ButtonProps) {
  return <button {...props} />;
}
```

```tsx
import { Button, type ButtonProps } from "@/components/ui/button";

type SubmitButtonProps = ButtonProps & {
  isSaving?: boolean;
};

function SubmitButton({ isSaving, children, ...props }: SubmitButtonProps) {
  return <Button {...props}>{isSaving ? "저장 중…" : children}</Button>;
}
```

- 타입 이름은 `<ComponentName>Props`로 맞춘다.
- wrapper 컴포넌트, helper hook, story args에서 재사용할 수 있어야 한다.

---

## 4. `as`와 `asChild`는 필요한 곳에만 연다

모든 컴포넌트를 polymorphic하게 만들 필요는 없다. 같은 스타일과 동작을 유지한 채 semantic element를 바꿔야 하는 shared wrapper일 때만 연다.

### `as` 패턴

```tsx
type PolymorphicProps<T extends React.ElementType> = {
  as?: T;
} & React.ComponentPropsWithoutRef<T>;

function Box<T extends React.ElementType = "div">({
  as,
  ...props
}: PolymorphicProps<T>) {
  const Component = as || "div";
  return <Component {...props} />;
}
```

### `asChild` 패턴

```tsx
import { Slot } from "@radix-ui/react-slot";

type ButtonProps = React.ComponentProps<"button"> & {
  asChild?: boolean;
};

function Button({ asChild = false, className, ...props }: ButtonProps) {
  const Component = asChild ? Slot : "button";
  return <Component className={cn(buttonVariants(), className)} {...props} />;
}
```

```tsx
<Button asChild>
  <a href="/settings">설정으로 이동</a>
</Button>
```

- `as`는 단순하게 element type만 바꾸고 싶을 때 적합하다.
- `asChild`는 child와 props를 합성해야 하는 trigger, slot wrapper, primitive adapter에서 강하다.
- 한 화면에서만 쓰는 앱 전용 컴포넌트면 polymorphism보다 variant 분리가 더 단순한지 먼저 본다.

---

## 5. 한 컴포넌트는 가능하면 하나의 element boundary를 책임진다

```tsx
// ❌ header, body, footer 구조가 모두 한 컴포넌트에 묶임
function Card({ title, description, footer, ...props }) {
  return (
    <div {...props}>
      <h2>{title}</h2>
      <p>{description}</p>
      <div>{footer}</div>
    </div>
  );
}
```

이 구조는 곧 `titleClassName`, `footerClassName`, `descriptionAs` 같은 prop 증가로 이어진다.

```tsx
// ✅ 구조를 쪼개서 호출부가 직접 조합
<Card.Root>
  <Card.Header>
    <Card.Title>제목</Card.Title>
    <Card.Description>설명</Card.Description>
  </Card.Header>
  <Card.Footer>액션</Card.Footer>
</Card.Root>
```

- 구조 커스터마이징 요구가 늘어나면 compound component로 다시 나눈다.
- 단일 컴포넌트 prop API로 억지로 버티면 곧 boolean prop과 render prop이 과해진다.

---

## 빠른 체크리스트

- 상위 제어가 필요한 상태면 controlled/uncontrolled를 함께 설계하는가?
- native element의 HTML 속성을 그대로 확장하는가?
- 공개 prop type을 export하는가?
- `as` 또는 `asChild`는 정말 semantic flexibility가 필요한 곳에만 쓰는가?
- 하나의 컴포넌트가 과도한 구조 prop을 받기 시작하면 composition으로 다시 나누는가?