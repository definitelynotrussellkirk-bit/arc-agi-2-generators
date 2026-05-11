# ARC Puzzle Bank — Set 19


This set contains 21 ARC-style puzzles split 7 easy / 7 medium / 7 hard.


New helper primitives in this batch:

- `row_span_fill`: Fill an inclusive row segment between matching same-color endpoints when the interior is empty.
- `crosshair_broadcast`: Broadcast a seed color across its entire row and column.
- `diagonal_union`: Copy every nonzero cell across the main diagonal and keep the originals.
- `odd_run_kernel`: Reduce each odd-length monochrome run to its center cell.
- `ring_center_fill`: Fill the center of a hollow 3x3 monochrome ring.
- `column_gravity`: Drop every column’s nonzero cells to the bottom while preserving order.
- `rectangle_corner_vote`: Infer the missing fourth corner of a three-corner rectangle.
- `area_rank_recolor`: Recolor objects by ordering them from smallest area to largest.
- `bbox_fill`: Replace each object by the solid fill of its axis-aligned bounding box.
- `corner_color_select`: Use a corner key color to select which object to crop.
- `frame_gallery`: Extract frame interiors and concatenate them as a gallery.
- `marker_count_rotate`: Use the number of marker cells to choose a rotation.
- `column_histogram`: Summarize an object by bottom-aligned column counts inside its bounding box.
- `hole_fill`: Fill zero regions that are fully enclosed by one surrounding color.
- `dual_key_select_transform`: One key chooses the object; another key chooses the transform.
- `portal_bfs`: Find a shortest path in a maze with teleport portals.
- `frame_pack_by_area`: Match objects to frames by ascending area and center them inside.
- `shape_boolean`: Align two cropped shapes and apply a keyed Boolean set operation.
- `transform_timeline`: Emit each intermediate transformed state in a left-to-right timeline.
- `contact_degree`: Build an object contact graph and recolor by node degree.
- `mirror_raytrace`: Trace a beam through slash and backslash mirrors until it exits or hits a wall.

## easy_p01 — Row Span Fill (easy)

**Tags:** rows, endpoints, same_size

**Written rule:** Whenever a row contains exactly two cells of the same nonzero color with only zeros between them, fill the entire inclusive span with that color.

**Program:** `solve_easy_p01`

**Primitives:** `row_span_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 4 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 3 0 0 3
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p02 — Seed Crosshair (easy)

**Tags:** projection, crosshair, same_size

**Written rule:** Each nonzero seed paints its full row and full column with its own color.

**Program:** `solve_easy_p02`

**Primitives:** `crosshair_broadcast`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 4 0 0 0
0 0 0 4 0 0 0
0 0 0 4 0 0 0
4 4 4 4 4 4 4
0 0 0 4 0 0 0
0 0 0 4 0 0 0
0 0 0 4 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2
0 2 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 8 0
8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
```

## easy_p03 — Main-Diagonal Reflection (easy)

**Tags:** symmetry, diagonal, same_size

**Written rule:** Copy every nonzero cell to its mirrored position across the main diagonal, while keeping all original cells.

**Program:** `solve_easy_p03`

**Primitives:** `diagonal_union`

### Train pairs

#### Train 1 input
```text
0 0 3 0 0 0
0 0 0 0 5 0
0 0 0 0 0 7
0 0 0 0 2 0
0 0 0 0 0 0
0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 3 0 0 0
0 0 0 0 5 0
3 0 0 0 0 7
0 0 0 0 2 0
0 5 0 2 0 0
0 0 7 0 0 0
```

#### Train 2 input
```text
0 0 0 4 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 8
0 0 0 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 4 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 8
4 0 0 0 0 2 0
0 0 0 0 0 0 0
0 6 0 2 0 0 0
0 0 8 0 0 0 0
```

#### Train 3 input
```text
0 7 0 0 0
0 0 0 4 0
0 0 0 0 6
0 0 0 0 0
0 0 0 0 0
```

#### Train 3 output
```text
0 7 0 0 0
7 0 0 4 0
0 0 0 0 6
0 4 0 0 0
0 0 6 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 2 0
0 0 0 5 0 0
0 0 0 0 0 8
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 2 0
0 0 0 5 0 0
0 0 0 0 0 8
0 5 0 0 0 0
2 0 0 0 0 0
0 0 8 0 0 0
```

