# 21 More ARC-Style Puzzles

This is the seventh continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E43–E49, M43–M49, H43–H49**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch pushes harder on row and header metadata, local-frame object transforms, analogy panels, prototype lookup, directional ray logic, and distance-field reasoning.

**New motifs in this batch**

**`ray_emit_until(seed, blocker)`** — treat a launcher and seed as the start of a directional paint ray that continues until a blocker or boundary. This is most visible in **E48** and **H46**.

**`nearest_seed_fill(seeds, tie=0)`** — assign each cell to the unique closest seed under Manhattan distance, leaving ties unclaimed. This is the main idea in **H49**.

## Easy

### E43 — Horizontal midpoint bridge

**What it tests:** Detect same-color horizontal endpoints with one missing cell between them.

**Staged hint:** Work row by row. For each color, look for two matching cells exactly two columns apart and fill the middle if it is 0.

**Train 1 — input**

```text
0000000
0202000
0000000
0000000
4040000
0000707
0000000
```

**Train 1 — output**

```text
0000000
0222000
0000000
0000000
4440000
0000777
0000000
```

**Train 2 — input**

```text
00303000
00000000
05050000
00000000
00000000
00000000
00006060
00000000
```

**Train 2 — output**

```text
00333000
00000000
05550000
00000000
00000000
00000000
00006660
00000000
```

**Test — input**

```text
000000000
202000000
000000000
000040400
000000000
000000000
000000000
000007070
000000000
```

**Test — expected output**

```text
000000000
222000000
000000000
000044400
000000000
000000000
000000000
000007770
000000000
```

**Written solution**

For each row, whenever two cells of the same nonzero color sit with exactly one empty cell between them, fill that middle cell with the same color and leave everything else unchanged.

**Reference program (`solve_E43`)**

```python
def solve_E43(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r][c+2] and g[r][c+1]==0:
                out[r][c+1]=g[r][c]
    return out
```

---

### E44 — Anti-diagonal reflection

**What it tests:** Coordinate reflection across the anti-diagonal of a square grid.

**Staged hint:** Ignore the colors at first and think in coordinates. Every cell moves from (r,c) to (n-1-c, n-1-r).

**Train 1 — input**

```text
020000
000000
000030
000000
500000
000007
```

**Train 1 — output**

```text
700000
000300
000000
000000
000002
050000
```

**Train 2 — input**

```text
0000000
0000004
0060000
0000000
0000000
3000000
0000800
```

**Train 2 — output**

```text
0000040
0000000
8000000
0000000
0000600
0000000
0300000
```

**Test — input**

```text
00000002
00050000
00000000
07000000
00000000
00000000
00000040
00000000
```

**Test — expected output**

```text
00000002
04000000
00000000
00000000
00000050
00000000
00007000
00000000
```

**Written solution**

Reflect the whole square grid across the anti-diagonal. Each nonzero cell moves to the position mirrored through the top-right to bottom-left diagonal.

**Reference program (`solve_E44`)**

```python
def solve_E44(g: Grid) -> Grid:
    n=len(g)
    out=blank(n,n)
    for r in range(n):
        for c in range(n):
            out[n-1-c][n-1-r]=g[r][c]
    return out
```

---

### E45 — Row-key stencil

**What it tests:** A row-level instruction cell controlling where placeholder cells get painted.

**Staged hint:** Treat the leftmost nonzero in each active row as the row's key color. Every 8 in that row is just a placeholder to be replaced.

**Train 1 — input**

```text
20080800
00000000
40800080
00000000
78008000
00000000
```

**Train 1 — output**

```text
20020200
00000000
40400040
00000000
77007000
00000000
```

**Train 2 — input**

```text
000000000
300080080
000000000
508800008
000000000
000000000
600008000
```

**Train 2 — output**

```text
000000000
300030030
000000000
505500005
000000000
000000000
600006000
```

**Test — input**

```text
4080000080
0000000000
0000000000
2000088000
0000000000
7808000008
0000000000
0000000000
```

