---
name: fe-react-patterns
description: "React component architecture and composition patterns. Use this skill when designing React component APIs, building compound components, deciding component structure, managing component state, solving props drilling, or migrating to React 19. Covers composition over configuration, compound components, explicit variants, state management patterns, and React 19 API changes. Always consult this skill when creating or restructuring any React component. For performance optimization, use fe-react-performance instead. This skill extends vercel-composition-patterns with Korean instructions and additional patterns from the team's code quality guidelines. Triggers on: component architecture, compound components, composition pattern, props drilling, state management, Context API design, React 19, forwardRef removal, 컴포넌트 설계, 합성 패턴, 상태관리 패턴, 컴포넌트 만들기, 컴포넌트 구조, 컴포넌트 리팩토링, Context 만들기, props가 너무 많아, boolean prop, 컴포넌트 나누기, 컴포넌트 분리, 재사용 가능한 컴포넌트, 커스텀 훅 패턴."
---

# React 컴포넌트 아키텍처 & 합성 패턴

## 핵심 철학: Composition over Configuration (설정보다 조합)

React 컴포넌트를 설계할 때 가장 중요한 원칙은 **"설정(Configuration)보다 조합(Composition)"** 이에요.

- ❌ Boolean props를 추가해서 컴포넌트 동작을 커스터마이징하지 마세요
- ✅ 작은 컴포넌트를 조합해서 필요한 UI를 만드세요

Boolean prop 하나가 추가될 때마다 가능한 상태 조합은 2배로 늘어나요. 이렇게 늘어난 조합은 유지보수를 어렵게 만들고, 불가능한 상태(impossible states)를 만들어요.

```tsx
// ❌ 나쁜 예: boolean props로 커스터마이징
<Composer isThread isEditing={false} showAttachments showFormatting={false} />

// ✅ 좋은 예: 명시적 variant로 조합
<ThreadComposer channelId="abc" />
```

## 패턴 개요

### 1. 컴포넌트 아키텍처

| 패턴 | 설명 | 우선순위 |
|------|------|----------|
| Boolean Props 지양 | boolean props 대신 composition 사용 | 🔴 CRITICAL |
| Compound Components | 공유 컨텍스트로 관련 컴포넌트 그룹화 | 🔴 HIGH |
| Explicit Variants | boolean 모드 대신 명시적 variant 컴포넌트 생성 | 🟡 MEDIUM |
| 컴포넌트 분리 전략 | 동시에 실행되지 않는 코드를 별도 컴포넌트로 분리 | 🟡 MEDIUM |

### 2. 상태 관리 패턴

| 패턴 | 설명 | 우선순위 |
|------|------|----------|
| State Lifting | Provider 컴포넌트로 상태를 끌어올려 형제 컴포넌트 간 공유 | 🔴 HIGH |
| Implementation Decoupling | Provider만 상태 구현을 알고, UI는 인터페이스만 소비 | 🟡 MEDIUM |
| Context Interface | state/actions/meta 제네릭 인터페이스로 의존성 주입 | 🔴 HIGH |

### 3. 합성 패턴

| 패턴 | 설명 | 우선순위 |
|------|------|----------|
| Children over Render Props | renderX props 대신 children으로 조합 | 🟡 MEDIUM |
| Props Drilling → Composition | Composition으로 Props Drilling 해결 | 🟡 MEDIUM |
| 구현 상세 추상화 | HOC/Wrapper로 관심사 분리 | 🟡 MEDIUM |

### 4. React 19 마이그레이션

| 변경사항 | 설명 |
|----------|------|
| forwardRef 제거 | ref를 일반 prop으로 직접 전달 |
| use() 도입 | useContext() 대신 use() 사용, 조건부 호출 가능 |

## 레퍼런스 가이드

각 패턴의 상세 설명과 Before/After 코드 예제는 `references/` 디렉토리에 있어요.

| 파일 | 내용 | 언제 참고하나요? |
|------|------|-----------------|
| `references/composition.md` | Compound Components, Explicit Variants, Boolean Props 지양, children vs render props, Props Drilling 해결, 컴포넌트 분리 전략 | 컴포넌트 API 설계, 리팩토링, Props Drilling 해결 시 |
| `references/state-management.md` | State Lifting, Implementation Decoupling, Context Interface 패턴 | Context API 설계, 상태 공유 구조 설계 시 |
| `references/react19.md` | forwardRef 제거, use() 사용법, 마이그레이션 가이드 | React 19 마이그레이션, 새 프로젝트 셋업 시 |

## 기존 스킬과의 관계

이 스킬은 `vercel-composition-patterns` 스킬의 내용을 한국어로 정리하고, 팀의 코드 품질 가이드라인 예제를 추가한 확장 버전이에요. 두 스킬이 동시에 있을 경우 이 스킬을 우선 참고하세요.

## 범위 안내

- **성능 최적화** (메모이제이션, 번들 사이즈, 렌더링 최적화) → `fe-react-performance` 스킬 참고
- **일반 코드 컨벤션** (네이밍, 파일 구조, 가독성 원칙) → `fe-code-conventions` 스킬 참고
- **접근성** (ARIA, 키보드 네비게이션, 시맨틱 HTML) → `fe-a11y` 스킬 참고

## 이 스킬을 사용하지 않는 경우

- 성능 최적화 (memo, useMemo, 번들 등) → `fe-react-performance`를 참고하세요
- 일반 코드 컨벤션 (네이밍, 가독성, 파일 구조) → `fe-code-conventions`를 참고하세요
- 접근성 패턴 → `fe-a11y`를 참고하세요
- React가 아닌 프레임워크 코드에는 이 스킬이 적용되지 않아요
