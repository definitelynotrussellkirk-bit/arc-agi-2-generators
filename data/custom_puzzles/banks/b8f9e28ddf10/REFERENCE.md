# 21 More ARC-Style Puzzles

This is the nineteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E127–E133, M127–M133, H127–H133**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into endpoint intervals, border classification, bbox abstraction, explicit-axis reflection, room filling, example-based transform inference, prototype stamping, edit-delta transfer, family matching under symmetry, and conflict-aware merges.

**New motifs in this batch**

**`interval_fill(row)`** — two equal-colored endpoints define a horizontal segment that should be completed. This is the core move in **E127**.

**`axis_reflect(axis, shape)`** — a full column of 8s acts as a literal mirror axis; preserve the axis and duplicate cells across it. This drives **M127**.

**`transform_recolor_infer(example_before, example_after, query)`** — infer both geometry and palette changes from one example pair, then apply both to a query. This is the key abstraction in **H127**.

**`edit_delta_relative(before, after, query)`** — extract which bbox-relative cells were added in an example edit and add the same relative cells to a new object. This powers **H129**.

**`family_match(prototypes, query)`** — compare a query against several prototype families up to rotation or reflection, then emit the canonical member of the matching family. This is the heart of **H131**.

**`conflict_merge(a, b)`** — merge two panels after a learned transform, but mark nonmatching overlaps with color 9 instead of choosing a side. This is central to **H132**.


## Easy

### E127 — Fill between matching endpoints

**What it tests:** Detect rows that contain exactly two equal-colored endpoints and fill the whole interval between them.

**Staged hint:** Ignore rows without a clean pair. On an active row, the endpoints already tell you the color and the span.

**Train 1 — input**

```text
0000000
2000200
0000000
0300030
0000000
```

**Train 1 — output**

```text
0000000
2222200
0000000
0333330
0000000
```

**Train 2 — input**

```text
000000
040040
000000
600600
000000
```

**Train 2 — output**

```text
000000
044440
000000
666600
000000
```

**Test — input**

```text
00000000
07000700
00000000
50005000
00000000
```

**Test — output**

```text
00000000
07777700
00000000
55555000
00000000
```

**Written solution:** Treat each row independently. When a row has exactly two nonzero cells and they have the same color, those cells act as endpoints of a horizontal segment. Fill every cell from the left endpoint to the right endpoint with that color. Leave all other rows unchanged.

**Program solution**

```python
def solve_E127(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        nz=[c for c in range(w) if grid[r][c]!=0]
        if len(nz)==2 and grid[r][nz[0]]==grid[r][nz[1]]:
            a,b=nz; color=grid[r][a]
            for c in range(a,b+1):
                out[r][c]=color
    return out
```

### E128 — Keep only border-touching objects

**What it tests:** Classify connected components by whether they touch the outer border.

**Staged hint:** First identify the objects. Then ask only one question about each object: does any cell lie on the frame of the grid?

**Train 1 — input**

```text
220000
020330
000030
044000
000000
```

**Train 1 — output**

```text
220000
020000
000000
000000
000000
```

**Train 2 — input**

```text
000006
077006
070000
000880
000000
```

**Train 2 — output**

```text
000006
000006
000000
000000
000000
```

**Test — input**

```text
0000000
9900300
0900330
0000000
0440002
0000002
```

**Test — output**

```text
0000000
9900000
0900000
0000000
0000002
0000002
```

**Written solution:** Find every nonzero connected component. Keep a component only if at least one of its cells touches the top row, bottom row, left column, or right column. Delete every fully interior object.

**Program solution**

```python
def solve_E128(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out
```

### E129 — Make the grid symmetric by transposition

**What it tests:** Use the main diagonal as a mirror and copy every colored cell to its transposed location.

**Staged hint:** Do not move cells; duplicate them. For every colored cell at (r,c), add the same color at (c,r).

**Train 1 — input**

```text
02000
00300
00000
00004
00000
```

**Train 1 — output**

```text
02000
20300
03000
00004
00040
```

**Train 2 — input**

```text
000600
000000
700000
000000
005000
000000
```

**Train 2 — output**

```text
007600
000000
700050
600000
005000
000000
```

**Test — input**

```text
008000
000000
000900
000000
040000
000000
```

**Test — output**

```text
008000
000040
800900
009000
040000
000000
```

