# 21 More ARC-Style Puzzles

This is the twenty-second continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E148–E154, M148–M154, H148–H154**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans more into **header-driven emitters, stencil extraction, anchor-relative motion, transform analogy, support-delta transfer, embedded operation inference, family matching under symmetry, and transform-shadow unions**.

**New motifs in this batch**

**`anchor_rebase(shape, src, dst)`** — treat two special anchors as a translation instruction for one object. This is the core move in **M148**.

**`support_delta_transfer(A, B, C)`** — read where support was added or removed from A to B inside a bbox, then replay that edit on C. This is the central abstraction in **H149**.

**`embedded_op_dispatch(example_left, example_right, example_out, target_left, target_right)`** — identify an operation from an embedded example triplet and reuse it on a target pair. This drives **H152**.

**`family_match_under_symmetry(query, candidates)`** — choose the candidate whose support matches a query up to rotation or reflection, then recolor it. This is the heart of **H151**.

**`shadow_union_analogy(A, B, C)`** — infer a support transform from A→B, apply it to C, and union the transformed copy with the original. This appears in **H154**.

## Easy

### E148 — Top-row diagonal emitters

**What it tests:** Read the top row as colored seeds and extend each one down-right.


**Staged hint:** Start with the header only. Each nonzero top-row cell determines one diagonal and nothing else matters.


**Train 1 — input**

```text
0200400
0000000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0200400
0020040
0002004
0000200
0000020
```


**Train 2 — input**

```text
500700
000000
000000
000000
000000
000000
```

**Train 2 — output**

```text
500700
050070
005007
000500
000050
000005
```

**Test — input**

```text
00600300
00000000
00000000
00000000
00000000
```

**Test — output**

```text
00600300
00060030
00006003
00000600
00000060
```

**Written solution:** Ignore every row except the first. For each nonzero color in the top row, draw a diagonal of that same color starting at the marker and moving one step down and one step right until the grid edge. All other cells stay 0.


**Program solution**

```python

def solve_E148(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c,color in enumerate(grid[0]):
        if color!=0:
            k=0
            while k<h and c+k<w:
                out[k][c+k]=color
                k+=1
    return out

```

### E149 — Complete the missing corner of each 2×2 block

**What it tests:** Detect local 2×2 almost-squares and fill the lone empty corner.


**Staged hint:** Scan every 2×2 window independently. When you see three matching colored cells and one 0, you know exactly what to add.


**Train 1 — input**

```text
220030
200033
004400
004000
```

**Train 1 — output**

```text
220033
220033
004400
004400
```


**Train 2 — input**

```text
05500
05006
70066
77000
```

**Train 2 — output**

```text
05500
05566
77066
77000
```

**Test — input**

```text
800990
880900
004000
004400
```

**Test — output**

```text
880990
880990
004400
004400
```

**Written solution:** Look at every 2×2 block. If exactly three cells are the same nonzero color and the fourth cell is 0, fill that missing cell with the same color. Keep the rest of the grid unchanged.


**Program solution**

```python

def solve_E149(grid):
    h,w=dims(grid)
    out=clone(grid)
    fills=[]
    for r in range(h-1):
        for c in range(w-1):
            cells=[grid[r+i][c+j] for i in range(2) for j in range(2)]
            nz=[v for v in cells if v!=0]
            if len(nz)==3 and len(set(nz))==1 and cells.count(0)==1:
                idx=cells.index(0)
                dr,dc=divmod(idx,2)
                fills.append((r+dr,c+dc,nz[0]))
    for r,c,v in fills:
        out[r][c]=v
    return out

```

### E150 — Drop the whole shape to the bottom

**What it tests:** Move one object vertically until it first touches the lower border.


**Staged hint:** Treat all nonzero cells as one rigid shape. The task is only to find the largest safe downward shift.


**Train 1 — input**

```text
04000
44000
00000
00000
00000
```

**Train 1 — output**

```text
00000
00000
00000
04000
44000
```


**Train 2 — input**

```text
007000
077700
000000
000000
000000
000000
```

