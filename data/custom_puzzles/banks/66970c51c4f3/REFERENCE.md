# ARC Additional Puzzle Bank — 21 Puzzles (Set 7)

This seventh pack continues the numbering with **`E43–E49`**, **`M43–M49`**, and **`H43–H49`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
trace_polyline_markers(base_grid, marker_groups, mode='hv', intersection_color=None)
```

Intuition: given ordered marker groups, draw Manhattan polylines through them and optionally recolor cells used by multiple groups as intersections. This primitive is used directly in **E49**, **M48**, and **H49**.

Design goals for this set:

- easy: fixed-offset echoes, diagonal midpoint completion, header-driven filling, corner-based rectangle recovery, local denoising, symmetry completion, and simple ordered routing

- medium: selector crops, parity fills, command transforms, legend matrices, object ranking, multi-color routing, and centered template replay

- hard: chained commands, normalized shape algebra, topological recoloring, distance ties, hole-aware ordering, and path-overlap highlighting

## Easy (7)

### E43 — Distance-2 Cross Echo

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local projection, fixed offset, same-color expansion

**Suggested staged path:** Ignore the empty cells first. Ask what new cells each seed paints at a fixed distance.

**Train 1 — input**

```text
000000000
004000000
000000000
000000000
000000000
000000700
000000000
000000000
```

**Train 1 — output**

```text
000000000
404040000
000000000
004000700
000000000
000070707
000000000
000000700
```

**Train 2 — input**

```text
0000000000
0000000020
0000300000
0000000000
0600000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000300000
0000002020
0630303000
0000000020
0606300000
0000000000
0600000000
```

**Train 3 — input**

```text
000050000
000000000
000000000
000000000
000000000
000000000
000000800
000000000
000000000
```

**Train 3 — output**

```text
005050500
000000000
000050000
000000000
000000800
000000000
000080808
000000000
000000800
```

**Train 4 — input**

```text
00000000
00000000
00000000
00090000
00000000
00000000
02000000
00000000
```

**Train 4 — output**

```text
00000000
00090000
00000000
09090900
02000000
00090000
02020000
00000000
```

**Test — input**

```text
0000000000
0000000000
0040000000
0000000000
0000000600
0000000000
0000000000
0000300000
0000000000
```

**Test — output**

```text
0040000000
0000000000
4040400600
0000000000
0040060606
0000300000
0000000600
0030303000
0000000000
```

**Written solution**

Keep every seed. For each nonzero cell, also paint the cells exactly two steps north, south, east, and west with the same color, when those positions stay inside the grid.

**Reference program**

```python
def rule_e43(g):
    h,w=size(g)
    out=clone(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                for dr,dc in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

### E44 — Diagonal Midpoint Fill

**Difficulty:** easy

**Train pairs:** 4

**Skills:** diagonal relation, midpoint inference, same-color completion

**Suggested staged path:** Look for same-colored cells that sit at opposite corners of a 3x3 diagonal. Only one cell is missing.

**Train 1 — input**

```text
00000000
02000050
00000000
00025000
00000000
00000000
00000000
```

**Train 1 — output**

```text
00000000
02000050
00200500
00025000
00000000
00000000
00000000
```

**Train 2 — input**

```text
00000000
00000000
00700000
00000000
00007000
03000000
00000000
00030000
```

**Train 2 — output**

```text
00000000
00000000
00700000
00070000
00007000
03000000
00300000
00030000
```

**Train 3 — input**

```text
006000000
000000000
000060000
000000040
000000000
000004000
080000000
000000000
000800000
```

**Train 3 — output**

```text
006000000
000600000
000060000
000000040
000000400
000004000
080000000
008000000
000800000
```

**Train 4 — input**

```text
0000000000
0000000090
0000000000
0000009000
0010000000
0000000000
0000100000
0000000000
```

**Train 4 — output**

```text
0000000000
0000000090
0000000900
0000009000
0010000000
0001000000
0000100000
0000000000
```

**Test — input**

```text
0000000000
0200000000
0000000050
0002000000
0000005000
0070000000
0000000000
0000700000
0000000000
```

**Test — output**

```text
0000000000
0200000000
0020000050
0002000500
0000005000
0070000000
0007000000
0000700000
0000000000
```

**Written solution**

Whenever two identical colors appear with row and column differences of 2 on a diagonal, fill the midpoint between them with that same color. Keep all existing cells.

**Reference program**

```python
def rule_e44(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0:
                continue
            for dr,dc in [(2,2),(2,-2)]:
                nr,nc=r+dr,c+dc
                mr,mc=r+dr//2,c+dc//2
                if 0<=nr<h and 0<=nc<w and g[nr][nc]==v and out[mr][mc]==0:
                    out[mr][mc]=v
    return out
```

### E45 — Header Column Flood

**Difficulty:** easy

**Train pairs:** 4

**Skills:** row guide, column selection, constant fill

**Suggested staged path:** Only the top row matters. Treat each nonzero header as an instruction for its whole column.

**Train 1 — input**

```text
020050080
000000000
000000000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
020050080
020050080
020050080
020050080
020050080
020050080
020050080
```

**Train 2 — input**

```text
30060090
00000000
00000000
00000000
00000000
00000000
00000000
00000000
```

**Train 2 — output**

```text
30060090
30060090
30060090
30060090
30060090
30060090
30060090
30060090
```

**Train 3 — input**

```text
0040070010
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0040070010
0040070010
0040070010
0040070010
0040070010
0040070010
```

**Train 4 — input**

```text
0800020
0000000
0000000
0000000
0000000
0000000
0000000
0000000
0000000
```

**Train 4 — output**

```text
0800020
0800020
0800020
0800020
0800020
0800020
0800020
0800020
0800020
```

**Test — input**

```text
6000309002
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
6000309002
6000309002
6000309002
6000309002
6000309002
6000309002
6000309002
6000309002
```

**Written solution**

Copy each nonzero cell in the top row straight down through the entire column. All other columns stay zero.

**Reference program**

```python
def rule_e45(g):
    h,w=size(g)
    out=blank(h,w)
    for c,v in enumerate(g[0]):
        if v!=0:
            for r in range(h):
                out[r][c]=v
    return out
```

### E46 — Solid Rectangle From Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** corner detection, rectangle completion, solid fill

**Suggested staged path:** Do not search for lines first; search for four same-colored corners that already define a box.

**Train 1 — input**

```text
0000000000
0200200000
0000000000
0200200000
0000005050
0000000000
0000005050
0000000000
```

**Train 1 — output**

```text
0000000000
0222200000
0222200000
0222200000
0000005550
0000005550
0000005550
0000000000
```

**Train 2 — input**

```text
000004040
000000000
000004040
000000000
080800000
000000000
000000000
080800000
000000000
```

**Train 2 — output**

```text
000004440
000004440
000004440
000000000
088800000
088800000
088800000
088800000
000000000
```

**Train 3 — input**

```text
00000000000
00300300000
00000000000
00000000000
00000000000
00300300000
00000000000
```

**Train 3 — output**

```text
00000000000
00333300000
00333300000
00333300000
00333300000
00333300000
00000000000
```

**Train 4 — input**

```text
0000000000
0000000000
0070700000
0000000000
0070700000
0000006060
0000000000
0000000000
0000006060
0000000000
```

**Train 4 — output**

```text
0000000000
0000000000
0077700000
0077700000
0077700000
0000006660
0000006660
0000006660
0000006660
0000000000
```

**Test — input**

```text
00000000000
02020000000
00000005050
00000000000
02020000000
00000000000
00000005050
00000000000
00000000000
```

**Test — output**

```text
00000000000
02220000000
02220005550
02220005550
02220005550
00000005550
00000005550
00000000000
00000000000
```

**Written solution**

Each color marks the four corners of an axis-aligned rectangle. Fill the full rectangle, including its interior, with that color.

**Reference program**

```python
def rule_e46(g):
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
        corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}
        if set(cells)==corners:
            fill_rect(out,r0,c0,r1,c1,color)
    return out
```

### E47 — Remove Isolated Cells

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local filtering, orthogonal adjacency, noise removal

**Suggested staged path:** Check each colored cell locally. The question is whether it has a same-colored orthogonal friend.

**Train 1 — input**

```text
000000000
022000000
000000040
000050000
000000000
000007700
000000700
000000000
```

**Train 1 — output**

```text
000000000
022000000
000000000
000000000
000000000
000007700
000000700
000000000
```

**Train 2 — input**

```text
3000000000
0000000000
0066000000
0000000000
0000008000
0000008000
0000000001
```

**Train 2 — output**

```text
0000000000
0000000000
0066000000
0000000000
0000008000
0000008000
0000000000
```

**Train 3 — input**

```text
000000000
000090000
000090000
000000000
022200000
000000000
000000000
000000050
000000000
```

**Train 3 — output**

```text
000000000
000090000
000090000
000000000
022200000
000000000
000000000
000000000
000000000
```

**Train 4 — input**

```text
00000000
00000000
04400000
00400000
00000000
00000600
30000000
00000000
```

**Train 4 — output**

```text
00000000
00000000
04400000
00400000
00000000
00000000
00000000
00000000
```

**Test — input**

```text
0000000000
0220000000
0000000050
0000000050
0000000000
0000700000
0000000000
0000000999
0000000000
```

**Test — output**

```text
0000000000
0220000000
0000000050
0000000050
0000000000
0000000000
0000000000
0000000999
0000000000
```

**Written solution**

Keep a nonzero cell only if at least one orthogonally adjacent cell has the same color. Delete isolated singletons.

**Reference program**

```python
def rule_e47(g):
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

### E48 — Anti-Diagonal Mirror Add

**Difficulty:** easy

**Train pairs:** 4

**Skills:** symmetry, anti-diagonal reflection, union

**Suggested staged path:** Treat the anti-diagonal as the fold line. Existing cells stay; reflected cells are only added where blank.

**Train 1 — input**

```text
0200000
0000500
0000000
0000000
0000070
0000000
0000000
```

**Train 1 — output**

```text
0200000
0070500
0000050
0000000
0000070
0000002
0000000
```

**Train 2 — input**

```text
00000000
03000000
00000600
00000000
00000000
00000040
00000000
00000000
```

**Train 2 — output**

```text
00000000
03400000
00000600
00000000
00000000
00000040
00000030
00000000
```

**Train 3 — input**

```text
000000800
000000000
005000000
000000000
000000000
000000000
000200000
000000000
000000000
```

**Train 3 — output**

```text
000000800
000000000
005000008
000000000
000000000
002000000
000200500
000000000
000000000
```

**Train 4 — input**

```text
900000
000400
000000
000000
070000
000000
```

**Train 4 — output**

```text
900000
000400
000040
000000
070000
000009
```

**Test — input**

```text
00200000
00000000
00000050
00000000
00070000
00000000
00000800
00000000
```

**Test — output**

```text
00200000
00000500
08000050
00000000
00070000
00000002
00000800
00000000
```

**Written solution**

Reflect every nonzero cell across the anti-diagonal and add the reflected copy. If a reflected position is already filled, leave it as it is.

**Reference program**

```python
def rule_e48(g):
    h,w=size(g)
    assert h==w
    ref=reflect_anti_diag(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]==0 and ref[r][c]!=0:
                out[r][c]=ref[r][c]
    return out
```

### E49 — Ordered Marker Polyline

**Difficulty:** easy

**Train pairs:** 4

**Skills:** marker order, Manhattan path, polyline tracing

**Suggested staged path:** Sort the markers in reading order and connect them one segment at a time.

**Train 1 — input**

```text
0000000000
0400004000
0000000000
0000000000
0000000000
0000000400
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0444444400
0000000400
0000000400
0000000400
0000000400
0000000000
0000000000
```

**Train 2 — input**

```text
000070000
000000000
000000000
007000000
000000000
000000000
000000700
000000000
000000000
```

**Train 2 — output**

```text
007770000
007000000
007000000
007777700
000000700
000000700
000000700
000000000
000000000
```

**Train 3 — input**

```text
00000000000
00000000200
00000000000
00000000000
02000000000
00000000020
00000000000
```

**Train 3 — output**

```text
00000000000
02222222200
02000000000
02000000000
02222222220
00000000020
00000000000
```

**Train 4 — input**

```text
05000000
00000000
00000000
00000500
00000000
00000000
00500050
00000000
```

**Train 4 — output**

```text
05555500
00000500
00000500
00555500
00500000
00500000
00555550
00000000
```

**Test — input**

```text
0000000000
0080000000
0000000080
0000000000
0000000000
0000000000
0008000000
0000000800
0000000000
```

**Test — output**

```text
0000000000
0088888880
0008888880
0008000000
0008000000
0008000000
0008888800
0000000800
0000000000
```

**Written solution**

Take the markers of the single color, sort them from top to bottom then left to right, and connect consecutive markers with Manhattan segments that go horizontally first and then vertically.

**Reference program**

```python
def rule_e49(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=None)
```

## Medium (7)

### M43 — Selector Crop By Color

**Difficulty:** medium

**Train pairs:** 4

**Skills:** selector cell, component filtering, cropping

**Suggested staged path:** The corner cell is a key, not part of the object. Find everything with that color and crop tightly around it.

**Train 1 — input**

```text
300000000000
000000005550
000330000500
000030000000
000000000000
000000000000
000000300000
000000330000
000000000000
000000000000
```

**Train 1 — output**

```text
33000
03000
00000
00000
00030
00033
```

**Train 2 — input**

```text
60000000000
00000000040
00000660040
00000066040
00000000000
02200000000
02000000000
00000000000
00000000000
```

**Train 2 — output**

```text
660
066
```

**Train 3 — input**

```text
4000000000
0000000707
0000000070
0004400000
0004400000
0000000000
0000004000
0000004400
0000000000
0000000000
```

**Train 3 — output**

```text
44000
44000
00000
00040
00044
```

**Train 4 — input**

```text
500000000000
000000000000
005550000000
000500000000
000000000000
000050008800
000055008800
000000000000
000000000000
```

**Train 4 — output**

```text
5550
0500
0000
0050
0055
```

**Test — input**

```text
200000000000
000000000770
000022000700
000002200000
000000000000
000000000000
000000020000
000000022000
000000000000
000000000000
```

**Test — output**

```text
22000
02200
00000
00000
00020
00022
```

**Written solution**

Read the top-left cell as the selected color. Ignore that selector cell itself, gather every other cell of that color, and crop the smallest rectangle that contains them.

**Reference program**

```python
def rule_m43(g):
    sel=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==sel and not (r==0 and c==0)]
    return crop_bbox(g, cells)
