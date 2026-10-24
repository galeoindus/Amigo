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

## Design and accessibility

- **W3C, WCAG 2 overview / Quick Reference:** https://www.w3.org/WAI/standards-guidelines/wcag/ and https://www.w3.org/WAI/WCAG22/quickref/ — used for contrast, keyboard interaction and not relying on color alone. Applicable tests depend on the actual artifact and available inspection tools.
- **Microsoft PowerPoint accessibility guidance:** https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities — recommends meaningful slide titles, logical reading order, alt text, adequate contrast and accessibility checks.
- **Apple Human Interface Guidelines — Accessibility:** https://developer.apple.com/design/human-interface-guidelines/accessibility — used as a platform reference only for Apple-platform reviews, not as universal law for every interface.
- **OWASP GenAI Security Project, LLM Top 10 2026:** https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ — used to strengthen awareness of prompt-injection and unsafe agent/tool behavior.

## Changes applied in this revision

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
