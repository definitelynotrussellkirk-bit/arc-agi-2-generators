# 21 More ARC-Style Puzzles

This is the fourth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E22–E28, M22–M28, H22–H28**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into local motif detection in the easy tier, object filtering and restructuring in the medium tier, and normalization / packing / template-transfer operations in the hard tier.

## Easy

### E22 — Highlight plus centers

**What it tests:** Detect exact cardinal pluses while preserving arms.

**Staged hint:** First mark cells whose four cardinal neighbors match their color; then recolor only those center cells.

**Train 1 — input**

```text
0000000
0002000
0022200
0002000
0000000
0003000
0033300
0003000
```

**Train 1 — output**

```text
0000000
0002000
0028200
0002000
0000000
0003000
0038300
0003000
```

**Train 2 — input**

```text
000000000
000040000
000444000
000040000
000000000
000060000
000666000
000060000
000000000
```

**Train 2 — output**

```text
000000000
000040000
000484000
000040000
000000000
000060000
000686000
000060000
000000000
```

**Test — input**

```text
00000000000
00002000000
00022200000
00002000000
00000000000
00000070000
00000777000
00000070000
00000000000
```

**Test — expected output**

```text
00000000000
00002000000
00028200000
00002000000
00000000000
00000070000
00000787000
00000070000
00000000000
```

**Written solution**

Whenever a nonzero cell has the same color directly above, below, left, and right, recolor that center cell to 8. Leave the arms and every other cell unchanged.

**Reference program (`solve_E22`)**

```python
def solve_E22(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c]==v and g[r+1][c]==v and g[r][c-1]==v and g[r][c+1]==v:
                out[r][c]=8
    return out
```

---

### E23 — Complete exact L-shapes to squares

**What it tests:** Local 2×2 reasoning with one missing corner.

**Staged hint:** Look at every 2×2 window. If three cells share one nonzero color and the fourth is 0, fill the missing corner.

**Train 1 — input**

```text
0000000
0220000
0200000
0000000
0003300
0003000
0000000
```

**Train 1 — output**

```text
0000000
0220000
0220000
0000000
0003300
0003300
0000000
```

**Train 2 — input**

```text
00000000
00044000
00004000
00000000
00550000
00500000
00000000
```

**Train 2 — output**

```text
00000000
00044000
00044000
00000000
00550000
00550000
00000000
```

**Test — input**

```text
000000000
006000000
066000000
000000000
000077000
000070000
000000000
000000550
000000500
```

**Test — expected output**

```text
000000000
066000000
066000000
000000000
000077000
000077000
000000000
000000550
000000550
```

**Written solution**

Look at every 2×2 window. If exactly three cells share the same nonzero color and the fourth cell is 0, fill the missing corner with that color.

**Reference program (`solve_E23`)**

```python
def solve_E23(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                col=nz[0]
                pos=[(r,c),(r,c+1),(r+1,c),(r+1,c+1)]
                for (rr,cc),v in zip(pos,vals):
                    if v==0:
                        out[rr][cc]=col
    return out
```

---

### E24 — Expand exact horizontal triples

**What it tests:** Exact-length run detection with local extension.

**Staged hint:** First detect horizontal runs of length exactly 3; then add one same-colored cell to each open end.

**Train 1 — input**

```text
000000000
000222000
000000000
004444000
000000000
```

**Train 1 — output**

```text
000000000
002222200
000000000
004444000
000000000
```

**Train 2 — input**

```text
00000000
03330000
00000000
00077770
00000000
```

**Train 2 — output**

```text
00000000
33333000
00000000
00077770
00000000
```

**Test — input**

```text
00000000000
00055500000
00000000000
00006666000
00000000000
00777000000
00000000000
```

**Test — expected output**

```text
00000000000
00555550000
00000000000
00006666000
00000000000
07777700000
00000000000
```

**Written solution**

For each horizontal run of length exactly 3, add one same-colored cell immediately to the left and right when those positions are inside the grid and currently 0. Longer runs stay unchanged.

**Reference program (`solve_E24`)**

