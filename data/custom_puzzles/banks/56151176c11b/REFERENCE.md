# ARC Puzzle Bank — Next 21 Puzzles

This second bank contains 21 additional ARC-style puzzles: 7 easy, 7 medium, and 7 hard. It keeps the same structure as the prior bundle, but continues the numbering inside each difficulty band (`08`–`14`) so it reads as a continuation rather than a reset.

Each puzzle includes train/test examples, scaffold notes, a written solution, and a Python reference solver.

Files in this bundle:
- `arc_puzzle_bank_next_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_next_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_next_21.md` — this human-readable catalog.

## Summary

### Easy (7)

- `easy_08_exact_vertical_quadruples` — **Exact Vertical Quadruples**
- `easy_09_fill_plus_centers` — **Fill the Missing Plus Centers**
- `easy_10_fill_single_frame_by_key` — **Fill the Frame by the Singleton Key**
- `easy_11_bridge_single_horizontal_gaps` — **Bridge Single Horizontal Gaps**
- `easy_12_diagonal_shadow_down_right` — **Diagonal Shadow Down-Right**
- `easy_13_keep_leftmost_component` — **Keep Only the Leftmost Component**
- `easy_14_mark_vertical_run_endpoints` — **Mark Vertical Run Endpoints**

### Medium (7)

- `medium_08_complete_rectangle_borders_from_diagonal_corners` — **Complete Rectangle Borders from Diagonal Corners**
- `medium_09_fill_component_bounding_boxes` — **Fill Each Component Bounding Box**
- `medium_10_recolor_objects_by_above_key` — **Recolor Objects by the Key Above**
- `medium_11_keep_shape_matching_template` — **Keep Components Matching the Template Shape**
- `medium_12_reflect_left_objects_across_center_axis` — **Reflect Left Objects Across the Center Axis**
- `medium_13_fill_rectangles_from_diagonal_corners` — **Fill Rectangles from Diagonal Corners**
- `medium_14_select_diagonal_touching_components` — **Select Components Touching the Main Diagonal**

### Hard (7)

- `hard_08_rotate_template_by_control_and_stamp` — **Rotate the Template by the Control Color**
- `hard_09_scale_second_smallest_component_2x` — **Scale the Second-Smallest Component 2x**
- `hard_10_palette_recolor_components_left_to_right` — **Palette-Recolor Components Left to Right**
- `hard_11_intersection_of_two_frame_interiors` — **Intersection of Two Frame Interiors**
- `hard_12_make_matching_shapes_symmetric` — **Make Matching Shapes Symmetric**
- `hard_13_multi_marker_rotated_stamping` — **Stamp Rotated Copies at Multiple Markers**
- `hard_14_select_shape_match_and_recolor_by_majority_singleton` — **Shape Match with Majority-Key Recolor**

## Exact Vertical Quadruples (`easy_08_exact_vertical_quadruples`)

**Difficulty:** easy

**Skills:** run detection, exact length, same-size recolor

**Scaffold notes:**
- Scan one column at a time.
- Group contiguous blue cells into vertical runs.
- Only recolor runs whose length is exactly 4.

**Written solution:** Recolor every vertical run of blue(1) cells of exact length 4 to red(2). Leave shorter and longer vertical runs unchanged.

**Program solution (Python reference):**
```python
def solve_easy_08_exact_vertical_quadruples(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for c in range(w):
        r = 0
        while r < h:
            if g[r][c] != 1:
                r += 1
                continue
            s = r
            while r < h and g[r][c] == 1:
                r += 1
            if r - s == 4:
                for rr in range(s, r):
                    out[rr][c] = 2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0
0 1 0 0 0 1 0 1 0 0 0 0
0 1 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 1 0 2 0 0 0 0
0 2 0 0 0 1 0 2 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 1 0
0 0 1 0 0 1 0 0 1 0
0 0 1 0 0 1 0 0 1 0
0 0 1 0 0 0 0 0 1 0
1 0 1 0 0 0 0 0 0 0
1 0 1 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 2 0
0 0 1 0 0 2 0 0 2 0
0 0 1 0 0 2 0 0 2 0
0 0 1 0 0 0 0 0 2 0
1 0 1 0 0 0 0 0 0 0
1 0 1 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0
0 1 0 0 0 0 0 1 0 0 0 0
0 1 0 1 0 1 0 0 0 0 0 0
0 0 0 1 0 1 0 0 0 0 0 0
0 0 0 1 0 1 0 1 0 0 0 0
0 0 0 1 0 1 0 1 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 2 0 0 0 0
0 2 0 2 0 1 0 0 0 0 0 0
0 0 0 2 0 1 0 0 0 0 0 0
0 0 0 2 0 1 0 1 0 0 0 0
0 0 0 2 0 1 0 1 0 0 0 0
0 0 0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 1 0 0 0 0 0 0 1 0 0 0
0 1 0 0 1 0 0 0 1 0 0 0
0 1 0 0 1 0 0 0 1 0 0 0
0 1 0 0 1 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 1 0 0 0 0 0
1 0 0 0 0 0 1 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 0 0 0 0 2 0 0 0
0 2 0 0 2 0 0 0 2 0 0 0
0 2 0 0 2 0 0 0 2 0 0 0
0 2 0 0 2 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 1 0 0 0 0 0
1 0 0 0 0 0 1 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
```

