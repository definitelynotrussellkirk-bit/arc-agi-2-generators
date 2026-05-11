# 21 More ARC-Style Puzzles

This is the next continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E15–E21, M15–M21, H15–H21**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

The emphasis in this batch is on clean local operators in the easy tier, object ranking and restructuring in the medium tier, and normalization / composition / analogy in the hard tier.


## Easy

### E15 — Cardinal center fill

**What it tests:** Immediate N/S/E/W agreement around an empty center.

**Staged hint:** First detect empty cells whose four cardinal neighbors match; then copy that shared color into the center.

**Train 1 — input**

```text
0000000
0002000
0020200
0002000
0000000
0003000
0030300
0003000
```

**Train 1 — output**

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

**Train 2 — input**

```text
000000000
000400000
004040000
000400000
000000000
000007000
000070700
000007000
```

**Train 2 — output**

```text
000000000
000400000
004440000
000400000
000000000
000007000
000077700
000007000
```

**Test — input**

```text
000000000
000020000
000202000
000020000
000000000
006000800
060608080
006000800
000000000
```

**Test — expected output**

```text
000000000
000020000
000222000
000020000
000000000
006000800
066608880
006000800
000000000
```

**Written solution**

Whenever a 0 cell has the same nonzero color directly above, below, left, and right, fill that center cell with that color. Leave every other cell unchanged.

**Reference program (`solve_E15`)**

```python
def solve_E15(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0:
                vals=[g[r-1][c],g[r+1][c],g[r][c-1],g[r][c+1]]
                if vals[0]!=0 and len(set(vals))==1:
                    out[r][c]=vals[0]
    return out
```

---

### E16 — Fill the column between matching endpoints

**What it tests:** Column-wise matching endpoints and vertical gap filling.

**Staged hint:** Inspect one column at a time. If the only two nonzero cells in that column match, fill the zeros between them with that color.

**Train 1 — input**

```text
000000
020030
000000
000000
020030
000000
```

**Train 1 — output**

```text
000000
020030
020030
020030
020030
000000
```

**Train 2 — input**

```text
0000000
0005000
0000000
0700000
0000000
0005000
0700000
```

**Train 2 — output**

```text
0000000
0005000
0005000
0705000
0705000
0705000
0700000
```

**Test — input**

```text
00000000
02000040
00000000
00000000
00050000
00000000
02000040
00050000
```

**Test — expected output**

```text
00000000
02000040
02000040
02000040
02050040
02050040
02050040
00050000
```

**Written solution**

Look at each column separately. If a column contains exactly two nonzero cells of the same color and only zeros between them, fill the entire vertical segment from the top endpoint to the bottom endpoint with that color.

**Reference program (`solve_E16`)**

```python
def solve_E16(g):
    h,w=dims(g); out=clone(g)
    for c in range(w):
        nz=[(r,g[r][c]) for r in range(h) if g[r][c]!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            (r0,val),(r1,_) = nz
            if all(g[r][c]==0 for r in range(r0+1,r1)):
                for r in range(r0,r1+1):
                    out[r][c]=val
    return out
```

---

### E17 — Highlight exact triple centers

**What it tests:** Exact-length horizontal run detection.

**Staged hint:** Classify horizontal runs by length first. Only runs of length 3 should change, and only at their middle cell.

**Train 1 — input**

```text
00000000
02220000
00033330
04400000
00005550
00000000
```

**Train 1 — output**

```text
00000000
02820000
00033330
04400000
00005850
00000000
```

**Train 2 — input**

```text
000000000
000666000
077770000
000000222
000000000
```

**Train 2 — output**

```text
000000000
000686000
077770000
000000282
000000000
```

**Test — input**

```text
0000000000
0222000000
0003333000
0000444000
0777000000
0000005555
0000000000
```

**Test — expected output**

```text
0000000000
0282000000
0003333000
0000484000
0787000000
0000005555
0000000000
```

**Written solution**

For every horizontal nonzero run of length exactly 3, recolor only the middle cell to 8. Runs of any other length stay unchanged.

**Reference program (`solve_E17`)**

```python
def solve_E17(g):
    out=clone(g)
    for r,c0,c1,val in horizontal_runs(g):
        if c1-c0+1==3:
            out[r][c0+1]=8
    return out
```

---

### E18 — Drop movable cells by one row