**Test — expected output**

```text
4040000040
0000000000
0000000000
2000022000
0000000000
7707000007
0000000000
0000000000
```

**Written solution**

In each row, the first-column color is the key. Replace every 8 elsewhere in that row with the key color, and keep the rest of the row as it is.

**Reference program (`solve_E45`)**

```python
def solve_E45(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        key=g[r][0]
        for c in range(1,w):
            if g[r][c]==8 and key!=0:
                out[r][c]=key
    return out
```

---

### E46 — Rightward row gravity

**What it tests:** Per-row compaction while preserving the left-to-right order of nonzero cells.

**Staged hint:** Solve one row at a time: strip out the zeros, keep the nonzero sequence in order, and slide that sequence against the right edge.

**Train 1 — input**

```text
2030040
0500600
7000008
0000000
9010200
```

**Train 1 — output**

```text
0000234
0000056
0000078
0000000
0000912
```

**Train 2 — input**

```text
04050600
70008009
00300020
10000000
```

**Train 2 — output**

```text
00000456
00000789
00000032
00000001
```

**Test — input**

```text
020030400
500600070
008009000
102000304
```

**Test — expected output**

```text
000000234
000000567
000000089
000001234
```

**Written solution**

For each row independently, remove the zeros, keep the remaining colors in their original order, and place that sequence flush against the right side of the row.

**Reference program (`solve_E46`)**

```python
def solve_E46(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        vals=[x for x in g[r] if x!=0]
        out[r][w-len(vals):]=vals
    return out
```

---

### E47 — Square-corner completion

**What it tests:** Local 2x2 pattern completion from three matching corners.

**Staged hint:** Scan every 2x2 block. If exactly three cells are the same nonzero color and one corner is 0, fill that missing corner.

**Train 1 — input**

```text
220000
200000
000000
000040
000440
000000
```

**Train 1 — output**

```text
220000
220000
000000
000440
000440
000000
```

**Train 2 — input**

```text
0000000
0330000
0030000
0000000
0000550
0000500
0000000
```

**Train 2 — output**

```text
0000000
0330000
0330000
0000000
0000550
0000550
0000000
```

**Test — input**

```text
00000600
00000660
00000000
00000000
00000000
07700000
07000000
00000000
```

**Test — expected output**

```text
00000660
00000660
00000000
00000000
00000000
07700000
07700000
00000000
```

**Written solution**

Look at every 2x2 block. When three corners are the same nonzero color and the fourth corner is empty, fill the empty corner with that color.

**Reference program (`solve_E47`)**

```python
def solve_E47(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            cells=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[x for x in cells if x!=0]
            if len(nz)==3 and len(set(nz))==1:
                v=nz[0]
                if g[r][c]==0: out[r][c]=v
                if g[r][c+1]==0: out[r][c+1]=v
                if g[r+1][c]==0: out[r+1][c]=v
                if g[r+1][c+1]==0: out[r+1][c+1]=v
    return out
```

---

### E48 — Rightward ray launch

**What it tests:** A launcher-plus-seed pair that extrudes color along a row until a blocker or edge.

**Staged hint:** Every [1, color] pair starts a ray. Keep the 1, keep the first colored seed, and extend that seed color through zeros until a 9 or the edge stops it.

**Train 1 — input**

```text
014000090
000000000
170000000
000000000
000150009
```

**Train 1 — output**

```text
014444490
000000000
177777777
000000000
000155559
```

**Train 2 — input**

```text
0000000000
0016000090
0000000000
1300090000
0000000000
0000180000
```

**Train 2 — output**

```text
0000000000
0016666690
0000000000
1333390000
0000000000
0000188888
```

**Test — input**

```text
12000090000
00000000000
00017000009
00000000000
00000000000
00000000000
00000140000
```

**Test — expected output**

```text
12222290000
00000000000
00017777779
00000000000
00000000000
00000000000
00000144444
```

**Written solution**

