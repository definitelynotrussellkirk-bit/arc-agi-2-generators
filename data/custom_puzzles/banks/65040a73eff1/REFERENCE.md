# ARC Puzzle Bank — Seventh 21 Puzzles
This seventh bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`43`–`49`) so it follows directly after the sixth bundle.
This volume leans into explicit axis reasoning, crop/extract transforms, local frame logic, hole-count selection, and template/code expansion. It deliberately widens the mechanics again rather than just repeating the most recent families.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_seventh_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_seventh_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_seventh_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_43_bridge_row_pairs` — **Bridge Each Pair of Row Markers**
- `easy_44_mirror_across_cyan_axis` — **Mirror the Objects across the Cyan Axis**
- `easy_45_draw_border_from_corners` — **Draw the Rectangle Border from its Four Corners**
- `easy_46_crop_frame_contents` — **Crop Out the Contents of the Frame**
- `easy_47_keep_most_frequent_color` — **Keep Only the Most Frequent Color**
- `easy_48_component_centers` — **Mark the Center of Each Component**
- `easy_49_palette_row_left_to_right` — **Read the Palette from Left to Right**

### Medium (7)
- `medium_43_marked_rowcol_crossings` — **Fill the Crossings of the Marked Rows and Columns**
- `medium_44_stamp_rotated_source_at_markers` — **Stamp Rotated Copies of the Source Shape at the Markers**
- `medium_45_crop_union_of_key_colors` — **Crop the Union of the Key Colors**
- `medium_46_scale_smallest_component_x2` — **Find the Smallest Component and Scale it by 2**
- `medium_47_pack_nonempty_columns_left` — **Pack the Nonempty Columns to the Left**
- `medium_48_crop_fullest_frame_interior` — **Crop the Interior of the Fullest Frame**
- `medium_49_draw_rectangles_from_opposite_corners` — **Draw a Rectangle for Each Opposite-Corner Pair**

### Hard (7)
- `hard_43_local_marked_rowcol_crossings_in_frames` — **Solve the Marked Crossings Separately inside Each Frame**
- `hard_44_template_tiling_from_code_grid` — **Tile the Template Library according to the Code Grid**
- `hard_45_overlay_selected_components_with_rotation` — **Overlay Two Keyed Components after Rotating the Second**
- `hard_46_local_symmetry_completion_by_frame_key` — **Complete the Symmetry inside Each Frame**
- `hard_47_tile_component_with_most_holes` — **Choose the Most Holed Component and Tile it 2×2**
- `hard_48_local_rotate_object_to_key_center` — **Rotate Each Framed Object and Recenter it**
- `hard_49_rotation_code_mosaic` — **Expand a Rotation Code Grid into a Full Mosaic**

## Bridge Each Pair of Row Markers (`easy_43_bridge_row_pairs`)

**Difficulty:** easy

**Skills:** row scan, segment filling, per-color reasoning

**Scaffold notes:**
- Work row by row rather than globally.
- Treat two equal-colored cells in a row as endpoints.
- Fill the whole horizontal span between those endpoints.

**Written solution:** Scan each row independently. Whenever a nonzero color appears as a left-right pair in that row, treat those two cells as the endpoints of a segment and fill every cell between them, inclusive, with that same color. Rows without a pair stay unchanged.

**Program solution (Python reference):**
```python
def solve_easy_43_bridge_row_pairs(g: Grid) -> Grid:
    out = clone(g)
    for r,row in enumerate(g):
        pos = defaultdict(list)
        for c,v in enumerate(row):
            if v != 0:
                pos[v].append(c)
        for color, cols in pos.items():
            if len(cols) >= 2:
                a,b = min(cols), max(cols)
                for c in range(a, b+1):
                    out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 5
0 2 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5
0 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## Mirror the Objects across the Cyan Axis (`easy_44_mirror_across_cyan_axis`)

**Difficulty:** easy

**Skills:** axis detection, reflection, same-size transform

**Scaffold notes:**
- First find the full-height cyan(8) line.
- Every non-axis colored cell has a reflected partner across that line.
- Keep the originals and add their mirror images.

**Written solution:** Identify the unique cyan(8) column that runs from the top of the grid to the bottom. That column is the mirror axis. Copy every nonzero, non-axis cell to the column at the same distance on the opposite side of the axis, keeping the same color and preserving the original cells.

**Program solution (Python reference):**
```python
def solve_easy_44_mirror_across_cyan_axis(g: Grid) -> Grid:
    h,w = dims(g)
    axis = None
    for c in range(w):
        if all(g[r][c] == 8 for r in range(h)):
            axis = c
            break
    assert axis is not None
    out = clone(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0 and c != axis:
                mc = 2*axis - c
                if 0 <= mc < w:
                    out[r][mc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 8 0 0 0 0
0 3 0 0 8 0 0 0 0
0 3 3 0 8 0 0 0 0
0 0 3 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
5 5 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 8 0 0 0 0
0 3 0 0 8 0 0 3 0
0 3 3 0 8 0 3 3 0
0 0 3 0 8 0 3 0 0
0 0 0 0 8 0 0 0 0
5 5 0 0 8 0 0 5 5
0 0 0 0 8 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 8 0 0 2 0
0 0 0 0 0 0 8 0 2 2 0
0 0 0 0 0 0 8 0 0 2 0
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 8 0 4 0 0
0 0 0 0 0 0 8 0 4 0 0
0 0 0 0 0 0 8 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 8 0 0 0 0
0 0 0 2 0 0 8 0 0 2 0
0 0 0 2 2 0 8 0 2 2 0
0 0 0 2 0 0 8 0 0 2 0
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 4 0 8 0 4 0 0
0 0 0 0 4 0 8 0 4 0 0
0 0 0 0 0 0 8 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 8 0 0 0 0
0 0 6 0 8 0 0 0 0
0 0 6 0 8 0 0 0 0
0 6 6 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 3 3 0 8 0 0 0 0
0 3 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 8 0 0 0 0
0 0 6 0 8 0 6 0 0
0 0 6 0 8 0 6 0 0
0 6 6 0 8 0 6 6 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 3 3 0 8 0 3 3 0
0 3 0 0 8 0 0 3 0
0 0 0 0 8 0 0 0 0
```

**Train 4 input**
```text
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 2 0 0
0 0 0 8 0 0 0 2 2 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 7 7 0 0
0 0 0 8 0 0 0 7 0 0
```

**Train 4 output**
```text
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 2 0 0
0 0 0 8 0 0 0 2 2 0
0 0 0 8 0 0 0 0 0 0
7 0 0 8 0 0 7 7 0 0
0 0 0 8 0 0 0 7 0 0
```

**Test 1 input**
```text
0 0 0 0 8 0 0 0 0
0 4 0 0 8 0 0 0 0
0 4 4 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 6 0 0
0 0 0 0 8 6 6 0 0
0 0 0 0 8 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 8 0 0 0 0
0 4 0 0 8 0 0 4 0
0 4 4 0 8 0 4 4 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 6 0 8 0 6 0 0
0 0 6 6 8 6 6 0 0
0 0 0 0 8 0 0 0 0
```


## Draw the Rectangle Border from its Four Corners (`easy_45_draw_border_from_corners`)

**Difficulty:** easy

**Skills:** bounding box, rectangle construction, border drawing

**Scaffold notes:**
- The four given cells are the rectangle corners.
- Use their min/max row and column to recover the box.
- Draw only the perimeter, not the filled interior.

