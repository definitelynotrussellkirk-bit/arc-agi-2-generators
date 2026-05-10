# ARC Additional Puzzle Bank — 21 Puzzles (Set 6)

This sixth pack continues the numbering with **`E36–E42`**, **`M36–M42`**, and **`H36–H42`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It also introduces a new helper primitive for solver-facing implementations:

```text
rebase_component(base_grid, source_cells, anchors, origin='bbox_topleft', recolor='keep'|'anchor', transform='id')
```
Intuition: normalize a source component to its own bounding box, optionally transform it, then replay it at one or more anchor locations. This primitive is used directly in **E41**, **M41**, and **H36**.

Design goals for this set:

- easy: straight-line filling, local completion, transpose-style symmetry, gravity, cropping, and simple shape replay

- medium: sparse-to-dense rectangle inference, guide-driven transforms, chamber filling, recolored broadcasting, and orthogonal routing

- hard: analogy transfer, rotation-command composition, topological hole counting, comparative frame selection, normalized subtraction, and Manhattan partitioning


## Easy (7)


### E36 — Fill Between Matching Endpoints

**Difficulty:** easy

**Train pairs:** 4

**Skills:** segment fill, alignment, endpoint inference

**Suggested staged path:** Start by ignoring color identity and just look for two identical nonzero cells that already lie on one straight line.


**Train 1 — input**

```text
000000040
020002000
000000000
000000000
000000000
000000040
006060000
000000000
```

**Train 1 — output**

```text
000000040
022222040
000000040
000000040
000000040
000000040
006660000
000000000
```


**Train 2 — input**

```text
0000000000
0000000030
1000100000
0000000000
0000000000
0000000030
0070007000
```

**Train 2 — output**

```text
0000000000
0000000030
1111100030
0000000030
0000000030
0000000030
0077777000
```


**Train 3 — input**

```text
000500000
000000000
000000002
000000000
000500000
000000000
000000002
080000080
000000000
```

**Train 3 — output**

```text
000500000
000500000
000500002
000500002
000500002
000000002
000000002
088888880
000000000
```


**Train 4 — input**

```text
40000000000
00000000000
00000000000
00900000090
00000000000
00000000000
40000000000
00000600006
```

**Train 4 — output**

```text
40000000000
40000000000
40000000000
40999999990
40000000000
40000000000
40000000000
00000666666
```

**Test — input**

```text
0000000080
0000002000
0000000000
0000000000
0500050000
0000000080
0000000000
0000002000
0000000000
```

**Expected test output**

```text
0000000080
0000002080
0000002080
0000002080
0555552080
0000002080
0000002000
0000002000
0000000000
```

**Written solution**

Each color appears exactly twice as the endpoints of a horizontal or vertical segment. Fill every cell on that segment, inclusive, with the same color.

**Reference program**

```python
def rule_e36(g):
    h,w=size(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
        elif c1==c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
        else:
            out[r1][c1]=color; out[r2][c2]=color
    return out
```


### E37 — Complete 2×2 Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local pattern completion, 2x2 reasoning, monochrome neighborhoods

**Suggested staged path:** Scan only 2×2 windows. Whenever three cells match and the fourth is black, the missing corner is the only thing that needs changing.


**Train 1 — input**

```text
00000066
02200006
02000000
00000400
00004400
00000000
00000000
```

**Train 1 — output**

```text
00000066
02200066
02200000
00004400
00004400
00000000
00000000
```


**Train 2 — input**

```text
000000000
000000070
003000770
003300000
000000000
000005500
000000500
000000000
```

**Train 2 — output**

```text
000000000
000000770
003300770
003300000
000000000
000005500
000005500
000000000
```


**Train 3 — input**

```text
0080000000
0880000000
0000000000
0000002000
0000002200
0044000000
0040000000
```

**Train 3 — output**

```text
0880000000
0880000000
0000000000
0000002200
0000002200
0044000000
0044000000
```


**Train 4 — input**

```text
000000000
000000000
011000000
001000000
000000005
000000055
000009000
000009900
000000000
```

**Train 4 — output**

```text
000000000
000000000
011000000
011000000
000000055
000000055
000009900
000009900
000000000
```

**Test — input**

```text
0000000000
0002000000
0002200044
0000000004
0000000660
0080000600
0880000000
0000000000
```

**Expected test output**

```text
0000000000
0002200000
0002200044
0000000044
0000000660
0880000660
0880000000
0000000000
```

**Written solution**

Every nonzero motif is a 2×2 block with one missing corner. If three cells in a 2×2 window share the same nonzero color and one cell is 0, fill the 0 with that color.

**Reference program**

```python
def rule_e37(g):
    h,w=size(g)
    out=clone(g)
    changed=True
    while changed:
        changed=False
        for r in range(h-1):
            for c in range(w-1):
                vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
                nz=[v for v in vals if v!=0]
                if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                    idx=vals.index(0)
                    rr=r + (idx//2)
                    cc=c + (idx%2)
                    out[rr][cc]=nz[0]
                    changed=True
        g=clone(out)
    return out
```


### E38 — Main-Diagonal Mirror Add

**Difficulty:** easy

**Train pairs:** 4

**Skills:** symmetry, transpose, same-size transform

**Suggested staged path:** Treat the main diagonal as the axis. First copy the original points, then add their transposed partners.


**Train 1 — input**

```text
0020000
0000400
0000060
0008000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0020000
0000400
2000060
0008000
0400000
0060000
0000000
```


**Train 2 — input**

```text
01000020
00000000
00000300
00000000
00000004
00000000
00000000
00000000
```

**Train 2 — output**

```text
01000020
10000000
00000300
00000000
00000004
00300000
20000000
00004000
```


**Train 3 — input**

```text
000050
000700
009000
000000
000000
000000
```

**Train 3 — output**

```text
000050
000700
009000
070000
500000
000000
```


**Train 4 — input**

