# 21 More ARC-Style Puzzles

This is the eighth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E50–E56, M50–M56, H50–H56**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans harder into legend-based painting, geometric completion, prototype stamping, frame-centered placement, panel composition, analogy-by-transform, header-driven reconstruction, and symmetry-coded reuse.

**New motifs in this batch**

**`orbit_union(pivot, prototype)`** — treat a single anchored prototype as relative offsets and union together its 0° / 90° / 180° / 270° copies around the same pivot. This is most visible in **H50**.

**`mask_and_carry(mask, payload)`** — use one structure only as geometry and another only as content, then compose them. This is the main idea in **H51**.

**`prototype_lookup(prototypes, query)`** — compare a query shape against labeled prototypes up to symmetry, then transfer the matched label. This shows up in **H55**.

## Easy

### E50 — Column legend painter

**What it tests:** Read a color key from the top row and apply it column-wise to marker cells.

**Staged hint:** Ignore everything except the top-row keys and the 8-markers underneath them.

**Train 1 — input**

```text
0200400
0000000
0800800
0000000
0800000
0000800
6000000
```

**Train 1 — output**

```text
0200400
0000000
0200400
0000000
0200000
0000400
6000000
```

**Train 2 — input**

```text
00300060
00800000
00000000
50000000
00000080
00000000
00800080
00000000
```

**Train 2 — output**

```text
00300060
00300000
00000000
50000000
00000060
00000000
00300060
00000000
```

**Test — input**

```text
050200700
000000000
080000800
000000000
000800000
000000000
080800000
000000800
000000004
```

**Test — expected output**

```text
050200700
000000000
050000700
000000000
000200000
000000000
050200000
000000700
000000004
```

**Written solution**

Treat the top row as a legend. In every column whose top cell is nonzero, replace each body cell equal to 8 with that column's legend color. Leave all other cells alone.

**Reference program (`solve_E50`)**

```python
def solve_E50(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for c in range(w):
        key = g[0][c]
        if key == 0:
            continue
        for r in range(1,h):
            if g[r][c] == 8:
                out[r][c] = key
    return out
```

### E51 — Vertical midpoint bridge

**What it tests:** Notice same-color cells two rows apart and repair the one missing middle cell.

**Staged hint:** Scan column by column for a color, a gap, and the same color again.

**Train 1 — input**

```text
0000040
0300000
0000040
0300000
0007000
0000000
0007002
```

**Train 1 — output**

```text
0000040
0300040
0300040
0300000
0007000
0007000
0007002
```

**Train 2 — input**

```text
20000000
00000050
20600000
00000050
00600000
00000000
00000000
00000009
```

**Train 2 — output**

```text
20000000
20000050
20600050
00600050
00600000
00000000
00000000
00000009
```

**Test — input**

```text
000030000
070000000
000030000
070000000
000000050
000200000
000000050
000200000
000000000
```

**Test — expected output**

```text
000030000
070030000
070030000
070000000
000000050
000200050
000200050
000200000
000000000
```

**Written solution**

Whenever two identical nonzero cells appear in the same column with exactly one empty cell between them, fill that middle cell with the same color.

**Reference program (`solve_E51`)**

```python
def solve_E51(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-2):
        for c in range(w):
            if g[r][c] != 0 and g[r][c] == g[r+2][c] and g[r+1][c] == 0:
                out[r+1][c] = g[r][c]
    return out
```

### E52 — Diagonal midpoint bridge

**What it tests:** Detect diagonal endpoints with one empty center and fill the missing midpoint.

**Staged hint:** Look inside every 3x3 window; the center matters only when opposite corners match.

**Train 1 — input**

```text
0000400
0200000
0040000
0002000
7000000
0000060
0070000
```

**Train 1 — output**

```text
0000400
0204000
0040000
0002000
7000000
0700060
0070000
```

**Train 2 — input**

```text
03000000
00000050
00030000
00005000
00006000
02000000
00000060
00020000
```

**Train 2 — output**

```text
03000000
00300050
00030500
00005000
00006000
02000600
00200060
00020000
```

