# ARC Puzzle Bank — Set 20


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `column_span_fill`: Fill an inclusive column segment between matching same-color endpoints when the interior is empty.
- `anti_diagonal_union`: Copy every nonzero cell across the anti-diagonal and keep the originals.
- `seed_plus`: Expand each isolated seed into a radius-1 plus of the same color.
- `missing_corner_fill2`: Complete a 2x2 block that has three cells of one nonzero color and one empty corner.
- `inward_border_beam`: Fire a straight beam inward from each border seed until a wall or the grid edge.
- `domino_square_grow`: Expand a same-color domino into a filled 2x2 square in the only open orthogonal direction.
- `aligned_midpoint_fill`: Fill the midpoint between aligned same-color endpoints separated by one empty cell.
- `orientation_recolor`: Recolor each connected object by whether its bounding box is horizontal, vertical, or square.
- `bbox_outline`: Replace each object by the outline of its tight axis-aligned bounding box.
- `corner_key_extract`: Use the top-left color key to select one object color and crop that object.
- `axis_key_reflect`: Use a marker key to choose horizontal versus vertical reflection of the cropped object.
- `room_fill`: Flood each wall-enclosed room with the room's single seed color.
- `size_sorted_strip`: Extract object crops and concatenate them in ascending area order.
- `marker_count_scale`: Scale an object by the number of marker cells in a control row.
- `keyed_frame_insert`: Select an object by color key, transform it by a second key, and center it inside a frame.
- `key_door_portal_bfs`: Run shortest-path search with inventory state, locked doors, and paired teleport portals.
- `holecount_frame_assign`: Match template objects to frames by topological hole count and recolor them to the frame.
- `boolean_transform_compose`: Transform one normalized shape, align it with another, and apply a keyed Boolean operation.
- `ordered_waypoint_path`: Find a shortest path that visits checkpoints in increasing order before reaching the goal.
- `scripted_gallery`: Apply a sequence of transforms cumulatively and emit the intermediate states as a gallery.
- `dihedral_anchor_stamp`: Stamp transformed copies of a template at anchor positions using dihedral transform keys.

## easy_p01 — Column Span Fill (easy)

**Tags:** columns, endpoints, same_size

**Written rule:** Whenever a column contains exactly two cells of the same nonzero color with only zeros between them, fill the full inclusive vertical span with that color.

**Program:** `solve_easy_p01`

**Primitives:** `column_span_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 6 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
```

#### Train 1 output
```text
0 0 0 0 6 0 0 0 0
0 2 0 0 6 0 0 0 0
0 2 0 0 6 0 0 3 0
0 2 0 0 6 0 0 3 0
0 2 0 0 6 0 0 3 0
0 2 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
```

#### Train 2 input
```text
0 0 0 0 0 0 7 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 4 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 7 0 0 0
0 0 4 0 0 0 7 0 0 0
0 0 4 0 0 0 7 0 5 0
0 0 4 0 0 0 7 0 5 0
0 0 4 0 0 0 0 0 5 0
0 0 4 0 0 0 0 0 5 0
0 0 4 0 0 0 0 0 0 0
```

#### Train 3 input
```text
9 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
```

#### Train 3 output
```text
9 0 0 0 0 0 0 0
9 0 0 0 0 0 8 0
9 0 0 0 0 0 8 0
9 0 0 2 0 0 8 0
9 0 0 2 0 0 8 0
9 0 0 2 0 0 0 0
9 0 0 2 0 0 0 0
9 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 6 0
0 0 5 0 0 3 0 0 0 6 0
0 0 5 0 0 3 0 0 0 6 0
0 0 5 0 0 3 0 0 0 6 0
0 0 5 0 0 3 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
```

## easy_p02 — Anti-Diagonal Union (easy)

**Tags:** symmetry, anti_diagonal, same_size

**Written rule:** On a square grid, copy every nonzero cell across the anti-diagonal and keep the originals.

**Program:** `solve_easy_p02`

**Primitives:** `anti_diagonal_union`

### Train pairs

#### Train 1 input
```text
0 2 0 0 0 0
0 0 0 0 3 0
0 0 0 0 0 0
5 0 0 0 0 0
0 0 7 0 0 0
0 0 0 0 0 0
```

