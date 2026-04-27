# Design Template

이 문서는 downstream definition phase에서 `design.md`를 작성할 때 따르는 artifact template다.
Designer가 primary owner지만, Mate가 downstream design kickoff를 준비하거나 Technical/Execution phase가 design intent를 해석할 때도 읽을 수 있다.

## Use This Doc When

- approved PRD를 기반으로 `design.md`를 처음 만들 때
- 기존 `design.md`를 새 PRD 방향에 맞게 갱신할 때
- visual tone, UX flow, component styling, implementation seed를 한 문서로 정리해야 할 때
- 디자인 결과를 개발로 이어질 수 있는 수준으로 구체화해야 할 때

## Mandatory Rules

- `design.md`는 approved `prd.md`를 전제로 한다.
- `design.md`는 PRD를 다시 쓰지 않고, approved PRD를 visual, UX, interaction decision으로 확장한다.
- `design.md`는 target surface를 실제로 만드는 UI-rendering evidence에서 시작한다. route/page, layout wrapper, shared component, primitive, theme/token, relevant style을 우선 읽는다.
- non-visual business logic는 visible state, interaction, accessibility를 설명할 때만 포함하고, 나머지는 과감히 제외한다.
- existing surface를 다루면 변경안 전에 current baseline과 preserve-without-drift를 먼저 적는다.
- existing UI, theme, product tone evidence가 있으면 external reference보다 먼저 읽는다.
- current design system의 color, typography, spacing, component language는 hard constraint로 다루고, deviation이 필요하면 rationale을 명시한다.
- abstract mood만 쓰고 끝내지 않는다. 필요할 때는 exact design seed를 남긴다. 예: hex, opacity, tracking, leading, radius, border weight, grid rule, easing family, duration band.
- external reference는 복제 근거가 아니라 개선 근거로만 사용한다.
- 강한 visual prompt나 style reference를 받았더라도 그대로 복붙하지 않고, current product에 맞는 design identity, layout grammar, signature component, anti-drift guardrail로 번역한다.
- 분위기 설명만 쓰지 말고 color, typography, component, state, layout, tone을 실제 의사결정 가능 수준으로 남긴다.
- page 또는 multi-block surface를 다루면 section blueprint를 남긴다. component-only task라면 relevant surface block만 남기고 불필요한 section은 억지로 채우지 않는다.
- generated image asset가 필요하면 `Image Asset Requirement List` section에 필요한 asset item만 최소 필드로 남긴다. 자세한 형식은 section 6A를 따르고, prompt detail은 Painter가 문서 전체 tone and manner에서 해석한다.
- design decision이 PRD scope, requirement, metric 변경을 요구하면 conflict를 명시하고 planning으로 되돌린다.
- interactive surface가 있으면 accessibility와 state behavior를 빠뜨리지 않는다.
- implementation seed는 direct code가 아니라 token, state, structure, interaction constraint 수준으로 남긴다.
- new shared token, component pattern, visual language를 제안하면 current system에서 왜 충분하지 않은지와 어떤 범위에 적용되는지 남긴다.
- strong-direction surface(landing, editorial, branding-heavy task)에서는 signature interaction이나 visual mechanism을 최소 하나 이상 recipe 수준으로 정의한다. [trigger] → [technique/property change] over [duration] using [easing] 형식을 기본으로 한다. 분위기 묘사로 끝내지 않는다.
- motion duration과 easing은 구체적으로 잠근다. ease-out, ease-in-out 같은 generic 키워드로 끝내지 않는다.
- key layout geometry(px, vw, max-width, gap/padding scale)는 section blueprint 또는 layout grammar에 적어도 한 곳 구체적으로 잠근다. 형용사 크기 묘사만 남기지 않는다.
- multilingual surface라면 measure 기준을 문자권과 text role을 고려하여 body prose 기본값, body/lede, hero/display headline을 여유있게 잠근다. 특히 CJK와 non-CJK가 섞인 surface에서는 `ch` 단위가 실제 글자 수처럼 동작하지 않는다는 점을 기억한다.
- section 12에는 concrete must-preserve 1개 이상과 concrete must-avoid 1개 이상을 반드시 포함시킨다. must-avoid는 "generic AI 느낌 배제" 수준이 아니라 어떤 property, color range, visual behavior, animation pattern이 금지인지 번역해 남긴다.
- strong-direction surface라면 section 12 또는 High-Direction Addendum의 locked rule을 MUST / DO NOT 명령형 구조로 각 1개 이상 작성한다.