**Test — input**

```text
004000000
000000060
000040000
000006000
030000000
000000002
000300000
000000200
000000000
```

**Test — expected output**

```text
004000000
000400060
000040600
000006000
030000000
003000002
000300020
000000200
000000000
```

**Written solution**

In any 3-cell diagonal run, if the two endpoints have the same nonzero color and the middle cell is 0, fill that middle cell with the endpoint color. Do this for both diagonal directions.

**Reference program (`solve_E52`)**

```python
def solve_E52(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c] != 0 and g[r][c] == g[r+2][c+2] and g[r+1][c+1] == 0:
                out[r+1][c+1] = g[r][c]
            if g[r][c+2] != 0 and g[r][c+2] == g[r+2][c] and g[r+1][c+1] == 0:
                out[r+1][c+1] = g[r][c+2]
    return out
```

### E53 — Vertical mirror overlay

**What it tests:** Apply a whole-grid vertical reflection without deleting the original shape.

**Staged hint:** Every nonzero cell should also appear at its vertically mirrored row.

**Train 1 — input**

```text
0200000
0220000
0000400
0000000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0200000
0220000
0000400
0000000
0000400
0220000
0200000
```

**Train 2 — input**

```text
33000000
30000000
00000600
00000660
00000000
00000000
00000000
00000000
```

**Train 2 — output**

```text
33000000
30000000
00000600
00000660
00000660
00000600
30000000
33000000
```

**Test — input**

```text
005000000
005500000
000000700
000000770
000040000
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
005000000
005500000
000000700
000000770
000040000
000000770
000000700
005500000
005000000
```

**Written solution**

Copy each nonzero cell to the cell reflected across the horizontal midline of the grid. Keep the original cells too, so the result is the union of the shape and its vertical mirror.

**Reference program (`solve_E53`)**

```python
def solve_E53(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[h-1-r][c] = g[r][c]
    return out
```

### E54 — Diagonal pair to square

**What it tests:** Recognize a 2x2 square from just its diagonal pair and complete the block.

**Staged hint:** Work one 2x2 window at a time. If only a same-color diagonal is present, fill the other diagonal.

**Train 1 — input**

```text
0000060
0200600
0020000
0000000
0000400
0000040
0000000
```

**Train 1 — output**

```text
0000660
0220660
0220000
0000000
0000440
0000440
0000000
```

**Train 2 — input**

```text
50000000
05000000
03000000
00300000
00000700
00007000
00000000
00000000
```

**Train 2 — output**

```text
55000000
55000000
03300000
03300000
00007700
00007700
00000000
00000000
```

**Test — input**

```text
300000000
030000200
000002000
040000000
004000000
000000700
000000070
000000000
000000000
```

**Test — expected output**

```text
330000000
330002200
000002200
044000000
044000000
000000770
000000770
000000000
000000000
```

**Written solution**

Inside any 2x2 block, if one diagonal contains two identical nonzero cells and the other two cells are empty, fill the empty cells to make the entire 2x2 block that color.

**Reference program (`solve_E54`)**

```python
def solve_E54(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-1):
        for c in range(w-1):
            a,b = g[r][c], g[r][c+1]
            d,e = g[r+1][c], g[r+1][c+1]
            if a != 0 and a == e and b == 0 and d == 0:
                out[r][c+1] = a
                out[r+1][c] = a
            if b != 0 and b == d and a == 0 and e == 0:
                out[r][c] = b
                out[r+1][c+1] = b
    return out
```

### E55 — Column gravity down

**What it tests:** Treat each column independently and let the nonzero cells fall to the bottom.

**Staged hint:** Do not mix columns. Just collect each column's colors in order and restack them at the bottom.

**Train 1 — input**

```text
200070
004000
300000
005000
000080
006000
```

**Train 1 — output**

```text
000000
000000
000000
004000
205070
306080
```

**Train 2 — input**

```text
0200000
0000060
0305000
0400000
0000070
0000000
0000000
```

**Train 2 — output**

