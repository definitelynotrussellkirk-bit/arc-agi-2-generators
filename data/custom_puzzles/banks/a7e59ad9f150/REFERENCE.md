# ARC-style Puzzle Bank — 21 more puzzles (set 2)

This second bank is organized into 7 easy, 7 medium, and 7 hard puzzles. Each entry includes what it probes, a scaffold, two train pairs, one test pair with solution, a written solution, and a compact Python reference program.

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set2_reference.py`.

## Index

### Easy

- **S2_E1** — Vertical Bar Selector
- **S2_E2** — Smallest Green Object
- **S2_E3** — Horizontal Span Fill
- **S2_E4** — Diagonal Echo
- **S2_E5** — Missing Cyan Corner
- **S2_E6** — L-Triomino Selector
- **S2_E7** — Square Keeper

### Medium

- **S2_M1** — Nearest Marker Object
- **S2_M2** — Frame Filled by Inner Dot
- **S2_M3** — Bounding-Box Outlines
- **S2_M4** — Header/Side Intersections
- **S2_M5** — Ring Selector
- **S2_M6** — Template Copies from Anchors
- **S2_M7** — Diagonal-Corner Rectangle Fill

### Hard

- **S2_H1** — Missing Quadrant Completion
- **S2_H2** — Marker Count Chooses Nth Largest
- **S2_H3** — Rotate by Corner Code
- **S2_H4** — Rotation-Coded Template Copies
- **S2_H5** — Header Pair Recolor Map
- **S2_H6** — Equality Matrix from Headers
- **S2_H7** — Odd-Shape-Out Border

# Easy

## S2_E1 — Vertical Bar Selector

**Skills:** orientation detection, component filtering, same-size recolor

**Scaffold:**
- Find all blue(1) connected components.
- Normalize each one.
- Recolor only the 3-cell vertical bars red(2).

**Train 1 input**
```text
00000000
01000000
01001110
01000000
00000000
00011100
00000000
00000000
```
**Train 1 output**
```text
00000000
02000000
02001110
02000000
00000000
00011100
00000000
00000000
```
**Train 2 input**
```text
000000000
001000010
001000010
001000010
000000000
011100000
000000000
000111000
000000000
```
**Train 2 output**
```text
000000000
002000020
002000020
002000020
000000000
011100000
000000000
000111000
000000000
```
**Test input**
```text
0000000000
0100001110
0100000000
0100000000
0000000100
0111000100
0000000100
0000000000
0011100000
0000000000
```
**Test output**
```text
0000000000
0200001110
0200000000
0200000000
0000000200
0111000200
0000000200
0000000000
0011100000
0000000000
```
**Written solution:** Find every blue(1) object that is exactly a 3-cell vertical line. Recolor those cells red(2). Leave horizontal blue bars unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid, {1}, 4):
        if normalize(comp['cells'])==[(0,0),(1,0),(2,0)]:
            for r,c in comp['cells']:
                out[r][c]=2
    return out
```

## S2_E2 — Smallest Green Object

**Skills:** component size ranking, object recolor

**Scaffold:**
- Extract green(3) components.
- Compare their sizes.
- Recolor the unique smallest one magenta(6).

**Train 1 input**
```text
000000000
033300000
003000000
000000000
000033000
000003000
000000000
000000033
000000000
```
**Train 1 output**
```text
000000000
033300000
003000000
000000000
000033000
000003000
000000000
000000066
000000000
```
**Train 2 input**
```text
0000000000
0030000000
0000000000
0003330000
0000000000
0000033000
0000003000
0000000000
0333300000
0000000000
```
**Train 2 output**
```text
0000000000
0060000000
0000000000
0003330000
0000000000
0000033000
0000003000
0000000000
0333300000
0000000000
```
**Test input**
```text
00000000000
00033000000
00000000000
00333300000
00003000000
00000000000
00000000330
00000000300
00000000300
00000000000
00000000000
```
**Test output**
```text
00000000000
00066000000
00000000000
00333300000
00003000000
00000000000
00000000330
00000000300
00000000300
00000000000
00000000000
```
**Written solution:** Among all green(3) objects, select the smallest connected component and recolor it magenta(6). Keep the larger green objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,{3},4)
    smallest=min(comps,key=lambda comp: len(comp['cells']))
    for r,c in smallest['cells']:
        out[r][c]=6
    return out
