---
name: fe-react-performance
description: "React and Next.js performance optimization patterns. Use this skill when optimizing React application performance, reducing bundle size, eliminating render waterfalls, improving server-side performance, optimizing re-renders, or when the user asks about slow rendering, large bundles, unnecessary re-renders, or data fetching optimization. Always consult this skill when you notice or suspect performance issues in React code. For component architecture patterns, use fe-react-patterns instead. This skill extends vercel-react-best-practices with Korean instructions organized by impact priority. Triggers on: performance optimization, bundle size, re-render, waterfall, lazy loading, code splitting, memo, useMemo, useCallback, Suspense, server components, 성능 최적화, 번들, 리렌더링, 느려, 느린 페이지, 초기 로딩, SSR 최적화, RSC, 서버 컴포넌트, Next.js 성능, 코드 스플리팅, 메모이제이션, 불필요한 렌더링, 하이드레이션, 앱이 무거워, 로딩이 오래 걸려."
---

# React/Next.js 성능 최적화 가이드

## 목표

영향도가 높은 순서대로 최적화를 적용한다. 낮은 우선순위부터 시작하면 노력 대비 효과가 적다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 성능을 최적화할 때는 아래 reference 문서를 직접 읽고 Before/After 예시와 세부 규칙을 확인한 뒤 적용한다.

> 범위 구분: 컴포넌트 설계/아키텍처 → `fe-react-patterns`스킬 / 일반 코드 품질 → `fe-code-conventions`스킬 / 접근성 → `fe-a11y`스킬 / 성능 최적화 → `fe-react-performance`스킬

---

## 성능 최적화 우선순위

### 1순위 — 비동기 워터폴 제거 (2~10배 성능 개선)

독립적인 비동기 요청들이 직렬로 실행되면 총 지연시간이 합산되기 때문에, 병렬 실행으로 전환하면 가장 큰 성능 개선을 얻는다.

- `Promise.all()`로 독립적인 비동기 작업 병렬 실행
  `await fetchUser()` → `await fetchPosts()` → `await fetchComments()`처럼 순차 실행하면 3번의 라운드트립이 발생한다. `Promise.all([fetchUser(), fetchPosts(), fetchComments()])`로 바꾸면 1번으로 줄어든다.
- 일부만 의존성이 있는 경우 Promise 체이닝으로 최대한 병렬화
  `fetchProfile(user.id)`가 `fetchUser()`에 의존하더라도, `fetchConfig()`는 독립적이다. `userPromise.then(u => fetchProfile(u.id))`를 미리 생성하고 `Promise.all`에 함께 넣으면 config와 profile이 병렬로 실행된다.
- Suspense 경계를 전략적으로 배치하여 스트리밍
  전체 페이지를 데이터 로딩에 블로킹하지 말고, 데이터가 필요한 컴포넌트만 `<Suspense>`로 감싸서 나머지 UI를 먼저 보여준다. 단, 레이아웃 결정에 필요한 핵심 데이터나 SEO에 중요한 콘텐츠에는 Suspense를 피한다.
- 불필요한 `await`는 실제 사용 분기로 이동
  `skipProcessing`일 때도 불필요하게 데이터를 fetch하는 대신, 조건 검사를 먼저 하고 필요할 때만 await한다.

실제 적용 전에는 [references/async-waterfall.md](references/async-waterfall.md)를 직접 읽고, Promise 체이닝·Suspense 배치·API 라우트 병렬화의 코드 예시를 확인한다.

→ 상세한 레퍼런스: [references/async-waterfall.md](references/async-waterfall.md)

### 2순위 — 번들 최적화 (TTI, LCP 직접 영향)

barrel 파일의 re-export는 트리 셰이킹을 방해해 사용하지 않는 모듈까지 번들에 포함시키기 때문에 200~800ms 비용이 발생하기 때문에 최적화시 개선을 얻는다.

