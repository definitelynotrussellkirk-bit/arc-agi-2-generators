# ARC Additional Puzzle Bank — 21 Puzzles (Set 5)

This is a fifth pack of **21 ARC-style puzzles**, continuing the numbering from the earlier banks: `E29–E35`, `M29–M35`, `H29–H35`.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It also introduces a new helper primitive for solver-facing implementations:

```text

stamp_template(grid, anchors, template, center=None, substitute=None, respect_original_nonzero=True, keep_anchor=True)

```

Intuition: Stamp a small template around anchor cells, optionally substituting one template token with the anchor color. This primitive is used directly in `E29`, `M34`, and `H34`, but the set as a whole is intentionally broader than templating alone.

Design goals for this set:

- easy: local completion, geometric reconstruction, symmetry, counting, command rows, cropping

- medium: components, hole filling, ranking, command decoding, midpoint inference, template replay

- hard: nesting depth, relational guide inference, global aggregation, boolean shape ops, perimeter sorting, blocked visibility


## Easy (7)


### E29 — Diagonal Halo Stamp

**Difficulty:** easy

**Train pairs:** 4

**Skills:** template stamping, diagonal offsets, new primitive

**Uses new primitive:** yes (`stamp_template`)

**Suggested staged path:** Ignore colors first. Around each 2, the changed cells always sit at the same four relative offsets.


**Train 1 — input**

```text
00000000
00200000
00000000
00000000
00000200
00000000
00000000
```

**Train 1 — output**

```text
07070000
00200000
07070000
00007070
00000200
00007070
00000000
```


**Train 2 — input**

```text
000020000
000000000
000000000
000000000
000000000
000000000
020000020
000000000
```

**Train 2 — output**

```text
000020000
000707000
000000000
000000000
000000000
707000707
020000020
707000707
```


**Train 3 — input**

```text
0000000000
0000000000
0020000000
0000000200
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0707000000
0020007070
0707000200
0000007070
0000000000
```


**Train 4 — input**

```text
000000000
020000000
000000000
000000000
000020000
000000000
000000000
000000020
000000000
```

**Train 4 — output**

```text
707000000
020000000
707000000
000707000
000020000
000707000
000000707
000000020
000000707
```


**Test — input**

```text
0000000000
0000000020
0000000000
0000000000
0020000000
0000000000
0000020000
0000000000
```

**Expected test output**

```text
0000000707
0000000020
0000000707
0707000000
0020000000
0707707000
0000020000
0000707000
```

**Written solution**

Each red(2) anchor keeps its value and stamps orange(7) onto its four diagonal neighbors, clipped by the grid boundary.

**Reference program**

```python
def rule_e29(g):
    template=[[7,0,7],[0,0,0],[7,0,7]]
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)
```


### E30 — Corner-To-Rectangle Border

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bounding boxes, opposite corners, same-size drawing

**Suggested staged path:** Each color gives you only two cells, so treat them as the extremal points of one larger object.


**Train 1 — input**

```text
000000000
010000000
000000000
000000000
000000000
000000100
000000000
000000000
```

**Train 1 — output**

```text
000000000
011111100
010000100
010000100
010000100
011111100
000000000
000000000
```


**Train 2 — input**

```text
0000000000
0000003000
0200000000
0000000000
0000000030
0000000000
0000000000
0000200000
0000000000
```

**Train 2 — output**

```text
0000000000
0000003330
0222203030
0200203030
0200203330
0200200000
0200200000
0222200000
0000000000
```


**Train 3 — input**

```text
00000000000
00040000000
00000000000
00000000000
00000000000
00000000040
00000000000
```

**Train 3 — output**

```text
00000000000
00044444440
00040000040
00040000040
00040000040
00044444440
00000000000
```


**Train 4 — input**

```text
0000000000
0000000000
0600000000
0000000000
0000008000
0000000000
0000000080
0000000000
0000600000
0000000000
```

**Train 4 — output**

```text
0000000000
0000000000
0666600000
0600600000
0600608880
0600608080
0600608880
0600600000
0666600000
0000000000
```


**Test — input**

```text
000000000000
002000000000
000000000000
000040000000
000000000000
000000000000
000000400000
000000000200
000000000000
```

**Expected test output**

```text
000000000000
002222222200
002000000200
002044400200
002040400200
002040400200
002044400200
002222222200
000000000000
```

**Written solution**

For each nonzero color, the two input cells are opposite corners of an axis-aligned rectangle. Draw the full border of that rectangle in the same color.

**Reference program**

```python
def rule_e30(g):
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
        r0,c0,r1,c1=bbox(cells)
        draw_rect_border(out, r0,c0,r1,c1, color)
    return out
```


### E31 — Vertical Mirror Add

**Difficulty:** easy

**Train pairs:** 4

**Skills:** reflection, symmetry, same-size completion

**Suggested staged path:** Nothing is deleted or moved. The output just adds the symmetric counterpart of each colored cell.


**Train 1 — input**

```text
000000000
000000000
010000000
000000000
000200000
400000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
010000010
000000000
000202000
400000004
000000000
```