```

## S2_E3 — Horizontal Span Fill

**Skills:** row-wise reasoning, endpoint completion, segment drawing

**Scaffold:**
- Scan each row for orange(7) endpoints.
- If a row has two endpoints with only black cells between them, fill the span.
- Do this independently for each row.

**Train 1 input**
```text
000000000
070000070
000000000
007000700
000000000
000000000
```
**Train 1 output**
```text
000000000
077777770
000000000
007777700
000000000
000000000
```
**Train 2 input**
```text
0000000000
0070000000
0000000000
0700000070
0000000000
0007000070
0000000000
```
**Train 2 output**
```text
0000000000
0070000000
0000000000
0777777770
0000000000
0007777770
0000000000
```
**Test input**
```text
00000000000
07000000070
00000000000
00070070000
00000000000
00700000000
00000000000
00000070070
```
**Test output**
```text
00000000000
07777777770
00000000000
00077770000
00000000000
00700000000
00000000000
00000077770
```
**Written solution:** Whenever a row contains two orange(7) endpoints with only black(0) cells between them, fill the whole horizontal segment between those endpoints with orange(7). Rows without such a pair stay unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        cols=[c for c in range(w) if grid[r][c]==7]
        if len(cols)==2 and all(grid[r][c]==0 for c in range(cols[0]+1, cols[1])):
            for c in range(cols[0],cols[1]+1):
                out[r][c]=7
    return out
```

## S2_E4 — Diagonal Echo

**Skills:** local translation, cell creation, boundary handling

**Scaffold:**
- Look at every red(2) cell.
- Paint a yellow(4) echo one step down-right when that target cell is inside the grid and currently black.
- Keep the original red cells.

**Train 1 input**
```text
20000000
00020000
00000000
02000000
00000020
00000000
00000000
00000000
```
**Train 1 output**
```text
20000000
04020000
00004000
02000000
00400020
00000004
00000000
00000000
```
**Train 2 input**
```text
000000000
002000000
000000000
000020000
000000000
200000000
000000000
000000020
000000000
```
**Train 2 output**
```text
000000000
002000000
000400000
000020000
000004000
200000000
040000000
000000020
000000004
```
**Test input**
```text
00000000000
00200000000
00000000000
00002000000
00000000000
20000000000
00000000000
00000002000
00000000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00200000000
00040000000
00002000000
00000400000
20000000000
04000000000
00000002000
00000000400
00000000000
00000000000
```
**Written solution:** Each red(2) cell creates a yellow(4) copy one step diagonally down and right, but only if that target location is inside the grid and empty. The original red cells remain.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]==2 and r+1<h and c+1<w and grid[r+1][c+1]==0:
                out[r+1][c+1]=4
    return out
```

## S2_E5 — Missing Cyan Corner

**Skills:** 2x2 local pattern completion, same-color fill

**Scaffold:**
- Inspect every 2x2 window.
- If it contains exactly three cyan(8) cells and one black cell, fill the missing corner.
- Apply this to all disjoint or overlapping windows.

**Train 1 input**
```text
000000000
088000000
080000000
000000000
000008800
000008000
000000000
```
**Train 1 output**
```text
000000000
088000000
088000000
000000000
000008800
000008800
000000000
```
**Train 2 input**
```text
0000000000
0008800000
0000800000
0000000000
0000000000
0000000880
0000000080
0000000000
```
**Train 2 output**
```text
0000000000
0008800000
0008800000
0000000000
0000000000
0000000880
0000000880
0000000000
```
**Test input**
```text
00000000000
00000880000
00000800000
00000000000
00880000000
00800000000
00000000000
00000000880
00000000080
```
**Test output**
```text
00000000000
00000880000
00000880000
00000000000
00880000000
00880000000
00000000000
00000000880
00000000880
```
**Written solution:** Complete every almost-full 2x2 cyan(8) square: when three corners are cyan(8) and the fourth corner is black(0), fill that missing corner with cyan(8).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h-1):
        for c in range(w-1):
            cells=[(r,c),(r+1,c),(r,c+1),(r+1,c+1)]
            vals=[grid[rr][cc] for rr,cc in cells]
            if vals.count(8)==3 and vals.count(0)==1:
                rr,cc=cells[vals.index(0)]
                out[rr][cc]=8
    return out
```

## S2_E6 — L-Triomino Selector

**Skills:** shape recognition, component normalization, recoloring

**Scaffold:**
- Find yellow(4) components of size 3.
- Use the bounding box to distinguish L-triominoes from straight 3-cell bars.
- Recolor only the L-shapes green(3).

