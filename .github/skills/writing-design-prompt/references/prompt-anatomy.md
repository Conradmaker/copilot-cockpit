# Prompt Anatomy Reference

디자인 프롬프트의 전체 구조, 시작점 선택, section 구조화, 요소별 specificity 패턴, theme coordination, anti-pattern 체크리스트를 정리한 상세 reference다.

---

## 1. 프롬프트 anatomy 구조

좋은 디자인 프롬프트는 아래 4개 layer를 위에서 아래로 쌓는다.

```
Layer 1: One-liner summary
  ─ 이 surface의 목적과 분위기를 한 문장으로

Layer 2: Design context block
  ─ platform, theme, palette, typography, layout, existing tone

Layer 3: Section structure
  ─ 번호+bold heading으로 page anatomy 정의

Layer 4: Detail specification
  ─ 각 section 내 component, state, interaction 구체화
```

### Layer 1: One-liner summary

surface가 무엇이며 어떤 느낌이어야 하는지 한 문장으로 잡는다. Designer가 전체 방향을 빠르게 파악하는 anchor 역할을 한다.

**예시:**
- "A clean, trustworthy login page with a centered form and subtle branding."
- "Dark-themed analytics dashboard emphasizing data density with high-contrast accent charts."
- "Mobile-first onboarding flow with warm illustration and progressive disclosure."

### Layer 2: Design context block

SKILL.md 핵심 패턴 3 (Design Context Injection)의 출력 형식을 따른다. 기존 design system이 있으면 그 값을 추출해 채우고, 없으면 existing UI evidence에서 추론한다.

### Layer 3: Section structure

page-level surface는 번호+bold heading으로 section anatomy를 정의한다.

```markdown
**Page Structure:**
1. **Header:** Navigation with logo and menu items
2. **Hero Section:** Headline, subtext, and primary CTA
3. **Content Area:** [Describe the main content]
4. **Footer:** Links, social icons, copyright
```

page-level surface를 작성할 때 프롬프트에서 잡은 section structure가 이후 design spec의 blueprint 뼈대가 된다.

### Layer 4: Detail specification

각 section 안의 component, state, interaction을 구체화한다. 여기서 Vague→Specific 변환과 color role formatting이 적용된다.

---

## 2. High-level ↔ Detailed 시작점 선택

프롬프트의 시작 깊이는 작업 복잡도에 맞춰 선택한다.

### High-level 시작 (broad → drill down)

**적합한 경우:**
- 전체 앱, multi-page surface를 처음 잡을 때
- 방향이 아직 정해지지 않았을 때
- Designer에게 넓은 탐색 여지를 주고 싶을 때

**패턴:**
```
An app for marathon runners to engage with a community,
find partners, get training advice, and find races near them.
```

broad start 후 screen별로 점진적으로 drill down한다.

### Detailed 시작 (targeted)

**적합한 경우:**
- 특정 screen, component, feature를 수정할 때
- 방향이 이미 명확할 때 (PRD, research evidence 확보 완료)
- 기존 surface에 incremental change를 적용할 때

**패턴:**
```
Product detail page for a Japandi-styled tea store.
Sells herbal teas, ceramics. Neutral, minimal colors,
black buttons. Soft, elegant font.
```

### 판단 기준

| 상황 | 시작점 |
| --- | --- |
| net-new app/surface, 방향 미정 | High-level → screen별 drill down |
| approved PRD + research evidence 있음 | Detailed (evidence 기반) |
| existing surface에 targeted edit | Detailed (preserve framing 포함) |
| material redesign | High-level identity → section별 refinement |

---

## 3. 요소별 Specificity 패턴

### Color specificity

`Descriptive Name (#hex) — functional role — rationale`

```
Deep Ocean Blue (#1a365d) — primary buttons and links — trustworthy, authoritative
Warm Cream (#faf5f0) — page background — inviting, reduces eye strain
Soft Gray (#6b7280) — secondary text — subtle hierarchy without harsh contrast
```

theme 변경을 프롬프트에 적을 때는 image와 icon도 함께 조율할지 명시한다.
```
Update theme to light orange. Ensure all images and illustrative icons
match this new color scheme.
```

### Typography specificity

`Family + weight + size band + character`

```
Heading: Inter, 600–700 weight, 32–48px range, clean geometric character
Body: Inter, 400 weight, 16–18px, generous leading (1.6–1.75)
Meta/Label: Inter, 500, 12–14px, uppercase with 0.05em tracking
```

font 변경 프롬프트는 성격(character)과 함께 적는다.
```
Use a playful sans-serif font for headings. Change body to a
readable serif with warm character.
```

### Layout specificity

`Grid system + max-width + gap/padding + responsive behavior`

```
12-column grid, max-width 1280px, 24px column gap
Section vertical padding: 80px desktop, 48px mobile
Sidebar: 280px fixed width, main content fluid
```

