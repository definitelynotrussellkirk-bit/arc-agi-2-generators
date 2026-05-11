# ARC-style Puzzle Bank: 21 Additional Tasks

This bank is split into 7 easy, 7 medium, and 7 hard tasks. I biased it toward the categories your current ARC solver is already instrumented around: same-size local transforms, object reasoning, extraction, scaling, and relayout.

## Index
- `easy_01` — **Fill hollow-square centers** (easy; same_size_local, pattern_completion)
- `easy_02` — **Seed paints its whole column** (easy; same_size_transform, column_logic)
- `easy_03` — **Crop to the tight bounding box** (easy; extraction, bbox)
- `easy_04` — **Mirror the left half** (easy; same_size_transform, symmetry)
- `easy_05` — **Draw down-right diagonals from seeds** (easy; same_size_transform, line_drawing)
- `easy_06` — **Recolor isolated cells** (easy; same_size_local, connectivity)
- `easy_07` — **Horizontal domino becomes a 2x2 block** (easy; same_size_local, shape_growth)
- `medium_01` — **Keep only the largest object** (medium; object_reasoning, selection)
- `medium_02` — **Draw rectangles from same-color marker pairs** (medium; global_layout, geometry)
- `medium_03` — **Scale the whole grid by 2** (medium; scaling, resampling)
- `medium_04` — **Center the object** (medium; object_reasoning, translation)
- `medium_05` — **Recolor by global color-frequency rank** (medium; global_counting, color_remap)
- `medium_06` — **Fill each object's bounding box** (medium; object_reasoning, bbox)
- `medium_07` — **Fill enclosed holes** (medium; object_reasoning, hole_fill)
- `hard_01` — **Pack objects left-to-right by size** (hard; object_extraction, sorting, relayout)
- `hard_02` — **Frame interior adopts the seed color** (hard; containment, frame_reasoning)
- `hard_03` — **Stamp a template at anchor cells** (hard; template_transfer, relayout)
- `hard_04` — **Slide the object toward the marker** (hard; translation, spatial_relation)
- `hard_05` — **Keep frames, recolor enclosed objects** (hard; containment, conditional_selection)
- `hard_06` — **Overlay two normalized objects** (hard; normalization, overlay)
- `hard_07` — **Scale the template by the number of markers** (hard; counting, scaling, template)

## easy_01 — Fill hollow-square centers

**Difficulty:** easy


**Tags:** same_size_local, pattern_completion


**Written solution:**


Whenever a 3x3 ring of a single nonzero color appears with a 0 in the middle, fill the center with that same color.


**Program solution:**

```python

def solve_e1_hollow_square_fill(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r-1][c-1]
            if color!=0:
                coords=[(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]
                if all(g[x][y]==color for x,y in coords) and g[r][c]==0:
                    out[r][c]=color
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
    3,
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    3,
    0,
    4,
    4
  ],
  [
    0,
    3,
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
    3,
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
    3,
    0,
    4,
    4
  ],
  [
    0,
    3,
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
    5,
    5,
    0,
    0,
    0
  ],
  [
    5,
    0,
    5,
    0,
    2,
    2
  ],
  [
    5,
    5,
    5,
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
    5,
    5,
    5,
    0,
    0,
    0
  ],
  [
    5,
    5,
    5,
    0,
    2,
    2
  ],
  [
    5,
    5,
    5,
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
    7,
    7,
    7,
    0
  ],
  [
    0,
    0,
    7,
    0,
    7,
    0
  ],
  [
    0,
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    9,
    9,
    9,
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
    9,
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
    7,
    7,
    7,
    0
  ],
  [
    0,
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    9,
    9,
    9,
    0,
    0
  ],
  [
    0,
    9,
    9,
    9,
    0,
    0
  ],
  [
    0,
    9,
    9,
    9,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
  [
    0,
    1,
    1,
    1,
    0,
    0
  ],
  [
    0,
    1,
    0,
    1,
    0,
    6
  ],
  [
    0,
    1,
    1,
    1,
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
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    0,
    4,
    0,
    0,
    0
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    0,
    1,
    1,
    1,
    0,
    0
  ],
  [
    0,
    1,
    1,
    1,
    0,
    6
  ],
  [
    0,
    1,
    1,
    1,
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
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ]
]
```

## easy_02 — Seed paints its whole column

**Difficulty:** easy


**Tags:** same_size_transform, column_logic


**Written solution:**


Each nonzero seed cell paints its entire column with its own color. Columns without seeds stay 0.


**Program solution:**