**Written solution:** The output is the union of the original pattern and its transpose. Scan every nonzero cell and place a copy of the same color at the reflected position across the main diagonal. Existing colored cells stay where they are.

**Program solution**

```python
def solve_E129(grid):
    h,w=dims(grid)
    assert h==w
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                out[c][r]=grid[r][c]
    return out
```

### E130 — Erase singleton objects

**What it tests:** Separate one-cell components from multi-cell components.

**Staged hint:** Count component size, not color frequency. A color may appear in several different objects.

**Train 1 — input**

```text
000000
203300
200040
005000
066000
```

**Train 1 — output**

```text
000000
203300
200000
000000
066000
```

**Train 2 — input**

```text
07000
07080
00000
90001
99000
```

**Train 2 — output**

```text
07000
07000
00000
90000
99000
```

**Test — input**

```text
0000000
4055000
0000060
0700060
0770000
```

**Test — output**

```text
0000000
0055000
0000060
0700060
0770000
```

**Written solution:** Compute connected components color by color. Remove every component of size 1. Keep every component of size 2 or larger exactly as it is.

**Program solution**

```python
def solve_E130(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        if len(cells)>1:
            for r,c in cells:
                out[r][c]=color
    return out
```

### E131 — Legend row repaints the markers

**What it tests:** Use a single nonzero color in the top row as metadata and repaint all body markers 1 with that color.

**Staged hint:** The top row is not part of the final picture. Read its one nonzero value, then apply it to all 1-cells below.

**Train 1 — input**

```text
004000
010010
000000
101001
000000
```

**Train 1 — output**

```text
000000
040040
000000
404004
000000
```

**Train 2 — input**

```text
00070
10100
00000
01010
```

**Train 2 — output**

```text
00000
70700
00000
07070
```

**Test — input**

```text
0000900
0100010
1001000
0000000
0110000
```

**Test — output**

```text
0000000
0900090
9009000
0000000
0990000
```

**Written solution:** The only information in the first row is the chosen color. Ignore its position. Remove the legend row from the output and replace every 1 in the remaining rows by that legend color.

**Program solution**

```python
def solve_E131(grid):
    h,w=dims(grid)
    color=max(grid[0])
    out=blank(h,w)
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]==1:
                out[r][c]=color
    return out
```

### E132 — Stamp the midpoint of each pair

**What it tests:** Convert a pair of equal-colored endpoints in a row into a single midpoint marker.

**Staged hint:** Look for rows with exactly two equal nonzero cells and check whether their midpoint is an integer column.

**Train 1 — input**

```text
0000000
2000200
0000000
0404000
0000000
```

**Train 1 — output**

```text
0000000
0020000
0000000
0040000
0000000
```

**Train 2 — input**

```text
000000
060006
000000
303000
```

**Train 2 — output**

```text
000000
000600
000000
030000
```

**Test — input**

```text
00000000
07000700
00000000
50005000
00000000
```

**Test — output**

```text
00000000
00070000
00000000
00500000
00000000
```

**Written solution:** Rows with two equal-colored endpoints encode one target cell: their midpoint. Produce an otherwise blank grid and place the color only at the midpoint of each valid pair. If the pair has no integer midpoint, produce nothing for that row.

**Program solution**

```python
def solve_E132(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        nz=[c for c in range(w) if grid[r][c]!=0]
        if len(nz)==2 and grid[r][nz[0]]==grid[r][nz[1]]:
            a,b=nz
            if (a+b)%2==0:
                out[r][(a+b)//2]=grid[r][a]
    return out
```

### E133 — Replace each object by its bbox center

**What it tests:** Abstract a whole connected component down to the center of its bounding box.

**Staged hint:** Do not use the centroid by counting cells. Use the center of the component's bounding rectangle.

**Train 1 — input**

```text
0000000
2220000
2020333
2220303
0000333
```

**Train 1 — output**

```text
0000000
0000000
0200000
0000030
0000000
```

**Train 2 — input**

```text
044400
040400
044400
000060
000666
000060
```

**Train 2 — output**

```text
000000
004000
000000
000000
000060
000000
```

**Test — input**

```text
0000000
0777000
0707050
0777555
0000050
0000000
```

**Test — output**

```text
0000000
0000000
0070000
0000050
0000000
0000000
```

**Written solution:** For each connected component, compute its bounding box. Mark only the central cell of that bounding box with the component's color, and clear everything else.

**Program solution**

