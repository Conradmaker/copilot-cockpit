# ESM Support

Prisma v7은 ESM-only 기본선을 전제로 둔다. CommonJS 프로젝트라면 무리하게 우회하기보다 ESM 경계를 먼저 정리한다.

## package.json

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "module": "ESNext",
    "moduleResolution": "bundler",
    "target": "ES2023",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src/**/*", "prisma/**/*"]
}
```

`Node16` 또는 `NodeNext` 조합도 가능하지만, 해당 경로에서는 `.js` extension 처리까지 같이 본다.

## Import pattern

```ts
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## CommonJS boundary

CommonJS를 완전히 없애기 어렵다면 Prisma 전용 ESM boundary를 만든다.

```js
// prisma.mjs
import { PrismaClient } from '../generated/client'
import { PrismaPg } from '@prisma/adapter-pg'

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL,
})

export const prisma = new PrismaClient({ adapter })
```

## Framework notes

- Next.js는 ESM을 기본 지원하므로 config 파일 확장자와 generated client import path를 먼저 본다.
- Jest를 쓴다면 ESM preset 또는 Vitest 전환을 검토한다.

## Fast checks

- `require()`로 Prisma v7 client를 가져오고 있으면 먼저 멈춘다.
- generated client import path가 ESM boundary와 맞는지 확인한다.
- SQLite path, tsconfig moduleResolution, runtime loader 설정이 함께 맞물리는지 본다.