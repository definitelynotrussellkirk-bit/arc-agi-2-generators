# 21 More ARC-Style Puzzles

This is the twentieth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E134–E140, M134–M140, H134–H140**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans more deliberately into **metadata dispatch, wall-cast shadows, panel analogies, bbox-relative edit transfer, family matching under symmetry, transform composition, and keyed prototype legends**.

**New motifs in this batch**

**`wall_shadow(shape, wall)`** — sweep every occupied cell straight toward a blocking wall of 8s and paint the full swept path. This is the main move in **M134**.

**`panel_analogy_apply(A, B, C)`** — infer a transform from panel A to panel B and then apply it to panel C. This is the core idea behind **M140**, and it becomes richer in **H134**, **H137**, and **H138**.

**`bbox_delta_transfer(before, after, query)`** — convert an edit into bbox-relative coordinates and replay that edit on a new object. This is the key abstraction in **H135**.

**`family_canonicalize(prototypes, query)`** — decide which prototype family a query belongs to up to symmetry, then emit the family’s canonical representative. This drives **H136**.

**`prototype_key_stamp(dictionary, seeds)`** — read a prototype legend from one region of the grid and stamp the matching prototype wherever its color key appears elsewhere. This is the central primitive in **H140**.


## Easy

### E134 — Legend row recolor mask

**What it tests:** Use a single legend color in the top row to recolor all mask cells in the body.


**Staged hint:** Ignore the exact position of the legend cell. First read its color, then apply it wherever the body contains 1.


**Train 1 — input**

```text
003000
010100
110001
001010
```

**Train 1 — output**

```text
000000
030300
330003
003030
```


**Train 2 — input**

```text
07000
10101
01000
11100
```

**Train 2 — output**

```text
00000
70707
07000
77700
```

**Test — input**

```text
000400
101010
010101
001000
```

**Test — output**

```text
000000
404040
040404
004000
```

**Written solution:** The top row contains one nonzero legend cell. Its value is the output color. Build a blank output grid of the same size, ignore the legend row itself, and replace every body cell equal to 1 with the legend color. Everything else becomes 0.


**Program solution**

```python
def solve_E134(grid):
    h,w=dims(grid)
    color=next(v for v in grid[0] if v!=0)
    out=blank(h,w)
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1:
                out[r][c]=color
    return out
```

### E135 — Fill vertical segments between matching endpoints

**What it tests:** Detect columns containing exactly two equal-colored endpoints and fill the interval between them.


**Staged hint:** Work column by column. When a column shows a clean pair of equal nonzero cells, that pair defines the segment.


**Train 1 — input**

```text
00300
20004
00300
00000
20004
00000
```

**Train 1 — output**

```text
00300
20304
20304
20004
20004
00000
```


**Train 2 — input**

```text
050006
000000
050000
000706
000000
000700
```

**Train 2 — output**

```text
050006
050006
050006
000706
000700
000700
```

**Test — input**

```text
00020
04000
00000
04000
00020
00000
```

**Test — output**

```text
00020
04020
04020
04020
00020
00000
```

**Written solution:** Treat each column independently. If a column contains exactly two nonzero cells and they have the same color, fill every cell from the upper endpoint down to the lower endpoint with that color. Leave all other cells unchanged.


**Program solution**

```python
def solve_E135(grid):
    out=clone(grid)
    h,w=dims(grid)
    for c in range(w):
        nz=[r for r in range(h) if grid[r][c]!=0]
        if len(nz)==2 and grid[nz[0]][c]==grid[nz[1]][c]:
            a,b=nz; color=grid[a][c]
            for r in range(a,b+1):
                out[r][c]=color
    return out
```

### E136 — Pack each row to the left

**What it tests:** Compress each row independently by preserving only the nonzero sequence and moving it to the left edge.


**Staged hint:** You do not need object structure here. Each row can be solved on its own by reading off the nonzero values in order.


**Train 1 — input**

```text
020300
400560
007089
```

**Train 1 — output**

```text
230000
456000
789000
```


**Train 2 — input**

```text
10203
00400
56070
08009
```

**Train 2 — output**

```text
12300
40000
56700
89000
```

**Test — input**

```text
040020
301005
000706
```

**Test — output**

```text
420000
315000
760000
```

