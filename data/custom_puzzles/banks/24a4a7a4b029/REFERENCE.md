# ARC-style Puzzle Bank — 21 additional puzzles

This bank is organized into 7 easy, 7 medium, and 7 hard puzzles. Each entry includes what it probes, a scaffold, two train pairs, one test pair with solution, a written solution, and a compact Python reference program.

The reference programs assume the shared helpers in `arc_puzzle_bank_21_reference.py`.

## Index

### Easy

- **E1** — X-Shape Selector
- **E2** — Largest Blue Object
- **E3** — Border Survivors
- **E4** — Right-Hand Echo
- **E5** — Fill the Hollow Boxes
- **E6** — Plus Centers Only
- **E7** — Line Orientation Recolor

### Medium

- **M1** — Middle by Size
- **M2** — Corner Pair to Rectangle
- **M3** — Move Shape to Anchor
- **M4** — Inherit the Outer Color
- **M5** — Mirror Across Divider
- **M6** — Arms Around Valid Centers
- **M7** — Endpoint Bridge

### Hard

- **H1** — Template Stamping
- **H2** — Translate by Marker Vector
- **H3** — Bridge the Congruent Pair
- **H4** — Mirror from Sparse Axis Markers
- **H5** — Top-Strip Color Cycle
- **H6** — Rotate into the Hole
- **H7** — Count-Matched Object


# Easy

## E1 — X-Shape Selector

**Skills:** shape recognition, same-size recolor, 8-connectivity

**Scaffold:**
- Extract 8-connected green objects.
- Normalize each shape.
- Recolor only the ones whose normalized shape is an X-of-5.

**Train 1 input**
```text
0000000
0303000
0030000
0303000
0004000
0044400
0004000
```
**Train 1 output**
```text
0000000
0202000
0020000
0202000
0004000
0044400
0004000
```
**Train 2 input**
```text
30300000
03000000
30300000
00000400
00004440
00000400
00000000
```
**Train 2 output**
```text
20200000
02000000
20200000
00000400
00004440
00000400
00000000
```
**Test input**
```text
00000040
03030444
00300040
03030000
00000303
00000030
00000303
00000000
```
**Test output**
```text
00000040
02020444
00200040
02020000
00000202
00000020
00000202
00000000
```
**Written solution:** Find every green(3) object shaped like a 5-cell X (four diagonal arms plus the center). Recolor those cells red(2). Leave non-X green objects, such as pluses, unchanged.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    for comp in components(grid, include_colors={3}, connectivity=8):
        if normalize(comp["cells"]) == [(0,0),(0,2),(1,1),(2,0),(2,2)]:
            for r, c in comp["cells"]:
                out[r][c] = 2
    return out
```

## E2 — Largest Blue Object

**Skills:** component size ranking, object recolor

**Scaffold:**
- Find all blue(1) connected components.
- Rank them by size.
- Recolor only the largest component orange(7).

**Train 1 input**
```text
0000000000
0100000000
0110011111
0000000000
0000000000
0110000000
0110000000
0000000000
```
**Train 1 output**
```text
0000000000
0100000000
0110077777
0000000000
0000000000
0110000000
0110000000
0000000000
```
**Train 2 input**
```text
0000000000
0100000000
0100010000
0000111000
0000010000
0000000110
0000000110
0000000000
```
**Train 2 output**
```text
0000000000
0100000000
0100070000
0000777000
0000070000
0000000110
0000000110
0000000000
```
**Test input**
```text
00000000000
01111000000
00000000000
00000000000
00000001000
01000011100
01100001000
00000000000
00000000000
```
**Test output**
```text
00000000000
01111000000
00000000000
00000000000
00000007000
01000077700
01100007000
00000000000
00000000000
```
**Written solution:** Among all blue(1) objects, identify the largest connected component and recolor it orange(7). Keep the smaller blue objects unchanged.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid, include_colors={1})
    largest = max(comps, key=lambda comp: len(comp["cells"]))
    for r, c in largest["cells"]:
        out[r][c] = 7
    return out
```

