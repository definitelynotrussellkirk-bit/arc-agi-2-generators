# ARC-style Puzzle Bank — 21 more puzzles (set 11)

This eleventh bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans into contour extraction, perimeter logic, hole reasoning, selection by structural signature, symmetry under rotation/reflection, anchor-based transport, and panel comparison. The shared emphasis is on distinguishing an object's boundary from its interior and then using that distinction in several different ways.

This set introduces a new helper primitive:

```text
boundary_cells(cells, connectivity=4)
  Return the subset of an object's cells that touch background or the outside in the chosen connectivity. This is useful for outline extraction, perimeter-based ranking, and separating boundary from interior.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set11_reference.py`.


## Index

### Easy

- **S11_E1** — Keep Only the Boundary

- **S11_E2** — Fill Rectangular Frames

- **S11_E3** — Crop the Smallest Object

- **S11_E4** — Mark Segment Endpoints

- **S11_E5** — Move an Outline to the Anchor

- **S11_E6** — Mirror Dots Across the Axis

- **S11_E7** — Bounding-Box Corners


### Medium

- **S11_M1** — Largest Perimeter Wins

- **S11_M2** — Fill Only Enclosed Holes

- **S11_M3** — Header Picks the Boundary Count

- **S11_M4** — Rectangle from Diagonal Markers

- **S11_M5** — Symmetrize the Largest Shape

- **S11_M6** — Two-Panel XOR Mask

- **S11_M7** — Area-Rank Recolor from Header


### Hard

- **S11_H1** — Nested Frame Fill by Container

- **S11_H2** — Rotation-Coded Boundary Stamps

- **S11_H3** — Select by Hole Count

- **S11_H4** — Find the Unpaired Shape Under Symmetry

- **S11_H5** — Translate and Split Boundary vs Interior

- **S11_H6** — Dual Legend: Area and Boundary

- **S11_H7** — Common Shape Across Three Panels


# Easy

## S11_E1 — Keep Only the Boundary

**Skills:** outline extraction, object components, same-size transform


**Primitive note:** Uses the new boundary_cells primitive directly.


**Scaffold:**

- Find every non-zero connected component.

- Keep only the cells that touch background or the outside.

- Erase each component's interior but preserve its color.


**Train 1 input**

```text
000000000
022220000
022220330
022220330
000000330
000000000
000000000
```
**Train 1 output**

```text
000000000
022220000
020020330
022220330
000000330
000000000
000000000
```

**Train 2 input**

```text
0000000000
0444400000
0444400000
0444400000
0000006660
0000006660
0000006660
0000000000
```
**Train 2 output**

```text
0000000000
0444400000
0400400000
0444400000
0000006660
0000006060
0000006660
0000000000
```
**Test input**

```text
00000000000
00022220000
00022220000
00022220000
00000000000
00777000000
00777000000
00777000000
00000000000
```
**Test output**

```text
00000000000
00022220000
00020020000
00022220000
00000000000
00777000000
00707000000
00777000000
00000000000
```
**Written solution:** Treat each colored object separately. A cell stays if it lies on the object's boundary, meaning at least one of its four neighbors is outside the object. Interior cells are turned to black(0), so every solid block becomes a hollow outline.

**Reference program:**

```python
def solve_S11_E1(grid):
    out = blank(*dims(grid), 0)
    for comp in components(grid):
        for r,c in boundary_cells(comp["cells"]):
            out[r][c] = comp["color"]
    return out
```

## S11_E2 — Fill Rectangular Frames

**Skills:** frame detection, interior fill, same-size transform


**Scaffold:**

- Look for hollow rectangular frames.

- Keep the frame colors unchanged.

- Fill the inside of each closed frame with cyan(8).


**Train 1 input**

```text
0000000000
0222203330
0200203030
0200203030
0222203330
0000000000
```
**Train 1 output**

```text
0000000000
0222203330
0288203830
0288203830
0222203330
0000000000
```

**Train 2 input**

```text
00000000000
04444400000
04000406660
04000406060
04000406060
04444406660
00000000000
```
**Train 2 output**

```text
00000000000
04444400000
04888406660
04888406860
04888406860
04444406660
00000000000
```
**Test input**

```text
000000000000
022220000666
020020000606
020020000606
022220000666
000000000000
```
**Test output**