- barrel 파일 re-export 대신 직접 import (또는 `optimizePackageImports`)
  `import { Check } from 'lucide-react'`는 1,583개 모듈을 로드한다. `import Check from 'lucide-react/dist/esm/icons/check'`로 바꾸면 필요한 것만 로드된다. Next.js 13.5+에서는 `optimizePackageImports` 설정으로 자동 변환할 수 있다.
  흔히 영향받는 라이브러리: `lucide-react`, `@mui/material`, `@tabler/icons-react`, `react-icons`, `lodash`, `date-fns`, `rxjs`
- `next/dynamic`으로 무거운 컴포넌트 지연 로드
  Monaco Editor(~300KB) 같은 무거운 컴포넌트는 `dynamic(() => import('./monaco-editor'), { ssr: false })`로 필요 시 로드한다.
- 분석/로깅 등 비핵심 서드파티 하이드레이션 후 로드
  Analytics, 에러 트래킹 같은 비핵심 모듈은 `dynamic`으로 `ssr: false` 처리하여 사용자 인터랙션을 차단하지 않게 한다.
- 중요 리소스는 hover/focus 시점에 preload
  에디터 버튼에 `onMouseEnter`/`onFocus`에서 `void import('./monaco-editor')`를 호출하면 클릭 전에 미리 로드돼 체감 지연이 줄어든다.

실제 적용 전에는 [references/bundle.md](references/bundle.md)를 직접 읽고, barrel import·dynamic import·preload의 코드 예시를 확인한다.

→ 상세한 레퍼런스: [references/bundle.md](references/bundle.md)

### 3순위 — 서버사이드 성능

서버 응답 시간과 서버 렌더링 최적화는 TTFB와 LCP에 직접적인 영향을 미친다.

- `React.cache()`로 요청 내 중복 제거 (원시 타입 인자 사용)
  인라인 객체를 인자로 넘기면 매번 새 참조가 생성되어 캐시 미스가 발생한다. `getUser({ uid: 1 })` 대신 `getUser(1)`처럼 원시 타입을 사용해야 캐시가 동작한다.
- LRU 캐시로 요청 간 데이터 캐싱
  `React.cache()`는 단일 요청 내에서만 동작한다. 여러 요청에 걸쳐 캐싱하려면 `lru-cache` 등을 사용한다.
- 서버 액션에 인증/권한 검증 추가 (보안 + 비용 절감)
  `"use server"` 함수는 공개 엔드포인트로 노출된다. 반드시 각 서버 액션 내부에서 인증/권한을 검증해야 한다. 미들웨어나 레이아웃 가드에만 의존하면 안 된다.
- RSC 경계에서 직렬화할 데이터 최소화
  서버 컴포넌트에서 클라이언트 컴포넌트로 50개 필드의 전체 객체를 넘기지 말고, 실제 사용하는 필드만 전달하여 직렬화 비용을 줄인다.
- 컴포넌트 합성으로 서버 페칭 병렬화
  RSC는 트리 내에서 순차 실행된다. `Header`와 `Sidebar`를 각각 독립 async 컴포넌트로 분리하면 데이터 페칭이 병렬화된다.
- `after()`로 로깅/분석 등 비차단 처리

실제 적용 전에는 [references/server.md](references/server.md)를 직접 읽고, cache() 주의사항·서버 액션 인증·RSC 직렬화의 코드 예시를 확인한다.

→ 상세 레퍼런스: [references/server.md](references/server.md)

### 4순위 - 클라이언트 데이터 페칭

- SWR이나 tanstack-query로 요청 중복 제거 및 캐싱
  `useEffect` + `fetch`로 직접 호출하면 컴포넌트 인스턴스마다 개별 요청이 발생한다. SWR을 사용하면 같은 키의 요청이 자동으로 중복 제거되고 캐싱된다.
- scroll/touch 이벤트에 `{ passive: true }` 적용 — 브라우저 스크롤 최적화에 필요
  `passive: true`를 설정하면 브라우저가 `preventDefault()` 호출 여부를 기다리지 않아 즉각적인 스크롤이 가능해진다. 단, 커스텀 스와이프 제스처처럼 `preventDefault()`가 필요한 경우에는 사용하지 않는다.
