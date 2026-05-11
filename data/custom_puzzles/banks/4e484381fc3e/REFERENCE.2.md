# New Primitive for Set 13 — `sprout_kernel`

```text
sprout_kernel(seed_cells, offsets, color_lookup=None, allowed=None, priority=None)
```

## Purpose

`sprout_kernel` is a compact helper for puzzles where one or more seed cells expand into a local motif. It supports three things that recur in ARC-style tasks:

1. applying the same relative offset pattern around many seeds,
2. clipping the expansion to an allowed region, and
3. resolving overlaps by priority rather than paint order.

It is used directly in **E85**, **M85**, and **H85**.

## Contract

- `seed_cells`: iterable of `(row, col, color)` tuples
- `offsets`: iterable of relative offsets `(dr, dc)` to paint around each seed
- `color_lookup`: optional function mapping a seed tuple to the color that should be painted
- `allowed`: optional set of cells that are legal paint targets
- `priority`: optional dict `color -> rank`, where lower rank wins collisions

## Return value

A dictionary:

```python
{(row, col): color, ...}
```

representing the final painted cells after clipping and collision resolution.

## Why it helps

Many solver sketches need something more expressive than a single-cell local rewrite but lighter than full template extraction. `sprout_kernel` covers a useful middle ground:

- plus and X expansions,
- frame-clipped local growth,
- seeded blooms with overlap precedence,
- staged solving where a model first identifies seeds, then learns the kernel.

## Example

```python
seeds = [(3, 3, 6), (5, 5, 4)]
offsets = [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
painted = sprout_kernel(seeds, offsets)
```

This paints two plus shapes, inheriting each seed's color.