```text
000000000000
022220000666
028820000686
028820000686
022220000666
000000000000
```
**Written solution:** Each object is a rectangular border. Detect its bounding box, verify that the colored cells form the border of that box, and then fill the interior cells with cyan(8) while leaving the frame itself unchanged.

**Reference program:**

```python
def solve_S11_E2(grid):
    out = copyg(grid)
    for comp in components(grid):
        cells = comp["cells"]
        r1,c1,r2,c2 = bbox(cells)
        if set(cells) == set(rect_border(r1,c1,r2,c2)):
            for r in range(r1+1, r2):
                for c in range(c1+1, c2):
                    if out[r][c] == 0:
                        out[r][c] = 8
    return out
```

## S11_E3 — Crop the Smallest Object

**Skills:** component counting, size comparison, cropping


**Scaffold:**

- Split the non-zero cells into connected objects.

- Choose the object with the fewest cells.

- Crop tightly to that object's bounding box.


**Train 1 input**

```text
000000000
022200000
022200330
000000000
000044400
000000000
000000000
```
**Train 1 output**

```text
33
```

**Train 2 input**

```text
0000000000
0444400000
0000000000
2200000000
0200007770
0000007770
0000007770
```
**Train 2 output**

```text
22
02
```
**Test input**

```text
00000000000
00077777000
00000000000
22000000000
22000066660
00000066660
00000066660
00000000000
```
**Test output**

```text
22
22
```
**Written solution:** Among all non-zero connected components, select the one with the smallest area. Ignore the larger distractors and return only the chosen object, cropped to its own bounding box.

**Reference program:**

```python
def solve_S11_E3(grid):
    best = min(components(grid), key=lambda c: (len(c["cells"]), c["color"]))
    return normalized_component_grid(grid, best["cells"])
```

## S11_E4 — Mark Segment Endpoints

**Skills:** line recognition, extreme points, same-size recolor


**Scaffold:**

- Each object is a straight horizontal or vertical segment.

- Find the two extreme cells of each segment.

- Recolor just those endpoints to cyan(8).


**Train 1 input**

```text
000000000
022220000
000000300
000000300
000000300
000000300
000000000
```
**Train 1 output**

```text
000000000
082280000
000000800
000000300
000000300
000000800
000000000
```

**Train 2 input**

```text
0004000000
0004000000
0004000000
0555555000
0000000000
0060000000
0060000000
```
**Train 2 output**

```text
0008000000
0004000000
0008000000
0855558000
0000000000
0080000000
0080000000
```
**Test input**

```text
0003000000
0003000000
0003000000
0003000000
0000000000
2222200000
0000000060
0000000060
```
**Test output**

```text
0008000000
0003000000
0003000000
0008000000
0000000000
8222800000
0000000080
0000000080
```
**Written solution:** For every straight line segment, keep the segment in place but recolor its endpoints. Horizontal segments use the leftmost and rightmost cells, and vertical segments use the topmost and bottommost cells.

**Reference program:**

```python
def solve_S11_E4(grid):
    out = copyg(grid)
    for comp in components(grid):
        cells = comp["cells"]
        rs = {r for r,c in cells}
        cs = {c for r,c in cells}
        if len(rs) == 1 and len(cells) >= 2:
            r = next(iter(rs))
            out[r][min(cs)] = 8
            out[r][max(cs)] = 8
        elif len(cs) == 1 and len(cells) >= 2:
            c = next(iter(cs))
            out[min(rs)][c] = 8
            out[max(rs)][c] = 8
    return out
```

## S11_E5 — Move an Outline to the Anchor

**Skills:** translation, bounding box alignment, outline extraction


**Primitive note:** Uses boundary_cells after translating the chosen object.


**Scaffold:**

- Find the single anchor cell color 1.

- Take the main colored object and keep only its boundary.

- Translate that boundary so its top-left corner lands on the anchor.


**Train 1 input**

```text
0000000000
0444400000
0444400000
0444400000
0000010000
0000000000
0000000000
0000000000
```
**Train 1 output**

```text
0000000000
0000000000
0000000000
0000000000
0000044440
0000040040
0000044440
0000000000
```

**Train 2 input**

