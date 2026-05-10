# ARC Additional Puzzle Bank — 21 Puzzles (Set 11)

This eleventh pack continues the numbering with **`E71–E77`**, **`M71–M77`**, and **`H71–H77`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
link_terminals(base_grid, endpoints, color_mode="endpoint", allow_bends=False, bend_policy="row-first", overlap_color=None, include_endpoints=True)
```

Intuition: pair colored terminal cells and draw explicit straight or single-bend Manhattan paths between them. The primitive can also recolor overlaps, which makes it useful for both direct connection tasks and harder routing puzzles.

It is used directly in **E71**, **M71**, and **H71**.

Design goals for this set:

- easy: clean geometric completion, row packing, guide reflection, counting, enclosure fill, and motif stamping

- medium: commanded routing, guide-based extraction, patterned frame filling, relational matrices, rank selection, normalized overlays, and legend-driven packing

- hard: overlap-aware routing, analogy transfer, containment depth, symmetry relations, command composition, chamber ownership, and hole-based ranking

## Easy (7)

### E71 — Straight Terminal Links
**Difficulty:** easy
**Train pairs:** 4
**Skills:** path completion, endpoint pairing, same-size transform
**Suggested staged path:** Find the colored terminal pairs first. Then connect each same-colored pair with the shortest straight segment.

**Train 1 — input**
```text
0000000
0200020
0003000
0000000
0000000
0003000
0000000
```
**Train 1 — output**
```text
0000000
0222220
0003000
0003000
0003000
0003000
0000000
```

**Train 2 — input**
```text
00000000
00000040
00000000
00000000
05000500
00000000
00000040
00000000
```
**Train 2 — output**
```text
00000000
00000040
00000040
00000040
05555540
00000040
00000040
00000000
```

**Train 3 — input**
```text
000000000
000000000
002000000
000000000
000000000
000000000
000060060
002000000
000000000
```
**Train 3 — output**
```text
000000000
000000000
002000000
002000000
002000000
002000000
002066660
002000000
000000000
```

**Train 4 — input**
```text
000000000
030000030
000040000
000000000
000000000
050500000
000040000
000000000
```
**Train 4 — output**
```text
000000000
033333330
000040000
000040000
000040000
055540000
000040000
000000000
```

**Test — input**
```text
0000000000
0020000000
0000000000
0000040040
0000000000
0000000000
0000006000
0020000000
0000006000
```
**Test — output**
```text
0000000000
0020000000
0020000000
0020044440
0020000000
0020000000
0020006000
0020006000
0000006000
```
**Written solution**

Each nonzero color appears exactly twice as aligned terminals. Connect each color's two cells with a straight horizontal or vertical segment of that same color.

**Reference program**
```python
def rule_e71(g):
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return link_terminals(g, endpoints, allow_bends=False)
```

### E72 — Complete the Rectangle
**Difficulty:** easy
**Train pairs:** 4
**Skills:** bounding boxes, rectangle inference, border drawing
**Suggested staged path:** Ignore the missing corner. Use the extreme occupied rows and columns to infer the whole rectangle.

**Train 1 — input**
```text
00000000
02000200
00000000
00000000
00000000
02000000
00000000
00000000
```
**Train 1 — output**
```text
00000000
02222200
02000200
02000200
02000200
02222200
00000000
00000000
```

**Train 2 — input**
```text
000000000
000000000
003000000
000000000
000000000
000000000
003000300
000000000
000000000
```
**Train 2 — output**
```text
000000000
000000000
003333300
003000300
003000300
003000300
003333300
000000000
000000000
```

**Train 3 — input**
```text
0000000000
0000000400
0000000000
0000000000
0000000000
0040000400
0000000000
```
**Train 3 — output**
```text
0000000000
0044444400
0040000400
0040000400
0040000400
0044444400
0000000000
```

**Train 4 — input**
```text
0000000000
0000000000
0005000050
0000000000
0000000000
0000000000
0000000000
0000000050
0000000000
0000000000
```
**Train 4 — output**
```text
0000000000
0000000000
0005555550
0005000050
0005000050
0005000050
0005000050
0005555550
0000000000
0000000000
```

**Test — input**
```text
00000000000
00600000060
00000000000
00000000000
00000000000
00000000000
00600000000
00000000000
```
**Test — output**
```text
00000000000
00666666660
00600000060
00600000060
00600000060
00600000060
00666666660
00000000000
```
**Written solution**

For each color, take the bounding box of its given corner cells and draw the full border of that axis-aligned rectangle.

**Reference program**
```python
def rule_e72(g):
    h,w=size(g)
    out=blank(h,w)
    colors=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                colors[v].append((r,c))
    for col,cells in colors.items():
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=out[r][c1]=col
    return out
