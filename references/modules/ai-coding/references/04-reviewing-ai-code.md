# Reviewing AI-Generated Code

AI output is a draft from a fast, confident, tireless contributor with no memory of your codebase and no accountability. Review it against the task, not just the diff.

## Contents
1. Why AI review is different
2. Frame the diff as a draft
3. The five things that most often go wrong
4. A 10-minute review routine
5. Evidence and tests
6. Reviewing in stages
7. Risk-tiered human approval
8. Metrics to watch

---

## 1. Why AI review is different

Human-written code carries an implicit promise that the author understood the context and the trade-offs. An agent constructs a plausible implementation without that architectural awareness. Two consequences:

- The code can execute perfectly while addressing the wrong objective. Reviewing it as a "deliverable" (does it run?) misses the point; reviewing it as a "draft" (does it fit the system and fulfil the intent?) is what matters.
- Agents have predictable failure modes that human reviewers are not trained to spot: weakened CI, reinvented utilities, plausible-but-wrong logic, hallucinated APIs and dependencies.

Acceptance rates reflect this: AI-generated PRs are merged without change far less often than human ones. Treat them as proposals.

## 2. Frame the diff as a draft

- **Read the ticket first.** The issue is the source of intent; the PR description is what the agent decided to build. Define expected behaviour and boundaries before opening files.
- **Check the title against the intent.** "Add idempotency cache" (implementation) is weaker than "Prevent duplicate charges on retry" (behaviour).
- **Judge the size.** Ten files or a few hundred changed lines is a signal to plan the review deliberately — or to ask for a smaller PR. Review quality falls off sharply past a few hundred lines; reviewers catch most defects at 200-400 lines per review.

## 3. The five things that most often go wrong

1. **CI gaming.** When agents fail CI, some take the obvious path: remove the tests, skip the lint step, add `|| true`. Before approving, check whether coverage thresholds changed, tests were removed/renamed/skipped, or a step was gated behind a condition. Any change that weakens CI is a blocker until explicitly justified.
2. **Code-reuse blindness.** Agents replicate a nearby pattern without noticing that a shared utility already exists. Look for new helpers that duplicate existing ones, validation re-implemented in several places, middleware rewritten from scratch. The agent's local context does not include the whole repo; yours does.
3. **Hallucinated correctness.** The dangerous case is code that compiles, passes its own tests, and is wrong — off-by-one in pagination, a missing permission check on a branch the tests never hit, validation that short-circuits on an edge case, a race condition that only appears at scale.
4. **Untrusted input in workflows.** If the PR touches any workflow that calls an LLM, watch for untrusted text (issue/PR bodies, commit messages) interpolated into prompts, over-scoped tokens, or model output executed as shell.
5. **Plausible-but-wrong dependencies.** New packages that do not exist, are unmaintained, or carry an incompatible license. See `05-security-and-risks.md`.

## 4. A 10-minute review routine

| Time | Step | What to do |
|---|---|---|
| 1-2 min | Scan and classify | Look at the file list and diff size. Narrow task or complex (multi-file, logic, performance, tests)? That sets your review depth. |
| 2-3 min | Check CI changes first | Before reading app code, inspect anything touching workflows, test config, coverage, or build scripts. Flag anything that weakens CI. Stop sign. |
| 3-5 min | Scan for new utilities | For each new function/helper/module, search the repo for an equivalent. Flag duplication and require consolidation. |
| 5-8 min | Trace one critical path | Pick the most important logic change and trace it end to end: input, transforms, output. Check boundaries (zero, max, empty), permissions on every branch, surprising conditions. Do not skip this. |
| 8-9 min | Security boundaries | If it touches auth, input handling, secrets or an LLM workflow, run the security checklist. |
| 9-10 min | Require evidence | For any non-trivial logic change, require a test that fails on the pre-change behaviour. For risky changes, ask for a rollback plan. |

Ask for a smaller PR when: the diff touches more than five unrelated files; you cannot state its purpose in one sentence; the PR has no plan and an empty body; or CI is failing and the only changes are to test files.

## 5. Evidence and tests

- **Require a failing-then-passing test.** If the agent cannot write a test that would have caught the bug it claims to fix, the fix is incomplete or the understanding is wrong.
- **Run the whole suite, not only the tests that came with the change.** Agent-written tests share the author's blind spots. Defects live where new code meets the rest of the system.
- **Read the evidence report, not every line.** Ask the agent to paste the commands it ran and their exit codes; spot-check the tests that prove the riskiest requirement.
- **Do not let the author approve its own change.** Use a second agent or a human; make it a property of the tool, not a guideline.

## 6. Reviewing in stages

1. Establish intent before opening files.
2. Read in a dependency-aware order: schemas, shared types, interfaces, config, migrations, utilities first; then dependent logic. Not alphabetical.
3. Separate behavioural logic from mechanical edits (renames, formatting, generated output); review behavioural changes together, mechanical ones in a separate pass.
4. Validate assumptions, security behaviour, and downstream/cross-file dependencies (callers, consumers, mocks, feature flags, serialization, external clients).
5. Route agent PRs into their own queue so you can track their metrics separately.

## 7. Risk-tiered human approval

Match review depth to risk, and let the change (not the author) set the tier:

| Risk | Examples | Approvals |
|---|---|---|
| Low | Docs, copy, additive changes behind a flag | None required once automated review and checks are green |
| Medium | Ordinary product changes; sensitive areas like caching or auth | One person |
| High | The riskiest code, plus paths that always need two reviewers | Two people |

Automated review can run on every PR first (reading the diff against the repo and the stated intent), with findings verified by a second agent before a human sees them, and security review that can block a merge. Keep human attention for the medium- and high-risk changes.

## 8. Metrics to watch

Measure outcomes, not the feeling of speed. Developers in a controlled trial felt faster while being measurably slower; intuition is a poor guide here.

- Time to first useful change, tool-call count, tokens/cost per task.
- Review comments per PR and reviewer time per PR (the real throughput effect).
- Diff size on merged PRs (scope discipline).
- Escaped defects and revert rate (the quality signal that matters).
- Whether the agent converged or thrashed after failures.
