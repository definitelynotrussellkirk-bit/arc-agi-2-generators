# 21 More ARC-Style Puzzles

This is the fourteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E92–E98, M92–M98, H92–H98**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into column-wise metadata, object relocation, panel transforms, prototype dictionaries, chamber fills, edit-delta transfer, and rank-based recolor/packing.

**New motifs in this batch**

**`panel_transform_from_example(example_src, example_dst, query)`** — infer a whole-panel flip or rotation from one example pair and reuse it on a query panel. This is the key move in **H92**.

**`orbit_union(anchor, shape)`** — reinterpret a shape in anchor-relative coordinates, rotate those offsets around the anchor, and output the union of all rotated copies. This is the core primitive in **H94**.

**`edit_delta_transfer(src, dst, query)`** — learn an additive edit inside an object's bounding box from one example source→target pair and apply that same relative edit to a new source. This drives **H96**.

**`rank_recolor_pack(objects, palette)`** — sort objects by area, recolor them by palette rank, crop them, and concatenate them into a new output canvas. This is the central pattern in **H98**.

## Easy

### E92 — Fill the vertical bridge

**What it tests:** Recognize same-color endpoints in a column and fill the zero cells between them.

**Staged hint:** Work color by color. Look for exactly two cells of one color that share a column.

**Train 1 — input**

```text
0000000
0002000
0000000
6000000
0002000
0000000
6000000
```

**Train 1 — output**

```text
0000000
0002000
0002000
6002000
6002000
6000000
6000000
```

**Train 2 — input**

```text
000000000
000000040
000000000
000500000
000000000
000500000
000000000
000000040
```

**Train 2 — output**

```text
000000000
000000040
000000040
000500040
000500040
000500040
000000040
000000040
```

**Test — input**

```text
00000000
00300000
00000070
00000000
00000000
00300000
00000000
00000070
```

**Test — expected output**

```text
00000000
00300000
00300070
00300070
00300070
00300070
00000070
00000070
```

**Written solution**

For each color, if it appears exactly twice in the same column with only zeros between those two cells, fill the entire vertical segment between the endpoints with that color. Leave all other cells unchanged.

**Reference program (`solve_E92`)**

```python
def solve_E92(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][1]==cells[1][1]:
            c=cells[0][1]
            a,b=sorted([cells[0][0],cells[1][0]])
            if all(grid[r][c]==0 for r in range(a+1,b)):
                for r in range(a,b+1):
                    out[r][c]=color
    return out
```

### E93 — Complete the 3×3 frame border

**What it tests:** Detect a 3×3 corner pattern and infer the missing border cells.

**Staged hint:** Scan every 3×3 window. Four equal corners are the signal.

**Train 1 — input**

```text
00000000
04040000
00000000
04040000
00000000
00007070
00000000
00007070
```

**Train 1 — output**

```text
00000000
04440000
04040000
04440000
00000000
00007770
00007070
00007770
```

**Train 2 — input**

```text
0000000
0050500
0000000
0050500
0000000
0000000
0000000
```

**Train 2 — output**

```text
0000000
0055500
0050500
0055500
0000000
0000000
0000000
```

**Test — input**

```text
000000000
000000000
006060000
000000000
006060000
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000000
006660000
006060000
006660000
000000000
000000000
000000000
000000000
```

**Written solution**

Whenever a 3×3 window has the same nonzero color in all four corners and a zero center, fill the eight border cells of that 3×3 window with the corner color. Keep the center unchanged.

**Reference program (`solve_E93`)**

```python
def solve_E93(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            vals=[grid[r][c],grid[r][c+2],grid[r+2][c],grid[r+2][c+2]]
            if vals[0]!=0 and len(set(vals))==1:
                color=vals[0]
                # interior of corners may be zeros
                # fill border if non-corners are zeros currently
                border=[(r,c),(r,c+1),(r,c+2),(r+1,c),(r+1,c+2),(r+2,c),(r+2,c+1),(r+2,c+2)]
                inner_ok = grid[r+1][c+1]==0
                side_ok = all(grid[x][y] in (0,color) for x,y in border)
                if inner_ok and side_ok:
                    for x,y in border:
                        out[x][y]=color
    return out
```

### E94 — Complete straight triplets

**What it tests:** Local horizontal and vertical line completion from two adjacent cells.

