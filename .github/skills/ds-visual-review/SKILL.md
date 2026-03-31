---
name: ds-visual-review
description: "Runtime visual inspection and fix workflow for websites running locally or remotely. Use when the user asks to review, check, fix, or validate UI visually in an actual browser — including layout issues, responsive breaks, overflow, alignment problems, visual inconsistencies, and accessibility gaps visible at runtime. Always consult this skill for visual inspection tasks that require browser evidence, even if the user only mentions 'check the UI', 'fix the layout', 'find design problems', 'why does this look broken', or 'responsive check'. For static design decisions without runtime verification use ds-visual-design, ds-ui-patterns, ds-product-ux. For raw browser automation without inspection workflow use agent-browser. Triggers on: review website, check UI, fix layout, visual inspection, responsive check, find design problems, UI 확인, 레이아웃 수정, 디자인 문제 찾기, 화면 깨짐, overflow, 정렬 문제, 반응형 검사, 브라우저 테스트, visual bug, layout break, runtime design."
---

# 실시간 시각 검수 (ds-visual-review)

## 목표

실제 브라우저에서 실행되는 웹사이트의 시각적 문제를 발견하고 수정하고 재검증한다. 이 스킬은 정적 디자인 가이드(ds-visual-design, ds-ui-patterns)와 달리 브라우저 automation을 통한 **runtime evidence**를 기반으로 작동한다. 스크린샷 캡처, viewport 테스트, DOM 검사, framework-specific fix 적용, re-verification loop까지 실행형 workflow를 담당한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 inspection을 수행하거나 fix를 적용할 때는 아래 reference 문서를 직접 읽고 상황에 맞는 workflow와 checklist를 확인한 뒤 실행한다.

---

## 5대 핵심 원칙

### 1. 브라우저에서 실제 실행 evidence를 캡처한다

정적 mockup이나 design file만 보고 시각적 문제를 판단하지 않는다. 실제 브라우저에서 실행되는 화면의 스크린샷, DOM structure, viewport 다양성을 기반으로 검수한다.

- 지정 URL로 브라우저를 열고 전체 페이지 스크린샷을 캡처한다
- Mobile (375px), Tablet (768px), Desktop (1280px), Wide (1920px) viewport에서 각각 테스트한다
- DOM snapshot 또는 read_page로 구조 정보를 수집한다
- 문제 영역을 selector로 지정해 부분 스크린샷을 추가 캡처한다

#### 빠른 판단 기준

- "이 화면 깨진 것 같아" → 브라우저를 열고 스크린샷을 먼저 캡처한다
- "모바일에서 문제 있어" → 375px viewport로 전환 후 스크린샷
- "특정 요소만 확인해줘" → 해당 selector의 부분 스크린샷

→ 상세: [references/01-inspection-workflow.md](references/01-inspection-workflow.md)

### 2. Layout, responsive, accessibility, visual consistency를 검토한다

브라우저 evidence를 기반으로 4가지 검수 영역을 체계적으로 점검한다.

- **Layout**: overflow, overlap, alignment, spacing, container break
- **Responsive**: breakpoint transition, mobile/tablet/desktop 적응
- **Accessibility**: contrast, focus state, keyboard navigation, screen reader
- **Visual Consistency**: font, color, spacing 일관성, state 표현

#### 빠른 판단 기준

- horizontal scrollbar가 보이면 overflow problem이다
- 요소 두 개가 겹쳐 보이면 overlap 또는 z-index issue
- 텍스트가 잘려 보이면 text clipping 또는 container overflow
- hover/focus state가 없으면 interactive element 불완전

→ 상세: [references/02-visual-checklist.md](references/02-visual-checklist.md)

### 3. Framework-specific fix를 적용한다

프로젝트가 사용하는 styling method(CSS, Tailwind, styled-components 등)에 맞는 fix pattern을 적용한다. 범용 fix가 아니라 framework별 best practice를 따른다.

- Pure CSS/SCSS: `overflow-x: hidden`, `max-width: 100%`, CSS custom properties
- Tailwind CSS: `overflow-hidden`, `max-w-full`, `truncate`, `line-clamp-*`, `break-words`
- styled-components/Emotion: theme 기반 spacing/color, responsive mixin
- React/Vue component: component-level style scope, conditional className

