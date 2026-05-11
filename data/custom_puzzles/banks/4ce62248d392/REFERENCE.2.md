# New Primitive for Set 12 — `pack_components`

## Signature

```text
pack_components(component_grids, axis="horizontal", gap=1, canvas_size=None, anchor=(0, 0))
```

## Purpose

Lay out a list of already-cropped components into a clean strip or column.

This helper is aimed at ARC tasks where the real reasoning work is:

- deciding which objects to keep
- choosing their order
- optionally transforming them first

Once those decisions are made, the final step is often a deterministic packing operation. A dedicated primitive keeps that bookkeeping separate from the higher-level selection logic.

## Arguments

- `component_grids`: a list of cropped component grids to place
- `axis`: `"horizontal"` for left-to-right packing or `"vertical"` for top-to-bottom packing
- `gap`: the number of blank rows or columns between consecutive packed components
- `canvas_size`: optional `(height, width)` for the target canvas; when omitted, the primitive creates the smallest canvas that fits the packed strip
- `anchor`: the `(row, col)` position where the first packed component should be placed

## Semantics

1. Start from a blank canvas, either of the supplied `canvas_size` or of the minimal fitting size.
2. Place the first component at `anchor`.
3. For horizontal packing, advance the write cursor by the component width plus `gap`.
4. For vertical packing, advance the cursor by the component height plus `gap`.
5. Repeat until every component has been placed.

The primitive does **not** decide which objects to keep or how to order them. Those choices belong to the task-specific rule.

## Why this primitive helps

ARC tasks frequently ask for an output strip assembled from extracted objects, sorted shapes, or transformed crops. Without a helper, the solver has to repeatedly re-implement:

- tight cropping
- cursor management
- one-cell or one-row gaps
- blank-canvas allocation
- horizontal versus vertical placement logic

`pack_components` collapses that repetitive layout logic into one explicit, reusable step.

## Used directly in this set

- **E78 — Pack Components by Area**
- **M78 — Legend-Ordered Pack**
- **H78 — Zone Commands: Transform and Pack**

## Minimal reference implementation

```python
def pack_components(component_grids, axis="horizontal", gap=1, canvas_size=None, anchor=(0, 0)):
    if canvas_size is None:
        if axis == "horizontal":
            h = max(len(g) for g in component_grids) if component_grids else 1
            w = sum(len(g[0]) for g in component_grids) + gap * max(0, len(component_grids) - 1)
        else:
            h = sum(len(g) for g in component_grids) + gap * max(0, len(component_grids) - 1)
            w = max(len(g[0]) for g in component_grids) if component_grids else 1
    else:
        h, w = canvas_size

    out = [[0] * w for _ in range(h)]
    r, c = anchor
    for comp in component_grids:
        for rr, row in enumerate(comp):
            for cc, val in enumerate(row):
                if val:
                    out[r + rr][c + cc] = val
        if axis == "horizontal":
            c += len(comp[0]) + gap
        else:
            r += len(comp) + gap
    return out
```
