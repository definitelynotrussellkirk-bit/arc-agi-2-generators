# 21 More ARC-Style Puzzles

This is the fifth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E29–E35, M29–M35, H29–H35**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch deliberately broadens the operation mix. In addition to local motifs and object selection, it leans into legends, masks, panel analogies, and one new reusable primitive:

**New primitive — `sweep_shadow(cells, direction, stop)`**

Interpret a shape as something that can be **extruded** in a direction. The primitive paints the entire swept path of that shape until a border or barrier stops it. It shows up most directly in **M31** and **H29**.

## Easy

### E29 — Diagonal bridge between matching endpoints

**What it tests:** Detect isolated same-color diagonal endpoints and fill the 45° path between them.

**Staged hint:** Group cells by color first. If a color appears as exactly two isolated endpoints on a diagonal, fill only the cells strictly between them.

**Train 1 — input**

```text
2000000
0000000
0000000
0002000
0000400
0000000
0040000
```

**Train 1 — output**

```text
2000000
0200000
0020000
0002000
0000400
0004000
0040000
```

**Train 2 — input**

```text
00000003
00000000
00500000
00000000
00000000
00000500
00000000
30000000
```

**Train 2 — output**

```text
00000003
00000030
00500300
00053000
00035000
00300500
03000000
30000000
```

**Test — input**

```text
000000007
000000000
000200000
000000000
000000200
000000000
040000000
000000000
700000004
```

**Test — expected output**

```text
000000007
000000070
000200700
000007000
000070200
000700000
047000000
070000000
700000004
```

**Written solution**

For each color, find the two cells of that color. If they lie on a 45° diagonal and every intermediate cell is 0, fill the cells between them with that color. Leave every other cell unchanged.

**Reference program (`solve_E29`)**

```python
def solve_E29(g):
    h,w=dims(g); out=clone(g)
    pos=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                pos[g[r][c]].append((r,c))
    for col,cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if abs(dr)==abs(dc) and abs(dr)>=2:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                ok=True
                for k in range(1,abs(dr)):
                    if g[r1+k*sr][c1+k*sc]!=0:
                        ok=False; break
                if ok:
                    for k in range(1,abs(dr)):
                        out[r1+k*sr][c1+k*sc]=col
    return out
```

---

### E30 — Highlight exact T-centers

**What it tests:** Recognize degree-3 cardinal junctions rather than pluses or lines.

**Staged hint:** Ignore diagonal neighbors. A center should have exactly three same-color neighbors among up, down, left, and right.

**Train 1 — input**

```text
0000000
0002000
0022200
0000000
0003300
0000300
0000300
```

**Train 1 — output**

```text
0000000
0002000
0028200
0000000
0003300
0000300
0000300
```

**Train 2 — input**

```text
00000000
00000000
00044400
00004000
00000000
00060000
00666000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00048400
00004000
00000000
00060000
00686000
00000000
```

**Test — input**

```text
000700000
007770000
000000000
000000500
000005500
000000500
000000000
000040000
000000000
```

**Test — expected output**

```text
000700000
007870000
000000000
000000500
000005800
000000500
000000000
000040000
000000000
```

**Written solution**

Whenever a nonzero cell has exactly three same-color cardinal neighbors, recolor that center cell to 8. The arms stay in their original color.

**Reference program (`solve_E30`)**

```python
def solve_E30(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v==0: 
                continue
            same=sum(g[r+dr][c+dc]==v for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)])
            if same==3:
                out[r][c]=8
    return out
```

---

### E31 — Complete diagonal corners to squares

**What it tests:** Use tiny 2×2 windows and infer the missing orthogonal pair from a diagonal pair.

**Staged hint:** Slide a 2×2 window over the grid. When the two occupied cells are diagonal corners of the same color and the other two are 0, fill the other two.

**Train 1 — input**

```text
0000000
0200000
0020000
0000000
0000400
0004000
0000000
```

**Train 1 — output**

```text
0000000
0220000
0220000
0000000
0004400
0004400
0000000
```

**Train 2 — input**

```text
00000000
00050000
00005000
00000000
00600000
00060000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00055000
00055000
00000000
00660000
00660000
00000000
00000000
```

