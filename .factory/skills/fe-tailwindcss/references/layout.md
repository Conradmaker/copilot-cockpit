# 레이아웃 유틸리티

raw flex 클래스 대신 semantic한 커스텀 유틸리티를 정의해 사용하면 의미가 명확하고 코드베이스 전체에서 일관성이 높아진다.

---

## 1. Stack 유틸리티 정의

```css
@utility v-stack {
  display: flex;
  flex-direction: column;
}

@utility v-stack-reverse {
  display: flex;
  flex-direction: column-reverse;
}

@utility h-stack {
  display: flex;
  flex-direction: row;
}

@utility h-stack-reverse {
  display: flex;
  flex-direction: row-reverse;
}

@utility z-stack {
  display: grid;
  align-items: center;
  justify-items: center;

  & > * {
    grid-area: 1 / 1 / 1 / 2;
  }
}

@utility center {
  display: flex;
  justify-content: center;
  align-items: center;
}

@utility spacer {
  flex: 1 1 auto;
}

@utility circle {
  aspect-ratio: 1 / 1;
  border-radius: 9999px;
  flex-shrink: 0;
}
```

### 클래스 참조

| 클래스 | 동등한 CSS | 용도 |
|--------|-----------|------|
| `v-stack` | `flex flex-col` | 세로 스택 |
| `h-stack` | `flex flex-row` | 가로 스택 |
| `v-stack-reverse` | `flex flex-col-reverse` | 역순 세로 |
| `h-stack-reverse` | `flex flex-row-reverse` | 역순 가로 |
| `z-stack` | grid overlay | 겹치는 중앙 스택 |
| `center` | `flex items-center justify-center` | 양축 중앙 |
| `spacer` | `flex-1` | 유연한 빈 공간 |
| `circle` | `aspect-square rounded-full shrink-0` | 완벽한 원 |

---

## 2. Gap-first 원칙

자식 요소의 `margin` 대신 부모의 `gap-*`으로 간격을 제어한다.

```tsx
// ❌ 자식 margin — 마지막 아이템 예외 처리 필요
<div>
  {items.map((item, i) => (
    <Item key={item.id} className={i < items.length - 1 ? "mb-4" : ""} />
  ))}
</div>

// ✅ 부모 gap — 간격이 부모 책임
<div className="v-stack gap-4">
  {items.map((item) => (
    <Item key={item.id} />
  ))}
</div>
```

- 부모가 레이아웃을 제어하고, 자식은 재사용 가능하게 유지한다
- `margin`은 컴포넌트 캡슐화를 깨뜨릴 수 있다
- 방향 전환 시 gap은 자동으로 대응하지만 margin은 방향에 묶인다

### 컴포넌트 내부 margin 금지

```tsx
// ❌ 컴포넌트가 자기 간격을 정의
function Card() {
  return <div className="mb-4 rounded-lg border p-4" />;
}

// ✅ 부모가 간격을 결정
<div className="v-stack gap-4">
  <Card />
  <Card />
</div>
```

---

## 3. Responsive Stack 패턴

반응형 방향 전환은 stack utility에 responsive prefix를 붙여 처리한다.

### 사이드바 레이아웃

```tsx
<div className="v-stack lg:h-stack gap-6">
  <main className="grow v-stack gap-4">{/* 메인 콘텐츠 */}</main>
  <aside className="shrink-0 w-full lg:max-w-xs v-stack gap-4">{/* 사이드바 */}</aside>
</div>
```

### 헤더 네비게이션

```tsx
<header className="h-stack items-center justify-between">
  <Logo />
  <nav className="h-stack gap-4 max-md:hidden">
    <Link to="/about">About</Link>
    <Link to="/contact">Contact</Link>
  </nav>
  <button className="md:hidden"><MenuIcon /></button>
</header>
```

### 폼 레이아웃

```tsx
<div className="v-stack md:h-stack gap-4">
  <Input label="성" className="md:w-1/2" />
  <Input label="이름" className="md:w-1/2" />
</div>
```

### z-stack 오버레이

```tsx
<div className="z-stack">
  <img src="/avatar.jpg" alt="Avatar" className="circle size-12" />
  <span className="bg-green-500 circle size-3 translate-x-4 translate-y-4" />
</div>
```

---

## Anti-Patterns

| ❌ 금지 | ✅ 대안 |
|---------|---------|
| `flex flex-col` | `v-stack` |
| `flex flex-row` | `h-stack` |
| `flex items-center justify-center` | `center` |
| 자식에 `mb-4` 반복 | 부모에 `gap-4` |
| 컴포넌트 내부 margin | 부모가 간격 제어 |
