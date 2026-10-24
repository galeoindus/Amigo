# Evaluation and Benchmarks

How to measure whether an AI coding tool, agent or feature is actually good — and why the famous leaderboards are a weak guide.

## Contents
1. What benchmarks measure and what they miss
2. SWE-bench and its contamination problem
3. The signals that actually predict usefulness
4. Building your own eval
5. Measuring an AI coding feature
6. Cost and efficiency
7. Reporting results honestly

---

## 1. What benchmarks measure and what they miss

Public coding benchmarks (SWE-bench and its variants, Terminal-Bench, and others) measure whether a system can close real GitHub issues or complete terminal tasks under controlled conditions. They are useful for tracking raw capability progress and for sanity-checking a model.

They miss almost everything about *your* situation: your conventions, your monorepo, your reviewer capacity, your security posture, and the cost per accepted change. A high benchmark number does not mean an agent will help your team.

## 2. SWE-bench and its contamination problem

SWE-bench gives a model a real GitHub issue and the repository before the fix, and grades the resulting patch by running the project's tests. SWE-bench Verified is a human-filtered 500-instance subset.

In early 2026, OpenAI published an audit recommending against using SWE-bench Verified to track frontier progress, for two reasons:

- **Flawed tests reject correct solutions.** In an audit of a subset that models struggled with, a majority of problems had test-design or description issues (narrow tests enforcing specific implementations, wide tests checking unspecified functionality) that made them very hard or impossible even for a strong model or human.
- **Training contamination.** The problems come from public repositories used for model training. Models could reproduce the human-written "gold patch" verbatim on some tasks, meaning gains reflect exposure at training time rather than real ability.

Verified scores have also saturated (frontier systems now cluster in the high 80s to high 90s on the bash-only leaderboard), which reduces their power to discriminate between good options. OpenAI recommends SWE-bench Pro as less contaminated, though it too is saturating.

Lesson: a leaderboard is a starting point, not a verdict, and any benchmark derived from public code drifts toward measuring memorisation.

## 3. The signals that actually predict usefulness

| Signal | What it tells you | What it misses |
|---|---|---|
| Public benchmark score | Can it close known issues in well-known repos | Does not reflect your codebase; saturating |
| **Your own 20-task internal eval** | How it behaves in your repo with your conventions | Costs 1-2 days to build |
| Time to first useful change | End-to-end loop quality | Single data point; noisy |
| Diff size on closed PRs | Scope discipline | Easy to game |
| Reviewer time per PR | The net team throughput effect | Slow to measure |
| Post-merge defect / revert rate | Whether the output was actually good | Lags |

The winner on your own eval is rarely the one with the best public number.

## 4. Building your own eval

1. **Pick real tasks from your last 90 days.** Half easy (one-file changes), half hard (cross-cutting refactors). Use real tickets, not invented puzzles.
2. **Write acceptance criteria a machine can check** — the test that must pass, the output that must match, the file that must not change.
3. **Run the same set against each candidate** agent or configuration. Same conditions, same tasks.
4. **Measure beyond pass/fail**: cost per task, wall time, tool-call count, whether it converged or thrashed, and whether the diff was reviewable.
5. **Make it regression-proof.** Run it in CI so a prompt edit or a model update that degrades behaviour fails before it ships. Add every production failure as a new case.

Keep the eval small enough to run often and specific enough to be trusted.

## 5. Measuring an AI coding feature

For a feature (not a full agent), the eval is a golden set plus thresholds:

- **Golden test cases** with expected behaviour, including at least one out-of-scope case that must be refused.
- **Metrics with thresholds**: accuracy, groundedness, latency p95, cost per call.
- **A CI gate** that fails the build on regression.
- **A scheduled run** (e.g. weekly) to catch drift, because LLM features regress without any code change — a provider update, a knowledge-base edit, a subtle prompt change.
- **Production panels**: cost per day, latency p95, refusal rate, and eval drift.

The eval-drift alert is the one teams skip and the one that catches silent regressions.

## 6. Cost and efficiency

Cost is (tokens per call) x (calls per task) x (price per token). Agentic loops make many calls, so waste compounds.

- Track cost per *successful* task, not per call.
- Watch tool-call count and steps-to-converge as proxies for waste.
- Reduce iteration waste with better prompts, real checks, and tight scope before switching vendors.
- Set spend caps on API keys and concurrency caps on parallel agents.

## 7. Reporting results honestly

- Distinguish what a tool result shows from what you infer.
- Report the harness and configuration, not just the score — the same model scores differently in different scaffolds.
- Note contamination and saturation where they apply.
- Prefer "this agent did better on our 20 tasks" over "this agent is better."