**Test — input**

```text
000000000
007000000
000700000
000000000
000020000
000200000
000000000
000000400
000000040
```

**Test — expected output**

```text
000000000
007700000
007700000
000000000
000220000
000220000
000000000
000000440
000000440
```

**Written solution**

Inspect every 2×2 block. If exactly two same-colored cells occupy opposite corners and the other two positions are empty, fill the empty positions with that same color to complete the square.

**Reference program (`solve_E31`)**

```python
def solve_E31(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            a,b,c1,d = g[r][c], g[r][c+1], g[r+1][c], g[r+1][c+1]
            vals=[a,b,c1,d]
            if a==d!=0 and b==0 and c1==0:
                out[r][c+1]=a; out[r+1][c]=a
            if b==c1!=0 and a==0 and d==0:
                out[r][c]=b; out[r+1][c+1]=b
    return out
```

---

### E32 — Singletons become X-shapes

**What it tests:** Expand truly isolated cells into a diagonal cross while preserving the original center.

**Staged hint:** First identify cells with no nonzero neighbors in the full 8-neighborhood. Only those cells should sprout diagonal arms.

**Train 1 — input**

```text
000000000
002000000
000000000
000000000
000040000
000000000
000000000
000000006
000000000
```

**Train 1 — output**

```text
020200000
002000000
020200000
000404000
000040000
000404000
000000060
000000006
000000060
```

**Train 2 — input**

```text
00000000000
00030000000
00000000000
00000000000
00000005000
00000000000
00000000000
70000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00303000000
00030000000
00303000000
00000050500
00000005000
00000050500
07000000000
70000000000
07000000000
00000000000
00000000000
```

**Test — input**

```text
00000000000
00000020000
00000000000
00000000000
00004000000
00000000000
00000000000
00000000070
00000000000
00000000000
00000000000
```

**Test — expected output**

```text
00000202000
00000020000
00000202000
00040400000
00004000000
00040400000
00000000707
00000000070
00000000707
00000000000
00000000000
```

**Written solution**

Find each isolated nonzero cell, meaning no nonzero cell touches it in any of the eight neighboring positions. Around each such cell, add the four diagonal neighbors in the same color when they fit inside the grid.

**Reference program (`solve_E32`)**

```python
def solve_E32(g):
    h,w=dims(g); out=clone(g)
    dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            # isolated in 8-neighborhood
            iso=True
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0: continue
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and g[nr][nc]!=0:
                        iso=False
            if iso:
                for dr,dc in dirs:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=v
    return out
```

---

### E33 — Shift movable cells down-right

**What it tests:** Apply a uniform diagonal motion rule with edge blocking.

**Staged hint:** Test the destination in the original grid, not after earlier moves. If the down-right cell is empty and inside the grid, move there; otherwise keep the cell where it is.

**Train 1 — input**

```text
2000000
0003000
0000000
0000400
0000000
0000005
0000000
```

**Train 1 — output**

```text
0000000
0200000
0000300
0000000
0000040
0000005
0000000
```

**Train 2 — input**

```text
00000000
06000000
00000000
00070000
00000000
00000008
00000000
90000000
```

**Train 2 — output**

```text
00000000
00000000
00600000
00000000
00007000
00000008
00000000
90000000
```

**Test — input**

```text
000000000
020000000
000000000
000040000
000000000
000000060
000000000
700000000
000000000
```

**Test — expected output**

```text
000000000
000000000
002000000
000000000
000004000
000000000
000000006
000000000
070000000
```

**Written solution**

Move every nonzero cell one step down and one step right if that destination is inside the grid and is 0 in the input. If the move would leave the grid or land on a nonzero cell, keep the cell in place.

**Reference program (`solve_E33`)**

```python
def solve_E33(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    # move if down-right empty in original and in bounds
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            nr,nc=r+1,c+1
            if nr<h and nc<w and g[nr][nc]==0:
                out[nr][nc]=v if out[nr][nc]==0 else out[nr][nc]
            else:
                out[r][c]=v if out[r][c]==0 else out[r][c]
    return out
```

---

### E34 — Mirror singletons across a guide wall

**What it tests:** Reflect sparse colored cells across a full-height guide column.