#### 빠른 판단 기준

- Tailwind 프로젝트에서 `style={{ width: '100%' }}`를 쓰고 있으면 `className="w-full max-w-full"`로 교체 검토
- CSS에서 magic number(`margin: 15px`)가 반복되면 CSS custom properties 검토
- styled-components에서 hardcoded color가 반복되면 theme token 검토

→ 상세: [references/03-framework-fixes.md](references/03-framework-fixes.md)

### 4. Re-verification loop를 유지한다

fix 적용 후 반드시 브라우저에서 재검증한다. HMR 또는 reload 후 스크린샷을 다시 캡처하고 before/after를 비교한다.

- fix 후 페이지 reload 또는 HMR wait
- 문제 영역 재스크린샷
- before/after 비교로 fix effectiveness 확인
- regression check: fix가 다른 영역에 side effect를 주지 않았는지 확인
- issues remaining → inspection loop 반복 (최대 3회)

#### 빠른 판단 기준

- fix 후 "이제 괜찮아?" → 스크린샷 재캡처로 확인
- 3회 fix attempt 후 문제가 남아 있으면 사용자에게 consult
- fix가 다른 페이지/viewport에 영향을 줬는지 확인

→ 상세: [references/01-inspection-workflow.md](references/01-inspection-workflow.md)

### 5. agent-browser와 complementary로 작동한다

이 스킬은 browser automation backend를 필요로 한다. `agent-browser` 스킬이 raw browser operation(navigation, screenshot, click, scraping)을 담당하고, `ds-visual-review`는 inspection→fix→re-verify workflow를 담당한다.

- browser operation은 agent-browser 또는 browser tools로 실행
- inspection logic, fix pattern, re-verification loop는 이 스킬이 제공
- 두 스킬을 같은 task에서 함께 사용할 수 있다 (complementary)

#### 빠른 판단 기준

- "브라우저 열어서 확인해줘" → agent-browser로 열고 ds-visual-review로 inspection
- "스크린샷만 필요해" → agent-browser만 사용
- "깨진 부분 찾아서 고쳐줘" → ds-visual-review 전체 workflow

---

## 범위

### 포함

- 실제 브라우저에서 실행되는 웹사이트 visual inspection
- Layout, responsive, accessibility, visual consistency 문제 발견
- Framework-specific fix 적용 (CSS, Tailwind, styled-components, React, Vue)
- Re-verification loop with screenshot evidence

### 제외

- 정적 design file/mockup 검수 (Figma, Sketch) → ds-visual-design 참조
- Layout pattern 설계 (page structure, section composition) → ds-ui-patterns 참조
- UX flow, copy, action pattern → ds-product-ux 참조
- Code logic, state management, performance → fe-* 스킬 참조

### agent-browser와 관계

| 스킬 | 역할 |
|------|------|
| agent-browser | Raw browser automation (navigation, screenshot, DOM read, click, scraping) |
| ds-visual-review | Inspection→fix→re-verify workflow using browser backend |

순서: agent-browser가 backend tool, ds-visual-review가 workflow orchestrator.

---

## 출력 형식

### Inspection Report

```markdown
# Visual Inspection Report

## Summary
| 항목 | 값 |
|------|-----|
| Target URL | {URL} |
| Viewports Tested | Desktop, Tablet, Mobile |
| Framework | {Detected} |
| Styling Method | {Tailwind / CSS / etc.} |
| Issues Detected | {N} |
| Issues Fixed | {M} |

## Detected Issues

### [P1] Layout Overflow
- **Location**: `.card-container` on mobile viewport
- **Evidence**: 스크린샷 참조
- **Severity**: High (horizontal scrollbar 발생)
- **Fix Applied**: `overflow-hidden` 추가

## Verification
- Before/After 스크린샷 비교
- Regression check 결과
```

---

## 관련 스킬

- **ds-visual-design**: Visual foundations (color, spacing, hierarchy, depth)
- **ds-ui-patterns**: Layout and section composition patterns
- **ds-product-ux**: UX flows, copy, action patterns
- **agent-browser**: Raw browser automation backend
- **fe-tailwindcss**: Tailwind CSS implementation patterns