# ARC Puzzle Bank — Twenty-First 21 Puzzles
This twenty-first bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`141`–`147`) so it follows directly after the twentieth bundle.
This volume leans into a different mechanic mix: column interval fills, diagonal X growth, center reductions, legend-based object selection, header intersections, segmented gravity, hole filling, dual-code library decoding, dihedral relation matrices, diagonal visibility counts, priority chamber fills, border-touch signatures, and sequential transform stamping.
It also introduces and reuses a few convenient solver primitives: `border_touch_signature`, `diagonal_visibility_count`, `centered_stamp_on_canvas`, and `transform_sequence_stamp`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_twentyfirst_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_twentyfirst_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_twentyfirst_21.md` — this human-readable catalog.

## Easy (7)
- `easy_141_fill_between_matching_column_markers` — **Fill Between the Matching Column Markers**
- `easy_142_expand_singletons_to_diagonal_xs` — **Expand the Singletons into Diagonal Xs**
- `easy_143_project_top_markers_down_columns` — **Project the Top Markers Down Their Columns**
- `easy_144_reduce_solid_3x3_blocks_to_centers` — **Reduce the Solid 3x3 Blocks to Their Centers**
- `easy_145_mirror_left_half_across_divider` — **Mirror the Left Half Across the Divider**
- `easy_146_outline_rectangles_from_diagonal_corner_pairs` — **Outline Rectangles from Diagonal Corner Pairs**
- `easy_147_bridge_one_cell_vertical_gaps` — **Bridge the One-Cell Vertical Gaps**

## Medium (7)
- `medium_141_select_legend_object_and_rotate_clockwise` — **Select the Legend-Matched Object and Rotate It Clockwise**
- `medium_142_fill_header_selected_intersections` — **Fill the Intersections Chosen by the Headers**
- `medium_143_apply_downward_gravity_in_walled_columns` — **Apply Downward Gravity in the Walled Column Segments**
- `medium_144_crop_the_horizontally_symmetric_object` — **Crop the Horizontally Symmetric Object**
- `medium_145_fill_holes_in_ring_components` — **Fill the Holes in the Ring Components**
- `medium_146_decode_transform_and_recolor_from_control_strip` — **Decode the Transform and Recolor from the Control Strip**
- `medium_147_fill_each_walled_chamber_from_its_seed` — **Fill Each Walled Chamber from Its Seed**

## Hard (7)
- `hard_141_decode_dual_code_library_and_center_stamp` — **Decode the Dual-Code Library and Center-Stamp the Result**
- `hard_142_build_dihedral_equivalence_matrix` — **Build the Dihedral Equivalence Matrix**
- `hard_143_overlay_diagonal_visibility_counts_with_walls` — **Overlay the Diagonal Visibility Counts with Walls**
- `hard_144_build_transform_recolor_gallery` — **Build the Transform × Recolor Gallery**
- `hard_145_fill_chambers_by_seed_priority_legend` — **Fill the Chambers by the Seed Priority Legend**
- `hard_146_select_object_by_border_touch_signature_and_scale2` — **Select the Object by Border-Touch Signature and Scale It by 2**
- `hard_147_apply_transform_sequence_and_stamp_at_anchors` — **Apply the Transform Sequence and Stamp at the Anchors**

## Fill Between the Matching Column Markers (`easy_141_fill_between_matching_column_markers`)

**Difficulty:** easy

**Skills:** column interval filling, same-size transform, endpoint detection


**Scaffold notes:**
- Look at each column independently.
- If a column contains two nonzero markers of the same color, fill the whole vertical span.
- Columns without such a pair stay as they are.

**Written solution:** For each column, locate the nonzero cells. When there are exactly two and they share a color, fill every cell between them, inclusive, with that color.

**Program solution (Python reference):**
```python
def solve_easy_141_fill_between_matching_column_markers(g):
    h, w = dims(g)
    out = clone(g)
    for c in range(w):
        nz = [(r, g[r][c]) for r in range(h) if g[r][c] != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            r0, color = nz[0]
            r1, _ = nz[1]
            for r in range(min(r0, r1), max(r0, r1) + 1):
                out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 5 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
```

**Train 1 output**
```text
0 0 0 0 5 0 0 0 0
0 2 0 0 5 0 0 0 0
0 2 0 0 5 0 0 3 0
0 2 0 0 5 0 0 3 0
0 2 0 0 5 0 0 3 0
0 2 0 0 0 0 0 3 0
0 2 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
```

**Train 2 input**
```text
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 4 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 6 0
7 0 0 4 0 0 0 0 6 0
7 0 0 4 0 0 0 0 6 0
7 0 0 4 0 0 0 0 6 0
7 0 0 4 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 4
0 0 9 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 4
0 0 9 0 0 0 0 4
0 0 9 0 0 2 0 4
0 0 9 0 0 2 0 4
0 0 0 0 0 2 0 4
0 0 0 0 0 2 0 4
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
```

**Train 4 input**
```text
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 0 0
```

**Train 4 output**
```text
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 5 0
0 3 0 0 0 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 5 0
0 0 0 0 8 0 0 0 0 0 0
```

**Test input**
```text
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 2 0
0 0 4 0 0 7 0 0 2 0
0 0 4 0 0 7 0 0 2 0
0 0 4 0 0 7 0 0 2 0
0 0 4 0 0 7 0 0 2 0
0 0 4 0 0 7 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
```

## Expand the Singletons into Diagonal Xs (`easy_142_expand_singletons_to_diagonal_xs`)

**Difficulty:** easy

**Skills:** diagonal growth, local stamping, clipping at borders


**Scaffold notes:**
- Each nonzero cell acts like the center of a tiny X.
- Keep the center and add the four diagonal neighbors when they exist.
- Nothing spreads horizontally or vertically.

**Written solution:** Create a blank output grid. For each nonzero input cell, copy its color to the center position and to the four diagonal neighbors one step away, clipping at the border.

**Program solution (Python reference):**
```python
def solve_easy_142_expand_singletons_to_diagonal_xs(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            color = g[r][c]
            if color == 0:
                continue
            for dr, dc in ((0,0), (-1,-1), (-1,1), (1,-1), (1,1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 2 0 0 0 0
0 2 0 0 0 0 0
2 0 2 0 0 0 0
0 0 0 0 6 0 6
0 0 0 0 0 6 0
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 7 0
0 3 0 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 5 0 5
0 8 0 8 0 0 0 0 5 0
0 0 8 0 0 0 0 5 0 5
0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 6 0 0
0 0 0 0 0 6 0 0 0
2 0 2 0 6 0 6 0 0
0 2 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 9 0 9
```

**Test input**
```text
0 0 0 4 0 0 0 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 4 0 3 0 3
0 0 4 0 4 0 3 0
0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0
0 0 7 0 0 0 0 0
0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0
```

## Project the Top Markers Down Their Columns (`easy_143_project_top_markers_down_columns`)

**Difficulty:** easy

**Skills:** column projection, header interpretation, same-size abstraction


**Scaffold notes:**
- Only the top row matters.
- Every nonzero top-row marker paints its whole column.
- Columns whose top cell is zero stay empty.

**Written solution:** Read the top row as a set of column colors. For each nonzero top-row cell, fill the entire column with that color and leave all other columns as zero.

**Program solution (Python reference):**
```python
def solve_easy_143_project_top_markers_down_columns(g):
    h, w = dims(g)
    out = zeros(h, w)
    for c in range(w):
        color = g[0][c]
        if color != 0:
            for r in range(h):
                out[r][c] = color
    return out
```

**Train 1 input**
```text
0 2 0 0 5 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
0 2 0 0 5 0 0 8 0
```

**Train 2 input**
```text
6 0 0 4 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 0 4 0 0 0 0 0 7
6 0 0 4 0 0 0 0 0 7
6 0 0 4 0 0 0 0 0 7
6 0 0 4 0 0 0 0 0 7
6 0 0 4 0 0 0 0 0 7
6 0 0 4 0 0 0 0 0 7
```

**Train 3 input**
```text
0 0 3 0 0 9 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
0 0 3 0 0 9 0 0
```

**Train 4 input**
```text
0 1 0 0 0 0 2 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
0 1 0 0 0 0 2 0 4 0 0
```

**Test input**
```text
5 0 0 0 2 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
5 0 0 0 2 0 0 6 0 0
```

## Reduce the Solid 3x3 Blocks to Their Centers (`easy_144_reduce_solid_3x3_blocks_to_centers`)

**Difficulty:** easy

**Skills:** object reduction, solid block detection, same-size output


**Scaffold notes:**
- Find the fully filled 3x3 monochrome squares.
- Everything disappears except the center of each square.
- The center keeps the square's color.

**Written solution:** Scan for nonzero 3x3 windows that are completely filled with one color. In the output, keep only the center cell of each such block.

**Program solution (Python reference):**
```python
def solve_easy_144_reduce_solid_3x3_blocks_to_centers(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h - 2):
        for c in range(w - 2):
            color = g[r][c]
            if color == 0:
                continue
            ok = True
            for rr in range(r, r + 3):
                for cc in range(c, c + 3):
                    if g[rr][cc] != color:
                        ok = False
            if ok:
                out[r + 1][c + 1] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 4 4 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 6 6 6 0
8 8 8 0 0 0 0 6 6 6 0
8 8 8 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 2 2 2 0
5 5 5 0 0 0 0 0 2 2 2 0
5 5 5 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
4 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0
0 0 0 0 7 7 7 0 0
0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Mirror the Left Half Across the Divider (`easy_145_mirror_left_half_across_divider`)

**Difficulty:** easy

**Skills:** mirror symmetry, divider semantics, same-size copying


**Scaffold notes:**
- The vertical line of 8s is a mirror divider.
- Only the left side contains the pattern to copy.
- Reflect every left-side nonzero cell to the matching place on the right.

**Written solution:** Treat the column of 8s as a mirror axis. Copy every nonzero cell from the left half to the reflected location on the right half, keeping the divider unchanged.

**Program solution (Python reference):**
```python
def solve_easy_145_mirror_left_half_across_divider(g):
    h, w = dims(g)
    mid = w // 2
    out = clone(g)
    for r in range(h):
        for c in range(mid):
            v = g[r][c]
            if v != 0 and v != 8:
                out[r][w - 1 - c] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 8 0 0 0 0
0 2 0 0 8 0 0 0 0
5 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 7 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 8 0 0 0 0
0 2 0 0 8 0 0 2 0
5 0 0 0 8 0 0 0 5
0 0 0 0 8 0 0 0 0
0 0 7 0 8 0 7 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
```

**Train 2 input**
```text
4 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 6 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 3 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Train 2 output**
```text
4 0 0 0 0 8 0 0 0 0 4
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 6 8 6 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 3 0 0 8 0 0 3 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 6 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 2 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
9 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 6 0 0 0 0 8 0 0 0 0 6 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 2 0 8 0 2 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
9 0 0 0 0 0 8 0 0 0 0 0 9
0 0 0 0 0 0 8 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 7 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 5 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
4 0 0 0 8 0 0 0 0
```

**Train 4 output**
```text
0 0 7 0 8 0 7 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 5 0 0 8 0 0 5 0
0 0 0 0 8 0 0 0 0
4 0 0 0 8 0 0 0 4
```

**Test input**
```text
0 0 0 0 0 8 0 0 0 0 0
3 0 0 0 0 8 0 0 0 0 0
0 0 0 6 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 2 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 8 0 0 0 0 0
3 0 0 0 0 8 0 0 0 0 3
0 0 0 6 0 8 0 6 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 2 8 2 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

## Outline Rectangles from Diagonal Corner Pairs (`easy_146_outline_rectangles_from_diagonal_corner_pairs`)

**Difficulty:** easy

**Skills:** sparse geometry, rectangle inference, same-size construction


**Scaffold notes:**
- Each color appears as a pair of opposite corners.
- Use those two corners to infer the rectangle.
- Draw only the border, not the filled interior.

**Written solution:** For every color, take its two marked cells as opposite corners of a rectangle and draw that rectangle's border in the same color.

**Program solution (Python reference):**
```python
def solve_easy_146_outline_rectangles_from_diagonal_corner_pairs(g):
    h, w = dims(g)
    out = zeros(h, w)
    positions = {}
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                positions.setdefault(v, []).append((r, c))
    for color, cells in positions.items():
        if len(cells) != 2:
            continue
        (r0, c0), (r1, c1) = cells
        r0, r1 = sorted((r0, r1))
        c0, c1 = sorted((c0, c1))
        for c in range(c0, c1 + 1):
            out[r0][c] = color
            out[r1][c] = color
        for r in range(r0, r1 + 1):
            out[r][c0] = color
            out[r][c1] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 4 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 4 4 4
0 2 2 2 2 2 0 4 0 4
0 2 0 0 0 2 0 4 0 4
0 2 0 0 0 2 0 4 0 4
0 2 2 2 2 2 0 4 0 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3
6 6 6 6 0 3 0 0 3
6 0 0 6 0 3 0 0 3
6 0 0 6 0 3 0 0 3
6 0 0 6 0 3 3 3 3
6 0 0 6 0 0 0 0 0
6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
```

**Train 3 output**
```text
5 5 5 5 5 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 0 0 0 0
5 0 0 0 5 0 0 0 7 7 7 7
5 5 5 5 5 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 7 7 7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4
```

**Test output**
```text
0 2 2 2 2 2 2 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 2 0 4 4 4
0 2 0 0 0 0 2 0 4 0 4
0 2 2 2 2 2 2 0 4 0 4
0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 4 4 4
```

## Bridge the One-Cell Vertical Gaps (`easy_147_bridge_one_cell_vertical_gaps`)

**Difficulty:** easy

**Skills:** local completion, vertical pattern detection, same-size transform


**Scaffold notes:**
- Look for a zero cell sandwiched between two equal colors in the same column.
- Only one-cell vertical gaps are bridged.
- Everything else stays unchanged.

**Written solution:** Whenever a zero cell has the same nonzero color directly above and below it, fill the middle cell with that color.

**Program solution (Python reference):**
```python
def solve_easy_147_bridge_one_cell_vertical_gaps(g):
    h, w = dims(g)
    out = clone(g)
    for r in range(1, h - 1):
        for c in range(w):
            if g[r][c] == 0 and g[r - 1][c] == g[r + 1][c] and g[r - 1][c] != 0:
                out[r][c] = g[r - 1][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 5 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 2 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 5 0
0 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 2 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 6 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
4 0 0 0 0 8 0 0 0 0
4 0 0 0 0 8 0 0 6 0
4 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
```

**Train 3 output**
```text
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 5 0 0 0 4 0 0 0
0 0 0 5 0 0 0 4 0 0 0
0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0
```

## Select the Legend-Matched Object and Rotate It Clockwise (`medium_141_select_legend_object_and_rotate_clockwise`)

**Difficulty:** medium

**Skills:** legend decoding, object selection, rotation, cropped output


**Scaffold notes:**
- The top-left cell is a color legend.
- Find the object whose color matches that legend.
- Crop that object and rotate it 90 degrees clockwise.

**Written solution:** Read the top-left cell as the target color. Find the connected object of that color, crop its bounding box, and rotate that crop clockwise.

**Program solution (Python reference):**
```python
def solve_medium_141_select_legend_object_and_rotate_clockwise(g):
    target_color = g[0][0]
    ignore = {(0, 0)}
    comps = connected_components(g, colors={target_color}, ignore_positions=ignore)
    comp = max(comps, key=len)
    obj = component_grid(g, comp)
    return rot90(obj)
```

**Train 1 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 2 0 0 0 0 0 4 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 4
4 4
0 4
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2
0 0 3 3 3 0 0 0 0 2 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6
6 6 6
6 0 0
```

**Train 3 input**
```text
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0 0 0
0 5 5 0 0 0 0 7 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7
0 7
0 7
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0 0
0 7 0 0 0 4 4 4 0 0
0 7 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 2
2 0 2
2 0 0
```

**Test input**
```text
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
3 3
0 3
0 3
```

## Fill the Intersections Chosen by the Headers (`medium_142_fill_header_selected_intersections`)

**Difficulty:** medium

**Skills:** header decoding, row/column selection, intersection construction


**Scaffold notes:**
- The first row chooses columns and the first column chooses rows.
- Only marked rows and marked columns matter.
- Fill their crossings with a new color.

**Written solution:** Treat 2s in the top row as active columns and 3s in the first column as active rows. Fill every active row/column intersection with color 5, keeping the headers unchanged.

**Program solution (Python reference):**
```python
def solve_medium_142_fill_header_selected_intersections(g):
    h, w = dims(g)
    out = clone(g)
    active_rows = [r for r in range(1, h) if g[r][0] == 3]
    active_cols = [c for c in range(1, w) if g[0][c] == 2]
    for r in active_rows:
        for c in active_cols:
            out[r][c] = 5
    return out
```

**Train 1 input**
```text
8 2 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0
3 5 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 5 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0
3 5 0 0 5 0 5 0 0
```

**Train 2 input**
```text
8 0 2 0 0 2 0 0 0 2
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 2 0 0 2 0 0 0 2
3 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 5 0 0 0 5
```

**Train 3 input**
```text
8 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 2 0 2 0 2 0 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
3 5 0 5 0 5 0 5
```

**Train 4 input**
```text
8 0 2 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 2 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 5 0 0 0 5 0 5 0 0
```

**Test input**
```text
8 0 0 2 2 0 0 0 2 2
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 0 0 2 2 0 0 0 2 2
3 0 0 5 5 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 5 5 0 0 0 5 5
3 0 0 5 5 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0
```

## Apply Downward Gravity in the Walled Column Segments (`medium_143_apply_downward_gravity_in_walled_columns`)

**Difficulty:** medium

**Skills:** segmented gravity, wall semantics, order preservation


**Scaffold notes:**
- Walls are 8s and they split a column into independent segments.
- Within each segment, colored cells fall downward.
- The order of falling cells is preserved.

**Written solution:** Process each column separately. Between walls, collect the nonzero colored cells and drop them to the bottom of that segment while preserving their top-to-bottom order.

**Program solution (Python reference):**
```python
def solve_medium_143_apply_downward_gravity_in_walled_columns(g):
    h, w = dims(g)
    out = clone(g)
    for c in range(w):
        start = 0
        while start < h:
            end = start
            while end < h and g[end][c] != 8:
                end += 1
            vals = [g[r][c] for r in range(start, end) if g[r][c] not in (0, 8)]
            for r in range(start, end):
                out[r][c] = 0
            for i, v in enumerate(reversed(vals)):
                out[end - 1 - i][c] = v
            if end < h:
                out[end][c] = 8
            start = end + 1
    return out
```

**Train 1 input**
```text
0 2 0 0 0 0 4 0
0 0 0 0 3 0 0 0
0 5 0 0 0 0 8 0
0 8 0 0 7 0 0 0
0 0 0 0 8 0 0 0
0 0 0 0 0 0 6 0
0 8 0 0 0 0 0 0
0 0 0 0 8 0 2 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0
0 5 0 0 3 0 8 0
0 8 0 0 7 0 0 0
0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 8 0 6 0
0 0 0 0 0 0 2 0
```

**Train 2 input**
```text
9 0 0 4 0 0 0
0 0 0 0 0 7 0
2 0 0 0 0 0 0
0 0 0 8 0 6 0
8 0 0 0 0 0 0
0 0 0 0 0 8 0
0 0 0 5 0 0 0
8 0 0 0 0 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
9 0 0 4 0 0 0
2 0 0 8 0 7 0
8 0 0 0 0 6 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
8 0 0 5 0 0 0
0 0 0 8 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 3 0 0 0 0 6 0
0 0 0 0 0 0 0 8 0
0 0 8 0 5 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 4 0 8 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 9 0 0 8 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 6 0
0 0 3 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 4 0 8 0 0 0 0
0 0 8 0 0 0 0 2 0
0 0 0 0 0 0 0 8 0
0 0 0 0 9 0 0 0 0
```

**Train 4 input**
```text
0 4 0 0 0 7 0 0 3
0 0 0 0 0 2 0 0 0
0 6 0 0 0 0 0 0 8
0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 9
0 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 3
0 6 0 0 0 7 0 0 8
0 8 0 0 0 2 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
```

**Test input**
```text
9 0 5 0 0 0 7 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
4 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0
8 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 8 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 0 0 0 7 0
9 0 2 0 0 0 8 0
4 0 8 0 0 0 0 0
8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 8 0 0 0 3 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```

## Crop the Horizontally Symmetric Object (`medium_144_crop_the_horizontally_symmetric_object`)

**Difficulty:** medium

**Skills:** symmetry detection, object selection, cropped output


**Scaffold notes:**
- There are several disconnected objects.
- Only one object's shape matches its own left-right mirror.
- Crop and return that object.

**Written solution:** Find the connected component whose binary shape is horizontally symmetric. Return the cropped bounding box of that object.

**Program solution (Python reference):**
```python
def solve_medium_144_crop_the_horizontally_symmetric_object(g):
    comps = connected_components(g)
    for comp in comps:
        obj = component_grid(g, comp)
        bin_obj = [[1 if v != 0 else 0 for v in row] for row in obj]
        if bin_obj == hflip(bin_obj):
            return obj
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 5 0 5 0 0 0
0 2 2 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
5 0 5
5 5 5
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 6 0 2 2 0
0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6
0 6 0
0 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 8 0 8 0 0 0
0 0 0 4 4 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 8
8 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
7 7 7
0 7 0
0 7 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 6 0 6 0 0
0 3 3 3 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 0 6
6 6 6
```

## Fill the Holes in the Ring Components (`medium_145_fill_holes_in_ring_components`)

**Difficulty:** medium

**Skills:** topology, hole filling, same-size transform


**Scaffold notes:**
- The nonzero objects are hollow rectangular rings.
- The border of each ring stays the same.
- Only the enclosed zero hole is filled.

**Written solution:** For each hollow ring, fill the interior hole with the ring's own color while leaving the rest of the grid unchanged.

**Program solution (Python reference):**
```python
def solve_medium_145_fill_holes_in_ring_components(g):
    out = clone(g)
    comps = connected_components(g)
    for comp in comps:
        obj = component_grid(g, comp)
        holes = find_holes_in_component([[1 if v != 0 else 0 for v in row] for row in obj])
        if not holes:
            continue
        color = next(v for row in obj for v in row if v != 0)
        r0, c0, _, _ = bbox(comp)
        for rr, cc in holes:
            out[r0 + rr][c0 + cc] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 5 5 5 5 0
0 2 0 0 2 0 0 5 0 0 5 0
0 2 2 2 2 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 2 2 2 2 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 3 0 0 0 3 0 0 0 0
0 3 0 0 0 3 0 0 0 0
0 3 0 0 0 3 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 7 7 7 7 7 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 0 4 4 4 4
```

**Train 3 output**
```text
0 0 7 7 7 7 7 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 4 4 4 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Decode the Transform and Recolor from the Control Strip (`medium_146_decode_transform_and_recolor_from_control_strip`)

**Difficulty:** medium

**Skills:** control codes, transform decoding, recoloring, cropped output


**Scaffold notes:**
- The first control cell picks a transform.
- The second control cell gives the output color.
- Apply the transform to the prototype object, then recolor it.

**Written solution:** Read the first-row controls as a transform code and an output color. Crop the prototype object, apply the requested transform, and recolor every nonzero cell to the new color.

**Program solution (Python reference):**
```python
def solve_medium_146_decode_transform_and_recolor_from_control_strip(g):
    tcode = g[0][0]
    out_color = g[0][1]
    ignore = {(0, 0), (0, 1)}
    comps = connected_components(g, ignore_positions=ignore)
    comp = max(comps, key=len)
    obj = component_grid(g, comp)
    obj_bin = [[1 if v != 0 else 0 for v in row] for row in obj]
    transformed = apply_transform(obj_bin, tcode)
    return recolor_nonzero(transformed, out_color)
```

**Train 1 input**
```text
4 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2
2 0 0
```

**Train 2 input**
```text
2 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 7 7
0 7 0
7 7 0
```

**Train 3 input**
```text
3 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 0
4 4 4
```

**Train 4 input**
```text
1 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 0 0
6 6 0
0 6 6
```

**Test input**
```text
4 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 5 5
5 0 5
5 0 0
```

## Fill Each Walled Chamber from Its Seed (`medium_147_fill_each_walled_chamber_from_its_seed`)

**Difficulty:** medium

**Skills:** chamber flood fill, wall parsing, region propagation


**Scaffold notes:**
- Walls are 8s and divide the board into chambers.
- Each chamber contains exactly one nonzero seed color.
- Flood that chamber with its seed's color.

**Written solution:** Find each connected non-wall chamber. Read the single nonzero seed color inside it and fill the entire chamber with that color.

**Program solution (Python reference):**
```python
def solve_medium_147_fill_each_walled_chamber_from_its_seed(g):
    h, w = dims(g)
    out = clone(g)
    regions = flood_regions_nonwall(g, wall=8)
    for reg in regions:
        seed_colors = sorted({g[r][c] for r, c in reg if g[r][c] not in (0, 8)})
        if len(seed_colors) != 1:
            continue
        color = seed_colors[0]
        for r, c in reg:
            out[r][c] = color
    return out
```

**Train 1 input**
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 2 0 0 8 0 4 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 6 0 0 8 0 9 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 4 4 4 4 8
8 2 2 2 2 8 4 4 4 4 8
8 2 2 2 2 8 4 4 4 4 8
8 8 8 8 8 8 8 8 8 8 8
8 6 6 6 6 8 9 9 9 9 8
8 6 6 6 6 8 9 9 9 9 8
8 6 6 6 6 8 9 9 9 9 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
8 8 8 8 8 8 8 8 8 8
8 0 3 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 7 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 3 3 3 8
8 3 3 3 3 3 3 3 3 8
8 8 8 8 8 8 8 8 8 8
8 7 7 7 7 7 7 7 7 8
8 7 7 7 7 7 7 7 7 8
8 7 7 7 7 7 7 7 7 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 5 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 2 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 6 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 5 5 5 8 2 2 2 8 6 6 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 8
8 0 0 0 4 0 0 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 8
8 0 0 7 0 0 0 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
8 8 8 8 8 8 8 8 8
8 4 4 4 4 4 4 4 8
8 4 4 4 4 4 4 4 8
8 4 4 4 4 4 4 4 8
8 8 8 8 8 8 8 8 8
8 7 7 7 7 7 7 7 8
8 7 7 7 7 7 7 7 8
8 7 7 7 7 7 7 7 8
8 8 8 8 8 8 8 8 8
```

**Test input**
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 3 0 0 8 0 6 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 9 0 0 8 0 2 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 8 6 6 6 6 8
8 3 3 3 3 8 6 6 6 6 8
8 3 3 3 3 8 6 6 6 6 8
8 8 8 8 8 8 8 8 8 8 8
8 9 9 9 9 8 2 2 2 2 8
8 9 9 9 9 8 2 2 2 2 8
8 9 9 9 9 8 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8
```

## Decode the Dual-Code Library and Center-Stamp the Result (`hard_141_decode_dual_code_library_and_center_stamp`)

**Difficulty:** hard

**Skills:** library lookup, transform decoding, recoloring, centered stamping


**Scaffold notes:**
- The first control cell chooses a prototype by color.
- The second control cell chooses a transform and the third chooses the output color.
- Find the framed canvas and center the transformed, recolored prototype inside it.

**Written solution:** Read the top control strip as prototype color, transform code, and output color. Find the matching prototype object in the library, apply the transform, recolor it, then place it centered inside the 8-framed canvas and return the cropped frame region.

**Program solution (Python reference):**
```python
def solve_hard_141_decode_dual_code_library_and_center_stamp(g):
    proto_color = g[0][0]
    tcode = g[0][1]
    out_color = g[0][2]
    ignore = {(0, 0), (0, 1), (0, 2)}
    wall_comps = connected_components(g, colors={8}, ignore_positions=ignore)
    frame = max(wall_comps, key=len)
    frame_box = bbox(frame)
    frame_grid = crop_bbox(g, frame_box)
    ignore |= set(frame)
    proto_comps = connected_components(g, colors={proto_color}, ignore_positions=ignore)
    proto = component_grid(g, max(proto_comps, key=len))
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    transformed = recolor_nonzero(apply_transform(proto_bin, tcode), out_color)
    return centered_stamp_on_canvas(frame_grid, transformed)
```

**Train 1 input**
```text
2 4 6 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 3 3 0 0 5 5 0 0 0
0 2 0 0 0 0 3 0 0 0 0 0 5 5 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
```

**Train 1 output**
```text
8 8 8 8 8 8 8
8 0 0 0 0 0 8
8 0 6 6 6 0 8
8 0 6 0 0 0 8
8 0 0 0 0 0 8
8 8 8 8 8 8 8
```

**Train 2 input**
```text
5 2 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 2 2 2 0
0 0 4 0 0 0 5 0 0 0 0 0 2 0 0
0 0 4 4 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
```

**Train 2 output**
```text
8 8 8 8 8 8 8
8 0 0 0 7 0 8
8 0 0 7 7 0 8
8 0 7 7 0 0 8
8 0 0 0 0 0 8
8 8 8 8 8 8 8
```

**Train 3 input**
```text
3 3 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 3 0 0 0 0 0 7 7 7 0 0
0 6 6 0 0 0 3 3 3 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
```

**Train 3 output**
```text
8 8 8 8 8 8 8
8 0 4 4 4 0 8
8 0 4 0 0 0 8
8 0 4 4 0 0 8
8 0 0 0 0 0 8
8 8 8 8 8 8 8
```

**Train 4 input**
```text
7 1 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 4 0 0 0 0 0 0 0 0
0 0 7 7 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
```

**Train 4 output**
```text
8 8 8 8 8 8 8
8 0 0 0 0 0 8
8 0 2 2 0 0 8
8 0 0 2 2 0 8
8 0 0 0 0 0 8
8 8 8 8 8 8 8
```

**Test input**
```text
4 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 2 2 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 2 2 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
```

**Test output**
```text
8 8 8 8 8 8 8
8 0 5 5 0 0 8
8 0 0 5 0 0 8
8 0 0 5 0 0 8
8 0 0 0 0 0 8
8 8 8 8 8 8 8
```

## Build the Dihedral Equivalence Matrix (`hard_142_build_dihedral_equivalence_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, dihedral reasoning, relation matrix construction


**Scaffold notes:**
- Each disconnected object is one item in the relation set.
- Two objects are related when one can be rotated or mirrored to match the other.
- Write the all-pairs relation matrix.

**Written solution:** Sort the disconnected objects by reading order. Compare every pair of binary shapes up to rotation and reflection, and place color 2 in the matrix where they are dihedrally equivalent.

**Program solution (Python reference):**
```python
def solve_hard_142_build_dihedral_equivalence_matrix(g):
    comps = connected_components(g)
    comps = sorted(comps, key=lambda comp: bbox(comp)[:2])
    norms = []
    for comp in comps:
        obj = component_grid(g, comp)
        norms.append([[1 if v != 0 else 0 for v in row] for row in obj])
    n = len(norms)
    out = zeros(n, n)
    for i in range(n):
        variants = dihedral_variants(norms[i])
        for j in range(n):
            if any(variants_k == norms[j] for variants_k in variants):
                out[i][j] = 2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 4 4 4 0 0 0
0 2 0 0 0 0 0 0 4 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 3 3 0 0 0
0 0 6 6 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0
2 2 0 0
0 0 2 2
0 0 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 5 5 5 0 0
0 2 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 4 0 0 0 0
0 0 0 7 0 0 0 0 0 0 4 4 0 0 0
0 0 0 7 7 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 0 0
2 2 0 0
0 0 2 0
0 0 0 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 6 0 6 0 0
0 0 0 3 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 9 9 9 0 0
0 2 0 0 0 0 0 0 0 0 0 9 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 0 0 0
0 2 0 0
0 0 2 2
0 0 2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 7 7 0 0
0 0 5 5 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 2 0 0 0 0 0 0 0 4 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 0 0
2 2 0 0
0 0 2 2
0 0 2 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 5 0 0
0 0 3 0 0 0 0 0 0 0 5 5 5 0 0
0 0 3 3 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 2 2 0 0 0
0 0 7 0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 0 0
2 2 0 0
0 0 2 0
0 0 0 2
```

## Overlay the Diagonal Visibility Counts with Walls (`hard_143_overlay_diagonal_visibility_counts_with_walls`)

**Difficulty:** hard

**Skills:** diagonal ray casting, count maps, wall blocking


**Scaffold notes:**
- Each emitter sends rays along the four diagonals.
- Rays stop when they hit a wall or the edge.
- Count how many rays visit each cell.

**Written solution:** From every emitter, trace all four diagonal directions until a wall or the border stops the ray. The output cell value is the number of rays that pass through that cell, while walls stay as 8.

**Program solution (Python reference):**
```python
def solve_hard_143_overlay_diagonal_visibility_counts_with_walls(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 8:
                out[r][c] = 8
    emitters = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in emitters:
        out[r][c] = min(9, (0 if out[r][c] == 8 else out[r][c]) + 1)
        for dr, dc in ((1,1), (1,-1), (-1,1), (-1,-1)):
            rr, cc = r + dr, c + dc
            while 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 8:
                if out[rr][cc] != 8:
                    out[rr][cc] = min(9, out[rr][cc] + 1)
                rr += dr
                cc += dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 8 0 0 0 0
0 0 0 0 8 0 0 2 0
0 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
1 0 1 0 0 1 0 0 0
0 1 0 0 8 0 1 0 1
1 0 1 0 8 0 0 1 0
0 0 0 1 8 0 1 0 1
0 0 8 8 8 8 8 0 0
1 0 0 0 1 0 0 0 0
0 1 0 1 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 8 0 0 0
0 0 0 2 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
8 0 8 0 8 0 8 0 8 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 2 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
1 0 0 0 0 0 1 1 0 1
0 1 0 0 0 1 0 0 1 0
0 0 1 0 1 0 8 1 0 1
0 0 0 1 0 0 8 0 0 0
0 0 1 0 1 0 8 0 0 0
8 1 8 0 8 1 8 0 8 0
1 0 0 1 0 0 8 0 0 0
1 0 1 0 0 0 8 0 0 0
0 1 0 0 0 0 8 0 0 0
1 0 1 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 8 0 0 0 0 0
0 2 0 0 0 8 0 0 0 2 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 2 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Train 3 output**
```text
1 0 1 0 0 8 0 0 1 0 1
0 1 0 0 0 8 0 0 0 1 0
1 0 1 0 0 8 0 0 1 0 1
0 0 0 1 0 8 0 1 0 0 0
0 0 0 0 1 8 1 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 1 8 8 8 8 8 8
0 0 0 1 0 8 0 0 0 0 0
1 0 1 0 0 8 0 0 0 0 0
0 1 0 0 0 8 0 0 0 0 0
1 0 1 0 0 8 0 0 0 0 0
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 4 output**
```text
1 0 0 0 0 0 0 0 8 0 0 0
0 1 0 0 0 0 0 0 8 0 0 0
1 0 1 0 0 0 0 0 8 0 0 0
0 1 8 8 8 8 8 8 8 8 0 0
0 0 1 0 1 0 0 0 8 0 0 0
0 0 0 1 0 0 0 0 0 1 0 0
0 0 1 0 1 0 0 0 0 0 1 0
0 1 0 0 0 1 0 0 0 0 0 1
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 2 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
8 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 2 0 0 8 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
1 0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 8 0 0 1 0 1
1 0 1 0 0 8 0 0 0 1 0
0 0 0 1 0 8 0 0 1 0 1
0 0 0 0 1 8 0 1 0 0 0
0 0 0 0 0 8 2 0 0 0 0
8 8 8 8 8 8 8 1 0 0 0
0 1 0 1 0 8 0 0 1 0 1
0 0 1 0 0 8 0 0 0 1 0
0 1 0 1 0 0 0 0 1 0 1
```

## Build the Transform × Recolor Gallery (`hard_144_build_transform_recolor_gallery`)

**Difficulty:** hard

**Skills:** cross-product construction, control headers, panel layout, shape transforms


**Scaffold notes:**
- The top header chooses transforms and the left header chooses colors.
- There is one prototype object elsewhere in the input.
- Build a gallery whose rows follow the colors and whose columns follow the transforms.

**Written solution:** Crop the prototype, treat the top row as transform codes and the left column as row colors, then build the full gallery of transformed and recolored copies with one blank separator between panels.

**Program solution (Python reference):**
```python
def solve_hard_144_build_transform_recolor_gallery(g):
    h, w = dims(g)
    tcols = [c for c in range(1, w) if g[0][c] != 0]
    rrows = [r for r in range(1, h) if g[r][0] != 0]
    transforms = [g[0][c] for c in tcols]
    colors = [g[r][0] for r in rrows]
    ignore = {(0, c) for c in tcols} | {(r, 0) for r in rrows}
    comps = connected_components(g, ignore_positions=ignore)
    proto = component_grid(g, max(comps, key=len))
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    ph, pw = dims(proto_bin)
    out = zeros(len(colors) * ph + (len(colors) - 1), len(transforms) * pw + (len(transforms) - 1))
    for i, color in enumerate(colors):
        for j, tcode in enumerate(transforms):
            tile = recolor_nonzero(apply_transform(proto_bin, tcode), color)
            top = i * (ph + 1)
            left = j * (pw + 1)
            stamp(out, tile, top, left)
    return out
```

**Train 1 input**
```text
0 1 2 4 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 0 2 2 0 2 2 2
2 0 0 0 0 0 2 0 2 0 2
2 2 2 0 2 2 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 0 0 0 5 5 0 5 5 5
5 0 0 0 0 0 5 0 5 0 5
5 5 5 0 5 5 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 7 7 0 7 7 7
7 0 0 0 0 0 7 0 7 0 7
7 7 7 0 7 7 7 0 7 0 0
```

**Train 2 input**
```text
0 4 1 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 0 3 3 0
3 3 3 0 0 3 0
3 0 0 0 0 3 3
0 0 0 0 0 0 0
0 0 6 0 6 6 0
6 6 6 0 0 6 0
6 0 0 0 0 6 6
0 0 0 0 0 0 0
0 0 9 0 9 9 0
9 9 9 0 0 9 0
9 0 0 0 0 9 9
```

**Train 3 input**
```text
0 2 3 1 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 4 0 0 4 4 0 4 0 0
0 4 4 0 4 4 0 0 4 4 0
4 4 0 0 4 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 7 0 7 0 0
0 7 7 0 7 7 0 0 7 7 0
7 7 0 0 7 0 0 0 0 7 7
```

**Train 4 input**
```text
0 1 4 2 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 2 0 2 2 0 0 2 2 2
2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 0 2 0 0 0 0 0
8 8 8 0 8 8 0 0 8 8 8
8 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 8 0 0 0 0 0
6 6 6 0 6 6 0 0 6 6 6
6 0 0 0 0 6 0 0 0 0 6
```

**Test input**
```text
0 3 1 2 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 5 5 0 5 5 0 0 0 5 5
5 0 0 0 5 0 0 0 0 0 5
5 5 0 0 5 5 5 0 5 5 5
0 0 0 0 0 0 0 0 0 0 0
9 9 9 0 9 9 0 0 0 9 9
9 0 0 0 9 0 0 0 0 0 9
9 9 0 0 9 9 9 0 9 9 9
```

## Fill the Chambers by the Seed Priority Legend (`hard_145_fill_chambers_by_seed_priority_legend`)

**Difficulty:** hard

**Skills:** legend priority, regional reasoning, wall parsing, decision by set membership


**Scaffold notes:**
- The top row gives a priority order of colors.
- A chamber may contain several seed colors.
- Each chamber is filled with the highest-priority seed color present in it.

**Written solution:** Read the first row as a color-priority legend from left to right. For each chamber below the legend, collect the seed colors in that chamber and fill the chamber with the highest-priority one.

**Program solution (Python reference):**
```python
def solve_hard_145_fill_chambers_by_seed_priority_legend(g):
    priority = [v for v in g[0] if v not in (0, 8)]
    rank = {color: i for i, color in enumerate(priority)}
    h, w = dims(g)
    out = clone(g)
    regions = flood_regions_nonwall(g, wall=8, row_start=1)
    for reg in regions:
        colors = sorted({g[r][c] for r, c in reg if g[r][c] not in (0, 8)}, key=lambda v: rank[v])
        if not colors:
            continue
        fill = colors[0]
        for r, c in reg:
            out[r][c] = fill
    return out
```

**Train 1 input**
```text
2 4 6 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 0 4 6 0 8 0 6 2 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 6 4 0 8 0 2 4 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
2 4 6 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 4 4 4 4 8 2 2 2 2 8
8 4 4 4 4 8 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8
8 4 4 4 4 8 2 2 2 2 8
8 4 4 4 4 8 2 2 2 2 8
8 4 4 4 4 8 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
5 3 7 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8
8 0 7 0 0 0 3 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
8 0 5 0 0 0 7 0 0 8
8 0 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
5 3 7 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 3 3 3 8
8 3 3 3 3 3 3 3 3 8
8 8 8 8 8 8 8 8 8 8
8 5 5 5 5 5 5 5 5 8
8 5 5 5 5 5 5 5 5 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
9 2 4 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8
8 0 4 0 8 0 2 0 8 2 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 9 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 4 0 8 0 0 8
8 0 0 0 8 0 0 0 8 9 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
9 2 4 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 9 9 9 8 2 2 2 8 9 9 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
3 6 2 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
8 0 6 0 0 0 2 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 8
8 0 3 0 0 0 6 0 8
8 0 0 0 0 0 0 0 8
8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
3 6 2 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
8 6 6 6 6 6 6 6 8
8 6 6 6 6 6 6 6 8
8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 3 3 8
8 3 3 3 3 3 3 3 8
8 3 3 3 3 3 3 3 8
8 8 8 8 8 8 8 8 8
```

**Test input**
```text
4 7 2 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 0 7 0 0 8 0 4 0 0 8
8 0 2 0 0 8 0 7 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 2 0 0 8 0 7 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
4 7 2 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 7 7 7 7 8 4 4 4 4 8
8 7 7 7 7 8 4 4 4 4 8
8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 7 7 7 7 8
8 2 2 2 2 8 7 7 7 7 8
8 2 2 2 2 8 7 7 7 7 8
8 8 8 8 8 8 8 8 8 8 8
```

## Select the Object by Border-Touch Signature and Scale It by 2 (`hard_146_select_object_by_border_touch_signature_and_scale2`)

**Difficulty:** hard

**Skills:** border-touch signature, object selection, cropping, scaling


**Scaffold notes:**
- The control strip encodes which borders the target object must touch.
- Different objects touch different subsets of the borders.
- Choose the matching object, crop it, and scale it up by 2.

**Written solution:** Interpret the top-row controls as a required set of touched borders: 1=top, 2=right, 3=bottom, 4=left, with the first data row counting as the top border because row 0 is reserved for controls. Find the object whose bbox touches exactly that set, crop it, and enlarge it by 2 in each direction.

**Program solution (Python reference):**
```python
def solve_hard_146_select_object_by_border_touch_signature_and_scale2(g):
    required = {v for v in g[0] if v in (1, 2, 3, 4)}
    h, w = dims(g)
    ignore = {(0, c) for c in range(w)}
    comps = connected_components(g, ignore_positions=ignore)
    for comp in comps:
        r0, c0, r1, c1 = bbox(comp)
        sig = set()
        if r0 == 1:
            sig.add(1)
        if c1 == w - 1:
            sig.add(2)
        if r1 == h - 1:
            sig.add(3)
        if c0 == 0:
            sig.add(4)
        if sig == required:
            return scale2(component_grid(g, comp))
    return [[0]]
```

**Train 1 input**
```text
1 4 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0
2 2 0 0
2 2 0 0
2 2 0 0
2 2 2 2
2 2 2 2
```

**Train 2 input**
```text
2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0
3 0 0 0 0 0 0 4 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6 6
```

**Train 2 output**
```text
6 6 0 0
6 6 0 0
6 6 0 0
6 6 0 0
6 6 6 6
6 6 6 6
```

**Train 3 input**
```text
3 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 7 7 7 0 2 2 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 5 5 5 0 0
5 5 5 5 0 0
0 0 5 5 0 0
0 0 5 5 0 0
0 0 5 5 5 5
0 0 5 5 5 5
```

**Train 4 input**
```text
1 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
6 6 6 6 0 0
6 6 6 6 0 0
0 0 6 6 6 6
0 0 6 6 6 6
```

**Test input**
```text
1 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
5 5 0 0
5 5 0 0
5 5 0 0
5 5 0 0
5 5 5 5
5 5 5 5
```

## Apply the Transform Sequence and Stamp at the Anchors (`hard_147_apply_transform_sequence_and_stamp_at_anchors`)

**Difficulty:** hard

**Skills:** sequential transforms, anchor-based stamping, recoloring, same-size construction


**Scaffold notes:**
- The first two control cells are a transform sequence.
- There is one prototype object colored 9 and several one-cell anchors of other colors.
- Transform the prototype, recolor it to each anchor's color, and stamp it centered on every anchor.

**Written solution:** Crop the prototype object, apply the two transforms in order, and use the result as a stamp. For each one-cell anchor, recolor the stamp to the anchor's color and place it centered on the anchor in a blank output grid.

**Program solution (Python reference):**
```python
def solve_hard_147_apply_transform_sequence_and_stamp_at_anchors(g):
    code1, code2 = g[0][0], g[0][1]
    h, w = dims(g)
    ignore = {(0, 0), (0, 1)}
    comps = connected_components(g, colors=None, ignore_positions=ignore)
    proto = None
    anchors = []
    for comp in comps:
        colors = {g[r][c] for r, c in comp}
        if len(colors) == 1 and next(iter(colors)) != 9:
            # one-cell anchors of various colors
            if len(comp) == 1:
                anchors.append(comp[0])
                continue
        if 9 in colors:
            proto = component_grid(g, comp)
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    transformed = apply_transform(apply_transform(proto_bin, code1), code2)
    ph, pw = dims(transformed)
    out = zeros(h, w)
    for r, c in anchors:
        color = g[r][c]
        tile = recolor_nonzero(transformed, color)
        top = r - ph // 2
        left = c - pw // 2
        stamp(out, tile, top, left)
    return out
```

**Train 1 input**
```text
2 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 0 6 0 0 0 2 2 2 0 0 0
0 0 0 0 6 0 6 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 7 0
0 0 0 0 0 0 0 4 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
1 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 2 2 0 5 5 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
3 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 3 3 0 0 0 0 6 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
4 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 2 2 0 0 0 5 0 0 0 0 0
0 0 0 2 0 0 0 0 5 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