## E3 — Border Survivors

**Skills:** border contact, component filtering

**Scaffold:**
- Find every non-black connected component.
- Test whether it touches the outer border.
- Keep border-touching components and erase the rest.

**Train 1 input**
```text
22000000
20000300
00000300
00000000
00004440
00000400
00000000
55500000
```
**Train 1 output**
```text
22000000
20000000
00000000
00000000
00000000
00000000
00000000
55500000
```
**Train 2 input**
```text
00000066
00300006
00300000
00000000
04444000
00400000
00000000
00000000
```
**Train 2 output**
```text
00000066
00000006
00000000
00000000
00000000
00000000
00000000
00000000
```
**Test input**
```text
70000000
77000000
00003300
00000300
00000000
00004440
00000000
00000008
```
**Test output**
```text
70000000
77000000
00000000
00000000
00000000
00000000
00000000
00000008
```
**Written solution:** Keep only the objects that touch at least one edge of the grid. Any object fully inside the grid is erased to black(0).

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    for comp in components(grid):
        if touches_border(comp["cells"], h, w):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out
```

## E4 — Right-Hand Echo

**Skills:** local directional paint, same-size transform

**Scaffold:**
- Scan for red(2) seed cells.
- For each seed, paint the cell immediately to its right blue(1) if it exists.
- Keep the original red seeds.

**Train 1 input**
```text
0000000
0200200
0000002
2000000
0002000
0000000
```
**Train 1 output**
```text
0000000
0210210
0000002
2100000
0002100
0000000
```
**Train 2 input**
```text
00000000
00200000
00000000
02000020
00002000
00000000
```
**Train 2 output**
```text
00000000
00210000
00000000
02100021
00002100
00000000
```
**Test input**
```text
20000000
00002000
00000002
00200020
00000000
00020000
```
**Test output**
```text
21000000
00002100
00000002
00210021
00000000
00021000
```
**Written solution:** Every red(2) cell writes a blue(1) copy one step to its right. The red cells stay where they are.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w - 1):
            if grid[r][c] == 2:
                out[r][c + 1] = 1
    return out
```

## E5 — Fill the Hollow Boxes

**Skills:** bbox reasoning, interior fill

**Scaffold:**
- Detect each rectangular ring.
- Compute its bounding box.
- Fill the interior with the same color as the outline.

**Train 1 input**
```text
000000000
044440000
040040000
044440000
000000000
000777700
000700700
000777700
000000000
```
**Train 1 output**
```text
000000000
044440000
044440000
044440000
000000000
000777700
000777700
000777700
000000000
```
**Train 2 input**
```text
0000000000
0666600000
0600600000
0600600000
0666600000
0000000000
0000444000
0000404000
0000444000
0000000000
```
**Train 2 output**
```text
0000000000
0666600000
0666600000
0666600000
0666600000
0000000000
0000444000
0000444000
0000444000
0000000000
```
**Test input**
```text
0000000000
0555550000
0500050000
0500050000
0555550000
0000000000
0000777700
0000700700
0000777700
0000000000
```
**Test output**
```text
0000000000
0555550000
0555550000
0555550000
0555550000
0000000000
0000777700
0000777700
0000777700
0000000000
```
**Written solution:** Each hollow rectangular outline becomes solid: fill all cells strictly inside the rectangle with the rectangle's own color.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    for comp in components(grid):
        r1, c1, r2, c2 = bbox(comp["cells"])
        for r in range(r1 + 1, r2):
            for c in range(c1 + 1, c2):
                out[r][c] = comp["color"]
    return out