```

### M44 — Checkerboard Interior Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame detection, parity fill, seed colors

**Suggested staged path:** Use the border only to find the playable interior. The two interior seed colors tell you the alternating pattern.

**Train 1 — input**

```text
00000000000
00111111100
00147000100
00100000100
00100000100
00100000100
00100000100
00111111100
00000000000
```

**Train 1 — output**

```text
00000000000
00111111100
00147474100
00174747100
00147474100
00174747100
00147474100
00111111100
00000000000
```

**Train 2 — input**

```text
0555555550
0528000050
0500000050
0500000050
0500000050
0500000050
0555555550
0000000000
```

**Train 2 — output**

```text
0555555550
0528282850
0582828250
0528282850
0582828250
0528282850
0555555550
0000000000
```

**Train 3 — input**

```text
0000000000
0000000000
0033333300
0036900300
0030000300
0030000300
0030000300
0030000300
0033333300
0000000000
```

**Train 3 — output**

```text
0000000000
0000000000
0033333300
0036969300
0039696300
0036969300
0039696300
0036969300
0033333300
0000000000
```

**Train 4 — input**

```text
000000000000
000044444440
000047200040
000040000040
000040000040
000040000040
000040000040
000044444440
000000000000
```

**Train 4 — output**

```text
000000000000
000044444440
000047272740
000042727240
000047272740
000042727240
000047272740
000044444440
000000000000
```

**Test — input**

```text
000000000000
066666666600
063800000600
060000000600
060000000600
060000000600
060000000600
060000000600
066666666600
000000000000
```

**Test — output**

```text
000000000000
066666666600
063838383600
068383838600
063838383600
068383838600
063838383600
068383838600
066666666600
000000000000
```

**Written solution**

Find the hollow rectangular frame. Read the two seed colors inside it and fill the entire interior as a checkerboard anchored so the top-left interior cell matches the left seed.

**Reference program**

```python
def rule_m44(g):
    h,w=size(g)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if len(cells)>=8 and is_rect_border(cells):
            frame=(color,bbox(cells))
            break
    assert frame is not None
    fcolor,(r0,c0,r1,c1)=frame
    interior=sorted((r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]!=0)
    a=interior[0][2]; b=interior[1][2]
    out=blank(h,w)
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            out[r][c]=a if ((r-(r0+1)) + (c-(c0+1)))%2==0 else b
    return out