---

## Fill the Missing Plus Centers (`easy_09_fill_plus_centers`)

**Difficulty:** easy

**Skills:** local neighborhood test, plus completion, same-size edit

**Scaffold notes:**
- Look for a blank cell, not a colored one.
- Check its up, down, left, and right neighbors.
- Only fill centers whose four cardinal neighbors are all green.

**Written solution:** Whenever four green(3) arm cells surround an empty center in the four cardinal directions, fill that center with yellow(4). Leave incomplete patterns alone.

**Program solution (Python reference):**
```python
def solve_easy_09_fill_plus_centers(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                continue
            vals = []
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    vals.append(g[nr][nc])
                else:
                    vals.append(None)
            if vals == [3,3,3,3]:
                out[r][c] = 4
    return out
```

**Train 1 input**
```text
0 0 0 3 0 0 0 0 0
0 0 3 0 3 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 3 0 0 0 3 0 3 0
0 0 3 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 3 0 0 0 0 0
0 0 3 4 3 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 3 0 0 0 3 4 3 0
0 0 3 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 3 0 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 0 0
```

**Train 2 output**
```text
0 3 0 0 0 0 0 0 0 0
3 4 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 4 3 0
0 0 0 0 0 0 0 3 0 0
0 3 0 0 0 0 0 0 0 0
3 4 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 4 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 4 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 3 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 3 0 0
3 0 3 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 4 3
0 0 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 4 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 3 0 0
3 4 3 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0
```

---

## Fill the Frame by the Singleton Key (`easy_10_fill_single_frame_by_key`)

**Difficulty:** easy

**Skills:** frame detection, singleton key extraction, interior fill

**Scaffold notes:**
- There is exactly one hollow frame.
- There is exactly one non-cyan key cell.
- Keep the frame and change only the inside.

**Written solution:** Find the hollow cyan(8) rectangular frame and fill its interior with the color of the lone non-cyan singleton elsewhere in the grid.

**Program solution (Python reference):**
```python
def solve_easy_10_fill_single_frame_by_key(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    counts = Counter(v for row in g for v in row if v != 0)
    key = None
    for color, count in counts.items():
        if color != 8 and count == 1:
            key = color
            break
    assert key is not None
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 8]
    r1, c1, r2, c2 = bbox(cells)
    for r in range(r1+1, r2):
        for c in range(c1+1, c2):
            out[r][c] = key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 8 0 0 0 8 0 0 0
5 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 8 5 5 5 8 0 0 0
5 0 8 5 5 5 8 0 0 0
0 0 8 5 5 5 8 0 0 0
0 0 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 0
0 8 0 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 0 8 0
0 8 0 0 0 0 0 0 0 0 8 0
0 8 8 8 8 8 8 8 8 8 8 7
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 8 8 0
0 8 7 7 7 7 7 7 7 7 8 0
0 8 7 7 7 7 7 7 7 7 8 0
0 8 7 7 7 7 7 7 7 7 8 0
0 8 7 7 7 7 7 7 7 7 8 0
0 8 7 7 7 7 7 7 7 7 8 0
0 8 8 8 8 8 8 8 8 8 8 7
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0
0 8 0 0 0 0 8 0 0 0 0
0 8 0 0 0 0 8 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0
0 8 6 6 6 6 8 0 0 0 0
0 8 6 6 6 6 8 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 0 0 0 0 0 0 0 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 8 5 5 5 5 5 5 5 8 0
0 0 8 5 5 5 5 5 5 5 8 0
0 0 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
```