```python
def solve_E133(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid):
        r0,r1,c0,c1=bbox(cells)
        rr=(r0+r1)//2; cc_=(c0+c1)//2
        out[rr][cc_]=color
    return out
```


## Medium

### M127 — Reflect across the explicit axis

**What it tests:** Recognize the full vertical axis line and mirror all non-axis cells across it.

**Staged hint:** Find the column filled entirely with 8 first. Then every colored cell on one side determines one partner on the other side.

**Train 1 — input**

```text
0080000
2080000
2280000
0080000
0080000
```

**Train 1 — output**

```text
0080000
2080200
2282200
0080000
0080000
```

**Train 2 — input**

```text
00080000
04080000
44080000
04080000
00080000
```

**Train 2 — output**

```text
00080000
04080400
44080440
04080400
00080000
```

**Test — input**

```text
000080000
066080000
060080000
060080000
000080000
```

**Test — output**

```text
000080000
066080660
060080060
060080060
000080000
```

**Written solution:** The column of 8s is a mirror axis. Preserve it. For every other nonzero cell, keep the original cell and also color the reflected cell at the same row and the mirrored column.

**Program solution**

```python
def solve_M127(grid):
    h,w=dims(grid)
    axis=None
    for c in range(w):
        if all(grid[r][c]==8 for r in range(h)):
            axis=c; break
    out=blank(h,w)
    for r in range(h):
        out[r][axis]=8
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,8):
                out[r][c]=v
                mc=2*axis-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

### M128 — Fill each room from its seed

**What it tests:** Flood rooms separated by wall color 5, but only when a room contains exactly one seed color.

**Staged hint:** Treat walls as barriers. Within each room, ask how many seed colors are present before you fill anything.

**Train 1 — input**

```text
5555555
5205305
5005005
5555555
```

**Train 1 — output**

```text
5555555
5225335
5225335
5555555
```

**Train 2 — input**

```text
55555555
54005605
50005005
55555555
```

**Train 2 — output**

```text
55555555
54445665
54445665
55555555
```

**Test — input**

```text
555555555
570058005
500050005
500050005
555555555
```

**Test — output**

```text
555555555
577758885
577758885
577758885
555555555
```

**Written solution:** Partition the grid into rooms using the 5-cells as walls. In any room containing exactly one nonzero seed color, fill all remaining zeros in that room with that seed color. Leave the walls untouched.

**Program solution**

```python
def solve_M128(grid):
    h,w=dims(grid)
    # walls are 5
    seen=set(); out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen: 
                continue
            # room = connected cells not wall
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            seeds=set()
            while q:
                x,y=q.popleft(); cells.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.add(grid[x][y])
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

### M129 — Infer the panel transform

**What it tests:** Use an example before/after panel pair to infer a geometric transform, then apply it to a query panel.

**Staged hint:** Ignore the separator column. Solve the example pair first: which single transform turns the first panel into the second?

**Train 1 — input**

```text
10050015020
11050115022
00050005000
```

**Train 1 — output**

```text
020
220
000
```

**Train 2 — input**

```text
30050335440
33350305040
00050305040
```

**Train 2 — output**

```text
004
444
000
```

**Test — input**

```text
06050005700
06656605770
00050605000
```

**Test — output**

```text
000
077
007
```

**Written solution:** The input contains three panels: example input, example output, and query. Identify the geometric transform that maps the first panel to the second, choosing from basic rotations or reflections, and apply that same transform to the query panel.

**Program solution**

```python
def solve_M129(grid):
    ex_in, ex_out, query = split_panel_row1(grid,3,sep=1)
    name=infer_transform(ex_in, ex_out)
    if name is None:
        raise ValueError("no transform")
    return TRANSFORMS[name](query)
```

### M130 — Stamp the prototype at every anchor

**What it tests:** Extract the largest non-anchor object, crop it tightly, and stamp that crop at every marker 1.

**Staged hint:** Do not keep the original prototype in place. Treat it as a reusable stamp.

**Train 1 — input**

```text
4400000
4001010
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0004444
0004040
0000000
0000000
```

**Train 2 — input**

```text
00600000
06601000
00000010
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000600
00006606
00000066
00000000
```

**Test — input**

```text
077000000
007001000
000000010
000000000
100000000
000000000
```

**Test — output**

```text
000000000
000007700
000000777
000000007
770000000
070000000
```

