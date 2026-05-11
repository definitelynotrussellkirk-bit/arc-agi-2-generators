# New Primitive for Set 10 — `broadcast_motif`

## Signature

```text
broadcast_motif(base_grid, motif_cells, src_anchor, dst_anchors, keep_anchors=True, recolor=None)
```

## Purpose

Copy a sparse motif from one anchored location to one or more new anchors without first turning it into a dense rectangular template.

## Arguments

- `base_grid`: the starting grid
- `motif_cells`: a list of `(row, col, color)` cells describing the source motif
- `src_anchor`: the source anchor `(row, col)` used to define offsets
- `dst_anchors`: a sequence of destination anchor coordinates
- `keep_anchors`: whether to preserve the destination anchor cells already present in the grid
- `recolor`: optional replacement color, per-anchor color list, or per-anchor color map

## Semantics

For every motif cell, compute its offset from the source anchor. Then replay that offset at every destination anchor. Geometry stays the same; only absolute position changes. When `recolor` is supplied, the copied cells can all be recolored uniformly or recolored differently for each destination anchor.

## Why this primitive helps

A lot of ARC-style rules say some version of:

- find the one example motif
- convert it into relative offsets
- find all target anchors
- replay the same sparse pattern at each anchor
- maybe recolor each replay based on a selector or legend

That logic is conceptually simple, but handwritten rules tend to repeat the same offset bookkeeping over and over. A helper like `broadcast_motif` makes the intended operation explicit and keeps the solver focused on the real puzzle logic: which cells belong to the motif, which anchors count, and whether copied motifs keep their colors or get recolored.

## Direct uses in this pack

- **E64** — copy the full sparse motif from the unique 5 anchor to every 6 anchor
- **M64** — copy only the selector-colored subset of the source motif
- **H64** — copy the source motif to ordered anchors and recolor each copy from a top-row legend
