# ARC Puzzle Bank — Set 18


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `periodic_ray`: Infer a step from two same-color seeds and continue stamping the color at that period.
- `segment_midpoint`: Fill the midpoint of a clear straight segment between matching endpoints.
- `distance_band`: Paint cells at an exact Manhattan distance from a seed.
- `bbox_corners`: Reduce each object to the four corners of its bounding box.
- `diagonal_line`: Complete the full main diagonal that passes through each seed.
- `row_leader_recolor`: Use the leftmost nonzero cell in a row as that row’s recolor key.
- `opposite_pair_fill`: Fill a zero cell when opposite neighbors horizontally or vertically agree.
- `room_flood`: Flood the zero cells inside a walled room from its seed color.
- `column_histogram`: Summarize an object by bottom-aligned bars whose heights equal per-column counts.
- `transform_script`: Apply a left-to-right sequence of transform codes to a cropped object.
- `contact_shell`: Replace an object by its one-step orthogonal shell.
- `offset_transfer`: Copy all payload offsets from one anchor to another anchor.
- `pivot_rays`: Cast four orthogonal rays from each pivot until a wall or obstacle.
- `frame_gallery`: Extract frame interiors and concatenate them as a gallery.
- `keyed_frame_embed`: Use a marker above a frame to choose which source object to center inside it.
- `portal_bfs`: Route a shortest path while teleporting across matched portal pairs.
- `radial_order_pack`: Sort objects by angle around a hub and pack them into a gallery.
- `transform_timeline`: Emit every intermediate transformed state, not only the final one.
- `gated_flood`: Flood through walls only at gate cells whose color matches the seed.
- `dihedral_select`: Find which candidate matches a guide under rotation or reflection.
- `parity_wavefront`: Color reachable cells by even or odd shortest-path distance from a seed.

## easy_p01 — Periodic Row Extension (easy)

**Tags:** periodicity, row-wise, same_size

**Written rule:** Whenever a row contains exactly two matching nonzero seeds with only zeros between them, treat their spacing as a period and keep placing that color to the right by the same step.

**Program:** `solve_easy_p01`

**Primitives:** `periodic_ray`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0
0 0 0 8 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 3 0 0 3
0 0 0 8 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 4 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 2 0 0 2 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 7 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 4 0 0 4 0 0 4 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
6 0 0 6 0 0 6 0 0 6
0 0 9 0 9 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 3
```

### Test pairs

#### Test 1 input
```text
0 4 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 4 0 4 0 4 0 4 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 8 0 0 0 8
```

## easy_p02 — Midpoint of a Clear Segment (easy)

**Tags:** midpoint, line-logic, same_size

**Written rule:** If two matching cells lie on the same row or column with a clear zero segment between them and a single central cell, fill just that midpoint.

**Program:** `solve_easy_p02`

**Primitives:** `segment_midpoint`

### Train pairs

#### Train 1 input
```text
0 0 0 0 3 0 0
0 2 0 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 3 0 0
6 0 0 0 6 0 0
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 3 0 0
0 2 0 2 0 2 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
0 0 0 0 3 0 0
6 0 6 0 6 0 0
0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0
4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0
4 0 0 4 0 0 4 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 3
```

#### Train 3 output
```text
0 0 5 0 5 0 5 0 0
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3
0 9 0 0 9 0 0 9 0
0 0 0 0 0 0 0 0 3
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 4
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0
```

#### Test 1 output
```text
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
4 0 0 0 4 0 0 0 4
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 7 0 0
```

## easy_p03 — Distance-Two Diamond Shell (easy)

**Tags:** distance, morphology, same_size

**Written rule:** Each seed keeps itself and paints every empty cell at Manhattan distance exactly 2 with the same color.

**Program:** `solve_easy_p03`

**Primitives:** `distance_band`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 3 0 0 0 0
0 3 0 3 0 0 0
3 0 3 0 3 6 0
0 3 0 3 6 0 6
0 0 3 6 0 6 0
0 0 0 0 6 0 6
0 0 0 0 0 6 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 2 0 2 0
0 0 0 2 0 2 0 2
0 0 0 0 2 0 2 0
0 7 0 0 0 2 0 0
7 0 7 0 0 0 0 0
0 7 0 7 0 0 0 0
7 0 7 0 0 0 0 0
0 7 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 4 0 0 0 0 0 0 0
4 0 4 0 0 0 8 0 0
0 4 0 4 0 8 0 8 0
4 0 4 0 8 0 8 0 8
0 4 0 0 0 8 0 8 0
0 0 0 0 0 0 8 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 5 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0
5 0 5 0 5 0 0 0 0
0 5 0 5 0 0 9 0 0
0 0 5 0 0 9 0 9 0
0 0 0 0 9 0 9 0 9
0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 9 0 0
```

