# 다크 모드

class 기반 다크 모드를 `@custom-variant dark`로 설정하고, CSS 변수 오버라이드와 ThemeProvider로 제어한다.

---

## 1. @custom-variant dark 설정

`.dark` 클래스와 `.system` 클래스를 모두 지원하는 커스텀 variant를 정의한다:

```css
@custom-variant dark {
  &:where(.dark *, .dark) {
    @slot;
  }

  &:where(.system *, .system) {
    @media (prefers-color-scheme: dark) {
      @slot;
    }
  }
}
```

- `.dark`: 사용자가 명시적으로 다크 모드를 선택
- `.system`: 시스템 설정을 따름 (`prefers-color-scheme: dark` 일 때 활성화)
- `.light`: 기본 상태 (추가 설정 불필요)

```tsx
<button className="bg-gray-900 text-white dark:bg-gray-100 dark:text-gray-900">
  Toggle
</button>
```

---

## 2. CSS 변수 오버라이드 패턴

디자인 토큰으로 다크 모드를 관리하면 `dark:` variant를 매번 적지 않아도 된다:

```css
:root {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.15 0 0);
  --color-primary: oklch(0.55 0.2 250);
  --color-primary-foreground: oklch(1 0 0);
  --color-border: oklch(0.85 0 0);
  --color-muted: oklch(0.96 0 0);
  --color-muted-foreground: oklch(0.45 0 0);
}

.dark {
  --color-background: oklch(0.15 0 0);
  --color-foreground: oklch(0.95 0 0);
  --color-primary: oklch(0.65 0.2 250);
  --color-primary-foreground: oklch(0.1 0 0);
  --color-border: oklch(0.3 0 0);
  --color-muted: oklch(0.2 0 0);
  --color-muted-foreground: oklch(0.65 0 0);
}
```

```tsx
// dark: prefix 없이 자동 전환
<div className="bg-background text-foreground border-border">
  Always correct
</div>
```

---

## 3. ThemeProvider 구현

```tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";

type Theme = "dark" | "light" | "system";

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  resolvedTheme: "dark" | "light";
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "theme",
}: {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
}) {
  const [theme, setTheme] = useState<Theme>(defaultTheme);
  const [resolvedTheme, setResolvedTheme] = useState<"dark" | "light">("light");

  useEffect(() => {
    const stored = localStorage.getItem(storageKey) as Theme | null;
    if (stored) setTheme(stored);
  }, [storageKey]);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove("light", "dark", "system");

    if (theme === "system") {
      root.classList.add("system");
      const resolved = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      setResolvedTheme(resolved);
    } else {
      root.classList.add(theme);
      setResolvedTheme(theme);
    }

    // 모바일 브라우저 상단바 색상 변경
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", resolvedTheme === "dark" ? "#09090b" : "#ffffff");
    }
  }, [theme, resolvedTheme]);

  return (
    <ThemeContext.Provider
      value={{
        theme,
        setTheme: (newTheme) => {
          localStorage.setItem(storageKey, newTheme);
          setTheme(newTheme);
        },
        resolvedTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within ThemeProvider");
  return context;
}
```

---

## 4. ThemeToggle 컴포넌트

```tsx
import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/providers/ThemeProvider";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      aria-label="Toggle theme"
    >
      <Sun className="size-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute size-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </button>
  );
}
```

---

## 5. FOUC(Flash of Unstyled Content) 방지

SSR/SSG 환경에서 첫 로드 시 깜빡임을 방지하려면 `<head>`에 인라인 스크립트를 넣는다:

```html
<script>
  (function() {
    var stored = localStorage.getItem('theme');
    if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    }
  })();
</script>
```

Next.js App Router에서는 `layout.tsx`의 `<head>` 또는 `<Script strategy="beforeInteractive">`에 넣는다.

---

## 빠른 체크리스트

- `@custom-variant dark`에 `.dark`와 `.system` 둘 다 정의했는가?
- CSS 변수 오버라이드로 토큰 기반 다크 모드를 구성했는가?
- ThemeProvider가 `localStorage`에 선택을 저장하는가?
- `meta[name="theme-color"]`을 업데이트하여 모바일 상단바에 반영하는가?
- SSR 환경에서 FOUC 방지 인라인 스크립트를 넣었는가?