```python

def solve_e2_seed_column(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        # any nonzero in column paints whole column using first nonzero's color
        col=0
        for r in range(h):
            if g[r][c]!=0:
                col=g[r][c]; break
        if col!=0:
            for r in range(h):
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

**Train 1 — Output**

```json
[
  [
    0,
    3,
    0,
    0,
    4
  ],
  [
    0,
    3,
    0,
    0,
    4
  ],
  [
    0,
    3,
    0,
    0,
    4
  ],
  [
    0,
    3,
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
  ],
  [
    2,
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

**Train 2 — Output**

```json
[
  [
    2,
    0,
    5,
    0,
    0,
    0
  ],
  [
    2,
    0,
    5,
    0,
    0,
    0
  ],
  [
    2,
    0,
    5,
    0,
    0,
    0
  ],
  [
    2,
    0,
    5,
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
    0,
    0,
    0,
    7,
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
    1,
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

**Train 3 — Output**

```json
[
  [
    0,
    1,
    0,
    7,
    0,
    0
  ],
  [
    0,
    1,
    0,
    7,
    0,
    0
  ],
  [
    0,
    1,
    0,
    7,
    0,
    0
  ],
  [
    0,
    1,
    0,
    7,
    0,
    0
  ],
  [
    0,
    1,
    0,
    7,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
  [
    0,
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
    0
  ],
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
    3,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    0,
    9,
    0,
    3,
    6,
    0
  ],
  [
    0,
    9,
    0,
    3,
    6,
    0
  ],
  [
    0,
    9,
    0,
    3,
    6,
    0
  ],
  [
    0,
    9,
    0,
    3,
    6,
    0
  ],
  [
    0,
    9,
    0,
    3,
    6,
    0
  ]
]
```

## easy_03 — Crop to the tight bounding box

**Difficulty:** easy


**Tags:** extraction, bbox


**Written solution:**


Output only the smallest rectangle that contains all nonzero cells.


**Program solution:**

```python

def solve_e3_crop_bbox(g):
    return crop_bbox(g)

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
    2,
    2,
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
    2
  ],
  [
    2,
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

**Train 2 — Output**

```json
[
  [
    5,
    0,
    0
  ],
  [
    5,
    5,
    5
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
    7,
    7,
    0,
    0
  ],
  [
    0,
    0,
    0,
    0,
    7,
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
    7,
    7
  ],
  [
    0,
    7
  ]
]
```

**Test — Input**

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
    4,
    0,
    0
  ],
  [
    0,
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

**Test — Output**

```json
[
  [
    0,
    4,
    0
  ],
  [
    4,
    4,
    4
  ]
]
```

## easy_04 — Mirror the left half

**Difficulty:** easy


**Tags:** same_size_transform, symmetry


**Written solution:**


Copy the pattern in the left half of the grid to the right half by horizontal mirroring.


**Program solution:**

```python

def solve_e4_mirror_left_half(g):
    h,w=dims(g); assert w%2==0
    out=copy_grid(g)
    half=w//2
    for r in range(h):
        for c in range(half):
            out[r][w-1-c]=g[r][c]
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
    2,
    2,
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
    0,
    2,
    0
  ],
  [
    2,
    2,
    0,
    0,
    2,
    2
  ],
  [
    0,
    2,
    0,
    0,
    2,
    0
  ]
]
```

**Train 2 — Input**

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
    0
  ],
  [
    3,
    3,
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
    0
  ]
]
```

**Train 2 — Output**

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
    3
  ],
  [
    3,
    3,
    0,
    0,
    0,
    0,
    3,
    3
  ],
  [
    0,
    3,
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
    0,
    0
  ],
  [
    0,
    0,
    4,
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

**Train 3 — Output**

```json
[
  [
    0,
    0,
    4,
    4,
    0,
    0
  ],
  [
    0,
    4,
    4,
    4,
    4,
    0
  ],
  [
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
    0
  ]
]
```

**Test — Input**

```json
[
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

**Test — Output**

```json
[
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
    0
  ]
]
```

## easy_05 — Draw down-right diagonals from seeds

**Difficulty:** easy


**Tags:** same_size_transform, line_drawing


**Written solution:**


From every nonzero seed, draw a diagonal line of the same color toward the bottom-right edge.


**Program solution:**

```python

def solve_e5_diagonal_dr(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r,c,v in nonzero_cells(g):
        x,y=r,c
        while 0<=x<h and 0<=y<w:
            out[x][y]=v
            x+=1; y+=1
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

**Train 1 — Output**

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
    0
  ],
  [
    0,
    0,
    0,
    6,
    0
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

**Train 2 — Output**

```json
[
  [
    2,
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
    0
  ],
  [
    0,
    0,
    2,
    4,
    0,
    0
  ],
  [
    0,
    0,
    0,
    2,
    4,
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

**Train 3 — Output**

```json
[
  [
    0,
    0,
    7,
    0,
    0
  ],
  [
    0,
    0,
    0,
    7,
    0
  ],
  [
    3,
    0,
    0,
    0,
    7
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
    0,
    3,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
  [
    0,
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

**Test — Output**

```json
[
  [
    0,
    5,
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
    0
  ],
  [
    0,
    0,
    0,
    5,
    8,
    0
  ],
  [
    0,
    0,
    0,
    0,
    5,
    8
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

## easy_06 — Recolor isolated cells

**Difficulty:** easy


**Tags:** same_size_local, connectivity


**Written solution:**


Any nonzero cell with no nonzero 4-neighbor is isolated and becomes cyan(8). Connected clusters stay unchanged.


**Program solution:**

```python

def solve_e6_isolated_to_8(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r,c,v in nonzero_cells(g):
        if all(not (0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]!=0) for dr,dc in DIR4):
            out[r][c]=8
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
    0
  ],
  [
    0,
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
    6,
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
    8,
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
    0,
    8,
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
    6,
    0
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
    0
  ],
  [
    0,
    0,
    0,
    7,
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
    0,
    0,
    9
  ]
]
```

**Train 2 — Output**

```json
[
  [
    8,
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
    0,
    0,
    8
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
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
    2,
    0
  ],
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
    8,
    0
  ],
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
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Input**

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
    0
  ],
  [
    6,
    0,
    0,
    0,
    0,
    0
  ],
  [
    6,
    0,
    7,
    0,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    0,
    8,
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
    6,
    0,
    0,
    0,
    0,
    0
  ],
  [
    6,
    0,
    8,
    0,
    0,
    0
  ]
]
```

## easy_07 — Horizontal domino becomes a 2x2 block

**Difficulty:** easy


**Tags:** same_size_local, shape_growth


**Written solution:**


Whenever two equal nonzero cells sit side by side horizontally, fill the two cells directly below them with that color.


**Program solution:**

```python

def solve_e7_domino_to_2x2(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            v=g[r][c]
            if v!=0 and g[r][c+1]==v:
                out[r+1][c]=v
                out[r+1][c+1]=v
    return out

```

**Train 1 — Input**

```json
[
  [
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
    0
  ],
  [
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
    2,
    0,
    0
  ],
  [
    0,
    2,
    2,
    0,
    0
  ],
  [
    0,
    0,
    3,
    3,
    0
  ],
  [
    0,
    0,
    3,
    3,
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
    0,
    0,
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
    0
  ]
]
```

**Train 2 — Output**

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
    4,
    4,
    0,
    5,
    5,
    0
  ],
  [
    0,
    0,
    0,
    5,
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

**Train 3 — Output**

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
    6,
    6,
    0,
    7,
    7
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
    0,
    0
  ]
]
```

**Test — Input**

```json
[
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

**Test — Output**

```json
[
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
    1,
    1,
    0,
    8,
    8
  ],
  [
    0,
    0,
    0,
    0,
    8,
    8
  ]
]
```

## medium_01 — Keep only the largest object

**Difficulty:** medium


**Tags:** object_reasoning, selection


**Written solution:**


Find the largest connected nonzero object, erase all other objects, and recolor the kept object to cyan(8).


**Program solution:**

```python

def solve_m1_keep_largest_recolor(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    if not comps:
        return zeros(h,w)
    best=max(comps, key=lambda comp: len(comp["cells"]))
    out=zeros(h,w)
    for r,c in best["cells"]:
        out[r][c]=8
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
    3,
    3,
    0,
    4,
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
    3,
    0,
    0,
    4,
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
    8,
    8,
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
    0,
    8,
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
  ]
]
```

**Train 2 — Input**

```json
[
  [
    0,
    6,
    6,
    6,
    0,
    0,
    0
  ],
  [
    0,
    6,
    0,
    6,
    0,
    2,
    0
  ],
  [
    0,
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
    0,
    0
  ],
  [
    3,
    3,
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
    8,
    8,
    8,
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
    0
  ],
  [
    0,
    8,
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
    1,
    1,
    1,
    0,
    0,
    0
  ],
  [
    0,
    1,
    0,
    0,
    7,
    7
  ],
  [
    0,
    1,
    0,
    0,
    0,
    7
  ],
  [
    0,
    1,
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
    8,
    8,
    8,
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
    0,
    8,
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
  ]
]
```

**Test — Input**

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
    4,
    4,
    4,
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
    2,
    2
  ],
  [
    0,
    4,
    4,
    4,
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
    5,
    5,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Output**

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
    8,
    8,
    8,
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
    0
  ],
  [
    0,
    8,
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

## medium_02 — Draw rectangles from same-color marker pairs

**Difficulty:** medium


**Tags:** global_layout, geometry


**Written solution:**


For each color, the two cells of that color mark opposite corners of a rectangle; draw the rectangle border in that color.


**Program solution:**

```python

def solve_m2_marker_rectangle_border(g):
    h,w=dims(g)
    positions=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                positions[v].append((r,c))
    out=zeros(h,w)
    for color,cells in positions.items():
        if len(cells)!=2:
            # just copy cells if not exactly two? but our examples will use pairs only
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        ra,rb=sorted([r1,r2]); ca,cb=sorted([c1,c2])
        for c in range(ca,cb+1):
            out[ra][c]=color
            out[rb][c]=color
        for r in range(ra,rb+1):
            out[r][ca]=color
            out[r][cb]=color
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
    2,
    2,
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
    0,
    0,
    4,
    4,
    4
  ],
  [
    0,
    0,
    0,
    4,
    4,
    4
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
    3,
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
  ],
  [
    3,
    0,
    0,
    0,
    0,
    5,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    3,
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
    0,
    0
  ],
  [
    3,
    0,
    0,
    5,
    5,
    5,
    0
  ],
  [
    3,
    0,
    0,
    5,
    0,
    5,
    0
  ],
  [
    3,
    0,
    0,
    5,
    5,
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
  ],
  [
    0,
    1,
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
    1,
    0
  ],
  [
    0,
    0,
    0,
    6,
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
    6,
    6,
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
    1,
    1,
    1,
    1,
    0
  ],
  [
    0,
    1,
    6,
    6,
    1,
    0
  ],
  [
    0,
    1,
    1,
    1,
    1,
    0
  ],
  [
    0,
    0,
    6,
    6,
    0,
    0
  ]
]
```

**Test — Input**

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
    7,
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
    7
  ],
  [
    0,
    0,
    0,
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
  ]
]
```

**Test — Output**

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
    7,
    7,
    7,
    7,
    7,
    7
  ],
  [
    0,
    7,
    7,
    7,
    7,
    7,
    7
  ],
  [
    0,
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
    3,
    0,
    3,
    0
  ],
  [
    0,
    0,
    0,
    3,
    3,
    3,
    0
  ]
]
```

## medium_03 — Scale the whole grid by 2

**Difficulty:** medium


**Tags:** scaling, resampling


**Written solution:**


Each input cell becomes a 2x2 block of the same color in the output.


**Program solution:**

```python

def solve_m3_scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=v
            out[2*r][2*c+1]=v
            out[2*r+1][2*c]=v
            out[2*r+1][2*c+1]=v
    return out

```

**Train 1 — Input**

```json
[
  [
    0,
    2,
    0
  ],
  [
    3,
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
    3,
    3,
    0,
    0,
    0,
    0
  ],
  [
    3,
    3,
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
    4,
    0,
    5
  ],
  [
    0,
    0,
    0
  ],
  [
    6,
    6,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    4,
    4,
    0,
    0,
    5,
    5
  ],
  [
    4,
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
    6,
    0,
    0
  ],
  [
    6,
    6,
    6,
    6,
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
    7
  ],
  [
    7,
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
    7,
    7
  ],
  [
    0,
    0,
    7,
    7
  ],
  [
    7,
    7,
    0,
    0
  ],
  [
    7,
    7,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
  [
    1,
    0,
    0
  ],
  [
    0,
    8,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    1,
    1,
    0,
    0,
    0,
    0
  ],
  [
    1,
    1,
    0,
    0,
    0,
    0
  ],
  [
    0,
    0,
    8,
    8,
    0,
    0
  ],
  [
    0,
    0,
    8,
    8,
    0,
    0
  ]
]
```

## medium_04 — Center the object

**Difficulty:** medium


**Tags:** object_reasoning, translation


**Written solution:**


Take the single nonzero object, keep its shape, and translate it so its bounding box is centered in the grid.


**Program solution:**

```python

def solve_m4_center_object(g):
    h,w=dims(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return zeros(h,w)
    rs=[r for r,c,v in cells]; cs=[c for r,c,v in cells]
    r0,c0,r1,c1=min(rs),min(cs),max(rs),max(cs)
    obj_h,obj_w=r1-r0+1,c1-c0+1
    new_r=(h-obj_h)//2
    new_c=(w-obj_w)//2
    out=zeros(h,w)
    for r,c,v in cells:
        out[new_r + (r-r0)][new_c + (c-c0)] = v
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
    2,
    0,
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
    2,
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
    5,
    0
  ],
  [
    0,
    0,
    0,
    0,
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
    7,
    7,
    7,
    0
  ],
  [
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
    0
  ],
  [
    0,
    7,
    7,
    7,
    0
  ],
  [
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

**Test — Input**

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
    4,
    4
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

**Test — Output**

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

## medium_05 — Recolor by global color-frequency rank

**Difficulty:** medium


**Tags:** global_counting, color_remap


**Written solution:**


Rank nonzero colors by how many cells they occupy. The most frequent becomes 1, the second becomes 2, the third becomes 3, and so on.


**Program solution:**

```python

def solve_m5_color_rank_recolor(g):
    counts=Counter(v for row in g for v in row if v!=0)
    order=[color for color,_ in sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))]
    mapping={color:i+1 for i,color in enumerate(order)}
    return [[mapping.get(v,0) for v in row] for row in g]

