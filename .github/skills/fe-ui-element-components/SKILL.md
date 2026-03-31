---
name: fe-ui-element-components
description: "Design-system component patterns for reusable primitives, shared UI libraries, tokens, theming, styling contracts, polymorphic APIs, and distribution. Use when building components for multi-project reuse: shared primitives, buttons, dialogs, inputs, design tokens, theme systems, npm/registry packages, polymorphic components (as/asChild), prop type exports, or primitive vs component decisions. Always consult for shared UI work, even if the user only asks to 'make a component' or 'create reusable elements' without mentioning design system. For product screens use fe-react-patterns/fe-a11y; for styling use fe-tailwindcss. Triggers on: design system, UI kit, shared component, component library, primitive, design token, theming, data-state, data-slot, asChild, polymorphic, registry, npm package, reusable UI, 디자인 시스템, 공용 컴포넌트, UI 킷, 컴포넌트 라이브러리, 프리미티브, 재사용 UI."
disable-model-invocation: false
user-invocable: false
---

# 공유 UI Element 컴포넌트

## 목표

공유 UI 컴포넌트를 앱 화면용 컴포넌트와 구분해서 설계한다. 이 스킬의 목표는 버튼 하나를 예쁘게 만드는 것이 아니라, 여러 프로젝트에서 재사용 가능한 컴포넌트의 수준을 정의하고, 토큰과 스타일 계약을 설계하고, 문서화와 배포 방식까지 일관되게 결정하는 것이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 디자인 시스템 컴포넌트를 만들거나 배포 전략을 정할 때는 아래 reference 문서를 직접 읽고 패턴과 예시를 확인한 뒤 적용한다.

---

## 6대 핵심 원칙

### 1. 🧱 먼저 어떤 artifact인지 분류한다

디자인 시스템 작업에서 가장 먼저 해야 할 일은 “지금 만드는 것이 primitive인지, styled component인지, block인지”를 구분하는 것이다. 이 분류가 흐려지면 API가 과도해지고 배포 단위와 문서 범위도 같이 흔들린다.

- primitive는 동작과 접근성만 제공하고 스타일은 주입받는다
- component는 visual default를 포함한 재사용 UI 단위다
- block은 product use case가 섞인 조합 결과물이라 라이브러리 import보다 copy-and-paste에 가깝다
- template은 여러 page와 provider, routing까지 포함한 시작점이다

#### 빠른 판단 기준

- 스타일 없이 동작과 a11y만 책임지면 primitive로 본다
- 여러 화면에서 import해 쓰는 low-level UI면 component로 본다
- 카피, 레이아웃, use case가 강하면 block으로 본다
- 앱 뼈대와 페이지 집합이면 template로 본다

실제 적용 전에는 [references/taxonomy.md](references/taxonomy.md)를 직접 읽고, primitive/component/block/template 구분 기준을 확인한다.

→ 상세: [references/taxonomy.md](references/taxonomy.md)

### 2. 🎨 토큰과 테마를 먼저 설계한다

공유 컴포넌트는 특정 브랜드 값에 묶이면 오래가지 못한다. 색상, spacing, radius, shadow 같은 값은 semantic token으로 추상화하고, 컴포넌트는 그 토큰을 소비하는 쪽이 유지보수에 유리하다.

- raw color보다 semantic token을 먼저 정의한다
- light/dark뿐 아니라 brand, density, accessibility override를 염두에 둔다
- 컴포넌트는 직접 값을 갖기보다 theme variable을 읽게 만든다
- 토큰 네이밍은 usage와 role이 드러나야 한다

#### 빠른 판단 기준

- `#1d4ed8` 같은 raw value가 컴포넌트 코드에 반복되면 토큰화 후보로 본다
- 버튼, input, card가 같은 surface/foreground를 공유하면 component prop보다 theme token을 먼저 손본다
- 여러 브랜드나 제품군을 지원해야 하면 token layer를 먼저 고정한다

실제 적용 전에는 [references/tokens-and-theming.md](references/tokens-and-theming.md)를 직접 읽고, semantic token과 theme variable 구조를 확인한다.

→ 상세: [references/tokens-and-theming.md](references/tokens-and-theming.md)

### 3. 🧩 variant는 시각적 계약으로, 구조 변경은 컴포넌트 분리로 해결한다

`variant`, `size`, `tone`처럼 시각적 차이만 variant prop으로 관리한다. footer 액션, field 배치, child structure가 달라지는 경우는 variant가 아니라 별도 컴포넌트로 분리한다.

- variant는 visual contract다 — 구조가 바뀌는 모드까지 하나의 variant prop에 넣지 않는다
- state (loading, open, active)와 variant (primary, secondary)는 별개 축이다
- state를 className branching이나 `data-state`로 표현하고, variant와 분리한다

### 4. 🧩 스타일과 상태 계약을 외부에 노출한다