```python
def solve_E24(g):
    h,w=dims(g); out=clone(g)
    for r,c0,c1,v in horizontal_runs(g):
        if c1-c0+1==3:
            if c0-1>=0 and g[r][c0-1]==0:
                out[r][c0-1]=v
            if c1+1<w and g[r][c1+1]==0:
                out[r][c1+1]=v
    return out
```

---

### E25 — Shift movable cells right

**What it tests:** One-step simultaneous motion with blockers.

**Staged hint:** Treat every nonzero cell independently: if the cell to its right is empty in the input, move it one step right; otherwise keep it in place.

**Train 1 — input**

```text
2003400
0000000
0500060
0000000
```

**Train 1 — output**

```text
0203040
0000000
0050006
0000000
```

**Train 2 — input**

```text
00000000
00670000
00000000
80009000
```

**Train 2 — output**

```text
00000000
00607000
00000000
08000900
```

**Test — input**

```text
300450000
000000000
007000890
000000000
```

**Test — expected output**

```text
030405000
000000000
000700809
000000000
```

**Written solution**

Move every nonzero cell one step to the right if the cell to its right is empty in the input. Cells blocked on the right stay where they are. Apply the move simultaneously.

**Reference program (`solve_E25`)**

```python
def solve_E25(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            if c+1<w and g[r][c+1]==0:
                out[r][c+1]=v if out[r][c+1]==0 else out[r][c+1]
            else:
                out[r][c]=v if out[r][c]==0 else out[r][c]
    return out
```

---

### E26 — Highlight exact vertical triple endpoints

**What it tests:** Exact vertical run length and endpoint targeting.

**Staged hint:** Find vertical runs of length exactly 3. Recolor only the top and bottom cells of each such run to 8.

**Train 1 — input**

```text
000000
003000
003000
003000
000000
000400
000400
000400
000400
```

**Train 1 — output**

```text
000000
008000
003000
008000
000000
000400
000400
000400
000400
```

**Train 2 — input**

```text
0000000
0005000
0005000
0005000
0000000
0600000
0600000
0000000
```

**Train 2 — output**

```text
0000000
0008000
0005000
0008000
0000000
0600000
0600000
0000000
```

**Test — input**

```text
000000000
007000000
007000000
007000000
000000000
000004000
000004000
000004000
000000000
```

**Test — expected output**

```text
000000000
008000000
007000000
008000000
000000000
000008000
000004000
000008000
000000000
```

**Written solution**

Find every vertical run of a single color with length exactly 3. Recolor only the top and bottom cells of that run to 8, leaving the center unchanged.

**Reference program (`solve_E26`)**

```python
def solve_E26(g):
    out=clone(g)
    for c,r0,r1,v in vertical_runs(g):
        if r1-r0+1==3:
            out[r0][c]=8; out[r1][c]=8
    return out
```

---

### E27 — Highlight X-shape centers

**What it tests:** Diagonal pattern detection around a nonzero center.

**Staged hint:** Find cells whose four diagonal neighbors match the center’s color; recolor only those centers.

**Train 1 — input**

```text
0000000
0202000
0020000
0202000
0000000
```

**Train 1 — output**

```text
0000000
0202000
0080000
0202000
0000000
```

**Train 2 — input**

```text
000000000
000303000
000030000
000303000
000000000
006060000
000600000
006060000
000000000
```

**Train 2 — output**

```text
000000000
000303000
000080000
000303000
000000000
006060000
000800000
006060000
000000000
```

**Test — input**

```text
00000000000
00040400000
00004000000
00040400000
00000000000
00000060600
00000006000
00000060600
00000000000
```

**Test — expected output**

```text
00000000000
00040400000
00008000000
00040400000
00000000000
00000060600
00000008000
00000060600
00000000000
```

**Written solution**

Whenever a nonzero center cell has the same color on all four diagonals, recolor that center to 8. Do not change the diagonal arms.

**Reference program (`solve_E27`)**

```python
def solve_E27(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c-1]==v and g[r-1][c+1]==v and g[r+1][c-1]==v and g[r+1][c+1]==v:
                out[r][c]=8
    return out
```

---

### E28 — Singletons become horizontal bars

**What it tests:** Isolated-object detection and controlled local expansion.

**Staged hint:** Detect single cells with no cardinally adjacent nonzero neighbors; then fill their left and right neighbors with the same color.

