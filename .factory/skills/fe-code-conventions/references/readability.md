# 가독성 (Readability)

> 코드가 읽기 쉬운 정도를 말해요. 코드가 변경하기 쉬우려면 먼저 코드가 어떤 동작을 하는지 이해할 수 있어야 해요.

읽기 좋은 코드는 읽는 사람이 한 번에 머릿속에서 고려하는 맥락이 적고, 위에서 아래로 자연스럽게 이어져요.

## 핵심 전략

가독성을 높이는 3가지 전략이에요:

1. **맥락 줄이기** — 동시에 고려해야 하는 정보의 양 줄이기
2. **이름 붙이기** — 복잡한 조건이나 매직 넘버에 의미 있는 이름 부여
3. **위에서 아래로 읽히게 하기** — 시점 이동과 복잡한 분기 최소화

---

## 예제 1: 매직 넘버에 이름 붙이기

**매직 넘버(Magic Number)** 란 정확한 뜻을 밝히지 않고 소스 코드 안에 직접 숫자 값을 넣는 것을 말해요.

### ❌ Before

```typescript
async function onLikeClick() {
  await postLike(url);
  await delay(300);
  await refetchPostLike();
}
```

`300`이 어떤 맥락으로 쓰였는지 알 수 없어요:
- 애니메이션 완료 대기?
- 좋아요 반영 시간?
- 테스트 코드 잔여물?

### ✅ After

```typescript
const ANIMATION_DELAY_MS = 300;

async function onLikeClick() {
  await postLike(url);
  await delay(ANIMATION_DELAY_MS);
  await refetchPostLike();
}
```

상수 `ANIMATION_DELAY_MS`로 선언하여 맥락을 명확하게 표시해요.

---

## 예제 2: 복잡한 조건에 이름 붙이기

복잡한 조건식이 이름 없이 사용되면, 조건이 뜻하는 바를 한눈에 파악하기 어려워요.

### ❌ Before

```typescript
const result = products.filter((product) =>
  product.categories.some(
    (category) =>
      category.id === targetCategory.id &&
      product.prices.some((price) => price >= minPrice && price <= maxPrice)
  )
);
```

`filter`, `some`, `&&` 같은 로직이 여러 단계로 중첩되어 정확한 조건을 파악하기 어려워요.

### ✅ After

```typescript
const matchedProducts = products.filter((product) => {
  return product.categories.some((category) => {
    const isSameCategory = category.id === targetCategory.id;
    const isPriceInRange = product.prices.some(
      (price) => price >= minPrice && price <= maxPrice
    );

    return isSameCategory && isPriceInRange;
  });
});
```

조건에 명시적인 이름을 붙여서, 한 번에 고려해야 할 맥락을 줄여요.

### 이름 붙이기 기준

**이름을 붙이는 것이 좋을 때:**
- 복잡한 로직을 다룰 때 (여러 줄에 걸친 조건문)
- 재사용성이 필요할 때 (동일 로직 반복 사용)
- 단위 테스트가 필요할 때

**이름을 붙이지 않아도 괜찮을 때:**
- 로직이 간단할 때 (예: `arr.map(x => x * 2)`)
- 한 번만 사용되며 복잡하지 않을 때

---

## 예제 3: 삼항 연산자 단순하게 하기

삼항 연산자를 복잡하게 사용하면 조건의 구조가 명확하게 보이지 않아서 코드를 읽기 어려울 수 있어요.

### ❌ Before

```typescript
const status =
  A조건 && B조건 ? "BOTH" : A조건 || B조건 ? (A조건 ? "A" : "B") : "NONE";
```

여러 삼항 연산자가 중첩되어, 어떤 조건으로 값이 계산되는지 한눈에 파악하기 어려워요.

### ✅ After

```typescript
const status = (() => {
  if (A조건 && B조건) return "BOTH";
  if (A조건) return "A";
  if (B조건) return "B";
  return "NONE";
})();
```

`if` 문으로 풀어서 명확하고 간단하게 조건을 드러내요.

---

## 예제 4: 비교문 순서 — 왼쪽에서 오른쪽으로 읽히게 하기

범위를 확인하는 조건문에서 부등호의 순서가 자연스럽지 않으면, 조건의 의도를 파악하는 데 시간이 더 걸려요.

### ❌ Before

```typescript
if (a >= b && a <= c) { ... }
if (score >= 80 && score <= 100) { ... }
```

중간값 `a`를 두 번 확인해야 하는 인지적 부담이 있어요.

### ✅ After

```typescript
if (b <= a && a <= c) { ... }
if (80 <= score && score <= 100) { ... }
if (minPrice <= price && price <= maxPrice) { ... }
```

`80 ≤ score ≤ 100`처럼 수학의 부등식과 같은 형태로 읽혀서, 범위 조건을 직관적으로 이해할 수 있어요.

---

## 예제 5: 구현 상세 추상화하기

한 사람이 코드를 읽을 때 동시에 고려할 수 있는 맥락의 숫자는 제한되어 있어요 (약 6~7개). 불필요한 맥락은 추상화해서 읽기 쉽게 만들어요.

### ❌ Before

```tsx
function LoginStartPage() {
  useCheckLogin({
    onChecked: (status) => {
      if (status === "LOGGED_IN") {
        location.href = "/home";
      }
    }
  });

  /* ... 로그인 관련 로직 ... */
  return <>{/* ... 로그인 관련 컴포넌트 ... */}</>;
}
```

