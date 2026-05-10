# 21 More ARC-Style Puzzles

This is the thirteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E85–E91, M85–M91, H85–H91**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into local completion, object relocation, command-conditioned geometry, prototype stamping, palette remapping, distance-based chamber fills, masked carry crops, sweep unions, and operation inference from examples.

**New motifs in this batch**

**`example_inferred_transform(example_in, example_out, query)`** — infer a flip or rotation from one example pair and reuse it on a query. This is the core move in **H85**.

**`prototype_dictionary_lookup(keys, prototypes, query)`** — read keyed prototypes from a dictionary-like layout and assemble a new output by query sequence. This drives **H89**.

**`sweep_union_until_wall(object, wall)`** — slide an object step by step until it meets a wall and keep the union of all visited positions. This is central to **H90**.

**`binary_op_from_example(A, B, C)`** — infer whether the hidden panel operation is union, intersection, or XOR from one example triplet, then apply it to a new pair. This is the main idea in **H91**.

## Easy

### E85 — Fill the horizontal bridge

**What it tests:** Recognize matching same-color endpoints in a row and fill the blank interval between them.

**Staged hint:** Scan row by row. Only pay attention to colors that appear as a clean two-endpoint pair in one row.

**Train 1 — input**

```text
00000000
02002000
00000000
00000000
60000060
00000000
00000000
```

**Train 1 — output**

```text
00000000
02222000
00000000
00000000
66666660
00000000
00000000
```

**Train 2 — input**

```text
000000000
000400040
000000000
700000007
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000444440
000000000
777777777
000000000
000000000
000000000
```

**Test — input**

```text
0000000000
0030000003
0000000000
0000000000
0000000000
0080000800
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0033333333
0000000000
0000000000
0000000000
0088888800
0000000000
0000000000
```

**Written solution**

For each color, if it appears exactly twice in the same row with only zeros between those two cells, fill the whole horizontal segment between the endpoints with that color. Leave every other cell unchanged.

**Reference program (`solve_E85`)**

```python
def solve_E85(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][0]==cells[1][0]:
            r=cells[0][0]
            a,b=sorted([cells[0][1], cells[1][1]])
            if all(g[r][c]==0 for c in range(a+1,b)):
                for c in range(a,b+1):
                    out[r][c]=color
    return out
```

### E86 — Fill the plus center

**What it tests:** Detect an empty center whose four cardinal neighbors all share the same nonzero color.

**Staged hint:** Ignore diagonals. Check only zero cells, and ask whether up, down, left, and right all match.

**Train 1 — input**

```text
0000000
0040000
0404000
0040000
0000070
0000707
0000070
```

**Train 1 — output**

```text
0000000
0040000
0444000
0040000
0000070
0000777
0000070
```

**Train 2 — input**

```text
000600000
006060000
000600000
000000000
000000500
000005050
000000500
000000000
```

**Train 2 — output**

```text
000600000
006660000
000600000
000000000
000000500
000005550
000000500
000000000
```

**Test — input**

```text
000000000
003000000
030300000
003000000
000000080
000000808
000000080
000000000
```

**Test — expected output**

```text
000000000
003000000
033300000
003000000
000000080
000000888
000000080
000000000
```

**Written solution**

Whenever a zero cell has the same nonzero color directly above, below, left, and right, fill that center with the shared color. Keep everything else as it is.

**Reference program (`solve_E86`)**

```python
def solve_E86(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            vals=[g[r-1][c],g[r+1][c],g[r][c-1],g[r][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out
```

### E87 — Complete the 2×2 corner

**What it tests:** Complete a 2×2 square when exactly three of its cells already contain the same nonzero color.

**Staged hint:** Look at every 2×2 window. If three cells match and the fourth is zero, fill the missing corner.

**Train 1 — input**

```text
0000000
0220000
0200000
0000000
0000060
0000660
0000000
```

**Train 1 — output**

```text
0000000
0220000
0220000
0000000
0000660
0000660
0000000
```

**Train 2 — input**

```text
000000000
000044000
000040000
000000000
000000700
000000770
000000000
```

**Train 2 — output**

```text
000000000
000044000
000044000
000000000
000000770
000000770
000000000
```