**Train 1 — input**

```text
0000000
0020000
0000000
0004000
0000000
```

**Train 1 — output**

```text
0000000
0222000
0000000
0044400
0000000
```

**Train 2 — input**

```text
000000000
000050000
000000000
000000700
000000000
```

**Train 2 — output**

```text
000000000
000555000
000000000
000007770
000000000
```

**Test — input**

```text
00000000000
00002000000
00000000000
00000000060
00000000000
00000050000
00000000000
```

**Test — expected output**

```text
00000000000
00022200000
00000000000
00000000666
00000000000
00000555000
00000000000
```

**Written solution**

Every isolated singleton becomes a horizontal bar of length 3: keep the original cell and fill its immediate left and right neighbors with the same color when those cells are available.

**Reference program (`solve_E28`)**

```python
def solve_E28(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            nbrs=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if all(not (0<=nr<h and 0<=nc<w and g[nr][nc]!=0) for nr,nc in nbrs):
                if c-1>=0 and out[r][c-1]==0: out[r][c-1]=v
                if c+1<w and out[r][c+1]==0: out[r][c+1]=v
    return out
```

---

## Medium

### M22 — Keep only one-border objects

**What it tests:** Object extraction plus exact border-touch counting.

**Staged hint:** For each component, count how many distinct outer borders its cells touch. Keep components that touch exactly one border.

**Train 1 — input**

```text
0222000
0000000
0003300
0000300
0000000
0000004
0000004
0000004
0000000
```

**Train 1 — output**

```text
0222000
0000000
0000000
0000000
0000000
0000004
0000004
0000004
0000000
```

**Train 2 — input**

```text
00000000
50000000
50066000
50006000
00000000
00000000
00000000
00777000
```

**Train 2 — output**

```text
00000000
50000000
50000000
50000000
00000000
00000000
00000000
00777000
```

**Test — input**

```text
000222000
000000000
300000007
300660007
300060007
000000000
000000000
000044400
550000000
```

**Test — expected output**

```text
000222000
000000000
300000007
300000007
300000007
000000000
000000000
000000000
000000000
```

**Written solution**

Separate the connected components and count how many distinct outer borders each one touches. Keep only the components that touch exactly one border; erase the rest.

**Reference program (`solve_M22`)**

```python
def solve_M22(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if border_count(cells,h,w)==1:
            for r,c in cells: out[r][c]=col
    return out
```

---

### M23 — Recolor the tallest object

**What it tests:** Component ranking by bbox height.

**Staged hint:** Measure each object’s bounding-box height and recolor the unique tallest one to 8.

**Train 1 — input**

```text
00000000
02220000
00000000
00030000
00030040
00030040
00000040
```

**Train 1 — output**

```text
00000000
02220000
00000000
00080000
00080040
00080040
00000040
```

**Train 2 — input**

```text
000000000
055500000
000000000
000006000
000006000
000006000
000006000
000000700
000000000
```

**Train 2 — output**

```text
000000000
055500000
000000000
000008000
000008000
000008000
000008000
000000700
000000000
```

**Test — input**

```text
0000000000
0222200000
0000000000
0000300000
0000300440
0000300040
0000300040
0000000000
```

**Test — expected output**

```text
0000000000
0222200000
0000000000
0000800000
0000800440
0000800040
0000800040
0000000000
```

**Written solution**

Compute each object’s bounding-box height. Recolor the unique tallest object to 8 and leave every other object unchanged.

**Reference program (`solve_M23`)**

```python
def solve_M23(g):
    comps=components(g)
    chosen=max(comps, key=lambda x: ((bbox(x[1])[1]-bbox(x[1])[0]+1), len(x[1]), -bbox(x[1])[0], -bbox(x[1])[2]))
    out=clone(g)
    for r,c in chosen[1]:
        out[r][c]=8
    return out
```

---

### M24 — Slide every object to the top border

**What it tests:** Per-object translation while preserving local shape.

**Staged hint:** For each component, find its topmost row and shift the whole object upward until that row becomes 0.

**Train 1 — input**

```text
000000000
000000000
002000000
022000000
000000500
000000500
000000000
```

**Train 1 — output**

