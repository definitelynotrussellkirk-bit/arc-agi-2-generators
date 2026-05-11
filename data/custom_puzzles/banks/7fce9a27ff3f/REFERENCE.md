# 21 More ARC-Style Puzzles

This is the twelfth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E78–E84, M78–M84, H78–H84**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into support-relative translation, line and point symmetry, marker-conditioned panel transforms, horizontal sweep shadows, analogy panels, keyed prototype stamping, counted vector copies, compartment flooding, and header-based dispatch.

**New motifs in this batch**

**`support_drop(shape, line)`** — move a whole object until it sits exactly one row above a support segment. This is the core move in **M78**.

**`marker_dispatch_transform(marker, panel)`** — use a symbolic marker to choose a geometric transform for a source panel. This drives **M80**.

**`counted_vector_copy(object, vector, k)`** — replicate an object along a measured vector a counted number of times. This is central to **H81**.

**`header_dispatch(row_header, col_header, mask)`** — treat interior symbols as instructions to pull colors from row or column headers. This is the main idea in **H84**.

## Easy

### E78 — Fill the vertical bridge

**What it tests:** Recognize matching endpoints in a column and fill the blank vertical interval between them.

**Staged hint:** Work column by column. Ignore colors that do not appear as a clean two-endpoint pair in one column.

**Train 1 — input**

```text
00000060
00200000
00000000
00000060
00200000
00000000
00000000
```

**Train 1 — output**

```text
00000060
00200060
00200060
00200060
00200000
00000000
00000000
```

**Train 2 — input**

```text
000000000
040000000
000007000
000000000
000000000
000007000
040000000
000000000
```

**Train 2 — output**

```text
000000000
040000000
040007000
040007000
040007000
040007000
040000000
000000000
```

**Test — input**

```text
0003000000
0000000000
0000000800
0000000000
0003000000
0000000000
0000000800
0000000000
```

**Test — expected output**

```text
0003000000
0003000000
0003000800
0003000800
0003000800
0000000800
0000000800
0000000000
```

**Written solution**

For each color, if it appears exactly twice in the same column with only zeros between the two cells, fill the whole vertical segment between those endpoints with that color. Leave everything else unchanged.

**Reference program (`solve_E78`)**

```python
def solve_E78(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][1]==cells[1][1]:
            c=cells[0][1]
            a,b=sorted([cells[0][0], cells[1][0]])
            if all(g[r][c]==0 for r in range(a+1,b)):
                for r in range(a,b+1):
                    out[r][c]=color
    return out
```

### E79 — Fill the diamond center

**What it tests:** Detect four equal diagonal corners around an empty center and fill the center cell.

**Staged hint:** Look only at empty cells. Ask whether the four diagonals around one empty spot all carry the same nonzero color.

**Train 1 — input**

```text
00000000
04040000
00000707
04040000
00000707
00000000
00000000
```

**Train 1 — output**

```text
00000000
04040000
00400707
04040070
00000707
00000000
00000000
```

**Train 2 — input**

```text
00000000
00003030
00000000
00003030
08080000
00000000
08080000
00000000
```

**Train 2 — output**

```text
00000000
00003030
00000300
00003030
08080000
00800000
08080000
00000000
```

**Test — input**

```text
000000000
020200000
000000606
020200000
000000606
000040400
000000000
000040400
000000000
```

**Test — expected output**

```text
000000000
020200000
002000606
020200060
000000606
000040400
000004000
000040400
000000000
```

**Written solution**

Whenever an empty cell has the same nonzero color on all four diagonal neighbors, fill that center with the shared color. All other cells stay as they are.

**Reference program (`solve_E79`)**

```python
def solve_E79(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out
```

### E80 — Remove the singleton noise

**What it tests:** Filter components by size and keep only shapes made of at least two connected cells.

**Staged hint:** Ignore color names at first. Just separate connected components and check their sizes.

**Train 1 — input**

```text
00000004
02000000
02200000
00000000
00000660
00000000
00700000
```

**Train 1 — output**

```text
00000000
02000000
02200000
00000000
00000660
00000000
00000000
```

**Train 2 — input**

```text
50000000
00003000
00003300
00000300
00000000
08000000
08000000
00000002
```

**Train 2 — output**

```text
00000000
00003000
00003300
00000300
00000000
08000000
08000000
00000000
```

**Test — input**

```text
000000002
040000000
040000000
040000003
000007700
000000700
000000000
000600000
```

