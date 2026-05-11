# ARC Puzzle Bank — Nineteenth 21 Puzzles
This nineteenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`127`–`133`) so it follows directly after the eighteenth bundle.
This volume pushes the mechanic mix in a different direction again: horizontal mirroring, rectangle completion, plus growth, column packing, transposition, bbox borders, legend-driven recolors, rotated object selection, equality matrices, chamber gravity, exemplar matching, elbow routing, perimeter ranking, symmetry selection, reflection-equivalence matrices, prototype-library decoding, elbow count maps, legend-priority chamber fills, boolean galleries, dihedral relation matrices, and sequential transform stamping.
It also introduces and reuses a few convenient solver primitives: `marker_equality_matrix`, `legend_priority_fill`, `dihedral_relation_matrix`, and `compose_then_center_stamp`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_nineteenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_nineteenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_nineteenth_21.md` — this human-readable catalog.

## Easy (7)
- `easy_127_complete_horizontal_mirror` — **Complete the Horizontal Mirror**
- `easy_128_fill_rectangle_from_opposite_corners` — **Fill the Rectangle from Opposite Corners**
- `easy_129_expand_singletons_to_radius1_pluses` — **Expand Singletons to Radius-1 Pluses**
- `easy_130_up_pack_each_column_preserving_order` — **Up-Pack Each Column Preserving Order**
- `easy_131_transpose_square_grid` — **Transpose the Square Grid**
- `easy_132_draw_bbox_border_around_nonzero_cells` — **Draw the Bounding-Box Border Around the Nonzero Cells**
- `easy_133_recolor_source_to_target_from_corner_legend` — **Recolor the Source Color to the Target Color from the Corner Legend**

## Medium (7)
- `medium_127_select_legend_object_and_rotate_cw` — **Select the Legend-Matched Object and Rotate It Clockwise**
- `medium_128_build_marker_equality_matrix` — **Build the Marker Equality Matrix**
- `medium_129_apply_upward_gravity_in_each_walled_chamber` — **Apply Upward Gravity in Each Walled Chamber**
- `medium_130_find_exemplar_match_and_recolor` — **Find the Exemplar Match and Recolor It**
- `medium_131_connect_color_pairs_with_clear_elbows` — **Connect the Color Pairs with the Clear Elbow**
- `medium_132_recolor_components_by_perimeter_rank` — **Recolor Components by Perimeter Rank**
- `medium_133_select_vertically_symmetric_object_and_crop` — **Select the Vertically Symmetric Object and Crop It**

## Hard (7)
- `hard_127_build_reflection_equivalence_matrix` — **Build the Reflection Equivalence Matrix**
- `hard_128_decode_prototype_library_with_transform_and_recolor_codes` — **Decode the Prototype Library with Transform and Recolor Codes**
- `hard_129_overlay_elbow_paths_count_map` — **Overlay the Elbow Paths into a Count Map**
- `hard_130_fill_chambers_by_legend_priority` — **Fill Chambers by Legend Priority**
- `hard_131_build_boolean_gallery_union_intersection_xor` — **Build the Boolean Gallery: Union, Intersection, XOR**
- `hard_132_build_dihedral_relation_matrix` — **Build the Dihedral Relation Matrix**
- `hard_133_compose_two_transforms_and_center_stamp` — **Compose Two Transforms and Center the Stamp**

## Complete the Horizontal Mirror (`easy_127_complete_horizontal_mirror`)

**Difficulty:** easy

**Skills:** horizontal symmetry completion, same-size transform, copying structure


**Scaffold notes:**
- Reflect the grid across its horizontal midline.
- Each nonzero cell should also appear in the mirrored row on the other side.
- Keep original cells and add their reflected copies.

**Written solution:** Reflect every nonzero cell across the horizontal axis. For each colored cell, copy the same color to the row equally far from the bottom edge.

**Program solution (Python reference):**
```python
def solve_easy_127_complete_horizontal_mirror(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                out[h-1-r][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 3 0 0 0 0 0
7 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 4 0 0 0 0 0
0 2 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 6 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 6 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 7 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
4 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 4
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 5 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Fill the Rectangle from Opposite Corners (`easy_128_fill_rectangle_from_opposite_corners`)

**Difficulty:** easy

**Skills:** rectangle completion, same-size fill, bounding-box reasoning


**Scaffold notes:**
- The two nonzero cells are opposite corners of one rectangle.
- Use their shared color for the whole target region.
- Fill every cell inside that axis-aligned box.

**Written solution:** Find the bounding box of the two corner markers and fill the entire rectangle with that color.

**Program solution (Python reference):**
```python
def solve_easy_128_fill_rectangle_from_opposite_corners(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return clone(g)
    color=g[cells[0][0]][cells[0][1]]
    r0,c0,r1,c1=bbox(cells)
    out=zeros(len(g), len(g[0]))
    for r in range(r0, r1+1):
        for c in range(c0, c1+1):
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 5 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 5 5 5 0 0
0 5 5 5 5 0 0
0 5 5 5 5 0 0
0 5 5 5 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0
```

## Expand Singletons to Radius-1 Pluses (`easy_129_expand_singletons_to_radius1_pluses`)

**Difficulty:** easy

**Skills:** local growth, same-size transform, cardinal neighbors


**Scaffold notes:**
- Each isolated colored cell becomes the center of a plus.
- Add one cell above, below, left, and right with the same color.
- Clip the plus if it touches the border.

**Written solution:** For every nonzero cell, paint that cell and its four cardinal neighbors with the same color.

**Program solution (Python reference):**
```python
def solve_easy_129_expand_singletons_to_radius1_pluses(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr,dc in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 6 0
0 0 4 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 6 0
```

**Train 3 input**
```text
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 7 7 7 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 2 2 2
0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
3 3 3 0 0 0 0 0
0 3 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 5 0
0 8 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 4 0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0 2 0
```

## Up-Pack Each Column Preserving Order (`easy_130_up_pack_each_column_preserving_order`)

**Difficulty:** easy

**Skills:** column compression, stable ordering, same-size transform


**Scaffold notes:**
- Treat each column independently.
- Move all nonzero values upward as far as possible.
- Keep their top-to-bottom order unchanged within each column.

**Written solution:** Collect the nonzero entries in each column from top to bottom and rewrite them at the top of that same column, leaving zeros underneath.

**Program solution (Python reference):**
```python
def solve_easy_130_up_pack_each_column_preserving_order(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[i][c]=v
    return out
```

**Train 1 input**
```text
0 2 0 0 3 0
4 0 0 5 0 0
0 0 6 0 0 1
7 0 0 8 0 0
0 9 0 0 2 0
3 0 4 0 0 5
```

**Train 1 output**
```text
4 2 6 5 3 1
7 9 4 8 2 5
3 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 2 0 0
3 0 0 4 0
0 5 0 0 6
7 0 8 0 0
0 9 0 1 0
2 0 3 0 4
0 0 0 5 0
```

**Train 2 output**
```text
3 5 2 4 6
7 9 8 1 4
2 0 3 5 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

**Train 3 input**
```text
1 0 0 2 0 0 3
0 4 0 0 5 0 0
6 0 7 0 0 8 0
0 9 0 1 0 0 2
3 0 4 0 5 0 0
0 0 0 6 0 7 0
```

**Train 3 output**
```text
1 4 7 2 5 8 3
6 9 4 1 5 7 2
3 0 0 6 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 2 0 3 0
4 0 5 0 6
0 7 0 8 0
9 0 1 0 2
0 3 0 4 0
```

**Train 4 output**
```text
4 2 5 3 6
9 7 1 8 2
0 3 0 4 0
0 0 0 0 0
0 0 0 0 0
```

**Test input**
```text
0 5 0 0 6 0
7 0 8 0 0 9
0 1 0 2 0 0
3 0 4 0 5 0
0 6 0 7 0 8
9 0 0 1 0 0
```

**Test output**
```text
7 5 8 2 6 9
3 1 4 7 5 8
9 6 0 1 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

## Transpose the Square Grid (`easy_131_transpose_square_grid`)

**Difficulty:** easy

**Skills:** matrix transpose, same-size transform, coordinate swap


**Scaffold notes:**
- Swap rows and columns.
- A cell at row r, column c moves to row c, column r.
- Because the grid is square, the output stays the same size.

**Written solution:** Transpose the square grid by copying each colored cell at (r,c) to (c,r).

**Program solution (Python reference):**
```python
def solve_easy_131_transpose_square_grid(g):
    return transpose_square(g)
```

**Train 1 input**
```text
0 2 0 0 0
0 0 0 4 0
0 0 0 0 0
5 0 0 0 0
0 0 0 0 7
```

**Train 1 output**
```text
0 0 0 5 0
2 0 0 0 0
0 0 0 0 0
0 4 0 0 0
0 0 0 0 7
```

**Train 2 input**
```text
0 0 0 0 0 3
0 0 0 0 0 0
0 6 0 0 0 0
0 0 0 0 2 0
0 0 0 0 0 0
8 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 8
0 0 6 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 2 0 0
3 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0
0 0 4 0 0 0 0
0 0 0 0 0 1 0
0 0 0 0 0 0 0
7 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 5 0 0 0
```

**Train 3 output**
```text
0 0 0 0 7 0 0
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 0 0 0 0 5
0 0 0 0 0 0 0
0 0 1 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 2
0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0
4 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 4
0 9 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 5
2 0 0 0 0
0 0 0 7 0
0 0 0 0 0
0 6 0 0 0
```

**Test output**
```text
0 2 0 0 0
0 0 0 0 6
0 0 0 0 0
0 0 7 0 0
5 0 0 0 0
```

## Draw the Bounding-Box Border Around the Nonzero Cells (`easy_132_draw_bbox_border_around_nonzero_cells`)

**Difficulty:** easy

**Skills:** bounding box, border drawing, same-size transform


**Scaffold notes:**
- Find the smallest box containing all nonzero cells.
- Draw that box's border in cyan(8).
- Keep the original colored cells where they already exist.

**Written solution:** Locate the global nonzero bounding box and add a cyan(8) border around it without erasing the original colored cells.

**Program solution (Python reference):**
```python
def solve_easy_132_draw_bbox_border_around_nonzero_cells(g):
    h,w=dims(g)
    out=clone(g)
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return out
    r0,c0,r1,c1=bbox(cells)
    for c in range(c0, c1+1):
        if out[r0][c]==0: out[r0][c]=8
        if out[r1][c]==0: out[r1][c]=8
    for r in range(r0, r1+1):
        if out[r][c0]==0: out[r][c0]=8
        if out[r][c1]==0: out[r][c1]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 8 8 8 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 5 0 0 0
0 0 8 8 2 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 4 0
0 0 8 0 0 0 0 8 0
0 0 6 0 0 0 0 8 0
0 0 8 0 0 0 0 8 0
0 0 8 0 0 0 0 8 0
0 0 8 8 8 7 8 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 8 8 8 8 8 0 0
0 0 0 8 0 0 0 0 5 0 0
0 0 0 8 0 0 0 0 8 0 0
0 0 0 8 8 7 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 8 8 8 8 8 0
0 8 0 0 0 0 8 0
0 8 0 0 0 0 8 0
0 8 0 0 0 0 3 0
0 8 0 0 0 0 8 0
0 8 8 5 8 8 8 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 8 8 8 8 8 8 8 0 0
0 0 8 0 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 0 4 0 0
0 0 8 0 0 0 0 0 0 8 0 0
0 0 8 8 8 7 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Recolor the Source Color to the Target Color from the Corner Legend (`easy_133_recolor_source_to_target_from_corner_legend`)

**Difficulty:** easy

**Skills:** legend reading, color remapping, same-size transform


**Scaffold notes:**
- The top-left cell gives the source color.
- The top-right cell gives the target color.
- Recolor every body cell of the source color into the target color.

**Written solution:** Read the source color from the top-left corner and the target color from the top-right corner, then replace every matching source-colored body cell with the target color.

**Program solution (Python reference):**
```python
def solve_easy_133_recolor_source_to_target_from_corner_legend(g):
    h,w=dims(g)
    src=g[0][0]
    tgt=g[0][w-1]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if (r,c) not in ((0,0),(0,w-1)) and out[r][c]==src:
                out[r][c]=tgt
    return out
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 7
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 0 0 0 0 0 0 0 0 7
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
5 0 0 0 0 0 0 0 2
0 5 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
4 0 0 0 0 0 0 6
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 0 0 0 0 0 6
0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 0 0 9
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 0 0 0 0 0 0 0 0 9
0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
6 0 0 0 0 0 0 0 0 3
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 0 0 0 0 0 0 0 0 3
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

## Select the Legend-Matched Object and Rotate It Clockwise (`medium_127_select_legend_object_and_rotate_cw`)

**Difficulty:** medium

**Skills:** legend lookup, object selection, rotation, cropping


**Scaffold notes:**
- The top-left corner cell is a legend telling you which object color matters.
- Find the connected object of that color elsewhere in the grid.
- Crop it to its bounding box and rotate it 90 degrees clockwise.

**Written solution:** Read the target color from the top-left legend cell, locate the connected object of that color, crop it, and rotate the crop 90 degrees clockwise.

**Program solution (Python reference):**
```python
def solve_medium_127_select_legend_object_and_rotate_cw(g):
    legend=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    comps=connected_components(gg)
    for cells in comps:
        colors={gg[r][c] for r,c in cells if gg[r][c]!=0}
        if colors=={legend}:
            return rot90(component_grid(gg, cells))
    return [[0]]
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 5 5 5 0 0
0 3 0 0 0 0 0 0 5 0 0 0
0 3 3 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 3
3 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 2 2 0 0 0 0 6 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6
0 6 6
```

**Train 3 input**
```text
5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
5 0 0
5 5 5
```

**Train 4 input**
```text
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 7 7 0 0
0 0 2 0 0 0 0 0 0 7 7 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 0
0 4 4
4 4 0
```

**Test input**
```text
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7
0 7 7
```

## Build the Marker Equality Matrix (`medium_128_build_marker_equality_matrix`)

**Difficulty:** medium

**Skills:** legend strip parsing, matrix construction, equality relation


**Scaffold notes:**
- The top row lists column colors and the left column lists row colors.
- The output is only the interior matrix, without the legends.
- Place a color at an interior cell exactly when its row legend and column legend match.

**Written solution:** Compare each left-column marker with each top-row marker and write that shared color into the output cell only when they are equal.

**Program solution (Python reference):**
```python
def solve_medium_128_build_marker_equality_matrix(g):
    top=g[0][1:]
    left=[row[0] for row in g[1:]]
    out=zeros(len(left), len(top))
    for r,lv in enumerate(left):
        for c,tv in enumerate(top):
            if lv!=0 and lv==tv:
                out[r][c]=lv
    return out
```

**Train 1 input**
```text
0 2 3 2 5 4
4 0 0 0 0 0
2 0 0 0 0 0
5 0 0 0 0 0
3 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 4
2 0 2 0 0
0 0 0 5 0
0 3 0 0 0
```

**Train 2 input**
```text
0 6 1 6 7
7 0 0 0 0
6 0 0 0 0
2 0 0 0 0
1 0 0 0 0
6 0 0 0 0
```

**Train 2 output**
```text
0 0 0 7
6 0 6 0
0 0 0 0
0 1 0 0
6 0 6 0
```

**Train 3 input**
```text
0 3 4 5 3 8
8 0 0 0 0 0
3 0 0 0 0 0
1 0 0 0 0 0
5 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 8
3 0 0 3 0
0 0 0 0 0
0 0 5 0 0
```

**Train 4 input**
```text
0 2 9 4 2 9 6
6 0 0 0 0 0 0
2 0 0 0 0 0 0
4 0 0 0 0 0 0
9 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 6
2 0 0 2 0 0
0 0 4 0 0 0
0 9 0 0 9 0
```

**Test input**
```text
0 5 2 7 5 3
3 0 0 0 0 0
5 0 0 0 0 0
1 0 0 0 0 0
7 0 0 0 0 0
2 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 3
5 0 0 5 0
0 0 0 0 0
0 0 7 0 0
0 2 0 0 0
```

## Apply Upward Gravity in Each Walled Chamber (`medium_129_apply_upward_gravity_in_each_walled_chamber`)

**Difficulty:** medium

**Skills:** chamber parsing, local gravity, same-size transform


**Scaffold notes:**
- Treat color 8 as an immovable wall.
- Each chamber moves its colored cells upward independently.
- Within each chamber column, keep the original top-to-bottom ordering of colors.

**Written solution:** Split the board into chambers separated by wall color 8, then in each chamber compress every column upward while preserving the order of the colored cells in that column.

**Program solution (Python reference):**
```python
def solve_medium_129_apply_upward_gravity_in_each_walled_chamber(g):
    h,w=dims(g)
    out=clone(g)
    chambers=flood_regions_nonwall(g, wall=8)
    for cells in chambers:
        for r,c in cells:
            out[r][c]=0
        cols=sorted({c for r,c in cells})
        for c in cols:
            rows=sorted(r for r,cc in cells if cc==c)
            vals=[g[r][c] for r in rows if g[r][c]!=0]
            for i,r in enumerate(rows):
                out[r][c]=vals[i] if i<len(vals) else 0
    return out
```

**Train 1 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 6 0 8 0 0 8
8 3 0 0 8 0 0 0 8 0 2 8
8 0 0 0 8 0 0 0 8 0 0 8
8 2 0 0 8 5 0 0 8 0 0 8
8 0 4 0 8 0 0 0 8 7 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 3 4 0 8 5 6 0 8 7 2 8
8 2 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 3 0 0 8 0 6 0 0 8
8 0 0 4 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 2 0 0 8
8 0 5 0 0 8 0 0 0 7 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
8 8 8 8 8 8 8 8 8 8 8
8 0 3 4 0 8 0 6 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 5 0 0 8 0 2 0 7 8
8 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 5 0 8 0 0 0 0 8 0 6 8
8 0 0 0 8 0 0 3 0 8 0 0 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 0 0 8 0 2 0 0 8 0 0 8
8 4 0 0 8 0 0 0 0 8 7 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 4 5 0 8 0 2 3 0 8 7 6 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 7 0 0 0 8 0 2 0 0 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 0 0 3 0 8 0 0 0 6 8
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 0 8 0 0 4 0 8
8 0 5 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 7 0 3 0 8 0 2 0 6 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
8 0 5 0 0 0 8 0 0 4 0 8
8 0 0 0 0 0 8 0 0 0 0 8
8 0 0 0 0 0 8 0 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Test input**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 5 0 8 0 0 0 8 0 3 8
8 0 0 0 8 0 2 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 4 0 0 8 0 0 8
8 3 0 0 8 0 0 0 8 6 0 8
8 0 7 0 8 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 3 5 0 8 4 2 0 8 6 3 8
8 0 7 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8
```

## Find the Exemplar Match and Recolor It (`medium_130_find_exemplar_match_and_recolor`)

**Difficulty:** medium

**Skills:** shape matching, cropping, binary comparison, recoloring


**Scaffold notes:**
- The 5×5 panel in the top-left contains the exemplar shape.
- Ignore color and compare only the cropped binary shape.
- Find the matching object elsewhere, crop it, and recolor it to red(2).

**Written solution:** Crop and binarize the top-left exemplar, search for the object elsewhere with the same cropped binary shape, then return that object cropped and recolored to red(2).

**Program solution (Python reference):**
```python
def solve_medium_130_find_exemplar_match_and_recolor(g):
    exemplar=[row[:5] for row in g[:5]]
    target_norm=normalize_binary(exemplar)
    gg=clone(g)
    for r in range(5):
        for c in range(5):
            gg[r][c]=0
    for cells in connected_components(gg):
        if normalize_binary(component_grid(gg, cells))==target_norm:
            return recolor_nonzero(component_grid(gg, cells), 2)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 4 4 0 0 0
0 1 1 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 5 5 5 0
0 0 6 6 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0
2 0
2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 5 5 0
0 0 0 0 0 7 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 2
0 2 0
0 2 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 6 0 6 0 0
0 0 1 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 0
2 2
0 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 5 0 0
0 0 0 0 0 0 8 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 5 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2
2 2
2 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 0 2
2 2 2
```

## Connect the Color Pairs with the Clear Elbow (`medium_131_connect_color_pairs_with_clear_elbows`)

**Difficulty:** medium

**Skills:** path finding, L-shaped routing, obstacle avoidance


**Scaffold notes:**
- Each non-wall color appears exactly twice.
- Try the horizontal-then-vertical elbow first.
- If that route is blocked, use the vertical-then-horizontal elbow instead.

**Written solution:** For each color pair, draw the unique clear L-shaped path between its endpoints, preferring horizontal-then-vertical unless that route hits a blocker.

**Program solution (Python reference):**
```python
def solve_medium_131_connect_color_pairs_with_clear_elbows(g):
    h,w=dims(g)
    out=clone(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v not in (0,8):
                pos.setdefault(v, []).append((r,c))
    for color, pts in pos.items():
        if len(pts)!=2:
            continue
        p1,p2=pts
        path_h=elbow_cells(p1,p2,'h')
        path_v=elbow_cells(p1,p2,'v')
        if path_clear(g, path_h, pts):
            cells=path_h
        else:
            cells=path_v
        for r,c in cells:
            if out[r][c]!=8:
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 8 0 0 0 8 0 0
0 0 0 8 0 0 3 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 2 0 0 0 0 0
0 4 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 8 0 0 0 8 0 0
0 2 0 8 0 0 3 3 3 0
0 4 4 4 4 4 0 0 3 0
0 4 0 0 0 0 0 8 3 0
0 4 2 2 2 0 0 0 3 0
0 4 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 8 0 0
0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 5 0 0 8 0 0 0
0 7 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 0 0 0 5 0 2 0 8 0 0
0 0 8 8 5 0 2 0 0 0 0
0 7 7 7 7 7 2 0 0 0 0
0 7 0 0 5 0 2 0 8 0 0
0 7 0 0 5 0 2 8 0 0 0
0 7 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 3 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 8 0 0 6 0 0 0 0 0
0 4 0 8 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 8 0 0 0 0 0 0
0 0 6 0 0 8 0 0 3 3 3 0
0 4 4 4 4 0 0 0 0 0 3 0
0 4 6 0 0 0 0 0 0 8 3 0
0 4 6 8 6 6 6 0 0 0 3 0
0 4 0 8 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 8 8 2 0 0 0
0 0 0 5 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 7 0 8 0 0
0 5 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 8 8 2 2 2 0
0 5 5 5 0 0 0 0 2 0
0 5 8 0 0 0 0 0 2 0
0 5 0 0 0 0 0 8 2 0
0 5 7 7 7 7 0 8 2 0
0 5 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 0 6 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 3 0 0 8 0 0
0 4 0 0 0 0 0 0 8 6 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 8 0 0 0 0 0 0
0 3 0 0 8 0 0 6 6 6 0
0 4 4 4 0 0 0 0 0 6 0
0 4 0 0 0 0 8 0 0 6 0
0 4 3 3 3 3 0 0 8 6 0
0 4 0 0 0 0 0 0 8 6 0
0 0 0 0 0 0 0 0 0 0 0
```

## Recolor Components by Perimeter Rank (`medium_132_recolor_components_by_perimeter_rank`)

**Difficulty:** medium

**Skills:** connected components, perimeter measurement, ranking


**Scaffold notes:**
- Find the connected nonzero components.
- Measure each component by exposed-edge perimeter, not by area.
- Recolor them from smallest perimeter to largest as 2, 3, 4.

**Written solution:** Compute the perimeter of each component and recolor the smallest-perimeter shape to 2, the next to 3, and the largest to 4.

**Program solution (Python reference):**
```python
def solve_medium_132_recolor_components_by_perimeter_rank(g):
    comps=connected_components(g)
    ranked=sorted(comps, key=lambda cells: perimeter_of_cells(cells))
    colors=[2,3,4]
    out=zeros(len(g), len(g[0]))
    for cells,color in zip(ranked, colors):
        for r,c in cells:
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 6 6 6 0 0 0 0
0 0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 4 4 4 0 0 0 0
0 0 0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 6 0 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 3 0 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Select the Vertically Symmetric Object and Crop It (`medium_133_select_vertically_symmetric_object_and_crop`)

**Difficulty:** medium

**Skills:** symmetry detection, object selection, cropping, recoloring


**Scaffold notes:**
- Exactly one object is vertically symmetric.
- Ignore the others, even if they are similar in size.
- Crop the symmetric object and recolor it to cyan(8).

**Written solution:** Find the unique object whose cropped binary shape equals its horizontal flip, crop that object, and recolor it to cyan(8).

**Program solution (Python reference):**
```python
def solve_medium_133_select_vertically_symmetric_object_and_crop(g):
    for cells in connected_components(g):
        cg=component_grid(g, cells)
        if is_vertical_symmetric(cg):
            return recolor_nonzero(cg, 8)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 4 0 0 0
0 2 2 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 8
8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 5 5 0 0 0
0 7 7 0 0 0 0 5 0 5 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8 0
8 8 8
8 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 0 6 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8
0 8 0
0 8 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 0 0 0 0 5 0 5 0 0 0
0 7 7 0 0 0 0 0 5 5 5 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8
8 0 8
8 8 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 4 0 4 6 6 0
0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0
```

## Build the Reflection Equivalence Matrix (`hard_127_build_reflection_equivalence_matrix`)

**Difficulty:** hard

**Skills:** panel parsing, reflection matching, relation matrix construction


**Scaffold notes:**
- The input contains three separate object panels.
- Compare the cropped binary object in each panel to every other one using horizontal or vertical reflection only.
- Write a 3×3 matrix with 8 on the diagonal and 2 when two panels are reflection matches.

**Written solution:** Split the row of panels, crop and binarize each object, and build a 3×3 matrix whose diagonal is 8 and whose off-diagonal entries are 2 exactly when one object becomes the other under a horizontal or vertical flip.

**Program solution (Python reference):**
```python
def solve_hard_127_build_reflection_equivalence_matrix(g):
    panel_w=5
    sep=1
    panels=[]
    c=0
    while c+panel_w<=len(g[0]):
        panel=[row[c:c+panel_w] for row in g]
        panels.append(normalize_binary(panel))
        c+=panel_w+sep
    n=len(panels)
    out=zeros(n,n)
    for i,a in enumerate(panels):
        for j,b in enumerate(panels):
            if i==j:
                out[i][j]=8
            elif b==normalize_binary(hflip(a)) or b==normalize_binary(vflip(a)):
                out[i][j]=2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 1 1 0 0 0 1 0 1 0
0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0
0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 1 0
0 0 1 0 0 0 0 1 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 2 0
2 8 0
0 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 1 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 1 0
0 1 0 0 0 0 0 0 1 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 2 0
2 8 0
0 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 1 0 0 0 1 1 1 0
0 1 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 2 0
2 8 0
0 0 8
```

## Decode the Prototype Library with Transform and Recolor Codes (`hard_128_decode_prototype_library_with_transform_and_recolor_codes`)

**Difficulty:** hard

**Skills:** library lookup, code decoding, transforms, gallery construction


**Scaffold notes:**
- The top band is a library of three prototypes.
- The bottom code row gives prototype index, transform code, and output color in three separate groups.
- Decode each group and build the resulting gallery left to right.

**Written solution:** Read the three prototype panels from the library row, then for each code triple select the prototype, apply the indicated transform, recolor its nonzero cells, and place the result into the output gallery.

**Program solution (Python reference):**
```python
def solve_hard_128_decode_prototype_library_with_transform_and_recolor_codes(g):
    lib_rows=g[:3]
    code_row=g[4]
    protos=[]
    c=0
    while c+3<=len(lib_rows[0]):
        protos.append([row[c:c+3] for row in lib_rows])
        c+=4
    panels=[]
    for start in (0,4,8):
        idx,code,col=code_row[start:start+3]
        obj=transform_by_code(protos[idx-1], code)
        panels.append(recolor_nonzero(obj, col))
    return panelize_row(panels, sep=1)
```

**Train 1 input**
```text
1 0 0 0 1 1 1 0 1 1 0
1 0 0 0 0 1 0 0 0 1 1
1 1 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 2 4 0 2 3 6 0 3 1 7
```

**Train 1 output**
```text
4 4 4 0 6 6 6 0 7 7 0
4 0 0 0 0 6 0 0 0 7 7
0 0 0 0 0 6 0 0 0 0 0
```

**Train 2 input**
```text
1 0 1 0 1 1 0 0 0 1 1
1 1 1 0 1 1 0 0 1 1 0
0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 4 3 0 1 1 5 0 3 2 8
```

**Train 2 output**
```text
3 0 0 0 5 0 5 0 0 8 0
3 3 0 0 5 5 5 0 0 8 8
3 3 0 0 0 0 0 0 0 0 8
```

**Train 3 input**
```text
1 0 0 0 0 1 0 0 1 1 1
1 1 0 0 1 1 1 0 0 0 0
0 1 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 2 0 1 4 7 0 2 2 5
```

**Train 3 output**
```text
2 2 2 0 0 7 0 0 5 5 0
0 0 0 0 7 7 0 0 0 5 5
0 0 0 0 7 0 0 0 5 5 0
```

**Train 4 input**
```text
1 1 1 0 1 0 0 0 1 0 1
1 0 1 0 1 0 0 0 1 1 1
1 1 1 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 6 0 3 2 4 0 2 3 7
```

**Train 4 output**
```text
6 6 6 0 0 4 4 0 0 0 7
6 0 6 0 0 4 0 0 0 0 7
6 6 6 0 0 4 4 0 0 7 7
```

**Test input**
```text
1 1 1 0 0 1 1 0 1 1 0
0 1 0 0 1 1 0 0 1 1 0
0 1 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 5 0 3 4 6 0 1 3 8
```

**Test output**
```text
0 5 0 0 6 0 0 0 8 8 8
0 5 5 0 6 6 0 0 0 8 0
0 0 5 0 6 6 0 0 0 8 0
```

## Overlay the Elbow Paths into a Count Map (`hard_129_overlay_elbow_paths_count_map`)

**Difficulty:** hard

**Skills:** pair grouping, path overlay, count mapping


**Scaffold notes:**
- Each color appears twice and defines one endpoint pair.
- For every pair, draw the horizontal-then-vertical elbow path.
- The output is not the paths' colors; it is a count map of how many paths cover each cell.

**Written solution:** Connect every same-colored pair with its horizontal-then-vertical elbow path, count how many paths cover each cell, and map counts 1, 2, 3+ to colors 2, 3, 4.

**Program solution (Python reference):**
```python
def solve_hard_129_overlay_elbow_paths_count_map(g):
    h,w=dims(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos.setdefault(v, []).append((r,c))
    counts=zeros(h,w)
    for color,pts in pos.items():
        if len(pts)!=2:
            continue
        for r,c in elbow_cells(pts[0], pts[1], 'h'):
            counts[r][c]+=1
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if counts[r][c]==1:
                out[r][c]=2
            elif counts[r][c]==2:
                out[r][c]=3
            elif counts[r][c]>=3:
                out[r][c]=4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 4 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
2 3 3 3 3 2 2 2 0 0
2 0 2 2 3 2 2 2 2 0
2 0 2 0 2 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 2 3 3 3 3 2 2 0 0
2 2 2 3 2 2 3 2 2 2 0
2 0 0 2 0 0 2 0 0 0 0
2 0 0 2 0 0 2 0 0 0 0
0 0 0 2 0 0 2 0 0 0 0
0 0 0 2 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 3 3 3 3 3 2 2 2 2 0
0 0 2 0 2 2 3 2 2 2 0 0
0 0 2 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
2 2 3 3 3 3 2 2 0 0
0 2 3 2 2 3 2 2 2 0
0 2 2 0 0 2 0 0 0 0
0 2 2 0 0 2 0 0 0 0
0 0 2 0 0 2 0 0 0 0
0 0 2 0 0 2 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 4 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
2 3 3 3 3 3 2 2 2 0 0
2 0 0 2 2 3 2 2 2 2 0
2 0 0 2 0 2 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Fill Chambers by Legend Priority (`hard_130_fill_chambers_by_legend_priority`)

**Difficulty:** hard

**Skills:** legend priorities, chamber parsing, seed selection, flood fill


**Scaffold notes:**
- The top row lists colors from highest priority to lowest.
- Ignore the separator row of wall cells.
- Within each chamber, fill everything with the highest-priority seed color that appears in that chamber.

**Written solution:** Read the priority order from the legend strip, find each chamber below the wall separator, inspect which seed colors appear inside it, and fill the whole chamber with the highest-priority one.

**Program solution (Python reference):**
```python
def solve_hard_130_fill_chambers_by_legend_priority(g):
    h,w=dims(g)
    out=clone(g)
    priority=[v for v in g[0] if v not in (0,8)]
    area=[row[:] for row in g[2:]]
    chambers=flood_regions_nonwall(area, wall=8)
    for cells in chambers:
        present={area[r][c] for r,c in cells if area[r][c]!=0}
        chosen=0
        for color in priority:
            if color in present:
                chosen=color
                break
        for r,c in cells:
            out[r+2][c]=chosen
    return out
```

**Train 1 input**
```text
2 3 4 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 8 0 0 8
8 4 0 0 8 2 0 8 0 0 8
8 0 0 0 8 0 0 8 0 2 8
8 0 3 0 8 0 0 8 0 0 8
8 0 0 0 8 0 0 8 4 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
2 3 4 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 8 2 2 8 2 2 8
8 3 3 3 8 2 2 8 2 2 8
8 3 3 3 8 2 2 8 2 2 8
8 3 3 3 8 2 2 8 2 2 8
8 3 3 3 8 2 2 8 2 2 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 input**
```text
5 2 7 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 8
8 0 7 0 0 8 0 2 0 8
8 0 0 2 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 0 0 0 8
8 0 5 0 0 8 0 7 0 8
8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
5 2 7 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 8 2 2 2 8
8 2 2 2 2 8 2 2 2 8
8 2 2 2 2 8 2 2 2 8
8 8 8 8 8 8 8 8 8 8
8 5 5 5 5 8 7 7 7 8
8 5 5 5 5 8 7 7 7 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
6 3 2 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 0 8 0 0 8
8 2 0 0 8 3 0 0 8 0 0 8
8 0 0 0 8 0 0 0 8 2 0 8
8 0 0 0 8 0 6 0 8 0 0 8
8 0 6 0 8 0 0 0 8 0 3 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
6 3 2 0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8
8 6 6 6 8 6 6 6 8 3 3 8
8 6 6 6 8 6 6 6 8 3 3 8
8 6 6 6 8 6 6 6 8 3 3 8
8 6 6 6 8 6 6 6 8 3 3 8
8 6 6 6 8 6 6 6 8 3 3 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 input**
```text
4 7 5 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 8 0 0 0 8
8 0 5 0 0 0 8 0 7 0 8
8 0 0 0 0 0 8 0 0 0 8
8 0 0 0 7 0 8 0 0 0 8
8 8 8 8 8 8 8 8 8 8 8
8 0 4 0 0 0 8 0 0 5 8
8 8 8 8 8 8 8 8 8 8 8
```

**Train 4 output**
```text
4 7 5 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 7 7 7 7 7 8 7 7 7 8
8 7 7 7 7 7 8 7 7 7 8
8 7 7 7 7 7 8 7 7 7 8
8 7 7 7 7 7 8 7 7 7 8
8 8 8 8 8 8 8 8 8 8 8
8 4 4 4 4 4 8 5 5 5 8
8 8 8 8 8 8 8 8 8 8 8
```

**Test input**
```text
3 6 2 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 8 0 0 8 0 0 8
8 2 0 0 8 3 0 8 0 0 8
8 0 0 0 8 0 0 8 0 2 8
8 0 6 0 8 0 0 8 0 0 8
8 0 0 0 8 0 0 8 6 0 8
8 8 8 8 8 8 8 8 8 8 8
```

**Test output**
```text
3 6 2 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 6 6 6 8 3 3 8 6 6 8
8 6 6 6 8 3 3 8 6 6 8
8 6 6 6 8 3 3 8 6 6 8
8 6 6 6 8 3 3 8 6 6 8
8 6 6 6 8 3 3 8 6 6 8
8 8 8 8 8 8 8 8 8 8 8
```

## Build the Boolean Gallery: Union, Intersection, XOR (`hard_131_build_boolean_gallery_union_intersection_xor`)

**Difficulty:** hard

**Skills:** panel parsing, boolean shape operations, gallery construction


**Scaffold notes:**
- The input contains two 5×5 binary shape panels.
- Compute union, intersection, and XOR in that order.
- Write them as three output panels from left to right, using colors 2, 3, 4 respectively.

**Written solution:** Compare the two panels cell by cell and build a three-panel gallery showing the union in color 2, the intersection in color 3, and the XOR in color 4.

**Program solution (Python reference):**
```python
def solve_hard_131_build_boolean_gallery_union_intersection_xor(g):
    left=[row[:5] for row in g]
    right=[row[6:11] for row in g]
    union=zeros(5,5)
    inter=zeros(5,5)
    xor=zeros(5,5)
    for r in range(5):
        for c in range(5):
            a=1 if left[r][c]!=0 else 0
            b=1 if right[r][c]!=0 else 0
            if a or b: union[r][c]=2
            if a and b: inter[r][c]=3
            if (a+b)==1: xor[r][c]=4
    return panelize_row([union, inter, xor], sep=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 1 1 0
0 1 0 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 3 0 0 0 0 0 0 4 4 0
0 2 2 0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 2 2 0 0 0 0 0 3 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 1 1 0 0
0 1 1 1 0 0 0 1 1 0 0
0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 3 0 0 0 0 0 0 4 4 0
0 2 2 2 0 0 0 3 3 0 0 0 0 0 0 4 0
0 2 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 1 1 0
0 0 1 1 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 3 0 0 0 0 4 0 4 0
0 2 2 2 0 0 0 0 3 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0
0 1 1 0 0 0 0 1 1 1 0
0 0 1 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 2 2 2 0 0 0 3 3 0 0 0 0 0 0 4 0
0 2 2 2 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 0 0 0
0 1 0 1 0 0 0 1 0 0 0
0 1 1 1 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 3 0 0 0 0 0 0 4 4 0
0 2 0 2 0 0 0 3 0 0 0 0 0 0 0 4 0
0 2 2 2 0 0 0 3 3 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Build the Dihedral Relation Matrix (`hard_132_build_dihedral_relation_matrix`)

**Difficulty:** hard

**Skills:** relation matrix, exact match, rotation match, reflection match


**Scaffold notes:**
- The input contains five object panels.
- Compare cropped binary shapes with precedence: exact, then rotation, then reflection, else none.
- Encode diagonal as 8, exact as 1, rotation as 2, reflection-only as 3, and unrelated as 0.

**Written solution:** Split the five panels, crop and binarize each object, then build a 5×5 relation matrix using 8 on the diagonal, 1 for exact matches, 2 for rotation matches, 3 for reflection-only matches, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_132_build_dihedral_relation_matrix(g):
    panel_w=5
    sep=1
    panels=[]
    c=0
    while c+panel_w<=len(g[0]):
        panel=[row[c:c+panel_w] for row in g]
        panels.append(normalize_binary(panel))
        c+=panel_w+sep
    n=len(panels)
    out=zeros(n,n)
    for i,a in enumerate(panels):
        rotset=all_rotations(a)
        dihedral=all_dihedral(a)
        for j,b in enumerate(panels):
            if i==j:
                out[i][j]=8
            elif b==a:
                out[i][j]=1
            elif b in rotset:
                out[i][j]=2
            elif b in dihedral:
                out[i][j]=3
            else:
                out[i][j]=0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0 0 0 0 1 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0
0 1 1 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 1 2 3 0
1 8 2 3 0
2 2 8 3 0
3 3 3 8 0
0 0 0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 1 1 0 0 0 1 1 1 0 0 0 1 1 0 0 0 0 1 1 1 0
0 1 1 0 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 0 1 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 1 2 3 0
1 8 2 3 0
2 2 8 3 0
3 3 3 8 0
0 0 0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 1 0 1 0
0 1 1 0 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 1 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 1 2 3 0
1 8 2 3 0
2 2 8 3 0
3 3 3 8 0
0 0 0 0 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 1 1 1 0 0 0 0 1 0 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 1 1 1 0
0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 1 2 2 0
1 8 2 2 0
2 2 8 1 0
2 2 1 8 0
0 0 0 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 1 1 0 0 0 0 0 1 0 0 0 0 0 1 1 0 0 0 1 1 1 0
0 0 1 1 0 0 0 0 1 1 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 1 2 3 0
1 8 2 3 0
2 2 8 3 0
3 3 3 8 0
0 0 0 0 8
```

## Compose Two Transforms and Center the Stamp (`hard_133_compose_two_transforms_and_center_stamp`)

**Difficulty:** hard

**Skills:** sequential code execution, transform composition, centering


**Scaffold notes:**
- The first five rows contain the prototype object.
- The last row gives two transform codes followed by the output color.
- Apply the two transforms in order, recolor the object, and center-stamp it into a 7×7 blank canvas.

**Written solution:** Crop the prototype from the first five rows, apply the first transform code and then the second, recolor the nonzero cells to the requested color, and place the transformed object centered in a 7×7 output grid.

**Program solution (Python reference):**
```python
def solve_hard_133_compose_two_transforms_and_center_stamp(g):
    proto=crop_nonzero(g[:5])
    t1,t2,col=g[5][:3]
    obj=transform_by_code(proto, t1)
    obj=transform_by_code(obj, t2)
    obj=recolor_nonzero(obj, col)
    return center_stamp(7, 7, obj)
```

**Train 1 input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 0 0 0
2 3 4 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 4 4 4 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0
0 1 1 1 0
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
3 2 6 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 6 0 0
0 0 6 6 6 0 0
0 0 0 0 6 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0
0 1 0 1 0
0 1 1 1 0
0 0 0 0 0
0 0 0 0 0
4 1 5 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 5 5 5 0 0
0 0 5 0 5 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0
0 1 0 0 0
0 1 1 0 0
0 0 1 0 0
0 0 0 0 0
2 4 7 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 7 7 0 0 0
0 0 0 7 7 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0
0 1 1 0 0
0 1 1 0 0
0 1 0 0 0
0 0 0 0 0
3 4 8 0 0
```

**Test output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 8 0 0 0
0 0 8 8 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

