# DESIGN.md 작성 가이드

프로젝트 전역의 visual identity와 design system을 하나의 마크다운 문서로 정리하는 방법론이다. DESIGN.md는 프로젝트의 디자인 시스템 source of truth로서, 새 화면을 만들거나 기존 화면을 수정할 때 visual language 일관성을 유지하는 전역 스타일 가이드 역할을 한다.

---

## DESIGN.md vs design.md 구분

이 두 문서는 이름이 비슷하지만 역할과 범위가 다르다.

| | DESIGN.md (프로젝트 전역 스타일 가이드) | design.md (per-task 디자인 spec) |
| --- | --- | --- |
| **위치** | 프로젝트 루트 또는 `ref/` | `/memories/session/design.md` |
| **범위** | 프로젝트 전체의 visual identity, color palette, typography, component language, layout principles | 특정 PRD/surface의 디자인 구체화 (화면 구조, UX flow, interaction, state) |
| **성격** | 재사용 가능한 디자인 시스템 문서 — 새 화면을 만들 때마다 참조하는 global source of truth | 일회성 design spec — approved PRD를 visual/UX/interaction decision으로 확장 |
| **구조** | 9-section 표준 (이 문서가 다루는 범위) | DESIGN-TEMPLATE.md의 14-section 구조 |
| **관계** | design.md(per-task)가 DESIGN.md(전역)를 existing tone evidence와 hard constraint로 참조해 일관성을 유지 | DESIGN.md의 palette, typography, component language를 baseline으로 사용 |
| **작성 주체** | 프로젝트 초기 또는 디자인 시스템 정리 시점에 작성 | Designer agent가 approved PRD를 기반으로 작성 |

### 핵심 관계

- DESIGN.md가 먼저 존재하면, per-task `design.md`는 DESIGN.md의 color, typography, spacing, component language를 hard constraint로 다루고 deviation은 rationale을 명시한다.
- DESIGN.md가 없는 프로젝트에서는 기존 UI의 theme token, global style, component language를 분석해 DESIGN.md를 먼저 작성하고 나서 per-task design work를 진행하는 것이 일관성에 유리하다.
- writing-design-prompt의 Design Context Injection 패턴에서 "프로젝트 style guide(DESIGN.md)가 있을 때"라고 언급하는 문서가 바로 이 DESIGN.md다.

---

## DESIGN.md의 목적

1. **디자인 프롬프트의 source of truth**: AI agent가 새 화면을 생성할 때 DESIGN.md를 읽고 기존 디자인 언어에 맞는 결과를 만든다.
2. **Visual language 일관성 유지**: color palette, typography, component styling, layout principles를 한 곳에 잠가서 화면 간 시각적 일관성을 보장한다.
3. **Design context injection의 원천**: 디자인 프롬프트에 design context block을 작성할 때 DESIGN.md에서 값을 추출한다.
4. **팀 커뮤니케이션 도구**: 디자이너, 개발자, AI agent가 동일한 디자인 vocabulary를 공유한다.

---

## 9-Section 표준 구조

17개 실제 프로젝트 DESIGN.md 분석 결과, 아래 9-section 구조가 표준이다.

| Section | 이름 | 역할 |
| --- | --- | --- |
| 1 | Visual Theme & Atmosphere | 전체 분위기, 미학적 방향, 핵심 시각적 특성 |
| 2 | Color Palette & Roles | 색상 시스템과 각 색상의 기능적 역할 |
| 3 | Typography Rules | 폰트 패밀리, 위계, weight, spacing 규칙 |
| 4 | Component Stylings | 버튼, 카드, 입력, 네비게이션 등 컴포넌트별 스타일 |
| 5 | Layout Principles | 그리드, 간격, 반응형 전략, 공간 활용 |
| 6 | Depth & Elevation | 그림자, 레이어, 깊이감 전략 |
| 7 | Do's and Don'ts | 이 디자인 시스템에서 허용되는 것과 금지되는 것 |
| 8 | Responsive Behavior | 브레이크포인트, 터치 타겟, 축소 전략 |
| 9 | Agent Prompt Guide | AI agent용 빠른 참조와 컴포넌트 프롬프트 예시 |

Section 1-5는 필수이고, Section 6-9는 comprehensive한 디자인 시스템 문서에서 권장된다. 간단한 프로젝트라면 1-5만으로도 유효하다.

---

## 섹션별 작성 가이드

### Section 1: Visual Theme & Atmosphere

전체 디자인의 분위기, 밀도, 미학적 철학을 서술한다. technical spec이 아니라 디자인의 "성격"을 잡는 섹션이다.