**Train 2 — input**

```text
0000000000
0030000000
0000000000
0000500000
0000000000
0000000000
0200000000
0000000000
```

**Train 2 — output**

```text
0000000000
0030000300
0000000000
0000550000
0000000000
0000000000
0200000020
0000000000
```


**Train 3 — input**

```text
60000000
00000000
00100000
00000000
00000000
00070000
```

**Train 3 — output**

```text
60000006
00000000
00100100
00000000
00000000
00077000
```


**Train 4 — input**

```text
00000000000
00000000000
00080000000
00000000000
02000000000
00000000000
00000000000
00004000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000000
00080008000
00000000000
02000000020
00000000000
00000000000
00004040000
00000000000
```


**Test — input**

```text
000000000000
030000000000
000000000000
000060000000
000000000000
000000000000
008000000000
000000000000
```

**Expected test output**

```text
000000000000
030000000030
000000000000
000060060000
000000000000
000000000000
008000000800
000000000000
```

**Written solution**

Mirror every nonzero cell across the vertical center line of the grid, keeping the originals. The result is the union of the input and its left-right reflection.

**Reference program**

```python
def rule_e31(g):
    return mirror_v(g)
```


### E32 — Count-To-Bar

**Difficulty:** easy

**Train pairs:** 4

**Skills:** counting, resize, serialization

**Suggested staged path:** All positions are irrelevant. Only one global quantity survives into the output.


**Train 1 — input**

```text
000000
020000
000020
000000
002000
000000
```

**Train 1 — output**

```text
222
```


**Train 2 — input**

```text
00200000
00000000
00000000
00000200
00000000
02000000
00000020
```

**Train 2 — output**

```text
2222
```


**Train 3 — input**

```text
000000000
020000020
000020000
000202000
000000000
```

**Train 3 — output**

```text
22222
```


**Train 4 — input**

```text
20000000
00000000
00200000
00000000
00000000
00000000
00000000
00000000
```

**Train 4 — output**

```text
22
```


**Test — input**

```text
0000200000
0200000000
0000000020
0000000000
0002000000
2000000000
0000002000
```

**Expected test output**

```text
222222
```

**Written solution**

Count how many red(2) cells appear anywhere in the input. Output a single row whose length equals that count, filled entirely with red(2).

**Reference program**

```python
def rule_e32(g):
    n=sum(1 for row in g for v in row if v==2)
    return [[2]*n]
```


### E33 — Top-Row Column Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** column propagation, same-size transform, command row

**Suggested staged path:** Read the first row as instructions and ignore the zeros beneath it.


**Train 1 — input**

```text
01002030
00000000
00000000
00000000
00000000
00000000
```

**Train 1 — output**

```text
01002030
01002030
01002030
01002030
01002030
01002030
```


**Train 2 — input**

```text
400600000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
400600000
400600000
400600000
400600000
400600000
400600000
400600000
```


**Train 3 — input**

```text
0020050070
0000000000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0020050070
0020050070
0020050070
0020050070
0020050070
```


**Train 4 — input**

```text
08000030
00000000
00000000
00000000
00000000
00000000
00000000
00000000
```

**Train 4 — output**

```text
08000030
08000030
08000030
08000030
08000030
08000030
08000030
08000030
```


**Test — input**

```text
60002000004
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Expected test output**

```text
60002000004
60002000004
60002000004
60002000004
60002000004
60002000004
60002000004
```

**Written solution**

Every nonzero cell in the top row controls its whole column. Copy that color straight down through the entire column, leaving unmarked columns black(0).

**Reference program**

```python
def rule_e33(g):
    h,w=size(g)
    out=blank(h,w)
    for c,v in enumerate(g[0]):
        if v!=0:
            for r in range(h):
                out[r][c]=v
    return out
```


### E34 — Center Completion

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local neighborhoods, pattern completion, same-size repair

**Suggested staged path:** Check zero cells only. Ask when a zero is surrounded by a perfect four-arm pattern of one color.


**Train 1 — input**

```text
00000000
00300030
03030030
00300030
00000400
00004040
00000400
```

**Train 1 — output**

```text
00000000
00300030
03330030
00300030
00000400
00004440
00000400
```


**Train 2 — input**

```text
000000000
000000050
000000050
000200050
002020000
000200000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000050
000000050
000200050
002220000
000200000
000000000
000000000
```


**Train 3 — input**

```text
0000000000
0000000600
0010006060
0101000600
0010550000
0000500000
```

**Train 3 — output**

```text
0000000000
0000000600
0010006660
0111000600
0010550000
0000500000
```


**Train 4 — input**

```text
000000000
003000000
033000000
000080000
000808000
000080000
000000000
000000000
000000000
```

**Train 4 — output**

```text
000000000
003000000
033000000
000080000
000888000
000080000
000000000
000000000
000000000
```


**Test — input**

```text
0000000000
0004000000
0040400000
0004000000
0000000200
0000002020
0660000200
0060000000
```

**Expected test output**

```text
0000000000
0004000000
0044400000
0004000000
0000000200
0000002220
0660000200
0060000000
```

**Written solution**

Whenever a black(0) cell has the same nonzero color directly above, below, left, and right, fill that center cell with that color. Everything else stays unchanged.

**Reference program**

```python
def rule_e34(g):
    h,w=size(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c], g[r+1][c], g[r][c-1], g[r][c+1]]
            if vals[0]!=0 and vals.count(vals[0])==4:
                out[r][c]=vals[0]
    return out