**Staged hint:** Look only at length-3 windows. Patterns of the form cc0 or 0cc are the ones that matter.

**Train 1 — input**

```text
00005000
00005000
00000000
66000000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00005000
00005000
00005000
66600000
00000000
00000000
00000000
```

**Train 2 — input**

```text
00000000
00000000
00000000
00000077
00000000
00400000
00400000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00000777
00400000
00400000
00400000
```

**Test — input**

```text
330000000
000000000
000000000
000000000
000000000
000000060
000000060
```

**Test — expected output**

```text
333000000
000000000
000000000
000000000
000000060
000000060
000000060
```

**Written solution**

In every row and column, if a length-3 segment is `color color 0` or `0 color color`, replace the zero with that color. This turns each two-cell straight segment into a three-cell straight segment.

**Reference program (`solve_E94`)**

```python
def solve_E94(grid):
    out=clone(grid)
    h,w=dims(grid)
    # horizontal 0cc or cc0
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a==0 and b!=0 and b==d:
                out[r][c]=b
            if a!=0 and a==b and d==0:
                out[r][c+2]=a
    # vertical
    for r in range(h-2):
        for c in range(w):
            a,b,d=grid[r][c],grid[r+1][c],grid[r+2][c]
            if a==0 and b!=0 and b==d:
                out[r][c]=b
            if a!=0 and a==b and d==0:
                out[r+2][c]=a
    return out
```

### E95 — Fill the X-center

**What it tests:** Use the four diagonal neighbors around a blank cell to infer a center color.

**Staged hint:** Ignore orthogonal neighbors. Only the four diagonal corners matter.

**Train 1 — input**

```text
0000000
0202000
0000000
0202000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0202000
0020000
0202000
0000000
0000000
0000000
```

**Train 2 — input**

```text
00000000
00000000
00303000
00000000
00303000
00000000
00070070
00000000
```

**Train 2 — output**

```text
00000000
00000000
00303000
00030000
00303000
00000000
00070070
00000000
```

**Test — input**

```text
000000000
000404000
000000000
000404000
000000000
060600000
000000000
060600000
000000000
```

**Test — expected output**

```text
000000000
000404000
000040000
000404000
000000000
060600000
006000000
060600000
000000000
```

**Written solution**

For any zero cell, if its four diagonal neighbors all exist and all have the same nonzero color, fill the center cell with that color. Otherwise leave it alone.

**Reference program (`solve_E95`)**

```python
def solve_E95(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c]!=0:
                continue
            vals=[grid[r-1][c-1],grid[r-1][c+1],grid[r+1][c-1],grid[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out
```

### E96 — Paint markers from the header row

**What it tests:** Column-wise metadata reading from a header row.

**Staged hint:** Treat row 0 as a legend. Marker cells borrow the color from their own column.

**Train 1 — input**

```text
02004000
00000000
01001000
00000000
00001000
01000000
00000000
```

**Train 1 — output**

```text
02004000
00000000
02004000
00000000
00004000
02000000
00000000
```

**Train 2 — input**

```text
00300070
00000000
00100010
00000000
00000000
00100000
00000010
```

**Train 2 — output**

```text
00300070
00000000
00300070
00000000
00000000
00300000
00000070
```

**Test — input**

```text
050060004
000000000
010000001
000010000
000000000
000000001
010000000
```

**Test — expected output**

```text
050060004
000000000
050000004
000060000
000000000
000000004
050000000
```

**Written solution**

The top row acts as a header. Every `1` elsewhere in the grid should be recolored to the nonzero header color in the same column; everything else stays the same.

**Reference program (`solve_E96`)**

```python
def solve_E96(grid):
    out=clone(grid)
    h,w=dims(grid)
    header=grid[0]
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1 and header[c]!=0:
                out[r][c]=header[c]
    return out
```

### E97 — Left-pack each row

**What it tests:** Stable row-wise compression that preserves color order.

**Staged hint:** Solve each row independently. Keep the nonzero sequence, then pad with zeros.

**Train 1 — input**

```text
00203000
00000000
40050060
07000008
00000000
```

**Train 1 — output**

```text
23000000
00000000
45600000
78000000
00000000
```

**Train 2 — input**

```text
0009000
0200003
0000000
0040500
0006000
```

**Train 2 — output**

```text
9000000
2300000
0000000
4500000
6000000
```

