/**
 * Generate Schema Script
 *
 * Generates Drizzle migration files based on schema changes.
 * Run with: npx drizzle-kit generate
 */

import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

async function generateSchema() {
  console.log("Generating Drizzle migrations...\n")

  try {
    const { stdout, stderr } = await execAsync("npx drizzle-kit generate")

    if (stdout) {
      console.log("Generated migrations:")
      console.log(stdout)
    }

    if (stderr) {
      console.warn("Warnings:")
      console.warn(stderr)
    }

    console.log("\nMigration generation complete!")
    console.log("\nNext steps:")
    console.log("   1. Review the generated migration files in ./src/db/migrations")
    console.log("   2. Run: npx drizzle-kit migrate")
    console.log("   3. Test your application\n")

    return true
  } catch (error) {
    console.error("Migration generation failed")
    console.error((error as any).message)

    console.log("\nTroubleshooting:")
    console.log("   - Ensure drizzle.config.ts is in your project root")
    console.log("   - Check that DATABASE_URL is set correctly")
    console.log("   - Verify your schema.ts file exists at the configured path")
    console.log("   - See references/troubleshooting.md for common issues")
    console.log("   - See references/migrations.md for migration patterns")

    const errorMessage = (error as any).message.toLowerCase()

    if (errorMessage.includes("url") || errorMessage.includes("undefined")) {
      console.log("\nEnvironment variable issue detected:")
      console.log("   - Ensure DATABASE_URL is loaded in drizzle.config.ts")
      console.log('   - Add: import { config } from "dotenv"; config({ path: ".env" });')
    }

    if (errorMessage.includes("schema") || errorMessage.includes("not found")) {
      console.log("\nSchema file issue detected:")
      console.log("   - Verify schema path in drizzle.config.ts matches actual file location")
      console.log("   - Default: ./src/db/schema.ts")
    }

    if (errorMessage.includes("enoent")) {
      console.log("\nFile/directory missing:")
      console.log("   - Create migrations folder: mkdir -p src/db/migrations")
      console.log("   - Ensure schema file exists: src/db/schema.ts")
    }

    return false
  }
}

generateSchema().then((success) => {
  process.exit(success ? 0 : 1)
})