**Written solution:** The four nonzero cells are the corners of one axis-aligned rectangle. Take the minimum and maximum row and column among them, then draw the full border of that rectangle in the same color. The interior remains empty.

**Program solution (Python reference):**
```python
def solve_easy_45_draw_border_from_corners(g: Grid) -> Grid:
    cells = nonzero_cells(g)
    r0,c0,r1,c1 = bbox(cells)
    color = g[cells[0][0]][cells[0][1]]
    out = zeros(len(g), len(g[0]), 0)
    for c in range(c0, c1+1):
        out[r0][c] = color
        out[r1][c] = color
    for r in range(r0, r1+1):
        out[r][c0] = color
        out[r][c1] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0
0 0 4 0 0 0 0 4 0
0 0 4 0 0 0 0 4 0
0 0 4 0 0 0 0 4 0
0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 6 0 0 0 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 6 0 0 0 6 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 6 6 6 6 0 0
0 6 0 0 0 6 0 0
0 6 0 0 0 6 0 0
0 6 0 0 0 6 0 0
0 6 0 0 0 6 0 0
0 6 0 0 0 6 0 0
0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2
0 0 0 2 0 0 0 0 0 2
0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 0 0
7 0 0 0 0 0 0 0 7 0 0
7 0 0 0 0 0 0 0 7 0 0
7 0 0 0 0 0 0 0 7 0 0
7 0 0 0 0 0 0 0 7 0 0
7 0 0 0 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5
0 0 5 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5
```


## Crop Out the Contents of the Frame (`easy_46_crop_frame_contents`)

**Difficulty:** easy

**Skills:** frame detection, interior extraction, size change

**Scaffold notes:**
- Find the single rectangular frame.
- Ignore the border itself.
- Return only the interior window as the new output.

**Written solution:** Locate the unique rectangular frame made of color 8. Remove the outer border conceptually and keep only the cells inside it. The output is exactly that interior crop, with all its colors and zeros preserved.

**Program solution (Python reference):**
```python
def solve_easy_46_crop_frame_contents(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 8)
    assert len(boxes) == 1
    ir0,ic0,ir1,ic1 = inside(boxes[0])
    return [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0
0 0 8 2 0 0 3 8 0
0 0 8 2 2 0 0 8 0
0 0 8 0 0 4 4 8 0
0 0 8 0 5 0 0 8 0
0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 3
2 2 0 0
0 0 4 4
0 5 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0
0 8 0 6 0 0 8 0 0 0
0 8 6 6 0 2 8 0 0 0
0 8 0 0 0 2 8 0 0 0
0 8 3 0 3 0 8 0 0 0
0 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0
6 6 0 2
0 0 0 2
3 0 3 0
```

**Train 3 input**
```text
0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 8 1 0 1 0 8 0
0 0 0 0 8 0 2 0 2 8 0
0 0 0 0 8 3 0 0 0 8 0
0 0 0 0 8 0 4 4 0 8 0
0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 0 1 0
0 2 0 2
3 0 0 0
0 4 4 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0
0 0 8 0 7 0 0 1 8 0
0 0 8 7 0 0 1 0 8 0
0 0 8 0 0 2 0 0 8 0
0 0 8 3 0 0 0 3 8 0
0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 7 0 0 1
7 0 0 1 0
0 0 2 0 0
3 0 0 0 3
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 8 2 0 0 2 8 0
0 0 0 0 0 8 0 3 3 0 8 0
0 0 0 0 0 8 4 0 0 4 8 0
0 0 0 0 0 8 0 5 0 0 8 0
0 0 0 0 0 8 6 0 6 0 8 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 0 0 2
0 3 3 0
4 0 0 4
0 5 0 0
6 0 6 0
```


## Keep Only the Most Frequent Color (`easy_47_keep_most_frequent_color`)

**Difficulty:** easy

**Skills:** color counting, filtering, same-size transform

**Scaffold notes:**
- Count how many times each nonzero color appears.
- Choose the color with the largest count.
- Erase every other color.

**Written solution:** Count the total number of cells for each nonzero color in the whole input. Find the color with the largest frequency. In the output, keep only cells of that winning color and set every other cell to background.

**Program solution (Python reference):**
```python
def solve_easy_47_keep_most_frequent_color(g: Grid) -> Grid:
    counts = defaultdict(int)
    for row in g:
        for v in row:
            if v != 0:
                counts[v] += 1
    keep = max(counts, key=lambda k: (counts[k], -k))
    out = zeros(len(g), len(g[0]), 0)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v == keep:
                out[r][c] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 2 0 0 4 0 0
0 0 0 0 0 0 4 4 0
0 3 3 3 3 3 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 5 5 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 2 2 0 0 7 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 3 0 0 0 0 4 4 4 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 5 0 0
0 0 8 0 0 0 0 5 5 0
0 0 0 0 2 2 2 0 5 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 7 0 0
0 2 0 0 0 0 0 0 7 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## Mark the Center of Each Component (`easy_48_component_centers`)

**Difficulty:** easy

**Skills:** connected components, bounding boxes, center extraction

**Scaffold notes:**
- Treat each colored blob as its own component.
- Compute the component's bounding box.
- Replace the whole blob by one cell at the box center.

**Written solution:** Split the nonzero cells into connected components. For each component, compute its bounding box and take the center cell of that box. The output keeps only one cell per component, in the original component color, placed at that center position.

**Program solution (Python reference):**
```python
def solve_easy_48_component_centers(g: Grid) -> Grid:
    out = zeros(len(g), len(g[0]), 0)
    for comp in connected_components(g):
        rr,cc = center_of_box(comp["bbox"])
        out[rr][cc] = comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 3 3 3 3 3
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 7 7 7 2 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 3 3 3 0 0
0 0 6 0 0 0 0 3 3 3 0 0
0 0 6 0 0 0 0 3 3 3 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 8 0 0 0 2 2 2 0
0 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 6 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
7 7 7 7 7 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## Read the Palette from Left to Right (`easy_49_palette_row_left_to_right`)

**Difficulty:** easy

**Skills:** ordering by position, component summaries, size change

**Scaffold notes:**
- Each component contributes one color to the answer.
- Order the components by their leftmost column.
- Write those colors into a single output row.

**Written solution:** Find all connected components and sort them by their leftmost column, breaking ties by topmost row if needed. Then output a one-row palette whose entries are the component colors in that spatial order. Each component contributes exactly one color cell to the row.

**Program solution (Python reference):**
```python
def solve_easy_49_palette_row_left_to_right(g: Grid) -> Grid:
    items = []
    for comp in connected_components(g):
        r0,c0,r1,c1 = comp["bbox"]
        items.append((c0, r0, comp["color"]))
    items.sort()
    return [[color for _,_,color in items]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 5 5 5 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 5 3
```

**Train 2 input**
```text
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 4 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 4 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
3 3 3 3 3 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 4 0 0 0
0 0 6 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 2 4 7
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 2 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 2 8
```


## Fill the Crossings of the Marked Rows and Columns (`medium_43_marked_rowcol_crossings`)

**Difficulty:** medium

**Skills:** edge markers, row/column selection, cross-product fill

**Scaffold notes:**
- Rows are selected by red(2) markers on both side edges.
- Columns are selected by blue(3) markers on both top and bottom edges.
- Fill every selected row/column intersection with cyan(8).

**Written solution:** Read the side markers first: a row is active when it has red(2) cells at both the left and right border, and a column is active when it has blue(3) cells at both the top and bottom border. Once those sets are known, fill the cartesian product of active rows and active columns with cyan(8). Keep the markers themselves.

