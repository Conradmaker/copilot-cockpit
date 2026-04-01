---
name: kick-design-booster
description: "Systematic design diagnosis and improvement workflow that evaluates existing UI through heuristic scoring, persona testing, cognitive load assessment, and technical audit, then applies targeted improvement workflows (simplify, harden, delight, polish, intensity) based on findings. Use when asked to review, improve, critique, audit, simplify, harden, polish, or boost UI quality — or when a design feels generic, cluttered, fragile, or unfinished. Always consult this skill for design improvement work, even if the user only says 'make this better', 'this looks AI-generated', 'pre-launch check', 'simplify this UI', 'make it bolder', or 'production-ready'. For runtime visual inspection use ds-visual-review. For code-level review use fe-code-review. Triggers on: design critique, design audit, UI improvement, simplify UI, harden, polish, delight, bolder, quieter, pre-launch, production-ready, AI slop, design boost, 디자인 비평, 디자인 감사, UI 개선, 간소화, 견고화, 마무리, 볼더, 콰이어터, 출시 전 점검, AI 슬롭, 디자인 부스트."
user-invocable: true
disable-model-invocation: true
---

# 디자인 진단·개선 부스터 (kick-design-booster)

Prefer retrieval-led reasoning over pre-training-led reasoning.

## 목표

현재 UI의 디자인 품질과 기술 품질을 체계적으로 진단하고, 발견된 문제에 맞는 개선 워크플로우를 조합 실행한다. 이 스킬은 행동형(action) 스킬이다. 기존 ds-*/fe-* 원칙형 스킬의 reference를 실행 중에 참조하며 개선을 수행한다.

---

## Phase 1: 진단 (Discovery)

### 1-1. 맥락 확인

사용자에게 아래를 확인한다:
- **범위**: 전체 페이지 / 특정 섹션 / 특정 컴포넌트
- **우선순위**: 시각 품질 / 기술 견고성 / 접근성 / 성능 / 전체
- **품질 기준**: MVP / 정식 출시 / 플래그십

Design Context(`.design-context.md` 또는 프로젝트 설정)가 없으면 `kick-init`부터 실행한다.

### 1-2. 디자인 품질 평가 (Critique)

10가지 차원에서 인터페이스를 평가한다:

1. **AI Slop 탐지** — 가장 먼저 확인. AI가 만든 것처럼 보이는가?
2. **시각적 위계** — 눈이 가장 중요한 요소로 먼저 가는가?
3. **정보 구조와 인지부하** — 구조가 직관적인가? 선택지가 4개를 넘는가?
4. **감정 여정** — 어떤 감정을 불러일으키는가? Peak-end가 긍정적인가?
5. **발견성과 어포던스** — 인터랙티브 요소가 명확히 인터랙티브해 보이는가?
6. **구성과 균형** — 레이아웃이 의도적으로 균형 잡혀 있는가?
7. **커뮤니케이션으로서의 타이포그래피** — 위계가 읽기 순서를 안내하는가?
8. **목적 있는 색상** — 색이 장식이 아니라 의미를 전달하는가?
9. **상태와 엣지 케이스** — 빈 상태, 로딩, 에러, 성공이 설계되었는가?
10. **마이크로카피와 보이스** — 글이 명확하고 브랜드에 맞는가?

→ 상세 절차: [references/01-critique-workflow.md](references/01-critique-workflow.md)

### 1-3. 기술 품질 감사 (Audit)

5차원에서 코드 수준 검사를 실행한다:

| 차원 | 검사 대상 |
| --- | --- |
| 접근성 | 대비, ARIA, 키보드, 시맨틱 HTML, alt text, 폼 |
| 성능 | 레이아웃 스래싱, 비싼 애니메이션, 이미지, 번들, 리렌더 |
| 테마 | 하드코딩 색상, 다크모드, 토큰 일관성 |
| 반응형 | 고정 너비, 터치 타겟, 수평 스크롤, 텍스트 스케일링 |
| 안티패턴 | AI slop 징후, 일반 디자인 안티패턴 |

→ 상세 절차: [references/02-audit-workflow.md](references/02-audit-workflow.md)

### 1-4. 점수 산출

| 평가 | 점수 체계 |
| --- | --- |
| Critique (Heuristic) | Nielsen 10 × 0–4 = 40점 만점 |
| Audit (Technical) | 5차원 × 0–4 = 20점 만점 |

---

## Phase 2: 개선 방향 합의

### 2-1. 문제 맵핑

Phase 1 에서 발견된 문제를 차원별로 매핑하고 severity 를 부여한다:

| 심각도 | 기준 | 액션 |
| --- | --- | --- |
| **P0 (치명)** | 사용자 흐름 차단, 신뢰 손상 | 즉시 수정 필수 |
| **P1 (심각)** | 주요 사용성 저하, 빈번한 오류 | 우선 수정 |
| **P2 (보통)** | 개선 필요하지만 우회 가능 | 계획적 수정 |
| **P3 (경미)** | 사소한 불편, cosmetic | 여유 있을 때 |

### 2-2. 영향도 평가

각 문제의 영향도를 3 축으로 평가:

- **사용자 영향** = 빈도 × 심각도 (높음/중간/낮음)
- **기술 부채** = 수정 비용 × 방치 비용 (높음/중간/낮음)
- **비즈니스 영향** = 전환 × 신뢰 (높음/중간/낮음)