**Test — input**

```text
000000000
102030000
000000000
000405006
700000008
000000000
```

**Test — expected output**

```text
000000000
123000000
000000000
456000000
780000000
000000000
```

**Written solution**

For each row, read the nonzero cells from left to right, place that sequence at the far left of the output row, and fill the remaining cells with zero. The order of colors within each row is preserved.

**Reference program (`solve_E97`)**

```python
def solve_E97(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        vals=[v for v in grid[r] if v!=0]
        out[r][:len(vals)] = vals
    return out
```

### E98 — Fill a rectangle from opposite corners

**What it tests:** Infer an axis-aligned rectangle from two matching diagonal corner cells.

**Staged hint:** Work by color. When exactly two cells of a color are diagonal corners, fill the box they define.

**Train 1 — input**

```text
00000000
03000000
00000000
00003000
00000000
00000070
00070000
00000000
```

**Train 1 — output**

```text
00000000
03333000
03333000
03333000
00000000
00077770
00077770
00000000
```

**Train 2 — input**

```text
000000000
000500000
000000000
000000000
000000500
000000000
000000000
```

**Train 2 — output**

```text
000000000
000555500
000555500
000555500
000555500
000000000
000000000
```

**Test — input**

```text
0000000000
0000000000
0040000000
0000000000
0000000000
0000004000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0044444000
0044444000
0044444000
0044444000
0000000000
0000000000
```

**Written solution**

For each color that appears exactly twice and whose two cells differ in both row and column, treat those cells as opposite corners of an axis-aligned rectangle and fill the entire rectangle with that color.

**Reference program (`solve_E98`)**

```python
def solve_E98(grid):
    out=clone(grid)
    by=defaultdict(list)
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    for c in range(min(c1,c2), max(c1,c2)+1):
                        out[r][c]=color
    return out
```

## Medium

### M92 — Move the object to the anchor

**What it tests:** Crop a multicolor object and relocate it using a target anchor cell.

**Staged hint:** Separate the anchor from the object first. Then think in terms of the object's bounding box.

**Train 1 — input**

```text
23000000
02000000
00000000
00000000
00000800
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00000230
00000020
00000000
00000000
```

**Train 2 — input**

```text
000000000
000400000
000440000
000000000
000000000
008000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000000000
004000000
004400000
000000000
000000000
```

**Test — input**

```text
000000000
055000000
005000000
000000000
000000000
000000800
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
000000550
000000050
000000000
000000000
```

**Written solution**

Ignore the anchor color `8`, take the bounding box of the remaining nonzero object, and paste that cropped object so that its top-left corner lands on the anchor cell. The output is otherwise blank.

**Reference program (`solve_M92`)**

```python
def solve_M92(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    anchors=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==8]
    if len(anchors)!=1:
        return clone(grid)
    ar,ac=anchors[0]
    obj_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c] not in (0,8)]
    if not obj_cells:
        return clone(grid)
    r0,r1,c0,c1=bbox_cells(obj_cells)
    obj=[row[c0:c1+1] for row in grid[r0:r1+1]]
    paste(out,obj,ar,ac)
    return out
```

### M93 — Flood a frame interior from its seed

**What it tests:** Detect hollow rectangular frames and use an interior seed to determine the fill color.

**Staged hint:** First identify which component is a rectangular border. Then inspect what color is inside it.

**Train 1 — input**

```text
000000000
022222000
020002000
020302000
020002000
022222000
000000000
```

**Train 1 — output**

```text
000000000
022222000
023332000
023332000
023332000
022222000
000000000
```

**Train 2 — input**

```text
444440000
400040000
407040000
400040000
444440000
000000000
000555550
000500050
000500650
000500050
000555550
```

**Train 2 — output**

```text
444440000
477740000
477740000
477740000
444440000
000000000
000555550
000566650
000566650
000566650
000555550
```

**Test — input**

```text
000000000
006666600
006000600
006040600
006000600
006666600
000000000
```

**Test — expected output**

```text
000000000
006666600
006444600
006444600
006444600
006666600
000000000
```

**Written solution**

Find any hollow rectangular border made from one color. If there is exactly one non-frame nonzero color inside that frame, fill the entire interior of the frame with that seed color while leaving the border unchanged.

**Reference program (`solve_M93`)**

