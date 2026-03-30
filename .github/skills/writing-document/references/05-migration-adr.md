# Migration Guide & ADR 작성 가이드

이 문서는 마이그레이션 가이드, deprecation notice, Architecture Decision Record(ADR)의 구조와 템플릿을 다룬다.

---

## 마이그레이션 가이드

### 목표

독자가 이전 버전에서 새 버전으로 안전하게 전환하는 것이 목표다. 무엇이 바뀌었고, 무엇을 해야 하고, 언제까지인지를 명확히 안내한다.

### 구조: What changed → Why → Step-by-step → Timeline → Support

| 섹션 | 내용 |
|-----|-----|
| **What changed** | 무엇이 바뀌었는지 요약 |
| **Why** | 왜 이 변경이 필요했는지 (독자 이점 중심) |
| **Step-by-step migration** | 구체적 전환 절차 |
| **Timeline** | 날짜별 마일스톤 (경고 시작 → 지원 중단 → 제거) |
| **Support** | 도움을 받을 수 있는 경로 |

### 템플릿

```markdown
# Migrating from v{X} to v{Y}

{한 문장: 이 가이드를 따르면 v{X}에서 v{Y}로 전환할 수 있다.}

## What changed

{주요 변경 사항 요약. bullet list로 주요 breaking change를 나열한다.}

- {변경 1: 이전 동작 → 새 동작}
- {변경 2: 제거된 API}
- {변경 3: 새로운 필수 설정}

## Why this change

{독자 관점에서 이 변경이 가져다주는 이점. 내부 사정이 아니라 독자가 얻는 것을 쓴다.}

## Prerequisites

- {마이그레이션 전 필요한 조건}
- {백업 안내}

## Step 1: {동사 + 작업}

{지시 + Before/After 코드.}

**Before (v{X}):**

\`\`\`ts
// 이전 코드
\`\`\`

**After (v{Y}):**

\`\`\`ts
// 새 코드
\`\`\`

## Step 2: {동사 + 작업}

{같은 패턴 반복.}

## Step 3: {동사 + 작업}

{같은 패턴 반복.}

## Verify

{전환 완료 확인 방법. 테스트 명령어, 예상 결과.}

\`\`\`bash
npm test
\`\`\`

## Timeline

| Date | Milestone |
|------|-----------|
| {날짜} | v{Y} released, v{X} still supported |
| {날짜} | v{X} returns deprecation warnings |
| {날짜} | v{X} end of support |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| {마이그레이션 중 흔한 에러} | {해결 방법} |

## Need help?

{지원 채널: 포럼, 이슈 트래커, 이메일 등.}
```

### 작성 규칙

- **Before/After 코드를 매 단계에 포함한다.** 코드 diff가 가장 명확한 안내다
- 자동화 도구(codemod, migration script)가 있으면 먼저 안내한다
- 백업/롤백 방법을 Prerequisites에 포함한다
- Timeline에 날짜를 반드시 넣는다. "곧"은 날짜가 아니다
- Troubleshooting 섹션으로 흔한 실수를 미리 안내한다

---

## Deprecation Notice

### 구조

Deprecation은 아래 정보를 반드시 포함한다.

| 항목 | 내용 |
|-----|-----|
| **무엇이 deprecated인가** | 구체적 API, 기능, 옵션 |
| **왜 deprecated인가** | 이유 (한 문장) |
| **대안은 무엇인가** | 대체 API, 기능, 코드 예시 |
| **언제 제거되는가** | 구체적 날짜 또는 버전 |

### 템플릿

```markdown
## Deprecated: {API/Feature name}

> **Deprecated since v{X}.** Will be removed in v{Y} ({날짜}).

{한 문장: 무엇이 deprecated이고 왜.}

### Migration

**Before:**

\`\`\`ts
// deprecated 코드
\`\`\`

**After:**

\`\`\`ts
// 대안 코드
\`\`\`

### Timeline

- **v{X}**: Deprecation warning added
- **v{Y}** ({날짜}): Will be removed
```

### 경고 수준

| 수준 | 사용 시점 | 표시 방법 |
|-----|---------|---------|
| **Notice** | 대안이 준비되었지만 제거 일정 미정 | 문서에 deprecation 표시 |
| **Warning** | 제거 일정이 확정됨 | 문서 + runtime warning |
| **Critical** | 제거까지 30일 이내 | 문서 + 눈에 띄는 배너 + changelog 상단 |

### 작성 규칙

- "곧 제거됩니다"는 쓰지 않는다. 날짜 또는 버전을 명시한다
- 대안 없이 deprecated하지 않는다. 대안이 없으면 그 사실을 명시한다
- Before/After 코드를 반드시 포함한다
- 단계적 제거(soft deprecation → hard deprecation → removal)를 타임라인으로 보여준다

---

## Architecture Decision Record (ADR)

### 목표

기술적 결정의 배경, 선택지, 결과를 기록해서 나중에 "왜 이렇게 했지?"라는 질문에 답할 수 있게 한다.

### 포맷: Michael Nygard 형식

