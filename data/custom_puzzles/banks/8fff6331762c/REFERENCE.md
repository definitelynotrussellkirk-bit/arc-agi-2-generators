# ARC Additional Puzzle Bank — 21 Puzzles (Set 10)

This tenth pack continues the numbering with **`E64–E70`**, **`M64–M70`**, and **`H64–H70`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
broadcast_motif(base_grid, motif_cells, src_anchor, dst_anchors, keep_anchors=True, recolor=None)
```

Intuition: describe a sparse motif once relative to a source anchor, then replay that exact offset pattern at one or more destination anchors. It is used directly in **E64**, **M64**, and **H64**.

Design goals for this set:

- easy: anchored copying, straight-line completion, 2×2 repair, rectangle filling, local filtering, selector crops, and guide reflection

- medium: selector-gated copying, per-row transforms, component abstraction, frame filling, rank-based recoloring, median-object normalization, and pairwise bbox reasoning

- hard: legend-conditioned copying, transform analogy, rotational equivalence, frame-local tiling, normalized boolean composition, transform-invariant candidate search, and hole-count ranking


## Easy (7)

### E64 — Broadcast Motif to Marker Anchors

**Difficulty:** easy

**Train pairs:** 4

**Skills:** anchored copying, offset transfer, sparse motif

**Suggested staged path:** Find the unique source anchor 5 first. Then express the motif as offsets and replay those offsets at every 6 marker.

**Train 1 — input**

```text
00000000
00200000
00530060
00040000
00000000
00000600
00000000
00000000
```

**Train 1 — output**

```text
00000000
00200020
00530063
00040004
00000200
00000630
00000040
00000000
```

**Train 2 — input**

```text
000000000
000000600
000000000
000700000
005040000
003000000
000000600
000000000
000000000
```

**Train 2 — output**

```text
000000070
000000604
000000300
000700000
005040000
003000070
000000604
000000300
000000000
```

**Train 3 — input**

```text
0000000000
0000000600
0008000000
0025000000
0000600000
0000000600
0000000000
```

**Train 3 — output**

```text
0000000800
0000002600
0008000000
0025800000
0002600800
0000002600
0000000000
```

**Train 4 — input**

```text
0000000000
0000000000
0000700060
0000040000
0000500000
0000200000
0000000000
0000000600
0000000000
```

**Train 4 — output**

```text
0000000070
0000000004
0000700060
0000040020
0000500000
0000200700
0000000040
0000000600
0000000200
```

**Test — input**

```text
000000000
000000000
009000600
005400000
070000000
000000000
006000600
000000000
000000000
```

**Test — output**

```text
000000000
000000900
009000640
005407000
070000000
009000900
006400640
070007000
000000000
```

**Written solution**

Locate the single source anchor colored 5. Collect every nonzero cell except the 5 and the destination 6 markers, convert them to offsets from the 5, and copy that sparse motif to every 6 anchor.

**Reference program**

```python
def rule_e64(g):
    src=find_unique(g,5)
    anchors=find_all(g,6)
    motif=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5,6)]
    return broadcast_motif(g, motif, src, anchors, keep_anchors=True)
```

### E65 — Complete Straight Segments

**Difficulty:** easy

**Train pairs:** 4

**Skills:** endpoint pairing, line completion, same-size transform

**Suggested staged path:** Group cells by color. Each color gives two endpoints on one row or one column.

**Train 1 — input**

```text
00000000
02000200
00000070
00000000
00000000
00000000
00000070
00000000
```

**Train 1 — output**

```text
00000000
02222200
00000070
00000070
00000070
00000070
00000070
00000000
```

**Train 2 — input**

```text
000000000
003000000
000000000
000000040
000000000
003000000
000000040
080000800
000000000
```

**Train 2 — output**

```text
000000000
003000000
003000000
003000040
003000040
003000040
000000040
088888800
000000000
```

**Train 3 — input**

```text
0000000000
0000000020
0600000600
0000000000
0000000000
0000000020
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000000020
0666666620
0000000020
0000000020
0000000020
0000000000
0000000000
```

**Train 4 — input**

```text
00000000
00000090
00000000
00707000
00000000
00000000
04000400
00000090
00000000
```

**Train 4 — output**

```text
00000000
00000090
00000090
00777090
00000090
00000090
04444490
00000090
00000000
```

**Test — input**

```text
0000000000
0200000200
0000000060
0000000000
0000000000
0000000000
0000000000
0004004000
0000000060
0000000000
```

**Test — output**

```text
0000000000
0222222200
0000000060
0000000060
0000000060
0000000060
0000000060
0004444060
0000000060
0000000000
```

**Written solution**

For each color, find its two endpoints. If they share a row, fill all cells between them horizontally; if they share a column, fill vertically.

**Reference program**

```python
def rule_e65(g):
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
        if r1==r2:
            a,b=sorted([c1,c2])
            for c in range(a,b+1):
                out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            for r in range(a,b+1):
                out[r][c1]=color
    return out