```text
000000002
000003000
000000040
000000500
000060000
000000000
000000000
000000000
000000000
```

**Train 4 — output**

```text
000000002
000003000
000000040
000000500
000060000
030000000
000500000
004000000
200000000
```

**Test — input**

```text
00020000
00000050
00007000
00000009
00000000
00000000
00000000
00000000
```

**Expected test output**

```text
00020000
00000050
00007000
20000009
00700000
00000000
05000000
00090000
```

**Written solution**

Reflect every nonzero cell across the main diagonal and keep the union of original and reflected cells. Diagonal cells stay where they are.

**Reference program**

```python
def rule_e38(g):
    h,w=size(g)
    assert h==w
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]==0 and g[c][r]!=0:
                out[r][c]=g[c][r]
    return out
```


### E39 — Column Gravity Down

**Difficulty:** easy

**Train pairs:** 4

**Skills:** gravity, column compression, order preservation

**Suggested staged path:** Solve one column at a time. Ignore colors until you see that only vertical order matters.


**Train 1 — input**

```text
20000070
00050000
40000000
00000080
00060000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00000000
20050070
40060080
```


**Train 2 — input**

```text
0030000
0040000
0000060
0000000
0000070
0050000
0000000
0000000
```

**Train 2 — output**

```text
0000000
0000000
0000000
0000000
0000000
0030000
0040060
0050070
```


**Train 3 — input**

```text
090040000
020000050
000030000
000000000
000000000
000000060
```

**Train 3 — output**

```text
000000000
000000000
000000000
000000000
090040050
020030060
```


**Train 4 — input**

```text
00000080
30000000
00050000
00000010
00000020
00000000
00000000
40000000
00000000
```

**Train 4 — output**

```text
00000000
00000000
00000000
00000000
00000000
00000000
00000080
30000010
40050020
```

**Test — input**

```text
200000060
000040000
000000070
300000000
000000000
000000080
000050000
000000000
```

**Expected test output**

```text
000000000
000000000
000000000
000000000
000000000
000000060
200040070
300050080
```

**Written solution**

Within each column, drop all nonzero cells to the bottom while preserving their top-to-bottom order. Every black cell ends up above the compressed stack.

**Reference program**

```python
def rule_e39(g):
    return gravity_down(g)
```


### E40 — Crop And Rotate Right

**Difficulty:** easy

**Train pairs:** 4

**Skills:** cropping, rotation, dynamic-size output

**Suggested staged path:** First isolate the minimal nonzero bounding box. Only after cropping should you worry about the rotation.


**Train 1 — input**

```text
000000000
000000000
000120000
000003000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
01
02
30
```


**Train 2 — input**

```text
00000000
00000000
00000000
00000000
04500000
04060000
00000000
00000000
00000000
```

**Train 2 — output**

```text
44
05
60
```


**Train 3 — input**

```text
0000000000
0000070000
0000077000
0000000700
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
077
070
700
```


**Train 4 — input**

```text
00000000
00000000
00000000
00890000
00009000
00999000
00000000
00000000
```

**Train 4 — output**

```text
908
909
990
```

**Test — input**

```text
000000000
000000000
000023000
000020340
000000300
000000000
000000000
000000000
000000000
```

**Expected test output**

```text
022
003
330
040
```

**Written solution**

Take the minimal bounding box containing the object, discard the surrounding black background, and rotate the cropped object 90 degrees clockwise.

**Reference program**

```python
def rule_e40(g):
    return rotate_cw(crop_nonzero(g))
```


### E41 — Glyph Broadcast From Anchors

**Difficulty:** easy

**Train pairs:** 4

**Skills:** shape normalization, translation, component copying

**Uses new primitive:** yes (`rebase_component`)

**Suggested staged path:** Identify the single source glyph first. Then treat each 3 as a place where that glyph should be replayed.


**Train 1 — input**

```text
0000000000
0220003000
0200000000
0222000000
0000000000
0030003000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000003300
0000003000
0000003330
0000000000
0033003300
0030003000
0033303330
0000000000
```


**Train 2 — input**

```text
00000003000
00000000000
02200000000
00200000000
02200030000
00000000030
00000000000
00000000000
```

**Train 2 — output**

```text
00000003300
00000000300
00000003300
00000000000
00000033000
00000003033
00000033003
00000000033
```


**Train 3 — input**

```text
0000000000
0020000000
0022200300
0002000000
0000000000
0000000000
0000030000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000000000
0000000300
0000000333
0000000030
0000000000
0000030000
0000033300
0000003000
0000000000
```


**Train 4 — input**

```text
022000000000
002000000000
002220003000
000000000000
000000000000
000000300000
000000000300
000000000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000000
000000003300
000000000300
000000000333
000000330000
000000030330
000000033330
000000000033
```

**Test — input**

```text
00000000000
02200003000
00200000000
00220000000
00000300000
00000000000
00000000300
00000000000
00000000000
00000000000
```

**Expected test output**

```text
00000000000
00000003300
00000000300
00000000330
00000330000
00000030000
00000033330
00000000030
00000000033
00000000000
```

**Written solution**

Find the color-2 source glyph, normalize it to its bounding box, and copy that same shape to every color-3 anchor. The copies are recolored to 3 and the original source is not kept.

**Reference program**

```python
def rule_e41(g):
    h,w=size(g)
    comps=components_of_color(g,2)
    assert len(comps)==1
    source_abs=[(r,c,2) for r,c in comps[0]]
    anchors=[(r,c,3) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    out=blank(h,w)
    out=rebase_component(out, source_abs, anchors, recolor='anchor')
    return out
```


### E42 — Bounding-Box Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bounding boxes, extrema, same-size abstraction

**Suggested staged path:** Forget the exact interior pattern of each color. Only its outermost row and column positions matter.


**Train 1 — input**

```text
000000000
020020000
000000000
002000000
000000500
000005500
000000050
000000000
```

