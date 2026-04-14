---
name: writing-design-prompt
description: "Design prompt authoring and refinement for Designer agent handoff, reference-to-prompt translation, and preserve-without-drift framing. Use when translating design direction, research evidence, or vague UI ideas into clear, specific, well-structured design prompts or briefs. Always consult for Designer handoff wording, reference-to-prompt translation, design brief sharpening, or preserve-without-drift framing, even if the user only asks to write design context, sharpen a brief, structure a visual request, or polish a prompt before sending to Designer. For screen/flow reference research use research-design. For final visual system rules use ds-visual-design. For layout composition use ds-ui-patterns. For implementation use fe-*. Triggers on: design prompt, prompt refinement, Designer handoff, design brief, reference-to-prompt, preserve-without-drift, vague UI idea, sharpen brief, design direction, 디자인 프롬프트, 프롬프트 작성, 디자이너 핸드오프, 디자인 브리프, 프롬프트 다듬기, 디자인 방향 정리."
---

# Design Prompt 작성과 정제

## 목표

모호한 UI 아이디어, research evidence, 기존 디자인 맥락을 구체적이고 구조화된 디자인 프롬프트나 brief로 변환한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 작업을 시작하기 전에는 아래 reference 문서를 직접 읽고 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

이 스킬의 결과물은 design spec의 대체물이 아니다. 디자인 프롬프트와 brief의 입력 품질을 높이는 것이 역할이다. final design decision은 Designer agent와 각 ds-* owner skill이 내린다.

---

## 핵심 패턴

### 1. Assess & Fill — 프롬프트 완성도 체크

프롬프트를 작성하거나 정제할 때 아래 6요소가 충분한지 먼저 평가한다. 누락된 요소는 맥락에서 추론하거나 보완한다.

| 요소 | 확인 | 누락 시 |
| --- | --- | --- |
| **Platform** | web, mobile, desktop | 맥락에서 추론하거나 명시적으로 추가 |
| **Surface type** | landing page, dashboard, form, modal, flow | 설명에서 유추하거나 질문 |
| **Structure** | section 구분, component 나열 | logical page structure 생성 |
| **Visual style** | vibe 형용사, mood | 적절한 형용사 조합 추가 |
| **Colors** | hex, role, descriptive name | 기존 design system에서 추출하거나 제안 |
| **Components** | UI 키워드 | 모호한 표현을 UI/UX 키워드로 변환 |

#### 빠른 판단 기준

- 6요소 중 3개 이상 빠져 있으면 프롬프트가 아직 rough 상태다
- platform과 surface type이 빠져 있으면 나머지를 보완해도 방향이 흔들린다
- 이미 프로젝트 style guide(DESIGN.md, theme config 등)가 있으면 거기서 대부분의 답을 먼저 추출한다

### 2. Vague → Specific — 모호한 표현을 정밀 키워드로 변환

일상적인 표현을 UI/UX 키워드로 번역하면 프롬프트의 해석 정확도가 올라간다.

| 모호한 표현 | 구체적 키워드 |
| --- | --- |
| "위에 메뉴" | navigation bar with logo and menu items |
| "버튼" | primary call-to-action button |
| "목록" | card grid layout 또는 vertical list with thumbnails |
| "입력 칸" | form with labeled input fields and submit button |
| "사진 영역" | hero section with full-width image |
| "모던한" | clean, minimal, with generous whitespace |
| "프로페셔널한" | sophisticated, trustworthy, with subtle shadows |
| "재미있는" | vibrant, playful, with rounded corners and bold colors |
| "다크 모드" | dark theme with high-contrast accents on deep backgrounds |

#### 빠른 판단 기준

- "느낌적인 느낌" 수준의 형용사만 있으면 vibe amplification이 필요하다
- component를 일상어로만 적었으면 UI 키워드로 번역해야 한다
- 형용사 1개보다 2~3개 조합이 방향을 더 정확하게 잡는다

상세 키워드와 형용사 팔레트는 [keywords.md](references/keywords.md)를 먼저 읽고 활용한다.