## easy_p04 — Bounding-Box Corners Only (easy)

**Tags:** objects, bbox, same_size

**Written rule:** Erase each connected object and keep only the four corners of its bounding box, in the object’s original color.

**Program:** `solve_easy_p04`

**Primitives:** `bbox_corners`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 3 3 0 0 7 7 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 3 0 0 7 0 7 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
2 0 2 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 9 9 0
0 5 5 5 0 0 0 0 0 9 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 9 0 9 0
0 5 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 6 6 0 0 0 3 3 0 0
0 0 6 0 0 0 3 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p05 — Complete the Main Diagonal (easy)

**Tags:** diagonal, projection, same_size

**Written rule:** Every seed fills the entire ↘ diagonal it lies on; all cells with the same row-minus-column value become that seed’s color.

**Program:** `solve_easy_p05`

**Primitives:** `diagonal_line`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 6 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 2 0 0 0 0
0 0 0 2 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 2 0
6 0 0 0 0 0 2
0 6 0 0 0 0 0
0 0 6 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 0
3 0 0 0 0 0 0 0 7
0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 8 0 0 0
5 0 0 0 0 0 0 8 0 0
0 5 0 0 0 0 0 0 8 0
0 0 5 0 0 0 0 0 0 8
0 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 9 0
4 0 0 0 0 0 0 0 9
0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0
```

## easy_p06 — Row Leader Recolor (easy)

**Tags:** row-control, recolor, same_size

**Written rule:** In each row, the leftmost nonzero cell chooses the row’s leader color; recolor every nonzero cell in that row to that leader.

**Program:** `solve_easy_p06`

**Primitives:** `row_leader_recolor`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0
3 0 5 0 7 0
0 0 0 0 0 0
2 4 0 6 0 8
0 9 0 9 9 0
```

#### Train 1 output
```text
0 0 0 0 0 0
3 0 3 0 3 0
0 0 0 0 0 0
2 2 0 2 0 2
0 9 0 9 9 0
```

#### Train 2 input
```text
4 0 2 2 0 0 7
0 0 0 0 0 0 0
6 0 0 3 0 3 0
0 5 5 0 1 0 1
```

#### Train 2 output
```text
4 0 4 4 0 0 4
0 0 0 0 0 0 0
6 0 0 6 0 6 0
0 5 5 0 5 0 5
```

#### Train 3 input
```text
0 8 0 4 0 4
9 0 7 0 7 7
0 0 0 0 0 0
3 1 1 0 2 0
```

#### Train 3 output
```text
0 8 0 8 0 8
9 0 9 0 9 9
0 0 0 0 0 0
3 3 3 0 3 0
```

### Test pairs

#### Test 1 input
```text
5 0 1 1 0 7 0
0 0 0 0 0 0 0
2 3 0 4 4 0 9
0 6 0 6 0 8 8
```

#### Test 1 output
```text
5 0 5 5 0 5 0
0 0 0 0 0 0 0
2 2 0 2 2 0 2
0 6 0 6 0 6 6
```

## easy_p07 — Opposite Pair Fill (easy)

**Tags:** local, gap-fill, same_size

**Written rule:** Any zero cell between matching opposite neighbors becomes that color: left/right matches fill horizontally and up/down matches fill vertically.

**Program:** `solve_easy_p07`

**Primitives:** `opposite_pair_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 5 0
```

#### Train 2 input
```text
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 9 0 9 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 9 9 9 0 0 4 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 6 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 6 6 6 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
```

#### Test 1 output
```text
0 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 7 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7 0
```

