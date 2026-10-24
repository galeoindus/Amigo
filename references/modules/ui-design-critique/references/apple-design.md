# Apple Design Principles & Critique Vocabulary

Use this to ground the layout, typography, color, components, and psychology sections in named principles. Cite the principle by name in the critique.

## Apple's three core themes (modern HIG)

- **Clarity.** Text is legible at every size, icons are precise, adornments are subtle, and the design sharpens focus on function. Negative space, color, fonts, and imagery all work to highlight what matters. *Failure looks like:* nothing dominates, decoration competing with content, ambiguous icons.
- **Deference.** The UI helps people understand and interact with content but never competes with it. Chrome (bars, controls, backgrounds) recedes; content leads. *Failure looks like:* heavy borders/shadows/gradients pulling attention off the actual content, a loud shell around quiet substance.
- **Depth.** Visual layers and realistic motion convey hierarchy and give life; transitions communicate where you are and where you came from. *Failure looks like:* flat, ambiguous stacking; state changes with no motion cue.

## Classic macOS HIG heuristics (still cited)

These predate the three themes and remain useful vocabulary:

- **Metaphors** — familiar real-world concepts lower learning cost.
- **Direct manipulation** — users act on visible objects and see immediate results.
- **See-and-point (recognition over recall)** — show options rather than requiring memorized commands.
- **Feedback** — every action produces a visible, immediate response.
- **Consistency** — same thing looks/behaves the same everywhere, within the app and with platform conventions.
- **WYSIWYG** — what you see is what you get; no hidden state.
- **User control** — the user initiates and controls actions, not the app.
- **Forgiveness** — actions are reversible; destructive ones are guarded; errors are recoverable.
- **Perceived stability** — a consistent, understandable structure the user can rely on.
- **Aesthetic integrity** — the look matches the function and the content's seriousness.
- **Modelessness** — avoid trapping the user in modes that change what the same action does.
- **Accessibility** — usable by the widest range of people and abilities.

## Gestalt principles (for layout & hierarchy)

How the eye groups elements. Name the specific one:

- **Proximity** — things placed close together are read as related. Misuse: even spacing everywhere, so nothing groups; or a label far from its field.
- **Similarity** — shared color/shape/size implies same category. Misuse: unrelated items styled alike; related items styled differently.
- **Common region** — a shared background/border groups items. Cards, panels.
- **Continuity** — the eye follows lines and alignment; strong edges guide reading order.
- **Closure** — the mind completes shapes; lets you imply structure without heavy borders.
- **Figure/ground** — clear separation of foreground content from background. Weak figure/ground = content that doesn't pop.
- **Common fate** — elements moving together are grouped (motion/animation).

## Hierarchy & spacing checklist

- Is there ONE clear focal point per screen that matches the stated purpose? (Squint test: what survives when you blur the image?)
- Does hierarchy use multiple reinforcing signals (size + weight + color + position + whitespace), not just one?
- Is the spacing built on a consistent scale (e.g. 4/8pt system)? Random gaps read as sloppy; a rhythm reads as intentional.
- Is whitespace used to group (proximity) and to give the focal point room, or is everything crammed edge-to-edge (deference failure — no breathing room for content)?
- Is alignment disciplined? Elements should share edges/baselines on a grid. Stray misalignments read as errors even when users can't name them.
- Are related controls grouped and unrelated ones separated (proximity + common region)?

## Typography checklist

- **Scale:** a small, deliberate set of sizes/weights with clear jumps between levels. If body, caption, and subhead are within a couple points of each other, hierarchy collapses.
- **Legibility:** body text large enough (≥16px web body is a safe floor), line height ~1.4–1.6, line length ~45–75 characters. Too-long lines tire the eye; too-short lines fragment reading.
- **Pairing:** ideally one family, two at most, with roles (display vs text). More families fragment the voice (aesthetic-integrity / consistency).
- **Balance:** avoid widows/orphans in headlines and short blocks — rewrite or rebalance line breaks so paragraphs make even shapes. Users feel this as care.
- **Alignment:** left-aligned for long-form Latin text; avoid justified text on the web (uneven rivers). Centered text only for short blocks.

## Color & contrast checklist

- **Discipline:** a limited palette with defined roles (primary, neutral ramp, one or two accents, semantic success/warning/danger). A page with many unrelated hues reads as chaotic.
- **Semantic consistency:** if blue means "interactive" once, it must mean it everywhere; don't reuse the action color for decoration.
- **Contrast (WCAG 2):** body/normal text ≥ **4.5:1**; large text (≥24px, or ≥19px bold) ≥ **3:1**; UI components and graphical objects ≥ **3:1** against adjacent colors. The most common real-world failure is light-gray secondary text on white.
- **Never rely on color alone** to convey meaning (state, required fields, errors, chart series) — pair with text, icon, or shape. This is an explicit Apple accessibility rule and helps colorblind and low-vision users.
- **Dark mode / elevation:** if shown, check that layers are distinguishable and contrast holds.

## Interaction & cognitive laws

- **Fitts's law** — time to hit a target grows as it shrinks and as it gets farther away. Implication: important/frequent controls should be larger and closer; touch targets ≥ ~44×44pt; screen corners/edges are "infinite" targets (easy to hit). Pointer input tolerates smaller, denser targets than touch.
- **Hick's law** — decision time grows with the number/complexity of choices. Implication: reduce or group options; use progressive disclosure; don't present ten equal-weight actions.
- **Miller's law (~7±2)** — working memory is limited; chunk information into groups.
- **Jakob's law** — users expect your product to work like the others they already know; deviating from platform conventions costs them effort (ties to consistency).
- **Affordances & signifiers** — an affordance is a possible action; a signifier is the perceptible cue that reveals it (a button that looks raised/tappable). Flat design often strips signifiers — check that interactive elements still *look* interactive and static ones don't.
- **Aesthetic-usability effect** — attractive interfaces are perceived as more usable and are more forgiven for minor issues; polish buys goodwill but never substitutes for clarity.

## Motion (when relevant / from "Designing Fluid Interfaces")

- Motion should be **interruptible, responsive, and continuous** — tied to user input, not canned animations that block interaction.
- Transitions should communicate spatial relationships (where this came from, where it goes) — supporting **depth**.
- Gratuitous animation that delays the user violates deference and user control.