**Staged hint:** Locate the solid column of 9s first. Then reflect every nonzero non-9 cell across that column, copying rather than moving.

**Train 1 — input**

```text
000900000
020900000
000900500
000900000
300900000
000900000
000900040
```

**Train 1 — output**

```text
000900000
020902000
500900500
000900000
300900300
000900000
000900040
```

**Train 2 — input**

```text
0000900000
0060900000
0000900000
0000907000
0000900000
5000900000
0000900000
0000900000
```

**Train 2 — output**

```text
0000900000
0060906000
0000900000
0070907000
0000900000
5000900050
0000900000
0000900000
```

**Test — input**

```text
00000900000
00000902000
70000900000
00000900000
00000900000
00000900040
00000900000
00000960000
```

**Test — expected output**

```text
00000900000
00020902000
70000900007
00000900000
00000900000
04000900040
00000900000
00006960000
```

**Written solution**

Find the vertical column made entirely of 9s. For each other nonzero cell, place a copy at the reflected position across that guide column, keeping the original cells and the guide unchanged.

**Reference program (`solve_E34`)**

```python
def solve_E34(g):
    h,w=dims(g)
    guide=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            guide=c; break
    out=clone(g)
    if guide is None: return out
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                mc=2*guide-c
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=v
    return out
```

---

### E35 — Row header paints the 8 marker

**What it tests:** Use a simple row-wise legend: the first column gives the replacement color for the row’s 8.

**Staged hint:** Read each row independently. The leftmost nonzero entry is the color instruction for that row.

**Train 1 — input**

```text
0000000
2008000
0000000
3000080
4000008
0000000
```

**Train 1 — output**

```text
0000000
2002000
0000000
3000030
4000004
0000000
```

**Train 2 — input**

```text
000000000
500000080
000000000
600800000
700000008
000000000
200080000
```

**Train 2 — output**

```text
000000000
500000050
000000000
600600000
700000007
000000000
200020000
```

**Test — input**

```text
0000000000
3000008000
0000000000
5000800000
6000000008
0000000000
2000080000
0000000000
```

**Test — expected output**

```text
0000000000
3000003000
0000000000
5000500000
6000000006
0000000000
2000020000
0000000000
```

**Written solution**

In any row whose first cell is a nonzero color, replace every 8 in that row with the row’s first-cell color. Everything else stays the same.

**Reference program (`solve_E35`)**

```python
def solve_E35(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        c0=g[r][0]
        if c0!=0:
            for c in range(1,w):
                if g[r][c]==8:
                    out[r][c]=c0
    return out
```

---

## Medium

### M29 — Keep the object whose area matches the header count

**What it tests:** Use a count in a header row to select one object by area.

**Staged hint:** Count the 1s in the top row first. Then compare that count with component sizes in the body.

**Train 1 — input**

```text
0111100000
0000000000
0003300000
0003300000
0000000000
0500000000
0500000220
0500000200
0000000220
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0003300000
0003300000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
01111100000
00000000000
00044000000
00044000000
00004000000
00000000000
00777000000
00000000000
00000066000
00000066000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00044000000
00044000000
00004000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Test — input**

```text
011111100000
000000000000
000000000000
000222000000
000222000000
000000000000
000055500000
000050000000
000000000000
000000077000
000000077000
000000007000
```

**Test — expected output**

```text
000000000000
000000000000
000000000000
000222000000
000222000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Written solution**

Count how many 1s appear in the top row. In the rows below, keep only the connected component whose number of cells equals that count, and erase every other body object and the header.

**Reference program (`solve_M29`)**

```python
def solve_M29(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    out=[[0]*w for _ in range(h)]
    comps=components([row[:] for row in g[1:]])  # body relative coords
    # need original coords
    body=[row[:] for row in g[1:]]
    for col,cells in components(body):
        if len(cells)==k:
            for r,c in cells:
                out[r+1][c]=col
    return out
```

---

### M30 — Recolor the body from a two-row legend

**What it tests:** Decode a source→target color mapping from stacked header rows and apply it only to the body.

**Staged hint:** Build the color map from corresponding nonzero entries in the first two rows. Then recolor rows below the legend without changing the legend itself.

