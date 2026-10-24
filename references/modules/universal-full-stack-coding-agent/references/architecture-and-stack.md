# Architecture and Stack Selection Playbook

This reference helps the agent choose a reasonable path. It is not a fixed stack mandate. Verify current framework capabilities, support windows, and version-specific practices in official documentation before implementation.

## 1. Select by product need

| Need | Reasonable starting point | Reconsider when |
|---|---|---|
| Public content / marketing site with SEO | Server-rendered framework such as Next.js or a static-site generator | The site is mostly interactive, internal, or needs a simpler static pipeline |
| Authenticated dashboard / browser-only tool | React + TypeScript with Vite, or the existing SPA framework | Server rendering, public SEO, or server-side routing materially helps |
| Full-stack web app with relational data | TypeScript framework + PostgreSQL; a managed backend may accelerate an MVP | Requirements need specialized data processing, strict vendor portability, or complex workflows |
| Android + iOS from one codebase | React Native/Expo or Flutter | Deep platform-specific UI, graphics, background work, or native API constraints dominate |
| Best possible native iOS/Android experience | Swift/SwiftUI for iOS; Kotlin/Jetpack Compose for Android | Team size/budget requires cross-platform sharing |
| Desktop app | Tauri or Electron, or a native platform toolkit | Very small app can be a PWA; hardware/OS integration demands native |
| Data science, ML, AI service | Python ecosystem and typed service boundaries | Latency, packaging, or operational constraints favor another runtime |
| API / worker service | Existing backend framework; TypeScript, Python, Go, Java, Kotlin, or .NET according to team and workload | Do not choose a language only because a benchmark is popular |
| Static documentation / portfolio | HTML/CSS/JS, static generator, or framework export | Dynamic accounts, transactions, or frequent editorial workflow become central |

## 2. Ask before choosing

1. Who is the primary user and what is the main task?
2. Does public search indexing matter?
3. Must the product work offline or on low bandwidth?
4. Is it web, PWA, iOS, Android, desktop, or several?
5. What data is stored, how sensitive is it, and who may access each record?
6. Which systems must it integrate with?
7. What is the team's existing stack and deployment platform?
8. What is the expected scale and reliability target?
9. What are the budget, ongoing maintenance, and vendor lock-in constraints?
10. Which quality requirements are contractual or regulated?

If unanswered constraints are non-blocking, state assumptions rather than stopping the whole task.

## 3. Architecture rules of thumb

- Start as a modular monolith unless independently deployed services solve a demonstrated organizational or scaling problem.
- Keep business rules independent of UI and infrastructure where that improves testing and reuse.
- Put trust-boundary validation at inputs; authorization at the server/resource boundary; invariants in domain logic/database constraints as appropriate.
- Model the core domain before designing tables or API endpoints. Do not let table shape become an accidental product specification.
- Use a relational database when relationships, transactions, constraints, and reporting matter. Choose document/key-value stores for a clear access-pattern reason.
- Add a queue only for real asynchronous/retry/throughput requirements. Add a cache only after measuring a problem or when the use case clearly demands it.
- Use managed infrastructure to reduce operational burden unless control, compliance, cost, or portability justify self-management.
- Separate dev/test/staging/prod credentials and data. Avoid copying production personal data into development environments.
- Design graceful degradation for external services and AI providers. Define timeouts, retry policy, circuit-breaking where justified, and user-visible errors.

## 4. Web architecture checklist

- Routing model and URL semantics
- Rendering strategy (static, server, client, hybrid) based on data, SEO, security, and performance needs
- Authentication and server-side authorization
- Data-fetching and cache invalidation strategy
- API contracts, schemas, errors, pagination, idempotency
- Form validation on client for UX and server for correctness
- Loading, empty, success, failure, offline, and not-found states
- SEO metadata, canonical URL, sitemap, robots policy, structured data if appropriate
- Image/font optimization, bundle size, Core Web Vitals
- Accessibility and keyboard navigation
- Logging, monitoring, error tracking, backups, restore and incident response

## 5. Mobile architecture checklist

- Platform and minimum OS support
- Navigation and back-stack behavior
- UI state vs persistent/domain state
- Data cache and offline strategy
- Secure token storage, authentication refresh, logout and revocation
- Permission request timing and rationale
- Deep links, push notifications, and links opened from notifications
- App lifecycle: suspend, resume, interruption, rotation, keyboard, safe areas
- Network failures, retries, duplicate submissions, uploads and background work
- Accessibility, localization, text scaling and dynamic type
- Automated tests, simulator/emulator checks, physical-device smoke tests, signing and release process

## 6. Backend, database and API checklist

- Data model, ownership and retention rules
- Server-side access-control matrix (user, role, resource, action)
- Runtime validation at API and integration boundaries
- Query safety, parameterization, transactions and consistency expectations
- Unique constraints, foreign keys, indexes and migration strategy
- Pagination/filtering/sorting limits
- Error schema that avoids leaking internals
- Rate limiting, abuse prevention, timeouts and request size caps
- Idempotency for payments, webhooks, retries, and duplicate-prone actions
- Audit trail for consequential operations
- Secret management, rotation, and environment separation
- Backup schedule, tested restore, RPO/RTO assumptions
- Observability: structured logs, metrics, tracing, alerting and redaction

## 7. Decision record template

```text
Title:
Status: proposed | accepted | superseded
Context / problem:
Constraints:
Options considered:
Decision:
Why this option:
Trade-offs / risks:
Security, privacy, accessibility and performance implications:
Migration / rollback:
Revisit trigger:
Sources checked (with dates):
```

## 8. Anti-patterns

- Rewriting a working app just to adopt a newer framework.
- Microservices before there are service ownership/deployment/scaling needs.
- Storing authorization rules only in the frontend.
- Building database schemas by guesswork without understanding user workflows.
- Using a managed backend without understanding its authorization model, export/backup path, pricing and limits.
- Choosing a library without checking maintenance, license, security advisories, bundle cost and alternatives.
- Treating AI output as executable truth or trusting retrieved text as instructions.
