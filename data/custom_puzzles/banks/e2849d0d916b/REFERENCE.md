# 21 More ARC-Style Puzzles

This is the seventeenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E113–E119, M113–M119, H113–H119**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into symbolic legends, local symmetry, anchor-based stamping, panel voting, bbox-relative edit transfer, conflict-aware panel merging, geodesic seed filling, prototype family matching, and transform composition.

**New motifs in this batch**

**`legend_strip_recolor(source_row, target_row, body)`** — read a compact source→target mapping from two legend rows and recolor the body accordingly. This is the key move in **M113**.

**`anchor_stamp(prototype_with_anchor, target_markers)`** — use an anchor cell embedded in a prototype object to stamp translated copies at every standalone anchor target. This drives **M116**.

**`panel_majority_vote(p1, p2, p3)`** — keep a cell when at least two panels agree that something nonzero is present there, using the majority color at that position. This powers **M117**.

**`cutout_stencil_transfer(example_before, example_after, query)`** — infer which bbox-relative cells were removed in an example and remove those same relative cells from a new object. This is the core abstraction in **H115**.

**`conflict_merge(a, b)`** — merge two panels cellwise so that blanks pass through, equal colors stay stable, and mismatched nonzero overlaps collapse to a special conflict color. This appears in **H116**.

**`compose_inferred_transforms(a, b, c, d, q)`** — infer one transform from the first example pair, a second transform from another example pair, then compose them on a query panel. This is the central move in **H119**.

## Easy

### E113 — Fill the horizontal bridge

**What it tests:** Detect same-color endpoints on a row and fill the zero cells between them.

**Staged hint:** Group cells by color. If a color appears exactly twice in one row with only 0s between them, paint the whole segment.

**Train 1 — input**

```text
0000000
2000002
0000000
0004004
0000000
```

**Train 1 — output**

```text
0000000
2222222
0000000
0004444
0000000
```

**Train 2 — input**

```text
00000000
00000000
03000300
00000000
00000000
00600060
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
03333300
00000000
00000000
00666660
00000000
00000000
```

**Test — input**

```text
000000000
700000007
000000000
000500005
000000000
```

**Test — output**

```text
000000000
777777777
000000000
000555555
000000000
```

**Written solution:** For each color, look for the case where it appears exactly twice in one row and every cell between those two endpoints is 0. Fill the entire horizontal segment between the endpoints with that color and leave all other cells unchanged.

**Program solution**

```python
def solve_E113(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][0]==cells[1][0]:
            r=cells[0][0]
            a,b=sorted([cells[0][1],cells[1][1]])
            if all(grid[r][c]==0 for c in range(a+1,b)):
                for c in range(a,b+1):
                    out[r][c]=color
    return out
```

### E114 — Fill the diagonal bridge

**What it tests:** Detect same-color endpoints on a down-right diagonal and fill the missing diagonal cells.

**Staged hint:** Look for a color that appears twice with equal row and column offsets. If the cells between them on that diagonal are 0, fill them.

**Train 1 — input**

```text
200000
000000
000000
000200
000000
000000
```

**Train 1 — output**

```text
200000
020000
002000
000200
000000
000000
```

**Train 2 — input**

```text
0000000
0700000
0000000
0000000
0000700
0000000
0000000
```

**Train 2 — output**

```text
0000000
0700000
0070000
0007000
0000700
0000000
0000000
```

**Test — input**

```text
0000000
0000000
3000000
0000000
0000000
0000000
0000300
```

**Test — output**

```text
0000000
0000000
3000000
0300000
0030000
0003000
0000300
```

**Written solution:** For each color, detect whether its two occurrences lie on the same down-right diagonal. If they do and all intervening cells on that diagonal are 0, fill the whole diagonal segment between them with that color.

**Program solution**

```python
def solve_E114(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if dr==dc and dr!=0:
                step=1 if dr>0 else -1
                if all(grid[r1+i*step][c1+i*step]==0 for i in range(1,abs(dr))):
                    for i in range(abs(dr)+1):
                        out[r1+i*step][c1+i*step]=color
    return out
```