```text
002000500
022000500
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0000000000
0000400000
0004440000
0000000000
7000000000
7700000000
0000000000
```

**Train 2 — output**

```text
7000400000
7704440000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000000000
00030000000
00333000000
00000000000
00000006000
00000006000
00000000000
00000000009
00000000099
```

**Test — expected output**

```text
00030006009
00333006099
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

For each component, shift it upward until the top of its bounding box reaches row 0. Preserve each object’s shape and columns.

**Reference program (`solve_M24`)**

```python
def solve_M24(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for r,c in cells:
            out[r-r0][c]=col
    return out
```

---

### M25 — Show every object’s bbox corners

**What it tests:** Bounding-box computation divorced from full shape copying.

**Staged hint:** For each component, compute its bounding box and keep only the four corner cells of that box.

**Train 1 — input**

```text
000000000
022200000
020000000
022000000
000000440
000000040
000000440
000000000
```

**Train 1 — output**

```text
000000000
020200000
000000000
020200000
000000440
000000000
000000440
000000000
```

**Train 2 — input**

```text
0000000000
0033300000
0003000000
0003000000
0000000000
0000000550
0000000050
0000000550
```

**Train 2 — output**

```text
0000000000
0030300000
0000000000
0030300000
0000000000
0000000550
0000000000
0000000550
```

**Test — input**

```text
00000000000
04440000000
00400000000
04400000000
00000000000
00000006660
00000000600
00000006600
00000000000
```

**Test — expected output**

```text
00000000000
04040000000
00000000000
04040000000
00000000000
00000006060
00000000000
00000006060
00000000000
```

**Written solution**

Replace every component by the four corner cells of its bounding box, using the component’s original color.

**Reference program (`solve_M25`)**

```python
def solve_M25(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for rr,cc in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            out[rr][cc]=col
    return out
```

---

### M26 — Fill hollow rectangular frames

**What it tests:** Rectangle-frame recognition and interior filling.

**Staged hint:** Identify components that are exactly the one-cell-thick border of an axis-aligned rectangle. Fill the entire rectangle for those components.

**Train 1 — input**

```text
000000000
022220000
020020000
020020000
022220000
000003000
000333000
000003000
000000000
```

**Train 1 — output**

```text
000000000
022220000
022220000
022220000
022220000
000003000
000333000
000003000
000000000
```

**Train 2 — input**

```text
0000000000
0004444000
0004004000
0004444000
0000000000
0555500000
0500500000
0555500000
0000006000
```

**Train 2 — output**

```text
0000000000
0004444000
0004444000
0004444000
0000000000
0555500000
0555500000
0555500000
0000006000
```

**Test — input**

```text
00000000000
02222000000
02002000000
02222000000
00000000000
00005555000
00005005000
00005555000
00000070000
00000777000
00000070000
```

**Test — expected output**

```text
00000000000
02222000000
02222000000
02222000000
00000000000
00005555000
00005555000
00005555000
00000070000
00000777000
00000070000
```

**Written solution**

Identify the components that are exactly one-cell-thick rectangular frames. Fill the entire rectangle for those frame objects and leave non-rectangular objects alone.

**Reference program (`solve_M26`)**

```python
def solve_M26(g):
    out=clone(g)
    for col,cells in components(g):
        if is_rect_frame(cells):
            r0,r1,c0,c1=bbox(cells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=col
    return out
```

---

### M27 — Keep only holed objects

**What it tests:** Hole detection at the component level.

**Staged hint:** Separate the components, then keep only those whose bounding boxes contain enclosed zero regions.

**Train 1 — input**

```text
000000000
022220000
020020000
022220000
000000000
000033300
000030000
000033000
000000000
```

**Train 1 — output**

```text
000000000
022220000
020020000
022220000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0044400000
0040400000
0044400000
0000000000
0000066600
0000006000
0000060000
0000000000
```

**Train 2 — output**

```text
0000000000
0044400000
0040400000
0044400000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
03333000000
03003000000
03333000000
00000000000
00000044400
00000004000
00000044400
00000000000
```

**Test — expected output**

```text
00000000000
03333000000
03003000000
03333000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

Keep only the components that contain at least one enclosed hole inside their bounding boxes. Remove all solid components.

**Reference program (`solve_M27`)**

```python
def solve_M27(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if hole_cells_of_component(g,cells):
            for r,c in cells: out[r][c]=col
    return out
```

---

### M28 — Keep only horizontally symmetric objects

**What it tests:** Local-frame symmetry checking across the horizontal axis.

**Staged hint:** Normalize each object to its own bounding box, reflect it top-to-bottom, and keep only the objects that match.

**Train 1 — input**

```text
000000000
022200000
002000000
022200000
000000000
000044400
000004000
000000000
```

**Train 1 — output**

```text
000000000
022200000
002000000
022200000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0005550000
0000500000
0005550000
0000000000
0000000660
0000000600
0000000000
```

**Train 2 — output**

```text
0000000000
0005550000
0000500000
0005550000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
03330000000
00300000000
03330000000
00000000000
00000007770
00000000700
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
03330000000
00300000000
03330000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

Normalize each object to its own bounding box and reflect it top-to-bottom. Keep the objects whose normalized shape matches that reflection; erase the others.

**Reference program (`solve_M28`)**

```python
def solve_M28(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if is_horiz_symmetric(cells):
            for r,c in cells: out[r][c]=col
    return out
```

---

## Hard

### H22 — Pack normalized objects sorted by perimeter

**What it tests:** Object normalization, geometric ranking, and output resizing.

**Staged hint:** Normalize each component to its own bbox, compute its perimeter, sort by that value, and pack the shapes left-to-right with one blank column between them.

**Train 1 — input**

```text
200000000
000000033
000000033
000400000
000440000
000000000
000000500
000000500
```

**Train 1 — output**

```text
205033040
005033044
```

**Train 2 — input**

```text
0000000000
0600000000
0000007770
0000000700
0000000000
0003300000
0000000000
0000000004
```

**Train 2 — output**

```text
6040330777
0000000070
```

**Test — input**

```text
00000000000
20000000000
00000004400
00000004000
00000000000
00055000000
00055000000
00000000007
```

**Test — expected output**

```text
207044055
000040055
```

**Written solution**

Normalize every object to its own bounding box, compute its perimeter, sort the objects by increasing perimeter, and pack the normalized shapes left-to-right with one blank column between them.

**Reference program (`solve_H22`)**

```python
def solve_H22(g):
    items=[]
    for col,cells in components(g):
        s,h,w=normalize_shape(cells)
        per=perimeter_of_shape(cells)
        r0,r1,c0,c1=bbox(cells)
        items.append((per, r0, c0, s, col, h, w))
    items.sort(key=lambda t:(t[0], t[1], t[2]))
    shapes=[(s,col,h,w) for per,r0,c0,s,col,h,w in items]
    return pack_row(shapes, sep=1)
```

---

### H23 — Rotate each object 90° clockwise in its own frame

**What it tests:** Per-object local-frame rotation without global repositioning.

**Staged hint:** Take each component’s bbox, normalize the shape, rotate it 90° clockwise inside that local frame, and place it back at the same top-left corner.

**Train 1 — input**

```text
000000000
022200000
020000000
000000000
000004000
000044400
000000000
```

**Train 1 — output**

```text
000000000
022000000
002000000
002000000
000040000
000044000
000040000
```

**Train 2 — input**

```text
0000000000
0055000000
0005000000
0005000000
0000000000
0000000660
0000000600
0000000000
```

**Train 2 — output**

```text
0000000000
0000500000
0055500000
0000000000
0000000000
0000000660
0000000060
0000000000
```

**Test — input**

```text
00000000000
03330000000
03000000000
00000000000
00000007700
00000000700
00000000700
00000000000
```

**Test — expected output**

```text
00000000000
03300000000
00300000000
00300000000
00000000070
00000007770
00000000000
00000000000
```

**Written solution**

Take each component in its own bounding box, rotate the normalized shape 90° clockwise, and place it back using the same top-left anchor.

**Reference program (`solve_H23`)**

```python
def solve_H23(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        s,hh,ww=normalize_shape(cells)
        rot={(c, hh-1-r) for r,c in s}
        r0,r1,c0,c1=bbox(cells)
        for r,c in rot:
            out[r0+r][c0+c]=col
    return out
```

---

### H24 — Stamp the rotated template at every marker

**What it tests:** Learning a template, applying a fixed rotation, and stamping copies at multiple anchors.

**Staged hint:** Separate the unique non-9 template from the 9 markers, rotate the template 90° clockwise, then stamp that rotated shape with its top-left corner at every marker.

**Train 1 — input**

```text
220000000
200000000
000000900
000090000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000220
000022020
000002000
```

**Train 2 — input**

```text
0003300000
0000300000
0000300000
0000000000
9000000900
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000000
0000000000
0030000003
3330000333
```

**Test — input**

```text
00004400000
00000400000
00000000000
00000090000
90000000009
00000000000
```

**Test — expected output**

```text
00000000000
00000000000
00000000000
00000004000
04000044000
44000000004
```

**Written solution**

Treat the unique non-9 object as the template. Rotate that template 90° clockwise, then stamp a copy with its top-left corner at every 9 marker. Output only the stamped copies.

**Reference program (`solve_H24`)**

```python
def solve_H24(g):
    comps=components(g)
    # template is unique non-9 component; markers are 9 singletons
    tpl=[(col,cells) for col,cells in comps if col!=9]
    markers=[cells[0] for col,cells in comps if col==9 and len(cells)==1]
    assert len(tpl)==1
    col,cells=tpl[0]
    s,h,w=normalize_shape(cells)
    rot={(c, h-1-r) for r,c in s}
    out=[[0]*len(g[0]) for _ in range(len(g))]
    # stamp rotated shape with top-left at marker
    H,W=dims(g)
    for mr,mc in markers:
        for r,c in rot:
            rr,cc=mr+r,mc+c
            if 0<=rr<H and 0<=cc<W:
                out[rr][cc]=col
    return out
```

---

### H25 — Pack the repeated normalized family

**What it tests:** Shape-family matching independent of translation and color, plus output packing.

**Staged hint:** Normalize every object, group them by shape, pick the family that repeats, and pack just those family members into a single row.

**Train 1 — input**

```text
220000000
200000000
000000330
000000330
000004400
000004000
```

**Train 1 — output**

```text
22044
20040
```

**Train 2 — input**

```text
0000555000
0000050000
0000000000
3300000000
0300000000
0000007700
0000000700
```

**Train 2 — output**

```text
33077
03007
```

**Test — input**

```text
00000000000
02220000000
00200000000
00000000000
00000044400
00000004000
00000000000
00007700000
00007000000
```

**Test — expected output**

```text
2220444
0200040
```

**Written solution**

Normalize all objects, group them by shape, pick the family that appears more than once, and pack those repeated-family members into a single row in reading order.

**Reference program (`solve_H25`)**

```python
def solve_H25(g):
    groups=defaultdict(list)
    for col,cells in components(g):
        s,h,w=normalize_shape(cells)
        r0,r1,c0,c1=bbox(cells)
        groups[(frozenset(s),h,w)].append((r0,c0,col,cells))
    fam=max(groups.items(), key=lambda kv:(len(kv[1]), len(kv[0][0]), kv[0][1], kv[0][2], -min(item[0] for item in kv[1])))
    key,items=fam
    s,h,w=set(key[0]), key[1], key[2]
    items=sorted(items, key=lambda x:(x[0],x[1]))
    shapes=[(s, col, h, w) for r0,c0,col,cells in items]
    return pack_row(shapes, sep=1)
```

---

### H26 — Mirror across the horizontal guide

**What it tests:** Global guide-line reasoning with reflection of multiple objects.

**Staged hint:** Find the full-width row of 9s. Reflect every other object across that row, preserving the guide itself.

**Train 1 — input**

```text
000220000
000200000
000000000
999999999
000000000
000000000
000004400
000000400
```

**Train 1 — output**

```text
000004400
000000000
000000000
999999999
000000000
000200000
000220000
000000000
```

**Train 2 — input**

```text
0000000000
0055500000
0005000000
0000000000
9999999999
0000000000
0000000660
0000000600
0000000000
```

**Train 2 — output**

```text
0000000000
0000000600
0000000660
0000000000
9999999999
0000000000
0005000000
0055500000
0000000000
```

**Test — input**

```text
00000000000
00033000000
00003000000
00000000000
99999999999
00000000000
00000007770
00000000700
00000000000
```

**Test — expected output**

```text
00000000000
00000000700
00000007770
00000000000
99999999999
00000000000
00003000000
00033000000
00000000000
```

**Written solution**

Find the full-width row of 9s and use it as a horizontal mirror line. Reflect every non-9 cell across that guide while keeping the guide row itself.

**Reference program (`solve_H26`)**

```python
def solve_H26(g):
    h,w=dims(g)
    # assume one full-width guide row of 9s
    guide=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            guide=r; break
    assert guide is not None
    out=[[0]*w for _ in range(h)]
    # preserve guide? Maybe output only mirrored objects, no guide. Need decide
    # let's not preserve guide to make task clearer? But mirror across guide maybe preserve? Usually preserve maybe yes.
    for c in range(w):
        out[guide][c]=9
    # objects above guide mirrored below and vice versa
    comps=components(g)
    for col,cells in comps:
        if col==9: continue
        for r,c in cells:
            rr = 2*guide - r
            if 0<=rr<h:
                out[rr][c]=col
    return out
```

---

### H27 — Normalized union of the two largest objects

**What it tests:** Selecting the top two components by size, aligning them locally, and composing an output shape.

**Staged hint:** Take the two largest objects, normalize both to top-left, union their occupied cells, and emit the result in color 8 on the minimal canvas.

**Train 1 — input**

```text
220000000
200000000
000000333
000000003
000000003
000000000
000040000
```

**Train 1 — output**

```text
888
808
008
```

**Train 2 — input**

```text
0000000000
0555000000
0050000000
0000000000
0000000666
0000000006
0000000000
0000000007
```

**Train 2 — output**

```text
888
088
```

**Test — input**

```text
00000000000
04440000000
04000000000
00000000000
00000003330
00000000300
00000000300
00000000000
00000000002
```

**Test — expected output**

```text
888
880
080
```

**Written solution**

Pick the two largest objects, normalize them to the same top-left origin, take the union of their occupied cells, and output that union in color 8 on the minimal canvas.

**Reference program (`solve_H27`)**

```python
def solve_H27(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda x:(-len(x[1]), bbox(x[1])[0], bbox(x[1])[2]))
    (col1,c1),(col2,c2)=comps_sorted[:2]
    s1,h1,w1=normalize_shape(c1); s2,h2,w2=normalize_shape(c2)
    H=max(h1,h2); W=max(w1,w2)
    out=[[0]*W for _ in range(H)]
    for r,c in s1|s2:
        out[r][c]=8
    return out
```

---

### H28 — Normalized difference: largest minus smallest

**What it tests:** Component ranking, local alignment, and shape subtraction.

**Staged hint:** Normalize the largest and smallest objects to the same top-left origin, subtract the smaller shape’s occupied cells from the larger one, and emit the remainder in the larger object’s color.

**Train 1 — input**

```text
022200000
002000000
002000000
000000000
000000330
000000300
```

**Train 1 — output**

```text
002
020
020
```

**Train 2 — input**

```text
0000000000
0555500000
0050000000
0050000000
0000000000
0000000770
```

**Train 2 — output**

```text
0055
0500
0500
```

**Test — input**

```text
00000000000
03333000000
00300000000
00300000000
00000000000
00000000055
```

**Test — expected output**

```text
0033
0300
0300
```

**Written solution**

Pick the largest and smallest objects, normalize them to the same top-left origin, subtract the smaller shape’s occupied cells from the larger shape, and output the remaining cells in the larger object’s color on the minimal canvas.

**Reference program (`solve_H28`)**

```python
def solve_H28(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda x:(-len(x[1]), bbox(x[1])[0], bbox(x[1])[2]))
    (col1,c1),(col2,c2)=comps_sorted[:2]
    s1,h1,w1=normalize_shape(c1); s2,h2,w2=normalize_shape(c2)
    H=max(h1,h2); W=max(w1,w2)
    diff=s1 - s2
    out=[[0]*W for _ in range(H)]
    for r,c in diff:
        out[r][c]=col1
    return out
```

---
