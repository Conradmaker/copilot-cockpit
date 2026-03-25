# Removed Features

Prisma v7에서는 몇 가지 익숙한 기능이 사라지거나 실행 방식이 바뀐다. upgrade 작업에서 놓치기 쉬운 부분만 먼저 정리한다.

## Client middleware

`prisma.$use()` middleware는 v7 mainline에서 제거됐다. query interception은 client extension으로 옮긴다.

```ts
const prisma = new PrismaClient({ adapter }).$extends({
  query: {
    $allModels: {
      async $allOperations({ operation, model, args, query }) {
        const before = Date.now()
        const result = await query(args)
        const after = Date.now()
        console.log(`${model}.${operation} took ${after - before}ms`)
        return result
      },
    },
  },
})
```

## Metrics

Metrics preview 기능은 제거됐다. query extension이나 driver-level metrics로 대체한다.

## Removed CLI habits

- `migrate dev --skip-generate`
- `migrate dev --skip-seed`
- `migrate reset --skip-seed`

v7에서는 auto-generate와 auto-seed를 기대하지 말고 명시적으로 실행한다.

```bash
prisma migrate dev --name add_field
prisma generate
prisma db seed
```

## migrate diff option changes

- `--from-url` → `--from-config-datasource`
- `--to-url` → `--to-config-datasource`
- `--from-schema-datasource` → `--from-config-datasource`
- `--to-schema-datasource` → `--to-config-datasource`

## rejectOnNotFound

legacy `rejectOnNotFound` 대신 `findUniqueOrThrow`, `findFirstOrThrow`를 쓴다.

### 빠른 판단 기준

- middleware 예시를 그대로 복붙하고 있으면 extension path로 바꾼다.
- migrate 이후 generate가 자동일 거라고 설명하면 v7 흐름과 어긋난다.
- old CLI flags를 스크립트에 남겨두면 먼저 제거한다.