```

### M45 — Command Rotate Crop

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command decoding, cropping, rotation

**Suggested staged path:** The corner digit is not part of the object. Crop the object first, then rotate it.

**Train 1 — input**

```text
1000000000
0000000000
0000230000
0000233000
0000030000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
230
233
030
```

**Train 2 — input**

```text
200000000
000000000
000000000
004400000
000400000
000440000
000000000
000000000
000000000
```

**Train 2 — output**

```text
004
444
400
```

**Train 3 — input**

```text
30000000000
00000000000
00000056000
00000055600
00000000600
00000000000
00000000000
00000000000
```

**Train 3 — output**

```text
600
655
065
```

**Train 4 — input**

```text
4000000000
0000000000
0000000000
0000000000
0000000000
0002300000
0002330000
0000300000
0000000000
0000000000
```

**Train 4 — output**

```text
030
333
220
```

**Test — input**

```text
20000000000
00000000000
00000000000
00000560000
00000556000
00000006000
00000000000
00000000000
00000000000
```

**Test — output**

```text
055
056
660
```

**Written solution**

Ignore the command cell in the top-left. Crop the remaining nonzero object tightly, then rotate it according to the command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.

**Reference program**

```python
def rule_m45(g):
    cmd=g[0][0]
    base=clone(g); base[0][0]=0
    cropped=crop_nonzero(base)
    return rotate_times(cropped, {1:0,2:1,3:2,4:3}[cmd])
