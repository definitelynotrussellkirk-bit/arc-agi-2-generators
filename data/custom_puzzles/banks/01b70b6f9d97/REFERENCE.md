# ARC Puzzle Bank — Set 21


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.

New helper primitives in this batch:

- `row_span_fill`: Fill an inclusive row segment between matching same-color endpoints when the interior is empty.
- `diagonal_mid_fill`: Fill the midpoint between same-color diagonal endpoints that are exactly two steps apart.
- `four_diag_center`: Fill an empty center cell when all four diagonal neighbors share one nonzero color.
- `rectangle_fourth_corner`: Infer and complete the missing corner of an axis-aligned monochrome rectangle.
- `row_majority_filter`: Keep only the most frequent nonzero color in each row.
- `line_extend_one`: Extend a domino by one cell along its unique open continuation direction.
- `border_crosshair`: Project top-border markers down columns and left-border markers across rows.
- `color_key_crop`: Use the top-left color key to select which monochrome object to crop.
- `bbox_outline_union`: Replace each object by the outline of its tight bounding box.
- `marker_offset_clone`: Use two marker cells to define a translation vector for cloning an object.
- `symmetry_signature_recolor`: Recolor objects according to their reflection symmetry signature.
- `perimeter_gallery`: Crop objects and concatenate them sorted by bounding-box perimeter.
- `seeded_room_fill`: Flood each enclosed wall room with the room's single seed color.
- `corner_key_transform`: Apply a transform chosen by the top-left key to the main object and crop the result.
- `mirror_beam`: Trace an eastward beam through reflective mirrors until it hits a wall or exits the grid.
- `normalize_boolean`: Normalize two shapes to one origin and apply a keyed Boolean operation.
- `containment_depth`: Assign each object a color based on how many bounding boxes contain it.
- `contact_matrix`: Output a relation matrix for orthogonally touching monochrome objects.
- `script_timeline`: Emit the initial crop and every cumulative transform state in a gallery.
- `frame_fit_insert`: Insert each loose object into the frame whose interior size exactly matches its crop.
- `portal_checkpoint_path`: Find a shortest path through a checkpoint using linked portals.

## easy_p01 — Row Span Fill (easy)

**Tags:** rows, endpoints, same_size

**Written rule:** In each row, whenever a nonzero color appears exactly twice and every cell between those two endpoints is 0, fill the full inclusive horizontal span with that color.

**Program:** `solve_easy_p01`

**Primitives:** `row_span_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0
0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0
0 0 8 0 8 0 0
0 0 0 0 0 0 0
9 0 0 0 0 0 9
0 0 0 0 0 0 0
0 4 0 0 0 4 0
0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0
0 0 8 8 8 0 0
0 0 0 0 0 0 0
9 9 9 9 9 9 9
0 0 0 0 0 0 0
0 4 4 4 4 4 0
0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0
```

## easy_p02 — Diagonal Midpoint Fill (easy)

**Tags:** diagonals, midpoints, same_size

**Written rule:** Whenever two cells of the same nonzero color lie exactly two steps apart on a diagonal and the midpoint is empty, fill that midpoint with the same color.

**Program:** `solve_easy_p02`

**Primitives:** `diagonal_mid_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 4 0
0 2 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 2 0 0 0
0 6 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 6 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 4 0
0 2 0 0 4 0 0
0 0 2 4 0 0 0
0 0 0 2 0 0 0
0 6 0 0 0 0 0
0 0 6 0 0 0 0
0 0 0 6 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 5 0 0 0 0 0 0
0 0 0 0 3 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 5 0 0 0 3 0 0
0 0 5 0 3 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7
```

#### Train 3 input
```text
8 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 2 0 0
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0
```

#### Train 3 output
```text
8 0 0 0 0 0 0 0 2
0 8 0 0 0 0 0 2 0
0 0 8 0 0 0 2 0 0
0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 2 0 0 0 0
0 0 0 0 4 0 0 0
6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 2 0 0 0 4 0
0 0 0 2 0 4 0 0
0 0 0 0 4 0 0 0
6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0
```

