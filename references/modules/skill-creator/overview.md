# Module guide: Skill Creator

> Integrated capability: create new skills, edit and improve existing ones, run evals, and optimize a skill's description for triggering accuracy. Load when the user wants to build, edit, benchmark or refine a skill.


# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run the agent-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Present the results to the user directly in the conversation — show each test case's prompt and output, and share the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.

## Indus environment

This skill runs inside a Indus agent. Indus agents do NOT have subagents, so the entire workflow is designed around sequential, inline execution. The key implications:

- **Test cases run one at a time.** For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — and the human review step compensates.
- **No baseline comparisons.** Baseline runs (without the skill) are skipped — they're only meaningful with parallel subagents. Focus on qualitative feedback from the user and on whether the skill's assertions pass.
- **No blind comparison.** The blind A/B comparison system requires subagents. Skip it.
- **Benchmarking is qualitative.** Quantitative benchmarking relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

### Indus tools

Indus agents have access to the following tools. When writing skills, reference these tool names (not Claude Code tool names):

| Tool | Purpose |
|------|---------|
| `skill_view` | Load a skill or read a file inside a skill. Call with `name` to get the SKILL.md body; call again with `file_path` to read a specific file. |
| `execute_code` | Run Python code in the per-session sandbox. State persists across calls. No network. |
| `terminal` | Run a shell command in the sandbox (pip install, git, file system, CLIs, running scripts). |
| `read_file` | Read a text file from the sandbox (up to 2000 lines from an offset). |
| `write_file` | Write a file, overwriting any existing one and creating parent dirs. |
| `patch` | Replace exact text in a file (targeted edits). Prefer this over `write_file` for small changes. |
| `search_files` | Search files in the sandbox by content or by name (ripgrep-backed). |
| `workspace_output` | Reserve an output path for a deliverable file. Call before writing. |
| `workspace_emit` | Promote a file from `/scratch/work/` to tracked outputs (for .pptx, .docx, .xlsx, .pdf, etc.). |
| `present_output` | Keep files permanently and show them as download tiles in chat. |
| `tool_search` | Discover tools not yet in your tool list. |
| `clarify` | Ask the user 1-4 clarifying questions in a single batch. |
| `todo` | Manage your task list for the current session. |

### Skill editing MCP tools

When you are in a skill build session, you have access to the `skill_admin` MCP, which provides tools for editing the target skill directly in the Indus database. These are the tools you use to create and edit skill content — you do NOT write files to the sandbox filesystem for the skill itself.

| Tool | Purpose |
|------|---------|
| `skill_get` | Read the target skill's meta, file list, and edit permission. Call this first to see the current state. |
| `skill_update` | Patch the skill's name, description, and/or categories. |
| `skill_file_read` | Read a file inside the skill. Omit `path` to get SKILL.md + a listing of all files. Pass `path` to read a specific file. |
| `skill_file_publish` | Publish new content for a file in the skill. Use for creating new files and genuine full rewrites. |
| `skill_file_patch` | Change part of an existing file by find-and-replace. **Preferred over `skill_file_publish` for edits** — it's cheaper and can't silently drop content. `old_string` must appear exactly once. |

If you are in an agent build session (not a skill build session), the `agent_admin` MCP provides `skill_create` which creates a skill, auto-publishes it to the agent's scope, and binds it — all in one call. After creation, use `skill_file_publish` to write the SKILL.md and any bundled files.

### Indus skill frontmatter

Skills use YAML frontmatter with these fields:

- **name** (required): Kebab-case, 1-64 chars, lowercase letters/digits/single hyphens.
- **description** (required): Non-empty string, max 1024 chars. This is the primary triggering mechanism.
- **allowed-tools** (optional): Space-delimited string of tool names the skill requires (e.g. `"execute_code terminal"`). These tools are unlocked when the skill is loaded.
- **license** (optional): String.
- **metadata** (optional): Mapping of string keys to string values.
- **compatibility** (optional): String, max 500 chars.

The field `required_tools` is rejected — use `allowed-tools`. The field `tools` is unsupported — use `allowed-tools`.

