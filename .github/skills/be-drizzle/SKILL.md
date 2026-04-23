---
name: be-drizzle
description: "Drizzle ORM 스키마 설계, relation modeling, migrations, query optimization, transactions, connection management, drizzle-kit 설정을 위한 스킬이다. Use this skill when working on Drizzle schema files (pgTable, mysqlTable, sqliteTable), adding or refactoring Drizzle models, choosing relation patterns, wiring drizzle() instances, configuring PostgreSQL/MySQL/SQLite/Neon/Turso/PlanetScale, fixing migration drift, or optimizing queries. Always consult for Drizzle persistence, even if user only asks to 'add a table', 'connect the database', or 'fix a Drizzle error'. For REST API design use be-api-design. For Prisma use be-prisma. For raw SQL use be-kysely. Triggers on: Drizzle, drizzle-orm, drizzle-kit, drizzle.config, pgTable, mysqlTable, sqliteTable, relations(), $inferSelect, $inferInsert, drizzle-kit generate, drizzle-kit migrate, drizzle-kit push, node-postgres, postgres-js, Neon, Turso, PlanetScale, 드리즐, 스키마 설계, 마이그레이션, DB 연결, ORM."
---

# Drizzle ORM 설계 & 운영 (be-drizzle)

## 목표

Drizzle을 단순 query wrapper가 아니라 schema, relation, migration, query, connection까지 포함한 type-safe SQL persistence contract로 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 작업을 시작하기 전에는 현재 문제에 맞는 reference 문서를 먼저 읽고, 훈련 데이터 기반 추측보다 로컬 reference를 우선 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 기본선

- Drizzle ORM + drizzle-kit을 기본 persistence stack으로 둔다.
- dialect 기반 설정을 전제로 한다. `drizzle.config.ts`에서 `dialect: 'postgresql' | 'mysql' | 'sqlite'`를 명시적으로 고정한다.
- PostgreSQL 환경에서는 `node-postgres` (`pg` + Pool)를 기본 driver로 둔다. serverless/edge 환경이면 `postgres-js`를 대안으로 검토한다.
- TypeScript-first 타입 추론을 기본값으로 둔다. `$inferSelect`, `$inferInsert`로 schema에서 직접 타입을 추론하고, 별도 type generation 단계를 두지 않는다.
- `drizzle-kit generate` → SQL review → `drizzle-kit migrate` 순서를 migration 기본 계약으로 둔다. `push`는 prototype/throwaway DB에서만 허용한다.
- import 생성 전에 `tsconfig.json`의 path alias (`compilerOptions.paths`)를 확인한다. alias가 있으면 사용하고, 없으면 상대 경로를 기본값으로 둔다.

---

## 핵심 단계

### 1. 런타임 기준선을 먼저 고정한다

schema를 바꾸기 전에 현재 프로젝트의 dialect, driver, config, 연결 방식이 안정적인지 확인한다. 이 기준선이 흔들리면 그 뒤의 schema와 migration 작업도 쉽게 어긋난다.

- `drizzle.config.ts`에서 `dialect`가 명시되어 있는지 확인한다.
- `dbCredentials.url`이 환경변수에서 올바르게 로드되는지 확인한다. `drizzle-kit`은 별도 프로세스로 실행되므로 `.env` 자동 로딩을 가정하면 `url: undefined` 에러가 생긴다.
- driver 선택이 실행 환경과 맞는지 확인한다. Node.js 서버(Express, Fastify, Bun)에서는 `node-postgres` Pool, serverless/edge(Vercel Edge, Cloudflare Workers)에서는 `postgres-js`나 provider-specific driver를 쓴다.
- `drizzle()` 인스턴스가 프로세스당 하나로 재사용되는지 확인한다. 매 요청마다 새 인스턴스를 만들면 connection lifecycle부터 고친다.

#### 빠른 판단 기준

- `drizzle.config.ts`가 없거나 `dialect`가 빠져 있으면 먼저 config를 만든다.
- `url: undefined` 에러가 나면 `dotenv`의 `config()` 호출이 `drizzle.config.ts` export 이전에 실행되는지 확인한다.
- 매 요청마다 `drizzle()`를 호출하면 singleton 패턴으로 바꾼다.
- edge runtime에서 `pg` Pool을 쓰려 하면 driver 선택부터 다시 본다.