```

**Train 1 — Input**

```json
[
  [
    0,
    4,
    4,
    4,
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
    7,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    0,
    1,
    1,
    1,
    0
  ],
  [
    0,
    1,
    0,
    0,
    0
  ],
  [
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
    3,
    0
  ]
]
```

**Train 2 — Input**

```json
[
  [
    5,
    5,
    5,
    0,
    0,
    0
  ],
  [
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
    6,
    0
  ],
  [
    0,
    8,
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
    1,
    0,
    0,
    0
  ],
  [
    1,
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
    0
  ],
  [
    0,
    3,
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
    9,
    9,
    9
  ],
  [
    0,
    0,
    9,
    0,
    0
  ],
  [
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    1,
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
    1,
    1,
    1
  ],
  [
    0,
    0,
    1,
    0,
    0
  ],
  [
    2,
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
    0
  ]
]
```

**Test — Input**

```json
[
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
    2,
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
    7,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    0,
    0,
    1,
    1,
    1,
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
    2,
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
    0
  ]
]
```

## medium_06 — Fill each object's bounding box

**Difficulty:** medium


**Tags:** object_reasoning, bbox


**Written solution:**


For every connected nonzero object, fill its entire axis-aligned bounding box with the object's color.


**Program solution:**

```python

def solve_m6_fill_bbox_each_object(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in components4(g, color_sensitive=True):
        color=comp["color"]
        r0,c0,r1,c1=bbox_of_cells(comp["cells"])
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
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
    4,
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
    0,
    0,
    0,
    0,
    4,
    4
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
    4,
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
    0,
    0,
    4,
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
    7,
    7,
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
    3,
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
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
  [
    0,
    1,
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
  ],
  [
    0,
    0,
    4,
    0,
    0,
    0
  ],
  [
    0,
    0,
    4,
    4,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    0,
    1,
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
  ],
  [
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
    4,
    4,
    0,
    0
  ]
]
```

## medium_07 — Fill enclosed holes

**Difficulty:** medium


**Tags:** object_reasoning, hole_fill


**Written solution:**


Any zero region completely enclosed by a single-color object gets filled with that object's color.


**Program solution:**

```python