Whenever a row contains a 1 immediately followed by some nonzero color, that color emits to the right through empty cells. The ray stops at a 9 or at the edge of the grid.

**Reference program (`solve_E48`)**

```python
def solve_E48(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        c=0
        while c < w-1:
            if g[r][c]==1 and g[r][c+1] not in (0,1,9):
                col=g[r][c+1]
                k=c+1
                while k < w and g[r][k] != 9:
                    if g[r][k] in (0,col):
                        out[r][k]=col
                    k += 1
                c=k
            else:
                c += 1
    return out
```

---

### E49 — Vertical mirror copy

**What it tests:** Completing a blank half by mirroring the occupied half across a vertical axis.

**Staged hint:** Only the left half carries information. Mirror every nonzero left-half cell into the symmetric position on the right half.

**Train 1 — input**

```text
20000000
00300000
00000000
04000000
00050000
00000000
```

**Train 1 — output**

```text
20000002
00300300
00000000
04000040
00055000
00000000
```

**Train 2 — input**

```text
0000600000
0000000000
2000000000
0070000000
0000000000
0300000000
0004000000
```

**Train 2 — output**

```text
0000660000
0000000000
2000000002
0070000700
0000000000
0300000030
0004004000
```

**Test — input**

```text
000000000000
500000000000
000002000000
000000000000
007000000000
000000000000
000030000000
000000000000
```

**Test — expected output**

```text
000000000000
500000000005
000002200000
000000000000
007000000700
000000000000
000030030000
000000000000
```

**Written solution**

Copy the left half of the grid into the right half by vertical mirroring, preserving the original colors and positions relative to the center line.

**Reference program (`solve_E49`)**

```python
def solve_E49(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    half=w//2
    for r in range(h):
        for c in range(half):
            if g[r][c]!=0:
                out[r][w-1-c]=g[r][c]
    return out
```

---

## Medium

### M43 — Header-count area select

**What it tests:** Using a numeric cue in the header row to choose an object by area.

**Staged hint:** Count the number of 1s in the top row first. Then measure the size of each body component and keep only the one whose area matches that count.

**Train 1 — input**

```text
01010010
00000000
22004000
00004400
00000000
00000700
00007770
00000700
```

**Train 1 — output**

```text
00000000
00000000
00004000
00004400
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
101010101
000000000
022000000
000004000
000004400
000000000
077700000
007000000
007000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
077700000
007000000
007000000
```

**Test — input**

```text
0101010100
0000000000
0220004000
0000004400
0000000000
0000660000
0000660000
0000000077
0000000777
```

**Test — expected output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000660000
0000660000
0000000000
0000000000
```

**Written solution**

The top row encodes a number k as the count of 1s. Among all nonzero connected components below it, keep only the component whose number of cells is exactly k and erase everything else.

**Reference program (`solve_M43`)**

```python
def solve_M43(g: Grid) -> Grid:
    h,w=dims(g)
    k=sum(1 for x in g[0] if x==1)
    out=blank(h,w)
    body=[row[:] for row in g[1:]]
    for col,cells in same_color_components(body):
        if len(cells)==k:
            for r,c in cells:
                out[r+1][c]=col
    return out
