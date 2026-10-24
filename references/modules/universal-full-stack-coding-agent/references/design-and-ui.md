# UI, UX, Visual Design and Accessibility Playbook

## 1. Begin with the user, not decoration

Define the primary user, their context, their main job-to-be-done, the most important action, and what success looks like. Map the shortest happy path and the most likely failure paths. Ask whether each screen and component helps users complete a task.

## 2. Design brief

- Product and audience:
- Main user goal:
- Secondary goals:
- Brand attributes (3-5 words):
- Existing brand assets and constraints:
- Information architecture / sitemap:
- Primary journey:
- Content requirements and real data examples:
- Platform and viewport range:
- Accessibility/localization needs:
- Performance constraints:
- References and why they are relevant:
- Acceptance checks:

## 3. Design system essentials

Create semantic tokens instead of arbitrary values scattered across screens:

- Color roles: background, surface, text, muted text, border, primary action, secondary action, focus, success, warning, danger.
- Typography: family, scale, weight, line-height, reading width, heading/body/caption roles.
- Spacing: consistent scale, content gutters, section rhythm, component padding.
- Shape/elevation: radii, border styles, layering and shadows used with restraint.
- Layout: breakpoints, content max-width, grid, stacking behavior.
- Components: button, link, input, select, checkbox, radio, switch, dialog, menu, tabs, table, card, alert, toast, skeleton, pagination.
- States: default, hover, focus-visible, active, disabled, loading, error, success, empty.
- Motion: purpose, duration, reduced-motion behavior.
- Iconography: consistent source, size, stroke/fill rules, accessible labels.

The semantic meaning of a color must not be the only way status is communicated. Check text/background contrast and visible keyboard focus.

## 4. Layout and responsive rules

- Establish hierarchy through content, typography, spacing, alignment and placement.
- Prefer a consistent spacing system and readable content widths.
- Use responsive layouts that adapt; do not merely scale a desktop canvas down.
- Check common phone, tablet and desktop sizes plus a narrow viewport and 200% zoom.
- Avoid horizontal overflow; test long names, translations, tables, error messages and empty datasets.
- Navigation should expose current location and a predictable way back.
- Preserve meaningful content order when columns stack or items reflow.
- Prioritize a clear primary CTA; do not make multiple competing actions equally loud.

## 5. UX states are part of the design

Every asynchronous flow should have appropriate loading/progress feedback, success confirmation, failure recovery, and duplicate-submission protection. Every collection should consider loading, empty, filtered-empty, error, pagination and permission-denied states. Destructive actions should explain the consequence and offer cancellation; provide undo when practical.

Forms should have persistent labels, expected formats, clear required/optional rules, inline error messages, field-level semantics, helpful error summaries where appropriate, and preserved user input after validation failure. Placeholder text is not a label.

## 6. Accessibility baseline

Aim for WCAG 2.2 AA when applicable. At minimum:

- Semantic elements and correct heading hierarchy
- Full keyboard navigation, visible focus, logical focus order
- Accessible names and instructions for controls
- Labels and programmatically associated errors
- Sufficient text and non-text contrast
- Text resize/reflow without loss of content or function
- Touch targets large enough for the context and spacing to reduce accidental activation
- Keyboard-accessible menus, dialogs, tabs and custom widgets
- Focus management and return focus for dialogs
- Status announcements for asynchronous changes where appropriate
- Alternative text for informative images; empty alt for decorative images
- Captions/transcripts for meaningful media where applicable
- Reduced-motion support and no harmful flashing
- Manual keyboard review alongside automated scanners

Automated accessibility tools catch only a subset of issues. Do not claim full WCAG conformance based only on a scanner.

## 7. Visual QA protocol

1. Run the project in a browser/device preview.
2. Inspect at least one narrow mobile viewport and one desktop viewport.
3. Compare against the approved brief/reference if supplied.
4. Check typography, spacing, content density, visual hierarchy, alignment, image crop, responsive breakpoints, focus states, hover/pressed states, and form errors.
5. Test actual navigation and controls; a static screenshot cannot prove functionality.
6. Look for console errors, broken images, layout shift, horizontal overflow and clipped content.
7. Fix the highest-impact issues first; do not spend time polishing micro-details while critical routes or errors remain.
8. Record screenshots/observations and retest after final changes.

## 8. Redesign audit score

Score each 0-4: 0 = missing/broken, 1 = poor, 2 = adequate with gaps, 3 = strong, 4 = excellent and verified.

- Clarity of value proposition
- Navigation and information architecture
- Primary journey completion
- Mobile responsiveness
- Typography and visual hierarchy
- Consistency/design system
- Forms and feedback states
- Accessibility and focus/keyboard behavior
- Performance/perceived speed
- Trust, privacy cues and error recovery
- Content quality and SEO if relevant
- Functional correctness

For each low score, record impact, evidence, recommended change, effort, dependency and success metric. Prioritize severity and user impact rather than aesthetics alone.

## 9. Avoid common AI-generated design failures

- Same generic gradient/card layout regardless of product.
- Fake logos, fake product screenshots, fake testimonials, fabricated metrics or placeholder content presented as real.
- Overuse of pill buttons, glass cards, shadows, animation and rounded rectangles.
- Tiny low-contrast text, decorative icons without names, and icon-only primary actions.
- A visually attractive first viewport with unfinished lower sections or broken mobile layout.
- Controls that appear interactive but do nothing.
- Modifying branding or product semantics without permission.