```text
0000000
0000000
0000000
0000000
0200000
0300060
0405070
```

**Test — input**

```text
20000300
00500000
00000800
40000000
00600000
00000009
00700000
00000000
```

**Test — expected output**

```text
00000000
00000000
00000000
00000000
00000000
00500000
20600300
40700809
```

**Written solution**

For each column, read the nonzero cells from top to bottom, then drop them to the bottom of that same column while preserving their order.

**Reference program (`solve_E55`)**

```python
def solve_E55(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for c in range(w):
        vals = [g[r][c] for r in range(h) if g[r][c] != 0]
        for i,v in enumerate(vals):
            out[h-len(vals)+i][c] = v
    return out
```

### E56 — Single-cell hole fill

**What it tests:** Spot exact 3x3 rings and fill only their missing center cell.

**Staged hint:** Check the eight neighbors around each zero cell. If they are all the same nonzero color, fill the center.

**Train 1 — input**

```text
0000000
0222000
0202000
0222444
0000404
0000444
0000000
```

**Train 1 — output**

```text
0000000
0222000
0222000
0222444
0000444
0000444
0000000
```

**Train 2 — input**

```text
00000000
00005550
00005050
00005550
06660000
06060000
06660000
00000000
```

**Train 2 — output**

```text
00000000
00005550
00005550
00005550
06660000
06660000
06660000
00000000
```

**Test — input**

```text
000000002
033300000
030300000
033300000
000007770
000007070
000007770
000000000
000000000
```

**Test — expected output**

```text
000000002
033300000
033300000
033300000
000007770
000007770
000007770
000000000
000000000
```

**Written solution**

Whenever a 0 cell is surrounded on all eight sides by the same nonzero color, fill that center with the surrounding color.

**Reference program (`solve_E56`)**

```python
def solve_E56(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            ring = [g[r+dr][c+dc] for dr in (-1,0,1) for dc in (-1,0,1) if not (dr==0 and dc==0)]
            if g[r][c] == 0 and len(set(ring)) == 1 and ring[0] != 0:
                out[r][c] = ring[0]
    return out
```

## Medium

### M50 — Keep the largest component of each color

**What it tests:** Segment by color and compare component sizes within each color class.

**Staged hint:** Do not compare red objects to blue ones. Decide 'largest' separately for each color.

**Train 1 — input**

```text
00000022
02000000
02000400
02200000
00000660
04400060
04400000
00000000
```

**Train 1 — output**

```text
00000000
02000000
02000000
02200000
00000660
04400060
04400000
00000000
```

**Train 2 — input**

```text
000000007
033300000
003000000
003000000
000000000
000077000
000007700
055000030
050000030
```

**Train 2 — output**

```text
000000000
033300000
003000000
003000000
000000000
000077000
000007700
055000000
050000000
```

**Test — input**

```text
6000000000
0000200000
0002220000
0000200000
0000000400
0600000440
0660000000
0060000000
0000000022
0000000000
```

**Test — expected output**

```text
0000000000
0000200000
0002220000
0000200000
0000000400
0600000440
0660000000
0060000000
0000000000
0000000000
```

**Written solution**

Find all connected components, grouped by color. For each color independently, keep only its largest component and remove the smaller components of that same color.

**Reference program (`solve_M50`)**

```python
def solve_M50(g: Grid) -> Grid:
    comps = same_color_components(g)
    best = {}
    for col,cells in comps:
        best[col] = max(best.get(col, 0), len(cells))
    out = blank(*dims(g))
    for col,cells in comps:
        if len(cells) == best[col]:
            for r,c in cells:
                out[r][c] = col
    return out
```

### M51 — Prototype stamp at anchor dots

**What it tests:** Extract one object, normalize it, and place copies at several target anchor cells.

**Staged hint:** First isolate the one real object. Then reuse its top-left-normalized shape at each 1-cell.

**Train 1 — input**

```text
30000100
33000000
00000000
00000000
00001000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000300
00000330
00000000
00000000
00003000
00003300
00000000
00000000
```

**Train 2 — input**

