# Amigo Changelog

## 1.4.0 — 2026-10-25

- Merged the `ai-coding` pack (31 source packs total): an AI-coding playbook with ten references (including two Hindi guides) plus its bundled `universal-full-stack-coding-agent` companion.
- Fixed a structural defect: the bundled companion shipped as a second `SKILL.md`; it is now `overview.md`, so the package keeps exactly one active manifest.
- Fixed an over-long frontmatter description (1153 chars, above the 1024 limit) by folding the capability and trigger text into a module blurb and a router row.
- Repointed every `bundled/...` cross-link to the merged module paths and renamed the companion README to `references/install-notes.md`.
- Refined the security statistic to separate the controlled-benchmark rate (about 44-45% of tasks produce a vulnerability) from the lower real-repository rate (about 27-30% of snippets), and kept the "secure instructions barely help" finding with its measured size.
- Added code verification and an AI-assisted-coding standard to the root guide; updated the router, module index and validation notes.

## 1.3.0 — 2026-10-25

- Merged four more packs (29 source packs total): visualization, time-series-analysis, ui-design-critique, and skill-creator.
- Rebranded the visualization pack's color grammar, palette and presentation references to Amigo; renamed its `Panja runtime` heading to `Amigo runtime` (matching the package convention).
- Added a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs the package validator, a compile check of every bundled script, and smoke tests of the offline helpers on push and pull request to `main`.
- `skill-creator` keeps its platform references (the host agent and its builder tools); the package's tool-reality rule still applies, so tool names must be verified against the live environment.
- Cross-linked `ui-design-critique` (the critique method) with `design-critique-creator` (the reviewer setup) instead of duplicating them.
- Updated the router, module index and validation notes; one active root manifest remains.

## 1.2.0 — 2026-10-25

- Merged ten additional packs (25 source packs total): metric reasoning, root-cause analysis, segmentation drilldown, statistical inference, product analytics, pptx-master, file organizer (builder + triage taxonomy), Mixpanel product data analyst builder, and presentation agent builder.
- Rebranded the whole package to **Amigo**: every prior brand spelling was removed from paths and text, the prior platform output-skill slugs were replaced with format-neutral routing, and the `Panja runtime` heading became `Amigo runtime`.
- Folded `pptx-master` into the presentation module (`brand-for-pptx`) as `references/template-first-workflow.md` and `references/typography.md`; adopted its Season Mix / Matter type system and hard rules, and made the footer line configurable rather than hard-coding another company's tagline.
- Corrected the statistics helper: replaced the plain Wald interval (poor coverage at small n and extreme proportions) with Newcombe's hybrid and Agresti–Caffo intervals, kept the pooled two-proportion z p-value, and added small-cell and small-sample warnings.
- Corrected the funnel helper: it now enforces step **order** using timestamps (its own STOP list forbids unordered funnels) and flags when no timestamps are present.
- Refined product analytics with a metric contract, rolling-window guidance, explicit Mixpanel retention terminology (on / on-or-after, birth / compounded, rolling / calendar), and the incomplete-cohort caution.
- Added sub-measure (numerator / denominator / mix) decomposition and Simpson's-paradox guidance to metric reasoning and segmentation drilldown; added change-point alignment to root-cause analysis.
- Added the file organizer with Google Drive read-only discovery and `md5Checksum`-based duplicate detection.
- Updated the router, module index, validation notes and research notes; one active root manifest remains.

## 1.1.0 — 2026-10-25

- Integrated five additional packs: data exploration, data schema crawler, deck build standards, descriptive statistics, and design critique creator (15 source packs total).
- Kept one active root `SKILL.md`; imported guides live as reference modules so skill discovery remains unambiguous.
- Namespaced local scripts and updated references/commands for the merged package layout.
- Enhanced dataset profiling to count absent keys as missing, infer numeric strings cautiously, calculate interpolated quantiles, and flag mixed timezone-awareness.
- Enhanced descriptive stats with sample variance/SD, IQR/MAD, Bowley skewness hint, missing/invalid counts and potential outlier candidates without auto-removal.
- Replaced obsolete brand/template assumptions in deck standards with Amigo assets or the user's existing brand/template, and added accessible rendering QA.
- Reworked design critique guidance with tool discovery, screenshot-only fallback, evidence-linked findings and prioritized remediation.
- Refreshed research notes from official OpenAI, Metabase, NIST, W3C, Microsoft and Apple documentation.
- Expanded package QA for old-brand strings in source/code, manifest count, local links, scripts and zip integrity.

## 1.0.0 — 2026-10-24

- Consolidated the initial 10 source skill packs under one root `SKILL.md` named Amigo.
- Preserved their reference files, templates, and visual assets as focused modules.
- Added package routing, tool-availability safeguards, source verification, prompt-injection resistance, least-privilege guidance, and output QA.
