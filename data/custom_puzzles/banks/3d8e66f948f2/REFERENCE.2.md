# New Primitive for Set 9 — `orbit_cells`

## Signature

```text
orbit_cells(base_grid, cells, pivot, turns=(0,1,2,3), keep_original=True, recolor_by_turn=None)
```

## Purpose

Replay a set of colored cells around a pivot by quarter turns. This is useful whenever the task gives one canonical orientation of a motif and expects rotational copies.

## Arguments

- `base_grid`: the grid to start from
- `cells`: a list of `(row, col, color)` cells describing the source motif
- `pivot`: the `(row, col)` pivot cell
- `turns`: which quarter turns to apply; `0` means original orientation, `1` means +90°, `2` means 180°, `3` means 270°
- `keep_original`: whether to preserve the source cells already present in `base_grid`
- `recolor_by_turn`: optional map from turn index to replacement color

## Semantics

For each source cell, compute its offset from the pivot. Then apply the requested quarter-turn rotations to that offset and write the resulting cells back into the grid. When `recolor_by_turn` is supplied, geometry comes from the source motif but color comes from the turn slot.

## Why this primitive helps

Without a helper like this, the solver has to re-derive the same rotation arithmetic every time:

- translate cells into pivot-relative offsets
- rotate `(dr, dc)` into `(dc, -dr)`, `(-dr, -dc)`, and `(-dc, dr)`
- translate back into absolute coordinates
- optionally recolor per turn

That is exactly the kind of repeated geometric bookkeeping that is easy to get wrong in handwritten rules and expensive to rediscover inside an iterative loop.

## Direct uses in this pack

- **E57** — copy all non-pivot cells to all four rotational positions
- **M57** — orbit only the selector-chosen color
- **H57** — orbit a source motif and recolor each turn from a legend row