```

### M46 — Border Equality Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** legend decoding, row-column interaction, dynamic output

**Suggested staged path:** Think of the top row as column labels and the first column as row labels. The output only keeps matching pairs.

**Train 1 — input**

```text
072452
200000
500000
700000
200000
```

**Train 1 — output**

```text
02002
00050
70000
02002
```

**Train 2 — input**

```text
01388
30000
80000
30000
```

**Train 2 — output**

```text
0300
0088
0300
```

**Train 3 — input**

```text
062146
600000
400000
600000
100000
```

**Train 3 — output**

```text
60006
00040
60006
00100
```

**Train 4 — input**

```text
029559
900000
500000
200000
900000
```

**Train 4 — output**

```text
09009
00550
20000
09009
```

**Test — input**

```text
074124
400000
700000
400000
200000
```

**Test — output**

```text
04004
70000
04004
00020
```

**Written solution**

Build an output matrix from the first column and first row. At each interior position, write the row label if it equals the column label; otherwise write 0.

**Reference program**

```python
def rule_m46(g):
    h,w=size(g)
    rows=[g[r][0] for r in range(1,h)]
    cols=g[0][1:]
    out=blank(len(rows), len(cols))
    for r,rv in enumerate(rows):
        for c,cv in enumerate(cols):
            out[r][c]=rv if rv==cv else 0
    return out
