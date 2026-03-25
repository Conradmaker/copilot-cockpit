# MongoDB Setup

**Warning: MongoDB는 Prisma v7 메인라인에서 지원되지 않는다.**

MongoDB를 계속 사용해야 한다면 Prisma v6 경로로 분기한다.

## 1. Schema configuration (v6)

```prisma
datasource db {
  provider = "mongodb"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}
```

## 2. ID field requirement

MongoDB model은 `_id` 매핑을 명시적으로 둔다.

```prisma
model User {
  id    String @id @default(auto()) @map("_id") @db.ObjectId
  email String @unique
  name  String?
}
```

relation ID도 `@db.ObjectId` 타입과 맞춰야 한다.

```prisma
model Post {
  id       String @id @default(auto()) @map("_id") @db.ObjectId
  author   User   @relation(fields: [authorId], references: [id])
  authorId String @db.ObjectId
}
```

## 3. Environment variable

```env
DATABASE_URL="mongodb+srv://user:password@cluster.mongodb.net/mydb?retryWrites=true&w=majority"
```

## 4. Migrations vs sync

- MongoDB는 schema-less라 `prisma migrate`를 쓰지 않는다.
- `prisma db push`로 index와 constraint를 sync한다.
- `prisma db pull`은 sampling 기반 introspection으로 본다.

## Common issues

### Transactions not supported

Replica set 구성이 필요하다. standalone MongoDB는 transaction을 지원하지 않는다.

### Invalid ObjectID

참조 field에 `@db.ObjectId`가 빠졌는지 먼저 확인한다.