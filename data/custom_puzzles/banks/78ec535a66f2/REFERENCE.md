# ARC-style Puzzle Bank: 21 More Tasks (Seventh Batch)

This seventh batch pushes harder into precedence, parity, symmetry selection,
extraction, control-token composition, pathfinding, and shape comparison.
It is meant to feel more heterogeneous in *reasoning style*, not just in surface appearance.

## New helper primitives highlighted in this batch

- `priority_overlay` — Resolve conflicting paint proposals by an explicit precedence order instead of simple last-write-wins.
- `apply_script` — Apply an ordered sequence of discrete shape transforms encoded by control tokens.
- `pack_gallery` — Pack cropped shapes into a fresh canvas with fixed black gaps and a chosen vertical alignment.
- `center_in_frame` — Compute the top-left placement that centers a cropped shape inside a rectangular outline frame.
- `normalize_pair` — Crop two shapes, align their top-left corners inside a common canvas, and compare them cellwise.
- `bfs_path` — Find a shortest orthogonal path through allowed cells.

## Index

- `easy_g01` — **Keep only the topmost nonzero in each column** (easy; same_size, columns, filter, projection)
- `easy_g02` — **Recolor each object by its size** (easy; same_size, objects, counting, recolor)
- `easy_g03` — **Row majority wins** (easy; same_size, rows, frequency, recolor)
- `easy_g04` — **Keep cells on the anchor parity** (easy; same_size, parity, filter, global)
- `easy_g05` — **Each filled 2x2 block becomes its main diagonal** (easy; same_size, local, blocks, shape_rewrite)
- `easy_g06` — **Shift the object one step toward the border marker** (easy; same_size, marker_control, translation, objects)
- `easy_g07` — **Horizontal triples turn vertical** (easy; same_size, local, rotation, runs)
- `medium_g08` — **Border emitters cast inward with precedence** (medium; same_size, rays, precedence, blockers; primitives: priority_overlay)
- `medium_g09` — **Recolor each object by the nearest corner marker** (medium; same_size, objects, position, assignment)
- `medium_g10` — **Keep only the 180-degree symmetric object** (medium; same_size, objects, symmetry, filter)
- `medium_g11` — **Convert object sizes into a bar chart** (medium; output_resize, objects, counting, chart; primitives: pack_gallery)
- `medium_g12` — **Transform the object according to the key color** (medium; output_resize, marker_control, transforms, objects; primitives: apply_transform)
- `medium_g13` — **Fill each bounding box with a checkerboard** (medium; same_size, objects, bounding_box, pattern_fill)
- `medium_g14` — **Pack the objects into one centered row** (medium; output_resize, objects, relayout, packing; primitives: pack_gallery)
- `hard_g15` — **Place objects into frames by size rank** (hard; same_size, objects, frames, assignment; primitives: center_in_frame)
- `hard_g16` — **Apply a whole script of transforms** (hard; output_resize, script, transforms, composition; primitives: apply_script, apply_transform)
- `hard_g17` — **Legend-controlled precedence rays** (hard; output_resize, rays, precedence, legend; primitives: priority_overlay)
- `hard_g18` — **Route the shortest path between the terminals** (hard; same_size, pathfinding, blockers, simulation; primitives: bfs_path)
- `hard_g19` — **Align two objects and keep only the XOR shape** (hard; output_resize, objects, comparison, xor; primitives: normalize_pair)
- `hard_g20` — **Transform each object by its nearest control token and pack the results** (hard; output_resize, objects, marker_control, relayout; primitives: apply_transform, pack_gallery)
- `hard_g21` — **Make a four-quadrant transform mosaic from the corner keys** (hard; output_resize, mosaic, transforms, marker_control; primitives: apply_transform, pack_gallery)

## easy_g01 — Keep only the topmost nonzero in each column

**Difficulty:** easy

**Tags:** same_size, columns, filter, projection

**Written solution:**

For each column independently, keep only the topmost nonzero cell in that column and erase every nonzero cell below it. Background stays black(0).

**Program solution:**

```python
def solve_g_g01_topmost_per_column(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        for r in range(h):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                break
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    4,
    0
  ],
  [
    5,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    7,
    8,
    0,
    0,
    9
  ],
  [
    1,
    0,
    0,
    0,
    4,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    4,
    0
  ],
  [
    5,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    9
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    0,
    4,
    0,
    0,
    0
  ],
  [
    2,
    0,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    5,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    0,
    0,
    8
  ],
  [
    9,
    0,
    0,
    1,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    0,
    4,
    0,
    0,
    0
  ],
  [
    2,
    0,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    5,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    0,
    0,
    8
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    1,
    0,
    0,
    2
  ],
  [
    3,
    0,
    4,
    0,
    0
  ],
  [
    0,
    5,
    0,
    6,
    0
  ],
  [
    7,
    0,
    8,
    0,
    9
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    1,
    0,
    0,
    2
  ],
  [
    3,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    1,
    0,
    0
  ],
  [
    2,
    0,
    3,
    0,
    4,
    0
  ],
  [
    0,
    5,
    0,
    0,
    0,
    6
  ],
  [
    7,
    0,
    8,
    9,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    4,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    1,
    0,
    0
  ],
  [
    2,
    0,
    3,
    0,
    4,
    0
  ],
  [
    0,
    5,
    0,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```


## easy_g02 — Recolor each object by its size

**Difficulty:** easy

**Tags:** same_size, objects, counting, recolor

**Written solution:**

Find each orthogonally connected nonzero object. Recolor every size-1 object to red(2), every size-2 object to yellow(4), every size-3 object to magenta(6), and any larger object to cyan(8). Keep each object’s shape.

**Program solution:**