```

### E73 — Left-Pack Every Row
**Difficulty:** easy
**Train pairs:** 4
**Skills:** row-wise processing, order preservation, compression
**Suggested staged path:** Treat each row independently. Keep the nonzero colors in order and slide them left.

**Train 1 — input**
```text
0200030
0004005
5060000
0000000
```
**Train 1 — output**
```text
2300000
4500000
5600000
0000000
```

**Train 2 — input**
```text
10200304
00000000
05006070
70000008
00090000
```
**Train 2 — output**
```text
12340000
00000000
56700000
78000000
90000000
```

**Train 3 — input**
```text
000000
202033
004040
050600
000000
```
**Train 3 — output**
```text
000000
223300
440000
560000
000000
```

**Train 4 — input**
```text
900080700
000000000
102000030
004050060
```
**Train 4 — output**
```text
987000000
000000000
123000000
456000000
```

**Test — input**
```text
00302010
40000005
06070000
00000000
80009000
```
**Test — output**
```text
32100000
45000000
67000000
00000000
89000000
```
**Written solution**

For every row, remove the zeros, keep the remaining colors in their original order, and place them flush to the left with zeros filling the rest.

**Reference program**
```python
def rule_e73(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        out[r][:len(vals)] = vals
    return out
```

### E74 — Mirror Across the Guide Wall
**Difficulty:** easy
**Train pairs:** 4
**Skills:** reflection, guide detection, same-size transform
**Suggested staged path:** First identify the full vertical guide. Then reflect every colored cell on the left side to the same offset on the right.

**Train 1 — input**
```text
000090000
020090000
022090000
000090000
300090000
030090000
000090000
```
**Train 1 — output**
```text
000090000
020090020
022090220
000090000
300090003
030090030
000090000
```

**Train 2 — input**
```text
00000900000
00400900000
00400900000
00040900000
00000900000
06000900000
06600900000
00000900000
```
**Train 2 — output**
```text
00000900000
00400900400
00400900400
00040904000
00000900000
06000900060
06600900660
00000900000
```

**Train 3 — input**
```text
000090000
505090000
050090000
000090000
007090000
000090000
```
**Train 3 — output**
```text
000090000
505090505
050090050
000090000
007090700
000090000
```

**Train 4 — input**
```text
0000009000000
0000009000000
0200009000000
0220009000000
0020009000000
0000009000000
8000009000000
0880009000000
0000009000000
```
**Train 4 — output**
```text
0000009000000
0000009000000
0200009000020
0220009000220
0020009000200
0000009000000
8000009000008
0880009000880
0000009000000
```

**Test — input**
```text
00000900000
03000900000
00300900000
03000900000
00000900000
00400900000
04000900000
00000900000
```
**Test — output**
```text
00000900000
03000900030
00300900300
03000900030
00000900000
00400900400
04000900040
00000900000
```
**Written solution**

The column filled with 9s is a mirror guide. Keep the original motif and copy each nonzero non-guide cell to its mirror position across that guide.

**Reference program**
```python
def rule_e74(g):
    h,w=size(g)
    out=clone(g)
    # full vertical 9 column
    guide_cols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    gc = guide_cols[0]
    for r in range(h):
        for c in range(gc):
            v=g[r][c]
            if v!=0 and v!=9:
                mc = 2*gc - c
                if 0<=mc<w:
                    out[r][mc] = v
    return out
```

### E75 — Count to a Bar
**Difficulty:** easy
**Train pairs:** 4
**Skills:** counting, dynamic-size output, color preservation
**Suggested staged path:** Only one color matters. Count how many times it appears, then output a bar of that many cells.

**Train 1 — input**
```text
020000
000200
002000
000000
000000
```
**Train 1 — output**
```text
222
```

**Train 2 — input**
```text
4000000
0000040
0400000
0000000
0000004
0004000
```
**Train 2 — output**
```text
44444
```

**Train 3 — input**
```text
00700700
07000000
00000070
00000000
```
**Train 3 — output**
```text
7777
```

**Train 4 — input**
```text
0000000
0300030
0000000
0003000
0000000
0300030
0003000
```
**Train 4 — output**
```text
333333
```

**Test — input**
```text
000060000
060000000
000000060
000600000
000006000
000000000
```
**Test — output**
```text
66666
```
**Written solution**

Count all nonzero marker cells and output a single row whose length equals that count, filled with the marker color.

**Reference program**
```python
def rule_e75(g):
    vals=[v for row in g for v in row if v!=0]
    col=vals[0]
    return [[col]*len(vals)]
```

### E76 — Fill the Enclosed Hole
**Difficulty:** easy
**Train pairs:** 4
**Skills:** enclosure, hole fill, region detection
**Suggested staged path:** Separate boundary-connected zeros from enclosed zeros. Only the interior zero region changes.

**Train 1 — input**
```text
00000000
02222220
02000020
02000020
02000020
02222220
00000000
```
**Train 1 — output**
```text
00000000
02222220
02222220
02222220
02222220
02222220
00000000
```

**Train 2 — input**
```text
000000000
000000000
004444440
004000040
004000040
004000040
004444440
000000000
```
**Train 2 — output**
```text
000000000
000000000
004444440
004444440
004444440
004444440
004444440
000000000
```

**Train 3 — input**
```text
0000000000
0005555550
0005000050
0005000050
0005555550
0000000000
```
**Train 3 — output**
```text
0000000000
0005555550
0005555550
0005555550
0005555550
0000000000
```

**Train 4 — input**
```text
000000000
033333330
030000030
030000030
030000030
030000030
030000030
033333330
000000000
```
**Train 4 — output**
```text
000000000
033333330
033333330
033333330
033333330
033333330
033333330
033333330
000000000
```

**Test — input**
```text
0000000000
0000000000
0666666660
0600000060
0600000060
0600000060
0666666660
0000000000
```
**Test — output**
```text
0000000000
0000000000
0666666660
0666666660
0666666660
0666666660
0666666660
0000000000
```
**Written solution**

Find zero regions that do not touch the outside border. If such a region is enclosed by a single surrounding color, fill the whole interior with that color.

**Reference program**
```python
def rule_e76(g):
    h,w=size(g)
    out=clone(g)
    vis=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 or vis[r][c]:
                continue
            vis[r][c]=True
            q=[(r,c)]
            region=[]
            border=False
            neigh=set()
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if rr==0 or cc==0 or rr==h-1 or cc==w-1:
                    border=True
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w:
                        if g[nr][nc]==0 and not vis[nr][nc]:
                            vis[nr][nc]=True; q.append((nr,nc))
                        elif g[nr][nc]!=0:
                            neigh.add(g[nr][nc])
            if not border and len(neigh)==1:
                col=next(iter(neigh))
                for rr,cc in region:
                    out[rr][cc]=col
    return out
```

### E77 — Stamp the Corner Motif
**Difficulty:** easy
**Train pairs:** 4
**Skills:** motif copying, marker interpretation, same-size transform
**Suggested staged path:** Read the 2×2 motif from the upper-left corner first. Then stamp that exact motif at every marker cell.

**Train 1 — input**
```text
20000000
34000000
00000000
00009000
00000000
09000000
00000000
```
**Train 1 — output**
```text
20000000
34000000
00000000
00002000
00003400
02000000
03400000
```

**Train 2 — input**
```text
500000000
060000000
000009000
000000000
000000000
000090000
090000000
000000000
```
**Train 2 — output**
```text
500000000
060000000
000005000
000000600
000000000
000050000
050006000
006000000
```

**Train 3 — input**
```text
2700000000
7000000000
0000000000
0090000000
0000009000
0000000000
0000000000
```
**Train 3 — output**
```text
2700000000
7000000000
0000000000
0027000000
0070002700
0000007000
0000000000
```

**Train 4 — input**
```text
800000000
180000000
000900000
000000000
000000000
000009000
009000000
000000000
000000000
```
**Train 4 — output**
```text
800000000
180000000
000800000
000180000
000000000
000008000
008001800
001800000
000000000
```

**Test — input**
```text
2400000000
4000000000
0000000000
0000090000
0000000000
0900000000
0000000900
0000000000
```
**Test — output**
```text
2400000000
4000000000
0000000000
0000024000
0000040000
0240000000
0400000240
0000000400
```
**Written solution**

Take the top-left 2×2 block as the source motif. Remove the 9 markers and paste the motif with each marker acting as the motif's top-left anchor.

**Reference program**
```python
def rule_e77(g):
    h,w=size(g)
    out=clone(g)
    motif=[row[:2] for row in g[:2]]
    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    for r,c in markers:
        out[r][c]=0
    for r,c in markers:
        for dr in range(2):
            for dc in range(2):
                v=motif[dr][dc]
                if v!=0:
                    out[r+dr][c+dc]=v
    return out
```

## Medium (7)

### M71 — Commanded L-Links
**Difficulty:** medium
**Train pairs:** 4
**Skills:** path routing, command decoding, paired terminals
**Suggested staged path:** Read the command cell before tracing any paths. Then connect each color pair with a single-bend Manhattan route that obeys that command.

**Train 1 — input**
```text
10000000
00000300
04000000
00000000
00000000
00300000
00004000
00000000
```
**Train 1 — output**
```text
10000000
00333300
04444000
00304000
00304000
00304000
00004000
00000000
```

**Train 2 — input**
```text
200000000
000000500
000000000
060000000
000000000
000000000
000500000
000006000
000000000
```
**Train 2 — output**
```text
200000000
000000500
000000500
060000500
060000500
060000500
060555500
066666000
000000000
```

**Train 3 — input**
```text
1000000000
0000000000
0000000300
0000000000
0070000000
0000000000
0000000000
0000300000
0000000070
0000000000
```
**Train 3 — output**
```text
1000000000
0000000000
0000333300
0000300000
0077777770
0000300070
0000300070
0000300070
0000000070
0000000000
```

**Train 4 — input**
```text
2000000000
0000000040
0050000000
0000000000
0000000000
0004000000
0000000500
0000000000
```
**Train 4 — output**
```text
2000000000
0000000040
0050000040
0050000040
0050000040
0054444440
0055555500
0000000000
```

**Test — input**
```text
1000000000
0000000300
0000000000
0600000000
0000000000
0000000000
0030000000
0000006000
0000000000
```
**Test — output**
```text
1000000000
0033333300
0030000000
0666666000
0030006000
0030006000
0030006000
0000006000
0000000000
```
**Written solution**

The top-left command chooses row-first or column-first routing. Connect each same-colored terminal pair with an L-shaped Manhattan path using that bend policy.

**Reference program**
```python
def rule_m71(g):
    cmd=g[0][0]
    bend='row-first' if cmd==1 else 'col-first'
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend)
```

### M72 — Guide-Color Crop
**Difficulty:** medium
**Train pairs:** 4
**Skills:** object selection, color matching, cropping
**Suggested staged path:** The guide color is in the top row. Ignore the other objects and crop only the component whose color matches that guide.

**Train 1 — input**
```text
3000000000
0000000000
0220033300
0200030300
0000000000
0044000000
0004400000
0000000000
```
**Train 1 — output**
```text
333
303
```

**Train 2 — input**
```text
500000000000
000000000000
005550000000
000500000000
000000033000
000000033000
066600000000
060000000000
000000000000
```
**Train 2 — output**
```text
555
050
```

**Train 3 — input**
```text
40000000000
00000000000
00200000000
02220000000
00200000000
00000044000
00000044000
00770040000
00700000000
00000000000
```
**Train 3 — output**
```text
44
44
40
```

**Train 4 — input**
```text
6000000000000
0000000000000
0033300000000
0000300066600
0000000060600
0000550066600
0000550000000
0000000000000
```
**Train 4 — output**
```text
666
606
666
```

**Test — input**
```text
200000000000
000000000000
004440000000
000400020000
000000022000
000666002200
000606000000
000000000000
000000000000
```
**Test — output**
```text
200
220
022
```
**Written solution**

Read the nonzero guide color from the top row, find the object of that color in the main grid, and output its tight bounding-box crop.

**Reference program**
```python
def rule_m72(g):
    guide=[v for v in g[0] if v!=0][0]
    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v==guide]
    return crop_bbox(g, cells)
