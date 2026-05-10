# ARC-style Puzzle Bank — 21 more puzzles (set 5)

This fifth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It deliberately broadens the task mix: crop/extract tasks, count/build tasks, legend-driven remaps, submatrix selection, rotation-invariant matching, and several ray-based tasks.

This set also introduces a new helper primitive:

```text
raycast_until(grid, start, step, blockers=None, include_blocker=False)
  Walk from start+step in a straight line until the first blocker or the edge,
  returning the traversed cells.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set5_reference.py`.

## Index

### Easy

- **S5_E1** — Legend Color Crop
- **S5_E2** — Blue Dot Count Strip
- **S5_E3** — Marked Row Extraction
- **S5_E4** — Rightward Ray Paint
- **S5_E5** — Border-Touching Shape Crop
- **S5_E6** — Horizontal Segment Completion
- **S5_E7** — Green Dot Count Square

### Medium

- **S5_M1** — Quadrant Palette Summary
- **S5_M2** — Beam Crossing Cells
- **S5_M3** — Marked Column Compression
- **S5_M4** — Object-Area Color Ranking
- **S5_M5** — Hole Count Object Selector
- **S5_M6** — Template Stamp at Anchors
- **S5_M7** — Nonempty Row Compression

### Hard

- **S5_H1** — Cells Seen by Two Emitters
- **S5_H2** — Two-Row Palette Permutation
- **S5_H3** — Rotation-Coded Stamps
- **S5_H4** — Repeated Shape Under Rotation
- **S5_H5** — Matched Beacon Corridors
- **S5_H6** — Color Count Histogram
- **S5_H7** — Row/Column Submatrix Extraction

# Easy

## S5_E1 — Legend Color Crop

**Skills:** legend reading, component extraction, output-size crop

**Scaffold:**
- Read the nonzero legend color in the top-left corner.
- Find the connected object elsewhere with that same color.
- Crop to that object's bounding box.

**Train 1 input**
```text
30000000
00000011
00000011
00003000
00003000
00003300
02220000
00000000
```
**Train 1 output**
```text
30
30
33
```
**Train 2 input**
```text
100000000
000000000
000000070
000000770
000111000
000010000
003000000
033300000
000000000
```
**Train 2 output**
```text
111
010
```
**Test input**
```text
7000000000
0000000040
0000070044
0000077000
0000007000
0000000000
0110000000
0010000000
```
**Test output**
```text
70
77
07
```
**Written solution:** Read the legend color from the top-left cell. Find the single object of that color elsewhere in the grid, and output only its bounding box crop.

**Reference program:**
```python
def solve(grid):
    target = grid[0][0]
    comps = components(grid, {target}, 4, ignore_cells={(0,0)})
    # choose largest or only
    comp = max(comps, key=lambda c: len(c['cells']))
    return crop_bbox(grid, comp['cells'])
```

## S5_E2 — Blue Dot Count Strip

**Skills:** counting, output construction, single-color summary

**Scaffold:**
- Count all blue(1) singleton cells in the grid.
- Ignore their positions.
- Output a 1-row strip of red(2) cells of that length.

**Train 1 input**
```text
010000
000000
000010
000000
100000
```
**Train 1 output**
```text
222
```
**Train 2 input**
```text
1000000
0000010
0010000
0000000
0000001
0001000
```
**Train 2 output**
```text
22222
```
**Test input**
```text
00000001
01000000
00000000
00010000
00000100
```
**Test output**
```text
2222
```
**Written solution:** Count the blue(1) dots. Build a single-row output whose length equals that count, and fill the row with red(2).

**Reference program:**
```python
def solve(grid):
    n = sum(cell==1 for row in grid for cell in row)
    return [[2]*n] if n>0 else [[0]]
```

## S5_E3 — Marked Row Extraction

**Skills:** indexing, row selection, output-size crop

**Scaffold:**
- Find the magenta(6) marker in the leftmost column.
- Take that entire row, excluding the marker column.
- Return it as a 1-row output.

