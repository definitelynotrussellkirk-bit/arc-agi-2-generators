# ARC Additional Puzzle Bank — 21 Puzzles (Set 20)

This twentieth pack continues the numbering with **`E134–E140`**, **`M134–M140`**, and **`H134–H140`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
pivot_rotate(cells, pivot, quarter_turns)
```

Intuition: treat a set of coordinates as a rigid motif around a known pivot, and rotate
that motif by 0, 90, 180, or 270 degrees without changing its internal colors. It is
used directly in **E134**, **M134**, and **H134**.

Design goals for this set:

- easy: pivot rotation, bounding boxes, reflection, span completion, cropping, centering, and seeded frame fills

- medium: multiple local rotations, component ranking, checker-frame filling, command-driven transforms, chamber ownership, pairwise shape comparison, and border-color panel selection

- hard: commanded local rotations, transform analogy, nested depth filling, Voronoi ownership, transform composition, relational area matrices, and select-then-transform behavior


## E134 — Pivot Around the Dot

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rigid rotation, pivot detection, coordinate transform

**Suggested staged path:** Ignore the color first and find the lone 8 pivot. Then treat every other nonzero cell as one rigid shape and rotate it one quarter-turn clockwise around that pivot.


**Train 1 — input**

```text
0000000
0000000
0004000
0048000
0040000
0000000
0000000
```


**Train 1 — output**

```text
0000000
0000000
0044000
0008400
0000000
0000000
0000000
```


**Train 2 — input**

```text
00000000
00000000
00000000
00060000
00068600
00000000
00000000
00000000
```


**Train 2 — output**

```text
00000000
00000000
00000000
00006600
00008000
00006000
00000000
00000000
```


**Train 3 — input**

```text
000000000
000000000
000000800
000003300
000003000
000000000
000000000
```


**Train 3 — output**

```text
000000000
000033000
000003800
000000000
000000000
000000000
000000000
```


**Train 4 — input**

```text
0000000
0000000
0000000
0070000
0077000
0080000
0000000
0000000
0000000
```


**Train 4 — output**

```text
0000000
0000000
0000000
0000000
0000000
0087700
0007000
0000000
0000000
```


**Test — input**

```text
000000000
000000000
000000000
000002000
000028000
000022000
000000000
000000000
```


**Test — output**

```text
000000000
000000000
000000000
000022000
000028200
000000000
000000000
000000000
```


**Written solution**

Find the unique 8 cell. Rotate every nonzero non-8 cell 90 degrees clockwise around it, preserving the original color and keeping the pivot unchanged.


**Reference program**

```python
def rule_e134(g):
    H,W=size(g)
    pivot=None
    cells=[]
    color=None
    for r in range(H):
        for c in range(W):
            v=g[r][c]
            if v==8:
                pivot=(r,c)
            elif v!=0:
                cells.append((r,c))
                color=v
    out=blank(H,W,0)
    pr,pc=pivot
    out[pr][pc]=8
    for r,c in pivot_rotate(cells,pivot,1):
        out[r][c]=color if color is not None else 1
    return out
```


## E135 — Draw the Missing Box

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bounding box, rectangle border inference, extremes

**Suggested staged path:** Do not follow the scattered cells individually. Just find the topmost, bottommost, leftmost, and rightmost nonzero cells and use them as the rectangle limits.


**Train 1 — input**

```text
00000000
00300000
00000300
00000000
00030000
00000000
00000000
```


**Train 1 — output**

```text
00000000
00333300
00300300
00300300
00333300
00000000
00000000
```


**Train 2 — input**

```text
00000000
00000000
06006000
00000000
00600000
00006000
00000000
00000000
```


**Train 2 — output**

```text
00000000
00000000
06666000
06006000
06006000
06666000
00000000
00000000
```


**Train 3 — input**

```text
0000000000
0000000400
0000000000
0004000000
0000000040
0000000000
```


**Train 3 — output**

```text
0000000000
0004444440
0004000040
0004000040
0004444440
0000000000
```


**Train 4 — input**

```text
0000000
0000000
0020000
0000020
0000000
0000200
0002000
0000000
0000000
```


**Train 4 — output**

```text
0000000
0000000
0022220
0020020
0020020
0020020
0022220
0000000
0000000
```


**Test — input**

```text
000000000
050000000
000000500
000000000
000000000
000500000
000000500
000000000
```


**Test — output**

```text
000000000
055555500
050000500
050000500
050000500
050000500
055555500
000000000
```


**Written solution**

Take the minimal bounding rectangle of the nonzero cells and draw the full rectangle border in the same color on an otherwise blank grid of the same size.


**Reference program**

```python
def rule_e135(g):
    H,W=size(g)
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    colors={g[r][c] for r,c in cells}
    color=next(iter(colors)) if colors else 1
    r0,c0,r1,c1=bbox(cells)
    out=blank(H,W,0)
    draw_frame(out,r0,c0,r1,c1,color)
    return out
