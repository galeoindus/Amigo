# Prompting and Context Engineering for Code

The model is capable; most bad output is a gap in the input. This file covers how to write requests that a coding agent can satisfy and verify, and how to keep the context window working for you.

## Contents
1. Prompting vs context engineering
2. The five prompt patterns
3. Writing a task as a spec
4. Verification-first prompting
5. Context engineering: what is in the window
6. Instruction files and steering layers
7. The four context failures
8. Context toolkit: write, compress, isolate
9. Plan mode and spec-driven work
10. Anti-patterns

---

## 1. Prompting vs context engineering

**Prompt engineering** is how you write a single instruction. **Context engineering** is the broader, iterative job of curating everything the model sees on a turn: system instructions, tool definitions, project files, retrieved snippets, and prior results. As agents run over many turns, context engineering matters more than any single prompt. The goal is the smallest set of high-signal tokens that lets the model act well.

## 2. The five prompt patterns

A coding agent treats everything you leave unsaid as a decision it is allowed to make. Each pattern below closes one kind of gap:

| Gap in the prompt | What the agent does | Pattern that closes it |
|---|---|---|
| Requirements you have not stated | Guesses a plausible default | Ask for questions first |
| Library, config and error behaviour | Improvises | State constraints |
| "Done" is undefined | Stops when the code looks done | Name the check it must run |
| Your house conventions | Invents its own | Point at an existing file |
| The approach itself | Commits to the first idea | Plan, then implement one step |

Order matters. Questions come first because the answers change the constraints; the check comes before the plan because a plan without a check cannot be accepted or rejected.

## 3. Writing a task as a spec

Treat the prompt like a technical spec, not a suggestion. A good coding prompt names: the goal, the files or area, the constraints (library, config source, failure behaviour, what not to touch), the pattern to follow, and the check.

Example — vague versus specified:

```
Vague:  Add a database connection.

Spec:   Add a PostgreSQL connection using the `pg` library.
        Read the connection string from DATABASE_URL.
        Retry with exponential backoff, at most five attempts.
        Export a typed healthCheck() function.
        Done when `npm test -- db` passes and `npm run typecheck` is clean.
        Do not add new dependencies or edit existing tests.
```

The last lines do the most work. They convert "the agent thinks it is finished" into "a machine decides whether it is finished."

Useful techniques: assign a role ("act as a senior security engineer reviewing this change"), give expected input/output examples, ask it to state its assumptions, and ask it to explain a confusing error in plain language before fixing it.

## 4. Verification-first prompting

Without a check it can run, "looks done" is the only signal available and you become the verification loop. Give the agent something that produces pass/fail it can read, then decide how hard it gates completion:

- **In one prompt:** "implement X, run the tests, fix failures, and paste the final output."
- **Across a session:** set the check as an acceptance condition or goal that is re-evaluated after each turn.
- **As a deterministic gate:** a hook or CI step that blocks the turn or the merge until the check passes.
- **By a second opinion:** a fresh agent or subagent tries to refute the result, so the author is not grading its own work.

Ask for **evidence**, not assertions: the test output, the command it ran and what it returned, or a screenshot. Reviewing evidence is faster than re-running the check yourself, and it works for runs you were not watching.

Ask for an **evidence report** before handoff:

```
Before you hand this back, write an evidence report:
1. Each requirement from my request and the test that proves it (file and test name).
2. Every command you ran to verify the work, with its exit code.
3. Every file you changed, one line each on why.
4. Anything you changed that I did not ask for, and anything you could not verify.
Keep it under 40 lines.
```

## 5. Context engineering: what is in the window

At any turn, the window typically holds: the system prompt, your prompt, the codebase structure, the current file and its dependencies, recent changes, project conventions and rules, available tools and their outputs, any retrieved snippets, and long-term memory. Every one of these competes for the same finite attention budget.

Principle: **the smallest set of high-signal tokens that maximizes the chance of the right outcome.** Minimal does not mean short — it means no filler. Start with a lean setup, test it on real tasks, and add only what fixes observed failures.

## 6. Instruction files and steering layers

Every major agent reads a project instruction file at session start. Keep it short and high-signal.

| Agent | Main file |
|---|---|
| Claude Code | `CLAUDE.md` (plus `.claude/rules/`, `.claude/skills/`, `.claude/agents/`) |
| OpenAI Codex | `AGENTS.md` (global, repo root, subdirectories; nearest wins) |
| Gemini / Antigravity | `GEMINI.md` / product configuration |

A good instruction file contains: how to build and test, an architecture map, coding conventions, and hard rules ("never commit to main", "never edit `migrations/` by hand"). Keep it under roughly 200 lines. Move longer procedures into on-demand skills or path-scoped rule files so they only load when relevant. Choosing the right layer matters: always-on context goes in the instruction file; reusable procedures go in skills; deterministic "must always happen" rules go in hooks, not prose.

## 7. The four context failures

1. **Poisoning** — a hallucination early in the session gets referenced repeatedly and the model "believes" it. Fix: correct it explicitly or restart the session.
2. **Distraction** — including the whole 2,000-line file when you need to fix a ten-line function. Fix: read only the relevant ranges.
3. **Confusion** — irrelevant patterns (React idioms in a Vue project) leaking into reasoning. Fix: keep the stack consistent in context.
4. **Clash** — two versions of the same API both in the window; the model picks the wrong one. Fix: prune stale docs and old code.

## 8. Context toolkit: write, compress, isolate

- **Write and select.** Put durable project knowledge in `AGENTS.md`/`CLAUDE.md` and in tests, so the important context is chosen deliberately rather than guessed.
- **Compress.** Ask the agent to summarize progress into a `progress.md` or `todo.md`. Periodically compact the conversation, preserving decisions and constraints and dropping raw output.
- **Isolate.** Spin up a subagent or a fresh session for a noisy sub-task (a wide search, a full test run) and take back only the summary. Load only the MCP tools the current job needs.

Session splitting is a strong habit: use one session for planning, one for implementation, one for testing. Fresh context improves focus.

## 9. Plan mode and spec-driven work

Separate research and planning from implementation to avoid solving the wrong problem.

1. **Explore (read-only).** Ask the agent to read the relevant code and explain how it works, with no edits.
2. **Plan.** Ask for a numbered plan: for each step, the files created or changed, what changes, the test that proves it, and every assumption. Correct the plan while it is still text.
3. **Implement one approved step.** Run the named test, paste the result, list any deviations, and stop.
4. **Verify and commit.** Then commit with a descriptive message and open a PR.

Skip planning when the scope is clear and the change is small (a typo, a log line, a rename) — if you could describe the diff in one sentence, plan mode is overhead.

## 10. Anti-patterns

- **One-shot "build the whole app" prompts.** They produce code that solves a vaguely-related problem.
- **Vague quality words.** "Make it better" gives no direction; name what better means.
- **Trusting a confident summary.** A green summary is not a green test.
- **Letting the agent weaken the check.** Say "do not edit or delete existing tests."
- **Mega-sessions.** Piling unrelated tasks into one context degrades every later answer.
- **Copy-pasting fixes blindly.** Treat each suggested fix as a hypothesis: apply, test, confirm the root cause.
