# 21 More ARC-Style Puzzles

This is the twenty-first continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E141–E147, M141–M147, H141–H147**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans more into **object filtering, guide-derived motion, panel selection, size-ranked recoloring, transform analogy, support edits, anchor orbits, and tokenized transform execution**.

**New motifs in this batch**

**`guide_union(shape, guide_a, guide_b)`** — read a translation vector from two guide dots and union the original object with a shifted copy. This is the core move in **M143**.

**`mask_carry_crop(mask, canvas)`** — use one panel as a binary selector over a second panel, then crop the selected colored result. This drives **M144**.

**`support_recolor_analogy(A, B, C)`** — infer a symmetry transform and color permutation from one panel pair and apply both to a new panel. This is the central abstraction in **H141**.

**`counted_orbit(anchor, object, k)`** — count header markers and use them to decide how many quarter-turn copies of an object to union around an anchor. This appears in **H146**.

**`token_transform_execute(tokens, shape)`** — treat a token strip as an executable transform program over a cropped shape. This is the defining primitive in **H147**.


## Easy

### E141 — Horizontal interval completion

**What it tests:** Complete each row segment whose only two nonzero endpoints match in color.


**Staged hint:** Ignore empty rows first. On an active row, the two matching colored endpoints tell you exactly what interval to fill.


**Train 1 — input**

```text
020020
000000
300003
040400
```

**Train 1 — output**

```text
022220
000000
333333
044400
```


**Train 2 — input**

```text
50050
00000
07007
00100
```

**Train 2 — output**

```text
55550
00000
07777
00000
```

**Test — input**

```text
0060060
2000002
0000000
0900090
```

**Test — output**

```text
0066660
2222222
0000000
0999990
```

**Written solution:** Look at each row independently. If the row contains exactly two nonzero cells and they have the same color, fill every cell between those two endpoints with that color, inclusive. Any row that does not satisfy that pattern becomes all 0s.

**Program solution**

```python
def solve_E141(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        nz=[(c,v) for c,v in enumerate(row) if v!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            c0,c1=nz[0][0],nz[1][0]
            color=nz[0][1]
            for c in range(min(c0,c1), max(c0,c1)+1):
                out[r][c]=color
    return out
```

### E142 — Keep the topmost nonzero per column

**What it tests:** Reduce each column to its first visible colored cell.


**Staged hint:** Work column by column. As soon as you meet the first nonzero cell, keep it and ignore everything below.


**Train 1 — input**

```text
00000
20030
04005
20630
04605
```

**Train 1 — output**

```text
00000
20030
04005
00600
00000
```


**Train 2 — input**

```text
0070
0200
5070
0209
5009
```

**Train 2 — output**

```text
0070
0200
5000
0009
0000
```

**Test — input**

```text
000000
010002
300400
015002
305060
```

**Test — output**

```text
000000
010002
300400
005000
000060
```

**Written solution:** For every column, scan from top to bottom and preserve only the first nonzero value you encounter. All lower nonzero cells in that column are erased, and columns with no nonzero cells stay empty.

**Program solution**

```python
def solve_E142(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c in range(w):
        for r in range(h):
            if grid[r][c]!=0:
                out[r][c]=grid[r][c]
                break
    return out
```

### E143 — Mirror across a vertical wall

**What it tests:** Use a full column of 8s as a mirror line and copy the left object to the right side.


**Staged hint:** Find the solid 8-wall first. Then reflect every colored cell on the left panel across that divider.


**Train 1 — input**

```text
0008000
0208000
2228000
0208000
0008000
```

**Train 1 — output**

```text
0008000
0208020
2228222
0208020
0008000
```


**Train 2 — input**

```text
000080000
033080000
003080000
003080000
```

**Train 2 — output**

```text
000080000
033080330
003080300
003080300
```

**Test — input**

```text
00000800000
04400800000
04000800000
04440800000
00000800000
```

**Test — output**

```text
00000800000
04400800440
04000800040
04440804440
00000800000
```

