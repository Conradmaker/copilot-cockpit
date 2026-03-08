# Affordance 클래스

element에 독립적인 시각적 패턴(affordance)을 `@utility`로 정의한다. `button`, `label`, `a`, `summary` 등 어떤 element에도 동일한 외형을 적용할 수 있다.

---

## 1. 왜 Affordance 클래스인가

- element 선택과 외형을 분리한다 (`<label>`에 버튼 스타일, `<a>`에 입력 스타일)
- 인터랙티브 스타일의 단일 진실 공급원을 유지한다
- Tailwind tree-shaking과 IntelliSense를 보존한다
- `:where()`로 specificity를 0으로 유지하여 utility override가 자연스럽다

---

## 2. 패턴

`@utility`로 정의하고, `:where()`로 감싸고, `@variant`로 상태별 스타일을 선언한다:

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

@utility ui-input {
  :where(&) {
    @apply block w-full rounded-md border border-neutral-300 bg-white px-3 py-2;
    @apply text-neutral-900;

    @variant focus-visible {
      @apply border-primary outline-2 outline-offset-2 outline-primary;
    }
  }
}
```

---

## 3. 사용 예시

```tsx
// label을 버튼처럼 스타일링
<label className="ui-button" htmlFor="document-upload">
  Choose file
</label>

// utility로 override (specificity 0이므로 자연스럽게 덮어쓴다)
<button className="ui-button bg-red-600 hover:bg-red-500">Delete</button>

// 같은 affordance를 다른 element에
<input className="ui-input" />
<textarea className="ui-input" />
```

---

## 4. 규칙

1. `ui-` (또는 프로젝트 prefix)로 시작하여 affordance임을 명시한다
2. `@utility`로 정의하여 tree-shaking과 IntelliSense를 보존한다
3. `:where()`로 감싸 specificity를 0으로 유지한다
4. `@variant` 블록으로 상태별 스타일을 가독성 있게 선언한다
5. 구조가 달라지면 affordance가 아닌 별도 컴포넌트로 분리한다