## medium_p01 — Fill Each Seeded Room (medium)

**Tags:** flood-fill, walls, same_size

**Written rule:** Walls are color 5. Each non-wall seed floods all zero cells in its own room without crossing walls.

**Program:** `solve_medium_p01`

**Primitives:** `room_flood`

### Train pairs

#### Train 1 input
```text
5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5
5 0 2 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 3 0 5
5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5
```

#### Train 1 output
```text
5 5 5 5 5 5 5 5 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 2 2 2 5 3 3 3 5
5 5 5 5 5 5 5 5 5
```

#### Train 2 input
```text
5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 4 0 5
5 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 0 0 5
5 0 6 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

#### Train 2 output
```text
5 5 5 5 5 5 5 5 5 5
5 4 4 4 4 4 4 4 4 5
5 4 4 4 4 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5
5 6 6 6 6 6 6 6 6 5
5 6 6 6 6 6 6 6 6 5
5 6 6 6 6 6 6 6 6 5
5 5 5 5 5 5 5 5 5 5
```

#### Train 3 input
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 7 0 0 5 0 0 3 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 9 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Train 3 output
```text
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 3 3 3 3 5
5 7 7 7 7 5 3 3 3 3 5
5 7 7 7 7 5 3 3 3 3 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 9 9 9 9 5
5 0 0 0 0 5 9 9 9 9 5
5 0 0 0 0 5 9 9 9 9 5
5 5 5 5 5 5 5 5 5 5 5
```

### Test pairs

#### Test 1 input
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 5 0 0 0 8 0 0 5
5 2 0 5 0 0 0 0 0 0 5
5 0 0 5 0 0 0 0 0 0 5
5 0 0 5 5 5 5 5 5 5 5
5 0 0 5 0 0 0 0 0 0 5
5 0 0 5 0 0 0 0 4 0 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Test 1 output
```text
5 5 5 5 5 5 5 5 5 5 5
5 2 2 5 8 8 8 8 8 8 5
5 2 2 5 8 8 8 8 8 8 5
5 2 2 5 8 8 8 8 8 8 5
5 2 2 5 5 5 5 5 5 5 5
5 2 2 5 4 4 4 4 4 4 5
5 2 2 5 4 4 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5 5
```

## medium_p02 — Column Height Summary (medium)

**Tags:** summary, column-profile, resize

**Written rule:** Crop the only object, count how many filled cells each column of its bounding box contains, and turn those counts into bottom-aligned bars of the same color.

**Program:** `solve_medium_p02`

**Primitives:** `column_histogram`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0
0 0 3 3 3 0 0 0
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
3 0 0
3 0 3
3 3 3
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 7 0 0
0 0 0 0 7 7 7 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 7 0 0
0 7 0 7
7 7 7 7
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
2 2 2
2 2 2
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0
0 0 6 0 6 6 0 0 0
0 0 6 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 0 0 0
6 0 6 6
6 6 6 6
```

## medium_p03 — Apply the Transform Script (medium)

**Tags:** transforms, script, resize

**Written rule:** Read the nonzero codes in the top row from left to right and apply those transforms to the cropped object below: 1=rotate 90° clockwise, 2=flip horizontally, 3=rotate 180°, 4=flip vertically.

**Program:** `solve_medium_p03`