```

## E6 — Plus Centers Only

**Skills:** local neighborhood test, center detection

**Scaffold:**
- Check each yellow(4) cell.
- A valid center has yellow neighbors in all four cardinal directions.
- Recolor only the center cell cyan(8).

**Train 1 input**
```text
004000000
044400000
004000000
000000000
000000400
000004440
000000400
444000000
```
**Train 1 output**
```text
004000000
048400000
004000000
000000000
000000400
000004840
000000400
444000000
```
**Train 2 input**
```text
000000004
000000004
000400004
004440000
000400000
040000000
444000000
040000000
000000000
```
**Train 2 output**
```text
000000004
000000004
000400004
004840000
000400000
040000000
484000000
040000000
000000000
```
**Test input**
```text
0000000004
0040000004
0444000004
0040000004
0000000400
0000004440
0000000400
0000000000
0000000000
```
**Test output**
```text
0000000004
0040000004
0484000004
0040000004
0000000400
0000004840
0000000400
0000000000
0000000000
```
**Written solution:** Find every yellow plus-shape. Recolor only its center cell to cyan(8), leaving the four yellow arms unchanged.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4 and all(
                0 <= r + dr < h and 0 <= c + dc < w and grid[r + dr][c + dc] == 4
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
            ):
                out[r][c] = 8
    return out
```

## E7 — Line Orientation Recolor

**Skills:** orientation, component bbox

**Scaffold:**
- Find each magenta(6) line object.
- If its bounding box is one row tall, it is horizontal; if one column wide, it is vertical.
- Horizontal lines become cyan(8), vertical lines become red(2).

**Train 1 input**
```text
000666000
000000000
006000060
006000060
006000060
000000000
000066660
```
**Train 1 output**
```text
000888000
000000000
002000020
002000020
002000020
000000000
000088880
```
**Train 2 input**
```text
0600000000
0600666600
0600000000
0000000000
0000060000
0000060000
0000060000
0000000000
```
**Train 2 output**
```text
0200000000
0200888800
0200000000
0000000000
0000020000
0000020000
0000020000
0000000000
```
**Test input**
```text
0000006600
0000000000
0666000000
0000000000
0006000600
0006000600
0006000600
0000000000
```
**Test output**
```text
0000008800
0000000000
0888000000
0000000000
0002000200
0002000200
0002000200
0000000000
```
**Written solution:** Recolor line objects by orientation: horizontal magenta(6) lines become cyan(8), while vertical magenta(6) lines become red(2).

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    for comp in components(grid, include_colors={6}):
        r1, c1, r2, c2 = bbox(comp["cells"])
        new_color = 8 if r1 == r2 else 2
        for r, c in comp["cells"]:
            out[r][c] = new_color
    return out
```


# Medium

## M1 — Middle by Size

**Skills:** ranking, component size ordering

**Scaffold:**
- Find the three blue(1) objects.
- Sort them by size.
- Recolor the median-sized object orange(7).

**Train 1 input**
```text
0000000000
0100000000
0110000100
0000001110
0000000100
0110000000
0110000000
0000000000
```
**Train 1 output**
```text
0000000000
0100000000
0110000100
0000001110
0000000100
0770000000
0770000000
0000000000
```
**Train 2 input**
```text
0000000000
0100001000
0100011100
0000001000
0000000000
0111100000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0100001000
0100011100
0000001000
0000000000
0777700000
0000000000
0000000000
```
**Test input**
```text
00000000000
01000000000
01000000100
00000001110
00000000100
01000000000
01100000000
00000000000
00000000000
```
**Test output**
```text
00000000000
01000000000
01000000100
00000001110
00000000100
07000000000
07700000000
00000000000
00000000000
```
**Written solution:** There are three blue objects of different sizes. Recolor the one in the middle by size orange(7); keep the smallest and largest blue.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid, include_colors={1})
    by_size = sorted(comps, key=lambda comp: len(comp["cells"]))
    target = by_size[len(by_size) // 2]
    for r, c in target["cells"]:
        out[r][c] = 7
    return out
```

## M2 — Corner Pair to Rectangle

**Skills:** corner inference, outline construction

**Scaffold:**
- Group same-colored singleton corners.
- Treat each pair as opposite corners of an axis-aligned rectangle.
- Draw the full rectangle outline in that color.

