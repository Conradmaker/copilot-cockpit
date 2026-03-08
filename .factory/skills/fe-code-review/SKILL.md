---
name: fe-code-review
description: "Unified frontend code review guide integrating clean code, React patterns, accessibility, and performance checks. Use this skill when reviewing pull requests, conducting code reviews, auditing frontend code quality, or when the user asks to review their code. Always use this skill when the user asks to check, review, or improve existing code quality. Triggers on: code review, PR review, review my code, audit code, 코드 리뷰, PR 리뷰, 코드 검토, 코드 감사, 코드 봐줘, 이거 괜찮아?, 이 코드 어때?, 뭐가 잘못됐어?, 개선할 점, 코드 피드백, 코드 품질 체크, PR 올리기 전에, 머지해도 될까, pull request."
---

# 프론트엔드 코드 리뷰 가이드

## 목표

코드 컨벤션 → React 패턴 → 접근성 → 성능 순으로 리뷰한다. 이 순서를 따르면 근본적인 구조 문제를 먼저 잡고 세부 최적화를 나중에 검토할 수 있다.

아래는 각 단계의 빠른 판단 기준이다. 실제 리뷰 시에는 [references/checklist.md](references/checklist.md)의 상세 체크리스트와 각 전문 스킬(`fe-code-conventions`, `fe-react-patterns`, `fe-a11y`, `fe-react-performance`)을 함께 참고해야 정확한 판단이 가능하다.

---

## 4단계 리뷰 절차

### 1단계: 코드 컨벤션 (가독성 · 예측가능성 · 응집도 · 결합도)

**가독성**

- 매직 넘버에 의미 있는 이름이 있는가? — `if (status === 3)` 같은 코드는 `COMPLETED`처럼 상수로 추출한다
- 복잡한 조건식이 의미 있는 변수로 추출되었는가? — `if (a && b && !c)` → `const isEligible = a && b && !c`
- 중첩 삼항 연산자 대신 명확한 분기를 사용하는가? — 삼항은 1단만. 2단 이상은 `if/else` 또는 초기 리턴으로 분리
- 구현 상세가 적절히 추상화되어 있는가? — 반복되는 래핑(config 초기화, try-catch 등)은 래퍼/HOC로 숨긴다
- 긴 텍스트, 빈 문자열, 빈 배열에서도 UI가 깨지지 않는가? — truncate/empty state 없이 그대로 렌더되면 의도치 않은 오버플로우나 빈 화면이 생길 수 있다

**예측가능성**

- 함수/변수 이름이 동작을 정확히 설명하는가? — `handleClick`보다 `handleSubmitOrder`가 예측 가능하다
- 같은 종류의 함수들이 일관된 반환 타입을 가지는가? — `fetch` 함수가 때로는 `T`, 때로는 `T | null`을 반환하면 안 된다. Discriminated Union(`{ ok: true, data } | { ok: false, error }`)을 사용한다
- 숨겨진 사이드 이펙트가 없는가? — `getUser()`라는 이름인데 내부에서 캐시를 갱신하면 안 된다. 이름에 드러나지 않는 동작을 숨기지 않는다
- 날짜/숫자 포맷이 하드코딩되어 있지 않은가? — 날짜·시간·통화·숫자는 `Intl.DateTimeFormat`, `Intl.NumberFormat`을 우선 사용한다

**응집도**

- 함께 수정되는 파일이 같은 디렉토리에 있는가? — feature 디렉토리 안에 컴포넌트·훅·유틸·테스트를 함께 배치한다
- 폼 필드의 유효성 검증과 UI가 함께 위치하는가? — 검증 로직이 별도 utils/에 흩어지면 응집도가 떨어진다. 필드 단위로 유효성 검증을 함께 둔다
- 불필요한 추상화 없이 의미 있는 중복은 허용하는가? — 3번 미만 반복이면 중복을 유지하는 편이 더 나을 수 있다

**결합도**

- Props Drilling이 적절히 해결되었는가? — Composition 패턴(children으로 내려보내기)을 Context보다 우선 시도한다
- 각 함수/컴포넌트가 하나의 책임만 가지는가? — 데이터 패칭과 UI 렌더링이 한 함수에 있으면 분리한다

> 실제 리뷰 시에는 `fe-code-conventions` SKILL과 reference 문서를 직접 읽고 원칙별 코드 예시를 확인한다.

### 2단계: React 패턴 (설계 · 합성 · 상태관리)

**컴포넌트 설계**

