# ARC Puzzle Bank — Set 24


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `one_gap_bridge`: Fill the single 0 exactly between two same-color endpoints in a row or column.
- `anti_diagonal_orbit`: Add the anti-diagonal reflection of every colored cell while keeping the originals.
- `square_ring_bloom`: Expand each solid monochrome 2x2 square into the surrounding 4x4 ring of the same color.
- `bottom_keep`: Keep only the bottommost nonzero cell in each column.
- `opposite_corner_complete`: Complete rectangles when only one diagonal pair of same-color corners is present.
- `half_turn_echo`: Add a 180-degree rotational echo of every colored cell.
- `blocked_crosshair`: Project each seed along its row and column until a wall or the border stops it.
- `color_key_crop`: Use a color key cell to select which object to crop tightly.
- `hole_rank_palette`: Recolor each object according to its number of enclosed holes.
- `compartment_left_pack`: Pack colored cells leftward inside each wall-bounded row compartment while preserving order.
- `external_seed_fill`: Fill each hollow frame interior using the nearby external seed color.
- `width_gallery`: Crop objects and lay them out left-to-right sorted by width.
- `diagonal_segment_connect`: Connect same-color markers by filling an unobstructed diagonal segment.
- `bbox_center_dock`: Translate an object so its bounding-box center lands on a marker.
- `script_transform_gallery`: Read a key script and output a gallery of transformed template copies in that order.
- `portal_shortest_path`: Find the shortest path when stepping onto a portal teleports you to its mate.
- `hole_key_frame_assign`: Assign objects to frames by matching each object's hole count to a frame key.
- `left_of_matrix`: Summarize horizontal relations between objects as a binary matrix.
- `dual_key_boolean`: Transform one shape by a key, then combine two normalized shapes with a keyed boolean op.
- `ordered_checkpoint_path`: Trace the shortest path that visits numbered checkpoints in ascending order before the goal.
- `wall_geodesic_voronoi`: Fill each reachable empty cell with the closest seed color by shortest path around walls.

## easy_p01 — One-Gap Bridge (easy)

**Tags:** local, interval, completion

**Written rule:** Whenever two same-color cells in the same row or column are separated by exactly one 0, fill that middle cell with the same color. Leave everything else unchanged.

**Program:** `solve_easy_p01`

**Primitives:** `one_gap_bridge`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 3 0
6 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 3 0
6 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 3 0
6 0 0 0 0 0 0 3 0
6 0 0 0 4 4 4 3 0
6 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 8 0 8 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 4 0
0 5 0 5 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 8 8 8 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 0
0 0 0 2 0 0 4 0
0 5 5 5 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 1 0 1 0 3 0 3 0
0 0 0 0 0 0 0 0 4 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0 0 0
6 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 1 1 1 0 3 3 3 0
0 0 0 0 0 0 0 0 4 0
6 0 0 0 0 0 0 0 0 0
6 0 0 0 7 7 7 0 0 0
6 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 3 0
0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 3 0
0 0 0 0 0 0 0 4 0 4 0
6 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 3 0
0 0 2 2 2 0 0 0 0 3 0
0 0 0 0 1 0 0 0 0 3 0
0 0 0 0 1 0 0 4 4 4 0
6 0 0 0 1 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## easy_p02 — Anti-Diagonal Orbit (easy)

**Tags:** symmetry, reflection, same_size

**Written rule:** For every colored cell, also color its reflection across the anti-diagonal of the square grid. Keep the original cells too.

**Program:** `solve_easy_p02`

**Primitives:** `anti_diagonal_orbit`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 4 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0
0 2 0 0 4 0 0
0 0 0 0 0 4 0
0 7 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 7 0 2 0
0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3
0 0 8 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 6 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 5 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 2 0 0 0
0 0 4 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p03 — Square Ring Bloom (easy)

**Tags:** local, shape_growth, square

**Written rule:** Each solid monochrome 2x2 square blooms into the surrounding 4x4 ring of the same color. Existing square cells stay colored.

**Program:** `solve_easy_p03`