```

### M73 — Checkerboard Frame Fill
**Difficulty:** medium
**Train pairs:** 4
**Skills:** frame detection, interior filling, parity patterns
**Suggested staged path:** First detect each rectangular frame. Then fill only its interior, using an alternating checkerboard aligned to the interior corner.

**Train 1 — input**
```text
0000000000
0222220000
0200020000
0200020000
0200020000
0222220000
0000000000
0000000000
```
**Train 1 — output**
```text
0000000000
0222220000
0220220000
0202020000
0220220000
0222220000
0000000000
0000000000
```

**Train 2 — input**
```text
000000000000
033330000000
030030055550
030030050050
030030050050
030030050050
033330050050
000000055550
000000000000
```
**Train 2 — output**
```text
000000000000
033330000000
033030055550
030330055050
033030050550
030330055050
033330050550
000000055550
000000000000
```

**Train 3 — input**
```text
0000000000
0000000000
0044444400
0040000400
0040000400
0040000400
0040000400
0044444400
0000000000
0000000000
```
**Train 3 — output**
```text
0000000000
0000000000
0044444400
0044040400
0040404400
0044040400
0040404400
0044444400
0000000000
0000000000
```

**Train 4 — input**
```text
0000000000000
0666660022220
0600060020020
0600060020020
0600060020020
0666660020020
0000000022220
0000000000000
```
**Train 4 — output**
```text
0000000000000
0666660022220
0660660022020
0606060020220
0660660022020
0666660020220
0000000022220
0000000000000
```

**Test — input**
```text
00000000000
00555555500
00500000500
00500000500
00500000500
00500000500
00555555500
00000000000
00000000000
```
**Test — output**
```text
00000000000
00555555500
00550505500
00505050500
00550505500
00505050500
00555555500
00000000000
00000000000
```
**Written solution**

For each rectangular border, keep the frame itself and fill its interior with a checkerboard of frame color and zero, starting with the frame color at the interior's top-left cell.

**Reference program**
```python
def rule_m73(g):
    h,w=size(g)
    out=blank(h,w)
    comps=components_nonzero(g, treat_colors_separately=True)
    for col,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=out[r][c1]=col
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=col if ((r-(r0+1)) + (c-(c0+1)))%2==0 else 0
    return out