**포함할 것:**
- 전체 분위기를 잡는 자연어 묘사 (예: "sophisticated, minimalist sanctuary", "warm, unhurried, intellectual")
- 핵심 시각 특성 3-6개를 Key Characteristics로 정리
- 어떤 감정이나 인상을 주는지, 왜 이 방향인지

**작성 원칙:**
- 단순히 "모던하다", "깔끔하다" 수준의 형용사로 끝내지 않는다. 이 디자인만의 distinctive한 특징을 구체적으로 서술한다.
- 기술적 구현과 시각적 효과를 함께 연결한다. 예: "negative letter-spacing (-2.4px at display sizes) creating headlines that feel compressed and engineered"
- 비유와 물리적 묘사를 활용한다. 예: "floating in a twilight sky", "premium print publication", "literary salon reimagined as a product page"

**판단 기준:**
- 이 섹션만 읽어도 "아, 이런 느낌의 디자인이구나"가 바로 잡히는가
- Key Characteristics 리스트가 실제 구현 가능한 수준의 구체성을 갖고 있는가
- generic한 묘사(clean, modern, minimal)만 나열하지 않고 이 프로젝트만의 signature가 드러나는가

### Section 2: Color Palette & Roles

색상 시스템을 정의한다. 단순 hex 나열이 아니라 각 색상의 기능적 역할과 사용 맥락을 함께 적는다.

**포함할 것:**
- Primary / Brand 색상
- Accent / Interactive 색상
- Neutral / Text hierarchy 색상
- Surface / Background 색상
- Semantic 색상 (success, error, warning)
- Border / Shadow 색상 (해당될 때)
- Gradient 전략 (있다면 명시, 없다면 "gradient-free" 같은 명시적 선언)

