---
name: ds-product-ux
description: "Product UX principles for UX writing, CTA labels, loading, feedback, confirmation, destructive actions, share and selection flows, navigation, motion, inclusive design, and dark pattern prevention. Use this skill when designing or reviewing product-level user flows, button labels, error messages, empty states, onboarding prompts, loading states, confirmation dialogs, delete flows, share flows, selection flows, navigation behavior, or motion guidelines. Always consult this skill for UX decisions that affect what users read, expect, choose, recover from, or trust, even if the user only asked for copy polish or screen-level UX feedback. For implementation-level accessibility use fe-a11y. For React architecture use fe-react-patterns. Triggers on: UX writing, voice and tone, CTA copy, error message, empty state, loading UX, spinner, skeleton, confirmation dialog, delete flow, share flow, selection flow, navigation UX, motion guideline, dark pattern, inclusive writing, UX review, 제품 UX, UX 라이팅, 버튼 문구, 에러 문구, 빈 상태, 로딩, 스피너, 스켈레톤, 확인 모달, 삭제, 공유, 선택, 내비게이션, 인터랙션, 모션, 다크패턴."
---

# 제품 UX 원칙 (ds-product-ux)

## 목표

사용자가 화면에서 읽고, 선택하고, 기다리고, 복구하는 모든 순간을 더 명확하고 예측 가능하게 설계한다. 이 스킬은 문구만 다듬는 용도가 아니라, CTA부터 로딩, 확인, 삭제, 공유, 선택, 피드백, 내비게이션, 모션, 접근성까지 제품 UX의 판단 기준을 통합해서 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 플로우를 설계하거나 문구를 쓰거나 UX를 리뷰할 때는 아래 reference 문서를 직접 읽고 상황에 맞는 기준과 예시를 확인한 뒤 적용한다.

---

## 7대 핵심 원칙

### 1. 핵심 과업을 먼저 드러낸다

한 화면에서 사용자가 지금 해야 할 결정이 무엇인지 먼저 보이게 만든다. 설명이 많더라도 핵심 과업이 흐려지면 사용자는 머뭇거린다.

- 한 화면에는 가능하면 하나의 주된 선택과 하나의 주된 행동만 둔다
- 지금 결정에 꼭 필요한 정보만 먼저 보여준다
- 설명이 길어질수록 사용자가 이미 알고 있는 문장은 먼저 걷어낸다

#### 빠른 판단 기준

- 제목과 CTA만 보고도 지금 해야 할 일이 설명되면 유지한다
- 보조 문구가 없어도 이해되는 문장을 반복해서 두고 있으면 삭제를 먼저 검토한다
- 사용자가 다음 화면보다 현재 화면의 설명을 더 오래 읽어야 한다면 정보량을 다시 줄인다

→ 상세: [references/06-foundations-principles.md](references/06-foundations-principles.md)

### 2. 다음 행동이 예측되게 만든다

버튼과 링크는 사용자가 누른 뒤 무슨 일이 일어나는지 미리 알려줘야 한다. 기대한 결과 대신 예상하지 못한 화면이 나오면 신뢰가 빠르게 떨어진다.

- CTA는 막연한 가치가 아니라 다음 행동이나 다음 화면을 드러낸다
- 뒤로 가기, 닫기, 이동은 사용자의 정신모형을 거스르지 않는다
- 진입 직후 인터럽트나 뒤로 가기 방해처럼 흐름을 가로채는 패턴을 피한다

#### 빠른 판단 기준

- CTA가 “좋은 결과”만 말하고 “다음에 무엇을 하는지” 숨기면 다시 쓴다
- 뒤로 가기 직전에 혜택, 동의, 광고를 끼워 넣고 있다면 다크패턴으로 본다
- 선택을 거절하거나 나갈 수 있는 경로가 보이지 않으면 구조부터 수정한다

→ 상세: [references/01-action-patterns.md](references/01-action-patterns.md)

### 3. 말은 짧고 인간적으로 쓴다

사용자는 화면의 문장을 읽기보다 스캔한다. 쉬운 단어, 능동형, 긍정형, 사용자 중심 표현이 기본이다.

- 전문 용어, 축약어, 불필요한 한자어와 외래어를 줄인다
- 시스템 처리보다 사용자의 행동과 이익을 말한다
- 한 문장에는 하나의 목적만 담는다

