# MySQL Setup

Configure Prisma with MySQL or MariaDB.

## 1. Schema configuration

`prisma/schema.prisma`:

```prisma
datasource db {
  provider = "mysql"
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
DATABASE_URL="mysql://user:password@localhost:3306/mydb"
```

## 4. Driver adapter

```bash
npm install @prisma/adapter-mariadb mariadb
```

```ts
import { PrismaClient } from '../generated/client'
import { PrismaMariaDb } from '@prisma/adapter-mariadb'

const adapter = new PrismaMariaDb({
  host: 'localhost',
  port: 3306,
  connectionLimit: 5,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
})

export const prisma = new PrismaClient({ adapter })
```

CLI와 migration은 `DATABASE_URL`을 쓰고, runtime adapter는 discrete env vars나 driver-friendly config로 푸는 편이 다루기 쉽다.

## PlanetScale

PlanetScale는 foreign key 제약을 직접 지원하지 않으므로 relation emulation이 필요할 수 있다.

```prisma
datasource db {
  provider     = "mysql"
  relationMode = "prisma"
}
```

## Common issues

### Too many connections

MySQL connection limit과 adapter pool size를 같이 조정한다.

### JSON support

MySQL 5.7+ 또는 MariaDB 10.2+ 이상인지 확인한다.