# New Primitive for Set 21: `phase_weave`

## Signature

```python
phase_weave(anchor, directions, palette, h, w, mask=None, include_anchor=False)
```

## Intuition

`phase_weave` walks outward from an anchor one step at a time along each
requested direction and paints cells using a repeating palette. It is meant
to capture tasks where the real work is not “find a shape” or “copy a block,”
but “emit a periodic signal from a seed,” optionally clipped by a chamber,
frame interior, or other allowed mask.

At distance 1 from the anchor it uses `palette[0]`, at distance 2 it uses
`palette[1]`, and so on, wrapping around when the palette ends.

## Parameters

- `anchor`: `(row, col)` origin cell
- `directions`: iterable of direction vectors such as `DIR4` or `DIR8`
- `palette`: ordered list of colors to cycle through
- `h, w`: grid bounds
- `mask`: optional set of allowed cells. If present, weaving stops when a
  step would leave the mask.
- `include_anchor`: whether to emit a colored anchor cell too

## Why it is useful

Many ARC tasks involve propagation with rhythm:

- alternating-color rays
- room-limited beams
- diagonal and cardinal “starbursts”
- repeated color phases controlled by a legend

Without a primitive like this, the solver often needs repetitive low-level
loops that obscure the actual rule.

## Used directly in this pack

- `E141 — Alternating Seed Rays`
- `M141 — Room-Limited Weave`
- `H141 — Eight-Way Room Weave`

## Reference implementation

```python
def phase_weave(anchor, directions, palette, h, w, mask=None, include_anchor=False):
    out = []
    if include_anchor:
        out.append((anchor[0], anchor[1], palette[0]))
    for dr, dc in directions:
        step = 1
        r, c = anchor[0] + dr, anchor[1] + dc
        while 0 <= r < h and 0 <= c < w and (mask is None or (r, c) in mask):
            out.append((r, c, palette[(step - 1) % len(palette)]))
            step += 1
            r += dr
            c += dc
    return out
```

## Solver-style reading

In a `rule!`-style setting, `phase_weave` should be thought of as a compact
way to say:

1. identify an origin cell,
2. identify a sequence of colors,
3. identify which directions to emit along,
4. stop at borders or chamber boundaries,
5. write the color determined by the phase index.
