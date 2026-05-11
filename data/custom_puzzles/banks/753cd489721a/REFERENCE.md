# ARC Puzzle Bank — Set 23


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `diag_agreement_fill`: Fill an empty cell when its four diagonal neighbors all share one nonzero color.
- `right_shadow_cast`: Cast each seed color rightward through empty cells until a blocker or the border.
- `cross_core_filter`: Keep only cells that have same-color neighbors in all four cardinal directions.
- `exact_two_gap_bridge`: Bridge same-color endpoints separated by exactly two empty cells in a row or column.
- `square_corner_bloom`: For every solid monochrome 2x2 block, bloom one same-color cell on each diagonal corner.
- `knight_bloom`: Around each isolated seed, stamp the eight knight-move positions with the seed color.
- `barbell_fill`: When two same-color 2x2 blocks align, fill the rectangle that connects them.
- `border_touch_rank`: Recolor each object by how many outer borders it touches.
- `compartment_gravity`: Let colored cells fall within each wall-bounded vertical compartment.
- `pair_bbox_fill`: For each color appearing exactly twice as markers, fill the rectangle spanning the pair.
- `count_key_crop`: Use the count of top-row key markers to select the left-to-right object to crop out.
- `nearest_corner_dock`: Move the single object to the geometrically nearest corner of the same canvas.
- `largest_mirror_crop`: Select the largest object, mirror its tight crop left-to-right, and output only that crop.
- `height_gallery`: Crop objects and lay them out left-to-right, bottom-aligned, sorted by height.
- `mirror_laser`: Trace a border-launched laser through slash and backslash mirrors until it exits or hits a wall.
- `dual_key_door_bfs`: Find the shortest path to the goal while collecting up to two keys that unlock matching doors.
- `visibility_matrix`: Output a matrix showing which objects have unobstructed orthogonal line-of-sight.
- `area_rank_frame_assign`: Assign cropped objects to hollow frames by matching object-area rank to frame-area rank.
- `dual_key_boolean`: Transform one normalized object by a key, then combine it with another via a keyed boolean op.
- `orbit_stamp`: Stamp four rotated copies of a template around an anchor point on the diagonals.
- `frame_key_stamp`: Stamp a template into each frame after applying the transform indicated by that frame's key.

## easy_p01 — Diagonal Agreement Fill (easy)

**Tags:** local, diagonal, completion

**Written rule:** Fill any 0 cell whose four diagonal neighbors all share the same nonzero color. Leave everything else unchanged.

**Program:** `solve_easy_p01`

**Primitives:** `diag_agreement_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 4 0 7 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 0 4 0 7 0 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 3 0 0
0 0 0 0 3 0 3 0
0 8 0 8 0 0 0 0
0 0 8 0 0 0 0 0
0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 6 0 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0
0 6 0 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 6 0 6 0 2 0 2 0
0 0 6 0 0 0 2 0 0
0 6 0 6 0 2 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 7 0 7 0 0 0 4 0 0
0 0 7 0 0 0 4 0 4 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p02 — Rightward Shadow Cast (easy)

**Tags:** local, beam, same_size

**Written rule:** In each row, every nonzero cell paints its own color rightward through consecutive empty cells, stopping just before the next nonzero cell or the border.

**Program:** `solve_easy_p02`

**Primitives:** `right_shadow_cast`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 2 0 0 0 7
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 6 6 6
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 2 2 2 2 7
0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 5 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 5 5 5 5 3 3 3
0 0 0 0 0 0 0 0 0
0 7 7 7 4 4 4 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 6
0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 1 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
9 9 9 9 1 1 1 1 1 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 6 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 4 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 2 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 4 4 4 4 4 4 4 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 2 2 2 2 9 9
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p03 — Cross-Core Filter (easy)

**Tags:** local, topology, filter

**Written rule:** Keep only the cells that have same-color neighbors directly above, below, left, and right. Turn every other cell to 0.

**Program:** `solve_easy_p03`

**Primitives:** `cross_core_filter`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 8 0
0 4 4 4 0 0 0 8 0
0 0 4 0 0 0 0 8 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 7 0 0
0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 5 0 0
0 6 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 9 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0
0 0 0 9 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 8 0 0 0 0 0
0 6 6 8 8 8 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 2 2 0
0 0 4 4 4 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 7 0 0
0 0 6 6 0 0 0 7 7 7 0
0 0 0 6 0 0 0 0 7 0 0
5 5 0 0 0 0 0 0 0 0 0
0 5 0 0 3 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## easy_p04 — Exact Two-Gap Bridge (easy)

**Tags:** local, interval, same_size

**Written rule:** Whenever two same-color cells in one row or one column are separated by exactly two empty cells, fill those two empty cells with that color.

**Program:** `solve_easy_p04`

**Primitives:** `exact_two_gap_bridge`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 7 0
0 0 9 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 7 7 5 7 0
0 0 9 0 0 0 0 5 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
```

