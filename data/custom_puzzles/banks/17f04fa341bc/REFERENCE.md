# ARC Additional Puzzle Bank — 21 Puzzles (Set 17)

This seventeenth pack continues the numbering with **`E113–E119`**, **`M113–M119`**, and **`H113–H119`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
palette_lift(template, legend, transform=None, symbol_order=None)
```
Intuition: the grid can carry **symbolic** motifs whose values `1/2/3/...` are not final colors but palette channels. A separate legend supplies the actual colors to substitute. The primitive optionally applies a transform first, then recolors the motif by channel. It is used directly in **E113**, **M113**, and **H113**.

Design goals for this set:

- easy: symbolic recoloring, rectangle inference, segment completion, reflection, seeded fills, object ranking, and counting strips

- medium: palette-aware bank assembly, commanded transforms, chamber fills, relational matrices, component ranking, anchor-copy overlays, and panel selection

- hard: per-slot recolored matrix assembly, analogy transforms, Voronoi partitions, nesting depth, transform composition, dihedral-equivalence matrices, and colorized anchor stamping


## E113 — Neutral Glyph Recolor

**Difficulty:** easy


**Train pairs:** 4


**Skills:** palette mapping, symbolic recoloring, crop output


**Suggested staged path:** Ignore the absolute colors in the lower motif. Treat 1/2/3 as abstract channels and substitute the palette from the header row.


**Train 1 — input**

```text
47300
00000
00100
01210
00100
```

**Train 1 — output**

```text
040
474
040
```

**Train 2 — input**

```text
62500
00000
01000
01200
00030
```

**Train 2 — output**

```text
600
620
005
```

**Train 3 — input**

```text
84100
00000
01000
02100
03210
```

**Train 3 — output**

```text
800
480
148
```

**Train 4 — input**

```text
73900
00000
01010
01210
00030
```

**Train 4 — output**

```text
707
737
009
```

**Test — input**

```text
26400
00000
01100
00230
00030
```

**Test — output**

```text
220
064
004
```

**Written solution**

The top row is a legend. Read its nonzero colors from left to right. The lower 3×3 motif is symbolic: replace every 1 with the first legend color, every 2 with the second, and every 3 with the third, then output only that recolored motif.


**Reference program**

```python
def rule_e113(g):
    legend = [v for v in g[0] if v != 0]
    template = [row[1:4] for row in g[2:5]]
    return palette_lift(template, legend)
```

## E114 — Diagonal Corners to Rectangle

**Difficulty:** easy


**Train pairs:** 4


**Skills:** rectangle inference, same-size drawing, corner detection


**Suggested staged path:** Only two nonzero cells matter. Use them as opposite corners of one axis-aligned rectangle.


**Train 1 — input**

```text
00000000
04000000
00000000
00000000
00000000
00000040
00000000
```

**Train 1 — output**

```text
00000000
04444440
04000040
04000040
04000040
04444440
00000000
```

**Train 2 — input**

```text
003000000
000000000
000000000
000000000
000000030
000000000
```

**Train 2 — output**

```text
003333330
003000030
003000030
003000030
003333330
000000000
```

**Train 3 — input**

```text
00000000
00000000
60000000
00000000
00000000
00000000
00000000
00000600
```

**Train 3 — output**

```text
00000000
00000000
66666600
60000600
60000600
60000600
60000600
66666600
```

**Train 4 — input**

```text
0000000000
0000200000
0000000000
0000000000
0000000000
0000000000
0000000002
0000000000
0000000000
```

**Train 4 — output**

```text
0000000000
0000222222
0000200002
0000200002
0000200002
0000200002
0000222222
0000000000
0000000000
```

**Test — input**

```text
000000000
007000000
000000000
000000000
000000000
000000070
000000000
```

**Test — output**

```text
000000000
007777770
007000070
007000070
007000070
007777770
000000000
```

**Written solution**

The two colored markers are opposite corners of a rectangle. Draw the full rectangle outline in the same color, spanning the rows and columns between those markers.


**Reference program**

```python
def rule_e114(g):
    cells = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    (r0, c0, color), (r1, c1, _) = cells
    out = blank(*size(g), 0)
    fill_rect_outline(out, min(r0, r1), min(c0, c1), max(r0, r1), max(c0, c1), color)
    return out