```


## E136 — Mirror Across the Guide

**Difficulty:** easy

**Train pairs:** 4

**Skills:** axis detection, reflection, symmetry

**Suggested staged path:** Look for the full row or full column of 8s. That line is the mirror axis; every other colored cell gets copied to the reflected location on the opposite side.


**Train 1 — input**

```text
000080000
030080000
033080000
000080000
000080000
000080000
```


**Train 1 — output**

```text
000080000
030080030
033080330
000080000
000080000
000080000
```


**Train 2 — input**

```text
00000000
00000000
00000000
88888888
00000000
00550000
00050000
```


**Train 2 — output**

```text
00050000
00550000
00000000
88888888
00000000
00550000
00050000
```


**Train 3 — input**

```text
0000008000
0000008000
0020008000
0200008000
0020008000
0000008000
0000008000
0000008000
```


**Train 3 — output**

```text
0000008000
0000008000
0020008000
0200008000
0020008000
0000008000
0000008000
0000008000
```


**Train 4 — input**

```text
000000000
000000000
888888888
000000000
000004000
000004400
000000000
```


**Train 4 — output**

```text
000004000
000000000
888888888
000000000
000004000
000004400
000000000
```


**Test — input**

```text
00000800000
00000800000
00770800000
00070800000
00070800000
00000800000
00000800000
00000800000
```


**Test — output**

```text
00000800000
00000800000
00770807700
00070807000
00070807000
00000800000
00000800000
00000800000
```


**Written solution**

Detect the full guide line of 8s, then reflect every nonzero non-8 cell across that line and keep both the original and reflected copies.


**Reference program**

```python
def rule_e136(g):
    H,W=size(g)
    out=clone(g)
    full_rows=[r for r in range(H) if all(g[r][c]==8 for c in range(W))]
    full_cols=[c for c in range(W) if all(g[r][c]==8 for r in range(H))]
    if full_cols:
        axis=full_cols[0]
        for r in range(H):
            for c in range(W):
                v=g[r][c]
                if v not in (0,8):
                    mc=2*axis-c
                    if 0<=mc<W:
                        out[r][mc]=v
    else:
        axis=full_rows[0]
        for r in range(H):
            for c in range(W):
                v=g[r][c]
                if v not in (0,8):
                    mr=2*axis-r
                    if 0<=mr<H:
                        out[mr][c]=v
    return out
```


## E137 — Connect Matching Endpoints

**Difficulty:** easy

**Train pairs:** 4

**Skills:** span filling, row/column reasoning, color matching

**Suggested staged path:** Treat each row and column separately. Whenever a color appears exactly twice on a straight line with only blanks between them, fill the straight segment.


**Train 1 — input**

```text
000000000
000000040
030000300
000000000
000000000
000000040
000000000
```


**Train 1 — output**

```text
000000000
000000040
033333340
000000040
000000040
000000040
000000000
```


**Train 2 — input**

```text
00000000
00000000
00000000
00500500
00000000
06000060
00000000
00000000
```


**Train 2 — output**

```text
00000000
00000000
00000000
00555500
00000000
06666660
00000000
00000000
```


**Train 3 — input**

```text
000000000
002000000
000000700
000000000
000000000
000000000
000000700
002000000
000000000
```


**Train 3 — output**

```text
000000000
002000000
002000700
002000700
002000700
002000700
002000700
002000000
000000000
```


**Train 4 — input**

```text
0000000000
4000000040
0000300000
0000000000
0000000000
0000000000
0000300000
```


**Train 4 — output**

```text
0000000000
4444444440
0000300000
0000300000
0000300000
0000300000
0000300000
```


**Test — input**

```text
0000000000
0000000050
0000000000
0000000000
0060000600
0000000000
0000000050
0000000000
```


**Test — output**

```text
0000000000
0000000050
0000000050
0000000050
0066666650
0000000050
0000000050
0000000000
```


**Written solution**

For each row and each column, if a color occurs at exactly two endpoints with only zeros between them, fill the entire span with that color.


**Reference program**

```python
def rule_e137(g):
    H,W=size(g)
    out=clone(g)
    # rows
    for r in range(H):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        for color, cols in positions.items():
            if len(cols)==2:
                a,b=min(cols),max(cols)
                if all(g[r][cc] in (0,color) for cc in range(a,b+1)):
                    for cc in range(a,b+1):
                        out[r][cc]=color
    # cols
    for c in range(W):
        positions=defaultdict(list)
        for r in range(H):
            v=g[r][c]
            if v!=0:
                positions[v].append(r)
        for color, rows_ in positions.items():
            if len(rows_)==2:
                a,b=min(rows_),max(rows_)
                if all(g[rr][c] in (0,color) for rr in range(a,b+1)):
                    for rr in range(a,b+1):
                        out[rr][c]=color
    return out
```


## E138 — Crop the Tagged Window

**Difficulty:** easy

**Train pairs:** 4

**Skills:** corner markers, cropping, bbox extraction

**Suggested staged path:** Ignore the inside pattern at first and locate the four 9 corner tags. Their bounding box tells you exactly what to crop.


**Train 1 — input**

```text
000000000
009000900
000203000
000040000
009000900
000000000
000000000
000000000
```


**Train 1 — output**

```text
203
040
```


**Train 2 — input**

```text
0000000000
0000000000
0900090000
0055000000
0006600000
0000600000
0900090000
0000000000
0000000000
0000000000
```


**Train 2 — output**

```text
550
066
006
```


**Train 3 — input**

```text
00000000
00000000
00000000
00090090
00007000
00007800
00000800
00090090
00000000
```


**Train 3 — output**

```text
70
78
08
```


**Train 4 — input**

```text
000000000000
000090000900
000003302000
000000440000
000090000900
000000000000
000000000000
000000000000
```


**Train 4 — output**

```text
3302
0440
```


**Test — input**

```text
000000000
000000000
000000000
000000000
009000900
000600000
000677000
009000900
000000000
```


**Test — output**

```text
600
677
```


**Written solution**

Use the four 9s as the corners of a window and return the interior subgrid inside that rectangle, excluding the corner markers themselves.


**Reference program**

```python
def rule_e138(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0+1:c1] for row in g[r0+1:r1]]
```


## E139 — Center the Object Crop

**Difficulty:** easy

**Train pairs:** 4

**Skills:** cropping, centering, translation

**Suggested staged path:** First isolate the tight crop of the nonzero object. Then forget its original position and paste that crop back into the center of a blank grid of the same size.


**Train 1 — input**

```text
000000000
020300000
024000000
000000000
000000000
000000000
000000000
000000000
```


**Train 1 — output**

```text
000000000
000000000
000000000
000203000
000240000
000000000
000000000
000000000
```


**Train 2 — input**

```text
000000000
000000000
000000000
000000000
000000000
055000000
006600000
000000000
000000000
```


**Train 2 — output**

```text
000000000
000000000
000000000
000550000
000066000
000000000
000000000
000000000
000000000
```


**Train 3 — input**

```text
00000000
00007000
00007880
00000080
00000000
00000000
00000000
00000000
00000000
00000000
```


**Train 3 — output**

```text
00000000
00000000
00000000
00700000
00788000
00008000
00000000
00000000
00000000
00000000
```


**Train 4 — input**

```text
00000000000
00000000000
00000000000
00000000000
00000003330
00000000400
00000000000
```


**Train 4 — output**

```text
00000000000
00000000000
00003330000
00000400000
00000000000
00000000000
00000000000
```


**Test — input**

```text
0000020500
0000026500
0000000000
0000000000
0000000000
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
0002050000
0002650000
0000000000
0000000000
0000000000
0000000000
```


**Written solution**

Crop the minimal bounding box of all nonzero cells and place that crop centered in a blank grid with the original dimensions.


**Reference program**

```python
def rule_e139(g):
    H,W=size(g)
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    crop=crop_bbox(g,cells)
    h,w=size(crop)
    out=blank(H,W,0)
    r0=(H-h)//2; c0=(W-w)//2
    paste(out,crop,r0,c0,transparent=None)  # include zeros from crop? yes
    return out
