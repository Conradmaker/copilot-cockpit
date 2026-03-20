# Response Patterns

## 목표

조사 결과를 raw log가 아니라 decision-ready synthesis로 반환하기 위한 구조 선택 가이드다.

## 기본 패턴

### 1. 조사 보고

탐색, 계획 전 조사, 근거 확인에 가장 무난한 기본값이다.

- Outcome
- Evidence
- Implication
- Open items

### 2. 리뷰 보고

문제 발견이 우선인 리뷰 작업에 쓴다.

- Findings
- Evidence
- Risks
- Open items

### 3. 권고안 비교

여러 선택지 중 하나를 고르게 도와야 할 때 쓴다.

- Recommendation
- Alternatives considered
- Evidence
- Tradeoffs
- Open items

### 4. 구현 전 브리핑

조사 결과를 바로 구현에 넘겨야 할 때 쓴다.

- Decision
- Evidence
- Constraints
- Next step

## 선택 규칙

- 단일 질문의 답을 주는 경우는 조사 보고를 기본값으로 둔다.
- merge readiness나 regression 중심 검토는 리뷰 보고를 쓴다.
- 사용자 선택이 핵심이면 권고안 비교를 쓴다.
- 구현 handoff 직전이면 구현 전 브리핑을 쓴다.

## 작성 규칙

- 각 섹션은 짧고 직접적이어야 한다.
- Evidence에는 실제 파일, 문서, 버전, 검색 범위를 남긴다.
- Open items가 없으면 억지로 만들지 않는다.
- 사용자가 바로 다음 행동을 고를 수 있어야 한다.
