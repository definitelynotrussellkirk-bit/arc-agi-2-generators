# ARC Puzzle Bank — Fourth 21 Puzzles
This fourth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`22`–`28`) so it reads as a direct continuation of the first three bundles.
To make the supervision denser, this volume uses **more example pairs on average**: easy and medium tasks each have 4 train pairs, hard tasks each have 5 train pairs, for an average of **4.33 train pairs per task**.
Each puzzle includes train/test examples, scaffold notes, a written solution, and a Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_fourth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_fourth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_fourth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_22_recolor_exact_pluses` — **Recolor the Exact Pluses**
- `easy_23_fill_hollow_ring_centers` — **Fill the Centers of Hollow 3x3 Rings**
- `easy_24_bridge_single_horizontal_gaps` — **Bridge Single Horizontal Gaps**
- `easy_25_complete_descending_diagonal_gaps` — **Complete Descending Diagonal Gaps**
- `easy_26_complete_2x2_from_l` — **Complete 2x2 Blocks from L Shapes**
- `easy_27_recolor_exact_2x3_rectangles` — **Recolor Exact 2x3 Rectangles**
- `easy_28_mirror_singletons_across_horizontal_midline` — **Mirror Singletons Across the Horizontal Midline**

### Medium (7)
- `medium_22_gravity_down_each_column` — **Apply Gravity Down Each Column**
- `medium_23_connect_aligned_pairs` — **Connect Aligned Pairs**
- `medium_24_keep_only_even_area_components` — **Keep Only the Even-Area Components**
- `medium_25_rotate_template_by_key_and_center` — **Rotate the Template by the Key and Center It**
- `medium_26_crop_and_stack_components_vertically_by_area` — **Crop and Stack Components Vertically by Area**
- `medium_27_place_cross_at_bbox_center` — **Place a Cross at Each Bounding-Box Center**
- `medium_28_fill_component_bboxes_with_key_color` — **Fill Component Bounding Boxes with the Key Color**

### Hard (7)
- `hard_22_local_key_rotate_template_inside_frames` — **Rotate the Template Inside Each Frame Using the Local Key**
- `hard_23_make_transform_strip_from_template_and_keys` — **Make a Transform Strip from the Template and the Keys**
- `hard_24_stamp_template_at_every_mask_cell` — **Stamp the Template at Every Mask Cell**
- `hard_25_bar_chart_component_areas_by_color` — **Make a Bar Chart of Component Areas by Color**
- `hard_26_stamp_unique_bisymmetric_component_at_markers` — **Stamp the Unique Bi-Symmetric Component at the Markers**
- `hard_27_frame_local_intersections_with_fill_key` — **Mark Local Row–Column Intersections Inside Each Frame**
- `hard_28_select_by_marker_count_scale_and_center` — **Select by Marker Count, Then Scale**

## Recolor the Exact Pluses (`easy_22_recolor_exact_pluses`)

**Difficulty:** easy

**Skills:** motif detection, same-size recolor, cardinal neighborhood

**Scaffold notes:**
- Look for cells that have four cardinal neighbors of the same source color.
- Once you find a plus center, recolor the center and its four arms.
- Ignore isolated green cells and short lines that do not make a full plus.

**Written solution:** Find every exact plus made of green(3) cells: a center with green cells directly above, below, left, and right. Recolor the center and its four arms to orange(7). Leave other green cells unchanged.

**Program solution (Python reference):**
```python
def solve_easy_22_recolor_exact_pluses(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    centers=[]
    for r in range(1, h-1):
        for c in range(1, w-1):
            if g[r][c]==3 and g[r-1][c]==3 and g[r+1][c]==3 and g[r][c-1]==3 and g[r][c+1]==3:
                centers.append((r,c))
    for r,c in centers:
        for rr,cc in [(r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
            out[rr][cc]=7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 3
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
3 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 3
0 0 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 0 0
3 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
```

**Train 2 output**
```text
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
```

**Train 3 input**
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 3 0
3 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 3
```

**Train 3 output**
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 7 7 0
3 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 3
```

**Train 4 input**
```text
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3
```

**Train 4 output**
```text
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 3
0 0 3 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 3 0
3 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 3
0 0 7 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 7 7 0
3 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
```

## Fill the Centers of Hollow 3x3 Rings (`easy_23_fill_hollow_ring_centers`)

**Difficulty:** easy

**Skills:** pattern windows, 3x3 ring detection, center fill

**Scaffold notes:**
- Scan every 3x3 window.
- The eight perimeter cells must all be blue(1).
- Only the center cell changes, and only when the center is the hole of a full ring.

**Written solution:** Whenever you see an exact 3x3 hollow ring of blue(1) cells, paint its center red(2). Leave all other cells unchanged.

**Program solution (Python reference):**
```python
def solve_easy_23_fill_hollow_ring_centers(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            ok=True
            for dr in range(3):
                for dc in range(3):
                    rr,cc=r+dr,c+dc
                    if dr==1 and dc==1:
                        if g[rr][cc]!=0:
                            ok=False
                    else:
                        if g[rr][cc]!=1:
                            ok=False
            if ok:
                out[r+1][c+1]=2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 1
0 1 1 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 1 1 1 0
1 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 1
0 1 1 1 0 0 0 0 0 0
0 1 2 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 2 1 0
0 0 0 0 0 0 1 1 1 0
1 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0
0 0 0 0 1 0 1 0 0
0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1
```

**Train 2 output**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0
0 0 0 0 1 2 1 0 0
0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1
```

**Train 3 input**
```text
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
```

**Train 3 output**
```text
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 2 1 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0
0 0 1 2 1 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 1 2 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 1 2 1 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 1
0 0 1 1 1 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0
0 1 1 1 0 0 0 0 1 0 1 0
0 1 0 1 0 0 0 0 1 1 1 0
0 1 1 1 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 1
0 0 1 1 1 0 0 0 0 0 0 0
0 0 1 2 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0
0 1 1 1 0 0 0 0 1 2 1 0
0 1 2 1 0 0 0 0 1 1 1 0
0 1 1 1 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
```

## Bridge Single Horizontal Gaps (`easy_24_bridge_single_horizontal_gaps`)

**Difficulty:** easy

**Skills:** row pattern detection, single-gap completion, same-size edit

**Scaffold notes:**
- Look for the local pattern 6,0,6 in a row.
- Only fill the middle cell.
- Do not trigger on patterns that are really part of longer magenta runs.

**Written solution:** Whenever two magenta(6) cells sit in the same row with exactly one blank cell between them, fill that single gap with cyan(8). Do not extend longer runs.

**Program solution (Python reference):**
```python
def solve_easy_24_bridge_single_horizontal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==6 and g[r][c+1]==6:
                if c-2 < 0 or g[r][c-2] != 6:
                    if c+2 >= w or g[r][c+2] != 6:
                        out[r][c]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 6
0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 6
0 6 8 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6
```

**Train 2 output**
```text
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 8 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 8 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 8 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 8 6 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 6 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 6 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 6 8 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 8 6 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0
```

## Complete Descending Diagonal Gaps (`easy_25_complete_descending_diagonal_gaps`)

**Difficulty:** easy

**Skills:** diagonal pattern detection, single-gap completion, same-color fill

**Scaffold notes:**
- Work only along down-right diagonals.
- The pattern is 4,0,4 with one missing center cell.
- Ignore longer diagonal runs; this rule only fills a single missing middle cell.

**Written solution:** If two yellow(4) cells lie on the same down-right diagonal with exactly one blank cell between them, fill the middle diagonal cell with yellow(4). Leave other yellow cells alone.

**Program solution (Python reference):**
```python
def solve_easy_25_complete_descending_diagonal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c]==4 and g[r+1][c+1]==0 and g[r+2][c+2]==4:
                if (r-1 < 0 or c-1 < 0 or g[r-1][c-1] != 4) and (r+3 >= h or c+3 >= w or g[r+3][c+3] != 4):
                    out[r+1][c+1]=4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 4
0 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 4 4 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
```

**Train 2 output**
```text
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
4 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0
4 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4
```

**Train 4 output**
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0
```

## Complete 2x2 Blocks from L Shapes (`easy_26_complete_2x2_from_l`)

**Difficulty:** easy

**Skills:** 2x2 window logic, missing-corner completion, same-color fill

**Scaffold notes:**
- Inspect each 2x2 window independently.
- You only act when there are exactly three source-colored cells and one blank.
- Fill the blank corner with the same source color.

**Written solution:** Whenever a 2x2 window contains exactly three gray(5) cells in an L shape, fill the missing corner with gray(5) to complete the 2x2 block.

**Program solution (Python reference):**
```python
def solve_easy_26_complete_2x2_from_l(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            cells=[g[r+dr][c+dc] for dr in range(2) for dc in range(2)]
            if cells.count(5)==3 and cells.count(0)==1:
                for dr in range(2):
                    for dc in range(2):
                        if g[r+dr][c+dc]==0:
                            out[r+dr][c+dc]=5
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 5
0 0 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0
0 0 0 0 0 5 0 0 0
5 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 5
0 5 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0
0 0 0 0 0 5 5 0 0
5 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
```

**Train 2 output**
```text
5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 5
0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 5
0 0 0 0 5 5 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 5
0 5 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0
5 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 5
0 5 5 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 5 5 0
5 0 0 0 0 0 0 0 0 0 0 0
```

## Recolor Exact 2x3 Rectangles (`easy_27_recolor_exact_2x3_rectangles`)

**Difficulty:** easy

**Skills:** component detection, bounding-box test, same-size recolor

**Scaffold notes:**
- Extract each connected red component.
- Check that its area is 6 and its bounding box is 2x3 or 3x2.
- Only fully filled rectangles are recolored.

**Written solution:** Find every connected red(2) component that is a fully filled 2x3 or 3x2 rectangle. Recolor those rectangle cells to cyan(8) and leave all other red cells unchanged.

**Program solution (Python reference):**
```python
def solve_easy_27_recolor_exact_2x3_rectangles(g: Grid) -> Grid:
    out = clone(g)
    comps = components4(g, include_colors={2})
    for comp in comps:
        r0,c0,r1,c1 = comp['bbox']
        h = comp['h']; w = comp['w']; area = comp['area']
        if area == 6 and ((h==2 and w==3) or (h==3 and w==2)):
            # ensure full rectangle
            full=True
            for rr in range(r0,r1+1):
                for cc in range(c0,c1+1):
                    if g[rr][cc] != 2:
                        full=False
            if full:
                for rr,cc in comp['cells']:
                    out[rr][cc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 2
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 2 2 0 0
2 0 0 0 0 0 2 2 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 2
0 8 8 8 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
2 0 0 0 0 0 8 8 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 2 output**
```text
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 2
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 2
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 2 2 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 2 2 0 0
2 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0
0 8 8 8 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 8 8 0 0
2 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 2
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 2
0 8 8 8 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
```

## Mirror Singletons Across the Horizontal Midline (`easy_28_mirror_singletons_across_horizontal_midline`)

**Difficulty:** easy

**Skills:** global symmetry, coordinate transform, same-size copy

**Scaffold notes:**
- The mirror changes the row but keeps the column.
- Use row `h-1-r` as the reflected row.
- The output contains both the original singletons and their reflected copies.

**Written solution:** For every orange(7) singleton in the grid, add its mirror image across the horizontal midline. Keep the original singleton too.

**Program solution (Python reference):**
```python
def solve_easy_28_mirror_singletons_across_horizontal_midline(g: Grid) -> Grid:
    out = clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==7:
                mr = h-1-r
                out[mr][c] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
7 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 7 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 7 0
0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0
```

## Apply Gravity Down Each Column (`medium_22_gravity_down_each_column`)

**Difficulty:** medium

**Skills:** column-wise compression, order preservation, same-size transform

**Scaffold notes:**
- Treat each column separately.
- Ignore zeros when collecting the falling cells.
- Write the collected nonzero values back at the bottom of the same column in the same order.

**Written solution:** In each column independently, let the nonzero cells fall straight downward until they are packed against the bottom. Preserve their top-to-bottom order within the column.

**Program solution (Python reference):**
```python
def solve_medium_22_gravity_down_each_column(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,val in enumerate(vals):
            out[start+i][c]=val
    return out
```

**Train 1 input**
```text
2 0 0 0 4 0 0 0
0 3 0 0 0 0 5 0
2 0 0 0 0 0 5 0
0 0 0 0 4 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
2 3 0 0 4 0 5 0
2 3 0 0 4 0 5 6
```

**Train 2 input**
```text
0 0 2 0 0 4 0
8 0 0 0 0 0 0
8 0 0 0 0 0 7
0 0 0 0 0 4 0
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 0 0 7
0 0 2 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 0 0 0 0
8 0 2 0 0 4 7
8 0 2 0 0 4 7
```

**Train 3 input**
```text
0 1 0 0 0 0 0 0 9
0 0 0 0 0 0 0 3 0
0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 3 0
0 1 0 2 0 0 0 3 0
0 1 0 2 0 0 0 3 9
```

**Train 4 input**
```text
5 0 0 0 6 0 0 0 0 0
5 0 0 0 0 0 8 0 0 0
5 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 8 0 0 0
5 0 0 0 6 0 8 0 0 2
5 0 0 0 6 0 8 0 0 2
```

**Test 1 input**
```text
2 0 0 0 0 4 0 0 0
0 0 3 0 0 0 0 0 0
2 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7
2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 4 0 0 0
2 0 3 0 0 4 0 0 7
2 0 3 0 0 4 0 0 7
```

## Connect Aligned Pairs (`medium_23_connect_aligned_pairs`)

**Difficulty:** medium

**Skills:** pair detection, row and column lines, color preservation

**Scaffold notes:**
- Group cells by color.
- Only colors with exactly two cells are candidates.
- If the pair shares a row or a column, fill the inclusive segment between them.

**Written solution:** For each color that appears exactly twice, if the two cells are aligned in one row or one column, fill the entire straight segment between them in that same color.

**Program solution (Python reference):**
```python
def solve_medium_23_connect_aligned_pairs(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors = sorted({g[r][c] for r in range(h) for c in range(w) if g[r][c] != 0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2:
                for c in range(min(c1,c2), max(c1,c2)+1):
                    out[r1][c]=color
            elif c1==c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    out[r][c1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 3 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 3 0 0 0 0 4 0
0 0 0 3 0 0 0 0 4 0
0 0 0 3 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 8
```

**Train 2 output**
```text
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 8
0 0 0 0 5 0 0 0 8
0 0 0 0 5 0 0 0 8
0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8
0 6 6 6 6 6 6 0 8
0 0 0 0 0 0 0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 2 2 2 2 2 2 2 2 0 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 7
9 9 9 9 9 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6
```

**Train 4 output**
```text
3 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
3 0 0 0 4 4 4 4 4 0 0
3 0 0 0 0 0 0 0 0 0 6
3 0 0 0 0 0 0 0 0 0 6
3 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 6
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 8 0 0 0 0 8 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0 0 0
```

## Keep Only the Even-Area Components (`medium_24_keep_only_even_area_components`)

**Difficulty:** medium

**Skills:** connected components, counting cells, selection by parity

**Scaffold notes:**
- Find each nonzero connected component.
- Count its cells.
- Copy only the components with an even number of cells into the output.

**Written solution:** Extract the connected components and keep only those whose area is even. Erase every odd-area component.

**Program solution (Python reference):**
```python
def solve_medium_24_keep_only_even_area_components(g: Grid) -> Grid:
    out=zeros(*dims(g))
    for comp in components4(g):
        if comp['area'] % 2 == 0:
            for r,c in comp['cells']:
                out[r][c]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 5 0 0 0
0 4 4 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 0
0 0 2 2 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0
0 4 4 4 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 0
0 0 2 2 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 3 0 3 0 0
0 0 2 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 2 2 0 0 0 3 3 3 0 0
0 0 2 2 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 0 0 0 0 0
0 2 2 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0
0 0 4 4 0 0 0 0 5 5 5 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Rotate the Template by the Key and Center It (`medium_25_rotate_template_by_key_and_center`)

**Difficulty:** medium

**Skills:** template extraction, rotation by key, centering

**Scaffold notes:**
- Ignore the key after decoding the rotation.
- Crop the template tightly before rotating it.
- After rotation, center the result in an otherwise blank canvas of the original size.

**Written solution:** Take the color-1 template, rotate it according to the singleton key color (2→0°, 3→90° clockwise, 4→180°, 5→270° clockwise), then place the rotated template centered in a blank output grid of the same size.

**Program solution (Python reference):**
```python
def solve_medium_25_rotate_template_by_key_and_center(g: Grid) -> Grid:
    h,w=dims(g)
    # template is all color 1 cells
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    assert cells
    r0,c0,r1,c1=bbox(cells)
    templ=[row[c0:c1+1] for row in g[r0:r1+1]]
    # trim to color1 only
    templ=[[1 if cell==1 else 0 for cell in row] for row in templ]
    key=[g[r][c] for r in range(h) for c in range(w) if g[r][c] in ROT_KEY]
    assert len(key)==1
    k=ROT_KEY[key[0]]
    tg=templ
    for _ in range(k):
        tg=rotate_grid_cw(tg)
    out=zeros(h,w)
    th,tw=dims(tg)
    top,left=centered_top_left(h,w,th,tw)
    paste(out,tg,top,left)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 2
0 1 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Crop and Stack Components Vertically by Area (`medium_26_crop_and_stack_components_vertically_by_area`)

**Difficulty:** medium

**Skills:** component extraction, size-changing output, sorting by area

**Scaffold notes:**
- First isolate each connected component.
- Turn each one into its tight crop.
- Sort by area before stacking, not by reading order.

**Written solution:** Crop each connected component to its tight bounding box. Sort the cropped pieces by increasing area and stack them from top to bottom with one blank row between consecutive pieces.

**Program solution (Python reference):**
```python
def solve_medium_26_crop_and_stack_components_vertically_by_area(g: Grid) -> Grid:
    comps=components4(g)
    comps_sorted=sorted(comps, key=lambda comp: (comp['area'], comp['bbox'][0], comp['bbox'][1]))
    crops=[]
    maxw=0
    for comp in comps_sorted:
        crop=crop_to_bbox(g, comp['cells'])
        crops.append(crop)
        maxw=max(maxw, len(crop[0]))
    totalh=sum(len(crop) for crop in crops) + max(0, len(crops)-1)
    out=zeros(totalh, maxw)
    r=0
    for i,crop in enumerate(crops):
        paste(out,crop,r,0)
        r += len(crop)
        if i < len(crops)-1:
            r += 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2
0 0
3 0
3 3
0 0
4 4
4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 2
0 0 0
3 3 0
0 3 3
0 0 0
0 4 0
4 4 4
0 4 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 3 0 0 0
0 0 2 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 0 0
2 0 0
0 0 0
3 3 0
3 3 0
0 0 0
4 0 4
4 4 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 0 0 0
0 2 2 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 0
2 2 0
0 0 0
0 3 0
3 3 3
0 0 0
4 4 0
4 4 0
4 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 0
0 0 0
3 3 0
0 3 3
0 0 0
0 4 0
4 4 4
0 4 0
```

## Place a Cross at Each Bounding-Box Center (`medium_27_place_cross_at_bbox_center`)

**Difficulty:** medium

**Skills:** component bounding boxes, center detection, symbol replacement

**Scaffold notes:**
- Compute the bounding box of each component.
- Use the geometric center of that box, not the component’s centroid.
- Draw a plus of length 1 in each cardinal direction around the center.

**Written solution:** For each connected component, find the center of its bounding box and place a 5-cell cross of the component’s color there in an otherwise blank output grid. Every input component has an odd-by-odd bounding box, so the center is a single cell.

**Program solution (Python reference):**
```python
def solve_medium_27_place_cross_at_bbox_center(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for comp in components4(g):
        color=max(comp['colors'], key=lambda k: comp['colors'][k])
        r0,c0,r1,c1=comp['bbox']
        bh, bw = comp['h'], comp['w']
        assert bh % 2 == 1 and bw % 2 == 1
        cr = (r0+r1)//2
        cc = (c0+c1)//2
        for rr,cc2 in [(cr,cc),(cr-1,cc),(cr+1,cc),(cr,cc-1),(cr,cc+1)]:
            out[rr][cc2]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 3 0 0 0
0 0 2 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 0 0 0
0 2 0 0 0 0 0 3 0 0 0
0 2 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 3 0 0 0 0
0 2 0 0 0 3 3 3 0 0 0
2 2 2 0 0 0 3 3 3 0 0
0 2 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 2 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 3 0 0
0 0 2 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 3 0 0
0 0 2 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Fill Component Bounding Boxes with the Key Color (`medium_28_fill_component_bboxes_with_key_color`)

**Difficulty:** medium

**Skills:** component bounding boxes, global key color, same-size replacement

**Scaffold notes:**
- Read the unique non-magenta singleton to get the fill color.
- Ignore the original component shapes after finding their bounding boxes.
- Each output rectangle is the solid bounding box of one magenta component.

**Written solution:** The singleton key color tells you the output color. For every magenta(6) component, fill its entire bounding box solid using that key color, on an otherwise blank output grid.

**Program solution (Python reference):**
```python
def solve_medium_28_fill_component_bboxes_with_key_color(g: Grid) -> Grid:
    h,w=dims(g)
    # key is unique singleton of color not 6
    key_cells=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=6]
    key_colors=[clr for r,c,clr in key_cells]
    assert len(key_colors)>=1
    # choose singleton color occurring once and not 6
    cnt=Counter(key_colors)
    key=[clr for clr,n in cnt.items() if n==1][0]
    out=zeros(h,w)
    for comp in components4(g, include_colors={6}):
        r0,c0,r1,c1=comp['bbox']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 2
0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Rotate the Template Inside Each Frame Using the Local Key (`hard_22_local_key_rotate_template_inside_frames`)

**Difficulty:** hard

**Skills:** template extraction, local rotation keys, per-frame centering, recolor by key

**Scaffold notes:**
- The template is shared globally, but each frame has its own local key.
- Treat each frame interior separately and center the transformed copy inside it.
- The output keeps the frame border and the key cell.

**Written solution:** Extract the color-1 template. For each hollow frame, read its local key color: 2 means no rotation, 3 means rotate 90° clockwise, 4 means rotate 180°, and 5 means rotate 270° clockwise. Center that transformed copy inside the frame and recolor it to the key color. Preserve the frames and keys.

**Program solution (Python reference):**
```python
def solve_hard_22_local_key_rotate_template_inside_frames(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    # template
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[1 if cell==1 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    # preserve frames and keys
    for r in range(h):
        for c in range(w):
            if g[r][c] in {7,2,3,4,5}:
                out[r][c]=g[r][c]
    # detect color7 frame components
    for comp in components4(g, include_colors={7}):
        if not is_full_rect_border(g, comp['cells'], 7):
            continue
        fr0,fc0,fr1,fc1 = comp['bbox']
        # key inside frame
        key_cells=[(r,c,g[r][c]) for r in range(fr0+1, fr1) for c in range(fc0+1, fc1) if g[r][c] in LOCAL_ROT_KEY]
        assert len(key_cells)==1
        _,_,key=key_cells[0]
        tg=templ
        for _ in range(LOCAL_ROT_KEY[key]):
            tg=rotate_grid_cw(tg)
        center_paste_inside_box(out, tg, (fr0+1,fc0+1,fr1-1,fc1-1), color=key)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 1 1 0 0 0 0 0 0 7 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 3 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 3 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 7 7 7 7 7 7 7
0 0 1 1 0 0 0 0 7 0 0 0 0 4 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 7 5 0 0 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 7 0 0 0 0 4 7
0 0 0 0 0 0 0 0 7 0 4 4 0 0 7
0 0 0 0 0 0 0 0 7 0 0 4 4 0 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 7 0 0 5 0 0 7 0 0 0 0 0 0 0
0 7 0 5 5 0 0 7 0 0 0 0 0 0 0
0 7 0 5 0 0 0 7 0 0 0 0 0 0 0
0 7 5 0 0 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 3 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 2 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 3 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 2 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 7 7 7 7 7 7 7
0 1 1 1 0 0 0 0 0 0 7 0 0 0 0 5 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 4 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 5 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 4 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 7 7 7 7 7 7 7
0 1 0 0 0 0 0 0 0 7 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 4 7 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Train 5 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 2 2 0 0 7
0 0 0 0 0 0 0 0 0 7 0 2 2 0 0 7
0 0 0 0 0 0 0 0 0 7 0 2 0 0 0 7
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 4 0 0 7 0 0 0 0 0 0 0
0 0 7 0 4 4 0 0 7 0 0 0 0 0 0 0
0 0 7 0 4 4 0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 4 7 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 1 1 0 0 0 0 0 0 0 7 0 0 0 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0 0
0 7 2 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 3 0 0 0 0 7 0 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0 0
0 7 2 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 2 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 2 2 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 0 0 0 0 0 7 0 0
0 7 0 0 0 0 0 7 0 7 3 0 0 0 0 7 0 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Make a Transform Strip from the Template and the Keys (`hard_23_make_transform_strip_from_template_and_keys`)

**Difficulty:** hard

**Skills:** template extraction, mixed transforms, size-changing packing, left-to-right key order

**Scaffold notes:**
- The output is a new strip, not the original canvas.
- The keys are ordered by position from left to right.
- Each transformed copy is recolored to match its own key.

**Written solution:** Crop the template, then read the three key cells from left to right. Each key chooses a transform: 2 = identity, 3 = rotate 90° clockwise, 4 = rotate 180°, 5 = vertical mirror. Recolor each transformed copy to the key color and pack the three copies into one horizontal strip with a single blank column between neighbors.

**Program solution (Python reference):**
```python
def solve_hard_23_make_transform_strip_from_template_and_three_keys(g: Grid) -> Grid:
    h,w=dims(g)
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[1 if cell==1 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    keys=sorted([(c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in STRIP_KEY_OPS])
    assert len(keys)==3
    pieces=[]
    maxh=0
    for _,key in keys:
        piece=apply_op_to_template(templ,key)
        piece=recolor_nonzero(piece,key)
        pieces.append(piece)
        maxh=max(maxh,len(piece))
    totalw=sum(len(piece[0]) for piece in pieces)+2
    out=zeros(maxh,totalw)
    c=0
    for i,piece in enumerate(pieces):
        paste(out,piece,0,c)
        c += len(piece[0])
        if i < len(pieces)-1:
            c += 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 3 0 0 0 5 0 0
```

**Train 1 output**
```text
2 0 0 3 3 0 0 5
2 2 0 3 0 0 5 5
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 4 0 0 0 2 0 0
```

**Train 2 output**
```text
0 3 0 4 4 0 0 2 2 0
3 3 0 0 4 4 0 0 2 2
3 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 2 0 0 0 0 4 0 0
```

**Train 3 output**
```text
0 5 0 0 0 2 0 0 4 4 4
5 5 5 0 2 2 2 0 0 4 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 5 0 0 0 0 3 0
```

**Train 4 output**
```text
4 4 4 0 5 0 5 0 3 3
4 0 4 0 5 5 5 0 3 0
0 0 0 0 0 0 0 0 3 3
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0 0 0 3 0
```

**Train 5 output**
```text
2 2 0 5 5 0 3 3 3
2 2 0 5 5 0 0 3 3
2 0 0 0 5 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 4 0 0 0 0 0 2 0
```

**Test 1 output**
```text
0 5 0 4 4 0 2 0
5 5 0 0 4 0 2 2
```

## Stamp the Template at Every Mask Cell (`hard_24_stamp_template_at_every_mask_cell`)

**Difficulty:** hard

**Skills:** template extraction, mask-driven stamping, union of copies, same-size synthesis

**Scaffold notes:**
- The mask tells you where to place copies of the template.
- Use the same template every time.
- The copies are unioned on a blank canvas; the original input objects do not remain.

**Written solution:** Take the color-2 template and crop it tightly. Every color-3 mask cell becomes the top-left anchor of a copy of that template. Stamp all of those copies onto a blank output grid and union the results using cyan(8).

**Program solution (Python reference):**
```python
def solve_hard_24_stamp_template_at_every_mask_cell(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    templ_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    r0,c0,r1,c1=bbox(templ_cells)
    templ=[[8 if cell==2 else 0 for cell in row[c0:c1+1]] for row in g[r0:r1+1]]
    mask_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3]
    for r,c in mask_cells:
        paste(out,templ,r,c)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 3 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 3 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Make a Bar Chart of Component Areas by Color (`hard_25_bar_chart_component_areas_by_color`)

**Difficulty:** hard

**Skills:** connected components, counting areas, size-changing abstraction

**Scaffold notes:**
- Count cells, not bounding-box area.
- Sort rows by color value.
- The output is a new compact chart, one row per color.

**Written solution:** Each color contributes one connected component. Count the area of each component. Build a new output grid whose rows are ordered by increasing color value, and in each row draw a horizontal bar of that row’s color whose length equals the component’s area.

**Program solution (Python reference):**
```python
def solve_hard_25_bar_chart_component_areas_by_color(g: Grid) -> Grid:
    comps=components4(g)
    area_by_color={}
    for comp in comps:
        # assume single-color comp
        color=max(comp['colors'], key=lambda k: comp['colors'][k])
        area_by_color[color]=comp['area']
    colors=sorted(area_by_color)
    maxw=max(area_by_color.values())
    out=zeros(len(colors), maxw)
    for r,color in enumerate(colors):
        for c in range(area_by_color[color]):
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0
4 4 4 0
6 6 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 0 0
5 5 5 5 0
7 7 7 7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 0 0 0
4 4 4 4 0
8 8 8 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 3 3 0
6 6 6 0 0
9 9 9 9 9
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 output**
```text
2 2 2 2 0
5 5 5 0 0
8 8 8 8 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 0 0 0
4 4 4 4 4
6 6 6 6 0
```

## Stamp the Unique Bi-Symmetric Component at the Markers (`hard_26_stamp_unique_bisymmetric_component_at_markers`)

**Difficulty:** hard

**Skills:** shape symmetry, component selection, marker-based stamping, recolor by marker

**Scaffold notes:**
- Only one of the color-1 components has both horizontal and vertical symmetry.
- That symmetric component becomes the shared template.
- Each marker colors its own copy.

**Written solution:** Among the color-1 components, find the unique one that is symmetric both horizontally and vertically. Crop that component, then stamp copies of it centered on every marker cell. Recolor each stamped copy to the marker’s color and draw the result on a blank canvas.

**Program solution (Python reference):**
```python
def solve_hard_26_stamp_unique_bisymmetric_component_at_markers(g: Grid) -> Grid:
    h,w=dims(g)
    comps=components4(g, include_colors={1})
    sym=[]
    for comp in comps:
        off=comp['norm_cells']
        if is_h_symmetric(off) and is_v_symmetric(off):
            sym.append(comp)
    assert len(sym)==1
    comp=sym[0]
    base=crop_to_bbox(g, comp['cells'])
    # recolor later
    bh,bw=dims(base)
    assert bh % 2 == 1 and bw % 2 == 1
    out=zeros(h,w)
    markers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in {2,3,4,5}]
    for r,c,color in markers:
        top = r - bh//2
        left = c - bw//2
        piece=recolor_nonzero(base,color)
        paste(out,piece,top,left)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 1 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 3 0 0 0 0 0 2 2 2 0 0
0 0 0 0 3 3 3 0 0 0 0 0 2 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0 1 1 1 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 5 0 0 0
0 0 0 4 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 1 1 0 0 0 0
0 1 1 0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 1 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 4 0 0
0 3 0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 5 5 5 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Mark Local Row–Column Intersections Inside Each Frame (`hard_27_frame_local_intersections_with_fill_key`)

**Difficulty:** hard

**Skills:** multiple local workspaces, row/column gating, frame reasoning, local key color

**Scaffold notes:**
- Process each frame separately.
- Read rows from the left inner border and columns from the top inner border.
- Use the local fill key from the same frame for the new intersection cells.

**Written solution:** Each hollow frame is its own little workspace. Row markers live on the left inner border, column markers live on the top inner border, and the local fill key sits inside the frame. Mark every intersection of a chosen row and a chosen column using that frame’s local fill color, while preserving the frame and the markers.

**Program solution (Python reference):**
```python
def solve_hard_27_frame_local_intersections_with_fill_key(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    # preserve all nonzero input
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[r][c]=g[r][c]
    for comp in components4(g, include_colors={7}):
        if not is_full_rect_border(g, comp['cells'], 7):
            continue
        r0,c0,r1,c1=comp['bbox']
        row_marks=[r for r in range(r0+1,r1) if g[r][c0+1]==2]
        col_marks=[c for c in range(c0+1,c1) if g[r0+1][c]==3]
        key_cells=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in {0,2,3}]
        # one fill key inside
        assert len(key_cells)>=1
        fill=Counter(key_cells).most_common(1)[0][0]
        for r in row_marks:
            for c in col_marks:
                out[r][c]=fill
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 2 3 0 3 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 4 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 3 0 3 0 3 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 6 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 2 4 0 4 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 4 0 4 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 4 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 3 0 3 0 3 7 0
0 0 0 0 0 0 0 0 0 0 7 6 0 6 0 6 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 6 0 6 0 6 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 2 3 0 0 3 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 2 0 0 0 5 7 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0
0 7 3 0 0 3 0 7 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 8 7 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 7 2 5 0 0 5 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 2 5 0 0 5 7 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 2 5 0 0 5 7 0
0 7 7 7 7 7 7 7 0 7 7 7 7 7 7 7 0
0 7 3 0 0 3 0 7 0 0 0 0 0 0 0 0 0
0 7 8 0 0 8 0 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
0 7 8 0 0 8 0 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 8 7 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 7 3 0 3 0 3 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 2 0 0 0 6 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 7 0 3 0 3 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 4 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 7 3 0 3 0 3 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0
0 7 6 0 6 0 6 7 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 7 0 3 0 3 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 2 4 0 4 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 4 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 0 3 3 0 3 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 3 0 3 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 6 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 0 3 3 0 3 7 0
0 0 0 0 0 0 0 0 0 0 7 2 5 5 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 5 5 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 5 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 6 0 6 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 6 0 6 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 6 0 6 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 3 0 0 3 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 8 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 3 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 4 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 7 3 0 0 3 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 8 0 0 8 0 7 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 7 8 0 0 8 8 7 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 2 0 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 4 7 0
0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 3 0 0 3 7 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 0 0 0 5 7 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 7 7 7 7 7 7 7 0
0 7 0 3 0 3 0 7 0 0 0 7 3 0 3 0 3 7 0
0 7 0 0 0 0 0 7 0 0 0 7 2 0 0 0 0 7 0
0 7 2 0 0 0 0 7 0 0 0 7 0 0 0 0 0 7 0
0 7 0 0 0 0 0 7 0 0 0 7 2 0 0 0 0 7 0
0 7 0 0 0 0 8 7 0 0 0 7 0 0 0 0 6 7 0
0 7 7 7 7 7 7 7 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 5 0 0 5 7 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 5 0 0 5 7 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 7 2 5 0 0 5 7 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0 7 7 7 7 7 7 7 0
0 7 0 3 0 3 0 7 0 0 0 7 3 0 3 0 3 7 0
0 7 0 0 0 0 0 7 0 0 0 7 6 0 6 0 6 7 0
0 7 2 8 0 8 0 7 0 0 0 7 0 0 0 0 0 7 0
0 7 0 0 0 0 0 7 0 0 0 7 6 0 6 0 6 7 0
0 7 0 0 0 0 8 7 0 0 0 7 0 0 0 0 6 7 0
0 7 7 7 7 7 7 7 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Select by Marker Count, Then Scale (`hard_28_select_by_marker_count_scale_and_center`)

**Difficulty:** hard

**Skills:** counting markers, ranking components by area, scaling, size-changing output

**Scaffold notes:**
- The markers tell you which area rank to select.
- Rank by cell count, not by reading order.
- After selection, the output is just the scaled crop of that one component.

**Written solution:** Count the blue(9) singleton markers. Sort the color-1 components by increasing area. Select the component whose rank matches the number of markers (1 = smallest, 2 = second-smallest, 3 = third-smallest), then crop it tightly, scale it by 2×, recolor it cyan(8), and output only that scaled crop.

**Program solution (Python reference):**
```python
def solve_hard_28_select_by_marker_count_scale_and_center(g: Grid) -> Grid:
    h,w=dims(g)
    comps=components4(g, include_colors={1})
    comps=sorted(comps, key=lambda comp: (comp['area'], comp['bbox'][0], comp['bbox'][1]))
    n_markers=sum(1 for r in range(h) for c in range(w) if g[r][c]==9)
    idx=n_markers-1
    comp=comps[idx]
    crop=crop_to_bbox(g, comp['cells'])
    # scale 2x and recolor 8
    offsets=offsets_from_grid(crop,{1})
    scaled=scale_offsets(offsets,2)
    out=grid_from_offsets(scaled, 8)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 8
8 8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 0 0
8 8 8 8 0 0
0 0 8 8 8 8
0 0 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
8 8 0 0
8 8 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 1 1 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8 8
8 8 8 8
8 8 8 8
8 8 8 8
```

**Train 5 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 5 output**
```text
8 8
8 8
8 8
8 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 8 8 0 0
0 0 8 8 0 0
8 8 8 8 8 8
8 8 8 8 8 8
0 0 8 8 0 0
0 0 8 8 0 0
```