**Primitives:** `transform_script`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 7 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 7 7
0 7 0
7 7 0
```

#### Train 2 input
```text
2 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 0
4 4 4
0 0 4
```

#### Train 3 input
```text
3 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0
0 0 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
8 8
8 8
0 8
```

### Test pairs

#### Test 1 input
```text
1 2 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 6 6 6 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 6 0
0 6 6
6 6 0
```

## medium_p04 — Orthogonal Contact Shell (medium)

**Tags:** morphology, objects, same_size

**Written rule:** Erase each object and keep only the empty cells one orthogonal step outside it, colored like the object that touches them.

**Program:** `solve_medium_p04`

**Primitives:** `contact_shell`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 7 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
3 0 3 0 0 0 7 0 0 0
3 0 0 3 0 7 0 7 0 0
0 3 3 0 0 7 0 0 7 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 4 4 4 0 0 0 0 0
4 0 0 0 4 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 4 0 0 0 8 0 0
0 0 0 0 0 8 0 8 0
0 0 0 0 0 8 0 8 0
0 0 0 0 8 0 0 8 0
0 0 0 0 0 8 8 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0
0 0 6 0 0 6 2 2 0 0
0 0 0 6 6 2 0 0 2 0
0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 9 9 0 0
0 0 0 0 0 9 0 0 0 9 0
0 0 0 0 0 0 9 9 0 9 0
0 5 0 0 0 0 0 0 9 0 0
5 0 5 0 0 0 0 0 0 0 0
5 0 0 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## medium_p05 — Offset Transfer Between Anchors (medium)

**Tags:** relative-position, anchors, same_size

**Written rule:** Color 1 is the source anchor and color 2 is the target anchor. Copy every payload cell’s offset from the source anchor over to the target anchor, and keep only the transferred payload plus the target anchor.

**Program:** `solve_medium_p05`

**Primitives:** `offset_transfer`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 1 4 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 2 4 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 1 0 6 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 2 0 6
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 9 0 1 0 0 0 0 2 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 2 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 1 0 6 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 2 0 6
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## medium_p06 — Pivot Cross Until Walls (medium)

**Tags:** rays, walls, same_size

**Written rule:** Every non-wall seed sends rays up, down, left, and right through zeros until a wall or another occupied cell blocks the ray.

**Program:** `solve_medium_p06`

**Primitives:** `pivot_rays`

### Train pairs

#### Train 1 input
```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 2 0 5 0 7 0 0
0 0 2 0 5 0 7 0 0
0 0 2 0 5 0 7 0 0
2 2 2 2 2 2 7 2 2
0 0 2 0 0 0 7 0 0
0 5 5 5 0 0 7 0 0
7 7 7 7 7 7 7 7 7
0 0 0 0 0 0 7 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 4 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 4 0 0 0 0 0 0
0 0 4 0 0 5 0 0 0
4 4 4 4 4 5 0 0 0
0 0 4 0 0 3 0 0 0
5 5 5 0 0 3 5 5 5
0 0 0 0 0 3 0 0 0
3 3 3 3 3 3 3 3 3
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 8 0 0 0 0 5 6 0
0 0 8 0 0 0 0 5 6 0
0 0 8 0 0 0 0 5 6 0
0 0 8 0 0 0 0 5 6 0
8 8 8 8 8 8 8 8 6 8
0 0 8 0 5 5 5 0 6 0
6 6 6 6 6 6 6 6 6 6
0 0 8 0 0 0 0 0 6 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 9 0 0 0 5 0 0 4 0 0
0 9 0 0 0 5 0 0 4 0 0
0 9 0 0 0 5 0 0 4 0 0
0 9 0 0 0 5 0 0 4 0 0
9 9 9 9 9 9 9 9 4 9 9
0 9 0 0 0 0 0 0 4 0 0
0 9 5 5 5 5 0 0 4 0 0
4 4 4 4 4 4 4 4 4 4 4
0 9 0 0 0 0 0 0 4 0 0
```

## medium_p07 — Frame Interior Gallery (medium)

**Tags:** extraction, frames, gallery

**Written rule:** Find the hollow color-5 frames, take each frame’s interior rectangle exactly as it appears, and concatenate those interiors left-to-right in frame order.

**Program:** `solve_medium_p07`

**Primitives:** `frame_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 5 5 5 5 5 0 0
0 5 2 0 5 0 0 5 0 3 0 5 0 0
0 5 2 2 5 0 0 5 3 3 3 5 0 0
0 5 5 5 5 0 0 5 0 3 0 5 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 0 0 0 3 0
2 2 0 3 3 3
0 0 0 0 3 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 4 0 4 5 0 0 0 5 5 5 5 0 0
0 5 4 4 0 5 0 0 0 5 7 7 5 0 0
0 5 0 4 0 5 0 0 0 5 0 7 5 0 0
0 5 5 5 5 5 0 0 0 5 7 0 5 0 0
0 0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 4 0 7 7
4 4 0 0 0 7
0 4 0 0 7 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 5 5 5 5 0 0 0
0 5 8 0 0 5 0 0 0 5 6 6 5 0 0 0
0 5 8 8 8 5 0 0 0 5 0 6 5 0 0 0
0 5 5 5 5 5 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
8 0 0 0 6 6
8 8 8 0 0 6
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 5 5 5 5 5 0 0 0 0 0
0 5 2 2 5 0 0 5 3 0 3 5 0 0 5 5 5
0 5 0 2 5 0 0 5 0 3 0 5 0 0 5 4 5
0 5 2 0 5 0 0 5 5 5 5 5 0 0 5 4 5
0 5 5 5 5 0 0 0 0 0 0 0 0 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
2 2 0 3 0 3 0 4
0 2 0 0 3 0 0 4
2 0 0 0 0 0 0 0
```

## hard_p01 — Keyed Frame Embedding (hard)

**Tags:** matching, frames, insertion

**Written rule:** Each color-5 frame has a key marker directly above its top edge. Find the source object of that key color elsewhere in the grid, crop it, and center it inside the matching frame. Remove the markers and source objects outside the frames.

**Program:** `solve_hard_p01`

**Primitives:** `keyed_frame_embed`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 7 0 0 0 0
0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 2 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 5 0 2 0 0 5 0 0 5 7 0 0 0 5 0
0 5 0 2 2 0 5 0 0 5 7 7 7 0 5 0
0 5 0 0 0 0 5 0 0 5 0 0 7 0 5 0
0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 8 0 0 0 0
0 0 5 0 0 0 0 5 0 0 5 5 5 5 5 5 0
0 0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 3 3 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 3 3 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 5 0 0 5 5 5 5 5 5 0
0 0 5 3 3 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 3 3 0 5 0 0 5 0 8 8 0 5 0
0 0 5 0 0 0 0 5 0 0 5 0 8 8 0 5 0
0 0 5 0 0 0 0 5 0 0 5 0 8 0 0 5 0
0 0 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 9 0 0 0 0
0 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 0 5 5 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 0 0 0 9 9 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 9 9 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 5 0 0 0 0 5 0 0 0 5 0 9 9 0 0 5 0
0 5 0 4 0 0 5 0 0 0 5 0 0 9 0 0 5 0
0 5 0 4 0 0 5 0 0 0 5 0 0 9 9 0 5 0
0 5 0 4 4 0 5 0 0 0 5 0 0 0 0 0 5 0
0 5 0 0 0 0 5 0 0 0 5 5 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 3 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 6 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 6 6 6 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 6 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 0 6 6 6 0 5 0 0 5 0 3 0 0 5 0
0 0 5 0 0 0 6 0 5 0 0 5 0 3 3 0 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p02 — Portal Shortest Path (hard)

**Tags:** pathfinding, portals, same_size

**Written rule:** Find the shortest path from 2 to 3 without crossing walls 5. Portal colors come in matched pairs, and stepping onto one portal lets the path jump to its partner. Paint the traversed empty cells with 8.

**Program:** `solve_hard_p02`

**Primitives:** `portal_bfs`

### Train pairs

#### Train 1 input
```text
5 0 5 5 5 5 5 5 5 5 5
0 4 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 0 0 0 0 3 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 4 0
5 5 5 5 5 5 5 5 5 0 5
```

#### Train 1 output
```text
5 0 5 5 5 5 5 5 5 5 5
0 4 0 0 0 5 0 0 0 0 0
0 8 0 0 0 5 0 0 0 0 0
0 8 0 0 0 5 0 0 0 0 0
0 2 0 0 0 0 0 0 0 3 0
0 0 0 0 0 5 0 0 0 8 0
0 0 0 0 0 5 0 0 0 8 0
0 0 0 0 0 5 0 0 0 4 0
5 5 5 5 5 5 5 5 5 0 5
```

#### Train 2 input
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 6 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
5 5 0 5 5 5 5 5 5 0 5 5
0 0 0 0 0 0 5 0 0 6 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 3 0
0 0 0 0 0 0 5 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 8 0 0 0 0 5 0 0 0 0 0
0 8 6 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
5 5 0 5 5 5 5 5 5 0 5 5
0 0 0 0 0 0 5 0 0 6 0 0
0 0 0 0 0 0 5 0 0 8 0 0
0 0 0 0 0 4 0 0 0 8 3 0
0 0 0 0 0 0 5 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 5 6 0 0 0
0 2 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 5 0 0 0 0
5 0 5 5 5 5 5 5 5 5 5 0 5
0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 3 0
0 0 0 6 5 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 5 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 5 6 0 0 0
0 2 0 0 0 0 0 0 5 8 0 0 0
0 8 0 0 5 0 0 0 5 8 8 8 0
5 8 5 5 5 5 5 5 5 5 5 8 5
0 8 0 0 5 0 0 0 5 0 0 8 0
0 8 0 0 5 0 0 0 0 0 0 3 0
0 8 8 6 5 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 5 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 5 0 0 0 5 0 0 0
0 2 0 0 0 5 0 0 0 5 6 0 0
0 0 0 0 0 5 0 4 0 0 0 0 0
5 0 5 5 5 5 5 5 5 5 5 0 5
0 0 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 5 0 0 0
0 0 4 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 5 6 0 0 5 0 3 0
0 0 0 0 0 5 0 0 0 5 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 5 0 0 0 5 0 0 0
0 2 0 0 0 5 0 0 0 5 6 0 0
0 8 0 0 0 5 0 4 8 8 8 8 0
5 8 5 5 5 5 5 5 5 5 5 8 5
0 8 0 0 0 5 0 0 0 5 0 8 0
0 8 0 0 0 5 0 0 0 5 0 8 0
0 8 0 0 0 5 0 0 0 5 0 8 0
0 8 4 0 0 0 0 0 0 5 0 8 0
0 0 0 0 0 5 6 0 0 5 0 3 0
0 0 0 0 0 5 0 0 0 5 0 0 0
```