**Written solution:** For every row, read the nonzero values from left to right, preserving their order. Write that sequence starting at the left edge of the output row and fill the remaining cells with 0. Rows do not interact with one another.


**Program solution**

```python
def solve_E136(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        vals=[v for v in grid[r] if v!=0]
        out[r][:len(vals)] = vals
    return out
```

### E137 — Reflect across a horizontal axis line

**What it tests:** Use a full row of 8s as a literal mirror axis and duplicate all colored cells across it.


**Staged hint:** The 8-row is not just decoration; it is the only row that stays fixed while everything else reflects through it.


**Train 1 — input**

```text
02000
02300
00300
88888
00000
00000
00000
```

**Train 1 — output**

```text
02000
02300
00300
88888
00300
02300
02000
```


**Train 2 — input**

```text
000000
000000
888888
044000
004050
000050
```

**Train 2 — output**

```text
004050
044000
888888
044000
004050
000050
```

**Test — input**

```text
006000
066070
888888
000000
000000
```

**Test — output**

```text
006000
066070
888888
066070
006000
```

**Written solution:** Find the row consisting entirely of 8s. Keep that axis row unchanged. For every other nonzero, non-8 cell, copy it to the mirror position on the opposite side of the axis while also preserving the original cell.


**Program solution**

```python
def solve_E137(grid):
    h,w=dims(grid)
    axis=None
    for r in range(h):
        if all(v==8 for v in grid[r]):
            axis=r; break
    out=blank(h,w)
    out[axis]=[8]*w
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v not in (0,8):
                out[r][c]=v
                rr=2*axis-r
                if 0<=rr<h:
                    out[rr][c]=v
    return out
```

### E138 — Expand seeds into pluses

**What it tests:** Turn each isolated seed cell into a cardinal plus centered on that seed.


**Staged hint:** Start from the center cell. Then add its four orthogonal neighbors if they lie inside the grid.


**Train 1 — input**

```text
0000000
0200030
0000000
0004000
0000000
```

**Train 1 — output**

```text
0200030
2220333
0204030
0044400
0004000
```


**Train 2 — input**

```text
00500
00000
60007
00000
00800
```

**Train 2 — output**

```text
05550
60507
66077
60807
08880
```

**Test — input**

```text
000000
040070
000000
006000
000000
```

**Test — output**

```text
040070
444777
046070
066600
006000
```

**Written solution:** Every nonzero cell acts as the center of a plus. Paint the center itself and the four cardinal neighbors with the same color, clipping naturally at the border if needed. The output is otherwise blank.


**Program solution**

```python
def solve_E138(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v!=0:
                for rr,cc_ in [(r,c),(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    if 0<=rr<h and 0<=cc_<w:
                        out[rr][cc_]=v
    return out
```

### E139 — Keep the majority color only

**What it tests:** Count all nonzero cells by color and preserve only the globally most frequent color.


**Staged hint:** Do not reason object by object. The deciding signal is the total color count across the whole grid.


**Train 1 — input**

```text
20302
02300
20030
02003
```

**Train 1 — output**

```text
20002
02000
20000
02000
```


**Train 2 — input**

```text
704070
074000
700400
070000
```

**Train 2 — output**

```text
700070
070000
700000
070000
```

**Test — input**

```text
506050
056050
500600
050000
```

**Test — output**

```text
500050
050050
500000
050000
```

**Written solution:** Count how many times each nonzero color appears in the input. Identify the unique majority color. Copy only cells of that color into the output and turn every other cell into 0.


**Program solution**

```python
def solve_E139(grid):
    counts={}
    for row in grid:
        for v in row:
            if v!=0:
                counts[v]=counts.get(v,0)+1
    major=max(counts, key=lambda k:(counts[k], -k))
    return [[v if v==major else 0 for v in row] for row in grid]
```

### E140 — Fill the center of 3×3 rings

**What it tests:** Detect hollow 3×3 same-colored rings and fill their missing center cell.


**Staged hint:** Look for a 3×3 window whose eight border cells are the same nonzero color while the middle is 0.


**Train 1 — input**

```text
0000000
0222000
0202033
0222030
0000033
```

**Train 1 — output**

```text
0000000
0222000
0222033
0222030
0000033
```


**Train 2 — input**

```text
444000
404055
444050
000055
```

**Train 2 — output**