```

### M74 — Area Equality Matrix
**Difficulty:** medium
**Train pairs:** 4
**Skills:** component measurement, reading-order sorting, relation matrices
**Suggested staged path:** Extract the three objects and measure their areas. The output is a matrix comparing those areas pairwise.

**Train 1 — input**
```text
000000000000
022000330000
020000033000
000000000000
000000000000
000000004400
000000004400
000000000000
```
**Train 1 — output**
```text
800
088
088
```

**Train 2 — input**
```text
0000000000000
0000000000000
0222005550000
0020005000000
0000000000000
0000000007700
0000000007700
0000000007000
0000000000000
```
**Train 2 — output**
```text
880
880
008
```

**Train 3 — input**
```text
000000000000
033000000000
033000000000
000000000000
000000444000
000000404000
000000000000
006600000000
006000000000
000000000000
```
**Train 3 — output**
```text
800
080
008
```

**Train 4 — input**
```text
00000000000000
02220000006660
00020000006000
00000000000000
00000005550000
00000000500000
00000000000000
00000000000000
```
**Train 4 — output**
```text
888
888
888
```

**Test — input**
```text
000000000000
002000044400
022200040400
002000044400
000000000000
000000000000
000660000000
000660000000
000600000000
```
**Test — output**
```text
808
080
808
```
**Written solution**

Sort the objects by reading order. Output a 3×3 matrix with 8 when two objects have the same number of cells and 0 otherwise.

**Reference program**
```python
def rule_m74(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    n=len(comps)
    areas=[len(cells) for col,cells in comps]
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if areas[i]==areas[j] else 0
    return out
```

### M75 — Rank-by-Area Extract
**Difficulty:** medium
**Train pairs:** 4
**Skills:** ranking, component areas, dynamic selection
**Suggested staged path:** The number of top-row markers tells you which ranked object to choose. Rank the objects by area, then crop the selected one.

**Train 1 — input**
```text
9000000000000
0000000000000
0220003300000
0200003300000
0000000000000
0000000000400
0000000004440
0000000000400
0000000000000
```
**Train 1 — output**
```text
22
20
```

**Train 2 — input**
```text
99000000000000
00000000000000
00222000000000
00200000066600
00000000060600
05500000066600
05500000000000
05000000000000
00000000000000
00000000000000
```
**Train 2 — output**
```text
55
55
50
```

**Train 3 — input**
```text
9990000000000
0000000000000
0333000400000
0030004440000
0000000400000
0000000077770
0000000070070
0000000077770
0000000000000
```
**Train 3 — output**
```text
7777
7007
7777
```

**Train 4 — input**
```text
990000000000000
000000000000000
000000000000000
002200005550000
002200005050000
066666000000000
060606000000000
060606000000000
060606000000000
066666000000000
000000000000000
```
**Train 4 — output**
```text
555
505
```

**Test — input**
```text
99900000000000
00000000000000
02200044000000
02000044000000
00000000666660
00000000606060
00000000606060
00000000606060
00000000666660
00000000000000
```
**Test — output**
```text
66666
60606
60606
60606
66666
```
**Written solution**

Count the 9 markers in the top row to get rank k. Sort the objects below by area from smallest to largest and output the tight crop of the kth object.

**Reference program**
```python
def rule_m75(g):
    k=sum(1 for v in g[0] if v==9)
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, ignore_positions={(0,c) for c in range(len(g[0]))}, ignore_colors={9}))
    comps=sorted(comps, key=lambda comp: (len(comp[1]),) + component_key(comp))
    sel=comps[k-1]
    return crop_bbox(g, sel[1])