```


## E140 — Seeded Frame Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** frame detection, interior fill, color transfer

**Suggested staged path:** Find the 8 frame and ignore everything outside it. The only other color inside tells you what the entire interior should become.


**Train 1 — input**

```text
000000000
008888800
008000800
008030800
008000800
008888800
000000000
000000000
```


**Train 1 — output**

```text
000000000
008888800
008333800
008333800
008333800
008888800
000000000
000000000
```


**Train 2 — input**

```text
0000000000
0000000000
0888880000
0800080000
0806080000
0800080000
0800080000
0888880000
0000000000
```


**Train 2 — output**

```text
0000000000
0000000000
0888880000
0866680000
0866680000
0866680000
0866680000
0888880000
0000000000
```


**Train 3 — input**

```text
00000000000
00000888880
00000804080
00000800080
00000800080
00000888880
00000000000
```


**Train 3 — output**

```text
00000000000
00000888880
00000844480
00000844480
00000844480
00000888880
00000000000
```


**Train 4 — input**

```text
000000000
000000000
000000000
008888880
008000080
008002080
008000080
008000080
008888880
000000000
```


**Train 4 — output**

```text
000000000
000000000
000000000
008888880
008222280
008222280
008222280
008222280
008888880
000000000
```


**Test — input**

```text
000000000000
000888888880
000800000080
000800000080
000800007080
000800000080
000888888880
000000000000
```


**Test — output**

```text
000000000000
000888888880
000877777780
000877777780
000877777780
000877777780
000888888880
000000000000
```


**Written solution**

Detect the rectangular 8 border and fill its entire interior with the single seed color found inside, leaving the frame unchanged.


**Reference program**

```python
def rule_e140(g):
    H,W=size(g)
    frame_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    r0,c0,r1,c1=bbox(frame_cells)
    seed_colors={g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]!=0}
    seed=next(iter(seed_colors)) if seed_colors else 1
    out=clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            out[r][c]=seed
    return out
```


## M134 — Many Pivot Rotations

**Difficulty:** medium

**Train pairs:** 4

**Skills:** object assignment, multiple pivots, rigid rotation

**Suggested staged path:** Split the scene into separate colored components and separate 8 pivots. Match each component to its nearest pivot, then rotate each one once clockwise.


**Train 1 — input**

```text
0000000000
0030000000
0380000000
0300000000
0000000000
0000005000
0000005850
0000000000
0000000000
```


**Train 1 — output**

```text
0000000000
0330000000
0083000000
0000000000
0000000000
0000000550
0000000800
0000000500
0000000000
```


**Train 2 — input**

```text
00000000000
00000000000
00020000000
00080000000
00022000000
00000000000
00000006600
00000006800
00000000000
00000000000
```


**Train 2 — output**

```text
00000000000
00000000000
00000000000
00282000000
00200000000
00000000000
00000000660
00000000860
00000000000
00000000000
```


**Train 3 — input**

```text
000000000000
000000004000
000000048000
000000040000
000000000000
000070000000
000870000000
000700000000
000000000000
```


**Train 3 — output**

```text
000000000000
000000044000
000000008400
000000000000
000000000000
000000000000
007800000000
000770000000
000000000000
```


**Train 4 — input**

```text
00000000000
00000000000
00000090000
00000098000
00000090000
00000000000
00000000000
00550000000
00850000000
00000000000
00000000000
```


**Train 4 — output**

```text
00000000000
00000000000
00000099900
00000008000
00000000000
00000000000
00000000000
00000000000
00850000000
00550000000
00000000000
```


**Test — input**

```text
000000000000
000600000000
006800000000
006000000000
000000000000
000000000000
000000004000
000000004800
000000000400
000000000000
```


**Test — output**

```text
000000000000
006600000000
000860000000
000000000000
000000000000
000000000000
000000000440
000000004800
000000000000
000000000000
```


**Written solution**

For each colored component, find the nearest 8 pivot and rotate that component 90 degrees clockwise around that pivot. Keep all pivots.


**Reference program**

```python
def rule_m134(g):
    H,W=size(g)
    pivots=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    comps=components_by_color(g, ignore={0,8})
    out=blank(H,W,0)
    for pr,pc in pivots:
        out[pr][pc]=8
    for comp in comps:
        cells=comp['cells']
        color=comp['color']
        pivot=min(pivots, key=lambda p: min(manhattan(p,cell) for cell in cells))
        for r,c in pivot_rotate(cells,pivot,1):
            out[r][c]=color
    return out