#### Train 1 output
```text
0 2 0 0 0 0
0 0 0 0 3 0
0 0 0 0 0 0
5 7 0 0 0 0
0 0 7 0 0 2
0 0 5 0 0 0
```

#### Train 2 input
```text
8 0 0 0 0 0 0
0 0 0 0 0 4 0
0 0 6 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 2 output
```text
8 0 0 0 0 0 0
0 0 0 0 0 4 0
0 0 6 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 6 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 8
```

#### Train 3 input
```text
0 0 0 9 0
0 2 0 0 0
0 0 0 0 0
0 0 0 0 5
0 0 0 0 0
```

#### Train 3 output
```text
0 5 0 9 0
0 2 0 0 9
0 0 0 0 0
0 0 0 2 5
0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 6 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 4
0 0 0 0 0 0 0
0 7 0 0 0 0 0
0 0 0 0 0 3 0
0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 6 0 4 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 4
0 0 0 0 0 0 0
0 7 0 0 0 0 6
0 0 7 0 0 3 0
0 0 0 0 0 0 0
```

## easy_p03 — Seed Plus Grow (easy)

**Tags:** local_growth, seeds, same_size

**Written rule:** Each isolated nonzero seed grows into a radius-1 plus of the same color: center, up, down, left, and right.

**Program:** `solve_easy_p03`

**Primitives:** `seed_plus`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 2 0 0 6 0 0
0 0 0 0 6 6 6 0
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 3 3 3
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 8 8 8 0 0 4 0
0 0 8 0 0 4 4 4
0 0 0 0 0 0 4 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 0 0 0
0 0 0 0 5 0 0 7 0
0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 7 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0
0 9 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
0 0 0 0 0 0 0
0 0 0 6 0 0 0
0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 9 0 0 0 0 0
9 9 9 0 0 0 0
0 9 0 0 0 2 0
0 0 0 0 2 2 2
0 0 0 6 0 2 0
0 0 6 6 6 0 0
0 0 0 6 0 0 0
```

## easy_p04 — Missing 2x2 Corner (easy)

**Tags:** local_completion, 2x2, same_size

**Written rule:** Whenever a 2x2 block contains exactly three cells of one nonzero color and one zero, fill the missing corner with that color.

**Program:** `solve_easy_p04`

**Primitives:** `missing_corner_fill2`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 2 0 0 0 0 6 0
0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0
0 2 2 0 0 6 6 0
0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 4 0 0 0
0 0 0 4 4 0 0
0 0 0 0 0 0 0
0 8 8 0 0 0 0
0 0 8 0 0 5 0
0 0 0 0 5 5 0
0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 4 4 0 0
0 0 0 4 4 0 0
0 0 0 0 0 0 0
0 8 8 0 0 0 0
0 8 8 0 5 5 0
0 0 0 0 5 5 0
0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 0
0 0 7 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 3 3 0
0 0 7 7 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 9 0 0 0 0 0 0
9 9 0 0 0 0 0 0
0 0 0 0 2 2 0 0
0 0 0 0 2 0 0 0
0 6 0 0 0 0 0 0
0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
9 9 0 0 0 0 0 0
9 9 0 0 0 0 0 0
0 0 0 0 2 2 0 0
0 0 0 0 2 2 0 0
0 6 6 0 0 0 0 0
0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## easy_p05 — Inward Border Beam (easy)

**Tags:** beam, border, walls

**Written rule:** Every colored seed on the border fires a straight beam inward, painting zeros until the beam hits a wall cell 8 or leaves the grid.

**Program:** `solve_easy_p05`

**Primitives:** `inward_border_beam`

### Train pairs