### Image specificity

이미지 변경이나 추가를 프롬프트에 적을 때는 위치 정의 → 대상 묘사 → 변경 지시 3단계를 따른다.

```
On 'Team' page, image of 'Dr. Carter (Lead Dentist)':
update her lab coat to black.
```

grouped image 변경:
```
Change background of all product images on landing page
to light taupe.
```

### Border & shape specificity

```
Buttons: fully rounded corners (pill-shaped), 2px solid border on secondary
Input fields: 1px solid border (#d1d5db), 8px radius, 2px solid brand color on focus
Cards: 12px radius, 1px border (#e5e7eb), soft shadow (0 1px 3px rgba(0,0,0,0.1))
```

---

## 4. Theme Coordination

theme 요소 하나를 바꿀 때 연쇄적으로 영향받는 요소를 함께 명시하는 패턴이다.

### Cross-element consistency matrix

| 변경 대상 | 함께 확인할 것 |
| --- | --- |
| Primary color | button, link, accent icon, brand element, image overlay |
| Font family | heading hierarchy, body readability, label/meta treatment, line-height |
| Border radius | button, card, input, modal, image — radius language 통일 |
| Background color | text contrast, card surface, divider visibility, image backdrop |
| Dark/Light theme | 모든 color role이 새 theme에서 contrast를 유지하는지 |

### 프롬프트 예시

```markdown
Update theme to dark mode.

**Cross-element coordination:**
- Background: Deep Charcoal (#1a1a2e) for page canvas
- Surface: Slate (#2d2d44) for cards and containers
- Text: adjust all text colors for WCAG AA contrast on new backgrounds
- Accent: keep Electric Blue (#4f9cf7) but verify contrast on dark surface
- Images: add subtle dark overlay to hero images
- Borders: switch from gray (#e5e7eb) to muted (#3d3d56)
- Icons: switch from dark-on-light to light-on-dark variant
```

---

## 5. DESIGN-TEMPLATE 섹션별 프롬프트 가이드

프롬프트에서 잡은 direction이 design spec의 어떤 영역으로 이어지는지 상세 매핑은 아래 테이블을 참고한다.

| 프롬프트에서 다루는 내용 | DESIGN-TEMPLATE 섹션 | 프롬프트에서 잡아야 할 최소 specificity |
| --- | --- | --- |
| 전체 분위기, 톤 | section 1 (Design Identity), section 2 (Visual Theme) | vibe 형용사 2~3개 + contrast/density 방향 |
| 색상 | section 3 (Color Palette & Roles) | descriptive name + hex + functional role |
| 타이포그래피 | section 4 (Typography Rules) | family + weight band + size range |
| 레이아웃, 여백 | section 5 (Layout Grammar) | grid + max-width + spacing scale |
| 페이지 구조 | section 6 (Section Blueprints) | 번호+heading으로 section anatomy |
| 이미지 에셋 | section 6A (Image Asset Requirement) | placement + ratio + style direction |
| 사용자 흐름, 상태 | section 7 (Core User Flows & States) | primary flow + key states (loading, empty, error, success) |
| 특징적 컴포넌트 | section 8 (Signature Components) | role + visual behavior + interaction direction |
| 일반 컴포넌트 스타일 | section 9 (Component Stylings) | shape + color + hierarchy rule |
| 카피, 톤 | section 10 (UX Writing & Tone) | voice character + CTA style |
| 모션, 접근성 | section 11 (Accessibility, Motion) | easing family + duration band + contrast rule |
| 유지/금지 규칙 | section 12 (Design System Fidelity) | must-preserve + must-avoid (구체적 property) |
| 구현 힌트 | section 13 (Implementation Seeds) | token + hard lock 값 |

"최소 specificity" 열은 프롬프트에 해당 내용을 담을 때 빠져서는 안 되는 수준이다. 이보다 모호하면 해석자가 추측해야 하고, 이보다 과하면 판단 여지가 줄어든다.

---

## 6. Anti-pattern 체크리스트

프롬프트를 완성한 뒤 아래를 빠르게 점검한다.

- [ ] "모던하게 해줘" 같은 단독 형용사만 있고 구체적 direction이 없지 않은가
- [ ] color가 hex 없이 이름만 적혀 있지 않은가
- [ ] existing surface인데 preserve 항목이 빠져 있지 않은가
- [ ] 여러 변경이 하나의 프롬프트에 뒤섞여 있지 않은가
- [ ] research evidence를 그대로 복붙하고 direction 변환이 없지 않은가
- [ ] motion direction이 "부드럽게" "자연스럽게" 수준에서 멈추지 않았는가
- [ ] image 변경 지시에 위치·대상·변경 중 빠진 것이 없는가
- [ ] theme 변경에 cross-element coordination이 빠져 있지 않은가
