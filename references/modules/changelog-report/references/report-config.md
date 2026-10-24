# Report configuration

This file holds the instance-specific settings for the changelog report. The
build interview fills it in once; every later run reads it. Replace every
`<placeholder>` below with the user's answers.

## GitHub source

- **Organization:** `<org>` — the GitHub org whose repos you track (e.g. `acme`).
- **Repositories:** the repos to track, one per line, with a note on whether
  filtering is needed:

  - `<org>/<repo-1>` — `<all PRs relevant? or filter needed?>`
  - `<org>/<repo-2>` — `<all PRs relevant? or filter needed?>`

## Product scope

If any tracked repo is shared across multiple products, describe how to tell
relevant changes from noise. If all repos are product-specific (every merged PR
is relevant), write "all PRs relevant — no filtering needed."

- **Product name:** `<product>` — the name shown in the summary line and the
  empty-state message.
- **Filter rules (if any):**
  - Include when: `<what makes a PR relevant — keywords, file paths, product
    areas>`
  - Exclude when: `<what makes a PR irrelevant — other product areas, keywords,
    file paths>`
  - When in doubt: skip. A shorter accurate report is better than a longer one
    with irrelevant changes.

## Date resolution

- **Timezone:** `<tz>` — the timezone to resolve relative dates in (e.g.
  `Asia/Kolkata`, `America/New_York`). "Today" and "yesterday" are resolved in
  this timezone; GitHub timestamps are UTC and converted for display.

## Branding

- **Report title:** `<title>` — shown as the H1 in the header (e.g. "Work
  Agents", "Platform", "API").
- **Eyebrow:** `<eyebrow>` — the small uppercase label above the title (usually
  "Changelog").
- **Logo:** `assets/logo.svg` — replace this file with the user's brand logo
  (SVG, embedded as base64 in the PDF). The template expects an SVG.
- **Footer text:** `<footer>` — shown at the bottom of every page (e.g.
  "Generated from today's merged work across <org>'s repositories.").

## Schedule & delivery

- **Frequency:** `<frequency>` — how often the report runs (daily, weekly,
  on-demand, custom).
- **Delivery:** `<delivery>` — where the report is delivered (chat, Slack,
  email, download).
- **Time:** `<time>` — when the report should run (e.g. "morning", "end of
  day", "09:00"). Only applies if frequency is daily or weekly..