```


## M135 — Sort Crops by Area

**Difficulty:** medium

**Train pairs:** 4

**Skills:** components, area ranking, packing

**Suggested staged path:** Do not reason about absolute position. Crop each connected component tightly, measure its cell count, sort by area, and repack the crops left to right.


**Train 1 — input**

```text
000000000000
020000000000
020000000000
022000000000
000000044000
000000004400
006660000000
000600000000
000000000000
```


**Train 1 — output**

```text
2004400666
2000440060
2200000000
```


**Train 2 — input**

```text
0000000000000
0000000033000
0000000003000
0000000003300
0000000000000
0700000000000
0700005500000
0770005500000
0000005000000
0000000000000
```


**Train 2 — output**

```text
700330055
700030055
770033050
```


**Train 3 — input**

```text
00000000000
08880000000
00800000000
00000000000
00000220000
00000022000
00000000600
00000000600
00000000660
```


**Train 3 — output**

```text
2200600888
0220600080
0000660000
```


**Train 4 — input**

```text
000000000000
009900000000
009900000000
009000000000
000000044000
000000004000
000000004400
060000000000
060000000000
066000000000
```


**Train 4 — output**

```text
600440099
600040099
660044090
```


**Test — input**

```text
0000000000000
0550000000000
0055000000000
0000000777000
0000000070000
0003300000000
0003300000000
0003000000000
0000000000000
```


**Test — output**

```text
5500777033
0550070033
0000000030
```


**Written solution**

Extract each connected colored component as a tight crop, sort the crops by area ascending, and place them in one top-aligned row separated by a single blank column.


**Reference program**

```python
def rule_m135(g):
    comps=components_by_color(g, ignore={0})
    items=[]
    for comp in comps:
        sub=crop_bbox(g, comp['cells'])
        items.append((len(comp['cells']), comp['color'], sub))
    items.sort(key=lambda x:(x[0], x[1]))
    h=max(size(sub)[0] for _,_,sub in items)
    w=sum(size(sub)[1] for _,_,sub in items) + max(0,len(items)-1)
    out=blank(h,w,0)
    c0=0
    for _,_,sub in items:
        paste(out, sub, 0, c0, transparent=None)
        c0 += size(sub)[1] + 1
    return out
```


## M136 — Checker Frames

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame detection, checkerboard fill, local phase

**Suggested staged path:** Identify each hollow rectangle first. The interior marker color pairs with the border color to define a checkerboard inside that frame.


**Train 1 — input**

```text
000000000000
022220000000
025020000000
020020000000
022220000000
000000033330
000000036030
000000030030
000000033330
000000000000
```


**Train 1 — output**

```text
000000000000
022220000000
025220000000
022520000000
022220000000
000000033330
000000036330
000000033630
000000033330
000000000000
```


**Train 2 — input**

```text
0000000000000
0044444000000
0040004000000
0040704000000
0040004000000
0044444000000
0000000022220
0000000023020
0000000020020
0000000022220
0000000000000
```


**Train 2 — output**

```text
0000000000000
0044444000000
0047474000000
0044744000000
0047474000000
0044444000000
0000000022220
0000000023220
0000000022320
0000000022220
0000000000000
```


**Train 3 — input**

```text
00000000000000
06666600000000
06020600000000
06000600000000
06666600000000
00000000555550
00000000503050
00000000500050
00000000555550
00000000000000
```


**Train 3 — output**

```text
00000000000000
06666600000000
06262600000000
06626600000000
06666600000000
00000000555550
00000000535350
00000000553550
00000000555550
00000000000000
```


**Train 4 — input**

```text
000000000000
000000000000
077770000000
070070000000
074070000000
070070000000
077770333330
000000300030
000000302030
000000300030
000000333330
000000000000
```


**Train 4 — output**

```text
000000000000
000000000000
077770000000
074770000000
077470000000
074770000000
077770333330
000000323230
000000332330
000000323230
000000333330
000000000000
```


**Test — input**

```text
00000000000000
00055555000000
00050005000000
00050205000000
00050005000000
00055555000000
00000000044440
00000000046040
00000000040040
00000000044440
00000000000000
```


**Test — output**

```text
00000000000000
00055555000000
00052525000000
00055255000000
00052525000000
00055555000000
00000000044440
00000000046440
00000000044640
00000000044440
00000000000000
```


**Written solution**

For every rectangular border, use its border color and the single interior marker color to fill the interior with a checkerboard whose top-left interior cell takes the marker color.


**Reference program**

```python
def rule_m136(g):
    out=clone(g)
    frames, others = frame_components(g)
    for fr in frames:
        r0,c0,r1,c1 = fr['bbox']
        border_color = fr['color']
        marker_colors={g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,border_color)}
        marker=next(iter(marker_colors)) if marker_colors else 1
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c] = marker if (r-(r0+1)+c-(c0+1))%2==0 else border_color
    return out
```


## M137 — Commanded Crop Transform

**Difficulty:** medium

**Train pairs:** 4

**Skills:** symbol-to-transform mapping, cropping, rotation/reflection

**Suggested staged path:** The top-left command cell is not part of the motif. Crop the remaining nonzero motif, decode the command, and apply the indicated transform.


**Train 1 — input**

```text
100000000
000000000
000000000
002030000
002400000
000000000
000000000
000000000
```


**Train 1 — output**

```text
22
40
03
```


**Train 2 — input**

```text
2000000000
0000000000
0000000000
0000000000
0005060000
0000760000
0000700000
0000000000
0000000000
```


**Train 2 — output**

```text
070
670
605
```


**Train 3 — input**

```text
30000000000
00000000000
00000020000
00000034000
00000004500
00000000000
00000000000
00000000000
```


**Train 3 — output**

```text
002
043
540
```


**Train 4 — input**

```text
4000000000
0000000000
0000000000
0000000000
0000000000
0023000000
0004500000
0000500000
0000000000
0000000000
```


**Train 4 — output**

```text
200
340
055
```


**Test — input**

```text
100000000000
000000000000
000000000000
000000000000
000000060700
000000068000
000000008900
000000000000
000000000000
```


**Test — output**

```text
066
880
907
```


**Written solution**

Read the command in the top-left cell, crop the rest of the nonzero motif, and transform the crop: 1=rotate90, 2=rotate180, 3=flip horizontally, 4=transpose.


**Reference program**

```python
def rule_m137(g):
    cmd=g[0][0]
    g2=clone(g)
    g2[0][0]=0
    motif=crop_bbox(g2)
    return apply_transform(motif, {1:1,2:2,3:3,4:5}[cmd])  # 4->transpose
