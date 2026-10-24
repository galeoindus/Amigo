# Existing PowerPoint Editing Workflow

1. Inventory slides, masters, layouts, media, fonts, and theme before changing the file.
2. Extract slide text and confirm the order and intended scope.
3. Use the least invasive edit that satisfies the request; preserve geometry and editable objects unless redesign is requested.
4. Track changes to text, color, typography, geometry, and assets separately so regressions can be isolated.
5. Rebuild a copy of the original; never silently overwrite it.
6. Render every slide, inspect the full deck, fix issues, and render again.
7. Compare extracted text and slide count before/after; verify there are no missing shapes, hidden text, broken relationships, or unintended content changes.

If a source element is unsupported by the available tooling, report it and keep it unchanged rather than inventing a replacement.
