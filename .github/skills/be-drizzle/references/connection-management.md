# Connection Management

Reference guide for selecting a Drizzle driver, creating a reusable `drizzle()` instance, and handling connection lifecycles across long-lived and serverless runtimes.

Prefer retrieval-led reasoning over pre-training-led reasoning.

## Table of Contents

- [Driver Selection Matrix](#driver-selection-matrix)
- [PostgreSQL Connection (node-postgres Pool)](#postgresql-connection-node-postgres-pool)
- [PostgreSQL Connection (postgres-js)](#postgresql-connection-postgres-js)
- [MySQL Connection](#mysql-connection)
- [SQLite Connection](#sqlite-connection)
- [Singleton Pattern](#singleton-pattern)
- [Graceful Shutdown](#graceful-shutdown)
- [Read Replicas](#read-replicas)
- [Provider-Specific Adapters](#provider-specific-adapters)

---

## Driver Selection Matrix

Use the runtime first, then pick the driver and adapter that match its connection model.

| Runtime | Package | Drizzle Adapter | When to Use |
| --- | --- | --- | --- |
| Node.js (long-lived) | `pg` | `drizzle-orm/node-postgres` | Express, Fastify, workers |
| Edge / Serverless | `postgres` | `drizzle-orm/postgres-js` | Vercel Edge, Cloudflare, Deno |
| Bun | `pg` | `drizzle-orm/node-postgres` | Bun server |
| MySQL | `mysql2` | `drizzle-orm/mysql2` | MySQL backends |
| SQLite | `better-sqlite3` | `drizzle-orm/better-sqlite3` | Local, embedded |
| Neon Serverless | `@neondatabase/serverless` | `drizzle-orm/neon-http` or `drizzle-orm/neon-serverless` | See references/neon.md |

Quick guidance:

- Use pooled drivers in long-lived Node.js or Bun processes.
- Use a low-connection client in serverless runtimes and reuse it across warm starts.
- Keep `drizzle()` instance creation at module scope or behind a getter so requests share the same connection owner.
- Use this guide for connection setup; use `performance.md` for deeper pool tuning and throughput work.

## PostgreSQL Connection (node-postgres Pool)

Use `pg` with `drizzle-orm/node-postgres` for long-lived runtimes that can keep TCP connections open and benefit from pooling.

```typescript
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

export const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT ?? '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const db = drizzle(pool);
```

Key points:

- `max` should reflect both process concurrency and your database connection budget.
- `idleTimeoutMillis` closes idle clients instead of keeping them open indefinitely.
- `connectionTimeoutMillis` keeps connection pressure from stalling requests forever.
- Reuse the exported `pool` and `db`; do not recreate them per request.

## PostgreSQL Connection (postgres-js)

Use `postgres` with `drizzle-orm/postgres-js` when you want a lightweight PostgreSQL client for serverless, edge, or other low-connection runtimes.

```typescript
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';

export const client = postgres(process.env.DATABASE_URL!, {
  max: 1,
  idle_timeout: 20,
  connect_timeout: 10,
  prepare: false,
});

export const db = drizzle(client);
```

Key points:

- `max: 1` keeps per-instance connection count predictable in serverless environments.
- `prepare: false` is a safe default in ephemeral runtimes where prepared statement reuse is limited.
- Keep the client at module scope so warm starts can reuse it.
- When the provider offers a dedicated adapter, prefer that adapter over forcing a generic client into the wrong transport model.

## MySQL Connection

Use `mysql2/promise` with `drizzle-orm/mysql2` for MySQL applications that need pooling and long-lived connections.

```typescript
import mysql from 'mysql2/promise';
import { drizzle } from 'drizzle-orm/mysql2';

export const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
  maxIdle: 10,
  idleTimeout: 60000,
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelay: 0,
});

export const db = drizzle(pool);
```

Key points:

- `connectionLimit` is the MySQL equivalent of pool size.
- `waitForConnections` and `queueLimit` control backpressure when the pool is saturated.
- Keep-alive settings help long-lived services avoid unnecessary reconnect churn.

## SQLite Connection

Use `better-sqlite3` with `drizzle-orm/better-sqlite3` for local development, embedded apps, and single-host deployments.

```typescript
import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';

export const sqlite = new Database('sqlite.db', {
  readonly: false,
  fileMustExist: false,
  timeout: 5000,
});

sqlite.pragma('journal_mode = WAL');
sqlite.pragma('synchronous = normal');
sqlite.pragma('cache_size = -64000');
sqlite.pragma('temp_store = memory');

export const db = drizzle(sqlite);
```

Key points:

- `journal_mode = WAL` improves concurrent reads while writes are happening.
- `synchronous = normal` is a common balance between durability and throughput.
- The cache and temp-store pragmas reduce disk churn for read-heavy local workloads.
- Close the database handle during process shutdown for clean exits.

## Singleton Pattern

Keep the connection owner and the `drizzle()` instance in one module so all requests reuse the same client.

### Module-Level Singleton

Use this pattern in long-lived Node.js or Bun processes.

```typescript
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

let cachedPool: Pool | null = null;
let cachedDb: ReturnType<typeof drizzle> | null = null;

export function getDb() {
  if (!cachedPool || !cachedDb) {
    cachedPool = new Pool({
      connectionString: process.env.DATABASE_URL!,
      max: 20,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
    cachedDb = drizzle(cachedPool);
  }

  return cachedDb;
}
```

### Serverless Warm-Start Reuse

Use this pattern in serverless functions where the runtime may reuse the same instance across multiple invocations.

```typescript
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

let cachedPool: Pool | null = null;
let cachedDb: ReturnType<typeof drizzle> | null = null;

export function getDb() {
  if (!cachedDb) {
    cachedPool = new Pool({
      connectionString: process.env.DATABASE_URL!,
      max: 1,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
    cachedDb = drizzle(cachedPool);
  }

  return cachedDb;
}
```

Key points:

- The long-lived pattern optimizes for shared pool reuse inside one process.
- The serverless pattern optimizes for predictable connection count per warm instance.
- Avoid creating a new pool inside every request handler.

## Graceful Shutdown

Long-lived Node.js services should close pools and clients when the process receives termination signals.

```typescript
import { Pool } from 'pg';

export function registerShutdown(pool: Pool) {
  let shuttingDown = false;

  const closePool = async () => {
    if (shuttingDown) {
      return;
    }

    shuttingDown = true;
    await pool.end();
    process.exit(0);
  };

  process.once('SIGTERM', () => {
    void closePool();
  });

  process.once('SIGINT', () => {
    void closePool();
  });
}
```

Driver-specific cleanup rules:

- `pg` and `mysql2` pools: call `await pool.end()`.
- `postgres` clients: call `await client.end({ timeout: 5 })` when your runtime exposes process shutdown hooks.
- `better-sqlite3`: call `sqlite.close()` before the process exits.
- Serverless and edge handlers usually do not register signal hooks; they should rely on runtime reuse instead of explicit shutdown code.

## Read Replicas

Create separate clients for writes and reads, then route queries intentionally.

```typescript
import { Pool } from 'pg';
import { drizzle } from 'drizzle-orm/node-postgres';

export const primaryPool = new Pool({
  connectionString: process.env.PRIMARY_DB_URL!,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const replicaPool = new Pool({
  connectionString: process.env.REPLICA_DB_URL!,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const primaryDb = drizzle(primaryPool);
export const replicaDb = drizzle(replicaPool);

export async function getUsers() {
  return replicaDb.select().from(users);
}

export async function createUser(data: NewUser) {
  return primaryDb.insert(users).values(data).returning();
}
```

Key points:

- Write traffic should go to the primary connection.
- Read traffic can go to the replica connection if the application tolerates replication lag.
- Keep primary and replica pools separate so you can tune and observe them independently.
- Use `performance.md` for broader read-scaling and query-volume guidance.

## Provider-Specific Adapters

Some providers ship adapters that fit their transport model better than a generic pooled client.

- Neon: use `drizzle-orm/neon-http` or `drizzle-orm/neon-serverless`; see `references/neon.md`.
- Cloudflare D1: use `drizzle-orm/d1` with the platform-provided database binding.
- Supabase: use `drizzle-orm/postgres-js` with `postgres` when you want a generic PostgreSQL client.
- Choose a provider-specific adapter when runtime or network constraints make pooled TCP connections a poor fit.