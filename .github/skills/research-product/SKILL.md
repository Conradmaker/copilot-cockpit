---
name: research-product
description: "Reference-led product discovery research workflow for validating product ideas, conducting user interviews, analyzing competition, assessing opportunities, and making product decisions grounded in market evidence. Use this skill when the user asks to research product opportunities, validate ideas, conduct competitive analysis, user interviews, JTBD analysis, Kano model, value proposition canvas, or market sizing before building. Always consult this skill for product discovery and validation work, even if the user only asks to 'validate this idea', 'analyze the market', 'research competitors', or 'should we build this'. For UI/UX reference research use research-design. For content research use research-content-source. Triggers on: product research, market research, competitive analysis, user interview, JTBD, Kano model, value proposition, opportunity assessment, product discovery, idea validation, market sizing, competitor analysis, TAM, SAM, SOM, Porter's 5 Forces, positioning, differentiation, 제품 조사, 시장 조사, 경쟁 분석, 사용자 인터뷰, JTBD, 카노 모델, 밸류 프러포지션, 기회 평가, 제품 디스커버리, 아이디어 검증, 시장 규모, TAM, 경쟁자 분석."
---
# Product Discovery Research 워크플로우

## 목표

프로덕트 디스커버리 리서치를 위한 reference-led 가이드다. 아이디어 검증, 사용자 인터뷰, 경쟁 분석, 시장 규모 파악, 기회 평가 등 제품 결정을 근거 기반으로 수행하는 방법론을 제공한다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 작업 전에는 references 문서를 읽고 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## Hard Rules

이 규칙은 mandatory다. 위반하면 스킬이 올바르게 작동하지 않음을 의미한다.

### No Solution-First Thinking

솔루션을 먼저 정의하지 않음. 항상 문제와 outcome을 먼저 명시한다.

```markdown
❌ FORBIDDEN:
"We should build a search bar"
"Let's add AI recommendations"

✅ REQUIRED:
"Problem: Users can't find products (40% exit rate)
Outcome: Reduce exit rate to 20%
Possible solutions: [search bar, recommendations, better navigation]"
```

### Evidence-Based Decisions

실제 사용자 리서치의 근거 없이 사용자 needs를 assume하지 않음.

```markdown
❌ FORBIDDEN:
- "Users probably want X"
- "Competitor has X, so we need it too"
- "CEO thinks we should build X"

✅ REQUIRED:
- "5 out of 8 interviewed users mentioned X as pain point"
- "Analytics show 60% abandon at step 3"
- "Prototype test: 7/10 completed task"
```

### Minimum Interview Threshold

segment당 최소 5개의 사용자 인터뷰 없이 문제를 validate하지 않음.

| Segment | Minimum Interviews |
|---------|-------------------|
| Power Users | 5+ |
| New Users | 5+ |
| Churned | 5+ |

### Falsifiable Assumptions

모든 assumption은 testable + falsifiable + clear success criteria여야 함.

| Assumption | Test | Success Criteria |
|------------|------|------------------|
| Users will complete onboarding | Prototype test (n=10) | >70% completion |
| Price point is acceptable | Landing page test | >3% conversion |

---

## 핵심 단계

### 1. Discovery Brief 고정

리서치 목적과 scope를 명확히 정의한다.

- 리서치 질문 작성 (What do we need to learn?)
- 대상 segment 정의 (Who are we learning from?)
- Timeline과 resource 확인
- 기존 evidence inventory (What do we already know?)

#### 빠른 판단 기준

- 리서치 질문이 falsifiable한가?
- segment당 최소 5 interviews 계획이 있는가?
- solution-first thinking이 없는가?

→ 상세: [references/discovery-template.md](references/discovery-template.md)

---

### 2. Evidence Collection

 JTBD, User Interview, Competitive Analysis, Market Sizing 등 방법론 선택 후 evidence 수집.

- JTBD Interview: "When [situation], I want to [motivation], So I can [outcome]" format
- Competitive Analysis: Porter's 5 Forces, Positioning Matrix, Feature Comparison
- Market Sizing: TAM/SAM/SOM framework (Top-Down vs Bottom-Up)
- User Research: Discovery Interview, Validation Interview, Contextual Inquiry

#### 빠른 판단 기준