```

## E115 — Terminal Run Completion

**Difficulty:** easy


**Train pairs:** 4


**Skills:** segment filling, axis alignment, pair matching


**Suggested staged path:** Look for equal-colored endpoints on a single row or column with only zeroes between them.


**Train 1 — input**

```text
00000040
02000200
00000000
00000000
00000040
00000000
00000000
```

**Train 1 — output**

```text
00000040
02222240
00000040
00000040
00000040
00000000
00000000
```

**Train 2 — input**

```text
000000000
000000000
007070000
000000000
000000000
300000300
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
007770000
000000000
000000000
333333300
000000000
000000000
```

**Train 3 — input**

```text
0000000000
0600000000
0000000000
0000020020
0000000000
0600000000
0000000000
```

**Train 3 — output**

```text
0000000000
0600000000
0600000000
0600022220
0600000000
0600000000
0000000000
```

**Train 4 — input**

```text
000000000
400400000
000000050
000000000
000000000
000000000
000000050
000030003
000000000
```

**Train 4 — output**

```text
000000000
444400000
000000050
000000050
000000050
000000050
000000050
000033333
000000000
```

**Test — input**

```text
0000000000
0000000030
0600000600
0000000000
0000000000
0000000030
0000000000
0000000000
```

**Test — output**

```text
0000000000
0000000030
0666666630
0000000030
0000000030
0000000030
0000000000
0000000000
```

**Written solution**

Whenever two cells of the same color lie on the same row or the same column and the cells in between are empty, fill the entire straight segment between them in that color.


**Reference program**

```python
def rule_e115(g):
    out = clone(g)
    h, w = size(g)
    for r in range(h):
        positions = defaultdict(list)
        for c, v in enumerate(g[r]):
            if v != 0:
                positions[v].append(c)
        for color, cols in positions.items():
            if len(cols) == 2:
                c1, c2 = sorted(cols)
                if all(g[r][c] == 0 for c in range(c1 + 1, c2)):
                    for c in range(c1, c2 + 1):
                        out[r][c] = color
    for c in range(w):
        positions = defaultdict(list)
        for r in range(h):
            v = g[r][c]
            if v != 0:
                positions[v].append(r)
        for color, rows in positions.items():
            if len(rows) == 2:
                r1, r2 = sorted(rows)
                if all(g[r][c] == 0 for r in range(r1 + 1, r2)):
                    for r in range(r1, r2 + 1):
                        out[r][c] = color
    return out
```

## E116 — Mirror Across the Guide

**Difficulty:** easy


**Train pairs:** 4


**Skills:** reflection, guide detection, same-size copying


**Suggested staged path:** The solid 8-column is the mirror. Copy the colored object across it.


**Train 1 — input**

```text
000080000
000080000
030080000
030080000
033380000
000080000
000080000
000080000
```

**Train 1 — output**

```text
000080000
000080000
030080030
030080030
033383330
000080000
000080000
000080000
```

**Train 2 — input**

```text
00000800000
00000800000
00000800000
00000804400
00000804400
00000804000
00000800000
00000800000
00000800000
```

**Train 2 — output**

```text
00000800000
00000800000
00000800000
00440804400
00440804400
00040804000
00000800000
00000800000
00000800000
```

**Train 3 — input**

```text
0000080000
0222080000
0020080000
0020080000
0000080000
0000080000
0000080000
0000080000
```

**Train 3 — output**

```text
0000080000
0222080222
0020080020
0020080020
0000080000
0000080000
0000080000
0000080000
```

**Train 4 — input**

```text
00000800000
00000800000
00000800000
00000800000
00000800660
00000806600
00000806000
00000800000
00000800000
00000800000
```

**Train 4 — output**

```text
00000800000
00000800000
00000800000
00000800000
06600800660
00660806600
00060806000
00000800000
00000800000
00000800000
```

**Test — input**

```text
000080000
000080000
070780000
070780000
077780000
000080000
000080000
000080000
000080000
```

**Test — output**

```text
000080000
000080000
070787070
070787070
077787770
000080000
000080000
000080000
000080000
```

**Written solution**

Find the vertical guide made entirely of color 8. Reflect every nonzero non-guide cell across that guide, keeping the original object and adding its mirror image on the other side.


**Reference program**

```python
def rule_e116(g):
    h, w = size(g)
    guide_col = [c for c in range(w) if all(g[r][c] == 8 for r in range(h))][0]
    out = clone(g)
    for r in range(h):
        for c, v in enumerate(g[r]):
            if v not in (0, 8):
                mc = 2 * guide_col - c
                if 0 <= mc < w:
                    out[r][mc] = v
    return out
```

## E117 — Seeded Interior Fill

**Difficulty:** easy


**Train pairs:** 4


**Skills:** frame detection, region filling, color transfer


**Suggested staged path:** The repeated border color marks the container. The single interior seed gives the fill color.


**Train 1 — input**

```text
000000000
044444440
040000040
040030040
040000040
040000040
044444440
000000000
```

**Train 1 — output**

```text
000000000
044444440
043333340
043333340
043333340
043333340
044444440
000000000
```

**Train 2 — input**

```text
0000000000
0000000000
0066666660
0060000060
0060002060
0060000060
0060000060
0066666660
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0066666660
0062222260
0062222260
0062222260
0062222260
0066666660
0000000000
```

**Train 3 — input**

```text
00000000
00077770
00070070
00075070
00070070
00077770
00000000
```

**Train 3 — output**

```text
00000000
00077770
00075570
00075570
00075570
00077770
00000000
```

**Train 4 — input**

```text
0000000000
0000000000
0333333330
0300000030
0300000030
0300090030
0300000030
0300000030
0333333330
0000000000
```

**Train 4 — output**

```text
0000000000
0000000000
0333333330
0399999930
0399999930
0399999930
0399999930
0399999930
0333333330
0000000000
```

**Test — input**

```text
000000000
005555500
005000500
005000500
005040500
005000500
005000500
005555500
000000000
```

**Test — output**

```text
000000000
005555500
005444500
005444500
005444500
005444500
005444500
005555500
000000000
```

**Written solution**

Identify the rectangular frame. Leave the frame unchanged and fill every empty interior cell with the color of the single non-frame seed cell inside it.


**Reference program**

```python
def rule_e117(g):
    out = clone(g)
    counts = Counter(v for row in g for v in row if v != 0)
    frame_color = max(counts, key=lambda c: counts[c])
    frame_cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == frame_color]
    r0, c0, r1, c1 = bbox(frame_cells)
    seed_color = [v for row in g for v in row if v not in (0, frame_color)][0]
    for r in range(r0 + 1, r1):
        for c in range(c0 + 1, c1):
            if out[r][c] == 0:
                out[r][c] = seed_color
    return out
