# 21 More ARC-Style Puzzles

This is a continuation bank: **7 easy, 7 medium, 7 hard**.
It follows the earlier format, but pushes a little further into normalization, local frames, and derived-structure reasoning.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

The IDs continue the earlier sequence as **E8–E14, M8–M14, H8–H14**.

## Easy

### E8 — Horizontal sandwich fill

**What it tests:** Immediate left/right matching with simultaneous updates.

**Staged hint:** First mark zero cells whose left and right neighbors match; then copy that color into the center.

**Train 1 — input**
```text
0000000
0202000
0000000
0030300
0000000
```

**Train 1 — output**
```text
0000000
0222000
0000000
0033300
0000000
```

**Train 2 — input**
```text
00000000
04040000
00000000
00505000
00006060
```

**Train 2 — output**
```text
00000000
04440000
00000000
00555000
00006660
```

**Test — input**
```text
000000000
070700000
000000000
000202000
000000000
009090900
```

**Test — expected output**
```text
000000000
077700000
000000000
000222000
000000000
009999900
```

**Written solution**

Any 0 cell that sits directly between two equal nonzero horizontal neighbors is filled with that same color. Everything else stays unchanged.

**Reference program (`solve_E8`)**
```python
def solve_E8(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
    return out
```

---

### E9 — Complete the missing square corner

**What it tests:** Local 2×2 completion from three-of-four evidence.

**Staged hint:** Scan 2×2 windows; if three cells are the same nonzero color and the fourth is 0, fill the missing corner.

**Train 1 — input**
```text
000000
044000
040000
000330
000300
000000
```

**Train 1 — output**
```text
000000
044000
044000
000330
000330
000000
```

**Train 2 — input**
```text
0000000
0220000
0020000
0000550
0000500
0000000
```

**Train 2 — output**
```text
0000000
0220000
0220000
0000550
0000550
0000000
```

**Test — input**
```text
00000000
06600000
06000000
00000000
00077000
00007000
00000000
```

**Test — expected output**
```text
00000000
06600000
06600000
00000000
00077000
00077000
00000000
```

**Written solution**

Whenever a 2×2 block contains exactly three cells of the same nonzero color and one empty cell, fill the empty corner with that color.

**Reference program (`solve_E9`)**
```python
def solve_E9(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                if g[r][c]==0: out[r][c]=nz[0]
                if g[r][c+1]==0: out[r][c+1]=nz[0]
                if g[r+1][c]==0: out[r+1][c]=nz[0]
                if g[r+1][c+1]==0: out[r+1][c+1]=nz[0]
    return out
```

---

### E10 — Fill the row between matching endpoints

**What it tests:** Rowwise segment completion using endpoint agreement.

**Staged hint:** Find rows that contain exactly two nonzero cells of the same color with only 0s between them; then fill the span.

**Train 1 — input**
```text
0000000
0200002
0000000
0030030
0000000
```

**Train 1 — output**
```text
0000000
0222222
0000000
0033330
0000000
```

**Train 2 — input**
```text
00000000
00600006
02000203
00000000
40000004
```

**Train 2 — output**
```text
00000000
00666666
02000203
00000000
44444444
```

**Test — input**
```text
000000000
070000007
000000000
002000200
300000003
```

**Test — expected output**
```text
000000000
077777777
000000000
002222200
333333333
```

**Written solution**

If a row has exactly two nonzero cells, both the same color, and all cells between them are 0, fill the entire segment from the left endpoint to the right endpoint with that color.

**Reference program (`solve_E10`)**
```python
def solve_E10(g):
    out=clone(g)
    for r,row in enumerate(g):
        nz=[(c,v) for c,v in enumerate(row) if v!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            c0,v=nz[0]; c1,_=nz[1]
            if all(row[c]==0 for c in range(c0+1,c1)):
                for c in range(c0,c1+1):
                    out[r][c]=v
    return out
```

---

### E11 — X-center fill

**What it tests:** Diagonal-neighbor pattern detection in a 3×3 neighborhood.

**Staged hint:** Ignore cardinal neighbors. Only look at the four diagonals around each 0 cell.

**Train 1 — input**
```text
00000
02020
00000
02020
00000
```

**Train 1 — output**
```text
00000
02020
00200
02020
00000
```