#### Train 2 input
```text
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 6 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0
0 0 0 0 0 8 0 0 0
```

#### Train 2 output
```text
4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
4 0 0 6 6 6 6 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0
0 2 2 2 2 8 0 0 0
0 0 0 0 0 8 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 9 0 0 0 0
5 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 9 0 0 0 0
5 5 5 5 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
6 8 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
6 0 0 0 0 0 0 0 0 7 0 0
6 0 0 0 0 0 0 0 0 7 0 0
6 0 0 0 0 0 0 0 0 7 0 0
6 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p05 — Square Corner Bloom (easy)

**Tags:** local, shape, same_size

**Written rule:** For every solid monochrome 2x2 block, add one same-color cell on each of its four diagonal corners when those cells are inside the grid.

**Program:** `solve_easy_p05`

**Primitives:** `square_corner_bloom`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 0 0 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
4 0 0 4 0 7 0 0 7 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 7 0 0 7 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0 0
8 0 0 3 0 0 3 0 0
0 8 8 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0
8 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
9 0 0 9 0 5 0 0 5 0
0 9 9 0 0 0 0 0 0 0
0 9 9 2 0 0 2 0 0 0
9 0 0 9 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 2 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0
0 8 8 0 0 0 0 4 4 0 0
0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 6 0 0 6 0 4 0 0 4 0
8 0 0 8 0 0 0 4 4 0 0
0 8 8 0 0 0 0 4 4 0 0
0 8 8 0 0 0 4 0 0 4 0
8 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## easy_p06 — Knight Bloom (easy)

**Tags:** offset, local, same_size

**Written rule:** Each isolated nonzero seed keeps its own cell and also paints the eight knight-move positions around it with the same color.

**Program:** `solve_easy_p06`

**Primitives:** `knight_bloom`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 4 0 4 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 0 0 0
0 4 0 4 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 7 0 7 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 5 0 0
0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0 5 0
0 9 0 9 0 5 0 5 0 0
9 0 0 0 9 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
9 0 0 0 9 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 6 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 6 0 0 0 6 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0
0 0 8 0 8 0 0 0 2 0 2 0
0 0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p07 — Barbell Rectangle Fill (easy)

**Tags:** shape, completion, same_size

**Written rule:** Whenever two same-color solid 2x2 blocks line up in the same rows or the same columns, fill the full rectangle that connects them.

**Program:** `solve_easy_p07`

**Primitives:** `barbell_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 4 4 0 0 0 4 4 0 7 7 0
0 4 4 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 4 4 4 4 4 4 4 0 7 7 0
0 4 4 4 4 4 4 4 0 7 7 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 8 8 0 8 8
0 0 0 0 0 8 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 8 8 8 8 8
0 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 6 6 0 0
0 0 6 6 0 2 2 6 6 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 5 5 0 0
0 0 5 5 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 3 3 0 3 3 0
0 0 0 0 0 0 3 3 0 3 3 0
9 9 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 5 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 3 3 3 3 3 0
9 9 0 0 0 0 3 3 3 3 3 0
9 9 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0
```

## medium_p01 — Border-Touch Rank Recolor (medium)

**Tags:** object, classification, same_size

**Written rule:** Find each connected object and recolor the whole object by how many outer borders it touches: 0 borders -> 1, 1 border -> 2, 2 borders -> 3, and 3 or 4 borders -> 4.

**Program:** `solve_medium_p01`

**Primitives:** `border_touch_rank`

### Train pairs

#### Train 1 input
```text
0 0 4 0 0 0 0 3 0 0
0 0 4 0 0 0 0 3 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 7 7 0 0 0 0
0 0 4 0 7 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
9 0 4 0 0 0 0 0 0 0
9 9 4 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 3 0 0 0 0 2 0 0
0 0 3 0 0 0 0 2 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 1 1 0 0 0 0
0 0 3 0 1 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
```

#### Train 2 input
```text
5 5 0 0 0 0 2 0 0
5 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 6
0 0 0 0 0 0 2 0 6
0 0 0 0 8 8 2 0 6
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0
```

#### Train 2 output
```text
3 3 0 0 0 0 3 0 0
3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 2
0 0 0 0 0 0 3 0 2
0 0 0 0 1 1 3 0 2
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0
```

#### Train 3 input
```text
4 4 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 3 0 0 0 0
4 0 0 0 0 3 3 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 7 7 0 0 0 0 0
```

#### Train 3 output
```text
4 4 0 0 0 0 0 0 0 3
4 0 0 0 0 0 0 0 3 3
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 1 0 0 0 0
4 0 0 0 0 1 1 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 2 2 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 4 4 0 0 0 0 0 0 0 2
0 0 4 0 0 0 0 0 0 0 2
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 6 0 0 0 0 0
0 0 4 0 0 6 6 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
9 0 4 0 0 0 0 0 0 0 0
9 9 4 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 3 3 0 0 0 0 0 0 0 3
0 0 3 0 0 0 0 0 0 0 3
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 1 0 0 0 0 0
0 0 3 0 0 1 1 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0
```

## medium_p02 — Compartment Gravity (medium)

**Tags:** physics, walls, same_size

**Written rule:** Treat gray(5) cells as fixed vertical walls. In each column segment between walls, let the nonzero non-wall cells fall downward as far as they can, preserving their top-to-bottom order.

**Program:** `solve_medium_p02`

**Primitives:** `compartment_gravity`

### Train pairs

#### Train 1 input
```text
0 2 0 0 5 3 0 0 0
0 0 0 8 5 3 0 0 0
0 2 0 0 5 0 0 5 7
0 2 0 0 0 0 0 5 0
0 0 0 8 5 3 0 5 7
0 0 0 0 5 0 0 5 0
0 0 0 0 5 0 0 5 0
0 0 0 0 5 0 0 5 0
```

#### Train 1 output
```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0
0 0 0 0 5 0 0 5 0
0 2 0 0 5 3 0 5 0
0 2 0 8 5 3 0 5 7
0 2 0 8 5 3 0 5 7
```

#### Train 2 input
```text
4 0 5 0 0 0 5 0 0 8
0 0 0 0 0 0 5 6 0 0
0 0 5 0 9 0 5 0 0 0
4 0 5 0 0 0 5 6 0 0
0 0 5 0 0 0 0 0 0 0
4 0 5 0 9 0 5 0 0 0
0 0 5 0 9 0 5 0 0 0
0 0 0 0 0 0 5 6 0 0
0 0 5 0 0 0 5 0 0 8
```

#### Train 2 output
```text
0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 5 0 0 0 5 0 0 0
0 0 5 0 0 0 5 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0 0
4 0 5 0 9 0 5 6 0 0
4 0 0 0 9 0 5 6 0 8
4 0 5 0 9 0 5 6 0 8
```

#### Train 3 input
```text
7 5 0 0 0 5 9 0
0 5 0 2 0 5 0 0
7 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0
0 5 0 2 0 5 9 0
0 0 0 0 0 5 0 0
0 5 0 0 0 5 9 0
7 5 0 0 0 5 0 0
0 5 0 2 0 5 0 0
0 5 0 0 0 5 0 0
```

#### Train 3 output
```text
0 5 0 0 0 5 0 0
0 5 0 0 0 5 0 0
0 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0
0 0 0 0 0 5 0 0
0 5 0 0 0 5 0 0
7 5 0 2 0 5 9 0
7 5 0 2 0 5 9 0
7 5 0 2 0 5 9 0
```

### Test pairs

#### Test 1 input
```text
0 4 0 5 0 0 0 5 9 0 0
0 0 0 5 0 6 0 5 0 0 2
0 4 0 0 0 0 0 5 9 0 0
0 0 0 5 0 6 0 5 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 4 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 2
0 0 0 5 0 0 0 5 9 0 0
0 0 0 5 0 6 0 5 0 0 0
```

#### Test 1 output
```text
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 4 0 0 0 6 0 5 9 0 0
0 4 0 5 0 6 0 5 9 0 2
0 4 0 5 0 6 0 5 9 0 2
```

## medium_p03 — Pair Marker Rectangle Fill (medium)

**Tags:** marker, geometry, same_size

**Written rule:** For each color that appears exactly twice as isolated marker cells, fill the full axis-aligned rectangle spanning those two markers with that color.

**Program:** `solve_medium_p03`

**Primitives:** `pair_bbox_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 6 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 6 6 6
0 2 2 2 2 0 0 6 6 6
0 2 2 2 2 0 0 6 6 6
0 2 2 2 2 0 0 6 6 6
0 0 0 0 0 0 0 6 6 6
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7
0 0 4 4 4 4 0 0 0
0 0 4 4 4 4 0 0 0
9 9 9 9 4 4 0 0 0
9 9 9 9 4 4 0 0 0
9 9 9 9 4 4 0 0 0
9 9 9 9 0 0 0 0 0
9 9 9 9 0 0 0 0 0
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5
```

#### Train 3 output
```text
3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 8 0 0
3 3 3 3 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 5 5 5 5 5
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 4 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 4 4 4
0 0 7 7 7 7 7 0 0 4 4 4
0 0 7 7 7 7 7 0 0 4 4 4
0 0 7 7 7 7 7 0 0 4 4 4
0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 0 0 0 0 0 0 0
9 9 9 9 9 0 0 0 0 0 0 0
9 9 9 9 9 0 0 0 0 0 0 0
```

## medium_p04 — Count-Key Object Crop (medium)

**Tags:** selection, crop, marker

**Written rule:** Count the red(2) markers in the top row. Ignore those markers, sort the remaining connected objects from left to right, and output the tight crop of the k-th object.

**Program:** `solve_medium_p04`

**Primitives:** `count_key_crop`

### Train pairs

#### Train 1 input
```text
0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0
0 5 0 0 0 7 7 0 0 8 8
0 5 5 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
7 7
0 7
0 7
```

#### Train 2 input
```text
2 0 2 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 3 0 0 0
0 0 9 0 0 0 0 0 3 0 0 0
0 0 0 0 0 6 0 0 3 3 0 0
0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
3 0
3 0
3 3
```

#### Train 3 input
```text
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 8 0 0 0 0 0
4 4 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
4 0
4 4
```

### Test pairs

#### Test 1 input
```text
0 2 0 2 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 7 7 0 0 0 0 0 0 0
4 4 0 0 7 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 8 0 0 6 6 0
0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 0
6 0
6 6
```

## medium_p05 — Nearest-Corner Dock (medium)

**Tags:** movement, geometry, same_size

**Written rule:** Take the single object, crop it tightly, and place that crop into whichever canvas corner is nearest to the object's current center. The object keeps its shape and color.

**Program:** `solve_medium_p05`

**Primitives:** `nearest_corner_dock`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 8
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## medium_p06 — Largest-Object Mirror Crop (medium)

**Tags:** selection, transform, crop

**Written rule:** Select the largest connected object, crop it tightly, reflect that crop left-to-right, and output only the mirrored crop.

**Program:** `solve_medium_p06`

**Primitives:** `largest_mirror_crop`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 7 0 0 0 0 0 0 4 0 0
0 7 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 7
0 7
7 7
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 3 0
0 8 0 0 0 0 0 0 3 3
0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 8
0 0 8
8 8 8
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 9
0 0 9
9 9 9
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 7 0 0 0 0 0 5 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 7
0 0 7
7 7 7
```

