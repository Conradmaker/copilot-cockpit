# ESLint 접근성 규칙

`eslint-plugin-jsx-a11y`를 사용하여 코드 작성 단계에서 접근성 문제를 미리 발견하고 해결하는 방법을 다룬다.

---

## 설정 가이드

### 설치

```bash
yarn add -D eslint-plugin-jsx-a11y
```

### Flat Config (eslint.config.js)

```js
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  jsxA11y.flatConfigs.recommended,
  {
    rules: {
      "jsx-a11y/control-has-associated-label": "error",
    },
  },
];
```

### Legacy Config (.eslintrc)

```json
{
  "plugins": ["jsx-a11y"],
  "extends": ["plugin:jsx-a11y/recommended"],
  "rules": {
    "jsx-a11y/control-has-associated-label": "error"
  }
}
```

> `control-has-associated-label`은 recommended에 기본 비활성화되어 있어 직접 추가 필요

---

## 주요 규칙

### alt-text

`<img />` 에는 반드시 `alt` 속성이 있어야 한다. 정보를 전달하지 않는 이미지라도 빈 값(`alt=""`)이 필요하다.

```tsx
// ❌ 링크에 이미지만 있을 때 alt 없음
<a href="/home">
  <img src="home.svg" />
</a>

// ✅ 링크에 이미지만 있을 때 alt 제공
<a href="/home">
  <img src="home.svg" alt="홈" />
</a>
```

```tsx
// ❌ 장식 이미지에 불필요한 alt
<img src="divider.png" alt="구분선" />

// ✅ 장식 이미지에 빈 alt
<img src="divider.png" alt="" />
```

```tsx
// ❌ 텍스트와 함께 있는 아이콘에 중복 alt
<button>
  <img src="trash-icon.svg" alt="삭제 아이콘" />
  삭제
</button>

// ✅ 텍스트와 함께 있는 아이콘에 빈 alt
<button>
  <img src="trash-icon.svg" alt="" />
  삭제
</button>
```

### control-has-associated-label

인터랙티브 요소에 반드시 목적을 알려주는 이름이 필요하다.

```tsx
// ❌ 아이콘 버튼에 레이블 없음
<button>
  <img src="close.svg" alt="" />
</button>

// ✅ aria-label 또는 img alt로 레이블 제공
<button aria-label="닫기">
  <img src="close.svg" alt="" />
</button>
// 또는
<button>
  <img src="close.svg" alt="닫기" />
</button>
```

### no-noninteractive-element-interactions

비상호작용 요소(`<div>`, `<span>` 등)에 클릭 이벤트를 추가할 때는 `role` 속성으로 상호작용 요소임을 명시해야 한다.

```tsx
// ❌ role 없이 클릭 이벤트
<div onClick={handleClick}>클릭</div>

// ✅ role과 tabIndex 추가
<div role="button" tabIndex={0} onClick={handleClick}>클릭</div>
```

### no-noninteractive-element-to-interactive-role

의미 있는 컨테이너 요소(`<main>`, `<h1>`, `<ul>` 등)에 상호작용 역할을 부여하면 안 된다.

```tsx
// ❌ 의미 요소에 interactive role
<main role="button" onClick={handleClick}>저장</main>
<ul role="button" onClick={handleClick}>리스트</ul>

// ✅ 의미에 맞는 태그 사용
<button onClick={handleClick}>저장</button>
<a href="/list">리스트</a>
```

### no-noninteractive-tabindex

비상호작용 요소에 `tabIndex`를 부여하면 안 된다.

```tsx
// ❌ 비상호작용 요소에 tabIndex
<div tabIndex={0}>텍스트</div>

// ✅ 상호작용 의도가 있다면 role 추가
<div tabIndex={0} role="button">버튼</div>

// ✅ 상호작용 의도가 없다면 tabIndex 제거
<span>텍스트</span>
```

> **왜?** 비상호작용 요소에 `tabIndex`를 부여하면:
>
> 1. 스크린 리더 사용자가 상호작용 가능하다고 오해
> 2. 키보드 사용자가 예상치 못한 요소에 포커스
> 3. DOM의 자연스러운 포커스 순서가 깨짐

### tabindex-no-positive

`tabIndex`에 1 이상의 값을 쓰면 DOM 순서와 다르게 포커스가 이동하여 예측이 어려워진다.

```tsx
// ❌ 양수 tabIndex
<button tabIndex={2}>확인</button>

// ✅ 0 또는 -1만 사용
<button tabIndex={0}>확인</button>
```

---

## 디자인 시스템과 결합하기

`eslint-plugin-jsx-a11y`는 기본적으로 표준 HTML 태그에만 동작한다. 디자인 시스템 컴포넌트에도 적용하려면 추가 설정이 필요하다.

### 1. 컴포넌트 매핑

자체 컴포넌트가 어떤 HTML 요소를 렌더링하는지 매핑한다.

```js
// eslint.config.js (flat config)
import jsxA11y from "eslint-plugin-jsx-a11y";

export default [
  jsxA11y.flatConfigs.recommended,
  {
    rules: {
      "jsx-a11y/control-has-associated-label": "error",
    },
    settings: {
      "jsx-a11y": {
        components: {
          MyButton: "button",
          MyTxt: "span",
        },
      },
    },
  },
];
```

```json
// .eslintrc (legacy config)
{
  "settings": {
    "jsx-a11y": {
      "components": {
        "MyButton": "button",
        "MyTxt": "span"
      }
    }
  }
}
```

이렇게 하면 `<MyButton>`에도 `<button>`에 적용되는 접근성 규칙이 동일하게 적용된다.

### 2. Polymorphic prop 지원

`as` 같은 prop으로 다양한 태그를 렌더링하는 컴포넌트:

```tsx
<MyButton as="a" href="/home">
  홈으로
</MyButton>
```

`polymorphicPropName` 옵션으로 설정:

```js
settings: {
  "jsx-a11y": {
    polymorphicPropName: "as",
    components: {
      MyButton: "button",
    },
  },
}
```

### 3. control-has-associated-label 커스텀

children 대신 별도의 prop으로 텍스트를 받는 컴포넌트:

```tsx
<MyCard contents="카드 내용" />
```

`labelAttributes` 옵션으로 해당 prop을 레이블로 인식시킴:

```js
// Flat config
rules: {
  "jsx-a11y/control-has-associated-label": [2, {
    "labelAttributes": ["contents"]
  }]
},
settings: {
  "jsx-a11y": {
    components: {
      MyCard: "button",
    },
  },
}
```

```json
// Legacy config
{
  "rules": {
    "jsx-a11y/control-has-associated-label": [
      2,
      {
        "labelAttributes": ["contents"]
      }
    ]
  }
}
```

---

## 참고 자료

- [eslint-plugin-jsx-a11y 공식 문서](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