**Test — expected output**

```text
000000000
040000000
040000000
040000000
000007700
000000700
000000000
000000000
```

**Written solution**

Find every 4-connected nonzero component. Erase components of size 1 and keep every component of size 2 or larger exactly as it is.

**Reference program (`solve_E80`)**

```python
def solve_E80(g):
    out=blank(*dims(g),0)
    for v,cells in components(g):
        if len(cells)>=2:
            for r,c in cells:
                out[r][c]=v
    return out
```

### E81 — Turn a diagonal pair into a 2x2 block

**What it tests:** Complete a 2x2 square when only its diagonal pair of same-colored cells is present.

**Staged hint:** Find diagonal-adjacent pairs first. Then look at the 2x2 box they define.

**Train 1 — input**

```text
00000000
02000000
00200000
00000000
00000600
00006000
00000000
```

**Train 1 — output**

```text
00000000
02200000
02200000
00000000
00006600
00006600
00000000
```

**Train 2 — input**

```text
00000000
00000300
00003000
00000000
00000000
07000000
00700000
00000000
```

**Train 2 — output**

```text
00000000
00003300
00003300
00000000
00000000
07700000
07700000
00000000
```

**Test — input**

```text
000000000
040000000
004000800
000008000
000000000
000200000
000020000
000000000
```

**Test — expected output**

```text
000000000
044000000
044008800
000008800
000000000
000220000
000220000
000000000
```

**Written solution**

Whenever two same-colored cells occupy opposite corners of a 2x2 box, fill the other two cells of that 2x2 with the same color. Preserve the rest of the grid.

**Reference program (`solve_E81`)**

```python
def solve_E81(g):
    out=clone(g)
    h,w=dims(g)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        s=set(cells)
        for r,c in cells:
            for dr,dc in ((1,1),(1,-1)):
                if (r+dr,c+dc) in s:
                    rs=sorted([r,r+dr])
                    cs=sorted([c,c+dc])
                    if rs[1]-rs[0]==1 and cs[1]-cs[0]==1:
                        for rr in rs:
                            for cc in cs:
                                out[rr][cc]=color
    return out
```

### E82 — Fill the center of each hollow 3x3 square

**What it tests:** Recognize 3x3 monochrome rings and fill their missing center cell.

**Staged hint:** Scan only the 3x3 neighborhoods around empty cells; do not treat larger shapes as candidates.

**Train 1 — input**

```text
000000000
022200000
020200000
022206660
000006060
000006660
000000000
```

**Train 1 — output**

```text
000000000
022200000
022200000
022206660
000006660
000006660
000000000
```

**Train 2 — input**

```text
000000000
000044400
000040400
000044400
000000000
088800000
080800000
088800000
000000000
```

**Train 2 — output**

```text
000000000
000044400
000044400
000044400
000000000
088800000
088800000
088800000
000000000
```

**Test — input**

```text
0000000000
0333000000
0303007770
0333007070
0000007770
0000222000
0000202000
0000222000
0000000000
```

**Test — expected output**

```text
0000000000
0333000000
0333007770
0333007770
0000007770
0000222000
0000222000
0000222000
0000000000
```

**Written solution**

If an empty cell is surrounded by the same nonzero color on all eight positions of its 3x3 neighborhood, fill the center with that color.

**Reference program (`solve_E82`)**

```python
def solve_E82(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            border=[]
            for rr in range(r-1,r+2):
                for cc in range(c-1,c+2):
                    if (rr,cc)!=(r,c):
                        border.append(g[rr][cc])
            if border[0]!=0 and all(v==border[0] for v in border):
                out[r][c]=border[0]
    return out
```

### E83 — Repair one-cell line gaps

**What it tests:** Fill a missing cell when two equal-colored cells are separated by exactly one blank in a row or column.

**Staged hint:** This is not long-interval filling. Only look for a single zero sandwiched between equal endpoints.

**Train 1 — input**

```text
000000000
020200000
000000000
404000000
000000600
000000000
000000600
```

**Train 1 — output**

```text
000000000
022200000
000000000
444000000
000000600
000000600
000000600
```

**Train 2 — input**

```text
00000000
00000050
00003000
00000050
00003000
00000000
08080000
00000000
```

**Train 2 — output**

```text
00000000
00000050
00003050
00003050
00003000
00000000
08880000
00000000
```

**Test — input**

```text
000000000
004040000
600000000
000000070
600000000
000000070
020200000
000000000
```