```


## M138 — Chamber Ownership Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** flood fill, region ownership, wall parsing

**Suggested staged path:** Treat the 8s as walls and flood the non-wall chambers. If a chamber contains exactly one nonzero color, that color owns the whole chamber.


**Train 1 — input**

```text
88888888888
80000800008
80200803008
80000800008
88888888888
80000800008
80000800408
80000800008
88888888888
```


**Train 1 — output**

```text
88888888888
82222833338
82222833338
82222833338
88888888888
80000844448
80000844448
80000844448
88888888888
```


**Train 2 — input**

```text
888888888888
800080000008
805080200008
800080000008
800080008008
888888888888
800080008008
800080008078
800080008008
888888888888
```


**Train 2 — output**

```text
888888888888
855582222228
855582222228
855582222228
855582228228
888888888888
800080008778
800080008778
800080008778
888888888888
```


**Train 3 — input**

```text
8888888888888
8000008000008
8030008000008
8888888888888
8000008060008
8000008000008
8000008888888
8000008000208
8888888888888
```


**Train 3 — output**

```text
8888888888888
8333338000008
8333338000008
8888888888888
8000008666668
8000008666668
8000008888888
8000008222228
8888888888888
```


**Train 4 — input**

```text
88888888888
80000800008
80400800608
80000800008
80000800008
88888888888
80000800008
80000800008
80300800508
80000800008
88888888888
```


**Train 4 — output**

```text
88888888888
84444866668
84444866668
84444866668
84444866668
88888888888
83333855558
83333855558
83333855558
83333855558
88888888888
```


**Test — input**

```text
88888888888888
80008000080008
80208000080008
80008000080008
80008000080008
88888888888888
80008000080008
80008040080708
80008000080008
88888888888888
```


**Test — output**

```text
88888888888888
82228000080008
82228000080008
82228000080008
82228000080008
88888888888888
80008444487778
80008444487778
80008444487778
88888888888888
```


**Written solution**

Partition the grid into non-8 chambers. Any chamber containing exactly one nonzero color is filled entirely with that color while walls remain unchanged.


**Reference program**

```python
def rule_m138(g):
    out=clone(g)
    for reg in flood_regions_not8(g):
        colors={g[r][c] for r,c in reg if g[r][c] not in (0,8)}
        if len(colors)==1:
            fill=next(iter(colors))
            for r,c in reg:
                if g[r][c]!=8:
                    out[r][c]=fill
    return out
```


## M139 — Shape Equality Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** panel parsing, shape normalization, pairwise comparison

**Suggested staged path:** Split the input into panels using the full 8 separator columns. Ignore color and translation, reduce each panel to a normalized shape mask, then compare every pair.


**Train 1 — input**

```text
00000800000800000
02000800500800000
02000800500803300
02200800550800330
00000800000800000
```


**Train 1 — output**

```text
110
110
001
```


**Train 2 — input**

```text
00000800000800000
04440806600804440
00400800600800400
00000800660800000
00000800000800000
```


**Train 2 — output**

```text
101
010
101
```


**Train 3 — input**

```text
00000800000800000
07700802000807700
07700802000807700
07000802200807000
00000800000800000
```


**Train 3 — output**

```text
101
010
101
```


**Train 4 — input**

```text
00000800000800000
00000806600800000
03300800600803300
00330800660800330
00000800000800000
```


**Train 4 — output**

```text
101
010
101
```


**Test — input**

```text
00000800000800000
00500804440806600
00500800400800600
00550800000800660
00000800000800000
```


**Test — output**

```text
100
010
001
```


**Written solution**

Separate the three panels, crop each object to a translation-invariant binary mask, and output a 3x3 matrix with 1 where two masks are equal and 0 otherwise.


**Reference program**

```python
def rule_m139(g):
    panels=panel_split_by_full8_cols(g)
    masks=[canonical_mask(p, ignore={0}) for p in panels]
    n=len(masks)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            out[i][j]=1 if masks[i]==masks[j] else 0
    return out
```


## M140 — Select Panel by Border

**Difficulty:** medium

**Train pairs:** 4

**Skills:** panel selection, border-color lookup, cropping

**Suggested staged path:** The lone outside cell is a selector, not part of any panel. Match its color to a panel border and return that panel’s interior.


**Train 1 — input**

```text
30000000000000
00000000000000
00777700333330
00720700344030
00723700305530
00777700300030
00000000333330
00000000000000
00000000000000
00000000000000
```


**Train 1 — output**

```text
440
055
000
```


**Train 2 — input**

```text
500000000000000
000000000000000
000555550000000
000560050044440
000506050042040
000500050042340
000555550040040
000000000044440
000000000000000
000000000000000
000000000000000
```


**Train 2 — output**

```text
600
060
000
```


**Train 3 — input**

```text
40000000000000000
00000000000000000
00333330004444440
00377730004606040
00308030004020040
00300030004444440
00333330000000000
00000000000000000
00000000000000000
00000000000000000
```


**Train 3 — output**

```text
6060
0200
```


**Train 4 — input**

```text
200000000000000
000000000000000
000000000000000
002222200000000
002440200666660
002055200660060
002000200606060
002222200600060
000000000666660
000000000000000
000000000000000
000000000000000
```


**Train 4 — output**

```text
440
055
000
```


**Test — input**

```text
60000000000000000
00000000000000000
00005555500000000
00005200500666660
00005230500677760
00005000500608060
00005555500600060
00000000000600060
00000000000600060
00000000000666660
00000000000000000
00000000000000000
```


**Test — output**

```text
777
080
000
000
000
```


**Written solution**

Find the outside selector color, choose the framed panel with the same border color, and output the interior of that panel without its border.


**Reference program**

```python
def rule_m140(g):
    selector=None
    frames, others=frame_components(g)
    frame_cell_set={cell for fr in frames for cell in fr['cells']}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and (r,c) not in frame_cell_set:
                # not inside any frame border? could be motif inside frame; need outside all frame bboxes
                inside=False
                for fr in frames:
                    r0,c0,r1,c1=fr['bbox']
                    if r0<=r<=r1 and c0<=c<=c1:
                        inside=True; break
                if not inside:
                    selector=v
                    break
        if selector is not None:
            break
    chosen=[fr for fr in frames if fr['color']==selector][0]
    r0,c0,r1,c1=chosen['bbox']
    return [row[c0+1:c1] for row in g[r0+1:r1]]