**Train 1 — input**

```text
20304000
50607000
00000000
00233040
00200040
00044000
03322000
```

**Train 1 — output**

```text
20304000
50607000
00000000
00566070
00500070
00077000
06655000
```

**Train 2 — input**

```text
04002030
07005060
00000000
00400230
00020030
00334000
02000040
```

**Train 2 — output**

```text
04002030
07005060
00000000
00700560
00050060
00667000
05000070
```

**Test — input**

```text
03004020
06007050
00000000
00340020
00004020
02233000
00400030
```

**Test — expected output**

```text
03004020
06007050
00000000
00670050
00007050
05566000
00700060
```

**Written solution**

Treat the first row as source colors and the second row as target colors at matching columns. Recolor every body cell according to that mapping, while leaving the top two legend rows unchanged.

**Reference program (`solve_M30`)**

```python
def solve_M30(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        s,t=g[0][c],g[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    out=clone(g)
    for r in range(2,h):
        for c in range(w):
            v=g[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out
```

---

### M31 — Sweep objects into the right wall

**What it tests:** Use the new sweep-shadow primitive against an explicit barrier.

**Staged hint:** Identify the 9-wall first. Then let each occupied cell cast a horizontal sweep to the right until the wall stops it.

**Train 1 — input**

```text
000000900
022000900
022000900
000500900
000000900
000660900
000660900
```

**Train 1 — output**

```text
000000900
022222900
022222900
000555900
000000900
000666900
000666900
```

**Train 2 — input**

```text
0000000900
0550000900
0000000900
0007000900
0007000900
0000000900
0060000900
0060000900
```

**Train 2 — output**

```text
0000000900
0555555900
0000000900
0007777900
0007777900
0000000900
0066666900
0066666900
```

**Test — input**

```text
00000000900
03300000900
03300000900
00000000900
00055000900
00000000900
00000070900
00000000900
```

**Test — expected output**

```text
00000000900
03333333900
03333333900
00000000900
00055555900
00000000900
00000077900
00000000900
```

**Written solution**

Find the vertical wall of 9s. For each colored object, sweep every one of its occupied cells horizontally to the right, painting all cells up to but not including the wall. The result is the object’s full shadow against the wall.

**Reference program (`solve_M31`)**

```python
def solve_M31(g):
    h,w=dims(g)
    out=clone(g)
    wall=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            wall=c
            break
    if wall is None:
        return out
    stop={(r,wall) for r in range(h)}
    for col,cells in components([[v if v not in (0,9) else 0 for v in row] for row in g]):
        swept=sweep_shadow(cells,(0,1),h,w,stop)
        for r,c in swept:
            if c!=wall:
                out[r][c]=col
    return out
```

---

### M32 — Row/column activation map

**What it tests:** Compose two 1D signals into a 2D cross-product pattern.

**Staged hint:** Read rows containing color 1 and columns containing color 2 as two separate active sets. Then intersect them.

**Train 1 — input**

```text
0020000
0000000
0100000
0000000
0000002
0000010
0000000
```

**Train 1 — output**

```text
0000000
0000000
0030003
0000000
0000000
0030003
0000000
```

**Train 2 — input**

```text
00000020
00000000
00100000
00020000
00000000
00000010
02000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
03030030
00000000
00000000
03030030
00000000
00000000
```

**Test — input**

```text
000200000
001000000
000000000
000000002
000010000
200000000
000000001
000000000
```

**Test — expected output**

```text
000000000
300300003
000000000
000000000
300300003
000000000
300300003
000000000
```

**Written solution**

Any row that contains a 1 becomes active. Any column that contains a 2 becomes active. Output 3 at every intersection of an active row and an active column, and 0 everywhere else.

**Reference program (`solve_M32`)**

```python
def solve_M32(g):
    h,w=dims(g)
    rows={r for r in range(h) if 1 in g[r]}
    cols={c for c in range(w) if any(g[r][c]==2 for r in range(h))}
    out=[[0]*w for _ in range(h)]
    for r in rows:
        for c in cols:
            out[r][c]=3
    return out
```

---

### M33 — Reduce solid objects to outlines

**What it tests:** Transform filled regions into their perimeters while preserving color and placement.

