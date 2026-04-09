# Troubleshooting

Common issues when working with shadcn/ui and their solutions.

---

## Import Errors

**"Cannot find module '@/components/ui/button'"**

Check `components.json` for correct alias configuration, then verify `tsconfig.json` includes the `@` path alias:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

For Vite, also update `vite.config.ts`:

```typescript
import path from "path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

Run `npx shadcn@latest info` to verify resolved paths match your project structure.

---

## Style Conflicts

**Components render without styling or look broken**

1. Ensure Tailwind CSS is properly configured
2. Check that `globals.css` (or equivalent) is imported in your root layout/entry point
3. Verify CSS variable names match between components and theme
4. Confirm `tailwindcss-animate` is installed: `npm install tailwindcss-animate`
5. Check that CSS variables are properly defined in `:root` and `.dark`

---

## Missing Dependencies

**Runtime errors about missing packages**

- Run component installation via CLI (`npx shadcn@latest add <component>`) to auto-install deps
- Manually check `package.json` for required Radix UI packages
- Use `npx shadcn@latest docs <component>` to check dependency lists

---

## TypeScript Errors

**Type errors in component files**

- Run `npm install` to ensure all dependencies are installed
- Check that `@types/react` is installed
- Restart TypeScript server in your editor
- Run `tsc --noEmit` to verify

---

## Version Compatibility

- shadcn/ui requires React 18+ and Next.js 13+ (if using Next.js)
- Some components require specific Radix UI versions
- Check documentation for breaking changes between versions
- Use `npx shadcn@latest add <component> --diff` to compare local vs upstream