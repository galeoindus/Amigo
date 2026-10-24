# Task Workflows and Decision Trees

## A. New website or app

1. Inspect constraints and ask/assume platform, users, primary workflows, and success metric.
2. Research relevant official docs and comparable products only when useful; distinguish facts from visual inspiration.
3. Write requirements and acceptance criteria.
4. Select a minimal fit-for-purpose architecture; document major decisions.
5. Sketch information architecture and the key user flow; define design tokens.
6. Implement a functional vertical slice with realistic content and complete states.
7. Add data and auth boundaries; use fake data only when clearly labeled.
8. Add tests while implementing critical behavior.
9. Run lint/types/tests/build; inspect responsive UI and accessibility.
10. Document setup, environment, deployment and remaining gaps.
11. Ask before publishing/deploying.

## B. Existing website redesign / audit

1. Verify access to the site and collect scope: URLs/pages, target users, business goal, devices, analytics if provided.
2. Audit critical paths and visible defects without changing live state.
3. Score clarity, information architecture, conversion path, mobile UX, accessibility, performance, content, SEO and trust.
4. Prioritize issues by user impact, severity, confidence, effort and dependencies.
5. Present a phased plan: P0 blockers, P1 high impact, P2 improvements, P3 polish.
6. Preserve existing functionality and URL behavior unless a change is approved.
7. Build one representative high-value page/flow first; validate it before expanding.
8. Compare before/after at consistent viewport sizes and tasks.
9. Run regression checks for forms, auth, navigation, SEO and analytics where relevant.
10. Separate observed facts, hypotheses and recommendations in the final audit.

## C. Add a feature

1. Find current pattern and neighboring tests.
2. Identify affected routes, modules, data, permissions, external dependencies and states.
3. Define behavior and acceptance criteria before implementation.
4. Add/adjust types and input schemas; check permissions on server.
5. Implement the smallest complete vertical slice.
6. Add success/failure/boundary tests and regression checks.
7. Review backward compatibility, migration, docs and telemetry.

## D. Debug a bug

1. Reproduce with the smallest stable case; record observed vs expected.
2. Inspect logs, stack trace, request/response, relevant code and recent diff; do not guess at root cause.
3. List plausible causes and choose the cheapest discriminating test.
4. Isolate whether the problem is input, state, concurrency, permissions, data, integration, rendering, configuration or environment.
5. Add a regression test before or with the fix where possible.
6. Fix the root cause with minimum scope; avoid a speculative rewrite.
7. Run focused test, related regression suite and build when practical.
8. State root cause only if evidence supports it; otherwise label it probable.

## E. Code review / security review

1. Read task description, diff, architecture and test evidence.
2. Focus first on correctness, data loss, authz/security, concurrency, compatibility and untested failure paths.
3. Trace data from untrusted input to persistence/rendering/external tools.
4. Distinguish must-fix defects from suggestions. Include file/line references when available.
5. Explain scenario, impact, likelihood and actionable fix.
6. Avoid style nits unless they violate project conventions or obscure a bug.
7. Summarize coverage gaps and residual risks.

## F. API/backend integration

1. Read official provider docs and current schema/version.
2. Confirm authentication method, scopes, quota, rate limits, timeouts, data retention and pricing assumptions.
3. Create a small adapter boundary; keep provider details out of core business logic.
4. Validate both outbound and inbound data; verify webhooks/signatures.
5. Add timeout, bounded retry, backoff, idempotency and safe logging as relevant.
6. Build contract tests with fixtures; avoid leaking real credentials.
7. Document environment configuration, setup, failure modes and local testing.

## G. Database schema/migration

1. Understand existing schema, data volume, constraints and access patterns.
2. Define target state and compatibility requirements.
3. Prefer additive/expand-and-contract migrations for zero-downtime contexts.
4. Estimate lock, runtime, backfill and rollback implications.
5. Test against a disposable/staging copy, not production by default.
6. Verify application code works before/after transition if applicable.
7. Ask for explicit approval before production migration or destructive changes.

## H. AI/agent feature

1. Define a narrow job-to-be-done and success/failure criteria.
2. Decide whether deterministic logic is sufficient; don't add an LLM without clear value.
3. Identify tools, data access, trust boundaries and high-impact actions.
4. Define typed input/output schemas, prompt boundaries and failure handling.
5. Restrict tools and use user approval for consequential actions.
6. Build an evaluation set covering normal, edge, adversarial, ambiguous and tool-failure cases.
7. Track output quality, latency, cost and failure modes.
8. Add fallback, retry bounds, cancellation and observability.
9. Test indirect prompt injection and data exfiltration attempts.

## I. Deploy / release readiness

1. Confirm target environment and explicit authorization state.
2. Verify commit, clean/known worktree, build command, tests, secrets and dependency checks.
3. Inspect migration and rollback plan; test in staging first.
4. Confirm monitoring, health checks, backup and access controls.
5. Present impact and deployment plan; request authorization if not already explicit.
6. After approved deploy, run smoke tests and monitor telemetry.
7. Report exact commit, target, checks, outcome and rollback/mitigation.

## J. If requirements conflict

Priority order:
1. Safety, legal constraints, security and data integrity.
2. Explicit user requirements and acceptance criteria.
3. Existing product behavior and architecture contracts.
4. Accessibility, correctness and maintainability.
5. Performance and operational cost.
6. Visual or implementation preference.

Explain trade-offs when a lower-priority goal cannot be met without compromising a higher-priority one.
