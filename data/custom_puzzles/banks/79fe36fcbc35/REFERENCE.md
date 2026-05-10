# ARC Additional Puzzle Bank — 21 Puzzles (Set 8)

This eighth pack continues the numbering with **`E50–E56`**, **`M50–M56`**, and **`H50–H56`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
reflect_across_guide(base_grid, cells, axis, guide_pos, keep_original=True, overlap_color=None)
```

Intuition: reflect a set of colored cells across a horizontal or vertical guide line while optionally keeping the originals. This primitive is used directly in **E50**, **M50**, and **H50**.

Design goals for this set:

- easy: direct reflections, segment filling, row flooding, compression, rectangle inference, cropping, and color counting

- medium: selector-driven mirroring, frame-local packing, motif tiling, command transforms, matrix slicing, component sorting, and template recoloring

- hard: dual-guide symmetry, relational matrices, nested ownership, rank selection with transforms, alternating tile variants, per-frame routing, and compositional extract-then-rotate tasks

## Easy (7)

### E50 — Guide Mirror Copy

**Difficulty:** easy

**Train pairs:** 4

**Skills:** reflection, guide line, same-color symmetry

**Suggested staged path:** Find the full guide line first. Then mirror each nonzero cell to the opposite side at the same distance.

**Train 1 — input**

```text
000050000
020050000
003050000
000050000
000050000
700050000
000050000
000050000
```

**Train 1 — output**

```text
000050000
020050020
003050300
000050000
000050000
700050007
000050000
000050000
```

**Train 2 — input**

```text
0400050000
0000050000
0000050000
0060050000
0000050000
0000050000
0008050000
```

**Train 2 — output**

```text
0400050004
0000050000
0000050000
0060050060
0000050000
0000050000
0008050800
```

**Train 3 — input**

```text
00000050000
00000050000
09000050000
00000050000
00020050000
00000050000
00000050000
50000050000
00000050000
```

**Train 3 — output**

```text
00000050000
00000050000
09000050000
00000050000
00020050020
00000050000
00000050000
50000050000
00000050000
```

**Train 4 — input**

```text
00050000
40050000
00050000
00050000
07050000
00050000
00250000
00050000
```

**Train 4 — output**

```text
00050000
40050040
00050000
00050000
07050700
00050000
00252000
00050000
```

**Test — input**

```text
0000050000
0300050000
0000050000
0080050000
0000050000
0000050000
4000050000
0000050000
0000050000
```

**Test — output**

```text
0000050000
0300050003
0000050000
0080050080
0000050000
0000050000
4000050000
0000050000
0000050000
```

**Written solution**

Locate the full 5-colored guide line. Keep every original nonzero cell, and add its mirror image across that guide.

**Reference program**

```python
def rule_e50(g):
    rows, cols = find_full_guides(g, 5)
    out = clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    if cols:
        out = reflect_across_guide(out, cells, 'v', cols[0], keep_original=True)
    elif rows:
        out = reflect_across_guide(out, cells, 'h', rows[0], keep_original=True)
    return out
```

### E51 — Straight Segment Completion

**Difficulty:** easy

**Train pairs:** 4

**Skills:** endpoint pairing, row/column completion, line filling

**Suggested staged path:** Ignore colors with only one cell. Pair identical endpoints, then fill the straight gap if they share a row or a column.

**Train 1 — input**

```text
000000000
020002000
000000000
000000040
000000000
000000000
000000040
000000000
```

**Train 1 — output**

```text
000000000
022222000
000000000
000000040
000000040
000000040
000000040
000000000
```

**Train 2 — input**

```text
0030000030
0000000000
0000060000
0000000000
0000000000
0000060000
0700700000
```

**Train 2 — output**

```text
0033333330
0000000000
0000060000
0000060000
0000060000
0000060000
0777700000
```

**Train 3 — input**

```text
000000000
000000000
800000800
000000000
000050000
000000000
000000000
000050000
000000000
```

**Train 3 — output**

```text
000000000
000000000
888888800
000000000
000050000
000050000
000050000
000050000
000000000
```

**Train 4 — input**

```text
00000000
00000090
00000000
00000000
00000000
00000090
02000200
00000000
```

**Train 4 — output**

```text
00000000
00000090
00000090
00000090
00000090
00000090
02222200
00000000
```

**Test — input**

```text
0400000400
0000000000
0000000060
0000000000
0000000000
0000000000
0030030000
0000000060
0000000000
```

**Test — output**

```text
0444444400
0000000000
0000000060
0000000060
0000000060
0000000060
0033330060
0000000060
0000000000
```

**Written solution**

For each color, find its two endpoints. If they are aligned horizontally or vertically, fill every cell between them with that color.

**Reference program**

```python
def rule_e51(g):
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

### E52 — Left Header Row Flood

**Difficulty:** easy

**Train pairs:** 4

**Skills:** row guide, constant fill, same-size transform

**Suggested staged path:** Treat the first column as instructions. Each nonzero header controls its entire row.

**Train 1 — input**

```text
00000000
20000000
00000000
00000000
50000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
22222222
00000000
00000000
55555555
00000000
00000000
```

**Train 2 — input**

```text
6000000
0000000
0000000
4000000
0000000
0000000
9000000
0000000
```