## Template

```markdown
## Design: {Title (2-10 words)}

{TL;DR - what experience is being designed, for whom, and what tone/direction this document recommends.}

**Design Context**

- Platform: {web / ios / android / mixed}
- Target surface: {route, screen, feature entry point}
- Surface type: {existing surface refinement / material redesign / net-new surface}
- Existing product surface: {current UI baseline or none}
- Design goal: {이번 design.md가 구체화해야 하는 핵심}
- Current baseline summary: {현재 surface의 tone, component language, visible behavior 요약}
- Preserve without drift: {이번 작업에서 유지해야 하는 tokens, layout language, component conventions}
- Allowed change surface: {이번 iteration에서 바꿔도 되는 범위}

## 0. UI Context Audit & Baseline

- Primary UI evidence: {target page/route, layout wrapper, key components, primitives}
- Theme/token/style evidence: {theme file, token source, globals.css, tailwind config, local design doc}
- Dependency tracing summary: {page → layout → component → primitive → token/style chain}
- Dependency trace stop reason: {어느 레이어에서 멈췄고 왜인지 — 파일 미존재 · scope 외 · evidence 충분 중 하나로 기록. 흐릿한 "파악 완료"로 끝내지 않는다.}
- Visible states that shaped decisions: {default / hover / focus / loading / empty / error / success}
- Non-visual logic intentionally excluded: {무시한 logic과 이유}
- Current baseline strengths: {보존할 가치가 있는 현재 패턴}
- Current baseline risks or drift to correct: {현재 UI에서 바로잡아야 할 일관성 문제}

## 1. Design Identity Summary

- System shorthand: {이 디자인을 한 줄로 부르는 working label}
- Core metaphor or material language: {technical blueprint / editorial poster / glass depth / structured grid 같은 working language}
- What should feel unmistakable: {사용자가 바로 기억해야 하는 핵심 visual differentiator}
- Authority or emotional stance: {technical / warm / premium / urgent / playful 등}
- Drift to avoid: {generic output, 과한 depth, random color injection 같은 금지 방향}

## 2. Visual Theme & Atmosphere

- Overall mood: {airy / focused / warm / technical / premium 같은 자연어 묘사}
- Density: {여백 전략과 정보 밀도}
- Aesthetic direction: {왜 이 톤이 PRD와 맞는지}
- Contrast strategy: {high contrast / low contrast / monochrome discipline / accent burst 등}
- Material or depth strategy: {flat / glass / layered / editorial / structural 등}
- Texture or blend strategy: {noise, grain, dashed line, overlay, blend mode가 있으면 명시}
- Existing tone to preserve: {유지해야 할 브랜드/제품 흔적}

## 3. Color Palette & Roles

- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}
- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}
- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}

색상은 descriptive name + exact hex + functional role + rationale를 함께 적는다.
background / foreground / accent / support / divider처럼 palette 역할을 잠근다.

## 4. Typography Rules

- Heading family and character: {앵커 폰트 성격과 왜 쓰는지}
- Body family and character: {본문 폰트 성격과 왜 쓰는지}
- Display scale and size range: {hero, section, body, meta를 size band 형용사가 아닌 exact px 또는 rem으로 잠근다. }
- Weight hierarchy: {header / section / body / meta의 구체적인 font-weight 수치로 잠근다}
- Letter spacing and rhythm: {heading, body, label 을 tight/generous 형용사로 끝내지 않고, 각각의 em 단위 tracking 값으로 구체화한다.}
- Leading strategy: {display, section, body의 형용사 리듬 묘사로 끝내지 않고 구체적인 line-height 숫자로 표현한다. 만약 영어가 아닌 한국어라면 line-height를 조금 더 열어서 글자 사이가 답답해 보이지 않도록 한다.}
- Measure rules: {Latin body prose, Korean body/lede, hero/display를 각기 다른 기준으로 작성한다. 예: Latin body 60–75ch, Korean body 70–84ch, Korean lede 76–92ch, hero/display는 intended line count + clamp(px/vw) 또는 em range로 잠근다.}
- Metadata or label treatment: {mono 여부, uppercase 여부, 구체적 tracking 수치.}

## 5. Layout Grammar & Spatial Rules

- Primary grid system: {12-column / split layout / bento / stacked ribbon 등}
- Page shell rule: {브라우저 가장자리와 만나는 outer container. 예: `min(1440px, calc(100% - 96px))`처럼 side padding 포함 기준을 잠근다}
- Content rail rule: {카드/섹션/주요 콘텐츠가 실제로 놓이는 inner rail 폭과 정렬 기준을 적는다. page shell과 다를 수 있다}
- Prose measure rule: {body paragraph, long-form copy의 폭 기준을 따로 적는다. body prose와 lede/supporting copy가 같은 값인지 여부도 명시한다}
- Display/headline measure rule: {hero, section headline, display copy는 body prose와 분리해 intended line count와 폭 기준을 적는다. 필요하면 `clamp()` 또는 `em` range를 사용한다}
- Wide desktop behavior: {1440px 이상에서 shell, background, media, grid line, hero copy가 어떻게 확장/고정/bleed 되는지 적는다. `desktop = 1200px centered`로 끝내지 않는다}
- Divider or border language: {hairline, top-border ribbon, 1px gap grid 등}
- Corner or radius language: {sharp / px / em / asymmetrical 등 구체적인 수치, 표현으로 작성}
- Whitespace strategy: {section 수직 padding, column gap을 tight/generous 형용사로 끝내지 않고 px 또는 spacing-scale 수치로 잠근다}
- Section rhythm: {major·minor section 전환 vertical padding 범위를 px 단위로 잠근다}
- Persistent background layer: {page 전반에 반복되는 structural layer이 있다면 구체적으로 명시하고, 없으면 명시적으로 "없음"으로 표기}
- Responsive behavior: {375, 768, 1280, 1440, 1920px에서 어떤 재배치가 필요한지 적는다. 1280과 1920을 같은 "desktop"으로 뭉개지 말고, wide desktop에서 background/content alignment, hero line count, media bleed 여부를 따로 기록한다}

## 6. Section Blueprints

- Navigation or header: {surface 상단 구조, tone, alignment, CTA rule — height 또는 min-height를 px로 잠근다}
- Hero or primary entry block: {headline structure, support copy, media or stat treatment — column span, vertical anchor, min-height 또는 viewport-height 의 구체적인 수치 단위로 잠근다. headline은 intended line count(예: desktop 2줄, 길면 3줄)와 measure를 함께 적고, body prose max-width를 재사용하지 않는지 확인한다}
- Key content blocks: {feature grid, manifesto, comparison list, simulator, pricing, dashboard modules 등 relevant section anatomy — 각 block의 column count, row height 또는 padding band, alignment anchor를 구체적으로 명시.}
- CTA or conversion block: {전환 구간의 구조와 긴장감 — column span, button alignment anchor 방향 명시}
- Footer or endcap: {마감 구조와 information density}
- Non-page exception: {component-only 또는 narrow task면 어떤 block만 남기고 무엇을 생략하는지}

## 6A. Image Asset Requirement List

이미지 생성이 필요한 경우에만 여러 asset item의 리스트로 남긴다.

- `{asset_id}` — `{output_path}` — `{placement}` — `{ratio}`
- `{asset_id}` — `{output_path}` — `{placement}` — `{ratio}`
- Optional note per item: {해당 placement 이름만으로는 정말 모호할 때만 한 줄}

각 image asset item은 최소 필드만 이용하며, 필요한 asset 수만큼 같은 형식의 줄을 반복한다.

## 7. Core User Flows & States

- Primary flow: {핵심 사용자 흐름}
- Key decision points: {사용자가 고민하거나 선택하는 지점}
- Loading state: {어떤 피드백을 보여줄지}
- Empty state: {무엇을 보여주고 어떤 행동을 유도할지}
- Error/recovery state: {실패 시 메시지와 복구 경로}
- Success/confirmation state: {완료 후 피드백과 다음 행동}

## 8. Signature Components

- {Component name}: {role, structure, visual behavior, relevant state} — Interaction recipe: [trigger] → [technique/property] over [duration] with [easing]
- {Component name}: {role} — Interaction recipe: [trigger] → [technique/property] over [duration] with [easing]
- Reusable accent patterns: {badge, cursor, marquee card, stat card, topology graph 같은 standout unit}

interaction이 있는 component는 분위기 묘사로 끝내지 않는다. clip-path reveal, stroke-text fill, scroll-driven opacity, grayscale-to-color 같은 naming 가능한 technique name과 property change 수준으로 기술한다. direct code가 아닌 design-to-dev bridge 수준을 유지한다.

## 9. Component Stylings

- **Buttons:** {shape description, color assignment, hierarchy, interaction behavior}
- **Cards/Containers:** {corner language, background, border/shadow depth, grouping logic}
- **Inputs/Forms:** {stroke style, fill/background, focus/error behavior, helper text tone}
- **Navigation/Feedback:** {tabs, toast, banner, modal, sheet 같은 relevant component rule}

모서리, 그림자, stroke는 기술값만 쓰지 말고 물리적 표현으로 설명한다.

## 10. UX Writing & Tone

- Voice character: {simple, calm, assertive, warm 등}
- CTA style: {동사 선택, 명확성 원칙}
- Error and recovery tone: {불안을 줄이고 다음 행동을 드러내는 방식}
- Confirmation and success tone: {과장 여부, 신뢰 표현 방식}

## 11. Accessibility, Motion & Interaction Constraints

- Contrast and legibility: {지켜야 할 기준}
- Keyboard/screen reader considerations: {relevant surface가 있으면 반드시 명시}
- Motion signature: {easing을 cubic-bezier 또는 named variant 수준으로 잠근다. duration은 ms/s 단위로 구체화한다. ease-out 같은 generic 키워드로 끝내지 않는다. reveal/hover behavior와 interaction tempo도 함께 명시한다.}
- Motion constraints: {reduce motion 대응, 의미 있는 전환만 허용 등}
- Interaction safety: {destructive action, confirmation, recovery 원칙}
- Cursor, overlay, blend, transform rule: {custom cursor, grayscale hover, clip-path reveal 같은 interaction grammar가 있으면 명시}

## 12. Design System Fidelity & Deviations

- Must preserve: {계속 유지할 font, color, spacing, radius, component language, motion rule — 구체적 property 또는 값으로 잠근다. "현재 톤 유지" 수준으로 끝내지 않는다.}
- Intentional deviations: {현재 system에서 의도적으로 바꾸는 요소}
- New or adjusted tokens/patterns: {정말 필요한 경우에만}
- Rationale for deviation: {왜 current system만으로는 부족한지}
- Must avoid: {도입하면 안 되는 visual 또는 interaction pattern — CSS property, color range, visual behavior로 구체화한다. "generic AI 느낌 배제" 같은 설명은 어떤 property/pattern이 금지인지 번역해 남긴다.}
- Guardrails against drift: {이번 design이 도입하면 안 되는 visual drift}
- Locked rules (strong-direction surface): MUST: {구체적인 유지 규칙 — property, color, geometry value} / DO NOT: {구체적인 금지 규칙 — property, visual behavior, aesthetic element} — landing, editorial, branding-heavy surface라면 각 1개 이상 명시한다.

## 13. Implementation Seeds

- Visual spec seeds: {hex, opacity, size, spacing, radius, border, blur, transform, easing 중 execution에 필요한 값}
- Token seeds: {color, radius, spacing, elevation, motion token 방향}
- Hard implementation locks: {execution에서 임의로 바꾸면 안 되는 값 목록 밖 값은 개발자가 결정한다고 명시.}
- Component states to implement: {default / hover / focus / active / disabled / loading / error}
- Structure seeds: {layout, grouping, reusable pattern 힌트}
- Non-goals for implementation: {이번 단계에서 하지 않을 것}

## 14. References & Evidence

- Local UI evidence:
  - {path} — {page, layout, component, primitive, token, style 중 무엇을 기여했는지}
- Dependency tracing coverage: {어느 chain까지 추적했고 어디서 멈췄는지}
- External references:
  - {url / source} — {what it contributed}
- Preserved constraints: {기존 system에서 그대로 유지한 것}
- Intentional deviations: {기존 system과 다르게 간 것과 이유}
- Design rationale summary: {왜 이 방향을 선택했는지}
- Conflicts or escalations: {PRD conflict 또는 unresolved choice가 있으면 명시}
```