## easy_p03 — Diagonal Cross Center (easy)

**Tags:** diagonals, local, completion

**Written rule:** If an empty cell is surrounded on all four diagonals by the same nonzero color, fill the center with that color.

**Program:** `solve_easy_p03`

**Primitives:** `four_diag_center`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0
0 2 0 2 0 0 0
0 0 0 0 0 0 0
0 2 0 2 6 0 6
0 0 0 0 0 0 0
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0
0 2 0 2 0 0 0
0 0 2 0 0 0 0
0 2 0 2 6 0 6
0 0 0 0 0 6 0
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3
0 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3
0 0 0 0 0 0 3 0
0 0 0 0 0 3 0 3
0 5 0 5 0 0 0 0
0 0 5 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 4 0 4
0 0 8 0 0 0 0 4 0
0 8 0 8 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 5 0 0 0 0 0
0 5 0 5 0 0 0 0
0 0 0 0 8 0 8 0
0 0 0 0 0 8 0 0
0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0
```

## easy_p04 — Fourth Rectangle Corner (easy)

**Tags:** rectangles, corners, completion

**Written rule:** Whenever three corners of an axis-aligned rectangle are present in the same nonzero color and the fourth corner is empty, fill the missing fourth corner with that color.

**Program:** `solve_easy_p04`

**Primitives:** `rectangle_fourth_corner`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0
0 7 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0
```

#### Train 3 input
```text
4 0 0 4 0 0 0 0 0
0 0 0 0 0 0 9 0 9
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
4 0 0 4 0 0 0 0 0
0 0 0 0 0 0 9 0 9
4 0 0 4 0 0 0 0 0
0 0 0 0 0 0 9 0 9
0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0
```

## easy_p05 — Row Majority Filter (easy)

**Tags:** rows, frequency, filtering

**Written rule:** For each row separately, keep only the cells whose nonzero color is the most frequent in that row, and turn all other cells in that row to 0.

**Program:** `solve_easy_p05`

**Primitives:** `row_majority_filter`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
2 2 0 3 0 2 0 3
4 0 4 4 5 0 5 0
0 6 6 0 7 6 0 0
8 0 9 9 9 0 8 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
2 2 0 0 0 2 0 0
4 0 4 4 0 0 0 0
0 6 6 0 0 6 0 0
0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0
5 1 5 0 1 5 0
2 2 2 3 0 3 0
4 0 4 4 0 0 6
0 7 7 8 7 8 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0
5 0 5 0 0 5 0
2 2 2 0 0 0 0
4 0 4 4 0 0 0
0 7 7 0 7 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
9 9 1 0 9 1 0 0 0
2 3 2 3 2 0 0 0 0
4 4 4 5 5 0 0 0 0
6 0 6 7 0 7 6 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
9 9 0 0 9 0 0 0 0
2 0 2 0 2 0 0 0 0
4 4 4 0 0 0 0 0 0
6 0 6 0 0 0 6 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0
3 3 1 0 3 1 0 0
5 0 5 5 2 2 0 0
7 8 7 0 8 7 0 0
9 0 9 4 0 9 4 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0
3 3 0 0 3 0 0 0
5 0 5 5 0 0 0 0
7 0 7 0 0 7 0 0
9 0 9 0 0 9 0 0
```

## easy_p06 — One-Step Segment Growth (easy)

**Tags:** segments, local, growth

**Written rule:** Every horizontal or vertical domino with exactly one open continuation cell grows by one step in that unique open direction.

**Program:** `solve_easy_p06`

**Primitives:** `line_extend_one`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
9 2 2 0 0 0 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 6 6 9
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
9 2 2 2 0 0 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 0
0 0 0 0 6 6 6 9
0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 9 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
9 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 9
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 9 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
9 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 9
0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 9 0 0
0 0 0 0 0 0 0 0 0
0 0 9 2 2 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 9 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 9 0 0
0 0 0 0 0 0 0 0 0
0 0 9 2 2 2 0 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 9 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0
9 2 2 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 9
0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0
9 2 2 2 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 7 7 7 9
0 0 0 0 0 0 0 0 0
```