**Train 2 — output**

```text
000000
000000
000000
000000
007000
077700
```

**Test — input**

```text
0330000
0030000
0033000
0000000
0000000
0000000
```

**Test — output**

```text
0000000
0000000
0000000
0330000
0030000
0033000
```

**Written solution:** Take all nonzero cells together as one rigid object. Slide that object straight downward as far as possible without changing its shape or colors, stopping when its lowest cell lands on the bottom row.


**Program solution**

```python

def solve_E150(grid):
    h,w=dims(grid)
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    if not cells: return clone(grid)
    shift=(h-1)-max(r for r,c,v in cells)
    out=blank(h,w)
    for r,c,v in cells:
        out[r+shift][c]=v
    return out

```

### E151 — Keep only the key color

**What it tests:** Use the first visible nonzero cell as a global color key.


**Staged hint:** Find the first nonzero cell by reading order. Once you know that color, the rest is just filtering.


**Train 1 — input**

```text
300000
022030
020030
400000
440330
```

**Train 1 — output**

```text
300000
000030
000030
000000
000330
```


**Train 2 — input**

```text
70000
05070
55070
00000
70660
```

**Train 2 — output**

```text
70000
00070
00070
00000
70000
```

**Test — input**

```text
500000
025000
520060
000560
770000
```

**Test — output**

```text
500000
005000
500000
000500
000000
```

**Written solution:** Read the grid in normal top-left to bottom-right order and find the first nonzero cell. Its color is the key. Erase every other color and keep only cells of that key color.


**Program solution**

```python

def solve_E151(grid):
    h,w=dims(grid)
    key=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                key=grid[r][c]
                break
        if key is not None: break
    out=blank(h,w)
    if key is None: return out
    for r in range(h):
        for c in range(w):
            if grid[r][c]==key: out[r][c]=key
    return out

```

### E152 — Replace the object by its bounding-box frame

**What it tests:** Abstract an irregular object into the outline of its bounding rectangle.


**Staged hint:** Ignore the interior details of the shape. Only its extreme top, bottom, left, and right occupied cells matter.


**Train 1 — input**

```text
000000
044000
004000
044400
000000
```

**Train 1 — output**

```text
000000
044400
040400
044400
000000
```


**Train 2 — input**

```text
00000
00600
06660
00600
00600
```

**Train 2 — output**

```text
00000
06660
06060
06060
06660
```

**Test — input**

```text
0000000
0022000
0002000
0222200
0000000
```

**Test — output**

```text
0000000
0222200
0200200
0222200
0000000
```

**Written solution:** Find the smallest rectangle containing all nonzero cells. Output only the outline of that rectangle, using the original object color, and set every other cell to 0.


**Program solution**

```python

def solve_E152(grid):
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    if not cells: return clone(grid)
    r0,r1,c0,c1=bbox(cells)
    color=next(v for row in grid for v in row if v!=0)
    out=blank(*dims(grid))
    for c in range(c0,c1+1):
        out[r0][c]=color
        out[r1][c]=color
    for r in range(r0,r1+1):
        out[r][c0]=color
        out[r][c1]=color
    return out

```

### E153 — Compact each row to the left

**What it tests:** Perform rowwise nonzero compression while preserving order.


**Staged hint:** Handle one row at a time. Keep the nonzero sequence in the same order and push it flush left.


**Train 1 — input**

```text
020304
500006
000000
708090
```

**Train 1 — output**

```text
234000
560000
000000
789000
```


**Train 2 — input**

```text
00102
30040
05006
```

**Train 2 — output**

```text
12000
34000
56000
```

**Test — input**

```text
0400701
2000000
0030506
0000000
```

**Test — output**

```text
4710000
2000000
3560000
0000000
```

**Written solution:** For each row independently, remove the 0s and slide the remaining colors as far left as possible, keeping their left-to-right order unchanged. Fill the emptied cells on the right with 0s.


**Program solution**

```python

def solve_E153(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        vals=[v for v in row if v!=0]
        for i,v in enumerate(vals):
            out[r][i]=v
    return out

```

