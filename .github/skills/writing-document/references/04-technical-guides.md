# Technical Guides 작성 가이드

이 문서는 How-to guide, Tutorial, Getting Started / Quickstart, Troubleshooting guide의 구조와 템플릿을 다룬다.

---

## 유형 구분

작성 전에 어떤 유형인지 먼저 고른다. 유형에 따라 구조가 달라진다.

| 유형 | 독자의 상태 | 핵심 질문 | 결과물 |
|-----|----------|---------|------|
| **Getting Started / Quickstart** | 처음 시작하는 사용자 | 가장 빠르게 동작하는 상태를 만드는 법은? | 최소 동작 환경 |
| **Tutorial** | 학습하고 싶은 사용자 | 처음부터 끝까지 따라하면 무엇이 완성되는가? | 완성된 결과물 |
| **How-to guide** | 특정 작업을 해야 하는 사용자 | 이 작업을 어떻게 하는가? | 작업 완료 |
| **Troubleshooting** | 문제를 겪고 있는 사용자 | 이 에러를 어떻게 고치는가? | 문제 해결 |

### 유형 판단 기준

- "5분 안에 시작하기" → **Getting Started**
- "블로그 앱을 만들어보자" → **Tutorial**
- "OAuth 2.0 연동하기" → **How-to**
- "CORS 에러 해결하기" → **Troubleshooting**

---

## Getting Started / Quickstart

### 목표

독자가 가장 빠르게 첫 번째 동작하는 상태를 만드는 것이 목표다. 깊이보다 속도를 우선한다.

### 템플릿

```markdown
# Getting Started with {Product}

{한 문장: 이 가이드를 마치면 무엇을 할 수 있는지.}

## Prerequisites

- {필수 도구/환경 + 버전}
- {필수 계정/접근 권한}

## Step 1: Install

{설치 명령어.}

\`\`\`bash
npm install {package}
\`\`\`

## Step 2: Configure

{최소 설정.}

\`\`\`ts filename="config.ts"
// 최소 설정 코드
\`\`\`

## Step 3: Run

{실행 확인.}

\`\`\`bash
npm run dev
\`\`\`

{성공 시 보이는 화면이나 출력 예시.}

## Next Steps

- {심화 가이드 링크}
- {관련 Tutorial 링크}
```

### 작성 규칙

- **3~5단계를 넘지 않는다.** 첫 동작까지 최단 경로만 다룬다
- 모든 단계에 복붙 가능한 코드를 넣는다
- "왜" 이렇게 하는지 설명은 최소화한다. Getting Started에서 독자는 이해보다 실행을 원한다
- 성공 확인 방법을 마지막 단계에 넣는다 (화면 스크린샷, 출력 메시지, 테스트 통과)
- Next Steps에서 Tutorial이나 심화 How-to로 안내한다

---

## Tutorial

### 목표

독자가 처음부터 끝까지 따라하면 하나의 완성된 결과물을 만드는 것이 목표다.

### 템플릿

```markdown
# Tutorial: Build a {결과물}

{한 문장: 이 Tutorial을 마치면 무엇이 완성되는지.}

**소요 시간**: {예상 시간}
**난이도**: {Beginner / Intermediate / Advanced}

## What you'll build

{완성된 결과물 스크린샷 또는 설명.}

## Prerequisites

- {사전 지식: "This tutorial assumes you know X"}
- {필요한 도구/환경}

## Step 1: {동사 + 작업}

{이 단계에서 무엇을 하는지 한 문장.}

\`\`\`tsx filename="path/to/file.tsx"
// 코드
\`\`\`

{필요 시 짧은 설명.}

## Step 2: {동사 + 작업}

{코드 + 설명 반복.}

## Step 3: {동사 + 작업}

{코드 + 설명 반복.}

## Verify

{완성 상태 확인 방법. 스크린샷이나 테스트 결과.}

## Summary

{배운 것 + Next Steps 링크.}
```

### 작성 규칙

- **완성된 결과물이 명확해야 한다.** "이것을 만든다"를 서두에 선언한다
- 매 단계는 **동사**로 시작한다: "Create the database", "Add authentication"
- 매 단계에 코드를 포함한다. 설명만 있는 단계는 다른 단계에 합친다
- 소요 시간과 난이도를 밝혀서 독자가 진행 여부를 판단하게 한다
- 사전 조건을 명확히 적는다. "React를 안다고 가정한다" 같은 한 줄이면 충분하다
- 마지막에 **Verify** 섹션으로 완성 상태를 확인시킨다

---

## How-to Guide

### 목표

독자가 특정 작업 하나를 완료하는 것이 목표다. Tutorial처럼 처음부터 전체를 만드는 것이 아니라, 기존 프로젝트에서 특정 작업을 수행하는 방법을 안내한다.

### 템플릿