**Train 1 input**
```text
000000000
044000000
040000000
000000000
000444000
000000000
000000044
000000004
000000000
```
**Train 1 output**
```text
000000000
033000000
030000000
000000000
000444000
000000000
000000033
000000003
000000000
```
**Train 2 input**
```text
0000000000
0004400000
0004000000
0000000000
0000444000
0000000000
4400000000
0400000000
0000000000
```
**Train 2 output**
```text
0000000000
0003300000
0003000000
0000000000
0000444000
0000000000
3300000000
0300000000
0000000000
```
**Test input**
```text
00000000000
04400000000
04000044400
00000000000
00000000000
00004400000
00000400000
00000000000
00000004440
00000000000
```
**Test output**
```text
00000000000
03300000000
03000044400
00000000000
00000000000
00003300000
00000300000
00000000000
00000004440
00000000000
```
**Written solution:** Among the yellow(4) objects of size 3, identify the ones shaped like an L rather than a straight line. Recolor the L-triominoes green(3) and leave the straight yellow bars unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{4},4):
        if len(comp['cells'])==3:
            r1,c1,r2,c2=bbox(comp['cells'])
            if r2-r1==1 and c2-c1==1: # 2x2 bbox => L triomino
                for r,c in comp['cells']:
                    out[r][c]=3
    return out
```

## S2_E7 — Square Keeper

**Skills:** shape filtering, component erasure, solid block detection

**Scaffold:**
- Extract magenta(6) components.
- Keep only components whose normalized shape is a solid 2x2 square.
- Erase all other magenta objects.

**Train 1 input**
```text
000000000
066000000
060000000
000000000
000066000
000066000
000000000
000000666
```
**Train 1 output**
```text
000000000
000000000
000000000
000000000
000066000
000066000
000000000
000000000
```
**Train 2 input**
```text
0000000000
0660000660
0660000060
0000000000
0006660000
0000000000
0000006600
0000006600
0000000000
```
**Train 2 output**
```text
0000000000
0660000000
0660000000
0000000000
0000000000
0000000000
0000006600
0000006600
0000000000
```
**Test input**
```text
00000000000
00660000000
00660066000
00000006000
00000000000
00000666000
00000000000
00000000066
00000000066
00000000000
```
**Test output**
```text
00000000000
00660000000
00660000000
00000000000
00000000000
00000000000
00000000000
00000000066
00000000066
00000000000
```
**Written solution:** Keep only the magenta(6) objects that are perfect solid 2x2 squares. Remove every other magenta shape, such as lines or L-shapes.

**Reference program:**
```python
def solve(grid):
    out=[[0]*len(grid[0]) for _ in grid]
    for comp in components(grid,{6},4):
        if normalize(comp['cells'])==[(0,0),(0,1),(1,0),(1,1)]:
            for r,c in comp['cells']:
                out[r][c]=6
    return out
```

# Medium

## S2_M1 — Nearest Marker Object

**Skills:** distance ranking, component selection, object recolor

**Scaffold:**
- Find the magenta(6) marker cell.
- Measure each blue(1) object's Manhattan distance to the marker.
- Recolor the nearest blue object orange(7).

**Train 1 input**
```text
0000000000
0110000000
0010000000
0000000000
0000000110
0000000110
0000000000
0000060000
0000000000
0001100000
```
**Train 1 output**
```text
0000000000
0110000000
0010000000
0000000000
0000000110
0000000110
0000000000
0000060000
0000000000
0007700000
```
**Train 2 input**
```text
00000000000
00001100000
00000100000
00000000000
01000000000
01000000000
00000000000
00000000000
00000000110
00000000600
00000000000
```
**Train 2 output**
```text
00000000000
00001100000
00000100000
00000000000
01000000000
01000000000
00000000000
00000000000
00000000770
00000000600
00000000000
```
**Test input**
```text
000000000000
011100000000
001000000000
000000000000
000000001000
000000011100
000000001000
000000000000
000000000000
000110000000
000006000000
000000000000
```
**Test output**
```text
000000000000
011100000000
001000000000
000000000000
000000001000
000000011100
000000001000
000000000000
000000000000
000770000000
000006000000
000000000000
```
**Written solution:** Use the magenta(6) marker as a reference point. Among the blue(1) objects, find the one with the smallest Manhattan distance to that marker and recolor that whole object orange(7).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    marker=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==6:
                marker=(r,c)
    comps=components(grid,{1},4)
    target=min(comps,key=lambda comp: manhattan_to_comp(marker, comp))
    for r,c in target['cells']:
        out[r][c]=7
    return out
```

## S2_M2 — Frame Filled by Inner Dot

**Skills:** enclosure, color transfer, rectangle-outline detection

**Scaffold:**
- Find gray(5) rectangular frames.
- Inside each frame, identify the single non-gray colored dot.
- Fill the frame's interior with that dot color while keeping the frame.

