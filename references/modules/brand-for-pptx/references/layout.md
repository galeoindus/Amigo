# Standard Layout — Coordinates & Code

Baseline 16:9 slide grid. Coordinate values are a starting point and should yield to the user’s template when present. Slide reference size: 1920×1080px.

## Positions (Figma px → EMU)

| Element | x (px) | y (px) | w (px) | h (px) | x (EMU) | y (EMU) | cx (EMU) | cy (EMU) |
|---------|--------|--------|--------|--------|---------|---------|----------|----------|
| Eyebrow | 80 | 60 | 1335 | 24 | 1016000 | 762000 | 16954500 | 304800 |
| Heading 1 | 80 | 94 | 1335 | 64 | 1016000 | 1193800 | 16954500 | 812800 |
| Sub Heading | 80 | 168 | 1335 | 33 | 1016000 | 2133600 | 16954500 | 419100 |
| Monogram | 1783 | 60 | 57 | 56 | 22649480 | 762000 | 718370 | 711200 |
| Footer Left | 80 | 1021 | — | 19 | 1016000 | 12966700 | 3035300 | 241300 |
| Footer Right | right-aligned | 1021 | — | 19 | 20244100 | 12966700 | 3035300 | 241300 |
| Content (w/ sub) | 80 | 224 | 1760 | 782 | — | — | — | — |
| Content (no sub) | 80 | 184 | 1760 | 822 | — | — | — | — |

**Gaps:** eyebrow→heading 10px, heading→sub 10px, header→content 24px, content→footer 15px, footer internal 12px. Margins: 80px sides, 60px top, 40px bottom.

## Multi-Line Heading Positions (collision prevention)

The default coordinates above assume a **single-line heading** at 48px (36pt). When a heading wraps to two lines, the fixed subheading position at y=168 causes a collision: the second heading line occupies the space where the subheading sits.

**Always calculate header element positions dynamically based on the heading line count.** Use the tables below.

### Single-line heading (default)

| Element | y (px) | h (px) | y (EMU) |
|---------|--------|--------|---------|
| Eyebrow | 60 | 24 | 762000 |
| Heading (1 line) | 94 | 64 | 1193800 |
| Sub Heading | 168 | 33 | 2133600 |
| Content top (w/ sub) | 224 | — | — |
| Content top (no sub) | 184 | — | — |

### Two-line heading

When the heading text wraps to two lines at 48px (36pt) with 120% line height, each line is ~58px tall. The heading block becomes 116px. All elements below shift down by ~58px.

| Element | y (px) | h (px) | y (EMU) |
|---------|--------|--------|---------|
| Eyebrow | 60 | 24 | 762000 |
| Heading (2 lines) | 94 | 116 | 1193800 |
| Sub Heading | 220 | 33 | 2794000 |
| Content top (w/ sub) | 276 | — | — |
| Content top (no sub, 2-line heading) | 232 | — | — |

**EMU conversion for two-line subheading:** y=220px × 9525 = 2794000.

**Rule:** Before placing the subheading or content, determine whether the heading will wrap. At 48px (36pt) Aptos Display in a 1335px-wide text box, fit varies by font and language; measure after rendering. If the heading exceeds this, use the two-line coordinates. When in doubt, use the two-line positions — a small gap on a one-line heading is better than a collision on a two-line heading.

### Preferred fix: shorten the headline

The content contract says headlines are assertions. A headline that wraps is usually too long. Before falling back to two-line coordinates, try shortening the headline so it fits on one line. Only use the two-line positions when the assertion cannot be made shorter without losing its meaning.

## Text Styling Cleanup

Remove from every `<a:rPr>` on every slide: attribute `b`, attribute `i`, attribute `u`, attribute `strike`, child element `<a:highlight>`.

One example — the pattern is identical for all five:

```xml
<!-- Before: --> <a:rPr b="1" i="1" u="sng" strike="sngStrike" lang="en-US" sz="1800">
                   <a:highlight><a:srgbClr val="FFFF00"/></a:highlight>
                   <a:latin typeface="Aptos"/>
                 </a:rPr>
<!-- After:  --> <a:rPr lang="en-US" sz="1800">
                   <a:latin typeface="Aptos"/>
                 </a:rPr>
```

## XML Skeleton