```

### M47 — Rectangle Strip By Area

**Difficulty:** medium

**Train pairs:** 4

**Skills:** object extraction, area ranking, dynamic layout

**Suggested staged path:** Every object is already a solid rectangle. Crop each one and sort them before arranging them.

**Train 1 — input**

```text
000000000000
033000555000
033000555000
000000555000
000000000000
007700000000
007700000000
007700000000
000000000000
000000000000
```

**Train 1 — output**

```text
330770555
330770555
000770555
```

**Train 2 — input**

```text
0000000000000
0222000000000
0000000000000
0000000880000
0000000880000
0000000880440
0000000000440
0000000000440
0000000000440
```

**Train 2 — output**

```text
222088044
000088044
000088044
000000044
```

**Train 3 — input**

```text
00000000000
00000660000
00000660000
00000660000
00000000000
03333000000
00000000000
00000009990
00000009990
00000009990
00000000000
```

**Train 3 — output**

```text
33330660999
00000660999
00000660999
```

**Train 4 — input**

```text
00000000000000
00000000077700
00555000077700
00555000000000
00555000000000
00000000000000
00000022000000
00000022000000
00000022000000
00000000000000
```

**Train 4 — output**

```text
2207770555
2207770555
2200000555
```

**Test — input**

```text
0000000000000
0440000000000
0440000660000
0000000660000
0000000660000
0000000660000
0009999000000
0009999000000
0009999000000
0000000000000
0000000000000
```

**Test — output**

```text
4406609999
4406609999
0006609999
0006600000
```

**Written solution**

Extract all solid monochrome rectangles, sort them by area ascending (breaking ties by color), and place their cropped rectangles left to right with a one-column gap between consecutive pieces.

**Reference program**

```python
def rule_m47(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_solid_rect_component(cells):
            r0,c0,r1,c1=bbox(cells)
            crop=[row[c0:c1+1] for row in g[r0:r1+1]]
            comps.append((len(cells), color, crop))
    comps.sort(key=lambda x:(x[0], x[1]))
    maxh=max(len(crop) for _,_,crop in comps)
    totalw=sum(len(crop[0]) for _,_,crop in comps)+max(0,len(comps)-1)
    out=blank(maxh,totalw)
    x=0
    for _,_,crop in comps:
        h,w=size(crop)
        for r in range(h):
            for c in range(w):
                out[r][x+c]=crop[r][c]
        x += w+1
    return out
```

### M48 — Multi-Color Ordered Polylines

**Difficulty:** medium

**Train pairs:** 4

**Skills:** per-color grouping, marker order, path tracing

**Suggested staged path:** Solve one color at a time. Each color has its own ordered marker sequence.

**Train 1 — input**

```text
000000000000
020000200000
000000000500
000000000000
000000000000
000000020000
000000000500
000500000000
000000000000
```

**Train 1 — output**

```text
000000000000
022222220000
000000020500
000000020500
000000020500
000000020500
000555555500
000500000000
000000000000
```

**Train 2 — input**

```text
0000300000
0000000070
0000000000
0000000000
0030000000
0000000070
0000000000
0700000000
0000030000
0000000000
```

**Train 2 — output**

```text
0033300000
0030000070
0030000070
0030000070
0033330070
0777737770
0700030000
0700030000
0000030000
0000000000
```

**Train 3 — input**

```text
0000000000080
0040000000000
0000000000000
0000000000400
0000000000000
0000000000080
0000800040000
0000000000000
```

**Train 3 — output**

```text
0000000000080
0044444444480
0000000000480
0000000044480
0000000040080
0000888848880
0000800040000
0000000000000
```

**Train 4 — input**

```text
00000000900
06000000000
00000000000
00000000090
00000060000
00000000000
00000000000
00600000090
00000000000
```

**Train 4 — output**

```text
00000000990
06666660090
00000060090
00000060090
00666660090
00600000090
00600000090
00600000090
00000000000
```

**Test — input**

```text
000000000070
002000000000
000000002000
000000000000
000000000000
000000000070
000000000000
000000002000
000700000000
000000000000
```

**Test — output**

```text
000000000070
002222222070
000000002070
000000002070
000000002070
000777772770
000700002000
000700002000
000700000000
000000000000
```

**Written solution**

For each color separately, sort its markers in reading order and connect consecutive markers with horizontal-then-vertical Manhattan segments. Combine all traced paths.

**Reference program**

```python
def rule_m48(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=None)
```

### M49 — Center Template In Frames

**Difficulty:** medium

**Train pairs:** 4

**Skills:** template extraction, frame detection, centering, recoloring

**Suggested staged path:** Separate the source template from the destination frames. The template is replayed centered inside every frame.

**Train 1 — input**

```text
00000000000000
02200000666660
00200000600060
02220000600060
00000000600060
00000000666660
00000008888800
00000008000800
00000008000800
00000008888800
00000000000000
```

**Train 1 — output**

```text
00000000000000
00000000666660
00000000666060
00000000606060
00000000666660
00000000666660
00000008888800
00000008080800
00000008888800
00000008888800
00000000000000
```

**Train 2 — input**

```text
0000000000000
0000000055550
0022000050050
0020000050050
0022000050050
0000000050050
0000000055550
0000000000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0000000055550
0000000055550
0000000055050
0000000055550
0000000050050
0000000055550
0000000000000
0000000000000
0000000000000
```

**Train 3 — input**

```text
000000000000000
000000000777770
000000000700070
002020000700070
002220000700070
000000000777770
000000004444400
000000004000400
000000004000400
000000004000400
000000004444400
000000000000000
```

**Train 3 — output**

```text
000000000000000
000000000777770
000000000770770
000000000777770
000000000700070
000000000777770
000000004444400
000000004404400
000000004444400
000000004000400
000000004444400
000000000000000
```

**Train 4 — input**

```text
00000000000000
00000000999990
00000000900090
00000000900090
02220000900090
00200000900090
00000000999990
00000003333300
00000003000300
00000003333300
00000000000000
```

**Train 4 — output**

```text
00000000000000
00000000999990
00000000900090
00000000999990
00000000909090
00000000900090
00000000999990
00000003333300
00000003030300
00000003333300
00000000000000
```

**Test — input**

```text
000000000000000
000000000555550
002200000500050
002220000500050
000200000500050
000000000500050
000000000555550
000000007777700
000000007000700
000000007000700
000000007777700
000000000000000
```

**Test — output**

```text
000000000000000
000000000555550
000000000555050
000000000555550
000000000505050
000000000500050
000000000555550
000000007777700
000000007777700
000000007070700
000000007777700
000000000000000
```

**Written solution**

Extract the non-frame shape made of 2s, normalize it to its own bounding box, then place a centered copy inside each hollow frame. Recolor the copied template to the frame’s color and keep the frames.

**Reference program**

```python
def rule_m49(g):
    h,w=size(g)
    source=None
    for comp in components_of_color(g,2):
        if not is_rect_border(comp):
            source=comp
            break
    assert source is not None
    templ=normalize_component(g, cells=[(r,c,2) for r,c in source])
    out=blank(h,w)
    for color in sorted({v for row in g for v in row if v not in (0,2)}):
        for comp in components_of_color(g,color):
            if is_rect_border(comp):
                box=bbox(comp)
                draw_rect_border(out,*box,color)
                out=center_stamp(out, templ, box, recolor='frame')
    return out
```

## Hard (7)

### H43 — Select Rotate And Stamp

**Difficulty:** hard

**Train pairs:** 4

**Skills:** selector command, object extraction, rotation, centering, frame replay

**Suggested staged path:** There are three jobs: select the right source color, transform it, then stamp it into every frame.

**Train 1 — input**

```text
200000000000002
000000000666660
022000000600060
020000000600060
022200000600060
000000000666660
033000008888800
003000008000800
000000008000800
000000008000800
000000008888800
000000000000000
```

**Train 1 — output**

```text
000000000000000
000000000666660
000000000666660
000000000660660
000000000660060
000000000666660
000000008888800
000000008888800
000000008808800
000000008800800
000000008888800
000000000000000
```

**Train 2 — input**

```text
30000000000004
00000000777770
00333000700070
00030000700070
00000000700070
00000000777770
02000000000000
02200000000000
00000000000000
00000000000000
00000000000000
```

**Train 2 — output**

```text
00000000000000
00000000777770
00000000770070
00000000777070
00000000770070
00000000777770
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```

**Train 3 — input**

```text
4000000000000003
0000000000555550
0000000000500050
0040400000500050
0044400000500050
0000000000500050
0000000000555550
0022000009999900
0020000009000900
0000000009000900
0000000009999900
0000000000000000
```

**Train 3 — output**

```text
0000000000000000
0000000000555550
0000000000500050
0000000000555550
0000000000550550
0000000000500050
0000000000555550
0000000009999900
0000000009999900
0000000009909900
0000000009999900
0000000000000000
```

**Train 4 — input**

```text
200000000000001
000000000888880
022000000800080
020000000800080
022000000800080
000000000800080
004440000888880
000400006666600
000000006000600
000000006666600
000000000000000
```

**Train 4 — output**

```text
000000000000000
000000000888880
000000000888080
000000000880080
000000000888080
000000000800080
000000000888880
000000006666600
000000006600600
000000006666600
000000000000000
```

**Test — input**

```text
300000000000002
000000000777770
003300000700070
000330000700070
000000000700070
000000000777770
022000005555500
020000005000500
000000005000500
000000005000500
000000005555500
000000000000000
```

**Test — output**

```text
000000000000000
000000000777770
000000000707070
000000000777070
000000000770070
000000000777770
000000005555500
000000005050500
000000005550500
000000005500500
000000005555500
000000000000000
```

**Written solution**

Use the top-left cell to choose which source component color to keep. Use the top-right command to rotate that selected component. Normalize the rotated component and center a recolored copy inside every hollow frame, using each frame’s color for the copy.

**Reference program**

```python
def rule_h43(g):
    h,w=size(g)
    sel=g[0][0]
    cmd=g[0][-1]
    comps=[comp for comp in components_of_color(g,sel) if (0,0) not in comp]
    sel_comp=max(comps, key=len)
    templ=normalize_component(g, cells=[(r,c,sel) for r,c in sel_comp])
    templ=apply_transform_to_cells(templ, {1:'id',2:'rot90',3:'rot180',4:'rot270'}[cmd])
    out=blank(h,w)
    for color in sorted({v for row in g for v in row if v not in (0,sel,cmd)}):
        for comp in components_of_color(g,color):
            if (0,0) in comp or (0,w-1) in comp:
                continue
            if is_rect_border(comp):
                box=bbox(comp)
                draw_rect_border(out,*box,color)
                out=center_stamp(out, templ, box, recolor='frame')
    return out
```

### H44 — Normalized Shape Intersection

**Difficulty:** hard

**Train pairs:** 4

**Skills:** object normalization, boolean AND, dynamic output

**Suggested staged path:** Ignore absolute placement. Compare the two shapes only after cropping each to its own origin.

**Train 1 — input**

```text
000000000000
022000000000
022200000000
002000000000
000000000000
000000030300
000000033300
000000003000
000000000000
000000000000
```

**Train 1 — output**

```text
800
888
080
```

**Train 2 — input**

```text
00000000000
00000000000
00220000000
00200000000
00220003300
00000000300
00000003300
00000000000
00000000000
```

**Train 2 — output**

```text
88
00
88
```

**Train 3 — input**

```text
0000000000
0000022200
0000002000
0000000000
0000000000
0000000000
0030000000
0333000000
0000000000
0000000000
```

**Train 3 — output**

```text
08
08
```

**Train 4 — input**

```text
000000000000
000000000000
020200000000
022200000000
000000000000
000000000000
000000033300
000000030300
000000000000
000000000000
000000000000
```

**Train 4 — output**

```text
808
808
```

**Test — input**

```text
000000000000
002200000000
002220000000
000200000000
000000000000
000000000000
000000033300
000000030300
000000003000
000000000000
```

**Test — output**

```text
880
808
```

**Written solution**

Crop the 2-shape and the 3-shape to their own bounding boxes and align both at the top-left. Output only the cells occupied in both normalized shapes, colored 8.

**Reference program**

```python
def rule_h44(g):
    comp2=max(components_of_color(g,2), key=len)
    comp3=max(components_of_color(g,3), key=len)
    n2={(r,c) for r,c,_ in normalize_component(g, cells=[(r,c,2) for r,c in comp2])}
    n3={(r,c) for r,c,_ in normalize_component(g, cells=[(r,c,3) for r,c in comp3])}
    pts=sorted(n2 & n3)
    if not pts:
        return [[0]]
    h=max(r for r,c in pts)+1; w=max(c for r,c in pts)+1
    out=blank(h,w)
    for r,c in pts:
        out[r][c]=8
    return out
```

### H45 — Hole-Count Legend Recolor

**Difficulty:** hard

**Train pairs:** 4

**Skills:** topological reasoning, legend mapping, component recoloring

**Suggested staged path:** Read the legend before touching the shapes. Then measure how many enclosed holes each component has.

**Train 1 — input**

```text
2580000000000000
0000000000000000
0700000888000000
0770000808000000
0070000888000000
0000000000000000
0000000009999999
0000000009009009
0000000009009009
0000000009009009
0000000009999999
0000000000000000
```

**Train 1 — output**

```text
2580000000000000
0000000000000000
0200000555000000
0220000505000000
0020000555000000
0000000000000000
0000000008888888
0000000008008008
0000000008008008
0000000008008008
0000000008888888
0000000000000000
```

**Train 2 — input**

```text
369000000000000
000000000000000
008880000000000
008080000070000
008880000077000
000000000007000
000009999999000
000009009009000
000009009009000
000009009009000
000009999999000
```

**Train 2 — output**

```text
369000000000000
000000000000000
006660000000000
006060000090000
006660000099000
000000000009000
000009999999000
000009009009000
000009009009000
000009009009000
000009999999000
```

**Train 3 — input**

```text
472000000000000
000000000000000
099999990000000
090090090000000
090090090000000
090090090000000
099999990888000
007000000808000
007700000888000
000700000000000
000000000000000
000000000000000
```

**Train 3 — output**

```text
472000000000000
000000000000000
022222220000000
020020020000000
020020020000000
020020020000000
022222220777000
002000000707000
002200000777000
000200000000000
000000000000000
000000000000000
```

**Train 4 — input**

```text
8160000000000000
0000000000000000
0007000000000000
0007700000000000
0000700000000000
0000000009999999
0000000009009009
0888000009009009
0808000009009009
0888000009999999
0000000000000000
```

**Train 4 — output**

```text
8160000000000000
0000000000000000
0008000000000000
0008800000000000
0000800000000000
0000000006666666
0000000006006006
0111000006006006
0101000006006006
0111000006666666
0000000000000000
```

**Test — input**

```text
5290000000000000
0000000000000000
0888000000000000
0808000000700000
0888000000770000
0000000000070000
0000000099999990
0000000090090090
0000000090090090
0000000090090090
0000000099999990
0000000000000000
```

**Test — output**

```text
5290000000000000
0000000000000000
0222000000000000
0202000000900000
0222000000990000
0000000000090000
0000000099999990
0000000090090090
0000000090090090
0000000090090090
0000000099999990
0000000000000000
```

**Written solution**

The first three nonzero cells in the top row give the output colors for components with 0, 1, and 2 holes. Recolor every component below the legend according to its hole count.

**Reference program**

```python
def rule_h45(g):
    legend=[v for v in g[0] if v!=0][:3]
    h,w=size(g)
    out=blank(h,w)
    out[0]=g[0][:]
    vis=[[False]*w for _ in range(h)]
    for r in range(1,h):
        for c in range(w):
            if vis[r][c] or g[r][c]==0:
                continue
            vis[r][c]=True
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if nr>=1 and not vis[nr][nc] and g[nr][nc]!=0:
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            holes=hole_count_of_cells(cells)
            color=legend[min(holes,2)]
            for rr,cc in cells:
                out[rr][cc]=color
    return out
```

### H46 — Manhattan Tie Cells In Frame

**Difficulty:** hard

**Train pairs:** 4

**Skills:** distance geometry, frame interior, equidistance

**Suggested staged path:** The new color does not spread from one seed; it marks cells that are balanced between the two seeds.

**Train 1 — input**

```text
0000000000000
0444444444440
0400000000040
0402000000040
0400000000040
0400000000040
0400000000040
0400000003040
0400000000040
0444444444440
0000000000000
```

**Train 1 — output**

```text
0000000000000
0444444444440
0400000090040
0402000090040
0400000900040
0400009000040
0400090000040
0400900003040
0400900000040
0444444444440
0000000000000
```

**Train 2 — input**

```text
000000000000
005555555500
005070000500
005000000500
005000000500
005000000500
005000020500
005000000500
005555555500
000000000000
```

**Train 2 — output**

```text
000000000000
005555555500
005070000500
005000000500
005000000500
005000000500
005000020500
005000000500
005555555500
000000000000
```

**Train 3 — input**

```text
00000000000000
00000000000000
06666666666660
06000000000060
06080000000060
06000000000060
06000000000060
06000000000060
06000000050060
06000000000060
06666666666660
00000000000000
```

**Train 3 — output**

```text
00000000000000
00000000000000
06666666666660
06000000900060
06080000900060
06000009000060
06000090000060
06000900000060
06009000050060
06009000000060
06666666666660
00000000000000
```

**Train 4 — input**

```text
00000000000
03333333330
03000000030
03000002030
03000000030
03000000030
03000000030
03060000030
03000000030
03333333330
00000000000
```

**Train 4 — output**

```text
00000000000
03333333330
03990000030
03990002030
03009000030
03000900030
03000090030
03060009930
03000009930
03333333330
00000000000
```

**Test — input**

```text
0000000000000
0777777777770
0700000000070
0700200000070
0700000000070
0700000000070
0700000000070
0700000000070
0700000050070
0700000000070
0777777777770
0000000000000
```

**Test — output**

```text
0000000000000
0777777777770
0700000000070
0700200000070
0700000000070
0700000000070
0700000000070
0700000000070
0700000050070
0700000000070
0777777777770
0000000000000
```

**Written solution**

Keep the frame and the two seeds. Inside the frame, color every cell whose Manhattan distance to the first seed equals its Manhattan distance to the second seed with 9.

**Reference program**

```python
def rule_h46(g):
    h,w=size(g)
    out=blank(h,w)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frame=(color,bbox(cells))
            break
    assert frame is not None
    fcolor,(r0,c0,r1,c1)=frame
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and v!=fcolor and not (r==0 or c==0 or r==h-1 or c==w-1)]
    assert len(seeds)==2
    (rA,cA,vA),(rB,cB,vB)=seeds
    out[rA][cA]=vA; out[rB][cB]=vB
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if (r,c) in [(rA,cA),(rB,cB)]:
                continue
            if abs(r-rA)+abs(c-cA) == abs(r-rB)+abs(c-cB):
                out[r][c]=9
    return out
