---
name: fe-a11y
description: "Frontend web accessibility patterns and best practices. Use this skill when building UI components that need to be accessible, implementing ARIA attributes, creating forms/modals/tabs/accordions, reviewing accessibility compliance, setting up a11y ESLint rules, or when the user asks about screen reader support, keyboard navigation, semantic HTML, or ARIA. IMPORTANT: Always consult this skill when creating any interactive UI component (buttons, forms, modals, tabs, accordions, switches, checkboxes, radios, dropdowns, dialogs, popups, toggles), including shared UI wrappers and reusable design-system primitives, even if the user doesn't explicitly mention accessibility. Triggers on: accessibility, a11y, ARIA, screen reader, keyboard navigation, semantic HTML, role, aria-label, aria-expanded, form accessibility, modal dialog, tab component, shared UI component, reusable component, 접근성, 스크린리더, 키보드 네비게이션, 시맨틱, 모달 만들기, 탭 만들기, 폼 만들기, 아코디언, 토글, 스위치, 체크박스, 라디오, 다이얼로그, 팝업, 버튼, input, select, 드롭다운, 사용성, UX, 웹표준, UI 컴포넌트, 재사용 컴포넌트."
---

# 프론트엔드 웹 접근성 (fe-a11y)

## 목표

인터랙티브 UI 컴포넌트(모달, 탭, 폼, 아코디언, 스위치, 체크박스, 라디오, 다이얼로그 등)를 모든 사용자가 사용할 수 있도록 만든다. 앱 화면용 컴포넌트뿐 아니라 shared UI wrapper, trigger, primitive adapter 같은 재사용 컴포넌트도 이 기준을 먼저 만족해야 한다. 접근성을 지키면 스크린 리더/키보드 사용자뿐 아니라, `testing-library`의 `getByRole` 쿼리로 요소를 특정할 수 있어 테스트 코드도 견고해진다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 UI 컴포넌트를 만들거나 접근성을 개선할 때는 아래 reference 문서를 직접 읽고 컴포넌트별 체크리스트와 코드 예시를 확인한 뒤 적용한다.

스크린 리더는 요소를 **역할(Role) → 레이블(Label) → 상태(State)** 순으로 읽는다.

```tsx
// 스크린 리더 읽기: "홈, 탭, 선택됨"
<button role="tab" aria-selected={true}>홈</button>

// 레이블 우선순위: aria-labelledby > aria-label > <label> > 내부 텍스트
<button aria-label="닫기"><CloseIcon /></button>
```

---

## 4대 핵심 원칙

### 1.🧱 올바른 구조 만들기

인터랙티브 요소(버튼, 링크 등) 안에 인터랙티브 요소를 중첩하면 키보드 포커스와 스크린 리더 동작이 깨진다. 또한 어떤 요소가 눌릴지 불분명해지고, 포커스 순서가 꼬이며, 모바일에서 의도치 않은 요소가 눌릴 수 있다.

```tsx
// ❌ 중첩된 인터랙티브 요소 금지
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

- `<a>` 안에 `<button>`을 중첩하지 말고, `<Button as="a" href="/go-to">` 형태로 하나의 역할만 갖도록 한다
- 카드 전체 클릭 + 내부 별도 버튼이 필요한 경우, `position: absolute` 투명 버튼과 `z-index`를 이용한 레이어링 패턴을 쓴다
- 테이블 행을 클릭 가능하게 만들 때는 `<tr>`에 직접 onClick을 붙이지 말고, CSS 가상 요소(`::after`)로 링크 영역을 확장한다

→ 상세: [references/semantic-structure.md](references/semantic-structure.md)

### 2. 🗣️ 접근 가능한 이름으로 의미를 정확하게 전달한다.

레이블이 없으면 스크린 리더가 해당 요소의 기능을 설명할 수 없다. 레이블 우선순위는 `aria-labelledby` > `aria-label` > `<label>` > 내부 텍스트 순이다.

```tsx
// ❌ 레이블 없는 버튼
<button><CloseIcon /></button>

// ✅ aria-label로 이름 부여
<button aria-label="닫기"><CloseIcon /></button>
```

- 아이콘만 있는 버튼에는 반드시 `aria-label`을 추가하고, 텍스트가 함께 있으면 불필요하다
- 입력창에는 `<label htmlFor="id">`로 연결하고, 시각적 레이블을 넣을 수 없을 때만 `aria-label`을 쓴다
- 카드번호처럼 여러 입력이 하나의 그룹인 경우 `<fieldset>` + `<legend>`로 그룹화하고 각 입력에 `aria-label`을 붙인다
- 같은 이름의 버튼이 반복될 때는 `aria-labelledby`로 주변 텍스트를 조합하여 구분한다 — "종이를 사용할 경우 선택", "연필을 사용할 경우 선택"

→ 상세: [references/basics.md](references/basics.md)

### 3. 🎯 시맨틱 HTML 사용으로 예측 가능한 인터랙션 제공

`div + onClick`으로 만든 가짜 버튼은 키보드 포커스, Enter 제출, autocomplete를 지원하지 않기 때문에 button, form 과 같은 시맨틱 요소를 사용한다.

```tsx
// ❌ 가짜 버튼은 접근성 문제 발생
<div onClick={handleClick}>클릭</div>

// ✅ 진짜 버튼요소 사용
<button onClick={handleClick}>클릭</button>

<form onSubmit={handleSubmit}>
  <input />
  <button type="submit">제출</button>
