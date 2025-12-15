## 2024-02-14 - [Keyboard Accessibility & SR Context]
**Learning:** External links often lack context for screen reader users. Adding visually hidden text "(opens in a new tab)" alongside `target="_blank"` significantly improves the experience. Also, default browser focus rings are sometimes insufficient; explicit `focus-visible` styles ensure keyboard users don't lose track of their position.
**Action:** Always include `sr-only` context for external links and define explicit `focus-visible` states for interactive elements.