def solve_m7_fill_holes(g):
    h,w=dims(g)
    out=copy_grid(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 or seen[r][c]:
                continue
            q=deque([(r,c)]); seen[r][c]=True; region=[]; touches=False; neigh_colors=set()
            while q:
                x,y=q.popleft(); region.append((x,y))
                if x==0 or y==0 or x==h-1 or y==w-1:
                    touches=True
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w:
                        if g[nx][ny]==0 and not seen[nx][ny]:
                            seen[nx][ny]=True; q.append((nx,ny))
                        elif g[nx][ny]!=0:
                            neigh_colors.add(g[nx][ny])
            if not touches and len(neigh_colors)==1:
                color=next(iter(neigh_colors))
                for x,y in region:
                    out[x][y]=color
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
    3,
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
    0,
    3,
    0,
    4,
    4
  ],
  [
    0,
    3,
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
    3,
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
    3,
    0,
    4,
    4
  ],
  [
    0,
    3,
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
    5,
    5,
    5,
    0,
    0
  ],
  [
    5,
    0,
    0,
    5,
    0,
    2
  ],
  [
    5,
    0,
    0,
    5,
    0,
    2
  ],
  [
    5,
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
    5,
    5,
    0,
    0
  ],
  [
    5,
    5,
    5,
    5,
    0,
    2
  ],
  [
    5,
    5,
    5,
    5,
    0,
    2
  ],
  [
    5,
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
    0
  ],
  [
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    7,
    0,
    7,
    0
  ],
  [
    0,
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
    0
  ],
  [
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
    7,
    7,
    7,
    0
  ],
  [
    0,
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
    0
  ]
]
```

**Test — Input**

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
    6,
    6,
    6,
    6,
    0
  ],
  [
    0,
    6,
    0,
    0,
    6,
    0
  ],
  [
    0,
    6,
    0,
    0,
    6,
    0
  ],
  [
    0,
    6,
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
    0,
    0
  ]
]
```