**Train 2 — input**
```text
00000000
03030000
00000000
03034040
00000000
00004040
00000000
```

**Train 2 — output**
```text
00000000
03030000
00300000
03034040
00000400
00004040
00000000
```

**Test — input**
```text
000000000
050500000
000000000
050506060
000000000
000006060
000000000
```

**Test — expected output**
```text
000000000
050500000
005000000
050506060
000000600
000006060
000000000
```

**Written solution**

If a 0 cell has the same nonzero color on all four diagonal positions around it, fill the center with that color.

**Reference program (`solve_E11`)**
```python
def solve_E11(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if g[r][c]==0 and vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
    return out
```

---

### E12 — Extend exact dominoes

**What it tests:** Run-length discrimination with a one-cell extension.

**Staged hint:** Detect horizontal runs of exact length 2; do not touch longer runs.

**Train 1 — input**
```text
0000000
0330000
0000000
0004400
0000000
```

**Train 1 — output**
```text
0000000
0333000
0000000
0004440
0000000
```

**Train 2 — input**
```text
00000000
05500000
00066600
00000000
77000000
```

**Train 2 — output**
```text
00000000
05550000
00066600
00000000
77700000
```

**Test — input**
```text
000000000
055000000
000666000
000000770
004400000
```

**Test — expected output**
```text
000000000
055500000
000666000
000000777
004440000
```

**Written solution**

Every horizontal run of exact length 2 is extended one cell to the right, provided the next cell is 0. Longer runs are left alone.

**Reference program (`solve_E12`)**
```python
def solve_E12(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]!=0:
                val=g[r][c]; start=c
                while c+1<w and g[r][c+1]==val: c+=1
                end=c
                if end-start+1==2 and end+1<w and g[r][end+1]==0:
                    out[r][end+1]=val
            c+=1
    return out
```

---

### E13 — Highlight 2×2 block anchors

**What it tests:** Exact solid-square detection with selective recoloring.

**Staged hint:** Find monochrome 2×2 blocks, but only change one designated cell inside each block.

**Train 1 — input**
```text
022000
022000
000330
000330
000000
```

**Train 1 — output**
```text
082000
022000
000830
000330
000000
```

**Train 2 — input**
```text
00000000
00440000
00440000
00000000
00066000
00066000
```

**Train 2 — output**
```text
00000000
00840000
00440000
00000000
00086000
00066000
```

**Test — input**
```text
000000000
022000440
022000440
000000000
000770000
000770000
```

**Test — expected output**
```text
000000000
082000840
022000440
000000000
000870000
000770000
```

**Written solution**

For every solid 2×2 block of the same nonzero color, recolor only its top-left cell to 8 and leave the other three cells unchanged.

**Reference program (`solve_E13`)**
```python
def solve_E13(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=8
    return out
```

---

### E14 — Horizontal symmetrization

**What it tests:** Global reflection across the horizontal midline.

**Staged hint:** Mirror nonzero cells to the row that is equally far from the opposite edge.

**Train 1 — input**
```text
0000000
0200000
0022000
0003000
0000000
```

**Train 1 — output**
```text
0000000
0203000
0022000
0203000
0000000
```

**Train 2 — input**
```text
00000000
00040000
00500000
00550000
00000000
00000060
00000000
```

**Train 2 — output**
```text
00000000
00040060
00500000
00550000
00500000
00040060
00000000
```

**Test — input**
```text
000000000
000600000
002200000
000030000
000000000
000000400
000000000
```

**Test — expected output**
```text
000000000
000600400
002200000
000030000
002200000
000600400
000000000
```

**Written solution**

Reflect every nonzero cell across the horizontal midline of the grid and add the mirrored copy while preserving the original cells.

**Reference program (`solve_E14`)**
```python
def solve_E14(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[h-1-r][c]=g[r][c]
    return out
```

---

## Medium

### M8 — Recolor the rightmost object

**What it tests:** Connected-component extraction and ranking by position.

**Staged hint:** First segment all objects. Then compare their maximum column positions.

**Train 1 — input**
```text
22000000
22000030
00000030
00440000
00000000
```

**Train 1 — output**
```text
22000000
22000080
00000080
00440000
00000000
```

**Train 2 — input**
```text
00005500
00005500
20000000
20000044
00000044
```

