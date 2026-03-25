# Prisma Client Setup

Prisma v7 기준에서 공통 client setup surface는 generator, output path, generate cadence, adapter wiring, single-instance reuse다.

## 1. 패키지를 설치한다

```bash
npm install -D prisma
npm install @prisma/client
```

## 2. generator를 v7 기준으로 맞춘다

`prisma/schema.prisma`:

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated"
}
```

`output`은 필수다. 생성 위치가 바뀌면 import 경로도 같이 바뀐다.

## 3. generate를 명시적으로 실행한다

```bash
npx prisma generate
```

schema 변경 후에는 다시 실행한다.

## 4. adapter와 함께 PrismaClient를 만든다

```ts
import 'dotenv/config'
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

provider가 다르면 adapter도 같이 바뀐다.

## 5. single instance를 유지한다

각 `PrismaClient` instance는 DB 연결을 만든다. 프로세스당 하나를 재사용하는 편이 안전하다.

### 빠른 판단 기준

- `@prisma/client`에서 바로 import하고 generated output을 안 쓰면 legacy 여부를 다시 본다.
- schema를 바꿨는데 generate가 안 돌아서 타입이 안 맞으면 regenerate부터 한다.
- request마다 client를 새로 만들면 connection lifecycle부터 고친다.