```python
def solve_g_g02_recolor_by_size(g):
    out=blank(*dims(g))
    color_map={1:2,2:4,3:6}
    for comp in components(g):
        sz=len(comp['cells'])
        col=color_map.get(sz,8)
        for r,c in comp['cells']:
            out[r][c]=col
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    3,
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    5
  ],
  [
    0,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    2
  ],
  [
    0,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    8,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    9,
    9,
    9,
    0,
    1,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    2,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    6,
    6,
    6,
    0,
    2,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    3
  ],
  [
    4,
    4,
    0,
    5,
    0
  ],
  [
    0,
    0,
    0,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    2
  ],
  [
    4,
    4,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    6,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    2,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    4,
    0,
    0,
    0,
    5
  ],
  [
    0,
    4,
    4,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    4,
    4,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    6,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0,
    2
  ],
  [
    0,
    6,
    6,
    0,
    0,
    0
  ]
]
```


## easy_g03 — Row majority wins

**Difficulty:** easy

**Tags:** same_size, rows, frequency, recolor

**Written solution:**

Treat each row independently. In a row that contains nonzero cells, find the most frequent nonzero color in that row and recolor every nonzero cell in that row to that color. Zeros remain zero. There are no ties.

**Program solution:**

```python
def solve_g_g03_row_majority_wins(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        nz=[v for v in row if v!=0]
        if not nz:
            continue
        cnt=Counter(nz)
        major=cnt.most_common(1)[0][0]
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=major
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    0,
    2,
    3,
    0,
    0
  ],
  [
    4,
    4,
    0,
    4,
    5,
    0
  ],
  [
    0,
    6,
    7,
    7,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    0,
    2,
    2,
    0,
    0
  ],
  [
    4,
    4,
    0,
    4,
    4,
    0
  ],
  [
    0,
    7,
    7,
    7,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    1,
    1,
    0,
    2,
    0
  ],
  [
    0,
    3,
    3,
    3,
    4
  ],
  [
    5,
    0,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    1,
    1,
    0,
    1,
    0
  ],
  [
    0,
    3,
    3,
    3,
    3
  ],
  [
    6,
    0,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    8,
    9,
    8,
    0,
    0
  ],
  [
    7,
    0,
    7,
    7,
    6,
    0
  ],
  [
    0,
    5,
    0,
    0,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    8,
    8,
    8,
    0,
    0
  ],
  [
    7,
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    5,
    0,
    0,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    2,
    2,
    3,
    0,
    0
  ],
  [
    4,
    0,
    4,
    5,
    4,
    0
  ],
  [
    0,
    6,
    0,
    6,
    7,
    6
  ],
  [
    8,
    8,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    2,
    2,
    2,
    0,
    0
  ],
  [
    4,
    0,
    4,
    4,
    4,
    0
  ],
  [
    0,
    6,
    0,
    6,
    6,
    6
  ],
  [
    8,
    8,
    0,
    0,
    0,
    0
  ]
]
```


## easy_g04 — Keep cells on the anchor parity

**Difficulty:** easy

**Tags:** same_size, parity, filter, global

**Written solution:**

There is exactly one gray(5) anchor cell. Keep every nonzero cell whose checkerboard parity matches the anchor, meaning `(row+col) mod 2` is the same as the anchor’s. Erase all other nonzero cells. The anchor itself stays.

**Program solution:**

```python
def solve_g_g04_anchor_parity_filter(g):
    h,w=dims(g)
    anchor=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                anchor=(r,c)
                break
        if anchor: break
    assert anchor is not None
    p=(anchor[0]+anchor[1])%2
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r+c)%2==p:
                out[r][c]=g[r][c]
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    2,
    0,
    3,
    0
  ],
  [
    4,
    0,
    0,
    6,
    0,
    7
  ],
  [
    0,
    8,
    9,
    0,
    1,
    0
  ],
  [
    2,
    0,
    3,
    4,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    0,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    8,
    0,
    0,
    0,
    0
  ],
  [
    2,
    0,
    3,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    5,
    2,
    0
  ],
  [
    0,
    3,
    0,
    0,
    4
  ],
  [
    6,
    0,
    7,
    0,
    0
  ],
  [
    0,
    8,
    0,
    9,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    5,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0
  ],
  [
    6,
    0,
    7,
    0,
    0
  ],
  [
    0,
    8,
    0,
    9,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    1,
    0,
    2,
    0
  ],
  [
    3,
    0,
    0,
    5,
    0,
    4
  ],
  [
    0,
    6,
    7,
    0,
    8,
    0
  ],
  [
    9,
    0,
    0,
    1,
    0,
    2
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    1,
    0,
    2,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0,
    4
  ],
  [
    0,
    0,
    7,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    1,
    0,
    2
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    1,
    2,
    0
  ],
  [
    3,
    0,
    4,
    0,
    6
  ],
  [
    0,
    7,
    0,
    8,
    0
  ],
  [
    9,
    0,
    1,
    0,
    2
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    0,
    2,
    0
  ],
  [
    3,
    0,
    4,
    0,
    6
  ],
  [
    0,
    7,
    0,
    8,
    0
  ],
  [
    9,
    0,
    1,
    0,
    2
  ]
]
```


## easy_g05 — Each filled 2x2 block becomes its main diagonal

**Difficulty:** easy

**Tags:** same_size, local, blocks, shape_rewrite

**Written solution:**

Every solid monochrome 2x2 square is rewritten as the main diagonal of that square: keep the top-left and bottom-right cells, and erase the other two cells. Any nonzero cells that are not part of such a square stay unchanged.

**Program solution:**

