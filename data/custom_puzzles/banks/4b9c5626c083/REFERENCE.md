# 21 More ARC-Style Puzzles

This is the fifteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E99–E105, M99–M105, H99–H105**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into vector-guided translation, header-driven recoloring, count-based tiling, room filling, example-inferred panel transforms, replayed panel edits, prototype dispatch, blocked sweeping, anchor orbits, and geodesic nearest-seed filling.

**New motifs in this batch**

**`guide_vector_move(object, src_marker, dst_marker)`** — compute the displacement from one guide cell to another and move the whole object by that vector. This is the key move in **M99**.

**`panel_edit_replay(example_before, example_after, query)`** — compare two example panels cellwise, extract the edit, and replay that exact edit on a third panel. This is the core primitive in **H100**.

**`prototype_dispatch_rot(prototypes, labels, query)`** — match a query shape to a prototype up to rotation and use the prototype’s label to recolor the query. This drives **H101**.

**`object_sweep_until_block(shape, direction, walls)`** — repeatedly translate a whole object and paint the union of all visited positions until the next move would hit a wall or boundary. This is the central operation in **H103**.

**`geodesic_voronoi_fill(seeds, walls)`** — fill each reachable empty cell with its uniquely nearest seed color through shortest paths in free space, leaving ties empty. This is the hardest idea in **H105**.

## Easy

### E99 — Fill the horizontal bridge

**What it tests:** Recognize same-color endpoints in a row and fill the zero cells between them.

**Staged hint:** Group cells by color. If a color appears exactly twice in one row with only zeros between them, fill that horizontal span.

**Train 1 — input**

```text
0000000
0200002
0000000
0000000
0000000
7000070
0000000
```

**Train 1 — output**

```text
0000000
0222222
0000000
0000000
0000000
7777770
0000000
```

**Train 2 — input**

```text
000000000
000500000
000000000
040000004
000000000
000000000
000000303
```

**Train 2 — output**

```text
000000000
000500000
000000000
044444444
000000000
000000000
000000333
```

**Test — input**

```text
00000000
00030003
00000000
06000006
00000000
00000000
00000000
00000000
```

**Test — expected output**

```text
00000000
00033333
00000000
06666666
00000000
00000000
00000000
00000000
```

**Written solution**

For each color, look for exactly two occurrences in the same row. If all cells between those endpoints are 0, fill the entire segment between them with that color. Leave all other cells unchanged.

**Reference program (`solve_E99`)**

