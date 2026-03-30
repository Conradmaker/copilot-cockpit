# Title, Meta, and Social Tags Guide

## 목표

title tag, meta description, Open Graph, Twitter card를 intent와 CTR 관점에서 최적화한다.

---

## 1. title tag 기본 규칙

| 항목 | 기준 |
| --- | --- |
| 길이 | 보통 50-60자 권장 |
| keyword position | primary keyword는 가능하면 앞쪽 |
| intent fit | SERP 기대와 맞아야 함 |
| click reason | benefit, specificity, question, contrast 중 하나 |
| brand | 일반적으로 뒤쪽 |

### title formula 예시

| 유형 | 템플릿 |
| --- | --- |
| Guide | How to [Achieve Result] ([Year]) |
| Definition | What Is [Topic]? [Short Clarifier] |
| Comparison | [A] vs [B]: [Differentiator] |
| List | [N] [Topic] Tips That [Result] |
| Problem | Why [Problem Exists] (And How to Fix It) |

### Title Tag Formulas by Content Type

#### Informational Content

| # | Formula | Example |
|---|---------|---------|
| 1 | How-To + Year | How to Build Backlinks in 2026 |
| 2 | How-To + Result | How to Write Meta Tags (Rank Higher) |
| 3 | Definitive Guide | The Definitive Guide to Technical SEO |
| 4 | Complete Guide | Schema Markup: The Complete Guide (2026) |
| 5 | Beginner's Guide | SEO for Beginners: Rank in 30 Days |
| 6 | What Is | What Is E-E-A-T? Google's Quality Standard |
| 7 | Step-by-Step | Link Building: A Step-by-Step Guide |

#### Listicle Content

| # | Formula | Example |
|---|---------|---------|
| 8 | Numbered Tips | 12 On-Page SEO Tips That Boost Rankings |
| 9 | Best Of | 9 Best SEO Tools in 2026 (Expert Tested) |
| 10 | Ways To | 7 Ways to Increase Organic Traffic This Month |
| 11 | Mistakes | 10 Title Tag Mistakes That Hurt Your CTR |
| 12 | Secrets | 5 SEO Secrets Top Agencies Use |

#### Comparison Content

| # | Formula | Example |
|---|---------|---------|
| 13 | A vs B | Ahrefs vs SEMrush: Which Tool Is Better? |
| 14 | A vs B + Year | WordPress vs Webflow (2026): Honest Comparison |
| 15 | Alternatives | 7 Best Ahrefs Alternatives in 2026 |

#### Commercial / Transactional Content

| # | Formula | Example |
|---|---------|---------|
| 16 | Product + Benefit | SEO Audit Tool - Find Issues in Minutes |
| 17 | Review | Surfer SEO Review (2026): Worth the Price? |
| 18 | Free Tool | Free Meta Tag Generator: Preview Your SERP Listing |

#### Problem-Awareness Content

| # | Formula | Example |
|---|---------|---------|
| 19 | Warning | Warning: These SEO Tactics Will Get You Penalized |
| 20 | Why + Problem | Why Your Meta Descriptions Are Ignored (And How to Fix It) |
| 21 | Stop Doing | Stop Keyword Stuffing: What to Do Instead |

### 빠른 판단 기준

- Informational 콘텐츠에는 How-To, Guide, What Is 형식이 잘 맞는다
- Listicle 콘텐츠에는 숫자, Best Of, Mistakes 형식이 잘 맞는다
- Comparison 콘텐츠에는 A vs B 형식이 필수다
- Commercial 콘텐츠에는 Product + Benefit 또는 Review 형식이 잘 맞는다
- Problem-Awareness 콘텐츠에는 Warning, Why + Problem 형식이 잘 맞는다

---

## 2. meta description 기본 규칙

| 항목 | 기준 |
| --- | --- |
| 길이 | 보통 150-160자 |
| keyword | 자연스럽게 1회 포함 |
| 구조 | what + why + CTA |
| 역할 | ranking보다 CTR preview에 가깝다 |

### description framework

- Benefit + proof + CTA
- Problem + promise + CTA
- What you'll learn + scope + CTA

### Meta Description Templates by Content Type

#### Blog Posts / Articles

| # | Template | Character Count |
|---|----------|-----------------|
| 1 | Learn [topic] with our [qualifier] guide. Covers [point 1], [point 2], and [point 3]. [CTA]. | ~140-155 |
| 2 | [Question]? This [year] guide explains [what], [why], and [how]. Get actionable tips now. | ~130-150 |
| 3 | Discover [N] [adjective] [topic] strategies that [result]. Backed by [proof element]. Read the full guide. | ~145-160 |

#### Product / Service Pages

| # | Template | Character Count |
|---|----------|-----------------|
| 4 | [Product] helps you [benefit]. [Feature 1], [Feature 2], [Feature 3]. [Price/offer]. [CTA]. | ~140-155 |
| 5 | Looking for [solution]? [Product] [key differentiator]. Trusted by [social proof]. [CTA]. | ~130-150 |
| 6 | [Product] - [primary benefit] in [timeframe]. [Star rating] from [N]+ reviews. [CTA]. | ~130-145 |

#### Comparison Pages

| # | Template | Character Count |
|---|----------|-----------------|
| 7 | [A] vs [B]: which is better for [use case]? We compared [criteria]. See the winner + detailed breakdown. | ~145-160 |
| 8 | Comparing [A] and [B] on [criteria 1], [criteria 2], and price. Our [year] verdict inside. | ~130-145 |

