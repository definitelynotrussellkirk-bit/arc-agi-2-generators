# ARC Additional Puzzle Bank — 21 Puzzles (Set 9)

This ninth pack continues the numbering with **`E57–E63`**, **`M57–M63`**, and **`H57–H63`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
orbit_cells(base_grid, cells, pivot, turns=(0,1,2,3), keep_original=True, recolor_by_turn=None)
```

Intuition: describe a set of colored cells once, then replay those offsets around a pivot by quarter turns. The primitive can preserve the original cells, or treat the original as just one orbit position and recolor each turn separately. It is used directly in **E57**, **M57**, and **H57**.

Design goals for this set:

- easy: symmetry, diagonal completion, local growth, rectangle inference, counting, header slicing, and single-object extraction

- medium: selective symmetry, cross-header slicing, ranked object selection, command strips, color-filtered hole filling, boolean panel logic, and object abstraction

- hard: recolored rotational replay, multi-frame insertion, nested-frame ring coloring, analogical translation, relational matrices, obstacle-aware routing, and normalized object packing

## Easy (7)

### E57 — Orbit Copy Around Pivot

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rotational symmetry, pivot reasoning, copying

**Suggested staged path:** Find the unique pivot first. Then reuse the same offsets from that pivot in the other three quarter-turn positions.

**Train 1 — input**

```text
0000000
0020000
0003000
0005000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0020000
0003020
0035300
0203000
0000200
0000000
```

**Train 2 — input**

```text
000000000
000070000
000400000
000060000
000050000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000070000
000400000
000060400
070656070
004060000
000004000
000070000
000000000
```

**Train 3 — input**

```text
0000000
0002000
0800000
0005000
0000000
0000000
0000000
```

**Train 3 — output**

```text
0000000
0002800
0800000
0205020
0000080
0082000
0000000
```

**Train 4 — input**

```text
000000000
000000000
003000000
000000000
000950000
000000000
000000000
000000000
000000000
```

**Train 4 — output**

```text
000000000
000000000
003000300
000090000
000959000
000090000
003000300
000000000
000000000
```

**Test — input**

```text
000000000
000200000
000070000
004000000
000050000
000000000
000000000
000000000
000000000
```

**Test — output**

```text
000000000
000200000
000074000
004000020
007050700
020000400
000470000
000002000
000000000
```

**Written solution**

Locate the single pivot cell colored 5. Every other nonzero cell is copied to its 90°, 180°, and 270° rotations around that pivot.

**Reference program**

```python
def rule_e57(g):
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    return orbit_cells(g, cells, pivot, turns=(0,1,2,3), keep_original=True)
```

### E58 — Diagonal Segment Completion

**Difficulty:** easy

**Train pairs:** 4

**Skills:** diagonal detection, endpoint completion, same-color linking

**Suggested staged path:** Ignore orthogonal neighbors. Pair the matching-color endpoints that already lie on one diagonal and fill the cells between them.

**Train 1 — input**

```text
0000000
0200000
0000000
0007000
0000200
0700000
0000000
```

**Train 1 — output**

```text
0000000
0200000
0020000
0007000
0070200
0700000
0000000
```

**Train 2 — input**

```text
00000000
00000300
06000000
00000000
00300000
00006000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000300
06003000
00630000
00360000
00006000
00000000
00000000
```

**Train 3 — input**

```text
000080000
000000000
000000000
000020000
000000008
000000000
020000000
000000000
000000000
```

**Train 3 — output**

```text
000080000
000008000
000000800
000020080
000200008
002000000
020000000
000000000
000000000
```

**Train 4 — input**

```text
000000000
000000090
000004000
000000000
000090000
004000000
000000000
```

**Train 4 — output**

```text
000000000
000000090
000004900
000049000
000490000
004000000
000000000
```

**Test — input**

```text
000000000
030000000
000000000
000080000
000000000
000003000
000000080
000000000
000000000
```

**Test — output**

```text
000000000
030000000
003000000
000380000
000038000
000003800
000000080
000000000
000000000
```

**Written solution**

For each color, find its two endpoints on a 45° diagonal and fill the whole diagonal segment connecting them.

**Reference program**

```python
def rule_e58(g):
    out=clone(g)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        dr=r2-r1; dc=c2-c1
        if abs(dr)!=abs(dc):
            continue
        sr=0 if dr==0 else (1 if dr>0 else -1)
        sc=0 if dc==0 else (1 if dc>0 else -1)
        steps=abs(dr)
        for k in range(steps+1):
            out[r1+k*sr][c1+k*sc]=color
    return out
