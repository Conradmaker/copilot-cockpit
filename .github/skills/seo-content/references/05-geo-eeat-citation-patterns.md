# GEO, E-E-A-T, and Citation Patterns

## 목표

AI engines가 인용하기 쉬운 콘텐츠 구조를 만들고, trust와 extractability를 높이는 신호를 정리한다.

---

## 1. Princeton GEO methods 요약

| Method | 기대 효과 | 적용 방식 |
| --- | --- | --- |
| Cite sources | 높음 | 권위 있는 출처와 함께 주장 제시 |
| Statistics addition | 높음 | 구체적인 수치와 날짜 제시 |
| Quotation addition | 중상 | 전문가 인용과 attribution |
| Authoritative tone | 중간 | 과장 없이 확신 있는 문장 |
| Easy to understand | 중간 | 직답, 쉬운 설명 |
| Technical terms | 중간 | 도메인 용어를 정확히 사용 |
| Unique words | 중간 | 과도한 반복을 줄임 |
| Fluency optimization | 중상 | 읽기 흐름과 구조 개선 |
| Avoid keyword stuffing | 필수 | 억지 반복 금지 |

---

## 2. content blocks that AI cites well

### 정의 블록

```markdown
**Search Engine Optimization (SEO)** is the practice of improving how search engines crawl, interpret, and rank a site so it can earn more organic visibility.
```

### 통계 블록

```markdown
According to [Source], [specific statistic] as of [year].
```

### 전문가 인용

```markdown
"[Quote]," says [Name], [Title] at [Organization].
```

### Q/A 블록

```markdown
### How long does SEO take to show results?

SEO usually takes 3-6 months to show meaningful results on a new site, though low-competition queries can move faster.
```

### 비교 표

```markdown
| Factor | Option A | Option B |
| --- | --- | --- |
| Best for | ... | ... |
| Time to value | ... | ... |
```

---

## 3. AI engine별 content preference 요약

| Engine | 선호 신호 |
| --- | --- |
| Google AI Overview | direct answer, tables, FAQ, structured data, authority |
| ChatGPT browse | factual density, citations, freshness, answer fit |
| Perplexity | recent sources, quotable blocks, strong structure, FAQ |
| Claude | factual density, clear structure, unambiguous definitions |
---

## 3-1. CORE-EEAT GEO-First Targets

AI engine 인용에 가장 영향력 있는 항목들이다.

**Top 6 Priority Items**:

| 순위 | ID | 기준 | 중요한 이유 |
|------|----|------|------------|
| 1 | C02 | 첫 150 단어 내 직답 | 모든 engine이 첫 paragraph에서 추출한다 |
| 2 | C09 | Schema 포함 Structured FAQ | AI follow-up queries에 직접 매칭된다 |
| 3 | O03 | 데이터를 표로, prose 대신 | 가장 추출 가능한 구조화 형식이다 |
| 4 | O05 | JSON-LD Schema Markup | AI가 콘텐츠 타입을 이해하는 데 도움이 된다 |
| 5 | E01 | 원본 first-party 데이터 | AI가 exclusive, verifiable source를 선호한다 |
| 6 | O02 | Key Takeaways / Summary Box | AI summary citations의 첫 선택이다 |

**All GEO-First Items**:
- Content: C02, C04, C05, C07, C08, C09
- Organization: O02, O03, O04, O05, O06, O09
- Research: R01, R02, R03, R04, R05, R07, R09
- Evidence: E01, E02, E03, E04, E06, E08, E09, E10
- Experience: Exp10
- Expertise: Ept05, Ept08
- Authority: A08

### 빠른 판단 기준

- C02 (직답)이 없으면 AI 인용 확률이 크게 낮아진다
- O03 (표)는 prose보다 3 배 더 추출 가능성이 높다
- FAQ Schema는 follow-up queries에 직접 매칭된다
- First-party data는 다른 source와 차별화된 가치를 만든다
- Summary Box는 AI summary의 기본 소스가 된다

**AI Engine별 우선순위**:

| Engine | Priority Items |
|--------|----------------|
| Google AI Overview | C02, O03, O05, C09 |
| ChatGPT Browse | C02, R01, R02, E01 |
| Perplexity AI | E01, R03, R05, Ept05 |
| Claude | R04, Ept08, Exp10, R03 |
---