**Test — Output**

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
    6,
    6,
    6,
    6,
    0
  ],
  [
    0,
    6,
    6,
    6,
    6,
    0
  ],
  [
    0,
    6,
    6,
    6,
    6,
    0
  ],
  [
    0,
    6,
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
    0,
    0
  ]
]
```

## hard_01 — Pack objects left-to-right by size

**Difficulty:** hard


**Tags:** object_extraction, sorting, relayout


**Written solution:**


Crop each connected object to its own bounding box, sort the cropped objects by size descending, and pack them left-to-right with one blank column between them.


**Program solution:**

```python

def solve_h1_pack_objects_sorted(g):
    comps=components4(g, color_sensitive=True)
    if not comps:
        return [[0]]
    # crop each object to bbox
    items=[]
    for comp in comps:
        sub,_=crop_from_cells(g, comp["cells"])
        h,w=dims(sub)
        items.append((len(comp["cells"]), h, w, comp["color"], sub))
    # sort by area desc, then top-left of original via min coords
    def key(item):
        area,h,w,color,sub=item
        return (-area, -h, -w, color)
    items=sorted(items, key=key)
    out_h=max(dims(sub)[0] for _,_,_,_,sub in items)
    out_w=sum(dims(sub)[1] for _,_,_,_,sub in items) + (len(items)-1)
    out=zeros(out_h,out_w)
    cur=0
    for _,_,_,_,sub in items:
        sh,sw=dims(sub)
        for r in range(sh):
            for c in range(sw):
                out[r][cur+c]=sub[r][c]
        cur += sw + 1
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
    2,
    0,
    4,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    4,
    4,
    0
  ],
  [
    0,
    2,
    0,
    0,
    0,
    0,
    0
  ],
  [
    6,
    6,
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
    0,
    6,
    6
  ],
  [
    2,
    0,
    0,
    4,
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
    0
  ],
  [
    0,
    3,
    3,
    3,
    0,
    5,
    0,
    0
  ],
  [
    0,
    3,
    0,
    3,
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
    5,
    0
  ],
  [
    7,
    7,
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
    3,
    3,
    3,
    0,
    5,
    0,
    0,
    7,
    7
  ],
  [
    3,
    0,
    3,
    0,
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
    5,
    5,
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
    1,
    0,
    0,
    0,
    0
  ],
  [
    0,
    1,
    0,
    0,
    6,
    6,
    0
  ],
  [
    0,
    1,
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
    0
  ],
  [
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

**Train 3 — Output**

```json
[
  [
    1,
    1,
    0,
    6,
    6,
    0,
    8
  ],
  [
    1,
    0,
    0,
    0,
    6,
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
    0
  ]
]
```

**Test — Input**

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
    0
  ],
  [
    0,
    4,
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
    4,
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
    0,
    2,
    2,
    0
  ],
  [
    7,
    7,
    0,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    4,
    4,
    4,
    0,
    2,
    0,
    0,
    7,
    7
  ],
  [
    4,
    0,
    4,
    0,
    2,
    2,
    0,
    0,
    0
  ]
]
```

## hard_02 — Frame interior adopts the seed color

**Difficulty:** hard


**Tags:** containment, frame_reasoning


**Written solution:**


Each hollow rectangular frame keeps its border color, but its interior is filled with the color of the nonzero seed placed inside the frame.


**Program solution:**

```python

