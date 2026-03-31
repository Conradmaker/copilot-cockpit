---
name: seo-content
description: "SEO and GEO content optimization for search intent, title/meta tags, on-page structure, featured snippets, FAQ design, internal linking, and AI-citable writing. Use this skill when asked to write or optimize SEO content, draft keyword-targeted posts, improve CTR, rewrite titles or meta tags, fix social preview tags, audit on-page SEO, align pages to search intent, add FAQ or comparison sections, refresh articles, reduce cannibalization, strengthen internal links, or make content more quotable by AI. Always consult this skill for search-intent-driven content work, even if the user only mentions a blog post, meta tag, FAQ, snippet, or GEO. For crawlability, indexation, schema validation, Core Web Vitals, hreflang, or bot access use seo-technical. For generic content structure use writing-content. Triggers on: seo content, on-page SEO, search intent, keyword, title tag, meta description, featured snippet, FAQ, CTR, Open Graph, GEO, AI citation, 콘텐츠 SEO, 온페이지 SEO, 검색 의도, 키워드, 타이틀, 메타 설명."
disable-model-invocation: false
user-invocable: false
---

# 콘텐츠 SEO·GEO 최적화 가이드 (seo-content)

## 목표

검색 의도에 맞는 콘텐츠를 설계하고, 메타데이터와 on-page 구조를 정리하고, 클릭과 인용을 동시에 높이는 것이 목표다. 이 스킬은 단순히 "SEO 글을 쓴다"가 아니라 **search intent -> SERP pattern -> title/meta/social tags -> on-page structure -> snippet formats -> GEO citation signals -> refresh loop**를 한 흐름으로 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 글을 쓰거나 진단하기 전에는 아래 reference 문서를 직접 읽고, 현재 작업이 new draft, existing-page optimization, on-page audit, meta tag rewrite, GEO uplift 중 무엇인지 먼저 좁힌 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 7대 핵심 단계

### 1. search intent와 page type을 먼저 고정한다

같은 키워드라도 독자가 원하는 결과가 다르면 페이지 형태가 달라진다. 정보형 쿼리에 판매 페이지를 쓰면, title이나 keyword placement를 아무리 다듬어도 맞지 않는다.

- informational, commercial, transactional, local, navigational intent를 먼저 나눈다
- blog, comparison, landing page, product page, service page, FAQ page 중 어떤 유형인지 고정한다
- 신규 초안인지, 기존 페이지 최적화인지, audit인지 함께 밝힌다

#### 빠른 판단 기준

- search intent가 안 보이면 title 작성부터 하지 않는다
- page type을 한 문장으로 말할 수 없으면 scope가 흐린 상태다
- keyword 하나만 있고 독자 상황이 없으면 [references/01-intent-serp-briefing.md](references/01-intent-serp-briefing.md)부터 본다

→ 상세: [references/01-intent-serp-briefing.md](references/01-intent-serp-briefing.md)

### 2. SERP와 query coverage를 먼저 본다

SEO 콘텐츠는 빈 페이지에서 시작하지 않는다. 현재 상위 결과가 어떤 구조인지, 어떤 질문을 커버하는지, 어떤 angle이 과포화인지 봐야 한다.

- top results format, common sections, average depth, featured snippets, PAA questions를 확인한다
- primary keyword 하나보다 query family 전체를 본다
- content angle은 "무엇을 쓸까"보다 "무엇을 다르게 줄까"에 가깝다
- 같은 사이트 안의 기존 cluster와 cannibalization risk도 같이 확인한다

#### 빠른 판단 기준

- 경쟁 페이지가 전부 comparison인데 혼자 glossary형 정의만 쓰면 mismatch 가능성이 높다
- PAA 질문이 반복되면 FAQ 또는 H2 구조에 반영한다
- 이미 같은 cluster 안에 비슷한 페이지가 있으면 cannibalization을 먼저 의심한다

→ 상세: [references/01-intent-serp-briefing.md](references/01-intent-serp-briefing.md)

### 3. title, meta, social tags는 copy와 structure를 같이 본다