**Train 2 — output**

```text
6666666
0000000
0000000
4444444
0000000
0000000
9999999
0000000
```

**Train 3 — input**

```text
000000000
000000000
300000000
000000000
000000000
700000000
```

**Train 3 — output**

```text
000000000
000000000
333333333
000000000
000000000
777777777
```

**Train 4 — input**

```text
000000
800000
000000
000000
000000
000000
000000
200000
000000
```

**Train 4 — output**

```text
000000
888888
000000
000000
000000
000000
000000
222222
000000
```

**Test — input**

```text
40000000
00000000
00000000
70000000
00000000
00000000
20000000
00000000
```

**Test — output**

```text
44444444
00000000
00000000
77777777
00000000
00000000
22222222
00000000
```

**Written solution**

Whenever the first cell of a row is nonzero, flood that whole row with the same color. Leave rows with a zero header empty.

**Reference program**

```python
def rule_e52(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        color=g[r][0]
        if color!=0:
            for c in range(w):
                out[r][c]=color
    return out
```

### E53 — Row Pack Left

**Difficulty:** easy

**Train pairs:** 4

**Skills:** compression, order preservation, row-wise transform

**Suggested staged path:** Work one row at a time. Keep the order of the colored cells, but remove the zeros between them.

**Train 1 — input**

```text
000000000
040002000
000000000
001080060
000000000
000000003
000000000
```

**Train 1 — output**

```text
000000000
420000000
000000000
186000000
000000000
300000000
000000000
```

**Train 2 — input**

```text
00200090
00000000
00040005
00000000
00000700
00000000
```

**Train 2 — output**

```text
29000000
00000000
45000000
00000000
70000000
00000000
```

**Train 3 — input**

```text
0000000000
0600600003
0000000000
0000000000
0000000000
8000000020
0000001000
0000000000
```

**Train 3 — output**

```text
0000000000
6630000000
0000000000
0000000000
0000000000
8200000000
1000000000
0000000000
```

**Train 4 — input**

```text
0000000
0000000
0090040
0000000
0500005
0000000
0000000
```

**Train 4 — output**

```text
0000000
0000000
9400000
0000000
5500000
0000000
0000000
```

**Test — input**

```text
000300020
000000000
010000008
000000000
000000000
700000400
000000000
000000000
```

**Test — output**

```text
320000000
000000000
180000000
000000000
000000000
740000000
000000000
000000000
```

**Written solution**

For each row, read the nonzero cells from left to right and rewrite them flush against the left edge, padding the rest with zeros.

**Reference program**

```python
def rule_e53(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        for c,v in enumerate(vals):
            out[r][c]=v
    return out
```

### E54 — Diagonal-Corner Rectangle Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rectangle inference, corner pairing, solid fill

**Suggested staged path:** The colored cells are not separate objects; they are opposite corners of hidden rectangles.

**Train 1 — input**

```text
000000000
020000000
000000000
000020000
000000500
000000000
000000005
000000000
```

**Train 1 — output**

```text
000000000
022220000
022220000
022220000
000000555
000000555
000000555
000000000
```

**Train 2 — input**

```text
3000000000
0000000000
0030000000
0000000000
0000000000
0000700000
0000000000
0000000000
0000000700
```

**Train 2 — output**

```text
3330000000
3330000000
3330000000
0000000000
0000000000
0000777700
0000777700
0000777700
0000777700
```

**Train 3 — input**

```text
00000000
00000900
04000000
00000000
00000009
00040000
00000000
```

**Train 3 — output**

```text
00000000
00000999
04440999
04440999
04440999
04440000
00000000
```

**Train 4 — input**

```text
00060000
00000000
00000000
00000060
80000000
00000000
00000000
00800000
```

**Train 4 — output**

```text
00066660
00066660
00066660
00066660
88800000
88800000
88800000
88800000
```

**Test — input**

```text
000000000
020000000
000000000
000000000
000002000
000000700
000000000
000000000
000000007
```

**Test — output**

```text
000000000
022222000
022222000
022222000
022222000
000000777
000000777
000000777
000000777
```

**Written solution**

Group cells by color. Each color gives two diagonal corners of a rectangle. Fill the whole rectangle with that color.

**Reference program**

```python
def rule_e54(g):
    h,w=size(g)
    out=blank(h,w)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        rr=sorted([r1,r2]); cc=sorted([c1,c2])
        fill_rect(out, rr[0], cc[0], rr[1], cc[1], color)
    return out
```

### E55 — Tight Bounding Crop

**Difficulty:** easy

**Train pairs:** 4

**Skills:** cropping, bounding box, shape isolation

**Suggested staged path:** Do not change the pattern. Just isolate it as tightly as possible.

**Train 1 — input**

```text
0000000000
0000000000
0000220000
0000022000
0000002000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
220
022
002
```

**Train 2 — input**

```text
000000000
000000000
000000000
000000000
030300000
003300000
000300000
000000000
000000000
```

**Train 2 — output**

```text
303
033
003
```

**Train 3 — input**

```text
00000000000
00000044000
00000044400
00000004000
00000000000
00000000000
00000000000
```

**Train 3 — output**

```text
440
444
040
```

