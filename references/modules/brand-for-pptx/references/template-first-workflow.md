# Template-first PPTX workflow (master guide)

> Merged from the `pptx-master` pack. Use when a `.pptx` is input, output, or both. The Amigo visual system (palette, assets, layout) lives in `../overview.md` and the other reference files in this folder.

Template-first workflow. Every deck starts from a template if one is provided — a reference deck of pre-built on-brand layouts with fonts embedded. Duplicate the layout you need, swap content, save. Do not build slides from raw XML.

## Routing (pick one)

| Task | Do this |
|---|---|
| Create a new deck (no .pptx attached) | Build from the bundled Amigo assets and layout, or from a user template if supplied |
| Edit / rebrand an existing deck (.pptx attached) | Edit in place at the run level, preserving structure |
| QA-only review | Run the QA section below |
| Brand question only ("what hex is the accent?") | Read `../overview.md` and `colors-full.md` |

**Every create or edit run ends with QA.** Not optional.

## If a template deck is supplied

A template may be a sibling `template.pptx` of this module or one the user attached. When present:

1. **Browse template thumbnails first** (once per task):
   ```bash
   mkdir -p thumbs
   soffice --headless --convert-to pdf --outdir thumbs template.pptx
   pdftoppm -jpeg -r 80 thumbs/template.pdf thumbs/t
   ```
   Then view the thumbnails and pick layouts by slide number. Ignore any section-marker slides (often a solid brand colour) — never copy one into output.
2. **Copy the template to a working file:** `cp template.pptx deck.pptx`.
3. **Delete unused slides**, keeping only the layouts you picked, in the order you want.
4. **Replace text at the run level** (see below), reusing the template's runs so font/size/colour survive.
5. **Swap images** where needed; keep shape positions and only replace the image fill.
6. **Run QA.**

If no template is supplied, build from the bundled Amigo assets and the layout in `layout.md`, and say you used the default Amigo layouts.

## Create

1. Pick layouts that match the user's outline.
2. Copy the template (or start from the default) to `deck.pptx`.
3. Keep only the needed slides, in order.
4. Replace text content using `paragraph.runs[i].text = "..."` on **existing runs** to preserve styling. Never build new text frames from scratch — reuse the template's. Assigning `shape.text_frame.text` collapses the paragraph to a single run and drops inline formatting; avoid it for edits.
5. Swap images where needed.
6. Run QA.

**Rule:** If a layout's content does not fit the message, pick a different layout — do not force text into a slot. If no layout fits, tell the user and ask which section to extend.

## Edit

1. **Extract what is there** and **render thumbnails** of the user's deck.
2. **For each slide**, decide: keep as-is, fix in place, or replace with a template layout.
   - **Fix in place** when structure is fine but fonts/colours/footer are off.
   - **Replace** when structure is wrong (e.g. a text-only slide, a non-brand layout). Copy a matching layout in and port content over.
3. **Apply the hard rules to every slide touched.** Edit at the run level so untouched runs stay byte-identical.
4. **Run QA.**

## QA

Run after every create or edit. Three checks:

**1. Content check** — no placeholder text left:
```bash
extract-text deck.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|caption text here|sub divider|cover / title"
```
Any hit = unfixed placeholder. Fix before shipping.

**2. Visual check** — render and inspect:
```bash
soffice --headless --convert-to pdf deck.pptx
rm -f qa-*.jpg
pdftoppm -jpeg -r 150 deck.pdf qa
ls -1 "$PWD"/qa-*.jpg
```
Then view each slide. Look for text overflow past shape bounds, overlaps, a missing footer/monogram on content slides, non-brand fonts, black backgrounds, and raw `#000000` text.

**3. Hard rules check** — run through the list below. Every violation = fix before shipping.

Stop after one fix-and-verify cycle. Do not chase sub-pixel nudges.

## Hard rules (apply to every slide touched)

1. **Fonts:** Season Mix (headings only) or Matter (everything else). No Arial, Calibri, Helvetica. No italics, underlines, strikethrough, highlights, or the bold attribute — weight comes from the font name (e.g. "Matter SemiBold"). If the brand fonts are not installed, fall back to Aptos/Arial/Noto Sans and verify glyph coverage.
2. **Colours:** light backgrounds or the main gradient (title/closing only). Never `#000000` or a dark charcoal as a background. Text is `#141414`, never `#000000`. See `colors-full.md`.
3. **Footer + monogram on every content slide.** Footer left: the deck's owner/brand line (configurable — do not hard-code another company's tagline). Footer right: zero-padded slide number. Monogram top-right. Present in the template layouts — do not remove them.
4. **Every content slide has a visual** — image, chart, icon, or a shape from `assets/shapes/`. No text-only content slides.
5. **Every visual is accompanied by supporting data or explanatory text** — no standalone diagrams, infographics, or charts without numbers, labels, or a written explanation alongside them on the same slide.
6. **Preserve the deck's theme.** Do not flip themes unless the user asks.
7. **Section-marker slides never appear in output.** They are template scaffolding only.
8. **Readable contrast** and a logical reading order; do not signal status by colour alone.