**Train 1 — output**

```text
000000000
020020000
000000000
020020000
000005050
000000000
000005050
000000000
```


**Train 2 — input**

```text
0030000000
0000000000
0000030000
0000000000
0003000000
0700000000
0070000000
0700700000
0000000000
```

**Train 2 — output**

```text
0030030000
0000000000
0000000000
0000000000
0030030000
0700700000
0000000000
0700700000
0000000000
```


**Train 3 — input**

```text
00000000000
00000000400
00000000004
00000040000
08000000000
00008000000
00800000000
```

**Train 3 — output**

```text
00000000000
00000040004
00000000000
00000040004
08008000000
00000000000
08008000000
```


**Train 4 — input**

```text
000000000
000000000
006000600
000000000
000060000
000600000
090000000
000090000
000009000
000000000
```

**Train 4 — output**

```text
000000000
000000000
006000600
000000000
000000000
006000600
090009000
000000000
090009000
000000000
```

**Test — input**

```text
80000000000
00800002000
08000000002
00000000020
00000000200
00500000000
00050000000
00005000000
00000000000
```

**Expected test output**

```text
80800000000
00000002002
80800000000
00000000000
00000002002
00505000000
00000000000
00505000000
00000000000
```

**Written solution**

For each nonzero color, compute the bounding box covering all cells of that color and keep only the four corners of that box in the output.

**Reference program**

```python
def rule_e42(g):
    h,w=size(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        r0,c0,r1,c1=bbox(cells)
        for rr,cc in {(r0,c0),(r0,c1),(r1,c0),(r1,c1)}:
            out[rr][cc]=color
    return out
```


## Medium (7)


### M36 — Fill Rectangles From Four Corners

**Difficulty:** medium

**Train pairs:** 4

**Skills:** rectangle inference, bbox fill, sparse-to-dense

**Suggested staged path:** Each color gives you only four clues. Treat them as the corners of one axis-aligned rectangle and fill the implied area.


**Train 1 — input**

```text
0000000000
0200200000
0000005050
0000000000
0200200000
0000000000
0000005050
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0222200000
0222205550
0222205550
0222205550
0000005550
0000005550
0000000000
0000000000
```


**Train 2 — input**

```text
00300300000
00000000000
00000000000
00300300000
00000007007
00000000000
00000000000
00000007007
```

**Train 2 — output**

```text
00333300000
00333300000
00333300000
00333300000
00000007777
00000007777
00000007777
00000007777
```


**Train 3 — input**

```text
0000000000
0000008008
0404000000
0000000000
0000008008
0000000000
0404000000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000008888
0444008888
0444008888
0444008888
0444000000
0444000000
0000000000
0000000000
0000000000
```


**Train 4 — input**

```text
000000000000
000000006060
000000000000
090090000000
000000000000
000000006060
000000000000
090090000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000006660
000000006660
099990006660
099990006660
099990006660
099990000000
099990000000
000000000000
```

**Test — input**

```text
00000000000
00000007070
00200200000
00000000000
00000007070
00000000000
40400200000
00000000000
40400000000
00000000000
```

**Expected test output**

```text
00000000000
00000007770
00000007770
00000007770
00000007770
00000000000
44400000000
44400000000
44400000000
00000000000
```

**Written solution**

Every color marks the four corners of a rectangle. Fill the entire rectangle, including its interior, with that same color.

**Reference program**

```python
def rule_m36(g):
    h,w=size(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        if len(cells)!=4:
            continue
        r0,c0,r1,c1=bbox(cells)
        fill_rect(out,r0,c0,r1,c1,color)
    return out
```


### M37 — Legend-Selected Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** legend decoding, color selection, cropping

**Suggested staged path:** Read the top-left legend cell before looking at shapes. The rest of the puzzle is just finding that chosen color and cropping it tightly.


**Train 1 — input**

```text
400000000000
002200000000
000220000000
000000000000
000000444000
000000404400
033000000000
033300000000
000000000000
000000000000
```

**Train 1 — output**

```text
4440
4044
```


**Train 2 — input**

```text
30000000000
00000330000
00000303000
00000333000
00000000444
00220000404
00220000000
00000000000
00000000000
```

**Train 2 — output**

```text
330
303
333
```


**Train 3 — input**

```text
200000000000
000000000000
000000020000
000000022200
000000000000
000000000000
033000000000
033300004444
000000004004
000000000000
000000000000
```

**Train 3 — output**

```text
200
222
```


**Train 4 — input**

```text
4000000000
0222000000
0202000000
0000000000
0000044000
0000044400
0033340400
0030300000
0000000000
0000000000
```

**Train 4 — output**

```text
440
444
404
```

**Test — input**

```text
300000000000
000000300000
000000333000
000000303000
000000000000
022200000000
002000004440
002220004040
000000000000
000000000000
```

**Expected test output**

```text
300
333
303
```

**Written solution**

The top-left cell tells you which color to select. Keep only the cells of that color, ignore all others, and crop the result to its minimal bounding box.

**Reference program**

```python
def rule_m37(g):
    sel=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==sel and not (r==0 and c==0)]
    return crop_bbox(g,cells)
```


### M38 — Diagonal Reflection By Command

**Difficulty:** medium

**Train pairs:** 4

**Skills:** conditional symmetry, main vs anti diagonal, guide markers

**Suggested staged path:** The guide only chooses the axis; it is not part of the final object. After that, the task is a diagonal reflection union.


**Train 1 — input**

```text
10000000
00000000
00000500
00005000
00000560
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000500
00005000
00050560
00505000
00006000
00000000
```


**Train 2 — input**

```text
000000002
000000000
070000000
077000000
000700000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
070000000
077000000
000700000
000070000
000007000
000007700
000000000
```


**Train 3 — input**

```text
10000000
00000800
00000080
00000088
00000000
00000000
00000000
00000000
```

