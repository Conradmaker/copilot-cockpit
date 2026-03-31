---
name: fe-zustand
description: "Zustand v5 client state management patterns for React applications. Use this skill when building or refactoring Zustand stores, choosing between create and createStore, fixing re-renders from broad subscriptions, composing persist/devtools/immer middleware, structuring slice-based stores, wiring scoped vanilla stores through context, or handling hydration issues in Next.js. Always consult this skill for Zustand work even if the user only asks to add a store, persist UI state, fix a Zustand bug, or decide whether state belongs in Zustand or TanStack Query. For component architecture use fe-react-patterns. For rendering optimization beyond store selection use fe-react-performance. For server-state caching and mutations use fe-tanstack-query. Triggers on: Zustand, zustand, createStore, persist middleware, devtools, slices pattern, client state, global store, hydration mismatch, Next.js Zustand, 전역 상태, 스토어 설계, 하이드레이션."
disable-model-invocation: false
user-invocable: false
---

# Zustand 상태 관리 패턴

## 목표

Zustand를 React의 client state 도구로 정확하게 사용한다. store를 아무 데나 늘리지 않고, broad subscription과 unstable selector output으로 생기는 re-render를 줄이고, middleware와 persistence를 현재 v5 기준으로 조합하고, Next.js와 SSR 환경에서 hydration mismatch를 피하는 것이 핵심이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 구현에 들어가기 전에는 아래 reference 문서를 직접 읽고 현재 작업이 일반 store 설계, middleware와 persistence, Next.js와 SSR 대응, integration과 anti-pattern 중 어디에 속하는지 먼저 좁힌 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 패턴

### 1. Zustand 경계를 먼저 정한다

Zustand는 client-only state에 집중할 때 가장 강하다. UI 토글, wizard progress, 선택 상태, preference, locally coordinated draft state처럼 서버와 권위 source를 공유하지 않는 데이터를 우선 담는다. 서버에서 가져온 entity 목록, pagination, mutation lifecycle까지 전부 넣기 시작하면 cache invalidation과 stale data 문제가 커진다.

- Zustand는 client state와 UI orchestration에 쓴다
- 서버 데이터 fetch와 cache는 TanStack Query를 우선 검토한다
- 단일 form 로컬 상태는 React state나 form library가 더 단순한지 먼저 본다
- 여러 화면이나 형제 컴포넌트가 같은 client state를 읽을 때만 전역 store를 검토한다

#### 빠른 판단 기준

- 데이터의 source of truth가 서버면 TanStack Query 쪽인지 먼저 본다
- 상태가 한 컴포넌트 안에서만 쓰이면 store보다 local state가 낫다
- 화면 간 공유되는 UI 상태인가에 답이 Yes일 때 Zustand 후보로 올린다

→ 상세: references/core-patterns.md

### 2. store는 작게 두고 selector를 기본값으로 둔다

Zustand에서 가장 흔한 성능 문제는 store가 아니라 구독 방식이다. useStore로 전체 store를 읽거나 selector가 매번 새 객체와 배열을 반환하면 v5에서 불필요한 re-render나 update depth 문제로 이어질 수 있다.

- hook store는 `create<T>()(...)` 패턴을 기본값으로 둔다
- vanilla store는 `createStore<T>()(...)`로 만들고 `useStore` 또는 `useStoreWithEqualityFn`으로 읽는다
- 한 값씩 selector로 읽는 방식을 기본으로 한다
- 여러 값을 같이 읽을 때는 `useShallow`로 stable output을 만든다
- custom equality가 정말 필요할 때만 `createWithEqualityFn` 또는 `useStoreWithEqualityFn`을 쓴다
- `shallow` comparator 자체가 필요할 때와 `useShallow`가 필요한 때를 구분한다

#### 빠른 판단 기준

- `const store = useAppStore()`가 보이면 selector 분리 여부를 본다
- selector가 배열이나 객체를 즉석에서 반환하면 stable output인지 확인한다
- 여러 값을 한 번에 뽑는다면 `useShallow`가 더 적합한지 먼저 검토한다