```text
444000
444055
444050
000055
```

**Test — input**

```text
0066600
0060600
0066600
7770000
7070000
7770000
```

**Test — output**

```text
0066600
0066600
0066600
7770000
7770000
7770000
```

**Written solution:** Scan all 3×3 windows. Whenever the border of the window is a complete ring of one nonzero color and the center is 0, fill the center with that same color. Preserve the ring itself and leave unrelated shapes unchanged.


**Program solution**

```python
def solve_E140(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-2):
        for c in range(w-2):
            border=[grid[r][c],grid[r][c+1],grid[r][c+2],grid[r+1][c],grid[r+1][c+2],grid[r+2][c],grid[r+2][c+1],grid[r+2][c+2]]
            if border[0]!=0 and len(set(border))==1 and grid[r+1][c+1]==0:
                out[r+1][c+1]=border[0]
    return out
```


## Medium

### M134 — Cast a shadow to the wall

**What it tests:** Use a full 8-wall as a stopping boundary and sweep each object cell straight toward it.


**Staged hint:** First identify whether the wall is a full row or a full column. Then fill along the perpendicular direction until the wall.


**Train 1 — input**

```text
0000800
0200800
0230800
0030800
0000800
```

**Train 1 — output**

```text
0000800
0222800
0232800
0033800
0000800
```


**Train 2 — input**

```text
000000
040500
000500
888888
000000
000000
```

**Train 2 — output**

```text
000000
040500
040500
888888
000000
000000
```

**Test — input**

```text
080000
080060
080760
080700
080000
```

**Test — output**

```text
080000
086660
087760
087700
080000
```

**Written solution:** Find the full wall of 8s. Every nonzero, non-8 cell casts a straight shadow toward that wall. If the wall is vertical, fill horizontally from the cell to the square just before the wall; if the wall is horizontal, fill vertically instead. Preserve the wall and the original object.


**Program solution**

```python
def solve_M134(grid):
    h,w=dims(grid)
    out=clone(grid)
    # detect full wall row or col of 8s
    wall_row=next((r for r in range(h) if all(v==8 for v in grid[r])), None)
    wall_col=next((c for c in range(w) if all(grid[r][c]==8 for r in range(h))), None)
    if wall_col is not None:
        non8=[c for r in range(h) for c,v in enumerate(grid[r]) if v not in (0,8)]
        side='left' if non8 and max(non8)<wall_col else 'right'
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v not in (0,8):
                    if side=='left':
                        for cc_ in range(c, wall_col):
                            if out[r][cc_]==0: out[r][cc_]=v
                    else:
                        for cc_ in range(wall_col+1, c+1):
                            if out[r][cc_]==0: out[r][cc_]=v
    elif wall_row is not None:
        non8=[r for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
        side='top' if non8 and max(non8)<wall_row else 'bottom'
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v not in (0,8):
                    if side=='top':
                        for rr in range(r, wall_row):
                            if out[rr][c]==0: out[rr][c]=v
                    else:
                        for rr in range(wall_row+1, r+1):
                            if out[rr][c]==0: out[rr][c]=v
    return out
```

### M135 — Extract the interior of the frame

**What it tests:** Find the rectangular 8-frame and output only its interior contents, cropped tightly.


**Staged hint:** Ignore the outside background completely. The output is just the inside of the framed region, without the frame itself.


**Train 1 — input**

```text
0000000
0888880
0820380
0823380
0800380
0888880
0000000
```

**Train 1 — output**

```text
203
233
003
```


**Train 2 — input**

```text
88888
84008
84408
80408
88888
```

**Train 2 — output**

```text
400
440
040
```

**Test — input**

```text
0088880
0085080
0085680
0080680
0088880
```

**Test — output**

```text
50
56
06
```

**Written solution:** Locate the rectangle made of 8s. Remove the border and take only the cells strictly inside it. The output grid is the cropped interior region, so its size is the frame’s inner width and height.


**Program solution**

```python
def solve_M135(grid):
    # crop interior of the only 8-frame rectangle
    h,w=dims(grid)
    cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==8]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0+1:c1] for row in grid[r0+1:r1]]
```

### M136 — Repeat the prototype by the header count

**What it tests:** Read how many 1s appear in the header row and stamp that many horizontal copies of the prototype shape.


