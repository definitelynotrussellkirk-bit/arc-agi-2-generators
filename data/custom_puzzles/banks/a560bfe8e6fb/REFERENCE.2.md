# Invented Primitive for Set 4 — `project_rays`

This pack adds a new helper primitive intended for solver-side DSLs and repair loops:

```text
project_rays(grid, starts, directions, stop_colors=None, stop_nonzero=False, paint='source')
```

## What it does

Starting from one or more source cells, march step by step in each requested direction and paint cells until a stop condition fires.

Typical uses:
- boundary-only projection
- projection until a frame or wall
- projection with source-color painting
- projection followed by overlap resolution

## Suggested semantics

- `grid`: the original grid
- `starts`: list of `(row, col)` source coordinates
- `directions`: for example the four cardinals
- `stop_colors`: optional set of colors that stop the ray before painting that cell
- `stop_nonzero`: if true, any nonzero cell blocks the ray
- `paint='source'`: use the source cell's color
- `paint=<int>`: use a fixed paint color instead

## Why this helper is useful

A lot of ARC tasks want “extend a line from here until something stops it.” In raw cell-by-cell code this is awkward and repetitive, especially inside a write→test→repair loop. Packaging it as one primitive makes projection tasks shorter, easier to patch, and less error-prone.

## Puzzles in this set that use it directly

- `E22 — Beacon Cross Rays`
- `M25 — Chamber Rays`
- `H25 — Ray Clash Grid`

## Reference Python implementation

```python
def project_rays(base_grid, starts, directions=DIR4, *, stop_colors=None, stop_nonzero=False, paint='source', respect_original_nonzero=True):
    g = clone(base_grid)
    h, w = size(base_grid)
    stop_colors = set(stop_colors or [])
    for r, c in starts:
        src = base_grid[r][c]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < h and 0 <= nc < w:
                v = base_grid[nr][nc]
                if (stop_nonzero and v != 0) or (v in stop_colors):
                    break
                if not (respect_original_nonzero and v != 0):
                    g[nr][nc] = src if paint == 'source' else paint
                nr += dr
                nc += dc
    return g
```
