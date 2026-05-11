# ARC Puzzle Bank — Ninth 21 Puzzles
This ninth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`57`–`63`) so it follows directly after the eighth bundle.
This volume leans more heavily into anti-diagonal symmetry, row-level ordering, bbox-overlap abstractions, transform strips, typed relation matrices, hole-count selection, and library-style code lookups.
It also introduces a few reusable solver primitives that fit your pipeline well: `anti_diag_reflect`, `bbox_overlap`, `row_occupancy_sort`, `typed_relation_matrix`, and library-style `select_then_transform` logic.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_ninth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_ninth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_ninth_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_57_complete_anti_diagonal_symmetry` — **Complete the Anti-Diagonal Symmetry**
- `easy_58_cast_vertical_shadows` — **Cast Vertical Shadows to the Floor**
- `easy_59_drop_single_object_to_floor` — **Drop the Whole Object to the Floor**
- `easy_60_keep_border_touching_components` — **Keep Only the Border-Touching Components**
- `easy_61_read_nonempty_rows_as_column` — **Read the Nonempty Rows as a Color Column**
- `easy_62_markers_to_keyed_shapes` — **Expand the Markers into Keyed Shapes**
- `easy_63_complete_2x2_from_diagonal_pairs` — **Complete 2×2 Squares from Diagonal Pairs**

### Medium (7)
- `medium_57_sort_rows_by_occupancy` — **Sort the Rows by Occupancy**
- `medium_58_fill_bbox_overlap_by_key` — **Fill the Overlap of the Two Bounding Boxes**
- `medium_59_transform_strip_from_key_row` — **Build the Transform Strip from the Key Row**
- `medium_60_translate_components_to_matching_markers` — **Move Each Component to its Matching Marker**
- `medium_61_order_framed_crops_by_key` — **Order the Framed Crops by their Keys**
- `medium_62_frame_color_presence_matrix` — **Build the Frame-by-Color Presence Matrix**
- `medium_63_crop_unique_180_symmetric_component` — **Crop the Only 180°-Symmetric Component**

### Hard (7)
- `hard_57_frame_select_rank_transform_pack` — **In Each Frame, Select by Size Key, Transform, and Pack**
- `hard_58_template_code_mosaic_recolor` — **Decode a Recolored Transform Mosaic from the Code Grid**
- `hard_59_typed_relation_matrix` — **Build the Typed Shape-and-Color Relation Matrix**
- `hard_60_select_by_hole_count_scale_to_marker` — **Select by Hole Count, Scale, and Move to the Marker**
- `hard_61_local_bbox_overlap_gallery` — **Make a Local Bounding-Box Overlap Gallery**
- `hard_62_library_select_transform_gallery` — **Select from the Library and Transform into a Gallery**
- `hard_63_boolean_gallery_from_two_templates` — **Build the Boolean Gallery from the Two Templates**

## Complete the Anti-Diagonal Symmetry (`easy_57_complete_anti_diagonal_symmetry`)

**Difficulty:** easy

**Skills:** anti-diagonal reflection, symmetry completion, same-size transform

**Scaffold notes:**
- Work on a square grid and identify the anti-diagonal, where row + column is constant.
- For a cell at (r, c), its anti-diagonal mirror lands at (n-1-c, n-1-r).
- Copy every colored cell to that mirrored position without deleting the original.

**Written solution:** Treat each nonzero cell as one half of an anti-diagonal mirror pair. Reflect it across the anti-diagonal of the square grid, keeping the original cell and adding its mirror cell in the same color.

**Program solution (Python reference):**
```python
def solve_easy_57_complete_anti_diagonal_symmetry(g:Grid)->Grid:
    return anti_diag_reflect(g)
```

**Train 1 input**
```text
8 2 0 0 0 0
0 3 4 6 0 0
0 4 0 0 0 0
0 8 0 0 0 0
7 0 0 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0 0 0 0
0 3 4 6 0 0
0 4 0 0 6 0
0 8 0 0 4 0
7 0 8 4 3 2
0 7 0 0 0 8
```

**Train 2 input**
```text
0 0 0 7 0 0 0 0
0 0 0 0 3 0 0 0
0 6 0 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 7 0 0 0 0
0 0 0 0 3 0 0 0
0 6 0 0 0 0 0 0
0 8 0 0 0 0 3 0
0 0 0 0 0 0 0 7
4 0 0 0 0 0 0 0
6 0 0 0 8 6 0 0
0 6 4 0 0 0 0 0
```

**Train 3 input**
```text
0 7 6 0 0 0
2 4 0 7 0 0
0 0 8 0 0 0
0 7 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 3 output**
```text
0 7 6 0 0 0
2 4 0 7 0 0
0 0 8 0 7 0
0 7 0 8 0 6
0 0 7 0 4 7
0 0 0 0 2 0
```

**Train 4 input**
```text
3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0
0 0 6 0 0 0 0 0
0 7 0 2 0 0 0 0
0 6 8 0 0 0 0 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0
0 0 6 0 0 0 0 0
0 7 0 2 0 0 0 0
0 6 8 0 2 0 0 0
0 8 0 8 0 6 3 0
0 0 8 6 7 0 0 0
0 0 0 0 0 0 0 3
```

**Test input**
```text
0 2 0 0 0 0
3 0 3 0 0 0
0 0 8 0 0 0
6 0 0 0 0 0
2 0 0 0 0 0
0 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 0 0
3 0 3 0 0 0
0 0 8 0 0 0
6 0 0 8 3 0
2 0 0 0 0 2
0 2 6 0 3 0
```

## Cast Vertical Shadows to the Floor (`easy_58_cast_vertical_shadows`)

**Difficulty:** easy

**Skills:** vertical propagation, column reasoning, same-size transform

**Scaffold notes:**
- Look at the nonzero cells as starting points.
- Nothing moves sideways; each action stays in one column.
- Extend each seed downward until the grid ends.

**Written solution:** Each colored seed cell casts a vertical shadow straight downward. Fill every cell from the seed’s row to the bottom of the grid in that same column and color.

**Program solution (Python reference):**
```python
def solve_easy_58_vertical_shadows_to_floor(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                for rr in range(r,h):
                    out[rr][c]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 1 0
0 0 0 8 0 0 0
0 0 0 0 6 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 1 0
0 0 0 8 0 1 0
0 0 0 8 6 1 0
0 0 3 8 6 1 0
0 0 3 8 6 1 0
0 4 3 8 6 1 0
0 4 3 8 6 1 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 7 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 7 0 8 0 0 0
0 6 0 7 0 8 0 0 0
0 6 0 7 0 8 0 0 0
0 6 0 7 4 8 0 0 0
0 6 0 7 4 8 0 0 0
```

**Train 3 input**
```text
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 6 0 1 0 0 0 0
0 0 6 0 1 0 0 2 0
0 0 6 0 1 0 3 2 0
0 0 6 0 1 0 3 2 0
0 0 6 0 1 0 3 2 0
```

**Train 4 input**
```text
0 1 0 0 0 0 0
0 0 7 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 3 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 1 0 0 0 0 0
0 1 7 0 0 0 0
0 1 7 0 0 0 0
0 1 7 0 2 0 0
0 1 7 0 2 3 0
0 1 7 0 2 3 0
0 1 7 0 2 3 0
```

**Test input**
```text
0 0 4 0 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 0 0 1 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test output**
```text
0 0 4 0 0 0 0
0 0 4 7 0 0 0
0 0 4 7 0 0 0
0 2 4 7 0 0 0
0 2 4 7 8 0 0
0 2 4 7 8 1 0
0 2 4 7 8 1 0
0 2 4 7 8 1 0
```

## Drop the Whole Object to the Floor (`easy_59_drop_single_object_to_floor`)

**Difficulty:** easy

**Skills:** whole-object translation, connected components, gravity-like motion

**Scaffold notes:**
- Do not let individual cells fall independently.
- Find the object’s lowest occupied row.
- Translate the whole component down by one constant offset.

**Written solution:** There is one connected colored object. Move that entire object straight downward, preserving its shape exactly, until its lowest cell touches the bottom row.

**Program solution (Python reference):**
```python
def solve_easy_59_drop_single_object_to_floor(g:Grid)->Grid:
    h,w=dims(g)
    cells=nonzero_cells(g)
    if not cells:
        return clone(g)
    shift=h-1-max(r for r,c in cells)
    out=zeros(h,w)
    for r,c in cells:
        out[r+shift][c]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 0 0 0 0 0
