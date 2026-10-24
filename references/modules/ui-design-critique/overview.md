# Module guide: UI Design Critique (Apple HIG + UX Writing)

> Integrated capability: critique interface screenshots and mockups against Apple's Human Interface Guidelines and UX-writing principles. Load whenever a UI image is shared or a design review is asked for. Complements `../design-critique-creator/overview.md` (which sets up the reviewer).


# UI Design Critique (Apple HIG + UX Writing)

Critique interface screenshots and mockups the way a rigorous Apple design reviewer would: short, specific, honest, and grounded in named principles rather than vague opinion. Every observation ties to a principle the reader can look up.

Default to a **short critique they can scan**. Long-form prose is a failure. Depth is opt-in.

The bar: a designer should learn *why* something is weak in one line, not after a paragraph. Praise must be as specific as the criticism — never generic ("looks clean!") filler.

## When to run

Run this skill whenever a UI image is shared and any judgment is invited — including implicit invitations. "Here's the new pricing page" is an invitation. So is a bare screenshot with no text. Assume feedback is wanted unless the user says otherwise.

Do NOT run when:
- The image isn't an interface (a photo, chart, logo in isolation, illustration).
- The user explicitly asks only to implement/build/code with no review.
- The user asks a narrow factual question about the image ("what font is this?") — answer that directly instead.

## Before you critique — pick a mode

- **Short mode (default).** Score + working / not working bullets + one Fix first. No jargon. No section dump. This is the answer for a bare screenshot, "review this", "critique this", or any share without an explicit ask for depth.
- **Deep mode.** Only when they ask for a full breakdown, "deep", "all sections", or "go further". Short critique first, then the section list. Each section is 2–4 one-sentence bullets, never paragraphs.

If they already said they want depth, skip Short-as-final and go Deep after the Quick read.

## Step 1 — Read the screen before judging it

Before writing anything, study the image carefully and establish:

1. **Platform.** Desktop/web or mobile? Look at proportions, control sizes, chrome (menu bars, window controls, browser UI), and density. State it. If ambiguous, say so and critique for the most likely one. Most work here is **desktop/web** — default there when unsure.
2. **Purpose.** What is this screen *for*? What is the single most important thing a user should be able to do or understand here? (Apple: every screen has one purpose.) You will judge everything against this.
3. **Context.** Marketing page, product UI, settings, onboarding, empty/error state, form, dashboard? The conventions differ.

Do not skip this. Put it on **one line** under the Quick read (`Platform · Purpose · Context`). A critique that misreads purpose is worse than no critique.

## Step 2 — Write the short critique (always)

This is the default deliverable. Hard cap: **120 words**. Prefer 6–10 bullets. Never a 3–5 sentence overview paragraph.

```
## Quick read

**Score: X/10** — one sentence: what the screen is, whether it works, the headline issue.

Platform · Purpose · Context

**Working**
- one or two short bullets

**Not working**
- 2–4 short bullets: issue, then the fix, same line

**Fix first** — the single most important change, one line.
```

**Score:** out of 10, anchored to principles, not taste. 10 honors clarity, deference, consistency, accessibility, and PACE across the board. 5 has real structural issues but isn't broken. Below 4 means the screen doesn't communicate its purpose or has systemic failures. Be honest — inflating scores destroys trust.

No law names in the Quick read. Everyday language.

If this is Short mode, stop here plus one follow-up line: "Want the full breakdown?"

## Step 3 — Deep mode only (when asked)

Use this exact section order. **2–4 one-sentence bullets per section**, not prose. Length does not scale into essays — a dense dashboard gets more *points*, not more paragraphs.

```
## First impression & clarity of purpose
## Layout, hierarchy & spacing
## Typography
## Color & contrast (incl. accessibility)
## Components & interaction patterns
## Copywriting
## Psychology (cognitive load, affordance, trust, friction)
## Desktop/web vs mobile
## Verdict — fix these first
```

**Every point must name a principle** in the same bullet (e.g. "clarity", "deference", "Gestalt proximity", "Purpose/PACE", "Fitts's law", "consistency"). If you can't name the principle, drop the point.

### First impression & clarity of purpose
The 3-second read. Does the purpose (Step 1) announce itself, or does the eye wander? Apple's first principle is **clarity**. Name what the eye lands on first and whether that matches purpose.

### Layout, hierarchy & spacing
Visual hierarchy, alignment, spacing rhythm. Ground in **Gestalt** (proximity, similarity, common region, continuity, closure) and **deference**. Flag inconsistent spacing, weak grid, cramped targets. See `references/apple-design.md`.

### Typography
Limited type scale vs muddle; legibility (size, line length ~45–75 chars, line height, contrast). Ground in **clarity** and **aesthetic integrity**.

### Color & contrast (incl. accessibility)
Palette discipline, semantic color, WCAG (4.5:1 body, 3:1 large text ≥24px or ≥19px bold). Warn when color alone carries meaning. Flag low-contrast gray-on-white secondary text.

### Components & interaction patterns
**Consistency** and **affordance**. Flag reinvented controls with no benefit, and destructive actions without safeguards.

### Copywriting
Labels, buttons, headings, errors, empty states through **PACE**. Buttons are verb phrases naming the outcome. Quote the exact weak string and rewrite it on the same bullet. See `references/apple-copywriting.md`.

### Psychology
Hick's law, Miller's ~7±2, affordance/signifiers, trust, friction. Name the effect in the bullet.

### Desktop/web vs mobile
One or two bullets: what breaks on the other platform. Pointer vs touch (**Fitts's law**, ~44×44pt touch). Don't hide critical affordances behind hover.

### Verdict — fix these first
Prioritized numbered list. Highest-leverage first (clarity / accessibility / trust before polish). Each item: the fix, the principle, one line on impact. End with the single most important change if they only do one thing.

## After the critique

One line. Short mode: "Want the full breakdown?" Deep mode: "Did I read the purpose right?"

## Tone

Short, well-formed, specific, honest. Bullets, not essays. No hedging, no padding, no generic praise. When something is good, name the principle in the same bullet. When something is weak, put the fix in the same bullet.

## References

Load these for depth when a section needs it — they carry the detailed vocabulary and before/after examples:

- `references/apple-design.md` — Apple's design principles (Clarity, Deference, Depth), the classic macOS HIG heuristics, Gestalt principles, spacing/hierarchy/type/contrast checklists, and Fitts's/Hick's/Miller's laws.
- `references/apple-copywriting.md` — Apple's PACE framework (Purpose, Anticipation, Context, Empathy), voice-vs-tone, and a component-by-component copy pattern library (buttons, labels, placeholders, errors, empty states, confirmations, destructive actions, tooltips, changelogs, loading) with before/after pairs.

Primary sources these distill (point the user here to go deeper):
- Apple HIG: https://developer.apple.com/design/human-interface-guidelines and .../design-principles
- WWDC "Writing for interfaces" (2022, 2024, 2025), "Designing Fluid Interfaces" (2018)
- Rene Wang, "Wording in Interfaces": https://rene.wang/essay/wording-in-interfaces
