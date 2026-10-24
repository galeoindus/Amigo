# Best Practices for Skill Creators

A consolidated reference for writing high-quality skills. Read this when creating or improving a skill.

## Start from real expertise

Asking an LLM to generate a skill without domain-specific context produces vague, generic procedures ("handle errors appropriately") rather than the specific API patterns, edge cases, and project conventions that make a skill valuable. Ground skills in real expertise:

- **Extract from a hands-on task**: complete a real task in conversation, then extract the reusable pattern — the steps that worked, the corrections made, input/output formats, and the context the agent didn't already know.
- **Synthesize from existing project artifacts**: internal docs, runbooks, style guides, API specs/schemas/configs, code-review comments, issue trackers, version-control history (patches reveal patterns), real failure cases and their resolutions. Project-specific material beats generic references.

## Refine with real execution

The first draft usually needs refinement. Run the skill against real tasks, feed all results (not just failures) back in. Ask: what triggered false positives? What was missed? What could be cut? Even one execute-then-revise pass noticeably improves quality.

Read agent execution traces, not just final outputs. Wasted steps usually mean:
- Instructions too vague (agent tries several approaches)
- Instructions that don't apply to the current task (agent follows them anyway)
- Too many options without a clear default

## Spending context wisely

Once a skill activates, its full SKILL.md body loads into the agent's context window. Every token competes for attention.

- **Add what the agent lacks, omit what it knows**: project-specific conventions, domain-specific procedures, non-obvious edge cases, the particular tools/APIs to use. Don't explain what a PDF is or how HTTP works. Ask of each line: "Would the agent get this wrong without this instruction?" If no, cut it.

  ```markdown
  <!-- Too verbose — the agent already knows what PDFs are -->
  ## Extract PDF text
  PDF (Portable Document Format) files are a common file format...
  To extract text from a PDF, you'll need to use a library...

  <!-- Better — jumps straight to what the agent wouldn't know on its own -->
  ## Extract PDF text
  Use pdfplumber for text extraction. For scanned documents, fall back to
  pdf2image with pytesseract.
  ```

- **Design coherent units**: a skill scopes like a function — one coherent unit of work that composes with other skills. Too narrow forces multiple skills to load; too broad is hard to activate precisely.
- **Aim for moderate detail**: overly comprehensive skills hurt — the agent struggles to extract what's relevant. Concise stepwise guidance with a working example beats exhaustive documentation. Most edge cases are better handled by the agent's judgment.
- **Structure large skills with progressive disclosure**: keep SKILL.md under 500 lines / ~5,000 tokens; move detailed reference material to `references/` files, and tell the agent *when* to load each file ("Read references/api-errors.md if the API returns a non-200") rather than a generic "see references/".

## Calibrating control

Not every part of a skill needs the same prescriptiveness. Match specificity to fragility.

- **Give freedom** when multiple approaches are valid; for flexible instructions, explaining *why* beats rigid directives — an agent that understands the purpose makes better context-dependent decisions.
- **Be prescriptive** when operations are fragile, consistency matters, or an exact sequence must be followed.
- **Provide defaults, not menus**: pick a default, mention alternatives briefly ("Use pdfplumber; for scanned PDFs use pdf2image with pytesseract").
- **Favor procedures over declarations**: teach *how to approach* a class of problems, not *what to produce* for one instance. The approach must generalize even when individual details are specific.

## Patterns for effective instructions

- **Gotchas sections**: the highest-value content in many skills — concrete, environment-specific corrections to mistakes the agent will otherwise make (soft-delete filters, inconsistent field names across services, misleading health endpoints). Keep gotchas in SKILL.md where they're read before the situation is encountered. When an agent makes a mistake you correct, add it to the gotchas section.

- **Templates for output format**: provide a concrete template rather than prose descriptions — agents pattern-match well against structures. Short templates inline; long/conditional ones in `assets/`.

  ```markdown
  ## Report structure
  ALWAYS use this exact template:
  # [Title]
  ## Executive summary
  ## Key findings
  ## Recommendations
  ```

- **Checklists for multi-step workflows**: explicit progress checklists prevent skipped steps, especially with dependencies or validation gates.

- **Validation loops**: do the work → run a validator (script, reference checklist, or self-check) → fix → repeat until it passes.

- **Plan-validate-execute**: for batch or destructive operations, create an intermediate structured plan, validate it against a source of truth with a script, only then execute. The validation error messages must give the agent enough to self-correct.

