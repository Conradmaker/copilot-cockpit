---
name: research-design
description: "Reference-led screen and flow research workflow using Refero MCP. Use this skill when the user asks to research real product screens, compare shipped flows, extract patterns from references, or turn UI references into design decisions before implementation. Always consult this skill for screen and flow reference research, even if the user only says 'find inspiration', 'show references', 'how do top products solve this', or 'research the flow first.' For layout, color, typography, motion, persuasion, or implementation decisions, hand off to ds-ui-patterns, ds-visual-design, ds-typography, ds-product-ux, and fe-* after the evidence pass. Triggers on: research-design, refero, screen research, flow research, shipped patterns, reference-driven design, pattern extraction, design references, MCP design research, 레퍼런스 조사, 화면 레퍼런스, 플로우 레퍼런스, 패턴 추출, 실서비스 분석, 조사 먼저."
---

# Research Design 리서치 워크플로우

## 목표

Refero MCP로 실서비스 screen과 flow evidence를 수집하고, 이를 구현 전에 사용할 수 있는 design decisions로 정리한다.

이 스킬은 레이아웃, 색상, 타이포그래피, 모션, 카피, 구현 규칙의 최종 owner가 아니다. 이 스킬의 역할은 reference를 찾고, 사실을 추출하고, pattern을 비교하고, 다음 owner 스킬로 handoff할 수 있는 근거를 만드는 것이다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 작업을 시작하기 전에는 아래 reference 문서를 직접 읽고 tool parameter와 예시 workflow를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 단계

### 1. Discovery brief를 먼저 고정한다

레퍼런스 검색은 brief가 없으면 금방 표면적인 취향 수집으로 무너진다. 검색 전에 아래를 짧게 고정한다.

- 무엇을 만들고 있는가: screen type, platform, scope
- 누구를 위한가: audience, domain familiarity, usage context
- 사용자가 지금 달성해야 하는 핵심 과업은 무엇인가
- 사용자가 망설일 가능성이 큰 objection은 무엇인가
- 반드시 지켜야 할 constraint는 무엇인가

#### 빠른 판단 기준

- brief 없이 바로 search_screens부터 호출하지 않는다
- "예뻐 보이는 것"보다 해결해야 할 문제와 맥락을 먼저 적는다
- 같은 task라도 web과 ios는 분리해서 brief를 잡는다

#### Brief 출력 형식

> "나는 [WHO]를 위한 [WHAT]을 조사하고 있다. 이 surface의 핵심 과업은 [GOAL]이고, 가장 큰 objection은 [OBJECTION]이다. platform은 [PLATFORM], constraint는 [CONSTRAINTS]다."

### 2. Search는 broad → narrow → leader 순으로 돌린다

좋은 reference research는 첫 검색 결과를 모아놓는 작업이 아니다. 여러 query 축을 바꿔가며 landscape를 넓게 본 뒤, 의미 있는 방향으로 좁혀야 한다.

- facts로 검색한다: screen type, component, company, platform, visible copy
- broad query로 landscape를 보고, interesting pattern이 보이면 narrow query로 들어간다
- 좋은 사례가 보이면 leader search로 그 회사 전체를 더 본다
- flow task면 screens와 flows를 같이 본다

#### 빠른 판단 기준

- 같은 단어만 바꿔 검색하지 않는다
- query는 broad, specific, leader, adjacent를 섞는다
- 10개 보고 멈추지 않고 최소 50개 이상 landscape를 본 뒤 판단한다

### 3. Search result가 아니라 get_screen과 get_flow로 deep dive한다

search 결과의 짧은 요약만 읽으면 surface-level research에 머문다. promising한 결과는 반드시 deep dive한다.

- screen research는 get_screen으로 상세 description과 metadata를 읽는다
- include_similar를 활용해 related examples를 확장한다
- flow research는 get_flow로 step sequence, decision point, recovery path를 읽는다
- visual이 꼭 필요할 때만 image_size를 올린다

#### 빠른 판단 기준

- best result 5~10개는 get_screen 또는 get_flow로 내려간다
- exact copy, number, condition, timing을 source-bound note로 남긴다
- image_size는 필요할 때만 올리고, 기본은 text 분석으로 충분한지 먼저 본다

### 4. 사실을 pattern으로 구조화한다

이 단계의 목적은 opinion을 만드는 것이 아니라 evidence를 재사용 가능한 형태로 구조화하는 것이다.

세 가지 lens로 정리한다.

