# Amigo module index

Amigo is one installable master skill. Exactly one `SKILL.md` is the active manifest; all imported skill guides are kept as `overview.md` reference modules or `overview-source.md` provenance copies, never separate nested manifests.

| Incoming pack | Integrated path | Capability |
|---|---|---|
| `amigo.zip` | `companion/companion-guide.md` + `companion/references/` | Friendly companion, interpersonal support, social safety, research extension, help-resource caution, productivity |
| `photostudy.zip` | `modules/photostudy/overview.md` | Photo-to-study, faithful transcription, step-by-step solutions, answer verification |
| `metabase-mcp.zip` | `modules/metabase-mcp/overview.md` + query/examples/tools references | Live Metabase discovery/query protocols and bounded data access |
| `analysis-validation.zip` | `modules/analysis-validation/overview.md` + checklist | Four-round analysis/KPI validation and confidence labeling |
| `analytical-planning.zip` | `modules/analytical-planning/overview.md` + investigation tree | Hypothesis-driven investigation and high-information query plans |
| `brand-for-pptx.zip` | `modules/brand-for-pptx/overview.md` + references/assets | Amigo visual system, PPTX creation/editing, rendering and visual QA |
| `changelog-report.zip` | `modules/changelog-report/overview.md` + template/config/logo | PR-based release notes and PDF-ready HTML report |
| `changelog-reporter-builder.zip` | `modules/changelog-reporter-builder/overview.md` | Configure a reusable changelog workflow with tool-aware fallbacks |
| `dashboard-design.zip` | `modules/dashboard-design/overview.md` | KPI story, dashboard hierarchy, trust states and accessibility |
| `data-dictionary.zip` | `modules/data-dictionary/overview.md` + schema/playbook/source map | Semantic definitions, grain, joins, source of truth and open questions |
| `data-exploration.zip` | `modules/data-exploration/overview.md` + protocol; `scripts/data-exploration/` | Bounded discovery and quantitative profiling of already-fetched data |
| `data-schema-crawler.zip` | `modules/data-schema-crawler/overview.md` + protocol/template; `scripts/data-schema-crawler/` | Capped discovery across BI/product/observability sources and schema distillation |
| `deck-build-standards.zip` | `modules/deck-build-standards/overview.md` | Content contract, chart/source requirements, render and accessibility QA |
| `descriptive-statistics.zip` | `modules/descriptive-statistics/overview.md`; `scripts/descriptive-statistics/summarize.py` | Distributions, missingness, robust spread and candidate outlier flags |
| `design-critique-creator.zip` | `modules/design-critique-creator/overview.md` | Tool-aware design-review setup, screenshot fallback, prioritized UX/accessibility critique |
| `metric-reasoning.zip` | `modules/metric-reasoning/overview.md` + `references/identities.md` | Governed metric semantics: metric contract, identities, rates vs counts, mix and denominator effects |
| `root-cause-analysis.zip` | `modules/root-cause-analysis/overview.md` + `references/evidence-language.md` | Hypothesis generation, change-point alignment, discriminating tests, confidence language |
| `segmentation-drilldown.zip` | `modules/segmentation-drilldown/overview.md`; `scripts/segmentation-drilldown/contribution_analysis.py` | Contribution/Pareto drilldown, mix-shift (Simpson) detection, sub-measure decomposition |
| `statistical-inference.zip` | `modules/statistical-inference/overview.md`; `scripts/statistical-inference/proportion_test.py` | Test selection, Newcombe/Agresti–Caffo intervals, effect size, experiment validity |
| `product-analytics.zip` | `modules/product-analytics/overview.md`; `scripts/product-analytics/funnel.py` | Value-based active definitions, funnels, retention/cohorts, diagnostic order, AI-product metrics |
| `pptx-master.zip` | `modules/brand-for-pptx/overview.md` + `references/template-first-workflow.md` and `references/typography.md` | Template-first PPTX create/edit/QA workflow, hard rules, font and logo spec (merged into the presentation module) |
| `file-organizer-builder.zip` | `modules/file-organizer/references/build-guide.md` | Setup-only build interview that writes the clone's taxonomy config; never moves files |
| `file-triage-taxonomy.zip` | `modules/file-organizer/overview.md` + `references/taxonomy.md` | File classification, naming convention, duplicate detection and output contract |
| `mixpanel-product-data-analyst-builder.zip` | `modules/mixpanel-product-data-analyst-builder/overview.md` | Build interview for a Mixpanel product data analyst clone; scope, bind, crawl, probe |
| `presentation-agent-builder.zip` | `modules/presentation-agent-builder/overview.md` | Build interview for a presentation agent; one brand choice, method stays fixed |

## Integration and safety notes

- One root manifest is intentional: the router selects a module and loads detailed references only when relevant.
- Scripts are offline helpers that consume local JSON or emit plans unless their code explicitly states otherwise; they do not provide credentials or establish connectivity.
- Any vendor tool sequence is an example until validated against the live tool schema, product version, permission scope, and pagination behavior.
- The master guide preserves user-provided brands and templates; Amigo colors/logos apply only when appropriate.
- Every metric definition must distinguish `verified`, `inferred`, and `placeholder`. A successful query does not by itself prove the metric is in scope.
- The two agent-builder modules (`file-organizer`, `mixpanel-product-data-analyst-builder`, `presentation-agent-builder`) describe clone setup and reference platform builder mechanics; they only apply when the host provides those tools, and their `clarify`/`agent_admin` steps degrade to plain questions otherwise.
- `pptx-master` is not a separate manifest: its template-first workflow, hard rules and font spec were merged into `brand-for-pptx` so the package keeps a single presentation capability and one active manifest.
