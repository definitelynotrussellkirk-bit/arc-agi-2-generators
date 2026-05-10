# New Primitive for Set 17: `palette_lift`

## Overview

This set introduces a palette-substitution helper:

```text
palette_lift(template, legend, transform=None, symbol_order=None)
```

The idea is to let a motif be **symbolic** rather than fully colored.  
Inside the motif, values like `1`, `2`, and `3` mean “first palette slot,” “second palette slot,” and “third palette slot,” not literal final colors. A separate legend row provides the actual colors to substitute.

An optional transform can be applied before recoloring, so the same symbolic motif can be reused in different orientations.

## Why this is useful

ARC tasks often separate:

1. **shape structure**, and
2. **final color choice**.

Without a helper like `palette_lift`, a solver has to re-implement the same sequence repeatedly:

- crop the symbolic motif,
- decode the legend,
- optionally rotate or flip the motif,
- substitute every symbolic channel with its real output color.

`palette_lift` compresses that pattern into one reusable operation.

## Suggested signature

```python
palette_lift(template, legend, transform=None, symbol_order=None)
```

Where:

- `template` is a grid containing `0` for background and small symbolic values like `1/2/3`
- `legend` is an ordered list of output colors
- `transform` is optional and may be one of the standard geometric transforms
- `symbol_order` optionally overrides the default ascending symbol order

## Semantics

Given

```text
legend = [4, 7, 3]
template =
010
121
003
```

the recolored output is

```text
040
474
003
```

because:

- every `1` becomes `4`
- every `2` becomes `7`
- every `3` becomes `3`

If a transform is supplied, apply it first and then perform the palette substitution.

## Direct uses in this pack

- **E113 — Neutral Glyph Recolor**  
  A single symbolic motif is recolored by the header palette.

- **M113 — Palette-Lift Strip Assembly**  
  A keyed bank of symbolic 2×2 blocks is selected, recolored, and concatenated into a strip.

- **H113 — Palette-Lift Matrix with Commands**  
  A selector matrix chooses symbolic 3×3 templates, a command matrix transforms each slot locally, and the final matrix is assembled from recolored blocks.

## Minimal reference implementation

```python
def palette_lift(template, legend, transform=None, symbol_order=None):
    if transform is not None:
        template = apply_transform(template, transform)
    if symbol_order is None:
        symbol_order = sorted({v for row in template for v in row if v != 0})
    mapping = {sym: color for sym, color in zip(symbol_order, legend)}
    out = [[0 for _ in row] for row in template]
    for r in range(len(template)):
        for c in range(len(template[0])):
            v = template[r][c]
            if v != 0:
                out[r][c] = mapping.get(v, v)
    return out
```

## What makes it new relative to recent helpers

Earlier helpers in the series centered on routing, orbiting, panel composition, chamber reasoning, or transform inference. `palette_lift` is different because it treats color as a **late-bound parameter**. The same geometric motif can be reused with many palettes, which is a compact way to express a family of ARC tasks where structure and color are intentionally decoupled.