**Primitives:** `square_ring_bloom`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 2 2 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 4 4 4 4 0
0 2 2 2 2 4 4 4 4 0
0 2 2 2 2 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 7 7 7 0 0 0 0 0
7 7 7 7 0 0 0 0 0
7 7 7 7 0 0 0 0 0
7 7 7 7 0 0 0 0 0
0 0 0 3 3 3 3 0 0
0 0 0 3 3 3 3 0 0
0 0 0 3 3 3 3 0 0
0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 8 8 8 8 0
0 5 5 5 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0 0
0 0 6 6 6 6 0 9 9 9 9 0
0 0 6 6 6 6 0 9 9 9 9 0
0 0 6 6 6 6 0 9 9 9 9 0
0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p04 — Bottommost Column Filter (easy)

**Tags:** filter, column, same_size

**Written rule:** In each column, keep only the lowest nonzero cell and erase every nonzero cell above it.

**Program:** `solve_easy_p04`

**Primitives:** `bottom_keep`

### Train pairs

#### Train 1 input
```text
0 2 0 0 0 0 0 8
0 0 0 5 0 0 0 0
0 0 0 0 0 6 0 0
0 4 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 3
0 7 0 0 0 0 0 0
0 0 0 0 0 1 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 3
0 7 0 0 0 0 0 0
0 0 0 0 0 1 0 0
```

#### Train 2 input
```text
4 0 0 0 0 0 0
0 0 0 0 6 0 0
0 0 7 0 0 0 0
0 0 0 0 0 0 8
0 0 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
0 0 9 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 8
0 0 0 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
0 0 9 0 0 0 0
```

#### Train 3 input
```text
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 5 0 0 0 0 0 7 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 8 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 8 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 8 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 2 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 2 0 0 0 0 0 0 0
```

## easy_p05 — Opposite-Corner Completion (easy)

**Tags:** rectangle, completion, geometry

**Written rule:** If a rectangle has one diagonal pair of same-color corners present and the other two corners empty, fill in the missing two corners with that color.

**Program:** `solve_easy_p05`

**Primitives:** `opposite_corner_complete`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 3 0 2 0 3 0 0
7 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0
0 0 3 0 0 0 3 0 0
7 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
9 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
9 0 0 9 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0
0 0 0 0 6 0 0 0 6 0
9 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 2
0 0 0 0 0 8 0 0
0 0 3 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 2 0 0 2
0 8 0 0 0 8 0 0
0 0 3 0 0 0 3 0
0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0
0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 5 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 7 0
0 5 0 0 0 0 5 0 0 0
4 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 7 0
0 5 0 0 0 0 5 0 0 0
4 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## easy_p06 — Half-Turn Echo (easy)

**Tags:** symmetry, rotation, same_size

**Written rule:** For every colored cell, add its 180-degree rotated counterpart in the same color. Keep the originals.

**Program:** `solve_easy_p06`