```

### E59 — Plus Expansion from Seeds

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local growth, orthogonal neighbors, same-color dilation

**Suggested staged path:** Treat each nonzero cell as a center. Add only the four orthogonal neighbors, not diagonals.

**Train 1 — input**

```text
0000000
0000000
0020000
0000000
0000060
0000000
0000000
```

**Train 1 — output**

```text
0000000
0020000
0222000
0020060
0000666
0000060
0000000
```

**Train 2 — input**

```text
00000000
00000300
00000000
00000000
00000000
00700000
00000000
00000000
```

**Train 2 — output**

```text
00000300
00003330
00000300
00000000
00700000
07770000
00700000
00000000
```

**Train 3 — input**

```text
000000000
080000000
000000000
000040000
000000000
000000000
000000000
```

**Train 3 — output**

```text
080000000
888000000
080040000
000444000
000040000
000000000
000000000
```

**Train 4 — input**

```text
000000000
000000000
000000900
000000000
000000000
000000000
005000000
000000000
000000000
```

**Train 4 — output**

```text
000000000
000000900
000009990
000000900
000000000
005000000
055500000
005000000
000000000
```

**Test — input**

```text
000000000
000000000
003000000
000000000
000020000
000000000
000000700
000000000
000000000
```

**Test — output**

```text
000000000
003000000
033300000
003020000
000222000
000020700
000007770
000000700
000000000
```

**Written solution**

Each nonzero seed grows into a plus of Manhattan radius 1 in the same color, clipped by the grid boundary.

**Reference program**

```python
def rule_e59(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=v
                for nr,nc in orth_neighbors(r,c,h,w):
                    out[nr][nc]=v
    return out
```

### E60 — Rectangle Border from Four Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** corners, rectangle inference, border drawing

**Suggested staged path:** Look for four equal-colored markers that already sit at rectangle corners. Use them as a frame recipe.

**Train 1 — input**

```text
00000000
02002000
00000707
00000000
00000000
02002000
00000707
00000000
```

**Train 1 — output**

```text
00000000
02222000
02002777
02002707
02002707
02222707
00000777
00000000
```

**Train 2 — input**

```text
003000300
000000000
000000000
000000000
003000300
080800000
000000000
000000000
080800000
```

**Train 2 — output**

```text
003333300
003000300
003000300
003000300
003333300
088800000
080800000
080800000
088800000
```

**Train 3 — input**

```text
0000000909
0400040000
0000000000
0000000000
0000000000
0400040000
0000000909
```

**Train 3 — output**

```text
0000000999
0444440909
0400040909
0400040909
0400040909
0444440909
0000000999
```

**Train 4 — input**

```text
000000000
000000022
006000600
000000000
000000000
000000022
006000600
000000000
```

**Train 4 — output**

```text
000000000
000000022
006666622
006000622
006000622
006000622
006666600
000000000
```

**Test — input**

```text
0000000077
0030000300
0000000000
0000000000
0000000000
0000000000
0030000300
0000000000
0000000077
```

**Test — output**

```text
0000000077
0033333377
0030000377
0030000377
0030000377
0030000377
0033333377
0000000077
0000000077
```

**Written solution**

For each color whose four cells form the corners of an axis-aligned rectangle, draw that whole rectangle border.

**Reference program**

```python
def rule_e60(g):
    out=blank(*size(g))
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=4:
            continue
        rs=sorted(set(r for r,c in pts)); cs=sorted(set(c for r,c in pts))
        if len(rs)==2 and len(cs)==2 and set(pts)=={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}:
            draw_rect_border(out, rs[0], cs[0], rs[1], cs[1], color)
    return out
```

### E61 — Color Histogram Column

**Difficulty:** easy

**Train pairs:** 4

**Skills:** counting, dynamic output, sorting by color

**Suggested staged path:** You do not need the positions. Only the multiset of colors matters.

**Train 1 — input**

```text
020000
002000
000000
000400
000070
```

**Train 1 — output**

```text
2
2
4
7
```

**Train 2 — input**

```text
300000
000000
003000
000003
080000
000008
```

**Train 2 — output**

```text
3
3
3
8
8
```

**Train 3 — input**

```text
0000000
0900020
0002000
5000000
0000000
```

**Train 3 — output**

```text
2
2
5
9
```

**Train 4 — input**

```text
0000004
0000000
0040000
0000000
0000400
0000000
1000000
```

**Train 4 — output**

```text
1
4
4
4
```

**Test — input**

```text
0020000
0000090
0020000
0600000
0000000
0000006
```

**Test — output**

```text
2
2
6
6
9
```

**Written solution**

Count how many times each nonzero color appears. Output a single column, stacking colors in ascending color order and repeating each color by its count.

**Reference program**

```python
def rule_e61(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    col=[]
    for color in sorted(counts):
        col.extend([color]*counts[color])
    return [[v] for v in col] if col else [[0]]
```

### E62 — Header-Selected Columns

**Difficulty:** easy

**Train pairs:** 4

**Skills:** matrix slicing, header markers, dynamic output

**Suggested staged path:** Solve the first row first: it only tells you which columns survive.

**Train 1 — input**

```text
080808
123456
654321
102030
778899
```

**Train 1 — output**

```text
246
531
000
789
```

**Train 2 — input**

```text
80800
31415
92653
58979
```

**Train 2 — output**

```text
34
96
59
```

**Train 3 — input**

```text
0880080
2468135
5318642
9090909
1234567
```

**Train 3 — output**

```text
463
314
090
236
```

**Train 4 — input**

```text
8008
4444
1234
7654
0101
```

**Train 4 — output**

```text
44
14
74
01
```

**Test — input**

```text
080880
271828
314159
265358
```

**Test — output**

```text
782
115
635
```

**Written solution**

Use the 8s in the top row as column selectors. Remove the header row and keep only those selected columns from the remaining rows.

**Reference program**

```python
def rule_e62(g):
    cols=[c for c,v in enumerate(g[0]) if v==8]
    if not cols:
        return [[0]]
    return [[row[c] for c in cols] for row in g[1:]]
```

### E63 — Crop the Largest Component

**Difficulty:** easy

**Train pairs:** 4

**Skills:** connected components, area comparison, cropping

**Suggested staged path:** Compare whole components, not individual cells. Once you know the largest one, the output is just its crop.

**Train 1 — input**

```text
000000000
022200000
020000000
000000000
000000000
000007700
000007700
000000000
000000000
```

**Train 1 — output**

```text
222
200
```

**Train 2 — input**

```text
0000000000
0000003300
0000000330
0000000000
0000000000
0444000000
0440000000
0400000000
0000000000
0000000000
```

**Train 2 — output**

```text
444
440
400
```

**Train 3 — input**

```text
06660000000
00600000000
00000000000
00000000000
00000008800
00000008800
00000008000
00000000000
```

**Train 3 — output**

```text
88
88
80
```

**Train 4 — input**

```text
0000000000
0550000000
0550000000
0500000000
0000022200
0000002000
0000000000
0000000000
0000000000
```

**Train 4 — output**

```text
55
55
50
```

**Test — input**

```text
0000000000
0330000000
0300000000
0000000000
0000777000
0000707000
0000777000
0000000000
0000000000
0000000000
```

**Test — output**

```text
777
707
777
```

**Written solution**

Find the largest same-color connected component and crop the output to its bounding box.

**Reference program**

```python
def rule_e63(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t:(-len(t[1]), t[0], component_top_left(t[1])))
    color,cells=comps[0]
    return crop_bbox(g, cells)
```

## Medium (7)

### M57 — Selector-Color Orbit Copy

**Difficulty:** medium

**Train pairs:** 4

**Skills:** selector cell, pivot reasoning, selective copying

**Suggested staged path:** The pivot still governs the geometry, but only one color is allowed to orbit. Read that color from the selector first.

**Train 1 — input**

```text
200000000
000200000
000020000
000000000
000050000
000000000
070000000
000000000
000000000
```

**Train 1 — output**

```text
200000000
000200000
000020000
000000020
002050200
020000000
070020000
000002000
000000000
```

**Train 2 — input**

```text
400000000
000000800
004000000
000040000
000050000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
400000000
000000800
004000400
000040000
000454000
000040000
004000400
000000000
000000000
```

**Train 3 — input**

```text
6000000
0060000
0006000
0005000
0000000
0000030
0000000
```

**Train 3 — output**

```text
6000000
0060000
0006060
0065600
0606000
0000630
0000000
```

**Train 4 — input**

```text
700000000
000000000
000700000
000700000
000050000
000000000
000000200
000000000
000000000
```

**Train 4 — output**

```text
700000000
000000000
000700000
000707700
000050000
007707000
000007200
000000000
000000000
```

**Test — input**

```text
300000000
000030000
000300000
000000000
000050000
000000800
003000000
000000000
000000000
```

**Test — output**

```text
300000000
000030000
003300300
000000300
030050030
003000800
003003300
000030000
000000000
```

**Written solution**

Read the selected color from the top-left cell. Keep the whole input, and orbit only cells of that color around the pivot 5 by quarter turns.

**Reference program**

```python
def rule_m57(g):
    target=g[0][0]
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and (r,c)!=(0,0)]
    return orbit_cells(g, cells, pivot, turns=(0,1,2,3), keep_original=True)
```

### M58 — Cross-Selected Submatrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** row selection, column selection, submatrix extraction

**Suggested staged path:** Read the two headers separately. The left edge chooses rows; the top edge chooses columns.

**Train 1 — input**

```text
080808
012345
854321
098765
801010
```

**Train 1 — output**

```text
531
000
```

**Train 2 — input**

```text
00808
82718
02818
81828
01111
89900
```

**Train 2 — output**

```text
78
88
90
```

**Train 3 — input**

```text
088008
031415
892653
058979
032384
862643
```

**Train 3 — output**

```text
923
623
```

**Train 4 — input**

```text
000808
870707
012345
054321
888888
```

**Train 4 — output**

```text
77
88
```

**Test — input**

```text
0080808
0135792
8246813
8357924
```

**Test — output**

```text
483
594
```

**Written solution**

The 8s in the top row choose columns and the 8s in the left column choose rows. Output the cross-product submatrix from the interior data.

**Reference program**

```python
def rule_m58(g):
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    if not rows or not cols:
        return [[0]]
    return [[g[r][c] for c in cols] for r in rows]
```

### M59 — Ranked Component Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component ranking, selector cell, cropping

**Suggested staged path:** Do not guess a component by color. Sort them by size first, then take the selector-th one.

**Train 1 — input**

```text
1000000000
0022000000
0000000000
0000000000
0333000000
0300000000
0000004400
0000004400
0000000000
0000000000
```

**Train 1 — output**

```text
22
```

**Train 2 — input**

```text
2000000000
0550000000
0055000000
0000000000
0000000770
0066000770
0060000000
0060000000
0000000000
0000000000
```

**Train 2 — output**

```text
66
60
60
```

**Train 3 — input**

```text
30000000000
00002200000
00000000000
08880000000
00800000000
00000009900
00000009900
00000009000
00000000000
```

**Train 3 — output**

```text
99
99
90
```

**Train 4 — input**

```text
2000000000
0000003330
0000000000
0000000000
0440000000
0400007700
0400007700
0000000000
0000000000
0000000000
```

**Train 4 — output**

```text
44
40
40
```

**Test — input**

```text
20000000000
02200000000
00000000000
00006660000
00006000000
00000000000
00000008800
00000008800
00000008000
00000000000
```

**Test — output**

```text
666
600
```

**Written solution**

The top-left selector gives a 1-based rank. Ignore that selector cell, sort same-color components by area ascending, and output the selected component cropped to its box.

**Reference program**

```python
def rule_m59(g):
    k=g[0][0]
    comps=components_nonzero(g, treat_colors_separately=True, exclude={(0,0)})
    comps.sort(key=lambda t:(len(t[1]), t[0], component_top_left(t[1])))
    color,cells=comps[k-1]
    return crop_bbox(g, cells)
```

### M60 — Command Strip Transform

**Difficulty:** medium

**Train pairs:** 4

**Skills:** symbolic commands, rotation, packing

**Suggested staged path:** Treat the top row as a program, not as part of the object.

**Train 1 — input**

```text
124
020
222
002
```

**Train 1 — output**

```text
02000200002
22200220222
00202200020
```

**Train 2 — input**

```text
310
660
066
```

**Train 2 — output**

```text
6600660
0660066
```

**Train 3 — input**

```text
2241
4000
4400
4000
```

**Train 3 — output**

```text
4440444040040
0400040044044
0000000040040
```

**Train 4 — input**

```text
432
777
070
```

**Train 4 — output**

```text
0700070007
7770777077
0000000007
```

**Test — input**

```text
142
030
333
300
```

**Test — output**

```text
03003000330
33303330033
30000300030
```

**Written solution**

Crop the motif below the command row. For each nonzero command code in the top row, output the corresponding transformed motif and pack the results left to right with one blank column between them.

**Reference program**

```python
def rule_m60(g):
    codes=[v for v in g[0] if v in (1,2,3,4)]
    motif=crop_bbox(g[1:])
    outs=[transform_code(motif, code) for code in codes]
    return pack_horiz(outs, sep=1)
```

### M61 — Fill Holes Only for the Selected Color

**Difficulty:** medium

**Train pairs:** 4

**Skills:** hole detection, selector cell, object filtering

**Suggested staged path:** The interior geometry matters only for one chosen color. Everything else is a distractor.

**Train 1 — input**

```text
4000000000
0444006660
0404006060
0444006660
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0444006660
0444006060
0444006660
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
60000000000
00000000000
00666000000
00606000000
00666000000
00000077700
00000070700
00000077700
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00666000000
00666000000
00666000000
00000077700
00000070700
00000077700
00000000000
00000000000
00000000000
```

**Train 3 — input**

```text
700000000000
077700000000
070700000000
077700000000
000000044400
000000040400
000000044400
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
077700000000
077700000000
077700000000
000000044400
000000040400
000000044400
000000000000
000000000000
000000000000
```

**Train 4 — input**

```text
40000000000
00000000000
00000444000
00000404000
00000444000
00000000000
06660000000
06060000000
06660000000
00000000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000000
00000444000
00000444000
00000444000
00000000000
06660000000
06060000000
06660000000
00000000000
00000000000
```

**Test — input**

```text
600000000000
000000000000
006660000000
006060000000
006660000000
000000000000
000000777000
044400707000
040400777000
044400000000
000000000000
000000000000
```

**Test — output**

```text
000000000000
000000000000
006660000000
006660000000
006660000000
000000000000
000000777000
044400707000
040400777000
044400000000
000000000000
000000000000
```

**Written solution**

Read the target color from the top-left selector. Fill enclosed holes only inside components of that color; leave all other colors unchanged.

**Reference program**

```python
def rule_m61(g):
    target=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    return fill_holes_selected(gg, target)
```

### M62 — Boolean Overlay of Two Panels

**Difficulty:** medium

**Train pairs:** 4

**Skills:** panel split, boolean operations, support masks

**Suggested staged path:** First separate the two panels. Then ignore color identities and think in terms of occupied versus empty cells.

**Train 1 — input**

```text
100000000
070050070
770050770
000050000
```

**Train 1 — output**

```text
0770
7770
0000
```

**Train 2 — input**

```text
200000000
770057000
070050770
000750007
```

**Train 2 — output**

```text
7000
0700
0007
```

**Train 3 — input**

```text
3000000
0705070
7775070
0705070
```

**Train 3 — output**

```text
000
707
000
```

**Train 4 — input**

```text
100000000
700750070
000050700
077050700
```

**Train 4 — output**

```text
7077
0700
0770
```

**Test — input**

```text
300000000
770050700
070050770
007050070
```

**Test — output**

```text
7000
0070
0000
```

**Written solution**

The top-left code chooses the operation on the left and right panel supports: 1 = union, 2 = intersection, 3 = xor. Return the resulting panel as color 7 on black.

**Reference program**

```python
def rule_m62(g):
    code=g[0][0]
    # find full 5 column below row 1
    h,w=size(g)
    split=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(1,h)):
            split=c
            break
    left=[row[:split] for row in g[1:]]
    right=[row[split+1:] for row in g[1:]]
    H=len(left); W=len(left[0])
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            a = left[r][c]!=0
            b = right[r][c]!=0
            cond = (a or b) if code==1 else (a and b) if code==2 else (a ^ b)
            if cond:
                out[r][c]=7
    return out