```python
def solve_M93(grid):
    out=clone(grid)
    h,w=dims(grid)
    # detect single-color rectangular frame components
    for color,cells in comps(grid, ignore=(0,)):
        r0,r1,c0,c1=bbox_cells(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            inner_colors={grid[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if grid[r][c] not in (0,color)}
            if len(inner_colors)==1:
                fill=next(iter(inner_colors))
                for r in range(r0+1,r1):
                    for c in range(c0+1,c1):
                        out[r][c]=fill
    return out
```

### M94 — Crop out the largest object

**What it tests:** Object detection, component sizing, and output-size change.

**Staged hint:** List the connected components, compare their areas, then forget everything except the largest one.

**Train 1 — input**

```text
000000000
033000000
030000600
033000600
000000600
000000000
000550000
000000000
```

**Train 1 — output**

```text
33
30
33
```

**Train 2 — input**

```text
0000000000
0000000000
0444000000
0404000000
0444000700
0000000700
0000000000
0000000000
```

**Train 2 — output**

```text
444
404
444
```

**Test — input**

```text
000000000
000220000
000220000
000000000
000000000
007000000
077700000
007000000
000000000
```

**Test — expected output**

```text
070
777
070
```

**Written solution**

Treat each connected nonzero region as an object, choose the largest one by cell count, and output only that object cropped to its bounding box. All smaller objects are discarded.

**Reference program (`solve_M94`)**

```python
def solve_M94(grid):
    comps_list=comps_any(grid, ignore=(0,))
    if not comps_list:
        return [[0]]
    cells=max(comps_list, key=len)
    return crop_bbox(grid, cells)
```

### M95 — Shift by the guide vector

**What it tests:** Extract a translation vector from two guide markers and apply it to an object.

**Staged hint:** Sort the two guide markers in reading order; the vector from the first to the second is the move.

**Train 1 — input**

```text
22000000
02000000
80000000
00080000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00022000
00002000
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
000000000
000550000
000050000
000000000
000080000
080000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
550000000
050000000
000000000
000000000
000000000
000000000
```

**Test — input**

```text
000000000
000000000
003300000
000300000
000000000
000800000
000000008
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000000033
000000003
000000000
000000000
000000000
```

**Written solution**

The two `8` markers define a translation vector from the earlier marker to the later one. Move every nonzero non-marker cell of the object by that same vector onto a blank canvas and drop the markers.

**Reference program (`solve_M95`)**

```python
def solve_M95(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    markers=sorted([(r,c) for r in range(h) for c in range(w) if grid[r][c]==8])
    if len(markers)!=2:
        return clone(grid)
    (r1,c1),(r2,c2)=markers
    dr,dc=r2-r1,c2-c1
    obj_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c] not in (0,8)]
    for r,c in obj_cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=grid[r][c]
    return out
```

### M96 — Mirror across the divider

**What it tests:** Panel-style reflection around a vertical separator.

**Staged hint:** Treat the column of 9s as a mirror axis, not as part of the object.

**Train 1 — input**

```text
000090000
022090000
020090000
000090000
000090000
```

**Train 1 — output**

```text
000090000
022090220
020090020
000090000
000090000
```

**Train 2 — input**

```text
0000090000
0060090000
0660090000
0060090000
0000090000
```

**Train 2 — output**

```text
0000090000
0060090060
0660090066
0060090060
0000090000
```

**Test — input**

```text
00000900000
00300900000
03300900000
00300900000
00000900000
00000900000
```

**Test — expected output**

```text
00000900000
00300900300
03300900330
00300900300
00000900000
00000900000
```

**Written solution**

Keep the divider of `9`s and the existing left-side object. Then reflect every nonzero non-divider cell across the divider and paint the mirrored copy on the right side.

**Reference program (`solve_M96`)**