**Written solution:** Find the largest connected component that is not an anchor 1. Crop it to its tight bounding box. Then create a blank output and stamp that cropped prototype with its top-left corner placed at every anchor cell.

**Program solution**

```python
def solve_M130(grid):
    h,w=dims(grid)
    comps=[(color,cells) for color,cells in cc(grid, ignore=(0,1))]
    if not comps:
        return blank(h,w)
    # largest component as prototype
    proto_color, proto_cells=max(comps, key=lambda t: len(t[1]))
    proto=crop_cells(grid, proto_cells)
    # bbox top-left of proto in source
    pr0,pr1,pc0,pc1=bbox(proto_cells)
    # output stamps prototype crop with its top-left anchored at each 1
    out=blank(h,w)
    anchors=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==1]
    ph,pw=dims(proto)
    for ar,ac in anchors:
        for r in range(ph):
            for c in range(pw):
                v=proto[r][c]
                if v!=0:
                    nr,nc=ar+r,ac+c
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

### M131 — Replace shapes by bounding-box frames

**What it tests:** Convert arbitrary connected components into rectangular outline frames of the same color.

**Staged hint:** Object geometry inside the box no longer matters. Only the extreme rows and columns matter.

**Train 1 — input**

```text
0000000
2200300
0200330
0000030
0000000
```

**Train 1 — output**

```text
0000000
2200330
2200330
0000330
0000000
```

**Train 2 — input**

```text
040000
444060
040066
000000
```

**Train 2 — output**

```text
444000
404066
444066
000000
```

**Test — input**

```text
00000000
07700500
00700550
00000050
00000000
```

**Test — output**

```text
00000000
07700550
07700550
00000550
00000000
```

**Written solution:** For each connected component, compute its bounding box and draw only the perimeter of that box in the component's color. Discard the original interior shape.

**Program solution**

```python
def solve_M131(grid):
    h,w=dims(grid); out=blank(h,w)
    for color,cells in cc(grid):
        r0,r1,c0,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out
```

### M132 — Reflect through the anchor point

**What it tests:** Use a single anchor 9 as a point of central symmetry and duplicate the shape through it.

**Staged hint:** The anchor is a point, not a line. For each cell, send it to the location equally far on the opposite side.

**Train 1 — input**

```text
0000000
0220000
0209000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0220000
0209020
0000220
0000000
```

**Train 2 — input**

```text
0000000
0040000
0049000
0044000
0000000
```

**Train 2 — output**

```text
0000000
0044400
0049400
0044400
0000000
```

**Test — input**

```text
00000000
00660000
00690000
00000000
00000000
```

**Test — output**

```text
00000000
00660000
00696000
00066000
00000000
```

**Written solution:** Locate the anchor 9. Keep it. For every other nonzero cell at (r,c), also place the same color at the point-reflected location (2*ar-r, 2*ac-c). The output is the union of the original shape and its point reflection.

**Program solution**

```python
def solve_M132(grid):
    h,w=dims(grid)
    ar=ac=None
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                ar,ac=r,c
    out[ar][ac]=9
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,9):
                out[r][c]=v
                nr,nc=2*ar-r,2*ac-c
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out
```

### M133 — Sort and pack components by area

**What it tests:** Normalize each connected component by cropping it, then sort the cropped pieces by area and pack them into a single strip.

**Staged hint:** Do not preserve their original positions. Crop first, rank second, pack last.

**Train 1 — input**

```text
0000000
2200300
2000330
0000000
0400000
```

**Train 1 — output**

```text
2203004
2003300
```

**Train 2 — input**

```text
000000
066600
006000
000077
000070
```

**Train 2 — output**

```text
666077
060070
```

**Test — input**

```text
00000000
08800900
08000990
00000000
04000000
```

**Test — output**

```text
8809004
8009900
```

**Written solution:** Extract each connected component and crop it to its tight bounding box. Sort the pieces by area from largest to smallest, breaking ties by earlier position, and place them left to right with one blank column between pieces in a minimal output canvas.

**Program solution**

```python
def solve_M133(grid):
    comps=[]
    for color,cells in cc(grid):
        piece=crop_cells(grid,cells)
        area=len(cells)
        r0,r1,c0,c1=bbox(cells)
        comps.append((area,r0,c0,color,piece))
    comps.sort(key=lambda t:(-t[0], t[1], t[2], t[3]))
    if not comps:
        return [[0]]
    heights=[dims(p)[0] for _,_,_,_,p in comps]
    widths=[dims(p)[1] for _,_,_,_,p in comps]
    out=blank(max(heights), sum(widths)+max(0,len(comps)-1))
    c0=0
    for i,(_,_,_,_,piece) in enumerate(comps):
        ph,pw=dims(piece)
        for r in range(ph):
            for c in range(pw):
                if piece[r][c]!=0:
                    out[r][c0+c]=piece[r][c]
        c0+=pw
        if i<len(comps)-1:
            c0+=1

    return out