## easy_p07 — Border Crosshair Projection (easy)

**Tags:** projection, rows, columns

**Written rule:** Every nonzero cell on the left border paints its entire row, every nonzero cell on the top border paints its entire column, and column paints override row paints at intersections.

**Program:** `solve_easy_p07`

**Primitives:** `border_crosshair`

### Train pairs

#### Train 1 input
```text
0 0 2 0 0 4 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
6 0 0 0 0 0 0
0 0 0 0 0 0 0
7 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 2 0 0 4 0
0 0 2 0 0 4 0
0 0 2 0 0 4 0
6 6 2 6 6 4 6
0 0 2 0 0 4 0
7 7 2 7 7 4 7
```

#### Train 2 input
```text
0 3 0 0 0 0 5 0
0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 3 0 0 0 0 5 0
0 3 0 0 0 0 5 0
8 3 8 8 8 8 5 8
0 3 0 0 0 0 5 0
0 3 0 0 0 0 5 0
0 3 0 0 0 0 5 0
2 3 2 2 2 2 5 2
```

#### Train 3 input
```text
0 0 0 0 9 0 0 0 6
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 9 0 0 0 6
4 4 4 4 9 4 4 4 6
0 0 0 0 9 0 0 0 6
0 0 0 0 9 0 0 0 6
5 5 5 5 9 5 5 5 6
```

### Test pair

#### Test 1 input
```text
0 2 0 0 0 0 5 0
0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 2 0 0 0 0 5 0
0 2 0 0 0 0 5 0
7 2 7 7 7 7 5 7
0 2 0 0 0 0 5 0
0 2 0 0 0 0 5 0
3 2 3 3 3 3 5 3
```

## medium_p01 — Keyed Color Crop (medium)

**Tags:** crop, selection, keys

**Written rule:** The top-left cell is a color key. Find the monochrome object of that color elsewhere in the grid and output its tight crop, ignoring the key cell itself.

**Program:** `solve_medium_p01`

**Primitives:** `color_key_crop`

### Train pairs

#### Train 1 input
```text
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0
0 0 3 0 0 0 0 5 0
0 0 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
3 0
3 0
3 3
```

