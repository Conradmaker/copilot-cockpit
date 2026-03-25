# CockroachDB Setup

Configure Prisma with CockroachDB.

## 1. Schema configuration

```prisma
datasource db {
  provider = "cockroachdb"
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
DATABASE_URL="postgresql://user:password@host:26257/db?sslmode=verify-full"
```

URL은 PostgreSQL wire protocol을 써도 `provider`는 반드시 `cockroachdb`로 둔다.

## 4. Driver adapter

```bash
npm install @prisma/adapter-pg pg
```

```ts
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## ID generation

CockroachDB에서는 `BigInt` 또는 UUID 전략을 명시적으로 선택하는 편이 좋다.

```prisma
model User {
  id BigInt @id @default(autoincrement())
}
```

또는:

```prisma
model User {
  id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
}
```