**Train 2 — output**
```text
00005500
00005500
20000000
20000088
00000088
```

**Test — input**
```text
000000000
022000000
022000055
000000055
000330000
000000000
```

**Test — expected output**
```text
000000000
022000000
022000088
000000088
000330000
000000000
```

**Written solution**

Find the connected component whose cells extend farthest to the right, and recolor that entire object to 8. Leave all other objects as they are.

**Reference program (`solve_M8`)**
```python
def solve_M8(g):
    comps=components(g)
    # choose comp with largest max col; tie by area then min row
    chosen=max(comps, key=lambda x: (max(c for r,c in x[1]), len(x[1]), -min(r for r,c in x[1])))
    out=clone(g)
    for r,c in chosen[1]:
        out[r][c]=8
    return out
```

---

### M9 — Draw every object's bounding-box border

**What it tests:** Object detection plus geometric abstraction to bounding rectangles.

**Staged hint:** Do not preserve the original shapes. Replace each object by the perimeter of its bounding box.

**Train 1 — input**
```text
22000000
20000000
22200000
00003300
00003000
00000000
```

**Train 1 — output**
```text
22200000
20200000
22200000
00003300
00003300
00000000
```

**Train 2 — input**
```text
000000000
044400000
040000000
044000000
000000330
000000030
000000000
```

**Train 2 — output**
```text
000000000
044400000
040400000
044400000
000000330
000000330
000000000
```

**Test — input**
```text
000000000
055000000
005000000
055500000
000000220
000000020
000000000
```

**Test — expected output**
```text
000000000
055500000
050500000
055500000
000000220
000000220
000000000
```

**Written solution**

For each connected nonzero object, compute its bounding box and draw only the rectangular border of that box in the object's color on an otherwise empty grid.

**Reference program (`solve_M9`)**
```python
def solve_M9(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        draw_rect_border(out,r0,r1,c0,c1,col)
    return out
```

---

### M10 — Bridge aligned same-color objects

**What it tests:** Relational reasoning between separate components of one color.

**Staged hint:** Group components by color, then look for two components that overlap in row range and have a horizontal gap between them.

**Train 1 — input**
```text
2200022
2200022
0000000
0330033
0330033
```

**Train 1 — output**
```text
2222222
2222222
0000000
0333333
0333333
```

**Train 2 — input**
```text
000000000
044000044
044000044
000000000
005500000
000000055
```

**Train 2 — output**
```text
000000000
044444444
044444444
000000000
005500000
000000055
```

**Test — input**
```text
0000000000
0220000022
0220000022
0000000000
0003303300
0003303300
```

**Test — expected output**
```text
0000000000
0222222222
0222222222
0000000000
0003333300
0003333300
```

**Written solution**

When a color has two separate objects whose row spans overlap, fill the horizontal gap between their bounding boxes across the overlapping rows using that same color.

**Reference program (`solve_M10`)**
```python
def solve_M10(g):
    out=clone(g)
    by_color=defaultdict(list)
    for col,cells in components(g):
        by_color[col].append(cells)
    for col, comps in by_color.items():
        if len(comps)==2:
            bbs=[bbox(cells) for cells in comps]
            # sort left to right
            (r0a,r1a,c0a,c1a),(r0b,r1b,c0b,c1b)=sorted(bbs,key=lambda b:b[2])
            overlap_r0=max(r0a,r0b); overlap_r1=min(r1a,r1b)
            if overlap_r0<=overlap_r1 and c1a+1<=c0b-1:
                for r in range(overlap_r0,overlap_r1+1):
                    for c in range(c1a+1,c0b):
                        out[r][c]=col
    return out
```

---

### M11 — Move the payload to the 9 marker

**What it tests:** Local-frame translation of an extracted object.

**Staged hint:** Crop the payload object, find its top-left corner, then paste the same local shape with that corner aligned to the 9 cell.

**Train 1 — input**
```text
2200000
2000000
0000000
0000900
0000000
0000000
```

**Train 1 — output**
```text
0000000
0000000
0000000
0000220
0000200
0000000
```

**Train 2 — input**
```text
00033000
00003000
00000000
09000000
00000000
00000000
```

**Train 2 — output**
```text
00000000
00000000
00000000
03300000
00300000
00000000
```