```

### M76 — Normalized Shape XOR
**Difficulty:** medium
**Train pairs:** 4
**Skills:** normalization, shape comparison, binary overlays
**Suggested staged path:** Ignore the colors after locating the two objects. Normalize each object to its own crop, then compare occupancy cell by cell.

**Train 1 — input**
```text
000000000000
022200003330
020000000300
000000000000
000000000000
000000000000
000000000000
```
**Train 1 — output**
```text
000
880
```

**Train 2 — input**
```text
0000000000000
0000000000000
0022000000000
0022000003300
0000000000330
0000000000000
0000000000000
0000000000000
```
**Train 2 — output**
```text
000
808
```

**Train 3 — input**
```text
00000000000000
00000000000000
00200000000000
02220000003330
00200000003030
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 3 — output**
```text
808
080
080
```

**Train 4 — input**
```text
000000000000
022000003330
022000003030
020000003330
000000000000
000000000000
000000000000
000000000000
```
**Train 4 — output**
```text
008
088
088
```

**Test — input**
```text
0000000000000
0000000000000
0200000000000
0220000000000
0022000003330
0000000003000
0000000000000
0000000000000
0000000000000
```
**Test — output**
```text
088
080
088
```
**Written solution**

Crop the two objects to their own bounding boxes, align both crops to the top-left of a shared canvas, and output 8 exactly where one occupancy mask is on and the other is off.

**Reference program**
```python
def rule_m76(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    # pick first two non-divider colors with largest components? We'll design only 2
    crops=[crop_bbox(g,cells) for col,cells in comps[:2]]
    h=max(len(crops[0]), len(crops[1]))
    w=max(len(crops[0][0]), len(crops[1][0]))
    a=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[0]], h,w)
    b=pad_to([[1 if v!=0 else 0 for v in row] for row in crops[1]], h,w)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=8 if a[r][c] != b[r][c] else 0
    return out
```

### M77 — Legend-Ordered Assembly
**Difficulty:** medium
**Train pairs:** 4
**Skills:** legend decoding, component extraction, packing
**Suggested staged path:** Read the top-row legend left to right. Then find those colored objects and pack their crops in that same order.

**Train 1 — input**
```text
32500000000000
00000000000000
00000033000000
02200033000000
02000000000000
00000000005550
00000000000500
00000000000000
00000000000000
```
**Train 1 — output**
```text
330220555
330200050
```

**Train 2 — input**
```text
640000000000000
000000000000000
000000000000000
004400000000000
004400000666000
004000000606000
000000000666000
000000000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
666044
606044
666040
```

**Train 3 — input**
```text
5270000000000000
0000000000000000
0555000000000000
0505022200000000
0000020000007700
0000000000000770
0000000000000000
0000000000000000
0000000000000000
```
**Train 3 — output**
```text
55502220770
50502000077
```

**Train 4 — input**
```text
46300000000000000
00000000000000000
00000000000000000
00040000000000000
00444000000000000
00040000600000000
00000000660000000
00000000066003300
00000000000003300
00000000000000000
00000000000000000
```
**Train 4 — output**
```text
0400600033
4440660033
0400066000
```

**Test — input**
```text
752000000000000
000000000000000
000000000007770
000000055507070
000000050007770
022000000000000
022000000000000
000000000000000
000000000000000
000000000000000
```
**Test — output**
```text
7770555022
7070500022
7770000000
```
**Written solution**

Treat the nonzero top row as an ordering legend. Crop the matching objects and concatenate them left to right in legend order with one blank separator column.

**Reference program**
```python
def rule_m77(g):
    legend=[v for v in g[0] if v!=0]
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True, ignore_positions={(0,c) for c in range(len(g[0]))}))
    by_color={}
    for col,cells in comps:
        by_color[col]=crop_bbox(g,cells)
    crops=[by_color[col] for col in legend]
    H=max(len(c) for c in crops)
    W=sum(len(c[0]) for c in crops)+(len(crops)-1)
    out=blank(H,W)
    x=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[r][x+c]=v
        x += len(crop[0])
        if i!=len(crops)-1:
            x += 1
    return out
```