```python
def solve_g_g05_block_to_main_diagonal(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
                out[r+1][c+1]=vals[0]
                used.update({(r,c),(r,c+1),(r+1,c),(r+1,c+1)})
    # preserve any other nonzero cells not part of a block? probably none, but keep unchanged
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in used:
                out[r][c]=g[r][c]
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    2,
    0,
    3,
    3
  ],
  [
    0,
    2,
    2,
    0,
    3,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    4,
    4,
    0,
    5,
    5,
    0
  ],
  [
    4,
    4,
    0,
    5,
    5,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    5,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    6,
    6,
    0,
    0,
    0
  ],
  [
    6,
    6,
    0,
    7,
    7
  ],
  [
    0,
    0,
    0,
    7,
    7
  ],
  [
    0,
    8,
    8,
    0,
    0
  ],
  [
    0,
    8,
    8,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7
  ],
  [
    0,
    8,
    0,
    0,
    0
  ],
  [
    0,
    0,
    8,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    9,
    9,
    0,
    0
  ],
  [
    1,
    1,
    9,
    9,
    0,
    0
  ],
  [
    1,
    1,
    0,
    0,
    2,
    2
  ],
  [
    0,
    0,
    0,
    0,
    2,
    2
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    9,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    9,
    0,
    0
  ],
  [
    0,
    1,
    0,
    0,
    2,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    2
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
    3,
    0,
    4,
    4
  ],
  [
    0,
    0,
    0,
    0,
    4,
    4
  ],
  [
    5,
    5,
    0,
    6,
    6,
    0
  ],
  [
    5,
    5,
    0,
    6,
    6,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    3,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    3,
    0,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    4
  ],
  [
    5,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    5,
    0,
    0,
    6,
    0
  ]
]
```


## easy_g06 — Shift the object one step toward the border marker

**Difficulty:** easy

**Tags:** same_size, marker_control, translation, objects

**Written solution:**

There is one border marker colored maroon(9) and one other object. Remove the marker and shift the entire object by exactly one cell toward that marker’s side: up for a top-edge marker, down for a bottom-edge marker, left for a left-edge marker, and right for a right-edge marker.

**Program solution:**

```python
def solve_g_g06_shift_object_toward_marker(g):
    h,w=dims(g)
    marker=None
    out=blank(h,w)
    obj_cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                marker=(r,c)
            elif g[r][c]!=0:
                obj_cells.append((r,c,g[r][c]))
    assert marker is not None
    if marker[0]==0: dr,dc=-1,0
    elif marker[0]==h-1: dr,dc=1,0
    elif marker[1]==0: dr,dc=0,-1
    else: dr,dc=0,1
    for r,c,v in obj_cells:
        nr,nc=r+dr,c+dc
        out[nr][nc]=v
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    9,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    0
  ],
  [
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    0
  ],
  [
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    9,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    9
  ],
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```


## easy_g07 — Horizontal triples turn vertical

**Difficulty:** easy

**Tags:** same_size, local, rotation, runs

**Written solution:**

Whenever three same-colored cells form a horizontal run of length 3, replace that run by a vertical run of length 3 through the same middle cell. Other nonzero cells stay unchanged.

**Program solution:**

```python
def solve_g_g07_horizontal3_to_vertical3(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h):
        for c in range(w-2):
            v=g[r][c]
            if v!=0 and g[r][c+1]==v and g[r][c+2]==v:
                if 0<r<h-1:
                    out[r-1][c+1]=v
                    out[r][c+1]=v
                    out[r+1][c+1]=v
                    used.update({(r,c),(r,c+1),(r,c+2)})
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in used:
                out[r][c]=g[r][c]
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    3,
    3,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    3,
    0,
    0
  ],
  [
    0,
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    0,
    3,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    4,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    4,
    5,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
    8,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    9,
    9,
    9
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    8,
    0,
    0,
    0
  ],
  [
    0,
    0,
    8,
    0,
    0,
    0
  ],
  [
    0,
    0,
    8,
    0,
    9,
    0
  ],
  [
    0,
    0,
    0,
    0,
    9,
    0
  ],
  [
    0,
    0,
    0,
    0,
    9,
    0
  ]
]
```


## medium_g08 — Border emitters cast inward with precedence

**Difficulty:** medium

**Tags:** same_size, rays, precedence, blockers

**Uses new primitive(s):** priority_overlay

**Written solution:**

Every nonzero, non-gray border cell is an emitter. Emitters on the top and bottom borders cast straight rays inward along their columns; emitters on the left and right borders cast straight rays inward along their rows. Gray(5) cells block rays and stay gray. When multiple rays want the same cell, keep the higher-priority color, which here is simply the larger color number.

**Program solution:**

```python
def solve_g_g08_border_rays_precedence(g):
    h,w=dims(g)
    blockers={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5}
    emitters=[]
    for c in range(w):
        if g[0][c] not in (0,5): emitters.append((0,c,g[0][c],'down'))
        if g[h-1][c] not in (0,5): emitters.append((h-1,c,g[h-1][c],'up'))
    for r in range(1,h-1):
        if g[r][0] not in (0,5): emitters.append((r,0,g[r][0],'right'))
        if g[r][w-1] not in (0,5): emitters.append((r,w-1,g[r][w-1],'left'))
    out=blank(h,w)
    # keep blockers and emitters
    for r,c in blockers: out[r][c]=5
    proposals=[]
    for r,c,color,dirn in emitters:
        out[r][c]=color
        dr,dc={'down':(1,0),'up':(-1,0),'right':(0,1),'left':(0,-1)}[dirn]
        nr,nc=r+dr,c+dc
        while 0<=nr<h and 0<=nc<w and g[nr][nc]!=5:
            proposals.append((nr,nc,color))
            nr+=dr; nc+=dc
    over=priority_overlay(h,w,proposals,precedence=[1,2,3,4,6,7,8,9])
    for r in range(h):
        for c in range(w):
            if over[r][c]!=0 and out[r][c]==0:
                out[r][c]=over[r][c]
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    2,
    0,
    0,
    0,
    0
  ],
  [
    3,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    7,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    2,
    0,
    7,
    0,
    0
  ],
  [
    3,
    3,
    3,
    7,
    3,
    3
  ],
  [
    0,
    2,
    5,
    7,
    4,
    4
  ],
  [
    0,
    2,
    0,
    7,
    0,
    0
  ],
  [
    0,
    2,
    0,
    7,
    0,
    0
  ],
  [
    0,
    2,
    0,
    7,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    8,
    0,
    0
  ],
  [
    1,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    2
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    3,
    8,
    0,
    0
  ],
  [
    1,
    3,
    8,
    1,
    1
  ],
  [
    0,
    3,
    5,
    2,
    2
  ],
  [
    0,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0,
    0,
    2
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    5,
    2,
    2,
    2
  ],
  [
    0,
    4,
    0,
    6,
    0,
    0,
    0
  ],
  [
    7,
    7,
    7,
    7,
    7,
    7,
    7
  ],
  [
    0,
    4,
    0,
    6,
    5,
    0,
    0
  ],
  [
    0,
    4,
    0,
    6,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    3,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    2,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    3,
    2,
    0,
    0
  ],
  [
    4,
    4,
    4,
    4,
    4,
    4
  ],
  [
    0,
    0,
    5,
    6,
    6,
    6
  ],
  [
    0,
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    2,
    0,
    0
  ]
]
```