```


### E35 — Crop The Nonzero Object

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bounding-box crop, resize, object extraction

**Suggested staged path:** The output never invents or edits cells; it only removes surrounding empty space.


**Train 1 — input**

```text
000000000
000000000
000012000
000010200
000022200
000000000
000000000
000000000
```

**Train 1 — output**

```text
120
102
222
```


**Train 2 — input**

```text
0000000000
0000000000
0000000000
0000000000
0340000000
0304400000
0034000000
0000000000
0000000000
```

**Train 2 — output**

```text
3400
3044
0340
```


**Train 3 — input**

```text
00000000000
00000056000
00000050600
00000055600
00000005000
00000000000
00000000000
```

**Train 3 — output**

```text
560
506
556
050
```


**Train 4 — input**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0002300000
0002030000
0002220000
0000200000
0000000000
```

**Train 4 — output**

```text
230
203
222
020
```


**Test — input**

```text
000000000000
000000000000
000000000000
000000078000
000000070880
000000007800
000000000000
000000000000
000000000000
```

**Expected test output**

```text
7800
7088
0780
```

**Written solution**

Take the bounding box of all nonzero cells and crop the input down to exactly that rectangle, preserving the internal multicolor pattern.

**Reference program**

```python
def rule_e35(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return crop_bbox(g, cells)
```

## Medium (7)


### M29 — Largest Component Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** connected components, size comparison, cropping

**Suggested staged path:** Separate the nonzero regions first, then compare them before thinking about the output size.


**Train 1 — input**

```text
000000000000
020000000000
020000000000
022000000000
000000000000
000000777700
000000777700
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
7777
7777
```


**Train 2 — input**

```text
00002000000
00002000100
00002201110
00000000100
05000000000
05000000000
05000000000
05550000000
00000000000
```

**Train 2 — output**

```text
500
500
500
555
```


**Train 3 — input**

```text
0000000000000
0033300000000
0030300000000
0033300000000
0000000000000
0000000000000
0000000000000
0000000099900
0000000099900
0000000000000
0000000000000
```

**Train 3 — output**

```text
333
303
333
```


**Train 4 — input**

```text
000000000000
080800000000
088800000000
000000666600
000000666600
000000666600
000000000000
000000000000
```

**Train 4 — output**

```text
6666
6666
6666
```


**Test — input**

```text
0000000000000
0000000004000
0000033304400
0000030300440
0050033300000
0050000000000
0050000000000
0055500000000
0000000000000
0000000000000
```

**Expected test output**

```text
333
303
333
```

**Written solution**

Find the largest connected nonzero component in the grid and crop the output to that component's bounding box. Smaller components are discarded.

**Reference program**

```python
def rule_m29(g):
    comps=components_nonzero(g, treat_colors_separately=False)
    best=max(comps, key=lambda item: len(item[1]))
    return crop_bbox(g, best[1])
```


### M30 — Marker-Framed Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command marker, cropping, padding

**Suggested staged path:** One cell is not part of the object at all: it tells you how to package the object.


**Train 1 — input**

```text
80000000000
00000000000
00000000000
00000012000
00000010200
00000022200
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
88888
81208
81028
82228
88888
```


**Train 2 — input**

```text
4000000000
0000000000
0000000000
0000000000
0000000000
0056000000
0050600000
0055600000
0005000000
0000000000
```

**Train 2 — output**

```text
44444
45604
45064
45564
40504
44444
```


**Train 3 — input**

```text
300000000000
000000000000
000000078000
000000070880
000000007800
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
333333
378003
370883
307803
333333
```


**Train 4 — input**

```text
60000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00003400000
00003044000
00000340000
00000000000
00000000000
```

**Train 4 — output**

```text
666666
634006
630446
603406
666666
```


**Test — input**

```text
500000000000
000000000000
000000000000
000000000000
000000023000
000000020300
000000022200
000000002000
000000000000
000000000000
```

**Expected test output**

```text
55555
52305
52035
52225
50205
55555
```

**Written solution**

Use the top-left marker color as the border color. Crop the rest of the nonzero object to its bounding box, then surround that crop with a one-cell frame of the marker color.

**Reference program**

```python
def rule_m30(g):
    frame_color=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    core=crop_bbox(g, cells)
    ch,cw=size(core)
    out=blank(ch+2, cw+2, frame_color)
    for r in range(ch):
        for c in range(cw):
            out[r+1][c+1]=core[r][c]
    return out
```


### M31 — Fill Enclosed Holes

**Difficulty:** medium

**Train pairs:** 4

**Skills:** enclosure, flood fill, interior detection

**Suggested staged path:** Think in terms of zero-regions, not colored regions. The key question is whether a zero region can escape to the outer border.


