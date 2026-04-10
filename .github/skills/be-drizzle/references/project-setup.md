# Drizzle Project Setup

This reference consolidates new-project setup and existing-project integration into one generic PostgreSQL guide for Drizzle ORM.

For Neon-specific adapter setup, see neon.md.

## Table of Contents

- [New Project Setup](#new-project-setup)
  - [Context Detection](#context-detection)
  - [Installation](#installation)
  - [Configuration](#configuration)
    - [Environment File](#environment-file)
    - [Drizzle Config](#drizzle-config)
    - [Database Connection](#database-connection)
  - [Schema Generation](#schema-generation)
  - [Migrations](#migrations)
  - [Package Scripts](#package-scripts)
- [Existing Project Integration](#existing-project-integration)
  - [Pre-Integration Check](#pre-integration-check)
  - [Incremental Installation](#incremental-installation)
  - [Schema Strategy](#schema-strategy)
  - [Migration Handling](#migration-handling)
  - [Coexistence Patterns](#coexistence-patterns)
  - [Verification](#verification)

## New Project Setup

Use this flow when you are adding Drizzle to a project from scratch.

### Context Detection

Auto-detect project context:

**Check Package Manager:**

```bash
ls package-lock.json  # -> npm
ls bun.lockb          # -> bun
ls pnpm-lock.yaml     # -> pnpm
ls yarn.lock          # -> yarn
```

**Check Framework:**

```bash
grep '"next"' package.json      # -> Next.js
grep '"express"' package.json   # -> Express
grep '"vite"' package.json      # -> Vite
```

**Check Existing Setup:**

```bash
ls drizzle.config.ts   # Already configured?
ls src/db/schema.ts    # Schema exists?
```

**Check Environment Files:**

```bash
ls .env .env.local .env.production
```

### Installation

Install dependencies based on the runtime you are targeting.

**For Edge or serverless runtimes:**

```bash
[package-manager] add drizzle-orm postgres
[package-manager] add -D drizzle-kit dotenv
```

**For Node.js servers:**

```bash
[package-manager] add drizzle-orm pg
[package-manager] add -D drizzle-kit dotenv
```

### Configuration

Create configuration files in dependency order.

#### Environment File

**Outcome**: A working `.env` or `.env.local` file with a real PostgreSQL connection string that the application can use immediately.

If `DATABASE_URL` already exists, reuse it after verifying that it points to the correct PostgreSQL database. If it does not exist yet, provision a PostgreSQL database through your hosting provider or infrastructure and write the connection string to the correct environment file (`.env.local` for Next.js, `.env` for other projects). Add that file to `.gitignore`.

**Environment file format:**

```bash
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

#### Drizzle Config

Create `drizzle.config.ts` with explicit environment loading.

**Critical:** The `config({ path: '...' })` line must match the environment file you chose in the previous step.

**For Next.js (using `.env.local`):**

```typescript
import { defineConfig } from 'drizzle-kit';
import { config } from 'dotenv';

config({ path: '.env.local' });

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**For other projects (using `.env`):**

```typescript
import { defineConfig } from 'drizzle-kit';
import { config } from 'dotenv';

config({ path: '.env' });

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Why this matters:**

- Without explicit `config({ path: '...' })`, drizzle-kit may not load environment variables.
- This prevents `url: undefined` errors during migrations.
- The path must match your environment file name.

#### Database Connection

Create `src/db/index.ts` with the adapter that matches your runtime.

**For Node.js servers:**

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL! });
export const db = drizzle(pool);
```

**For Edge or serverless runtimes:**

```typescript
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client);
```

For Neon-specific adapter setup, see neon.md.

### Schema Generation

Based on app type, create an appropriate schema.

**Todo app example:**

```typescript
import { pgTable, serial, text, boolean, timestamp, varchar } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

export const todos = pgTable('todos', {
  id: serial('id').primaryKey(),
  userId: serial('user_id').notNull().references(() => users.id),
  title: text('title').notNull(),
  completed: boolean('completed').default(false),
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Blog app example:**

```typescript
import { pgTable, serial, text, timestamp, varchar, index } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 255 }).notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  userId: serial('user_id').notNull().references(() => users.id),
  title: text('title').notNull(),
  content: text('content').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
}, (table) => ({
  userIdIdx: index('posts_user_id_idx').on(table.userId),
}));

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.userId],
    references: [users.id],
  }),
}));
```

### Migrations

Run migrations with explicit environment loading so the CLI sees the same `DATABASE_URL` as your app.

**Generate a migration:**

```bash
[package-manager] drizzle-kit generate
```

This creates SQL files in `src/db/migrations/`.

**Apply a migration with `.env.local`:**

```bash
export DATABASE_URL="$(grep '^DATABASE_URL=' .env.local | cut -d '=' -f2-)" && \
[package-manager] drizzle-kit migrate
```

**Apply a migration with `.env`:**

```bash
export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d '=' -f2-)" && \
[package-manager] drizzle-kit migrate
```

**Why this works:** Ensures `DATABASE_URL` is available to drizzle-kit and helps avoid `url: undefined` errors.

If a migration fails, review the generated SQL and see `migrations.md` for common patterns and recovery steps.

### Package Scripts

Add these convenience scripts to `package.json`:

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

**Usage:**

```bash
npm run db:generate  # Generate migrations from schema changes
npm run db:migrate   # Apply pending migrations
npm run db:push      # Push schema directly (development only)
npm run db:studio    # Open Drizzle Studio
```

Replace `npm run` with your package manager's equivalent (`pnpm`, `yarn`, or `bun`).

## Existing Project Integration

Use this flow when you need to add Drizzle to an existing application without breaking current database access.

### Pre-Integration Check

Before adding Drizzle, check for conflicts.

**Check for other ORMs:**

```bash
grep -E '"(prisma|typeorm|sequelize|mongoose)"' package.json
```

**If found:**

- Consider a coexistence strategy before planning a full replacement.
- Document which tables use which ORM.
- Plan gradual migration if needed.

**Check database schema:**

```bash
psql "$DATABASE_URL" -c "\\dt"
```

Note the existing tables. Drizzle should not conflict with them.

**Check environment setup:**

```bash
ls .env .env.local .env.production
grep DATABASE_URL .env*
```

**If `DATABASE_URL` exists:**

- Verify the connection string format is valid for PostgreSQL (`postgresql://...`).
- If it points at a different database engine, you will need a PostgreSQL target or a different Drizzle dialect.

**If `DATABASE_URL` does not exist:**

- Provision a PostgreSQL database through your platform or infrastructure.
- Write the URL to the appropriate environment file (`.env.local` for Next.js, `.env` for other projects).
- Add that file to `.gitignore`.
- Verify both the app runtime and drizzle-kit can read the same variable.

### Incremental Installation

Add Drizzle without disrupting the existing setup.

**Install dependencies for Edge or serverless runtimes:**

```bash
[package-manager] add drizzle-orm postgres
[package-manager] add -D drizzle-kit dotenv
```

**Install dependencies for Node.js servers:**

```bash
[package-manager] add drizzle-orm pg
[package-manager] add -D drizzle-kit dotenv
```

**Create an isolated Drizzle directory:**

```bash
mkdir -p src/drizzle
```

Recommended structure:

```text
src/drizzle/
├── index.ts
├── schema.ts
└── migrations/
```

**Create `drizzle.config.ts` for Next.js projects:**

```typescript
import { defineConfig } from 'drizzle-kit';
import { config } from 'dotenv';

config({ path: '.env.local' });

export default defineConfig({
  schema: './src/drizzle/schema.ts',
  out: './src/drizzle/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Create `drizzle.config.ts` for other projects:**

```typescript
import { defineConfig } from 'drizzle-kit';
import { config } from 'dotenv';

config({ path: '.env' });

export default defineConfig({
  schema: './src/drizzle/schema.ts',
  out: './src/drizzle/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Create `src/drizzle/index.ts` for Node.js servers:**

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const pool = new Pool({ connectionString: process.env.DATABASE_URL! });
export const drizzleDb = drizzle(pool);
```

**Create `src/drizzle/index.ts` for Edge or serverless runtimes:**

```typescript
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';

const client = postgres(process.env.DATABASE_URL!);
export const drizzleDb = drizzle(client);
```

Name the exported client `drizzleDb` if your project already has another `db` export.

For Neon-specific adapter setup, see neon.md.

### Schema Strategy

Choose the integration approach that matches your migration risk tolerance.

**Option A: New tables only**

Create schemas for new features only and leave existing tables alone:

```typescript
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const newFeatureTable = pgTable('new_feature', {
  id: serial('id').primaryKey(),
  data: text('data').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Pros:**

- No migration of existing data.
- Minimal risk to current functionality.
- Easy gradual adoption.

**Cons:**

- Mixed query patterns across the codebase.
- Two connection patterns can coexist for a while.

**Option B: Mirror existing tables**

Define schemas for existing tables so you can gradually migrate queries:

```typescript
import { pgTable, serial, varchar, timestamp } from 'drizzle-orm/pg-core';

export const existingUsers = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull(),
  name: varchar('name', { length: 255 }),
  createdAt: timestamp('created_at'),
});
```

**Pros:**

- Existing data becomes queryable through Drizzle.
- You can replace old ORM queries incrementally.
- Existing tables gain type-safe access.

**Cons:**

- The Drizzle schema must match the live schema exactly.
- Migration handling becomes more sensitive.

**Recommended hybrid approach:**

1. Start with Option A for new tables only.
2. Add mirrored schemas only for high-value existing tables.
3. Gradually migrate queries from the old ORM to Drizzle.
4. Remove the old ORM after query parity and verification are complete.

### Migration Handling

Handle migrations differently depending on whether Drizzle owns the tables.

**For new tables:**

```bash
[package-manager] drizzle-kit generate
export DATABASE_URL="$(grep '^DATABASE_URL=' .env.local | cut -d '=' -f2-)" && \
[package-manager] drizzle-kit migrate
```

**With `.env` instead of `.env.local`:**

```bash
[package-manager] drizzle-kit generate
export DATABASE_URL="$(grep '^DATABASE_URL=' .env | cut -d '=' -f2-)" && \
[package-manager] drizzle-kit migrate
```

**For existing tables:**

Do not run migrations for tables that already exist. Define schemas so Drizzle can query them safely.

```typescript
import { drizzleDb } from './drizzle';
import { existingUsers } from './drizzle/schema';

const users = await drizzleDb.select().from(existingUsers);
```

**For mixed scenarios:**

1. Define both new and existing-table schemas in `schema.ts`.
2. Run `drizzle-kit generate`.
3. Manually edit the generated migration to remove SQL for existing tables.
4. Apply the migration only after reviewing the remaining SQL.

**Package scripts:**

Reuse the same `db:generate`, `db:migrate`, `db:push`, and `db:studio` scripts shown in the new-project flow.

See `migrations.md` for deeper guidance on reviewing generated SQL and handling rename or coexistence cases.

### Coexistence Patterns

Keep the old ORM and Drizzle clearly separated while you migrate.

**Naming conventions:**

```typescript
import { db as prismaDb } from './lib/prisma';
import { drizzleDb } from './drizzle';

const prismaUsers = await prismaDb.user.findMany();
const drizzleFeatures = await drizzleDb.select().from(newFeatureTable);
```

**Gradual migration:**

**Step 1: New features use Drizzle**

```typescript
async function createFeature(data: NewFeatureInput) {
  return drizzleDb.insert(newFeatureTable).values(data).returning();
}
```

**Step 2: Migrate read queries first**

```typescript
async function getUsers() {
  return drizzleDb.select().from(existingUsers);
}
```

**Step 3: Migrate write queries after thorough testing**

```typescript
import { eq } from 'drizzle-orm';

async function updateUser(id: number, data: UserUpdate) {
  return drizzleDb.update(existingUsers)
    .set(data)
    .where(eq(existingUsers.id, id));
}
```

**Step 4:** Remove the old ORM once all critical queries have been migrated and validated.

### Verification

Verify the Drizzle integration without breaking current behavior.

**Test new tables:**

```typescript
import { drizzleDb } from './drizzle';
import { newFeatureTable } from './drizzle/schema';

const result = await drizzleDb.insert(newFeatureTable)
  .values({ data: 'test' })
  .returning();

console.log('New table works:', result);
```

**Test existing tables (if mirrored):**

```typescript
import { drizzleDb } from './drizzle';
import { existingUsers } from './drizzle/schema';

const users = await drizzleDb.select().from(existingUsers);
console.log('Existing table accessible:', users);
```

**Verify the old ORM still works:**

```typescript
import { db as oldDb } from './lib/your-orm';

const oldQuery = await oldDb.users.findMany();
console.log('Old ORM still works:', oldQuery);
```