```

### H47 — Rotate Then Flip

**Difficulty:** hard

**Train pairs:** 4

**Skills:** command composition, rotation, reflection, cropping

**Suggested staged path:** There are two commands, and order matters. Rotate first, then apply the chosen flip.

**Train 1 — input**

```text
200000000001
000000000000
000000000000
000002300000
000002330000
000000300000
000000000000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
030
333
022
```

**Train 2 — input**

```text
40000000002
00000000000
00004400000
00000400000
00000440000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
400
444
004
```

**Train 3 — input**

```text
3000000000001
0000000000000
0000000000000
0000000000000
0000005600000
0000005560000
0000000060000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 3 — output**

```text
065
655
600
```

**Train 4 — input**

```text
1000000002
0000000000
0000000000
0000000000
0000000000
0023000000
0023300000
0003000000
0000000000
0000000000
```

**Train 4 — output**

```text
032
332
030
```

**Test — input**

```text
200000000002
000000000000
000000000000
000000000000
000005600000
000005560000
000000060000
000000000000
000000000000
000000000000
000000000000
```

**Test — output**

```text
550
650
066
```

**Written solution**

Ignore the two command cells in the top corners. Crop the remaining object, rotate it according to the left command (1=id, 2=90° clockwise, 3=180°, 4=270° clockwise), then flip it according to the right command (1=vertical flip across a horizontal axis, 2=horizontal flip across a vertical axis).