### 3. Design Context Injection — 기존 디자인 맥락 주입

프롬프트에 기존 디자인 시스템, theme token, local component language를 주입하면 결과물의 일관성이 유지된다.

#### 프로젝트 style guide(DESIGN.md)가 있을 때

1. style guide에서 color palette, typography rules, layout grammar, component stylings를 추출한다
2. 프롬프트에 design context block으로 포함시킨다
3. preserve-without-drift 항목을 명시한다

DESIGN.md는 프로젝트 전역의 visual identity와 design system을 정의하는 스타일 가이드 문서다. Designer agent의 per-task `design.md`(DESIGN-TEMPLATE 기반)와는 역할과 범위가 다르다. DESIGN.md의 작성 구조와 섹션별 가이드는 [design-md.md](references/design-md.md)를 읽고 활용한다.

#### 프로젝트 style guide(DESIGN.md)가 없을 때

1. existing UI의 theme token, global style, component language를 먼저 확보한다
2. 확보한 evidence를 design context block으로 정리한다
3. 이 evidence가 프롬프트의 visual constraint로 작용하게 한다
4. 프로젝트 전체에 일관된 디자인 시스템이 필요하면 DESIGN.md를 먼저 작성하는 것을 권장한다. 작성 방법은 [design-md.md](references/design-md.md)를 따른다.

#### Design context block 구조

```markdown
**Design Context:**
- Platform: {Web/Mobile}, {Desktop/Mobile}-first
- Theme: {Light/Dark}, {style descriptors}
- Palette: {Descriptive Name} ({#hex}) — {functional role}
- Typography: {heading family} / {body family}, {scale range}
- Layout: {grid system}, {max-width}, {spacing scale}
- Existing tone: {보존해야 할 현재 분위기}
```

#### 빠른 판단 기준

- multi-page, multi-screen 작업이면 design context injection이 사실상 필수다
- component 하나만 수정하는 작업이라도 기존 palette와 radius를 무시하면 drift가 생긴다
- color를 적을 때는 반드시 `Descriptive Name (#hex) — functional role` 형식을 쓴다

### 4. Reference → Brief Translation — evidence를 Designer brief로 압축

research-design에서 나온 candidate decisions, steal list, pattern table 같은 evidence를 Designer가 바로 해석할 수 있는 brief로 압축하는 패턴이다.

#### 번역 순서

1. **Evidence 분류**: research output에서 structure, surface facts, product logic으로 분류된 항목을 확인한다
2. **Direction 문장 변환**: candidate decision마다 "무엇을 왜 어떻게" 한 줄로 압축한다
3. **Design spec 영역 매핑**: 각 direction이 design spec의 어떤 영역(identity, color, typography, layout, flow 등)에 해당하는지 태그한다
4. **Open questions 보존**: 아직 결정되지 않은 trade-off는 숨기지 않고 brief에 남긴다

#### 변환 예시

| Research evidence | Designer brief |
| --- | --- |
| "Clay: 7-step cancellation, `25% OFF FOR LIFE` retention offer" | Retention offer는 permanence framing 적용. 할인의 지속성을 시각적으로 강조. → signature component 영역 |
| "ElevenLabs: feature thumbnails in loss screen" | Feature loss는 텍스트 나열이 아닌 구체적 visual treatment. → page structure + user flow 영역 |
| "Multi-select vs single-select reason collection" | Reason collection은 multi-select checkbox 우선 검토. 최종 결정은 Designer. → user flow 영역 |

#### 빠른 판단 기준

- evidence를 그대로 복붙하면 brief가 아니라 research dump가 된다
- direction 문장에 source와 rationale이 빠지면 Designer가 맥락을 잃는다
- design spec 영역 태그가 있으면 결과물에서 어디에 반영할지 바로 찾을 수 있다
- trade-off를 caller가 미리 단일 답으로 합쳐 버리면 Designer의 판단 여지가 사라진다

