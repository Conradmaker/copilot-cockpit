# On-Page Structure and Scoring Guide

## 목표

title, meta, headers, content, keywords, links, images, technical-on-page 요소를 분해해서 점수와 우선순위를 만든다.

---

## 1. on-page audit 영역

| 영역 | 핵심 질문 |
| --- | --- |
| Title | keyword, intent, CTR signal이 맞는가 |
| Meta description | click reason과 정확성이 있는가 |
| Headers | H1-H2-H3 구조와 topic coverage가 맞는가 |
| Content | depth, clarity, examples, freshness가 충분한가 |
| Keywords | placement와 semantic coverage가 적절한가 |
| Links | internal/external link quality가 충분한가 |
| Images | alt, filename, size, format이 적절한가 |
| Technical on-page | URL, canonical, mobile, schema 등 page-level hygiene가 맞는가 |

---

## 2. 가중치 예시

| Section | Weight |
| --- | --- |
| Title tag | 15% |
| Meta description | 5% |
| Header structure | 10% |
| Content quality | 25% |
| Keyword optimization | 15% |
| Internal/external links | 10% |
| Image optimization | 10% |
| Technical on-page | 10% |

### overall score 계산

```text
Overall Score = Sum(section_score x section_weight) x 10
```

---

## 3. keyword placement checklist

- primary keyword in title
- primary keyword in H1
- primary keyword in first 100 words
- primary keyword in at least one H2 when natural
- primary keyword in conclusion when natural
- primary keyword in meta description
- secondary keywords in H2s/H3s
- related terms throughout body
- keyword in URL slug when appropriate
- at least one relevant image alt containing the keyword naturally

### density note

keyword density는 hard rule이 아니다. 0.5-2.5% 안쪽이면 자연스러운 경우가 많지만, semantic coverage가 더 중요하다.

---

## 4. header 구조 기준

- H1은 하나
- H1은 page promise와 keyword를 함께 반영
- H2는 주요 subtopics를 덮어야 함
- H3는 H2 안에서만 내려감
- heading은 styling이 아니라 structure를 설명해야 함

---

## 5. internal and external link 기준

### internal links

- 1000단어 기준 3-5개 이상을 기본값으로 보되, relevance가 더 중요하다
- anchor text는 "click here"보다 destination meaning을 드러내야 한다
- orphan page를 줄이고 cluster를 연결하는 방향으로 링크한다

### external links

- 핵심 주장에 authoritative source를 연결한다
- source dump가 아니라 claim support 용도로 쓴다

---

## 6. image 기준

- 모든 이미지에 alt text
- alt는 설명적이어야 하고, keyword는 자연스러운 경우만 포함
- file name은 `img1234.jpg`보다 descriptive slug
- 가능하면 modern format(WebP/AVIF)

---

## 7. score report 템플릿

```markdown
## On-Page Score

| Area | Score | Key finding |
| --- | --- | --- |
| Title | 8/10 | strong keyword placement, weak specificity |
| Meta | 6/10 | accurate but generic CTA |
| Headers | 9/10 | clean hierarchy |
| Content | 7/10 | depth okay, missing first-party data |
| Keywords | 8/10 | solid placement |
| Links | 5/10 | internal links underdeveloped |
| Images | 6/10 | alt text missing on several images |
| Technical | 7/10 | canonical present, schema weak |
```

---

## 8. Scoring Rubric (상세 기준)

### Section 1: Title Tag (Weight: 15%, Max: 15 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Keyword presence | 3 | Primary keyword appears in title |
| Keyword position | 2 | Primary keyword in first half of title |
| Length optimization | 2 | Between 50-60 characters |
| Uniqueness | 2 | Title is unique across the site |
| Compelling copy | 2 | Includes benefit, modifier, or hook |
| Intent match | 2 | Title matches search intent accurately |
| Brand inclusion | 1 | Brand name present (at end) |
| No truncation risk | 1 | Displays fully in SERP without cutoff |

**Calibration Examples**:
- **15/15**: "Keyword Research: 7 Proven Methods to Find Low-Competition Keywords | Brand" (58 chars, keyword at front, benefit-driven)
- **11/15**: "The Complete Guide to Keyword Research for Beginners" (52 chars, keyword present but not at front)
- **7/15**: "Keyword Research" (too short, no benefit, generic)
- **3/15**: "Blog Post #47 - Untitled" (no keyword, not descriptive)

### Section 2: Meta Description (Weight: 5%, Max: 5 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Keyword inclusion | 1 | Primary keyword appears naturally |
| Length optimization | 1 | Between 150-160 characters |
| Call-to-action | 1 | Contains explicit or implicit CTA |
| Unique description | 1 | Not duplicated from other pages |
| Accurate summary | 1 | Accurately describes page content |

