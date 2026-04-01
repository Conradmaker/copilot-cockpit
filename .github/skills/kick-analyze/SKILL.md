---
name: kick-analyze
description: "User-initiated comprehensive product analysis workflow that orchestrates multiple research and design skills to analyze your current product from market, competitive, UX, and strategic perspectives. Generates actionable recommendations and structured report. Invoke this skill when you want to deeply analyze your product's competitive positioning, identify improvement opportunities, or understand market fit. This skill coordinates research-product, research-design, research-content-source, research-foundation, ds-product-ux, ds-ui-patterns, ds-visual-design, fe-* and other domain skills. Triggers on: kick-analyze, analyze product, product analysis, competitive analysis, market fit, product review, kick, analyze, 제품 분석, 경쟁력 분석, 마켓핏, 제품 리뷰, kick 분석."
user-invocable: true
disable-model-invocation: true
---
# Kick-Analyze: Comprehensive Product Analysis

## 목표

유저가 직접 호출하는 kick- 스킬이다. 현재 프로덕트를 시장, 경쟁, UX, 전략적 관점에서 깊고 넊게 분석해 경쟁력을 높일 수 있는 아이디어와 방법을 추천하고 보고서를 생성한다.

이 스킬은 여러 research-/ds-/fe- 스킬들을 orchestrate한다. agent가 자동 호출하지 않으며, 유저가 명시적으로 요청해야 실행된다.

---

## 워크플로우

### 1. Initialize

분석의 목적과 scope를 명확히 한다.

- 분석 topic 확인 (예: "현재 landing page의 market fit 분석")
- 분석 goals 정의 (예: "경쟁력 파악, 개선 아이디어 추천")
- 현재 프로덕트 상태 파악 (codebase, design artifacts, existing docs)

**질문 예시**:
- "어떤 부분을 분석하고 싶은가?" (전체 product vs 특정 feature vs landing page)
- "분석의 목적은?" (market fit 확인, competitive positioning, UX 개선, 기획 방향)
- "기존에 파악된 문제나 concern이 있는가?"

---

### 2. Parallel Investigation

여러 영역을 동시에 조사한다. 호출할 스킬들을 parallel로 실행.

#### 호출할 스킬 목록

| 영역 | 스킬 | 조사 내용 |
|------|------|-----------|
| **Product Discovery** | research-product | JTBD, Market Sizing, Competitive Analysis, User Research |
| **UI/UX Reference** | research-design | Screen/flow research, pattern extraction, reference-driven synthesis |
| **Content Research** | research-content-source | Source gathering, fact check, credibility evaluation |
| **Research Foundation** | research-foundation | Source ladder, 공식 문서 및 로컬 근거 합성 |
| **Product UX** | ds-product-ux | CTA copy, error/empty state, loading UX, trust signals |
| **UI Patterns** | ds-ui-patterns | Layout pattern, hero, dashboard, section composition |
| **Visual Design** | ds-visual-design | Palette, spacing, hierarchy, depth, anti-AI-slop |
| **Typography** | ds-typography | Font choice, pairing, scale, line-height, tracking |
| **Frontend Patterns** | fe-react-patterns, fe-tailwindcss | Component architecture, styling patterns |
| **SEO** | seo-technical, seo-content | Technical SEO, on-page SEO, search intent |

#### Parallel Execution Rules

- 독립적인 조사 영역일 때만 병렬화
- 같은 파일과 같은 질문을 중복 조사하지 않음
- 2-3개의 독립적인 호출만 병렬화
- Sequential dependency가 강하면 순차 실행

---

### 3. Synthesis

수집된 evidence를 합성해 보고서를 생성한다.

#### 보고서 구조

1. **Executive Summary** — 핵심 finding 3-5개
2. **Market & Competitive Analysis** — TAM/SAM/SOM, Porter's 5 Forces, Positioning
3. **UX & Design Analysis** — UI patterns, visual hierarchy, UX writing, accessibility
4. **Technical & SEO Analysis** — Performance, Core Web Vitals, SEO issues
5. **Recommendations** — Build/Pivot/Kill, 개선 아이디어 ranked by impact
6. **Implementation Roadmap** — Short-term, medium-term, long-term actions
7. **Open Questions** — Unresolved items, next research priorities

#### Evidence Quality Gate

- 모든 claim에 evidence backing
- Source citation (URL, interview n, analytics data)
- Confidence level (High/Medium/Low)

---

### 4. Delivery

유저에게 보고서를 납품한다.

- 보고서 파일 생성 (templates/analysis-report.md 사용)
- Key findings 요약 presentation
- Q&A session (유저가 추가 질문 가능)
- Next steps agreement (구현으로 넘어갈지, 추가 research 필요한지)

---

## templates/ 가이드

| 파일 | 용도 |
|------|------|
| [templates/analysis-report.md](templates/analysis-report.md) | 보고서 템플릿 (YAML frontmatter + sections) |

---

## 범위

- 이 스킬은 **유저가 직접 호출하는 kick- 스킬**이다.
- agent가 자동 호출하는 스킬은 **research- 계열**이다.
- kick- 스킬은 orchestration만 수행하고, 실제 research는 research-* 스킬들이 수행한다.
- Implementation decisions는 domain skills (fe-, be-, ds-)가 owner다.