---

## Bridge Single Horizontal Gaps (`easy_11_bridge_single_horizontal_gaps`)

**Difficulty:** easy

**Skills:** local pattern completion, horizontal scan, gap filling

**Scaffold notes:**
- Scan rows, not columns.
- You only need a length-3 window.
- The output changes only the middle blank cell.

**Written solution:** Whenever a row contains the pattern red(2), blank, red(2), fill the single blank gap between them with orange(7). Leave longer gaps unchanged.

**Program solution (Python reference):**
```python
def solve_easy_11_bridge_single_horizontal_gaps(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c] == 2 and g[r][c+1] == 0 and g[r][c+2] == 2:
                out[r][c+1] = 7
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 2 0 2 0
2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 0 2 7 2 7 2 7 2 0
2 0 0 0 0 0 0 0 0 0 0
0 0 2 7 2 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 7 2 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 2 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 2 2 0 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0
2 0 0 2 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 7 2 0
0 2 7 2 0 0 0 0 0 0
0 0 0 0 0 2 2 7 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 7 2 0 0
2 0 0 2 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 2 0 2 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 2 0 2
2 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 2 7 2 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 7 2 7 2
2 7 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 7 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 7 2 0 0 2 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 2 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 2 0 0
0 0 2 0 2 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
2 7 2 0 0 0 2 7 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 2 7 2 0 0
0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 2 0 0
0 0 2 7 2 0 0 0 0 0 0 0
```

---

## Diagonal Shadow Down-Right (`easy_12_diagonal_shadow_down_right`)

**Difficulty:** easy

**Skills:** local offset, copy by displacement, collision check

**Scaffold notes:**
- Each source cell contributes at most one shadow.
- The shadow is always at offset (+1,+1).
- Do not overwrite cells that are already occupied in the input.

**Written solution:** For every green(3) cell, place a gray(5) shadow one step down-right when that destination is empty. Keep the original green cells unchanged.

**Program solution (Python reference):**
```python
def solve_easy_12_diagonal_shadow_down_right(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 3:
                nr, nc = r + 1, c + 1
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0:
                    out[nr][nc] = 5
    return out
```

**Train 1 input**
```text
3 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 3 3 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
3 3 0 3 3 0 0 0 0 0
0 2 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 0 0 0 0 0 0 0 0 0
3 5 0 0 0 0 0 3 3 0
0 2 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
3 3 0 3 3 0 0 0 0 0
0 2 5 0 5 5 0 3 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 2
```

**Train 2 output**
```text
3 3 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 5 2
```

**Train 3 input**
```text
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 2 0
```

**Train 3 output**
```text
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 0 0 5 0 5 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 5 0
0 0 0 0 0 0 0 0 2 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 0 3 0 0
0 0 0 0 0 3 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 3 0 0
0 0 0 0 0 3 0 0 3 5 0
0 0 0 0 0 3 2 0 0 5 0
0 0 0 0 0 0 5 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## Keep Only the Leftmost Component (`easy_13_keep_leftmost_component`)

**Difficulty:** easy

**Skills:** connected components, left-to-right ordering, selection

**Scaffold notes:**
- Treat touching red cells as a component.
- Compare components by their leftmost column.
- Only one component survives in the output.

**Written solution:** Among all red(2) connected components, keep only the leftmost one and recolor it to cyan(8). Erase the rest to background.

**Program solution (Python reference):**
```python
def solve_easy_13_keep_leftmost_component(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g, {2})
    def keyfn(comp):
        r1, c1, _, _ = bbox(comp['cells'])
        return (c1, r1)
    best = min(comps, key=keyfn)
    for r, c in best['cells']:
        out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 2 0 0 0
0 0 2 0 0 0 0 0 2 2 0 0
0 2 2 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
0 2 2 0 0 0 0 2 2 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 2 2 0 0 0
0 0 0 0 2 2 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Mark Vertical Run Endpoints (`easy_14_mark_vertical_run_endpoints`)

**Difficulty:** easy

**Skills:** run detection, endpoint marking, same-size recolor