## Hard (7)

### H71 — Overlapping Routed Links
**Difficulty:** hard
**Train pairs:** 4
**Skills:** path routing, overlap handling, terminal pairing
**Suggested staged path:** Decode the routing command first. Then route every terminal pair, and only after that handle cells claimed by more than one path.

**Train 1 — input**
```text
10000000
00400300
00000000
00000000
00000000
00300400
00000000
00000000
```
**Train 1 — output**
```text
10000000
00888800
00300400
00300400
00300400
00300400
00000000
00000000
```

**Train 2 — input**
```text
200000000
000000500
000000000
000000600
000000000
000000000
060500000
000000000
000000000
```
**Train 2 — output**
```text
200000000
000000500
000000500
000000800
000000800
000000800
066888800
000000000
000000000
```

**Train 3 — input**
```text
1000000000
0000000000
0007000030
0000000000
0400000000
0000000000
0000000070
0000000000
0003004000
0000000000
```
**Train 3 — output**
```text
1000000000
0000000000
0008888880
0003000070
0448444070
0003004070
0003004070
0003004000
0003004000
0000000000
```

**Train 4 — input**
```text
2000000000
0005000040
0000000000
0000000000
0000000000
0000000050
0004000000
0000000000
```
**Train 4 — output**
```text
2000000000
0005000040
0005000040
0005000040
0005000040
0005555580
0004444440
0000000000
```

**Test — input**
```text
1000000000
0060000300
0000000000
0000400000
0000000000
0000000000
0000000600
0030400000
0000000000
```
**Test — output**
```text
1000000000
0088888800
0030000600
0030400600
0030400600
0030400600
0030400600
0030400000
0000000000
```
**Written solution**

Use the command-selected bend policy to connect every same-colored terminal pair. Any cell traversed by multiple routed paths becomes overlap color 8.

**Reference program**
```python
def rule_h71(g):
    cmd=g[0][0]
    bend='row-first' if cmd==1 else 'col-first'
    endpoints=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    return link_terminals(g, endpoints, allow_bends=True, bend_policy=bend, overlap_color=8)
```

### H72 — Translation Analogy
**Difficulty:** hard
**Train pairs:** 4
**Skills:** relational analogy, translation vectors, object transfer
**Suggested staged path:** Compare the 2-object pair before touching the target object. The shift from color 2 to color 3 is the only transformation that matters.

**Train 1 — input**
```text
000000000000
022000000000
020000000000
000003300000
000003000000
004400000000
004400000000
000000000000
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
000000000000
000000440000
000000440000
```

**Train 2 — input**
```text
0000000000000
0000044400000
0022240400000
0002000000000
0000000000000
0000003330000
0000000300000
0000000000000
0000000000000
0000000000000
```
**Train 2 — output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000004440
0000000004040
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 3 — input**
```text
00000000000000
00000000022000
00000000444000
00000000420000
00000000000000
00003300000000
00003300000000
00003000000000
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
00044400000000
00040000000000
00000000000000
```

**Train 4 — input**
```text
000000000000000
000000000000000
020000000000000
022000000000000
002200000000000
000444030000000
000404033000000
000444003300000
000000000000000
000000000000000
000000000000000
```
**Train 4 — output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000444000
000000000404000
000000000444000
```

**Test — input**
```text
00000000000000
00004400000000
00222440000000
00200000000000
00000000000000
00000000000000
00000003330000
00000003000000
00000000000000
00000000000000
```
**Test — output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000044000
00000000004400
00000000000000
00000000000000
00000000000000
```
**Written solution**

Colors 2 and 3 show the same shape before and after a translation. Compute that translation vector and apply it to the color-4 object on a blank output grid.

**Reference program**
```python
def rule_h72(g):
    # colors 2,3 define translation; color 4 target
    by_color=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (2,3,4):
                by_color[v].append((r,c))
    r20,c20,_,_ = bbox(by_color[2])
    r30,c30,_,_ = bbox(by_color[3])
    dr,dc = r30-r20, c30-c20
    h,w=size(g)
    out=blank(h,w)
    for r,c in by_color[4]:
        nr,nc=r+dr,c+dc
        out[nr][nc]=4
    return out
```

### H73 — Nested Frame Depth Map
**Difficulty:** hard
**Train pairs:** 4
**Skills:** containment depth, nested rectangles, count-based recoloring
**Suggested staged path:** Ignore the original colors once you identify the frames. What matters is how many nested rectangles contain each cell.

**Train 1 — input**
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
**Train 1 — output**
```text
000000000
011111110
011111110
011222110
011222110
011222110
011111110
011111110
000000000
```

**Train 2 — input**
```text
000000000000
044444444440
040000000040
040555555040
040500005040
040500005040
040555555040
040000000040
044444444440
000000000000
```
**Train 2 — output**
```text
000000000000
011111111110
011111111110
011222222110
011222222110
011222222110
011222222110
011111111110
011111111110
000000000000
```

**Train 3 — input**
```text
00000000000
02222222220
02000000020
02066666020
02064446020
02064046020
02064446020
02066666020
02000000020
02222222220
00000000000
```
**Train 3 — output**
```text
00000000000
01111111110
01111111110
01122222110
01123332110
01123332110
01123332110
01122222110
01111111110
01111111110
00000000000
```

