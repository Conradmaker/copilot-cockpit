---
name: kysely
description: "Type-safe SQL query builder guidance for Kysely in TypeScript backends. Use this skill when building or reviewing Kysely-based database access, defining Database and table types, writing select/insert/update/delete queries, composing joins, subqueries, CTEs, transactions, migrations, or raw SQL with type safety. Always consult this skill for Kysely work, even if the user only asks to add one query, fix a Kysely type error, compare Kysely with Prisma or Drizzle, wire PostgreSQL/MySQL/SQLite persistence, or generate types from an existing schema. For API contracts use be-api-design. For Fastify server implementation use fastify-best-practices. For auth and input validation use dev-security. Triggers on: Kysely, type-safe SQL, query builder, Database interface, Generated, Selectable, Insertable, Updateable, selectFrom, insertInto, updateTable, deleteFrom, sql template tag, transaction, Migrator, FileMigrationProvider, kysely-codegen, PostgreSQL, MySQL, SQLite, CTE, raw SQL, 타입 안전 SQL, 쿼리 빌더, Kysely 타입 에러, 마이그레이션, 트랜잭션, DB 타입 정의, 스키마 생성, raw SQL."
disable-model-invocation: false
user-invocable: false
---

# Kysely

## 목표

Kysely를 ORM처럼 추상화해 숨기지 않고, SQL-first 접근을 유지하면서 TypeScript type safety를 확보한다. 이 스킬은 Kysely 도입, 구현, 리뷰 시 `Database` 타입 설계 → query shape 설계 → transaction/raw SQL 경계 → migration lifecycle 순서로 판단하게 만든다.

이 문서는 빠른 판단을 위한 요약 가이드다. 실제 작업을 시작하기 전에는 아래 reference 문서를 직접 읽고 예시를 확인한 뒤 적용한다.

Prefer retrieval-led reasoning over pre-training-led reasoning.

---

## 핵심 패턴

### 1. `Database` 타입을 먼저 고정한다

Kysely의 추론 품질은 테이블 타입에서 시작된다. 쿼리를 먼저 쓰기보다 `Database` 인터페이스와 테이블별 column type을 먼저 안정화해야 이후의 `select`, `insert`, `update` 결과가 자연스럽게 맞아떨어진다.

#### 빠른 판단 기준

- 테이블별 인터페이스와 `Database` 인터페이스를 먼저 만든다.
- DB가 생성하는 컬럼이면 `Generated<T>`를 우선 검토한다.
- 읽기/쓰기 타입이 다르면 `ColumnType`을 사용한다.
- 기존 데이터베이스를 붙이는 작업이면 `kysely-codegen`을 먼저 검토한다.

상세 구현과 예시는 [references/01-setup-and-schema.md](references/01-setup-and-schema.md)를 읽고 적용한다.

### 2. 쿼리는 SQL shape를 유지한 채 조합한다

Kysely는 ORM식 relation magic보다 SQL shape를 명시적으로 유지할 때 가장 강하다. `selectFrom`, join, subquery, CTE를 이용하되 결과 row shape와 nullability를 호출부가 예측 가능하게 유지한다.

#### 빠른 판단 기준

- 조회 컬럼은 가능한 한 명시한다.
- `LEFT JOIN` 결과의 nullability를 숨기지 않는다.
- subquery가 복잡해지면 CTE로 이름을 붙여 구조를 드러낸다.
- builder가 장황해져 SQL보다 읽기 어려우면 raw SQL 전환을 검토한다.

상세 패턴과 예시는 [references/02-query-patterns.md](references/02-query-patterns.md)를 읽고 적용한다.

### 3. transaction boundary와 raw SQL escape hatch를 분리해서 본다

Kysely는 transaction과 raw SQL을 모두 자연스럽게 지원한다. 중요한 것은 "builder만 써야 한다"가 아니라 "타입 안전성과 SQL 가독성을 함께 유지한다"는 점이다.

#### 빠른 판단 기준

