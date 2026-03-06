---
name: fe-react-performance
description: "React and Next.js performance optimization patterns. Use this skill when optimizing React application performance, reducing bundle size, eliminating render waterfalls, improving server-side performance, optimizing re-renders, or when the user asks about slow rendering, large bundles, unnecessary re-renders, or data fetching optimization. Always consult this skill when you notice or suspect performance issues in React code. For component architecture patterns, use fe-react-patterns instead. This skill extends vercel-react-best-practices with Korean instructions organized by impact priority. Triggers on: performance optimization, bundle size, re-render, waterfall, lazy loading, code splitting, memo, useMemo, useCallback, Suspense, server components, 성능 최적화, 번들, 리렌더링, 느려, 느린 페이지, 초기 로딩, SSR 최적화, RSC, 서버 컴포넌트, Next.js 성능, 코드 스플리팅, 메모이제이션, 불필요한 렌더링, 하이드레이션, 앱이 무거워, 로딩이 오래 걸려."
---

# React/Next.js 성능 최적화 가이드

React 및 Next.js 애플리케이션의 성능을 최적화하기 위한 58개 규칙을 **영향도 순**으로 정리한 가이드예요.
Vercel Engineering의 React Best Practices를 기반으로 해요.

> **범위 구분:**
> - 컴포넌트 설계/아키텍처 → `fe-react-patterns`
> - 일반 코드 품질/클린코드 → `fe-code-conventions`
> - **성능 최적화 (이 스킬)** → 렌더링, 번들, 비동기, 서버 패턴

---

## 성능 최적화 우선순위 가이드

영향도가 높은 순서대로 최적화를 적용하세요. 낮은 우선순위부터 시작하면 노력 대비 효과가 적어요.

### 🔴 CRITICAL — 비동기 워터폴 제거
**2~10배 성능 개선 가능. 가장 먼저 확인하세요.**
- `Promise.all()`로 독립적인 비동기 작업 병렬 실행
- 의존성 있는 요청은 `better-all` 또는 Promise 체이닝으로 최대 병렬화
- Suspense 경계를 전략적으로 배치하여 스트리밍
- 불필요한 `await`는 실제 사용 분기로 이동
- API 라우트에서 Promise를 먼저 생성하고 나중에 await

→ 상세: [references/async-waterfall.md](references/async-waterfall.md)

### 🔴 CRITICAL — 번들 최적화
**TTI, LCP에 직접 영향. barrel import는 200~800ms 비용 발생.**
- barrel 파일 re-export 대신 직접 import (또는 `optimizePackageImports`)
- `next/dynamic`으로 무거운 컴포넌트 지연 로드
- 분석/로깅 등 비핵심 서드파티 하이드레이션 후 로드
- 중요 리소스는 hover/focus 시점에 preload
- 조건부 기능은 활성화 시에만 모듈 로드

→ 상세: [references/bundle.md](references/bundle.md)

### 🟠 HIGH — 서버사이드 성능
**요청 중복 제거, 직렬화 최소화, 병렬 페칭으로 서버 응답 시간 단축.**
- `React.cache()`로 요청 내 중복 제거 (원시 타입 인자 사용)
- LRU 캐시로 요청 간 데이터 캐싱
- 서버 액션에 반드시 인증/권한 검증 추가
- RSC 경계에서 직렬화할 데이터 최소화
- 컴포넌트 합성으로 서버 페칭 병렬화
- `after()`로 로깅/분석 등 비차단 처리
- 정적 I/O (폰트, 로고)를 모듈 레벨로 호이스팅

→ 상세: [references/server.md](references/server.md)

### 🟡 MEDIUM-HIGH — 클라이언트 데이터 페칭
**SWR로 자동 중복 제거, 이벤트 리스너 최적화.**
- SWR로 요청 중복 제거 및 캐싱
- 글로벌 이벤트 리스너 중복 등록 방지
- scroll/touch에 `{ passive: true }` 적용
- localStorage 스키마 버전 관리 및 최소화

→ 상세: [references/client.md](references/client.md)

