---
name: dev-turbopack
description: Turbopack patterns for Next.js bundler configuration, webpack migration, CSS and asset parity, bundle analysis, HMR tracing, build diagnostics, and opt-out decisions. Use this skill when working in a Next.js app with turbopack config, next dev --turbopack, loader migration, build failures, HMR performance, or webpack to Turbopack migration. Always consult this skill for Turbopack changes even if the user only asks to fix a Next.js bundler error, migrate experimental.turbopack, replace webpack loaders, or profile slow dev and build cycles. For app-router or component architecture concerns use the relevant frontend skill. Triggers on: Turbopack, next dev --turbopack, next dev --turbo, next.config.ts turbopack, experimental.turbopack, webpack migration, resolveAlias, turbopack.rules, bundleAnalyzer, HMR tracing, server-only, 번들러, 터보팩, 웹팩 마이그레이션.
disable-model-invocation: false
user-invocable: false
---

# Turbopack 번들러 패턴

## 목표

Next.js에서 Turbopack을 쓸 때 config migration, CSS와 asset 처리, webpack customization 대체, bundle analysis, build and dev diagnostics를 빠르게 판단하게 만든다. 핵심은 Turbopack의 built-in path를 먼저 쓰고, webpack-era custom loader와 plugin 의존성은 parity 여부를 확인한 뒤 옮기거나 opt out 하는 것이다.

이 문서는 빠른 판단을 위한 요약 가이드다. Turbopack은 Next.js 16 기준으로 보는 것이 기본이므로, 프로젝트가 실제로 어떤 Next.js major를 쓰는지 먼저 확인하고 적용한다.

기본 특성도 기억한다. Turbopack은 instant HMR, Next.js 16.1+의 stable file system cache, browser/server/edge/SSR/RSC multi-environment build, 그리고 TypeScript/JSX/CSS/CSS Modules/WebAssembly 기본 지원을 제공한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 검토 시작점

- `next.config.*`에서 `experimental.turbopack`, top-level `turbopack`, `webpack()` override, `bundler` 설정을 먼저 본다.
- `postcss.config.*`, Sass 사용 여부, CSS-in-JS compiler 설정 여부를 같이 본다.
- `package.json`의 `sideEffects` 선언과 analyzer 관련 스크립트를 같이 본다.
- client component의 `"use client"` 경계와 server-only import를 같이 본다.

---

## 핵심 패턴

### 1. Next.js 16 기준으로 top-level `turbopack` 설정부터 맞춘다

Turbopack은 Next.js 16에서 기본 번들러다. config는 `experimental.turbopack`가 아니라 top-level `turbopack`로 두고, webpack 시절 custom override는 그대로 남겨 두지 않는다.

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  turbopack: {
    resolveAlias: {
      'old-package': 'new-package',
    },
    resolveExtensions: ['.ts', '.tsx', '.js', '.jsx', '.json'],
  },
}

