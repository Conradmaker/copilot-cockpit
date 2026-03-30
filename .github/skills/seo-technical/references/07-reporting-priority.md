# Reporting and Priority Guide

## 목표

technical SEO findings를 실행 가능한 우선순위와 검증 계획으로 바꾼다.

---

## 1. 우선순위 매트릭스

| Priority | 의미 | 대표 예시 |
| --- | --- | --- |
| P0 | indexing/crawling을 막는 문제 | site-wide noindex, robots block, 5xx |
| P1 | 노출과 순위에 큰 손실을 주는 문제 | redirect chain, canonical conflict, severe CWV |
| P2 | 개선 가치가 큰 최적화 | schema enhancement, image compression |

### 판단 요소

| 요소 | 질문 |
| --- | --- |
| blast radius | 몇 개 URL에 영향이 가는가 |
| business impact | 매출/리드/핵심 페이지인가 |
| verification ease | 수정 후 확인이 가능한가 |
| implementation effort | 낮은 공수로 해결 가능한가 |

---

## 2. Quick wins vs structural fixes

### Quick wins

- 잘못된 robots rule 제거
- 잘못된 canonical 수정
- sitemap 정리
- HTTP -> HTTPS redirect 추가
- missing image dimensions 추가

### Structural fixes

- faceted navigation strategy 재설계
- render architecture 수정
- CDN/cache layer 도입
- hreflang 체계 재구축

---

## 3. 최종 보고서 기본 템플릿

```markdown
# Technical SEO Audit Report

## Scope

- Domain / URL
- Context
- Pages analyzed

## Executive Summary

- Overall technical health: X/100
- Top blockers
- Recommended first 3 actions

## Findings

| Priority | Issue | Impact | Evidence | Fix | Verification |
| --- | --- | --- | --- | --- | --- |

## Quick Wins

1. ...
2. ...

## Structural Fixes

1. ...
2. ...

## Verification Plan

- Re-test robots and sitemap
- Inspect URLs in Search Console
- Re-run Rich Results validation
- Compare CWV after deployment
```

---

## 4. 문장 규칙

- generic advice를 쓰지 않는다. evidence를 함께 적는다
- 각 이슈에 affected scope를 적는다
- fix는 실행 가능한 수준으로 쓴다
- verification이 없는 권고는 제출하지 않는다