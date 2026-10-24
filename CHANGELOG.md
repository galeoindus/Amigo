# Amigo Changelog

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
