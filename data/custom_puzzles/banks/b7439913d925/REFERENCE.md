# 21 More ARC-Style Puzzles

This is the eighteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E120–E126, M120–M126, H120–H126**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into row metadata, corner completion, mirror symmetry, legend strips, vector transport, mask-based cropping, anchor stamping, example-inferred transforms, transform+recolor composition, inferred binary operations, stencil transfer, nearest-seed fills, prototype-family matching, and packed inventories.

**New motifs in this batch**

**`row_header_dispatch(row)`** — treat the first cell in a row as metadata that repaints a single marker elsewhere in that row. This is the central idea in **E120**.

**`mask_crop_normalize(mask, source)`** — use one panel as a binary selector on another panel, keep only the selected colored cells, and crop them tightly. This drives **M122**.

**`operation_from_example(a, b, r)`** — infer which binary panel operation produced the example result, then reuse that operation on a query pair. This is the key abstraction in **H121**.

**`stencil_delta_transfer(before, after, query)`** — infer which bbox-relative cells were added in an example edit and add those same relative cells to a new object. This powers **H122**.

**`prototype_family_match(library, query)`** — identify which stored prototype matches the query up to rotation or reflection, then emit the stored canonical prototype with the query color. This is the heart of **H124**.

**`transform_then_conflict_merge(example_before, example_after, x, y)`** — infer a transform from one example pair, apply it to a query panel, then merge it with another panel so nonmatching overlaps become color 9. This appears in **H126**.

## Easy

### E120 — Row header paints the marker

**What it tests:** Use the nonzero cell in column 0 as row metadata and paint the single marker 1 in that row with that header color.

**Staged hint:** Work row by row. Ignore empty rows. When a row starts with a nonzero header and contains one marker 1 elsewhere, move the header color onto the marker and blank the header cell.

**Train 1 — input**

```text
0000000
3001000
0000000
7000001
0000000
4000100
```

**Train 1 — output**

```text
0000000
0003000
0000000
0000007
0000000
0000400
```

**Train 2 — input**

```text
000000
200001
000000
600100
000000
900010
```

**Train 2 — output**

```text
000000
000002
000000
000600
000000
000090
```

**Test — input**

```text
00000000
50000100
00000000
80000001
30010000
00000000
```

**Test — output**

```text
00000000
00000500
00000000
00000008
00030000
00000000
```

**Written solution:** Read each row independently. A nonzero value in column 0 is not part of the final picture; it is a row header that tells you which color to place on that row's single marker 1. Move that header color onto the marker and blank the header cell.

**Program solution**

```python
def solve_E120(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        header=grid[r][0]
        if header!=0:
            markers=[c for c in range(1,w) if grid[r][c]==1]
            if len(markers)==1:
                out[r][0]=0
                out[r][markers[0]]=header
    return out
```

### E121 — Complete the 2×2 corner

**What it tests:** Find any 2×2 block with three equal nonzero cells and one blank, then fill the missing corner.

**Staged hint:** Scan every 2×2 window. If it contains exactly three copies of the same color and one 0, the 0 is the missing corner.

**Train 1 — input**

```text
000000
220000
200330
000300
000000
```

**Train 1 — output**

```text
000000
220000
220330
000330
000000
```

**Train 2 — input**

```text
7000000
7700000
0000440
0000040
0000000
```

**Train 2 — output**

```text
7700000
7700000
0000440
0000440
0000000
```

**Test — input**

```text
0000000
0550000
0050000
0000000
0003300
0003000
```

**Test — output**

```text
0000000
0550000
0550000
0000000
0003300
0003300
```

**Written solution:** Sweep over every 2×2 window. Whenever three cells in the window are the same nonzero color and the fourth is 0, the transformation is simply to complete that missing corner with the shared color.

**Program solution**

```python
def solve_E121(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                idx=vals.index(0)
                rr=r+idx//2; cc_=c+idx%2
                out[rr][cc_]=nz[0]
    return out
```

### E122 — Keep only the largest object

**What it tests:** Detect connected components and keep the unique largest one while erasing all smaller components.

**Staged hint:** Count the size of each 4-connected nonzero object. Copy only the biggest object to the output.

**Train 1 — input**