```

## E118 — Crop the Largest Object

**Difficulty:** easy


**Train pairs:** 4


**Skills:** component analysis, ranking by area, bbox crop


**Suggested staged path:** Ignore background and compare connected components by size first, then by top-left position if needed.


**Train 1 — input**

```text
0000000000
0200000000
0200006600
0222006600
0000046400
0000040400
0000044400
0000000000
0000000000
```

**Train 1 — output**

```text
464
404
444
```

**Train 2 — input**

```text
000000000000
003300000000
000300000000
033300000000
000000000000
000000770000
002220707700
002000777000
002000000000
000000000000
```

**Train 2 — output**

```text
7700
7077
7770
```

**Train 3 — input**

```text
00000000000
00000008800
00000008800
00000008000
05050000000
05050000000
05550003330
00000000300
00000000300
```

**Train 3 — output**

```text
505
505
555
```

**Train 4 — input**

```text
000000000000
000000000000
004400000000
044000000000
040000000000
000000666000
009000606000
009000660000
009990060000
000000000000
```

**Train 4 — output**

```text
666
606
660
060
```

**Test — input**

```text
000000000000
020200000000
020200000000
022200000000
000000000000
000000077000
044000007000
044000777000
040000000000
000000000000
```

**Test — output**

```text
202
202
222
```

**Written solution**

Find all connected colored objects. Choose the largest one by area; if there is a tie, take the uppermost then leftmost. Output the tight crop of that object.


**Reference program**

```python
def rule_e118(g):
    comps = components_color(g)
    scored = []
    for comp in comps:
        area = len(comp["cells"])
        r0, c0, _, _ = bbox(comp["cells"])
        scored.append((-area, r0, c0, comp))
    best = sorted(scored, key=lambda t: t[:3])[0][3]
    return crop_bbox(g, best["cells"])
```

## E119 — Frequency Strip

**Difficulty:** easy


**Train pairs:** 4


**Skills:** counting, sorting, symbolic output


**Suggested staged path:** The output is not spatial. It is a compact count summary.


**Train 1 — input**

```text
0400007
0400000
0020000
2000000
0000002
```

**Train 1 — output**

```text
222447
```

**Train 2 — input**

```text
30000003
00006000
00300000
00000000
08000000
80000300
```

**Train 2 — output**

```text
3333886
```

**Train 3 — input**

```text
000000900
050000050
000050000
000000000
001000000
000000001
```

**Train 3 — output**

```text
555119
```

**Train 4 — input**

```text
2000004
0002000
0000002
0007000
0000000
0000020
4000000
```

**Train 4 — output**

```text
2222447
```

**Test — input**

```text
00600000
00000030
00600000
05000000
00600000
00000003
```

**Test — output**

```text
666335
```

**Written solution**

Count how many times each nonzero color appears. Sort colors by descending count and break ties by smaller color number. Output a single row where each color is repeated exactly its count.


**Reference program**

```python
def rule_e119(g):
    counts = Counter(v for row in g for v in row if v != 0)
    order = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    row = []
    for color, count in order:
        row.extend([color] * count)
    return [row]
```

## M113 — Palette-Lift Strip Assembly

**Difficulty:** medium


**Train pairs:** 4


**Skills:** palette lifting, bank parsing, strip assembly


**Suggested staged path:** Read the palette first, then the selector strip, then the keyed neutral block bank.


**Train 1 — input**

```text
47300000
21300000
00000000
10020030
10012001
21003023
```

**Train 1 — output**

```text
474004
037473
```

**Train 2 — input**

```text
62500000
33120000
00000000
10020030
30010012
21021003
```

**Train 2 — output**

```text
62625060
05052626
```

**Train 3 — input**

```text
84100000
12100000
00000000
10020030
12030001
03021023
```

**Train 3 — output**

```text
841084
014801
```

**Train 4 — input**

```text
73900000
23120000
00000000
10020030
01012030
23003021
```

**Train 4 — output**

```text
73900773
09373909
```

**Test — input**

```text
26400000
13200000
00000000
10020030
10030012
21021003
```

**Test — output**

```text
202640
620462
```

**Written solution**

The first row supplies a three-color palette. The second row is an ordered selector of keyed blocks. The lower bank maps each key to a 2×2 neutral block whose values 1/2/3 are symbolic. Recolor each selected block with the palette, then concatenate the recolored blocks in selector order.


**Reference program**

```python
def rule_m113(g):
    legend = [v for v in g[0] if v != 0]
    selector = [v for v in g[1] if v != 0]
    bank = {}
    c = 0
    while c < len(g[0]):
        if g[3][c] != 0:
            key = g[3][c]
            bank[key] = [row[c:c+2] for row in g[4:6]]
            c += 3
        else:
            c += 1
    blocks = [palette_lift(bank[key], legend) for key in selector]
    return concat_h(blocks, sep=0)
