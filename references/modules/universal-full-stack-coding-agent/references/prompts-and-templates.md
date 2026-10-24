# Prompt Examples and Reusable Templates

These prompts are examples for the user or coding agent. Adapt to the actual repository and tools; don't assume a browser, terminal, cloud account, or visual design tool is available.

## 1. Audit a live website

```text
Audit this website: [URL]. First verify what you can access. Do not change production.
Inspect the homepage, navigation, primary conversion journey, mobile layout, forms, accessibility, performance signals, content clarity, SEO basics, trust/security cues and error states.
Separate observed facts from hypotheses. Create a prioritized report with severity, evidence, user impact, recommended change, effort, dependencies, validation metric and sources.
Do not fabricate analytics or claim tests you didn't run. Propose a phased redesign plan that preserves existing business functionality and URLs unless explicitly approved.
```

## 2. Build a new app

```text
Build [product] for [target users]. The primary user outcome is [outcome].
Before coding, inspect this repo and infer its stack from actual files. Summarize assumptions and acceptance criteria. Reuse the existing design system where appropriate.
Implement a complete vertical slice, including loading/empty/error/success states, server-side authorization where relevant, validation, tests and setup documentation. Use official docs for version-sensitive decisions. Run the relevant checks and report exact results. Do not deploy without permission.
```

## 3. Redesign a page

```text
Redesign [page/flow] to improve [goal]. Keep these behaviors: [list].
First identify users, hierarchy, content, states, brand constraints, responsive rules and accessibility risks. Create a coherent design system rather than styling components independently. Implement the responsive page and verify mobile/desktop, keyboard/focus, real interactions, long content, errors and empty/loading states. No fake testimonials, fabricated metrics or decorative controls that do nothing.
```

## 4. Debug a bug

```text
Investigate [symptom]. Reproduce before editing if possible. Compare expected vs actual behavior, inspect recent changes and trace data/control flow. State the root cause only when evidence supports it. Add a regression test and make the smallest robust fix. Run focused tests and related checks; report commands, results and remaining uncertainty.
```

## 5. Review code

```text
Review this diff as a senior engineer. Prioritize correctness, authorization, data integrity, security, concurrency, backwards compatibility and missing tests. Report only actionable findings, each with severity, evidence/location, exploit/failure scenario, impact and fix. Separate confirmed bugs from risks and style suggestions. Do not modify code unless asked.
```

## 6. Plan a database migration

```text
Inspect schema and usages. Propose the target model, compatibility plan, constraints/indexes, data backfill, lock/runtime risks, monitoring and rollback/forward-recovery steps. Test against disposable/staging data. Do not run a production or destructive migration without explicit approval.
```

## 7. Final answer template

```text
## Summary
- What changed and user-visible impact.

## Files / systems changed
- Main files or modules and why.

## Validation
- Command or method — actual result.
- Checks not run — why and how to run them.

## Security / data / release notes
- Authorization, migration, secrets, external calls, deploy state.

## Known limitations
- Verified gaps and residual risk.

## Next step
- One highest-value follow-up.
```

## 8. Technical decision record

See `architecture-and-stack.md` for a full decision record. Each decision should name the context, options, selected approach, reason, trade-offs, migration/rollback and sources checked.

## 9. Acceptance criteria template

```text
Feature:
User/persona:
Preconditions:
Happy-path behavior:
Validation and error behavior:
Permissions / abuse cases:
Loading / empty / offline behavior:
Performance expectation:
Accessibility expectation:
Analytics / observability:
Out of scope:
Acceptance tests:
```
