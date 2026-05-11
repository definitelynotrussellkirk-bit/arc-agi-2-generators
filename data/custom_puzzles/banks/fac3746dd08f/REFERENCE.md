# ARC Additional Puzzle Bank — 21 Puzzles (Set 15)

This fifteenth pack continues the numbering with **`E99–E105`**, **`M99–M105`**, and **`H99–H105`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
resolve_chambers(base_grid, wall_color, reducer, preserve_walls=True)
```

Intuition: partition a grid into wall-bounded chambers, inspect the markers inside each chamber, and paint each chamber according to a chamber-local rule. This primitive is used directly in **E99**, **M99**, and **H99**.

Design goals for this set:

- easy: chamber fills, local diagonal completion, row spans, rectangle outlines, color-directed extraction, diagonal symmetry, and coded translation

- medium: chamber aggregation, crop+rotate, size encoding, normalized overlap, equality matrices, ranked extraction, and motif broadcasting

- hard: patterned chamber fills, panel analogies, command-strip mosaics, hole-aware packing, rotation-invariant relations, anchor alignment, and combined color+transform analogies


## E99 — Chamber Seed Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** chamber partitioning, seed propagation, wall handling

**Suggested staged path:** Treat the wall color as hard boundaries first. Then solve each chamber independently from its one seed.

**Train 1 — input**

```text
5555555555
5200050305
5000050005
5555555555
5000050005
5040050605
5000050005
5555555555
```

**Train 1 — output**

```text
5555555555
5222253335
5222253335
5555555555
5444456665
5444456665
5444456665
5555555555
```

**Train 2 — input**

```text
55555555555
52050005065
50050405005
50050005005
55555555555
50050005005
57050805035
50050005005
55555555555
```

**Train 2 — output**

```text
55555555555
52254445665
52254445665
52254445665
55555555555
57758885335
57758885335
57758885335
55555555555
```

**Train 3 — input**

```text
5555555555
5200050305
5000050005
5555555555
5040050605
5000050005
5555555555
5000050005
5070050805
5555555555
```

**Train 3 — output**

```text
5555555555
5222253335
5222253335
5555555555
5444456665
5444456665
5555555555
5777758885
5777758885
5555555555
```

**Train 4 — input**

```text
5555555555555
5200504005065
5000500005005
5555555555555
5000500005005
5030507005085
5555555555555
```

**Train 4 — output**

```text
5555555555555
5222544445665
5222544445665
5555555555555
5333577775885
5333577775885
5555555555555
```

**Test — input**

```text
5555555555555
5200503050405
5555555555555
5060507050805
5000500050005
5555555555555
5000500050005
5090502050305
5555555555555
```

**Test — output**

```text
5555555555555
5222533354445
5555555555555
5666577758885
5666577758885
5555555555555
5999522253335
5999522253335
5555555555555
```

**Written solution**

The wall cells split the board into chambers. Each chamber contains exactly one colored seed; fill every non-wall cell in that chamber with that seed color.

**Reference program**

```python
def rule_e99(g):
    wall=5
    return resolve_chambers(g, wall, lambda cells, markers, grid: markers[0][2] if markers else 0)
```

## E100 — Diagonal Midpoint Completion

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local diagonal rule, midpoint inference, same-size

**Suggested staged path:** Look only at empty cells. An empty cell changes only when it sits exactly between two equal diagonal neighbors.

**Train 1 — input**

```text
00000000
04000000
00000020
00040000
00002000
00000000
00000070
00000000
```

**Train 1 — output**

```text
00000000
04000000
00400020
00040200
00002000
00000000
00000070
00000000
```

**Train 2 — input**

```text
000000000
000000030
000000000
000503000
000000000
000805000
000000000
080000000
000000000
```

**Train 2 — output**

```text
000000000
000000030
000000300
000503000
000050000
000805000
008000000
080000000
000000000
```

**Train 3 — input**

```text
0000000000
0600000040
0000000000
0006204000
0000000000
0000002000
0000000000
```

**Train 3 — output**

```text
0000000000
0600000040
0060000400
0006204000
0000020000
0000002000
0000000000
```

**Train 4 — input**

```text
00000000
00000000
00900000
00000000
00009000
00000700
00000200
00070000
00000002
00000000
```

**Train 4 — output**

```text
00000000
00000000
00900000
00090000
00009000
00000700
00007200
00070020
00000002
00000000
```

**Test — input**

```text
0000000000
0040000060
0000000000
0000406000
0000800000
0003000000
0000008000
0300000000
0000000000
```

**Test — output**

```text
0000000000
0040000060
0004000600
0000406000
0000800000
0003080000
0030008000
0300000000
0000000000
```

**Written solution**

Whenever two equal colored cells lie on a diagonal with one empty cell between them, copy that color into the midpoint.

**Reference program**

```python
def rule_e100(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            hits=[]
            if 0<r<h-1 and 0<c<w-1 and g[r-1][c-1]!=0 and g[r-1][c-1]==g[r+1][c+1]:
                hits.append(g[r-1][c-1])
            if 0<r<h-1 and 0<c<w-1 and g[r-1][c+1]!=0 and g[r-1][c+1]==g[r+1][c-1]:
                hits.append(g[r-1][c+1])
            hits=list(dict.fromkeys(hits))
            if len(hits)==1:
                out[r][c]=hits[0]
    return out
```

## E101 — Row Span Paint

**Difficulty:** easy

**Train pairs:** 4

**Skills:** segment completion, row-wise reasoning, same-size

**Suggested staged path:** Process one row at a time. The two colored endpoints on a row define the whole span.

**Train 1 — input**

```text
0000000000
0200020000
0000000000
0040000400
0000000000
7000000007
0000000000
```

**Train 1 — output**

```text
0000000000
0222220000
0000000000
0044444400
0000000000
7777777777
0000000000
```

**Train 2 — input**

```text
003000300
000000000
080080000
000000000
000000000
000000000
000500005
000000000
```

**Train 2 — output**

```text
003333300
000000000
088880000
000000000
000000000
000000000
000555555
000000000
```

**Train 3 — input**

```text
00000000000
40000000004
00000000000
00006006000
00200000020
00000000000
```

**Train 3 — output**

```text
00000000000
44444444444
00000000000
00006666000
00222222220
00000000000
```

**Train 4 — input**

```text
000000000000
000000000000
000700007000
000000000000
050000000050
000000000000
000000000000
900090000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000000
000777777000
000000000000
055555555550
000000000000
000000000000
999990000000
000000000000
```

**Test — input**

```text
0000000000
0400000040
0000000000
6000060000
0000000000
0000000000
0030000003
0000000000
```

**Test — output**

```text
0000000000
0444444440
0000000000
6666660000
0000000000
0000000000
0033333333
0000000000
```

**Written solution**

Each active row contains two endpoints of the same color. Fill every cell between those endpoints, inclusive, with that color.

**Reference program**

```python
def rule_e101(g):
    out=clone(g)
    h,w=size(g)
    for r in range(h):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        if len(positions)==1:
            color=list(positions.keys())[0]
            cols=positions[color]
            if len(cols)==2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c]=color
    return out