**What it tests:** Simultaneous one-step motion with blocking.

**Staged hint:** Use the original grid to decide which cells can move. A nonzero cell moves down one row only if the cell directly below it is 0.

**Train 1 — input**

```text
020000
000300
000000
004000
000005
```

**Train 1 — output**

```text
000000
020000
000300
000000
004005
```

**Train 2 — input**

```text
000000
060000
060700
000000
000000
```

**Train 2 — output**

```text
000000
060000
000000
060700
000000
```

**Test — input**

```text
0200000
0003000
0000000
0040005
0000000
0006000
```

**Test — expected output**

```text
0000000
0200000
0003000
0000000
0040005
0006000
```

**Written solution**

Every nonzero cell tries to move down by exactly one row. If the cell below it is 0 in the input, it drops there; otherwise it stays where it is. All moves happen simultaneously.

**Reference program (`solve_E18`)**

```python
def solve_E18(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            if r+1<h and g[r+1][c]==0:
                out[r+1][c]=v
            else:
                out[r][c]=v
    return out
```

---

### E19 — Expand isolated singletons to pluses

**What it tests:** Local growth from truly isolated seed cells.

**Staged hint:** Find cells with no nonzero cardinal neighbors. Then add one cell of the same color above, below, left, and right wherever those spots are empty.

**Train 1 — input**

```text
0000000
0002000
0000000
0000000
0050000
0000000
0000000
```

**Train 1 — output**

```text
0002000
0022200
0002000
0050000
0555000
0050000
0000000
```

**Train 2 — input**

```text
00000000
00000000
00060000
00000000
00000070
00000000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00060000
00666000
00060070
00000777
00000070
00000000
00000000
```

**Test — input**

```text
000000000
000020000
000000000
000000000
004000000
000000000
000000800
000000000
000000000
```

**Test — expected output**

```text
000020000
000222000
000020000
004000000
044400000
004000800
000008880
000000800
000000000
```

**Written solution**

Each isolated nonzero cell becomes the center of a plus: keep the original cell and fill its four cardinal neighbors with the same color, as long as those locations are in bounds and currently 0.

**Reference program (`solve_E19`)**

```python
def solve_E19(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            nbrs=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            if all(not (0<=nr<h and 0<=nc<w and g[nr][nc]!=0) for nr,nc in nbrs):
                for nr,nc in nbrs:
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=v
    return out
```

---

### E20 — Diagonalize solid 2x2 blocks

**What it tests:** 2x2 block detection and structured deletion.

**Staged hint:** Scan 2x2 windows. When all four cells are the same nonzero color, keep only the top-left and bottom-right cells of that square.

**Train 1 — input**

```text
0000000
0220000
0220000
0003300
0003300
0000000
```

**Train 1 — output**

```text
0000000
0200000
0020000
0003000
0000300
0000000
```

**Train 2 — input**

```text
04400000
04400000
00000000
00000550
00000550
00000000
00000066
00000066
```

**Train 2 — output**

```text
04000000
00400000
00000000
00000500
00000050
00000000
00000060
00000006
```

**Test — input**

```text
000000000
022000770
022000770
000330000
000330000
000000000
000044000
000044000
000000000
```

**Test — expected output**

```text
000000000
020000700
002000070
000300000
000030000
000000000
000040000
000004000
000000000
```

**Written solution**

Whenever a monochrome 2x2 block appears, erase its top-right and bottom-left cells, leaving only the main diagonal (top-left and bottom-right) in that block. Other cells stay as they were.

**Reference program (`solve_E20`)**

```python
def solve_E20(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
                out[r][c+1]=0
                out[r+1][c]=0
                out[r+1][c+1]=vals[0]
    return out
```

---

### E21 — Mark line endpoints

**What it tests:** Local same-color connectivity and endpoint detection.

**Staged hint:** Count same-color cardinal neighbors for each nonzero cell. Cells with exactly one such neighbor are the endpoints.

**Train 1 — input**

```text
00000000
02222000
00030000
00030000
00030000
00004000
00000000
```

**Train 1 — output**

```text
00000000
08228000
00080000
00030000
00080000
00004000
00000000
```

**Train 2 — input**

```text
000000000
000660000
000000000
055555000
000700000
000700000
000000000
```

**Train 2 — output**

```text
000000000
000880000
000000000
085558000
000800000
000800000
000000000
```

**Test — input**

