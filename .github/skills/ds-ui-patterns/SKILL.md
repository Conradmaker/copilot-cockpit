---
name: ds-ui-patterns
description: "Modern UI layout patterns, section composition, dashboard design, SaaS landing structures, interactive sections, and engaging design techniques. Use this skill when designing page layouts, structuring SaaS landing pages, building dashboards, composing hero sections, creating bento grids, designing navigation menus, structuring pricing pages, building analytics views, or deciding how to arrange sections and interactive elements on a page. Always consult this skill when making layout and section composition decisions, even if the user only asked to 'make a landing page' or 'build a dashboard'. For product-level UX flows and copy use ds-product-ux. For visual design foundations (color, typography, spacing) use ds-visual-design. For Tailwind CSS implementation use fe-tailwindcss. For component API design use fe-ui-element-components. Triggers on: layout pattern, page layout, landing page, hero section, bento grid, dashboard layout, sidebar, SaaS layout, section design, pricing page, analytics page, navigation menu, popover, modal layout, interactive section, tab section, card layout, grid layout, 레이아웃, 페이지 구성, 랜딩 페이지, 히어로 섹션, 벤토 그리드, 대시보드, 사이드바, SaaS 디자인, 섹션 구성, 가격 페이지, 분석 페이지, 내비게이션, 카드 레이아웃, 그리드."
---

# UI 레이아웃 패턴 (ds-ui-patterns)

## 목표

페이지와 섹션을 정보 전달과 사용자 탐색에 최적화된 구조로 설계한다. 이 스킬은 개별 컴포넌트가 아니라, 화면 전체의 레이아웃 구성, 섹션 배치, 대시보드 설계, 인터랙티브 패턴 같은 "큰 그림" 수준의 판단 기준을 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 레이아웃을 설계하거나 섹션을 구성할 때는 아래 reference 문서를 직접 읽고 상황에 맞는 패턴과 예시를 확인한 뒤 적용한다.

---

## 6대 핵심 원칙

### 1. 레이아웃 패턴으로 정보를 구조화한다

검증된 레이아웃 패턴을 시작점으로 사용하면 사용자의 기대를 존중하면서도 탐색 비용을 낮출 수 있다.

- 정형화된 히어로 섹션: 중앙 정렬 큰 텍스트 + 아래 큰 이미지 + 충분한 여백이 기본이다
- 벤토(Bento) 레이아웃: 격자 구조를 따르되 카드 크기 변주로 트렌디함을 유지한다
- 직선 그리드: 명확한 선으로 구획을 나눠 정보를 구조적으로 전달한다
- 로고 섹션: 유명 기업 로고로 사회적 증거를 제공한다 — 마키 애니메이션 + 가장자리 블러가 고급스럽다
- 클릭 가능한 멀티 섹션(탭): 사용자가 직접 탐색하며 인지 부하를 줄인다
- 내비게이션 드롭다운에 텍스트 리스트 대신 이미지를 함께 배치하면 맥락 파악이 빨라진다

#### 빠른 판단 기준

- 히어로 섹션에 CTA가 2개 이상이면 하나로 줄인다
- 섹션이 5초 스크롤 안에 핵심 아이디어를 전달하지 못하면 구조를 단순화한다
- 벤토 그리드가 기계적인 격자로만 보이면 카드 크기에 변주를 준다

→ 상세: [references/01-saas-layout.md](references/01-saas-layout.md)

### 2. 대시보드는 인지 부하를 줄이는 방향으로 설계한다

대시보드는 랜딩 페이지와 정반대다 — 많은 정보를 좁은 공간에 넣어야 하므로 폰트 크기는 작게, 간격은 촘촘하게 가져간다.

- 사이드바는 영구적으로 필요한 요소(내비게이션, 프로필, 검색)만 담고, 자주 안 쓰는 링크는 하단으로 밀거나 팝오버로 숨긴다
- 그리드 시스템을 엄격하게 지키고, 사용자가 가장 중요하게 생각하는 정보를 메인 섹션 상단에 배치한다
- 리스트와 테이블은 검색, 필터링, 정렬 기능을 추가해 인터랙티브한 도구로 만든다
- 벌크 액션(여러 항목 선택 시 나타나는 버튼)을 통해 평소에는 화면을 깔끔하게 유지한다
- 불필요한 정보(같은 KPI가 여기저기 반복)가 있으면 과감히 제거한다

