---
name: fe-code-conventions
description: "Frontend clean code conventions and code quality principles. Use this skill when writing new frontend code, refactoring existing code, reviewing code quality, or when the user asks about naming conventions, code readability, file/directory structure, component organization, or coupling/cohesion decisions. This covers language-agnostic frontend principles (not React-specific patterns - see fe-react-patterns for those). Always consult this skill during any frontend code writing or refactoring task, even if the user doesn't explicitly ask about code quality. Triggers on: code refactoring, clean code, naming, readability, file structure, code organization, coupling, cohesion, code conventions, 코드 컨벤션, 클린코드, 리팩토링, 변수명, 함수명, 폴더 구조, 디렉토리 구조, 코드 정리, 코드 개선, 좋은 코드, 매직넘버, 하드코딩, 조건문 정리, 코드 구조, 코드 품질, 읽기 쉬운 코드, 유지보수, 코드가 복잡해, 함수가 너무 길어."
---

# 프론트엔드 클린 코드

## 목표

새로운 요구사항이 생겼을 때 기존 코드를 수정하고 배포하기 쉬운 코드를 작성한다. 변경하기 쉬운 코드인지는 아래 4가지 원칙으로 판단한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 코드를 작성하거나 리팩토링할 때는 아래 reference 문서를 직접 읽고 Before/After 예시를 확인한 뒤 적용한다.

---

## 4대 원칙

### 1. 가독성 (Readability)

한 번에 고려해야 하는 맥락이 적고, 위에서 아래로 자연스럽게 읽히는 코드를 작성한다. 가독성을 높이는 3가지 전략은 **맥락 줄이기**, **이름 붙이기**, **위에서 아래로 읽히게 하기**다.

- 매직 넘버에 이름 붙인다
  `300`이라는 숫자만으로는 애니메이션 대기인지, 서버 응답 시간인지, 테스트 코드 잔여물인지 알 수 없다. `const ANIMATION_DELAY_MS = 300`처럼 상수로 선언하면 맥락이 즉시 드러나고 수정 누락도 방지된다.
- 복잡한 조건식에 의미 있는 이름을 부여한다
  `filter`, `some`, `&&`가 여러 단계로 중첩된 조건은 한눈에 파악하기 어렵다. `const isSameCategory = ...`, `const isPriceInRange = ...`처럼 각 조건에 이름을 붙이면 한 번에 고려해야 할 맥락이 줄어든다.
- 중첩된 삼항 연산자는 if문으로 풀어 쓴다
  `A ? "BOTH" : B ? (C ? "A" : "B") : "NONE"` 같은 중첩 삼항은 IIFE + if문으로 풀면 각 분기의 의도가 명확해진다.
- 범위 비교는 수학 부등식 순서로 작성한다
  `if (a >= b && a <= c)` 대신 `if (b <= a && a <= c)`로 쓰면 `b ≤ a ≤ c` 형태로 읽혀서 범위 조건을 직관적으로 이해할 수 있다.
- 구현 상세는 Wrapper 컴포넌트나 함수로 추상화한다
  한 사람이 동시에 고려할 수 있는 맥락의 수는 약 6~7개다. 로그인 체크, 권한 확인 같은 횡단 관심사는 `AuthGuard` 같은 래퍼로 추상화하면 메인 컴포넌트의 복잡도가 줄어든다.

실제 적용 전에는 [references/readability.md](references/readability.md)를 직접 읽고, 매직 넘버·조건식·삼항 연산자·구현 추상화의 Before/After 예시를 확인한다.

→ 상세 레퍼런스: [references/readability.md](references/readability.md)

### 2. 예측 가능성 (Predictability)

함수 이름과 파라미터만 보고 동작을 예측할 수 있어야 사이드 이펙트 없이 코드를 안전하게 변경할 수 있다.

- 라이브러리 함수명과 겹치지 않는 명확한 이름을 사용한다
  `http.get`을 래핑하면서 내부에서 토큰을 가져오는 추가 작업을 숨기면, 호출자는 단순한 GET 요청으로 오해한다. `httpService.getWithAuth()`처럼 이름 자체가 동작을 설명해야 기대 동작과 실제 동작의 차이가 사라진다.
- 같은 종류의 함수는 반환 타입을 통일한다
  API Hook이 어떤 곳에서는 `Query` 객체를, 어떤 곳에서는 `data`만 반환하면 호출할 때마다 반환 타입을 확인해야 한다. 유효성 검사 함수도 마찬가지로 `boolean`과 `{ ok, reason }` 객체가 섞이면 `if (checkIsAgeValid(age))` 같은 코드가 항상 truthy가 되는 버그가 생길 수 있다. Discriminated Union 타입으로 통일하면 컴파일러가 검증해준다.
- 이름·파라미터·반환값에 드러나지 않는 숨은 로직을 제거한다
  `fetchBalance()` 안에 로깅이 숨어 있으면, 함수를 호출하는 쪽에서 로깅이 발생하는지 예측할 수 없다. 숨은 사이드 이펙트는 별도 함수로 분리하거나 이름에 명시한다.

실제 적용 전에는 [references/predictability.md](references/predictability.md)를 직접 읽고, 이름 충돌·반환 타입 불일치·숨은 로직의 Before/After 예시를 확인한다.

→ 상세: [references/predictability.md](references/predictability.md)

### 3. 응집도 (Cohesion)