```

## E102 — Rectangle Outline from Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rectangle inference, corner markers, outline drawing

**Suggested staged path:** Ignore the empty background and treat each color separately. The four colored cells are the corners of one rectangle.

**Train 1 — input**

```text
0000000000
0200020000
0000000440
0000000000
0200020000
0000000000
0000000440
0000000000
```

**Train 1 — output**

```text
0000000000
0222220000
0200020440
0200020440
0222220440
0000000440
0000000440
0000000000
```

**Train 2 — input**

```text
000000000
060600000
000000000
000008080
000000000
000000000
000008080
060600000
000000000
```

**Train 2 — output**

```text
000000000
066600000
060600000
060608880
060608080
060608080
060608880
066600000
000000000
```

**Train 3 — input**

```text
000000007007
003003000000
000000000000
000000000000
000000007007
003003000000
000000000000
```

**Train 3 — output**

```text
000000007777
003333007007
003003007007
003003007007
003003007777
003333000000
000000000000
```

**Train 4 — input**

```text
0000000000
0000009009
0040400000
0000000000
0000000000
0000009009
0000000000
0000000000
0040400000
0000000000
```

**Train 4 — output**

```text
0000000000
0000009999
0044409009
0040409009
0040409009
0040409999
0040400000
0040400000
0044400000
0000000000
```

**Test — input**

```text
00000000000
02020000000
00000500050
00000000000
00000000000
00000000000
02020000000
00000500050
```

**Test — output**

```text
00000000000
02220000000
02020555550
02020500050
02020500050
02020500050
02220500050
00000555550
```

**Written solution**

For each color, the input marks the four corners of a rectangle. Draw that rectangle's outline in the same color.

**Reference program**

```python
def rule_e102(g):
    out=clone(g)
    by_color=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    out=blank(*size(g))
    for color,cells in by_color.items():
        if not cells:
            continue
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out
```

## E103 — Legend Color Crop

**Difficulty:** easy

**Train pairs:** 4

**Skills:** selection by code, cropping, object extraction

**Suggested staged path:** Read the top-left legend cell first. Then ignore every object whose color does not match it.

**Train 1 — input**

```text
4000000000
0000007700
0400007700
0400000000
0444000000
0000022200
0000000000
0000000000
```

**Train 1 — output**

```text
400
400
444
```

**Train 2 — input**

```text
600000000
000000880
066600880
006000000
006000000
000003000
000003300
000003330
000000000
```

**Train 2 — output**

```text
666
060
060
```

**Train 3 — input**

```text
20000000000
00000005000
00000005000
00220005550
00020000000
00022000000
00000099900
00000000000
```

**Train 3 — output**

```text
220
020
022
```

**Train 4 — input**

```text
7000000000
0000003330
0000000300
0000000300
0707000000
0707000000
0777000000
0000000220
0000000220
0000000000
```

**Train 4 — output**

```text
707
707
777
```

**Test — input**

```text
500000000000
000000003300
005000000300
005500000330
005550000000
000000000000
000000077700
000000000000
000000000000
```

**Test — output**

```text
500
550
555
```

**Written solution**

The top-left cell names the target color. Keep only cells of that color and crop the result to their bounding box.

**Reference program**

```python
def rule_e103(g):
    target=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and not (r==0 and c==0)]
    return crop_bbox(g, cells)
