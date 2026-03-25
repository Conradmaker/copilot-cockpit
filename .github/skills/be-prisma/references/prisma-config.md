# Prisma Config

Prisma v7에서는 `prisma.config.ts`가 CLI configuration의 중심이다.

## Basic configuration

```ts
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: {
    path: 'prisma/migrations',
  },
  datasource: {
    url: env('DATABASE_URL'),
  },
})
```

## Common options

### datasource.url

```ts
datasource: {
  url: env('DATABASE_URL'),
}
```

### datasource.directUrl

```ts
datasource: {
  url: env('DATABASE_URL'),
  directUrl: env('DIRECT_DATABASE_URL'),
}
```

### datasource.shadowDatabaseUrl

```ts
datasource: {
  url: env('DATABASE_URL'),
  shadowDatabaseUrl: env('SHADOW_DATABASE_URL'),
}
```

### migrations.seed

```ts
migrations: {
  path: 'prisma/migrations',
  seed: 'tsx prisma/seed.ts',
}
```

## Monorepo example

```ts
import 'dotenv/config'
import path from 'path'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: path.join(__dirname, 'packages/database/prisma/schema.prisma'),
  migrations: {
    path: path.join(__dirname, 'packages/database/prisma/migrations'),
  },
  datasource: {
    url: env('DATABASE_URL'),
  },
})
```

## Fast checks

- datasource URL이 아직 `schema.prisma`에 남아 있으면 config 이동을 먼저 검토한다.
- `--url`이나 legacy CLI flag 설명이 보이면 config-first 흐름으로 바꿀지 확인한다.