**Program solution (Python reference):**
```python
def solve_medium_43_marked_rowcol_crossings(g: Grid) -> Grid:
    h,w = dims(g)
    rows = [r for r in range(1, h-1) if g[r][0] == 2 and g[r][w-1] == 2]
    cols = [c for c in range(1, w-1) if g[0][c] == 3 and g[h-1][c] == 3]
    out = clone(g)
    for r in rows:
        for c in cols:
            out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 3 0 0 3 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0
```

**Train 1 output**
```text
0 0 0 3 0 0 3 0 0
0 0 0 0 0 0 0 0 0
2 0 0 8 0 0 8 0 2
0 0 0 0 0 0 0 0 0
2 0 0 8 0 0 8 0 2
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 3 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 3 0 0
2 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 2
0 0 3 0 0 0 0 3 0 0
```

**Train 2 output**
```text
0 0 3 0 0 0 0 3 0 0
2 0 8 0 0 0 0 8 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 8 0 0 0 0 8 0 2
2 0 8 0 0 0 0 8 0 2
0 0 3 0 0 0 0 3 0 0
```

**Train 3 input**
```text
0 3 0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 2
0 3 0 0 3 0 0 0 3 0 0
```

**Train 3 output**
```text
0 3 0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
2 8 0 0 8 0 0 0 8 0 2
2 8 0 0 8 0 0 0 8 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 8 0 0 8 0 0 0 8 0 2
0 3 0 0 3 0 0 0 3 0 0
```

**Train 4 input**
```text
0 0 3 0 0 3 0 0 0 3 0 0
2 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 2
0 0 3 0 0 3 0 0 0 3 0 0
```

**Train 4 output**
```text
0 0 3 0 0 3 0 0 0 3 0 0
2 0 8 0 0 8 0 0 0 8 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 8 0 0 8 0 0 0 8 0 2
0 0 3 0 0 3 0 0 0 3 0 0
```

**Test 1 input**
```text
0 0 0 3 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 2
2 0 0 0 0 0 0 0 0 0 0 2
0 0 0 3 0 0 0 3 0 0 3 0
```

**Test 1 output**
```text
0 0 0 3 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 8 0 0 0 8 0 0 8 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 8 0 0 0 8 0 0 8 2
2 0 0 8 0 0 0 8 0 0 8 2
0 0 0 3 0 0 0 3 0 0 3 0
```


## Stamp Rotated Copies of the Source Shape at the Markers (`medium_44_stamp_rotated_source_at_markers`)

**Difficulty:** medium

**Skills:** source extraction, rotation, marker-driven stamping

**Scaffold notes:**
- The one multi-cell non-marker object is the source template.
- Marker colors 1/2/3/4 encode 0°/90°/180°/270° clockwise rotation.
- At each marker, paste the corresponding rotated template and recolor it to the marker color.

**Written solution:** Find the unique multi-cell source object and crop it to its bounding box. Each singleton marker then requests a copy of that template: color 1 means no rotation, 2 means rotate 90° clockwise, 3 means 180°, and 4 means 270°. Paste the requested rotated template with its top-left aligned to the marker position, recoloring the copied cells to the marker color, and discard the original source.

**Program solution (Python reference):**
```python
def solve_medium_44_stamp_rotated_source_at_markers(g: Grid) -> Grid:
    comps = connected_components(g)
    source = max([comp for comp in comps if comp["color"] not in {1,2,3,4}], key=lambda comp: len(comp["cells"]))
    pat = crop_bbox(g, source["bbox"])
    # binarize the source crop
    pat = [[1 if v == source["color"] else 0 for v in row] for row in pat]
    out = zeros(len(g), len(g[0]), 0)
    rot_map = {1:0, 2:1, 3:2, 4:3}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in rot_map:
                rg = pat
                for _ in range(rot_map[v]):
                    rg = rotate_grid_cw(rg)
                for rr in range(len(rg)):
                    for cc in range(len(rg[0])):
                        if rg[rr][cc]:
                            out[r+rr][c+cc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 1 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 4 0 0 0 0 0 3 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 1 1 1 4 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 3 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 2 2 0 0 1 1 0 0
0 0 0 2 2 0 0 0 0 1 4 4
0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 1 1 0 2 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0 1 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 3 3 3 2 2 0
0 0 0 4 4 4 0 0 3 0 3 0 0 0
0 0 0 0 0 4 0 0 3 0 3 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Crop the Union of the Key Colors (`medium_45_crop_union_of_key_colors`)

**Difficulty:** medium

**Skills:** key reading, color filtering, cropped output

**Scaffold notes:**
- The first row is a key strip that tells you which colors matter.
- Below that row, ignore every color not named in the key.
- Crop tightly around all remaining keyed cells.

**Written solution:** Read the nonzero colors in the first row; that set is the key. In the rest of the grid, keep only cells whose color belongs to that key set. Then take the tight bounding box around all kept cells and return that crop as the output.

**Program solution (Python reference):**
```python
def solve_medium_45_crop_union_of_key_colors(g: Grid) -> Grid:
    key_colors = {v for v in g[0] if v != 0}
    cells = [(r,c) for r in range(1, len(g)) for c,v in enumerate(g[r]) if v in key_colors]
    r0,c0,r1,c1 = bbox(cells)
    out = zeros(r1-r0+1, c1-c0+1, 0)
    for r in range(r0, r1+1):
        for c in range(c0, c1+1):
            if g[r][c] in key_colors:
                out[r-r0][c-c0] = g[r][c]
    return out
```

**Train 1 input**
```text
0 2 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 7 7 7 5 0 0 0
0 0 0 0 0 0 7 0 5 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 5
```

**Train 2 input**
```text
0 3 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 4 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6
```

**Train 3 input**
```text
0 4 0 7 0 2 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0
0 0 7 0 5 0 0 0 0 0 0
0 0 0 0 5 5 5 2 2 2 0
4 0 0 0 0 0 0 0 2 0 0
4 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 7 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
4 0 0 0 0 0 0 0 2 0
4 0 0 0 0 0 0 0 2 0
```

**Train 4 input**
```text
0 8 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 3 0 0 0
0 6 0 0 0 0 0 0 3 3 3 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 8 0 0 0 0 0 0
8 8 8 0 0 0 0 0
0 8 0 0 0 3 0 0
0 0 0 0 0 3 3 3
```

**Test 1 input**
```text
0 5 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 5 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 2 0
```


## Find the Smallest Component and Scale it by 2 (`medium_46_scale_smallest_component_x2`)

**Difficulty:** medium

**Skills:** component comparison, cropping, uniform scaling

**Scaffold notes:**
- Compare components by number of cells, not by bounding-box size.
- Take the unique smallest component.
- Crop it and expand each input cell into a 2×2 block.

**Written solution:** Separate the nonzero cells into connected components and count the number of cells in each one. Select the unique smallest component, crop its bounding box, and then scale that crop by a factor of two in both directions. Every input cell becomes a 2×2 block of the same value.

**Program solution (Python reference):**
```python
def solve_medium_46_scale_smallest_component_x2(g: Grid) -> Grid:
    comp = min(connected_components(g), key=lambda comp: (len(comp["cells"]), comp["bbox"]))
    crop = crop_bbox(g, comp["bbox"])
    return scale2(crop)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 5 0 0 0 0 7 7 7 0 0