**Staged hint:** Separate the counting role of the header from the geometry of the lower prototype.


**Train 1 — input**

```text
1010100
0000000
0200000
0220000
```

**Train 1 — output**

```text
20020020
22022022
```


**Train 2 — input**

```text
010100
000000
033000
033000
```

**Train 2 — output**

```text
33033
33033
```

**Test — input**

```text
1010101
0000000
0444000
0040000
```

**Test — output**

```text
444044404440444
040004000400040
```

**Written solution:** Count the number of 1s in the top row. Below the header there is one prototype object. Crop that prototype to its bounding box and place exactly that many copies side by side in the output with one blank column between copies.


**Program solution**

```python
def solve_M136(grid):
    k=sum(1 for v in grid[0] if v==1)
    cells=[(r,c) for r in range(1,len(grid)) for c,v in enumerate(grid[r]) if v!=0]
    proto=crop_cells(grid,cells)
    ph,pw=dims(proto)
    out=blank(ph, k*pw+(k-1))
    x=0
    for i in range(k):
        for r in range(ph):
            for c in range(pw):
                out[r][x+c]=proto[r][c]
        x += pw
        if i<k-1: x += 1
    return out
```

### M137 — Use the left panel as a mask

**What it tests:** Interpret the left panel as a binary mask selecting cells from the colored right panel.


**Staged hint:** The separator just divides two roles: selector on the left, source colors on the right.


**Train 1 — input**

```text
101082233
011084455
110086677
```

**Train 1 — output**

```text
2030
0450
6600
```


**Train 2 — input**

```text
0108345
1108678
0018222
1018919
```

**Train 2 — output**

```text
040
670
002
909
```

**Test — input**

```text
100185522
110083344
011086776
001188118
```

**Test — output**

```text
5002
3300
0770
0018
```

**Written solution:** Split the input into two equal panels separated by a column of 8s. In the left panel, 1 means keep and 0 means discard. Apply that mask to the right panel cell by cell and output only the kept colors.


**Program solution**

```python
def solve_M137(grid):
    a,b=split_panels_row(grid,2,sep=8)
    h,w=dims(a)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if a[r][c]==1:
                out[r][c]=b[r][c]
    return out
```

### M138 — Reflect the shape through the anchor

**What it tests:** Use the single 9-cell as a point of symmetry and add the reflected copy of the shape.


**Staged hint:** Measure each colored cell as an offset from the anchor, then place the opposite offset as well.


**Train 1 — input**

```text
0000000
0220000
0200000
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0220000
0200000
0009000
0000020
0000220
0000000
```


**Train 2 — input**

```text
000000
000900
000040
000440
000400
000000
```

**Train 2 — output**

```text
004000
000900
000040
000440
000400
000000
```

**Test — input**

```text
0000000
0000000
0500000
0559000
0000000
0000000
0000000
```

**Test — output**

```text
0000000
0000000
0500000
0559550
0000050
0000000
0000000
```

**Written solution:** Find the anchor cell colored 9. For every other nonzero cell, compute its offset from the anchor and add a second copy at the opposite offset, provided that reflected position lies inside the grid. Keep the original shape and the anchor.


**Program solution**

```python
def solve_M138(grid):
    h,w=dims(grid)
    cells=[(r,c,v) for r in range(h) for c,v in enumerate(grid[r]) if v!=0]
    ar,ac = next((r,c) for r,c,v in cells if v==9)
    out=clone(grid)
    for r,c,v in cells:
        if v==9: continue
        rr,cc_=2*ar-r,2*ac-c
        if 0<=rr<h and 0<=cc_<w:
            out[rr][cc_]=v
    return out
```

### M139 — Sort components by area into a canonical row

**What it tests:** Extract connected components, crop them, sort them by size, and repack them in a standard left-to-right order.


**Staged hint:** First isolate the components. Then forget where they came from and only compare their areas.


**Train 1 — input**

```text
2200030
2000030
0004440
0000400
```

**Train 1 — output**

```text
44402203
04002003
```


**Train 2 — input**

```text
050066
055000
000070
000077
```

**Train 2 — output**

```text
50070066
55077000
```

**Test — input**

```text
8000990
8800090
0004400
0004000
```

**Test — output**

```text
44080099
40088009
```