**Train 3 — output**

```text
00000000
00000800
00000080
00000088
00000000
08000000
00880000
00080000
```


**Train 4 — input**

```text
0000000002
0000000000
0000000000
0000000000
0060000000
0006600000
0000600000
0000000000
0000000000
0000000000
```

**Train 4 — output**

```text
0000000000
0000000000
0000000000
0000000000
0060000000
0006600000
0000600000
0000060000
0000000000
0000000000
```

**Test — input**

```text
000000002
000000000
000900000
000099000
000009000
000000000
000000000
000000000
000000000
```

**Expected test output**

```text
000000000
000000000
000900000
000099000
000009000
000000900
000000000
000000000
000000000
```

**Written solution**

A guide marker chooses which diagonal to reflect across: one command means the main diagonal, the other the anti-diagonal. Remove the guide and output the union of the object with its reflection.

**Reference program**

```python
def rule_m38(g):
    h,w=size(g)
    assert h==w
    cmd='diag' if g[0][0]==1 else 'anti'
    base=clone(g)
    base[0][0]=0
    base[0][w-1]=0
    trans = reflect_main_diag if cmd=='diag' else reflect_anti_diag
    ref=trans(base)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=base[r][c] if base[r][c]!=0 else ref[r][c]
    return out
```


### M39 — Directional Gravity By Guide

**Difficulty:** medium

**Train pairs:** 4

**Skills:** conditional movement, gravity, row/column preservation

**Suggested staged path:** Use the guide cell to decide the direction first. Then apply the same compression logic everywhere in that direction.


**Train 1 — input**

```text
100007000
005000000
000000090
006000000
000008000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
005007000
006008090
```


**Train 2 — input**

```text
20000000
00000000
00000000
00000500
03000000
00000000
00000060
02000000
00000400
```

**Train 2 — output**

```text
03000560
02000400
00000000
00000000
00000000
00000000
00000000
00000000
00000000
```


**Train 3 — input**

```text
3000000000
0000000203
0000000000
0000000000
0000040050
0000006000
0000000000
```

**Train 3 — output**

```text
0000000000
2300000000
0000000000
0000000000
4500000000
6000000000
0000000000
```


**Train 4 — input**

```text
4000000000
0000000000
0708000000
0000000000
0000500000
0000000000
2000003000
0000000000
```

**Train 4 — output**

```text
0000000000
0000000000
0000000078
0000000000
0000000005
0000000000
0000000023
0000000000
```

**Test — input**

```text
100020000
000000000
000000400
000000000
000030000
006000000
000000000
000000500
000000000
```

**Expected test output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000020400
006030500
```

**Written solution**

The guide color specifies a gravity direction: down, up, left, or right. Remove the guide, then compress all nonzero cells along that direction while preserving their order within each line.

**Reference program**

```python
def rule_m39(g):
    cmd=g[0][0]
    base=clone(g); base[0][0]=0
    if cmd==1: return gravity_down(base)
    if cmd==2: return gravity_up(base)
    if cmd==3: return gravity_left(base)
    if cmd==4: return gravity_right(base)
    return base
```


### M40 — Seeded Chamber Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** containment, rectangular borders, interior repainting

**Suggested staged path:** Separate border cells from interior clues. The only interior information that matters is the seed color inside each chamber.


**Train 1 — input**

```text
000000000000
022220000000
027020055550
020020050050
022220058050
000000050050
000000055550
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
022220000000
027720055550
027720058850
022220058850
000000058850
000000055550
000000000000
000000000000
000000000000
```


**Train 2 — input**

```text
00000000000
00000333330
04440300030
04040306030
04940300030
04040333330
04440000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000333330
04440366630
04940366630
04940366630
04940333330
04440000000
00000000000
00000000000
```


**Train 3 — input**

```text
000000000000
066666000000
060006000000
060206000000
060006000000
066666000000
000000077770
000000074070
000000070070
000000077770
000000000000
```

**Train 3 — output**

```text
000000000000
066666000000
062226000000
062226000000
062226000000
066666000000
000000077770
000000074470
000000074470
000000077770
000000000000
```


**Train 4 — input**

```text
0000000000
0000008880
0000008380
0000008080
0000008880
0222000000
0262000000
0202000000
0222000000
0000000000
```

**Train 4 — output**

```text
0000000000
0000008880
0000008380
0000008380
0000008880
0222000000
0262000000
0262000000
0222000000
0000000000
```

**Test — input**

```text
00000000000
03333000000
03003000000
03703000000
03003066660
03333060060
00000062060
00000060060
00000060060
00000066660
00000000000
```

**Expected test output**

```text
00000000000
03333000000
03773000000
03773000000
03773066660
03333062260
00000062260
00000062260
00000062260
00000066660
00000000000
```

**Written solution**

Each hollow rectangle is a chamber, and each chamber contains a colored seed. Preserve the border, then fill the chamber interior with the seed's color.

**Reference program**

```python
def rule_m40(g):
    h,w=size(g)
    out=blank(h,w)
    used=[[False]*w for _ in range(h)]
    # copy rectangle borders
    rects=[]
    for color in sorted({v for row in g for v in row if v!=0}):
        for comp in components_of_color(g,color):
            if len(comp)>=8 and is_rect_border_component(g, comp, color):
                rects.append((color,comp,bbox(comp)))
                for r,c in comp:
                    out[r][c]=color
    for color,comp,(r0,c0,r1,c1) in rects:
        seeds=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]!=0 and (r,c) not in comp]
        if not seeds:
            continue
        # choose first non-border seed
        sr,sc,scol=seeds[0]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=scol
    return out
