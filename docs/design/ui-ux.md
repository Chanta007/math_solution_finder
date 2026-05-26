# UI / UX Design

> Last updated: <!-- DATE -->

## 1. Purpose

Defines the user interface conventions: component library, responsive design strategy, accessibility standards, and interaction patterns. Every user-facing surface follows these patterns.

<!-- CUSTOMIZE: Remove this entire file if your project has no web UI. -->

## 2. Key Files

| File | Responsibility |
|------|---------------|
| <!-- e.g., `src/components/ui/` --> | Base UI components (owned copy-paste from component library) |
| <!-- e.g., `src/components/` --> | Application-specific components |
| <!-- e.g., `src/app/globals.css` --> | Global styles, CSS custom properties |
| <!-- e.g., `tailwind.config.ts` --> | Theme configuration |

## 3. Architecture

### Component Library

<!-- CUSTOMIZE: Choose your component library. -->

**Recommended: shadcn/ui + Radix** (copy-paste ownership, full control)
- Components copied into `components/ui/` — you own them
- Radix primitives for accessibility
- Tailwind for styling
- Not a framework dependency — just source files

**Alternative: Material UI, Ant Design, Chakra** (framework approach)
- Imported as npm dependency
- Less control, more out-of-box features

### Component Hierarchy

```
Page (server component, data fetching)
  └─ Layout (responsive shell)
      └─ Feature Component (client, interactive)
          └─ UI Component (from component library)
```

### Server vs Client Components

- **Server Components** (default): Data fetching, auth checks, no interactivity
- **Client Components** (`"use client"`): User interaction, state, effects

Data flows: Server Component fetches → serializes → passes as props to Client Component.

## 4. Responsive Design

### Breakpoints

| Breakpoint | Width | Target |
|------------|-------|--------|
| Mobile | 375px - 767px | iPhone SE through large phones |
| Tablet | 768px - 1279px | iPad, small laptops |
| Desktop | 1280px+ | Standard desktop |

### Rules

- **Mobile-first**: Default styles target mobile. Use `min-width` media queries to add desktop styles.
- **No horizontal scroll**: Every component fits within viewport width at 375px.
- **Touch targets**: Minimum 44px × 44px (per Apple HIG).
- **`dvh` over `vh`**: Use dynamic viewport height for full-height layouts (accounts for mobile browser chrome).
- **Test on real devices**: Browser resize is not sufficient for mobile testing.

### Navigation

| Viewport | Navigation Pattern |
|----------|-------------------|
| Mobile | Hamburger menu or bottom tab bar |
| Tablet | Collapsible sidebar |
| Desktop | Full sidebar or top navigation bar |

Navigation state persists across page transitions.

## 5. Visual Design

### Principles

- **Content-first**: Minimize chrome. Every pixel serves a function.
- **Clean & clear**: Generous whitespace. Clear visual hierarchy. No decorative clutter.
- **Consistent**: Same patterns everywhere. Buttons look like buttons. Links look like links.
- **Dark mode**: Support light and dark themes via CSS custom properties or Tailwind dark mode.

### Color

- Use semantic color tokens (`--color-primary`, `--color-error`) not raw hex values
- Ensure WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Color is not the only indicator (use icons, text, patterns alongside)

### Typography

- System font stack for performance (or a single web font family)
- Clear hierarchy: headings, body, captions
- Line height: 1.5 for body text, 1.2 for headings
- Maximum line length: ~65-75 characters for readability

## 6. Loading & Error States

### Loading

- **Initial page load**: Skeleton screens (not spinners)
- **Action in progress**: Inline spinner or progress indicator on the trigger element
- **Background processing**: Toast notification or status badge
- **AI/LLM streaming**: Progressive text rendering with cursor indicator

### Errors

- Every error has a **user-facing message** (no raw error codes or stack traces)
- **Recovery actions** where possible ("Retry", "Go back", "Contact support")
- Error messages are visible without scrolling
- Form validation errors appear next to the relevant field

## 7. Accessibility

### Minimum Standards

- **Semantic HTML**: Use `<nav>`, `<main>`, `<button>`, `<label>`, etc.
- **ARIA labels**: On all interactive elements that lack visible text
- **Keyboard navigation**: Tab order follows visual order. Focus indicators visible.
- **Screen reader**: Key flows tested with VoiceOver/NVDA
- **Contrast**: WCAG AA minimum (4.5:1 normal text, 3:1 large text)
- **Motion**: Respect `prefers-reduced-motion` media query

### Interactive Elements

- Buttons have visible focus states
- Form inputs have associated labels
- Dialogs trap focus while open
- Dropdown menus support arrow key navigation

## 8. Forms

- Large touch targets on mobile
- Appropriate input types (`type="email"`, `type="tel"`, `inputmode="numeric"`)
- Real-time validation feedback (not just on submit)
- Error messages visible without scrolling
- Auto-focus first field on page/dialog open
- Submit on Enter key where appropriate

## 9. Cross-references

- **[CONSTRAINTS.md](../CONSTRAINTS.md)** — Mobile UX constraints (§10)
- **[design/core-architecture.md](core-architecture.md)** — Rendering strategy
