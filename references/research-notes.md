# Amigo modernization research notes

**Research checked:** 2026-10-25. This file records official/reference materials reviewed for this package. Product docs and API behavior can change; re-check the live version before important integrations.

## Agent Skills architecture

- **OpenAI, Skills:** https://developers.openai.com/api/docs/guides/tools-skills — skill bundles consist of a `SKILL.md` manifest plus optional references, scripts and assets; documents modularity, tool requirements and the risk of unreviewed skills. Used to keep one active manifest, useful description, progressive disclosure and explicit security checks.
- **OpenAI, Build skills (Plugins):** https://developers.openai.com/plugins/build/skills — recommends clear triggers/boundaries, inputs and outputs, stop conditions, reference files, and validating live MCP dependencies. Used to sharpen routing and avoid unsupported tool assumptions.
- **OpenAI, Rethinking skills and prompts for GPT-6 Astra (2026-09-11):** https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra — warns against bloated instruction scaffolding. Used to keep task instructions concise while preserving specialized procedures in references.

## Analytics and statistics

- **Metabase Agent API:** https://www.metabase.com/docs/latest/ai/agent-api — documents a versioned Agent API that is permission-scoped and supports table/metric discovery, fields, query construction/execution, a 200-row request cap and continuation tokens. Used to update crawler assumptions; behavior must only be used when this API is actually connected.
- **Metabase API docs and changelog:** https://www.metabase.com/docs/latest/api and https://www.metabase.com/docs/latest/developers-guide/api-changelog — reminds that non-Agent API endpoints can change. Used to require live version/schema validation instead of treating snippets as universal.
- **NIST/SEMATECH e-Handbook of Statistical Methods:** https://www.itl.nist.gov/div898/handbook/ — official statistical reference for exploratory analysis and measures of scale.
- **NIST, Detection of Outliers:** https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm and https://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm — potential outliers can be bad data or valid unusual observations. Used to prohibit automatic deletion and require investigation/context.
- **NIST, Measures of Scale:** https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm — explains SD, IQR and MAD and when heavy tails make robust alternatives useful.
- **Brown, Cai & DasGupta, Interval Estimation for a Binomial Proportion:** https://doi.org/10.1214/ss/1009213286 — shows the Wald interval has poor, erratic coverage and recommends the Wilson / Jeffreys / Agresti–Coull intervals. Used to change the statistics helper's default interval.
- **Agresti & Caffo (2000), add-two-successes-and-two-failures:** https://alanagresti.com/articles/agresti_caffo_2000.pdf — a simple adjusted interval for a difference of proportions with near-nominal coverage; basis for the Agresti–Caffo output.
- **Newcombe's hybrid method (two-proportion z-test):** https://en.wikipedia.org/wiki/Two-proportion_Z-test — score-based interval for the difference, always within [-1, 1]; basis for the default Newcombe output and the paired/small-cell caveats (McNemar, Fisher's exact).
- **Mixpanel, Retention report:** https://docs.mixpanel.com/docs/reports/retention — defines On vs On-or-After, rolling vs calendar windows, birth vs compounded, and intervalized averages that exclude incomplete periods. Used to sharpen the retention vocabulary.
- **Mixpanel, Get to know your users (DAU/WAU/MAU):** https://docs.mixpanel.com/guides/strategic-playbooks/guide-to-product-analytics/get-to-know-your-users — "active" should be tied to a value moment, not logins; used to refine the product-analytics active-user guidance.
- **Google Drive API, files.list and Search for files:** https://developers.google.com/workspace/drive/api/reference/rest/v3/files/list and https://developers.google.com/workspace/drive/api/guides/search-files — `'<FOLDER_ID>' in parents and trashed = false`, `pageSize` up to 1000, `nextPageToken`, no single-call recursive traversal, and `md5Checksum` for binary files. Used for the file-organizer discovery and duplicate steps.
- **Visualizing Statistical Mix Effects and Simpson's Paradox (IEEE TVCG):** https://doi.org/10.1109/tvcg.2014.2346297 — mix effects are ubiquitous and can reverse an aggregate; disaggregation is necessary but not a magic bullet. Used in segmentation and evidence-language guidance.
- **python-pptx, Working with text:** https://python-pptx.readthedocs.io/en/latest/user/text.html — formatting is carried at the run level and `text_frame.text` collapses runs; used to reinforce run-level editing in the presentation module.

## Design and accessibility