- Boolean props 대신 명시적 variant를 사용하는가? — `<Button primary ghost>` → `<Button variant="primary">`. Boolean 조합이 2개 이상이면 의미 충돌이 발생한다
- 관련 컴포넌트가 Compound Component로 그룹화되었는가? — `<Select>`, `<Select.Option>`, `<Select.Group>` 식으로 네임스페이스를 공유하면 사용처에서 조합이 명확해진다
- `children`이 render props보다 우선 사용되었는가? — children은 가장 단순한 합성. render props는 부모에게 데이터를 노출해야 할 때만 사용한다
- 컴포넌트가 적절한 크기로 분리되었는가? — 한 파일이 200줄 이상이면 분리 시점을 의심한다
- 파괴적 액션에 확인 모달 또는 되돌리기 흐름이 있는가? — 삭제/초기화/해제는 즉시 실행보다 확인 또는 undo가 안전하다

**상태 관리**

- Context가 구현이 아닌 인터페이스(`state`, `actions`, `meta`)로 설계되었는가? — Context value에 구현 상세(내부 상태, reducer dispatch)를 노출하지 않는다
- 상태가 적절한 레벨에 위치하는가? — 하위 컴포넌트만 사용하는 상태를 최상위로 끌어올리지 않는다
- Provider가 상태 구현의 유일한 소유자인가? — 상태 로직이 Provider 밖에 분산되면 디버깅이 어렵다
- 탭, 필터, 페이지네이션 같은 상태가 URL에 반영되는가? — 새로고침, 공유, 뒤로가기에 견디지 못하면 상태 설계가 약한 신호다

**React 19 (해당 시에만)**

- `forwardRef` 대신 직접 `ref` prop을 사용하는가?
- `useContext` 대신 `use()`를 사용하는가?

> 실제 리뷰 시에는 `fe-react-patterns` SKILL과 reference 문서를 직접 읽고 패턴별 Before/After 예시를 확인한다.

### 3단계: 접근성 (ARIA · 시맨틱 · 키보드)

**올바른 구조**

- 인터랙티브 요소가 중첩되지 않았는가? — 버튼 안에 링크, 링크 안에 버튼은 금지. 카드 UI는 레이어를 분리해 클릭 영역을 겹치지 않게 한다
- 시맨틱 HTML 요소를 우선 사용하는가? — `<div onClick>` 대신 `<button>`. `role="button"`을 `<div>`에 붙이면 키보드·포커스 동작을 모두 수동 구현해야 한다
- 비상호작용 요소에 상호작용 역할(role)을 부여하지 않았는가?
- 포커스 표시를 제거하지 않았는가? — `outline-none`을 썼다면 `:focus-visible` 또는 동등한 대체 스타일이 반드시 필요하다

**의미 전달**

- 모든 인터랙티브 요소에 접근 가능한 이름(label)이 있는가? — 우선순위: 보이는 `<label>` > `aria-labelledby` > `aria-label`. 아이콘 버튼에는 반드시 `aria-label`을 제공한다
- 같은 이름의 요소에 구분 가능한 추가 설명이 있는가? — "더 보기" 링크가 3개면 `aria-label="프로모션 더 보기"` 등으로 구분한다
- `aria-*` 속성이 올바르게, 최소한으로 사용되었는가? — 시맨틱 HTML로 충분한 곳에 ARIA를 중복 적용하지 않는다

**예측 가능한 인터랙션**

- 버튼 역할과 동작이 일치하는가? — 페이지 이동은 `<a>`, 인터랙션 동작은 `<button>`. form 안 버튼은 `type="button"`을 명시해 의도치 않은 submit을 방지한다
- 폼이 `<form>` 태그로 감싸져 있는가? — `<form>`은 Enter 키 제출, 자동완성, 스크린 리더 탐색(랜드마크)을 제공한다
- 키보드로 모든 기능을 사용할 수 있는가? — Tab 순서가 시각적 순서와 일치하는가, Escape로 닫기가 가능한가
- 입력에 `name`, `autocomplete`, `type`, `inputMode`가 적절히 설정되어 있는가? — 모바일 키패드, 자동완성, 브라우저 기본 UX와 직접 연결된다
- 붙여넣기 차단과 오류 포커스 누락이 없는가? — `onPaste` 차단은 피하고, 제출 실패 시 첫 번째 오류 필드로 포커스를 보낸다

**시각 정보 보완**

- 이미지에 적절한 `alt` 텍스트가 있는가? — 장식용은 `alt=""`, 정보 전달용은 내용을 설명한다
- 색상만으로 정보를 구분하지 않는가? — 에러 표시에 빨간색 + 아이콘/텍스트를 함께 사용한다

**UI 컴포넌트**

- 모달이 포커스 트래핑, Escape 닫기를 지원하는가? — `<dialog>` + `showModal()`을 사용하면 내장 지원. 배경에 `inert`를 적용해 포커스 이탈을 방지한다
- 탭/아코디언이 화살표 키 탐색을 지원하는가? — 탭: `role="tablist"` + `role="tab"` + `role="tabpanel"`, `aria-selected`로 활성 탭 표시
- `tabIndex`에 양수 값이 사용되지 않았는가? — 0(자연 순서) 또는 -1(프로그래밍 포커스 전용)만 허용
- 모달/드로어의 스크롤 영역이 배경 페이지로 전파되지 않는가? — 필요한 경우 `overscroll-behavior: contain`을 검토한다

