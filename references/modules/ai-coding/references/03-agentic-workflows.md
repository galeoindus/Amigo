# Agentic Workflows

How coding agents actually run, and how to keep the loop reliable when the work spans many steps, files or sessions.

## Contents
1. What an agent is
2. The canonical loop
3. The three engineering layers
4. Verification: the ladder and the stopping condition
5. Subagents and isolation
6. Parallel agents and worktrees
7. Hooks and deterministic guardrails
8. Headless and CI use
9. Human-in-the-loop boundaries
10. Budgets, failure modes and recovery
11. Progress files for long tasks

---

## 1. What an agent is

An agent is a language model that calls tools in a loop: the model decides the next step, your code runs the tool, the result goes back into the conversation, and the cycle repeats until the model stops asking for tools.

```
while True:
    response = model(context)
    if response.has_tool_calls():
        context += run_tools(response.tool_calls)
    else:
        break
```

The loop is nearly identical across products. The engineering effort — and the quality difference — lives in everything around it.

## 2. The canonical loop

Every production-grade coding agent runs a variant of this:

```
1. INGEST   read the issue, the relevant files, the failing test
2. PLAN     produce a short ordered task list
3. ACT      pick a tool (read_file, edit_file, run_shell, run_tests)
4. OBSERVE  read the tool output verbatim
5. REFLECT  does the observation match the plan? what changed?
6. DECIDE   continue, replan, escalate, or stop
7. VERIFY   run tests, type-check, lint, re-read the diff
8. SUBMIT   open a PR (or commit) with a summary of what was done
```

The loop is the product; the model is the engine. Treat them as separate components when you build or evaluate.

## 3. The three engineering layers

- **Context engineering** — everything the model sees on a turn. Goal: the smallest set of high-signal tokens that lets it act well.
- **Harness engineering** — the code around the model: tools, permissions, sandboxes, hooks, state, error recovery, observability. A good harness makes a capable model dependable.
- **Loop engineering** — the cycle that keeps the agent working toward a goal and decides when to stop. Three hard problems: managing context across iterations, deciding when to terminate, and verifying that the result is truly done.

Guidance that holds across vendors: start with the simplest thing that works; build the verifier before scaling the generator; give the agent sharp, non-overlapping tools (cutting tool count has been observed to raise success rates); keep tool outputs token-efficient.

## 4. Verification: the ladder and the stopping condition

Run verification as a ladder, cheapest first, and let failures feed back as observations the agent loops on:

1. Format and lint
2. Unit tests
3. Integration / build
4. Runtime / end-to-end (when relevant)
5. Human checkpoints (merge gates)

The hardest part of an agent is the **stopping condition**. "All tests pass" is weak — tests can be missing or wrong. A strong stopping condition is: tests pass **and** the diff is small enough to review **and** the agent can summarize what it changed in one paragraph. Agents without a strong stopping condition produce 800-line PRs nobody merges.

Always re-verify after each change, not only at the end. Same model, different verification cadence, can be a 15-plus-point swing in task success.

## 5. Subagents and isolation

A subagent is an isolated assistant with its own prompt, tools and context. Use it to keep the main loop's context clean:

- Delegate noisy investigation (large logs, wide searches, full test suites, browser automation) and take back only the summary.
- Use a subagent for a second opinion on a risky change, so the author is not grading itself.
- Keep the main loop's working memory small; let subagents do the exploring.

## 6. Parallel agents and worktrees

Running several agents at once multiplies throughput but also multiplies risk and token spend.

- **Isolate tasks.** Give each parallel task its own git worktree or sandbox so they cannot clobber each other's files.
- **One repository, one bill.** Teams often route several agents through one model gateway for centralised billing and model choice.
- **Beware the cost.** Vendors warn that parallel runs multiply token use; cap concurrency and budget per task.
- **Coordinate.** For fleets, use a shared task board or a manager view so work is not duplicated.

## 7. Hooks and deterministic guardrails

Prompts are advisory; hooks are enforced. Use lifecycle hooks (shell commands fired at defined points) for anything that must always happen:

- Run the formatter or linter after every file write.
- Block a turn from ending until tests pass (a stop hook).
- Reject writes to protected paths or to secrets.
- Log every tool call and its arguments for auditability.

The rule of thumb: if it must always happen, put it in a hook, not in prose.

## 8. Headless and CI use

Every major agent can run without a human. Common patterns:

- `claude -p`, `codex exec`, `agent -p` and similar one-shot/print modes for scripts and CI.
- GitHub Actions that triage issues, draft migrations, or review PRs automatically.
- Scheduled runs for recurring chores (dependency bumps, doc fixes, lint sweeps).

In CI, treat model output as untrusted: do not interpolate issue/PR text into prompts without sanitisation, keep the workflow token least-privilege (`permissions: read-all` as a default), and never `eval` model output as shell.

## 9. Human-in-the-loop boundaries

The single highest-stakes decision: who merges the PR?

- **Review-required.** A human reviews every diff before merge. Throughput bounded by reviewer time; risk bounded by reviewer attention. The default for anything touching money, auth, customer data or production infra.
- **Auto-merge with guardrails.** The agent merges only if all tests pass, no protected files are touched, and the diff is under N lines. For low-stakes cleanup.
- **Auto-merge with rollback.** The agent merges and a canary watches error rates, auto-reverting on regression. Only for orgs with mature deploy infra.

Do not jump to auto-merge before you have telemetry to catch the failures. Also enforce separation of duties: the agent or person who wrote the change cannot be the one who approves it.

## 10. Budgets, failure modes and recovery

Five failure modes show up in every deployment. Plan for all of them:

1. **Overconfident wrong patches** — compiles, passes tests, still wrong. Mitigation: write the failing test first and give it as part of the spec.
2. **Infinite loops** — fixing A breaks B, fixing B breaks A. Mitigation: hard caps on iterations and tokens per task.
3. **Scope creep** — the agent refactors the surrounding module while fixing the bug. Mitigation: explicit scope ("touch only files in `/lib/billing`") and a diff-size budget.
4. **Secret leakage** — the agent reads `.env` and commits a key. Mitigation: scan the working tree for secrets before it runs; redact in shell output; pre-commit hooks.
5. **Hallucinated dependencies** — imports a package that does not exist or is malicious. Mitigation: lock-file diff review and a dependency allowlist.

Recovery: read the actual error, form a hypothesis, make the smallest change that tests it, re-run. If the same approach fails twice, change strategy — re-read the code, check versions and docs, or reduce to a minimal reproduction.

## 11. Progress files for long tasks

For work spanning many steps or sessions, keep a progress file in the repo: goal, done, next, open questions, decisions. A fresh session can then resume cleanly. Write recurring corrections into the project instruction file so the next session starts better.