```text
000000000
022200000
000000000
000330000
000030000
000030000
000000000
000000440
```

**Test — expected output**

```text
000000000
082800000
000000000
000830000
000030000
000080000
000000000
000000880
```

**Written solution**

A nonzero cell is an endpoint if it has exactly one same-colored cardinal neighbor. Recolor all such endpoints to 8 and leave every other cell unchanged.

**Reference program (`solve_E21`)**

```python
def solve_E21(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if not v: continue
            cnt=sum(1 for nr,nc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)] if 0<=nr<h and 0<=nc<w and g[nr][nc]==v)
            if cnt==1:
                out[r][c]=8
    return out
```

---


## Medium

### M15 — Keep only square-bbox objects

**What it tests:** Connected components and bounding-box geometry.

**Staged hint:** Detect each object first, then compute its bounding box. Preserve the object only if that box is as tall as it is wide.

**Train 1 — input**

```text
22000000
22000000
00030000
00030000
00030000
00000044
```

**Train 1 — output**

```text
22000000
22000000
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
000000000
000555000
000505000
000555000
700000660
770000000
000000000
```

**Train 2 — output**

```text
000000000
000555000
000505000
000555000
700000000
770000000
000000000
```

**Test — input**

```text
000000000
022000000
020000000
000000333
000000303
000000333
000044440
000000000
000000000
```

**Test — expected output**

```text
000000000
022000000
020000000
000000333
000000303
000000333
000000000
000000000
000000000
```

**Written solution**

Treat each connected nonzero object separately. Keep an object if its bounding box is square; erase it otherwise. The object's exact shape does not matter beyond its bounding-box size.

**Reference program (`solve_M15`)**

```python
def solve_M15(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        if (r1-r0)==(c1-c0):
            for r,c in cells: out[r][c]=col
    return out
```

---

### M16 — Recolor the object closest to the grid center

**What it tests:** Ranking whole objects by location rather than by size.

**Staged hint:** Compute a center point for each object's bounding box and compare its distance to the center of the whole grid.

**Train 1 — input**

```text
220000000
220000000
000000000
000033000
000033000
000000000
000000044
000000044
000000000
```

**Train 1 — output**

```text
220000000
220000000
000000000
000088000
000088000
000000000
000000044
000000044
000000000
```

**Train 2 — input**

```text
000000000
077000000
077000000
000000000
000055000
000055000
000000000
000000330
000000330
```

**Train 2 — output**

```text
000000000
077000000
077000000
000000000
000088000
000088000
000000000
000000330
000000330
```

**Test — input**

```text
00000000000
22000000000
22000000000
00000000000
00000440000
00000440000
00000000000
00000000066
00000000066
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
22000000000
22000000000
00000000000
00000880000
00000880000
00000000000
00000000066
00000000066
00000000000
00000000000
```

**Written solution**

Find the object whose bounding-box center is closest to the center of the full grid, using Manhattan distance. Recolor that one object to 8 and leave every other object unchanged.

**Reference program (`solve_M16`)**

```python
def solve_M16(g):
    h,w=dims(g)
    comps=components(g)
    def score(item):
        _,cells=item
        r0,r1,c0,c1=bbox(cells)
        return (abs((r0+r1)-(h-1))+abs((c0+c1)-(w-1)), len(cells), r0, c0)
    chosen=min(comps,key=score)
    out=clone(g)
    for r,c in chosen[1]: out[r][c]=8
    return out
```

---

### M17 — Slide every object to the left border

**What it tests:** Object-wise translation while preserving shape.

**Staged hint:** Work component by component. For each object, subtract its minimum column from every cell coordinate so its left edge lands on column 0.

**Train 1 — input**

```text
000000000
000022000
000022000
000000000
000000330
000000330
000000000
```

**Train 1 — output**

```text
000000000
220000000
220000000
000000000
330000000
330000000
000000000
```

**Train 2 — input**

```text
0000000000
0000000440
0000000440
0000000000
0007770000
0007770000
0000000000
0000000066
```

**Train 2 — output**

```text
0000000000
4400000000
4400000000
0000000000
7770000000
7770000000
0000000000
6600000000
```

**Test — input**

```text
0000000000
0000220000
0000220000
0000000000
0000003300
0000003300
0000000000
0000000007
0000000000
```

**Test — expected output**

