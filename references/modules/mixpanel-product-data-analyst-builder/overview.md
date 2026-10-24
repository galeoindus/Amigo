# Module guide: Mixpanel Product Data Analyst — Build Interview

> Integrated capability: build-interview for a Mixpanel Product Data Analyst clone. Calibrate, bind the Mixpanel connector, crawl the data dictionary, and confirm the analyst modules are on the clone. Load this — and only this — when the session is standing up that template.

# Mixpanel Product Data Analyst — build interview

Configuring a **Mixpanel Product Data Analyst** clone. After Step 0, follow the data-schema-crawler module (writes the data dictionary, not a Mixpanel-specific skill).

## Ask with `clarify`, never chat

Every probing question goes through the `clarify` tool. Never ask as plain chat text — that stalls the session and drops tappable choices. 1–4 questions per call. Shape: `{"question": "...", "choices": ["...", "..."], "multi_choice": false}`. Omit `choices` for free-text. Skip anything already answered or that a connector crawl can discover. Do not ask about missing output skills — bind whatever exists and continue.

## What this agent already does

- Plans investigations (`../analytical-planning/overview.md`) before querying.
- Profiles data (`../data-exploration/overview.md`) so schema != reality.
- Answers activation / funnel / retention via `../product-analytics/overview.md` + connectors.
- Runs an RCA loop with validation — not text-to-SQL.
- Carries metric hierarchy, diagnostic order, common traps, and AI product metrics in `../product-analytics/overview.md`.
- Routes deliverables through whichever output skills are bound (PDF, PPTX, DOCX, HTML, XLSX). Never ask the user about a missing format.

You still need: product prefix, skip-filters, and the Mixpanel project.

Product scope is a hard boundary. A saved artifact can be governed and still be out of scope: open it and inspect its events before assigning a metric role. Do not put out-of-scope artifacts in the metric table or playbook. For a `payments.` build, a `marketing.*` report belongs only in the excluded/landmines section.

## Bind (if missing on the target)

Core analyst modules: analysis validation, analytical planning, dashboard design, data dictionary, data exploration, descriptive statistics, metric reasoning, root-cause analysis, segmentation drilldown, statistical inference, time-series analysis, visualization, data-schema-crawler, and this builder.
Domain: product analytics.
Output: bind every live PDF / presentation / DOCX / HTML / XLSX output skill onto the clone. Skip ones that do not exist. Do **not** `clarify` about a missing output skill.
Connectors: Mixpanel (required), code sandbox (required), web search (optional), vision (optional).

## Probing questions

Two `clarify` batches after the crawl — never these as chat. Do not ask them to list 130 event names.

**Batch 1**
1. `"Which product / event prefix should I track?"` — free-text. If unknown, list events with a keyword first, then offer discovered prefixes as `choices`.
2. `"In your words, what is activation?"` — free-text; confirm against crawled events.
3. `"Any internal or test traffic I should skip?"` — free-text.

**Batch 2**
4. `"Which Mixpanel project should I use?"` — free-text, or `choices` from the project list if already available.
5. `"Chat answers only, or also a weekly digest file?"` — choices `["Chat only", "Chat and a weekly digest file"]`.

## UAT

- "What's our activation rate this week vs last?"
- "Where do users drop in the first-session funnel?"
- "Why did feature adoption move?"
- "Is the AI product working? Show me task success and retry rate."
- "Build me a weekly digest PDF with the 6 governing KPIs."

## Routing

The template's first sample prompt must stay: 'Set up this Mixpanel Product Data Analyst. Crawl the connected data stores, write the data dictionary, and ask only what the tools cannot discover.' The Agent Creator matches that line to this builder. Do not load the general product-analytics builder (that belongs to a different template).