### 2-3. 워크플로우 조합 추천

문제 유형과 우선순위에 따라 워크플로우를 조합한다.

| 문제 유형 | 1 순위 | 2 순위 | 3 순위 |
| --- | --- | --- | --- |
| **복잡함** | distill | arrange | clarify |
| **불안정함** | harden | polish | — |
| **지루함** | delight | animate | colorize |
| **약함** | typeset | colorize | arrange |
| **혼란스러움** | clarify | distill | arrange |
| **과함** | distill | intensity(↓) | clarify |
| **부족함** | intensity(↑) | delight | animate |

**사용자 확인:**
1. P0/P1 문제부터 처리할 것인가?
2. 어떤 차원을 가장 먼저 개선할 것인가? (시각/기술/전체)
3. 예상 효과와 소요 시간을 고려하여 워크플로우를 선택한다.

---

## Phase 3: 개선 실행

### 워크플로우 선택 가이드

| 워크플로우 | 언제 선택하는가 | 참조할 기존 스킬 |
| --- | --- | --- |
| **distill** (간소화) | 복잡하고 어수선하다 | ds-ui-patterns, ds-product-ux |
| **harden** (견고화) | 엣지 케이스, i18n, 에러 처리 부족 | fe-a11y, ds-product-ux |
| **overdrive** (초월) | 기술적으로 인상적인 구현 필요 | ds-ui-patterns/04, fe-react-performance |
| **delight** (즐거움) | 기능적이지만 감정이 없다 | ds-product-ux, ds-visual-design |
| **polish** (마무리) | 기능 완성 후 최종 품질 점검 | ds-visual-design, ds-typography, fe-a11y |
| **intensity** (강도 조절) | 너무 안전하거나 과하다 | ds-visual-design, ds-typography |
| **arrange** (레이아웃) | 구성과 균형이 어긋나 있다 | ds-ui-patterns |
| **typeset** (타이포) | 폰트/계층이 약하다 | ds-typography |
| **colorize** (색상) | 색이 부족하거나 의미 없다 | ds-visual-design |
| **animate** (모션) | 정적이고 생기가 없다 | ds-ui-patterns/04-motion-interaction.md |
| **clarify** (UX writing) | 글이 혼란스럽다 | ds-product-ux |

각 워크플로우의 상세 절차:

- [references/03-distill-workflow.md](references/03-distill-workflow.md) — 복잡도 제거, 진행적 노출, 정보 정리
- [references/04-harden-workflow.md](references/04-harden-workflow.md) — i18n, 텍스트 오버플로, 에러 시나리오, 극단 입력
- [references/05-overdrive-workflow.md](references/05-overdrive-workflow.md) — View Transitions, scroll-driven animation, WebGL, spring physics
- [references/06-delight-workflow.md](references/06-delight-workflow.md) — 마이크로 인터랙션, 카피 개성, 만족감 인터랙션
- [references/07-polish-workflow.md](references/07-polish-workflow.md) — 정렬, 타이포, 색상, 상태, 전환, 엣지케이스 최종 체크리스트
- [references/08-intensity-workflow.md](references/08-intensity-workflow.md) — bolder(강도↑) + quieter(강도↓) 조절
- [references/09-arrange-workflow.md](references/09-arrange-workflow.md) — 레이아웃/간격/균형 개선
- [references/10-typeset-workflow.md](references/10-typeset-workflow.md) — 타이포그래피 위계/가독성 개선
- [references/11-colorize-workflow.md](references/11-colorize-workflow.md) — 색상 전략/팔레트/의미 부여
- [references/12-animate-workflow.md](references/12-animate-workflow.md) — 모션/인터랙션/생동감 추가
- [references/13-clarify-workflow.md](references/13-clarify-workflow.md) — UX writing/마이크로카피/보이스 정립

---

## Phase 4: 검증 (Re-audit)

개선 후 Phase 1의 진단을 다시 실행한다.

- Before/After 점수 비교
- 잔여 P0/P1 이슈 확인
- 개선이 다른 차원에 regression을 일으키지 않았는지 확인
→ 상세 절차: [references/14-verification-report.md](references/14-verification-report.md)

---

## 추천 로드 순서

- 전체 디자인 리뷰: `01 → 02 → 15 → 16 → 17`
- 간소화: `03 → 01`
- 견고화: `04 → 02`
- 레이아웃 개선: `09 → 01`
- 타이포그래피 개선: `10 → 01`
- 색상 전략: `11 → 01`
- 모션 추가: `12 → 01`
- UX writing: `13 → 01`
- 마무리: `07 → 01 → 02`
- 검증: `14` (모든 개선 후)

---

## 범위

### 포함

- 디자인 품질 비평 (heuristic, persona, cognitive load, emotion)
- 기술 품질 감사 (a11y, performance, theme, responsive, anti-pattern)
- 6가지 개선 워크플로우 (distill, harden, overdrive, delight, polish, intensity)
- 개선 후 재진단

### 제외

- 런타임 브라우저 검수 → `ds-visual-review`
- 코드 품질 리뷰 (구문, 패턴, 컨벤션) → `fe-code-review`
- 디자인 초기 컨텍스트 수집 → `kick-init`
- 레이아웃 설계, 타이포그래피 선택 같은 원칙형 판단 → 각 `ds-*/fe-*` 스킬
