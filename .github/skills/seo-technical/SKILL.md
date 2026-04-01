---
name: seo-technical
description: "Technical SEO audit and remediation for crawlability, indexation, rendering, schema validation, redirects, Core Web Vitals, mobile parity, HTTPS, hreflang, and search/AI bot access. Use when diagnosing robots.txt, sitemap.xml, canonicals, redirect chains, crawl budget, JavaScript rendering, structured data, page speed, 5xx errors, mixed content, or why pages are not indexed by Google, Bing, Copilot, Claude, or Perplexity. Always consult this skill for site mechanics that affect discovery, crawlability, indexability, and trust by search and AI engines, even if the request only mentions page speed, schema, or bot access. For title/meta copy, search intent, on-page scoring, and GEO writing use seo-content. Triggers on: technical SEO, indexing, crawlability, robots.txt, sitemap, canonical, redirect, structured data, Core Web Vitals, page speed, AI bot access, SEO audit, why not indexed, 테크니컬 SEO, 인덱싱, 크롤링, SEO 진단, 인덱싱 안 됨."
disable-model-invocation: false
user-invocable: false
---

# 테크니컬 SEO 구현·검증 가이드 (seo-technical)

## 목표

검색 엔진과 AI 엔진이 페이지를 제대로 발견하고, 크롤링하고, 렌더링하고, 인덱싱하고, 검증하도록 만든다. 이 스킬의 중심은 "SEO 전반"이 아니라 robots.txt, sitemap, canonical, redirect, render parity, schema validation, Core Web Vitals, mobile, HTTPS, hreflang, bot access 같은 **사이트 메커니즘**을 점검하고 수정 우선순위를 정하는 데 있다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 진단하거나 수정 방안을 작성하기 전에는 아래 reference 문서를 직접 읽고, 현재 문제가 crawl, index, render, validate, performance, platform 중 어디에 속하는지 먼저 좁힌 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 6대 핵심 단계

### 1. 문제를 기술 신호로 먼저 분류한다

기술 SEO 문제는 한 덩어리가 아니다. 같은 "노출이 안 된다"라도 크롤링 차단인지, 인덱싱 누락인지, 렌더링 실패인지, 성능 저하인지, 플랫폼별 bot access 문제인지가 완전히 다르다.

- site-wide 문제인지, 특정 URL 문제인지 먼저 나눈다
- launch, migration, ranking drop, page-specific bug 중 어떤 상황인지 밝힌다
- scope가 흐리면 broad SEO 진단보다 기술 신호 수집부터 한다

#### 빠른 판단 기준

- robots.txt, sitemap, canonical, redirect, noindex, hreflang, schema, CWV, HTTPS가 나오면 이 스킬 범위다
- title tag, meta description, keyword, H1-H3, FAQ copy가 중심이면 seo-content 범위다
- "왜 안 뜨지" 수준의 막연한 요청이면 먼저 [references/01-audit-workflow.md](references/01-audit-workflow.md)로 스코프를 고정한다

→ 상세: [references/01-audit-workflow.md](references/01-audit-workflow.md)

### 2. Crawlability와 indexation을 가장 먼저 본다

콘텐츠가 좋아도 검색 엔진이 못 찾거나 못 인덱싱하면 의미가 없다. 기술 SEO는 항상 crawlability와 indexation부터 확인한다.

- robots.txt, XML sitemap, noindex, canonical, redirect chain, status code를 먼저 확인한다
- sitemap의 URL 집합과 실제 인덱싱된 URL 집합이 얼마나 다른지 비교한다
- 중요한 상업 페이지가 차단됐는지, 중복 URL이 확산되는지 확인한다
- crawl depth, orphan page, faceted navigation, parameter URL 확산까지 함께 본다

#### 빠른 판단 기준

- 200이 아닌 상태 코드가 중요한 페이지에 있으면 P0 또는 P1 후보다
- sitemap에 noindex, redirected, canonicalized URL이 섞여 있으면 정리 대상이다
- site: 검색, Search Console coverage, Bing indexing 간 괴리가 크면 indexation 문제를 의심한다

→ 상세: [references/02-crawl-indexation.md](references/02-crawl-indexation.md)

### 3. 렌더링과 schema 검증은 static fetch만 믿지 않는다

JavaScript 렌더링과 JSON-LD schema는 정적 HTML만 보고 판단하면 오진이 많다. 특히 CMS 플러그인이나 클라이언트 주입 스크립트는 curl이나 markdown 변환에서 사라질 수 있다.

- schema를 볼 때는 browser rendering, Rich Results Test, Schema Validator를 우선한다
- render parity를 확인해 검색 엔진이 실제로 보는 DOM과 사용자가 보는 DOM이 같은지 본다
- FAQ, Article, Product, Breadcrumb, Organization 등 schema type을 페이지 목적과 맞춘다

#### 빠른 판단 기준

- 정적 HTML에 schema가 안 보인다는 이유만으로 "schema 없음" 결론을 내리지 않는다
- client-side injected content가 핵심 본문을 차지하면 render issue 가능성을 먼저 본다
- schema는 존재 여부보다 유효성, 페이지 목적 적합성, 필수 필드 충족 여부가 중요하다

→ 상세: [references/03-rendering-schema-validation.md](references/03-rendering-schema-validation.md)