**Train 1 input**
```text
000000000
020000000
000000000
000000000
000000020
000000000
000300300
```
**Train 1 output**
```text
000000000
022222220
020000020
020000020
022222220
000000000
000333300
```
**Train 2 input**
```text
0000000000
0000000000
0400000040
0000000000
0000000000
0000500000
0000000000
0000000500
```
**Train 2 output**
```text
0000000000
0000000000
0444444440
0000000000
0000000000
0000555500
0000500500
0000555500
```
**Test input**
```text
00000000000
00060000000
00000000000
00000000000
00000000060
00000000000
00000000000
07000000000
00000000000
00000007000
```
**Test output**
```text
00000000000
00066666660
00060000060
00060000060
00066666660
00000000000
00000000000
07777777000
07000007000
07777777000
```
**Written solution:** Whenever two cells of the same color appear, they mark opposite corners of a rectangle. Draw the full axis-aligned rectangle outline connecting them.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    pos_by_color = {}
    for r in range(h):
        for c in range(w):
            color = grid[r][c]
            if color != 0:
                pos_by_color.setdefault(color, []).append((r, c))
    for color, pts in pos_by_color.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            r1, r2 = sorted((r1, r2))
            c1, c2 = sorted((c1, c2))
            for c in range(c1, c2 + 1):
                out[r1][c] = color
                out[r2][c] = color
            for r in range(r1, r2 + 1):
                out[r][c1] = color
                out[r][c2] = color
    return out
```

## M3 — Move Shape to Anchor

**Skills:** translation, object normalization, recolor on move

**Scaffold:**
- Find the anchor cell color 2 and the moving object color 3.
- Normalize the object's shape.
- Place it so its top-left cell sits one row down and one column right of the anchor, recolored to 2.

**Train 1 input**
```text
000000000
020000000
000000000
000000000
000003000
000003300
000000000
000000000
```
**Train 1 output**
```text
000000000
000000000
002000000
002200000
000000000
000000000
000000000
000000000
```
**Train 2 input**
```text
0000020000
0000000000
0000000000
0000000000
0333000000
0030000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000002220
0000000200
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Test input**
```text
00000000000
00000000000
00000002000
00000000000
00000000000
03300000000
03300000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000000000
00000000000
00000000220
00000000220
00000000000
00000000000
00000000000
00000000000
```
**Written solution:** Take the color-3 object, erase it from its old location, and redraw the same shape in color 2 so that its bounding box starts one step down-right from the color-2 anchor.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    anchor = next((r, c) for r in range(h) for c in range(w) if grid[r][c] == 2)
    obj = max(components(grid, include_colors={3}), key=lambda comp: len(comp["cells"]))
    top, left = anchor[0] + 1, anchor[1] + 1
    for dr, dc in normalize(obj["cells"]):
        out[top + dr][left + dc] = 2
    return out
```

## M4 — Inherit the Outer Color

**Skills:** containment, bbox nesting, recolor by enclosure

**Scaffold:**
- Detect rectangular frame objects.
- Find smaller objects strictly inside each frame's bbox.
- Recolor each inner object to the frame's color.

**Train 1 input**
```text
000000000000
044444007777
040304007007
044444007307
000000007777
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
044444007777
040404007007
044444007707
000000007777
000000000000
000000000000
000000000000
```
**Train 2 input**
```text
000000000000
066660000000
063060000000
060060000000
066660022222
000000020302
000000020002
030000022222
000000000000
```
**Train 2 output**
```text
000000000000
066660000000
066060000000
060060000000
066660022222
000000020202
000000020002
030000022222
000000000000
```
**Test input**
```text
0000000000000
0888880000000
0803080055550
0803080053050
0800080050050
0888880055550
0000000000000
0000000000300
0000000000000
```
**Test output**
```text
0000000000000
0888880000000
0808080055550
0808080055050
0800080050050
0888880055550
0000000000000
0000000000300
0000000000000
```
**Written solution:** Any object sitting inside a hollow rectangle inherits the rectangle's color. The rectangle itself stays unchanged, and outside objects stay as they are.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    rings = [comp for comp in comps if is_rectangle_outline(comp)]
    others = [comp for comp in comps if not is_rectangle_outline(comp)]
    for obj in others:
        r1, c1, r2, c2 = bbox(obj["cells"])
        for ring in rings:
            R1, C1, R2, C2 = bbox(ring["cells"])
            if R1 < r1 and r2 < R2 and C1 < c1 and c2 < C2:
                for r, c in obj["cells"]:
                    out[r][c] = ring["color"]
                break
    return out
```