## hard_p03 — Radial Order Gallery (hard)

**Tags:** sorting, objects, gallery

**Written rule:** Use the hub marker 9 as the center. Sort the surrounding objects by the angle of their centroids, starting from straight up and moving clockwise, then pack the cropped objects into a left-to-right gallery.

**Program:** `solve_hard_p03`

**Primitives:** `radial_order_pack`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 4 0 0
0 0 8 0 0 0 9 0 0 4 0 0
0 8 8 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 0 0 7 7 7 0 0 8 0 2 0
4 0 0 0 7 0 0 0 8 0 2 2
4 4 0 0 0 0 0 8 8 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 9 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
3 3 0 5 5 0 0 6 0 0
3 3 0 0 5 0 0 6 6 6
3 0 0 0 5 5 0 0 0 6
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 9 0 0 0 2 2 0
0 0 0 0 6 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
4 4 4 0 2 2 0 0 8 0 0 6 0 0
0 4 0 0 0 2 2 0 8 0 0 6 6 6
0 0 0 0 0 0 0 0 8 8 0 0 0 6
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 9 0 0 0 2 2 0
0 0 3 3 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
5 0 0 2 2 0 0 7 7 0 0 3
5 5 0 0 2 0 0 7 7 0 0 3
0 0 0 0 2 2 0 7 0 0 3 3
```

## hard_p04 — Transform Timeline Gallery (hard)

**Tags:** transforms, sequence, gallery

**Written rule:** Read the top-row transform codes and emit a gallery of the object’s states: the original crop first, then the result after each code is applied in order.

**Program:** `solve_hard_p04`

**Primitives:** `transform_timeline`

### Train pairs

#### Train 1 input
```text
1 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
7 0 0 0 0 7 7 0 7 7 0
7 7 7 0 0 7 0 0 0 7 0
0 0 7 0 7 7 0 0 0 7 7
```

#### Train 2 input
```text
4 1 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 5 0 0 0 5 5 0 5 0 0 0 5 0 0
0 5 0 0 0 5 0 0 5 5 5 0 5 5 5
0 5 5 0 5 5 0 0 0 0 5 0 0 0 5
```

#### Train 3 input
```text
2 1 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
8 8 0 8 8 0 0 8 8 0 8 8 0
8 8 0 8 8 0 8 8 8 0 8 8 8
8 0 0 0 8 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
1 4 2 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 6 0 0 6 6 0 0 0 6 0 0 0 6 0 0 6 6 0
6 6 6 0 0 6 6 0 0 6 6 0 6 6 0 0 0 6 6
6 0 0 0 0 6 0 0 6 6 0 0 0 6 6 0 0 6 0
```

## hard_p05 — Flood Through Matching Gates (hard)

**Tags:** flood-fill, gates, same_size

**Written rule:** Walls are 5. A seed may flood through zeros and through gate cells that share its own color, but all other wall cells and foreign-color gates remain blocked.

**Program:** `solve_hard_p05`

**Primitives:** `gated_flood`

### Train pairs

#### Train 1 input
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 0 0 0 5
5 0 2 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 5
5 5 5 2 5 5 5 3 5 5 5
5 0 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 3 0 5
5 0 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Train 1 output
```text
5 5 5 5 5 5 5 5 5 5 5
5 2 2 2 2 2 2 2 2 2 5
5 2 2 2 2 2 2 2 2 2 5
5 2 2 2 2 2 2 2 2 2 5
5 5 5 2 5 5 5 3 5 5 5
5 2 2 2 2 2 2 2 2 2 5
5 2 2 2 2 2 2 2 3 2 5
5 2 2 2 2 2 2 2 2 2 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Train 2 input
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 4 0 0 0 0 0 5
5 0 4 0 0 5 0 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 5 0 0 6 0 0 5
5 0 0 0 0 6 0 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
```

#### Train 2 output
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 4 4 4 4 5 4 4 4 4 4 5
5 4 4 4 4 4 4 4 4 4 4 5
5 4 4 4 4 5 4 4 4 4 4 5
5 4 4 4 4 5 4 4 4 4 4 5
5 4 4 4 4 5 4 4 4 4 4 5
5 4 4 4 4 5 4 4 6 4 4 5
5 4 4 4 4 6 4 4 4 4 4 5
5 4 4 4 4 5 4 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5 5 5
```