## medium_g09 — Recolor each object by the nearest corner marker

**Difficulty:** medium

**Tags:** same_size, objects, position, assignment

**Written solution:**

The four corners are fixed marker colors. For each other connected object, measure the center of its bounding box and recolor the entire object to the color of the nearest corner marker by Manhattan distance. Corner markers stay as they are.

**Program solution:**

```python
def solve_g_g09_recolor_by_nearest_corner(g):
    h,w=dims(g)
    corners={(0,0):g[0][0], (0,w-1):g[0][w-1], (h-1,0):g[h-1][0], (h-1,w-1):g[h-1][w-1]}
    out=blank(h,w)
    for (r,c),v in corners.items():
        out[r][c]=v
    corner_positions=list(corners.keys())
    for comp in components(g, exclude=[]):
        # exclude corner markers as singleton objects if at corners
        if all((r,c) in corners for r,c in comp['cells']) and len(comp['cells'])==1:
            continue
        ctr=center_of_bbox(comp)
        best=min(corner_positions, key=lambda p: manhattan(ctr,p))
        color=corners[best]
        for r,c in comp['cells']:
            out[r][c]=color
    return out
```

**Train 1 — Input**

```json
[
  [
    1,
    0,
    0,
    0,
    0,
    2
  ],
  [
    0,
    0,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    0,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    3,
    0,
    0,
    0,
    0,
    4
  ]
]
```

**Train 1 — Output**

```json
[
  [
    1,
    0,
    0,
    0,
    0,
    2
  ],
  [
    0,
    0,
    1,
    1,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    3,
    0,
    0,
    0,
    0,
    4
  ]
]
```

**Train 2 — Input**

```json
[
  [
    5,
    0,
    0,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    8,
    0
  ],
  [
    9,
    0,
    0,
    0,
    0,
    1
  ]
]
```

**Train 2 — Output**

```json
[
  [
    5,
    0,
    0,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    1,
    0
  ],
  [
    0,
    0,
    0,
    0,
    1,
    0
  ],
  [
    9,
    0,
    0,
    0,
    0,
    1
  ]
]
```

**Train 3 — Input**

```json
[
  [
    2,
    0,
    0,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    5
  ]
]
```

**Train 3 — Output**

```json
[
  [
    2,
    0,
    0,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    5
  ]
]
```

**Test 1 — Input**

```json
[
  [
    1,
    0,
    0,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    7
  ],
  [
    2,
    0,
    0,
    0,
    0,
    3
  ]
]
```

**Test 1 — Output**

```json
[
  [
    1,
    0,
    0,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    1,
    1,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    3,
    3
  ],
  [
    2,
    0,
    0,
    0,
    0,
    3
  ]
]
```


## medium_g10 — Keep only the 180-degree symmetric object

**Difficulty:** medium

**Tags:** same_size, objects, symmetry, filter

**Written solution:**

Among all connected objects, exactly one has a cropped shape that looks the same after a 180-degree rotation. Keep that object unchanged and erase all others.

**Program solution:**

```python
def solve_g_g10_keep_180_symmetric_object(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        shape,_=object_shape(comp)
        if shape_equal_under_180(shape):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    2,
    2,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    4,
    4,
    0
  ],
  [
    0,
    0,
    5,
    5,
    0,
    4,
    0
  ],
  [
    0,
    0,
    5,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    7
  ],
  [
    0,
    8,
    8,
    0,
    0,
    7
  ],
  [
    0,
    8,
    8,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    7
  ],
  [
    0,
    8,
    8,
    0,
    0,
    7
  ],
  [
    0,
    8,
    8,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    9,
    9,
    0,
    0,
    1,
    0
  ],
  [
    9,
    0,
    0,
    0,
    1,
    1
  ],
  [
    0,
    0,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    3,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    3,
    0,
    4,
    4,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    0,
    6,
    6,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```


## medium_g11 — Convert object sizes into a bar chart

**Difficulty:** medium

**Tags:** output_resize, objects, counting, chart

**Uses new primitive(s):** pack_gallery

**Written solution:**

Read the connected objects from left to right. Output a bottom-aligned bar chart with one colored column per object, separated by one black column. Each bar’s height equals the number of cells in that object, and each bar keeps the object’s color.

**Program solution:**

```python
def solve_g_g11_bar_chart_sizes(g):
    comps=sorted(components(g), key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    sizes=[len(comp['cells']) for comp in comps]
    colors=[comp['color'] for comp in comps]
    H=max(sizes) if sizes else 1
    W=max(1, 2*len(comps)-1)
    out=blank(H,W)
    for i,(sz,col) in enumerate(zip(sizes,colors)):
        c=2*i
        for r in range(H-sz,H):
            out[r][c]=col
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    0,
    3,
    3,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    3,
    0,
    4
  ],
  [
    2,
    0,
    3,
    0,
    4
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    5,
    0,
    0,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    7,
    7,
    0,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    7,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    7,
    0,
    5,
    0,
    6,
    0,
    8
  ]
]
```

**Train 3 — Input**