### E154 — Stamp a plus at every marker

**What it tests:** Expand single markers into clipped cardinal crosses.


**Staged hint:** Each nonzero cell acts like a center. Add its up, down, left, and right neighbors in the same color.


**Train 1 — input**

```text
00000
02000
00003
00000
40000
```

**Train 1 — output**

```text
02000
22203
02033
40003
44000
```


**Train 2 — input**

```text
005000
000000
000006
000000
070000
```

**Train 2 — output**

```text
055500
005006
000066
070006
777000
```

**Test — input**

```text
000000
080000
000090
000000
002000
000000
```

**Test — output**

```text
080000
888090
080999
002090
022200
002000
```

**Written solution:** Every nonzero cell becomes a plus shape made of the center cell and its four cardinal neighbors, clipped by the grid boundary. Draw all such pluses on an otherwise blank canvas.


**Program solution**

```python

def solve_E154(grid):
    h,w=dims(grid)
    out=blank(h,w)
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


## Medium

### M148 — Rebase the object from anchor 1 to anchor 2

**What it tests:** Read a translation vector from two special anchors and move a shape by that vector.


**Staged hint:** First find anchor 1 and anchor 2. Then treat every other nonzero cell as one object whose relative offsets from anchor 1 must be preserved around anchor 2.


**Train 1 — input**

```text
0000000
0150000
0550000
0000020
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0000000
0000005
0000055
0000000
```


**Train 2 — input**

```text
000000
000020
000000
077000
017000
000000
```

**Train 2 — output**

```text
000077
000007
000000
000000
000000
000000
```

**Test — input**

```text
0000000
0020000
0000000
0106600
0000600
0000000
```

**Test — output**

```text
0000000
0000660
0000060
0000000
0000000
0000000
```

**Written solution:** Locate the cell with color 1 and the cell with color 2. The vector from 1 to 2 defines how far the object should move. Translate every other nonzero cell by exactly that vector and output only the moved object.


**Program solution**

```python

def solve_M148(grid):
    h,w=dims(grid)
    src=dst=None
    obj=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==1: src=(r,c)
            elif v==2: dst=(r,c)
            elif v!=0: obj.append((r,c,v))
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    out=blank(h,w)
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out

```

### M149 — Infer the panel transform and apply it to the third panel

**What it tests:** Do per-instance transform analogy with three separated panels.


**Staged hint:** Compare the first two panels and name the geometric transform between them before touching the third panel.


**Train 1 — input**

```text
20080228033
22080208030
00080008000
```

**Train 1 — output**

```text
000
033
003
```


**Train 2 — input**

```text
04080408005
44080448055
40080048050
```

**Train 2 — output**

```text
500
550
050
```

**Test — input**

```text
60086608007
66080668077
06080008070
```

**Test — output**

```text
000
077
770
```

**Written solution:** Split the input into three panels separated by a full column of 8s. Determine which geometric transform turns panel A into panel B, then apply that same transform to panel C and output only the transformed C panel.


**Program solution**

```python