#### 빠른 판단 기준

- 사이드바 링크가 10개 이상이면 그룹화하거나 팝오버로 분리한다
- 같은 데이터가 2곳 이상에서 반복되면 가장 중요한 곳만 남긴다
- 차트가 복잡한 모양이면 단순한 선 그래프나 막대 그래프로 바꿀 수 있는지 먼저 확인한다

→ 상세: [references/02-dashboard-design.md](references/02-dashboard-design.md)

### 3. 참여형 디자인으로 사용자의 몰입을 높인다

지루한 디자인과 매혹적인 디자인의 차이는 사용자가 화면과 "상호작용"할 수 있느냐에 있다.

- 여백을 활용한 문맥 부여: 텍스트 주변에 서비스 성격을 보여주는 이미지, 아이콘을 배치해 글을 읽지 않아도 직관적으로 느끼게 한다
- 패턴 깨기: 때로는 표준 레이아웃에서 벗어나 사용자에게 예상치 못한 즐거움을 주는 요소가 필요하다
- 보상형 UI: 사용자의 클릭이나 탐색 행동에 세련된 애니메이션으로 시각적 보상을 제공한다
- 404 에러 페이지를 브랜드의 매력을 보여주는 쇼케이스로 탈바꿈한다
- 친근한 언어(카피)를 사용한다 — 딱딱한 기업형 문구 대신 자연스럽고 쉬운 표현

#### 빠른 판단 기준

- 텍스트 주변이 텅 비어 보이면 문맥을 제공하는 시각적 요소를 추가한다
- 장식 요소가 시선을 중앙(핵심 메시지)으로 모이게 하는지 확인한다
- 사용자가 클릭했을 때 시각적 변화가 없다면 피드백 요소를 추가한다

→ 상세: [references/03-engaging-ui.md](references/03-engaging-ui.md)

### 4. 모션과 애니메이션은 목적이 있어야 한다

좋은 모션은 원인과 결과를 보여주고 주의를 핵심 기능으로 이끈다. 목적 없는 화려한 애니메이션은 탐색을 방해할 뿐이다.

- 호버(Hover) 시 제품 기능을 시연하는 애니메이션은 가치가 있지만, 복잡하기만 한 애니메이션은 내비게이션을 방해한다
- 스크롤에 따라 텍스트가 사라지고 이미지가 나타나는 점진적 노출(Progressive Disclosure)로 모션이 명확성을 지원하게 한다
- 패럴랙스(Parallax)는 무거운 3D 없이도 깊이감을 줄 수 있다 — 가장자리 장식 요소에 적용하면 효과적이다
- 작고 절제된(Tasteful) 애니메이션이 과도한 3D보다 전문적이다
- 텍스트 마이크로 인터랙션(타이핑 효과, 단어 변환)은 시선을 잡는 데 효과적이다

#### 빠른 판단 기준

- 정적인 UI로도 같은 정보를 전달할 수 있다면 애니메이션을 재검토한다
- 애니메이션이 있는데 "무엇이 바뀌었는지"가 불명확하면 실패한 모션이다
- 마우스 반응 애니메이션을 넣었는데 모바일 대응이 없으면 보완한다

→ 상세: [references/04-motion-interaction.md](references/04-motion-interaction.md)

### 5. AI 도구 UI는 투명성과 즉시성을 우선한다

AI 기반 제품의 UI 패턴은 투명성(AI가 무엇을 하는지 보여주기)과 즉시성(피드백 없는 대기를 줄이기)이 핵심이다.

- 거대한 프롬프트 입력창을 첫 화면에 배치해 사용자가 즉시 핵심 기능을 사용하게 만든다
- AI의 작업 과정("문서 검색 중 → 인용구 추출 중 → 답변 작성 중")을 시각화해 블랙박스가 아닌 협력 파트너로 느끼게 한다
- 스트리밍(한 단어씩 흘러나오는)과 스켈레톤(쉬머 효과)으로 대기 시간을 기대감으로 바꾼다
- 인라인 편집(드래그로 특정 부분만 수정)으로 흐름을 끊지 않는 실시간 교정 경험을 제공한다
- 생성 히스토리와 검색 기능을 제공해 과거 결과를 "워크스페이스"로 느끼게 한다
- 영구 메모리를 설정 깊숙이 숨기지 말고 사용자가 직접 보고 제어할 수 있는 전용 패널을 제공한다

