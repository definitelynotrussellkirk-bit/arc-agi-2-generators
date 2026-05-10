# ARC-style Puzzle Bank — 21 more puzzles (set 10)

This tenth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans into beam tracing, interval completion, cropping, anchor-based transport, seeded room filling, legend remaps, gravity/projection effects, panel comparison, template stamping, and quadrant symmetry.

This set introduces a new helper primitive:

```text
trace_beam(grid, start, direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'})
  Trace a ray through passable cells; slash and backslash mirror cells turn the direction, and the beam stops at walls or the grid boundary.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set10_reference.py`.


## Index

### Easy

- **S10_E1** — Rightward Beam Trace
- **S10_E2** — Fill Row Intervals
- **S10_E3** — Crop the Active Bounding Box
- **S10_E4** — Move Shape to Anchor
- **S10_E5** — Keep Only Internal Objects
- **S10_E6** — Paint Aligned Midpoints
- **S10_E7** — Most-Frequent Color Bar

### Medium

- **S10_M1** — One-Mirror Beam
- **S10_M2** — Seeded Room Fill
- **S10_M3** — Two-Row Recolor Legend
- **S10_M4** — Pick the Object with Area N
- **S10_M5** — Column Gravity Compression
- **S10_M6** — Downward Color Shadows
- **S10_M7** — Two-Panel Difference Mask

### Hard

- **S10_H1** — Two-Mirror Beam Maze
- **S10_H2** — Rotation-Coded Template Stamps
- **S10_H3** — Extract the Unpaired Shape
- **S10_H4** — Three-Panel Majority Merge
- **S10_H5** — Legend-Driven Room Repaint
- **S10_H6** — Complete the Missing Symmetric Quadrant
- **S10_H7** — Count, Select, Move, Recolor


# Easy

## S10_E1 — Rightward Beam Trace

**Skills:** beam tracing, straight-line projection, same-size transform

**Primitive note:** Uses the new trace_beam primitive without mirrors.

**Scaffold:**
- Find each source cell color 2.
- Trace to the right through zeros until a wall color 5 or the edge.
- Color the traversed cells orange(7) and keep the source/walls.

**Train 1 input**
```text
000000000
020000050
000000000
000000000
200005000
000000000
```
**Train 1 output**
```text
000000000
027777750
000000000
000000000
277775000
000000000
```
**Train 2 input**
```text
0020000050
0000000000
0000000000
0000200500
0000000000
0000000000
0200050000
```
**Train 2 output**
```text
0027777750
0000000000
0000000000
0000277500
0000000000
0000000000
0277750000
```
**Test input**
```text
00000000000
00000200000
20000050000
00000000000
00000000000
00020000050
00000000000
00000000000
```
**Test output**
```text
00000000000
00000277777
27777750000
00000000000
00000000000
00027777750
00000000000
00000000000
```
**Written solution:** Treat every red(2) cell as a source that emits a beam to the right. Follow background cells until the beam would hit a gray(5) wall or leave the grid, and paint exactly those traversed cells orange(7). Keep the original sources and walls unchanged.

**Reference program:**
```python
def solve_S10_E1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}):
                    if out[rr][cc]==0:
                        out[rr][cc]=7
    return out
```

## S10_E2 — Fill Row Intervals

**Skills:** row scanning, endpoint detection, interval fill

**Scaffold:**
- Work row by row.
- When the same nonzero color appears exactly twice in a row, look at the cells between them.
- If the middle is empty, fill the full interval with that color.

**Train 1 input**
```text
000000000
030000300
000000000
000000000
004000004
000000000
```
**Train 1 output**
```text
000000000
033333300
000000000
000000000
004444444
000000000
```
**Train 2 input**
```text
2000200000
0000000000
0000000000
0007000007
0000000000
0600000600
0000000000
```
**Train 2 output**
```text
2222200000
0000000000
0000000000
0007777777
0000000000
0666666600
0000000000
```
**Test input**
```text
00000000000
00900000009
00000000000
00000000000
40000040000
00000000000
00000300030
00000000000
```
**Test output**
```text
00000000000
00999999999
00000000000
00000000000
44444440000
00000000000
00000333330
00000000000
```
**Written solution:** In each row, look for a color that appears exactly twice. When the two copies of that color bound an all-zero gap, fill from the left endpoint to the right endpoint inclusive with that same color. Rows without such a pair stay unchanged.

