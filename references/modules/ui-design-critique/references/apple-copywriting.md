# Apple UX Writing & Interface Copy Patterns

Use this to ground the Copywriting section. Every word in an interface is a design decision; strip away the visuals and the text does most of the work. A pixel-perfect layout with lazy copy reads as broken — the gap is trust. Quote the actual strings from the screenshot and rewrite the weak ones.

## PACE framework (Apple, "Writing for interfaces")

The lens Apple's own UX writers use. PACE = keeping a natural flow so people stay oriented.

- **Purpose.** Every screen has one most-important thing to convey. Establish information hierarchy (headline states the purpose; buttons are clear on their own). Know what to leave out — cut, move, or demote secondary ideas. Tell people the purpose; it's not a secret. Aim for simplicity over exhaustive detail.
- **Anticipation.** Treat the interface as a conversation with back-and-forth. Anticipate the user's next question or action and answer it in place ("What comes next?"). Develop one **voice**, then vary **tone** by situation (celebratory for a milestone, calm and plain in a stressful moment). Use exclamation points rarely.
- **Context.** Consider what's happening outside the app (busy, driving, glancing) and write for that attention budget. Alerts are interruptions — make them helpful, name the specific action on the buttons (never bare Yes/No), put the destructive option clearly. Errors should say what went wrong and exactly what to do. Empty states educate or celebrate and always guide what goes here.
- **Empathy.** Write for everyone: simple, plain language; avoid idioms/humor that don't translate or exclude. Be localization-aware (text length varies, RTL exists). Write thoughtful, descriptive accessibility text for every element, symbol, and image — for some users that text *is* the interface. Prefer "person" over gendered nouns.

Final Apple tip: **read the copy out loud** — it exposes stiffness, repetition, and errors, and checks that it sounds like talking to a friend.

## Voice vs tone

- **Voice** is constant (who the product is — playful game vs trustworthy bank vs kid-friendly app). Define what it would and wouldn't say; keep a term list.
- **Tone** flexes with the moment. Same voice, different tone for an error vs a celebration.

## Component-level copy patterns (before → after)

Cite these when critiquing specific strings. The principle is in **bold**.

- **Buttons — name the outcome (verb phrase).** "Help" (a noun/category) → "Get Help". "Desktop App" → "Download Desktop App". A button label is a promise of what clicking does.
- **Buttons in flows — name the destination.** "Next" → "Continue to payment". Naming where you're going removes a blind-trust click.
- **Settings labels — describe the experience, not the tech.** "Enable two-factor authentication" → "Require a code to sign in". Give toggles a clear on-state ("Send me email notifications"). Use **positive phrasing**: "Renew automatically" beats "Disable auto-renewal". Name the real category ("Billing", not "Advanced"). Descriptions should add new info, not repeat the title.
- **Placeholder text — describe scope, not mechanics.** "Enter keywords" → "Search issues, projects, pages". For inputs, show an example ("contact@rene.wang") rather than restating the field.
- **Error messages — problem + reason + path forward.** "Invalid input." → "This email is already registered. Try signing in instead." Avoid "oops/uh-oh" (patronizing) and hollow "sorry/please".
- **Confirmations — echo the action and the object.** "Successfully saved." → "Your changes to 'Project Alpha' have been saved." Vague reassurance is noise.
- **Empty states — echo intent + offer a next step.** "No results found." → "No results for 'fluxcap'. Try a different keyword or check your spelling." The highest-leverage overlooked moment.
- **Destructive actions — list consequences, don't escalate fear.** Not "WARNING… permanent… irreversible… cannot be undone" (three synonyms, no information) → "Delete 'Landing Page'? 12 published posts will be unpublished · 3 team members will lose access · Cannot be undone." Reframe the safe button as a positive choice ("Keep project" beats "Cancel"). Consequences inform; fear becomes noise users click through.
- **Disabled/locked states — name the reward, not just the gate.** "Available on Pro plan" → "Unlock custom domains → Pro". A disabled control is a desire signal; convert it.
- **Changelogs — describe the outcome, not the diff.** "Fixed custom font rendering issue" → "Your exports now include custom fonts." Name the specific fixed problem ("blank pages on Firefox", not "PDF bug"). Users care about their workflow, not your bugs.
- **Loading copy — name the action + set expectation.** "Please wait…" → "Generating your report (about 6 seconds)" with a live counter, so the wait feels intentional, not broken.
- **FAQ / answer length — brevity signals confidence.** For a trust-sensitive question ("Can I cancel anytime?"), "Yes. No fees, no questions." beats three qualified paragraphs. Length itself is a message; over-explaining reads as hiding.

## Cross-cutting copy rules

- **Consistency of terms.** Pick one noun and one verb per concept and hold them everywhere. "Remove member" for every row beats a mix of "Remove / Kick out / Delete user" — synonyms create micro-doubt ("is Kick out the same as Remove?"). Consistency is a contract that lets users stop reading carefully.
- **No relative dates in persistent copy.** "Expires in 72 hours" → "Expires March 27, 2026." Don't make the reader do math.
- **Positive over negative** phrasing for toggles and actions.
- **Specific over generic** everywhere — echo the user's object/query/action back to them.
- **Visual shape of text** matters: rewrite to kill widows and make paragraphs even; it reads as care.
- **Sentence case** for most Apple UI text (buttons, labels, titles) unless a strong reason for title case; be consistent either way.