```python
def solve_M96(grid):
    out=clone(grid)
    h,w=dims(grid)
    div=None
    for c in range(w):
        if all(grid[r][c]==9 for r in range(h)):
            div=c
            break
    if div is None:
        return clone(grid)
    for r in range(h):
        for c in range(div):
            v=grid[r][c]
            if v not in (0,9):
                mc=div + (div-c)
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

### M97 — Extract the guide-colored object

**What it tests:** Use a guide color to select one object from several distractors.

**Staged hint:** The top-left cell is not part of the object; it is a key telling you which color to keep.

**Train 1 — input**

```text
300000000
000330000
000300000
000000000
000000440
000000040
000000000
```

**Train 1 — output**

```text
33
30
```

**Train 2 — input**

```text
400000000
000000000
005500000
005500000
000000000
000044400
000004000
000000000
```

**Train 2 — output**

```text
444
040
```

**Test — input**

```text
500000000
000000000
000006000
000666000
000006000
000000000
055500000
050000000
000000000
```

**Test — expected output**

```text
555
500
```

**Written solution**

Read the guide color from the top-left cell, then find the connected object of that color elsewhere in the grid. Output only that object's bounding-box crop.

**Reference program (`solve_M97`)**

```python
def solve_M97(grid):
    h,w=dims(grid)
    target=grid[0][0]
    # ignore guide cell itself
    grid2=clone(grid)
    grid2[0][0]=0
    for color,cells in comps(grid2, ignore=(0,)):
        if color==target:
            return crop_bbox(grid2, cells)
    return [[0]]
```

### M98 — Pack objects in header order

**What it tests:** Read an ordering legend and concatenate cropped objects accordingly.

**Staged hint:** Treat the nonzero header colors as an ordered list. Match each object to one header color.

**Train 1 — input**

```text
2030000000
0000000000
0002200000
0000200000
0000000000
0000000033
0000000003
0000000000
```

**Train 1 — output**

```text
22033
02003
```

**Train 2 — input**

```text
40560000000
00000000000
04400000000
00400000000
00000000000
00000055500
00000050500
00000000000
00000000006
00000000006
00000000000
```

**Train 2 — output**

```text
44055506
04050506
```

**Test — input**

```text
730400000000
000000000000
007770000000
000700000000
000000000000
000000000440
000000000040
000000000000
000000300000
000000300000
000000000000
```

**Test — expected output**

```text
77703044
07003004
```

**Written solution**

The nonzero colors in the top row specify an order. Find the corresponding objects below, crop each one to its bounding box, and concatenate them left-to-right in header order with a single zero column between pieces.

**Reference program (`solve_M98`)**

```python
def solve_M98(grid):
    header=[v for v in grid[0] if v!=0]
    # find one object per header color
    objs={}
    body=grid[1:]
    for color,cells in comps(body, ignore=(0,)):
        if color in header:
            objs[color]=crop_bbox(body, cells)
    pieces=[objs[c] for c in header if c in objs]
    if not pieces:
        return [[0]]
    H=max(len(p) for p in pieces)
    W=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur += len(p[0])+1
    return out
```

## Hard

### H92 — Infer a panel transform from the example

**What it tests:** Meta-level transform inference from one example panel pair.

**Staged hint:** Solve the top row first: identify the exact transform from left panel to right panel. Then reuse it below.

**Train 1 — input**

```text
2209022
2009002
0009000
9999999
3309000
0309000
0309000
```

**Train 1 — output**

```text
2209022
2009002
0009000
9999999
3309003
0309333
0309000
```

**Train 2 — input**

```text
4009444
4009400
4409000
9999999
0509000
5559000
0009000
```

**Train 2 — output**

```text
4009444
4009400
4409000
9999999
0509050
5559055
0009050
```

**Test — input**

```text
0609000
6609660
0009060
9999999
0079000
0779000
0079000
```

**Test — expected output**

```text
0609000
6609660
0009060
9999999
0079777
0779070
0079000
```

**Written solution**

The top-left and top-right panels form an example pair that reveals a whole-panel transform such as a rotation or flip. Apply that same inferred transform to the bottom-left query panel and place the result into the blank bottom-right panel.

**Reference program (`solve_H92`)**

```python
def solve_H92(grid):
    h,w=dims(grid)
    # find sep row and col of all 9
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_c=next((c for c in range(w) if all(grid[r][c]==9 for r in range(h))), None)
    if sep_r is None or sep_c is None:
        return clone(grid)
    A=[row[:sep_c] for row in grid[:sep_r]]
    B=[row[sep_c+1:] for row in grid[:sep_r]]
    C=[row[:sep_c] for row in grid[sep_r+1:]]
    trans=[rot90, rot180, rot270, flip_h, flip_v]
    fn=None
    for t in trans:
        if t(A)==B:
            fn=t; break
    if fn is None:
        return clone(grid)
    D=fn(C)
    out=clone(grid)
    for r in range(len(D)):
        for c in range(len(D[0])):
            out[sep_r+1+r][sep_c+1+c]=D[r][c]
    return out
