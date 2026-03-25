# Prisma Postgres Setup

Configure Prisma with Prisma Postgres.

## Overview

Prisma Postgres는 Prisma managed PostgreSQL 경로다. runtime path를 direct TCP adapter로 가져갈지, Accelerate extension path로 가져갈지 먼저 분기한다.

## 1. Schema configuration

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

## 3. Connection strings

```env
DATABASE_URL="prisma+postgres://api_key@host.prisma-data.net/env_id"
PRISMA_DIRECT_TCP_URL="postgresql://user:password@host:5432/db"
```

## 4. Direct TCP adapter path

```bash
npm install @prisma/adapter-ppg @prisma/ppg
```

```ts
import 'dotenv/config'
import { PrismaClient } from '../generated/client'
import { PrismaPostgresAdapter } from '@prisma/adapter-ppg'

export const prisma = new PrismaClient({
  adapter: new PrismaPostgresAdapter({
    connectionString: process.env.PRISMA_DIRECT_TCP_URL,
  }),
})
```

## 5. Accelerate-style path

`prisma+postgres://` URL을 앱 runtime에서 그대로 쓰려면 [accelerate-users](accelerate-users.md) 경로를 함께 본다.

## Features

- serverless-friendly runtime path
- query caching and edge support options
- Prisma ecosystem integration