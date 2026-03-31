# Framework-specific Fix Guide

각 framework와 styling method에 맞는 fix pattern을 다룬다.

---

## 목차

1. Pure CSS / SCSS
2. Tailwind CSS
3. React + CSS Modules
4. styled-components / Emotion
5. Vue (Scoped Styles)
6. Svelte

---

## 1. Pure CSS / SCSS

### Layout Overflow Fix

```css
/* Before: Overflow 발생 */
.container {
  width: 100%;
}

/* After: Overflow 제어 */
.container {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}
```

### Text Clipping Prevention

```css
/* 단일 줄 truncation */
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 다중 줄 truncation */
.text-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Word wrapping */
.text-wrap {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}
```

### Spacing Unification

```css
/* CSS custom properties로 spacing 통일 */
:root {
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

.card {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}
```

### Contrast Improvement

```css
/* Before: Contrast 부족 */
.text {
  color: #999999;
  background-color: #ffffff;
}

/* After: WCAG AA standards 충족 */
.text {
  color: #595959; /* Contrast ratio 7:1 */
  background-color: #ffffff;
}
```

---

## 2. Tailwind CSS

### Layout Fixes

```jsx
{/* Before: Overflow */}
<div className="w-full">
  <img src="..." />
</div>

{/* After: Overflow 제어 */}
<div className="w-full max-w-full overflow-hidden">
  <img src="..." className="w-full h-auto object-contain" />
</div>
```

### Text Clipping Prevention

```jsx
{/* 단일 줄 truncation */}
<p className="truncate">긴 텍스트...</p>

{/* 다중 줄 truncation */}
<p className="line-clamp-3">긴 텍스트...</p>

{/* Word wrapping */}
<p className="break-words">긴 텍스트...</p>
```

### Responsive Support

```jsx
{/* Mobile-first responsive */}
<div className="
  flex flex-col gap-4
  md:flex-row md:gap-6
  lg:gap-8
">
  <div className="w-full md:w-1/2 lg:w-1/3">
    Content
  </div>
</div>
```

### Spacing Unification (Tailwind Config)

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
      },
    },
  },
}
```

### Accessibility Improvements

```jsx
{/* Focus state 추가 */}
<button className="
  bg-blue-500 text-white
  hover:bg-blue-600
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
">
  Button
</button>

{/* Contrast 개선 */}
<p className="text-gray-700 bg-white"> {/* text-gray-500에서 변경 */}
  Readable text
</p>
```

---

## 3. React + CSS Modules

### Module Scope Fixes

```css
/* Component.module.css */

/* Before */
.container {
  display: flex;
}

/* After: Overflow 제어 추가 */
.container {
  display: flex;
  flex-wrap: wrap;
  overflow: hidden;
  max-width: 100%;
}
```

### Component-side Fixes

```jsx
// Component.jsx
import styles from './Component.module.css';

// Before
<div className={styles.container}>

// After: Conditional class 추가
<div className={`${styles.container} ${isOverflow ? styles.overflow : ''}`}>
```

---

## 4. styled-components / Emotion

### Style Fixes

```jsx
// Before
const Container = styled.div`
  width: 100%;
`;

// After
const Container = styled.div`
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;
```

### Responsive Support

```jsx
const Card = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  
  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 640px) {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
`;
```

### Theme-based Consistency

```jsx
// theme.js
export const theme = {
  colors: {
    primary: '#2563eb',
    text: '#1f2937',
    textLight: '#4b5563', // Contrast 개선
  },
  spacing: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
  },
};

// Usage
const Text = styled.p`
  color: ${({ theme }) => theme.colors.text};
  margin-bottom: ${({ theme }) => theme.spacing.md};
`;
```

---

## 5. Vue (Scoped Styles)

### Scoped Style Fixes

```vue
<template>
  <div class="container">
    <p class="text">Content</p>
  </div>
</template>

<style scoped>
/* 해당 component에만 적용 */
.container {
  max-width: 100%;
  overflow: hidden;
}

.text {
  /* Fix: Contrast 개선 */
  color: #374151; /* Was: #9ca3af */
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
}
</style>
```

---

## 6. Svelte

### Component Style Fixes

```svelte
<div class="container">
  <p class="text">Content</p>
</div>

<style>
.container {
  max-width: 100%;
  overflow: hidden;
}

.text {
  color: #374151; /* Contrast 개선 */
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
}
</style>
```

---

## Common Fix Patterns

### Overflow Pattern

| Issue | CSS Fix | Tailwind Fix |
|-------|---------|--------------|
| Horizontal scrollbar | `overflow-x: hidden` | `overflow-x-hidden` |
| Content overflow | `max-width: 100%` | `max-w-full` |
| Image overflow | `object-fit: contain` | `object-contain` |

### Text Handling Pattern

| Issue | CSS Fix | Tailwind Fix |
|-------|---------|--------------|
| Single line truncate | `overflow: hidden; text-overflow: ellipsis; white-space: nowrap` | `truncate` |
| Multi-line clamp | `-webkit-line-clamp: N` | `line-clamp-N` |
| Word break | `word-wrap: break-word` | `break-words` |

### Contrast Pattern

| Issue | Before | After |
|-------|--------|-------|
| Low contrast text | `color: #999999` | `color: #595959` |
| Placeholder text | `color: #9ca3af` | `color: #6b7280` |
| Disabled text | `color: #d1d5db` | `color: #9ca3af` |

---

## Fix 적용 원칙

1. **Minimal Changes**: 문제 해결에 필요한 최소 변경만 적용
2. **Respect Existing Patterns**: 프로젝트 기존 code style 따름
3. **Avoid Breaking Changes**: 다른 영역에 side effect 주지 않도록 주의
4. **Add Comments**: fix 이유 설명하는 comment 추가