```text
0000000
0222000
0002000
0000000
0033000
0003000
0000004
```

**Train 1 — output**

```text
0000000
0222000
0002000
0000000
0000000
0000000
0000000
```

**Train 2 — input**

```text
00000000
04440000
04000000
04400000
00000000
00066000
00006000
00000000
```

**Train 2 — output**

```text
00000000
04440000
04000000
04400000
00000000
00000000
00000000
00000000
```

**Test — input**

```text
000000000
003330000
000030000
000000000
000077700
000070000
000077000
000000000
000000220
```

**Test — output**

```text
000000000
000000000
000000000
000000000
000077700
000070000
000077000
000000000
000000000
```

**Written solution:** Break the picture into 4-connected nonzero objects and compare their sizes. The output keeps only the unique largest component in its original position and removes every smaller object.

**Program solution**

```python
def solve_E122(grid):
    h,w=dims(grid)
    comps=cc(grid)
    if not comps:
        return blank(h,w)
    comps_sorted=sorted(comps, key=lambda t: len(t[1]), reverse=True)
    keep=set(comps_sorted[0][1])
    out=blank(h,w)
    for color,cells in comps:
        if set(cells)==keep:
            for r,c in cells:
                out[r][c]=color
    return out
```

### E123 — Reflect the left half across the 9-axis

**What it tests:** Use the full vertical line of 9s as a mirror axis and copy every colored cell on the left to its symmetric position on the right.

**Staged hint:** First find the column that is entirely 9. Then mirror each nonzero non-9 cell across that axis.

**Train 1 — input**

```text
0009000
0209000
0229000
0009000
0309000
0339000
0009000
```

**Train 1 — output**

```text
0009000
0209020
0229220
0009000
0309030
0339330
0009000
```

**Train 2 — input**

```text
000090000
040090000
044090000
004090000
000090000
007090000
007790000
000090000
```

**Train 2 — output**

```text
000090000
040090040
044090440
004090400
000090000
007090700
007797700
000090000
```

**Test — input**

```text
000090000
006090000
066090000
006090000
000090000
002290000
000090000
```

**Test — output**

```text
000090000
006090600
066090660
006090600
000090000
002292200
000090000
```

**Written solution:** The full column of 9s is a mirror axis. Copy every colored cell on the left side to the symmetric location on the right side while keeping the original left half and the 9-axis unchanged.

**Program solution**