**Train 1 input**
```text
00000000000
05555000000
05005000000
05035000000
05555000000
00000000000
00005555500
00005000500
00005020500
00005555500
00000000000
```
**Train 1 output**
```text
00000000000
05555000000
05335000000
05335000000
05555000000
00000000000
00005555500
00005222500
00005222500
00005555500
00000000000
```
**Train 2 input**
```text
000000000000
055555000000
050005000000
050405000000
050005000000
055555000000
000000000000
000000055550
000000050050
000000050150
000000055550
000000000000
```
**Train 2 output**
```text
000000000000
055555000000
054445000000
054445000000
054445000000
055555000000
000000000000
000000055550
000000051150
000000051150
000000055550
000000000000
```
**Test input**
```text
0000000000000
0555500000000
0500500000000
0502500000000
0555500000000
0000000000000
0000005555500
0000005000500
0000005000500
0000005004500
0000005555500
0000000000000
```
**Test output**
```text
0000000000000
0555500000000
0522500000000
0522500000000
0555500000000
0000000000000
0000005555500
0000005444500
0000005444500
0000005444500
0000005555500
0000000000000
```
**Written solution:** Each gray(5) rectangle is a frame around a single colored dot. Fill the inside of the frame with the dot's color, keeping the gray border intact.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{5},4):
        if not is_rectangle_outline_cells(comp['cells']):
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        inner_colors=set()
        dot_color=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c] not in (0,5):
                    inner_colors.add(grid[r][c])
        if len(inner_colors)!=1:
            continue
        dot_color=next(iter(inner_colors))
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                out[r][c]=dot_color
    return out
```

## S2_M3 — Bounding-Box Outlines

**Skills:** object abstraction, bounding boxes, shape replacement

**Scaffold:**
- Find each red(2) component.
- Compute its bounding box.
- Replace the component by the outline of that full bounding box.

**Train 1 input**
```text
0000000000
0220000000
0200000000
0200000000
0000000000
0000002200
0000000200
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0220000000
0220000000
0220000000
0000000000
0000002200
0000002200
0000000000
0000000000
```
**Train 2 input**
```text
00000000000
00022200000
00002000000
00000000000
00000000000
02200000000
00220000000
00020000000
00000000000
```
**Train 2 output**
```text
00000000000
00022200000
00022200000
00000000000
00000000000
02220000000
02020000000
02220000000
00000000000
```
**Test input**
```text
000000000000
000220000000
000020000000
000000000000
000000222000
000000020000
000000000000
022000000000
020000000000
020000000000
000000000000
```
**Test output**
```text
000000000000
000220000000
000220000000
000000000000
000000222000
000000222000
000000000000
022000000000
022000000000
022000000000
000000000000
```
**Written solution:** For every red(2) object, ignore its exact interior shape and replace it with the red outline of its minimal bounding rectangle.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,{2},4):
        r1,c1,r2,c2=bbox(comp['cells'])
        for c in range(c1,c2+1):
            out[r1][c]=2; out[r2][c]=2
        for r in range(r1,r2+1):
            out[r][c1]=2; out[r][c2]=2
    return out
```

## S2_M4 — Header/Side Intersections

**Skills:** Cartesian product reasoning, marker extraction, sparse grid generation

**Scaffold:**
- Read blue(1) markers from the top row and red(2) markers from the left column.
- Form every row/column intersection between those markers.
- Color each such interior intersection yellow(4) and keep the markers.

**Train 1 input**
```text
0010010000
0000000000
2000000000
0000000000
2000000000
0000000000
2000000000
0000000000
```
**Train 1 output**
```text
0010010000
0000000000
2040040000
0000000000
2040040000
0000000000
2040040000
0000000000
```
**Train 2 input**
```text
00010010000
00000000000
20000000000
00000000000
00000000000
20000000000
00000000000
20000000000
00000000000
00000000000
```
**Train 2 output**
```text
00010010000
00000000000
20040040000
00000000000
00000000000
20040040000
00000000000
20040040000
00000000000
00000000000
```
**Test input**
```text
010010010000
000000000000
000000000000
200000000000
000000000000
200000000000
000000000000
000000000000
200000000000
000000000000
```
**Test output**
```text
010010010000
000000000000
000000000000
240040040000
000000000000
240040040000
000000000000
000000000000
240040040000
000000000000
```
**Written solution:** The top row marks columns with blue(1), and the left column marks rows with red(2). Fill every intersection of a marked row and a marked column with yellow(4), while leaving the original markers in place.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    cols=[c for c in range(1,w) if grid[0][c]==1]
    rows=[r for r in range(1,h) if grid[r][0]==2]
    for r in rows:
        for c in cols:
            out[r][c]=4
    return out
