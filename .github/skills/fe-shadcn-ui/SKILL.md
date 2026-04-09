---
name: fe-shadcn-ui
description: "shadcn/ui 컴포넌트 통합, 설정, 커스터마이징, composition, 스타일링 규칙을 위한 스킬이다. Use when adding, composing, styling, debugging, or customizing shadcn/ui components, setting up projects, choosing Radix vs Base UI, wiring FieldGroup/Field form layouts, applying presets, using CLI/MCP tools, or migrating from MUI/Chakra/Ant Design. Always consult this skill for any shadcn/ui work, even if the user only asks to 'add a button', 'make a form', 'customize the theme', or 'set up shadcn'. For React architecture use fe-react-patterns; for Tailwind config use fe-tailwindcss; for shared primitives use fe-ui-element-components; for accessibility use fe-a11y. Triggers on: shadcn, shadcn-ui, components.json, cn, cva, Radix UI, Base UI, FieldGroup, Field, data-icon, npx shadcn, preset, registry, UI library migration, 컴포넌트 추가, 테마 커스터마이징, 폼 레이아웃."
---

# shadcn/ui 컴포넌트 통합

## 목표

shadcn/ui 컴포넌트를 올바르게 추가하고, 조합하고, 커스터마이징한다. copy-and-paste 모델의 장점(Full ownership, No version lock-in, Zero runtime overhead)을 살리면서, Critical Rules와 base/radix 분기를 지켜 일관된 코드를 만든다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제로 작업을 시작하기 전에는 아래 reference와 rules 문서를 직접 읽고 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 원칙

### 1. 프로젝트 컨텍스트를 먼저 확인한다

`npx shadcn@latest info --json`으로 aliases, isRSC, tailwindVersion, base, iconLibrary, resolvedPaths를 확인한다. 이 필드들이 이후 모든 판단의 기준이 된다.

#### 빠른 판단 기준

- `base` 필드가 `radix`인가 `base`인가 → asChild vs render 분기
- `tailwindVersion`이 `v3`인가 `v4`인가 → @theme inline vs tailwind.config.js 분기
- `isRSC`가 true인가 → useState/useEffect 사용 시 "use client" 필수
- `iconLibrary` 확인 → lucide-react vs @tabler/icons-react 등
- `aliases` → import alias prefix를 하드코딩하지 않는다
- `tailwindCssFile` → 커스텀 CSS 변수를 정의하는 전역 CSS 파일
- `style` → 컴포넌트 비주얼 스타일 (nova, vega, maia, lyra, mira, luma)
- `framework` → 라우팅, 파일 구조 컨벤션 (Next.js App Router vs Vite SPA 등)
- `packageManager` → shadcn 외 의존성 설치 시 사용하는 패키지 매니저

### 2. 기존 컴포넌트를 먼저 찾는다

- `npx shadcn@latest search`로 registry 검색 (커뮤니티 registry 포함)
- `npx shadcn@latest docs <component>`로 문서/예시 URL 확인 후 fetch
- 커스텀 마크업을 쓰기 전에 항상 기존 컴포넌트가 있는지 확인
- 조합으로 해결: Settings = Tabs + Card + form controls, Dashboard = Sidebar + Card + Chart + Table

### 3. Critical Rules를 지킨다

**스타일링:** className은 layout 전용, semantic colors 사용, gap-* (not space-y-*), size-* (not w-* h-*), truncate, cn(), no manual dark:, no manual z-index

**폼:** FieldGroup + Field, InputGroup + InputGroupInput, ToggleGroup (2-7 options), FieldSet + FieldLegend, data-invalid + aria-invalid

**조합:** Items→Group, Dialog/Sheet/Drawer Title 필수, full Card composition, Button loading = Spinner + data-icon + disabled, 기존 컴포넌트 우선 (Alert, Empty, sonner, Separator, Skeleton, Badge)

**아이콘:** data-icon attribute, no sizing classes inside components, project iconLibrary respect, icons as component objects

#### 빠른 판단 기준

- `space-y-4`가 보이면 → `flex flex-col gap-4`로
- `bg-blue-500`이 보이면 → `bg-primary`로
- `w-10 h-10`이 보이면 → `size-10`으로
- Button에 아이콘이 있으면 → `data-icon="inline-start"` 확인
- DialogContent에 Title이 없으면 → 추가 (sr-only 가능)
- SelectItem이 Group 없이 있으면 → SelectGroup으로 감싸기
- 커스텀 `animate-pulse` div → `Skeleton` 컴포넌트 사용
- 커스텀 styled span → `Badge` 컴포넌트 사용
- `<hr>` 또는 `border-t` div → `Separator` 컴포넌트 사용