**Written solution:** A full vertical column of 8s divides the grid. Keep the divider and the original left-side object, then place a mirrored copy on the right by reflecting each nonzero non-8 cell across the wall.

**Program solution**

```python
def solve_E143(grid):
    h,w=dims(grid)
    div=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    out=clone(grid)
    for r in range(h):
        for c in range(div):
            v=grid[r][c]
            if v not in (0,8):
                mc=div + (div-c)
                if mc<w:
                    out[r][mc]=v
    return out
```

### E144 — Crop to the nonzero bounding box

**What it tests:** Resize the output to the minimal rectangle containing all colored cells.


**Staged hint:** Forget the surrounding empty border. Only the tight rectangle around the shape matters.


**Train 1 — input**

```text
00000
00400
04440
00400
00000
```

**Train 1 — output**

```text
040
444
040
```


**Train 2 — input**

```text
000000
020000
022000
000000
```

**Train 2 — output**

```text
20
22
```

**Test — input**

```text
000000
000700
007700
000700
000000
```

**Test — output**

```text
07
77
07
```

**Written solution:** Find the bounding box of all nonzero cells and output exactly that cropped rectangle. The outer all-0 padding is removed completely.

**Program solution**

```python
def solve_E144(grid):
    return crop_bbox(grid)
```

### E145 — Seed expands to a full cross

**What it tests:** A single colored seed generates its whole row and whole column.


**Staged hint:** Start from the lone nonzero cell. The output keeps its row and column and clears everything else.


**Train 1 — input**

```text
00000
00300
00000
00000
```

**Train 1 — output**

```text
00300
33333
00300
00300
```


**Train 2 — input**

```text
0000
0000
5000
0000
0000
```

**Train 2 — output**

```text
5000
5000
5555
5000
5000
```

**Test — input**

```text
000000
000000
000070
000000
```

**Test — output**

```text
000070
000070
777777
000070
```

**Written solution:** There is exactly one nonzero seed. Copy its color across the entire row and the entire column passing through that seed, leaving every other cell as 0.

**Program solution**

```python
def solve_E145(grid):
    h,w=dims(grid)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    assert len(seeds)==1
    r,c,v=seeds[0]
    for j in range(w): out[r][j]=v
    for i in range(h): out[i][c]=v
    return out
```

### E146 — Keep only border-touching components

**What it tests:** Filter connected components by whether they touch the outer frame.


**Staged hint:** Treat each color component as an object. Keep an object only if at least one of its cells lies on the grid border.


**Train 1 — input**

```text
220000
200300
000330
040000
044055
000050
```

**Train 1 — output**

```text
220000
200000
000000
000000
000055
000050
```


**Train 2 — input**

```text
00060
07060
07700
00008
99000
```

**Train 2 — output**

```text
00060
00060
00000
00008
99000
```

**Test — input**

```text
004400
004000
020000
022050
000055
000000
```

**Test — output**

```text
004400
004000
000000
000050
000055
000000
```

**Written solution:** Split the grid into 4-connected same-color components. Preserve only the components that touch the top, bottom, left, or right edge of the grid; erase every fully interior component.

**Program solution**

```python
def solve_E146(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells: out[r][c]=color
    return out
```

### E147 — Stamp a corner prototype at seed cells

**What it tests:** Read a 2×2 prototype from the upper-left corner and stamp it wherever a 9 seed appears.


**Staged hint:** Separate the prototype from the seeds. Once you know the 2×2 pattern, each 9 simply marks a new top-left position for a copy.


**Train 1 — input**

```text
200000
220000
009000
000090
000000
000000
```

**Train 1 — output**

```text
000000
000000
002000
002220
000022
000000
```


**Train 2 — input**

```text
0300000
3300000
0009000
0000000
0090000
0000000
```

**Train 2 — output**

```text
0000000
0000000
0000300
0003300
0003000
0033000
```

**Test — input**

```text
4400000
0400000
0090000
0000090
0009000
0000000
```

**Test — output**