```text
0000000000
2200000000
2200000000
0000000000
3300000000
3300000000
0000000000
7000000000
0000000000
```

**Written solution**

Move each connected object horizontally as far left as possible until its bounding box touches column 0. Preserve its rows, color, and internal shape exactly.

**Reference program (`solve_M17`)**

```python
def solve_M17(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        for r,c in cells: out[r][c-c0]=col
    return out
```

---

### M18 — Reduce each object to its bbox center

**What it tests:** Collapsing objects to a derived representative cell.

**Staged hint:** For every object, compute the center cell of its bounding box. Keep only that single cell in the output.

**Train 1 — input**

```text
000000000
022200000
022200000
022200000
000000000
000030000
000030000
000030000
000000000
```

**Train 1 — output**

```text
000000000
000000000
002000000
000000000
000000000
000000000
000030000
000000000
000000000
```

**Train 2 — input**

```text
000000000
000040000
000444000
000040000
000000000
000005550
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000040000
000000000
000000000
000000500
000000000
000000000
000000000
```

**Test — input**

```text
000000000
000222000
000202000
000222000
000000000
000000330
000000330
000000330
000000000
```

**Test — expected output**

```text
000000000
000000000
000020000
000000000
000000000
000000000
000000300
000000000
000000000
```

**Written solution**

Replace every object by a single cell at the center of its bounding box. The color is preserved, but all other cells of the object disappear.

**Reference program (`solve_M18`)**

```python
def solve_M18(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        out[(r0+r1)//2][(c0+c1)//2]=col
    return out
```

---

### M19 — Crop to the active area

**What it tests:** Global output resizing based on nonzero support.

**Staged hint:** Find the smallest rectangle that contains every nonzero cell. Output exactly that crop and discard the surrounding empty border.

**Train 1 — input**

```text
000000000
000220000
000220000
000000000
000000300
000000000
```

**Train 1 — output**

```text
2200
2200
0000
0003
```

**Train 2 — input**

```text
0000000000
0000000000
0044000000
0044000000
0000000000
0000000007
0000000000
```

**Train 2 — output**

```text
44000000
44000000
00000000
00000007
```

**Test — input**

```text
00000000000
00000000000
00005500000
00005000000
00005500000
00000000000
00000000060
00000000000
```

**Test — expected output**

```text
550000
500000
550000
000000
000006
```

**Written solution**

Ignore the blank margin. Output the tightest rectangular crop that still contains all the nonzero cells from the input.

**Reference program (`solve_M19`)**

```python
def solve_M19(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]
```

---

### M20 — Fill holes of all hollow objects

**What it tests:** Hole detection inside multiple components.

**Staged hint:** Identify each object, then find zero regions fully enclosed inside its bounding box. Fill those enclosed holes with the object's own color.

**Train 1 — input**

```text
000000000
022200000
020200000
022200000
000003330
000003030
000003330
```

**Train 1 — output**

```text
000000000
022200000
022200000
022200000
000003330
000003330
000003330
```

**Train 2 — input**

```text
0000000000
0444400000
0400400000
0400400000
0444400000
0000000000
0000002220
0000002020
0000002220
```

**Train 2 — output**

```text
0000000000
0444400000
0444400000
0444400000
0444400000
0000000000
0000002220
0000002220
0000002220
```

**Test — input**

```text
00000000000
02220000000
02020000000
02220000000
00000000000
00000333300
00000300300
00000333300
00000000000
00000044440
00000040040
00000044440
```

**Test — expected output**

```text
00000000000
02220000000
02220000000
02220000000
00000000000
00000333300
00000333300
00000333300
00000000000
00000044440
00000044440
00000044440
```

**Written solution**

Every hollow object becomes solid. For each connected component, fill any fully enclosed zero hole inside that object's boundary with the same color as the object.

**Reference program (`solve_M20`)**

```python
def solve_M20(g):
    out=clone(g)
    for col,cells in components(g):
        for region in hole_cells_of_component(g,cells):
            for r,c in region: out[r][c]=col
    return out
```

---

### M21 — Fill rectangles from color-matched point pairs

**What it tests:** Grouping single-cell markers by color and generating shapes from them.

**Staged hint:** Each nonzero color appears exactly twice. Take those two cells as opposite corners and fill the full axis-aligned rectangle between them.

**Train 1 — input**

```text
000000000
020000300
000000000
000000000
020003000
000000000
```