**Test — input**

```text
00000000
03300000
00300000
00000000
00000500
00005500
00000000
00000000
```

**Test — expected output**

```text
00000000
03300000
03300000
00000000
00005500
00005500
00000000
00000000
```

**Written solution**

Inspect every 2×2 block. If it contains exactly three copies of the same nonzero color and one zero, fill the zero with that color so the whole 2×2 block becomes solid.

**Reference program (`solve_E87`)**

```python
def solve_E87(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and 0 in vals:
                color=nz[0]
                if g[r][c]==0: out[r][c]=color
                if g[r][c+1]==0: out[r][c+1]=color
                if g[r+1][c]==0: out[r+1][c]=color
                if g[r+1][c+1]==0: out[r+1][c+1]=color
    return out
```

### E88 — Fill the straight midpoint

**What it tests:** Fill the single missing cell between two equal colors separated by exactly one blank in a row or column.

**Staged hint:** Look for A-0-A patterns horizontally and vertically.

**Train 1 — input**

```text
0000000
0202000
0000000
0006000
0000000
0006000
0000000
```

**Train 1 — output**

```text
0000000
0222000
0000000
0006000
0006000
0006000
0000000
```

**Train 2 — input**

```text
000000000
000040400
000000000
700000000
000000000
700000000
000000000
```

**Train 2 — output**

```text
000000000
000044400
000000000
700000000
700000000
700000000
000000000
```

**Test — input**

```text
000000000
003003000
000000000
000080000
000000000
000080000
000000000
```

**Test — expected output**

```text
000000000
003003000
000000000
000080000
000080000
000080000
000000000
```

**Written solution**

Whenever two equal nonzero cells lie two steps apart in the same row or column with one zero between them, fill the midpoint with that color. Nothing else changes.

**Reference program (`solve_E88`)**

```python
def solve_E88(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r][c+2] and g[r][c+1]==0:
                out[r][c+1]=g[r][c]
    for r in range(h-2):
        for c in range(w):
            if g[r][c]!=0 and g[r][c]==g[r+2][c] and g[r+1][c]==0:
                out[r+1][c]=g[r][c]
    return out
```

### E89 — Fill the diagonal midpoint

**What it tests:** Recognize matching diagonal endpoints two steps apart and fill the empty center between them.

**Staged hint:** Check both diagonal directions: top-left to bottom-right and top-right to bottom-left.

**Train 1 — input**

```text
0200000
0000000
0002000
0000000
0000060
0000000
0000006
```

**Train 1 — output**

```text
0200000
0020000
0002000
0000000
0000060
0000000
0000006
```

**Train 2 — input**

```text
00000000
00400000
00000000
00004000
00000070
00000000
00000700
00000000
```

**Train 2 — output**

```text
00000000
00400000
00040000
00004000
00000070
00000000
00000700
00000000
```

**Test — input**

```text
000000000
030000000
000000000
000300000
000000080
000000000
000008000
000000000
000000000
```

**Test — expected output**

```text
000000000
030000000
003000000
000300000
000000080
000000800
000008000
000000000
000000000
```

**Written solution**

If the same nonzero color appears at the two ends of a length-2 diagonal and the middle diagonal cell is zero, fill that middle cell with the shared color.

**Reference program (`solve_E89`)**

```python
def solve_E89(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c]!=0 and g[r][c]==g[r+2][c+2] and g[r+1][c+1]==0:
                out[r+1][c+1]=g[r][c]
    for r in range(h-2):
        for c in range(2,w):
            if g[r][c]!=0 and g[r][c]==g[r+2][c-2] and g[r+1][c-1]==0:
                out[r+1][c-1]=g[r][c]
    return out
```

### E90 — Fill the ring center

**What it tests:** Detect a hollow 3×3 ring of one color and fill its empty center.

**Staged hint:** Only zero cells can change. Ask whether all eight surrounding cells of the 3×3 neighborhood match.

**Train 1 — input**

```text
000000000
022200000
020200000
022200000
000000000
000007770
000007070
000007770
000000000
```

**Train 1 — output**

```text
000000000
022200000
022200000
022200000
000000000
000007770
000007770
000007770
000000000
```

**Train 2 — input**