```

---

### M44 — In-place component rotation

**What it tests:** Normalizing each object to its own local frame and rotating it there.

**Staged hint:** Separate the components first. For each one, use its own bounding box as a local coordinate frame and rotate the shape 90 degrees clockwise inside that box.

**Train 1 — input**

```text
20000444
20000040
22000000
00000000
00000000
00006000
00006000
00066000
```

**Train 1 — output**

```text
22200040
20000440
00000040
00000000
00000000
00060000
00066600
00000000
```

**Train 2 — input**

```text
000000000
003300000
033000000
000000000
000007770
500000700
500000000
550000000
000000000
```

**Train 2 — output**

```text
000000000
030000000
033000000
003000000
000000700
555007700
500000700
000000000
000000000
```

**Test — input**

```text
0002000000
0002000000
0022000000
0000000000
0000044000
0000440000
0000000000
0000000666
0000000060
0000000000
```

**Test — expected output**

```text
0020000000
0022200000
0000000000
0000000000
0000400000
0000440000
0000040000
0000000060
0000000660
0000000060
```

**Written solution**

Treat each connected same-color object independently. Find its bounding box, interpret the shape in local coordinates, rotate it 90 degrees clockwise, and place it back into the same box.

**Reference program (`solve_M44`)**

```python
def solve_M44(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for col,cells in same_color_components(g):
        shape,(hh,ww),(r0,c0)=normalize(cells)
        tshape={(c,hh-1-r) for r,c in shape}
        for dr,dc in tshape:
            out[r0+dr][c0+dc]=col
    return out
```

---

### M45 — Bounding-box solidify

**What it tests:** Turning sparse objects into solid rectangles defined by their bounding boxes.

**Staged hint:** Object detection matters more than local neighborhoods here. Once you know an object's min/max rows and columns, fill the whole rectangle.

**Train 1 — input**

```text
000000000
020000000
020000000
022000000
000004440
000000400
000000000
000000000
```

**Train 1 — output**

```text
000000000
022000000
022000000
022000000
000004440
000004440
000000000
000000000
```

**Train 2 — input**

```text
0000000330
0000003300
0000000000
0000000000
0000000000
0050000000
0050000000
0550000000
0000000000
```

**Train 2 — output**

```text
0000003330
0000003330
0000000000
0000000000
0000000000
0550000000
0550000000
0550000000
0000000000
```

**Test — input**

```text
0000000000
0600000000
0600000000
0660000000
0006000000
0000000700
0000077700
0000070000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0660000000
0660000000
0660000000
0006000000
0000077700
0000077700
0000077700
0000000000
0000000000
```

**Written solution**

For every connected nonzero object, compute its bounding box and fill every cell inside that rectangle with the object's color.

**Reference program (`solve_M45`)**

```python
def solve_M45(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for col,cells in same_color_components(g):
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=col
    return out
```

---

### M46 — Marker-vector translation

**What it tests:** Extracting a motion vector from two markers and applying it to a shape.

**Staged hint:** Find the vector from the 1 to the 2 once. Then apply that same row/column shift to every 3-cell and output only the translated shape.

**Train 1 — input**

```text
00030000
01033000
00000000
00002000
00000000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000030
00000033
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
000030000
000330100
000030000
000000000
000020000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
003000000
033000000
003000000
000000000
000000000
000000000
```

**Test — input**

```text
0000000000
0033000100
0003000000
0003000000
0000020000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000000000
0000000000
3300000000
0300000000
0300000000
0000000000
0000000000
0000000000
```

**Written solution**

Use the displacement from marker 1 to marker 2 as a translation vector. Move all color-3 cells by that vector and output the moved shape alone.

**Reference program (`solve_M46`)**

```python
def solve_M46(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    p1=p2=None
    cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                p1=(r,c)
            elif g[r][c]==2:
                p2=(r,c)
            elif g[r][c]==3:
                cells.append((r,c))
    dr,dc=p2[0]-p1[0], p2[1]-p1[1]
    for r,c in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=3
    return out
```

---

### M47 — Two-row palette remap

**What it tests:** Reading a color-to-color legend and recoloring the body accordingly.

**Staged hint:** The first two rows are a lookup table: row 0 says 'from', row 1 says 'to'. Build the mapping first, then recolor the lower rows cell by cell.

**Train 1 — input**

```text
20304000
50607000
00000000
20003330
20000300
22000040
00000040
00000440
```

**Train 1 — output**

```text
20304000
50607000
00000000
50006660
50000600
55000070
00000070
00000770
```

**Train 2 — input**

```text
040607000
020803000
000000777
004400070
044000000
000006000
000006000
000006600
000000000
```

**Train 2 — output**

```text
040607000
020803000
000000333
002200030
022000000
000008000
000008000
000008800
000000000
```

**Test — input**

```text
2050700000
8040300000
0000000000
0200000000
0200000000
0220055000
0000550000
0000000777
0000000070
0000000000
```

**Test — expected output**

```text
2050700000
8040300000
0000000000
0800000000
0800000000
0880044000
0000440000
0000000333
0000000030
0000000000
```

**Written solution**

Read each nonzero column in the first two rows as a mapping from a source color to a target color. Keep the legend rows, and recolor all matching body cells using that mapping.

**Reference program (`solve_M47`)**

```python
def solve_M47(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    mapping={}
    for c in range(w):
        if g[0][c]!=0:
            mapping[g[0][c]]=g[1][c]
    for r in range(2,h):
        for c in range(w):
            if g[r][c] in mapping:
                out[r][c]=mapping[g[r][c]]
    return out
```

---

### M48 — Marker-box crop

**What it tests:** Variable-size output defined by a marker rectangle.

**Staged hint:** Ignore most of the grid. The two 9s are opposite corners of the relevant rectangle, and the output is just that cropped window.

**Train 1 — input**

```text
000000000
009000000
000200000
000004000
007000900
000000000
000000000
000000000
```

**Train 1 — output**

```text
90000
02000
00040
70009
```

**Train 2 — input**

```text
0000000000
0000000000
0900000000
0030000000
0000000000
0000600000
0200000000
0000090000
0000000000
```

**Train 2 — output**

```text
90000
03000
00000
00060
20000
00009
```

**Test — input**

```text
0000000000
0000900000
0000050000
0000000200
0000000000
0000700000
0000003090
0000000000
0000000000
0000000000
```

**Test — expected output**

```text
90000
05000
00020
00000
70000
00309
```

**Written solution**

Find the two 9 markers, treat them as opposite corners of an axis-aligned rectangle, and output the inclusive crop bounded by those corners.

**Reference program (`solve_M48`)**

```python
def solve_M48(g: Grid) -> Grid:
    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    (r1,c1),(r2,c2)=pts
    r0,r3=sorted([r1,r2])
    c0,c3=sorted([c1,c2])
    return [row[c0:c3+1] for row in g[r0:r3+1]]
```

---

### M49 — Point reflection about anchor

**What it tests:** Using a central anchor to reflect a pattern into the opposite side of the grid.

**Staged hint:** Treat the 9 as the center of a point reflection. Every offset from the anchor is copied with the same magnitude in the opposite direction.

**Train 1 — input**

```text
0000000
0020000
0420000
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0000000
0009000
0000240
0000200
0000000
```

**Train 2 — input**

```text
00000000
00000000
00003300
00006000
00000900
00000000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00000000
00000900
00000060
00000330
00000000
```

**Test — input**

```text
000000000
000200000
002200000
050000000
000090000
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000000000
000090000
000000050
000002200
000002000
000000000
```

**Written solution**

Reflect every nonzero non-9 cell through the 9 by point symmetry: a cell at offset (dr,dc) from the anchor moves to offset (-dr,-dc). Preserve the 9 itself.

**Reference program (`solve_M49`)**

```python
def solve_M49(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    ar,ac=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9][0]
    out[ar][ac]=9
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                nr,nc=2*ar-r,2*ac-c
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out
```

---

## Hard

### H43 — Panel overlay logic

**What it tests:** Aligned panel comparison with different outputs for unique versus overlapping occupancy.

**Staged hint:** Do not reason objectwise yet; reason positionwise. Compare the left and middle panels cell by cell and encode left-only, middle-only, and overlap separately in the right panel.

**Train 1 — input**

```text
02000903000900000
02000933300900000
02200903000900000
00000900000900000
00000900000900000
```

**Train 1 — output**

```text
02000903000908000
02000933300938300
02200903000908200
00000900000900000
00000900000900000
```

**Train 2 — input**

```text
00000966000900000
04400906000900000
00400906000900000
00400900000900000
00000900000900000
```

**Train 2 — output**

```text
00000966000966000
04400906000908400
00400906000906400
00400900000900400
00000900000900000
```

**Test — input**

```text
00500900000900000
05550907700900000
00500900700900000
00000900700900000
00000900000900000
```

**Test — expected output**

```text
00500900000900500
05550907700908850
00500900700900800
00000900700900700
00000900000900000
```

**Written solution**

The left and middle 5x5 panels are aligned. In the right panel, copy left-only occupied cells with the left panel's color, copy middle-only occupied cells with the middle panel's color, and paint overlaps as color 8.

**Reference program (`solve_H43`)**

```python
def solve_H43(g: Grid) -> Grid:
    left,mid,right=split_h_panels(g,5)
    out_right=blank(5,5)
    for r in range(5):
        for c in range(5):
            a,b=left[r][c], mid[r][c]
            if a!=0 and b!=0:
                out_right[r][c]=8
            elif a!=0:
                out_right[r][c]=a
            elif b!=0:
                out_right[r][c]=b
    return join_h_panels([left,mid,out_right])
```

---

### H44 — Learn-the-rotation analogy

**What it tests:** Transferring a transform shown in one panel pair to a second panel pair.

**Staged hint:** Infer the relation from top-left to top-right first. Once that example tells you the transform, apply the same transform to the bottom-left panel and write the result into bottom-right.

**Train 1 — input**

```text
20000900222
20000900200
22000900000
00000900000
00000900000
99999999999
44400900000
04000900000
00000900000
00000900000
00000900000
```

**Train 1 — output**

```text
20000900222
20000900200
22000900000
00000900000
00000900000
99999999999
44400900004
04000900044
00000900004
00000900000
00000900000
```

**Train 2 — input**

```text
03300900030
33000900033
00000900003
00000900000
00000900000
99999999999
06000900000
06000900000
66000900000
00000900000
00000900000
```

**Train 2 — output**

```text
03300900030
33000900033
00000900003
00000900000
00000900000
99999999999
06000900600
06000900666
66000900000
00000900000
00000900000
```

**Test — input**

```text
55500900005
05000900055
00000900005
00000900000
00000900000
99999999999
70000900000
70000900000
77000900000
00000900000
00000900000
```

**Test — expected output**

```text
55500900005
05000900055
00000900005
00000900000
00000900000
99999999999
70000900777
70000900700
77000900000
00000900000
00000900000
```

**Written solution**

The top pair shows the rule: the source panel is rotated 90 degrees clockwise to make the target panel. Apply that same rotation to the bottom-left panel and place the result in the bottom-right panel, leaving the rest unchanged.

**Reference program (`solve_H44`)**

```python
def solve_H44(g: Grid) -> Grid:
    out=clone(g)
    bl=[row[:5] for row in g[6:11]]
    br=rotate_panel_cw(bl)
    for r in range(5):
        for c in range(5):
            out[6+r][6+c]=br[r][c]
    return out
```

---

### H45 — Legend prototype stamping

**What it tests:** Retrieving small templates from a legend region and stamping them into a separate workspace.

**Staged hint:** The top strip stores the prototypes; the bottom markers only tell you which one to use and where to anchor it. Clear the workspace mentally, then stamp the matching 3x3 template for each marker.

**Train 1 — input**

```text
2009333
2009030
2209000
9999999
0000000
2000000
0000300
0000000
0000000
0000000
0000000
```

**Train 1 — output**

```text
2009333
2009030
2209000
9999999
0000000
2000000
2000333
2200030
0000000
0000000
0000000
```

**Train 2 — input**

```text
0209033
0209330
2209000
9999999
0300000
0000000
0000000
2000000
0000000
0000000
0000000
```

**Train 2 — output**

```text
0209033
0209330
2209000
9999999
0033000
0330000
0000000
0200000
0200000
2200000
0000000
```

**Test — input**

```text
22293000
02093000
00093300
99999999
20000000
00003000
00000000
00000000
02000000
00000000
00000000
00000000
```

**Test — expected output**

```text
22293000
02093000
00093300
99999999
22200000
02003000
00003000
00003300
02220000
00200000
00000000
00000000
```

**Written solution**

The top region contains a 3x3 prototype for color 2 and a 3x3 prototype for color 3. In the lower workspace, every marker 2 or 3 is replaced by the corresponding prototype, anchored at the marker's position.

**Reference program (`solve_H45`)**

```python
def solve_H45(g: Grid) -> Grid:
    h,w=dims(g)
    proto2=[row[0:3] for row in g[0:3]]
    proto3=[row[4:7] for row in g[0:3]]
    out=blank(h,w)
    for r in range(4):
        for c in range(w):
            out[r][c]=g[r][c]
    for r in range(4,h):
        for c in range(w):
            if g[r][c]==2:
                for dr in range(3):
                    for dc in range(3):
                        if r+dr<h and c+dc<w and proto2[dr][dc]==2:
                            out[r+dr][c+dc]=2
            elif g[r][c]==3:
                for dr in range(3):
                    for dc in range(3):
                        if r+dr<h and c+dc<w and proto3[dr][dc]==3:
                            out[r+dr][c+dc]=3
    return out
```

---

### H46 — Crossing rays with blockers

**What it tests:** Directional propagation from border launchers with blockers and intersection handling.

**Staged hint:** Horizontal rays start from left-border 2s and vertical rays start from top-border 3s. Let 9 stop both, then give intersection cells special treatment.

**Train 1 — input**

```text
00300300
00000000
20000000
00009000
00000000
20000900
00000000
```

**Train 1 — output**

```text
00300300
00300300
22822822
00309300
00300300
22822900
00300000
```

**Train 2 — input**

```text
030000300
200000000
000000000
000000000
000000900
000000000
200900000
000000000
```

**Train 2 — output**

```text
030000300
282222822
030000300
030000300
030000900
030000000
282900000
030000000
```

**Test — input**

```text
0003000300
0000000000
2000000000
0000000000
0009000000
0000000000
0000000900
2000090000
0000000000
```

**Test — expected output**

```text
0003000300
0003000300
2228222822
0003000300
0009000300
0000000300
0000000900
2222290000
0000000000
```

**Written solution**

Emit horizontal rays of color 2 from every left-border 2 and vertical rays of color 3 from every top-border 3. Rays stop when they hit a 9. Cells reached by both kinds of rays become 8; cells reached by only one keep that ray's color.

**Reference program (`solve_H46`)**

```python
def solve_H46(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    horiz=set()
    vert=set()
    for r in range(h):
        if g[r][0]==2:
            c=1
            while c < w and g[r][c] != 9:
                horiz.add((r,c))
                c += 1
    for c in range(w):
        if g[0][c]==3:
            r=1
            while r < h and g[r][c] != 9:
                vert.add((r,c))
                r += 1
    for r,c in horiz | vert:
        if g[r][c]==9:
            continue
        if (r,c) in horiz and (r,c) in vert:
            out[r][c]=8
        elif (r,c) in horiz:
            out[r][c]=2
        elif (r,c) in vert:
            out[r][c]=3
    return out
```

---

### H47 — Translate then fill

**What it tests:** A composed transform that first relocates a sparse shape and then abstracts it into a solid rectangle.

**Staged hint:** Break the task into two stages. First compute the same translation vector as in a marker-vector task; then forget the original sparsity and fill the moved shape's bounding box.

**Train 1 — input**

```text
000400000
010440000
000000000
000020000
000000000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000440
000000440
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0004000100
0044000000
0004000000
0000020000
0000000000
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
0000000000
4400000000
4400000000
4400000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
04400000000
04100000000
04000000000
00000000000
00000020000
00000000000
00000000000
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
00000000000
00000000000
00000000000
00000440000
00000440000
00000440000
00000000000
00000000000
00000000000
```

**Written solution**

Use the vector from marker 1 to marker 2 to translate all color-4 cells. Then take the translated cells' bounding box and fill that entire rectangle with color 4.

**Reference program (`solve_H47`)**

```python
def solve_H47(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    p1=p2=None
    cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                p1=(r,c)
            elif g[r][c]==2:
                p2=(r,c)
            elif g[r][c]==4:
                cells.append((r,c))
    dr,dc=p2[0]-p1[0], p2[1]-p1[1]
    moved=[(r+dr,c+dc) for r,c in cells if 0<=r+dr<h and 0<=c+dc<w]
    if not moved:
        return out
    rs=[r for r,c in moved]
    cs=[c for r,c in moved]
    for r in range(min(rs), max(rs)+1):
        for c in range(min(cs), max(cs)+1):
            out[r][c]=4
    return out
```

---

### H48 — Three-panel majority silhouette

**What it tests:** Voting across multiple noisy aligned panels to recover a consensus shape.

**Staged hint:** Ignore colors and focus on occupancy. For each position, count in how many of the first three panels that position is filled; keep it only when at least two panels agree.

**Train 1 — input**

```text
02000903000944000900000
02000933300904000900000
02200903000904400900000
00000900000900000900000
00000900000900000900000
```

**Train 1 — output**

```text
02000903000944000908000
02000933300904000908000
02200903000904400908800
00000900000900000900000
00000900000900000900000
```

**Train 2 — input**

```text
00000960000977000900000
05500906600907000900000
00500900600907000900000
00500900600900000900000
00000900000900000900000
```

**Train 2 — output**

```text
00000960000977000980000
05500906600907000908800
00500900600907000900800
00500900600900000900800
00000900000900000900000
```

**Test — input**

```text
00200900300900000900000
02220903330904440900000
00200900300900400900000
00000900300900400900000
00000900000900000900000
```

**Test — expected output**

```text
00200900300900000900800
02220903330904440908880
00200900300900400900800
00000900300900400900800
00000900000900000900000
```

**Written solution**

Compare the first three aligned panels position by position. In the fourth panel, place color 8 wherever at least two of the three source panels are occupied at that position.

**Reference program (`solve_H48`)**

```python
def solve_H48(g: Grid) -> Grid:
    p1,p2,p3,p4=split_h_panels(g,5)
    outp=blank(5,5)
    for r in range(5):
        for c in range(5):
            cnt=sum(1 for p in [p1,p2,p3] if p[r][c]!=0)
            if cnt >= 2:
                outp[r][c]=8
    return join_h_panels([p1,p2,p3,outp])
```

---

### H49 — Manhattan nearest-seed fill

**What it tests:** Global distance-based partitioning with explicit tie behavior.

**Staged hint:** Think of every colored seed as claiming territory by Manhattan distance. A cell inherits the nearest seed's color; ties do not belong to anyone and stay 0.

**Train 1 — input**

```text
20003
00000
00000
00000
00500
```

**Train 1 — output**

```text
22033
22033
20503
05550
55555
```

**Train 2 — input**

```text
000000
040070
000000
000000
000200
000000
```

**Train 2 — output**

```text
444777
444777
444077
442200
222222
222222
```

**Test — input**

```text
0002000
0000000
0000000
4000000
0000000
0000000
0000007
```

**Test — expected output**

```text
0222222
4022222
4402227
4440077
4440777
4447777
4477777
```

**Written solution**

For every cell, compute which seed is closest in Manhattan distance. Color the cell with that seed's color if the closest seed is unique; if there is a tie for nearest, leave the cell as 0.

**Reference program (`solve_H49`)**

```python
def solve_H49(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    for r in range(h):
        for c in range(w):
            best=None
            colors=[]
            for sr,sc,v in seeds:
                d=abs(sr-r)+abs(sc-c)
                if best is None or d < best:
                    best=d
                    colors=[v]
                elif d == best:
                    colors.append(v)
            out[r][c]=colors[0] if len(set(colors))==1 else 0
    return out
```

---