```

### H93 — Prototype dictionary lookup

**What it tests:** Read keyed prototypes from a dictionary-like layout and assemble a query sequence.

**Staged hint:** Top row gives the keys; the 3×3 blocks underneath are the prototypes. The last row asks for a sequence of keys.

**Train 1 — input**

```text
02000300040
22000330044
20000300040
00000330040
00000000000
42300000000
```

**Train 1 — output**

```text
04402200033
04002000030
04000000033
```

**Train 2 — input**

```text
05000600070
50006600777
55506060007
50000660007
00000000000
75670000000
```

**Train 2 — output**

```text
777050006600777
007055506060007
007050000660007
```

**Test — input**

```text
02000800030
22000800033
20008880030
00000800033
00000000000
83280000000
```

**Test — expected output**

```text
080003302200080
888003002000888
080003300000080
```

**Written solution**

Use the labeled 3×3 prototype blocks in the top part of the input as a dictionary from key color to shape. Then read the nonzero query sequence in the last row and concatenate the corresponding prototype blocks left-to-right with one zero column gap.

**Reference program (`solve_H93`)**

```python
def solve_H93(grid):
    h,w=dims(grid)
    # query is last row
    query=[v for v in grid[-1] if v!=0]
    groups=split_proto_dictionary(grid[:-1])  # but row0 still same if passing whole grid? not used
    # Actually use original grid row0 and rows1:4 as prototypes
    proto={}
    for key,c0,c1 in split_proto_dictionary(grid):
        proto[key]=[row[c0:c1+1] for row in grid[1:4]]
    pieces=[proto[k] for k in query if k in proto]
    if not pieces:
        return [[0]]
    H=3
    W=sum(3 for _ in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur+=4
    return out
```

### H94 — Orbit the shape around its anchor

**What it tests:** Reference-frame reasoning around an anchor and 90° rotational symmetry.

**Staged hint:** Describe every object cell relative to the anchor. Then rotate those offsets, not the raw grid.

**Train 1 — input**

```text
0000000
0002000
0002200
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0002000
0022200
0229220
0022200
0002000
0000000
```

**Train 2 — input**

```text
000000000
000000000
000044000
000004000
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
000044000
004404000
004090400
000404400
000440000
000000000
000000000
```

**Test — input**

```text
000000000
000000000
000000000
000700000
000770900
000000000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000770
000000700
000700000
000770907
000000000
000000700
000007700
000000000
```

**Written solution**

Treat the `9` cell as an anchor. Take the nonzero shape around it, rotate the shape's offsets around the anchor by 0°, 90°, 180°, and 270°, and output the union of all four copies while keeping the anchor.

**Reference program (`solve_H94`)**

```python
def solve_H94(grid):
    h,w=dims(grid)
    anchor=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    if len(anchor)!=1:
        return clone(grid)
    ar,ac=anchor[0]
    out=blank(h,w,0)
    out[ar][ac]=9
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,9)]
    for k in range(4):
        for r,c,v in obj:
            dr,dc=r-ar,c-ac
            rr,cc=rotate_point(dr,dc,k)
            nr,nc=ar+rr,ac+cc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

### H95 — Fill each chamber by nearest seed

**What it tests:** Compartment reasoning with walls and nearest-seed assignment.

**Staged hint:** First split the board into chambers separated by 9s. Then solve each chamber independently.

**Train 1 — input**

```text
999999999
900020009
900000009
909999909
900300009
900000009
999999999
```

**Train 1 — output**

```text
999999999
922222229
922222229
939999929
933333339
933333339
999999999
```

**Train 2 — input**

```text
99999999
92000049
90000009
90999009
90000009
99999999
```

**Train 2 — output**

```text
99999999
92224449
92224449
92999449
92224449
99999999
```

**Test — input**

```text
999999999
920000009
900000009
909090909
900000005
900000009
999999999
```

**Test — expected output**

```text
999999999
922222259
922222559
929295959
922255555
922255559
999999999
```

**Written solution**

Treat `9` cells as walls that partition the grid into chambers. Inside each chamber, keep the seed cells as they are and fill every zero cell with the color of the nearest seed in that same chamber, breaking ties by the smaller color value.

