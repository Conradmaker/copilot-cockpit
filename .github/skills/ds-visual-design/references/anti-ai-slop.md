# Anti-AI-Slop

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 문서는 시각 디자인이 "AI가 평균값을 안전하게 뽑아낸 결과"처럼 보일 때 나타나는 경고 신호와, 이를 걸러내는 품질 게이트를 모아둔 reference다.

여기서 다루는 것은 visual-level smell이다. 레이아웃 cliché와 section order cliché의 최종 owner는 `ds-ui-patterns`지만, 그 냄새가 시각적으로 어떻게 드러나는지는 여기서 먼저 검토한다.

---

## 1. 가장 강한 신호: 근거 없는 Indigo와 Violet

AI가 만든 화면은 이유 없이 indigo나 violet 계열 accent에 수렴하는 경우가 많다. 안전하고 현대적으로 보인다는 이유만으로 고르면, 결과는 빠르게 generic해진다.

### 경고 신호

- brand와 무관한 `#6366f1`, `#8b5cf6`, `#7c3aed` 계열 accent
- reference나 product tone 설명 없이 "그냥 좋아 보여서" 선택한 purple 계열
- 다른 visual choice는 비어 있는데 accent만 AI default처럼 보이는 상태

### 빠른 대안

- 신뢰와 안정: blue 계열
- 신선함과 구분감: teal 계열
- 진짜 brand tone: reference에서 나온 고유 accent

### 판단 기준

- 왜 purple인지 설명 못하면 다시 고른다
- 색을 바꾸면 화면 정체성이 바로 무너지면 원래 정체성이 없던 것이다

---

## 2. Generic해 보이는 증상

### 타이포그래피

- 이유 없이 모두 같은 weight
- display와 body의 역할 분리가 없음
- 작은 텍스트와 ALL CAPS에서 letter-spacing 조정이 없음
- "무난한 시스템 폰트"만 쓰고 tone이 비어 있음

### 색상

- accent hierarchy가 없음
- gradient가 기능이 아니라 분위기만 흉내 냄
- 모든 색이 고르게 분산돼 시선 우선순위가 흐림
- brand meaning보다 safety를 우선한 palette

### 레이아웃과 시각 리듬

- 완벽한 대칭만 반복됨
- hero left text + right image 같은 template가 이유 없이 재생산됨
- card grid가 정보 구조가 아니라 습관처럼 배치됨
- 화면 전체가 안전하지만 기억점이 없음

### 디테일

- 의미 없는 blob background
- 아무 product에도 붙을 수 있는 stock visual
- hierarchy를 돕지 않는 shadow와 effect
- 다듬지 않은 micro-detail 때문에 전체가 template처럼 보임
- 모든 heading 위에 큰 둥근 아이콘을 반복 배치
- hero 영역에 "큰 숫자 + 작은 라벨" metric layout template
- 장식용 sparkline (실제 데이터 없이 분위기만)
- 모달을 남용 — 진짜 필요한 경우가 아니면 inline으로 해결
- glassmorphism을 모든 곳에 적용 — 한두 곳의 의도된 사용만 유효

---

## 3. 의도된 선택으로 되돌린다

Anti-AI-Slop의 핵심은 더 화려하게 만드는 것이 아니라, 각 선택의 이유를 복원하는 것이다.

### Typography with purpose

- reference와 tone에 맞는 font를 고른다
- hierarchy는 size만이 아니라 weight, spacing, opacity로 만든다
- 작은 텍스트와 label까지 포함해 type system을 끝까지 본다

### Color with meaning

- palette는 brand와 reference evidence에서 시작한다
- dominant neutral + intentional accent 구조를 만든다
- semantic color를 장식이 아니라 의미로 사용한다

### Layout with intention

- asymmetry와 whitespace를 정보 구조에 맞게 쓴다
- 시선을 어디로 보낼지 설명할 수 없는 구성은 다시 짠다
- template를 그대로 복제하지 않고 왜 이 순서와 왜 이 구성을 택했는지 적는다

### Details that distinguish

- hierarchy를 돕는 shadow와 depth만 남긴다
- 브랜드 성격을 드러내는 작은 detail을 의도적으로 만든다
- screenshot 한 장으로도 기억나는 visual decision을 최소 하나 둔다

### 구현 전 방향 고정

generic한 결과가 나오는 원인은 대부분 "방향이 없었다"는 것이다. 구현 전에 아래 4가지를 먼저 고정하면 default 수렴을 막을 수 있다.

- **Purpose**: 이 제품/화면이 사용자에게 주는 핵심 가치
- **Tone**: 전달해야 하는 감정/분위기 — "현대적" 같은 추상적 형용사 대신 reference 이미지나 구체적 제품 예시로 고정
- **Constraints**: 기술 제약, 브랜드 제약 — 이 제약이 오히려 결정을 날카롭게 만듦
- **Differentiation**: "같은 카테고리의 다른 제품과 이 화면이 다른 점은 무엇인가?" — 대담함이 아니라 정확성에서 차별점이 나온다

---

## 4. Anti-AI-Slop 체크리스트

- [ ] accent color가 indigo/violet default처럼 보이지 않는가
- [ ] ALL CAPS와 small text에 필요한 letter-spacing이 있는가
- [ ] screenshot test에서 기억나는 visual decision이 최소 하나 있는가
- [ ] font choice가 reference와 tone에 기반해 설명 가능한가
- [ ] palette가 default가 아니라 product meaning에서 나왔는가
- [ ] visual tension이나 hierarchy가 template보다 먼저 읽히는가
- [ ] generic pattern을 그대로 쓴 부분에 대해 justification이 있는가

---

## 5. Safe와 Intentional을 구분한다

"다들 이렇게 하니까"는 quality signal이 아니라 평균 회귀일 수 있다.

### Safe

- 3-column pricing grid를 이유 없이 반복
- hero left text + right image를 관성적으로 사용
- equal card grid를 기본값으로 두고 끝냄

### Intentional

- product tier 수에 맞춰 2-column pricing을 선택
- brand tone 때문에 full-width visual hero를 선택
- 시선 흐름을 위해 asymmetrical composition을 선택

### 질문

> "이 선택을 이 프로젝트 맥락에서 왜 했는가?"

이 질문에 답할 수 없으면, 더 독특하게 만들기 전에 먼저 더 정확하게 만들어야 한다.