```text
00000000000
07770000000
07770000000
07770000000
00000000000
00000100000
00000000000
00000000000
```
**Train 2 output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000777000
00000707000
00000777000
```
**Test input**

```text
000000000000
000044440000
000044440000
000044440000
000000000000
010000000000
000000000000
000000000000
000000000000
```
**Test output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
044440000000
040040000000
044440000000
000000000000
```
**Written solution:** Find the anchor cell and the main non-anchor object. Compute the object's top-left bounding-box corner, keep only the boundary cells of the object, and translate those boundary cells so that corner aligns with the anchor. The output is otherwise blank.

**Reference program:**

```python
def solve_S11_E5(grid):
    h, w = dims(grid)
    anchor = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 1)
    comp = max([c for c in components(grid) if c["color"] != 1], key=lambda c: len(c["cells"]))
    r1,c1,r2,c2 = bbox(comp["cells"])
    dr, dc = anchor[0]-r1, anchor[1]-c1
    out = blank(h, w, 0)
    for r,c in boundary_cells(comp["cells"]):
        nr, nc = r+dr, c+dc
        if 0 <= nr < h and 0 <= nc < w:
            out[nr][nc] = comp["color"]
    return out
```

## S11_E6 — Mirror Dots Across the Axis

**Skills:** reflection, axis detection, same-size completion


**Scaffold:**

- Find the full vertical axis made of color 5.

- For every colored dot away from the axis, reflect it across that line.

- Keep the originals and add the missing mirrors.


**Train 1 input**

```text
000050000
020050000
000050300
000050000
004050000
000050000
```
**Train 1 output**

```text
000050000
020050020
003050300
000050000
004050400
000050000
```

**Train 2 input**

```text
00000500000
20000500000
00000500000
00000500040
00000500000
03000500000
00000500000
```
**Train 2 output**

```text
00000500000
20000500002
00000500000
04000500040
00000500000
03000500030
00000500000
```
**Test input**

```text
0000500000
0200500000
0000504000
0000500000
0030500000
0000500000
```
**Test output**

```text
0000500000
0200500200
0040504000
0000500000
0030503000
0000500000
```
**Written solution:** The column of 5s is a mirror axis. Every non-zero non-axis cell gets copied to the reflected position on the other side of the axis, preserving color. Existing cells remain in place.

**Reference program:**

```python
def solve_S11_E6(grid):
    out = copyg(grid)
    h, w = dims(grid)
    axis_col = next(c for c in range(w) if all(grid[r][c] == 5 for r in range(h)))
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            if v not in (0,5) and c != axis_col:
                mc = 2*axis_col - c
                if 0 <= mc < w and out[r][mc] == 0:
                    out[r][mc] = v
    return out
```

## S11_E7 — Bounding-Box Corners

**Skills:** bounding boxes, corner extraction, same-size transform


**Scaffold:**

- Find each connected object.

- Compute its bounding box.

- Mark only the four corners of that box in the object's color.


**Train 1 input**

```text
0000000000
0222200000
0222200000
0222200000
0000004440
0000004440
0000000000
```
**Train 1 output**

```text
0000000000
0200200000
0000000000
0200200000
0000004040
0000004040
0000000000
```

**Train 2 input**

```text
00000000000
03330000000
03330000000
00000066660
00000066660
00000066660
00000000000
```
**Train 2 output**

```text
00000000000
03030000000
03030000000
00000060060
00000000000
00000060060
00000000000
```
**Test input**

```text
000000000000
022222000000
022222000000
022222000000
000000000000
000007770000
000007770000
000000000000
```
**Test output**

```text
000000000000
020002000000
000000000000
020002000000
000000000000
000007070000
000007070000
000000000000
```
**Written solution:** For each colored component, compute the minimum and maximum row and column it occupies. Paint only those four bounding-box corner cells and erase everything else.

**Reference program:**

```python
def solve_S11_E7(grid):
    out = blank(*dims(grid), 0)
    for comp in components(grid):
        r1,c1,r2,c2 = bbox(comp["cells"])
        for r,c in {(r1,c1),(r1,c2),(r2,c1),(r2,c2)}:
            out[r][c] = comp["color"]
    return out
```

# Medium

## S11_M1 — Largest Perimeter Wins

**Skills:** boundary counting, component comparison, selection


**Primitive note:** Uses boundary_cells to compare perimeters rather than areas.


**Scaffold:**

- Measure the boundary size of each component.

- Choose the object with the most boundary cells.

- Output only that object, recolored to cyan(8).


