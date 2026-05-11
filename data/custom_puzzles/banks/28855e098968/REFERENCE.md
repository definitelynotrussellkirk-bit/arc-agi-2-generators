# ARC Additional Puzzle Bank — 21 Puzzles (Set 18)

This eighteenth pack continues the numbering with **`E120–E126`**, **`M120–M126`**, and **`H120–H126`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
offset_scatter(offsets, anchors, paint_color=None, transforms=None, recolor=None, merge="overwrite|max|keep")
```

Intuition: represent a motif as a set of relative offsets from an origin, then replay that cloud around one or more anchors, optionally rotating, recoloring, and merging copies. This primitive is used directly in **E120**, **M120**, and **H120**.

## E120 — Offset Cloud Replay

**Difficulty:** easy

**Train pairs:** 4

**Skills:** relative offsets, anchor replay, same-size painting

**Suggested staged path:** Ignore the special 9 except as an origin. First read the 4-cells as a set of offsets, then replay that offset cloud around every 2 anchor.

**Train 1 — input**

```text
000000000000
094000000000
044000000000
004000000000
000000000000
000000000000
000000002000
000000000000
000020000000
000000000000
```

**Train 1 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000002400
000000004400
000024000400
000044000000
```

**Train 2 — input**

```text
0000000000000
0040000000000
0094000000000
0044000000000
0000000200000
0000000000000
0000000002000
0000000000000
0000020000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0000000000000
0000000000000
0000000400000
0000000240000
0000000444000
0000000002400
0000040004400
0000024000000
0000044000000
0000000000000
```

**Train 3 — input**

```text
00000000000
00944000000
00400000000
00040000000
00000000000
00000002000
00000000000
00020000000
00000000000
```

**Train 3 — output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000002440
00000004000
00024400400
00040000000
```

**Train 4 — input**

```text
000000000000
004000000000
094000000000
044000000000
004000000000
000000000000
000002000000
000000002000
000000000000
000020000000
000000000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000400000
000002400400
000004402400
000004404400
000024000400
000044000000
000004000000
```

**Test — input**

```text
000000000000
004000000000
009400000000
004440000000
000000000200
000000000000
000000002000
000000000000
000020000000
000000000000
000000000000
```

**Test — output**

```text
000000000000
000000000000
000000000000
000000000400
000000000240
000000004444
000000002400
000040004440
000024000000
000044400000
000000000000
```

**Written solution**

Find the 9 cell and record the relative positions of all 4-cells around it. Erase the template. For every 2 in the grid, place 4s at those same relative offsets and keep the anchor itself as 2.

**Reference program**

```python
def rule_e120(g):
    h,w=size(g)
    ref=find_color_positions(g,9)[0]
    offsets=[(r-ref[0], c-ref[1]) for r,row in enumerate(g) for c,v in enumerate(row) if v==4]
    anchors=find_color_positions(g,2)
    out=blank(h,w)
    for ar,ac in anchors:
        out[ar][ac]=2
    out=offset_scatter(out, offsets, anchors, paint_color=4, merge='overwrite')
    for ar,ac in anchors:
        out[ar][ac]=2
    return out
```

## E121 — Endpoint Segment Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** row completion, endpoint reasoning, same-size fill

**Suggested staged path:** Look one row at a time. Whenever a color appears as separated endpoints in a row, fill the horizontal run between them.

**Train 1 — input**

```text
000000000000
020002000000
000000000000
000000000000
000400000400
000000000000
707000000000
000000000000
```

**Train 1 — output**

```text
000000000000
022222000000
000000000000
000000000000
000444444400
000000000000
777000000000
000000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00300000300
00000000000
00000000000
06006000000
00000000000
00000050005
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00333333300
00000000000
00000000000
06666000000
00000000000
00000055555
00000000000
```

**Train 3 — input**

```text
9009000000
0000000000
0000000000
0040000400
0000000000
0000020002
0000000000
```

**Train 3 — output**

```text
9999000000
0000000000
0000000000
0044444400
0000000000
0000022222
0000000000
```

**Train 4 — input**

```text
0000000000000
0000000000000
0000500000500
0000000000000
3000003000000
0000000000000
0000000070007
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000000000
0000555555500
0000000000000
3333333000000
0000000000000
0000000077777
0000000000000
```

**Test — input**

```text
000000000000
004000000400
000000000000
600060000000
000000000000
000000000000
000000000000
000000020002
000000000000
```

**Test — output**

```text
000000000000
004444444400
000000000000
666660000000
000000000000
000000000000
000000000000
000000022222
000000000000
```

**Written solution**

For each row, find the leftmost and rightmost occurrence of each nonzero color. Fill every cell between those endpoints with that same color.

**Reference program**

```python
def rule_e121(g):
    out=clone(g)
    h,w=size(g)
    for r in range(h):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        for col, cols in positions.items():
            if len(cols)>=2:
                c0,c1=min(cols), max(cols)
                for c in range(c0,c1+1):
                    out[r][c]=col
    return out
```

## E122 — Opposite Corner Rectangle Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rectangle inference, corner markers, area fill

**Suggested staged path:** Treat each color as giving you two opposite corners. Convert the sparse clues into full solid rectangles.

**Train 1 — input**

```text
00000000000
02000000000
00000000000
00002000000
00000050000
00000000000
00000000050
00000000000
```

**Train 1 — output**

```text
00000000000
02222000000
02222000000
02222000000
00000055550
00000055550
00000055550
00000000000
```

**Train 2 — input**

```text
003000000000
000000000000
000003000000
000000000000
000000000000
000000060000
000000000000
000000000000
000000000060
```

**Train 2 — output**

```text
003333000000
003333000000
003333000000
000000000000
000000000000
000000066660
000000066660
000000066660
000000066660
```

**Train 3 — input**

```text
0000000000
0000040000
0000000000
0700000000
0000000040
0007000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000044440
0000044440
0777044440
0777044440
0777000000
0000000000
```

**Train 4 — input**

```text
0000000000000
0000000020000
0090000000000
0000000000020
0000000000000
0000000000000
0000900000000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000022220
0099900022220
0099900022220
0099900000000
0099900000000
0099900000000
0000000000000
0000000000000
0000000000000
```

**Test — input**

```text
000000000000
050000000000
000000000000
000000030000
000005000000
000000000000
000000000000
000000000030
000000000000
```

**Test — output**

```text
000000000000
055555000000
055555000000
055555033330
055555033330
000000033330
000000033330
000000033330
000000000000
```

**Written solution**

For each nonzero color, take its two marked cells as opposite corners of an axis-aligned rectangle. Fill the whole rectangle with that color.

**Reference program**

```python
def rule_e122(g):
    out=blank(*size(g))
    positions=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                positions[v].append((r,c))
    for col, cells in positions.items():
        if len(cells)>=2:
            (r0,c0),(r1,c1)=cells[0], cells[-1]
            rr0,cc0=min(r0,r1),min(c0,c1)
            rr1,cc1=max(r0,r1),max(c0,c1)
            for r in range(rr0,rr1+1):
                for c in range(cc0,cc1+1):
                    out[r][c]=col
    return out