디자인 시스템 컴포넌트는 내부 상태를 감추되, 소비자가 styling hook을 안정적으로 잡을 수 있어야 한다. 이때 `data-state`, `data-slot` 같은 data attribute는 prop explosion 없이 상태와 구조를 노출하는 좋은 방법이다.

- open/closed, active/inactive 같은 시각 상태는 `data-state`로 노출한다
- 조합 구조 안의 역할은 `data-slot`으로 식별한다
- `className` 하나로 override 가능하도록 계약을 단순하게 유지한다
- state styling과 variant styling의 책임을 분리한다

#### 빠른 판단 기준

- `openClassName`, `closedClassName` 같은 prop이 늘어나면 data attribute 계약으로 바꿀지 검토한다
- 부모가 자식 슬롯을 안정적으로 target해야 하면 `data-slot`을 검토한다
- 같은 상태를 CSS와 JS가 따로 추적하면 계약이 약한 상태로 본다

실제 적용 전에는 [references/style-contracts.md](references/style-contracts.md)를 직접 읽고, `data-state`, `data-slot`, override-friendly contract 패턴을 확인한다.

→ 상세: [references/style-contracts.md](references/style-contracts.md)

### 5. 🔌 공유 컴포넌트 API를 설계한다

디자인 시스템 컴포넌트는 앱 전용 컴포넌트보다 API 계약이 중요하다. 특히 `as`/`asChild` 같은 polymorphism, prop type export, single element boundary 원칙은 shared primitive와 trigger 계열에서 핵심이다.

- `as` 또는 `asChild`는 링크처럼도 쓰이고 버튼처럼도 쓰이는 shared primitive, trigger 계열에만 도입한다
- `ButtonProps`, `DialogContentProps` 같은 타입을 export해서 래퍼 확장을 쉽게 만든다
- 하나의 컴포넌트는 가능하면 하나의 element boundary를 책임지게 한다
- title, description, footer를 한 컴포넌트 prop으로 다 받으면 compound component나 slot으로 분리한다

실제 적용 전에는 [references/component-api.md](references/component-api.md)를 직접 읽고, `as`/`asChild` 선택 기준, prop type export, single element boundary 패턴을 확인한다.

→ 상세: [references/component-api.md](references/component-api.md)

### 6. 📦 문서화와 배포 단위까지 함께 설계한다

디자인 시스템 컴포넌트는 코드만으로 끝나지 않는다. 어떤 설치 방식이 맞는지, 문서 페이지에 무엇을 보여줄지, npm과 registry 중 무엇이 코드 소유권과 업데이트 정책에 맞는지 함께 정해야 한다.

- npm package는 버전 관리와 중앙 배포에 강하다
- registry는 source ownership과 copy-and-paste distribution에 강하다
- marketplace는 discovery와 유통 채널에 강하다
- 문서는 demo, 설치법, API, a11y, changelog까지 포함해야 한다

#### 빠른 판단 기준

- 소비자가 코드를 직접 수정해야 하면 npm보다 registry를 먼저 검토한다
- 내부 팀에서 버전 고정과 peer dependency 관리가 중요하면 npm package가 유리하다
- 외부 배포와 발견 가능성이 중요하면 marketplace를 검토한다
- 컴포넌트 설치 방법을 한 줄 명령으로 설명할 수 없다면 배포 전략이 아직 정리되지 않은 상태로 본다

실제 적용 전에는 [references/distribution.md](references/distribution.md)와 [references/documentation.md](references/documentation.md)를 직접 읽고, 배포 방식과 문서 구조를 확정한다.

→ 상세: [references/distribution.md](references/distribution.md)

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 디자인 시스템 컴포넌트를 설계하거나 배포하기 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 작업을 시작하기 전에 해당 문서를 직접 읽는다.

| 파일 | 내용 |
| --- | --- |
| `references/taxonomy.md` | primitive, component, block, template 분류 기준과 artifact 수준 판단법 |
| `references/tokens-and-theming.md` | semantic token, CSS variable, light/dark 및 multi-brand theme 구조 설계법 |
| `references/style-contracts.md` | `data-state`, `data-slot`, override-friendly styling contract 설계법 |
| `references/component-api.md` | `as`/`asChild`, prop type export, single element boundary, polymorphic 컴포넌트 설계 |
| `references/distribution.md` | npm, registry, marketplace의 차이와 선택 기준 |
| `references/documentation.md` | demo, installation, API, accessibility, changelog를 포함한 문서 페이지 설계 |

---

## 범위

- Tailwind CSS 스타일링 패턴 (className 병합, CVA, 토큰 설정, 애니메이션) → `fe-tailwindcss`
- 일반 React 컴포넌트 구조, controlled/uncontrolled, 합성 패턴 → `fe-react-patterns`
- 접근성 (ARIA, 키보드, 시맨틱 HTML) → `fe-a11y`
- 일반 코드 품질, 응집도, 결합도 → `fe-code-conventions`
- 성능 최적화 → `fe-react-performance`