#### Train 2 input
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 6 0 0 7 7
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
6 0
6 6
0 6
```

#### Train 3 input
```text
2 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 9 0 0 0 0 0 0
0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
2 2 2
0 2 0
0 2 0
```

### Test pair

#### Test 1 input
```text
8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6
0 0 8 8 0 0 0 0 6 0
0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
8 8 0
0 8 8
```

## medium_p02 — Bounding-Box Outline (medium)

**Tags:** objects, bounding_boxes, same_size

**Written rule:** Replace each connected monochrome object by the outline of its tight axis-aligned bounding box in the same color.

**Program:** `solve_medium_p02`

**Primitives:** `bbox_outline_union`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0
0 0 7 0 0 0 9 0 0
0 0 7 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0
0 7 7 0 0 0 9 9 0
0 7 7 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 8 0 0 0
0 0 4 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 0 8 8 0 0
0 4 4 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## medium_p03 — Marker Vector Clone (medium)

**Tags:** translation, markers, duplication

**Written rule:** The cells 1 and 2 define a translation vector from 1 to 2. Remove the markers and duplicate the main non-marker object by that vector while keeping the original in place.

**Program:** `solve_medium_p03`

**Primitives:** `marker_offset_clone`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 1 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 1 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 1 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## medium_p04 — Symmetry Signature Recolor (medium)

**Tags:** symmetry, recolor, objects

**Written rule:** Recolor each object by its reflection symmetry: both left-right and top-bottom symmetric → 2, left-right symmetric only → 3, top-bottom symmetric only → 4, and neither → 6.

**Program:** `solve_medium_p04`

**Primitives:** `symmetry_signature_recolor`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 5 0 5 0 0
0 8 8 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 0 3 0 0
0 2 2 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 4 4 0 0 0 0 3 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 2 2 0 0 0 0 6 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 8 8 0 0
0 6 6 6 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 4 4 0 0
0 3 3 3 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 9 9 0 0 0
0 8 8 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 0 0 0
0 2 2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## medium_p05 — Perimeter Gallery (medium)

**Tags:** packing, sorting, cropping

**Written rule:** Crop every monochrome object, sort the crops by bounding-box perimeter from smallest to largest, and place them left-to-right with one empty column between neighbors.

**Program:** `solve_medium_p05`

**Primitives:** `perimeter_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 6 0 6 0
0 0 2 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 4 0 6 0 6 0 2 2 2
4 4 0 6 6 6 0 0 2 0
0 0 0 0 0 0 0 0 2 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 7 7 0
0 3 3 3 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 7 0 3 0 3 0 5 5 5
7 7 0 3 3 3 0 0 5 0
0 0 0 0 0 0 0 0 5 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 2 2 2 0
0 8 8 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 9 0 9 0 0 0 0 0 0
0 0 0 0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
8 8 0 9 0 9 0 2 2 2
8 8 0 9 9 9 0 0 2 0
0 0 0 0 0 0 0 0 2 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
4 4 0 2 0 2 0 6 6 6
4 4 0 2 2 2 0 0 6 0
0 0 0 0 0 0 0 0 6 0
```

## medium_p06 — Seeded Room Fill (medium)

**Tags:** walls, flood_fill, rooms

**Written rule:** Walls are color 8. Each enclosed room contains exactly one seed color; fill all empty cells in that room with the seed color while leaving walls unchanged.

**Program:** `solve_medium_p06`

**Primitives:** `seeded_room_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 8 8 8 8 0
0 8 2 0 8 0 0 8 0 0 8 0
0 8 0 0 8 0 0 8 5 0 8 0
0 8 8 8 8 0 0 8 0 0 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 8 8 8 8 0
0 8 2 2 8 0 0 8 5 5 8 0
0 8 2 2 8 0 0 8 5 5 8 0
0 8 8 8 8 0 0 8 5 5 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 0 3 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0
0 0 0 0 8 0 7 0 8 0
0 0 0 0 8 0 0 0 8 0
0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 3 3 3 8 0 0 0 0
0 8 3 3 3 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 0 0 0 8 8 8 8 8 0
0 0 0 0 8 7 7 7 8 0
0 0 0 0 8 7 7 7 8 0
0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0
0 8 0 0 8 0 8 8 8 8 0
0 8 4 0 8 0 8 0 0 8 0
0 8 0 0 8 0 8 0 0 8 0
0 8 0 0 8 0 8 0 6 8 0
0 8 8 8 8 0 8 0 0 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0
0 8 4 4 8 0 8 8 8 8 0
0 8 4 4 8 0 8 6 6 8 0
0 8 4 4 8 0 8 6 6 8 0
0 8 4 4 8 0 8 6 6 8 0
0 8 8 8 8 0 8 6 6 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 8 8 8 8 0
0 8 2 0 8 0 0 8 0 0 8 0
0 8 0 0 8 0 0 8 0 0 8 0
0 8 8 8 8 0 0 8 5 0 8 0
0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 8 8 8 8 0
0 8 2 2 8 0 0 8 5 5 8 0
0 8 2 2 8 0 0 8 5 5 8 0
0 8 8 8 8 0 0 8 5 5 8 0
0 0 0 0 0 0 0 8 5 5 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p07 — Corner-Key Transform Crop (medium)

**Tags:** transform, keys, crop

**Written rule:** The top-left cell is a transform key: 1 = rotate 90°, 2 = rotate 180°, 3 = rotate 270°, 4 = horizontal flip. Apply that transform to the main object and output the transformed tight crop.

**Program:** `solve_medium_p07`

