---
name: dev-vite
description: "Vite build tool patterns for vite.config.ts, dev server setup, import.meta features, asset queries, env handling, plugin authoring boundaries, library mode, low-level SSR APIs, and Vite 8 Rolldown/Oxc migration. Use this skill when working with Vite projects, vite.config.ts, Vite plugins, build scripts, dev server behavior, library builds, or framework and tooling integrations built on Vite. Always consult this skill for Vite-specific configuration or migration work, even if the user only asks to fix aliases, env loading, HMR, asset imports, plugin hooks, or update Rollup-era config to Rolldown. For low-level plugin and SSR API details read the bundled references. Triggers on: Vite, vite.config.ts, defineConfig, import.meta.glob, loadEnv, plugin API, virtual module, Rolldown, Oxc, library mode, SSR middleware, vite preview, vite build, Vite migration, Vite plugin, vite 설정, 번들러, 개발 서버."
disable-model-invocation: false
user-invocable: false
---

# Vite 빌드/개발 패턴

## 목표

Vite 프로젝트에서 설정, dev server, build, library mode, low-level SSR, plugin authoring, 그리고 Vite 8 migration을 한 흐름으로 판단하게 만든다. 핵심은 Vite 고유 기능을 먼저 쓰고, plugin이나 low-level SSR은 정말 필요한 경우에만 여는 것이다.

이 문서는 빠른 판단을 위한 요약 가이드다. config와 feature 계열은 본문에서 바로 판단하고, plugin authoring이나 low-level build and SSR 세부는 아래 reference를 읽고 적용한다.

이 스킬은 Vite 8 기준 내용을 우선 다루지만, 실제 적용 전에는 프로젝트가 정말 Vite 8을 쓰는지, 아니면 Vite 6/7 계열인지 먼저 확인한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## Quick Reference

- 기본 CLI는 `vite`, `vite build`, `vite preview`, `vite build --ssr` 네 축으로 보면 된다.
- React, Vue, Vue JSX, legacy browser 대응은 공식 plugin을 우선 검토한다. 예: `@vitejs/plugin-react`, `@vitejs/plugin-react-swc`, `@vitejs/plugin-vue`, `@vitejs/plugin-vue-jsx`, `@vitejs/plugin-legacy`.
- alias, define, proxy, loadEnv, import.meta, asset query, HMR, env exposure, Vite 8 migration이 핵심이면 이 SKILL.md부터 읽는다.
- custom plugin, virtual module, transformIndexHtml, custom HMR event, plugin ordering이 핵심이면 [references/plugin-api.md](references/plugin-api.md)를 바로 읽는다.
- library mode, multi-page build, createServer/build/preview/resolveConfig/loadEnv JavaScript API, low-level SSR, environment API가 핵심이면 [references/build-and-ssr.md](references/build-and-ssr.md)를 읽는다.

---

## 핵심 패턴

### 1. 먼저 Vite 버전과 기준 구성을 확인한다

Vite 설정은 버전에 따라 이름이 달라진다. Vite 8에서는 Rolldown과 Oxc가 기본이지만, 프로젝트가 아직 Vite 6 또는 7이면 `rolldownOptions`나 `oxc`를 바로 쓰면 안 된다.

- 기본 설정 파일은 `vite.config.ts`를 우선한다.
- ESM을 기본으로 보고 CommonJS 설정은 새로 늘리지 않는다.
- `defineConfig()`를 기본으로 쓰고, `command`나 `mode`에 따라 갈리면 함수 형태로 export 한다.
- async config가 필요하면 `defineConfig(async ({ command, mode }) => ...)` 형태도 가능하다.
- `.env`는 config 해석 뒤에 로드되므로 config 안에서는 `loadEnv()`로 읽는다.
- JS config를 유지해야 하면 JSDoc 타입 또는 `satisfies UserConfig`로 타입 힌트를 보강한다.

#### 빠른 판단 기준

- 프로젝트의 실제 Vite major version을 아직 확인하지 않았다면 migration 판단을 미룬다.
- 기존 프로젝트 config에 `rollupOptions`나 `esbuild`가 보이면, 실제 Vite 8 migration인지 먼저 확인하기 전에는 섣불리 바꾸지 않는다.
- `vite.config.js`가 복잡해지고 타입 힌트가 약하면 `vite.config.ts` 전환을 먼저 검토한다.
- config에서 env가 필요한데 `process.env`를 바로 읽고 있으면 `loadEnv()` 사용 여부를 먼저 본다.

### 2. config는 alias, define, proxy, build target 중심으로 단순하게 유지한다

많은 Vite 설정은 몇 가지 shared option 안에서 정리된다. alias, define, dev proxy, build target, plugin 배열을 먼저 정돈하고, 그다음에 plugin이나 custom transform이 정말 필요한지 본다.