**Primitives:** `half_turn_echo`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 4 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 3 0
0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0
0 3 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 5 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
0 5 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 9 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
```

## easy_p07 — Blocked Crosshair Projection (easy)

**Tags:** projection, walls, same_size

**Written rule:** Each colored seed projects its color horizontally and vertically through 0 cells until a wall-colored 5 cell or the border stops the beam. Walls remain 5.

**Program:** `solve_easy_p07`

**Primitives:** `blocked_crosshair`

### Train pairs

#### Train 1 input
```text
0 0 0 0 5 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 3 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 5 0 0 0 0 5 0
0 0 0 0 5 0 0 0 4 5 0
0 0 0 0 5 0 0 0 0 5 0
0 0 0 0 5 0 0 0 0 5 0
```

#### Train 1 output
```text
0 2 0 0 5 0 3 0 0 0 0
2 2 2 2 5 0 3 0 0 0 0
0 2 0 0 5 3 3 3 3 3 3
0 2 0 0 5 5 5 5 5 0 0
0 2 0 0 5 0 0 0 4 5 0
0 2 0 0 5 4 4 4 4 5 0
0 2 0 0 5 0 0 0 4 5 0
0 2 0 0 5 0 0 0 4 5 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
5 5 5 5 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 5 5 5 5
0 0 0 0 5 8 0 0 0
0 0 0 0 5 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 7 0
7 7 7 7 7 7 7 7 7
5 5 5 5 5 0 0 7 0
0 0 2 0 5 0 0 7 0
2 2 2 2 5 0 0 7 0
0 0 2 0 5 0 0 7 0
0 0 2 0 5 5 5 5 5
0 0 2 0 5 8 8 8 8
0 0 2 0 5 8 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 3 0 0 0 0 5 0 0 0 0
5 5 5 5 5 5 0 5 0 0 0 0
0 0 0 0 0 1 0 5 0 0 0 0
0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 5 0 0 0 5 0 6 0 0
0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 5 0 0 0 5 0 0 0 0
```

#### Train 3 output
```text
0 0 3 0 0 0 0 5 0 6 0 0
0 0 3 0 0 0 0 5 0 6 0 0
3 3 3 3 3 3 3 5 0 6 0 0
5 5 5 5 5 5 0 5 0 6 0 0
1 1 1 1 1 1 1 5 0 6 0 0
0 0 0 5 0 1 0 5 0 6 0 0
0 0 0 5 0 1 0 5 6 6 6 6
0 0 0 5 0 1 0 5 0 6 0 0
0 0 0 5 0 1 0 5 0 6 0 0
0 0 0 5 0 1 0 5 0 6 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 5 5 5 5 5 5 5 5
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
5 5 5 5 5 0 5 0 0 0
0 4 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 2 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 5 5 5 5 5 5 5 5
9 9 9 9 9 9 9 2 9 9
0 0 0 0 9 0 0 2 0 0
0 0 0 0 9 0 5 2 0 0
5 5 5 5 5 0 5 2 0 0
4 4 4 4 4 4 5 2 0 0
0 4 0 0 0 0 5 2 2 2
0 4 0 0 0 0 0 2 0 0
```

## medium_p01 — Color-Key Crop (medium)

**Tags:** selection, crop, marker

**Written rule:** The top-left key cell names a color. Find the connected object of that color elsewhere in the grid and output its tight bounding-box crop.

**Program:** `solve_medium_p01`

**Primitives:** `color_key_crop`

### Train pairs

#### Train 1 input
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 2 0 0 0 4 4 4 0 0 0
0 2 0 0 0 0 4 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 4 0
4 4 4
0 4 0
```

#### Train 2 input
```text
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 7 7 0 0
0 9 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 0 7
7 7 7
```

#### Train 3 input
```text
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 2 2 0 0 0 0 0 4 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
2 2
2 2
2 0
```

### Test pairs

#### Test 1 input
```text
6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0
0 0 0 0 2 0 2 0 0
0 8 8 8 2 2 2 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 0
6 0
6 6
```

## medium_p02 — Hole Count Recolor (medium)

**Tags:** topology, recolor, objects

**Written rule:** Recolor each object only by how many holes it encloses: 0 holes become color 2, 1 hole becomes color 3, and 2 holes become color 4.

**Program:** `solve_medium_p02`

**Primitives:** `hole_rank_palette`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 7 7 7 0 0 0 0 0
0 4 4 0 0 0 7 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 9 9 0 0 0 0 0 0
0 0 0 9 0 9 0 9 0 0 0 0 0 0
0 0 0 9 9 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 3 0 0 0 0 0
0 2 2 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 4 0 4 0 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0
0 6 6 6 0 0 0 3 0 0 3 0 0
0 6 6 6 0 0 0 3 0 0 3 0 0
0 6 6 6 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0
0 2 2 2 0 0 0 3 0 0 3 0 0
0 2 2 2 0 0 0 3 0 0 3 0 0
0 2 2 2 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 4 0 4 0 4 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 7 7 7 7 7 0 0 0 0
0 2 2 0 0 0 7 0 7 0 7 0 0 0 0
0 2 2 0 0 0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 2 2 0 0 0 4 0 4 0 4 0 0 0 0
0 2 2 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 6 6
0 4 4 4 0 0 0 6 0 6 0 6
0 4 0 4 0 0 0 6 6 6 6 6
0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4
0 3 3 3 0 0 0 4 0 4 0 4
0 3 0 3 0 0 0 4 4 4 4 4
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p03 — Compartment Left Pack (medium)

**Tags:** gravity, walls, rowwise