#### 빠른 판단 기준

- 소리 내어 읽었을 때 어색하면 다시 쓴다
- “완료되었습니다”, “처리됩니다”보다 사용자가 한 행동으로 바꿀 수 있으면 바꾼다
- 에러나 제한을 말하면서 해결 방법이 빠져 있으면 불완전한 문장으로 본다

→ 상세: [references/02-ux-writing.md](references/02-ux-writing.md)

### 4. 사용자를 몰아붙이지 않고 선택권을 남긴다

확인, 삭제, 동의, 공유 같은 민감한 행동일수록 사용자가 스스로 선택하고 있다고 느껴야 한다. 공포감, 압박, 탈출 불가 구조는 단기 전환보다 장기 신뢰를 더 크게 해친다.

- 확인은 반드시 필요한 순간에만 쓴다
- 파괴적 행동은 중요도와 복구 가능성에 맞춰 다룬다
- 제안은 하되 강요하지 않는다

#### 빠른 판단 기준

- 사용자를 설득하기 위해 손해, 공포, 죄책감을 과장하고 있으면 다시 쓴다
- 삭제가 돌이킬 수 없는데 객체 이름과 결과 설명이 빠져 있으면 보완한다
- 사용자가 거절할 수 없는 구조면 문구보다 플로우를 먼저 수정한다

→ 상세: [references/01-action-patterns.md](references/01-action-patterns.md)

### 5. 로딩과 피드백은 기다림의 비용에 맞춘다

로딩 표현은 기다림의 길이와 범위에 맞아야 한다. 짧은 지연에는 아무것도 보여주지 않는 편이 낫고, 긴 지연에는 진행 상황과 다음 선택지가 필요하다.

- 먼저 실제 성능을 개선하고, 로더는 보조수단으로 쓴다
- 로딩 시간과 콘텐츠 구조에 맞춰 spinner, skeleton, progress를 고른다
- 성공과 실패 피드백은 사용자가 다음 행동을 정할 수 있게 해준다

#### 빠른 판단 기준

- 1초 이내 지연에 로더를 보여 플리커가 생기면 제거를 먼저 검토한다
- 10초 이상 걸리는데 아직도 불확정 spinner만 돌고 있으면 determinate progress를 검토한다
- 실패 후 재시도나 대안이 없으면 피드백이 아니라 막다른길이다

→ 상세: [references/03-loading-feedback.md](references/03-loading-feedback.md)

### 6. 모션은 장식이 아니라 이해를 돕는 기능으로 쓴다

좋은 모션은 원인과 결과를 보여주고 주의를 올바른 곳으로 이끈다. 구현 공수만 높이고 의미를 더하지 못하는 모션은 줄이는 편이 낫다.

- 모션은 상태 변화, 전환, 강조, 몰입에만 쓴다
- 기기와 맥락에 맞는 상호작용을 설계한다
- 반복되는 패턴은 토큰과 템플릿으로 시스템화한다

#### 빠른 판단 기준

- 정적인 UI로도 같은 가치를 전달할 수 있다면 모션을 다시 검토한다
- 모션이 있어도 무엇이 바뀌었는지 설명되지 않으면 실패한 모션으로 본다
- 자동 재생, 자동 스크롤, 자동 사라짐에는 제어권을 같이 제공한다

→ 상세: [references/04-interaction-motion.md](references/04-interaction-motion.md)

### 7. 접근성과 포용성은 별도 검토가 아니라 기본값이다

색상, 위치, 속도, 손가락 제스처, 글자 크기, 언어 수준은 사용자마다 다르게 느껴진다. 접근성과 포용성은 마지막 점검 항목이 아니라 설계의 시작점이어야 한다.

- 영구적, 일시적, 상황적 제약을 모두 고려한다
- 색상, 소리, 위치 하나에만 의미를 맡기지 않는다
- 큰 글씨, 낮은 대비, 느린 조작, 보조기기 사용에서도 흐름이 유지되어야 한다

#### 빠른 판단 기준