**Written solution:** Find all connected nonzero components. Crop each one to its own bounding box. Sort the cropped components by descending area, breaking ties consistently, and place them left to right on a fresh canvas with one blank column between them, aligned at the top.


**Program solution**

```python
def solve_M139(grid):
    comps=[]
    for color,cells in cc(grid):
        comps.append((len(cells), color, crop_cells(grid,cells)))
    comps.sort(key=lambda t:(-t[0], t[1]))
    h=max(len(g) for _,_,g in comps)
    w=sum(len(g[0]) for _,_,g in comps)+(len(comps)-1)
    out=blank(h,w)
    x=0
    for _,_,g in comps:
        gh,gw=dims(g)
        for r in range(gh):
            for c in range(gw):
                out[r][x+c]=g[r][c]
        x += gw+1
    return out
```

### M140 — Infer the transform from the first two panels

**What it tests:** Read an example transform from panel A to panel B, then apply the same geometric transform to panel C.


**Staged hint:** Do not hard-code a specific transform. Compare the first two panels and let them tell you which symmetry or rotation is in play.


**Train 1 — input**

```text
20008002280300
22008022083300
02008000080000
00008000080000
```

**Train 1 — output**

```text
0030
0033
0000
0000
```


**Train 2 — input**

```text
04408044085000
00408040085500
00008000080000
00008000080000
```

**Train 2 — output**

```text
0005
0055
0000
0000
```

**Test — input**

```text
06008060087700
66008660080700
00008000080000
00008000080000
```

**Test — output**

```text
7700
0700
0000
0000
```

**Written solution:** Split the input into three equal square panels separated by 8-columns. Determine which geometric transform turns the first panel into the second. Then apply that same transform to the third panel to produce the output.


**Program solution**

```python
def solve_M140(grid):
    a,b,c = split_panels_row(grid,3,sep=8)
    name=infer_transform(a,b)
    return TRANSFORMS[name](c)
```


## Hard

### H134 — Infer transform and recolor jointly

**What it tests:** Infer both a geometric transform and a color mapping from the first panel pair, then apply both to the query panel.


**Staged hint:** You need two layers of alignment: shape alignment for the transform, and color alignment once the transformed support matches.


**Train 1 — input**

```text
20008005580200
23008077083200
03008000083000
00008000080000
```

**Train 1 — output**

```text
0770
0055
0000
0000
```


**Train 2 — input**

```text
04008000084400
46608000080600
00008199080600
00008010080000
```

**Train 2 — output**

```text
0000
0900
0900
1100
```

**Test — input**

```text
30508220080300
35508060085350
00008660080000
00008000080000
```

**Test — output**

```text
0600
2200
0600
0000
```

**Written solution:** Split the grid into three equal panels. Compare panel A with panel B. Find a geometric transform that aligns A to B, and from that aligned pair infer the consistent nonzero color mapping from A’s colors to B’s colors. Then transform panel C in the same way and recolor it using the learned mapping.


**Program solution**

```python
def solve_H134(grid):
    a,b,c = split_panels_row(grid,3,sep=8)
    for name,fn in TRANSFORMS.items():
        ta=fn(a)
        if dims(ta)!=dims(b): 
            continue
        mapping={}
        ok=True
        for r in range(len(ta)):
            for cc_ in range(len(ta[0])):
                va,vb=ta[r][cc_],b[r][cc_]
                if va==0 and vb==0:
                    continue
                if va==0 or vb==0:
                    ok=False; break
                if va in mapping and mapping[va]!=vb:
                    ok=False; break
                mapping[va]=vb
            if not ok: break
        if ok:
            return apply_recolor(fn(c), mapping)
    raise ValueError('no transform+recolor found')
```

### H135 — Transfer the learned edit delta

**What it tests:** Learn which bbox-relative cells were added in an example edit and add the same relative cells to a new object.


**Staged hint:** Focus on the difference between the first two panels, not on their absolute position in the larger panel.


**Train 1 — input**

```text
20082208500
22082208550
00080008000
```

**Train 1 — output**

```text
550
550
000
```


**Train 2 — input**

```text
03080308070
03080308070
03080338070
```

**Train 2 — output**

```text
070
070
077
```

**Test — input**

```text
44408444086660
04008444080600
00008000080000
00008000080000
```

**Test — output**

```text
6660
6660
0000
0000
```