```text
060000000
666000000
000000000
000000000
000001000
000000000
010000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000000600
000006660
006000000
066600000
000000000
```

**Test — input**

```text
7700000000
0770000000
0000000000
0000010000
0000000000
0000000000
1000000000
0000001000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000000000
0000077000
0000007700
0000000000
7700000000
0770007700
0000000770
0000000000
```

**Written solution**

Treat the largest non-anchor object as the prototype. Normalize its shape to its own top-left corner, then stamp that same shape at every anchor cell colored 1. The output contains only those stamped copies.

**Reference program (`solve_M51`)**

```python
def solve_M51(g: Grid) -> Grid:
    h,w = dims(g)
    anchors = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 1]
    comps = [(col,cells) for col,cells in same_color_components(g) if col != 1]
    col,cells = max(comps, key=lambda t: len(t[1]))
    shape,_,_ = normalize(cells)
    out = blank(h,w)
    for ar,ac in anchors:
        for dr,dc in shape:
            rr,cc = ar+dr, ac+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = col
    return out
```

### M52 — Turn each object into its bounding-box border

**What it tests:** Move from raw object pixels to an object-level abstraction: the bounding box.

**Staged hint:** Ignore the interior geometry after you find each component. Only its min/max rows and columns matter.

**Train 1 — input**

```text
00000000
02000000
02000000
02200000
00000400
00000440
00000040
00000000
```

**Train 1 — output**

```text
00000000
02200000
02200000
02200000
00000440
00000440
00000440
00000000
```

**Train 2 — input**

```text
000000300
000000300
000000333
000000000
000000000
077000000
007000000
007000000
000000000
```

**Train 2 — output**

```text
000000333
000000303
000000333
000000000
000000000
077000000
077000000
077000000
000000000
```

**Test — input**

```text
0000000000
0050000000
0050000000
0055500000
0000000000
0000008000
0000008800
0000000800
0000000800
0000000000
```

**Test — expected output**

```text
0000000000
0055500000
0050500000
0055500000
0000000000
0000008800
0000008800
0000008800
0000008800
0000000000
```

**Written solution**

For every connected component, compute its bounding box and draw only the border of that rectangle in the component's own color. Discard the original interior shape.

**Reference program (`solve_M52`)**

```python
def solve_M52(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        r0,r1,c0,c1 = bbox(cells)
        for r in range(r0,r1+1):
            out[r][c0] = col
            out[r][c1] = col
        for c in range(c0,c1+1):
            out[r0][c] = col
            out[r1][c] = col
    return out
```

### M53 — Keep only the object with a true hole

**What it tests:** Distinguish between ordinary empty space in a bounding box and an actually enclosed hole.

**Staged hint:** Do not use the box alone. Ask whether a zero region is trapped away from the box boundary.

**Train 1 — input**

```text
000000000
022200444
020200040
022200040
000000000
000000000
000006600
000006600
000000000
```

**Train 1 — output**

```text
000000000
022200000
020200000
022200000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000300
0000000300
0055550330
0050050000
0050050000
0055550000
0000000000
0770000000
0070000000
0070000000
```

**Train 2 — output**

```text
0000000000
0000000000
0055550000
0050050000
0050050000
0055550000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
0000000000
0000888800
0000800800
0000800800
0000888800
0000000000
0200000000
0220000040
0000000440
0000000000
```

**Test — expected output**