**Train 1 input**
```text
0011002
0300300
0440040
6123400
0005550
0700077
```
**Train 1 output**
```text
123400
```
**Train 2 input**
```text
01010101
62220000
00303030
04044004
05500505
```
**Train 2 output**
```text
2220000
```
**Test input**
```text
00770070
08080808
00099900
02202022
61001100
03330033
```
**Test output**
```text
1001100
```
**Written solution:** Use the magenta(6) marker in the first column to choose one row. Remove the marker column and output the contents of that marked row by itself.

**Reference program:**
```python
def solve(grid):
    r = next(i for i,row in enumerate(grid) if row[0]==6)
    return [grid[r][1:]]
```

## S5_E4 — Rightward Ray Paint

**Skills:** directional propagation, blocking, same-size transform

**Primitive note:** Uses the new primitive `raycast_until(start, step, blockers)`.

**Scaffold:**
- Find each yellow(4) emitter.
- Cast a ray to the right until a maroon(9) blocker or the grid edge.
- Paint the traversed empty cells cyan(8), keeping emitters and blockers unchanged.

**Train 1 input**
```text
0000000000
0400000090
0000000000
4000090000
0000004000
0000000000
```
**Train 1 output**
```text
0000000000
0488888890
0000000000
4888890000
0000004888
0000000000
```
**Train 2 input**
```text
00400090000
00000000000
00004000009
00000000000
00000000000
04090000000
00000000000
```
**Train 2 output**
```text
00488890000
00000000000
00004888889
00000000000
00000000000
04890000000
00000000000
```
**Test input**
```text
000000000000
400090000000
000004000009
000000000000
000400000000
000000000000
```
**Test output**
```text
000000000000
488890000000
000004888889
000000000000
000488888888
000000000000
```
**Written solution:** From every yellow(4) emitter, paint a cyan(8) beam to the right. The beam continues through empty cells and stops just before the first maroon(9) blocker, or at the boundary if there is no blocker.

**Reference program:**
```python
def solve(grid):
    out = copyg(grid)
    for r,row in enumerate(grid):
        for c,val in enumerate(row):
            if val==4:
                for rr,cc in raycast_until(grid,(r,c),(0,1),blockers={9}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out
```

## S5_E5 — Border-Touching Shape Crop

**Skills:** border detection, component selection, output-size crop

**Scaffold:**
- Extract the red(2) connected components.
- Identify the one that touches any grid border.
- Crop exactly that component's bounding box.

**Train 1 input**
```text
00000000
00000220
20000220
20000000
22000000
00000000
00001100
00000000
```
**Train 1 output**
```text
20
20
22
```
**Train 2 input**
```text
000002200
000000200
000000200
000000004
000000000
022200000
002000000
000000000
```
**Train 2 output**
```text
22
02
02
```
**Test input**
```text
100000000
000000000
000000200
000000200
000002200
000000000
000200000
002200000
002000000
```
**Test output**
```text
02
22
20
```
**Written solution:** Among the red(2) objects, choose the one that touches the outer border of the input. Output only the bounding-box crop of that border-touching object.

**Reference program:**
```python
def solve(grid):
    comps = components(grid, {2}, 4)
    h,w=dims(grid)
    def touches_border(comp):
        return any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells'])
    comp = next(comp for comp in comps if touches_border(comp))
    return crop_bbox(grid, comp['cells'])
```

## S5_E6 — Horizontal Segment Completion

**Skills:** scanline reasoning, between-markers fill, same-size transform

**Scaffold:**
- Look row by row.
- Whenever a row contains exactly two blue(1) markers, fill the cells between them.
- Leave all other rows unchanged.

**Train 1 input**
```text
000000000
010001000
000000000
100000001
000010000
000000000
```
**Train 1 output**
```text
000000000
011111000
000000000
111111111
000010000
000000000
```
**Train 2 input**
```text
0010000100
0000000000
0000101000
0000000000
0000000000
0101000000
0000000000
```
**Train 2 output**
```text
0011111100
0000000000
0000111000
0000000000
0000000000
0111000000
0000000000
```
**Test input**
```text
00000000000
10001000000
00000100001
00000000000
00010001000
00000000000
```
**Test output**
```text
00000000000
11111000000
00000111111
00000000000
00011111000
00000000000
```
**Written solution:** In each row that has exactly two blue(1) endpoints, fill the whole horizontal segment between them with blue(1).