## Review Checklist

- approved PRD의 direction과 충돌하지 않는가
- target surface, shared layout, primitives, theme/token, relevant style까지 UI evidence chain이 확보되었는가
- non-visual logic는 visible state와 interaction 설명에 필요한 수준으로만 포함되었는가
- existing surface라면 current baseline과 preserve-without-drift가 먼저 정리되었는가
- design identity summary가 있고, 이 surface를 기억하게 만드는 unmistakable differentiator가 정리되었는가
- existing tone evidence와 external reference의 우선순위가 분명한가
- palette, typography, radius, border, grid, motion 가운데 relevant한 spec seed가 충분히 구체적인가
- prose measure와 display/headline measure가 분리되어 있는가 (특히 Korean 또는 multilingual surface에서)
- page나 multi-block surface라면 section blueprint가 있고, component-heavy task라면 signature component가 정의되었는가
- generated image asset가 필요한 경우 image requirement list가 있고, 필요한 asset item마다 필수 필드가 `asset_id`, `output_path`, `placement`, `ratio`로 최소화되어 있는가
- current design system에서 벗어나는 제안이 있으면 rationale과 적용 범위가 명시되었는가
- 색상, 타이포, shape, depth, layout이 실제 구현 가능한 수준으로 구체화되었는가
- loading, empty, error, success 상태가 빠지지 않았는가
- interactive surface에 대한 accessibility와 interaction constraint가 포함되었는가
- do-not-drift 또는 must-avoid guardrail이 명시되었는가
- implementation seed가 direct code가 아니라 design-to-dev bridge 수준으로 정리되었는가
- unresolved conflict가 있으면 숨기지 않고 명시했는가
- strong-direction surface라면 signature interaction이 recipe 수준(trigger → technique → duration → easing)으로 정의되었는가
- motion signature가 cubic-bezier 또는 named easing variant 수준으로 잠겨있는가 (generic keyword로 끝나지 않았는가)
- key layout geometry(px, max-width, gap/padding scale)가 section blueprint 또는 layout grammar에 적어도 한 곳 잠겨있는가
- page shell / content rail / prose measure / display-headline measure / wide desktop behavior가 하나의 값으로 뭉개지지 않고 분리되어 있는가
- 1280px와 1920px에서 hero 줄 수, background/content alignment, media bleed가 어떻게 달라지는지 적혀 있는가
- section 12의 must-preserve와 must-avoid가 구체적인 property/pattern 수준인가 (형용사 묘사 수준으로 끝나지 않았는가)
- strong-direction surface라면 MUST/DO NOT 형태의 locked rule이 section 12 또는 High-Direction Addendum에 포함되었는가

