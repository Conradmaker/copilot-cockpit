# Driver Adapters

Prisma v7의 기본 runtime path는 driver adapter다. direct database connection을 쓴다면 adapter를 명시적으로 고른다.

## Adapter matrix

| Database | Adapter package | Underlying driver |
| --- | --- | --- |
| PostgreSQL | `@prisma/adapter-pg` | `pg` |
| CockroachDB | `@prisma/adapter-pg` | `pg` |
| MySQL or MariaDB | `@prisma/adapter-mariadb` | `mariadb` |
| SQLite | `@prisma/adapter-better-sqlite3` | `better-sqlite3` |
| Turso or libSQL | `@prisma/adapter-libsql` | `@libsql/client` |
| SQL Server | `@prisma/adapter-mssql` | `mssql` |
| Prisma Postgres | `@prisma/adapter-ppg` | `@prisma/ppg` |
| Neon | `@prisma/adapter-neon` | `@neondatabase/serverless` |
| PlanetScale | `@prisma/adapter-planetscale` | `@planetscale/database` |
| D1 | `@prisma/adapter-d1` | Cloudflare D1 |

## Base pattern

```ts
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## Pool and SSL

driver adapter는 underlying driver 설정을 그대로 따른다.

```ts
const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
  ssl: {
    rejectUnauthorized: false,
  },
})
```

## Migration from v6

### Before

```ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient({
  datasources: {
    db: { url: process.env.DATABASE_URL },
  },
})
```

### After

```ts
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

const prisma = new PrismaClient({ adapter })
```

## Fast checks

- direct DB URL이면 adapter path를 쓴다.
- `prisma://` 또는 `prisma+postgres://` URL이면 [accelerate-users](accelerate-users.md)를 먼저 본다.
- runtime이 edge이면 adapter가 해당 환경을 지원하는지 먼저 확인한다.