**Test — expected output**

```text
000000000
004440000
600000000
600000070
600000070
000000070
022200000
000000000
```

**Written solution**

Whenever you see x 0 x horizontally or vertically with the same nonzero color x on both sides, replace the 0 by x. Perform that repair everywhere it applies.

**Reference program (`solve_E83`)**

```python
def solve_E83(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out
```

### E84 — Mirror the top half below the separator

**What it tests:** Use a full separator row to reflect the pattern above it into the empty space below.

**Staged hint:** First find the all-9 separator row. Then copy top rows downward in reverse order.

**Train 1 — input**

```text
00000060
02000000
00200600
99999999
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000060
02000000
00200600
99999999
00200600
02000000
00000060
```

**Train 2 — input**

```text
000070000
003000000
000000300
070000000
999999999
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000070000
003000000
000000300
070000000
999999999
070000000
000000300
003000000
000070000
```

**Test — input**

```text
0400000060
0002000000
0000020000
0000000400
9999999999
0000000000
0000000000
0000000000
0000000000
```

**Test — expected output**

```text
0400000060
0002000000
0000020000
0000000400
9999999999
0000000400
0000020000
0002000000
0400000060
```

**Written solution**

Locate the row made entirely of 9s. Reflect the rows above that separator into the rows below it, preserving the separator itself.

**Reference program (`solve_E84`)**

```python
def solve_E84(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep=r
            break
    out=clone(g)
    if sep is None:
        return out
    for r in range(sep):
        rr=sep+1+(sep-1-r)
        if 0<=rr<h:
            for c in range(w):
                if out[rr][c]==0:
                    out[rr][c]=g[r][c]
    return out
```

## Medium

### M78 — Drop the object onto the support line

**What it tests:** Translate a whole shape until it sits directly above a horizontal support segment.

**Staged hint:** Ignore the object's color and internal shape at first. Measure only its bottom row and the support row.

**Train 1 — input**

```text
00000000
00400000
00440000
00000000
00000000
00000000
09999990
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00400000
00440000
09999990
00000000
```

**Train 2 — input**

```text
000006600
000006000
000006000
000000000
000000000
000000000
000000000
009999990
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000006600
000006000
000006000
009999990
000000000
```

**Test — input**

```text
0000000000
0030000000
0333000000
0000000000
0000000000
0000000000
0000000000
0000000000
0009999990
```

**Test — expected output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0030000000
0333000000
0009999990
```

**Written solution**

Keep the support line fixed. Move the entire non-support object straight downward so that its lowest occupied row ends exactly one row above the row containing the 9 support segment.

**Reference program (`solve_M78`)**

```python
def solve_M78(g):
    h,w=dims(g)
    out=blank(h,w,0)
    support_row=None
    for r in range(h):
        if any(v==9 for v in g[r]) and all(v in (0,9) for v in g[r]):
            support_row=r
            for c,v in enumerate(g[r]):
                if v==9:
                    out[r][c]=9
    cells=[]
    maxr=-10
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cells.append((r,c,v))
                maxr=max(maxr,r)
    if not cells or support_row is None:
        return clone(g)
    delta=(support_row-1)-maxr
    for r,c,v in cells:
        out[r+delta][c]=v
    return out
```

### M79 — Reflect the object across the marked axis

**What it tests:** Use a full vertical 9-axis as a mirror and copy the object to the other side.

**Staged hint:** Treat the 9 column as the hinge. Preserve the original object and add its mirror image.

**Train 1 — input**

```text
000090000
000090000
030090000
033090000
000090000
000090000
000090000
```

**Train 1 — output**

```text
000090000
000090000
030090030
033090330
000090000
000090000
000090000
```

**Train 2 — input**

```text
00000900000
00200900000
00440900000
00200900000
00000900000
00000900000
00000900000
00000900000
```

**Train 2 — output**

```text
00000900000
00200900200
00440904400
00200900200
00000900000
00000900000
00000900000
00000900000
```

**Test — input**

```text
00000900000
00000900000
00600900000
06600900000
06800900000
00000900000
00000900000
00000900000
00000900000
```

**Test — expected output**

```text
00000900000
00000900000
00600900600
06600900660
06800900860
00000900000
00000900000
00000900000
00000900000
```

**Written solution**

Find the full vertical line of 9s. Reflect every nonzero non-9 cell across that axis to the opposite side, keeping the original cells as well.

**Reference program (`solve_M79`)**

```python
def solve_M79(g):
    h,w=dims(g)
    out=clone(g)
    axis=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            axis=c
            break
    if axis is None:
        return out
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cc=2*axis-c
                if 0<=cc<w:
                    out[r][cc]=v
    return out