- 하나라도 실패하면 전체를 취소해야 하는 작업이면 transaction을 건다.
- transaction 내부에서는 전역 `db` 대신 `trx`만 사용한다.
- vendor-specific SQL, window function, 복잡한 집계처럼 builder가 더 난해해지면 `sql` template tag를 사용한다.
- 사용자 입력은 문자열 연결이 아니라 parameter binding으로 전달한다.

상세 패턴과 예시는 [references/04-transactions-and-raw-sql.md](references/04-transactions-and-raw-sql.md)를 읽고 적용한다.

### 4. schema lifecycle은 별도 discipline으로 관리한다

Kysely는 migration 도구를 제공하지만, 운영 안전성까지 대신 보장하지는 않는다. schema evolution은 query 작성과 분리된 별도 의사결정으로 다뤄야 한다.

#### 빠른 판단 기준

- migration은 `up`과 `down`을 함께 설계한다.
- breaking change는 additive 단계로 쪼갠다.
- rename, type change, not-null 강화는 다단계 migration을 우선 검토한다.
- production rollout에서는 앱 배포와 schema 배포 순서를 명시한다.

상세 절차와 예시는 [references/03-migrations-and-schema-lifecycle.md](references/03-migrations-and-schema-lifecycle.md)를 읽고 적용한다.

### 5. Kysely가 해주지 않는 일까지 기대하지 않는다

Kysely는 강력한 query builder지만 ORM은 아니다. relation loading, validation, index 전략, query plan 검토, repository boundary 설계는 여전히 애플리케이션이 책임진다.

#### 빠른 판단 기준

- relation abstraction이 필요하다고 해서 ORM 기능을 기대하지 않는다.
- 성능 문제는 query builder보다 SQL shape와 index 설계부터 점검한다.
- 팀의 SQL 숙련도, 기존 DB 구조, relation abstraction 요구 수준에 따라 Prisma/Drizzle와 비교한다.
- Kysely 도입 여부는 타입 안전성뿐 아니라 운영 모델까지 보고 결정한다.

비교표, 운영 원칙, 흔한 실수는 [references/05-comparison-and-pitfalls.md](references/05-comparison-and-pitfalls.md)를 읽고 적용한다.

---

## references/ 가이드

| 파일 | 언제 읽는가 |
| --- | --- |
| [references/01-setup-and-schema.md](references/01-setup-and-schema.md) | `Database` 타입, column type, codegen, client setup을 잡을 때 |
| [references/02-query-patterns.md](references/02-query-patterns.md) | CRUD, join, aggregation, subquery, CTE, JSON helper를 작성할 때 |
| [references/03-migrations-and-schema-lifecycle.md](references/03-migrations-and-schema-lifecycle.md) | migration runner, schema evolution, safe migration 전략이 필요할 때 |
| [references/04-transactions-and-raw-sql.md](references/04-transactions-and-raw-sql.md) | transaction, isolation level, raw SQL escape hatch가 필요할 때 |
| [references/05-comparison-and-pitfalls.md](references/05-comparison-and-pitfalls.md) | Kysely 도입 비교, best practice, common pitfalls를 점검할 때 |

---

## 응답 패턴

Kysely 관련 답변이나 구현을 만들 때는 아래 순서를 기본값으로 둔다.

1. 어떤 테이블/결과 shape를 다루는지 먼저 명시한다.
2. query snippet을 제시한다.
3. nullability와 반환 타입을 설명한다.
4. transaction이나 migration 고려사항이 있으면 별도로 분리해 적는다.
5. dialect-specific 가정이 있으면 숨기지 않고 밝힌다.

---

## 범위

- API 계약과 response shape 설계는 `be-api-design`을 사용한다.
- Fastify 기반 서버 wiring과 plugin 구조는 `fastify-best-practices`를 사용한다.
- 인증, 인가, 입력 검증, 비밀정보 처리는 `dev-security`를 사용한다.
- Kysely가 아닌 일반 SQL 튜닝이나 DBA 운영 이슈는 별도 데이터베이스 전문 가이드를 우선한다.