## High-Direction Surface Addendum

landing page, editorial 화면, branding-heavy surface처럼 뚜렷한 visual identity가 필요한 task에만 적용한다. 좁은 feature 추가나 component-only task에는 사용하지 않는다.

### A. Persistent Visual System

page 전반에 걸쳐 지속되는 visual grammar를 명시한다.

- Structural background layer: {전체 페이지에서 반복되는 grid, texture, line 언어 — 예: 12-column hairline overlay, 0.04 opacity noise texture}
- Signature typography treatment: {display, heading, body, label의 체계 — stroke-text, uppercase tracking, mono accent 등 해당 technique 명시}
- Global animation curve: {page-wide transition easing — cubic-bezier 또는 named variant로 잠근다}

### B. Named Interaction Recipes

component별 interaction을 recipe 형식으로 정의한다. generic hover 하나로 모두 묶지 않는다.

- {recipe name}: [trigger] → [CSS technique/property] from [initial value] to [final value] over [duration] using [easing]
- {recipe name}: [trigger] → [CSS technique/property] from [initial value] to [final value] over [duration] using [easing]

### C. Anti-Drift Locks

surface에서 절대 도입하면 안 되는 것을 MUST / DO NOT 형식으로 잠근다.

- MUST: {구체적 유지 규칙 — property, color, geometry value}
- MUST: {구체적 유지 규칙}
- DO NOT: {구체적 금지 규칙 — property, visual behavior, aesthetic element}
- DO NOT: {구체적 금지 규칙}