def solve_M149(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    for name,T in all_transforms(A).items():
        if T==B:
            return all_transforms(C)[name]
    raise ValueError("no transform match")

```

### M150 — Select the k-th largest component

**What it tests:** Use a header count to choose one object by size ranking.


**Staged hint:** Count the nonzero header markers first. Then sort the components in the body by area from largest to smallest.


**Train 1 — input**

```text
10000000
22000333
20000000
20044000
00000000
```

**Train 1 — output**

```text
22
20
20
```


**Train 2 — input**

```text
1100000
0555000
0500060
0500060
0007760
```

**Train 2 — output**

```text
6
6
6
```

**Test — input**

```text
11100000
88800000
80800900
88000900
00004444
00000000
```

**Test — output**

```text
9
9
```

**Written solution:** The number of nonzero cells in the top row gives k. Ignore that row, find all connected nonzero components in the body, sort them by size from largest to smallest, and output the k-th component cropped to its own bounding box.


**Program solution**

```python

def solve_M150(grid):
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    comps=cc(body, ignore=(0,), same_color=True)
    comps_sorted=sorted(comps, key=lambda t: (-len(t[1]), bbox(t[1])[0], bbox(t[1])[2]))
    color,cells=comps_sorted[k-1]
    return crop_component(body, cells)

```

### M151 — Use one panel as a stencil over another

**What it tests:** Combine aligned panels with masking and then crop the selected result.


**Staged hint:** Only positions that are nonzero in both panels survive. After that, crop tightly.


**Train 1 — input**

```text
00100800200
01100803400
00100800500
00000800000
00011800067
```

**Train 1 — output**

```text
0200
3400
0500
0000
0067
```


**Train 2 — input**

```text
10000890000
01000808000
00100800700
00000800000
00110800540
```

**Train 2 — output**

```text
9000
0800
0070
0000
0054
```

**Test — input**

```text
0010008004000
0111008056700
0010008008000
0000008000000
0001108000230
0000108000090
```

**Test — output**

```text
0400
5670
0800
0000
0023
0009
```

**Written solution:** Split the input into two aligned panels separated by a full 8-column. Use the left panel as a binary mask over the right panel: keep the right-panel color only where the left panel is nonzero. Then crop the surviving colored cells to their bounding box.


**Program solution**

```python

def solve_M151(grid):
    left,right = split_by_full_sep_cols(grid, sep=8)
    h,w=dims(left)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if left[r][c]!=0 and right[r][c]!=0:
                out[r][c]=right[r][c]
    return crop_bbox(out)

```

### M152 — Rotate the object clockwise around the 9-anchor

**What it tests:** Anchor-relative rotation with preserved colors.


**Staged hint:** Treat the 9 as a pivot. Convert object cells to offsets from that pivot, rotate the offsets, and place them back.


**Train 1 — input**

```text
0000000
0022000
0020000
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0000220
0009020
0000000
0000000
0000000
```


**Train 2 — input**

```text
000000
000400
000400
009440
000000
000000
```

**Train 2 — output**

```text
000000
000000
000000
009000
004440
004000
```

**Test — input**

```text
0000000
0000000
0330000
0039000
0030000
0000000
0000000
```

**Test — output**

```text
0000000
0000300
0033300
0009000
0000000
0000000
0000000
```

**Written solution:** Use the cell colored 9 as a rotation center. Rotate every other nonzero cell 90 degrees clockwise around that anchor, preserve its color, and keep the anchor itself unchanged.


**Program solution**

```python

def solve_M152(grid):
    h,w=dims(grid)
    anchor=None
    objs=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9: anchor=(r,c)
            elif v!=0: objs.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w)
    out[ar][ac]=9
    for r,c,v in objs:
        dr,dc = r-ar, c-ac
        nr,nc = ar+dc, ac-dr
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out

```

### M153 — Panel XOR overlay

**What it tests:** Compute an exclusive-or support merge across two aligned panels.


**Staged hint:** At each aligned cell, keep a color only if exactly one panel contributes a nonzero there.


**Train 1 — input**

```text
220082000
020080110
000080000
003080030
```

**Train 1 — output**

```text
0200
0010
0000
0000
```


**Train 2 — input**

```text
040080000
444080440
000080550
000080000
```

**Train 2 — output**

```text
0400
4000
0550
0000
```

**Test — input**

```text
600686000
060080060
000080000
007080007
```

**Test — output**

```text
0006
0660
0000
0077
```

**Written solution:** Split the input into two equal panels separated by a full 8-column. For each position, output the color from the unique nonzero panel if exactly one panel is nonzero there; otherwise output 0.


**Program solution**

```python

def solve_M153(grid):
    A,B = split_by_full_sep_cols(grid, sep=8)
    h,w=dims(A)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            av,bv=A[r][c], B[r][c]
            if (av!=0) ^ (bv!=0):
                out[r][c]=av if av!=0 else bv
    return out