#### Train 1 input
```text
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
3 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 8 8 0
5 2 5 5 5 5 5 5 5 5
0 2 0 0 8 0 0 0 0 0
0 2 0 0 8 0 0 0 0 0
0 2 0 0 8 0 0 0 0 0
3 2 3 3 8 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 4 0 0
0 0 0 0 8 0 0 0 0
0 8 8 8 8 8 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 7
0 0 0 0 8 0 0 0 0
0 0 2 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 4 0 0
0 0 0 0 8 0 4 0 0
0 8 8 8 8 8 4 0 0
0 0 2 0 8 0 4 0 0
0 0 2 0 8 7 4 7 7
0 0 2 0 8 0 4 0 0
0 0 2 0 0 0 4 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 3 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0
5 0 0 0 0 8 0 0 0
0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 6 0 0 0 0 0 3 0
0 6 0 0 0 8 0 3 0
0 6 0 0 0 8 0 3 0
5 6 5 5 5 8 0 3 0
0 6 8 8 8 8 8 8 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 8 8 8 0
0 0 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 2
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
```

#### Test 1 output
```text
0 0 0 9 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 8 9 0 0 0 0 0 0 0
0 0 8 9 0 0 8 8 8 8 0
0 0 8 9 0 0 0 4 0 0 0
0 0 8 9 2 2 2 4 2 2 2
0 0 8 9 0 0 0 4 0 0 0
0 0 0 9 0 0 0 4 0 0 0
```

## easy_p06 — Domino Square Grow (easy)

**Tags:** domino, growth, same_size

**Written rule:** A horizontal same-color domino grows downward into a 2x2 square, and a vertical same-color domino grows rightward into a 2x2 square.

**Program:** `solve_easy_p06`

**Primitives:** `domino_square_grow`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 3 3
0 0 0 0 0 0 0 3 3
0 0 0 0 0 6 6 0 0
0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 5 5 0 0
0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 0 0 0 4 4 0
0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
3 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
3 3 7 7 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 6 0 0 0 0
0 5 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## easy_p07 — Midpoint Bridge (easy)

**Tags:** midpoint, alignment, same_size

**Written rule:** If two same-color cells lie in the same row or column with exactly one zero between them, fill the midpoint with that color.

**Program:** `solve_easy_p07`

**Primitives:** `aligned_midpoint_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 6 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0
```

#### Train 2 output
```text
0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 8 0 0 0 4 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
3 0 7 7 7 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 6 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 0
0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
```

## medium_p01 — Orientation Recolor (medium)

**Tags:** objects, orientation, recolor

**Written rule:** Detect each connected object and recolor it by the shape of its bounding box: horizontal objects become 2, vertical objects become 3, and square objects become 4.

**Program:** `solve_medium_p01`

**Primitives:** `orientation_recolor`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 9 9 0 7 0 0
0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 4 4 0 3 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 8 0
3 3 3 0 0 0 0 8 0
3 3 3 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 3 0
4 4 4 0 0 0 0 3 0
4 4 4 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 2 2 2 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 2 2 2 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## medium_p02 — Bounding Box Outline (medium)

**Tags:** objects, bbox, outline

**Written rule:** Replace every object by the outline of its tight axis-aligned bounding box, using the object's original color.

**Program:** `solve_medium_p02`

**Primitives:** `bbox_outline`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 6 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 6 6 6 0
0 0 4 4 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0
0 0 0 0 8 0 0 3 0 3 0
0 0 0 0 8 8 0 3 3 3 0
0 5 5 0 0 8 8 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 8 8 8 3 0 3 0
0 0 0 0 8 0 8 3 3 3 0
0 5 5 0 8 8 8 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 9 9 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 9 9 9 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 4 0 4 0 0 0 0 3 3 0
0 0 4 0 4 0 0 0 0 0 3 3
0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 4 4 4 0 0 0 0 3 0 3
0 0 4 0 4 0 0 0 0 3 3 3
0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p03 — Corner-Key Extract (medium)

**Tags:** selection, crop, color_key

**Written rule:** The top-left corner gives a color key. Extract only the object of that color and return its tight crop.

**Program:** `solve_medium_p03`

**Primitives:** `corner_key_extract`

### Train pairs

#### Train 1 input
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 8 8 0
0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
6 0
6 0
6 6
```

#### Train 2 input
```text
4 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0
0 0 7 7 0 0 0 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 4 0 4 2 0
0 0 0 0 4 0 4 0 0
0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 4
4 0 4
4 4 4
```

#### Train 3 input
```text
9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
9 9
9 9
9 0
```

### Test pair

#### Test 1 input
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 7 0
0 0 2 0 0 0 0 0 7 0
0 0 2 2 0 0 0 0 7 0
0 0 0 2 2 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
2 0 0
2 2 0
0 2 2
```

