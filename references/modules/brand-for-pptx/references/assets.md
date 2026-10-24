# Amigo Decorative Shape Assets

The package includes 22 generic Amigo decorative motifs in SVG and PNG form under `assets/shapes/`. They are designed as flexible accents for section dividers, visual examples, and restrained slide decoration. They are not tied to a product model, customer, or third-party brand.

## Asset registry

| Asset | Recommended use |
|---|---|
| Assets 01–05 | Warm organic petals, circles, and rounded geometry |
| Assets 06–10 | Lantern, rosette, arch, and clover motifs |
| Assets 11–15 | Scalloped circles, butterfly, and bright warm accents |
| Assets 16–18 | Wide split form, frame, and soft daisy motifs |
| Assets 19–22 | Rounded frames, scalloped circles, and clover motifs |

Choose one visual motif per deck or section, not a new shape on every slide. Keep all ornaments subordinate to the slide's message. Use PNG in PPTX when reliable raster embedding is needed; use SVG in web/HTML when vector scaling is supported.

## Wordmarks and monograms

The bundled `assets/logo/` directory contains black/dark and white variants in SVG and PNG. Use a dark wordmark on a light background; use the white version only over a sufficiently dark or saturated area. Do not recolor the logos ad hoc.

## Embedding images in PPTX

Prefer the presentation library's supported image API to manage relationships and content types. If editing OOXML manually, ensure each image part has a matching relationship and content type; do not copy a relationship ID without checking for conflicts.

## HTML use

Use a relative asset path and meaningful alternative text for informative images. Decorative images should have an empty alt attribute so they are not read aloud.