```

### M154 — Recolor the gray region by nearest seed

**What it tests:** Partition a neutral shape by Manhattan distance to colored seeds.


**Staged hint:** Ignore the gray region's original color. Each gray cell just needs to know which seed is nearest.


**Train 1 — input**

```text
020000
055500
055503
055500
000000
```

**Train 1 — output**

```text
020000
022200
022303
022300
000000
```


**Train 2 — input**

```text
0004000
0055500
0055500
0700000
0000000
```

**Train 2 — output**

```text
0004000
0044400
0074400
0700000
0000000
```

**Test — input**

```text
0060000
0055550
0055550
0055558
0000000
```

**Test — output**

```text
0060000
0066680
0066880
0068888
0000000
```

**Written solution:** Treat color 5 as neutral material and every other nonzero cell as a colored seed. Recolor each gray cell with the color of the nearest seed by Manhattan distance, breaking ties by the stable reading-order rule implied by the examples, and preserve the seed cells.


**Program solution**

```python

def solve_M154(grid):
    h,w=dims(grid)
    seeds=[]; out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and v!=5:
                seeds.append((r,c,v))
                out[r][c]=v
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                best=min(seeds, key=lambda t: (abs(r-t[0])+abs(c-t[1]), t[2], t[0], t[1]))
                out[r][c]=best[2]
    return out

```


## Hard

### H148 — Infer both a transform and a color map

**What it tests:** Compose geometric analogy and color remapping inside a three-panel input.


**Staged hint:** Do not guess the output panel directly. First solve A→B as a transform plus palette map, then apply both to C.


**Train 1 — input**

```text
20080058023
23080658003
00080008000
```

**Train 1 — output**

```text
650
600
000
```


**Train 2 — input**

```text
44008000780040
06008002780660
00008000080000
00008000080000
```

**Train 2 — output**

```text
0000
0020
0027
0000
```

**Test — input**

```text
25088808052
20089008002
00080008000
```

**Test — output**

```text
000
900
880
```

**Written solution:** Split the grid into three panels separated by full 8-columns. Determine which geometric transform turns panel A into panel B and which color mapping is applied at the same time. Then transform panel C in the same geometric way and recolor it with the same map.


**Program solution**

```python