0 5 5 5 0 0 7 7 7 0 0
0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
5 5 0 0 0 0
5 5 0 0 0 0
5 5 5 5 5 5
5 5 5 5 5 5
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 8 0 0 0
0 6 6 0 0 0 0 8 8 8 0 0
0 0 6 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 0 0
6 6 0 0
6 6 6 6
6 6 6 6
0 0 6 6
0 0 6 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 2 2 2 2 2
0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7
7 7
7 7
7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 2 0 0 0 0 0 0 0 6 0 0
0 0 2 2 2 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 0 0 0 0
2 2 0 0 0 0
2 2 2 2 2 2
2 2 2 2 2 2
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 0 0
0 3 0 0 0 0 0 0 5 0 0 0
0 3 3 0 0 0 0 0 5 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
3 3 0 0
3 3 0 0
3 3 3 3
3 3 3 3
0 0 3 3
0 0 3 3
```


## Pack the Nonempty Columns to the Left (`medium_47_pack_nonempty_columns_left`)

**Difficulty:** medium

**Skills:** column filtering, order preservation, size change

**Scaffold notes:**
- Look at columns, not rows.
- Discard every all-zero column.
- Keep the remaining columns in the same relative order and pack them together.

**Written solution:** Inspect each column and keep only those that contain at least one nonzero cell. Preserve their left-to-right order, but remove all gaps caused by empty columns. The result is a narrower grid with the same height.

**Program solution (Python reference):**
```python
def solve_medium_47_pack_nonempty_columns_left(g: Grid) -> Grid:
    h,w = dims(g)
    cols = [c for c in range(w) if any(g[r][c] != 0 for r in range(h))]
    return [[g[r][c] for c in cols] for r in range(h)]
```

**Train 1 input**
```text
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 3 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
```

**Train 1 output**
```text
2 0 0
2 0 3
2 0 0
0 5 3
0 5 0
0 0 3
```

**Train 2 input**
```text
0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
6 0 0 4 0 0 0 0 0 0 0
6 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 0
0 4 0
6 4 0
6 4 0
0 0 2
0 0 2
0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 3 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
```

**Train 3 output**
```text
0 0 3
7 0 0
7 0 0
7 0 0
0 5 0
0 5 0
0 5 0
0 0 3
```

**Train 4 input**
```text
0 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 6
0 0 0 0 2 0 0 0 6
0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0
8 0 6
0 2 6
0 2 0
0 2 0
0 0 0
```

**Test 1 input**
```text
0 0 0 0 3 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 3 0 7 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 3 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 3 0 0
5 0 0 0
5 0 7 0
0 3 7 0
0 0 7 0
0 0 0 2
0 3 0 0
```


## Crop the Interior of the Fullest Frame (`medium_48_crop_fullest_frame_interior`)

**Difficulty:** medium

**Skills:** multi-frame selection, interior counting, cropped output

**Scaffold notes:**
- There are several candidate frames.
- Count how many nonzero interior cells each frame contains.
- Return the inside of the most populated frame.

**Written solution:** Detect all rectangular color-1 frames. For each frame, count the number of nonzero cells inside its border. Choose the frame whose interior contains the most nonzero cells and output exactly that interior crop.

**Program solution (Python reference):**
```python
def solve_medium_48_crop_fullest_frame_interior(g: Grid) -> Grid:
    best_box = None
    best_count = -1
    for box in frame_boxes_from_color(g, 1):
        ir0,ic0,ir1,ic1 = inside(box)
        cnt = sum(1 for r in range(ir0, ir1+1) for c in range(ic0, ic1+1) if g[r][c] != 0)
        if cnt > best_count:
            best_count = cnt
            best_box = box
    ir0,ic0,ir1,ic1 = inside(best_box)
    return [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 1 1 1 1 1 0
0 1 2 0 2 1 0 0 0 0 1 3 3 0 1 0
0 1 0 2 0 1 0 0 0 0 1 0 3 0 1 0
0 1 2 0 2 1 0 0 0 0 1 3 0 3 1 0
0 1 1 1 1 1 0 0 0 0 1 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 1 4 0 4 0 1 0 0 0 0 0
0 0 0 0 0 1 4 4 4 0 1 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 2
0 2 0
2 0 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 0 0
0 1 2 2 0 0 1 0 0 0 1 3 0 3 1 0 0
0 1 0 2 0 0 1 0 0 0 1 3 3 3 1 0 0
0 1 0 0 0 0 1 0 0 0 1 0 3 0 1 0 0
0 1 0 0 0 0 1 0 0 0 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 1 4 4 4 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 4 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 4 0 4 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 0 3
3 3 3
0 3 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 0 0
0 0 1 5 0 5 0 1 0 0 0 1 2 2 2 1 0 0
0 0 1 0 5 0 0 1 0 0 0 1 2 0 2 1 0 0
0 0 1 0 0 0 0 1 0 0 0 1 0 2 0 1 0 0
0 0 1 1 1 1 1 1 0 0 0 1 2 0 2 1 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 7 0 7 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 7 7 7 1 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2
2 0 2
0 2 0
2 0 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 0
0 1 3 0 0 1 0 0 0 0 1 4 4 0 4 1 0
0 1 0 3 0 1 0 0 0 0 1 0 4 4 0 1 0
0 1 0 0 3 1 0 0 0 0 1 4 0 4 0 1 0
0 1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 2 2 2 1 0 0 0 0 0 0 0
0 0 0 0 0 1 2 2 2 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 0 4
0 4 4 0
4 0 4 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 1 1 1 1 1 0 0
0 0 1 2 0 2 1 0 0 0 0 1 3 3 3 1 0 0
0 0 1 0 2 0 1 0 0 0 0 1 0 3 0 1 0 0
0 0 1 2 0 2 1 0 0 0 0 1 3 0 3 1 0 0
0 0 1 1 1 1 1 0 0 0 0 1 0 3 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 4 4 4 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 4 0 4 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 4 4 4 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
4 4 4 0
4 0 4 0
4 4 4 0
```


## Draw a Rectangle for Each Opposite-Corner Pair (`medium_49_draw_rectangles_from_opposite_corners`)

**Difficulty:** medium

**Skills:** pair grouping, geometry, multiple objects

**Scaffold notes:**
- Each color appears exactly twice.
- Those two cells are opposite corners of one rectangle.
- Draw the border of every such rectangle in its own color.

**Written solution:** Group the nonzero cells by color. Every color occurs exactly twice, and those two cells define opposite corners of an axis-aligned rectangle. For each color, draw that rectangle's border in the same color and combine all the rectangles in the output.

**Program solution (Python reference):**
```python
def solve_medium_49_draw_rectangles_from_opposite_corners(g: Grid) -> Grid:
    h,w = dims(g)
    out = zeros(h, w, 0)
    pos = defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v != 0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells) == 2:
            (r0,c0),(r1,c1) = cells
            ra,rb = sorted((r0,r1))
            ca,cb = sorted((c0,c1))
            for c in range(ca, cb+1):
                out[ra][c] = color
                out[rb][c] = color
            for r in range(ra, rb+1):
                out[r][ca] = color
                out[r][cb] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 0 0 2 0 0 5 5 5 0
