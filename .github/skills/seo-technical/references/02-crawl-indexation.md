# Crawlability and Indexation Guide

## 목표

검색 엔진이 페이지를 발견하고 인덱싱할 수 있는지 확인한다. technical SEO의 첫 번째 체크포인트다.

---

## 1. robots.txt

### 반드시 확인할 것

- 중요한 페이지나 디렉터리가 차단되지 않았는가
- sitemap이 선언되어 있는가
- CSS/JS 같은 렌더링 자산이 막히지 않았는가
- AI bot 정책이 의도와 맞는가

### 흔한 실수

| 실수 | 문제 |
| --- | --- |
| `Disallow: /` | 전체 사이트 차단 |
| 중요한 상업 페이지 경로 차단 | 인덱싱 불가 |
| CSS/JS 차단 | 렌더링 품질 저하 |
| parameter 차단 규칙이 과도함 | 유효 페이지까지 차단 |

### 기본 패턴

```text
User-agent: *
Disallow: /admin/
Disallow: /private/

Sitemap: https://example.com/sitemap.xml
```

---

## 2. XML Sitemap

### 반드시 확인할 것

- sitemap이 존재하고 200 응답을 주는가
- canonical, indexable URL만 포함하는가
- redirected, noindex, 4xx, 5xx URL이 섞이지 않았는가
- lastmod가 실제 업데이트와 대체로 맞는가

### 판단 기준

- sitemap은 "인덱싱해야 하는 URL 집합"이어야 한다
- sitemap과 실제 인덱싱 상태가 크게 다르면 coverage gap을 추적한다

---

## 3. Index blockers

### 점검 항목

- meta robots noindex
- X-Robots-Tag noindex
- robots.txt block
- canonical to another URL
- 3xx chains
- 4xx/5xx
- soft 404

### soft 404 신호

- 상태 코드는 200인데 본문은 사실상 not found
- 빈 카테고리/태그 페이지가 대량으로 생성됨
- 자동 생성 페이지가 얕은 내용만 보여줌

---

## 4. Canonicalization

### 확인 순서

1. self-referencing canonical이 있는가
2. canonical target이 200이며 indexable한가
3. HTTP/HTTPS, www/non-www, trailing slash 정책이 일관적인가
4. canonical과 redirect가 서로 충돌하지 않는가

### 흔한 실수

| 패턴 | 문제 |
| --- | --- |
| canonical 없음 | 중복 URL 확산 위험 |
| canonical이 다른 템플릿을 가리킴 | 잘못된 대표 URL 지정 |
| canonical target이 noindex | 신호 충돌 |
| canonical과 internal link target 불일치 | 혼선 증가 |

---

## 5. Redirects and Status Codes

### 우선순위

- 301: 영구 이동
- 302/307: 임시 이동. 영구 변경에 남용하지 않는다
- 404/410: 삭제된 페이지. 대체 URL이 없을 때만 허용
- 5xx: 즉시 대응 대상

### redirect chain 판단

| 상태 | 기준 |
| --- | --- |
| 양호 | 0~1 hop |
| 주의 | 2 hops |
| 문제 | 3 hops 이상 |

### 권고

- old URL에서 final destination으로 직접 보낸다
- chain과 loop는 crawl budget과 UX를 동시에 해친다

---

## 6. Crawl budget and discovery

큰 사이트에서만 중요해 보이지만, 중형 사이트도 중복 URL과 faceted navigation이 늘면 crawl budget 문제가 생긴다.

### 점검 신호

- parameter URL 대량 생성
- faceted navigation indexation
- infinite scroll without crawl path
- orphan pages
- session ID, sort/filter duplication

### quick win

- crawl 가치 없는 파라미터를 정리한다
- 내부 링크로 중요한 URL discoverability를 높인다
- sitemap을 정돈한다

---

## 7. 기본 점검 표

```markdown
| Check | Status | Notes |
| --- | --- | --- |
| robots.txt accessible | ✅/⚠️/❌ | |
| key pages blocked | ✅/⚠️/❌ | |
| sitemap exists | ✅/⚠️/❌ | |
| sitemap only indexable URLs | ✅/⚠️/❌ | |
| self-referencing canonical | ✅/⚠️/❌ | |
| canonical conflicts | ✅/⚠️/❌ | |
| redirect chains | ✅/⚠️/❌ | |
| noindex on key pages | ✅/⚠️/❌ | |
| indexed vs expected ratio | ✅/⚠️/❌ | |
```