→ 상세: references/core-patterns.md

### 3. store 구조는 slice와 scoped vanilla store 중심으로 설계한다

공용 app state가 커질수록 하나의 거대한 initializer에 모든 도메인을 몰아넣는 방식은 빠르게 유지보수성을 잃는다. 반대로 Next.js나 탭별 독립 상태처럼 인스턴스가 여러 개 필요한 경우에는 hook store보다 scoped vanilla store가 더 자연스럽다.

- 큰 공용 store는 typed slices로 쪼개고 combined store에서만 조합한다
- slice 안에서 다른 slice 상태가 필요하면 `get()`로 접근한다
- middleware는 slice 내부가 아니라 combined store 레벨에서 적용한다
- 요청 단위, route 단위, provider 단위로 store 인스턴스가 달라야 하면 `createStore` + context를 사용한다

#### 빠른 판단 기준

- auth, cart, ui concern이 한 파일에서 뒤엉키면 slices 후보로 본다
- 탭별 독립 상태나 provider별 분리가 필요하면 scoped vanilla store 쪽이 맞다
- slice 파일에서 직접 middleware를 두 번 감싸고 있으면 구조를 다시 본다

→ 상세: references/core-patterns.md

### 4. middleware와 persistence는 조합 규칙을 분명히 둔다

Zustand v5에서는 middleware의 실행 순서뿐 아니라 TypeScript mutator inference도 중요하다. 특히 upstream 가이드는 `devtools`를 가능한 바깥쪽에 두라고 권장한다. persistence는 정말 durable해야 하는 값만 저장하고, schema 변경 가능성이 있으면 `version`과 `migrate`를 함께 두는 편이 안전하다.

- 여러 middleware를 섞을 때는 `devtools(...)`를 가능한 마지막 wrapper로 둔다
- nested update가 자주 나올 때만 `immer`를 쓴다
- durable client state만 `persist`로 저장하고 `partialize`로 범위를 줄인다
- persisted schema가 바뀌면 `version`과 `migrate`를 같이 둔다
- SSR이 있는 환경에서는 `skipHydration`과 manual `rehydrate()`를 검토한다
- action naming과 devtools options를 명시해 timeline을 읽기 쉽게 만든다
- primitive, array, reset처럼 전체 상태 replacement가 필요한 구간에서는 `setState(..., true)` semantics를 분명히 이해하고 사용한다

#### 빠른 판단 기준

- `persist`가 붙은 store에 `partialize`가 없으면 저장 범위가 과한지 본다
- persisted data shape를 바꿨는데 `version`과 `migrate`가 없으면 보완한다
- TypeScript mutator inference가 어색하면 wrapper 순서부터 점검한다
- `replace=true`가 필요한 reset이나 primitive store인데 merge처럼 쓰고 있으면 semantics를 다시 본다

→ 상세: references/middleware-and-persistence.md

### 5. Next.js와 SSR에서는 per-request와 hydration 경계를 지킨다

Next.js에서 module-level global store를 서버와 공유하면 요청 간 상태 오염과 hydration mismatch가 생길 수 있다. React Server Components는 Zustand store를 읽고 쓰는 장소가 아니다. stable한 원칙은 per-request or per-provider store, client boundary 안에서의 사용, 그리고 서버와 클라이언트가 같은 초기 상태를 보게 만드는 것이다.

- Next.js 서버 환경에서는 전역 hook store를 source of truth처럼 공유하지 않는다
- store factory를 만들고 client provider에서 인스턴스를 생성한다
- RSC에서는 store를 읽거나 쓰지 않는다
- persisted client state는 hydration mismatch를 유발할 수 있으므로 지연된 read나 manual rehydrate를 검토한다
- experimental API는 기본 권장으로 두지 않는다

#### 빠른 판단 기준