- `resolve.alias`는 import path 안정화용으로만 쓴다.
- `define`에는 JSON-serializable value나 single identifier만 넣는다.
- `server.proxy`는 dev proxy 용도에만 쓰고, production reverse proxy 요구사항과 혼동하지 않는다.
- `build.target`은 실제 브라우저 대상에 맞춘다. 불필요하게 `esnext`를 기본값처럼 쓰지 않는다.
- framework plugin은 공식 plugin을 우선한다. 예: `@vitejs/plugin-react`, `@vitejs/plugin-react-swc`, `@vitejs/plugin-vue`, `@vitejs/plugin-vue-jsx`, `@vitejs/plugin-legacy`.

```ts
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '')

	return {
		resolve: {
			alias: {
				'@': '/src',
			},
		},
		define: {
			__APP_ENV__: JSON.stringify(env.APP_ENV),
		},
		server: {
			port: env.APP_PORT ? Number(env.APP_PORT) : 5173,
			proxy: {
				'/api': 'http://localhost:8080',
			},
		},
		build: {
			target: 'es2020',
		},
	}
})
```

#### 빠른 판단 기준

- `command === 'serve'`와 `command === 'build'` 분기가 있으면 함수형 config가 더 자연스럽다.
- dev 서버에서만 필요한 proxy를 build config에 억지로 섞고 있으면 분리 대상이다.
- `define`에 runtime object를 통째로 넣으려 하면 설계가 잘못된 신호로 본다.

### 3. custom plugin보다 Vite-native feature를 먼저 쓴다

많은 작업은 plugin 없이 해결된다. `import.meta.glob`, asset query, `import.meta.env`, CSS Modules, JSON import, HMR API를 먼저 쓰는 편이 더 단순하고 유지보수에 유리하다.

- 여러 파일을 불러올 때는 `import.meta.glob()`을 우선 검토한다. eager loading, named import, multiple pattern, negative pattern, custom query까지 기본 기능 안에서 해결 가능하다.
- asset import는 `?raw`, `?url`, `?inline`, `?no-inline`로 처리한다.
- worker는 `?worker` import보다 `new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' })` 패턴을 우선한다.
- client에 노출할 env는 `VITE_` prefix만 사용한다. built-in constant는 `MODE`, `BASE_URL`, `PROD`, `DEV`, `SSR`이다.
- env file 우선순위는 `.env`, `.env.local`, `.env.[mode]`, `.env.[mode].local` 순으로 본다.
- HTML 안에서 `%MODE%`, `%VITE_*%` 치환도 가능하다.
- `.module.css`는 기본 CSS Module로 보고, PostCSS 설정은 보통 자동 인식된다. Sass 같은 pre-processor도 패키지 설치만으로 연결되는 경우가 많다.
- JSON은 named import까지 활용 가능하다.
- HMR은 `import.meta.hot.accept`, `dispose`, `invalidate`까지 기본 API 안에서 해결할 수 있다.

#### 빠른 판단 기준

- 파일 탐색이나 route-like registration 때문에 plugin을 만들려 하면 `import.meta.glob()`으로 충분한지 먼저 본다.
- client code에서 `process.env.*`를 읽고 있으면 `import.meta.env` 체계로 돌리는 것이 우선이다.
- asset를 string, URL, worker 중 무엇으로 써야 하는지 모호하면 query 방식으로 해결 가능한지 먼저 본다.
- env를 client에 노출해야 하는데 prefix가 없다면 일단 설계를 다시 본다.
- module update cleanup이 필요한데 full reload만 쓰고 있으면 `dispose`나 custom HMR event가 맞는지 확인한다.

### 4. 앱 SSR은 framework에 맡기고, low-level SSR과 JavaScript API는 도구 작업에 한정한다

Vite 자체 SSR API는 meta-framework를 만드는 쪽에 더 가깝다. 일반 애플리케이션 SSR은 Nuxt, SvelteKit, SolidStart, TanStack Start 같은 Vite 기반 framework가 더 적합하다. 반면 library build, multi-page build, dev server embedding, custom tooling은 Vite의 low-level API가 잘 맞는다.

- 배포용 라이브러리는 `build.lib`와 external/globals 구성을 함께 본다.
- single entry library는 보통 `es`와 `umd`, multiple entry는 `es`와 `cjs` 조합을 본다.
- 배포 패키지면 `package.json`의 `main`, `module`, `exports`, `files`까지 함께 정렬한다.
- multi-page app은 `build.rolldownOptions.input` 또는 현재 프로젝트 버전에 맞는 입력 설정으로 나눈다.
- custom dev tooling이 필요하면 `createServer()`, `build()`, `preview()`, `resolveConfig()`, `loadEnv()`를 직접 쓸 수 있다.
- multiple runtime environment나 custom environment는 plugin 또는 framework author 수준의 고급 주제다.

#### 빠른 판단 기준

