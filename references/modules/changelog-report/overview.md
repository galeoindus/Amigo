# Module guide: Changelog Report

> Integrated capability: A print-optimized HTML template + method for producing a daily (or range)

# Changelog Report

A method + print-optimized HTML template for turning a day's (or range's)
merged GitHub PRs into a readable, branded PDF changelog written for
non-technical readers. The report is the deliverable; the chat reply is a
one-line pointer to it.

## When to use

Use this skill when generating a changelog report that will be rendered as
HTML and then converted to PDF (via WeasyPrint or similar). The HTML it
produces is print-first: it is designed to look correct as a PDF, not as a web
page.

## One-time setup — read the config

Before first use, this skill needs to know about your setup: which GitHub org
and repos to track, how to filter shared repos to your product area, what
branding to use, what timezone to resolve dates in, and what the footer should
say. That knowledge lives in `references/report-config.md`. If it is empty or
missing, ask the user the setup questions (see the builder skill) and fill it
in before proceeding.

## How it works

1. Load the skill via `skill_view("changelog-report")` to get the `sandbox_dir`.
2. Read the template: `read_file("<sandbox_dir>/assets/changelog-template.html")`.
3. Read the logo: `read_file("<sandbox_dir>/assets/logo.svg")`.
4. Convert the logo to a base64 data URI: `"data:image/svg+xml;base64," + base64_encode(svg_content)`.
5. Read `references/report-config.md` for the org, repos, product filter,
   branding, timezone, and footer text.
6. Replace the template placeholders (`{{DATE}}`, `{{DATE_LONG}}`, `{{SUMMARY}}`,
   `{{SECTIONS}}`, `{{LOGO}}`, `{{TITLE}}`, `{{EYEBROW}}`, `{{FOOTER}}`) with
   actual content.
7. Write the filled HTML to a file and convert to PDF with WeasyPrint.

**Important:** Both the template and the logo are in the `assets/` directory.
They are uploaded to the sandbox filesystem when `skill_view` runs, so
`read_file()` will find them on disk. Do NOT use the `templates/` path — that
directory is not uploaded to disk and will cause a "file not found" error.

## Template structure

The template uses these critical print CSS techniques:

### Page setup with margin box footer
```css
@page {
  size: A4;
  margin: 20mm 18mm 25mm 18mm;

  @bottom-center {
    content: "{{FOOTER}}";
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    color: #6b7280;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    color: #6b7280;
  }
}
```
The footer lives in the `@bottom-center` margin box — it appears on every page
but never collides with body content.

### Vertical timeline layout (border-left, not pseudo-element)
```css
.timeline {
  border-left: 2px solid #d1d5db;
  padding-left: 26px;
}
```
The timeline uses a `border-left` on the `.timeline` container, NOT a
`position: absolute` pseudo-element. This is critical: in WeasyPrint's paged
media model, borders on block elements repeat across page breaks, while
absolutely-positioned pseudo-elements only render on the first page. The
vertical grey line must continue on every page.

Each entry has a solid dark grey dot (`#374151`) positioned on the line.
Section headings have NO dots next to them — only entries do.

### Entry-level page break protection
```css
.changelog-entry {
  break-inside: avoid;
  page-break-inside: avoid;
}
```
Each changelog entry (title + contributors + details) is treated as an atomic
block. WeasyPrint will move the whole block to the next page rather than
splitting it mid-sentence.

### Section-level break control
```css
.changelog-section {
  break-inside: auto;
}
.changelog-section__heading {
  break-after: avoid;
}
```
Sections can span pages (they may contain many entries), but a section heading
will never be orphaned at the bottom of a page — it always stays with its first
entry.

## Content format

The template expects these placeholders:

- `{{DATE}}` — the report date in dd/mm/yyyy format (e.g. "16/08/2026")
- `{{DATE_LONG}}` — the date in long form (e.g. "Saturday, 16 August 2026")
- `{{TITLE}}` — the report title (e.g. "Work Agents", "Platform")
- `{{EYEBROW}}` — the small uppercase label above the title (e.g. "Changelog")
- `{{SUMMARY}}` — 1-line summary. For 1-5 PRs: "N PRs merged across <repos> for
  <product> — #xxx, #yyy." For 6+ PRs: "N PRs merged across <repos> for
  <product>." If zero: "No changes for <product> on <date>."