**Written solution:** Treat the first panel as ‘before’ and the second as ‘after’. Compute the object’s bounding box in each, convert both supports to bbox-relative coordinates, and identify which relative cells were added. Then locate the query object’s bounding box and add those same relative cells to it using the query color.


**Program solution**

```python
def solve_H135(grid):
    before,after,query = split_panels_row(grid,3,sep=8)
    bcells=[(r,c) for r,row in enumerate(before) for c,v in enumerate(row) if v!=0]
    acells=[(r,c) for r,row in enumerate(after) for c,v in enumerate(row) if v!=0]
    qcells=[(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v!=0]
    br0,br1,bc0,bc1=bbox(bcells)
    ar0,ar1,ac0,ac1=bbox(acells)
    qr0,qr1,qc0,qc1=bbox(qcells)
    before_set={(r-br0,c-bc0) for r,c in bcells}
    after_set={(r-ar0,c-ac0) for r,c in acells}
    added=after_set-before_set
    out=clone(query)
    color=next(v for row in query for v in row if v!=0)
    for dr,dc in added:
        rr,cc_=qr0+dr,qc0+dc
        if 0<=rr<len(query) and 0<=cc_<len(query[0]):
            out[rr][cc_]=color
    return out
```

### H136 — Match a prototype family up to symmetry

**What it tests:** Choose which prototype the query belongs to under rotation or reflection, then emit the prototype’s canonical form in the query color.


**Staged hint:** Normalize the prototypes conceptually, but compare the query against all transformed versions of each family.


**Train 1 — input**

```text
20008030080066
22008333080060
00008000080000
00008000080000
```

**Train 1 — output**

```text
60
66
```


**Train 2 — input**

```text
44008050080070
04008555080777
00008050080070
00008000080000
```

**Train 2 — output**

```text
070
777
070
```

**Test — input**

```text
00808900080000
88808990080000
00008090080440
00008000084400
```

**Test — output**

```text
40
44
04
```

**Written solution:** The first two panels are prototype families in canonical orientation. The third panel is a transformed instance of one of those families in a new color. Compare the query against all symmetries of each prototype support, identify the matching family, and output that family’s canonical prototype recolored with the query’s color. The output is cropped to the prototype’s own bounding box.


**Program solution**

```python
def solve_H136(grid):
    p1,p2,q = split_panels_row(grid,3,sep=8)
    s1,_=normalize_support(p1)
    s2,_=normalize_support(p2)
    sq,qcolor=normalize_support(q)
    # compare query against transformed families
    for base in [s1,s2]:
        for name,fn in TRANSFORMS.items():
            if transform_support(base, fn)==sq:
                return apply_support(base,qcolor)
    raise ValueError('no family match')
```

### H137 — Infer a transform, then self-merge with conflicts

**What it tests:** Infer a transform from panels A and B, apply it to the query, and merge the original query with its transformed copy using 9 for overlaps.


**Staged hint:** The first step is analogy; the second is a nontrivial merge. Keep those two subproblems separate.


**Train 1 — input**

```text
20080028550
22080228500
00080008000
```

**Train 1 — output**

```text
595
505
000
```


**Train 2 — input**

```text
03080008770
33080338070
00080308000
```

**Train 2 — output**

```text
770
090
077
```

**Test — input**

```text
40084408060
44080408660
00080008000
```

**Test — output**

```text
090
990
000
```

**Written solution:** Determine which transform maps the first panel to the second. Apply that transform to the query panel. Merge the original query and the transformed copy cell by cell: if exactly one has a nonzero cell, keep that color; if both occupy the same position, write 9 there to mark the conflict.


**Program solution**

```python
def solve_H137(grid):
    a,b,q = split_panels_row(grid,3,sep=8)
    name=infer_transform(a,b)
    tq=TRANSFORMS[name](q)
    h,w=dims(q) if dims(q)==dims(tq) else dims(tq)
    # assume same dims due chosen transform on square panel
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            va=q[r][c]
            vb=tq[r][c]
            if va!=0 and vb!=0:
                out[r][c]=9
            else:
                out[r][c]=va or vb
    return out
```

### H138 — Infer a two-step transform chain

**What it tests:** Read one transform from A→B and a second from B→C, then compose them and apply the composition to the query.


**Staged hint:** Do not skip straight to a guessed final move. Identify the two transforms separately and then compose them.