```python
def solve_E123(grid):
    out=clone(grid)
    h,w=dims(grid)
    axes=[c for c in range(w) if all(grid[r][c]==9 for r in range(h))]
    assert len(axes)==1
    a=axes[0]
    for r in range(h):
        for c in range(a):
            v=grid[r][c]
            if v not in (0,9):
                mc=2*a-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

### E124 — Complete the missing plus arm

**What it tests:** Identify a plus-shaped cluster missing exactly one cardinal arm and fill that arm.

**Staged hint:** Treat each nonzero cell as a possible center. If three of its four cardinal neighbors match it and the fourth is 0, fill the missing arm.

**Train 1 — input**

```text
0000000
0004000
0044400
0000000
0000000
```

**Train 1 — output**

```text
0000000
0004000
0044400
0004000
0000000
```

**Train 2 — input**

```text
000000000
000700000
000700000
007770000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000700000
000700000
007770000
000700000
000000000
```

**Test — input**

```text
000000000
000500000
005550000
000000000
000000000
000660000
000600000
000660000
000000000
```

**Test — output**

```text
000000000
000500000
005550000
000500000
000000000
000660000
000600000
000660000
000000000
```

**Written solution:** Treat each nonzero cell as a possible plus center. If exactly three of its four cardinal neighbors match the center color and the remaining in-bounds neighbor is blank, fill that blank to complete the plus.

**Program solution**

```python
def solve_E124(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==0: 
                continue
            neigh=[(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            same=[]; zeros=[]
            for rr,cc_ in neigh:
                if 0<=rr<h and 0<=cc_<w:
                    if grid[rr][cc_]==v: same.append((rr,cc_))
                    elif grid[rr][cc_]==0: zeros.append((rr,cc_))
            if len(same)==3 and len(zeros)>=1:
                # fill only if exactly one cardinal direction within bounds is zero and others same?
                # Determine directions
                vals=[]
                for rr,cc_ in neigh:
                    if 0<=rr<h and 0<=cc_<w:
                        vals.append(grid[rr][cc_])
                    else:
                        vals.append(None)
                if sum(x==v for x in vals)==3 and sum(x==0 for x in vals)==1:
                    idx=vals.index(0)
                    rr,cc_=neigh[idx]
                    out[rr][cc_]=v
    return out
```

### E125 — Fill the center of each 3×3 ring

**What it tests:** Detect solid 3×3 rings and fill their blank centers with the ring color.

**Staged hint:** Look for 3×3 windows whose eight border cells are the same nonzero color and whose center is 0.

**Train 1 — input**

```text
0000000
0222000
0202000
0222000
0000000
0077700
0070700
0077700
```

**Train 1 — output**

```text
0000000
0222000
0222000
0222000
0000000
0077700
0077700
0077700
```

**Train 2 — input**

```text
000000000
000444000
000404000
000444000
000000000
003330000
003030000
003330000
000000000
```

**Train 2 — output**

```text
000000000
000444000
000444000
000444000
000000000
003330000
003330000
003330000
000000000
```

**Test — input**

```text
000000000
055500000
050500000
055500000
000000000
000666000
000606000
000666000
000000000
```

**Test — output**

```text
000000000
055500000
055500000
055500000
000000000
000666000
000666000
000666000
000000000
```

**Written solution:** Look for 3×3 windows whose eight border cells all share one nonzero color while the center is empty. Each such ring gets its middle cell filled with the same ring color.

**Program solution**

```python
def solve_E125(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            cells=[grid[r+i][c+j] for i in range(3) for j in range(3)]
            border=[cells[k] for k in [0,1,2,3,5,6,7,8]]
            center=cells[4]
            nz=[v for v in border if v!=0]
            if len(nz)==8 and len(set(nz))==1 and center==0:
                out[r+1][c+1]=nz[0]
    return out
```

### E126 — Draw the rectangle border from opposite corners

**What it tests:** When a color appears exactly twice as opposite rectangle corners, draw the full border of that rectangle.

**Staged hint:** For each color, take its two cells as opposite corners. Paint the top, bottom, left, and right edges of the implied rectangle.

**Train 1 — input**

```text
0000000
0200000
0000000
0000200
0000000
0007000
0000000
0700000
```

**Train 1 — output**

```text
0000000
0222200
0200200
0222200
0000000
0777000
0707000
0777000
```

**Train 2 — input**

```text
00000000
00300000
00000000
00000030
00000000
00040000
00000000
40000000
```

**Train 2 — output**

```text
00000000
00333330
00300030
00333330
00000000
44440000
40040000
44440000
```

**Test — input**

```text
000000000
000600000
000000000
000000600
000000000
005000000
000000000
000000050
000000000
```

**Test — output**

```text
000000000
000666600
000600600
000666600
000000000
005555550
005000050
005555550
000000000
```

**Written solution:** For each color, take its two cells as opposite corners of an axis-aligned rectangle. Draw the rectangle border by filling the top edge, bottom edge, left edge, and right edge in that color.

**Program solution**

```python
def solve_E126(grid):
    h,w=dims(grid)
    out=blank(h,w)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                r0,r1_=sorted([r1,r2]); c0,c1_=sorted([c1,c2])
                for c in range(c0,c1_+1):
                    out[r0][c]=color
                    out[r1_][c]=color
                for r in range(r0,r1_+1):
                    out[r][c0]=color
                    out[r][c1_]=color
    return out
```

## Medium

### M120 — Legend strip recolors the body

**What it tests:** Read a source→target color mapping from the first two rows and apply it to the body of the grid.

**Staged hint:** Treat row 0 as the source legend and row 1 as the target legend. Match nonzero columns, then recolor every body cell accordingly and blank the legend rows.

**Train 1 — input**

```text
2340000
7860000
0203400
0030040
4002000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0708600
0080060
6007000
0000000
```

**Train 2 — input**

```text
670000
230000
006700
700060
060000
000000
```

**Train 2 — output**

```text
000000
000000
002300
300020
020000
000000
```

**Test — input**

```text
48200000
63900000
00482000
80030020
00000000
02000480
```

**Test — output**

```text
00000000
00000000
00639000
30030090
00000000
09000630
```

**Written solution:** The first two rows encode a color substitution table: each nonzero entry in row 0 maps to the nonzero entry directly below it in row 1. Apply that recoloring to every body cell and clear the legend rows in the output.

**Program solution**

```python
def solve_M120(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        s=grid[0][c]; t=grid[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    out=blank(h,w)
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            out[r][c]=mapping.get(v,v)
    return out
```

### M121 — Translate the object by the guide vector

**What it tests:** Use the vector from marker 1 to marker 2 and apply that same translation to the colored object.

**Staged hint:** Ignore colors 1 and 2 except as guides. Compute the displacement from 1 to 2, then move every other nonzero cell by that vector.

**Train 1 — input**

```text
0000400
0100440
0000000
0020000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0000040
0000044
0000000
0000000
0000000
```

**Train 2 — input**

```text
00000000
00000000
07000000
07700000
01000000
00020000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00070000
00077000
00000000
00000000
00000000
```

**Test — input**

```text
000000000
000000000
001000000
000000660
000000060
000000000
000002000
000000000
000000000
```

**Test — output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Written solution:** The two guide markers 1 and 2 define a displacement vector. Ignore them as picture content, compute the vector from 1 to 2, and translate every other nonzero cell by that same offset into a blank output grid.

**Program solution**

```python
def solve_M121(grid):
    h,w=dims(grid)
    pos1=pos2=None
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==1: pos1=(r,c)
            elif grid[r][c]==2: pos2=(r,c)
    dr=pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,1,2):
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out
```

### M122 — Use the left panel as a crop mask

**What it tests:** Treat the left panel as a binary mask, keep only the overlapping colored cells from the right panel, and normalize the result to its bounding box.

**Staged hint:** Overlay the two panels cellwise. Wherever the left panel is nonzero, keep the right-panel color. Then crop the kept cells tightly.

**Train 1 — input**

```text
100052000
110052300
010050300
000050000
```

**Train 1 — output**

```text
20
23
03
```

**Train 2 — input**

```text
011050440
001050060
111056660
000050000
```

**Train 2 — output**

```text
044
006
666
```

**Test — input**

```text
010050700
111057800
010050800
000050000
```

**Test — output**

```text
07
78
08
```

**Written solution:** Overlay the left and right panels cellwise. Keep the right-panel color only where the left panel's mask is nonzero, then crop the selected colored cells to their tight bounding box.

**Program solution**

```python
def solve_M122(grid):
    mask,src = split_panel_row(grid,2,sep=5)
    cells=[]
    colors={}
    h,w=dims(mask)
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0 and src[r][c]!=0:
                cells.append((r,c))
                colors[(r,c)]=src[r][c]
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for (r,c),v in colors.items():
        out[r-r0][c-c0]=v
    return out
```

### M123 — Recolor objects by area rank

**What it tests:** Sort the body objects from smallest to largest and recolor them using the palette listed in the top row.

**Staged hint:** Ignore the palette row until the end. Measure each 4-connected object, rank the objects by area, and repaint them with palette colors in ascending-size order.

**Train 1 — input**

```text
2460000
0088000
0008000
0000000
0000880
0000000
0000008
```

**Train 1 — output**

```text
0000000
0066000
0006000
0000000
0000440
0000000
0000002
```

**Train 2 — input**

```text
35700000
00090000
00090000
00000000
00999000
00009000
00000009
00000000
```

**Train 2 — output**

```text
00000000
00050000
00050000
00000000
00777000
00007000
00000003
00000000
```

**Test — input**

```text
864000000
000770000
000070000
000000000
000077700
000000000
000000070
000000000
```

**Test — output**

```text
000000000
000660000
000060000
000000000
000044400
000000000
000000080
000000000
```

**Written solution:** Ignore the top palette row until after you measure the body objects. Rank the objects from smallest to largest area, then repaint them in place using the palette colors from left to right in that rank order.

**Program solution**

```python
def solve_M123(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body)
    comps_sorted=sorted(comps, key=lambda t: len(t[1]))  # ascending
    out=blank(h,w)
    for idx,(color,cells) in enumerate(comps_sorted):
        newc=palette[idx]
        for r,c in cells:
            out[r+1][c]=newc
    return out
```

### M124 — Stamp the anchored prototype at every 9

**What it tests:** Find the one connected prototype that includes a 9 anchor, then copy its non-anchor shape to every 9 position.

**Staged hint:** Use the 9 inside the prototype as the origin. Record the relative offsets of the prototype's colored cells, then replay those offsets at every 9 in the grid.

**Train 1 — input**

```text
0930000
0330000
0000000
0009000
0000000
0000009
0000000
```

**Train 1 — output**

```text
0030000
0330000
0000000
0000300
0003300
0000000
0000003
```

**Train 2 — input**

```text
00000000
00920000
09220000
00000000
00009000
00000000
00000009
00000000
```

**Train 2 — output**

```text
00000000
00020000
00220000
02200000
00000200
00002200
00000000
00000002
```

**Test — input**

```text
000000000
004000000
049400000
004000000
000000000
000000900
000000000
900000000
000000000
```

**Test — output**

```text
000000000
004000000
040400000
004000000
000000400
000004040
400000400
040000000
400000000
```

**Written solution:** Find the one connected prototype object that contains a 9 anchor. Record the offsets of all non-anchor cells relative to that 9, then stamp those offsets at every 9 position in the grid and omit the 9s themselves from the output.

**Program solution**

```python
def solve_M124(grid):
    h,w=dims(grid)
    comps=cc_any(grid, ignore=(0,))
    proto=None
    for color,cells in comps:
        vals=[grid[r][c] for r,c in cells]
        if 9 in vals and len(cells)>1:
            proto=cells
            break
    assert proto is not None
    anchor=[(r,c) for r,c in proto if grid[r][c]==9][0]
    rel=[(r-anchor[0], c-anchor[1], grid[r][c]) for r,c in proto if grid[r][c]!=9]
    targets=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    out=blank(h,w)
    for ar,ac in targets:
        for dr,dc,v in rel:
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

### M125 — Fill each walled room from its seed

**What it tests:** Walls split the grid into rooms, and each room contains exactly one seed color. Flood the whole room with that color.

**Staged hint:** Treat 5 as a wall. For each connected non-wall region, identify its single seed color and fill every 0 in that region with that seed.

**Train 1 — input**

```text
555555555
520500305
500500005
555555555
540500605
500500005
555555555
```

**Train 1 — output**

```text
555555555
522533335
522533335
555555555
544566665
544566665
555555555
```

**Train 2 — input**

```text
55555555
53005045
50005005
55555555
56007005
50000005
55555555
```

**Train 2 — output**

```text
55555555
53335445
53335445
55555555
56007005
50000005
55555555
```

**Test — input**

```text
555555555
570500205
500500005
555555555
530500405
500500005
555555555
```

**Test — output**

```text
555555555
577522225
577522225
555555555
533544445
533544445
555555555
```

**Written solution:** Treat color 5 as walls that partition the board into separate rooms. In each non-wall room, there is exactly one seed color; fill every blank in that room with the seed while preserving the walls.

**Program solution**

```python
def solve_M125(grid):
    h,w=dims(grid)
    seen=set()
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=set()
            while q:
                x,y=q.popleft(); cells.append((x,y))
                v=grid[x][y]
                if v not in (0,5): seeds.add(v)
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if len(seeds)==1:
                color=next(iter(seeds))
                for x,y in cells:
                    if out[x][y]==0:
                        out[x][y]=color
    return out
```

### M126 — Infer the panel transform and apply it to the query

**What it tests:** Use the first two panels as an explicit before→after example, infer the geometric transform, and apply it to the third panel.

**Staged hint:** Forget the separator color. Compare panel 1 to panel 2, identify which symmetry or rotation turns one into the other, then apply the same transform to panel 3.

**Train 1 — input**

```text
10005001150200
11005001050220
00005000050020
00005000050000
```

**Train 1 — output**

```text
0000
0022
0220
0000
```

**Train 2 — input**

```text
00035300054000
00335330054400
00035300050400
00005000050000
```

**Train 2 — output**

```text
0004
0044
0040
0000
```

**Test — input**

```text
70005770050600
77005077050660
07005000050060
00005000050000
```

**Test — output**

```text
0000
6600
0660
0000
```

**Written solution:** The first two panels explicitly show one geometric transform. Identify which symmetry or rotation changes panel 1 into panel 2, then apply that same transform to the query panel.

**Program solution**

```python
def solve_M126(grid):
    a,b,q=split_panel_row(grid,3,sep=5)
    _,f=infer_transform(a,b)
    return f(q)
```

## Hard

### H120 — Compose an inferred transform with an inferred recolor map

**What it tests:** Read geometry from one example pair, read a color permutation from another pair, and apply both to the query.

**Staged hint:** The first example pair tells you how the shape moves. The second pair tells you how colors rename while positions stay fixed. Apply the movement first, then recolor.

**Train 1 — input**

```text
230050222523005760052300
200050303520005700052030
233050300523305766050000
000050000500005000050000
```

**Train 1 — output**

```text
0077
0006
0060
0000
```

**Train 2 — input**

```text
230050032523005480050030
200050002520005400050230
233050332523305488050200
000050000500005000050000
```

**Train 2 — output**

```text
0800
0840
0040
0000
```

**Test — input**

```text
230052220523005940052000
200053030520005900052300
233050030523305944052030
000050000500005000050000
```

**Test — output**

```text
9990
0400
0040
0000
```

**Written solution:** Split the input into five panels. The first pair teaches the geometric transform, the second pair teaches a color mapping without moving cells, and the fifth panel is the query. Transform the query shape first, then rename its colors using the inferred mapping.

**Program solution**

```python
def solve_H120(grid):
    a,b,c,d,q=split_panel_row(grid,5,sep=5)
    _,f=infer_transform(a,b)
    # infer recolor map from c->d by position
    mapping={}
    h,w=dims(c)
    for r in range(h):
        for col in range(w):
            x,y=c[r][col],d[r][col]
            if x!=0 and y!=0:
                mapping[x]=y
    tq=f(q)
    out=clone(tq)
    h2,w2=dims(out)
    for r in range(h2):
        for c_ in range(w2):
            if out[r][c_]!=0:
                out[r][c_]=mapping.get(out[r][c_], out[r][c_])
    return out
```

### H121 — Infer the binary panel operation from an example

**What it tests:** Use one example triple to infer which binary operation combines two panels, then apply that operation to a new pair.

**Staged hint:** Compare the example operands to the example result. Decide which rule fits exactly, then run the same rule on the query operands.

**Train 1 — input**

```text
110050100510005220050030
010050110500105020050030
000050000500005000050000
000050000500005000050000
```

**Train 1 — output**

```text
2230
0230
0000
0000
```

**Train 2 — input**

```text
330050400539005700050600
030050440509405770050660
000050000500005000050000
000050000500005000050000
```

**Train 2 — output**

```text
7600
7960
0000
0000
```

**Test — input**

```text
220050200502005770050700
020050220502005070050770
000050000500005007050000
000050000500005000050000
```

**Test — output**

```text
0700
0700
0000
0000
```

**Written solution:** Use the example operands and result to determine which binary panel operation is in force. Once the example matches exactly one operation, run that same operation on the query operand pair to produce the output.

**Program solution**

```python
def solve_H121(grid):
    a,b,r,x,y = split_panel_row(grid,5,sep=5)
    chosen=None
    for name,f in OPS.items():
        if f(a,b)==r:
            chosen=f
            break
    assert chosen is not None
    return chosen(x,y)
```

### H122 — Transfer the added stencil cells to a new object

**What it tests:** Infer which bbox-relative cells were added in an example before→after pair and add those same relative cells to the query object.

**Staged hint:** Normalize the example object by its bounding box, compute which relative cells appear only after the edit, then stamp those relative additions onto the query object's bounding box.

**Train 1 — input**

```text
22005222056600
02005020050600
00005020050000
00005000050000
```

**Train 1 — output**

```text
6660
0600
0600
0000
```

**Train 2 — input**

```text
33005333057700
33005330057700
00005030050000
00005000050000
```

**Train 2 — output**

```text
7770
7700
0700
0000
```

**Test — input**

```text
44005444058800
04005040050800
00005040050000
00005000050000
```

**Test — output**

```text
8880
0800
0800
0000
```

**Written solution:** Normalize the example before/after object by its bounding box and compare them to find which relative cells were added. Then locate the query object's bounding box and add those same relative cells using the query's own color.

**Program solution**

```python
def solve_H122(grid):
    before,after,q = split_panel_row(grid,3,sep=5)
    # assume each panel has one colored object
    cb=[cells for color,cells in cc(before)][0]
    ca=[cells for color,cells in cc(after)][0]
    qb=[cells for color,cells in cc(q)][0]
    r0b,r1b,c0b,c1b=bbox(cb)
    r0a,r1a,c0a,c1a=bbox(ca)
    # additions relative to bbox, assuming after bbox same size or larger enough to contain before
    rel_before={(r-r0b,c-c0b) for r,c in cb}
    rel_after={(r-r0a,c-c0a) for r,c in ca}
    added=rel_after-rel_before
    qcolor=next(v for row in q for v in row if v!=0)
    r0q,r1q,c0q,c1q=bbox(qb)
    out=clone(q)
    for dr,dc in added:
        nr,nc=r0q+dr,c0q+dc
        if 0<=nr<len(out) and 0<=nc<len(out[0]):
            out[nr][nc]=qcolor
    return out
```

### H123 — Fill each room by nearest seed

**What it tests:** Inside each walled room, color every blank cell with the uniquely nearest seed color and leave ties blank.

**Staged hint:** Treat 5 as a wall. Work room by room. For each blank, compare distances to all seeds in that room; fill only when one seed is strictly closest.

**Train 1 — input**

```text
555555555
520000305
500000005
500000005
555555555
560000405
555555555
```

**Train 1 — output**

```text
555555555
522233335
522233335
522233335
555555555
566644445
555555555
```

**Train 2 — input**

```text
55555555555
52000000035
50000000005
50000070005
50000000005
55555555555
```

**Train 2 — output**

```text
55555555555
52222773335
52227777335
52277777735
52277777735
55555555555
```

**Test — input**

```text
555555555
530000205
500000005
500000005
555555555
540000605
555555555
```

**Test — output**

```text
555555555
533322225
533322225
533322225
555555555
544466665
555555555
```

**Written solution:** Inside each room separated by walls, compare every blank cell to all seeds in that same room. Fill a blank only if one seed is strictly closest by Manhattan distance within the room; if multiple seeds tie for closest, leave the blank as 0.

**Program solution**

```python
def solve_H123(grid):
    h,w=dims(grid)
    out=clone(grid)
    # find rooms of non-wall cells
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if not seeds:
                continue
            for x,y in cells:
                if grid[x][y]==0:
                    dists=[]
                    for sr,sc,col in seeds:
                        d=abs(sr-x)+abs(sc-y)  # same room, no walls inside component
                        dists.append((d,col))
                    mind=min(d for d,col in dists)
                    cols={col for d,col in dists if d==mind}
                    if len(cols)==1:
                        out[x][y]=next(iter(cols))
    return out
```

### H124 — Choose the matching prototype family under symmetry

**What it tests:** Match the query shape to one of several prototype panels up to rotation or reflection, then output that prototype in canonical orientation with the query color.

**Staged hint:** Ignore absolute position and orientation. Identify which library prototype is the same shape family as the query under any symmetry, then repaint that stored prototype with the query's color.

**Train 1 — input**

```text
1000511105110050007
1000501005011050077
1100501005001050770
0000500005000050000
```

**Train 1 — output**

```text
7700
0770
0070
0000
```

**Train 2 — input**

```text
1000511105110050004
1000501005011050004
1100501005001050044
0000500005000050000
```

**Train 2 — output**

```text
4000
4000
4400
0000
```

**Test — input**

```text
1000511105110050000
1000501005011058000
1100501005001058880
0000500005000058000
```

**Test — output**

```text
8880
0800
0800
0000
```

**Written solution:** Compare the query object against each library prototype up to rotation and reflection. Once you know which prototype family matches, output that stored canonical prototype repainted with the query color.

**Program solution**

```python
def solve_H124(grid):
    p1,p2,p3,q = split_panel_row(grid,4,sep=5)
    libs=[p1,p2,p3]
    qcells=[(r,c) for r,row in enumerate(q) for c,v in enumerate(row) if v!=0]
    qcolor=next(v for row in q for v in row if v!=0)
    qcanon=canonical_shape(q)
    chosen=None
    for lib in libs:
        # compare under symmetries
        for name,f in TRANSFORMS.items():
            if canonical_shape(f(lib))==qcanon:
                chosen=lib
                break
        if chosen is not None:
            break
    assert chosen is not None
    out=blank(*dims(chosen))
    for r,row in enumerate(chosen):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=qcolor
    return out
```

### H125 — Pack the object inventory by height

**What it tests:** Extract the body objects, normalize them, sort them by bounding-box height, recolor them with the palette, and pack them into a tight horizontal strip.

**Staged hint:** Ignore the palette row until the end. Normalize each component to its own top-left corner, sort by height descending, then lay the components out left-to-right with one blank column between them.

**Train 1 — input**

```text
246000000
080000880
080000880
080000000
000000000
000008880
000000000
```

**Train 1 — output**

```text
20440666
20440000
20000000
```

**Train 2 — input**

```text
3570000000
0090000000
0090007700
0090007700
0000007700
0000000000
0000000088
0000000000
```

**Train 2 — output**

```text
3305077
3305000
3305000
```

**Test — input**

```text
8640000000
0005500000
0005500000
0005500000
0000000000
0000007700
0000007000
0000000008
0000000000
```

**Test — output**

```text
8806604
8806000
8800000
```

**Written solution:** Ignore the palette row, extract each body object, and normalize it to its own top-left corner. Sort the normalized objects by bounding-box height from tallest to shortest, recolor them with the palette in that order, and pack them side by side with one blank column between neighbors.

**Program solution**

```python
def solve_H125(grid):
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body)
    # sort by bbox height descending, then width descending
    items=[]
    for color,cells in comps:
        r0,r1,c0,c1=bbox(cells)
        h=r1-r0+1; w=c1-c0+1
        shape=blank(h,w)
        for r,c in cells:
            shape[r-r0][c-c0]=1
        items.append((h,w,shape))
    items.sort(key=lambda t:(-t[0],-t[1]))
    heights=[h for h,w,shape in items]
    total_h=max(heights) if items else 1
    total_w=sum(t[1] for t in items)+max(0,len(items)-1)
    out=blank(total_h,total_w)
    cur=0
    for idx,(h,w,shape) in enumerate(items):
        color=palette[idx]
        for r in range(h):
            for c in range(w):
                if shape[r][c]:
                    out[r][cur+c]=color
        cur+=w+1
    return out
```

### H126 — Transform the second panel before merging

**What it tests:** Infer a transform from one panel pair, apply that transform to a second query panel, and then merge the transformed panel with the first query panel using conflict-aware overlay.

**Staged hint:** First infer the geometry change from panel A to panel B. Apply that same change to query panel Y. Then merge X with the transformed Y, letting mismatched overlaps become conflict color 9.

**Train 1 — input**

```text
1000500115220050030
1100500105020050030
0000500005000050000
0000500005000050000
```

**Train 1 — output**

```text
2200
0200
0033
0000
```

**Train 2 — input**

```text
0004500005700050600
0044500005770050660
0000500445000050000
0000500045000050000
```

**Train 2 — output**

```text
7000
7700
0660
0600
```

**Test — input**

```text
8000588005004057000
8800508805044057700
0800500005004050000
0000500005000050000
```

**Test — output**

```text
7740
0940
0040
0000
```

**Written solution:** The first pair of panels defines a geometric transform. Apply that transform to the second query panel, then overlay it onto the first query panel using conflict-aware merge: blanks pass through, equal colors stay, and mismatched nonzero overlaps become 9.

**Program solution**

```python
def solve_H126(grid):
    a,b,x,y = split_panel_row(grid,4,sep=5)
    _,f=infer_transform(a,b)
    ty=f(y)
    return merge_op(x,ty)
```