```text
0000000
0000000
0044000
0004044
0004404
0000400
```

**Written solution:** The upper-left 2×2 block is a prototype. For every cell with value 9 in the body, place a copy of that 2×2 prototype with the seed as the prototype’s top-left corner. The legend and seeds themselves disappear in the output.

**Program solution**

```python
def solve_E147(grid):
    h,w=dims(grid)
    proto=[row[:2] for row in grid[:2]]
    out=blank(h,w)
    for r in range(2,h-1):
        for c in range(2,w-1):
            if grid[r][c]==9:
                for dr in range(2):
                    for dc in range(2):
                        if proto[dr][dc]!=0:
                            out[r+dr][c+dc]=proto[dr][dc]
    return out
```


## Medium

### M141 — Sweep shadow into a wall

**What it tests:** Extrude a shape horizontally until it reaches a full wall of 8s.


**Staged hint:** Find which side of the wall the shape lives on. Then sweep each occupied cell straight toward the wall, painting the full path.


**Train 1 — input**

```text
0000800
0200800
2220800
0200800
0000800
```

**Train 1 — output**

```text
0000800
0222800
2222800
0222800
0000800
```


**Train 2 — input**

```text
0080000
0080330
0080030
0080030
```

**Train 2 — output**

```text
0080000
0083330
0083330
0083330
```

**Test — input**

```text
00000800
04400800
00400800
04440800
00000800
```

**Test — output**

```text
00000800
04444800
00444800
04444800
00000800
```

**Written solution:** A full vertical wall of 8s blocks motion. Every nonzero non-8 cell casts a horizontal shadow toward that wall, filling every cell from its original position up to the wall. Preserve the wall itself.

**Program solution**

```python
def solve_M141(grid):
    h,w=dims(grid)
    wall=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    out=blank(h,w)
    for r in range(h): out[r][wall]=8
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
    side=1 if all(c<wall for r,c,v in cells) else -1
    for r,c,v in cells:
        if side==1:
            for j in range(c, wall):
                out[r][j]=v
        else:
            for j in range(wall+1, c+1):
                out[r][j]=v
    return out
```

### M142 — Keyed prototype dictionary stamping

**What it tests:** Use the top legend to choose between multiple 2×2 prototypes when stamping seeds.


**Staged hint:** Do the dictionary lookup first: each nonzero key in the top row owns the 2×2 block directly underneath it.


**Train 1 — input**

```text
200300
220300
020330
000000
020030
000000
```

**Train 1 — output**

```text
000000
000000
000000
000000
022030
002033
```


**Train 2 — input**

```text
4005000
4405000
0405500
0000000
0050400
0000000
```

**Train 2 — output**

```text
0000000
0000000
0000000
0000000
0050440
0055040
```

**Test — input**

```text
6007000
6607000
0607700
0000000
0700000
0006000
0000000
```

**Test — output**

```text
0000000
0000000
0000000
0000000
0700000
0776600
0000600
```

**Written solution:** The top legend defines several 2×2 prototypes, one for each nonzero key in the first row. In the lower body, any seed whose value matches a key causes the corresponding 2×2 prototype to be stamped at that seed position.

**Program solution**

```python
def solve_M142(grid):
    h,w=dims(grid)
    key_cols=[c for c,v in enumerate(grid[0]) if v!=0]
    proto_by_key={}
    for c in key_cols:
        proto_by_key[grid[0][c]]=[grid[1][c:c+2], grid[2][c:c+2]]
    out=blank(h,w)
    for r in range(3,h-1):
        for c in range(w-1):
            key=grid[r][c]
            if key in proto_by_key:
                proto=proto_by_key[key]
                for dr in range(2):
                    for dc in range(2):
                        v=proto[dr][dc]
                        if v!=0:
                            out[r+dr][c+dc]=v
    return out
```

### M143 — Guide-vector union copy

**What it tests:** Two guide dots define a translation vector for duplicating the main object.


**Staged hint:** Ignore the guides as objects. Their only job is to tell you the shift from the first guide to the second.


