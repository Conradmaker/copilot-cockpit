# Validation & Quality Checklist

Before committing shadcn/ui components, verify these quality gates.

---

## 1. Type Check

```bash
tsc --noEmit
```

Ensures all component types, props, and imports are correct.

---

## 2. Lint

Run your project's linter to catch style issues and unused imports:

```bash
npm run lint
# or
npx eslint src/components/ui/
```

---

## 3. Test Accessibility

- Use axe DevTools browser extension to scan for ARIA violations
- Verify keyboard navigation (Tab, Enter, Escape, Arrow keys)
- Test with screen readers when modifying interactive components
- Confirm focus indicators are visible

---

## 4. Visual QA

- Test in both light and dark modes
- Verify semantic color tokens render correctly in both themes
- Check component states: default, hover, focus, active, disabled

---

## 5. Responsive Check

- Verify behavior at mobile, tablet, and desktop breakpoints
- Check overlay components (Dialog, Sheet, Drawer) at small viewports
- Confirm form layouts remain usable at narrow widths

---

## 6. Component Audit (via MCP or CLI)

```bash
# Use the audit checklist from MCP
# shadcn:get_audit_checklist

# Or manually verify imports, dependencies, and lint
npx shadcn@latest info
```