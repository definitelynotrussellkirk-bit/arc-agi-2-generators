# ARC Puzzle Bank — Seventeenth 21 Puzzles
This seventeenth bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`113`–`119`) so it follows directly after the sixteenth bundle.
This volume leans into a broader mix of mechanisms: mirror completion, sparse-corner rectangle recovery, diagonal segment filling, frame-local line logic, topology-aware recoloring, box-local gravity, rotation-matching, staircase paths, dihedral equivalence, priority-filled chambers, prototype mosaics, and overlay count maps.
It also introduces and reuses a few convenient primitives for solver work: `monotone_stair_path`, legend-priority chamber filling, prototype-mosaic decoding, and transformed-prototype overlay counting.
Every puzzle in this volume has **4 train pairs and 1 test pair**. Each entry includes scaffold notes, a written solution, and a verified Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_seventeenth_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_seventeenth_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_seventeenth_21.md` — this human-readable catalog.

## Summary
### Easy (7)
- `easy_113_complete_horizontal_mirror` — **Complete the Horizontal Mirror**
- `easy_114_draw_rectangle_borders_from_opposite_corners` — **Draw Rectangle Borders from Opposite Corners**
- `easy_115_top_pack_each_column` — **Top-Pack Each Column**
- `easy_116_fill_diagonal_segments` — **Fill the Diagonal Segments**
- `easy_117_crop_largest_object` — **Crop the Largest Object**
- `easy_118_turn_filled_rectangles_into_frames` — **Turn Filled Rectangles into Frames**
- `easy_119_keep_centers_of_odd_squares` — **Keep the Centers of Odd Squares**

### Medium (7)
- `medium_113_select_object_by_legend_and_transform` — **Select the Legend Object and Transform It**
- `medium_114_fill_matching_border_lines_inside_frame` — **Fill Matching Border Lines Inside the Frame**
- `medium_115_recolor_objects_by_hole_count` — **Recolor Objects by Hole Count**
- `medium_116_apply_gravity_inside_each_box` — **Apply Gravity Inside Each Box**
- `medium_117_select_rotation_match_and_recolor` — **Select the Rotation Match and Recolor It**
- `medium_118_connect_pairs_with_monotone_staircases` — **Connect Pairs with Monotone Staircases**
- `medium_119_scale_the_only_horizontally_symmetric_object` — **Scale the Only Horizontally Symmetric Object**

### Hard (7)
- `hard_113_build_dihedral_equivalence_matrix` — **Build the Dihedral Equivalence Matrix**
- `hard_114_decode_library_strip_with_transform_and_recolor` — **Decode the Library Strip with Transform and Recolor**
- `hard_115_overlay_monotone_staircases_into_count_map` — **Overlay the Staircases into a Count Map**
- `hard_116_fill_chambers_by_priority_seed` — **Fill Chambers by Priority Seed**
- `hard_117_decode_index_grid_into_prototype_mosaic` — **Decode the Index Grid into a Prototype Mosaic**
- `hard_118_overlay_transformed_prototype_stamps_into_count_map` — **Overlay Transformed Prototype Stamps into a Count Map**
- `hard_119_build_pairwise_union_gallery` — **Build the Pairwise Union Gallery**

## Complete the Horizontal Mirror (`easy_113_complete_horizontal_mirror`)

**Difficulty:** easy

**Skills:** horizontal symmetry completion, same-size transform, copying structure

**Scaffold notes:**
- Look at the grid as reflected across the horizontal midline.
- Every nonzero cell in the top half should also appear in the mirrored row below.
- Keep the original cells and add their reflected copies.

**Written solution:** Reflect every nonzero cell across the horizontal axis of the grid. Copy each colored cell to the row equally far from the bottom, preserving the column and color.

**Program solution (Python reference):**
```python
def solve_easy_113_complete_horizontal_mirror(g):
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
0 2 0 0 0 0 0 0 0
0 2 0 0 0 3 3 0 0
0 2 2 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0 0 0 0
0 2 0 0 0 3 3 0 0
0 2 2 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 8 0
0 2 0 0 0 3 3 0 0
0 2 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 7 0 0
0 4 4 4 0 0 0 0 0 0
0 0 4 0 0 6 6 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 7 0 0
0 4 4 4 0 0 0 0 0 0
0 0 4 0 0 6 6 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 4 0 0 6 6 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
```

**Train 3 input**
```text
2 0 0 0 0 0 0 0
2 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0
0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 0 0 0 0 0 0 0
2 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0
0 0 0 0 0 0 9 0
0 0 0 0 0 0 9 0
0 0 0 0 3 3 0 0
2 0 0 3 3 0 0 0
2 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 3 0
0 0 6 6 0 0 0 0 0 0 0
0 0 6 0 0 0 0 4 4 0 0
0 0 6 0 0 0 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0 3 0
0 0 6 6 0 0 0 0 0 0 0
0 0 6 0 0 0 0 4 4 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 4 4 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0
```

**Test 1 input**
```text
0 0 0 0 0 0 2 0 0
0 7 0 7 0 0 2 0 0
0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 2 0 0
0 7 0 7 0 0 2 0 0
0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4
0 7 7 7 0 0 0 0 0
0 7 0 7 0 0 2 0 0
0 0 0 0 0 0 2 0 0
```

## Draw Rectangle Borders from Opposite Corners (`easy_114_draw_rectangle_borders_from_opposite_corners`)

**Difficulty:** easy

**Skills:** color grouping, rectangle completion, same-size transform

**Scaffold notes:**
- Each color appears exactly twice.
- The two cells of one color are opposite corners of an axis-aligned rectangle.
- Draw the full rectangle border for each color.

**Written solution:** Treat each color pair as opposite corners of one rectangle. For each pair, compute the min and max row and column and draw the rectangle border connecting them in that same color.

**Program solution (Python reference):**
```python
def solve_easy_114_draw_rectangle_borders_from_opposite_corners(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=cells
        rlo,rhi=min(r0,r1),max(r0,r1)
        clo,chi=min(c0,c1),max(c0,c1)
        for c in range(clo,chi+1):
            out[rlo][c]=color
            out[rhi][c]=color
        for r in range(rlo,rhi+1):
            out[r][clo]=color
            out[r][chi]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 8 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 8 8 8 8 0
0 2 2 2 2 8 0 0 8 0
0 2 0 0 2 8 0 3 3 3
0 2 0 0 2 8 8 3 8 3
0 2 0 0 2 0 0 3 0 3
0 2 2 2 2 0 0 3 0 3
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 6 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6
9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 6 6 6
0 0 4 4 4 4 4 0 6 0 6
0 0 4 0 0 0 4 0 6 0 6
0 0 4 0 0 0 4 0 6 0 6
0 0 4 0 0 0 4 0 6 6 6
9 9 9 9 0 0 4 0 0 0 0
9 0 4 9 0 0 4 0 0 0 0
9 0 4 9 4 4 4 0 0 0 0
9 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 2 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 2 2 2 2 2 0
0 3 3 3 3 3 0 2 0
0 3 0 2 0 3 7 7 7
0 3 0 2 2 3 7 2 7
0 3 3 3 3 3 7 0 7
0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4
0 8 8 8 8 8 0 4 0 0 0 4
0 8 0 0 0 8 0 4 0 0 0 4
0 8 6 6 6 8 0 4 0 0 0 4
0 8 6 0 6 8 0 4 0 0 0 4
0 8 6 0 6 8 0 4 4 4 4 4
0 8 6 0 6 8 0 0 0 0 0 0
0 8 6 8 6 8 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 5 5 5
0 0 2 2 2 2 2 0 5 0 5
0 0 2 0 0 0 2 0 5 0 5
7 7 7 7 0 0 2 0 5 0 5
7 0 2 7 0 0 2 0 5 5 5
7 0 2 7 0 0 2 0 0 0 0
7 0 2 7 2 2 2 0 0 0 0
7 0 0 7 0 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0 0
```

## Top-Pack Each Column (`easy_115_top_pack_each_column`)

**Difficulty:** easy

**Skills:** column-wise packing, order preservation, same-size transform

**Scaffold notes:**
- Solve each column independently.
- Read the nonzero cells from top to bottom.
- Rewrite them starting at the top of the same column, leaving zeros underneath.

**Written solution:** For every column, collect its nonzero values in their original top-to-bottom order, then place them back from the top row downward. Everything below the packed values becomes background.

**Program solution (Python reference):**
```python
def solve_easy_115_top_pack_each_column(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for r,v in enumerate(vals):
            out[r][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 7
0 0 4 0 0 0 0
3 0 0 0 0 0 0
0 0 0 0 6 0 0
0 0 0 0 0 0 7
0 0 4 0 0 0 0
2 0 0 0 0 0 0
0 0 8 0 0 0 0
```

**Train 1 output**
```text
3 0 4 0 6 0 7
2 0 4 0 0 0 7
0 0 8 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0
0 0 0 8 0 0 0 0
0 0 0 0 0 9 0 0
0 0 0 3 0 0 0 0
0 2 0 0 0 0 0 4
```

**Train 2 output**
```text
0 5 0 3 0 9 0 4
0 2 0 8 0 0 0 4
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 5
0 0 2 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 5
0 0 0 0 3 0 0 0 0
6 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0
```

**Train 3 output**
```text
6 0 2 0 7 0 0 0 5
0 0 2 0 3 0 0 0 5
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 9
0 0 0 7 0 0
0 0 0 0 0 0
8 0 0 0 0 0
0 0 0 0 0 6
2 0 0 0 0 0
0 0 0 7 0 0
0 0 0 0 0 0
0 0 4 0 0 0
2 0 0 0 0 6
```

**Train 4 output**
```text
8 0 4 7 0 9
2 0 0 7 0 6
2 0 0 0 0 6
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 6 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 9 0
0 0 7 0 0 0 0 0
0 0 0 0 3 0 0 0
0 4 0 0 3 0 0 0
```

**Test 1 output**
```text
0 2 7 0 6 0 9 0
0 4 7 0 3 0 0 0
0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Fill the Diagonal Segments (`easy_116_fill_diagonal_segments`)

**Difficulty:** easy

**Skills:** diagonal reasoning, span filling, same-size transform

**Scaffold notes:**
- Each color has two endpoints on one diagonal.
- Find the step direction between the endpoints.
- Fill every cell on the inclusive diagonal segment.

**Written solution:** Each color marks the two ends of a diagonal segment. Determine whether the diagonal slopes down-right or down-left and fill all cells between the endpoints with that color.

**Program solution (Python reference):**
```python
def solve_easy_116_fill_diagonal_segments(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=cells
        dr = 1 if r1>r0 else -1
        dc = 1 if c1>c0 else -1
        if abs(r1-r0)==abs(c1-c0):
            steps=abs(r1-r0)
            for k in range(steps+1):
                out[r0+dr*k][c0+dc*k]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 4 0
0 0 2 0 0 0 4 0 0
0 0 0 2 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 6 0
0 0 0 3 0 0 0 6 0 0
0 0 0 0 3 0 6 0 0 0
0 0 0 0 0 6 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 2 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 5 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 2 0
0 0 5 0 0 0 0 0 2 0 0
0 0 0 5 0 0 0 2 0 0 0
0 0 0 0 5 0 2 0 0 0 0
0 0 0 0 0 5 0 0 9 0 0
0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 7 0 0
0 0 4 0 0 7 0 0 0
0 0 0 4 7 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 4 0 0 0
3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
```

**Test 1 input**
```text
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 2 0
0 0 0 6 0 0 0 2 0 0
0 0 0 0 6 0 2 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Crop the Largest Object (`easy_117_crop_largest_object`)

**Difficulty:** easy

**Skills:** connected components, area comparison, cropping

**Scaffold notes:**
- Separate the nonzero objects.
- Compare their areas.
- Keep only the bounding box of the largest one.

**Written solution:** Find all connected nonzero components, select the one with the largest number of cells, and return its bounding-box crop as the output.

**Program solution (Python reference):**
```python
def solve_easy_117_crop_largest_object(g):
    comps=connected_components(g)
    comp=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return object_crop_from_component(g, comp)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 6 6 6 0 0 0 0
0 2 0 0 0 6 0 6 0 0 0 0
0 2 2 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6
6 0 6
6 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 8
8 8 8
8 0 8
```

**Train 3 input**
```text
2 0 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 0 0 0
0 0 0 0 7 0 0 7 0 0 0
0 0 0 0 7 0 0 7 0 0 0
4 4 4 0 7 7 7 7 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 7 7
7 0 0 7
7 0 0 7
7 7 7 7
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0 0
0 3 0 3 0 3 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 9 9 9 0 0
0 0 0 0 0 9 0 0 0 9 0 0
4 0 0 0 0 9 9 9 9 9 0 0
4 0 0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 9 9 9
9 0 0 0 9
9 9 9 9 9
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 6 0 0 6 0 0
0 0 0 0 0 0 6 0 0 6 0 0
0 0 7 0 0 0 6 6 6 6 0 0
0 7 7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 6 6
6 0 0 6
6 0 0 6
6 6 6 6
```

## Turn Filled Rectangles into Frames (`easy_118_turn_filled_rectangles_into_frames`)

**Difficulty:** easy

**Skills:** shape abstraction, rectangle borders, same-size transform

**Scaffold notes:**
- Each component is a solid rectangle.
- Keep the outer border of each rectangle.
- Clear the interior cells.

**Written solution:** For every filled rectangular block, preserve only the cells on its outer border and set the interior to background. The output stays the same size as the input.

**Program solution (Python reference):**
```python
def solve_easy_118_turn_filled_rectangles_into_frames(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 7 7 7 0
0 2 2 2 2 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 7 7 7 0
0 2 2 2 2 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 8 8 8 0 0 0 0 2 2 2 0
0 8 8 8 0 0 0 0 2 2 2 0
0 8 8 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 4 4 4 4 0 0
0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 8 8 8 0 0 0 0 2 0 2 0
0 8 0 8 0 0 0 0 2 2 2 0
0 8 0 8 0 0 0 0 0 0 0 0
0 8 0 8 0 0 0 0 0 0 0 0
0 8 8 8 0 0 4 4 4 4 0 0
0 0 0 0 0 0 4 0 0 4 0 0
0 0 0 0 0 0 4 0 0 4 0 0
0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 5 0 0 0 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 9 0 9 0 0 0
0 0 0 0 9 0 9 0 0 0
0 0 0 0 9 0 9 0 0 0
0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7
0 0 2 2 2 2 0 0 7 7 7
0 0 2 2 2 2 0 0 7 7 7
0 0 2 2 2 2 0 0 7 7 7
0 0 2 2 2 2 0 0 7 7 7
4 4 4 4 4 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7
0 0 2 2 2 2 0 0 7 0 7
0 0 2 0 0 2 0 0 7 0 7
0 0 2 0 0 2 0 0 7 0 7
0 0 2 2 2 2 0 0 7 7 7
4 4 4 4 4 0 0 0 0 0 0
4 0 0 0 4 0 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Keep the Centers of Odd Squares (`easy_119_keep_centers_of_odd_squares`)

**Difficulty:** easy

**Skills:** geometry reduction, square detection, same-size transform

**Scaffold notes:**
- Each object is an odd-sized filled square.
- Odd squares have one unique center cell.
- Keep only that center cell in the same color.

**Written solution:** Find each filled odd-sized square, compute its center, and remove the rest of the square. The center cell keeps the square’s original color.

**Program solution (Python reference):**
```python
def solve_easy_119_keep_centers_of_odd_squares(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        hh=r1-r0+1
        ww=c1-c0+1
        if hh==ww and hh%2==1:
            out[r0+hh//2][c0+ww//2]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 5 5 5 5 5 0
8 8 8 0 0 0 5 5 5 5 5 0
8 8 8 0 0 0 5 5 5 5 5 0
8 8 8 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 7 7 7 0 0
0 4 4 4 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 6 6 6 0 0 0 2 2 2 2 2 0
0 6 6 6 0 0 0 2 2 2 2 2 0
0 6 6 6 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
4 4 4 4 4 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0
4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 2 2 2 0 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 8 8 8 8 0
6 6 6 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Select the Legend Object and Transform It (`medium_113_select_object_by_legend_and_transform`)

**Difficulty:** medium

**Skills:** control cells, object selection, geometric transforms

**Scaffold notes:**
- The top-left cell tells you which object color matters.
- The top-right cell is a transform code.
- Crop that object and apply the specified transform.

**Written solution:** Read the color key from the top-left corner to choose the target object. Read the transform code from the top-right corner, crop the selected object, and output its transformed version.

**Program solution (Python reference):**
```python
def solve_medium_113_select_object_by_legend_and_transform(g):
    h,w=dims(g)
    key=g[0][0]
    code=g[0][w-1]
    work=clone(g)
    work[0][0]=0
    work[0][w-1]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    obj=object_crop_from_component(work, comp)
    return apply_transform_code(obj, code)
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
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
7 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 4 0 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7
7 7
0 7
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 8 8 8 0
0 6 0 0 0 0 0 8 0 8 0
0 6 6 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 0
0 4 4
```

**Train 4 input**
```text
8 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8
8 0 0
8 8 8
```

**Test 1 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0
0 7 0 0 0 0 0 0 4 0 4 0 0
0 7 0 0 0 0 0 0 4 4 4 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 6
6 0 6
```

## Fill Matching Border Lines Inside the Frame (`medium_114_fill_matching_border_lines_inside_frame`)

**Difficulty:** medium

**Skills:** frame detection, pair matching, line filling

**Scaffold notes:**
- First locate the large frame.
- Markers of the same color on opposite borders define a line to fill.
- A color can define both a horizontal and a vertical line, producing a cross.

**Written solution:** Identify the main rectangular frame. For each marker color, if that color appears on opposite left and right border cells in the same row, fill the interior row segment; if it appears on opposite top and bottom border cells in the same column, fill that interior column segment.

**Program solution (Python reference):**
```python
def solve_medium_114_fill_matching_border_lines_inside_frame(g):
    h,w=dims(g)
    out=clone(g)
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==5]
    r0,c0,r1,c1=bbox(frame_cells)
    groups=collections.defaultdict(list)
    border_positions=set()
    for c in range(c0,c1+1):
        border_positions.add((r0,c)); border_positions.add((r1,c))
    for r in range(r0,r1+1):
        border_positions.add((r,c0)); border_positions.add((r,c1))
    for r,c in border_positions:
        v=g[r][c]
        if v not in (0,5):
            groups[v].append((r,c))
    for color,cells in groups.items():
        rows=collections.defaultdict(list)
        cols=collections.defaultdict(list)
        for r,c in cells:
            rows[r].append(c)
            cols[c].append(r)
        for r,cs in rows.items():
            if len(cs)>=2:
                lo,hi=min(cs),max(cs)
                if lo==c0 and hi==c1:
                    for c in range(c0+1,c1):
                        out[r][c]=color
        for c,rs in cols.items():
            if len(rs)>=2:
                lo,hi=min(rs),max(rs)
                if lo==r0 and hi==r1:
                    for r in range(r0+1,r1):
                        out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 2 5 7 5 5 0 0
0 5 0 0 0 0 0 0 0 0 5 0 0
0 2 0 0 0 0 0 0 0 0 2 0 0
0 5 0 0 0 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 0 5 0 0
0 4 0 0 0 0 0 0 0 0 4 0 0
0 5 0 0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 5 2 5 7 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 2 5 7 5 5 0 0
0 5 0 0 0 0 2 0 7 0 5 0 0
0 2 2 2 2 2 2 2 7 2 2 0 0
0 5 0 0 0 0 2 0 7 0 5 0 0
0 5 0 0 0 0 2 0 7 0 5 0 0
0 4 4 4 4 4 4 4 4 4 4 0 0
0 5 0 0 0 0 2 0 7 0 5 0 0
0 5 5 5 5 5 2 5 7 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 8 5 6 5 5 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 3 0 0 0 0 0 0 3 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 6 0 0 0 0 0 0 6 0 0
0 0 5 0 0 0 0 0 0 5 0 0
0 0 5 5 8 5 6 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 8 5 6 5 5 5 0 0
0 0 5 0 8 0 6 0 0 5 0 0
0 0 3 3 8 3 6 3 3 3 0 0
0 0 5 0 8 0 6 0 0 5 0 0
0 0 5 0 8 0 6 0 0 5 0 0
0 0 6 6 6 6 6 6 6 6 0 0
0 0 5 0 8 0 6 0 0 5 0 0
0 0 5 5 8 5 6 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 2 5 8 5 5 0 0
0 0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 0 7 0 0 0 0 0 0 0 7 0 0
0 0 0 8 0 0 0 0 0 0 0 8 0 0
0 0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 0 5 5 5 5 2 5 8 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 2 5 8 5 5 0 0
0 0 0 5 0 0 0 2 0 8 0 5 0 0
0 0 0 5 0 0 0 2 0 8 0 5 0 0
0 0 0 5 0 0 0 2 0 8 0 5 0 0
0 0 0 7 7 7 7 2 7 7 7 7 0 0
0 0 0 8 8 8 8 2 8 8 8 8 0 0
0 0 0 5 0 0 0 2 0 8 0 5 0 0
0 0 0 5 0 0 0 2 0 8 0 5 0 0
0 0 0 5 5 5 5 2 5 8 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 3 5 9 5 5 0 0
0 5 0 0 0 0 0 0 0 5 0 0
0 4 0 0 0 0 0 0 0 4 0 0
0 5 0 0 0 0 0 0 0 5 0 0
0 9 0 0 0 0 0 0 0 9 0 0
0 5 0 0 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 3 5 9 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 3 5 9 5 5 0 0
0 5 0 0 0 3 0 9 0 5 0 0
0 4 4 4 4 3 4 9 4 4 0 0
0 5 0 0 0 3 0 9 0 5 0 0
0 9 9 9 9 9 9 9 9 9 0 0
0 5 0 0 0 3 0 9 0 5 0 0
0 5 0 0 0 3 0 9 0 5 0 0
0 5 0 0 0 3 0 9 0 5 0 0
0 5 5 5 5 3 5 9 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 2 5 7 5 5 0 0
0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 6 0 0 0 0 0 0 0 6 0 0
0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 2 5 7 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 2 5 7 5 5 0 0
0 0 5 0 0 0 2 0 7 0 5 0 0
0 0 2 2 2 2 2 2 7 2 2 0 0
0 0 5 0 0 0 2 0 7 0 5 0 0
0 0 6 6 6 6 6 6 7 6 6 0 0
0 0 5 0 0 0 2 0 7 0 5 0 0
0 0 5 0 0 0 2 0 7 0 5 0 0
0 0 5 0 0 0 2 0 7 0 5 0 0
0 0 5 5 5 5 2 5 7 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Recolor Objects by Hole Count (`medium_115_recolor_objects_by_hole_count`)

**Difficulty:** medium

**Skills:** topology, connected components, recoloring

**Scaffold notes:**
- Separate the objects first.
- Ask whether each object encloses a hole.
- Objects with no holes become one color; objects with a hole become another.

**Written solution:** Split the grid into connected components, count whether each component contains an enclosed hole, and recolor the whole component accordingly: one color for hole-free objects and another for holed objects.

**Program solution (Python reference):**
```python
def solve_medium_115_recolor_objects_by_hole_count(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        obj=object_crop_from_component(g, comp)
        new_color=8 if hole_count(obj)>=1 else 2
        for r,c in comp["cells"]:
            out[r][c]=new_color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 6 6 6 0 0 0 0
0 6 0 0 0 0 6 0 6 0 0 0 0
0 6 6 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 0
0 0 0 6 6 6 0 0 6 0 0 6 0
0 0 0 0 6 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 8 8 8 0 0 0 0
0 2 0 0 0 0 8 0 8 0 0 0 0
0 2 2 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 2 2 2 0 0 8 0 0 8 0
0 0 0 0 2 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0
0 6 6 6 0 0 6 6 6 6 6 0
0 0 0 0 0 0 6 0 0 0 6 0
0 0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 6 6 6 0 0
0 0 6 6 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 8 8 8 8 8 0
0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 8 8 8 0 0
0 0 2 2 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 6 6 6 6 0 0 0
0 6 6 6 0 0 0 6 0 0 6 0 0 0
0 6 0 6 0 0 0 6 0 0 6 0 0 0
0 0 0 0 0 0 0 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 6 6 6 0 0
0 0 6 6 0 0 0 0 0 6 0 6 0 0
0 0 6 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 8 8 8 8 0 0 0
0 2 2 2 0 0 0 8 0 0 8 0 0 0
0 2 0 2 0 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 8 8 8 0 0
0 0 2 2 0 0 0 0 0 8 0 8 0 0
0 0 2 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 6 6 6 0 0 0
0 6 0 0 0 0 0 6 0 6 0 0 0
0 6 6 6 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 6 6 6 6 6 0
0 0 0 6 0 0 0 6 0 0 0 6 0
0 0 0 6 6 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 8 8 8 0 0 0
0 2 0 0 0 0 0 8 0 8 0 0 0
0 2 2 2 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 8 8 8 8 8 0
0 0 0 2 0 0 0 8 0 0 0 8 0
0 0 0 2 2 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 6 6 6 6 0 0 0
0 6 6 0 0 0 6 0 0 6 0 0 0
0 6 0 0 0 0 6 0 0 6 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 6 6 6 0
0 0 6 6 6 0 0 0 0 6 0 6 0
0 0 6 0 6 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 8 8 8 8 0 0 0
0 2 2 0 0 0 8 0 0 8 0 0 0
0 2 0 0 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 8 8 8 0
0 0 2 2 2 0 0 0 0 8 0 8 0
0 0 2 0 2 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Apply Gravity Inside Each Box (`medium_116_apply_gravity_inside_each_box`)

**Difficulty:** medium

**Skills:** frame-local reasoning, column gravity, multi-object decomposition

**Scaffold notes:**
- Each hollow rectangle is an independent box.
- Only the cells inside a box move.
- Within each box, pack each interior column downward while keeping the wall fixed.

**Written solution:** For every hollow box, treat its interior separately. In each interior column, collect the nonzero cells and drop them to the bottom of that column inside the box, leaving the box border unchanged.

**Program solution (Python reference):**
```python
def solve_medium_116_apply_gravity_inside_each_box(g):
    h,w=dims(g)
    out=zeros(h,w)
    boxes=[comp for comp in connected_components(g, colors={5})]
    for box in boxes:
        r0,c0,r1,c1=box["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=5
            out[r1][c]=5
        for r in range(r0,r1+1):
            out[r][c0]=5
            out[r][c1]=5
        ih=r1-r0-1
        iw=c1-c0-1
        for ic in range(iw):
            vals=[]
            for ir in range(ih):
                v=g[r0+1+ir][c0+1+ic]
                if v!=0:
                    vals.append(v)
            for i,v in enumerate(reversed(vals)):
                out[r1-1-i][c0+1+ic]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 2 0 0 4 0 0 0 0 0 0 0 0
0 5 0 0 3 5 0 0 0 0 0 0 0 0
0 5 0 0 2 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 7 0 0 9 0
0 0 0 0 0 0 0 5 0 0 0 8 5 0
0 0 0 0 0 0 0 5 7 0 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0 0 0
0 5 0 0 3 5 0 0 0 0 0 0 0 0
0 5 2 0 2 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 5 7 7 0 8 5 0
0 0 0 0 0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 5 4 2 0 5 0 5 5 5 5 0
0 0 5 0 0 3 5 0 5 6 0 5 0
0 0 5 0 2 0 5 0 5 0 8 5 0
0 0 5 0 0 0 5 0 5 7 0 5 0
0 0 5 5 5 5 5 0 5 0 0 5 0
0 0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0 0
0 0 5 0 0 0 5 0 5 5 5 5 0
0 0 5 0 0 0 5 0 5 0 0 5 0
0 0 5 0 2 0 5 0 5 0 0 5 0
0 0 5 4 2 3 5 0 5 0 0 5 0
0 0 5 5 5 5 5 0 5 6 0 5 0
0 0 0 0 0 0 0 0 5 7 8 5 0
0 0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 2 0 0 0 5 0 0 0 0 0 0 0 0
0 5 0 0 4 0 5 0 0 0 5 5 5 5 0
0 5 0 0 0 0 3 0 0 0 5 2 0 5 0
0 5 5 5 5 5 5 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 3 5 0
0 0 0 5 5 5 5 5 0 0 5 0 0 5 0
0 0 0 5 8 6 0 5 0 0 5 4 0 5 0
0 0 0 5 0 0 0 7 0 0 5 5 5 5 0
0 0 0 5 0 0 9 5 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0 0 0 0 0 0
0 5 0 0 0 0 5 0 0 0 5 5 5 5 0
0 5 2 0 4 0 5 0 0 0 5 0 0 5 0
0 5 5 5 5 5 5 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 5 5 5 5 5 0 0 5 2 0 5 0
0 0 0 5 0 0 0 5 0 0 5 4 3 5 0
0 0 0 5 0 0 0 5 0 0 5 5 5 5 0
0 0 0 5 8 6 9 5 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 2 0 0 4 0 0 0 0 0 0
0 5 0 0 3 5 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 5 0 7 0 5 0
0 0 0 0 0 0 5 9 0 0 5 0
0 0 0 0 0 0 5 0 0 8 5 0
0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 2 0 3 5 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 5 9 7 8 5 0
0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0
0 0 5 0 2 0 0 3 0 0 0 0 0 0
0 0 5 4 0 0 0 5 0 0 0 0 0 0
0 0 5 0 0 0 2 5 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 5 7 0 0 5 0
0 0 0 0 0 0 0 0 5 0 0 6 5 0
0 0 0 0 0 0 0 0 5 0 8 0 5 0
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0 0 0
0 0 5 4 2 0 2 5 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 0 0 0 5 7 8 6 5 0
0 0 0 0 0 0 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Select the Rotation Match and Recolor It (`medium_117_select_rotation_match_and_recolor`)

**Difficulty:** medium

**Skills:** reference matching, rotation invariance, recoloring

**Scaffold notes:**
- The small object near the top-left is the reference.
- One larger object elsewhere matches it under rotation.
- The top-right cell gives the output color.

**Written solution:** Use the top-left reference object as a shape template. Find the object elsewhere in the grid whose binary shape matches the reference under rotation, crop it, and recolor all its nonzero cells to the target color from the top-right corner.

**Program solution (Python reference):**
```python
def solve_medium_117_select_rotation_match_and_recolor(g):
    h,w=dims(g)
    target=g[0][w-1]
    work=clone(g)
    work[0][w-1]=0
    ref_comp=max([comp for comp in connected_components(work, colors={1})], key=lambda comp: comp["area"])
    ref_obj=object_crop_from_component(work, ref_comp)
    for r,c in ref_comp["cells"]:
        work[r][c]=0
    candidates=connected_components(work)
    for comp in sorted(candidates, key=lambda comp: (comp["bbox"][0], comp["bbox"][1])):
        obj=object_crop_from_component(work, comp)
        if same_under_rotation(ref_obj, obj):
            return recolor_object(obj, target)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 8
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 3 3 3 0 0 0
0 1 1 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8
8 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 7
0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 7
7 7
7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 2
0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 7 7 7 0 0
0 0 5 5 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 2
2 2
2 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 9
0 1 1 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 2 0 2 0 0 0
0 0 6 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 9 9
0 0 9
9 9 9
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 6
0 1 1 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 2 0 2 0 0
0 0 0 7 7 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 6
0 6 6
```

## Connect Pairs with Monotone Staircases (`medium_118_connect_pairs_with_monotone_staircases`)

**Difficulty:** medium

**Skills:** path construction, pair grouping, same-size transform

**Scaffold notes:**
- Each color appears exactly twice.
- Move from one endpoint toward the other by alternating row progress and column progress.
- Draw the whole staircase path in that color.

**Written solution:** For each same-colored pair, connect the endpoints with a deterministic monotone staircase path that steadily approaches the target by stepping in row and column directions until it arrives.

**Program solution (Python reference):**
```python
def solve_medium_118_connect_pairs_with_monotone_staircases(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        for r,c in monotone_stair_path(cells[0], cells[1]):
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 7 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 4 0 0
0 0 2 2 7 0 0 0 4 4 0 0
0 0 0 7 7 0 0 4 4 0 0 0
0 0 7 7 2 2 4 4 0 0 0 0
0 7 7 0 0 2 4 0 0 0 0 0
0 7 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 6 0 0 0 0 0 3 3 0 0
0 6 6 0 0 0 3 3 0 0 0
0 0 6 6 0 3 3 0 0 0 0
0 0 0 6 6 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 6 6 0 0 0 0
0 0 8 8 0 0 6 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 7 0
0 0 0 0 4 4 0 0 0 0 7 7 0
0 0 0 0 0 4 2 0 0 7 7 0 0
0 0 0 0 0 2 2 4 7 7 0 0 0
0 0 0 0 2 2 0 7 7 0 0 0 0
0 0 0 2 2 0 7 7 4 0 0 0 0
0 0 2 2 0 7 7 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
9 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 5 0
0 9 9 0 0 0 0 5 5 0
0 0 9 9 0 0 5 3 0 0
0 0 0 9 9 5 3 3 0 0
0 0 0 0 5 3 3 0 0 0
0 0 0 5 3 3 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 6 0 0 0 0 0 0 0 2 2 0
0 6 6 0 0 0 0 0 2 2 0 0
0 0 6 6 0 0 0 2 8 0 0 0
0 0 0 6 6 0 2 8 8 0 0 0
0 0 0 0 6 6 8 8 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 8 8 6 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Scale the Only Horizontally Symmetric Object (`medium_119_scale_the_only_horizontally_symmetric_object`)

**Difficulty:** medium

**Skills:** symmetry detection, object selection, scaling

**Scaffold notes:**
- Among the objects, exactly one is horizontally symmetric.
- Crop that symmetric object.
- Expand it by a factor of 2 in both directions.

**Written solution:** Find the single object whose cropped shape is invariant under horizontal reflection, crop it, and scale it up by duplicating every row and every column.

**Program solution (Python reference):**
```python
def solve_medium_119_scale_the_only_horizontally_symmetric_object(g):
    comps=connected_components(g)
    for comp in sorted(comps, key=lambda comp: (comp["bbox"][0], comp["bbox"][1])):
        obj=object_crop_from_component(g, comp)
        if is_horiz_symmetric(obj):
            return scale2(obj)
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 4 0 0 0 0 0
0 2 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 2 2
2 2 0 0 2 2
2 2 2 2 2 2
2 2 2 2 2 2
2 2 0 0 2 2
2 2 0 0 2 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 0 0 3 3
3 3 0 0 3 3
3 3 3 3 3 3
3 3 3 3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0 0 0 0 0
0 7 0 7 0 7 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 6 0 0 0 3 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 4 4 0 0 0 3 3 0 0 0 0
0 0 0 4 4 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 0 0 6 6
6 6 0 0 6 6
6 6 6 6 6 6
6 6 6 6 6 6
```

## Build the Dihedral Equivalence Matrix (`hard_113_build_dihedral_equivalence_matrix`)

**Difficulty:** hard

**Skills:** shape normalization, pairwise relations, matrix abstraction

**Scaffold notes:**
- Order the objects from left to right.
- Compare every pair up to rotation and reflection.
- Write a relation matrix showing which pairs are equivalent.

**Written solution:** Crop the objects in left-to-right order. For every ordered pair, check whether the two shapes are equivalent under any rotation or reflection, and write a positive marker in the corresponding matrix cell when they are.

**Program solution (Python reference):**
```python
def solve_hard_113_build_dihedral_equivalence_matrix(g):
    comps=sorted(connected_components(g), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    n=len(comps)
    out=zeros(n,n)
    objs=[object_crop_from_component(g, comp) for comp in comps]
    for i in range(n):
        for j in range(n):
            if same_under_dihedral(objs[i], objs[j]):
                out[i][j]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 4 4 0 0 0 6 6 0 0
0 2 0 0 0 3 3 3 0 0 4 4 0 6 6 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 0 0
8 8 0 0
0 0 8 8
0 0 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 0 0 0 4 4 4 0 6 0 6
0 2 2 0 0 3 3 0 0 0 0 4 0 0 6 6 6
0 2 0 0 0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 3 3 3 0 0 4 0 0 0 0 7 0 0 0
0 2 0 0 0 0 0 0 3 0 0 4 0 0 0 0 7 0 0 0
0 2 2 2 0 0 3 3 3 0 0 4 4 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0 0
8 8 0 0
0 0 8 8
0 0 8 8
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 3 0 0 4 0 4 0 6 6 6
0 2 2 0 0 3 3 0 0 4 4 4 0 0 6 0
0 2 0 0 0 3 0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 3 3 3 0 0 4 4 0 0 6 6 6 0
0 2 0 0 0 0 0 3 0 0 4 4 0 0 0 6 0 0
0 2 2 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 0 0
8 8 0 0
0 0 8 0
0 0 0 8
```

## Decode the Library Strip with Transform and Recolor (`hard_114_decode_library_strip_with_transform_and_recolor`)

**Difficulty:** hard

**Skills:** library lookup, sequence decoding, transform composition

**Scaffold notes:**
- The top region is a shape library keyed by object color.
- The bottom row is a sequence of selector/transform/recolor tokens.
- Decode each token into one transformed recolored object and concatenate the results.

**Written solution:** Build a library from the top objects, using each object’s color as its selector code. Then read the bottom row in triples: choose the library object, apply the transform code, recolor the result, and place the decoded objects left to right in one strip.

**Program solution (Python reference):**
```python
def solve_hard_114_decode_library_strip_with_transform_and_recolor(g):
    h,w=dims(g)
    lib_area=[row[:] for row in g[:-1]]
    seq=g[-1]
    lib={}
    for comp in sorted(connected_components(lib_area), key=lambda comp: (comp["bbox"][1], comp["bbox"][0])):
        lib[comp["color"]]=object_crop_from_component(lib_area, comp)
    tokens=[]
    i=0
    while i < w:
        if seq[i]==0:
            i+=1
            continue
        if i+2 >= w:
            break
        tokens.append((seq[i], seq[i+1], seq[i+2]))
        i += 4
    objs=[]
    for selector,code,recolor in tokens:
        obj=apply_transform_code(lib[selector], code)
        objs.append(recolor_object(obj, recolor))
    return gallery_row(objs, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 3 3 0 0 0 4 4 0 0 0 0 0
0 2 0 0 0 0 0 0 3 0 0 0 0 0 4 4 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 8 0 4 1 6 0 3 4 7 0 2 3 9 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 0 6 6 0 0 7 0 0 9 9
8 0 0 0 0 6 6 0 7 7 0 0 9
0 0 0 0 0 0 0 0 7 0 0 0 9
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 0 3 0 0 0 0 4 4 4 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 3 3 0 0 0 0 4 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 5 8 0 2 3 6 0 4 2 7 0 3 1 9 0 2 4 5 0 0 0 0 0
```

**Train 2 output**
```text
8 0 8 0 0 6 0 7 7 7 0 9 0 9 0 5 5 0
8 8 8 0 6 6 0 7 0 7 0 9 9 9 0 5 5 5
0 0 0 0 6 6 0 7 0 7 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 3 0 3 0 0 0 4 0 0 0 0 0 0
0 2 2 0 0 0 0 3 3 3 0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 3 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 2 6 0 2 4 8 0 3 6 7 0 4 1 9 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6 0 8 8 0 0 7 0 7 0 9 0
6 0 0 0 0 8 8 0 7 7 7 0 9 0
0 0 0 0 0 0 0 0 7 0 7 0 9 9
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 3 3 0 0 0 0 0 0 4 4 4 0 0 0 0
0 2 0 0 0 0 0 0 0 3 3 0 0 0 0 0 0 0 4 0 0 0 0 0
0 2 2 2 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 4 7 0 3 2 8 0 4 3 6 0 2 1 9 0 3 5 5 0 0 0 0 0
```

**Train 4 output**
```text
7 0 7 0 8 8 8 0 0 6 0 0 9 9 9 0 5 5
7 0 7 0 0 8 8 0 6 6 6 0 9 0 0 0 5 5
7 7 7 0 0 0 0 0 0 0 0 0 9 9 9 0 0 5
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 3 0 0 0 4 4 0 0 0 0 0
0 2 0 0 0 0 0 3 3 3 0 0 0 0 4 4 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 4 8 0 2 2 6 0 4 3 7 0 3 1 9 0 0 0 0 0
```

**Test 1 output**
```text
8 8 0 6 6 6 0 7 7 0 0 9 0 9
0 8 0 6 0 0 0 0 7 7 0 9 9 9
8 8 0 0 0 0 0 0 0 0 0 0 0 0
```

## Overlay the Staircases into a Count Map (`hard_115_overlay_monotone_staircases_into_count_map`)

**Difficulty:** hard

**Skills:** path overlays, count aggregation, abstract output

**Scaffold notes:**
- Construct the staircase path for every same-color pair.
- Count how many paths pass through each cell.
- Encode that count as the output color.

**Written solution:** Draw every monotone staircase path implied by the endpoint pairs, accumulate how many paths cover each cell, and convert the coverage counts into an output count map.

**Program solution (Python reference):**
```python
def solve_hard_115_overlay_monotone_staircases_into_count_map(g):
    h,w=dims(g)
    counts=zeros(h,w)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        for r,c in monotone_stair_path(cells[0], cells[1]):
            counts[r][c]+=1
    return encode_count_map(counts)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 2 0 0 0
0 2 2 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 0 0 0 0 3 2 0 0 0 0
0 0 0 2 2 2 0 3 3 0 0 0 0 0
0 0 0 0 2 3 4 3 0 0 0 0 0 0
0 0 0 0 0 4 5 2 0 0 0 0 0 0
0 0 0 0 3 3 2 2 2 0 0 0 0 0
0 0 0 2 3 0 2 0 2 2 0 0 0 0
0 0 2 2 0 0 0 0 0 2 2 0 0 0
0 2 2 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 2 0
0 2 2 0 0 0 0 0 0 0 2 2 0
0 0 2 2 2 0 0 0 0 2 2 0 0
0 0 0 2 3 2 2 0 2 2 0 0 0
0 0 0 0 2 4 3 2 2 0 0 0 0
0 0 0 0 2 3 4 3 0 0 0 0 0
0 0 0 2 2 2 3 3 2 0 0 0 0
0 0 2 2 0 0 0 0 2 2 0 0 0
2 2 2 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 7
```

**Train 3 output**
```text
2 0 0 0 0 0 0 0 0 0 0 2
2 2 0 0 0 0 0 0 0 0 2 2
0 2 2 0 0 0 0 0 0 2 2 0
0 0 2 2 0 2 0 0 2 2 0 0
0 0 0 2 2 2 2 3 2 0 0 0
0 0 0 0 2 2 4 4 0 0 0 0
0 0 0 0 0 4 4 2 2 0 0 0
0 0 0 0 3 3 2 2 2 2 0 0
0 0 0 3 3 0 0 2 2 2 2 0
0 0 2 2 0 0 0 0 0 0 2 2
0 2 2 0 0 0 0 0 0 0 0 2
2 2 0 0 0 0 0 0 0 0 0 2
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 7 0 0 0 5 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 2 0 0
0 0 2 2 0 0 2 0 0 0 0 2 2 0 0
0 0 0 2 2 0 2 2 2 0 2 2 0 0 0
0 0 0 0 2 2 0 3 3 2 2 0 0 0 0
0 0 0 0 0 2 3 2 3 3 0 0 0 0 0
0 0 0 0 0 2 3 3 2 2 2 0 0 0 0
0 0 0 0 2 2 2 3 2 2 2 2 0 0 0
0 2 2 2 2 2 2 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 2 0
0 2 2 0 0 0 0 0 0 0 0 2 2 0
0 0 2 2 0 0 2 0 0 0 2 2 0 0
0 0 0 2 2 0 2 2 2 2 2 0 0 0
0 0 0 0 2 2 0 3 4 2 0 0 0 0
0 0 0 0 0 2 3 3 3 2 0 0 0 0
0 0 0 0 0 2 4 3 0 2 2 0 0 0
0 0 0 0 2 3 2 2 0 0 2 2 0 0
0 0 0 2 2 0 0 2 0 0 0 2 2 0
0 2 2 2 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Fill Chambers by Priority Seed (`hard_116_fill_chambers_by_priority_seed`)

**Difficulty:** hard

**Skills:** chamber decomposition, legend priority, region filling

**Scaffold notes:**
- The top row lists colors in priority order.
- Walls split the lower area into separate chambers.
- Each chamber takes the highest-priority seed color present inside it.

**Written solution:** Use the top legend row to define a priority ordering over colors. Partition the walled region below into chambers, inspect which seed colors appear inside each chamber, and fill the chamber with the highest-priority color found there while preserving the walls.

**Program solution (Python reference):**
```python
def solve_hard_116_fill_chambers_by_priority_seed(g):
    h,w=dims(g)
    legend=[v for v in g[0] if v not in (0,5)]
    priority={color:i for i,color in enumerate(legend)}
    out=clone(g)
    visited=set()
    for r in range(1,h):
        for c in range(w):
            if g[r][c] in (0,*legend) and (r,c) not in visited:
                region=flood_region_within(g,(r,c),wall_color=5, row_min=1)
                visited |= region
                seeds=sorted({g[rr][cc] for rr,cc in region if g[rr][cc] in priority}, key=lambda color: priority[color])
                if not seeds:
                    fill=0
                else:
                    fill=seeds[0]
                for rr,cc in region:
                    out[rr][cc]=fill
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    return out
```

**Train 1 input**
```text
2 3 6 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 0 3 0 5 0 6 0 5 0 0 5
5 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 5 5 5 5 5 5 5 5
5 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 5 0 2 0 5 0 0 5
5 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 5 0 0 0 0 0 6 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
2 3 6 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
5 3 3 3 5 6 6 6 5 0 0 5
5 3 3 3 5 6 6 6 5 0 0 5
5 3 3 3 5 5 5 5 5 5 5 5
5 3 3 3 5 2 2 2 5 2 2 5
5 3 3 3 5 2 2 2 5 2 2 5
5 3 3 3 5 2 2 2 5 2 2 5
5 3 3 3 5 2 2 2 2 2 2 5
5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
6 2 8 3 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 8 0 0 5 0 0 0 5 0 0 5
5 0 0 0 0 5 0 2 0 5 0 0 5
5 0 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 0 5 5 5 5 5 5 5 5
5 0 0 0 0 5 0 0 0 5 0 0 5
5 0 0 0 0 5 0 6 0 5 0 0 5
5 0 0 0 0 5 0 0 0 5 5 5 5
5 0 0 0 0 5 0 0 0 0 2 3 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
6 2 8 3 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 5 2 2 2 5 0 0 5
5 8 8 8 8 5 2 2 2 5 0 0 5
5 8 8 8 8 5 2 2 2 5 0 0 5
5 8 8 8 8 5 5 5 5 5 5 5 5
5 8 8 8 8 5 6 6 6 5 0 0 5
5 8 8 8 8 5 6 6 6 5 0 0 5
5 8 8 8 8 5 6 6 6 5 5 5 5
5 8 8 8 8 5 6 6 6 6 6 6 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
3 8 2 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 8 0 5 0 2 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 0 5 0 3 0 5
5 0 0 0 5 0 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 0 5 0 0 0 5
5 0 0 0 5 5 5 5 5 5 0 0 0 5
5 0 0 0 5 0 0 0 0 5 0 0 0 5
5 0 3 0 5 0 8 0 0 5 0 2 0 5
5 0 0 0 5 0 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
3 8 2 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 3 3 3 5 2 2 2 2 5 3 3 3 5
5 3 3 3 5 2 2 2 2 5 3 3 3 5
5 3 3 3 5 2 2 2 2 5 3 3 3 5
5 3 3 3 5 2 2 2 2 5 3 3 3 5
5 3 3 3 5 5 5 5 5 5 3 3 3 5
5 3 3 3 5 8 8 8 8 5 3 3 3 5
5 3 3 3 5 8 8 8 8 5 3 3 3 5
5 3 3 3 5 8 8 8 8 5 3 3 3 5
5 3 3 3 5 8 8 8 8 5 3 3 3 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 input**
```text
8 2 6 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 2 0 5 0 8 0 5 0 2 5
5 0 0 5 0 0 0 5 0 0 5
5 0 0 5 0 0 0 5 0 0 5
5 0 0 5 5 5 5 5 0 0 5
5 0 0 5 0 0 0 5 0 0 5
5 0 0 5 0 6 0 5 0 0 5
5 0 0 5 0 0 0 5 0 0 5
5 5 5 5 5 5 5 5 5 5 5
```

**Train 4 output**
```text
8 2 6 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5
5 2 2 5 8 8 8 5 2 2 5
5 2 2 5 8 8 8 5 2 2 5
5 2 2 5 8 8 8 5 2 2 5
5 2 2 5 5 5 5 5 2 2 5
5 2 2 5 6 6 6 5 2 2 5
5 2 2 5 6 6 6 5 2 2 5
5 2 2 5 6 6 6 5 2 2 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
2 6 8 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
5 0 6 0 5 0 8 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 0 0 5 0 0 0 5
5 0 0 0 5 5 5 5 5 0 0 0 5
5 0 0 0 5 0 0 0 5 0 0 0 5
5 0 0 0 5 0 2 0 5 0 6 0 5
5 0 0 0 5 0 0 0 5 0 0 0 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
2 6 8 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
5 6 6 6 5 8 8 8 5 6 6 6 5
5 6 6 6 5 8 8 8 5 6 6 6 5
5 6 6 6 5 8 8 8 5 6 6 6 5
5 6 6 6 5 8 8 8 5 6 6 6 5
5 6 6 6 5 5 5 5 5 6 6 6 5
5 6 6 6 5 2 2 2 5 6 6 6 5
5 6 6 6 5 2 2 2 5 6 6 6 5
5 6 6 6 5 2 2 2 5 6 6 6 5
5 5 5 5 5 5 5 5 5 5 5 5 5
```

## Decode the Index Grid into a Prototype Mosaic (`hard_117_decode_index_grid_into_prototype_mosaic`)

**Difficulty:** hard

**Skills:** prototype library, symbolic replacement, mosaic construction

**Scaffold notes:**
- The top objects form a library keyed by color.
- A blank separator row splits the library from the index grid.
- Replace each index cell with the corresponding prototype panel.

**Written solution:** Treat the objects above the blank row as prototype panels keyed by their colors. Then read the lower color grid and replace each color cell with its matching prototype, assembling a full mosaic.

**Program solution (Python reference):**
```python
def solve_hard_117_decode_index_grid_into_prototype_mosaic(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==0 for v in g[r]):
            sep=r
            break
    lib_area=[row[:] for row in g[:sep]]
    raw_index=[row[:] for row in g[sep+1:]]
    # crop index grid to its nonzero extent so right-side padding does not matter
    index_area=crop_nonzero(raw_index)
    lib={}
    comps=sorted(connected_components(lib_area), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    ph=max(comp["bbox"][2]-comp["bbox"][0]+1 for comp in comps)
    pw=max(comp["bbox"][3]-comp["bbox"][1]+1 for comp in comps)
    for comp in comps:
        obj=object_crop_from_component(lib_area, comp)
        padded=zeros(ph,pw)
        stamp(padded,obj,0,0)
        lib[comp["color"]]=padded
    rows=len(index_area)
    cols=len(index_area[0])
    panels=[]
    for r in range(rows):
        prow=[]
        for c in range(cols):
            prow.append(lib[index_area[r][c]])
        panels.append(prow)
    return gallery_grid(panels, gap=0)
```

**Train 1 input**
```text
2 0 0 0 3 3 3 0 4 4 0
2 0 0 0 0 3 0 0 0 4 4
2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 3 4 0 0 0 0 0 0 0 0
4 2 3 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 3 3 3 4 4 0
2 0 0 0 3 0 0 4 4
2 2 0 0 0 0 0 0 0
4 4 0 2 0 0 3 3 3
0 4 4 2 0 0 0 3 0
0 0 0 2 2 0 0 0 0
```

**Train 2 input**
```text
2 2 0 0 6 0 6 0 8 8 8
2 2 0 0 6 6 6 0 8 0 0
2 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
8 2 0 0 0 0 0 0 0 0 0
6 8 0 0 0 0 0 0 0 0 0
2 6 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 2 2 0
8 0 0 2 2 0
8 8 8 2 0 0
6 0 6 8 8 8
6 6 6 8 0 0
0 0 0 8 8 8
2 2 0 6 0 6
2 2 0 6 6 6
2 0 0 0 0 0
```

**Train 3 input**
```text
3 0 3 0 0 4 0 0 7 0 0
3 3 3 0 4 4 0 0 7 0 0
3 0 3 0 4 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
7 3 4 0 0 0 0 0 0 0 0
4 7 3 0 0 0 0 0 0 0 0
3 4 7 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 0 3 0 3 0 4 0
7 0 0 3 3 3 4 4 0
7 7 0 3 0 3 4 0 0
0 4 0 7 0 0 3 0 3
4 4 0 7 0 0 3 3 3
4 0 0 7 7 0 3 0 3
3 0 3 0 4 0 7 0 0
3 3 3 4 4 0 7 0 0
3 0 3 4 0 0 7 7 0
```

**Train 4 input**
```text
2 2 2 0 5 5 0 0 8 8 8
2 0 2 0 5 5 0 0 0 8 0
2 2 2 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 2 0 0 0 0 0 0 0 0 0
8 5 0 0 0 0 0 0 0 0 0
2 8 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
5 5 0 2 2 2
5 5 0 2 0 2
5 0 0 2 2 2
8 8 8 5 5 0
0 8 0 5 5 0
0 0 0 5 0 0
2 2 2 8 8 8
2 0 2 0 8 0
2 2 2 0 0 0
```

**Test 1 input**
```text
2 0 0 0 4 0 4 0 0 7 0
2 0 0 0 4 4 4 0 7 7 0
2 2 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
7 2 4 0 0 0 0 0 0 0 0
2 4 7 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 7 0 2 0 0 4 0 4
7 7 0 2 0 0 4 4 4
7 0 0 2 2 0 0 0 0
2 0 0 4 0 4 0 7 0
2 0 0 4 4 4 7 7 0
2 2 0 0 0 0 7 0 0
```

## Overlay Transformed Prototype Stamps into a Count Map (`hard_118_overlay_transformed_prototype_stamps_into_count_map`)

**Difficulty:** hard

**Skills:** prototype extraction, anchor-coded transforms, count-map synthesis

**Scaffold notes:**
- The color-8 object in the corner is the prototype.
- Singleton code cells elsewhere say which transform to stamp at that anchor.
- Overlay all transformed copies and output the coverage count map.

**Written solution:** Extract the prototype object from the corner, then for every singleton transform code elsewhere, stamp the appropriately transformed prototype with that cell as the anchor. Count overlaps across all stamps and convert the counts into the output colors.

**Program solution (Python reference):**
```python
def solve_hard_118_overlay_transformed_prototype_stamps_into_count_map(g):
    h,w=dims(g)
    proto_comp=max([comp for comp in connected_components(g, colors={8})], key=lambda comp: comp["area"])
    proto=object_crop_from_component(g, proto_comp)
    counts=zeros(h,w)
    for r in range(h):
        for c in range(w):
            code=g[r][c]
            if code in (1,2,3,4):
                obj=apply_transform_code(proto, code)
                count_stamp(counts, obj, r, c)
    return encode_count_map(counts)
```

**Train 1 input**
```text
8 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 2 0 0
8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 2 0
0 0 2 2 0 2 2 0 2 2 2 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 2 2 2 0 0 0 2 2 2 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
8 8 0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 2 2 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
8 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 0 0 0 2 2
0 0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 2 2 0 0 0
0 2 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
8 0 8 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2 2 0 0 0
0 0 2 2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0 0
```

## Build the Pairwise Union Gallery (`hard_119_build_pairwise_union_gallery`)

**Difficulty:** hard

**Skills:** boolean shape operations, pairwise construction, gallery layout

**Scaffold notes:**
- Order the input objects from left to right.
- For every ordered pair, take the union of their normalized binary masks.
- Arrange those union panels in a matrix gallery.

**Written solution:** Normalize the input shapes, compute the binary union for every ordered pair of objects, color the union cells, and arrange all pairwise unions in a gallery matrix.

**Program solution (Python reference):**
```python
def solve_hard_119_build_pairwise_union_gallery(g):
    comps=sorted(connected_components(g), key=lambda comp: (comp["bbox"][1], comp["bbox"][0]))
    objs=[normalize_binary(object_crop_from_component(g, comp)) for comp in comps]
    ph=max(len(o) for o in objs)
    pw=max(len(o[0]) for o in objs)
    padded=[]
    for obj in objs:
        tmp=zeros(ph,pw)
        for r in range(len(obj)):
            for c in range(len(obj[0])):
                if obj[r][c]:
                    tmp[r][c]=1
        padded.append(tmp)
    panels=[]
    for a in padded:
        row=[]
        for b in padded:
            union=zeros(ph,pw)
            for r in range(ph):
                for c in range(pw):
                    if a[r][c] or b[r][c]:
                        union[r][c]=8
            row.append(union)
        panels.append(row)
    return gallery_grid(panels, gap=1)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 3 3 0 0 4 4 0 0 0 0 0
0 2 0 0 0 0 0 3 0 0 0 0 4 4 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 0 0 0 8 8 8 0 8 8 0
8 0 0 0 8 8 0 0 8 8 8
8 8 0 0 8 8 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 8 8 8
8 8 0 0 0 8 0 0 0 8 8
8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 8 8 8 0 8 8 0
8 8 8 0 0 8 8 0 0 8 8
8 8 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 0 3 0 0 0 4 4 4 0 0 0 0
0 2 2 0 0 0 0 3 3 3 0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0 0 8 8 8 0 8 8 8
8 8 0 0 8 8 8 0 8 8 0
8 0 0 0 8 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 0 8 0 8 8 8
8 8 8 0 8 8 8 0 8 8 8
8 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 8 8 8
8 8 0 0 8 8 8 0 8 0 0
8 8 8 0 8 8 8 0 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 3 0 0 0 4 0 0 0 0
0 2 2 2 0 0 0 3 3 0 0 0 4 0 0 0 0
0 2 0 2 0 0 0 3 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 8 0 8 8 8 0 8 0 8
8 8 8 0 8 8 8 0 8 8 8
8 0 8 0 8 0 8 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 0 8 0 0 8 8 0
8 8 8 0 8 8 0 0 8 8 0
8 0 8 0 8 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 8 0 0 8 0 0
8 8 8 0 8 8 0 0 8 0 0
8 8 8 0 8 8 0 0 8 8 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 5 5 0 0 0 0 8 8 8 0 0
0 2 0 2 0 0 0 5 5 0 0 0 0 0 8 0 0 0
0 2 2 2 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 4 output**
```text
8 8 8 0 8 8 8 0 8 8 8
8 0 8 0 8 8 8 0 8 8 8
8 8 8 0 8 8 8 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 0 0 8 8 8
8 8 8 0 8 8 0 0 8 8 0
8 8 8 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 8 0 8 8 8 0 8 8 8
8 8 8 0 8 8 0 0 0 8 0
8 8 8 0 8 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 3 0 0 0 4 4 0 0 0
0 2 0 0 0 0 0 3 3 3 0 0 0 0 4 4 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 0 0 0 8 0 8 0 8 8 0
8 0 0 0 8 8 8 0 8 8 8
8 8 0 0 8 8 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 8 8
8 8 8 0 8 8 8 0 8 8 8
8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 8 8 8 0 8 8 0
8 8 8 0 8 8 8 0 0 8 8
8 8 0 0 0 0 0 0 0 0 0
```