### E115 — Complete the 2x2 square

**What it tests:** Recognize an L-shape that almost forms a 2x2 monochrome square and fill the missing corner.

**Staged hint:** Scan every 2x2 window. If exactly three cells are the same nonzero color and the fourth is 0, fill the 0 with that color.

**Train 1 — input**

```text
0000000
0220000
0200000
0003300
0003030
0000000
```

**Train 1 — output**

```text
0000000
0220000
0220000
0003300
0003330
0000000
```

**Train 2 — input**

```text
00000000
00440000
00040000
00000000
00000060
00000066
00000000
```

**Train 2 — output**

```text
00000000
00440000
00440000
00000000
00000066
00000066
00000000
```

**Test — input**

```text
0000000
0770000
0700000
0000000
0003300
0003000
0000000
```

**Test — output**

```text
0000000
0770000
0770000
0000000
0003300
0003300
0000000
```

**Written solution:** Scan every 2x2 window in the original grid. Whenever three cells in that window share the same nonzero color and the fourth is empty, fill the empty corner with that same color.

**Program solution**

```python
def solve_E115(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                color=nz[0]
                idx=vals.index(0)
                rr=r+(idx//2); cc_=c+(idx%2)
                out[rr][cc_]=color
    return out
```

### E116 — Keep only border-touching objects

**What it tests:** Connected-component reasoning and filtering by contact with the grid frame.

**Staged hint:** Treat each monochrome component as an object. Preserve it only if at least one of its cells touches the outer border.

**Train 1 — input**

```text
2200000
2200000
0003000
0003300
0000000
0000004
0000004
```

**Train 1 — output**

```text
2200000
2200000
0000000
0000000
0000000
0000004
0000004
```

**Train 2 — input**

```text
00000000
00000000
06600000
06600000
00000055
00000055
00077000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00000000
00000055
00000055
00000000
00000000
```

**Test — input**

```text
00004400
00004400
00000000
00222000
00000000
70000000
70000000
00000000
```

**Test — output**

```text
00004400
00004400
00000000
00000000
00000000
70000000
70000000
00000000
```

**Written solution:** Treat every monochrome connected component as an object. Keep an object only if at least one of its cells touches the outer frame of the grid; erase all objects that are entirely interior.

**Program solution**

```python
def solve_E116(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out
```

### E117 — Fill the orthogonal cavity

**What it tests:** Local cavity detection using the four cardinal neighbors.

**Staged hint:** A 0 cell should change only if its up, down, left, and right neighbors are all the same nonzero color.

**Train 1 — input**

```text
0000000
0020000
0222000
0020000
0000000
0003300
0030300
0003300
```

**Train 1 — output**

```text
0000000
0020000
0222000
0020000
0000000
0003300
0033300
0003300
```

**Train 2 — input**

```text
00000000
00044000
00404000
00044000
00000000
00666000
00606000
00666000
```

**Train 2 — output**

```text
00000000
00044000
00444000
00044000
00000000
00666000
00666000
00666000
```

**Test — input**

```text
0000000
0077700
0070700
0077700
0000000
0002200
0020200
0002200
```

**Test — output**

```text
0000000
0077700
0077700
0077700
0000000
0002200
0022200
0002200
```

**Written solution:** Check each 0 cell that has four cardinal neighbors. If its up, down, left, and right neighbors are all the same nonzero color, change that center cell to that color; otherwise leave it alone.

**Program solution**

```python
def solve_E117(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if grid[r][c]==0:
                ns=[grid[r-1][c],grid[r+1][c],grid[r][c-1],grid[r][c+1]]
                if ns[0]!=0 and ns.count(ns[0])==4:
                    out[r][c]=ns[0]
    return out
```

### E118 — Mirror across the divider bar

**What it tests:** Reflection around a full-height divider column.

**Staged hint:** Find the solid vertical bar. Every non-divider cell should also appear at the mirrored column on the other side.

**Train 1 — input**

```text
000500000
022500000
020500000
022500000
000500000
```