#### Train 3 input
```text
5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 7 0 0 0 0 0 5
5 0 7 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 5 7 5 5 5 5 5 5 5 3 5 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 0 5 0 0 0 3 0 5
5 0 0 0 0 0 3 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

#### Train 3 output
```text
5 5 5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 7 7 7 7 7 7 7 5
5 7 7 7 7 7 5 7 7 7 7 7 5
5 7 7 7 7 7 5 7 7 7 7 7 5
5 5 7 5 5 5 5 5 5 5 3 5 5
5 7 7 7 7 7 5 3 3 3 3 3 5
5 7 7 7 7 7 5 3 3 3 3 3 5
5 7 7 7 7 7 3 3 3 3 3 3 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

### Test pairs

#### Test 1 input
```text
5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 0 2 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 0 2 0 0 0 0 0 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 5 5 5 2 5 5 5 9 5 5 5 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 0 0 0 0 0 9 0 0 0 9 0 5
5 0 0 0 0 0 5 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

#### Test 1 output
```text
5 5 5 5 5 5 5 5 5 5 5 5 5
5 2 2 2 2 2 5 2 2 2 2 2 5
5 2 2 2 2 2 5 2 2 2 2 2 5
5 2 2 2 2 2 2 2 2 2 2 2 5
5 2 2 2 2 2 5 2 2 2 2 2 5
5 5 5 5 2 5 5 5 9 5 5 5 5
5 2 2 2 2 2 5 9 9 9 9 9 5
5 2 2 2 2 2 9 9 9 9 9 9 5
5 2 2 2 2 2 5 9 9 9 9 9 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

