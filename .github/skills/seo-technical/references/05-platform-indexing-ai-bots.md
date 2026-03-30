# Platform Indexing and AI Bot Access

## 목표

Google, Bing/Copilot, Perplexity, Claude/Brave 계열 visibility를 위해 필요한 crawler access와 indexing readiness를 구분한다.

---

## 1. 기본 원칙

- AI visibility 문제도 먼저 indexing readiness를 본다
- 각 엔진은 서로 다른 index와 retrieval 경로를 가진다
- bot allow가 되어 있어도 content structure와 freshness가 받쳐주지 않으면 citation likelihood는 낮다

---

## 2. 엔진별 technical checkpoints

| Engine | 핵심 인덱스/경로 | 먼저 볼 technical signal |
| --- | --- | --- |
| Google Search / AI Overview | Google index | crawl/index health, CWV, structured data |
| Bing / Copilot | Bing index | Bingbot allow, Bing indexing, fast pages |
| Perplexity | 자체 retrieval + web | PerplexityBot allow, FAQ/schema, clean sitemap |
| Claude | Brave search + web retrieval | ClaudeBot/anthropic-ai allow, clear factual pages |
| ChatGPT browse | web retrieval | strong domain trust, factual structure, freshness |

---

## 3. AI bot allow table

| Bot | typical use |
| --- | --- |
| Googlebot | Google crawling |
| Bingbot | Bing and Copilot crawling |
| GPTBot / ChatGPT-User | OpenAI ecosystem |
| PerplexityBot | Perplexity crawling |
| ClaudeBot / anthropic-ai | Anthropic crawling |

### 기본 robots 예시

```text
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

Sitemap: https://example.com/sitemap.xml
```

---

## 4. 엔진별 빠른 해석

### Google / AI Overview

- traditional SEO health가 기본이다
- structured data, E-E-A-T, content usefulness가 중요하다

### Bing / Copilot

- Bing에 안 잡히면 Copilot visibility도 약해진다
- IndexNow, Bing Webmaster, Bingbot allow 여부를 같이 본다

### Perplexity

- FAQ schema, atomic paragraphs, freshness, PDF/public resources가 강하게 작동할 수 있다

### Claude

- Brave indexing 여부를 간접적으로 추정해야 한다
- factual density와 structural clarity가 중요하다

---

## 5. 보고서에 넣을 문장 패턴

- "Bingbot is allowed, but the key commercial page is not indexed in Bing yet. Copilot visibility is therefore likely constrained by Bing index coverage, not just content quality."
- "Static fetch did not confirm JSON-LD, so AI visibility recommendations should wait for rendered validation."