**Train 1 input**

```text
000000000000
022222220000
022222220000
000000000000
000044440000
000044440000
000044440000
000044440000
```
**Train 1 output**

```text
000000000000
088888880000
088888880000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 2 input**

```text
0000000000000
0333333330000
0333333330000
0000000000000
0000444444000
0000444444000
0000444444000
0000000000000
```
**Train 2 output**

```text
0000000000000
0888888880000
0888888880000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Test input**

```text
000000000000
022222220000
022222220000
000000000000
000033330000
000033330000
000033330000
000000000000
```
**Test output**

```text
000000000000
088888880000
088888880000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Written solution:** Do not choose by area alone. Count boundary cells for each component and select the one with the largest perimeter-like boundary size. Copy only that object into a blank grid and recolor it to cyan(8).

**Reference program:**

```python
def solve_S11_M1(grid):
    best = max(components(grid), key=lambda c: (len(boundary_cells(c["cells"])), len(c["cells"]), c["color"]))
    out = blank(*dims(grid), 0)
    for r,c in best["cells"]:
        out[r][c] = 8
    return out
```

## S11_M2 — Fill Only Enclosed Holes

**Skills:** flood fill, enclosure, hole detection


**Scaffold:**

- Look at the black(0) regions, not just the colored objects.

- Find zero regions that do not touch the outside border.

- Fill only those enclosed holes with cyan(8).


**Train 1 input**

```text
000000000000
022220000000
020020044400
020020040000
022220044400
000000000000
```
**Train 1 output**

```text
000000000000
022220000000
028820044400
028820040000
022220044400
000000000000
```

**Train 2 input**

```text
000000000000
033300000000
030300066660
033300060060
000000066660
000000000000
```
**Train 2 output**

```text
000000000000
033300000000
038300066660
033300068860
000000066660
000000000000
```
**Test input**

```text
000000000000
066660000000
060060044400
066660040000
000000044400
000000000000
```
**Test output**

```text
000000000000
066660000000
068860044400
066660040000
000000044400
000000000000
```
**Written solution:** Compute connected components of the background. Any zero-region that touches the outer border is still outside and stays black; any zero-region fully enclosed by colored cells is a hole and gets filled with cyan(8).

**Reference program:**

```python
def solve_S11_M2(grid):
    out = copyg(grid)
    for cells in enclosed_zero_regions(grid):
        for r,c in cells:
            out[r][c] = 8
    return out
```

## S11_M3 — Header Picks the Boundary Count

**Skills:** header decoding, boundary counting, normalized crop


**Primitive note:** Uses boundary_cells as the feature matched against the header count.


**Scaffold:**

- Count the 1s in the top row.

- In the body, find the object whose boundary has exactly that many cells.

- Return that object's boundary as a tight normalized crop.


**Train 1 input**

```text
111111110000
220003330000
220003330000
000003330444
000000000444
000000000444
000000000000
```
**Train 1 output**

```text
333
303
333
```

**Train 2 input**

```text
1111111111000
2200033304440
2200033304440
0000033304440
0000000004440
0000000000000
```
**Train 2 output**

```text
444
404
404
444
```
**Test input**

```text
111100000000
2200033304440
2200033304440
0000033304440
0000000004440
0000000000000
```
**Test output**

```text
22
22
```
**Written solution:** The top row gives a target number. Compare that number to the boundary-cell counts of the body objects, choose the matching object, then crop tightly to it and keep only its boundary cells.

**Reference program:**

```python
def solve_S11_M3(grid):
    n = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if len(boundary_cells(comp["cells"])) == n)
    return normalized_component_grid(body, best["cells"], use_boundary=True)