```markdown
# ADR-{번호}: {결정 제목}

**Status**: {Proposed | Accepted | Deprecated | Superseded by ADR-{번호}}
**Date**: {YYYY-MM-DD}
**Deciders**: {참여자}

## Context

{어떤 문제나 상황이 있었는가. 이 결정이 필요한 배경.}

## Decision

{무엇을 결정했는가. 명확하게 한 문장 이상으로.}

## Consequences

### Positive

- {긍정적 결과}

### Negative

- {부정적 결과, 트레이드오프}

### Neutral

- {중립적 결과}

## Alternatives Considered

### {대안 1}

{설명과 채택하지 않은 이유.}

### {대안 2}

{설명과 채택하지 않은 이유.}
```

### ADR 상태 관리

| 상태 | 의미 |
|-----|-----|
| **Proposed** | 검토 대기 중. 아직 확정되지 않음 |
| **Accepted** | 채택됨. 현재 유효한 결정 |
| **Deprecated** | 더 이상 유효하지 않음. 후속 결정 참조 |
| **Superseded by ADR-{N}** | 새 결정으로 대체됨. 후속 ADR 번호 명시 |

### 작성 규칙

- **Context는 객관적 사실만 쓴다.** 판단은 Decision에서 한다
- Decision은 모호하지 않게 쓴다. "~를 고려한다"가 아니라 "~를 사용한다"
- Consequences는 좋은 것과 나쁜 것을 모두 기록한다. 나쁜 결과를 숨기지 않는다
- Alternatives Considered를 반드시 포함한다. 왜 다른 선택지를 버렸는지가 미래의 맥락이다
- 상태가 바뀌면 ADR을 삭제하지 않고, 상태만 갱신한다

### 번호 체계

- 순차 번호: `ADR-001`, `ADR-002`, ...
- 날짜 기반: `ADR-2026-02-08-{slug}`
- 프로젝트에서 하나를 정해서 일관되게 사용한다

### 파일 관리

```
docs/
  adr/
    ADR-001-use-postgresql.md
    ADR-002-adopt-prisma-orm.md
    ADR-003-switch-to-kysely.md    # Status: Superseded by ADR-003
    README.md                       # ADR 목록과 현재 상태
```

- `README.md`에 ADR 목록 테이블을 유지한다
- Superseded된 ADR은 삭제하지 않는다. 역사적 맥락으로 보존한다

---

## Internal Technical Spec

### 목표

구현 전에 무엇을 만들 것이고, 왜 이렇게 설계하는지를 문서화한다. ADR이 단일 결정에 집중한다면, technical spec은 하나의 기능이나 시스템의 전체 설계를 다룬다.

### 구조

```markdown
# Technical Spec: {기능/시스템 이름}

**Status**: {Draft | In Review | Approved | Implemented}
**Author**: {작성자}
**Date**: {YYYY-MM-DD}
**Reviewers**: {리뷰어}

## Summary

{한 문단: 무엇을 만들고, 왜 필요한가.}

## Goals

- {목표 1}
- {목표 2}

## Non-goals

- {명시적으로 다루지 않는 것}

## Design

{아키텍처, 데이터 모델, API 설계, 시퀀스 다이어그램 등.}

## Alternatives Considered

{고려했지만 선택하지 않은 접근 방식과 이유.}

## Open Questions

- {아직 결정되지 않은 사항}

## Implementation Plan

{단계별 구현 계획. 마일스톤, 의존성.}
```

### 작성 규칙

- **Non-goals를 반드시 포함한다.** 범위를 명확히 제한하는 것이 핵심이다
- Summary와 Goals만 읽어도 전체 방향이 파악되어야 한다
- Open Questions를 숨기지 않는다. 미결정 사항은 명시적으로 표시한다

---

## 유형별 셀프 리뷰 체크리스트

### 마이그레이션 가이드

- [ ] What changed가 bullet list로 명확히 요약되어 있다
- [ ] 매 단계에 Before/After 코드가 있다
- [ ] Timeline에 구체적 날짜가 있다
- [ ] 자동화 도구(codemod, script)가 있으면 먼저 안내한다
- [ ] 백업/롤백 방법이 Prerequisites에 있다
- [ ] Troubleshooting 섹션이 있다
- [ ] 지원 채널이 안내되어 있다

### Deprecation Notice

- [ ] deprecated 대상, 이유, 대안, 제거 시점이 모두 있다
- [ ] Before/After 코드가 있다
- [ ] "곧"이 아니라 구체적 날짜/버전이 있다
- [ ] 대안이 없으면 그 사실을 명시했다

### ADR

- [ ] Status, Date, Deciders가 있다
- [ ] Context가 객관적 사실로만 구성되어 있다
- [ ] Decision이 모호하지 않다
- [ ] Consequences에 긍정·부정 모두 기록되어 있다
- [ ] Alternatives Considered가 있다
- [ ] 상태 변경 시 삭제 대신 상태만 갱신한다

### Technical Spec

- [ ] Summary만 읽어도 방향이 파악된다
- [ ] Non-goals가 명시되어 있다
- [ ] Open Questions가 숨겨지지 않았다
