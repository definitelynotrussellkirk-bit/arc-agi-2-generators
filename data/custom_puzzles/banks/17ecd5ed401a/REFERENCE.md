# 21 More ARC-Style Puzzles

This is the sixteenth continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E106–E112, M106–M112, H106–H112**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into vertical completion, local object growth, guide-vector copying, border-contact classification, frame transplantation, prototype dispatch, edit-stencil transfer, mask composition, roomwise seed filling, and binary-operation inference.

**New motifs in this batch**

**`vector_shadow_copy(object, marker8, marker9)`** — compute the displacement from marker 8 to marker 9 and stamp a second copy of the object at that offset. This is the core move in **M106**.

**`room_seed_fill(walls, seeds)`** — flood each room, detect whether it has exactly one seed, and if so fill the room with that seed color. This drives **M112**.

**`prototype_label_dispatch(prototypes, query)`** — compare a neutral query shape against labeled prototypes up to rotation and reflection, then recolor the query with the winning prototype’s label. This is the key abstraction in **H107**.

**`edit_stencil_transfer(example_before, example_after, query)`** — recover which cells were added in the example relative to the object’s bounding box, then replay that edit on a new object. This is the governing move in **H108**.

**`panel_mask_compose(mask, a, b)`** — build an output panel by selecting cells from panel A wherever the mask is active and from panel B elsewhere. This powers **H110**.

**`binary_op_infer(exampleA, exampleB, exampleC, queryD, queryE)`** — infer whether the example uses union, intersection, or xor on occupancy, then apply that same operation to a new pair. This is the central idea in **H112**.

## Easy

### E106 — Fill the vertical bridge

**What it tests:** Recognize same-color endpoints in a column and fill the zero cells between them.

**Staged hint:** Group cells by color. If a color appears exactly twice in one column with only zeros between them, fill that vertical span.

**Train 1 — input**

```text
0000000
7002000
0000000
0000000
7000000
0002000
0000000
```
**Train 1 — output**

```text
0000000
7002000
7002000
7002000
7002000
0002000
0000000
```
**Train 2 — input**

```text
00000000
00040000
00000000
03000000
00000000
03000000
00040000
00000000
```
**Train 2 — output**

```text
00000000
00040000
00040000
03040000
03040000
03040000
00040000
00000000
```
**Test — input**

```text
00000000
00000060
00000000
02000000
00000060
00000000
02000000
00000000
```
**Test — output**

```text
00000000
00000060
00000060
02000060
02000060
02000000
02000000
00000000
```
**Written solution:** For each color, find cases where it appears exactly twice in the same column and every cell between the two endpoints is 0. Fill the whole segment between those endpoints with that color and leave everything else unchanged.

**Program solution**