상세 프롬프트 anatomy와 요소별 specificity 패턴은 [prompt-anatomy.md](references/prompt-anatomy.md)를 읽고 활용한다.

### 5. Preserve-without-Drift Framing — 정체성 보존 프레이밍

기존 디자인 정체성을 유지하면서 변경 surface만 명확히 여는 프레이밍 패턴이다. 특히 existing surface refinement이나 incremental update에서 중요하다.

#### 프레이밍 구조

```markdown
**Preserve (do not change):**
- {유지할 color token, typography, spacing, component language}
- {유지할 tone, visual identity, interaction pattern}

**Allowed change surface:**
- {이번에 바꾸는 구체적인 영역과 범위}

**Anti-drift rule:**
- {도입하면 안 되는 새로운 visual pattern이나 deviation}
```

#### 빠른 판단 기준

- existing surface를 다루면 preserve 항목이 없는 프롬프트는 미완성이다
- "기존 느낌 유지"는 preserve가 아니다. 어떤 token, pattern, value를 유지하는지 구체화해야 한다
- allowed change surface가 넓을수록 anti-drift rule이 더 구체적어야 한다
- net-new surface라도 기존 제품의 design language가 있으면 최소한의 preserve를 설정한다

### 6. Incremental Refinement — 점진적이고 정밀한 변경

한 번에 하나의 변경에 집중하고, 변경 대상을 삼중으로 특정한다.

#### Targeting 삼중 구조

변경을 지시할 때 세 가지를 함께 특정한다.

1. **위치**: 어떤 화면, 어떤 section, 어떤 component
2. **대상**: 해당 위치 안의 구체적인 element
3. **변경**: 무엇을 어떻게 바꾸는지

#### 예시

```markdown
**Specific changes:**
- Location: Header navigation, right side before user avatar
- Target: Search input
- Change: Pill-shaped, subtle gray background (#f3f4f6), magnifying glass icon on left, 240px default → 320px on focus with subtle shadow

**Context:** This is a targeted edit. Make only this change while preserving all existing elements.
```

#### 빠른 판단 기준

- "검색바 추가해줘"는 위치·대상·변경 중 2개가 빠져 있다
- 여러 변경을 하나의 프롬프트에 묶으면 결과 추적이 어렵다
- "preserving all existing elements" 같은 context 문구가 drift를 줄인다
- 복잡한 page 전체를 한 번에 요청하는 것보다 section별로 나눠 refinement하는 것이 정확도가 높다

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/keywords.md](references/keywords.md) | UI/UX component 키워드, adjective palette, color role, shape, motion/easing 용어를 확인할 때 |
| [references/prompt-anatomy.md](references/prompt-anatomy.md) | 프롬프트 전체 구조, high-level↔detailed 시작점 선택, section structuring, color·typography·layout·image specificity 패턴, theme coordination, anti-pattern 체크리스트를 확인할 때 |
| [references/design-md.md](references/design-md.md) | 프로젝트 전역 스타일 가이드인 DESIGN.md를 작성할 때 — DESIGN.md vs design.md 구분, 9-section 표준 구조, 섹션별 작성 지침, analysis 방법론, 예시 참조 |

---

## 범위

- 이 스킬은 design prompt authoring, refinement, reference-to-prompt translation, preserve-without-drift framing의 owner다.
- 프로젝트 전역 스타일 가이드인 DESIGN.md 작성 방법론은 이 스킬의 reference(`references/design-md.md`)가 다룬다.
- per-task design spec(`design.md`) 작성과 final design decision은 Designer agent가 owner다. Designer agent는 DESIGN-TEMPLATE.md를 따른다.
- screen/flow reference research는 research-design이 owner다.
- final color, visual polish, Anti-AI-Slop rule은 ds-visual-design이 owner다.
- layout composition는 ds-ui-patterns가 owner다.
- typography rule은 ds-typography가 owner다.
- trust, CTA, objection handling, UX flow는 ds-product-ux가 owner다.
- implementation, accessibility, Tailwind, component API는 fe-*가 owner다.
