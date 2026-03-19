# Kysely 트랜잭션과 raw SQL

## 언제 읽는가

- 여러 쿼리를 원자적으로 묶어야 할 때
- isolation level을 조정해야 할 때
- query builder보다 SQL이 더 명확한 쿼리를 써야 할 때

---

## 1. 기본 트랜잭션

```ts
await db.transaction().execute(async (trx) => {
  await trx
    .insertInto("users")
    .values({
      email: "alice@example.com",
      name: "Alice",
      updated_at: new Date(),
    })
    .execute();

  await trx
    .insertInto("posts")
    .values({
      user_id: 1,
      title: "First Post",
      content: "Hello",
    })
    .execute();
});
```

에러가 나면 자동 rollback된다.

### 빠른 판단 기준

- 하나라도 실패하면 전부 취소되어야 하는 작업이면 transaction을 건다.
- 트랜잭션 내부에서는 전역 `db`가 아니라 전달받은 `trx`만 사용한다.
- 외부 API 호출처럼 오래 걸리는 부수효과는 트랜잭션 안에 오래 잡아두지 않는다.

---

## 2. 결과를 반환하는 트랜잭션

```ts
const result = await db.transaction().execute(async (trx) => {
  const user = await trx
    .insertInto("users")
    .values({
      email: "bob@example.com",
      name: "Bob",
      updated_at: new Date(),
    })
    .returningAll()
    .executeTakeFirstOrThrow();

  const post = await trx
    .insertInto("posts")
    .values({
      user_id: user.id,
      title: "Bob's Post",
      content: "Content",
    })
    .returningAll()
    .executeTakeFirstOrThrow();

  return {user, post};
});
```

---

## 3. Isolation level

```ts
await db
  .transaction()
  .setIsolationLevel("serializable")
  .execute(async (trx) => {
    const balance = await trx
      .selectFrom("accounts")
      .select("balance")
      .where("id", "=", accountId)
      .executeTakeFirstOrThrow();

    await trx
      .updateTable("accounts")
      .set({balance: balance.balance - amount})
      .where("id", "=", accountId)
      .execute();
  });
```

### 빠른 판단 기준

- 기본값으로 충분하면 isolation level을 굳이 올리지 않는다.
- race condition이 실제로 문제인 쓰기 작업에만 더 강한 isolation을 검토한다.
- isolation 강화는 정확성뿐 아니라 잠금 비용도 함께 고려한다.

---

## 4. `sql` template tag

Kysely는 raw SQL escape hatch를 제공한다. builder보다 SQL이 더 읽기 쉬우면 과감하게 `sql`을 쓴다.

```ts
import {sql} from "kysely";

const result = await db
  .selectFrom("users")
  .select([
    "id",
    sql<string>`UPPER(name)`.as("uppercase_name"),
    sql<number>`EXTRACT(YEAR FROM created_at)`.as("year_created"),
  ])
  .execute();
```

```ts
const filtered = await db
  .selectFrom("posts")
  .selectAll()
  .where(sql`LOWER(title)`, "like", "%typescript%")
  .execute();
```

### 빠른 판단 기준

- 함수식, window function, vendor-specific feature처럼 builder가 지나치게 복잡해지면 `sql`을 검토한다.
- 값 바인딩은 템플릿 보간으로 넘기고 문자열 이어붙이기를 피한다.
- raw SQL을 쓴다고 type safety를 완전히 버릴 필요는 없다. 결과 타입을 함께 선언한다.

---

## 5. 전체 raw query

```ts
const topPosts = await sql<{id: number; user_id: number; rank: number}>`
  WITH ranked_posts AS (
    SELECT
      p.id,
      p.user_id,
      ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY views DESC) AS rank
    FROM posts p
  )
  SELECT * FROM ranked_posts WHERE rank <= 3
`.execute(db);
```

```ts
const email = "alice@example.com";

const user = await sql<{id: number; email: string}>`
  SELECT id, email
  FROM users
  WHERE email = ${email}
`.execute(db);
```

---

## 6. raw SQL 사용 원칙

- query builder로 자연스럽게 표현되면 builder를 유지한다.
- SQL 자체가 더 설명적이면 `sql`을 쓴다.
- 벤더 종속 SQL은 reference나 helper 함수로 의도를 남긴다.
- 사용자 입력을 문자열로 조립하지 않는다.
- 서비스 계층에서는 raw SQL 여부보다 반환 shape와 transaction boundary를 더 중요하게 본다.