**Staged hint:** Work component by component. A cell stays only if at least one of its four cardinal neighbors lies outside the component.

**Train 1 — input**

```text
000000000
022200000
022200000
022200000
000000000
000555500
000555500
000555500
000000000
```

**Train 1 — output**

```text
000000000
022200000
020200000
022200000
000000000
000555500
000500500
000555500
000000000
```

**Train 2 — input**

```text
0000000000
0033300000
0033300000
0033300000
0000000000
0000066600
0000066600
0000066600
0000066600
0000000000
```

**Train 2 — output**

```text
0000000000
0033300000
0030300000
0033300000
0000000000
0000066600
0000060600
0000060600
0000066600
0000000000
```

**Test — input**

```text
00000000000
00022220000
00022220000
00022220000
00022220000
00000000000
00000055550
00000055550
00000055550
00000000000
```

**Test — expected output**

```text
00000000000
00022220000
00020020000
00020020000
00022220000
00000000000
00000055550
00000050050
00000055550
00000000000
```

**Written solution**

For each connected object, keep only its boundary cells: a cell remains if one of its four cardinal neighbors is outside the object. Delete any interior cells.

**Reference program (`solve_M33`)**

```python
def solve_M33(g):
    h,w=dims(g); out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        oc=outline_cells(cells)
        for r,c in oc:
            out[r][c]=col
    return out
```

---

### M34 — Crop the body by a column mask

**What it tests:** Use a binary header row as a keep/drop mask for columns and shrink the output width.

**Staged hint:** Read the first row as a column selector. Then copy only those body columns, in order, into the output.

**Train 1 — input**

```text
1010101
2345678
0003000
8888888
1201201
```

**Train 1 — output**

```text
2468
0000
8888
1021
```

**Train 2 — input**

```text
11001010
12345678
00070000
22222222
80402010
99999999
```

**Train 2 — output**

```text
1257
0000
2222
8021
9999
```

**Test — input**

```text
101101001
123456789
000040000
987654321
111111111
200000003
```

**Test — expected output**

```text
13469
00000
97641
11111
20003
```

**Written solution**

Look at the first row and keep exactly the columns marked with 1. Drop the other columns, remove the mask row itself, and output only the body rows using the kept columns.

**Reference program (`solve_M34`)**

```python
def solve_M34(g):
    h,w=dims(g)
    keep=[c for c,v in enumerate(g[0]) if v==1]
    out=[]
    for r in range(1,h):
        out.append([g[r][c] for c in keep])
    return out
```

---

### M35 — Point-reflect the object around the anchor

**What it tests:** Apply a 180° coordinate reflection around a single marked cell.

**Staged hint:** Find the unique 9 first. Every colored cell should be copied to the point directly opposite across that anchor.

**Train 1 — input**

```text
000000000
022000000
022000000
000090000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
022000000
022000000
000090000
000000220
000000220
000000000
```

**Train 2 — input**

```text
0000000000
0000550000
0000050000
0000900000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000550000
0000050000
0000900000
0005000000
0005500000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000330000
00000030000
00000000000
00000900000
00000000000
00000000000
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
00000330000
00000030000
00000000000
00000900000
00000000000
00003000000
00003300000
00000000000
```

**Written solution**

Use the 9 as a central anchor. For each nonzero non-9 cell, place a copy at the point-reflected position across the anchor, preserving the original object and the anchor.

**Reference program (`solve_M35`)**

```python
def solve_M35(g):
    h,w=dims(g); out=clone(g)
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    if len(anchors)!=1: return out
    a=anchors[0]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                rr,cc=2*a[0]-r, 2*a[1]-c
                if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                    out[rr][cc]=v
    return out
```

---

## Hard

### H29 — Arrow-driven sweep shadows

**What it tests:** Combine object–instruction association with the new sweep-shadow primitive.

**Staged hint:** Associate each object with its adjacent arrow cell first. Only after that should you sweep the whole object in the arrow’s direction.

**Train 1 — input**

```text
0000000000
0016600000
0006600000
0000000000
0000000000
0000008820
0000008000
0000000000
0000000000
```

**Train 1 — output**