- 일반 앱 SSR만 필요하다면 low-level SSR wiring보다 framework 도입을 우선 검토한다.
- 패키지 배포라면 library mode와 `package.json` export 정렬까지 같이 본다.
- dev server를 다른 Node 서버에 임베드해야 하면 JavaScript API reference를 바로 읽는다.

→ 상세: [references/build-and-ssr.md](references/build-and-ssr.md)

### 5. plugin은 config로 안 풀리는 경우에만 만들고, hook 경계를 명확히 둔다

Vite plugin은 Rolldown plugin 위에 Vite-specific hook이 추가된 형태다. `config`, `configResolved`, `configureServer`, `transformIndexHtml`, `handleHotUpdate`가 핵심이고, virtual module과 HMR custom event까지 여기서 처리한다.

- config 수정은 `config`, 최종 resolved config 참조는 `configResolved`를 쓴다.
- dev server middleware는 `configureServer`에서 추가한다.
- HTML entry 조작은 `transformIndexHtml`로 처리한다.
- custom HMR 동작은 `handleHotUpdate`와 websocket event를 함께 쓴다.
- virtual module은 user-facing id를 `virtual:*`, 내부 resolved id를 `\0virtual:*` convention으로 둔다.
- plugin ordering은 `enforce`, 적용 조건은 `apply`로 명시한다.

#### 빠른 판단 기준

- 설정 변경만 필요하면 full plugin보다 config function이 더 단순한지 먼저 본다.
- 파일이 없는 가상 import를 제공해야 하면 virtual module이 맞는 신호다.
- build에서만 필요한 plugin인데 dev에서도 돌고 있으면 `apply: 'build'`를 먼저 검토한다.

→ 상세: [references/plugin-api.md](references/plugin-api.md)

### 6. Vite 8 migration은 Rolldown과 Oxc 경계부터 정리한다

Vite 8에서는 production build와 dependency pre-bundling 축이 Rolldown 중심으로 정리되고, transform 설정도 `esbuild`에서 `oxc`로 이동한다. migration은 설정 이름 바꾸기만이 아니라, 현재 프로젝트와 framework가 정말 Vite 8을 받는지부터 확인해야 한다.

- `build.rollupOptions`는 Vite 8에서 `build.rolldownOptions`로 옮긴다.
- `esbuild` 관련 JSX 설정은 `oxc.jsx`와 `oxc.jsxInject` 쪽으로 옮긴다. 필요하면 `runtime`, `importSource`, `pragma`, `pragmaFrag`까지 함께 옮긴다.
- 대부분의 Vite plugin은 그대로 동작하지만, build-only plugin이면 `apply: 'build'`와 `enforce: 'post'` 조합이 필요한지 확인한다.
- Vite 8은 Rollup 대비 production build가 크게 빨라질 수 있지만, framework와 plugin compatibility를 먼저 확인한다.
- 대형 프로젝트는 `rolldown-vite`로 선행 검증 후 Vite 8로 올리는 gradual migration 경로도 가능하다.
- framework가 구버전 Vite를 pin하고 있으면 override는 신중하게 적용한다.
- Environment API는 end-user app보다는 plugin/framework author에게 더 relevant하다.

```ts
export default defineConfig({
	build: {
		rolldownOptions: {
			external: ['vue'],
		},
	},
	oxc: {
		jsx: {
			runtime: 'automatic',
			importSource: 'react',
		},
	},
})
```

#### 빠른 판단 기준

- config에 `rollupOptions`나 `esbuild`가 보이면 현재 Vite version과 migration 대상인지 먼저 확인한다.
- framework dependency가 아직 old Vite면 바로 major upgrade를 밀지 않는다.
- advanced runtime 환경을 직접 정의하려 하면 보통 app code가 아니라 tooling/framework work에 가깝다.
- plugin이 build에서만 의미가 있는데도 serve와 build를 모두 건드리면 apply 범위를 재검토한다.

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/plugin-api.md](references/plugin-api.md) | custom plugin, virtual module, transformIndexHtml, custom HMR event, plugin ordering을 구현하거나 리뷰할 때 |
| [references/build-and-ssr.md](references/build-and-ssr.md) | library mode, multi-page build, JavaScript API, low-level SSR, advanced environment 구성을 다룰 때 |

### 추천 로드 순서

- 기본 설정 또는 migration: 이 SKILL.md -> 필요한 경우 references/build-and-ssr.md
- plugin authoring: 이 SKILL.md -> references/plugin-api.md
- embedded dev server 또는 low-level SSR: 이 SKILL.md -> references/build-and-ssr.md

---

## 범위

- React, Vue, Svelte 컴포넌트 구조 자체는 각 frontend skill이 담당한다.
- low-level Vite SSR 위에서 실제 framework architecture를 설계하는 일은 이 스킬의 기본 범위를 넘는다.
- generic bundler theory보다 Vite-specific 설정과 migration 판단에 집중한다.