## 4. E-E-A-T content checks

- author identity or clear ownership
- citations to trustworthy sources
- recent timestamps when freshness matters
- first-party examples or tested claims when available
- limitations or uncertainty stated honestly

### 주의

- 과장된 권위 톤은 신뢰를 깎는다
- evidence 없이 confident tone만 세우면 역효과다

---

## 5. FAQ schema starter

visible FAQ와 질문-답변이 있을 때만 붙인다.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does SEO take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO usually takes 3-6 months to show meaningful results on a new site."
      }
    }
  ]
}
```

---

## 6. quotable content checklist

- [ ] key terms are clearly defined
- [ ] at least several specific statistics are included where relevant
- [ ] major claims have sources
- [ ] headings match common user questions
- [ ] tables or lists are used where they help extraction
- [ ] answer-first structure appears early
- [ ] keyword stuffing is absent

---

## 7. GEO 최적화 6 가지 기법

### 1. Definition Optimization

AI systems love clear, quotable definitions.

**Template**:
> "[Term] is [clear category/classification] that [primary function/purpose], [key characteristic or benefit]."

**Before** (Weak for GEO):
> SEO is really important for businesses and involves various techniques to improve visibility online through search engines.

**After** (Strong for GEO):
> **Search Engine Optimization (SEO)** is the practice of optimizing websites and content to rank higher in search engine results pages (SERPs), increasing organic traffic and visibility.

**Checklist for GEO-Optimized Definitions**:
- [ ] Starts with the term being defined
- [ ] Provides clear category (what type of thing it is)
- [ ] Explains primary function or purpose
- [ ] Uses precise, unambiguous language
- [ ] Can stand alone as a complete answer
- [ ] Is 25-50 words for optimal citation length

**빠른 판단 기준**:
- 정의가 25-50 단어 길이이면 AI 인용에 최적이다
- category와 purpose가 명확하면 extraction 확률이 높아진다
- ambiguous language는 AI가 misinterpret할 가능성이 있다
- standalone answer 형태면 context 없이도 인용 가능하다

### 2. Quotable Statement Creation

AI systems cite specific, standalone statements.

**Types of Quotable Statements**:

1. **Statistics**: "According to [Source], [specific statistic] as of [date]."
2. **Facts**: "[Subject] was [fact], according to [authoritative source]."
3. **Comparisons**: "Unlike [A], [B] [specific difference], which means [implication]."
4. **How-to Steps**: "To [achieve goal], [step 1], then [step 2], and finally [step 3]."

**Before** (Not quotable):
> Email marketing is pretty effective and lots of companies use it.

**After** (Quotable):
> Email marketing delivers an average ROI of $42 for every $1 spent, making it one of the highest-performing digital marketing channels.

**빠른 판단 기준**:
- Statistics는 source, specific statistic, date를 모두 포함한다
- Facts는 authoritative source와 함께 제시한다
- Comparisons는 specific difference와 implication을 명시한다
- How-to Steps는 3 단계 이내로 clear하게 작성한다
- vague claims를 specific numbers로 변환하면 quotable이 된다

### 3. Authority Signal Enhancement

**Expert Attribution**:
> "AI will transform how we search for information," says Dr. Jane Smith, AI Research Director at Stanford University.

**Source Citations**:

Before:
> Studies show that most people prefer video content.

After:
> According to Wyzowl's 2024 Video Marketing Statistics report, 91% of consumers want to see more online video content from brands.

**Authority Elements to Add**:
- [ ] Author byline with credentials
- [ ] Expert quotes with attribution
- [ ] Citations to peer-reviewed research
- [ ] References to recognized authorities
- [ ] Original data or research
- [ ] Case studies with named companies
- [ ] Industry statistics with sources

**빠른 판단 기준**:
- Expert Attribution은 이름, Title, Organization을 모두 포함한다
- Source Citations은 source name, year, specific statistic을 명시한다
- Author byline with credentials는 페이지에 필수다
- Original data는 다른 source와 차별화된 가치를 만든다
- peer-reviewed research citations는 신뢰도를 높인다

### 4. Structure Optimization

AI systems parse structured content more effectively.

**Q&A Format**:
```markdown
## What is [Topic]?