```


## H134 — Commanded Pivot Rotations

**Difficulty:** hard

**Train pairs:** 4

**Skills:** multiple local commands, rigid rotation, group assignment

**Suggested staged path:** Break the task into local pivot groups. For each 8 pivot, read the command color immediately to its left, attach the nearest component, and rotate by that many quarter turns.


**Train 1 — input**

```text
000000000000
000000000000
000200000000
002800000000
002000000000
000000000000
000000050000
000000058500
000000000000
000000000000
```


**Train 1 — output**

```text
000000000000
000000000000
000020000000
000820000000
000200000000
000000000000
000000050000
000000058500
000000000000
000000000000
```


**Train 2 — input**

```text
0000000000000
0000000000000
0000000004000
0000000048000
0000000040000
0000000000000
0000000000000
0000070000000
0001870000000
0000700000000
0000000000000
```


**Train 2 — output**

```text
0000000000000
0000000000000
0000000004000
0000000048000
0000000040000
0000000000000
0000000000000
0000000000000
0007800000000
0000770000000
0000000000000
```


**Train 3 — input**

```text
00000000000000
00006000000000
00068000000000
00060000000000
00000000000000
00000000000000
00000000030000
00000000038000
00000000003000
00000000000000
```


**Train 3 — output**

```text
00000000000000
00006000000000
00068000000000
00060000000000
00000000000000
00000000000000
00000000000000
00000000008300
00000000033000
00000000000000
```


**Train 4 — input**

```text
000000000000
000000000000
000900000000
000990000000
001800000000
000000000000
000000000000
000000020000
000000028000
000000020000
000000000000
000000000000
```


**Train 4 — output**

```text
000000000000
000000000000
000000000000
000000000000
000899000000
000090000000
000000000000
000000000200
000000008200
000000000200
000000000000
000000000000
```


**Test — input**

```text
00000000000000
00000000000000
00000500000000
00005800000000
00005000000000
00000000000000
00000000000000
00000000007000
00000000018700
00000000000700
00000000000000
```


**Test — output**

```text
00000000000000
00000000000000
00000500000000
00005800000000
00005000000000
00000000000000
00000000000000
00000000000000
00000000008700
00000000077000
00000000000000
```


**Written solution**

Each pivot has a command cell just to its left. Match each colored component to its nearest pivot and rotate it clockwise by the command value in quarter-turns, keeping only pivots and rotated components.


**Reference program**

```python
def rule_h134(g):
    H,W=size(g)
    pivots=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    comps=components_by_color(g, ignore={0,1,8})
    out=blank(H,W,0)
    for pr,pc in pivots:
        out[pr][pc]=8
        # keep command cell(s) of 1,2,3? We use left neighbor as command color and do not keep it in output?
        # Let's preserve none of command markers in output for cleaner target? Need decide. We'll probably remove commands in output.
    for comp in comps:
        cells=comp['cells']; color=comp['color']
        pivot=nearest_pivot_for_comp(cells,pivots)
        pr,pc=pivot
        cmd = g[pr][pc-1] if pc-1>=0 and g[pr][pc-1] in (1,2,3) else 0
        for r,c in pivot_rotate(cells,pivot,cmd):
            out[r][c]=color
    return out
```


## H135 — Transform Analogy

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, panel parsing

**Suggested staged path:** Use the first two panels to infer the transform exactly, then apply the same transform to the third panel.


**Train 1 — input**

```text
00000080000008000000
02030080220008000000
02400080400008002000
00000080030008003400
00000080000008000450
00000080000008000000
```


**Train 1 — output**

```text
032
440
500
```


**Train 2 — input**

```text
00000008000000080000000
05060008006050080000000
00760008006700080230000
00700008000700080045000
00000008000000080005000
00000008000000080000000
00000008000000080000000
```


**Train 2 — output**

```text
032
540
500
```


**Train 3 — input**

```text
00000080000008000000
00200080230008000000
00340080044008090200
00045080005008003200
00000080000008000000
00000080000008000000
```


**Train 3 — output**

```text
90
03
22
```


**Train 4 — input**

```text
00000080000008000000
02300080500008000000
00450080540008002030
00050080032008002400
00000080000008000000
00000080000008000000
```


**Train 4 — output**

```text
042
302
```


**Test — input**

```text
00000080000008000000
00000080003208060700
09020080090208068000
00320080000008008900
00000080000008000000
00000080000008000000
```


**Test — output**

```text
089
680
607
```


**Written solution**

Split the three panels, identify which allowed transform maps panel A to panel B, then apply that same transform to panel C and output the result.


**Reference program**

```python
def rule_h135(g):
    panels=panel_split_by_full8_cols(g)
    assert len(panels)==3
    A,B,C=panels
    A_crop=crop_bbox(A)
    B_crop=crop_bbox(B)
    C_crop=crop_bbox(C)
    k=match_transform(A_crop,B_crop)
    return TRANSFORMS[k](C_crop)
