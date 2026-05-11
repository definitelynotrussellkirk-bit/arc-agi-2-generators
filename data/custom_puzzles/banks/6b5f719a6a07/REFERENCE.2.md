# New Primitive Spec — `stamp_template`

## Signature

```text
stamp_template(grid, anchors, template, center=None, substitute=None, respect_original_nonzero=True, keep_anchor=True)
```

## Intuition

`stamp_template` takes a small local motif and replays it around one or more anchor cells.
It is meant for ARC tasks where the input contains either:

- a literal exemplar motif that should be copied elsewhere, or
- a motif with one variable token whose color should be supplied by the anchor.

This lets you express "broadcast this local pattern" rules without manually rewriting
offset logic every time.

## Parameters

- `grid`: the base grid to read from and paint onto
- `anchors`: iterable of `(r, c)` or `(r, c, anchor_color)` items
- `template`: a small 2D grid; zero means transparent
- `center`: which template cell aligns with the anchor; defaults to the geometric center
- `substitute`: optional dictionary mapping template values to replacement values
  - use `'anchor'` to substitute the current anchor's color
- `respect_original_nonzero`: if true, do not overwrite existing nonzero cells in the base grid
- `keep_anchor`: if true, preserve the original anchor cell

## Typical Use Cases

### 1. Fixed motif replay
Copy the same 3×3 pattern around several anchors.

### 2. Anchor-colored substitution
Use a token like `9` inside the template to mean "paint this part with the anchor's color."

### 3. Border-clipped local stamping
Because stamping is coordinate-based, motifs naturally clip at grid borders.

## Examples In Set 5

- `E29` — diagonal halo around each anchor
- `M34` — replay the top-left 3×3 exemplar at every other anchor
- `H34` — replay a motif while substituting the token `9` with each anchor color

## Minimal Example

```python
template = [
    [7, 0, 7],
    [0, 0, 0],
    [7, 0, 7],
]
anchors = [(3, 4), (6, 7)]
out = stamp_template(grid, anchors, template, center=(1, 1), keep_anchor=True)
```

This stamps four diagonal `7`s around each anchor while preserving the anchors themselves.
