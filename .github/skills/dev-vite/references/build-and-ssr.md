---
name: dev-vite-build-ssr
description: Detailed Vite library mode, JavaScript API, low-level SSR, and environment API guidance.
---

# Vite Build and SSR

이 문서는 library mode, multi-page build, JavaScript API, low-level SSR, 그리고 advanced environment 구성을 다룰 때 읽는 reference다.

## Library Mode

```ts
import { resolve } from 'node:path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: resolve(import.meta.dirname, 'lib/main.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
    },
    rolldownOptions: {
      external: ['vue', 'react'],
      output: {
        globals: {
          vue: 'Vue',
          react: 'React',
        },
      },
    },
  },
})
```

- single entry는 보통 `es`와 `umd`, multiple entry는 `es`와 `cjs` 조합을 본다.
- 외부 peer dependency는 `external`로 분리하고, UMD global 이름까지 같이 맞춘다.
- 배포 패키지면 `package.json`의 `main`, `module`, `exports`, `files`까지 함께 정렬한다.

예시:

```json
{
  "name": "my-lib",
  "type": "module",
  "files": ["dist"],
  "main": "./dist/my-lib.umd.cjs",
  "module": "./dist/my-lib.js",
  "exports": {
    ".": {
      "import": "./dist/my-lib.js",
      "require": "./dist/my-lib.umd.cjs"
    },
    "./style.css": "./dist/my-lib.css"
  }
}
```

multiple entry 예시:

```ts
lib: {
  entry: {
    'my-lib': resolve(import.meta.dirname, 'lib/main.ts'),
    secondary: resolve(import.meta.dirname, 'lib/secondary.ts'),
  },
  name: 'MyLib',
}
```

## Multi-Page Build

```ts
export default defineConfig({
  build: {
    rolldownOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        nested: resolve(import.meta.dirname, 'nested/index.html'),
      },
    },
  },
})
```

app entry가 여러 개면 multi-page build로 푸는 것이 먼저다. custom HTML rewriting이나 서버 routing을 과하게 먼저 늘리지 않는다.

## Low-level SSR

Vite의 SSR API는 application team보다 meta-framework나 tooling author에 더 맞다.

- 일반 제품 SSR이면 Nuxt, SvelteKit, SolidStart, TanStack Start 같은 Vite 기반 framework를 우선 본다.
- framework-agnostic server layer가 필요하면 Nitro 같은 server runtime을 검토할 수 있다.
- 직접 wiring이 필요한 경우에만 Vite SSR primitive를 연다.

Nitro는 file-based API routing, auto-import, deployment preset을 묶어 제공하는 server runtime으로, low-level SSR을 전부 직접 짜고 싶지 않을 때 현실적인 대안이다.

## JavaScript API

### `createServer`

```ts
import { createServer } from 'vite'

const server = await createServer({
  configFile: false,
  root: import.meta.dirname,
  server: { port: 1337 },
})

await server.listen()
server.printUrls()
```

### `build`

```ts
import { build } from 'vite'

await build({
  root: './project',
  build: { outDir: 'dist' },
})
```

### `preview`

```ts
import { preview } from 'vite'

const previewServer = await preview({
  preview: { port: 8080, open: true },
})
previewServer.printUrls()
```

### `resolveConfig`

```ts
import { resolveConfig } from 'vite'

const config = await resolveConfig({}, 'build')
```

### `loadEnv`

```ts
import { loadEnv } from 'vite'

const env = loadEnv('development', process.cwd(), '')
```

## Environment API

Vite 6+에서는 `client`와 `ssr`만 암묵적으로 보는 대신 여러 runtime environment를 명시적으로 정의할 수 있다.

```ts
export default defineConfig({
  build: { sourcemap: false },
  optimizeDeps: { include: ['lib'] },
  environments: {
    server: {},
    edge: {
      resolve: { noExternal: true },
    },
  },
})
```

- top-level config는 environment에 상속된다.
- `optimizeDeps`처럼 client-only로 해석되는 옵션이 있으니 모든 environment에 똑같이 적용된다고 가정하지 않는다.
- end-user app은 대체로 framework가 처리하므로 직접 만질 일이 적다.
- plugin/framework author는 transform이나 runtime provider 차원에서 environment-aware behavior를 볼 수 있다.

custom environment provider 예시:

```ts
import { customEnvironment } from 'vite-environment-provider'

export default defineConfig({
  environments: {
    ssr: customEnvironment({
      build: { outDir: '/dist/ssr' },
    }),
  },
})
```

hook 쪽에서는 `options?.ssr`처럼 environment signal을 읽어 분기할 수 있다.

backward compatibility도 같이 기억한다.

- `server.moduleGraph`는 mixed client/SSR view를 반환할 수 있다.
- `ssrLoadModule`은 계속 동작한다.
- 기존 SSR 앱 다수가 큰 수정 없이 유지될 수 있다.

## 빠른 판단 기준

- 앱 SSR만 필요하면 low-level SSR API부터 열지 않는다.
- 라이브러리 배포면 bundle output뿐 아니라 package export shape까지 같이 본다.
- 여러 runtime을 동시에 지원해야 하면 Environment API가 실제 요구사항인지, 아니면 framework가 이미 해결하는지 먼저 확인한다.