- `{{LOGO}}` — a base64 data URI of the logo SVG (see How it works above)
- `{{FOOTER}}` — the footer text (from config)
- `{{SECTIONS}}` — HTML blocks for each section, structured as:

```html
<section class="changelog-section changelog-section--fixed">
  <h2 class="changelog-section__heading">Fixed</h2>
  <div class="changelog-entry">
    <h3 class="changelog-entry__title">Translated replies no longer disappear from chat</h3>
    <div class="changelog-entry__contributors"><span class="changelog-entry__date">15 Aug</span><strong>by</strong> contributor <a href="https://github.com/org/repo/pull/955">#955</a></div>
    <p class="changelog-entry__text">Translated replies in Indian languages were silently disappearing from chat — on web from the second message onward, on mobile from the very first. The text now streams correctly on every turn and survives a page reload, on both web and mobile.</p>
  </div>
</section>
```

### Entry structure

Each entry has three parts:
1. **Title** (`changelog-entry__title`) — a one-line title from the user's
   job-to-be-done perspective. What problem did this solve or what capability
   did it add? Written in plain English, not technical.
2. **Contributors** (`changelog-entry__contributors`) — starts with the merge
   date in bold (`changelog-entry__date` span, format `dd Mon` e.g. "15 Aug"),
   then the GitHub usernames of who shipped the change prefixed with "by",
   followed by the PR number as a clickable link. Use the PR author's
   `user.login` field and `pr['html_url']` for the link. Format: `15 Aug · by
   contributor #955` where `#955` is an `<a>` tag linking to the PR URL. If
   multiple people contributed: `15 Aug · by contributor #955, another #951`.
   **Entries within each section must be sorted chronologically by
   `merged_at` — oldest first.**
3. **Details** (`changelog-entry__text`) — the plain-English explanation of what
   changed and why it matters. **Keep to 2-3 sentences maximum.** No jargon, no
   class names, no file paths.

### Section CSS modifiers

Use these class modifiers on the `changelog-section` element. Note: these only
color the section heading text, not the entry boxes (entries have no colored
background):
- `changelog-section--new` — green accent (new features)
- `changelog-section--improved` — teal accent (improvements)
- `changelog-section--fixed` — rose accent (bug fixes)
- `changelog-section--hood` — grey accent (under the hood)

## Assets

Both assets are in the `assets/` directory and are uploaded to the sandbox
filesystem by `skill_view`:

- `assets/changelog-template.html` — the print-optimized HTML template
- `assets/logo.svg` — the logo (placeholder; the build interview replaces this
  with the user's brand logo)

## PDF conversion

After generating the HTML, convert to PDF using WeasyPrint:

```python
from weasyprint import HTML
HTML('/path/to/changelog.html').write_pdf('/path/to/changelog.pdf')
```

WeasyPrint is the recommended converter because it has full support for
`@page` margin boxes, `break-inside: avoid`, `border-left` page-break
repetition, and CSS Paged Media — the features this template relies on.

## Quality checks before delivery

After generating the PDF, verify:
- No sentence is split across two pages (each entry is atomic)
- The footer appears at the bottom of each page, not in the content area
- Section headings are not orphaned at the bottom of a page
- Page numbers appear in the bottom-right corner
- The logo appears in the top-right of the header
- Each entry has a title, a contributors line with merge date + username + PR
  link (#xxx), and details (2-3 sentences)
- Entries within each section are sorted chronologically (oldest merge first)
- The layout is a vertical grey timeline with solid dark grey dots on entries
  only — section headings (Fixed, Improved, etc.) have NO circles next to them
- The vertical grey timeline line continues on every page (not just page 1)
- The report fits cleanly — if it's only slightly over one page, consider
  tightening summaries rather than spilling a few lines onto page 2
