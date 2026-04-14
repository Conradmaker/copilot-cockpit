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

## Surface-trigger 재평가

초기 user phrasing만으로 끝내지 않는다. 작업 도중 current file, changed surface, selected symbol, current phase, active artifact, path, subagent synthesis처럼 현재 문제 해석을 바꾸는 evidence가 나타나면 relevant skill candidate를 다시 평가하고  surface에 맞춰 active skill set을 확장하거나 갱신하는 것이다.

### 신호

- 현재 보고 있는 artifact의 역할이 바뀌었는가.
- selected symbol, changed function/class, failing output, lint/test error가 새 문제 축을 드러내는가.
- subagent나 추가 탐색 결과가 기존 가정보다 더 강한 evidence를 가져왔는가.
- 기존 skill set만으로는 현재 subproblem을 설명하기 약해졌는가.
- 작업의 흐름이 바뀌었는가.
- current file이나 changed surface가 특정 lane을 강하게 시사하는가. path/파일 신호는 대표 예시일 뿐이고, 재탐색의 핵심은 변화한 문제 해석이다.

### 적용 규칙

- weak signal 하나만으로 즉시 전환하지는 않는다. 다만 새 evidence가 현재 subproblem을 materially 바꾸면 candidate 단계에서 멈추지 말고 relevant skill을 바로 읽는다.
- 이미 읽은 skill은 surface가 materially change되지 않으면 다시 읽지 않는다. 하지만 `already loaded`는 새 category 진입을 막는 이유가 아니다.
- 복합 작업에서는 active skill set이 고정되지 않는다. frontend, design, backend, verification skill이 순차적으로 계속해서 추가될 수 있다.
- category thrash를 피한다. 새 evidence가 기존 판단보다 강할 때면 전환하거나 확장한다.
- initial discovery 이후, clarification 이후, major file-surface change 이후, subagent 결과 수신 직후, error/test/lint output이 새 축을 드러낸 직후에는 이 루프를 다시 돈다.
- 변화가 없더라도 같은 skill set으로 여러 탐색/수정이 이어지는데 진전이 없으면 safety check로 한 번 더 재평가한다.
- subagent도 packet, current file, 새 evidence를 읽은 직후 이 루프를 다시 돈다. main agent가 relevant skill을 초반에 다 읽었다고 가정하지 않는다.

## 빠른 선택 기준

이 섹션은 카테고리 선택용이다. 여기서는 특정 스킬 이름으로 바로 점프하지 말고, 먼저 어떤 카테고리를 열어야 하는지 판단한다. 세부 스킬 선택은 아래 카테고리 블록에서 한다.

- trigger가 2개 이상 맞으면 relevant category를 모두 열고, 현재 작업 surface에 더 가까운 category부터 읽는다.
- current artifact가 `prd.md`, `design.md`, `technical.md`, `execution-plan.md`이면 현재 phase owner와 support lane skill을 다시 평가한다.

- onboarding, CTA, error state, loading, layout, typography, design research, screen/flow design, visual polish, visual inspection, responsive check, runtime design validation, design context, design critique, design audit, design boost, design improvement, design prompt, prompt refinement, Designer handoff, anti-ai-slop, AI slop, generic UI, template UI, AI-generated look, AI가 만든 것 같은이면 `Design & UX`를 먼저 본다.
- content draft, technical documentation, prose polish, AI pattern removal, source gathering, fact check, product research, market research, JTBD, Kano, value proposition, market sizing이면 `Writing & content`를 먼저 본다.
- React UI, Zustand, TanStack Query, component split, shared UI, form, modal, accessibility, Tailwind, hydration mismatch, rerender, frontend review, shadcn, shadcn-ui, components.json, FieldGroup, data-icon, preset, registry, UI library migration, ai-elements, AI chat, chatbot, AI assistant UI, AI SDK, useChat, Conversation, Message, PromptInput, AI streaming, tool invocation UI이면 `Frontend engineering`를 먼저 본다.
- auth, permission, validation, API contract, status code, Fastify, secure coding, secret handling, Kysely, Prisma, Drizzle, query builder, database setup, schema design, migration, driver adapter, persistence setup, state adapter면 `Security & backend`를 먼저 본다.
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

화면 구조, copy/feedback, visual direction, reference-led UI 설계, design prompt authoring, runtime visual inspection이 필요할 때 읽는다.

- `.github/skills/ds-product-ux/SKILL.md`: CTA copy, feedback, loading, confirmation, trust-sensitive UX
- `.github/skills/ds-ui-patterns/SKILL.md`: layout pattern, hero, dashboard, section composition
- `.github/skills/ds-typography/SKILL.md`: font choice, pairing, scale, line-height, tracking, responsive type
- `.github/skills/ds-visual-design/SKILL.md`: palette, spacing, hierarchy, depth, overall visual polish
- `.github/skills/ds-anti-ai-slop/SKILL.md`: AI-generated UI anti-pattern catalog (38 rules), AI slop detection, generic UI audit, visual tell identification, template feel removal
- `.github/skills/ds-visual-review/SKILL.md`: runtime visual inspection, browser-based UI review, responsive testing, layout/overflow fix workflow (agent-browser complementary)
- `.github/skills/research-design/SKILL.md`: reference-led screen/flow research, MCP 기반 retrieval, pattern extraction, reference-driven synthesis
- `.github/skills/writing-design-prompt/SKILL.md`: design prompt authoring/refinement, Designer handoff wording, reference-to-prompt translation, preserve-without-drift framing

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
- `.github/skills/fe-shadcn-ui/SKILL.md`: shadcn/ui component integration, composition rules, FieldGroup/Field forms, base-vs-radix, CLI/MCP tools, presets, component styling, UI library migration
- `.github/skills/fe-ui-element-components/SKILL.md`: shared UI primitive, design-system API
- `.github/skills/fe-zustand/SKILL.md`: Zustand v5 client state, selectors, slices, persistence, Next.js hydration boundaries
- `.github/skills/fe-ai-elements/SKILL.md`: AI Elements 컴포넌트, AI chat interface, Conversation/Message/Tool/PromptInput, Vercel AI SDK useChat integration, streaming UI, multi-modal input, tool invocation display

### Security & backend

대표 trigger: auth, permission, API contract, validation, Fastify, secure coding, Kysely, Prisma, Drizzle, query builder, schema design, migration, persistence setup

보안, API 계약, backend framework, persistence setup, schema/migration, secure server implementation을 다룰 때 읽는다.

- `.github/skills/dev-security/SKILL.md`: auth, authorization, input validation, exploitability
- `.github/skills/be-api-design/SKILL.md`: REST contract, resource model, status code, error envelope
- `.github/skills/fastify-best-practices/SKILL.md`: Fastify route/plugin/error/security patterns
- `.github/skills/be-prisma/SKILL.md`: Prisma ORM schema design, migrations, query optimization, provider setup, Prisma v7 upgrade
- `.github/skills/be-drizzle/SKILL.md`: Drizzle ORM type-safe SQL, schema design, migrations, query patterns, connection management, multi-dialect support (PostgreSQL, MySQL, SQLite)
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
