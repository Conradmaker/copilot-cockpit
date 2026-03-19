---
name: ds-visual-design
description: "Visual design foundations for building coherent color, typography, spacing, hierarchy, depth, and icon systems in UI. Use this skill when designing or reviewing palettes, dark mode, font pairing, type scales, spacing systems, emphasis, shadows, or overall visual polish. Always consult this skill for visual decisions that affect perceived structure, readability, emphasis, or brand tone, even if the user only asks to pick a color, tweak spacing, adjust typography, or make a screen feel more refined. For product-level flows and copy use ds-product-ux. For layout and section composition use ds-ui-patterns. For Tailwind tokens and utilities use fe-tailwindcss. Triggers on: color palette, dark mode, OKLCH, typography, font pairing, type scale, spacing system, visual hierarchy, shadows, depth, icon style, design polish, 색상 시스템, 컬러 팔레트, 다크모드, 타이포그래피, 폰트 조합, 폰트 스케일, 스페이싱, 시각적 계층, 그림자, 깊이감, 아이콘, 디자인 퀄리티."
---

# 시각 디자인 기초 (ds-visual-design)

## 목표

색상, 타이포그래피, 스페이싱, 시각적 계층, 깊이감, 아이콘을 체계적으로 다뤄 UI가 구조적이고 일관되며 신뢰감 있게 보이게 만든다. 이 스킬은 단순히 "예쁘게 만드는" 수준이 아니라, 사용자의 시선을 유도하고 정보를 계층화하며 브랜드 정체성을 유지하는 시각적 시스템의 판단 기준을 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 색상을 고르거나 스페이싱을 설계하거나 시각적 계층을 점검할 때는 아래 reference 문서를 직접 읽고 상황에 맞는 기준과 예시를 확인한 뒤 적용한다.

---

## 6대 핵심 원칙

### 1. 색상 시스템을 체계적으로 설계한다

색상은 브랜드 컬러 하나를 고르는 게 아니라, 중립색 레이어 → 기능적 액센트 → 시맨틱 컬러 → 다크모드 전략까지 포함하는 시스템으로 설계해야 한다.

- 60-30-10 법칙을 시작점으로 사용하되, 프로덕트에서는 중립 기반 레이어와 컬러 램프로 확장한다
- 강조색(Accent)은 전체의 10% 이하로 제한하고, 나머지는 중립색과 보조색으로 채운다
- 브랜드 컬러를 단일 값이 아니라 가장 밝은 톤부터 어두운 톤까지의 컬러 램프로 준비한다
- 삭제는 빨간색, 성공은 초록색 같은 시맨틱 컬러는 브랜드 컬러와 별개로 유지한다
- 다크모드는 단순 반전이 아니라, 요소 간 색상 거리를 라이트모드의 2배로 넓히고 고도가 높은 surface일수록 밝게 한다

#### 빠른 판단 기준

