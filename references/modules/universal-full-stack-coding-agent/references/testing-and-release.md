# Testing, Quality Gates and Release Playbook

## 1. Choose tests by risk

- **Unit tests:** pure business logic, validation, calculations, formatters, state transitions.
- **Component tests:** critical accessible behavior, validation errors, empty/loading states.
- **Integration tests:** API + database, auth, transactions, provider adapters, webhook handling.
- **End-to-end tests:** the critical journeys a real user must complete.
- **Contract tests:** compatibility between clients, services and external API schemas.
- **Visual regression:** layout-sensitive interfaces, shared components and important responsive screens.
- **Accessibility tests:** automated scans plus manual keyboard/focus review and assistive-technology checks where practical.
- **Performance tests:** measure when latency, throughput or size matters; use representative scenarios.
- **Security tests:** authz boundaries, validation, dependency checks, secrets and threat-specific tests.

Not every task needs every test type. Select checks based on changed behavior and risk, and explain omissions.

## 2. Typical validation ladder

Run commands from the repository's own package scripts/Makefile/CI first; names below are examples, not assumptions:

```bash
# examples only; inspect the repo before running
npm run lint
npm run typecheck
npm test
npm run test:e2e
npm run build
```

For Python projects, use the repo-configured formatter/linter/type checker/test runner. For native mobile, use the project's actual Gradle/Xcode/Flutter/React Native commands. For database changes, run migrations against a disposable test database and verify rollback or forward-recovery.

## 3. Test design

- Assert behavior visible to a user or consumer of the API.
- Cover positive, negative, boundary, permission-denied, empty and failure cases.
- Make test data explicit, unique, and cleaned up. Keep tests independently runnable.
- Avoid sleeps and fragile timing; use framework wait conditions and stable semantic locators.
- Mock only boundaries that benefit from isolation; preserve at least some integration coverage for critical paths.
- For async or distributed operations, test timeout, duplicate delivery, retry and partial failure.
- Add regression tests for confirmed bugs.
- Do not change tests only to silence a failure without understanding the behavioral contract.

## 4. Test evidence report

Record:

| Check | Command / method | Result | Scope | Caveat |
|---|---|---|---|---|
| Lint | actual command | Pass/Fail/Not run | files / repo | blocker or notes |
| Types | actual command | Pass/Fail/Not run | scope | blocker or notes |
| Unit | actual command | Pass/Fail/Not run | tests | count if available |
| Integration/E2E | actual command | Pass/Fail/Not run | critical paths | environment limitations |
| Build | actual command | Pass/Fail/Not run | target | caveat |
| Accessibility | tool + manual check | Result | viewports/flows | scanner limitations |
| Security | checks performed | Result | threat areas | residual risks |

Never infer “pass” because there was no error message in chat. Use the tool's returned exit code and output when available.

## 5. Release readiness

- Build artifact reproducibly from a known commit.
- Confirm environment variables and secret source without exposing values.
- Check supported runtime/framework versions and dependency advisories.
- Confirm database migrations, forward/rollback strategy, backup and restore assumptions.
- Verify domains, HTTPS, redirect behavior, headers, robots/sitemap policy, app signing and store metadata where relevant.
- Confirm health checks, logs, metrics, error tracking, alerts and dashboards.
- Document operational owner, user support route, maintenance mode and incident response.
- Perform smoke tests after deployment only if deployment was approved and completed.
- Have a rollback or mitigation strategy for high-risk releases.

## 6. Release approval boundaries

A green build does not authorize production deployment. The agent may prepare commands, checklist and release notes. It must not deploy, publish, run production data migrations, alter billing, change IAM permissions, or contact users without explicit authorization.

## 7. Performance and reliability checks

- Measure the critical user journey, not just synthetic microbenchmarks.
- Identify slow network waterfalls, oversized bundles, large images, unnecessary client-side JavaScript and inefficient queries.
- Use pagination and limits for potentially large collections.
- Set timeouts and bounded retries for external calls; avoid unbounded retry storms.
- Use idempotency and deduplication for operations that may repeat.
- Make transient, permanent and user-correctable errors distinguishable.
- Establish reasonable targets with the user/product; don't invent SLAs that the system has not committed to.

## 8. Observability and operations

- Structured logs with correlation/request IDs (without sensitive payloads)
- Metrics for latency, error rate, traffic and saturation where relevant
- Traces for multi-service latency when useful
- Error reporting with source maps or symbolication protected appropriately
- Alerts based on user impact and actionable thresholds
- Runbooks for common incidents and dependencies
- Backups and periodic restore tests for critical data
- Feature flags or staged rollout when blast radius warrants it
