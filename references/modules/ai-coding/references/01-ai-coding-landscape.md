# The AI Coding Landscape (as of late 2026)

AI coding tools change monthly. Treat everything here as a map, not a fact sheet: confirm pricing, limits, model names and configuration file names in each vendor's own documentation before relying on them.

## Contents
1. Two things people mean by "AI coding"
2. The three shapes of tool
3. The main agents, by vendor
4. Model vs harness: why the same model scores differently
5. Pricing and limit signals
6. Choosing by workflow
7. Setup checklist for any agent

---

## 1. Two things people mean by "AI coding"

"AI coding" covers two different jobs, and conflating them causes bad decisions.

- **Using AI to write software** — driving an assistant or agent to produce, fix, refactor, review and deploy code. This is the majority of day-to-day interest, and most of this skill.
- **Building AI coding capability** — constructing a coding agent, or adding an AI coding feature to a product. This is engineering work; see `06-building-ai-coding-features.md`.

The two share vocabulary (context, tools, evals) but not the same success criteria. A user of an agent cares whether the code is correct and safe; a builder cares about pass rates, cost per task, and how the loop behaves at scale.

## 2. The three shapes of tool

- **Inline assistant / autocomplete.** Ghost-text completions and chat inside an editor (GitHub Copilot, Cursor tab, IDE extensions). Fast, cheap, low autonomy. Best for boilerplate and small edits.
- **Agentic CLI or IDE agent.** Reads the repo, plans, edits files, runs commands, opens PRs (Claude Code, Codex CLI, Cursor's agent, Antigravity, OpenCode, Aider). The centre of gravity in 2026.
- **Cloud / background agent.** Runs a task in an isolated remote sandbox and returns a diff or PR, often in parallel and unattended (Codex cloud, Cursor background agents, Copilot coding agent, Devin, Jules).

Match the shape to the task, not the other way around. Do not put a fully autonomous cloud agent on a one-line change, and do not put inline autocomplete on a cross-cutting refactor.

## 3. The main agents, by vendor

Names and editions shift constantly; verify current details. A representative late-2026 snapshot:

| Tool | Vendor | Models | How you pay (signal) | Notes |
|---|---|---|---|---|
| Claude Code | Anthropic | Claude family | Plan from ~$20/mo, or API key | Terminal-first, deep customisation: skills, hooks, subagents, worktrees, MCP, headless mode |
| Codex CLI | OpenAI | OpenAI GPT models | Bundled with ChatGPT plans, or API key | Open-source CLI (Apache-2.0), cloud tasks, subagents, worktrees, `codex exec` for CI |
| Cursor | Anysphere | Multi-vendor (Anthropic, OpenAI, Google, plus its own) | Free tier, paid plans from ~$8/mo | VS Code fork; widest model choice; background/cloud agents |
| Antigravity | Google | Gemini, plus some others | Free tier with limits; paid tiers | Agent-first IDE + CLI; manager view orchestrating parallel agents; built-in browser verification |
| GitHub Copilot | GitHub | Multi-vendor | Free tier, Pro from ~$10/mo | Editor extension, CLI, and a cloud coding agent wired into GitHub |
| OpenCode | Anomaly (SST) | Any provider (75+) | Free software; you pay the model | Open source (MIT); model-agnostic; terminal + IDE + desktop |
| Aider, Goose, Qwen Code, and others | Various | Various / local | Free or your own keys | Open source; good for self-hosting, local models, cost control |

Two useful reminders: several vendors now ship both an IDE and a CLI that share one configuration, and Google folded its standalone Gemini CLI into the Antigravity tooling in mid-2026 — always check which surface a guide is actually describing.

## 4. Model vs harness: why the same model scores differently

The same underlying model can produce very different results across tools. The difference is the **harness**: the retrieval, tools, permissions, verification cadence, context management and stopping conditions wrapped around the model. Benchmarks and vendor claims that cite a model's score are often really measuring the scaffold.

Practical consequence: when comparing tools, compare them on *your* repository and *your* tasks, not on a public leaderboard number. Two agents on the same model can differ by many points on a real SWE-bench-style task purely because one re-verifies after every change and the other does not.

## 5. Pricing and limit signals

- **Subscription windows.** Most plans throttle with a rolling window (commonly five-hourly) plus a weekly cap, shared across surfaces (chat, CLI, IDE).
- **Per-token API billing.** You pay for every call; agentic loops make many calls. Set a spending cap.
- **Measured cost per call.** One 2026 study of real usage found the cheapest agent's median call around $0.002 and the priciest around $0.09 — a reminder that "which agent is cheapest" depends heavily on the model and how much it iterates.
- **Credit pools.** Some IDEs meter their own models with a weekly pool and bill frontier models at list price on top.

Cost is a function of (tokens per call) x (calls per task) x (price per token). Reducing iteration waste (good prompts, real checks, tight scope) usually saves more than switching vendors.

## 6. Choosing by workflow

Ask "what does my workflow need?", not "which tool is best?".

- **I want the deepest toolbox and terminal-native autonomy** → Claude Code (skills, hooks, subagents, worktrees).
- **I want unattended, sandboxed parallel runs** → Codex cloud or Cursor background agents.
- **I want one IDE with model choice and a visual diff** → Cursor.
- **I am already on a vendor's stack** → that vendor's agent (Copilot for GitHub-centric teams, Antigravity for Google Cloud, Codex for ChatGPT subscribers).
- **I want open source, any model, or self-hosting** → OpenCode, Codex CLI, Qwen Code, or a local-model setup.
- **I just want help inside my current editor** → the built-in assistant.

Most productive teams end up *composing* rather than picking one: a strong interactive agent for hard work, a cloud agent for parallel fan-out, and one shared model gateway so billing and model choice are centralised.

## 7. Setup checklist for any agent

1. Version control first. Commit before letting an agent loose, so any change is one revert away.
2. Work on a branch, or in a worktree/sandbox, for anything large.
3. Write a project instruction file: build/test commands, architecture map, conventions, hard "never do X" rules. Keep it short.
4. Tell it how to verify — the exact test, lint, typecheck or build command.
5. Start in a read-only / plan mode; loosen permissions only once you trust the pattern.
6. Keep secrets out of reach: no `.env`, no credentials in the sandbox, egress allowlisted.
7. Set a budget: iteration and token caps, and a spend cap on API keys.
8. Review every diff before accepting it.
