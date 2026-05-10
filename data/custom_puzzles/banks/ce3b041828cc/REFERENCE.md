# ARC Puzzle Bank — Fourteenth 21 Puzzles
This fourteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`92`–`98`) so it follows directly after the thirteenth bundle.
This volume shifts the mechanic mix again: interval filling, divider mirroring, rectangle reconstruction from sparse corners, center extraction, key-selected crops, framed row/column matching, diagonal ray casting, chamber filling from legends, dihedral relation matrices, template galleries, border-ray intersections, and transformed-template count maps.
It also introduces a few reusable solver primitives that fit your pipeline well: `horizontal_interval_fill`, `frame_match_cross`, `legend_chamber_fill`, `border_ray_match`, `template_gallery_decode`, and `template_overlay_count`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_fourteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_fourteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_fourteenth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_92_fill_horizontal_intervals` — **Fill the Horizontal Intervals**
- `easy_93_fill_vertical_intervals` — **Fill the Vertical Intervals**
- `easy_94_mirror_left_panel_to_right` — **Mirror the Left Panel to the Right**
- `easy_95_draw_rectangle_borders_from_diagonal_corners` — **Draw Rectangle Borders from Opposite Corners**
- `easy_96_keep_centers_of_odd_rectangles` — **Keep Only the Rectangle Centers**
- `easy_97_mirror_top_panel_to_bottom` — **Mirror the Top Panel to the Bottom**
- `easy_98_stamp_pluses_at_markers` — **Stamp Pluses at the Markers**

### Medium (7)
- `medium_92_crop_component_selected_by_bottom_key` — **Crop the Component Selected by the Bottom Key**
- `medium_93_rotate_object_by_top_code` — **Rotate the Object by the Top Code**
- `medium_94_fill_matching_row_column_intersections` — **Fill Matching Row-Column Intersections**
- `medium_95_cast_diagonal_rays_until_wall` — **Cast Diagonal Rays Until a Wall**
- `medium_96_select_border_touching_object_and_recolor_by_key` — **Select the Border-Touching Object and Recolor It**
- `medium_97_sort_cropped_objects_by_width_and_pack_horizontal` — **Sort Cropped Objects by Width and Pack Them**
- `medium_98_boolean_xor_of_two_halves` — **Take the XOR of the Two Halves**

### Hard (7)
- `hard_92_decode_templates_into_2x2_gallery` — **Decode Templates into a 2×2 Gallery**
- `hard_93_build_dihedral_equivalence_matrix` — **Build the Dihedral-Equivalence Matrix**
- `hard_94_fill_chambers_by_legend_dot_count` — **Fill Chambers by Legend Dot Count**
- `hard_95_select_holed_object_rotate_and_scale2` — **Select the Holed Object, Rotate It, and Scale It 2×**
- `hard_96_build_pairwise_intersection_gallery` — **Build the Pairwise Intersection Gallery**
- `hard_97_cast_border_rays_and_mark_matching_intersections` — **Cast Border Rays and Mark Matching Intersections**
- `hard_98_overlay_transformed_templates_to_count_map` — **Overlay Transformed Templates into a Count Map**

## Fill the Horizontal Intervals (`easy_92_fill_horizontal_intervals`)

**Difficulty:** easy

**Skills:** row-wise segment detection, same-color endpoint matching, same-size transform

**Scaffold notes:**
- Work row by row.
- For each color, find the leftmost and rightmost occurrence in that row.
- Fill the whole interval between those endpoints with that color.

**Written solution:** In each row, cells of the same nonzero color appear as two endpoints. For every color in that row, fill all cells from the leftmost endpoint to the rightmost endpoint, inclusive.

**Program solution (Python reference):**
```python
def solve_easy_92_fill_horizontal_intervals(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        pos=collections.defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append(c)
        for color, cols in pos.items():
            if len(cols) >= 2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 6 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 7 0 0 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 4 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Fill the Vertical Intervals (`easy_93_fill_vertical_intervals`)

**Difficulty:** easy

**Skills:** column-wise span detection, same-color endpoint matching, same-size transform

**Scaffold notes:**
- Work column by column.
- For each color, find the topmost and bottommost occurrence in that column.
- Fill the entire vertical segment between them.

**Written solution:** In each column, two cells of the same nonzero color act as vertical endpoints. For every color in that column, fill all cells between the topmost and bottommost occurrence, inclusive.

**Program solution (Python reference):**
```python
def solve_easy_93_fill_vertical_intervals(g):
    h,w=dims(g)
    out=clone(g)
    for c in range(w):
        pos=collections.defaultdict(list)
        for r in range(h):
            v=g[r][c]
            if v!=0:
                pos[v].append(r)
        for color, rows in pos.items():
            if len(rows) >= 2:
                for r in range(min(rows), max(rows)+1):
                    out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
3 2 0 0 0 0 0 0 0 0
3 2 0 4 0 0 0 0 0 0
3 2 0 4 0 0 0 0 0 0
3 0 0 4 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
```

**Train 2 output**
```text
0 0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0 2
0 0 6 0 0 8 0 0 2
0 0 6 0 0 8 0 0 2
0 0 6 0 0 8 0 0 2
0 0 6 0 0 8 0 0 0
0 0 6 0 0 8 0 0 0
0 0 6 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 4 0
7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 4 0
7 0 0 0 0 0 0 0 0 4 0
7 0 0 0 3 0 0 0 0 4 0
7 0 0 0 3 0 0 0 0 4 0
7 0 0 0 3 0 0 0 0 4 0
7 0 0 0 3 0 0 0 0 4 0
7 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 9 0 0 0 0 2 0 0 0
0 9 0 0 0 0 2 0 3 0
0 9 0 0 0 0 2 0 3 0
0 9 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 2 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
```

**Test output**
```text
0 0 0 0 0 2 0 0 0 0 0 0
0 0 4 0 0 2 0 0 0 0 0 0
0 0 4 0 0 2 0 0 0 0 0 0
0 0 4 0 0 2 0 0 0 0 6 0
0 0 4 0 0 2 0 0 0 0 6 0
0 0 4 0 0 2 0 0 0 0 6 0
0 0 4 0 0 2 0 0 0 0 6 0
0 0 4 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
```

## Mirror the Left Panel to the Right (`easy_94_mirror_left_panel_to_right`)

**Difficulty:** easy

**Skills:** panel parsing, reflection across divider, same-size transform

**Scaffold notes:**
- Find the solid vertical divider.
- Read the colored pattern on the left side only.
- Copy it to the right by horizontal reflection across the divider.

**Written solution:** The middle column is a divider. Everything on the left side should be copied to the right side as a mirror image, while the divider and the original left-side pattern stay unchanged.

**Program solution (Python reference):**
```python
def solve_easy_94_mirror_left_panel_to_right(g):
    h,w=dims(g)
    divider=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            divider=c; break
    assert divider is not None
    out=clone(g)
    for r in range(h):
        for c in range(divider):
            if g[r][c] != 0:
                out[r][2*divider - c] = g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0 0
0 0 0 4 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
6 0 0 0 0 5 0 0 0 0 0
0 0 3 0 0 5 0 0 0 0 0
0 0 0 0 8 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 2 0
0 0 0 4 0 5 0 4 0 0 0
0 0 0 0 0 5 0 0 0 0 0
6 0 0 0 0 5 0 0 0 0 6
0 0 3 0 0 5 0 0 3 0 0
0 0 0 0 8 5 8 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 input**
```text
7 0 0 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 4 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 6 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 2 output**
```text
7 0 0 0 5 0 0 0 7
0 0 2 0 5 0 2 0 0
0 0 0 0 5 0 0 0 0
0 4 0 0 5 0 0 4 0
0 0 0 0 5 0 0 0 0
0 0 0 6 5 6 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 3 5 0 0 0 0 0
0 0 8 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
4 0 0 0 0 5 0 0 0 0 0
0 0 0 6 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 3 5 3 0 0 0 0
0 0 8 0 0 5 0 0 8 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 2 0
0 0 0 0 0 5 0 0 0 0 0
4 0 0 0 0 5 0 0 0 0 4
0 0 0 6 0 5 0 6 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 4 input**
```text
0 2 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 7 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 3 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
8 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 4 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Train 4 output**
```text
0 2 0 0 0 0 5 0 0 0 0 2 0
0 0 0 0 7 0 5 0 7 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 3 0 0 0 5 0 0 0 3 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
8 0 0 0 0 0 5 0 0 0 0 0 8
0 0 0 0 0 4 5 4 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 5 0 0 0 0 0
3 0 0 0 0 5 0 0 0 0 0
0 0 7 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 2 5 0 0 0 0 0
0 8 0 0 0 5 0 0 0 0 0
0 0 0 4 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 5 0 0 0 0 0
3 0 0 0 0 5 0 0 0 0 3
0 0 7 0 0 5 0 0 7 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 2 5 2 0 0 0 0
0 8 0 0 0 5 0 0 0 8 0
0 0 0 4 0 5 0 4 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

## Draw Rectangle Borders from Opposite Corners (`easy_95_draw_rectangle_borders_from_diagonal_corners`)

**Difficulty:** easy

**Skills:** bbox from sparse cues, rectangle border drawing, same-size transform

**Scaffold notes:**
- For each color, locate its two given corner cells.
- Use those two cells as opposite corners of an axis-aligned rectangle.
- Draw the full border of that rectangle in the same color.

**Written solution:** Each color appears twice, marking two opposite corners of a rectangle. For every color, draw the entire axis-aligned rectangle border connecting those corners.

**Program solution (Python reference):**
```python
def solve_easy_95_draw_rectangle_borders_from_diagonal_corners(g):
    h,w=dims(g)
    out=zeros(h,w)
    pos=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)>=2:
            r0=min(r for r,c in cells); r1=max(r for r,c in cells)
            c0=min(c for r,c in cells); c1=max(c for r,c in cells)
            draw_rect_border(out,r0,c0,r1,c1,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0
0 2 0 0 0 2 0 4 4 4 0
0 2 0 0 0 2 0 4 0 4 0
0 2 2 2 2 2 0 4 0 4 0
0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 3 3 3 3 3 3 0 0 0
0 0 3 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 3 0 0 0
0 0 3 3 3 3 3 3 3 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
6 0 0 6 0 2 2 2 2 0
6 0 0 6 0 2 0 0 2 0
6 0 0 6 0 2 0 0 2 0
6 0 0 6 0 2 2 2 2 0
6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 4 4 4 4 4 4 4 4 4 0 8
0 0 4 0 0 0 0 0 0 8 4 8 8
0 0 4 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 4 0 0
0 0 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 6 6 0 0 0 0 0 0 0 0 0
6 0 6 2 2 2 2 2 2 2 0 0
6 0 6 2 0 0 0 0 0 2 0 0
6 0 6 2 0 0 0 0 0 2 0 0
6 6 6 2 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0 2 0 0
0 0 0 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Keep Only the Rectangle Centers (`easy_96_keep_centers_of_odd_rectangles`)

**Difficulty:** easy

**Skills:** connected components, odd rectangle centers, same-size transform

**Scaffold notes:**
- Each object is a filled rectangle with odd height and odd width.
- Compute the center cell of each rectangle's bounding box.
- Keep only that single center cell in the object's color.

**Written solution:** Every colored object is a solid rectangle with odd dimensions. Replace each rectangle by just its center cell, keeping the same color.

**Program solution (Python reference):**
```python
def solve_easy_96_keep_centers_of_odd_rectangles(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        rr=(r0+r1)//2
        cc=(c0+c1)//2
        out[rr][cc]=comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 6 6 6 0
7 7 7 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 2 2 2 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Mirror the Top Panel to the Bottom (`easy_97_mirror_top_panel_to_bottom`)

**Difficulty:** easy

**Skills:** panel parsing, reflection across horizontal divider, same-size transform

**Scaffold notes:**
- Find the solid horizontal divider.
- Read the colored pattern in the top half only.
- Copy it downward by vertical reflection across the divider.

**Written solution:** The middle row is a divider. Everything above it should be copied below it as a mirror image across that divider, while the divider and the original top pattern stay unchanged.

**Program solution (Python reference):**
```python
def solve_easy_97_mirror_top_panel_to_bottom(g):
    h,w=dims(g)
    divider=None
    for r in range(h):
        if all(v==5 for v in g[r]):
            divider=r; break
    assert divider is not None
    out=clone(g)
    for r in range(divider):
        for c in range(w):
            if g[r][c] != 0:
                out[2*divider-r][c] = g[r][c]
    return out
```

**Train 1 input**
```text
0 2 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 3 0
8 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 3 0
8 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 6 0 0 0 0
0 2 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 4 0
0 0 7 0 0 0 0 0
0 0 0 0 0 2 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 4 0
0 0 7 0 0 0 0 0
0 0 0 0 0 2 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 4 0
```

**Train 3 input**
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
6 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 7 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 7 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
5 5 5 5 5 5 5 5 5
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 2 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
```

**Test input**
```text
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 7 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 7 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 4 0 0 0 0 0 0 0 0
```

## Stamp Pluses at the Markers (`easy_98_stamp_pluses_at_markers`)

**Difficulty:** easy

**Skills:** local stamping, orthogonal neighborhoods, same-size transform

**Scaffold notes:**
- Treat each nonzero cell as the center of a plus.
- The plus contains the center plus its four orthogonal neighbors.
- Use the marker's own color for all cells of that plus.

**Written solution:** Every nonzero cell is a marker. Replace each marker by a 3-cell-wide plus consisting of the center cell and its up, down, left, and right neighbors in the same color.

**Program solution (Python reference):**
```python
def solve_easy_98_stamp_pluses_at_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 8 0 4 0 0 0
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 3 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 7 0 0 0
0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 7 0 2 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 2 0 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 0 0 0
0 6 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
0 6 0 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 7 0 0 0
0 0 4 0 0 0 0 7 7 7 0 0
0 0 0 0 0 2 0 0 7 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Crop the Component Selected by the Bottom Key (`medium_92_crop_component_selected_by_bottom_key`)

**Difficulty:** medium

**Skills:** key lookup, component extraction, bbox crop

**Scaffold notes:**
- Read the single nonzero key cell on the bottom row.
- Find the object above whose color matches that key.
- Output the tight crop of that matching component.

**Written solution:** The bottom row contains a single key color. Among the objects above it, find the component with that color and output just its tight bounding-box crop.

**Program solution (Python reference):**
```python
def solve_medium_92_crop_component_selected_by_bottom_key(g):
    h,w=dims(g)
    key = next(v for v in g[h-1] if v != 0)
    comps = [comp for comp in connected_components(g[:-1]) if comp["color"] == key]
    comp = comps[0]
    return crop_bbox(g[:-1], comp["bbox"])
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0 4 0 0
0 2 0 0 0 0 0 4 0 4 0 0
0 2 2 2 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
```

**Train 1 output**
```text
4 0 4
4 0 4
4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 2 0 0 0 0 0 0 7 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7 0
0 7 7
0 0 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 8 0 0 0
0 4 4 4 0 0 0 8 0 0 0
0 4 0 4 0 0 0 0 0 0 0
0 4 4 4 0 6 6 6 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
```

**Train 3 output**
```text
6 6 6
6 0 0
6 6 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 2 0 2 0 0 0 0 0 4 4 4 0
0 0 2 0 2 0 0 0 0 0 0 0 4 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
```

**Train 4 output**
```text
2 0 2
2 0 2
2 2 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 4 4 4 6 6 6 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0
```

**Test output**
```text
6 6 6
6 0 6
6 6 6
```

## Rotate the Object by the Top Code (`medium_93_rotate_object_by_top_code`)

**Difficulty:** medium

**Skills:** code reading, cropping, rotation

**Scaffold notes:**
- The single nonzero cell on the top row is a rotation code.
- Crop the one object below to its tight bounding box.
- Apply the coded rotation to that cropped object.

**Written solution:** Read the single rotation code from the top row: 1 = no rotation, 2 = clockwise, 3 = 180°, 4 = counterclockwise. Crop the object below and apply that rotation.

**Program solution (Python reference):**
```python
def solve_medium_93_rotate_object_by_top_code(g):
    code = next(v for v in g[0] if v != 0)
    obj = crop_nonzero(g[1:])
    return apply_transform(obj, code)
```

**Train 1 input**
```text
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2
2 0 0
2 0 0
```

**Train 2 input**
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 4
0 0 4
4 4 4
```

**Train 3 input**
```text
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 7 7
0 7 0
7 7 0
7 0 0
```

**Train 4 input**
```text
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 6
6 6
6 6
```

**Test input**
```text
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 3 3
3 3 0
3 0 0
```

## Fill Matching Row-Column Intersections (`medium_94_fill_matching_row_column_intersections`)

**Difficulty:** medium

**Skills:** frame parsing, cross-product reasoning, color matching

**Scaffold notes:**
- The frame stays fixed.
- Read row keys from the left interior column and column keys from the top interior row.
- Inside the frame, color only the intersections where the row key and column key are the same.

**Written solution:** Inside the framed area, the left interior column labels rows and the top interior row labels columns. Fill an interior cell exactly when its row label and column label match, using that shared color.

**Program solution (Python reference):**
```python
def solve_medium_94_fill_matching_row_column_intersections(g):
    h,w=dims(g)
    out=clone(g)
    # assume outer frame 5 at border, row markers on row1, col markers on col1
    row_colors = {r:g[r][1] for r in range(2,h-1) if g[r][1] not in (0,5)}
    col_colors = {c:g[1][c] for c in range(2,w-1) if g[1][c] not in (0,5)}
    for r,color_r in row_colors.items():
        for c,color_c in col_colors.items():
            if color_r == color_c:
                out[r][c] = color_r
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5
5 0 4 2 0 7 2 4 5
5 2 0 0 0 0 0 0 5
5 4 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 2 0 0 0 0 0 0 5
5 7 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5
5 0 4 2 0 7 2 4 5
5 2 0 2 0 0 2 0 5
5 4 4 0 0 0 0 4 5
5 0 0 0 0 0 0 0 5
5 2 0 2 0 0 2 0 5
5 7 0 0 0 7 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5 5 5
5 0 6 0 3 8 0 3 6 5
5 3 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 5
5 6 0 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 0 5
5 3 0 0 0 0 0 0 0 5
5 8 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5 5 5
5 0 6 0 3 8 0 3 6 5
5 3 0 0 3 0 0 3 0 5
5 0 0 0 0 0 0 0 0 5
5 6 6 0 0 0 0 0 6 5
5 0 0 0 0 0 0 0 0 5
5 3 0 0 3 0 0 3 0 5
5 8 0 0 0 8 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5
5 0 2 7 0 7 2 5
5 7 0 0 0 0 0 5
5 0 0 0 0 0 0 5
5 2 0 0 0 0 0 5
5 7 0 0 0 0 0 5
5 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5
5 0 2 7 0 7 2 5
5 7 0 7 0 7 0 5
5 0 0 0 0 0 0 5
5 2 2 0 0 0 2 5
5 7 0 7 0 7 0 5
5 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
5 5 5 5 5 5 5 5 5
5 0 8 0 4 6 0 4 5
5 4 0 0 0 0 0 0 5
5 8 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 4 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 6 0 0 0 0 0 0 5
5 8 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
5 5 5 5 5 5 5 5 5
5 0 8 0 4 6 0 4 5
5 4 0 0 4 0 0 4 5
5 8 8 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 4 0 0 4 0 0 4 5
5 0 0 0 0 0 0 0 5
5 6 0 0 0 6 0 0 5
5 8 8 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Test input**
```text
5 5 5 5 5 5 5 5 5
5 0 4 2 0 6 2 0 5
5 2 0 0 0 0 0 0 5
5 6 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 4 0 0 0 0 0 0 5
5 2 0 0 0 0 0 0 5
5 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5
```

**Test output**
```text
5 5 5 5 5 5 5 5 5
5 0 4 2 0 6 2 0 5
5 2 0 2 0 0 2 0 5
5 6 0 0 0 6 0 0 5
5 0 0 0 0 0 0 0 5
5 4 4 0 0 0 0 0 5
5 2 0 2 0 0 2 0 5
5 0 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5
```

## Cast Diagonal Rays Until a Wall (`medium_95_cast_diagonal_rays_until_wall`)

**Difficulty:** medium

**Skills:** diagonal ray casting, blockers, same-size transform

**Scaffold notes:**
- Treat each non-wall, nonzero singleton as an emitter.
- From each emitter, cast diagonal rays in all four diagonal directions.
- Stop a ray when it reaches a nonzero blocker or the grid boundary.

**Written solution:** Every nonzero cell that is not a wall emits diagonal rays. Copy the emitter's color along each diagonal direction through empty cells, stopping before any wall or other nonzero blocker.

**Program solution (Python reference):**
```python
def solve_medium_95_cast_diagonal_rays_until_wall(g):
    h,w=dims(g)
    out=clone(g)
    # walls are 5, emitters are nonzero !=5
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=5:
                for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                    nr,nc=r+dr,c+dc
                    while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:
                        out[nr][nc]=v
                        nr += dr; nc += dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 2 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 2 0 0 4 0 0 5 5 5 0
0 4 2 4 0 0 0 0 2 0 0
0 0 4 2 0 0 0 2 5 0 0
0 4 0 4 2 0 2 0 5 0 0
4 0 0 0 4 2 0 0 5 0 0
0 0 0 0 2 4 2 0 5 0 0
0 0 0 2 0 0 4 2 0 0 0
0 0 2 0 0 0 0 4 2 0 0
0 2 0 0 0 0 0 0 4 2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 6 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 6 0 0 0 6
0 0 0 5 0 0 6 0 6 3
0 0 0 5 0 0 0 6 3 0
0 0 0 5 0 0 6 3 6 0
0 0 0 5 3 6 3 0 0 6
0 0 0 0 6 3 0 0 0 0
0 0 0 6 3 0 3 0 0 0
0 0 6 3 5 5 5 5 5 0
0 6 3 0 0 0 0 0 0 0
6 3 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 4 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 4 0 0 0 0 8 0 0 0 0 0
0 8 4 0 0 8 0 0 0 0 0 0
0 0 8 4 8 0 0 0 0 0 0 0
0 0 0 8 4 0 0 0 0 0 0 0
0 0 8 0 8 4 0 0 0 0 0 0
0 5 5 5 5 8 4 0 0 0 0 0
0 0 0 0 0 0 8 4 0 5 0 0
0 0 0 0 0 0 0 8 4 5 0 0
0 0 0 0 0 0 0 4 8 5 0 0
0 0 0 0 0 0 4 0 0 5 0 0
0 0 0 0 0 4 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 5 0 2 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 5 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 0 0 0 7 0 7 2
0 2 0 0 0 0 7 2 0
0 0 2 0 0 7 2 7 0
0 0 5 2 7 2 0 0 7
0 0 5 7 2 0 0 0 0
0 0 5 2 0 2 0 0 0
0 0 5 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 2 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 6 2 0 0 0 0 6 0 0 0
0 0 6 2 0 0 6 0 0 0 0
0 0 0 6 2 6 0 5 5 5 0
0 0 0 0 6 2 0 0 0 0 0
0 0 0 6 0 6 2 0 0 0 2
0 0 6 0 0 5 6 2 0 2 0
0 6 0 0 0 5 0 6 2 0 0
6 0 0 0 0 5 0 2 6 2 0
0 0 0 0 0 5 2 0 0 6 2
0 0 0 0 0 2 0 0 0 0 6
```

## Select the Border-Touching Object and Recolor It (`medium_96_select_border_touching_object_and_recolor_by_key`)

**Difficulty:** medium

**Skills:** object selection by property, key-based recoloring, size-changing output

**Scaffold notes:**
- Read the new target color from the top row.
- Among the objects below, find the only component that touches the border of the lower panel.
- Output that object alone, recolored to the key color.

**Written solution:** The top row gives the replacement color. In the lower panel, select the unique object that touches the panel border; remove everything else and recolor that selected object to the key color.

**Program solution (Python reference):**
```python
def solve_medium_96_select_border_touching_object_and_recolor_by_key(g):
    h,w=dims(g)
    # key is singleton color 9? no, any nonzero cell in top-right corner row or bottom row outside objects. We'll define it as first nonzero in row0.
    key = next(v for v in g[0] if v != 0)
    comps = connected_components(g[1:])  # objects below top row
    # adjust bbox not needed, crop shapes from g[1:]
    out = zeros(h-1,w)
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        if r0==0 or c0==0 or r1==h-2 or c1==w-1:
            for r,c in comp["cells"]:
                out[r][c]=key
            break
    return out
```

**Train 1 input**
```text
0 0 0 0 0 8 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 4 0 4 0 0 0
0 0 0 0 0 4 0 6 6 6 0
0 0 0 0 0 4 4 4 6 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 4 0 4 0 0 0 0
0 0 2 0 0 4 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
8 0 0 0 3 2 2 2 0 0
8 0 0 0 0 2 0 2 0 0
8 8 8 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 6 6 0 0 0 0 0
0 0 2 2 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 2 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 4 4 4 0 0
0 0 0 0 6 6 6 4 0 4 0 0
0 0 0 0 6 0 0 4 4 4 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Sort Cropped Objects by Width and Pack Them (`medium_97_sort_cropped_objects_by_width_and_pack_horizontal`)

**Difficulty:** medium

**Skills:** component cropping, ordering by width, horizontal packing

**Scaffold notes:**
- Extract each object and crop it tightly.
- Measure each cropped object's width.
- Sort from narrowest to widest and pack them left-to-right with a one-cell gap.

**Written solution:** Take every connected component, crop it to its bounding box, order the crops by width from smallest to largest, and pack them horizontally with a single blank column between them.

**Program solution (Python reference):**
```python
def solve_medium_97_sort_cropped_objects_by_width_and_pack_horizontal(g):
    comps = connected_components(g)
    crops = [crop_bbox(g, comp["bbox"]) for comp in comps]
    crops = sorted(crops, key=lambda cg: (len(cg[0]), len(cg), min(v for row in cg for v in row if v!=0)))
    return hstack(crops, gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 0 0 0 0 0
0 2 2 2 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 0 2 0 0 0 4 4 0 0
6 6 0 2 0 0 0 0 4 4 4
6 0 0 2 2 2 0 0 0 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 8 0 0 0 2 0 0
0 0 0 0 0 0 8 8 8 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 0 8 0 8 0 0 0 2
0 3 0 0 8 0 8 0 0 2 2
0 3 0 0 8 8 8 0 0 2 0
0 0 0 0 0 0 0 0 2 2 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 6 6 6 0 0 0 0 0
0 4 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 0 4 4 4 0 6 6 6
7 7 0 4 0 0 0 6 0 0
7 0 0 4 0 0 0 6 6 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 6 6 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 2 0 4 4 4 0 6 6 0 0
2 0 2 0 0 4 0 0 0 6 6 6
2 2 2 0 0 4 0 0 0 0 0 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 2 0 0
0 0 0 0 0 7 0 7 0 0 2 2 0 0
0 0 0 0 0 7 7 7 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
3 3 3 0 7 0 7 0 0 0 2
3 0 0 0 7 0 7 0 0 2 2
3 3 0 0 7 7 7 0 0 2 0
0 0 0 0 0 0 0 0 2 2 0
```

## Take the XOR of the Two Halves (`medium_98_boolean_xor_of_two_halves`)

**Difficulty:** medium

**Skills:** panel parsing, boolean comparison, shape arithmetic

**Scaffold notes:**
- Split the input at the vertical divider.
- Treat nonzero cells in each half as binary masks.
- Output a mask where exactly one side has a filled cell.

**Written solution:** The left and right panels are two binary shapes separated by a divider. Produce a single-panel output colored 8 exactly where one shape is filled and the other is empty.

**Program solution (Python reference):**
```python
def solve_medium_98_boolean_xor_of_two_halves(g):
    h,w=dims(g)
    divider=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            divider=c; break
    left=[row[:divider] for row in g]
    right=[row[divider+1:] for row in g]
    assert len(left[0]) == len(right[0])
    H,W=dims(left)
    out=zeros(H,W)
    for r in range(H):
        for c in range(W):
            a = left[r][c]!=0
            b = right[r][c]!=0
            if a ^ b:
                out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 3 3 3 0
0 2 0 0 0 5 0 0 3 0 0
0 2 2 2 0 5 0 0 3 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0
0 0 8 8 0
0 8 8 0 0
0 8 0 8 0
0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 4 4 4 0 5 0 6 0 6 0
0 0 4 4 0 5 0 6 0 6 0
0 0 0 0 0 5 0 6 6 6 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0
0 0 8 0 0
0 8 8 0 0
0 8 8 8 0
0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 7 7 7 0 5 0 2 2 2 0
0 7 0 0 0 5 0 0 0 2 0
0 7 7 0 0 5 0 0 0 2 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0
0 0 0 0 0
0 8 0 8 0
0 8 8 8 0
0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 2 2 2 0 5 0 0 0 0 0
0 2 0 2 0 5 0 4 4 0 0
0 2 2 2 0 5 0 4 4 4 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0
0 8 8 8 0
0 0 8 8 0
0 0 0 0 0
0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 3 0 5 0 2 2 2 0
0 3 3 3 0 5 0 2 0 2 0
0 0 0 3 0 5 0 2 2 2 0
0 0 0 0 0 5 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0
0 8 8 0 0
0 0 8 0 0
0 8 8 0 0
0 0 0 0 0
```

## Decode Templates into a 2×2 Gallery (`hard_92_decode_templates_into_2x2_gallery`)

**Difficulty:** hard

**Skills:** library lookup, code decoding, rotation, gallery assembly

**Scaffold notes:**
- Read the four template panels across the top and identify each by its color.
- On the code row, read four consecutive (template-color, transform-code) pairs.
- Transform the chosen templates and place them into a 2×2 gallery in row-major order.

**Written solution:** The top band is a template library. Each pair on the bottom code row selects one template by color and tells how to rotate it (1 none, 2 clockwise, 3 180°, 4 counterclockwise). Decode the four pairs and place the transformed templates into a 2×2 gallery.

**Program solution (Python reference):**
```python
def solve_hard_92_decode_templates_into_2x2_gallery(g):
    # top 5 rows: 4 panels of width 5 separated by 1
    library={}
    top = g[:5]
    for i in range(4):
        x=i*6
        panel=[row[x:x+5] for row in top]
        cropped=crop_nonzero(panel)
        color=next(v for row in cropped for v in row if v!=0)
        library[color]=cropped
    code_row = g[6]
    pairs=[]
    i=0
    while i+1 < len(code_row):
        if code_row[i]==0:
            break
        pairs.append((code_row[i], code_row[i+1]))
        i+=2
    items=[apply_transform(library[color], code) for color,code in pairs[:4]]
    # arrange 2x2 with gap 1
    row1 = hstack(items[:2], gap=1, bg=0)
    row2 = hstack(items[2:4], gap=1, bg=0)
    return vstack([row1,row2], gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 6 0 6 0 0 0 8 8 8 0
0 2 0 0 0 0 0 0 4 0 0 0 0 6 0 6 0 0 0 8 0 0 0
0 2 2 2 0 0 0 0 4 0 0 0 0 6 6 6 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 1 6 2 4 3 8 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 6 6 6
2 0 0 0 6 0 0
2 2 2 0 6 6 6
0 0 0 0 0 0 0
0 4 0 0 8 0 0
0 4 0 0 8 0 8
4 4 4 0 8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 7 7 0 0 0 0 0 2 2 2 0 0 0 4 0 0 0
0 3 3 0 0 0 0 7 7 7 0 0 0 2 0 2 0 0 0 4 0 0 0
0 3 0 0 0 0 0 0 0 7 0 0 0 2 2 2 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 4 3 2 4 1 2 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 7 7 0 0 0 0
0 7 0 0 3 3 3
7 7 0 0 0 3 3
7 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 2 2 2
4 0 0 0 2 0 2
4 4 4 0 2 2 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 2 2 2 0 0 0 8 8 8 0 0 0 4 4 0 0
0 6 0 6 0 0 0 2 0 0 0 0 0 0 8 0 0 0 0 4 4 0 0
0 6 6 6 0 0 0 2 2 0 0 0 0 0 8 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 2 6 3 2 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8 0 6 6 6
8 8 8 0 6 0 6
0 0 8 0 6 0 6
0 0 0 0 0 0 0
2 0 0 0 4 4 0
2 0 2 0 4 4 0
2 2 2 0 4 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 3 0 0 0 0 6 6 0 0 0 0 0 2 2 2 0
0 7 0 7 0 0 0 3 0 0 0 0 0 6 6 6 0 0 0 0 2 0 0
0 7 7 7 0 0 0 3 3 3 0 0 0 0 0 6 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 7 1 2 2 6 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 3 0 7 7 7
0 0 3 0 7 0 7
0 0 3 0 7 7 7
0 0 0 0 0 0 0
0 0 2 0 0 6 6
2 2 2 0 0 6 0
0 0 2 0 6 6 0
0 0 0 0 6 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 2 0 2 0 0 0 7 7 0 0 0 6 6 0 0 0
0 4 0 0 0 0 0 2 0 2 0 0 0 7 7 0 0 0 0 6 6 6 0
0 4 4 0 0 0 0 2 2 2 0 0 0 7 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 4 7 2 6 1 4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 2 0 7 7 7 0
0 0 2 0 0 7 7 0
2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0
6 6 0 0 0 0 4 4
0 6 6 6 0 0 0 4
0 0 0 6 0 4 4 4
```

## Build the Dihedral-Equivalence Matrix (`hard_93_build_dihedral_equivalence_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, rotation/reflection reasoning, matrix construction

**Scaffold notes:**
- Crop each of the four panels to its shape.
- Compare every pair up to rotation first, then up to full dihedral symmetry.
- Write 8 on the diagonal, 2 for rotation-equivalent pairs, 6 for reflection-only pairs, and 0 otherwise.

**Written solution:** Across the input are four shapes. Produce a 4×4 matrix: diagonal cells are 8; if two shapes match by rotation, write 2; if they match only after a reflection, write 6; otherwise write 0.

**Program solution (Python reference):**
```python
def solve_hard_93_build_dihedral_equivalence_matrix(g):
    # four 5x5 panels side by side gap1
    panels=[]
    for i in range(4):
        x=i*6
        panel=[row[x:x+5] for row in g]
        panels.append(crop_nonzero(panel))
    rot_sets=[rotations(p) for p in panels]
    dih_sets=[dihedral(p) for p in panels]
    n=4
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=8
            elif normalize_shape(panels[j]) in rot_sets[i]:
                out[i][j]=2
            elif normalize_shape(panels[j]) in dih_sets[i]:
                out[i][j]=6
            else:
                out[i][j]=0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 4 4 4 0 0 0 6 6 6 0 0 0 8 8 8 0
0 2 0 0 0 0 0 4 0 4 0 0 0 0 0 6 0 0 0 0 8 0 0
0 2 2 0 0 0 0 0 0 4 0 0 0 0 6 6 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 6 0
2 8 6 0
6 6 8 0
0 0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 6 6 6 0 0 0 8 0 8 0
0 2 0 0 0 0 0 0 0 4 0 0 0 0 0 6 0 0 0 8 0 8 0
0 2 2 2 0 0 0 0 0 4 0 0 0 0 6 6 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 2 0 0
2 8 0 0
0 0 8 0
0 0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 7 7 7 0 0 0 2 2 2 0 0 0 6 0 0 0
0 3 0 0 0 0 0 0 0 7 0 0 0 2 0 0 0 0 0 6 0 0 0
0 3 3 0 0 0 0 0 7 7 0 0 0 2 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 6 0 0
6 8 0 0
0 0 8 2
0 0 2 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 2 2 2 0 0 0 6 6 6 0 0 0 0 0 8 0
0 0 4 0 0 0 0 2 0 0 0 0 0 0 0 6 0 0 0 8 8 8 0
0 0 4 0 0 0 0 2 2 0 0 0 0 0 6 6 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0 2
0 8 6 0
0 6 8 0
2 0 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 4 4 4 0 0 0 7 7 7 0 0 0 6 0 6 0
0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 7 0 0 0 6 0 6 0
0 2 2 0 0 0 0 4 4 0 0 0 0 0 7 7 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 2 6 0
2 8 6 0
6 6 8 0
0 0 0 8
```

## Fill Chambers by Legend Dot Count (`hard_94_fill_chambers_by_legend_dot_count`)

**Difficulty:** hard

**Skills:** legend parsing, region flood-fill, count-based recoloring

**Scaffold notes:**
- The top row lists the colors for chambers containing 1, 2, and 3 dots.
- Below the blank row, walls partition the grid into chambers.
- Count the dots in each chamber and fill the entire chamber with the matching legend color.

**Written solution:** The top row is a legend: its first, second, and third colors correspond to chambers containing 1, 2, and 3 dots. In the chamber map below, count the dots in each region and flood-fill the whole chamber with the legend color for that count, keeping the walls unchanged.

**Program solution (Python reference):**
```python
def solve_hard_94_fill_chambers_by_legend_dot_count(g):
    legend=[v for v in g[0] if v!=0]
    sub=clone(g[2:])
    h,w=dims(sub)
    out=clone(sub)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if sub[r][c] != 5 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                cells=[]
                dot_count=0
                while q:
                    rr,cc=q.popleft()
                    cells.append((rr,cc))
                    if sub[rr][cc]==1:
                        dot_count += 1
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and sub[nr][nc] != 5 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                color=legend[dot_count-1]
                for rr,cc in cells:
                    out[rr][cc]=color
    full=clone(g)
    for r in range(h):
        full[r+2]=out[r]
    return full
```

**Train 1 input**
```text
2 4 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 1 0 0 5 0 1 1 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 5 0 0 0 0 0 0 0 5 5
5 5 0 1 1 1 0 0 0 5 5
5 5 0 0 0 0 0 0 0 5 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
2 4 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 2 2 2 2 5 4 4 4 4 5
5 2 2 2 2 5 4 4 4 4 5
5 2 2 2 2 5 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5 5
5 5 6 6 6 6 6 6 6 5 5
5 5 6 6 6 6 6 6 6 5 5
5 5 6 6 6 6 6 6 6 5 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
3 7 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 5 0 0 0 0 5
5 0 1 1 0 5 5 0 1 0 0 5
5 0 0 0 0 5 5 0 0 0 0 5
5 0 0 0 0 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5
5 5 0 0 0 0 5 0 0 0 0 5
5 5 0 1 1 0 5 0 1 1 0 5
5 5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
3 7 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 5 3 3 3 3 5
5 7 7 7 7 5 5 3 3 3 3 5
5 7 7 7 7 5 5 3 3 3 3 5
5 7 7 7 7 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5
5 5 7 7 7 7 5 7 7 7 7 5
5 5 7 7 7 7 5 7 7 7 7 5
5 5 7 7 7 7 5 7 7 7 7 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
4 2 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 0 5
5 0 1 0 5 0 1 1 0 5
5 0 0 0 5 0 1 0 0 5
5 5 5 5 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 5
5 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
4 2 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
5 4 4 4 5 6 6 6 6 5
5 4 4 4 5 6 6 6 6 5
5 4 4 4 5 6 6 6 6 5
5 5 5 5 5 6 6 6 6 5
5 5 5 5 5 5 5 5 5 5
5 6 6 6 6 5 6 6 6 5
5 6 6 6 6 5 6 6 6 5
5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
8 3 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 0 5 0 0 0 5
5 0 1 1 0 0 5 0 1 0 5
5 0 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 1 1 0 5 0 1 1 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
8 3 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 3 3 3 3 3 5 8 8 8 5
5 3 3 3 3 3 5 8 8 8 5
5 3 3 3 3 3 5 8 8 8 5
5 5 5 5 5 5 5 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5
5 3 3 3 3 5 3 3 3 3 5
5 3 3 3 3 5 3 3 3 3 5
5 3 3 3 3 5 3 3 3 3 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test input**
```text
2 6 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 5 0 0 0 0 5
5 0 1 1 0 5 5 0 1 0 0 5
5 0 0 0 0 5 5 0 0 0 0 5
5 5 5 5 5 5 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
5 5 0 0 0 0 5 0 0 0 0 5
5 5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Test output**
```text
2 6 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 6 6 6 6 5 5 2 2 2 2 5
5 6 6 6 6 5 5 2 2 2 2 5
5 6 6 6 6 5 5 2 2 2 2 5
5 5 5 5 5 5 5 2 2 2 2 5
5 5 5 5 5 5 5 5 5 5 5 5
5 5 8 8 8 8 5 8 8 8 8 5
5 5 8 8 8 8 5 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5 5
```

## Select the Holed Object, Rotate It, and Scale It 2× (`hard_95_select_holed_object_rotate_and_scale2`)

**Difficulty:** hard

**Skills:** hole counting, object selection, rotation and scaling

**Scaffold notes:**
- Read the rotation code from the top row.
- Among the lower objects, find the unique component that contains a hole.
- Crop it, apply the coded rotation, and scale the result by 2 in both dimensions.

**Written solution:** The top row gives a rotation code (1 none, 2 clockwise, 3 180°, 4 counterclockwise). Among the objects below, choose the only holed object, crop it tightly, rotate it by the code, and then scale it 2×.

**Program solution (Python reference):**
```python
def solve_hard_95_select_holed_object_rotate_and_scale2(g):
    code = next(v for v in g[0] if v!=0)
    comps=connected_components(g[1:])
    selected=None
    base=g[1:]
    for comp in comps:
        crop=crop_bbox(base, comp["bbox"])
        if count_holes_binary(crop)==1:
            selected=crop
            break
    assert selected is not None
    return scale2(apply_transform(selected, code))
```

**Train 1 input**
```text
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 2 0 0 0
0 0 4 0 4 0 0 0 2 0 0 0
0 0 4 4 4 0 0 0 2 2 2 0
0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 4 4 4 4
4 4 4 4 4 4
4 4 0 0 4 4
4 4 0 0 4 4
4 4 4 4 4 4
4 4 4 4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 3 3 3 0 0
0 7 0 0 7 0 0 0 3 0 0 0 0
0 7 0 0 7 0 0 0 3 3 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 0 0 0 0 7 7
7 7 0 0 0 0 7 7
7 7 0 0 0 0 7 7
7 7 0 0 0 0 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
```

**Train 3 input**
```text
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 0 2 2 2 0 0
0 8 0 8 0 0 2 0 2 0 0
0 8 8 8 0 0 2 2 2 0 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2 2 2 2
2 2 2 2 2 2
2 2 0 0 2 2
2 2 0 0 2 2
2 2 2 2 2 2
2 2 2 2 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 6 6 6 6 0
0 0 3 0 0 0 0 6 0 0 6 0
0 0 3 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 6 6 6 6 0
0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
6 6 0 0 0 0 6 6
6 6 0 0 0 0 6 6
6 6 0 0 0 0 6 6
6 6 0 0 0 0 6 6
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
```

**Test input**
```text
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 7 7 7 0 0 0 0
0 3 0 0 0 7 0 7 0 0 0 0
0 3 3 3 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7 7 7 7
7 7 7 7 7 7
7 7 0 0 7 7
7 7 0 0 7 7
7 7 7 7 7 7
7 7 7 7 7 7
```

## Build the Pairwise Intersection Gallery (`hard_96_build_pairwise_intersection_gallery`)

**Difficulty:** hard

**Skills:** panel, alignment, boolean, intersections, gallery

**Scaffold notes:**
- Treat the three panels as aligned binary masks.
- Compute the pairwise intersections A∩B, A∩C, and B∩C.
- Display those three intersections left-to-right as equally sized panels.

**Written solution:** The three input panels are aligned shapes. Build a three-panel gallery showing the pairwise intersections A∩B, A∩C, and B∩C, using color 8 for intersection cells.

**Program solution (Python reference):**
```python
def solve_hard_96_build_pairwise_intersection_gallery(g):
    panels=[]
    for i in range(3):
        x=i*6
        panel=[row[x:x+5] for row in g]
        panels.append(panel)
    def inter(a,b):
        h,w=dims(a)
        out=zeros(h,w)
        for r in range(h):
            for c in range(w):
                if a[r][c]!=0 and b[r][c]!=0:
                    out[r][c]=8
        return out
    items=[inter(panels[0], panels[1]), inter(panels[0], panels[2]), inter(panels[1], panels[2])]
    return hstack(items, gap=1, bg=0)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 6 0 6 0
0 2 0 0 0 0 0 0 4 0 0 0 0 6 0 6 0
0 2 2 2 0 0 0 0 4 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 8 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 7 7 0 0 0 0 2 2 2 0
0 3 0 0 0 0 0 7 7 0 0 0 0 2 0 2 0
0 3 3 0 0 0 0 7 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 8 8 0 0 0 8 8 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 8 8 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 8 0 8 0 0 0 6 6 6 0
0 4 4 4 0 0 0 8 0 8 0 0 0 0 6 0 0
0 0 0 4 0 0 0 8 8 8 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 8 0
0 8 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 4 0 0 0 0 0 7 7 7 0
0 2 2 0 0 0 0 4 0 0 0 0 0 7 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 8 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 6 6 6 0 0 0 8 8 0 0
0 3 0 3 0 0 0 0 6 0 0 0 0 8 8 0 0
0 3 3 3 0 0 0 0 6 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 8 8 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Cast Border Rays and Mark Matching Intersections (`hard_97_cast_border_rays_and_mark_matching_intersections`)

**Difficulty:** hard

**Skills:** ray casting with blockers, two-direction constraint reasoning, same-size transform

**Scaffold notes:**
- Top-border emitters cast vertical rays downward until a wall.
- Left-border emitters cast horizontal rays rightward until a wall.
- Color a cell only when a vertical and a horizontal ray of the same color both reach it.

**Written solution:** Emitters on the top border send rays downward and emitters on the left border send rays rightward, both stopping at walls. Mark a cell only if it is reached by both a horizontal and a vertical ray of the same color; keep the walls and emitters.

**Program solution (Python reference):**
```python
def solve_hard_97_cast_border_rays_and_mark_matching_intersections(g):
    h,w=dims(g)
    out=zeros(h,w)
    # preserve walls and emitters
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or (r==0 and g[r][c]!=0) or (c==0 and g[r][c]!=0):
                out[r][c]=g[r][c]
    vertical=[ [set() for _ in range(w)] for _ in range(h) ]
    horizontal=[ [set() for _ in range(w)] for _ in range(h) ]
    for c in range(1,w):
        color=g[0][c]
        if color not in (0,5):
            r=1
            while r<h and g[r][c]!=5:
                vertical[r][c].add(color)
                r += 1
    for r in range(1,h):
        color=g[r][0]
        if color not in (0,5):
            c=1
            while c<w and g[r][c]!=5:
                horizontal[r][c].add(color)
                c += 1
    for r in range(1,h):
        for c in range(1,w):
            if g[r][c]==5:
                out[r][c]=5
                continue
            common = vertical[r][c] & horizontal[r][c]
            if common:
                out[r][c]=sorted(common)[0]
    return out
```

**Train 1 input**
```text
0 0 2 0 0 4 0 0 6 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
6 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 2 0 0 4 0 0 6 0
0 0 0 0 0 0 0 0 0 0
2 0 2 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0
6 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 7 0 0 2 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0
4 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
7 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 7 0 0 2 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0
4 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
7 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 6 0 3 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
3 0 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0
6 0 0 0 0 5 0 0 0
0 0 5 5 5 5 0 0 0
8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 6 0 3 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
3 0 0 0 3 5 0 0 0
0 0 0 0 0 5 0 0 0
6 0 6 0 0 5 0 0 0
0 0 5 5 5 5 0 0 0
8 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 4 0 0 0 7 0 2 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
2 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0
4 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 4 0 0 0 7 0 2 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
2 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0
4 0 4 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 2 0 6 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 5 0 0 0
2 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
6 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 2 0 6 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 4 0 0
0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 5 0 0 0
2 0 2 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
6 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Overlay Transformed Templates into a Count Map (`hard_98_overlay_transformed_templates_to_count_map`)

**Difficulty:** hard

**Skills:** template transforms, overlay reasoning, count-map synthesis

**Scaffold notes:**
- Read the three 5×5 templates across the top.
- The bottom code cells indicate how to transform each template.
- Overlay the transformed templates and convert counts 1, 2, and 3 into colors 2, 4, and 8.

**Written solution:** Take the three top templates, apply the transform code shown beneath each one (1 none, 2 clockwise, 3 180°, 4 counterclockwise), overlay the transformed templates, and output a count map using 2 for single coverage, 4 for double coverage, and 8 for triple coverage.

**Program solution (Python reference):**
```python
def solve_hard_98_overlay_transformed_templates_to_count_map(g):
    panels=[]
    top=g[:5]
    for i in range(3):
        x=i*6
        panel=[row[x:x+5] for row in top]
        panels.append(panel)
    code_row=g[6]
    codes=[]
    for i in range(3):
        segment=code_row[i*6:i*6+5]
        code=next(v for v in segment if v!=0)
        codes.append(code)
    transformed=[apply_transform(panel, code) for panel,code in zip(panels,codes)]
    h,w=dims(transformed[0])
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for panel in transformed if panel[r][c]!=0)
            if cnt:
                out[r][c]={1:2,2:4,3:8}[cnt]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 6 0 6 0
0 2 0 0 0 0 0 0 4 0 0 0 0 6 0 6 0
0 2 2 2 0 0 0 0 4 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 2 0 0 0 0 0 3 0 0
```

**Train 1 output**
```text
0 0 0 0 0
0 4 2 4 0
0 8 2 4 0
0 4 2 8 0
0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 7 7 0 0 0 0 2 2 2 0
0 3 0 0 0 0 0 7 7 0 0 0 0 2 0 2 0
0 3 3 0 0 0 0 7 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 1 0 0 0 0 0 2 0 0
```

**Train 2 output**
```text
0 0 0 0 0
0 8 4 2 0
0 8 2 4 0
0 8 4 4 0
0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 8 0 8 0 0 0 6 6 6 0
0 4 4 4 0 0 0 8 0 8 0 0 0 0 6 0 0
0 0 0 4 0 0 0 8 8 8 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 4 0 0 0 0 0 1 0 0
```

**Train 3 output**
```text
0 0 0 0 0
0 8 4 4 0
0 2 4 4 0
0 2 4 4 2
0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 4 0 0 0 0 0 7 7 7 0
0 2 2 0 0 0 0 4 0 0 0 0 0 7 0 0 0
0 2 0 0 0 0 0 4 4 4 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 0 0 0 0 0 4 0 0
```

**Train 4 output**
```text
0 0 0 0 0
0 8 4 4 0
0 2 2 8 0
0 2 2 4 0
0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 6 6 6 0 0 0 8 8 0 0
0 3 0 3 0 0 0 0 6 0 0 0 0 8 8 0 0
0 3 3 3 0 0 0 0 6 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 2 0 0 0 0 0 1 0 0
```

**Test output**
```text
0 0 0 0 0
0 4 4 4 0
0 8 4 4 0
0 4 2 4 0
0 0 0 0 0
```