```

## M114 — Commanded Crop Transform

**Difficulty:** medium


**Train pairs:** 4


**Skills:** command decoding, object crop, geometric transforms


**Suggested staged path:** The only thing outside the object is the command cell.


**Train 1 — input**

```text
100000000
000000000
000000000
000023000
000020300
000022200
000000000
000000000
```

**Train 1 — output**

```text
222
203
230
```

**Train 2 — input**

```text
200000000
000000000
000000000
000450000
000440000
000405000
000000000
000000000
```

**Train 2 — output**

```text
504
044
054
```

**Train 3 — input**

```text
300000000
000000000
000006070
000000600
000007600
000000000
000000000
000000000
```

**Train 3 — output**

```text
607
066
700
```

**Train 4 — input**

```text
400000000
000000000
000000000
000000000
002300000
002030000
002220000
000000000
```

**Train 4 — output**

```text
032
302
222
```

**Test — input**

```text
200000000
000000000
000000000
000060700
000006000
000076000
000000000
000000000
```

**Test — output**

```text
067
060
706
```

**Written solution**

Read the command in the top-left cell. Crop the single object from the rest of the grid and apply the corresponding transform: 1=rot90, 2=rot180, 3=rot270, 4=flip horizontally, 5=flip vertically.


**Reference program**

```python
def rule_m114(g):
    cmd = g[0][0]
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0 and not (r == 0 and c == 0)]
    obj = crop_bbox(g, cells)
    return apply_transform(obj, cmd)