## Communicating with the user

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of AI agents is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable the agent to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs (file transforms, data extraction, code generation, fixed workflow steps) benefit from test cases. Skills with subjective outputs (writing style, art) often don't need them. Suggest the appropriate default based on the skill type, but let the user decide.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier (kebab-case, 1-64 chars)
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently the agent has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal data.", you might write "How to build a simple fast dashboard to display internal data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"
- **allowed-tools**: Space-delimited string of Indus tool names the skill requires (e.g. `"execute_code terminal"`). Only include tools that are actually needed — the agent gets these tools unlocked when it loads the skill.
- **the rest of the skill :)**

**Publishing the skill content:** Once you've drafted the SKILL.md, publish it using the skill_admin MCP tools:

- If you're in a **skill build session** (the skill already exists as the target), use `skill_file_publish(path="SKILL.md", data=<content>)` to publish the SKILL.md. Use `skill_file_publish` for each additional file (scripts, references, assets) — e.g. `skill_file_publish(path="scripts/helper.py", data=<content>)`.
- If you're in an **agent build session**, use `skill_create(name=<name>, description=<description>)` first to create the skill and bind it to the agent, then use `skill_file_publish` to write the SKILL.md and any bundled files.
- For **editing an existing file**, prefer `skill_file_patch` over `skill_file_publish` — it's cheaper and can't silently drop content. Read the file first with `skill_file_read`, copy the exact text you want to replace into `old_string`, and provide the replacement in `new_string`.

