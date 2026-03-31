---
name: be-prisma
description: "Prisma ORM 스키마 설계, relation modeling, migrations, query optimization, transactions, driver adapters, provider setup, and Prisma v7 migration을 위한 스킬이다. Use this skill when working on schema.prisma, adding or refactoring Prisma models, choosing relation patterns, wiring PrismaClient, configuring PostgreSQL/MySQL/SQLite/SQL Server/CockroachDB/Prisma Postgres, fixing migration drift, or upgrading from Prisma v6 to v7. Always consult this skill for Prisma-backed persistence work, even if the user only asks to 'add a table', 'connect the database', 'fix a Prisma error', or 'wire the client'. For REST API contract design use be-api-design. For raw SQL-heavy access patterns or query-builder-first codebases use kysely. Triggers on: prisma, schema.prisma, PrismaClient, prisma migrate, prisma generate, driver adapter, prisma.config.ts, relation modeling, query optimization, transaction, Prisma 7, PostgreSQL, MySQL, SQLite, SQL Server, CockroachDB, Prisma Postgres, 프리즈마, 스키마 설계, 마이그레이션, 드라이버 어댑터, DB 연결."
disable-model-invocation: false
user-invocable: false
---

# Prisma ORM 설계 & 운영 (be-prisma)

## 목표

Prisma를 단순 ORM wrapper가 아니라 schema, relation, migration, query, runtime configuration까지 포함한 persistence contract로 다룬다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 작업을 시작하기 전에는 현재 문제에 맞는 reference 문서를 먼저 읽고, 훈련 데이터 기반 추측보다 로컬 reference를 우선 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 기본선

- Prisma v7을 기본값으로 둔다.
- Node.js 20.19.0+, TypeScript 5.4.0+, ESM 환경을 기본 전제로 둔다.
- `prisma-client` generator, explicit `output`, `prisma.config.ts`, manual env loading, driver adapter 구성을 기본 경로로 본다.
- `new PrismaClient()`만 단독으로 두는 v6 스타일은 경고 신호로 본다. v7에서는 보통 adapter 또는 `accelerateUrl`이 필요하다.
- MongoDB는 Prisma v7 메인라인에서 지원되지 않으므로, MongoDB 작업이면 v6 예외 경로로 분기한다.
- Prisma v7에서는 migrate 이후 auto-generate, auto-seed, middleware 같은 과거 습관이 그대로 성립하지 않는다고 가정한다.

---

## 핵심 단계

### 1. 런타임 기준선을 먼저 고정한다

schema를 바꾸기 전에 현재 프로젝트가 Prisma v7 runtime contract를 만족하는지 확인한다. generator, output path, module system, env loading, adapter wiring이 흔들리면 그 뒤의 schema 작업도 쉽게 어긋난다.

- `schema.prisma`의 generator가 `prisma-client-js`면 legacy 경로로 본다.
- `prisma.config.ts`가 없는데 v7 전환을 말하고 있으면 먼저 config surface부터 만든다.
- generated client import path가 `@prisma/client`에 고정돼 있으면 v6 흔적일 가능성이 높다.
- `prisma://` 또는 `prisma+postgres://` URL을 direct adapter에 넣고 있으면 Accelerate/Prisma Postgres 경로를 다시 본다.

#### 빠른 판단 기준

- `new PrismaClient()`만 보이고 adapter가 안 보이면 v7 wiring을 재검토한다.
- `url = env("DATABASE_URL")`가 아직 `schema.prisma` datasource에 남아 있으면 `prisma.config.ts`로 옮길지 먼저 판단한다.
- `.env` 자동 로딩을 전제로 한 설명은 v7 문맥에서 그대로 복사하지 않는다.

실제 적용 전에는 [schema-changes](./references/schema-changes.md), [driver-adapters](./references/driver-adapters.md), [prisma-config](./references/prisma-config.md), [env-variables](./references/env-variables.md), [esm-support](./references/esm-support.md)를 먼저 읽는다.