**Train 1 — output**

```text
000500000
022522000
020502000
022522000
000500000
```

**Train 2 — input**

```text
000050000
000050330
000050030
000050330
000050000
```

**Train 2 — output**

```text
000050000
033050330
030050030
033050330
000050000
```

**Test — input**

```text
0000050000
0000050000
0770050000
0700050000
0770050000
0000050000
```

**Test — output**

```text
0000050000
0000050000
0770050077
0700050007
0770050077
0000050000
```

**Written solution:** Find the full-height divider bar. Every non-divider colored cell should also appear at the reflected column across that bar, so copy the object by mirror symmetry while keeping the original and the divider unchanged.

**Program solution**

```python
def solve_E118(grid):
    h,w=dims(grid)
    out=clone(grid)
    # full-height single-color divider column (all same nonzero)
    divider=None
    dcolor=None
    for c in range(w):
        col=[grid[r][c] for r in range(h)]
        if col[0]!=0 and all(v==col[0] for v in col):
            divider=c; dcolor=col[0]; break
    assert divider is not None
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and c!=divider and v!=dcolor:
                mc=2*divider-c
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=v
    return out
```

### E119 — Mark the midpoint

**What it tests:** Infer the midpoint of a horizontal or vertical same-color pair.

**Staged hint:** For each color that appears exactly twice in one row or one column, place the same color at the midpoint if that cell is 0.

**Train 1 — input**

```text
0000000
2000200
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
2020200
0000000
0000000
0000000
```

**Train 2 — input**

```text
000000
000300
000000
000000
000000
000300
000000
```

**Train 2 — output**

```text
000000
000300
000000
000300
000000
000300
000000
```

**Test — input**

```text
0000000
0000000
0060006
0000000
0000000
0000000
0000000
```

**Test — output**

```text
0000000
0000000
0060606
0000000
0000000
0000000
0000000
```

**Written solution:** For each color that appears exactly twice in a single row or a single column, compute the midpoint between the two cells. If that midpoint cell is empty, fill it with the same color.

**Program solution**

```python
def solve_E119(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2 and (c1+c2)%2==0:
                m=(c1+c2)//2
                if grid[r1][m]==0:
                    out[r1][m]=color
            elif c1==c2 and (r1+r2)%2==0:
                m=(r1+r2)//2
                if grid[m][c1]==0:
                    out[m][c1]=color
    return out
```


## Medium

### M113 — Recolor from the legend strip

**What it tests:** Symbolic color remapping from a compact legend embedded in the grid.

**Staged hint:** Read row 0 as source colors and row 1 as destination colors in the same columns. Then recolor matching body cells below.

**Train 1 — input**

```text
02040000
08070000
00000000
00220000
00040000
00000440
00000000
```

**Train 1 — output**

```text
02040000
08070000
00000000
00880000
00070000
00000770
00000000
```

**Train 2 — input**

```text
00300700
00600100
00000000
03000070
00330000
00000700
00000000
```

**Train 2 — output**

```text
00300700
00600100
00000000
06000010
00660000
00000100
00000000
```

**Test — input**

```text
09000600
02000400
00000000
00990000
00000660
00000009
00000000
```

**Test — output**

```text
09000600
02000400
00000000
00220000
00000440
00000002
00000000
```

**Written solution:** Read the first two rows as a legend: whenever a column has a nonzero in both row 0 and row 1, the top color maps to the bottom color. Apply that color remapping to the rows below while leaving the legend rows unchanged.

**Program solution**

```python
def solve_M113(grid):
    out=clone(grid)
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        s=grid[0][c]
        t=grid[1][c]
        if s!=0 and t!=0:
            mapping[s]=t
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out
```

### M114 — Stamp the prototype into the frames

**What it tests:** Extract a prototype object, detect empty frames, and place copies inside matching interiors.

**Staged hint:** The non-5 object is the prototype. Each 5 rectangle is a frame; copy the prototype into any frame whose interior size matches the prototype bbox.

**Train 1 — input**