**Train 1 — input**

```text
0000000
0220090
0020000
0009000
0000000
```

**Train 1 — output**

```text
0000000
0220000
0020000
2000000
2000000
```


**Train 2 — input**

```text
000000
009000
033000
003000
000090
000000
```

**Train 2 — output**

```text
000000
000000
033000
003000
000000
000330
```

**Test — input**

```text
0000000
0040000
0444090
0000000
0090000
0000000
```

**Test — output**

```text
0000000
0040000
0444000
0000000
4000000
0000000
```

**Written solution:** There is one main colored object and exactly two guide cells with value 9. Compute the translation vector from the earlier guide to the later guide, keep the original object, and add a translated copy shifted by that vector.

**Program solution**

```python
def solve_M143(grid):
    h,w=dims(grid)
    guides=sorted((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==9)
    (r1,c1),(r2,c2)=guides
    dr,dc=r2-r1,c2-c1
    out=blank(h,w)
    for color,cells in cc(grid, ignore=(0,9)):
        for r,c in cells:
            out[r][c]=color
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=color
    return out
```

### M144 — Mask carry and crop

**What it tests:** Use a binary mask panel to select colored cells from a companion panel and then crop the result.


**Staged hint:** Line up the two panels cell-for-cell across the separator. Keep canvas cells only where the mask is nonzero, then trim away unused empty border.


**Train 1 — input**

```text
010080500
110086600
001080780
001180099
```

**Train 1 — output**

```text
0500
6600
0080
0099
```


**Train 2 — input**

```text
100182005
011080330
001080040
000080000
```

**Train 2 — output**

```text
2005
0330
0040
```

**Test — input**

```text
01100802200
11000833000
00010800040
00011800044
```

**Test — output**

```text
02200
33000
00040
00044
```

**Written solution:** The grid is split by a full 8-column into a left mask panel and a right color panel of the same size. Copy only the colored cells from the right panel that sit under nonzero mask cells on the left, and then crop the selected result to its nonzero bounding box.

**Program solution**

```python
def solve_M144(grid):
    h,w=dims(grid)
    div=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))][0]
    mask=[row[:div] for row in grid]
    canvas=[row[div+1:] for row in grid]
    selected=[]
    for r in range(h):
        for c in range(div):
            if mask[r][c]!=0 and canvas[r][c]!=0:
                selected.append((r,c,canvas[r][c]))
    if not selected:
        return [[0]]
    rs=[r for r,c,v in selected]; cs=[c for r,c,v in selected]
    r0,r1,c0,c1=min(rs),max(rs),min(cs),max(cs)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c,v in selected:
        out[r-r0][c-c0]=v
    return out
```

### M145 — Sort objects by area and pack them

**What it tests:** Reorder disconnected objects from smallest to largest and place them side by side.


**Staged hint:** Treat each connected component as a separate tile. Crop each tile tightly before packing them left to right by size.


**Train 1 — input**

```text
000000
200030
000030
400000
444000
```

**Train 1 — output**

```text
2030400
0030444
```


**Train 2 — input**

```text
0050000
0000600
7000600
7700600
7000000
```

**Train 2 — output**

```text
506070
006077
006070
```

**Test — input**

```text
0000080
9000080
0000080
4400080
0400000
```

**Test — output**

```text
904408
000408
000008
000008
```

**Written solution:** Extract every connected same-color object, crop each one to its own bounding box, sort the cropped objects by number of cells from smallest to largest, and pack them left to right with a one-column gap.

**Program solution**

```python
def solve_M145(grid):
    comps=[(len(cells), crop_component(grid,cells)) for color,cells in cc(grid)]
    comps.sort(key=lambda x: x[0])
    return pack_h([g for _,g in comps], gap=1)
```

### M146 — Palette recolor by size rank

**What it tests:** Use the top-row palette to recolor objects according to their size order.


**Staged hint:** Do not keep the original body colors. The only thing that matters is whether a component is the smallest, middle, or largest.


