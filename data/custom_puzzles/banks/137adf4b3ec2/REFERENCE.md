# ARC Additional Puzzle Bank — 21 Puzzles (Set 22)
This twenty-second pack continues the numbering with **`E148–E154`**, **`M148–M154`**, and **`H148–H154`**.
This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.
It introduces a new helper primitive for solver-facing implementations:
```text
span_markers(markers)
```
Intuition: when two matching markers lie on one row or one column, recover the full closed interval between them. It is used directly in **E148**, **M152**, and **H152**.
Design goals for this set:

- easy: interval completion, bbox crops, diagonal symmetry, command-driven rotation, rectangle filling, square diagonals, and row filtering

- medium: object selection, legend-driven assembly, chamber flood fill, vector translation, span overlays, component histograms, and frame matching

- hard: transform analogy, nesting depth, Manhattan partitioning, dihedral shape comparison, overlap counting, palette transfer, and transform composition

## E148 — Complete the Axis Span
**Difficulty:** easy
**Train pairs:** 4
**Skills:** endpoint detection, axis-aligned completion, same-color fill
**Suggested staged path:** Ignore the empty space and look only at the two matching markers. Decide whether they share a row or a column, then fill the closed interval between them.

**Train 1 — input**
```text
000000000
000000000
080000080
000000000
000000000
000000000
```
**Train 1 — output**
```text
000000000
000000000
088888880
000000000
000000000
000000000
```
**Train 2 — input**
```text
000000
000400
000000
000000
000000
000000
000400
000000
```
**Train 2 — output**
```text
000000
000400
000400
000400
000400
000400
000400
000000
```
**Train 3 — input**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0060000060
0000000000
```
**Train 3 — output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0066666660
0000000000
```
**Train 4 — input**
```text
0000000
0000000
0000030
0000000
0000000
0000000
0000000
0000030
0000000
```
**Train 4 — output**
```text
0000000
0000000
0000030
0000030
0000030
0000030
0000030
0000030
0000000
```
**Test — input**
```text
00000000000
00000000000
00000000000
07000000070
00000000000
00000000000
00000000000
00000000000
```
**Test — output**
```text
00000000000
00000000000
00000000000
07777777770
00000000000
00000000000
00000000000
00000000000
```
**Written solution**

There are exactly two nonzero markers of the same color. They lie on one row or one column. Fill every cell from one marker to the other, inclusive, with that same color.

**Reference program**
```python
def rule_e148(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    color=pts[0][2]
    out=blank(*size(g),0)
    cells=span_markers([(pts[0][0],pts[0][1]),(pts[1][0],pts[1][1])])
    for r,c in cells:
        out[r][c]=color
    return out
```

## E149 — Tight Crop of the Motif
**Difficulty:** easy
**Train pairs:** 4
**Skills:** bounding box detection, output resizing, motif extraction
**Suggested staged path:** First forget the surrounding black area. Find the smallest rectangle that contains every nonzero cell, then output only that rectangle.

**Train 1 — input**
```text
000000000
000000000
000023000
000020300
000000000
000000000
000000000
000000000
```
**Train 1 — output**
```text
230
203
```
**Train 2 — input**
```text
0000000000
0000000000
0000000000
0045000000
0400400000
0000000000
0000000000
```
**Train 2 — output**
```text
0450
4004
```
**Train 3 — input**
```text
000000000
000000670
000006070
000007700
000000000
000000000
000000000
000000000
000000000
```
**Train 3 — output**
```text
067
607
770
```
**Train 4 — input**
```text
00000000000
00000000000
00000000000
00000000000
00028000000
00020200000
00002200000
00000000000
```
**Train 4 — output**
```text
280
202
022
```
**Test — input**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000340000
000000304000
000000044000
000000000000
000000000000
```
**Test — output**
```text
340
304
044
```
**Written solution**

All black padding is irrelevant. Compute the tight bounding box of the nonzero pattern and return just that cropped subgrid.

**Reference program**
```python
def rule_e149(g):
    return crop_bbox(g)
```

## E150 — Mirror Across the Main Diagonal
**Difficulty:** easy
**Train pairs:** 4
**Skills:** diagonal symmetry, same-size completion, coordinate transposition
**Suggested staged path:** Treat each colored cell as an instruction to also color its transposed position. Keep originals and add the reflected copy across the main diagonal.

**Train 1 — input**
```text
004000
000420
000000
000000
000000
000000
```
**Train 1 — output**
```text
004000
000420
400000
040000
020000
000000
```
**Train 2 — input**
```text
0000600
0003000
0000060
0000000
0000000
0000000
0000000
```
**Train 2 — output**
```text
0000600
0003000
0000060
0300000
6000000
0060000
0000000
```
**Train 3 — input**
```text
08020
00008
00000
00000
00000
```
**Train 3 — output**
```text
08020
80008
00000
20000
08000
```
**Train 4 — input**
```text
00005000
00000070
00000700
00000000
00000000
00000000
00000000
00000000
```
**Train 4 — output**
```text
00005000
00000070
00000700
00000000
50000000
00700000
07000000
00000000
```
**Test — input**
```text
000003
006030
000600
000000
000000
000000
```
**Test — output**
```text
000003
006030
060600
006000
030000
300000
```
**Written solution**

For every nonzero cell at row r and column c, copy the same color to position c,r. The result is the original pattern plus its mirror across the main diagonal.

**Reference program**
```python
def rule_e150(g):
    n,m=size(g)
    assert n==m
    out=clone(g)
    for r in range(n):
        for c in range(m):
            v=g[r][c]
            if v!=0:
                out[c][r]=v
    return out