```

## M115 — Chamber Majority Flood

**Difficulty:** medium


**Train pairs:** 4


**Skills:** region partitioning, majority vote, wall-aware filling


**Suggested staged path:** The 8-walls divide the board into chambers. Each chamber decides its fill color locally.


**Train 1 — input**

```text
88888888888
82000830008
80200800308
84000806008
88888888888
80700810008
87070805008
80000800108
88888888888
```

**Train 1 — output**

```text
88888888888
82222833338
82222833338
84222836338
88888888888
87777811118
87777815118
87777811118
88888888888
```

**Train 2 — input**

```text
88888888888
84000806008
80400800608
80040820008
88888888888
83000800508
80070805008
80300810008
88888888888
```

**Train 2 — output**

```text
88888888888
84444866668
84444866668
84444826668
88888888888
83333855558
83373855558
83333815558
88888888888
```

**Train 3 — input**

```text
88888888888
80020890008
82000804008
80060800908
88888888888
80300870008
85000800708
80300802008
88888888888
```

**Train 3 — output**

```text
88888888888
82222899998
82222894998
82262899998
88888888888
83333877778
85333877778
83333872778
88888888888
```

**Train 4 — input**

```text
88888888888
80010802008
81000800208
80400860008
88888888888
85000800308
80500890008
80050803008
88888888888
```

**Train 4 — output**

```text
88888888888
81111822228
81111822228
81411862228
88888888888
85555833338
85555893338
85555833338
88888888888
```

**Test — input**

```text
88888888888
86000800408
80600804008
80020870008
88888888888
80300850008
83000800508
80090801008
88888888888
```

**Test — output**

```text
88888888888
86666844448
86666844448
86626874448
88888888888
83333855558
83333855558
83393851558
88888888888
```

**Written solution**

Treat color 8 as walls. Each enclosed chamber contains a few colored seeds. Determine the majority nonzero seed color inside each chamber and fill all empty cells of that chamber with that majority color, keeping walls and original seeds unchanged.


**Reference program**

```python
def rule_m115(g):
    out = clone(g)
    for region in flood_regions_not_wall(g, wall=8):
        colors = [g[r][c] for r, c in region if g[r][c] not in (0, 8)]
        if not colors:
            continue
        majority = sorted(Counter(colors).items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        for r, c in region:
            if out[r][c] == 0:
                out[r][c] = majority
    return out
```

## M116 — Area–Hole Relation Matrix

**Difficulty:** medium


**Train pairs:** 4


**Skills:** panel parsing, shape statistics, relational output


**Suggested staged path:** Each panel gives one object; the output compares every object with every other.


**Train 1 — input**

```text
222030304400
202030304044
222033304440
```

**Train 1 — output**

```text
506
050
605
```

**Train 2 — input**

```text
500066607777
500006007007
555006007007
000000007777
```

**Train 2 — output**

```text
560
650
005
```

**Train 3 — input**

```text
0220044088
0020440088
2220400080
```

**Train 3 — output**

```text
533
356
365
```

**Train 4 — input**

```text
330006660099
303306060009
333006660999
```

**Train 4 — output**

```text
560
650
005
```

**Test — input**

```text
2000440777
2000440707
2220400777
```

**Test — output**

```text
560
650
005
```

**Written solution**

Split the input into three object panels. For each object compute its area and number of holes. Output a 3×3 relation matrix: diagonal cells are 5; use 6 if two objects share both area and hole count, 2 if they share only area, 3 if they share only hole count, and 0 otherwise.


**Reference program**

```python
def rule_m116(g):
    panels = [crop_nonzero(p) for p in panel_split_horizontal(g)]
    info = []
    for p in panels:
        area = shape_area(p)
        holes = count_holes_binary([[1 if v != 0 else 0 for v in row] for row in p])
        info.append((area, holes))
    n = len(info)
    out = blank(n, n, 0)
    for i, (ai, hi) in enumerate(info):
        for j, (aj, hj) in enumerate(info):
            out[i][j] = relation_color(ai, hi, aj, hj, same_self=(i == j))
    return out
```

## M117 — Ranked Component Selection

**Difficulty:** medium


**Train pairs:** 4


**Skills:** component metrics, command routing, crop output


**Suggested staged path:** The command chooses a ranking rule, not a color.


**Train 1 — input**

```text
100000000000
002000000000
002000000000
002220000000
000000404000
066000404000
060660444000
066600000000
000000000000
000000000000
```

**Train 1 — output**

```text
200
200
222
```

**Train 2 — input**

```text
200000000000
000000003300
000000033000
000000030000
055000000000
050550000000
055500007700
000000007700
000000007000
000000000000
```

**Train 2 — output**

```text
5500
5055
5550
```

**Train 3 — input**

```text
3000000000000
0020000000000
0020000000000
0022200000000
0000000044000
0000000004000
0606000444000
0606000000000
0666000000000
0000000000000
```

**Train 3 — output**

```text
606
606
666
```

**Train 4 — input**

```text
400000000000
000000222000
000000020000
000000020000
040000000000
040000077700
044400070700
000000077000
000000007000
000000000000
```

**Train 4 — output**

```text
777
707
770
070
```

**Test — input**

```text
200000000000
033000000000
033000000000
030000000000
000000606000
022200606000
020200666000
022000000000
002000000000
000000000000
```

**Test — output**

```text
222
202
220
020
```

**Written solution**

Ignore the top-left command cell and analyze the remaining colored objects. Command 1 selects the smallest-area component, 2 the largest-area component, 3 the widest component, and 4 the tallest component. Output the tight crop of the selected component.


**Reference program**

```python
def rule_m117(g):
    cmd = g[0][0]
    g2 = clone(g)
    g2[0][0] = 0
    comp = choose_component_by_cmd(components_color(g2), cmd)
    return crop_bbox(g2, comp["cells"])
```

## M118 — Anchor Copies with Overlap

**Difficulty:** medium


**Train pairs:** 4


**Skills:** prototype extraction, relative translation, overlap handling


**Suggested staged path:** There is one full prototype containing an origin 8, and the other 8s are target origins.


**Train 1 — input**

```text
0000000000
0820000000
0220000080
0023000000
0000000000
0000008000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0820000000
0220000082
0023000022
0000000002
0000008200
0000002200
0000000230
0000000000
```

**Train 2 — input**

```text
00000000000
00082000000
00222000000
00030000000
00000000000
00000800000
00000080000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00082000000
00222000000
00030000000
00000000000
00000820000
00002292000
00000922000
00000030000
00000000000
```

**Train 3 — input**

```text
000000000000
000000000000
028000000800
020300000000
023000000000
000000080000
000000000080
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
028000002800
020000002000
023000002300
000000280000
000000200280
000000230200
000000000230
```

**Train 4 — input**

```text
0000000000
0000000800
0000000000
0008200000
0002200000
0000230000
0080000000
0000000000
0000000000
0000000000
```

**Train 4 — output**

```text
0000000000
0000000820
0000000220
0008200023
0002200000
0000230000
0082000000
0022000000
0002300000
0000000000
```

**Test — input**

```text
00000000000
00000000000
00820000800
02220000000
00300000000
00000000000
00000080000
00000000800
00000000000
00000000000
```

**Test — output**

```text
00000000000
00000000000
00820000820
02220002220
00300000300
00000000000
00000082000
00000222820
00000032220
00000000300
```

**Written solution**

Find the connected prototype that contains color 8; that 8 marks the prototype origin. Copy the whole prototype so that its origin lands on every other 8 in the grid as well as on its original location. Overlay all copies in the original canvas. If two copies write different nonzero colors to the same cell, mark the overlap as 9.


**Reference program**

```python
def rule_m118(g):
    template, origin, anchors = find_prototype_and_anchors(g)
    return overlay_template_copies_same_size(template, origin, anchors, size(g), overlap_color=9)
```

## M119 — Select a Panel, Then Transform It

**Difficulty:** medium


**Train pairs:** 4


**Skills:** panel indexing, command decoding, crop and transform


**Suggested staged path:** The first header value chooses which panel; the second chooses how to transform it.


**Train 1 — input**

```text
1100000000
2000404066
2000404066
2220444060
```

**Train 1 — output**

```text
222
200
200
```

**Train 2 — input**

```text
220000000000
333055000077
030050550770
030055500700
```

**Train 2 — output**

```text
0555
5505
0055
```

**Train 3 — input**

```text
34000000000
02208000606
00208000606
22208880666
```

**Train 3 — output**

```text
606
606
666
```

**Train 4 — input**

```text
25000000000
44002207700
44022007077
40020007770
```

**Train 4 — output**

```text
200
220
022
```

**Test — input**

```text
320000000000
666030005500
060030005055
060033305550
```

**Test — output**

```text
0555
5505
0055
```

**Written solution**

Below the header are multiple zero-separated panels. The first header number selects which panel to use (1-based). Crop that panel tightly and apply the transform given by the second header number using the same command code as in the commanded-crop task.


**Reference program**

```python
def rule_m119(g):
    which = g[0][0]
    cmd = g[0][1]
    panels = panel_split_horizontal(g[1:])
    panel = crop_nonzero(panels[which - 1])
    return apply_transform(panel, cmd)
```

## H113 — Palette-Lift Matrix with Commands

**Difficulty:** hard


**Train pairs:** 4


**Skills:** palette lifting, matrix assembly, per-slot transforms


**Suggested staged path:** There are three layers of control: palette, selector matrix, and command matrix.


**Train 1 — input**

```text
47300000000
12000000000
31000000000
01000000000
42000000000
00000000000
10002000300
01001000100
12101200210
01000030321
```

**Train 1 — output**

```text
040044
474070
040300
004040
047474
473040
```

**Train 2 — input**

```text
62500000000
23000000000
12000000000
30000000000
15000000000
00000000000
10002000300
11001010100
02301210120
00300030003
```

**Train 2 — output**

```text
660600
020620
665005
006005
026626
550606
```

**Train 3 — input**

```text
84100000000
31000000000
23000000000
24000000000
01000000000
00000000000
10002000300
10000100110
21001210023
32100100003
```

**Train 3 — output**

```text
100008
140084
088841
080008
848048
080110
```

**Train 4 — input**

```text
73900000000
13000000000
21000000000
52000000000
10000000000
00000000000
10002000300
10101000010
12101200121
00300030010
```

**Train 4 — output**

```text
009070
737737
707070
077707
030737
900009
```

**Test — input**

```text
26400000000
21000000000
32000000000
04000000000
31000000000
00000000000
10002000300
11001000101
02302100121
00303210003
```

**Test — output**

```text
200022
620460
462400
220462
060620
224200
```

**Written solution**

The top row is a three-color palette. The next 2×2 block chooses which keyed neutral 3×3 template to place in each output slot. The following 2×2 command block tells how to transform each chosen template. Recolor every chosen template with the palette, apply its local transform, and assemble the four resulting 3×3 blocks into a 2×2 output matrix.


**Reference program**

```python
def rule_h113(g):
    legend = [v for v in g[0] if v != 0]
    selector = [[g[1 + r][c] for c in range(2)] for r in range(2)]
    commands = [[g[3 + r][c] for c in range(2)] for r in range(2)]
    bank = {}
    c = 0
    while c < len(g[0]):
        if g[6][c] != 0:
            key = g[6][c]
            bank[key] = [row[c:c+3] for row in g[7:10]]
            c += 4
        else:
            c += 1
    rows = []
    for r in range(2):
        blocks = []
        for c in range(2):
            block = palette_lift(bank[selector[r][c]], legend, transform=commands[r][c])
            blocks.append(block)
        rows.append(concat_h(blocks, sep=0))
    return concat_v(rows, sep=0)
```

## H114 — Panel Analogy Transform

**Difficulty:** hard


**Train pairs:** 4


**Skills:** analogy, transform inference, panel transfer


**Suggested staged path:** Use the first two panels to discover one transform, then reuse it on the third panel.


**Train 1 — input**

```text
20002220404
20002000404
22202000444
```

**Train 1 — output**

```text
444
400
444
```

**Train 2 — input**

```text
330030066
330330006
300330666
```

**Train 2 — output**

```text
666
600
660
```

**Train 3 — input**

```text
05505500700
55000550700
50000050777
```

**Train 3 — output**

```text
777
700
700
```

**Train 4 — input**

```text
2200022200888
2022020220080
2220022000080
```

**Train 4 — output**

```text
080
080
888
```

**Test — input**

```text
30303330066
30303030660
33303030600
```

**Test — output**

```text
006
066
660
```

**Written solution**

The first panel becomes the second by one geometric transform. Infer which transform from the examples among identity, rotations, and flips. Then apply exactly the same transform to the third panel and output the transformed crop.


**Reference program**

```python
def rule_h114(g):
    a, b, c = [crop_nonzero(p) for p in panel_split_horizontal(g)]
    cmd = None
    for _, fn, code in TRANSFORMS:
        if fn(a) == b:
            cmd = code
            break
    return apply_transform(c, cmd)
```

## H115 — Voronoi Frame Fill

**Difficulty:** hard


**Train pairs:** 4


**Skills:** distance reasoning, partitioning, tie handling


**Suggested staged path:** Each empty interior cell belongs to its nearest seed. Ties are special.


**Train 1 — input**

```text
888888888
800000708
802000008
800000008
800000408
800000008
888888888
```

**Train 1 — output**

```text
888888888
822277778
822227778
822254448
822544448
822544448
888888888
```

**Train 2 — input**

```text
88888888
83000008
80000008
80000008
80000008
80000608
80000008
88888888
```

**Train 2 — output**

```text
88888888
83333558
83335668
83356668
83566668
85666668
85666668
88888888
```

**Train 3 — input**

```text
8888888888
8000000008
8000000208
8000000008
8000090008
8000000008
8050000008
8000000008
8888888888
```

**Train 3 — output**

```text
8888888888
8555552228
8555552228
8559995228
8559999558
8555999558
8555599558
8555599558
8888888888
```

**Train 4 — input**

```text
888888888
800000408
800000008
800020008
800000008
807000008
800000008
888888888
```

**Train 4 — output**

```text
888888888
855554448
855225448
855222558
877522558
877755558
877755558
888888888
```

**Test — input**

```text
888888888
800000008
806000308
800000008
800000008
800000008
800070008
800000008
888888888
```

**Test — output**

```text
888888888
866653338
866653338
866653338
866575338
855777558
877777778
877777778
888888888
```

**Written solution**

Inside the 8-frame are several colored seed cells. Fill every empty interior cell with the color of its nearest seed by Manhattan distance. If a cell is equally close to at least two seeds, color it 5 instead.


**Reference program**

```python
def rule_h115(g):
    out = clone(g)
    h, w = size(g)
    seeds = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 8)]
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if g[r][c] == 0:
                dists = sorted((manhattan((r, c), (sr, sc)), color) for sr, sc, color in seeds)
                out[r][c] = 5 if len(dists) > 1 and dists[0][0] == dists[1][0] else dists[0][1]
    return out
