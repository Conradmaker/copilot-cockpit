---
name: fe-code-review
description: "Unified frontend code review guide integrating clean code, React patterns, accessibility, and performance checks. Use this skill when reviewing pull requests, conducting code reviews, auditing frontend code quality, or when the user asks to review their code. Always use this skill when the user asks to check, review, or improve existing code quality. Triggers on: code review, PR review, review my code, audit code, 코드 리뷰, PR 리뷰, 코드 검토, 코드 감사, 코드 봐줘, 이거 괜찮아?, 이 코드 어때?, 뭐가 잘못됐어?, 개선할 점, 코드 피드백, 코드 품질 체크, PR 올리기 전에, 머지해도 될까, pull request."
---

# 프론트엔드 코드 리뷰 가이드

코드 리뷰를 체계적으로 진행하기 위한 통합 가이드예요. 4단계 리뷰 절차와 체크리스트를 제공해요.

## 리뷰 절차

코드 리뷰는 다음 4단계 순서로 진행해요:

### 1단계: 코드 컨벤션 (가독성 · 예측가능성 · 응집도 · 결합도)

변경된 코드가 깨끗하고 유지보수하기 쉬운지 확인해요.
→ 자세한 원칙과 예제는 `fe-code-conventions`를 참고하세요.

**핵심 체크 포인트:**
- 매직 넘버에 의미 있는 이름이 있는가?
- 함수/변수 이름이 동작을 정확히 설명하는가?
- 숨겨진 사이드 이펙트가 없는가?
- 함께 변경되는 코드가 같은 위치에 있는가?

### 2단계: React 패턴 (설계 · 합성 · 상태관리)

컴포넌트 구조와 패턴이 올바른지 확인해요.
→ 자세한 패턴과 예제는 `fe-react-patterns`를 참고하세요.

**핵심 체크 포인트:**
- Boolean props 대신 명시적 variant를 사용하는가?
- Compound Component로 관련 컴포넌트가 그룹화되었는가?
- Props Drilling 대신 Composition 패턴을 사용하는가?
- Context가 interface로 설계되었는가?

### 3단계: 접근성 (ARIA · 시맨틱 · 키보드)

인터랙티브 요소가 모든 사용자에게 접근 가능한지 확인해요.
→ 자세한 규칙과 패턴은 `fe-a11y`를 참고하세요.

**핵심 체크 포인트:**
- 모든 인터랙티브 요소에 접근 가능한 이름(label)이 있는가?
- 시맨틱 HTML 요소를 우선 사용하는가?
- 키보드로 모든 기능을 사용할 수 있는가?
- UI 컴포넌트가 접근성 패턴을 따르는가?

### 4단계: 성능 (번들 · 리렌더 · 서버)

성능에 부정적인 영향이 없는지 확인해요.
→ 자세한 최적화 규칙은 `fe-react-performance`를 참고하세요.

**핵심 체크 포인트:**
- 비동기 요청이 병렬로 처리되는가?
- barrel 파일의 re-export를 피하는가?
- 불필요한 리렌더가 방지되었는가?
- 서버 데이터 캐싱이 적절한가?

## 리뷰 결과 보고 형식

발견한 이슈는 다음 형식으로 보고해요:

```
파일경로:줄번호 - [카테고리] 이슈 설명
  → 제안: 개선 방법
```

### 심각도 분류

- 🔴 **Critical**: 반드시 수정해야 해요 (버그, 접근성 위반, 보안 문제)
- 🟡 **Warning**: 수정을 권장해요 (성능 이슈, 패턴 위반, 가독성 저하)
- 🟢 **Suggestion**: 고려해 볼 만한 개선이에요 (더 나은 패턴, 미세 최적화)

## 이 스킬을 사용하지 않는 경우

- 새 코드를 작성할 때는 각 전문 스킬을 직접 참고하세요 (fe-code-conventions, fe-react-patterns, fe-a11y, fe-react-performance)
- 백엔드/서버 코드 리뷰에는 이 스킬이 적용되지 않아요

## 상세 체크리스트

리뷰 단계별 상세 체크리스트가 필요하면 `references/checklist.md`를 참고하세요.