**Train 1 — input**

```text
2040600
0000000
1003300
0000305
0000305
```

**Train 1 — output**

```text
0000000
0000000
2006600
0000604
0000604
```


**Train 2 — input**

```text
708090
000000
200040
060040
066600
```

**Train 2 — output**

```text
000000
000000
700080
090080
099900
```

**Test — input**

```text
3050700
0000000
1000000
2200400
0220400
```

**Test — output**

```text
0000000
0000000
3000000
7700500
0770500
```

**Written solution:** The first row is a palette of three colors. In the body below, find the three connected components and rank them by area. Recolor the smallest component with the first palette color, the medium component with the second, and the largest with the third.

**Program solution**

```python
def solve_M146(grid):
    palette=[v for v in grid[0] if v!=0]
    comps=components_body(grid,1)
    comps.sort(key=lambda x: len(x[1]))
    out=blank(*dims(grid))
    for rank,(orig,cells) in enumerate(comps):
        color=palette[rank]
        for r,c in cells:
            out[r][c]=color
    return out
```

### M147 — Marker-dispatched transform

**What it tests:** A single marker chooses whether the main object is rotated or mirrored.


**Staged hint:** Separate the marker from the shape. Once the shape is cropped, marker 8 and marker 9 dispatch two different transforms.


**Train 1 — input**

```text
000080
020000
222000
002000
```

**Train 1 — output**

```text
020
022
220
```


**Train 2 — input**

```text
000009
033000
003000
003300
```

**Train 2 — output**

```text
033
030
330
```

**Test — input**

```text
000800
044000
004000
004400
```

**Test — output**

```text
004
444
400
```

**Written solution:** Ignore the lone marker cell and crop the main shape. If the marker is 8, output the shape rotated 90° clockwise. If the marker is 9, output the shape mirrored left-to-right.

**Program solution**

```python
def solve_M147(grid):
    marker=None
    shape_cells=[]
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in (8,9):
                marker=v
            elif v!=0:
                shape_cells.append((r,c))
    r0,r1,c0,c1=bbox(shape_cells)
    shape=[row[c0:c1+1] for row in grid[r0:r1+1]]
    return rot90(shape) if marker==8 else flip_h(shape)
```


## Hard

### H141 — Analogy with transform and recolor

**What it tests:** Infer both a symmetry transform and a color substitution from panel A→B, then apply them to panel C.


**Staged hint:** Support comes first, colors second. Find the geometric transform that matches A to B, then read off the color map on corresponding occupied cells.


**Train 1 — input**

```text
10284038110
12284438020
02080408022
```

**Train 1 — output**

```text
033
040
440
```


**Train 2 — input**

```text
50080228050
56680708556
00687708006
```

**Train 2 — output**

```text
020
022
770
```

**Test — input**

```text
44086008400
04086668440
04480068040
```

**Test — output**

```text
660
066
000
```

**Written solution:** The input has three panels separated by 8-columns. The second panel is the first panel after some symmetry transform plus a consistent nonzero color remapping. Infer both from A→B, then apply the same transform and recoloring to panel C.

**Program solution**

```python
def solve_H141(grid):
    a,b,c=split_by_full_sep_cols(grid, sep=8)
    name,mapping=infer_transform_and_color_map(a,b)
    return apply_color_map(TRANSFORMS[name](c), mapping)
```

### H142 — Edit-stencil transfer

**What it tests:** Infer which bbox positions were added or removed from a before/after pair and replay that edit on a query.


**Staged hint:** Compare supports, not colors. Cells removed in the example should be removed from the query, and cells added in the example should be added using the query’s own color.


**Train 1 — input**

```text
01080108050
11180118555
00080018000
```

**Train 1 — output**

```text
050
055
005
```


**Train 2 — input**

```text
22082208770
02082208070
02080008070
```

**Train 2 — output**

```text
770
770
000
```

**Test — input**

```text
03083308060
33080338660
00380038006
```

**Test — output**