```python
def solve_E99(grid):
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

### E100 — Paint the midpoint

**What it tests:** Find aligned endpoint pairs and mark the unique center cell when the span has an exact midpoint.

**Staged hint:** Check each color separately. If its two cells line up horizontally or vertically and the gap length is even, paint the midpoint.

**Train 1 — input**

```text
0000000
0300030
0000000
0000000
0000000
0006000
0000000
0006000
0000000
```

**Train 1 — output**

```text
0000000
0303030
0000000
0000000
0000000
0006000
0006000
0006000
0000000
```

**Train 2 — input**

```text
000000000
000000000
004000000
000000000
004000000
000000000
000700070
000000000
```

**Train 2 — output**

```text
000000000
000000000
004000000
004000000
004000000
000000000
000707070
000000000
```

**Test — input**

```text
000000000
000400040
000000000
000000000
007000000
000000000
007000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000404040
000000000
000000000
007000000
007000000
007000000
000000000
000000000
```

**Written solution**

For every color that appears exactly twice, check whether the two cells share a row or a column. If they do and there is a single midpoint between them, paint that midpoint with the same color while keeping the endpoints.

**Reference program (`solve_E100`)**

```python
def solve_E100(grid):
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
            if r1==r2:
                a,b=sorted([c1,c2])
                if (b-a)%2==0 and all(grid[r1][c]==0 for c in range(a+1,b)):
                    out[r1][(a+b)//2]=color
            elif c1==c2:
                a,b=sorted([r1,r2])
                if (b-a)%2==0 and all(grid[r][c1]==0 for r in range(a+1,b)):
                    out[(a+b)//2][c1]=color
    return out
```

### E101 — Complete the missing corner

**What it tests:** Local 2x2 pattern completion from an L-shape of three equal-colored cells.

**Staged hint:** Slide a 2x2 window over the grid. Whenever three cells in that window share one color and the fourth is 0, fill the missing one.

**Train 1 — input**

```text
0000000
0220000
0200000
0000000
0003300
0000330
0000000
```

**Train 1 — output**

```text
0000000
0220000
0220000
0000000
0003330
0003330
0000000
```

**Train 2 — input**

```text
00000000
04400000
00400000
00000000
00000660
00000600
00000000
00000000
```

**Train 2 — output**

```text
00000000
04400000
04400000
00000000
00000660
00000660
00000000
00000000
```

**Test — input**

```text
00000000
05500000
00500000
00000000
00000066
00000060
00000000
00000000
```

**Test — expected output**

```text
00000000
05500000
05500000
00000000
00000066
00000066
00000000
00000000
```

**Written solution**

Inspect every 2x2 block. If exactly three cells are nonzero and all three have the same color, fill the fourth cell with that color. This completes each partial 2x2 square.

**Reference program (`solve_E101`)**

```python
def solve_E101(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r+1][c],grid[r][c+1],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                color=nz[0]
                if vals[0]==0: out[r][c]=color
                if vals[1]==0: out[r+1][c]=color
                if vals[2]==0: out[r][c+1]=color
                if vals[3]==0: out[r+1][c+1]=color
    return out
```

### E102 — Keep only the largest component

**What it tests:** Connected-component detection and size-based filtering.

**Staged hint:** Find all nonzero 4-connected components, compare their areas, and keep only the biggest one.

**Train 1 — input**

```text
00000000
02220000
02000000
02200000
00000000
00055000
00005000
00000000
```

**Train 1 — output**

```text
00000000
02220000
02000000
02200000
00000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
000000000
000770000
000070000
000000000
044400000
040000000
000000330
000000030
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
044400000
040000000
000000000
000000000
000000000
```

**Test — input**

```text
000000000
000330000
000030000
000000000
077770000
070000000
000000550
000000050
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000000000
077770000
070000000
000000000
000000000
000000000
```

**Written solution**

Split the grid into connected nonzero components using 4-neighbor connectivity. Choose the component with the largest area, copy it unchanged into a blank grid, and erase every other component.

**Reference program (`solve_E102`)**

```python
def solve_E102(grid):
    h,w=dims(grid)
    comps=connected_components(grid)
    if not comps:
        return blank(h,w)
    best=max(comps, key=lambda vc:(len(vc[1]), -min(r for r,c in vc[1]), -min(c for r,c in vc[1])))
    out=blank(h,w)
    color,cells=best
    for r,c in cells:
        out[r][c]=color
    return out
```

### E103 — Draw the rectangle from diagonal corners

**What it tests:** Infer an axis-aligned rectangle outline from two opposite corner markers.

**Staged hint:** Two cells of the same color determine the top/bottom rows and left/right columns of a rectangle.

**Train 1 — input**

```text
0000000
0200000
0000000
0000000
0000020
0004000
0000004
```

**Train 1 — output**

```text
0000000
0222220
0200020
0200020
0222220
0004444
0004444
```

**Train 2 — input**

```text
000000000
000000000
001000000
000000000
000000000
000001000
000000000
000600000
000000060
```

**Train 2 — output**

```text
000000000
000000000
001111000
001001000
001001000
001111000
000000000
000666660
000666660
```

**Test — input**

```text
000000000
000000000
002000000
000000000
000000000
000020000
000000700
000000000
000000007
```

**Test — expected output**

```text
000000000
000000000
002220000
002020000
002020000
002220000
000000777
000000707
000000777
```

**Written solution**

For each color, treat its two cells as opposite corners of an axis-aligned rectangle. Draw the rectangle's outline in that color by filling the two horizontal edges and the two vertical edges.

**Reference program (`solve_E103`)**

```python
def solve_E103(grid):
    h,w=dims(grid)
    out=blank(h,w)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                by[grid[r][c]].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1!=r2 and c1!=c2:
                rlo,rhi=sorted([r1,r2]); clo,chi=sorted([c1,c2])
                for c in range(clo,chi+1):
                    out[rlo][c]=color; out[rhi][c]=color
                for r in range(rlo,rhi+1):
                    out[r][clo]=color; out[r][chi]=color
    return out
```

### E104 — Mirror across the main diagonal

**What it tests:** Coordinate transposition and symmetric union in a square grid.

**Staged hint:** Each colored cell at (r,c) should also appear at (c,r). Keep the originals too.

**Train 1 — input**

```text
0000000
0200000
0020000
0000000
0007000
0000700
0000000
```

**Train 1 — output**

```text
0000000
0200000
0020000
0000700
0007070
0000700
0000000
```

**Train 2 — input**

```text
000000
000000
040000
004000
000000
000800
```

**Train 2 — output**

```text
000000
004000
040400
004008
000000
000800
```

**Test — input**

```text
000000
006000
000000
000400
000040
000000
```

**Test — expected output**

```text
000000
006000
060000
000400
000040
000000
```

**Written solution**

Use the main diagonal as a mirror. For every nonzero cell, place a same-colored copy at the transposed coordinate with row and column swapped. Keep all original cells as well.

**Reference program (`solve_E104`)**

```python
def solve_E104(grid):
    h,w=dims(grid)
    assert h==w
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                out[c][r]=v
    return out
```

### E105 — Remove border-touching components

**What it tests:** Filter connected components by whether they touch the outer frame.

**Staged hint:** Find each nonzero component and ask whether any of its cells touches row 0, row h-1, col 0, or col w-1.

**Train 1 — input**

```text
22000000
20000000
00033000
00003000
00000000
00004440
00000400
00000000
```

**Train 1 — output**

```text
00000000
00000000
00033000
00003000
00000000
00004440
00000400
00000000
```

**Train 2 — input**

```text
000000000
000550000
000050000
000000000
000000660
000000060
000000000
770000000
070000000
```

**Train 2 — output**

```text
000000000
000550000
000050000
000000000
000000660
000000060
000000000
000000000
000000000
```

**Test — input**

```text
000000000
220000000
200000000
000055000
000005000
000000000
000007700
000000700
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000055000
000005000
000000000
000007700
000000700
000000000
```

**Written solution**

Decompose the grid into connected nonzero components. Any component that touches the outer border is deleted; any component fully enclosed in the interior is preserved unchanged.

**Reference program (`solve_E105`)**

```python
def solve_E105(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid):
        if all(0<r<h-1 and 0<c<w-1 for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out
```

## Medium

### M99 — Move by the guide vector

**What it tests:** Translate an entire object using the vector from a source marker to a destination marker.

**Staged hint:** Ignore the 8 and 9 markers except to compute their row/column difference. Apply that vector to every other nonzero cell.

**Train 1 — input**

```text
00000000
08002000
00002300
00090000
00000000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000020
00000023
00000000
00000000
00000000
```

**Train 2 — input**

```text
000000000
000000000
000400000
000440000
000000000
080000000
000090000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000400
000000440
000000000
000000000
000000000
000000000
```

**Test — input**

```text
000000000
080000000
000000000
000900000
055000000
050000000
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
000000000
000550000
000500000
000000000
```

**Written solution**

Find the unique 8 cell and the unique 9 cell. Compute the translation vector from 8 to 9, remove the markers, and move every remaining nonzero cell by that same vector into a blank output grid.

**Reference program (`solve_M99`)**

```python
def solve_M99(grid):
    h,w=dims(grid)
    p8=p9=None
    obj=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==8: p8=(r,c)
            elif v==9: p9=(r,c)
            elif v!=0: obj.append((r,c,v))
    dr=p9[0]-p8[0]; dc=p9[1]-p8[1]
    out=blank(h,w)
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out
```

### M100 — Recolor by column headers

**What it tests:** Use a metadata row to recolor a body mask column by column.

**Staged hint:** The top row gives the output color for each column. Any nonzero body cell becomes that column's header color.

**Train 1 — input**

```text
20340
70070
00700
70070
00070
```

**Train 1 — output**

```text
00000
20040
00300
20040
00040
```

**Train 2 — input**

```text
506020
700000
007000
700070
000070
007000
```

**Train 2 — output**

```text
000000
500000
006000
500020
000020
006000
```

**Test — input**

```text
3040200
7000000
0070000
7000700
0000700
0070000
0000000
```

**Test — expected output**

```text
0000000
3000000
0040000
3000200
0000200
0040000
0000000
```

**Written solution**

Treat row 0 as column metadata. For every nonzero cell below the header row, replace it with the color shown at the top of its column. Cells under a 0 header stay 0. The header row itself disappears.

**Reference program (`solve_M100`)**

```python
def solve_M100(grid):
    h,w=dims(grid)
    out=blank(h,w)
    headers=grid[0]
    for r in range(1,h):
        for c in range(w):
            if grid[r][c]!=0:
                out[r][c]=headers[c]
    return out
```

### M101 — Repeat the cropped object k times

**What it tests:** Count markers, crop an object to its bounding box, and tile copies with spacing.

**Staged hint:** Count the 9s in the top row, crop the non-marker object below, then concatenate that cropped patch horizontally with one blank column between copies.

**Train 1 — input**

```text
990000
020000
022000
000000
```

**Train 1 — output**

```text
20020
22022
```

**Train 2 — input**

```text
9990000
0033000
0003000
0000000
```

**Train 2 — output**

```text
33033033
03003003
```

**Test — input**

```text
99990000
00600000
06600000
00000000
```

**Test — expected output**

```text
06006006006
66066066066
```

**Written solution**

Count how many 9 markers appear in the top row. Crop the nonzero object below to its minimal bounding box, then build a new output canvas consisting of that cropped patch repeated k times horizontally with one empty spacer column between copies.

**Reference program (`solve_M101`)**

```python
def solve_M101(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v==9)
    cells=[(r,c) for r in range(1,h) for c in range(w) if grid[r][c]!=0]
    r0,r1,c0,c1=bbox_of_cells(cells)
    obj=[row[c0:c1+1] for row in grid[r0:r1+1]]
    oh,ow=dims(obj)
    out=blank(oh, ow*k + (k-1))
    x=0
    for i in range(k):
        paste(out,0,x,obj)
        x += ow+1
    return out
```

### M102 — Keep the nearest object to the anchor

**What it tests:** Object selection by Manhattan distance to a special anchor cell.

**Staged hint:** Measure the distance from the 9 anchor to each component using the closest cell of that component.

**Train 1 — input**

```text
000000000
022200000
020000000
000000900
000055000
000005000
000000000
000007700
000000700
```

**Train 1 — output**

```text
000000000
000000000
000000000
000000000
000055000
000005000
000000000
000000000
000000000
```

**Train 2 — input**

```text
00000000
00440000
00040000
00000000
00090000
00000000
00002220
00002000
```

**Train 2 — output**

```text
00000000
00440000
00040000
00000000
00000000
00000000
00000000
00000000
```

**Test — input**

```text
000000000
000440000
000040000
000000000
000009000
000000000
007700000
000700000
000000000
```

**Test — expected output**

```text
000000000
000440000
000040000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Written solution**

Locate the anchor cell 9. Among all other connected components, choose the one whose nearest cell has the smallest Manhattan distance to the anchor. Copy only that component into a blank output grid.

**Reference program (`solve_M102`)**

```python
def solve_M102(grid):
    h,w=dims(grid)
    anchor=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                anchor=(r,c)
    out=blank(h,w)
    best=None
    for color,cells in connected_components(grid, ignore=(0,9)):
        dist=min(abs(r-anchor[0])+abs(c-anchor[1]) for r,c in cells)
        key=(dist, len(cells), min(r for r,c in cells), min(c for r,c in cells))
        if best is None or key < best[0]:
            best=(key,color,cells)
    if best:
        _,color,cells=best
        for r,c in cells:
            out[r][c]=color
    return out
```

### M103 — Fill each room from its seed

**What it tests:** Room segmentation with walls and flood-fill from the unique seed in each room.

**Staged hint:** Treat 1 as a wall. Each open room contains exactly one nonzero seed color; fill the room's zeros with that color.

**Train 1 — input**

```text
111111111
120010031
100010001
100010001
111111111
140000001
100000001
111111111
```

**Train 1 — output**

```text
111111111
122213331
122213331
122213331
111111111
144444441
144444441
111111111
```

**Train 2 — input**

```text
11111111
15010021
10010001
11111111
13000001
10000001
11111111
```

**Train 2 — output**

```text
11111111
15512221
15512221
11111111
13333331
13333331
11111111
```

**Test — input**

```text
111111111
120010041
100010001
100010001
111111111
130000001
100000001
111111111
```

**Test — expected output**

```text
111111111
122214441
122214441
122214441
111111111
133333331
133333331
111111111
```

**Written solution**

Consider the 1s to be walls. Each connected zero/nonzero region separated by those walls contains one seed color. Fill every 0 cell in that room with the seed's color, while keeping the walls unchanged.

**Reference program (`solve_M103`)**

```python
def solve_M103(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=1 and (r,c) not in seen:
                q=deque([(r,c)]); seen.add((r,c)); room=[]; seeds={}
                while q:
                    x,y=q.popleft(); room.append((x,y))
                    if grid[x][y]!=0:
                        seeds[grid[x][y]]=seeds.get(grid[x][y],0)+1
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=1 and (nx,ny) not in seen:
                            seen.add((nx,ny)); q.append((nx,ny))
                if len(seeds)==1:
                    color=next(iter(seeds))
                    for x,y in room:
                        if out[x][y]==0:
                            out[x][y]=color
    return out
```

### M104 — Crop the object and stamp it at the marker

**What it tests:** Bounding-box normalization followed by relocation to a target marker.

**Staged hint:** Find the non-marker object's bounding box, crop it, and paste that crop with its top-left corner at the 9 marker.

**Train 1 — input**

```text
00000000
02200000
02000000
00000090
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000022
00000020
00000000
```

**Train 2 — input**

```text
000000000
000330000
000030000
000000000
900000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
330000000
030000000
000000000
```

**Test — input**

```text
000000000
004400000
000400000
000000000
000009000
000000000
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
000004400
000000400
000000000
000000000
000000000
```

**Written solution**

Ignore the 9 marker when extracting the object. Crop the object's minimal bounding box, erase the original scene, and paste that cropped patch into a blank grid so that its top-left corner lands on the 9 marker position.

**Reference program (`solve_M104`)**

```python
def solve_M104(grid):
    h,w=dims(grid)
    marker=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9: marker=(r,c)
            elif v!=0: cells.append((r,c))
    r0,r1,c0,c1=bbox_of_cells(cells)
    sub=[row[c0:c1+1] for row in grid[r0:r1+1]]
    out=blank(h,w)
    paste(out,marker[0],marker[1],sub)
    return out
```

### M105 — Emit rays from coded direction markers

**What it tests:** Symbolic direction decoding and line emission from colored seeds.

**Staged hint:** Colors 1, 2, 3, and 4 act as up, down, left, and right markers. Each marker is attached to one seed cell, and that seed color extends along the coded direction.

**Train 1 — input**

```text
0000000
0000000
0054000
0000000
0006000
0002000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0055555
0000000
0006000
0006000
0006000
```

**Train 2 — input**

```text
00000000
00000000
00010000
00070000
00000000
00003600
00000000
00000000
```

**Train 2 — output**

```text
00070000
00070000
00070000
00070000
00000000
66666600
00000000
00000000
```

**Test — input**

```text
000000000
000050400
000000000
000010000
000070000
000000000
000003600
000000000
000000000
```

**Test — expected output**

```text
000070000
000070000
000070000
000070000
000070000
000000000
666666600
000000000
000000000
```

**Written solution**

Interpret marker colors 1/2/3/4 as up/down/left/right. Each marker sits adjacent to a colored seed. Starting from the seed, draw a straight ray of the seed's color in the marker's direction until the grid boundary, and omit the marker itself.

**Reference program (`solve_M105`)**

```python
def solve_M105(grid):
    h,w=dims(grid)
    out=blank(h,w)
    dirs={1:(-1,0), 2:(1,0), 3:(0,-1), 4:(0,1)}
    used=set()
    for r in range(h):
        for c in range(w):
            code=grid[r][c]
            if code in dirs:
                dr,dc=dirs[code]
                sr,sc=r-dr,c-dc  # seed sits opposite to travel direction: marker is just beyond seed
                if 0<=sr<h and 0<=sc<w and grid[sr][sc] not in (0,1,2,3,4):
                    color=grid[sr][sc]
                    x,y=sr,sc
                    while 0<=x<h and 0<=y<w:
                        out[x][y]=color
                        x+=dr; y+=dc
    return out
```

## Hard

### H99 — Infer the panel transform from the example

**What it tests:** Within-instance transform inference from one example panel pair, then reuse on a query panel.

**Staged hint:** The left panel and middle panel show the transform. Identify which global flip/rotation maps the first to the second, then apply it to the right panel.

**Train 1 — input**

```text
10005001150200
11005011050220
01005000050000
00005000050000
```

**Train 1 — output**

```text
0000
0022
0020
0000
```

**Train 2 — input**

```text
03005003054000
03305033054400
00305030050400
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
20005000050030
22005002050330
02005002250000
00005000250000
```

**Test — expected output**

```text
0000
0000
0330
0300
```

**Written solution**

Read the input as three panels separated by 5-columns. The first panel is an example source, the second panel is its transformed target, and the third panel is a query. Detect which whole-panel transform maps panel 1 to panel 2, then apply that same transform to panel 3.

**Reference program (`solve_H99`)**

```python
def solve_H99(grid):
    h,w=dims(grid)
    n=h
    A,B,C = split_panels_row(grid,n,count=3)
    transforms=["rot90","rot180","rot270","flip_h","flip_v","transpose"]
    chosen=None
    for t in transforms:
        if apply_transform(A,t)==B:
            chosen=t
            break
    if chosen is None:
        raise ValueError("no transform match")
    return apply_transform(C,chosen)
```

### H100 — Replay the panel edit

**What it tests:** Within-instance edit extraction and transfer from an example panel pair to a query panel.

**Staged hint:** Compare the first two panels cell by cell. Whatever changes from panel 1 to panel 2 should be replayed onto panel 3.

**Train 1 — input**

```text
02000502004500000
02200502204500330
00000500000500030
00000500000500000
00000500000500000
```

**Train 1 — output**

```text
00004
00334
00030
00000
00000
```

**Train 2 — input**

```text
00000500000500060
00500500500500060
05500505500500000
00000500700500000
00000500700500000
```

**Train 2 — output**

```text
00060
00060
00000
00700
00700
```

**Test — input**

```text
00000590000500060
00200590200500060
02200592200500000
00000500000500000
00000500000500000
```

**Test — expected output**

```text
90060
90060
90000
00000
00000
```

**Written solution**

Again treat the input as three panels separated by 5-columns. Compare the first panel with the second to find the exact cellwise edit pattern. Apply those same additions, removals, or recolors at the same panel coordinates to the third panel.

**Reference program (`solve_H100`)**

```python
def solve_H100(grid):
    h,w=dims(grid)
    n=h
    A,B,C = split_panels_row(grid,n,count=3)
    out=clone(C)
    for r in range(n):
        for c in range(n):
            if A[r][c]==0 and B[r][c]!=0:
                out[r][c]=B[r][c]
            elif A[r][c]!=0 and B[r][c]==0:
                out[r][c]=0
            elif A[r][c]!=B[r][c] and A[r][c]!=0 and B[r][c]!=0:
                out[r][c]=B[r][c]
    return out
```

### H101 — Dispatch by rotated prototype

**What it tests:** Prototype matching under rotation plus label lookup from a multi-panel dictionary.

**Staged hint:** The first and third panels are prototype shapes. The second and fourth panels give their label colors. Match the fifth panel to one prototype up to rotation, then recolor the query with that prototype's label.

**Train 1 — input**

```text
100050000501105000050010
100050000511005000050011
110050060500005000750001
000050000500005000050000
```

**Train 1 — output**

```text
0070
0077
0007
0000
```

**Train 2 — input**

```text
010050000500105000050000
010050000501115000050010
011050080500005004051110
000050000500005000050000
```

**Train 2 — output**

```text
0000
0080
8880
0000
```

**Test — input**

```text
010050000500105000050000
010050000501105000050010
011050008501005000450110
000050000500005000050100
```

**Test — expected output**

```text
0000
0040
0440
0400
```

**Written solution**

Read the input as five panels in a row. Panel 1 and panel 3 are prototype shapes, and panel 2 and panel 4 each contain a single label color for the prototype next to them. The fifth panel is a query shape. Match the query's occupancy pattern to one prototype up to rotation, then recolor the query shape with the corresponding label color.

**Reference program (`solve_H101`)**

```python
def solve_H101(grid):
    n=len(grid)
    P1,L1,P2,L2,Q = panels5(grid)
    label1=next(v for row in L1 for v in row if v!=0)
    label2=next(v for row in L2 for v in row if v!=0)
    q_occ=occupancy(Q)
    p1_vars=[occupancy(apply_transform(P1,t)) for t in ["id","rot90","rot180","rot270"]]
    p2_vars=[occupancy(apply_transform(P2,t)) for t in ["id","rot90","rot180","rot270"]]
    if q_occ in p1_vars:
        return recolor_shape(Q,label1)
    if q_occ in p2_vars:
        return recolor_shape(Q,label2)
    raise ValueError("query matches no prototype")
```

### H102 — Sort rows and columns by the headers

**What it tests:** Dual-axis permutation of a body matrix based on top and left metadata headers.

**Staged hint:** Ignore the top-left corner. Sort body rows by the left header values and sort body columns by the top header values.

**Train 1 — input**

```text
0312
2456
3789
1654
```

**Train 1 — output**

```text
546
564
897
```

**Train 2 — input**

```text
0213
3478
1594
2675
```

**Train 2 — output**

```text
954
765
748
```

**Test — input**

```text
0321
1789
2546
3675
```

**Test — expected output**

```text
987
645
576
```

**Written solution**

The first row and first column are metadata. Take the interior body matrix, reorder its rows so the left-side headers are in ascending order, and reorder its columns so the top headers are in ascending order. Output only the permuted body.

**Reference program (`solve_H102`)**

```python
def solve_H102(grid):
    n=len(grid)-1
    col_headers=grid[0][1:]
    row_headers=[grid[r][0] for r in range(1,n+1)]
    body=[row[1:] for row in grid[1:]]
    row_order=sorted(range(n), key=lambda i: row_headers[i])
    col_order=sorted(range(n), key=lambda i: col_headers[i])
    return [[body[r][c] for c in col_order] for r in row_order]
```

### H103 — Sweep the whole object until blocked

**What it tests:** Iterative object translation with blockers, keeping the full swept union.

**Staged hint:** One unique direction marker controls the entire non-marker object. Move the object step by step, painting every visited position, until the next move would hit a wall or leave the grid.

**Train 1 — input**

```text
4000000
0660000
0600008
0000008
0000008
0000000
0000000
```

**Train 1 — output**

```text
0000000
0666666
0666668
0000008
0000008
0000000
0000000
```

**Train 2 — input**

```text
2000000
0000000
0006600
0000600
0000000
8888888
0000000
```

**Train 2 — output**

```text
0000000
0000000
0006600
0006600
0000600
8888888
0000000
```

**Test — input**

```text
00000000
00000000
00007700
00007000
40000008
00000008
00000008
00000000
```

**Test — expected output**

```text
00000000
00000000
00007777
00007770
00000008
00000008
00000008
00000000
```

**Written solution**

Interpret the unique marker 1/2/3/4 as a global sweep direction for the whole object. Treat 8 as an immovable wall. Starting from the initial object, repeatedly translate it by one step in the chosen direction and paint the union of all positions, stopping just before a step would hit a wall or the boundary.

**Reference program (`solve_H103`)**

```python
def solve_H103(grid):
    h,w=dims(grid)
    dirs={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}
    code_cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] in dirs]
    if len(code_cells)!=1:
        raise ValueError("need exactly one direction marker")
    r0,c0,code=code_cells[0]
    walls={(r,c) for r in range(h) for c in range(w) if grid[r][c]==8}
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,8,1,2,3,4)]
    dr,dc=dirs[code]
    out=blank(h,w)
    for r,c in walls:
        out[r][c]=8
    cur=obj[:]
    while True:
        for r,c,v in cur:
            out[r][c]=v
        nxt=[(r+dr,c+dc,v) for r,c,v in cur]
        if any(not (0<=r<h and 0<=c<w) or (r,c) in walls for r,c,v in nxt):
            break
        cur=nxt
    return out
```

### H104 — Build a k-step orbit around the anchor

**What it tests:** Anchor-relative quarter-turn rotation and union of the first k orbit states.

**Staged hint:** Count the 1s in the top row. Keep the 9 anchor fixed, reinterpret the other cells as offsets from it, and rotate those offsets by 0, 90, 180, ... degrees for k steps.

**Train 1 — input**

```text
1100000
0000000
0006600
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0006600
0009600
0000600
0000000
0000000
```

**Train 2 — input**

```text
111000000
000000000
000000000
000060000
000690000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000000000
000060000
000696000
000060000
000000000
000000000
000000000
```

**Test — input**

```text
111100000
000000000
000000000
000000000
000096000
000006000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000000
000000000
000666000
000696000
000666000
000000000
000000000
000000000
```

**Written solution**

The 9 cell is a fixed anchor. The number of 1 markers tells you how many quarter-turn copies to include. Express every non-marker shape cell as an offset from the anchor, then paint the union of that shape rotated around the anchor through the first k quarter turns, keeping the anchor itself.

**Reference program (`solve_H104`)**

```python
def solve_H104(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v==1)
    anchor=None
    shape=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v not in (0,1):
                shape.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w)
    out[ar][ac]=9
    for quarter in range(k):
        for r,c,v in shape:
            if (r,c)==anchor: 
                continue
            dr,dc=r-ar,c-ac
            nr_off,nc_off=rotate_offset(dr,dc,quarter)
            nr,nc=ar+nr_off,ac+nc_off
            if 0<=nr<h and 0<=nc<w and not (nr==ar and nc==ac):
                out[nr][nc]=v
    return out
```

### H105 — Fill by nearest seed through corridors

**What it tests:** Geodesic Voronoi-style filling with walls and tie handling.

**Staged hint:** Treat 1 as walls. For every empty cell, compare shortest-path distances to all seeds through open space; a unique nearest seed wins, and ties stay 0.

**Train 1 — input**

```text
111111111
120000031
100000001
100000001
111101111
140000001
100000001
111111111
```

**Train 1 — output**

```text
111111111
122203331
122203331
122203331
111141111
144444441
144444441
111111111
```

**Train 2 — input**

```text
111111111
120000041
100000001
100000001
100000001
111111111
```

**Train 2 — output**

```text
111111111
122204441
122204441
122204441
122204441
111111111
```

**Test — input**

```text
1111111111
1200000041
1000000001
1000000001
1111011111
1300000001
1000000001
1111111111
```

**Test — expected output**

```text
1111111111
1222244441
1222244441
1222044441
1111311111
1333333331
1333333331
1111111111
```

**Written solution**

Use the 1s as walls that block movement. For each 0 cell, compute the shortest-path distance through open cells to every colored seed. If exactly one seed is nearest, fill the cell with that seed's color; if there is a tie, leave the cell 0. Keep walls and original seeds unchanged.

**Reference program (`solve_H105`)**

```python
def solve_H105(grid):
    h,w=dims(grid)
    walls={(r,c) for r in range(h) for c in range(w) if grid[r][c]==1}
    seeds=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,1)]
    dist_maps={}
    for sr,sc,color in seeds:
        q=deque([(sr,sc)])
        dist={(sr,sc):0}
        while q:
            r,c=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in walls and (nr,nc) not in dist:
                    dist[(nr,nc)] = dist[(r,c)] + 1
                    q.append((nr,nc))
        dist_maps[(sr,sc,color)] = dist
    out=clone(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0:
                best=None; best_colors=[]
                for seed,dist in dist_maps.items():
                    if (r,c) in dist:
                        d=dist[(r,c)]
                        color=seed[2]
                        if best is None or d<best:
                            best=d; best_colors=[color]
                        elif d==best and color not in best_colors:
                            best_colors.append(color)
                if best is not None and len(best_colors)==1:
                    out[r][c]=best_colors[0]
    return out
```