- 글로벌 이벤트 리스너 중복 등록 방지
  N개 인스턴스가 각각 `addEventListener`를 호출하면 N개 리스너가 등록된다. `useSWRSubscription`이나 공유 Map 패턴으로 1개 리스너를 공유한다.

실제 적용 전에는 [references/client.md](references/client.md)를 직접 읽고, SWR 패턴·passive 이벤트·localStorage 스키마 버전 관리의 코드 예시를 확인한다.

→ 상세 레퍼런스: [references/client.md](references/client.md)

### 5순위 — 리렌더 최적화

- 단순 표현식은 `useMemo` 없이 렌더 중 계산
  `useMemo(() => a || b, [a, b])` 같은 간단한 boolean 계산은 오히려 `useMemo`의 호출·의존성 비교 비용이 더 크다. 결과가 원시 타입인 간단한 표현식은 그냥 계산한다.
- 비용이 큰 작업만 `memo()` 컴포넌트로 분리
  비싼 연산을 메모이즈된 컴포넌트로 추출하면, 로딩 상태 등에서 조기 반환이 가능해져 불필요한 연산을 건너뛸 수 있다.
- 비원시 타입 기본값은 상수로 호이스팅
  `memo()` 컴포넌트의 `onClick = () => {}` 같은 기본값은 매 렌더마다 새 인스턴스가 생성되어 메모이제이션이 깨진다. `const NOOP = () => {}`를 모듈 스코프에 두고 기본값으로 쓴다.
- `setState(prev => ...)` 함수형 업데이트로 안정 콜백
  `setItems([...items, ...newItems])`는 items 의존성 때문에 매번 콜백이 재생성되거나 stale closure 버그가 발생한다. `setItems(curr => [...curr, ...newItems])`로 바꾸면 의존성 없이 안정적이다.
- 파생 상태는 렌더 중 계산 (Effect 사용 금지)
  `fullName`을 `useEffect`로 `firstName + lastName`에서 동기화하면 불필요한 리렌더와 상태 동기화 문제가 생긴다. 렌더링 중 `const fullName = firstName + ' ' + lastName`으로 직접 계산한다.

실제 적용 전에는 [references/rerender.md](references/rerender.md)를 직접 읽고, 파생 boolean 구독·함수형 setState·useState 지연 초기화 등의 코드 예시를 확인한다.

→ 상세 레퍼런스: [references/rerender.md](references/rerender.md)

### 6순위 — 렌더링 성능

- 조건부 렌더링에 `&&` 대신 삼항 연산자 사용 — falsy 값이 렌더되는 버그 방지
  `count && <Badge />` 에서 count가 0이면 `"0"`이 화면에 렌더된다. `count > 0 ? <Badge /> : null`로 명시적으로 처리한다.
- `content-visibility: auto`로 오프스크린 렌더링 지연
  1000개 메시지 리스트에서 화면 밖 ~990개 항목의 레이아웃/페인트를 건너뛰어 초기 렌더가 10배 빨라질 수 있다. `contain-intrinsic-size`로 예상 크기를 지정한다.
- 정적 JSX는 컴포넌트 외부로 호이스팅
  매 렌더마다 변하지 않는 큰 정적 JSX(특히 SVG)를 컴포넌트 밖 상수로 추출하면 재생성 비용이 사라진다.
- 애니메이션은 `transform`과 `opacity` 중심으로 구성하고 `transition: all`은 피한다
  자주 발생하는 인터랙션일수록 레이아웃 재계산이 큰 속성을 피해야 한다. 사용자의 모션 축소 선호가 있으면 `prefers-reduced-motion`으로 애니메이션을 줄이거나 끈다.
- 레이아웃 읽기와 쓰기를 섞지 않는다
  `getBoundingClientRect()`, `offsetHeight` 같은 레이아웃 읽기와 `style` 변경을 번갈아 호출하면 강제 리플로우가 발생한다. 읽기를 먼저 모으고, 쓰기는 뒤에서 한 번에 적용한다.