0 0 4 4 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 6 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0
0 7 7 7 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0
0 7 7 7 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 8 8 8
0 0 0 0 8 0 0
0 0 0 0 8 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 8 8
0 0 0 0 8 0 0
0 0 0 0 8 0 0
```

**Test input**
```text
0 0 0 0 0 0 0
6 6 0 0 0 0 0
6 6 0 0 0 0 0
6 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
6 6 0 0 0 0 0
6 6 0 0 0 0 0
6 0 0 0 0 0 0
```

## Keep Only the Border-Touching Components (`easy_60_keep_border_touching_components`)

**Difficulty:** easy

**Skills:** component detection, border reasoning, filtering

**Scaffold notes:**
- Treat disconnected colored regions as separate objects.
- Check whether any cell of an object lies on the top, bottom, left, or right border.
- Copy only those qualifying objects to the output.

**Written solution:** Split the grid into connected components. Keep exactly the components that touch the outer border of the grid, and erase every fully interior component.

**Program solution (Python reference):**
```python
def solve_easy_60_keep_border_touching_components(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp["cells"]):
            for r,c in comp["cells"]:
                out[r][c]=comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 4 4 4 7 0 0 0
0 0 4 0 0 7 0 0 0
0 0 4 0 0 7 7 0 3
0 0 0 0 0 0 0 0 3
0 0 6 0 0 0 0 0 3
0 6 6 6 0 0 0 2 0
0 0 6 0 0 0 0 2 0
0 0 0 0 0 0 0 2 2
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 3
0 4 4 0 0 0 0 3
0 0 6 0 0 0 0 3
0 6 6 6 0 0 0 0
0 7 6 0 0 0 0 0
0 7 0 0 0 0 2 2
0 7 7 0 0 0 2 2
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2
0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0
0 0 6 0 0 7 7 0
0 0 6 0 0 7 0 0
0 0 6 6 0 0 0 0
0 0 0 0 4 4 4 0
0 0 0 0 4 0 3 0
0 0 2 2 4 0 3 0
0 0 2 2 0 0 3 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 2 2 0 0 3 0
0 0 2 2 0 0 3 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
2 7 7 4 4 4 0 0 0
2 7 7 0 4 0 0 0 0
2 2 0 0 6 6 6 0 0
0 0 0 0 6 3 0 0 0
0 0 0 0 6 3 0 0 0
0 0 0 0 0 3 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 0 0 0
```

**Test input**
```text
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 6 6 4 0 0 0
0 7 7 6 6 4 0 0 0
0 7 7 6 0 4 4 0 0
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Read the Nonempty Rows as a Color Column (`easy_61_read_nonempty_rows_as_column`)

**Difficulty:** easy

**Skills:** row scanning, size change, order preservation

**Scaffold notes:**
- First decide which rows matter at all.
- Every nonempty row contributes exactly one color to the answer.
- The output is a column, not a same-size grid.

**Written solution:** Ignore empty rows. For each nonempty row, read its color and write that color into a single-cell row of a new one-column output, preserving the original top-to-bottom order of the nonempty rows.

**Program solution (Python reference):**
```python
def solve_easy_61_read_row_colors_into_column(g:Grid)->Grid:
    out=[]
    for row in g:
        vals=[v for v in row if v!=0]
        if vals:
            out.append([vals[0]])
    return out if out else [[0]]
```

**Train 1 input**
```text
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 6 6 6
1 1 1 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0
```

**Train 1 output**
```text
3
6
1
7
4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6
3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0
0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0
```

**Train 2 output**
```text
6
3
2
7
8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0
0 0 0 2 2 2 2 0
4 4 4 4 0 0 0 0
```

**Train 3 output**
```text
7
2
4
```

**Train 4 input**
```text
0 0 0 0 0 0 0
2 2 2 0 0 0 0
0 0 0 0 0 0 0
7 7 0 0 0 0 0
0 0 0 1 1 1 1
6 6 6 0 0 0 0
```

**Train 4 output**
```text
2
7
1
6
```

**Test input**
```text
0 0 0 0 0 2 2 0 0
8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 6 6 6 0 0
```

**Test output**
```text
2
8
3
6
```

## Expand the Markers into Keyed Shapes (`easy_62_markers_to_keyed_shapes`)

**Difficulty:** easy

**Skills:** local stamping, color-key mapping, shape expansion

**Scaffold notes:**
- The marker cell is the center of the output shape.
- Learn the color-to-shape mapping from the training pairs.
- Apply the correct local stencil independently to every marker.

**Written solution:** Each marker color names a different local shape: red(2) becomes a horizontal 3-cell bar, green(3) becomes a vertical 3-cell bar, and yellow(4) becomes a 5-cell plus. Replace every marker by its keyed shape in the same color.

**Program solution (Python reference):**
```python
def solve_easy_62_markers_to_keyed_shapes(g:Grid)->Grid:
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2:
                for dc in (-1,0,1):
                    out[r][c+dc]=2
            elif v==3:
                for dr in (-1,0,1):
                    out[r+dr][c]=3
            elif v==4:
                for dr,dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
                    out[r+dr][c+dc]=4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
0 3 0 0 2 0 4 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 0
0 3 0 0 0 3 4 0
0 3 0 2 2 4 4 4
0 4 0 0 0 0 4 0
4 4 4 0 0 0 0 0
0 4 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 0 0 0 0 0 0 0
4 4 4 0 0 0 2 2 2
0 4 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 4 3 0 3 0 0
0 0 4 4 4 0 3 0 0
0 0 0 4 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
0 3 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 3 0
0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
0 3 0 4 4 4 0
0 3 0 0 4 0 0
0 3 0 4 0 3 0
0 0 4 4 4 3 0
0 0 0 4 0 3 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 3 0 0 0 0 2 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
2 3 2 0 0 0 0 0 0
0 3 0 0 0 2 2 4 0
0 3 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 0
```

