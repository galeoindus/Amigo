# Amigo — Unified Master Skill

This package merges **15 uploaded skill packs** into one Agent Skill with one root `SKILL.md`. The master router points to focused reference modules and namespaced helper scripts so a task loads only the material it needs.

## Main entrypoint

- `SKILL.md` — Amigo master skill, global safety contract, capability router and final QA
- `openai.yaml` — display metadata
- `references/module-index.md` — inventory and mapping from all 15 source packs
- `references/research-notes.md` — official docs used for modernization
- `references/companion/` — conversation, interpersonal support and productivity references
- `references/modules/` — study, analytics, data exploration, schema crawling, dashboard, presentation, design critique and changelog guides
- `scripts/` — local/offline helpers grouped by capability; no external service is called unless a user-hosted runtime separately wires a tool

## Install/use

Upload the ZIP where Agent Skills bundles are supported, or place the `Amigo/` directory in the supported skills folder. The host agent must provide any tools/connectors required for external actions. This package does not create credentials, connect external services, grant permissions, or imply that an integration was live-tested.

## Helpful local commands

```bash
python scripts/validate_package.py
python scripts/data-exploration/profile_dataset.py --input /path/to/rows.json
python scripts/descriptive-statistics/summarize.py --input /path/to/rows.json --column amount
python scripts/data-schema-crawler/harvest_plan.py mixpanel
```

The data scripts consume bounded, already-fetched data. Profile results from a sample must not be presented as full-population results. Potential outlier flags are diagnostic prompts, not deletion instructions.

## Compatibility and safety

The root router is the only skill manifest. Imported `SKILL.md` files were converted to reference guides to avoid nested active manifests. The helpers are not guaranteed to match all vendor connector versions; inspect live tool schemas first. Review privacy, least privilege, prompt-injection resistance, approval for consequential actions, source freshness and visual QA before delivery.

## Validation

`python scripts/validate_package.py` checks one manifest, known old-brand strings in text files, required Amigo assets, metadata, archive/module link integrity, and path/name consistency. A validation pass covers package structure, not live GitHub, Metabase, Figma, Mixpanel, SigNoz or PowerPoint integration testing.