```

### M63 — Component Center Markers

**Difficulty:** medium

**Train pairs:** 4

**Skills:** bounding boxes, object abstraction, centers

**Suggested staged path:** Do not preserve full objects. Collapse each one to a single representative cell.

**Train 1 — input**

```text
000000000
022200000
022200000
022200000
000000000
000006660
000006660
000006660
000000000
```

**Train 1 — output**

```text
000000000
000000000
002000000
000000000
000000000
000000000
000000600
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0000003330
0000003330
0000003330
0000000000
0888000000
0888000000
0888000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000300
0000000000
0000000000
0000000000
0080000000
0000000000
0000000000
0000000000
```

**Train 3 — input**

```text
00000000000
04440000000
04440000000
04440000000
00000007770
00000007770
00000007770
00000000000
00000000000
```

**Train 3 — output**

```text
00000000000
00000000000
00400000000
00000000000
00000000000
00000000700
00000000000
00000000000
00000000000
```

**Train 4 — input**

```text
00000000000
00000000000
00555000000
00555000000
00555000000
00000000000
00000099900
00000099900
00000099900
00000000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000000
00000000000
00050000000
00000000000
00000000000
00000000000
00000009000
00000000000
00000000000
00000000000
```

**Test — input**

```text
00000000000
00000002220
00000002220
00000002220
00004440000
00004440000
06664440000
06660000000
06660000000
00000000000
00000000000
```

**Test — output**

```text
00000000000
00000000000
00000000200
00000000000
00000000000
00000400000
00000000000
00600000000
00000000000
00000000000
00000000000
```

**Written solution**

For every connected same-color component, compute its bounding-box center and place one cell of that color there in an otherwise blank grid of the same size.

**Reference program**

```python
def rule_m63(g):
    h,w=size(g)
    out=blank(h,w)
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        r0,c0,r1,c1=bbox(cells)
        cr=(r0+r1)//2; cc=(c0+c1)//2
        out[cr][cc]=color
    return out