- 강조색이 너무 밝아 눈이 아프면 채도를 낮추고 텍스트를 검은색으로 바꾼다
- 완전한 검정(#000000)이나 흰색(#FFFFFF)보다 짙은 회색, 연한 회색을 먼저 검토한다
- 중립색 배경에 브랜드 톤을 살짝 섞으면 세련된 느낌이 난다
- 차트 색상이 구분 안 되면 OKLCH 팔레트를 검토한다
- 다크모드에서 순수 화이트 텍스트는 밝은 회색으로 바꿔 눈의 피로를 줄인다

→ 상세: [references/01-color-system.md](references/01-color-system.md)

### 2. 타이포그래피로 개성과 계층을 만든다

폰트 선택은 미적 취향이 아니라, 브랜드 성격을 설정하고 텍스트 간 역할을 구분하는 구조적 결정이다. 타이포그래피 자체가 강력한 아트 디렉션이 될 수 있다.

- 헤드라인(앵커 폰트)를 먼저 정하고, 시각적 대비가 느껴지는 본문 폰트를 조합한다
- 구글 폰트 등 기본 제공 폰트 외에도 커스텀 폰트 리서치를 습관화하되, 실사용 전 상업용 라이선스를 반드시 확인한다
- 너무 비슷한 폰트끼리 조합하면 오히려 어색하다 — 대비감이 핵심이다
- 폰트 수는 1~2개가 안정적이고, 3개까지 허용 가능하지만 4개 이상은 거의 항상 과하다
- 한 디자인에 폰트 두께는 최대 2가지, 텍스트 색상은 기본 + 투명도 조정 1~2가지로 제한한다
- 폰트 크기는 비율 기반 스케일(golden ratio 1.618 또는 촘촘한 1.272)로 시스템화한다 — 랜딩은 6개 이하, 대시보드는 24px 이하 스케일이 일반적이다
- line-height는 본문 약 150%, 큰 제목 130~150%로 설정하고 밀도감을 만든다.
- 반응형에서는 clamp 같은 fluid typography로 화면 크기에 따라 자연스럽게 변화시킨다
- 텍스트 스와핑이나 모핑 등 텍스트 자체를 시각적 변화 요소로 다룰 수 있다
- 숙련도가 부족하면 단일 sans-serif가 안전하고, 강한 브랜드 성격이 필요하면 앵커+대비 body 조합을 적극 활용한다
- Display Font는 시각 요소로 활용할 수 있지만 페이지당 1~2회로 절제한다
- 가변 폰트(Variable Fonts)는 굵기, 기울기, 형태를 세밀하게 제어할 수 있어 타이포그래피 표현력을 높인다

#### 빠른 판단 기준

- 헤드라인과 본문을 합쳐 3개 이상 폰트 패밀리가 보이면 줄일지 먼저 검토한다
- 폰트 크기만으로 계층을 나누고 있다면 두께와 색상(불투명도)을 함께 조정한다
- 폰트 크기가 비율 기반 스케일 없이 임의로 정해져 있다면 시스템화를 먼저 검토한다
- 큰 제목의 line-height가 본문과 같으면(150%) 130~150%로 약간 줄여 밀도감을 확인한다
- Fonts in Use 같은 사이트에서 앵커 폰트와의 조합 사례를 참고한다

→ 상세: [references/02-typography.md](references/02-typography.md)

### 3. 스페이싱으로 관계와 구조를 드러낸다

간격은 요소 간의 관계를 시각적으로 보여준다. 같은 간격을 모든 곳에 동일하게 쓰면 구조가 흐려진다.

- px 대신 rem 단위를 기본으로 사용하고, 0.25rem(4px) 단위로 일관된 스케일을 구축한다
- 관련된 요소는 작은 간격으로 그룹화하고, 다른 그룹과는 1rem 이상으로 분리한다
- 요소 안쪽 간격(Inner)은 반드시 바깥쪽 간격(Outer/Padding)보다 작아야 한다
- 상하 패딩은 좌우 패딩보다 작게 설정한다 — 텍스트의 시각적 무게가 좌우로 쏠리기 때문이다
- 간격을 설정할 때는 큰 값(1.5~2rem)에서 시작해 줄여가는 방향이 결과가 좋다
- 수학적으로 같은 padding도 시각적으로 다르게 보일 수 있다(optical correction) — 텍스트 bounding box 때문에 위쪽 여백을 미세하게 줄여야 할 때가 있다
- heading과 subtext는 가깝게, 별개 조작 그룹은 멀게 — 간격은 요소 간 관계 강도(relationship strength)를 반영한다
- spacing preset(XS~2XL)은 선형보다 지수적으로 커질 때 인지 단계와 잘 맞는다
- "여백 먼저"가 원칙이지만, 첫 진입/설정/폼/선택 상태에서는 컨테이너(경계선, 박스)가 필요할 수 있다

#### 빠른 판단 기준

- 자식 요소에 `mb-4`가 반복되면 부모의 `gap-4`로 교체한다
- 구분선이나 박스를 너무 많이 쓰고 있다면 여백만으로 분리할 수 있는지 먼저 확인한다
- 단, 사용자가 구조를 처음 보는 화면이라면 여백만으로는 구조가 불분명할 수 있다 — 컨테이너를 먼저 검토한다
- 모바일에서 간격이 부족해 보이면 생각보다 더 넓은 여백이 필요하다
- 텍스트와 아이콘이 시각적 중앙에서 어긋나 보이면 optical correction이 필요하다

→ 상세: [references/03-spacing-system.md](references/03-spacing-system.md)

### 4. 시각적 계층으로 시선을 유도한다

사용자의 시선은 크기 → 두께 → 색상(명도) → 위치 순으로 흐른다. 이를 의도적으로 설계해야 한다.

- 가장 중요한 텍스트에 100% 또는 87% 불투명도, 중간 중요도는 60~70%, 보조 정보는 45% 이하로 낮춘다
- 주요 동작(Primary) 버튼 하나에만 배경색을 넣고, 보조 버튼은 테두리만 또는 배경 없이 처리한다
- 덜 중요한 정보(파일 크기, 날짜, 메타데이터)는 짙은 회색으로 시각적 우선순위를 낮춘다
- 버튼의 Hover/Active/Disabled 상태를 색상 변화로 명확히 구분한다
- 모든 요소에 각기 다른 색을 쓰면 시선이 분산된다 — 강조는 최소화한다

#### 빠른 판단 기준

- 헤드라인과 본문의 시각적 차이가 크기뿐이면 두께와 불투명도를 함께 조정한다
- 모든 버튼에 배경색이 있으면 Primary 하나만 남기고 나머지를 줄인다
- 중요한 수치와 보조 메타데이터가 같은 시각적 강도를 갖고 있으면 불투명도로 분리한다

→ 상세: [references/04-visual-hierarchy.md](references/04-visual-hierarchy.md)

### 5. 깊이감과 질감으로 공간감을 만든다

평면적인 화면에 물리적 공간감을 부여하면 인터페이스가 더 자연스럽고 몰입감 있게 느껴진다.

- 순백색(#FFFFFF) 대신 미세한 Off-white 캔버스를 활용해 눈의 피로를 줄이고 다른 요소와의 대비를 입체적으로 만든다
- 배경에 미세한 노이즈 텍스처를 추가하면 입체감과 전체적인 응집력(Cohesion)이 생기지만, 메인 요소를 방해하지 않도록 극히 미세하게 적용한다
- 그림자는 X ≤ Y, Blur = Y × 1.3~2, 불투명도 15~20%가 자연스러운 기본값이다
- 겹겹이 쌓이는 요소에는 Offset backplate(어긋난 배경 판)를 활용해 평면적이면서도 깊이감 있는 계층을 구성할 수 있다
- 잘못 쓴 그림자와 그라데이션은 없는 것보다 나쁘다 — 확신이 없으면 제거한다
- 글래스모피즘(반투명 + blur + 1px 테두리 + 내부 그림자)은 고급스러운 유리 느낌을 준다
- 시각적 라이밍(Visual Rhyming): 로고의 도형, 색상, 텍스처를 다른 요소에 반복해서 사이트 전체의 통일감을 높인다

#### 빠른 판단 기준

- 배경이 완전히 쨍한 흰색이라면 약간의 색온도가 들어간 Off-white나 극미세 노이즈 텍스처를 검토한다
- 그림자가 피그마 기본값 그대로라면 불투명도를 낮추고 블러를 높여 자연스럽게 만든다
- 그라데이션이 조잡해 보이면 같은 색상의 명도 차이만으로 바꾸거나 제거한다
- 깊이감 요소가 시각적 주인공(Star of the Show)을 가리고 있으면 제거를 먼저 검토한다

→ 상세: [references/05-depth-texture.md](references/05-depth-texture.md)

### 6. 절제와 일관성으로 완성도를 높인다

화려한 기술보다 절제된 일관성이 더 전문적인 결과물을 만든다.

- 아이콘은 하나의 라이브러리(Lucide, Phosphor, Feather 등)에서 통일된 스타일로 사용한다
- 선택된(Active) 상태와 기본 상태는 외곽선(Outline)과 채움(Filled) 스타일 혹은 명확한 대비를 통해 시각적으로 즉각 분리한다
- 여러 스타일의 아이콘을 섞거나 이모지를 대체로 쓰면 전문성이 떨어진다
- 정형화된 UI에 대비를 주고자 할 때만 핸드드로잉 형태의 액센트나 마크를 의도적으로 사용한다
- 마스코트나 일러스트레이션은 단발성이 아니라, 상태와 시나리오(성공, 에러, 로딩 등)에 맞춰 변형할 수 있는 시스템으로 접근한다
- 디자인이 막혔을 때는 수정보다 전체를 반전(다크/라이트, 레이아웃 뒤집기)시켜보는 시도가 효과적이다
- 화면 전체를 채울 필요 없다 — 적은 것으로 더 많이 보여주는(Less is More) 접근이 결과적으로 더 사용성이 높다
- 간격, 모서리 곡률, 색상에 변수(Variables)를 사용해 통일성을 유지한다

#### 빠른 판단 기준

- 서로 다른 스타일의 아이콘이 한 화면에 섞여 있다면 하나의 라이브러리로 통일한다
- active 상태를 색만으로 구분하고 있다면 filled/outline 같은 형태 언어를 함께 검토한다
- 화면에 요소가 많아 복잡해 보이면 "없어도 되는 것"부터 지우고 시작한다
- 손그림 액센트나 마스코트가 포인트를 넘어서 화면의 주인공이 되고 있으면 줄인다
- 모서리 곡률이 컴포넌트마다 다르면 하나의 값으로 통일한다

→ 상세: [references/06-design-craft.md](references/06-design-craft.md)

---

## references 가이드

아래 문서는 실제 시각 디자인 결정을 내리기 전 직접 읽어야 하는 구현 가이드다. 작업 성격에 따라 필요한 reference를 먼저 읽고 판단한다.

| 파일                                                                   | 읽을 때                                                                                                                                                     |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [references/01-color-system.md](references/01-color-system.md)         | 색상 팔레트, 중립색, 액센트, 시맨틱 컬러, 다크모드 색상, OKLCH, 컬러 램프를 설계할 때                                                                       |
| [references/02-typography.md](references/02-typography.md)             | 폰트 조합, 앵커 폰트, 커스텀 폰트 리서치, 타이포 아트 디렉션, line-height, fluid typography를 결정할 때                                                     |
| [references/03-spacing-system.md](references/03-spacing-system.md)     | 스페이싱 스케일, rem 기반 간격, 그룹화/분리, inner/outer, optical correction, relationship strength, exponential scaling, 컨테이너 vs 여백 분기를 설계할 때 |
| [references/04-visual-hierarchy.md](references/04-visual-hierarchy.md) | 텍스트 불투명도, 버튼 우선순위, 상태 색상, 강조 절제를 판단할 때                                                                                            |
| [references/05-depth-texture.md](references/05-depth-texture.md)       | 그림자, 오프화이트 캔버스, 노이즈 텍스처, offset backplate, 글래스모피즘을 적용할 때                                                                        |
| [references/06-design-craft.md](references/06-design-craft.md)         | 아이콘 상태 언어, hand-drawn accent, 마스코트 시스템, 절제와 일관성을 검토할 때                                                                             |

### 추천 로드 순서

- 전체 시각 디자인 리뷰: `01 → 04 → 03 → 02`
- 색상 시스템 설계: `01 → 04 → 05`
- 타이포그래피와 계층: `02 → 04 → 03`
- 세부 품질 개선: `05 → 06 → 04`

---

## 범위

- 프로덕트 UX 흐름, CTA, 로딩, 피드백, 확인 → `ds-product-ux`
- UI 레이아웃 패턴, 대시보드, SaaS 섹션 구성 → `ds-ui-patterns`
- 모션의 물리감, swipe choreography, high-risk interaction policy → `ds-product-ux` 또는 `ds-ui-patterns`
- Tailwind CSS 토큰, 유틸리티, className 병합 → `fe-tailwindcss`
- 구현 수준의 접근성, ARIA, 키보드, 시맨틱 HTML → `fe-a11y`
- 공유 UI 컴포넌트 API, 디자인 시스템 아키텍처 → `fe-ui-element-components`