def solve_h2_frame_fill_from_seed(g):
    out=copy_grid(g)
    frames=find_rect_frames(g)
    for fr in frames:
        color=fr["color"]; r0,c0,r1,c1=fr["bbox"]
        # find nonzero seed cells strictly inside that are not frame color
        seeds=[]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0 and g[r][c]!=color:
                    seeds.append(g[r][c])
        if len(set(seeds))==1 and seeds:
            fill=seeds[0]
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=fill
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
    2,
    2,
    2,
    0,
    0
  ],
  [
    0,
    2,
    0,
    5,
    2,
    0,
    0
  ],
  [
    0,
    2,
    0,
    0,
    2,
    0,
    0
  ],
  [
    0,
    2,
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
    2,
    2,
    2,
    2,
    0,
    0
  ],
  [
    0,
    2,
    5,
    5,
    2,
    0,
    0
  ],
  [
    0,
    2,
    5,
    5,
    2,
    0,
    0
  ],
  [
    0,
    2,
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
    0,
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
    4,
    4,
    4,
    0,
    0
  ],
  [
    4,
    0,
    0,
    0,
    4,
    0,
    0
  ],
  [
    4,
    0,
    7,
    0,
    4,
    0,
    6
  ],
  [
    4,
    0,
    0,
    0,
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
    0,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    4,
    4,
    4,
    4,
    4,
    0,
    0
  ],
  [
    4,
    7,
    7,
    7,
    4,
    0,
    0
  ],
  [
    4,
    7,
    7,
    7,
    4,
    0,
    6
  ],
  [
    4,
    7,
    7,
    7,
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
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
    8,
    8,
    0,
    1,
    1
  ],
  [
    0,
    8,
    0,
    0,
    8,
    0,
    1,
    1
  ],
  [
    0,
    8,
    2,
    0,
    8,
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
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
    0
  ],
  [
    0,
    8,
    8,
    8,
    8,
    0,
    1,
    1
  ],
  [
    0,
    8,
    2,
    2,
    8,
    0,
    1,
    1
  ],
  [
    0,
    8,
    2,
    2,
    8,
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
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
    0,
    0,
    0
  ]
]
```

**Test — Input**

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
    5,
    5,
    5,
    5,
    0,
    0
  ],
  [
    0,
    5,
    0,
    9,
    5,
    0,
    0
  ],
  [
    0,
    5,
    0,
    0,
    5,
    0,
    0
  ],
  [
    0,
    5,
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
    0,
    0
  ]
]
```

**Test — Output**

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
    5,
    5,
    5,
    5,
    0,
    0
  ],
  [
    0,
    5,
    9,
    9,
    5,
    0,
    0
  ],
  [
    0,
    5,
    9,
    9,
    5,
    0,
    0
  ],
  [
    0,
    5,
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
    0,
    0
  ]
]
```

## hard_03 — Stamp a template at anchor cells

**Difficulty:** hard


**Tags:** template_transfer, relayout


**Written solution:**


Find the one multi-cell template object. For every single-cell anchor, stamp a copy of the template's cropped shape using the anchor color, with the anchor as the template's top-left corner. The original input objects disappear.


**Program solution:**

```python

def solve_h3_stamp_template_at_anchors(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    # template = unique component with size >1; anchors = singleton components
    templates=[comp for comp in comps if len(comp["cells"])>1]
    singles=[comp for comp in comps if len(comp["cells"])==1]
    assert len(templates)==1
    template=templates[0]
    temp_sub,_=crop_from_cells(g, template["cells"])
    # anchor color from singleton comps, assume all same color
    anchor_color=singles[0]["color"] if singles else template["color"]
    out=zeros(h,w)
    # use anchor cell as top-left placement
    for comp in singles:
        (ar,ac)=comp["cells"][0]
        for r,row in enumerate(temp_sub):
            for c,v in enumerate(row):
                if v!=0 and 0<=ar+r<h and 0<=ac+c<w:
                    out[ar+r][ac+c]=anchor_color
    return out

```

**Train 1 — Input**

```json
[
  [
    2,
    2,
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
    8,
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
    0
  ],
  [
    0,
    0,
    0,
    0,
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
    8,
    0,
    0,
    0
  ],
  [
    0,
    8,
    8,
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
    0,
    8,
    8
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
    0
  ],
  [
    0,
    3,
    0,
    0,
    7,
    0
  ],
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
    4,
    4,
    0,
    0,
    0
  ],
  [
    0,
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
    6,
    0
  ],
  [
    0,
    6,
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
    6,
    6
  ],
  [
    0,
    6,
    6,
    0,
    0,
    6,
    0
  ],
  [
    0,
    6,
    0,
    0,
    0,
    0,
    0
  ]
]
```

**Test — Input**

```json
[
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
    5,
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
    0,
    0
  ],
  [
    9,
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
    9,
    0,
    0
  ]
]
```

**Test — Output**

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
    9,
    9
  ],
  [
    0,
    0,
    0,
    0,
    0,
    0,
    9
  ],
  [
    9,
    9,
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
    0,
    9,
    9,
    0
  ]
]
```