### 빠른 판단 기준

- Blog Posts에는 Learn, Question, Discover 프레임이 잘 맞는다
- Product Pages에는 benefit + features + CTA 구조가 필수다
- Comparison Pages에는 A vs B + criteria + winner 구조가 필수다
- 길이는 140-160 자 사이에서 CTA까지 포함한다
- keyword는 자연스럽게 1 회 포함하고 과도한 repetition은 피한다

### 예시

```text
Compare the best technical SEO tools for 2026. See pricing, strengths, and use cases so you can pick the right option faster.
```

---

## 3. CTR 개선 신호

| 요소 | 기대 효과 |
| --- | --- |
| 숫자 | specificity 증가 |
| current year | freshness signal |
| brackets / parenthetical | extra value signal |
| clear audience | relevance 증가 |
| question format | curiosity 증가 |

### 주의

- clickbait는 금지
- title promise와 본문 delivery가 맞지 않으면 long-term 성과가 나빠진다

---

## 4. Open Graph and Twitter cards

### 기본 블록

```html
<title>[Optimized Title]</title>
<meta name="description" content="[Optimized Description]">
<link rel="canonical" href="[Canonical URL]">

<meta property="og:type" content="article">
<meta property="og:url" content="[URL]">
<meta property="og:title" content="[OG Title]">
<meta property="og:description" content="[OG Description]">
<meta property="og:image" content="[Image URL]">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Twitter Title]">
<meta name="twitter:description" content="[Twitter Description]">
<meta name="twitter:image" content="[Image URL]">
```

### 이미지 기준

| Platform | 권장 크기 |
| --- | --- |
| Facebook / LinkedIn | 1200x630 |
| Twitter/X | 1200x600 또는 1200x630 |
| Pinterest | 1000x1500 |

### page-type templates

| Page type | Title template | Description template |
| --- | --- | --- |
| Homepage | [Brand] - [Primary Value Prop] | [Brand] helps [audience] [goal]. [CTA] |
| Product | [Product] - [Key Benefit] | [Product] [features]. [Offer]. [CTA] |
| Blog | [How to/What is/Number] [Keyword] | [What they'll learn]. [Key points]. [CTA] |
| Service | [Service] in [Location] - [Brand] | [Service description]. [Differentiator]. [CTA] |

---

## 5. A/B testing 최소 규칙

1. title 또는 description 중 하나만 바꾼다
2. baseline을 30일 이상 본다
3. re-crawl 이후 데이터를 본다
4. position이 크게 바뀌지 않은 구간에서 CTR을 비교한다
### A/B 테스트 방법론

#### 테스트 전 준비

1. **베이스라인 메트릭** — 현재 CTR, 평균 position, impressions, clicks를 기록한다 (최소 30 일 데이터).
2. **가설** — 무엇이 바뀔지, 왜 바뀔지 명시한다: "타이틀에 숫자를 추가하면 CTR이 X% 증가할 것이다. 이 SERP position에서 listicle 타이틀이 generic 타이틀보다 성과가 좋기 때문이다."
3. **단일 변수** — 한 테스트에서 하나의 요소만 변경한다 (title 또는 description, 둘 다 변경하지 않음).
4. **최소 샘플** — 테스트 기간에 페이지가 최소 1,000 impressions을 축적한 후 결론을 도출한다.

#### 테스트 실행 단계

| 단계 | 작업 | 기간 |
|------|------|------|
| 1 | 베이스라인 CTR 30 일 기록 | 30 일 |
| 2 | 타이틀/디스크립션 변경 적용 | Day 0 |
| 3 | Google re-crawl 및 SERP 업데이트 대기 | 3-7 일 |
| 4 | 새 CTR 모니터링 (첫 7 일 제외) | 30+ 일 |
| 5 | 같은 avg. position에서 새 CTR vs 베이스라인 비교 | — |
| 6 | 결정: 유지, 롤백, 또는 반복 | — |

#### 무엇을 테스트할지 (우선순위)

| 우선순위 | 요소 | 테스트 변수 | 예상 효과 |
|----------|------|------------|----------|
| 1 | Title tag | 숫자 추가/제거 | +15-25% CTR |
| 2 | Title tag | year 추가/제거 | +10-15% CTR |
| 3 | Title tag | brackets/parentheses 추가 | +10-38% CTR |
| 4 | Title tag | power word 변경 | +5-12% CTR |
| 5 | Title tag | keyword 위치 변경 | +5-10% CTR |
| 6 | Meta description | CTA 추가 | +5-10% CTR |
| 7 | Meta description | 숫자/통계 추가 | +5-15% CTR |
| 8 | Meta description | 감정 tone 변경 | +3-8% CTR |

#### 통계적 유의성 체크리스트

- [ ] 테스트 기간 최소 1,000 impressions
- [ ] 테스트 최소 30 일 실행 (re-crawl 후)
- [ ] 평균 position이 2 position 이상 이동하지 않음
- [ ] 테스트 기간에 주요 알고리즘 업데이트 없음
- [ ] 계절적 bias 없음 (연도별 비교)
- [ ] CTR 변화가 10% relative difference 초과
### test backlog 예시

- 숫자 추가 vs 미추가
- year modifier 추가 vs 미추가
- benefit-led title vs question-led title
- CTA 강한 description vs 정보형 description