**Train 1 — input**

```text
00000000000
02222000000
02002004440
02002004040
02002004040
02222004040
00000004440
03000000000
00000000000
```

**Train 1 — output**

```text
00000000000
02222000000
02772004440
02772004740
02772004740
02222004740
00000004440
03000000000
00000000000
```


**Train 2 — input**

```text
0000000000
0066666600
0060000600
0060000600
0066666600
0000000000
0000000005
0000000000
```

**Train 2 — output**

```text
0000000000
0066666600
0067777600
0067777600
0066666600
0000000000
0000000005
0000000000
```


**Train 3 — input**

```text
000000000000
000000008880
003333008080
003003008080
003003008880
003003000000
003003000000
003333000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000008880
003333008780
003773008780
003773008880
003773000000
003773000000
003333000000
000000000000
000000000000
```


**Train 4 — input**

```text
000000002
055555550
050000050
050000050
050000050
050000050
050000050
055555550
000000000
```

**Train 4 — output**

```text
000000002
055555550
057777750
057777750
057777750
057777750
057777750
055555550
000000000
```


**Test — input**

```text
00000000006
04444000000
04004000000
04004022220
04004020020
04004020020
04444020020
00000020020
00000022220
00000000000
```

**Expected test output**

```text
00000000006
04444000000
04774000000
04774022220
04774027720
04774027720
04444027720
00000027720
00000022220
00000000000
```

**Written solution**

Any black(0) region that is completely enclosed and does not touch the outer border is filled with orange(7). Border-connected zero regions remain black.

**Reference program**

```python
def rule_m31(g):
    out=clone(g)
    for cells,touch in components_zero(g):
        if touch:
            continue
        for r,c in cells:
            out[r][c]=7
    return out
```


### M32 — Area-Sorted Color Row

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component area, ranking, symbolic output

**Suggested staged path:** The output forgets geometry but remembers object size order.


**Train 1 — input**

```text
000000000000
088880000000
088880000000
000000000000
000060000000
000060000000
000060000100
000066600100
000000000110
000000000000
```

**Train 1 — output**

```text
168
```


**Train 2 — input**

```text
0000100000000
0000100040000
0000110044000
0000000004400
0555500000000
0555500000000
0555500000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
145
```


**Train 3 — input**

```text
00000000000
03330000000
03000000000
03330000000
00000000000
00000000000
00000004000
00000004400
08888000440
08888000000
00000000000
```

**Train 3 — output**

```text
438
```


**Train 4 — input**

```text
00000000000000
00000000006000
00000000006000
00000000006000
00000333006660
00000300000000
01000333000000
01000000888800
01100000888800
00000000000000
```

**Train 4 — output**

```text
1638
```


**Test — input**

```text
0000000000000
0000000003330
0040000003000
0044000003330
0004400000000
0000000555500
0000000555500
0000000555500
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
435
```

**Written solution**

Measure the area of each connected colored component. Output a single row containing their colors sorted from smallest component to largest component.

**Reference program**

```python
def rule_m32(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    items=sorted(((len(cells), color) for color,cells in comps), key=lambda x:(x[0], x[1]))
    return [[color for _,color in items]]
```


### M33 — Axis Command Mirror

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command decoding, reflection, same-size duplication

**Suggested staged path:** The nonzero corner cell is a literal command: decode it before touching the object.


**Train 1 — input**

```text
1000000000
0000000000
0120000000
0102000000
0222000000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
1000000000
0000000000
0120000210
0102002010
0222002220
0000000000
0000000000
0000000000
```


**Train 2 — input**

```text
20000000000
00000034000
00000030400
00000004400
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
20000000000
00000034000
00000030400
00000004400
00000000000
00000004400
00000030400
00000034000
00000000000
```


**Train 3 — input**

```text
100000000000
000000000000
000000000000
000000000000
005600000000
005066000000
000560000000
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
100000000000
000000000000
000000000000
000000000000
005600006500
005066660500
000560065000
000000000000
000000000000
000000000000
```


**Train 4 — input**

```text
200000000
078000000
070800000
088800000
000000000
000000000
000000000
000000000
```

**Train 4 — output**

```text
200000000
078000000
070800000
088800000
088800000
070800000
078000000
000000000
```


**Test — input**

```text
10000000000
00000000000
00000000000
00000000000
00000000000
00340000000
00304000000
00044000000
00000000000
00000000000
```

**Expected test output**

```text
10000000000
00000000000
00000000000
00000000000
00000000000
00340004300
00304040300
00044044000
00000000000
00000000000
```

**Written solution**

Read the top-left command cell. If it is blue(1), mirror the non-command pattern across the vertical axis; if it is red(2), mirror it across the horizontal axis. Keep the command cell.

**Reference program**

```python
def rule_m33(g):
    h,w=size(g)
    cmd=g[0][0]
    work=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and not (r==0 and c==0):
                work[r][c]=v
    out = mirror_v(work) if cmd==1 else mirror_h(work)
    out[0][0]=cmd
    return out
```


### M34 — Template Broadcast

