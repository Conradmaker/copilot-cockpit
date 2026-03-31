# Visual Checklist

실시간 시각 검수에서 체계적으로 확인해야 할 검수 항목 checklist이다.

---

## 목차

1. Layout 검수
2. Typography 검수
3. Color & Contrast 검수
4. Responsive 검수
5. Interactive Element 검수
6. Images & Media 검수
7. Accessibility 검수
8. Performance-related Visual 검수

---

## 1. Layout 검수

### 구조 무결성

- [ ] Header가 화면 상단에 올바르게 fixed/positioned되어 있다
- [ ] Footer가 화면 하단 또는 content 끝에 위치한다
- [ ] Main content area가 중앙 정렬되어 적절한 width를 갖는다
- [ ] Sidebar(있는 경우)가 올바르게 위치한다
- [ ] Navigation이 의도한 위치에 표시된다

### Overflow

- [ ] Horizontal scrollbar가 의도치 않게 표시되지 않는다
- [ ] Content가 parent element에서 overflow하지 않는다
- [ ] Images가 parent container 내에 fit한다
- [ ] Tables가 container width를 초과하지 않는다
- [ ] Code blocks가 wrap 또는 scroll appropriately

### Alignment

- [ ] Grid items가 evenly distributed
- [ ] Flex item alignment가 올바르다
- [ ] Text alignment(left/center/right)가 일관된다
- [ ] Icons와 text가 vertically aligned
- [ ] Form labels와 input fields가 올바르게 positioned

---

## 2. Typography 검수

### Readability

- [ ] Body text font size가 충분하다 (minimum 16px recommended)
- [ ] Line height가 적절하다 (1.5-1.8 recommended)
- [ ] Characters per line이 적절하다 (40-80 characters recommended)
- [ ] Paragraph 간 spacing이 충분하다
- [ ] Heading size hierarchy가 명확하다

### Text Handling

- [ ] Long words가 appropriately wrap
- [ ] URLs과 code가 properly handled
- [ ] Text clipping이 발생하지 않는다
- [ ] Ellipsis(...)가 correctly displays
- [ ] Language-specific line breaking rules가 작동한다

### Fonts

- [ ] Web fonts가 correctly load
- [ ] Fallback fonts가 appropriate
- [ ] Font weights가 intended
- [ ] Special characters와 emoji가 correctly display

---

## 3. Color & Contrast 검수

### 접근성 (WCAG Standards)

- [ ] Body text: Contrast ratio 4.5:1 or higher (AA)
- [ ] Large text (18px+ bold or 24px+): 3:1 or higher
- [ ] Interactive element borders: 3:1 or higher
- [ ] Focus indicators: Background와 sufficient contrast

### Color 일관성

- [ ] Brand colors가 unified
- [ ] Link colors가 consistent
- [ ] Error state red가 unified
- [ ] Success state green이 unified
- [ ] Hover/active state colors가 appropriate

### Color Vision Diversity

- [ ] Information이 shape와 text로 conveyed, color만으로 아님
- [ ] Charts와 diagrams가 color vision diversity 고려
- [ ] Error messages가 color만으로 의존하지 않음

---

## 4. Responsive 검수

### Mobile (~640px)

- [ ] Content가 screen width 내에 fit
- [ ] Touch targets이 44x44px or larger
- [ ] Text가 readable size
- [ ] Horizontal scrolling이 발생하지 않음
- [ ] Navigation이 mobile-friendly (hamburger menu, etc.)
- [ ] Form inputs가 easy to use

### Tablet (641px~1024px)

- [ ] Layout이 tablet에 optimized
- [ ] Two-column layouts가 appropriately display
- [ ] Image sizes가 appropriate
- [ ] Sidebar show/hide가 appropriate

### Desktop (1025px~)

- [ ] Maximum width가 extra-large screens에서 break하지 않음
- [ ] Spacing이 sufficient
- [ ] Multi-column layouts가 correctly function
- [ ] Hover states가 implemented

### Breakpoint Transitions

- [ ] Layout이 screen size change 시 smoothly transition
- [ ] Layout이 intermediate sizes에서 break하지 않음
- [ ] Content가 disappear 또는 duplicate하지 않음

---

## 5. Interactive Element 검수

### Buttons

- [ ] Default state가 clear
- [ ] Hover state가 exists (desktop)
- [ ] Focus state가 visually clear
- [ ] Active (pressed) state가 exists
- [ ] Disabled state가 distinguishable
- [ ] Loading state (if applicable)

### Links

- [ ] Links가 visually identifiable
- [ ] Visited links가 distinguishable (if needed)
- [ ] Hover state가 exists
- [ ] Focus state가 clear

### Form Elements

- [ ] Input field boundaries가 clear
- [ ] Placeholder text contrast가 appropriate
- [ ] Visual feedback on focus
- [ ] Error state display
- [ ] Required field indication
- [ ] Dropdowns가 correctly function

---

## 6. Images & Media 검수

### Images

- [ ] Images가 appropriate size에 display
- [ ] Aspect ratio가 maintained
- [ ] High resolution display support (@2x)
- [ ] Image load failure 시 display
- [ ] Lazy loading behavior가 works

### Video & Embeds

- [ ] Videos가 containers 내에 fit
- [ ] Aspect ratio가 maintained
- [ ] Embedded content가 responsive
- [ ] iframes가 overflow하지 않음

---

## 7. Accessibility 검수

### Keyboard Navigation

- [ ] All interactive elements가 Tab key로 accessible
- [ ] Focus order가 logical
- [ ] Focus traps가 appropriate (modals, etc.)
- [ ] Skip to content link가 exists

### Screen Reader Support

- [ ] Images가 alt text를 갖는다
- [ ] Forms가 labels를 갖는다
- [ ] ARIA labels가 appropriately set
- [ ] Heading hierarchy가 correct (h1→h2→h3...)

### Motion

- [ ] Animations가 excessive하지 않음
- [ ] prefers-reduced-motion이 supported (if possible)

---

## 8. Performance-related Visual 검수

### Loading

- [ ] Font FOUT/FOIT이 minimal
- [ ] Layout shift (CLS)가 occurs하지 않음
- [ ] Image load 시 jumping하지 않음
- [ ] Skeleton screens가 appropriate (if applicable)

### Animation

- [ ] Animations가 smooth (60fps)
- [ ] Scrolling 시 performance issues 없음
- [ ] Transitions가 natural

---

## Priority Matrix

| Priority | Category | Examples |
|----------|----------|----------|
| P0 (Critical) | Functionality breaking | Complete element overlap, content disappearance |
| P1 (High) | Serious UX issues | Unreadable text, inoperable buttons |
| P2 (Medium) | Moderate issues | Alignment issues, spacing inconsistencies |
| P3 (Low) | Minor issues | Slight positioning differences, minor color variations |

---

## Verification Tools

### Browser DevTools

- Elements panel: DOM과 style inspection
- Lighthouse: Performance과 accessibility audits
- Device toolbar: Responsive testing

### Accessibility Tools

- axe DevTools
- WAVE
- Color Contrast Analyzer

### Automation Tools

- Playwright (screenshot comparison)
- Percy / Chromatic (Visual Regression Testing)