```

## S2_M5 — Ring Selector

**Skills:** hole detection, outline recognition, object recolor

**Scaffold:**
- Find green(3) connected components.
- Identify which ones are rectangular outlines rather than solid shapes or open shapes.
- Recolor only the ring-like outline components orange(7).

**Train 1 input**
```text
0000000000
0333000000
0303000000
0333000000
0000000000
0000033000
0000033000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0777000000
0707000000
0777000000
0000000000
0000033000
0000033000
0000000000
0000000000
```
**Train 2 input**
```text
00000000000
00033300000
00030300000
00033300000
00000000000
03300000000
00300000000
00300000000
00000000000
00000033300
00000030300
00000033300
```
**Train 2 output**
```text
00000000000
00077700000
00070700000
00077700000
00000000000
03300000000
00300000000
00300000000
00000000000
00000077700
00000070700
00000077700
```
**Test input**
```text
000000000000
033300000000
030300000000
033300000000
000000000000
000000000000
000000333300
000000300300
000000333300
000000000000
000033000000
000003000000
000003000000
```
**Test output**
```text
000000000000
077700000000
070700000000
077700000000
000000000000
000000000000
000000777700
000000700700
000000777700
000000000000
000033000000
000003000000
000003000000
```
**Written solution:** Recolor the green(3) objects that form closed rectangular rings to orange(7). Solid blocks and open green shapes stay green.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{3},4):
        if is_rectangle_outline_cells(comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=7
    return out
```

## S2_M6 — Template Copies from Anchors

**Skills:** template extraction, translation, shape copying

**Scaffold:**
- Treat the largest red(2) object as the template.
- Normalize its shape.
- For every blue(1) anchor cell, stamp a blue copy of the template with the anchor as the template's top-left origin.

**Train 1 input**
```text
000000000000
020000010000
022000000000
002000000000
000000000000
000000001000
000000000000
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
020000010000
022000011000
002000001000
000000000000
000000001000
000000001100
000000000100
000000000000
000000000000
```
**Train 2 input**
```text
0000000000000
0020000000000
0222000000000
0000000000000
0000000000000
0000000010000
0000000000000
0000100000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**
```text
0000000000000
0020000000000
0222000000000
0000000000000
0000000000000
0000000011000
0000000011100
0000110000000
0000111000000
0000000000000
0000000000000
```
**Test input**
```text
00000000000000
00000000010000
00200000000000
00200000000000
00220000000000
00000000000000
00000000000000
00000000001000
00000100000000
00000000000000
00000000000000
00000000000000
```
**Test output**
```text
00000000000000
00000000010000
00200000010000
00200000011000
00220000000000
00000000000000
00000000000000
00000000001000
00000100001000
00000100001100
00000110000000
00000000000000
```
**Written solution:** Use the largest red(2) object as a template shape. At each blue(1) anchor, place a blue copy of that same shape aligned by its top-left corner. Keep the original red template too.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    reds=components(grid,{2},4)
    template=max(reds,key=lambda comp: len(comp['cells']))
    tmpl=normalize(template['cells'])
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==1:
                for dr,dc in tmpl:
                    rr,cc=r+dr,c+dc
                    out[rr][cc]=1
    return out
```

## S2_M7 — Diagonal-Corner Rectangle Fill

**Skills:** pairing by color, rectangle completion, full-region fill

**Scaffold:**
- Find colors that appear exactly twice as isolated corner markers.
- Treat the two cells of a given color as opposite corners of a rectangle.
- Fill the whole rectangle with that color.

**Train 1 input**
```text
0000000000
0200000000
0000000000
0000200000
0000000000
0000000300
0000000000
0000000003
0000000000
```
**Train 1 output**
```text
0000000000
0222200000
0222200000
0222200000
0000000000
0000000333
0000000333
0000000333
0000000000
```
**Train 2 input**
```text
00000000000
00040000000
00000000000
00000000400
00000000000
05000000000
00000000000
00000500000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00044444400
00044444400
00044444400
00000000000
05555500000
05555500000
05555500000
00000000000
00000000000
```
**Test input**
```text
000000000000
000020000000
000000000000
000000020000
000000000000
000000000300
000000000000
000000000003
000000000000
000500000000
000000000000
000000050000
```
**Test output**
```text
000000000000
000022220000
000022220000
000022220000
000000000000
000000000333
000000000333
000000000333
000000000000
000555550000
000555550000
000555550000
```
**Written solution:** For each color that appears exactly twice, interpret the two cells as diagonal corners of a rectangle and fill the entire rectangle with that color.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    positions=defaultdict(list)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                positions[v].append((r,c))
    # only colors with exactly two singleton cells (as entire color count 2)
    for color,cells in positions.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            for r in range(min(r1,r2),max(r1,r2)+1):
                for c in range(min(c1,c2),max(c1,c2)+1):
                    out[r][c]=color
    return out