## medium_p04 — Axis-Key Reflect (medium)

**Tags:** reflection, crop, marker_key

**Written rule:** The top-left key chooses an axis: 1 means reflect the cropped object horizontally, and 2 means reflect it vertically.

**Program:** `solve_medium_p04`

**Primitives:** `axis_key_reflect`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0
0 0 2 3 3 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
3 0 2
3 3 2
```

#### Train 2 input
```text
2 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 4 5 0 0
0 0 0 5 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 5
4 5
4 0
```

#### Train 3 input
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 7 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 7 6
7 7 0
```

### Test pair

#### Test 1 input
```text
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0
0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
8 8 0
8 0 8
```

## medium_p05 — Room Fill from Doors (medium)

**Tags:** flood_fill, rooms, walls

**Written rule:** Walls are color 8. Each enclosed room contains one colored door/seed; fill every zero cell in that room with the room's seed color while leaving the walls unchanged.

**Program:** `solve_medium_p05`

**Primitives:** `room_fill`

### Train pairs

#### Train 1 input
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 2 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 0 6 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Train 1 output
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 6 6 6 6 8
8 2 2 2 2 8 6 6 6 6 8
8 2 2 2 2 8 6 6 6 6 8
8 2 2 2 2 8 6 6 6 6 8
8 2 2 2 2 8 6 6 6 6 8
8 2 2 2 2 8 6 6 6 6 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 input
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 8 0 0 0 8
8 0 0 4 0 0 0 8 0 7 0 8
8 0 0 0 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 8 0 0 0 0 0 0 0 8
8 3 0 8 0 0 0 0 5 0 0 8
8 0 0 8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 output
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 4 4 4 4 4 4 8 7 7 7 8
8 4 4 4 4 4 4 8 7 7 7 8
8 4 4 4 4 4 4 8 7 7 7 8
8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 8 5 5 5 5 5 5 5 8
8 3 3 8 5 5 5 5 5 5 5 8
8 3 3 8 5 5 5 5 5 5 5 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 input
```text
8 8 8 8 8 8 8 8 8 8
8 9 0 0 8 0 0 6 0 8
8 0 0 0 8 0 0 0 0 8
8 0 0 0 8 8 8 8 8 8
8 0 0 0 8 0 0 0 0 8
8 0 2 0 8 0 0 4 0 8
8 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

#### Train 3 output
```text
8 8 8 8 8 8 8 8 8 8
8 9 0 0 8 6 6 6 6 8
8 0 0 0 8 6 6 6 6 8
8 0 0 0 8 8 8 8 8 8
8 0 0 0 8 4 4 4 4 8
8 0 2 0 8 4 4 4 4 8
8 0 0 0 8 4 4 4 4 8
8 8 8 8 8 8 8 8 8 8
```

### Test pair

#### Test 1 input
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 3 0 0 0 0 7 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 8 0 0 0 8
8 0 0 0 0 0 8 0 0 0 8
8 0 5 0 0 0 8 0 0 0 8
8 0 0 0 0 0 8 0 2 0 8
8 0 0 0 0 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Test 1 output
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 3 0 0 0 0 7 0 8
8 8 8 8 8 8 8 8 8 8 8
8 5 5 5 5 5 8 2 2 2 8
8 5 5 5 5 5 8 2 2 2 8
8 5 5 5 5 5 8 2 2 2 8
8 5 5 5 5 5 8 2 2 2 8
8 5 5 5 5 5 8 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8
```

## medium_p06 — Size-Sorted Strip (medium)

**Tags:** gallery, sorting, resize

**Written rule:** Extract each object's tight crop and place the crops side by side, separated by one blank column, sorted from smallest area to largest.

**Program:** `solve_medium_p06`

