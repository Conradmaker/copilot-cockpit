# Connection Management

Prisma client lifecycle과 driver adapter pool 설정은 별개의 계층이지만 함께 봐야 한다. instance를 너무 많이 만들면 pool이 터지고, pool만 조절해도 잘못된 lifecycle은 고쳐지지 않는다.

## 1. 프로세스당 Prisma client를 하나로 재사용한다

```ts
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
})

export const prisma =
  globalForPrisma.prisma ?? new PrismaClient({ adapter })

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### 빠른 판단 기준

- request handler 안에서 `new PrismaClient()`를 만들면 우선 고친다.
- hot reload 환경에서 client singleton이 없으면 개발 중 connection이 쉽게 누적된다.

## 2. pool 설정은 adapter와 driver 문맥에서 본다

Prisma v7은 adapter 기반이므로 실제 connection behavior는 underlying driver 설정에 좌우된다.

```ts
const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
  max: 10,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
})
```

### 빠른 판단 기준

- v6 시절 URL query parameter 설정만 복사하지 말고, 현재 driver가 무엇을 받는지 먼저 확인한다.
- DB connection limit이 낮은 환경이면 pool size와 server concurrency를 함께 조정한다.

## 3. serverless와 edge는 adapter 선택이 중요하다

- direct TCP adapter는 장기 실행 Node 서버와 잘 맞는다.
- edge나 serverless는 Neon, libsql, Prisma Postgres, Accelerate 같은 경로가 더 적합할 수 있다.
- `prisma://` 또는 `prisma+postgres://`는 direct TCP adapter에 넣지 않는다.

### 빠른 판단 기준

- edge runtime인데 classic TCP connection을 당연하게 가정하면 runtime mismatch를 의심한다.
- Accelerate를 쓰는데 `PrismaPg` 같은 direct adapter를 붙이면 경로를 다시 잡는다.

## 4. SSL과 인증은 adapter layer에서 명시한다

```ts
const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
})
```

### 빠른 판단 기준

- self-signed certificate 이슈를 URL 파라미터만으로 우회하려고 하지 말고 adapter 옵션도 본다.
- 운영에서는 `rejectUnauthorized: false`를 기본값으로 두지 않는다.

## 리뷰 포인트

- singleton이 보장되는가
- adapter와 runtime이 맞는가
- pool size와 DB limit이 맞는가
- serverless/edge에서 direct TCP를 무리하게 쓰고 있지 않은가
- SSL과 인증 구성이 환경별로 분리돼 있는가