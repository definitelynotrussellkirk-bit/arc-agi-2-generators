# ARC Puzzle Bank — Twelfth 21 Puzzles
This twelfth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`78`–`84`) so it follows directly after the eleventh bundle.
This volume pushes in a different direction than the last few: axis-span filling, rectangle completion from sparse corners, column gravity, divider-based mirroring, legend-driven recoloring, elbow routing with blockers, lattice projection, library decoding, dihedral relation matrices, chamber flood-fills, boolean mosaics, topological sorting, and sequence decoding.
It also adds a few reusable solver primitives that fit your pipeline well: `axis_span_fill`, `clear_elbow_connect`, `legend_strip_remap`, `chamber_key_fill`, and `library_sequence_decode`.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_twelfth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_twelfth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_twelfth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_78_fill_axis_spans_between_matching_endpoints` — **Fill Axis Spans Between Matching Endpoints**
- `easy_79_fill_rectangles_from_diagonal_corners` — **Fill Rectangles from Diagonal Corners**
- `easy_80_compact_columns_downward` — **Compact Each Column Downward**
- `easy_81_mirror_left_half_across_divider` — **Mirror the Left Half Across the Divider**
- `easy_82_draw_object_bounding_boxes` — **Draw a Bounding Box Around Each Object**
- `easy_83_complete_l_trominoes_to_2x2` — **Complete Each L Tromino to a 2×2 Block**
- `easy_84_recolor_border_touching_components` — **Recolor Border-Touching Components**

### Medium (7)
- `medium_78_recolor_canvas_via_two_row_legend` — **Recolor the Canvas via a Two-Row Legend**
- `medium_79_rotate_cropped_object_by_control_color` — **Rotate the Cropped Object by the Control Color**
- `medium_80_connect_pairs_with_clear_elbow_path` — **Connect Each Pair with the Clear Elbow Path**
- `medium_81_select_area_matched_component_scale2` — **Select the Area-Matched Component and Scale It 2×**
- `medium_82_stack_cropped_objects_by_left_to_right_order` — **Stack Cropped Objects by Left-to-Right Order**
- `medium_83_select_vertically_symmetric_object_and_recolor` — **Select the Left-Right Symmetric Object and Recolor It**
- `medium_84_project_2x2_blocks_to_mini_grid` — **Project 2×2 Blocks to a Mini Grid**

### Hard (7)
- `hard_78_library_decode_select_transform_recolor_shape` — **Decode a Library Shape, Transform It, and Recolor It**
- `hard_79_dihedral_equivalence_matrix_ignoring_color` — **Build the Dihedral-Equivalence Matrix Ignoring Color**
- `hard_80_select_object_by_holes_and_symmetry_scale2` — **Select the Object by Holes and Symmetry, Then Scale It 2×**
- `hard_81_fill_partitioned_chambers_by_internal_keys` — **Fill Partitioned Chambers by Their Internal Keys**
- `hard_82_boolean_mosaic_from_row_and_column_templates` — **Build a Boolean Mosaic from Row and Column Templates**
- `hard_83_sort_objects_by_holes_then_area_and_pack` — **Sort Objects by Hole Count Then Area and Pack Them**
- `hard_84_decode_sequence_of_transformed_library_shapes` — **Decode a Sequence of Transformed Library Shapes**

## Fill Axis Spans Between Matching Endpoints (`easy_78_fill_axis_spans_between_matching_endpoints`)

**Difficulty:** easy

**Skills:** axis-aligned spans, same-color endpoint pairing, same-size transform

**Scaffold notes:**
- Group cells by color.
- For each color, check whether the two cells share a row or a column.
- Fill the inclusive span between them.

**Written solution:** Group nonzero cells by color. Each color appears exactly twice on the same row or the same column. Fill the full horizontal or vertical segment between the two endpoints with that color.

**Program solution (Python reference):**
```python
def solve_easy_78_fill_axis_spans_between_matching_endpoints(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells)!=2:
            continue
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
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 0 0 1 0 8 0 0
0 0 0 0 0 0 0 0
7 0 0 7 0 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 1 1 1 0 8 0 0
0 0 0 0 0 8 0 0
7 7 7 7 0 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0
0 9 0 0 0 0 0 9
0 0 1 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0
0 9 9 9 9 9 9 9
0 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 2 0
0 0 0 9 0 0 0 0
0 0 0 0 0 0 2 8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8
0 0 0 9 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 2 0
0 0 0 9 0 0 2 0
0 0 0 9 0 0 2 8
0 0 0 9 0 0 0 8
0 0 0 9 0 0 0 8
0 0 0 9 0 0 0 8
0 0 0 9 0 0 0 8
0 0 0 9 0 0 0 0
```

**Train 4 input**
```text
2 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 9 9 9
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
1 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0
```

## Fill Rectangles from Diagonal Corners (`easy_79_fill_rectangles_from_diagonal_corners`)

**Difficulty:** easy

**Skills:** rectangle completion, diagonal corner pairing, same-size transform

**Scaffold notes:**
- Pair the two cells of each color.
- Use them as the opposite corners of a rectangle.
- Fill the whole rectangle, not just the border.

**Written solution:** Each color marks two opposite corners of an axis-aligned rectangle. For every color, fill the entire rectangle between those corners with that same color.

**Program solution (Python reference):**
```python
def solve_easy_79_fill_rectangles_from_diagonal_corners(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        r0,r1s=sorted([r1,r2]); c0,c1s=sorted([c1,c2])
        for r in range(r0,r1s+1):
            for c in range(c0,c1s+1):
                out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 6 0 0
0 0 0 0 3 0 0 0
0 0 0 0 0 0 6 0
```

**Train 1 output**
```text
0 0 9 9 0 0 0 0
0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 3 6 6 0
0 0 0 3 3 6 6 0
0 0 0 0 0 6 6 0
```

**Train 2 input**
```text
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 7 7 7
0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0
8 8 8 0 0 0 0 0
0 0 0 0 9 9 0 0
0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 2 0 0 0 0 0 0
0 0 0 2 8 0 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 2 2 0 0 0 0 0
0 0 2 2 8 8 8 8 0
0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0 0
0 0 9 9 9 9 0 0 0
0 0 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 9 0 0
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
0 0 6 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 9 9 9
6 6 6 0 0 0 9 9 9
6 6 6 0 0 0 9 9 9
6 6 6 0 0 0 0 0 0
```

**Test 1 input**
```text
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 9 9 9 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0
2 2 2 2 0 0 0 4 4 4
2 2 2 2 0 0 0 4 4 4
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0
```

## Compact Each Column Downward (`easy_80_compact_columns_downward`)

**Difficulty:** easy

**Skills:** columnwise gravity, stable order preservation, same-size transform

**Scaffold notes:**
- Process one column at a time.
- Ignore zeros and keep the nonzero order.
- Write the collected values back at the bottom.

**Written solution:** Treat each column independently. Read the nonzero cells from top to bottom, then drop them to the bottom of the same column while keeping their relative order unchanged.

**Program solution (Python reference):**
```python
def solve_easy_80_compact_columns_downward(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 1 0 0 1
0 0 0 6 0 0 0 3
0 0 1 0 0 0 0 8
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 8 0 0 1
2 7 0 0 0 6 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 3
0 0 0 6 1 0 0 8
2 7 1 2 8 6 0 1
```

**Train 2 input**
```text
9 0 9 1 0 0 8 0
0 0 3 0 0 0 0 0
0 2 3 0 2 0 4 0
0 0 0 3 3 0 6 2
0 0 0 0 0 7 0 0
0 9 0 0 0 3 8 0
6 0 0 0 6 0 6 0
2 6 0 8 3 6 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 2 0 4 0
9 2 9 1 3 7 6 0
6 9 3 3 6 3 8 0
2 6 3 8 3 6 6 2
```

**Train 3 input**
```text
3 0 0 0 8 0 0 0 7
0 0 4 0 0 3 0 0 0
3 0 0 7 6 9 0 0 0
2 0 0 0 0 0 0 0 4
3 0 8 0 0 0 2 0 7
0 0 0 0 1 0 3 0 0
0 4 0 0 4 0 3 7 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 8 0 0 0 0
3 0 0 0 6 0 2 0 7
2 0 4 0 1 3 3 0 4
3 4 8 7 4 9 3 7 7
```

**Train 4 input**
```text
0 4 1 0 0 0 0
3 0 0 0 0 0 0
4 0 4 0 0 7 0
0 0 0 0 0 0 0
3 1 0 7 0 0 0
4 8 0 0 0 0 0
2 0 0 4 0 0 0
0 0 0 4 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
3 0 0 0 0 0 0
4 0 0 0 0 0 0
3 4 0 7 0 0 0
4 1 1 4 0 0 0
2 8 4 4 0 7 0
```

**Test 1 input**
```text
0 0 0 0 0 9 8
7 0 0 2 0 7 0
0 0 0 0 0 4 0
8 0 0 7 0 0 0
4 0 0 0 0 3 8
0 1 1 0 0 0 9
1 0 6 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
7 0 0 0 0 9 0
8 0 0 0 0 7 8
4 0 1 2 0 4 8
1 1 6 7 0 3 9
```

## Mirror the Left Half Across the Divider (`easy_81_mirror_left_half_across_divider`)

**Difficulty:** easy

**Skills:** reflection, copying across an axis, same-size transform

**Scaffold notes:**
- Locate the solid divider column.
- For each nonzero cell left of the divider, reflect its column index across the divider.
- Write the same color into the mirrored position.

**Written solution:** The full nonzero divider column is the mirror axis. Keep the left half as it is and copy every nonzero cell to its mirrored position on the right half.

**Program solution (Python reference):**
```python
def solve_easy_81_mirror_left_half_across_divider(g):
    out=clone(g)
    h,w=dims(g)
    divider=None
    # find uniform nonzero full column
    for c in range(w):
        vals=[g[r][c] for r in range(h)]
        nz=[v for v in vals if v!=0]
        if len(nz)==h and len(set(nz))==1:
            divider=c
            break
    if divider is None:
        divider=w//2
    for r in range(h):
        for c in range(divider):
            v=g[r][c]
            if v!=0:
                out[r][2*divider-c]=v
    return out
```

**Train 1 input**
```text
0 0 0 5 0 0 0
0 8 0 5 0 0 0
0 0 9 5 0 0 0
2 0 0 5 0 0 0
4 0 6 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
```

**Train 1 output**
```text
0 0 0 5 0 0 0
0 8 0 5 0 8 0
0 0 9 5 9 0 0
2 0 0 5 0 0 2
4 0 6 5 6 0 4
0 0 0 5 0 0 0
0 0 0 5 0 0 0
```

**Train 2 input**
```text
0 9 0 5 0 0 0
0 0 0 5 0 0 0
0 0 9 5 0 0 0
0 0 0 5 0 0 0
3 4 0 5 0 0 0
0 0 7 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
6 0 2 5 0 0 0
```

**Train 2 output**
```text
0 9 0 5 0 9 0
0 0 0 5 0 0 0
0 0 9 5 9 0 0
0 0 0 5 0 0 0
3 4 0 5 0 4 3
0 0 7 5 7 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
6 0 2 5 2 0 6
```

**Train 3 input**
```text
0 0 6 5 0 0 0
0 0 0 5 0 0 0
0 0 7 5 0 0 0
0 0 0 5 0 0 0
0 2 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
3 0 0 5 0 0 0
```

**Train 3 output**
```text
0 0 6 5 6 0 0
0 0 0 5 0 0 0
0 0 7 5 7 0 0
0 0 0 5 0 0 0
0 2 0 5 0 2 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
3 0 0 5 0 0 3
```

**Train 4 input**
```text
0 0 0 6 5 0 0 0 0
6 8 0 0 5 0 0 0 0
2 0 0 0 5 0 0 0 0
0 9 0 6 5 0 0 0 0
0 0 0 3 5 0 0 0 0
7 0 0 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 4 output**
```text
0 0 0 6 5 6 0 0 0
6 8 0 0 5 0 0 8 6
2 0 0 0 5 0 0 0 2
0 9 0 6 5 6 0 9 0
0 0 0 3 5 3 0 0 0
7 0 0 0 5 0 0 0 7
0 0 0 0 5 0 0 0 0
```

**Test 1 input**
```text
0 3 0 0 5 0 0 0 0
7 0 3 0 5 0 0 0 0
0 8 0 0 5 0 0 0 0
0 0 0 1 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 4 1 0 5 0 0 0 0
0 0 3 1 5 0 0 0 0
1 1 0 7 5 0 0 0 0
1 8 0 0 5 0 0 0 0
```

**Test 1 output**
```text
0 3 0 0 5 0 0 3 0
7 0 3 0 5 0 3 0 7
0 8 0 0 5 0 0 8 0
0 0 0 1 5 1 0 0 0
0 0 0 0 5 0 0 0 0
0 4 1 0 5 0 1 4 0
0 0 3 1 5 1 3 0 0
1 1 0 7 5 7 0 1 1
1 8 0 0 5 0 0 8 1
```

## Draw a Bounding Box Around Each Object (`easy_82_draw_object_bounding_boxes`)

**Difficulty:** easy

**Skills:** connected components, bounding boxes, same-size transform

**Scaffold notes:**
- Split the grid into connected monochrome objects.
- Compute the min and max rows and columns for each object.
- Draw the rectangle border for each bounding box.

**Written solution:** Find each monochrome connected component. Compute its bounding box, then draw the border of that box in the component’s own color while leaving the original object in place.

**Program solution (Python reference):**
```python
def solve_easy_82_draw_object_bounding_boxes(g):
    out=clone(g)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp['bbox']
        draw_rect_border(out,r0,c0,r1,c1,comp['color'])
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0
0 0 0 7 7 0 0 0
0 0 0 7 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 0 2 2
0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0
0 0 0 7 7 7 0 0
0 0 0 7 7 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 8 8 0 0 0
0 7 7 7 8 8 0 0 0 0
0 0 7 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 8 8 8 0 0 0
0 7 7 7 8 8 8 0 0 0
0 7 7 7 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 9 0 9 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 9 0 0 0
0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 7 1 1 0 0 0 0
0 7 7 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 9 9 0 0
0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 7 1 1 1 0 0 0
7 7 1 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0
0 0 0 4 0 2 2 0 0
0 0 0 4 0 0 7 0 0
0 0 0 4 4 4 7 7 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0
0 0 0 4 4 4 2 0 0
0 0 0 4 0 4 7 7 0
0 0 0 4 4 4 7 7 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0
0 0 0 1 1 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 2 2 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0
0 0 0 7 7 7 0 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 2 2 0 0
```

## Complete Each L Tromino to a 2×2 Block (`easy_83_complete_l_trominoes_to_2x2`)

**Difficulty:** easy

**Skills:** local completion, 2×2 reasoning, same-size transform

**Scaffold notes:**
- Look for components with area three and a 2×2 bounding box.
- Find the one missing cell inside that box.
- Fill it with the component’s color.

**Written solution:** Every nonzero object is a three-cell L inside a 2×2 box. Fill the one missing corner so that each object becomes a solid 2×2 block of the same color.

**Program solution (Python reference):**
```python
def solve_easy_83_complete_l_trominoes_to_2x2(g):
    out=clone(g)
    for comp in connected_components(g):
        if comp['area']!=3:
            continue
        r0,c0,r1,c1=comp['bbox']
        if r1-r0==1 and c1-c0==1:
            cells=set(comp['cells'])
            for rr in range(r0,r1+1):
                for cc in range(c0,c1+1):
                    if (rr,cc) not in cells:
                        out[rr][cc]=comp['color']
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 0 0 6 6 0
0 0 0 0 6 9 9
0 0 0 0 0 9 0
0 0 0 0 0 0 0
0 3 3 8 0 0 0
0 0 3 8 8 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 6 6 0
0 0 0 0 6 6 9
0 0 0 0 0 9 9
0 0 0 0 0 0 0
0 3 3 8 8 0 0
0 3 3 8 8 0 0
```

**Train 2 input**
```text
0 0 9 9 0 0 0 0
0 3 3 9 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 1 0 0 0
0 0 7 0 1 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 9 9 0 0 0 0
0 3 9 9 0 0 0 0
0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 1 1 0 0
0 7 7 0 1 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 1 9 9 0
0 0 0 1 1 9 0 0
0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0
0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 1 1 9 9 0
0 0 0 1 1 9 9 0
0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0
0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0
0 0 0 0 9 0 0 0
0 0 0 8 8 0 0 0
0 0 4 0 8 0 0 0
0 0 4 4 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0
0 0 0 9 9 0 0 0
0 0 0 8 8 0 0 0
0 0 4 4 8 0 0 0
0 0 4 4 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 6 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 6 6 0 0 0
0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0
```

## Recolor Border-Touching Components (`easy_84_recolor_border_touching_components`)

**Difficulty:** easy

**Skills:** component selection, border detection, same-size recolor

**Scaffold notes:**
- Extract connected monochrome components.
- Check whether each component’s bounding box touches the grid border.
- Recolor only those border-touching components to 7.

**Written solution:** Find every monochrome connected component. If any cell of that component touches the outer border of the grid, recolor the whole component to orange(7). Leave interior components unchanged.

**Program solution (Python reference):**
```python
def solve_easy_84_recolor_border_touching_components(g):
    h,w=dims(g)
    out=clone(g)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp['bbox']
        if r0==0 or c0==0 or r1==h-1 or c1==w-1:
            for r,c in comp['cells']:
                out[r][c]=7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 6 6 0 0
0 0 0 2 2 0 6 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 5 5 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 7 7 0 0
0 0 0 2 2 0 7 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 7 7 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 5 5 0
0 9 9 0 5 5 0 0
0 0 9 9 5 0 0 0
0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0
0 2 2 0 0 0 0 0
3 2 0 0 0 0 0 0
3 3 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 7 7 0
0 9 9 0 7 7 0 0
0 0 9 9 7 0 0 0
0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0
0 2 2 0 0 0 0 0
7 2 0 0 0 0 0 0
7 7 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 6 6 3 3 0 0 0 0 0
4 4 6 6 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
7 6 6 3 3 0 0 0 0 0
7 7 6 6 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 9 9 0 0 4 4 0
9 9 0 0 0 0 4 4
9 1 0 0 0 0 0 0
0 1 1 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 7 7 0 0 7 7 0
7 7 0 0 0 0 7 7
7 1 0 0 0 0 0 0
0 1 1 0 0 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
1 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 0 6 6 0 0
0 0 4 4 4 6 6 0
0 0 0 0 0 9 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 9 9 9
```

**Test 1 output**
```text
7 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 0 6 6 0 0
0 0 4 4 4 6 6 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 7 7
```

## Recolor the Canvas via a Two-Row Legend (`medium_78_recolor_canvas_via_two_row_legend`)

**Difficulty:** medium

**Skills:** legend decoding, palette remapping, crop after decode

**Scaffold notes:**
- Read the legend columns from the first two rows.
- Build a color-to-color mapping.
- Crop away the legend and apply the mapping to the canvas.

**Written solution:** The top two rows form a legend: each nonzero color in row 0 maps to the color directly beneath it in row 1. Ignore the blank separator row, crop the canvas below it, and recolor every canvas cell through that mapping.

**Program solution (Python reference):**
```python
def solve_medium_78_recolor_canvas_via_two_row_legend(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        a=g[0][c]; b=g[1][c]
        if a!=0 and b!=0:
            mapping[a]=b
    canvas=[row[:] for row in g[3:]]
    out=zeros(len(canvas), len(canvas[0]))
    for r in range(len(canvas)):
        for c in range(len(canvas[0])):
            v=canvas[r][c]
            out[r][c]=mapping.get(v, v)
    return out
```

**Train 1 input**
```text
0 9 0 5 4 0
0 1 0 8 6 0
0 0 0 0 0 0
4 4 0 0 0 0
0 0 0 5 5 5
5 0 4 0 5 5
9 9 4 4 9 9
0 0 0 0 9 4
4 9 5 0 0 4
```

**Train 1 output**
```text
6 6 0 0 0 0
0 0 0 8 8 8
8 0 6 0 8 8
1 1 6 6 1 1
0 0 0 0 1 6
6 1 8 0 0 6
```

**Train 2 input**
```text
0 1 4 0 5 0
0 2 6 0 9 0
0 0 0 0 0 0
0 0 0 1 1 0
4 4 5 5 4 0
0 0 1 0 5 0
0 0 0 5 5 0
```

**Train 2 output**
```text
0 0 0 2 2 0
6 6 9 9 6 0
0 0 2 0 9 0
0 0 0 9 9 0
```

**Train 3 input**
```text
0 0 3 0 1 6
0 0 2 0 5 7
0 0 0 0 0 0
0 0 1 1 0 3
1 6 1 0 3 0
6 3 6 0 0 1
1 3 0 6 0 0
```

**Train 3 output**
```text
0 0 5 5 0 2
5 7 5 0 2 0
7 2 7 0 0 5
5 2 0 7 0 0
```

**Train 4 input**
```text
6 0 3 0 0 5
9 0 8 0 0 4
0 0 0 0 0 0
3 0 0 3 0 5
0 3 5 6 0 3
0 3 5 5 0 0
3 0 5 6 3 3
6 3 3 0 6 0
```

**Train 4 output**
```text
8 0 0 8 0 4
0 8 4 9 0 8
0 8 4 4 0 0
8 0 4 9 8 8
9 8 8 0 9 0
```

**Test 1 input**
```text
8 4 2 0 0 0 0
9 6 1 0 0 0 0
0 0 0 0 0 0 0
2 4 8 2 8 4 0
0 4 8 0 4 2 0
0 0 0 4 8 8 8
2 4 0 4 0 8 4
0 2 8 0 8 0 0
```

**Test 1 output**
```text
1 6 9 1 9 6 0
0 6 9 0 6 1 0
0 0 0 6 9 9 9
1 6 0 6 0 9 6
0 1 9 0 9 0 0
```

## Rotate the Cropped Object by the Control Color (`medium_79_rotate_cropped_object_by_control_color`)

**Difficulty:** medium

**Skills:** control codes, rotation, object cropping

**Scaffold notes:**
- Read the control code at the top-left.
- Crop the only nonzero object after removing the control cell.
- Apply the chosen rotation to the cropped object.

**Written solution:** The single control cell in the top-left corner chooses a rotation. Remove that control cell, crop the remaining object to its bounding box, and rotate the crop according to the code.

**Program solution (Python reference):**
```python
def solve_medium_79_rotate_cropped_object_by_control_color(g):
    code=g[0][0]
    work=clone(g)
    work[0][0]=0
    obj=crop_nonzero(work)
    return apply_transform(obj, code)
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8
0 0 0 0 0 8 8 0
0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8
8 8 0
8 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8
0 0 0 0 0 8 8 0
0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 0
8 8 0
0 8 8
```

**Train 3 input**
```text
1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 0
0 0 0 0 9 9 0 0
0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 9
9 9 0
9 0 0
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0
0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 8
8 8
8 0
```

**Test 1 input**
```text
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5
0 0 0 0 0 5 5 0
0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 0
0 5 5
0 0 5
```

## Connect Each Pair with the Clear Elbow Path (`medium_80_connect_pairs_with_clear_elbow_path`)

**Difficulty:** medium

**Skills:** paired routing, obstacle avoidance, elbow paths

**Scaffold notes:**
- Ignore the blocker color 5.
- For each color pair, test the two candidate elbow turns.
- Draw the L path that stays clear.

**Written solution:** Each non-blocker color appears twice and must be connected by a one-cell-wide L path. Try the two possible elbows; exactly one is clear of blockers, so draw that path in the endpoint color.

**Program solution (Python reference):**
```python
def solve_medium_80_connect_pairs_with_clear_elbow_path(g):
    out=clone(g)
    pos=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v not in (0,5):
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        elbows=[(r1,c2),(r2,c1)]
        chosen=None
        for er,ec in elbows:
            if clear_line(g,r1,c1,er,ec,color) and clear_line(g,er,ec,r2,c2,color):
                chosen=(er,ec)
                break
        if chosen is None:
            continue
        er,ec=chosen
        draw_line(out,r1,c1,er,ec,color)
        draw_line(out,er,ec,r2,c2,color)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 5 0 2 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0
0 0 0 5 0 2 4 0 0
0 0 0 2 2 2 4 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 0
0 5 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 7 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 5 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 7 5 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 7 7 0 0 0
0 5 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 2
0 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
5 3 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 6 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0
5 3 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 5 0 0 0 6 0 0 0
```

**Train 4 input**
```text
0 0 0 3 0 0 0 0 0
0 0 5 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 3 3 3 3 0 0
0 0 5 2 0 0 3 0 0
0 0 0 2 0 0 3 0 0
0 0 0 2 0 0 3 0 0
0 0 2 2 0 0 3 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0
0 0 0 5 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
9 2 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
9 2 5 5 0 0 0 0 0
9 2 0 0 0 0 0 0 0
9 2 2 2 0 0 0 0 0
9 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Select the Area-Matched Component and Scale It 2× (`medium_81_select_area_matched_component_scale2`)

**Difficulty:** medium

**Skills:** area matching, marker counting, size change

**Scaffold notes:**
- Count the markers in the top row.
- Measure the area of each component below.
- Select the matching component, crop it, and scale each cell into a 2×2 block.

**Written solution:** Count the blue marker cells in the top row. Among the objects below, find the connected component whose area matches that count, crop it to its bounding box, and scale the crop by a factor of two.

**Program solution (Python reference):**
```python
def solve_medium_81_select_area_matched_component_scale2(g):
    k=sum(1 for v in g[0] if v==1)
    work=[row[:] for row in g[1:]]
    comps=connected_components(work)
    target=min([c for c in comps if c['area']==k], key=lambda c:(c['bbox'][0],c['bbox'][1]))
    return scale2(crop_bbox(work, target['bbox']))
```

**Train 1 input**
```text
1 0 0 0 1 1 0 1 0
7 7 7 6 0 0 0 0 0
0 7 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 8 0 0 0
```

**Train 1 output**
```text
7 7 7 7 7 7
7 7 7 7 7 7
0 0 7 7 0 0
0 0 7 7 0 0
```

**Train 2 input**
```text
1 0 1 0 1 1 0 0 1
7 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 0 8 8 8 0
0 0 0 0 0 0 8 0 0
```

**Train 2 output**
```text
7 7 0 0 0 0
7 7 0 0 0 0
7 7 0 0 0 0
7 7 0 0 0 0
7 7 7 7 7 7
7 7 7 7 7 7
```

**Train 3 input**
```text
1 0 1 0 1 0 1 1 0
8 8 8 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 0 0 5 0 0 0
0 0 4 4 4 5 5 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 0 0 0 0
4 4 0 0 0 0
4 4 0 0 0 0
4 4 0 0 0 0
4 4 4 4 4 4
4 4 4 4 4 4
```

**Train 4 input**
```text
0 0 1 0 0 1 1 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 6 6 6
2 2 2 0 0 0 0 6 0
2 2 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 0 0
4 4 0 0
4 4 4 4
4 4 4 4
```

**Test 1 input**
```text
0 1 0 1 0 1 1 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 8 8 8 0 0
0 2 2 2 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
```

**Test 1 output**
```text
4 4 4 4 4 4
4 4 4 4 4 4
0 0 4 4 0 0
0 0 4 4 0 0
```

## Stack Cropped Objects by Left-to-Right Order (`medium_82_stack_cropped_objects_by_left_to_right_order`)

**Difficulty:** medium

**Skills:** component extraction, ordering by position, packing

**Scaffold notes:**
- Find connected components and their bounding boxes.
- Sort components by minimum column.
- Crop each one and pack the crops into a vertical strip.

**Written solution:** Find all connected components, sort them by the left edge of their bounding boxes, crop each object to its own box, and stack the crops vertically in that left-to-right order with a one-row gap between them.

**Program solution (Python reference):**
```python
def solve_medium_82_stack_cropped_objects_by_left_to_right_order(g):
    comps=sorted(connected_components(g), key=lambda c:(c['bbox'][1], c['bbox'][0]))
    pieces=[crop_bbox(g, comp['bbox']) for comp in comps]
    return vstack(pieces, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0
0 3 3 3 0 0 0 0 6 6
0 0 3 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 3
0 3 0
0 0 0
4 0 0
4 0 0
4 4 4
0 0 0
6 6 0
0 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 0 0
4 4 0
0 0 0
9 0 0
9 0 0
9 9 9
0 0 0
8 8 0
0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 6 0
0 0 7 7 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 0
0 7 7
0 0 0
3 0 0
3 0 0
3 3 3
0 0 0
6 0 0
6 6 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 0
8 8 0
0 0 0
4 4 4
0 4 0
0 0 0
3 0 0
3 0 0
3 3 3
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 9 9 6 6 6
0 8 0 0 0 0 9 9 6 0
0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 0 0
8 0 0
8 8 8
0 0 0
9 9 6
0 9 9
0 0 0
6 6 6
9 6 0
```

## Select the Left-Right Symmetric Object and Recolor It (`medium_83_select_vertically_symmetric_object_and_recolor`)

**Difficulty:** medium

**Skills:** symmetry detection, marker-controlled recolor, object crop

**Scaffold notes:**
- Remove the marker cell and read its color.
- Check each object for vertical mirror symmetry within its bounding box.
- Crop the unique symmetric object and recolor it to the marker color.

**Written solution:** The top-left marker gives the target output color. Among the objects below, exactly one is symmetric under left-right reflection inside its own bounding box; crop that object and recolor every nonzero cell to the marker color.

**Program solution (Python reference):**
```python
def solve_medium_83_select_vertically_symmetric_object_and_recolor(g):
    target_color=g[0][0]
    work=clone(g)
    work[0][0]=0
    comps=connected_components(work)
    candidates=[]
    for comp in comps:
        cropped=crop_bbox(work, comp['bbox'])
        if is_vertically_symmetric(cropped):
            candidates.append(comp)
    target=min(candidates, key=lambda c:(c['bbox'][0], c['bbox'][1]))
    return recolor(crop_bbox(work, target['bbox']), target_color)
```

**Train 1 input**
```text
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 5 3 0 1 0 1 0 0 0
0 0 3 0 1 1 1 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 0 6
6 0 6
6 6 6
```

**Train 2 input**
```text
8 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 5 5 5 0 0 0
0 3 3 3 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8
0 8 0
```

**Train 3 input**
```text
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 3 3 1 0 1 0 0 0 0
0 3 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 0 9
9 9 9
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 4 4 4 0
0 0 0 0 4 0 0 4 0 0
0 0 3 3 4 4 4 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 9
0 9 0
```

**Test 1 input**
```text
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 3 0
0 0 0 4 0 0 3 3 3 0
0 0 0 4 0 0 5 5 0 0
0 0 0 4 4 4 0 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 0 7
7 7 7
```

## Project 2×2 Blocks to a Mini Grid (`medium_84_project_2x2_blocks_to_mini_grid`)

**Difficulty:** medium

**Skills:** object abstraction, lattice detection, size reduction

**Scaffold notes:**
- Detect the solid 2×2 monochrome blocks.
- Record their top-left lattice positions.
- Map distinct block rows and columns to indices in a smaller grid.

**Written solution:** Every object is a solid 2×2 block placed on a lattice with one-cell gaps. Replace each 2×2 block by a single cell of the same color, preserving its row and column order on the lattice, to produce the smaller summary grid.

**Program solution (Python reference):**
```python
def solve_medium_84_project_2x2_blocks_to_mini_grid(g):
    h,w=dims(g)
    blocks=[]
    used=set()
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r+i][c+j] for i in range(2) for j in range(2)]
            if vals[0]!=0 and len(set(vals))==1:
                cells={(r+i,c+j) for i in range(2) for j in range(2)}
                if not any(cell in used for cell in cells):
                    blocks.append((r,c,vals[0]))
                    used |= cells
    rows=sorted({r for r,c,color in blocks})
    cols=sorted({c for r,c,color in blocks})
    out=zeros(len(rows), len(cols))
    rix={r:i for i,r in enumerate(rows)}
    cix={c:i for i,c in enumerate(cols)}
    for r,c,color in blocks:
        out[rix[r]][cix[c]]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 5
0 4 0
1 0 0
0 3 0
```

**Train 2 input**
```text
3 3 0 0 0 0 0 0
3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 4 0 2 2
0 0 0 4 4 0 2 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
8 8 0 0 0 0 7 7
8 8 0 0 0 0 7 7
```

**Train 2 output**
```text
3 0 0
0 4 2
8 0 7
```

**Train 3 input**
```text
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3
0 9
0 2
7 0
```

**Train 4 input**
```text
3 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 7 7 0 0 0
1 1 0 0 0 0 7 7 0 0 0
```

**Train 4 output**
```text
3 0
4 0
1 7
```

**Test 1 input**
```text
5 5 0 8 8 0 0 0 0 0 0
5 5 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 0 2 2 0 0 0
0 0 0 1 1 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 7 7 0 0 0
```

**Test 1 output**
```text
5 8 0
0 1 2
0 0 7
```

## Decode a Library Shape, Transform It, and Recolor It (`hard_78_library_decode_select_transform_recolor_shape`)

**Difficulty:** hard

**Skills:** panel library decoding, control-strip interpretation, multi-step transform

**Scaffold notes:**
- Read the panel index from the number of blue markers.
- Read the transform code and target color from the control strip.
- Crop the selected panel’s object, transform it, and recolor it.

**Written solution:** The control strip has three jobs: the count of blue cells selects one of the four library panels, the middle code chooses a geometric transform, and the last code gives the output color. Crop the chosen library shape, apply the transform, and recolor every nonzero cell to the target color.

**Program solution (Python reference):**
```python
def solve_hard_78_library_decode_select_transform_recolor_shape(g):
    # row0: blue markers count -> 1..4 panel index; col5 transform code; col7 target color
    index=sum(1 for v in g[0][:4] if v==1)
    code=g[0][5]
    target=g[0][7]
    positions=panel_positions_2x2(4,4,gap=1,top=2,left=0)
    top,left=positions[index-1]
    panel=crop_panel(g, top,left,4,4)
    obj=crop_nonzero(panel)
    transformed=apply_transform(obj, code)
    return recolor(transformed, target)
```

**Train 1 input**
```text
1 0 0 0 0 5 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 4 4 0
0 8 0 0 0 0 0 4 4
0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0
7 7 0 0 0 0 0 5 5
7 0 0 0 0 0 5 5 0
0 0 0 0 0 0 5 0 0
```

**Train 1 output**
```text
0 0 4
0 0 4
4 4 4
```

**Train 2 input**
```text
1 1 1 0 0 2 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 9 9 0 0
0 2 0 0 0 0 9 9 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
4 4 0 0 0 0 0 5 5
4 0 0 0 0 0 5 5 0
0 0 0 0 0 0 5 0 0
```

**Train 2 output**
```text
3 3 3
0 3 3
0 0 3
```

**Train 3 input**
```text
1 1 1 0 0 4 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 6 6 0
0 2 2 2 0 0 0 6 6
0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 9 9 0
0 8 8 0 0 9 9 0 0
0 8 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0
8 8 0
8 8 8
```

**Train 4 input**
```text
1 1 0 0 0 4 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 9 9 0
8 0 0 0 0 0 0 9 9
8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 7 7 0
3 3 0 0 0 7 7 0 0
3 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 9
9 9
9 0
```

**Test 1 input**
```text
1 1 1 1 0 5 0 2 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 3 3 0 0
0 5 0 0 0 0 3 3 0
0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0
2 2 2 0 0 8 8 0 0
2 2 0 0 0 8 0 0 0
2 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 2 0
0 2 2
0 0 2
```

## Build the Dihedral-Equivalence Matrix Ignoring Color (`hard_79_dihedral_equivalence_matrix_ignoring_color`)

**Difficulty:** hard

**Skills:** shape normalization, dihedral symmetry, relation matrix

**Scaffold notes:**
- Crop the shape in each panel and ignore the exact colors.
- Generate the rotation/flip variants of each shape.
- Fill a 4×4 matrix according to pairwise equivalence.

**Written solution:** Treat the four panels as binary shapes, ignoring their colors. Two shapes match if one can be turned into the other by a rotation or a mirror flip. Output a 4×4 matrix whose cells are cyan(8) exactly where the corresponding pair of panels is dihedrally equivalent.

**Program solution (Python reference):**
```python
def solve_hard_79_dihedral_equivalence_matrix_ignoring_color(g):
    positions=panel_positions_2x2(4,4,gap=1,top=0,left=0)
    objs=[crop_nonzero(crop_panel(g,top,left,4,4)) for top,left in positions]
    variants=[set(dihedral_variants(obj)) for obj in objs]
    out=zeros(4,4)
    for i in range(4):
        for j in range(4):
            if normalize_binary(objs[j]) in variants[i]:
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 4
6 0 6 0 0 0 0 0 4
6 6 6 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 7 7 7
0 8 0 0 0 0 7 0 7
0 8 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 0 8
0 8 8 0
0 8 8 0
8 0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 8 8 8
0 7 7 7 0 0 8 0 8
0 7 0 0 0 0 8 8 8
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 9 9 9 0 6 6 6 0
0 9 0 9 0 0 0 6 0
0 9 9 9 0 0 0 6 0
```

**Train 2 output**
```text
8 0 0 8
0 8 8 0
0 8 8 0
8 0 0 8
```

**Train 3 input**
```text
0 9 9 9 0 0 7 0 0
0 0 9 9 0 7 7 0 0
0 0 0 9 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0
7 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 6 0
```

**Train 3 output**
```text
8 0 8 0
0 8 0 8
8 0 8 0
0 8 0 8
```

**Train 4 input**
```text
0 0 0 0 0 4 0 0 0
0 9 0 0 0 4 0 0 0
0 9 9 0 0 4 4 4 0
0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
0 0 6 0 0 0 0 0 9
0 6 6 6 0 0 9 9 9
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 0 8 0
0 8 0 8
8 0 8 0
0 8 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 7 0
2 2 0 0 0 0 7 7 0
0 2 2 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0
7 0 7 0 0 0 7 7 7
7 7 7 0 0 0 7 0 7
0 0 0 0 0 0 7 7 7
```

**Test 1 output**
```text
8 8 0 0
8 8 0 0
0 0 8 8
0 0 8 8
```

## Select the Object by Holes and Symmetry, Then Scale It 2× (`hard_80_select_object_by_holes_and_symmetry_scale2`)

**Difficulty:** hard

**Skills:** topological features, multi-key selection, size change

**Scaffold notes:**
- Decode the required hole count, symmetry flag, and output color from the top row.
- Measure hole count and mirror symmetry for each object below.
- Select the unique match, crop it, scale it 2×, and recolor it.

**Written solution:** The top row encodes three things: the number of blue markers minus one gives the required hole count, the middle code says whether the target object must be left-right symmetric, and the last code gives the output color. Find the unique matching object below, crop it, scale it by 2, and recolor it to the target color.

**Program solution (Python reference):**
```python
def solve_hard_80_select_object_by_holes_and_symmetry_scale2(g):
    holes_req=sum(1 for v in g[0] if v==1)-1
    sym_req=(g[0][4]==2)
    target_color=g[0][6]
    work=[row[:] for row in g[1:]]
    comps=connected_components(work)
    choices=[]
    for comp in comps:
        cropped=crop_bbox(work, comp['bbox'])
        if hole_count(cropped)==holes_req and is_vertically_symmetric(cropped)==sym_req:
            choices.append(comp)
    target=min(choices, key=lambda c:(c['bbox'][0], c['bbox'][1]))
    return recolor(scale2(crop_bbox(work, target['bbox'])), target_color)
```

**Train 1 input**
```text
0 1 0 0 2 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0
3 3 3 3 3 9 9 9 9 9 0
0 0 0 0 0 9 0 9 0 9 9
0 0 0 0 0 9 9 9 9 9 0
0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 7 7 7 7
7 7 7 7 7 7
0 0 7 7 0 0
0 0 7 7 0 0
```

**Train 2 input**
```text
1 1 1 0 2 0 8 0 0 0 0
3 3 3 0 0 0 0 2 2 2 0
0 3 0 0 0 0 0 2 0 2 2
0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 8 0 8 0 8 0 0
0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 0 0 8 8 0 0 8 8
8 8 0 0 8 8 0 0 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
1 1 0 0 2 0 8 0 0 0 0
2 2 2 0 9 9 9 9 9 0 0
2 0 2 0 9 0 9 0 9 9 0
2 2 2 0 9 9 9 9 9 0 0
0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 8 0 8 0 8 0 0
0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 4 input**
```text
1 1 1 0 3 0 7 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 3 0 3 3 0 0 9 0 0 0
0 3 3 3 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0
0 0 4 0 4 0 4 4 0 0 0
0 0 4 4 4 4 4 0 0 0 0
```

**Train 4 output**
```text
7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 0 0
7 7 0 0 7 7 0 0 7 7 7 7
7 7 0 0 7 7 0 0 7 7 7 7
7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 0 0
```

**Test 1 input**
```text
1 0 1 0 2 0 9 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 8 0 8 8 0
0 0 0 6 6 6 8 8 8 0 0
0 0 0 6 0 6 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0
0 0 5 0 5 0 5 5 0 0 0
0 0 5 5 5 5 5 0 0 0 0
```

**Test 1 output**
```text
9 9 9 9 9 9
9 9 9 9 9 9
9 9 0 0 9 9
9 9 0 0 9 9
9 9 9 9 9 9
9 9 9 9 9 9
```

## Fill Partitioned Chambers by Their Internal Keys (`hard_81_fill_partitioned_chambers_by_internal_keys`)

**Difficulty:** hard

**Skills:** flood fill, wall-separated regions, key propagation

**Scaffold notes:**
- Treat 5 as an impassable wall.
- Find connected regions in the remaining cells.
- If a region contains exactly one key color, fill its zeros with that color.

**Written solution:** The wall color 5 partitions the grid into chambers. If a chamber contains a single colored key cell, flood the rest of that chamber with the same color while leaving the walls untouched. Chambers without a key stay blank.

**Program solution (Python reference):**
```python
def solve_hard_81_fill_partitioned_chambers_by_internal_keys(g):
    h,w=dims(g)
    out=clone(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or seen[r][c]:
                continue
            q=deque([(r,c)]); seen[r][c]=True
            cells=[]; colors=set()
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                if g[rr][cc] not in (0,5):
                    colors.add(g[rr][cc])
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=5:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            if len(colors)==1:
                color=next(iter(colors))
                for rr,cc in cells:
                    if out[rr][cc]==0:
                        out[rr][cc]=color
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 5 5 5 5 5 5 5 5
5 0 0 5 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 5 0 0 0 0 0 0 5
5 0 0 5 0 0 0 8 0 0 5
5 0 0 5 0 0 0 0 0 0 5
5 3 0 5 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 5 5 5 5 5 5 5 5
5 0 0 5 0 0 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 3 3 5 8 8 8 8 8 8 5
5 3 3 5 8 8 8 8 8 8 5
5 3 3 5 8 8 8 8 8 8 5
5 3 3 5 8 8 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 3 0 0 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 2 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 6 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 3 3 3 3 5 5 5 5 5 5
5 3 3 3 3 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 2 2 2 2 5 6 6 6 6 5
5 2 2 2 2 5 6 6 6 6 5
5 2 2 2 2 5 6 6 6 6 5
5 2 2 2 2 5 6 6 6 6 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 4 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 7 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 4 4 4 4 5
5 7 7 7 7 5 4 4 4 4 5
5 7 7 7 7 5 4 4 4 4 5
5 7 7 7 7 5 4 4 4 4 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 7 0 0 5 0 0 0 0 5
5 0 0 0 0 5 6 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 1 0 0 5 9 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 7 7 7 7 5 6 6 6 6 5
5 7 7 7 7 5 6 6 6 6 5
5 7 7 7 7 5 6 6 6 6 5
5 7 7 7 7 5 6 6 6 6 5
5 5 5 5 5 5 5 5 5 5 5
5 1 1 1 1 5 9 9 9 9 5
5 1 1 1 1 5 9 9 9 9 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 4 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 0 5 0 1 0 0 5
5 0 0 0 0 5 0 0 0 0 5
5 0 0 0 8 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 4 4 4 4 5 0 0 0 0 5
5 4 4 4 4 5 0 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 5 1 1 1 1 5
5 8 8 8 8 5 1 1 1 1 5
5 8 8 8 8 5 1 1 1 1 5
5 8 8 8 8 5 1 1 1 1 5
5 5 5 5 5 5 5 5 5 5 5
```

## Build a Boolean Mosaic from Row and Column Templates (`hard_82_boolean_mosaic_from_row_and_column_templates`)

**Difficulty:** hard

**Skills:** template galleries, boolean shape composition, cross-product construction

**Scaffold notes:**
- Read the boolean operation code.
- Extract the two top templates and the two left templates.
- Build the 2×2 cross-product gallery using AND, OR, or XOR on their binary masks.

**Written solution:** The code in the top-left selects a boolean operation. Two templates sit across the top and two more down the left. Combine every row template with every column template using the chosen boolean operation on nonzero cells, and place the four results in a 2×2 gallery.

**Program solution (Python reference):**
```python
def solve_hard_82_boolean_mosaic_from_row_and_column_templates(g):
    op=g[1][1]
    row_templates=[
        crop_panel(g,0,4,3,3),
        crop_panel(g,0,8,3,3),
    ]
    col_templates=[
        crop_panel(g,4,0,3,3),
        crop_panel(g,8,0,3,3),
    ]
    rows=[]
    for ctemp in col_templates:
        panels=[]
        for rtemp in row_templates:
            panels.append(boolean_combine(rtemp, ctemp, op))
        rows.append(hstack(panels, gap=1))
    return vstack(rows, gap=1)
```

**Train 1 input**
```text
0 0 0 0 2 0 0 0 3 0 3
0 3 0 0 2 2 0 0 0 3 0
0 0 0 0 0 2 0 0 3 0 3
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 8
0 0 0 0 8 0 0
0 0 0 0 8 8 8
0 0 0 0 0 0 0
8 8 0 0 8 8 8
0 0 8 0 8 0 8
0 8 8 0 8 0 0
```

**Train 2 input**
```text
0 0 0 0 9 9 9 0 0 7 0
0 1 0 0 0 9 0 0 7 7 7
0 0 0 0 0 9 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 8 0 0 0 0
0 8 0 0 0 8 0
0 0 0 0 0 0 8
0 0 0 0 0 0 0
0 8 0 0 0 8 0
0 8 0 0 8 8 8
0 0 0 0 0 0 8
```

**Train 3 input**
```text
0 0 0 0 9 9 0 0 6 0 0
0 2 0 0 0 9 9 0 6 6 0
0 0 0 0 0 0 9 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0 0 8 8 0
8 8 8 0 8 8 8
0 0 8 0 0 8 8
0 0 0 0 0 0 0
8 8 8 0 8 8 8
0 8 8 0 8 8 0
0 8 8 0 0 8 0
```

**Train 4 input**
```text
0 0 0 0 0 6 0 0 4 4 4
0 1 0 0 6 6 6 0 0 4 0
0 0 0 0 0 0 6 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
8 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 8 0 8
0 8 0 0 0 8 0
0 0 8 0 0 0 0
0 0 0 0 0 0 0
0 8 0 0 0 8 0
8 8 8 0 0 8 0
0 0 8 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 8 0 0 0 8 8 8
0 1 0 0 8 8 0 0 0 8 0
0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 0 0 0 8 8 0
0 8 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 8 0
8 8 0 0 0 8 0
0 0 0 0 0 0 0
```

## Sort Objects by Hole Count Then Area and Pack Them (`hard_83_sort_objects_by_holes_then_area_and_pack`)

**Difficulty:** hard

**Skills:** topological ranking, multi-criterion sorting, packing

**Scaffold notes:**
- Measure hole count and area for each object.
- Sort first by holes, then by area.
- Crop the sorted objects and pack them horizontally.

**Written solution:** Find all connected objects, count the enclosed holes in each one, and compute each area. Sort objects by hole count from highest to lowest, then by area from largest to smallest, crop each object, and pack the crops left to right with a one-column gap.

**Program solution (Python reference):**
```python
def solve_hard_83_sort_objects_by_holes_then_area_and_pack(g):
    comps=connected_components(g)
    comps=sorted(comps, key=lambda c:(-hole_count(crop_bbox(g, c['bbox'])), -c['area'], c['bbox'][0], c['bbox'][1]))
    pieces=[crop_bbox(g, comp['bbox']) for comp in comps]
    return hstack(pieces, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 2 0 2 0 2 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 5 5 5 0 0 0 0 0
0 0 1 0 0 5 0 5 5 0 0 0 0
0 0 1 1 1 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 2 2 0 5 5 5 0 0 1 0 0
2 0 2 0 2 0 5 0 5 5 0 1 0 0
2 2 2 2 2 0 5 5 5 0 0 1 1 1
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 5 0 5 5 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 4 0 4 0 4 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0
```

**Train 2 output**
```text
4 4 4 4 4 0 5 5 5 0 0 1 0 0
4 0 4 0 4 0 5 0 5 5 0 1 0 0
4 4 4 4 4 0 5 5 5 0 0 1 1 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 0 7 7 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 3 3 3 3 3 0 0
0 0 9 0 0 0 3 0 3 0 3 0 0
0 0 9 9 9 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 3 3 3 3 0 7 7 7 0 0 9 0 0
3 0 3 0 3 0 7 0 7 7 0 9 0 0
3 3 3 3 3 0 7 7 7 0 0 9 9 9
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 9 9 9 9 9 0 2 0 0 0 0
0 0 9 0 9 0 9 0 2 2 2 0 0
0 0 9 9 9 9 9 6 6 6 0 0 0
0 0 0 0 0 0 0 6 0 6 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 9 9 9 0 6 6 6 0 0 2 0 0
9 0 9 0 9 0 6 0 6 6 0 2 0 0
9 9 9 9 9 0 6 6 6 0 0 2 2 2
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 9 9 9 9 9
0 0 0 0 0 4 0 0 9 0 9 0 9
0 0 0 0 0 4 4 4 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 8 0 8 8 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
```

**Test 1 output**
```text
9 9 9 9 9 0 8 8 8 0 0 4 0 0
9 0 9 0 9 0 8 0 8 8 0 4 0 0
9 9 9 9 9 0 8 8 8 0 0 4 4 4
```

## Decode a Sequence of Transformed Library Shapes (`hard_84_decode_sequence_of_transformed_library_shapes`)

**Difficulty:** hard

**Skills:** sequence decoding, panel libraries, transform strip construction

**Scaffold notes:**
- Read the three panel indices, three transform codes, and three target colors.
- Crop the three library shapes from the fixed panel positions.
- Execute the coded sequence and concatenate the transformed outputs.

**Written solution:** The first three rows encode a three-step program: each step chooses a library panel, a transform, and an output color. Apply each step to the library below, then place the three resulting transformed crops side by side to form the output strip.

**Program solution (Python reference):**
```python
def solve_hard_84_decode_sequence_of_transformed_library_shapes(g):
    idx_codes=[g[0][c] for c in (0,2,4)]
    tf_codes=[g[1][c] for c in (0,2,4)]
    colors=[g[2][c] for c in (0,2,4)]
    panels=[crop_panel(g,4,0,4,4), crop_panel(g,4,5,4,4), crop_panel(g,4,10,4,4)]
    pieces=[]
    for idx, tf, color in zip(idx_codes, tf_codes, colors):
        obj=crop_nonzero(panels[idx-1])
        transformed=apply_transform(obj, tf)
        pieces.append(recolor(transformed, color))
    return hstack(pieces, gap=1)
```

**Train 1 input**
```text
3 0 3 0 3 0 0 0 0 0 0 0 0 0
2 0 4 0 4 0 0 0 0 0 0 0 0 0
7 0 9 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 4 4 4
0 8 0 0 0 9 9 0 0 0 0 4 4 0
0 8 8 8 0 0 9 9 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 7 0 9 0 0 0 4 0 0
0 7 7 0 9 9 0 0 4 4 0
0 0 7 0 9 9 9 0 4 4 4
```

**Train 2 input**
```text
3 0 3 0 1 0 0 0 0 0 0 0 0 0
2 0 4 0 4 0 0 0 0 0 0 0 0 0
7 0 3 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0 0 0 0
6 0 0 0 0 0 0 9 9 0 2 2 2 0
6 0 0 0 0 0 0 0 0 0 2 2 0 0
6 6 6 0 0 0 0 0 0 0 2 0 0 0
```

**Train 2 output**
```text
7 7 7 0 3 0 0 0 0 0 2
0 7 7 0 3 3 0 0 0 0 2
0 0 7 0 3 3 3 0 2 2 2
```

**Train 3 input**
```text
1 0 2 0 1 0 0 0 0 0 0 0 0 0
5 0 5 0 3 0 0 0 0 0 0 0 0 0
4 0 8 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 6 6 6 0
0 8 0 0 0 9 9 0 0 0 6 6 0 0
0 8 8 8 0 0 9 9 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 4 0 0 8 8 0 9 9 9
0 0 4 0 8 8 0 0 0 0 9
4 4 4 0 0 0 0 0 0 0 9
```

**Train 4 input**
```text
2 0 2 0 1 0 0 0 0 0 0 0 0 0
4 0 2 0 3 0 0 0 0 0 0 0 0 0
3 0 2 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 3 3 0 0 0 0 0 0
8 0 0 0 0 0 0 3 3 0 0 6 6 6
8 8 8 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0
```

**Train 4 output**
```text
0 3 0 0 2 0 6 6 6
3 3 0 2 2 0 0 0 6
3 0 0 2 0 0 0 0 6
```

**Test 1 input**
```text
2 0 2 0 3 0 0 0 0 0 0 0 0 0
4 0 2 0 3 0 0 0 0 0 0 0 0 0
2 0 4 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 7 7 0 0 0 0 1 1 1
0 2 0 0 0 0 7 7 0 0 0 1 1 0
0 2 2 2 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 2 0 0 4 0 0 0 7
2 2 0 4 4 0 0 7 7
2 0 0 4 0 0 7 7 7
```