```json
[
  [
    9,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    1,
    1,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    2,
    2,
    2,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    1
  ],
  [
    9,
    0,
    2,
    0,
    1
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    3,
    0,
    0,
    0,
    4
  ],
  [
    2,
    2,
    0,
    3,
    0,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    5,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    2,
    0,
    3,
    0,
    5,
    0,
    4
  ],
  [
    2,
    0,
    3,
    0,
    5,
    0,
    4
  ]
]
```


## medium_g12 — Transform the object according to the key color

**Difficulty:** medium

**Tags:** output_resize, marker_control, transforms, objects

**Uses new primitive(s):** apply_transform

**Written solution:**

There is one key cell colored 1, 2, 3, or 4. Remove the key and crop the remaining object tightly. Then apply the matching transform: 1 = rotate 90° clockwise, 2 = rotate 180°, 3 = mirror left-right, 4 = transpose across the main diagonal.

**Program solution:**

```python
def solve_g_g12_transform_by_key(g):
    # one key cell in top row, object elsewhere
    h,w=dims(g)
    key=None
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4):
            key=v; key_pos=(0,c); break
    if key is None:
        for r in range(h):
            for c,v in enumerate(g[r]):
                if v in (1,2,3,4):
                    key=v; key_pos=(r,c); break
            if key is not None: break
    assert key is not None
    temp=copy_grid(g); temp[key_pos[0]][key_pos[1]]=0
    shape=crop_nonzero(temp)
    return apply_transform(shape,key)
```

**Train 1 — Input**

```json
[
  [
    0,
    1,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    6,
    6
  ],
  [
    6,
    0
  ],
  [
    6,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    8,
    0
  ],
  [
    0,
    0,
    7,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    8,
    0,
    7,
    0
  ],
  [
    8,
    0,
    7,
    0
  ],
  [
    0,
    0,
    7,
    7
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    9,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    9,
    9
  ],
  [
    0,
    9,
    0
  ],
  [
    9,
    9,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    4,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    6,
    6,
    0
  ],
  [
    0,
    6,
    6
  ]
]
```


## medium_g13 — Fill each bounding box with a checkerboard

**Difficulty:** medium

**Tags:** same_size, objects, bounding_box, pattern_fill

**Written solution:**

For each connected monochrome object, find its bounding box. Replace that object by the full bounding box filled in a checkerboard pattern of its color and black(0), starting with the object’s color at the top-left corner of the box.

**Program solution:**

```python
def solve_g_g13_checkerfill_bboxes(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        r0,c0,r1,c1=bbox(comp['cells'])
        col=comp['color']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if (r-r0 + c-c0)%2==0:
                    out[r][c]=col
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    3,
    0
  ],
  [
    0,
    2,
    2,
    0,
    3,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    5,
    0,
    0,
    0,
    0
  ],
  [
    5,
    5,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    6,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    5,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    0,
    7,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    8,
    8
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    8
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    0,
    9,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    1,
    0
  ],
  [
    0,
    0,
    0,
    0,
    1,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    0,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    1,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```


## medium_g14 — Pack the objects into one centered row

**Difficulty:** medium

**Tags:** output_resize, objects, relayout, packing

**Uses new primitive(s):** pack_gallery

**Written solution:**

Crop each connected object tightly, preserve the objects’ left-to-right order from the input, and pack the cropped objects into a single row with one black column between neighboring objects. Vertically center the objects inside the new output.

**Program solution:**

```python
def solve_g_g14_pack_objects_row(g):
    comps=sorted(components(g), key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    shapes=[object_shape(comp)[0] for comp in comps]
    return pack_gallery(shapes, gap=1, align='center')
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    2,
    2,
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    5,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    2,
    2,
    0,
    4,
    0,
    5,
    5,
    0,
    3,
    0
  ],
  [
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    3,
    3
  ]
]
```

**Train 2 — Input**

```json
[
  [
    6,
    0,
    0,
    0,
    7,
    7
  ],
  [
    6,
    6,
    0,
    0,
    0,
    7
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
    8,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    6,
    0,
    0,
    8,
    8,
    8,
    0,
    7,
    7
  ],
  [
    6,
    6,
    0,
    0,
    0,
    0,
    0,
    0,
    7
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    9,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    1,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    9,
    0,
    0,
    1,
    1
  ],
  [
    9,
    9,
    0,
    0,
    1
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    2,
    0,
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    2,
    2,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    4,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    2,
    0,
    0,
    4,
    4,
    0,
    3,
    3
  ],
  [
    2,
    2,
    0,
    0,
    4,
    0,
    0,
    3
  ]
]
```


## hard_g15 — Place objects into frames by size rank

**Difficulty:** hard

**Tags:** same_size, objects, frames, assignment

**Uses new primitive(s):** center_in_frame

**Written solution:**

Some connected components are empty rectangular outline frames, and the other components are ordinary objects. Sort the ordinary objects from smallest to largest by cell count, sort the frames from smallest to largest by interior area, and place each cropped object centered inside the frame of the matching rank. Keep the frames.

**Program solution:**

```python
def solve_g_g15_assign_objects_to_frames(g):
    h,w=dims(g)
    comps=components(g)
    frames=[comp for comp in comps if is_rect_frame(comp)]
    objs=[comp for comp in comps if not is_rect_frame(comp)]
    frames=sorted(frames, key=lambda comp: ((bbox(comp['cells'])[2]-bbox(comp['cells'])[0]-1)*(bbox(comp['cells'])[3]-bbox(comp['cells'])[1]-1), bbox(comp['cells'])[1]))
    objs=sorted(objs, key=lambda comp: (len(comp['cells']), bbox(comp['cells'])[1]))
    out=blank(h,w)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    for obj,fr in zip(objs,frames):
        shape,_=object_shape(obj)
        top,left=center_in_frame(shape, fr['cells'])
        paste(out, shape, top, left, transparent=True)
    return out
```

**Train 1 — Input**

