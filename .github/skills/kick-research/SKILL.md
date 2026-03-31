---
name: kick-research
description: "User-initiated intensive research orchestration workflow for broad, high-effort evidence gathering across codebase rules, official docs, product research, design references, content sources, and live web evidence. Invoke this skill when you want a topic investigated deeply, need multiple research lanes coordinated, or want much stronger evidence before making a decision. This skill is for explicit user-directed deep-dive research and should not be auto-invoked for ordinary evidence passes. It coordinates research-foundation, research-product, research-design, research-content-source, agent-browser, and other domain research skills as needed. Triggers on: kick-research, deep research, intensive research, broad research, investigate thoroughly, research aggressively, 심층 리서치, 정밀 조사, 깊게 조사, 빡세게 조사, 자료조사 크게."
user-invocable: true
disable-model-invocation: true
---

# Kick-Research: Intensive Research Orchestration

## 목표

유저가 직접 호출하는 kick- 스킬이다. 특정 주제에 대해 높은 강도의 자료조사를 orchestrate하고, 의사결정에 영향을 주는 근거를 최대한 넓고 깊게 확보한다.

이 스킬의 핵심은 큰 보고서를 만드는 일이 아니라, 에이전트 실행 중 자료조사 workflow를 강화하고 evidence quality를 끌어올리는 데 있다.

---

## 워크플로우

### 1. Research brief를 먼저 고정한다

조사부터 넓게 시작하지 않는다. 먼저 무엇을 결정하려는지, 무엇을 증명하거나 반박하려는지 고정한다.

- 핵심 질문과 의사결정 포인트를 적는다
- 포함 범위와 제외 범위를 적는다
- 어떤 수준의 근거가 있어야 충분한지 proof bar를 적는다
- 이미 알고 있는 사실과 아직 모르는 사실을 분리한다

#### 빠른 판단 기준

- 무엇을 알고 싶은가만 있고 무슨 결정을 바꾸려는가가 없으면 brief가 약하다
- 범위와 제외 범위가 없으면 탐색이 끝없이 퍼진다
- proof bar가 없으면 검색은 늘어나고 결론은 약해진다

### 2. 조사 lane을 먼저 나눈다

모든 자료조사를 하나의 검색 흐름으로 합치지 않는다. 조사 질문을 lane으로 나눈 뒤, 독립적인 lane만 병렬화한다.

| Lane | 언제 여는가 | 기본 owner |
| --- | --- | --- |
| Foundation evidence | 로컬 규칙, 기존 구현, 공식 문서, upstream source가 중요할 때 | research-foundation |
| Product and market | 시장, 경쟁, 포지셔닝, JTBD, 기회 평가가 중요할 때 | research-product |
| Design reference | 실서비스 화면, 플로우, 패턴 비교가 필요할 때 | research-design |
| Content and sources | 통계, 인용, 주장 검증, source quality 평가가 중요할 때 | research-content-source |
| Live web evidence | 특정 사이트 상태 확인, 브라우저 검증, 실시간 캡처가 필요할 때 | agent-browser |

#### 빠른 판단 기준

- lane 기준 없이 검색부터 시작하지 않는다
- 같은 질문을 서로 다른 lane에서 중복 검색하지 않는다
- lane이 다르더라도 하나의 의사결정에 연결되지 않으면 확장하지 않는다

### 3. 기본 모드는 intensive지만 bounded여야 한다

이 스킬의 기본 모드는 강한 조사다. 다만 많이 찾는 것보다 결론을 바꿀 수 있는 근거를 찾는 것이 중요하다.

- broad -> narrow -> confirm 순으로 탐색한다
- 독립적인 lane만 병렬화한다
- source type이 한쪽으로 치우치면 다른 출처 계층을 보강한다
- 같은 claim은 가능한 한 서로 독립적인 근거로 교차 확인한다
- 추가 검색이 결론을 거의 바꾸지 못하면 멈춘다

#### 빠른 판단 기준

- 결과 수가 많아도 source tier가 약하면 아직 충분하지 않다
- 같은 기사나 요약문을 여러 번 찾은 것은 증거가 늘어난 것이 아니다
- 다음 wave가 decision quality를 올리지 못하면 stop rule을 적용한다

### 4. wave마다 checkpoint를 둔다

강한 조사일수록 중간 checkpoint가 없으면 중복 탐색과 runaway searching이 생긴다. 각 wave 뒤에 현재 상태를 정리하고 다음 wave 필요성을 판정한다.

- 지금까지 confirmed / inferred / unresolved를 정리한다
- 충돌하는 근거가 있으면 그대로 남긴다
- 다음 wave가 필요한 이유를 한 줄로 적는다
- 더 깊게 들어갈 lane과 닫을 lane을 분리한다

#### 빠른 판단 기준

- unresolved가 남아도 추가 wave가 결론을 안 바꾸면 닫는다
- conflict를 지우고 평균내지 않는다
- checkpoint 없이 자동 최대 탐색만 계속하지 않는다

### 5. synthesis는 handoff 가능해야 한다

조사 결과는 링크 모음이나 메모 덤프가 아니라, 다음 owner가 바로 이어받을 수 있는 handoff 형태여야 한다.

- 핵심 결론과 근거를 연결한다
- lane별 findings를 남긴다
- unresolved gaps와 추가 조사 필요 여부를 적는다
- 다음에 읽을 domain skill이나 owner를 추천한다

#### 빠른 판단 기준

- 결론에 근거가 붙지 않으면 synthesis가 약하다
- 조사 결과를 봐도 다음 액션이 안 보이면 handoff가 실패한 것이다

---

## 기본 출력

이 스킬을 사용할 때는 기본적으로 아래 구조를 만든다.

1. Research brief
2. Lane plan
3. Wave summary
4. Key findings with evidence
5. Conflicts and unresolved gaps
6. Recommended handoff or next research step

## 범위

- 이 스킬은 유저가 직접 호출하는 intensive research orchestrator다.
- ordinary evidence pass, 로컬 규칙 확인, 공식 문서 우선 검증은 research-foundation이 owner다.
- 제품 조사, 디자인 레퍼런스 조사, 콘텐츠 source 검증의 실제 deep dive는 각 research-* 스킬이 owner다.
- 구현, 설계, 문장 작성, 시각 디자인의 최종 owner decision은 domain skill이 담당한다.