**Reference program:**
```python
def solve_S10_E2(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        pos=defaultdict(list)
        for c,v in enumerate(grid[r]):
            if v!=0:
                pos[v].append(c)
        for v, cols in pos.items():
            if len(cols)==2:
                c1,c2=cols
                if all(grid[r][c]==0 for c in range(c1+1,c2)):
                    for c in range(c1,c2+1):
                        out[r][c]=v
    return out
```

## S10_E3 — Crop the Active Bounding Box

**Skills:** bounding box, size change, object localization

**Scaffold:**
- Find every nonzero cell in the input.
- Compute the smallest rectangle containing all of them.
- Return just that cropped rectangle.

**Train 1 input**
```text
00000000
00000000
02000000
02200000
00003330
00000000
00000000
```
**Train 1 output**
```text
200000
220000
000333
```
**Train 2 input**
```text
0000000000
0000044000
0000004400
0000000000
0000000000
0070000000
0070000000
0000000000
```
**Train 2 output**
```text
000440
000044
000000
000000
700000
700000
```
**Test input**
```text
000000000
000000080
000000880
066600000
006000000
000000000
000000000
000000000
000000000
```
**Test output**
```text
0000008
0000088
6660000
0600000
```
**Written solution:** Ignore the background and locate the minimal bounding box that contains every nonzero cell. The output is simply that rectangle cropped out of the input, preserving the colors and relative positions inside it.

**Reference program:**
```python
def solve_S10_E3(grid):
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    r1,c1,r2,c2=bbox(cells)
    return [row[c1:c2+1] for row in grid[r1:r2+1]]
```

## S10_E4 — Move Shape to Anchor

**Skills:** translation, bbox alignment, shape preservation

**Scaffold:**
- Separate the anchor color 1 from the object.
- Take the top-left corner of the object's bounding box as its reference point.
- Translate the whole object so that this reference lands on the anchor.

**Train 1 input**
```text
00000000
03000000
03300000
00000000
00000100
00000000
00000000
```
**Train 1 output**
```text
00000000
00000000
00000000
00000000
00000300
00000330
00000000
```
**Train 2 input**
```text
000000000
000001000
000000000
000000000
000000000
044000000
004400000
000000000
```
**Train 2 output**
```text
000000000
000004400
000000440
000000000
000000000
000000000
000000000
000000000
```
**Test input**
```text
0000000000
0000000000
0000000100
0060000000
0666000000
0060000000
0000000000
0000000000
0000000000
```
**Test output**
```text
0000000000
0000000000
0000000060
0000000666
0000000060
0000000000
0000000000
0000000000
0000000000
```
**Written solution:** There is one real object and one anchor marker color 1. Compute the object's bounding box, then shift every object cell by the vector that moves the bounding box's top-left corner onto the anchor cell. Output only the translated object on a blank grid.

**Reference program:**
```python
def solve_S10_E4(grid):
    h,w=dims(grid)
    anchor=next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1)
    obj_cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,1)]
    color=next(v for row in grid for v in row if v not in (0,1))
    r1,c1,r2,c2=bbox(obj_cells)
    dr,dc=anchor[0]-r1, anchor[1]-c1
    out=blank(h,w,0)
    for r,c in obj_cells:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=color
    return out
```

## S10_E5 — Keep Only Internal Objects

**Skills:** connected components, border test, object filtering

**Scaffold:**
- Split the nonzero cells into connected components.
- Check whether each component touches any outer border.
- Erase border-touching components and keep only the fully internal ones.

**Train 1 input**
```text
02000000
02000000
00000000
00003000
00003300
00000040
00000040
```
**Train 1 output**
```text
00000000
00000000
00000000
00003000
00003300
00000000
00000000
```
**Train 2 input**
```text
000000000
000000007
006600007
006600000
000000000
000000000
000000000
220000000
```
**Train 2 output**
```text
000000000
000000000
006600000
006600000
000000000
000000000
000000000
000000000
```
**Test input**
```text
0000080000
0000080000
0000000000
0000000000
0000333000
0000030000
0000000000
0000000040
0000000040
```
**Test output**
```text
0000000000
0000000000
0000000000
0000000000
0000333000
0000030000
0000000000
0000000000
0000000000
```
**Written solution:** Decompose the grid into connected nonzero objects. Any object that touches the top, bottom, left, or right boundary is discarded. The output is a blank grid containing only the components that stay strictly inside the frame.

**Reference program:**
```python
def solve_S10_E5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        if not any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out
```

## S10_E6 — Paint Aligned Midpoints

**Skills:** alignment, odd-distance midpoint, marker placement