- **W3C, WCAG 2 overview / Quick Reference:** https://www.w3.org/WAI/standards-guidelines/wcag/ and https://www.w3.org/WAI/WCAG22/quickref/ — used for contrast, keyboard interaction and not relying on color alone. Applicable tests depend on the actual artifact and available inspection tools.
- **Microsoft PowerPoint accessibility guidance:** https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities — recommends meaningful slide titles, logical reading order, alt text, adequate contrast and accessibility checks.
- **Apple Human Interface Guidelines — Accessibility:** https://developer.apple.com/design/human-interface-guidelines/accessibility — used as a platform reference only for Apple-platform reviews, not as universal law for every interface.
- **Apple HIG design principles and WWDC "Writing for interfaces":** https://developer.apple.com/design/human-interface-guidelines and .../design-principles — Clarity/Deference/Depth and the PACE copy framework; distilled into the ui-design-critique module. Also Rene Wang, "Wording in Interfaces": https://rene.wang/essay/wording-in-interfaces.
- **Veracode GenAI Code Security Report (2025 and 2026):** https://www.veracode.com/wp-content/uploads/2025_GenAI_Code_Security_Report_Final.pdf and https://view.ceros.com/veracode/genai-code-security-report2026 — about 44-45% of AI code-generation tasks introduce a detectable OWASP/CWE vulnerability; the rate has barely moved across model generations. Used to state the benchmark figure precisely.
- **"Broken by Default" (arXiv, 2026) and Schreiber & Tippe (arXiv 2510.26103, 2025):** https://arxiv.org/abs/2604.05292 and https://arxiv.org/abs/2510.26103 — explicit security instructions cut the vulnerability rate by only ~4 points; large-scale analysis of public GitHub repos found ~27-30% of AI-attributed snippets carry a weakness. Used to separate benchmark from real-world rates.
- **JetBrains developer survey (2026), via roundups:** https://cyborb.ai/blog/best-ai-coding-agents-2026 — current adoption (Claude Code, Copilot, Codex, Cursor) and the 2026 tool landscape (Antigravity replaced Gemini CLI). Used to sanity-check the tool table.
- **OWASP GenAI Security Project, LLM Top 10 2026:** https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ — used to strengthen awareness of prompt-injection and unsafe agent/tool behavior.

## Changes applied in revision 1.4.0

1. Merged the ai-coding pack and its bundled universal-full-stack-coding-agent companion.
2. Fixed the nested second manifest (converted to a module), the over-long frontmatter description, and the stale `bundled/` cross-links.
3. Refined the AI-code security statistic to distinguish the benchmark rate from the real-repository rate, and added the current tool landscape.

## Changes applied in revision 1.3.0

1. Merged four packs (visualization, time-series-analysis, ui-design-critique, skill-creator) and rebranded the visualization pack to Amigo.
2. Added a GitHub Actions CI workflow that validates the package, compiles every script and smoke-tests the offline helpers on push/PR.
3. Cross-linked ui-design-critique with the existing design-critique-creator rather than duplicating the reviewer setup.

## Changes applied in revision 1.2.0

1. Merged ten new packs and rebranded the whole package to Amigo (no prior brand spelling in any path or text; the prior platform output slugs replaced with format-neutral routing; `Panja runtime` renamed `Amigo runtime`).
2. Swapped the statistics helper's default interval from Wald to Newcombe (with Agresti–Caffo also reported) and added small-cell / small-sample warnings, on the strength of the coverage literature above.
3. Made the funnel helper order-aware using timestamps, matching its own STOP list against unordered funnels.
4. Added a metric contract, rolling-window and retention terminology, and incomplete-cohort caution to product analytics.
5. Added numerator/denominator/mix decomposition and Simpson's-paradox guidance to metric reasoning and segmentation drilldown; added change-point alignment to root-cause analysis.
6. Folded pptx-master into the presentation module, adopting its Season Mix / Matter type system and run-level editing rules.
7. Added the file organizer with Drive read-only discovery and md5-based dedup, and the two agent-builder guides.

## Changes applied in revision 1.1.0

1. Integrated five new packs (data exploration, schema crawler, deck build standards, descriptive statistics, design critique) into one Amigo router; one active root manifest remains.
2. Replaced obsolete tool names as hard requirements with a live-schema check and an honest fallback when an environment lacks a connector/action.
3. Namespaced offline helper scripts and updated instructions to use the paths inside this bundle.
4. Fixed dataset profiling so absent columns count toward missingness; numeric/date inference is explicitly heuristic and mixed timezone awareness is not silently compared.
5. Improved numeric summaries with interpolated quantiles, sample size, missing/invalid counts, IQR, MAD, and a potential-outlier count that never removes rows.
6. Removed outdated external brand requirements and an assumed `pptx-master` dependency; deck rules now inherit the Amigo module or preserve the user's own brand/template.
7. Added design-critique evidence requirements, platform-specific references, severity/effort prioritization and screenshot-only fallback.
8. Expanded package validation to include code text, old brand spellings, single-manifest rules, assets, local links, compile checks and representative helper smoke tests.

## Limitations

This was a documentation and local-helper review, not a live integration test against the user's actual MCP/GitHub/Metabase/Figma connectors or a rendered PowerPoint deck. Vendor tool examples remain conditional on the version and schemas actually available at runtime.