```

## Hard (7)

### H57 — Legend-Recolored Orbit

**Difficulty:** hard

**Train pairs:** 4

**Skills:** rotational symmetry, recoloring, legend decoding

**Suggested staged path:** Separate the geometry from the palette. The source object only tells you the shape and offsets; the top row tells you the colors of the four rotations.

**Train 1 — input**

```text
234600000
000000000
000900000
000990000
000050000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
234600000
000000000
000200000
000223300
000653000
006644000
000004000
000000000
000000000
```

**Train 2 — input**

```text
78240000000
00000000000
00000000000
00000100000
00000110000
00000510000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
78240000000
00000000000
00000000000
00000700000
00004470000
00044588000
00002280000
00000200000
00000000000
00000000000
00000000000
```

**Train 3 — input**

```text
369200000
000080000
000088000
000000000
000050000
000000000
000000000
000000000
000000000
```

**Train 3 — output**

```text
369200000
000030000
000033000
002000000
022050660
000000600
000990000
000090000
000000000
```

**Train 4 — input**

```text
42780000000
00000000000
00000000000
00006000000
00006600000
00006500000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 4 — output**

```text
42780000000
00000000000
00000000000
00004000000
00004222000
00008570000
00088870000
00000070000
00000000000
00000000000
00000000000
```