```

# Hard

## S2_H1 — Missing Quadrant Completion

**Skills:** motif extraction, layout reasoning, template placement

**Scaffold:**
- Use the all-black separator row and column to split the grid into four quadrants.
- Find the repeated motif that appears in three quadrants.
- Copy that motif into the empty quadrant at the corresponding position.

**Train 1 input**
```text
00000000000
06600006600
06000006000
00000000000
00000000000
00000000000
00000000000
06600000000
06000000000
00000000000
00000000000
```
**Train 1 output**
```text
00000000000
06600006600
06000006000
00000000000
00000000000
00000000000
00000000000
06600006600
06000006000
00000000000
00000000000
```
**Train 2 input**
```text
00000000600
00000006600
00000000600
00000000000
00000000000
00000000000
00600000600
06600006600
00600000600
00000000000
00000000000
```
**Train 2 output**
```text
00600000600
06600006600
00600000600
00000000000
00000000000
00000000000
00600000600
06600006600
00600000600
00000000000
00000000000
```
**Test input**
```text
06000000000
06000000000
06600000000
00000000000
00000000000
00000000000
06000006000
06000006000
06600006600
00000000000
00000000000
```
**Test output**
```text
06000006000
06000006000
06600006600
00000000000
00000000000
00000000000
06000006000
06000006000
06600006600
00000000000
00000000000
```
**Written solution:** The grid is divided into four equal quadrants by a blank row and column. Three quadrants contain the same motif in the same relative position. Copy that motif into the missing quadrant.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    sr,sc=find_zero_separator_rowcol(grid)
    quads=[
        ((0,0),(sr,sc)),
        ((0,sc+1),(sr,w)),
        ((sr+1,0),(h,sc)),
        ((sr+1,sc+1),(h,w)),
    ]
    shapes=[]
    empty_idx=None
    color=None
    for i,((r0,c0),(r1,c1)) in enumerate(quads):
        cells=[]
        cols=set()
        for r in range(r0,r1):
            for c in range(c0,c1):
                if grid[r][c]!=0:
                    cells.append((r-r0,c-c0))
                    cols.add(grid[r][c])
        if cells:
            shapes.append((i,sorted(cells), next(iter(cols))))
        else:
            empty_idx=i
    # choose common shape from first non-empty (assumed same)
    shape=shapes[0][1]
    color=shapes[0][2]
    out=copyg(grid)
    (r0,c0),(r1,c1)=quads[empty_idx]
    for dr,dc in shape:
        out[r0+dr][c0+dc]=color
    return out
```

## S2_H2 — Marker Count Chooses Nth Largest

**Skills:** counting, ranking by size, meta-selection

**Scaffold:**
- Count the blue(1) markers in the top row.
- Rank the green(3) objects below by size from largest to smallest.
- Recolor the Nth largest object red(2), where N is the marker count.

**Train 1 input**
```text
01010000000
00000000000
03333000000
00030000000
00000000000
00000033000
00000003000
00000000000
00000000033
00000000000
```
**Train 1 output**
```text
01010000000
00000000000
03333000000
00030000000
00000000000
00000022000
00000002000
00000000000
00000000033
00000000000
```
**Train 2 input**
```text
001010100000
000000000000
033333000000
000030000000
000000000000
000000333000
000000030000
000000000000
000000000330
000000000300
000330000000
000000000000
```
**Train 2 output**
```text
001010100000
000000000000
033333000000
000030000000
000000000000
000000333000
000000030000
000000000000
000000000220
000000000200
000330000000
000000000000
```
**Test input**
```text
0100100000000
0000000000000
0003333000000
0000300000000
0000000000000
0033300000000
0003000000000
0000000000000
0000000000033
0000000000000
0000003300000
0000003000000
0000000000000
```
**Test output**
```text
0100100000000
0000000000000
0003333000000
0000300000000
0000000000000
0022200000000
0002000000000
0000000000000
0000000000033
0000000000000
0000003300000
0000003000000
0000000000000
```
**Written solution:** The number of blue(1) markers in the top row tells you which green(3) object to select after sorting by size from largest to smallest. Recolor that chosen object red(2).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    k=sum(1 for v in grid[0] if v==1)
    comps=[comp for comp in components(grid,{3},4) if all(r>0 for r,c in comp['cells'])]
    comps_sorted=sorted(comps,key=lambda comp: (-len(comp['cells']), min(comp['cells'])))
    target=comps_sorted[k-1]
    for r,c in target['cells']:
        out[r][c]=2
    return out