## easy_p04 — Odd Run Centers (easy)

**Tags:** runs, row-wise, filtering

**Written rule:** For every horizontal monochrome run of odd length at least 3, keep only its center cell and erase the rest.

**Program:** `solve_easy_p04`

**Primitives:** `odd_run_kernel`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0
2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
9 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
```

## easy_p05 — Hollow Ring Centers (easy)

**Tags:** local_pattern, 3x3, completion

**Written rule:** Whenever eight cells of a 3×3 block form a same-color ring around a zero center, fill the center with that color.

**Program:** `solve_easy_p05`

**Primitives:** `ring_center_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 3 0 3 0 0 8 8 8 0
0 3 3 3 0 0 8 0 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 8 8 8 0
0 3 3 3 0 0 8 8 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
4 4 4 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 7 0 7 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
4 4 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 6 0 6 0 0
2 2 2 0 6 6 6 0 0
2 0 2 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 6 6 6 0 0
2 2 2 0 6 6 6 0 0
2 2 2 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 9 0 9 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## easy_p06 — Column Gravity (easy)

**Tags:** gravity, columns, same_size

**Written rule:** Within each column, let all nonzero cells fall to the bottom, preserving their top-to-bottom order.

**Program:** `solve_easy_p06`

**Primitives:** `column_gravity`

### Train pairs

#### Train 1 input
```text
0 3 0 0 0 0 5 0
0 0 0 8 0 0 0 0
0 0 0 0 0 0 5 0
0 4 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0
0 3 0 8 0 0 5 0
0 4 0 2 0 0 1 0
```

#### Train 2 input
```text
0 0 4 0 0 0 0
6 0 0 0 0 0 0
0 0 0 0 0 3 0
0 0 4 0 0 0 0
0 0 0 0 0 0 0
0 0 7 0 0 0 0
2 0 0 0 0 0 0
0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 4 0 0 0 0
6 0 4 0 0 0 0
2 0 7 0 0 3 0
```

#### Train 3 input
```text
0 8 0 0 0 0 0 6 0
0 0 0 0 5 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 5 0 0 6 0
0 8 0 0 2 0 0 1 0
```

### Test pair

#### Test input
```text
0 0 2 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 2 0 0 0 4 0
0 0 2 0 6 0 5 0
```

## easy_p07 — Missing Rectangle Corner (easy)

**Tags:** geometry, corners, completion

**Written rule:** If three corners of an axis-aligned rectangle are present in one color and the fourth corner is empty, fill the missing corner with that color.

**Program:** `solve_easy_p07`

**Primitives:** `rectangle_corner_vote`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 8
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 8 0 8
0 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 8 0 8
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 9
0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p01 — Area Rank Recolor (medium)

**Tags:** objects, ranking, recolor

**Written rule:** Find the three connected objects, order them by area from smallest to largest, and recolor them to 2, 3, and 4 respectively.

**Program:** `solve_medium_p01`

**Primitives:** `area_rank_recolor`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 5 0 0 0 0
0 7 0 0 0 0 5 5 5 0 0 0
0 7 7 0 0 0 0 5 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 0 0 0
0 2 0 0 0 0 3 3 3 0 0 0
0 2 2 0 0 0 0 3 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 4 0 0 0 0 0 0 6 6 6 0 0
0 4 4 0 0 0 0 0 0 6 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 4 0 0 0 0 0 0 3 3 3 0 0
0 4 4 0 0 0 0 0 0 3 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
9 9 9 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 2 0 0 7 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
2 2 2 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0
0 0 0 4 0 0 3 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
7 0 0 0 0 4 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
4 0 0 0 0 3 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p02 — Bounding-Box Fill (medium)

**Tags:** objects, bounding_box, same_size

**Written rule:** Replace each connected object by the solid filled rectangle of its bounding box, using the object’s own color.

**Program:** `solve_medium_p02`

