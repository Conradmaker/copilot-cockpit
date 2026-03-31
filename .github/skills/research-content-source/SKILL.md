---
name: research-content-source
description: "Reference-first workflow for gathering sources, verifying claims, and preparing research briefs before writing audience-facing content. Use this skill when researching sources, checking statistics, verifying quotes, judging credibility, or organizing evidence for blog posts, articles, social posts, and thought-leadership drafts. Always consult this skill for pre-writing research tasks, even if the user only asks to 'find sources' or 'verify this claim'. For writing structure use writing-content. For prose clarity use writing-clearly. For technical docs use writing-document. For codebase evidence use research-foundation. Triggers on: content research, source gathering, research brief, fact check, verify claim, statistics, expert quote, credible source, claim inventory, 콘텐츠 리서치, 자료 수집, 출처 조사, 소스 수집, 리서치 브리프, 팩트 체크, 통계 찾기, 근거 모으기."
disable-model-invocation: false
user-invocable: false
---

# 콘텐츠 소스 리서치 (research-content-source)

## 목표

콘텐츠를 쓰기 전에 무엇을 확인해야 하는지 claim 단위로 고정하고, source ladder로 자료를 찾고, 신뢰도와 최신성을 판정한 뒤, writing 스킬로 넘길 수 있는 research brief로 정리한다. 이 스킬의 중심은 자료를 많이 모으는 일이 아니라, 글의 근거로 쓸 수 있는 소스를 빠르게 가려내고 구조화하는 데 있다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 리서치를 시작하기 전에는 아래 reference를 직접 읽고, 현재 요청에 맞는 템플릿과 평가 기준을 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 4대 핵심 원칙

### 1. 주제보다 claim inventory를 먼저 만든다

리서치는 넓은 주제에서 바로 시작하지 않는다. 먼저 글에서 확인해야 할 claim과 question을 3~5개로 줄여야 검색 범위와 브리프 구조가 같이 선다.

- claim 또는 question을 한 줄로 적는다
- 각 claim마다 필요한 근거 유형을 먼저 붙인다
- source priority와 현재 status를 열어 둔다

#### 빠른 판단 기준

- 무엇을 확인해야 하는지 한 줄 claim으로 못 쓰면 아직 검색할 단계가 아니다
- claim마다 evidence needed가 없으면 자료를 모아도 평가가 어렵다

→ 상세: [references/claim-inventory.md](references/claim-inventory.md)

### 2. source ladder로 가까운 근거부터 찾는다

자료 수집은 무조건 웹 검색부터 넓히지 않는다. source ladder를 기준으로 source of truth에 가까운 소스부터 보고, 낮은 단계에서 찾은 주장은 가능한 한 원출처까지 올린다.

- 내부 자료, 1차 출처, 전문가 소스, 2차 분석 순으로 우선순위를 잡는다
- 보조 자료는 단서로 쓰고 단독 근거로 끝내지 않는다
- 찾는 즉시 제목, 저자 또는 기관, 발행일, URL을 함께 남긴다
- source ladder의 상세 기준은 reference에 맡긴다

#### 빠른 판단 기준

- 2차 요약만 있고 원출처를 아직 안 봤다면 한 단계 더 올린다
- 내부나 1차 자료에 답이 있는데 외부 검색을 늘리고 있으면 방향이 어긋난다
- 제목, 저자, 날짜, URL이 남지 않으면 아직 쓸 수 있는 source가 아니다

→ 상세: [references/source-evaluation.md](references/source-evaluation.md)

### 3. 많이 모으기보다 쓸 수 있는 소스를 남긴다

수집보다 판정이 중요하다. 저자, 발행 주체, 날짜, 원출처 접근성, 교차 검증 가능성을 보고 글에 실제로 쓸 수 있는 소스만 남긴다.

- 핵심 수치와 인용은 독립된 근거로 교차 확인한다
- 최신성이 중요한 주제는 시점 기준을 더 엄격하게 본다
- confirmed, partial, open 같은 상태 구분을 유지한다

#### 빠른 판단 기준

- 저자, 날짜, 원출처가 불명확하면 근거 등급을 낮춘다
- 같은 수치가 반복되어도 원본이 하나면 독립된 여러 근거로 세지 않는다

→ 상세: [references/source-evaluation.md](references/source-evaluation.md)

### 4. research brief로 넘겨 쓰기 단계와 분리한다

리서치 결과는 링크 모음이 아니라 브리프여야 한다. writing 스킬이 바로 사용할 수 있게 핵심 포인트, 상태, 출처, 미해결 항목을 구조화해 넘긴다.

- 핵심 질문, 핵심 포인트, 데이터와 인용, 미해결 항목을 분리한다
- confirmed, inferred, unresolved를 숨기지 않는다
- 글 초안이 아니라 근거 브리프로 유지한다

#### 빠른 판단 기준

- 핵심 질문당 usable한 근거가 하나도 없으면 브리프가 아직 비어 있다
- unresolved를 지우지 말고 브리프에 남겨 표현 수위를 조절하게 한다

→ 상세: [references/research-brief.md](references/research-brief.md)

## references/ 가이드

아래 문서는 실제 리서치를 시작하기 전에 읽어야 하는 작업 가이드다. 이 본문은 방향을 잡는 용도고, 세부 템플릿과 평가 기준은 references에서 확인한다.

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/claim-inventory.md](references/claim-inventory.md) | 주제를 claim과 question으로 줄이고, evidence needed와 source priority를 먼저 고정할 때 |
| [references/source-evaluation.md](references/source-evaluation.md) | source ladder를 적용하고, 신뢰도, 최신성, 교차 검증 기준으로 소스를 판정할 때 |
| [references/research-brief.md](references/research-brief.md) | 확인된 근거를 writing 단계로 넘길 research brief와 팩트체크 메모를 정리할 때 |

### 추천 로드 순서

- 새 리서치 시작: `claim-inventory → source-evaluation → research-brief`
- 이미 자료가 있는 상태: `source-evaluation → research-brief`
- 기존 브리프 검수: `research-brief`, 필요하면 `source-evaluation`

## 응답 패턴

### 리서치 착수 요청

1. 주제와 작성 목적
2. claim inventory 초안
3. 우선 조사할 source ladder 구간
4. open 상태로 남아 있는 핵심 질문

### 소스 검증 요청

1. 검증 대상 claim
2. 소스 판정 요약
3. 상태 분류: confirmed / partial / open
4. 추가 확인이 필요한 빈칸

### 브리프 납품

[references/research-brief.md](references/research-brief.md) 템플릿에 맞춰 핵심 포인트, 데이터와 인용, 미해결 항목, 핸드오프 메모를 구조화해 전달한다.

## 범위

- 채널별 구조, 훅, 보이스, CTA, 발행용 초안 작성은 writing-content
- 문장 교정, 명료화, AI 말투 제거는 writing-clearly
- README, changelog, API reference 같은 기술 문서는 writing-document
- 코드베이스 규칙, 로컬 구현 근거, 공식 개발 문서 확인은 research-foundation
- SEO 키워드 전략이나 검색 의도 최적화는 seo 계열 스킬

이 스킬은 콘텐츠 작성을 위한 source gathering, evaluation, brief handoff에 집중한다. 글을 실제로 쓰는 일, 문장을 다듬는 일, 코드 근거를 찾는 일까지 한 스킬에 넣지 않는다.