```


## Hard

### H127 — Infer transform and recolor together

**What it tests:** Recover both a geometric transform and a color mapping from an example panel pair, then apply both to a query.

**Staged hint:** Separate shape and palette. First infer how the occupied cells move, then infer how colors change at the moved locations.

**Train 1 — input**

```text
20005000750600
23005004750610
03305044050011
00005000050000
```

**Train 1 — output**

```text
0060
0160
1100
0000
```

**Train 2 — input**

```text
40005008850100
46605002050133
00605022050003
00005000050000
```

**Train 2 — output**

```text
0000
0011
0030
0330
```

**Test — input**

```text
05005000050500
05705990050570
00705033050070
00005000050000
```

**Test — output**

```text
0000
9900
0330
0000
```

**Written solution:** Use the example input/output panels to infer two things: which geometric transform was applied to the shape support, and how colors were remapped after the transform. Apply the same transform to the query panel and then recolor each transformed cell using the learned color mapping.

**Program solution**

```python
def solve_H127(grid):
    ex_in, ex_out, query = split_panel_row1(grid,3,sep=1)
    # infer transform by support
    support_ex_in=[[1 if v!=0 else 0 for v in row] for row in ex_in]
    support_ex_out=[[1 if v!=0 else 0 for v in row] for row in ex_out]
    chosen=None
    for name,fn in TRANSFORMS.items():
        t=fn(support_ex_in)
        if dims(t)==dims(support_ex_out) and t==support_ex_out:
            chosen=name; break
    if chosen is None:
        raise ValueError("no support transform")
    tq=TRANSFORMS[chosen](query)
    tex=TRANSFORMS[chosen](ex_in)
    # infer color mapping from transformed example to ex_out
    mapping={}
    h,w=dims(ex_out)
    for r in range(h):
        for c in range(w):
            a=tex[r][c]; b=ex_out[r][c]
            if a!=0 and b!=0:
                mapping[a]=b
    out=clone(tq)
    for r in range(len(out)):
        for c in range(len(out[0])):
            if out[r][c]!=0:
                out[r][c]=mapping.get(out[r][c], out[r][c])
    return out
```

### H128 — Infer the binary mask operation

**What it tests:** Identify whether the example panels were combined by union, intersection, or xor on their occupied cells, then reuse that operation.

**Staged hint:** Treat the example result as evidence about set logic on nonzero positions, not about specific coordinates alone.

**Train 1 — input**

```text
2005000520050705000
2005020522050705700
0005020502050005700
```

**Train 1 — output**

```text
070
770
700
```

**Train 2 — input**

```text
3305030503058005000
0305030503058805880
0005030500050005080
```

**Train 2 — output**

```text
000
880
000
```

**Test — input**

```text
4405040540056005000
0405040500056605660
0005004500450005006
```

**Test — output**

```text
600
000
006
```

**Written solution:** Interpret each panel as a binary mask of occupied cells. Determine whether the example result is the union, intersection, or xor of the first two masks. Apply that same binary operation to the query pair and paint the resulting occupied cells with the query color.

**Program solution**

```python
def solve_H128(grid):
    a,b,res,c,d = split_panel_row1(grid,5,sep=1)
    def occ(g): return [[1 if v!=0 else 0 for v in row] for row in g]
    oa,ob,or_=occ(a),occ(b),occ(res)
    def union(x,y): return [[1 if x[r][c] or y[r][c] else 0 for c in range(len(x[0]))] for r in range(len(x))]
    def inter(x,y): return [[1 if x[r][c] and y[r][c] else 0 for c in range(len(x[0]))] for r in range(len(x))]
    def xor(x,y): return [[1 if (x[r][c]+y[r][c])%2==1 else 0 for c in range(len(x[0]))] for r in range(len(x))]
    ops={"union":union,"intersection":inter,"xor":xor}
    opname=None
    for name,fn in ops.items():
        if fn(oa,ob)==or_:
            opname=name; break
    if opname is None: raise ValueError("no op")
    o=ops[opname](occ(c), occ(d))
    # query color = first nonzero in c or d
    qcolor=0
    for panel in (c,d):
        for row in panel:
            for v in row:
                if v!=0:
                    qcolor=v; break
            if qcolor: break
        if qcolor: break
    out=blank(len(o), len(o[0]))
    for r in range(len(o)):
        for cc_ in range(len(o[0])):
            if o[r][cc_]:
                out[r][cc_]=qcolor
    return out