**Written rule:** Treat each row segment between wall cells 5 as a separate compartment. Within each compartment, slide all colored cells as far left as possible while preserving their order.

**Program:** `solve_medium_p03`

**Primitives:** `compartment_left_pack`

### Train pairs

#### Train 1 input
```text
0 5 0 0 0 5 0 0 0 5 0 0
0 5 4 0 7 5 2 0 0 5 0 0
3 5 0 8 0 5 0 6 0 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 5 9 0 0 5 1 0 0 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 5 0 0 0 5 0 0 4 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
```

#### Train 1 output
```text
0 5 0 0 0 5 0 0 0 5 0 0
0 5 4 7 0 5 2 0 0 5 0 0
3 5 8 0 0 5 6 0 0 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 5 9 0 0 5 1 0 0 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
0 5 0 0 0 5 4 0 0 5 0 0
0 5 0 0 0 5 0 0 0 5 0 0
```

#### Train 2 input
```text
0 6 0 5 0 2 0 5 0 0 0
9 0 0 5 0 0 4 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 1 5 0 0 0 5 3 0 0
0 0 0 5 0 0 0 5 0 0 0
0 7 0 5 0 8 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 0 5 0 6 0
0 0 0 5 0 0 0 5 0 0 0
```

#### Train 2 output
```text
6 0 0 5 2 0 0 5 0 0 0
9 0 0 5 4 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
1 0 0 5 0 0 0 5 3 0 0
0 0 0 5 0 0 0 5 0 0 0
7 0 0 5 8 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
2 0 0 5 0 0 0 5 6 0 0
0 0 0 5 0 0 0 5 0 0 0
```

#### Train 3 input
```text
2 0 0 0 5 0 5 0 5 0 5 0 0
0 7 0 0 5 3 0 0 5 0 5 0 0
0 0 0 0 5 0 0 9 5 0 5 4 0
0 0 0 0 5 0 0 0 5 0 5 0 0
0 0 6 0 5 0 0 0 5 1 5 0 0
0 0 0 0 5 0 0 0 5 0 5 0 0
8 0 0 0 5 0 2 0 5 0 5 0 0
```

#### Train 3 output
```text
2 0 0 0 5 0 5 0 5 0 5 0 0
7 0 0 0 5 3 0 0 5 0 5 0 0
0 0 0 0 5 9 0 0 5 0 5 4 0
0 0 0 0 5 0 0 0 5 0 5 0 0
6 0 0 0 5 0 0 0 5 1 5 0 0
0 0 0 0 5 0 0 0 5 0 5 0 0
8 0 0 0 5 2 0 0 5 0 5 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 5 0 0 0 5 0 0 0
3 0 5 0 7 0 5 0 0 0
0 8 5 0 0 0 5 4 0 0
0 0 5 0 0 0 5 0 0 0
9 0 5 0 0 2 5 0 0 0
0 0 5 0 0 0 5 0 0 0
0 0 5 0 0 0 5 0 1 0
0 0 5 0 0 0 5 0 0 0
```

#### Test 1 output
```text
0 0 5 0 0 0 5 0 0 0
3 0 5 7 0 0 5 0 0 0
8 0 5 0 0 0 5 4 0 0
0 0 5 0 0 0 5 0 0 0
9 0 5 2 0 0 5 0 0 0
0 0 5 0 0 0 5 0 0 0
0 0 5 0 0 0 5 1 0 0
0 0 5 0 0 0 5 0 0 0
```

## medium_p04 — External Seed Frame Fill (medium)

**Tags:** frames, seeded_fill, same_size

**Written rule:** Each hollow rectangular frame has a colored seed immediately outside it. Fill that frame's interior with the seed color while keeping the frame border as 5.

**Program:** `solve_medium_p04`

