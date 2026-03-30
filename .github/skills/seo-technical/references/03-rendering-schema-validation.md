# Rendering and Schema Validation Guide

## 목표

정적 HTML만으로 보이지 않는 렌더링 문제와 structured data validation 문제를 오진 없이 다룬다.

---

## 1. 먼저 기억할 제약

`web_fetch`, markdown 변환, 단순 curl은 JSON-LD나 client-side injected DOM을 놓칠 수 있다.

### 왜 문제가 되나

- CMS plugins가 `<script type="application/ld+json">`를 클라이언트에서 삽입한다
- 일부 페이지는 hydration 이후에만 핵심 FAQ, product data, content blocks가 나타난다
- 정적 fetch 결과만 보고 "schema 없음" 또는 "본문 없음"이라고 결론 내리면 false negative가 난다

### 우선 사용 도구

1. browser rendering
2. Google Rich Results Test
3. Schema Validator
4. Search Console enhancements

---

## 2. Render parity 점검

### 확인할 것

- 사용자에게 보이는 핵심 본문이 초기 HTML에도 있는가
- lazy content나 tabs 안의 핵심 정보가 렌더링 후에도 노출되는가
- mobile과 desktop의 structured data, meta, visible copy가 크게 다르지 않은가

### 위험 신호

- 핵심 콘텐츠가 JS 실행 후에만 나타남
- placeholder만 있고 실제 텍스트가 늦게 채워짐
- hydration error로 일부 콘텐츠가 사라짐

---

## 3. Structured data validation flow

### 1단계: 존재 확인

- FAQ, Article, Product, Organization, Breadcrumb, WebPage 등 어떤 schema가 있는지 확인한다

### 2단계: 페이지 목적 적합성 확인

- blog/article 페이지: Article
- FAQ 섹션이 보이는 페이지: FAQPage
- e-commerce product page: Product
- site hierarchy pages: BreadcrumbList
- homepage/about: Organization/WebSite

### 3단계: 유효성 확인

- required property 누락 여부
- datePublished/dateModified 정확성
- author/publisher/logo 등의 field 일관성
- schema content와 visible content 일치 여부

### 4단계: enhancement 기회 확인

- FAQ visible content가 있는데 schema 없음
- article pages에 author/timestamp/schema 누락
- breadcrumb가 UI에 있는데 structured data 없음

---

## 4. 최소 JSON-LD starter snippets

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is technical SEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Technical SEO improves how search engines crawl, render, index, and validate a site."
      }
    }
  ]
}
```

### Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Example article",
  "datePublished": "2026-03-28",
  "dateModified": "2026-03-28",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  }
}
```

### Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Inc.",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png"
}
```

---

## 5. 보고서 작성 규칙

- 정적 HTML만으로 검증한 한계를 반드시 밝힌다
- "schema 없음" 대신 "정적 응답에서는 확인되지 않았고, browser/Rich Results validation이 추가로 필요함"처럼 쓴다
- schema는 존재 여부, validity, page-fit, content-match 네 축으로 평가한다