```text
0003330000
0003030000
0003330000
0000000000
0000004400
0000004040
0000004400
0000000000
0000000000
```

**Train 2 — output**

```text
0003330000
0003330000
0003330000
0000000000
0000004400
0000004040
0000004400
0000000000
0000000000
```

**Test — input**

```text
0000000000
0555000000
0505000000
0555000000
0000000000
0000000666
0000000606
0000000666
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0555000000
0555000000
0555000000
0000000000
0000000666
0000000666
0000000666
0000000000
0000000000
```

**Written solution**

Whenever a zero cell is surrounded on all eight neighboring positions by the same nonzero color, fill that center with the ring color. Leave every other cell untouched.

**Reference program (`solve_E90`)**

```python
def solve_E90(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            border=[]
            ok=True
            for rr in range(r-1,r+2):
                for cc in range(c-1,c+2):
                    if (rr,cc)==(r,c): 
                        continue
                    border.append(g[rr][cc])
            if border[0]!=0 and all(v==border[0] for v in border):
                out[r][c]=border[0]
    return out
```

### E91 — Mirror across the row axis

**What it tests:** Use a 9 in each row as a local mirror axis and copy colored cells to their symmetric partner positions.

**Staged hint:** Treat each row independently. Preserve the 9 and reflect nonzero cells across it when the mirrored slot is empty.

**Train 1 — input**

```text
000000000
002090000
000090060
040090000
000000000
```

**Train 1 — output**

```text
000000000
002090200
060090060
040090040
000000000
```

**Train 2 — input**

```text
0000000000
0003009000
0700009000
0000009005
0000000000
```

**Train 2 — output**

```text
0000000000
0003009003
0700009000
0005009005
0000000000
```

**Test — input**

```text
0000000000
0040009000
0000009006
0200009000
0000000000
```

**Test — expected output**

```text
0000000000
0040009000
0006009006
0200009000
0000000000
```

**Written solution**

In any row containing a 9, treat that 9 as a reflection axis. For each nonzero non-9 cell in the row, paint the symmetric cell on the opposite side of the 9 if that mirrored position lies in bounds and is empty.

**Reference program (`solve_E91`)**

```python
def solve_E91(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        if 9 not in g[r]:
            continue
        axis=g[r].index(9)
        for c,v in enumerate(g[r]):
            if v!=0 and v!=9:
                cc=2*axis-c
                if 0<=cc<w and out[r][cc]==0:
                    out[r][cc]=v
    return out
```

## Medium

### M85 — Move the object to the marker

**What it tests:** Extract one object, crop it to its bounding box, and relocate it so that its top-left corner lands on the marker.

**Staged hint:** Ignore the background. Find the one 9, then move the whole nonzero object as a unit.

**Train 1 — input**

```text
0220000
0200000
0222000
0000000
0009000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0000000
0000000
0002200
0002000
0002220
```

**Train 2 — input**

```text
00000000
00330000
00030000
00030000
00000000
00000090
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00000000
00000000
00000033
00000003
00000003
```

**Test — input**

```text
000440000
000040000
000044400
000000000
000000000
000090000
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
000000000
000044000
000004000
000004440
000000000
```

**Written solution**

Take all nonzero cells except the 9, crop them to their tight bounding box, and paste that cropped object back onto a blank grid so that the object’s top-left corner starts exactly at the 9’s position. Remove the original object and the marker.

**Reference program (`solve_M85`)**

```python
def solve_M85(g):
    h,w=dims(g)
    marker=None
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==9:
                marker=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w,0)
    if not cells or marker is None:
        return clone(g)
    r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
    r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
    obj=blank(r1-r0+1,c1-c0+1,0)
    for r,c,v in cells:
        obj[r-r0][c-c0]=v
    return paste(out,obj,marker[0],marker[1])
```

### M86 — Commanded crop transform

**What it tests:** Use a single command cell to decide how to transform a cropped object before outputting it.

**Staged hint:** The command is in the top-left corner. First crop the object, then apply the transform selected by the command color.

**Train 1 — input**

```text
100000
002200
000200
000200
000000
```

**Train 1 — output**

```text
22
20
20
```

**Train 2 — input**

