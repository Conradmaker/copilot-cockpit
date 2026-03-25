# Environment Variables

Prisma v7은 `.env`를 자동으로 로드하지 않는다. env loading을 명시적으로 넣는다.

## Basic setup

### 1. Install dotenv

```bash
npm install dotenv
```

### 2. Load in prisma.config.ts

```ts
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  datasource: {
    url: env('DATABASE_URL'),
  },
})
```

## Bun

Bun은 `.env`를 자동 로드하므로 별도 `dotenv` import가 필요 없을 수 있다.

## Multiple env files

```bash
npm install -D dotenv-cli
```

```json
{
  "scripts": {
    "db:migrate": "dotenv -e .env.local -- prisma migrate dev",
    "db:push": "dotenv -e .env.development -- prisma db push"
  }
}
```

## Application code

```ts
import 'dotenv/config'

import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## Removed env vars

다음과 같은 engine 관련 Prisma env var는 v7 mainline에서 제거됐다.

- `PRISMA_CLI_QUERY_ENGINE_TYPE`
- `PRISMA_CLIENT_ENGINE_TYPE`
- `PRISMA_QUERY_ENGINE_BINARY`
- `PRISMA_QUERY_ENGINE_LIBRARY`
- `PRISMA_GENERATE_SKIP_AUTOINSTALL`
- `PRISMA_SKIP_POSTINSTALL_GENERATE`
- `PRISMA_MIGRATE_SKIP_GENERATE`
- `PRISMA_MIGRATE_SKIP_SEED`

## CI

CI에서는 dotenv 대신 secret env injection을 우선한다.

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```