**Difficulty:** medium

**Train pairs:** 4

**Skills:** template extraction, broadcast, new primitive

**Uses new primitive:** yes (`stamp_template`)

**Suggested staged path:** The top-left 3×3 patch is an exemplar. The lone 2s elsewhere tell you where to replay it.


**Train 1 — input**

```text
0300000000
3230000000
0300000000
0000000000
0000000000
0000020000
0000000000
0000000020
0000000000
```

**Train 1 — output**

```text
0300000000
3230000000
0300000000
0000000000
0000030000
0000323000
0000030030
0000000323
0000000030
```


**Train 2 — input**

```text
40400000000
02000000000
40400000000
00000000000
00000002000
00000000000
00000000000
00002000000
00000000000
00000000000
```

**Train 2 — output**

```text
40400000000
02000000000
40400000000
00000040400
00000002000
00000040400
00040400000
00002000000
00040400000
00000000000
```


**Train 3 — input**

```text
050000000000
252000000000
050000000000
000000000200
000000000000
000000000000
000000200000
000000000000
```

**Train 3 — output**

```text
050000000000
252000000000
050000000500
000000002220
000000000500
000000500000
000002220000
000000500000
```


**Train 4 — input**

```text
60600000000
02000000000
60600000000
00000000000
00000000020
00000200000
00000000000
00000000000
00000000200
00000000000
00000000000
```

**Train 4 — output**

```text
60600000000
02000000000
60600000000
00000000606
00006060020
00000200606
00006060000
00000006060
00000000200
00000006060
00000000000
```


**Test — input**

```text
070000000000
727000000000
070000000000
000000000000
000002000000
000000000000
000000000000
000000000200
000000000000
000000000000
```

**Expected test output**

```text
070000000000
727000000000
070000000000
000007000000
000072700000
000007000000
000000000700
000000007270
000000000700
000000000000
```

**Written solution**

Treat the top-left 3×3 motif as a template whose center is the digit 2. Stamp that exact 3×3 motif, centered, at every other red(2) anchor in the grid.

**Reference program**

```python
def rule_m34(g):
    template=[row[:3] for row in g[:3]]
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row)
             if v==2 and not (0<=r<3 and 0<=c<3)]
    return stamp_template(g, anchors, template, center=(1,1), keep_anchor=True)
```


### M35 — Midpoint Dots

**Difficulty:** medium

**Train pairs:** 4

**Skills:** pairing, alignment, midpoint inference

**Suggested staged path:** Group cells by color. Each group forms one aligned pair whose halfway point is what matters.


**Train 1 — input**

```text
0000000000
0000000000
0100000100
0000000000
0000000000
0000300000
0000000000
0000300000
```

**Train 1 — output**

```text
0000000000
0000000000
0100900100
0000000000
0000000000
0000300000
0000900000
0000300000
```


**Train 2 — input**

```text
000000000
004000000
000000000
000000000
000000000
004000000
060000060
000000000
000000000
```

**Train 2 — output**

```text
000000000
004000000
000000000
009000000
000000000
004000000
060090060
000000000
000000000
```


**Train 3 — input**

```text
00000000000
00000080000
00000000000
02000000020
00000000000
00000080000
00000000000
```

**Train 3 — output**

```text
00000000000
00000080000
00000000000
02000990020
00000000000
00000080000
00000000000
```


**Train 4 — input**

```text
000000000000
000000000300
005000000000
000000000000
000000070070
000000000300
000000000000
000000000000
005000000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000300
005000000000
000000000900
000000070070
009000000300
000000000000
000000000000
005000000000
000000000000
```


**Test — input**

```text
000000000000
000100000100
000000000000
000000006000
000000000000
040000040000
000000000000
000000006000
000000000000
```

**Expected test output**

```text
000000000000
000100900100
000000000000
000000006000
000000000000
040090049000
000000000000
000000006000
000000000000
```

**Written solution**

For each color, the two input cells define a horizontal or vertical segment of odd length. Mark the exact midpoint of that segment with maroon(9), keeping the endpoints unchanged.

**Reference program**

```python
def rule_m35(g):
    out=clone(g)
    groups=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                groups[v].append((r,c))
    for color,cells in groups.items():
        if len(cells)!=2:
            continue
        (r0,c0),(r1,c1)=cells
        if r0==r1 and abs(c1-c0)%2==0:
            out[r0][(c0+c1)//2]=9
        elif c0==c1 and abs(r1-r0)%2==0:
            out[(r0+r1)//2][c0]=9
    return out
```

## Hard (7)


### H29 — Depth-Colored Nested Frames

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nested containment, ordering, recoloring

**Suggested staged path:** Do not treat all frames equally. Their relative containment determines the output colors.


**Train 1 — input**

```text
000000000
011111110
010000010
010111010
010101010
010111010
010000010
011111110
000000000
```

**Train 1 — output**

```text
000000000
022222220
020000020
020333020
020303020
020333020
020000020
022222220
000000000
```


**Train 2 — input**

```text
00000000000
01111111110
01000000010
01011111010
01010001010
01010101010
01010001010
01011111010
01000000010
01111111110
00000000000
```