def solve_H148(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    for name,TA in all_transforms(A).items():
        if dims(TA)!=dims(B): continue
        mapping={}; ok=True
        for r in range(len(TA)):
            for c in range(len(TA[0])):
                a,b = TA[r][c], B[r][c]
                if a==0 and b==0: continue
                if (a==0)!=(b==0):
                    ok=False; break
                if a in mapping and mapping[a]!=b:
                    ok=False; break
                mapping[a]=b
            if not ok: break
        if ok:
            return recolor(all_transforms(C)[name], mapping)
    raise ValueError("no transform/color-map match")

```

### H149 — Transfer the support edit from A→B onto C

**What it tests:** Learn a relative add/delete edit inside one object's bounding box and replay it on another.


**Staged hint:** Crop the source object's bounding box mentally. Ask which relative cells were added and which were deleted, then replay that edit on the target object's bbox.


**Train 1 — input**

```text
22000822000800000
20000822000800055
00000800000800005
00000800000800000
00000800000800000
```

**Train 1 — output**

```text
00000
00055
00005
00000
00000
```


**Train 2 — input**

```text
00000800000800000
03300803300800000
03300800300800660
00000800000800660
00000800000800000
```

**Train 2 — output**

```text
00000
00000
00660
00060
00000
```

**Test — input**

```text
00000800000800000
04440804040800000
00400804440800707
00000800000800070
00000800000800000
```

**Test — output**

```text
00000
00000
00707
00777
00000
```

**Written solution:** Compare panels A and B. Inside A's bounding box, some relative positions become occupied and some become empty. Apply that same support edit, position by position, inside C's bounding box, using C's own color for added cells and 0 for removed ones.


**Program solution**

```python

def solve_H149(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    Acells=[(r,c) for r,row in enumerate(A) for c,v in enumerate(row) if v!=0]
    Ccells=[(r,c) for r,row in enumerate(C) for c,v in enumerate(row) if v!=0]
    if not Acells or not Ccells: return clone(C)
    ar0,ar1,ac0,ac1 = bbox(Acells)
    cr0,cr1,cc0,cc1 = bbox(Ccells)
    ah,aw = ar1-ar0+1, ac1-ac0+1
    ch,cw = cr1-cr0+1, cc1-cc0+1
    if (ah,aw)!=(ch,cw):
        raise ValueError("bbox mismatch")
    tcolor=dominant_nonzero_color([row[cc0:cc1+1] for row in C[cr0:cr1+1]])
    out=clone(C)
    for dr in range(ah):
        for dc in range(aw):
            a_non = A[ar0+dr][ac0+dc] != 0
            b_non = B[ar0+dr][ac0+dc] != 0
            if a_non and not b_non:
                out[cr0+dr][cc0+dc]=0
            elif (not a_non) and b_non:
                out[cr0+dr][cc0+dc]=tcolor
    return out

```

### H150 — Execute the transform token strip

**What it tests:** Interpret a row of symbolic operation tokens as a small program over a cropped shape.


**Staged hint:** Separate the token row from the body. Apply the geometric operations in order to the cropped body shape.


**Train 1 — input**

```text
1200
0500
0550
0000
```

**Train 1 — output**

```text
55
05
```


**Train 2 — input**

```text
43000
06600
00600
00600
00000
```

**Train 2 — output**

```text
666
600
```

**Test — input**

```text
21400
00700
07700
07000
00000
```

**Test — output**

```text
07
77
70
```

**Written solution:** The first row is a token program. Crop the nonzero shape in the rows below, then execute the tokens from left to right using the operation meanings revealed by the examples: rotate, flip, and transpose. Output the final transformed crop.


**Program solution**

```python

def solve_H150(grid):
    tokens=[v for v in grid[0] if v!=0]
    shape=crop_bbox([row[:] for row in grid[1:]])
    for t in tokens:
        if t==1: shape=rot90(shape)
        elif t==2: shape=flip_h(shape)
        elif t==3: shape=flip_v(shape)
        elif t==4: shape=transpose(shape)
        else: raise ValueError("unknown token")
    return shape

```

### H151 — Find the matching family under symmetry

**What it tests:** Use a query prototype to choose the one candidate component sharing its support up to symmetry.


**Staged hint:** Normalize the query support and compare it against every candidate under all flips and rotations.


**Train 1 — input**

```text
11084000550
01084400550
00080000000
```

**Train 1 — output**

```text
10
11
```


**Train 2 — input**

```text
02083300000
22283300600
00080006660
00080000000
00080000000
```

**Train 2 — output**

```text
020
222
```

**Test — input**

```text
770844000000
077804400000
000800000066
000800000660
000800000000
```

**Test — output**

```text
770
077
```

**Written solution:** Split the input into a small query panel and a candidate panel region. Find the candidate component whose support matches the query under some rotation or reflection. Output that candidate cropped to its bbox, but recolored to the query's color.


**Program solution**

```python

def solve_H151(grid):
    query,cands = split_by_full_sep_cols(grid, sep=8)
    qcolor=next(v for row in query for v in row if v!=0)
    qcrop=crop_bbox(query)
    qsupports={normalize_support(T) for T in all_transforms(qcrop).values()}
    comps=cc(cands, ignore=(0,), same_color=True)
    for color,cells in comps:
        cand_crop=crop_component(cands, cells)
        if normalize_support(cand_crop) in qsupports:
            return [[qcolor if v!=0 else 0 for v in row] for row in cand_crop]
    raise ValueError("no matching candidate")

```

### H152 — Infer the embedded binary operation and reuse it

**What it tests:** Discover union, intersection, or xor from an example triplet and apply it to a target pair.


**Staged hint:** Use the first three panels only to identify the operation family. Then run the same operation on the target pair.


**Train 1 — input**

```text
1108100804082208020
0108111840480208222
0008000800080008000
```

**Train 1 — output**

```text
200
202
000
```


**Train 2 — input**

```text
055080500805008066080600
555080550805508606080660
000080000800008000080000
000080000800008000080000
```

**Train 2 — output**

```text
0600
0060
0000
0000
```

**Test — input**

```text
700080700877008002080002
770080770877708022080022
000080000800008000080000
000080000800008000080000
```

**Test — output**

```text
0022
0222
0000
0000
```

**Written solution:** The input contains five panels: example left, example right, example output, target left, and target right. First determine which binary support operation makes the example output from the example inputs. Then apply that same operation to the target pair and output the result.


**Program solution**

```python

def solve_H152(grid):
    EA,EB,EO,TA,TB = split_by_full_sep_cols(grid, sep=8)
    opname=None
    ex_color=dominant_nonzero_color(EO)
    for name,fn in OPS.items():
        if fn(EA,EB,ex_color)==EO:
            opname=name
            break
    if opname is None: raise ValueError("no embedded operation match")
    tcolor=dominant_nonzero_color(TA)
    return OPS[opname](TA,TB,tcolor)

```

### H153 — Counted quarter-turn orbit around the anchor

**What it tests:** Use a header count to decide how many rotated copies of an object to union around a pivot.


**Staged hint:** Read k from the top row first. Then rotate the object's offsets around the 9-anchor through the first k quarter turns.


**Train 1 — input**

```text
110000
000000
009200
000200
000000
```

**Train 1 — output**

```text
000000
009200
022200
000000
```


**Train 2 — input**

```text
1110000
0000000
0009300
0003300
0000000
0000000
```

**Train 2 — output**

```text
0033000
0039300
0033300
0000000
0000000
```

**Test — input**

```text
1111000
0000000
0049000
0004000
0000000
0000000
```

**Test — output**

```text
0004000
0049400
0004000
0000000
0000000
```

**Written solution:** The number of nonzero header markers gives k. Ignore that header row after counting it. In the body, rotate the object's cells around the 9-anchor by successive quarter turns and union the first k orientations, keeping the anchor unchanged.


**Program solution**

```python

def solve_H153(grid):
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    h,w=dims(body)
    anchor=None; objs=[]
    for r in range(h):
        for c in range(w):
            v=body[r][c]
            if v==9: anchor=(r,c)
            elif v!=0: objs.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w); out[ar][ac]=9
    for r,c,v in objs:
        dr,dc=r-ar,c-ac
        pos=[(dr,dc),(dc,-dr),(-dr,-dc),(-dc,dr)]
        for idx in range(min(k,4)):
            rr,cc=pos[idx]
            nr,nc=ar+rr, ac+cc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

```

### H154 — Infer a support transform and shadow-union it with the target

**What it tests:** Read a pure support transform from A→B, apply it to C, then union transformed C with original C.


**Staged hint:** Treat A and B as a support-only analogy. Once you know the transform, copy it onto C and keep both original and transformed supports.


**Train 1 — input**

```text
20080028005
22080228055
00080008000
```

**Train 1 — output**

```text
505
555
000
```


**Train 2 — input**

```text
33080038006
03080338066
00080008060
```

**Train 2 — output**

```text
006
666
066
```

**Test — input**

```text
70087708009
77080708099
00080008090
```

**Test — output**

```text
009
099
990
```

**Written solution:** Determine which geometric transform turns panel A's support into panel B's support, ignoring color details. Apply that same transform to panel C, then union the transformed C with the original C in the same panel.


**Program solution**

```python

def solve_H154(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A_sup=[[1 if v!=0 else 0 for v in row] for row in A]
    B_sup=[[1 if v!=0 else 0 for v in row] for row in B]
    match=None
    for name,T in all_transforms(A_sup).items():
        if T==B_sup:
            match=name
            break
    if match is None: raise ValueError("no support transform match")
    TC=all_transforms(C)[match]
    out=clone(C)
    for r in range(len(C)):
        for c in range(len(C[0])):
            if TC[r][c]!=0:
                out[r][c]=TC[r][c]
    return out

```
