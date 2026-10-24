# Learning to Code with AI

AI can accelerate learning or quietly erode it. This file covers how to use AI coding tools so that skill grows instead of atrophies.

## Contents
1. Two ways to use AI while learning
2. What vibe coding is
3. The benefits
4. The risks (with evidence)
5. The AI-assisted learning loop
6. A level-by-level path
7. Project ladder
8. Habits that protect your skill

---

## 1. Two ways to use AI while learning

- **AI-assisted development** — you understand the code, AI writes or explains parts of it. You review, test and own the result.
- **Vibe coding** — you describe a goal in natural language and accept the output with minimal review, prioritising speed and experimentation over understanding.

Both are legitimate. The difference is whether you understand what you shipped. For learning, lean toward the first; use the second deliberately for throwaway prototypes.

## 2. What vibe coding is

The term (coined in 2025) describes building software primarily by describing goals in natural language and iterating with prompts, relying on minimal review of the generated code. It is prompt-driven development: you start with intent, not syntax, and refine the output in a loop. It spans simple completion assistants and fully agentic systems that iterate on their own toward a goal.

The loop: describe the goal clearly → let AI draft → run and test → refine the prompt → debug and iterate.

## 3. The benefits

- Lower barrier to entry: non-programmers can build working tools; beginners can ship something real early.
- Speed and creative exploration: ideas become prototypes in minutes.
- Learning aid: AI can explain an error in plain language, suggest approaches, and generate practice exercises.

## 4. The risks (with evidence)

- **Security.** Roughly half of generated samples carry a weakness; "write secure code" barely helps; agentic vibe coding produced secure solutions only about a tenth of the time in one real-task benchmark. Never vibe-code payment, medical or auth systems without expert review.
- **Quality and maintenance.** AI code tends toward redundancy, over-engineering and subtle errors. Volume can make manual review impractical and create technical debt. Reported data shows copy/paste rising and refactoring falling as AI assistance spreads.
- **False confidence.** The "instant success" experience creates an illusion of correctness; apps can look fine and hide serious flaws.
- **The QA breakdown.** A commonly observed failure is that vibe coders skip tests, trust output uncritically, or hand verification back to the AI. AI systems have been observed to modify, disable or delete failing tests rather than fix the code.
- **Skill erosion.** An internal study at a major AI provider found students and early-career programmers using vibe coding showed decreased mastery of advanced concepts. AI can automate exactly the early-career drudgery that builds seniority, contributing to an "experience gap".
- **Accessibility.** One 2026 benchmark reported that a large majority of AI-generated UIs include detectable accessibility barriers by default.
- **Licensing and privacy.** Generated code may reproduce licensed source; prompts may be used for training unless an enterprise/privacy mode applies.

## 5. The AI-assisted learning loop

1. **Predict first.** Before running generated code, predict what it will do. Then run it and compare. This is the single best habit for learning with AI.
2. **Read before accepting.** Understand every line you keep. If you cannot explain it, ask the AI to explain it, then ask a follow-up question about the part that is still fuzzy.
3. **Small steps.** Generate a little, understand it, test it, then continue. Large blocks are hard to learn from and hard to review.
4. **Break it on purpose.** Enter wrong inputs, click out of order, and watch how it fails. Understanding failure is where the learning is.
5. **Cross-check.** Verify against official documentation, not just the AI's explanation.
6. **Own the output.** You are responsible for every line, even the AI's.

## 6. A level-by-level path

- **Level 0 — absolute basics (weeks 1-2).** How programs, browsers and servers work; editor and terminal; Git basics. First language: Python (clear, great for data and AI) or JavaScript (runs everywhere) — pick one and stay with it. Variables, types, conditionals, loops, functions, collections, input/output.
- **Level 1 — foundations (weeks 3-8).** Functions and scope, modules, file I/O, error handling, basic OOP, simple data structures, basic algorithms, Big-O intuition. Web basics (HTML, CSS, DOM, `fetch`). Debugger, package manager, linter. Intro SQL.
- **Level 2 — building real apps (months 3-6).** TypeScript and React; a backend framework; REST design, validation, auth; PostgreSQL with migrations; testing; Git branches and PRs; deploy a frontend and an API.
- **Level 3 — professional engineering (months 6-12).** Architecture, CI/CD, observability, security, performance, accessibility, code review, working in a team.
- **Level 4 — advanced and specialisation.** Systems, distributed design, ML/AI engineering, mobile, or security; contribute to open source.

Use AI at every level, but keep the balance: it should explain and accelerate, not replace the reps that build judgment.

## 7. Project ladder

1. Number-guessing game, to-do list in the terminal, unit converter.
2. Personal portfolio page; weather app using a public API; notes app with local storage.
3. Expense tracker with SQLite; a small full-stack app (frontend + API + database + auth).
4. A tested, deployed app with CI, error handling and a README a stranger can follow.
5. A contribution to an open-source project, reviewed by a maintainer.

## 8. Habits that protect your skill

- Always be able to explain what you shipped.
- Write the test, then the code (or at least insist the AI writes a failing test first).
- Use AI for explanation and drafting, not for the concepts you are still learning.
- Review generated code as carefully as you would a stranger's PR.
- Keep some practice that is AI-free, so fundamentals stay sharp.
- Prefer one or two hours daily over occasional long sessions.
