/**
 * Run Migration Script
 *
 * Applies pending Drizzle migrations to your PostgreSQL database.
 * Run with: npx ts-node scripts/run-migration.ts
 *
 * Uses node-postgres (pg) Pool by default.
 * For Neon HTTP adapter, see references/neon.md.
 */

import { drizzle } from "drizzle-orm/node-postgres"
import { migrate } from "drizzle-orm/node-postgres/migrator"
import { Pool } from "pg"

const DATABASE_URL = process.env.DATABASE_URL

if (!DATABASE_URL) {
  console.error("DATABASE_URL environment variable is not set")
  process.exit(1)
}

async function runMigrations() {
  console.log("Running Drizzle migrations...\n")

  const pool = new Pool({ connectionString: DATABASE_URL })

  try {
    const db = drizzle(pool)

    console.log("Applying migrations...")
    await migrate(db, {
      migrationsFolder: "./src/db/migrations",
    })

    console.log("All migrations applied successfully!\n")

    console.log("Migration Summary:")
    console.log("   Migrations folder: ./src/db/migrations")
    console.log("   Status: Up to date\n")

    return true
  } catch (error) {
    console.error("Migration failed")
    console.error((error as any).message)

    console.log("\nTroubleshooting:")
    console.log("   - Ensure ./src/db/migrations directory exists")
    console.log("   - Verify DATABASE_URL is correct")
    console.log("   - Check that migrations are properly formatted SQL files")
    console.log("   - Try running: npx drizzle-kit generate first")
    console.log("   - See references/troubleshooting.md for common migration errors")
    console.log("   - See references/migrations.md for detailed migration guide")

    const errorMessage = (error as any).message.toLowerCase()

    if (errorMessage.includes("connect") || errorMessage.includes("connection")) {
      console.log("\nConnection issue detected:")
      console.log("   - Verify DATABASE_URL format: postgresql://user:pass@host/db?sslmode=require")
      console.log("   - Ensure database is accessible")
      console.log("   - Check firewall/network settings")
    }

    if (errorMessage.includes("already exists") || errorMessage.includes("duplicate")) {
      console.log("\nMigration conflict detected:")
      console.log("   - Migration may have been partially applied")
      console.log('   - Check database state: psql $DATABASE_URL -c "\\dt"')
      console.log("   - See references/migrations.md for handling conflicts")
    }

    if (errorMessage.includes("not found") || errorMessage.includes("enoent")) {
      console.log("\nMigrations folder missing:")
      console.log("   - Run: npx drizzle-kit generate")
      console.log("   - Ensure migrations folder path matches drizzle.config.ts")
    }

    if (errorMessage.includes("syntax")) {
      console.log("\nSQL syntax error:")
      console.log("   - Review generated migration files in ./src/db/migrations")
      console.log("   - Check for manually edited migrations")
      console.log("   - See references/migrations.md for safe editing practices")
    }

    return false
  } finally {
    await pool.end()
  }
}

runMigrations().then((success) => {
  process.exit(success ? 0 : 1)
})