```

## E151 — Rotate the Motif by the Corner Command
**Difficulty:** easy
**Train pairs:** 4
**Skills:** legend decoding, rotation, cropped output
**Suggested staged path:** Separate the command cell from the motif. Crop the motif first, then interpret the command value as which rotation to apply.

**Train 1 — input**
```text
200000000
000000000
000000000
000023000
000020300
000000000
000000000
000000000
```
**Train 1 — output**
```text
22
03
30
```
**Train 2 — input**
```text
30000000
00000000
00450000
00045000
00005000
00000000
00000000
```
**Train 2 — output**
```text
500
540
054
```
**Train 3 — input**
```text
400000000
000000000
000000000
000000000
000000000
000006700
000006070
000000000
000000000
```
**Train 3 — output**
```text
07
70
66
```
**Train 4 — input**
```text
1000000000
0000000000
0000000000
0000002800
0000002820
0000002200
0000000000
0000000000
```
**Train 4 — output**
```text
280
282
220
```
**Test — input**
```text
2000000000
0000000000
0000000000
0000000000
0034000000
0030400000
0004400000
0000000000
0000000000
```
**Test — output**
```text
033
404
440
```
**Written solution**

The top-left command chooses a rotation: 1 means leave the motif as-is, 2 means rotate 90 degrees clockwise, 3 means rotate 180 degrees, and 4 means rotate 270 degrees. Ignore the command cell itself, crop the remaining motif tightly, and output the rotated crop.

**Reference program**
```python
def rule_e151(g):
    code=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    motif=crop_bbox(g, cells=cells, ignore=set())
    return apply_transform(motif, code)
```

## E152 — Fill the Hollow Rectangle
**Difficulty:** easy
**Train pairs:** 4
**Skills:** rectangle inference, interior fill, same-size completion
**Suggested staged path:** Recognize that the nonzero cells are the border of one rectangle. Once the bounding box is clear, fill the whole box with that color.

**Train 1 — input**
```text
0000000000
0044444400
0040000400
0040000400
0040000400
0044444400
0000000000
0000000000
```
**Train 1 — output**
```text
0000000000
0044444400
0044444400
0044444400
0044444400
0044444400
0000000000
0000000000
```
**Train 2 — input**
```text
000000000
000000000
066666600
060000600
060000600
066666600
000000000
```
**Train 2 — output**
```text
000000000
000000000
066666600
066666600
066666600
066666600
000000000
```
**Train 3 — input**
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
**Train 3 — output**
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
**Train 4 — input**
```text
00000000000
00007777770
00007000070
00007000070
00007777770
00000000000
```
**Train 4 — output**
```text
00000000000
00007777770
00007777770
00007777770
00007777770
00000000000
```
**Test — input**
```text
000000000000
000000000000
000555555550
000500000050
000500000050
000500000050
000555555550
000000000000
```
**Test — output**
```text
000000000000
000000000000
000555555550
000555555550
000555555550
000555555550
000555555550
000000000000
```
**Written solution**

The colored cells form a hollow axis-aligned rectangle. Keep the same bounding box, but fill its entire interior and border with the rectangle's color.

**Reference program**
```python
def rule_e152(g):
    pts=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,c0,r1,c1=bbox(pts)
    color=g[pts[0][0]][pts[0][1]]
    out=blank(*size(g),0)
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            out[r][c]=color
    return out
