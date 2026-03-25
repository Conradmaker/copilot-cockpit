# SQLite Setup

Configure Prisma with SQLite.

## 1. Schema configuration

`prisma/schema.prisma`:

```prisma
datasource db {
  provider = "sqlite"
}

generator client {
  provider = "prisma-client"
  output   = "../generated"
}
```

## 2. prisma.config.ts

```ts
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  datasource: {
    url: env('DATABASE_URL'),
  },
})
```

## 3. Environment variable

```env
DATABASE_URL="file:./dev.db"
```

Prisma v7에서는 SQLite URL 해석 기준이 config 파일 쪽으로 이동할 수 있으므로 schema 기준 상대 경로라고 단정하지 않는다.

## 4. Driver adapter

```bash
npm install @prisma/adapter-better-sqlite3 better-sqlite3
```

```ts
import { PrismaClient } from '../generated/client'
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3'

const adapter = new PrismaBetterSqlite3({
  url: process.env.DATABASE_URL ?? 'file:./dev.db',
})

export const prisma = new PrismaClient({ adapter })
```

## Turso or libSQL

```bash
npm install @prisma/adapter-libsql @libsql/client
```

```ts
import { PrismaClient } from '../generated/client'
import { PrismaLibSql } from '@prisma/adapter-libsql'

const adapter = new PrismaLibSql({
  url: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
})

export const prisma = new PrismaClient({ adapter })
```

## Limitations

- enum support가 제한적이다.
- scalar list가 직접 지원되지 않는다.
- write concurrency가 낮고 file lock 영향이 크다.