**Primitives:** `corner_key_transform`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 5
5 5
5 0
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 0
7 7
0 7
```

#### Train 3 input
```text
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0
0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
9 0 9
9 9 9
```

### Test pair

#### Test 1 input
```text
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 6
0 6 6
6 6 0
```

## hard_p01 — Mirror Beam Trace (hard)

**Tags:** simulation, mirrors, path

**Written rule:** Start a beam at the 1 cell moving east. Mirrors 2 and 3 reflect the beam like / and \ respectively, walls 8 stop it, and every traversed empty cell becomes 7.

**Program:** `solve_hard_p01`

**Primitives:** `mirror_beam`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 7 7 7 3 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 7 7 3 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 1 7 7 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 3 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 7 7 7 3 0 0 0 0 0 0
0 0 8 0 0 7 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0 0 0 0
0 0 3 7 7 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 3 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 7 7 7 7 3 0 0 0 0 0
0 0 0 8 0 0 7 0 0 0 0 0
0 0 0 7 0 0 7 0 0 0 0 0
0 0 0 7 0 0 7 0 0 0 0 0
0 0 0 3 7 7 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p02 — Keyed Normalized Boolean (hard)

**Tags:** boolean, normalization, keys

**Written rule:** The top-left key chooses a Boolean operation on the normalized color-4 and color-6 shapes: 1 = union, 2 = intersection, 3 = xor. Crop both shapes to their own boxes, align their top-left corners, apply the chosen operation, and output the result in color 8.

**Program:** `solve_hard_p02`

**Primitives:** `normalize_boolean`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
8 8
8 8
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
8 0
0 8
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 6 0 0 0
0 0 0 4 4 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 8 0
8 0 8
0 8 8
```

### Test pair

#### Test 1 input
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 6 0 6 0
0 4 4 4 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
8 8 8
8 8 8
8 8 8
```

## hard_p03 — Containment Depth Recolor (hard)

**Tags:** nesting, containment, recolor

**Written rule:** Recolor every nonzero component according to its bounding-box containment depth: outermost objects become 2, objects inside one containing box become 3, inside two become 4, and so on.

**Program:** `solve_hard_p03`

**Primitives:** `containment_depth`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 0 0
0 5 0 0 0 0 0 0 0 4 0
0 5 0 6 6 6 6 6 0 5 0
0 5 0 6 0 0 0 6 0 5 0
0 5 0 6 0 7 0 6 0 5 0
0 5 0 6 0 0 0 6 0 5 0
0 5 0 6 6 6 6 6 0 5 0
0 5 0 0 0 0 0 0 0 5 0
0 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0
0 2 0 0 0 0 0 0 0 3 0
0 2 0 3 3 3 3 3 0 2 0
0 2 0 3 0 0 0 3 0 2 0
0 2 0 3 0 4 0 3 0 2 0
0 2 0 3 0 0 0 3 0 2 0
0 2 0 3 3 3 3 3 0 2 0
0 2 0 0 0 0 0 0 0 2 0
0 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 0
0 8 0 4 4 4 4 4 0 0 8 0
0 8 0 4 9 9 9 4 0 0 8 0
0 8 0 4 9 0 9 4 0 0 8 0
0 8 0 4 9 9 9 4 0 0 8 0
0 8 0 4 4 4 4 4 0 0 8 0
0 8 3 0 0 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 2 0 3 3 3 3 3 0 0 2 0
0 2 0 3 4 4 4 3 0 0 2 0
0 2 0 3 4 0 4 3 0 0 2 0
0 2 0 3 4 4 4 3 0 0 2 0
0 2 0 3 3 3 3 3 0 0 2 0
0 2 3 0 0 0 0 0 0 0 2 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 6 6 6 6 0
0 2 0 0 0 2 0 0 6 0 0 6 0
0 2 0 5 0 2 0 0 6 7 7 6 0
0 2 0 0 0 2 0 0 6 7 7 6 0
0 2 0 0 0 2 0 0 6 7 7 6 0
0 2 0 0 0 2 0 0 6 0 0 6 0
0 2 2 2 2 2 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 2 2 2 2 0
0 2 0 0 0 2 0 0 2 0 0 2 0
0 2 0 3 0 2 0 0 2 3 3 2 0
0 2 0 0 0 2 0 0 2 3 3 2 0
0 2 0 0 0 2 0 0 2 3 3 2 0
0 2 0 0 0 2 0 0 2 0 0 2 0
0 2 2 2 2 2 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 0
0 5 6 6 6 6 6 6 6 5 0
0 5 6 0 0 0 0 0 6 5 0
0 5 6 0 0 0 0 0 6 5 0
0 5 6 0 0 7 0 0 6 5 0
0 5 6 0 0 0 0 0 6 5 0
0 5 6 0 0 0 0 0 6 5 0
0 5 6 6 6 6 6 6 6 5 0
0 5 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 0
0 2 3 3 3 3 3 3 3 2 0
0 2 3 0 0 0 0 0 3 2 0
0 2 3 0 0 0 0 0 3 2 0
0 2 3 0 0 4 0 0 3 2 0
0 2 3 0 0 0 0 0 3 2 0
0 2 3 0 0 0 0 0 3 2 0
0 2 3 3 3 3 3 3 3 2 0
0 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

## hard_p04 — Contact Matrix (hard)

**Tags:** relations, matrices, objects

**Written rule:** Sort monochrome objects from left to right and output an N×N relation matrix. Put 5 on the diagonal, 7 off-diagonal when two differently colored objects touch orthogonally in the input, and 0 otherwise.

**Program:** `solve_hard_p04`

**Primitives:** `contact_matrix`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0
2 2 3 0 0 4 0 0
0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
5 7 0
7 5 0
0 0 5
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 5 6 6 0 0 0 0 0 0
0 0 0 6 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
5 7 0 0
7 5 7 0
0 7 5 0
0 0 0 5
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0
0 9 0 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 6 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
5 0 0
0 5 7
0 7 5
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 3 0 0 0 0 0 0 0 0
0 0 3 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
5 7 0 0
7 5 7 0
0 7 5 0
0 0 0 5
```