## medium_p07 — Height Gallery (medium)

**Tags:** gallery, object, layout

**Written rule:** Crop every connected object, sort the crops by height from tallest to shortest (breaking ties by width), and lay them out left-to-right on one canvas, bottom-aligned, with a single blank column between crops.

**Program:** `solve_medium_p07`

**Primitives:** `height_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 4 0 0 0 7 7 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
8 0 0 4 0 0 0
8 0 0 4 0 7 0
8 8 0 4 0 7 7
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 6 0 0 0
0 5 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 0 0 0 0 0
5 0 0 0 0 0
5 0 6 0 0 9
5 0 6 6 0 9
```

#### Train 3 input
```text
0 0 0 0 0 0 7 0 0 0 0
0 0 3 0 0 0 7 7 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
8 0 0 3 0 0 0
8 0 0 3 0 7 0
8 8 0 3 0 7 7
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0
4 0 0 0 7 7 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 6 0
4 0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
4 0 0 0 0 0 0 0 0
4 0 9 0 0 0 0 0 0
4 0 9 0 0 7 0 0 6
4 0 9 9 0 7 7 0 6
```

## hard_p01 — Mirror Laser Trace (hard)

**Tags:** beam, simulation, mirrors

**Written rule:** Launch the beam from the single start cell on the border. It travels inward, reflects off / mirrors (3) and \ mirrors (4), stops at walls (5) or when it leaves the grid, and paints every empty traversed cell with 8.