#### 빠른 판단 기준

- 프롬프트 입력창에 모드 변경(칩), 파일 미리보기, 외부 툴 연동이 있는지 확인한다
- AI 응답 중 피드백이 없는 대기 구간이 있으면 스트리밍이나 스켈레톤을 적용한다
- 이전 히스토리를 검색할 수 없다면 검색 기능 추가를 검토한다

→ 상세: [references/05-ai-ui-patterns.md](references/05-ai-ui-patterns.md)

### 6. 현대 트렌드는 융합해서 사용한다

2026년 디자인의 가장 큰 특징은 단 하나의 트렌드만 쓰는 것이 아니라 여러 트렌드를 혼합하는 것이다.

- 그리드 기반 모듈형 디자인 + 인터랙티브 요소
- 2D 텍스트와 3D 배경의 혼합
- 미니멀리즘의 진화: 적은 것으로 더 많이 보여주기 (선, 여백, 대칭 활용)
- 가변 폰트로 타이포그래피 표현 확장
- 벤토 그리드 + 마우스 반응 인터랙션
- 손그림 일러스트나 마스코트로 브랜드 개성 부여

#### 빠른 판단 기준

- 하나의 트렌드만 과도하게 적용하고 있으면 다른 트렌드와 조합할 수 있는지 검토한다
- 트렌드를 따르되 사용자가 정보를 탐색하는 데 방해가 되지 않는지 먼저 확인한다
- 화려한 효과보다 사용성(탐색, 이해, 행동)이 우선이다

→ 상세: [references/06-modern-trends.md](references/06-modern-trends.md)

---

## references 가이드

아래 문서는 실제 레이아웃과 섹션 구성을 결정하기 전 직접 읽어야 하는 구현 가이드다.

| 파일                                                                       | 읽을 때                                                                         |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [references/01-saas-layout.md](references/01-saas-layout.md)               | SaaS 랜딩 페이지, 히어로, 벤토, 그리드, 로고, 멀티 섹션, 내비게이션을 구성할 때 |
| [references/02-dashboard-design.md](references/02-dashboard-design.md)     | 대시보드 레이아웃, 사이드바, 테이블, 차트, 팝오버/모달/토스트/탭을 설계할 때    |
| [references/03-engaging-ui.md](references/03-engaging-ui.md)               | 여백 문맥, 참여형 요소, 보상형 UI, 404 페이지, 친근한 카피를 설계할 때          |
| [references/04-motion-interaction.md](references/04-motion-interaction.md) | 목적 있는 모션, 패럴랙스, 텍스트 애니메이션, 점진적 노출을 판단할 때            |
| [references/05-ai-ui-patterns.md](references/05-ai-ui-patterns.md)         | AI 프롬프트, 히스토리, 인라인 편집, 작업 과정 시각화, 스켈레톤을 설계할 때      |
| [references/06-modern-trends.md](references/06-modern-trends.md)           | 2026 웹 디자인 트렌드, 트렌드 융합, 그리드/3D/미니멀 혼합을 판단할 때           |

### 추천 로드 순서

- SaaS 랜딩 페이지 설계: `01 → 03 → 04 → 06`
- 대시보드 설계: `02 → 04`
- AI 도구 UI: `05 → 02 → 04`
- 디자인 리뷰: `01 → 03 → 06`

---

## 범위

- 프로덕트 UX 흐름, CTA, 로딩, 피드백, 확인 → `ds-product-ux`
- 색상, 타이포, 스페이싱, 시각적 계층 → `ds-visual-design`
- Tailwind CSS 토큰, 유틸리티, className 병합 → `fe-tailwindcss`
- 구현 수준의 접근성, ARIA, 키보드 → `fe-a11y`
- 공유 UI 컴포넌트 API, 디자인 시스템 아키텍처 → `fe-ui-element-components`
- React 퍼포먼스, 번들 → `fe-react-performance`
