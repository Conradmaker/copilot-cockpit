# UI/UX Keywords Reference

디자인 프롬프트에서 사용하는 UI 용어, 분위기 형용사, 색상 역할, 형태, motion/easing 키워드의 progressive disclosure reference다.

---

## Component Keywords

### Navigation

- navigation bar, nav menu, header
- breadcrumbs, tabs, sidebar
- hamburger menu, dropdown menu
- back button, close button

### Content Containers

- hero section, hero banner
- card, card grid, tile
- modal, dialog, popup
- accordion, collapsible section
- carousel, slider

### Forms

- input field, text input
- dropdown, select menu
- checkbox, radio button
- toggle switch
- date picker, time picker
- search bar, search input
- submit button, form actions

### Calls to Action

- primary button, secondary button
- ghost button, text link
- floating action button (FAB)
- icon button

### Feedback

- toast notification, snackbar
- alert banner, warning message
- loading spinner, skeleton loader
- progress bar, step indicator

### Layout

- grid layout, flexbox
- sidebar layout, split view
- sticky header, fixed footer
- full-width, contained width
- centered content, max-width container

---

## Adjective Palettes

### Minimal / Clean

- minimal, clean, uncluttered
- generous whitespace, breathing room
- subtle, understated, refined
- simple, focused, distraction-free

### Professional / Corporate

- sophisticated, polished, trustworthy
- corporate, business-like, formal
- subtle shadows, clean lines
- structured, organized, hierarchical

### Playful / Fun

- vibrant, colorful, energetic
- rounded corners, soft edges
- bold, expressive, dynamic
- friendly, approachable, warm

### Premium / Luxury

- elegant, luxurious, high-end
- dramatic, bold contrasts
- sleek, modern, cutting-edge
- exclusive, boutique, curated

### Dark Mode

- dark theme, night mode
- high-contrast accents
- soft glows, subtle highlights
- deep backgrounds, muted surfaces

### Organic / Natural

- earthy tones, natural colors
- warm, inviting, cozy
- textured, tactile, handcrafted
- flowing, organic shapes

---

## Color Role Terminology

색상을 프롬프트에 적을 때는 반드시 `Descriptive Name (#hex) — functional role` 형식을 사용한다.

### Backgrounds

- page background, canvas
- surface color, card background
- overlay, scrim

### Text

- primary text, heading color
- secondary text, body copy
- muted text, placeholder
- inverse text (on dark backgrounds)

### Accents

- primary accent, brand color
- secondary accent, highlight
- success, error, warning colors
- hover state, active state

---

## Shape Descriptions

| Technical | Natural Language |
| --- | --- |
| `rounded-none` | sharp, squared-off edges |
| `rounded-sm` | slightly softened corners |
| `rounded-md` | gently rounded corners |
| `rounded-lg` | generously rounded corners |
| `rounded-xl` | very rounded, pillow-like |
| `rounded-full` | pill-shaped, circular |

---

## Motion & Easing Keywords

프롬프트에서 motion을 적을 때는 generic 키워드(ease-out 등)로 끝내지 않고, cubic-bezier 또는 named variant 수준으로 구체화하면 해석 정확도가 올라간다. 아래는 프롬프트에서 motion direction을 설정할 때 사용하는 키워드 팔레트다.

### Easing Families

| Named Variant | Cubic-bezier | 성격 |
| --- | --- | --- |
| ease-out-expo | `cubic-bezier(0.16, 1, 0.3, 1)` | 빠른 시작, 부드러운 착지. snappy reveal |
| ease-out-quart | `cubic-bezier(0.25, 1, 0.5, 1)` | 자연스러운 감속. default transition |
| ease-in-out-cubic | `cubic-bezier(0.65, 0, 0.35, 1)` | 부드러운 입출. modal, overlay |
| ease-in-out-quint | `cubic-bezier(0.83, 0, 0.17, 1)` | 극적인 전환. page transition |
| spring-gentle | `cubic-bezier(0.34, 1.56, 0.64, 1)` | 살짝 튀는 느낌. button feedback |
| linear | `cubic-bezier(0, 0, 1, 1)` | 균일한 속도. progress, continuous animation |

### Duration Bands

| Band | Range | 용도 |
| --- | --- | --- |
| instant | 50–100ms | micro-feedback, toggle, checkbox |
| fast | 150–200ms | hover, focus, button press |
| normal | 250–350ms | panel slide, card expand, dropdown |
| slow | 400–600ms | page transition, modal enter/exit |
| dramatic | 700ms–1s+ | hero reveal, scroll-driven animation |

### Interaction Recipe Format

motion direction을 설정할 때 아래 형식을 사용하면 구체적이고 해석 가능한 recipe로 바로 변환할 수 있다:

```
[trigger] → [technique/property] from [initial] to [final] over [duration] using [easing]
```

프롬프트에서 motion direction을 설정할 때 이 형식을 사용하면 구체적인 specification으로 바로 변환할 수 있다.

예시:
- "hover 시 카드를 살짝 들어올리는 느낌" → `hover → translateY from 0 to -4px over 200ms using ease-out-quart`
- "스크롤로 hero 텍스트가 드러나는 효과" → `scroll-enter → opacity+translateY from (0, 20px) to (1, 0) over 600ms using ease-out-expo`

---

## Language & Copy Keywords

### Tone Directions

- calm, reassuring, confident
- urgent, action-oriented, direct
- warm, friendly, conversational
- formal, precise, authoritative

### CTA Formatting

- 동사로 시작: "Start free trial", "Get started", "시작하기"
- 결과를 포함: "Save 20% today", "20% 절약하기"
- 구체적: "Create your first project" > "Get started"

---

## DESIGN-TEMPLATE 매핑 가이드

이 프로젝트의 `.github/agents/artifacts/DESIGN-TEMPLATE.md`를 사용하는 경우, 위 키워드 카테고리가 template의 어떤 섹션에 대응하는지 아래 테이블로 빠르게 확인한다. DESIGN-TEMPLATE을 사용하지 않는 프로젝트에서는 이 섹션을 무시해도 된다.

| 키워드 카테고리 | DESIGN-TEMPLATE 섹션 |
| --- | --- |
| Component Keywords | section 6 (Section Blueprints), section 8 (Signature Components), section 9 (Component Stylings) |
| Adjective Palettes | section 1 (Design Identity Summary), section 2 (Visual Theme & Atmosphere) |
| Color Role Terminology | section 3 (Color Palette & Roles) |
| Shape Descriptions | section 5 (Layout Grammar & Spatial Rules), section 9 (Component Stylings) |
| Motion & Easing Keywords | section 8 (Signature Components — interaction recipe), section 11 (Accessibility, Motion & Interaction Constraints) |
| Language & Copy Keywords | section 10 (UX Writing & Tone) |
