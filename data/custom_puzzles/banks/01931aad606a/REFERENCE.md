# ARC Puzzle Bank — Third 21 Puzzles
This third bank contains 21 more ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It continues the numbering inside each difficulty band (`15`–`21`) so it reads as a direct continuation of the first two bundles.
Each puzzle includes train/test examples, scaffold notes, a written solution, and a Python reference solver.
Files in this bundle:
- `arc_puzzle_bank_third_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_third_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_third_21.md` — this human-readable catalog.

## Summary

### Easy (7)
- `easy_15_exact_descending_diagonal_pairs` — **Exact Descending Diagonal Pairs**
- `easy_16_fill_x_centers` — **Fill the Missing X Centers**
- `easy_17_extend_exact_horizontal_triples` — **Extend Exact Horizontal Triples**
- `easy_18_mirror_singletons_across_vertical_midline` — **Mirror Singletons Across the Vertical Midline**
- `easy_19_grow_crosses_from_red_seeds` — **Grow Crosses from Red Seeds**
- `easy_20_fill_the_singleton_row` — **Fill the Singleton Row**
- `easy_21_tight_crop_of_nonzero_bbox` — **Tight Crop of the Nonzero Bounding Box**

### Medium (7)
- `medium_15_outline_filled_rectangles` — **Outline the Filled Rectangles**
- `medium_16_shift_all_objects_by_direction_key` — **Shift All Objects by the Direction Key**
- `medium_17_keep_only_hole_bearing_components` — **Keep Only the Hole-Bearing Components**
- `medium_18_rotate_each_l_triomino_clockwise` — **Rotate Each L-Triomino Clockwise**
- `medium_19_keep_corner_touching_components` — **Keep the Corner-Touching Components**
- `medium_20_crop_and_pack_components_horizontally` — **Crop and Pack Components Horizontally**
- `medium_21_keep_components_matching_template_under_rotation` — **Keep Components Matching the Template Under Rotation**

### Hard (7)
- `hard_15_make_transform_panel_from_single_template` — **Make a Transform Panel from a Single Template**
- `hard_16_scale_the_unique_vertically_symmetric_component` — **Scale the Unique Vertically Symmetric Component**
- `hard_17_center_template_inside_every_frame` — **Center the Template Inside Every Frame**
- `hard_18_pack_components_by_area_with_palette_top_to_bottom` — **Pack Components by Area with a Top-to-Bottom Palette**
- `hard_19_complete_missing_quadrant_by_rotation` — **Complete the Missing Quadrant by Rotation**
- `hard_20_boolean_combine_two_templates_by_key` — **Boolean-Combine Two Templates by the Key**
- `hard_21_cartesian_product_of_row_shapes_and_column_colors` — **Cartesian Product of Row Shapes and Column Colors**

## Exact Descending Diagonal Pairs (`easy_15_exact_descending_diagonal_pairs`)

**Difficulty:** easy

**Skills:** diagonal run detection, exact length, same-size recolor

**Scaffold notes:**
- Start only where the up-left neighbor is not red(2).
- Count the full run along the down-right diagonal.
- Recolor only the runs whose length is exactly 2.

**Written solution:** Recolor every down-right diagonal run of red(2) cells of exact length 2 to cyan(8). Leave singletons and longer diagonal runs unchanged.

