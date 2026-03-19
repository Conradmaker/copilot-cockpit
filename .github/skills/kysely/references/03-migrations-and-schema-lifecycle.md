# Kysely 마이그레이션과 스키마 수명주기

## 언제 읽는가

- migration runner를 붙일 때
- 새 테이블/컬럼 추가, 변경, 제거를 설계할 때
- zero-downtime에 가까운 안전한 schema evolution이 필요할 때

---

## 1. Migration provider 설정

```ts
import {FileMigrationProvider, Migrator} from "kysely";
import {promises as fs} from "fs";
import path from "path";

const migrator = new Migrator({
  db,
  provider: new FileMigrationProvider({
    fs,
    path,
    migrationFolder: path.join(__dirname, "migrations"),
  }),
});
```

실행 예시:

```ts
async function migrateToLatest() {
  const {error, results} = await migrator.migrateToLatest();

  results?.forEach((item) => {
    if (item.status === "Success") {
      console.log(`Migration "${item.migrationName}" executed successfully`);
    }

    if (item.status === "Error") {
      console.error(`Migration "${item.migrationName}" failed`);
    }
  });

  if (error) {
    console.error("Migration failed", error);
    process.exit(1);
  }
}
```

### 빠른 판단 기준

- 애플리케이션 부트 과정과 migration 실행을 무조건 섞지 않는다.
- 배포 파이프라인에서 migration 실행 시점과 rollback 절차를 먼저 정한다.
- migration 실패 시 프로세스를 계속 띄우지 않는다.

---

## 2. 기본 migration 파일 패턴

```ts
import {Kysely, sql} from "kysely";

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable("users")
    .addColumn("id", "serial", (col) => col.primaryKey())
    .addColumn("email", "varchar(255)", (col) => col.notNull().unique())
    .addColumn("name", "varchar(255)")
    .addColumn("created_at", "timestamp", (col) =>
      col.defaultTo(sql`CURRENT_TIMESTAMP`).notNull()
    )
    .execute();

  await db.schema
    .createIndex("users_email_idx")
    .on("users")
    .column("email")
    .execute();
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable("users").execute();
}
```

### 빠른 판단 기준

- `up`과 `down`을 함께 설계한다.
- 인덱스 생성 여부를 테이블 생성과 같이 검토한다.
- DB vendor별 문법 차이가 큰 부분은 `sql` escape hatch를 허용한다.

---

## 3. 흔한 변경 패턴

### Foreign key 추가

```ts
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable("posts")
    .addColumn("id", "serial", (col) => col.primaryKey())
    .addColumn("user_id", "integer", (col) =>
      col.references("users.id").onDelete("cascade").notNull()
    )
    .addColumn("title", "varchar(500)", (col) => col.notNull())
    .addColumn("content", "text")
    .execute();
}
```

### 테이블 수정

```ts
export async function up(db: Kysely<any>): Promise<void> {
  await db.schema.alterTable("users").addColumn("bio", "text").execute();
}
```

### PostgreSQL enum 추가

```ts
import {sql} from "kysely";

export async function up(db: Kysely<any>): Promise<void> {
  await sql`CREATE TYPE user_role AS ENUM ('admin', 'user', 'guest')`.execute(db);

  await db.schema
    .alterTable("users")
    .addColumn("role", sql`user_role`, (col) => col.defaultTo("user"))
    .execute();
}
```

---

## 4. 안전한 마이그레이션 원칙

### 기본 원칙

1. backward compatible하게 나눈다.
2. 가능한 한 reversible하게 만든다.
3. big-bang 변경보다 작은 단계로 쪼갠다.
4. 앱 배포와 스키마 배포의 순서를 의식한다.

### 추천 패턴

- 컬럼 이름 변경: 새 컬럼 추가 → 데이터 복사 → 앱 전환 → 기존 컬럼 제거
- nullable -> not null: 컬럼 추가 또는 backfill 완료 후 별도 migration에서 제약 강화
- 타입 변경: 새 컬럼 추가 → 변환 복사 → 읽기 경로 전환 → 구 컬럼 제거

예시:

```ts
import {sql} from "kysely";

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .alterTable("users")
    .addColumn("full_name", "varchar(255)")
    .execute();

  await db
    .updateTable("users")
    .set({
      full_name: sql`concat(first_name, ' ', last_name)`,
    })
    .execute();
}
```

---

## 5. 테스트와 운영 체크리스트

- 로컬 또는 staging에서 `up`과 `down`을 모두 검증한다.
- 대량 테이블이면 lock, rewrite, index build 비용을 먼저 본다.
- destructive migration은 백업/rollback 전략을 준비한다.
- 애플리케이션이 구/신 스키마 모두와 잠시 공존할 수 있는지 확인한다.

Kysely는 migration 도구를 제공하지만, production rollout 전략을 대신 설계해주지는 않는다.