**Reference program**

```python
def rule_h47(g):
    cmd_rot=g[0][0]
    cmd_flip=g[0][-1]
    base=clone(g); base[0][0]=0; base[0][-1]=0
    cropped=crop_nonzero(base)
    out=rotate_times(cropped, {1:0,2:1,3:2,4:3}[cmd_rot])
    out=flip_h(out) if cmd_flip==1 else flip_v(out)
    return out
```

### H48 — Hole-Sorted Component Strip

**Difficulty:** hard

**Train pairs:** 4

**Skills:** component extraction, hole counting, dynamic ordering, layout

**Suggested staged path:** First split the objects, then count holes, then arrange. Do not try to sort raw pixels directly.

**Train 1 — input**

```text
00000000000000000000
00000000000000000000
08880000000000000000
08080000070000000000
08880000077000000000
00000000007000000000
00000000000099999990
00000000000090090090
00000000000090090090
00000000000090090090
00000000000099999990
00000000000000000000
```

**Train 1 — output**

```text
70088809999999
77080809009009
07088809009009
00000009009009
00000009999999
```

**Train 2 — input**

```text
00000000000000000000
00000000000000000000
09999999000000000000
09009009000000000000
09009009000000000000
09009009000088800000
09997999000080800000
00007700000088800000
00000700000000000000
00000000000000000000
00000000000000000000
```