```text
2200000000
0200005555
0000005005
0000005005
0000005555
0000000000
```

**Train 1 — output**

```text
2200000000
0200005555
0000005225
0000005025
0000005555
0000000000
```

**Train 2 — input**

```text
77000000000000
70000055550000
00000050050000
00000050050000
00000055550000
00000000005555
00000000005005
00000000005005
00000000005555
```

**Train 2 — output**

```text
77000000000000
70000055550000
00000057750000
00000057050000
00000055550000
00000000005555
00000000005775
00000000005705
00000000005555
```

**Test — input**

```text
44000000000000
40000055550000
00000050050000
00000050050000
00000055550000
00000000005555
00000000005005
00000000005005
00000000005555
```

**Test — output**

```text
44000000000000
40000055550000
00000054450000
00000054050000
00000055550000
00000000005555
00000000005445
00000000005405
00000000005555
```

**Written solution:** The only non-5 object is the prototype. Find every hollow rectangular frame made of 5s whose interior size matches the prototype’s bounding box, and stamp a copy of the prototype into that interior at the same relative shape positions.

**Program solution**

```python
def solve_M114(grid):
    out=clone(grid)
    comps=cc(grid)
    proto=None
    for color,cells in comps:
        if color!=5:
            proto=(color,cells)
            break
    assert proto
    pcolor,pcells=proto
    pr0,pr1,pc0,pc1=bbox(pcells)
    shape=[(r-pr0,c-pc0) for r,c in pcells]
    ph,pw=pr1-pr0+1,pc1-pc0+1
    for r0,r1,c0,c1 in find_rect_frames(grid,5):
        ih,iw=(r1-r0-1),(c1-c0-1)
        if ih==ph and iw==pw:
            for dr,dc in shape:
                out[r0+1+dr][c0+1+dc]=pcolor
    return out
```

### M115 — Recolor by border contact

**What it tests:** Classify objects by which side of the outer border they touch.

**Staged hint:** Find each object, ask whether it touches the top, bottom, left, right, or no border, then recolor by that class.

**Train 1 — input**

```text
00022000
00002000
70033000
70003090
00000099
00000000
```

**Train 1 — output**

```text
00022000
00002000
40088000
40008060
00000066
00000000
```

**Train 2 — input**

```text
00000000
00440000
00000000
00077000
00077000
00000006
00330006
```

**Train 2 — output**

```text
00000000
00880000
00000000
00088000
00088000
00000003
00330003
```

**Test — input**

```text
00000000
00000077
00000007
22000000
02003300
00003300
00000000
00000099
```

**Test — output**

```text
00000000
00000066
00000006
44000000
04008800
00008800
00000000
00000033
```

**Written solution:** Find each connected object and determine which outer border it touches. Recolor top-touching objects to 2, bottom-touching objects to 3, left-touching objects to 4, right-touching objects to 6, and fully interior objects to 8.

**Program solution**

```python
def solve_M115(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        touches=set()
        for r,c in cells:
            if r==0: touches.add('top')
            if r==h-1: touches.add('bottom')
            if c==0: touches.add('left')
            if c==w-1: touches.add('right')
        if 'top' in touches:
            new=2
        elif 'bottom' in touches:
            new=3
        elif 'left' in touches:
            new=4
        elif 'right' in touches:
            new=6
        else:
            new=8
        for r,c in cells:
            out[r][c]=new
    return out
```

### M116 — Anchor-based stamping

**What it tests:** Use an anchor cell inside a prototype object to stamp translated copies at target anchor markers.

**Staged hint:** Find the connected object that contains an 8. Standalone 8s are destinations; copy the whole anchored shape so its 8 lands on each one.

**Train 1 — input**

```text
000000000
082200000
002000800
000000000
000000000
```

**Train 1 — output**

```text
000000000
082200000
002000822
000000020
000000000
```

**Train 2 — input**

```text
0000000000
0060000000
0686000008
0060000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0060000006
0686000068
0060000006
0000000000
0000000000
```

**Test — input**

```text
000000000000
044000000000
084400008000
000000000000
000000800000
000000000000
```