```text
2000000
0003300
0000300
0000000
0000000
```

**Train 2 — output**

```text
03
33
```

**Test — input**

```text
20000000
00004400
00000400
00000440
00000000
00000000
```

**Test — expected output**

```text
004
444
400
```

**Written solution**

Ignore the command cell after reading it. Crop the remaining nonzero object to its bounding box, then transform that crop according to the command: 1 means horizontal flip, 2 means rotate 90° clockwise, and 3 means rotate 180°. Output only the transformed crop.

**Reference program (`solve_M86`)**

```python
def solve_M86(g):
    cmd=g[0][0]
    canvas=clone(g)
    canvas[0][0]=0
    obj=crop_nonzero(canvas)
    if cmd==1:
        out=flip_h(obj)
    elif cmd==2:
        out=rot90(obj)
    elif cmd==3:
        out=rot180(obj)
    else:
        out=obj
    return out
```

### M87 — Keep the largest, recolor by the smallest

**What it tests:** Rank connected components by size, keep the largest one, and recolor it using the smallest component’s color.

**Staged hint:** Do not focus on positions first. Identify component sizes and compare them.

**Train 1 — input**

```text
0220000
0200000
0222000
0000000
0000060
0000060
0000000
0000007
```

**Train 1 — output**

```text
0770000
0700000
0777000
0000000
0000000
0000000
0000000
0000000
```

**Train 2 — input**

```text
00040000
00444000
00040000
00000000
00000060
00000060
00000060
00000000
00000002
```

**Train 2 — output**

```text
00020000
00222000
00020000
00000000
00000000
00000000
00000000
00000000
00000000
```

**Test — input**

```text
000000000
033000000
030000000
033300000
000000000
000007700
000000700
000000000
000000008
```

**Test — expected output**

```text
000000000
088000000
080000000
088800000
000000000
000000000
000000000
000000000
000000000
```

**Written solution**

Find all nonzero connected components. Determine which component is smallest and which is largest by cell count. Erase everything except the largest component, and recolor that surviving component with the smallest component’s color.

**Reference program (`solve_M87`)**

```python
def solve_M87(g):
    comps=comps_samecolor(g)
    if not comps:
        return clone(g)
    comps_sorted=sorted(comps,key=lambda vc: len(vc[1]))
    small_color=comps_sorted[0][0]
    large_cells=max(comps,key=lambda vc: len(vc[1]))[1]
    h,w=dims(g)
    out=blank(h,w,0)
    for r,c in large_cells:
        out[r][c]=small_color
    return out
```

### M88 — Stamp the prototype at every seed

**What it tests:** Recover one prototype object and copy it to every seed marker while preserving the original.

**Staged hint:** Separate the real object from the seed color. The seeds only tell you where to paste copies.

**Train 1 — input**

```text
022000000
002200000
000000000
000009000
000000000
900000000
000000000
000000000
```

**Train 1 — output**

```text
022000000
002200000
000000000
000002200
000000220
220000000
022000000
000000000
```

**Train 2 — input**

```text
000330000
000030000
000030000
000000000
009000000
000000900
000000000
000000000
```

**Train 2 — output**

```text
000330000
000030000
000030000
000000000
003300000
000300330
000300030
000000030
```

**Test — input**

```text
044000000
004400000
000000000
000009000
000000000
000000009
000000000
000000000
000000000
```

**Test — expected output**

```text
044000000
004400000
000000000
000004400
000000440
000000004
000000000
000000000
000000000
```

**Written solution**

Treat all nonzero cells except the 9s as one prototype object. Crop that object to its bounding box. Keep the original object in place, erase the 9s, and paste copies of the cropped prototype so that each seed cell becomes the top-left corner of one copy.

**Reference program (`solve_M88`)**

```python
def solve_M88(g):
    h,w=dims(g)
    seeds=[]
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==9: seeds.append((r,c))
            elif v!=0: cells.append((r,c,v))
    out=clone(g)
    for r,c in seeds: out[r][c]=0
    if not cells:
        return out
    r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
    r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
    obj=blank(r1-r0+1,c1-c0+1,0)
    for r,c,v in cells:
        obj[r-r0][c-c0]=v
    for sr,sc in seeds:
        out=paste(out,obj,sr,sc)
    return out
```

