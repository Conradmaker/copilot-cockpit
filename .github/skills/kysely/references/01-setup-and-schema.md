# Kysely 설정과 스키마 타입

## 언제 읽는가

- Kysely를 처음 붙일 때
- `Database` 인터페이스와 테이블 타입을 정의할 때
- 기존 DB에서 타입을 생성할지, 수동으로 관리할지 결정할 때

---

## 1. 설치

```bash
npm install kysely
npm install pg
```

드라이버는 실제 데이터베이스에 맞춰 고른다.

- PostgreSQL: `pg`
- MySQL: `mysql2`
- SQLite: `better-sqlite3`
- MSSQL: 해당 dialect 패키지

Kysely는 ORM이 아니라 SQL query builder다. 따라서 연결 풀 설정, 인덱스 전략, relation loading, validation은 직접 책임져야 한다.

---

## 2. 테이블 타입을 먼저 고정한다

Kysely의 핵심은 `Database` 인터페이스다. 쿼리 이전에 테이블별 타입을 먼저 안정화해야 이후 모든 추론이 일관된다.

```ts
import { Generated, Insertable, Selectable, Updateable } from "kysely"

interface UserTable {
  id: Generated<number>
  email: string
  name: string | null
  created_at: Generated<Date>
  updated_at: Date
}

interface PostTable {
  id: Generated<number>
  user_id: number
  title: string
  content: string | null
  published: Generated<boolean>
  created_at: Generated<Date>
}

export interface Database {
  users: UserTable
  posts: PostTable
}

export type User = Selectable<UserTable>
export type NewUser = Insertable<UserTable>
export type UserUpdate = Updateable<UserTable>
```

### 빠른 판단 기준

- DB가 생성하는 컬럼이면 `Generated<T>`를 우선 검토한다.
- 조회 전용 결과 타입이 필요하면 `Selectable<T>`를 쓴다.
- `INSERT` payload는 `Insertable<T>`, `UPDATE` payload는 `Updateable<T>`를 기본값으로 둔다.
- nullable 컬럼은 TypeScript에서도 nullable로 유지한다. Kysely가 대신 숨겨주지 않는다.

---

## 3. 읽기/쓰기 타입이 다르면 `ColumnType`을 쓴다

날짜, JSON, numeric, UUID처럼 select/insert/update 타입이 다를 때는 `ColumnType`이 필요하다.

```ts
import { ColumnType, Generated } from "kysely"

interface ProductTable {
  id: Generated<string>
  price: ColumnType<number, number, number | undefined>
  metadata: ColumnType<Record<string, unknown>, string, string>
  created_at: ColumnType<Date, string | undefined, never>
}
```

### 언제 필요한가

- DB 드라이버가 문자열로 받지만 애플리케이션에서는 다른 타입으로 쓰고 싶을 때
- JSON/JSONB 컬럼을 객체로 읽고 문자열로 쓰는 식의 비대칭 매핑이 필요할 때
- `numeric` 정밀도를 문자열로 유지할지 숫자로 변환할지 명시해야 할 때

---

## 4. Kysely 인스턴스 생성

```ts
import { Kysely, PostgresDialect } from "kysely"
import { Pool } from "pg"
import type { Database } from "./database"

export const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 10,
    }),
  }),
})
```

### 빠른 판단 기준

- 앱 전체에서 공유할 단일 `db` 인스턴스를 만든다.
- 서버리스 환경이면 연결 풀과 lifecycle을 프레임워크 런타임에 맞춰 조정한다.
- 트랜잭션 단위 작업에서는 전역 `db` 대신 전달받은 `trx`를 계속 사용한다.

---

## 5. 기존 DB가 있으면 `kysely-codegen`을 우선 검토한다

수동으로 타입을 만드는 것보다 기존 스키마에서 생성하는 편이 drift를 줄인다.

```bash
npm install --save-dev kysely-codegen
npx kysely-codegen --url "postgresql://user:pass@localhost:5432/mydb"
```

생성 파일 예시:

```ts
import type { Generated } from "kysely"

export interface Database {
  users: UsersTable
  posts: PostsTable
}

export interface UsersTable {
  id: Generated<number>
  email: string
  name: string | null
  created_at: Generated<Date>
}
```

### 수동 정의 vs codegen

- greenfield + 스키마 변화가 잦음: 수동 정의도 가능
- 기존 DB 사용: codegen 우선
- DB가 여러 서비스와 공유됨: codegen 쪽이 drift 관리에 유리
- DB 타입이 커스텀 변환을 많이 요구함: 생성 후 래퍼 타입을 덧씌운다

---

## 6. 추천 초기 구조

```text
src/db/
├── client.ts
├── database.ts
├── queries/
│   ├── users.ts
│   └── posts.ts
└── migrations/
```

### 구조 원칙

- `database.ts`: 테이블 타입과 `Database` 인터페이스
- `client.ts`: dialect와 pool 설정
- `queries/`: 도메인별 쿼리 함수
- `migrations/`: schema 변경 이력

테이블 타입과 쿼리 함수를 같은 파일에 무리하게 섞지 않는 편이 유지보수에 유리하다.