**Scaffold notes:**
- Work one column at a time.
- Short runs of length 1 or 2 do not change.
- Only the endpoints change color.

**Written solution:** For each vertical run of magenta(6) cells of length at least 3, recolor just the top and bottom endpoint cells to blue(1). Leave the interior magenta.

**Program solution (Python reference):**
```python
def solve_easy_14_mark_vertical_run_endpoints(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for c in range(w):
        r = 0
        while r < h:
            if g[r][c] != 6:
                r += 1
                continue
            s = r
            while r < h and g[r][c] == 6:
                r += 1
            if r - s >= 3:
                out[s][c] = 1
                out[r-1][c] = 1
    return out
```

**Train 1 input**
```text
0 0 0 0 6 0 0 6 0 0
0 0 0 0 6 0 0 6 0 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 1 0 0 6 0 0
0 0 0 0 6 0 0 6 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0
6 0 6 0 0 0 0 0 0 0
1 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 6 0 0 0 0 6 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 6 0 0 6 0 0 0 6
0 0 0 6 0 0 6 0 0 0 6
0 0 0 6 0 0 6 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 6 0 0 0 0 6 0
0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 1 0 0 6 0 0 0 1
0 0 0 6 0 0 6 0 0 0 6
0 0 0 1 0 0 1 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 6 0
6 0 0 0 6 0 0 0 6 0
6 0 0 0 6 0 0 0 6 0
0 0 0 0 6 0 6 0 6 0
0 0 0 0 6 0 6 0 6 0
0 0 0 0 6 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 1 0
6 0 0 0 1 0 0 0 6 0
6 0 0 0 6 0 0 0 6 0
0 0 0 0 6 0 1 0 6 0
0 0 0 0 6 0 6 0 1 0
0 0 0 0 1 0 6 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 6 0 6 0 0
0 0 0 6 0 6 0 6 0 6
6 0 0 6 0 0 0 6 0 6
6 0 0 6 0 0 0 6 0 6
0 0 0 6 0 0 0 6 0 6
0 0 0 6 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 6 0 1 0 0
0 0 0 1 0 6 0 6 0 1
6 0 0 6 0 0 0 6 0 6
6 0 0 6 0 0 0 6 0 6
0 0 0 6 0 0 0 1 0 6
0 0 0 1 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

---

## Complete Rectangle Borders from Diagonal Corners (`medium_08_complete_rectangle_borders_from_diagonal_corners`)

**Difficulty:** medium

**Skills:** geometry from corners, rectangle border drawing, multi-object handling

**Scaffold notes:**
- The two same-colored cells are opposite corners, not adjacent points.
- Recover the rectangle's row span and column span first.
- Then draw only the border, not the filled interior.

**Written solution:** Each color appears as exactly two diagonal corner cells of an axis-aligned rectangle. Draw the full rectangle border for every such colored pair.

**Program solution (Python reference):**
```python
def solve_medium_08_complete_rectangle_borders_from_diagonal_corners(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    colors = sorted({v for row in g for v in row if v != 0})
    for color in colors:
        cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == color]
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 == r2 or c1 == c2:
            continue
        ra, rb = sorted((r1,r2))
        ca, cb = sorted((c1,c2))
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
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 4 0 0 4 0 0
0 0 0 0 0 0 4 0 0 4 0 0
0 0 0 0 0 0 4 0 0 4 0 0
0 2 2 2 0 0 4 4 4 4 0 0
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 9 9 9 9 9 0 0 0
0 0 0 9 0 0 0 9 0 0 0
0 0 0 9 0 0 0 9 0 0 0
0 0 0 9 0 0 0 9 0 0 0
0 0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 6 0 0 6
0 0 0 0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 3 3 3 3 3 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0 0 0
1 0 0 0 1 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0
```

---

## Fill Each Component Bounding Box (`medium_09_fill_component_bounding_boxes`)

**Difficulty:** medium

**Skills:** connected components, bounding boxes, object expansion

**Scaffold notes:**
- Detect each component separately.
- Convert each component to its minimum enclosing axis-aligned rectangle.
- The output is the union of those filled rectangles.

**Written solution:** For every orange(4) component, compute its bounding box and fill that entire rectangle with orange(4).

**Program solution (Python reference):**
```python
def solve_medium_09_fill_component_bounding_boxes(g: Grid) -> Grid:
    out = clone(g)
    comps = components_by_color(g, {4})
    for comp in comps:
        r1, c1, r2, c2 = bbox(comp['cells'])
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                out[r][c] = 4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 4 4 0 0 0 0 0 0
0 4 4 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 4 4 4 0 0 0 0 0
0 4 4 0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Recolor Objects by the Key Above (`medium_10_recolor_objects_by_above_key`)