- 이미지 크기와 로딩 우선순위를 명시한다
  `<img>`에는 `width`/`height`를 제공해 CLS를 줄이고, 아래 폴드 이미지는 `loading="lazy"`, 핵심 이미지는 `fetchPriority="high"` 또는 프레임워크 우선 로드 옵션을 사용한다.

실제 적용 전에는 [references/rendering.md](references/rendering.md)를 직접 읽고, 하이드레이션 불일치 방지·SVG 애니메이션 래퍼·reduced motion·레이아웃 스래싱 방지·이미지 로딩 전략의 코드 예시를 확인한다.

→ 상세: [references/rendering.md](references/rendering.md)

### 7순위 — JS 마이크로 최적화

일반 코드에서는 가독성 저하 대비 이점이 작다. 성능 측정 후 핫 패스라고 확인된 코드에서만 적용한다.

- `Map`/`Set`으로 O(1) 조회
  1000 orders × 1000 users에서 `.find()`는 100만 번 순회하지만, `new Map(users.map(u => [u.id, u]))`로 인덱스를 만들면 2000번 연산으로 줄어든다.
- 조기 반환으로 불필요한 연산 회피
  에러가 발견된 후에도 모든 항목을 처리하는 대신, 첫 에러에서 즉시 반환하면 불필요한 순회를 건너뛴다.
- 반복 함수 호출 결과를 Map으로 캐싱
  같은 입력으로 `slugify()`를 100번 호출하는 대신 모듈 레벨 Map에 캐싱한다.
- RegExp를 루프 밖으로 호이스팅
  렌더 안에서 `new RegExp()`를 생성하면 매 렌더마다 새 정규식이 만들어진다. 모듈 스코프로 호이스팅하거나 `useMemo`로 메모이즈한다.
- 레이아웃 스래싱 방지 — 스타일 쓰기와 레이아웃 읽기를 번갈아 하지 않는다
  `element.style.width = ...` → `element.offsetWidth` → `element.style.height = ...` 같은 인터리빙은 동기 리플로우를 강제한다. 쓰기를 모아서 하고 읽기는 한 번에 한다. 가능하면 CSS 클래스를 사용한다.

실제 적용 전에는 [references/js-optimization.md](references/js-optimization.md)를 직접 읽고, Set/Map·레이아웃 스래싱 방지·toSorted() 등의 코드 예시를 확인한다.

→ 상세 레퍼런스: [references/js-optimization.md](references/js-optimization.md)

---

## 엣지케이스: React Compiler

프로젝트에 React Compiler가 활성화되어 있으면 `memo()`, `useMemo()`, `useCallback()` 수동 메모이제이션과 정적 JSX 호이스팅이 자동 처리된다. 비동기 워터폴, 번들 최적화, 서버 패턴은 여전히 수동으로 적용해야 한다.

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 최적화를 적용하기 전 반드시 확인해야 하는 구현 가이드다. 본문에서 방향을 잡고, 최적화를 시작하기 전에 해당 문서를 직접 읽는다.

각 최적화 패턴에 대한 상세 설명과 코드 예시는 `references/` 디렉토리의 개별 파일에 있다.

| 파일                 | 내용                                                                     |
| -------------------- | ------------------------------------------------------------------------ |
| `async-waterfall.md` | 비동기 워터폴 제거 패턴                                                  |
| `bundle.md`          | 번들 최적화 패턴                                                         |
| `server.md`          | 서버사이드 성능 패턴                                                     |
| `client.md`          | 클라이언트 데이터 페칭 패턴                                              |
| `rerender.md`        | 리렌더 최적화 패턴                                                       |
| `rendering.md`       | 렌더링 성능 패턴, reduced motion, 레이아웃 스래싱 방지, 이미지 로딩 전략 |
| `js-optimization.md` | JS 마이크로 최적화 패턴                                                  |

---

## 범위

- 컴포넌트 설계/아키텍처 → `fe-react-patterns`
- 일반 코드 컨벤션 (네이밍, 가독성) → `fe-code-conventions`
- 접근성 → `fe-a11y`
