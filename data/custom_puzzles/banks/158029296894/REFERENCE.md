# ARC Puzzle Bank — 21 Additional Puzzles

This bank contains 21 new ARC-style puzzles: 7 easy, 7 medium, and 7 hard. Each puzzle includes train/test examples, a written solution, scaffold notes, and a Python reference solver.

Files in this bundle:
- `arc_puzzle_bank_21.json` — machine-readable task bank with solutions.
- `arc_puzzle_bank_21_reference.py` — helper library plus 21 verified reference solvers.
- `arc_puzzle_bank_21.md` — this human-readable catalog.

## Summary

### Easy (7)

- `easy_01_exact_horizontal_triples` — **Exact Horizontal Triples**
- `easy_02_frame_2x2_blocks` — **Frame the 2x2 Blocks**
- `easy_03_recolor_L_by_key` — **Keyed L-Triomino Recolor**
- `easy_04_intersections_from_markers` — **Border Marker Intersections**
- `easy_05_complete_rectangle_borders_from_corners` — **Complete Rectangle Borders**
- `easy_06_mirror_object_across_bar` — **Mirror Across the Guide Bar**
- `easy_07_keep_largest_component_recolor` — **Keep the Largest Component**

### Medium (7)

- `medium_01_connect_matching_endpoints` — **Connect Matching Endpoints**
- `medium_02_translate_object_by_vector` — **Translate by Marker Vector**
- `medium_03_fill_keyed_rectangle_holes` — **Fill the Keyed Rings**
- `medium_04_mark_bbox_corners` — **Mark Bounding-Box Corners**
- `medium_05_stamp_exemplar_at_targets` — **Stamp the Exemplar at Every Target**
- `medium_06_recolor_border_touching_objects` — **Recolor Border-Touching Objects**
- `medium_07_raycast_cross_from_centers` — **Ray-Cast Crosses**

### Hard (7)

- `hard_01_rotate_exemplar_by_target_color` — **Rotate the Exemplar by Target Color**
- `hard_02_scale_smallest_object_2x` — **Scale the Smallest Object 2x**
- `hard_03_dual_key_select_and_recolor` — **Dual-Key Shape and Color Selection**
- `hard_04_row_col_intersections_within_bbox` — **Intersections Only Inside the Frame**
- `hard_05_symmetric_object_mirror` — **Mirror Only the Symmetric Object**
- `hard_06_rank_components_by_area_recolor` — **Rank Components by Area**
- `hard_07_fill_ring_by_repeated_corner_color` — **Fill Rings by the Repeated Corner Color**

## Exact Horizontal Triples (`easy_01_exact_horizontal_triples`)

**Difficulty:** easy

**Skills:** run detection, exact length, same-size recolor

**Scaffold notes:**
- Ignore all non-red cells.
- Scan each row for contiguous red runs.
- Only recolor runs whose length is exactly 3.

**Written solution:** Recolor every horizontal run of red(2) cells of exact length 3 to orange(7). Leave shorter and longer red runs unchanged.