**Test — input**
```text
000000000
004400000
000400000
000000000
000000900
000000000
000000000
```

**Test — expected output**
```text
000000000
000000000
000000000
000000000
000000440
000000040
000000000
```

**Written solution**

There is one payload object and one cell colored 9. Remove both from their original locations and place the payload again so that its bounding-box top-left corner lands exactly on the 9 cell.

**Reference program (`solve_M11`)**
```python
def solve_M11(g):
    comps=[(col,cells) for col,cells in components(g) if col!=9]
    marker=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    assert len(comps)==1 and len(marker)==1
    col,cells=comps[0]
    mr,mc=marker[0]
    r0,r1,c0,c1=bbox(cells)
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for r,c in cells:
        out[mr+(r-r0)][mc+(c-c0)] = col
    return out
```

---

### M12 — Keep only vertically symmetric objects

**What it tests:** Symmetry checking inside each object's own coordinate frame.

**Staged hint:** Test symmetry after cropping each object to its own bounding box; do not judge symmetry in the global grid.

**Train 1 — input**
```text
000000000
020000330
222000300
020000300
000000000
004000000
004000000
```

**Train 1 — output**
```text
000000000
020000000
222000000
020000000
000000000
004000000
004000000
```

**Train 2 — input**
```text
00000000
05500000
05500060
00000066
00000060
00000000
```

**Train 2 — output**
```text
00000000
05500000
05500000
00000000
00000000
00000000
```

**Test — input**
```text
0000000000
0030004400
0333004400
0030000400
0000000000
0005500000
0000550000
0000000000
```

**Test — expected output**
```text
0000000000
0030000000
0333000000
0030000000
0000000000
0000000000
0000000000
0000000000
```

**Written solution**

Preserve only those connected objects whose cropped shape is symmetric across a vertical axis through the center of their own bounding box. Remove all other objects.

**Reference program (`solve_M12`)**
```python
def solve_M12(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if is_vert_sym(cells):
            for r,c in cells:
                out[r][c]=col
    return out
```

---

### M13 — Fill each object's row gaps

**What it tests:** Objectwise row-wise hull filling.

**Staged hint:** Work row by row inside each object: if a row contains that object's color in multiple columns, fill the interval between the leftmost and rightmost occupied cells.

**Train 1 — input**
```text
0000000
0220020
0200020
0222220
0000000
```

**Train 1 — output**
```text
0000000
0222220
0222220
0222220
0000000
```

**Train 2 — input**
```text
00000000
03300030
00300030
03333330
00000000
```

**Train 2 — output**
```text
00000000
03333330
00333330
03333330
00000000
```

**Test — input**
```text
000000000
044000040
004000040
044444440
000000000
```

**Test — expected output**
```text
000000000
044444440
004444440
044444440
000000000
```

**Written solution**

For every connected object, look at each row where that object appears and fill all cells between that row's leftmost and rightmost object cell with the object's color.

**Reference program (`solve_M13`)**
```python
def solve_M13(g):
    out=clone(g)
    for col,cells in components(g):
        rows=defaultdict(list)
        for r,c in cells:
            rows[r].append(c)
        for r, cs in rows.items():
            for c in range(min(cs), max(cs)+1):
                out[r][c]=col
    return out
```

---

### M14 — Fill the holes of the largest hollow object

**What it tests:** Hole detection and object ranking by area.

**Staged hint:** Find which objects actually contain enclosed 0-regions; among those, pick the largest one before filling anything.

**Train 1 — input**
```text
000000000
044444000
040004000
040004000
044444000
000220000
000220000
000000000
```

**Train 1 — output**
```text
000000000
044444000
044444000
044444000
044444000
000220000
000220000
000000000
```

**Train 2 — input**
```text
0000000000
0333333000
0300003000
0300003000
0333333000
0000555000
0000505000
0000555000
0000000000
```

**Train 2 — output**
```text
0000000000
0333333000
0333333000
0333333000
0333333000
0000555000
0000505000
0000555000
0000000000
```

**Test — input**
```text
00000000000
02222222000
02000002000
02000002000
02222222000
00000000000
00055550000
00050050000
00055550000
00000000000
```