```

### E66 — Finish Monochrome 2×2 Blocks

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local completion, 2x2 reasoning, pattern repair

**Suggested staged path:** Look only at 2×2 windows. The intended pattern is three cells of one color and one missing corner.

**Train 1 — input**

```text
00000000
00200000
02200400
00000440
00007700
00007000
00000000
00000000
```

**Train 1 — output**

```text
00000000
02200000
02200440
00000440
00007700
00007700
00000000
00000000
```

**Train 2 — input**

```text
000000000
000330000
000030000
000000000
000000000
080000000
088000060
000000660
000000000
```

**Train 2 — output**

```text
000000000
000330000
000330000
000000000
000000000
088000000
088000660
000000660
000000000
```

**Train 3 — input**

```text
0000000000
0000000000
0055000990
0050000090
0000000000
0000400000
0000440000
0000000000
```

**Train 3 — output**

```text
0000000000
0000000000
0055000990
0055000990
0000000000
0000440000
0000440000
0000000000
```

**Train 4 — input**

```text
00000000
07000000
07700000
00000000
00000020
00000220
00880000
00080000
00000000
```

**Train 4 — output**

```text
00000000
07700000
07700000
00000000
00000220
00000220
00880000
00880000
00000000
```

**Test — input**

```text
0000000000
0000000400
0000004400
0000000000
0099000000
0090000000
0000000000
0000002000
0000002200
0000000000
```

**Test — output**

```text
0000000000
0000004400
0000004400
0000000000
0099000000
0099000000
0000000000
0000002200
0000002200
0000000000
```

**Written solution**

Whenever a 2×2 window contains exactly three cells of the same nonzero color and one empty cell, fill the missing corner with that color.

**Reference program**

```python
def rule_e66(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                idx=vals.index(0)
                if idx==0: out[r][c]=nz[0]
                elif idx==1: out[r][c+1]=nz[0]
                elif idx==2: out[r+1][c]=nz[0]
                else: out[r+1][c+1]=nz[0]
    return out
```

### E67 — Fill Rectangles from Diagonal Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bounding boxes, rectangle inference, fill

**Suggested staged path:** Two same-colored points define one rectangle. Use them as opposite corners.

**Train 1 — input**

```text
00000000
02000000
00000000
00020000
00000700
00000000
00000070
00000000
```

**Train 1 — output**

```text
00000000
02220000
02220000
02220000
00000770
00000770
00000770
00000000
```

**Train 2 — input**

```text
000000000
000030000
000000000
000000000
000000030
080000000
000000000
000800000
000000000
```

**Train 2 — output**

```text
000000000
000033330
000033330
000033330
000033330
088800000
088800000
088800000
000000000
```

**Train 3 — input**

```text
0000000000
0000000400
0600000000
0000000040
0000000000
0000600000
0000000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000000440
0666600440
0666600440
0666600000
0666600000
0000000000
0000000000
```

**Train 4 — input**

```text
00000000
07000000
00000700
00000000
00002000
00000000
00000000
00000020
00000000
```

**Train 4 — output**

```text
00000000
07777700
07777700
00000000
00002220
00002220
00002220
00002220
00000000
```

**Test — input**

```text
0000000000
0000003000
0000000000
0000000000
0000000030
0900000000
0000000000
0000000000
0009000000
0000000000
```

**Test — output**

```text
0000000000
0000003330
0000003330
0000003330
0000003330
0999000000
0999000000
0999000000
0999000000
0000000000
```

**Written solution**

For each color, take its two points as the diagonal corners of an axis-aligned rectangle and fill the full rectangle with that color.

**Reference program**

```python
def rule_e67(g):
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
        r0,r1=sorted([r1,r2]); c0,c1=sorted([c1,c2])
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out
```

### E68 — Remove Isolated Noise

**Difficulty:** easy

**Train pairs:** 4

**Skills:** neighbor checks, filtering, local support

**Suggested staged path:** A cell survives only if it is supported by a same-colored orthogonal neighbor.

**Train 1 — input**

```text
00000003
02000000
02000000
02200000
00007700
00000770
05000000
00000090
```

**Train 1 — output**

```text
00000000
02000000
02000000
02200000
00007700
00000770
00000000
00000000
```

**Train 2 — input**

```text
000000000
000000020
004440000
000400000
000400000
000000880
000000000
060000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
004440000
000400000
000400000
000000880
000000000
000000000
000000000
```

**Train 3 — input**

```text
0000000004
0333000000
0000000000
0000000000
0000077700
0000070000
0080070000
0000000000
```

**Train 3 — output**

```text
0000000000
0333000000
0000000000
0000000000
0000077700
0000070000
0000070000
0000000000
```

**Train 4 — input**

```text
00000000
00000090
06000000
06660000
00060000
00000220
00000200
00400000
00000000
```

**Train 4 — output**

```text
00000000
00000000
06000000
06660000
00060000
00000220
00000200
00000000
00000000
```

**Test — input**

```text
0000000020
0500000000
0550000000
0055000000
0000000000
0000007700
0000007700
0000007000
0900000000
0000000004
```

**Test — output**

```text
0000000000
0500000000
0550000000
0055000000
0000000000
0000007700
0000007700
0000007000
0000000000
0000000000
```

**Written solution**

Keep a nonzero cell if at least one of its four orthogonal neighbors has the same color. Delete isolated singletons.

**Reference program**

```python
def rule_e68(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==0:
                continue
            if any(g[nr][nc]==v for nr,nc in orth_neighbors(r,c,h,w)):
                out[r][c]=v
    return out
```

### E69 — Crop the Selector-Colored Object

**Difficulty:** easy

**Train pairs:** 4

**Skills:** selection, cropping, component detection

**Suggested staged path:** Read the target color from the top-left selector, then ignore every component of other colors.

**Train 1 — input**

```text
400000000
000000770
004000077
004000000
004400000
000000000
000002200
000002200
000000000
```

**Train 1 — output**

```text
40
40
44
```

**Train 2 — input**

```text
7000000000
0000000200
0333000200
0300000200
0300000000
0000007770
0000000700
0000000700
0000000000
0000000000
```

**Train 2 — output**

```text
777
070
070
```

**Train 3 — input**

```text
2000000000
0000000800
0022000800
0002200880
0000000000
0000006600
0000006600
0000006000
0000000000
```

**Train 3 — output**

```text
220
022
```

**Train 4 — input**

```text
800000000
022000000
000008000
000008880
000000080
000000000
044400000
040400000
044400000
000000000
```

**Train 4 — output**

```text
800
888
008
```

**Test — input**

```text
60000000000
00000000000
00606003300
00606000330
00666000000
00000000000
00000000000
00090000000
00090000000
00099000000
00000000000
```

**Test — output**

```text
606
606
666
```

**Written solution**

Use the top-left cell as the target color. Find the unique connected component of that color in the rest of the grid and return its tight crop.

**Reference program**

```python
def rule_e69(g):
    target=g[0][0]
    comps=components_nonzero(g, treat_colors_separately=True, exclude={(0,0)})
    choices=[cells for color,cells in comps if color==target]
    if not choices:
        return [[0]]
    # assume unique target component
    return crop_bbox(g, choices[0])
```

### E70 — Mirror Across the Full Guide Column

**Difficulty:** easy

**Train pairs:** 4

**Skills:** reflection, guide detection, symmetry

**Suggested staged path:** The full vertical line of 5s is the mirror axis. Only the left side needs to be copied.

**Train 1 — input**

```text
000050000
020050000
007050000
000050000
000050000
030050000
000050000
000050000
```

**Train 1 — output**

```text
000050000
020050020
007050700
000050000
000050000
030050030
000050000
000050000
```

**Train 2 — input**

```text
00000500000
00400500000
00000500000
08000500000
00000500000
00000500000
00002500000
00060500000
00000500000
```

**Train 2 — output**

```text
00000500000
00400500400
00000500000
08000500080
00000500000
00000500000
00002520000
00060506000
00000500000
```

**Train 3 — input**

```text
0000500000
0900500000
0003500000
0000500000
0000500000
0070500000
0000500000
0000500000
```

**Train 3 — output**

```text
0000500000
0900500900
0003530000
0000500000
0000500000
0070507000
0000500000
0000500000
```

**Train 4 — input**

```text
00000500000
00000500000
02000500000
00000500000
00080500000
00000500000
00000500000
00004500000
00600500000
00000500000
```

**Train 4 — output**

```text
00000500000
00000500000
02000500020
00000500000
00080508000
00000500000
00000500000
00004540000
00600500600
00000500000
```

**Test — input**

```text
00000500000
00700500000
00000500000
04000500000
00000500000
00000500000
00002500000
00000500000
00090500000
00000500000
```

**Test — output**

```text
00000500000
00700500700
00000500000
04000500040
00000500000
00000500000
00002520000
00000500000
00090509000
00000500000
```

**Written solution**

Find the column filled with 5s. Mirror every non-guide colored cell on the left side across that axis, keeping the original cells and the guide.

**Reference program**

```python
def rule_e70(g):
    h,w=size(g)
    guides=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    if not guides:
        return clone(g)
    gc=guides[0]
    out=clone(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0 and v!=5 and c<gc:
                mc=2*gc-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```


## Medium (7)

### M64 — Selector Broadcast of One Motif Color

**Difficulty:** medium

**Train pairs:** 4

**Skills:** selection, anchored copying, color filtering

**Suggested staged path:** First solve the easy broadcast idea, then add the selector: only one color from the source motif should be copied.

**Train 1 — input**

```text
200000000
000000000
000000060
002000000
005300000
000200000
000000000
000000600
000000000
```

**Train 1 — output**

```text
200000000
000000020
000000060
002000002
005300000
000200000
000000200
000000600
000000020
```

**Train 2 — input**

```text
7000000000
0000000000
0000000060
0000000000
0000700000
0005040000
0007200000
0000000000
0000000060
0000000000
```

**Train 2 — output**

```text
7000000000
0000000007
0000000060
0000000070
0000700000
0005040000
0007200000
0000000007
0000000060
0000000070
```

**Train 3 — input**

```text
4000000000
0000000000
0000000060
0000400000
0008500000
0000040000
0000000000
0000000060
0000000000
```

**Train 3 — output**

```text
4000000000
0000000040
0000000060
0000400004
0008500000
0000040000
0000000040
0000000060
0000000004
```

**Train 4 — input**

```text
300000000
000000000
000000060
003000000
000400000
005000000
003000000
000000000
000000060
000000000
```

**Train 4 — output**

```text
300000030
000000000
000000060
003000030
000400000
005000000
003000030
000000000
000000060
000000030
```

**Test — input**

```text
8000000000
0000000000
0000000060
0000000000
0008000000
0005400000
0080000000
0000000000
0006000060
0000000000
```

**Test — output**

```text
8000000000
0000000080
0000000060
0000000800
0008000000
0005400000
0080000000
0008000080
0006000060
0080000800
```

**Written solution**

Read the selector color from the top-left cell. Around the unique 5 anchor, keep only motif cells of that selected color and broadcast those offsets to every 6 anchor.

**Reference program**

```python
def rule_m64(g):
    target=g[0][0]
    src=find_unique(g,5)
    anchors=find_all(g,6)
    motif=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and (r,c)!=(0,0)]
    return broadcast_motif(g, motif, src, anchors, keep_anchors=True)
```

### M65 — Row-Wise Right Shifts from Header Codes

**Difficulty:** medium

**Train pairs:** 4

**Skills:** row transforms, header decoding, same-size transform

**Suggested staged path:** Treat each row independently. The first column is not data; it is the shift amount for that row.

**Train 1 — input**

```text
1200300
2044000
3700080
1006600
```

**Train 1 — output**

```text
1020030
2000440
3000700
1000660
```

**Train 2 — input**

```text
2055000
1300040
3002200
2600700
1080080
```

**Train 2 — output**

```text
2000550
1030004
3000002
2006007
1008008
```

**Train 3 — input**

```text
3900040
1022000
2506000
1070700
```

**Train 3 — output**

```text
3000900
1002200
2005060
1007070
```

**Train 4 — input**

```text
1440000
3002080
2600600
2077000
```

**Train 4 — output**

```text
1044000
3000002
2006006
2000770
```

**Test — input**

```text
2033000
1400050
3007008
2660000
```

**Test — output**

```text
2000330
1040005
3000007
2006600
```

**Written solution**

For each row, read the shift amount from the first column and move every other nonzero cell in that row to the right by that many columns.

**Reference program**

```python
def rule_m65(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        shift=g[r][0]
        out[r][0]=shift
        for c in range(1,w):
            v=g[r][c]
            if v!=0 and c+shift < w:
                out[r][c+shift]=v
    return out
```

### M66 — Convert Components to Area Bars

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component counting, dynamic output, abstraction

**Suggested staged path:** Do not preserve geometry. Reduce each object to one scalar: its area.

**Train 1 — input**

```text
0000000000
0200007700
0200000000
0220000000
0000000000
0000000000
0000444000
0000404000
0000444000
0000000000
```

**Train 1 — output**

```text
22220000
77000000
44444444
```

**Train 2 — input**

```text
00000000000
00000000000
00333000000
00030000000
00030000000
00000005000
08880005000
00000005000
00000005000
00000000000
00000000000
```

**Train 2 — output**

```text
33333
55550
88800
```

**Train 3 — input**

```text
000000000000
066600000000
060000002200
060000002200
000000000000
000000000000
000009900000
000000990000
000000000000
000000000000
```

**Train 3 — output**

```text
66666
22220
99990
```

**Train 4 — input**

```text
0000000000
0000000000
0070000000
0077700000
0000700000
0000000000
0000004440
0300004000
0300000000
0000000000
0000000000
```

**Train 4 — output**

```text
77777
44440
33000
```

**Test — input**

```text
000000000000
005050000000
005050000000
005550002220
000000000000
000000000000
000000000000
000077777000
000070707000
000077777000
000000000000
000000000000
```

**Test — output**

```text
5555555000000
2220000000000
7777777777777
```

**Written solution**

Find the connected components in top-left order. For each component, output one row containing a horizontal bar of that component’s color whose length equals the component area.

**Reference program**

```python
def rule_m66(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t: component_top_left(t[1]))
    if not comps:
        return [[0]]
    areas=[len(cells) for color,cells in comps]
    W=max(areas)
    out=blank(len(comps), W)
    for r,(color,cells) in enumerate(comps):
        for c in range(len(cells)):
            out[r][c]=color
    return out
```

### M67 — Fill Only the Selected Frames

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame detection, selection, interior fill

**Suggested staged path:** The selector chooses a border color, not a region position. Only matching hollow rectangles should be filled.

**Train 1 — input**

```text
2000000000
0000000000
0022227770
0020027070
0020027070
0022227070
0000007770
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
2000000000
0000000000
0022227770
0022227070
0022227070
0022227070
0000007770
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
80000000000
00000000000
00888880000
00800084444
00800084004
00800084004
00888884004
00000004004
00000004444
00000000000
00000000000
```

**Train 2 — output**

```text
80000000000
00000000000
00888880000
00888884444
00888884004
00888884004
00888884004
00000004004
00000004444
00000000000
00000000000
```

**Train 3 — input**

```text
400000000000
000000000000
004444006660
004004006060
004004006060
004004006060
004444006060
000000006660
000000000000
000000000000
```

**Train 3 — output**

```text
400000000000
000000000000
004444006660
004444006060
004444006060
004444006060
004444006060
000000006660
000000000000
000000000000
```

**Train 4 — input**

```text
700000000000
000000000000
007777700000
007000700000
007000700000
007000703333
007000703003
007777703003
000000003003
000000003333
000000000000
000000000000
```

**Train 4 — output**

```text
700000000000
000000000000
007777700000
007777700000
007777700000
007777703333
007777703003
007777703003
000000003003
000000003333
000000000000
000000000000
```

**Test — input**

```text
6000000000000
0000000000000
0066666000000
0060006044440
0060006040040
0060006040040
0060006040040
0066666040040
0666600040040
0600600044440
0666600000000
0000000000000
```

**Test — output**

```text
6000000000000
0000000000000
0066666000000
0060006044440
0060006040040
0060006040040
0060006040040
0066666040040
0666600040040
0600600044440
0666600000000
0000000000000
```

**Written solution**

Use the top-left selector color to choose which rectangular frame borders matter. Fill the interiors of all frames with that border color and leave other frames hollow.

**Reference program**

```python
def rule_m67(g):
    target=g[0][0]
    out=clone(g)
    comps=components_nonzero(g, treat_colors_separately=True, exclude={(0,0)})
    for color,cells in comps:
        if color==target and is_rect_border(cells):
            r0,c0,r1,c1=bbox(cells)
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=color
    return out
```

### M68 — Recolor Components by Area Rank

**Difficulty:** medium

**Train pairs:** 4

**Skills:** ranking, legend decoding, recoloring

**Suggested staged path:** The top row is the target palette in order. Sort the objects by size before painting them.

**Train 1 — input**

```text
234000000000
000000000000
080000880000
080000000000
088000000000
000000000000
000088800000
000008000000
000008000000
000000000000
```

**Train 1 — output**

```text
234000000000
000000000000
030000440000
030000000000
033000000000
000000000000
000022200000
000002000000
000002000000
000000000000
```

**Train 2 — input**

```text
752000000000
000000000000
008800008000
000880008000
000000008000
000000000000
000008880000
000008000000
000008000000
000000000000
000000000000
```

**Train 2 — output**

```text
752000000000
000000000000
005500002000
000550002000
000000002000
000000000000
000007770000
000007000000
000007000000
000000000000
000000000000
```

**Train 3 — input**

```text
46900000000
00000000000
08880000000
00000000000
00000088800
00000080800
00800088800
00800000000
00880000000
00000000000
```

**Train 3 — output**

```text
46900000000
00000000000
09990000000
00000000000
00000044400
00000040400
00600044400
00600000000
00660000000
00000000000
```

**Train 4 — input**

```text
3820000000000
0000000000000
0088800008800
0008000008800
0008000000000
0000000000000
0000000000000
0000080000000
0000088800000
0000000800000
0000000000000
```

**Train 4 — output**

```text
3820000000000
0000000000000
0033300002200
0003000002200
0003000000000
0000000000000
0000000000000
0000080000000
0000088800000
0000000800000
0000000000000
```

**Test — input**

```text
9470000000000
0000000000000
0888000000000
0800000088800
0800000000000
0000000000000
0000000000000
0000880000000
0000088000000
0000000000000
0000000000000
```

**Test — output**

```text
9470000000000
0000000000000
0999000000000
0900000077700
0900000000000
0000000000000
0000000000000
0000440000000
0000044000000
0000000000000
0000000000000
```

**Written solution**

Read the legend colors from the top row. Sort the components below by area descending, breaking ties by top-left position, and recolor the largest with the first legend color, the next with the second, and so on.

**Reference program**

```python
def rule_m68(g):
    legend=[v for v in g[0] if v!=0]
    h,w=size(g)
    body=[row[:] for row in g[1:]]
    comps=components_nonzero(body, treat_colors_separately=False)
    # adjust coords by +1 row
    comps=[(color,[(r+1,c) for r,c in cells]) for color,cells in comps]
    comps.sort(key=lambda t:(-len(t[1]), component_top_left(t[1])))
    out=blank(h,w)
    for c,v in enumerate(g[0]):
        out[0][c]=v
    for idx,(color,cells) in enumerate(comps):
        new_color=legend[idx]
        for r,c in cells:
            out[r][c]=new_color
    return out
```

### M69 — Crop the Median-Area Component

**Difficulty:** medium

**Train pairs:** 4

**Skills:** ranking, cropping, conditional rotation

**Suggested staged path:** Order the components by area, not by color. After cropping the middle one, normalize orientation if it is taller than wide.

**Train 1 — input**

```text
0000000000
0220004000
0000004000
0000004400
0000000000
0000000000
0000777000
0000707000
0000777000
0000000000
```

**Train 1 — output**

```text
444
400
```

**Train 2 — input**

```text
00000000000
00333000000
00000000000
00000000000
00000008880
00000008000
00000008000
05555500000
05050500000
05555500000
00000000000
```

**Train 2 — output**

```text
888
800
800
```

**Train 3 — input**

```text
000000000000
066000000000
006600002220
000000000200
000000000200
000000000000
000009900000
000009900000
000000000000
000000000000
```

**Train 3 — output**

```text
99
99
```

**Train 4 — input**

```text
000000000000
040000000000
040000000000
000000707000
000000707000
000000777000
000000000000
003330000000
003030000000
003330000000
000000000000
```

**Train 4 — output**

```text
707
707
777
```

**Test — input**

```text
000000000000
022200000000
000000000000
000000080000
000000088800
000000000800
000000000000
000555550000
000505050000
000555550000
000000000000
000000000000
```

**Test — output**

```text
800
888
008
```

**Written solution**

Find all components and sort them by area ascending. Take the median component, crop it to its bounding box, and rotate it clockwise once if the crop is taller than it is wide.

**Reference program**

```python
def rule_m69(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t:(len(t[1]), component_top_left(t[1])))
    color,cells=comps[len(comps)//2]
    crop=grid_from_component(g, cells)
    h,w=size(crop)
    if h>w:
        crop=rotate_cw(crop)
    return crop
```

### M70 — Bounding-Box Width Comparison Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** pairwise relations, bbox abstraction, dynamic output

**Suggested staged path:** Replace each object with just one measurement: bbox width. Then compare those widths pairwise.

**Train 1 — input**

```text
0000000000
0220000000
0000077700
0000000000
0000000000
0000000000
0044000000
0044000000
0000000000
0000000000
```

**Train 1 — output**

```text
131
212
131
```

**Train 2 — input**

```text
00000000000
03000000000
03000088800
03000080000
00000080000
00000000000
00000000000
00005555000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
133
213
221
```

**Train 3 — input**

```text
000000000000
006000000000
006000002220
006600000000
000000000000
000000000000
000009990000
000009090000
000009990000
000000000000
```

**Train 3 — output**

```text
133
211
211
```

**Train 4 — input**

```text
000000000000
044440000000
000000000000
000000000000
000000077000
000000000000
000000000000
003030000000
003030000000
003330000000
000000000000
```

**Train 4 — output**

```text
122
313
321
```

**Test — input**

```text
000000000000
022000000000
000000880000
000000088000
000000000000
000000000000
000000000000
000555500000
000000000000
000000000000
000000000000
000000000000
```

**Test — output**

```text
133
213
221
```

**Written solution**

Order the components by top-left position. Build an N×N matrix where 1 means equal bbox width, 2 means the row component is wider, and 3 means it is narrower.

**Reference program**

```python
def rule_m70(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t:component_top_left(t[1]))
    widths=[]
    for color,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        widths.append(c1-c0+1)
    n=len(widths)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if widths[i]==widths[j]:
                out[i][j]=1
            elif widths[i]>widths[j]:
                out[i][j]=2
            else:
                out[i][j]=3
    return out
```


## Hard (7)

### H64 — Legend-Recolored Broadcast Copies

**Difficulty:** hard

**Train pairs:** 4

**Skills:** anchored copying, ordering, legend recolor

**Suggested staged path:** Separate geometry from color. The source motif gives offsets, while the legend row gives the colors of the copies.

**Train 1 — input**

```text
2300000000
0000000000
0000000060
0000000000
0090000000
0059000000
0009000000
0000000000
0000000600
0000000000
```

**Train 1 — output**

```text
2300000000
0000000020
0000000062
0000000002
0090000000
0059000000
0009000000
0000000300
0000000630
0000000030
```

**Train 2 — input**

```text
74200000000
00000000000
00000000600
00000000000
00008000000
00050800000
00080000000
00000000000
00060000600
00000000000
00000000000
```

**Train 2 — output**

```text
74200000000
00000000070
00000000607
00000000700
00008000000
00050800000
00080000000
00004000020
00060400602
00040000200
00000000000
```

**Train 3 — input**

```text
94000000000
00000000000
00000000060
00007000000
00000700000
00005000000
00007000000
00000000000
00000000600
00000000000
```

**Train 3 — output**

```text
94000000090
00000000009
00000000060
00007000090
00000700000
00005000000
00007000400
00000000040
00000000600
00000000400
```

**Train 4 — input**

```text
3840000000
0000000000
0000000600
0000000000
0000000000
0070000000
0057000000
0700000000
0060000600
0000000000
0000000000
```

**Train 4 — output**

```text
3840000000
0000000300
0000000630
0000003000
0000000000
0070000000
0057000000
0780000400
0068000640
0800004000
0000000000
```

**Test — input**

```text
47200000000
00000000000
00000000600
00000000000
00090000000
00059000000
00009000000
00000000000
00060000600
00000000000
00000000000
```

**Test — output**

```text
47200000000
00000000400
00000000640
00000000040
00090000000
00059000000
00009000000
00070000200
00067000620
00007000020
00000000000
```

**Written solution**

Read the legend colors from the top row and sort the destination 6 anchors in reading order. Copy the sparse motif around the unique 5 anchor to each destination anchor, recoloring every copied cell with that anchor’s legend color.

**Reference program**

```python
def rule_h64(g):
    legend=[v for v in g[0] if v!=0]
    src=find_unique(g,5)
    anchors=sorted(find_all(g,6))
    motif=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5,6) and r!=0]  # ignore legend
    return broadcast_motif(g, motif, src, anchors, keep_anchors=True, recolor=legend)
```

### H65 — Infer a Whole-Panel Transform

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, panel decomposition, transform inference

**Suggested staged path:** The first two panels teach one global transform. Identify that transform before looking at panel three.

**Train 1 — input**

```text
00000500000500000
02000502220507700
02000502000500770
02200500000500000
00000500000500000
```

**Train 1 — output**

```text
00000
00070
00770
00700
00000
```

**Train 2 — input**

```text
00000050000005000000
03330050000005000000
03000050300005008000
03000050300005008000
00000050333005008800
00000050000005000000
```

**Train 2 — output**

```text
000000
008800
008000
008000
000000
000000
```

**Train 3 — input**

```text
00000500000500000
06600500660504440
00660506600500400
00000500000500400
00000500000500000
```

**Train 3 — output**

```text
00000
04440
00400
00400
00000
```

**Train 4 — input**

```text
00000050000005000000
02000050000005009900
02220050020005009900
00020050022205009000
00000050000205000000
00000050000005000000
```

**Train 4 — output**

```text
000000
000000
000900
009900
009900
000000
```

**Test — input**

```text
00000050000005000000
04400050004405077700
04400050004405070000
04000050000405070000
00000050000005000000
00000050000005000000
```

**Test — output**

```text
000000
007770
000070
000070
000000
000000
```

**Written solution**

Split the input into three panels using the separator columns. Determine which whole-panel transform maps panel A to panel B, then apply the same transform to panel C and return the transformed third panel.

**Reference program**

```python
def rule_h65(g):
    A,B,C=split_panels_horiz(g, sep_color=5)
    for code in (1,2,3,4,5):
        if apply_transform_square(A, code)==B:
            return apply_transform_square(C, code)
    return clone(C)
```

### H66 — Rotational Equivalence Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** shape normalization, rotation invariance, pairwise relations

**Suggested staged path:** Ignore colors and exact placement. Compare cropped shapes only up to quarter-turn rotation.

**Train 1 — input**

```text
00000000000
02000003330
02000003000
02200000000
00000000000
00000000000
00007770000
00000700000
00000700000
00000000000
00000000000
```

**Train 1 — output**

```text
123
213
331
```

**Train 2 — input**

```text
000000000000
044400000000
040000000080
040000000080
000000008880
000000000000
000000000000
000660000000
000066000000
000000000000
000000000000
000000000000
```

**Train 2 — output**

```text
123
213
331
```

**Train 3 — input**

```text
000000000000
005000000000
005500000020
000550000220
000000002200
000000000000
000000000000
000009090000
000009090000
000009990000
000000000000
```

**Train 3 — output**

```text
123
213
331
```

**Train 4 — input**

```text
00000000000
07700000000
07700003330
07000000330
00000000000
00000000000
00000000000
00000000000
00044400000
00040000000
00044400000
00000000000
```

**Train 4 — output**

```text
123
213
331
```

**Test — input**

```text
000000000000
020000000000
020000007700
022000000700
000000000700
000000000000
000000000000
000044400000
000040400000
000044400000
000000000000
000000000000
```

**Test — output**

```text
123
213
331
```

**Written solution**

Crop every connected component to its bounding box and convert it to a binary shape. Order components by top-left position and build an N×N matrix with 2 when two shapes are equal up to rotation, 1 on the diagonal, and 3 otherwise.

**Reference program**

```python
def rule_h66(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    comps.sort(key=lambda t:component_top_left(t[1]))
    crops=[binary_from_component(g,cells) for color,cells in comps]
    n=len(crops)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=1
            elif same_under_rot(crops[i], crops[j]):
                out[i][j]=2
            else:
                out[i][j]=3
    return out
```

### H67 — Frame-Local 2×2 Tiling

**Difficulty:** hard

**Train pairs:** 4

**Skills:** local templates, frame reasoning, periodic fill

**Suggested staged path:** Each frame has its own nearby sample, so do not reuse one sample globally.

**Train 1 — input**

```text
00000000000000
00230000070000
00420000007000
00000000000000
00888880088888
00800080080008
00800080080008
00800080080008
00800080080008
00888880088888
00000000000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
00230000070000
00420000007000
00000000000000
00888880088888
00842480080708
00800080080008
00842480080708
00800080080008
00888880088888
00000000000000
00000000000000
```

**Train 2 — input**

```text
000000000000000
000000000000000
004200000037000
002400000073000
000000000000000
008888800088888
008000800080008
008000800080008
008000800080008
008000800080008
008888800088888
000000000000000
000000000000000
```

**Train 2 — output**

```text
000000000000000
000000000000000
004200000037000
002400000073000
000000000000000
008888800088888
008242800087378
008000800080008
008242800087378
008000800080008
008888800088888
000000000000000
000000000000000
```

**Train 3 — input**

```text
000000000000000
000400000027000
000040000072000
000000000000000
000888880088888
000800080080008
000800080080008
000800080080008
000800080080008
000888880088888
000000000000000
000000000000000
```

**Train 3 — output**

```text
000000000000000
000400000027000
000040000072000
000000000000000
000888880088888
000804080087278
000800080080008
000804080087278
000800080080008
000888880088888
000000000000000
000000000000000
```

**Train 4 — input**

```text
00000000000000
00000000000000
00140000073000
00410000037000
00000000000000
00888880088888
00800080080008
00800080080008
00800080080008
00800080080008
00800080080008
00888880088888
00000000000000
```

**Train 4 — output**

```text
00000000000000
00000000000000
00140000073000
00410000037000
00000000000000
00888880088888
00841480083738
00800080080008
00841480083738
00800080080008
00841480083738
00888880088888
00000000000000
```

**Test — input**

```text
000000000000000
000000000000000
002400000073000
004200000037000
000000000000000
008888800088888
008000800080008
008000800080008
008000800080008
008000800080008
008000800080008
008888800088888
000000000000000
```

**Test — output**

```text
000000000000000
000000000000000
002400000073000
004200000037000
000000000000000
008888800088888
008424800083738
008000800080008
008424800083738
008000800080008
008424800083738
008888800088888
000000000000000
```

**Written solution**

For every 8-bordered frame, read the 2×2 sample block immediately above its left edge and tile that sample periodically across the frame interior.

**Reference program**

```python
def rule_h67(g):
    out=clone(g)
    comps=components_nonzero(g, treat_colors_separately=True)
    frames=[]
    for color,cells in comps:
        if color==8 and is_rect_border(cells):
            frames.append(bbox(cells))
    for r0,c0,r1,c1 in frames:
        sample=[g[r0-2][c0:c0+2], g[r0-1][c0:c0+2]]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=sample[(r-(r0+1))%2][(c-(c0+1))%2]
    return out
```

### H68 — Normalized XOR of Two Panels

**Difficulty:** hard

**Train pairs:** 4

**Skills:** normalization, boolean operations, panel abstraction

**Suggested staged path:** Crop the two objects before comparing them. The output is about occupancy, not original colors.

**Train 1 — input**

```text
0000005000000
0200005077000
0200005007700
0220005000000
0000005000000
0000005000000
```

**Train 1 — output**

```text
070
777
770
```

**Train 2 — input**

```text
0000005000000
0333005088800
0300005008000
0300005008000
0000005000000
0000005000000
```

**Train 2 — output**

```text
000
770
770
```

**Train 3 — input**

```text
00000500000
04400506000
04400506000
04000506600
00000500000
```

**Train 3 — output**

```text
07
07
07
```

**Train 4 — input**

```text
0000005000000
0900005020200
0990005020200
0099005022200
0000005000000
0000005000000
```

**Train 4 — output**

```text
007
077
700
```

**Test — input**

```text
0000005000000
0440005088800
0044005080000
0000005080000
0000005000000
0000005000000
```

**Test — output**

```text
007
777
700
```

**Written solution**

Split the input into two panels, crop the nonzero object in each panel, align the two cropped binary masks at the top-left of a common canvas, and output color 7 wherever exactly one mask is occupied.

**Reference program**

```python
def rule_h68(g):
    A,B=split_panels_horiz(g, sep_color=5)
    a=normalize_binary_crop(A); b=normalize_binary_crop(B)
    H=max(len(a), len(b)); W=max(len(a[0]), len(b[0]))
    a2=pad_to(a,H,W,0); b2=pad_to(b,H,W,0)
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            out[r][c]=7 if (a2[r][c]!=0) ^ (b2[r][c]!=0) else 0
    return out
```

### H69 — Find the Transform-Matching Candidate

**Difficulty:** hard

**Train pairs:** 4

**Skills:** template matching, transform invariance, panel search

**Suggested staged path:** Start from the template panel only. One candidate matches it after a rotation or flip; the others are distractors.

**Train 1 — input**

```text
00000500000500000500000
02000507700504440508880
02000500770504000500800
02200500000500000500800
00000500000500000500000
```

**Train 1 — output**

```text
00000
04440
04000
00000
00000
```

**Train 2 — input**

```text
000000500000050000005000000
033300506000050000005022000
030000506000050900005002200
030000506600050900005000000
000000500000050999005000000
000000500000050000005000000
```

**Train 2 — output**

```text
000000
000000
090000
090000
099900
000000
```

**Train 3 — input**

```text
00000500000500000500000
04400507070500880502000
04400507070500880502000
04000507770500080502200
00000500000500000500000
```

**Train 3 — output**

```text
00000
00880
00880
00080
00000
```

**Train 4 — input**

```text
000000500000050000005000000
020000506660050000005088800
022000500600050044005080000
002200500600050004405088800
000000500000050000405000000
000000500000050000005000000
```

**Train 4 — output**

```text
000000
000000
004400
000440
000040
000000
```

**Test — input**

```text
000000500000050000005000000
030000507070050000905022000
030000507070050000905002200
033000507770050009905000000
000000500000050000005000000
000000500000050000005000000
```

**Test — output**

```text
000000
000090
000090
000990
000000
000000
```

**Written solution**

Use the first panel as a template shape. Among the candidate panels, find the one whose cropped binary object matches the template up to rotation or reflection, and return that full candidate panel.

**Reference program**

```python
def rule_h69(g):
    panels=split_panels_horiz(g, sep_color=5)
    template=normalize_binary_crop(panels[0])
    for cand in panels[1:]:
        cc=normalize_binary_crop(cand)
        if same_under_transform(template, cc):
            return cand
    return panels[1]
```

### H70 — Pack Crops by Hole Count

**Difficulty:** hard

**Train pairs:** 4

**Skills:** hole counting, ranking, packing

**Suggested staged path:** Reduce each object to two summaries first: number of enclosed holes and area.

**Train 1 — input**

```text
00000000000000
02200077700000
02200070700000
00000077700000
00000000000000
00000000044444
00000000040404
00000000044444
00000000000000
00000000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
444440777022
404040707022
444440777000
```

**Train 2 — input**

```text
000000000000000
006060000000000
006060003330000
006660003030000
000000003330000
000000000000000
000000000000000
000099999000000
000090909000000
000099999000000
000000000000000
000000000000000
000000000000000
```

**Train 2 — output**

```text
9999903330606
9090903030606
9999903330666
```

**Train 3 — input**

```text
000000000000000
055500000000000
050000000888000
050000000808000
000000000888000
000000000000000
000000000000000
000022222000000
000020202000000
000022222000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
2222208880555
2020208080500
2222208880500
```

**Train 4 — input**

```text
00000000000000
00700000000000
00700000444000
00770000404000
00000000444000
00000000000000
00000000000000
00000000000000
00066666000000
00060606000000
00066666000000
00000000000000
00000000000000
```

**Train 4 — output**

```text
666660444070
606060404070
666660444077
```

**Test — input**

```text
000000000000000
033000000000000
033000007770000
000000007070000
000000007770000
000000000000000
000000000000000
000055555000000
000050505000000
000055555000000
000000000000000
000000000000000
000000000000000
```

**Test — output**

```text
555550777033
505050707033
555550777000
```

**Written solution**

Crop every component, count how many enclosed zero holes it has, sort components by hole count descending and then area descending, and pack the crops from left to right with one blank column between them.

**Reference program**

```python
def rule_h70(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    enriched=[]
    for color,cells in comps:
        crop=grid_from_component(g,cells)
        holes=holes_in_crop(crop)
        area=len(cells)
        enriched.append((holes,-area,color,crop))
    enriched.sort(key=lambda t:(-t[0], t[1], t[2]))
    crops=[crop for holes,neg_area,color,crop in enriched]
    return pack_horiz(crops, sep=1)
```