**Program solution (Python reference):**
```python
def solve_easy_01_exact_horizontal_triples(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]!=2:
                c+=1; continue
            s=c
            while c<w and g[r][c]==2:
                c+=1
            if c-s==3:
                for cc in range(s,c):
                    out[r][cc]=7
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7
2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
2 2 2 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
7 7 7 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## Frame the 2x2 Blocks (`easy_02_frame_2x2_blocks`)

**Difficulty:** easy

**Skills:** 2x2 object detection, border drawing

**Scaffold notes:**
- Find every 2x2 all-green block.
- Treat each block's bounding box as fixed.
- Add a one-cell outer border on the surrounding background.

**Written solution:** Find each isolated 2x2 green(3) block and draw a one-cell gray(5) frame around it, keeping the green block unchanged.

**Program solution (Python reference):**
```python
def solve_easy_02_frame_2x2_blocks(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            if g[r][c]==g[r+1][c]==g[r][c+1]==g[r+1][c+1]==3:
                for rr in range(r-1,r+3):
                    for cc in range(c-1,c+3):
                        if 0<=rr<h and 0<=cc<w and not (r<=rr<=r+1 and c<=cc<=c+1):
                            if out[rr][cc]==0:
                                out[rr][cc]=5
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0
0 5 3 3 5 0 0 0 0
0 5 3 3 5 5 5 5 5
0 5 5 5 5 5 3 3 5
0 0 0 0 0 5 3 3 5
0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 5 5 5 5 0 0
0 0 0 0 5 3 3 5 0 0
0 0 0 0 5 3 3 5 0 0
0 0 0 0 5 5 5 5 0 0
5 5 5 5 0 0 0 0 0 0
5 3 3 5 0 0 0 0 0 0
5 3 3 5 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 5 3 3 5 0
0 0 0 0 0 0 5 3 3 5 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 5 5 5 5 0 0 0 0 0 0
0 5 3 3 5 0 0 0 0 0 0
0 5 3 3 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 5 3 3 5 0
0 0 0 0 0 0 5 3 3 5 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## Keyed L-Triomino Recolor (`easy_03_recolor_L_by_key`)

**Difficulty:** easy

**Skills:** shape detection, singleton key, recolor

**Scaffold notes:**
- First identify the singleton key color.
- Then segment the green components.
- Recolor only components that are size 3 and fit a 2x2 box.

**Written solution:** The single non-3 color cell is the key color. Recolor every green(3) L-triomino to that key color, and leave the key cell in place.

**Program solution (Python reference):**
```python
def solve_easy_03_recolor_L_by_key(g: Grid) -> Grid:
    out=clone(g)
    key=None
    counts=Counter(v for row in g for v in row if v!=0)
    # key is singleton color not 3
    for color,count in counts.items():
        if color!=3 and count==1:
            key=color
            break
    assert key is not None
    for comp in components_by_color(g, {3}):
        if is_L_triomino(comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=key
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0
0 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 0
0 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4
```

---

## Border Marker Intersections (`easy_04_intersections_from_markers`)

**Difficulty:** easy

**Skills:** row-column composition, border markers

**Scaffold notes:**
- Read selected rows from the left edge.
- Read selected columns from the top edge.
- Combine them by Cartesian product.

**Written solution:** Red(2) markers in the left border select rows. Blue(1) markers in the top border select columns. Put yellow(4) cells at every selected row/column intersection.

**Program solution (Python reference):**
```python
def solve_easy_04_intersections_from_markers(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    rows=[r for r in range(1,h) if g[r][0]==2]
    cols=[c for c in range(1,w) if g[0][c]==1]
    for r in rows:
        for c in cols:
            if out[r][c]==0:
                out[r][c]=4
    return out
```

**Train 1 input**
```text
0 0 1 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 1 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 4 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 0 4 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 1 0 0 1 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 1 0 0 1 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
2 4 0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 4 0 0 4 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 1 0 0 1 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 1 0 0 1 0
2 0 0 4 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 4 0 0 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 0 0 4 0 0 4 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 1 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 1 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
2 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
2 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
2 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
```

---

## Complete Rectangle Borders (`easy_05_complete_rectangle_borders_from_corners`)

**Difficulty:** easy

**Skills:** corner detection, rectangle completion

**Scaffold notes:**
- Group corner dots by color.
- For each color, look for four corners of an axis-aligned rectangle.
- Draw just the border, not the filled interior.

**Written solution:** Each set of four same-colored corner dots defines an axis-aligned rectangle. Draw the full rectangle border in that same color.

**Program solution (Python reference):**
```python
def solve_easy_05_complete_rectangle_borders_from_corners(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        # look for rectangles by corner quadruples
        rows=sorted({r for r,c in cells}); cols=sorted({c for r,c in cells})
        for i,r1 in enumerate(rows):
            for r2 in rows[i+1:]:
                for j,c1 in enumerate(cols):
                    for c2 in cols[j+1:]:
                        corners={(r1,c1),(r1,c2),(r2,c1),(r2,c2)}
                        if corners.issubset(cells):
                            for cc in range(c1,c2+1):
                                out[r1][cc]=color
                                out[r2][cc]=color
                            for rr in range(r1,r2+1):
                                out[rr][c1]=color
                                out[rr][c2]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 0 0 6 0 3 3 3 0
0 6 0 0 6 0 3 0 3 0
0 6 6 6 6 0 3 0 3 0
0 0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 6 0 0 0
8 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 0 0 8 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 6 6 0 0 0
0 0 6 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 6 0 0 0
0 0 6 6 6 6 6 6 0 0 0
8 8 8 8 0 0 0 0 0 0 0
8 0 0 8 0 0 0 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0
```

**Train 3 input**
```text
4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2
4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2
```

**Train 3 output**
```text
4 4 4 4 4 4 0 0 0
4 0 0 0 0 4 0 0 0
4 0 0 0 0 4 0 2 2
4 4 4 4 4 4 0 2 2
0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 2 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 0 0 0 0
0 6 0 0 0 6 0 0 7 7 7 0
0 6 0 0 0 6 0 0 7 0 7 0
0 6 6 6 6 6 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Mirror Across the Guide Bar (`easy_06_mirror_object_across_bar`)

**Difficulty:** easy

**Skills:** mirror symmetry, guide line, copy

**Scaffold notes:**
- Locate the full-height vertical guide bar.
- Measure each object's horizontal offset from the bar.
- Copy the object to the opposite side using the mirrored offset.

**Written solution:** A full-height gray(5) vertical bar is the mirror axis. Copy every red(2) cell across the bar to the opposite side in cyan(8), keeping the original object and the bar.

**Program solution (Python reference):**
```python
def solve_easy_06_mirror_object_across_bar(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    bar_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            bar_col=c
            break
    assert bar_col is not None
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    for r,c in cells:
        mc=2*bar_col-c
        if 0<=mc<w and out[r][mc]==0:
            out[r][mc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0 0
0 2 2 0 0 5 0 0 0 0 0
0 0 2 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 0 0 0 5 0 0 0 8 0
0 2 2 0 0 5 0 0 8 8 0
0 0 2 0 0 5 0 0 8 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 2 2 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 0 2 0 5 0 0 0 0
0 0 0 0 5 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 8 0 0
0 2 2 0 5 0 8 8 0
0 0 0 0 5 0 0 0 0
0 0 2 0 5 0 8 0 0
0 0 2 0 5 0 8 0 0
0 0 0 0 5 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 2 2 0 0 5 0 0 0 0 0 0
0 0 0 2 0 0 5 0 0 0 0 0 0
0 0 0 2 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 2 2 0 0 5 0 0 8 8 0 0
0 0 0 2 0 0 5 0 0 8 0 0 0
0 0 0 2 0 0 5 0 0 8 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 2 0 0 5 0 0 0 0 0
0 0 2 2 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 2 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 2 0 0 5 0 0 8 0 0
0 0 2 2 0 5 0 8 8 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 2 2 0 0 5 0 0 8 8 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

---

## Keep the Largest Component (`easy_07_keep_largest_component_recolor`)

**Difficulty:** easy

**Skills:** connected components, size comparison, selection

**Scaffold notes:**
- Find all green connected components.
- Compare their sizes.
- Keep only the largest and recolor it.

**Written solution:** Among all green(3) connected components, keep only the largest one and recolor it to maroon(9). Everything else becomes background.

**Program solution (Python reference):**
```python
def solve_easy_07_keep_largest_component_recolor(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    comps=components_by_color(g,{3})
    largest=max(comps, key=lambda comp: len(comp['cells']))
    for r,c in largest['cells']:
        out[r][c]=9
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 3 0
0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 3 3 0 0 0
0 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 3 0 0
0 0 0 0 0 3 3 0 3 3 0
0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 3 0 0
0 0 3 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0
```

---

## Connect Matching Endpoints (`medium_01_connect_matching_endpoints`)

**Difficulty:** medium

**Skills:** pair matching, line drawing

**Scaffold notes:**
- Treat each color independently.
- Each usable color appears exactly twice.
- Fill the inclusive straight path between the two endpoints.

**Written solution:** For each color that appears exactly twice, connect the two endpoints with a straight horizontal or vertical line of that same color.

**Program solution (Python reference):**
```python
def solve_medium_01_connect_matching_endpoints(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for cc in range(min(c1,c2), max(c1,c2)+1):
                out[r1][cc]=color
        elif c1==c2:
            for rr in range(min(r1,r2), max(r1,r2)+1):
                out[rr][c1]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 7 7 7 7 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 8 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 2
0 0 0 0 0 0 0 0 9 0 0
```

**Train 3 output**
```text
0 0 0 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 9 0 0
0 0 0 6 0 0 0 0 9 0 0
0 0 0 6 0 0 0 0 9 0 0
0 0 0 0 0 0 2 2 9 2 2
0 0 0 0 0 0 0 0 9 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 7 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 2 2 2 2 2 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 7 7 7 7 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

---

## Translate by Marker Vector (`medium_02_translate_object_by_vector`)

**Difficulty:** medium

**Skills:** vector extraction, object translation

**Scaffold notes:**
- Read the vector from marker 1 to marker 2.
- Extract the green object as a set of coordinates.
- Apply the same vector to every object cell.

**Written solution:** The blue(1) and red(2) markers define a translation vector from 1 to 2. Move the green(3) object by that vector and draw the translated copy in cyan(8) on a blank output grid.

**Program solution (Python reference):**
```python
def solve_medium_02_translate_object_by_vector(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    pos1=pos2=None
    obj=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1: pos1=(r,c)
            elif g[r][c]==2: pos2=(r,c)
            elif g[r][c]==3: obj.append((r,c))
    dr=pos2[0]-pos1[0]
    dc=pos2[1]-pos1[1]
    for r,c in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 3 0
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
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 1 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## Fill the Keyed Rings (`medium_03_fill_keyed_rectangle_holes`)

**Difficulty:** medium

**Skills:** color selection, ring detection, interior fill

**Scaffold notes:**
- Identify the color that appears both as a singleton key and as a ring.
- Find the rectangular ring components of that color.
- Fill only their interiors.

**Written solution:** One color appears both as a singleton key and as one or more hollow rectangular rings. Fill the interiors of the rings of that keyed color with cyan(8), leaving other rings unchanged.

**Program solution (Python reference):**
```python
def solve_medium_03_fill_keyed_rectangle_holes(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    comps=components_by_color(g)
    key=None
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp['color']].append(comp)
    for color, lst in by_color.items():
        if any(len(comp['cells'])==1 for comp in lst) and any(len(comp['cells'])>1 for comp in lst):
            key=color
            break
    assert key is not None
    for comp in by_color[key]:
        if len(comp['cells'])==1:
            continue
        r0,c0,r1,c1=bbox(comp['cells'])
        good=True
        for cc in range(c0,c1+1):
            if g[r0][cc]!=key or g[r1][cc]!=key: good=False
        for rr in range(r0,r1+1):
            if g[rr][c0]!=key or g[rr][c1]!=key: good=False
        if good and r1-r0>=2 and c1-c0>=2:
            for rr in range(r0+1,r1):
                for cc in range(c0+1,c1):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 2 0 0 6 6 6 6 0
0 2 0 0 2 0 0 6 0 0 6 0
0 2 2 2 2 0 0 6 0 0 6 0
0 0 0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0
0 2 8 8 2 0 0 6 6 6 6 0
0 2 8 8 2 0 0 6 0 0 6 0
0 2 2 2 2 0 0 6 0 0 6 0
0 0 0 0 0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 6 0 0 0 6 0
0 0 0 0 0 6 0 0 0 6 0
0 2 2 2 0 6 0 0 0 6 0
0 2 0 2 0 6 6 6 6 6 0
0 2 0 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 6 8 8 8 6 0
0 0 0 0 0 6 8 8 8 6 0
0 2 2 2 0 6 8 8 8 6 0
0 2 0 2 0 6 6 6 6 6 0
0 2 0 2 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 6 6 6 0 0
0 2 0 0 0 2 0 0 6 0 6 0 0
0 2 0 0 0 2 0 0 6 6 6 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 2 8 8 8 2 0 0 6 6 6 0 0
0 2 8 8 8 2 0 0 6 0 6 0 0
0 2 8 8 8 2 0 0 6 6 6 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 2 8 8 2 0
0 0 0 0 0 0 0 0 2 8 8 2 0
0 0 0 0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 6 6 6 6 6 0 2 0 2 0
0 0 6 0 0 0 6 0 2 0 2 0
0 0 6 0 0 0 6 0 2 2 2 0
0 0 6 0 0 0 6 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 6 6 6 6 6 0 2 0 2 0
0 0 6 8 8 8 6 0 2 0 2 0
0 0 6 8 8 8 6 0 2 2 2 0
0 0 6 8 8 8 6 0 0 0 0 0
0 0 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

---

## Mark Bounding-Box Corners (`medium_04_mark_bbox_corners`)

**Difficulty:** medium

**Skills:** connected components, bounding boxes

**Scaffold notes:**
- Segment the green objects first.
- Compute each object's bounding box.
- Write four corner markers per box.

**Written solution:** For each green(4) object, compute its bounding box and mark the four corners of that box with blue(1). Keep the original object cells.

**Program solution (Python reference):**
```python
def solve_medium_04_mark_bbox_corners(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for comp in components_by_color(g,{4}):
        r0,c0,r1,c1=bbox(comp['cells'])
        for r,c in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            out[r][c]=1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 4 1 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0
0 1 4 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 4 4 0 0 0 4 4 0
0 0 0 4 0 0 0 0 4 4
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 1
0 0 1 1 0 0 0 4 4 0
0 0 0 4 0 0 0 1 4 1
0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 0 4 4 4 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 4 1 0
0 1 1 0 0 0 0 0 1 4 1 0
0 4 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 4 1 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 1 4 1 0 0
0 0 0 0 0 0 0 0 0 0 0
```

---

## Stamp the Exemplar at Every Target (`medium_05_stamp_exemplar_at_targets`)

**Difficulty:** medium

**Skills:** template extraction, anchor-relative copy, multi-target stamping

**Scaffold notes:**
- Find the one connected pattern that contains both the anchor and body.
- Measure body-cell offsets relative to the anchor.
- Replay those offsets at every other anchor.

**Written solution:** The exemplar is the only connected pattern containing a blue(1) anchor plus green(3) body cells. Copy the green body cells to every other blue(1) target anchor using the same offsets.

**Program solution (Python reference):**
```python
def solve_medium_05_stamp_exemplar_at_targets(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    # find exemplar component containing 1 and 3
    seen=[[False]*w for _ in range(h)]
    exemplar_anchor=None
    offsets=None
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0:
                continue
            # flood any nonzero comp
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                rr,cc=q.popleft(); cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=0:
                        seen[nr][nc]=True; q.append((nr,nc))
            vals=[g[rr][cc] for rr,cc in cells]
            if 1 in vals and 3 in vals:
                exemplar_anchor=next((rr,cc) for rr,cc in cells if g[rr][cc]==1)
                offsets=[(rr-exemplar_anchor[0], cc-exemplar_anchor[1]) for rr,cc in cells if g[rr][cc]==3]
                break
        if exemplar_anchor: break
    assert exemplar_anchor is not None
    targets=[(r,c) for r in range(h) for c in range(w) if g[r][c]==1 and (r,c)!=exemplar_anchor]
    for tr,tc in targets:
        for dr,dc in offsets:
            nr,nc=tr+dr, tc+dc
            if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                out[nr][nc]=3
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 1 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 1 3 0
0 3 3 0 0 0 0 0 3 3 0
0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
0 0 1 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 3 0
0 0 1 3 0 0 0 0 0 0 3 0
0 0 0 3 0 0 0 0 0 3 3 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 3 0 0
0 1 3 0 0 0 0 0 0 3 0 0
0 0 3 0 0 0 0 0 3 3 0 0
0 3 3 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 3 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 1 3 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 1 3 0
0 0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 3 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Recolor Border-Touching Objects (`medium_06_recolor_border_touching_objects`)

**Difficulty:** medium

**Skills:** connected components, border relation

**Scaffold notes:**
- Segment the green objects.
- Ask whether any cell of an object touches the outer frame.
- Recolor only those touching components.

**Written solution:** Find all green(4) objects. Recolor exactly those objects that touch any image border to red(2). Leave interior objects green.

**Program solution (Python reference):**
```python
def solve_medium_06_recolor_border_touching_objects(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    for comp in components_by_color(g,{4}):
        if touches_border(comp['cells'], h,w):
            for r,c in comp['cells']:
                out[r][c]=2
    return out
```

**Train 1 input**
```text
0 4 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 2 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
4 0 0 0 0 4 0 0 0 0 0
4 4 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 4 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
2 0 0 0 0 4 0 0 0 0 0
2 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 4 4 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 2 0 0
0 4 0 0 0 0 2 2 0
0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

---

## Ray-Cast Crosses (`medium_07_raycast_cross_from_centers`)

**Difficulty:** medium

**Skills:** ray casting, blockers, grid growth

**Scaffold notes:**
- Start from each magenta center.
- Shoot rays in four cardinal directions.
- Stop each ray at a blocker or the grid edge.

**Written solution:** From each magenta(6) center, extend magenta rays up, down, left, and right through empty cells until a gray(5) blocker or the edge stops the ray.

**Program solution (Python reference):**
```python
def solve_medium_07_raycast_cross_from_centers(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    centers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==6]
    blockers={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    for r,c in centers:
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc=r+dr,c+dc
            while 0<=nr<h and 0<=nc<w and (nr,nc) not in blockers:
                out[nr][nc]=6
                nr+=dr; nc+=dc
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 6 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 5 6 6 6 6 6 6 5 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 0 6 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 6 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 2 output**
```text
0 0 5 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
5 6 6 6 6 5 0 0 0 0
0 0 6 0 0 0 0 5 0 0
0 0 5 0 0 0 0 6 0 0
0 0 0 0 5 6 6 6 6 5
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 6 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 5 6 6 6 6 6 6 5 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 6 0 0 5
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 6 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 5 6 6 6 6 6 5
0 0 5 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 6 0 0 0
5 6 6 6 6 5 0 6 0 0 0
0 0 6 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 5 0 0 0
```

---

## Rotate the Exemplar by Target Color (`hard_01_rotate_exemplar_by_target_color`)

**Difficulty:** hard

**Skills:** template extraction, rotation, color-coded control

**Scaffold notes:**
- Extract the exemplar as anchor plus relative body offsets.
- Decode target-marker color into a rotation amount.
- Rotate the offsets before stamping them at each target.

**Written solution:** The exemplar is the connected shape with a blue(1) anchor and green(3) body. Copy its green body to each target marker. Marker color 2 means no rotation, 4 means rotate 90° clockwise, 6 means 180°, and 8 means 270° clockwise.

**Program solution (Python reference):**
```python
def solve_hard_01_rotate_exemplar_by_target_color(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    # exemplar comp with anchor 1 and body 3
    seen=[[False]*w for _ in range(h)]
    anchor=None
    body_offsets=None
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0:
                continue
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                rr,cc=q.popleft(); cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]!=0:
                        seen[nr][nc]=True; q.append((nr,nc))
            vals=[g[rr][cc] for rr,cc in cells]
            if 1 in vals and 3 in vals:
                anchor=next((rr,cc) for rr,cc in cells if g[rr][cc]==1)
                body_offsets=[(rr-anchor[0], cc-anchor[1]) for rr,cc in cells if g[rr][cc]==3]
                break
        if anchor: break
    assert anchor
    rot_map={2:0,4:1,6:2,8:3}
    targets=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in rot_map and (r,c)!=anchor]
    for tr,tc,color in targets:
        roffs=rotate_offsets(body_offsets, rot_map[color])
        for dr,dc in roffs:
            nr,nc=tr+dr, tc+dc
            if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                out[nr][nc]=3
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 2 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 2 3 0 0
0 0 3 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 4 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 3 0 0 0 0 0 0 6 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 1 3 0 0 0 0 0 3 6 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 8 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 2 3 0
0 0 0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 6 0 0 0
0 0 3 4 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 0 4 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 3 0 0 0 0 0 0 3 4 0 0
0 3 3 0 0 0 0 0 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 8 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 3 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
```

---

## Scale the Smallest Object 2x (`hard_02_scale_smallest_object_2x`)

**Difficulty:** hard

**Skills:** component selection, scaling

**Scaffold notes:**
- Find all green components and choose the smallest.
- Normalize it to its top-left corner.
- Replace each source cell by a 2x2 block at doubled coordinates.

**Written solution:** Among all green(3) objects, choose the smallest connected component. Remove everything else and draw a 2x scaled version of that smallest object in cyan(8), anchored at the same top-left corner.

**Program solution (Python reference):**
```python
def solve_hard_02_scale_smallest_object_2x(g: Grid) -> Grid:
    h,w=dims(g)
    out=zeros(h,w)
    comps=components_by_color(g,{3})
    smallest=min(comps, key=lambda comp: len(comp['cells']))
    r0,c0,r1,c1=bbox(smallest['cells'])
    pts=[(r-r0,c-c0) for r,c in smallest['cells']]
    for r,c in pts:
        base_r=r0+2*r
        base_c=c0+2*c
        for dr in [0,1]:
            for dc in [0,1]:
                nr,nc=base_r+dr, base_c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0
0 3 0 0 0 0 0 0 3 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 3 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 3 3 0 0
0 0 3 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 3 0 0 0 0 0 0 3 3 0 0 0
0 3 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Dual-Key Shape and Color Selection (`hard_03_dual_key_select_and_recolor`)

**Difficulty:** hard

**Skills:** two control signals, shape classification, conditional recolor

**Scaffold notes:**
- Read the shape key and the color key separately.
- Classify each green component by shape family.
- Recolor only the family named by the shape key.

**Written solution:** A singleton shape key chooses which family of green(3) objects to recolor: blue(1) selects L-triominoes, yellow(4) selects plus-shapes. A singleton color key (2, 6, or 8) gives the new color. Recolor only the selected family to the color key.

**Program solution (Python reference):**
```python
def solve_hard_03_dual_key_select_and_recolor(g: Grid) -> Grid:
    out=clone(g)
    counts=Counter(v for row in g for v in row if v!=0)
    color_key=None
    shape_key=None
    # color key among {2,6,8} with singleton
    for color in [2,6,8]:
        if counts[color]==1:
            color_key=color
    # shape key among {1,4} with singleton
    for color in [1,4]:
        if counts[color]==1:
            shape_key=color
    assert color_key is not None and shape_key is not None
    for comp in components_by_color(g,{3}):
        fam='L' if is_L_triomino(comp['cells']) else 'PLUS' if is_plus5(comp['cells']) else None
        if (shape_key==1 and fam=='L') or (shape_key==4 and fam=='PLUS'):
            for r,c in comp['cells']:
                out[r][c]=color_key
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 1 output**
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 3 0 0
0 0 2 2 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0
0 3 3 3 0 0 0 0 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 3 0 0
0 6 6 6 0 0 0 0 3 3 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 8 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 3 0
0 0 0 0 3 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
```

**Train 3 output**
```text
0 0 0 0 0 8 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 8 0
0 0 0 0 3 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1
```

**Test input**
```text
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 3 0 0 0 0 0 3 3 3 0 0
0 3 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 3 0 0 0 0 0 2 2 2 0 0
0 3 3 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
```

---

## Intersections Only Inside the Frame (`hard_04_row_col_intersections_within_bbox`)

**Difficulty:** hard

**Skills:** global markers, bbox gating, multi-step composition

**Scaffold notes:**
- Read candidate rows and columns from the border markers.
- Find the interior of the gray frame.
- Only keep row/column intersections that fall inside that interior.

**Written solution:** Blue(1) top markers choose columns and red(2) left markers choose rows, but only intersections strictly inside the gray(7) rectangular frame are filled. Put cyan(8) at those valid intersections only.

**Program solution (Python reference):**
```python
def solve_hard_04_row_col_intersections_within_bbox(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==7]
    r0,c0,r1,c1=bbox(frame_cells)
    rows=[r for r in range(1,h) if g[r][0]==2 and r0<r<r1]
    cols=[c for c in range(1,w) if g[0][c]==1 and c0<c<c1]
    for r in rows:
        for c in cols:
            if out[r][c]==0:
                out[r][c]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 1 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 7 0 0 0 0 0 7 0 0
0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 7 0 0 0 0 0 7 0 0
0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 1 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 7 8 0 0 8 0 7 0 0
0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 7 8 0 0 8 0 7 0 0
0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 1 0 0 1 0 0 1 0
0 0 7 7 7 7 7 7 7 0 0
2 0 7 0 0 0 0 0 7 0 0
0 0 7 0 0 0 0 0 7 0 0
2 0 7 0 0 0 0 0 7 0 0
0 0 7 0 0 0 0 0 7 0 0
0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 1 0 0 1 0 0 1 0
0 0 7 7 7 7 7 7 7 0 0
2 0 7 8 0 0 8 0 7 0 0
0 0 7 0 0 0 0 0 7 0 0
2 0 7 8 0 0 8 0 7 0 0
0 0 7 0 0 0 0 0 7 0 0
0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 1 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 1 0 0 1 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 7 7 7 7 0 0
2 0 0 0 7 8 0 0 8 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 0 7 8 0 0 8 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
0 0 0 0 7 0 0 0 0 0 7 0 0
2 0 0 0 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 1 0 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0
2 0 7 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
2 0 7 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 1 0 1 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0
2 0 7 8 0 8 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
2 0 7 8 0 8 0 0 7 0 0 0
0 0 7 0 0 0 0 0 7 0 0 0
0 0 7 7 7 7 7 7 7 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
```

---

## Mirror Only the Symmetric Object (`hard_05_symmetric_object_mirror`)

**Difficulty:** hard

**Skills:** property-based selection, symmetry, copy

**Scaffold notes:**
- Test each left-side object for vertical symmetry within its own box.
- Select the unique symmetric one.
- Mirror only that object across the guide bar.

**Written solution:** Several green(4) objects appear left of a full-height gray(5) guide bar. Exactly one of them is vertically symmetric within its own bounding box. Mirror only that symmetric object across the guide bar in cyan(8).

**Program solution (Python reference):**
```python
def solve_hard_05_symmetric_object_mirror(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    bar_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            bar_col=c; break
    assert bar_col is not None
    target=None
    for comp in components_by_color(g,{4}):
        if is_vertically_symmetric(comp['cells']):
            target=comp['cells']; break
    assert target is not None
    for r,c in target:
        mc=2*bar_col-c
        if 0<=mc<w and out[r][mc]==0:
            out[r][mc]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 4 0 5 0 0 0 0 0 0
0 0 4 0 4 4 5 0 0 0 0 0 0
0 4 4 4 0 0 5 0 0 0 0 0 0
0 0 4 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 4 4 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 4 0 5 0 0 0 0 0 0
0 0 4 0 4 4 5 0 0 0 8 0 0
0 4 4 4 0 0 5 0 0 8 8 8 0
0 0 4 0 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 4 4 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 4 0 0 5 0 0 0 0 0
0 4 4 4 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 4 0 4 0 5 0 0 0 0 0
0 4 4 4 0 5 0 0 0 0 0
0 0 0 4 4 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 4 0 0 5 0 0 8 0 0
0 4 4 4 0 5 0 8 8 8 0
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
0 4 0 4 0 5 0 0 0 0 0
0 4 4 4 0 5 0 0 0 0 0
0 0 0 4 4 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 4 0 5 0 0 0 0 0 0 0
0 0 0 0 0 4 4 5 0 0 0 0 0 0 0
0 0 4 0 0 0 0 5 0 0 0 0 0 0 0
0 4 4 4 0 0 0 5 0 0 0 0 0 0 0
0 0 4 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 4 4 0 0 5 0 0 0 0 0 0 0
0 0 0 0 4 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 4 0 5 0 0 0 0 0 0 0
0 0 0 0 0 4 4 5 0 0 0 0 0 0 0
0 0 4 0 0 0 0 5 0 0 0 0 8 0 0
0 4 4 4 0 0 0 5 0 0 0 8 8 8 0
0 0 4 0 0 0 0 5 0 0 0 0 8 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 4 4 0 0 5 0 0 0 0 0 0 0
0 0 0 0 4 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 0 0 0 0
0 0 4 4 4 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 4 0 0 0 0 5 0 0 0 0 0 0
0 4 4 0 4 4 5 0 0 0 0 0 0
0 0 0 0 0 4 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 4 0 0 5 0 0 8 0 0 0
0 0 4 4 4 0 5 0 8 8 8 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 4 0 0 0 0 5 0 0 0 0 0 0
0 4 4 0 4 4 5 0 0 0 0 0 0
0 0 0 0 0 4 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0
```

---

## Rank Components by Area (`hard_06_rank_components_by_area_recolor`)

**Difficulty:** hard

**Skills:** connected components, sorting, rank-based recolor

**Scaffold notes:**
- Segment the three components.
- Sort them by area from smallest to largest.
- Apply a different target color to each rank.

**Written solution:** There are exactly three green(3) connected components. Recolor the smallest one to red(2), the middle one to yellow(4), and the largest one to magenta(6).

**Program solution (Python reference):**
```python
def solve_hard_06_rank_components_by_area_recolor(g: Grid) -> Grid:
    out=clone(g)
    comps=components_by_color(g,{3})
    ordered=sorted(comps, key=lambda comp: len(comp['cells']))
    rank_colors=[2,4,6]
    assert len(ordered)==3
    for rank,comp in enumerate(ordered):
        for r,c in comp['cells']:
            out[r][c]=rank_colors[rank]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0 0 0
0 3 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 0 0 0 0
0 2 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0
0 0 4 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 6 0 2 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

---

## Fill Rings by the Repeated Corner Color (`hard_07_fill_ring_by_repeated_corner_color`)

**Difficulty:** hard

**Skills:** counting, global key extraction, ring filling

**Scaffold notes:**
- Read the four corner-marker colors as a multiset.
- Choose the color that occurs most often.
- Use that as the fill for every hollow ring interior.

**Written solution:** Look at the four corner marker colors. The color that appears most often is the fill color. Fill the interiors of all hollow green(3) rings with that repeated corner color, while keeping the rings and corner markers.

**Program solution (Python reference):**
```python
def solve_hard_07_fill_ring_by_repeated_corner_color(g: Grid) -> Grid:
    out=clone(g)
    h,w=dims(g)
    corners=[g[0][0], g[0][w-1], g[h-1][0], g[h-1][w-1]]
    counts=Counter(c for c in corners if c!=0)
    fill_color=max(counts, key=lambda c: counts[c])
    # fill interiors of rectangular rings of color 3
    for comp in components_by_color(g,{3}):
        r0,c0,r1,c1=bbox(comp['cells'])
        good=True
        for cc in range(c0,c1+1):
            if g[r0][cc]!=3 or g[r1][cc]!=3: good=False
        for rr in range(r0,r1+1):
            if g[rr][c0]!=3 or g[rr][c1]!=3: good=False
        if good and r1-r0>=2 and c1-c0>=2:
            for rr in range(r0+1,r1):
                for cc in range(c0+1,c1):
                    if out[rr][cc]==0:
                        out[rr][cc]=fill_color
    return out
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 3 0 0 3 0 0 3 3 3 0
0 0 3 0 0 3 0 0 3 0 3 0
0 0 3 0 0 3 0 0 3 0 3 0
0 0 3 3 3 3 0 0 3 0 3 0
0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 6
```

**Train 1 output**
```text
2 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 3 2 2 3 0 0 3 3 3 0
0 0 3 2 2 3 0 0 3 2 3 0
0 0 3 2 2 3 0 0 3 2 3 0
0 0 3 3 3 3 0 0 3 2 3 0
0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 6
```

**Train 2 input**
```text
8 0 0 0 0 0 0 0 0 0 4
0 0 0 3 3 3 3 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 8
```

**Train 2 output**
```text
8 0 0 0 0 0 0 0 0 0 4
0 0 0 3 3 3 3 3 0 0 0
0 0 0 3 8 8 8 3 0 0 0
0 0 0 3 8 8 8 3 0 0 0
0 0 0 3 8 8 8 3 0 0 0
0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 8
```

**Train 3 input**
```text
6 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 3 0 0 3 3 3 3 0
0 0 3 0 0 3 0 0 3 0 0 3 0
0 0 3 0 0 3 0 0 3 0 0 3 0
0 0 3 0 0 3 0 0 3 0 0 3 0
0 0 3 3 3 3 0 0 3 0 0 3 0
0 0 0 0 0 0 0 0 3 3 3 3 0
2 0 0 0 0 0 0 0 0 0 0 0 6
```

**Train 3 output**
```text
6 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0 0
0 0 3 6 6 3 0 0 0 0 0 0 0
0 0 3 6 6 3 0 0 3 3 3 3 0
0 0 3 6 6 3 0 0 3 6 6 3 0
0 0 3 6 6 3 0 0 3 6 6 3 0
0 0 3 6 6 3 0 0 3 6 6 3 0
0 0 3 3 3 3 0 0 3 6 6 3 0
0 0 0 0 0 0 0 0 3 3 3 3 0
2 0 0 0 0 0 0 0 0 0 0 0 6
```

**Test input**
```text
4 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 3 3 3 3 0
0 3 3 3 3 0 0 3 0 0 3 0
0 3 0 0 3 0 0 3 0 0 3 0
0 3 0 0 3 0 0 3 3 3 3 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 4
```

**Test output**
```text
4 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 3 3 3 3 0
0 3 3 3 3 0 0 3 4 4 3 0
0 3 4 4 3 0 0 3 4 4 3 0
0 3 4 4 3 0 0 3 3 3 3 0
0 3 4 4 3 0 0 0 0 0 0 0
0 3 4 4 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 4
```

---