export default nextConfig
```

- alias는 `turbopack.resolveAlias`로 옮긴다.
- custom resolution 확장은 `turbopack.resolveExtensions`에서 다룬다.
- `webpack()` function이 남아 있으면 Turbopack migration이 반쯤 멈춘 상태일 가능성이 높다.

#### 빠른 판단 기준

- `experimental.turbopack`가 보이면 top-level 이동 대상이다.
- `webpack()` override가 남아 있으면 실제로 아직 webpack path에 묶인 요구사항이 무엇인지 먼저 분리한다.
- Turbopack과 webpack을 비교 중이면 `bundler: 'webpack'` opt-out path가 이미 쓰이고 있는지 확인한다.

### 2. CSS, asset, Sass, PostCSS는 built-in path를 우선한다

Turbopack은 CSS, CSS Modules, PostCSS, Sass를 기본 지원한다. webpack loader 조합을 그대로 재현하려 하기보다 built-in pipeline으로 단순화하는 편이 맞다.

- global CSS는 root layout에서 import 한다.
- `.module.css`와 `.module.scss`는 기본 지원으로 본다.
- `postcss.config.js`는 자동으로 읽힌다.
- Tailwind CSS v4는 별도 loader 없이 PostCSS 경로로 연결한다.
- CSS-in-JS는 `styled-components`, `emotion` 같은 SWC/compiler 설정이 필요한지 별도로 본다.

주의할 점도 함께 본다.

- CSS chunk ordering은 webpack과 다를 수 있으므로 source order specificity에 기대지 않는다.
- global CSS의 `@import`는 circular import가 생기지 않게 본다.
- asset 처리 대부분은 built-in이지만 library-specific transform은 별도 규칙이 필요한지 본다.

#### 빠른 판단 기준

- CSS 때문에 loader를 바로 추가하려 하면 built-in path로 충분한지 먼저 본다.
- migration 후 시각 회귀가 생기면 CSS ordering 차이를 우선 의심한다.
- Sass만 필요하면 loader가 아니라 `sass` 패키지 설치 여부를 먼저 본다.

### 3. webpack customization은 parity table로 하나씩 옮긴다

Turbopack은 webpack loader를 직접 실행하지 않는다. 그래서 migration은 webpack config를 보존하는 작업이 아니라, 각 loader 요구사항을 built-in feature, `turbopack.rules`, native syntax, 또는 webpack opt-out 중 어디로 보낼지 결정하는 작업이다.

| Webpack pattern | Turbopack path |
| --- | --- |
| `css-loader` + `style-loader` | built-in CSS support |
| `sass-loader` | built-in Sass + `sass` package |
| `postcss-loader` | built-in PostCSS config loading |
| `file-loader`, `url-loader` | built-in static asset handling |
| `@svgr/webpack` | `turbopack.rules`로 연결 |
| `raw-loader` | `?raw` import |
| `worker-loader` | `new Worker(new URL(...))` |
| `graphql-tag/loader` | build-time codegen 쪽 검토 |

SVG처럼 built-in이 아닌 경우는 `turbopack.rules`로 옮긴다.

```ts
const nextConfig: NextConfig = {
  turbopack: {
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },
}
```

parity가 없고 workaround도 없으면 webpack으로 opt out 하는 것이 맞다.

```ts
const nextConfig: NextConfig = {
  bundler: 'webpack',
}
```

#### 빠른 판단 기준

- webpack loader 이름이 보이면 built-in, `turbopack.rules`, native syntax, opt-out 네 갈래로 먼저 분류한다.
- custom plugin이나 Module Federation처럼 webpack-specific 요구가 강하면 빠르게 opt-out 가능성을 검토한다.
- loader migration이 안 되는 상태에서 `webpack()`만 지우는 식의 반쪽 migration은 피한다.

### 4. tree shaking, bundle size, client boundary를 함께 본다

Turbopack은 module-level tree shaking을 하므로 package export shape와 client boundary가 bundle 크기에 직접 영향을 준다.

- named export를 우선하고 무분별한 `export *`는 줄인다.
- side-effect가 없는 package는 `package.json`에 `"sideEffects": false`를 명시한다.
- dynamic import는 async chunk boundary로 활용할 수 있다.
- `"use client"` 경계를 과하게 넓히면 chunk가 커진다.
- server-only 코드는 `server-only` 패키지로 client import를 강제 차단할 수 있다.

bundle analyzer는 현재 Next.js 버전에 맞춰 쓴다.

- Next.js 16.1+에서는 `experimental.bundleAnalyzer`를 우선 검토한다.
- fallback으로 `@next/bundle-analyzer`를 쓸 수 있다.

#### 빠른 판단 기준

- build output이 크면 `"use client"` 경계와 accidentally bundled server package부터 본다.
- barrel file이 많고 `sideEffects` 선언이 없으면 tree shaking 이득이 줄어든다.
- analyzer가 필요하면 먼저 현재 Next.js 버전에서 built-in path가 가능한지 확인한다.

### 5. build failure와 module boundary error는 config보다 import graph를 먼저 본다

Turbopack 오류는 config syntax보다 import boundary나 unsupported customization에서 자주 나온다.

- build 실패 시 `webpack()` override 잔재, 잘못된 `turbopack.rules`, 누락된 loader package부터 확인한다.
- client나 edge bundle에서 `fs`, `path` 같은 Node built-in import는 바로 실패 원인이 된다.
- module not found가 나면 예전 webpack alias가 `resolveAlias`로 제대로 옮겨졌는지 본다.
- CSS ordering regression은 visual bug로 나타날 수 있으니 build success만 보고 끝내지 않는다.

webpack과의 차이를 비교할 때는 둘 다 돌려서 `.next/` 결과와 page chunk를 비교한다.

```bash
next build
BUNDLER=webpack next build
```

#### 빠른 판단 기준

- build error가 생기면 unsupported webpack customization이 숨어 있는지 먼저 본다.
- edge/client error인데 Node built-in import가 보이면 boundary issue를 우선 본다.
- migration 뒤 레이아웃이 깨졌다면 CSS ordering 차이를 먼저 점검한다.

### 6. tracing, memory, concurrency로 dev and build 문제를 계측한다

성능 문제는 감으로 해결하지 않는다. tracing과 analyzer를 켠 뒤 long transform, large module graph, cache miss, memory pressure를 확인한다.

- dev HMR tracing: `NEXT_TURBOPACK_TRACING=1 next dev`
- build tracing: `NEXT_TURBOPACK_TRACING=1 next build`
- trace는 `trace.json`으로 남기고 Chrome tracing 또는 Perfetto에서 본다.
- long-running transform은 heavy PostCSS config나 plugin cost를 의심한다.
- large module graph는 barrel re-export와 wide client boundary를 의심한다.
- cache miss가 많으면 build마다 바뀌는 generated file이나 timestamp를 의심한다.
- OOM이면 `NODE_OPTIONS='--max-old-space-size=8192'`나 Turborepo concurrency 조정을 검토한다.

Turbopack은 development뿐 아니라 production build도 담당할 수 있다. 다만 parity가 없는 loader나 plugin 요구가 강하면 webpack fallback이 더 현실적일 수 있다.

development와 production 둘 다 Turbopack이 맡을 수 있지만, 아래 조건이면 webpack이 더 현실적일 수 있다.

- parity 없는 custom loader
- complex webpack plugin chain
- `externals` function 같은 webpack-specific feature

#### 빠른 판단 기준

- HMR이 느리면 trace부터 켜고 module graph와 transform cost를 본다.
- build가 OOM이면 Node heap과 concurrency부터 줄여 본다.
- 요구사항이 Turbopack parity 밖이면 억지 migration보다 webpack 유지가 더 낫다.

---

## 범위

- 이 스킬은 Next.js의 bundler layer에 집중한다.
- App Router 설계, React component 구조, 상태 관리, CSS utility 설계 자체는 다른 frontend skill이 맡는다.
- Turborepo 파이프라인 전반보다 Turbopack migration과 diagnostics가 주 관심사다.