### 2. 스키마는 relation과 query path를 기준으로 설계한다

Prisma schema는 테이블 선언 모음이 아니라 애플리케이션이 실제로 읽고 쓰는 관계 모델이다. relation, identifier, uniqueness, index, naming mapping을 명시적으로 설계해야 런타임과 migration이 안정적이다.

- 다중 관계나 의미가 갈리는 관계는 named relation으로 명시한다.
- foreign key field와 `references`는 숨기지 않고 드러낸다.
- 조회 경로가 반복되는 field는 `@@index`나 `@@unique`까지 같이 본다.
- payload나 lifecycle이 있는 many-to-many는 explicit join table을 우선 검토한다.
- Prisma model 이름은 읽기 좋은 도메인 이름으로 두고, 물리 테이블 이름과 어긋나면 `@@map`이나 `@map`으로 분리한다.

#### 빠른 판단 기준

- relation field는 있는데 foreign key scalar field가 없다면 model shape를 다시 본다.
- 자주 조회되는 `where`와 `orderBy` 조합에 index가 없으면 schema 단계에서 성능 문제가 이미 시작된 것이다.
- 간단한 implicit many-to-many에 메타데이터를 붙이기 시작하면 explicit join table로 바꾼다.

실제 적용 전에는 [schema-design](./references/schema-design.md)을 먼저 읽는다.

### 3. migration은 배포 계약으로 다룬다

`prisma migrate`는 단순한 파일 생성 명령이 아니라 배포 가능한 데이터 변경 계약이다. 개발용 reset 흐름과 운영용 deploy 흐름을 섞지 않는다.

- 개발에서는 `prisma migrate dev`, 운영에서는 `prisma migrate deploy`를 기본값으로 둔다.
- `prisma migrate reset`은 개발용 파괴 명령으로 취급한다.
- `db push`는 prototype, throwaway dev DB, MongoDB 같은 제한된 맥락에서만 허용한다.
- nullable 추가 → backfill → not null 강화 같은 expand-migrate-contract 순서를 우선 검토한다.

#### 빠른 판단 기준

- production 경로에서 `migrate dev`를 제안하면 잘못된 플로우로 본다.
- 필드 rename이나 type change를 한 migration에 한 번에 밀어 넣으면 rollback과 data safety 관점에서 재설계한다.
- migration drift를 무시하고 schema만 계속 고치면 결국 deploy 시점에 더 크게 깨진다.

실제 적용 전에는 [migrations](./references/migrations.md)를 먼저 읽는다.

### 4. query는 필요한 shape만 가져오도록 설계한다

Prisma query는 작성이 쉬워서 over-fetching과 N+1을 숨기기 쉽다. relation을 읽을 때는 `include`만 늘리기보다 필요한 field shape를 먼저 고정한다.

- 기본값은 `select`다. `include`는 필요한 relation을 함께 가져와야 할 때만 쓴다.
- list query는 stable `orderBy`와 pagination 전략을 같이 정한다.
- 개발 환경에서는 query logging이나 slow query 관찰 경로를 열어 둔다.
- 복잡한 aggregation이나 Prisma가 어색한 SQL은 `$queryRaw`로 내려가되, raw SQL을 기본값으로 삼지 않는다.

#### 빠른 판단 기준

- `findMany()` 후 loop 안에서 relation query를 다시 날리면 N+1로 본다.
- 응답에서 실제로 안 쓰는 relation을 `include`하고 있으면 먼저 줄인다.
- pagination 없이 무제한 list query를 반환하면 API surface와 DB 둘 다 불안정해진다.

실제 적용 전에는 [query-optimization](./references/query-optimization.md)을 먼저 읽는다.

### 5. transaction과 connection lifecycle을 따로 본다

transaction correctness와 connection stability는 서로 다른 문제다. `$transaction`만 잘 써도 pool이 터질 수 있고, singleton만 만들어도 비원자적 쓰기는 막지 못한다.