**Program solution (Python reference):**
```python
def solve_easy_15_exact_descending_diagonal_pairs(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 2:
                continue
            if r > 0 and c > 0 and g[r - 1][c - 1] == 2:
                continue
            rr, cc = r, c
            cells = []
            while rr < h and cc < w and g[rr][cc] == 2:
                cells.append((rr, cc))
                rr += 1
                cc += 1
            if len(cells) == 2:
                for cr, cc in cells:
                    out[cr][cc] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 2 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 2 0 0 0
0 8 0 0 0 0 0 2 0 0
0 0 8 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0
2 0 0 0 0 2 0 0 0
0 2 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0
8 0 0 0 0 2 0 0 0
0 8 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 2 0 0
0 0 2 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0
2 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 8 0 0
0 0 2 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0
2 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 2 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Fill the Missing X Centers (`easy_16_fill_x_centers`)

**Difficulty:** easy

**Skills:** local diagonal neighborhood, pattern completion, same-size fill

**Scaffold notes:**
- Look only at black cells with room on all four diagonals.
- Check the four diagonal positions, not the orthogonal ones.
- If all four are green(3), place yellow(4) in the middle.

**Written solution:** Whenever a black(0) cell has green(3) cells on all four diagonal neighbors, fill that center with yellow(4). Everything else stays the same.

**Program solution (Python reference):**
```python
def solve_easy_16_fill_x_centers(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if g[r][c] != 0:
                continue
            if g[r - 1][c - 1] == 3 and g[r - 1][c + 1] == 3 and g[r + 1][c - 1] == 3 and g[r + 1][c + 1] == 3:
                out[r][c] = 4
    return out
```

**Train 1 input**
```text
3 0 3 0 0 0 0
0 0 0 0 0 0 0
3 0 3 0 3 0 0
0 0 0 0 3 0 0
0 0 3 0 3 0 0
0 0 0 0 3 0 3
0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 0 3 0 0 0 0
0 4 0 0 0 0 0
3 0 3 0 3 0 0
0 0 0 4 3 0 0
0 0 3 0 3 0 0
0 0 0 0 3 0 3
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 0 0 3 0 0
0 0 0 3 0 3 0 3 0
0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 4 0 3 0 0
0 0 0 3 0 3 0 3 0
0 3 0 3 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 3 0
0 0 3 0 0 0 0 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 3 0
0 0 3 0 0 0 4 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 4 0 4 0 0
0 0 0 3 0 3 0 3 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 3 0 3 0 0 3 0
0 0 0 0 0 3 0 0
0 3 0 3 0 0 3 0
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 3 0 3 0 0 3 0
0 0 4 0 0 3 0 0
0 3 0 3 0 0 3 0
0 0 0 0 3 0 3 0
0 0 0 0 0 4 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
```

## Extend Exact Horizontal Triples (`easy_17_extend_exact_horizontal_triples`)

**Difficulty:** easy

**Skills:** horizontal run detection, context check, same-size growth

**Scaffold notes:**
- Scan row by row and group contiguous orange(7) cells.
- Only exact length-3 runs can grow.
- Make sure both extension cells are inside the grid and currently black(0).

**Written solution:** Find every horizontal orange(7) run of exact length 3 whose immediate left and right neighbors are black(0). Extend it by one orange cell on each side to make a length-5 bar.

**Program solution (Python reference):**
```python
def solve_easy_17_extend_exact_horizontal_triples(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        c = 0
        while c < w:
            if g[r][c] != 7:
                c += 1
                continue
            s = c
            while c < w and g[r][c] == 7:
                c += 1
            if c - s == 3 and s > 0 and c < w and g[r][s - 1] == 0 and g[r][c] == 0:
                out[r][s - 1] = 7
                out[r][c] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 7 7 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 7 7 0
0 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7
0 0 0 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Mirror Singletons Across the Vertical Midline (`easy_18_mirror_singletons_across_vertical_midline`)

**Difficulty:** easy

**Skills:** global symmetry, coordinate transform, same-size copy

**Scaffold notes:**
- Use the full grid width to find the mirror column.
- Keep original cells and add their mirrored copies.
- A cell already on the center column stays where it is.

**Written solution:** Every nonzero cell is a singleton marker. Copy each one to its mirror position across the full grid’s vertical center line, keeping the original cell too.

**Program solution (Python reference):**
```python
def solve_easy_18_mirror_singletons_across_vertical_midline(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[r][w - 1 - c] = g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0
5 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
```

## Grow Crosses from Red Seeds (`easy_19_grow_crosses_from_red_seeds`)

**Difficulty:** easy

**Skills:** local expansion, orthogonal neighbors, same-size construction

**Scaffold notes:**
- Find the red seed cells first.
- For each seed, visit up, down, left, and right.
- Paint neighbors blue(1), then restore the seed itself to red(2).

**Written solution:** Each red(2) seed keeps its own cell and paints its four orthogonal neighbors blue(1), as long as those neighbors are inside the grid.

**Program solution (Python reference):**
```python
def solve_easy_19_grow_crosses_from_red_seeds(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    seeds = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in seeds:
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and out[nr][nc] == 0:
                out[nr][nc] = 1
    for r, c in seeds:
        out[r][c] = 2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 1 0 0 0 0
0 1 2 1 0 0 0
0 0 1 0 0 1 0
0 0 0 0 1 2 1
0 0 0 0 0 1 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 1 0 0 0 0
0 0 0 1 2 1 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 1 2 1 0 0 0 1 0
0 0 1 0 0 0 1 2 1
0 0 0 0 0 0 0 1 0
```

**Train 3 input**
```text
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 1 2 1 0 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 1 2 1 0 0 0
0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 0 0 0
1 2 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 1 2 1 0
0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0
0 1 2 1 0 0 0 0
0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Fill the Singleton Row (`easy_20_fill_the_singleton_row`)

**Difficulty:** easy

**Skills:** singleton key, row selection, same-size painting

**Scaffold notes:**
- Locate the one nonzero cell.
- Read both its row index and its color.
- Paint every column in that row with the same color.

**Written solution:** There is exactly one colored cell. Fill its entire row with that same color on an otherwise black canvas of the same size.

**Program solution (Python reference):**
```python
def solve_easy_20_fill_the_singleton_row(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    cells = [(r, c, g[r][c]) for r in range(h) for c in range(w) if g[r][c] != 0]
    assert len(cells) == 1
    r, c, color = cells[0]
    for cc in range(w):
        out[r][cc] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
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
2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0
```

## Tight Crop of the Nonzero Bounding Box (`easy_21_tight_crop_of_nonzero_bbox`)

**Difficulty:** easy

**Skills:** bounding box, size change, exact crop

**Scaffold notes:**
- Find the min and max rows containing nonzero cells.
- Find the min and max columns containing nonzero cells.
- Slice out exactly that rectangle.

**Written solution:** Take the tight bounding box around all nonzero cells and output only that cropped rectangle, preserving the colors exactly.

**Program solution (Python reference):**
```python
def solve_easy_21_tight_crop_of_nonzero_bbox(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 0
2 2 0 0 0
0 0 0 5 5
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 0 0 0
4 4 4 0 0
0 4 0 0 0
0 0 0 0 0
0 0 0 0 7
0 0 0 0 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3 3 3
0 3 0 3
0 3 3 3
2 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 0 0 0 0
0 6 6 0 0 0
0 0 0 0 2 0
0 0 0 0 2 2
```

## Outline the Filled Rectangles (`medium_15_outline_filled_rectangles`)

**Difficulty:** medium

**Skills:** component bounding boxes, rectangle reasoning, same-size transform

**Scaffold notes:**
- Treat each nonzero component as one rectangle.
- Recover its bounding box from the component cells.
- Keep only the cells on the top, bottom, left, or right edge of that box.

**Written solution:** Each colored component is a solid filled rectangle. Replace every one with just its border, preserving its color and position.

**Program solution (Python reference):**
```python
def solve_medium_15_outline_filled_rectangles(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        color = comp["color"]
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if r in (r0, r1) or c in (c0, c1):
                    out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0
0 7 7 7 0 0 3 3 3 0
0 7 7 7 0 0 3 3 3 0
0 7 7 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0
0 7 7 7 0 0 3 0 3 0
0 7 0 7 0 0 3 3 3 0
0 7 0 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
6 6 6 6 6 0 0 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 6 6 6 0 0 0 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 2 2 0
0 0 5 5 5 5 0 0 2 2 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 2 2 0
0 0 5 5 5 5 0 0 2 2 0
0 0 5 0 0 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Shift All Objects by the Direction Key (`medium_16_shift_all_objects_by_direction_key`)

**Difficulty:** medium

**Skills:** control-color mapping, global translation, object movement

**Scaffold notes:**
- Read the singleton key color first and map it to a direction.
- Ignore the control cell after decoding the direction.
- Translate every remaining nonzero cell by exactly one step.

**Written solution:** A singleton control color chooses a direction: blue(1)=up, red(2)=down, green(3)=left, yellow(4)=right. Move every other object one cell in that direction onto a blank output grid and discard the control marker.

**Program solution (Python reference):**
```python
def solve_medium_16_shift_all_objects_by_direction_key(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    counts = Counter(v for row in g for v in row if v != 0)
    control = None
    for color in (1, 2, 3, 4):
        if counts.get(color, 0) == 1:
            control = color
            break
    assert control is not None
    delta = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}[control]
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or v == control:
                continue
            nr, nc = r + delta[0], c + delta[1]
            out[nr][nc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 6 6 6 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 4 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
```

**Train 4 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

## Keep Only the Hole-Bearing Components (`medium_17_keep_only_hole_bearing_components`)

**Difficulty:** medium

**Skills:** component analysis, hole detection, selection

**Scaffold notes:**
- Process one connected component at a time.
- Look inside its bounding box and distinguish enclosed empty cells from outside empty space.
- Preserve only components that truly trap a hole.

**Written solution:** Keep only the components that enclose at least one internal hole. Solid shapes and open shapes are removed.

**Program solution (Python reference):**
```python
def solve_medium_17_keep_only_hole_bearing_components(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        if has_hole(comp["cells"]):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 6 6 6 6 6
0 2 2 2 0 0 0 6 0 0 0 6
0 2 0 2 0 0 0 6 0 0 0 6
0 2 2 2 0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 6 6 6 6 6
0 2 2 2 0 0 0 6 0 0 0 6
0 2 0 2 0 0 0 6 0 0 0 6
0 2 2 2 0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0
0 3 0 0 0 0 8 8 8 0
0 3 3 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 0 0
0 0 5 5 5 0 0 0 0 0 2 2 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 0 5 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 4 0 0 0 0 4 0
0 0 0 0 0 0 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 3 0 0 0 0 7 0 7 0
0 0 3 3 3 0 0 0 7 7 7 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Rotate Each L-Triomino Clockwise (`medium_18_rotate_each_l_triomino_clockwise`)

**Difficulty:** medium

**Skills:** object-wise transform, rotation, bounding-box anchoring

**Scaffold notes:**
- Separate the L pieces into components.
- Normalize each one inside its 2×2 box.
- Rotate the offsets clockwise and place them back at the same top-left anchor.

**Written solution:** Every component is an L-triomino. Rotate each one 90° clockwise inside its own tight 2×2 bounding box.

**Program solution (Python reference):**
```python
def solve_medium_18_rotate_each_l_triomino_clockwise(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        offsets = norm(comp["cells"])
        rot = rotate_offsets(offsets, 1)
        for dr, dc in rot:
            out[r0 + dr][c0 + dc] = comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0
0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 6 6 0
0 6 6 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 6 0
0 6 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
6 6 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 6 0 0 6 6 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
6 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Keep the Corner-Touching Components (`medium_19_keep_corner_touching_components`)

**Difficulty:** medium

**Skills:** border reasoning, component selection, same-size filtering

**Scaffold notes:**
- For each component, ask whether it touches top or bottom.
- Then ask whether it touches left or right.
- Keep it only if both tests are true.

**Written solution:** Keep only the components that touch both a horizontal border and a vertical border of the grid, meaning they occupy a corner region. Remove components that touch just one border or none.

**Program solution (Python reference):**
```python
def solve_medium_19_keep_corner_touching_components(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    for comp in components_by_color(g):
        if touches_corner(comp["cells"], h, w):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out
```

**Train 1 input**
```text
2 2 0 0 0 0 0 0 3 0
2 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 0 0 0 0 3 0
2 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 5 0
7 7 0 0 0 0 0 5 5
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 5 0
7 7 0 0 0 0 0 5 5
```

**Train 3 input**
```text
6 0 0 0 0 0 0 0 0 4 4
6 6 0 0 0 0 0 0 0 0 4
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
```

**Train 3 output**
```text
6 0 0 0 0 0 0 0 0 4 4
6 6 0 0 0 0 0 0 0 0 4
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 6 6
```

**Test 1 output**
```text
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 6 6
```

## Crop and Pack Components Horizontally (`medium_20_crop_and_pack_components_horizontally`)

**Difficulty:** medium

**Skills:** component extraction, size change, packing

**Scaffold notes:**
- Sort components by where they appear from left to right.
- Crop each one to its tight box before packing.
- Build a new output width from the crop widths plus one-column gaps.

**Written solution:** Crop each component to its own tight bounding box, keep the original left-to-right order, and pack the cropped pieces side by side with one blank column between them. Align them to the top of the new canvas.

**Program solution (Python reference):**
```python
def solve_medium_20_crop_and_pack_components_horizontally(g: Grid) -> Grid:
    comps = components_by_color(g)
    comps.sort(key=lambda comp: (min(c for r, c in comp["cells"]), min(r for r, c in comp["cells"])))
    crops = [crop_to_bbox(g, comp["cells"]) for comp in comps]
    H = max(len(crop) for crop in crops)
    W = sum(len(crop[0]) for crop in crops) + (len(crops) - 1)
    out = zeros(H, W)
    x = 0
    for crop in crops:
        ch, cw = len(crop), len(crop[0])
        for r in range(ch):
            for c in range(cw):
                out[r][x + c] = crop[r][c]
        x += cw + 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 4 0 0 6 6 0
2 2 0 4 4 4 0 0 6 6
0 0 0 0 4 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 3 0 0 0 5 5 5 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7 7 0 3 0 0 5 0
7 0 7 0 3 0 5 5 5
7 7 7 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 0 2 0 0 4 4 4
8 8 8 0 2 2 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 2 0 0 0 0 7 0 0
0 0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 0 0 2 0 0 0 7 0
0 6 6 0 2 2 0 7 7 7
0 0 0 0 0 0 0 0 7 0
```

## Keep Components Matching the Template Under Rotation (`medium_21_keep_components_matching_template_under_rotation`)

**Difficulty:** medium

**Skills:** template matching, rotation invariance, object filtering

**Scaffold notes:**
- Extract and normalize the template first.
- Generate all four rotated versions of the template.
- Compare each candidate component after normalizing its shape.

**Written solution:** The color-1 component is the template. Keep only the color-3 components whose shape matches that template under some rotation, and recolor those kept components to cyan(8).

**Program solution (Python reference):**
```python
def solve_medium_21_keep_components_matching_template_under_rotation(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template_comp = components_by_color(g, {1})[0]
    target_shapes = {tuple(shape) for shape in canonical_rotations(norm(template_comp["cells"]))}
    for comp in components_by_color(g, {3}):
        if tuple(norm(comp["cells"])) in target_shapes:
            for r, c in comp["cells"]:
                out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 3 3 0 0 0 0
0 1 1 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 3 3 3 0
0 0 0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 0 3 3 3 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 3 3 3 0 0
0 1 1 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 3 3 0 0
0 0 3 3 3 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Make a Transform Panel from a Single Template (`hard_15_make_transform_panel_from_single_template`)

**Difficulty:** hard

**Skills:** template extraction, control grid, rotation and reflection, size change

**Scaffold notes:**
- The four control colors form a 2×2 arrangement whose positions determine the output quadrants.
- Apply the right transform to the same template for each quadrant.
- Stamp the transformed copies onto a fresh panel with one-row and one-column gaps.

**Written solution:** Extract the lone color-2 template, then build a 2×2 output panel in gray(7). Each control marker says which transform to apply in its quadrant: blue(1)=identity, green(3)=rotate 90° clockwise, yellow(4)=rotate 180°, magenta(6)=vertical reflection.

**Program solution (Python reference):**
```python
def solve_hard_15_make_transform_panel_from_single_template(g: Grid) -> Grid:
    template_comp = components_by_color(g, {2})[0]
    template = crop_to_bbox(g, template_comp["cells"])
    th, tw = dims(template)
    assert th == tw
    control_cells = [(r, c, g[r][c]) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] in (1, 3, 4, 6)]
    pos = sorted_control_grid_positions(control_cells)
    out = zeros(2 * th + 1, 2 * tw + 1)
    mapping = {1: ("rot", 0), 3: ("rot", 1), 4: ("rot", 2), 6: ("ref", 0)}
    for qr, qc, _r, _c, color in pos:
        kind, arg = mapping[color]
        block = rotate_grid_times(template, arg) if kind == "rot" else reflect_grid_vert(template)
        for r in range(th):
            for c in range(tw):
                if block[r][c] != 0:
                    out[qr * (th + 1) + r][qc * (tw + 1) + c] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 6 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0 4 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 0 0 0 0 0 7
7 0 0 0 0 0 7
7 7 7 0 7 7 7
0 0 0 0 0 0 0
7 7 7 0 7 7 7
7 0 0 0 0 0 7
7 0 0 0 0 0 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 3 0 0
0 0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 7 0 0 7 7
0 7 7 0 7 7 0
7 7 0 0 7 0 0
0 0 0 0 0 0 0
7 7 0 0 7 7 0
0 7 7 0 0 7 7
0 0 7 0 0 0 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 6 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 7 0 0 0 0 7
0 7 0 0 7 7 7
0 7 7 0 7 0 0
0 0 0 0 0 0 0
0 0 7 0 7 0 0
7 7 7 0 7 7 7
7 0 0 0 0 0 7
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 4 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 7 0 7 7 7
0 0 7 0 7 0 0
7 7 7 0 7 0 0
0 0 0 0 0 0 0
7 0 0 0 7 7 7
7 0 0 0 0 0 7
7 7 7 0 0 0 7
```

## Scale the Unique Vertically Symmetric Component (`hard_16_scale_the_unique_vertically_symmetric_component`)

**Difficulty:** hard

**Skills:** symmetry test, component selection, 2× scaling, size change

**Scaffold notes:**
- Normalize each component shape before testing symmetry.
- Reflect the shape across its own vertical axis to see which one matches itself.
- After choosing the symmetric component, scale every occupied cell into a 2×2 block.

**Written solution:** Among the color-3 components, find the only one whose shape is vertically symmetric inside its bounding box. Scale that shape by 2× on a fresh canvas and recolor it to cyan(8).

**Program solution (Python reference):**
```python
def solve_hard_16_scale_the_unique_vertically_symmetric_component(g: Grid) -> Grid:
    comps = components_by_color(g, {3})
    chosen = None
    for comp in comps:
        if vertical_symmetric(norm(comp["cells"])):
            chosen = comp
            break
    assert chosen is not None
    offsets = scale_offsets(norm(chosen["cells"]), 2)
    mr = max(r for r, c in offsets)
    mc = max(c for r, c in offsets)
    out = zeros(mr + 1, mc + 1)
    for r, c in offsets:
        out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 3 3 0 0 0
0 3 3 3 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 3 0 3 0 0 0
0 3 0 0 0 3 3 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8 8 8
8 8 8 8 8 8
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 3 0 0 0 0 0 3 3 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8 8 0 0
0 0 8 8 0 0
8 8 8 8 8 8
8 8 8 8 8 8
0 0 8 8 0 0
0 0 8 8 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 3 0 3 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 0 0 8 8
8 8 0 0 8 8
8 8 8 8 8 8
8 8 8 8 8 8
```

## Center the Template Inside Every Frame (`hard_17_center_template_inside_every_frame`)

**Difficulty:** hard

**Skills:** template extraction, frame interiors, centering, multi-object stamping

**Scaffold notes:**
- Separate the source template from the frame objects.
- For each frame, compute the interior size and the template’s size.
- Place the template at the centered interior anchor, using the frame color.

**Written solution:** The color-2 component is a template. Copy it into the center of every rectangular frame, recoloring each copy to match that frame’s color, and output the frames plus the centered copies on a fresh same-size canvas.

**Program solution (Python reference):**
```python
def solve_hard_17_center_template_inside_every_frame(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template_comp = components_by_color(g, {2})[0]
    template_offsets = norm(template_comp["cells"])
    tr, tc = max(r for r, c in template_offsets) + 1, max(c for r, c in template_offsets) + 1
    for comp in components_by_color(g):
        color = comp["color"]
        if color == 2:
            continue
        r0, c0, r1, c1 = bbox(comp["cells"])
        for r, c in comp["cells"]:
            out[r][c] = color
        ih, iw = r1 - r0 - 1, c1 - c0 - 1
        sr = r0 + 1 + (ih - tr) // 2
        sc = c0 + 1 + (iw - tc) // 2
        for dr, dc in template_offsets:
            out[sr + dr][sc + dc] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 6 6 6 6 6 0 0
0 2 2 0 0 0 6 0 0 0 6 0 0
0 0 0 0 0 0 6 0 0 0 6 0 0
0 0 0 0 0 0 6 0 0 0 6 0 0
0 4 4 4 4 0 6 6 6 6 6 0 0
0 4 0 0 4 0 0 0 0 0 0 0 0
0 4 0 0 4 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 6 6 0 0 6 0 0
0 0 0 0 0 0 6 6 6 0 6 0 0
0 0 0 0 0 0 6 0 0 0 6 0 0
0 4 4 4 4 0 6 6 6 6 6 0 0
0 4 4 0 4 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 7 7 7 7 7 7 7 0
0 0 2 2 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 0 0 0 0 7 0 7 7 0 0 7 0
0 0 0 0 0 0 7 0 0 7 7 0 7 0
0 0 0 0 0 0 7 7 7 7 7 7 7 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0
0 0 3 3 3 0 3 0 0 0 0 0 0 0
0 0 3 0 3 3 3 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 5 5 5 5 5 5 5 0
0 2 2 2 0 0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 5 0 0 0 0 0 5 0
0 0 0 0 0 0 0 5 0 0 0 0 0 5 0
0 8 8 8 8 8 0 5 5 5 5 5 5 5 0
0 8 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 5 5 5 0 5 0
0 0 0 0 0 0 0 5 0 0 0 0 0 5 0
0 8 8 8 8 8 0 5 5 5 5 5 5 5 0
0 8 0 8 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 6 6 6 6 6 0 0
0 2 0 0 0 0 0 6 0 0 0 6 0 0
0 2 2 2 0 0 0 6 0 0 0 6 0 0
0 0 0 4 4 4 4 4 4 4 0 6 0 0
0 0 0 4 0 0 0 6 6 4 6 6 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 6 6 0 0 6 0 0
0 0 0 0 0 0 0 6 6 0 0 6 0 0
0 0 0 4 4 4 6 4 4 4 6 6 0 0
0 0 0 4 0 0 6 6 6 4 6 6 0 0
0 0 0 4 0 4 6 6 6 4 0 0 0 0
0 0 0 4 0 4 0 0 0 4 0 0 0 0
0 0 0 4 0 4 4 4 0 4 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Pack Components by Area with a Top-to-Bottom Palette (`hard_18_pack_components_by_area_with_palette_top_to_bottom`)

**Difficulty:** hard

**Skills:** area ranking, palette decoding, size change, vertical packing

**Scaffold notes:**
- Decode the palette order from the first column before touching the shapes.
- Rank the target components by number of occupied cells.
- Recolor after cropping, then stack on a fresh canvas.

**Written solution:** The first-column singletons form a top-to-bottom palette. Sort the color-3 components by area from largest to smallest, crop each one to its tight box, recolor them using the palette order, and pack them vertically with one blank row between pieces.

**Program solution (Python reference):**
```python
def solve_hard_18_pack_components_by_area_with_palette_top_to_bottom(g: Grid) -> Grid:
    palette = [(r, c, g[r][c]) for r in range(len(g)) for c in range(len(g[0])) if c == 0 and g[r][c] not in (0, 3)]
    palette.sort()
    colors = [color for _r, _c, color in palette]
    comps = components_by_color(g, {3})
    comps.sort(key=lambda comp: (-len(comp["cells"]), min(r for r, c in comp["cells"]), min(c for r, c in comp["cells"])))
    crops = []
    for comp, color in zip(comps, colors):
        crop = crop_to_bbox(g, comp["cells"])
        recol = [[color if v != 0 else 0 for v in row] for row in crop]
        crops.append(recol)
    H = sum(len(crop) for crop in crops) + (len(crops) - 1)
    W = max(len(crop[0]) for crop in crops)
    out = zeros(H, W)
    y = 0
    for crop in crops:
        ch, cw = len(crop), len(crop[0])
        for r in range(ch):
            for c in range(cw):
                out[y + r][c] = crop[r][c]
        y += ch + 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0 3 0 0 0
7 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
5 5 5
5 5 5
0 0 0
0 7 0
7 7 7
0 7 0
0 0 0
2 0 0
2 2 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
8 0 0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6
6 0 6
6 6 6
0 0 0
8 8 0
0 8 8
0 0 0
4 0 0
4 4 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 3 0 0 0
5 0 0 0 3 3 3 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 0 0
9 0 0
9 9 9
0 0 0
0 5 0
5 5 5
0 0 0
7 0 0
7 7 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0 0 0 3 0 0
6 0 0 0 3 3 3 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
4 4 4
4 0 4
4 4 4
0 0 0
0 6 0
6 6 6
0 6 0
0 0 0
8 0 0
8 8 0
```

## Complete the Missing Quadrant by Rotation (`hard_19_complete_missing_quadrant_by_rotation`)

**Difficulty:** hard

**Skills:** rotational symmetry, center-based transform, same-size completion

**Scaffold notes:**
- Use the grid center as the rotation pivot.
- Take every existing color-2 cell and rotate it around that center.
- The union of those rotations gives the completed output.

**Written solution:** The color-2 pattern should appear in all four quadrants as 90° rotations around the center marker. Add the missing rotated quadrant so the full pattern has fourfold rotational symmetry.

**Program solution (Python reference):**
```python
def solve_hard_19_complete_missing_quadrant_by_rotation(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w and h % 2 == 1
    ctr = h // 2
    out = clone(g)
    cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in cells:
        rr, cc = r, c
        for _ in range(3):
            dr, dc = rr - ctr, cc - ctr
            rr, cc = ctr + dc, ctr - dr
            out[rr][cc] = 2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 2 0 0
0 2 2 0 0 0 2 0 0
0 2 0 0 0 0 0 2 0
0 0 0 0 9 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 2 0 0
0 2 2 0 0 0 2 0 0
0 2 0 0 0 0 0 2 0
0 0 0 0 9 0 0 0 0
0 2 0 0 0 0 0 2 0
0 0 2 0 0 0 2 2 0
0 0 2 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 2 0 0
0 0 0 2 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 2 0 0
0 0 0 0 0 9 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 2 0 0
0 0 0 2 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 2 0 0 0
0 0 0 2 0 2 0 2 0
0 2 2 0 0 0 2 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 2 0 0 0
0 0 0 2 0 2 0 2 0
0 2 2 0 0 0 2 0 0
0 0 0 0 9 0 0 0 0
0 0 2 0 0 0 2 2 0
0 2 0 2 0 2 0 0 0
0 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 9 0 0 2 0 0
0 0 0 2 0 0 0 2 2 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 2 2 0 0 0 2 0 0 0
0 0 2 0 0 9 0 0 2 0 0
0 0 0 2 0 0 0 2 2 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Boolean-Combine Two Templates by the Key (`hard_20_boolean_combine_two_templates_by_key`)

**Difficulty:** hard

**Skills:** shape normalization, set operations, control-color mapping, size change

**Scaffold notes:**
- Normalize both shapes independently before combining them.
- Treat the occupied cells as sets of coordinates.
- After the chosen boolean operation, crop the result to its own tight bounding box.

**Written solution:** Normalize the color-1 and color-2 components to a common origin, then combine their occupied-cell sets according to the singleton key: green(3)=union, yellow(4)=intersection, magenta(6)=xor. Output the result in gray(8).

**Program solution (Python reference):**
```python
def solve_hard_20_boolean_combine_two_templates_by_key(g: Grid) -> Grid:
    s1 = norm(components_by_color(g, {1})[0]["cells"])
    s2 = norm(components_by_color(g, {2})[0]["cells"])
    counts = Counter(v for row in g for v in row if v != 0)
    control = None
    for color in (3, 4, 6):
        if counts.get(color, 0) == 1:
            control = color
            break
    assert control is not None
    op = {3: "union", 4: "intersection", 6: "xor"}[control]
    res = overlay_sets(s1, s2, op)
    if not res:
        return [[0]]
    mr = max(r for r, c in res)
    mc = max(c for r, c in res)
    out = zeros(mr + 1, mc + 1)
    for r, c in res:
        out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 2 2 0 0 0
0 1 1 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8
8 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8 0
8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 6
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 8
0 8 8
0 8 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6
```

**Test 1 output**
```text
8 0 0
8 0 8
8 0 0
```

## Cartesian Product of Row Shapes and Column Colors (`hard_21_cartesian_product_of_row_shapes_and_column_colors`)

**Difficulty:** hard

**Skills:** panel construction, cross-product reasoning, recoloring, size change

**Scaffold notes:**
- Extract the row shapes and sort them from top to bottom.
- Read the column colors from left to right along the top row.
- Use one fixed slot size and stamp every row-shape / column-color combination into the panel.

**Written solution:** The color-2 components define the rows of a panel, in top-to-bottom order. The colored singletons on the top row define the columns, in left-to-right order. Build a fresh panel where each cell contains the row shape recolored to the column color.

**Program solution (Python reference):**
```python
def solve_hard_21_cartesian_product_of_row_shapes_and_column_colors(g: Grid) -> Grid:
    row_shapes = [crop_to_bbox(g, comp["cells"]) for comp in sorted(components_by_color(g, {2}), key=lambda comp: min(r for r, c in comp["cells"]))]
    col_colors = [g[r][c] for r in range(len(g)) for c in range(len(g[0])) if r == 0 and g[r][c] not in (0, 2)]
    slot_h = max(len(shape) for shape in row_shapes)
    slot_w = max(len(shape[0]) for shape in row_shapes)
    rows = len(row_shapes)
    cols = len(col_colors)
    out = zeros(rows * slot_h + (rows - 1), cols * slot_w + (cols - 1))
    for i, shape in enumerate(row_shapes):
        sh, sw = len(shape), len(shape[0])
        for j, color in enumerate(col_colors):
            y = i * (slot_h + 1)
            x = j * (slot_w + 1)
            for r in range(sh):
                for c in range(sw):
                    if shape[r][c] != 0:
                        out[y + r][x + c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 4 0 0 6 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 0 0 0 6 0 0 0 7 0 0
4 4 0 0 6 6 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 6 0 0 0 7 0
4 4 4 0 6 6 6 0 7 7 7
0 4 0 0 0 6 0 0 0 7 0
```

**Train 2 input**
```text
0 0 0 0 3 0 0 5 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 0 0 5 5 0 0 8 8 0
0 3 3 0 0 5 5 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 5 0 0 0 8 0
3 3 3 0 5 5 5 0 8 8 8
```

**Train 3 input**
```text
0 0 0 9 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 9 0 4 4 4
9 0 9 0 4 0 4
9 9 9 0 4 4 4
0 0 0 0 0 0 0
9 0 0 0 4 0 0
9 9 0 0 4 4 0
0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 5 0 0 7 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 0 0 0 7 0 0 0 3 0 0
5 0 0 0 7 0 0 0 3 0 0
5 5 0 0 7 7 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
5 5 0 0 7 7 0 0 3 3 0
0 5 5 0 0 7 7 0 0 3 3
0 0 0 0 0 0 0 0 0 0 0
```
