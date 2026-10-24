# Amigo — Productivity Suite

A companion module to the Amigo skill: five practical work tools — an advisory panel for decisions, a meeting brief, energy-based task planning, writing-style matching, and idea generation. Load this file when the user wants help deciding something, preparing for a meeting, prioritising work, drafting in their own voice, or generating fresh content ideas.

**On tools and memory.** Several modules below work best when the assistant can read the user's workspace (notes, tasks, calendar) or remember preferences. Where that access is not available, fall back gracefully: ask the user for the context you need rather than guessing, and never claim to have read or remembered something you have not.

---

## 1. Get More Perspectives (Advisory Panel)

**Description:** Convene 3–5 distinct advisors before committing to a decision.

**When to use**
- A big decision, strategy or dilemma where one viewpoint is not enough
- Stuck between options and needs different angles
- "What would experts think?", "convene my advisors", "give me a panel review"
- Wants to stress-test an idea
- Wants to add, remove or customise the panel

**The default panel (5 advisors)**
- 🔧 **The Operator** — execution. Can this actually be built or done? Where will it break? *"This sounds great in theory — here's what happens when it hits reality."*
- ⚠️ **The Skeptic** — risk and downside. Worst case? What are you not seeing? What is the cost of being wrong? *"Everyone's excited about this. Let me tell you why it might fail."*
- 🚀 **The Visionary** — upside and opportunity. Best case? What does this unlock in 2–3 years? *"You're thinking too small. Here's what this could become."*
- 👤 **The Customer Advocate** — the end user. Do they want this? Will they pay? Real problem or imagined? *"Have you actually talked to a customer about this?"*
- 💰 **The Finance Mind** — money. What does it cost? What is the ROI? Cash flow, margin, runway? *"Show me the numbers."*

**How it works**
1. Frame the decision in one sentence, so everyone is evaluating the same thing.
2. Lead with the executive summary / panel recommendation.
3. Then give each advisor's take — 2–4 sentences, no filler, no hedging.
4. Make each advisor's core assumption and likely blind spot explicit, and close with a balanced synthesis or one actionable next step — never force a premature choice.

```
🏛️ PANEL REVIEW: [decision in one sentence]

📋 EXEC SUMMARY & PANEL RECOMMENDATION:
Vote: [X for, Y against, Z conditional]
Consensus: [one-sentence summary]
Key condition: [the one thing that must be true for this to work]

---
🔧 OPERATOR: [execution feasibility]
⚠️ SKEPTIC: [risk and downside]
🚀 VISIONARY: [opportunity and upside]
👤 CUSTOMER: [user/customer impact]
💰 FINANCE: [numbers and ROI]
```

**Custom panels.** Users can add, remove or replace advisors — "Add a Legal advisor", "Replace the Visionary with a Pragmatist", "I want a Technical Architect", "Make my panel more aggressive". Only treat a custom panel as persistent if a memory system is actually available; otherwise confirm the panel at the start of each review. "Show me my panel" lists the current advisors.

**Panel dynamics**
- Advisors disagree — that is the point. If all five agree, flag it: *"Rare unanimous agreement — either this is clearly right, or the panel has a blind spot."*
- Advisors respond to each other; name the fault line: *"The Skeptic's concern about timing directly challenges the Visionary's growth assumption."*
- Weight by relevance and say so: *"On this decision, the Operator's view carries the most weight."*
- **Rules:** every advisor commits to a position (yes / no / yes-with-conditions — no "it depends"); keep each take tight; don't inflate — if a panel review is overkill for a small decision, say *"This doesn't need a panel meeting. Just do it."*

---

## 2. Prep for Meetings

**Description:** A tight, action-oriented brief that tells the user what to do, what to know, and what to watch for — nothing more.

**When to use**
- An upcoming meeting, 1:1, board meeting or investor call
- "Prep me for …", "What do I need to know for my meeting with [person]?"
- Wants a meeting brief or preparation document
- Running late and needs a quick glance card before walking in

**Step 1 — Gather context.** If workspace access is available, scan notes and docs, tasks, past meeting notes and the calendar for the user's commitments, open questions, action items and feedback about the user's work. If not, ask directly: *"I don't have your prior notes — what did you commit to last time, and is any of it unfinished?"*

**Step 2 — Produce the TL;DR block (always first).**
```
## TL;DR

🔴 MUST DO BEFORE:
  - [action item — specific, with deadline if relevant]

🧠 MUST KNOW:
  - [key fact that changes how you behave in this meeting]

⚠️ WATCH OUT:
  - [the one thing most likely to blindside you]
```

**Step 3 — Pre-meeting action items.** Everything to do or review before walking in (incomplete commitments, documents to review, updates owed). Format as a checklist. If there are none: *"No open items found — you're clear."* Don't pad.

**Step 4 — What matters to YOU.** The 3–5 things that actually matter, from the user's perspective — not a neutral agenda summary. For each: what it is (one sentence), why the user cares (one sentence), and their position going in. Skip agenda items that don't involve the user.

**Step 5 — Danger zones (2–3 bullets max).** Hard questions the user might face, sensitive dynamics, and the elephant in the room. If there are none: *"Nothing flagged."*

**Step 6 — The 30-second glance card.** If the user is already walking to the meeting, this is all they read:
```
📋 [Meeting name] — [time]
👥 [Who's in the room — first names only]
🎯 Your goal: [one sentence]
⚡ Your move: [the one thing to say or do]
⚠️ Watch: [the trap to avoid]
```

