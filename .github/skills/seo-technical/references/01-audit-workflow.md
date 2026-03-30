# Technical SEO Audit Workflow

## 목표

문제가 crawl, index, render, performance, platform 중 어디에 속하는지 빠르게 좁히고, evidence-first 방식으로 감사를 진행한다.

---

## 1. 감사 시작 전에 고정할 입력

| 항목 | 확인할 내용 |
| --- | --- |
| 대상 | domain 전체인지, 특정 URL인지 |
| 상황 | launch, migration, ranking drop, page bug, AI visibility issue |
| 우선 페이지 | 매출 페이지, 제품 페이지, 핵심 문서, 허브 콘텐츠 |
| 가용 데이터 | Search Console, Bing Webmaster, crawl export, PageSpeed, browser access |
| 성공 기준 | index recovery, speed improvement, bot access recovery 등 |

### 빠른 질문 세트

1. 전체 사이트 문제인가, 특정 URL 문제인가?
2. 최근 배포, 도메인 이동, 템플릿 변경, CMS 플러그인 변경이 있었는가?
3. Search Console/Bing 데이터가 있는가?
4. 가장 중요한 URL 3개는 무엇인가?

---

## 2. 감사를 여는 우선순위

technical SEO는 아래 순서로 본다.

1. crawlability
2. indexation
3. rendering and schema validation
4. performance and mobile parity
5. platform indexing and AI bot access

이 순서를 바꾸는 경우는 거의 없다. title/meta가 아무리 좋아도 1~2단계에서 막히면 의미가 없기 때문이다.

---

## 3. 증상별 시작 지점

| 증상 | 먼저 볼 것 |
| --- | --- |
| Google에 안 뜬다 | robots, noindex, canonical, sitemap, status code |
| Bing/Copilot에 안 뜬다 | Bing indexing, Bingbot allow, sitemap, canonical |
| Claude/AI visibility가 약하다 | bot access, Brave/Bing/Google indexing readiness, factual page structure |
| schema가 없다고 보인다 | browser render, Rich Results Test, JSON-LD injection |
| 페이지가 느리다 | CWV, TTFB, image, JS, font, request count |
| migration 이후 하락 | redirect mapping, canonical, status code, internal links, sitemap |

---

## 4. severity 프레임

| 수준 | 의미 | 예시 |
| --- | --- | --- |
| P0 | 즉시 고쳐야 하는 blocking issue | robots.txt로 핵심 페이지 차단, 5xx, site-wide noindex |
| P1 | 순위와 발견 가능성에 큰 영향을 주는 문제 | redirect chain, canonical conflict, LCP 과다, Bing 미인덱싱 |
| P2 | 개선 가치가 있으나 blocking은 아닌 문제 | 누락된 structured data, image optimization, header hardening |

### 판단 기준

- 영향을 받는 URL 수가 많을수록 우선순위가 오른다
- revenue 또는 conversion page를 막는 이슈는 가중치를 높인다
- 확인 가능한 증거가 많은 문제를 먼저 다룬다

---

## 5. 권고안 작성 규칙

각 finding은 아래 5가지를 포함한다.

| 필드 | 내용 |
| --- | --- |
| Issue | 무엇이 잘못됐는가 |
| Impact | 왜 중요한가 |
| Evidence | 어떤 신호로 확인했는가 |
| Fix | 구체적으로 무엇을 바꿀 것인가 |
| Verification | 수정 후 무엇으로 확인할 것인가 |

### 좋은 finding 예시

```markdown
- Issue: `/pricing/` is blocked by robots.txt.
- Impact: A revenue page cannot be crawled or indexed.
- Evidence: `Disallow: /pricing` rule in robots.txt and URL inspection showing blocked by robots.txt.
- Fix: Remove the blocking rule or scope it to the actual private path.
- Verification: Re-test robots.txt, inspect the URL in Search Console, confirm crawl and index status after recrawl.
```

---

## 6. 최종 보고서 기본 뼈대

```markdown
# Technical SEO Audit

## Scope

- Domain / URL
- Context
- Priority pages

## Executive Summary

- Overall health
- Top blockers
- Quick wins

## Findings

| Priority | Issue | Impact | Evidence | Fix | Verification |
| --- | --- | --- | --- | --- | --- |

## Quick Wins

## Structural Fixes

## Verification Plan

## Monitoring After Changes
```