```

## S11_M4 — Rectangle from Diagonal Markers

**Skills:** pairing, geometry, rectangle construction


**Scaffold:**

- Each color appears exactly twice.

- Treat the pair as opposite corners of an axis-aligned rectangle.

- Draw the full rectangle border in that same color.


**Train 1 input**

```text
0000000000
0200000000
0000003000
0000000000
0000020000
0000000003
0000000000
```
**Train 1 output**

```text
0000000000
0222220000
0200023333
0200023003
0222223003
0000003333
0000000000
```

**Train 2 input**

```text
00000000000
04000000000
00000000060
00000000000
00040000000
00000000000
00000060000
```
**Train 2 output**

```text
00000000000
04440000000
04040066660
04040060060
04440060060
00000060060
00000066660
```
**Test input**

```text
0000000000
0200000000
0000000000
0000000030
0000000000
0000200000
0000003000
```
**Test output**

```text
0000000000
0222200000
0200200000
0200203330
0200203030
0222203030
0000003330
```
**Written solution:** For each color, find its two marker cells. Use their rows and columns as the corners of a rectangle and paint the entire border of that rectangle in the same color.

**Reference program:**

```python
def solve_S11_M4(grid):
    out = blank(*dims(grid), 0)
    pos = defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v != 0:
                pos[v].append((r,c))
    for v, cells in pos.items():
        if len(cells) == 2:
            (r1,c1),(r2,c2) = cells
            for r,c in rect_border(min(r1,r2), min(c1,c2), max(r1,r2), max(c1,c2)):
                out[r][c] = v
    return out
```

## S11_M5 — Symmetrize the Largest Shape

**Skills:** reflection, normalization, largest-object selection


**Scaffold:**

- Pick the largest component.

- Normalize it to its own bounding box.

- Union it with its mirror across the bounding box's vertical axis and output the result as a crop.


**Train 1 input**

```text
0000000000
0222000000
0200003300
0220003000
0000000000
```
**Train 1 output**

```text
222
202
222
```

**Train 2 input**

```text
00000000000
03330000000
00300000000
03300004400
00000004000
00000000000
```
**Train 2 output**

```text
333
030
333
```
**Test input**

```text
00000000000
04440000000
04000000000
04400033000
00000030000
00000000000
```
**Test output**

```text
444
404
444
```
**Written solution:** Find the largest object, crop it to its own local coordinates, reflect it horizontally inside that local box, and take the union of original plus reflection. The result is a vertically symmetric version of the original object.

**Reference program:**

```python
def solve_S11_M5(grid):
    best = max(components(grid), key=lambda c: (len(c["cells"]), len(boundary_cells(c["cells"]))))
    pts = norm_cells(best["cells"])
    union = sorted(set(pts) | set(mirror_h_pts(pts)))
    rmax = max(r for r,c in union)
    cmax = max(c for r,c in union)
    out = blank(rmax+1, cmax+1, 0)
    for r,c in union:
        out[r][c] = best["color"]
    return out
```

## S11_M6 — Two-Panel XOR Mask

**Skills:** panel parsing, occupancy comparison, logical xor


**Scaffold:**

- Split the input at the vertical bar of 5s.

- Compare the left and right panels cell by cell as occupied vs empty.

- Output cyan(8) exactly where the two panels differ.


**Train 1 input**

```text
200050220
020050000
000050220
000050020
```
**Train 1 output**

```text
8880
0800
0880
0080
```

**Train 2 input**

```text
220050000
220050220
000050220
000050000
```
**Train 2 output**

```text
8800
8080
0880
0000
```
**Test input**

```text
220050000
020050220
000050020
000050000
```
**Test output**

```text
8800
0080
0080
0000
```
**Written solution:** Ignore the original colors and interpret non-zero as occupied. In the output panel, paint cyan(8) for cells occupied in exactly one of the two panels and leave cells black when both panels agree.

**Reference program:**

```python
def solve_S11_M6(grid):
    bars = split_by_vertical_bars(grid, 5)
    c = bars[0]
    left = [row[:c] for row in grid]
    right = [row[c+1:] for row in grid]
    h, w = dims(left)
    out = blank(h, w, 0)
    for r in range(h):
        for cc in range(w):
            if (left[r][cc] != 0) ^ (right[r][cc] != 0):
                out[r][cc] = 8
    return out
