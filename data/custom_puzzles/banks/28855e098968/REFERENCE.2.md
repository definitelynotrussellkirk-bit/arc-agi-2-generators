# New Primitive for Set 18: `offset_scatter`

## Overview

This set introduces an offset-cloud replay primitive:

```text
offset_scatter(offsets, anchors, paint_color=None, transforms=None, recolor=None, merge="overwrite|max|keep")
```

The idea is to represent a motif not as a dense rectangle, but as a **set of signed offsets** relative to an origin. Once you have that cloud of offsets, you can replay it around many anchors.

## Why this is useful

Many ARC-style tasks are easier to describe as:

1. detect a special origin,
2. record where the interesting cells lie relative to that origin,
3. replay those relative positions elsewhere,
4. optionally rotate or recolor each replay,
5. resolve overlaps.

A dense template helper often carries around a lot of irrelevant zeros. `offset_scatter` keeps only the meaningful relative geometry.

## Suggested signature

```python
offset_scatter(offsets, anchors, paint_color=None, transforms=None, recolor=None, merge="overwrite|max|keep")
```

Where:

- `offsets` is a list of relative `(dr, dc)` positions,
- `anchors` is a list of target locations, optionally with metadata such as anchor color,
- `paint_color` sets one fixed output color when no recoloring function is used,
- `transforms` optionally rotates each replay independently,
- `recolor` optionally computes a painted color per anchor or per offset,
- `merge` decides what happens when replays overlap.

## Semantics

### Plain replay

If the offsets are:

```text
[(0,1), (1,0), (1,1), (2,1)]
```

and the anchors are:

```text
[(6,8), (8,4)]
```

then two copies of that offset cloud are painted around `(6,8)` and `(8,4)`.

### With rotation

If a transform list is provided, each replay can be rotated independently before painting.

### With recoloring

A recolor callback can choose the painted color from the anchor metadata. This is what lets a single geometric cloud produce different colors at different destinations.

### With merge rules

When replays overlap:

- `overwrite` lets the latest paint win,
- `keep` preserves the earliest paint,
- `max` keeps the maximum color.

## Direct uses in this pack

- **E120 — Offset Cloud Replay**  
  Read a cloud once and replay it around every anchor.

- **M120 — Rotated Offset Replay**  
  Replay the cloud with per-anchor rotations.

- **H120 — Keyed Offset Merge**  
  Replay with both rotations and anchor-dependent recoloring, then max-merge overlaps.

## Minimal reference implementation

```python
def offset_scatter(canvas, offsets, anchors, paint_color=None, transforms=None, recolor=None, merge="overwrite"):
    out = clone(canvas)
    for i, anchor in enumerate(anchors):
        if len(anchor) == 2:
            ar, ac = anchor
            aval = None
        else:
            ar, ac, aval = anchor
        t = transforms[i] if transforms is not None else 0
        for dr, dc in offsets:
            rr, cc = rotate_offset(dr, dc, t)
            r, c = ar + rr, ac + cc
            if not in_bounds(out, r, c):
                continue
            nv = paint_color if recolor is None else recolor(aval, i, (dr, dc), (rr, cc))
            paint(out, r, c, nv, merge=merge)
    return out
```

## What makes it new relative to earlier helpers

Earlier helpers in the series focused on dense templates, anchors, rays, or chamber logic. `offset_scatter` treats a pattern as a sparse geometric cloud, which makes command-conditioned replay tasks much more natural.
