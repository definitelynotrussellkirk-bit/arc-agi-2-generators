# New Primitive for Set 22: `span_markers`

## Overview

This set introduces a reusable interval helper:

```text
span_markers(markers)
```

Given two matching markers on the same row or the same column, the primitive returns every grid cell on the closed axis-aligned segment between them, including both endpoints.

## Why this is useful

A surprising number of ARC tasks hide a full structure behind only a sparse pair of anchors. Without a named helper, every solver has to repeat the same low-level work:

- check whether the anchors share a row or a column,
- compute the inclusive coordinate interval,
- emit all cells in that interval,
- then separately reason about overlaps or later compositions.

`span_markers` makes that pattern explicit. It is small, deterministic, and composable with other helpers.

## Suggested signature

```python
span_markers(markers)
```

Where `markers` is a two-element collection of coordinates such as `[(r1, c1), (r2, c2)]`.

## Semantics

- If the markers share a row, return all cells from the left marker to the right marker.
- If the markers share a column, return all cells from the upper marker to the lower marker.
- The result is inclusive of the endpoints.
- Non-axis-aligned marker pairs are invalid for this primitive.

## Direct uses in this pack

- **E148 — Complete the Axis Span**  
  The whole task is exactly one interval recovery from a matched marker pair.

- **M152 — Span Overlay with Crossings**  
  Multiple colored marker pairs each become a span before the solver reasons about overlaps.

- **H152 — Overlap Count of Multiple Spans**  
  The primitive is reused, but the output now depends only on the coverage count induced by many spans.

## Minimal reference implementation

```python
def span_markers(markers):
    markers=list(markers)
    if len(markers)!=2: raise ValueError(markers)
    (r1,c1),(r2,c2)=markers
    cells=[]
    if r1==r2:
        a,b=sorted([c1,c2]); cells=[(r1,c) for c in range(a,b+1)]
    elif c1==c2:
        a,b=sorted([r1,r2]); cells=[(r,c1) for r in range(a,b+1)]
    else:
        raise ValueError("not axis-aligned")
    return cells
```