```

## S11_M7 — Area-Rank Recolor from Header

**Skills:** ranking, header legend, component recolor


**Scaffold:**

- Read the non-zero colors in the top row from left to right.

- Sort the body objects by area from smallest to largest.

- Recolor the objects using the header colors in that sorted order.


**Train 1 input**

```text
2003004000
0770000000
0770007770
0000007770
0000007770
0007700000
0007700000
```
**Train 1 output**

```text
2003004000
0220000000
0220004440
0000004440
0000004440
0003300000
0003300000
```

**Train 2 input**

```text
6002004000
0770000000
0000007770
0000007770
0007700000
0007700000
```
**Train 2 output**

```text
6002004000
0660000000
0000004440
0000004440
0002200000
0002200000
```
**Test input**

```text
3004006000
0770000000
0000007770
0000007770
0007700000
0000770000
0000000000
```
**Test output**

```text
3004006000
0330000000
0000006660
0000006660
0004400000
0000440000
0000000000
```
**Written solution:** The top row is a legend sequence. Rank the body objects by their cell counts, then assign the first legend color to the smallest object, the next to the middle one, and so on, keeping each object in place.

**Reference program:**

```python
def solve_S11_M7(grid):
    legend = [v for v in grid[0] if v != 0]
    out = copyg(grid)
    body = [row[:] for row in grid[1:]]
    comps = sorted(components(body), key=lambda c: (len(c["cells"]), c["cells"][0]))
    for comp, color in zip(comps, legend):
        for r,c in comp["cells"]:
            out[r+1][c] = color
    return out
```

# Hard

## S11_H1 — Nested Frame Fill by Container

**Skills:** nested frames, region ownership, multi-layer filling


**Scaffold:**

- Detect every rectangular frame and order them by size.

- For each empty cell, find the smallest frame that still contains it.

- Fill that cell with the color of its immediate container frame.


**Train 1 input**

```text
00000000000
02222222220
02000000020
02033333020
02030003020
02033333020
02000000020
02222222220
00000000000
```
**Train 1 output**

```text
00000000000
02222222220
02222222220
02233333220
02233333220
02233333220
02222222220
02222222220
00000000000
```

**Train 2 input**

```text
00000000000
04444444440
04666666640
04600000640
04603330640
04603030640
04603330640
04600000640
04666666640
04444444440
00000000000
```
**Train 2 output**

```text
00000000000
04444444440
04666666640
04666666640
04663336640
04663336640
04663336640
04666666640
04666666640
04444444440
00000000000
```
**Test input**

```text
00000000000
02222222220
02777777720
02700000720
02705550720
02705050720
02705550720
02700000720
02777777720
02222222220
00000000000
```
**Test output**

```text
00000000000
02222222220
02777777720
02777777720
02775557720
02775557720
02775557720
02777777720
02777777720
02222222220
00000000000
```
**Written solution:** This is a region-ownership task. Each black cell inside nested frames belongs to the smallest enclosing frame, not necessarily the outermost one. Fill each annulus with the color of the frame immediately surrounding it, and keep the frames themselves unchanged.

**Reference program:**

```python
def solve_S11_H1(grid):
    out = copyg(grid)
    frames = []
    for comp in components(grid):
        cells = comp["cells"]
        r1,c1,r2,c2 = bbox(cells)
        if set(cells) == set(rect_border(r1,c1,r2,c2)):
            frames.append(((r2-r1+1)*(c2-c1+1), (r1,c1,r2,c2), comp["color"]))
    frames.sort()
    h, w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 0:
                for _, (r1,c1,r2,c2), color in frames:
                    if r1 < r < r2 and c1 < c < c2:
                        out[r][c] = color
                        break
    return out
```

## S11_H2 — Rotation-Coded Boundary Stamps

**Skills:** template extraction, rotation codes, multiple placements


**Primitive note:** Uses boundary_cells to stamp the template's outline rather than its full fill.


**Scaffold:**

- Find the main template object in color 2.

- Treat cells 1, 3, 4, and 6 as anchor+rotation codes for 0°, 90°, 180°, and 270°.

- Stamp the rotated boundary of the template at each coded anchor in cyan(8).


**Train 1 input**

```text
02200010000
02000000040
02220000000
00000000000
00000030000
00000000000
```
**Train 1 output**

```text
00000088000
00000080088
00000088800
00000000008
00000088800
00000080800
```

**Train 2 input**

```text
022200001000
002000000000
002000000060
000000000000
000030000000
000000000000
000000000000
```
**Train 2 output**

```text
000000008880
000000000800
000000000880
000000000088
000000800080
000088800000
000000800000
```
**Test input**

```text
022200000000
020000000400
022000000000
000000100000
000000000000
000000000060
000000000000
```
**Test output**

```text
000000000000
000000000088
000000000008
000000888888
000000800000
000000880080
000000000080
```
**Written solution:** Extract the boundary of the color-2 template, normalize it, and rotate it according to the code value at each anchor cell. Then place the rotated boundary copy with its top-left corner at that coded cell. The output is a blank canvas containing only the stamped cyan(8) outlines.

**Reference program:**

```python
def solve_S11_H2(grid):
    code_to_rot = {1:0, 3:1, 4:2, 6:3}
    template = max([c for c in components(grid) if c["color"] == 2], key=lambda c: len(c["cells"]))
    pts = norm_cells(boundary_cells(template["cells"]))
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in code_to_rot:
                rot_pts = rotate_pts(pts, code_to_rot[v])
                for rr,cc in rot_pts:
                    nr, nc = r+rr, c+cc
                    if 0 <= nr < h and 0 <= nc < w:
                        out[nr][nc] = 8
    return out