```

## H116 — Nested Frame Depth Recolor

**Difficulty:** hard


**Train pairs:** 4


**Skills:** nesting, component ordering, depth mapping


**Suggested staged path:** All input frames start the same color, so depth is the only thing that changes.


**Train 1 — input**

```text
11111111111
10000000001
10111111101
10100000101
10101110101
10101010101
10101110101
10100000101
10111111101
10000000001
11111111111
```

**Train 1 — output**

```text
22222222222
20000000002
20444444402
20400000402
20406660402
20406060402
20406660402
20400000402
20444444402
20000000002
22222222222
```

**Train 2 — input**

```text
0111111111110
0100000000010
0101111111010
0101000001010
0101000001010
0101000001010
0101111111010
0100000000010
0111111111110
```

**Train 2 — output**

```text
0222222222220
0200000000020
0204444444020
0204000004020
0204000004020
0204000004020
0204444444020
0200000000020
0222222222220
```

**Train 3 — input**

```text
1111111111111
1000000000001
1011111111101
1010000000101
1010111110101
1010111110101
1010110110101
1010111110101
1010111110101
1010000000101
1011111111101
1000000000001
1111111111111
```

**Train 3 — output**

```text
2222222222222
2000000000002
2044444444402
2040000000402
2040666660402
2040666660402
2040660660402
2040666660402
2040666660402
2040000000402
2044444444402
2000000000002
2222222222222
```

**Train 4 — input**

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

**Train 4 — output**

```text
000000000000
022222222220
020000000020
020444444020
020400004020
020400004020
020444444020
020000000020
022222222220
000000000000
```

**Test — input**

```text
111111111111
100000000001
101111111101
101000000101
101011110101
101010010101
101010010101
101011110101
101000000101
101111111101
100000000001
111111111111
```

**Test — output**

```text
222222222222
200000000002
204444444402
204000000402
204066660402
204060060402
204060060402
204066660402
204000000402
204444444402
200000000002
222222222222
```

**Written solution**

The input consists of nested rectangular outlines, all in color 1. Order the frames from outermost to innermost by bounding-box area. Recolor them by depth using the fixed palette: depth 1→2, depth 2→4, depth 3→6, depth 4→7, depth 5→3, depth 6→9.


**Reference program**

```python
def rule_h116(g):
    frames = [comp for comp in components_color(g) if comp["color"] == 1]
    scored = []
    for comp in frames:
        r0, c0, r1, c1 = bbox(comp["cells"])
        area = (r1 - r0 + 1) * (c1 - c0 + 1)
        scored.append((-area, r0, c0, comp))
    ordered = [t[3] for t in sorted(scored, key=lambda t: t[:3])]
    out = blank(*size(g), 0)
    for depth, comp in enumerate(ordered):
        color = depth_palette[depth]
        for r, c in comp["cells"]:
            out[r][c] = color
    return out