- 색을 빼면 의미 구분이 사라지면 다시 설계한다
- 오류가 발생했는데 다음 행동으로 이동할 포커스나 설명이 없으면 보완한다
- 사용자 집단을 단정하거나 특정 문화, 성별, 지역을 기본값처럼 쓰고 있다면 표현을 바꾼다

→ 상세: [references/05-accessibility-inclusion.md](references/05-accessibility-inclusion.md)

---

## references 가이드

아래 문서는 “더 자세한 참고자료”가 아니라, 실제 제품 UX 결정을 내리기 전 직접 읽어야 하는 구현 가이드다. 작업 성격에 따라 필요한 reference를 먼저 읽고 판단한다.

| 파일                                                                                 | 읽을 때                                                                     |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| [references/01-action-patterns.md](references/01-action-patterns.md)                 | CTA, 확인, 삭제, 공유, 선택, 내비게이션, 다크패턴 여부를 판단할 때          |
| [references/02-ux-writing.md](references/02-ux-writing.md)                           | 버튼 문구, 에러 메시지, 빈 상태, 안내 문구, 톤을 쓸 때                      |
| [references/03-loading-feedback.md](references/03-loading-feedback.md)               | spinner, skeleton, progress, toast, snackbar, 실패 안내를 결정할 때         |
| [references/04-interaction-motion.md](references/04-interaction-motion.md)           | 인터랙션과 모션의 역할, 기기별 상호작용, 모션 시스템화를 판단할 때          |
| [references/05-accessibility-inclusion.md](references/05-accessibility-inclusion.md) | 접근성, 포용성, 색상 대비, 큰 글씨, 제스처 대안, 입력/오류 흐름을 검토할 때 |
| [references/06-foundations-principles.md](references/06-foundations-principles.md)   | 상위 UX 원칙, 신뢰, 연속성, 브랜드 보이스, 핵심 과업 우선순위를 정리할 때   |
| [references/08-docs-index.md](references/07-docs-index.md)                           | retrieval 중심으로 관련 reference를 빠르게 찾을 때                          |

### 추천 로드 순서

- 플로우 리뷰나 화면 구조 판단: `06 → 01 → 03 → 05`
- 문구 작성이나 카피 개선: `06 → 02 → 01`
- 로딩/피드백/상태 전환 설계: `03 → 04 → 05`
- 민감한 액션(삭제, 결제, 동의, 공유): `01 → 02 → 05`

---

## 응답 패턴

이 스킬을 사용할 때는 원칙만 나열하지 말고, 사용자가 바로 설계에 옮길 수 있는 구조와 문구까지 함께 제안한다.

### 1. 플로우 리뷰 요청

아래 순서로 답하는 것을 기본값으로 둔다.

1. 현재 흐름의 문제점
2. 왜 신뢰나 과업 완료를 해치는지
3. 더 나은 대체 플로우
4. 바뀐 CTA, 제목, 본문 같은 권장 카피
5. 접근성, 다크패턴, 복구 경로 체크포인트

### 2. 민감한 액션 설계 요청

삭제, 해제, 취소, 동의 철회 같은 요청에는 아래 항목을 빠뜨리지 않는다.

- 진입 CTA와 그 이유
- 확인이 필요한지 여부
- 다이얼로그 제목, 본문, 버튼 라벨
- 실행 후 피드백과 undo 또는 대체 경로
- 연쇄 영향과 접근성 주의점

### 3. 로딩/피드백 설계 요청

시간대별 로딩 요소만 고르지 말고 아래까지 같이 제안한다.

- 각 상황의 시간대 분류
- 왜 spinner, skeleton, progress 중 하나를 골랐는지
- 5초 이후 추가 안내 문구나 상태 설명
- 실패 시 다음 행동
- 적절한 피드백 채널

---

## 범위

- 구현 수준의 접근성, ARIA, 키보드, 시맨틱 HTML → `fe-a11y`
- React 컴포넌트 구조, controlled/uncontrolled, compound components → `fe-react-patterns`
- 공유 UI 컴포넌트 API, primitive/component/block 구분 → `fe-ui-element-components`
- Tailwind CSS 스타일링, 토큰, className 병합 → `fe-tailwindcss`
- 성능 최적화 → `fe-react-performance`
- 일반 코드 품질과 리팩토링 → `fe-code-conventions`
- 기존 코드 리뷰 절차 → `fe-code-review`