## hard_04 — Slide the object toward the marker

**Difficulty:** hard


**Tags:** translation, spatial_relation


**Written solution:**


There is one marker cell and one multi-cell object. Move the object in a straight line until its bounding box becomes edge-adjacent to the marker, without moving the marker.


**Program solution:**

```python

def solve_h4_move_object_toward_marker(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    singles=[comp for comp in comps if len(comp["cells"])==1]
    objects=[comp for comp in comps if len(comp["cells"])>1]
    assert len(singles)==1 and len(objects)==1
    marker=singles[0]["cells"][0]
    obj=objects[0]
    r0,c0,r1,c1=bbox_of_cells(obj["cells"])
    mr,mc=marker
    # determine if marker is left/right/up/down of bbox with no overlap in that axis
    dr=dc=0
    if mc > c1:
        dc = (mc - 1) - c1
    elif mc < c0:
        dc = (mc + 1) - c0
    elif mr > r1:
        dr = (mr - 1) - r1
    elif mr < r0:
        dr = (mr + 1) - r0
    else:
        # marker aligned inside bbox projection; choose minimal move away? not used
        pass
    out=zeros(h,w)
    # keep marker
    out[mr][mc]=g[mr][mc]
    color=obj["color"]
    for r,c in obj["cells"]:
        nr,nc=r+dr,c+dc
        out[nr][nc]=color
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
    2,
    0,
    0,
    0,
    1
  ],
  [
    2,
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
    0,
    2,
    2,
    1
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
    0,
    0,
    0,
    0
  ],
  [
    1,
    0,
    0,
    3,
    3
  ],
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
    1,
    3,
    3,
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
    1,
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
    4,
    4,
    0
  ],
  [
    0,
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
    1,
    0,
    0
  ],
  [
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
    0,
    0,
    0
  ]
]
```

**Test — Input**

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
    5,
    5,
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
  ],
  [
    0,
    0,
    0,
    1,
    0,
    0
  ]
]
```

**Test — Output**

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
    5,
    5,
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
    1,
    0,
    0
  ]
]
```

## hard_05 — Keep frames, recolor enclosed objects

**Difficulty:** hard


**Tags:** containment, conditional_selection


**Written solution:**


Keep every rectangular frame. Any object fully enclosed inside a frame is recolored to the frame's color. Any object outside all frames is erased.


**Program solution:**

```python

def solve_h5_enclosed_recolor_keep_frames(g):
    h,w=dims(g)
    out=zeros(h,w)
    frames=find_rect_frames(g)
    # keep frames
    for fr in frames:
        for r,c in fr["cells"]:
            out[r][c]=fr["color"]
    # recolor enclosed objects
    comps=components4(g, color_sensitive=True)
    frame_cell_sets=[set(fr["cells"]) for fr in frames]
    for comp in comps:
        cells=set(comp["cells"])
        # skip frames themselves
        if any(cells==fset for fset in frame_cell_sets):
            continue
        # find containing frame whose bbox strictly contains comp bbox
        cr0,cc0,cr1,cc1=bbox_of_cells(comp["cells"])
        containing=[]
        for fr in frames:
            r0,c0,r1,c1=fr["bbox"]
            if r0 < cr0 and c0 < cc0 and cr1 < r1 and cc1 < c1:
                containing.append(fr)
        if containing:
            # choose smallest containing frame by area
            fr=min(containing, key=lambda fr:(fr["bbox"][2]-fr["bbox"][0])*(fr["bbox"][3]-fr["bbox"][1]))
            for r,c in comp["cells"]:
                out[r][c]=fr["color"]
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
    2,
    2,
    2,
    0,
    0
  ],
  [
    0,
    2,
    5,
    0,
    2,
    0,
    7
  ],
  [
    0,
    2,
    0,
    5,
    2,
    0,
    0
  ],
  [
    0,
    2,
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
    2,
    2,
    2,
    2,
    0,
    0
  ],
  [
    0,
    2,
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
    2,
    0,
    0
  ],
  [
    0,
    2,
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
    0,
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
    4,
    4,
    0,
    0
  ],
  [
    4,
    0,
    6,
    4,
    0,
    8
  ],
  [
    4,
    0,
    0,
    4,
    0,
    0
  ],
  [
    4,
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
    4,
    4,
    4,
    4,
    0,
    0
  ],
  [
    4,
    0,
    4,
    4,
    0,
    0
  ],
  [
    4,
    0,
    0,
    4,
    0,
    0
  ],
  [
    4,
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
    0,
    0,
    0
  ],
  [
    0,
    3,
    3,
    3,
    3,
    0,
    1,
    1
  ],
  [
    0,
    3,
    0,
    9,
    3,
    0,
    1,
    0
  ],
  [
    0,
    3,
    0,
    0,
    3,
    0,
    1,
    1
  ],
  [
    0,
    3,
    3,
    3,
    3,
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
    0
  ],
  [
    0,
    3,
    3,
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
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
    0,
    0,
    3,
    0,
    0,
    0
  ],
  [
    0,
    3,
    3,
    3,
    3,
    0,
    0,
    0
  ]
]
```