### 🟢 MEDIUM — 리렌더 최적화
**불필요한 리렌더를 줄여 UI 반응성 개선.**
- 단순 표현식은 `useMemo` 불필요
- 비용이 큰 작업은 `memo()` 컴포넌트로 분리
- 비원시 타입 기본값은 상수로 호이스팅
- 파생 상태는 렌더 중 계산 (Effect 사용 금지)
- `setState(prev => ...)` 함수형 업데이트로 안정 콜백
- `useState(() => ...)` 지연 초기화
- `startTransition`으로 비긴급 업데이트 처리
- Effect 의존성은 원시 타입으로 좁히기
- 콜백에서만 쓰는 상태는 구독하지 말기
- 상호작용 로직은 이벤트 핸들러에 넣기
- 자주 변하는 일시적 값은 `useRef` 사용

→ 상세: [references/rerender.md](references/rerender.md)

### 🟢 MEDIUM — 렌더링 성능
**하이드레이션, 조건부 렌더링, CSS 최적화.**
- 조건부 렌더링에 `&&` 대신 삼항 연산자 사용
- `content-visibility: auto`로 오프스크린 렌더링 지연
- 하이드레이션 불일치 방지: 인라인 스크립트 활용
- 예상된 하이드레이션 불일치는 `suppressHydrationWarning`
- SVG 좌표 정밀도 축소, SVG 애니메이션은 래퍼 div에
- 정적 JSX는 컴포넌트 외부로 호이스팅
- `useTransition`으로 로딩 상태 관리
- `<Activity>`로 상태 보존하며 토글

→ 상세: [references/rendering.md](references/rendering.md)

### 🔵 LOW-MEDIUM — JavaScript 마이크로 최적화
**핫 패스에서 누적 효과. 일반 코드에서는 우선순위 낮음.**
- `Map`/`Set`으로 O(1) 조회
- 조기 반환으로 불필요한 연산 회피
- 반복 함수 호출 결과를 Map으로 캐싱
- RegExp를 루프 밖으로 호이스팅
- DOM 스타일 변경 배치 (레이아웃 스래싱 방지)
- `toSorted()` 등 불변 배열 메서드 사용
- 앱 초기화는 마운트가 아닌 모듈 레벨에서 1회만
- 이벤트 핸들러를 ref에 저장하여 안정적 구독
- `useEffectEvent`로 안정적 콜백 참조

→ 상세: [references/js-optimization.md](references/js-optimization.md)

---

## 레퍼런스 파일 가이드

| 파일 | 내용 | 언제 참조? |
|------|------|-----------|
| `async-waterfall.md` | 비동기 워터폴 제거 (5개 규칙) | 데이터 페칭이 느릴 때, Promise 패턴 최적화 시 |
| `bundle.md` | 번들 최적화 (5개 규칙) | 초기 로딩이 느릴 때, TTI/LCP 개선 시 |
| `server.md` | 서버사이드 성능 (8개 규칙) | RSC/서버 액션 작성 시, 서버 응답 최적화 시 |
| `client.md` | 클라이언트 데이터 페칭 (4개 규칙) | 클라이언트 데이터 로딩 최적화 시 |
| `rerender.md` | 리렌더 최적화 (12개 규칙) | 컴포넌트가 불필요하게 리렌더될 때 |
| `rendering.md` | 렌더링 성능 (9개 규칙) | 하이드레이션/CSS/SVG 렌더링 문제 시 |
| `js-optimization.md` | JS 마이크로 최적화 (9개 규칙) | 핫 패스 코드 최적화, 고급 패턴 적용 시 |

---

## React Compiler 참고

프로젝트에 [React Compiler](https://react.dev/learn/react-compiler)가 활성화되어 있다면:
- `memo()`, `useMemo()`, `useCallback()`의 수동 메모이제이션이 자동화돼요
- 정적 JSX 호이스팅도 자동 처리돼요
- 그러나 **비동기 워터폴, 번들 최적화, 서버 패턴** 등은 여전히 수동 적용이 필요해요

---

## 기존 스킬과의 관계

이 스킬은 `vercel-react-best-practices` 스킬의 58개 규칙을 한국어로 정리하고 영향도 순으로 재구성한 버전이에요. 두 스킬이 동시에 있을 경우 이 스킬을 우선 참고하세요.

## 이 스킬을 사용하지 않는 경우

- 컴포넌트 설계/아키텍처 → `fe-react-patterns`를 참고하세요
- 일반 코드 컨벤션 (네이밍, 가독성) → `fe-code-conventions`를 참고하세요
- 접근성 → `fe-a11y`를 참고하세요
- 순수 백엔드/서버 로직 최적화에는 이 스킬이 적용되지 않아요