```

### M80 — Use the marker to choose a panel transform

**What it tests:** Read a marker color, then apply the corresponding transform from the left panel into the blank right panel.

**Staged hint:** Do not touch the source panel first. Learn what marker 2 and marker 3 mean, then only transform the left 5x5 panel into the right one.

**Train 1 — input**

```text
200000000000
040000900000
040000900000
044000900000
000000900000
000000900000
```

**Train 1 — output**

```text
200000000000
040000900004
040000900004
044000900044
000000900000
000000900000
```

**Train 2 — input**

```text
300000000000
055000900000
005000900000
005000900000
000000900000
000000900000
```

**Train 2 — output**

```text
300000000000
055000900005
005000900555
005000900000
000000900000
000000900000
```

**Test — input**

```text
300000000000
007000900000
007000900000
077000900000
000000900000
000000900000
```

**Test — expected output**

```text
300000000000
007000900700
007000900777
077000900000
000000900000
000000900000
```

**Written solution**

The row-0 marker chooses the transform for the source panel. Marker 2 means flip the source horizontally; marker 3 means rotate the source 90 degrees clockwise. Write the transformed result into the blank panel on the right.

**Reference program (`solve_M80`)**

```python
def solve_M80(g):
    h,w=dims(g)
    marker=g[0][0]
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(1,h)):
            sep=c
            break
    if sep is None:
        return clone(g)
    src=[row[1:sep] for row in g[1:]]
    if marker==2:
        trans=flip_h(src)
    elif marker==3:
        trans=rot90(src)
    else:
        trans=src
    out=clone(g)
    th=len(g)-1
    tw=w-sep-1
    for r in range(th):
        for c in range(tw):
            out[r+1][sep+1+c]=trans[r][c]
    return out
```

### M81 — Sweep the shape to the right

**What it tests:** Extrude a whole object by repeatedly translating it rightward and taking the union of all positions.

**Staged hint:** Separate the marker from the object. Then imagine shifting the object one step right, then again, until it would leave the grid.

**Train 1 — input**

```text
70000000
00000000
02000000
02200000
00000000
00000000
```

**Train 1 — output**

```text
70000000
00000000
02222220
02222222
00000000
00000000
```

**Train 2 — input**

```text
700000000
000000000
000000000
004400000
000400000
000000000
000000000
```

**Train 2 — output**

```text
700000000
000000000
000000000
004444444
000444444
000000000
000000000
```

**Test — input**

```text
7000000000
0000000000
0060000000
0066000000
0006000000
0000000000
0000000000
```

**Test — expected output**

```text
7000000000
0000000000
0066666660
0066666666
0006666666
0000000000
0000000000
```

**Written solution**

Ignore the 7 marker. Take the nonzero object and union together all of its horizontal translations to the right until the shifted copy would run off the grid.

**Reference program (`solve_M81`)**

```python
def solve_M81(g):
    h,w=dims(g)
    out=clone(g)
    obj=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,7):
                obj.append((r,c,v))
    if not obj:
        return out
    maxc=max(c for r,c,v in obj)
    for shift in range(1,w-maxc):
        for r,c,v in obj:
            if c+shift<w:
                out[r][c+shift]=v
    return out
```

### M82 — Crop the object chosen by the key cell

**What it tests:** Select the component whose color matches the key cell, then return only that component's bounding box.

**Staged hint:** Read the key color first. Ignore all components of other colors before you crop anything.

**Train 1 — input**

```text
60000000
00000000
00000000
00006000
00066600
00000000
00000020
00000000
```

**Train 1 — output**

```text
060
666
```

**Train 2 — input**

```text
400000000
000000700
000000700
000000000
040000000
044000000
004000000
000000000
000000000
```

**Train 2 — output**

```text
40
44
04
```

**Test — input**

```text
3000000000
0000000000
0000003000
0000003000
0000033000
0000000000
0880000000
0800000000
0000000000
```

**Test — expected output**

```text
03
03
33
```

**Written solution**

The cell at the top-left is a key. Find the main disconnected component with that same color elsewhere in the grid, compute its minimal bounding box, and output that cropped subgrid.

**Reference program (`solve_M82`)**

```python
def solve_M82(g):
    key=g[0][0]
    target=None
    for v,cells in components(g, ignore=(0,)):
        if v==key and (0,0) not in cells:
            if target is None or len(cells)>len(target):
                target=cells
    if target is None:
        return [[key]]
    r0,r1,c0,c1=bbox(target)
    return [row[c0:c1+1] for row in g[r0:r1+1]]