```

## S11_H3 — Select by Hole Count

**Skills:** hole counting, component selection, normalized outline


**Scaffold:**

- Count the number of 1s in the top row.

- Choose the body object with exactly that many enclosed holes.

- Return a tight crop of its boundary, recolored to cyan(8).


**Train 1 input**

```text
100000000000000
220003330044444
220003030044004
000003330044444
000000000000000
```
**Train 1 output**

```text
888
808
888
```

**Train 2 input**

```text
110000000000000
220000000044444
220003330044004
000003030044444
000003330040004
000000000044444
```
**Train 2 output**

```text
88888
88008
88888
80008
88888
```
**Test input**

```text
110000000000000000
220000666000444440
220000606000400040
000000666000444440
000000000000400040
000000000000444440
```
**Test output**

```text
88888
80008
88888
80008
88888
```
**Written solution:** The header specifies a hole count. For each body component, count how many enclosed zero-regions lie inside it; then pick the object with the matching hole count. Output only that object's boundary as a normalized cyan(8) crop.

**Reference program:**

```python
def solve_S11_H3(grid):
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if hole_count_for_component(body, comp["cells"]) == k)
    return normalized_component_grid(body, best["cells"], use_boundary=True, recolor=8)
```

## S11_H4 — Find the Unpaired Shape Under Symmetry

**Skills:** shape canonicalization, dihedral equivalence, odd-one-out


**Scaffold:**

- Normalize each object by shape, ignoring color and position.

- Treat rotations and reflections as equivalent.

- All shapes occur in pairs except one; output the unpaired shape as a tight crop.


**Train 1 input**

```text
200003330000000
200003000000000
220000000000000
440000066000000
044000660000000
000000000000000
000000000077700
000000000007000
```
**Train 1 output**

```text
777
070
```

**Train 2 input**

```text
222000300000000
020003300000000
000000300000000
440000066000000
044000660000000
000000000007000
000000000007000
000000000007700
```
**Train 2 output**

```text
70
70
77
```
**Test input**

```text
200003330000000
200003000000000
220000000000000
444000060000000
040000660000000
000000060000000
000000000077000
000000000007700
```
**Test output**

```text
770
077
```
**Written solution:** Convert each component to a canonical shape signature under the full dihedral symmetry group. Most signatures appear twice; one appears only once. Output that unmatched component as a tight normalized crop.

**Reference program:**

```python
def solve_S11_H4(grid):
    sigs = defaultdict(list)
    for comp in components(grid):
        sigs[canonical_signature(comp["cells"])].append(comp)
    unmatched = [vals[0] for vals in sigs.values() if len(vals) == 1]
    best = unmatched[0]
    return normalized_component_grid(grid, best["cells"], use_boundary=True)
```

## S11_H5 — Translate and Split Boundary vs Interior

**Skills:** translation vectors, boundary/interior separation, constructive recolor


**Primitive note:** Uses boundary_cells to decide which translated cells become 7 and which become 8.


**Scaffold:**

- The vector from marker 1 to marker 2 tells you how far to move the main object.

- Translate the whole object by that vector.

- Paint translated boundary cells orange(7) and translated interior cells cyan(8).


**Train 1 input**

```text
000000000000
033330000000
033330000000
033330000000
000000000000
001000000000
000000000200
000000000000
000000000000
```
**Train 1 output**

```text
000000000000
000000000000
000000007777
000000007887
000000007777
000000000000
000000000000
000000000000
000000000000
```

**Train 2 input**

```text
000000000000
000444400000
000444400000
000444400000
000444400000
010000000000
000000200000
000000000000
000000000000
```
**Train 2 output**

```text
000000000000
000000000000
000000007777
000000007887
000000007887
000000007777
000000000000
000000000000
000000000000
```
**Test input**

```text
0000000000000
0000555500000
0000555500000
0000555500000
0000000000000
0010000000000
0000000020000
0000000000000
0000000000000
```
**Test output**

```text
0000000000000
0000000000000
0000000000777
0000000000788
0000000000777
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** Find the source and target markers and compute their offset. Move the main object by that offset, but do not preserve its old color: boundary cells become orange(7) while strictly interior cells become cyan(8). The output contains only the translated object.