**Primitives:** `size_sorted_strip`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
8 8 8 8 0 2 2 0 6 0
0 0 0 0 0 2 2 0 6 0
0 0 0 0 0 0 0 0 6 6
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 0 0
0 5 0 0 0 0 0 0 0 0 0
0 5 0 0 0 9 9 9 0 0 0
0 5 0 0 0 9 9 9 0 0 0
0 0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 0 3 3 3 0 9 9 9
5 0 0 3 0 0 9 9 9
5 0 0 0 0 0 9 9 9
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 2 2 2 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
7 7 0 4 4 0 0 2 0 2
7 7 0 0 4 4 0 2 0 2
0 0 0 0 0 0 0 2 2 2
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
6 6 6 0 3 3 0 8 8 8
0 0 0 0 3 3 0 8 0 8
0 0 0 0 3 0 0 8 8 8
```

## medium_p07 — Marker-Count Scale (medium)

**Tags:** scale, counting, resize

**Written rule:** Count the number of marker cells 1 in the top row. Scale the single object below by that factor using nearest-neighbor pixel replication.

**Program:** `solve_medium_p07`

**Primitives:** `marker_count_scale`

### Train pairs

#### Train 1 input
```text
1 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 2 0 0
2 2 0 0
2 2 2 2
2 2 2 2
```

#### Train 2 input
```text
1 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 3 3 3 3 3 3
0 0 0 3 3 3 3 3 3
0 0 0 3 3 3 3 3 3
3 3 3 3 3 3 0 0 0
3 3 3 3 3 3 0 0 0
3 3 3 3 3 3 0 0 0
```

#### Train 3 input
```text
1 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
4 4 4 4 0 0
4 4 4 4 0 0
0 0 4 4 4 4
0 0 4 4 4 4
```

### Test pair

#### Test 1 input
```text
1 0 1 0 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 5 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
5 5 5 0 0 0
5 5 5 0 0 0
5 5 5 0 0 0
5 5 5 5 5 5
5 5 5 5 5 5
5 5 5 5 5 5
0 0 0 5 5 5
0 0 0 5 5 5
0 0 0 5 5 5
```

## hard_p01 — Keyed Frame Insert (hard)

**Tags:** selection, transform, frame

**Written rule:** The top-left corner selects which object color to use. The top-right corner chooses a transform (1=rot90, 2=rot180, 3=flip horizontally, 4=identity). Transform that object's tight crop and center it inside the hollow frame of 8s.

**Program:** `solve_hard_p01`

**Primitives:** `keyed_frame_insert`

### Train pairs

#### Train 1 input
```text
6 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 7 7 0 0
0 6 0 0 0 0 8 8 8 8 8 0
0 6 0 0 0 0 8 0 0 0 8 0
0 6 6 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 9 9 9 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 6 6 6 8 0
0 0 0 0 0 0 8 6 0 0 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
7 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 6 6 6 0 0 0 8 0 0 8 0
0 0 0 6 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 8 0 0 8 0
0 7 0 0 0 0 0 0 8 0 0 8 0
0 7 7 0 0 0 0 0 8 8 8 8 0
0 0 7 7 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 7 7 0 8 0
0 0 0 0 0 0 0 0 8 7 7 8 0
0 0 0 0 0 0 0 0 8 0 7 8 0
0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
9 0 0 0 0 0 0 0 0 0 3
0 0 9 9 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 7 0 0
0 0 9 0 0 8 8 8 8 8 0
0 0 0 0 0 8 0 0 7 8 0
0 6 6 6 0 8 0 0 7 8 0
0 6 6 6 0 8 0 0 0 8 0
0 6 6 6 0 8 0 0 0 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 9 9 0 8 0
0 0 0 0 0 8 9 9 0 8 0
0 0 0 0 0 8 0 9 0 8 0
0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
6 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 8 7 7 8 0
0 0 0 0 0 0 0 8 0 0 8 0
0 6 0 6 0 0 0 8 0 0 8 0
0 6 0 6 0 0 0 8 0 0 8 0
0 6 6 6 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 6 0 6 8 0
0 0 0 0 0 0 0 6 0 6 8 0
0 0 0 0 0 0 0 6 6 6 8 0
0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p02 — Key-Door Portal Path (hard)

**Tags:** pathfinding, portal, state

**Written rule:** Find the shortest path from start 2 to goal 3. You may not pass through door 5 until you have picked up key 4. Stepping onto a portal 6 teleports you to the other portal. Mark the traversed zero cells with 7.

**Program:** `solve_hard_p02`