**Reference program:**
```python
def solve(grid):
    out = copyg(grid)
    h,w=dims(grid)
    for r in range(h):
        cols=[c for c in range(w) if grid[r][c]==1]
        if len(cols)==2:
            a,b=cols
            for c in range(a,b+1):
                out[r][c]=1
    return out
```

## S5_E7 — Green Dot Count Square

**Skills:** counting, output construction, size inference

**Scaffold:**
- Count the green(3) dots in the input.
- Use that count as both the height and width.
- Output an orange(7) square of that size.

**Train 1 input**
```text
000000
030000
000000
000030
000000
```
**Train 1 output**
```text
77
77
```
**Train 2 input**
```text
3000000
0000030
0000000
0000000
0030000
0000003
```
**Train 2 output**
```text
7777
7777
7777
7777
```
**Test input**
```text
0000003
0000000
0030000
0000000
0300000
```
**Test output**
```text
777
777
777
```
**Written solution:** Count the green(3) dots. If there are n of them, output an n×n square filled with orange(7).

**Reference program:**
```python
def solve(grid):
    n = sum(cell==3 for row in grid for cell in row)
    return [[7]*n for _ in range(n)] if n>0 else [[0]]
```

# Medium

## S5_M1 — Quadrant Palette Summary

**Skills:** spatial partitioning, color summarization, output compression

**Scaffold:**
- Split the input into four equal quadrants.
- Read the nonzero color present in each quadrant, or 0 if it is empty.
- Write those four values into a 2×2 summary grid.