**Train 2 — output**

```text
00000000000
02222222220
02000000020
02033333020
02030003020
02030403020
02030003020
02033333020
02000000020
02222222220
00000000000
```


**Train 3 — input**

```text
000000000000
011111111110
010000000010
010111111010
010100001010
010100001010
010111111010
010000000010
011111111110
000000000000
```

**Train 3 — output**

```text
000000000000
022222222220
020000000020
020333333020
020300003020
020300003020
020333333020
020000000020
022222222220
000000000000
```


**Train 4 — input**

```text
0000000000000
0111111111110
0100000000010
0101111111010
0101000001010
0101011101010
0101010101010
0101011101010
0101000001010
0101111111010
0100000000010
0111111111110
0000000000000
```

**Train 4 — output**

```text
0000000000000
0222222222220
0200000000020
0203333333020
0203000003020
0203044403020
0203040403020
0203044403020
0203000003020
0203333333020
0200000000020
0222222222220
0000000000000
```


**Test — input**

```text
000000000000
011111111110
010000000010
010111111010
010100001010
010101101010
010101101010
010100001010
010111111010
010000000010
011111111110
000000000000
```

**Expected test output**

```text
000000000000
022222222220
020000000020
020333333020
020300003020
020304403020
020304403020
020300003020
020333333020
020000000020
022222222220
000000000000
```

**Written solution**

The input consists of nested rectangular frames. Recolor the outermost frame to red(2), the next nested frame to green(3), the next to yellow(4), and so on in depth order, preserving the frame shapes.

**Reference program**

```python
def rule_h29(g):
    h,w=size(g)
    comps=components_nonzero(g, treat_colors_separately=False)
    items=[]
    for _,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        area=(r1-r0+1)*(c1-c0+1)
        items.append((-(area), cells))
    items.sort(key=lambda x:x[0])
    out=blank(h,w)
    for idx,(_,cells) in enumerate(items):
        color=2+idx
        for r,c in cells:
            out[r][c]=color
    return out
```


### H30 — Guide-Selected Mirror

**Difficulty:** hard

**Train pairs:** 4

**Skills:** relational command, axis inference, reflection

**Suggested staged path:** There is no symbolic command value. The two guide cells communicate the axis through their alignment.


**Train 1 — input**

```text
00500000500
00000000000
01200000000
01020000000
02220000000
00000000000
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
00500000500
00000000000
01200000000
01020000000
02220000000
01020000000
01200000000
00000000000
00000000000
```


**Train 2 — input**

```text
000000000000
500000000000
000000034000
000000030400
000000004400
000000000000
000000000000
000000000000
500000000000
000000000000
```

**Train 2 — output**

```text
000000000000
500000000000
000430034000
004030030400
004400004400
000000000000
000000000000
000000000000
500000000000
000000000000
```


**Train 3 — input**

```text
00000000000
00000000000
00000000000
00560000000
00506600000
00056000000
00000000000
00000000000
00000000000
00000000000
00050000500
```

**Train 3 — output**

```text
00000000000
00000000000
00000000000
00560006000
00506660000
00056060000
00000000000
00000000000
00000000000
00000000000
00050000500
```


**Train 4 — input**

```text
0000000000
0780000005
0708000000
0888000000
0000000000
0000000000
0000000005
0000000000
```

**Train 4 — output**

```text
0000000000
0780000875
0708008070
0888008880
0000000000
0000000000
0000000005
0000000000
```


**Test — input**

```text
00000500000
00000000000
00000000000
00000000000
03400000000
03040000000
00440000000
00000000000
00000000000
00000500000
```

**Expected test output**

```text
00000500000
00000000000
00000000000
00000000000
03400000430
03040004030
00440004400
00000000000
00000000000
00000500000
```

**Written solution**

Find the two gray(5) guide cells. If they share a row, mirror the non-guide pattern across the horizontal axis; if they share a column, mirror it across the vertical axis. Keep the guides.

**Reference program**

```python
def rule_h30(g):
    h,w=size(g)
    guides=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    work=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and v!=5:
                work[r][c]=v
    if len(guides)==2 and guides[0][0]==guides[1][0]:
        out=mirror_h(work)
    else:
        out=mirror_v(work)
    for r,c in guides:
        out[r][c]=5
    return out
```


### H31 — Color-Frequency Ranking

**Difficulty:** hard

**Train pairs:** 4

**Skills:** global counting, aggregation by color, symbolic output

**Suggested staged path:** Same-color pieces may be split across the grid. Aggregate by color before ranking.


**Train 1 — input**

```text
000000000000
022220000000
022220000000
000000400000
000000440000
000000044000
000000003000
000000003000
000000003300
000000000000
```

**Train 1 — output**

```text
243
```


**Train 2 — input**

```text
0000000000000
0555500000000
0555500000000
0555500000000
0000000000000
0000600000000
0000600000100
0000600001110
0000666000100
0101010000000
0000000000000
```

**Train 2 — output**

```text
516
```


**Train 3 — input**