## hard_p06 — Choose the Dihedral Match (hard)

**Tags:** matching, rotation-reflection, resize

**Written rule:** The color-1 guide names a shape. Among the other candidates, exactly one matches that guide under some rotation or reflection. Output the matching candidate transformed into the guide’s orientation, using the candidate’s own color.

**Program:** `solve_hard_p06`

**Primitives:** `dihedral_select`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 2 0 0 0 0
0 1 1 1 0 0 0 2 2 2 0 0 0 0
0 0 0 1 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 7 7 7 0 0 0 0 0 4 0 0 0
0 0 0 7 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 0 0
2 2 2
0 0 2
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 3 3 0 0 0 0 0
0 0 1 0 0 0 0 0 0 3 0 0 0 0 0
0 0 1 1 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 6 6 0 0 0 0
0 0 8 8 8 0 0 0 0 6 6 0 0 0 0
0 0 0 0 8 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
3 3 0
0 3 0
0 3 3
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 5 0 0 0 0
0 0 1 1 1 0 0 0 0 5 5 5 0 0 0
0 0 1 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 7 7 0 0 0
0 0 4 4 0 0 0 0 0 0 0 7 7 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 5 0
5 5 5
5 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 6 6 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 0 0
6 6 6
0 0 6
```

## hard_p07 — Parity Wavefront Fill (hard)

**Tags:** distance, parity, same_size

**Written rule:** Flood from the seed through all non-wall cells. Reachable zeros at even distance take the seed’s color; reachable zeros at odd distance become color 8.

**Program:** `solve_hard_p07`

**Primitives:** `parity_wavefront`

### Train pairs

#### Train 1 input
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 0 0 0 5
5 0 3 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 5
5 0 5 5 5 5 5 5 5 0 5
5 0 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Train 1 output
```text
5 5 5 5 5 5 5 5 5 5 5
5 3 8 3 8 3 8 3 8 3 5
5 8 3 8 3 8 3 8 3 8 5
5 3 8 3 8 3 8 3 8 3 5
5 8 5 5 5 5 5 5 5 8 5
5 3 8 3 8 3 8 3 8 3 5
5 8 3 8 3 8 3 8 3 8 5
5 3 8 3 8 3 8 3 8 3 5
5 5 5 5 5 5 5 5 5 5 5
```

#### Train 2 input
```text
5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 0 6 0 0 5 0 0 0 5
5 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