```


## H136 — Nested Palette Fill

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nested frames, depth reasoning, palette application

**Suggested staged path:** Read the palette strip first, then count how many nested 8 frames contain each zero cell. Depth 1 gets the first palette color, depth 2 the next, and so on.


**Train 1 — input**

```text
200000000000
300888888888
000800000008
000808888808
000808000808
000808000808
000808000808
000808888808
000800000008
000888888888
000000000000
```


**Train 1 — output**

```text
200000000000
300888888888
000822222228
000828888828
000828333828
000828333828
000828333828
000828888828
000822222228
000888888888
000000000000
```


**Train 2 — input**

```text
4000000000000
5000888888888
6000800000008
0000808888808
0000808000808
0000808888808
0000808808808
0000808888808
0000808000808
0000808888808
0000800000008
0000888888888
0000000000000
```


**Train 2 — output**

```text
4000000000000
5000888888888
6000844444448
0000848888848
0000848444848
0000848888848
0000848848848
0000848888848
0000848444848
0000848888848
0000844444448
0000888888888
0000000000000
```


**Train 3 — input**

```text
30000000000000
70000000000000
00000888888888
00000800000008
00000808888808
00000808000808
00000808000808
00000808000808
00000808888808
00000800000008
00000888888888
00000000000000
```


**Train 3 — output**

```text
30000000000000
70000000000000
00000888888888
00000833333338
00000838888838
00000838777838
00000838777838
00000838777838
00000838888838
00000833333338
00000888888888
00000000000000
```


**Train 4 — input**

```text
200000000000000
400008888888888
600008000000008
000008088888808
000008080000808
000008088888808
000008088008808
000008088008808
000008088888808
000008080000808
000008088888808
000008000000008
000008888888888
000000000000000
```


**Train 4 — output**

```text
200000000000000
400008888888888
600008222222228
000008288888828
000008282222828
000008288888828
000008288228828
000008288228828
000008288888828
000008282222828
000008288888828
000008222222228
000008888888888
000000000000000
```


**Test — input**

```text
500000000000
200000000000
000088888888
000080000008
000080888808
000080800808
000080800808
000080800808
000080888808
000080000008
000088888888
000000000000
```


**Test — output**

```text
500000000000
200000000000
000088888888
000085555558
000085888858
000085822858
000085822858
000085822858
000085888858
000085555558
000088888888
000000000000
```


**Written solution**

The left palette lists fill colors from outermost chamber inward. For each zero cell inside the nested 8 rectangles, count how many frames contain it and fill it with the corresponding palette color.


**Reference program**

```python
def rule_h136(g):
    H,W=size(g)
    # palette in leftmost column nonzero excluding 8
    palette=[g[r][0] for r in range(H) if g[r][0] not in (0,8)]
    out=clone(g)
    # find frame bboxes of 8 on right side. assume nested rectangles same color 8
    frames=[]
    # detect top-left corners of rectangles from 8s
    # simpler: unique row/col extents from 8 cells
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    # frame detection by scanning rectangles
    seen=set()
    for comp in components_by_color(g, ignore={0}):
        if comp['color']!=8:
            continue
        # nested frames are connected if sharing corners? Actually disjoint by zeros? same color 8 nested rectangles are disconnected? yes because separated by zeros.
        r0,c0,r1,c1=bbox(comp['cells'])
        border=set(frame_border_cells(r0,c0,r1,c1))
        if set(comp['cells'])==border:
            frames.append((r0,c0,r1,c1))
    frames.sort(key=lambda b:(b[0], b[1]))  # outer first
    # compute chambers from outside to inside by flood fill restricted to frame area?
    # We'll fill regions inside outer frame and outside next etc.
    # Use depth based on how many frames strictly contain cell.
    for r in range(H):
        for c in range(W):
            if g[r][c]!=0:
                continue
            depth=0
            for r0,c0,r1,c1 in frames:
                if r0 < r < r1 and c0 < c < c1:
                    depth += 1
            if depth>0 and depth<=len(palette):
                out[r][c]=palette[depth-1]
    return out
```


## H137 — Voronoi Inside the Frame

**Difficulty:** hard

**Train pairs:** 4

**Skills:** distance fields, seed ownership, tie handling

**Suggested staged path:** Ignore the border at first and focus on the seed cells. Each interior location belongs to the nearest seed by Manhattan distance; equal-distance ties stay blank.


**Train 1 — input**

```text
000000000000
008888888800
008000000800
008020000800
008000000800
008000000800
008000030800
008000000800
008888888800
000000000000
```


**Train 1 — output**

```text
000000000000
008888888800
008222200800
008222200800
008222033800
008220333800
008003333800
008003333800
008888888800
000000000000
```


**Train 2 — input**

```text
0000000000000
0008888888880
0008000000080
0008040000080
0008000000080
0008000200080
0008000000080
0008000006080
0008000000080
0008888888880
0000000000000
```


**Train 2 — output**

```text
0000000000000
0008888888880
0008444000080
0008444000080
0008440220080
0008002220080
0008002206680
0008000066680
0008000066680
0008888888880
0000000000000
```


**Train 3 — input**

```text
00000000000
08888888880
08050000080
08000000080
08000000080
08000003080
08000000080
08888888880
00000000000
```


**Train 3 — output**

```text
00000000000
08888888880
08555553380
08555533380
08555333380
08553333380
08553333380
08888888880
00000000000
```


**Train 4 — input**

```text
00000000000000
00000000000000
00888888888880
00800000000080
00802000007080
00800000000080
00800000000080
00800000000080
00800005000080
00800000000080
00888888888880
00000000000000
```


**Train 4 — output**

```text
00000000000000
00000000000000
00888888888880
00822220777780
00822220777780
00822225777780
00822255577780
00822555557780
00855555555580
00855555555580
00888888888880
00000000000000
```


**Test — input**

```text
000000000000000
000088888888880
000080000000080
000080600000080
000080000200080
000080000000080
000080000004080
000080000000080
000088888888880
000000000000000
```


**Test — output**

```text
000000000000000
000088888888880
000086660220080
000086660220080
000086602220080
000086602204480
000086600044480
000086600044480
000088888888880
000000000000000
```


**Written solution**

Inside the 8 frame, fill every cell with the color of the nearest seed using Manhattan distance. If two or more seed colors tie for nearest, leave the cell 0. Keep the border and seeds.


**Reference program**

```python
def rule_h137(g):
    H,W=size(g)
    out=clone(g)
    frame_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    r0,c0,r1,c1=bbox(frame_cells)
    seeds=[((r,c),g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,8)]
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if g[r][c]==8:
                continue
            dists=[(abs(r-sr)+abs(c-sc), color) for (sr,sc),color in seeds]
            md=min(d for d,_ in dists)
            colors=[color for d,color in dists if d==md]
            out[r][c]=colors[0] if len(set(colors))==1 else 0
    return out
