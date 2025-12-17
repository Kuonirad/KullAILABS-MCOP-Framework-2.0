## 2024-02-14 - Accessible Link Patterns
**Learning:** Default external links lack screen reader context and tactile feedback, making the UI feel "flat" and less accessible.
**Action:** Always include `active:scale-95` for button-like links, `focus-visible` rings using theme colors, and `sr-only` spans for external link context.

## 2024-02-14 - Directional Micro-interactions
**Learning:** Static arrow icons in links (→) miss an opportunity to reinforce directionality. Animating the arrow on hover (translating x) creates a subtle, delightful affordance that encourages action.
**Action:** Wrap directional characters/icons in a span with `group-hover:translate-x-1` (and `motion-reduce:transform-none`) when the parent link is hovered.
