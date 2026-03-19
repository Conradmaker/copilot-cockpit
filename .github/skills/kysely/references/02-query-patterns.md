# Kysely 쿼리 패턴

## 언제 읽는가

- `selectFrom`, `insertInto`, `updateTable`, `deleteFrom`를 작성할 때
- join, aggregation, subquery, CTE가 필요한 쿼리를 만들 때
- Postgres JSON helper나 pagination 패턴이 필요할 때

---

## 1. 기본 CRUD

```ts
const users = await db
  .selectFrom("users")
  .select(["id", "email", "name"])
  .where("created_at", ">", new Date("2024-01-01"))
  .execute();

const inserted = await db
  .insertInto("users")
  .values({
    email: "alice@example.com",
    name: "Alice",
    updated_at: new Date(),
  })
  .returningAll()
  .executeTakeFirstOrThrow();

await db
  .updateTable("users")
  .set({name: "Alice Updated", updated_at: new Date()})
  .where("id", "=", 1)
  .execute();

await db
  .deleteFrom("users")
  .where("email", "like", "%@spam.com")
  .execute();
```

### 빠른 판단 기준

- 빌더만 만들고 `execute()`를 빼먹지 않는다.
- 조회 컬럼은 가능한 한 명시한다. `selectAll()`은 내부 도구성 코드나 정말 필요한 경우에만 쓴다.
- `executeTakeFirstOrThrow()`는 결과가 반드시 있어야 하는 조회/삽입 결과에만 쓴다.

---

## 2. Join과 nullability

```ts
const usersWithPosts = await db
  .selectFrom("users")
  .innerJoin("posts", "posts.user_id", "users.id")
  .select(["users.id", "users.name", "posts.title"])
  .execute();

const usersWithOptionalPosts = await db
  .selectFrom("users")
  .leftJoin("posts", "posts.user_id", "users.id")
  .select(["users.id", "users.email", "posts.title"])
  .execute();
```

`LEFT JOIN` 결과는 null 가능성을 그대로 가져간다.

### 빠른 판단 기준

- `LEFT JOIN`이면 오른쪽 테이블 컬럼을 `null` 가능성으로 처리한다.
- 충돌 가능한 컬럼명은 `as` alias로 분리한다.
- 조인 조건이 FK와 정확히 맞는지 먼저 점검한다.

---

## 3. Aggregation과 grouping

```ts
const stats = await db
  .selectFrom("posts")
  .select([
    "user_id",
    db.fn.count<number>("id").as("post_count"),
    db.fn.avg<number>("views").as("avg_views"),
  ])
  .groupBy("user_id")
  .having(db.fn.count("id"), ">", 5)
  .execute();
```

복잡한 aggregate는 `sql`과 조합해도 된다.

```ts
import {sql} from "kysely";

const advanced = await db
  .selectFrom("users")
  .leftJoin("posts", "posts.user_id", "users.id")
  .select([
    "users.id",
    sql<number>`COUNT(DISTINCT posts.id)`.as("total_posts"),
    sql<Date>`MAX(posts.created_at)`.as("latest_post"),
  ])
  .groupBy("users.id")
  .execute();
```

---

## 4. Subquery

```ts
const usersWithPostCount = await db
  .selectFrom("users")
  .select([
    "users.id",
    "users.name",
    (eb) =>
      eb
        .selectFrom("posts")
        .select(eb.fn.count<number>("id").as("count"))
        .whereRef("posts.user_id", "=", "users.id")
        .as("post_count"),
  ])
  .execute();
```

`EXISTS`와 `IN`도 동일하게 표현할 수 있다.

```ts
const activeUsers = await db
  .selectFrom("users")
  .selectAll()
  .where((eb) =>
    eb.exists(
      eb
        .selectFrom("posts")
        .select("id")
        .whereRef("posts.user_id", "=", "users.id")
        .where("created_at", ">", new Date("2024-01-01"))
    )
  )
  .execute();
```

### 빠른 판단 기준

- 외부 컬럼 참조는 `whereRef`를 먼저 본다.
- membership check는 `IN`보다 `EXISTS`가 더 자연스러운지 같이 검토한다.
- builder가 지나치게 장황해지면 CTE나 raw SQL로 바꾸는 편이 낫다.

---

## 5. CTE

```ts
const result = await db
  .with("popular_posts", (db) =>
    db
      .selectFrom("posts")
      .select(["id", "user_id", "title"])
      .where("views", ">", 1000)
  )
  .with("active_users", (db) =>
    db
      .selectFrom("users")
      .select(["id", "email"])
      .where("last_login", ">", new Date("2024-01-01"))
  )
  .selectFrom("popular_posts")
  .innerJoin("active_users", "active_users.id", "popular_posts.user_id")
  .selectAll()
  .execute();
```

재귀 CTE도 가능하다.

```ts
interface OrgNode {
  id: number;
  name: string;
  parent_id: number | null;
  level: number;
}
```

### 빠른 판단 기준

- 한 쿼리 안에서 중간 결과를 이름 붙여 설명하고 싶다면 CTE를 우선 검토한다.
- 트리/계층 구조면 recursive CTE를 고려한다.
- DB dialect가 recursive CTE를 어떻게 지원하는지 먼저 확인한다.

---

## 6. Postgres helper와 중첩 결과

```ts
import {jsonArrayFrom, jsonBuildObject} from "kysely/helpers/postgres";
import {sql} from "kysely";

const usersWithPosts = await db
  .selectFrom("users")
  .select([
    "users.id",
    "users.name",
    jsonArrayFrom(
      db
        .selectFrom("posts")
        .select(["posts.id", "posts.title", "posts.content"])
        .whereRef("posts.user_id", "=", "users.id")
    ).as("posts"),
  ])
  .execute();

const nested = await db
  .selectFrom("users")
  .select([
    "users.id",
    jsonBuildObject({
      name: "users.name",
      email: "users.email",
      postCount: sql<number>`(SELECT COUNT(*) FROM posts WHERE user_id = users.id)`,
    }).as("user_data"),
  ])
  .execute();
```

---

## 7. Pagination helper

```ts
import {SelectQueryBuilder} from "kysely";

function paginate<DB, TB extends keyof DB, O>(
  query: SelectQueryBuilder<DB, TB, O>,
  page: number,
  pageSize: number
) {
  return query.limit(pageSize).offset((page - 1) * pageSize);
}
```

카운트가 필요하면 count query를 별도로 유지한다.

### 빠른 판단 기준

- offset pagination은 관리 화면이나 낮은 cardinality 목록에 적합하다.
- 무한 스크롤이나 large dataset이면 cursor pagination을 별도로 설계한다.

---

## 8. Full-text search 예시

```ts
import {sql} from "kysely";

const searchResults = await db
  .selectFrom("posts")
  .selectAll()
  .where(sql`search_vector`, "@@", sql`to_tsquery('english', ${query})`)
  .execute();
```

Kysely가 인덱스를 대신 잡아주지 않는다. 성능은 DB schema와 index 설계가 좌우한다.