**Test — expected output**
```text
00000000000
02222222000
02222222000
02222222000
02222222000
00000000000
00055550000
00050050000
00055550000
00000000000
```

**Written solution**

Identify all hollow objects. Among them, choose the one with the largest area and fill all of its enclosed holes using that object's color. Leave every other object unchanged.

**Reference program (`solve_M14`)**
```python
def solve_M14(g):
    out=clone(g)
    hollow=[]
    for col,cells in components(g):
        holes=hole_cells_of_component(g,cells)
        if holes:
            hollow.append((len(cells), col, cells, holes))
    if not hollow:
        return out
    _, col, cells, holes = max(hollow, key=lambda x:x[0])
    for r,c in holes:
        out[r][c]=col
    return out
```

---

## Hard

### H8 — Stack normalized objects by width

**What it tests:** Output resizing, object normalization, sorting, and repacking.

**Staged hint:** Crop every object first. Then sort the cropped pieces by width from widest to narrowest and stack them top-to-bottom with one blank row between pieces.

**Train 1 — input**
```text
0000000000
0220003333
0220000000
0000004000
0000004000
0000004000
0000000000
```

**Train 1 — output**
```text
3333
0000
2200
2200
0000
4000
4000
4000
```

**Train 2 — input**
```text
00000000000
05555500000
00000000000
00066000000
00006000000
00000000070
00000000000
```

**Train 2 — output**
```text
55555
00000
66000
06000
00000
70000
```

**Test — input**
```text
000000000000
000220000000
000220000000
000000000000
000000444400
000000000000
000000000006
000000000000
```

**Test — expected output**
```text
4444
0000
2200
2200
0000
6000
```

**Written solution**

Extract every connected object, crop it to its bounding box, sort the cropped objects by width descending, and build a new output grid that stacks them vertically with one blank row between neighboring objects. Left-align all stacked shapes.

**Reference program (`solve_H8`)**
```python
def solve_H8(g):
    comps=components(g)
    items=[]
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        items.append((W,H,col,set(local)))
    items.sort(key=lambda x:(-x[0], -x[1], x[2]))
    out_h=sum(H for W,H,col,s in items) + max(0, len(items)-1)
    out_w=max(W for W,H,col,s in items) if items else 0
    out=[[0]*out_w for _ in range(out_h)]
    r_off=0
    for W,H,col,s in items:
        for r,c in s:
            out[r_off+r][c]=col
        r_off += H + 1
    return out
```

---

### H9 — Normalized shape XOR

**What it tests:** Shape normalization and comparison independent of absolute position.

**Staged hint:** Crop the color-2 object and the color-3 object separately, align both cropped shapes to the same top-left origin, then keep only cells occupied by exactly one of them.

**Train 1 — input**
```text
222000000
020000300
020000300
000000333
000000000
```

**Train 1 — output**
```text
088
880
808
```

**Train 2 — input**
```text
022000000
022000333
000000030
000000000
```

**Train 2 — output**
```text
008
800
```

**Test — input**
```text
2200000000
2000003000
2000003330
0000000000
```

**Test — expected output**
```text
080
088
800
```

**Written solution**

Take the color-2 object and the color-3 object, crop each to its own bounding box, normalize both to the top-left corner of a shared canvas, and output color 8 wherever exactly one normalized shape occupies a cell.

**Reference program (`solve_H9`)**
```python
def solve_H9(g):
    comps=components(g)
    # choose first color2 and first color3
    c2=[cells for col,cells in comps if col==2][0]
    c3=[cells for col,cells in comps if col==3][0]
    s2,(H2,W2)=crop_cells(c2); s2=set(s2)
    s3,(H3,W3)=crop_cells(c3); s3=set(s3)
    H=max(H2,H3); W=max(W2,W3)
    out=[[0]*W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            in2=(r,c) in s2
            in3=(r,c) in s3
            if in2 ^ in3:
                out[r][c]=8
    return out
```

---

### H10 — Rotate each object 180° in its own frame

**What it tests:** Per-object local coordinate transforms without moving the bbox.

**Staged hint:** Do not rotate the whole canvas. Rotate each cropped object inside its own bounding box, then paste it back into the same bbox location.

**Train 1 — input**
```text
22000000
20000033
20000003
00000000
```

**Train 1 — output**
```text
02000000
02000030
22000033
00000000
```