#### Train 2 output
```text
5 5 5 5 5 5 5 5 5 5
5 8 6 8 6 8 6 8 6 5
5 6 8 6 8 5 8 6 8 5
5 8 6 8 6 5 6 8 6 5
5 6 8 6 8 5 8 6 8 5
5 8 6 8 6 5 6 8 6 5
5 6 8 6 8 5 8 6 8 5
5 8 6 8 6 5 6 8 6 5
5 6 8 6 8 6 8 6 8 5
5 5 5 5 5 5 5 5 5 5
```

#### Train 3 input
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 0 4 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 0 5
5 0 0 5 5 5 5 5 5 5 0 5
5 0 0 0 0 0 0 5 0 0 0 5
5 0 0 0 0 0 0 5 0 0 0 5
5 0 0 0 0 0 0 5 0 0 0 5
5 0 0 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
```

#### Train 3 output
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 8 4 8 4 8 4 8 4 8 4 5
5 4 8 4 8 4 8 4 8 4 8 5
5 8 4 5 5 5 5 5 5 5 4 5
5 4 8 4 8 4 8 5 8 4 8 5
5 8 4 8 4 8 4 5 4 8 4 5
5 4 8 4 8 4 8 5 8 4 8 5
5 8 4 8 4 8 4 5 4 8 4 5
5 5 5 5 5 5 5 5 5 5 5 5
```

### Test pairs

#### Test 1 input
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 0 0 0 5
5 0 7 0 0 0 5 0 0 0 0 5
5 0 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 0 5 0 0 0 0 5
5 0 5 5 5 5 5 5 5 5 0 5
5 0 0 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
```

#### Test 1 output
```text
5 5 5 5 5 5 5 5 5 5 5 5
5 7 8 7 8 7 5 7 8 7 8 5
5 8 7 8 7 8 5 8 7 8 7 5
5 7 8 7 8 7 5 7 8 7 8 5
5 8 7 8 7 8 5 8 7 8 7 5
5 7 5 5 5 5 5 5 5 5 8 5
5 8 7 8 7 8 7 8 7 8 7 5
5 7 8 7 8 7 8 7 8 7 8 5
5 8 7 8 7 8 7 8 7 8 7 5
5 5 5 5 5 5 5 5 5 5 5 5
```