```text
660
066
006
```

**Written solution:** The first two panels show a before/after edit on the same support grid. Any cell present before but absent after is a deletion; any cell absent before but present after is an addition. Apply that same add/remove stencil to the query panel, using the query’s color for added cells.

**Program solution**

```python
def solve_H142(grid):
    before,after,query=split_by_full_sep_cols(grid, sep=8)
    qcolor=next(v for row in query for v in row if v!=0)
    out=clone(query)
    h,w=dims(before)
    for r in range(h):
        for c in range(w):
            b=before[r][c]!=0
            a=after[r][c]!=0
            if b and not a:
                out[r][c]=0
            elif not b and a:
                out[r][c]=qcolor
    return out
```

### H143 — Family match under symmetry

**What it tests:** Match a query shape to one of two prototype families up to rotation or reflection and output the family’s canonical prototype.


**Staged hint:** Ignore the query’s color and orientation. Normalize shape support under symmetry and ask which prototype family it belongs to.


**Train 1 — input**

```text
20080308077
22283338070
00280308770
```

**Train 1 — output**

```text
200
222
002
```


**Train 2 — input**

```text
20080308060
22283338666
00280308060
```

**Train 2 — output**

```text
030
333
030
```

**Test — input**

```text
20080308550
22283338050
00280308055
```

**Test — output**

```text
200
222
002
```

**Written solution:** The first two panels are canonical prototype families. The third panel is a transformed, recolored version of one of those families. Determine which family matches up to symmetry, then output that family’s original canonical prototype.

**Program solution**

```python
def solve_H143(grid):
    a,b,q=split_by_full_sep_cols(grid, sep=8)
    supp_q=normalize_support(q)
    for name,fn in TRANSFORMS.items():
        if normalize_support(fn(a))==supp_q:
            return a
    return b
```

### H144 — Roomwise geodesic fill

**What it tests:** Fill every non-wall cell with the color of the nearest seed while respecting 8-walls as barriers.


**Staged hint:** Think in path distance, not straight-line distance. Colors can spread only through open cells, never through walls.


**Train 1 — input**

```text
8888888
8208038
8008008
8800088
8408058
8888888
```

**Train 1 — output**

```text
8888888
8228338
8228338
8844588
8448558
8888888
```


**Train 2 — input**

```text
888888
820038
808008
848058
800008
888888
```

**Train 2 — output**

```text
888888
822338
828338
848558
844558
888888
```

**Test — input**

```text
8888888
8200838
8080808
8080008
8408508
8888888
```

**Test — output**

```text
8888888
8222838
8282838
8485538
8448558
8888888
```

**Written solution:** Cells with value 8 are walls. Other nonzero cells are color seeds. Spread each seed through the open space using shortest-path distance on the grid, filling every reachable 0 cell with the color of the nearest seed while preserving the walls.

**Program solution**

```python
def solve_H144(grid):
    h,w=dims(grid)
    dist=[[math.inf]*w for _ in range(h)]
    col=[[0]*w for _ in range(h)]
    pq=[]
    for r in range(h):
        for c in range(w):
            if grid[r][c] not in (0,8):
                dist[r][c]=0
                col[r][c]=grid[r][c]
                heapq.heappush(pq,(0,grid[r][c],r,c))
            elif grid[r][c]==8:
                col[r][c]=8
    while pq:
        d,color,r,c=heapq.heappop(pq)
        if d!=dist[r][c] or color!=col[r][c]:
            continue
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and grid[nr][nc]!=8:
                nd=d+1
                if nd<dist[nr][nc] or (nd==dist[nr][nc] and color<col[nr][nc]):
                    dist[nr][nc]=nd
                    col[nr][nc]=color
                    heapq.heappush(pq,(nd,color,nr,nc))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=8 if grid[r][c]==8 else col[r][c]
    return out
```

### H145 — Infer the binary support operation

**What it tests:** Learn a set operation from example panels and apply it to a new pair.


**Staged hint:** Focus only on occupied positions. Decide whether the example result is union, intersection, or XOR of the first two supports.