```text
0006600000
0006600000
0006600000
0000000000
0000000000
0000008888
0000008888
0000000000
0000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00000000000
00005540000
00000500000
00000030000
00000077000
00000077000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000000
55555500000
55555500000
00000000000
00000077000
00000077000
00000077000
00000077000
```

**Test — input**

```text
000000000000
000010000000
000066000000
000066000000
000000000000
000000300000
000000770000
000000770000
000000000000
000000000882
000000000080
000000000000
```

**Test — expected output**

```text
000066000000
000066000000
000066000000
000066000000
000000000000
000000000000
000000770000
000000770000
000000770000
000000770888
000000770088
000000770000
```

**Written solution**

Each object has a touching arrow marker: 1 means up, 2 right, 3 down, 4 left. Remove the arrows, then sweep the entire object in the indicated direction, painting the full swept path all the way to the grid edge.

**Reference program (`solve_H29`)**

```python
def solve_H29(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    obj_grid=[[v if v>=5 else 0 for v in row] for row in g]
    for col,cells in components(obj_grid):
        arrow=None
        for r,c in cells:
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and g[nr][nc] in ARROW_DIR:
                    arrow=g[nr][nc]
                    break
            if arrow is not None:
                break
        swept=sweep_shadow(cells,ARROW_DIR[arrow],h,w)
        for r,c in swept:
            out[r][c]=col
    return out
```

---

### H30 — Permute column blocks by the header

**What it tests:** Decode a permutation from one header row and apply it to equal-width body blocks.

**Staged hint:** Segment the first header row into repeated-label blocks. The second header row tells you the new order of those same blocks.

**Train 1 — input**

```text
112233
331122
204560
204560
004500
777888
```

**Train 1 — output**

```text
602045
602045
000045
887778
```

**Train 2 — input**

```text
111222333444
333111444222
120034005600
120034005600
120000005600
999888777666
```

**Train 2 — output**

```text
005120600034
005120600034
005120600000
777999666888
```

**Test — input**

```text
11223344
44112233
21004365
21004365
00004300
77770000
```

**Test — expected output**

```text
65210043
65210043
00000043
00777700
```

**Written solution**

Treat the body as equal-width column blocks identified by the labels in the first row. Reorder those body blocks so they appear in the label order shown by the second row, and output only the reordered body.

**Reference program (`solve_H30`)**

```python
def solve_H30(g):
    h,w=dims(g)
    src_runs=[run for run in runs_of_row(g[0]) if run[2]!=0]
    dst_runs=[run for run in runs_of_row(g[1]) if run[2]!=0]
    # map id->slice
    blocks={}
    for s,e,v in src_runs:
        blocks[v]=(s,e+1)
    out=[]
    for r in range(2,h):
        row=[]
        for s,e,v in dst_runs:
            bs,be=blocks[v]
            row.extend(g[r][bs:be])
        out.append(row)
    return out
```

---

### H31 — Quadrant analogy — rotate 90°

**What it tests:** Learn a transformation from one panel pair and apply it to another panel in the same grid.

**Staged hint:** Use the top-left and top-right quadrants to identify the relation. Then apply that same relation to the bottom-left quadrant.

**Train 1 — input**

```text
200092220
200092000
220090000
000090000
999999999
330090000
030090000
030090000
000090000
```

**Train 1 — output**

```text
200092220
200092000
220090000
000090000
999999999
330090030
030093330
030090000
000090000
```

**Train 2 — input**

```text
04000904440
04000904000
04400900000
00000900000
00000900000
99999999999
06000900000
66600900000
00000900000
00000900000
00000900000
```

**Train 2 — output**

```text
04000904440
04000904000
04400900000
00000900000
00000900000
99999999999
06000960000
66600966000
00000960000
00000900000
00000900000
```

**Test — input**

```text
50000955000
55500950000
00000950000
00000900000
00000900000
99999999999
00700900000
77700900000
00700900000
00000900000
00000900000
```

**Test — expected output**

```text
50000955000
55500950000
00000950000
00000900000
00000900000
99999999999
00700907000
77700907000
00700977700
00000900000
00000900000
```

**Written solution**