**Train 1 input**
```text
00000000
01100000
01000000
00000000
00000300
02000330
02200000
00000000
```
**Train 1 output**
```text
10
23
```
**Train 2 input**
```text
00000400
00000440
00000000
00000000
00000000
77000080
07000880
00000000
```
**Train 2 output**
```text
04
78
```
**Test input**
```text
0000000000
0900000500
0090000000
0000000050
0000000000
0000000000
0000000000
0060000000
0660000000
0000000000
```
**Test output**
```text
95
60
```
**Written solution:** Partition the grid into top-left, top-right, bottom-left, and bottom-right quadrants. For each quadrant, output its single nonzero color, or 0 if it has none.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    mh,mw=h//2,w//2
    out=[[0,0],[0,0]]
    quads=[(0,mh,0,mw),(0,mh,mw,w),(mh,h,0,mw),(mh,h,mw,w)]
    for idx,(r1,r2,c1,c2) in enumerate(quads):
        colors={grid[r][c] for r in range(r1,r2) for c in range(c1,c2) if grid[r][c]!=0}
        val=next(iter(colors)) if colors else 0
        out[idx//2][idx%2]=val
    return out
```

## S5_M2 — Beam Crossing Cells

**Skills:** orthogonal ray casting, set intersection, same-size output

**Primitive note:** Uses the new primitive `raycast_until(start, step, blockers)`.

**Scaffold:**
- Cast red(2) beams downward from the top-row emitters until gray(5) blockers.
- Cast blue(1) beams rightward from the left-column emitters until gray(5) blockers.
- Output only the cells visited by both kinds of beams, colored magenta(6).

**Train 1 input**
```text
00200200
00000000
00000000
10000000
00000000
00000000
10000000
00000000
```
**Train 1 output**
```text
00000000
00000000
00000000
00600600
00000000
00000000
00600600
00000000
```
**Train 2 input**
```text
000200200
000000000
100005000
000000000
000500000
100000000
000000500
000000000
000000000
```
**Train 2 output**
```text
000000000
000000000
000600000
000000000
000000000
000000600
000000000
000000000
000000000
```
**Test input**
```text
0200000200
1000000000
0000000000
0500000000
0000000000
1000500000
0000000000
0000000000
```
**Test output**
```text
0000000000
0600000600
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Written solution:** Top red(2) emitters send vertical beams downward and left blue(1) emitters send horizontal beams rightward. Both stop before gray(5) blockers. The output keeps only the crossing cells, colored magenta(6).

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    vert=set()
    horiz=set()
    for c,val in enumerate(grid[0]):
        if val==2:
            vert.update(raycast_until(grid,(0,c),(1,0),blockers={5}))
    for r in range(h):
        if grid[r][0]==1:
            horiz.update(raycast_until(grid,(r,0),(0,1),blockers={5}))
    inter=vert & horiz
    out=blank(h,w)
    for r,c in inter:
        out[r][c]=6
    return out
```

## S5_M3 — Marked Column Compression

**Skills:** column selection, legend markers, output-size change

**Scaffold:**
- Read the top-row marker positions.
- Select those columns from the body of the grid.
- Compress them side by side in the same order.

**Train 1 input**
```text
04004040
01234567
76543210
10101010
22222222
98765432
```
**Train 1 output**
```text
146
631
011
222
853
```
**Train 2 input**
```text
004004004
123456789
987654321
010101010
246802468
```
**Train 2 output**
```text
369
741
010
628
```
**Test input**
```text
0404000404
5432101234
0987654321
1122334455
5544332211
0101010101
9090909090
```
**Test output**
```text
4224
9731
1245
5421
1111
0000
```
**Written solution:** The top row marks which columns matter. Remove the top row, keep only the marked columns from the remaining rows, and pack those columns together in order.

**Reference program:**
```python
def solve(grid):
    cols=[c for c,v in enumerate(grid[0]) if v==4]
    body=grid[1:]
    return [[row[c] for c in cols] for row in body]
```

## S5_M4 — Object-Area Color Ranking

**Skills:** component measurement, sorting, symbolic output

**Scaffold:**
- Extract all nonzero connected components.
- Measure each component's area.
- Output a 1-row strip of component colors ordered from smallest area to largest.

**Train 1 input**
```text
00000000
01000220
00000000
00000000
03000440
03300440
00000000
00000000
```
**Train 1 output**
```text
1234
```
**Train 2 input**
```text
000000000
000000050
000000050
000000000
000060000
000000000
077000880
070000888
000000000
```
**Train 2 output**
```text
6578
```
**Test input**
```text
0000000000
0990000030
0990000000
0000000000
0000000000
0020000000
0020000400
0000000440
0000000000
0000000000
```
**Test output**
```text
3249
```
**Written solution:** Measure the size of every colored object. Then output a single row listing the objects' colors in ascending order of area.

**Reference program:**
```python
def solve(grid):
    comps=components(grid, None, 4)
    comps_sorted=sorted(comps, key=lambda comp:(len(comp['cells']), comp['color']))
    return [[comp['color'] for comp in comps_sorted]]
```

## S5_M5 — Hole Count Object Selector

**Skills:** hole counting, marker decoding, output-size crop

**Scaffold:**
- Count the blue(1) markers in the top row.
- Compute the number of enclosed holes in each orange(7) object.
- Crop the object whose hole count matches the marker count.

**Train 1 input**
```text
10000000000000
00000077700000
07770070700000
07770077700000
00000000000000
00000000000000
00000777777700
00000700700700
00000777777700
00000000000000
```
**Train 1 output**
```text
777
707
777
```
**Train 2 input**
```text
11000000000000
00000077700000
07770070700000
07770077700000
00000000000000
00000000000000
00000777777700
00000700700700
00000777777700
00000000000000
```
**Train 2 output**
```text
7777777
7007007
7777777
```
**Test input**
```text
00000000000000
00000077700000
07770070700000
07770077700000
00000000000000
00000000000000
00000777777700
00000700700700
00000777777700
00000000000000
```
**Test output**
```text
777
777
```
**Written solution:** The number of blue(1) markers in the first row tells you how many holes to look for. Among the orange(7) objects, choose the one with exactly that many holes and output its bounding-box crop.

**Reference program:**
```python
def solve(grid):
    k=sum(v==1 for v in grid[0])
    body=grid[1:]
    # components in body with absolute coords offset by 1 row
    comps=components(grid, {7}, 4)
    # ignore top row markers if any 7? none
    selected=None
    for comp in comps:
        if count_holes(grid, comp)==k:
            selected=comp
            break
    return crop_bbox(grid, selected['cells'])
```

## S5_M6 — Template Stamp at Anchors

**Skills:** template extraction, shape copying, same-size construction

**Scaffold:**
- Find the green(3) source object and normalize its shape.
- Use every red(4) singleton as a top-left anchor.
- Stamp cyan(8) copies of the template at all anchor positions on a blank grid.

**Train 1 input**
```text
3000000000
3300000000
0000000000
0000400000
0000000000
0000000400
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0000800000
0000880000
0000000800
0000000880
0000000000
```
**Train 2 input**
```text
00000000000
03300000000
00330000000
00000000000
00000400000
00000000400
04000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00000000000
00000000000
00000880000
00000088880
08800000088
00880000000
00000000000
```
**Test input**
```text
030000000000
033000000000
003000000000
000000400000
000000000000
000000000000
000400000000
000000004000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000000800000
000000880000
000000080000
000800000000
000880008000
000080008800
000000000800
```
**Written solution:** Treat the green(3) object as a reusable template. For each red(4) anchor cell, place a cyan(8) copy of that template with its top-left corner at the anchor. The output is otherwise blank.

**Reference program:**
```python
def solve(grid):
    comps=components(grid, {3}, 4)
    template = max(comps, key=lambda c: len(c['cells']))
    norm = normalize_cells(template['cells'])
    out=blank(*dims(grid))
    h,w=dims(grid)
    # anchors color4
    for r in range(h):
        for c in range(w):
            if grid[r][c]==4:
                for dr,dc in norm:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=8
    return out
```

## S5_M7 — Nonempty Row Compression

**Skills:** row filtering, order preservation, output-size compression

**Scaffold:**
- Scan rows from top to bottom.
- Keep only rows that contain at least one nonzero cell.
- Stack the surviving rows without changing their order.

**Train 1 input**
```text
000000
120000
000000
003300
000000
400004
```
**Train 1 output**
```text
120000
003300
400004
```
**Train 2 input**
```text
0000000
0000000
1110000
0000000
0022200
0000000
0000003
```
**Train 2 output**
```text
1110000
0022200
0000003
```
**Test input**
```text
00000000
50000005
00000000
01111000
00000000
00070000
00000000
33000033
```
**Test output**
```text
50000005
01111000
00070000
33000033
```
**Written solution:** Delete every all-zero row. Keep the nonempty rows in the same order and stack them together.

**Reference program:**
```python
def solve(grid):
    rows=[row[:] for row in grid if any(v!=0 for v in row)]
    return rows if rows else [[0]*len(grid[0])]
```

# Hard

## S5_H1 — Cells Seen by Two Emitters

**Skills:** multi-source visibility, ray counting, thresholding

**Primitive note:** Uses the new primitive `raycast_until(start, step, blockers)` in four directions.

**Scaffold:**
- From each yellow(4) emitter, cast rays in all four cardinal directions until gray(5) blockers or the edge.
- Count how many emitters can see each cell.
- Output only the cells seen by at least two emitters, colored red(2).

**Train 1 input**
```text
0000000
0400040
0000000
0005000
0000000
0004000
0000000
```
**Train 1 output**
```text
0000000
2022202
0000000
0000000
0000000
0200020
0000000
```
**Train 2 input**
```text
00000000
00400000
00000500
00000000
00400040
00500000
00000000
00000000
```
**Train 2 output**
```text
00200000
00000020
00200000
00200000
22222202
00000000
00000000
00000000
```
**Test input**
```text
000000000
040000040
000000000
000000000
050040050
000000000
000000000
000040000
000000000
```
**Test output**
```text
000020000
202222202
000020000
000020000
000000000
000020000
000020000
000000000
000020000
```
**Written solution:** Every yellow(4) emitter sees outward in the four cardinal directions until a gray(5) blocker or the boundary. Count the visibility coverage, and keep only cells reached by two or more emitters.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    counts=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if grid[r][c]==4:
                for step in dirs4:
                    for rr,cc in raycast_until(grid,(r,c),step,blockers={5}):
                        counts[rr][cc]+=1
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if counts[r][c]>=2:
                out[r][c]=2
    return out
```

## S5_H2 — Two-Row Palette Permutation

**Skills:** legend mapping, color permutation, header removal

**Scaffold:**
- Read the source colors from the first row and the corresponding target colors from the second row.
- Build a color map from those aligned pairs.
- Recolor the remaining body rows with that map and drop the legend rows.

**Train 1 input**
```text
123000
789000
100220
110220
003300
003330
```
**Train 1 output**
```text
700880
770880
009900
009990
```
**Train 2 input**
```text
2460000
1380000
2004400
2204400
0000060
0000660
```
**Train 2 output**
```text
1003300
1103300
0000080
0000880
```
**Test input**
```text
13500000
92700000
10050000
03350000
00335000
00000111
```
**Test output**
```text
90070000
02270000
00227000
00000999
```
**Written solution:** The first two rows form a source→target color legend by column. Apply that recoloring to the body of the grid and output only the recolored body.

**Reference program:**
```python
def solve(grid):
    src=grid[0]
    tgt=grid[1]
    mp={}
    for a,b in zip(src,tgt):
        if a!=0:
            mp[a]=b
    body=grid[2:]
    return [[mp.get(v,v) if v!=0 else 0 for v in row] for row in body]
```

## S5_H3 — Rotation-Coded Stamps

**Skills:** template extraction, rotation reasoning, coded markers

**Scaffold:**
- Normalize the green(3) template shape.
- Interpret marker colors 1,2,4,5 as 0°, 90°, 180°, and 270° rotations.
- Stamp cyan(8) rotated copies on a blank grid, anchored at each marker cell.

**Train 1 input**
```text
3000000000
3300000000
0000000000
0000100000
0000000000
0200000000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0000800000
0000880000
0880000000
0800000000
0000000000
```
**Train 2 input**
```text
03000000000
33000005000
03000000000
00000000000
00000400000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000008880
00000000800
00000000000
00000800000
00000880000
00000800000
00000000000
00000000000
```
**Test input**
```text
330000000000
030000000000
030000000000
000000100000
000000000000
002000000000
000000004000
000000000000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000000880000
000000080000
000080080000
008880008000
000000008000
000000008800
000000000000
```
**Written solution:** Use the green(3) object as a template. Marker colors encode how much to rotate that template before stamping a cyan(8) copy starting at the marker location.

**Reference program:**
```python
def solve(grid):
    # colors 1,2,4,5 => rotations 0,1,2,3 quarter turns
    rot_map={1:0,2:1,4:2,5:3}
    template=max(components(grid,{3},4), key=lambda c: len(c['cells']))
    base=normalize_cells(template['cells'])
    out=blank(*dims(grid))
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] in rot_map:
                shape=rotate_norm_cells(base, rot_map[grid[r][c]])
                for dr,dc in shape:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=8
    return out
```

## S5_H4 — Repeated Shape Under Rotation

**Skills:** rotation-invariant matching, component normalization, canonical output

**Scaffold:**
- Normalize every blue(1) component up to rotation.
- Find the shape that appears twice under rotation.
- Output its canonical normalized form in cyan(8).

**Train 1 input**
```text
0000000000
0100001100
0110000100
0000000000
0000001100
0111001100
0000000000
0000000000
```
**Train 1 output**
```text
88
80
```
**Train 2 input**
```text
00000000000
00110000000
01100001000
00000001000
00000000000
00000001000
01000001100
01100000100
00000000000
```
**Train 2 output**
```text
80
88
08
```
**Test input**
```text
000000000000
001000000000
001000000110
001100000010
000000000000
000000000010
000000001110
011100000000
001000000000
000000000000
```
**Test output**
```text
888
800
```
**Written solution:** Among the blue(1) objects, one shape is repeated in a different rotation. Detect that repeated shape up to rotation, choose a canonical orientation, and output it alone in cyan(8).

**Reference program:**
```python
def solve(grid):
    comps=components(grid,{1},4)
    canons=[canonical_rot(normalize_cells(comp['cells'])) for comp in comps]
    from collections import Counter
    cnt=Counter(canons)
    target=next(c for c,n in cnt.items() if n>=2)
    # output canonical shape in color 8
    maxr=max(r for r,c in target); maxc=max(c for r,c in target)
    out=blank(maxr+1,maxc+1)
    for r,c in target:
        out[r][c]=8
    return out
```

## S5_H5 — Matched Beacon Corridors

**Skills:** pairing by color, axis alignment, same-size construction

**Primitive note:** Can be implemented as repeated axis-aligned ray walks between matched endpoints.

**Scaffold:**
- Group the singleton beacons by color.
- Each color appears exactly twice and the two beacons are aligned horizontally or vertically.
- Fill the corridor between each pair using that same color.

**Train 1 input**
```text
000000000
020000200
000030000
000000000
000000000
400400000
000030000
000000000
```
**Train 1 output**
```text
000000000
022222200
000030000
000030000
000030000
444430000
000030000
000000000
```
**Train 2 input**
```text
0050000000
0000000000
0000000000
0000060006
0050000000
0000000000
0700000700
0000000000
0000000000
```
**Train 2 output**
```text
0050000000
0050000000
0050000000
0050066666
0050000000
0000000000
0777777700
0000000000
0000000000
```
**Test input**
```text
0000000000
2000020000
0000000030
0500000000
0000000000
0040004000
0000000000
0000000030
0500000000
0000000000
```
**Test output**
```text
0000000000
2222220000
0000000030
0500000030
0500000030
0544444030
0500000030
0500000030
0500000000
0000000000
```
**Written solution:** For every color, connect its two matching beacons with a solid straight segment of that color. Horizontal pairs make horizontal corridors and vertical pairs make vertical corridors.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    positions={}
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                positions.setdefault(v, []).append((r,c))
    out=blank(h,w)
    for color,cells in positions.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            a,b=sorted([c1,c2])
            clear=all(grid[r1][c]==0 or c in (a,b) for c in range(a,b+1))
            if clear:
                for c in range(a,b+1):
                    out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            clear=all(grid[r][c1]==0 or r in (a,b) for r in range(a,b+1))
            if clear:
                for r in range(a,b+1):
                    out[r][c1]=color
    return out
```

## S5_H6 — Color Count Histogram

**Skills:** counting by color, histogram construction, output resizing

**Scaffold:**
- Count total cells of color 1, then 2, then 3.
- Let the output width be the maximum of those counts.
- Build one row per color, filled from the left with that color repeated its count times.

**Train 1 input**
```text
100000
022000
020030
020000
000001
```
**Train 1 output**
```text
1100
2222
3000
```
**Train 2 input**
```text
1000003
0000023
0010003
0000003
0000003
0000001
```
**Train 2 output**
```text
11100
20000
33333
```
**Test input**
```text
01000000
01000000
01000333
01000000
00000000
22000000
```
**Test output**
```text
1111
2200
3330
```
**Written solution:** Count how many cells of colors 1, 2, and 3 appear. Make a three-row histogram: row 1 contains that many 1s, row 2 that many 2s, row 3 that many 3s, padded with zeros to a common width.

**Reference program:**
```python
def solve(grid):
    colors=[1,2,3]
    counts=[sum(v==color for row in grid for v in row) for color in colors]
    w=max(counts) if counts else 1
    out=blank(len(colors), w)
    for i,color in enumerate(colors):
        for c in range(counts[i]):
            out[i][c]=color
    return out
```

## S5_H7 — Row/Column Submatrix Extraction

**Skills:** dual-axis indexing, submatrix extraction, compositional selection

**Scaffold:**
- Use top-row red(4) markers to choose columns.
- Use left-column blue(5) markers to choose rows.
- Output the body submatrix at the selected rows and selected columns, preserving order.

**Train 1 input**
```text
0040404
0123456
5891234
4321012
5468024
9876543
```
**Train 1 output**
```text
924
604
```
**Train 2 input**
```text
04040004
52345678
87654321
01010101
99887766
54680246
50505050
```
**Train 2 output**
```text
248
486
000
```
**Test input**
```text
004004004
101010101
534567890
987654321
512233445
544332211
090807060
577000888
```
**Test output**
```text
470
235
421
708
```
**Written solution:** The top row selects columns and the left column selects rows. Take the interior grid and extract the submatrix formed by those chosen rows and columns.

**Reference program:**
```python
def solve(grid):
    sel_cols=[c for c,v in enumerate(grid[0]) if v==4 and c>0]
    sel_rows=[r for r in range(1,len(grid)) if grid[r][0]==5]
    return [[grid[r][c] for c in sel_cols] for r in sel_rows]
```
