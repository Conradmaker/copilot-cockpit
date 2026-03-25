# SQL Server Setup

Configure Prisma with Microsoft SQL Server or Azure SQL.

## 1. Schema configuration

```prisma
datasource db {
  provider = "sqlserver"
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
DATABASE_URL="sqlserver://localhost:1433;database=mydb;user=sa;password=Password123;encrypt=true;trustServerCertificate=true"
```

## 4. Driver adapter

```bash
npm install @prisma/adapter-mssql mssql
```

```ts
import { PrismaClient } from '../generated/client'
import { PrismaMssql } from '@prisma/adapter-mssql'

const adapter = new PrismaMssql({
  server: 'localhost',
  port: 1433,
  database: 'mydb',
  user: process.env.SQLSERVER_USER,
  password: process.env.SQLSERVER_PASSWORD,
  options: {
    encrypt: true,
    trustServerCertificate: true,
  },
})

export const prisma = new PrismaClient({ adapter })
```

## Common issues

### Login failed for user

- SQL Server authentication mode와 credentials를 확인한다.
- TCP/IP가 활성화돼 있는지 확인한다.

### Table not found in dbo schema

- 기본 schema가 `dbo`라는 가정을 쓰고 있는지 확인한다.