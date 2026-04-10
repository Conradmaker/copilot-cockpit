# Neon Provider Reference

Neon Serverless PostgreSQL adapter setup for Drizzle ORM.

> This reference covers Neon-specific configuration only. For general Drizzle setup, see `project-setup.md` and `connection-management.md`.

## Adapter Decision

| Environment | Adapter | Package | Drizzle Import |
|---|---|---|---|
| Edge / Serverless (Vercel, Cloudflare, Lambda) | HTTP | `@neondatabase/serverless` | `drizzle-orm/neon-http` |
| Node.js / Long-lived server | WebSocket | `@neondatabase/serverless` + `ws` | `drizzle-orm/neon-serverless` |

**Quick rule:** Stateless request → HTTP adapter. Persistent process → WebSocket adapter.

## HTTP Adapter Setup

Best for serverless/edge environments. Stateless, no connection pool.

### Installation

```bash
npm add drizzle-orm @neondatabase/serverless
npm add -D drizzle-kit
```

### Connection

```typescript
import { drizzle } from 'drizzle-orm/neon-http';
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql);
```

### Characteristics

- No transactions (use batch operations instead)
- No prepared statements
- No streaming
- Fast cold starts, auto-scales
- Each query = single HTTP request

### Batch Operations (transaction alternative)

```typescript
await db.batch([
  db.insert(users).values({ email: 'a@example.com' }),
  db.insert(posts).values({ title: 'Test' }),
]);
```

## WebSocket Adapter Setup

Best for long-lived Node.js processes. Supports transactions, connection pooling, streaming.

### Installation

```bash
npm add drizzle-orm @neondatabase/serverless ws
npm add -D drizzle-kit @types/ws
```

### Connection

```typescript
import { drizzle } from 'drizzle-orm/neon-serverless';
import { Pool, neonConfig } from '@neondatabase/serverless';
import ws from 'ws';

neonConfig.webSocketConstructor = ws;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL!,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

export const db = drizzle(pool);

// Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end();
  process.exit(0);
});
```

> **Bun:** Built-in WebSocket support — skip the `ws` import and `neonConfig.webSocketConstructor` line.

## Feature Comparison

| Feature | HTTP Adapter | WebSocket Adapter |
|---------|-------------|-------------------|
| Transactions | No | Yes |
| Prepared statements | No | Yes |
| Streaming results | No | Yes |
| Connection pooling | N/A (stateless) | Yes |
| Edge runtime | Yes | No |
| Cold start speed | Fast | Slower |
| Latency per query | Higher (50-200ms) | Lower (10-50ms) |
| Batch operations | Yes | Yes |

## Framework Recommendations

| Framework | Adapter | Reason |
|---|---|---|
| Next.js App Router (Vercel) | HTTP | Edge Runtime, stateless |
| Next.js Pages Router | Either | HTTP for consistency |
| Express / Fastify | WebSocket | Long-lived, connection pooling |
| Bun server | WebSocket | Persistent runtime |
| Vercel Edge Functions | HTTP | Edge runtime |
| Cloudflare Workers | HTTP | Edge runtime, no WebSocket |
| AWS Lambda | HTTP | Stateless, cold starts |

## Mixed Environments

If your app has both serverless and long-lived components:

```
src/
├── db/
│   ├── http.ts        # HTTP adapter for serverless routes
│   ├── ws.ts          # WebSocket for background workers
│   └── schema.ts      # Shared schema
```

## Neon-Specific Troubleshooting

### "WebSocket connection failed"

Missing WebSocket constructor in Node.js:

```typescript
import { neonConfig } from '@neondatabase/serverless';
import ws from 'ws';

neonConfig.webSocketConstructor = ws;
```

### "Cannot perform transactions with HTTP adapter"

HTTP adapter does not support transactions. Switch to WebSocket adapter or use batch operations.

### Wrong Adapter for Environment

- App works locally but fails in production → probably using WebSocket in an edge environment
- Works in production but not locally → may need `ws` package for Node.js WebSocket

### Connection String Format

```
postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require
```

Ensure `?sslmode=require` is included for Neon connections.

## Migration Between Adapters

### HTTP → WebSocket

1. Install `ws`: `npm add ws @types/ws`
2. Update connection file to WebSocket adapter
3. Test transactions (now available)

### WebSocket → HTTP

1. Update connection file to HTTP adapter
2. Remove `ws` dependency
3. Replace transactions with batch operations
4. Test thoroughly (feature differences)

## Related Resources

- `connection-management.md` — generic driver selection and connection patterns
- `troubleshooting.md` — general Drizzle troubleshooting
- `performance.md` — connection pooling and query optimization