**Scaffold:**
- For each color, find its two markers.
- If they lie in the same row or same column with an odd number of steps between them, compute the exact midpoint.
- Paint the midpoint cyan(8) and keep the markers.

**Train 1 input**
```text
000030000
020000020
000000000
000000000
000030000
000000000
```
**Train 1 output**
```text
000030000
020080020
000080000
000000000
000030000
000000000
```
**Train 2 input**
```text
0000000000
0000000060
4000004000
0000000000
0000000000
0000000060
0000000000
```
**Train 2 output**
```text
0000000000
0000000060
4008004000
0000000080
0000000000
0000000060
0000000000
```
**Test input**
```text
00700000000
00000000000
00000003000
00000000000
00009000009
00000000000
00700003000
00000000000
```
**Test output**
```text
00700000000
00000000000
00000003000
00800000000
00009008009
00000000000
00700003000
00000000000
```
**Written solution:** Each relevant color appears exactly twice. If the pair is horizontally or vertically aligned and the gap has a single center cell, paint that center cell cyan(8). The original markers remain in place.

**Reference program:**
```python
def solve_S10_E6(grid):
    out=copyg(grid)
    pos=defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for v, cells in pos.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            if r1==r2 and abs(c1-c2)%2==0:
                out[r1][(c1+c2)//2]=8
            elif c1==c2 and abs(r1-r2)%2==0:
                out[(r1+r2)//2][c1]=8
    return out
```

## S10_E7 — Most-Frequent Color Bar

**Skills:** counting, argmax, constructive output

**Scaffold:**
- Count how many cells each nonzero color occupies.
- Find the color with the highest count.
- Build a bottom-row bar of that color whose length equals the count.

**Train 1 input**
```text
02000300
02000300
02000300
02000000
00000004
00000000
```
**Train 1 output**
```text
00000000
00000000
00000000
00000000
00000000
22220000
```
**Train 2 input**
```text
0000000070
0440000070
0440000070
0400000000
0400000000
0000022000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
4444440000
```
**Test input**
```text
70000000000
70000300000
70000300000
70000300000
70000300000
00000000000
00000000099
00000000000
```
**Test output**
```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
77777000000
```
**Written solution:** Count the number of cells for every nonzero color and select the unique most frequent one. The output is otherwise blank, except that the bottom row begins with a horizontal bar in that winning color whose length equals its cell count.

**Reference program:**
```python
def solve_S10_E7(grid):
    h,w=dims(grid)
    counts=Counter(v for row in grid for v in row if v!=0)
    color=max(sorted(counts), key=lambda v: counts[v])
    n=counts[color]
    out=blank(h,w,0)
    for c in range(min(n,w)):
        out[h-1][c]=color
    return out
```


# Medium

## S10_M1 — One-Mirror Beam

**Skills:** beam tracing, mirror reflection, path painting

**Primitive note:** Uses trace_beam with a single mirror turn.

**Scaffold:**
- Start at the red(2) source and trace right.
- When the beam hits a slash or backslash mirror, rotate the direction accordingly.
- Continue until a wall or the boundary and paint the full traversed path cyan(8).

**Train 1 input**
```text
000000000
000005000
000000000
000000000
000000000
020006000
000000000
```
**Train 1 output**
```text
000000000
000005000
000008000
000008000
000008000
028886000
000000000
```
**Train 2 input**
```text
0000000000
0200700000
0000000000
0000000000
0000000000
0000000000
0000500000
0000000000
```
**Train 2 output**
```text
0000000000
0288700000
0000800000
0000800000
0000800000
0000800000
0000500000
0000000000
```
**Test input**
```text
00000000000
00000000000
00000050000
00000000000
00000000000
00000000000
00000000000
20000060000
00000000000
```
**Test output**
```text
00000000000
00000000000
00000050000
00000080000
00000080000
00000080000
00000080000
28888860000
00000000000
```
**Written solution:** Emit a beam from the red(2) source heading right. The beam travels through zeros, turns once when it encounters the mirror cell, and then continues until it hits a gray(5) wall or leaves the grid. Paint only the beam path cyan(8), leaving the source, mirror, and walls unchanged.

**Reference program:**
```python
def solve_S10_M1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out
```

## S10_M2 — Seeded Room Fill

**Skills:** rectangular frame detection, seed extraction, interior fill

**Scaffold:**
- Detect each rectangular frame made of gray(5).
- Inside every frame there is exactly one seed color.
- Fill the zero interior cells of that room with the seed color.