### Section 3: Header Structure (Weight: 10%, Max: 10 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Single H1 present | 2 | Exactly one H1 on the page |
| H1 contains keyword | 2 | Primary keyword in H1 text |
| Logical hierarchy | 2 | No skipped levels (H1→H2→H3) |
| H2s cover key subtopics | 2 | H2s address main topic facets |
| Descriptive headers | 1 | Headers describe section content clearly |
| Keyword variations in H2s | 1 | Secondary keywords or LSI terms in subheadings |

### Section 4: Content Quality (Weight: 25%, Max: 25 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Sufficient length | 4 | Meets minimum for query type |
| Comprehensive coverage | 4 | Covers all major subtopics |
| Unique value | 4 | Original insights, data, or perspective |
| Up-to-date information | 3 | Statistics and references are current |
| Proper formatting | 3 | Uses lists, tables, bold, images |
| Readability | 3 | Appropriate reading level |
| E-E-A-T signals | 4 | Author byline, credentials, sources |

**Content Length Benchmarks**:

| Query Type | Minimum for 4/4 | Minimum for 3/4 | Minimum for 2/4 | Below 1/4 |
|-----------|-----------------|-----------------|-----------------|-----------|
| Informational | 1,500+ words | 1,000-1,499 | 500-999 | <500 |
| Commercial | 1,200+ words | 800-1,199 | 400-799 | <400 |
| Transactional | 500+ words | 350-499 | 200-349 | <200 |
| Local | 400+ words | 250-399 | 150-249 | <150 |

### Section 5: Keyword Optimization (Weight: 15%, Max: 15 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Primary in title | 3 | Primary keyword in title tag |
| Primary in H1 | 3 | Primary keyword in H1 |
| Primary in first 100 words | 3 | Appears early in content |
| Primary in H2s | 2 | In at least one H2 when natural |
| Primary in conclusion | 2 | In conclusion section |
| Secondary keywords | 2 | In H2s/H3s throughout |

### Section 6: Internal/External Links (Weight: 10%, Max: 10 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Internal links present | 3 | At least 3-5 relevant internal links |
| Anchor text quality | 3 | Descriptive, not "click here" |
| External authoritative sources | 2 | Links to trustworthy sources |
| Link relevance | 2 | Links match context and topic |

### Section 7: Image Optimization (Weight: 10%, Max: 10 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| All images have alt | 4 | No missing alt text |
| Alt is descriptive | 3 | Alt describes image content |
| Filename is descriptive | 2 | Not `img1234.jpg` but descriptive slug |
| Modern format | 1 | WebP or AVIF when possible |

### 섹션 8: 기술적 온페이지 (가중치: 10%, 최대: 10 점)

| 기준 | 점수 | 요구사항 |
|------|------|----------|
| Clean URL | 2 | 짧고, 읽기 쉽고, keyword 포함 |
| Canonical tag | 2 | 존재하고 정확함 |
| Mobile-friendly | 2 | 반응형이고 읽기 가능 |
| Schema markup | 2 | 관련 schema 존재 |
| Page speed | 2 | 3 초 이내 로딩 |

---

## 9. 점수 보고서 템플릿

```markdown
## Overall Score: [X]/100

| Section | Score | Weight | Weighted Score |
|---------|-------|--------|----------------|
| Title tag | [X]/15 | 15% | [X] |
| Meta description | [X]/5 | 5% | [X] |
| Header structure | [X]/10 | 10% | [X] |
| Content quality | [X]/25 | 25% | [X] |
| Keyword optimization | [X]/15 | 15% | [X] |
| Internal/external links | [X]/10 | 10% | [X] |
| Image optimization | [X]/10 | 10% | [X] |
| Technical on-page | [X]/10 | 10% | [X] |
| **Total** | | **100%** | **[X]/100** |

### Priority Issues

1. [Highest impact issue]
2. [Second highest]
3. [Third highest]

### Quick Wins

- [Quick win 1]
- [Quick win 2]
```

### 빠른 판단 기준

- 점수가 80 점 이상이면 강력한 온페이지 기반을 갖춘 상태다
- 60-79 점은 중간 수준, Priority Issues를 먼저 해결한다
- 60 점 미만은 Quick Wins부터 적용 후 재평가한다
- Content quality 섹션의 점수가 전체 점수의 25%를 차지한다
- Title tag과 Keyword optimization이 각각 15%로 높은 가중치를 갖는다