**Primitives:** `external_seed_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0 5 5 5 5 0
0 2 5 0 0 0 5 0 0 5 0 0 5 0
0 0 5 0 0 0 5 0 7 5 0 0 5 0
0 0 5 5 5 5 5 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 5 2 2 2 5 0 0 5 5 5 5 0
0 2 5 2 2 2 5 0 0 5 7 7 5 0
0 0 5 2 2 2 5 0 7 5 7 7 5 0
0 0 5 5 5 5 5 0 0 5 7 7 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 4 5 0 0 0 5 0 0 0 0 0
0 0 0 5 0 0 0 5 0 5 5 5 5
0 0 0 5 5 5 5 5 0 5 0 0 5
0 0 0 0 0 0 0 0 8 5 0 0 5
0 0 0 0 0 0 0 0 0 5 0 0 5
0 0 0 0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 4 5 4 4 4 5 0 0 0 0 0
0 0 0 5 4 4 4 5 0 5 5 5 5
0 0 0 5 5 5 5 5 0 5 8 8 5
0 0 0 0 0 0 0 0 8 5 8 8 5
0 0 0 0 0 0 0 0 0 5 8 8 5
0 0 0 0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0 0 0 0 0
0 6 5 0 0 5 0 0 0 5 5 5 5 5 0
0 0 5 0 0 5 0 0 0 5 0 0 0 5 0
0 0 5 5 5 5 0 0 3 5 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0 0 0 0 0
0 6 5 6 6 5 0 0 0 5 5 5 5 5 0
0 0 5 6 6 5 0 0 0 5 3 3 3 5 0
0 0 5 5 5 5 0 0 3 5 3 3 3 5 0
0 0 0 0 0 0 0 0 0 5 3 3 3 5 0
0 0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0
0 5 0 0 5 0 0 5 5 5 5 0
9 5 0 0 5 0 0 5 0 0 5 0
0 5 0 0 5 0 2 5 0 0 5 0
0 5 5 5 5 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0
0 5 9 9 5 0 0 5 5 5 5 0
9 5 9 9 5 0 0 5 2 2 5 0
0 5 9 9 5 0 2 5 2 2 5 0
0 5 5 5 5 0 0 5 2 2 5 0
0 0 0 0 0 0 0 5 2 2 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p05 — Width-Sorted Gallery (medium)

**Tags:** gallery, crop, ordering

**Written rule:** Crop each object to its tight box, sort the crops by width from narrowest to widest, and place them left-to-right with one blank column between them.

**Program:** `solve_medium_p05`

**Primitives:** `width_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 4 4 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 0 0 7 7 7 0 4 4 4 4
2 0 0 7 0 7 0 0 0 0 0
2 2 0 7 7 7 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0 0 0
0 0 0 6 6 6 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
8 8 0 6 0 6 0 0 3 0
8 8 0 6 6 6 0 3 3 3
0 0 0 0 0 0 0 0 3 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 4 4 4 0 0
0 0 0 0 2 2 2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
4 4 4 0 9 9 0 0 2 2 2
0 4 0 0 0 9 9 0 2 2 2
0 0 0 0 0 0 0 0 2 2 2
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 5 5 5 5 0
0 7 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 3 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
3 0 7 7 0 5 5 5 5
0 0 7 7 0 5 0 0 5
0 0 7 0 0 5 0 0 5
0 0 0 0 0 5 5 5 5
```

## medium_p06 — Diagonal Segment Connect (medium)

**Tags:** diagonal, connection, markers

**Written rule:** Whenever two same-color markers lie on a clean diagonal with only 0s between them, fill the whole diagonal segment in that color.

**Program:** `solve_medium_p06`

**Primitives:** `diagonal_segment_connect`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 0
0 0 0 0 2 0 4 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 7 0 0 0 0 0 3 0 0 0
0 0 0 7 0 0 0 3 0 0 0 0
0 0 0 0 7 0 3 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 8 0 0 0 0 6 0 0 0 0
0 0 8 0 0 0 0 6 0 0 0
0 0 0 8 0 0 0 0 6 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 9 0 0
0 0 0 0 4 0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0 9 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
```

## medium_p07 — Center Dock to Marker (medium)

**Tags:** translation, marker, objects

**Written rule:** Move the single object so that the center of its bounding box lands on the marker cell colored 8. Remove the marker and keep the canvas size the same.

**Program:** `solve_medium_p07`

**Primitives:** `bbox_center_dock`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 8 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## hard_p01 — Scripted Transform Gallery (hard)

**Tags:** script, transforms, gallery

**Written rule:** Read the nonzero keys in the top row from left to right. Apply each keyed transform to the template object and output the transformed crops as a gallery in that same order.