```markdown
# How to {동사 + 작업}

{한 문장: 이 가이드를 마치면 무엇을 할 수 있는지.}

**난이도**: {Beginner / Intermediate / Advanced}
**소요 시간**: {예상 시간}

## Prerequisites

- [ ] {필요 도구 + 버전}
- [ ] {선행 작업 (링크)}

## Overview

{전체 흐름을 한 문단으로 요약.}

## Step 1: {동사 + 작업}

{지시 + 코드.}

\`\`\`bash
{명령어}
\`\`\`

> **Tip**: {이 단계의 팁.}

## Step 2: {동사 + 작업}

{지시 + 코드.}

⚠️ **Warning**: {흔한 실수.}

## Step 3: {동사 + 작업}

{지시 + 코드.}

## Verify

{작업 완료 확인 방법.}

## Troubleshooting

| Problem | Solution |
|---------|----------|
| {에러 메시지 또는 증상} | {해결 방법} |
| {에러 메시지 또는 증상} | {해결 방법} |

## Next Steps

- {관련 심화 가이드}
- {연결되는 작업}
```

### 작성 규칙

- **작업 하나에 집중한다.** "OAuth 연동하기"와 "사용자 관리하기"를 한 문서에 넣지 않는다
- 매 단계 제목에 **동사**를 넣는다
- Prerequisites는 체크리스트 형태로 작성한다
- 끝에 Troubleshooting 섹션을 넣어 흔한 실수와 해결법을 안내한다
- Tip과 Warning을 적절히 배치한다. 단, 매 단계마다 넣지 않는다

---

## Troubleshooting Guide

### 목표

독자가 겪고 있는 문제를 빠르게 찾아서 해결하는 것이 목표다.

### 템플릿

```markdown
# Troubleshooting: {영역}

{한 문장: 이 문서에서 다루는 문제 범위.}

## Common Issues

### {에러 메시지 또는 증상}

**증상**: {독자가 보는 화면, 에러 메시지, 또는 동작.}

**원인**: {왜 이런 일이 발생하는지 한 문장.}

**해결**:

1. {첫 번째 시도}
2. {두 번째 시도}
3. {여전히 안 되면}

\`\`\`bash
# 해결 명령어
\`\`\`

---

### {다음 에러 메시지 또는 증상}

{같은 구조 반복.}

## FAQ

**Q: {자주 묻는 질문}**

A: {답변. 필요하면 코드 포함.}

## Still having issues?

{지원 채널 안내: 포럼, 이슈 트래커, 지원 이메일 등.}
```

### 작성 규칙

- 에러 메시지를 **그대로** 제목에 쓴다. 독자는 에러 메시지를 복사해서 검색한다
- **증상 → 원인 → 해결** 순서를 지킨다. 원인만 설명하고 해결법이 없으면 안 된다
- 해결 방법은 **가장 간단한 것부터** 순서대로 나열한다
- 코드를 포함한다. "설정을 변경하세요"보다 "이 줄을 추가하세요"가 낫다
- 모든 문제를 한 문서에 넣지 않는다. 영역별로 분리한다

---

## 공통 작성 패턴

### Tech Stack 테이블

Getting Started나 프로젝트 문서에서 기술 스택을 한눈에 보여줄 때 사용한다.

```markdown
| Layer     | Technology | Version |
|-----------|-----------|---------|
| Language  | TypeScript | 5.x     |
| Framework | Next.js    | 14.x    |
| Database  | PostgreSQL | 16      |
| ORM       | Prisma     | 5.x     |
```

### Directory Map

프로젝트 구조를 설명할 때 사용한다.

```markdown
| Directory        | Purpose                          |
|-----------------|----------------------------------|
| `src/components/` | React UI components              |
| `src/api/`       | API route handlers               |
| `src/lib/`       | Shared utilities                 |
| `prisma/`        | Database schema and migrations   |
| `tests/`         | Test suites                      |
```

### Common Tasks 테이블

```markdown
| I want to...            | Command / Location           |
|------------------------|------------------------------|
| Run dev server         | `npm run dev`                |
| Run tests              | `npm test`                   |
| Add a database table   | `prisma/schema.prisma`       |
| Add an API endpoint    | `src/app/api/`               |
```

---

## 유형별 셀프 리뷰 체크리스트

### Getting Started

- [ ] 3~5단계 이하로 첫 동작까지 도달한다
- [ ] Prerequisites에 도구 이름 + 버전이 있다
- [ ] 모든 단계에 복붙 가능한 코드가 있다
- [ ] 마지막에 성공 확인 방법이 있다
- [ ] Next Steps로 심화 가이드를 안내한다

### Tutorial

- [ ] "무엇을 만드는가"가 서두에 선언되어 있다
- [ ] 소요 시간과 난이도가 명시되어 있다
- [ ] 사전 조건이 명확하다
- [ ] 매 단계에 코드가 있다
- [ ] Verify 섹션으로 완성 상태를 확인한다

### How-to

- [ ] 작업 하나에 집중한다
- [ ] Prerequisites가 체크리스트 형태다
- [ ] 매 단계 제목에 동사가 있다
- [ ] Troubleshooting 섹션이 끝에 있다
- [ ] Tip/Warning이 적절히 배치되어 있다 (과하지 않다)

### Troubleshooting

- [ ] 에러 메시지가 제목에 그대로 포함되어 있다
- [ ] 증상 → 원인 → 해결 순서를 지킨다
- [ ] 해결 방법에 코드가 포함되어 있다
- [ ] 가장 간단한 해결법부터 나열한다
- [ ] "Still having issues?" 섹션에 지원 채널이 있다