**Reference program:**

```python
def solve_S11_H5(grid):
    h, w = dims(grid)
    src = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 1)
    dst = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2)
    comp = max([c for c in components(grid) if c["color"] not in (1,2)], key=lambda c: len(c["cells"]))
    bc = set(boundary_cells(comp["cells"]))
    dr, dc = dst[0]-src[0], dst[1]-src[1]
    out = blank(h, w, 0)
    for r,c in comp["cells"]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < h and 0 <= nc < w:
            out[nr][nc] = 7 if (r,c) in bc else 8
    return out
```

## S11_H6 — Dual Legend: Area and Boundary

**Skills:** multi-feature matching, header decoding, component selection


**Primitive note:** Uses boundary_cells together with raw area as a dual matching key.


**Scaffold:**

- Count the 1s in the header for the target area.

- Count the 2s in the header for the target boundary size.

- Choose the unique body object matching both and output it as a normalized cyan(8) crop.


**Train 1 input**

```text
1111111122222222
2200033300444400
2200030300444400
0000033300444400
```
**Train 1 output**

```text
888
808
888
```

**Train 2 input**

```text
1111111111112222222222
2200033300444400000000
2200030300444400000000
0000033300444400000000
```
**Train 2 output**

```text
8888
8888
8888
```
**Test input**

```text
1111222200000000
2200033300444400
2200030300444400
0000033300444400
```
**Test output**

```text
88
88
```
**Written solution:** This header specifies two independent features: total cells and boundary cells. Compute both values for each candidate object, find the one that matches both targets, and return that whole object as a tight crop recolored to cyan(8).

**Reference program:**

```python
def solve_S11_H6(grid):
    area = sum(1 for v in grid[0] if v == 1)
    bcount = sum(1 for v in grid[0] if v == 2)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if len(comp["cells"]) == area and len(boundary_cells(comp["cells"])) == bcount)
    return normalized_component_grid(body, best["cells"], use_boundary=False, recolor=8)
```

## S11_H7 — Common Shape Across Three Panels

**Skills:** panel parsing, shape equivalence, majority-by-form


**Scaffold:**

- Split the input into three panels at the two vertical bars of 5s.

- Normalize each panel's object up to rotation and reflection.

- Two panels contain the same shape family and one differs; output the common shape as a normalized cyan(8) crop.


**Train 1 input**

```text
20005333054440
20005300050400
22005000050000
00005000050000
00005000050000
```
**Train 1 output**

```text
888
800
```

**Train 2 input**

```text
22005033054000
02205330054000
00005000054400
00005000050000
00005000050000
```
**Train 2 output**

```text
880
088
```
**Test input**

```text
22205030054400
02005330050440
00005030050000
00005000050000
00005000050000
```
**Test output**

```text
888
080
```
**Written solution:** Compare the three panel objects by canonical shape under rotation/reflection. The majority signature is the common shape. Output that common form once, normalized and recolored to cyan(8).

**Reference program:**

```python
def solve_S11_H7(grid):
    bars = split_by_vertical_bars(grid, 5)
    c1, c2 = bars
    panels = [
        [row[:c1] for row in grid],
        [row[c1+1:c2] for row in grid],
        [row[c2+1:] for row in grid],
    ]
    sigs = []
    for p in panels:
        comp = max(components(p), key=lambda c: len(c["cells"]))
        sigs.append(canonical_signature(comp["cells"]))
    common_sig = Counter(sigs).most_common(1)[0][0]
    pts = list(common_sig)
    rmax = max(r for r,c in pts)
    cmax = max(c for r,c in pts)
    out = blank(rmax+1, cmax+1, 0)
    for r,c in pts:
        out[r][c] = 8
    return out
```