**Test — input**

```text
28370000000
00000000000
00000000000
00000900000
00000900000
00009590000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Test — output**

```text
28370000000
00000000000
00000000000
00000200000
00000700000
00077538000
00000700000
00000300000
00000000000
00000000000
00000000000
```

**Written solution**

Read the four legend colors from the top row. Orbit the source object around the pivot 5 at quarter turns, recoloring the original orientation and the three rotated copies according to legend order.

**Reference program**

```python
def rule_h57(g):
    legend=[v for v in g[0] if v!=0][:4]
    pivot=find_unique(g,5)
    cells=[(r,c,v) for r,row in enumerate(g[1:], start=1) for c,v in enumerate(row) if v not in (0,5)]
    base=blank(*size(g))
    for c,v in enumerate(legend):
        base[0][c]=v
    pr,pc=pivot
    base[pr][pc]=5
    return orbit_cells(base, cells, pivot, turns=(0,1,2,3), keep_original=False, recolor_by_turn={i:legend[i] for i in range(4)})
```

### H58 — Commanded Multi-Frame Insertion

**Difficulty:** hard

**Train pairs:** 4

**Skills:** template extraction, frame reasoning, local transforms

**Suggested staged path:** Find the source motif once. Then each empty target frame becomes a transformed copy request.

**Train 1 — input**

```text
0000000000000000000
0000000010000020000
0999990088888088888
0920090080008080008
0922290080008080008
0900290080008080008
0999990088888088888
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```

**Train 1 — output**

```text
0000000000000000000
0000000010000020000
0999990088888088888
0920090082008080228
0922290082228080208
0900290080028082208
0999990088888088888
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```

**Train 2 — input**

```text
0000000000000000000
0000000000000000000
0000000030000040000
0999990088888088888
0906690080008080008
0966090080008080008
0906090080008080008
0999990088888088888
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```

**Train 2 — output**

```text
0000000000000000000
0000000000000000000
0000000030000040000
0999990088888088888
0906690080608080608
0966090080668086608
0906090086608080668
0999990088888088888
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
0000000000000000000
```

**Train 3 — input**

```text
00000000000000000000
00000000000000000000
00000000000000000000
00000000200000100000
09999900888880888880
09444900800080800080
09040900800080800080
09040900800080800080
09999900888880888880
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Train 3 — output**

