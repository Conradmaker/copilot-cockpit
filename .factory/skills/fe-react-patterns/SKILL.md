name: fe-react-patterns
description: "React component architecture and composition patterns. Use this skill when designing React component APIs, building compound components, deciding component structure, managing controlled and uncontrolled state, solving props drilling, implementing reusable wrapper components, adding polymorphism (`as`, `asChild`), typing shared component props, or migrating to React 19. Covers composition over configuration, compound components, explicit variants, state management patterns, reusable component API design, variant-driven styling contracts, and React 19 API changes. Always consult this skill when creating or restructuring any React component, especially shared UI wrappers or reusable building blocks, even if the user only asked to 'make a component'. For accessibility details use fe-a11y. For performance optimization use fe-react-performance instead. This skill extends vercel-composition-patterns with Korean instructions and additional patterns from the team's code quality guidelines. Triggers on: component architecture, compound components, composition pattern, props drilling, state management, controlled component, uncontrolled component, Context API design, component API, polymorphism, asChild, as prop, reusable wrapper, variant API, className merge, React 19, forwardRef removal, 컴포넌트 설계, 합성 패턴, 상태관리 패턴, 제어 컴포넌트, 비제어 컴포넌트, 컴포넌트 API, asChild, polymorphism, 재사용 가능한 컴포넌트, 래퍼 컴포넌트, boolean prop, 컴포넌트 나누기, 컴포넌트 분리, 커스텀 훅 패턴."

---

# React 컴포넌트 아키텍처 & 합성 패턴

## 목표

Boolean props를 최소화하고 작은 컴포넌트를 조합하는 방식으로 설계한다. Boolean prop 하나가 추가될 때마다 가능한 상태 조합이 2배로 늘어나 불가능한 상태(impossible states)가 발생하고 유지보수가 어려워진다.

또한 재사용 가능한 컴포넌트는 공개 API가 예측 가능해야 한다. `className` 병합 순서, controlled/uncontrolled 지원, `as` 또는 `asChild` 같은 합성 방식, HTML 속성 확장 방식이 일관돼야 여러 화면과 도메인에서 안전하게 재사용할 수 있다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 컴포넌트를 설계하거나 리팩토링할 때는 각각의 해당하는 reference 문서를 직접 읽고 Before/After 예시를 확인한 뒤 적용한다.

```tsx
// ❌ boolean props로 커스터마이징
<Composer isThread isEditing={false} showAttachments showFormatting={false} />

// ✅ 명시적 variant로 조합
<ThreadComposer channelId="abc" />
```

---

## 핵심 패턴

### 1. 합성 설계 (Composition over Configuration)

Boolean props/renderProps 대신 작은 컴포넌트의 조합으로 API를 설계하면 불가능한 상태 조합이 사라지고, Props Drilling 없이 데이터가 필요한 곳에서 직접 소비할 수 있다.

- Boolean props 대신 Explicit Variant 컴포넌트로 분리한다
  `isThread`, `isEditing`, `isForwarding`를 한 컴포넌트에 몰아 넣으면 호출부에서는 어떤 UI가 실제로 그려지는지 알기 어렵다. `ThreadComposer`, `EditComposer`, `ForwardMessageComposer`처럼 variant를 분리하면 호출부만 봐도 역할과 상태가 드러난다.
- 공유 컨텍스트로 관련 컴포넌트를 그룹화한다 (Compound Components)
  `Composer.Frame`, `Composer.Input`, `Composer.Footer`, `Composer.Submit`처럼 내부 조각을 노출하면 소비자가 필요한 UI 구조만 조합할 수 있다. 이 방식은 거대한 부모 컴포넌트의 숨겨진 조건문보다 읽기 쉽고, Footer 액션만 바꾸는 식의 부분 교체도 자연스럽다.
- renderX props 대신 children으로 조합한다
  `renderFooter`, `renderActions`, `renderHeader` 같은 API는 콜백 시그니처를 먼저 이해해야 해서 구조 파악이 늦다. `<Composer.Footer><Composer.Formatting /><Composer.Submit /></Composer.Footer>`처럼 children 기반으로 조합하면 화면 구조가 JSX에 그대로 드러난다.
- Props Drilling은 Composition으로 해결한다
  중간 컴포넌트가 `keyword`, `onClose`, `recommendedItems` 같은 prop을 직접 쓰지 않고 아래로만 전달한다면 이미 결합도가 높아진 상태다. 이럴 때는 자식 슬롯을 열어 필요한 위치에 직접 렌더링하거나 compound component로 소비 위치를 아래로 내린다.
