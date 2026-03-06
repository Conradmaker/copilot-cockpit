---
name: fe-code-conventions
description: "Frontend clean code conventions and code quality principles. Use this skill when writing new frontend code, refactoring existing code, reviewing code quality, or when the user asks about naming conventions, code readability, file/directory structure, component organization, or coupling/cohesion decisions. This covers language-agnostic frontend principles (not React-specific patterns - see fe-react-patterns for those). Always consult this skill during any frontend code writing or refactoring task, even if the user doesn't explicitly ask about code quality. Triggers on: code refactoring, clean code, naming, readability, file structure, code organization, coupling, cohesion, code conventions, 코드 컨벤션, 클린코드, 리팩토링, 변수명, 함수명, 폴더 구조, 디렉토리 구조, 코드 정리, 코드 개선, 좋은 코드, 매직넘버, 하드코딩, 조건문 정리, 코드 구조, 코드 품질, 읽기 쉬운 코드, 유지보수, 코드가 복잡해, 함수가 너무 길어."
---

# 프론트엔드 코드 컨벤션

## 핵심 철학

> **"변경하기 쉬운 코드"** = 좋은 프론트엔드 코드

새로운 요구사항이 생겼을 때, 기존 코드를 수정하고 배포하기 수월한 코드가 좋은 코드예요.
코드가 변경하기 쉬운지는 **4가지 원칙**으로 판단할 수 있어요.

---

## 4대 원칙 요약

### 1. 가독성 (Readability)

> 코드가 읽기 쉬운 정도. 한 번에 고려해야 하는 맥락이 적고, 위에서 아래로 자연스럽게 읽히는 코드.

**핵심 패턴:**
- 매직 넘버에 이름 붙이기 → `const ANIMATION_DELAY_MS = 300;`
- 복잡한 조건식에 의미 있는 이름 부여 → `const isSameCategory = ...`
- 동시에 실행되지 않는 코드는 별도 컴포넌트로 분리

📖 상세 가이드: [references/readability.md](references/readability.md)

### 2. 예측 가능성 (Predictability)

> 함수나 컴포넌트의 이름과 파라미터, 반환 값만 보고도 동작을 예측할 수 있는 정도.

**핵심 패턴:**
- 라이브러리 함수명과 겹치지 않는 명확한 이름 사용 → `httpService.getWithAuth()`
- 같은 종류의 함수는 반환 타입을 통일 → API Hook은 항상 `Query` 객체 반환

📖 상세 가이드: [references/predictability.md](references/predictability.md)

### 3. 응집도 (Cohesion)

> 수정되어야 할 코드가 항상 같이 수정되는지의 정도. 함께 변경되는 코드는 함께 위치해야 함.

**핵심 패턴:**
- 함께 수정되는 파일을 같은 디렉토리에 배치 (도메인별 코로케이션)
- 매직 넘버를 상수로 추출하여 관련 코드와 함께 관리

📖 상세 가이드: [references/cohesion.md](references/cohesion.md)

### 4. 결합도 (Coupling)

> 코드를 수정했을 때의 영향 범위. 영향 범위가 좁고 예측 가능한 코드가 좋은 코드.

**핵심 패턴:**
- 하나의 Hook/함수에 하나의 책임만 부여
- 불필요한 공통화보다 중복 코드를 허용하여 영향 범위 축소

📖 상세 가이드: [references/coupling.md](references/coupling.md)

---

## 원칙 간 트레이드오프

이 4가지 원칙을 모두 동시에 완벽하게 충족하기는 어려워요. 상황에 따라 우선순위를 판단해야 해요.

### 가독성 vs 응집도
- 응집도를 높이기 위해 공통화/추상화하면, 코드가 한 단계 더 추상화되어 **가독성이 떨어질 수 있어요**.
- 함께 수정하지 않으면 오류가 발생할 위험이 높은 경우 → **응집도 우선**
- 위험성이 낮은 경우 → **가독성 우선**, 코드 중복 허용

### 응집도 vs 결합도
- 중복 코드를 허용하면 영향 범위가 줄어 **결합도가 낮아져요**.
- 하지만 한쪽을 수정할 때 다른 쪽을 놓칠 수 있어 **응집도가 떨어져요**.
- 동작이 동일하고 앞으로도 동일할 예정이라면 → **응집도를 위해 공통화**
- 페이지마다 동작이 달라질 여지가 있다면 → **결합도를 위해 중복 허용**

### 판단 기준
> 현재 직면한 상황을 바탕으로, 장기적으로 코드가 수정하기 쉽게 하기 위해 어떤 가치를 우선해야 하는지 깊이 고민하세요.

---

## References 가이드

| 파일 | 내용 | 언제 참고하나요? |
|------|------|-----------------|
| [readability.md](references/readability.md) | 가독성 원칙 + 8개 예제 | 코드가 읽기 어렵거나, 네이밍/조건문/함수 분리를 고민할 때 |
| [predictability.md](references/predictability.md) | 예측 가능성 원칙 + 3개 예제 | 함수 이름/반환 타입/숨겨진 로직에 대해 고민할 때 |
| [cohesion.md](references/cohesion.md) | 응집도 원칙 + 3개 예제 | 디렉토리 구조, 매직 넘버, 폼 설계를 고민할 때 |
| [coupling.md](references/coupling.md) | 결합도 원칙 + 3개 예제 | Hook 책임 분리, 공통화 여부, Props Drilling을 고민할 때 |

---

## 스킬 범위

- ✅ **이 스킬이 다루는 것**: 언어/프레임워크에 무관한 프론트엔드 코드 품질 원칙 (네이밍, 가독성, 파일 구조, 결합도/응집도)
- ❌ **React 전용 패턴** (컴포넌트 설계, 상태 관리, 훅 패턴 등) → `fe-react-patterns` 참고
- ❌ **접근성** (ARIA, 키보드 내비게이션, 스크린 리더 등) → `fe-a11y` 참고

## 이 스킬을 사용하지 않는 경우

- React 전용 컴포넌트 설계 패턴 → `fe-react-patterns`를 참고하세요
- 성능 최적화 → `fe-react-performance`를 참고하세요
- 접근성 패턴 → `fe-a11y`를 참고하세요
- 코드 리뷰 절차 → `fe-code-review`를 참고하세요
- 백엔드/서버 로직, 순수 데이터 처리에는 이 스킬이 적용되지 않아요