```


### M41 — Recolor Broadcast Component

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component normalization, anchor recoloring, broadcast copy

**Uses new primitive:** yes (`rebase_component`)

**Suggested staged path:** Identify the one multi-cell source component first. Then treat every singleton anchor as a place to replay its shape, but not its palette.


**Train 1 — input**

```text
000000000000
024000060000
024400000000
004000000000
000000000000
000007000000
000000000800
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
000000066000
000000066600
000000006000
000000000000
000007700000
000007770880
000000700888
000000000080
000000000000
```


**Train 2 — input**

```text
00220000000
00040000000
00444006000
00000000000
00000000000
08000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000006600
00000000600
00000006660
08800000000
00800000000
08880000000
00000000000
```


**Train 3 — input**

```text
000000000000
020400000000
024400000000
000400007000
000000000000
000000000000
000000000000
000009000000
000000000600
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000007070
000000007770
000000000070
000000000000
000009090000
000009990606
000000090666
000000000006
```


**Train 4 — input**

```text
0000000000
0240008000
0044000000
0004400000
0000000000
0000700000
0000000000
0000000000
0000000000
0000000000
```

**Train 4 — output**

```text
0000000000
0000008800
0000000880
0000000088
0000000000
0000770000
0000077000
0000007700
0000000000
0000000000
```

**Test — input**

```text
000000000000
024000000000
024000006000
004400000000
000000000000
000000000000
000007000000
000000000900
000000000000
000000000000
000000000000
```

**Expected test output**

```text
000000000000
000000000000
000000006600
000000006600
000000000660
000000000000
000007700000
000007700990
000000770990
000000000099
000000000000
```

**Written solution**

Find the multicolor source component, normalize its shape, and copy that shape to every anchor cell. Each copy is recolored uniformly to the anchor's color.

**Reference program**

```python
def rule_m41(g):
    h,w=size(g)
    comps=components_nonzero(g, treat_colors_separately=False)
    # source = largest component with size>1 and colors subset of {2,4}
    source=None
    for color,cells in sorted(comps, key=lambda x: -len(x[1])):
        vals={g[r][c] for r,c in cells}
        if len(cells)>1 and vals <= {2,4}:
            source=cells
            break
    assert source is not None
    source_abs=[(r,c,g[r][c]) for r,c in source]
    anchor_colors={v for row in g for v in row if v in {6,7,8,9}}
    anchors=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v in anchor_colors and (r,c) not in set(source)]
    out=blank(h,w)
    out=rebase_component(out, source_abs, anchors, recolor='anchor')
    return out
```


### M42 — Guided L-Paths

**Difficulty:** medium

**Train pairs:** 4

**Skills:** pair matching, orthogonal paths, global turn convention

**Suggested staged path:** Pair the matching colors first. Then use the guide to decide whether every path turns row-first or column-first.


**Train 1 — input**

```text
10000000000
00000000400
02000000000
00000000000
00000000040
00000000000
00000200000
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
00000000000
00000000440
02222200040
00000200040
00000200040
00000200000
00000200000
00000000000
00000000000
00000000000
```


**Train 2 — input**

```text
2000000000
0030000000
0000000070
0000000000
0000000000
0000000000
0000003000
0000700000
0000000000
```

**Train 2 — output**

```text
0000000000
0030000000
0030000070
0030000070
0030000070
0030000070
0033333070
0000777770
0000000000
```


**Train 3 — input**

```text
100000000000
000000000000
000000000080
000500000000
000000000000
000000800000
000000000000
000000005000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000888880
000555555000
000000805000
000000805000
000000005000
000000005000
000000000000
000000000000
```


**Train 4 — input**

```text
20000000000
00000009000
00000000000
06000000000
00000000000
00000000000
00000000090
00000000000
00000600000
00000000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000009000
00000009000
06000009000
06000009000
06000009000
06000009990
06000000000
06666600000
00000000000
00000000000
```

**Test — input**

```text
100000000000
000000000000
002000000000
000000000000
000000000050
000000000000
000000000000
000000020000
000500000000
000000000000
```

**Expected test output**

```text
000000000000
000000000000
002222220000
000000020000
000555555550
000500020000
000500020000
000500020000
000500000000
000000000000
```

**Written solution**

Each color appears twice and must be connected by an L-shaped orthogonal path. The guide chooses a global turn convention: horizontal-then-vertical or vertical-then-horizontal.

**Reference program**

```python
def rule_m42(g):
    h,w=size(g)
    cmd=g[0][0]
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and not (r==0 and c==0):
                groups[v].append((r,c))
    out=blank(h,w)
    for color,cells in groups.items():
        if len(cells)!=2: 
            continue
        (r1,c1),(r2,c2)=cells
        out[r1][c1]=color; out[r2][c2]=color
        if cmd==1:  # horizontal then vertical
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c2]=color
        else:  # vertical then horizontal
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r2][c]=color
    return out