**Primitives:** `key_door_portal_bfs`

### Train pairs

#### Train 1 input
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 8 8 8 8 8 8 8
8 8 8 8 0 8 0 0 0 0 3 8 8
8 4 0 0 0 5 6 8 8 8 0 8 8
8 8 8 8 8 8 8 8 0 8 0 8 8
8 0 0 0 0 0 0 8 0 8 0 8 8
8 0 8 8 8 8 8 8 0 8 0 8 8
8 0 0 0 0 0 0 8 6 0 0 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 1 output
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 7 8 8 8 8 8 8 8 8
8 8 8 8 7 8 7 7 7 7 3 8 8
8 4 7 7 7 5 6 8 8 8 0 8 8
8 8 8 8 8 8 8 8 0 8 0 8 8
8 0 0 0 0 0 0 8 0 8 0 8 8
8 0 8 8 8 8 8 8 7 8 0 8 8
8 0 0 0 0 0 0 8 6 0 0 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 input
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 8 8 8 8 8 8
8 8 8 0 0 8 0 0 0 3 8 8
8 4 0 0 8 5 6 8 8 0 8 8
8 8 8 0 8 8 8 8 0 0 8 8
8 0 0 0 0 0 0 8 0 8 8 8
8 0 8 8 8 8 0 8 0 8 8 8
8 0 0 0 0 0 6 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 output
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 0 8 8 8 8 8 8 8
8 8 8 7 0 8 7 7 7 3 8 8
8 4 0 7 8 5 6 8 8 0 8 8
8 8 8 7 8 8 8 8 0 0 8 8
8 0 0 7 7 7 7 8 0 8 8 8
8 0 8 8 8 8 7 8 0 8 8 8
8 0 0 0 0 0 6 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 input
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 0 8 8 8 8 8 8 8
8 8 8 8 8 0 8 0 0 0 3 8 8
8 4 0 0 0 0 5 6 8 8 0 8 8
8 8 8 8 8 8 8 8 8 0 0 8 8
8 0 0 0 0 0 0 8 0 0 8 8 8
8 0 8 8 8 8 0 8 0 8 8 8 8
8 0 0 0 0 0 6 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 output
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 7 7 8 8 8 8 8 8 8
8 8 8 8 8 7 8 7 7 7 3 8 8
8 4 7 7 7 7 5 6 8 8 0 8 8
8 8 8 8 8 8 8 8 8 0 0 8 8
8 0 0 0 0 0 0 8 0 0 8 8 8
8 0 8 8 8 8 7 8 0 8 8 8 8
8 0 0 0 0 0 6 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

### Test pair

#### Test 1 input
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 8 8 8 8 8 8
8 8 8 0 0 8 0 0 0 3 8 8
8 4 0 0 8 5 0 8 8 0 8 8
8 8 8 0 8 8 6 8 0 0 8 8
8 0 0 0 0 0 0 8 0 8 8 8
8 0 8 8 8 8 0 8 0 8 8 8
8 0 0 0 0 0 6 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Test 1 output
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 0 8 8 8 8 8 8 8
8 8 8 7 0 8 7 7 7 3 8 8
8 4 0 7 8 5 7 8 8 0 8 8
8 8 8 7 8 8 6 8 0 0 8 8
8 0 0 7 7 7 7 8 0 8 8 8
8 0 8 8 8 8 7 8 0 8 8 8
8 0 0 0 0 0 6 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

## hard_p03 — Holecount Frame Assign (hard)

**Tags:** topology, frames, matching

**Written rule:** There are two template objects: one with no holes and one with one hole. Insert the no-hole template into the red frame 2 and the one-hole template into the green frame 3, centering each and recoloring it to match its frame.

**Program:** `solve_hard_p03`

