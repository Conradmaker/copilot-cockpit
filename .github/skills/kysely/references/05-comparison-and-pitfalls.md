# Kysely 비교, 운영 원칙, 함정

## 언제 읽는가

- Kysely를 Prisma/Drizzle와 비교해야 할 때
- Kysely 도입 여부를 판단할 때
- 흔한 타입 실수나 query-builder 오용을 점검할 때

---

## 1. Kysely vs Drizzle vs Prisma

| 항목 | Kysely | Drizzle | Prisma |
| --- | --- | --- | --- |
| 기본 성격 | SQL-first query builder | schema-first query builder | ORM |
| 타입 안전성 | schema → query → result 전 구간 | schema → query 전 구간 | generated client 중심 |
| SQL 제어력 | 높음 | 높음 | 상대적으로 제한적 |
| raw SQL 친화성 | 매우 높음 | 높음 | 낮음 |
| relation abstraction | 직접 설계 | 일부 제공 | 강함 |
| codegen 의존성 | 선택 | 낮음 | 높음 |
| 적합한 상황 | 복잡한 SQL, 기존 DB, 성능 민감 | TS schema 중심 greenfield | 빠른 개발, ORM 선호 팀 |

### Kysely를 고르기 좋은 경우

- 팀이 SQL을 읽고 유지보수할 수 있다.
- 복잡한 join, subquery, CTE, window function이 많다.
- 기존 데이터베이스를 그대로 활용해야 한다.
- ORM의 relation abstraction보다 SQL 제어권이 더 중요하다.
- edge/serverless처럼 bundle 부담을 줄이고 싶다.

### 다른 선택지가 더 나은 경우

- relation mapping과 높은 추상화가 더 중요하다면 Prisma가 나을 수 있다.
- schema-first 선언 경험을 더 선호하면 Drizzle이 더 잘 맞을 수 있다.
- 팀이 SQL에 익숙하지 않다면 Kysely는 학습 비용이 높아질 수 있다.

---

## 2. 운영 원칙

1. Kysely를 ORM처럼 다루지 않는다.
2. 결과 shape는 query에서 명시적으로 설계한다.
3. 성능은 인덱스와 SQL shape가 좌우한다.
4. migration은 small batch로 나눈다.
5. raw SQL은 escape hatch이지 실패가 아니다.
6. repository/service 경계에서 return type을 안정화한다.

---

## 3. 흔한 함정

### `execute()`를 빼먹는 경우

```ts
const users = db.selectFrom("users").selectAll();
```

위 코드는 결과가 아니라 query builder다.

```ts
const users = await db.selectFrom("users").selectAll().execute();
```

### `Generated`를 빼먹는 경우

```ts
interface UserTable {
  id: number;
}
```

이렇게 두면 `INSERT` 시 `id` 입력을 요구받는다.

```ts
import {Generated} from "kysely";

interface UserTable {
  id: Generated<number>;
}
```

### `LEFT JOIN` nullability를 무시하는 경우

```ts
const result = await db
  .selectFrom("users")
  .leftJoin("posts", "posts.user_id", "users.id")
  .select(["users.name", "posts.title"])
  .execute();
```

여기서 `posts.title`은 `string | null`일 수 있다.

### builder를 과도하게 고집하는 경우

쿼리가 지나치게 복잡해져 읽기 어려우면 CTE나 raw SQL로 전환한다. Kysely 사용의 목적은 builder 순수주의가 아니라 type-safe SQL 유지다.

---

## 4. 실무 체크리스트

- 결과 row shape가 호출부 기대와 정확히 맞는가
- nullable 컬럼과 join nullability를 처리했는가
- transaction boundary가 명확한가
- dialect-specific SQL을 별도 helper나 reference로 남겼는가
- migration이 backward compatible한가
- 인덱스와 query plan을 별도로 검토했는가

---

## 5. 참고 리소스

- 공식 문서: https://kysely.dev
- GitHub: https://github.com/kysely-org/kysely
- Playground: https://kysely-org.github.io/kysely-playground/
- codegen: https://github.com/RobinBlomberg/kysely-codegen