```

## S2_H3 — Rotate by Corner Code

**Skills:** symbolic code reading, rotation, shape normalization

**Scaffold:**
- Find the red(2) template object and the single cyan(8) corner code.
- Use the corner position as the rotation instruction: top-left=0°, top-right=90°, bottom-right=180°, bottom-left=270° clockwise.
- Replace the template by its rotated version, anchored at the same top-left bounding-box position.

**Train 1 input**
```text
000000008
000000000
002000000
002000000
002200000
000000000
000000000
000000000
000000000
```
**Train 1 output**
```text
000000008
000000000
002220000
002000000
000000000
000000000
000000000
000000000
000000000
```
**Train 2 input**
```text
0000000000
0000000000
0000200000
0000200000
0002200000
0000000000
0000000000
0000000000
0000000000
8000000000
```
**Train 2 output**
```text
0000000000
0000000000
0002220000
0000020000
0000000000
0000000000
0000000000
0000000000
0000000000
8000000000
```
**Test input**
```text
0000000000
0000000000
0000000000
0022000000
0020000000
0020000000
0000000000
0000000000
0000000000
0000000008
```
**Test output**
```text
0000000000
0000000000
0000000000
0002000000
0002000000
0022000000
0000000000
0000000000
0000000000
0000000008
```
**Written solution:** A cyan(8) corner marker encodes how much to rotate the red(2) shape: top-left means no rotation, top-right means 90° clockwise, bottom-right means 180°, and bottom-left means 270°. Rotate the red template accordingly.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    # keep marker
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    k=None
    for (r,c),rot in corners.items():
        if grid[r][c]==8:
            k=rot
            out[r][c]=8
            break
    comp=max(components(grid,{2},4), key=lambda comp: len(comp['cells']))
    r1,c1,r2,c2=bbox(comp['cells'])
    rot_cells=rotate_norm(normalize(comp['cells']), k)
    for dr,dc in rot_cells:
        out[r1+dr][c1+dc]=2
    return out
```

## S2_H4 — Rotation-Coded Template Copies

**Skills:** template extraction, rotation codes, multi-anchor stamping

**Scaffold:**
- Treat the largest gray(5) object as the template.
- Anchor colors 1,2,3,4 mean stamp a copy rotated by 0°, 90°, 180°, 270° clockwise, respectively.
- Place each rotated copy using the anchor cell as the template's top-left origin and color the copy with the anchor's color.

**Train 1 input**
```text
00000000000000
05000000010000
05500000000000
00500000000000
00000000000000
00000000000000
00000000020000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**
```text
00000000000000
05000000010000
05500000011000
00500000001000
00000000000000
00000000000000
00000000022200
00000000022000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 2 input**
```text
00000000000000
00500000000000
05550000000000
00000000000000
00000000000000
00000000300000
00000000000000
00040000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**
```text
00000000000000
00500000000000
05550000000000
00000000000000
00000000000000
00000000333000
00000000030000
00044000000000
00044000000000
00004000000000
00000000000000
00000000000000
```
**Test input**
```text
0000000000000000
0000000000100000
0050000000000000
0050000000000000
0055000000000000
0000000000000000
0000000000000000
0000400002000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Test output**
```text
0000000000000000
0000000000100000
0050000000100000
0050000000110000
0055000000000000
0000000000000000
0000000000000000
0000404002220000
0000444002000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Written solution:** Use the largest gray(5) object as a template. Each colored anchor cell tells you to place a rotated copy of that template: color 1 = 0°, 2 = 90°, 3 = 180°, 4 = 270°. The stamped copy uses the anchor's own color.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    template=max(components(grid,{5},4), key=lambda comp: len(comp['cells']))
    tmpl=normalize(template['cells'])
    color_to_rot={1:0,2:1,3:2,4:3}
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v in color_to_rot:
                rot_cells=rotate_norm(tmpl, color_to_rot[v])
                for dr,dc in rot_cells:
                    rr,cc=r+dr,c+dc
                    out[rr][cc]=v
    return out
```

## S2_H5 — Header Pair Recolor Map

**Skills:** legend reading, color remapping, symbolic control

**Scaffold:**
- Read the nonzero colors in the top row from left to right as consecutive pairs.
- Each pair means old-color -> new-color.
- Apply those recolor mappings to the body of the grid, leaving the header row itself unchanged.