```json
[
  [
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    3,
    3,
    0,
    0,
    5,
    0,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    3,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    4,
    4,
    4,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    4,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    2,
    5,
    0,
    5,
    3,
    3,
    5,
    0,
    5,
    4,
    4,
    4,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    3,
    5,
    0,
    5,
    0,
    4,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    6,
    0,
    0,
    7,
    0,
    0,
    0,
    5,
    0,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    7,
    7,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    8,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    8,
    8,
    8,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    6,
    5,
    0,
    5,
    7,
    0,
    5,
    0,
    5,
    8,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    7,
    7,
    5,
    0,
    5,
    8,
    8,
    8,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    9,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    5,
    0,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    2,
    2,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    9,
    5,
    0,
    5,
    0,
    1,
    5,
    0,
    5,
    0,
    2,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    1,
    1,
    5,
    0,
    5,
    2,
    2,
    2,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    3,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    4,
    4,
    0,
    0,
    5,
    0,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    4,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    6,
    6,
    6,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    6,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    3,
    5,
    0,
    5,
    4,
    4,
    5,
    0,
    5,
    6,
    6,
    6,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    0,
    5,
    0,
    4,
    5,
    0,
    5,
    0,
    6,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    5,
    0,
    0,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    5,
    5,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```


## hard_g16 — Apply a whole script of transforms

**Difficulty:** hard

**Tags:** output_resize, script, transforms, composition

**Uses new primitive(s):** apply_script, apply_transform

**Written solution:**

The top row is a left-to-right script of transform tokens. Remove that row, crop the remaining object tightly, and apply the token sequence in order: 1 = rotate 90° clockwise, 2 = rotate 180°, 3 = mirror left-right, 4 = transpose. Output the final transformed crop.

**Program solution:**

```python
def solve_g_g16_scripted_transform(g):
    h,w=dims(g)
    # top row tokens 1-4; object below
    tokens=[v for v in g[0] if v in (1,2,3,4)]
    temp=[row[:] for row in g[1:]]
    shape=crop_nonzero(temp)
    return apply_script(shape, tokens)
```

**Train 1 — Input**

```json
[
  [
    1,
    3,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    6,
    6
  ],
  [
    0,
    6
  ],
  [
    0,
    6
  ]
]
```

**Train 2 — Input**

```json
[
  [
    4,
    2,
    1,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    8,
    0
  ],
  [
    0,
    0,
    7,
    0,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    7,
    0,
    8
  ],
  [
    0,
    7,
    0,
    8
  ],
  [
    7,
    7,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    3,
    3,
    2,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    9,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    9,
    9,
    0
  ],
  [
    0,
    9,
    0
  ],
  [
    0,
    9,
    9
  ]
]
```

**Test 1 — Input**

```json
[
  [
    1,
    4,
    3,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    6,
    0
  ],
  [
    6,
    6
  ],
  [
    0,
    6
  ]
]
```


## hard_g17 — Legend-controlled precedence rays

**Difficulty:** hard

**Tags:** output_resize, rays, precedence, legend

**Uses new primitive(s):** priority_overlay

**Written solution:**

The top row is a precedence legend from weakest to strongest. Ignore that row when tracing rays. In the remaining field, border emitters cast inward exactly as in the simpler ray task, gray(5) cells block them, and when multiple rays overlap, the legend order decides the winner: later colors in the legend beat earlier ones.

**Program solution:**

```python
def solve_g_g17_precedence_rays_with_legend(g):
    # row0 from col1.. has precedence legend sequence unique colors; row1+ field with border emitters and blockers
    legend=[v for v in g[0] if v!=0]
    field=[row[:] for row in g[1:]]
    h,w=dims(field)
    blockers={(r,c) for r,row in enumerate(field) for c,v in enumerate(row) if v==5}
    emitters=[]
    for c in range(w):
        if field[0][c] not in (0,5): emitters.append((0,c,field[0][c],'down'))
        if field[h-1][c] not in (0,5): emitters.append((h-1,c,field[h-1][c],'up'))
    for r in range(1,h-1):
        if field[r][0] not in (0,5): emitters.append((r,0,field[r][0],'right'))
        if field[r][w-1] not in (0,5): emitters.append((r,w-1,field[r][w-1],'left'))
    out=blank(h,w)
    for r,c in blockers: out[r][c]=5
    proposals=[]
    for r,c,color,dirn in emitters:
        out[r][c]=color
        dr,dc={'down':(1,0),'up':(-1,0),'right':(0,1),'left':(0,-1)}[dirn]
        nr,nc=r+dr,c+dc
        while 0<=nr<h and 0<=nc<w and field[nr][nc]!=5:
            proposals.append((nr,nc,color))
            nr+=dr; nc+=dc
    over=priority_overlay(h,w,proposals,precedence=legend)
    for r in range(h):
        for c in range(w):
            if over[r][c]!=0 and out[r][c]==0:
                out[r][c]=over[r][c]
    return out
```

**Train 1 — Input**

```json
[
  [
    2,
    4,
    3,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    2,
    0,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    2,
    0,
    2,
    0,
    0
  ],
  [
    4,
    4,
    4,
    4,
    4,
    4
  ],
  [
    0,
    2,
    5,
    3,
    3,
    3
  ],
  [
    0,
    2,
    0,
    2,
    0,
    0
  ],
  [
    0,
    2,
    0,
    2,
    0,
    0
  ],
  [
    0,
    2,
    0,
    2,
    0,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    6,
    1,
    8,
    0,
    0
  ],
  [
    0,
    0,
    1,
    0,
    0
  ],
  [
    6,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    8
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    6,
    1,
    0,
    0
  ],
  [
    6,
    6,
    1,
    6,
    6
  ],
  [
    0,
    6,
    5,
    8,
    8
  ],
  [
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    3,
    7,
    2,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    0,
    0,
    5,
    0,
    0,
    2
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    7,
    0,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    3,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    7,
    7,
    5,
    2,
    2,
    2
  ],
  [
    0,
    3,
    0,
    7,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    7,
    5,
    0,
    0
  ],
  [
    0,
    3,
    0,
    7,
    0,
    0,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    1,
    4,
    2,
    3,
    0,
    0
  ],
  [
    0,
    0,
    1,
    0,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    0,
    2
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0,
    1,
    4,
    0,
    0
  ],
  [
    4,
    4,
    4,
    4,
    4,
    4
  ],
  [
    0,
    0,
    5,
    2,
    2,
    2
  ],
  [
    0,
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    0,
    0
  ]
]
```