**Primitives:** `bbox_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 7 7 0 0
0 3 3 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 7 7 7 0 0
0 3 3 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0
0 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 4 4 4 0 0
0 8 8 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 9 0 0
0 0 0 0 0 0 0 0 9 9 9 0 0
5 5 5 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 9 9 9 0 0
5 5 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 7 7 7 0 0 0 0 0 0 8
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 7 7 7 0 0 0 0 0 0 8
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## medium_p03 — Corner-Key Crop (medium)

**Tags:** selection, crop, color_key

**Written rule:** A colored key cell appears in one corner; crop out the unique object of that same color and output its tight bounding box.

**Program:** `solve_medium_p03`

**Primitives:** `corner_color_select`

### Train pairs

#### Train 1 input
```text
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 7 0 0 0
0 4 4 0 0 0 0 7 7 7 0 0
0 0 0 0 2 0 0 0 7 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 0
4 0
4 4
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
0 3 3 3 0 0 0 0 0 7 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7
```

#### Train 2 output
```text
0 7 0
7 7 7
0 7 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 2
0 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 8 8 0 2 2 2 0 0 0
0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 2
0 2 2
2 2 2
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 6 0 6 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
6 0 6
6 6 6
```

## medium_p04 — Frame Interior Gallery (medium)

**Tags:** frames, extraction, gallery

**Written rule:** Extract the interiors of all hollow rectangular frames, sort them by frame color from smallest to largest, and place those interiors left-to-right with one blank separator column.

**Program:** `solve_medium_p04`

**Primitives:** `frame_gallery`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 3 3 3 3 3 9 9 9 9
0 7 0 2 0 7 0 3 4 0 4 3 9 5 5 0
0 7 2 2 2 7 0 3 0 4 0 3 9 0 5 0
0 7 0 2 0 7 0 3 4 0 4 3 9 0 5 5
0 7 7 7 7 7 0 3 3 3 3 3 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 0 4 0 0 2 0
0 4 0 0 2 2 2
4 0 4 0 0 2 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 8 8 8 8 8 2 2 2 2 2
0 4 1 1 0 4 0 8 0 6 0 8 2 3 0 3 2
0 4 0 1 0 4 0 8 6 6 6 8 2 0 3 0 2
0 4 0 1 1 4 0 8 0 6 0 8 2 3 0 3 2
0 4 4 4 4 4 0 8 8 8 8 8 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
3 0 3 0 1 1 0 0 0 6 0
0 3 0 0 0 1 0 0 6 6 6
3 0 3 0 0 1 1 0 0 6 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 9 9 9 9 9 3 3 3 3
0 0 5 7 0 0 5 9 0 8 8 9 3 4 4 4
0 0 5 7 7 0 5 9 8 8 0 9 3 0 4 0
0 0 5 7 7 7 5 9 0 0 0 9 3 0 4 0
0 0 5 5 5 5 5 9 9 9 9 9 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
7 0 0 0 0 8 8
7 7 0 0 8 8 0
7 7 7 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 1 1 1 1 1 8 8 8 8 8
0 6 2 2 2 6 0 1 0 5 0 1 8 9 0 9 8
0 6 2 0 2 6 0 1 5 5 5 1 8 0 9 0 8
0 6 2 2 2 6 0 1 0 5 0 1 8 9 0 9 8
0 6 6 6 6 6 0 1 1 1 1 1 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 5 0 0 0 0 2 2 2 0 9 0 9
5 5 5 0 0 0 2 0 2 0 0 9 0
0 5 0 0 0 0 2 2 2 0 9 0 9
```

## medium_p05 — Marker-Count Rotation (medium)

**Tags:** rotation, markers, crop

**Written rule:** Ignore the top-row marker cells. Crop the remaining object tightly, then rotate it clockwise by 90° times the number of markers modulo 4.

**Program:** `solve_medium_p05`

**Primitives:** `marker_count_rotate`

### Train pairs

#### Train 1 input
```text
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 4 4
4 0 0
```

#### Train 2 input
```text
9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 7 0
7 7 7
```

#### Train 3 input
```text
9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 2
0 2 2
2 2 2
```

### Test pair

#### Test input
```text
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
6 6
6 0
6 6
```

## medium_p06 — Object Column Histogram (medium)

**Tags:** summary, histogram, shape_measurement