실제 적용 전에는 [project-setup](./references/project-setup.md)과 [connection-management](./references/connection-management.md)를 먼저 읽는다.

### 2. 스키마는 relation과 query path를 기준으로 설계한다

Drizzle schema는 TypeScript 코드로 선언하는 테이블 정의이자 타입 추론의 원천이다. relation, identifier, uniqueness, index, naming을 명시적으로 설계해야 런타임과 migration이 안정적이다.

- column type은 dialect별 import(`drizzle-orm/pg-core`, `drizzle-orm/mysql-core`, `drizzle-orm/sqlite-core`)에서 가져온다. dialect 간 type 차이를 확인한다.
- 관계는 `relations()` helper로 선언한다. foreign key는 schema에서 `.references()`로 명시하되, 관계 query를 위한 `relations()` 정의를 별도로 둔다.
- `$inferSelect`와 `$inferInsert`로 타입을 추론한다. 별도 interface를 수동으로 만들지 않는다.
- 조회 경로가 반복되는 field에는 index를 건다. foreign key column에는 index를 기본으로 추가한다.
- payload나 lifecycle이 있는 many-to-many는 explicit junction table을 우선 검토한다.

#### 빠른 판단 기준

- foreign key column에 index가 없으면 schema 단계에서 성능 문제가 이미 시작된 것이다.
- JSON column에 `any` 또는 `unknown`을 쓰면 `.$type<T>()`로 타입을 좁히거나 Zod 검증을 건다.
- 간단한 many-to-many에 메타데이터를 붙이기 시작하면 junction table로 바꾼다.
- column type mapping(PostgreSQL/MySQL/SQLite → TypeScript)이 확실하지 않으면 reference를 먼저 확인한다.

실제 적용 전에는 [schema-design](./references/schema-design.md)을 먼저 읽는다. 고급 패턴(custom type, enum, composite key, multi-tenant, generated column)은 [advanced-schemas](./references/advanced-schemas.md)를 읽는다.

### 3. migration은 배포 계약으로 다룬다

`drizzle-kit generate`는 단순한 파일 생성 명령이 아니라 배포 가능한 데이터 변경 계약이다. 개발용 push 흐름과 운영용 generate/migrate 흐름을 섞지 않는다.

- 개발과 운영 모두 `drizzle-kit generate` → SQL review → `drizzle-kit migrate`를 기본값으로 둔다.
- `drizzle-kit push`는 prototype, throwaway dev DB, 빠른 iteration에서만 허용한다.
- 생성된 SQL을 반드시 리뷰한다. Drizzle은 column rename을 drop + add로 생성할 수 있으므로 데이터 유실 위험이 있다.
- nullable 추가 → backfill → not null 강화 같은 expand-migrate-contract 순서를 우선 검토한다.
- CI/CD에서는 `drizzle-kit migrate`를 명시적 환경변수 로딩과 함께 실행한다.

#### 빠른 판단 기준

- column rename이면 생성된 SQL이 DROP + ADD가 아닌 RENAME인지 직접 확인하고, 아니면 수동 수정한다.
- `push`가 운영 배포 경로에 포함되어 있으면 `generate` + `migrate`로 바꾼다.
- migration drift를 무시하고 schema만 계속 고치면 배포 시점에 더 크게 깨진다.
- `.env` 로딩이 되지 않아 `url: undefined`가 나면 `drizzle.config.ts`의 dotenv 설정을 먼저 본다.

실제 적용 전에는 [migrations](./references/migrations.md)를 먼저 읽는다.

### 4. query는 필요한 shape만 가져오도록 설계한다

Drizzle의 SQL-like API는 직관적이지만 over-fetching과 N+1을 숨기기 쉽다.