[Direct answer in 40-60 words]

## How does [Topic] work?

[Clear explanation with steps if applicable]

## Why is [Topic] important?

[Specific reasons with evidence]
```

**Comparison Tables**:
```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| [Feature 1] | [Specific value] | [Specific value] |
| **Best for** | [Use case] | [Use case] |
```

**Numbered Lists**:
```markdown
1. **Step 1: [Action]** - [Brief explanation]
2. **Step 2: [Action]** - [Brief explanation]
3. **Step 3: [Action]** - [Brief explanation]
```

**빠른 판단 기준**:
- Q&A Format은 40-60 단어 direct answer를 사용한다
- Comparison Tables는 Feature, Specific value, Best for를 포함한다
- Numbered Lists는 Action과 Brief explanation을 명시한다
- structured content는 prose보다 extraction 확률이 3 배 높다
- AI systems는 headings, tables, lists를 priority로 parse한다

### 5. Factual Density Improvement

AI systems prefer fact-rich content over opinion-heavy content.

**Content Transformation**:

**Low factual density**:
> SEO tools are generally quite helpful for improving rankings.

**High factual density**:
> A 2024 study of 10,000 websites found that pages using SEO tools ranked 2.3x higher on average than those without. Specifically, sites using Ahrefs saw a 34% increase in organic traffic within 6 months.

**Transformation Rules**:
- Replace vague claims with specific numbers
- Add sources and dates to statistics
- Include comparison baselines
- Name specific tools, companies, or studies

**빠른 판단 기준**:
- Low factual density는 vague claims만 있는 상태다
- High factual density는 specific numbers, sources, dates를 포함한다
- "generally quite helpful" → "2.3x higher"로 변환한다
- comparison baselines를 추가하면 credibility가 높아진다
- opinion-heavy content는 AI 인용 확률이 낮아진다

### 6. FAQ Schema Implementation

visible FAQ 와 질문 - 답변이 있을 때만 붙인다.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does SEO take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SEO usually takes 3-6 months to show meaningful results on a new site."
      }
    }
  ]
}
```

**FAQ Best Practices**:
- Use visible Q&A text on the page first
- Match questions to actual user queries
- Keep answers concise (40-60 words)
- Include numbers and specifics where possible

### 빠른 판단 기준

- visible FAQ 없이 Schema만 추가하면 Google guideline 위반이다
- 답변 길이가 40-60 단어를 넘으면 extraction 효율이 낮아진다
- 실제 user queries와 매칭되는 질문을 사용한다
- 숫자와 specifics를 포함하면 인용 가능성이 높아진다
- FAQ Schema는 follow-up queries에 직접 매칭된다

---

### 섹션 7 빠른 판단 기준

- Definition Optimization은 25-50 단어로 명확하게 작성한다
- Quotable Statement는 숫자, 출처, 날짜를 포함한다
- Authority Signal은 expert attribution과 source citations를 추가한다
- Structure Optimization은 Q&A format, comparison tables, numbered lists를 사용한다
- Factual Density는 vague claims 대신 specific numbers로 변환한다
- FAQ Schema는 visible Q&A text와 함께 사용한다

## 8. GEO 점수 (8 개 인자)

콘텐츠의 AI 인용 준비도를 평가하는 8 개 인자다.

| GEO 인자 | 현재 점수 (1-10) | 비고 |
|---------|-----------------|------|
| 명확한 정의 | [X] | [비고] |
| 인용 가능한 문장 | [X] | [비고] |
| 사실 밀도 | [X] | [비고] |
| 출처 citations | [X] | [비고] |
| Q&A format | [X] | [비고] |
| 권위 신호 | [X] | [비고] |
| 콘텐츠 freshness | [X] | [비고] |
| 구조 clarity | [X] | [비고] |
| **GEO Readiness** | **[avg]/10** | **인자 평균** |

### 빠른 판단 기준

- GEO Readiness 7 점 미만이면 6 가지 기법부터 적용한다
- 명확한 정의와 인용 가능한 문장이 가장 영향력이 크다
- AI engine 별 우선순위 항목을 먼저 최적화한다
- 사실 밀도가 낮으면 opinion-heavy 콘텐츠로 평가된다
- 출처 citations가 없으면 신뢰도가 낮아진다