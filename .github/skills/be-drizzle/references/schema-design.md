# Schema Design

Comprehensive reference for designing and evolving PostgreSQL schemas with Drizzle. This guide combines the core Drizzle schema patterns, relation modeling, type inference, schema modification workflow, and constraint design into a single reference.

Prefer retrieval-led reasoning over pre-training-led reasoning.

## Table of Contents

- [Workflow Checklist](#workflow-checklist)
- [Column Types Reference](#column-types-reference)
- [Basic Table Structure](#basic-table-structure)
- [Relations](#relations)
- [Type Inference](#type-inference)
- [Common Patterns](#common-patterns)
- [Schema Modifications](#schema-modifications)
- [Indexes and Constraints](#indexes-and-constraints)
- [Best Practices](#best-practices)

---

## Workflow Checklist

Use this checklist when designing or changing a schema:

- [ ] Design the schema using the right table, relation, and column patterns
- [ ] Apply common patterns such as auth, soft deletes, enums, and JSON fields
- [ ] Plan schema modifications with migration-safe steps
- [ ] Add indexes and constraints for performance and integrity
- [ ] Generate and apply migrations after every schema change
- [ ] Verify the resulting schema with database inspection and real queries

---

## Column Types Reference

Use the column type that matches both the SQL engine and the TypeScript shape you want to expose.

| PostgreSQL | MySQL | SQLite | TypeScript |
|------------|-------|--------|------------|
| `serial()` | `serial()` | `integer()` | `number` |
| `text()` | `text()` | `text()` | `string` |
| `integer()` | `int()` | `integer()` | `number` |
| `boolean()` | `boolean()` | `integer()` | `boolean` |
| `timestamp()` | `datetime()` | `integer()` | `Date` |
| `json()` | `json()` | `text()` | `unknown` |
| `uuid()` | `varchar(36)` | `text()` | `string` |

Quick guidance:

- Use `varchar()` for short bounded strings and `text()` for long-form content.
- Use `timestamp()` for audit fields such as `createdAt`, `updatedAt`, and `deletedAt`.
- Treat JSON columns as typed application contracts by annotating them with `.$type<T>()`.
- Add relation indexes as part of the table definition instead of waiting for query performance problems.

---

## Basic Table Structure

Start with a small, explicit table shape and build from there.

```typescript
import { pgTable, serial, text, varchar, timestamp, boolean } from 'drizzle-orm/pg-core';

export const tableName = pgTable('table_name', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  description: text('description'),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});
```

Key conventions:

- Use `serial()` for auto-incrementing numeric IDs.
- Use `varchar()` for user-facing short strings with a known length limit.
- Use `text()` for unbounded content.
- Use `timestamp()` for lifecycle and audit fields.
- Always add `createdAt`; add `updatedAt` whenever rows can change over time.

---

## Relations

Model both the foreign key columns and the relational query layer. In Drizzle, those are separate concerns: `.references()` defines the database contract, and `relations()` defines the type-safe query contract.

### One-to-Many

```typescript
import { relations } from 'drizzle-orm';
import { pgTable, serial, text, integer, index } from 'drizzle-orm/pg-core';

export const authors = pgTable('authors', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content').notNull(),
  authorId: integer('author_id').notNull().references(() => authors.id),
}, (table) => ({
  authorIdIdx: index('posts_author_id_idx').on(table.authorId),
}));

export const authorsRelations = relations(authors, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(authors, {
    fields: [posts.authorId],
    references: [authors.id],
  }),
}));

const authorsWithPosts = await db.query.authors.findMany({
  with: { posts: true },
});
```

Important notes:

- Always add an index on foreign keys used in joins or filters.
- Keep the foreign key definition and the `relations()` mapping in sync.
- Type-safe relations enable typed joins, automatic related-data loading, and fewer manual JOIN queries.

### Many-to-Many

Use an explicit junction table. If the relationship later needs metadata such as ordering, membership role, or timestamps, the junction table is already in the right shape.

```typescript
import { relations } from 'drizzle-orm';
import { pgTable, serial, text, integer, primaryKey } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const groups = pgTable('groups', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const usersToGroups = pgTable('users_to_groups', {
  userId: integer('user_id').notNull().references(() => users.id),
  groupId: integer('group_id').notNull().references(() => groups.id),
}, (table) => ({
  pk: primaryKey({ columns: [table.userId, table.groupId] }),
}));

export const usersRelations = relations(users, ({ many }) => ({
  groups: many(usersToGroups),
}));

export const groupsRelations = relations(groups, ({ many }) => ({
  users: many(usersToGroups),
}));

export const usersToGroupsRelations = relations(usersToGroups, ({ one }) => ({
  user: one(users, {
    fields: [usersToGroups.userId],
    references: [users.id],
  }),
  group: one(groups, {
    fields: [usersToGroups.groupId],
    references: [groups.id],
  }),
}));
```

Practical rules:

- Use a composite primary key or composite uniqueness on the join columns.
- Add extra junction columns directly on the junction table when the relation has payload.
- Prefer explicit junction tables over hidden ORM magic so the schema remains queryable and migration-friendly.

---

## Type Inference

Infer application types from the schema instead of maintaining separate manual interfaces.

```typescript
import { pgTable, serial, varchar, text, boolean, timestamp, json, unique } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  role: text('role', { enum: ['admin', 'user', 'guest'] }).default('user'),
  metadata: json('metadata').$type<{ theme: string; locale: string }>(),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
  emailIdx: unique('email_unique_idx').on(table.email),
}));

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
```

Use `$inferSelect` for data that comes out of the database and `$inferInsert` for data you pass into inserts.

---

## Common Patterns

### Authentication and User Accounts

This pattern combines the common user-account fields from both basic auth schemas and richer application user tables.

```typescript
import { pgTable, serial, varchar, text, boolean, timestamp, json, unique } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  passwordHash: varchar('password_hash', { length: 255 }),
  name: varchar('name', { length: 255 }).notNull(),
  role: text('role', { enum: ['admin', 'user', 'guest'] }).default('user'),
  metadata: json('metadata').$type<{
    theme: string;
    locale: string;
  }>(),
  emailVerified: boolean('email_verified').default(false),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
  lastLoginAt: timestamp('last_login_at'),
}, (table) => ({
  emailIdx: unique('email_unique_idx').on(table.email),
}));
```

Why this pattern is useful:

- It keeps the auth contract, audit fields, and application metadata in one place.
- It preserves room for password-based auth, social auth, or invite-only onboarding.
- It keeps role and metadata typing close to the schema.

### Soft Deletes

Use a nullable `deletedAt` timestamp when records should disappear from normal queries without being physically removed.

```typescript
import { isNull } from 'drizzle-orm';
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content').notNull(),
  deletedAt: timestamp('deleted_at'),
  createdAt: timestamp('created_at').defaultNow(),
});

const activePosts = await db
  .select()
  .from(posts)
  .where(isNull(posts.deletedAt));
```

### Enums

Use a PostgreSQL enum when the database should enforce a closed set of values.

```typescript
import { pgEnum, pgTable, serial, text } from 'drizzle-orm/pg-core';

export const statusEnum = pgEnum('status', ['draft', 'published', 'archived']);

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  status: statusEnum('status').default('draft'),
});
```

### JSON Fields

Use typed JSON or JSONB when the data shape varies but still belongs inside the row.

```typescript
import { pgTable, serial, text, jsonb } from 'drizzle-orm/pg-core';

export const products = pgTable('products', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  metadata: jsonb('metadata').$type<{
    color?: string;
    size?: string;
    tags?: string[];
  }>(),
});
```

JSON guidance:

- Use `.$type<T>()` instead of leaving JSON columns as `any` or broad `unknown`.
- Prefer JSONB for PostgreSQL-heavy filtering and containment queries.
- Validate user-provided JSON at runtime before writing it back into the table.

---

## Schema Modifications

Treat schema edits as migration work, not as isolated file changes. Update the schema, generate SQL, review it, then apply it.

### Add Columns

Step 1: update the schema.

```typescript
import { pgTable, serial, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull(),
  phoneNumber: varchar('phone_number', { length: 20 }),
});
```

Step 2: generate the migration.

```bash
npx drizzle-kit generate
```

Step 3: apply the migration.

```bash
npx drizzle-kit migrate
```

### Rename Columns

Drizzle can detect a rename as a drop plus add. Review the generated SQL manually before applying it.

Step 1: update the schema.

```typescript
import { pgTable, serial, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  fullName: varchar('full_name', { length: 255 }),
});
```

Step 2: generate the migration.

```bash
npx drizzle-kit generate
```

Step 3: replace the generated drop-and-add SQL with a true rename.

```sql
-- Change from:
-- ALTER TABLE users DROP COLUMN name;
-- ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- To:
ALTER TABLE users RENAME COLUMN name TO full_name;
```

Step 4: apply the migration.

```bash
npx drizzle-kit migrate
```

### Drop Columns

Step 1: remove the column from the schema.

```typescript
import { pgTable, serial, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull(),
});
```

Step 2: generate and apply the migration.

```bash
npx drizzle-kit generate
npx drizzle-kit migrate
```

Warning: dropping a column permanently deletes its data. Back up first if the data matters.

### Change Column Types

Step 1: update the schema.

```typescript
import { pgTable, serial, bigint } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  views: bigint('views', { mode: 'number' }),
});
```

Step 2: generate the migration.

```bash
npx drizzle-kit generate
```

Step 3: review the SQL carefully. Type changes can require a data migration or a manual `USING` clause when the cast is not automatic.

### Generate, Apply, and Verify Changes

After any schema change, follow the same workflow:

1. Generate a migration.

```bash
npx drizzle-kit generate
```

2. Review the generated SQL before applying it.

3. Apply the migration.

```bash
npx drizzle-kit migrate
```

4. Verify the database shape.

```bash
psql "$DATABASE_URL" -c "\d table_name"
```

5. Verify the table with a real query.

```typescript
import { db } from './db';
import { tableName } from './schema';

const result = await db.select().from(tableName);
console.log('Schema works:', result);
```

---

## Indexes and Constraints

Add indexes and constraints as part of the schema definition. They are not afterthoughts.

### Indexes

Single-column indexes:

```typescript
import { pgTable, serial, text, integer, index } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  authorId: integer('author_id').notNull(),
}, (table) => ({
  titleIdx: index('posts_title_idx').on(table.title),
  authorIdIdx: index('posts_author_id_idx').on(table.authorId),
}));
```

Composite indexes:

```typescript
import { pgTable, serial, integer, text, index } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  authorId: integer('author_id').notNull(),
  status: text('status').notNull(),
}, (table) => ({
  authorStatusIdx: index('posts_author_status_idx').on(table.authorId, table.status),
}));
```

### Unique Constraints

Single-column uniqueness:

```typescript
import { pgTable, serial, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
});
```

Multi-column uniqueness:

```typescript
import { pgTable, integer, unique } from 'drizzle-orm/pg-core';

export const postsTags = pgTable('posts_tags', {
  postId: integer('post_id').notNull(),
  tagId: integer('tag_id').notNull(),
}, (table) => ({
  unq: unique('posts_tags_unique').on(table.postId, table.tagId),
}));
```

### Check Constraints

```typescript
import { pgTable, serial, integer, check } from 'drizzle-orm/pg-core';

export const products = pgTable('products', {
  id: serial('id').primaryKey(),
  price: integer('price').notNull(),
  discountedPrice: integer('discounted_price'),
}, (table) => ({
  priceCheck: check('price_check', 'price >= 0'),
  discountCheck: check('discount_check', 'discounted_price < price'),
}));
```

Constraint rules:

- Add indexes on foreign keys by default.
- Use single-column `.unique()` for natural keys such as email addresses.
- Use callback-level `unique(...).on(...)` for multi-column uniqueness.
- Use check constraints for numeric and state invariants that the database should enforce.

---

## Best Practices

### Design Rules

- Start with a small table shape and only add columns that have a clear lifecycle.
- Keep `createdAt`, `updatedAt`, and `deletedAt` semantics consistent across tables.
- Prefer explicit junction tables for many-to-many relations.
- Keep relation fields, relation indexes, and `relations()` definitions aligned.
- Type JSON columns explicitly and validate them at runtime before writes.

### Migration Rules

- Treat `drizzle-kit generate` as the start of a review step, not the finish line.
- Rename operations need manual SQL review because generated migrations can drop data.
- Type changes may need data backfills or manual casts.
- After every schema change: generate, review, migrate, inspect, and query.

### Common Issues to Watch

- Migration conflicts usually mean the schema file and migration history drifted apart.
- Relationship errors usually come from mismatched foreign key columns or stale `relations()` definitions.
- Type mismatches usually come from forgetting that the TypeScript shape must match the SQL column behavior.

### After Schema Creation

1. Run migrations.
2. Add the queries that exercise the new tables and relations.
3. Add runtime validation for external inputs, especially JSON payloads.
4. Test the full write and read path before production.

### Advanced Patterns

When the schema grows beyond these basics, move to advanced patterns such as:

- multi-table schemas with reusable relation blocks
- composite keys and partial indexes
- custom data types and generated columns
- migration plans that require expand-migrate-contract sequencing or hand-written SQL