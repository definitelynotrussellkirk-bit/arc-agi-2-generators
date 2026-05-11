# New Primitive Spec — `reflect_across_guide`

```python
reflect_across_guide(base_grid, cells, axis, guide_pos, keep_original=True, overlap_color=None)
```

Purpose: reflect colored cells across a detected horizontal or vertical guide line. The primitive can preserve the original cells while painting their reflected counterparts, which makes it useful for one-sided mirror tasks and multi-axis symmetry composition.

Arguments:

- `base_grid`: the canvas to paint on
- `cells`: iterable of `(row, col, color)` triples to reflect
- `axis`: `'h'` for a horizontal guide row or `'v'` for a vertical guide column
- `guide_pos`: row index or column index of the guide
- `keep_original`: whether the source cells remain after reflection
- `overlap_color`: optional recolor for landing on an occupied non-guide cell

Why it matters: ARC-style tasks often encode symmetry with an explicit divider. Making that divider a first-class primitive is much cleaner than rebuilding reflection arithmetic from scratch inside every rule.

Used in this set: **E50**, **M50**, and **H50**.