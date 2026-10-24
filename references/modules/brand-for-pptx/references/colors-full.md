# Amigo Color Palette and Gradients

The Amigo default palette is warm and friendly, with a warm-to-cool gradient for cover and closing slides. If a user supplies another brand palette, preserve it rather than imposing this default.

## Core colors

| Token | Hex | Use |
|---|---|---|
| Amigo Orange | `#E6651B` | Primary warm accent |
| Deep Orange | `#A5460F` | Strong warm emphasis |
| Soft Orange | `#FEEDE6` | Background tint |
| Amigo Indigo | `#3333CC` | Cool primary accent |
| Soft Indigo | `#E8EFFC` | Background tint |
| Teal | `#0F766E` | Secondary accent; use sparingly |
| Dark Text | `#141414` | Main text on light backgrounds |
| Muted Text | `#666666` | Supporting labels |
| White | `#FFFFFF` | Light slide background / reversed text |
| Light Neutral | `#F5F5F5` | Alternate content background |
| Border | `#E6E6E6` | Dividers and subtle edges |

## Supporting shades

| Family | Shades (dark to light) |
|---|---|
| Red | `#3E140B`, `#52170E`, `#781A11`, `#8E1912`, `#A21913`, `#B81514`, `#C43D2B`, `#DB715C`, `#EBA18F`, `#F8D1C6`, `#FDE7E2` |
| Pink | `#4D192C`, `#611C35`, `#731E3F`, `#871F4B`, `#9D2055`, `#B12060`, `#D4508E`, `#E380A8`, `#EFABC5`, `#F9D5E1`, `#FCEAF0` |
| Indigo | `#11115B`, `#212191`, `#3333CC`, `#4250D5`, `#556ADC`, `#6A88E2`, `#81A0E9`, `#A7C0F1`, `#D2DFF9`, `#E8EFFC`, `#FAFCFF` |
| Green | `#152605`, `#263D0E`, `#385418`, `#496D21`, `#6EA335`, `#83C040`, `#90C85B`, `#ACD587`, `#C8E4B0`, `#E3F1D8`, `#F2F8EB` |
| Yellow | `#362813`, `#6B4C1C`, `#A27224`, `#C08827`, `#DF9C2A`, `#FEB12B`, `#FFB94A`, `#FFCB79`, `#FFE8B7`, `#FFF0CF`, `#FFF8E6` |
| Orange | `#682906`, `#A5460F`, `#E6651B`, `#E96C2F`, `#EE7944`, `#F38858`, `#F59970`, `#FABB9E`, `#FDDCCE`, `#FEEDE6`, `#FFFBFA` |
| Neutral | `#1F1F1F`, `#292929`, `#3D3D3D`, `#666666`, `#999999`, `#B3B3B3`, `#CCCCCC`, `#E6E6E6`, `#F0F0F0`, `#F6F6F6`, `#FAFAFA` |

## Amigo Main Gradient (warm → cool)

Use as a full-bleed cover or closing background when it strengthens the story. Stops: `#AA490D` at 0%, `#F9730C` at 25%, `#FFB053` at 55%, `#BED2FF` at 75%, and `#F4F7FF` at 100%. The package includes a pre-rendered `assets/gradients/main-gradient.png`.

Over dark/warm areas, use white text and the white wordmark. Over light/cool areas, use dark text and the dark wordmark. Do not place the wordmark where it loses contrast. Content slides usually use white or near-white backgrounds; do not force the gradient onto every slide.

## PowerPoint XML examples

Solid fill: `<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>`

Main gradient fill: use stops `AA490D`, `F9730C`, `FFB053`, `BED2FF`, `F4F7FF` with increasing `a:gs pos` values.

## Contrast

Check text contrast for the final foreground/background pair; do not assume a color is accessible just because it is in the palette. Use text labels and shapes as well as color to communicate meaning. See the W3C source in `../../research-notes.md`.