함께 변경되는 코드가 같은 위치에 있어야 수정 누락이 방지된다.

- 함께 수정되는 파일을 같은 디렉토리에 배치한다 (도메인별 코로케이션)
  `components/`, `hooks/`, `utils/` 같은 종류별 분류는 어떤 코드가 어떤 코드를 참조하는지 파악하기 어렵고, 기능 삭제 시 사용되지 않는 코드가 남기 쉽다. 도메인 단위(`domains/Domain1/components`, `domains/Domain1/hooks`)로 배치하면 의존 관계가 명확해지고 기능 삭제 시 디렉토리 하나만 제거하면 된다.
- 매직 넘버를 상수로 추출하여 관련 코드와 함께 관리한다
  `delay(300)`에서 `300`이 애니메이션 대기 시간이라면 애니메이션을 변경할 때 이 값도 함께 수정되어야 한다. 매직 넘버로 두면 수정이 누락될 수 있다 — 같이 수정되어야 할 코드 중 한쪽만 수정되는 것이 응집도 문제다.
- 폼 설계 시 필드 단위 응집도와 폼 전체 단위 응집도를 상황에 맞게 선택한다
  각 필드가 독립적으로 검증 로직을 가지는 방식(react-hook-form의 validate)과, Zod 스키마로 전체 폼의 규칙을 한곳에 모으는 방식이 있다. 필드 간 교차 검증이 많거나 검증 규칙이 자주 바뀌면 폼 단위 응집도가, 필드마다 독립적이면 필드 단위 응집도가 적합하다.

실제 적용 전에는 [references/cohesion.md](references/cohesion.md)를 직접 읽고, 디렉토리 구조·매직 넘버·폼 설계의 Before/After 예시를 확인한다.

→ 상세: [references/cohesion.md](references/cohesion.md)

### 4. 결합도 (Coupling)

코드를 수정했을 때 그 영향 범위가 좁고 예측 가능해야 안전하게 변경할 수 있다.

- 하나의 Hook/함수에 하나의 책임만 부여한다
  `usePageState`처럼 "이 페이지에 필요한 모든 쿼리 파라미터"를 관리하는 광범위 Hook은 수정 시 영향 범위가 급격히 확장된다. `useCardIdQueryParam()`, `useStatusListQueryParam()`처럼 쿼리 파라미터별로 분리하면 수정 영향이 좁아지고 이름도 명확해진다.
- 불필요한 공통화보다 중복을 허용하여 영향 범위를 축소한다
  여러 페이지에서 반복되는 로직을 하나의 Hook으로 공통화하면, 한 페이지의 요구사항이 바뀔 때 모든 사용처를 테스트해야 한다. 동작이 앞으로도 동일할 예정이면 공통화(응집도 우선)하고, 페이지마다 달라질 여지가 있으면 중복을 허용(결합도 우선)한다.
- Props Drilling은 Composition으로 먼저 해결하고, 그래도 안 되면 Context API를 사용한다
  중간 컴포넌트가 props를 전달만 하고 사용하지 않는다면 이미 결합도가 높아진 상태다. `children` prop을 이용한 조합 패턴으로 depth를 먼저 줄이고, 조합으로도 해결되지 않을 때 Context를 도입한다.

실제 적용 전에는 [references/coupling.md](references/coupling.md)를 직접 읽고, 단일 책임 Hook·공통화 판단 기준·Props Drilling 해결의 Before/After 예시를 확인한다.

→ 상세: [references/coupling.md](references/coupling.md)

---

## 원칙 간 트레이드오프

4가지 원칙을 동시에 완벽하게 충족하기는 어렵다. 상황에 따라 우선순위를 판단한다.

**가독성 vs 응집도**: 공통화/추상화하면 추상화 계층이 늘어 가독성이 떨어진다. 수정 누락 시 오류 위험이 높으면 응집도 우선, 위험이 낮으면 가독성 우선(중복 허용).

**응집도 vs 결합도**: 중복 코드를 허용하면 영향 범위가 줄어 결합도가 낮아진다. 동작이 동일하고 앞으로도 동일할 예정이면 응집도를 위해 공통화하고, 페이지마다 다르게 동작할 여지가 있으면 결합도를 위해 중복을 허용한다.

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 적용 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 변경을 시작하기 전에 해당 문서를 직접 읽는다.

| 파일                                              | 내용                                                                    |
| ------------------------------------------------- | ----------------------------------------------------------------------- |
| [readability.md](references/readability.md)       | 코드를 읽기 쉽고 만들고, 네이밍/조건문/함수 분리하는 가독성 원칙 적용법 |
| [predictability.md](references/predictability.md) | 함수 이름/반환 타입/숨겨진 로직에 대한 예측 가능성 원칙 적용법          |
| [cohesion.md](references/cohesion.md)             | 디렉토리 구조, 매직 넘버, 폼 설계시 응집도 원칙 적용법                  |
| [coupling.md](references/coupling.md)             | Hook 책임 분리, 공통화 여부, Props Drilling에 대한 결합도 원칙 적용법   |

---

## 범위

- React 전용 패턴 (컴포넌트 설계, 상태 관리, 훅 패턴) → `fe-react-patterns`
- 접근성 (ARIA, 키보드, 시맨틱 HTML) → `fe-a11y`
- 성능 최적화 → `fe-react-performance`
- 코드 리뷰 절차 → `fe-code-review`
