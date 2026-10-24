# Amigo Changelog

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