**Train 1 input**
```text
0000000000
0555500000
0530505550
0500505050
0555505250
0000005050
0000005550
0000000000
```
**Train 1 output**
```text
0000000000
0555500000
0533505550
0533505250
0555505250
0000005250
0000005550
0000000000
```
**Train 2 input**
```text
00000000000
05555505550
05000505650
05040505050
05000505550
05555500000
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
05555505550
05444505650
05444505650
05444505550
05555500000
00000000000
00000000000
00000000000
```
**Test input**
```text
000000000000
000000000000
055550000000
050050055550
057050050050
050050050350
055550050050
000000050050
000000055550
000000000000
```
**Test output**
```text
000000000000
000000000000
055550000000
057750055550
057750053350
057750053350
055550053350
000000053350
000000055550
000000000000
```
**Written solution:** Find every rectangular gray(5) frame. Each one contains a single nonzero seed that determines the room's fill color. Fill all zero cells strictly inside the frame with that seed color, while keeping the frame and seed itself.

**Reference program:**
```python
def solve_S10_M2(grid):
    out=copyg(grid)
    for comp in components(grid, colors={5}):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        frame=set(rect_frame_cells(r1,c1,r2,c2))
        if set(cells)!=frame:
            continue
        seeds=[grid[r][c] for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,5)]
        if len(set(seeds))!=1:
            continue
        fill=seeds[0]
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if out[r][c]==0:
                    out[r][c]=fill
    return out
```

## S10_M3 — Two-Row Recolor Legend

**Skills:** legend decoding, mapping, global recolor

**Scaffold:**
- Read the old colors from the top row and the replacement colors directly below them.
- Build a color-to-color mapping from these pairs.
- Apply the mapping to the body of the grid while leaving unmapped colors alone.

**Train 1 input**
```text
230000000
740000000
000003000
020003000
022000000
000000090
000000000
```
**Train 1 output**
```text
230000000
740000000
000004000
070004000
077000000
000000090
000000000
```
**Train 2 input**
```text
4780000000
6230000000
0000000000
0440000080
0440000080
0000077700
0000000000
0000000000
```
**Train 2 output**
```text
4780000000
6230000000
0000000000
0660000030
0660000030
0000022200
0000000000
0000000000
```
**Test input**
```text
12600000000
98400000000
00000000000
00002200000
01000220000
01000000000
00000000600
00000000660
00000000000
```
**Test output**
```text
12600000000
98400000000
00000000000
00008800000
09000880000
09000000000
00000000400
00000000440
00000000000
```
**Written solution:** The first two rows form a legend: every nonzero entry in row 0 maps to the nonzero entry directly beneath it in row 1. Recolor every occurrence of those old colors in the rows below according to that legend. Any body color not named in the legend stays unchanged.

**Reference program:**
```python
def solve_S10_M3(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        old=grid[0][c]
        new=grid[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    out=copyg(grid)
    for r in range(2,h):
        for c in range(w):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out
```

## S10_M4 — Pick the Object with Area N

**Skills:** counting, component area, selection by measurement

**Scaffold:**
- Count the number of blue(1) dots in the top row to get N.
- Measure the area of each body object.
- Keep only the object whose area equals N, recolored to cyan(8).

**Train 1 input**
```text
0101010000
0000000000
0300003300
0330003300
0000000000
0000033300
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0800000000
0880000000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
01010101000
00000000000
00000000000
03300030000
00330030000
00000033300
00000000300
00000000330
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00000000000
08800000000
00880000000
00000000000
00000000000
00000000000
00000000000
```
**Test input**
```text
010101010100
000000000000
000000000000
000300000000
003330003000
000300003000
000000003300
000003300000
000003300000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000800000000
008880000000
000800000000
000000000000
000000000000
000000000000
000000000000
```
**Written solution:** The top row encodes a number N as the count of blue(1) dots. Among the connected body objects, exactly one has area N. Output a blank grid with that object alone, recolored cyan(8), in its original position.

**Reference program:**
```python
def solve_S10_M4(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    out=blank(h,w,0)
    body=[row[:] for row in grid[1:]]
    comps=components(body, colors={3})
    for comp in comps:
        if len(comp['cells'])==target:
            for r,c in comp['cells']:
                out[r+1][c]=8
            break
    return out
```

## S10_M5 — Column Gravity Compression

**Skills:** column-wise transform, stable compression, gravity

**Scaffold:**
- Process each column independently.
- Read the nonzero cells in their top-to-bottom order.
- Drop them to the bottom of the same column while preserving that order.