```


## H138 — Compose Two Commands

**Difficulty:** hard

**Train pairs:** 4

**Skills:** transform composition, symbol decoding, cropping

**Suggested staged path:** The first two cells form an ordered command pair. Crop the motif, apply the first transform, then apply the second to the result.


**Train 1 — input**

```text
1300000000
0000000000
0000000000
0002030000
0002400000
0000000000
0000000000
0000000000
0000000000
```


**Train 1 — output**

```text
22
04
30
```


**Train 2 — input**

```text
52000000000
00000000000
00000000000
00000000000
00050600000
00007600000
00007000000
00000000000
00000000000
00000000000
```


**Train 2 — output**

```text
066
770
005
```


**Train 3 — input**

```text
310000000000
000000000000
000000000000
000000020000
000000034000
000000004500
000000000000
000000000000
000000000000
```


**Train 3 — output**

```text
500
440
032
```


**Train 4 — input**

```text
4500000000
0000000000
0000000000
0000000000
0000000000
0023000000
0004500000
0000500000
0000000000
0000000000
```


**Train 4 — output**

```text
002
043
550
```


**Test — input**

```text
230000000000
000000000000
000000000000
000000000000
000000000000
000006070000
000006800000
000000890000
000000000000
000000000000
000000000000
```


**Test — output**

```text
089
680
607
```


**Written solution**

Read the two command cells, crop the remaining motif, and compose the transforms in order: first command 1 then command 2.


**Reference program**

```python
def rule_h138(g):
    cmd1,cmd2=g[0][0],g[0][1]
    g2=clone(g); g2[0][0]=0; g2[0][1]=0
    motif=crop_bbox(g2)
    map_cmd={1:1,2:2,3:3,4:4,5:5}
    return apply_transform(apply_transform(motif,map_cmd[cmd1]), map_cmd[cmd2])
```


## H139 — Area Comparison Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** panel parsing, relational reasoning, pairwise comparison

**Suggested staged path:** Extract one component from each panel, count its area, then compare every ordered pair. Encode greater, equal, and smaller with different output colors.


**Train 1 — input**

```text
0000080000008000000
0200080400008050500
0200080400008055500
0220080444008005000
0000080000008000000
0000080000008000000
```


**Train 1 — output**

```text
133
213
221
```


**Train 2 — input**

```text
000000800000800000
066000803330802000
066000800300802000
060000800000802200
000000800000800000
000000800000800000
```


**Train 2 — output**

```text
122
311
311
```


**Train 3 — input**

```text
00000080000008000000
05050080700008040000
05550080770008040000
00500080077008044400
00000080000008000000
00000080000008000000
```


**Train 3 — output**

```text
122
311
311
```


**Train 4 — input**

```text
0000008000000800000
0400008066000803330
0400008066000800300
0444008060000800000
0000008000000800000
0000008000000800000
```


**Train 4 — output**

```text
112
112
331
```


**Test — input**

```text
00000800000800000
02000803330802000
02000800300802000
02200800000802200
00000800000800000
```


**Test — output**

```text
111
111
111
```


**Written solution**

Split the three panels, measure each object’s area, and output a 3x3 matrix: 1 for equal area, 2 when the row panel is larger, and 3 when it is smaller.


**Reference program**

```python
def rule_h139(g):
    panels=panel_split_by_full8_cols(g)
    areas=[]
    for p in panels:
        areas.append(sum(v!=0 for row in p for v in row if v!=8))
    n=len(areas)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            out[i][j]=1 if areas[i]==areas[j] else (2 if areas[i]>areas[j] else 3)
    return out
```


## H140 — Select and Transform the Panel

**Difficulty:** hard

**Train pairs:** 4

**Skills:** selector legend, panel lookup, transform application

**Suggested staged path:** The first selector cell chooses a border color and the second chooses a transform. Find the matching panel, crop its interior motif, and transform that crop.


**Train 1 — input**

```text
910000000000000000
000000000000000000
000111110009999900
000120310009200900
000124010009340900
000100010009045900
000111110009000900
000000000009999900
000006666600000000
000006220600000000
000006030600000000
000006666600000000
000000000000000000
```


**Train 1 — output**

```text
032
440
500
```


**Train 2 — input**

```text
8200000000000000000
0000000000000000000
0088888800000000000
0085060800111111000
0080700800120301000
0080000800124001000
0080000800100001000
0088888800100001000
0000000000111111000
0000000000009999900
0000000000009220900
0000000000009030900
0000000000009999900
0000000000000000000
```


**Train 2 — output**

```text
070
605
```


**Train 3 — input**

```text
13000000000000000000
00000000000000000000
00001111111009999900
00001200001009220900
00001340001009030900
00001045001009000900
00001000001009999900
00001111111000000000
00000000666666000000
00000000650606000000
00000000607006000000
00000000666666000000
00000000000000000000
```


**Train 3 — output**

```text
002
043
540
```


**Train 4 — input**

```text
64000000000000000000
00000000000000000000
00000000000000000000
00099999900066666600
00092030900062000600
00092400900063400600
00090000900060450600
00090000900060000600
00099999900060000600
00000000000066666600
00000011111000000000
00000012201000000000
00000010301000000000
00000011111000000000
00000000000000000000
```


**Train 4 — output**

```text
230
044
005
```


**Test — input**

```text
910000000000000000
000000000000000000
009999990011111100
009506090012030100
009070090012400100
009000090010000100
009000090010000100
009999990010000100
000000000011111100
000066666000000000
000062206000000000
000060306000000000
000066666000000000
000000000000000000
```


**Test — output**

```text
05
70
06
```


**Written solution**

Use the first top-row cell to select the framed panel by border color, crop that panel’s interior motif, then transform it according to the second top-row command.


**Reference program**

```python
def rule_h140(g):
    selector_color=g[0][0]
    cmd=g[0][1]
    frames, others=frame_components(g)
    chosen=[fr for fr in frames if fr['color']==selector_color][0]
    r0,c0,r1,c1=chosen['bbox']
    motif=[row[c0+1:c1] for row in g[r0+1:r1]]
    transform_map={1:1,2:2,3:3,4:5}  # 4->transpose
    return apply_transform(crop_bbox(motif), transform_map[cmd])
```