```

### M83 — Copy the object by point reflection

**What it tests:** Use a single 9 anchor as a center of 180-degree rotation and add the reflected copy.

**Staged hint:** Treat the 9 cell as a point, not a line. Every object's offset from that point should be negated.

**Train 1 — input**

```text
0000000
0440000
0400000
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0440000
0400000
0009000
0000040
0000440
0000000
```

**Train 2 — input**

```text
000000000
000000000
002600000
006000000
000090000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
002600000
006000000
000090000
000000600
000006200
000000000
000000000
```

**Test — input**

```text
000000000
007000000
037700000
000000000
000090000
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
007000000
037700000
000000000
000090000
000000000
000007730
000000700
000000000
```

**Written solution**

Locate the single 9 anchor. For every nonzero non-9 cell, place a second copy at the point-reflected position across that anchor, preserving colors and keeping the original cells too.

**Reference program (`solve_M83`)**

```python
def solve_M83(g):
    h,w=dims(g)
    out=clone(g)
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    if not anchors:
        return out
    ar,ac=anchors[0]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                rr,cc=2*ar-r,2*ac-c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out
```

### M84 — Transplant the shape into the colored frame

**What it tests:** Copy the left panel's occupancy pattern into the right panel and recolor it with the frame's color.

**Staged hint:** Extract only the shape mask from the left side. The right side already tells you the target color.

**Train 1 — input**

```text
00000966666
02200960006
02000960006
02200960006
00000966666
```

**Train 1 — output**

```text
00000966666
02200966606
02000966006
02200966606
00000966666
```

**Train 2 — input**

```text
0000009333333
0040009300003
0440009300003
0040009300003
0000009300003
0000009333333
```

**Train 2 — output**

```text
0000009333333
0040009303003
0440009333003
0040009303003
0000009300003
0000009333333
```

**Test — input**

```text
0000009888888
0700009800008
0777009800008
0007009800008
0000009800008
0000009888888
```

**Test — expected output**

```text
0000009888888
0700009880008
0777009888808
0007009800808
0000009800008
0000009888888
```

**Written solution**

Use the left panel as a binary shape mask. In the right panel, keep the existing frame and fill the cells in the same positions as the left shape using the frame color.

**Reference program (`solve_M84`)**

```python
def solve_M84(g):
    h,w=dims(g)
    out=clone(g)
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c
            break
    if sep is None:
        return out
    left=[row[:sep] for row in g]
    right=[row[sep+1:] for row in g]
    border_color=None
    for r in range(h):
        for v in right[r]:
            if v!=0:
                border_color=v
                break
        if border_color is not None:
            break
    for r in range(h):
        for c,v in enumerate(left[r]):
            if v!=0:
                out[r][sep+1+c]=border_color
    return out
```

## Hard

### H78 — Panel analogy by rotation

**What it tests:** Infer a panel-to-panel geometric transform from the first pair and apply it to a later panel.

**Staged hint:** Use the first two panels only to identify the transformation. Do not mix them with the query panel until you know the rule.

**Train 1 — input**

```text
00000900000900000900000
02000902220900400900000
02000902000900400900000
02200900000904400900000
00000900000900000900000
```

**Train 1 — output**

```text
00000900000900000900000
02000902220900400904000
02000902000900400904440
02200900000904400900000
00000900000900000900000
```

**Train 2 — input**

```text
00600900000900000900000
00660900000933000900000
00000900066903000900000
00000900060903000900000
00000900000900000900000
```

**Train 2 — output**

```text
00600900000900000900030
00660900000933000903330
00000900066903000900000
00000900060903000900000
00000900000900000900000
```

**Test — input**

```text
00000900000908000900000
07700900070908800900000
00700907770900800900000
00700900000900000900000
00000900000900000900000
```

**Test — expected output**

```text
00000900000908000900000
07700900070908800900088
00700907770900800900880
00700900000900000900000
00000900000900000900000
```

**Written solution**

The second panel is the first panel rotated 90 degrees clockwise. Apply that same rotation to the third panel and write the result into the blank fourth panel.

**Reference program (`solve_H78`)**

```python
def solve_H78(g):
    h,w=dims(g)
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[w]
    panels=[[row[s:e] for row in g] for s,e in zip(starts,ends)]
    _,_,C,D=panels
    trans=rot90(C)
    out=clone(g)
    s=starts[3]
    for r in range(h):
        for c in range(len(D[0])):
            out[r][s+c]=trans[r][c]
    return out