**Primitives:** `holecount_frame_assign`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 2 2 2 2 0 0
0 6 0 0 0 0 0 2 0 0 2 0 0
0 6 6 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 2 2 2 2 0 0
0 7 7 7 0 0 0 0 3 3 3 3 0
0 7 0 7 0 0 0 0 3 0 0 3 0
0 7 7 7 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 2 2 0 2 0 0
0 0 0 0 0 0 0 2 2 0 2 0 0
0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 3 0 3 3 0
0 0 0 0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 8 8 0 0 0 0 2 0 0 0 2 0
0 0 8 8 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 5 5 5 5 0 0 0 0 3 3 3 3 3
0 5 0 0 5 0 0 0 0 3 0 0 0 3
0 5 0 0 5 0 0 0 0 3 0 0 0 3
0 5 5 5 5 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 2 2 2 0 2 0
0 0 0 0 0 0 0 0 2 2 2 0 2 0
0 0 0 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3 0 0 3 3
0 0 0 0 0 0 0 0 0 3 0 0 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 2 2 2 2 0
0 0 9 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0 2 2 2 2 0
0 6 6 6 0 0 0 0 0 3 3 3 3 3
0 6 0 6 0 0 0 0 0 3 0 0 0 3
0 6 6 6 0 0 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 2 2 0 2 0
0 0 0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 0 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 7 7 0 0 0 0 2 0 0 0 2 0
0 7 7 0 0 0 0 2 0 0 0 2 0
0 7 0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 0 0 0 3 3 3 3 3
0 9 0 0 9 0 0 0 3 0 0 0 3
0 9 0 0 9 0 0 0 3 0 0 0 3
0 9 9 9 9 0 0 0 3 0 0 0 3
0 0 0 0 0 0 0 0 3 3 3 3 3
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 0 2 0
0 0 0 0 0 0 0 2 2 2 0 2 0
0 0 0 0 0 0 0 2 2 0 0 2 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 3 0 0 3 3
0 0 0 0 0 0 0 0 3 0 0 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3
```

## hard_p04 — Boolean Transform Composer (hard)

**Tags:** boolean, transform, selection

**Written rule:** Use the top-left key to choose a set operation on two normalized shapes (1=union, 2=intersection, 3=xor). Use the top-right key to transform the second shape (6=identity, 7=flip horizontally, 8=rotate 90°). Output the resulting normalized shape in color 9.

**Program:** `solve_hard_p04`

**Primitives:** `boolean_transform_compose`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 5 5 5 0 0
0 4 0 0 0 0 0 0 5 0 0 0
0 4 4 4 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
9 9 9
9 9 0
9 9 9
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 5 5 0 0
0 4 4 4 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 9
9 9 0
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 4 4 0 0 0 0 5 5 0 0
0 0 0 4 0 0 0 0 5 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 9
0 0
9 0
```

### Test pair

#### Test 1 input
```text
1 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 5 5 0
0 0 4 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
9 9 9
9 9 0
0 9 0
```

## hard_p05 — Ordered Waypoint Path (hard)

**Tags:** pathfinding, ordering, maze

**Written rule:** Find a shortest path that starts at 2, visits every checkpoint in increasing color order (4, then 5, then 6 if present), and ends at 3. Mark the traversed zero cells with 7.

**Program:** `solve_hard_p05`

**Primitives:** `ordered_waypoint_path`

### Train pairs

#### Train 1 input
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 8 0 0 0 0 3 8
8 8 8 0 8 0 8 8 0 8 8
8 4 0 0 8 0 8 5 0 0 8
8 8 8 0 8 0 8 8 8 0 8
8 0 0 0 0 0 0 0 8 0 8
8 0 8 8 8 8 8 0 8 0 8
8 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Train 1 output
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 8 7 7 7 7 3 8
8 8 8 7 8 7 8 8 7 8 8
8 4 7 7 8 7 8 5 7 0 8
8 8 8 7 8 7 8 8 8 0 8
8 0 0 7 7 7 0 0 8 0 8
8 0 8 8 8 8 8 0 8 0 8
8 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 input
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 0 0 0 0 3 8
8 8 8 8 0 8 0 8 8 0 8 8
8 4 0 0 0 8 0 8 5 0 0 8
8 8 8 0 8 8 0 8 8 8 0 8
8 0 0 0 0 0 0 0 0 8 0 8
8 0 8 8 8 8 8 8 0 8 0 8
8 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 2 output
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 7 8 7 7 7 7 3 8
8 8 8 8 7 8 7 8 8 7 8 8
8 4 7 7 7 8 7 8 5 7 0 8
8 8 8 7 8 8 7 8 8 8 0 8
8 0 0 7 7 7 7 0 0 8 0 8
8 0 8 8 8 8 8 8 0 8 0 8
8 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 input
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 8 0 0 0 8 0 0 3 8
8 8 8 0 8 0 8 0 8 0 8 8 8
8 4 0 0 8 0 8 0 0 0 8 5 8
8 8 8 0 8 0 8 8 8 0 8 0 8
8 0 0 0 0 0 0 0 8 0 8 0 8
8 0 8 8 8 8 8 0 8 0 8 0 8
8 0 0 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

