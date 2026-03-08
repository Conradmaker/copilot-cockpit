# 예측 가능성 (Predictability)

> 함께 협업하는 동료들이 함수나 컴포넌트의 동작을 얼마나 예측할 수 있는지를 말한다.

예측 가능성이 높은 코드는 일관적인 규칙을 따르고, 함수나 컴포넌트의 이름과 파라미터, 반환 값만 보고도 어떤 동작을 하는지 알 수 있다.

## 핵심 전략

1. **이름 겹치지 않게 관리하기** — 같은 이름은 같은 동작을 보장
2. **같은 종류의 함수는 반환 타입 통일하기** — 일관적인 인터페이스 유지
3. **숨은 로직 드러내기** — 이름/파라미터/반환값으로 예측 가능한 것만 구현에 포함

---

## 예제 1: 이름 겹치지 않게 관리하기

같은 이름을 가지는 함수나 변수는 동일한 동작을 해야 한다. 작은 동작 차이는 코드의 예측 가능성을 낮추고, 읽는 사람에게 혼란을 줄 수 있다.

### ❌ Before

```typescript
// http.ts
import {http as httpLibrary} from "@some-library/http";

export const http = {
  async get(url: string) {
    const token = await fetchToken();

    return httpLibrary.get(url, {
      headers: {Authorization: `Bearer ${token}`},
    });
  },
};
```

```typescript
// fetchUser.ts
import {http} from "./http";

export async function fetchUser() {
  return http.get("...");
}
```

`http.get`을 호출하는 개발자는 단순한 GET 요청을 예상하지만, 실제로는 토큰을 가져오는 추가 작업이 수행된다. 오해로 기대 동작과 실제 동작의 차이가 생기고, 버그가 발생하거나 디버깅이 어려워질 수 있다.

### ✅ After

```typescript
// httpService.ts
import {http as httpLibrary} from "@some-library/http";

export const httpService = {
  async getWithAuth(url: string) {
    const token = await fetchToken();

    return httpLibrary.get(url, {
      headers: {Authorization: `Bearer ${token}`},
    });
  },
};
```

```typescript
// fetchUser.ts
import {httpService} from "./httpService";

export async function fetchUser() {
  return await httpService.getWithAuth("...");
}
```

- 라이브러리 함수명과 구분되는 명확한 이름 (`httpService`, `getWithAuth`)
- 함수명을 통해 인증된 요청을 보낸다는 것을 바로 알 수 있다

---

## 예제 2: 같은 종류의 함수는 반환 타입 통일하기

같은 종류의 함수나 Hook이 서로 다른 반환 타입을 가지면 코드의 일관성이 떨어져서, 동료들이 코드를 읽는 데 헷갈릴 수 있다.

### 사례 A: API Hook의 반환 타입

#### ❌ Before

```typescript
function useUser() {
  const query = useQuery({
    queryKey: ["user"],
    queryFn: fetchUser,
  });
  return query; // Query 객체 반환
}

function useServerTime() {
  const query = useQuery({
    queryKey: ["serverTime"],
    queryFn: fetchServerTime,
  });
  return query.data; // 데이터만 반환
}
```

서버 API를 호출하는 Hook의 반환 타입이 서로 다르면, 동료들은 매번 반환 타입이 무엇인지 확인해야 한다.

#### ✅ After

```typescript
function useUser() {
  const query = useQuery({
    queryKey: ["user"],
    queryFn: fetchUser,
  });
  return query;
}

function useServerTime() {
  const query = useQuery({
    queryKey: ["serverTime"],
    queryFn: fetchServerTime,
  });
  return query; // 일관적으로 Query 객체 반환
}
```

### 사례 B: 유효성 검사 함수의 반환 타입

#### ❌ Before

```typescript
function checkIsNameValid(name: string) {
  const isValid = name.length > 0 && name.length < 20;
  return isValid; // boolean 반환
}

function checkIsAgeValid(age: number) {
  if (!Number.isInteger(age)) {
    return {ok: false, reason: "나이는 정수여야 해요."}; // 객체 반환
  }
  // ...
  return {ok: true};
}
```

반환 타입이 다르면, 특히 엄격한 불리언 검증을 사용하지 않는 경우 오류의 원인이 될 수 있다:

```typescript
// boolean → 올바르게 동작
if (checkIsNameValid(name)) { ... }

// 항상 객체를 반환하므로 if 문 안 코드가 항상 실행됨!
if (checkIsAgeValid(age)) { ... }
```

#### ✅ After

```typescript
type ValidationCheckReturnType = {ok: true} | {ok: false; reason: string};

function checkIsNameValid(name: string): ValidationCheckReturnType {
  if (name.length === 0) {
    return {ok: false, reason: "이름은 빈 값일 수 없어요."};
  }
  if (name.length >= 20) {
    return {ok: false, reason: "이름은 20자 이상 입력할 수 없어요."};
  }
  return {ok: true};
}

function checkIsAgeValid(age: number): ValidationCheckReturnType {
  if (!Number.isInteger(age)) {
    return {ok: false, reason: "나이는 정수여야 해요."};
  }
  if (age < 18) {
    return {ok: false, reason: "나이는 18세 이상이어야 해요."};
  }
  if (age > 99) {
    return {ok: false, reason: "나이는 99세 이하이어야 해요."};
  }
  return {ok: true};
}
```

**Discriminated Union**으로 정의하면, `ok` 값에 따라 `reason`의 존재 유무를 컴파일러가 검증할 수 있다.

---

## 예제 3: 숨은 로직 드러내기

함수나 컴포넌트의 이름, 파라미터, 반환 값에 드러나지 않는 숨은 로직이 있다면, 동료들이 동작을 예측하는 데 어려움을 겪을 수 있다.

### ❌ Before

```typescript
async function fetchBalance(): Promise<number> {
  const balance = await http.get<number>("...");

  logging.log("balance_fetched"); // 숨겨진 로깅 로직

  return balance;
}
```

`fetchBalance` 함수의 이름과 반환 타입만으로는 로깅이 이루어지는지 알 수 없다:

- 로깅을 원하지 않는 곳에서도 로깅이 발생할 수 있음
- 로깅 로직 오류 시 잔액 조회 로직까지 망가질 수 있음

### ✅ After

```typescript
// 함수는 이름/파라미터/반환 타입으로 예측 가능한 로직만 포함
async function fetchBalance(): Promise<number> {
  const balance = await http.get<number>("...");
  return balance;
}
```

```tsx
// 로깅은 호출하는 곳에서 명시적으로 수행
<Button
  onClick={async () => {
    const balance = await fetchBalance();
    logging.log("balance_fetched");
    await syncBalance(balance);
  }}
>
  계좌 잔액 갱신하기
</Button>
```

함수의 이름과 파라미터, 반환 타입으로 예측할 수 있는 로직만 구현 부분에 남긴다.

---

## 핵심 규칙 체크리스트

- [ ] 기존 라이브러리/모듈의 함수명과 겹치는 이름을 사용하고 있지 않은가?
- [ ] 같은 종류의 함수/Hook이 일관된 반환 타입을 가지고 있는가?
- [ ] Discriminated Union 등을 활용하여 타입 안전성을 확보했는가?
- [ ] 함수 내부에 이름/파라미터/반환값으로 예측할 수 없는 부수효과(side effect)가 없는가?
- [ ] 로깅, 분석 등의 부수효과를 호출하는 곳에서 명시적으로 처리하고 있는가?
