# Performance, Mobile, and Security Guide

## 목표

Core Web Vitals, mobile parity, HTTPS와 security hygiene를 한 묶음으로 보고 실제 개선 우선순위를 정한다.

---

## 1. Core Web Vitals 기준

| Metric | Good | Needs work | Poor |
| --- | --- | --- | --- |
| LCP | < 2.5s | 2.5-4.0s | > 4.0s |
| INP | < 200ms | 200-500ms | > 500ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |

### 함께 볼 보조 지표

- TTFB
- FCP
- Speed Index
- Total Blocking Time
- total page weight
- request count

---

## 2. 원인별 개선 플레이북

### LCP가 느릴 때

| 원인 | 신호 | 권고 |
| --- | --- | --- |
| 큰 hero image | hero asset이 수 MB | resize, WebP/AVIF, preload |
| 높은 TTFB | origin 응답이 느림 | caching, CDN, server tuning |
| render-blocking CSS/JS | initial render 지연 | critical CSS, defer/async, script pruning |
| font dependency | text paint 지연 | font-display, preload |

### CLS가 높을 때

| 원인 | 신호 | 권고 |
| --- | --- | --- |
| 이미지 dimension 없음 | loading 중 점프 | width/height or aspect-ratio 지정 |
| ad/embed injection | layout shift 발생 | reserve space |
| web font swap | text shift | fallback tuning |

### INP가 나쁠 때

| 원인 | 신호 | 권고 |
| --- | --- | --- |
| long JS tasks | main thread block | split work, cut JS |
| heavy event handlers | interaction lag | debounce/throttle, simplify handler |

---

## 3. Mobile parity

### 점검 항목

- 모바일과 데스크톱의 본문이 같은가
- structured data와 meta tags가 같은가
- tap target이 충분한가
- viewport 설정이 정상인가
- horizontal scroll이 없는가

### 흔한 문제

- 데스크톱 전용 탭 콘텐츠가 모바일에서 사라짐
- 모바일 템플릿이 요약본만 렌더링
- 모바일 이미지에 alt나 lazy 설정이 다르게 적용됨

---

## 4. HTTPS와 security hygiene

### 체크리스트

- HTTP -> HTTPS 301 redirect
- valid SSL certificate
- mixed content 없음
- canonical이 HTTPS를 가리킴
- HSTS 여부
- 보안 헤더(CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy)

### 우선순위

- mixed content와 HTTP direct access는 먼저 해결한다
- security headers는 ranking factor보다 hygiene 관점이지만, trust와 운영 안정성에 중요하다

---

## 5. 보고서 출력 예시

```markdown
## Performance Analysis

| Metric | Mobile | Desktop | Target | Status |
| --- | --- | --- | --- | --- |
| LCP | 4.8s | 2.1s | <2.5s | ❌ / ✅ |
| INP | 340ms | 140ms | <200ms | ❌ / ✅ |
| CLS | 0.24 | 0.08 | <0.1 | ❌ / ✅ |

### High-impact fixes

1. Convert hero image to WebP and reduce payload by ~1.8MB.
2. Add CDN or cache layer to reduce TTFB.
3. Reserve space for the promo banner to remove layout shift.
```