## hard_p05 — Transform Timeline Gallery (hard)

**Tags:** scripts, transforms, gallery

**Written rule:** Read transform codes from the top row until the first 0. Starting from the cropped object below, output a left-to-right gallery containing the initial crop and then every cumulative transform state after applying the codes in order.

**Program:** `solve_hard_p05`

**Primitives:** `script_timeline`

### Train pairs

#### Train 1 input
```text
1 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
5 0 0 0 0 5 5 0 5 5 0 0 5 0 0
5 5 0 0 5 5 0 0 0 5 5 0 5 5 0
0 5 5 0 5 0 0 0 0 0 5 0 0 5 5
```

#### Train 2 input
```text
4 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 7 0 0 0 7 7 0 7 0 0
0 7 0 0 0 7 0 0 7 7 7
0 7 7 0 7 7 0 0 0 0 7
```

#### Train 3 input
```text
3 4 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
9 0 0 0 9 0 0 0 9 0 0 9 0
9 9 0 9 9 9 0 9 9 9 0 9 9
9 0 0 0 0 0 0 0 0 0 0 9 0
```

### Test pair

#### Test 1 input
```text
4 3 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
7 0 7 0 7 0 7 0 7 7 0 7 0 7
7 7 0 0 0 7 7 0 0 7 0 0 7 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0
```

## hard_p06 — Exact Frame Fit Insert (hard)

**Tags:** assignment, frames, insertion

**Written rule:** Identify hollow rectangular frames and loose objects. Match each loose object to the frame whose interior height and width exactly equal that object's tight crop dimensions, remove the loose objects from their original locations, and insert each crop into its matching frame interior.

**Program:** `solve_hard_p06`