- 동시에 실행되지 않는 코드를 별도 컴포넌트로 분리한다
  한 컴포넌트 안에서 `isEditing ? ... : isForwarding ? ... : ...` 같은 분기가 반복되면 서로 배타적인 모드가 한 파일에 섞인 것이다. 이 경우 공통 뼈대만 재사용하고, 실제 모드별 UI는 별도 variant 컴포넌트로 나누는 편이 변경에 강하다.

#### 빠른 판단 기준

- Boolean prop이 2개 이상 붙기 시작하면 variant 분리를 먼저 검토한다
- `renderHeader`, `renderFooter`, `renderActions`처럼 render prop이 늘어나면 compound components가 더 적합한지 본다
- 중간 컴포넌트가 받은 props를 그대로 아래로만 넘기면 Props Drilling 신호로 본다
- 코드가 "무엇을 렌더링하는지"보다 "어떤 모드인지" 설명하는 분기로 가득하면 composition으로 다시 설계한다

실제 적용 전에는 [references/composition.md](references/composition.md)를 직접 읽고, Boolean props를 explicit variants로 바꾸는 예시와 render props를 children 조합으로 바꾸는 예시를 확인한다.

→ 상세: [references/composition.md](references/composition.md)

### 2. 상태 관리 (State Lifting · Context Interface)

Provider 컴포넌트로 상태를 끌어올려 형제 컴포넌트 간 공유하되, UI는 구현 상세를 모르고 인터페이스만 소비해야 상태 라이브러리 교체가 자유롭다.

- Provider 컴포넌트로 상태를 끌어올려 형제 간 공유한다 (State Lifting)
  상태가 컴포넌트 내부에 갇혀 있으면 다이얼로그 하단의 액션 버튼이나 미리보기 패널이 같은 데이터를 쓰기 어렵다. `ForwardMessageProvider` 같은 상위 Provider로 끌어올리면 `Composer.Frame` 바깥에 있는 `MessagePreview`, `ForwardButton`도 같은 상태와 액션을 읽을 수 있다.
- Provider만 상태 구현을 알고, UI는 인터페이스만 소비한다 (Implementation Decoupling)
  `ChannelComposer` 같은 UI 컴포넌트가 `useState`, Zustand, 서버 동기화 훅을 직접 알기 시작하면 재사용성이 급격히 떨어진다. 상태 구현은 Provider에 격리하고, UI는 `state`, `actions`, `meta`만 소비하게 하면 같은 UI를 로컬 상태와 전역 상태 양쪽에 붙일 수 있다.
- state/actions/meta 제네릭 인터페이스로 의존성을 주입한다 (Context Interface)
  Context 값은 한 덩어리 객체로 두기보다 역할별로 나누는 것이 좋다. `state`는 input, attachments, isSubmitting 같은 읽기 모델을 담고, `actions`는 update, submit 같은 변경 함수를 담고, `meta`는 inputRef 같은 부가 정보를 담게 하면 Provider가 달라도 UI 계약은 안정적으로 유지된다.

#### 피해야 할 패턴

- 형제 컴포넌트 동기화를 위해 `useEffect`로 상태를 복사하지 않는다
  `onInputChange`로 부모 상태를 따로 들고 매 입력마다 동기화하면 원본 상태가 둘이 된다. 이런 구조는 누락과 타이밍 버그가 생기기 쉬우므로 상태를 한 곳으로 끌어올리는 편이 낫다.
- 외부에서 내부 상태를 읽기 위해 ref를 임시 저장소처럼 쓰지 않는다
  `stateRef.current`를 외부에서 읽어 submit에 쓰는 방식은 React의 데이터 흐름을 우회한다. 상태와 액션이 필요하면 ref가 아니라 Context 인터페이스로 노출한다.
- UI 컴포넌트 안에서 상태 구현 훅을 직접 호출해 구조를 결합시키지 않는다
  예를 들어 `ComposerInput` 내부에서 특정 전역 스토어 훅을 직접 호출하면 그 컴포넌트는 더 이상 다른 Provider와 함께 재사용할 수 없다. UI는 항상 인터페이스를 소비하고, 구현 선택은 Provider가 맡는다.

#### 빠른 판단 기준

- 상태를 같이 써야 하는 형제 컴포넌트가 2개 이상이면 Provider로 끌어올릴지 먼저 본다
- 같은 UI를 다른 데이터 소스에 붙여 재사용해야 하면 Provider 분리 구조를 택한다
- Context 값이 커지더라도 역할이 `state/actions/meta`로 나뉘면 허용하고, 역할이 섞이면 다시 분해한다