실제 적용 전에는 [rules/styling.md](rules/styling.md), [rules/forms.md](rules/forms.md), [rules/composition.md](rules/composition.md), [rules/icons.md](rules/icons.md)를 직접 읽고 Incorrect/Correct 코드 쌍을 확인한다.

### 4. base vs radix 차이를 지킨다

- `base` 필드에 따라 asChild/render, Select props, ToggleGroup type/multiple, Slider 값 형식이 달라진다
- 실제 적용 전에는 [rules/base-vs-radix.md](rules/base-vs-radix.md)를 직접 읽고 분기를 확인한다

### 5. 커스터마이징은 단계적으로 한다

1. Built-in variants 먼저 (`variant="outline"`, `size="sm"` 등)
2. className으로 layout 조정
3. cva로 새 variant 추가
4. Wrapper component로 조합

색상은 OKLCH 포맷으로 CSS variable에 정의하고, Tailwind v4는 @theme inline, v3는 tailwind.config.js에 등록한다.

실제 적용 전에는 [references/customization.md](references/customization.md)를 직접 읽고 color variable 정의와 등록 절차를 확인한다.

---

## Key Patterns

가장 자주 쓰이는 패턴을 보여준다. edge case는 위 rules 파일에서 확인한다.

```tsx
// Form layout: FieldGroup + Field, not div + Label.
<FieldGroup>
  <Field>
    <FieldLabel htmlFor="email">Email</FieldLabel>
    <Input id="email" />
  </Field>
</FieldGroup>

// Validation: data-invalid on Field, aria-invalid on the control.
<Field data-invalid>
  <FieldLabel>Email</FieldLabel>
  <Input aria-invalid />
  <FieldDescription>Invalid email.</FieldDescription>
</Field>

// Icons in buttons: data-icon, no sizing classes.
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// Spacing: gap-*, not space-y-*.
<div className="flex flex-col gap-4">  {/* correct */}
<div className="space-y-4">           {/* wrong */}

// Equal dimensions: size-*, not w-* h-*.
<Avatar className="size-10">   {/* correct */}
<Avatar className="w-10 h-10"> {/* wrong */}

// Status colors: Badge variants or semantic tokens, not raw colors.
<Badge variant="secondary">+20.1%</Badge>    {/* correct */}
<span className="text-emerald-600">+20.1%</span> {/* wrong */}
```

---

## Component Selection

| Need                       | Use                                                                                                 |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Button/action              | `Button` with appropriate variant                                                                   |
| Form inputs                | `Input`, `Select`, `Combobox`, `Switch`, `Checkbox`, `RadioGroup`, `Textarea`, `InputOTP`, `Slider` |
| Toggle between 2–5 options | `ToggleGroup` + `ToggleGroupItem`                                                                   |
| Data display               | `Table`, `Card`, `Badge`, `Avatar`                                                                  |
| Navigation                 | `Sidebar`, `NavigationMenu`, `Breadcrumb`, `Tabs`, `Pagination`                                     |
| Overlays                   | `Dialog` (modal), `Sheet` (side panel), `Drawer` (bottom sheet), `AlertDialog` (confirmation)       |
| Feedback                   | `sonner` (toast), `Alert`, `Progress`, `Skeleton`, `Spinner`                                        |
| Command palette            | `Command` inside `Dialog`                                                                           |
| Charts                     | `Chart` (wraps Recharts)                                                                            |
| Layout                     | `Card`, `Separator`, `Resizable`, `ScrollArea`, `Accordion`, `Collapsible`                          |
| Empty states               | `Empty`                                                                                             |
| Menus                      | `DropdownMenu`, `ContextMenu`, `Menubar`                                                            |
| Tooltips/info              | `Tooltip`, `HoverCard`, `Popover`                                                                   |

---

## Workflow

