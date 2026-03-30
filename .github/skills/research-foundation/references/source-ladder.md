# Source Ladder

## 목표

같은 품질의 결론을 더 짧은 조사 비용으로 얻기 위한 우선순위 규칙이다.

## 기본 순서

### 1. Repository truth

먼저 현재 저장소 안의 규칙과 사실을 확인한다.

- AGENTS.md
- 관련 instructions
- 관련 SKILL.md
- README, docs, examples
- 실제 구현 파일과 테스트
- 현재 에러와 변경 surface

이 단계에서 이미 답이 충분하면 외부 웹 검색을 늘리지 않는다.

### 2. Local precedent

같은 코드베이스 안에 유사한 구현이나 naming, folder placement, contract pattern이 있는지 확인한다.

이 단계의 목표는 새로운 정답을 발명하는 것이 아니라, 현재 코드베이스의 기대치를 맞추는 것이다.

### 3. Official external evidence

외부 계약이나 버전 민감 동작이 걸리면 공식 자료를 확인한다.

- 공식 문서
- 공식 예제
- upstream source
- 공식 release notes

가능하면 문서 버전이나 날짜를 함께 남긴다.

디자인과 제품 작업에서는 이 단계를 아래처럼 해석한다.

- 공식 design system 문서
- 실제 서비스의 현재 화면과 flow
- 최신 shipped example 또는 release surface

이 경우에도 오래된 레퍼런스보다 현재 서비스 상태에 가까운 자료를 우선한다.

### 4. Secondary evidence

공식 자료만으로 빈칸이 남을 때만 보조 자료를 사용한다.

- maintainer issue comment
- reputable blog post
- discussion thread with concrete evidence
- 최근 비교 분석 글이나 사례 정리

이 자료는 보강용이다. 공식 근거를 대체한다고 가정하지 않는다.

## 최신성 규칙

- 최신성이 결론에 영향을 주는 작업이면 자료의 시점이나 버전을 함께 남긴다.
- 라이브러리, API, 디자인 트렌드, 제품 UI처럼 변화가 빠른 주제는 오래된 예시를 현재 truth로 취급하지 않는다.
- 최신 근거를 찾기 어렵다면 그 한계를 open item으로 남긴다.

### 5. User alignment

남은 불확실성이 기술 사실이 아니라 선택의 문제라면 사용자에게 묻는다.

예:

- 속도와 정확도 중 어느 쪽을 더 우선하는가
- 로컬 관례를 따를지, 외부 모범 사례로 바꿀지
- 간단한 답과 깊은 조사 중 어느 정도 깊이를 원하는가

## 병렬화 규칙

- 로컬 패턴 탐색과 공식 문서 확인처럼 독립적인 lane만 병렬화한다.
- 같은 질문을 local search와 web search로 무의미하게 중복하지 않는다.
- parallel 결과는 마지막에 하나의 synthesis로 합친다.

## 중단 조건

아래 중 하나에 해당하면 조사를 멈추고 합성 단계로 넘어간다.

- 다음 소스가 결론을 바꿀 가능성이 낮다.
- 이미 충분한 근거로 구현 또는 판단이 가능하다.
- 남은 공백이 사실 문제가 아니라 사용자 선택 문제다.
- 추가 검색이 같은 정보의 반복만 늘린다.

## 충돌 처리

근거가 충돌하면 다수결로 덮지 않는다.

1. 어떤 소스끼리 충돌하는지 적는다.
2. source of truth에 더 가까운 자료를 우선한다.
3. 그래도 결정이 안 나면 open item으로 남기고 사용자 정렬을 요청한다.

## 메모 규칙

조사 결과를 남길 때는 아래 네 가지를 최소 단위로 적는다.

- conclusion: 지금 채택할 판단
- evidence: 그 판단을 지지한 파일, 문서, 버전
- implication: 구현이나 리뷰에 주는 영향
- open items: 아직 비어 있는 부분