**Train 2 — input**
```text
055000000
005000660
005000060
000000000
```

**Train 2 — output**
```text
050000000
050000600
055000660
000000000
```

**Test — input**
```text
000220000
000200000
000200330
000000030
000000000
```

**Test — expected output**
```text
000020000
000020000
000220300
000000330
000000000
```

**Written solution**

For every connected object, crop to its bounding box, rotate that local shape by 180 degrees, and place the rotated version back into the same bounding-box position on an otherwise empty grid.

**Reference program (`solve_H10`)**
```python
def solve_H10(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        H=r1-r0+1; W=c1-c0+1
        local,_=crop_cells(cells)
        for r,c in local:
            rr = H-1-r
            cc = W-1-c
            out[r0+rr][c0+cc]=col
    return out
```

---

### H11 — Extract the repeated shape family

**What it tests:** Normalized-shape matching across colors and positions, plus output resizing.

**Staged hint:** Compare objects by shape after cropping and normalization, ignoring color and location. Find the shape that appears more than once.

**Train 1 — input**
```text
22000000
20000000
00003300
00003000
00000000
00040000
00040000
```

**Train 1 — output**
```text
88
80
```

**Train 2 — input**
```text
0500000600
5550006660
0500000600
0000000000
0000077000
0000077000
```

**Train 2 — output**
```text
080
888
080
```

**Test — input**
```text
0002200000
0002000000
0000000000
0330000000
0030000550
0000000050
0000000000
```

**Test — expected output**
```text
88
08
```

**Written solution**

Among the input objects, two share the same normalized shape while at least one other object is different. Output the repeated normalized shape alone, recolored entirely to 8.

**Reference program (`solve_H11`)**
```python
def solve_H11(g):
    comps=components(g)
    groups=defaultdict(list)
    dims_map={}
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        key=tuple(sorted(local))
        groups[key].append((col,cells,H,W))
        dims_map[key]=(H,W)
    key=max(groups.keys(), key=lambda k: (len(groups[k]), len(k)))
    H,W=dims_map[key]
    out=[[0]*W for _ in range(H)]
    for r,c in key:
        out[r][c]=8
    return out
```

---

### H12 — Arrange four objects by area in a 2×2 pack

**What it tests:** Multi-object ranking, output resizing, and two-dimensional packing.

**Staged hint:** Crop all four objects, sort them by area ascending, then assign them in reading order to the top-left, top-right, bottom-left, and bottom-right cells of a new 2×2 packing layout with one blank row and one blank column as separators.

**Train 1 — input**
```text
200000000
000033000
000000000
000400000
000440000
000000055
000000055
```

**Train 1 — output**
```text
20033
00000
40055
44055
```

**Train 2 — input**
```text
0000000000
0002000000
0000000300
0000000300
0440000000
0040000000
0000005555
```

**Train 2 — output**
```text
2003000
0003000
0000000
4405555
0400000
```

**Test — input**
```text
00000000000
00002000000
00000000000
33000000000
00000004400
00000000400
00000000000
00000000055
00000000055
```

**Test — expected output**
```text
20033
00000
44055
04055
```

**Written solution**

Extract and crop the four objects. Sort them by area from smallest to largest. Place them into a new output canvas in reading order: smallest in the top-left cell, next in the top-right, next in the bottom-left, and largest in the bottom-right, with one blank row and one blank column separating the packed quadrants.

**Reference program (`solve_H12`)**
```python
def solve_H12(g):
    comps=components(g)
    items=[]
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        items.append((len(cells), W, H, col, set(local)))
    items.sort(key=lambda x:(x[0], x[1], x[2], x[3]))
    # take first four
    items=items[:4]
    (a_area,aW,aH,aCol,aS),(b_area,bW,bH,bCol,bS),(c_area,cW,cH,cCol,cS),(d_area,dW,dH,dCol,dS)=items
    left_w=max(aW,cW); right_w=max(bW,dW)
    top_h=max(aH,bH); bot_h=max(cH,dH)
    H=top_h+1+bot_h; W=left_w+1+right_w
    out=[[0]*W for _ in range(H)]
    # TL
    for r,c in aS: out[r][c]=aCol
    # TR
    for r,c in bS: out[r][left_w+1+c]=bCol
    # BL
    for r,c in cS: out[top_h+1+r][c]=cCol
    # BR
    for r,c in dS: out[top_h+1+r][left_w+1+c]=dCol
    return out
```