**색상 작성 포맷:**
```
- **Descriptive Name** (`#hex`) — functional role. 사용 맥락과 이유.
```

예시:
```
- **Deep Muted Teal-Navy** (`#294056`) — primary CTA, active navigation. 차분하면서도 신뢰감 있는 유일한 accent.
- **Warm Barely-There Cream** (`#FCFAFA`) — page background. 순수 화이트보다 미세하게 따뜻한 기본 캔버스.
```

**작성 원칙:**
- "blue"나 "gray" 같은 generic 이름 대신 색상의 성격을 담은 descriptive name을 사용한다.
- hex 코드는 항상 포함한다. descriptive name만으로는 정확한 재현이 불가능하다.
- functional role을 반드시 적는다. 같은 회색이라도 "primary text"와 "secondary text"와 "border"는 역할이 다르다.
- rgba 또는 hsla 값이 중요한 경우(shadow color, overlay 등) 함께 적는다.

**판단 기준:**
- 모든 색상에 descriptive name + hex + functional role이 있는가
- palette의 역할 분담이 명확한가 (background, text, accent, interactive, semantic)
- 이 palette만으로 전체 UI를 일관되게 렌더링할 수 있는가

### Section 3: Typography Rules

폰트 패밀리, 위계, weight 전략, spacing 규칙을 정의한다.

**포함할 것:**
- Font family와 fallback chain
- OpenType feature 사용 여부 (liga, tnum, ss01 등)
- 역할별 hierarchy table (Display, Heading, Sub-heading, Body, Caption, Code 등)
- Typography principles (weight 전략, tracking 전략, line-height 전략)

**Hierarchy table 포맷:**

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Display Hero | {font} | {px (rem)} | {number} | {ratio} | {px or em} | {특이사항} |

**작성 원칙:**
- size는 px와 rem을 병기한다.
- weight는 형용사(bold, light)가 아니라 숫자(300, 400, 600)로 적는다.
- letter-spacing은 tight/generous 같은 형용사 대신 구체적 px 또는 em 값을 적는다.
- line-height은 비율(1.10, 1.50, 1.60)로 적는다.
- Principles 섹션에서 이 typography system의 distinctive한 전략을 설명한다. 예: "Weight 300 as the signature headline weight — light, confident, anti-convention"

**판단 기준:**
- hierarchy table에서 모든 역할의 size, weight, line-height, letter-spacing이 구체적 값으로 채워져 있는가
- font family의 fallback chain이 명시되어 있는가
- 이 typography system만의 signature(distinctive typography choice)가 Principles에 드러나는가

### Section 4: Component Stylings

주요 UI 컴포넌트의 시각적 스타일을 정의한다.

**포함할 것:**
- Buttons (primary, secondary, ghost, disabled — shape, color, padding, radius, hover/focus state)
- Cards / Containers (background, border, radius, shadow, hover behavior)
- Inputs / Forms (border, focus state, placeholder, padding)
- Navigation (layout, typography, active/hover state, mobile treatment)
- Badges / Tags / Pills (해당될 때)
- 기타 프로젝트 특화 컴포넌트

**작성 원칙:**
- 기술 값(border-radius, padding px)과 자연어 묘사를 함께 적는다. 예: "Gently rounded corners (12px/0.75rem)"
- hover, focus, active, disabled 같은 interaction state를 빠뜨리지 않는다.
- transition/animation이 있으면 duration과 easing을 구체적으로 적는다.

**판단 기준:**
- 주요 컴포넌트(button, card, input, navigation)가 모두 다뤄졌는가
- state별(default, hover, focus, active, disabled) 스타일이 정의되었는가
- 값이 구체적이어서 바로 구현 가능한 수준인가

### Section 5: Layout Principles

그리드, 간격, 공간 전략, 반응형 기초를 정의한다.

**포함할 것:**
- Grid system (column count, gutter size, max-width)
- Spacing scale 또는 base unit
- Section spacing (vertical padding between major sections)
- Container/wrapper rules
- Alignment principles

**작성 원칙:**
- "generous spacing" 같은 형용사로 끝내지 않고 px 또는 rem 값으로 잠근다.
- max-width, gutter, section padding은 desktop과 mobile 값을 함께 적는다.

**판단 기준:**
- grid system이 column count, gutter, max-width로 정의되어 있는가
- spacing이 구체적 숫자로 잠겨 있는가
- 이 layout만의 distinctive한 공간 전략이 드러나는가

### Section 6: Depth & Elevation

그림자, 레이어링, 깊이감 전략을 정의한다.

**포함할 것:**
- Elevation level별 shadow 정의 (flat, subtle, card, elevated, modal 등)
- Shadow philosophy (multi-layer compositing, shadow-as-border, flat 등)
- Border와 shadow의 관계 (shadow가 border를 대체하는지 등)
- Decorative depth (gradient, glow, blur 유무)

**작성 원칙:**
- shadow 값은 full CSS 값으로 적는다. 예: `rgba(50,50,93,0.25) 0px 30px 45px -30px`
- shadow의 색상에 브랜드 톤이 반영되어 있으면 그 이유를 설명한다.
- "flat" 또는 "no shadows"도 의도적인 design decision이므로 명시한다.

**판단 기준:**
- elevation이 level별로 구분되어 있는가
- shadow 값이 재현 가능한 수준으로 구체적인가
- depth 전략의 철학이 서술되어 있는가

### Section 7: Do's and Don'ts

디자인 시스템의 사용 경계를 명확히 한다.

**포함할 것:**
- Do: 이 디자인 시스템을 쓸 때 반드시 따라야 하는 규칙 (4-8개)
- Don't: 이 디자인 시스템에서 금지되는 패턴 (3-6개)

**작성 원칙:**
- 구체적으로 적는다. "깔끔하게 유지하세요"가 아니라 "Use Cal Sans exclusively for headings (24px+) and never for body text"
- 실제로 실수하기 쉬운 항목을 중심으로 적는다.
- color, typography, spacing, component 사용의 hard boundary를 잡는다.

**판단 기준:**
- Do/Don't가 구체적인 property와 패턴 수준으로 작성되었는가
- 이 디자인 시스템을 처음 접하는 사람이 실수를 예방할 수 있는가

### Section 8: Responsive Behavior

브레이크포인트, 축소 전략, 터치 타겟을 정의한다.

**포함할 것:**
- Breakpoint table (name, width range, key changes)
- Touch target rules
- Collapsing strategy (navigation, hero, grid, spacing의 반응형 변화)
- Image behavior (responsive scaling, art direction 여부)

**작성 원칙:**
- breakpoint는 table 포맷으로 정리한다.
- 각 breakpoint에서 무엇이 바뀌는지 구체적으로 적는다.

### Section 9: Agent Prompt Guide

AI agent가 이 디자인 시스템을 적용할 때 빠르게 참조할 수 있는 가이드다.

**포함할 것:**
- Quick Color Reference (가장 자주 쓰는 색상 5-8개의 이름과 hex)
- Example Component Prompts (이 디자인 시스템에 맞는 컴포넌트 생성 프롬프트 3-5개)
- Iteration Guide (기존 화면을 수정할 때 체크해야 할 항목 3-5개)

**작성 원칙:**
- Example Component Prompts는 실제로 AI에게 줄 수 있는 형태로 적는다. 구체적인 hex, px, weight, radius 값을 포함한다.
- Iteration Guide는 "이 디자인 시스템다운가?"를 체크하는 최소 항목으로 구성한다.

**판단 기준:**
- Quick Color Reference만 보고 주요 색상을 바로 쓸 수 있는가
- Example Component Prompts가 실행 가능한 수준으로 구체적인가
- Iteration Guide가 디자인 시스템의 핵심 identity를 보호하는가

---

## Analysis 방법론

DESIGN.md를 작성하기 위해 기존 프로젝트의 디자인을 분석하는 방법이다.

### 1. Project Identity 추출

- 프로젝트 제목과 핵심 제품 영역을 파악한다.
- 프로젝트가 어떤 산업, 사용자, 목적을 가지는지 확인한다.

### 2. Atmosphere 정의

스크린샷이나 HTML 구조를 보고 전체 "분위기"를 포착한다. 아래 관점으로 평가한다:
- 정보 밀도: 여유로운가(airy) 밀집된가(dense)
- 톤: 따뜻한가(warm) 차가운가(cool) 중립인가(neutral)
- 성격: 기술적인가(technical) 편안한가(friendly) 고급스러운가(premium)
- 개성: 이 디자인만의 뚜렷한 특징은 무엇인가

### 3. Color Palette 매핑

HTML/CSS/Tailwind config에서 색상을 추출한다.
- CSS custom properties (--color-*, --theme-*)
- Tailwind config의 theme.extend.colors
- 인라인 style의 color, background-color, border-color
- rgba/hsla 값이 사용된 shadow, overlay, border

각 색상에 descriptive name + hex + functional role을 부여한다.

### 4. Typography 해석

폰트 설정을 추출하고 위계를 매핑한다.
- @font-face 또는 Google Fonts import
- font-family, font-weight, font-size, line-height, letter-spacing
- OpenType feature-settings

### 5. Geometry 변환

기술값을 자연어로 번역한다:

| Technical | Natural Language |
| --- | --- |
| `rounded-none` / `0px` | sharp, squared-off edges |
| `rounded-sm` / `2px` | slightly softened corners |
| `rounded-md` / `6px` | gently rounded corners |
| `rounded-lg` / `8-12px` | generously rounded corners |
| `rounded-xl` / `16px+` | very rounded, pillow-like |
| `rounded-full` / `9999px` | pill-shaped, circular |

### 6. Depth 묘사

shadow와 elevation을 분석한다:
- box-shadow 값을 level별로 분류한다.
- shadow color에 브랜드 톤이 반영되어 있는지 확인한다.
- border와 shadow의 역할 분담을 파악한다.
- "flat" design인 경우에도 명시적으로 기록한다.

---

## Output Format

```markdown
# Design System: [Project Title]