**Train 1 input**
```text
02030000
00000070
00400000
00000020
00005000
00000000
```
**Train 1 output**
```text
00000000
00000000
00000000
00000000
00000070
02435020
```
**Train 2 input**
```text
400008000
000200000
600000009
000003000
000000000
000700000
000000000
```
**Train 2 output**
```text
000000000
000000000
000000000
000000000
000000000
400208000
600703009
```
**Test input**
```text
0000700000
0200000000
0000000600
0000000008
0300000000
0000700000
0000000400
0000000000
```
**Test output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0200700600
0300700408
```
**Written solution:** Treat each column as a stack under gravity. Remove the zero gaps, keep the nonzero values in their original top-to-bottom order, and place them flush against the bottom of the column. Do this independently for every column.

**Reference program:**
```python
def solve_S10_M5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        vals=[grid[r][c] for r in range(h) if grid[r][c]!=0]
        start=h-len(vals)
        for i,v in enumerate(vals):
            out[start+i][c]=v
    return out
```

## S10_M6 — Downward Color Shadows

**Skills:** projection, vertical scan, blocking

**Primitive note:** trace_beam is not used directly here, but the logic is a repeated vertical projection.

**Scaffold:**
- Every nonzero non-wall cell projects downward.
- Continue through zeros only, stopping when another nonzero cell or a wall blocks the path.
- Paint the shadow cells with the source's color.

**Train 1 input**
```text
02000000
00000000
00003000
00000000
05000000
00005000
00000000
```
**Train 1 output**
```text
02000000
02000000
02003000
02003000
05003000
00005000
00000000
```
**Train 2 input**
```text
000000700
004000000
000000000
000000000
000000200
000000000
005000500
000000000
```
**Train 2 output**
```text
000000700
004000700
004000700
004000700
004000200
004000200
005000500
000000000
```
**Test input**
```text
0000000000
0000030000
0600000000
0000000000
0000000000
0000040000
0000000000
0500000000
0000050000
```
**Test output**
```text
0000000000
0000030000
0600030000
0600030000
0600030000
0600040000
0600040000
0500040000
0000050000
```
**Written solution:** For each colored source cell, copy its color straight downward through consecutive zeros. The projection stops before any nonzero blocker or wall color 5, and the original cells remain. The result is a set of vertical same-color shadows.

**Reference program:**
```python
def solve_S10_M6(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==0 or v==5:
                continue
            rr=r+1
            while rr<h and grid[rr][c]==0:
                out[rr][c]=v
                rr+=1
    return out
```

## S10_M7 — Two-Panel Difference Mask

**Skills:** panel parsing, cellwise comparison, size change

**Scaffold:**
- Split the input into two equal panels around the gray divider.
- Compare corresponding cells in the left and right panels.
- Output a mask with cyan(8) wherever the two panels differ.

**Train 1 input**
```text
200050200
000050300
004050004
300050000
```
**Train 1 output**
```text
8800
0800
0088
8000
```
**Train 2 input**
```text
02000502000
00000503000
44000544010
00000500000
```
**Train 2 output**
```text
00000
08000
00080
00000
```
**Test input**
```text
3000005000003
0300005000003
0002205220000
0000005000000
```
**Test output**
```text
800008
080008
880880
000000
```
**Written solution:** The grid contains two same-size panels separated by a vertical gray divider. Compare the panels cell by cell. The output is a single panel-sized mask whose cells are cyan(8) exactly where the two inputs differ and black(0) where they match.

**Reference program:**
```python
def solve_S10_M7(grid):
    h,w=dims(grid)
    div=next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    left=[row[:div] for row in grid]
    right=[row[div+1:] for row in grid]
    oh,ow=len(left), len(left[0])
    out=blank(oh,ow,0)
    for r in range(oh):
        for c in range(ow):
            if left[r][c]!=right[r][c]:
                out[r][c]=8
    return out
```


# Hard

## S10_H1 — Two-Mirror Beam Maze

**Skills:** multi-step beam tracing, two reflections, path synthesis

**Primitive note:** Uses trace_beam across two mirror turns.

**Scaffold:**
- Start with the rightward beam from the red(2) source.
- Follow both mirror reflections in sequence.
- Paint the whole route until the beam reaches a wall or exits the grid.

**Train 1 input**
```text
00000000000
00000000000
00000070050
00000000000
00000000000
00000000000
00000000000
02000060000
00000000000
```
**Train 1 output**
```text
00000000000
00000000000
88888870050
00000080000
00000080000
00000080000
00000080000
02888860000
00000000000
```
**Train 2 input**
```text
0000000000
0200700000
0000000000
0000000000
0000000000
0000000000
5000600000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0288700000
0000800000
0000800000
0000800000
0000800000
5888600000
0000000000
0000000000
```
**Test input**
```text
000000000000
000000000000
000000000000
005000070000
000000000000
000000000000
000000000000
000000000000
200000060000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
005888870000
000000080000
000000080000
000000080000
000000080000
288888860000
000000000000
```
**Written solution:** This is the same beam logic as before, but now the path includes two reflections. Trace the beam from the red(2) source as it travels right, turns at the first mirror, turns again at the second mirror, and then continues until blocked. Paint every traversed zero cell cyan(8).

**Reference program:**
```python
def solve_S10_H1(grid):
    out=copyg(grid)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==2:
                for rr,cc in trace_beam(grid, (r,c), direction=(0,1), passable={0}, walls={5}, mirrors={6:'/',7:'\\'}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out
```

## S10_H2 — Rotation-Coded Template Stamps

**Skills:** template extraction, rotation, multi-anchor construction

**Scaffold:**
- Extract the template shape formed by the color-3 cells.
- For every anchor color 1, read the rotation code from the cell immediately to its left.
- Rotate the template accordingly and stamp it with color 8 at that anchor as the template's top-left.

**Train 1 input**
```text
300000000000
330000000000
000000000000
000000000000
021000000000
000000000000
000000041000
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
000000000000
000000000000
000000000000
008000000000
008800000000
000000008800
000000008000
000000000000
000000000000
```
**Train 2 input**
```text
3330000000000
0300000000000
0000000000000
0000000000000
0061000000000
0000000000000
0000000910000
0000000000000
0000000002100
0000000000000
0000000000000
```
**Train 2 output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000800000000
0008880000000
0000000080000
0000000088000
0000000080888
0000000000080
0000000000000
```
**Test input**
```text
33000000000000
03300000000000
00000000000000
00000000000000
00000000000000
00410000000000
00000000000000
00000000091000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00008000000000
00088000000000
00080000000800
00000000008800
00000000008000
00000000000000
00000000000000
```
**Written solution:** The input contains one template made of color 3 and several anchor markers color 1. The cell immediately left of each anchor is a rotation code: 2 means 0°, 4 means 90°, 6 means 180°, and 9 means 270°. Normalize the template, rotate it as requested for each anchor, and stamp the rotated copy in color 8 starting at the anchor cell.

**Reference program:**
```python
def solve_S10_H2(grid):
    h,w=dims(grid)
    tmpl=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    base=norm_cells(tmpl)
    code_to_rot={2:0,4:1,6:2,9:3}
    out=blank(h,w,0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==1 and c-1>=0 and grid[r][c-1] in code_to_rot:
                rot=code_to_rot[grid[r][c-1]]
                pts=rotate_pts(base, rot)
                for dr,dc in pts:
                    rr,cc=r+dr,c+dc
                    if inb(out,rr,cc):
                        out[rr][cc]=8
    return out
```

## S10_H3 — Extract the Unpaired Shape

**Skills:** shape normalization, frequency analysis, odd-one-out

**Scaffold:**
- Break the nonzero cells into objects.
- Normalize each object's shape by translation only.
- Most shapes appear in pairs; output only the unique unpaired shape recolored cyan(8).

**Train 1 input**
```text
0000000000000
0400000400000
0440000440000
0000000000000
0000000000000
0000444000000
0000040000000
0000000000000
0000000000000
```
**Train 1 output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000888000000
0000080000000
0000000000000
0000000000000
```
**Train 2 input**
```text
00000000000000
04000000040000
04000000040000
04400000044000
00000000000000
04400000440000
04400000440000
00000440000000
00000044000000
00000000000000
```
**Train 2 output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000880000000
00000088000000
00000000000000
```
**Test input**
```text
000000000000000
004000000040000
044400000444000
004000000040000
000000000000000
000000000000000
004000000040000
004400000044000
000000440000000
000000044000000
000000000000000
```
**Test output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000880000000
000000088000000
000000000000000
```
**Written solution:** Group cells into connected objects and compare their shapes after removing translation. Every repeated shape occurs exactly twice except one. Keep only that unique shape, in its original position, recolored to cyan(8).

**Reference program:**
```python
def solve_S10_H3(grid):
    comps=components(grid)
    sig_to_comps=defaultdict(list)
    for comp in comps:
        sig=tuple(norm_cells(comp['cells']))
        sig_to_comps[sig].append(comp)
    out=blank(len(grid), len(grid[0]), 0)
    target=None
    for sig, comps2 in sig_to_comps.items():
        if len(comps2)==1:
            target=comps2[0]
            break
    if target is not None:
        for r,c in target['cells']:
            out[r][c]=8
    return out
```

## S10_H4 — Three-Panel Majority Merge

**Skills:** panel parsing, majority vote, color agreement

**Scaffold:**
- Split the input into three equal panels using the two gray dividers.
- Look at the three corresponding cells at every position.
- If some nonzero color appears in at least two panels, output that color; otherwise output 0.

**Train 1 input**
```text
20005200050000
02005000050200
00405004050040
00005000350003
```
**Train 1 output**
```text
2000
0200
0040
0003
```
**Train 2 input**
```text
03000503000503000
00300500000500300
00000500040500040
00020500020500000
```
**Train 2 output**
```text
03000
00300
00040
00020
```
**Test input**
```text
20000520000520000
02000502000500000
00200500000500200
00000500000500000
00030500030500000
```
**Test output**
```text
20000
02000
00200
00000
00030
```
**Written solution:** Parse the three side-by-side panels and compare them position by position. For each cell location, find whether some nonzero color is supported by at least two of the three panels. The output is a single panel that keeps only those majority-supported nonzero cells.

**Reference program:**
```python
def solve_S10_H4(grid):
    h,w=dims(grid)
    divs=[c for c in range(w) if all(grid[r][c]==5 for r in range(h))]
    d1,d2=divs[0],divs[1]
    p1=[row[:d1] for row in grid]
    p2=[row[d1+1:d2] for row in grid]
    p3=[row[d2+1:] for row in grid]
    ph,pw=len(p1), len(p1[0])
    out=blank(ph,pw,0)
    for r in range(ph):
        for c in range(pw):
            vals=[p1[r][c], p2[r][c], p3[r][c]]
            non=[v for v in vals if v!=0]
            counts=Counter(non)
            if counts:
                v,n=max(counts.items(), key=lambda kv: kv[1])
                if n>=2:
                    out[r][c]=v
    return out
```

## S10_H5 — Legend-Driven Room Repaint

**Skills:** legend decoding, frame fill, compositional reasoning

**Scaffold:**
- First decode the old→new color mapping from the top two rows.
- Then find each gray frame and read the seed color inside it.
- Use the mapping to decide the room's fill color, and repaint the whole interior with that mapped color.

**Train 1 input**
```text
230000000000
780000000000
000000000000
055550000000
052050055550
050050050050
055550053050
000000050050
000000055550
000000000000
```
**Train 1 output**
```text
230000000000
780000000000
000000000000
055550000000
057750055550
057750058850
055550058850
000000058850
000000055550
000000000000
```
**Train 2 input**
```text
4780000000000
6230000000000
0000000000000
0555550000000
0500050055550
0504050050050
0500050057050
0555550050050
0000000055550
0000000000000
0000000000000
```
**Train 2 output**
```text
4780000000000
6230000000000
0000000000000
0555550000000
0566650055550
0566650052250
0566650052250
0555550052250
0000000055550
0000000000000
0000000000000
```
**Test input**
```text
12600000000000
98400000000000
00000000000000
00000000000000
05555000000000
05005000555550
05205000500050
05005000506050
05555000500050
00000000500050
00000000555550
00000000000000
```
**Test output**
```text
12600000000000
98400000000000
00000000000000
00000000000000
05555000000000
05885000555550
05885000544450
05885000544450
05555000544450
00000000544450
00000000555550
00000000000000
```
**Written solution:** This combines a legend step with a room-filling step. The top two rows define how seed colors should be translated into output colors. Each framed room contains one seed color from that legend; fill the room interior with the mapped output color rather than the original seed color.

**Reference program:**
```python
def solve_S10_H5(grid):
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        old=grid[0][c]
        new=grid[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    out=copyg(grid)
    body=[row[:] for row in grid[2:]]
    for comp in components(body, colors={5}):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        frame=set(rect_frame_cells(r1,c1,r2,c2))
        if set(cells)!=frame:
            continue
        seeds=[body[r][c] for r in range(r1+1,r2) for c in range(c1+1,c2) if body[r][c] not in (0,5)]
        if len(set(seeds))!=1:
            continue
        seed=seeds[0]
        fill=mapping[seed]
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                out[r+2][c]=fill
    return out
```

## S10_H6 — Complete the Missing Symmetric Quadrant

**Skills:** quadrant parsing, mirroring, partial completion

**Scaffold:**
- Use the gray cross to split the grid into four quadrants.
- The occupied quadrants are mirrored versions of one canonical shape.
- Infer the missing quadrant by applying the appropriate horizontal and/or vertical reflection.

**Train 1 input**
```text
400050400
440054400
000050000
000050000
555555555
440050000
400050000
000050000
000050000
```
**Train 1 output**
```text
400050400
440054400
000050000
000050000
555555555
440054400
400050400
000050000
000050000
```
**Train 2 input**
```text
000050770
000057700
000050000
000050000
555555555
077057700
770050770
000050000
000050000
```
**Train 2 output**
```text
770050770
077057700
000050000
000050000
555555555
077057700
770050770
000050000
000050000
```
**Test input**
```text
06000500000
66600500000
06000500000
00000500000
00000500000
55555555555
06000506000
66600566600
06000506000
00000500000
00000500000
```
**Test output**
```text
06000506000
66600566600
06000506000
00000500000
00000500000
55555555555
06000506000
66600566600
06000506000
00000500000
00000500000
```
**Written solution:** The gray row and column divide the grid into four equal quadrants. The nonempty quadrants are mirrored versions of the same underlying shape. Recover that canonical shape from any filled quadrant and place the correctly mirrored version into the single missing quadrant.

**Reference program:**
```python
def solve_S10_H6(grid):
    h,w=dims(grid)
    divr=next(r for r in range(h) if all(grid[r][c]==5 for c in range(w)))
    divc=next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    qh,qw=divr,divc
    quads={
        'TL': (0,0),
        'TR': (0,divc+1),
        'BL': (divr+1,0),
        'BR': (divr+1,divc+1),
    }
    canon=None
    color=None
    for name,(r0,c0) in quads.items():
        cells=[(r-r0,c-c0) for r in range(r0,r0+qh) for c in range(c0,c0+qw) if grid[r][c] not in (0,5)]
        if not cells:
            continue
        color=grid[r0+cells[0][0]][c0+cells[0][1]]
        pts=norm_cells(cells)
        if name=='TR':
            pts=mirror_h_pts(pts)
        elif name=='BL':
            pts=mirror_v_pts(pts)
        elif name=='BR':
            pts=mirror_v_pts(mirror_h_pts(pts))
        canon=pts
        break
    out=copyg(grid)
    for name,(r0,c0) in quads.items():
        existing=[(r,c) for r in range(r0,r0+qh) for c in range(c0,c0+qw) if grid[r][c] not in (0,5)]
        if existing:
            continue
        pts=canon
        if name=='TR':
            pts=mirror_h_pts(canon)
        elif name=='BL':
            pts=mirror_v_pts(canon)
        elif name=='BR':
            pts=mirror_v_pts(mirror_h_pts(canon))
        for dr,dc in pts:
            out[r0+dr][c0+dc]=color
    return out
```

## S10_H7 — Count, Select, Move, Recolor

**Skills:** counting, component selection, translation composition

**Scaffold:**
- Count the top-row blue(1) dots to obtain the target area.
- Find the body object with exactly that many cells.
- Move it so its bounding-box top-left lands on the anchor color 2, and recolor it cyan(8).

**Train 1 input**
```text
0101010000
0000000000
0300003300
0330003300
0000000000
0000020000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000080000
0000088000
0000000000
```
**Train 2 input**
```text
01010101000
00000000200
00000000000
03300030000
00330030000
00000033300
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000880
00000000088
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Test input**
```text
010101010100
000000000000
000000000000
000300000000
003330003000
000300003000
000000003300
000000200000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000080000
000000888000
000000080000
```
**Written solution:** This combines a counting selector with a transport step. The top row gives a target area N. Choose the body object of color 3 whose area is N, translate it so that its bounding box's top-left corner lands on the anchor cell color 2, recolor it cyan(8), and output only the moved object.

**Reference program:**
```python
def solve_S10_H7(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    anchor=next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2)
    comps=components([row[:] for row in grid[1:]], colors={3})
    chosen=None
    for comp in comps:
        if len(comp['cells'])==target:
            chosen=comp['cells']
            break
    out=blank(h,w,0)
    if chosen is None:
        return out
    abs_cells=[(r+1,c) for r,c in chosen]
    r1,c1,r2,c2=bbox(abs_cells)
    dr,dc=anchor[0]-r1, anchor[1]-c1
    for r,c in abs_cells:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out
```