### 4. Performance, mobile, security는 한 묶음으로 본다

Core Web Vitals만 따로 떼어보면 원인 추적이 약해진다. LCP, INP, CLS 문제는 종종 TTFB, 이미지, JS, font, layout shift, HTTPS, mixed content와 같이 움직인다.

- CWV는 metric 자체보다 원인과 개선 우선순위를 함께 본다
- mobile-first indexing을 전제로 모바일 콘텐츠 parity를 확인한다
- HTTPS 강제, mixed content, security headers를 함께 점검한다

#### 빠른 판단 기준

- LCP > 2.5s, INP > 200ms, CLS > 0.1이면 개선 계획이 필요하다
- 모바일과 데스크톱의 콘텐츠나 structured data가 다르면 mobile parity 이슈다
- HTTP가 301 없이 열리거나 mixed content가 있으면 security와 canonicalization을 함께 본다

→ 상세: [references/04-performance-mobile-security.md](references/04-performance-mobile-security.md)

### 5. 검색 엔진과 AI 엔진별 접근 요구를 따로 본다

Google, Bing/Copilot, Perplexity, Claude/Brave는 인덱스와 retrieval 경로가 다르다. technical SEO는 전통 검색과 AI 검색의 공통분모와 차이를 둘 다 다뤄야 한다.

- Googlebot, Bingbot, GPTBot, PerplexityBot, ClaudeBot, anthropic-ai 접근 정책을 확인한다
- Bing index, Brave index, Google index의 차이를 감안해 platform-specific visibility blockers를 본다
- FAQ schema, Article schema, timestamp, clean sitemap, bot allow rules 같은 요구를 엔진별로 구분한다
- 다국어 사이트라면 hreflang, x-default, locale별 인덱싱 편차를 엔진별로 함께 본다

#### 빠른 판단 기준

- Bing에 안 잡히면 Copilot 계열 인용 가능성이 크게 떨어진다
- Claude visibility를 묻는데 Google만 보고 끝내면 불완전하다
- AI visibility 문제라도 bot access와 index readiness는 이 스킬 범위다

→ 상세: [references/05-platform-indexing-ai-bots.md](references/05-platform-indexing-ai-bots.md), [references/06-international-platform-indexing.md](references/06-international-platform-indexing.md)

### 6. 수정은 blast radius와 검증 가능성 기준으로 우선순위를 잡는다

기술 SEO는 발견보다 우선순위가 더 중요하다. 모든 이슈를 같은 무게로 다루면 실행력이 떨어진다.

- index-blocking, revenue-page blocking, site-wide duplication은 P0/P1로 올린다
- quick win과 structural fix를 구분한다
- 각 권고안은 evidence, affected scope, verification method까지 함께 적는다

#### 빠른 판단 기준

- site-wide robots/canonical/redirect 문제는 page-level alt text보다 우선이다
- verification path가 없는 권고는 약한 권고다
- 실행 후 무엇을 다시 측정할지 없으면 보고서가 아니라 의견에 가깝다

→ 상세: [references/07-reporting-priority.md](references/07-reporting-priority.md)

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/01-audit-workflow.md](references/01-audit-workflow.md) | scope를 정하고 technical audit 흐름과 severity를 고정할 때 |
| [references/02-crawl-indexation.md](references/02-crawl-indexation.md) | robots, sitemap, canonical, redirect, noindex, index coverage를 볼 때 |
| [references/03-rendering-schema-validation.md](references/03-rendering-schema-validation.md) | JS rendering, schema detection limitation, validation 절차를 다룰 때 |
| [references/04-performance-mobile-security.md](references/04-performance-mobile-security.md) | CWV, TTFB, mobile parity, HTTPS, mixed content, security headers를 다룰 때 |
| [references/05-platform-indexing-ai-bots.md](references/05-platform-indexing-ai-bots.md) | Google/Bing/Perplexity/Claude 계열 bot access와 platform indexing을 볼 때 |
| [references/06-international-platform-indexing.md](references/06-international-platform-indexing.md) | hreflang, locale targeting, cross-engine indexing 차이를 함께 볼 때 |
| [references/07-reporting-priority.md](references/07-reporting-priority.md) | 최종 우선순위 표, remediation roadmap, verification plan을 만들 때 |

### 추천 로드 순서

- broad technical audit: `01 -> 02 -> 03 -> 04 -> 05 -> 07`
- indexing issue: `01 -> 02 -> 05 -> 07`
- schema/render issue: `01 -> 03 -> 05 -> 07`
- Core Web Vitals issue: `01 -> 04 -> 07`
- multi-region site: `01 -> 02 -> 06 -> 07`

---

## 범위

- title tags, meta descriptions, Open Graph, Twitter cards, keyword mapping, search intent, on-page scoring, featured snippets, FAQ copy, GEO writing → seo-content
- generic content structure and blog/article writing → writing-content
- source gathering, stats, expert quotes, claim validation → research-content-source

이 스킬은 사이트 메커니즘과 technical verification을 담당한다. title/meta copy, keyword strategy, on-page content optimization, generic writing까지 한 스킬에 넣지 않는다.

Scope가 불명확한 요청("SEO가 안 좋아", "SEO 도와줘")은 이 스킬의 audit workflow로 진입해 문제를 분류한 후, 필요시 seo-content로 handoff한다.