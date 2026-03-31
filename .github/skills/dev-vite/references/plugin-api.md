---
name: dev-vite-plugin-api
description: Detailed Vite plugin authoring patterns, hooks, virtual modules, and custom HMR messaging.
---

# Vite Plugin API

이 문서는 custom plugin을 실제로 작성하거나 리뷰할 때 읽는 상세 reference다. Vite-specific hook과 plugin ordering, virtual module, custom HMR 통신만 남기고 불필요한 설명은 덜어낸다.

## 기본 구조

```ts
import type { Plugin, ResolvedConfig } from 'vite'

function myPlugin(): Plugin {
  return {
    name: 'my-plugin',
  }
}
```

## 핵심 hook

### `config`

resolved 전 config를 보정할 때 쓴다.

```ts
const plugin = () => ({
  name: 'add-alias',
  config: () => ({
    resolve: {
      alias: { foo: 'bar' },
    },
  }),
})
```

### `configResolved`

최종 config를 읽고 이후 hook에서 재사용할 때 쓴다.

```ts
const plugin = () => {
  let config: ResolvedConfig

  return {
    name: 'read-config',
    configResolved(resolvedConfig) {
      config = resolvedConfig
    },
    transform(code: string, id: string) {
      if (config.command === 'serve') {
        return code
      }
    },
  }
}
```

### `configureServer`

dev server middleware나 websocket wiring이 필요할 때 쓴다. 후처리 middleware가 필요하면 cleanup function처럼 return function을 쓴다.

```ts
const plugin = () => ({
  name: 'custom-middleware',
  configureServer(server) {
    server.middlewares.use((req, res, next) => {
      next()
    })

    return () => {
      server.middlewares.use((req, res, next) => {
        next()
      })
    }
  },
})
```

### `transformIndexHtml`

HTML entry를 치환하거나 tag를 inject할 때 쓴다.

```ts
transformIndexHtml() {
  return [
    {
      tag: 'script',
      attrs: { src: '/inject.js' },
      injectTo: 'body',
    },
  ]
}
```

### `handleHotUpdate`

기본 HMR 외 custom event나 full invalidation 제어가 필요할 때 쓴다.

```ts
handleHotUpdate({ server }) {
  server.ws.send({ type: 'custom', event: 'special-update', data: {} })
  return []
}
```

빈 배열을 반환하면 default HMR을 skip한다.

## Virtual Module

디스크에 없는 module을 import surface로 노출할 때는 `virtual:`와 `\0` prefix convention을 쓴다.

```ts
const plugin = () => {
  const virtualModuleId = 'virtual:my-module'
  const resolvedId = '\0' + virtualModuleId

  return {
    name: 'virtual-module',
    resolveId(id: string) {
      if (id === virtualModuleId) {
        return resolvedId
      }
    },
    load(id: string) {
      if (id === resolvedId) {
        return 'export const msg = "from virtual module"'
      }
    },
  }
}
```

## Plugin Ordering 과 적용 범위

```ts
{
  name: 'pre-plugin',
  enforce: 'pre',
}

{
  name: 'post-plugin',
  enforce: 'post',
  apply: 'build',
}
```

- `enforce: 'pre'`는 core plugin보다 먼저 돈다.
- `enforce: 'post'`는 build plugin 뒤에서 돈다.
- `apply: 'build'` 또는 `apply: 'serve'`로 실행 범위를 좁힌다.
- function form `apply(config, { command })`은 SSR build 제외 같은 세밀한 조건에 쓴다.

## Universal Hook

dev와 build 모두에서 같은 logic이 필요하면 아래 hook을 우선 본다.

- `resolveId(id, importer)`
- `load(id)`
- `transform(code, id)`

```ts
transform(code: string, id: string) {
  if (id.endsWith('.custom')) {
    return { code: compile(code), map: null }
  }
}
```

## Client-Server HMR 통신

서버에서 클라이언트로 보내기:

```ts
configureServer(server) {
  server.ws.send('my:event', { msg: 'hello' })
}
```

클라이언트에서 받기:

```ts
if (import.meta.hot) {
  import.meta.hot.on('my:event', (data) => {
    console.log(data.msg)
  })
}
```

클라이언트에서 서버로 보내기:

```ts
import.meta.hot.send('my:from-client', { msg: 'Hey!' })
```

```ts
server.ws.on('my:from-client', (data, client) => {
  client.send('my:ack', { msg: 'Got it!' })
})
```

## 빠른 판단 기준

- config만 바꾸면 되는 문제라면 plugin을 만들지 않는다.
- dev server middleware가 필요하면 `configureServer`가 맞다.
- HTML entry를 건드리는데 `transform()`을 쓰고 있으면 `transformIndexHtml`로 옮길지 먼저 본다.
- build-only transform이면 `apply: 'build'`를 빠뜨리지 않는다.