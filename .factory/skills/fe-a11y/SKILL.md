---
name: fe-a11y
description: "Frontend web accessibility patterns and best practices. Use this skill when building UI components that need to be accessible, implementing ARIA attributes, creating forms/modals/tabs/accordions, reviewing accessibility compliance, setting up a11y ESLint rules, or when the user asks about screen reader support, keyboard navigation, semantic HTML, or ARIA. IMPORTANT: Always consult this skill when creating any interactive UI component (buttons, forms, modals, tabs, accordions, switches, checkboxes, radios, dropdowns, dialogs, popups, toggles), even if the user doesn't explicitly mention accessibility. Triggers on: accessibility, a11y, ARIA, screen reader, keyboard navigation, semantic HTML, role, aria-label, aria-expanded, form accessibility, modal dialog, tab component, 접근성, 스크린리더, 키보드 네비게이션, 시맨틱, 모달 만들기, 탭 만들기, 폼 만들기, 아코디언, 토글, 스위치, 체크박스, 라디오, 다이얼로그, 팝업, 버튼, input, select, 드롭다운, 사용성, UX, 웹표준, UI 컴포넌트."
---

# 프론트엔드 웹 접근성 (fe-a11y)

## 접근성의 핵심 가치

접근성(Accessibility, A11y)을 지키면 **장애인, 비장애인, 개발자 모두**에게 이득이에요.

| 대상 | 효과 |
|------|------|
| **장애인 사용자** | 스크린 리더, 키보드 등 보조기기로 웹을 원활하게 이용할 수 있어요 |
| **비장애인 사용자** | Enter로 폼 제출, 우클릭 컨텍스트 메뉴, 키보드 탐색 등 익숙한 웹 동작을 자연스럽게 사용할 수 있어요 |
| **개발자** | `testing-library`의 `ByRole` 쿼리로 요소를 쉽게 특정할 수 있고, 견고하고 유지보수하기 쉬운 코드를 작성할 수 있어요 |

```js
// 접근성을 잘 지킨 코드 → 테스트가 쉬워요
expect(screen.getByRole("button", { name: "저장" })).toBeInTheDocument();
```

## 스크린 리더의 3요소

스크린 리더는 화면의 요소를 다음 순서로 읽어요:

### 1. 역할(Role)
요소가 어떤 종류인지 나타내요. (예: 버튼, 입력창, 스위치)

| HTML 요소 | 기본 role |
|-----------|-----------|
| `<button>` | `button` |
| `<a>` | `link` |
| `<input>` | `textbox` |
| `<input type="checkbox">` | `checkbox` |
| `<dialog>` | `dialog` |

### 2. 레이블(Label)
컴포넌트의 이름이에요. 어떤 기능인지 설명해요.

```tsx
// 우선순위: aria-labelledby > aria-label > <label> > placeholder > 내부 텍스트
<button aria-label="검색"><SearchIcon /></button>
```

### 3. 상태(State)
현재 상태를 알려줘요. (예: 선택됨, 꺼짐, 펼쳐짐)

```tsx
<button role="tab" aria-selected={true}>홈</button>
// 스크린 리더: "홈, 탭, 선택됨"
```

## 4대 핵심 원칙

### 1. 🧱 올바른 구조 만들기
인터랙티브 요소(버튼, 링크 등) 안에 또 다른 인터랙티브 요소를 중첩하면 안 돼요.

```tsx
// ❌ button 안에 button
<button>카드 <button>삭제</button></button>

// ✅ 레이어링으로 분리
<div style={{ position: "relative" }}>
  <button style={{ position: "absolute", inset: 0 }}>상세보기</button>
  카드
  <div style={{ position: "relative", zIndex: 2 }}>
    <button>삭제</button>
  </div>
</div>
```

### 2. 🗣️ 의미를 정확하게 전달하기
모든 인터랙티브 요소에는 반드시 접근 가능한 이름을 부여해야 해요.

```tsx
// ❌ 이름 없는 버튼
<button><CloseIcon /></button>

// ✅ aria-label로 이름 부여
<button aria-label="닫기"><CloseIcon /></button>
```

### 3. 🎯 예측 가능한 인터랙션 만들기
- 버튼은 반드시 `<button>` 요소를 사용해요 (div + onClick ❌)
- 입력 요소는 `<form>`으로 감싸서 Enter 제출, autocomplete 등을 지원해요

```tsx
// ❌ 가짜 버튼
<div style={{ cursor: "pointer" }} onClick={handleClick}>클릭</div>

// ✅ 진짜 버튼
<button onClick={handleClick}>클릭</button>
```

### 4. 🌈 시각 정보에만 의존하지 않기
이미지, 아이콘, 차트 등 시각 요소에는 반드시 대체 텍스트를 제공해요.

```tsx
// ❌ 의미 있는 이미지에 alt 누락
<button><img src="search.svg" alt="" /></button>

// ✅ 적절한 대체 텍스트
<button><img src="search.svg" alt="검색" /></button>
```

## 언제 이 스킬을 참고해야 하나요?

인터랙티브한 UI 컴포넌트를 만들 때는 **항상** 이 스킬을 참고하세요. "접근성을 개선해줘"라는 명시적 요청이 없더라도, 모달/탭/폼/아코디언/스위치/체크박스/라디오/다이얼로그를 구현할 때 이 스킬의 `references/ui-components.md`를 확인하면 올바른 ARIA 패턴으로 바로 만들 수 있어요.

## 📚 references/ 가이드

| 파일 | 내용 | 이럴 때 참조하세요 |
|------|------|---------------------|
| [basics.md](./references/basics.md) | 역할(Role), 레이블(Label), 상태(State) 상세 가이드 | ARIA 속성 사용법을 알고 싶을 때 |
| [semantic-structure.md](./references/semantic-structure.md) | 시맨틱 HTML, 인터랙티브 요소 중첩 금지, 테이블 행 링크 | HTML 구조 설계 시 |
| [ui-components.md](./references/ui-components.md) | 모달, 스위치, 탭, 체크박스, 라디오, 아코디언 접근성 패턴 | UI 컴포넌트 구현 시 |
| [forms.md](./references/forms.md) | 폼, 가짜 버튼, react-aria 활용 | 폼과 인터랙션 구현 시 |
| [eslint.md](./references/eslint.md) | eslint-plugin-jsx-a11y 설정, 주요 규칙, 디자인 시스템 매핑 | 접근성 린트 설정 시 |
| [alt-text.md](./references/alt-text.md) | 이미지 대체 텍스트 작성법, 유형별 가이드 | 이미지/아이콘 대체 텍스트 작성 시 |

## 🔗 범위

- **일반 코드 품질** (네이밍, 함수 설계, 에러 처리 등) → `fe-code-conventions` 스킬 참조
- **React 고유 패턴** (hooks, 상태 관리, 컴포넌트 설계 등) → `fe-react-patterns` 스킬 참조
- **디자인/디자인 시스템** → 별도 디자인 관련 스킬 참조

## 이 스킬을 사용하지 않는 경우

- 순수 데이터 처리, 백엔드 로직, API 호출에는 이 스킬이 적용되지 않아요
- React 컴포넌트 아키텍처/합성 패턴 → `fe-react-patterns`를 참고하세요
- 일반 코드 컨벤션 → `fe-code-conventions`를 참고하세요
- 성능 최적화 → `fe-react-performance`를 참고하세요