**Train 1 — output**

```text
000000000
020003300
020003300
020003300
020003300
000000000
```

**Train 2 — input**

```text
00000000
00040000
00000000
00000006
00000000
04000000
00000006
00000000
```

**Train 2 — output**

```text
00000000
04440000
04440000
04440006
04440006
04440006
00000006
00000000
```

**Test — input**

```text
0000000000
0200000000
0000005000
0000000000
0200005000
0000000000
0007000000
0000000000
0000000700
0000000000
```

**Test — expected output**

```text
0000000000
0200000000
0200005000
0200005000
0200005000
0000000000
0007777700
0007777700
0007777700
0000000000
```

**Written solution**

For each color, find its two single-cell markers and treat them as opposite corners of a rectangle. Fill that entire rectangle with the same color.

**Reference program (`solve_M21`)**

```python
def solve_M21(g):
    h,w=dims(g); by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: by[g[r][c]].append((r,c))
    out=[[0]*w for _ in range(h)]
    for col,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            for r in range(min(r1,r2),max(r1,r2)+1):
                for c in range(min(c1,c2),max(c1,c2)+1):
                    out[r][c]=col
    return out
```

---


## Hard

### H15 — Extract the odd normalized shape

**What it tests:** Shape normalization, congruence, and outlier detection.

**Staged hint:** Normalize every object to its own top-left corner. Two normalized shapes will match exactly; output the one normalized shape that does not match the others.

**Train 1 — input**

```text
0000000000
0200002000
0200002000
0220002200
0000000000
0000222000
0000020000
0000020000
0000000000
```

**Train 1 — output**

```text
222
020
020
```

**Train 2 — input**

```text
000000000
044000440
044000440
000000000
000660000
000060000
000060000
000000000
000000000
```

**Train 2 — output**

```text
66
06
06
```

**Test — input**

```text
0000000000
0700007000
0700007000
0770007700
0000000000
0000550000
0005550000
0000500000
0000000000
```

**Test — expected output**

```text
055
555
050
```

**Written solution**

Normalize every connected object by moving its bounding box to the top-left corner. Two objects are the same shape after normalization; the third is different. Output just that odd normalized shape in its original color.

**Reference program (`solve_H15`)**

```python
def solve_H15(g):
    reps=[]
    for col,cells in components(g):
        shape,(H,W)=crop_cells(cells)
        reps.append((col,shape,H,W))
    counts=Counter((frozenset(shape),H,W) for col,shape,H,W in reps)
    odd=[item for item in reps if counts[(frozenset(item[1]),item[2],item[3])]==1]
    assert len(odd)==1
    col,shape,H,W=odd[0]
    out=[[0]*W for _ in range(H)]
    for r,c in shape: out[r][c]=col
    return out
```

---

### H16 — Stamp the template at every 9 marker

**What it tests:** Separating a template object from destination markers and replicating it.

**Staged hint:** First isolate the one non-9 object as the template. Normalize it, then place a copy with its top-left corner anchored at each 9 marker.

**Train 1 — input**

```text
00000000
02000090
02000000
02200000
00000000
00090000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000020
00000020
00000022
00000000
00020000
00020000
00022000
```

**Train 2 — input**

```text
0000000000
0055500000
0005000900
0000000000
0000000000
9000000000
0000009000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000555
0000000050
0000000000
5550000000
0500005550
0000000500
0000000000
0000000000
```

**Test — input**

```text
0000000000
0007700000
0000700090
0000700000
0000000000
9000000000
0000009000
0000000000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000000077
0000000007
0000000007
7700000000
0700007700
0700000700
0000000700
0000000000
```

**Written solution**

There is one template object and several 9 markers. Remove the template from its original location and draw a copy of it at every 9 marker, aligning the template's top-left corner with the marker cell.

**Reference program (`solve_H16`)**

```python
def solve_H16(g):
    h,w=dims(g)
    comps=[(col,cells) for col,cells in components(g) if col!=9]
    assert len(comps)==1
    col,cells=comps[0]
    shape,(H,W)=crop_cells(cells)
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=[[0]*w for _ in range(h)]
    for mr,mc in markers:
        for r,c in shape:
            out[mr+r][mc+c]=col
    return out
```

---

### H17 — Normalized overlay with overlap color 8

**What it tests:** Combining two normalized shapes into one derived output.