```

## E123 — Guide Reflection

**Difficulty:** easy

**Train pairs:** 4

**Skills:** mirror symmetry, guide line, same-size copy

**Suggested staged path:** The full-height 8 column is the mirror. Copy the left motif across that line without deleting the original.

**Train 1 — input**

```text
0000008000000
0200008000000
0020008000000
0000008000000
0004008000000
0000008000000
0030008000000
0000008000000
0000008000000
```

**Train 1 — output**

```text
0000008000000
0200008000020
0020008000200
0000008000000
0004008004000
0000008000000
0030008000300
0000008000000
0000008000000
```

**Train 2 — input**

```text
00000800000
50000800000
00500800000
00000800000
00000800000
00070800000
00000800000
00000800000
```

**Train 2 — output**

```text
00000800000
50000800005
00500800500
00000800000
00000800000
00070807000
00000800000
00000800000
```

**Train 3 — input**

```text
000000080000000
000000080000000
030000080000000
000600080000000
000000080000000
000000080000000
000060080000000
002000080000000
000000080000000
000000080000000
```

**Train 3 — output**

```text
000000080000000
000000080000000
030000080000030
000600080006000
000000080000000
000000080000000
000060080060000
002000080000200
000000080000000
000000080000000
```

**Train 4 — input**

```text
0000008000000
0000008000000
0090008000000
0400008000000
0000008000000
0000408000000
0000008000000
0000008000000
0000008000000
```

**Train 4 — output**

```text
0000008000000
0000008000000
0090008000900
0400008000040
0000008000000
0000408040000
0000008000000
0000008000000
0000008000000
```

**Test — input**

```text
0000008000000
0020008000000
0000008000000
0000508000000
0000008000000
0500008000000
0007008000000
0000008000000
```

**Test — output**

```text
0000008000000
0020008000200
0000008000000
0000508050000
0000008000000
0500008000050
0007008007000
0000008000000
```

**Written solution**

Find the vertical guide made entirely of 8s. For every nonzero non-guide cell on the left, reflect it to the symmetric position on the right and keep the original cells and the guide.

**Reference program**

```python
def rule_e123(g):
    h,w=size(g)
    out=clone(g)
    guide=[c for c in range(w) if all(g[r][c]==8 for r in range(h))][0]
    for r in range(h):
        for c in range(guide):
            v=g[r][c]
            if v!=0 and v!=8:
                mc=guide + (guide-c)
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

## E124 — Sorted Count Strip

**Difficulty:** easy

**Train pairs:** 4

**Skills:** counting, sorting by color, crop output

**Suggested staged path:** Ignore positions. Count how many times each color appears, then write a compact strip ordered by color number.

**Train 1 — input**

```text
200000
002000
050000
000000
000030
050000
```

**Train 1 — output**

```text
22355
```

**Train 2 — input**

```text
0000004
0700000
0040000
0000040
0000000
0002000
0000000
```

**Train 2 — output**

```text
24447
```

**Train 3 — input**

```text
90000000
00003000
00000003
00900000
00000020
02000000
```

**Train 3 — output**

```text
223399
```

**Train 4 — input**

```text
000000005
050000000
000500000
000000200
400000000
```

**Train 4 — output**

```text
24555
```

**Test — input**

```text
00600000
00000002
06000000
00000000
00004000
00000400
20000000
```

**Test — output**

```text
224466
```

**Written solution**

Count every nonzero cell by color. Output a single row containing each color repeated its count times, ordered from the smallest color to the largest.

**Reference program**

```python
def rule_e124(g):
    counts=Counter(v for row in g for v in row if v!=0)
    colors=sorted(counts)
    row=[]
    for col in colors:
        row.extend([col]*counts[col])
    return [row if row else [0]]
```

## E125 — Largest Component Crop

**Difficulty:** easy

**Train pairs:** 4

**Skills:** component detection, area comparison, crop output

**Suggested staged path:** Separate the disconnected nonzero components. Keep only the biggest one and crop tightly around it.

**Train 1 — input**

```text
000000000000
010000000000
011000000000
001100000000
000000000000
000000002200
000000002000
000777000000
000000000000
```

**Train 1 — output**

```text
100
110
011
```

**Train 2 — input**

```text
000000000000
000000099000
001010009900
001110000000
000100000000
000000000000
000000005500
000000000500
000000000000
000000000000
```

**Train 2 — output**

```text
101
111
010
```

**Train 3 — input**

```text
00000000000
01110000000
00100000000
00100000000
00000004400
00000004400
00300000000
00330000000
```

**Train 3 — output**

```text
111
010
010
```

**Train 4 — input**

```text
0000000000000
2200000000000
0201100000000
0000100000000
0000110000000
0000000006660
0000000006000
0000000000000
0000000000000
```

**Train 4 — output**

```text
110
010
011
```

**Test — input**

```text
000000000000
011000000000
001100000000
000000000000
000000000000
000000088800
003300008000
003000000000
000000000000
```

**Test — output**

```text
110
011
```

**Written solution**

Find all connected nonzero components. Choose the one with the most cells and output its tight bounding box.

**Reference program**

```python
def rule_e125(g):
    comps=components_nonzero(g)
    cells=sorted(comps, key=lambda x:(-len(x), bbox(x)[0], bbox(x)[1]))[0]
    return crop_bbox(g, cells)
```