CTR 문제는 title tag만의 문제가 아니다. meta description, Open Graph, Twitter card, brand positioning, year modifier, bracket, query fit를 함께 봐야 한다.

- title은 intent fit, keyword position, specificity, CTR signal을 함께 본다
- meta description은 요약이 아니라 click reason을 제공해야 한다
- Open Graph와 Twitter card는 social preview 맥락에 맞춰 별도로 최적화할 수 있다
- A/B test는 한 번에 한 변수만 바꾼다

#### 빠른 판단 기준

- title이 맞아도 description이 generic이면 CTR이 약하다
- OG/Twitter는 title/meta를 그대로 복붙하지 않아도 된다
- position이 비슷한데 CTR만 낮다면 meta and title rewrite 우선순위가 높다

→ 상세: [references/02-title-meta-social-tags.md](references/02-title-meta-social-tags.md)

### 4. on-page는 구조, 키워드, 링크, 이미지, technical-on-page를 함께 본다

온페이지 최적화는 keyword density만의 문제가 아니다. title, H1, H2, intro, URL slug, internal/external links, image alt, FAQ, schema opportunity까지 한 세트다.

- H1-H3 hierarchy와 section chunking을 먼저 본다
- keyword는 placement와 semantic coverage가 중요하다
- internal links는 양보다 relevance와 anchor text를 본다
- image alt와 filename은 보조 신호지만 누적되면 차이를 만든다
- external links, quick summary blocks, FAQ visibility처럼 trust와 snippet 기회를 높이는 요소도 같이 본다

#### 빠른 판단 기준

- H1은 하나여야 하고 primary keyword와 어긋나지 않아야 한다
- 첫 100단어에 핵심 답이 없으면 informational 쿼리에서 약하다
- title/meta/header/content/link/image/technical 중 어디서 점수를 잃는지 분해해야 한다

→ 상세: [references/03-on-page-structure-scoring.md](references/03-on-page-structure-scoring.md)

### 5. 콘텐츠 템플릿과 snippet 포맷을 쿼리에 맞춘다

featured snippet과 AI extractability는 형식 영향을 많이 받는다. 정의형, 리스트형, 표형, how-to형, comparison형은 각각 맞는 구조가 있다.

- definition query는 40-60단어 직답 블록이 좋다
- comparison query는 표와 verdict 구조가 강하다
- how-to query는 번호 매긴 단계와 verify가 필요하다
- FAQ는 visible content와 Q/A 구조가 맞아야 한다

#### 빠른 판단 기준

- comparison 주제에 표가 없으면 snippet 기회가 약해진다
- how-to인데 numbered steps가 없으면 구조 mismatch 가능성이 높다
- FAQ는 단순 리스트가 아니라 실제 질문 문장과 답이 필요하다

→ 상세: [references/04-content-templates-snippets.md](references/04-content-templates-snippets.md)

### 6. GEO와 E-E-A-T 신호를 콘텐츠 안에 심는다

AI citation을 높이는 건 별도의 마법이 아니다. 정의, 통계, 출처, 전문가 인용, answer-first, factual density, quotable sentence 같은 신호를 콘텐츠 안에 넣는 일이다.

- Princeton GEO methods는 cite sources, statistics, quotation, authoritative tone, easy language, technical terms, unique words, fluency를 중심으로 본다
- keyword stuffing은 traditional SEO뿐 아니라 GEO에도 불리하다
- AI engine마다 좋아하는 형식이 약간 다르지만, 공통분모는 clear answers + verifiable facts + extractable structure다
- author identity, first-party data, recent timestamps, limitation disclosure 같은 E-E-A-T 신호도 같이 점검한다

#### 빠른 판단 기준

- 정의가 흐리고 수치와 출처가 없으면 AI-citable likelihood가 낮다
- FAQ, table, list, summary box가 없으면 extractability가 약해진다
- AI visibility를 원하면서 content freshness를 무시하면 결과가 약해질 수 있다

→ 상세: [references/05-geo-eeat-citation-patterns.md](references/05-geo-eeat-citation-patterns.md)

### 7. 최종 리뷰와 refresh loop를 문서화한다