</form>
```

- `<button>` 사용이 어려운 경우(block 요소 내부 등)에는 `role="button"` + `tabIndex={0}` + `onKeyDown` 으로 Enter/Space 키 입력을 처리하거나, react-aria의 `useButton` 훅을 사용한다
- `<form>` 안에 배치해야 Enter 키 제출, 자동완성, 스크린 리더 단축키 탐색이 동작한다. 제출이 아닌 버튼에는 반드시 `type="button"`을 명시한다
- 페이지 이동이 목적이면 `<button>` 대신 `<a>` 태그를 사용한다. 우클릭 컨텍스트 메뉴(새 창, 링크 복사)가 제공되기 때문이다
- 입력 필드에는 레이블 외에도 의미 있는 `name`, 적절한 `autocomplete`, 목적에 맞는 `type`/`inputMode`를 제공한다. 이메일·인증코드처럼 맞춤법 검사 대상이 아닌 입력은 `spellCheck={false}`를 검토한다
- 붙여넣기 차단을 위해 `onPaste` + `preventDefault()`를 사용하지 않는다. 비밀번호 관리자와 보조기기 흐름을 깨뜨릴 수 있다

실제 적용 전에는 [references/forms.md](references/forms.md)와 [references/semantic-structure.md](references/semantic-structure.md)를 직접 읽고, 폼·가짜 버튼·react-aria 활용 예시를 확인한다.

### 4. 🌈 각 정보에만 의존하지 않고 시각 정보 대체 텍스트를 제공한다.

이미지/아이콘 등 시각 요소에 대체 텍스트가 없으면 스크린 리더가 내용을 전달할 수 없다.

```tsx
// ❌
<img src="search.svg" alt="" />

// ✅ 의미 있는 이미지
<img src="search.svg" alt="검색" />

// ✅ 장식용 이미지
<img src="deco.svg" alt="" role="presentation" />
```

→ 상세 레퍼런스: [references/alt-text.md](references/alt-text.md)

---

## 엣지케이스

- **동적 상태**: 펼침/접힘, 선택 여부 등 동적 상태는 `aria-expanded`, `aria-selected`, `aria-checked`로 동기화한다. 주요 aria 상태 속성으로는 `aria-checked`(체크박스·스위치), `aria-selected`(탭·리스트), `aria-expanded`(아코디언·드롭다운), `aria-disabled`(비활성화), `aria-current`(네비게이션·달력), `aria-busy`(로딩), `aria-live`(실시간 업데이트)가 있다.
- **포커스 관리**: 모달이 열릴 때 포커스를 모달 내부로 이동하고, 닫힐 때 트리거 요소로 복귀시킨다. `<dialog>` + `showModal()`을 사용하면 포커스 이동·포커스 트랩·ESC 닫기·복원이 브라우저 기본 동작으로 제공된다. `<dialog>` 없이 구현할 때는 `inert` 속성으로 배경 콘텐츠를 비활성화하고 포커스 저장/복원을 직접 처리한다.
- **포커스 표시**: `outline: none` 또는 `outline-none`으로 기본 포커스를 제거했다면 반드시 `:focus-visible` 또는 `:focus-within`으로 대체 표시를 제공한다.
- **라이브 리전**: 비동기 알림/에러는 `aria-live="polite"`로 감싸야 스크린 리더가 변경을 자동으로 읽는다.
- **폼 에러 처리**: 제출 실패 시 첫 번째 오류 필드로 포커스를 이동하고, 에러 메시지는 필드 근처에서 `role="status"` 또는 `aria-live`로 전달한다.
- **스위치 컴포넌트**: `role="switch"` + `aria-checked`를 설정하고, 커스텀 요소일 때는 `tabIndex={0}`으로 키보드 포커스를, Space 키로 상태 변경을 지원한다.
- **탭 컴포넌트**: 탭 목록에 `role="tablist"`, 각 탭에 `role="tab"` + `aria-selected`, 패널에 `role="tabpanel"` + `aria-labelledby`를 설정한다. 비활성 탭 패널은 반드시 `hidden`으로 숨긴다.
- **오버스크롤 제어**: 모달·드로어·바텀시트처럼 자체 스크롤 영역이 있는 컴포넌트는 `overscroll-behavior: contain`을 검토한다.

실제로 모달·탭·스위치·체크박스·아코디언 등 구체적인 UI 컴포넌트를 구현할 때는 [references/ui-components.md](references/ui-components.md)의 컴포넌트별 체크리스트와 코드 예시를 반드시 확인한다.

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 UI 컴포넌트를 구현하기 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 컴포넌트를 만들기 전에 해당 문서를 직접 읽는다.

컴포넌트별 ARIA 패턴이 필요할 때 아래 파일을 읽는다.

| 파일                                                        | 내용                                                                       |
| ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| [ui-components.md](./references/ui-components.md)           | 모달, 스위치, 탭, 체크박스, 라디오, 아코디언 패턴과 포커스/오버스크롤 제어 |
| [forms.md](./references/forms.md)                           | 폼, 입력 속성, 유효성 검사, 가짜 버튼, react-aria 활용                     |
| [basics.md](./references/basics.md)                         | Role/Label/State 상세 가이드                                               |
| [semantic-structure.md](./references/semantic-structure.md) | 시맨틱 HTML, 인터랙티브 요소 중첩 금지, focus-visible/focus-within 패턴    |
| [eslint.md](./references/eslint.md)                         | eslint-plugin-jsx-a11y 을 통해 접근성 규칙 검사 자동화                     |
| [alt-text.md](./references/alt-text.md)                     | 이미지 대체 텍스트 작성법                                                  |

---

## 범위

- 일반 코드 품질 → `fe-code-conventions`
- React 컴포넌트 설계 → `fe-react-patterns`
- 성능 최적화 → `fe-react-performance`
