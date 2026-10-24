# PPTX Generation with PptxGenJS

Use the library's native APIs for text, shapes, charts, images, and speaker notes when supported. Keep layout data in reusable helpers rather than copying coordinates everywhere.

## Safe starting pattern

```js
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Amigo';
pptx.subject = 'Presentation';
pptx.title = 'Presentation title';
pptx.company = 'Amigo';
pptx.lang = 'en-US';
// Add slides and content using the current PptxGenJS API.
// Render and inspect the exported file before delivery.
```

Confirm the installed library version and API documentation before using version-specific features. Use relative asset paths based on the script directory where possible; check every path exists before embedding. When adding charts, include labels, units, data labels where useful, and an accessible textual takeaway.