### M89 — Move the crop into the frame

**What it tests:** Extract an object from one area and relocate its crop into the interior of a frame.

**Staged hint:** Find the rectangular frame first. Then crop the other object tightly and place that crop inside the frame.

**Train 1 — input**

```text
22000000
02000000
22200000
00000000
00088880
00080080
00080080
00088880
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00088880
00082280
00080280
00082220
```

**Train 2 — input**

```text
000000000
003300000
000300000
000300000
000000000
008888000
008008000
008008000
008888000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000000000
008888000
008338000
008038000
008838000
```

**Test — input**

```text
000440000
000040000
000044400
000000000
000088888
000080008
000080008
000088888
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000000000
000088888
000084408
000080408
000088444
000000000
```

**Written solution**

Preserve the frame cells. Crop the non-frame object to its tight bounding box, erase the original object, and paste the crop into the frame interior starting at the interior’s top-left corner.

**Reference program (`solve_M89`)**

```python
def solve_M89(g):
    h,w=dims(g)
    out=blank(h,w,0)
    frame=[(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8]
    cells=[(r,c,v) for r in range(h) for c,v in enumerate(g[r]) if v not in (0,8)]
    if not frame:
        return clone(g)
    fr0,fr1,fc0,fc1=bbox_cells(frame)
    for r,c in frame:
        out[r][c]=8
    if cells:
        r0=min(r for r,c,v in cells); c0=min(c for r,c,v in cells)
        r1=max(r for r,c,v in cells); c1=max(c for r,c,v in cells)
        obj=blank(r1-r0+1,c1-c0+1,0)
        for r,c,v in cells:
            obj[r-r0][c-c0]=v
        paste(out,obj,fr0+1,fc0+1)
    return out
```

### M90 — XOR the two panels

**What it tests:** Compare two panels separated by a 9-column and mark cells that are occupied in exactly one panel.

**Staged hint:** Ignore the original colors. This is about presence versus absence in the two panels.

**Train 1 — input**

```text
2009000
0209004
0009004
0009000
```

**Train 1 — output**

```text
200
022
002
000
```

**Train 2 — input**

```text
030090000
000090500
030090500
000090000
```

**Train 2 — output**

```text
0200
0200
0000
0000
```

**Test — input**

```text
400090000
040090600
000090600
000090000
000090000
```

**Test — expected output**

```text
2000
0000
0200
0000
0000
```

**Written solution**

Split the grid into left and right panels at the all-9 separator column. For each position, output color 2 if exactly one of the two panels has a nonzero cell there, and output 0 otherwise.

**Reference program (`solve_M90`)**

```python
def solve_M90(g):
    h,w=dims(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    if sep is None:
        return clone(g)
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    h2,w2=dims(left)
    out=blank(h2,w2,0)
    for r in range(h2):
        for c in range(w2):
            if (left[r][c]!=0) ^ (right[r][c]!=0):
                out[r][c]=2
    return out
```

### M91 — Draw bounding box outlines

**What it tests:** Convert each connected component into the outline of its bounding box.

**Staged hint:** Think object-by-object. Compute a bounding box for each component and draw only the border of that box.

**Train 1 — input**

```text
0220000
0200000
0222000
0000000
0000060
0000660
0000060
```

**Train 1 — output**

```text
0222000
0202000
0222000
0000000
0000660
0000660
0000660
```

**Train 2 — input**

```text
000000000
003300000
000300000
000300000
000000000
000000550
000000050
000000550
000000000
```

**Train 2 — output**

```text
000000000
003300000
003300000
003300000
000000000
000000550
000000550
000000550
000000000
```

**Test — input**

```text
000000000
044000000
040000000
044440000
000000000
000007000
000077700
000007000
000000000
```

**Test — expected output**

```text
000000000
044440000
040040000
044440000
000000000
000077700
000070700
000077700
000000000
```

**Written solution**

For each nonzero connected component, find its bounding box. Output a blank grid of the same size, then draw the border of each bounding box in that component’s original color.

**Reference program (`solve_M91`)**

```python
def solve_M91(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for color,cells in comps_samecolor(g):
        r0,r1,c0,c1=bbox_cells(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out
```