```text
0000000000
0000888800
0000800800
0000800800
0000888800
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Written solution**

Find the connected component that encloses at least one real hole: an empty cell region inside its bounding box that cannot reach the box boundary through empty cells. Keep only that component and delete all others.

**Reference program (`solve_M53`)**

```python
def solve_M53(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        if has_hole(cells):
            for r,c in cells:
                out[r][c] = col
    return out
```

### M54 — Point-reflect the object around the anchor

**What it tests:** Use a single anchor cell as the center of a 180-degree reflection.

**Staged hint:** Keep the original object, then map every object cell through the anchor to the opposite side.

**Train 1 — input**

```text
000000000
000000000
000330000
000300000
000010000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000330000
000300000
000010000
000003000
000033000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0000000000
0000000000
0007000000
0077000000
0000010000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000000
0007000000
0077000000
0000010000
0000000770
0000000700
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000000000
00006000000
00006600000
00000600000
00000100000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
00000000000
00006000000
00006600000
00000600000
00000100000
00000600000
00000660000
00000060000
00000000000
00000000000
```

**Written solution**

Preserve the anchor cell colored 1. For every other nonzero cell, also place a copy at the point-reflected position across the anchor, so the result is the union of the original object and its 180-degree reflection.

**Reference program (`solve_M54`)**

```python
def solve_M54(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    anchor = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    ar,ac = anchor
    out[ar][ac] = 1
    for r in range(h):
        for c in range(w):
            if g[r][c] not in (0,1):
                out[r][c] = g[r][c]
                rr,cc = 2*ar-r, 2*ac-c
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = g[r][c]
    return out
```

### M55 — Remove every component that touches the border

**What it tests:** Filter objects by a global geometric property: contact with the outer frame.

**Staged hint:** Solve it component by component. Any component that hits row 0, last row, column 0, or last column is deleted.

**Train 1 — input**

```text
20000000
22000000
00000000
00044000
00004000
03300000
00300060
00000060
```

**Train 1 — output**

```text
00000000
00000000
00000000
00044000
00004000
03300000
00300000
00000000
```

**Train 2 — input**

```text
000005000
000005500
000000000
007000000
007700000
000700000
000000220
000000200
440000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
007000000
007700000
000700000
000000220
000000200
000000000
```

**Test — input**

```text
0000000030
0000000033
0060000000
0066000000
2006000000
0000005000
0000005500
0000000500
0000700000
0000700000
```

**Test — expected output**

```text
0000000000
0000000000
0060000000
0066000000
0006000000
0000005000
0000005500
0000000500
0000000000
0000000000
```

**Written solution**

Find each connected component. Delete any component that touches the grid border, and keep only the components that are fully interior.

**Reference program (`solve_M55`)**

```python
def solve_M55(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        if not any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c] = col
    return out
```

### M56 — Center the prototype inside every rectangular frame

**What it tests:** Separate the payload object from the frame objects, then center the payload inside each frame interior.

**Staged hint:** First identify which components are hollow rectangular frames. The other object is the prototype you need to reuse.

**Train 1 — input**

```text
60000000000
66000011111
00000010001
00000010001
00000010001
00000011111
01111100000
01000100000
01000100000
01000100000
01111100000
```

**Train 1 — output**

```text
00000000000
00000000000
00000006000
00000006600
00000000000
00000000000
00000000000
00600000000
00660000000
00000000000
00000000000
```

**Train 2 — input**

```text
040000000000
444000000000
000000111111
000000100001
000000100001
000000100001
000000100001
111111111111
100001000000
100001000000
100001000000
111111000000
```

**Train 2 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Test — input**

```text
7700000000000
0770000000000
0000000111110
0000000100010
0000000100010
0000000100010
0000000111110
0111110000000
0100010011111
0100010010001
0100010010001
0111110010001
0000000011111
```

**Test — expected output**

```text
0000000000000
0000000000000
0000000000000
0000000077000
0000000007700
0000000000000
0000000000000
0000000000000
0077000000000
0007700007700
0000000000770
0000000000000
0000000000000
```

**Written solution**

Treat every hollow rectangle of color 1 as a frame. Take the single non-frame object as the prototype, normalize it, and place a centered copy inside each frame interior. The output contains only those centered copies.

**Reference program (`solve_M56`)**

```python
def solve_M56(g: Grid) -> Grid:
    h,w = dims(g)
    comps = same_color_components(g)
    frames = []
    proto = None
    for col,cells in comps:
        if col == 1 and is_rect_border(cells):
            frames.append((col,cells))
        elif col != 1:
            if proto is None or len(cells) > len(proto[1]):
                proto = (col,cells)
    pcol, pcells = proto
    pshape,(ph,pw),_ = normalize(pcells)
    out = blank(h,w)
    for _,fcells in frames:
        r0,r1,c0,c1 = bbox(fcells)
        ih,iw = (r1-r0-1), (c1-c0-1)
        sr = r0 + 1 + (ih-ph)//2
        sc = c0 + 1 + (iw-pw)//2
        for dr,dc in pshape:
            rr,cc = sr+dr, sc+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = pcol
    return out
```

## Hard

### H50 — Orbit the prototype around the pivot

**What it tests:** Use one anchor as a rotational pivot and union all four quarter-turn copies of a shape.

**Staged hint:** First record the shape as offsets from the 1-cell. Then rotate those offsets through 0, 90, 180, and 270 degrees.

**Train 1 — input**

```text
000000000
000000000
000030000
000033000
000010000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000030000
000333000
003313300
000333000
000030000
000000000
000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00000000000
00006000000
00006600000
00000100000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000000
00006000000
00006666000
00006160000
00066660000
00000060000
00000000000
00000000000
00000000000
```

**Test — input**

```text
0000000000000
0000000000000
0000000000000
0000008000000
0000008800000
0000000800000
0000001000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Test — expected output**

```text
0000000000000
0000000000000
0000000000000
0000008000000
0000008800000
0000880800000
0008801088000
0000080880000
0000088000000
0000008000000
0000000000000
0000000000000
0000000000000
```

**Written solution**

Treat the cell colored 1 as the pivot. Measure the prototype object's cells as offsets from that pivot, then stamp the object at all four quarter-turn rotations around the same pivot. Keep the pivot itself.

**Reference program (`solve_H50`)**

```python
def solve_H50(g: Grid) -> Grid:
    h,w = dims(g)
    anchor = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    ar,ac = anchor
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] not in (0,1)]
    col = g[cells[0][0]][cells[0][1]]
    rel = [(r-ar, c-ac) for r,c in cells]
    out = blank(h,w)
    out[ar][ac] = 1
    for dr,dc in rel:
        for rr,cc in [(dr,dc), (-dc,dr), (-dr,-dc), (dc,-dr)]:
            r,c = ar+rr, ac+cc
            if 0 <= r < h and 0 <= c < w:
                out[r][c] = col
    return out
```

### H51 — Mask and carry across panels

**What it tests:** Separate geometry from content: one panel tells you where, the other tells you what colors to keep.

**Staged hint:** Ignore the mask's actual color values. Its nonzero pattern is the stencil for the payload panel.

**Train 1 — input**

```text
02000934567
22200976543
02000923456
00020965432
00020912345
```

**Train 1 — output**

```text
04000
76500
03000
00030
00040
```

**Train 2 — input**

```text
2200009514263
0200009362514
0220009426351
0000209153642
0000209241536
0000229635124
```

**Train 2 — output**

```text
510000
060000
026000
000040
000030
000024
```

**Test — input**

```text
0020009876543
0020009123456
2222009654321
0002009718263
0002009362514
0000029426351
```

**Test — expected output**

```text
006000
003000
654300
000200
000500
000001
```

**Written solution**

Split the input into left and right panels at the separator column of 9s. Use the left panel only as a binary mask, and copy through the right panel's colors only at positions where the left panel is nonzero.

**Reference program (`solve_H51`)**

```python
def solve_H51(g: Grid) -> Grid:
    left,right = split_h_panels_by_sep(g, sep=9)
    h,w = dims(left)
    out = blank(h,w)
    for r in range(h):
        for c in range(w):
            if left[r][c] != 0:
                out[r][c] = right[r][c]
    return out
```

### H52 — Infer the panel transform and apply it to the query

**What it tests:** Reason analogically: discover the transformation from panel A to panel B, then reuse it on panel C.

**Staged hint:** Do not assume a fixed transform for the whole puzzle bank. Infer it fresh from the first two panels of each input.

**Train 1 — input**

```text
20009000290050
20009000290550
22009002290500
00009000090000
```

**Train 1 — output**

```text
0500
0550
0050
0000
```

**Train 2 — input**

```text
03000900000900000
03000900000900060
03330903330906660
00000900030900060
00000900030900000
```

**Train 2 — output**

```text
00000
06000
06660
06000
00000
```

**Test — input**

```text
04009000090000
04009044497770
04409040090070
00009000090000
```

**Test — expected output**

```text
0070
0070
0770
0000
```

**Written solution**

Split the input into three panels. Identify which transformation maps the first panel to the second from among the candidate symmetries, then apply that same transformation to the third panel.

**Reference program (`solve_H52`)**

```python
def solve_H52(g: Grid) -> Grid:
    panels = split_h_panels_by_sep(g, sep=9)
    A,B,C = panels
    candidates = {
        'rot90': rotate_grid_cw,
        'rot270': rotate_grid_ccw,
        'rot180': rotate_grid_180,
        'hflip': hflip_grid,
        'vflip': vflip_grid,
    }
    for name,fn in candidates.items():
        if fn(A) == B:
            return fn(C)
    return C
```

### H53 — Rebuild the Ferrers shape from numeric headers

**What it tests:** Interpret grid values as counts in the top row and left column, then reconstruct the shared footprint they permit.

**Staged hint:** Think of the first row as column heights and the first column as row lengths. A cell is filled only if both headers allow it.

**Train 1 — input**

```text
043211
500000
300000
200000
100000
000000
```

**Train 1 — output**

```text
000000
088888
088800
088000
080000
000000
```

**Train 2 — input**

```text
0543211
6000000
4000000
4000000
2000000
1000000
0000000
```

**Train 2 — output**

```text
0000000
0888888
0888800
0888000
0880000
0800000
0000000
```

**Test — input**

```text
0553210
5000000
5000000
3000000
2000000
1000000
0000000
```

**Test — expected output**

```text
0000000
0888880
0888800
0888000
0880000
0800000
0000000
```

**Written solution**

Use the first column as row lengths and the first row as column heights. In the interior, fill a cell with color 8 exactly when it lies within both the row-length limit for its row and the column-height limit for its column. Clear the headers in the output.

**Reference program (`solve_H53`)**

```python
def solve_H53(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    rowlens = [g[r][0] for r in range(1,h)]
    collens = [g[0][c] for c in range(1,w)]
    for r in range(1,h):
        for c in range(1,w):
            if rowlens[r-1] >= c and collens[c-1] >= r:
                out[r][c] = 8
    return out
```

### H54 — Use the control cell to choose the local transform

**What it tests:** Apply a discrete transformation code to a single object within its own bounding box.

**Staged hint:** Isolate the object's local frame first. The control cell only tells you which symmetry to use.

**Train 1 — input**

```text
30000000
00700000
00700000
00770000
00000000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00070000
00070000
00770000
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
100000000
000000000
000050000
000555000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000500000
000550000
000500000
000000000
000000000
000000000
000000000
```

**Test — input**

```text
400000000
000000000
006600000
000600000
000600000
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000000
000600000
000600000
006600000
000000000
000000000
000000000
000000000
```

**Written solution**

The top-left control cell selects a transformation: 1 = rotate 90° clockwise, 2 = rotate 180°, 3 = horizontal flip, 4 = vertical flip. Apply that transformation to the lone object inside its own bounding box, keep it in the same local frame, and remove the control cell.

**Reference program (`solve_H54`)**

```python
def solve_H54(g: Grid) -> Grid:
    h,w = dims(g)
    code = g[0][0]
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] != 0 and not (r==0 and c==0)]
    color = g[cells[0][0]][cells[0][1]]
    shape,(ph,pw),(r0,c0) = normalize(cells)
    kind = {1:'rot90', 2:'rot180', 3:'hflip', 4:'vflip'}[code]
    tshape = transform_shape(shape, kind)
    out = blank(h,w)
    for dr,dc in tshape:
        rr,cc = r0+dr, c0+dc
        if 0 <= rr < h and 0 <= cc < w:
            out[rr][cc] = color
    return out
```

### H55 — Match the query shape to the right prototype and recolor it

**What it tests:** Compare normalized shapes up to symmetry, then transfer the matching prototype's label color to the query.

**Staged hint:** The prototype's visible object color is not the answer color. The answer color is the prototype panel's label cell.

**Train 1 — input**

```text
40000960000900000
02000900300908880
02000903330908000
02200900000900000
00000900000900000
```

**Train 1 — output**

```text
00000
04440
04000
00000
00000
```

**Train 2 — input**

```text
40000960000900000
02000900300900800
02000903330908800
02200900000900800
00000900000900000
```

**Train 2 — output**

```text
00000
00600
06600
00600
00000
```

**Test — input**

```text
40000960000900000
02000900300900800
02000903330900800
02200900000908800
00000900000900000
```

**Test — expected output**

```text
00000
00400
00400
04400
00000
```

**Written solution**

Split the input into three panels. The first two panels each contain a labeled prototype shape; the label is the color in the panel's top-left corner. Compare the query shape in the third panel against the prototype shapes up to rotation and reflection, then recolor the entire query shape with the matching label color.

**Reference program (`solve_H55`)**

```python
def solve_H55(g: Grid) -> Grid:
    p1,p2,q = split_h_panels_by_sep(g, sep=9)
    def label_and_shape(panel):
        label = panel[0][0]
        cells = [(r,c) for r in range(len(panel)) for c in range(len(panel[0]))
                 if panel[r][c] != 0 and not (r==0 and c==0)]
        sh,_,_ = normalize(cells)
        return label, sh, cells
    lab1,sh1,_ = label_and_shape(p1)
    lab2,sh2,_ = label_and_shape(p2)
    qcells = [(r,c) for r in range(len(q)) for c in range(len(q[0])) if q[r][c] != 0]
    qshape,_,_ = normalize(qcells)
    out = blank(*dims(q))
    if qshape in all_symmetries(sh1):
        lab = lab1
    else:
        lab = lab2
    for r,c in qcells:
        out[r][c] = lab
    return out
```

### H56 — Stamp the prototype with anchor-coded rotations

**What it tests:** Reuse one prototype at multiple anchors, but let the anchor color choose the orientation.

**Staged hint:** Separate the prototype from the anchor dots first. Then decode each anchor color into a transformation before stamping.

**Train 1 — input**

```text
6000002000
6600000000
0000000000
0000000000
0000030000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000006000
0000006600
0000000000
0000000000
0000066000
0000060000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
77000002000
07700000000
00000000000
00000000000
00000000000
40000000000
00000050000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000007700
00000000770
00000000000
00000000000
00000000000
77000000000
07700007000
00000077000
00000070000
00000000000
00000000000
```

**Test — input**

```text
080000002000
888000000000
000000000000
000000000000
300000000000
000000000000
000000050000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Test — expected output**

```text
000000000800
000000008880
000000000000
000000000000
800000000000
880000000000
800000008000
000000088000
000000008000
000000000000
000000000000
000000000000
```

**Written solution**

Treat the largest non-anchor object as the prototype. Each anchor color chooses how to transform that prototype before stamping it with the anchor as the placement origin: 2 = identity, 3 = rotate 90° clockwise, 4 = rotate 180°, 5 = rotate 270° clockwise.

**Reference program (`solve_H56`)**

```python
def solve_H56(g: Grid) -> Grid:
    h,w = dims(g)
    anchors = [(g[r][c], r, c) for r in range(h) for c in range(w) if g[r][c] in (2,3,4,5)]
    comps = [(col,cells) for col,cells in same_color_components(g) if col not in (2,3,4,5)]
    pcol,pcells = max(comps, key=lambda t: len(t[1]))
    pshape,_,_ = normalize(pcells)
    code_to_kind = {2:'id', 3:'rot90', 4:'rot180', 5:'rot270'}
    out = blank(h,w)
    for code,ar,ac in anchors:
        tshape = transform_shape(pshape, code_to_kind[code])
        for dr,dc in tshape:
            rr,cc = ar+dr, ac+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = pcol
    return out
```