**Train 4 — input**
```text
00000000000000
03333333333330
03000000000030
03055555555030
03050000005030
03050777705030
03050777705030
03050000005030
03055555555030
03000000000030
03333333333330
00000000000000
```
**Train 4 — output**
```text
00000000000000
01111111111110
01111111111110
01122222222110
01122222222110
01122333322110
01122333322110
01122222222110
01122222222110
01111111111110
01111111111110
00000000000000
```

**Test — input**
```text
0000000000000
0222222222220
0204444444020
0204000004020
0204066604020
0204060604020
0204066604020
0204000004020
0204444444020
0222222222220
0000000000000
```
**Test — output**
```text
0000000000000
0111111111110
0112222222110
0112222222110
0112233322110
0112233322110
0112233322110
0112222222110
0112222222110
0111111111110
0000000000000
```
**Written solution**

Find the rectangular frames and count, for every grid cell, how many frame bounding boxes contain it. Output that containment depth as the new color, leaving outside cells at 0.

**Reference program**
```python
def rule_h73(g):
    h,w=size(g)
    comps=components_nonzero(g, treat_colors_separately=True)
    rects=[]
    for col,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        rects.append((r0,c0,r1,c1))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            depth=sum(1 for r0,c0,r1,c1 in rects if r0<=r<=r1 and c0<=c<=c1)
            out[r][c]=depth
    return out
```

### H74 — Symmetry Equivalence Matrix
**Difficulty:** hard
**Train pairs:** 4
**Skills:** dihedral symmetry, shape normalization, relation matrices
**Suggested staged path:** Normalize the objects before comparing them. Two shapes match if one can be rotated or reflected into the other.

**Train 1 — input**
```text
00000000000000
02220033000000
02000003000000
00000003000000
00000000000000
00000000004440
00000000000400
00000000000000
00000000000000
```
**Train 1 — output**
```text
880
880
008
```

**Train 2 — input**
```text
0000000000000
0220000000000
0022000000000
0000000550000
0000005500000
0000000000660
0000000000660
0000000000000
```
**Train 2 — output**
```text
880
880
008
```

**Train 3 — input**
```text
000000000000000
000000000000000
033000044000000
033000044000000
030000004000000
000000000007770
000000000000770
000000000000000
000000000000000
000000000000000
```
**Train 3 — output**
```text
888
888
888
```

**Train 4 — input**
```text
00000000000000
02220000000000
02020000550000
02220000550000
00000000000000
00000000000660
00000000000660
00000000000000
00000000000000
```
**Train 4 — output**
```text
800
088
088
```

**Test — input**
```text
000000000000000
022000000000000
020000000000000
000000440000000
000000040000000
000000000000000
000000000077700
000000000070700
000000000000000
000000000000000
```
**Test — output**
```text
880
880
008
```
**Written solution**

Crop the three objects, ignore their colors, and compare their binary shapes up to any rotation or reflection. Output 8 where two objects are dihedrally equivalent and 0 otherwise.

**Reference program**
```python
def rule_h74(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    bins=[]
    for col,cells in comps:
        crop=crop_bbox(g,cells)
        bins.append(normalize_binary(crop))
    n=len(bins)
    vars=[set(dihedral_variants(b)) for b in bins]
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if bins[j] in vars[i] else 0
    return out
```

### H75 — Command Composition Transform
**Difficulty:** hard
**Train pairs:** 4
**Skills:** sequential transforms, command execution, cropped outputs
**Suggested staged path:** Do not collapse the commands into one guess. Apply them in the given order to the cropped template.

**Train 1 — input**
```text
1000000000
0000000000
0000000000
0012000000
0034000000
0000000000
0000000000
0000000000
```
**Train 1 — output**
```text
31
42
```

**Train 2 — input**
```text
21000000000
00000000000
00000000000
00000500000
00000067000
00000008000
00000000000
00000000000
00000000000
```
**Train 2 — output**
```text
870
060
005
```

**Train 3 — input**
```text
430000000000
000000000000
000000000000
000000000000
002200000000
002030000000
000440000000
000000000000
000000000000
000000000000
```
**Train 3 — output**
```text
034
204
220
```

**Train 4 — input**
```text
1210000000
0000000000
0000000000
0000123000
0000405000
0000000000
0000000000
0000000000
0000000000
```
**Train 4 — output**
```text
321
504
```

**Test — input**
```text
34100000000
00000000000
00000000000
00000000000
00012000000
00034000000
00000000000
00000000000
00000000000
```
**Test — output**
```text
43
21
```
**Written solution**

Read the nonzero command strip from the top row left to right, crop the lower object, and apply the listed transforms in sequence: rotate, flip, or transpose.

**Reference program**
```python
def rule_h75(g):
    cmds=[]
    for v in g[0]:
        if v==0: break
        cmds.append(v)
    cells=[(r,c) for r in range(1,len(g)) for c,v in enumerate(g[r]) if v!=0]
    obj=crop_bbox(g,cells)
    cur=obj
    for cmd in cmds:
        if cmd==1:
            cur=rotate_cw(cur)
        elif cmd==2:
            cur=flip_h(cur)
        elif cmd==3:
            cur=flip_v(cur)
        elif cmd==4:
            cur=transpose(cur)
        else:
            raise ValueError(cmd)
    return cur
```