## Hard

### H85 — Infer the transform from the example pair

**What it tests:** Use one source/target panel pair to infer a geometric transform, then apply the same transform to the query panel.

**Staged hint:** Do not hard-code a specific transform. First determine how the top-left panel became the top-right panel.

**Train 1 — input**

```text
2209022
0209020
0009000
9999999
3009000
3309000
3009000
```

**Train 1 — output**

```text
2209022
0209020
0009000
9999999
3009003
3309033
3009003
```

**Train 2 — input**

```text
4009044
4409440
0409000
9999999
0509000
5509000
0009000
```

**Train 2 — output**

```text
4009044
4409440
0409000
9999999
0509050
5509055
0009000
```

**Test — input**

```text
0609060
6609066
0609060
9999999
7009000
7709000
7009000
```

**Test — expected output**

```text
0609060
6609066
0609060
9999999
7009007
7709077
7009007
```

**Written solution**

Split the grid into four equal panels using the 9-row and 9-column separators. Identify which transform maps the top-left panel to the top-right panel, choosing among the basic flips and rotations. Apply that same transform to the bottom-left panel and write the result into the bottom-right panel.

**Reference program (`solve_H85`)**

```python
def solve_H85(g):
    h,w=dims(g)
    sep_r=None; sep_c=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep_r=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep_c=c; break
    if sep_r is None or sep_c is None:
        return clone(g)
    tl=[row[:sep_c] for row in g[:sep_r]]
    tr=[row[sep_c+1:] for row in g[:sep_r]]
    bl=[row[:sep_c] for row in g[sep_r+1:]]
    funcs=[lambda x:x, rot90, rot180, rot270, flip_h, flip_v]
    found=funcs[0]
    for f in funcs:
        if f(tl)==tr:
            found=f
            break
    br=found(bl)
    out=clone(g)
    for r in range(len(br)):
        for c in range(len(br[0])):
            out[sep_r+1+r][sep_c+1+c]=br[r][c]
    return out
```

### H86 — Recolor by the header mapping

**What it tests:** Read a palette mapping from header rows and use it to recolor a lower image.

**Staged hint:** Separate the legend from the picture. The first header row gives source colors and the second gives their replacements.

**Train 1 — input**

```text
203400
785600
002300
044000
000320
```

**Train 1 — output**

```text
007800
055000
000870
```

**Train 2 — input**

```text
5020600
3470800
0002050
0060000
5000200
```

**Train 2 — output**

```text
0004030
0070000
3000400
```

**Test — input**

```text
2040500
7860300
0002500
4400000
0000502
```

**Test — expected output**

```text
0007600
8800000
0000607
```

**Written solution**

Take the nonzero colors from the first row as source colors and the nonzero colors from the second row as their aligned replacements. Then remove the header and recolor the remaining picture by applying that source-to-target mapping cell by cell.

**Reference program (`solve_H86`)**

```python
def solve_H86(g):
    src=[v for v in g[0] if v!=0]
    tgt=[v for v in g[1] if v!=0]
    mapping={s:t for s,t in zip(src,tgt)}
    canvas=g[2:]
    out=[]
    for row in canvas:
        out.append([mapping.get(v,v) if v!=0 else 0 for v in row])
    return out
```

### H87 — Fill the chamber by nearest seed

**What it tests:** Perform a Voronoi-like fill inside a frame using the nearest interior seed color.

**Staged hint:** Work only inside the frame. For each blank interior cell, compare its Manhattan distance to every seed.

**Train 1 — input**

```text
8888888
8000008
8020008
8003008
8000008
8888888
```

**Train 1 — output**

```text
8888888
8222228
8222228
8223338
8223338
8888888
```

**Train 2 — input**

```text
88888888
80000008
80040008
80000008
80000058
88888888
```

**Train 2 — output**

```text
88888888
84444458
84444458
84444558
84445558
88888888
```

**Test — input**

```text
888888888
800000008
800200008
800000008
800000308
800000008
888888888
```

**Test — expected output**

```text
888888888
822222338
822222338
822223338
822233338
822233338
888888888
```

**Written solution**