**Program:** `solve_hard_p01`

**Primitives:** `mirror_laser`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 4 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
2 8 8 8 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 2 0 0 0 0 0 0 0
8 8 8 8 8 8 8 4 0 0
0 0 8 0 0 0 0 8 0 0
0 0 4 8 8 8 8 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 8 5 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 4 8 8 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 2 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 8 8 4 0 0
0 0 0 0 0 8 0 0 8 0 0
8 8 8 8 8 8 8 8 3 0 0
0 0 0 0 0 2 0 0 0 0 0
```

## hard_p02 — Dual-Key Door Shortest Path (hard)

**Tags:** pathfinding, stateful, maze

**Written rule:** Travel from the start(2) to the goal(3) by the shortest valid path. Walls are 4. Collect key 5 to open door 6, and key 7 to open door 8. Paint the traversed empty path cells with 9.

**Program:** `solve_hard_p02`

**Primitives:** `dual_key_door_bfs`

### Train pairs

#### Train 1 input
```text
4 4 4 4 4 4 4 4 4 4
4 2 0 0 0 5 0 0 0 4
4 0 4 4 4 4 4 4 4 4
4 0 0 0 0 6 0 0 0 4
4 4 4 4 4 6 4 4 0 4
4 0 0 0 0 0 0 0 3 4
4 4 4 4 4 4 4 4 4 4
```

#### Train 1 output
```text
4 4 4 4 4 4 4 4 4 4
4 2 9 9 9 5 0 0 0 4
4 9 4 4 4 4 4 4 4 4
4 9 9 9 9 6 0 0 0 4
4 4 4 4 4 6 4 4 0 4
4 0 0 0 0 9 9 9 3 4
4 4 4 4 4 4 4 4 4 4
```

#### Train 2 input
```text
4 4 4 4 4 4 4 4 4 4 4 4
4 2 0 0 5 0 6 0 0 4 4 4
4 4 4 4 4 4 4 4 0 4 4 4
4 4 4 4 4 4 4 4 7 4 4 4
4 4 4 4 4 4 4 4 0 4 4 4
4 4 4 4 4 4 4 4 8 0 3 4
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
```

#### Train 2 output
```text
4 4 4 4 4 4 4 4 4 4 4 4
4 2 9 9 5 9 6 9 9 4 4 4
4 4 4 4 4 4 4 4 9 4 4 4
4 4 4 4 4 4 4 4 7 4 4 4
4 4 4 4 4 4 4 4 9 4 4 4
4 4 4 4 4 4 4 4 8 9 3 4
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
```

#### Train 3 input
```text
4 4 4 4 4 4 4 4 4 4 4 4 4
4 2 0 7 0 0 8 4 4 4 4 4 4
4 4 4 4 4 4 0 4 4 4 4 4 4
4 4 4 4 4 4 0 4 4 4 4 4 4
4 4 4 4 4 4 0 4 4 4 4 4 4
4 4 4 4 4 4 5 0 0 6 0 4 4
4 4 4 4 4 4 4 4 4 4 0 4 4
4 4 4 4 4 4 4 4 4 4 0 3 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```

#### Train 3 output
```text
4 4 4 4 4 4 4 4 4 4 4 4 4
4 2 9 7 9 9 8 4 4 4 4 4 4
4 4 4 4 4 4 9 4 4 4 4 4 4
4 4 4 4 4 4 9 4 4 4 4 4 4
4 4 4 4 4 4 9 4 4 4 4 4 4
4 4 4 4 4 4 5 9 9 6 9 4 4
4 4 4 4 4 4 4 4 4 4 9 4 4
4 4 4 4 4 4 4 4 4 4 9 3 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```

### Test pairs

#### Test 1 input
```text
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 2 0 0 5 4 4 0 0 7 4 4 4 4
4 4 4 4 0 4 4 0 4 0 4 4 4 4
4 4 4 4 0 0 0 6 4 0 4 4 4 4
4 4 4 4 4 4 4 4 4 8 4 4 4 4
4 4 4 4 4 4 4 4 4 0 4 4 4 4
4 4 4 4 4 4 4 4 4 0 0 0 3 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
```

#### Test 1 output
```text
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 2 9 9 5 4 4 9 9 7 4 4 4 4
4 4 4 4 9 4 4 9 4 9 4 4 4 4
4 4 4 4 9 9 9 6 4 9 4 4 4 4
4 4 4 4 4 4 4 4 4 8 4 4 4 4
4 4 4 4 4 4 4 4 4 9 4 4 4 4
4 4 4 4 4 4 4 4 4 9 9 9 3 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
```

## hard_p03 — Visibility Matrix (hard)

**Tags:** relation, matrix, object

**Written rule:** Sort the connected objects by top-to-bottom, then left-to-right. Output an n×n matrix with 1 on the diagonal and 8 whenever a pair of objects has unobstructed horizontal or vertical line-of-sight through at least one empty cell.

**Program:** `solve_hard_p03`

**Primitives:** `visibility_matrix`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
1 8 8
8 1 0
8 0 1
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
1 8 8 0
8 1 0 8
8 0 1 8
0 8 8 1
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
1 8 8 0
8 1 0 8
8 0 1 8
0 8 8 1
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 6 6 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
1 8 8 0
8 1 0 8
8 0 1 8
0 8 8 1
```