SEO 콘텐츠는 발행으로 끝나지 않는다. pre-publish check, CTR diagnosis, low-performing page refresh, stale stats replacement, snippet retest가 필요하다.

- final review는 score와 action list로 끝내는 편이 낫다
- CTR이 낮을 때는 title/meta, SERP fit, position, rich result 유무를 같이 본다
- refresh는 새 글 작성이 아니라 기존 asset의 ROI를 올리는 작업이다
- AI스러운 filler와 과장된 문장을 마지막에 한 번 더 제거한다

#### 빠른 판단 기준

- published page인데 6-12개월 이상 update signal이 없으면 refresh 후보일 수 있다
- position은 괜찮은데 CTR이 낮으면 title/meta loop를 먼저 본다
- content가 synthetic하게 느껴지면 writing-clearly 쪽 품질 게이트를 같이 적용한다

→ 상세: [references/07-final-review-refresh.md](references/07-final-review-refresh.md)

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/01-intent-serp-briefing.md](references/01-intent-serp-briefing.md) | search intent, page type, keyword map, SERP structure + 섹션 7 (CORE-EEAT 사전 작성 체크리스트) |
| [references/02-title-meta-social-tags.md](references/02-title-meta-social-tags.md) | title, meta description, OG, Twitter card, CTR test + Title/Meta Formulas, A/B 테스트 방법론 |
| [references/03-on-page-structure-scoring.md](references/03-on-page-structure-scoring.md) | on-page SEO audit, scoring, keyword placement, links, images + 섹션 8,9 (Scoring Rubric, 점수 보고서 템플릿) |
| [references/04-content-templates-snippets.md](references/04-content-templates-snippets.md) | blog/comparison/listicle/how-to/FAQ 구조와 snippet formats를 고를 때 |
| [references/05-geo-eeat-citation-patterns.md](references/05-geo-eeat-citation-patterns.md) | GEO uplift, AI citation, answer-first + 섹션 3-1 (GEO-First Targets), 섹션 7 (GEO 최적화 6 가지 기법), 섹션 8 (GEO 점수) |
| [references/06-research-and-sourcing.md](references/06-research-and-sourcing.md) | stats, expert quote, first-party data, claim inventory를 준비할 때 |
| [references/07-final-review-refresh.md](references/07-final-review-refresh.md) | pre-publish QA, CTR diagnosis, refresh backlog, AI-pattern sanity check를 돌릴 때 |
| [references/08-internal-linking.md](references/08-internal-linking.md) | site architecture, authority distribution, orphan pages, topic cluster, anchor text optimization |

### 추천 로드 순서

- new SEO draft: `01 -> 04 -> 02 -> 06 -> 05 -> 07`
- title/meta rewrite: `01 -> 02 -> 07`
- on-page audit: `01 -> 03 -> 08 -> 07`
- GEO optimization: `01 -> 05 -> 06 -> 07`
- internal linking audit: `01 -> 03 -> 08`
- refresh existing page: `01 -> 03 -> 02 -> 05 -> 08 -> 07`

---

## 응답 패턴

### 1. 새 SEO 콘텐츠 요청

1. intent and page type
2. keyword and SERP summary
3. title/meta options
4. outline or draft
5. GEO/EEAT notes
6. final checklist

### 2. on-page audit 요청

1. overall score or summary
2. score breakdown
3. priority issues
4. recommended fixes by area
5. quick wins

### 3. meta/CTR 개선 요청

1. current problem framing
2. title options
3. meta description options
4. OG/Twitter block
5. A/B test hypothesis

---

## 범위

- crawlability, indexation, rendering, schema validation, Core Web Vitals, HTTPS, hreflang, bot access, platform indexing → seo-technical
- generic blog/article/social structure and voice → writing-content
- source gathering, fact-checking, research brief creation → research-content-source
- prose cleanup, AI-pattern removal at sentence level → writing-clearly

이 스킬은 검색 의도 기반 콘텐츠 최적화와 GEO-friendly formatting을 담당한다. crawl/index/render/security 같은 사이트 메커니즘까지 한 스킬에 넣지 않는다.