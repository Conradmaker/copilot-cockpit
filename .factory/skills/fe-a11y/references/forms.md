# 폼 & 인터랙션 접근성

입력 폼과 버튼 등 인터랙티브 요소의 접근성 패턴을 다룬다.

---

## `<form>` 태그 사용하기

입력 요소는 반드시 `<form>`으로 감싸야 한다. `<form>`을 사용하면 별도의 스크립트 없이 다음 기능이 제공된다:

- **Enter 키로 폼 제출** — 사용자가 기대하는 기본 동작
- **브라우저 자동완성** (autocomplete) — 입력 기록 저장
- **모바일 입력 최적화** — 키보드 레이아웃 등
- **스크린 리더 탐색** — 폼 영역 단축키로 빠른 탐색 가능

### 스크린 리더에서의 효과

```html
<form aria-label="로그인">
  <label for="id">아이디</label>
  <input id="id" name="id" type="text" />
  <label for="pw">비밀번호</label>
  <input id="pw" name="pw" type="password" />
  <button type="submit">로그인</button>
</form>
```

**스크린 리더:** "로그인, 폼 / 아이디, 편집 / 비밀번호, 편집 / 로그인, 버튼 / 폼 종료"

스크린 리더 사용자에게 폼이 제공하는 것:

- **역할(Role) 안내:** "폼의 시작", "폼의 끝" 안내
- **빠른 탐색:** 단축키(NVDA/JAWS의 `f` 키)로 폼 영역만 빠르게 탐색
- **맥락 제공:** 여러 입력 요소가 하나의 폼에 속해 있다는 맥락 전달
- **에러/상태 안내:** 폼 제출 시 에러 메시지 등 흐름 유지

### 올바른 form 사용법

```html
<form onsubmit="event.preventDefault(); /* 원하는 동작 */">
  <input type="text" name="username" />
  <input type="password" name="password" />
  <button type="submit">로그인</button>
  <button type="button">취소</button>
  <!-- 단순 동작용 -->
</form>
```

**핵심 규칙:**

- 입력 요소는 `<form>` 안에 배치
- 페이지 새로고침 없이 동작하려면 `onsubmit`에서 `event.preventDefault()` 호출
- 제출 버튼: `<button type="submit">` (기본 타입이 submit)
- 단순 클릭 버튼: `<button type="button">` (반드시 명시!)

> ⚠️ `<form>` 안의 `<button>`은 기본적으로 submit 동작을 한다. 단순 클릭 이벤트만 필요한 버튼은 `type="button"`을 꼭 명시한다.

### 버튼이 form 바깥에 있을 때

```html
<form id="my-form" onsubmit="event.preventDefault();">
  <input type="text" name="search" />
</form>
<button type="submit" form="my-form">검색</button>
```

### 실전 예시: 로그인 폼

```html
<form onsubmit="event.preventDefault();">
  <label for="login-id">아이디</label>
  <div>
    <input id="login-id" name="id" type="text" />
    <button type="button" tabindex="-1" aria-label="아이디 입력값 삭제">❌</button>
  </div>
  <label for="login-pw">비밀번호</label>
  <div>
    <input id="login-pw" name="pw" type="password" />
    <button type="button" tabindex="-1" aria-label="비밀번호 입력값 삭제">❌</button>
  </div>
  <button type="submit">로그인</button>
</form>
```

> 삭제 버튼에 `tabindex="-1"`을 지정하여 키보드 포커스를 받지 않게 했다. 텍스트는 `Backspace` 키로 지울 수 있기 때문에 키보드 사용자에게 불필요한 포커스 이동을 방지한다.

---

## 가짜 버튼 금지

`<div>`나 `<span>`에 `cursor: pointer`와 `onClick`만 추가한 것은 진짜 버튼이 아니다.

### 문제점

```tsx
// ❌ 가짜 버튼
<div className="button-style" style={{cursor: "pointer"}} onClick={handleClick}>
  문의하기
</div>
```

- 키보드로 이동 불가 (Tab 키로 포커스 안 됨)
- Enter/Space 키로 클릭 불가
- 스크린 리더가 "버튼"으로 인식하지 못함

### ✅ 방법 1: `<button>` 요소 사용 (권장)

```tsx
<button onClick={handleClick}>문의하기</button>
```

`<button>`이 제공하는 기본 접근성:

- 키보드 포커스
- Enter/Space 키로 클릭
- 스크린 리더에서 "버튼"으로 인식
- 적절한 ARIA 속성 자동 제공

### ✅ 방법 2: `<button>` 사용 불가 시 (block 요소 내부 등)

```tsx
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      handleClick();
    }
  }}
>
  <div>내부 block 요소</div>
</div>
```

- `role="button"`: 스크린 리더에게 버튼임을 알림
- `tabIndex={0}`: 키보드 포커스 가능
- `onKeyDown`: Enter/Space 키 입력 시 클릭 이벤트 발생

### ✅ 방법 3: react-aria `useButton` 훅 사용

[React-Aria](https://react-spectrum.adobe.com/react-aria/index.html)의 `useButton` 훅을 사용하면 접근성 속성을 직접 처리하지 않아도 된다.

```tsx
import {useButton} from "react-aria";

const buttonRef = useRef<HTMLDivElement>(null);
const {buttonProps} = useButton(
  {
    elementType: "div",
    onPress: handleClick,
  },
  buttonRef
);

<div ref={buttonRef} {...buttonProps}>
  <div>내부 block 요소</div>
</div>;
```

> `useButton`이 `role`, `tabIndex`, `onKeyDown` 등 필수 접근성 설정을 모두 제공한다.

### 링크에도 동일하게 적용

링크가 가능한 요소는 반드시 `<a>` 태그를 사용한다.

- `<a>` 태그는 block 요소를 자식으로 포함할 수 있다
- `<button>`과 달리 페이지 이동에 사용
- 우클릭 컨텍스트 메뉴(새 창 열기, 링크 복사 등) 제공