```text
00000000000
08880000070
08000000000
08880000000
00000000000
08080800000
00000070700
00000077700
00000000000
00000000000
```

**Train 3 — output**

```text
87
```


**Train 4 — input**

```text
00000000000009
00000000004000
00000000004409
00000000000440
09990000000009
09990000000000
00000000000009
00000000000000
00000000000000
```

**Train 4 — output**

```text
94
```


**Test — input**

```text
202020000000
060000000000
060000000000
060000000000
066600000000
000000022200
000000022200
000000000000
000000000000
000000000000
```

**Expected test output**

```text
26
```

**Written solution**

Count the total number of cells of each nonzero color across the whole grid, combining all components of that color. Output one row of colors ordered from highest total count to lowest.

**Reference program**

```python
def rule_h31(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    order=sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))
    return [[color for color,_ in order]]
```


### H32 — Normalized Shape XOR

**Difficulty:** hard

**Train pairs:** 4

**Skills:** shape normalization, boolean composition, resize

**Suggested staged path:** The two shapes are compared after cropping away their surrounding whitespace.


**Train 1 — input**

```text
0000000000
0110000000
0011000000
0000000000
0000000000
0000000000
0000002220
0000002000
0000000000
0000000000
```

**Train 1 — output**

```text
007
777
```


**Train 2 — input**

```text
000000000000
000000000100
000000001110
000000000100
000000000000
022000000000
002200000000
000000000000
000000000000
```

**Train 2 — output**

```text
700
700
070
```


**Train 3 — input**

```text
00000000000
00000000000
00111000000
00101000000
00000000000
00000000000
00000000000
00000002200
00000022000
00000000000
00000000000
```

**Train 3 — output**

```text
700
077
```


**Train 4 — input**

```text
0000000000000
0100000000000
0111000000000
0000000000000
0000000022200
0000000002000
0000000000000
0000000000000
```

**Train 4 — output**

```text
077
707
```


**Test — input**

```text
000000000000
011100000000
000110000000
000000000000
000000000000
000000000000
000000022200
000000220000
000000000000
000000000000
```

**Expected test output**

```text
7007
7777
```

**Written solution**

Crop the color-1 shape and the color-2 shape to their own bounding boxes, align both cropped binaries to the top-left corner of a common canvas, and output their XOR silhouette in orange(7).

**Reference program**

```python
def rule_h32(g):
    cells1=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    cells2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    s1=binary_shape_from_cells(cells1)
    s2=binary_shape_from_cells(cells2)
    h=max(len(s1), len(s2))
    w=max(len(s1[0]), len(s2[0]))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            a = r < len(s1) and c < len(s1[0]) and s1[r][c] == 1
            b = r < len(s2) and c < len(s2[0]) and s2[r][c] == 1
            if bool(a) ^ bool(b):
                out[r][c]=7
    return out
```


### H33 — Perimeter-Sorted Shape Stack

**Difficulty:** hard

**Train pairs:** 4

**Skills:** perimeter computation, sorting, shape serialization

**Suggested staged path:** The output keeps whole shapes, but their order comes from a geometric statistic, not from position or color alone.


**Train 1 — input**

```text
0000000000000
0200000000000
0200000088800
0220000080000
0000000088800
0060000000000
0060000000000
0060000000000
0066600000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
888
800
888
000
600
600
600
666
000
200
200
220
```


**Train 2 — input**

```text
000000000000
000000040000
000000044000
000000004400
000006000000
000006000000
020006000000
020006660000
022000000000
000000000000
```

**Train 2 — output**

```text
600
600
600
666
000
400
440
044
000
200
200
220
```


**Train 3 — input**

```text
00000000000000
08880000000000
08000000000000
08880000000000
00000000000000
00000000000000
00000000000000
00000000004000
00020000004400
00020000000440
00022000000000
00000000000000
```

**Train 3 — output**

```text
888
800
888
000
400
440
044
000
200
200
220
```


**Train 4 — input**

```text
00000000000
00000060000
00000060000
00000060000
00000066600
00004000000
00004400000
02000448880
02000008000
02200008880
00000000000
```

**Train 4 — output**

```text
888
800
888
000
600
600
600
666
000
400
440
044
000
200
200
220
```


**Test — input**

```text
0000000000000
0400000088800
0440000080000
0044000088800
0000000000000
0000000000000
0000002000000
0000002000000
0000002200000
0000000000000
```

**Expected test output**

```text
888
800
888
000
400
440
044
000
200
200
220
```

**Written solution**

Compute the perimeter of each connected colored component. Crop each component to its own bounding box, sort the cropped shapes from largest perimeter to smallest, and stack them top-to-bottom with one blank row between them.

**Reference program**

```python
def rule_h33(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    items=[]
    for color,cells in comps:
        shape=crop_bbox(g, cells)
        per=perimeter_of_cells(cells)
        items.append((-per, color, shape))
    items.sort(key=lambda x:(x[0], x[1]))
    width=max(len(shape[0]) for _,_,shape in items)
    height=sum(len(shape) for _,_,shape in items) + (len(items)-1)
    out=blank(height, width)
    cur=0
    for i,(_,color,shape) in enumerate(items):
        sh,sw=size(shape)
        for r in range(sh):
            for c in range(sw):
                out[cur+r][c]=shape[r][c]
        cur += sh
        if i != len(items)-1:
            cur += 1
    return out
```