1. **프로젝트 컨텍스트 확인** — `npx shadcn@latest info --json`. 이미 주입되어 있으면 생략.
2. **설치된 컴포넌트 확인** — `add` 전에 `components` 목록이나 `resolvedPaths.ui` 디렉토리를 본다. 미설치 컴포넌트를 import하지 말고, 이미 설치된 것을 다시 add하지 않는다.
3. **컴포넌트 찾기** — `npx shadcn@latest search`. 커뮤니티 registry도 확인.
4. **문서/예시 확인** — `npx shadcn@latest docs <component>`로 URL을 얻고 fetch한다. `npx shadcn@latest view`로 미설치 registry item 탐색. 설치 컴포넌트 변경 미리보기는 `npx shadcn@latest add --diff`.
5. **설치/업데이트** — `npx shadcn@latest add`. 기존 컴포넌트 업데이트 시 `--dry-run`과 `--diff`로 미리 확인 (아래 Updating Components 참조).
6. **서드파티 import 수정** — 커뮤니티 registry에서 추가한 파일의 하드코딩 import path를 프로젝트 alias로 교체.
7. **추가된 컴포넌트 리뷰** — 추가 후 반드시 파일을 읽고 Critical Rules 위반, 누락된 sub-component, 잘못된 import을 확인. `iconLibrary`에 맞지 않는 아이콘 import도 교체.
8. **Registry는 명시적으로** — 사용자가 registry를 지정하지 않은 채 블록/컴포넌트 추가를 요청하면, 어떤 registry를 쓸지 먼저 확인. 임의로 기본 registry를 정하지 않는다.
9. **Preset 전환** — 사용자에게 overwrite / merge / skip 중 선택을 먼저 묻는다.
   - **Overwrite**: `npx shadcn@latest apply --preset <code>`. 기존 컴포넌트, 폰트, CSS variable 덮어쓰기.
   - **Merge**: `npx shadcn@latest init --preset <code> --force --no-reinstall` 후 설치된 컴포넌트마다 `--dry-run`/`--diff`로 smart merge.
   - **Skip**: `npx shadcn@latest init --preset <code> --force --no-reinstall`. config/CSS만 업데이트, 컴포넌트는 그대로.
   - 항상 프로젝트 디렉토리에서 실행. `apply`는 `components.json`이 있는 기존 프로젝트에서만 작동. CLI는 현재 base를 자동 보존.

## Updating Components

사용자가 upstream 변경을 로컬 수정과 합치려 할 때 `--dry-run`과 `--diff`로 지능적으로 merge한다. **GitHub에서 raw 파일을 직접 fetch하지 말고 항상 CLI를 사용한다.**

1. `npx shadcn@latest add <component> --dry-run` — 영향받는 파일 목록 확인
2. `npx shadcn@latest add <component> --diff <file>` — 파일별 upstream vs local diff 확인
3. 파일별 판단:
   - 로컬 변경 없음 → 안전하게 덮어쓰기
   - 로컬 변경 있음 → 로컬 파일 읽고, diff 분석 후, upstream 변경만 선택 적용
   - 사용자가 "전부 업데이트" → `--overwrite` 사용, 단 반드시 사전 확인
4. **`--overwrite`는 사용자 명시적 승인 없이 절대 사용 금지**

---

## Quick Reference

```bash
# 새 프로젝트 생성
npx shadcn@latest init --name my-app --preset base-nova
npx shadcn@latest init --name my-app --preset a2r6bw --template vite

# 모노레포 프로젝트 생성
npx shadcn@latest init --name my-app --preset base-nova --monorepo

# 기존 프로젝트 초기화
npx shadcn@latest init --preset base-nova
npx shadcn@latest init --defaults

# Preset 적용
npx shadcn@latest apply --preset a2r6bw

# 컴포넌트 추가
npx shadcn@latest add button card dialog
npx shadcn@latest add @magicui/shimmer-button
npx shadcn@latest add --all

# 변경 미리보기
npx shadcn@latest add button --dry-run
npx shadcn@latest add button --diff button.tsx
npx shadcn@latest add @acme/form --view button.tsx

# Registry 검색
npx shadcn@latest search @shadcn -q "sidebar"
npx shadcn@latest search @tailark -q "stats"

# 컴포넌트 문서/예시 URL
npx shadcn@latest docs button dialog select

# Registry item 보기 (미설치)
npx shadcn@latest view @shadcn/button
```