- JTBD Job Statement가 situation → motivation → outcome 구조를 따르는가?
- 경쟁 분석이 5 Forces를 모두 다루는가?
- Market Sizing이 Top-Down과 Bottom-Up 중 적절한 방식을 선택한가?
- 인터뷰가 최소 threshold를 충족하는가?

→ 상세: [references/jtbd.md](references/jtbd.md), [references/user-research.md](references/user-research.md), [references/competitive-analysis.md](references/competitive-analysis.md), [references/market-sizing.md](references/market-sizing.md)

---

### 3. Analysis

수집된 evidence를 분석해 insights를 추출한다.

- Forces Diagram 분석 (Push/Pull/Anxiety/Habit)
- Pain points clustering
- Market opportunity sizing
- Competitive positioning mapping
- Assumption vs Evidence gap analysis

#### 빠른 판단 기준

- Forces Diagram이 4가지 forces를 모두 다루는가?
- Pain points가 evidence로 backed되어 있는가?
- Competitive positioning이 differentiation을 명시하는가?

---

### 4. Synthesis

분석 결과를 actionable recommendations로 합성한다.

- Key findings summary
- Assumption validation status (Confirmed / Partially Confirmed / Refuted / Unknown)
- Opportunity ranking
- Recommended next steps (Build / Pivot / Kill)

#### 빠른 판단 기준

- 모든 finding이 evidence로 backed되어 있는가?
- assumption이 validation status를 가지는가?
- recommendation이 Build/Pivot/Kill 중 하나로 명확한가?

---

### 5. Handoff

구현 단계로 넘어갈지, 추가 리서치가 필요한지 결정한다.

- PRD-ready 여부 판단
- Unresolved assumptions list
- Next research priorities
- Document to `prd.md` or `research-notes.md`

#### 빠른 판단 기준

- PRD를 작성할 evidence가 충분한가?
- critical assumption이 모두 validated인가?
- 추가 리서치가 필요한가?

---

## references/ 가이드

| 파일 | 언제 읽는가 |
|------|------------|
| [jtbd.md](references/jtbd.md) | JTBD interview, Job Statement, Forces Diagram 작성 시 |
| [user-research.md](references/user-research.md) | Interview methods, Sample size, Best practices 확인 시 |
| [competitive-analysis.md](references/competitive-analysis.md) | Porter's 5 Forces, Positioning Matrix, Feature Comparison 수행 시 |
| [market-sizing.md](references/market-sizing.md) | TAM/SAM/SOM, Top-Down/Bottom-Up, SOM calculation 시 |
| [hard-rules.md](references/hard-rules.md) | Core principles, Evidence-based decisions, Minimum threshold 확인 시 |
| [discovery-template.md](references/discovery-template.md) | Discovery Brief 템플릿 작성 시 |

---

## 응답 패턴

### 1. Research Summary

```markdown
## Research Summary
**Topic**: [research topic]
**Segments**: [segments studied]
**Methods**: [JTBD, Interview, Competitive Analysis, Market Sizing]
**Key Finding**: [most important finding]
**Confidence**: [High/Medium/Low based on evidence quality]
```

### 2. Evidence Table

```markdown
## Evidence Table
| Assumption | Evidence | Status | Confidence |
|------------|----------|--------|------------|
| [assumption] | [source: interview n=X, analytics] | [Confirmed/Partial/Refuted/Unknown] | [High/Medium/Low] |
```

### 3. Recommendations

```markdown
## Recommendations
**Decision**: [Build / Pivot / Kill / Research More]
**Rationale**: [evidence-based reasoning]
**Next Steps**: [specific actions]
**Open Questions**: [unresolved items]
```

### 4. Competitive Analysis Summary

```markdown
## Competitive Landscape
**Key Players**: [competitors]
**Positioning**: [where we fit]
**Differentiation**: [our unique value]
**Threats**: [Porter's 5 Forces analysis]
```

---

## 범위

- 이 스킬은 **product discovery research**에 집중한다.
- UI/UX screen/flow reference research → **research-design**이 owner다.
- Content source gathering → **research-content-source**이 owner다.
- Implementation decisions → domain skills (fe-, be-, ds-)가 owner다.
- Technical SEO → **seo-technical**이 owner다.