```

## H117 — Compose Two Commands

**Difficulty:** hard


**Train pairs:** 4


**Skills:** command composition, transform sequencing, crop output


**Suggested staged path:** Do not collapse the header to one code. Apply the first command, then the second.


**Train 1 — input**

```text
140000000
000000000
000000000
000230000
000203000
000222000
000000000
000000000
```

**Train 1 — output**

```text
222
302
032
```

**Train 2 — input**

```text
210000000
000000000
000045000
000044000
000040500
000000000
000000000
000000000
```

**Train 2 — output**

```text
005
540
444
```

**Train 3 — input**

```text
530000000
000000000
000000000
000607000
000060000
000760000
000000000
000000000
```

**Train 3 — output**

```text
706
660
007
```

**Train 4 — input**

```text
420000000
000000000
000000000
000000000
002300000
002030000
002220000
000000000
```

**Train 4 — output**

```text
222
203
230
```

**Test — input**

```text
340000000
000000000
000000000
000450000
000440000
000405000
000000000
000000000
```

**Test — output**

```text
444
045
500
```

**Written solution**

Crop the single object beneath the two-cell header. Interpret the first header number as one transform command and the second as another. Apply the first transform to the cropped object and then apply the second transform to that intermediate result.


**Reference program**

```python
def rule_h117(g):
    cmd1, cmd2 = g[0][0], g[0][1]
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0 and not (r == 0 and c in (0, 1))]
    obj = crop_bbox(g, cells)
    return apply_transform(apply_transform(obj, cmd1), cmd2)