```text
00000000000000000000
00000000000000000000
00000000000000000000
00000000200000100000
09999900888880888880
09444900800480844480
09040900844480804080
09040900800480804080
09999900888880888880
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Train 4 — input**

```text
00000000000000000000
00000000040000030000
00999990088888088888
00970790080008080008
00977790080008080008
00907090080008080008
00999990088888088888
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Train 4 — output**

```text
00000000000000000000
00000000040000030000
00999990088888088888
00970790080708080708
00977790087778087778
00907090087078087078
00999990088888088888
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Test — input**

```text
00000000000000000000
00000000000000000000
00000000100000200000
09999900888880888880
09330900800080800080
09033900800080800080
09003900800080800080
09999900888880888880
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Test — output**

```text
00000000000000000000
00000000000000000000
00000000100000200000
09999900888880888880
09330900833080800380
09033900803380803380
09003900800380833080
09999900888880888880
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
00000000000000000000
```

**Written solution**

Extract the motif from inside the unique 9-bordered source frame. For every 8-bordered target frame, read the command cell just above its left border and place the commanded transform of the source motif into that frame interior.

**Reference program**

```python
def rule_h58(g):
    # source motif inside 9-frame; target 8-frames have code cell above left corner
    out=clone(g)
    source=None
    for (r0,c0,r1,c1),cells in frame_info_by_color(g,9):
        source=subgrid(g,r0+1,c0+1,r1-1,c1-1)
        break
    if source is None:
        return g
    for (r0,c0,r1,c1),cells in frame_info_by_color(g,8):
        code = g[r0-1][c0] if r0-1>=0 else 1
        motif=transform_code(source, code)
        mh,mw=size(motif)
        ih,iw=r1-r0-1,c1-c0-1
        sr=r0+1+(ih-mh)//2
        sc=c0+1+(iw-mw)//2
        for r in range(sr, r1):
            for c in range(c0+1,c1):
                out[r][c]=0
        for r in range(mh):
            for c in range(mw):
                if motif[r][c]!=0:
                    out[sr+r][sc+c]=motif[r][c]
    return out
```

### H59 — Nested Frame Depth Coloring

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nested structures, frame depth, legend use

**Suggested staged path:** Do not fill all interiors at once. Color the region between one frame and the next inner frame.

**Train 1 — input**

```text
23000000000
00000000000
00888888888
00800000008
00808888808
00808000808
00808000808
00808000808
00808888808
00800000008
00888888888
```

**Train 1 — output**

```text
23000000000
00000000000
00888888888
00822222228
00828888828
00828333828
00828333828
00828333828
00828888828
00822222228
00888888888
```

**Train 2 — input**

```text
4620000000000
0000000000000
0088888888888
0080000000008
0080888888808
0080800000808
0080808880808
0080808080808
0080808880808
0080800000808
0080888888808
0080000000008
0088888888888
```

**Train 2 — output**

```text
4620000000000
0000000000000
0088888888888
0084444444448
0084888888848
0084866666848
0084868886848
0084868286848
0084868886848
0084866666848
0084888888848
0084444444448
0088888888888
```

**Train 3 — input**

```text
730000000000
000000000000
088888888800
080000000800
080888880800
080800080800
080800080800
080800080800
080888880800
080000000800
088888888800
000000000000
```

**Train 3 — output**

```text
730000000000
000000000000
088888888800
087777777800
087888887800
087833387800
087833387800
087833387800
087888887800
087777777800
088888888800
000000000000
```