**Test — Input**

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
    6,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    6,
    0,
    4,
    6,
    0,
    0
  ],
  [
    0,
    6,
    4,
    4,
    6,
    0,
    2
  ],
  [
    0,
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
    0,
    0,
    0,
    0
  ]
]
```

**Test — Output**

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
    6,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
    6,
    0,
    6,
    6,
    0,
    0
  ],
  [
    0,
    6,
    6,
    6,
    6,
    0,
    0
  ],
  [
    0,
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
    0,
    0,
    0,
    0
  ]
]
```

## hard_06 — Overlay two normalized objects

**Difficulty:** hard


**Tags:** normalization, overlay


**Written solution:**


Crop the two objects to their own bounding boxes, translate both crops to the top-left origin, and overlay them. Cells occupied by both become cyan(8); cells occupied by only one keep that object's color.


**Program solution:**

```python

def solve_h6_overlay_normalized(g):
    comps=components4(g, color_sensitive=True)
    assert len(comps)==2
    comp_a, comp_b = comps
    sub_a=normalize_object_to_origin(g, comp_a)
    sub_b=normalize_object_to_origin(g, comp_b)
    ha,wa=dims(sub_a); hb,wb=dims(sub_b)
    out=zeros(max(ha,hb), max(wa,wb))
    color_a=comp_a["color"]; color_b=comp_b["color"]
    for r in range(len(out)):
        for c in range(len(out[0])):
            va = sub_a[r][c] if r<ha and c<wa else 0
            vb = sub_b[r][c] if r<hb and c<wb else 0
            if va!=0 and vb!=0:
                out[r][c]=8
            elif va!=0:
                out[r][c]=color_a
            elif vb!=0:
                out[r][c]=color_b
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
    0,
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
    5,
    0
  ]
]
```

**Train 1 — Output**

```json
[
  [
    2,
    8
  ],
  [
    8,
    5
  ]
]
```

**Train 2 — Input**

```json
[
  [
    3,
    0,
    0,
    0,
    0
  ],
  [
    3,
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
    0,
    7,
    7,
    0
  ],
  [
    0,
    0,
    0,
    7,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    8,
    7
  ],
  [
    3,
    8
  ]
]
```

**Train 3 — Input**

```json
[
  [
    0,
    4,
    4,
    0,
    0,
    0
  ],
  [
    0,
    0,
    4,
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
  ]
]
```

**Train 3 — Output**

```json
[
  [
    8,
    4
  ],
  [
    6,
    8
  ]
]
```

**Test — Input**

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
    9,
    9,
    0,
    0
  ],
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
    2,
    2,
    0
  ]
]
```

**Test — Output**

```json
[
  [
    9,
    8,
    9
  ],
  [
    8,
    2,
    0
  ]
]
```

## hard_07 — Scale the template by the number of markers

**Difficulty:** hard


**Tags:** counting, scaling, template


**Written solution:**


Count the number of single-cell markers. Crop the one multi-cell template object and scale it uniformly by that count.


**Program solution:**

```python

def solve_h7_scale_template_by_marker_count(g):
    comps=components4(g, color_sensitive=True)
    templates=[comp for comp in comps if len(comp["cells"])>1]
    markers=[comp for comp in comps if len(comp["cells"])==1]
    assert len(templates)==1
    k=len(markers)
    sub,_=crop_from_cells(g, templates[0]["cells"])
    return scale_grid_nearest(sub, k)

```

**Train 1 — Input**

```json
[
  [
    2,
    2,
    0,
    0,
    0
  ],
  [
    2,
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
    9
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
    2
  ],
  [
    2,
    2,
    2,
    2
  ],
  [
    2,
    2,
    0,
    0
  ],
  [
    2,
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
    0,
    3,
    3,
    0,
    0,
    0
  ],
  [
    0,
    0,
    3,
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
    8,
    0
  ]
]
```

**Train 2 — Output**

```json
[
  [
    3,
    3,
    3,
    3,
    3,
    3
  ],
  [
    3,
    3,
    3,
    3,
    3,
    3
  ],
  [
    3,
    3,
    3,
    3,
    3,
    3
  ],
  [
    0,
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
    3,
    3,
    3
  ],
  [
    0,
    0,
    0,
    3,
    3,
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
    0,
    0,
    0
  ],
  [
    4,
    4,
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
    0,
    0,
    7,
    0
  ]
]
```

**Train 3 — Output**

```json
[
  [
    4,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    4,
    4,
    0,
    0,
    0
  ],
  [
    4,
    4,
    4,
    0,
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
    4,
    4,
    4,
    4,
    4,
    4
  ],
  [
    4,
    4,
    4,
    4,
    4,
    4
  ]
]
```

**Test — Input**

```json
[
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
    6
  ]
]
```

**Test — Output**

```json
[
  [
    5,
    5,
    5,
    5
  ],
  [
    5,
    5,
    5,
    5
  ],
  [
    5,
    5,
    0,
    0
  ],
  [
    5,
    5,
    0,
    0
  ]
]
```