**Difficulty:** medium

**Skills:** object-marker association, bbox anchoring, recoloring

**Scaffold notes:**
- Find the object's top-left bbox corner.
- Read the color in the cell just above that corner.
- Apply that color to the whole object.

**Written solution:** Each green(3) object has a colored singleton sitting directly above its bounding box top-left corner. Recolor the entire object to that key color.

**Program solution (Python reference):**
```python
def solve_medium_10_recolor_objects_by_above_key(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    comps = components_by_color(g, {3})
    for comp in comps:
        r1, c1, r2, c2 = bbox(comp['cells'])
        kr, kc = r1 - 1, c1
        assert 0 <= kr < h and 0 <= kc < w
        key = g[kr][kc]
        assert key not in (0, 3)
        for r, c in comp['cells']:
            out[r][c] = key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 4 0 0 0 0
0 8 0 0 0 3 3 0 0 0
0 3 3 0 0 3 3 0 0 0
0 0 3 3 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 4 0 0 0 0
0 8 0 0 0 4 4 0 0 0
0 8 8 0 0 4 4 0 0 0
0 0 8 8 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 3
```

**Train 2 output**
```text
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
4 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 0 3 3 0 0 0
0 3 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
4 0 0 0 0 0 0 5 0 0 0
0 4 0 0 0 0 5 5 0 0 0
0 4 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 7 0 0 0
0 3 3 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 7 0 0 0
0 8 8 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 7 7 0 0
```

---

## Keep Components Matching the Template Shape (`medium_11_keep_shape_matching_template`)

**Difficulty:** medium

**Skills:** shape normalization, translation-invariant matching, selection

**Scaffold notes:**
- Ignore absolute position when comparing shapes.
- Do not rotate or reflect anything.
- Only exact translation matches survive.

**Written solution:** Use the lone blue(1) component as a template. Keep only the green(3) components with exactly the same translated shape, and recolor them to cyan(8).