로그인 확인 로직이 추상화 없이 노출되어 있어서, 한 번에 이해해야 하는 맥락이 많아요.

### ✅ After — Wrapper 컴포넌트 사용

```tsx
function App() {
  return (
    <AuthGuard>
      <LoginStartPage />
    </AuthGuard>
  );
}

function AuthGuard({ children }) {
  const status = useCheckLoginStatus();

  useEffect(() => {
    if (status === "LOGGED_IN") {
      location.href = "/home";
    }
  }, [status]);

  return status !== "LOGGED_IN" ? children : null;
}

function LoginStartPage() {
  /* ... 로그인 관련 로직 ... */
  return <>{/* ... 로그인 관련 컴포넌트 ... */}</>;
}
```

로그인 확인/이동 로직을 `AuthGuard`로 분리하여 각 컴포넌트의 맥락을 줄였어요.

---

## 예제 6: 같이 실행되지 않는 코드 분리하기

동시에 실행되지 않는 코드가 하나의 컴포넌트에 있으면, 동작을 한눈에 파악하기 어려워요.

### ❌ Before

```tsx
function SubmitButton() {
  const isViewer = useRole() === "viewer";

  useEffect(() => {
    if (isViewer) {
      return;
    }
    showButtonAnimation();
  }, [isViewer]);

  return isViewer ? (
    <TextButton disabled>Submit</TextButton>
  ) : (
    <Button type="submit">Submit</Button>
  );
}
```

2가지 권한 상태를 하나의 컴포넌트에서 처리하여, 동시에 실행되지 않는 코드가 교차되어 나타나요.

### ✅ After

```tsx
function SubmitButton() {
  const isViewer = useRole() === "viewer";
  return isViewer ? <ViewerSubmitButton /> : <AdminSubmitButton />;
}

function ViewerSubmitButton() {
  return <TextButton disabled>Submit</TextButton>;
}

function AdminSubmitButton() {
  useEffect(() => {
    showButtonAnimation();
  }, []);

  return <Button type="submit">Submit</Button>;
}
```

- 분기가 단 하나로 합쳐지고
- 각 컴포넌트에서 하나의 분기만 관리하여 맥락이 줄어들어요

---

## 예제 7: 시점 이동 줄이기

코드를 읽을 때 위아래를 오가거나, 여러 파일/함수/변수를 넘나들면서 읽는 것을 **시점 이동**이라고 해요. 시점 이동이 많을수록 코드 파악에 시간이 더 걸려요.

### ❌ Before

```tsx
function Page() {
  const user = useUser();
  const policy = getPolicyByRole(user.role);

  return (
    <div>
      <Button disabled={!policy.canInvite}>Invite</Button>
      <Button disabled={!policy.canView}>View</Button>
    </div>
  );
}

function getPolicyByRole(role) {
  const policy = POLICY_SET[role];
  return {
    canInvite: policy.includes("invite"),
    canView: policy.includes("view")
  };
}

const POLICY_SET = {
  admin: ["invite", "view"],
  viewer: ["view"]
};
```

`policy.canInvite` → `getPolicyByRole()` → `POLICY_SET` 순으로 3번의 시점 이동이 발생해요.

### ✅ After — 조건을 한눈에 볼 수 있는 객체로 만들기

```tsx
function Page() {
  const user = useUser();
  const policy = {
    admin: { canInvite: true, canView: true },
    viewer: { canInvite: false, canView: true }
  }[user.role];

  return (
    <div>
      <Button disabled={!policy.canInvite}>Invite</Button>
      <Button disabled={!policy.canView}>View</Button>
    </div>
  );
}
```

여러 차례의 시점 이동 없이, 컴포넌트만 보면 조건을 한눈에 파악할 수 있어요.

---

## 예제 8: 로직 종류에 따라 합쳐진 함수 쪼개기

쿼리 파라미터, 상태, API 호출과 같은 로직의 종류에 따라서 함수/Hook을 만들면, 한 번에 다루는 맥락이 많아져서 이해하기 힘들고 수정하기 어려운 코드가 돼요.

모놀리식 Hook(예: `usePageState`)을 각 쿼리 파라미터별로 별도의 Hook으로 쪼개면, 명확한 이름과 책임을 가지고 수정 시 영향 범위가 좁아져요.

이 예제는 결합도 관점에서도 중요해요. 자세한 내용은 coupling.md 예제 1을 참고하세요.

---

## 핵심 규칙 체크리스트

- [ ] 매직 넘버에 의미 있는 상수 이름을 부여했는가?
- [ ] 복잡한 조건식에 설명적인 변수 이름을 붙였는가?
- [ ] 중첩된 삼항 연산자를 `if` 문이나 IIFE로 풀었는가?
- [ ] 범위 비교를 왼쪽→오른쪽 순서로 작성했는가?
- [ ] 구현 상세를 적절히 추상화했는가? (6~7개 이하의 맥락)
- [ ] 동시에 실행되지 않는 코드를 별도 컴포넌트로 분리했는가?
- [ ] 시점 이동(코드 위아래 왔다갔다)을 최소화했는가?
- [ ] 하나의 Hook/함수가 하나의 논리적 책임만 담당하는가?