**Written rule:** Take the main object, crop its bounding box, count how many object cells appear in each bbox column, and output a bottom-aligned histogram of those counts in the same color.

**Program:** `solve_medium_p06`

**Primitives:** `column_histogram`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
5 0 0
5 5 0
5 5 5
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 7 0
0 7 0
7 7 7
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
3 0 3
3 3 3
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
8 0 0
8 8 8
```

## medium_p07 — Fill Enclosed Holes (medium)

**Tags:** topology, enclosure, same_size

**Written rule:** Any zero region that does not touch the border and is surrounded by exactly one color is filled with that surrounding color.

**Program:** `solve_medium_p07`

**Primitives:** `hole_fill`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 3 0 0 0 3 0 8 8 8 8 0
0 3 0 0 0 3 0 8 0 0 8 0
0 3 0 0 0 3 0 8 0 0 8 0
0 3 3 3 3 3 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 3 3 3 3 3 0 8 8 8 8 0
0 3 3 3 3 3 0 8 8 8 8 0
0 3 3 3 3 3 0 8 8 8 8 0
0 3 3 3 3 3 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 0 0 0
0 0 4 0 0 0 0 4 0 7 7 7 7
0 0 4 0 0 0 0 4 0 7 0 0 7
0 0 4 0 0 0 0 4 0 7 0 0 7
0 0 4 4 4 4 4 4 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0 0
0 0 4 4 4 4 4 4 0 7 7 7 7
0 0 4 4 4 4 4 4 0 7 7 7 7
0 0 4 4 4 4 4 4 0 7 7 7 7
0 0 4 4 4 4 4 4 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
6 6 6 6 6 0 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0 0
6 6 6 6 6 0 2 2 2 2 2
0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 2 2 2 2 2
```

#### Train 3 output
```text
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 2 2 2 2 2
0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 2 2 2 2 2
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9
0 5 5 5 5 5 5 0 9 0 0 9
0 5 0 0 0 0 5 0 9 0 0 9
0 5 0 0 0 0 5 0 9 0 0 9
0 5 0 0 0 0 5 0 9 0 0 9
0 5 5 5 5 5 5 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9
0 5 5 5 5 5 5 0 9 9 9 9
0 5 5 5 5 5 5 0 9 9 9 9
0 5 5 5 5 5 5 0 9 9 9 9
0 5 5 5 5 5 5 0 9 9 9 9
0 5 5 5 5 5 5 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p01 — Dual-Key Object Transform (hard)

**Tags:** selection, transformation, compositional

**Written rule:** The color of the top-left key selects which object to use, and the number of top-row marker cells selects the transform: 1=rotate90, 2=rotate180, 3=mirror horizontally, 4=transpose. Output the transformed tight crop of the selected object.

**Program:** `solve_hard_p01`

**Primitives:** `dual_key_select_transform`

### Train pairs

#### Train 1 input
```text
7 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 7 0 0 0 0
0 4 4 0 5 0 0 0 7 7 7 0 0 0
0 0 0 0 5 5 0 0 0 7 0 0 0 0
0 0 0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 7 0
7 7 7
0 7 0
```

#### Train 2 input
```text
5 9 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 5 0
5 5 5
```

#### Train 3 input
```text
3 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 3 0 0 0 0 0 6 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
3 0 0
3 3 0
3 3 3
```

### Test pair

#### Test input
```text
8 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 8
8 8
8 0
```

## hard_p02 — Portal Maze Path (hard)

**Tags:** pathfinding, portals, maze

**Written rule:** Find the shortest path from start(2) to goal(3), treating equal-colored portal cells as teleport pairs. Preserve the maze and mark the traversed empty cells with 7.

**Program:** `solve_hard_p02`

**Primitives:** `portal_bfs`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 4 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 3 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 8 0 0 0 0 0 0
0 2 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 5 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 3 0
0 0 0 0 0 8 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 8 0 0 0 0 0 0
0 2 0 0 0 8 0 0 0 0 0 0
0 7 0 0 0 8 0 0 0 5 0 0
0 7 0 0 0 8 0 0 0 7 0 0
0 7 0 0 0 8 0 0 0 7 0 0
0 7 0 0 0 8 0 0 0 7 0 0
0 7 0 0 0 8 0 0 0 7 0 0
0 7 7 7 7 5 0 0 0 7 3 0
0 0 0 0 0 8 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 4 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 7 7 7 7 7 7 7 0 0 0 0 0
0 2 0 0 0 0 8 7 0 0 0 0 0
0 0 0 0 0 0 8 7 7 7 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 4 0 0 0 8 0 0 0 0 0 0
0 0 7 0 0 0 8 0 0 0 0 0 0
0 0 7 0 0 0 8 7 7 7 7 3 0
0 0 7 7 7 7 7 7 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 6 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 7 7 7 7 3 0
0 0 0 0 0 0 0 0 0 0 0
```

