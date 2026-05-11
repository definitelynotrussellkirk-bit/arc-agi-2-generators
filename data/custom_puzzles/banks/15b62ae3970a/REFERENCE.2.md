# New Primitive for Set 15 — `resolve_chambers`

## Signature

```text
resolve_chambers(base_grid, wall_color, reducer, preserve_walls=True)
```

## Purpose

Treat wall-separated chambers as first-class objects.

Many ARC-style tasks are easiest to solve by first partitioning the grid with a designated wall color and then reasoning chamber by chamber. Without an explicit helper, the solver has to repeatedly rediscover the same low-level flood-fill logic before it can do anything interesting. `resolve_chambers` makes the partition step explicit and reusable.

## Arguments

- `base_grid`: the full input grid
- `wall_color`: the color that acts as an impermeable barrier
- `reducer`: a chamber-local function receiving `(chamber_cells, markers, grid)`
- `preserve_walls`: when true, copy wall cells through unchanged

Here `markers` means all nonzero, non-wall cells already present inside that chamber.

## Semantics

1. Find connected components of cells that are **not** the wall color.
2. Treat each such component as one chamber.
3. Gather the chamber's marker cells and pass them to `reducer`.
4. Use the reducer's return value to paint that chamber.

The reducer can return either:

- a **single color**, meaning “paint the whole chamber with this value”, or
- a **cell-to-color mapping**, meaning “paint each chamber cell according to a chamber-local pattern.”

That second form is what lets the same helper support both simple fills and richer chamber-local textures.

## Why this helper matters

`resolve_chambers` encourages a stronger staged decomposition:

1. identify the wall color,
2. segment the grid into chambers,
3. summarize the markers per chamber,
4. apply a chamber-local rule.

That is often much easier for an iterative solver than trying to reason about the entire grid at once. It also keeps chamber tasks from collapsing into ad hoc nested loops and duplicated flood-fill code.

## Direct uses in this pack

- **E99** — fill each chamber from its single seed color
- **M99** — fill each chamber with the maximum marker color found inside it
- **H99** — fill each chamber with a checkerboard made from its smallest and largest marker colors