## hard_p04 — Area-Rank Frame Assignment (hard)

**Tags:** assignment, frames, ranking

**Written rule:** Ignore the hollow gray(5) frames and sort the free objects by area from smallest to largest. Sort the frames by their interior area from smallest to largest, then center each cropped object inside the correspondingly ranked frame.

**Program:** `solve_hard_p04`

**Primitives:** `area_rank_frame_assign`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 5 5 5 5 0 0
0 5 0 5 0 0 0 0 5 0 0 5 0 0
0 5 5 5 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 8 0
0 5 0 0 0 5 0 0 0 3 0 8 8 8
0 5 0 0 0 5 0 0 0 3 3 0 8 0
0 5 0 0 0 5 0 0 0 0 7 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 5 5 5 5 0 0
0 5 7 5 0 0 0 0 5 3 0 5 0 0
0 5 5 5 0 0 0 0 5 3 3 5 0 0
0 0 0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 0 8 0 5 0 0 0 0 0 0 0 0
0 5 8 8 8 5 0 0 0 0 0 0 0 0
0 5 0 8 0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 5 5 5 0 0
0 0 0 9 0 0 4 4 0 0 5 0 5 0 0
0 0 0 0 0 0 0 4 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 5 5 5 5 5 0
0 5 0 0 5 0 0 0 0 5 0 0 0 5 0
0 5 5 5 5 0 0 6 0 5 0 0 0 5 0
0 0 0 0 0 0 6 6 6 5 0 0 0 5 0
0 0 0 0 0 0 0 6 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 9 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 5 4 0 5 0 0 0 0 5 5 5 5 5 0
0 5 4 4 5 0 0 0 0 5 0 6 0 5 0
0 5 5 4 5 0 0 0 0 5 6 6 6 5 0
0 0 0 0 0 0 0 0 0 5 0 6 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 5 5 5 5 0 0
0 5 0 0 0 5 0 0 0 0 5 0 0 5 0 0
0 5 0 0 0 5 0 0 0 0 5 0 0 5 0 0
0 5 0 0 0 5 0 0 0 0 5 5 5 5 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 3 3 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 5 5 5 0 0
0 0 4 0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 4 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 5 5 5 5 0 0
0 5 4 4 4 5 0 0 0 0 5 3 0 5 0 0
0 5 0 4 0 5 0 0 0 0 5 3 3 5 0 0
0 5 0 4 0 5 0 0 0 0 5 5 5 5 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 7 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 0
0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 0
0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 0
0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 4 0 0 0 0 0 9 9 9
0 5 5 5 0 0 0 4 4 0 0 0 0 0 9 0
0 5 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 5 5 5 5 5 0
0 0 5 4 0 5 0 0 0 0 5 0 9 0 5 0
0 0 5 4 4 5 0 0 0 0 5 9 9 9 5 0
0 0 5 5 5 5 0 0 0 0 5 0 9 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 8 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p05 — Dual-Key Boolean Composer (hard)

