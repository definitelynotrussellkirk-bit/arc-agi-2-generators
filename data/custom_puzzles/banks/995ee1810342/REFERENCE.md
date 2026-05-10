# ARC Puzzle Bank — Set 12

This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set12.json` — machine-readable task data
- `arc_puzzle_bank_21_set12_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set12_validation.txt` — validation log

## Easy (7)

### easy_l01 — Keep only the endcaps of each vertical run

**Written rule:** For each contiguous vertical run of a nonzero color, keep only its topmost and bottommost cells; erase the interior of the run.

**Program function:** `solve_easy_l01`

**Primitives:** vertical_run_endcaps

```python
def solve_easy_l01(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r0, r1, c, col in run_vertical_segments(g):
        out[r0][c] = col
        out[r1][c] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 3 0 0
0 2 0 0 3 0 0
0 2 0 0 3 0 0
0 2 0 0 3 0 0
0 0 0 0 3 0 0
0 0 4 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 3 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 3 0 0
0 0 4 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
6 0 0 7 0 0 0 0
6 0 0 0 0 0 0 0
6 0 0 0 0 0 8 0
6 0 0 0 0 0 8 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
6 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
6 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 9 0
0 0 0 0 2 0 0 9 0
0 0 0 0 2 0 0 9 0
0 0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
```

**Train 3 output**
```text
0 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 9 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
```

**Test input**
```text
0 0 0 2 0 0 0 0 0
4 0 0 2 0 0 0 0 0
4 0 0 2 0 0 0 0 0
4 0 0 0 0 0 7 0 0
4 0 0 0 0 0 7 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 2 0 0 0 0 0
4 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0 0
4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### easy_l02 — Erase globally unique colors

**Written rule:** Count each nonzero color across the whole grid. Any color that appears exactly once disappears; colors that appear two or more times stay where they are.

**Program function:** `solve_easy_l02`

**Primitives:** global_color_count

```python
def solve_easy_l02(g: Grid) -> Grid:
    cnt = count_colors(g)
    return [[v if v != 0 and cnt[v] > 1 else 0 for v in row] for row in g]
```

**Train 1 input**
```text
0 2 0 0 3 0 0
0 2 0 4 0 0 0
0 0 0 4 0 5 0
6 0 0 0 0 5 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0 0
0 2 0 4 0 0 0
0 0 0 4 0 5 0
0 0 0 0 0 5 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
1 0 0 2 2 0
0 0 3 0 0 0
0 4 0 4 0 0
0 0 0 0 5 0
0 0 0 0 5 0
6 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 2 2 0
0 0 0 0 0 0
0 4 0 4 0 0
0 0 0 0 5 0
0 0 0 0 5 0
0 0 0 0 0 0
```

**Train 3 input**
```text
0 7 0 0 0 8 0 0
0 7 0 9 0 0 0 0
0 0 0 9 0 0 0 0
1 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 7 0 0 0 0 0 0
0 7 0 9 0 0 0 0
0 0 0 9 0 0 0 0
0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 1 0 0 0 2 0 0
0 1 0 3 0 0 0 4
0 0 0 3 0 0 0 0
5 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 1 0 0 0 0 0 0
0 1 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0
```

### easy_l03 — Turn solid rectangles into checkerboards

**Written rule:** Every solid monochrome rectangle becomes a checkerboard on its own bounding box, keeping the rectangle color on alternating cells and turning the other cells black.

**Program function:** `solve_easy_l03`

**Primitives:** solid_rectangle_detect, checkerize_bbox

```python
def solve_easy_l03(g: Grid) -> Grid:
    out = blank(*dims(g))
    for comp in solid_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        col = comp["color"]
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if ((r - r0) + (c - c0)) % 2 == 0:
                    out[r][c] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0
0 2 2 2 2 0 0 0 0
0 2 2 2 2 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 2 0 2 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 4 4 4 4 0 0 0
4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0
0 0 0 7 7 7 0 0
0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 0 4 0 4 0 0 0
0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 7 0 0
0 0 0 0 7 0 0 0
0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 8 8 0
0 0 6 6 6 0 0 8 8 0
0 0 6 6 6 0 0 8 8 0
0 0 6 6 6 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 8 0 0
0 0 6 0 6 0 0 0 8 0
0 0 0 6 0 0 0 8 0 0
0 0 6 0 6 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 1 1 0
0 9 9 9 9 9 0 1 1 0
0 9 9 9 9 9 0 1 1 0
0 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 1 0
0 9 0 9 0 9 0 1 0 0
0 0 9 0 9 0 0 0 1 0
0 9 0 9 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### easy_l04 — Turn odd rectangles into pluses

**Written rule:** Each solid odd-by-odd rectangle is replaced by the plus made from its center row and center column, using the same color.

**Program function:** `solve_easy_l04`

**Primitives:** solid_rectangle_detect, bbox_center_cross

```python
def solve_easy_l04(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for comp in solid_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        if (r1 - r0) % 2 == 0 and (c1 - c0) % 2 == 0:
            rm = (r0 + r1) // 2
            cm = (c0 + c1) // 2
            for c in range(c0, c1 + 1):
                out[rm][c] = comp["color"]
            for r in range(r0, r1 + 1):
                out[r][cm] = comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0
0 2 2 2 2 2 0 0 0
0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 3 3 3
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 3 0
```

**Train 2 input**
```text
4 4 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
4 4 4 0 0 7 7 7 7 7 0
4 4 4 0 0 7 7 7 7 7 0
0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 7 0 0 0
0 4 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 8 8 0
0 6 6 6 0 0 8 8 8 0
0 6 6 6 0 0 8 8 8 0
0 6 6 6 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 6 0 0 0 8 8 8 0
0 6 6 6 0 0 0 8 0 0
0 0 6 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 9 9 9 9 9 0 1 1 1
0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0
```

### easy_l05 — Fill the center of each hollow odd frame

**Written rule:** Keep every hollow odd-by-odd frame and add a single cell of the same color at its exact center.

**Program function:** `solve_easy_l05`

**Primitives:** frame_detect, frame_center_fill

```python
def solve_easy_l05(g: Grid) -> Grid:
    out = copy_grid(g)
    for comp in frame_rectangles(g):
        r0, c0, r1, c1 = bbox(comp["cells"])
        if (r1 - r0) % 2 == 0 and (c1 - c0) % 2 == 0:
            out[(r0 + r1) // 2][(c0 + c1) // 2] = comp["color"]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0
0 2 0 0 0 2 0 3 3 3 0
0 2 0 0 0 2 0 3 0 3 0
0 2 0 0 0 2 0 3 3 3 0
0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0
0 2 0 0 0 2 0 3 3 3 0
0 2 0 2 0 2 0 3 3 3 0
0 2 0 0 0 2 0 3 3 3 0
0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 4 4 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0
4 0 4 0 0 7 7 7 7 7 0
4 4 4 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0 0
4 0 4 0 0 7 7 7 7 7 0
4 4 4 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 7 0 7 0
0 0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 6 0 0 0 6 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 6 0 6 0 6 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 1 1 1
0 0 9 9 9 9 9 0 1 0 1
0 0 9 0 0 0 9 0 1 1 1
0 0 9 0 0 0 9 0 0 0 0
0 0 9 0 0 0 9 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 1 1 1
0 0 9 9 9 9 9 0 1 1 1
0 0 9 0 0 0 9 0 1 1 1
0 0 9 0 9 0 9 0 0 0 0
0 0 9 0 0 0 9 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### easy_l06 — Each plus becomes an X

**Written rule:** Every 5-cell plus shape is replaced by the 5-cell X shape centered at the same cell and colored the same way.

**Program function:** `solve_easy_l06`

**Primitives:** plus_detect, plus_to_x

```python
def solve_easy_l06(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            col = g[r][c]
            if col != 0 and g[r - 1][c] == col and g[r + 1][c] == col and g[r][c - 1] == col and g[r][c + 1] == col:
                for dr, dc in [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    out[r + dr][c + dc] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 0 2 0 3 0 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0
0 0 7 4 0 0 0 0
0 7 7 7 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
0 7 4 7 4 0 0 0
0 0 7 0 0 0 0 0
0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 8 0 0 0 6 6 6 0
0 8 8 8 0 0 0 6 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0
0 8 0 8 0 0 0 6 0 0
0 0 8 0 0 0 6 0 6 0
0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0
```

### easy_l07 — Each X becomes a plus

**Written rule:** Every 5-cell X shape is replaced by the 5-cell plus shape centered at the same cell and colored the same way.

**Program function:** `solve_easy_l07`

**Primitives:** x_detect, x_to_plus

```python
def solve_easy_l07(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            col = g[r][c]
            if col != 0 and g[r - 1][c - 1] == col and g[r - 1][c + 1] == col and g[r + 1][c - 1] == col and g[r + 1][c + 1] == col:
                for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                    out[r + dr][c + dc] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 0 2 0 3 0 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 3 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
0 7 4 7 4 0 0 0
0 0 7 0 0 0 0 0
0 7 0 7 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 4 4 4 0 0 0
0 0 7 4 0 0 0 0
0 7 7 7 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 6 0
0 8 0 8 0 0 0 6 0 0
0 0 8 0 0 0 6 0 6 0
0 8 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 8 0 0 0 6 6 6 0
0 8 8 8 0 0 0 6 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
```

## Medium (7)

### medium_l08 — Fill the room that contains each seed

**Written rule:** Gray(5) cells are walls. In each enclosed room, a colored seed expands to fill every black cell in that room, while the walls stay gray.

**Program function:** `solve_medium_l08`

**Primitives:** room_fill

```python
def solve_medium_l08(g: Grid) -> Grid:
    h, w = dims(g)
    out = copy_grid(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and v != 5:
                q = deque([(r, c)])
                seen = {(r, c)}
                while q:
                    rr, cc = q.popleft()
                    for dr, dc in DIR4:
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in seen:
                            if g[nr][nc] == 0 or (nr, nc) == (r, c):
                                seen.add((nr, nc))
                                q.append((nr, nc))
                for rr, cc in seen:
                    if g[rr][cc] == 0:
                        out[rr][cc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 5 5 5 5 0
0 5 2 0 5 0 0 5 0 0 5 0
0 5 0 0 5 0 0 5 3 0 5 0
0 5 5 5 5 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 5 5 5 5 0
0 5 2 2 5 0 0 5 3 3 5 0
0 5 2 2 5 0 0 5 3 3 5 0
0 5 5 5 5 0 0 5 3 3 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 0 5 0 5 5 5 5 0
0 5 4 5 0 5 0 0 5 0
0 5 0 5 0 5 0 7 5 0
0 5 0 5 0 5 5 5 5 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 4 5 0 5 5 5 5 0
0 5 4 5 0 5 7 7 5 0
0 5 4 5 0 5 7 7 5 0
0 5 4 5 0 5 5 5 5 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 0 0 0 5 0 0 5 8 0 5 0
0 5 0 6 0 5 0 0 5 0 0 5 0
0 5 0 0 0 5 0 0 5 5 5 5 0
0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 6 6 6 5 0 0 5 8 8 5 0
0 5 6 6 6 5 0 0 5 8 8 5 0
0 5 6 6 6 5 0 0 5 5 5 5 0
0 5 5 5 5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 9 0 5 0 0 5 5 5 5 5 0 0
0 5 0 0 5 0 0 5 0 0 0 5 0 0
0 5 0 0 5 0 0 5 0 1 0 5 0 0
0 5 0 0 5 0 0 5 0 0 0 5 0 0
0 5 5 5 5 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 9 9 5 0 0 5 5 5 5 5 0 0
0 5 9 9 5 0 0 5 1 1 1 5 0 0
0 5 9 9 5 0 0 5 1 1 1 5 0 0
0 5 9 9 5 0 0 5 1 1 1 5 0 0
0 5 5 5 5 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_l09 — Keep only the median-area object

**Written rule:** Find all connected objects and compare their areas. Keep only the object whose area is the median one; erase the smaller and larger objects.

**Program function:** `solve_medium_l09`

**Primitives:** component_area_rank, median_select

```python
def solve_medium_l09(g: Grid) -> Grid:
    comps = find_components(g)
    ranked = sorted((len(c["cells"]), i) for i, c in enumerate(comps))
    median_idx = ranked[len(ranked) // 2][1]
    keep = set(comps[median_idx]["cells"])
    return [[g[r][c] if (r, c) in keep else 0 for c in range(len(g[0]))] for r in range(len(g))]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 9 0 0 0 0 0
0 0 0 9 9 9 9 0 0 0 0 0
0 0 0 9 9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_l10 — Crop the object with exactly one hole

**Written rule:** Among all connected objects, select the one that encloses exactly one hole and output just that object cropped to its tight bounding box.

**Program function:** `solve_medium_l10`

**Primitives:** hole_count, crop_bbox

```python
def solve_medium_l10(g: Grid) -> Grid:
    for comp in find_components(g):
        if component_holes(g, comp) == 1:
            return crop_to_cells(g, comp["cells"])
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 3 3 3 0
0 2 2 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 3 3 3
3 0 0 0 3
3 0 0 0 3
3 3 3 3 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0
0 6 0 0 0 6 0 7 7 0
0 6 0 0 0 6 0 7 7 0
0 6 0 0 0 6 0 7 7 0
0 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 9 9 9 9 0 0 0
0 2 2 2 0 0 9 0 0 9 0 0 0
0 2 2 2 0 0 9 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0 9 0 0 0
0 0 0 0 0 0 9 9 9 9 0 4 4
0 0 0 0 0 0 0 0 0 0 0 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 9 9
9 0 0 9
9 0 0 9
9 0 0 9
9 9 9 9
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 0 3 0 0 0 3 0
0 0 0 0 0 0 0 3 3 3 3 3 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
3 3 3 3 3
3 0 0 0 3
3 0 0 0 3
3 0 0 0 3
3 3 3 3 3
```

### medium_l11 — Pack objects left-to-right by color

**Written rule:** Crop every object to its own bounding box, sort the cropped objects by color value from smallest to largest, then pack them left-to-right with one blank column between neighbors.

**Program function:** `solve_medium_l11`

**Primitives:** crop_bbox, pack_gallery, sort_by_color

```python
def solve_medium_l11(g: Grid) -> Grid:
    return pack_components_from_grid(g, find_components(g), key_fn=lambda c: c["color"])
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 3 3 3 0 0 0 0
0 7 0 0 0 0 3 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 3 3 0 5 5 0 0 7 0
0 3 0 0 0 5 5 0 7 0
0 0 0 0 0 0 0 0 7 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 8 8 0 0 0 2 0 0 0 0 0 0
0 0 8 8 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 0 0 6 6 6 0 8 8 0
2 0 0 0 6 0 0 0 8 8
2 2 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 4 4 0 0 1 0 0
0 0 0 0 0 0 0 0 4 4 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
1 0 0 4 4 0 0 9 9 9
1 0 0 0 4 4 0 0 9 0
1 1 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0 0
0 5 0 0 0 0 0 2 2 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 2 0 0 5 0 0 8 8 8
0 2 2 0 5 0 0 0 8 0
0 0 0 0 5 5 0 0 0 0
```

### medium_l12 — Recolor objects by prime vs composite area

**Written rule:** For each connected object, compute its area. Prime-area objects become red(2); composite-area objects become cyan(8). The shapes stay the same.

**Program function:** `solve_medium_l12`

**Primitives:** area_primality

```python
def solve_medium_l12(g: Grid) -> Grid:
    out = blank(*dims(g))
    for comp in find_components(g):
        col = 2 if is_prime(len(comp["cells"])) else 8
        for r, c in comp["cells"]:
            out[r][c] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 1 1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_l13 — Draw rectangle borders from matching corner markers

**Written rule:** Each color appears exactly twice, and the two cells of a color are opposite corners of a rectangle. Draw only that rectangle’s border in that color.

**Program function:** `solve_medium_l13`

**Primitives:** corner_pair_rect_border

```python
def solve_medium_l13(g: Grid) -> Grid:
    h, w = dims(g)
    out = blank(h, w)
    positions = defaultdict(list)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0:
                positions[v].append((r, c))
    for col, pts in positions.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            r0, r1b = sorted((r1, r2))
            c0, c1b = sorted((c1, c2))
            for r in range(r0, r1b + 1):
                out[r][c0] = col
                out[r][c1b] = col
            for c in range(c0, c1b + 1):
                out[r0][c] = col
                out[r1b][c] = col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 2 0 0 0 2 0 3 3 3
0 2 0 0 0 2 0 3 0 3
0 2 2 2 2 2 0 3 0 3
0 0 0 0 0 0 0 3 0 3
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
4 4 4 4 0 0 0 0 0 0 0
4 0 0 4 0 0 0 0 0 0 0
4 0 0 4 0 0 7 7 7 7 7
4 0 0 4 0 0 7 0 0 0 7
4 4 4 4 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 8 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 8 8
0 0 6 6 6 6 6 6 6 0 8 8
0 0 6 0 0 0 0 0 6 0 8 8
0 0 6 0 0 0 0 0 6 0 8 8
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 1
0 9 9 9 9 0 0 1 0 0 0 1
0 9 0 0 9 0 0 1 0 0 0 1
0 9 0 0 9 0 0 1 0 0 0 1
0 9 0 0 9 0 0 1 0 0 0 1
0 9 0 0 9 0 0 1 1 1 1 1
0 9 0 0 9 0 0 0 0 0 0 0
0 9 9 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_l14 — Stamp transformed templates at the markers

**Written rule:** The small template above the gray separator row is copied below. Marker color 1 means keep the template as-is, 2 means rotate 90°, 3 means rotate 180°, and 4 means rotate 270°; stamp the chosen transform centered on each marker.

**Program function:** `solve_medium_l14`

**Primitives:** extract_template, marker_transform_stamp

```python
def solve_medium_l14(g: Grid) -> Grid:
    template, markers, mh, mw = extract_template_and_markers(g)
    out = blank(mh, mw)
    for r, c, v in markers:
        tr = transform_by_marker(template, v)
        th, tw = dims(tr)
        r0 = r - th // 2
        c0 = c - tw // 2
        for i, row in enumerate(tr):
            for j, val in enumerate(row):
                if val != 0:
                    rr, cc = r0 + i, c0 + j
                    if 0 <= rr < mh and 0 <= cc < mw:
                        out[rr][cc] = val
    return out
```

**Train 1 input**
```text
0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 2 0 0 0 0 0 2 2 0 0
0 2 2 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 2 0 0 2 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 2 2 0 0 2 2 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0
```

**Train 3 input**
```text
0 2 0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 2 2 0 0
0 2 2 0 0 0 0 0 0 2 0 0
2 0 2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 2 0 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 2 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 2 0 2
0 0 0 0 0 0 0 2 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Hard (7)

### hard_l15 — Route one shortest path through ordered waypoints

**Written rule:** Walls are gray(5). Starting at 1, route a shortest path that visits 2, then 3, then 4, and finally reaches 6. Paint the traversed empty cells cyan(8).

**Program function:** `solve_hard_l15`

**Primitives:** ordered_waypoint_path

```python
def solve_hard_l15(g: Grid) -> Grid:
    path = shortest_path_with_waypoints(g, order_colors=[2, 3, 4], start_color=1, end_color=6, wall_colors={5})
    out = copy_grid(g)
    if path is None:
        return out
    for r, c in path:
        if out[r][c] == 0:
            out[r][c] = 8
    return out
```

**Train 1 input**
```text
1 0 0 5 0 0 0 0 0
5 5 0 5 0 5 5 5 0
0 0 0 0 0 0 0 5 0
0 5 5 5 5 5 0 5 0
0 0 2 0 0 0 0 0 0
0 5 5 5 0 5 5 5 0
0 0 0 3 0 0 4 0 6
```

**Train 1 output**
```text
1 8 8 5 0 0 0 0 0
5 5 8 5 0 5 5 5 0
8 8 8 0 0 0 0 5 0
8 5 5 5 5 5 0 5 0
8 8 2 8 8 0 0 0 0
0 5 5 5 8 5 5 5 0
0 0 0 3 8 8 4 8 6
```

**Train 2 input**
```text
1 0 0 0 5 0 0 0 0 0
5 5 5 0 5 0 5 5 5 0
2 0 0 0 0 0 0 0 5 0
0 0 5 5 5 5 5 0 5 0
0 0 0 0 3 0 0 0 0 0
0 5 5 5 5 5 0 5 5 0
0 0 0 0 0 4 0 0 0 6
```

**Train 2 output**
```text
1 8 8 8 5 0 0 0 0 0
5 5 5 8 5 0 5 5 5 0
2 8 8 8 0 0 0 0 5 0
8 0 5 5 5 5 5 0 5 0
8 8 8 8 3 8 8 0 0 0
0 5 5 5 5 5 8 5 5 0
0 0 0 0 0 4 8 8 8 6
```

**Train 3 input**
```text
1 0 5 0 0 0 0 0 0
0 0 5 0 5 5 5 5 0
0 2 0 0 0 0 0 5 0
0 5 5 5 5 5 0 5 0
0 0 0 0 3 0 0 0 0
0 5 5 0 5 5 5 5 0
0 0 0 0 0 4 0 0 6
```

**Train 3 output**
```text
1 0 5 0 0 0 0 0 0
8 0 5 0 5 5 5 5 0
8 2 0 0 0 0 0 5 0
8 5 5 5 5 5 0 5 0
8 8 8 8 3 0 0 0 0
0 5 5 8 5 5 5 5 0
0 0 0 8 8 4 8 8 6
```

**Test input**
```text
1 0 0 0 0 5 0 0 0 0
5 5 5 5 0 5 0 5 5 0
2 0 0 0 0 0 0 5 0 0
0 0 5 5 5 5 0 5 0 5
0 0 0 0 3 0 0 0 0 0
0 5 5 5 5 5 5 5 0 0
0 0 0 0 0 4 0 0 0 6
```

**Test output**
```text
1 8 8 8 8 5 0 0 0 0
5 5 5 5 8 5 0 5 5 0
2 8 8 8 8 0 0 5 0 0
8 0 5 5 5 5 0 5 0 5
8 8 8 8 3 8 8 8 8 0
0 5 5 5 5 5 5 5 8 0
0 0 0 0 0 4 8 8 8 6
```

### hard_l16 — Fill each region by nearest seed through walls

**Written rule:** Gray(5) cells are walls. Every empty cell is colored by the seed with the smallest geodesic distance through open space; ties stay black. Seeds and walls remain unchanged.

**Program function:** `solve_hard_l16`

**Primitives:** geodesic_voronoi

```python
def solve_hard_l16(g: Grid) -> Grid:
    return geodesic_voronoi(g, wall_colors={5})
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 5 5 5 5 5 0
0 5 0 0 0 5 0 5 0 0 0 5 0
0 5 0 0 0 5 0 5 0 0 0 5 0
0 5 0 2 0 5 0 5 0 3 0 5 0
0 5 0 0 0 5 0 5 0 0 0 5 0
0 5 0 0 0 5 0 5 0 0 0 5 0
0 5 5 5 5 5 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 5 5 5 5 5 0
0 5 2 2 2 5 0 5 3 3 3 5 0
0 5 2 2 2 5 0 5 3 3 3 5 0
0 5 2 2 2 5 0 5 3 3 3 5 0
0 5 2 2 2 5 0 5 3 3 3 5 0
0 5 2 2 2 5 0 5 3 3 3 5 0
0 5 5 5 5 5 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 5 5 5 5 5 0
0 5 0 0 5 0 5 0 0 0 5 0
0 5 4 0 5 0 5 0 5 0 5 0
0 5 0 0 5 0 5 0 5 0 5 0
0 5 0 0 5 0 5 0 5 0 5 0
0 5 0 0 5 0 5 0 5 7 5 0
0 5 0 0 5 0 5 0 5 0 5 0
0 5 5 5 5 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 5 5 5 5 5 0
0 5 4 4 5 0 5 7 7 7 5 0
0 5 4 4 5 0 5 7 5 7 5 0
0 5 4 4 5 0 5 7 5 7 5 0
0 5 4 4 5 0 5 7 5 7 5 0
0 5 4 4 5 0 5 7 5 7 5 0
0 5 4 4 5 0 5 7 5 7 5 0
0 5 5 5 5 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 5 0
0 5 6 0 0 5 0 0 5 1 0 0 5 0
0 5 0 0 0 5 0 0 5 0 0 0 5 0
0 5 0 0 0 5 0 0 5 0 0 0 5 0
0 5 0 0 8 5 0 0 5 0 0 3 5 0
0 5 5 5 5 5 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 5 0
0 5 6 6 6 5 0 0 5 1 1 1 5 0
0 5 6 6 8 5 0 0 5 1 1 3 5 0
0 5 6 8 8 5 0 0 5 1 3 3 5 0
0 5 8 8 8 5 0 0 5 3 3 3 5 0
0 5 5 5 5 5 0 0 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5 0
0 5 2 0 0 0 5 0 5 7 0 0 0 5 0
0 5 0 0 0 0 5 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 5 0 0 0 0 5 0
0 5 0 0 0 0 5 0 5 0 0 0 0 5 0
0 5 0 0 0 4 5 0 5 0 0 0 9 5 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5 0
0 5 2 2 2 2 5 0 5 7 7 7 7 5 0
0 5 2 2 2 0 5 0 5 7 7 7 0 5 0
0 5 2 2 0 4 5 0 5 7 7 0 9 5 0
0 5 2 0 4 4 5 0 5 7 0 9 9 5 0
0 5 0 4 4 4 5 0 5 0 9 9 9 5 0
0 5 4 4 4 4 5 0 5 9 9 9 9 5 0
0 5 5 5 5 5 5 0 5 5 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_l17 — Tile transformed templates inside colored frames

**Written rule:** The template above the gray separator row is repeated inside every hollow frame below. Frame color 1 uses the template as-is, 2 rotates it 90°, 3 rotates it 180°, and 4 rotates it 270° before tiling the frame interior periodically.

**Program function:** `solve_hard_l17`

**Primitives:** extract_template, frame_tiling, color_key_rotation

```python
def solve_hard_l17(g: Grid) -> Grid:
    template, lower, frames = extract_template_and_frames(g)
    out = copy_grid(lower)
    for comp in frames:
        t = transform_by_marker(template, comp["color"])
        out = tile_inside_frame(out, comp, t)
    return out
```

**Train 1 input**
```text
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 2 2 2 2 0 0
0 1 0 0 1 0 0 0 2 0 0 2 0 0
0 1 0 0 1 0 0 0 2 0 0 2 0 0
0 1 1 1 1 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 2 2 2 2 0 0
0 1 2 0 1 0 0 0 2 0 2 2 0 0
0 1 0 3 1 0 0 0 2 3 0 2 0 0
0 1 1 1 1 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
0 3 3 3 3 3 0 0 4 4 4 4 0
0 3 0 0 0 3 0 0 4 0 0 4 0
0 3 0 0 0 3 0 0 4 0 0 4 0
0 3 0 0 0 3 0 0 4 0 0 4 0
0 3 3 3 3 3 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 3 3 3 3 3 0 0 4 4 4 4 0
0 3 3 0 3 3 0 0 4 2 0 4 0
0 3 0 2 0 3 0 0 4 0 3 4 0
0 3 3 0 3 3 0 0 4 2 0 4 0
0 3 3 3 3 3 0 0 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 1 1 1 1 0
0 0 2 0 0 0 2 0 0 1 0 0 1 0
0 0 2 0 0 0 2 0 0 1 0 0 1 0
0 0 2 2 2 2 2 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 1 1 1 1 0
0 0 2 0 2 0 2 0 0 1 2 0 1 0
0 0 2 3 0 3 2 0 0 1 0 3 1 0
0 0 2 2 2 2 2 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5
0 4 4 4 4 0 0 3 3 3 3 3 0
0 4 0 0 4 0 0 3 0 0 0 3 0
0 4 0 0 4 0 0 3 0 0 0 3 0
0 4 0 0 4 0 0 3 0 0 0 3 0
0 4 4 4 4 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 4 4 4 4 0 0 3 3 3 3 3 0
0 4 2 0 4 0 0 3 3 0 3 3 0
0 4 0 3 4 0 0 3 0 2 0 3 0
0 4 2 0 4 0 0 3 3 0 3 3 0
0 4 4 4 4 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_l18 — Keep the cells occupied by exactly two normalized shapes

**Written rule:** Normalize the three separate objects to the top-left of their own bounding boxes and align them on one canvas. Output the cells covered by exactly two shapes in red(2), and the cells covered by all three in cyan(8).

**Program function:** `solve_hard_l18`

**Primitives:** normalize_shapes, two_of_three_overlay

```python
def solve_hard_l18(g: Grid) -> Grid:
    shapes = [(comp["color"], normalize_cells(comp["cells"])) for comp in find_components(g)]
    H = max((max(r for r, c in cells) + 1 for _, cells in shapes), default=1)
    W = max((max(c for r, c in cells) + 1 for _, cells in shapes), default=1)
    count = [[0] * W for _ in range(H)]
    for _, cells in shapes:
        for r, c in cells:
            count[r][c] += 1
    out = blank(H, W)
    for r in range(H):
        for c in range(W):
            if count[r][c] == 2:
                out[r][c] = 2
            elif count[r][c] == 3:
                out[r][c] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 3 3 0 0 4 4 0
0 2 0 0 0 0 0 3 0 0 0 0 4 4
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 2 0
0 2 0
0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 5 5 5 0 0 6 0 0 0 0 7 7 7 0
0 0 5 0 0 0 6 6 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 2 2
0 2 0
0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 9 9 0 0 0 1 0 0 0
0 0 8 8 0 0 0 0 9 9 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 2 0
0 2 2
0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 3 0 0 4 0 0 0
0 2 0 0 0 0 0 0 0 0 0 4 0 0 0
0 2 2 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 0 0
2 0 0
2 2 0
```

### hard_l19 — Build the visibility adjacency matrix

**Written rule:** Sort the objects from left to right by centroid. Output an N×N matrix for the N objects: diagonal cells show the object colors, and an off-diagonal cell is cyan(8) exactly when the two corresponding objects have unobstructed line-of-sight along a row or column.

**Program function:** `solve_hard_l19`

**Primitives:** visibility_graph, adjacency_matrix

```python
def solve_hard_l19(g: Grid) -> Grid:
    comps, edges = visibility_edges(g)
    order = sorted(range(len(comps)), key=lambda i: (
        sum(c for r, c in comps[i]["cells"]) / len(comps[i]["cells"]),
        sum(r for r, c in comps[i]["cells"]) / len(comps[i]["cells"])
    ))
    idx_map = {old: new for new, old in enumerate(order)}
    n = len(comps)
    out = blank(n, n)
    for old_i in order:
        ni = idx_map[old_i]
        out[ni][ni] = comps[old_i]["color"]
        for old_j in order:
            nj = idx_map[old_j]
            if old_i != old_j and edges[old_i][old_j]:
                out[ni][nj] = 8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 8 8 0
8 4 0 8
8 0 3 0
0 8 0 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 3 3 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 8 0 8
8 6 0 0
0 0 4 8
8 0 8 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
7 8 0 8
8 1 8 0
0 8 5 8
8 0 8 9
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
2 0 8 0
0 4 0 0
8 0 3 0
0 0 0 6
```

### hard_l20 — Fit solid inserts into matching frames

**Written rule:** The left half contains solid inserts; the right half contains hollow frames. Match each insert to the frame whose interior dimensions fit it (allowing a 90° rotation), then place the insert inside that frame.

**Program function:** `solve_hard_l20`

**Primitives:** split_canvas, fit_by_interior_dims, optional_rotate

```python
def solve_hard_l20(g: Grid) -> Grid:
    h, w = dims(g)
    mid = w // 2
    left = [row[:mid] for row in g]
    right = [row[mid:] for row in g]
    inserts = find_components(left)
    frames = frame_rectangles(right)
    out = copy_grid(right)
    used = set()
    for frame in frames:
        fr0, fc0, fr1, fc1 = bbox(frame["cells"])
        ih, iw = fr1 - fr0 - 1, fc1 - fc0 - 1
        chosen = None
        chosen_idx = None
        for i, ins in enumerate(inserts):
            if i in used:
                continue
            ir0, ic0, ir1, ic1 = bbox(ins["cells"])
            sh = [row[ic0:ic1 + 1] for row in left[ir0:ir1 + 1]]
            sh_h, sh_w = len(sh), len(sh[0])
            if (sh_h, sh_w) == (ih, iw):
                chosen = sh
                chosen_idx = i
                break
            if (sh_w, sh_h) == (ih, iw):
                chosen = rotate90(sh)
                chosen_idx = i
                break
        if chosen is None:
            continue
        used.add(chosen_idx)
        for r in range(ih):
            for c in range(iw):
                if chosen[r][c] != 0:
                    out[fr0 + 1 + r][fc0 + 1 + c] = chosen[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0
0 2 0 0 0 0 0 0 0 0 7 0 0 8 8 8 8 8
0 2 2 0 3 3 3 0 0 0 7 0 0 8 0 0 0 8
0 0 0 0 0 3 0 0 0 0 7 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0 7 7 7 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0
0 7 0 0 8 8 8 8 8
0 7 0 0 8 2 2 2 8
0 7 0 0 8 2 0 0 8
0 7 7 7 8 8 8 8 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0
0 0 4 4 0 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 3 3 3 3
0 0 0 6 0 0 0 0 0 0 2 2 2 2 3 0 0 3
0 0 0 6 0 0 0 0 0 0 0 0 0 0 3 0 0 3
0 0 0 6 6 0 0 0 0 0 0 0 0 0 3 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0
0 2 0 0 0 2 0 0 0
0 2 0 0 0 3 3 3 3
0 2 2 2 2 3 0 4 3
0 0 0 0 0 3 4 4 3
0 0 0 0 0 3 4 0 3
0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 4 4 4 4 0 0 0 0
0 0 0 8 0 0 0 0 0 0 4 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 5 5 5 5 5
0 9 9 0 0 0 0 0 0 0 4 0 0 5 0 0 0 5
0 0 9 9 0 0 0 0 0 0 4 4 4 5 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0
0 4 0 0 4 0 0 0 0
0 4 0 0 5 5 5 5 5
0 4 0 0 5 8 8 8 5
0 4 4 4 5 0 8 0 5
0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 1 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 0 1 1 0 0 0 0 0 0 6 0 0 0 6 0 0 0
0 2 2 2 0 0 0 0 0 0 6 6 6 6 7 7 7 7
0 0 2 0 0 0 0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0
0 6 0 0 0 6 0 0 0
0 6 0 0 0 6 0 0 0
0 6 6 6 6 7 7 7 7
0 0 0 0 0 7 1 0 7
0 0 0 0 0 7 1 0 7
0 0 0 0 0 7 1 1 7
0 0 0 0 0 7 7 7 7
```

### hard_l21 — Fill even-distance cells from the room seed

**Written rule:** Gray(5) cells are walls. In each room, start from the colored seed and fill only the black cells at even geodesic distance from that seed; odd-distance cells stay black.

**Program function:** `solve_hard_l21`

**Primitives:** room_bfs_parity_fill

```python
def solve_hard_l21(g: Grid) -> Grid:
    h, w = dims(g)
    out = copy_grid(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0 and v != 5:
                q = deque([(r, c)])
                dist = {(r, c): 0}
                while q:
                    rr, cc = q.popleft()
                    for dr, dc in DIR4:
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in dist:
                            if g[nr][nc] == 0:
                                dist[(nr, nc)] = dist[(rr, cc)] + 1
                                q.append((nr, nc))
                for (rr, cc), d in dist.items():
                    if g[rr][cc] == 0 and d % 2 == 0:
                        out[rr][cc] = v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 5 5 5 5 0
0 5 2 0 0 5 0 5 0 0 5 0
0 5 0 0 0 5 0 5 3 0 5 0
0 5 0 0 0 5 0 5 0 0 5 0
0 5 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 5 5 5 5 0
0 5 2 0 2 5 0 5 0 3 5 0
0 5 0 2 0 5 0 5 3 0 5 0
0 5 2 0 2 5 0 5 0 3 5 0
0 5 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 4 5 0 5 5 5 5 0
0 5 0 5 0 5 0 0 5 0
0 5 0 5 0 5 0 7 5 0
0 5 0 5 0 5 0 0 5 0
0 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 4 5 0 5 5 5 5 0
0 5 0 5 0 5 7 0 5 0
0 5 4 5 0 5 0 7 5 0
0 5 0 5 0 5 7 0 5 0
0 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 6 0 0 5 0 0 5 8 0 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 6 0 6 5 0 0 5 8 0 5 0
0 5 0 6 0 5 0 0 5 0 8 5 0
0 5 6 0 6 5 0 0 5 8 0 5 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 9 0 5 0 0 5 5 5 5 5 0 0
0 5 0 0 5 0 0 5 1 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0 0 5 0 0
0 5 5 5 5 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0 0 0 0
0 5 9 0 5 0 0 5 5 5 5 5 0 0
0 5 0 9 5 0 0 5 1 0 1 5 0 0
0 5 9 0 5 0 0 5 0 1 0 5 0 0
0 5 0 9 5 0 0 5 1 0 1 5 0 0
0 5 5 5 5 0 0 5 0 1 0 5 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