#### Train 3 output
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 8 0 0 0 8 7 7 3 8
8 8 8 7 8 0 8 0 8 7 8 8 8
8 4 7 7 8 0 8 0 0 7 8 5 8
8 8 8 7 8 0 8 8 8 7 8 7 8
8 0 0 7 7 7 7 7 8 7 8 7 8
8 0 8 8 8 8 8 7 8 7 8 7 8
8 0 0 0 0 0 0 7 7 7 7 7 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

### Test pair

#### Test 1 input
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 0 0 0 3 8
8 8 8 0 8 8 0 8 0 8 8
8 4 0 0 8 0 0 8 5 0 8
8 8 8 0 8 0 8 8 8 0 8
8 6 0 0 0 0 8 0 0 0 8
8 8 8 8 8 0 8 0 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

#### Test 1 output
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 7 7 0 8 7 7 7 3 8
8 8 8 7 8 8 7 8 7 8 8
8 4 7 7 8 7 7 8 5 0 8
8 8 8 7 8 7 8 8 8 0 8
8 6 7 7 7 7 8 0 0 0 8
8 8 8 8 8 0 8 0 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

## hard_p06 — Scripted Transform Gallery (hard)

**Tags:** transforms, gallery, composition

**Written rule:** Read the script in the top row from left to right. Starting with the cropped object below, apply each transform cumulatively (1=identity, 2=rot90, 3=flip horizontally, 4=rot180) and emit each intermediate state as a left-to-right gallery separated by one blank column.

**Program:** `solve_hard_p06`

**Primitives:** `scripted_gallery`

### Train pairs

#### Train 1 input
```text
2 0 3 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0
0 0 2 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
2 2 0 2 2 0 2 2
3 0 0 0 3 0 0 3
3 3 0 3 3 0 3 3
```

#### Train 2 input
```text
1 0 4 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 4 5 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 0 0 5 5 0 0 5 5
4 5 0 5 4 0 4 4 5
5 5 0 0 4 0 0 0 0
```

#### Train 3 input
```text
3 0 2 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 7 6 0 7 0 0 6 0
7 7 0 0 7 7 0 7 7
0 0 0 0 0 6 0 0 7
```

### Test pair

#### Test 1 input
```text
4 0 3 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 8 8 0 8 8 0 0 8 8
8 0 8 0 8 0 8 0 0 8
0 0 0 0 0 0 0 0 8 0
```

## hard_p07 — Dihedral Anchor Stamp (hard)

**Tags:** template, stamping, dihedral

**Written rule:** Take the multicolor template and stamp transformed copies at each anchor. Anchor colors choose the transform: 1=identity, 2=rot90, 3=rot180, 4=rot270, 5=flip horizontally. Each anchor marks the top-left corner of its stamped copy.

**Program:** `solve_hard_p07`

**Primitives:** `dihedral_anchor_stamp`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 7 0 0 0 1 0 0 0 0
0 6 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 7 0 0
0 0 0 0 0 0 0 6 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 7 0 6 0 7 7 0 0 0
0 0 0 7 7 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 6 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 8 6 0 0 0 6 6 0 0 0
0 0 0 0 6 6 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 8 0 0 0 0 0 0 0 0
0 7 8 0 0 0 0 2 0 0 0 0
0 7 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 7 0 0
0 0 8 0 8 0 0 0 8 7 0 0
0 0 0 8 8 0 0 8 8 7 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 6 0 0 0 0 0 0 0 0 0 0
0 0 6 0 5 0 0 0 1 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 9 0 0 9 6 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0
0 0 0 0 6 6 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 0 9 0 0
0 0 0 0 6 6 0 0 6 6 6 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 6 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