**Tags:** boolean, transform, composition

**Written rule:** Use the top-right key to transform the second object, normalize both cropped objects to one origin, then combine them according to the top-left key: 1=union, 2=intersection, 3=xor, 4=A-minus-B, anything else=B-minus-A.

**Program:** `solve_hard_p05`

**Primitives:** `dual_key_boolean`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 7 7 0 0 0
0 6 0 0 0 0 0 0 7 0 0 0
0 6 6 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 0 3
8 3 3
2 2 0
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 9 0 0 0 0
0 0 8 0 0 0 0 0 9 0 0 0 0
0 0 8 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 8
0 0
8 0
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 7 7 0 0 0
0 6 6 6 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0
0 2 2
3 3 0
```

### Test pairs

#### Test 1 input
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 9 0 0 0 0
0 0 8 0 0 0 0 0 0 9 9 9 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
2 0
2 0
0 0
```

## hard_p06 — Orbit Stamp Around Anchor (hard)

**Tags:** transform, stamping, rotation

**Written rule:** Crop the template object, then stamp four copies of it around the anchor(9): the original in the northwest, a 90° rotation in the northeast, a 180° rotation in the southwest, and a 270° rotation in the southeast.

**Program:** `solve_hard_p06`

**Primitives:** `orbit_stamp`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 6 6 0 0 0 0
0 0 0 6 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 6 6 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 7 7 7 0 0 0 0
0 0 0 0 7 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 8 8 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p07 — Frame-Key Transform Stamp (hard)