실제 적용 전에는 [references/state-management.md](references/state-management.md)를 직접 읽고, `useEffect` 동기화나 ref 우회 방식 대신 Provider로 상태를 끌어올리는 예시를 확인한다.

→ 상세: [references/state-management.md](references/state-management.md)

### 3. 재사용 가능한 컴포넌트 API 설계

재사용 컴포넌트는 JSX 한 줄로도 의도가 읽혀야 하고, 소비자가 HTML 의미론과 동작을 제어할 수 있어야 한다.

- controlled와 uncontrolled를 둘 다 지원할지 먼저 결정한다
  입력, 아코디언, 탭처럼 상위 상태 제어가 자주 필요한 컴포넌트는 `value`/`open` + `onChange` 계열과 `defaultValue`/`defaultOpen` 계열을 함께 설계한다. 반대로 단순 presentational wrapper라면 이런 상태 API를 만들지 않는다.
- 기본 엘리먼트의 HTML 속성을 그대로 확장한다
  `<button>`을 감싸는 컴포넌트라면 `React.ComponentProps<"button">`를 바탕으로 설계해서 `type`, `disabled`, `aria-*`, `className` 같은 속성이 자연스럽게 통과되게 만든다.

#### 빠른 판단 기준

- 상위에서 상태를 제어해야 하는 시나리오가 2개 이상 나오면 controlled/uncontrolled 지원을 먼저 검토한다
- `href`, `type`, `target`, `aria-*`를 그대로 열어줘야 하는 wrapper면 native props 확장을 기본으로 둔다

---

## 엣지케이스: React 19 마이그레이션

| 변경사항        | 내용                                                           |
| --------------- | -------------------------------------------------------------- |
| forwardRef 제거 | ref를 일반 prop으로 직접 전달한다                              |
| use() 도입      | `useContext()` 대신 `use()`를 사용한다. 조건부 호출이 가능하다 |

### 빠른 체크리스트

- React 19 이상일 때만 `use()`와 새 Context Provider 문법을 적용한다
- `forwardRef`가 꼭 필요한 구조인지 먼저 보고, 가능하면 일반 `ref` prop 전달로 단순화한다
- `useContext()`를 기계적으로 치환하기보다 조건부 Context 소비가 필요한 지점에 `use()`를 우선 적용한다
- 새 Provider 문법 `<Context value={...}>`를 쓸 수 있지만, 팀 코드베이스가 아직 React 18 호환을 유지하면 기존 문법을 유지한다

### 적용 예시

- `forwardRef((props, ref) => <Input ref={ref} {...props} />)` 형태의 래퍼 컴포넌트는 React 19에서는 일반 `ref` prop을 받는 함수 컴포넌트로 단순화할 수 있다
- Compound Component 내부에서 `ComposerContext`를 읽을 때, 기존 `useContext(ComposerContext)`는 `use(ComposerContext)`로 바꿀 수 있다
- variant에 따라 다른 Context를 읽어야 하는 입력 컴포넌트라면 `if (variant === "rich") { const value = use(RichEditorContext) }` 같은 조건부 소비가 가능해진다

실제 마이그레이션 전에는 [references/react19.md](references/react19.md)를 직접 읽고, 프로젝트의 React 버전과 호환성 조건을 먼저 확인한다.

→ 상세: [references/react19.md](references/react19.md)

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 적용 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 변경을 시작하기 전에 해당 문서를 직접 읽는다.

| 파일                             | 내용                                                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `references/composition.md`      | Compound Components, Explicit Variants, Boolean Props 지양, Props Drilling 해결하여 컴포넌트 API 설계, 리팩토링 하는 방법   |
| `references/state-management.md` | State Lifting, Implementation Decoupling, Context Interface 패턴을 활용하여 Context API 설계, 상태 공유 구조 설계 하는 방법 |
| `references/react19.md`          | React 19 마이그레이션 시 forwardRef 제거, use() 사용법, 마이그레이션 가이드                                                 |

---

## 범위

- Tailwind CSS 스타일링 패턴 (className 병합, CVA, 토큰, 애니메이션) → `fe-tailwindcss`
- 공유 컴포넌트 API 설계 (as/asChild, prop type export, single element boundary, 토큰/테마, 배포) → `fe-ui-element-components`
- 성능 최적화 (메모이제이션, 번들, 렌더링 최적화) → `fe-react-performance`
- 일반 코드 컨벤션 (네이밍, 파일 구조, 가독성) → `fe-code-conventions`
- 접근성 (ARIA, 키보드, 시맨틱 HTML) → `fe-a11y`