**Program:** `solve_hard_p01`

**Primitives:** `script_transform_gallery`

### Train pairs

#### Train 1 input
```text
0 1 0 2 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
7 7 0 7 7 7 0 7 7
7 7 0 0 7 7 0 7 7
7 0 0 0 0 0 0 0 7
```

#### Train 2 input
```text
0 4 0 1 0 3 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
6 6 6 0 6 0 6 0 6 0 6 0 6 6
6 0 6 0 6 6 6 0 6 6 6 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6
```

#### Train 3 input
```text
0 2 0 4 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 8 0 8 8 0 0 8 8 0
8 8 0 0 8 8 0 0 8 8
8 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 3 0 2 0 4 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
9 9 9 0 0 9 0 0 9 0 0 9 9 9
0 9 0 0 9 9 0 9 9 9 0 0 9 0
0 0 0 0 0 9 0 0 0 0 0 0 0 0
```

## hard_p02 — Portal Shortest Path (hard)

**Tags:** pathfinding, portals, maze

**Written rule:** Find the shortest path from the start 2 to the goal 3 while avoiding wall cells 5. Stepping onto a portal teleports you instantly to its matching portal. Mark the traversed empty path cells with 8.

**Program:** `solve_hard_p02`

**Primitives:** `portal_shortest_path`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 6 0 0
0 5 5 0 5 5 5 5 5 5 0
0 0 0 0 0 5 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 5 0 0 0 0 0
0 5 5 5 5 5 5 0 5 5 0
0 7 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
8 2 0 0 0 0 0 0 6 0 0
8 5 5 0 5 5 5 5 5 5 0
8 0 0 0 0 5 0 0 0 7 0
8 0 0 0 0 0 0 0 0 8 0
8 0 6 0 0 5 0 0 0 8 8
8 5 5 5 5 5 5 0 5 5 8
8 7 0 0 0 0 0 0 0 3 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 5 0 7 5 0 0 0
0 0 0 0 0 0 5 0 6 0
0 0 0 5 0 0 5 0 0 0
0 5 5 5 5 0 5 5 5 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 6 5 0 0 0 0 0 0
0 0 0 5 0 7 5 0 3 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 8 8 8 8 0 0 0 0 0
0 2 0 5 8 7 5 0 0 0
0 0 0 0 0 0 5 0 6 0
0 0 0 5 0 0 5 0 0 0
0 5 5 5 5 0 5 5 5 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 6 5 0 8 8 8 0 0
0 0 0 5 0 7 5 8 3 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 5 5 5 5 5 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 5 5 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 6 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 0 5 5 5 5 5 5 0 0
0 8 0 0 0 0 5 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 7 0
0 8 0 0 0 0 5 0 0 0 0 8 0
0 8 5 5 5 5 5 5 0 5 5 8 0
0 8 6 0 0 0 0 0 0 0 0 8 0
0 8 8 8 8 7 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 7 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 5 5 0 0
0 0 6 0 5 0 0 0 0 0 0 0
0 0 0 0 5 7 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 6 0 0
0 8 0 0 0 0 0 0 0 8 0 0
0 8 0 0 5 0 0 0 0 8 7 0
0 8 0 0 5 0 0 0 0 8 8 0
0 8 5 5 5 5 5 0 5 5 8 0
0 8 6 0 5 0 0 0 0 0 8 0
0 0 0 0 5 7 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p03 — Hole-Key Frame Assignment (hard)

**Tags:** assignment, topology, frames

**Written rule:** Each frame key encodes a target hole count: key 1 wants a 0-hole object, key 2 wants a 1-hole object, and key 3 wants a 2-hole object. Move each matching object into the corresponding frame, centered inside it.

**Program:** `solve_hard_p03`

