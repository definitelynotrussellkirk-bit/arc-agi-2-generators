# New Primitive for Set 20: `pivot_rotate`

## Overview

This set introduces a rigid-rotation helper:

```text
pivot_rotate(cells, pivot, quarter_turns)
```

The idea is simple: you already know which cells belong to a motif and you already know
the pivot point. Instead of rebuilding a rotation from scratch in every rule, this helper
takes the whole coordinate set and rotates it as one rigid object around that pivot.

## Why this primitive is useful

Many ARC-style tasks are not about generic image-wide transforms. They are about **local
object motion around a marker**:

- rotate one motif around one dot
- rotate several motifs around separate pivots
- read a local command and rotate each attached object by a different amount

That pattern is common enough that a direct helper is cleaner than open-coding the
coordinate algebra every time.

## Suggested semantics

```python
pivot_rotate(cells, pivot, quarter_turns)
```

Where:

- `cells` is a list or set of `(row, col)` coordinates belonging to one object
- `pivot` is the `(row, col)` coordinate of the rotation center
- `quarter_turns` is an integer, usually interpreted modulo 4

A clockwise 90-degree step maps a relative offset `(dr, dc)` to `(dc, -dr)`.

## Reference behavior

Pseudo-logic:

```python
def pivot_rotate(cells, pivot, quarter_turns):
    pr, pc = pivot
    k = quarter_turns % 4
    out = []
    for r, c in cells:
        dr, dc = r - pr, c - pc
        if k == 0:
            nr, nc = pr + dr, pc + dc
        elif k == 1:
            nr, nc = pr + dc, pc - dr
        elif k == 2:
            nr, nc = pr - dr, pc - dc
        else:
            nr, nc = pr - dc, pc + dr
        out.append((nr, nc))
    return out
```

## Direct uses in this pack

- **E134 — Pivot Around the Dot**: one motif rotates once around one pivot.
- **M134 — Many Pivot Rotations**: several separate motifs each rotate around the nearest pivot.
- **H134 — Commanded Pivot Rotations**: each pivot group rotates by a locally encoded number of quarter turns.

## Relationship to earlier helpers

This primitive is different from helpers for docking, projection, or stamping.
Those move or replay objects in straight directions or at anchors. `pivot_rotate`
is specifically about **local rotational motion around an explicit center**.

## Failure modes it helps isolate

Using this helper makes it easier to separate:

- pivot detection errors
- wrong rotation direction
- wrong number of quarter turns
- incorrect component-to-pivot assignment
- regressions where a partial rule already has the right component but not the right transform