**Staged hint:** Normalize both objects to the same origin. Cells occupied by only one shape keep that shape's color; cells occupied by both become 8.

**Train 1 — input**

```text
000000000
022000000
020000000
020000000
000000000
000033300
000003000
000003000
000000000
```

**Train 1 — output**

```text
883
230
230
```

**Train 2 — input**

```text
000000000
044400000
000400000
000000000
000000660
000000060
000000060
000000000
000000000
```

**Train 2 — output**

```text
884
064
060
```

**Test — input**

```text
000000000
055000000
055000000
050000000
000000000
000007700
000000700
000000700
000000000
```

**Test — expected output**

```text
88
58
57
```

**Written solution**

Normalize the two objects to the top-left corner of their own bounding boxes and overlay them on a common canvas. Unique cells keep their original colors; overlapping cells become color 8.

**Reference program (`solve_H17`)**

```python
def solve_H17(g):
    comps=components(g); assert len(comps)==2
    (col1,cells1),(col2,cells2)=comps
    shape1,(H1,W1)=crop_cells(cells1)
    shape2,(H2,W2)=crop_cells(cells2)
    H=max(H1,H2); W=max(W1,W2)
    s1=set(shape1); s2=set(shape2)
    out=[[0]*W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if (r,c) in s1 and (r,c) in s2: out[r][c]=8
            elif (r,c) in s1: out[r][c]=col1
            elif (r,c) in s2: out[r][c]=col2
    return out
```

---

### H18 — Mirror across the vertical guide

**What it tests:** Global reflection relative to an explicit axis marker.

**Staged hint:** Find the column formed by the 7 guide line. Keep the original non-guide object and reflect each of its cells across that vertical axis.

**Train 1 — input**

```text
000070000
020070000
020070000
022070000
000070000
000070000
000070000
000070000
000070000
```

**Train 1 — output**

```text
000000000
020000020
020000020
022000220
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000700000
0000700400
0000700400
0000700440
0000700000
0000700000
0000700000
0000700000
0000700000
0000700000
```

**Train 2 — output**

```text
0000000000
0400000400
0400000400
4400000440
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
0000070000
0000070000
0020070000
0020070000
0022070000
0000070000
0000070000
0000070000
0000070000
0000070000
```

**Test — expected output**

```text
0000000000
0000000000
0020000020
0020000020
0022000220
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Written solution**

A vertical line of 7s marks the mirror axis. Ignore the guide in the final output, keep the original object, and add its reflected copy across that axis in the same color.

**Reference program (`solve_H18`)**

```python
def solve_H18(g):
    h,w=dims(g)
    axis_cols={c for r in range(h) for c in range(w) if g[r][c]==7}
    assert len(axis_cols)==1
    axis=next(iter(axis_cols))
    out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=7:
                out[r][c]=v
                mc=2*axis-c
                if 0<=mc<w: out[r][mc]=v
    return out
```

---

### H19 — Pack normalized objects sorted by hole count

**What it tests:** Hole counting, normalization, sorting, and output packing.

**Staged hint:** Normalize each object, count how many enclosed holes it has, sort the normalized objects by that count, and pack them left-to-right with a one-column gap.

**Train 1 — input**

```text
220000000000000
220000000000000
000000333000000
000000303000000
000000333000000
000000000000000
000000000044444
000000000040004
000000000044444
000000000040004
000000000044444
```

**Train 1 — output**

```text
220333044444
220303040004
000333044444
000000040004
000000044444
```

**Train 2 — input**

```text
000000000000000
055000000000000
050000000000000
055000000000000
000000000000000
000003330000000
000003030000000
000003330000000
000000000000000
000000000066666
000000000060006
000000000066666
000000000060006
000000000066666
```

**Train 2 — output**

```text
550333066666
500303060006
550333066666
000000060006
000000066666
```

**Test — input**

```text
770000000000000
770000000000000
000000222000000
000000202000000
000000222000000
000000000000000
000000000055555
000000000050005
000000000055555
000000000050005
000000000055555
```

**Test — expected output**

```text
770222055555
770202050005
000222055555
000000050005
000000055555
```

**Written solution**

For each object, count its enclosed holes after identifying its bounding box. Normalize every object to the top-left corner, sort them by number of holes, and pack them into a single row with one blank column between neighbors.

**Reference program (`solve_H19`)**

```python
def solve_H19(g):
    items=[]
    for col,cells in components(g):
        shape,(H,W)=crop_cells(cells)
        holes=len(hole_cells_of_component(g,cells))
        items.append((holes,col,shape,H,W))
    items.sort(key=lambda x:(x[0],x[1]))
    total_w=sum(W for _,_,_,_,W in items)+max(0,len(items)-1)
    max_h=max(H for _,_,_,H,_ in items)
    out=[[0]*total_w for _ in range(max_h)]
    cur=0
    for holes,col,shape,H,W in items:
        for r,c in shape:
            out[r][cur+c]=col
        cur += W+1
    return out