**Tags:** transform, frames, multi_target

**Written rule:** Use the free template object as the stamp. For each hollow frame, read its nearby key (1=identity, 2=rotate90, 3=flip-left-right, 4=flip-up-down), transform the template accordingly, and center that transformed template inside the frame.

**Program:** `solve_hard_p07`

**Primitives:** `frame_key_stamp`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 1 0 0 0 0 2 0 0 0 0
0 6 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 6 7 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 5 6 0 5 0 5 6 6 5 0
0 0 0 0 0 0 0 0 5 6 7 5 0 5 7 0 5 0
0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 6 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 7 6 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 6 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 6 7 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 6 7 5 0 5 6 0 5 0
0 0 0 0 0 0 0 0 0 0 5 6 0 5 0 5 6 7 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 6 6 5 0 5 0 6 5 0
0 0 0 0 0 0 0 0 0 0 5 7 0 5 0 5 7 6 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0
0 6 7 0 0 0 0 0 0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 6 6 5 0 5 6 7 5 0
0 0 0 0 0 0 0 0 0 0 5 7 0 5 0 5 6 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 6 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 6 7 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 6 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 6 7 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 6 5 0 5 6 6 5 0
0 0 0 0 0 0 0 0 0 0 0 5 7 6 5 0 5 7 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 6 7 5 0 5 6 0 5 0
0 0 0 0 0 0 0 0 0 0 0 5 6 0 5 0 5 6 7 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