Find the rectangular chamber bounded by 8s. Inside that chamber, keep the existing seed cells and fill every zero cell with the color of the seed that is closest in Manhattan distance. Break ties by choosing the seed that comes first in reading order.

**Reference program (`solve_H87`)**

```python
def solve_H87(g):
    h,w=dims(g)
    frame=[(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8]
    if not frame:
        return clone(g)
    r0,r1,c0,c1=bbox_cells(frame)
    seeds=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,8)]
    out=clone(g)
    seeds_sorted=sorted(seeds,key=lambda t:(t[0],t[1]))
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c]==0 and seeds_sorted:
                best=None
                bestkey=None
                for sr,sc,color in seeds_sorted:
                    key=(abs(sr-r)+abs(sc-c), sr, sc)
                    if bestkey is None or key<bestkey:
                        bestkey=key; best=color
                out[r][c]=best
    return out
```

### H88 — Mask the image, then crop it

**What it tests:** Use one panel as a binary mask over a second panel, then crop the surviving colored cells.

**Staged hint:** The left panel decides what survives. Apply the mask first, and only then crop the result tightly.

**Train 1 — input**

```text
0109000
1119044
0109040
0009000
```

**Train 1 — output**

```text
44
40
```

**Train 2 — input**

```text
110095500
011090500
001090050
000090000
```

**Train 2 — output**

```text
550
050
005
```

**Test — input**

```text
0109666
1119666
0109666
0009000
```

**Test — expected output**

```text
060
666
060
```

**Written solution**

Split the input at the 9 separator column. Treat the left panel as a binary mask and the right panel as a colored image. Keep only the right-panel cells whose corresponding left-panel positions are nonzero, erase everything else, and finally crop the surviving colored pattern to its tight bounding box.

**Reference program (`solve_H88`)**

```python
def solve_H88(g):
    h,w=dims(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    hh,ww=dims(left)
    masked=blank(hh,ww,0)
    for r in range(hh):
        for c in range(ww):
            if left[r][c]!=0 and right[r][c]!=0:
                masked[r][c]=right[r][c]
    return crop_nonzero(masked)
```

### H89 — Build the output from the prototype dictionary

**What it tests:** Read a small dictionary of keyed prototypes and assemble a new output by looking up a query sequence.

**Staged hint:** The top row gives the keys, the next three rows give the corresponding 3×3 prototypes, and the bottom row is the query.

**Train 1 — input**

```text
03005007000
02000440000
22200404000
02000440000
00000000000
73500000000
```

**Train 1 — output**

```text
40000200004
04002220004
40000200004
```

**Train 2 — input**

```text
04006008000
04400070000
04000077000
04400070000
00000000000
86400000000
```

**Train 2 — output**

```text
70000000044
77000000040
70000000044
```

**Test — input**

```text
02005009000
22200440000
02000404000
22200440000
00000000000
95200000000
```

**Test — expected output**

```text
40000040222
04000040020
40000040222
```

**Written solution**

The first row assigns a color key to each 3×3 prototype block stored below it. Read the nonzero query keys from the last row from left to right. For each query key, copy the matching 3×3 prototype into the output, concatenating the chosen prototypes horizontally with one blank column between consecutive copies.

**Reference program (`solve_H89`)**

```python
def solve_H89(g):
    h,w=dims(g)
    groups=split_prototype_groups(g)
    protos={}
    for c0,c1,key in groups:
        proto=[row[c0:c1+1] for row in g[1:4]]
        protos[key]=proto
    query=[v for v in g[-1] if v!=0]
    if not query:
        return [[0]]
    out_h=3
    out_w=len(query)*3 + (len(query)-1)
    out=blank(out_h,out_w,0)
    x=0
    for i,key in enumerate(query):
        proto=protos[key]
        for r in range(3):
            for c in range(3):
                out[r][x+c]=proto[r][c]
        x+=4
    return out
```

### H90 — Sweep the object until the wall

**What it tests:** Move an object repeatedly to the right until it would hit a wall, and paint the union of all visited positions.

**Staged hint:** This is not a single translation. Imagine the whole object sliding step by step and keep every intermediate footprint.

**Train 1 — input**

```text
220000080
020000080
000000080
000000080
```

