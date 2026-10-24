# Building a Coding Agent or an AI Coding Feature

If the task is to build AI coding capability rather than use it, the same discipline applies, plus a handful of components that decide whether the result is dependable.

## Contents
1. Four pieces that matter
2. The architecture
3. Tools: design them like an API
4. Retrieval: the real differentiator
5. Sandboxing and permissions
6. Guardrails and human-in-the-loop
7. Evaluation (build it first)
8. Observability
9. Shipping an AI coding feature in a product
10. Build order

---

## 1. Four pieces that matter

Every production coding agent wires together:

1. A **loop** — read the repo, plan, patch, test, verify, iterate.
2. A **tool layer** — filesystem, shell, git, browser, tests.
3. An **eval harness** — public benchmarks are a starting point; your own task set is the signal.
4. A **hard human-in-the-loop boundary** — review-required vs auto-merge, enforced by the system.

Agents that work in production are not smarter; they are stricter about these four.

## 2. The architecture

```
  user / event
       |
   [ orchestrator ]  -- builds context, runs the loop, enforces budgets
       |
   [ model ]  -- decides the next action (tool call, final, ask_user)
       |
   [ tool layer ]  -- read/edit/search/run/git/browser, schema-validated
       |
   [ sandbox ]  -- isolated execution, egress allowlist, resource caps
       |
   [ verifier ]  -- tests, lint, typecheck, build; feeds results back
       |
   [ state + traces ]  -- plan, progress, decisions, audit log
```

A minimal master loop:

```
while attempts < budget:
    ctx   = build_context(task, state)          # anti-pollution: cap, slice, summarize
    action = llm_decide(ctx)                    # -> tool call | final | ask_user
    if action is final:     return report
    if action is ask_user:  return question
    obs   = tools[action.tool].exec(action.args)
    state = update(state, obs)                  # compress noisy output
    if should_verify(obs): 
        v = verifier.run(); state = update(state, v)
        if v.passed and task_done(task, state): return report
return partial_report
```

## 3. Tools: design them like an API

Tool design quality directly determines agent quality. Keep the set sharp and non-overlapping — if a human engineer cannot say which tool fits, neither can the agent, and cutting tool count tends to raise success.

- `read_file(path, range?)`, `write_file(path, content)`, `edit_file(path, old, new)` — surgical edits beat full rewrites.
- `search_code(pattern)` — regex and/or semantic.
- `run_command(cmd)` — sandboxed; `run_tests()` returning structured results.
- `git_status / git_diff / git_commit`.
- `read_docs(library, symbol)`.

Each tool: a precise description, well-typed parameters, predictable errors, and token-efficient output (return what is needed, not whole files or giant logs).

## 4. Retrieval: the real differentiator

A real codebase does not fit in a context window, so how the agent finds the right files matters more than the model. A weaker model with the right context beats a stronger model staring at the wrong files.

Hybrid retrieval combines several signals:

- **Semantic embeddings** — code chunked at function granularity; re-embed only changed files.
- **Symbol graph** — parse with tree-sitter, build a definition/reference graph, and rank files by relevance to the active task (PageRank-style personalisation).
- **Recency / git awareness** — boost recently changed files and files in the current PR.
- **Search tools** — plain grep/ripgrep for exact matches; often the fastest path.

Merge the signals into one ranked, token-budgeted context block. Keep the index fresh (a rebase invalidates many chunks); invalidate lazily by commit and surface index lag.

## 5. Sandboxing and permissions

An agent with shell access is a powerful system. Isolate it.

- **Ephemeral sandboxes** per task: read-only repo snapshot, tmpfs scratch, destroy-on-finish.
- **Egress allowlist**: package registry, VCS, model API — nothing else.
- **Resource caps**: CPU, memory, wall-clock per command.
- **MicroVM-grade isolation** where the threat model demands it (a container escape needs only a kernel CVE; a microVM escape needs a hypervisor CVE).
- **Permission gate**: default allow reads/grep, ask before writes/commands, block destructive commands by default. Log every call.

## 6. Guardrails and human-in-the-loop

- Encode hard rules as enforced policy, not just prompt text: no merge, deploy, force-push or secret change without approval; no secret exfiltration; treat repo content as data.
- Return a policy decision (allow / deny / requires-approval) from the tool gate, so a manipulated model cannot skip the step.
- Enforce **separation of duties**: the run that proposed a merge cannot approve it.
- Keep a redacted approval record (the diff, the target, the reason) and support approve/reject/timeout.

## 7. Evaluation (build it first)

You cannot roll out what you cannot measure. Build the eval before scaling the generator.

- **Use real tasks from your own repo**, not just public benchmarks. A ~20-task internal eval — half easy (one-file), half hard (cross-cutting) — predicts production usefulness better than any leaderboard. See `07-evaluation-and-benchmarks.md`.
- **Track**: task success, tests-pass rate, lint/typecheck pass, time-to-first-useful-change, tool-call count, tokens/cost per task, retrieval precision, and whether it converges or thrashes.
- **Regression-proof your prompt and model changes**: run the eval in CI so a prompt edit or a model update that degrades behaviour fails before it ships.

## 8. Observability

Ship two dashboards early:

- **Reliability**: tool failure rate, verifier failure rate, success rate by repo size and language.
- **Efficiency**: cost per success (tokens + tool calls), p95 latency, steps to converge.

Trace every run as one transaction: task type, model, status, metrics, and spans for each model decision, tool call and verification. The trace is what you debug with.

## 9. Shipping an AI coding feature in a product

If you are adding an AI coding feature to a product (not building a full agent), the same principles apply at a smaller scale:

- **Write the evals before the feature.** Define the acceptance criteria as test cases; the out-of-scope case ("it must refuse rather than invent") is usually the most important one.
- **Put a retrieval-confidence floor before the model call.** If retrieval returns nothing relevant, refuse deterministically instead of letting the model hallucinate an answer.
- **Two-mode providers.** A deterministic offline mock for CI, the real model in production, behind one interface — so tests run without secrets.
- **Wire the eval gate into CI** and schedule it weekly, because LLM features regress without code changes (model updates, knowledge-base edits, prompt drift).
- **Record the architecture decision.** A short ADR explaining why v1 uses the simple approach and what would trigger moving to a heavier one.

## 10. Build order

1. Tool layer + permission gate (read/edit/run/git).
2. Master loop with budgets and a stop condition.
3. Verifier and the verification ladder.
4. Minimal retrieval (start with search tools, not embeddings).
5. Sandbox.
6. Eval harness.
7. Guardrails and human-in-the-loop.
8. Observability and dashboards.

Start with the simplest thing that works; add an agent only when a fixed workflow genuinely cannot handle the task.