**Primitives:** `frame_fit_insert`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 3 3 3 3 0 0
0 2 0 0 0 2 0 0 3 0 0 3 0 0
0 2 0 0 0 2 0 0 3 0 0 3 0 0
0 2 2 2 2 2 0 0 3 0 0 3 0 0
0 0 0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 6 6 0 0 0 0
0 4 4 4 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 3 3 3 3 0 0
0 2 4 0 4 2 0 0 3 6 6 3 0 0
0 2 4 4 4 2 0 0 3 0 6 3 0 0
0 2 2 2 2 2 0 0 3 6 6 3 0 0
0 0 0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 7 7 7 7 7 0
0 5 0 0 5 0 0 7 0 0 0 7 0
0 5 0 0 5 0 0 7 7 7 7 7 0
0 5 0 0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 9 9 9 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 7 7 7 7 7 0
0 5 8 0 5 0 0 7 9 9 9 7 0
0 5 8 8 5 0 0 7 7 7 7 7 0
0 5 8 0 5 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 4 4 4 4 4 0 0 0
0 2 0 0 2 0 0 4 0 0 0 4 0 0 0
0 2 2 2 2 0 0 4 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 8 0 0 6 0 5 5 0 0 0 0 0 0 0
0 8 8 0 6 0 0 5 5 0 3 3 0 0 0
0 6 8 0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 4 4 4 4 4 0 0 0
0 2 3 3 2 0 0 4 5 5 0 4 0 0 0
0 2 2 2 2 0 0 4 0 5 5 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 4 4 4 4 4 0 0 0
0 2 0 0 2 0 4 0 0 0 4 0 0 0
0 2 2 2 2 0 4 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 4 4 4 4 4 0 0 0
0 2 5 5 2 0 4 7 0 7 4 0 0 0
0 2 2 2 2 0 4 7 7 7 4 0 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p07 — Portal Checkpoint Path (hard)

**Tags:** pathfinding, portals, checkpoints

**Written rule:** Find a shortest path from 1 to 2 that visits the checkpoint 3 first. Cells 4 are a linked portal pair: stepping onto one instantly teleports to the other. Walls 8 are impassable, and every traversed empty path cell becomes 7.

**Program:** `solve_hard_p07`

**Primitives:** `portal_checkpoint_path`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 4 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 3 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 4 0 0 0 0
0 0 0 0 0 8 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 7 7 4 8 0 0 0 0 0 0
0 0 0 0 0 8 0 7 7 3 0 0
0 0 0 0 0 8 0 7 0 7 0 0
0 0 0 0 0 8 0 7 0 7 0 0
0 0 0 0 0 8 0 7 0 7 0 0
0 0 0 0 0 8 0 4 0 7 0 0
0 0 0 0 0 8 0 0 0 7 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 3 0 0 0 0 0 8 0 0 0
0 0 0 0 4 0 0 0 8 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 4 0 0
0 7 0 0 0 0 0 0 0 7 7 0
0 7 8 8 8 8 8 8 8 8 7 0
0 7 0 0 0 0 0 0 8 0 7 0
0 7 0 0 0 0 0 0 8 0 7 0
0 7 3 0 0 0 0 0 8 0 7 0
0 0 7 7 4 0 0 0 8 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 8 0 0 0 0 0 0 2 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 4 0 8 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 0 0
0 0 0 0 8 0 4 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 8 0 0 0 0 0 0 2 0
0 7 0 0 8 0 0 0 0 0 0 7 0
0 7 4 0 8 0 0 0 0 0 0 7 0
0 0 0 0 8 0 0 0 0 0 0 7 0
0 0 0 0 8 0 0 0 0 0 0 7 0
0 0 0 0 8 8 8 8 8 8 8 7 0
0 0 0 0 8 0 4 7 7 7 7 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 8 0 0 0 0 0 2 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 4 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 8 0 4 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 8 0 0 0 0 0 2 0
0 7 0 0 0 8 0 0 0 0 0 7 0
0 7 7 4 0 8 0 0 0 0 0 7 0
0 0 0 0 0 8 0 0 0 0 0 7 0
0 0 0 0 0 8 0 0 0 0 0 7 0
0 0 0 0 0 8 0 0 0 0 0 7 0
0 0 0 0 0 8 8 8 8 8 8 7 0
0 0 0 0 0 8 0 4 7 7 7 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