```

## E104 — Main-Diagonal Mirror

**Difficulty:** easy

**Train pairs:** 4

**Skills:** symmetry, reflection, square grids

**Suggested staged path:** Treat the main diagonal as the mirror line. Every colored cell should appear at the transposed position too.

**Train 1 — input**

```text
0000700
0002000
0000040
0000003
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000700
0002000
0000040
0200003
7000000
0040000
0003000
```

**Train 2 — input**

```text
00000600
00000020
00000008
00000400
00000000
00000000
00000000
00000000
```

**Train 2 — output**

```text
00000600
00000020
00000008
00000400
00000000
60040000
02000000
00800000
```

**Train 3 — input**

```text
000900
000050
000002
000000
000000
000000
```

**Train 3 — output**

```text
000900
000050
000002
900000
050000
002000
```

**Train 4 — input**

```text
000000002
000000030
000000007
000000400
000000000
000000000
000000000
000000000
000000000
```

**Train 4 — output**

```text
000000002
000000030
000000007
000000400
000000000
000000000
000400000
030000000
207000000
```

**Test — input**

```text
00000004
00000800
00000030
00000006
00000000
00000000
00000000
00000000
```

**Test — output**

```text
00000004
00000800
00000030
00000006
00000000
08000000
00300000
40060000
```

**Written solution**

Copy every colored cell across the main diagonal while keeping the originals. Empty transposed positions become the mirrored color.

**Reference program**

```python
def rule_e104(g):
    h,w=size(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and g[c][r]!=0:
                out[r][c]=g[c][r]
    return out
```

## E105 — One-Step Shift by Code

**Difficulty:** easy

**Train pairs:** 4

**Skills:** coded direction, translation, same-size

**Suggested staged path:** Separate the code cell from the object. The code is only a direction, not part of the moved shape.

**Train 1 — input**

```text
200000000
000000000
000000000
004000000
004000000
004440000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000000
000400000
000400000
000444000
000000000
000000000
```

**Train 2 — input**

```text
10000000
00000000
00000000
00000000
00066600
00006000
00006000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00000000
00066600
00006000
00006000
00000000
00000000
00000000
```

**Train 3 — input**

```text
3000000000
0000000000
0000022000
0000002000
0000002200
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000000000
0000000000
0000022000
0000002000
0000002200
0000000000
0000000000
```

**Train 4 — input**

```text
400000000
000000000
000000000
000000000
000077000
000077000
000000000
000000000
000000000
```

**Train 4 — output**

```text
000000000
000000000
000000000
000000000
000770000
000770000
000000000
000000000
000000000
```

**Test — input**

```text
2000000000
0000000000
0000000000
0050000000
0055000000
0055500000
0000000000
0000000000
0000000000
0000000000
```

**Test — output**

```text
0000000000
0000000000
0000000000
0005000000
0005500000
0005550000
0000000000
0000000000
0000000000
0000000000
```

**Written solution**

The top-left cell encodes a one-cell direction: 1 up, 2 right, 3 down, 4 left. Shift the whole object one step that way and remove the code.

**Reference program**

```python
def rule_e105(g):
    code=g[0][0]
    delta={1:(-1,0),2:(0,1),3:(1,0),4:(0,-1)}[code]
    out=blank(*size(g))
    h,w=size(g)
    dr,dc=delta
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if (r,c)==(0,0) or v==0:
                continue
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

## M99 — Chamber Max Selector

**Difficulty:** medium

**Train pairs:** 4

**Skills:** chamber partitioning, aggregation, wall handling

**Suggested staged path:** Again solve one chamber at a time. This time the chamber color is not a single seed position but the largest marker value inside it.

**Train 1 — input**

```text
5555555555
5270050305
5000050045
5555555555
5000050005
5040050105
5006050085
5555555555
```

**Train 1 — output**

```text
5555555555
5777754445
5777754445
5555555555
5666658885
5666658885
5666658885
5555555555
```

**Train 2 — input**

```text
55555555555
52050605065
50550405015
50050005005
55555555555
50050005005
57350805035
50050205095
55555555555
```

**Train 2 — output**

```text
55555555555
52256665665
52556665665
52256665665
55555555555
57758885995
57758885995
57758885995
55555555555
```

**Train 3 — input**

```text
5555555555
5200050305
5090050405
5555555555
5040050605
5005050015
5555555555
5008050305
5070050205
5555555555
```

**Train 3 — output**

```text
5555555555
5999954445
5999954445
5555555555
5444456665
5445456665
5555555555
5888853335
5888853335
5555555555
```

**Train 4 — input**

```text
5555555555555
5230504005065
5000508005705
5555555555555
5000500005405
5930507205085
5555555555555
```

**Train 4 — output**

```text
5555555555555
5333588885775
5333588885775
5555555555555
5999577775885
5999577775885
5555555555555
```

**Test — input**

```text
5555555555555
5240503950455
5555555555555
5060507050805
5010508050205
5555555555555
5000500050005
5093502750365
5555555555555
```

**Test — output**

```text
5555555555555
5444599954455
5555555555555
5666588858885
5666588858885
5555555555555
5999577756665
5999577756665
5555555555555
```

**Written solution**

The wall cells define chambers. In each chamber, inspect the colored markers already present and repaint the entire chamber with the largest color number found there.

**Reference program**

```python
def rule_m99(g):
    wall=5
    return resolve_chambers(g, wall, lambda cells, markers, grid: max(v for _,_,v in markers) if markers else 0)
```

## M100 — Commanded Crop Rotation

**Difficulty:** medium

**Train pairs:** 4

**Skills:** cropping, rotation, coded transform

**Suggested staged path:** First remove the code cell and crop the object. Only then apply the transform chosen by the code.

**Train 1 — input**

```text
100000000
000000000
000000000
000203000
000233000
000000000
000000000
000000000
```

**Train 1 — output**

```text
203
233
```

**Train 2 — input**

```text
2000000000
0000000000
0000000000
0000440000
0000045000
0000005000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
004
044
550
```

**Train 3 — input**

```text
30000000
00000000
00006000
00006700
00007700
00000000
00000000
00000000
```

**Train 3 — output**

```text
77
76
06
```

**Train 4 — input**

```text
4000000000
0000000000
0000000000
0000000000
0000000000
0022000000
0002300000
0000300000
0000000000
0000000000
```

**Train 4 — output**

```text
200
220
033
```

**Test — input**

```text
200000000
000000000
000000000
000000000
000808000
000080000
000000000
000000000
000000000
```

**Test — output**

```text
08
80
08
```

**Written solution**

Ignore the top-left command cell when finding the object. Crop the object's bounding box, then rotate it according to the code: 1 identity, 2 90°, 3 180°, 4 270°.

**Reference program**

```python
def rule_m100(g):
    code=g[0][0]
    g2=clone(g); g2[0][0]=0
    obj=crop_nonzero(g2)
    return transform_code(obj, code)
```

## M101 — Area-Sorted Color Strip

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component analysis, counting, sorting

**Suggested staged path:** Turn each object into two facts: its color and its area. The output is only a sorted one-dimensional encoding of those facts.

**Train 1 — input**

```text
000000000000
020000044000
020000044000
022200000000
000000000900
007770009900
000000009000
000000000000
```

**Train 1 — output**

```text
2222244449999777
```

**Train 2 — input**

```text
00000000000
03000000000
03300008880
03330000000
00000000000
06600000000
06600000000
00000000000
00000000000
```

**Train 2 — output**

```text
3333336666888
```

**Train 3 — input**

```text
0000000000000
0555000000000
0050000000000
0050000200000
0000000200000
0000000222990
0000000000990
0000000000000
```

**Train 3 — output**

```text
22222555559999
```

**Train 4 — input**

```text
000000000000
040400000000
040400000000
044400000000
000000002200
000000002200
077700000000
000000000000
000000000000
000000000000
```

**Train 4 — output**

```text
44444442222777
```

**Test — input**

```text
000000000000
006000003300
066600003300
006000000000
000000000002
000000000022
000008880020
000000000000
000000000000
```

**Test — output**

```text
6666622223333888
```

**Written solution**

Find each connected colored object, measure its area, sort objects from largest to smallest (breaking ties by color), and output a single row where each object's color is repeated by its area.

**Reference program**

```python
def rule_m101(g):
    comps=components_nonzero(g)
    items=[]
    for comp in comps:
        color=comp["color"]
        area=len(comp["cells"])
        items.append(( -area, color, area))
    items.sort()
    row=[]
    for neg_area,color,area in items:
        row.extend([color]*area)
    return [row] if row else [[0]]
```

## M102 — Normalized Overlap Overlay

**Difficulty:** medium

**Train pairs:** 4

**Skills:** shape normalization, overlay, set algebra

**Suggested staged path:** Forget the absolute positions. Crop both colored shapes to their own bounding boxes and align them at the same top-left origin.

**Train 1 — input**

```text
000000000000
020000000000
020000033300
022200003000
000000003000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
933
230
292
```

**Train 2 — input**

```text
00000000000
04000000000
04400000000
04440000000
00000077000
00000077000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
970
990
444
```

**Train 3 — input**

```text
000000000000
066000000000
006000000000
006600020000
000000020000
000000022200
000000000000
000000000000
```

**Train 3 — output**

```text
960
260
299
```

**Train 4 — input**

```text
000000000000
030300000000
030300000000
033300000000
000000000800
000000008880
000000000800
000000000000
000000000000
000000000000
```

**Train 4 — output**

```text
383
989
393
```

**Test — input**

```text
0000000000000
0000000000000
0050000000000
0550000000000
0500000002200
0000000002200
0000000000000
0000000000000
0000000000000
```

**Test — output**

```text
29
99
50
```

**Written solution**

Take the two colored shapes, normalize each to its own top-left bounding-box origin, and overlay them on one canvas. Cells belonging to both become 9; otherwise keep the single shape's color.

**Reference program**

```python
def rule_m102(g):
    colors=unique_colors(g)
    assert len(colors)==2
    c1,c2=colors
    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c1]
    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==c2]
    n1=normalize_cells(cells1); n2=normalize_cells(cells2)
    maxr=max([r for r,c in n1+n2]+[0]); maxc=max([c for r,c in n1+n2]+[0])
    out=blank(maxr+1, maxc+1)
    for r,c in n1:
        out[r][c]=c1
    for r,c in n2:
        out[r][c]=9 if out[r][c]!=0 else c2
    return out
```

## M103 — Shape Equality Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** object normalization, relational output, matrix construction

**Suggested staged path:** Read the components left to right. The output is not a transformed picture but a comparison table between their normalized shapes.

**Train 1 — input**

```text
0000000000000
0200070004440
0200070000400
0222077700400
0000000000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
880
880
008
```

**Train 2 — input**

```text
0000000000000000
0000000000000000
0330008880055000
0330000000055000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```

**Train 2 — output**

```text
808
080
808
```

**Train 3 — input**

```text
000000000000000
000000000000000
066000222009900
006000020000900
006600020000990
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
808
080
808
```

**Train 4 — input**

```text
00000000000000
00000000000000
00700040000200
07700040002200
07000044402000
00000000000000
00000000000000
00000000000000
```

**Train 4 — output**

```text
808
080
808
```

**Test — input**

```text
000000000000000000
000000000000000000
030300055000808000
030300055000808000
033300000000888000
000000000000000000
000000000000000000
000000000000000000
```

**Test — output**

```text
808
080
808
```

**Written solution**

List the disconnected objects from left to right and compare their shapes after normalizing away position and color. Output an N×N matrix with 8 wherever two normalized shapes are equal, else 0.

**Reference program**

```python
def rule_m103(g):
    comps=components_any_nonzero(g)
    comps=sorted(comps, key=lambda comp: bbox(comp["cells"])[1])  # left to right
    shapes=[normalize_binary_shape(comp["cells"]) for comp in comps]
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if shapes[i]==shapes[j]:
                out[i][j]=8
    return out
```

## M104 — Ranked Object Extraction

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component ranking, selection, cropping

**Suggested staged path:** Use the code cell only as a rank. After ranking objects by area, you only need one of them.

**Train 1 — input**

```text
10000000000000
00000000000000
02000004400000
02000004400000
02220000000000
00000000000000
00000000007770
00000000000000
00000000000000
```

**Train 1 — output**

```text
200
200
222
```

**Train 2 — input**

```text
20000000000000
00000000000000
03000000008880
03300000000000
03330000000000
00000000660000
00000000660000
00000000000000
00000000000000
```

**Train 2 — output**

```text
66
66
```

**Train 3 — input**

```text
300000000000000
000000000000000
050500020000000
050500020000000
055500022200000
000000000000000
000000000009900
000000000009900
000000000000000
000000000000000
```

**Train 3 — output**

```text
99
99
```

**Train 4 — input**

```text
2000000000000000
0000000000000000
0040000077000000
0444000077000000
0040000000000000
0000000000000000
0000000000002220
0000000000000000
0000000000000000
0000000000000000
```

**Train 4 — output**

```text
77
77
```

**Test — input**

```text
100000000000000
000000000000000
006000030000000
066000033000000
060000033300000
000000000000000
000000000008800
000000000008800
000000000000000
```

**Test — output**

```text
300
330
333
```

**Written solution**

The top-left cell gives a rank: 1 largest, 2 second largest, 3 third largest. Rank the disconnected objects by area and crop out the object at that rank.

**Reference program**

```python
def rule_m104(g):
    rank=g[0][0]
    g2=clone(g); g2[0][0]=0
    comps=components_nonzero(g2)
    comps=sorted(comps, key=lambda comp: (-len(comp["cells"]), bbox(comp["cells"])[1], comp["color"]))
    comp=comps[rank-1]
    return crop_bbox(g2, comp["cells"])
```

## M105 — Motif Recolor Broadcast

**Difficulty:** medium

**Train pairs:** 4

**Skills:** motif extraction, recoloring, sequence composition

**Suggested staged path:** Extract the source motif before looking at the command row. The bottom-row colors tell you how many recolored copies to emit and in what order.

**Train 1 — input**

```text
000000000
010100000
011100000
000000000
000000000
246000000
```

**Train 1 — output**

```text
20204040606
22204440666
```

**Train 2 — input**

```text
0000000000
0000000000
0011000000
0001100000
0000100000
0000000000
3580000000
```

**Train 2 — output**

```text
33005500880
03300550088
00300050008
```

**Train 3 — input**

```text
00000000
00010000
00011000
00011000
00000000
72490000
```

**Train 3 — output**

```text
70020040090
77022044099
77022044099
```

**Train 4 — input**

```text
00000000000
00000000000
01010000000
00100000000
00000000000
00000000000
68300000000
```

**Train 4 — output**

```text
60608080303
06000800030
```

**Test — input**

```text
0000000000
0000000000
0011000000
0001100000
0000100000
0000000000
4720000000
```

**Test — output**

```text
44007700220
04400770022
00400070002
```

**Written solution**

Crop the source motif from the upper part of the grid. For each nonzero color in the bottom row, make one recolored copy of the motif and place the copies side by side with a one-column gap.

**Reference program**

```python
def rule_m105(g):
    # top-left 3x3-ish motif color 1-ish? Actually any nonzero except bottom row commands
    h,w=size(g)
    commands=[v for v in g[h-1] if v!=0]
    base=[row[:] for row in g[:-1]]
    motif=crop_nonzero(base)
    mh,mw=size(motif)
    out=blank(mh, len(commands)*mw + max(0,len(commands)-1))
    cursor=0
    src_colors=[v for row in motif for v in row if v!=0]
    src_color=src_colors[0] if src_colors else 1
    for i,cmd in enumerate(commands):
        recolored=[[cmd if v!=0 else 0 for v in row] for row in motif]
        place_shape(out, recolored, 0, cursor)
        cursor += mw + 1
    return out
```

## H99 — Chamber Checker Weave

**Difficulty:** hard

**Train pairs:** 4

**Skills:** chamber partitioning, pattern fill, multi-seed reasoning

**Suggested staged path:** Partition into chambers first. Inside each chamber, reduce the markers to the smallest and largest colors, then use only those two to paint a local pattern.

**Train 1 — input**

```text
5555555555
5200050305
5070050065
5555555555
5000050005
5040050105
5008050095
5555555555
```

**Train 1 — output**

```text
5555555555
5272753635
5727256365
5555555555
5484851915
5848459195
5484851915
5555555555
```

**Train 2 — input**

```text
55555555555
52050405065
50550905085
50050005005
55555555555
50050005005
57050205015
50350805045
55555555555
```

**Train 2 — output**

```text
55555555555
52254945685
52559495865
52254945685
55555555555
53752825145
57358285415
53752825145
55555555555
```

**Train 3 — input**

```text
5555555555
5200050305
5090050405
5555555555
5040050605
5007050015
5555555555
5008050505
5070050205
5555555555
```

**Train 3 — output**

```text
5555555555
5292953435
5929254345
5555555555
5474751615
5747456165
5555555555
5787852525
5878752225
5555555555
```

**Train 4 — input**

```text
5555555555555
5200504005065
5030508005705
5555555555555
5900500005405
5030507205085
5555555555555
```

**Train 4 — output**

```text
5555555555555
5232548485675
5323584845765
5555555555555
5393527275485
5939572725845
5555555555555
```

**Test — input**

```text
5555555555555
5240503950455
5555555555555
5060507050805
5010508050205
5555555555555
5000500050005
5093502750365
5555555555555
```

**Test — output**

```text
5555555555555
5242539354455
5555555555555
5161578752825
5616587858285
5555555555555
5393527253635
5939572756365
5555555555555
```

**Written solution**

The wall cells define chambers. In each chamber, take the smallest and largest marker colors present there and fill the chamber with a checkerboard anchored at that chamber's top-left cell.

**Reference program**

```python
def rule_h99(g):
    wall=5
    def reducer(cells, markers, grid):
        colors=sorted({v for _,_,v in markers})
        if len(colors)<2:
            fill=colors[0] if colors else 0
            return {pos: fill for pos in cells}
        a,b=colors[0], colors[-1]
        r0,c0,_,_=bbox(cells)
        d={}
        for r,c in cells:
            d[(r,c)] = a if ((r-r0)+(c-c0))%2==0 else b
        return d
    return resolve_chambers(g, wall, reducer)
```

## H100 — Panel Transform Analogy

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, panel parsing

**Suggested staged path:** Split the three panels first. The first two tell you the transform; the third is just the same transform applied again.

**Train 1 — input**

```text
00000500000500000
01000501110501110
01000501000500100
01110501000500100
00000500000500000
```

**Train 1 — output**

```text
001
111
001
```

**Train 2 — input**

```text
00000500000500000
01100501100501000
00100500100501100
00110500110501110
00000500000500000
```

**Train 2 — output**

```text
100
110
111
```

**Train 3 — input**

```text
00000500000500000
00100501000501000
01100501100501000
01000500100501110
00000500000500000
```

**Train 3 — output**

```text
001
001
111
```

**Train 4 — input**

```text
00000500000500000
01110501000501100
00100501110501100
00100501000500000
00000500000500000
```

**Train 4 — output**

```text
11
11
```

**Test — input**

```text
00000500000500000
01000501110501100
01100501100500100
01110501000500110
00000500000500000
```

**Test — output**

```text
001
111
100
```

**Written solution**

The input contains three panels separated by full separator columns. Infer the geometric transform that maps panel A's cropped object to panel B's, then apply that same transform to panel C's cropped object.

**Reference program**

```python
def rule_h100(g):
    panels=split_panels_horizontal(g, sep_color=5)
    assert len(panels)==3
    A,B,C=panels
    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)
    tf=detect_transform(a,b)
    return apply_named_transform(c, tf)
```

## H101 — Sequential Transform Mosaic

**Difficulty:** hard

**Train pairs:** 4

**Skills:** command sequences, transform composition, dynamic output

**Suggested staged path:** Read the command strip separately from the motif. The output is simply a tiled replay of transformed motif variants in command order.

**Train 1 — input**

```text
123000
000000
010100
011100
000000
000000
```

**Train 1 — output**

```text
1010110111
1110100101
0000110000
```

**Train 2 — input**

```text
4120000
0000000
0011000
0001100
0000100
0000000
0000000
```

**Train 2 — output**

```text
10001100001
11000110011
01100010110
```

**Train 3 — input**

```text
2431000
0000000
0000000
0010000
0011000
0011000
0000000
```

**Train 3 — output**

```text
1110111011010
1100011011011
0000000001011
```

**Train 4 — input**

```text
32100000
00000000
00000000
00110000
00011000
00001000
00000000
00000000
```

**Train 4 — output**

```text
10000010110
11000110011
01101100001
```

**Test — input**

```text
4213000
0000000
0010100
0001000
0000000
0000000
0000000
```

**Test — output**

```text
1000101010010
0101000100101
1000100000000
```

**Written solution**

The top row is a sequence of transform codes and the lower part contains one source motif. Crop the motif and emit transformed copies in command order, separated by one blank column.

**Reference program**

```python
def rule_h101(g):
    commands=[v for v in g[0] if v!=0]
    base=[row[:] for row in g[1:]]
    motif=crop_nonzero(base)
    pieces=[]
    for cmd in commands:
        pieces.append(transform_code(motif, cmd))
    height=max(len(p) for p in pieces)
    width=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(height,width)
    cur=0
    for p in pieces:
        place_shape(out,p,0,cur)
        cur += len(p[0])+1
    return out
```

## H102 — Hole-Count Packing

**Difficulty:** hard

**Train pairs:** 4

**Skills:** topology, component sorting, packing

**Suggested staged path:** Do not sort by color or raw size first. Each object's number of holes is the primary key.

**Train 1 — input**

```text
0000000000000000
0220004440000000
0220004040000000
0000004440777770
0000000000707070
0000000000777770
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```

**Train 1 — output**

```text
220444077777
220404070707
000444077777
```

**Train 2 — input**

```text
000000000000000000
033300000000000000
030300000000000000
033300000008888000
000000000008008000
000000660008008000
000000660008888000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```

**Train 2 — output**

```text
66088880333
66080080303
00080080333
00088880000
```

**Train 3 — input**

```text
000000000000000000
055555000000000000
050505000000000000
055555000000000000
000000000000000000
000000000000000000
000000002220000000
000000002020000000
000000002220009900
000000000000009900
000000000000000000
000000000000000000
```

**Train 3 — output**

```text
990222055555
990202050505
000222055555
```

**Train 4 — input**

```text
00000000000000000
04444000000000000
04004000000000000
04004000000000000
04444000000022200
00000000000020200
00000007700022200
00000007700000000
00000000000000000
00000000000000000
```

**Train 4 — output**

```text
77044440222
77040040202
00040040222
00044440000
```

**Test — input**

```text
0000000000000000000
0660000000000000000
0660000000000000000
0000000033333000000
0000000030303000000
0000000033333000000
0000000000000000000
0000000000000008880
0000000000000008080
0000000000000008880
0000000000000000000
```

**Test — output**

```text
660888033333
660808030303
000888033333
```

**Written solution**

Crop each disconnected object, count how many enclosed holes it contains, then pack the cropped objects left to right in increasing hole count order, breaking ties by larger area first.

**Reference program**

```python
def rule_h102(g):
    comps=components_nonzero(g)
    items=[]
    for comp in comps:
        cropped=crop_bbox(g, comp["cells"])
        binary=[[1 if v!=0 else 0 for v in row] for row in cropped]
        holes=count_holes_binary(binary)
        area=len(comp["cells"])
        items.append((holes, -area, comp["color"], cropped))
    items.sort(key=lambda t:(t[0], t[1], t[2]))
    height=max(len(cropped) for _,_,_,cropped in items)
    width=sum(len(cropped[0]) for _,_,_,cropped in items)+(len(items)-1)
    out=blank(height,width)
    cur=0
    for _,_,_,cropped in items:
        place_shape(out,cropped,0,cur)
        cur += len(cropped[0])+1
    return out
```

## H103 — Rotation-Equivalence Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** rotation invariance, relational output, shape comparison

**Suggested staged path:** Normalize position and ignore color, but do not require exact orientation. Two objects match if one can become the other by quarter turns.

**Train 1 — input**

```text
000000000000000000
000000000000000000
020000077700044400
020000070000004000
022200070000004000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```

**Train 1 — output**

```text
770
770
007
```

**Train 2 — input**

```text
000000000000000000
000000000000000000
033300080000055000
000000080000055000
000000080000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```

**Train 2 — output**

```text
770
770
007
```

**Train 3 — input**

```text
00000000000000000000
00000000000000000000
06600000220000009000
00600000020000099000
00660000022000090000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Train 3 — output**

```text
770
770
007
```

**Train 4 — input**

```text
00000000000000000000
00000000000000000000
07000000044400002000
07700000004400002000
07770000000400002220
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Train 4 — output**

```text
770
770
007
```

**Test — input**

```text
000000000000000000
000000000000000000
033300000600000000
003000000600009900
003000006660009900
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```

**Test — output**

```text
770
770
007
```

**Written solution**

List the disconnected objects from left to right. Output an N×N matrix with 7 when two objects have the same shape up to rotation, and 0 otherwise.

**Reference program**

```python
def rule_h103(g):
    comps=components_any_nonzero(g)
    comps=sorted(comps, key=lambda comp: bbox(comp["cells"])[1])
    shapes=[]
    for comp in comps:
        cropped=crop_bbox(g, comp["cells"])
        shapes.append([[1 if v!=0 else 0 for v in row] for row in cropped])
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if equal_grid_up_to_rotation(shapes[i], shapes[j]):
                out[i][j]=7
    return out
```

## H104 — Anchor-Aligned Overlap

**Difficulty:** hard

**Train pairs:** 4

**Skills:** anchor alignment, overlay, special overlap color

**Suggested staged path:** Each object has one anchor cell of color 9. Align anchors first; only after that should you think about overlap colors.

**Train 1 — input**

```text
000000000000
090000000000
022000000000
002200000000
000000090000
000000060000
000000066600
000000000000
000000000000
```

**Train 1 — output**

```text
800
820
688
```

**Train 2 — input**

```text
0000000000000
0000000000000
0090000000000
0440000000000
0040000000000
0000000009000
0000000007700
0000000007000
0000000000000
0000000000000
```

**Train 2 — output**

```text
080
487
080
```

**Train 3 — input**

```text
00000000000000
00900000000000
00300000000000
00333000000000
00000000090000
00000000088000
00000000008800
00000000000000
00000000000000
```

**Train 3 — output**

```text
800
880
388
```

**Train 4 — input**

```text
000000000000
000000000000
000900000000
000550000000
000500000000
000000000000
000000009000
000000022000
000000002000
000000000000
```

**Train 4 — output**

```text
080
285
080
```

**Test — input**

```text
00000000000000
00090000000000
00044000000000
00004400000000
00000000000000
00000000009000
00000000007700
00000000007000
00000000000000
00000000000000
```

**Test — output**

```text
800
880
744
```

**Written solution**

Treat each connected object as having a single anchor cell colored 9. Translate both objects so their anchors coincide, then overlay them; cells claimed by both become 8.

**Reference program**

```python
def rule_h104(g):
    colors=unique_colors(g)
    # expect three colors: object1 color, object2 color, anchor 9 included in objects
    # components_any_nonzero over all nonzero regardless color; should yield 2 objects
    comps=components_any_nonzero(g)
    assert len(comps)==2
    overlays=[]
    colors_per=[]
    for comp in comps:
        cells=comp["cells"]
        # anchor cell color 9 inside component
        anchor=[(r,c) for r,c in cells if g[r][c]==9]
        assert len(anchor)==1
        ar,ac=anchor[0]
        rel=[(r-ar,c-ac,g[r][c]) for r,c in cells]
        overlays.append(rel)
    rs=[r for rel in overlays for r,c,v in rel]
    cs=[c for rel in overlays for r,c,v in rel]
    rshift=-min(rs); cshift=-min(cs)
    maxr=max(rs)+rshift; maxc=max(cs)+cshift
    out=blank(maxr+1,maxc+1)
    for rel in overlays:
        for r,c,v in rel:
            rr,cc=r+rshift,c+cshift
            if out[rr][cc]==0:
                out[rr][cc]=v
            else:
                out[rr][cc]=8
    return out
```

## H105 — Color+Transform Analogy

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, color remapping

**Suggested staged path:** The first two panels teach both the geometry change and the color change. Apply both lessons to the third panel.

**Train 1 — input**

```text
00000500000500000
02000507770504440
02000507000500400
02220507000500400
00000500000500000
```

**Train 1 — output**

```text
007
777
007
```

**Train 2 — input**

```text
00000500000500000
03300500880506000
00300500800506600
00330508800506660
00000500000500000
```

**Train 2 — output**

```text
008
088
888
```

**Train 3 — input**

```text
00000500000500000
04440500200507000
00400500200507000
00400502220507770
00000500000500000
```

**Train 3 — output**

```text
222
002
002
```

**Train 4 — input**

```text
00000500000500000
06000503330508800
06600503300500800
06660503000500880
00000500000500000
```

**Train 4 — output**

```text
003
333
300
```

**Test — input**

```text
00000500000500000
00700500440502200
07700504400502200
07000500000500000
00000500000500000
```

**Test — output**

```text
44
44
```

**Written solution**

Split the three panels. Infer the geometric transform from panel A to panel B and also the uniform recolor from A's nonzero color to B's; then apply both to panel C's cropped object.

**Reference program**

```python
def rule_h105(g):
    panels=split_panels_horizontal(g, sep_color=5)
    assert len(panels)==3
    A,B,C=panels
    a=crop_nonzero(A); b=crop_nonzero(B); c=crop_nonzero(C)
    # infer transform ignoring colors via binary support
    abinary=[[1 if v!=0 else 0 for v in row] for row in a]
    bbinary=[[1 if v!=0 else 0 for v in row] for row in b]
    tf=detect_transform(abinary, bbinary)
    a_colors=sorted({v for row in a for v in row if v!=0})
    b_colors=sorted({v for row in b for v in row if v!=0})
    # expect one nonzero color each
    src=a_colors[0]; dst=b_colors[0]
    transformed=apply_named_transform(c, tf)
    out=[[dst if v!=0 else 0 for v in row] for row in transformed]
    return out
```