**Primitives:** `hole_key_frame_assign`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 0 0 0 5
0 6 6 6 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 5 0 0 0 5
0 6 0 6 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 5 5 5 5
0 6 6 6 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 8 0 8 0 8 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 4 4 0 5 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 4 4 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 6 6 6 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 6 0 6 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 6 6 6 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 5 0 0 0 5
0 9 9 9 9 9 0 0 0 0 0 0 0 0 3 0 0 0 0 5 0 0 0 5
0 9 0 9 0 9 0 0 0 0 0 0 5 5 5 5 5 0 0 5 0 0 0 5
0 9 9 9 9 9 0 0 0 0 0 0 5 0 0 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 7 7 7 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 7 0 7 5 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 5 7 7 7 5 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 5 4 4 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 5 4 4 4 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 4 4 4 5
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 9 0 9 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0
0 5 0 5 0 5 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 5 0 0 5
0 6 6 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 0 0 5
0 6 6 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 5 0 5 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 4 4 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 4 0 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 4 4 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 6 6 0 5 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 6 6 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 3 0 0
0 5 5 5 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 0 0 0 5
0 7 7 7 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 5 5 5 5 5
0 7 0 7 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 9 0 9 0 5 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 9 0 9 0 9
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 7 7 7 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 7 0 7 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 7 7 7 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p04 — Left-Of Relation Matrix (hard)

**Tags:** relations, matrix, objects

**Written rule:** Order the objects by color value. Output a binary matrix where entry (i,j) is 1 iff object i is strictly left of object j, using bounding-box centers.

**Program:** `solve_hard_p04`

**Primitives:** `left_of_matrix`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 1 1
0 0 1
0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7
0 0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 5 0 5 0 0 0 0 0
0 9 9 0 0 0 5 5 5 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 1 1 0
0 0 1 0
0 0 0 0
1 1 1 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 1
1 0 1
0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 3 3 0 0 0 0 0 0 0 0 7 0 0 0
0 0 3 3 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0 9 9 9
0 0 0 0 0 0 5 5 5 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 1 1 1
0 0 1 1
0 0 0 1
0 0 0 0
```

## hard_p05 — Dual-Key Boolean Compose (hard)

**Tags:** boolean, transforms, composition

**Written rule:** Use the first key to transform one source shape, then use the second key to choose union, intersection, or xor with the other source shape. Output the resulting normalized shape in color 8.

**Program:** `solve_hard_p05`

**Primitives:** `dual_key_boolean`

### Train pairs

#### Train 1 input
```text
0 2 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
8 8 8
8 8 8
0 8 0
```

#### Train 2 input
```text
0 3 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
8
8
```

#### Train 3 input
```text
0 4 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 3 3 3 0 0 0
0 0 2 0 0 0 0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 8
8 0
8 8
```

### Test pairs

#### Test 1 input
```text
0 1 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 3 3 3 0 0
0 0 2 2 2 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
8 8 8
8 8 8
8 8 8
```

## hard_p06 — Ordered Checkpoint Path (hard)

**Tags:** pathfinding, ordered_goals, maze

**Written rule:** Find the shortest path from start 2 to goal 3 while visiting all numbered checkpoint cells in ascending order first. Avoid walls 5 and mark the traversed empty path cells with 8.

**Program:** `solve_hard_p06`

**Primitives:** `ordered_checkpoint_path`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 5 5 5 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 5 5 5 0
0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
8 2 0 0 0 0 0 0 0 0 0
8 5 5 5 0 5 5 5 5 5 0
8 0 0 0 0 0 0 0 0 0 0
8 8 4 8 8 8 8 8 6 0 0
0 0 0 0 0 0 0 0 8 8 8
0 5 5 5 5 5 0 5 5 5 8
0 0 0 0 0 0 0 0 0 3 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 5 0 0 0 4 0 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 5 5 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 6 0 0 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 8 8 8 8 8 8 0 0 0 0 0
0 2 0 0 0 5 8 8 8 4 0 0
0 0 0 0 0 5 0 0 0 8 0 0
0 8 8 8 8 8 8 8 8 8 0 0
0 8 5 5 5 5 5 5 0 5 5 0
0 8 0 0 0 5 0 0 0 0 0 0
0 8 0 0 0 5 0 0 0 0 0 0
0 8 6 0 0 5 0 0 0 0 0 0
0 0 8 0 0 5 8 8 8 8 3 0
0 0 8 8 8 8 8 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 8 8 8 8 8 8 8 8 4 0 0
0 0 8 8 8 8 8 8 8 8 8 0 0
0 5 8 5 5 5 5 5 5 5 5 5 0
0 0 8 0 0 0 0 5 0 0 0 0 0
0 0 8 0 0 0 0 5 0 0 0 0 0
0 0 8 0 0 0 0 5 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 6 0 0 0 0 5 8 0 0 0 0
0 0 0 0 0 0 0 5 8 8 8 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 5 5 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 6 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 4 0 0
0 0 0 0 5 0 0 0 0 8 0 0
0 0 0 0 5 0 0 0 8 8 0 0
0 0 0 0 5 5 5 5 8 5 5 0
0 0 0 0 5 0 0 0 8 0 0 0
0 0 0 0 5 6 8 8 8 8 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p07 — Wall-Geodesic Voronoi (hard)

**Tags:** distance, walls, fill

**Written rule:** Treat each nonzero non-wall cell as a seed color. Fill every reachable empty cell with the color of the seed that is closest by shortest path around the wall cells 5. Ties stay 0.

**Program:** `solve_hard_p07`

**Primitives:** `wall_geodesic_voronoi`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 4 0 0
0 0 0 0 0 5 0 0 0 0 0
5 5 0 5 5 5 5 5 5 5 5
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 5 0 0 9 0 0
0 0 0 0 0 5 0 0 0 0 0
```