## M5 — Mirror Across Divider

**Skills:** explicit reference frame, reflection

**Scaffold:**
- Find the full-height divider column of color 5.
- Reflect every non-divider object cell across that vertical axis.
- Keep both the original and its mirror copy.

**Train 1 input**
```text
000500000
030500000
033500000
000500000
000500000
000500000
000500000
```
**Train 1 output**
```text
000500000
030503000
033533000
000500000
000500000
000500000
000500000
```
**Train 2 input**
```text
0000500000
0000500400
0000504400
0000500000
0000500000
0000500000
0000500000
```
**Train 2 output**
```text
0000500000
0400500400
0440504400
0000500000
0000500000
0000500000
0000500000
```
**Test input**
```text
00000500000
00000500000
00000533000
00000503000
00000500000
00000500000
00000500000
00000500000
```
**Test output**
```text
00000500000
00000500000
00033533000
00030503000
00000500000
00000500000
00000500000
00000500000
```
**Written solution:** The solid color-5 column is a mirror axis. Copy every object to the opposite side by horizontal reflection across that divider.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    divider = next(c for c in range(w) if all(grid[r][c] == 5 for r in range(h)))
    for r in range(h):
        for c in range(w):
            if grid[r][c] not in (0, 5):
                out[r][2 * divider - c] = grid[r][c]
    return out