- App Router에서 module-scope store를 여러 요청이 공유하면 구조를 바꾼다
- 서버 렌더와 클라이언트 첫 렌더 값이 다르면 hydration 전략을 다시 본다
- client component 밖에서 store hook을 쓰고 있으면 경계를 점검한다

→ 상세: references/nextjs-and-ssr.md

### 6. testing과 integration은 anti-pattern을 같이 본다

Zustand store는 테스트 가능성이 좋아야 한다. 초기 상태와 reset 경로가 없으면 테스트가 어렵고, broad integration은 점점 event bus처럼 흐르기 쉽다. 특히 derived state, server state, secret persistence, full-store destructuring은 반복적으로 문제를 만든다.

- initial state factory나 reset path를 준비한다
- store logic은 UI와 분리해 테스트 가능하게 둔다
- TanStack Query와의 역할을 분리한다
- derived state는 저장하지 말고 selector에서 계산한다
- secret과 token은 persistence 대상으로 두지 않는다
- full-store destructuring과 per-slice middleware 적용을 피한다

testing 관점에서는 두 문서를 나눠 본다. store 생성, reset, fresh instance 같은 기본 테스트 뼈대는 `core-patterns`에서 먼저 잡고, TanStack Query 경계와 review용 anti-pattern 점검은 `integration-and-anti-patterns`에서 마무리한다.

#### 빠른 판단 기준

- 테스트에서 이전 상태가 새 테스트에 새면 reset 전략이 필요하다
- users, projects 같은 서버 entity를 store가 직접 fetch하고 캐시하고 있으면 경계를 다시 본다
- total, isComplete 같은 파생값을 state로 저장하고 있으면 selector 계산으로 내릴 수 있는지 확인한다
- 테스트 셋업 자체가 막히면 `core-patterns`부터, 구조 리뷰나 경계 판단이 애매하면 `integration-and-anti-patterns`부터 읽는다

→ 상세: references/integration-and-anti-patterns.md

---

## references/ 가이드

아래 문서는 실제 구현 전에 읽어야 하는 작업 가이드다. 이 본문은 방향을 잡는 용도고, 세부 예시와 버전 민감한 주의사항은 references에서 확인한다.

| 파일 | 언제 읽는가 |
| --- | --- |
| references/core-patterns.md | `create`, `createStore`, selectors, `useShallow`, `createWithEqualityFn`, slices, scoped vanilla store, 기본 testing/reset 패턴처럼 store 자체의 뼈대를 잡을 때 |
| references/middleware-and-persistence.md | `devtools`, `persist`, `immer`, `subscribeWithSelector`, storage, migration, hydration lifecycle, `replace` semantics처럼 middleware와 persistence의 동작 규칙을 설계할 때 |
| references/nextjs-and-ssr.md | Next.js App Router, client boundary, per-request store, hydration mismatch 대응이 필요할 때 |
| references/integration-and-anti-patterns.md | TanStack Query 경계, anti-pattern, forms, secret persistence, review checklist, 그리고 integration 관점의 testing 포인트를 점검할 때 |

### 추천 로드 순서

- 새 store 설계: `core-patterns -> middleware-and-persistence`
- Next.js에서 Zustand 도입: `nextjs-and-ssr -> core-patterns -> middleware-and-persistence`
- re-render나 hydration bug 수정: `core-patterns -> nextjs-and-ssr -> integration-and-anti-patterns`
- 구조 리팩토링과 code review: `core-patterns -> integration-and-anti-patterns`

---

## 범위

- React 컴포넌트 구조와 상태 소유권 설계 → `fe-react-patterns`
- broad rendering, waterfalls, bundle cost 최적화 → `fe-react-performance`
- 서버 상태 캐시, mutation lifecycle, invalidation → `fe-tanstack-query`
- reusable design-system primitive 설계 → `fe-ui-element-components`

이 스킬은 Zustand를 어디에 쓰고 어떻게 구조화할지에 집중한다. generic React architecture, server-state orchestration, component API 설계까지 한 스킬에 넣지 않는다.