```


## Hard (7)


### H36 — Command-Rotated Broadcast

**Difficulty:** hard

**Train pairs:** 4

**Skills:** rotation commands, component broadcasting, shape transport

**Uses new primitive:** yes (`rebase_component`)

**Suggested staged path:** Ignore the anchors at first and recover the source component. Once you have it, each command-anchor pair only chooses a rotation and a destination.


**Train 1 — input**

```text
00000000000000
05600019000000
00570000000000
05550000000000
00000000000000
00000000290000
00000000000000
00000000000000
00000000000490
00000000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
00000005600000
00000000570000
00000005550000
00000000000000
00000000050500
00000000055600
00000000057000
00000000000007
00000000000065
00000000000050
00000000000000
```


**Train 2 — input**

```text
0000000000000
0570000000000
0055000490000
0006500000000
0000000000000
0000000000000
0000000003900
0001900000000
0000000000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0000000000000
0000000000500
0000000005600
0000000075000
0000000050000
0000000000560
0000570000055
0000055000007
0000006500000
0000000000000
```


**Train 3 — input**

```text
000000000000
056000000000
055500290000
007500000000
000000000000
000000000000
000000000000
000000049000
000190000000
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000005500
000000075600
000000055000
000000000000
000000000000
000000000550
000056006570
000055505500
000007500000
000000000000
```


**Train 4 — input**

```text
00000000000000
05000000000000
05670000390000
00550000000000
00000000000000
00000000000000
00000001900000
00000000000000
00000000000000
00000000000490
00000000000000
00000000000000
00000000000000
```

**Train 4 — output**

```text
00000000000000
00000000000000
00000000055000
00000000076500
00000000000500
00000000000000
00000000500000
00000000567000
00000000055000
00000000000007
00000000000006
00000000000055
00000000000000
```

**Test — input**

```text
00000000000000
05600000000000
00550001900000
05750000000000
00000000000000
00000000000000
00000000029000
00000000000000
00000000000490
00000000000000
00000000000000
00000000000000
```

**Expected test output**

```text
00000000000000
00000000000000
00000000560000
00000000055000
00000000575000
00000000000000
00000000005050
00000000007560
00000000005505
00000000000065
00000000000050
00000000000000
```

**Written solution**

Extract the multicolor source component, then for every command-anchor pair, rotate the source by the commanded amount and place a copy with its bounding-box origin at the anchor.

**Reference program**

```python
def rule_h36(g):
    h,w=size(g)
    # source colors 5,6,7 ; anchor 9 ; command left of anchor =1..4
    comps=components_nonzero(g, treat_colors_separately=False)
    source=None
    for color,cells in sorted(comps, key=lambda x:-len(x[1])):
        vals={g[r][c] for r,c in cells}
        if len(cells)>1 and vals <= {5,6,7}:
            source=[(r,c,g[r][c]) for r,c in cells]
            break
    assert source is not None
    out=blank(h,w)
    for r in range(h):
        for c in range(1,w):
            if g[r][c]==9 and g[r][c-1] in {1,2,3,4}:
                cmd=g[r][c-1]
                transform={1:'id',2:'rot90',3:'rot180',4:'rot270'}[cmd]
                out=rebase_component(out, source, [(r,c,9)], recolor='keep', transform=transform)
    return out
```


### H37 — Symmetry Analogy Transfer

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, rotation/reflection

**Suggested staged path:** Do not solve the query immediately. First determine which symmetry transforms the exemplar A into exemplar B, then apply that same transform to the query shape.


**Train 1 — input**

```text
00000000000000
02220000220000
02000000020000
00000000020000
00000000000000
00000000000000
00000000000000
00033000000000
00030000000000
00030000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
333
003
```


**Train 2 — input**

```text
00000000000000
02200000220000
02000000020000
02000000020000
00000000000000
00000000000000
00000000000000
00030000000000
00033300000000
00000000000000
00000000000000
00000000000000
```

**Train 2 — output**

```text
003
333
```


**Train 3 — input**

```text
00000000000000
02000000222000
02220000002000
00000000000000
00000000000000
00000000000000
00000000000000
00003300000000
00000300000000
00000000000000
00000000000000
00000000000000
```

**Train 3 — output**

```text
30
33
```


**Train 4 — input**

```text
00000000000000
02200000200000
00200000222000
00200000000000
00000000000000
00000000000000
00000000000000
00030000000000
00033000000000
00003000000000
00000000000000
00000000000000
```

**Train 4 — output**

```text
330
033
```

**Test — input**

```text
00000000000000
02220000200000
02000000200000
00000000220000
00000000000000
00000000000000
00000000000000
00000000000000
00003300000000
00003330000000
00000000000000
00000000000000
00000000000000
```

**Expected test output**

```text
03
33
33
```

**Written solution**

Two exemplar components of color 2 show an input-output transformation under a rotation or reflection. Infer that transform from the exemplar pair and apply it to the color-3 query component; output only the transformed query.

**Reference program**

```python
def rule_h37(g):
    a_b = components_of_color(g,2)
    q_comps = components_of_color(g,3)
    assert len(a_b)==2 and len(q_comps)==1
    a,b = sorted(a_b, key=lambda cells: min(c for r,c in cells))
    q = q_comps[0]
    b_grid=strings_from_grid(render_component_cells(normalize_component_cells([(r,c,1) for r,c in b])))
    chosen=None
    a_pts=normalize_component_cells([(r,c,1) for r,c in a])
    for t in TRANSFORMS:
        tg=strings_from_grid(render_component_cells(apply_transform_to_cells(a_pts, t)))
        if tg==b_grid:
            chosen=t
            break
    assert chosen is not None
    q_pts=[(r,c,3) for r,c in q]
    out=render_component_cells(apply_transform_to_cells(normalize_component_cells(q_pts), chosen))
    return out
```


### H38 — Translation Analogy Transfer

**Difficulty:** hard

**Train pairs:** 4

**Skills:** vector inference, analogy, same-size placement

**Suggested staged path:** Treat the two color-4 components as an example pair. Their relative shift gives you the vector you must reuse on the color-3 query shape.


**Train 1 — input**

```text
0000000000000
0440000000000
0044000000000
0000000000000
0000044000000
0000004400000
0000000000000
0033000000000
0003300000000
0000000000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000003300000
0000000330000
```


**Train 2 — input**

```text
000000000000
004440000000
000400033000
000000003300
000000000000
004440000000
000400000000
000000000000
000000000000
000000000000
000000000000
```

**Train 2 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000033000
000000003300
000000000000
000000000000
000000000000
```


**Train 3 — input**

```text
00000000000000
00000000000000
04000040000000
04440044400000
00000000000000
00000000000000
00000000000000
00003300000000
00003000000000
00003330000000
00000000000000
00000000000000
```

**Train 3 — output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000033000
00000000030000
00000000033300
00000000000000
00000000000000
```


**Train 4 — input**

```text
0000000000000
0440000000000
0400000033000
0444000030300
0000000033300
0000440000000
0000400000000
0000444000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000033
0000000000030
0000000000033
0000000000000
0000000000000
0000000000000
0000000000000
```

**Test — input**

```text
00000000000000
00440000000000
00044000000000
00000000000000
00000000440000
00000000044000
00033000000000
00033300000000
00000000000000
00000000000000
00000000000000
00000000000000
```

**Expected test output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000033000
00000000033300
00000000000000
```

