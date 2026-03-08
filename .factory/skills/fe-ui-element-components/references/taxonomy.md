# Artifact 분류 체계

디자인 시스템 컴포넌트를 설계할 때는 구현보다 분류가 먼저다. 지금 만드는 것이 primitive인지 component인지 block인지 명확하지 않으면 API, 문서, 배포 단위가 모두 흔들린다.

---

## 1. Primitive

primitive는 스타일 없는 동작 단위다. 의미론, 포커스 관리, 키보드 인터랙션, layering, ARIA wiring 같은 behavior를 제공하지만 visual default는 제공하지 않는다.

### 예시

- Dialog primitive
- Popover primitive
- Tooltip primitive
- Focus scope

### 기대 사항

- headless에 가깝다
- single responsibility를 가진다
- role에 필요한 a11y 동작을 기본 제공한다
- styled component가 위에서 감싸기 쉽다

---

## 2. Component

component는 재사용 가능한 styled UI 단위다. primitive를 감싸거나 자체 구현을 가질 수 있지만, 앱 여러 곳에서 import해 사용하는 low-level building block이어야 한다.

### 예시

- Button
- Input
- Dialog
- Select

### 기대 사항

- default visual style을 가진다
- `className`, token, variant 등으로 override 가능해야 한다
- keyboard와 screen reader 사용성을 기본으로 갖춘다
- composition과 controlled/uncontrolled 시나리오를 고려한다

---

## 3. Block

block은 product use case가 강한 조합 결과물이다. speed of adoption을 위해 강한 default를 가지지만 일반 component처럼 import해서 everywhere에 쓰는 대상은 아니다.

### 예시

- Pricing section
- Auth screen block
- Billing form block
- AI chat panel

### 기대 사항

- copy-and-paste 친화적이다
- layout과 content scaffold를 포함한다
- domain logic은 handler로 주입하거나 stub 처리한다
- component library보다 registry distribution에 잘 맞는다

---

## 4. Template

template은 여러 page, provider, layout, routing까지 포함한 시작점이다. import보다 fork와 customization을 전제로 한다.

### 예시

- SaaS starter
- E-commerce template
- Dashboard application shell

### 기대 사항

- 여러 route를 포함한다
- global provider와 layout shell을 포함한다
- opinionated project structure를 가진다

---

## 빠른 판단 체크리스트

- 스타일 없이 behavior와 a11y만 책임지면 primitive
- low-level reusable UI면 component
- use case와 copy가 섞인 opinionated 조합이면 block
- 앱 시작점과 페이지 집합이면 template