The 9 cross splits the grid into four panels. The top-right panel is the top-left panel rotated 90° clockwise inside the object’s own bounding box. Apply that same 90° clockwise rotation to the bottom-left object and place the result in the bottom-right panel.

**Reference program (`solve_H31`)**

```python
def solve_H31(g):
    out=clone(g)
    # apply rotate90 clockwise to BL into BR
    cells_rel,_=extract_quad_cells(g,'BL')
    if not cells_rel: 
        return out
    color=cells_rel[0][0]  # assume monochrome shape
    rot,offset,hh,ww=rotate_bbox_preserve_offset(cells_rel)
    roff,coff=offset
    for r,c in rot:
        rr,cc=roff+r, coff+c
        place_r0,place_r1,place_c0,place_c1=quadrant_bounds(out,'BR')
        if place_r0+rr<place_r1 and place_c0+cc<place_c1:
            out[place_r0+rr][place_c0+cc]=color
    return out
```

---

### H32 — Recolor anchored template at markers

**What it tests:** Extract a source template with an internal anchor and restamp it at multiple target markers with recoloring.

**Staged hint:** Find the connected nonzero template that contains the 9 anchor. Record the occupied offsets relative to that anchor before stamping them at the colored markers.

**Train 1 — input**

```text
0000000000
0090000000
0660000000
0060000000
0000020000
0000000000
0000000300
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0000000000
0000000000
0000020000
0000220000
0000020300
0000003300
0000000300
```

**Train 2 — input**

```text
00009000000
00066600000
00006000000
00000000000
00000040000
00000000000
00000000070
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000000
00000000000
00000040000
00000444000
00000040070
00000000777
00000000070
```

**Test — input**

```text
000000000000
000090000000
000660000000
000600000000
000000000000
000000020000
000000000000
000000000500
000000000000
000000008000
000000000000
```

**Test — expected output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000020000
000000220000
000000200500
000000005500
000000008000
000000088000
```

**Written solution**

The source template is the connected multicolor object containing the 9 anchor. Take the occupied shape of that template relative to the 9. For every marker cell elsewhere, stamp that same shape so the anchor lands on the marker, and recolor the whole stamped copy to the marker’s color. Output only the stamped copies.

**Reference program (`solve_H32`)**

```python
def solve_H32(g):
    h,w=dims(g)
    # find anchor 9 in source template; assume one 9 in multi-cell component and maybe other nonzero singleton markers
    anchor=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                # if connected to another nonzero, treat as source anchor
                comp=nz_component(g,(r,c))
                if len(comp)>1:
                    anchor=(r,c); template_comp=comp
                    break
        if anchor: break
    if anchor is None:
        return clone(g)
    # relative shape of all cells in template component relative to anchor
    rel=[(r-anchor[0], c-anchor[1]) for r,c in template_comp]
    template_set=set(template_comp)
    out=[[0]*w for _ in range(h)]
    # destination markers: nonzero cells outside template
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in template_set:
                col=g[r][c]
                for dr,dc in rel:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=col
    return out