**Named presets:** `nova`, `vega`, `maia`, `lyra`, `mira`, `luma`
**Templates:** `next`, `vite`, `start`, `react-router`, `astro` (all support `--monorepo`) and `laravel` (not for monorepo)
**Preset codes:** Version-prefixed base62 strings (e.g. `a2r6bw`), from [ui.shadcn.com](https://ui.shadcn.com)

---

## references/ 가이드

| 파일 | 언제 읽는가 |
|------|-----------|
| [references/cli.md](references/cli.md) | CLI 명령, 플래그, dry-run, preset, template 확인할 때 |
| [references/mcp.md](references/mcp.md) | MCP 서버 설정, registry tool 사용할 때 |
| [references/customization.md](references/customization.md) | 테마 변경, custom color 추가, dark mode, border radius 설정할 때 |
| [references/component-catalog.md](references/component-catalog.md) | 사용 가능한 컴포넌트 일람, props, dependencies 확인할 때 |
| [references/setup-guide.md](references/setup-guide.md) | 새 프로젝트 셋업, 기존 프로젝트 초기화할 때 |
| [references/migration-guide.md](references/migration-guide.md) | MUI/Chakra/Ant Design에서 마이그레이션할 때 |
| [references/troubleshooting.md](references/troubleshooting.md) | import error, style conflict, missing dependency 해결할 때 |
| [references/validation.md](references/validation.md) | 배포 전 품질 체크리스트 (tsc, lint, a11y, visual QA) |

## rules/ 가이드

| 파일 | 언제 읽는가 |
|------|-----------|
| [rules/styling.md](rules/styling.md) | 스타일링 코드 작성/리뷰할 때 — Incorrect/Correct 쌍 |
| [rules/forms.md](rules/forms.md) | 폼 레이아웃, 입력, 검증 코드 작성할 때 |
| [rules/composition.md](rules/composition.md) | 컴포넌트 조합, overlay, Card, Table, 로딩 상태 작성할 때 |
| [rules/icons.md](rules/icons.md) | 아이콘 사용, data-icon, iconLibrary 확인할 때 |
| [rules/base-vs-radix.md](rules/base-vs-radix.md) | Radix/Base UI API 차이 확인할 때 |

## examples/ 가이드

폼, 데이터 테이블, 인증 레이아웃 같은 실전 패턴을 전체 코드로 보여준다. 비슷한 화면을 만들 때 구조와 컴포넌트 조합을 먼저 참고하고, 프로젝트 컨텍스트에 맞게 수정한다.

| 파일 | 무엇을 보여주는가 |
|------|-----------------|
| [examples/form-pattern.md](examples/form-pattern.md) | react-hook-form + zod + shadcn Form 조합 전체 흐름. zodResolver로 스키마 검증, FormField/FormItem/FormLabel/FormMessage로 필드 구성, Select/Textarea 포함 복합 폼, 타입 추론(z.infer), onSubmit + toast 피드백까지 한 파일에서 확인 |
| [examples/data-table.md](examples/data-table.md) | TanStack Table(@tanstack/react-table) + shadcn Table 통합 패턴. ColumnDef 정의, 헤더 클릭 정렬, 텍스트 필터링, DropdownMenuCheckboxItem으로 컬럼 토글, 행별 DropdownMenu 액션, Previous/Next 페이지네이션, 선택 행 카운트 표시 |
| [examples/auth-layout.md](examples/auth-layout.md) | Card + Tabs로 로그인/회원가입 전환 레이아웃. TabsList grid 2단 구성, CardHeader/CardContent/CardFooter 분리, Label+Input 폼 구조, Button disabled+텍스트 전환으로 로딩 상태 처리, min-h-screen 중앙 정렬 반응형 |

---

## 범위

### 이 스킬이 담당하는 영역

- shadcn/ui 컴포넌트 추가, 설정, 커스터마이징
- components.json 구성, presets, registries
- CLI 명령 (init, apply, add, search, docs, info, view, build)
- MCP 서버 tools (get_project_registries, list/search/view_items, get_add_command, get_audit_checklist)
- cn(), cva utility (shadcn/ui 컨텍스트)
- FieldGroup/Field 폼 레이아웃, data-icon, composition rules
- base vs radix API 분기
- 다른 UI 라이브러리에서 shadcn/ui로 마이그레이션
- 컴포넌트 업데이트 (smart merge with --diff)
- Blocks (authentication, dashboards, sidebars)

### 다른 스킬로 위임

- **fe-tailwindcss**: Tailwind CSS v4 설정, @theme/@utility, responsive/dark mode 일반 패턴. 커스터마이징 시 함께 참조
- **fe-ui-element-components**: 공유 UI primitive 설계, design token, data-state/data-slot 계약. shadcn 컴포넌트를 design system으로 확장할 때
- **fe-a11y**: 접근성 원칙, semantic HTML, keyboard, ARIA, focus. shadcn 컴포넌트 커스터마이징 시
- **fe-react-patterns**: React component architecture, composition, state ownership. shadcn 컴포넌트를 조합해서 화면을 만들 때