## hard_p03 — Frames by Area (hard)

**Tags:** matching, frames, relayout

**Written rule:** Sort the hollow frames by interior area and sort the loose objects by object area. Center the smallest object in the smallest frame, the next in the next frame, and so on; remove the loose source objects.

**Program:** `solve_hard_p03`

**Primitives:** `frame_pack_by_area`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 8 8 8 8 8 0 9 9 9 9 9 9 0
0 7 0 7 0 8 0 0 0 8 0 9 0 0 0 0 9 0
0 7 7 7 0 8 0 0 0 8 0 9 0 0 0 0 9 0
0 0 0 0 0 8 0 0 0 8 0 9 0 0 0 0 9 0
0 0 0 0 0 8 8 8 8 8 0 9 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0 4 4 4 0 0
0 2 0 0 0 0 3 3 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 8 8 8 8 8 0 9 9 9 9 9 9 0
0 7 2 7 0 8 3 3 0 8 0 9 0 4 0 0 9 0
0 7 7 7 0 8 3 3 0 8 0 9 4 4 4 0 9 0
0 0 0 0 0 8 0 0 0 8 0 9 0 4 0 0 9 0
0 0 0 0 0 8 8 8 8 8 0 9 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 7 7 7 7 7 7 0 8 8 8 8 0
0 6 0 0 6 0 0 7 0 0 0 0 7 0 8 0 0 8 0
0 6 0 0 6 0 0 7 0 0 0 0 7 0 8 0 0 8 0
0 6 6 6 6 0 0 7 0 0 0 0 7 0 8 0 0 8 0
0 0 0 0 0 0 0 7 7 7 7 7 7 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 4 0 0 0
0 2 0 0 0 0 0 3 0 0 0 0 0 0 4 4 4 0 0
0 2 0 0 0 0 0 3 3 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 7 7 7 7 7 7 0 8 8 8 8 0
0 6 2 0 6 0 0 7 0 4 0 0 7 0 8 3 0 8 0
0 6 2 0 6 0 0 7 4 4 4 0 7 0 8 3 0 8 0
0 6 6 6 6 0 0 7 0 4 0 0 7 0 8 3 3 8 0
0 0 0 0 0 0 0 7 7 7 7 7 7 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 6 6 6 6 6 0 7 7 7 7 7 7 7 0
0 5 0 0 5 0 6 0 0 0 6 0 7 0 0 0 0 0 7 0
0 5 5 5 5 0 6 0 0 0 6 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 6 0 0 0 6 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 6 0 0 0 6 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 4 4 0 0 0 0
0 2 2 0 0 0 0 3 3 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 6 6 6 6 6 0 7 7 7 7 7 7 7 0
0 5 2 2 5 0 6 3 0 0 6 0 7 0 4 0 0 0 7 0
0 5 5 5 5 0 6 3 0 0 6 0 7 0 4 4 0 0 7 0
0 0 0 0 0 0 6 3 3 0 6 0 7 0 4 4 4 0 7 0
0 0 0 0 0 0 6 0 0 0 6 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 5 5 5 5 5 0 6 6 6 6 6 6 6 0 0
0 4 0 4 0 5 0 0 0 5 0 6 0 0 0 0 0 6 0 0
0 4 4 4 0 5 0 0 0 5 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 5 5 5 5 5 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 7 7 0 0 0 0 0
0 0 2 0 0 0 3 3 0 0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 5 5 3 5 5 0 6 6 6 6 6 6 6 0 0
0 4 2 4 0 5 3 3 0 5 0 6 0 7 0 0 0 6 0 0
0 4 4 4 0 5 0 3 0 5 0 6 0 7 7 0 0 6 0 0
0 0 0 0 0 5 5 5 5 5 0 6 0 7 7 7 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## hard_p04 — Keyed Shape Boolean (hard)