**Train 1 input**
```text
2073040000
0000000000
0220003300
0200000300
0000000000
0003300000
0000300000
0000000000
```
**Train 1 output**
```text
2073040000
0000000000
0770004400
0700000400
0000000000
0004400000
0000400000
0000000000
```
**Train 2 input**
```text
10540200000
00000000000
01100044400
00100004000
00000000000
00011000000
00000000000
00000000400
```
**Train 2 output**
```text
10540200000
00000000000
05500022200
00500002000
00000000000
00055000000
00000000000
00000000200
```
**Test input**
```text
601208000000
000000000000
066000022000
006000002000
000000000000
000660000000
000000000000
000000002200
000000000000
```
**Test output**
```text
601208000000
000000000000
011000088000
001000008000
000000000000
000110000000
000000000000
000000008800
000000000000
```
**Written solution:** The top row is a legend made of consecutive nonzero color pairs. Each pair defines a recolor rule from the first color to the second. Recolor the body using those mappings, but do not change the header row.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    nonzero=[v for v in grid[0] if v!=0]
    # pair consecutive nonzeros
    pairs=list(zip(nonzero[::2], nonzero[1::2]))
    mapping={}
    for a,b in pairs:
        mapping[a]=b
    for r in range(1,len(grid)):
        for c in range(len(grid[0])):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out
```

## S2_H6 — Equality Matrix from Headers

**Skills:** relational grid construction, header decoding, symbol matching

**Scaffold:**
- Read the color labels across the top row and down the left column.
- For each interior cell, compare its row label and column label.
- Fill the cell with that color only when the two labels match; otherwise leave it black.

**Train 1 input**
```text
012301
100000
200000
300000
100000
200000
```
**Train 1 output**
```text
012301
110001
202000
300300
110001
202000
```
**Train 2 input**
```text
0455400
4000000
5000000
4000000
5000000
0000000
4000000
```
**Train 2 output**
```text
0455400
4400400
5055000
4400400
5055000
0000000
4400400
```
**Test input**
```text
02362000
20000000
30000000
60000000
20000000
60000000
30000000
00000000
```
**Test output**
```text
02362000
22002000
30300000
60060000
22002000
60060000
30300000
00000000
```
**Written solution:** The top row and left column act as headers. Each interior cell becomes colored only when its row-header color matches its column-header color, and then it takes that shared color.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=copyg(grid)
    top=grid[0]
    left=[grid[r][0] for r in range(h)]
    for r in range(1,h):
        for c in range(1,w):
            out[r][c]=top[c] if top[c]==left[r] else 0
    return out
```

## S2_H7 — Odd-Shape-Out Border

**Skills:** shape comparison, frequency counting, derived border drawing

**Scaffold:**
- Extract all green(3) objects and normalize their shapes.
- Find the shape that appears only once while another shape repeats.
- Draw a yellow(4) border one cell outside the unique object's bounding box, keeping the original objects.

**Train 1 input**
```text
00000000000000
03000000300000
03300000330000
00000000000000
00000000000000
00000000000000
00000030000000
00000333000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**
```text
00000000000000
03000000300000
03300000330000
00000000000000
00000000000000
00004444400000
00004030400000
00004333400000
00004444400000
00000000000000
00000000000000
00000000000000
```
**Train 2 input**
```text
000000000000000
000000000000000
003300000000000
003000000000000
000000000000000
000000003330000
000000000300000
000000000000000
003300000000000
003000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**
```text
000000000000000
000000000000000
003300000000000
003000000000000
000000044444000
000000043334000
000000040304000
000000044444000
003300000000000
003000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test input**
```text
0000000000000000
0030000000000000
0033000000000000
0000000000000000
0000000000000000
0000000000000000
0000000030000000
0000000033000000
0000000030000000
0030000000000000
0033000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Test output**
```text
0000000000000000
0030000000000000
0033000000000000
0000000000000000
0000000000000000
0000000444400000
0000000430400000
0000000433400000
0000000430400000
0030000444400000
0033000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Written solution:** Compare the green(3) objects by shape. Two of them share the same normalized form, while one is different. Draw a yellow(4) rectangular border around the unique object's bounding box, one cell away from it.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,{3},4)
    shape_counts=Counter(tuple(normalize(comp['cells'])) for comp in comps)
    target=None
    for comp in comps:
        sh=tuple(normalize(comp['cells']))
        if shape_counts[sh]==1:
            target=comp
            break
    r1,c1,r2,c2=bbox(target['cells'])
    # draw border outside bbox one cell away
    for c in range(c1-1,c2+2):
        out[r1-1][c]=4
        out[r2+1][c]=4
    for r in range(r1-1,r2+2):
        out[r][c1-1]=4
        out[r][c2+1]=4
    return out
```
