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
- existing UI, theme, product tone evidence가 있으면 external reference보다 먼저 읽는다.
- external reference는 복제 근거가 아니라 개선 근거로만 사용한다.
- 분위기 설명만 쓰지 말고 color, typography, component, state, layout, tone을 실제 의사결정 가능 수준으로 남긴다.
- design decision이 PRD scope, requirement, metric 변경을 요구하면 conflict를 명시하고 planning으로 되돌린다.
- interactive surface가 있으면 accessibility와 state behavior를 빠뜨리지 않는다.
- implementation seed는 direct code가 아니라 token, state, structure, interaction constraint 수준으로 남긴다.

## Template

```markdown
## Design: {Title (2-10 words)}

{TL;DR - what experience is being designed, for whom, and what tone/direction this document recommends.}

**Design Context**

- Source PRD: {path or title}
- Platform: {web / ios / android / mixed}
- Existing product surface: {current UI baseline or none}
- Design goal: {이번 design.md가 구체화해야 하는 핵심}

## 1. Visual Theme & Atmosphere

- Overall mood: {airy / focused / warm / technical / premium 같은 자연어 묘사}
- Density: {여백 전략과 정보 밀도}
- Aesthetic direction: {왜 이 톤이 PRD와 맞는지}
- Existing tone to preserve: {유지해야 할 브랜드/제품 흔적}

## 2. Color Palette & Roles

- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}
- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}
- {Descriptive color name} ({#HEX}) — {functional role} — {why this role fits}

색상은 descriptive name + exact hex + functional role + rationale를 함께 적는다.

## 3. Typography Rules

- Heading family and character: {앵커 폰트 성격과 왜 쓰는지}
- Body family and character: {본문 폰트 성격과 왜 쓰는지}
- Weight hierarchy: {header / section / body / meta의 weight usage}
- Letter spacing and rhythm: {tight / neutral / generous 등}

## 4. Core User Flows & States

- Primary flow: {핵심 사용자 흐름}
- Key decision points: {사용자가 고민하거나 선택하는 지점}
- Loading state: {어떤 피드백을 보여줄지}
- Empty state: {무엇을 보여주고 어떤 행동을 유도할지}
- Error/recovery state: {실패 시 메시지와 복구 경로}
- Success/confirmation state: {완료 후 피드백과 다음 행동}

## 5. Component Stylings

- **Buttons:** {shape description, color assignment, hierarchy, interaction behavior}
- **Cards/Containers:** {corner language, background, border/shadow depth, grouping logic}
- **Inputs/Forms:** {stroke style, fill/background, focus/error behavior, helper text tone}
- **Navigation/Feedback:** {tabs, toast, banner, modal, sheet 같은 relevant component rule}

모서리, 그림자, stroke는 기술값만 쓰지 말고 물리적 표현으로 설명한다.

## 6. Layout Principles

- Grid and alignment: {column, grouping, anchor alignment}
- Whitespace strategy: {tight / balanced / generous + 왜 그렇게 두는지}
- Section rhythm: {정보를 어떤 순서와 간격으로 끊는지}
- Responsive behavior: {mobile/desktop에서 어떤 재배치가 필요한지}

## 7. UX Writing & Tone

- Voice character: {simple, calm, assertive, warm 등}
- CTA style: {동사 선택, 명확성 원칙}
- Error and recovery tone: {불안을 줄이고 다음 행동을 드러내는 방식}
- Confirmation and success tone: {과장 여부, 신뢰 표현 방식}

## 8. Accessibility & Interaction Constraints

- Contrast and legibility: {지켜야 할 기준}
- Keyboard/screen reader considerations: {relevant surface가 있으면 반드시 명시}
- Motion constraints: {reduce motion 대응, 의미 있는 전환만 허용 등}
- Interaction safety: {destructive action, confirmation, recovery 원칙}

## 9. Implementation Seeds

- Token seeds: {color, radius, spacing, elevation, motion token 방향}
- Component states to implement: {default / hover / focus / active / disabled / loading / error}
- Structure seeds: {layout, grouping, reusable pattern 힌트}
- Non-goals for implementation: {이번 단계에서 하지 않을 것}

## 10. References & Evidence

- Local evidence:
  - {path} — {what it contributed}
- External references:
  - {url / source} — {what it contributed}
- Design rationale summary: {왜 이 방향을 선택했는지}
- Conflicts or escalations: {PRD conflict 또는 unresolved choice가 있으면 명시}
```

## Review Checklist

- approved PRD의 direction과 충돌하지 않는가
- existing tone evidence와 external reference의 우선순위가 분명한가
- 색상, 타이포, shape, depth, layout이 실제 구현 가능한 수준으로 구체화되었는가
- loading, empty, error, success 상태가 빠지지 않았는가
- interactive surface에 대한 accessibility와 interaction constraint가 포함되었는가
- implementation seed가 direct code가 아니라 design-to-dev bridge 수준으로 정리되었는가
- unresolved conflict가 있으면 숨기지 않고 명시했는가