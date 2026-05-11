# New Primitive for Set 11 — `link_terminals`

## Signature

```text
link_terminals(base_grid, endpoints, color_mode="endpoint", allow_bends=False, bend_policy="row-first", overlap_color=None, include_endpoints=True)
```

## Purpose

Connect matched terminal cells with explicit Manhattan paths.

This primitive is meant for ARC tasks where colored endpoint cells imply an unseen segment or route. In the easy setting the route is a straight line. In the medium and hard setting it may need one bend, and collisions between routes may themselves become semantically meaningful.

## Arguments

- `base_grid`: the grid to paint onto
- `endpoints`: a list of `(row, col, color)` terminal cells; typically there are exactly two terminals per active color
- `color_mode`: either `"endpoint"` to paint with each pair's own color, or a fixed color value
- `allow_bends`: whether non-aligned pairs may be connected with a single Manhattan bend
- `bend_policy`: for bent routes, choose `"row-first"` or `"col-first"`
- `overlap_color`: optional color to write when two or more routed paths claim the same cell
- `include_endpoints`: whether the terminal cells themselves are included in the painted path

## Semantics

For each color, pair its two terminals and construct the path between them.

- If the terminals share a row or column, draw the straight inclusive segment.
- If they do not align and `allow_bends=False`, the route is invalid.
- If `allow_bends=True`, draw a single-bend Manhattan route according to the selected bend policy.
- If multiple paths use the same cell and `overlap_color` is set, recolor that cell with the overlap color.

## Why this primitive helps

Without a dedicated helper, ARC programs repeatedly have to re-implement the same low-level steps:

- group terminal cells by color
- choose a routing policy
- enumerate every cell on each segment
- decide what happens at overlaps
- preserve or drop endpoints

That bookkeeping is noisy but not conceptually interesting. A helper keeps the rule close to the task's real meaning: *connect the terminals*.

## Direct uses in this pack

- **E71** — connect aligned terminal pairs with straight segments
- **M71** — connect non-aligned pairs with command-selected row-first or column-first bends
- **H71** — route multiple pairs and recolor path overlaps
