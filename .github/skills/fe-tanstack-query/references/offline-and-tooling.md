# Offline And Tooling

## 목표

offline UX와 운영 도구를 구조 단계에서 같이 본다. networkMode, persistence, error boundary reset, Devtools, ESLint plugin query, testing은 부가 옵션이 아니라 안정성 장치다.

이 문서는 기존 `network-mode`, `persist-queries`, `err-error-boundaries` rule과 최신 tooling 보강을 합친 reference다.

---

## 핵심 규칙

### network-mode

- 대부분의 앱은 기본 `online` 모드로 충분하다
- offline-first 성격이 강하면 `always` 또는 `offlineFirst`를 검토한다
- `fetchStatus === "paused"`를 사용자 피드백에 반영할지 같이 본다

### persist-queries

- persistence가 필요하면 `@tanstack/react-query-persist-client` 기반 구성을 쓴다
- persisted cache가 의미 있으려면 gcTime이 너무 짧지 않아야 한다
- `buster`, `maxAge`, `shouldDehydrateQuery`로 persistence 범위를 제어한다
- sensitive data, real-time data, failed query는 기본 제외 후보로 본다

### err-error-boundaries

- Suspense query에는 error boundary reset 경로를 둔다
- `useQueryErrorResetBoundary`와 boundary `onReset`을 연결한다
- granular boundary로 failure isolation을 설계할 수 있다

---

## tooling 보강

- Devtools는 local debug에서 cache shape와 stale status를 빠르게 확인하는 기본 도구다
- ESLint Plugin Query의 stable-query-client, no-unstable-deps, no-rest-destructuring 같은 규칙을 검토한다
- test에서는 fresh QueryClient per test, retry off, staleTime/gcTime 제어를 기본값으로 두는 편이 안전하다

## streaming + persistence 주의사항

- advanced SSR streaming에서 pending query dehydration을 켠 경우, persist adapter는 successful query만 저장하도록 조정한다
- promise를 storage에 저장하지 않도록 `dehydrateOptions.shouldDehydrateQuery`를 분리한다

## 빠른 체크리스트

- networkMode가 앱 성격과 맞는가
- persisted query 범위가 과하지 않은가
- Suspense error reset 경로가 있는가
- Devtools, ESLint, test용 QueryClient 전략이 준비됐는가