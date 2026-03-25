---
description: "Always-on workspace skill discovery index. Use when mapping a task to relevant local skills before implementation, review, design, backend, workflow, or memory work. Always consult this index before deciding which SKILL.md files to load."
applyTo: "**"
---

# 워크스페이스 스킬 인덱스

이 문서는 워크스페이스 스킬 discovery의 source of truth다.
상세 규칙은 각 `SKILL.md`가 owner고, 이 문서는 어떤 작업에서 어떤 스킬을 먼저 읽고, 그 뒤 어떤 reference까지 따라가야 하는지 빠르게 좁히는 registry까지 맡는다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

## 사용 규칙

- substantial work 전에 아래 카테고리에서 relevant skill을 먼저 찾는다.
- category가 2개 이상 맞으면 relevant skill을 모두 읽는다.
- 이 문서는 selection surface다. 실제 판단과 구현 규칙은 반드시 해당 `SKILL.md`를 읽고 따른다.
- category 이름이나 skill path가 바뀌면 dependent agent/reviewer 문서도 함께 갱신한다.

## 스킬 선택 루프

- user phrasing, changed surface, expected output에서 category 후보를 먼저 고른다.
- trigger가 약하게만 보여도 품질 lift가 크면 under-trigger보다 약간 pushy한 trigger를 허용한다. skill description은 discovery surface다.
- 선택한 skill의 `SKILL.md`를 읽은 뒤, body 안의 `references/` 포인터를 바로 찾는다.
- `SKILL.md`가 specific reference file이나 `references/ 가이드`를 주면 현재 subproblem에 맞는 reference 추가로 읽고 적용한다.

## 빠른 선택 기준

- onboarding, CTA, error state, loading, visual polish, layout, design research, screen/flow design이면 `Design & UX`를 먼저 본다.
- font pairing, type scale, line-height, letter-spacing, tracking, responsive typography, variable font 판단이면 `ds-typography`를 먼저 본다.
- React, component split, form, modal, accessibility, Tailwind, render flow, shared UI, frontend review면 `Frontend engineering`을 먼저 본다.
- auth, validation, API contract, status code, Fastify, secure coding, secret handling이면 `Security & backend`를 먼저 본다.
- query builder, database setup, Prisma, TanStack Query, hydration, mutation, state adapter면 `Data & state`를 먼저 본다.
- browser automation, README, git, gh, PDF, SEO, ideation, skill authoring, 자료조사, 레퍼런스 강화, 공식 문서 확인, 근거 기반 답변이면 `Workflow & tooling`를 먼저 본다.
- image generation, hero image, illustration, compositing, visual asset backend면 `Web visuals`를 먼저 본다.
- memory tail, repo memory, durable fact, memory pollution 판단이면 `Memory & context`를 먼저 본다.

## 카테고리

### Design & UX

대표 trigger: onboarding, CTA, typography system, font pairing, type scale, empty state, loading, hero, dashboard, visual hierarchy, refero research

화면 구조, UX writing, visual direction, research-first UI 설계가 필요할 때 읽는다.

- `.github/skills/ds-product-ux/SKILL.md`: CTA copy, feedback, loading, confirmation, trust-sensitive UX
- `.github/skills/ds-ui-patterns/SKILL.md`: layout pattern, hero, dashboard, section composition
- `.github/skills/ds-typography/SKILL.md`: font choice, pairing, scale, line-height, tracking, responsive type
- `.github/skills/ds-visual-design/SKILL.md`: palette, spacing, hierarchy, depth, overall visual polish
- `.github/skills/research-design/SKILL.md`: reference-led screen/flow research, MCP 기반 retrieval, pattern extraction, reference-driven synthesis

### Web visuals

대표 trigger: image generation, hero image, illustration, prompt refinement, compositing

이미지 생성이나 visual asset backend가 필요할 때 읽는다.

- `.github/skills/ds-image-gen/SKILL.md`: prompt-only image generation, edit, compositing

### Frontend engineering

대표 trigger: React, component API, modal, form, dropdown, a11y, Tailwind, rerender, design system

UI 구현, component architecture, accessibility, styling, review 품질을 다룰 때 읽는다.

- `.github/skills/fe-a11y/SKILL.md`: semantic HTML, keyboard support, focus, ARIA
- `.github/skills/fe-code-conventions/SKILL.md`: naming, readability, cohesion, cleanup
- `.github/skills/fe-code-review/SKILL.md`: frontend diff review, regression, merge readiness
- `.github/skills/fe-react-patterns/SKILL.md`: component split, composition, state ownership
- `.github/skills/fe-react-performance/SKILL.md`: hydration, waterfalls, rerender, bundle cost
- `.github/skills/fe-tailwindcss/SKILL.md`: utility styling, theme tokens, responsive classes
- `.github/skills/fe-ui-element-components/SKILL.md`: shared UI primitive, design-system API

### Security & backend

대표 trigger: auth, permission, endpoint, validation, status code, error contract, Fastify, secrets

보안, API 계약, backend framework, secure server implementation을 다룰 때 읽는다.

- `.github/skills/dev-security/SKILL.md`: auth, authorization, input validation, exploitability
- `.github/skills/be-api-design/SKILL.md`: REST contract, resource model, status code, error envelope
- `.github/skills/fastify-best-practices/SKILL.md`: Fastify route/plugin/error/security patterns

### Data & state

대표 trigger: Kysely, Prisma, TanStack Query, query key, mutation, hydration, Zustand, migration

database access, persistence setup, caching, server state, state adapter를 다룰 때 읽는다.

- `.github/skills/kysely/SKILL.md`: type-safe SQL query builder, transactions, migrations
- `.github/skills/prisma-database-setup/SKILL.md`: database provider setup, connection troubleshooting
- `.github/skills/tanstack-query-best-practices/SKILL.md`: query keys, caching, invalidation, optimistic update
- `.github/skills/zustand/SKILL.md`: `@json-render/zustand` state adapter integration

### Workflow & tooling

대표 trigger: browser automation, README, git, gh, PDF, SEO, skill authoring

browser automation, ideation, docs, git, SEO, PDF, skill authoring 같은 작업 흐름 도구가 필요할 때 읽는다.

- `.github/skills/agent-browser/SKILL.md`: site navigation, scraping, screenshots, browser verification
- `.github/skills/brainstorming/SKILL.md`: creative or architectural direction setting before build
- `.github/skills/writing-readme/SKILL.md`: README creation, update, stale section review, audience fit
- `.github/skills/evidence-first-research/SKILL.md`: reference-first 조사, source ladder, 공식 문서 및 로컬 근거 합성
- `.github/skills/gh-cli/SKILL.md`: GitHub CLI workflow for repo, PR, issue operations
- `.github/skills/git-workflow/SKILL.md`: branch, commit, PR workflow
- `.github/skills/pdf/SKILL.md`: PDF read, split, merge, OCR, fill
- `.github/skills/seo-audit/SKILL.md`: SEO audit and diagnosis
- `.github/skills/skill-creator/SKILL.md`: create or improve skills and evaluate trigger quality

### Memory & context

대표 trigger: memory tail, remember this, repo memory, durable fact, memory pollution

memory tail이나 durable signal 분류가 필요할 때 읽는다.

- `.github/skills/memory-synthesizer/SKILL.md`: memory scope selection, durable fact filtering, memory pollution 방지