- **Bundling reusable scripts**: if traces show the agent reinventing the same logic each run, write a tested script once and bundle it in `scripts/`.

## Optimizing skill descriptions

The `description` field carries the entire burden of triggering: agents load only name + description at startup and decide from those.

- **Use imperative phrasing** ("Use this skill when…")
- **Focus on user intent** (what the user is trying to achieve, not internal mechanics)
- **Err pushy** (list contexts where it applies, "even if they don't explicitly mention X")
- **Keep it coherent** and under the 1024-character limit
- Test with realistic should-trigger and should-not-trigger queries; the most valuable negatives are near-misses sharing keywords but needing something different
- Split train/validation to avoid overfitting the description

Before and after:

```yaml
# Before
description: Process CSV files.

# After
description: >
  Analyze CSV and tabular data files — compute summary statistics,
  add derived columns, generate charts, and clean messy data. Use this
  skill when the user has a CSV, TSV, or Excel file and wants to
  explore, transform, or visualize the data, even if they don't
  explicitly mention "CSV" or "analysis."
```

## Using scripts in skills

### One-off commands

When an existing package already does what you need, reference it directly in SKILL.md without a `scripts/` directory. Pin versions for reproducibility, and state prerequisites rather than assuming the environment.

```bash
# Python (via uvx)
uvx ruff@0.8.0 check .

# Node.js (via npx)
npx eslint@9 --fix .

# Go
go run golang.org/x/tools/cmd/goimports@v0.28.0 .
```

Move complex commands into tested scripts when they grow hard to get right on the first try.

### Referencing scripts from SKILL.md

Use relative paths from the skill directory root. List available scripts so the agent knows they exist:

```markdown
## Available scripts

- **`scripts/validate.sh`** — Validates configuration files
- **`scripts/process.py`** — Processes input data
```

Then instruct the agent to run them:

```markdown
## Workflow

1. Run the validation script:
   ```bash
   bash scripts/validate.sh "$INPUT_FILE"
   ```

2. Process the results:
   ```bash
   python3 scripts/process.py --input results.json
   ```
```

### Self-contained scripts

Bundle a script in `scripts/` that declares its own dependencies inline so one command runs it.

**Python (PEP 723):**

```python
# /// script
# dependencies = [
#   "beautifulsoup4>=4.12,<5",
# ]
# ///

from bs4 import BeautifulSoup

html = '<html><body><h1>Welcome</h1><p class="info">Test.</p></body></html>'
print(BeautifulSoup(html, "html.parser").select_one("p.info").get_text())
```

Run with `uv run scripts/extract.py` — creates an isolated environment, installs dependencies, runs the script.

**Deno:**

```typescript
import * as cheerio from "npm:cheerio@1.0.0";

const html = `<html><body><h1>Welcome</h1><p class="info">Test.</p></body></html>`;
const $ = cheerio.load(html);
console.log($("p.info").text());
```

Run with `deno run scripts/extract.ts`.

### Designing scripts for agentic use

When an agent runs your script, it reads stdout and stderr to decide what to do next. A few design choices make scripts dramatically easier for agents to use:

- **No interactive prompts** — agents run non-interactive shells; a blocking prompt hangs forever. Accept all input via flags/env/stdin.

  ```
  # Bad: hangs waiting for input
  $ python scripts/deploy.py
  Target environment: _

  # Good: clear error with guidance
  $ python scripts/deploy.py
  Error: --env is required. Options: development, staging, production.
  Usage: python scripts/deploy.py --env staging --tag v1.2.3
  ```

- **Document usage with `--help`** — brief description, flags, examples. Keep it concise (it enters the context window).

- **Helpful error messages** — say what went wrong, what was expected, what to try ("--format must be one of: json, csv, table. Received: 'xml'").

- **Structured output** — prefer JSON/CSV/TSV over free-form text; data to stdout, diagnostics to stderr.

- **Idempotency** — agents retry; "create if not exists" beats "fail on duplicate".

- **Reject ambiguous input** with a clear error rather than guessing; use enums/closed sets.

- **Dry-run support** for destructive/stateful operations.

- **Meaningful exit codes** — distinct codes per failure type, documented in `--help`.

- **Safe defaults** — destructive operations may require explicit `--confirm`/`--force`.

- **Predictable output size** — harnesses truncate large tool output; default to summaries/limits with paging flags, or require `--output` for large results.