## hard_g18 — Route the shortest path between the terminals

**Difficulty:** hard

**Tags:** same_size, pathfinding, blockers, simulation

**Uses new primitive(s):** bfs_path

**Written solution:**

There are exactly two terminals of the same nonzero color and gray(5) blockers. Fill the unique shortest orthogonal path between the terminals with the terminal color, including both endpoints. Everything else becomes black(0).

**Program solution:**

```python
def solve_g_g18_shortest_path(g):
    h,w=dims(g)
    pos_by_color=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,5):
                pos_by_color[v].append((r,c))
    color,pts=min(((col,pts) for col,pts in pos_by_color.items() if len(pts)==2), key=lambda x:x[0])
    path=bfs_path(g, pts[0], pts[1], passable={0,color})
    out=blank(h,w)
    for r,c in path:
        out[r][c]=color
    return out
```

**Train 1 — Input**

```json
[
  [
    2,
    0,
    0,
    5,
    0,
    0
  ],
  [
    5,
    5,
    0,
    5,
    0,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    5
  ],
  [
    0,
    5,
    5,
    5,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    2
  ]
]
```

**Train 1 — Output**

```json
[
  [
    2,
    2,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    2,
    2,
    2,
    0
  ],
  [
    0,
    0,
    0,
    0,
    2,
    0
  ],
  [
    0,
    0,
    0,
    0,
    2,
    2
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    3,
    0,
    0
  ],
  [
    5,
    5,
    0,
    5,
    0
  ],
  [
    0,
    0,
    0,
    5,
    0
  ],
  [
    0,
    5,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    5,
    3
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    3,
    0,
    0
  ],
  [
    0,
    0,
    3,
    3,
    3
  ],
  [
    0,
    0,
    0,
    0,
    3
  ]
]
```

**Train 3 — Input**

```json
[
  [
    4,
    0,
    5,
    0,
    0,
    0
  ],
  [
    0,
    0,
    5,
    0,
    5,
    0
  ],
  [
    5,
    0,
    0,
    0,
    5,
    0
  ],
  [
    5,
    5,
    5,
    0,
    5,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    4
  ]
]
```

**Train 3 — Output**

```json
[
  [
    4,
    0,
    0,
    0,
    0,
    0
  ],
  [
    4,
    4,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    4,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    4,
    4,
    4
  ]
]
```

**Test 1 — Input**

```json
[
  [
    6,
    0,
    0,
    0,
    5,
    0
  ],
  [
    5,
    5,
    5,
    0,
    5,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    5,
    5,
    5,
    5,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    6
  ]
]
```

**Test 1 — Output**

```json
[
  [
    6,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    6,
    6,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    6
  ],
  [
    0,
    0,
    0,
    0,
    0,
    6
  ]
]
```


## hard_g19 — Align two objects and keep only the XOR shape

**Difficulty:** hard

**Tags:** output_resize, objects, comparison, xor

**Uses new primitive(s):** normalize_pair

**Written solution:**

Take the two connected objects, crop each one tightly, align their top-left corners, and compare them cell by cell as binary shapes. Output the cells that belong to exactly one of the two shapes, colored cyan(8).

**Program solution:**

```python
def solve_g_g19_normalized_xor(g):
    comps=sorted(components(g), key=lambda comp: bbox(comp['cells'])[1])
    assert len(comps)>=2
    s1,_=object_shape(comps[0]); s2,_=object_shape(comps[1])
    A,B=normalize_pair(s1,s2)
    H,W=len(A),len(A[0])
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            if (A[r][c] and not B[r][c]) or (B[r][c] and not A[r][c]):
                out[r][c]=8
    return out
```

**Train 1 — Input**

```json
[
  [
    0,
    0,
    2,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    2,
    2,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    3,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    0,
    0
  ],
  [
    0,
    0,
    8
  ],
  [
    0,
    8,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    4,
    4,
    0,
    0,
    0,
    0
  ],
  [
    0,
    4,
    0,
    0,
    5,
    0
  ],
  [
    0,
    4,
    0,
    0,
    5,
    5
  ],
  [
    0,
    0,
    0,
    0,
    0,
    5
  ]
]
```

**Train 2 — Output**

```json
[
  [
    0,
    8
  ],
  [
    8,
    0
  ],
  [
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    6,
    0,
    0,
    0,
    0
  ],
  [
    6,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
    7
  ],
  [
    0,
    0,
    0,
    0,
    0,
    7
  ],
  [
    0,
    0,
    0,
    0,
    7,
    7
  ]
]
```

**Train 3 — Output**

```json
[
  [
    8,
    0,
    0
  ],
  [
    8,
    0,
    8
  ],
  [
    8,
    8,
    0
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    0,
    9,
    0,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0,
    1
  ],
  [
    0,
    0,
    0,
    0,
    1,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0,
    1
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    0
  ],
  [
    0,
    0
  ],
  [
    0,
    0
  ]
]
```


## hard_g20 — Transform each object by its nearest control token and pack the results

**Difficulty:** hard

**Tags:** output_resize, objects, marker_control, relayout

**Uses new primitive(s):** apply_transform, pack_gallery

**Written solution:**

The bottom row contains control tokens 1, 2, 3, and 4. For each object above that row, find the nearest control token directly below it in horizontal position, crop the object, apply that token’s transform (1 = rotate 90° clockwise, 2 = rotate 180°, 3 = mirror left-right, 4 = transpose), then pack the transformed crops left to right with one black column gap.

**Program solution:**

