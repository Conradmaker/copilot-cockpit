# 응집도 (Cohesion)

> 수정되어야 할 코드가 항상 같이 수정되는지를 말한다. 함께 수정되어야 할 부분이 반드시 함께 수정되도록 구조적으로 뒷받침하는 것이 중요하다.

응집도가 높은 코드는 코드의 한 부분을 수정해도 의도치 않게 다른 부분에서 오류가 발생하지 않는다.

## ⚠️ 가독성과 응집도의 트레이드오프

일반적으로 응집도를 높이기 위해서는 변수나 함수를 추상화하는 등 가독성을 떨어뜨리는 결정을 해야 한다.

- 함께 수정하지 않으면 오류가 발생할 수 있는 경우 → **응집도를 우선**하여 공통화, 추상화
- 위험성이 높지 않은 경우 → **가독성을 우선**하여 코드 중복 허용

---

## 예제 1: 함께 수정되는 파일을 같은 디렉토리에 두기 (코로케이션)

프로젝트에서 Hook, 컴포넌트, 유틸리티 함수 등을 여러 파일로 나누어 관리할 때, 함께 수정되는 소스 파일을 하나의 디렉토리에 배치하면 코드의 의존 관계를 명확하게 드러낼 수 있다.

### ❌ Before — 종류별 분류

```text
└─ src
   ├─ components
   ├─ constants
   ├─ containers
   ├─ contexts
   ├─ remotes
   ├─ hooks
   ├─ utils
   └─ ...
```

**문제점:**

- 어떤 코드가 어떤 코드를 참조하는지 쉽게 확인할 수 없다
- 특정 기능 삭제 시 연관된 코드가 함께 삭제되지 못해 사용되지 않는 코드가 남을 수 있다
- 프로젝트 규모가 커지면 디렉토리 하나에 100개가 넘는 파일이 쌓일 수 있다

### ✅ After — 도메인별 코로케이션

```text
└─ src
   │  // 전체 프로젝트에서 사용되는 코드
   ├─ components
   ├─ containers
   ├─ hooks
   ├─ utils
   ├─ ...
   │
   └─ domains
      │  // Domain1에서만 사용되는 코드
      ├─ Domain1
      │     ├─ components
      │     ├─ containers
      │     ├─ hooks
      │     ├─ utils
      │     └─ ...
      │
      │  // Domain2에서만 사용되는 코드
      └─ Domain2
            ├─ components
            ├─ containers
            ├─ hooks
            ├─ utils
            └─ ...
```

**이점:**

- 코드 사이의 의존 관계를 파악하기 쉬움
- 잘못된 참조를 쉽게 인지 가능 (예: `import { useFoo } from "../../../Domain2/hooks/useFoo"` → 잘못된 참조)
- 특정 기능 삭제 시 한 디렉토리 전체를 삭제하면 깔끔하게 정리됨

---

## 예제 2: 매직 넘버와 응집도

매직 넘버가 코드에 직접 사용되면, 관련 코드를 수정할 때 조용히 서비스가 깨질 수 있는 위험성이 있다.

### ❌ Before

```typescript
async function onLikeClick() {
  await postLike(url)
  await delay(300)
  await refetchPostLike()
}
```

`300`이 애니메이션 완료 대기 시간이라면, 애니메이션을 변경했을 때 이 값도 함께 수정되어야 한다. 하지만 매직 넘버로 사용되면 수정이 누락될 수 있다. **같이 수정되어야 할 코드 중 한쪽만 수정되는 것**이다.

### ✅ After

```typescript
const ANIMATION_DELAY_MS = 300

async function onLikeClick() {
  await postLike(url)
  await delay(ANIMATION_DELAY_MS)
  await refetchPostLike()
}
```

상수로 선언하면, 애니메이션 관련 코드를 수정할 때 이 상수도 함께 확인하게 된다.

---

## 예제 3: 폼의 응집도 전략

폼을 관리할 때는 **필드 단위 응집도**와 **폼 전체 단위 응집도** 중 상황에 맞는 방식을 선택해야 한다.

### 전략 A: 필드 단위 응집도

각 필드가 독립적으로 검증 로직을 가지는 방식이다.

```tsx
import { useForm } from "react-hook-form"

export function Form() {
  const {
    register,
    formState: { errors },
    handleSubmit,
  } = useForm({
    defaultValues: { name: "", email: "" },
  })

  const onSubmit = handleSubmit((formData) => {
    console.log("Form submitted:", formData)
  })

  return (
    <form onSubmit={onSubmit}>
      <div>
        <input
          {...register("name", {
            validate: (value) => (isEmptyStringOrNil(value) ? "이름을 입력해주세요." : ""),
          })}
          placeholder="이름"
        />
        {errors.name && <p>{errors.name.message}</p>}
      </div>

      <div>
        <input
          {...register("email", {
            validate: (value) => {
              if (isEmptyStringOrNil(value)) return "이메일을 입력해주세요."
              if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value))
                return "유효한 이메일 주소를 입력해주세요."
              return ""
            },
          })}
          placeholder="이메일"
        />
        {errors.email && <p>{errors.email.message}</p>}
      </div>

      <button type="submit">제출</button>
    </form>
  )
}
```

### 전략 B: 폼 전체 단위 응집도

모든 필드의 검증 로직이 폼에 종속되는 방식이다.

```tsx
import * as z from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

const schema = z.object({
  name: z.string().min(1, "이름을 입력해주세요."),
  email: z.string().min(1, "이메일을 입력해주세요.").email("유효한 이메일 주소를 입력해주세요."),
})

export function Form() {
  const {
    register,
    formState: { errors },
    handleSubmit,
  } = useForm({
    defaultValues: { name: "", email: "" },
    resolver: zodResolver(schema),
  })

  const onSubmit = handleSubmit((formData) => {
    console.log("Form submitted:", formData)
  })

  return (
    <form onSubmit={onSubmit}>
      <div>
        <input {...register("name")} placeholder="이름" />
        {errors.name && <p>{errors.name.message}</p>}
      </div>
      <div>
        <input {...register("email")} placeholder="이메일" />
        {errors.email && <p>{errors.email.message}</p>}
      </div>
      <button type="submit">제출</button>
    </form>
  )
}
```

### 어떤 전략을 선택할까?

**필드 단위 응집도가 좋을 때:**

- 독립적인 검증이 필요할 때 (비동기 검증, 고유 검증 로직)
- 필드와 검증 로직을 다른 폼에서도 재사용해야 할 때

**폼 전체 단위 응집도가 좋을 때:**

- 모든 필드가 하나의 완결된 기능을 구성할 때 (결제, 배송 정보)
- 단계별 입력이 필요할 때 (Wizard Form)
- 필드 간 의존성이 있을 때 (비밀번호 확인, 총액 계산)

---

## 핵심 규칙 체크리스트

- [ ] 함께 수정되는 파일이 같은 디렉토리에 위치하는가?
- [ ] 도메인별로 코드가 분리되어 있는가?
- [ ] 매직 넘버를 의미 있는 상수로 추출하여 관련 코드와 함께 관리하고 있는가?
- [ ] 폼 설계 시 필드 단위 vs 폼 전체 단위 응집도를 의식적으로 선택했는가?
- [ ] 다른 도메인의 코드를 불필요하게 참조하고 있지 않은가?