**Reference program (`solve_H95`)**

```python
def solve_H95(grid):
    h,w=dims(grid)
    out=clone(grid)
    # components of cells not wall 9
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,9):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=9 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if not seeds:
                continue
            for x,y in cells:
                if grid[x][y]==0:
                    best=min(seeds, key=lambda s:(abs(s[0]-x)+abs(s[1]-y), s[2], s[0], s[1]))
                    out[x][y]=best[2]
    return out
```

### H96 — Transfer the edit delta

**What it tests:** Learn a relative edit from one source→target example and apply it to a new source.

**Staged hint:** Do not compare whole panels first; compare the top source and top target inside the source object's bounding box.

**Train 1 — input**

```text
220092200
200092200
000090000
000090000
999999999
330090000
300090000
000090000
000090000
```

**Train 1 — output**

```text
220092200
200092200
000090000
000090000
999999999
330093300
300093300
000090000
000090000
```

**Train 2 — input**

```text
600096000
600096600
600096000
000090000
999999999
500090000
500090000
500090000
000090000
```

**Train 2 — output**

```text
600096000
600096600
600096000
000090000
999999999
500095000
500095500
500095000
000090000
```

**Test — input**

```text
770097700
700097700
000090000
000090000
999999999
330090000
300090000
000090000
000090000
```

**Test — expected output**

```text
770097700
700097700
000090000
000090000
999999999
330093300
300093300
000090000
000090000
```

**Written solution**

The top example shows how a source object is edited into a target object by adding cells at certain positions relative to the object's bounding box. Copy the bottom-left query panel into the blank bottom-right panel and apply the same relative additions there.

**Reference program (`solve_H96`)**

```python
def solve_H96(grid):
    h,w=dims(grid)
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_c=next((c for c in range(w) if all(grid[r][c]==9 for r in range(h))), None)
    if sep_r is None or sep_c is None:
        return clone(grid)
    A=[row[:sep_c] for row in grid[:sep_r]]
    B=[row[sep_c+1:] for row in grid[:sep_r]]
    C=[row[:sep_c] for row in grid[sep_r+1:]]
    # derive delta additions in bbox coordinates
    def bbox_nonzero(g):
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
        if not cells:
            return None
        return bbox_cells(cells)
    ba=bbox_nonzero(A); bb=bbox_nonzero(B); bc=bbox_nonzero(C)
    if ba is None or bb is None or bc is None:
        return clone(grid)
    ar0,ar1,ac0,ac1=ba
    br0,br1,bc0,bc1=bb
    cr0,cr1,cc0,cc1=bc
    # assume same bbox size example
    adds=[]
    for r in range(max(ar1-ar0+1, br1-br0+1)):
        for c in range(max(ac1-ac0+1, bc1-bc0+1)):
            av=A[ar0+r][ac0+c] if ar0+r<=ar1 and ac0+c<=ac1 else 0
            bv=B[br0+r][bc0+c] if br0+r<=br1 and bc0+c<=bc1 else 0
            if av==0 and bv!=0:
                adds.append((r,c,bv))
    out=clone(grid)
    # start with C copied to D
    for r in range(len(C)):
        for c in range(len(C[0])):
            out[sep_r+1+r][sep_c+1+c]=C[r][c]
    # dominant color in C
    qcolors=[v for row in C for v in row if v!=0]
    qcolor=max(set(qcolors), key=qcolors.count)
    for r,c,v in adds:
        nr,nc=cr0+r,cc0+c
        if 0<=nr<len(C) and 0<=nc<len(C[0]):
            out[sep_r+1+nr][sep_c+1+nc]=qcolor if v!=0 else 0
    return out
```

### H97 — Infer the hidden binary operation

**What it tests:** Learn a set operation on panels from one example and apply it to a new pair.

**Staged hint:** Top row is the worked example: panel A, panel B, result. Decide which binary operation explains it before touching the bottom row.

**Train 1 — input**

```text
22090209200
20090029200
00090009000
99999999999
02290209000
00292009000
00090009000
```

**Train 1 — output**

```text
22090209200
20090029200
00090009000
99999999999
02290209002
00292009002
00090009000
```

**Train 2 — input**

```text
04090049022
44490049222
00090009000
99999999999
50090059000
05090059000
05590009000
```