**Test — output**

```text
000000000000
044000004400
084400008440
000000440000
000000844000
000000000000
```

**Written solution:** Locate the connected prototype that contains an anchor cell 8. Any isolated 8 elsewhere is a destination marker; copy the entire anchored object so that its anchor lands on each destination marker, while preserving the original prototype as well.

**Program solution**

```python
def solve_M116(grid):
    out=clone(grid)
    comps=cc_any(grid)
    proto_cells=None
    anchor=None
    targets=[]
    for _,cells in comps:
        colors=[grid[r][c] for r,c in cells]
        if 8 in colors and len(cells)>1:
            proto_cells=cells
            anchor=[(r,c) for r,c in cells if grid[r][c]==8][0]
        elif len(cells)==1 and grid[cells[0][0]][cells[0][1]]==8:
            targets.append(cells[0])
    assert proto_cells is not None
    rel=[(r-anchor[0], c-anchor[1], grid[r][c]) for r,c in proto_cells]
    h,w=dims(grid)
    for tr,tc in targets:
        for dr,dc,val in rel:
            nr,nc=tr+dr,tc+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=val
    return out
```

### M117 — Majority overlay from three panels

**What it tests:** Panel decomposition and cellwise majority voting over occupancy/color.

**Staged hint:** Split the input into three equal panels. A cell survives in the output when at least two panels have a nonzero there.

**Train 1 — input**

```text
02050005020
00050205020
20052005000
```

**Train 1 — output**

```text
020
020
200
```

**Train 2 — input**

```text
30005300050000
03005000050300
00005003050030
00035000050003
```

**Train 2 — output**

```text
3000
0300
0030
0003
```

**Test — input**

```text
04005040050000
00405000050040
00005000450004
40005400050000
```

**Test — output**

```text
0400
0040
0004
4000
```

**Written solution:** Split the input into three equal panels. For each cell position, if at least two panels contain a nonzero there, keep that position in the output and use the majority nonzero color at that cell; otherwise leave it 0.

**Program solution**

```python
def solve_M117(grid):
    panels=split_panel_row(grid,3,sep=5)
    h,w=dims(panels[0])
    out=blank(h,w)
    # choose majority of occupancy; color = max nonzero among occupied? maybe fixed 2 if occupied.
    # Use dominant nonzero color among panels if >=2 nonzero and same? To keep simple use color from nonzero cells if at least two agree or one nonzero repeated.
    for r in range(h):
        for c in range(w):
            vals=[p[r][c] for p in panels]
            nz=[v for v in vals if v!=0]
            if len(nz)>=2:
                # choose most common nonzero color
                counts=defaultdict(int)
                for v in nz: counts[v]+=1
                v=max(counts, key=lambda k:(counts[k], k))
                out[r][c]=v
    return out
```

### M118 — Crop, sort, and pack

**What it tests:** Object extraction, bbox cropping, area ranking, and output-size change.

**Staged hint:** Crop each object to its tight bounding box, sort objects by area from largest to smallest, then pack them side by side with one empty column between.

**Train 1 — input**

```text
00000000
02200000
02000000
00000000
00033000
00030000
00030000
00000000
```

**Train 1 — output**

```text
33022
30020
30000
```

**Train 2 — input**

```text
000000000
044000000
040000660
000000060
000000060
000000000
```

**Train 2 — output**

```text
66044
06040
06000
```

**Test — input**

```text
0000000000
0770000000
0700000000
0000002200
0000000200
0000000200
0000000000
```

**Test — output**

```text
22077
02070
02000
```

**Written solution:** Extract each connected object, crop it to its tight bounding box, and sort the cropped objects by area from largest to smallest. Build a new minimal output canvas by packing those cropped objects side by side with one empty column between neighbors.

**Program solution**