```

---

### H20 — Add the missing fourth translated copy

**What it tests:** Object congruence plus 2D translation analogy.

**Staged hint:** All visible objects are identical up to translation. Use the top-left copy as the reference, find the horizontal and vertical translation vectors, and place the missing copy at the fourth corner.

**Train 1 — input**

```text
0000000000
0200002000
0200002000
0220002200
0000000000
0000000000
0200000000
0200000000
0220000000
0000000000
```

**Train 1 — output**

```text
0000000000
0200002000
0200002000
0220002200
0000000000
0000000000
0200002000
0200002000
0220002200
0000000000
```

**Train 2 — input**

```text
444000044400
040000004000
000000000000
000000000000
444000000000
040000000000
000000000000
000000000000
```

**Train 2 — output**

```text
444000044400
040000004000
000000000000
000000000000
444000044400
040000004000
000000000000
000000000000
```

**Test — input**

```text
055000005500
005000000500
005000000500
000000000000
000000000000
055000000000
005000000000
005000000000
000000000000
000000000000
```

**Test — expected output**

```text
055000005500
005000000500
005000000500
000000000000
000000000000
055000005500
005000000500
005000000500
000000000000
000000000000
```

**Written solution**

The input shows three translated copies of the same shape arranged like three corners of a rectangle. Add the missing fourth copy at the final corner, preserving the same color and orientation.

**Reference program (`solve_H20`)**

```python
def solve_H20(g):
    comps=components(g)
    items=[]
    common=None
    for col,cells in comps:
        shape,(H,W)=crop_cells(cells)
        items.append((col,shape,H,W,bbox(cells)[0],bbox(cells)[2]))
        if common is None: common=frozenset(shape)
        else: assert frozenset(shape)==common
    pivot=min(items,key=lambda t:(t[4],t[5]))
    horiz=[it for it in items if it[4]==pivot[4] and it[5]!=pivot[5]]
    vert=[it for it in items if it[5]==pivot[5] and it[4]!=pivot[4]]
    assert horiz and vert
    col,shape,H,W,_,_=pivot
    mr=vert[0][4]; mc=horiz[0][5]
    out=clone(g)
    for r,c in shape: out[mr+r][mc+c]=col
    return out
```

---

### H21 — Reconstruct the full shape by normalized union

**What it tests:** Combining multiple partial observations of one latent shape.

**Staged hint:** Normalize each same-colored component to its own top-left corner. Take the union of all occupied normalized coordinates and output that reconstructed shape once.

**Train 1 — input**

```text
0000000000
0220000000
0020000000
0020000000
0000000000
0000022000
0000002000
0000002000
0000000000
0000000222
0000000020
0000000000
```

**Train 1 — output**

```text
222
020
020
```

**Train 2 — input**

```text
000000000
055000000
005500000
000000000
000055000
000005500
000000000
000000055
000000005
```

**Train 2 — output**

```text
550
055
```

**Test — input**

```text
0000000000
0660000000
0060000000
0060000000
0000000000
0000006600
0000000600
0000000000
0000660000
0000600000
```

**Test — expected output**

```text
66
66
06
```

**Written solution**

Every component is a partial version of the same underlying shape. Normalize them all to a common origin, take the union of their occupied cells, and output that reconstructed full shape once in the original color.

**Reference program (`solve_H21`)**

```python
def solve_H21(g):
    comps=components(g)
    col=comps[0][0]
    union=set()
    for _,cells in comps:
        shape,(H,W)=crop_cells(cells)
        union |= set(shape)
    H=max(r for r,c in union)+1
    W=max(c for r,c in union)+1
    out=[[0]*W for _ in range(H)]
    for r,c in union: out[r][c]=col
    return out
```

---