**Written solution**

The two color-4 exemplar components are the same shape at two different positions. Infer the translation vector from the first exemplar to the second, then translate the color-3 query component by that same vector.

**Reference program**

```python
def rule_h38(g):
    ex=components_of_color(g,4)
    q=components_of_color(g,3)
    assert len(ex)==2 and len(q)==1
    ex1,ex2=sorted(ex, key=lambda cells: min(c for r,c in cells))
    r10,c10,_,_=bbox(ex1)
    r20,c20,_,_=bbox(ex2)
    dr,dc=r20-r10,c20-c10
    out=blank(*size(g))
    qcells=q[0]
    qcolor=3
    for r,c in qcells:
        nr,nc=r+dr,c+dc
        if 0<=nr<len(g) and 0<=nc<len(g[0]):
            out[nr][nc]=qcolor
    return out
```


### H39 — Hole-Count Recolor

**Difficulty:** hard

**Train pairs:** 4

**Skills:** topology, hole counting, component-wise recoloring

**Suggested staged path:** Work component by component. Before recoloring anything, count how many enclosed black holes each shape contains.


**Train 1 — input**

```text
00000000000000
02200022200000
02200020200000
00000022200000
00000000000000
00222220000000
00200020000000
00222220000000
00200020000000
00222220000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
03300044400000
03300040400000
00000044400000
00000000000000
00555550000000
00500050000000
00555550000000
00500050000000
00555550000000
00000000000000
00000000000000
```


**Train 2 — input**

```text
00000000000000
00000000000000
02220002200000
02020002200000
02220000000000
00000000000000
00000000000000
00002222222000
00002000002000
00002222222000
00002000002000
00002222222000
00002000002000
00002222222000
```

**Train 2 — output**

```text
00000000000000
00000000000000
04440003300000
04040003300000
04440000000000
00000000000000
00000000000000
00006666666000
00006000006000
00006666666000
00006000006000
00006666666000
00006000006000
00006666666000
```


**Train 3 — input**

```text
000000000000000
002222200000000
002000200000000
002222200000000
002000200000000
002222200000000
000000000000000
000000000222000
022000000202000
022000000222000
000000000000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
000000000000000
005555500000000
005000500000000
005555500000000
005000500000000
005555500000000
000000000000000
000000000444000
033000000404000
033000000444000
000000000000000
000000000000000
000000000000000
```


**Train 4 — input**

```text
000000000000000
022222220000000
020000020000000
022222220000000
020000020000000
022222220000000
020000020000000
022222220000000
000000000022200
002200000020200
002200000022200
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 4 — output**

```text
000000000000000
066666660000000
060000060000000
066666660000000
060000060000000
066666660000000
060000060000000
066666660000000
000000000044400
003300000040400
003300000044400
000000000000000
000000000000000
000000000000000
000000000000000
```

**Test — input**

```text
000000000000000
022200022222000
020200020002000
022200022222000
000000020002000
000000022222000
000000000000000
000000000022222
000220000020000
000220000022222
000000000020000
000000000022222
000000000020000
000000000022222
```

**Expected test output**

```text
000000000000000
044400055555000
040400050005000
044400055555000
000000050005000
000000055555000
000000000000000
000000000033333
000330000030000
000330000033333
000000000030000
000000000033333
000000000030000
000000000033333
```

**Written solution**

Every component starts as color 2. Recolor each component according to how many holes it encloses: 0 holes becomes 3, 1 hole becomes 4, 2 holes becomes 5, and 3 or more holes becomes 6.

**Reference program**

```python
def rule_h39(g):
    out=blank(*size(g))
    for comp in components_of_color(g,2):
        holes=component_hole_count(comp)
        col={0:3,1:4,2:5,3:6}.get(holes,6)
        for r,c in comp:
            out[r][c]=col
    return out
```


### H40 — Fill Only The Max-Seed Frames

**Difficulty:** hard

**Train pairs:** 4

**Skills:** counting, selection by maximum, frame interiors

**Suggested staged path:** Count seeds inside every frame before filling any of them. The key is comparative, not local.


**Train 1 — input**

```text
00000000000000
02222000000000
02802005555500
02002005800500
02222005080500
00000005000500
00000005555500
00777700000000
00788700000000
00700700000000
00777700000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
02222000000000
02002005555500
02002005555500
02222005555500
00000005555500
00000005555500
00777700000000
00777700000000
00777700000000
00777700000000
00000000000000
```


**Train 2 — input**

```text
0000000000000
0000003333000
0000003803000
0000003083000
0000003333000
0666600999990
0680600980090
0600600980090
0600600900890
0666600999990
0000000000000
```

**Train 2 — output**

```text
0000000000000
0000003333000
0000003003000
0000003003000
0000003333000
0666600999990
0600600999990
0600600999990
0600600999990
0666600999990
0000000000000
```


**Train 3 — input**

```text
0000000000000
0444400000000
0480400888880
0408400880080
0400400800080
0444400800080
0000000888880
0022220000000
0028020000000
0020820000000
0022220000000
0000000000000
0000000000000
```

**Train 3 — output**

```text
0000000000000
0444400000000
0444400000000
0444400000000
0444400000000
0444400000000
0000000000000
0022220000000
0022220000000
0022220000000
0022220000000
0000000000000
0000000000000
```


**Train 4 — input**

```text
000000000000000
055555000000000
058085000000000
050805000000000
055555000000000
000000007777770
033330007800070
030030007008070
038830007000070
030830007777770
033330000000000
000000000000000
```

**Train 4 — output**

```text
000000000000000
055555000000000
055555000000000
055555000000000
055555000000000
000000007777770
033330007000070
033330007000070
033330007000070
033330007777770
033330000000000
000000000000000
```

**Test — input**

```text
00000000000000
02222200000000
02800200666660
02080200680060
02000200608060
02222200680060
00000000666660
00999990000000
00980090000000
00900090000000
00900090000000
00999990000000
00000000000000
```

**Expected test output**

```text
00000000000000
02222200000000
02000200666660
02000200666660
02000200666660
02222200666660
00000000666660
00999990000000
00900090000000
00900090000000
00900090000000
00999990000000
00000000000000
```

**Written solution**

Each rectangular frame contains some number of seed dots. Keep all borders, but fill the interior only for those frame(s) that contain the maximum number of seeds; frames with fewer seeds remain hollow.

**Reference program**

```python
def rule_h40(g):
    h,w=size(g)
    rects=[]
    for color in sorted({v for row in g for v in row if v not in {0,8}}):
        for comp in components_of_color(g,color):
            if len(comp)>=8 and is_rect_border_component(g, comp, color):
                r0,c0,r1,c1=bbox(comp)
                count=sum(1 for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]==8)
                rects.append((count,color,comp,(r0,c0,r1,c1)))
    maxcount=max(count for count,_,_,_ in rects)
    out=blank(h,w)
    for count,color,comp,(r0,c0,r1,c1) in rects:
        for r,c in comp:
            out[r][c]=color
        if count==maxcount:
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=color
    return out