```

## H118 — Transform-Equivalence Matrix

**Difficulty:** hard


**Train pairs:** 4


**Skills:** shape normalization, dihedral equivalence, relational matrix


**Suggested staged path:** Two panels count as equivalent if one shape can be rotated or flipped into the other.


**Train 1 — input**

```text
20004440606
20004000606
22204000666
```

**Train 1 — output**

```text
520
250
005
```

**Train 2 — input**

```text
330550077
330550007
300050777
```

**Train 2 — output**

```text
520
250
005
```

**Train 3 — input**

```text
2200066600444
2022060604404
2220066600044
```

**Train 3 — output**

```text
502
050
205
```

**Train 4 — input**

```text
03300880555
33008800050
30008000050
```

**Train 4 — output**

```text
520
250
005
```

**Test — input**

```text
2020777044
2020707044
2220707040
```

**Test — output**

```text
520
250
005
```

**Written solution**

Split the input into three object panels. Normalize each object up to rotations and reflections. Output a 3×3 matrix whose diagonal is 5 and whose off-diagonal entries are 2 exactly when the two corresponding objects are the same up to dihedral transform; otherwise use 0.


**Reference program**

```python
def rule_h118(g):
    panels = [crop_nonzero(p) for p in panel_split_horizontal(g)]
    canons = [canonicalize_transform_equiv([[1 if v != 0 else 0 for v in row] for row in p]) for p in panels]
    n = len(canons)
    out = blank(n, n, 0)
    for i in range(n):
        for j in range(n):
            out[i][j] = 5 if i == j else (2 if canons[i] == canons[j] else 0)
    return out
```

## H119 — Colorized Anchor Stamp

**Difficulty:** hard


**Train pairs:** 4


**Skills:** prototype extraction, anchor-conditioned recoloring, overlap marking


**Suggested staged path:** The prototype uses 8 only to mark its origin; the external anchor colors tell you what color each copy should become.


**Train 1 — input**

```text
0000000000
0810000000
0110000040
0011000000
0000000000
0000002000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0000000044
0000000044
0000000004
0000002200
0000002200
0000000220
0000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00810000300
01110000000
00100000000
00000000000
00000700000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000330
00000003330
00000000300
00000000000
00000770000
00007770000
00000700000
00000000000
```

**Train 3 — input**

```text
000000000000
008100000000
001010000000
001100000040
000000000000
000000002000
000000000600
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000000044
000000000040
000000002244
000000002660
000000002900
000000000660
000000000000
```

**Train 4 — input**

```text
00000000000
00000000500
00810000000
00110000000
00011000000
00000000000
00000070000
00000000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000550
00000000550
00000000055
00000000000
00000000000
00000077000
00000077000
00000007700
```

**Test — input**

```text
00000000000
00810000000
01110002000
00100000000
00000000000
00000000000
00000400000
00000006000
00000000000
00000000000
```

**Test — output**

```text
00000000000
00000000000
00000002200
00000022200
00000002000
00000000000
00000440000
00004446600
00000466600
00000006000
```

**Written solution**

Extract the prototype component containing an origin cell 8. Convert it to a binary stamp: every nonzero cell of the prototype belongs to the stamp. For every external nonzero anchor cell, place one translated copy of that stamp so the prototype origin lands on the anchor. Color the whole copy with the anchor’s color. When different colored copies overlap, mark those overlap cells as 9.


**Reference program**

```python
def rule_h119(g):
    comps = components_nonzero(g)
    proto_comp = None
    for comp in comps:
        vals = [g[r][c] for r, c in comp["cells"]]
        if 8 in vals and len(comp["cells"]) > 1:
            proto_comp = comp
            break
    r0, c0, r1, c1 = bbox(proto_comp["cells"])
    proto = [row[c0:c1+1] for row in g[r0:r1+1]]
    origin = next((r, c) for r in range(len(proto)) for c in range(len(proto[0])) if proto[r][c] == 8)
    mask = [[1 if v != 0 else 0 for v in row] for row in proto]
    out = blank(*size(g), 0)
    anchors = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v not in (0, 1, 8)]
    for ar, ac, color in anchors:
        top, left = ar - origin[0], ac - origin[1]
        for r in range(len(mask)):
            for c in range(len(mask[0])):
                if mask[r][c]:
                    rr, cc = top + r, left + c
                    if 0 <= rr < len(out) and 0 <= cc < len(out[0]):
                        if out[rr][cc] == 0:
                            out[rr][cc] = color
                        elif out[rr][cc] != color:
                            out[rr][cc] = 9
    return out
```