- 기본값은 `select()`에 필요한 column만 지정하는 것이다. 전체 column을 가져오는 `.select()`는 큰 테이블에서 피한다.
- relation data가 필요하면 `db.query.*.findMany({ with: { ... } })`를 사용한다. loop 안에서 관계 query를 다시 날리면 N+1로 본다.
- list query에는 stable `orderBy`와 pagination을 같이 정한다. OFFSET pagination보다 cursor-based pagination이 대량 데이터에서 안정적이다.
- `sql` template tag를 사용한 raw SQL은 parameterized query로 작성한다. string concatenation으로 SQL을 만들면 SQL injection 위험이다.
- 복잡한 aggregation은 `sql` template이나 CTE(`$with`)를 검토한다.

#### 빠른 판단 기준

- `findMany()` 후 loop 안에서 relation query를 다시 날리면 N+1이다.
- pagination 없이 무제한 list query를 반환하면 API와 DB 둘 다 불안정해진다.
- raw SQL을 string concatenation으로 만들면 `sql` template으로 바꾼다.
- `select()` 호출에 column 지정 없이 큰 테이블에서 전체를 가져오면 먼저 줄인다.
- multi-step data modification에 transaction을 쓰지 않으면 transaction으로 감싼다.

실제 적용 전에는 [query-patterns](./references/query-patterns.md)를 먼저 읽는다.

### 5. transaction과 connection lifecycle을 따로 본다

transaction correctness와 connection stability는 서로 다른 문제다. Pool만 잘 설정해도 비원자적 쓰기는 막지 못하고, transaction만 잘 써도 Pool이 터질 수 있다.

- 프로세스당 drizzle instance와 Pool은 가능한 한 하나로 재사용한다.
- Pool 설정(max, idleTimeoutMillis, connectionTimeoutMillis)은 driver 기준으로 잡는다.
- 독립 쿼리 묶음이면 `db.transaction()` 안에서 순차 실행하고, 실패 시 자동 rollback을 활용한다.
- transaction 안에서는 네트워크 I/O나 긴 business logic을 피한다.
- serverless 환경이면 connection reuse 패턴과 HTTP-based driver(postgres-js 등)를 먼저 본다.
- graceful shutdown(SIGTERM/SIGINT)에서 `pool.end()`를 호출한다.

#### 빠른 판단 기준

- 매 요청마다 새 Pool이나 drizzle instance를 만들면 connection lifecycle부터 고친다.
- HTTP-based driver(Neon HTTP, postgres-js in serverless mode)에서 transaction을 쓰려 하면 driver 제약을 먼저 확인한다.
- Pool max를 기본값(10)으로 두고 있는데 동시 접속이 잦으면 Pool 설정을 다시 본다.
- serverless/edge 맥락이면 Pool보다 single connection이나 HTTP driver를 먼저 검토한다.

실제 적용 전에는 [connection-management](./references/connection-management.md)와 [performance](./references/performance.md)를 먼저 읽는다.

### 6. provider별 setup과 예외 경로를 분기한다

Drizzle 문제의 상당수는 schema가 아니라 provider와 runtime 조합에서 생긴다. driver import path, Pool 설정, migration runner가 provider마다 다르므로 먼저 분기하면 시행착오를 줄인다.

- PostgreSQL + Node.js: `drizzle-orm/node-postgres` + `pg` Pool을 기본값으로 둔다.
- PostgreSQL + serverless/edge: `drizzle-orm/postgres-js` + `postgres`를 기본값으로 둔다.
- Neon: HTTP adapter(`drizzle-orm/neon-http`)와 WebSocket adapter(`drizzle-orm/neon-serverless`)를 환경에 따라 분기한다.
- MySQL: `drizzle-orm/mysql2` + `mysql2/promise`를 기본값으로 둔다.
- SQLite: `drizzle-orm/better-sqlite3`를 기본값으로 둔다. Turso/libSQL이면 `drizzle-orm/libsql`을 쓴다.
- PlanetScale이나 Turso처럼 provider nuance가 큰 환경은 일반 SQL 가정으로 뭉개지 않는다.

#### 빠른 판단 기준

- `drizzle-orm/node-postgres`와 `drizzle-orm/postgres-js`를 혼동하면 import path부터 다시 본다.
- edge runtime에서 `pg` Pool import가 보이면 driver 선택이 맞는지 확인한다.
- Neon을 쓰는데 adapter 선택이 불분명하면 환경(Node.js vs edge)부터 먼저 확인한다.
- SQLite에서 enum, scalar list, write concurrency가 필요하면 dialect 제약을 먼저 본다.