0 2 0 0 2 0 0 5 0 5 0
0 2 2 2 2 0 0 5 0 5 0
0 0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 4 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0
0 0 3 0 0 3 0 0 7 7 7 7
0 0 3 0 0 3 0 0 7 0 0 7
4 4 4 4 0 3 0 0 7 0 0 7
4 0 3 4 3 3 0 0 7 0 0 7
4 0 0 4 0 0 0 0 7 7 7 7
4 4 4 4 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 0 0 6 0 2 2 2 2
0 6 0 0 6 0 2 0 0 2
0 6 0 0 6 0 2 0 0 2
0 6 0 0 6 0 2 2 2 2
0 6 0 0 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 3 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0 0 0 0
0 0 0 8 0 0 0 0 8 0 5 5 5
0 0 0 8 0 0 0 0 8 0 5 0 5
0 0 0 8 0 0 0 0 8 0 5 0 5
0 0 0 8 8 8 8 8 8 0 5 0 5
3 3 3 0 0 0 0 0 0 0 5 0 5
3 0 3 0 0 0 0 0 0 0 5 5 5
3 3 3 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 2 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0
0 4 0 0 0 0 4 0 7 7 7 0
0 4 0 0 0 0 4 0 7 0 7 0
0 4 0 0 0 0 4 0 7 0 7 0
0 4 0 0 0 0 4 0 7 0 7 0
0 4 4 4 4 4 4 0 7 0 7 0
2 2 2 2 0 0 0 0 7 0 7 0
2 0 0 2 0 0 0 0 7 7 7 0
2 2 2 2 0 0 0 0 0 0 0 0
```


## Solve the Marked Crossings Separately inside Each Frame (`hard_43_local_marked_rowcol_crossings_in_frames`)

**Difficulty:** hard

**Skills:** frame-local reasoning, edge markers, per-frame key colors

**Scaffold notes:**
- Do the row/column selection independently in each frame.
- The fill color comes from the frame's key cell above it.
- Only intersections inside that frame's interior should be filled.

**Written solution:** Each rectangular color-5 frame defines its own local subproblem. Inside one frame, rows are selected by red(2) markers on the left and right interior edges, and columns are selected by blue(3) markers on the top and bottom interior edges. Read the frame's key color from the cell above the frame, then fill only the intersections inside that frame with that key color.

**Program solution (Python reference):**
```python
def solve_hard_43_local_marked_rowcol_crossings_in_frames(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v not in (0,5):
                    key = v
                    break
        assert key is not None
        rows = [r for r in range(ir0, ir1+1) if g[r][ic0] == 2 and g[r][ic1] == 2]
        cols = [c for c in range(ic0, ic1+1) if g[ir0][c] == 3 and g[ir1][c] == 3]
        for r in rows:
            for c in cols:
                out[r][c] = key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 8 0 0 0 0 0 0
0 0 5 0 3 3 0 5 0 0 0 5 5 5 5 5 5 0
0 0 5 2 0 0 2 5 0 0 0 5 0 3 0 3 5 0
0 0 5 0 0 0 0 5 0 0 0 5 2 0 0 2 5 0
0 0 5 2 3 3 2 5 0 0 0 5 0 0 0 0 5 0
0 0 5 5 5 5 5 5 0 0 0 5 2 0 0 2 5 0
0 0 0 0 0 0 0 0 0 0 0 5 2 3 0 3 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 8 0 0 0 0 0 0
0 0 5 0 3 3 0 5 0 0 0 5 5 5 5 5 5 0
0 0 5 2 6 6 2 5 0 0 0 5 0 3 0 3 5 0
0 0 5 0 0 0 0 5 0 0 0 5 2 8 0 8 5 0
0 0 5 2 6 6 2 5 0 0 0 5 0 0 0 0 5 0
0 0 5 5 5 5 5 5 0 0 0 5 2 8 0 8 5 0
0 0 0 0 0 0 0 0 0 0 0 5 2 3 0 3 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 3 0 3 0 5 0 0 9 0 0 0 0 0 0
0 0 0 5 2 0 0 0 2 5 0 0 5 5 5 5 5 5 0
0 0 0 5 0 0 0 0 0 5 0 0 5 0 3 3 3 5 0
0 0 0 5 2 0 0 0 2 5 0 0 5 2 0 0 2 5 0
0 0 0 5 2 3 0 3 2 5 0 0 5 0 0 0 0 5 0
0 0 0 5 5 5 5 5 5 5 0 0 5 2 0 0 2 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 3 3 3 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 3 0 3 0 5 0 0 9 0 0 0 0 0 0
0 0 0 5 2 7 0 7 2 5 0 0 5 5 5 5 5 5 0
0 0 0 5 0 0 0 0 0 5 0 0 5 0 3 3 3 5 0
0 0 0 5 2 7 0 7 2 5 0 0 5 2 9 9 9 5 0
0 0 0 5 2 7 0 7 2 5 0 0 5 0 0 0 0 5 0
0 0 0 5 5 5 5 5 5 5 0 0 5 2 9 9 9 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 3 3 3 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 0 3 0 3 0 5 0 0 0 5 0 3 0 3 3 5 0
0 0 5 2 0 0 0 2 5 0 0 0 5 2 0 0 0 2 5 0
0 0 5 2 0 0 0 2 5 0 0 0 5 0 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 0 5 2 3 0 3 3 5 0
0 0 5 0 3 0 3 0 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 0 3 0 3 0 5 0 0 0 5 0 3 0 3 3 5 0
0 0 5 2 6 0 6 2 5 0 0 0 5 2 7 0 7 7 5 0
0 0 5 2 6 0 6 2 5 0 0 0 5 0 0 0 0 0 5 0
0 0 5 0 0 0 0 0 5 0 0 0 5 2 3 0 3 3 5 0
0 0 5 0 3 0 3 0 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 3 0 3 0 5 0 0 6 0 0 0 0 0 0 0 0
0 0 5 2 0 0 0 2 5 0 0 5 5 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 3 0 3 0 3 5 0
0 0 5 2 0 0 0 2 5 0 0 5 2 0 0 0 0 2 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 5 0
0 0 5 2 3 0 3 2 5 0 0 5 0 0 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 0 0 5 2 0 0 0 0 2 5 0
0 0 0 0 0 0 0 0 0 0 0 5 2 3 0 3 0 3 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 3 0 3 0 5 0 0 6 0 0 0 0 0 0 0 0
0 0 5 2 8 0 8 2 5 0 0 5 5 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 3 0 3 0 3 5 0
0 0 5 2 8 0 8 2 5 0 0 5 2 6 0 6 0 6 5 0
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 5 0
0 0 5 2 8 0 8 2 5 0 0 5 0 0 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 0 0 5 2 6 0 6 0 6 5 0
0 0 0 0 0 0 0 0 0 0 0 5 2 3 0 3 0 3 5 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 3 0 3 0 3 5 0 0 0 7 0 0 0 0 0 0 0
0 0 5 2 0 0 0 0 2 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 3 0 3 0 5 0
0 0 5 2 0 0 0 0 2 5 0 0 0 5 2 0 0 0 2 5 0
0 0 5 2 3 0 3 0 3 5 0 0 0 5 0 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 5 0 0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 2 0 0 0 2 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 3 0 3 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 3 0 3 0 3 5 0 0 0 7 0 0 0 0 0 0 0
0 0 5 2 9 0 9 0 9 5 0 0 0 5 5 5 5 5 5 5 0
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 3 0 3 0 5 0
0 0 5 2 9 0 9 0 9 5 0 0 0 5 2 7 0 7 2 5 0
0 0 5 2 3 0 3 0 3 5 0 0 0 5 0 0 0 0 0 5 0
0 0 5 5 5 5 5 5 5 5 0 0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 2 7 0 7 2 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 3 0 3 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Tile the Template Library according to the Code Grid (`hard_44_template_tiling_from_code_grid`)

**Difficulty:** hard

**Skills:** template extraction, symbolic lookup, mosaic construction

**Scaffold notes:**
- The left side stores a small template library inside frames.
- Each template is identified by its unique nonzero color.
- Every code cell on the right should be expanded into the matching template.

**Written solution:** Extract the framed templates from the library area and map each template's unique color to its interior pattern. Then read the code grid on the right: each code cell names one template color. Build the output as a tiled mosaic in which every code cell is replaced by the corresponding template interior.

**Program solution (Python reference):**
```python
def solve_hard_44_template_tiling_from_code_grid(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 1)
    code_to_template = {}
    frame_cells = set()
    for box in boxes:
        for r in range(box[0], box[2]+1):
            for c in range(box[1], box[3]+1):
                frame_cells.add((r,c))
        ir0,ic0,ir1,ic1 = inside(box)
        temp = [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
        colors = {v for row in temp for v in row if v != 0}
        assert len(colors) == 1
        code = next(iter(colors))
        code_to_template[code] = temp
    code_cells = [(r,c) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] != 0 and (r,c) not in frame_cells]
    r0,c0,r1,c1 = bbox(code_cells)
    codes = [row[c0:c1+1] for row in g[r0:r1+1]]
    th,tw = dims(next(iter(code_to_template.values())))
    out = zeros(len(codes)*th, len(codes[0])*tw, 0)
    for rr,row in enumerate(codes):
        for cc,code in enumerate(row):
            paste(out, code_to_template[code], rr*th, cc*tw, transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 0 0 1 0 0 0 0 0 0 0 0 2 3 0 0
0 1 2 2 0 1 0 0 0 0 0 0 0 0 4 2 0 0
0 1 0 2 0 1 0 0 0 0 0 0 0 0 3 4 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 3 3 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 3 0
2 2 0 3 3 3
0 2 0 0 0 0
4 4 0 2 0 0
0 4 0 2 2 0
0 4 0 0 2 0
0 3 0 4 4 0
3 3 3 0 4 0
0 0 0 0 4 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 2 0 1 0 0 0 0 0 0 0 4 4 2 0 0
0 0 1 2 2 0 1 0 0 0 0 0 0 0 3 2 3 0 0
0 0 1 0 2 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 0 3 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 0 3 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 4 4 4 0 2 0
0 4 0 0 4 0 2 2 0
0 4 0 0 4 0 0 2 0
3 0 3 0 2 0 3 0 3
0 3 0 2 2 0 0 3 0
3 0 3 0 2 0 3 0 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 2 0 1 0 0 0 0 0 0 0 0 0 0 3 2 0 0
0 1 0 2 0 1 0 0 0 0 0 0 0 0 0 0 2 4 0 0
0 1 0 2 2 1 0 0 0 0 0 0 0 0 0 0 4 3 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 3 3 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3 0 2 2 0
0 3 0 0 2 0
3 3 3 0 2 2
2 2 0 4 0 4
0 2 0 4 4 4
0 2 2 0 0 0
4 0 4 0 3 0
4 4 4 0 3 0
0 0 0 3 3 3
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 2 0 2 1 0 0 0 0 0 0 2 4 3 0 0
0 0 1 2 2 2 1 0 0 0 0 0 0 3 2 4 0 0
0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 3 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 3 3 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 2 0 4 0 3 3 0
2 2 2 4 4 4 0 3 0
0 0 0 0 4 0 0 3 3
3 3 0 2 0 2 0 4 0
0 3 0 2 2 2 4 4 4
0 3 3 0 0 0 0 4 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 2 0 1 0 0 0 0 0 0 0 0 0 4 2 3 0 0
0 1 2 2 0 1 0 0 0 0 0 0 0 0 0 2 3 4 0 0
0 1 0 2 0 1 0 0 0 0 0 0 0 0 0 3 4 2 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 3 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 3 3 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 4 0 0 2 0 0 3 0
4 4 4 2 2 0 0 3 0
0 4 0 0 2 0 3 3 3
0 2 0 0 3 0 0 4 0
2 2 0 0 3 0 4 4 4
0 2 0 3 3 3 0 4 0
0 3 0 0 4 0 0 2 0
0 3 0 4 4 4 2 2 0
3 3 3 0 4 0 0 2 0
```


## Overlay Two Keyed Components after Rotating the Second (`hard_45_overlay_selected_components_with_rotation`)

**Difficulty:** hard

**Skills:** key-driven selection, rotation, overlay logic

**Scaffold notes:**
- The top row names the two relevant colors.
- Crop the first selected component as-is, but rotate the second 90° clockwise.
- Overlay them at a shared top-left origin; overlaps become cyan(8).

**Written solution:** Read the two nonzero key colors from the first row and find the components of those colors below. Crop both components to their bounding boxes, rotate the second crop 90° clockwise, and align the two crops at the same top-left corner on a canvas large enough for both. Cells coming only from the first component keep the first color, cells coming only from the second keep the second color, and overlapping cells become cyan(8).

**Program solution (Python reference):**
```python
def solve_hard_45_overlay_selected_components_with_rotation(g: Grid) -> Grid:
    keys = [v for v in g[0] if v != 0]
    a,b = keys[0], keys[1]
    comps = {comp["color"]: comp for comp in connected_components([row[:] for row in g[1:]])}
    ca = comps[a]
    cb = comps[b]
    ga = crop_bbox(g[1:], ca["bbox"])
    gb = crop_bbox(g[1:], cb["bbox"])
    ga = [[a if v == a else 0 for v in row] for row in ga]
    gb = [[b if v == b else 0 for v in row] for row in gb]
    gb = rotate_grid_cw(gb)
    h = max(len(ga), len(gb))
    w = max(len(ga[0]), len(gb[0]))
    out = zeros(h,w,0)
    for r in range(len(ga)):
        for c in range(len(ga[0])):
            if ga[r][c]:
                out[r][c] = a
    for r in range(len(gb)):
        for c in range(len(gb[0])):
            if gb[r][c]:
                if out[r][c] != 0:
                    out[r][c] = 8
                else:
                    out[r][c] = b
    return out
```

**Train 1 input**
```text
0 2 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 4 4 0 0 0 0
0 2 2 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 4
8 8 8
0 0 4
```

**Train 2 input**
```text
0 5 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 5
3 5 0
3 5 0
```

**Train 3 input**
```text
0 7 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 2 2 0 0 0 0
0 0 7 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 2
8 8 2
2 7 0
```

**Train 4 input**
```text
0 6 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 8 8
8 8 6
0 6 0
```

**Test 1 input**
```text
0 4 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 7 0 0 0 0 0
0 0 4 0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
4 8 8
7 8 0
0 4 0
```


## Complete the Symmetry inside Each Frame (`hard_46_local_symmetry_completion_by_frame_key`)

**Difficulty:** hard

**Skills:** local reflection, frame-local transforms, key-controlled axis

**Scaffold notes:**
- Handle each frame independently.
- Key 6 means reflect across the frame's vertical midline; key 7 means reflect across the horizontal midline.
- Add the reflected copy without removing the original shape.

**Written solution:** For every framed chamber, read the key above it to decide which symmetry to apply. A key of 6 requests horizontal reflection across the chamber's vertical centerline, while 7 requests vertical reflection across the chamber's horizontal centerline. Reflect every interior shape cell accordingly, keeping the original cells and adding the mirrored ones.

**Program solution (Python reference):**
```python
def solve_hard_46_local_symmetry_completion_by_frame_key(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v in (6,7):
                    key = v
                    break
        assert key is not None
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                v = g[r][c]
                if v != 0:
                    if key == 6:
                        mc = ic0 + ic1 - c
                        out[r][mc] = v
                    else:
                        mr = ir0 + ir1 - r
                        out[mr][c] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 7 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 5 2 0 0 0 0 5 0 0 5 0 3 3 0 0 5
0 0 5 2 2 0 0 0 5 0 0 5 0 0 3 0 0 5
0 0 5 0 2 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 5 0 0 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 0 0 7 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 5 2 0 0 0 2 5 0 0 5 0 3 3 0 0 5
0 0 5 2 2 0 2 2 5 0 0 5 0 0 3 0 0 5
0 0 5 0 2 0 2 0 5 0 0 5 0 0 0 0 0 5
0 0 5 0 0 0 0 0 5 0 0 5 0 0 3 0 0 5
0 0 5 5 5 5 5 5 5 0 0 5 0 3 3 0 0 5
0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 4 4 4 0 0 5 0 0 6 0 0 0 0 0 0
0 0 0 5 0 0 4 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 6 0 0 0 0 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 6 6 0 0 0 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 0 5 5 5 5 5 5 5 5 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 4 4 4 0 0 5 0 0 6 0 0 0 0 0 0
0 0 0 5 0 0 4 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 0 5 0 0 0 0 0 0 5 0 0 5 6 0 0 0 6 5
0 0 0 5 0 0 4 0 0 0 5 0 0 5 6 6 0 6 6 5
0 0 0 5 0 4 4 4 0 0 5 0 0 5 0 0 0 0 0 5
0 0 0 5 5 5 5 5 5 5 5 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 7 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 5 7 0 0 0 0 0 5 0 0 5 0 2 2 0 0 5
0 0 5 7 7 7 0 0 0 5 0 0 5 0 2 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 2 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 5 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 7 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 5 5 5 5 5 5 5
0 0 5 7 0 0 0 0 7 5 0 0 5 0 2 2 0 0 5
0 0 5 7 7 7 7 7 7 5 0 0 5 0 2 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 2 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 2 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 5 0 2 2 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 8 0 8 0 0 5 0 0 0 6 0 0 0 0 0 0 0
0 0 5 0 8 8 8 0 0 5 0 0 0 5 5 5 5 5 5 5 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 3 3 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 3 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 8 0 8 0 0 5 0 0 0 6 0 0 0 0 0 0 0
0 0 5 0 8 8 8 0 0 5 0 0 0 5 5 5 5 5 5 5 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 0 5 3 3 0 0 3 3 5
0 0 5 0 8 8 8 0 0 5 0 0 0 5 0 3 0 0 3 0 5
0 0 5 0 8 0 8 0 0 5 0 0 0 5 0 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 7 0 0 0 0 0 0 0
0 0 5 4 4 0 0 0 0 5 0 0 5 5 5 5 5 5 5 5
0 0 5 0 4 0 0 0 0 5 0 0 5 0 7 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 7 7 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 7 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 7 0 0 0 0 0 0 0
0 0 5 4 4 0 0 4 4 5 0 0 5 5 5 5 5 5 5 5
0 0 5 0 4 0 0 4 0 5 0 0 5 0 7 0 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 7 7 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 7 0 0 0 5
0 0 5 0 0 0 0 0 0 5 0 0 5 0 0 7 0 0 0 5
0 0 5 5 5 5 5 5 5 5 0 0 5 0 7 7 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 0 7 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Choose the Most Holed Component and Tile it 2×2 (`hard_47_tile_component_with_most_holes`)

**Difficulty:** hard

**Skills:** hole counting, component selection, tiling

**Scaffold notes:**
- Do not select by area alone.
- Count enclosed zero-regions inside each component's bounding box.
- Crop the winner and tile that crop in a 2×2 block.

**Written solution:** Inspect each connected component and count how many enclosed holes it contains, meaning zero-regions trapped inside its cropped bounding box that do not touch the crop border. Select the component with the highest hole count, crop it tightly, and tile that crop in a 2×2 arrangement. The component's original color and internal zeros are preserved.

**Program solution (Python reference):**
```python
def solve_hard_47_tile_component_with_most_holes(g: Grid) -> Grid:
    best = None
    best_holes = -1
    best_cells = -1
    for comp in connected_components(g):
        cg = crop_bbox(g, comp["bbox"])
        holes = component_hole_count([[1 if v == comp["color"] else 0 for v in row] for row in cg])
        score = (holes, len(comp["cells"]))
        if score > (best_holes, best_cells):
            best_holes, best_cells = score
            best = [[comp["color"] if v == comp["color"] else 0 for v in row] for row in cg]
    return tile_2x2(best)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 4 4 4 4 4 0 0 0
0 2 0 2 0 0 0 4 0 4 0 4 0 0 0
0 2 2 2 0 0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 4 0 4 0 4 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 3 0 0 0 0 7 7 7 0 0 0
0 3 3 3 3 3 0 0 0 0 7 0 7 0 0 0
0 3 0 3 0 3 0 0 0 0 7 7 7 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 3 3 3 3 3 3 3
3 0 3 0 3 3 0 3 0 3
3 3 3 3 3 3 3 3 3 3
3 0 3 0 3 3 0 3 0 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 0 3 0 3 3 0 3 0 3
3 3 3 3 3 3 3 3 3 3
3 0 3 0 3 3 0 3 0 3
3 3 3 3 3 3 3 3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 2 2 2 2 2 0 0
0 8 0 8 0 0 0 0 2 0 2 0 2 0 0
0 8 8 8 0 0 0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 2 0 2 0 2 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 6 0 0 0 3 3 3 0 0 0 0
0 0 6 6 6 6 6 0 0 0 3 0 3 0 0 0 0
0 0 6 0 6 0 6 0 0 0 3 3 3 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 6 0 6 0 6
6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 6 0 6 0 6
6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 6 0 6 0 6
6 6 6 6 6 6 6 6 6 6
6 0 6 0 6 6 0 6 0 6
6 6 6 6 6 6 6 6 6 6
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 2 2 2 2 2 0 0 0
0 5 0 5 0 0 0 0 2 0 2 0 2 0 0 0
0 5 5 5 0 0 0 0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 0 2 2 0 2 0 2
2 2 2 2 2 2 2 2 2 2
```


## Rotate Each Framed Object and Recenter it (`hard_48_local_rotate_object_to_key_center`)

**Difficulty:** hard

**Skills:** local rotation, recentering, frame-wise transforms

**Scaffold notes:**
- Each frame has one object and one key above it.
- Keys 2/3/4/5 mean 0°/90°/180°/270° clockwise rotation.
- After rotating, clear the old interior and place the rotated object centered in the frame.

**Written solution:** Treat each color-1 frame separately. Crop the object's bounding box from the frame interior, rotate it according to the key above the frame, erase the old interior contents, and place the rotated crop centered inside the frame. Keep the frame and key markers.

**Program solution (Python reference):**
```python
def solve_hard_48_local_rotate_object_to_key_center(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 1):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v in (2,3,4,5):
                    key = v
                    break
        assert key is not None
        # clear the interior
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                out[r][c] = 0
        cells = [(r,c) for r in range(ir0, ir1+1) for c in range(ic0, ic1+1) if g[r][c] != 0]
        box2 = bbox(cells)
        obj = crop_bbox(g, box2)
        colors = {v for row in obj for v in row if v != 0}
        color = next(iter(colors))
        obj = [[color if v == color else 0 for v in row] for row in obj]
        rot_map = {2:0, 3:1, 4:2, 5:3}
        for _ in range(rot_map[key]):
            obj = rotate_grid_cw(obj)
        ph,pw = dims(obj)
        ih,iw = ir1-ir0+1, ic1-ic0+1
        top = ir0 + (ih - ph)//2
        left = ic0 + (iw - pw)//2
        paste(out, obj, top, left, transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 3 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 1 0 0 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 6 0 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 6 6 6 0 0 1 0 0 1 4 0 0 0 0 1
0 0 1 0 0 0 0 0 1 0 0 1 4 4 0 0 0 1
0 0 1 1 1 1 1 1 1 0 0 1 0 4 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 3 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 1 0 6 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 0 6 6 6 0 1 0 0 1 0 0 0 0 0 1
0 0 1 0 0 0 0 0 1 0 0 1 0 0 4 4 0 1
0 0 1 0 0 0 0 0 1 0 0 1 0 4 4 0 0 1
0 0 1 1 1 1 1 1 1 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 0 0 5 0 0 0 0 0 0
0 0 0 1 7 7 7 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 0 1 0 7 0 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 0 1 0 7 0 0 0 0 1 0 0 1 0 2 0 0 0 1
0 0 0 1 0 0 0 0 0 0 1 0 0 1 0 2 2 2 0 1
0 0 0 1 1 1 1 1 1 1 1 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 7 0 0 0 1 0 0 5 0 0 0 0 0 0
0 0 0 1 0 0 7 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 0 1 0 7 7 7 0 0 1 0 0 1 0 0 0 0 0 1
0 0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 2 0 0 1
0 0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 2 0 0 1
0 0 0 1 1 1 1 1 1 1 1 0 0 1 0 2 2 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 2 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 1 0 8 8 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 0 0 8 0 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 0 0 8 8 0 0 1 0 0 1 0 5 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 5 5 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 1 0 0 5 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 2 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1
0 0 1 0 0 0 8 0 0 1 0 0 1 0 0 0 0 0 1
0 0 1 0 8 8 8 0 0 1 0 0 1 0 5 0 0 0 1
0 0 1 0 8 0 0 0 0 1 0 0 1 0 5 5 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 5 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 4 0 0 0 0 0 0 0
0 0 1 0 3 0 0 0 0 1 0 0 0 1 1 1 1 1 1 1 1
0 0 1 3 3 3 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1
0 0 1 0 3 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 6 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 6 6 6 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 4 0 0 0 0 0 0 0
0 0 1 0 0 3 0 0 0 1 0 0 0 1 1 1 1 1 1 1 1
0 0 1 0 3 3 3 0 0 1 0 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 3 0 0 0 1 0 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 6 6 6 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 0 1 0 0 0 6 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 5 0 0 0 0 0 0 0
0 0 1 4 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1 1
0 0 1 4 4 4 0 0 0 1 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 7 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 7 7 0 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 1 0 0 7 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 5 0 0 0 0 0 0 0
0 0 1 0 0 4 4 0 0 1 0 0 1 1 1 1 1 1 1 1
0 0 1 0 0 4 0 0 0 1 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 4 0 0 0 1 0 0 1 0 0 0 0 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 7 7 0 0 1
0 0 1 0 0 0 0 0 0 1 0 0 1 0 7 7 0 0 0 1
0 0 1 1 1 1 1 1 1 1 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Expand a Rotation Code Grid into a Full Mosaic (`hard_49_rotation_code_mosaic`)

**Difficulty:** hard

**Skills:** template extraction, rotation coding, tiled output

**Scaffold notes:**
- Extract the source template from the single frame.
- The code grid uses 2/3/4/5 for 0°/90°/180°/270° rotations.
- Replace each code cell by the corresponding rotated copy of the source template.

**Written solution:** Crop the single framed source template from the input. Then read the separate code grid: each code cell tells you how to rotate the source template before using it. Expand the code grid into a larger mosaic by replacing every code cell with the correctly rotated copy of the source template.

**Program solution (Python reference):**
```python
def solve_hard_49_rotation_code_mosaic(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 1)
    assert len(boxes) == 1
    box = boxes[0]
    frame_cells = {(r,c) for r in range(box[0], box[2]+1) for c in range(box[1], box[3]+1)}
    ir0,ic0,ir1,ic1 = inside(box)
    src = [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
    colors = {v for row in src for v in row if v != 0}
    color = next(iter(colors))
    src = [[color if v == color else 0 for v in row] for row in src]
    code_cells = [(r,c) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] in (2,3,4,5) and (r,c) not in frame_cells]
    r0,c0,r1,c1 = bbox(code_cells)
    codes = [row[c0:c1+1] for row in g[r0:r1+1]]
    h,w = dims(src)
    out = zeros(len(codes)*h, len(codes[0])*w, 0)
    rot_map = {2:0, 3:1, 4:2, 5:3}
    for rr,row in enumerate(codes):
        for cc,code in enumerate(row):
            pat = src
            for _ in range(rot_map[code]):
                pat = rotate_grid_cw(pat)
            paste(out, pat, rr*h, cc*w, transparent=0)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 3 4 0 0
0 1 1 1 1 1 0 0 0 0 0 5 2 3 0 0
0 1 6 0 6 1 0 0 0 0 0 0 0 0 0 0
0 1 6 6 6 1 0 0 0 0 0 0 0 0 0 0
0 1 0 6 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 0 6 0 6 6 0 6 0
6 6 6 6 6 0 6 6 6
0 6 0 0 6 6 6 0 6
6 6 0 6 0 6 0 6 6
0 6 6 6 6 6 6 6 0
6 6 0 0 6 0 0 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 4 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 5 3 0 0
0 1 6 6 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 6 0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 6 6 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6 0 0 6
6 6 6 6 6 6
6 0 0 6 0 0
6 6 0 6 6 0
0 6 0 0 6 0
0 6 6 0 6 6
0 0 6 0 0 6
6 6 6 6 6 6
6 0 0 6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 2 5 0 0
0 1 1 1 1 1 0 0 0 0 0 3 4 2 0 0
0 1 0 6 0 1 0 0 0 0 0 0 0 0 0 0
0 1 6 6 6 1 0 0 0 0 0 0 0 0 0 0
0 1 6 0 6 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 0 6 0 6 0 0 6 6
6 6 6 6 6 6 6 6 0
0 6 0 6 0 6 0 6 6
6 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6
6 6 0 0 6 0 6 0 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 5 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 2 5 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 6 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 6 6 6 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 6 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 0 0 0 6 6 0 6 6
6 6 6 0 6 0 0 6 0
0 0 6 6 6 0 6 6 0
6 0 0 6 0 0 0 6 6
6 6 6 6 6 6 0 6 0
0 0 6 0 0 6 6 6 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 5 4 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 5 4 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 3 2 5 0 0
0 1 6 0 6 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 6 6 6 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 6 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 0 0 6 0 0 6 6
0 6 6 6 6 6 6 6 0
6 6 0 6 0 6 0 6 6
6 0 6 6 6 0 0 6 0
6 6 6 0 6 6 6 6 6
0 6 0 6 6 0 6 0 6
0 6 6 6 0 6 6 6 0
6 6 0 6 6 6 0 6 6
0 6 6 0 6 0 6 6 0
```