```

### H79 — Panel analogy by XOR overlay

**What it tests:** Read a binary shape operation from example panels and apply it to a second pair.

**Staged hint:** Treat colors as occupancy only. First decide what operation turns the first two panels into the third.

**Train 1 — input**

```text
00000900000900000900000900000900000
02200900300902000904000900600900000
02000900300902200904400900660900000
00000900300900200900400900000900000
00000900000900000900000900000900000
```

**Train 1 — output**

```text
00000900000900000900000900000900000
02200900300902000904000900600902200
02000900300902200904400900660902020
00000900300900200900400900000900200
00000900000900000900000900000900000
```

**Train 2 — input**

```text
07000900000902000900000900000900000
07000988800920200900000900200900000
07000900000902000905000900220900000
00000900000900000905500900000900000
00000900000900000900000900000900000
```

**Train 2 — output**

```text
07000900000902000900000900000900000
07000988800920200900000900200900200
07000900000902000905000900220902220
00000900000900000905500900000902200
00000900000900000900000900000900000
```

**Test — input**

```text
00000906600902200900000900700900000
40000900600920200903300900770900000
40000900600920200900300900000900000
44000900000922000900300900000900000
00000900000900000900000900000900000
```

**Test — expected output**

```text
00000906600902200900000900700900200
40000900600920200903300900770902020
40000900600920200900300900000900200
44000900000922000900300900000900200
00000900000900000900000900000900000
```

**Written solution**

The third panel is the XOR of the first two: cells occupied in exactly one input panel survive. Apply that same XOR operation to the fourth and fifth panels and place the result in the blank sixth panel.

**Reference program (`solve_H79`)**

```python
def solve_H79(g):
    h,w=dims(g)
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[w]
    panels=[[row[s:e] for row in g] for s,e in zip(starts,ends)]
    _,_,_,Q1,Q2,OUT=panels
    res=apply_xor(Q1,Q2)
    out=clone(g)
    s=starts[5]
    for r in range(h):
        for c in range(len(OUT[0])):
            out[r][s+c]=res[r][c]
    return out
```

### H80 — Prototype dictionary stamping

**What it tests:** Read a small keyed pattern library and stamp each prototype wherever its key appears on the canvas.

**Staged hint:** Separate the top dictionary from the bottom canvas first. The top does not transform; it only tells you what to stamp for each key.

**Train 1 — input**

```text
02090009600
22090449060
00090409006
99999999999
00000000000
00200000000
00000000000
00000000600
00000400000
00000000000
00000000000
```

**Train 1 — output**

```text
02090009600
22090449060
00090409006
99999999999
00200000000
02200000000
00000006000
00000000600
00000440060
00000400000
00000000000
```

**Train 2 — input**

```text
03090009707
03095559070
03090009070
99999999999
00000000000
00000000070
03000000000
00000000000
00000000000
00000500000
00000000000
```

**Train 2 — output**

```text
03090009707
03095559070
03090009070
99999999999
00000000707
03000000070
03000000070
03000000000
00000000000
00005550000
00000000000
```

**Test — input**

```text
02090009400
02298809040
00098009044
99999999999
00000000000
00000000000
00200000000
00000000000
00000008000
04000000000
00000000000
```

**Test — expected output**

```text
02090009400
02298809040
00098009044
99999999999
00000000000
00200000000
00220000000
00000000000
40000088000
04000080000
04400000000
```

**Written solution**

Above the separator row sit several 3x3 prototype boxes. The center color of each box is its key, and the nonzero pattern of that box is the template to stamp, centered on any matching key cell below the separator.

**Reference program (`solve_H80`)**

```python
def solve_H80(g):
    h,w=dims(g)
    sep=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            sep=r
            break
    top=g[:sep]
    ht,wt=dims(top)
    sepcols=[c for c in range(wt) if all(top[r][c]==9 for r in range(ht))]
    starts=[0]+[c+1 for c in sepcols]
    ends=sepcols+[wt]
    boxes=[[row[s:e] for row in top] for s,e in zip(starts,ends)]
    protos={}
    for box in boxes:
        key=box[1][1]
        cells=[(r-1,c-1) for r in range(3) for c in range(3) if box[r][c]!=0]
        protos[key]=cells
    out=clone(g)
    base=sep+1
    for r in range(base,h):
        for c,v in enumerate(g[r]):
            if v in protos:
                for dr,dc in protos[v]:
                    rr,cc=r+dr,c+dc
                    if base<=rr<h and 0<=cc<w:
                        out[rr][cc]=v
    return out