```

### H129 — Transfer the edit delta

**What it tests:** Infer which bbox-relative cells were added in an example edit and replay the same edit on a new object.

**Staged hint:** Compare before and after only after normalizing them to the same bounding-box frame.

**Train 1 — input**

```text
22052205000
20052205033
00050005030
```

**Train 1 — output**

```text
000
033
033
```

**Train 2 — input**

```text
04005440050000
44005440050060
00005000050660
00005000050000
```

**Train 2 — output**

```text
0000
0660
0660
0000
```

**Test — input**

```text
77005770050000
07005077050550
00005000050050
00005000050000
```

**Test — output**

```text
0000
0550
0055
0000
```

**Written solution:** Look at the example before/after object pair and record which cells were added, relative to the object's bounding box. Then find the query object's bounding box and add cells at the same relative positions using the query color.

**Program solution**

```python
def solve_H129(grid):
    before, after, query = split_panel_row1(grid,3,sep=1)
    # compute delta relative to bbox of before
    comps=cc(before)
    # assume one component
    color_b, cells_b = comps[0]
    r0,r1,c0,c1=bbox(cells_b)
    support_b={(r-r0,c-c0) for r,c in cells_b}
    color_a, cells_a = cc(after)[0]
    ra0,ra1,ca0,ca1=bbox(cells_a)
    support_a={(r-ra0,c-ca0) for r,c in cells_a}
    delta = support_a - support_b
    # apply to query's main component
    qcolor, qcells = cc(query)[0]
    qr0,qr1,qc0,qc1=bbox(qcells)
    out=clone(query)
    for dr,dc in delta:
        nr,nc=qr0+dr,qc0+dc
        if 0<=nr<len(out) and 0<=nc<len(out[0]):
            out[nr][nc]=qcolor
    return out
```

### H130 — Nearest-seed fill with ties

**What it tests:** Fill rooms by Manhattan distance to seeds while marking equal-distance ties with 9.

**Staged hint:** Work within one room at a time. For each zero cell, compare distances to all seeds in that room.

**Train 1 — input**

```text
55555
52035
50005
50005
55555
```

**Train 1 — output**

```text
55555
52935
52935
52935
55555
```

**Train 2 — input**

```text
5555555
5040005
5000005
5000605
5555555
```

**Train 2 — output**

```text
5555555
5444995
5449665
5996665
5555555
```

**Test — input**

```text
5555555
5700085
5000005
5000005
5555555
```

**Test — output**

```text
5555555
5779885
5779885
5779885
5555555
```

**Written solution:** Treat 5-cells as walls. In each room, every zero cell takes the color of the closest seed by Manhattan distance. If two different seed colors are tied for closest, color that cell 9 instead.

**Program solution**

```python
def solve_H130(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); room=[]
            seeds=[]
            while q:
                x,y=q.popleft(); room.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            for x,y in room:
                if grid[x][y]==0 and seeds:
                    dists=sorted((abs(x-sr)+abs(y-sc), col) for sr,sc,col in seeds)
                    if len(dists)>=2 and dists[0][0]==dists[1][0] and dists[0][1]!=dists[1][1]:
                        out[x][y]=9
                    else:
                        out[x][y]=dists[0][1]
    return out