```python
def solve_M118(grid):
    comps=cc(grid)
    items=[]
    for idx,(color,cells) in enumerate(comps):
        shape,(h,w)=normalize_shape(cells)
        items.append((len(cells), idx, color, shape, h, w))
    items.sort(key=lambda x:(-x[0], x[1]))
    H=max(h for _,_,_,_,h,w in items) if items else 0
    W=sum(w for _,_,_,_,h,w in items)+max(0,len(items)-1)
    out=blank(H,W)
    x=0
    for area,idx,color,shape,h,w in items:
        for r,c in shape:
            out[r][x+c]=color
        x+=w+1
    return out
```

### M119 — Choose the panel with the most query color

**What it tests:** Read a query color from a control panel, then compare candidate panels by count.

**Staged hint:** The first panel only tells you the target color. Among the other panels, return the one that contains the most cells of that color.

**Train 1 — input**

```text
200502052005000
000500052005000
000522050005002
```

**Train 1 — output**

```text
020
000
220
```

**Train 2 — input**

```text
040540050405000
000504054045040
000500050405000
```

**Train 2 — output**

```text
040
404
040
```

**Test — input**

```text
000570050705000
070507057075007
000500750705000
```

**Test — output**

```text
070
707
070
```

**Written solution:** The first panel only specifies the query color. Count how many cells of that color appear in each of the remaining candidate panels, and return the panel with the largest count.

**Program solution**

```python
def solve_M119(grid):
    panels=split_panel_row(grid,4,sep=5)
    qpanel=panels[0]
    q=None
    for row in qpanel:
        for v in row:
            if v!=0:
                q=v; break
        if q is not None: break
    assert q is not None
    best=max(panels[1:], key=lambda p: sum(v==q for row in p for v in row))
    return best
```


## Hard

### H113 — Infer the panel transform

**What it tests:** Recover a dihedral transform from an example pair and apply it to a new panel in the same input.

**Staged hint:** Split the input into three panels. Find which rotation or reflection turns panel 1 into panel 2, then use that same transform on panel 3.

**Train 1 — input**

```text
20050225030
22050205033
00050005000
```

**Train 1 — output**

```text
000
033
030
```

**Train 2 — input**

```text
44005004450030
04005004050330
04405044050030
00005000050000
```

**Train 2 — output**

```text
0300
0330
0300
0000
```

**Test — input**

```text
60005660050070
66005066050770
06005000050000
00005000050000
```

**Test — output**

```text
0000
0700
7700
0000
```

**Written solution:** Split the input into three panels A, B, and C. Determine which rotation or reflection transforms A into B, then apply exactly that same dihedral transform to C to get the output.

**Program solution**

```python
def solve_H113(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    _,f = infer_transform(a,b)
    return f(c)
```

### H114 — Infer the color remap

**What it tests:** Infer a position-preserving color permutation from an example panel pair and apply it to a query panel.

**Staged hint:** Panel 1 and panel 2 have the same shapes in the same places. Use their aligned cells to read the color mapping, then recolor panel 3.

**Train 1 — input**

```text
22005770050022
03005040053000
00305004050300
00005000050000
```

**Train 1 — output**

```text
0077
4000
0400
0000
```

**Train 2 — input**

```text
60045100854600
06005010050060
00045000854000
00005000050000
```

**Train 2 — output**

```text
8100
0010
8000
0000
```

**Test — input**

```text
22075990357022
02005090050002
70005300050700
00005000050000
```

**Test — output**

```text
3099
0009
0300
0000
```

**Written solution:** Panels 1 and 2 show the same occupied positions but with recolored cells. Use aligned positions to infer the color mapping from panel 1 to panel 2, then apply that mapping to every nonzero cell of panel 3.

**Program solution**

```python
def solve_H114(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    mapping={}
    h,w=dims(a)
    for r in range(h):
        for col in range(w):
            va,vb=a[r][col],b[r][col]
            if va!=0:
                mapping[va]=vb
    out=clone(c)
    for r in range(h):
        for col in range(w):
            v=c[r][col]
            if v in mapping:
                out[r][col]=mapping[v]
    return out
```

### H115 — Replay the cutout pattern

**What it tests:** Transfer a removal stencil from one object to another using relative bbox coordinates.

