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

이 섹션은 카테고리 선택용이다. 여기서는 특정 스킬 이름으로 바로 점프하지 말고, 먼저 어떤 카테고리를 열어야 하는지 판단한다. 세부 스킬 선택은 아래 카테고리 블록에서 한다.

- trigger가 2개 이상 맞으면 relevant category를 모두 열고, 현재 작업 surface에 더 가까운 category부터 읽는다.

- onboarding, CTA, error state, loading, layout, typography, design research, screen/flow design, visual polish, visual inspection, responsive check, runtime design validation, design context, design critique, design audit, design boost, design improvement이면 `Design & UX`를 먼저 본다.
- content draft, technical documentation, prose polish, AI pattern removal, source gathering, fact check, product research, market research, JTBD, Kano, value proposition, market sizing이면 `Writing & content`를 먼저 본다.
- React UI, Zustand, TanStack Query, component split, shared UI, form, modal, accessibility, Tailwind, hydration mismatch, rerender, frontend review이면 `Frontend engineering`를 먼저 본다.
- auth, permission, validation, API contract, status code, Fastify, secure coding, secret handling, Kysely, Prisma, query builder, database setup, schema design, migration, driver adapter, persistence setup, state adapter면 `Security & backend`를 먼저 본다.
- technical SEO, indexing, crawlability, schema validation, Core Web Vitals, AI bot access, title/meta, on-page SEO, featured snippet, GEO면 `SEO`를 먼저 본다.
- browser automation, README, git/gh workflow, PDF, skill authoring, Vite, Turbopack, bundler migration, research-first workflow, official-doc verification이면 `Workflow & tooling`를 먼저 본다.
- image generation, image edit, hero image, illustration, compositing, visual asset backend면 `Web visuals`를 먼저 본다.
- memory tail, repo memory, remember this, durable fact, memory pollution 판단이면 `Memory & context`를 먼저 본다.

## 카테고리

### Writing & content

대표 trigger: content draft, technical documentation, prose polish, source gathering, product research

글 초안, 기술 문서, 문장 다듬기, 조사·팩트체크를 먼저 분류할 때 읽는다.

- `.github/skills/writing-content/SKILL.md`: social, blog, article writing methods, voice and structure, publishability checks
- `.github/skills/writing-clearly/SKILL.md`: clear prose, concise writing, AI pattern detection and correction (EN/KO), voice and rhythm
- `.github/skills/writing-document/SKILL.md`: technical documentation, changelog, release notes, API reference, migration guide, ADR, configuration reference, SDK documentation, getting started, how-to, troubleshooting
- `.github/skills/research-content-source/SKILL.md`: content research, source gathering, source ladder, research brief, claim inventory, fact check, credibility evaluation
- `.github/skills/research-product/SKILL.md`: product discovery, JTBD, Kano model, value proposition, competitive analysis, market sizing, user research, opportunity assessment, TAM/SAM/SOM, Porter's 5 Forces

### Design & UX

대표 trigger: layout, UX writing, typography, design research, visual review

화면 구조, copy/feedback, visual direction, reference-led UI 설계, runtime visual inspection이 필요할 때 읽는다.

- `.github/skills/ds-product-ux/SKILL.md`: CTA copy, feedback, loading, confirmation, trust-sensitive UX
- `.github/skills/ds-ui-patterns/SKILL.md`: layout pattern, hero, dashboard, section composition
- `.github/skills/ds-typography/SKILL.md`: font choice, pairing, scale, line-height, tracking, responsive type
- `.github/skills/ds-visual-design/SKILL.md`: palette, spacing, hierarchy, depth, overall visual polish
- `.github/skills/ds-visual-review/SKILL.md`: runtime visual inspection, browser-based UI review, responsive testing, layout/overflow fix workflow (agent-browser complementary)
- `.github/skills/research-design/SKILL.md`: reference-led screen/flow research, MCP 기반 retrieval, pattern extraction, reference-driven synthesis

### Web visuals

대표 trigger: image generation, image edit, hero image, illustration, compositing

이미지 생성, 수정, 합성 같은 visual asset 작업이 필요할 때 읽는다.

- `.github/skills/ds-image-gen/SKILL.md`: prompt-only image generation, edit, compositing

### Frontend engineering

대표 trigger: React UI, shared state, server state, accessibility, styling, frontend review

UI 구현, component architecture, state ownership, accessibility, styling, review 품질을 다룰 때 읽는다.