```


### H41 — Normalized Shape Subtraction

**Difficulty:** hard

**Train pairs:** 4

**Skills:** shape normalization, mask subtraction, dynamic output

**Suggested staged path:** Normalize the source and the mask into their own top-left-aligned coordinate systems. After alignment, the task is just subtraction.


**Train 1 — input**

```text
000000000000
033000055000
030300005500
033300000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
300
333
```


**Train 2 — input**

```text
0000000000000
0033000000000
0030300055000
0033300005000
0000000005500
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
303
300
```


**Train 3 — input**

```text
00000000000
03330005500
03000000500
03330000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 3 — output**

```text
003
300
333
```


**Train 4 — input**

```text
000000000000
003300000000
003330000550
000300005500
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 4 — output**

```text
300
003
030
```

**Test — input**

```text
0000000000000
0333000000000
0303000055000
0333000005500
0000000005000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
003
300
303
```

**Written solution**

Crop and normalize the color-3 source shape and the color-5 mask shape to their own bounding boxes, overlay them at the same top-left origin, subtract every masked cell from the source, and output the remaining source shape cropped tightly.

**Reference program**

```python
def rule_h41(g):
    src=components_of_color(g,3)
    msk=components_of_color(g,5)
    assert len(src)==1 and len(msk)==1
    src_norm=normalize_component_cells([(r,c,3) for r,c in src[0]])
    msk_norm={(r,c) for r,c,_ in normalize_component_cells([(r,c,1) for r,c in msk[0]])}
    out_cells=[]
    for r,c,v in src_norm:
        if (r,c) not in msk_norm:
            out_cells.append((r,c,3))
    return crop_bbox(render_component_cells(out_cells))
```


### H42 — Voronoi Fill Inside A Frame

**Difficulty:** hard

**Train pairs:** 4

**Skills:** distance reasoning, partitioning, tie handling

**Suggested staged path:** The border only defines the domain. Inside that region, every cell depends on which seed is nearest by Manhattan distance.


**Train 1 — input**

```text
00000000000
01111111110
01200000010
01000000010
01000000410
01003000010
01000000010
01111111110
00000000000
```

**Train 1 — output**

```text
00000000000
01111111110
01222204410
01223344410
01233344410
01333334410
01333334410
01111111110
00000000000
```


**Train 2 — input**

```text
0000000000
0111111110
0120000310
0100000010
0100000010
0100000010
0100000010
0100400010
0111111110
0000000000
```

**Train 2 — output**

```text
0000000000
0111111110
0122233310
0122233310
0122403310
0124440310
0144444010
0144444410
0111111110
0000000000
```


**Train 3 — input**

```text
000000000000
000000000000
001111111100
001200000100
001000000100
001000003100
001000000100
001000000100
001004000100
001111111100
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
001111111100
001222233100
001222333100
001220333100
001244033100
001444403100
001444440100
001111111100
000000000000
```


**Train 4 — input**

```text
000000000000
011111111110
010000002010
010000000010
010000000010
010300000010
010000000010
010000000010
010000040010
010000000010
011111111110
000000000000
```

**Train 4 — output**

```text
000000000000
011111111110
013302222210
013330222210
013333022210
013333342210
013333444410
013334444410
013344444410
013344444410
011111111110
000000000000
```

**Test — input**

```text
0000000000000
0011111111100
0012000000100
0010000000100
0010000030100
0010000000100
0010000000100
0010000000100
0010040000100
0011111111100
0000000000000
```

**Expected test output**

```text
0000000000000
0011111111100
0012222333100
0012223333100
0012233333100
0012043333100
0010444333100
0014444433100
0014444444100
0011111111100
0000000000000
```

**Written solution**

Inside the rectangular frame, fill every interior cell with the color of the nearest seed using Manhattan distance. Seeds remain as they are, the border stays 1, and ties remain black.

**Reference program**

```python
def rule_h42(g):
    h,w=size(g)
    # one frame color 1
    frame=components_of_color(g,1)[0]
    r0,c0,r1,c1=bbox(frame)
    seeds=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in {0,1}]
    out=clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if g[r][c]==1:
                continue
            dists=collections.defaultdict(list)
            for sr,sc,col in seeds:
                d=abs(sr-r)+abs(sc-c)
                dists[d].append(col)
            mind=min(dists)
            cols=set(dists[mind])
            if len(cols)==1:
                out[r][c]=next(iter(cols))
            else:
                out[r][c]=0
    return out
```