**Workflow for each edit:**
1. Call `skill_get()` to see the current state of the skill (files, permission).
2. Call `skill_file_read(path="SKILL.md")` to read the current content before editing.
3. For new files: `skill_file_publish(path=<path>, data=<content>)`.
4. For edits to existing files: `skill_file_patch(path=<path>, old_string=<exact text>, new_string=<replacement>)`.

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
The agent reads only the relevant reference file via `skill_view(name, file_path="references/aws.md")`.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: [you don't have to use this exact language] "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `expectations` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through.

Use `workspace_output` to create a workspace directory for results, and organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Run test cases sequentially (inline, no subagents)

Indus agents do not have subagents, so test cases run one at a time. For each test case:

1. The skill is already published in the database — `skill_view(name)` will load it into context.
2. Follow the skill's instructions to accomplish the test prompt.
3. Save outputs using `workspace_output` and `write_file` to `/workspace/outputs/<artifact_id>/`.
4. Save the execution transcript to the workspace as well.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

**Skip baseline runs.** Baselines (without the skill) are only meaningful with parallel subagents. Just run the skill and complete the task as requested.

### Step 2: While runs are in progress, draft assertions

Don't just wait — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names. Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted.

### Step 3: Capture timing data

After each test case completes, record timing data to `timing.json` in the run directory:

```json
{
  "total_duration_seconds": 23.3
}
```

### Step 4: Grade and present results to the user

Once all runs are done:

1. **Grade each run** — evaluate each assertion against the outputs. Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence`. For assertions that can be checked programmatically, write and run a script via `execute_code` rather than eyeballing it — scripts are faster, more reliable, and can be reused across iterations.

2. **Do an analyst pass** — review the grading results and surface patterns the aggregate stats might hide. Look for things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time tradeoffs.

3. **Present results to the user directly in the conversation.** For each test case, show:
   - The prompt that was given
   - The output the skill produced (if it's a file, share it via `present_output`)
   - The assertion pass/fail results
   - Ask for feedback: "How does this look? Anything you'd change?"

### Step 5: Collect feedback

When the user tells you their feedback, note it per test case. Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if you wrote similar helper scripts or took the same multi-step approach to something across multiple test cases. If all 3 test cases resulted in writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, publish it with `skill_file_publish(path="scripts/helper.py", data=<content>)`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements using `skill_file_patch` (for targeted edits) or `skill_file_publish` (for new files or full rewrites) — always `skill_file_read` before editing so your `old_string` matches the live content.
2. Rerun all test cases into a new `iteration-<N+1>/` directory
3. Present the results to the user again, referencing the previous iteration's outputs for comparison
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether the agent invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy.

Since Indus agents cannot call other agents or LLMs, description optimization is an inline reasoning process — you do it yourself by analyzing the queries and rewriting the description, not by running a script that calls the gateway.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something a Indus user would actually type. Not abstract requests, but requests that are concrete and specific and have a good amount of detail. For instance, file paths, personal context about the user's job or situation, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut (the user will get a chance to sign off on them).

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage. You want different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in some uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the skill does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user

Present the eval set to the user directly in the conversation. List each query with its should-trigger label and ask: "Do these look right, or do you want to add/remove/change any?"

This step matters — bad eval queries lead to bad descriptions.

### Step 3: Optimize the description inline

Since you cannot call another agent or LLM, you optimize the description yourself through reasoning. For each iteration:

1. **Review the current description** against each eval query. For each query, ask yourself: "If I were an agent seeing this description in my `## Available Skills` list, would I call `skill_view` for this query?" Be honest — if the answer is unclear, mark it as a failure.

2. **Identify failure patterns.** Group the failures:
   - **Failed to trigger** (should have triggered but the description didn't make it clear enough): What keywords or intent is the description missing? Is the phrasing too narrow?
   - **False triggers** (triggered but shouldn't have): What in the description is too broad? Is it matching queries that belong to a different skill?

3. **Rewrite the description** to address the failures. Tips that work well:
   - Phrase in the imperative — "Use this skill for" rather than "this skill does"
   - Focus on the user's intent, not implementation details
   - Make it distinctive — the description competes with other skills for the agent's attention
   - If you're getting lots of failures after repeated attempts, change things up. Try different sentence structures or wordings.
   - There is a hard limit of 1024 characters — stay comfortably under it.

4. **Re-evaluate** the new description against all queries. Track which ones flipped from fail to pass and vice versa.

5. **Repeat** up to 5 times, keeping the description with the best overall pass rate.

6. **Split into train/test** to check for overfitting: designate 60% of queries as "train" (the ones you optimized against) and 40% as "test" (held-out queries you didn't directly target). If the test pass rate is much lower than the train pass rate, the description is overfit — broaden it.

### How skill triggering works

Understanding the triggering mechanism helps design better eval queries. Skills appear in the agent's `## Available Skills` list with their name + description, and the agent decides whether to call `skill_view` based on that description. The important thing to know is that the agent only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because the agent can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means your eval queries should be substantive enough that the agent would actually benefit from consulting a skill. Simple queries like "read file X" are poor test cases — they won't trigger skills regardless of description quality.

### Step 4: Apply the result

Take the best-performing description and update the skill using `skill_update(description=<new description>)`. Show the user before/after and report the scores.

---

### Finalize

The skill is already live in the Indus database — every `skill_file_publish` and `skill_file_patch` call wrote directly to the canonical skill. There is no separate packaging step.

Before finishing:
1. Call `skill_get()` to confirm all files are present and the skill looks correct.
2. Call `skill_file_read(path="SKILL.md")` to do a final read-through of the SKILL.md.
3. If you changed the description during optimization, call `skill_update(description=<new description>)` to apply it.
4. Tell the user the skill is ready and bound to their agent.

---

## Reference files

The references/ directory has additional documentation:
- `references/best-practices.md` — Best practices for skill creators: expertise sourcing, context budgeting, control calibration, instruction patterns, description optimization, and script design
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill (using `skill_file_publish` / `skill_file_patch` via the skill_admin MCP)
- Run the agent-with-access-to-the-skill on test prompts (sequentially, one at a time)
- With the user, evaluate the outputs:
  - Grade assertions and present results directly in the conversation
  - Run quantitative evals
- Repeat until you and the user are satisfied
- The skill is already live in the database — confirm with `skill_get()` and tell the user it's ready.

Please add steps to your TodoList (via the `todo` tool) to make sure you don't forget. Specifically put "Grade evals and present results to user for review" in your TodoList to make sure it happens.

Good luck!