- `.github/skills/fe-a11y/SKILL.md`: semantic HTML, keyboard support, focus, ARIA
- `.github/skills/fe-code-conventions/SKILL.md`: naming, readability, cohesion, cleanup
- `.github/skills/fe-code-review/SKILL.md`: frontend diff review, regression, merge readiness
- `.github/skills/fe-react-patterns/SKILL.md`: component split, composition, state ownership
- `.github/skills/fe-react-performance/SKILL.md`: hydration, waterfalls, rerender, bundle cost
- `.github/skills/fe-tailwindcss/SKILL.md`: utility styling, theme tokens, responsive classes
- `.github/skills/fe-tanstack-query/SKILL.md`: query keys, queryOptions-based organization, invalidation, SSR hydration, .query.ts module structure
- `.github/skills/fe-ui-element-components/SKILL.md`: shared UI primitive, design-system API
- `.github/skills/fe-zustand/SKILL.md`: Zustand v5 client state, selectors, slices, persistence, Next.js hydration boundaries

### Security & backend

대표 trigger: auth, permission, API contract, validation, Fastify, secure coding, Kysely, Prisma, query builder, schema design, migration, persistence setup

보안, API 계약, backend framework, persistence setup, schema/migration, secure server implementation을 다룰 때 읽는다.

- `.github/skills/dev-security/SKILL.md`: auth, authorization, input validation, exploitability
- `.github/skills/be-api-design/SKILL.md`: REST contract, resource model, status code, error envelope
- `.github/skills/fastify-best-practices/SKILL.md`: Fastify route/plugin/error/security patterns
- `.github/skills/be-prisma/SKILL.md`: Prisma ORM schema design, migrations, query optimization, provider setup, Prisma v7 upgrade
- `.github/skills/be-kysely/SKILL.md`: type-safe SQL query builder, transactions, migrations

### SEO

대표 trigger: technical SEO, indexing, crawlability, on-page SEO, structured data, GEO

검색 엔진과 AI 검색을 위한 site mechanics, 메타데이터, 온페이지 구조, GEO 최적화가 필요할 때 읽는다.

- `.github/skills/seo-technical/SKILL.md`: technical SEO audit and remediation for crawlability, indexation, rendering, schema validation, Core Web Vitals, mobile, HTTPS, hreflang, platform indexing, AI bot access. Scope가 불명확한 경우 seo-technical의 audit workflow를 먼저 사용해 문제 분류 후 필요시 seo-content로 handoff
- `.github/skills/seo-content/SKILL.md`: search intent, keyword map, title/meta/social tags, on-page scoring, snippet formats, GEO-friendly content structure, refresh workflow

### Workflow & tooling

대표 trigger: browser automation, docs workflow, git/gh, PDF, research workflow, bundler tooling

browser automation, docs workflow, repo operations, research-first workflow, bundler/tooling 작업이 필요할 때 읽는다.

- `.github/skills/agent-browser/SKILL.md`: site navigation, scraping, screenshots, browser verification
- `.github/skills/brainstorming/SKILL.md`: creative or architectural direction setting before build
- `.github/skills/writing-readme/SKILL.md`: README creation, update, stale section review, audience fit
- `.github/skills/research-foundation/SKILL.md`: 자료조사 방법론, source ladder, 공식 문서 및 로컬 근거 합성
- `.github/skills/kick-research/SKILL.md`: user-invocable intensive research orchestration across research-* lanes
- `.github/skills/gh-cli/SKILL.md`: GitHub CLI workflow for repo, PR, issue operations
- `.github/skills/git-workflow/SKILL.md`: branch, commit, PR workflow
- `.github/skills/dev-vite/SKILL.md`: Vite config, import.meta features, plugin boundaries, library mode, low-level SSR, Rolldown/Oxc migration
- `.github/skills/dev-turbopack/SKILL.md`: Next.js Turbopack config, webpack migration, CSS/asset parity, bundle analysis, HMR/build diagnostics
- `.github/skills/pdf/SKILL.md`: PDF read, split, merge, OCR, fill
- `.github/skills/skill-creator/SKILL.md`: create or improve skills and evaluate trigger quality

### Memory & context

대표 trigger: memory tail, remember this, repo memory, durable fact, memory pollution

memory tail이나 durable signal 분류가 필요할 때 읽는다.

- `.github/skills/memory-synthesizer/SKILL.md`: memory scope selection, durable fact filtering, memory pollution 방지