**Train 1 — output**

```text
222222280
022222280
000000080
000000080
```

**Train 2 — input**

```text
0440000080
0040000080
0444000080
0000000080
0000000080
```

**Train 2 — output**

```text
0444444080
0044444080
0444444480
0000000080
0000000080
```

**Test — input**

```text
0660000800
0060000800
0066000800
0000000800
0000000800
```

**Test — expected output**

```text
0666660800
0066660800
0066666800
0000000800
0000000800
```

**Written solution**

Treat all nonzero non-wall cells as one movable object and all 8s as fixed wall cells. Slide the object to the right as far as possible without overlapping a wall or leaving the grid. Output the wall plus the union of the object at every intermediate horizontal position from its start to its stopping position.

**Reference program (`solve_H90`)**

```python
def solve_H90(g):
    h,w=dims(g)
    wall={(r,c) for r in range(h) for c,v in enumerate(g[r]) if v==8}
    obj=[(r,c,v) for r in range(h) for c,v in enumerate(g[r]) if v not in (0,8)]
    out=blank(h,w,0)
    for r,c in wall:
        out[r][c]=8
    if not obj:
        return out
    t=0
    while True:
        ok=True
        for r,c,v in obj:
            nc=c+t+1
            if nc>=w or (r,nc) in wall:
                ok=False
                break
        if ok:
            t+=1
        else:
            break
    for shift in range(t+1):
        for r,c,v in obj:
            out[r][c+shift]=v
    return out
```

### H91 — Infer the binary operation from the example triplet

**What it tests:** Use one three-panel example to determine whether the operation is union, intersection, or XOR, then apply it to a new pair.

**Staged hint:** Focus on occupied versus empty positions. The output color is fixed; what matters is which boolean operation explains the top row.

**Train 1 — input**

```text
20090209220
02090009020
00092009200
99999999999
20090009000
00090209000
00090009000
```

**Train 1 — output**

```text
20090209220
02090009020
00092009200
99999999999
20090009200
00090209020
00090009000
```

**Train 2 — input**

```text
30093009000
03090009020
00090039002
99999999999
04090009000
00090409000
00490049000
```

**Train 2 — output**

```text
30093009000
03090009020
00090039002
99999999999
04090009020
00090409020
00490049000
```

**Test — input**

```text
50095009200
05090009000
00090509000
99999999999
06090609000
06090009000
00090609000
```

**Test — expected output**

```text
50095009200
05090009000
00090509000
99999999999
06090609020
06090009000
00090609000
```

**Written solution**

Split the puzzle into three aligned panels across the top row and three across the bottom row using the 9 separators. Determine which boolean operation on occupied cells—union, intersection, or XOR—turns the first two top panels into the third top panel. Then apply that same operation to the two bottom input panels and write the result into the bottom output panel using color 2.

**Reference program (`solve_H91`)**

```python
def solve_H91(g):
    h,w=dims(g)
    sep_r=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep_r=r; break
    sep_cs=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    if sep_r is None or len(sep_cs)<2:
        return clone(g)
    c1,c2=sep_cs[:2]
    A=[row[:c1] for row in g[:sep_r]]
    B=[row[c1+1:c2] for row in g[:sep_r]]
    C=[row[c2+1:] for row in g[:sep_r]]
    D=[row[:c1] for row in g[sep_r+1:]]
    E=[row[c1+1:c2] for row in g[sep_r+1:]]
    def make(op,x,y):
        h,w=dims(x)
        out=blank(h,w,0)
        for r in range(h):
            for c in range(w):
                xx=x[r][c]!=0; yy=y[r][c]!=0
                flag=op(xx,yy)
                if flag: out[r][c]=2
        return out
    ops=[
        ("union", lambda a,b: a or b),
        ("intersection", lambda a,b: a and b),
        ("xor", lambda a,b: (a and not b) or (b and not a))
    ]
    chosen=ops[0][1]
    for name,op in ops:
        if make(op,A,B)==C:
            chosen=op; break
    F=make(chosen,D,E)
    out=clone(g)
    for r in range(len(F)):
        for c in range(len(F[0])):
            out[sep_r+1+r][c2+1+c]=F[r][c]
    return out
```