```

### H81 — Repeat the object along the measured vector

**What it tests:** Use one marker pair as a displacement vector and another marker count as the number of copies.

**Staged hint:** Find the vector first, then count how many 3-cells there are. Only after that start placing repeated copies.

**Train 1 — input**

```text
10200000
00000000
04000000
04400000
00000000
00000000
00000000
33000000
```

**Train 1 — output**

```text
10200000
00000000
04040400
04444440
00000000
00000000
00000000
33000000
```

**Train 2 — input**

```text
100000000
200000000
000066000
000006000
000000000
000000000
000000000
000000000
333000000
```

**Train 2 — output**

```text
100000000
200000000
000066000
000066000
000066000
000066000
000006000
000000000
333000000
```

**Test — input**

```text
0102000000
0000000000
0080000000
0088000000
0008000000
0000000000
0000000000
0000000000
3330000000
```

**Test — expected output**

```text
0102000000
0000000000
0080808080
0088888888
0008080808
0000000000
0000000000
0000000000
3330000000
```

**Written solution**

The vector from marker 1 to marker 2 gives the translation step. Count the number of 3-cells; if there are k of them, draw the original object plus k additional translated copies along that vector.

**Reference program (`solve_H81`)**

```python
def solve_H81(g):
    h,w=dims(g)
    out=blank(h,w,0)
    p1=p2=None
    k=0
    obj=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==1:
                p1=(r,c)
                out[r][c]=1
            elif v==2:
                p2=(r,c)
                out[r][c]=2
            elif v==3:
                k+=1
                out[r][c]=3
            elif v!=0:
                obj.append((r,c,v))
    if not p1 or not p2:
        return clone(g)
    dr,dc=p2[0]-p1[0],p2[1]-p1[1]
    for mult in range(k+1):
        for r,c,v in obj:
            rr,cc=r+mult*dr,c+mult*dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out
```

### H82 — Compose geometry from one example and recoloring from another

**What it tests:** Extract a spatial transform from one example pair and a color map from another, then apply both to the query.

**Staged hint:** Solve this in two passes: geometry first, recoloring second.

**Train 1 — input**

```text
200090002
200090002
220090022
000090000
999999999
000090000
044090660
070090800
000090000
999999999
740090000
040090000
044090000
000090000
```

**Train 1 — output**

```text
200090002
200090002
220090022
000090000
999999999
000090000
044090660
070090800
000090000
999999999
740090068
040090060
044090660
000090000
```

**Train 2 — input**

```text
033090000
003090003
003090333
000090000
999999999
000090000
020090700
025090740
000090000
999999999
005090000
220090000
020090000
020090000
```

**Train 2 — output**

```text
033090000
003090003
003090333
000090000
999999999
000090000
020090700
025090740
000090000
999999999
005090070
220097770
020090004
020090000
```

**Test — input**

```text
060090000
060096600
660090600
000090600
999999999
000090000
033090550
008090020
000090000
999999999
080090000
300090000
330090000
030090000
```

**Test — expected output**

```text
060090000
060096600
660090600
000090600
999999999
000090000
033090550
008090020
000090000
999999999
080090500
300095500
330095000
030090200
```

**Written solution**

The top example pair teaches a geometric transform, while the middle example pair teaches a nonzero color substitution map. Apply the learned geometry to the bottom-left query and then recolor the transformed result using the learned map, writing it into the blank bottom-right panel.

**Reference program (`solve_H82`)**

```python
def solve_H82(g):
    h,w=dims(g)
    seprows=[r for r in range(h) if all(v==9 for v in g[r])]
    sepcols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    csep=sepcols[0]
    r1,r2=seprows
    topL=[row[:csep] for row in g[:r1]]
    topR=[row[csep+1:] for row in g[:r1]]
    midL=[row[:csep] for row in g[r1+1:r2]]
    midR=[row[csep+1:] for row in g[r1+1:r2]]
    botL=[row[:csep] for row in g[r2+1:]]
    botR=[row[csep+1:] for row in g[r2+1:]]

    def identity(x): return clone(x)
    candidates=[identity,rot90,rot180,rot270,flip_h,flip_v]
    geom=identity
    for fn in candidates:
        if fn(topL)==topR:
            geom=fn
            break

    cmap={}
    mh,mw=dims(midL)
    for r in range(mh):
        for c in range(mw):
            a,b=midL[r][c],midR[r][c]
            if a!=0:
                cmap[a]=b

    tmp=geom(botL)
    res=[[cmap.get(v,v) if v!=0 else 0 for v in row] for row in tmp]

    out=clone(g)
    brs=r2+1
    for r in range(len(botR)):
        for c in range(len(botR[0])):
            out[brs+r][csep+1+c]=res[r][c]
    return out