> 실제 리뷰 시에는 `fe-a11y` SKILL과 reference 문서를 직접 읽고 컴포넌트별 접근성 패턴을 확인한다.

### 4단계: 성능 (번들 · 리렌더 · 서버)

**워터폴 제거 (Critical)**

- 독립적인 비동기 요청이 `Promise.all()`로 병렬 처리되는가? — `const a = await fetchA(); const b = await fetchB();` → `const [a, b] = await Promise.all([fetchA(), fetchB()])`
- 불필요한 `await`로 블로킹하지 않는가? — 결과가 바로 필요하지 않으면 `await`를 조건 분기 뒤로 이동한다
- Suspense 경계가 적절히 설정되었는가? — 각 비동기 영역을 감싸지 않으면 가장 느린 요청이 전체를 지연시킨다

**번들 크기 (Critical)**

- barrel 파일(`index.ts`에서 re-export) 대신 직접 임포트를 사용하는가? — tree-shaking이 실패하면 번들에 불필요한 코드가 포함된다
- 무거운 서드파티 스크립트가 지연 로드되는가? — 분석·채팅 위젯 등은 `next/script strategy="lazyOnload"`를 사용한다
- `next/dynamic` 또는 `React.lazy`로 코드 분할을 하는가? — 모달·차트 등 즉시 필요하지 않은 컴포넌트는 지연 로드한다

**서버 사이드 (High)**

- 서버 데이터 캐싱이 적절한가? — 동일 렌더 내 중복 호출은 `React.cache`로 제거, 요청 간 재사용은 LRU 캐시를 사용한다
- RSC props에 중복 직렬화가 없는가? — 같은 데이터를 여러 클라이언트 컴포넌트에 반복 전달하면 HTML 크기가 커진다
- 서버 액션에 인증 검사가 있는가? — 서버 액션은 공개 HTTP 엔드포인트이므로 반드시 인증/인가를 확인한다

**리렌더 최적화 (Medium)**

- 불필요한 리렌더가 방지되었는가? — `memo`보다 먼저 컴포넌트 분리를 시도한다. derived state는 `useEffect` 대신 렌더 시점에 계산한다
- 비-프리미티브 기본값이 컴포넌트 외부에 호이스팅되었는가? — `items = []` 같은 기본값은 매 렌더마다 새 참조를 생성한다
- 콜백에서만 사용하는 상태를 구독하지 않는가? — `useRef`로 최신 값만 참조하면 리렌더를 피할 수 있다

**렌더링 (Medium)**

- `content-visibility: auto`가 긴 리스트에 적용되었는가? — 뷰포트 밖 콘텐츠의 렌더링을 건너뛰어 초기 로드 속도를 개선한다
- 정적 JSX가 컴포넌트 외부로 추출되었는가? — 변하지 않는 JSX 블록을 상수로 호이스팅하면 React가 비교를 건너뛴다
- `transition: all`을 피하고 reduced motion을 지원하는가? — 잦은 애니메이션일수록 `transform`/`opacity` 중심으로 제한하고 `prefers-reduced-motion`을 확인한다
- 렌더링 중 레이아웃 읽기와 DOM 쓰기가 섞이지 않는가? — `getBoundingClientRect`, `offsetHeight` 같은 읽기와 style 변경을 교차하면 강제 리플로우가 발생한다
- 이미지 크기와 로딩 우선순위가 명시되는가? — `width`/`height`, `loading="lazy"`, 핵심 이미지 우선 로드 전략을 검토한다

> 실제 리뷰 시에는 `fe-react-performance` SKILL과 reference 문서를 직접 읽고 우선순위별 최적화 기법을 확인한다.

---

## 결과 보고 형식

```
파일경로:줄번호 - [카테고리] 이슈 설명
  → 제안: 개선 방법
```

**심각도:**

- 🔴 Critical: 버그, 접근성 위반, 보안 문제 — 머지 전 수정
- 🟡 Warning: 성능 이슈, 패턴 위반, 가독성 저하 — 수정 권장
- 🟢 Suggestion: 더 나은 패턴, 미세 최적화 — 선택적 반영

---

## references/ 가이드

아래 문서는 "더 자세한 참고자료"가 아니라, 실제 리뷰를 수행하기 전 반드시 확인해야 하는 상세 체크리스트다. 본문에서 리뷰 방향을 잡고, 실제 코드를 점검할 때 체크리스트를 열어 항목별로 확인한다.

단계별 상세 체크리스트는 [references/checklist.md](references/checklist.md)에 있다.

---

## 범위

새 코드 작성 시에는 각 전문 스킬(`fe-code-conventions`, `fe-react-patterns`, `fe-a11y`, `fe-react-performance`)을 직접 참고한다. 이 스킬은 기존 코드 리뷰 전용이다.
