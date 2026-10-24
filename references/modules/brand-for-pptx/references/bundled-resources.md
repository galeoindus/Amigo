# Amigo Presentation Bundle Manifest

The presentation module is self-contained and ships with its own generic Amigo branding assets. Asset paths below are relative to this module directory.

```text
brand-for-pptx/
├── overview.md
├── references/
│   ├── assets.md
│   ├── bundled-resources.md
│   ├── colors-full.md
│   ├── design-ideas.md
│   ├── layout.md
│   └── qa.md
└── assets/
    ├── logo/
    │   ├── Amigo Wordmark Black.svg / .png
    │   ├── Amigo Wordmark White.svg / .png
    │   ├── Amigo Monogram Black.svg / .png
    │   └── Amigo Monogram Black-1.svg / .png
    ├── shapes/ (Assets 01–22, SVG and PNG)
    └── gradients/main-gradient.png (1920 × 1080)
```

The package validation script verifies expected logo, shape and gradient files. If an optional image cannot be loaded by a tool, fall back to available native PowerPoint shapes only after checking the visual result; never claim a missing asset was embedded.

## Fonts

No font binaries are distributed. Prefer Aptos Display and Aptos, with Arial/Noto Sans fallbacks. If the target system substitutes fonts, render and inspect text wrapping and multilingual shaping.
