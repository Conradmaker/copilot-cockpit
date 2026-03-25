# Prisma Accelerate Users

Accelerate 또는 Prisma Postgres의 `prisma://`, `prisma+postgres://` URL을 쓰는 경우 direct adapter path와 분리해서 본다.

## 핵심 규칙

**Accelerate URL을 direct driver adapter에 넣지 않는다.**

`PrismaPg`, `PrismaPostgresAdapter` 같은 direct adapter는 direct DB connection string을 기대한다.

## Correct setup

### 1. Keep the Accelerate URL

```env
DATABASE_URL="prisma://accelerate.prisma-data.net/?api_key=..."
```

또는:

```env
DATABASE_URL="prisma+postgres://accelerate.prisma-data.net/..."
```

### 2. Install the extension

```bash
npm install @prisma/extension-accelerate
```

### 3. prisma.config.ts

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

### 4. Instantiate with accelerateUrl

```ts
import { PrismaClient } from '../generated/client'
import { withAccelerate } from '@prisma/extension-accelerate'

export const prisma = new PrismaClient({
  accelerateUrl: process.env.DATABASE_URL,
}).$extends(withAccelerate())
```

## What not to do

```ts
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})
```

위 코드는 `DATABASE_URL`이 `prisma://` 또는 `prisma+postgres://`이면 잘못된 경로다.

## Migrations

CLI는 Accelerate URL만으로 충분할 수도 있지만, direct DB connection이 필요한 운영 환경도 있다.

```env
DATABASE_URL="prisma+postgres://..."
DIRECT_DATABASE_URL="postgresql://..."
```

```ts
export default defineConfig({
  datasource: {
    url: env('DIRECT_DATABASE_URL'),
  },
})
```

## Caching

```ts
const users = await prisma.user.findMany({
  cacheStrategy: {
    ttl: 60,
    swr: 120,
  },
})
```

### 빠른 판단 기준

- adapter와 accelerate path를 동시에 섞지 않는다.
- runtime URL과 migration URL을 분리해야 하는지 먼저 판단한다.