**Train 4 — input**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0022000000
0002200000
0000200000
0000000000
0000000000
```

**Train 4 — output**

```text
220
022
002
```

**Test — input**

```text
000000000000
000000000000
000000030300
000000003300
000000000300
000000000000
000000000000
000000000000
000000000000
```

**Test — output**

```text
303
033
003
```

**Written solution**

Find the minimal bounding box that contains all nonzero cells and return that crop unchanged.

**Reference program**

```python
def rule_e55(g):
    return crop_nonzero(g)
```

### E56 — Singleton Multiset Strip

**Difficulty:** easy

**Train pairs:** 4

**Skills:** counting, sorting by color, dynamic output

**Suggested staged path:** Ignore the positions of the dots. Only their colors and counts matter.

**Train 1 — input**

```text
00000000
02000000
00000200
00000000
00004000
00000000
70000000
```

**Train 1 — output**

```text
2247
```

**Train 2 — input**

```text
000300000
000000000
000000000
000000050
000000000
050000000
000000800
000000000
```

**Train 2 — output**

```text
3558
```

**Train 3 — input**

```text
0000090000
0000000001
0040000000
0000004000
0000000000
4000000000
```

**Train 3 — output**

```text
14449
```

**Train 4 — input**

```text
0000000
0000000
0600000
0000000
0000060
0000000
0002000
0000000
0000000
```

**Train 4 — output**

```text
266
```

**Test — input**

```text
00000000
03000000
00000030
00001000
00000000
00700000
00000000
00000007
```

**Test — output**

```text
13377
```

**Written solution**

Count how many times each nonzero color appears. Output a single row where colors are listed in ascending order, repeated by their counts.

**Reference program**

```python
def rule_e56(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    row=[]
    for color in sorted(counts):
        row.extend([color]*counts[color])
    return [row] if row else [[0]]
```

## Medium (7)

### M50 — Mirror Target Color Across Guide

**Difficulty:** medium

**Train pairs:** 4

**Skills:** selector cell, reflection, guide line

**Suggested staged path:** The guide line matters, but only one color reacts to it. Use the top-left selector before reflecting.

**Train 1 — input**

```text
2000050000
0200050070
0020050000
0200050000
0000050000
0000050400
0000050000
0000050000
```

**Train 1 — output**

```text
2000050000
0200050072
0020050020
0200050002
0000050000
0000050400
0000050000
0000050000
```

**Train 2 — input**

```text
600000000
006000000
006600000
000000000
555555555
000000000
050000000
000000300
000000000
```

**Train 2 — output**

```text
600000000
006000000
006600000
000000000
555555555
000000000
056600000
006000300
000000000
```

**Train 3 — input**

```text
40000050000
00000050000
04000050080
04000050000
00400050000
00000050300
00000050000
00000050000
```

**Train 3 — output**

```text
40000050000
00000050000
04000050080
04000050000
00400050004
00000050300
00000050000
00000050000
```

**Train 4 — input**

```text
7000000000
0000700000
0000770000
0000000000
0000000000
0000000000
5555555555
0600000000
0000000020
0000000000
```

**Train 4 — output**

```text
7000000000
0000700000
0000770000
0000000000
0000000000
0000000000
5555555555
0600000000
0000000020
0000000000
```

**Test — input**

```text
30000005000
00000005060
03000005000
00300005000
03000005000
00000005000
00000005000
00000005400
00000005000
```

**Test — output**

```text
30000005000
00000005060
03000005000
00300005000
03000005000
00000005000
00000005000
00000005400
00000005000
```

**Written solution**

Read the target color from the top-left cell. Keep the whole grid, and reflect only cells of that color across the 5-colored guide line.

**Reference program**

```python
def rule_m50(g):
    target=g[0][0]
    rows, cols = find_full_guides(g, 5)
    out=clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and (r,c)!=(0,0)]
    if cols:
        out=reflect_across_guide(out, cells, 'v', cols[0], keep_original=True)
    elif rows:
        out=reflect_across_guide(out, cells, 'h', rows[0], keep_original=True)
    return out
