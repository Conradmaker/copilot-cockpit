---
name: evidence-first-research
description: Reference-led research workflow for tasks where the user explicitly wants stronger research or where the quality of the answer depends on current local rules, official docs, or real product references. Use this skill when the user asks to research first, bring stronger references, verify assumptions, confirm against docs, or ground plans, specs, reviews, customizations, and design decisions in evidence. Also use it when recent shipped examples or latest references matter across development, product, and design work. Do not trigger for trivial wording or tiny edits that will not materially change with more evidence. For domain-specific implementation details, combine this skill with the relevant domain skill after the evidence pass. Triggers on: research first, stronger references, latest references, current examples, official docs, verify assumptions, product references, design references, 자료조사, 레퍼런스, 근거, 최신 레퍼런스, 공식 문서, 조사 먼저, 추측하지 말고 확인.
---

# Evidence-First Research

## 목표

정확도가 중요한 작업에서 답을 먼저 만들지 말고, 근거를 먼저 만든다.

이 문서는 빠른 판단용 요약 가이드다. 작업을 시작하기 전에 현재 저장소의 규칙 문서, 관련 구현 파일, 필요한 외부 공식 문서를 먼저 읽고 판단한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 단계

### 1. 먼저 무엇이 불확실한지 쪼갠다

질문이 큰 상태로 조사하지 않는다. 아래처럼 증거 질문으로 분해한다.

- 이 저장소에 이미 정해진 규칙이 있는가
- 로컬에 재사용 가능한 패턴이 있는가
- 외부 API나 라이브러리 동작이 버전 민감한가
- 사용자의 선호가 기술 결정보다 더 중요한가

#### 빠른 판단 기준

- 답이 구현, 설계, 리뷰 결론을 바꿀 수 있으면 조사부터 한다.
- 단순 문장 다듬기나 사소한 포맷 정리는 과한 조사보다 바로 처리하는 편이 낫다.

실제 source 선택은 [source ladder 가이드](references/source-ladder.md)를 먼저 읽고 정한다.

### 2. 근거는 가까운 곳에서 먼 곳 순으로 찾는다

무조건 웹부터 찾지 않는다. 현재 작업의 source of truth에 더 가까운 자료를 먼저 읽는다.

1. 워크스페이스 규칙과 로컬 문서
2. 관련 구현 파일과 기존 패턴
3. 공식 문서, 공식 예제, upstream source
4. 평판 있는 보조 자료
5. 여전히 남는 선택지는 사용자에게 확인

디자인이나 제품 판단이라면 공식 문서만 보지 않는다. 최신 실서비스 화면, design system, 실제 shipped flow 같은 현재성 있는 reference를 함께 찾는다.

#### 빠른 판단 기준

- 로컬 규칙이 있으면 외부 자료보다 우선한다.
- 공식 문서가 필요한데 없으면 추측으로 메우지 않는다.
- 보조 자료는 공식 근거를 대체하지 않고 보완만 한다.

세부 우선순위와 중단 조건은 [source ladder 가이드](references/source-ladder.md)를 따른다.

### 3. 독립적인 조사 lane만 병렬화한다

같은 질문을 다른 표현으로 여러 번 찾지 않는다. 로컬 패턴 탐색과 외부 계약 확인처럼 서로 독립적인 lane일 때만 병렬화한다.

#### 빠른 판단 기준

- 같은 파일과 같은 질문을 중복 탐색하지 않는다.
- 다음 소스가 결론을 거의 바꾸지 못하면 멈춘다.
- 충돌하는 근거가 나오면 숨기지 말고 충돌 자체를 결과에 남긴다.

### 4. 근거를 결정과 직접 연결한다

자료를 많이 모으는 것보다, 어떤 근거가 어떤 결정을 지지하는지 연결하는 편이 중요하다.

- 추천안마다 해당 근거를 붙인다.
- confirmed, inferred, unresolved를 구분한다.
- 버전, 경로, 문서 이름, 검색 범위를 가능한 한 구체적으로 남긴다.

#### 빠른 판단 기준

- 구체적 파일이나 문서 없이 나온 결론은 약한 결론일 가능성이 높다.
- 증거가 약하면 단정 대신 조건부 표현과 open item을 남긴다.

응답 구조는 [response pattern 가이드](references/response-patterns.md)를 기준으로 고른다.

### 5. 덤프하지 말고 합성한다

search log나 링크 모음을 그대로 내놓지 않는다. 지금 결정을 위해 필요한 최소 근거만 정리한다.

#### 빠른 판단 기준

- 결과는 결론, 근거, 영향, 남은 공백 순으로 정리한다.
- 사용자가 바로 다음 결정을 내릴 수 있어야 한다.

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/source-ladder.md](references/source-ladder.md) | 어떤 소스를 어떤 순서로 읽을지, 어디서 멈출지 정할 때 |
| [references/response-patterns.md](references/response-patterns.md) | 조사 결과를 어떤 구조로 반환할지 고를 때 |

## 범위

- 이 스킬은 조사와 근거 정리에 집중한다. 실제 구현 규칙은 해당 도메인 스킬을 이어서 읽는다.
- UI 화면이나 플로우 레퍼런스 연구가 핵심이면 research-design이 더 적합하다.
- agent, instruction, skill, workflow customization을 편집할 때는 이 스킬로 근거를 모은 뒤 관련 customization 규칙을 적용한다.
