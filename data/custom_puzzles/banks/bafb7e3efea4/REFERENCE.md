# ARC Puzzle Bank — Twentieth 21 Puzzles
This twentieth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`134`–`140`) so it follows directly after the nineteenth bundle.
This volume leans into a new mix: row interval fills, main-diagonal completion, singleton-to-diamond growth, full-cross projection, legend-driven object selection, header-derived match maps, blocked-ray painting, area-parity recolors, library decoding, nearest-seed chamber fills, rotation relation matrices, centered transform stamping, and cross-product transform galleries.
It also introduces and reuses a few convenient solver primitives: `row_interval_fill`, `blocked_rays_count`, `nearest_seed_fill`, `rotation_relation_matrix`, and `transform_gallery_row`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_twentieth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_twentieth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_twentieth_21.md` — this human-readable catalog.

## Easy (7)
- `easy_134_fill_between_matching_row_markers` — **Fill Between the Matching Row Markers**
- `easy_135_complete_main_diagonal_reflection` — **Complete the Main-Diagonal Reflection**
- `easy_136_expand_singletons_to_diamonds` — **Expand the Singletons into Diamonds**
- `easy_137_left_pack_rows_preserving_order` — **Left-Pack the Rows While Preserving Order**
- `easy_138_project_markers_to_full_crosses` — **Project the Markers to Full Crosses**
- `easy_139_fill_hollow_rectangles` — **Fill the Hollow Rectangles**
- `easy_140_crop_tight_nonzero_bbox` — **Crop the Tight Nonzero Bounding Box**

## Medium (7)
- `medium_134_select_legend_object_and_flip_horizontally` — **Select the Legend-Matched Object and Flip It Horizontally**
- `medium_135_build_row_column_color_match_map` — **Build the Row/Column Color-Match Map**
- `medium_136_apply_rightward_gravity_in_each_walled_segment` — **Apply Rightward Gravity in Each Walled Segment**
- `medium_137_match_prototype_under_rotation_and_recolor` — **Match the Prototype Under Rotation and Recolor It**
- `medium_138_paint_blocked_rays_from_emitters` — **Paint the Blocked Rays from the Emitters**
- `medium_139_recolor_components_by_area_parity` — **Recolor the Components by Area Parity**
- `medium_140_select_object_touching_two_borders_and_crop` — **Select the Object Touching Two Borders and Crop It**

## Hard (7)
- `hard_134_decode_library_with_transform_and_border_codes` — **Decode the Library with Transform and Border Codes**
- `hard_135_overlay_blocked_ray_counts` — **Overlay the Blocked Rays into a Count Map**
- `hard_136_fill_chambers_by_nearest_seed_with_tie_break` — **Fill the Chambers by the Nearest Seed with a Tie Break**
- `hard_137_build_rotation_relation_matrix` — **Build the Rotation Relation Matrix**
- `hard_138_select_transform_recolor_and_center_stamp` — **Select, Transform, Recolor, and Center-Stamp**
- `hard_139_build_cross_product_gallery_of_color_and_transform_codes` — **Build the Cross-Product Gallery of Color and Transform Codes**
- `hard_140_decode_transform_sequence_and_stamp_row` — **Decode the Transform Sequence and Stamp the Row**

## Fill Between the Matching Row Markers (`easy_134_fill_between_matching_row_markers`)

**Difficulty:** easy

**Skills:** row interval filling, same-size transform, endpoint detection


**Scaffold notes:**
- Look at each row independently.
- When a row has two equal-colored markers, the whole span between them should take that color.
- Rows without such a pair stay unchanged.

**Written solution:** For each row, find the two nonzero endpoint markers. If they have the same color, fill every cell between them, inclusive, with that color.

**Program solution (Python reference):**
```python
def solve_easy_134_fill_between_matching_row_markers(g):
    h, w = dims(g)
    out = clone(g)
    for r in range(h):
        nz = [(c, v) for c, v in enumerate(g[r]) if v != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            c0, color = nz[0]
            c1, _ = nz[1]
            for c in range(min(c0, c1), max(c0, c1) + 1):
                out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 5 0
```

**Train 2 output**
```text
0 0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 5 5 5 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0
```


## Complete the Main-Diagonal Reflection (`easy_135_complete_main_diagonal_reflection`)

**Difficulty:** easy

**Skills:** diagonal symmetry completion, square-grid reasoning, copying structure


**Scaffold notes:**
- Treat the main diagonal as the mirror line.
- Every colored cell should also appear at its transposed position.
- Keep the original cells and add the missing mirrored ones.

**Written solution:** Reflect every nonzero cell across the main diagonal. If a cell is at row r and column c, copy the same color to row c and column r.

**Program solution (Python reference):**
```python
def solve_easy_135_complete_main_diagonal_reflection(g):
    n = len(g)
    out = clone(g)
    for r in range(n):
        for c in range(n):
            if g[r][c] != 0:
                out[c][r] = g[r][c]
    return out
```

**Train 1 input**
```text
0 2 0 0 0 0
0 0 0 0 3 0
0 0 0 0 0 4
0 0 0 0 0 0
0 0 6 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0
2 0 0 0 3 0
0 0 0 0 6 4
0 0 0 0 0 0
0 3 6 0 0 0
0 0 4 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 7 0
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 4
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 7 0
0 0 2 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 4
0 0 0 0 0 8 0
7 0 0 0 8 0 0
0 0 0 4 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 3 0
0 0 0 0 0 0 5 0
0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0
3 5 0 0 0 0 0 0
0 0 0 0 9 0 0 0
```

**Train 4 input**
```text
4 0 0 0 0 0
0 0 0 6 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 2
0 0 0 0 0 0
```

**Train 4 output**
```text
4 0 0 0 0 0
0 0 0 6 0 0
0 0 0 0 0 0
0 6 0 0 0 0
0 0 0 0 0 2
0 0 0 0 2 0
```

**Test input**
```text
0 0 0 0 0 0 5
0 0 0 0 0 0 0
0 0 0 0 7 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 9
```

**Test output**
```text
0 0 0 0 0 0 5
0 0 0 0 0 3 0
0 0 0 0 7 0 0
0 0 0 0 0 0 0
0 0 7 0 0 0 0
0 3 0 0 0 0 0
5 0 0 0 0 0 9
```


## Expand the Singletons into Diamonds (`easy_136_expand_singletons_to_diamonds`)

**Difficulty:** easy

**Skills:** local expansion, Manhattan neighborhood, same-size transform


**Scaffold notes:**
- Each nonzero cell acts like a seed.
- The seed expands to itself plus its four orthogonal neighbors.
- Clip the diamond at the grid boundary if necessary.

**Written solution:** Replace each singleton seed by a radius-1 Manhattan diamond: the seed itself and the cells directly above, below, left, and right become that seed's color.

**Program solution (Python reference):**
```python
def solve_easy_136_expand_singletons_to_diamonds(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for dr, dc in ((0,0), (1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < h and 0 <= nc < w:
                        out[nr][nc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0 0 0
2 2 2 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 4 4 4 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0
```

**Train 2 output**
```text
0 0 0 6 6 6 0 0 0
0 0 0 0 6 0 0 0 0
0 3 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 0
0 0 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 0 9 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 4 0 0 2 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
```

**Test input**
```text
3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2
```

**Test output**
```text
3 3 0 0 0 0 0 0
3 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 6 6 6 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 2
```


## Left-Pack the Rows While Preserving Order (`easy_137_left_pack_rows_preserving_order`)

**Difficulty:** easy

**Skills:** row compaction, order preservation, same-size transform


**Scaffold notes:**
- Read each row from left to right.
- Keep the nonzero colors in that order.
- Move them flush to the left and leave the rest zero.

**Written solution:** For each row, remove the zeros, keep the remaining colors in their original left-to-right order, and write them back starting from the left edge.

**Program solution (Python reference):**
```python
def solve_easy_137_left_pack_rows_preserving_order(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        vals = [v for v in g[r] if v != 0]
        for i, v in enumerate(vals):
            out[r][i] = v
    return out
```

**Train 1 input**
```text
0 2 0 4 0 0 6 0
0 0 0 0 0 0 0 0
3 0 0 5 0 7 0 0
0 9 0 0 1 0 0 0
0 0 8 0 0 0 0 2
```

**Train 1 output**
```text
2 4 6 0 0 0 0 0
0 0 0 0 0 0 0 0
3 5 7 0 0 0 0 0
9 1 0 0 0 0 0 0
8 2 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 7 0 3 0 0
5 0 0 0 0 1 0
0 4 0 6 0 0 2
0 0 0 0 0 0 0
8 0 9 0 0 0 0
0 2 0 0 3 0 4
```

**Train 2 output**
```text
7 3 0 0 0 0 0
5 1 0 0 0 0 0
4 6 2 0 0 0 0
0 0 0 0 0 0 0
8 9 0 0 0 0 0
2 3 4 0 0 0 0
```

**Train 3 input**
```text
1 0 2 0 3 0 4 0 5
0 0 0 6 0 0 0 0 0
7 0 8 9 0 0 0 0 0
0 2 0 0 0 5 0 0 1
```

**Train 3 output**
```text
1 2 3 4 5 0 0 0 0
6 0 0 0 0 0 0 0 0
7 8 9 0 0 0 0 0 0
2 5 1 0 0 0 0 0 0
```

**Train 4 input**
```text
0 3 0 0 0 7 0 8
6 0 0 0 2 0 0 0
0 0 5 0 0 4 0 0
1 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 7 8 0 0 0 0 0
6 2 0 0 0 0 0 0
5 4 0 0 0 0 0 0
1 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 4 0 0 7 0 0 2
3 0 0 5 0 6 0 0
0 0 8 0 0 0 0 1
9 0 0 0 0 0 4 0
0 2 0 0 0 3 0 0
```

**Test output**
```text
4 7 2 0 0 0 0 0
3 5 6 0 0 0 0 0
8 1 0 0 0 0 0 0
9 4 0 0 0 0 0 0
2 3 0 0 0 0 0 0
```


## Project the Markers to Full Crosses (`easy_138_project_markers_to_full_crosses`)

**Difficulty:** easy

**Skills:** row/column projection, same-size transform, marker expansion


**Scaffold notes:**
- Each marker controls its whole row and its whole column.
- Paint straight outward all the way to the grid edges.
- The result is the union of those full crosses.

**Written solution:** For every nonzero marker, paint its entire row and entire column with the marker color. The output is the union of all such crosses.

**Program solution (Python reference):**
```python
def solve_easy_138_project_markers_to_full_crosses(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for cc in range(w):
                    out[r][cc] = v
                for rr in range(h):
                    out[rr][c] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 3 0 3 0 0
3 3 3 3 3 3 3
0 0 3 0 3 0 0
0 0 3 0 3 0 0
0 0 3 0 3 0 0
3 3 3 3 3 3 3
0 0 3 0 3 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
6 6 6 6 6 6 6 6
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
6 6 6 6 6 6 6 6
0 6 0 0 0 0 6 0
```

**Train 3 input**
```text
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2 2 2 2 2 2 2
0 2 0 0 2 0 0 2 0
0 2 0 0 2 0 0 2 0
2 2 2 2 2 2 2 2 2
0 2 0 0 2 0 0 2 0
0 2 0 0 2 0 0 2 0
2 2 2 2 2 2 2 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 8 0 0 0 8 0 0
0 0 8 0 0 0 8 0 0
8 8 8 8 8 8 8 8 8
0 0 8 0 0 0 8 0 0
8 8 8 8 8 8 8 8 8
0 0 8 0 0 0 8 0 0
0 0 8 0 0 0 8 0 0
0 0 8 0 0 0 8 0 0
0 0 8 0 0 0 8 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
0 0 0 5 0 0 0 0 5 0
0 0 0 5 0 0 0 0 5 0
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
```


## Fill the Hollow Rectangles (`easy_139_fill_hollow_rectangles`)

**Difficulty:** easy

**Skills:** rectangle detection, interior filling, same-size transform


**Scaffold notes:**
- Each connected colored border is a hollow rectangle.
- Use its bounding box.
- Fill the whole rectangle area with that same color.

**Written solution:** Find each hollow rectangular border, compute its bounding box, and fill that entire rectangle, including the interior, with the rectangle's color.

**Program solution (Python reference):**
```python
def solve_easy_139_fill_hollow_rectangles(g):
    out = clone(g)
    for cells in connected_components(g):
        color = g[cells[0][0]][cells[0][1]]
        r0, c0, r1, c1 = bbox(cells)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 3 3 3 0 0 0 0 0 0 0
3 0 0 3 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 7 0 0 0 0 7
0 0 0 0 0 7 0 0 0 0 7
0 0 0 0 0 7 7 7 7 7 7
```

**Train 2 output**
```text
3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 7 7 7 7 7 7
0 0 0 0 0 7 7 7 7 7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 8 8 8 0 0 0 5 0 0 5 0
0 8 0 8 0 0 0 5 5 5 5 0
0 8 0 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 8 8 8 0 0 0 5 5 5 5 0
0 8 8 8 0 0 0 5 5 5 5 0
0 8 8 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
9 9 9 0 0 0 0 0 0 0
9 0 9 0 0 0 0 0 0 0
9 0 9 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
6 6 6 6 6 6 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 5 5 5 5 0
0 2 0 0 2 0 0 5 0 0 5 0
0 2 2 2 2 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Crop the Tight Nonzero Bounding Box (`easy_140_crop_tight_nonzero_bbox`)

**Difficulty:** easy

**Skills:** size-changing transform, bounding-box extraction, cropping


**Scaffold notes:**
- Ignore the surrounding empty margin.
- Keep the smallest rectangle that still contains every nonzero cell.
- Return just that cropped subgrid.

**Written solution:** Take the smallest axis-aligned bounding box that contains all nonzero cells and output exactly that cropped region.

**Program solution (Python reference):**
```python
def solve_easy_140_crop_tight_nonzero_bbox(g):
    return crop_nonzero(g)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 0
2 0 0 0 0
2 2 0 0 0
0 0 4 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 6 0
0 0 0 0 0 6 6
0 0 0 0 0 0 6
0 0 0 0 0 0 0
0 0 0 0 0 0 0
3 3 0 0 0 0 0
3 3 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 5 0 0 0 0 0 0
5 5 5 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0
8 8 0
0 8 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 2 0 2
0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0
```


## Select the Legend-Matched Object and Flip It Horizontally (`medium_134_select_legend_object_and_flip_horizontally`)

**Difficulty:** medium

**Skills:** legend lookup, object selection, horizontal reflection, cropping


**Scaffold notes:**
- The top-left legend cell tells you which colored object matters.
- Ignore the legend cell itself and find the object of that color.
- Crop that object tightly, then mirror it left-to-right.

**Written solution:** Read the legend color from the top-left cell, locate the connected object of that color, crop it to its own bounding box, and horizontally flip the cropped object.

**Program solution (Python reference):**
```python
def solve_medium_134_select_legend_object_and_flip_horizontally(g):
    legend = g[0][0]
    comps = connected_components(g, colors={legend}, ignore_positions={(0, 0)})
    target = max(comps, key=len)
    return hflip(component_grid(g, target))
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 3 3 0 0 0 0 0
0 0 2 2 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 3 3
3 3 0
```

**Train 2 input**
```text
5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 5 0 0 0 0 0 0 0 2 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5
5 5
5 0
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4
4 0
4 0
```

**Train 4 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 7 0 0 0 0 0 0 0 0 0
0 3 3 0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 7
0 7 7
7 7 0
```

**Test input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 0
0 0 2 2 0 0 0 0 0 0 0 0 0 4 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2
2 2
0 2
```


## Build the Row/Column Color-Match Map (`medium_135_build_row_column_color_match_map`)

**Difficulty:** medium

**Skills:** header interpretation, matrix construction, color equality reasoning


**Scaffold notes:**
- The top row provides the column colors.
- The left column provides the row colors.
- Write the matching color at an interior position exactly when the row and column colors are the same.

**Written solution:** Discard the headers conceptually and create the interior matrix. At each interior position, output the shared color if the row header equals the column header; otherwise output 0.

**Program solution (Python reference):**
```python
def solve_medium_135_build_row_column_color_match_map(g):
    top = g[0][1:]
    left = [row[0] for row in g[1:]]
    out = zeros(len(left), len(top))
    for r, lc in enumerate(left):
        for c, tc in enumerate(top):
            if lc != 0 and lc == tc:
                out[r][c] = lc
    return out
```

**Train 1 input**
```text
0 2 3 4 2 5 3
5 0 0 0 0 0 0
2 0 0 0 0 0 0
4 0 0 0 0 0 0
3 0 0 0 0 0 0
2 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 5 0
2 0 0 2 0 0
0 0 4 0 0 0
0 3 0 0 0 3
2 0 0 2 0 0
```

**Train 2 input**
```text
0 7 6 7 8 6
6 0 0 0 0 0
8 0 0 0 0 0
7 0 0 0 0 0
7 0 0 0 0 0
```

**Train 2 output**
```text
0 6 0 0 6
0 0 0 8 0
7 0 7 0 0
7 0 7 0 0
```

**Train 3 input**
```text
0 3 5 3 5 2 2
2 0 0 0 0 0 0
5 0 0 0 0 0 0
4 0 0 0 0 0 0
3 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 2 2
0 5 0 5 0 0
0 0 0 0 0 0
3 0 3 0 0 0
```

**Train 4 input**
```text
0 9 4 1 4 9
1 0 0 0 0 0
9 0 0 0 0 0
4 0 0 0 0 0
4 0 0 0 0 0
2 0 0 0 0 0
```

**Train 4 output**
```text
0 0 1 0 0
9 0 0 0 9
0 4 0 4 0
0 4 0 4 0
0 0 0 0 0
```

**Test input**
```text
0 6 2 6 5 3 5
3 0 0 0 0 0 0
6 0 0 0 0 0 0
5 0 0 0 0 0 0
2 0 0 0 0 0 0
6 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 3 0
6 0 6 0 0 0
0 0 0 5 0 5
0 2 0 0 0 0
6 0 6 0 0 0
```


## Apply Rightward Gravity in Each Walled Segment (`medium_136_apply_rightward_gravity_in_each_walled_segment`)

**Difficulty:** medium

**Skills:** segmentation by walls, local gravity, order preservation


**Scaffold notes:**
- Treat every row segment between walls as its own container.
- Within each segment, the nonzero cells slide to the right.
- Preserve the order of the colored cells inside each segment.

**Written solution:** For each row, split it into contiguous non-wall segments. In every such segment, shift the nonzero values to the right edge while keeping their original order, and leave the wall cells fixed.

**Program solution (Python reference):**
```python
def solve_medium_136_apply_rightward_gravity_in_each_walled_segment(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        c = 0
        while c < w:
            if g[r][c] == 8:
                out[r][c] = 8
                c += 1
                continue
            start = c
            while c < w and g[r][c] != 8:
                c += 1
            end = c
            vals = [g[r][cc] for cc in range(start, end) if g[r][cc] != 0]
            write = end - len(vals)
            for i, v in enumerate(vals):
                out[r][write + i] = v
    return out
```

**Train 1 input**
```text
8 0 2 0 8 3 0 4 0 8
8 5 0 0 8 0 6 0 7 8
8 0 0 0 8 2 0 0 0 8
8 1 0 9 8 0 0 0 4 8
8 0 3 0 8 8 0 5 0 8
8 2 0 0 8 7 0 0 0 8
```

**Train 1 output**
```text
8 0 0 2 8 0 0 3 4 8
8 0 0 5 8 0 0 6 7 8
8 0 0 0 8 0 0 0 2 8
8 0 1 9 8 0 0 0 4 8
8 0 0 3 8 8 0 0 5 8
8 0 0 2 8 0 0 0 7 8
```

**Train 2 input**
```text
0 4 0 8 2 0 0 8 5 0 0
0 0 6 8 0 3 0 8 0 7 0
1 0 0 8 4 0 2 8 0 0 8
0 9 0 8 0 0 0 8 6 0 0
3 0 5 8 7 0 0 8 0 0 2
```

**Train 2 output**
```text
0 0 4 8 0 0 2 8 0 0 5
0 0 6 8 0 0 3 8 0 0 7
0 0 1 8 0 4 2 8 0 0 8
0 0 9 8 0 0 0 8 0 0 6
0 3 5 8 0 0 7 8 0 0 2
```

**Train 3 input**
```text
8 1 0 0 8 0 4 0 8 2 0 0 8
8 0 3 0 8 5 0 6 8 0 0 7 8
8 0 0 0 8 0 0 0 8 9 0 0 8
8 2 0 8 8 1 0 0 8 0 3 0 8
```

**Train 3 output**
```text
8 0 0 1 8 0 0 4 8 0 0 2 8
8 0 0 3 8 0 5 6 8 0 0 7 8
8 0 0 0 8 0 0 0 8 0 0 9 8
8 0 2 8 8 0 0 1 8 0 0 3 8
```

**Train 4 input**
```text
0 0 5 0 8 0 2 0 0 8 4 0
7 0 0 0 8 3 0 0 1 8 0 6
0 9 0 8 8 0 0 5 0 8 2 0
4 0 0 0 8 0 7 0 0 8 0 3
0 0 1 0 8 6 0 0 0 8 8 0
```

**Train 4 output**
```text
0 0 0 5 8 0 0 0 2 8 0 4
0 0 0 7 8 0 0 3 1 8 0 6
0 0 9 8 8 0 0 0 5 8 0 2
0 0 0 4 8 0 0 0 7 8 0 3
0 0 0 1 8 0 0 0 6 8 8 0
```

**Test input**
```text
8 0 6 0 8 2 0 0 8 5 0 8
8 3 0 4 8 0 0 7 8 0 9 8
8 0 0 0 8 1 0 0 8 6 0 8
8 5 0 2 8 0 8 0 8 0 4 8
8 0 7 0 8 3 0 0 8 2 0 8
```

**Test output**
```text
8 0 0 6 8 0 0 2 8 0 5 8
8 0 3 4 8 0 0 7 8 0 9 8
8 0 0 0 8 0 0 1 8 0 6 8
8 0 5 2 8 0 8 0 8 0 4 8
8 0 0 7 8 0 0 3 8 0 2 8
```


## Match the Prototype Under Rotation and Recolor It (`medium_137_match_prototype_under_rotation_and_recolor`)

**Difficulty:** medium

**Skills:** panel parsing, rotation equivalence, object selection, recoloring


**Scaffold notes:**
- The left panel is the prototype shape.
- Exactly one candidate panel is the same shape up to rotation.
- Take that candidate, crop it, and recolor it to the footer color.

**Written solution:** Compare the prototype panel to the candidate panels up to rotation. Select the matching candidate, crop it to its tight bounding box, and recolor all nonzero cells to the target color given in the footer row.

**Program solution (Python reference):**
```python
def solve_medium_137_match_prototype_under_rotation_and_recolor(g):
    target_color = g[5][0]
    proto = [row[0:5] for row in g[0:5]]
    candidates = [[row[c:c+5] for row in g[0:5]] for c in (6, 12, 18)]
    rotset = all_rotations(proto)
    for cand in candidates:
        if normalize_binary(cand) in rotset:
            return recolor_nonzero(crop_nonzero(cand), target_color)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 2 2 2 0 0 0 0 3 0 0 0 0 4 4 0 0
0 1 0 0 0 0 0 2 0 0 0 0 0 3 3 3 0 0 0 0 4 4 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 7
7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 2 0 2 0 0 0 5 5 0 0 0 0 4 0 0 0
0 0 1 1 0 0 0 2 2 2 0 0 0 0 5 5 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0
0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 3 0 0 0 0 0 6 6 6 0 0 0 5 5 0 0
0 0 1 0 0 0 0 3 3 0 0 0 0 6 0 0 0 0 0 5 5 0 0
0 0 1 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2
2 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 7 7 0 0 0 0 0 4 4 0 0 0 9 9 9 0
0 1 1 1 0 0 0 7 7 0 0 0 0 4 4 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6
0 6 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 5 5 0 0 0 3 0 3 0 0 0 0 7 0 0
0 1 1 0 0 0 0 5 5 0 0 0 0 3 3 3 0 0 0 0 7 0 0
0 0 1 1 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 4 4
4 4 0
4 0 0
```


## Paint the Blocked Rays from the Emitters (`medium_138_paint_blocked_rays_from_emitters`)

**Difficulty:** medium

**Skills:** ray casting, wall blocking, same-size transform


**Scaffold notes:**
- The 2-cells are emitters and the 8-cells are blockers.
- Each emitter sends rays in the four cardinal directions.
- A ray keeps painting until it hits a wall or the grid edge.

**Written solution:** From every emitter cell, extend in the four cardinal directions and color each reached cell with 2 until a wall cell 8 or the edge stops the ray. Keep the walls in place.

**Program solution (Python reference):**
```python
def solve_medium_138_paint_blocked_rays_from_emitters(g):
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 2:
                for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                    rr, cc = r + dr, c + dc
                    while 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 8:
                        out[rr][cc] = 2
                        rr += dr
                        cc += dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 8 0 0 0 0
0 2 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 2 0
0 0 0 8 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 8 0 0 2 0
2 2 2 2 2 8 0 0 2 0
0 2 0 0 0 8 0 0 2 0
0 2 8 8 8 8 8 8 2 0
0 2 0 0 0 0 0 0 2 0
0 2 0 8 0 0 0 0 2 0
0 2 0 8 2 2 2 2 2 2
0 2 0 8 0 0 0 0 2 0
```

**Train 2 input**
```text
0 2 0 0 0 0 8 0
0 0 0 0 0 0 8 0
8 8 8 8 8 8 8 8
0 0 0 0 0 0 8 0
0 0 0 8 0 0 8 0
0 0 0 8 0 2 8 0
0 0 0 8 0 0 0 0
0 0 0 8 0 0 0 0
```

**Train 2 output**
```text
2 2 2 2 2 2 8 0
0 2 0 0 0 0 8 0
8 8 8 8 8 8 8 8
0 0 0 0 0 2 8 0
0 0 0 8 0 2 8 0
0 0 0 8 2 2 8 0
0 0 0 8 0 2 0 0
0 0 0 8 0 2 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 8 0
0 0 0 0 8 0 0 8 0
0 0 2 0 8 0 0 8 0
0 0 0 0 8 0 0 8 0
0 0 0 0 8 0 0 0 2
0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
0 0 2 0 0 0 0 8 2
0 0 2 0 8 0 0 8 2
2 2 2 2 8 0 0 8 2
0 0 2 0 8 0 0 8 2
0 0 2 0 8 2 2 2 2
0 0 2 0 8 0 0 0 2
8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 2 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 2 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 2 0
0 0 0 8 2 2 2 2 2 2
0 0 0 8 0 0 0 0 2 0
0 0 0 8 0 0 0 0 2 0
0 8 8 8 8 8 8 8 8 0
0 0 2 0 0 0 8 0 0 0
0 0 2 0 0 0 8 0 0 0
2 2 2 2 2 2 8 0 0 0
0 0 2 0 0 0 8 0 0 0
```

**Test input**
```text
0 0 0 0 8 0 0 0 0 0
0 2 0 0 8 0 0 0 0 0
0 0 0 0 8 0 0 8 0 0
0 0 0 0 8 0 0 8 0 0
0 0 0 0 8 0 0 8 0 0
0 0 0 0 8 0 0 0 2 0
0 0 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 8 0 0 0 2 0
2 2 2 2 8 0 0 0 2 0
0 2 0 0 8 0 0 8 2 0
0 2 0 0 8 0 0 8 2 0
0 2 0 0 8 0 0 8 2 0
0 2 0 0 8 2 2 2 2 2
0 2 8 8 8 8 8 8 8 8
0 2 0 0 0 0 0 0 0 0
```


## Recolor the Components by Area Parity (`medium_139_recolor_components_by_area_parity`)

**Difficulty:** medium

**Skills:** connected components, area counting, conditional recoloring


**Scaffold notes:**
- Separate the nonzero cells into connected objects.
- Count the number of cells in each object.
- Odd-sized objects become one color and even-sized objects become another.

**Written solution:** Find each connected nonzero component, count its cells, and recolor the whole component to 3 if its area is odd or 4 if its area is even.

**Program solution (Python reference):**
```python
def solve_medium_139_recolor_components_by_area_parity(g):
    h, w = dims(g)
    out = zeros(h, w)
    for cells in connected_components(g):
        color = 3 if (len(cells) % 2 == 1) else 4
        for r, c in cells:
            out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 6 0 0 0 0
0 6 0 0 0 0 6 6 6 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0 0 0 0
0 4 0 0 0 0 4 4 4 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 6 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 6 0 0 0 0 6 6 6 0
0 6 6 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 4 0 0 0 0 3 3 3 0
0 4 4 0 0 0 0 3 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 6 6 0 0
0 6 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 4 4 0 0
0 3 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 6 0 0 0 0
0 6 6 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 3 0 0 0 0
0 4 4 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## Select the Object Touching Two Borders and Crop It (`medium_140_select_object_touching_two_borders_and_crop`)

**Difficulty:** medium

**Skills:** border reasoning, connected components, cropping


**Scaffold notes:**
- Check how many outer borders each object touches.
- Exactly one object touches two borders of the full grid.
- Return only that object's tight crop.

**Written solution:** Find the connected object that touches exactly two distinct outer borders of the input grid, then crop and output that object alone.

**Program solution (Python reference):**
```python
def solve_medium_140_select_object_touching_two_borders_and_crop(g):
    h, w = dims(g)
    for cells in connected_components(g):
        if len(touch_borders(cells, h, w)) == 2:
            return component_grid(g, cells)
    return [[0]]
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0
2 0
2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 5 0 5
0 0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 3 0 7 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 5
5 5 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6
6 6
6 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 4 4
```

**Train 4 output**
```text
0 4 0
4 4 4
```

**Test input**
```text
7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 0
7 7
0 7
```


## Decode the Library with Transform and Border Codes (`hard_134_decode_library_with_transform_and_border_codes`)

**Difficulty:** hard

**Skills:** library lookup, symbolic code decoding, geometric transform, recoloring, frame construction


**Scaffold notes:**
- The header row gives a prototype index, a transform code, a fill color, and a border color.
- Use the index to select one library panel.
- Transform and recolor the selected shape, then wrap it in a one-cell border.

**Written solution:** Read the selected prototype index and transform code from the header, crop that library shape, apply the requested transform, recolor all nonzero cells to the fill color, and then surround the result with a one-cell rectangular border in the border color.

**Program solution (Python reference):**
```python
def solve_hard_134_decode_library_with_transform_and_border_codes(g):
    index = g[0][0] - 1
    transform_code = g[0][1]
    fill_color = g[0][2]
    border_color = g[0][3]
    panels = [[row[c:c+5] for row in g[1:6]] for c in (0, 6, 12)]
    obj = crop_nonzero(panels[index])
    obj = transform_by_code(obj, transform_code)
    obj = recolor_nonzero(obj, fill_color)
    return add_rect_border(obj, border_color)
```

**Train 1 input**
```text
2 1 7 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 1 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 1 1 0 0 0 1 1 1 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
9 9 9 9
9 0 7 9
9 7 7 9
9 7 0 9
9 9 9 9
```

**Train 2 input**
```text
1 4 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 1 0 0 0 0 0 1 1 0 0
0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 8
8 3 0 3 8
8 3 3 3 8
8 8 8 8 8
```

**Train 3 input**
```text
3 2 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 0 0 0 0 0 1 1 0 0
0 0 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 2 2
2 5 5 2
2 5 5 2
2 2 2 2
```

**Train 4 input**
```text
2 5 6 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 1 0 0 0 0 0 1 0 1 0
0 1 1 1 0 0 0 1 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 4 4
4 6 6 4
4 6 0 4
4 6 0 4
4 4 4 4
```

**Test input**
```text
1 3 2 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 0 0 0 0 0 1 1 0 0
0 1 1 0 0 0 0 1 1 0 0 0 0 0 1 1 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7 7 7
7 2 2 0 7
7 2 2 2 7
7 7 7 7 7
```


## Overlay the Blocked Rays into a Count Map (`hard_135_overlay_blocked_ray_counts`)

**Difficulty:** hard

**Skills:** ray casting, overlap counting, count-to-color encoding, wall handling


**Scaffold notes:**
- Emitters send blocked rays just as in the simpler ray task.
- Now overlapping rays matter.
- Convert the number of rays through each cell into a color code.

**Written solution:** Cast blocked cardinal rays from every emitter. Count how many rays cover each cell, keep walls as 8, and encode the counts as 2 for one ray, 3 for two rays, and 4 for three or more rays.

**Program solution (Python reference):**
```python
def solve_hard_135_overlay_blocked_ray_counts(g):
    h, w = dims(g)
    counts = count_rays(g, emitter_color=2, wall=8)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 8:
                out[r][c] = 8
            elif counts[r][c] == 1:
                out[r][c] = 2
            elif counts[r][c] == 2:
                out[r][c] = 3
            elif counts[r][c] >= 3:
                out[r][c] = 4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 8 0 0 0 0
0 2 0 0 0 8 0 0 2 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 8 0 0 2 0
2 4 2 2 2 8 2 2 4 2
0 2 0 0 0 8 0 0 2 0
0 2 0 0 0 8 0 0 2 0
0 2 8 8 8 8 8 8 2 0
0 2 0 0 2 0 0 0 2 0
2 3 2 2 4 2 2 2 3 2
0 2 0 0 2 0 0 0 2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 2 0 8 0 2 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 2 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 2 0 0 0 2 0 0
0 0 2 0 8 0 2 0 0
2 2 4 2 8 2 4 2 2
0 0 2 0 8 0 2 0 0
0 0 2 0 8 0 2 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 8 0 0 2 0
0 0 0 0 8 2 2 4 2
0 0 0 0 0 0 0 2 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 2 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 2 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 2 0 0 8 0 0 0
2 2 2 2 2 4 2 2 8 0 0 0
0 0 0 0 0 2 0 0 8 0 0 0
0 8 8 8 8 8 8 8 8 8 8 0
0 0 2 0 0 0 0 0 8 0 2 0
0 0 2 0 0 0 0 0 8 0 2 0
3 3 4 3 3 3 3 3 3 3 4 3
0 0 2 0 0 0 0 0 0 0 2 0
```

**Train 4 input**
```text
0 0 0 0 0 0 8 0 0 0
0 2 0 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 2 0 8 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 2 0 0 2 0 8 0 0 0
2 4 2 2 3 2 8 0 0 0
0 2 8 0 2 0 8 0 0 0
0 2 8 0 2 0 8 0 0 0
0 2 8 2 4 2 8 0 0 0
0 2 8 0 2 0 0 0 0 0
0 2 8 8 8 8 8 8 8 0
0 2 8 0 0 0 0 0 2 0
2 3 2 2 2 2 2 2 4 2
0 2 0 0 0 0 0 0 2 0
```

**Test input**
```text
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 2 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 2 0 8 0 0 0
0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 8 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 8 0 2 0 0 0 2 0
0 0 0 8 0 2 0 8 2 4 2
0 0 0 8 0 2 0 8 0 2 0
0 0 0 8 0 2 0 8 0 2 0
0 0 0 8 2 4 2 8 0 2 0
0 8 8 8 8 8 8 8 8 8 0
0 2 0 0 0 0 0 8 0 0 0
2 4 2 2 2 2 2 2 2 2 2
0 2 0 0 0 0 0 0 0 0 0
```


## Fill the Chambers by the Nearest Seed with a Tie Break (`hard_136_fill_chambers_by_nearest_seed_with_tie_break`)

**Difficulty:** hard

**Skills:** chamber segmentation, multi-source distance, nearest-seed filling, tie-breaking


**Scaffold notes:**
- Walls split the board into independent chambers.
- Within each chamber, every cell belongs to the nearest seed color.
- When two seeds are equally near, prefer the smaller color number.

**Written solution:** Treat each wall-bounded chamber separately. For every non-wall cell, find the reachable seed in that chamber with the smallest shortest-path distance; if there is a tie, choose the smaller color, and fill the cell with that seed color.

**Program solution (Python reference):**
```python
def solve_hard_136_fill_chambers_by_nearest_seed_with_tie_break(g):
    h, w = dims(g)
    out = clone(g)
    for cells in flood_regions_nonwall(g, wall=8):
        area = set(cells)
        seeds = [(r, c, g[r][c]) for r, c in cells if g[r][c] != 0]
        if not seeds:
            continue
        dmaps = {(r, c): shortest_paths_from_seed(area, (r, c)) for r, c, _ in seeds}
        for r, c in cells:
            if g[r][c] == 8:
                continue
            best = None
            best_color = None
            for sr, sc, color in seeds:
                d = dmaps[(sr, sc)].get((r, c), 10**9)
                cand = (d, color)
                if best is None or cand < best:
                    best = cand
                    best_color = color
            out[r][c] = best_color
    return out
```

**Train 1 input**
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 8 0 0 0 3 0 8
8 0 0 0 8 0 8 0 0 0 8
8 0 0 0 8 0 8 0 0 0 8
8 4 0 0 8 0 0 0 5 0 8
8 0 0 0 8 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 8 3 3 3 3 3 8
8 2 2 2 8 3 8 3 3 3 8
8 4 4 4 8 5 8 5 5 5 8
8 4 4 4 8 5 5 5 5 5 8
8 4 4 4 8 5 5 5 5 5 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
8 8 8 8 8 8 8 8 8
8 0 0 3 0 0 8 2 8
8 0 8 8 8 0 8 0 8
8 4 0 0 0 0 8 0 8
8 0 0 8 8 0 0 0 8
8 0 0 8 5 0 0 0 8
8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 8 2 8
8 4 8 8 8 3 8 2 8
8 4 4 4 4 5 8 2 8
8 4 4 8 8 5 5 2 8
8 4 4 8 5 5 5 5 8
8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
8 8 8 8 8 8 8 8 8 8
8 2 0 0 8 3 0 0 4 8
8 0 0 0 8 0 8 0 0 8
8 0 0 0 8 0 8 0 0 8
8 5 0 0 8 0 0 0 6 8
8 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
8 8 8 8 8 8 8 8 8 8
8 2 2 2 8 3 3 4 4 8
8 2 2 2 8 3 8 4 4 8
8 5 5 5 8 3 8 6 6 8
8 5 5 5 8 3 6 6 6 8
8 5 5 5 8 3 6 6 6 8
8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
8 8 8 8 8 8 8 8 8
8 2 0 0 0 8 4 0 8
8 0 8 8 0 8 0 0 8
8 0 0 3 0 8 0 5 8
8 0 0 0 0 8 0 0 8
8 6 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 4 4 8
8 2 8 8 3 8 4 5 8
8 2 3 3 3 8 5 5 8
8 6 3 3 3 8 5 5 8
8 6 6 3 3 8 5 5 8
8 8 8 8 8 8 8 8 8
```

**Test input**
```text
8 8 8 8 8 8 8 8 8 8
8 0 0 2 0 8 0 0 3 8
8 0 8 8 0 8 0 8 0 8
8 4 0 0 0 8 5 0 0 8
8 0 0 0 0 8 0 0 0 8
8 0 8 0 0 8 0 8 6 8
8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 3 3 3 8
8 4 8 8 2 8 5 8 3 8
8 4 4 4 2 8 5 5 3 8
8 4 4 4 2 8 5 5 6 8
8 4 8 4 2 8 5 8 6 8
8 8 8 8 8 8 8 8 8 8
```


## Build the Rotation Relation Matrix (`hard_137_build_rotation_relation_matrix`)

**Difficulty:** hard

**Skills:** panel parsing, shape normalization, rotation equivalence, relation matrix construction


**Scaffold notes:**
- Each panel contains one shape.
- Compare every ordered pair of panels up to rotation.
- Use one code for identical orientation, another for rotated equivalence, and 8 on the diagonal.

**Written solution:** Normalize each panel to its cropped binary shape. Build a 4×4 matrix with 8 on the diagonal, 1 when two off-diagonal panels are exactly identical in orientation, 2 when they match only up to a nontrivial rotation, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_137_build_rotation_relation_matrix(g):
    panels = [[row[c:c+5] for row in g] for c in (0, 6, 12, 18)]
    norms = [normalize_binary(p) for p in panels]
    out = zeros(4, 4)
    for i, a in enumerate(norms):
        aset = all_rotations(a)
        for j, b in enumerate(norms):
            if i == j:
                out[i][j] = 8
            elif b == a:
                out[i][j] = 1
            elif b in aset:
                out[i][j] = 2
            else:
                out[i][j] = 0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 1 1 1 0 0 0 1 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0 1
2 8 0 2
0 0 8 0
1 2 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 1 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
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
0 1 1 0 0 0 0 1 1 1 0 0 0 1 0 0 0 0 0 1 1 0 0
0 1 1 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 2 0 1
2 8 0 2
0 0 8 0
1 2 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0
0 1 1 1 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 2 0 0
2 8 0 0
0 0 8 1
0 0 1 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 1 0
0 1 1 1 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 2 0 1
2 8 0 2
0 0 8 0
1 2 0 8
```


## Select, Transform, Recolor, and Center-Stamp (`hard_138_select_transform_recolor_and_center_stamp`)

**Difficulty:** hard

**Skills:** coded selection, object extraction, geometric transform, recoloring, fixed-canvas placement


**Scaffold notes:**
- The header encodes which color to select, how to transform it, and what output color to use.
- Extract the matching object from the scene.
- Transform it, recolor it, and center it on a 7×7 blank canvas.

**Written solution:** Read the selector color, transform code, and target color from the header. Find the connected object of the selector color, crop it, apply the specified transform, recolor its nonzero cells to the target color, and center-stamp it onto a 7×7 output grid.

**Program solution (Python reference):**
```python
def solve_hard_138_select_transform_recolor_and_center_stamp(g):
    selector_color = g[0][0]
    transform_code = g[0][1]
    target_color = g[0][2]
    area = [row[:] for row in g[1:8]]
    comps = connected_components(area, colors={selector_color})
    target = max(comps, key=len)
    obj = component_grid(area, target)
    obj = transform_by_code(obj, transform_code)
    obj = recolor_nonzero(obj, target_color)
    return center_stamp(7, 7, obj)
```

**Train 1 input**
```text
3 1 7 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 5 0 0 0 3 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 7 0 0
0 0 7 7 7 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
5 4 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0
0 0 4 0 0 0 0 0 5 5 5 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 0 2 0 0
0 0 2 2 2 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 3 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 2 2 0 0 0 0 0 4 4 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 6 0 0 0
0 0 6 6 6 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
4 5 9 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 6 0 0 4 4 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 9 9 0 0 0
0 0 9 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test input**
```text
6 2 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 2 0 0
0 0 0 6 0 0 0 0 2 2 2 0 0
0 0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 5 0 0 0 0
0 0 5 5 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## Build the Cross-Product Gallery of Color and Transform Codes (`hard_139_build_cross_product_gallery_of_color_and_transform_codes`)

**Difficulty:** hard

**Skills:** code-strip decoding, cross-product construction, panel gallery generation


**Scaffold notes:**
- The prototype panel is reused many times.
- One code strip lists transforms and the other lists colors.
- Make every color/transform combination and place the results in a gallery grid.

**Written solution:** Take the prototype panel, apply each transform code from the transform strip, recolor the transformed result with each color from the color strip, and arrange the full cross product as a gallery with one row per color and one column per transform.

**Program solution (Python reference):**
```python
def solve_hard_139_build_cross_product_gallery_of_color_and_transform_codes(g):
    proto = [row[:] for row in g[0:5]]
    transform_codes = g[5][0:3]
    colors = g[6][0:3]
    rows = []
    for color in colors:
        prow = []
        for code in transform_codes:
            obj = transform_by_code(proto, code)
            prow.append(recolor_nonzero(obj, color))
        rows.append(prow)
    return panelize_grid(rows, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 0 0 0
0 1 4 0 0
2 5 7 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 2 2 0 0 0 0 0 2 0
0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 2 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 5 5 5 0 0 0 0 0 5 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 5 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 7 7 7 0 0 0 0 0 7 0
0 7 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0
0 7 7 0 0 0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0
0 1 1 0 0
0 0 1 1 0
0 0 0 0 0
0 0 0 0 0
2 3 5 0 0
3 6 8 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 3 3 0 0 0 0 0 3 3 0
0 0 3 3 0 0 0 3 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 6 6 0 0 0 0 0 6 6 0
0 0 6 6 0 0 0 6 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 8 0 0 0 0 0 8 8 0
0 0 8 8 0 0 0 8 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0
0 1 0 1 0
0 1 1 1 0
0 0 0 0 0
0 0 0 0 0
0 2 5 0 0
4 7 9 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 0 4 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 7 7 7 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 7 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 9 9 9 0 0 0 9 9 9 0
0 0 0 0 0 0 0 9 0 9 0 0 0 9 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0
0 1 1 0 0
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
1 4 5 0 0
2 3 6 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 2 0 0 0 0 2 0 0
0 2 2 2 0 0 0 0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 3 3 0 0 0 0 3 0 0
0 3 3 3 0 0 0 0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 6 6 0 0 0 0 6 0 0
0 6 6 6 0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 1 0 0
0 0 0 0 0
0 1 3 0 0
5 7 8 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 5 5 0 0 0 0 0 5 5 0
0 0 5 0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 7 7 0 0 0 0 0 0 0
0 7 7 0 0 0 0 7 7 0 0 0 0 0 7 7 0
0 0 7 0 0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 8 0 0 0 0 0 8 8 0
0 0 8 0 0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## Decode the Transform Sequence and Stamp the Row (`hard_140_decode_transform_sequence_and_stamp_row`)

**Difficulty:** hard

**Skills:** sequential transformation, stateful composition, gallery row construction


**Scaffold notes:**
- The footer row gives a sequence of transforms and a final output color.
- Apply the transforms cumulatively, not independently.
- After each step, recolor the current state and place it as the next panel in the row.

**Written solution:** Starting from the prototype panel, apply the listed transform codes one after another. After each cumulative step, recolor the current nonzero cells to the target color and append that panel to the output row gallery.

**Program solution (Python reference):**
```python
def solve_hard_140_decode_transform_sequence_and_stamp_row(g):
    proto = [row[:] for row in g[0:5]]
    codes = [v for v in g[5][0:4]]
    target_color = g[5][4]
    panels = []
    cur = clone(proto)
    for code in codes:
        cur = transform_by_code(cur, code)
        panels.append(recolor_nonzero(cur, target_color))
    return panelize_row(panels, sep=1)
```

**Train 1 input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 0 0 0
1 4 2 5 7
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 7 7 7 0
0 7 0 0 0 0 0 0 0 7 0 0 0 7 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 1 0 0
0 0 0 0 0
0 1 1 4 3
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 3 3 0 0 0 0 3 0 0 0 0 0 3 0 0
0 3 3 0 0 0 0 3 3 0 0 0 0 0 3 3 0 0 0 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0
0 1 0 1 0
0 1 1 1 0
0 0 0 0 0
0 0 0 0 0
4 1 3 2 5
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 5 5 0 0 0 5 0 5 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 5 0 0 0 0 5 5 5 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0
0 1 1 0 0
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
5 1 4 0 9
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 9 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0
0 0 9 0 0 0 0 9 9 9 0 0 0 9 9 9 0 0 0 9 9 9 0
0 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0
0 1 1 0 0
0 0 1 1 0
0 0 0 0 0
0 0 0 0 0
1 2 4 3 6
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 6 0 0 0 0 0 6 0 0 0 0 0 6 6 0
0 0 6 6 0 0 0 6 6 0 0 0 0 0 6 6 0 0 0 6 6 0 0
0 0 6 0 0 0 0 6 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