```

### M51 — Column Packing Inside Frame

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame reasoning, column-wise packing, order preservation

**Suggested staged path:** Solve the frame first, then handle each interior column independently.

**Train 1 — input**

```text
0000000000
0888888880
0820000080
0800600080
0800000080
0840100080
0830007080
0888888880
0000000000
```

**Train 1 — output**

```text
0000000000
0888888880
0820607080
0840100080
0830000080
0800000080
0800000080
0888888880
0000000000
```

**Train 2 — input**

```text
000000000
008888880
008500080
008009080
008500380
008200080
008888880
000000000
```

**Train 2 — output**

```text
000000000
008888880
008509380
008500080
008200080
008000080
008888880
000000000
```

**Train 3 — input**

```text
0000000000
0000000000
0888888880
0890007080
0800000080
0800200080
0800200080
0840000080
0888888880
0000000000
```

**Train 3 — output**

```text
0000000000
0000000000
0888888880
0890207080
0840200080
0800000080
0800000080
0800000080
0888888880
0000000000
```

**Train 4 — input**

```text
00000000000
08888888880
08060002080
08000000080
08000400080
08010000080
08070005080
08888888880
00000000000
```

**Train 4 — output**

```text
00000000000
08888888880
08060402080
08010005080
08070000080
08000000080
08000000080
08888888880
00000000000
```

**Test — input**

```text
0000000000
0088888800
0087000800
0080009800
0080010800
0080000800
0084000800
0080010800
0088888800
0000000000
```

**Test — output**

```text
0000000000
0088888800
0087019800
0084010800
0080000800
0080000800
0080000800
0080000800
0088888800
0000000000
```

**Written solution**

Keep the rectangular frame. Inside it, compress each column upward so the nonzero cells stack from the top of the interior while preserving top-to-bottom order.

**Reference program**

```python
def rule_m51(g):
    h,w=size(g)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frame=(color,cells)
            break
    if frame is None:
        return g
    fcolor,cells=frame
    r0,c0,r1,c1=bbox(cells)
    out=blank(h,w)
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    for c in range(c0+1,c1):
        vals=[g[r][c] for r in range(r0+1,r1) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[r0+1+i][c]=v
    return out
```

### M52 — Periodic Tile Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** motif extraction, tiling, periodicity

**Suggested staged path:** First crop the seed motif in the corner. Then repeat it over the whole canvas.

**Train 1 — input**

```text
120000000
012000000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
120120120
012012012
120120120
012012012
120120120
012012012
120120120
012012012
```

**Train 2 — input**

```text
330000000
303000000
033000000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
330330330
303303303
033033033
330330330
303303303
033033033
330330330
303303303
033033033
```

**Train 3 — input**

```text
4500000000
0450000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
4504504504
0450450450
4504504504
0450450450
4504504504
0450450450
4504504504
0450450450
```

**Train 4 — input**

```text
120000000000
012000000000
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
120120120120
012012012012
120120120120
012012012012
120120120120
012012012012
120120120120
012012012012
120120120120
012012012012
```

**Test — input**

```text
330000000000
303000000000
033000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Test — output**

```text
330330330330
303303303303
033033033033
330330330330
303303303303
033033033033
330330330330
303303303303
033033033033
```

**Written solution**

Crop the nonzero motif in the corner and tile that exact pattern periodically across the entire output grid.

**Reference program**

```python
def rule_m52(g):
    motif=crop_nonzero(g)
    mh,mw=size(motif)
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=motif[r%mh][c%mw]
    return out
```

### M53 — Command Rotate Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command decoding, rotation, cropping

**Suggested staged path:** Separate the command cell from the object. The command tells you how to rotate the cropped object.

**Train 1 — input**

```text
2000000000
0000000000
0000000000
0000220000
0000022000
0000002000
0000000000
0000000000
```

**Train 1 — output**

```text
002
022
220
```

**Train 2 — input**

```text
300000000
000000000
000000000
000000000
030300000
003300000
000300000
000000000
000000000
```

**Train 2 — output**

```text
300
330
303
```

**Train 3 — input**

```text
40000000000
00000000000
00000044000
00000044400
00000004000
00000000000
00000000000
00000000000
```

**Train 3 — output**

```text
040
444
440
```

**Train 4 — input**

```text
1000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000303000
0000033000
0000003000
0000000000
```

**Train 4 — output**

```text
303
033
003
```

**Test — input**

```text
200000000000
000000000000
000000000000
000000000000
000000044000
000000044400
000000004000
000000000000
000000000000
```

**Test — output**

```text
044
444
040
```

**Written solution**

Ignore the command cell at the top-left, crop the remaining nonzero object, and rotate it according to the command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.

**Reference program**

```python
def rule_m53(g):
    cmd=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    return transform_by_code(obj, cmd)
```

### M54 — Masked Submatrix Extraction

**Difficulty:** medium

**Train pairs:** 4

**Skills:** row/column selection, matrix slicing, dynamic output

**Suggested staged path:** The top row selects columns and the left column selects rows. The answer is the intersection.

**Train 1 — input**

```text
00808
81234
05678
89123
04567
```

**Train 1 — output**

```text
24
13
```

**Train 2 — input**

```text
08080
02468
81357
08642
87531
81111
```

**Train 2 — output**

```text
15
73
11
```

**Train 3 — input**

```text
008808
812345
867891
023456
878912
```

**Train 3 — output**

```text
235
781
892
```

**Train 4 — input**

```text
08808
09876
05432
81098
07654
```

**Train 4 — output**

```text
108
```

**Test — input**

```text
080808
832145
065432
878987
811223
```

**Test — output**

```text
315
797
123
```

**Written solution**

Take the interior matrix. Keep only the rows marked by 8 in the first column and only the columns marked by 8 in the top row, preserving order.

**Reference program**

```python
def rule_m54(g):
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    out=[]
    for r in rows:
        out.append([g[r][c] for c in cols])
    return out if out else [[0]]
```

### M55 — Area-Sorted Rectangle Strip

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component sorting, cropping, layout

**Suggested staged path:** Split the rectangles first. Then sort them by area before laying them out.

**Train 1 — input**

```text
00000000000000
03300000000000
03300000007700
00000000007700
00000555507700
00000555507700
00000555500000
00000000000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
3307705555
3307705555
0007705555
0007700000
```

**Train 2 — input**

```text
0000000000000
0222000000000
0222000004400
0222000004400
0000000004400
0066666004400
0000000004400
0000000000000
0000000000000
```

**Train 2 — output**

```text
666660222044
000000222044
000000222044
000000000044
000000000044
```

**Train 3 — input**

```text
000000000000000
000000000005550
088000000000000
088000000000000
088000000000000
000000000000000
000033333000000
000033333000000
000033333000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
555088033333
000088033333
000088033333
```

**Train 4 — input**

```text
00000000000000
00999900000000
00000000000000
00000000440000
00000000440000
07770000440000
07770000440000
07770000000000
00000000000000
```

**Train 4 — output**

```text
99990440777
00000440777
00000440777
00000440000
```

**Test — input**

```text
000000000000000
000000006600000
022200006600000
022200006600000
022200006600000
000000006600000
000000000004444
000000000004444
000000000000000
000000000000000
```

**Test — output**

```text
44440222066
44440222066
00000222066
00000000066
00000000066
```

**Written solution**

Extract the disconnected solid rectangles, crop each one tightly, sort them by area ascending, and place the crops left to right with one zero column between them.

**Reference program**

```python
def rule_m55(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        crop=grid_from_component(g,cells)
        h,w=size(crop)
        comps.append((len(cells), color, crop, h, w))
    comps.sort(key=lambda t:(t[0], t[1]))
    H=max(h for _,_,_,h,_ in comps)
    W=sum(w for *_,w in comps)+max(0,len(comps)-1)
    out=blank(H,W)
    c0=0
    for _,_,crop,h,w in comps:
        for r in range(h):
            for c in range(w):
                if crop[r][c]!=0:
                    out[r][c0+c]=crop[r][c]
        c0+=w+1
    return out
```

### M56 — Colorized Template Transfer

**Difficulty:** medium

**Train pairs:** 4

**Skills:** template extraction, recoloring, component classification

**Suggested staged path:** Decide which object is the color source and which object is the template mask.

**Train 1 — input**

```text
00000000000
00000000000
02200000000
00220000000
00200007700
00000007700
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
770
077
070
```

**Train 2 — input**

```text
000000000000
000000004440
000000004440
000000000000
000000000000
003300000000
003330000000
000030000000
000000000000
000000000000
```

**Train 2 — output**

```text
440
444
004
```

**Train 3 — input**

```text
0000000000000
0000000000000
0440400000000
0004400000000
0000400000000
0000000006600
0000000006600
0000000006600
0000000000000
```

**Train 3 — output**

```text
06
66
06
```

**Train 4 — input**

```text
000000000000
000000000000
000000033000
000000033000
000000033000
000000000000
022000000000
002200000000
002000000000
000000000000
000000000000
```

**Train 4 — output**

```text
330
033
030
```

**Test — input**

```text
0000000000000
0000000000000
0000000000000
0033000000000
0033300000000
0000300000000
0000000008880
0000000008880
0000000000000
0000000000000
```

**Test — output**

```text
880
888
008
```

**Written solution**

One component is a solid rectangle that supplies the target color; the other is the template shape. Crop the template and recolor every nonzero cell with the rectangle’s color.

**Reference program**

```python
def rule_m56(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    rect=None
    shape=None
    for color,cells in comps:
        if is_solid_rect_component(cells):
            rect=(color,cells)
        else:
            shape=(color,cells)
    if rect is None or shape is None:
        return [[0]]
    target_color=rect[0]
    _,cells=shape
    out=grid_from_component(g,cells,recolor=target_color)
    return out
```

## Hard (7)

### H50 — Quadrant Mirror From Dual Guides

**Difficulty:** hard

**Train pairs:** 4

**Skills:** dual-axis symmetry, guide detection, composed reflection

**Suggested staged path:** Find both guides before moving anything. Then use the same object to generate all reflected copies.

**Train 1 — input**

```text
0000005000000
0120005000000
0102005000000
0222005000000
0000005000000
6666665666666
0000005000000
0000005000000
0000005000000
0000005000000
0000005000000
```

**Train 1 — output**

```text
0000005000000
0120005000210
0102005002010
0222005002220
0000005000000
6666665666666
0000005000000
0222005002220
0102005002010
0120005000210
0000005000000
```

**Train 2 — input**

```text
000000050000
000000053400
000000050340
000000050440
666666656666
000000050000
000000050000
000000050000
000000050000
000000050000
```

**Train 2 — output**

```text
000000050000
000004353400
000043050340
000044050440
666666656666
000044050440
000043050340
000004353400
000000050000
000000050000
```

**Train 3 — input**

```text
00000500000000
00000500000000
00000500000000
00000500000000
00000500000000
00000500000000
66666566666666
07800500000000
07080500000000
08880500000000
00000500000000
00000500000000
```

**Train 3 — output**

```text
00000500000000
00000500000000
00000500000000
08880508880000
07080508070000
07800500870000
66666566666666
07800500870000
07080508070000
08880508880000
00000500000000
00000500000000
```

**Train 4 — input**

```text
00000500000
00000500000
00000500000
00000500000
00000500000
66666566666
00000500000
00000503400
00000500340
00000500440
00000500000
```

**Train 4 — output**

```text
00000500000
04400500440
04300500340
00430503400
00000500000
66666566666
00000500000
00430503400
04300500340
04400500440
00000500000
```

**Test — input**

```text
000000500000
000000501200
000000501020
000000502220
000000500000
000000500000
666666566666
000000500000
000000500000
000000500000
000000500000
000000500000
```

**Test — output**

```text
000000500000
000210501200
002010501020
002220502220
000000500000
000000500000
666666566666
000000500000
000000500000
002220502220
002010501020
000210501200
```

**Written solution**

Detect the full vertical 5-guide and the full horizontal 6-guide. Keep the original object and reflect it across the vertical guide, the horizontal guide, and both guides so it appears in all symmetric quadrants.

**Reference program**

```python
def rule_h50(g):
    h,w=size(g)
    hr=None
    vc=None
    for r in range(h):
        vals=g[r]
        if all(v in (5,6) for v in vals) and vals.count(6)>=w-1:
            hr=r
            break
    for c in range(w):
        vals=[g[r][c] for r in range(h)]
        if all(v in (5,6) for v in vals) and vals.count(5)>=h-1:
            vc=c
            break
    out=clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5,6)]
    out=reflect_across_guide(out, cells, 'v', vc, keep_original=True)
    cells2=[(r,c,v) for r,row in enumerate(out) for c,v in enumerate(row) if v not in (0,5,6)]
    out=reflect_across_guide(out, cells2, 'h', hr, keep_original=True)
    return out
```

### H51 — Bounding-Box Projection Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** relational reasoning, component analysis, dynamic matrix

**Suggested staged path:** Do not compare pixels directly. Compare the row ranges and column ranges of the rectangles.

**Train 1 — input**

```text
00000000000000
02220000000000
02220005500000
02220005500000
00000005500000
00000000000000
00000000000000
00777700000000
00777700000000
00777700000000
00000000000000
00000000000000
```

**Train 1 — output**

```text
312
130
203
```

**Train 2 — input**

```text
0000000000000
0033330004440
0033330004440
0000000004440
0000000000000
0660000888800
0660000888800
0660000888800
0000000888800
0000000000000
0000000000000
```

**Train 2 — output**

```text
3120
1302
2031
0213
```

**Train 3 — input**

```text
099000000000
099000000000
099000000000
000002222000
000002222000
000002222000
777700000000
777700000000
777700000000
000000000000
```

**Train 3 — output**

```text
302
030
203
```

**Train 4 — input**

```text
000000000000000
055550000000000
055550006660000
055550006660000
055550006660000
000000006660000
000000000000000
000333300000000
000333300004440
000333300004440
000000000004440
000000000004440
000000000000000
```

**Train 4 — output**

```text
3120
1300
2031
0013
```

**Test — input**

```text
0000000000000
0880002222000
0880002222000
0880002222000
0000002222000
0000000000000
0077770000000
0077770044400
0077770044400
0000000044400
0000000044400
0000000000000
```

**Test — output**

```text
3120
1302
2031
0213
```

**Written solution**

Extract the solid rectangles in reading order. Build an n×n matrix where each entry is 3 if the two rectangles’ bounding boxes overlap in both rows and columns, 1 if only row ranges overlap, 2 if only column ranges overlap, and 0 if neither overlaps.

**Reference program**

```python
def rule_h51(g):
    rects=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        rects.append((color,cells,bbox(cells)))
    rects.sort(key=lambda t:(t[2][0], t[2][1]))
    n=len(rects)
    out=blank(n,n)
    for i,(_,_,b1) in enumerate(rects):
        for j,(_,_,b2) in enumerate(rects):
            ro=row_overlap(b1,b2)
            co=col_overlap(b1,b2)
            out[i][j]=3 if ro and co else 1 if ro else 2 if co else 0
    return out
```

### H52 — Nested Frame Ownership Fill

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nesting, containment, region ownership

**Suggested staged path:** Think region by region, not frame by frame. Every empty cell belongs to the smallest frame that still contains it.

**Train 1 — input**

```text
00000000000
02222222220
02000000020
02044444020
02040004020
02040004020
02040004020
02044444020
02000000020
02222222220
00000000000
```

**Train 1 — output**

```text
00000000000
02222222220
02222222220
02244444220
02244444220
02244444220
02244444220
02244444220
02222222220
02222222220
00000000000
```

**Train 2 — input**

```text
000000000000
033333333330
030000000030
030666666030
030600006030
030609906030
030609906030
030600006030
030666666030
030000000030
033333333330
000000000000
```

**Train 2 — output**

```text
000000000000
033333333330
033333333330
033666666330
033666666330
033669966330
033669966330
033666666330
033666666330
033333333330
033333333330
000000000000
```

**Train 3 — input**

```text
0000000000000
0055555555500
0050000000500
0050777770500
0050700070500
0050700070500
0050777770500
0050000000500
0055555555500
0000000000000
```

**Train 3 — output**

```text
0000000000000
0055555555500
0055555555500
0055777775500
0055777775500
0055777775500
0055777775500
0055555555500
0055555555500
0000000000000
```

**Train 4 — input**

```text
0000000000000
0888888888880
0800000000080
0800000000080
0800222220080
0800200020080
0800200020080
0800200020080
0800222220080
0800000000080
0800000000080
0888888888880
0000000000000
```

**Train 4 — output**

```text
0000000000000
0888888888880
0888888888880
0888888888880
0888222228880
0888222228880
0888222228880
0888222228880
0888222228880
0888888888880
0888888888880
0888888888880
0000000000000
```

**Test — input**

```text
00000000000000
04444444444440
04000000000040
04077777777040
04070000007040
04070222207040
04070222207040
04070000007040
04077777777040
04000000000040
04444444444440
00000000000000
```

**Test — output**

```text
00000000000000
04444444444440
04444444444440
04477777777440
04477777777440
04477222277440
04477222277440
04477777777440
04477777777440
04444444444440
04444444444440
00000000000000
```

**Written solution**

Keep every rectangular border. Fill each zero cell with the color of the innermost border that contains it.

**Reference program**

```python
def rule_h52(g):
    out=clone(g)
    frames=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            r0,c0,r1,c1=bbox(cells)
            frames.append(((r1-r0+1)*(c1-c0+1), color, (r0,c0,r1,c1)))
    frames.sort()  # innermost first via smallest bbox area
    h,w=size(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]!=0:
                continue
            for _,color,(r0,c0,r1,c1) in frames:
                if r0 < r < r1 and c0 < c < c1:
                    out[r][c]=color
                    break
    return out
```

### H53 — Rank-Selected Transform In Frame

**Difficulty:** hard

**Train pairs:** 4

**Skills:** ranking by area, command transform, centering

**Suggested staged path:** There are three candidate shapes, one rank command, one transform command, and one destination frame.

**Train 1 — input**

```text
1000000000000002
0000000000000000
0022000000000000
0020000000888888
0000000000800008
0330000000800008
0333000000800008
0000440000800008
0000444400800008
0000000000800008
0000000000888888
0000000000000000
```

**Train 1 — output**

```text
888888
800008
800008
802208
800208
800008
800008
888888
```

**Train 2 — input**

```text
20000000000000003
00000000000000000
00440000000000000
00444400000000000
00000000000888888
00000000000800008
02200000000800008
02000000000800008
00003300000800008
00003330000800008
00000000000800008
00000000000888888
00000000000000000
```

**Train 2 — output**

```text
888888
800008
800008
833308
833008
800008
800008
888888
```

**Train 3 — input**

```text
300000000000004
000000000000000
000000000888888
000000000800008
033000000800008
033300000800008
000044000800008
000044440800008
002200000800008
002000000888888
000000000000000
000000000000000
```

**Train 3 — output**

```text
888888
800008
800008
800448
844448
800008
800008
888888
```

**Train 4 — input**

```text
200000000000001
002200000000000
002000000000000
000000000888888
000000000800008
044000000800008
044440000800008
000033000800008
000033300800008
000000000888888
000000000000000
```

**Train 4 — output**

```text
888888
800008
833008
833308
800008
800008
888888
```

**Test — input**

```text
3000000000000002
0000000000000000
0330000000000000
0333000000888888
0000000000800008
0000000000800008
0022000000800008
0020440000800008
0000444400800008
0000000000800008
0000000000888888
0000000000000000
```

**Test — output**

```text
888888
800008
804408
804408
804008
804008
800008
888888
```

**Written solution**

Ignore the two command cells. Rank the non-frame components by area, choose the requested rank, transform it by the second command (1=id, 2=90° clockwise, 3=flip vertically across a horizontal axis, 4=flip horizontally across a vertical axis), and center the result inside the empty frame.

**Reference program**

```python
def rule_h53(g):
    rank_cmd=g[0][0]
    tf_cmd=g[0][-1]
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True, exclude={(0,0),(0,len(g[0])-1)}):
        if is_rect_border(cells):
            frame=(color,cells)
            break
    candidates=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True, exclude={(0,0),(0,len(g[0])-1)}):
        if frame and set(cells)==set(frame[1]):
            continue
        candidates.append((len(cells), color, cells))
    candidates.sort(key=lambda t:(t[0], t[1]))
    idx=min(rank_cmd-1, len(candidates)-1)
    chosen=candidates[idx][2]
    obj=grid_from_component(g, chosen)
    obj=transform_h53(obj, tf_cmd)
    frame_grid=grid_from_component(g, frame[1])
    return center_in_frame(frame_grid, obj)
```

### H54 — Alternating Rotated Tiling

**Difficulty:** hard

**Train pairs:** 4

**Skills:** periodic structure, rotation alternation, checkerboard logic

**Suggested staged path:** Extract the motif once, then tile by blocks rather than by individual cells.

**Train 1 — input**

```text
120000000
012000000
201000000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
120201120
012012012
201120201
201120201
012012012
120201120
120201120
012012012
201120201
```

**Train 2 — input**

```text
330000000000
303000000000
033000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 2 — output**

```text
330033330033
303303303303
033330033330
033330033330
303303303303
330033330033
330033330033
303303303303
033330033330
033330033330
303303303303
330033330033
```

**Train 3 — input**

```text
450000000000
045000000000
504000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
450504450504
045045045045
504450504450
504450504450
045045045045
450504450504
450504450504
045045045045
504450504450
```

**Train 4 — input**

```text
120000000
012000000
201000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 4 — output**

```text
120201120
012012012
201120201
201120201
012012012
120201120
120201120
012012012
201120201
201120201
012012012
120201120
```

**Test — input**

```text
330000000000000
303000000000000
033000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Test — output**

```text
330033330033330
303303303303303
033330033330033
033330033330033
303303303303303
330033330033330
330033330033330
303303303303303
033330033330033
033330033330033
303303303303303
330033330033330
```

**Written solution**

Crop the corner motif, tile it over the whole output, and rotate every odd checkerboard tile 90° clockwise while leaving even tiles unchanged.

**Reference program**

```python
def rule_h54(g):
    motif=crop_nonzero(g)
    n=len(motif)
    rot=rotate_times(motif,1)
    h,w=size(g)
    out=blank(h,w)
    for tr in range(0,h,n):
        for tc in range(0,w,n):
            tile = motif if ((tr//n + tc//n)%2==0) else rot
            for r in range(n):
                for c in range(n):
                    out[tr+r][tc+c]=tile[r][c]
    return out
```

### H55 — Per-Frame Endpoint Routing

**Difficulty:** hard

**Train pairs:** 4

**Skills:** independent subproblems, containment, path tracing

**Suggested staged path:** Treat each frame as its own small puzzle. Connect only the endpoints that live inside the same frame.

**Train 1 — input**

```text
00000000000000
08888800000000
08200800000000
08000800000000
08002800000000
08888800000000
00000008888880
00000008600080
00000008000080
00000008000680
00000008888880
00000000000000
```

**Train 1 — output**

```text
00000000000000
08888800000000
08222800000000
08002800000000
08002800000000
08888800000000
00000008888880
00000008666680
00000008000680
00000008000680
00000008888880
00000000000000
```

**Train 2 — input**

```text
0000000000000
0088888000000
0083008000000
0080038000000
0088888000000
0000000088880
0000000087080
0000000080080
0000000080780
0000000088880
0000000000000
```

**Train 2 — output**

```text
0000000000000
0088888000000
0083338000000
0080038000000
0088888000000
0000000088880
0000000087780
0000000080780
0000000080780
0000000088880
0000000000000
```

**Train 3 — input**

```text
000000000000000
000000000000000
088888000000000
080048000000000
080008000000000
084008000000000
088888000000000
000000008888880
000000008900080
000000008000080
000000008000980
000000008888880
000000000000000
```

**Train 3 — output**

```text
000000000000000
000000000000000
088888000000000
084448000000000
084008000000000
084008000000000
088888000000000
000000008888880
000000008999980
000000008000980
000000008000980
000000008888880
000000000000000
```

**Train 4 — input**

```text
000000000000
088880000000
085080000000
080580000000
088880000000
000000000000
000000888880
000000800280
000000800080
000000820080
000000888880
000000000000
```

**Train 4 — output**

```text
000000000000
088880000000
085580000000
080580000000
088880000000
000000000000
000000888880
000000822280
000000820080
000000820080
000000888880
000000000000
```

**Test — input**

```text
00000000000000
08888880000000
08007080000000
08000080000000
08700080000000
08888880000000
00000000000000
00000008888880
00000008300080
00000008000080
00000008000380
00000008888880
00000000000000
```

**Test — output**

```text
00000000000000
08888880000000
08777080000000
08700080000000
08700080000000
08888880000000
00000000000000
00000008888880
00000008333380
00000008000380
00000008000380
00000008888880
00000000000000
```

**Written solution**

For each rectangular frame, find the two same-colored endpoints inside it and draw a horizontal-then-vertical Manhattan path connecting them with that color, keeping the frame intact.

**Reference program**

```python
def rule_h55(g):
    out=clone(g)
    frames=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frames.append((color,cells,bbox(cells)))
    for fcolor,cells,(r0,c0,r1,c1) in frames:
        inside=collections.defaultdict(list)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v!=0 and v!=fcolor:
                    inside[v].append((r,c))
        for color,pts in inside.items():
            if len(pts)==2:
                for rr,cc in trace_hv(pts[0], pts[1]):
                    out[rr][cc]=color
    return out
```

### H56 — Masked Submatrix Then Rotate

**Difficulty:** hard

**Train pairs:** 4

**Skills:** compositional reasoning, matrix slicing, command transform

**Suggested staged path:** First extract the marked submatrix exactly as in a selection task. Only then apply the command transform.

**Train 1 — input**

```text
20808
81234
05678
89123
04567
```

**Train 1 — output**

```text
12
34
```

**Train 2 — input**

```text
38080
02468
81357
08642
87531
81111
```

**Train 2 — output**

```text
11
37
51
```

**Train 3 — input**

```text
408808
812345
867891
023456
878912
```

**Train 3 — output**

```text
512
389
278
```

**Train 4 — input**

```text
18808
09876
05432
81098
07654
```

**Train 4 — output**

```text
108
```

**Test — input**

```text
380808
832145
065432
878987
811223
```

**Test — output**

```text
321
797
513
```

**Written solution**

Use the first column and top row to select rows and columns from the interior matrix, then rotate the extracted submatrix according to the top-left command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.

**Reference program**

```python
def rule_h56(g):
    cmd=g[0][0]
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    sub=[[g[r][c] for c in cols] for r in rows]
    if not sub:
        sub=[[0]]
    return transform_by_code(sub, cmd)
```