**Staged hint:** Compare panel 1 and panel 2 to see which occupied cells were removed. Remove cells in those same bbox-relative positions from panel 3.

**Train 1 — input**

```text
22252205777
22252025777
22252225777
```

**Train 1 — output**

```text
770
707
777
```

**Train 2 — input**

```text
44445404456666
44445444456666
44445444056666
44445444456666
```

**Train 2 — output**

```text
6066
6666
6660
6666
```

**Test — input**

```text
33335330357777
33335333357777
33335333357777
33335033357777
```

**Test — output**

```text
7707
7777
7777
0777
```

**Written solution:** Compare the first two panels to see which occupied cells were removed from the example object. Record those removals relative to the example object’s bounding box, then remove cells in the same bbox-relative positions from the query object in panel 3.

**Program solution**

```python
def solve_H115(grid):
    a,b,c = split_panel_row(grid,3,sep=5)
    # compute removed cells relative to bbox of nonzero in a
    cells_a=[(r,col) for r,row in enumerate(a) for col,v in enumerate(row) if v!=0]
    cells_b={(r,col) for r,row in enumerate(b) for col,v in enumerate(row) if v!=0}
    ar0,ar1,ac0,ac1=bbox(cells_a)
    removed=[]
    for r,col in cells_a:
        if (r,col) not in cells_b:
            removed.append((r-ar0, col-ac0))
    out=clone(c)
    cells_c=[(r,col) for r,row in enumerate(c) for col,v in enumerate(row) if v!=0]
    cr0,cr1,cc0,cc1=bbox(cells_c)
    for dr,dc in removed:
        rr,cc_=cr0+dr, cc0+dc
        if 0<=rr<len(out) and 0<=cc_<len(out[0]):
            out[rr][cc_]=0
    return out
```

### H116 — Merge with a conflict color

**What it tests:** Apply a cellwise merge rule where clashes between different nonzero colors become a special color.

**Staged hint:** Use the example triple to infer the merge rule: blank passes through, agreement stays, and conflicting nonzero colors collapse to one special conflict color.

**Train 1 — input**

```text
2005000520054005000
0205030509050405060
0005003500350045600
```

**Train 1 — output**

```text
400
090
604
```

**Train 2 — input**

```text
070050700507005003350003
007050008500785030050300
000050000500005000053000
000050000500005000050000
```

**Train 2 — output**

```text
0033
0300
3000
0000
```

**Test — input**

```text
220050200522005004450400
020052000522005040054000
000050000500005000050000
000050000500005000050000
```

**Test — output**

```text
0444
4400
0000
0000
```

**Written solution:** Combine two panels cell by cell using the rule illustrated by the example triple: blank values pass through, equal nonzero colors stay as they are, and conflicting different nonzero colors become the special conflict color 9. Apply that same merge rule to the query pair.

**Program solution**

```python
def solve_H116(grid):
    a,b,ex,d,e = split_panel_row(grid,5,sep=5)
    # could verify ex equals merge_op(a,b)
    return merge_op(d,e)
```

### H117 — Geodesic nearest-seed fill with ties

**What it tests:** Flood fill over free space while respecting walls and resolving distance ties separately.

**Staged hint:** Treat each non-wall nonzero cell as a seed. Fill every reachable empty cell with the nearest seed color, but use a tie color when distances match.

**Train 1 — input**

```text
5555555
5200005
5000005
5000035
5555555
```

**Train 1 — output**

```text
5555555
5222835
5228335
5283335
5555555
```

**Train 2 — input**

```text
55555555
54000565
50000505
50000505
55555555
```

**Train 2 — output**

```text
55555555
54444565
54444565
54444565
55555555
```

**Test — input**

```text
555555555
520000005
500000005
500000305
500000005
555555555
```

**Test — output**

```text
555555555
522223335
522233335
522333335
522333335
555555555
```

**Written solution:** Treat 5 as walls and every other nonzero cell as a seed. For each open cell, compute the shortest path distance through non-wall cells to every seed; fill with the nearest seed’s color, and use color 8 whenever two or more seeds tie for nearest distance.

