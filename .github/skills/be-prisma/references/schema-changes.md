# Schema Changes

Prisma v7에서는 generator와 datasource surface가 바뀐다. 먼저 generator를 `prisma-client`로 옮기고, datasource URL은 `prisma.config.ts`로 이동하는 흐름을 기준으로 본다.

## Generator block

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated"
}
```

## 핵심 변경점

### 1. provider name

v7에서는 `prisma-client`를 쓴다.

### 2. output is required

`output`은 필수다. generated client는 더 이상 `node_modules`에 자동 생성되지 않는다.

### 3. datasource URL은 config로 이동한다

`schema.prisma`에는 provider만 남기고, URL 관련 설정은 `prisma.config.ts`로 이동한다.

```prisma
datasource db {
  provider = "postgresql"
}
```

```ts
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: {
    url: env('DATABASE_URL'),
    directUrl: env('DIRECT_URL'),
    shadowDatabaseUrl: env('SHADOW_DATABASE_URL'),
  },
})
```

### 4. engineType는 제거됐다

generator의 `engineType` 설정은 v7 경로에서 제거한다.

## After schema changes

1. `npx prisma generate`
2. generated client import 경로를 새 output 기준으로 업데이트
3. generated output이 VCS에 들어가지 않게 ignore 정책을 확인