**Train 1 — input**

```text
200800280008330
220802280208300
000800080228000
```

**Train 1 — output**

```text
000
003
033
```


**Train 2 — input**

```text
040804080008500
440844084408550
000800080408000
```

**Train 2 — output**

```text
000
050
550
```

**Test — input**

```text
660800080008070
060806080608770
000806686608000
```

**Test — output**

```text
000
770
070
```

**Written solution:** Split the input into four panels. Infer the transform that maps panel A to panel B, and the transform that maps panel B to panel C. Compose those two transforms in that order and apply the resulting two-step transform chain to the query panel.


**Program solution**

```python
def solve_H138(grid):
    a,b,c,q = split_panels_row(grid,4,sep=8)
    t1=infer_transform(a,b)
    t2=infer_transform(b,c)
    return TRANSFORMS[t2](TRANSFORMS[t1](q))
```

### H139 — Recolor components by area rank from a palette header

**What it tests:** Use the palette in the header row as an ordered rank list, then recolor components from largest to smallest.


**Staged hint:** The header colors are not object labels in the body; they are an ordered palette that should be assigned by size rank.


**Train 1 — input**

```text
234000
110010
100010
000111
000010
```

**Train 1 — output**

```text
330020
300020
000222
000020
```


**Train 2 — input**

```text
56780
10011
11000
00111
00010
```

**Train 2 — output**

```text
60077
66000
00555
00050
```

**Test — input**

```text
429000
111010
010010
000010
110000
```

**Test — output**

```text
444020
040020
000020
990000
```

**Written solution:** Ignore the top row when finding components; it only supplies the palette order. In the body, find all connected components, rank them by descending area, and recolor the largest component with the first palette color, the next largest with the second palette color, and so on while preserving each component’s position and shape.


**Program solution**

```python
def solve_H139(grid):
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=[(len(cells), idx, cells) for idx,(color,cells) in enumerate(cc(body, ignore=(0,), same_color=True))]
    comps.sort(key=lambda t:(-t[0], t[1]))
    out=blank(len(body), len(body[0]))
    for i,(_,_,cells) in enumerate(comps):
        color=palette[i]
        for r,c in cells:
            out[r][c]=color
    return out
```

### H140 — Stamp keyed prototypes from an in-grid legend

**What it tests:** Read a miniature prototype dictionary from the top band and stamp the matching prototype wherever its color key appears below.


**Staged hint:** Treat the top band as a lookup table. Each body seed chooses a prototype by color and places it centered on that seed.


**Train 1 — input**

```text
02083008444
22283308040
02080008000
88888888888
00000000000
02000030000
00000000000
00004000000
00000000000
```

**Train 1 — output**

```text
02000300000
22200330000
02044400000
00004000000
00000000000
```


**Train 2 — input**

```text
02083008444
22283308040
02080008000
88888888888
00300000000
00000000000
40000020000
00000000000
00000300000
```

**Train 2 — output**

```text
03300000000
44000020000
40000222000
00003020000
00003300000
```

**Test — input**

```text
02083008444
22283308040
02080008000
88888888888
00020000000
00000030000
00000000000
04000002000
00003000000
```

**Test — output**

```text
00222300000
00020330000
44400002000
04030022200
00033002000
```

**Written solution:** The top three rows contain three miniature prototypes separated by 8-columns, and the next row is just a separator. Each prototype’s nonzero color is also its key. In the body, every nonzero singleton chooses the prototype of the same color. Stamp that prototype centered on the singleton’s position using the same color.


**Program solution**

```python
def solve_H140(grid):
    top=grid[:3]
    body=[row[:] for row in grid[4:]]  # row 3 is all 8 separator
    p1,p2,p3 = split_panels_row(top,3,sep=8)
    protos={}
    for p in [p1,p2,p3]:
        color=next(v for row in p for v in row if v!=0)
        supp,_=normalize_support(p)
        # anchor at center of 3x3
        rel=[(r-1,c-1) for r,c in supp]
        protos[color]=rel
    h,w=dims(body)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(body[r]):
            if v!=0:
                for dr,dc in protos[v]:
                    rr,cc_=r+dr,c+dc
                    if 0<=rr<h and 0<=cc_<w:
                        out[rr][cc_]=v
    return out
```