- 프로세스당 Prisma client instance는 가능한 한 하나로 재사용한다.
- adapter pool 설정은 v6의 DATABASE_URL 옵션과 동일하지 않을 수 있으므로 driver 기준으로 다시 본다.
- 독립 쿼리 묶음이면 array transaction, 중간 검증이 있으면 interactive transaction을 쓴다.
- transaction 안에서는 네트워크 I/O나 긴 business logic을 피한다.
- 충돌 가능성이 큰 업데이트는 optimistic concurrency나 retry 전략을 함께 본다.

#### 빠른 판단 기준

- 매 요청마다 `new PrismaClient()`를 만들면 connection lifecycle부터 고친다.
- interactive transaction 안에서 외부 API 호출을 하거나 오래 대기하면 구조를 다시 잡는다.
- serverless나 edge 문맥이면 adapter 선택과 runtime 제약을 먼저 본다.

실제 적용 전에는 [transactions](./references/transactions.md)와 [connection-management](./references/connection-management.md)를 먼저 읽는다.

### 6. provider별 setup과 예외 경로를 분기한다

Prisma 문제의 상당수는 schema가 아니라 provider와 runtime 조합에서 생긴다. provider setup, adapter choice, Prisma Postgres/Accelerate, MongoDB legacy 경로를 먼저 분기하면 시행착오를 줄일 수 있다.

- PostgreSQL, MySQL, SQLite, SQL Server, CockroachDB, Prisma Postgres는 v7 mainline provider reference를 따른다.
- Prisma Postgres와 Accelerate는 direct adapter path와 `accelerateUrl` path를 구분한다.
- MongoDB는 v6 legacy reference로만 안내한다.

#### 빠른 판단 기준

- direct DB URL인지 Accelerate URL인지 헷갈리면 adapter wiring부터 멈추고 다시 확인한다.
- SQLite는 간편하지만 enum, scalar list, write concurrency 제약이 있으니 기능 요구를 먼저 본다.
- PlanetScale나 CockroachDB처럼 provider nuance가 큰 환경은 일반 SQL 가정으로 뭉개지 않는다.

실제 적용 전에는 [prisma-client-setup](./references/prisma-client-setup.md)와 해당 provider reference, 필요 시 [accelerate-users](./references/accelerate-users.md)를 함께 읽는다.

---

## 엣지케이스

### MongoDB는 v7 기본선에서 제외한다

MongoDB는 Prisma v7 메인라인에서 지원되지 않는다. MongoDB를 계속 써야 한다면 v6 generator와 `db push` 중심 경로로 분기한다.

### Prisma Postgres와 Accelerate는 direct adapter와 다르게 다룬다

`prisma://` 또는 `prisma+postgres://` URL은 direct TCP adapter에 그대로 넣지 않는다. 이 경로는 `accelerateUrl` 또는 Prisma Postgres 전용 adapter/extension path를 먼저 확인한다.

### SQLite URL 해석 기준이 달라질 수 있다

Prisma v7에서는 SQLite datasource URL이 config 파일 기준으로 해석될 수 있다. schema 기준 상대 경로라고 단정하지 않는다.

### v7에서는 과거 client middleware와 자동 동작을 기대하지 않는다