**Train 2 — output**

```text
88809999999
80809009009
88809009009
00009009009
00009997999
00000007700
00000000700
```

**Train 3 — input**

```text
00000000000000000000
00000000000000000000
00700000008880000000
00770000008080000000
00070000008880000000
00000000000000000000
00000000000099999990
00000000000090090090
00000000000090090090
00000000000090090090
00000000000099999990
00000000000000000000
```

**Train 3 — output**

```text
70088809999999
77080809009009
07088809009009
00000009009009
00000009999999
```

**Train 4 — input**

```text
00000000000000000000
00000000000000000000
00008880000000000000
00008080000000000000
00008880000000000000
00000000000999999900
07000000000900900900
07700000000900900900
00700000000900900900
00000000000999999900
00000000000000000000
```

**Train 4 — output**

```text
70088809999999
77080809009009
07088809009009
00000009009009
00000009999999
```

**Test — input**

```text
00000000000000000000
00000000000000000000
00999999900000000000
00900900900000000000
00900900900000000000
00900900900008880000
00999999900008080000
00007000000008880000
00007700000000000000
00000700000000000000
00000000000000000000
00000000000000000000
```

**Test — output**

```text
88809999999
80809009009
88809009009
00009009009
00009999999
00000070000
00000077000
00000007000
```

**Written solution**

Extract the disconnected nonzero components, sort them by hole count ascending and then by area ascending, crop each one tightly, and place the cropped components left to right with one zero column between them.

**Reference program**

```python
def rule_h48(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=False):
        crop=crop_bbox(g, cells)
        holes=hole_count_of_cells(cells)
        area=len(cells)
        comps.append((holes, area, color, crop))
    comps.sort(key=lambda x:(x[0], x[1], x[2]))
    maxh=max(len(crop) for _,_,_,crop in comps)
    totalw=sum(len(crop[0]) for _,_,_,crop in comps)+max(0,len(comps)-1)
    out=blank(maxh,totalw)
    x=0
    for _,_,_,crop in comps:
        h,w=size(crop)
        for r in range(h):
            for c in range(w):
                out[r][x+c]=crop[r][c]
        x += w+1
    return out
```

### H49 — Polyline Intersections Highlighted

**Difficulty:** hard

**Train pairs:** 4

**Skills:** multi-object tracing, intersection detection, marker order

**Suggested staged path:** First trace each color’s path separately. Only after that decide which cells are overlaps.

**Train 1 — input**

```text
000005000000
020000002000
000000000000
000000000000
000000000000
000000000000
005005000000
000000002000
000000000000
000000000000
```

**Train 1 — output**

```text
005555000000
029222222000
005000002000
005000002000
005000002000
005000002000
005555002000
000000002000
000000000000
000000000000
```

**Train 2 — input**

```text
00030000000
00000000000
70000070000
00000000000
00000000000
00030000300
00000000000
00000070000
00000000000
```

**Train 2 — output**

```text
00030000000
00030000000
77797770000
00030070000
00030070000
00033393300
00000070000
00000070000
00000000000
```

**Train 3 — input**

```text
0000008000000
0000000000400
0000000000000
0000000000000
0000008000080
0000000000000
0004000000400
0000000000000
0000000000000
0000000000000
```

**Train 3 — output**

```text
0000008000000
0004449444400
0004008000000
0004008000000
0004008888880
0004000000000
0004444444400
0000000000000
0000000000000
0000000000000
```

**Train 4 — input**

```text
000020000000
060000060000
000000000000
000000000000
000000000000
020020000000
000000060000
000000000000
000000000000
```

**Train 4 — output**

```text
022220000000
096666660000
020000060000
020000060000
020000060000
022220060000
000000060000
000000000000
000000000000
```

**Test — input**

```text
0000007000000
0020000002000
0000000000000
0000000000000
0000000000000
0000000000000
0007007000000
0000000002000
0000000000000
0000000000000
```

**Test — output**

```text
0007777000000
0029222222000
0007000002000
0007000002000
0007000002000
0007000002000
0007777002000
0000000002000
0000000000000
0000000000000
```

**Written solution**

Sort each color’s markers in reading order and trace a horizontal-then-vertical Manhattan polyline through them. Color normal path cells with their path color, but recolor any cell used by two or more different paths to 9.

**Reference program**

```python
def rule_h49(g):
    h,w=size(g)
    colors=sorted({v for row in g for v in row if v!=0})
    groups=[]
    for color in colors:
        groups.append((color, sorted((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color)))
    return trace_polyline_markers(blank(h,w), groups, mode='hv', intersection_color=9)
```