실제 적용 전에는 [connection-management](./references/connection-management.md)를 읽고, Neon 환경이면 [neon](./references/neon.md)을 추가로 읽는다.

---

## 엣지케이스

### HTTP-based driver에서 transaction 제약

Neon HTTP adapter나 일부 serverless driver는 persistent connection이 없어 transaction을 지원하지 않는다. transaction이 필요하면 WebSocket adapter나 node-postgres로 전환하거나, application-level 보상 로직을 검토한다.

### Drizzle은 column rename을 drop + add로 생성할 수 있다

schema에서 column 이름을 바꾸면 `drizzle-kit generate`가 DROP + ADD SQL을 만들어 데이터가 날아갈 수 있다. rename이면 생성된 SQL을 반드시 확인하고, 필요하면 `ALTER TABLE ... RENAME COLUMN`으로 수동 수정한다.

### `select()` 없이 전체 column을 가져오는 패턴

Drizzle에서 `db.select().from(table)`은 전체 column을 가져온다. 큰 테이블에서 이 패턴이 반복되면 필요한 column만 지정하는 것이 안전하다.

### Prisma와 Drizzle 병행

기존 Prisma 프로젝트에 Drizzle을 점진적으로 도입하는 경우, naming 충돌(prismaDb vs drizzleDb)과 migration 충돌을 분리하고 coexistence 패턴을 따른다.

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/project-setup.md](./references/project-setup.md) | 신규 프로젝트 setup, 기존 프로젝트 통합, drizzle.config.ts, package.json scripts를 잡을 때 |
| [references/connection-management.md](./references/connection-management.md) | drizzle() 인스턴스, Pool 설정, singleton, graceful shutdown, driver 선택 매트릭스를 볼 때 |
| [references/schema-design.md](./references/schema-design.md) | column types, relations, indexes, junction table, type 추론, schema 수정 패턴을 볼 때 |
| [references/advanced-schemas.md](./references/advanced-schemas.md) | custom type, enum, composite key, check constraint, generated column, multi-tenant, DB별 특화 기능을 볼 때 |
| [references/migrations.md](./references/migrations.md) | migration lifecycle, env loading, CI/CD, advanced patterns(data migration, rename, rollback)을 볼 때 |
| [references/query-patterns.md](./references/query-patterns.md) | CRUD, filtering, joins, relations query, aggregation, CTE, raw SQL, prepared statement, batch, locking을 볼 때 |
| [references/performance.md](./references/performance.md) | connection pooling, query optimization, edge runtime, caching, batch, read replica, monitoring을 볼 때 |
| [references/troubleshooting.md](./references/troubleshooting.md) | migration 에러, connection 에러, type 에러, query 에러, 환경변수 문제를 디버깅할 때 |
| [references/neon.md](./references/neon.md) | Neon 환경 setup, HTTP vs WebSocket adapter 선택, Neon 전용 troubleshooting을 볼 때 |
| [references/vs-prisma.md](./references/vs-prisma.md) | Drizzle vs Prisma 비교, migration 가이드, 선택 기준을 볼 때 |

### 추천 로드 순서

- 신규 setup: `project-setup → connection-management → schema-design → migrations`
- schema 변경: `schema-design → migrations → query-patterns`
- query 최적화: `query-patterns → performance → connection-management`
- Neon 환경: `neon → connection-management`
- Prisma에서 전환: `vs-prisma → project-setup → schema-design`
- 트러블슈팅: `troubleshooting`

---

## 범위

- REST API contract, status code, error envelope, OpenAPI 3.1 설계 → `be-api-design`
- Fastify plugin, route, validation, hook, logging 구현 → `fastify-best-practices`
- auth, authorization, input validation, exploitability 검토 → `dev-security`
- Prisma 기반 persistence → `be-prisma`
- Kysely 기반 raw SQL query 빌더 → `be-kysely`
- DB 서버 운영, 인프라 레벨 connection pooler, replication, backup 정책 → 별도 DB/infra 가이드
