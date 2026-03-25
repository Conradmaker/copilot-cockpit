# PostgreSQL Setup

Configure Prisma with PostgreSQL.

## 1. Schema configuration

`prisma/schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"
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
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
```

## 4. Driver adapter

```bash
npm install @prisma/adapter-pg pg
```

```ts
import 'dotenv/config'
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## Common issues

### Can't reach database server

- host와 port를 다시 확인한다.
- DB 프로세스와 네트워크 접근을 먼저 확인한다.

### Authentication failed

- username/password를 다시 확인한다.
- 비밀번호에 특수문자가 있으면 URL encode 여부를 본다.

### Schema does not exist

- `?schema=public` 또는 실제 schema 이름이 URL에 맞는지 확인한다.