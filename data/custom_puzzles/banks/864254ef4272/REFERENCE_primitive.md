# Helper Primitive Spec — `rebase_component`

## Signature

```text
rebase_component(base_grid, source_cells, anchors, origin='bbox_topleft', recolor='keep'|'anchor', transform='id')
```

## Purpose

Normalize a source component to the top-left corner of its own bounding box, optionally transform it, and then replay that normalized shape at one or more anchor locations.

This is useful when a puzzle says, in effect:

- “take this learned shape and copy it elsewhere,”
- “copy the same shape but recolor it to match the anchor,” or
- “copy the same shape but rotate it first.”

## Parameters

- `base_grid`  
  The canvas you will paint onto.

- `source_cells`  
  A list of source component cells, typically triples `(r, c, value)`.

- `anchors`  
  A list of anchor locations. Each entry can be:
  - `(r, c)` if no anchor color is needed, or
  - `(r, c, anchor_color)` if recoloring depends on the anchor.

- `origin='bbox_topleft'`  
  The placement origin. In this set, the normalized component is aligned by its bounding-box top-left corner.

- `recolor='keep'|'anchor'`  
  - `keep`: preserve the source colors  
  - `anchor`: recolor every nonzero source cell to the anchor color

- `transform='id'`  
  Optional transform applied before placement. Typical values:
  - `id`
  - `rot90`
  - `rot180`
  - `rot270`
  - `flip_h`
  - `flip_v`
  - `diag`
  - `anti`

## Operational intuition

1. Extract the source component.
2. Crop it conceptually to its own bounding box.
3. Convert its cells into normalized offsets from that bounding-box origin.
4. Optionally transform those offsets.
5. Stamp the resulting offsets at each anchor.

## Why this primitive matters

Without it, the solver tends to reinvent the same logic repeatedly:

- component extraction
- bbox normalization
- coordinate offsetting
- optional rotation/reflection
- recolor-or-keep decisions
- replay at multiple anchors

That is exactly the kind of repeated structural work worth elevating into a reusable primitive.

## Used directly in Set 6

- **E41 — Glyph Broadcast From Anchors**  
  Copy one learned glyph to every anchor, recolored to the anchor color.

- **M41 — Recolor Broadcast Component**  
  Copy a multicolor source component to several anchors, but repaint each copy uniformly with the anchor’s color.

- **H36 — Command-Rotated Broadcast**  
  Copy a learned source component to multiple anchors, but apply a command-specific rotation before each placement.

## Minimal pseudocode

```python
def rebase_component(base_grid, source_cells, anchors, recolor='keep', transform='id'):
    norm = normalize_to_bbox_top_left(source_cells)
    norm = apply_transform(norm, transform)
    out = clone(base_grid)
    for anchor in anchors:
        for rr, cc, value in norm:
            paint = value if recolor == 'keep' else anchor.color
            out[anchor.r + rr][anchor.c + cc] = paint
    return out
```