```python
def solve_g_g20_controlled_gallery(g):
    h,w=dims(g)
    token_positions=[(c,v) for c,v in enumerate(g[h-1]) if v in (1,2,3,4)]
    field=[row[:] for row in g[:-1]]
    comps=components(field)
    assigned=[]
    for comp in sorted(comps, key=lambda comp:bbox(comp['cells'])[1]):
        ctr=center_of_bbox(comp)
        ctoken=min(token_positions, key=lambda cv: abs(ctr[1]-cv[0]))
        shape,_=object_shape(comp)
        assigned.append(apply_transform(shape, ctoken[1]))
    return pack_gallery(assigned, gap=1, align='center')
```

**Train 1 — Input**

```json
[
  [
    0,
    2,
    2,
    0,
    0,
    0,
    3,
    0
  ],
  [
    0,
    0,
    2,
    0,
    0,
    0,
    3,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    0,
    0,
    0,
    4,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    2,
    0,
    3,
    3
  ],
  [
    2,
    2,
    0,
    0,
    3
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    0,
    5,
    0,
    0,
    6,
    6,
    0
  ],
  [
    0,
    5,
    5,
    0,
    0,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    0,
    3,
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    5,
    5,
    0,
    6,
    6
  ],
  [
    5,
    0,
    0,
    6,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    7,
    0,
    0,
    0,
    0,
    8,
    0
  ],
  [
    7,
    7,
    0,
    0,
    0,
    8,
    8
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    0,
    4,
    0,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    7,
    7,
    0,
    8,
    8
  ],
  [
    7,
    0,
    0,
    0,
    8
  ]
]
```

**Test 1 — Input**

```json
[
  [
    0,
    9,
    9,
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    9,
    0,
    0,
    0,
    6,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    0,
    0,
    3,
    0,
    0,
    0
  ]
]
```

**Test 1 — Output**

```json
[
  [
    0,
    9,
    0,
    0,
    6
  ],
  [
    9,
    9,
    0,
    6,
    6
  ]
]
```


## hard_g21 — Make a four-quadrant transform mosaic from the corner keys

**Difficulty:** hard

**Tags:** output_resize, mosaic, transforms, marker_control

**Uses new primitive(s):** apply_transform, pack_gallery

**Written solution:**

The four corners are transform keys for one central object. Remove the corner keys, crop the remaining object tightly, transform one copy according to each corner key (1 = rotate 90° clockwise, 2 = rotate 180°, 3 = mirror left-right, 4 = transpose), then assemble the four transformed copies into a 2×2 mosaic with one black row and one black column gap.

**Program solution:**

```python
def solve_g_g21_corner_mosaic(g):
    h,w=dims(g)
    corner_keys={(0,0):g[0][0], (0,w-1):g[0][w-1], (h-1,0):g[h-1][0], (h-1,w-1):g[h-1][w-1]}
    temp=copy_grid(g)
    for r,c in corner_keys:
        temp[r][c]=0
    shape=crop_nonzero(temp)
    tl=apply_transform(shape, corner_keys[(0,0)])
    tr=apply_transform(shape, corner_keys[(0,w-1)])
    bl=apply_transform(shape, corner_keys[(h-1,0)])
    br=apply_transform(shape, corner_keys[(h-1,w-1)])
    top=pack_gallery([tl,tr], gap=1, align='top')
    bot=pack_gallery([bl,br], gap=1, align='top')
    W=max(dims(top)[1],dims(bot)[1])
    top2=blank(dims(top)[0],W); paste(top2, top, 0, 0)
    bot2=blank(dims(bot)[0],W); paste(bot2, bot, 0, 0)
    out=top2 + [ [0]*W ] + bot2
    return out
```

**Train 1 — Input**

```json
[
  [
    1,
    0,
    0,
    0,
    4
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    6,
    0
  ],
  [
    3,
    0,
    0,
    0,
    2
  ]
]
```

**Train 1 — Output**

```json
[
  [
    6,
    6,
    0,
    6,
    6,
    0,
    0
  ],
  [
    6,
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    6,
    0,
    0,
    0,
    6,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    6,
    0,
    6,
    6,
    6
  ],
  [
    6,
    6,
    6,
    0,
    0,
    0,
    6
  ]
]
```

**Train 2 — Input**

```json
[
  [
    2,
    0,
    0,
    0,
    3
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    7,
    7,
    0,
    0
  ],
  [
    0,
    0,
    7,
    0,
    8
  ],
  [
    4,
    0,
    0,
    0,
    1
  ]
]
```

**Train 2 — Output**

```json
[
  [
    8,
    0,
    7,
    0,
    0,
    0,
    0,
    7,
    7
  ],
  [
    0,
    0,
    7,
    7,
    0,
    8,
    0,
    7,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    7,
    0,
    0,
    0,
    7,
    0,
    0,
    0,
    0
  ],
  [
    7,
    7,
    0,
    7,
    7,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    8,
    0,
    8,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Train 3 — Input**

```json
[
  [
    3,
    0,
    0,
    0,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    9,
    9,
    0,
    0
  ],
  [
    0,
    0,
    9,
    9,
    0
  ],
  [
    2,
    0,
    0,
    0,
    4
  ]
]
```

**Train 3 — Output**

```json
[
  [
    0,
    9,
    9,
    0,
    0,
    9
  ],
  [
    9,
    9,
    0,
    0,
    9,
    9
  ],
  [
    0,
    0,
    0,
    0,
    9,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0
  ],
  [
    9,
    9,
    0,
    0,
    9,
    0
  ],
  [
    0,
    9,
    9,
    0,
    9,
    9
  ],
  [
    0,
    0,
    0,
    0,
    0,
    9
  ]
]
```

**Test 1 — Input**

```json
[
  [
    4,
    0,
    0,
    0,
    1
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    6,
    0,
    0
  ],
  [
    3,
    0,
    0,
    0,
    2
  ]
]
```

**Test 1 — Output**

```json
[
  [
    6,
    6,
    0,
    6,
    6
  ],
  [
    0,
    6,
    0,
    6,
    0
  ],
  [
    0,
    0,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    6,
    6
  ],
  [
    6,
    6,
    0,
    0,
    6
  ]
]
```