```

### H83 — Fill each walled compartment from its border key

**What it tests:** Flood separate zero compartments using the colored border key that opens into each one.

**Staged hint:** Treat 5 as an absolute wall. Start the fill only from border colors that touch interior zero cells.

**Train 1 — input**

```text
552555555
500050005
300050005
500050005
555555555
500050005
700050004
500050005
555555555
```

**Train 1 — output**

```text
552555555
522250005
322250005
522250005
555555555
577754445
777754444
577754445
555555555
```

**Train 2 — input**

```text
5255565585
5005005005
5005005005
5005005005
5005005005
5005005005
5005005005
5005005005
5555555555
```

**Train 2 — output**

```text
5255565585
5225665885
5225665885
5225665885
5225665885
5225665885
5225665885
5225665885
5555555555
```

**Test — input**

```text
5535555555
5000500005
7000500005
5000500005
5000500005
5555555555
5000500005
5000500005
2000500006
5555555555
```

**Test — expected output**

```text
5535555555
5333500005
7333500005
5333500005
5333500005
5555555555
5222566665
5222566665
2222566666
5555555555
```

**Written solution**

The 5-cells are walls. Each colored cell on the outer border serves as a seed for the zero compartment it touches. Flood-fill each compartment with the corresponding border color, without crossing any 5-wall.

**Reference program (`solve_H83`)**

```python
def solve_H83(g):
    h,w=dims(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if r in (0,h-1) or c in (0,w-1):
                v=g[r][c]
                if v not in (0,5):
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=r+dr,c+dc
                        if 0<=nr<h and 0<=nc<w and g[nr][nc]==0 and (nr,nc) not in seen:
                            q=deque([(nr,nc)])
                            seen.add((nr,nc))
                            cells=[]
                            while q:
                                x,y=q.popleft()
                                cells.append((x,y))
                                for ddx,ddy in ((1,0),(-1,0),(0,1),(0,-1)):
                                    xx,yy=x+ddx,y+ddy
                                    if 0<=xx<h and 0<=yy<w and g[xx][yy]==0 and (xx,yy) not in seen:
                                        seen.add((xx,yy))
                                        q.append((xx,yy))
                            for x,y in cells:
                                out[x][y]=v
    return out
```

### H84 — Dispatch colors from row and column headers

**What it tests:** Use row headers and column headers as two different palettes, chosen by symbolic interior markers.

**Staged hint:** Do not treat the interior values as colors. Treat 1 and 2 as instructions.

**Train 1 — input**

```text
046728
310200
501020
220010
600100
402000
```

**Train 1 — output**

```text
046728
330700
505020
240020
600600
406000
```

**Train 2 — input**

```text
0825637
4020010
7100200
6001000
2010000
5000020
8200100
```

**Train 2 — output**

```text
0825637
4020040
7700600
6006000
2020000
5000030
8800800
```

**Test — input**

```text
03682745
21002000
50010020
70200100
40000002
62001000
80000010
```

**Test — expected output**

```text
03682745
22002000
50050040
70600700
40000005
63006000
80000080
```

**Written solution**

Keep the top row and left column as headers. Inside the grid, every 1 should be replaced by that row's header color, while every 2 should be replaced by that column's header color. Zeros remain zero.

**Reference program (`solve_H84`)**

```python
def solve_H84(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for c in range(w):
        out[0][c]=g[0][c]
    for r in range(h):
        out[r][0]=g[r][0]
    for r in range(1,h):
        for c in range(1,w):
            v=g[r][c]
            if v==1:
                out[r][c]=g[r][0]
            elif v==2:
                out[r][c]=g[0][c]
    return out
```