**Program solution**

```python
def solve_H117(grid):
    h,w=dims(grid)
    out=clone(grid)
    # identify all seeds nonzero not wall
    seeds=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,5):
                seeds.append((r,c,v))
    # BFS distances within non-wall cells
    from collections import deque
    INF=10**9
    dists={}
    for sr,sc,color in seeds:
        dist=[[INF]*w for _ in range(h)]
        q=deque([(sr,sc)])
        dist[sr][sc]=0
        while q:
            r,c=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and grid[nr][nc]!=5 and dist[nr][nc]==INF:
                    dist[nr][nc]=dist[r][c]+1
                    q.append((nr,nc))
        dists[(sr,sc,color)] = dist
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                continue
            best=None; winners=[]
            for key,dist in dists.items():
                d=dist[r][c]
                if best is None or d<best:
                    best=d; winners=[key]
                elif d==best:
                    winners.append(key)
            if len(winners)==1:
                out[r][c]=winners[0][2]
            else:
                out[r][c]=8
    return out
```

### H118 — Prototype family dispatch under symmetry

**What it tests:** Match a neutral query shape against labeled prototypes up to rotation and reflection.

**Staged hint:** Compare the query shape to the prototype families by occupancy only. Once you know which family it belongs to, repaint the query with that prototype's label color.

**Train 1 — input**

```text
220533350775001
200503057705011
000500050005001
```

**Train 1 — output**

```text
003
033
003
```

**Train 2 — input**

```text
220533350775011
200503057705001
000500050005000
```

**Train 2 — output**

```text
022
002
000
```

**Test — input**

```text
220533350775100
200503057705110
000500050005010
```

**Test — output**

```text
700
770
070
```

**Written solution:** The first three panels are labeled prototype families. Compare the query panel’s occupancy pattern against those prototypes up to rotation and reflection, then recolor the query shape with the label color of the matching prototype.

**Program solution**

```python
def solve_H118(grid):
    p1,p2,p3,q = split_panel_row(grid,4,sep=5)
    prototypes=[]
    for p in [p1,p2,p3]:
        # label color = unique nonzero color in last row? maybe prototype colored already.
        colors={v for row in p for v in row if v!=0}
        # use max color as label? Hmm we will design prototype panels monochrome colored with label color.
        label=max(colors)
        shape_panel=[[1 if v!=0 else 0 for v in row] for row in p]
        variants={canon for _,_,canon in transformed_variants(shape_panel)}
        prototypes.append((label,variants))
    qshape_panel=[[1 if v!=0 else 0 for v in row] for row in q]
    qcanon=canonical_shape(qshape_panel)
    label=next(lbl for lbl,vars in prototypes if qcanon in vars)
    out=blank(*dims(q))
    for r,row in enumerate(q):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=label
    return out
```

### H119 — Compose two inferred transforms

**What it tests:** Infer one transform from panel A→B and another from C→D, then compose them on a query panel.

**Staged hint:** The first example gives transform T1 and the second gives T2. Apply T1 to the query first, then apply T2 to that result.

**Train 1 — input**

```text
2005022533050335040
2205020503050305044
0005000500050005000
```

**Train 1 — output**

```text
000
440
040
```

**Train 2 — input**

```text
600056600507705000050030
660050660500705000050330
060050000500005070050000
000050000500005077050000
```

**Train 2 — output**

```text
0000
0033
0030
0000
```

**Test — input**

```text
440050000500075000052200
040050440500775000050200
044050400500005007050000
000054400500005007750000
```

**Test — output**

```text
2000
2200
0000
0000
```

**Written solution:** Infer one transform T1 from the first example pair A→B and another transform T2 from the second example pair C→D. Apply T1 to the query panel first, then apply T2 to that intermediate result.

**Program solution**

```python
def solve_H119(grid):
    a,b,c,d,q = split_panel_row(grid,5,sep=5)
    _,f1=infer_transform(a,b)
    _,f2=infer_transform(c,d)
    return f2(f1(q))
```