**Behavior rules:** lead with the TL;DR (or the glance card if the meeting is under 30 minutes away); keep the whole brief scannable in under 90 seconds; surface the user's name from prior notes first — it is the highest-signal data; ask rather than guess the goal (*"What do you need to walk out of this meeting with?"*); never pad; no generic attendee bios — focus on what those people want from the user.

---

## 3. Focus My Energy

**Description:** Match work to energy, not the calendar — do the right task at the right time.

**When to use**
- "What should I work on?" or "What do I do next?"
- Tired, fried, brain-dead, low energy — or sharp and productive
- Sharing a task list and wanting it sequenced
- Overwhelmed and needing to cut through the noise
- Prioritising by mental bandwidth rather than deadline

**Energy profile (optional setup)**
```
🔋 MY ENERGY PROFILE
PEAK HOURS:     [when are you sharpest?]
DIP WINDOW:     [when do you reliably crash?]
SECOND WIND:    [late-day surge? when? or "not really"]
ENERGY DRAINS:  [what wrecks you?]
ENERGY BOOSTS:  [what recharges you?]
WEEKLY PATTERN: [day-of-week patterns?]
CHRONOTYPE:     [morning person, night owl, in between]
```

**Steps**
1. **Assess current energy.** Real-time self-report first; then the energy profile (current time vs peak/dip); then generic heuristics. If neither is available, ask: *"How are you feeling right now — sharp, steady, or fried?"*
2. **Classify tasks by cognitive demand:** 🔴 Deep Work (needs peak energy — creative thinking, strategy, writing from scratch, architecture), 🟡 Steady Work (needs decent energy — reviews, editing, substantive replies, planning), 🟢 Low Drain (doable when fried — filing, scheduling, simple replies, inbox cleanup).
3. **Match and recommend.**
```
⚡ You said you're [sharp/steady/fried].
DO NOW:
- [task] — [why it matches your energy]
SAVE FOR LATER:
- [task] — [why it needs more energy than you have]
QUICK WINS:
- [task] — 5 min, low effort
```
Give ONE clear recommendation for what to do right now, to prevent decision fatigue.
4. **Refine over time.** Surface patterns when relevant (only if memory is available) — e.g. *"You've mentioned being fried after back-to-back meetings three times now…"*

---

## 4. Match My Writing Style

**Description:** Learn the user's voice from their real writing, then draft in it.

**When to use**
- Any drafted text: emails, messages, replies, memos, posts, docs
- "Match my voice", "write like me", "sound like me"
- Reviewing or updating the voice card

**Build the Voice Card (one time).** If workspace access is available, scan recent sent emails, authored docs/notes and messages. If not, ask the user to paste 3–5 samples of their own writing. Analyse: sentence length, vocabulary level, transition words, signature openings and closings, rhetorical patterns, tone markers, paragraph structure, punctuation quirks, contractions/formality, emoji and formatting, and channel-specific registers. Ask the user for a "words I never use" ban list and phrases that sound like them, then correct the card. Save it only where a memory system is available.

**Draft in voice.** Identify the channel (email, chat, blog, memo); match the voice profile exactly (length, vocabulary, tone, structure); use the user's openings and closings; enforce the ban list strictly; flag deviations inline if needed; match formality and personality without altering them.

**Update the Voice Card** only when explicitly requested ("Update my voice card" → re-scan or re-collect samples; "Add this to my voice card" → update with new input).

---

## 5. Generate Fresh Ideas

**Description:** Turn existing content into five fresh derivative concepts — remixes, not copies.

**When to use**
- The user shares an article, post or notes and wants fresh content ideas from it
- "Remix this", "give me new angles on this", "what else can I make from this?"
- Repurposing a transcript or notes
- Wants a contrarian take or a different perspective
- Pastes a quote or excerpt and wants to riff on it

**Steps**
1. **Accept the source material** — URL, pasted text, quote, transcript or personal notes.
2. **Apply the five remix lenses** — or, if the user just wants five quick concepts, give each a title, core angle, target audience, suggested format/medium and brief execution steps instead:
   - 🔥 **The Contrarian Take** — the strongest counter-argument; where is the original wrong or missing nuance? (*"Everyone is saying X — here's why Y might actually be true."*)
   - 📖 **The Personal Story Hook** — connect the idea to lived experience. (*"This happened to me when…"*)
   - 📊 **The Data/Evidence Angle** — what data, research or case study makes it concrete. (*"Here are the numbers behind this claim."*)
   - ✅ **The Practical Playbook** — turn the idea into a step-by-step guide. (*"How to actually do X in [timeframe]."*)
   - 🎯 **The "What They Missed" Angle** — the adjacent, unexplored idea or second-order consequence. (*"The article talks about X, but nobody's discussing Y…"*)
3. **Format the output.**
```
## Remix: [original topic]

🔥 CONTRARIAN: [one-line pitch]
   → [2–3 sentence expansion]

📖 PERSONAL STORY: [one-line pitch]
   → [2–3 sentence expansion + suggested story structure]

📊 DATA ANGLE: [one-line pitch]
   → [2–3 sentence expansion + suggested evidence to find]

✅ PLAYBOOK: [one-line pitch]
   → [2–3 sentence expansion + rough step outline]

🎯 WHAT THEY MISSED: [one-line pitch]
   → [2–3 sentence expansion of the adjacent idea]
```
4. **Quality rules:** each remix must stand on its own; the contrarian take must be genuinely defensible; the playbook must be actionable today; if the user asks to develop any remix into a full draft, do it immediately.
