## 2024-02-14 - Accessible Link Patterns
**Learning:** Default external links lack screen reader context and tactile feedback, making the UI feel "flat" and less accessible.
**Action:** Always include `active:scale-95` for button-like links, `focus-visible` rings using theme colors, and `sr-only` spans for external link context.

## 2024-03-20 - Animated Arrow Links
**Learning:** Simple text arrows in links feel static. Separating the arrow allows for playful interaction without breaking text decoration.
**Action:** For links with arrows (→), wrap text in `group-hover:underline` and arrow in `group-hover:translate-x-1`. Use `motion-reduce` to disable animation.