## E126 — Complete the 2x2 Blocks

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local completion, 2x2 reasoning, same-size repair

**Suggested staged path:** Scan each 2x2 window. Whenever three cells already agree on a color and one corner is empty, fill the missing corner.

**Train 1 — input**

```text
0000000000
0040000000
0440000200
0000000220
0000077000
0000070000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0440000000
0440000220
0000000220
0000077000
0000077000
0000000000
0000000000
```

**Train 2 — input**

```text
00005500000
00000500000
00000000000
00000000000
00000000000
03000000000
03300000900
00000009900
00000000000
```

**Train 2 — output**

```text
00005500000
00005500000
00000000000
00000000000
00000000000
03300000000
03300009900
00000009900
00000000000
```

**Train 3 — input**

```text
000000000
000000660
000000600
000200000
002288000
000008000
000000000
```

**Train 3 — output**

```text
000000000
000000660
000000660
002200000
002288000
000088000
000000000
```

**Train 4 — input**

```text
000000000000
000000000000
070000004400
077000000400
000000000000
000000300000
000003300000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000000
077000004400
077000004400
000000000000
000003300000
000003300000
000000000000
```

**Test — input**

```text
00000000000
00550000000
00500000000
00000000200
00000002200
00006000000
00006600000
00000000000
```

**Test — output**

```text
00000000000
00550000000
00550000000
00000002200
00000002200
00006600000
00006600000
00000000000
```

**Written solution**

In every 2x2 block that contains three copies of the same nonzero color and one zero, replace the zero with that color. Apply this everywhere until no such block remains.

**Reference program**

```python
def rule_e126(g):
    out=clone(g)
    h,w=size(g)
    changed=True
    while changed:
        changed=False
        for r in range(h-1):
            for c in range(w-1):
                vals=[out[r][c],out[r][c+1],out[r+1][c],out[r+1][c+1]]
                nonzero=[v for v in vals if v!=0]
                if vals.count(0)==1 and len(nonzero)==3 and len(set(nonzero))==1:
                    idx=vals.index(0)
                    rr=r + idx//2
                    cc=c + idx%2
                    out[rr][cc]=nonzero[0]
                    changed=True
    return out
```

## M120 — Rotated Offset Replay

**Difficulty:** medium

**Train pairs:** 4

**Skills:** relative offsets, rotation commands, anchor replay

**Suggested staged path:** Read the 7-cells as an offset cloud around the 9 origin. Then let each anchor color tell you which rotation to apply before replaying the cloud.

**Train 1 — input**

```text
000000000000
007000000000
009700000000
007700000000
000000000000
000000500000
000000000000
000000000000
002000003000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000770000
000007570000
000000000000
007000000000
002700073700
007700077000
000000000000
000000000000
```

**Train 2 — input**

```text
0000000000000
0000000000000
0970000000000
0770000000000
0070000000000
0000000000000
0000000002000
0004000000000
0000000000500
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0070000000000
0077000002700
0074000007777
0000000000570
0000000000000
0000000000000
```

**Train 3 — input**

```text
000000000000
009700000000
077700000000
000000000000
000000000200
000000000000
000300000000
000000004000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000270
007000007770
007300077700
007700074000
000000000000
000000000000
```

**Train 4 — input**

```text
00000000000000
00070000000000
00970000000000
00770000000000
00070000000000
00000000000200
00000000000000
00000000000000
00005000000000
00000000003000
00000000000000
00000000000000
```

**Train 4 — output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000070
00000000000270
00000000000770
00077770000070
00005700000000
00000000073000
00000000777700
00000000000000
```

**Test — input**

```text
0000000000000
0070000000000
0097000000000
0077700000000
0000000000500
0000000000000
0000000000000
0002000004000
0000000000000
0000000000000
0000000000000
```

**Test — output**

```text
0000000000000
0000000000000
0000000000070
0000000000770
0000000007570
0000000000000
0007000777000
0002700074000
0007770007000
0000000000000
0000000000000
```

**Written solution**

Record the relative positions of the 7-cells around the 9. Each anchor color encodes a rotation: 2 none, 3 quarter-turn, 4 half-turn, 5 three-quarter-turn. Replay the rotated cloud around each anchor and keep the anchor colors.

**Reference program**

```python
def rule_m120(g):
    h,w=size(g)
    ref=find_color_positions(g,9)[0]
    offsets=[(r-ref[0], c-ref[1]) for r,row in enumerate(g) for c,v in enumerate(row) if v==7]
    anchors=[]
    transforms=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (2,3,4,5):
                anchors.append((r,c,v))
                transforms.append({2:0,3:1,4:2,5:3}[v])
    out=blank(h,w)
    for r,c,v in anchors:
        out[r][c]=v
    out=offset_scatter(out, offsets, anchors, transforms=transforms,
                       recolor=lambda aval,i,od,nd: 7, merge='overwrite')
    for r,c,v in anchors:
        out[r][c]=v
    return out
```

## M121 — Legend Motif Sequencing

**Difficulty:** medium

**Train pairs:** 4

**Skills:** legend order, component cropping, horizontal packing

**Suggested staged path:** The top row tells you only the order. Find the matching monochrome motifs below, crop each one tightly, and lay them out left to right in legend order.

**Train 1 — input**

```text
03050700000000
00000000000000
00000077000000
03030007700000
03330000000000
00300000050000
00000000055500
00000000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
30305000770
33305550077
03000000000
```

**Train 2 — input**

```text
060204000000000
000000000000000
000004400000000
000000400066600
000000440006000
000000000006000
002000000000000
002200000000000
000220000000000
000000000000000
000000000000000
```

**Train 2 — output**

```text
66602000440
06002200040
06000220044
```

**Train 3 — input**

```text
0903050000000
0000000000000
0000000033000
0000000003300
0900000000000
0999000000000
0000005050000
0000005550000
0000000500000
0000000000000
```

**Train 3 — output**

```text
90003300505
99900330555
00000000050
```

**Train 4 — input**

```text
04070200000000
00000000000000
00440000000000
00040000000000
00044000000000
00000000077700
00000200007000
00000220007000
00000022000000
00000000000000
00000000000000
```

**Train 4 — output**

```text
44007770200
04000700220
04400700022
```

**Test — input**

```text
050803000000000
000000000000000
000000000000000
005000000000000
005550000000000
000000000088000
000000333008000
000000030008800
000000030000000
000000000000000
000000000000000
```

**Test — output**

```text
50008800333
55500800030
00000880030
```

**Written solution**

Read the nonzero colors in the top row from left to right. For each such color, find the disconnected component of that color below, crop it to its bounding box, and concatenate the crops horizontally with a zero separator column.

**Reference program**

```python
def rule_m121(g):
    legend=[v for v in g[0] if v!=0]
    comps=components_color(g)
    blocks=[]
    for col in legend:
        matches=[comp['cells'] for comp in comps if comp['color']==col and bbox(comp['cells'])[0] > 0]
        cells=sorted(matches, key=lambda x:(-len(x), bbox(x)[0], bbox(x)[1]))[0]
        blocks.append(crop_bbox(g, cells))
    return concat_h(blocks, sep=1)