**Tags:** boolean, alignment, shape_algebra

**Written rule:** The key at the top-left chooses a Boolean operation on the two cropped shapes after top-left alignment: 1=union, 2=intersection, 3=xor, 4=A minus B. Output the result in color 4.

**Program:** `solve_hard_p04`

**Primitives:** `shape_boolean`

### Train pairs

#### Train 1 input
```text
1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 3 3 0 0
0 2 0 0 0 0 0 0 0 3 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 4 4
4 4 0
4 4 0
```

#### Train 2 input
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 3 3 3 0 0
0 2 2 2 0 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 4 0
0 4 0
0 0 0
```

#### Train 3 input
```text
3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 3 3 3 0 0
0 2 2 2 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 4 0 0
```

### Test pair

#### Test input
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 0 0 3 0 0 0
0 2 2 2 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0
4 0 0
4 4 0
```

## hard_p05 — Transform Timeline Gallery (hard)

**Tags:** scripts, sequential, gallery

**Written rule:** The top row gives a transform script over the cropped object below: 1=rotate90, 2=rotate180, 3=mirror horizontally, 4=transpose. Apply the script step by step and output every intermediate state as a left-to-right gallery.

**Program:** `solve_hard_p05`

**Primitives:** `transform_timeline`

### Train pairs

#### Train 1 input
```text
1 3 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
4 4 4 0 4 4 4 0 0 4
4 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 4 4
```

#### Train 2 input
```text
4 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
7 0 0 7 7 7
7 7 0 0 7 0
7 0 0 0 0 0
```

#### Train 3 input
```text
2 4 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 5 0 0 0 0
0 0 0 0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
5 5 5 0 5 5 0 5 5
5 0 5 0 5 0 0 0 5
0 0 0 0 5 5 0 5 5
```

### Test pair

#### Test input
```text
1 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
8 8 8 0 8 8 8 0 8 0 0
8 8 0 0 0 8 8 0 8 8 0
8 0 0 0 0 0 8 0 8 8 8
```

## hard_p06 — Contact-Degree Recolor (hard)

**Tags:** graphs, objects, recolor

**Written rule:** Treat each monochrome object as a node and connect nodes when their cells touch orthogonally. Recolor each object by its graph degree: degree 0→1, degree 1→2, degree 2→3, degree 3 or more→4.

**Program:** `solve_hard_p06`

**Primitives:** `contact_degree`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 9 9 0 0 0 0
0 0 3 3 9 9 4 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 2 2 4 4 2 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 7 0
0 0 2 2 3 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 1 0
0 0 2 2 3 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 2 2 3 3 0 6 0 0 0
0 0 0 2 2 3 3 0 6 7 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 4 4 2 2 0 2 0 0 0
0 0 0 4 4 2 2 0 2 2 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 2 2 2 5 0 0 0 0 0
0 0 0 4 0 5 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 4 4 4 3 0 0 0 0 0
0 0 0 2 0 3 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
```

## hard_p07 — Mirror Beam Trace (hard)

**Tags:** raytracing, mirrors, simulation

**Written rule:** A beam starts at the border emitter(2) and travels inward. Slash mirrors(4) and backslash mirrors(5) reflect it; walls(8) stop it. Preserve the symbols and mark traversed empty cells with 7.

**Program:** `solve_hard_p07`

**Primitives:** `mirror_raytrace`

### Train pairs

#### Train 1 input
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 1 output
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 7 7 7 5 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 5 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
```

#### Train 2 input
```text
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 2 output
```text
0 0 2 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
7 7 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

#### Train 3 input
```text
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

#### Train 3 output
```text
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 4 0 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 5 0 0 7
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7
```

### Test pair

#### Test input
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
```

#### Test output
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
2 7 7 7 7 7 7 7 7
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
```