middleware는 client extensions로 옮기고, auto-generate와 auto-seed는 명시적 명령으로 바꾼다.

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/prisma-client-setup.md](./references/prisma-client-setup.md) | generator, output, generated client import, single-instance 기본선을 잡을 때 |
| [references/postgresql.md](./references/postgresql.md) | PostgreSQL setup, URL, adapter, schema nuance를 볼 때 |
| [references/mysql.md](./references/mysql.md) | MySQL 또는 MariaDB setup, PlanetScale 분기를 볼 때 |
| [references/sqlite.md](./references/sqlite.md) | SQLite 또는 Turso/libSQL setup와 제약을 확인할 때 |
| [references/sqlserver.md](./references/sqlserver.md) | SQL Server나 Azure SQL setup를 확인할 때 |
| [references/cockroachdb.md](./references/cockroachdb.md) | CockroachDB provider와 PostgreSQL adapter 조합을 볼 때 |
| [references/prisma-postgres.md](./references/prisma-postgres.md) | Prisma Postgres managed setup와 direct TCP 경로를 볼 때 |
| [references/mongodb.md](./references/mongodb.md) | MongoDB legacy v6 exception path를 확인할 때 |
| [references/schema-design.md](./references/schema-design.md) | relation, index, join table, naming, mapping 설계를 볼 때 |
| [references/migrations.md](./references/migrations.md) | dev/deploy migration flow, drift, destructive change safety를 볼 때 |
| [references/query-optimization.md](./references/query-optimization.md) | over-fetching, N+1, pagination, query logging, raw SQL fallback를 볼 때 |
| [references/transactions.md](./references/transactions.md) | array transaction, interactive transaction, OCC, retry를 볼 때 |
| [references/connection-management.md](./references/connection-management.md) | singleton, pool tuning, serverless/edge, SSL 설정을 볼 때 |
| [references/review-checklist.md](./references/review-checklist.md) | schema, query, migration, runtime review 포인트를 빠르게 훑을 때 |
| [references/schema-changes.md](./references/schema-changes.md) | v6에서 v7 generator와 datasource surface를 바꿀 때 |
| [references/driver-adapters.md](./references/driver-adapters.md) | v7 adapter matrix와 provider별 wiring을 확인할 때 |
| [references/prisma-config.md](./references/prisma-config.md) | `prisma.config.ts` 구조, `directUrl`, `shadowDatabaseUrl`, seed 설정을 볼 때 |
| [references/env-variables.md](./references/env-variables.md) | v7 manual env loading, CI, dotenv path를 정리할 때 |
| [references/esm-support.md](./references/esm-support.md) | ESM-only 제약, tsconfig, CommonJS boundary를 정리할 때 |
| [references/removed-features.md](./references/removed-features.md) | middleware, metrics, removed flags, auto behaviors 제거를 마이그레이션할 때 |
| [references/accelerate-users.md](./references/accelerate-users.md) | Prisma Accelerate 또는 `prisma://` URL을 쓰는 환경을 다룰 때 |

### 추천 로드 순서

- 신규 setup: `prisma-client-setup → provider 문서 → driver-adapters → prisma-config`
- schema 변경: `schema-design → migrations → query-optimization`
- v6에서 v7 업그레이드: `schema-changes → driver-adapters → prisma-config → env-variables → esm-support → removed-features`
- 성능/런타임 이슈: `query-optimization → connection-management → transactions`
- Prisma Postgres/Accelerate: `prisma-postgres → accelerate-users`
- MongoDB: `mongodb`만 읽고 v6 예외 경로로 처리

---

## 응답 패턴

이 스킬로 답할 때는 아래 순서를 기본으로 둔다.

1. Runtime baseline: Prisma version, module system, generator, output path, adapter 또는 `accelerateUrl` 경로
2. Data model or query decision: model, field, relation, index, query shape, pagination, transaction choice
3. Setup or migration steps: 변경할 파일, CLI commands, env/config 이동, provider-specific notes
4. Risks: data loss, migration ordering, provider caveats, unsupported paths, runtime constraints
5. Verification: `prisma validate`, `prisma generate`, `prisma migrate status`, targeted query/log checks

구현 요청이 섞여 있어도 먼저 runtime baseline과 schema/migration contract를 잠근 뒤, 코드 예시를 작성한다.

---

## 범위

- REST API contract, status code, error envelope, OpenAPI 3.1 설계 → `be-api-design`
- Fastify plugin, route, validation, hook, logging 구현 → `fastify-best-practices`
- auth, authorization, input validation, exploitability 검토 → `dev-security`
- raw SQL-first 접근, query builder 중심 코드베이스, Prisma 대체 검토 → `kysely`
- DB 서버 운영, 인프라 레벨 connection pooler, replication, backup 정책 → 별도 DB/infra 가이드