**Program solution (Python reference):**
```python
def solve_medium_11_keep_shape_matching_template(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            for r, c in comp['cells']:
                out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 3 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 8 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
1 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 3 0 0 0 0 0 0
1 1 1 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Reflect Left Objects Across the Center Axis (`medium_12_reflect_left_objects_across_center_axis`)

**Difficulty:** medium

**Skills:** global axis detection, reflection, copy with recolor

**Scaffold notes:**
- The axis is the central column of the whole grid.
- Only left-side red cells generate reflected copies.
- The reflected copies use a new color.

**Written solution:** Treat the grid's middle column as the reflection axis. For every red(2) cell on the left side, add its mirrored counterpart on the right side in orange(7), while keeping the original red cells.

**Program solution (Python reference):**
```python
def solve_medium_12_reflect_left_objects_across_center_axis(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    axis = w // 2
    for r in range(h):
        for c in range(axis):
            if g[r][c] == 2:
                mc = 2 * axis - c
                if 0 <= mc < w:
                    out[r][mc] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 7 7
0 2 2 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 7 7 0
0 0 2 2 0 0 0 7 7 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 0 0 0 0 0 0 0 0 0 7
2 2 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 7
2 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 7 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 7 7 0
0 0 2 2 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 7 0 0
2 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 7 0
```

---

## Fill Rectangles from Diagonal Corners (`medium_13_fill_rectangles_from_diagonal_corners`)

**Difficulty:** medium

**Skills:** geometry from corners, rectangle fill, multi-object handling

**Scaffold notes:**
- Recover the row and column span from each diagonal pair.
- Unlike the border version, every cell inside the rectangle changes.
- Process each color separately.

**Written solution:** Each colored pair marks opposite corners of an axis-aligned rectangle. Fill the entire rectangle area in that same color.

**Program solution (Python reference):**
```python
def solve_medium_13_fill_rectangles_from_diagonal_corners(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    colors = sorted({v for row in g for v in row if v != 0})
    for color in colors:
        cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == color]
        if len(cells) != 2:
            continue
        (r1,c1),(r2,c2) = cells
        if r1 == r2 or c1 == c2:
            continue
        ra, rb = sorted((r1,r2))
        ca, cb = sorted((c1,c2))
        for r in range(ra, rb+1):
            for c in range(ca, cb+1):
                out[r][c] = color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0
0 0 9 9 9 0 1 1 1 1 1
0 0 9 9 9 0 1 1 1 1 1
0 0 9 9 9 0 1 1 1 1 1
0 0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0
0 1 1 1 1 1 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 0 0 0
0 0 0 0 0 7 7 7 7 0 0 0
0 0 0 0 0 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
8 8 8 0 1 1 1 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
8 8 8 0 0 0 0 0 0 0 0
```

---

## Select Components Touching the Main Diagonal (`medium_14_select_diagonal_touching_components`)

**Difficulty:** medium

**Skills:** connected components, global diagonal relation, selection

**Scaffold notes:**
- First find connected components.
- Then test whether any cell of the component lies on the main diagonal.
- Only diagonal-touching components remain.

**Written solution:** Among all magenta(6) components, keep only those that touch the main diagonal r=c, and recolor them to red(2). Remove the others.

**Program solution (Python reference):**
```python
def solve_medium_14_select_diagonal_touching_components(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w
    out = zeros(h, w)
    for comp in components_by_color(g, {6}):
        if any(r == c for r, c in comp['cells']):
            for r, c in comp['cells']:
                out[r][c] = 2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 6 6 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0
6 0 0 0 6 6 0 0 0
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 6 6 0 0 0
```

**Train 2 output**
```text
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0
0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 6
0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 6 0
0 0 0 0 6 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

---

## Rotate the Template by the Control Color (`hard_08_rotate_template_by_control_and_stamp`)

**Difficulty:** hard

**Skills:** template extraction, control-color mapping, rotation, stamping

**Scaffold notes:**
- Separate the template, the control singleton, and the target marker.
- Normalize the template before rotating it.
- Use the target marker as the top-left anchor of the rotated bounding box.

**Written solution:** Extract the lone green(2) template shape. Rotate it according to the singleton control color (blue(1)=0°, green(3)=90° clockwise, yellow(4)=180°, magenta(6)=270°), then stamp the rotated copy at the cyan(8) target marker in gray(7). Output only the stamped result.

**Program solution (Python reference):**
```python
def solve_hard_08_rotate_template_by_control_and_stamp(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template = components_by_color(g, {2})
    assert len(template) == 1
    template_offsets = norm(template[0]['cells'])
    counts = Counter(v for row in g for v in row if v != 0)
    control_color = None
    for color, count in counts.items():
        if color in (1, 3, 4, 6) and count == 1:
            control_color = color
            break
    assert control_color is not None
    rotation_map = {1: 0, 3: 1, 4: 2, 6: 3}
    k = rotation_map[control_color]
    target = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 8]
    assert len(target) == 1
    tr, tc = target[0]
    rot = rotate_offsets(template_offsets, k)
    for dr, dc in rot:
        out[tr + dr][tc + dc] = 7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 7 7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 7 7
```

**Test input**
```text
0 0 2 2 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0 7
```

---

## Scale the Second-Smallest Component 2x (`hard_09_scale_second_smallest_component_2x`)

**Difficulty:** hard

**Skills:** component ranking by area, shape scaling, selection

**Scaffold notes:**
- Rank components by size, not position.
- Take the second item in that sorted order.
- Scaling doubles each cell into a 2x2 block.

**Written solution:** Among the green(3) components, select the second-smallest by area and scale its shape by a factor of 2, anchored at its original top-left bounding-box corner. Recolor the scaled result to cyan(8) and erase everything else.

**Program solution (Python reference):**
```python
def solve_hard_09_scale_second_smallest_component_2x(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g, {3})
    assert len(comps) >= 2
    comps = sorted(comps, key=lambda comp: (len(comp['cells']), bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    target = comps[1]
    r1, c1, _, _ = bbox(target['cells'])
    scaled = scale_offsets(norm(target['cells']), 2)
    for dr, dc in scaled:
        out[r1 + dr][c1 + dc] = 8
    return out
```

**Train 1 input**
```text
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
3 3 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
3 3 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
```

---

## Palette-Recolor Components Left to Right (`hard_10_palette_recolor_components_left_to_right`)

**Difficulty:** hard

**Skills:** palette extraction, ordering by position, component recoloring

**Scaffold notes:**
- The palette is not part of the objects below.
- Component order is determined by horizontal position.
- Assign the first palette color to the leftmost component, and so on.

**Written solution:** Read the palette colors from the top row singleton cells, in left-to-right order. Then sort the green(2) components left-to-right and recolor them with the corresponding palette colors.

**Program solution (Python reference):**
```python
def solve_hard_10_palette_recolor_components_left_to_right(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    palette = [g[0][c] for c in range(w) if g[0][c] not in (0, 2)]
    assert len(palette) >= 3
    comps = components_by_color(g, {2})
    comps = sorted(comps, key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    for comp, color in zip(comps, palette):
        for r, c in comp['cells']:
            out[r][c] = color
    return out
```

**Train 1 input**
```text
0 9 0 0 0 0 5 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 2 0 0
0 0 0 2 2 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 9 0 0 0 0 5 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 8 0 0
0 0 0 9 9 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 4 0 0 5 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
2 0 0 0 0 0 0 2 0 0 0 0
2 0 0 0 0 0 0 2 2 2 0 0
2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 0 0 5 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
4 0 0 0 0 0 0 5 0 0 0 0
4 0 0 0 0 0 0 5 5 5 0 0
4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 1 4 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0
2 0 0 0 0 0 0 0 0 2 2 2
2 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 1 4 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 9 0 0
0 0 0 0 0 0 0 0 0 9 0 0
1 0 0 0 0 0 0 0 0 9 9 9
1 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 7 6 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0
0 0 0 2 2 2 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 7 6 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 6 0 0
0 0 0 7 7 7 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Intersection of Two Frame Interiors (`hard_11_intersection_of_two_frame_interiors`)

**Difficulty:** hard

**Skills:** frame detection, bbox interiors, set intersection

**Scaffold notes:**
- Ignore the frame borders themselves.
- Compute the strict interior of each frame from its bounding box.
- The answer is the intersection of those two interior regions.

**Written solution:** Take the interiors of the two hollow rectangular frames and color only their overlapping cells in orange(7). Output just that overlap region on a blank background.

**Program solution (Python reference):**
```python
def solve_hard_11_intersection_of_two_frame_interiors(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps = components_by_color(g)
    frames = [comp for comp in comps if len(comp['cells']) >= 8]
    assert len(frames) >= 2
    # choose first two colors by sorted color order for determinism
    frames = sorted(frames, key=lambda comp: comp['color'])[:2]
    interiors = []
    for comp in frames:
        r1, c1, r2, c2 = bbox(comp['cells'])
        inside = {(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)}
        interiors.append(inside)
    for r, c in sorted(interiors[0] & interiors[1]):
        out[r][c] = 7
    return out
```

**Train 1 input**
```text
0 2 2 2 2 2 2 2 2 0 0 0 0
0 2 0 0 3 3 3 3 3 3 0 0 0
0 2 0 0 3 0 0 0 2 3 0 0 0
0 2 0 0 3 0 0 0 2 3 0 0 0
0 2 0 0 3 0 0 0 2 3 0 0 0
0 2 0 0 3 0 0 0 2 3 0 0 0
0 2 0 0 3 3 3 3 3 3 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 0 3 3 3 3 3 0 0 0 0
0 0 2 0 3 0 0 2 3 0 0 0 0
0 0 2 0 3 0 0 2 3 0 0 0 0
0 0 2 0 3 0 0 2 3 0 0 0 0
0 0 2 0 3 0 0 2 3 0 0 0 0
0 0 2 2 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 2 3 3 3 3 3 3 3 2 2 0 0
2 0 3 0 0 0 0 0 3 0 2 0 0
2 0 3 0 0 0 0 0 3 0 2 0 0
2 0 3 0 0 0 0 0 3 0 2 0 0
2 0 3 0 0 0 0 0 3 0 2 0 0
2 0 3 3 3 3 3 3 3 0 2 0 0
2 0 0 0 0 0 0 0 0 0 2 0 0
2 2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 2 2 2 2 2 2 2 2 0 0 0 0
0 2 0 0 0 0 0 0 2 0 0 0 0
0 2 0 0 3 3 3 3 2 0 0 0 0
0 2 0 0 3 0 0 3 2 0 0 0 0
0 2 0 0 3 0 0 3 2 0 0 0 0
0 2 0 0 3 0 0 3 2 0 0 0 0
0 2 0 0 3 3 3 3 2 0 0 0 0
0 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Make Matching Shapes Symmetric (`hard_12_make_matching_shapes_symmetric`)

**Difficulty:** hard

**Skills:** template matching, per-object reflection, shape completion

**Scaffold notes:**
- First decide which components match the template exactly up to translation.
- Then reflect each matching component inside its own bounding box.
- The output keeps the union of original and reflected cells.

**Written solution:** Use the lone blue(1) component as a template. For every green(3) component with the same translated shape, reflect it across its own vertical bounding-box axis, union the reflection with the original, and recolor the result to cyan(8). Remove all non-matching components.

**Program solution (Python reference):**
```python
def solve_hard_12_make_matching_shapes_symmetric(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            r1, c1, r2, c2 = bbox(comp['cells'])
            pts = {(r, c) for r, c in comp['cells']}
            for r, c in list(pts):
                mc = c1 + c2 - c
                pts.add((r, mc))
            for r, c in pts:
                out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 0 0 3 3 3 0 0
0 0 0 0 3 3 0 0 0 0 3 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 1 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
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
0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Stamp Rotated Copies at Multiple Markers (`hard_13_multi_marker_rotated_stamping`)

**Difficulty:** hard

**Skills:** template extraction, multi-target stamping, rotation control

**Scaffold notes:**
- All markers use the same template shape.
- Each marker carries its own rotation instruction.
- The stamped copies may differ only by rotation, not by scale.

**Written solution:** Extract the green(2) template shape. Every colored marker (blue(1), green(3), yellow(4), magenta(6)) tells you to stamp a rotated copy of that template at that marker: 0°, 90°, 180°, or 270° clockwise respectively. Stamp all copies in cyan(8) on a blank background.

**Program solution (Python reference):**
```python
def solve_hard_13_multi_marker_rotated_stamping(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    template = components_by_color(g, {2})
    assert len(template) == 1
    template_offsets = norm(template[0]['cells'])
    rotation_map = {1: 0, 3: 1, 4: 2, 6: 3}
    for r in range(h):
        for c in range(w):
            if g[r][c] in rotation_map:
                rot = rotate_offsets(template_offsets, rotation_map[g[r][c]])
                for dr, dc in rot:
                    out[r + dr][c + dc] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 4 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8
8 8 0 0 0 0 0 0 0 0 8 8 0
0 8 8 0 0 0 0 0 0 0 8 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 6 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 8 8 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 4 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 8 0
0 8 8 8 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Shape Match with Majority-Key Recolor (`hard_14_select_shape_match_and_recolor_by_majority_singleton`)

**Difficulty:** hard

**Skills:** template matching, color aggregation, selection and recolor

**Scaffold notes:**
- One subproblem is shape matching; the other is finding the majority key color.
- Only singleton key cells count toward the majority vote.
- After you know the majority color, apply it to all matching candidates.

**Written solution:** Use the lone blue(1) component as a shape template. Among the green(3) candidates, keep the ones with the same translated shape, and recolor them to the majority color among the non-template singleton key cells.

**Program solution (Python reference):**
```python
def solve_hard_14_select_shape_match_and_recolor_by_majority_singleton(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    comps1 = components_by_color(g, {1})
    assert len(comps1) == 1
    target = norm(comps1[0]['cells'])
    counts = Counter()
    for color, count in Counter(v for row in g for v in row if v != 0).items():
        if color not in (1, 3) and count >= 1:
            counts[color] += count
    # majority by total singleton count
    majority_color = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
    for comp in components_by_color(g, {3}):
        if norm(comp['cells']) == target:
            for r, c in comp['cells']:
                out[r][c] = majority_color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0 5
1 0 0 0 0 0 0 0 0 0 2 0 0
1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 2 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 5 0 0
0 0 1 0 0 0 0 3 0 0 0 0
0 0 1 1 1 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 1 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 7 0 0 0 0 7 0
0 0 0 1 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 3 0 0 0 0 0 3 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 7 0 0 0 0 0 7 0
0 0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 6 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---
