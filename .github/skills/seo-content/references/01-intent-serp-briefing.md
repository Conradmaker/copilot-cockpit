# Intent and SERP Briefing Guide

## 목표

콘텐츠를 쓰기 전에 쿼리 의도, 페이지 유형, 경쟁 결과 구조, query coverage를 먼저 정리한다.

---

## 1. intent 분류

| Intent | 독자가 원하는 것 | 잘 맞는 페이지 |
| --- | --- | --- |
| Informational | 정의, 설명, how-to, 원인 | guide, glossary, tutorial, FAQ |
| Commercial | 비교, 추천, 리뷰, 평가 | comparison, roundup, review |
| Transactional | 구매, 가입, 문의 | landing, product, pricing, service |
| Local | 지역 기반 서비스/방문 | local service page, location page |
| Navigational | 특정 브랜드/페이지 찾기 | homepage, brand page, docs entry |

### 빠른 판단 기준

- "what is", "how to", "why"는 대체로 informational
- "best", "vs", "review", "alternatives"는 commercial
- "pricing", "buy", "demo", "sign up"은 transactional

---

## 2. page type 선택

| Page type | 언제 선택하나 |
| --- | --- |
| Blog guide | 개념 설명과 교육이 중심일 때 |
| Comparison page | 둘 이상 비교가 핵심일 때 |
| Listicle / roundup | 선택지 큐레이션이 핵심일 때 |
| Landing / service page | 전환과 제안이 핵심일 때 |
| FAQ page | 질문 기반 검색 수요가 많을 때 |
| Product page | 특정 제품 정보를 찾는 경우 |

---

## 3. SERP 브리핑 템플릿

```markdown
## SERP Brief

- Primary keyword:
- Search intent:
- Page type recommendation:
- Top ranking formats:
- Repeating sections in top results:
- PAA questions:
- Snippet opportunities:
- Thin spots or angle gaps:
- Internal cannibalization risk:
```

---

## 4. keyword map

| Bucket | 내용 |
| --- | --- |
| Primary | 핵심 키워드. title, H1, intro, conclusion에 반영 |
| Secondary | 섹션 확장용. H2/H3, body에 자연스럽게 배치 |
| Related terms | LSI와 entity. 본문 semantic coverage용 |
| Questions | FAQ, H2, snippet block 후보 |

### query coverage 기준

- primary keyword 하나만 반복하지 않는다
- top SERP가 함께 다루는 하위 질문을 3개 이상 커버한다
- 기존 사이트 내 유사 페이지와 역할이 겹치지 않게 한다

---

## 5. content angle 잡는 법

- 더 깊게: 더 많은 근거, 예시, 실험, 데이터
- 더 빠르게: 더 짧은 direct answer, checklist, decision guide
- 더 명확하게: jargon을 풀고 structure를 정리
- 더 특화되게: 특정 audience, use case, region, stack에 맞춤

### angle 질문

1. 상위 결과가 공통으로 놓치는 질문은 무엇인가?
2. 우리에게만 있는 사례, 데이터, product angle이 있는가?
3. 독자가 이 페이지를 저장하거나 공유할 이유는 무엇인가?

---

## 6. cannibalization quick check

- 같은 사이트에 유사 keyword와 intent를 가진 페이지가 이미 있는가
- 두 페이지가 다른 user task를 해결하는가
- title/H1이 지나치게 비슷한가

### 신호

| 신호 | 해석 |
| --- | --- |
| 같은 keyword, 같은 intent, 같은 page type | 병합 또는 재포지셔닝 후보 |
| 같은 keyword, 다른 intent | 공존 가능. intent를 분리해서 설명 필요 |

---

## 7. CORE-EEAT 사전 작성 체크리스트

콘텐츠를 쓰기 전에 품질 기준을 먼저 고정한다. 아래 16 개 항목은 모든 콘텐츠 타입에 공통으로 적용된다.

| ID | 기준 | 적용 방법 |
|----|------|-----------|
| C01 | Intent Alignment | 타이틀 약속이 콘텐츠 전달 내용과 일치한다 |
| C02 | Direct Answer | 핵심 답변을 첫 150 단어 내에 제공한다 |
| C06 | Audience Targeting | "이 글은...를 위한 글입니다" 명시한다 |
| C10 | Semantic Closure | 결론이 도입 질문에 답하고 다음 단계를 제시한다 |
| O01 | Heading Hierarchy | H1→H2→H3, 단계 건너뛰기 없이 |
| O02 | Summary Box | TL;DR 또는 Key Takeaways 포함한다 |
| O06 | Section Chunking | 섹션당 하나의 주제; 문단은 3–5 문장 |
| O09 | Information Density | filler 없이; 용어 일관성 유지한다 |
| R01 | Data Precision | ≥5 개의 정밀한 숫자와 단위 포함한다 |
| R02 | Citation Density | 500 단어당 ≥1 개의 외부 인용 포함한다 |
| R04 | Evidence-Claim Mapping | 모든 주장은 근거로 뒷받침한다 |
| R07 | Entity Precision | 사람/조직/제품의 전체 이름 사용한다 |
| C03 | Query Coverage | ≥3 개의 쿼리 변형(동의어, long-tail) 커버한다 |
| O08 | Anchor Navigation | 점프 링크가 있는 목차 포함한다 |
| O10 | Multimedia Structure | 이미지/비디오에 캡션과 정보성 내용 포함한다 |
| E07 | Practical Tools | 다운로드 가능한 템플릿, 체크리스트, 계산기 포함한다 |

### 콘텐츠 타입별 가중치

- **Blog guide**: C01, C02, O01, O02, R02, C03
- **Comparison**: R01, R04, R07, O06, O09
- **Landing page**: C01, C06, C10, O02, E07
- **FAQ page**: C02, C03, O06, R07

콘텐츠 타입별 차원 가중치는 CORE-EEAT Benchmark 의 Content-Type Weight Table 을 참조한다.

### 빠른 판단 기준

- 작성 시작 전 이 체크리스트를 먼저 읽는다
- 16 개 항목 중 현재 콘텐츠 타입에 높은 가중치를 가진 항목을 우선 적용한다
- 근거가 부족한 주장은 쓰지 않거나 조사 후 추가한다
- 타이틀과 콘텐츠 불일치는 intent mismatch 의 주요 원인이다
- 첫 150 단어에 답이 없으면 독자가 스크롤하지 않을 수 있다