## 1. Visual Theme & Atmosphere
(분위기, 밀도, 미학적 철학. Key Characteristics 목록 포함.)

## 2. Color Palette & Roles
(Descriptive Name + Hex Code + Functional Role. 카테고리별 그룹화.)

## 3. Typography Rules
(Font family, fallback, OpenType features. Hierarchy table. Principles.)

## 4. Component Stylings
(Buttons, Cards, Inputs, Navigation 등. 형상 + 색상 + state.)

## 5. Layout Principles
(Grid, max-width, spacing scale, section rhythm.)

## 6. Depth & Elevation
(Level별 shadow 정의, shadow philosophy.)

## 7. Do's and Don'ts
(Do: 4-8개, Don't: 3-6개. concrete property 수준.)

## 8. Responsive Behavior
(Breakpoint table, touch targets, collapsing strategy.)

## 9. Agent Prompt Guide
(Quick Color Reference, Example Component Prompts, Iteration Guide.)
```

---

## Best Practices

- **Be Descriptive**: "blue"나 "rounded" 같은 generic 용어 대신 "Ocean-deep Cerulean (#0077B6)", "Gently curved edges (8px)" 처럼 성격과 값을 함께 적는다.
- **Be Functional**: 모든 디자인 요소가 왜 그 역할을 하는지 설명한다. 색상은 hex만이 아니라 functional role을, typography는 size만이 아니라 hierarchy에서의 위치를 적는다.
- **Be Consistent**: 문서 전체에서 같은 용어를 사용한다. Section 1에서 "Deep Navy"라고 부른 색상을 Section 4에서 "dark blue"로 바꾸지 않는다.
- **Be Visual**: 읽는 사람이 머릿속에 디자인을 그릴 수 있게 묘사한다. 기술 스펙과 감성적 묘사를 함께 쓴다.
- **Be Precise**: 자연어 묘사 뒤에 항상 exact value를 괄호로 병기한다. hex code, px value, font-weight number를 빠뜨리지 않는다.

## Common Pitfalls

- ❌ 기술 용어만 쓰고 자연어 번역이 없는 경우 (예: `rounded-xl` 대신 "generously rounded corners"가 필요)
- ❌ hex code 없이 descriptive name만 적는 경우 (정확한 재현 불가)
- ❌ functional role을 빠뜨리는 경우 (같은 #333이라도 heading vs body vs border는 역할이 다름)
- ❌ atmosphere 묘사가 너무 모호한 경우 ("깔끔하다"는 대부분의 프로젝트에 해당되므로 구분이 안 됨)
- ❌ shadow나 spacing의 미묘한 디자인 디테일을 무시하는 경우
- ❌ 분위기만 서술하고 concrete value가 없는 경우 (구현 불가)
- ❌ Section 7 Do's/Don'ts가 형용사 수준으로 끝나는 경우 ("깔끔하게 유지" 대신 구체적인 property/pattern boundary 필요)

---

## 예시 참조

[research-design/assets/](../../research-design/assets/) 폴더에 18개의 실제 DESIGN.md 예시가 있다. 작업 시 이 예시들을 참고하면 각 섹션의 구체적인 작성 수준을 파악할 수 있다.

| 예시 | 특징 | 주목할 점 |
| --- | --- | --- |
| [stripe.md](../../research-design/assets/stripe.md) | Fintech, premium purple accent, custom sohne-var font | multi-layer blue-tinted shadow 시스템, OpenType ss01 활용, 극단적으로 가벼운 weight 300 전략 |
| [vercel.md](../../research-design/assets/vercel.md) | Developer infrastructure, monochrome, Geist font family | shadow-as-border 기법 (`0px 0px 0px 1px`), extreme negative letter-spacing, workflow-specific accent colors |
| [claude.md](../../research-design/assets/claude.md) | AI product, warm parchment canvas, serif headings | 철저한 warm neutral palette (cool gray 없음), Anthropic Serif/Sans/Mono 3-font system, gradient-free depth |
| [cursor.md](../../research-design/assets/cursor.md) | Code editor, warm off-white, 3-font system | oklab color space border, CursorGothic + jjannon serif + berkeleyMono, OpenType cswh swash |
| [ollama.md](../../research-design/assets/ollama.md) | Developer CLI, pure grayscale, radical minimalism | 완전한 무채색 palette, SF Pro Rounded + pill geometry, zero shadows |
| [supabase.md](../../research-design/assets/supabase.md) | Developer platform, dark-mode-native, emerald accent | HSL-based color token system, translucent layering, Circular font with compressed display |
| [cal.md](../../research-design/assets/cal.md) | Scheduling tool, monochrome confidence, Cal Sans display | multi-layered shadow compositing (ring + soft + contact), grayscale-only aesthetic |
| [elevenlabs.md](../../research-design/assets/elevenlabs.md) | Voice AI, near-black canvas, studio aesthetic | monospace-forward typography, amber accent on dark, editorial precision |
| [revolut.md](../../research-design/assets/revolut.md) | Fintech, clean authority, data-dense | utilitarian precision, strong neutral hierarchy, financial-grade trust signals |
| [spacex.md](../../research-design/assets/spacex.md) | Aerospace, dramatic dark mode, cinematic scale | large-format imagery, futuristic geometry, extreme contrast |
| [warp.md](../../research-design/assets/warp.md) | Terminal, warm dark editorial, Matter font | warm parchment text on dark, cinematic photography, uppercase editorial labels |
| [mintlify.md](../../research-design/assets/mintlify.md) | Documentation, minimal 5-section structure | compact format 예시 — 1-5 section만으로도 유효한 DESIGN.md |
| [ibm.md](../../research-design/assets/ibm.md) | Enterprise, structured grid, Plex font system | systematic color tokens, 8-point grid, accessibility-first hierarchy |
| [composio.md](../../research-design/assets/composio.md) | Developer tools, clean dark mode | concise component documentation, dark/light surface interplay |
| [intercom.md](../../research-design/assets/intercom.md) | Customer messaging, warm brand personality | conversational tone reflected in design language, distinctive brand green |
| [runwayml.md](../../research-design/assets/runwayml.md) | Creative AI, editorial black-and-white | cinematic photography, art-direction typography, creative tool aesthetic |
| [voltagent.md](../../research-design/assets/voltagent.md) | AI agents framework, developer-focused | technical documentation style, gradient accents on dark surface |
| [together-ai.md](../../research-design/assets/together-ai.md) | AI infrastructure, clean modern | developer-friendly dark surface, gradient accent strategy |

예시를 참조할 때는 자신의 프로젝트와 가장 성격이 비슷한 1-3개를 골라 섹션별 작성 수준과 어투를 모델링한다.