**Test input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 0 0 4 0 0
0 0 3 3 0 0 0
0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 4 0 0
0 0 3 3 4 4 0
0 0 3 3 4 0 0
0 0 3 3 0 0 0
```

## Complete 2×2 Squares from Diagonal Pairs (`easy_63_complete_2x2_from_diagonal_pairs`)

**Difficulty:** easy

**Skills:** local window reasoning, 2×2 completion, same-color grouping

**Scaffold notes:**
- Inspect 2×2 windows rather than full objects.
- Only diagonal same-color pairs trigger a change.
- When a window matches, fill all four cells.

**Written solution:** Find each 2×2 window where the two colored cells occupy opposite corners and share the same color. Fill the other two corners so that the whole 2×2 block becomes solid in that color.

**Program solution (Python reference):**
```python
def solve_easy_63_complete_2x2_from_diagonal_pairs(g:Grid)->Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            non=[v for v in vals if v!=0]
            if len(non)==2 and len(set(non))==1:
                if (g[r][c]!=0 and g[r+1][c+1]!=0 and g[r][c+1]==0 and g[r+1][c]==0) or \
                   (g[r][c+1]!=0 and g[r+1][c]!=0 and g[r][c]==0 and g[r+1][c+1]==0):
                    color=non[0]
                    out[r][c]=out[r][c+1]=out[r+1][c]=out[r+1][c+1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 7 0
0 0 2 0 7 0 0
0 2 0 0 0 3 0
0 0 0 0 0 0 3
0 0 0 0 0 0 0
0 0 6 0 0 0 0
0 0 0 6 0 0 0
```

**Train 1 output**
```text
0 0 0 0 7 7 0
0 2 2 0 7 7 0
0 2 2 0 0 3 3
0 0 0 0 0 3 3
0 0 0 0 0 0 0
0 0 6 6 0 0 0
0 0 6 6 0 0 0
```

**Train 2 input**
```text
0 0 8 0 0 0 0 0
0 0 6 8 0 0 0 0
0 6 0 0 0 0 0 0
0 0 0 0 1 0 0 0
0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 8 0 0 0 0 0
0 6 6 8 0 0 0 0
0 6 6 0 0 0 0 0
0 0 0 1 1 0 0 0
0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0
0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 3 0 0 0
0 0 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 8 0 2 0
0 0 8 0 2 0 0
```

**Train 3 output**
```text
0 0 3 3 0 0 0
0 0 3 3 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 8 8 2 2 0
0 0 8 8 2 2 0
```

**Train 4 input**
```text
0 0 0 0 0 7 0 0
0 0 0 0 7 0 2 0
0 0 0 0 0 2 0 0
4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 7 7 0 0
0 0 0 0 7 2 2 0
0 0 0 0 0 2 2 0
4 4 0 0 0 0 0 0
4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 3 0 0 0 0 0 0
3 0 0 0 0 0 4 0
0 0 7 0 0 4 0 0
0 2 0 7 0 0 0 0
0 0 2 0 0 0 0 0
0 6 0 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
3 3 0 0 0 0 0 0
3 3 0 0 0 4 4 0
0 0 7 7 0 4 4 0
0 2 2 7 0 0 0 0
0 2 2 0 0 0 0 0
0 6 6 0 0 0 0 0
0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Sort the Rows by Occupancy (`medium_57_sort_rows_by_occupancy`)

**Difficulty:** medium

**Skills:** row reordering, counting, same-size transform

**Scaffold notes:**
- The colored patterns inside rows do not change.
- The only thing that changes is row order.
- Use nonzero count as the sorting key.

**Written solution:** Count the number of nonzero cells in each row. Reorder the rows from most occupied to least occupied, preserving each row’s internal pattern exactly.

**Program solution (Python reference):**
```python
def solve_medium_57_sort_rows_by_occupancy(g:Grid)->Grid:
    rows=sorted(g, key=lambda row: sum(v!=0 for v in row), reverse=True)
    return [row[:] for row in rows]
```

**Train 1 input**
```text
0 0 0 0 0 4 0 0 0
6 6 0 6 6 0 0 0 0
8 8 8 8 0 8 8 8 0
1 1 1 1 1 0 0 0 0
0 0 0 0 0 2 2 2 0
4 4 4 4 4 0 4 0 0
4 4 4 4 4 4 4 4 0
```

**Train 1 output**
```text
4 4 4 4 4 4 4 4 0
8 8 8 8 0 8 8 8 0
4 4 4 4 4 0 4 0 0
1 1 1 1 1 0 0 0 0
6 6 0 6 6 0 0 0 0
0 0 0 0 0 2 2 2 0
0 0 0 0 0 4 0 0 0
```

**Train 2 input**
```text
0 0 0 6 6 6 0 0
0 0 1 0 0 0 0 0
0 0 8 8 8 8 0 0
0 4 4 4 4 4 4 0
7 7 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 4 4 4 4 4 0
0 0 8 8 8 8 0 0
0 0 0 6 6 6 0 0
7 7 0 0 0 0 0 0
0 0 1 0 0 0 0 0
```

**Train 3 input**
```text
0 0 3 3 0 3 3 3
0 0 0 0 1 1 1 0
0 7 7 7 7 7 7 0
8 8 8 8 8 0 8 8
0 0 0 0 0 0 0 7
0 0 0 0 0 0 8 8
8 8 8 8 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8 8 0 8 8
0 7 7 7 7 7 7 0
0 0 3 3 0 3 3 3
8 8 8 8 0 0 0 0
0 0 0 0 1 1 1 0
0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 7
```

**Train 4 input**
```text
0 7 7 7 7 0 0 0
0 0 2 2 2 2 2 0
2 2 2 2 0 2 2 2
0 0 0 0 0 0 6 0
0 4 4 4 0 4 4 4
```

**Train 4 output**
```text
2 2 2 2 0 2 2 2
0 4 4 4 0 4 4 4
0 0 2 2 2 2 2 0
0 7 7 7 7 0 0 0
0 0 0 0 0 0 6 0
```

**Test input**
```text
7 7 7 7 7 7 0 7 7 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 0 0 0 0
0 6 6 6 6 6 6 6 6 6
```

**Test output**
```text
0 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 0 7 7 0
7 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 7
```

## Fill the Overlap of the Two Bounding Boxes (`medium_58_fill_bbox_overlap_by_key`)

**Difficulty:** medium

**Skills:** bounding boxes, region intersection, keyed recoloring

**Scaffold notes:**
- Ignore the exact interior geometry once the boxes are known.
- You need two boxes first, then their intersection.
- The singleton color tells you what color to paint the overlap.

**Written solution:** Compute the bounding box of the red(2) shape and the bounding box of the blue(1) shape. Take their rectangular overlap and fill that overlap with the singleton key color, leaving everything else blank.

**Program solution (Python reference):**
```python
def solve_medium_58_fill_bbox_overlap_by_key(g:Grid)->Grid:
    h,w=dims(g)
    red=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    blue=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1]
    key=[g[r][c] for r in range(h) for c in range(w) if g[r][c] not in (0,1,2)][0]
    rr0,rc0,rr1,rc1=bbox(red)
    br0,bc0,br1,bc1=bbox(blue)
    r0=max(rr0,br0); c0=max(rc0,bc0); r1=min(rr1,br1); c1=min(rc1,bc1)
    out=zeros(h,w)
    if r0<=r1 and c0<=c1:
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=key
    return out
```

**Train 1 input**
```text
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 1 0 0 0
0 0 0 0 2 1 1 0 0
0 0 0 0 2 2 1 1 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 0 0
0 0 0 2 0 2 1 1 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 1 0
0 0 0 0 2 1 1 1 0
0 0 0 0 2 0 0 0 0
0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
7 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0
0 0 0 1 1 0 0 0
0 2 2 2 1 1 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 1 1 1 0 0 0 0
0 2 0 1 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Build the Transform Strip from the Key Row (`medium_59_transform_strip_from_key_row`)

**Difficulty:** medium

**Skills:** cropping, transform lookup, gallery construction

**Scaffold notes:**
- Separate the source object from the control row.
- Learn the transform attached to each key color.
- The output is a packed gallery in key order.

**Written solution:** Crop the source object above the key row. Then read the key row left to right: 2 means identity, 3 means rotate clockwise, 4 means rotate 180°, and 5 means flip horizontally. Apply each transform to the source crop and place the results in a horizontal strip.

**Program solution (Python reference):**
```python
def solve_medium_59_transform_strip_from_key_row(g:Grid)->Grid:
    h,w=dims(g)
    keys=[v for v in g[h-1] if v!=0]
    source=[[g[r][c] if r<h-1 else 0 for c in range(w)] for r in range(h-1)]
    source=crop_nonzero(source)
    out_parts=[]
    for k in keys:
        tg=apply_transform(source, k)
        out_parts.append(tg)
    return hstack(out_parts, gap=1)
```

**Train 1 input**
```text
0 1 1 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 0 5 0 0 3
```

**Train 1 output**
```text
1 1 0 1 1 0 1 1 0 1 1 1
1 1 0 1 1 0 1 1 0 0 1 1
1 0 0 1 0 0 1 0 0 0 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 0 0 3 3 0 4 0 0
```

**Train 2 output**
```text
2 0 0 2 2 2 0 2 2 2 0 2 2
2 0 0 2 0 0 0 2 0 0 0 0 2
2 2 0 0 0 0 0 0 0 0 0 0 2
```

**Train 3 input**
```text
4 0 4 0 0 0 0
4 4 4 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 0 0 3 4 0 0
```

**Train 3 output**
```text
4 0 4 0 4 4 0 4 4 4
4 4 4 0 4 0 0 4 0 4
0 0 0 0 4 4 0 0 0 0
```

**Train 4 input**
```text
3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 2 3
```

**Train 4 output**
```text
3 3 3 0 3 3 3 0 3 3 0 3 3 3
0 3 3 0 0 3 3 0 3 3 0 0 3 3
0 0 0 0 0 0 0 0 3 0 0 0 0 0
```

**Test input**
```text
1 1 0 0 0 0 0
1 1 0 0 0 0 0
1 0 0 0 0 0 0
0 0 0 0 0 0 0
0 3 0 0 2 0 5
```

**Test output**
```text
1 1 1 0 1 1 0 1 1
0 1 1 0 1 1 0 1 1
0 0 0 0 1 0 0 1 0
```

## Move Each Component to its Matching Marker (`medium_60_translate_components_to_matching_markers`)

**Difficulty:** medium

**Skills:** component matching, translation, color correspondence

**Scaffold notes:**
- Within each color, distinguish the object from the marker by size.
- The marker does not describe a new shape; it gives the destination.
- Use one translation vector per color.

**Written solution:** For each color, match the large component of that color with the singleton marker of the same color. Translate the whole component so that its bounding box’s top-left corner lands on the marker cell, and remove the original placement.

**Program solution (Python reference):**
```python
def solve_medium_60_translate_components_to_matching_markers(g:Grid)->Grid:
    h,w=dims(g)
    comps=connected_components(g)
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp["color"]].append(comp)
    out=zeros(h,w)
    for color,items in by_color.items():
        marker=min(items, key=lambda comp: comp["area"])
        obj=max(items, key=lambda comp: comp["area"])
        mr,mc=marker["cells"][0]
        r0,c0,r1,c1=obj["bbox"]
        dr,dc=mr-r0,mc-c0
        for r,c in obj["cells"]:
            out[r+dr][c+dc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 2 2
0 3 0 0 2 0 0 0 2 2
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 2 2 0 0 0 0
0 3 3 0 2 2 0 0 0 0
0 3 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0
4 0 2 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 2 0 0 0 0 3 3 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 4 4 4 0 0 0 0
0 0 3 3 4 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 4 2 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 2 2 0 0 6 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 4 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 2 0 0 0 0 0
0 0 4 4 0 0 0 2 0 0 0
0 0 4 4 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 4 4 0 0 0
0 0 3 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 4 2 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 3 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Order the Framed Crops by their Keys (`medium_61_order_framed_crops_by_key`)

**Difficulty:** medium

**Skills:** frame parsing, crop extraction, key-based ordering

**Scaffold notes:**
- Treat each frame as its own local region.
- Ignore the frame border in the output; only the interior object matters.
- The keys determine output order, not the original positions.

**Written solution:** Read each framed subtask independently. For every frame, crop the interior object tightly, read the key above the frame, and then pack the crops left to right in ascending key order.

**Program solution (Python reference):**
```python
def solve_medium_61_order_framed_crops_by_key(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        key_cells=[g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c]!=0 and g[r0-1][c]!=9]
        key=key_cells[0]
        interior=crop_interior(g,fr)
        part=crop_nonzero([[0 if v==9 else v for v in row] for row in interior])
        parts.append((key,part))
    parts.sort(key=lambda kp: kp[0])
    return hstack([p for _,p in parts], gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 4 0 0 0 0 0 2 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 2 0 0 9 0 9 4 4 0 9 0 9 6 0 6 9
0 9 2 0 0 9 0 9 4 4 0 9 0 9 6 6 6 9
0 9 2 2 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 0 6 0 2 0 0 4 4
6 6 6 0 2 0 0 4 4
0 0 0 0 2 2 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 3 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 4 4 4 9 0 9 0 1 1 9 0 9 0 0 0 9
0 9 4 0 0 9 0 9 0 1 1 9 0 9 0 2 2 9
0 9 4 0 0 9 0 9 0 0 0 9 0 9 0 2 2 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 0 2 2 0 1 1
4 0 0 0 2 2 0 1 1
4 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 4 0 0 0 0 0 2 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 1 1 1 9 0 9 3 3 3 9 0 9 0 0 0 9
0 9 1 0 0 9 0 9 0 3 0 9 0 9 4 4 0 9
0 9 1 0 0 9 0 9 0 0 0 9 0 9 4 4 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 0 1 1 1 0 3 3 3
4 4 0 1 0 0 0 0 3 0
0 0 0 1 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 3 0 0 0 0 0 4 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 3 3 3 9 0 9 7 0 7 9 0 9 6 6 0 9
0 9 0 3 0 9 0 9 7 7 7 9 0 9 6 6 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 3 0 7 0 7 0 6 6
0 3 0 0 7 7 7 0 6 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 4 0 0 0 0 0 2 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 4 4 4 9 0 9 0 0 0 9 0 9 6 6 6 9
0 9 4 0 0 9 0 9 1 1 1 9 0 9 6 0 0 9
0 9 4 0 0 9 0 9 0 1 0 9 0 9 6 0 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 6 6 0 4 4 4 0 1 1 1
6 0 0 0 4 0 0 0 0 1 0
6 0 0 0 4 0 0 0 0 0 0
```

## Build the Frame-by-Color Presence Matrix (`medium_62_frame_color_presence_matrix`)

**Difficulty:** medium

**Skills:** frame parsing, set membership, matrix construction

**Scaffold notes:**
- Read the palette once; it fixes the output columns.
- Each frame contributes one output row.
- This is a presence/absence summary, not a count.

**Written solution:** The top palette row lists the colors to check. For each frame, inspect its interior and mark a matrix row where a palette color is written if that color appears inside the frame, otherwise 0.

**Program solution (Python reference):**
```python
def solve_medium_62_frame_color_presence_matrix(g:Grid)->Grid:
    palette=[v for v in g[0] if v!=0 and v!=9]
    frames=find_frames(g,9)
    rows=[]
    for fr in frames:
        interior=crop_interior(g,fr)
        colors=set(v for row in interior for v in row if v not in (0,9))
        rows.append([col if col in colors else 0 for col in palette])
    return rows
```

**Train 1 input**
```text
0 0 3 0 0 8 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 0 0 9 0 9 4 0 3 9 0 9 4 0 3 9
0 9 0 0 0 9 0 9 0 0 3 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 4 0 0 9 0 9 0 0 8 9 0 9 0 0 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 4
3 8 4
3 0 4
```

**Train 2 input**
```text
0 0 8 0 0 4 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 0 0 9 0 9 7 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 7 0 8 9 0 9 0 0 0 9 0 9 0 0 7 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 7
0 0 7
0 0 7
```

**Train 3 input**
```text
0 0 8 0 0 4 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 4 0 0 9 0 9 0 0 8 9 0 9 8 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 8 0 0 9
0 9 0 8 0 9 0 9 0 4 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 1 0 0 9 0 9 0 0 1 9 0 9 0 0 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 4 1
8 4 1
8 0 0
```

**Train 4 input**
```text
0 0 3 0 0 8 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 0 0 9 0 9 0 0 6 9 0 9 0 0 3 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 3 9
0 9 0 3 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 3 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 6 0 8 9 0 9 8 0 3 9 0 9 0 0 0 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 8 6
3 8 6
3 0 0
```

**Test input**
```text
0 0 4 0 0 3 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 0 0 0 9 0 9 0 6 0 9 0 9 0 4 0 9
0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 0 0 9
0 9 3 0 0 9 0 9 3 0 0 9 0 9 0 0 3 9
0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 3 0
0 3 6
4 3 0
```

## Crop the Only 180°-Symmetric Component (`medium_63_crop_unique_180_symmetric_component`)

**Difficulty:** medium

**Skills:** shape symmetry, component filtering, cropping

**Scaffold notes:**
- Compare shapes after cropping away empty background.
- The test is rotational symmetry by 180°, not mirror symmetry.
- Exactly one component satisfies the rule in each puzzle.

**Written solution:** Find the connected component whose cropped binary shape is unchanged by a 180° rotation. Discard the others and output a tight crop of that unique component.

**Program solution (Python reference):**
```python
def solve_medium_63_crop_unique_180_symmetric_component(g:Grid)->Grid:
    good=[]
    for comp in connected_components(g):
        crop=crop_bbox(g, comp["bbox"])
        crop=[[comp["color"] if (r+comp["bbox"][0], c+comp["bbox"][1]) in set(comp["cells"]) else 0 for c in range(len(crop[0]))] for r,row in enumerate(crop)]
        norm=normalize_shape(crop)
        if rotate_180(norm)==norm:
            good.append(crop_nonzero(crop))
    # exactly one by construction
    return good[0]
```

**Train 1 input**
```text
0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 2 2
0 0 0 4 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2
2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 3 3 3
0 0 0 0 4 4 0 0 0 0
0 0 0 0 4 4 2 2 0 0
0 0 0 0 4 2 2 0 0 0
```

**Train 2 output**
```text
0 2 2
2 2 0
```

**Train 3 input**
```text
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2
2 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 2 2 0 0 0 0
0 0 0 0 2 2 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 2 2
2 2 0
```

**Test input**
```text
0 4 4 0 0 0 0 0 0 0
0 4 4 3 0 0 2 2 0 0
0 4 0 3 3 0 0 2 2 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 0
0 2 2
```

## In Each Frame, Select by Size Key, Transform, and Pack (`hard_57_frame_select_rank_transform_pack`)

**Difficulty:** hard

**Skills:** local frame reasoning, rank selection, local transforms, gallery packing

**Scaffold notes:**
- There are two local decisions per frame: which object and which transform.
- Use area to decide smaller versus larger.
- After the local work, assemble one global strip.

**Written solution:** Handle each frame separately. The top key chooses whether to keep the smaller or larger interior component; the left key chooses the transform (rotate clockwise, flip horizontally, or rotate 180°). After selecting and transforming the chosen component, crop it tightly and pack the results into a horizontal strip in frame order.

**Program solution (Python reference):**
```python
def solve_hard_57_frame_select_rank_transform_pack(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        sel=[g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9)]
        tr=[g[r][c0-1] for r in range(r0,r1+1) if c0-1>=0 and g[r][c0-1] not in (0,9)]
        sel_key=sel[0]; tr_key=tr[0]
        ibox=interior_box(fr)
        ir0,ic0,ir1,ic1=ibox
        sub=[row[ic0:ic1+1] for row in g[ir0:ir1+1]]
        comps=connected_components(sub)
        comps.sort(key=lambda comp: comp["area"])
        chosen=comps[0] if sel_key==2 else comps[-1]
        part=zeros(ir1-ir0+1, ic1-ic0+1)
        for r,c in chosen["cells"]:
            part[r][c]=chosen["color"]
        part=crop_nonzero(part)
        if tr_key==4:
            part=rotate_cw(part)
        elif tr_key==5:
            part=flip_h(part)
        elif tr_key==6:
            part=rotate_180(part)
        parts.append(part)
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 0 0 0 1 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 3 3 3 0 0 9 0 0 9 0 0 0 1 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 3 0 3 0 0 9 0 0 9 0 0 0 1 1 9 0 0 9 0 6 0 3 0 9 0 0
0 4 9 3 0 3 0 0 9 0 5 9 0 0 0 0 0 9 0 5 9 6 6 6 3 0 9 0 0
0 0 9 0 0 3 0 0 9 0 0 9 0 1 0 1 0 9 0 0 9 0 6 0 3 3 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 0 1 1 1 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 3 3 3 0 0 1 0 0 3
0 0 0 3 0 0 1 0 0 3
3 3 3 3 0 1 1 0 3 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 9 0 0 0 7 0 9 0 0 9 0 0 0 0 0 9 0 0 9 0 7 0 0 0 9 0 0
0 0 9 0 0 7 7 7 9 0 0 9 4 4 0 0 0 9 0 0 9 0 7 0 0 0 9 0 0
0 0 9 0 0 1 7 0 9 0 0 9 4 4 0 0 0 9 0 0 9 0 7 7 0 0 9 0 0
0 5 9 0 0 1 0 0 9 0 6 9 1 1 1 0 0 9 0 6 9 0 0 1 0 0 9 0 0
0 0 9 0 0 1 1 0 9 0 0 9 1 0 0 0 0 9 0 0 9 0 0 1 1 0 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 1 0 0 0 0 9 0 0 9 0 0 0 1 1 9 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 1 0 0 0 1 0 1 1 0
0 1 0 0 0 1 0 0 1 1
1 1 0 1 1 1 0 0 0 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 9 0 0 0 6 6 9 0 0 9 0 0 0 0 3 9 0 0 9 4 0 4 4 0 9 0 0
0 0 9 0 0 0 6 6 9 0 0 9 0 0 0 0 3 9 0 0 9 4 0 4 4 0 9 0 0
0 0 9 0 0 0 6 3 9 0 0 9 4 0 0 0 3 9 0 0 9 4 4 4 0 0 9 0 0
0 6 9 0 0 0 0 3 9 0 4 9 4 4 0 0 0 9 0 5 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 3 9 0 0 9 0 4 4 0 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 0 0 0 0 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 0 4 4 0 4 4 0 4
3 0 4 4 0 0 4 4 0 4
3 0 4 0 0 0 0 4 4 4
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 9 4 4 4 0 0 9 0 0 9 0 0 0 0 0 9 0 0 9 1 1 1 0 0 9 0 0
0 0 9 4 0 0 0 0 9 0 0 9 0 3 3 3 0 9 0 0 9 1 0 0 0 0 9 0 0
0 0 9 4 6 0 0 0 9 0 0 9 0 3 7 0 0 9 0 0 9 1 0 0 0 0 9 0 0
0 4 9 0 6 0 0 0 9 0 6 9 0 3 7 0 0 9 0 5 9 0 3 0 0 0 9 0 0
0 0 9 0 6 6 0 0 9 0 0 9 0 0 7 7 0 9 0 0 9 0 3 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 0 0 0 0 0 9 0 0 9 0 3 3 0 0 9 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
4 4 4 0 0 0 3 0 1 1 1
0 0 4 0 0 0 3 0 0 0 1
0 0 4 0 3 3 3 0 0 0 1
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 9 0 0 0 0 0 9 0 0 9 0 2 2 0 0 9 0 0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 7 0 9 0 0 9 0 2 2 0 0 9 0 0 9 0 6 6 0 0 9 0 0
0 0 9 0 0 7 7 7 9 0 0 9 0 0 0 7 0 9 0 0 9 0 6 6 0 0 9 0 0
0 6 9 0 0 6 7 0 9 0 4 9 0 0 7 7 7 9 0 5 9 0 0 7 0 0 9 0 0
0 0 9 0 0 6 0 0 9 0 0 9 0 0 0 7 0 9 0 0 9 0 7 7 7 0 9 0 0
0 0 9 0 0 6 6 0 9 0 0 9 0 0 0 0 0 9 0 0 9 0 0 7 0 0 9 0 0
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 7 0 0 2 2 0 6 6
7 7 7 0 2 2 0 6 6
0 7 0 0 0 0 0 0 0
```

## Decode a Recolored Transform Mosaic from the Code Grid (`hard_58_template_code_mosaic_recolor`)

**Difficulty:** hard

**Skills:** template extraction, transform lookup, mosaic construction, recoloring

**Scaffold notes:**
- Separate the source template from the smaller code grid.
- One code controls both geometry and color.
- Expand the small code grid into a larger tile mosaic.

**Written solution:** Extract the source template made of color 1. Each code color in the code grid chooses a transform of that template and also supplies the output color: 2 = identity, 3 = rotate clockwise, 4 = rotate 180°, 5 = flip horizontally. Replace every code cell by the corresponding transformed, recolored tile and arrange them in the code-grid layout.

**Program solution (Python reference):**
```python
def solve_hard_58_template_code_mosaic_recolor(g:Grid)->Grid:
    h,w=dims(g)
    # source uses color 1, code cells use 2-5
    source=crop_nonzero([[1 if g[r][c]==1 else 0 for c in range(w)] for r in range(h)])
    codes=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (2,3,4,5)]
    rs=[r for r,c,v in codes]; cs=[c for r,c,v in codes]
    r0,c0,r1,c1=min(rs),min(cs),max(rs),max(cs)
    code_grid=[[g[r][c] if g[r][c] in (2,3,4,5) else 0 for c in range(c0,c1+1)] for r in range(r0,r1+1)]
    tiles=[]
    for row in code_grid:
        row_tiles=[]
        for code in row:
            if code==0:
                row_tiles.append(zeros(len(source), len(source[0])))
            else:
                if code==2:
                    part=clone(source)
                elif code==3:
                    part=rotate_cw(source)
                elif code==4:
                    part=rotate_180(source)
                elif code==5:
                    part=flip_h(source)
                part=recolor_nonzero(part, code)
                row_tiles.append(part)
        tiles.append(hstack(row_tiles, gap=1))
    return vstack(tiles, gap=1)
```

**Train 1 input**
```text
0 1 0 0 0 0 5 5
0 1 0 0 0 0 5 3
0 1 1 0 0 0 2 2
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 5 0 0 5 0
0 5 0 0 5 0
5 5 0 5 5 0
0 0 0 0 0 0
0 5 0 3 3 3
0 5 0 3 0 0
5 5 0 0 0 0
0 0 0 0 0 0
2 0 0 2 0 0
2 0 0 2 0 0
2 2 0 2 2 0
```

**Train 2 input**
```text
0 1 1 0 0 0 3 3 4
0 1 1 0 0 0 5 4 2
0 1 0 0 0 0 4 4 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 0 3 3 3 0 0 4
0 3 3 0 0 3 3 0 4 4
0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 4 0 2 2 0
0 5 5 0 4 4 0 2 2 0
0 0 5 0 4 4 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 4 0 3 3 3 0
4 4 0 4 4 0 0 3 3 0
4 4 0 4 4 0 0 0 0 0
```

**Train 3 input**
```text
1 0 0 0 0 0 3 2 5
1 1 0 0 0 0 5 4 4
0 1 1 0 0 0 3 4 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3 3 0 2 0 0 0 0 0 5
3 3 0 0 2 2 0 0 0 5 5
3 0 0 0 0 2 2 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 4 4 0 0 4 4 0
0 5 5 0 0 4 4 0 0 4 4
5 5 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 4 4 0 0 4 4 0
3 3 0 0 0 4 4 0 0 4 4
3 0 0 0 0 0 4 0 0 0 4
```

**Train 4 input**
```text
0 0 0 0 0 0 2 4 3
1 0 1 0 0 0 3 4 3
1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
2 0 2 0 4 4 4 0 3 3
2 2 2 0 4 0 4 0 3 0
0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0
3 3 0 4 4 4 0 3 3 0
3 0 0 4 0 4 0 3 0 0
3 3 0 0 0 0 0 3 3 0
```

**Test input**
```text
0 1 0 0 0 0 4 3 4
0 1 0 0 0 0 5 4 5
0 1 1 0 0 0 3 4 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
4 4 0 3 3 3 0 4 4 0
0 4 0 3 0 0 0 0 4 0
0 4 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 4 4 0 0 5 0
0 0 5 0 0 4 0 0 5 0
0 5 5 0 0 4 0 5 5 0
0 0 0 0 0 0 0 0 0 0
3 3 3 0 4 4 0 3 3 3
3 0 0 0 0 4 0 3 0 0
0 0 0 0 0 4 0 0 0 0
```

## Build the Typed Shape-and-Color Relation Matrix (`hard_59_typed_relation_matrix`)

**Difficulty:** hard

**Skills:** shape comparison, rotation invariance, relation matrices, color comparison

**Scaffold notes:**
- The frames define the row objects and column objects.
- Shape comparison is rotation-invariant, color comparison is exact.
- The output is a full pairwise relation matrix.

**Written solution:** Compare every left-column framed shape against every top-row framed shape. Write 8 if shape and color both match, 6 if the shapes match up to rotation but the colors differ, 3 if the colors match but the shapes do not, and 0 otherwise.

**Program solution (Python reference):**
```python
def solve_hard_59_typed_relation_matrix(g:Grid)->Grid:
    frames=find_frames(g,9)
    # classify frames: top gallery have minimal top; left gallery have minimal left, excluding corner none
    tops=sorted(set(fr["bbox"][0] for fr in frames))
    lefts=sorted(set(fr["bbox"][1] for fr in frames))
    top_band=min(tops)
    left_band=min(lefts)
    row_frames=[fr for fr in frames if fr["bbox"][0]==top_band]
    col_frames=[fr for fr in frames if fr["bbox"][1]==left_band and fr["bbox"][0]!=top_band]
    row_frames.sort(key=lambda fr: fr["bbox"][1])
    col_frames.sort(key=lambda fr: fr["bbox"][0])
    row_parts=[]; col_parts=[]
    for fr in row_frames:
        interior=crop_nonzero(crop_interior(g,fr))
        row_parts.append(interior)
    for fr in col_frames:
        interior=crop_nonzero(crop_interior(g,fr))
        col_parts.append(interior)
    out=zeros(len(col_parts), len(row_parts))
    for i,a in enumerate(col_parts):
        acol=next(v for row in a for v in row if v!=0)
        for j,b in enumerate(row_parts):
            bcol=next(v for row in b for v in row if v!=0)
            same_shape=same_shape_under_rotation(a,b)
            same_color=(acol==bcol)
            out[i][j]=8 if same_shape and same_color else 6 if same_shape else 3 if same_color else 0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 9 3 3 0 9 0 9 6 0 6 9 0 9 2 0 0 9 0
0 0 0 0 0 0 0 9 3 3 0 9 0 9 6 6 6 9 0 9 2 2 0 9 0
0 0 0 0 0 0 0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 2 2 9 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 4 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 4 4 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 4 4 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 6 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 6 6 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 6 6 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 2 2 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 2 2 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 6
0 3 6
0 0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 9 6 0 6 9 0 9 6 0 6 9 0 9 3 3 3 9 0
0 0 0 0 0 0 0 9 6 6 6 9 0 9 6 6 6 9 0 9 3 0 0 9 0
0 0 0 0 0 0 0 9 0 0 0 9 0 9 0 0 0 9 0 9 3 0 0 9 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 2 0 2 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 2 2 2 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 8 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 8 8 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 0 8 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 8 8 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 0
0 0 0
6 6 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 9 3 3 0 9 0 9 3 3 0 9 0 9 2 0 0 9 0
0 0 0 0 0 0 0 9 3 3 0 9 0 9 0 3 3 9 0 9 2 2 0 9 0
0 0 0 0 0 0 0 9 0 0 0 9 0 9 0 0 0 9 0 9 0 2 2 9 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 7 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 7 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 3 3 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 7 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 7 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 0 0
3 3 0
6 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 9 6 6 0 9 0 9 3 3 0 9 0 9 4 0 0 9 0
0 0 0 0 0 0 0 9 6 6 0 9 0 9 3 3 0 9 0 9 4 0 0 9 0
0 0 0 0 0 0 0 9 0 0 0 9 0 9 3 0 0 9 0 9 4 4 0 9 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 4 4 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 4 4 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 4 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 7 7 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 6 3
0 0 6
0 3 6
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 9 7 7 0 9 0 9 7 7 7 9 0 9 3 3 0 9 0
0 0 0 0 0 0 0 9 7 7 0 9 0 9 7 0 0 9 0 9 3 3 0 9 0
0 0 0 0 0 0 0 9 7 0 0 9 0 9 7 0 0 9 0 9 0 0 0 9 0
0 0 0 0 0 0 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 3 3 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 3 3 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 8 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 8 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 8 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
6 0 3
0 0 3
6 0 0
```

## Select by Hole Count, Scale, and Move to the Marker (`hard_60_select_by_hole_count_scale_to_marker`)

**Difficulty:** hard

**Skills:** hole counting, component selection, scaling, translation

**Scaffold notes:**
- Count enclosed holes in the cropped binary shape.
- Only one component matches the requested hole count.
- After selection, do two more steps: scale, then translate.

**Written solution:** The key color says how many holes the desired component has: 2 means one hole, 3 means two holes. Find the matching component, crop it, scale it by 2 in both directions, and place the scaled result so that its top-left corner lands on the marker cell.

**Program solution (Python reference):**
```python
def solve_hard_60_select_by_hole_count_scale_to_marker(g:Grid)->Grid:
    h,w=dims(g)
    key=next(v for row in g for v in row if v in (2,3))
    need={2:1,3:2}[key]
    marker=next((r,c) for r in range(h) for c in range(w) if g[r][c]==8)
    comps=[comp for comp in connected_components(g) if comp["color"]==4]
    chosen=None
    for comp in comps:
        part=zeros(h,w)
        for r,c in comp["cells"]:
            part[r][c]=4
        crop=crop_nonzero(part)
        holes=count_holes_binary(normalize_shape(crop))
        if holes==need:
            chosen=crop
            break
    part=scale2(chosen)
    out=zeros(h,w)
    paste(out, part, marker[0], marker[1], transparent=0, allow_overlap=False)
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 4 0 4 0 0 0 4 0 4 0 4 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 4 0 4 0 0 0 4 0 4 0 4 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 0 0 4 4 0 0 4 4 0 0 0
0 4 4 0 0 4 4 0 0 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 4 0 4 0 0 0 4 0 4 0 4 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 4 0 4 0 0 0 4 0 4 0 4 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 0 0 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 4 0 4 0 0 0 4 0 4 0 4 0 0
0 4 4 4 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 0 0 4 4 0 0 4 4 0 0 0
0 4 4 0 0 4 4 0 0 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Make a Local Bounding-Box Overlap Gallery (`hard_61_local_bbox_overlap_gallery`)

**Difficulty:** hard

**Skills:** local frame reasoning, bounding boxes, intersection, gallery packing

**Scaffold notes:**
- Do not mix information across frames.
- Each frame has its own local fill color from the key above.
- The final output is built from the per-frame overlap crops.

**Written solution:** Inside each frame, compute the bounding boxes of the red(2) object and the blue(1) object. Fill their overlapping rectangle with the local key color above that frame, crop the result tightly, and pack all frame results into a horizontal gallery.

**Program solution (Python reference):**
```python
def solve_hard_61_local_bbox_overlap_gallery(g:Grid)->Grid:
    frames=find_frames(g,9)
    parts=[]
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        key=next(g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9))
        interior=crop_interior(g,fr)
        red=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v==2]
        blue=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v==1]
        rr0,rc0,rr1,rc1=bbox(red)
        br0,bc0,br1,bc1=bbox(blue)
        a0=max(rr0,br0); b0=max(rc0,bc0); a1=min(rr1,br1); b1=min(rc1,bc1)
        part=zeros(a1-a0+1,b1-b0+1)
        for r in range(a1-a0+1):
            for c in range(b1-b0+1):
                part[r][c]=key
        parts.append(part)
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 9 1 0 0 0 0 9 0 9 0 2 0 2 0 9 0 9 0 0 0 2 0 9 0
0 9 1 1 0 0 0 9 0 9 0 2 2 2 1 9 0 9 0 0 0 2 0 9 0
0 9 2 1 1 0 0 9 0 9 0 0 0 0 1 9 0 9 0 0 1 2 2 9 0
0 9 2 2 0 0 0 9 0 9 0 0 0 1 1 9 0 9 0 0 1 1 0 9 0
0 9 0 2 2 0 0 9 0 9 0 0 0 0 0 9 0 9 0 0 0 1 1 9 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6 0 7 0 7 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 6 0 0 0 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 9 0 1 1 0 0 9 0 9 0 0 0 1 0 9 0 9 0 0 0 0 0 9 0
0 9 0 1 1 0 0 9 0 9 0 0 0 1 0 9 0 9 0 0 0 0 0 9 0
0 9 0 1 2 0 0 9 0 9 0 2 1 1 0 9 0 9 2 0 2 1 0 9 0
0 9 0 0 2 0 0 9 0 9 0 2 2 0 0 9 0 9 2 2 2 1 0 9 0
0 9 0 0 2 2 0 9 0 9 0 0 2 2 0 9 0 9 0 0 1 1 0 9 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 6 6 0 6
0 0 0 0 0 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 6 0 0 0 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 9 0 0 0 0 0 9 0 9 2 0 0 0 0 9 0 9 2 2 2 0 0 9 0
0 9 0 1 1 1 0 9 0 9 2 2 0 0 0 9 0 9 2 0 0 0 0 9 0
0 9 0 0 1 2 0 9 0 9 0 2 2 1 0 9 0 9 2 0 1 0 0 9 0
0 9 0 0 0 2 0 9 0 9 0 0 0 1 0 9 0 9 0 0 1 1 0 9 0
0 9 0 0 0 2 2 9 0 9 0 0 1 1 0 9 0 9 0 0 0 1 1 9 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 0 6 0 6
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 9 0 0 2 2 2 9 0 9 0 1 1 0 0 9 0 9 0 0 0 0 0 9 0
0 9 0 0 2 1 1 9 0 9 0 1 1 0 0 9 0 9 0 0 1 1 1 9 0
0 9 0 0 2 1 1 9 0 9 0 1 2 0 0 9 0 9 0 2 0 1 0 9 0
0 9 0 0 0 1 0 9 0 9 0 0 2 0 0 9 0 9 0 2 0 0 0 9 0
0 9 0 0 0 0 0 9 0 9 0 0 2 2 0 9 0 9 0 2 2 0 0 9 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 0 8 0 8
8 8 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 7 0 0 0 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 9 0 0 0 0 0 9 0 9 2 2 2 0 0 9 0 9 0 0 0 0 0 9 0
0 9 1 0 2 0 2 9 0 9 2 1 0 0 0 9 0 9 2 2 2 0 0 9 0
0 9 1 1 2 2 2 9 0 9 2 1 0 0 0 9 0 9 2 1 1 1 0 9 0
0 9 0 1 1 0 0 9 0 9 1 1 0 0 0 9 0 9 2 0 1 0 0 9 0
0 9 0 0 0 0 0 9 0 9 0 0 0 0 0 9 0 9 0 0 0 0 0 9 0
0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0 9 9 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 0 6 6 0 7 7
7 0 6 6 0 7 7
```

## Select from the Library and Transform into a Gallery (`hard_62_library_select_transform_gallery`)

**Difficulty:** hard

**Skills:** library lookup, coded selection, transforms, gallery packing

**Scaffold notes:**
- First build the mapping from label color to template.
- Then read the two-row code strip as selector/transform pairs.
- Produce one transformed crop per code column.

**Written solution:** The framed templates at the top form a small library, each named by the key above it. The second-to-last row selects library entries, and the last row supplies transforms (5 = identity, 6 = rotate clockwise, 7 = flip horizontally). For each column of the code strip, take the named template, apply the requested transform, and place the result into a horizontal gallery.

**Program solution (Python reference):**
```python
def solve_hard_62_library_select_transform_gallery(g:Grid)->Grid:
    h,w=dims(g)
    frames=find_frames(g,9)
    library={}
    for fr in frames:
        r0,c0,r1,c1=fr["bbox"]
        if r1 < h-3:  # library frames above code rows
            key=next(g[r0-1][c] for c in range(c0,c1+1) if r0-1>=0 and g[r0-1][c] not in (0,9))
            library[key]=crop_nonzero(crop_interior(g,fr))
    selector_row=[v for v in g[h-2] if v in library]
    transform_row=[v for v in g[h-1] if v in (5,6,7)]
    parts=[]
    for s,t in zip(selector_row, transform_row):
        part=clone(library[s])
        if t==5:
            part=clone(part)
        elif t==6:
            part=rotate_cw(part)
        elif t==7:
            part=flip_h(part)
        parts.append(part)
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 2 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 9 1 1 0 9 0 0 9 8 8 0 9 0 0 9 7 0 0 9 0
0 9 1 1 0 9 0 0 9 8 8 0 9 0 0 9 7 7 0 9 0
0 9 1 0 0 9 0 0 9 8 0 0 9 0 0 9 0 7 7 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 0 2 0 0 0
0 0 0 0 6 0 0 0 0 0 5 0 0 0 0 0 0 7 0 0 0
```

**Train 1 output**
```text
0 7 7 0 7 0 0 0 1 1
7 7 0 0 7 7 0 0 1 1
7 0 0 0 0 7 7 0 0 1
```

**Train 2 input**
```text
0 0 0 2 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 9 0 0 0 9 0 0 9 8 0 0 9 0 0 9 1 0 0 9 0
0 9 1 0 1 9 0 0 9 8 8 0 9 0 0 9 1 0 0 9 0
0 9 1 1 1 9 0 0 9 0 8 8 9 0 0 9 1 1 0 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 0
0 7 0 0 0 0 0 0 5 0 0 0 0 0 7 0 0 0 0 0 0
```

**Train 2 output**
```text
0 1 0 1 0 0 0 1
0 1 0 1 0 0 0 1
1 1 0 1 1 0 1 1
```

**Train 3 input**
```text
0 0 0 2 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 1 1 1 9 0 0 9 3 0 3 9 0 0 9 6 6 6 9 0
0 9 0 1 0 9 0 0 9 3 3 3 9 0 0 9 0 6 0 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0 0
0 0 5 0 0 0 0 0 0 5 0 0 0 0 0 0 6 0 0 0 0
```

**Train 3 output**
```text
3 0 3 0 3 0 3 0 0 6
3 3 3 0 3 3 3 0 6 6
0 0 0 0 0 0 0 0 0 6
```

**Train 4 input**
```text
0 0 0 2 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 9 7 0 0 9 0 0 9 0 0 0 9 0 0 9 3 3 3 9 0
0 9 7 0 0 9 0 0 9 7 0 7 9 0 0 9 3 0 0 9 0
0 9 7 7 0 9 0 0 9 7 7 7 9 0 0 9 3 0 0 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 3 4 0 4 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 7 5 0 6 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
3 3 3 0 7 0 7 0 3 3 3 0 3 3 3
3 0 0 0 7 7 7 0 3 0 0 0 0 0 3
3 0 0 0 0 0 0 0 3 0 0 0 0 0 3
```

**Test input**
```text
0 0 0 2 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 1 0 0 9 0
0 9 1 0 1 9 0 0 9 2 0 2 9 0 0 9 1 1 0 9 0
0 9 1 1 1 9 0 0 9 2 2 2 9 0 0 9 0 1 1 9 0
0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0
0 9 9 9 9 9 0 0 9 9 9 9 9 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 5 0 0 0 6 0 0 0
```

**Test output**
```text
2 0 2 0 1 0 1 0 1 1
2 2 2 0 1 1 1 0 1 0
0 0 0 0 0 0 0 0 1 1
```

## Build the Boolean Gallery from the Two Templates (`hard_63_boolean_gallery_from_two_templates`)

**Difficulty:** hard

**Skills:** boolean shape operations, template comparison, gallery packing

**Scaffold notes:**
- Ignore the original template colors once you turn them into binary masks.
- Each code color names a different boolean operation.
- Every code cell produces one output panel in the gallery.

**Written solution:** Take the two framed binary templates and align them on a common canvas. Then read the code row: 4 = union, 5 = intersection, 6 = left-minus-right, 7 = xor. For each code, compute the corresponding boolean combination, color the kept cells with that code color, crop tightly, and place the result in a strip.

**Program solution (Python reference):**
```python
def solve_hard_63_boolean_gallery_from_two_templates(g:Grid)->Grid:
    h,w=dims(g)
    frames=find_frames(g,9)
    frames.sort(key=lambda fr: fr["bbox"][1])
    A=normalize_shape(crop_interior(g,frames[0]))
    B=normalize_shape(crop_interior(g,frames[1]))
    # make same dims
    hh=max(len(A),len(B)); ww=max(len(A[0]),len(B[0]))
    def pad(x):
        out=zeros(hh,ww)
        paste(out, x, (hh-len(x))//2, (ww-len(x[0]))//2)
        return out
    A=pad(A); B=pad(B)
    codes=[v for v in g[h-1] if v in (4,5,6,7)]
    parts=[]
    for code in codes:
        out=zeros(hh,ww)
        for r in range(hh):
            for c in range(ww):
                a=A[r][c]!=0; b=B[r][c]!=0
                keep=False
                if code==4: keep=a or b
                elif code==5: keep=a and b
                elif code==6: keep=a and not b
                elif code==7: keep=(a!=b)
                out[r][c]=code if keep else 0
        parts.append(crop_nonzero(out))
    return hstack(parts, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 2 0 2 0 9 0 9 3 3 0 0 9 0 0 0 0
0 9 2 2 2 0 9 0 9 0 3 3 0 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0
```

**Train 1 output**
```text
5 0 0 0 0 7 7 0 0 7 7
0 5 5 0 7 0 0 0 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 9 0 0 0 0 9 0 9 3 0 0 0 9 0 0 0 0
0 9 2 2 2 0 9 0 9 3 3 0 0 9 0 0 0 0
0 9 0 2 0 0 9 0 9 0 3 3 0 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 4 6 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 0 4 4 4 0 0 0
0 5 0 4 4 0 0 6 6
0 0 0 0 4 4 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 9 0 0 0 0 9 0 9 3 3 3 0 9 0 0 0 0
0 9 2 0 2 0 9 0 9 3 0 0 0 9 0 0 0 0
0 9 2 2 2 0 9 0 9 3 0 0 0 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 6 0 0 7 0 0 0 0 0 0 0 6 0 0 0 0
```

**Train 3 output**
```text
5 0 5 0 0 0 0 0 7 0 0 0 0
5 0 0 0 6 6 0 0 7 7 0 6 6
0 0 0 0 0 0 0 7 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 9 2 2 2 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 2 0 0 0 9 0 9 3 3 3 0 9 0 0 0 0
0 9 2 0 0 0 9 0 9 0 3 0 0 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0 0 4 0 0 0 0
```

**Train 4 output**
```text
6 0 6 0 4 4 4
6 0 6 0 4 4 0
0 0 0 0 4 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 9 2 0 0 0 9 0 9 0 3 3 0 9 0 0 0 0
0 9 2 2 0 0 9 0 9 0 3 3 0 9 0 0 0 0
0 9 0 2 2 0 9 0 9 0 3 0 0 9 0 0 0 0
0 9 0 0 0 0 9 0 9 0 0 0 0 9 0 0 0 0
0 9 9 9 9 9 9 0 9 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 7 0 0 0 0 0 0 0 6 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 7 0 0 0 0
6 6 0 6 6 0 0 0 0 0 6 6
0 0 0 0 0 0 7 7 7 0 0 0
```