- Structure: layout, step count, information hierarchy, decision sequence
- Surface facts: observed typography, color use, spacing rhythm, icon style, visual treatments
- Product logic: objection handling, trust signals, friction reducers, recovery paths

#### 빠른 판단 기준

- "좋다", "세련됐다" 같은 인상평만 남기지 않는다
- 각 finding은 source name과 exact detail을 같이 남긴다
- generic pattern과 best-in-class pattern을 구분한다

#### 필수 산출물

- Research summary
- Pattern table
- Steal list
- Open questions

### 5. Evidence를 design decisions로 번역한다

reference를 모으는 것만으로는 설계가 되지 않는다. 하지만 이 단계에서도 final owner decision까지 refero가 가져가면 안 된다. 역할은 evidence를 design-ready한 형태로 정리하는 데서 멈춘다.

- observed facts를 candidate decisions로 번역한다
- 각 decision에 source와 rationale을 붙인다
- conflicting pattern은 하나로 합치지 말고 trade-off로 남긴다
- final rulebook은 해당 owner skill로 handoff한다

#### 빠른 판단 기준

- final palette, final type scale, final motion system을 refero에서 확정하지 않는다
- "이 방향이 왜 맞는지"는 설명하되, 최종 visual system 규칙은 owner skill에 넘긴다
- handoff에서 open question을 숨기지 않는다

#### Handoff 매트릭스

| 현재 결정 항목 | 다음 owner |
| --- | --- |
| layout, section rhythm, surface composition | ds-ui-patterns |
| color, depth, icon language, visual polish, Anti-AI-Slop | ds-visual-design |
| font choice, type scale, leading, tracking | ds-typography |
| trust signal, CTA, objection handling, loading, interaction meaning | ds-product-ux |
| prompt language, Designer-ready brief, reference-to-prompt translation | writing-design-prompt |
| DESIGN.md 작성, project-wide visual system documentation | writing-design-prompt → [design-md.md](../writing-design-prompt/references/design-md.md) |
| implementation, accessibility, Tailwind, component API | fe-* |

### Visual System Reference Assets

`assets/` 폴더에 18개의 실서비스 DESIGN.md 예시가 있다. Refero MCP가 screen/flow의 layout과 interaction을 조사하는 반면, 이 assets는 project-wide visual system style guide의 tone과 구조를 참고할 때 사용한다.

예시 목록, industry별 선택 가이드, 역할 구분 상세는 [references/design-md-examples.md](references/design-md-examples.md)를 읽는다.

---

## 응답 패턴

이 스킬을 사용할 때는 링크 모음이나 막연한 취향평으로 끝내지 않는다. 아래 구조를 기본값으로 사용한다.

### 1. Research summary

- query 수
- reviewed result 수
- deep dive한 screen 또는 flow 수
- 핵심 관찰 결과 3~7개

### 2. Pattern table

| Aspect | Ref A | Ref B | Ref C | Pattern |
| --- | --- | --- | --- | --- |

### 3. Steal list

| Source | Exact detail | Why it works | Candidate use |
| --- | --- | --- | --- |

### 4. Candidate decisions

- Decision
- Evidence
- Why this matters
- Owner handoff

### 5. Open questions

- evidence가 부족한 지점
- owner skill로 넘겨야 할 unresolved choice

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/mcp-tools.md](references/mcp-tools.md) | search_screens, search_flows, get_screen, get_flow, get_design_guidance의 parameter와 사용법을 확인할 때 |
| [references/example-workflow.md](./references/example-workflow.md) | discovery → research → analyze → handoff 흐름을 end-to-end 예시로 보고 싶을 때 |
| [references/design-md-examples.md](references/design-md-examples.md) | assets/ DESIGN.md 예시 18개의 목록, 특징, industry별 선택 가이드를 볼 때 |
| [design-md.md](../writing-design-prompt/references/design-md.md) | DESIGN.md 작성 규칙, section 가이드, DESIGN.md vs design.md 구분이 필요할 때 |

## 범위

- 이 스킬은 reference research, pattern extraction, reference-driven synthesis owner다.
- final layout rule은 ds-ui-patterns가 owner다.
- final color, icon, polish, Anti-AI-Slop rule은 ds-visual-design이 owner다.
- final typography rule은 ds-typography가 owner다.
- trust, copy, objection handling, loading, interaction meaning은 ds-product-ux가 owner다.
- evidence를 Designer-ready prompt language나 brief로 압축하는 것은 writing-design-prompt가 owner다.
- code, accessibility, Tailwind, component API 같은 implementation deep dive는 fe-*가 owner다.