```

### H131 — Match the prototype family

**What it tests:** Compare a query shape against several prototype families up to rotation or reflection, then emit the canonical prototype in the query color.

**Staged hint:** Normalize supports, not colors. The family match is geometric; recoloring happens only after the family is identified.

**Train 1 — input**

```text
100522250335007
110502053305077
000500050005007
```

**Train 1 — output**

```text
777
070
```

**Train 2 — input**

```text
100522250335006
110502053305066
000500050005000
```

**Train 2 — output**

```text
60
66
```

**Test — input**

```text
100522250335900
110502053305990
000500050005090
```

**Test — output**

```text
099
990
```

**Written solution:** Three prototype panels define three shape families. The query panel is one of those families after some rotation or reflection and a color change. Find which family matches, then output the canonical prototype shape from the library, recolored with the query color and cropped tightly.

**Program solution**

```python
def solve_H131(grid):
    p1,p2,p3,query = split_panel_row1(grid,4,sep=1)
    protos=[p1,p2,p3]
    qsupp,qcolor=normalize_support(query)
    match_idx=None
    for i,p in enumerate(protos):
        psupp,_=normalize_support(p)
        fam={transform_support(psupp,fn) for fn in TRANSFORMS.values()}
        if qsupp in fam:
            match_idx=i; break
    if match_idx is None: raise ValueError("no family")
    canon_supp,_=normalize_support(protos[match_idx])
    return apply_support(canon_supp, qcolor)
```

### H132 — Transform then merge with conflicts

**What it tests:** Infer a transform from an example pair, apply it to one query panel, and then merge that transformed panel with another one using conflict color 9.

**Staged hint:** Solve the example transform first. Only after that should you think about the merge rule.

**Train 1 — input**

```text
100500150205003
110501152205023
000500050005000
```

**Train 1 — output**

```text
023
029
000
```

**Train 2 — input**

```text
400504450605000
444504050665607
000504050005607
```

**Train 2 — output**

```text
000
669
667
```

**Test — input**

```text
080500056005000
088588056605094
000508050005004
```

**Test — output**

```text
000
099
009
```

**Written solution:** Infer the geometric transform that maps the example input panel to the example output panel. Apply that transform to the third panel. Then merge it with the fourth panel: keep lone nonzero cells, keep matching overlaps, and mark nonmatching overlaps with color 9.

**Program solution**

```python
def solve_H132(grid):
    ex_in, ex_out, x, y = split_panel_row1(grid,4,sep=1)
    name=infer_transform(ex_in, ex_out)
    if name is None: raise ValueError("no transform")
    tx=TRANSFORMS[name](x)
    h,w=dims(tx)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a,b=tx[r][c], y[r][c]
            if a==0 and b==0:
                out[r][c]=0
            elif a==0:
                out[r][c]=b
            elif b==0:
                out[r][c]=a
            elif a==b:
                out[r][c]=a
            else:
                out[r][c]=9
    return out
```

### H133 — Rank recolor and pack the inventory

**What it tests:** Use a palette row to recolor components by rank, then crop and pack them into a strip.

**Staged hint:** The top row gives the output colors in rank order. Rank the body components by area before recoloring.

**Train 1 — input**

```text
2340000
0100011
0000010
0000000
0110000
```

**Train 1 — output**

```text
2033044
0000040
```

**Train 2 — input**

```text
56700000
01000010
01100010
00000011
00001000
```

**Train 2 — output**

```text
5060070
0066070
0000077
```

**Test — input**

```text
89240000
01100010
01000011
00000000
00101110
```

**Test — output**

```text
80990200444
00900220000
```

**Written solution:** Ignore the top row as geometry and treat it as a palette list. Extract the connected components in the body, sort them by area from smallest to largest, recolor the ranked pieces using the palette colors in order, crop each piece tightly, and pack them left to right with one blank column between pieces.

**Program solution**

```python
def solve_H133(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=grid[1:]
    comps=[]
    for color,cells in cc(body):
        piece=crop_cells(body,cells)
        area=len(cells)
        r0,r1,c0,c1=bbox(cells)
        comps.append((area,r0,c0,piece))
    comps.sort(key=lambda t:(t[0], t[1], t[2]))  # ascending area
    recolored=[]
    for i,(area,r0,c0,piece) in enumerate(comps):
        ph,pw=dims(piece)
        rp=blank(ph,pw)
        color=palette[i]
        for r in range(ph):
            for c in range(pw):
                if piece[r][c]!=0:
                    rp[r][c]=color
        recolored.append(rp)
    if not recolored:
        return [[0]]
    out=blank(max(dims(p)[0] for p in recolored), sum(dims(p)[1] for p in recolored)+max(0,len(recolored)-1))
    c0=0
    for i,p in enumerate(recolored):
        ph,pw=dims(p)
        for r in range(ph):
            for c in range(pw):
                if p[r][c]!=0:
                    out[r][c0+c]=p[r][c]
        c0+=pw
        if i<len(recolored)-1:
            c0+=1
    return out
```