```python
def solve_E106(grid):
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

### E107 — Complete the 2x2 square

**What it tests:** Detect an L-shape of three equal cells inside a 2x2 box and fill the missing corner.

**Staged hint:** Scan every 2x2 window. If three cells share the same nonzero color and the fourth cell is 0, fill that missing corner.

**Train 1 — input**

```text
000000
022000
020000
000030
000330
000000
```
**Train 1 — output**

```text
000000
022000
022000
000330
000330
000000
```
**Train 2 — input**

```text
0000000
0000000
0044000
0004000
0000000
0070000
0077000
```
**Train 2 — output**

```text
0000000
0000000
0044000
0044000
0000000
0077000
0077000
```
**Test — input**

```text
0000000
0330000
0030000
0000000
0000200
0002200
0000000
```
**Test — output**

```text
0000000
0330000
0330000
0000000
0002200
0002200
0000000
```
**Written solution:** Look at every 2x2 block. Whenever exactly three cells in the block have the same nonzero color and the fourth is empty, complete the square by filling the empty cell with that color.

**Program solution**

```python
def solve_E107(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                color=nz[0]
                if grid[r][c]==0: out[r][c]=color
                if grid[r][c+1]==0: out[r][c+1]=color
                if grid[r+1][c]==0: out[r+1][c]=color
                if grid[r+1][c+1]==0: out[r+1][c+1]=color
    return out
```

### E108 — Fill the midpoint

**What it tests:** Spot two equal cells with one empty cell exactly between them horizontally or vertically.

**Staged hint:** Look for the pattern color-0-color in a straight line of length 3. Replace the middle 0 with that color.

**Train 1 — input**

```text
0000000
0404000
0000000
0000070
0000000
0000070
0000000
```
**Train 1 — output**

```text
0000000
0444000
0000000
0000070
0000070
0000070
0000000
```
**Train 2 — input**

```text
00000000
00000000
00303000
00000000
00000000
00050000
00000000
00050000
```
**Train 2 — output**

```text
00000000
00000000
00333000
00000000
00000000
00050000
00050000
00050000
```
**Test — input**

```text
0000000
0606000
0000000
0000000
0000400
0000000
0000400
```
**Test — output**

```text
0000000
0666000
0000000
0000000
0000400
0000400
0000400
```
**Written solution:** Whenever two equal nonzero cells are separated by exactly one empty cell in the same row or the same column, fill the midpoint with that color. Do this independently for every such triple.

**Program solution**

```python
def solve_E108(grid):
    out=clone(grid)
    h,w=dims(grid)
    # horizontal
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a!=0 and a==d and b==0:
                out[r][c+1]=a
    # vertical
    for r in range(h-2):
        for c in range(w):
            a,b,d=grid[r][c],grid[r+1][c],grid[r+2][c]
            if a!=0 and a==d and b==0:
                out[r+1][c]=a
    return out
```

### E109 — Grow each seed into a plus

**What it tests:** Apply the same local expansion around every singleton, including clipping at edges.

**Staged hint:** Treat each nonzero cell as the center of a radius-1 plus. Paint the center and its four orthogonal neighbors with the same color.

**Train 1 — input**

```text
0000000
0200000
0000000
0000000
0000060
0000000
0000000
```
**Train 1 — output**

```text
0200000
2220000
0200000
0000060
0000666
0000060
0000000
```
**Train 2 — input**

```text
0004000
0000000
0000000
0000000
0300000
0000000
0000000
```
**Train 2 — output**

```text
0044400
0004000
0000000
0300000
3330000
0300000
0000000
```
**Test — input**

```text
0000000
0000000
0050000
0000000
0000000
0000007
0000000
```
**Test — output**

```text
0000000
0050000
0555000
0050000
0000007
0000077
0000007
```
**Written solution:** For every nonzero seed, produce a plus of radius 1 in the same color: the seed itself plus the cells directly above, below, left, and right, as long as they stay inside the grid. Different pluses do not interact except by overwriting with the same color in these examples.

**Program solution**

```python
def solve_E109(grid):
    out=blank(*dims(grid))
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

### E110 — Reflect across the main diagonal

**What it tests:** Copy occupied cells to their transposed coordinates while keeping the originals.

**Staged hint:** For each colored cell at (r,c), also paint the cell at (c,r) with the same color.

**Train 1 — input**

```text
00020
00000
07000
00000
00000
```
**Train 1 — output**

```text
00020
00700
07000
20000
00000
```
**Train 2 — input**

```text
000000
004000
000000
000006
000000
200000
```
**Train 2 — output**

```text
000002
004000
040000
000006
000000
200600
```
**Test — input**

```text
000000
000300
000000
000000
700000
000000
```
**Test — output**

```text
000070
000300
000000
030000
700000
000000
```
**Written solution:** On this square grid, every nonzero cell is mirrored across the main diagonal. Keep the original cells and also fill their transposed positions with the same colors.

**Program solution**

```python
def solve_E110(grid):
    out=clone(grid)
    h,w=dims(grid)
    assert h==w
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                out[c][r]=v
    return out
```

### E111 — Extend each horizontal domino

**What it tests:** Recognize exact horizontal runs of length 2 and continue them by one more cell to the right.

**Staged hint:** Find nonzero runs of length exactly 2 in a row. If the cell immediately to the right is empty, fill it with the same color.

**Train 1 — input**

```text
0000000
0220000
0000000
0000000
0007700
0000000
```
**Train 1 — output**

```text
0000000
0222000
0000000
0000000
0007770
0000000
```
**Train 2 — input**

```text
00000000
00000000
00033000
00000000
50000000
05500000
00000000
00000000
```
**Train 2 — output**

```text
00000000
00000000
00033300
00000000
50000000
05550000
00000000
00000000
```
**Test — input**

```text
0000000
0000000
0440000
0000000
0000660
0000000
```
**Test — output**

```text
0000000
0000000
0444000
0000000
0000666
0000000
```
**Written solution:** Whenever a row contains an exact horizontal domino of one color, extend it by one additional cell to the right. Only true length-2 runs count; longer runs are ignored.

**Program solution**

```python
def solve_E111(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        c=0
        while c<w-1:
            v=grid[r][c]
            if v!=0 and c+1<w and grid[r][c+1]==v:
                left_same = c-1>=0 and grid[r][c-1]==v
                right_same = c+2<w and grid[r][c+2]==v
                if not left_same and not right_same and c+2<w and grid[r][c+2]==0:
                    out[r][c+2]=v
                c += 2
            else:
                c += 1
    return out
```

### E112 — Fill seeded columns

**What it tests:** Broadcast a seed color through its entire column.

**Staged hint:** If a column contains exactly one nonzero seed, fill the whole column with that seed’s color.

**Train 1 — input**

```text
0000000
0000060
0000000
0200000
0000000
0000000
0000000
```
**Train 1 — output**

```text
0200060
0200060
0200060
0200060
0200060
0200060
0200060
```
**Train 2 — input**

```text
00000000
00000000
00030000
00000000
00000000
00000000
70000000
00000000
```
**Train 2 — output**

```text
70030000
70030000
70030000
70030000
70030000
70030000
70030000
70030000
```
**Test — input**

```text
0000000
0000000
0004000
0000000
0000000
0000020
0000000
```
**Test — output**

```text
0004020
0004020
0004020
0004020
0004020
0004020
0004020
```
**Written solution:** Treat each column independently. Whenever a column has exactly one nonzero cell, use that cell’s color to fill the entire column. Other columns remain 0 in these examples.

**Program solution**

```python
def solve_E112(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c in range(w):
        cells=[grid[r][c] for r in range(h) if grid[r][c]!=0]
        if len(cells)==1:
            color=cells[0]
            for r in range(h):
                out[r][c]=color
    return out
```

## Medium

### M106 — Vector shadow copy

**What it tests:** Use two guide markers to compute a displacement and duplicate an object by that vector.

**Staged hint:** Find the displacement from marker 8 to marker 9. Keep the original object and stamp a translated copy using that same vector.

**Train 1 — input**

```text
00000800
04000000
04400090
00000000
00000000
00000000
00000000
00000000
```
**Train 1 — output**

```text
00000000
04000000
04400000
00400000
00440000
00000000
00000000
00000000
```
**Train 2 — input**

```text
000000000
000000000
000000000
000090000
000000000
080600000
000660000
000000000
```
**Train 2 — output**

```text
000000000
000000000
000000000
000000600
000000660
000600000
000660000
000000000
```
**Test — input**

```text
00000000
00000080
00090000
00000000
00000300
00000330
00000000
00000000
```
**Test — output**

```text
00000000
00000000
00000000
00000000
00000300
00300330
00330000
00000000
```
**Written solution:** Ignore the guide markers except as a displacement cue. Compute the vector from the 8-cell to the 9-cell, keep the original non-marker object, and add a second copy shifted by exactly that vector. The markers themselves disappear.

**Program solution**

```python
def solve_M106(grid):
    h,w=dims(grid)
    out=blank(h,w)
    src=dst=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==8:
                src=(r,c)
            elif grid[r][c]==9:
                dst=(r,c)
    assert src and dst
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and v not in (8,9):
                out[r][c]=v
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out
```

### M107 — Keep only border-touching objects

**What it tests:** Classify connected components by whether they touch the outer boundary.

**Staged hint:** Flood-fill each object. If any cell of that object touches the border, keep it and recolor it to 8; otherwise erase it.

**Train 1 — input**

```text
00000000
22000000
20000000
00033000
00030000
00000000
00000044
00000040
```
**Train 1 — output**

```text
00000000
88000000
80000000
00000000
00000000
00000000
00000088
00000080
```
**Train 2 — input**

```text
00000005
00000055
00000000
00330000
00030000
00000000
77000000
70000000
```
**Train 2 — output**

```text
00000008
00000088
00000000
00000000
00000000
00000000
88000000
80000000
```
**Test — input**

```text
00000000
00022000
00002000
00000000
00000000
00000300
66000300
60000000
```
**Test — output**

```text
00000000
00000000
00000000
00000000
00000000
00000000
88000000
80000000
```
**Written solution:** Find every connected nonzero object. If an object touches the outer edge of the grid anywhere, keep its shape but recolor all of its cells to 8. Remove all interior-only objects.

**Program solution**

```python
def solve_M107(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid, ignore=(0,), same_color=True):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=8
    return out
```

### M108 — Replace each object by its bounding-box frame

**What it tests:** Detect connected components, compute their bounding boxes, and draw only the box outlines.

**Staged hint:** For each object, find its tight bounding box. Erase the original interior structure and paint just the border of that box in the object’s color.

**Train 1 — input**

```text
00000000
02000000
02000000
02200000
00000070
00000077
00000000
00000000
```
**Train 1 — output**

```text
00000000
02200000
02200000
02200000
00000077
00000077
00000000
00000000
```
**Train 2 — input**

```text
000000000
000300000
000300000
000333000
000000000
060000000
066000000
060000000
000000000
```
**Train 2 — output**

```text
000000000
000333000
000303000
000333000
000000000
066000000
066000000
066000000
000000000
```
**Test — input**

```text
00000000
00400000
00400000
00440000
00000000
00000700
00000770
00000000
```
**Test — output**

```text
00000000
00440000
00440000
00440000
00000000
00000770
00000770
00000000
```
**Written solution:** Treat each connected component separately. Compute its minimal axis-aligned bounding box and output only the outline of that box, using the object’s original color. The original object cells are not preserved unless they lie on that outline.

**Program solution**

```python
def solve_M108(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid, ignore=(0,), same_color=True):
        r0,r1,c0,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
    return out
```

### M109 — Rotate the object around the anchor

**What it tests:** Use a designated pivot cell to rotate an entire object by 90 degrees clockwise.

**Staged hint:** Take every non-anchor object cell, convert its offset from the 9-anchor by (dr,dc)->(dc,-dr), and paint the rotated result.

**Train 1 — input**

```text
0000000
0000000
0020000
0022000
0090000
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
0000000
```
**Train 2 — input**

```text
0000000
0000000
0050900
0055000
0000000
0000000
```
**Train 2 — output**

```text
0005500
0005000
0000000
0000000
0000000
0000000
```
**Test — input**

```text
00000000
00000000
00004000
00004400
00009000
00000000
00000000
00000000
```
**Test — output**

```text
00000000
00000000
00000000
00000000
00000440
00000400
00000000
00000000
```
**Written solution:** The 9-cell is a pivot. Remove it, then rotate every other nonzero cell 90° clockwise around that pivot while preserving colors and relative shape.

**Program solution**

```python
def solve_M109(grid):
    h,w=dims(grid)
    out=blank(h,w)
    anchor=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    assert anchor
    ar,ac=anchor
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        nr,nc=ar+dc, ac-dr
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out
```

### M110 — Transplant the object into the frame

**What it tests:** Compute the object’s bounding box and move it so its top-left corner aligns with the frame interior.

**Staged hint:** Ignore the gray frame except for its interior top-left. Translate the whole colored object so its bbox top-left lands there, and erase the frame.

**Train 1 — input**

```text
00000000
03000000
03300000
00000000
00005555
00005005
00005005
00005555
```
**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00000000
00000300
00000330
00000000
```
**Train 2 — input**

```text
000055555
000050005
000050005
000050005
000055555
077000000
007000000
000000000
000000000
```
**Train 2 — output**

```text
000000000
000007700
000000700
000000000
000000000
000000000
000000000
000000000
000000000
```
**Test — input**

```text
000000000
000000000
044400000
004000000
000000000
000000555
000000505
000000505
000000555
```
**Test — output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
000000044
000000004
000000000
```
**Written solution:** There is one non-frame object and one hollow gray frame. Find the object’s tight bounding box, find the frame’s interior top-left cell, and translate the entire object so those two positions coincide. The frame itself disappears.

**Program solution**

```python
def solve_M110(grid):
    h,w=dims(grid)
    # frame cells are color 5
    frame_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==5]
    obj_cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,5)]
    assert frame_cells and obj_cells
    fr0,fr1,fc0,fc1=bbox([(r,c) for r,c in frame_cells])
    target=(fr0+1, fc0+1)
    or0,or1,oc0,oc1=bbox([(r,c) for r,c,v in obj_cells])
    out=blank(h,w)
    dr,dc=target[0]-or0, target[1]-oc0
    for r,c,v in obj_cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out
```

### M111 — Recolor objects by size rank

**What it tests:** Measure connected-component areas and map ranks to a fixed palette.

**Staged hint:** Find the three objects, sort them by area ascending, then recolor them as 2, 4, and 8 from smallest to largest.

**Train 1 — input**

```text
00000000
07000000
00000000
00033000
00000000
00000066
00000066
00000000
```
**Train 1 — output**

```text
00000000
02000000
00000000
00044000
00000000
00000088
00000088
00000000
```
**Train 2 — input**

```text
000000000
000000000
004400000
000000000
000700000
000770000
000000000
000000088
000000088
```
**Train 2 — output**

```text
000000000
000000000
002200000
000000000
000400000
000440000
000000000
000000088
000000088
```
**Test — input**

```text
00000000
00000000
05000000
00066000
00006000
00000000
00000077
00000077
```
**Test — output**

```text
00000000
00000000
02000000
00044000
00004000
00000000
00000088
00000088
```
**Written solution:** Compute the size of each connected object. Recolor the smallest object to 2, the middle-sized object to 4, and the largest object to 8. Leave all positions and shapes unchanged.

**Program solution**

```python
def solve_M111(grid):
    h,w=dims(grid)
    comps=connected_components(grid, ignore=(0,), same_color=True)
    assert len(comps)==3
    comps_sorted=sorted(comps, key=lambda x: len(x[1]))
    palette=[2,4,8]
    out=blank(h,w)
    for new_color, (_,cells) in zip(palette, comps_sorted):
        for r,c in cells:
            out[r][c]=new_color
    return out
```

### M112 — Fill each room from its unique seed

**What it tests:** Reason over wall-separated chambers instead of individual cells.

**Staged hint:** Flood-fill each non-wall room. If a room contains exactly one colored seed, fill the whole room with that seed’s color; empty rooms stay empty.

**Train 1 — input**

```text
555555555
520050005
500050005
555555555
500050305
500050005
555555555
```
**Train 1 — output**

```text
555555555
522250005
522250005
555555555
500053335
500053335
555555555
```
**Train 2 — input**

```text
555555555
500050405
500050005
555555555
500050005
205050005
555555555
```
**Train 2 — output**

```text
555555555
500054445
500054445
555555555
522250005
225250005
555555555
```
**Test — input**

```text
555555555
500050005
300050005
555555555
500050205
500050005
555555555
```
**Test — output**

```text
555555555
533350005
333350005
555555555
500052225
500052225
555555555
```
**Written solution:** Gray 5-cells are walls. Treat every connected non-wall region as a room. If a room contains exactly one nonzero seed, fill all its empty cells with that seed’s color. Rooms with no seeds stay empty in these examples.

**Program solution**

```python
def solve_M112(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); region=[]
            seeds=[]
            while q:
                x,y=q.popleft(); region.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append(grid[x][y])
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            uniq=set(seeds)
            if len(uniq)==1 and len(seeds)==1:
                color=next(iter(uniq))
                for x,y in region:
                    if grid[x][y]!=5:
                        out[x][y]=color
    return out
```

## Hard

### H106 — Infer the panel transform from an example pair

**What it tests:** Infer a dihedral transform from panel 1 → panel 2, then apply it to panel 3.

**Staged hint:** Try the small family of flips, rotations, and transposes. Find the one that turns the first panel into the second, then use that same transform on the third.

**Train 1 — input**

```text
00000500000500070
02000500220500070
02220500200500770
00000500200500000
00000500000500000
```
**Train 1 — output**

```text
00000
00000
00700
00777
00000
```
**Train 2 — input**

```text
00300500000500000
00330500000504400
00030500030500400
00000500330500400
00000500300500000
```
**Train 2 — output**

```text
00000
00400
00400
04400
00000
```
**Test — input**

```text
00000500000500000
06000506600500700
06600500660507700
00600500000507000
00000500000500000
```
**Test — output**

```text
00000
00770
07700
00000
00000
```
**Written solution:** Each input contains three square panels separated by gray columns. The second panel is a transformed version of the first, using one transform from a small dihedral family such as rotation, flip, or transpose. Identify that transform by comparing panel 1 to panel 2, then apply it to panel 3 and output only the transformed third panel.

**Program solution**

```python
def solve_H106(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3=split_panels_row(grid, n, 3, sep_color=5)
    name=infer_transform(p1,p2, candidates=["rot90","rot180","rot270","flip_h","flip_v","transpose","anti_transpose","id"])
    return TRANSFORMS[name](p3)
```

### H107 — Prototype label dispatch

**What it tests:** Match a query shape to one of two labeled prototypes up to rotation/reflection.

**Staged hint:** Ignore the label cell when comparing shapes. Normalize each prototype and the query by occupancy, test all dihedral variants, and recolor the query with the matching prototype’s label.

**Train 1 — input**

```text
20000570000500000
01000500100501100
01100501110501000
00000500000500000
00000500000500000
```
**Train 1 — output**

```text
00000
02200
02000
00000
00000
```
**Train 2 — input**

```text
30000580000500000
01100501000501110
00110501000501000
00000501100500000
00000500000500000
```
**Train 2 — output**

```text
00000
08880
08000
00000
00000
```
**Test — input**

```text
40000560000500000
01110500110501100
00100501100500110
00000501000500010
00000500000500000
```
**Test — output**

```text
00000
06600
00660
00060
00000
```
**Written solution:** The first two panels are labeled prototypes: the top-left cell gives the label color, and the rest of the nonzero cells define the prototype shape. The third panel is a query shape in a neutral color. Match the query to the correct prototype up to rotation or reflection, then recolor the query with that prototype’s label color.

**Program solution**

```python
def solve_H107(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3=split_panels_row(grid, n, 3, sep_color=5)
    label1, occ1 = panel_label_and_occ(p1)
    label2, occ2 = panel_label_and_occ(p2)
    _, query_occ = panel_label_and_occ(p3)
    q_transforms=set(all_occ_transforms(query_occ).values())
    if occ1 in q_transforms and occ2 not in q_transforms:
        label=label1
    elif occ2 in q_transforms and occ1 not in q_transforms:
        label=label2
    elif occ1 in q_transforms:
        label=label1
    elif occ2 in q_transforms:
        label=label2
    else:
        raise ValueError("no prototype match")
    out=blank(n,n)
    for r,row in enumerate(p3):
        for c,v in enumerate(row):
            if v!=0 and not (r==0 and c==0):
                out[r][c]=label
    return out
```

### H108 — Transfer the additive edit stencil

**What it tests:** Extract which cells were added in an example panel and replay that edit around a new object.

**Staged hint:** Compare before and after. Record the cells added in color 8 relative to the main object’s bounding box, then stamp those same relative additions onto the query object’s bounding box.

**Train 1 — input**

```text
00000500000500000
02200502280500000
02000502000500660
00000508000500600
00000500000500000
```
**Train 1 — output**

```text
00000
00000
00668
00600
00800
```
**Train 2 — input**

```text
00000500000500000
03330503330500000
00000500000507770
00000508080500000
00000500000500000
```
**Train 2 — output**

```text
00000
00000
07770
00000
08080
```
**Test — input**

```text
00000500000500000
05550505558566600
00500500500506000
00000508000500000
00000500000500000
```
**Test — output**

```text
00000
66680
06000
80000
00000
```
**Written solution:** The first panel shows an object before editing and the second shows the same object after extra 8-cells were added. Compute the added-cell stencil relative to the object’s bounding box, not in absolute coordinates. Then apply that same relative stencil to the query object in the third panel and output the edited query.

**Program solution**

```python
def solve_H108(grid):
    h,w=dims(grid)
    n=h
    before, after, query = split_panels_row(grid, n, 3, sep_color=5)
    (br0,br1,bc0,bc1), before_cells = main_object_bbox(before, ignore_colors=(0,8))
    # Added stencil = cells that are 8 in after but 0 in before
    added=[(r-br0,c-bc0) for r in range(n) for c in range(n) if after[r][c]==8 and before[r][c]==0]
    (qr0,qr1,qc0,qc1), query_cells = main_object_bbox(query, ignore_colors=(0,8))
    out=clone(query)
    for dr,dc in added:
        nr,nc=qr0+dr,qc0+dc
        if 0<=nr<n and 0<=nc<n:
            out[nr][nc]=8
    return out
```

### H109 — Orbit scaffold around the anchor

**What it tests:** Rotate a seed shape around a pivot and take the union of all four quarter-turns.

**Staged hint:** Treat the non-anchor shape as offsets from the 9-cell. Add the shape at 0°, 90°, 180°, and 270° around that anchor, then erase the anchor.

**Train 1 — input**

```text
0000000
0002200
0000000
0009000
0000000
0000000
0000000
```
**Train 1 — output**

```text
0000000
0002200
0200000
0200020
0000020
0022000
0000000
```
**Train 2 — input**

```text
0000000
0000000
0090600
0000600
0000000
0000000
0000000
```
**Train 2 — output**

```text
0066000
6000000
6000600
0000600
0660000
0000000
0000000
```
**Test — input**

```text
0000000
0000000
0000040
0009040
0000040
0000000
0000000
```
**Test — output**

```text
0000000
0044400
0400040
0400040
0400040
0044400
0000000
```
**Written solution:** Use the 9-cell as an anchor. Take every other nonzero cell, rotate its offset around the anchor through all four quarter-turns, and output the union of those rotated copies in the same color. The anchor itself is removed.

**Program solution**

```python
def solve_H109(grid):
    h,w=dims(grid)
    out=blank(h,w)
    anchor=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    ar,ac=anchor
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        for _ in range(4):
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
            dr,dc=dc,-dr
    return out
```

### H110 — Compose two panels through a mask

**What it tests:** Use one panel as a selector that chooses cell values from one of two source panels.

**Staged hint:** Where the mask panel is nonzero, copy the cell from panel A; where the mask is zero, copy the cell from panel B.

**Train 1 — input**

```text
00000500000577777
00800500200570007
08880502220570007
00800500200570007
00000500000577777
```
**Train 1 — output**

```text
77777
70207
72227
70207
77777
```
**Train 2 — input**

```text
00000533000566666
00800503300560006
08880500330560606
00800500033560006
00000500000566666
```
**Train 2 — output**

```text
66666
60306
60336
60006
66666
```
**Test — input**

```text
88000540004500077
88000504440500770
00880500400507700
00880504440570000
00000540004500000
```
**Test — output**

```text
40077
04770
07400
70440
00000
```
**Written solution:** The first panel is a binary mask. Build the output by taking the corresponding cell from the second panel wherever the mask is nonzero, and from the third panel wherever the mask is zero. Output only the composed panel.

**Program solution**

```python
def solve_H110(grid):
    h,w=dims(grid)
    n=h
    mask,a,b=split_panels_row(grid, n, 3, sep_color=5)
    out=blank(n,n)
    for r in range(n):
        for c in range(n):
            out[r][c]=a[r][c] if mask[r][c]!=0 else b[r][c]
    return out
```

### H111 — Roomwise nearest-seed fill with ties blank

**What it tests:** Do shortest-path nearest-seed filling inside wall-bounded rooms, leaving ties unresolved.

**Staged hint:** Flood each room separately. For every empty cell, compare shortest-path distances to the seeds in that same room. Fill with the unique nearest seed color; leave ties as 0.

**Train 1 — input**

```text
555555555
520000035
500000005
500500005
500000005
500000005
555555555
```
**Train 1 — output**

```text
555555555
522203335
522203335
522503335
522203335
522203335
555555555
```
**Train 2 — input**

```text
55555555555
54000050005
50000050005
50000050035
50000050005
50000050005
55555555555
```
**Train 2 — output**

```text
55555555555
54444453335
54444453335
54444453335
54444453335
54444453335
55555555555
```
**Test — input**

```text
55555555555
52000050005
50000050005
50000050035
50000050005
40000050005
55555555555
```
**Test — output**

```text
55555555555
52222253335
52222253335
52222253335
54444453335
44444453335
55555555555
```
**Written solution:** Gray 5-cells are walls. Inside each connected room of non-wall cells, colored seeds spread through shortest paths. Fill each empty cell with the color of its uniquely nearest seed within that room. If two different seeds are tied for nearest, leave that cell empty.

**Program solution**

```python
def solve_H111(grid):
    return geodesic_room_fill(grid)
```

### H112 — Infer the binary shape operation

**What it tests:** Infer whether the example panels use union, intersection, or xor, then apply that same operation to a new pair.

**Staged hint:** Compare panels 1 and 2 to panel 3. Test union, intersection, and xor on occupancy until one matches, then use it on panels 4 and 5.

**Train 1 — input**

```text
020050000502005000050000
022050022502025220050020
000050020500205020050220
000050000500005000050000
```
**Train 1 — output**

```text
0000
2220
0020
0000
```
**Train 2 — input**

```text
022050020500205000050200
022050020500205222050220
000050020500005022050220
000050000500005000050000
```
**Train 2 — output**

```text
0000
0220
0220
0000
```
**Test — input**

```text
020050000502005022050000
020050220502205020050220
000050000500005000050020
000050000500005000050000
```
**Test — output**

```text
0220
0220
0020
0000
```
**Written solution:** Each input contains five panels. The third panel is the result of applying one binary operation to the first two panels. Infer whether that operation is union, intersection, or xor of occupied cells, then apply the same operation to the fourth and fifth panels and output the result.

**Program solution**

```python
def solve_H112(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3,p4,p5=split_panels_row(grid,n,5,sep_color=5)
    op_name=None
    for name,fn in OPS.items():
        if fn(p1,p2)==p3:
            op_name=name
            break
    if op_name is None:
        raise ValueError("no binary op match")
    return OPS[op_name](p4,p5)
```