```

## M122 — Chamber Seed Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** region filling, walls and chambers, seed propagation

**Suggested staged path:** Treat 1 as walls and look for enclosed chambers. If a chamber contains one seed color, flood the empty cells of that chamber with that color.

**Train 1 — input**

```text
00000000000000
01111000000000
01001000111110
01201000100010
01001000105010
01111000100010
00000000100010
00000000111110
00000000000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
01111000000000
01221000111110
01221000155510
01221000155510
01111000155510
00000000155510
00000000111110
00000000000000
00000000000000
```

**Train 2 — input**

```text
000000000000000
001111100000000
001030100000000
001000100000000
001111100000000
000000000111110
011110000100010
016010000107010
010010000100010
011110000111110
000000000000000
```

**Train 2 — output**

```text
000000000000000
001111100000000
001333100000000
001333100000000
001111100000000
000000000111110
011110000177710
016610000177710
016610000177710
011110000111110
000000000000000
```

**Train 3 — input**

```text
0000000000000
0111100011110
0140100010010
0100100012010
0111100010010
0000000011110
0000011111000
0000010701000
0000011111000
0000000000000
```

**Train 3 — output**

```text
0000000000000
0111100011110
0144100012210
0144100012210
0111100012210
0000000011110
0000011111000
0000017771000
0000011111000
0000000000000
```

**Train 4 — input**

```text
0000000000000000
0000000000000000
0011110000000000
0010010001111100
0019010001000100
0010010001040100
0011110001000100
0111100001000100
0160100001111100
0100100000000000
0111100000000000
0000000000000000
```

**Train 4 — output**

```text
0000000000000000
0000000000000000
0011110000000000
0019910001111100
0019910001444100
0019910001444100
0011110001444100
0111100001444100
0166100001111100
0166100000000000
0111100000000000
0000000000000000
```

**Test — input**

```text
000000000000000
011111000000000
010001001111100
010501001000100
010001001020100
011111001000100
000111111111100
000107010000000
000100010000000
000111110000000
000000000000000
```

**Test — output**

```text
000000000000000
011111000000000
015551001111100
015551001222100
015551001222100
011111001222100
000111111111100
000177710000000
000177710000000
000111110000000
000000000000000
```

**Written solution**

Walls of 1 partition the grid into regions. For each non-wall region that contains exactly one nonzero seed color, fill its zero cells with that seed color while keeping the walls unchanged.

**Reference program**

```python
def rule_m122(g):
    h,w=size(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==1 or (r,c) in seen:
                continue
            q=[(r,c)]
            seen.add((r,c))
            region=[]
            colors=set()
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if g[rr][cc] > 1:
                    colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and g[nr][nc]!=1 and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            if len(colors)==1:
                col=next(iter(colors))
                for rr,cc in region:
                    if out[rr][cc]==0:
                        out[rr][cc]=col
    return out
```

## M123 — Area Winner Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** area comparison, relational output, matrix construction

**Suggested staged path:** Measure the areas of the three colored components first. Then convert those pairwise comparisons into a tiny 3x3 table.

**Train 1 — input**

```text
0000000000000
0202000000000
0222000060000
0020000066000
0000000006600
0040000000000
0044400000000
0000000000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
022
206
260
```

**Train 2 — input**

```text
000000000000
000000007700
033000007700
003000000000
003300000000
000000055500
000000005000
000000005000
000000000000
000000000000
```

**Train 2 — output**

```text
003
005
350
```

**Train 3 — input**

```text
000000000000
022000000000
002200000000
000000000000
000000060600
000000066600
000800006000
000888000000
000000000000
```

**Train 3 — output**

```text
060
606
060
```

**Train 4 — input**

```text
0000000000000
0000000000000
0040000000000
0044000000000
0004400000000
0000909000000
0000999055500
0000090050000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
049
409
990
```

**Test — input**

```text
0000000000000
0333000000000
0030000000000
0030000000000
0000000000000
0000000066000
0000000006000
0088000006600
0008000000000
0000000000000
```

**Test — output**

```text
003
006
360
```

**Written solution**

Order the component colors numerically. In the output matrix, entry (i,j) is the color of the larger of those two components, or 0 on the diagonal and for equal areas.

**Reference program**

```python
def rule_m123(g):
    comps=[]
    for comp in components_color(g):
        if comp['color'] != 0:
            comps.append((comp['color'], len(comp['cells'])))
    comps=sorted(comps)
    colors=[c for c,a in comps]
    areas={c:a for c,a in comps}
    out=blank(len(colors), len(colors))
    for i,ci in enumerate(colors):
        for j,cj in enumerate(colors):
            if i==j:
                out[i][j]=0
            elif areas[ci] > areas[cj]:
                out[i][j]=ci
            elif areas[cj] > areas[ci]:
                out[i][j]=cj
            else:
                out[i][j]=0
    return out
```

## M124 — Commanded Extraction

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command decoding, crop output, geometric transform

**Suggested staged path:** Ignore the absolute position of the lower motif. Read the single command in the top row, crop the motif, then apply the indicated transform.

**Train 1 — input**

```text
030000000000
000000000000
000000000000
000002000000
000002340000
000000400000
000000000000
000000000000
```

**Train 1 — output**

```text
022
430
040
```

**Train 2 — input**

```text
0500000000000
0000000000000
0000000000000
0000000000000
0000000050000
0000000556000
0000000060000
0000000000000
0000000000000
```

**Train 2 — output**

```text
050
655
060
```

**Train 3 — input**

```text
02000000000
00000000000
00000000000
00708000000
00788000000
00080000000
00000000000
00000000000
```

**Train 3 — output**

```text
708
788
080
```

**Train 4 — input**

```text
060000000000
000000000000
000000000000
000000000000
000000220000
000000034000
000000040000
000000000000
000000000000
```

**Train 4 — output**

```text
040
034
220
```

**Test — input**

```text
040000000000
000000000000
000000000000
000000000000
000005060000
000005600000
000000660000
000000000000
000000000000
```

**Test — output**

```text
660
065
605
```

**Written solution**

The lone nonzero cell in the top row encodes a transform: 2 identity, 3 rotate 90, 4 rotate 180, 5 horizontal flip, 6 vertical flip. Crop the motif below and output the transformed crop.

**Reference program**

```python
def rule_m124(g):
    cmd=[v for v in g[0] if v!=0][0]
    mapping={2:0,3:1,4:2,5:4,6:5}
    comps=sorted(components_nonzero(g[1:]), key=lambda x:bbox(x))
    # rebuild cell coords with +1 row offset
    cells=[(r+1,c) for r,c in comps[0]]
    motif=crop_bbox(g, cells)
    return apply_transform(motif, mapping[cmd])
```

## M125 — Nested Frame Depth Recolor

**Difficulty:** medium

**Train pairs:** 4

**Skills:** nesting depth, frame detection, palette remapping

**Suggested staged path:** All frames start as 8. Sort them from outermost to innermost and then recolor by depth.

**Train 1 — input**

```text
00000000000
08888888880
08000000080
08088888080
08080008080
08080808080
08080008080
08088888080
08000000080
08888888880
00000000000
```

**Train 1 — output**

```text
00000000000
02222222220
02000000020
02044444020
02040004020
02040604020
02040004020
02044444020
02000000020
02222222220
00000000000
```

**Train 2 — input**

```text
000000000000
088888888880
080000000080
080888888080
080800008080
080800008080
080800008080
080800008080
080888888080
080000000080
088888888880
000000000000
```

**Train 2 — output**

```text
000000000000
022222222220
020000000020
020444444020
020400004020
020400004020
020400004020
020400004020
020444444020
020000000020
022222222220
000000000000
```

**Train 3 — input**

```text
0000000000000
0888888888880
0800000000080
0808888888080
0808000008080
0808088808080
0808080808080
0808088808080
0808000008080
0808888888080
0800000000080
0888888888880
0000000000000
```

**Train 3 — output**

```text
0000000000000
0222222222220
0200000000020
0204444444020
0204000004020
0204066604020
0204060604020
0204066604020
0204000004020
0204444444020
0200000000020
0222222222220
0000000000000
```

**Train 4 — input**

```text
00000000000000
00888888888800
00800000000800
00808888880800
00808000080800
00808000080800
00808888880800
00800000000800
00888888888800
00000000000000
```

**Train 4 — output**

```text
00000000000000
00222222222200
00200000000200
00204444440200
00204000040200
00204000040200
00204444440200
00200000000200
00222222222200
00000000000000
```

**Test — input**

```text
0000000000000
0888888888880
0800000000080
0808888888080
0808000008080
0808088808080
0808088808080
0808088808080
0808000008080
0808888888080
0800000000080
0888888888880
0000000000000
```

**Test — output**

```text
0000000000000
0222222222220
0200000000020
0204444444020
0204000004020
0204066604020
0204066604020
0204066604020
0204000004020
0204444444020
0200000000020
0222222222220
0000000000000
```

**Written solution**

Each 8-colored component is a rectangular frame. Order the frames from outside to inside and recolor them using the fixed depth palette 2,4,6,7,... while leaving the background empty.

**Reference program**

```python
def rule_m125(g):
    frames=[comp['cells'] for comp in components_color(g) if comp['color']==8]
    frames=sorted(frames, key=lambda cells: (bbox(cells)[2]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[1]+1), reverse=True)
    out=blank(*size(g))
    for depth, cells in enumerate(frames):
        col=DEPTH_PALETTE[depth]
        for r,c in cells:
            out[r][c]=col
    return out
```

## M126 — Column Gravity with Obstacles

**Difficulty:** medium

**Train pairs:** 4

**Skills:** gravity, columnwise simulation, static blockers

**Suggested staged path:** Treat 1-cells as fixed blockers. Within each column segment between blockers, let the colored cells fall to the bottom while preserving their vertical order.

**Train 1 — input**

```text
00050000
02000030
04000060
00070000
00000010
00010000
00010000
00010000
00000000
11111111
```

**Train 1 — output**

```text
00000000
00000000
00000030
00050060
00070010
00010000
00010000
02010000
04000000
11111111
```

**Train 2 — input**

```text
000000000
002000090
000004000
003000000
000006000
000001020
001001000
001001000
000000000
000000000
111111111
```

**Train 2 — output**

```text
000000000
000000000
000000000
000004000
002006000
003001000
001001000
001001000
000000090
000000020
111111111
```

**Train 3 — input**

```text
070000000
000000200
050000300
000090100
010000100
010000000
010000000
000000000
000000000
111111111
```

**Train 3 — output**

```text
000000000
000000200
070000300
050000100
010000100
010000000
010000000
000000000
000090000
111111111
```

**Train 4 — input**

```text
00000009
20000000
00006000
40000000
00003000
10000000
10000005
00001000
00001000
00000000
00000000
11111111
```

**Train 4 — output**

```text
00000000
00000000
00000000
20000000
40000000
10006000
10003000
00001000
00001000
00000009
00000005
11111111
```

**Test — input**

```text
90000000
00200400
00000000
00700600
00000003
00000100
00100100
00100000
00000000
00000000
11111111
```

**Test — output**

```text
00000000
00000000
00000000
00000400
00200600
00700100
00100100
00100000
00000000
90000003
11111111
```

**Written solution**

Keep the 1-cells fixed. In every column and in every vertical segment separated by 1s, collect the colored cells and drop them to the lowest available positions of that segment, preserving their order.

**Reference program**

```python
def rule_m126(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                out[r][c]=1
    for c in range(w):
        start=h-1
        r=h-1
        while r>=0:
            if g[r][c]==1:
                start=r-1
                r-=1
                continue
            end=r
            while r>=0 and g[r][c]!=1:
                r-=1
            seg_top=r+1
            vals=[g[rr][c] for rr in range(seg_top, end+1) if g[rr][c] not in (0,1)]
            write=end
            for v in reversed(vals):
                out[write][c]=v
                write-=1
    return out
```

## H120 — Keyed Offset Merge

**Difficulty:** hard

**Train pairs:** 4

**Skills:** relative offsets, rotation commands, color remapping, overlap merge

**Suggested staged path:** Start like the medium offset task, but now each anchor color also changes the paint color. When two clouds overlap, the larger color wins.

**Train 1 — input**

```text
00000000000
09800000000
08800000000
00800000000
00000000000
00000000000
00000000000
00002030000
00000400000
00000000000
00000000000
```

**Train 1 — output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00006000000
00006630000
00006450000
00000400000
00000000000
```

**Train 2 — input**

```text
000000000000
008000000000
009800000000
008880000000
000000000000
000000000000
000000000000
000002050000
000000000000
000000300000
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
000000007000
000004077000
000002757000
000004440000
000005350000
000005500000
000005000000
```

**Train 3 — input**

```text
0000000000000
0000000000000
0980000000000
0880000000000
0080000000000
0000000000000
0000000040000
0000000002000
0000000050000
0000000000000
0000000000000
```

**Train 3 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000600000
0000000660000
0000000640000
0000000077700
0000000057400
0000000000400
0000000000000
```

**Train 4 — input**

```text
000000000000
000800000000
009800000000
008800000000
000800000000
000000000000
000000000000
000000000000
000030400000
000002000000
000000000000
000000000000
```

**Train 4 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000006000000
000006600000
000536400000
005552400000
000004400000
000000400000
```

**Test — input**

```text
000000000000
008000000000
009800000000
008800000000
000800000000
000000000000
000000000000
000002030000
000000000000
000000500000
000000000000
000000000000
```

**Test — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000004000000
000002535000
000005777000
000007570000
000000000000
000000000000
```

**Written solution**

Read the 8-cells as an offset cloud around the 9 origin. Anchor colors 2,3,4,5 encode rotations 0,90,180,270 and also paint colors 4,5,6,7. Replay each rotated cloud around its anchor and merge overlaps by taking the maximum color at each cell.

**Reference program**

```python
def rule_h120(g):
    h,w=size(g)
    ref=find_color_positions(g,9)[0]
    offsets=[(r-ref[0], c-ref[1]) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    anchors=[]
    transforms=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (2,3,4,5):
                anchors.append((r,c,v))
                transforms.append({2:0,3:1,4:2,5:3}[v])
    color_map={2:4,3:5,4:6,5:7}
    out=blank(h,w)
    for r,c,v in anchors:
        out[r][c]=v
    out=offset_scatter(out, offsets, anchors, transforms=transforms,
                       recolor=lambda aval,i,od,nd: color_map[aval], merge='max')
    for r,c,v in anchors:
        out[r][c]=max(out[r][c], v)
    return out
```

## H121 — Transform by Example

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, crop output

**Suggested staged path:** Use the upper pair to discover the transform first. Once you know that transform, ignore the example and apply it to the lower motif.

**Train 1 — input**

```text
000000000000000
020000000002200
023400000043000
004000000004000
000000000000000
000000000000000
000500000000000
005560000000000
000600000000000
000000000000000
000000000000000
```

**Train 1 — output**

```text
050
655
060
```

**Train 2 — input**

```text
0000000000000000
0220000000002200
0034000000043000
0040000000004000
0000000000000000
0000000000000000
0000000000000000
0070800000000000
0078800000000000
0008000000000000
0000000000000000
0000000000000000
```

**Train 2 — output**

```text
807
887
080
```

**Train 3 — input**

```text
000000000000000
040000000006000
045600000065400
006000000000400
000000000000000
000000000000000
005060000000000
005600000000000
000660000000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
660
065
605
```

**Train 4 — input**

```text
0000000000000000
0050000000006000
0556000000055600
0060000000005000
0000000000000000
0000000000000000
0000000000000000
0020000000000000
0023400000000000
0004000000000000
0000000000000000
0000000000000000
```

**Train 4 — output**

```text
040
234
200
```

**Test — input**

```text
000000000000000
070800000077000
078800000008800
008000000088000
000000000000000
000000000000000
002200000000000
000340000000000
000400000000000
000000000000000
000000000000000
```

**Test — output**

```text
200
234
040
```

**Written solution**

There are three disconnected motifs: A, transformed A, and B. Infer which dihedral transform maps A to its example partner, then apply the same transform to B and output the transformed crop.

**Reference program**

```python
def rule_h121(g):
    comps=sorted(components_nonzero(g), key=lambda cells: bbox(cells))
    a=crop_bbox(g, comps[0])
    ap=crop_bbox(g, comps[1])
    b=crop_bbox(g, comps[2])
    found=None
    for t in TRANSFORMS:
        if apply_transform(a, t) == ap:
            found=t
            break
    return apply_transform(b, found)
```

## H122 — Canonical Packing by Perimeter

**Difficulty:** hard

**Train pairs:** 4

**Skills:** perimeter computation, component cropping, canonical ordering

**Suggested staged path:** Separate the disconnected components, compute which one has the biggest boundary, then pack the crops from most boundary to least.

**Train 1 — input**

```text
0000000000000000
0101000000000000
0111000000000000
0010000000700000
0000000000770000
0000000000700000
0055500000000000
0050500000000000
0000000000000000
0000000000000000
0000000000000000
```

**Train 1 — output**

```text
1010555070
1110505077
0100000070
```

**Train 2 — input**

```text
000000000000000
000000000004400
001000000004400
001100000000000
000110000000000
000000000000000
000000000666000
000000000060000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 2 — output**

```text
1000666044
1100060044
0110000000
```

**Train 3 — input**

```text
000000000000000
011000000000000
001000000000000
001100000000000
000000000000000
000000002220000
000990002000000
000090000000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
1100222099
0100200009
0110000000
```

**Train 4 — input**

```text
0000000000000000
0011100000000000
0001000000000000
0001000000000000
0000000000000000
0000000000088800
0000000000080800
0000033000000000
0000030000000000
0000000000000000
0000000000000000
```

**Train 4 — output**

```text
1110888033
0100808030
0100000000
```

**Test — input**

```text
0000000000000000
0100000000000000
0111000000000000
0000000000000000
0000000000000000
0000000000777000
0000000000707000
0000440000000000
0000040000000000
0000000000000000
0000000000000000
```

**Test — output**

```text
7770100044
7070111004
```

**Written solution**

Find all connected components. Crop each one tightly, sort them by descending 4-neighbor perimeter (breaking ties by size), and concatenate the crops horizontally with a zero separator column.

**Reference program**

```python
def rule_h122(g):
    comps=components_nonzero(g)
    comps=sorted(comps, key=lambda cells:(-rect_perimeter(cells), -len(cells), bbox(cells)[0], bbox(cells)[1]))
    blocks=[crop_bbox(g, cells) for cells in comps]
    return concat_h(blocks, sep=1)
```

## H123 — Nearest-Seed Partition with Ties

**Difficulty:** hard

**Train pairs:** 4

**Skills:** distance reasoning, partitioning, tie handling

**Suggested staged path:** Treat the nonzero cells as seeds. For each empty cell, compare Manhattan distances to all seeds and mark ties separately.

**Train 1 — input**

```text
000000000
020000030
000000000
000000000
000000000
000000000
000000000
000040000
000000000
```

**Train 1 — output**

```text
222283333
222283333
222283333
222243333
222444333
224444433
444444444
444444444
444444444
```

**Train 2 — input**

```text
0000000000
0050000000
0000000000
0000000000
0000000020
0000000000
0000000000
0000000000
0007000000
0000000000
```

**Train 2 — output**

```text
5555555222
5555555222
5555552222
5555522222
5558222222
8887722222
7777772222
7777777222
7777777722
7777777722
```

**Train 3 — input**

```text
00000000000
03000000060
00000000000
00000000000
00000000000
00000000000
00000000000
00000200000
00000000000
```

**Train 3 — output**

```text
33333866666
33333866666
33333866666
33338286666
33382228666
33822222866
88222222288
22222222222
22222222222
```

**Train 4 — input**

```text
000000000000
000000000000
004000000700
000000000000
000000000000
000000000000
000000000000
000000000000
000005000000
000000000000
```

**Train 4 — output**

```text
444444777777
444444777777
444444777777
444444777777
444445877777
444455587777
444555558777
555555555888
555555555555
555555555555
```

**Test — input**

```text
00000000000
00200000500
00000000000
00000000000
00000000000
00000000000
00000000000
00000700000
00000000000
```

**Test — output**

```text
22222855555
22222855555
22222855555
22222755555
22227775555
22277777555
77777777777
77777777777
77777777777
```

**Written solution**

Every zero cell is colored by the nearest seed under Manhattan distance. If two or more seed colors are tied for the minimum distance, the cell becomes 8. Original seed cells stay unchanged.

**Reference program**

```python
def rule_h123(g):
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                continue
            dists=[]
            for sr,sc,col in seeds:
                d=abs(r-sr)+abs(c-sc)
                dists.append((d,col))
            m=min(d for d,col in dists)
            cols={col for d,col in dists if d==m}
            out[r][c]=next(iter(cols)) if len(cols)==1 else 8
    return out
```

## H124 — Composed Transform Strip

**Difficulty:** hard

**Train pairs:** 4

**Skills:** command composition, multiple transforms, crop output

**Suggested staged path:** Do not jump straight to the answer. First decode the command strip into a sequence of transforms, then apply them one after another to the lower motif.

**Train 1 — input**

```text
02050000000000
00000000000000
00000000000000
00000000000000
00000020000000
00000023400000
00000004000000
00000000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
220
034
040
```

**Train 2 — input**

```text
040602000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000050600000
000000056000000
000000006600000
000000000000000
000000000000000
000000000000000
```

**Train 2 — output**

```text
506
560
066
```

**Train 3 — input**

```text
03050000000000
00000000000000
00000000000000
00000000000000
00000708000000
00000788000000
00000080000000
00000000000000
00000000000000
00000000000000
```

**Train 3 — output**

```text
080
788
708
```

**Train 4 — input**

```text
060202000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000220000000
000000034000000
000000040000000
000000000000000
000000000000000
000000000000000
```

**Train 4 — output**

```text
022
430
040
```

**Test — input**

```text
05040200000000
00000000000000
00000000000000
00000000000000
00000005000000
00000055600000
00000006000000
00000000000000
00000000000000
00000000000000
```

**Test — output**

```text
050
556
060
```

**Written solution**

Read the nonzero command colors in the top row from left to right. Map 2,3,4,5,6 to rotate90, rotate180, rotate270, flip_h, flip_v, apply those transforms sequentially to the lower motif, and output the final crop.

**Reference program**

```python
def rule_h124(g):
    cmds=[v for v in g[0] if v!=0]
    mapping={2:1,3:2,4:3,5:4,6:5}
    comps=[cells for cells in components_nonzero(g) if bbox(cells)[0] > 0]
    motif=crop_bbox(g, sorted(comps, key=bbox)[0])
    out=motif
    for cmd in cmds:
        out=apply_transform(out, mapping[cmd])
    return out
```

## H125 — Size-Matched Frame Insertion

**Difficulty:** hard

**Train pairs:** 4

**Skills:** frame detection, size matching, placement by fit

**Suggested staged path:** Separate the empty 8-frames from the free shapes. Match each shape’s cropped size to one frame’s interior size and then insert it there.

**Train 1 — input**

```text
0000000000000000
0888880008888000
0800080008008000
0800080008008000
0800080008888000
0888880000000000
0000040000000000
0220044088888000
0022000080008666
0000000080008060
0000000088888000
0000000000000000
```

**Train 1 — output**

```text
0000000000000000
0888880008888000
0800080008008000
0800080008008000
0800080008888000
0888880000000000
0000040000000000
0220044088888000
0022000082208666
0000000080228060
0000000088888000
0000000000000000
```

**Train 2 — input**

```text
00000000000000000
00888880000333000
00800080000300000
00800080000007070
00888880000007770
00000000000000700
08888800000000000
08000800008888800
08000800008000800
08000855008000800
08888805008000800
00000000008888800
00000000000000000
```

**Train 2 — output**

```text
00000000000000000
00888880000333000
00833380000300000
00830080000007070
00888880000007770
00000000000000700
08888800000000000
08707800008888800
08777800008000800
08070855008000800
08888805008000800
00000000008888800
00000000000000000
```

**Train 3 — input**

```text
0000000000000000
0888800088888600
0800800080008660
0800800080008060
0888800080008000
0000000088888000
0000000000000444
0088888000000040
0080008000220000
0080008000200000
0080008000000000
0088888000000000
```

**Train 3 — output**

```text
0000000000000000
0888800088888600
0822800080008660
0820800080008060
0888800080008000
0000000088888000
0000000000000444
0088888000000040
0080008000220000
0080008000200000
0080008000000000
0088888000000000
```

**Train 4 — input**

```text
000000000000000000
088888800000007070
080000800088887700
080000800080080000
080000800080080000
088888800088880000
000000000000000000
055000000888880000
005500000800080000
000003300800080000
000003300800080000
000000000888880000
000000000000000000
```

**Train 4 — output**

```text
000000000000000000
088888800000007070
080000800088887700
080000800083380000
080000800083380000
088888800088880000
000000000000000000
055000000888880000
005500000800080000
000003300800080000
000003300800080000
000000000888880000
000000000000000000
```

**Test — input**

```text
0000000000000000
0888880008888000
0800080008008000
0800080008008000
0800080008888000
0888880000000000
0000040000000000
0222044088888000
0020000080008606
0000000080008660
0000000088888000
0000000000000000
```

**Test — output**

```text
0000000000000000
0888880008888000
0800080008008000
0800080008008000
0800080008888000
0888880000000000
0000040000000000
0222044088888000
0020000082228606
0000000080208660
0000000088888000
0000000000000000
```

**Written solution**

Find every hollow rectangular frame of 8s and compute its interior size. Crop the other components, match each crop to the frame whose interior has the same size, and place that crop into that frame’s interior.

**Reference program**

```python
def rule_h125(g):
    out=clone(g)
    frame_comps=[comp['cells'] for comp in components_color(g) if comp['color']==8]
    frames=[]
    for cells in frame_comps:
        r0,c0,r1,c1=bbox(cells)
        if len(cells) == 2*((r1-r0+1)+(c1-c0+1))-4:
            frames.append((r0,c0,r1,c1))
    shapes=[cells for cells in components_nonzero(g) if g[cells[0][0]][cells[0][1]] != 8]
    shape_info=[]
    for cells in shapes:
        block=crop_bbox(g,cells)
        bh,bw=size(block)
        shape_info.append((bh,bw,block))
    used=[False]*len(shape_info)
    for r0,c0,r1,c1 in sorted(frames):
        ih,iw=(r1-r0-1),(c1-c0-1)
        for i,(bh,bw,block) in enumerate(shape_info):
            if not used[i] and (bh,bw)==(ih,iw):
                for r in range(bh):
                    for c in range(bw):
                        if block[r][c]!=0:
                            out[r0+1+r][c0+1+c]=block[r][c]
                used[i]=True
                break
    return out
```

## H126 — Transform and Palette by Example

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, palette mapping

**Suggested staged path:** Use the upper pair twice: once to infer geometry and once to infer the color substitution. Then apply both to the lower motif.

**Train 1 — input**

```text
0000000000000000
0200000000005500
0234000000076000
0040000000007000
0000000000000000
0000000000000000
0022000000000000
0003400000000000
0004000000000000
0000000000000000
0000000000000000
```

**Train 1 — output**

```text
005
765
070
```

**Train 2 — input**

```text
00000000000000000
04000000000000200
04560000000093200
00600000000009000
00000000000000000
00000000000000000
00000000000000000
00506000000000000
00560000000000000
00066000000000000
00000000000000000
00000000000000000
```

**Train 2 — output**

```text
903
093
990
```

**Train 3 — input**

```text
0000000000000000
0050000000004000
0556000000047700
0060000000007000
0000000000000000
0000000000000000
0050600000000000
0056000000000000
0006600000000000
0000000000000000
0000000000000000
```

**Train 3 — output**

```text
440
047
407
```

**Train 4 — input**

```text
00000000000000000
07080000000006000
07880000000026600
00800000000020600
00000000000000000
00000000000000000
00000000000000000
00708000000000000
00088000000000000
00700000000000000
00000000000000000
00000000000000000
```

**Train 4 — output**

```text
2
```

**Test — input**

```text
0000000000000000
0220000000080000
0034000000085600
0040000000006000
0000000000000000
0000000000000000
0020000000000000
0023400000000000
0004000000000000
0000000000000000
0000000000000000
```

**Test — output**

```text
880
056
060
```

**Written solution**

The upper pair shows a geometric transform together with a color mapping. Infer both from A to A-prime, then apply that same transform and recoloring to the lower motif B and output the result.

**Reference program**

```python
def rule_h126(g):
    comps=sorted(components_nonzero(g), key=lambda cells: bbox(cells))
    a=crop_bbox(g, comps[0])
    ap=crop_bbox(g, comps[1])
    b=crop_bbox(g, comps[2])
    found_t=None
    mapping=None
    for t in TRANSFORMS:
        ta=apply_transform(a, t)
        if size(ta) != size(ap):
            continue
        ok=True
        m={}
        rev={}
        h,w=size(ta)
        for r in range(h):
            for c in range(w):
                va,vb=ta[r][c], ap[r][c]
                if (va==0) != (vb==0):
                    ok=False
                    break
                if va!=0:
                    if va in m and m[va]!=vb:
                        ok=False
                        break
                    if vb in rev and rev[vb]!=va:
                        ok=False
                        break
                    m[va]=vb
                    rev[vb]=va
            if not ok:
                break
        if ok:
            found_t=t
            mapping=m
            break
    tb=apply_transform(b, found_t)
    out=clone(tb)
    for r,row in enumerate(out):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=mapping[v]
    return out
```