**Train 4 — input**

```text
258000000000000
000000000000000
000000000000000
000888888888880
000800000000080
000808888888080
000808000008080
000808088808080
000808080808080
000808088808080
000808000008080
000808888888080
000800000000080
000888888888880
000000000000000
```

**Train 4 — output**

```text
258000000000000
000000000000000
000000000000000
000888888888880
000822222222280
000828888888280
000828555558280
000828588858280
000828588858280
000828588858280
000828555558280
000828888888280
000822222222280
000888888888880
000000000000000
```

**Test — input**

```text
3740000000000
0000000000000
0088888888888
0080000000008
0080888888808
0080800000808
0080808880808
0080808080808
0080808880808
0080800000808
0080888888808
0080000000008
0088888888888
```

**Test — output**

```text
3740000000000
0000000000000
0088888888888
0083333333338
0083888888838
0083877777838
0083878887838
0083878487838
0083878887838
0083877777838
0083888888838
0083333333338
0088888888888
```

**Written solution**

Use the top-row legend as outer-to-inner fill colors. Keep the 8-colored frame borders, and fill each ring region between nested frames with the corresponding legend color; the innermost open region gets the deepest legend color.

**Reference program**

```python
def rule_h59(g):
    out=clone(g)
    legend=[v for v in g[0] if v!=0]
    infos=[info for info in frame_info_by_color(g,8) if info[0][0]>0]  # frames below legend row
    infos.sort(key=lambda t: ((t[0][2]-t[0][0]+1)*(t[0][3]-t[0][1]+1)), reverse=True)
    bbs=[bb for bb,_ in infos]
    for idx,(r0,c0,r1,c1) in enumerate(bbs):
        inner = bbs[idx+1] if idx+1 < len(bbs) else None
        color = legend[min(idx, len(legend)-1)]
        for r in range(r0+1, r1):
            for c in range(c0+1, c1):
                if inner and (inner[0] <= r <= inner[2] and inner[1] <= c <= inner[3]):
                    continue
                out[r][c]=color
    return out
```

### H60 — Analogical Translation Across Panels

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, translation vectors, panel decomposition

**Suggested staged path:** The first two panels teach a motion. Measure that motion, then apply it to the third panel’s object.

**Train 1 — input**

```text
02005000050070
22205020050770
00005222050000
00005000050000
```

**Train 1 — output**

```text
0000
0070
0770
0000
```

**Train 2 — input**

```text
00305000054400
03305003050400
00005033050000
00005000050000
```

**Train 2 — output**

```text
0000
4400
0400
0000
```

**Train 3 — input**

```text
00000500000500800
06600500000508880
06000506600500000
00000506000500000
```

**Train 3 — output**

```text
00000
00800
08880
00000
```

**Train 4 — input**

```text
09005009055500
09905009955000
00005000050000
00005000050000
```

**Train 4 — output**

```text
0550
0500
0000
0000
```

**Test — input**

```text
00200500000507000
02200500200577700
00000502200500000
00000500000500000
```

**Test — output**

```text
00000
07000
77700
00000
```

**Written solution**

Compare the object positions in the first and second panels to infer one translation vector. Apply that same vector to the third panel object and return only the translated third panel.

**Reference program**

```python
def rule_h60(g):
    h,w=size(g)
    split_cols=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    a=subgrid(g,0,0,h-1,split_cols[0]-1)
    b=subgrid(g,0,split_cols[0]+1,h-1,split_cols[1]-1)
    cpanel=subgrid(g,0,split_cols[1]+1,h-1,w-1)
    comp_a=components_nonzero(a, treat_colors_separately=False)[0][1]
    comp_b=components_nonzero(b, treat_colors_separately=False)[0][1]
    comp_c=components_nonzero(cpanel, treat_colors_separately=False)[0][1]
    ra,ca,_,_=bbox(comp_a)
    rb,cb,_,_=bbox(comp_b)
    dr,dc=rb-ra, cb-ca
    H,W=size(cpanel)
    out=blank(H,W)
    for r,c in comp_c:
        nr,nc=r+dr,c+dc
        if 0<=nr<H and 0<=nc<W:
            out[nr][nc]=cpanel[r][c]
    return out
```

### H61 — Area Comparison Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** component abstraction, pairwise relations, dynamic output

**Suggested staged path:** The output is not a picture of the input. It is a table comparing every object to every other object.

**Train 1 — input**

```text
000000000
022000333
000000000
000000000
000000000
000440000
000440000
000000000
000000000
```

**Train 1 — output**

```text
133
213
221
```

**Train 2 — input**

```text
0000000000
0555000000
0500000660
0000000000
0000000000
0000000000
0077000000
0077000000
0070000000
0000000000
```

**Train 2 — output**

```text
123
313
221
```

**Train 3 — input**

```text
00000000000
00220000000
00000000000
00000000000
00000888000
00000888000
00000000000
09990000000
00000000000
00000000000
00000000000
```

**Train 3 — output**

```text
133
212
231
```

**Train 4 — input**

