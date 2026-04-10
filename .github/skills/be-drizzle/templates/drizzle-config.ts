/**
 * Drizzle Configuration
 *
 * Place this in your project root as drizzle.config.ts.
 *
 * CRITICAL: The config({ path: '...' }) line must match your environment file.
 *   - Next.js → '.env.local'
 *   - Other projects → '.env'
 */

import { config } from "dotenv"
import type { Config } from "drizzle-kit"

config({ path: ".env" })

const dbUrl = process.env.DATABASE_URL

if (!dbUrl) {
  throw new Error("DATABASE_URL environment variable is not set")
}

export default {
  schema: "./src/db/schema.ts",
  out: "./src/db/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: dbUrl,
  },
  migrations: {
    prefix: "timestamp",
  },
  verbose: process.env.DEBUG === "true",
  strict: true,
} satisfies Config

/**
 * Migration Commands
 *
 * npx drizzle-kit generate    # Generate migration files from schema changes
 * npx drizzle-kit migrate     # Apply migrations to database
 * npx drizzle-kit drop        # Drop all tables (careful!)
 * npx drizzle-kit introspect  # Introspect existing database
 * npx drizzle-kit push        # Push schema changes directly (development only)
 */