```xml
<!-- ZONE 1: Header Block -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="10" name="EyebrowTag"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1016000" y="762000"/><a:ext cx="16954500" cy="304800"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
    <a:p><a:r>
      <a:rPr lang="en-US" sz="1200" dirty="0"><a:solidFill><a:srgbClr val="141414"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr>
      <a:t>Eyebrow Tag</a:t>
    </a:r></a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="11" name="Heading1"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1016000" y="1193800"/><a:ext cx="16954500" cy="812800"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
    <a:p><a:r>
      <a:rPr lang="en-US" sz="6400" dirty="0"><a:solidFill><a:srgbClr val="141414"/></a:solidFill><a:latin typeface="Aptos Display"/></a:rPr>
      <a:t>Heading Text Here</a:t>
    </a:r></a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="12" name="SubHeading"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1016000" y="2133600"/><a:ext cx="16954500" cy="419100"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
    <a:p><a:r>
      <a:rPr lang="en-US" sz="2800" dirty="0"><a:solidFill><a:srgbClr val="666666"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr>
      <a:t>Sub heading text here</a:t>
    </a:r></a:p>
  </p:txBody>
</p:sp>

<!-- ZONE 2: Monogram — embed as p:pic -->
<!-- x=22649480, y=762000, cx=718370, cy=711200 -->
<!-- See references/assets.md for embedding pattern -->

<!-- ZONE 3: Footer Bar -->
<p:sp>
  <p:nvSpPr><p:cNvPr id="20" name="FooterLeft"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="1016000" y="12966700"/><a:ext cx="3035300" cy="241300"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
    <a:p><a:pPr algn="l"/>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="999999"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr><a:t>Amigo AI</a:t></a:r>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="B3B3B3"/></a:solidFill><a:latin typeface="Aptos Light"/><a:cs typeface="Aptos Light"/></a:rPr><a:t>  |  </a:t></a:r>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="999999"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr><a:t>AI for All, from India</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>

<p:sp>
  <p:nvSpPr><p:cNvPr id="21" name="FooterRight"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="20244100" y="12966700"/><a:ext cx="3035300" cy="241300"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
  <p:txBody>
    <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
    <a:p><a:pPr algn="r"/>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="999999"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr><a:t>Deck name here</a:t></a:r>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="B3B3B3"/></a:solidFill><a:latin typeface="Aptos Light"/><a:cs typeface="Aptos Light"/></a:rPr><a:t>  |  </a:t></a:r>
      <a:r><a:rPr lang="en-US" sz="800" dirty="0"><a:solidFill><a:srgbClr val="999999"/></a:solidFill><a:latin typeface="Aptos"/><a:cs typeface="Aptos"/></a:rPr><a:t>00</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

## PptxGenJS Equivalent

```javascript
function addStandardLayout(slide, { eyebrow, heading, subHeading, deckName, slideNum }) {
  // Determine if heading will wrap (roughly 42 chars fit on one line at 36pt Aptos Display, w=9.27")
  const headingIsTwoLine = heading.length > 42;

  if (eyebrow) {
    slide.addText(eyebrow, {
      x: 0.56, y: 0.42, w: 9.27, h: 0.17,
      fontFace: 'Aptos', fontSize: 12, color: '141414', align: 'left', lineSpacingMultiple: 1.2,
    });
  }

  // Heading height: 0.44" for 1 line, 0.81" for 2 lines
  const headingH = headingIsTwoLine ? 0.81 : 0.44;
  slide.addText(heading, {
    x: 0.56, y: 0.65, w: 9.27, h: headingH,
    fontFace: 'Aptos Display', fontSize: 48, color: '141414', align: 'left', lineSpacingMultiple: 1.2,
  });

  // Subheading y shifts down when heading is 2 lines
  // 1-line: y=1.17, 2-line: y=1.53
  const subY = headingIsTwoLine ? 1.53 : 1.17;
  if (subHeading) {
    slide.addText(subHeading, {
      x: 0.56, y: subY, w: 9.27, h: 0.23,
      fontFace: 'Aptos', fontSize: 21, color: '666666', align: 'left', lineSpacingMultiple: 1.2,
    });
  }

  // Content zone shifts based on heading lines and subheading presence
  // 1-line heading + sub:    y=1.56
  // 1-line heading, no sub:  y=1.28
  // 2-line heading + sub:    y=1.92
  // 2-line heading, no sub:  y=1.61
  let contentY;
  if (subHeading) {
    contentY = headingIsTwoLine ? 1.92 : 1.56;
  } else {
    contentY = headingIsTwoLine ? 1.61 : 1.28;
  }
  const contentH = 7.5 - contentY - 0.5; // leave 0.5" before footer at y=7.09

  slide.addImage({ path: 'assets/logo/Amigo Monogram Black.png', x: 12.38, y: 0.42, w: 0.39, h: 0.39 });
  slide.addText([
    { text: 'Amigo AI', options: { fontFace: 'Aptos', fontSize: 8, color: '999999' } },
    { text: '  |  ', options: { fontFace: 'Aptos Light', fontSize: 8, color: 'B3B3B3' } },
    { text: 'AI for All, from India', options: { fontFace: 'Aptos', fontSize: 8, color: '999999' } },
  ], { x: 0.56, y: 7.09, w: 3.0, h: 0.13, align: 'left' });
  slide.addText([
    { text: deckName || 'Deck name here', options: { fontFace: 'Aptos', fontSize: 8, color: '999999' } },
    { text: '  |  ', options: { fontFace: 'Aptos Light', fontSize: 8, color: 'B3B3B3' } },
    { text: String(slideNum).padStart(2, '0'), options: { fontFace: 'Aptos', fontSize: 8, color: '999999' } },
  ], { x: 9.78, y: 7.09, w: 3.0, h: 0.13, align: 'right' });

  return { contentY, contentH };
}
```