**Train 2 — output**

```text
04090049022
44490049222
00090009000
99999999999
50090059202
05090059022
05590009022
```

**Test — input**

```text
66090609200
06090669002
00090009000
99999999999
07790079000
07090779000
00090009000
```

**Test — expected output**

```text
66090609200
06090669002
00090009000
99999999999
07790079020
07090779002
00090009000
```

**Written solution**

In the top row, the first two panels combine to make the third using one hidden binary operation on occupancy, such as union, intersection, XOR, A−B, or B−A. Infer that operation and apply it to the bottom-left pair to fill the blank bottom-right result panel.

**Reference program (`solve_H97`)**

```python
def solve_H97(grid):
    h,w=dims(grid)
    sep_r=next((r for r in range(h) if all(v==9 for v in grid[r])), None)
    sep_cs=[c for c in range(w) if all(grid[r][c]==9 for r in range(h))]
    if sep_r is None or len(sep_cs)<2:
        return clone(grid)
    c1,c2=sep_cs[:2]
    A=[row[:c1] for row in grid[:sep_r]]
    B=[row[c1+1:c2] for row in grid[:sep_r]]
    C=[row[c2+1:] for row in grid[:sep_r]]
    D=[row[:c1] for row in grid[sep_r+1:]]
    E=[row[c1+1:c2] for row in grid[sep_r+1:]]
    def op_apply(name,X,Y):
        h,w=dims(X); out=blank(h,w,0)
        for r in range(h):
            for c in range(w):
                x=X[r][c]!=0; y=Y[r][c]!=0
                if name=="union" and (x or y):
                    out[r][c]=2
                elif name=="intersection" and (x and y):
                    out[r][c]=2
                elif name=="xor" and (x ^ y):
                    out[r][c]=2
                elif name=="AminusB" and (x and not y):
                    out[r][c]=2
                elif name=="BminusA" and (y and not x):
                    out[r][c]=2
        return out
    choices=["union","intersection","xor","AminusB","BminusA"]
    chosen="union"
    for name in choices:
        if op_apply(name,A,B)==C:
            chosen=name; break
    F=op_apply(chosen,D,E)
    out=clone(grid)
    for r in range(len(F)):
        for c in range(len(F[0])):
            out[sep_r+1+r][c2+1+c]=F[r][c]
    return out
```

### H98 — Recolor by size rank and pack

**What it tests:** Object sizing, rank-based palette assignment, and packed output construction.

**Staged hint:** Ignore original object colors after you detect the objects. The top row gives the new palette by rank.

**Train 1 — input**

```text
4560000000
0000000000
0110000000
0000000000
0022000000
0002000000
0000000000
0000003300
0000003300
0000000000
```

**Train 1 — output**

```text
44055066
00005066
```

**Train 2 — input**

```text
28750000000
00000000000
00100000000
00100000000
00000000000
00002220000
00002000000
00000000000
00000007700
00000007700
00000007000
```

**Train 2 — output**

```text
20888077
20800077
00000070
```

**Test — input**

```text
963400000000
000000000000
000010000000
000010000000
000000000000
000000220000
000000020000
000000000000
000000000033
000000000033
000000000000
```

**Test — expected output**

```text
9066033
9006033
```

**Written solution**

Find all nonzero connected objects below the palette row and sort them by area from smallest to largest. Recolor the smallest object with the first palette color, the next object with the second palette color, and so on, then crop and concatenate the recolored objects left-to-right with single zero-column gaps.

**Reference program (`solve_H98`)**

```python
def solve_H98(grid):
    palette=[v for v in grid[0] if v!=0]
    body=grid[1:]
    parts=[]
    for cells in comps_any(body, ignore=(0,)):
        comp_grid=crop_bbox(body,cells)
        parts.append((len(cells), comp_grid))
    parts.sort(key=lambda x:x[0])
    pieces=[]
    for i,(size,p) in enumerate(parts):
        color=palette[i]
        q=clone(p)
        for r in range(len(q)):
            for c in range(len(q[0])):
                if q[r][c]!=0:
                    q[r][c]=color
        pieces.append(q)
    if not pieces:
        return [[0]]
    H=max(len(p) for p in pieces)
    W=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(H,W,0)
    cur=0
    for p in pieces:
        paste(out,p,0,cur)
        cur += len(p[0])+1
    return out
```