---

### H13 — Pack the hole patterns

**What it tests:** Hole extraction, normalization of derived structures, and packing.

**Staged hint:** Ignore the outer shells once you have found the holes. Treat each hole pattern as its own derived object, crop it, and then pack the resulting patterns left-to-right.

**Train 1 — input**
```text
000000000000
022220033333
020020030003
020020033333
022220000000
000000000000
```

**Train 1 — output**
```text
220333
220000
```

**Train 2 — input**
```text
000000000000
044440005550
040040005050
044440005550
000000000000
```

**Train 2 — output**
```text
4405
```

**Test — input**
```text
0000000000000
03333300022220
03000300020020
03000300020020
03333300022220
0000000000000
```

**Test — expected output**
```text
333022
333022
```

**Written solution**

For every hollow object, extract only its enclosed hole cells, recolor those hole cells with the color of the object they came from, crop each resulting hole pattern to its own bounding box, and pack the cropped hole patterns left-to-right with one blank column between them.

**Reference program (`solve_H13`)**
```python
def solve_H13(g):
    # extract hole patterns, crop them to hole bbox, pack left->right with gap 1 by original left order
    items=[]
    for col,cells in components(g):
        holes=hole_cells_of_component(g,cells)
        if holes:
            hr0,hr1,hc0,hc1=bbox(holes)
            local=[(r-hr0,c-hc0) for r,c in holes]
            H=hr1-hr0+1; W=hc1-hc0+1
            comp_bb=bbox(cells)
            items.append((comp_bb[2], H, W, col, set(local)))
    items.sort(key=lambda x:x[0])
    if not items:
        return [[]]
    H=max(item[1] for item in items)
    W=sum(item[2] for item in items)+max(0,len(items)-1)
    out=[[0]*W for _ in range(H)]
    off=0
    for _,h,w,col,s in items:
        for r,c in s: out[r][off+c]=col
        off += w+1
    return out
```

---

### H14 — Transfer the hole pattern to the solid twin

**What it tests:** Local-frame correspondence between a hollow template and a same-sized solid target.

**Staged hint:** Use the hollow object only as a template: record its hole coordinates relative to its own bounding box, then erase the corresponding relative cells inside the solid object's bounding box.

**Train 1 — input**
```text
02222033330
02002033330
02002033330
02222033330
00000000000
```

**Train 1 — output**
```text
02222033330
02002030030
02002030030
02222033330
00000000000
```

**Train 2 — input**
```text
000000000000
044440055550
040040055550
044440055550
000000000000
```

**Train 2 — output**
```text
000000000000
044440055550
040040050050
044440055550
000000000000
```

**Test — input**
```text
0000000000000
06666000077770
06006000077770
06006000077770
06666000077770
0000000000000
```

**Test — expected output**
```text
0000000000000
06666000077770
06006000070070
06006000070070
06666000077770
0000000000000
```

**Written solution**

Find the hollow object and the solid object with the same bounding-box size. Compute the hollow object's hole pattern in local coordinates, then carve out zeros at the corresponding local positions inside the solid object's bounding box. Keep the hollow template unchanged.

**Reference program (`solve_H14`)**
```python
def solve_H14(g):
    comps=components(g)
    hollow=[]; solid=[]
    for col,cells in comps:
        holes=hole_cells_of_component(g,cells)
        bb=bbox(cells)
        if holes:
            hollow.append((col,cells,holes,bb))
        else:
            solid.append((col,cells,bb))
    # match by bbox dims
    out=clone(g)
    for hcol,hcells,holes,hbb in hollow:
        hH=hbb[1]-hbb[0]+1; hW=hbb[3]-hbb[2]+1
        rel=[(r-hbb[0], c-hbb[2]) for r,c in holes]
        for scol,scells,sbb in solid:
            sH=sbb[1]-sbb[0]+1; sW=sbb[3]-sbb[2]+1
            if (sH,sW)==(hH,hW):
                for rr,cc in rel:
                    out[sbb[0]+rr][sbb[2]+cc]=0
                return out
    return out
```

---