### H76 — Chamber Ownership Fill
**Difficulty:** hard
**Train pairs:** 4
**Skills:** flood fill, wall topology, region ownership
**Suggested staged path:** Use the 9s only as walls. Flood the open chambers, identify which chamber contains which marker, and then fill chamber interiors accordingly.

**Train 1 — input**
```text
999999999
920090039
900090009
900090009
999999999
940090059
900090009
900090009
999999999
```
**Train 1 — output**
```text
999999999
922293339
922293339
922293339
999999999
944495559
944495559
944495559
999999999
```

**Train 2 — input**
```text
9999999999
9500092009
9000090009
9000090009
9999999999
9300094009
9000090009
9000090009
9999999999
```
**Train 2 — output**
```text
9999999999
9555592229
9555592229
9555592229
9999999999
9333394449
9333394449
9333394449
9999999999
```

**Train 3 — input**
```text
99999999999
96000900039
90000900009
90000900009
99999999999
92000950009
90000900009
90000900009
99999999999
```
**Train 3 — output**
```text
99999999999
96666933339
96666933339
96666933339
99999999999
92222955559
92222955559
92222955559
99999999999
```

**Train 4 — input**
```text
999999999
970090009
900090009
900090009
999999999
900090009
900050009
900090009
999999999
```
**Train 4 — output**
```text
999999999
977790009
977790009
977790009
999999999
955595559
955555559
955595559
999999999
```

**Test — input**
```text
9999999999
9200096009
9000090009
9000090009
9999999999
9300094009
9000090009
9000090009
9999999999
```
**Test — output**
```text
9999999999
9222296669
9222296669
9222296669
9999999999
9333394449
9333394449
9333394449
9999999999
```
**Written solution**

Treat 9 as an impassable wall. For each open chamber, if it contains exactly one marker color, fill the whole chamber with that color while keeping walls unchanged.

**Reference program**
```python
def rule_h76(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                out[r][c]=9
    vis=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==9 or vis[r][c]:
                continue
            vis[r][c]=True
            q=[(r,c)]
            region=[]
            colors=set()
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if g[rr][cc] not in (0,9):
                    colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not vis[nr][nc] and g[nr][nc]!=9:
                        vis[nr][nc]=True; q.append((nr,nc))
            fill = next(iter(colors)) if len(colors)==1 else 0
            for rr,cc in region:
                if fill and g[rr][cc]==0:
                    out[rr][cc]=fill
                elif g[rr][cc]!=0 and g[rr][cc]!=9:
                    out[rr][cc]=g[rr][cc]
    return out
```

### H77 — Hole-Count Packing
**Difficulty:** hard
**Train pairs:** 4
**Skills:** hole counting, object ranking, normalized packing
**Suggested staged path:** Measure each object's holes before packing anything. Once ranked, just crop and place them side by side.

**Train 1 — input**
```text
000000000000000000
022200000000000000
020200003330000000
022200003000000000
000000000000000000
000000000000444440
000000000000404040
000000000000404040
000000000000404040
000000000000444440
000000000000000000
```
**Train 1 — output**
```text
3330222044444
3000202040404
0000222040404
0000000040404
0000000044444
```

**Train 2 — input**
```text
00000000000000000
05555500000000000
05050500002200000
05050500002200000
05050500000000000
05555566660000000
00000060060000000
00000066660000000
00000000000000000
00000000000000000
```
**Train 2 — output**
```text
2206666055555
2206006050505
0006666050505
0000000050505
0000000055555
```

**Train 3 — input**
```text
000000000000000000
000000000000000000
007700000000000000
007000000000000000
000000000004444400
000000000004040400
000000000004040400
000003330004040400
000003030004444400
000003330000000000
000000000000000000
000000000000000000
```
**Train 3 — output**
```text
770333044444
700303040404
000333040404
000000040404
000000044444
```

**Train 4 — input**
```text
00000000000000000
02222000000000000
02002000000000000
02222000055000000
00000000055000000
00000000050666660
00000000000606060
00000000000606060
00000000000606060
00000000000666660
00000000000000000
```
**Train 4 — output**
```text
5502222066666
5502002060606
5002222060606
0000000060606
0000000066666
```

**Test — input**
```text
000000000000000000
022222000000000000
020202000444000000
020202000400000000
020202000000000000
022222000000000000
000000000000066600
000000000000060600
000000000000066600
000000000000000000
000000000000000000
000000000000000000
```
**Test — output**
```text
4440666022222
4000606020202
0000666020202
0000000020202
0000000022222
```
**Written solution**

Count the enclosed holes in each object's tight crop, sort the objects by hole count from fewest to most, and pack the cropped shapes left to right with one blank separator column.

**Reference program**
```python
def rule_h77(g):
    comps=rowcol_sort_components(components_nonzero(g, treat_colors_separately=True))
    items=[]
    for idx,(col,cells) in enumerate(comps):
        crop=crop_bbox(g,cells)
        items.append((count_holes(crop), idx, crop))
    items.sort(key=lambda x:(x[0],x[1]))
    crops=[crop for _,_,crop in items]
    H=max(len(c) for c in crops)
    W=sum(len(c[0]) for c in crops)+(len(crops)-1)
    out=blank(H,W)
    x=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[r][x+c]=v
        x += len(crop[0])
        if i!=len(crops)-1:
            x += 1
    return out
```