```

---

### H33 — Count-select, outline, then crop

**What it tests:** Chain three operations: read a count, select an object by area, then produce a cropped outline.

**Staged hint:** Do not outline everything. First use the header count to decide which object matters.

**Train 1 — input**

```text
01111111110
00000000000
02220000000
02220000000
02220000000
00000000000
00000550000
00000500000
00000000000
00000007700
00000007700
```

**Train 1 — output**

```text
222
202
222
```

**Train 2 — input**

```text
01111111111110
00000000000000
00033330000000
00033330000000
00033330000000
00000000000000
05550000000000
00500000000000
00000000000000
00000006600000
00000006600000
00000000000000
```

**Train 2 — output**

```text
3333
3003
3333
```

**Test — input**

```text
011111111111111110
000000000000000000
000044440000000000
000044440000000000
000044440000000000
000044440000000000
000000000000000000
000000055500000000
000000005000000000
000000000000000000
000000000077000000
000000000077000000
```

**Test — expected output**

```text
4444
4004
4004
4444
```

**Written solution**

Count the 1s in the top row. In the body, select the component whose area matches that count. Replace it by its outline only, then crop the output to that outlined component’s bounding box.

**Reference program (`solve_H33`)**

```python
def solve_H33(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    chosen=None
    chosen_col=None
    for col,cells in components([row[:] for row in g[1:]]):
        if len(cells)==k:
            chosen={(r+1,c) for r,c in cells}
            chosen_col=col
            break
    if chosen is None:
        return [[0]]
    oc=outline_cells(chosen)
    # crop
    rs=[r for r,c in oc]; cs=[c for r,c in oc]
    r0,r1,c0,c1=min(rs),max(rs),min(cs),max(cs)
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in oc:
        out[r-r0][c-c0]=chosen_col
    return out
```

---

### H34 — Quadrant analogy — outline transform

**What it tests:** Infer a nontrivial transform from one quadrant pair and reuse it on a second shape.

**Staged hint:** The top pair gives you the transformation family: a solid shape becomes its outline. Apply that exact family to the lower-left shape.

**Train 1 — input**

```text
222092220
222092020
222092220
000090000
999999999
333090000
333090000
333090000
000090000
```

**Train 1 — output**

```text
222092220
222092020
222092220
000090000
999999999
333093330
333093030
333093330
000090000
```

**Train 2 — input**

```text
04440904440
04440904040
04440904040
04440904440
00000900000
99999999999
00000900000
06660900000
06660900000
06660900000
00000900000
```

**Train 2 — output**

```text
04440904440
04440904040
04440904040
04440904440
00000900000
99999999999
00000900000
06660906660
06660906060
06660906660
00000900000
```

**Test — input**

```text
55000955000
55000955000
00000900000
00000900000
00000900000
99999999999
77700900000
77700900000
77700900000
77700900000
00000900000
```

**Test — expected output**

```text
55000955000
55000955000
00000900000
00000900000
00000900000
99999999999
77700977700
77700970700
77700970700
77700977700
00000900000
```

**Written solution**

The 9 cross divides the grid into four panels. In the top pair, the right panel shows the outline of the solid shape in the left panel. Apply that same solid→outline transformation to the bottom-left shape and place the outlined result in the bottom-right panel.

**Reference program (`solve_H34`)**

```python
def solve_H34(g):
    out=clone(g)
    cells_rel,_=extract_quad_cells(g,'BL')
    if not cells_rel:
        return out
    color=cells_rel[0][0]
    coords=[(r,c) for _,r,c in cells_rel]
    rs=[r for r,c in coords]; cs=[c for r,c in coords]
    rmin,rmax,cmin,cmax=min(rs),max(rs),min(cs),max(cs)
    shape={(r-rmin,c-cmin) for r,c in coords}
    outshape=outline_cells({(r,c) for r,c in shape})
    br0,br1,bc0,bc1=quadrant_bounds(out,'BR')
    for r,c in outshape:
        rr,cc=br0+rmin+r, bc0+cmin+c
        out[rr][cc]=color
    return out
```

---

### H35 — Recolor by legend, then crop masked columns

**What it tests:** Compose two symbolic instructions: a palette remap and a column-selection mask.

**Staged hint:** Read the legend before reading the mask. First translate body colors with rows 1–2, then apply the keep/drop column rule from row 3.

**Train 1 — input**

```text
20304000
50607000
10101010
00233040
00200040
44420030
```

**Train 1 — output**

```text
0567
0507
7706
```

**Train 2 — input**

```text
040020300
070050600
110010101
402030402
000200030
304040203
020300040
```

**Train 2 — output**

```text
70675
00000
60756
05000
```

**Test — input**

```text
0300402050
0600705080
1011010011
0034002050
0000402050
0223300040
0040003060
```

**Test — expected output**

```text
067080
000080
056070
070060
```

**Written solution**

Rows 1 and 2 define a source-to-target color map. Row 3 marks which columns to keep. Recolor the body using the legend, then drop every unmarked column and output only the recolored kept columns.

**Reference program (`solve_H35`)**

```python
def solve_H35(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        s,t=g[0][c],g[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    keep=[c for c,v in enumerate(g[2]) if v==1]
    out=[]
    for r in range(3,h):
        row=[]
        for c in keep:
            v=g[r][c]
            row.append(mapping.get(v,v))
        out.append(row)
    return out
```

---

