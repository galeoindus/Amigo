# Security and the Risks of AI-Written Code

Assume AI-generated code is insecure until verified. This file summarises the evidence, the risk catalogue, and the controls.

## Contents
1. What the research shows
2. Why "write secure code" does not fix it
3. Risk catalogue
4. Prompt injection and the lethal trifecta
5. Dependencies, licensing and supply chain
6. Secrets and data privacy
7. Controls: a security baseline for AI-assisted work
8. Governance

---

## 1. What the research shows

Multiple large 2026 studies converge:

- **Roughly half of AI-generated code samples contain a security weakness.** One formal-verification study across seven models found a mean vulnerability rate of about 56%, with no model scoring better than a "D". A vendor's 2026 report found about 44% of AI code-generation tasks introduced a risky vulnerability, with an average security pass rate near 56% — essentially flat year over year even as models got better at syntax.
- **Syntax is solved; security is not.** Modern models produce syntactically correct code almost every time, but secure coding has not followed the same curve. Working code is not trustworthy code by default.
- **Certain categories are far worse than others.** Models do comparatively well on SQL injection and crypto-algorithm selection, and poorly on cross-site scripting, log injection, integer-overflow in allocation arithmetic, and other context-dependent, dataflow-sensitive weaknesses.
- **The vulnerability classes are model-agnostic.** Integer arithmetic and memory allocation in C/C++ were the worst across every model tested, because the failure comes from the model's generation prior, not its instruction-following.
- **AI-attributed code is reaching public repositories.** Large-scale scans of GitHub found thousands of CWE instances in AI-attributed files, with language-specific patterns (Python notably higher than TypeScript).
- **Agentic "vibe coding" is worse than the raw model.** In one benchmark of 186 real feature tasks, 57% of an agent's solutions were functionally correct but only about 12% were secure — i.e. most correct-looking solutions shipped a security flaw.

## 2. Why "write secure code" does not fix it

The formal study tested an explicit security prompt: it reduced the mean vulnerability rate by only about 4 percentage points, leaving most models still failing. Security is baked into the generation prior, not the instruction surface.

The most striking finding is a **generation-review asymmetry**: when models were fed their own vulnerable code back and asked to review it, they identified the vulnerability about 79% of the time — yet generated it by default. The knowledge exists; it is not applied spontaneously during generation. The practical implication: **run a separate security review pass**, and do not rely on a security prefix in the prompt as a mitigation.

## 3. Risk catalogue

- **Injection** (SQL, NoSQL, OS command, XSS): unparameterised queries, string-built shell commands, unescaped output.
- **Broken access control**: missing server-side authorisation on a branch, IDOR/BOLA, SSRF via unvalidated outbound URLs.
- **Weak auth and crypto**: fast password hashes, insecure randomness, home-grown crypto, hard-coded keys.
- **Memory and integer safety** (C/C++): unguarded `malloc(n * sizeof(T))`, signed/unsigned conversion, unsafe string functions.
- **Misconfiguration**: debug on in production, permissive CORS, missing security headers, default credentials.
- **Insecure design**: no rate limits, no abuse-case handling, business-logic limits missing.
- **Mishandled exceptions**: sensitive data in error messages, failing open instead of closed.

## 4. Prompt injection and the lethal trifecta

An agent with shell access that reads untrusted content is exposed to indirect prompt injection: a malicious instruction hidden in an issue body, README, code comment, dependency, or web page, interpreted as a command.

The "lethal trifecta" is when the same agent has (a) access to private data, (b) exposure to untrusted content, and (c) the ability to communicate externally. Any two are survivable; all three is an exfiltration path. Break the trifecta: keep private data and external egress out of the same session as untrusted input, and treat all retrieved content as data, never instructions.

## 5. Dependencies, licensing and supply chain

- **Slopsquatting.** Models hallucinate plausible package names; attackers register them. A 2025 study found a meaningful share of generated library names were fake. Verify every new dependency exists, is maintained, and is legitimate before adding it.
- **Supply-chain risk.** AI-assisted development widens the attack surface. Pin and lock versions, scan dependencies, prefer well-maintained packages, and review lock-file diffs on every PR. Software supply-chain failures are now a top-tier web risk.
- **Licensing.** Models were trained on public code, some under copyleft or attribution licenses. Generating large blocks in one go raises the chance of reproducing licensed code. Generate in small steps, and check license compatibility for commercial products.

## 6. Secrets and data privacy

- Never paste credentials, tokens or proprietary data into a prompt; web-based tools may use inputs for training unless an enterprise/privacy mode applies.
- Scan the working tree for secrets before an agent runs; keep `.env` and credential files out of reach; redact secrets in shell output and logs.
- A leaked secret is a rotation event, not a cleanup: tell the user and rotate.

## 7. Controls: a security baseline for AI-assisted work

1. **Verify, do not trust.** Run SAST, dependency scanning and secret scanning on AI-generated commits exactly as on human ones. Note that static tools miss a large share of formally-proven vulnerabilities, so scanning alone is not enough — pair it with human review of security-sensitive paths.
2. **Review security-sensitive paths deliberately.** Auth, authorisation, input handling, secrets and data access get their own pass.
3. **Run a separate security review pass**, ideally by a different agent or person than the author.
4. **Gate destructive actions.** No merge, deploy, force-push, history rewrite or secret change without human approval; enforce it in the tool, not the prompt.
5. **Least privilege and sandboxes.** Scope tokens (read + open PR, not admin); run agents in ephemeral sandboxes with an egress allowlist and no production credentials.
6. **Treat repo content as data.** Sanitise untrusted text before it reaches a prompt; never execute model output as shell.
7. **Log everything.** Record every shell command and tool call for audit.

## 8. Governance

If AI writes a large share of your code, AI usage becomes a governed software input. Policy should cover: which models are used and where; how output is checked before it reaches production; who is accountable for merges; and how outcomes (defects, reverts) are tracked over time. Security teams should prioritise remediation where models are least reliable, and set separate review queues and size budgets for agent-generated changes.
