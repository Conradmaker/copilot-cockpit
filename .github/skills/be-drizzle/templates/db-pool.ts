import { drizzle } from "drizzle-orm/node-postgres"
import { Pool } from "pg"

const pool = new Pool({
  connectionString: process.env.DATABASE_URL!,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
})

export const db = drizzle(pool)

process.on("SIGTERM", async () => {
  await pool.end()
  process.exit(0)
})

process.on("SIGINT", async () => {
  await pool.end()
  process.exit(0)
})