```

## E153 — Draw the X from Square Corners
**Difficulty:** easy
**Train pairs:** 4
**Skills:** corner inference, diagonal drawing, square geometry
**Suggested staged path:** Use the four markers only to recover the square they define. Then draw both diagonals of that square in the same color.

**Train 1 — input**
```text
00000000
02000200
00000000
00000000
00000000
02000200
00000000
00000000
```
**Train 1 — output**
```text
00000000
02000200
00202000
00020000
00202000
02000200
00000000
00000000
```
**Train 2 — input**
```text
000000000
000000000
000600600
000000000
000000000
000600600
000000000
000000000
000000000
```
**Train 2 — output**
```text
000000000
000000000
000600600
000066000
000066000
000600600
000000000
000000000
000000000
```
**Train 3 — input**
```text
0000000000
0000700007
0000000000
0000000000
0000000000
0000000000
0000700007
0000000000
0000000000
0000000000
```
**Train 3 — output**
```text
0000000000
0000700007
0000070070
0000007700
0000007700
0000070070
0000700007
0000000000
0000000000
0000000000
```
**Train 4 — input**
```text
4000004
0000000
0000000
0000000
0000000
0000000
4000004
```
**Train 4 — output**
```text
4000004
0400040
0040400
0004000
0040400
0400040
4000004
```
**Test — input**
```text
000000000
008000800
000000000
000000000
000000000
008000800
000000000
000000000
000000000
```
**Test — output**
```text
000000000
008000800
000808000
000080000
000808000
008000800
000000000
000000000
000000000
```
**Written solution**

The four colored cells are the corners of a square. Draw both diagonals connecting opposite corners, using the same color as the markers, and leave everything else black.

**Reference program**
```python
def rule_e153(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    color=pts[0][2]
    coords=[(r,c) for r,c,v in pts]
    r0,c0,r1,c1=bbox(coords)
    side=r1-r0
    out=blank(*size(g),0)
    for i in range(side+1):
        out[r0+i][c0+i]=color
        out[r0+i][c1-i]=color
    return out
```

## E154 — Keep Only the Nonempty Rows
**Difficulty:** easy
**Train pairs:** 4
**Skills:** row filtering, output resizing, order preservation
**Suggested staged path:** Look row by row and ignore any row that is completely black. Stack the remaining rows in their original top-to-bottom order.

**Train 1 — input**
```text
00000000
02200000
00000000
00440000
00000000
00000000
00006600
```
**Train 1 — output**
```text
02200000
00440000
00006600
```
**Train 2 — input**
```text
0300000
0000000
0000000
0000000
0005500
0000000
0000000
7000007
```
**Train 2 — output**
```text
0300000
0005500
7000007
```
**Train 3 — input**
```text
000000000
000000000
000888000
000000000
000000000
404000404
```
**Train 3 — output**
```text
000888000
404000404
```
**Train 4 — input**
```text
000000
066000
000033
000000
000000
000000
000000
000000
222000
```
**Train 4 — output**
```text
066000
000033
222000
```
**Test — input**
```text
00500000
00000000
00000000
77000000
00000000
00002220
00000000
00000000
```
**Test — output**
```text
00500000
77000000
00002220
```
**Written solution**

Delete every all-zero row. The output is just the nonempty rows, preserved in the same order and with the same width as before.

**Reference program**
```python
def rule_e154(g):
    return [row[:] for row in g if any(v!=0 for v in row)]
```

## M148 — Crop the Largest Component
**Difficulty:** medium
**Train pairs:** 4
**Skills:** connected components, size comparison, bounding box crop
**Suggested staged path:** First split the grid into disconnected objects. Compare their areas, keep only the largest one, and crop it tightly.

**Train 1 — input**
```text
000000000000
022000000000
020000000000
000000000000
000000033000
000000003300
004000000300
004400000000
000000000000
```
**Train 1 — output**
```text
330
033
003
```
**Train 2 — input**
```text
0000000000
0000055000
0000050500
0000055500
0000000700
0000000000
0660000000
0600000000
0000000000
0000000000
```
**Train 2 — output**
```text
550
505
555
007
```
**Train 3 — input**
```text
0000000000000
0280000000000
0282000033000
0220000030000
0000000000000
0000044000000
0000004400000
0000000000000
```
**Train 3 — output**
```text
280
282
220
```
**Train 4 — input**
```text
67000000000
60700000000
00000000000
00000000000
00000023000
00000020300
00000022000
00800000000
00000000000
```
**Train 4 — output**
```text
23
20
22
```
**Test — input**
```text
000000000000
000000000330
004500000000
004050000000
004440000000
000000000000
000000000000
000000280000
000000202000
000000000000
```
**Test — output**
```text
450
405
444
```
**Written solution**

Treat each disconnected nonzero object as one component. Select the component with the most cells and output its tight bounding box, preserving its colors.

**Reference program**
```python
def rule_m148(g):
    comps=components(g, ignore={0}, color_sensitive=False)
    best=max(comps, key=lambda comp: len(comp["cells"]))
    return crop_bbox(g, cells=best["cells"], ignore=set())
```

## M149 — Assemble Components by Legend Order
**Difficulty:** medium
**Train pairs:** 4
**Skills:** legend reading, component extraction, horizontal packing
**Suggested staged path:** Use the top row only as an ordering legend. Find the component matching each legend color, crop each one, and then place those crops left-to-right in the legend order.

**Train 1 — input**
```text
04020700000000
00000000000000
02200440000000
02000044007000
00000000007700
```
**Train 1 — output**
```text
440022070
044020077
```
**Train 2 — input**
```text
060308000000000
000000000000000
000000808000000
033000888006000
003000000006600
```
**Train 2 — output**
```text
600330808
660030888
```
**Train 3 — input**
```text
0507020000000000
0000000000000000
0022000000005550
0020200070005000
0000000077000000
0000000007000000
```
**Train 3 — output**
```text
55507002
50007700
00000700
```
**Train 4 — input**
```text
080406000000000
000000000000000
040000000008080
044000660000800
000000600000000
000000660000000
```
**Train 4 — output**
```text
8040066
0044060
0000066
```
**Test — input**
```text
0705030000000000
0000000000000000
0330000000070700
0003000500007700
0000000550000000
```
**Test — output**
```text
0705003
7705500
```
**Written solution**

The top row lists the colors in the desired order. Below it, each listed color appears as exactly one component. Crop each component tightly and concatenate the crops from left to right with a single black column between neighbors.

**Reference program**
```python
def rule_m149(g):
    order=[v for v in g[0] if v!=0]
    below=[row[:] for row in g[1:]]
    comps=components(below, ignore={0}, color_sensitive=True)
    keyed={}
    for comp in comps:
        color=comp["color"]
        crop=crop_bbox(below, cells=comp["cells"], ignore=set())
        keyed[color]=crop
    pieces=[keyed[c] for c in order]
    h=max(size(p)[0] for p in pieces)
    gap=1
    total_w=sum(size(p)[1] for p in pieces)+gap*(len(pieces)-1)
    out=blank(h,total_w,0)
    c0=0
    for idx,p in enumerate(pieces):
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                if p[r][c]!=0:
                    out[r][c0+c]=p[r][c]
        c0 += pw
        if idx < len(pieces)-1:
            c0 += gap
    return out
```

## M150 — Flood Each Chamber from Its Seed
**Difficulty:** medium
**Train pairs:** 4
**Skills:** chamber detection, wall-aware flood fill, seed propagation
**Suggested staged path:** Treat the wall color as blocking cells and identify the empty regions it creates. Each region touches one colored seed; fill that region with the seed color.

**Train 1 — input**
```text
88888888888
80000800008
80200800008
80000800008
80000800008
80000800008
80000800408
80000800008
88888888888
```
**Train 1 — output**
```text
88888888888
82222844448
82222844448
82222844448
82222844448
82222844448
82222844448
82222844448
88888888888
```
**Train 2 — input**
```text
8888888888
8000000008
8000000308
8000000008
8000000008
8888888888
8000000008
8060000008
8000000008
8888888888
```
**Train 2 — output**
```text
8888888888
8333333338
8333333338
8333333338
8333333338
8888888888
8666666668
8666666668
8666666668
8888888888
```
**Train 3 — input**
```text
8888888888888
8000800080008
8000800080008
8050800080008
8000800080008
8000800080008
8000802080008
8000800080008
8000800080708
8000800080008
8888888888888
```
**Train 3 — output**
```text
8888888888888
8555822287778
8555822287778
8555822287778
8555822287778
8555822287778
8555822287778
8555822287778
8555822287778
8555822287778
8888888888888
```
**Train 4 — input**
```text
888888888888
800000800008
804000806008
800000800008
888888888888
800000800008
800000800008
800300800508
800000800008
888888888888
```
**Train 4 — output**
```text
888888888888
844444866668
844444866668
844444866668
888888888888
833333855558
833333855558
833333855558
833333855558
888888888888
```
**Test — input**
```text
888888888888
800080008008
802080008008
800080008008
800080708008
800080008008
800080008038
800080008008
888888888888
```
**Test — output**
```text
888888888888
822287778338
822287778338
822287778338
822287778338
822287778338
822287778338
822287778338
888888888888
```
**Written solution**

The wall color partitions the grid into chambers. Every chamber contains exactly one colored seed. Replace the zeros in that chamber with the seed color while leaving the walls unchanged.

**Reference program**
```python
def rule_m150(g):
    return fill_chamber(g, wall=8)
```

## M151 — Translate the Payload by the Anchor Vector
**Difficulty:** medium
**Train pairs:** 4
**Skills:** vector extraction, translation, object isolation
**Suggested staged path:** Ignore the payload at first and compute the vector from the source anchor to the target anchor. Then apply that same vector to every payload cell.

**Train 1 — input**
```text
0000000000
0200000000
0044000000
0040000000
0000030000
0000000000
0000000000
0000000000
0000000000
```
**Train 1 — output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000004400
0000004000
0000000000
0000000000
```
**Train 2 — input**
```text
00000000000
00000000000
00000000200
00000002300
00000002030
00000000000
00003000000
00000000000
00000000000
00000000000
```
**Train 2 — output**
```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Train 3 — input**
```text
000000000000
067000000020
060700000000
000000000000
000000000000
000000300000
000000000000
000000000000
```
**Train 3 — output**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Train 4 — input**
```text
00000000000
00000000000
00000000000
00000000000
00000300000
00000000000
00550000000
00505000000
02000000000
00000000000
00000000000
```
**Train 4 — output**
```text
00000000000
00000000000
00000055000
00000050500
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Test — input**
```text
000000000000
002000000000
028000000000
028200000000
022000000000
000000000000
000000003000
000000000000
000000000000
000000000000
```
**Test — output**
```text
000000000000
000000000000
000000000000
000000000000
000000008000
000000008000
000000000000
000000000000
000000000000
000000000000
```
**Written solution**

One anchor marks the starting point and another marks the destination. Compute the offset from the first anchor to the second, remove the anchors, and copy the payload component after translating every one of its cells by that offset.

**Reference program**
```python
def rule_m151(g):
    h,w=size(g)
    src=dst=None
    payload=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==2:
                src=(r,c)
            elif v==3:
                dst=(r,c)
            elif v!=0:
                payload.append((r,c,v))
    dr=dst[0]-src[0]; dc=dst[1]-src[1]
    out=blank(h,w,0)
    for r,c,v in payload:
        rr,cc=r+dr,c+dc
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=v
    return out
```

## M152 — Span Overlay with Crossings
**Difficulty:** medium
**Train pairs:** 4
**Skills:** pairwise span inference, overlap handling, same-size synthesis
**Suggested staged path:** Recover each axis-aligned span independently from its matching marker pair. Only after that should you merge the spans and mark any shared cells specially.

**Train 1 — input**
```text
0000400000
0200000200
0000000000
0000000000
0000000000
0000000000
0000400000
0000000000
```
**Train 1 — output**
```text
0000400000
0222922200
0000400000
0000400000
0000400000
0000400000
0000400000
0000000000
```
**Train 2 — input**
```text
000000000
000000700
030000000
000000000
000000000
600000006
000000000
030000700
000000000
```
**Train 2 — output**
```text
000000000
000000700
030000700
030000700
030000700
696666966
030000700
030000700
000000000
```
**Train 3 — input**
```text
000000000000
000005000000
000000000000
002000000020
000000000000
000000000000
070000000700
000000000000
000005000000
000000000000
```
**Train 3 — output**
```text
000000000000
000005000000
000005000000
002229222220
000005000000
000005000000
077779777700
000005000000
000005000000
000000000000
```
**Train 4 — input**
```text
00000200000
00000000040
00000000000
00000000000
00600000006
00000000000
00000000040
00000200000
```
**Train 4 — output**
```text
00000200000
00000200040
00000200040
00000200040
00666966696
00000200040
00000200040
00000200000
```
**Test — input**
```text
0000005000000
0000000000000
0300000000030
0000000000000
0000000000000
0007000000700
0000000000000
0000000000000
0000005000000
```
**Test — output**
```text
0000005000000
0000005000000
0333339333330
0000005000000
0000005000000
0007779777700
0000005000000
0000005000000
0000005000000
```
**Written solution**

Each color appears exactly twice and those two markers define one horizontal or vertical span. Draw all such spans. Cells covered by only one span keep that span's color, while cells where two or more spans overlap become 9.

**Reference program**
```python
def rule_m152(g):
    h,w=size(g)
    by_color=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    cover=collections.defaultdict(list)
    for color, pts in by_color.items():
        cells=span_markers(pts)
        for cell in cells:
            cover[cell].append(color)
    out=blank(h,w,0)
    for (r,c), colors in cover.items():
        out[r][c]=9 if len(colors)>1 else colors[0]
    return out
```

## M153 — Histogram of Component Colors
**Difficulty:** medium
**Train pairs:** 4
**Skills:** component counting, color grouping, structured output
**Suggested staged path:** Do not count cells; count disconnected components for each color. Then build one output row per present color, ordered from smallest color to largest.

**Train 1 — input**
```text
00000000000
02002000000
00000000000
00330000000
00000000000
00000003000
00000000044
00000000040
```
**Train 1 — output**
```text
22
33
40
```
**Train 2 — input**
```text
0000000000
0550005000
0000000000
0000000000
0020000000
0000000000
0000020000
0000000020
0000000000
```
**Train 2 — output**
```text
222
550
```
**Train 3 — input**
```text
000000000000
060000004400
000000004000
000600000000
000000000000
000006000000
000000000000
000000000400
000000000000
000000000000
```
**Train 3 — output**
```text
440
666
```
**Train 4 — input**
```text
00000000000
00000000000
00700007700
00000000000
00000000000
03000300030
00000000000
00000000000
00000000000
```
**Train 4 — output**
```text
333
770
```
**Test — input**
```text
0000000000
0200020020
0000000000
0000000000
0044000000
0000000000
0000005000
0000000000
0000000000
0000000000
```
**Test — output**
```text
222
400
500
```
**Written solution**

Count how many connected components exist for each nonzero color. Sort the colors in ascending order. For each color, output a row containing that color repeated once per component, padded on the right with zeros to the maximum row length.

**Reference program**
```python
def rule_m153(g):
    counts=collections.Counter()
    h,w=size(g)
    # Count connected components per color
    seen=set()
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or (r,c) in seen:
                continue
            q=[(r,c)]; seen.add((r,c)); cells=[]
            while q:
                rr,cc=q.pop(); cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]==v:
                        seen.add((nr,nc)); q.append((nr,nc))
            counts[v]+=1
    colors=sorted(counts)
    width=max(counts.values()) if counts else 1
    out=blank(len(colors), width, 0)
    for r,color in enumerate(colors):
        for c in range(counts[color]):
            out[r][c]=color
    return out
```

## M154 — Copy the Template into the Matching Frame
**Difficulty:** medium
**Train pairs:** 4
**Skills:** template extraction, frame detection, size matching
**Suggested staged path:** First isolate the multicolor template and measure its cropped size. Then scan the empty frames and choose the one whose interior has exactly the same height and width.

**Train 1 — input**
```text
00000000000000
02300000888880
02030000800080
00000000800080
00000000888880
00000008888800
00000008000800
00000008000800
00000008000800
00000008888800
```
**Train 1 — output**
```text
00000000000000
02300000888880
02030000800080
00000000800080
00000000888880
00000008888800
00000008000800
00000008000800
00000008000800
00000008888800
```
**Train 2 — input**
```text
000000000000000
000000000888880
045000000800080
040500000800080
044400000800080
000000000888880
000000008888800
000000008000800
000000008000800
000000008888800
000000000000000
```
**Train 2 — output**
```text
000000000000000
000000000888880
045000000800080
040500000800080
044400000800080
000000000888880
000000008888800
000000008000800
000000008000800
000000008888800
000000000000000
```
**Train 3 — input**
```text
00000000000000
00000000888800
00000000800800
00000000800800
00000000888800
00000000888880
06700000800080
06070000800080
00000000800080
00000000888880
```
**Train 3 — output**
```text
00000000000000
00000000888800
00000000800800
00000000800800
00000000888800
00000000888880
06700000800080
06070000800080
00000000800080
00000000888880
```
**Train 4 — input**
```text
0000000000000000
0000000000888880
0280000000800080
0282000000800080
0220000000800080
0000000000888880
0000000008888800
0000000008000800
0000000008000800
0000000008888800
0000000000000000
0000000000000000
```
**Train 4 — output**
```text
0000000000000000
0000000000888880
0280000000800080
0282000000800080
0220000000800080
0000000000888880
0000000008888800
0000000008000800
0000000008000800
0000000008888800
0000000000000000
0000000000000000
```
**Test — input**
```text
000000000000000
000000000888880
000000000800080
000000000800080
000000000800080
000000000888880
034000000888888
030400000800008
004400000800008
000000000800008
000000000888888
```
**Test — output**
```text
000000000000000
000000000888880
000000000800080
000000000800080
000000000800080
000000000888880
034000000888888
030400000800008
004400000800008
000000000800008
000000000888888
```
**Written solution**

Crop the non-frame template tightly. Among the empty rectangular frames, exactly one has an interior whose size matches the template. Copy the template into that frame's interior, aligned to the interior's top-left corner, and leave everything else unchanged.

**Reference program**
```python
def rule_m154(g):
    out=clone(g)
    # template: all nonzero non-8 cells
    temp_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,8)]
    temp=crop_bbox(g, cells=temp_cells, ignore=set())
    th,tw=size(temp)
    for r0,c0,r1,c1 in find_rect_frames(g, color=8):
        ih,iw=r1-r0-1,c1-c0-1
        if (ih,iw)==(th,tw):
            for r in range(th):
                for c in range(tw):
                    if temp[r][c]!=0:
                        out[r0+1+r][c0+1+c]=temp[r][c]
            break
    return out
```

## H148 — Transform Analogy Across Panels
**Difficulty:** hard
**Train pairs:** 4
**Skills:** panel parsing, transform inference, analogy transfer
**Suggested staged path:** Split the input into the three separator-defined panels. Infer which geometric transform turns panel A into panel B, then apply that same transform to panel C.

**Train 1 — input**
```text
00000922000900000
02300903000904400
02030930000904040
00000900000900000
00000900000900000
```
**Train 1 — output**
```text
44
04
40
```
**Train 2 — input**
```text
00000906500900000
56000960500907700
50600900500907070
50000900000900000
00000900000900000
```
**Train 2 — output**
```text
077
707
```
**Train 3 — input**
```text
03400904400900000
03040940400966000
00440933000906000
00000900000900000
00000900000900000
```
**Train 3 — output**
```text
66
60
```
**Train 4 — input**
```text
00000902200904500
02800920200904050
02020908200900000
02200900000900000
00000900000900000
```
**Train 4 — output**
```text
504
054
```
**Test — input**
```text
00000966000900000
06700907000903300
06070970000903030
00000900000903000
00000900000900000
```
**Test — output**
```text
333
003
030
```
**Written solution**

The first two panels show an example transform: panel B is panel A after a rotation or reflection. Detect which transform was used by comparing the cropped nonzero shapes in those panels, then apply that transform to the cropped shape in panel C and output the result.

**Reference program**
```python
def rule_h148(g):
    panels=split_panels_by_sep(g, sep=9)
    a,b,c=panels
    code=detect_transform(a,b)
    return apply_transform(crop_bbox(c), code)
```

## H149 — Recolor Nested Frames by Depth
**Difficulty:** hard
**Train pairs:** 4
**Skills:** nested-object reasoning, area ranking, depth encoding
**Suggested staged path:** Treat each rectangular border as a separate object and order them from outside to inside. Once the nesting order is clear, recolor by depth.

**Train 1 — input**
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
**Train 1 — output**
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
**Train 2 — input**
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
**Train 2 — output**
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
**Train 3 — input**
```text
00000000000000
00111111111100
00100000000100
00101111110100
00101000010100
00101000010100
00101000010100
00101000010100
00101111110100
00100000000100
00111111111100
00000000000000
```
**Train 3 — output**
```text
00000000000000
00222222222200
00200000000200
00203333330200
00203000030200
00203000030200
00203000030200
00203000030200
00203333330200
00200000000200
00222222222200
00000000000000
```
**Train 4 — input**
```text
000000000000000
011111111111110
010000000000010
010111111111010
010100000001010
010101111101010
010101000101010
010101010101010
010101000101010
010101111101010
010100000001010
010111111111010
010000000000010
011111111111110
000000000000000
```
**Train 4 — output**
```text
000000000000000
022222222222220
020000000000020
020333333333020
020300000003020
020304444403020
020304000403020
020304050403020
020304000403020
020304444403020
020300000003020
020333333333020
020000000000020
022222222222220
000000000000000
```
**Test — input**
```text
000000000000000
001111111111100
001000000000100
001011111110100
001010000010100
001010111010100
001010101010100
001010111010100
001010000010100
001011111110100
001000000000100
001111111111100
000000000000000
```
**Test — output**
```text
000000000000000
002222222222200
002000000000200
002033333330200
002030000030200
002030444030200
002030404030200
002030444030200
002030000030200
002033333330200
002000000000200
002222222222200
000000000000000
```
**Written solution**

The grid contains several nested rectangular borders, all initially in color 1. Sort those frame borders by decreasing bounding-box area so the outermost frame comes first. Recolor the outermost frame to 2, the next one to 3, then 4, and so on inward.

**Reference program**
```python
def rule_h149(g):
    comps=components_of_color(g, 1)
    ordered=sorted(comps, key=lambda cells: ((bbox(cells)[2]-bbox(cells)[0]+1)*(bbox(cells)[3]-bbox(cells)[1]+1)), reverse=True)
    out=blank(*size(g),0)
    for idx,cells in enumerate(ordered, start=2):
        for r,c in cells:
            out[r][c]=idx
    return out
```

## H150 — Voronoi Fill Inside the Frame
**Difficulty:** hard
**Train pairs:** 4
**Skills:** distance reasoning, tie handling, region partitioning
**Suggested staged path:** Leave the wall cells alone and reason only about the interior. For each empty interior cell, compare its Manhattan distance to the seeds and handle ties explicitly.

**Train 1 — input**
```text
555555555
500000005
502000405
500000005
500000005
500000005
500070005
500000005
555555555
```
**Train 1 — output**
```text
555555555
522284445
522284445
522284445
522878445
588777885
577777775
577777775
555555555
```
**Train 2 — input**
```text
55555555555
50000000005
50300000605
50000000005
50000000005
50000000005
50000000005
50000200005
50000000005
55555555555
```
**Train 2 — output**
```text
55555555555
53333866665
53333866665
53333866665
53338286665
53382228665
58822222885
52222222225
52222222225
55555555555
```
**Train 3 — input**
```text
55555555555
50000000005
50000000005
50040007005
50000000005
50000000005
50000000005
50020006005
50000000005
50000000005
55555555555
```
**Train 3 — output**
```text
55555555555
54444877775
54444877775
54444877775
54444877775
58888888885
52222866665
52222866665
52222866665
52222866665
55555555555
```
**Train 4 — input**
```text
555555555555
500000000005
500300002005
500000000005
500000000005
500000000005
500004000005
500000000005
555555555555
```
**Train 4 — output**
```text
555555555555
533333222225
533333222225
533338222225
533384422225
588844442225
544444444445
544444444445
555555555555
```
**Test — input**
```text
5555555555
5000000005
5020000605
5000000005
5000000005
5000000005
5000000005
5000400005
5000000005
5555555555
```
**Test — output**
```text
5555555555
5222266665
5222266665
5222266665
5222486665
5224448665
5444444885
5444444445
5444444445
5555555555
```
**Written solution**

The boundary color 5 forms a closed frame. Interior zeros are assigned to the nearest seed by Manhattan distance. If a cell is tied between two or more seeds, color it 8. Keep the seeds and the frame as they are.

**Reference program**
```python
def rule_h150(g):
    h,w=size(g)
    out=clone(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            best=min(abs(sr-r)+abs(sc-c) for sr,sc,_ in seeds)
            colors=[v for sr,sc,v in seeds if abs(sr-r)+abs(sc-c)==best]
            out[r][c]=colors[0] if len(colors)==1 else 8
    return out
```

## H151 — Dihedral Equality Matrix
**Difficulty:** hard
**Train pairs:** 4
**Skills:** shape normalization, rotation/flip equivalence, matrix output
**Suggested staged path:** First split the input into its separate objects and ignore their colors. For each object, compute its shape up to rotation and reflection, then compare every pair.

**Train 1 — input**
```text
000000000000000
022000200003330
020000220000300
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 1 — output**
```text
220
220
002
```
**Train 2 — input**
```text
00000000000000000
00000000040000000
04400000440005500
00440000000005000
00000000000005000
00000000000000000
00000000000000000
00000000000000000
```
**Train 2 — output**
```text
200
020
002
```
**Train 3 — input**
```text
000000000000000000
000000000000077000
066000006000007000
006000066000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```
**Train 3 — output**
```text
222
222
222
```
**Train 4 — input**
```text
0000000000000000
0280000000003300
0220000022003000
0000000082000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Train 4 — output**
```text
202
020
202
```
**Test — input**
```text
00000000000000000
04500000000006600
04450005440000600
00000004500000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Test — output**
```text
202
020
202
```
**Written solution**

Each disconnected object is one shape. Two shapes count as equal if one can be rotated or reflected to match the other. Order the objects by their top-left positions and output a square matrix with 2 where a pair of shapes is dihedrally equivalent and 0 otherwise.

**Reference program**
```python
def rule_h151(g):
    comps=sorted(components(g, ignore={0}, color_sensitive=False), key=lambda comp: bbox(comp["cells"])[:2])
    shape_sets=[all_dihedral_shapes(crop_bbox(g, cells=comp["cells"], ignore=set())) for comp in comps]
    n=len(shape_sets)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            out[i][j]=2 if shape_sets[i] & shape_sets[j] else 0
    return out
```

## H152 — Overlap Count of Multiple Spans
**Difficulty:** hard
**Train pairs:** 4
**Skills:** multi-span reasoning, coverage counting, special-case overlap colors
**Suggested staged path:** Recover every axis-aligned span first, exactly as in the easier span task. Then ignore the individual colors and count how many spans cover each cell.

**Train 1 — input**
```text
00000400000
02000000020
00000000000
00000000000
00600000600
00000000000
00000000000
00000000000
00000400000
```
**Train 1 — output**
```text
00000000000
00000800000
00000000000
00000000000
00000800000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 — input**
```text
0000000000
0000000000
0300000700
0000000000
0000000000
5000000005
0000000000
0000000000
0300000700
0000000000
```
**Train 2 — output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0800000800
0000000000
0000000000
0000000000
0000000000
```
**Train 3 — input**
```text
0000004000000
0006000000000
0000000000000
0020000000200
0000000000000
0700000000070
0000000000000
0006000000000
0000004000000
```
**Train 3 — output**
```text
0000000000000
0000000000000
0000000000000
0008008000000
0000000000000
0008008000000
0000000000000
0000000000000
0000000000000
```
**Train 4 — input**
```text
00000000000
03000400000
00000000700
00000000000
00000000000
60000000006
00000000000
00000000000
00000000700
03000400000
00000000000
```
**Train 4 — output**
```text
00000000000
00000000000
00000000000
00000000000
00000000000
08000800800
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Test — input**
```text
000000400000
000070000000
020000000020
000000000000
000000000000
006000000600
000000000000
000000000000
000070000000
000000400000
```
**Test — output**
```text
000000000000
000000000000
000080800000
000000000000
000000000000
000080800000
000000000000
000000000000
000000000000
000000000000
```
**Written solution**

Each repeated color defines one horizontal or vertical span between its two markers. Count, for every cell, how many of these spans pass through it. Cells covered by exactly two spans become 8, cells covered by three or more spans become 9, and all other cells stay 0.

**Reference program**
```python
def rule_h152(g):
    h,w=size(g)
    by_color=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by_color[v].append((r,c))
    cover=collections.Counter()
    for color,pts in by_color.items():
        for cell in span_markers(pts):
            cover[cell]+=1
    out=blank(h,w,0)
    for (r,c), n in cover.items():
        if n==2:
            out[r][c]=8
        elif n>=3:
            out[r][c]=9
    return out
```

## H153 — Transfer a Color Mapping
**Difficulty:** hard
**Train pairs:** 4
**Skills:** palette inference, panel analogy, recoloring
**Suggested staged path:** Use the first two panels only to infer a color-to-color mapping. Once that mapping is known, apply it to the third panel's cropped motif.

**Train 1 — input**
```text
00000900000900000
02300904700903200
02030904070903020
00000900000900000
00000900000900000
```
**Train 1 — output**
```text
740
704
```
**Train 2 — input**
```text
00000900000900000
45000962000905400
40500960200900050
04400906600900000
00000900000900000
```
**Train 2 — output**
```text
260
002
```
**Train 3 — input**
```text
00000900000907600
06700903800907070
06070903080900000
00000900000900000
00000900000900000
```
**Train 3 — output**
```text
830
808
```
**Train 4 — input**
```text
00000900000900000
02800905400982000
02020905050928200
02200905500900000
00000900000900000
```
**Train 4 — output**
```text
450
545
```
**Test — input**
```text
00000900000900000
03400907200904300
03040907020904040
00440900220900000
00000900000900000
```
**Test — output**
```text
270
202
```
**Written solution**

Panels A and B have the same shape layout, but B recolors A by a consistent palette mapping. Infer that mapping from corresponding nonzero cells, then apply the same color substitution to panel C's cropped pattern and output the recolored crop.

**Reference program**
```python
def rule_h153(g):
    panels=split_panels_by_sep(g, sep=9)
    a,b,c=panels
    # derive color map from overlapping nonzero cells in cropped panels? better use full panels same size
    mapping={}
    for r in range(len(a)):
        for col in range(len(a[0])):
            va=a[r][col]; vb=b[r][col]
            if va!=0:
                mapping[va]=vb
    out=crop_bbox(c)
    for r,row in enumerate(out):
        for col,v in enumerate(row):
            if v!=0:
                out[r][col]=mapping[v]
    return out
```

## H154 — Compose Two Transform Commands
**Difficulty:** hard
**Train pairs:** 4
**Skills:** command composition, geometric transforms, cropped output
**Suggested staged path:** Treat the two command cells as an ordered sequence rather than a single code. Crop the motif, apply the first transform, then apply the second to the result.

**Train 1 — input**
```text
250000000
000000000
000000000
000023000
000020300
```
**Train 1 — output**
```text
22
30
03
```
**Train 2 — input**
```text
4300000000
0000000000
0000045000
0000004500
0000000500
```
**Train 2 — output**
```text
004
045
550
```
**Train 3 — input**
```text
520000000
000000000
000000000
000000000
006700000
006070000
```
**Train 3 — output**
```text
70
07
66
```
**Train 4 — input**
```text
34000000000
00000000000
00000000000
00000028000
00000028200
00000022000
```
**Train 4 — output**
```text
222
288
020
```
**Test — input**
```text
2600000000
0000000000
0000000000
0003400000
0003040000
0000440000
```
**Test — output**
```text
440
404
033
```
**Written solution**

The two command values on the top row specify two geometric transforms in order. Crop the motif below them, apply the first transform, then apply the second. Commands use the same code system as the single-command rotation task, extended with 5 for horizontal flip and 6 for vertical flip.

**Reference program**
```python
def rule_h154(g):
    code1,code2=[v for v in g[0] if v!=0][:2]
    motif=[row[:] for row in g[1:]]
    motif=crop_bbox(motif)
    return apply_transform(apply_transform(motif, code1), code2)
```
