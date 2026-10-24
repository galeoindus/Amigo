# Universal Full-Stack Coding Agent Skill

A reusable coding-agent skill for planning, researching, designing, implementing, testing, securing and preparing software for release. It covers websites, web apps, mobile apps, backends, APIs, databases, integrations, AI features and UI/UX redesigns.

## Package contents

- `overview.md` — the agent's main workflow and non-negotiable rules.
- `references/architecture-and-stack.md` — platform/stack decision guide.
- `references/design-and-ui.md` — UI/UX, design systems, responsive design and accessibility.
- `references/security-and-privacy.md` — secure development, privacy, agent safety and approvals.
- `references/testing-and-release.md` — validation, test evidence and release readiness.
- `references/workflows.md` — task playbooks for building, redesigning, debugging, reviewing and releasing.
- `references/prompts-and-templates.md` — reusable user prompts and report templates.
- `references/official-sources.md` — official primary-source links checked on 24 October 2026.
- `templates/AGENTS.md` — short persistent repository instructions.

## Install in a project

### OpenAI Codex
Copy the complete skill folder to `.agents/skills/universal-full-stack-coding-agent/` in the repository. Keep `AGENTS.md` in the repository root if you want persistent project-wide guidance. Codex also supports personal skills under `~/.agents/skills/` and global instructions under `~/.codex/AGENTS.md`.

### Google Antigravity
Copy the complete skill folder to `.agents/skills/universal-full-stack-coding-agent/` in the workspace. Antigravity discovers relevant skills and can invoke them by name/slash command depending on the surface. Global paths vary by surface; consult the current official docs before installing globally.

### Claude Code
Copy the complete skill folder to `.claude/skills/universal-full-stack-coding-agent/` in the repository, or to `~/.claude/skills/universal-full-stack-coding-agent/` for a personal skill. Claude Code skill discovery/permissions may differ by release; verify the current documentation and keep the project-level instructions consistent.

### Other coding agents
The package follows the shared `overview.md` folder pattern. If the agent does not auto-discover skills, paste the core workflow into its project instructions and manually open `overview.md` and the relevant references when needed.

## Recommended usage

Prompt example:

> Use the `universal-full-stack-coding-agent` skill. First inspect this repository, state assumptions and acceptance criteria, and plan the smallest complete implementation. Follow the existing stack and conventions. Do not deploy or perform destructive operations without explicit approval. Run relevant checks and report exact results.

For a broad task, ask the agent to read the relevant reference files rather than loading all of them. This keeps context focused and reduces conflicting instructions.

## Important limitations

This skill does not install SDKs, grant access to repositories, create credentials, or enable browser/terminal/cloud tools. It cannot make an agent's model, runtime, security sandbox, or available tools equivalent across products. It guides process and quality; actual outcomes depend on the host agent and permissions.