#### Train 1 output
```text
2 2 2 2 2 5 4 4 4 4 4
2 2 2 2 2 0 4 4 4 4 4
2 2 2 2 2 5 4 4 4 4 4
2 2 2 2 2 5 4 4 4 4 4
5 5 7 5 5 5 5 5 5 5 5
7 7 7 7 7 5 9 9 9 9 9
7 7 7 7 7 0 9 9 9 9 9
7 7 7 7 7 5 9 9 9 9 9
7 7 7 7 7 5 9 9 9 9 9
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 5 0 0 0 0 5 0 0 0
0 0 0 5 0 0 0 0 5 0 6 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 5 0 0 0 0 5 0 0 0
0 5 5 5 5 5 0 5 5 5 5 0
0 0 0 5 0 0 0 0 5 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 2 0 5 0 0 0 0 5 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
3 3 3 3 3 3 0 6 6 6 6 6
3 3 3 5 3 3 0 6 5 6 6 6
3 3 3 5 3 3 0 6 5 6 6 6
3 3 3 3 3 3 3 0 5 6 6 6
3 3 3 5 3 3 0 0 5 6 6 6
2 5 5 5 5 5 9 5 5 5 5 0
2 2 2 5 2 9 9 9 5 9 9 9
2 2 2 5 2 9 9 9 9 9 9 9
2 2 2 5 2 2 9 9 5 9 9 9
2 2 2 2 2 2 9 9 9 9 9 9
```

#### Train 3 input
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 4 0 0 0 0 5 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
5 5 5 0 5 5 5 5 5 0 5 5 5
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

#### Train 3 output
```text
4 4 4 4 4 4 5 7 7 7 7 7 7
4 4 4 4 4 4 5 7 7 7 7 7 7
4 4 4 4 4 4 0 7 7 7 7 7 7
4 4 4 4 4 4 5 7 7 7 7 7 7
4 4 4 4 4 4 5 7 7 7 7 7 7
5 5 5 2 5 5 5 5 5 8 5 5 5
2 2 2 2 2 2 5 8 8 8 8 8 8
2 2 2 2 2 2 5 8 8 8 8 8 8
2 2 2 2 2 2 0 8 8 8 8 8 8
2 2 2 2 2 2 5 8 8 8 8 8 8
2 2 2 2 2 2 5 8 8 8 8 8 8
```

### Test pairs

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 5 0 0
0 4 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
2 2 2 2 2 2 0 6 6 6 6 6 6
2 2 2 2 2 2 0 6 6 6 6 6 6
2 2 2 2 2 2 0 6 6 6 6 6 6
2 2 5 5 5 2 5 5 5 5 5 6 6
0 0 0 0 0 0 0 5 0 0 0 0 0
4 4 4 4 4 4 0 9 9 9 9 9 9
4 4 5 5 5 5 5 5 5 9 5 9 9
4 4 4 4 4 4 0 9 9 9 9 9 9
4 4 4 4 4 4 0 9 9 9 9 9 9
```