**Train 1 — input**

```text
2008020822085008005
2208220800080508050
0008000800080008000
```

**Train 1 — output**

```text
505
000
000
```


**Train 2 — input**

```text
0208002802286608066
2228222800080608060
0008000800080008000
```

**Train 2 — output**

```text
606
000
000
```

**Test — input**

```text
0708070800080408040
7708077870784408044
0008000800080008000
```

**Test — output**

```text
000
404
000
```

**Written solution:** The first three panels show two input supports and their result under one fixed binary operation. Infer whether the operation is union, intersection, or XOR on occupied cells, then apply the same operation to the last two query panels and paint the output in the query color.

**Program solution**

```python
def solve_H145(grid):
    a,b,r,c,d=split_by_full_sep_cols(grid, sep=8)
    ops={
        "union": lambda x,y: x|y,
        "intersection": lambda x,y: x&y,
        "xor": lambda x,y: x^y,
    }
    sa,sb,sr=support(a),support(b),support(r)
    op=None
    for name,fn in ops.items():
        if fn(sa,sb)==sr:
            op=fn; break
    qcolor=next(v for panel in (c,d) for row in panel for v in row if v!=0)
    out=blank(*dims(c))
    for r0,c0 in op(support(c), support(d)):
        out[r0][c0]=qcolor
    return out
```

### H146 — Counted orbit around an anchor

**What it tests:** A header count says how many quarter-turn copies of an object to add around a 9 anchor.


**Staged hint:** The top row is not part of the output body. It only counts how many 90° rotations beyond the original should be included.


**Train 1 — input**

```text
10000
00200
00920
00000
00000
```

**Train 1 — output**

```text
00200
02920
00000
00000
```


**Train 2 — input**

```text
1100000
0000000
0200000
0290000
0000000
0000000
```

**Train 2 — output**

```text
0000000
0200000
0292000
0222000
0000000
```

**Test — input**

```text
111000
000000
033000
009000
000000
000000
```

**Test — output**

```text
000000
033300
039300
033300
000000
```

**Written solution:** Count the number of 1s in the top header row. In the body below, rotate the colored object around the anchor cell 9 by 90° clockwise repeatedly, keeping the original plus that many additional quarter-turn copies, and output only the body grid.

**Program solution**

```python
def solve_H146(grid):
    k=sum(1 for v in grid[0] if v==1)
    body=[row[:] for row in grid[1:]]
    h,w=dims(body)
    ar,ac=[(r,c) for r,row in enumerate(body) for c,v in enumerate(row) if v==9][0]
    obj=[(r,c,v) for r,row in enumerate(body) for c,v in enumerate(row) if v not in (0,9)]
    out=blank(h,w)
    out[ar][ac]=9
    for turns in range(k+1):
        for r,c,v in obj:
            nr,nc=rotate_point_about_anchor(r,c, ar,ac, turns)
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

### H147 — Execute a transform token strip

**What it tests:** A token row applies a sequence of grid transforms to the body shape.


**Staged hint:** Read the tokens left to right and compose them in order after cropping the body shape.


**Train 1 — input**

```text
2000
8888
0500
5550
0050
```

**Train 1 — output**

```text
050
055
550
```


**Train 2 — input**

```text
3400
8888
0660
0060
0066
```

**Train 2 — output**

```text
006
666
600
```

**Test — input**

```text
23000
88888
07000
77700
00700
```

**Test — output**

```text
070
770
077
```

**Written solution:** Crop the shape below the 8-separator row, then execute the token sequence from left to right. Token 2 means rotate 90° clockwise, token 3 means horizontal mirror, and token 4 means transpose.

**Program solution**

```python
def solve_H147(grid):
    tokens=[v for v in grid[0] if v!=0]
    shape=crop_bbox(grid[2:])
    op_map={2:rot90, 3:flip_h, 4:transpose}
    out=shape
    for t in tokens:
        out=op_map[t](out)
    return out
```