```

## M6 — Arms Around Valid Centers

**Skills:** derived intermediate grid, two-pass local reasoning

**Scaffold:**
- Detect color-4 centers whose four cardinal neighbors are all color 7.
- Once centers are known, recolor just those four neighboring arm cells to color 8.
- Leave everything else unchanged.

**Train 1 input**
```text
000000070
007000777
074700070
007000000
000000700
000007470
000000700
000000000
```
**Train 1 output**
```text
000000070
008000777
084800070
008000000
000000800
000008480
000000800
000000000
```
**Train 2 input**
```text
0700000000
7770000000
0707000000
0074700000
0007000000
0000000700
0000007470
0000000700
0000000000
```
**Train 2 output**
```text
0700000000
7770000000
0708000000
0084800000
0008000000
0000000800
0000008480
0000000800
0000000000
```
**Test input**
```text
0000000000
0000000700
0000007470
0000000700
0000077700
0070000000
0747000000
0070000000
0000000000
```
**Test output**
```text
0000000000
0000000800
0000008480
0000000800
0000077700
0080000000
0848000000
0080000000
0000000000
```
**Written solution:** A valid pattern is a color-4 center surrounded by four color-7 arms. Recolor the arms to color 8, but keep the center at color 4.

**Reference program:**
```python
def solve(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4 and all(
                0 <= rr < h and 0 <= cc < w and grid[rr][cc] == 7
                for rr, cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            ):
                for rr, cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    out[rr][cc] = 8
    return out
```

## M7 — Endpoint Bridge

**Skills:** pairing, line drawing, alignment

**Scaffold:**
- For each color that appears exactly twice, check whether the two cells are aligned horizontally or vertically.
- Draw the straight line segment between them in the same color.
- Keep the endpoints.

**Train 1 input**
```text
000000000
020000020
000000000
000300000
000000000
000300000
000000000
000000000
```
**Train 1 output**
```text
000000000
022222220
000000000
000300000
000300000
000300000
000000000
000000000
```
**Train 2 input**
```text
0000000000
0000000000
0400000000
0000000000
0400000000
0000000000
0000550000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0400000000
0400000000
0400000000
0000000000
0000550000
0000000000
```
**Test input**
```text
00000000000
00000000000
00000600000
00000000000
00000600000
00000000000
07000000007
00000000000
```
**Test output**
```text
00000000000
00000000000
00000600000
00000600000
00000600000
00000000000
07777777777
00000000000
```
**Written solution:** Two matching endpoints define a segment. Fill the whole horizontal or vertical span between them with that same color.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    pos_by_color = {}
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                pos_by_color.setdefault(color, []).append((r, c))
    for color, pts in pos_by_color.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            if r1 == r2 or c1 == c2:
                for r, c in line_cells(r1, c1, r2, c2):
                    out[r][c] = color
    return out
```


# Hard

## H1 — Template Stamping

**Skills:** template extraction, shape normalization, copy at markers

**Scaffold:**
- Find the largest color-3 object and treat it as the template.
- Normalize its shape.
- At every non-3 singleton marker, stamp a copy of that template in the marker's own color, using the marker as the top-left anchor.

**Train 1 input**
```text
000000001000
030000000000
033000000000
000000000000
000000000000
000000020000
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000001000
030000001100
033000000000
000000000000
000000000000
000000020000
000000022000
000000000000
000000000000
```
**Train 2 input**
```text
000000000000
003330000000
000300000000
000000000000
000000006000
040000000000
000000000000
000000000000
000000000000
```
**Train 2 output**
```text
000000000000
003330000000
000300000000
000000000000
000000006660
044400000600
004000000000
000000000000
000000000000
```
**Test input**
```text
0000000002000
0330000000000
0033000000000
0000000000000
0000000000000
0000000000000
0000000800000
0040000000000
0000000000000
0000000000000
```
**Test output**
```text
0000000002200
0330000000220
0033000000000
0000000000000
0000000000000
0000000000000
0000000880000
0044000088000
0004400000000
0000000000000
```
**Written solution:** Use the largest color-3 object as a template. Copy that exact shape at each single-cell marker, coloring each copy with the marker's color.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    template = max([c for c in comps if c["color"] == 3], key=lambda comp: len(comp["cells"]))
    shape = normalize(template["cells"])
    for comp in comps:
        if len(comp["cells"]) == 1 and comp["color"] != 3:
            r0, c0 = comp["cells"][0]
            for dr, dc in shape:
                out[r0 + dr][c0 + dc] = comp["color"]
    return out
```

## H2 — Translate by Marker Vector

**Skills:** vector inference, object translation, cross-object relation

**Scaffold:**
- Read the vector from the color-1 marker to the color-2 marker.
- Find the color-3 object.
- Copy that object by the same vector and paint the translated copy color 2.

**Train 1 input**
```text
000000000000
010000000000
000000000000
000020000000
000000000000
033300000000
003000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
010000000000
000000000000
000020000000
000000000000
033300000000
003000000000
000022200000
000002000000
```
**Train 2 input**
```text
001000000000
000000000000
000000020000
000000000000
030000000000
033000000000
000000000000
000000000000
000000000000
```
**Train 2 output**
```text
001000000000
000000000000
000000020000
000000000000
030000000000
033000000000
000000200000
000000220000
000000000000
```
**Test input**
```text
0000000000000
0000000330000
0100000330000
0000000000000
0000000000000
0000020000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0000000330000
0100000330000
0000000000000
0000000000022
0000020000022
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution:** The color-1 and color-2 cells define a translation vector. Apply that same displacement to the color-3 object and draw the translated copy in color 2.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    p1 = next((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 1)
    p2 = next((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 2)
    dr, dc = p2[0] - p1[0], p2[1] - p1[1]
    obj = max(components(grid, include_colors={3}), key=lambda comp: len(comp["cells"]))
    for r, c in obj["cells"]:
        out[r + dr][c + dc] = 2
    return out
```

## H3 — Bridge the Congruent Pair

**Skills:** shape matching, pair selection, relational drawing

**Scaffold:**
- Extract all objects and normalize their shapes.
- Find the pair with identical shape signatures.
- Draw a straight color-8 bridge between the two matching objects along their shared row-span or column-span.

**Train 1 input**
```text
000000000000
030000040000
033000044000
000000000000
000000000000
000022000000
000022000000
000000000000
```
**Train 1 output**
```text
000000000000
038888880000
033000044000
000000000000
000000000000
000022000000
000022000000
000000000000
```
**Train 2 input**
```text
0000000000
0066600000
0006000000
0000000400
0000000400
0000000000
0033300000
0003000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0066600000
0008000000
0008000400
0008000400
0008000000
0038300000
0003000000
0000000000
0000000000
```
**Test input**
```text
0000000000000
0000000000000
0770000022000
0077000002200
0000000000000
0000000000000
0000044000000
0000044000000
0000000000000
```
**Test output**
```text
0000000000000
0000000000000
0778888882000
0077000002200
0000000000000
0000000000000
0000044000000
0000044000000
0000000000000
```
**Written solution:** Among all objects, locate the two congruent ones. Then connect them with a straight color-8 bridge running between the matching pair.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    by_shape = {}
    for comp in comps:
        by_shape.setdefault(tuple(normalize(comp["cells"])), []).append(comp)
    a, b = next(lst[:2] for lst in by_shape.values() if len(lst) >= 2)
    a_r1, a_c1, a_r2, a_c2 = bbox(a["cells"])
    b_r1, b_c1, b_r2, b_c2 = bbox(b["cells"])
    if a_r1 == b_r1 and a_r2 == b_r2:
        row = (a_r1 + a_r2) // 2
        left = min(a_c2, b_c2)
        right = max(a_c1, b_c1)
        for c in range(left, right + 1):
            out[row][c] = 8
    else:
        col = (a_c1 + a_c2) // 2
        top = min(a_r2, b_r2)
        bottom = max(a_r1, b_r1)
        for r in range(top, bottom + 1):
            out[r][col] = 8
    return out
```

## H4 — Mirror from Sparse Axis Markers

**Skills:** implicit axis inference, reflection, sparse cues

**Scaffold:**
- Find the two color-5 axis markers.
- Infer the mirror column from their shared x-position.
- Reflect every non-marker object across that implicit vertical axis.

**Train 1 input**
```text
00000500000
00000000000
03330000000
00300000000
00000000000
00400000000
00440000000
00000500000
```
**Train 1 output**
```text
00000500000
00000000000
03330003330
00300000300
00000000000
00400000400
00440004400
00000500000
```
**Train 2 input**
```text
0000005000000
0000000000000
0770000000000
0077000000000
0000000000000
0000000000000
0002000000000
0002000000000
0000005000000
```
**Train 2 output**
```text
0000005000000
0000000000000
0770000000770
0077000007700
0000000000000
0000000000000
0002000002000
0002000002000
0000005000000
```
**Test input**
```text
0000500000000
0000000000000
6000000000000
6600000000000
0000000000000
0000000000000
0333300000000
0000000000000
0000500000000
```
**Test output**
```text
0000500000000
0000000000000
6000000060000
6600000660000
0000000000000
0000000000000
0333333300000
0000000000000
0000500000000
```
**Written solution:** The two color-5 marker cells indicate a vertical mirror axis even though the axis is not drawn as a full line. Reflect every object across that inferred column.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    markers = [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 5]
    axis = markers[0][1]
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v not in (0, 5):
                out[r][2 * axis - c] = v
    return out
```

## H5 — Top-Strip Color Cycle

**Skills:** meta-rule from strip, dynamic color mapping

**Scaffold:**
- Read the ordered nonzero colors in the top row.
- Build a cyclic mapping from each strip color to the next one.
- Apply that recoloring to all objects below the strip while leaving the strip unchanged.

**Train 1 input**
```text
020407000
000000000
022000000
002000440
000000400
000770000
000700000
```
**Train 1 output**
```text
020407000
000000000
044000000
004000770
000000700
000220000
000200000
```
**Train 2 input**
```text
0609020000
0000000000
0060000000
0060009900
0000009000
0002200000
0002000000
```
**Train 2 output**
```text
0609020000
0000000000
0090000000
0090002200
0000002000
0006600000
0006000000
```
**Test input**
```text
08030500000
00000000000
00880000000
00080033300
00000030000
00000550000
00000050000
```
**Test output**
```text
08030500000
00000000000
00330000000
00030055500
00000050000
00000880000
00000080000
```
**Written solution:** The top strip defines a cyclic color map. Every object below the strip changes to the next color in that strip order.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    strip = [v for v in grid[0] if v != 0]
    mapping = {strip[i]: strip[(i + 1) % len(strip)] for i in range(len(strip))}
    for r in range(1, len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in mapping:
                out[r][c] = mapping[grid[r][c]]
    return out
```

## H6 — Rotate into the Hole

**Skills:** rotation, placement into container, erase-and-reuse object

**Scaffold:**
- Find the color-3 source object and the hollow rectangle.
- Rotate the source object 90° clockwise.
- Erase it from its original location and place the rotated version in the top-left corner of the rectangle's interior.

**Train 1 input**
```text
0000000000
0300000000
0330000000
0000077770
0000070070
0000070070
0000077770
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0000077770
0000073370
0000073070
0000077770
0000000000
```
**Train 2 input**
```text
000000000000
003000000000
003000000000
000000000000
000000066660
000000060060
000000060060
000000066660
000000000000
```
**Train 2 output**
```text
000000000000
000000000000
000000000000
000000000000
000000066660
000000063360
000000060060
000000066660
000000000000
```
**Test input**
```text
000000000000
033000000000
003300000000
000000000000
000000000000
000000888880
000000800080
000000800080
000000888880
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000888880
000000803080
000000833080
000000838880
000000000000
```
**Written solution:** Take the color-3 object, rotate it clockwise, remove it from where it started, and place the rotated shape inside the hollow box anchored at the box's top-left interior cell.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    obj = max([c for c in comps if c["color"] == 3], key=lambda comp: len(comp["cells"]))
    ring = max([c for c in comps if c["color"] != 3 and is_rectangle_outline(c)],
               key=lambda comp: len(comp["cells"]))
    for r, c in obj["cells"]:
        out[r][c] = 0
    r1, c1, r2, c2 = bbox(ring["cells"])
    for dr, dc in rotate_cells_90(obj["cells"]):
        out[r1 + 1 + dr][c1 + 1 + dc] = 3
    return out
```

## H7 — Count-Matched Object

**Skills:** counting, size comparison, cross-region dependency

**Scaffold:**
- Count how many color-1 marker cells appear in the top row.
- Find the color-3 object whose size matches that count.
- Erase the markers and recolor only the size-matching object to color 8.

**Train 1 input**
```text
0111000000
0000000000
0300030000
0300033000
0000000000
0000000330
0000000330
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0300080000
0300088000
0000000000
0000000330
0000000330
0000000000
```
**Train 2 input**
```text
111100000000
000000000000
030000000000
033000330000
000000330000
000000000000
000300000000
003330000000
000300000000
```
**Train 2 output**
```text
000000000000
000000000000
030000000000
033000880000
000000880000
000000000000
000300000000
003330000000
000300000000
```
**Test input**
```text
001100000000
000000000000
030000000000
030000330000
000000330000
000000000000
000000003000
000000003300
000000000000
```
**Test output**
```text
000000000000
000000000000
080000000000
080000330000
000000330000
000000000000
000000003000
000000003300
000000000000
```
**Written solution:** The number of top-row marker cells tells you which object to select: recolor the color-3 object whose area equals that count, and remove the markers.

**Reference program:**
```python
def solve(grid):
    out = [row[:] for row in grid]
    target_size = sum(1 for v in grid[0] if v == 1)
    for c in range(len(grid[0])):
        if out[0][c] == 1:
            out[0][c] = 0
    for comp in components(grid, include_colors={3}):
        if len(comp["cells"]) == target_size:
            for r, c in comp["cells"]:
                out[r][c] = 8
    return out
```