### H34 — Anchor Motif Substitution

**Difficulty:** hard

**Train pairs:** 4

**Skills:** template substitution, broadcast, new primitive

**Uses new primitive:** yes (`stamp_template`)

**Suggested staged path:** The top-left motif is not literal everywhere: one token inside it stands for the anchor's color.


**Train 1 — input**

```text
79700000000
90900000000
79700000000
00000000000
00000000000
00000200000
00000000000
00000000400
00000000000
00000000000
```

**Train 1 — output**

```text
79700000000
90900000000
79700000000
00000000000
00007270000
00002220000
00007277470
00000004440
00000007470
00000000000
```


**Train 2 — input**

```text
090000000000
979000000000
090000000000
000000000000
000000003000
000000000000
000060000000
000000000000
000000000000
```

**Train 2 — output**

```text
090000000000
979000000000
090000000000
000000003000
000000033300
000060003000
000666000000
000060000000
000000000000
```


**Train 3 — input**

```text
70700000000
99900000000
70700000000
00000000000
00000000000
00000600000
00000000000
00000000000
00000000800
00000000000
00000000000
```

**Train 3 — output**

```text
70700000000
99900000000
70700000000
00000000000
00007070000
00006660000
00007070000
00000007070
00000008880
00000007070
00000000000
```


**Train 4 — input**

```text
9790000000000
7070000000000
9790000000000
0000000080000
0000000000000
0000000000200
0000000000000
0000060000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
9790000000000
7070000000000
9790000878000
0000000787000
0000000872720
0000000007270
0000676002720
0000767000000
0000676000000
0000000000000
```


**Test — input**

```text
797000000000
090000000000
797000000000
000000000000
000004000000
000000000000
000000000000
000000000600
000000000000
000000000000
```

**Expected test output**

```text
797000000000
090000000000
797000000000
000074700000
000004000000
000074700000
000000007670
000000000600
000000007670
000000000000
```

**Written solution**

Use the top-left 3×3 motif as a template. Wherever the template contains 9, substitute the color of the current anchor cell; all other template colors stay literal. Stamp that substituted motif around every anchor outside the template block.

**Reference program**

```python
def rule_h34(g):
    template=[row[:3] for row in g[:3]]
    anchors=[(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row)
             if v!=0 and not (0<=r<3 and 0<=c<3)]
    return stamp_template(g, anchors, template, center=(1,1), substitute={9:'anchor'}, keep_anchor=True)
```


### H35 — Ray Intersections With Blockers

**Difficulty:** hard

**Train pairs:** 4

**Skills:** line of sight, set intersection, blockers

**Suggested staged path:** First think of horizontal visibility from the 2s and vertical visibility from the 3s. The answer is where those two sets overlap.


**Train 1 — input**

```text
0000300000
0200050000
0000000000
0050000000
0000000000
0000000200
0030000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000800000
0000000000
0000000000
0000000000
0080800000
0000000000
0000000000
```


**Train 2 — input**

```text
000000000
000030000
050000000
000000000
020000020
000000000
000000000
000000300
000000005
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000080800
000000000
000000000
000000000
000000000
```


**Train 3 — input**

```text
000000000000
000000300000
002000000000
000000000000
000000000000
000500000000
000000000000
020000000000
000300000000
000000000500
```

**Train 3 — output**

```text
000000000000
000000000000
000000800000
000000000000
000000000000
000000000000
000000000000
000800800000
000000000000
000000000000
```


**Train 4 — input**

```text
00000000000
00000300000
00000000000
02000000000
00000000500
00500000000
00000000200
00300000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000000
00000000000
00000800000
00000000000
00000000000
00800800000
00000000000
00000000000
```


**Test — input**

```text
0000000300
0000000000
0200000000
0000000050
0000000000
0005000000
0000000000
0000002000
0003000000
0000000000
```

**Expected test output**

```text
0000000000
0000000000
0000000800
0000000000
0000000000
0000000000
0000000000
0008000800
0000000000
0000000000
```

**Written solution**

Red(2) sources project horizontally through zeros until blocked by any nonzero cell, and blue(3) sources project vertically the same way. Output cyan(8) only at cells reached by both a red horizontal ray and a blue vertical ray.

**Reference program**

```python
def rule_h35(g):
    h,w=size(g)
    horiz=blank(h,w)
    vert=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==2:
                for dc in (-1,1):
                    cc=c+dc
                    while 0<=cc<w and g[r][cc]==0:
                        horiz[r][cc]=1
                        cc += dc
            elif v==3:
                for dr in (-1,1):
                    rr=r+dr
                    while 0<=rr<h and g[rr][c]==0:
                        vert[rr][c]=1
                        rr += dr
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if horiz[r][c] and vert[r][c]:
                out[r][c]=8
    return out
```
