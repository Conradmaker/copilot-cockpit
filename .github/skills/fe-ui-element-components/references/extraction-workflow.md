# 컴포넌트 추출 워크플로

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 제품 화면에서 재사용 가능한 컴포넌트를 추출하고, 시간이 지나며 발생하는 drift를 진단하는 절차를 다룬다.

---

## 1. 추출 판단 기준

### 추출해야 할 때

- 같은 시각적 패턴이 **3곳 이상**에서 반복된다
- 반복되는 패턴의 **behavior(상태, 이벤트, API)**가 동일하거나 매우 유사하다
- 변경이 한 곳에서 일어나면 다른 곳도 함께 바뀌어야 한다

### 추출하지 말아야 할 때

- 시각적으로 비슷하지만 **behavior가 다르다** — 강제 통합하면 분기 지옥이 된다
- 2곳에서만 반복되고, 추후 확장 계획이 불분명하다
- 추출하면 props가 5개 이상 필요해진다 — 과도한 일반화의 신호

---

## 2. 추출 절차

### Step 1: 후보 식별

제품 화면을 훑으며 시각적 반복 패턴을 수집한다.

- 사용처(화면, 컴포넌트 경로)와 현재 구현 방식을 기록한다
- 각 사용처의 **공통점**과 **차이점**을 나열한다

### Step 2: API 설계

- 공통점은 **기본 동작(default)**으로 만든다
- 차이점 중 빈도가 높은 것은 **variant** 또는 **prop**으로 수용한다
- 차이점 중 빈도가 낮은 것은 **composition(children, slot, render prop)**으로 열어둔다
- boolean prop 2개 이상이 조합되면 enum variant로 교체한다

### Step 3: 구현과 이관

1. 추출된 컴포넌트를 shared 위치에 생성한다
2. 기존 사용처를 하나씩 교체하며 visual regression이 없는지 확인한다
3. 교체 완료 후 기존 중복 코드를 제거한다

---

## 3. Drift 진단

시간이 지나면 추출된 컴포넌트와 실제 사용처 사이에 drift가 생긴다.

### 증상

| 증상 | 원인 | 처방 |
| --- | --- | --- |
| 같은 컴포넌트인데 화면마다 미세하게 다르다 | 사용처에서 className이나 style override를 직접 넣었다 | variant로 공식화하거나, 의도적 차이인지 확인 |
| 공용 컴포넌트 변경 시 사이드 이펙트가 여러 곳에서 발생한다 | 컴포넌트가 너무 많은 context를 알고 있다 | 관심사 분리, composition 패턴 도입 |
| 새 기능을 넣으려면 기존 prop에 분기를 추가해야 한다 | 컴포넌트가 과도하게 일반화되었다 | 분리(fork)를 검토 — 모든 것을 한 곳에 담지 않는다 |
| 컴포넌트 이름과 실제 역할이 맞지 않는다 | 원래 목적에서 벗어나 기능이 누적되었다 | rename 또는 책임 분리 |

### Drift 정기 점검 질문

1. 이 컴포넌트의 사용처 수를 알고 있는가?
2. 사용처 중 override(`className`, `style`, `!important`)가 있는 곳은 몇 개인가?
3. 마지막으로 이 컴포넌트의 API를 의도적으로 리뷰한 시점은 언제인가?

---

## 4. 분류 기준 (Taxonomy 연결)

추출된 컴포넌트가 어디에 속하는지 빠르게 판단한다.

| 분류 | 특성 | 예시 |
| --- | --- | --- |
| Primitive | 스타일 없는 동작 단위, headless | Dialog primitive, Focus scope |
| Component | 재사용 가능한 styled UI 단위 | Button, Input, Select |
| Block | 제품 use case 특화 조합 | Pricing section, Auth screen |

- Primitive는 behavior만 제공하고 visual은 consumer가 결정한다
- Component는 default visual + override 가능성을 가진다
- Block은 copy-and-paste 친화적이며 강한 default를 가진다

→ 상세 분류 기준: [taxonomy.md](taxonomy.md)

---

## 체크리스트

- [ ] 3곳 이상 반복되는 패턴인가
- [ ] behavior가 동일하거나 variant로 수용 가능한가
- [ ] boolean prop 조합이 아닌 enum variant를 사용하는가
- [ ] 기존 사용처를 교체할 때 visual regression 검증을 했는가
- [ ] 정기적으로 override/drift를 점검하는가