```text
000000000000
033300000000
000000000000
000000004400
000000004400
000000000000
000077000000
000070000000
000070000000
000000000000
```

**Train 4 — output**

```text
133
211
211
```

**Test — input**

```text
00000000000
02200000000
00000055500
00000000000
00000000000
00000000000
00770000000
00770008880
00000008000
00000000000
00000000000
```

**Test — output**

```text
1333
2133
2211
2211
```

**Written solution**

Order the components by top-left position. Build an N×N matrix: 1 on ties, 2 when the row component has larger area than the column component, and 3 when it has smaller area.

**Reference program**

```python
def rule_h61(g):
    comps=[cells for color,cells in components_nonzero(g, treat_colors_separately=True)]
    comps.sort(key=component_top_left)
    n=len(comps)
    out=blank(n,n)
    areas=[len(c) for c in comps]
    for i in range(n):
        for j in range(n):
            if areas[i]==areas[j]:
                out[i][j]=1
            elif areas[i]>areas[j]:
                out[i][j]=2
            else:
                out[i][j]=3
    return out
```

### H62 — Blocked L-Path Connector

**Difficulty:** hard

**Train pairs:** 4

**Skills:** path selection, obstacle avoidance, multi-object routing

**Suggested staged path:** Try the two possible L routes separately. One of them is blocked, and the other is the intended connection.

**Train 1 — input**

```text
00000000
02009000
00009070
00009000
00009000
00002900
00000070
00000000
```

**Train 1 — output**

```text
00000000
02009000
02009070
02009070
02009070
02222970
00000070
00000000
```

**Train 2 — input**

```text
00000000
00900300
06900000
00900000
00900000
00390000
00006000
00000000
```

**Train 2 — output**

```text
00000000
00900300
06900300
06900300
06900300
06333300
06666000
00000000
```

**Train 3 — input**

```text
000000000
040009000
000009080
000009000
000009000
000000900
000004000
000000080
000000000
```

**Train 3 — output**

```text
000000000
040009000
040009080
040009080
040009080
040000980
044444080
000000080
000000000
```

**Train 4 — input**

```text
000000000
000900500
070900000
000900000
000900000
000590000
000000700
000000000
```

**Train 4 — output**

```text
000000000
000900500
070900500
070900500
070900500
070555500
077777700
000000000
```

**Test — input**

```text
000000000
002000900
000000960
000000900
000000900
000009000
000000200
000600000
000000000
```

**Test — output**

```text
000000000
002000900
002000960
002000960
002000960
002009060
002222260
000666660
000000000
```

**Written solution**

Connect each same-color endpoint pair with an L-shaped path of that color. Prefer horizontal-then-vertical if it is clear; otherwise use vertical-then-horizontal. Blocker cells colored 9 remain unchanged.

**Reference program**

```python
def rule_h62(g):
    out=clone(g)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,9):
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        p1,p2=pts
        cand1=path_hv(p1,p2)
        cand2=path_vh(p1,p2)
        pts_use = cand1 if clear_path(g,cand1,color) else cand2
        for r,c in pts_use:
            out[r][c]=color
    return out
```

### H63 — Rotate-Tall Pack by Area

**Difficulty:** hard

**Train pairs:** 4

**Skills:** component extraction, conditional rotation, sorting and packing

**Suggested staged path:** Standardize each object before sorting. The key normalization is to rotate only the tall ones.

**Train 1 — input**

```text
000000000000
020000000000
020006600000
020000660000
020000000000
000000000000
000000004400
000000004400
000000000000
000000000000
```

**Train 1 — output**

```text
22220440660
00000440066
```

**Train 2 — input**

```text
00000000000
00000003000
00000003000
00000003000
07770000000
07000000000
00000000000
00000088000
00000088000
00000000000
00000000000
```

**Train 2 — output**

```text
7770880333
7000880000
```

**Train 3 — input**

```text
0000000000000
0500000000000
0500002220000
0500000000000
0500000000000
0000000000000
0000000009900
0000000009000
0000000009000
0000000000000
```

**Train 3 — output**

```text
555509990222
000000090000
```

**Train 4 — input**

```text
000000000000
004000000000
004000000000
004000066600
000000006000
000000000000
000000000000
077000000000
077000000000
000000000000
000000000000
```

**Train 4 — output**

```text
6660770444
0600770000
```

**Test — input**

```text
0000000000000
0300000000000
0300008880000
0300008000000
0300000000000
0000000000000
0000000000000
0000000055000
0000000055000
0000000000000
0000000000000
```

**Test — output**

```text
33330550888
00000550800
```

**Written solution**

Crop every same-color component. If a crop is taller than it is wide, rotate it clockwise once. Then sort components by area descending and color ascending, and pack them left to right with one blank column between them.

**Reference program**

```python
def rule_h63(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        crop=grid_from_component(g,cells)
        h,w=size(crop)
        if h>w:
            crop=rotate_times(crop,1)
            h,w=size(crop)
        comps.append((len(cells), color, crop))
    comps.sort(key=lambda t:(-t[0], t[1]))
    return pack_horiz([crop for _,_,crop in comps], sep=1)
```
