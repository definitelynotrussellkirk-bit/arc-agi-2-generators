# ARC-style Puzzle Bank — 21 more puzzles (set 3)

This third bank is organized into 7 easy, 7 medium, and 7 hard puzzles. Each entry includes what it probes, a scaffold, two train pairs, one test pair with solution, a written solution, and a compact Python reference program.

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set3_reference.py`.

## Index

### Easy

- **S3_E1** — Singleton Blue Selector
- **S3_E2** — Leftmost Yellow Object
- **S3_E3** — Vertical Magenta Span
- **S3_E4** — Triple Centers
- **S3_E5** — Horizontal Gray Dominoes
- **S3_E6** — Down-Left Echo
- **S3_E7** — Unique-Color Component

### Medium

- **S3_M1** — Point Reflection Around Pivot
- **S3_M2** — Frame Cross from Inner Dot
- **S3_M3** — Farthest-from-Border Object
- **S3_M4** — Header Column Projection
- **S3_M5** — Reduce Objects to Centers
- **S3_M6** — Bounding-Box Corners
- **S3_M7** — Pivot Rotation Clockwise

### Hard

- **S3_H1** — Shape Legend Recolor
- **S3_H2** — Hole-Count Match
- **S3_H3** — Overlap of Two Template Stamps
- **S3_H4** — Symmetry Completion Inside Frame
- **S3_H5** — Smallest Enclosing Frame Color
- **S3_H6** — Panel Count Selects Object
- **S3_H7** — Size-to-Color Legend

# Easy

## S3_E1 — Singleton Blue Selector

**Skills:** component size filtering, same-size recolor, 4-connectivity

**Scaffold:**
- Extract blue(1) components.
- Identify which blue components are single-cell singleton objects.
- Recolor only those singleton blue cells red(2).

**Train 1 input**
```text
00000000
01000110
00000000
00000000
00100000
00100000
00000010
00000000
```
**Train 1 output**
```text
00000000
02000110
00000000
00000000
00100000
00100000
00000020
00000000
```
**Train 2 input**
```text
000000000
011100000
000000010
000000000
000000000
000001100
000001100
010000000
000000000
```
**Train 2 output**
```text
000000000
011100000
000000020
000000000
000000000
000001100
000001100
020000000
000000000
```
**Test input**
```text
0000000000
0000000010
0100000000
0100000000
0100000000
0000010000
0000000000
0000000110
0010000000
0000000000
```
**Test output**
```text
0000000000
0000000020
0100000000
0100000000
0100000000
0000020000
0000000000
0000000110
0020000000
0000000000
```
**Written solution:** Find every blue(1) connected component of size 1. Recolor those singleton cells red(2). Leave larger blue objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if len(comp['cells'])==1:
            r,c=comp['cells'][0]
            out[r][c]=2
    return out
```

## S3_E2 — Leftmost Yellow Object

**Skills:** spatial ranking, component extraction, object recolor

**Scaffold:**
- Find all yellow(4) connected components.
- Compare their leftmost column positions using each component's bounding box.
- Recolor only the leftmost yellow object green(3).

**Train 1 input**
```text
0000000000
0440044000
0400044000
0000000000
0000000000
0000000400
0000000400
0000000400
```
**Train 1 output**
```text
0000000000
0330044000
0300044000
0000000000
0000000000
0000000400
0000000400
0000000400
```
**Train 2 input**
```text
00000000000
00000000440
00000440440
00000400000
00000400000
00000000000
04440000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000440
00000440440
00000400000
00000400000
00000000000
03330000000
00000000000
00000000000
```
**Test input**
```text
000000000000
000000040000
004400040000
004400040000
000000040000
000000000000
000000000000
000000000440
000000000000
000000000000
```
**Test output**
```text
000000000000
000000040000
003300040000
003300040000
000000040000
000000000000
000000000000
000000000440
000000000000
000000000000
```
**Written solution:** Among all yellow(4) objects, pick the one whose bounding box starts furthest to the left. Recolor that whole object green(3). Leave the other yellow objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,{4},4)
    target=min(comps,key=lambda comp:(bbox(comp['cells'])[1],bbox(comp['cells'])[0]))
    for r,c in target['cells']:
        out[r][c]=3
    return out
```

## S3_E3 — Vertical Magenta Span

**Skills:** column reasoning, line completion, same-color fill

**Scaffold:**
- Inspect each column independently.
- If a column contains exactly two magenta(6) cells with only zeros between them, fill the gap.
- Ignore columns that have more than two magenta cells.

**Train 1 input**
```text
000000000
006000006
000000600
000000006
000000000
006000000
000000606
000000000
```
**Train 1 output**
```text
000000000
006000006
006000600
006000606
006000600
006000600
000000606
000000000
```
**Train 2 input**
```text
0000000000
0600000000
0000000060
0000600000
0000000060
0000000000
0000600000
0600000000
0000000000
```
**Train 2 output**
```text
0000000000
0600000000
0600000060
0600600060
0600600060
0600600000
0600600000
0600000000
0000000000
```
**Test input**
```text
0000000006
0000060000
0060000006
0000000600
0000000000
0000060000
0000000000
0000000600
0060000000
0000000000
```
**Test output**
```text
0000000006
0000060006
0060060006
0060060600
0060060600
0060060600
0060000600
0060000600
0060000000
0000000000
```
**Written solution:** For each column, if there are exactly two magenta(6) cells and the cells between them are blank, fill the whole vertical segment between them with magenta(6). Columns with extra magenta cells are not completed.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for c in range(w):
        rows=[r for r in range(h) if grid[r][c]==6]
        if len(rows)==2 and all(grid[r][c]==0 for r in range(rows[0]+1, rows[1])):
            for r in range(rows[0], rows[1]+1):
                out[r][c]=6
    return out
```

## S3_E4 — Triple Centers

**Skills:** shape detection, local recolor, component normalization

**Scaffold:**
- Find red(2) components.
- Detect which components are exactly 3-cell horizontal bars.
- Recolor only the middle cell of each such bar blue(1).

**Train 1 input**
```text
0000000000
0222000000
0000000020
0000000020
0000222220
0000000000
0000002220
0000000000
```
**Train 1 output**
```text
0000000000
0212000000
0000000020
0000000020
0000222220
0000000000
0000002120
0000000000
```
**Train 2 input**
```text
00000000000
00000000020
00222000020
00000000020
00000000020
00000002220
00000000000
02200000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000020
00212000020
00000000020
00000000020
00000002220
00000000000
02200000000
00000000000
```
**Test input**
```text
000000000000
000002220000
000000000000
000000000000
022200000000
000000000000
000000000020
000000000020
000000222220
000000000000
```
**Test output**
```text
000000000000
000002120000
000000000000
000000000000
021200000000
000000000000
000000000020
000000000020
000000222220
000000000000
```
**Written solution:** Locate every red(2) object that is exactly a horizontal line of length 3. Change only its center cell to blue(1). Leave longer bars and vertical bars unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{2},4):
        if normalize(comp['cells'])==[(0,0),(0,1),(0,2)]:
            r1,c1,_,_=bbox(comp['cells'])
            out[r1][c1+1]=1
    return out
```

## S3_E5 — Horizontal Gray Dominoes

**Skills:** orientation detection, component filtering, recolor

**Scaffold:**
- Find gray(5) connected components.
- Identify which components are exactly 2-cell horizontal dominoes.
- Recolor only those dominoes cyan(8).

**Train 1 input**
```text
0000000000
0550005000
0000005000
0000000000
0000000000
0000555000
0000000055
0000000000
```
**Train 1 output**
```text
0000000000
0880005000
0000005000
0000000000
0000000000
0000555000
0000000088
0000000000
```
**Train 2 input**
```text
000000000
000000055
005500055
000000000
000000500
000000500
000000000
055000000
000000000
```
**Train 2 output**
```text
000000000
000000055
008800055
000000000
000000500
000000500
000000000
088000000
000000000
```
**Test input**
```text
00000000000
00000000550
00000000000
00000000000
00000000000
00055000000
00000000050
00000000050
05555000000
00000000000
```
**Test output**
```text
00000000000
00000000880
00000000000
00000000000
00000000000
00088000000
00000000050
00000000050
05555000000
00000000000
```
**Written solution:** Find every gray(5) object that is exactly two cells wide and one cell tall. Recolor those horizontal dominoes cyan(8). Vertical dominoes and longer gray objects stay gray.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{5},4):
        if normalize(comp['cells'])==[(0,0),(0,1)]:
            for r,c in comp['cells']:
                out[r][c]=8
    return out
```

## S3_E6 — Down-Left Echo

**Skills:** relative placement, local propagation, boundary safety

**Scaffold:**
- Scan for maroon(9) cells.
- For each maroon cell, look one step down and one step left.
- If that target cell is in bounds and blank, paint it gray(5).

**Train 1 input**
```text
000000000
000900000
000000090
000000000
000000000
440009000
440000000
000000000
```
**Train 1 output**
```text
000000000
000900000
005000090
000000500
000000000
440009000
440050000
000000000
```
**Train 2 input**
```text
0000000000
0000000090
0000000000
0000900000
0000000000
0000000000
0090000000
0000001110
0000000000
```
**Train 2 output**
```text
0000000000
0000000090
0000000500
0000900000
0005000000
0000000000
0090000000
0500001110
0000000000
```
**Test input**
```text
0000900000
0000000000
0000000000
0000000000
0000000090
0000000000
3000000000
3000009000
0000000000
0000000000
```
**Test output**
```text
0000900000
0005000000
0000000000
0000000000
0000000090
0000000500
3000000000
3000009000
0000050000
0000000000
```
**Written solution:** Every maroon(9) cell casts a gray(5) echo one cell down-left. Paint that echo only when the target cell is inside the grid and empty.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                rr,cc=r+1,c-1
                if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                    out[rr][cc]=5
    return out
```

## S3_E7 — Unique-Color Component

**Skills:** counting components by color, meta-selection, object recolor

**Scaffold:**
- Group connected components by color.
- Find the color that appears in exactly one component.
- Recolor that entire unique-color component yellow(4).

**Train 1 input**
```text
000000000
011000000
000033000
000033000
000000000
000000100
000000100
000000000
```
**Train 1 output**
```text
000000000
011000000
000044000
000044000
000000000
000000100
000000100
000000000
```
**Train 2 input**
```text
0000000000
0000000010
0066000000
0060000000
0000010000
0000010000
0000000000
0111000000
0000000000
```
**Train 2 output**
```text
0000000000
0000000010
0044000000
0040000000
0000010000
0000010000
0000000000
0111000000
0000000000
```
**Test input**
```text
0000000000
0770000000
0770000200
0000000200
0000000200
0000020000
0000000000
0000000000
0002200000
0000000000
```
**Test output**
```text
0000000000
0440000000
0440000200
0000000200
0000000200
0000020000
0000000000
0000000000
0002200000
0000000000
```
**Written solution:** Count how many connected components each nonzero color forms. Exactly one color appears in only one component; recolor that whole component yellow(4).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp['color']].append(comp)
    target_color=min([color for color,lst in by_color.items() if len(lst)==1])
    for comp in by_color[target_color]:
        for r,c in comp['cells']:
            out[r][c]=4
    return out
```

# Medium

## S3_M1 — Point Reflection Around Pivot

**Skills:** point symmetry, multi-color copying, relative coordinates

**Scaffold:**
- Locate the gray(5) pivot cell.
- For every other nonzero cell, compute its position reflected through the pivot.
- Copy each color to its reflected position while keeping the original cells.

**Train 1 input**
```text
000000000
000003000
002203000
002000000
000050000
000000000
000000000
000000000
000000000
```
**Train 1 output**
```text
000000000
000003000
002203000
002000000
000050000
000000200
000302200
000300000
000000000
```
**Train 2 input**
```text
0000000000
0000000000
0001007000
0001100000
0000000700
0000050000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0001007000
0001100000
0000000700
0000050000
0007000000
0000001100
0000700100
0000000000
```
**Test input**
```text
00000000000
00000000000
04400000000
00400000600
00400006600
00000500000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000000000
04400000000
00400000600
00400006600
00000500000
00660000400
00600000400
00000000440
00000000000
00000000000
```
**Written solution:** Treat the gray(5) cell as the center of a 180° rotation. For every nonzero cell other than the pivot, place the same color at the point-reflected position across that pivot, keeping the original pattern too.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    pivot=next((r,c) for r in range(h) for c in range(w) if grid[r][c]==5)
    pr,pc=pivot
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,5):
                rr,cc=2*pr-r, 2*pc-c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out
```

## S3_M2 — Frame Cross from Inner Dot

**Skills:** frame detection, containment, row-and-column filling

**Scaffold:**
- Detect each rectangular outline frame.
- Find the red(2) dot inside that frame.
- Fill the interior row and interior column through the dot using the frame's color.

**Train 1 input**
```text
000000000000
033333000000
030003000000
030203000000
030003077770
033333072070
000000070070
000000077770
000000000000
```
**Train 1 output**
```text
000000000000
033333000000
030303000000
033333000000
030303077770
033333077770
000000077070
000000077770
000000000000
```
**Train 2 input**
```text
000000000000
044444400000
040000400000
040000400000
040200400000
040000666660
044444602060
000000600060
000000666660
000000000000
```
**Train 2 output**
```text
000000000000
044444400000
040000400000
040000400000
040200400000
040000666660
044444666660
000000606060
000000666660
000000000000
```
**Test input**
```text
0000000000000
0888888800000
0800000800000
0800200800000
0800000800000
0888888333330
0000000300030
0000000302030
0000000300030
0000000333330
0000000000000
```
**Test output**
```text
0000000000000
0888888800000
0800000800000
0800200800000
0800000800000
0888888333330
0000000303030
0000000333330
0000000303030
0000000333330
0000000000000
```
**Written solution:** Inside each rectangle outline, there is one red(2) dot. Draw a cross through that dot—its interior row and interior column—using the color of the enclosing frame.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    frames=[comp for comp in comps if comp['color']!=2 and is_rectangle_outline_cells(comp['cells'])]
    dots=[comp for comp in comps if comp['color']==2 and len(comp['cells'])==1]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        for dot in dots:
            dr,dc=dot['cells'][0]
            if r1<dr<r2 and c1<dc<c2:
                color=frame['color']
                for c in range(c1+1,c2):
                    out[dr][c]=color
                for r in range(r1+1,r2):
                    out[r][dc]=color
    return out
```

## S3_M3 — Farthest-from-Border Object

**Skills:** positional ranking, bounding boxes, object recolor

**Scaffold:**
- Find all blue(1) components.
- For each one, measure its minimum distance to any grid border via its bounding box.
- Recolor the component farthest from the border orange(7).

**Train 1 input**
```text
1100000000
1100001100
0000001100
0000000000
0000110000
0000110000
0000000000
0000000000
0000000000
0000000000
```
**Train 1 output**
```text
1100000000
1100001100
0000001100
0000000000
0000770000
0000770000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
00000111000
00000000000
00000000110
01100000110
01100000000
00000011000
00000011000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000111000
00000000000
00000000110
01100000110
01100000000
00000077000
00000077000
00000000000
00000000000
00000000000
00000000000
```
**Test input**
```text
000000000000
011000001100
011000001100
000000000000
000000000000
000001100000
000001100000
000000000000
001100000000
001100000000
000000000000
000000000000
```
**Test output**
```text
000000000000
011000001100
011000001100
000000000000
000000000000
000007700000
000007700000
000000000000
001100000000
001100000000
000000000000
000000000000
```
**Written solution:** Among the blue(1) objects, choose the one whose bounding box sits deepest inside the grid, farthest from every border. Recolor that object orange(7).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,{1},4)
    h,w=len(grid),len(grid[0])
    target=max(comps,key=lambda comp:(border_distance(comp,h,w), -bbox(comp['cells'])[0], -bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=7
    return out
```

## S3_M4 — Header Column Projection

**Skills:** header interpretation, column projection, conditional recolor

**Scaffold:**
- Read the marked columns from the top row red(2) markers.
- Look down those marked columns only.
- Whenever a blue(1) body cell lies in a marked column, recolor it green(3).

**Train 1 input**
```text
0200200020
0000000000
0110000000
0000100000
0000000010
1000100000
0000000110
0000000000
```
**Train 1 output**
```text
0200200020
0000000000
0310000000
0000300000
0000000030
1000300000
0000000130
0000000000
```
**Train 2 input**
```text
00200200020
00000100000
00100000000
00000100000
01000100000
00000000010
00000000000
00010000010
00000000000
```
**Train 2 output**
```text
00200200020
00000300000
00300000000
00000300000
01000300000
00000000030
00000000000
00010000030
00000000000
```
**Test input**
```text
020000200020
010000000000
000000110000
000000000000
000000000010
000000100000
000000000000
010000000000
000000000110
000000000000
```
**Test output**
```text
020000200020
030000000000
000000310000
000000000000
000000000030
000000300000
000000000000
030000000000
000000000130
000000000000
```
**Written solution:** The top row marks important columns with red(2). Recolor any blue(1) cell that sits under one of those marked columns to green(3), and leave all other body cells unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    marked=[c for c in range(w) if grid[0][c]==2]
    for r in range(1,h):
        for c in marked:
            if grid[r][c]==1:
                out[r][c]=3
    return out
```

## S3_M5 — Reduce Objects to Centers

**Skills:** object abstraction, bounding boxes, grid reduction

**Scaffold:**
- Identify every nonzero connected component.
- Compute the center cell of its bounding box.
- Output only those center cells, using each component's original color.

**Train 1 input**
```text
00000000000
08880000300
08880000300
08880000300
00000000000
00000000000
00000666000
00000000000
00000000000
```
**Train 1 output**
```text
00000000000
00000000000
00800000300
00000000000
00000000000
00000000000
00000060000
00000000000
00000000000
```
**Train 2 input**
```text
000000000000
000000000020
004440000020
000000000020
000000077720
000000077720
000000077700
000000000000
000000000000
000000000000
```
**Train 2 output**
```text
000000000000
000000000000
000400000000
000000000020
000000000000
000000007000
000000000000
000000000000
000000000000
000000000000
```
**Test input**
```text
0000000000000
0000000000000
0088800000000
0088800000000
0088800000000
0000000000400
0000000000400
0000000000400
0000011111000
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0000000000000
0000000000000
0008000000000
0000000000000
0000000000000
0000000000400
0000000000000
0000000100000
0000000000000
0000000000000
```
**Written solution:** Replace each object by a single cell at the center of its bounding box. The output is otherwise blank, and each retained center keeps the original object's color.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,None,4):
        if comp['color']==0: 
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        # assume odd dimensions
        cr,cc=(r1+r2)//2,(c1+c2)//2
        out[cr][cc]=comp['color']
    return out
```

## S3_M6 — Bounding-Box Corners

**Skills:** object abstraction, bounding boxes, corner extraction

**Scaffold:**
- Find every nonzero object.
- Compute its bounding box.
- Output only the four corners of that bounding box in the object's color.

**Train 1 input**
```text
000000000000
033300000000
033300000020
000000000020
000000077020
000000070000
000000070000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
030300000000
030300000020
000000000000
000000077020
000000000000
000000077000
000000000000
000000000000
```
**Train 2 input**
```text
000000000000
004440000000
004440000000
004440000000
000000008880
000000008000
066660008000
066660000000
000000000000
000000000000
```
**Train 2 output**
```text
000000000000
004040000000
000000000000
004040000000
000000008080
000000000000
060060008080
060060000000
000000000000
000000000000
```
**Test input**
```text
0000000000000
0000000000000
0222220000000
0222220000000
0222220000330
0000000000300
0000000000300
0000000000300
0000000555500
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0000000000000
0200020000000
0000000000000
0200020000330
0000000000000
0000000000000
0000000000330
0000000500500
0000000000000
0000000000000
```
**Written solution:** For each object, ignore its interior shape and keep only the four corners of its bounding box. The output grid is blank except for those corner markers.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,None,4):
        if comp['color']==0: continue
        r1,c1,r2,c2=bbox(comp['cells'])
        for rr,cc in [(r1,c1),(r1,c2),(r2,c1),(r2,c2)]:
            out[rr][cc]=comp['color']
    return out
```

## S3_M7 — Pivot Rotation Clockwise

**Skills:** 90-degree rotation, pivot geometry, relative coordinates

**Scaffold:**
- Locate the pivot marker color6.
- For every other nonzero cell, measure its offset from the pivot.
- Rotate that offset 90° clockwise and place the cell there; keep only the rotated copy plus the pivot.

**Train 1 input**
```text
000000000
000000000
003300000
003000000
000060000
000000000
000000000
000000000
000000000
```
**Train 1 output**
```text
000000000
000000000
000003300
000000300
000060000
000000000
000000000
000000000
000000000
```
**Train 2 input**
```text
0000000000
0000000000
0000000000
0070000000
0077700000
0000600000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0000000000
0000077000
0000070000
0000670000
0000000000
0000000000
0000000000
0000000000
```
**Test input**
```text
00000000000
00000000000
00000000000
00002000000
00002200000
00002000000
00000600000
00000000000
00000000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000022200
00000602000
00000000000
00000000000
00000000000
00000000000
```
**Written solution:** Use the color6 pivot as the center of rotation. Rotate the non-pivot pattern 90° clockwise around that pivot, and output only the rotated result together with the pivot.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    pivot=next((r,c) for r in range(h) for c in range(w) if grid[r][c]==6)
    pr,pc=pivot
    out[pr][pc]=6
    for comp in components(grid,None,4):
        if comp['color'] in (0,6): continue
        for r,c in comp['cells']:
            dr,dc=r-pr,c-pc
            rr,cc=pr+dc, pc-dr
            out[rr][cc]=comp['color']
    return out
```

# Hard

## S3_H1 — Shape Legend Recolor

**Skills:** legend extraction, shape matching, cross-band transfer

**Scaffold:**
- Above the separator row, read the colored exemplar shapes as a legend.
- Normalize each exemplar shape and record its color.
- Below the separator, recolor each gray(5) shape with the color of the matching exemplar.

**Train 1 input**
```text
000000000000
022200440770
000000400770
000000000000
000000000000
000000000000
005550000000
000000055000
000000050000
000000000550
000000000550
000000000000
```
**Train 1 output**
```text
000000000000
022200440770
000000400770
000000000000
000000000000
000000000000
002220000000
000000044000
000000040000
000000000770
000000000770
000000000000
```
**Train 2 input**
```text
0000000000000
0880030066600
0880030006000
0000030000000
0000000000000
0000000000000
0000000000000
0555000000000
0050000055000
0000050055000
0000050000000
0000050000000
0000000000000
```
**Train 2 output**
```text
0000000000000
0880030066600
0880030006000
0000030000000
0000000000000
0000000000000
0000000000000
0666000000000
0060000088000
0000030088000
0000030000000
0000030000000
0000000000000
```
**Test input**
```text
00000000000000
01111007702200
00000007702000
00000000002000
00000000000000
00000000000000
00000000000000
00550000000000
00550000000000
00000000555500
00005500000000
00005000000000
00005000000000
00000000000000
```
**Test output**
```text
00000000000000
01111007702200
00000007702000
00000000002000
00000000000000
00000000000000
00000000000000
00770000000000
00770000000000
00000000111100
00002200000000
00002000000000
00002000000000
00000000000000
```
**Written solution:** The top band is a legend: each colored shape defines a shape→color mapping. In the lower band, gray(5) copies of those shapes must be recolored according to the matching legend shape.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    sep=choose_separator_row(grid)
    legend=components([row[:] for row in grid[:sep]], None, 4)
    mapping={}
    for comp in legend:
        mapping[tuple(normalize(comp['cells']))]=comp['color']
    out=copyg(grid)
    for comp in components([row[:] for row in grid[sep+1:]], {5}, 4):
        shape=tuple(normalize(comp['cells']))
        color=mapping[shape]
        for r,c in comp['cells']:
            out[sep+1+r][c]=color
    return out
```

## S3_H2 — Hole-Count Match

**Skills:** counting holes, component analysis, header count selection

**Scaffold:**
- Count how many marker cells appear in the top row.
- For each green(3) object below, count how many enclosed holes it contains.
- Recolor the object whose hole count matches the top-row marker count red(2).

**Train 1 input**
```text
0010000000000
0000000000000
0330033303330
0330030303030
0000033303330
0000000003030
0000000003330
0000000000000
0000000000000
0000000000000
```
**Train 1 output**
```text
0000000000000
0000000000000
0330022203330
0330020203030
0000022203330
0000000003030
0000000003330
0000000000000
0000000000000
0000000000000
```
**Train 2 input**
```text
01010000000000
00000000000000
03330033300000
03030030300330
03330033300330
03030000000000
03330000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 2 output**
```text
00000000000000
00000000000000
02220033300000
02020030300330
02220033300330
02020000000000
02220000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test input**
```text
000000000000
000000000000
033300330000
030300330000
033300003330
000000003030
000000003330
000000003030
000000003330
000000000000
```
**Test output**
```text
000000000000
000000000000
033300220000
030300220000
033300003330
000000003030
000000003330
000000003030
000000003330
000000000000
```
**Written solution:** Use the number of top-row markers as a target hole-count. Among the green(3) objects below, find the one with that many enclosed holes and recolor it red(2). The top-row markers disappear in the output.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    k=sum(1 for v in grid[0] if v==1)
    for c in range(len(grid[0])):
        if out[0][c]==1:
            out[0][c]=0
    candidates=[comp for comp in components(grid,{3},4) if all(r>0 for r,c in comp['cells'])]
    target=next(comp for comp in candidates if count_holes_in_component(grid, comp)==k)
    for r,c in target['cells']:
        out[r][c]=2
    return out
```

## S3_H3 — Overlap of Two Template Stamps

**Skills:** template extraction, translation, set intersection

**Scaffold:**
- Extract the green(3) template object's normalized shape.
- Stamp one copy with its top-left at the color1 anchor and another with its top-left at the color2 anchor.
- Output only the cells where the two stamped copies overlap, in cyan(8).

**Train 1 input**
```text
000000000000
033300000000
003000000000
000000000000
000000000000
000001000000
000000200000
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
000000000000
000000000000
000000800000
000000000000
000000000000
000000000000
```
**Train 2 input**
```text
0000000000000
0000000033000
0000000030000
0000000030000
0000000000000
0010000000000
0020000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0080000000000
0080000000000
0000000000000
0000000000000
0000000000000
```
**Test input**
```text
00000000000000
00000000000000
00333300000000
00000000000000
00000000000000
00000000000000
00000102000000
00000000000000
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
00000000000000
00000008800000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Written solution:** Take the green(3) template shape, place one copy at the color1 anchor and another at the color2 anchor, then keep only the overlapping cells. The output is otherwise blank and the overlap is colored cyan(8).

**Reference program:**
```python
def solve(grid):
    # template color 3, anchors 1 and 2. output overlap of template stamped at anchor positions, color 8
    h,w=len(grid),len(grid[0])
    template=max(components(grid,{3},4), key=lambda comp: len(comp['cells']))
    shape=normalize(template['cells'])
    anchors={}
    for r in range(h):
        for c in range(w):
            if grid[r][c] in (1,2):
                anchors[grid[r][c]]=(r,c)
    stamps=[]
    for marker in (1,2):
        r0,c0=anchors[marker]
        stamps.append(set((r0+dr,c0+dc) for dr,dc in shape))
    overlap=stamps[0] & stamps[1]
    out=[[0]*w for _ in range(h)]
    for r,c in overlap:
        if 0<=r<h and 0<=c<w:
            out[r][c]=8
    return out
```

## S3_H4 — Symmetry Completion Inside Frame

**Skills:** inferred symmetry axis, frame geometry, multi-color mirroring

**Scaffold:**
- Detect the large enclosing frame.
- Infer its vertical symmetry axis from the frame's bounding box.
- Mirror the interior non-frame pattern across that axis to complete the right side.

**Train 1 input**
```text
0000000000000
0000000000000
0044444444400
0042000000400
0040200000400
0043000000400
0040070000400
0040000000400
0044444444400
0000000000000
0000000000000
```
**Train 1 output**
```text
0000000000000
0000000000000
0044444444400
0042000002400
0040200020400
0043000003400
0040070700400
0040000000400
0044444444400
0000000000000
0000000000000
```
**Train 2 input**
```text
00000000000000
00000000000000
00666666666000
00600000006000
00610000006000
00601000006000
00600000006000
00600300006000
00603000006000
00666666666000
00000000000000
00000000000000
```
**Train 2 output**
```text
00000000000000
00000000000000
00666666666000
00600000006000
00610000016000
00601000106000
00600000006000
00600303006000
00603000306000
00666666666000
00000000000000
00000000000000
```
**Test input**
```text
000000000000000
000000000000000
008888888888800
008000000000800
008200000000800
008004000000800
008000000000800
008040000000800
008000100000800
008000000000800
008888888888800
000000000000000
000000000000000
```
**Test output**
```text
000000000000000
000000000000000
008888888888800
008000000000800
008200000002800
008004000400800
008000000000800
008040000040800
008000101000800
008000000000800
008888888888800
000000000000000
000000000000000
```
**Written solution:** The frame defines a vertical axis of symmetry. Mirror the interior colored pattern across the frame's center line so the contents become bilaterally symmetric inside the frame.

**Reference program:**
```python
def solve(grid):
    # frame defines vertical symmetry axis; mirror nonzero non-frame cells from whichever side exists
    out=copyg(grid)
    frame=max([comp for comp in components(grid,None,4) if is_rectangle_outline_cells(comp['cells'])], key=lambda comp: len(comp['cells']))
    r1,c1,r2,c2=bbox(frame['cells'])
    axis=(c1+c2)//2
    for r in range(r1+1,r2):
        for c in range(c1+1,c2+1):
            v=grid[r][c]
            if v!=0 and v!=frame['color']:
                mc=2*axis-c
                if c1<mc<c2:
                    out[r][mc]=v
    return out
```

## S3_H5 — Smallest Enclosing Frame Color

**Skills:** nested containment, frame hierarchy, smallest-enclosing selection

**Scaffold:**
- Detect all rectangular outline frames.
- For each white marker cell, list the frames that contain it.
- Recolor the marker with the color of the smallest enclosing frame.

**Train 1 input**
```text
0000000000000
0333333333330
0310000000030
0300777770030
0300700070030
0300701070030
0300700070030
0300777770030
0300000000030
0333333333330
0000000000000
```
**Train 1 output**
```text
0000000000000
0333333333330
0330000000030
0300777770030
0300700070030
0300707070030
0300700070030
0300777770030
0300000000030
0333333333330
0000000000000
```
**Train 2 input**
```text
00000000000000
04444444444440
04000000000140
04066666666040
04061000006040
04060888006040
04060818006040
04060888006040
04066666666040
04000000000040
04444444444440
00000000000000
```
**Train 2 output**
```text
00000000000000
04444444444440
04000000000440
04066666666040
04066000006040
04060888006040
04060888006040
04060888006040
04066666666040
04000000000040
04444444444440
00000000000000
```
**Test input**
```text
000000000000000
000000000000000
022222222200000
021000007777777
020555557200007
020500057200007
020501057201007
020500057200007
020555557200007
020000007777777
022222222200000
000000000000000
000000000000000
```
**Test output**
```text
000000000000000
000000000000000
022222222200000
021000007777777
020555557200007
020500057200007
020505057207007
020500057200007
020555557200007
020000007777777
022222222200000
000000000000000
000000000000000
```
**Written solution:** Each marker lies inside one or more nested frames. Recolor each marker to the color of the smallest frame that still encloses it, not the outermost one.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    frames=[comp for comp in components(grid,None,4) if is_rectangle_outline_cells(comp['cells'])]
    dots=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1]
    for r,c in dots:
        enclosing=[]
        for frame in frames:
            r1,c1,r2,c2=bbox(frame['cells'])
            if r1<r<r2 and c1<c<c2:
                area=(r2-r1+1)*(c2-c1+1)
                enclosing.append((area,frame['color']))
        if enclosing:
            color=min(enclosing)[1]
            out[r][c]=color
    return out
```

## S3_H6 — Panel Count Selects Object

**Skills:** two-panel reasoning, count matching, object selection

**Scaffold:**
- Use the zero separator column to split left and right panels.
- Count the marker cells in the left panel.
- In the right panel, find the object whose cell count equals that number, then draw its bounding-box outline in cyan(8).

**Train 1 input**
```text
00000000000000
01000000000000
00000003300000
00100003000000
00000000000000
00000000033000
00010000033000
00000000000000
00000003333300
00000000000000
```
**Train 1 output**
```text
00000000000000
01000000000000
00000008800000
00100008800000
00000000000000
00000000033000
00010000033000
00000000000000
00000003333300
00000000000000
```
**Train 2 input**
```text
000000000000000
010000000000000
001000003300000
000000003300000
010000000000000
000000000000000
000000000033000
000100000030000
000000033333000
000000000000000
000000000000000
```
**Train 2 output**
```text
000000000000000
010000000000000
001000008800000
000000008800000
010000000000000
000000000000000
000000000033000
000100000030000
000000033333000
000000000000000
000000000000000
```
**Test input**
```text
0000000000000000
0100000000000000
0010000003333300
0100000000000000
0001000000000000
0000000000000000
0000000000330000
0000000000330000
0010000000000000
0000000033000000
0000000030000000
0000000000000000
```
**Test output**
```text
0000000000000000
0100000000000000
0010000008888800
0100000000000000
0001000000000000
0000000000000000
0000000000330000
0000000000330000
0010000000000000
0000000033000000
0000000030000000
0000000000000000
```
**Written solution:** The left panel supplies a number via its marker count. In the right panel, select the object whose size matches that number and mark it by drawing a cyan(8) outline around its bounding box.

**Reference program:**
```python
def solve(grid):
    h,w=len(grid),len(grid[0])
    sep=choose_separator_col(grid)
    k=sum(1 for r in range(h) for c in range(sep) if grid[r][c]==1)
    right=[[grid[r][c] for c in range(sep+1,w)] for r in range(h)]
    target=None
    for comp in components(right,{3},4):
        if len(comp['cells'])==k:
            target=comp; break
    out=copyg(grid)
    r1,c1,r2,c2=bbox(target['cells'])
    c1+=sep+1; c2+=sep+1
    for c in range(c1,c2+1):
        out[r1][c]=8; out[r2][c]=8
    for r in range(r1,r2+1):
        out[r][c1]=8; out[r][c2]=8
    return out
```

## S3_H7 — Size-to-Color Legend

**Skills:** legend decoding, size matching, object recolor

**Scaffold:**
- Read the top-row legend as contiguous color groups.
- Use each group's length as a size and its color as the output color.
- Recolor each gray(5) object below according to the legend entry whose group length matches that object's size.

**Train 1 input**
```text
02200444066660
00000000000000
00000000000000
05500000000000
00000000000000
00000550000000
00000500000000
00000000005500
00000000005500
00000000000000
```
**Train 1 output**
```text
02200444066660
00000000000000
00000000000000
02200000000000
00000000000000
00000440000000
00000400000000
00000000006600
00000000006600
00000000000000
```
**Train 2 input**
```text
077700330088880
000000000000000
000000000055000
000000000055000
000000000000000
005500000000000
005000000000000
000000000000000
000000055000000
000000000000000
000000000000000
```
**Train 2 output**
```text
077700330088880
000000000000000
000000000088000
000000000088000
000000000000000
007700000000000
007000000000000
000000000000000
000000033000000
000000000000000
000000000000000
```
**Test input**
```text
0111100666002200
0000000000000000
0000000000005500
0000000000000000
0000000000000000
0550000000000000
0550000000000000
0000000000000000
0000000055000000
0000000050000000
0000000000000000
0000000000000000
```
**Test output**
```text
0111100666002200
0000000000000000
0000000000002200
0000000000000000
0000000000000000
0110000000000000
0110000000000000
0000000000000000
0000000066000000
0000000060000000
0000000000000000
0000000000000000
```
**Written solution:** The top row is a size→color legend: the length of each contiguous colored run tells you an object size, and the run's color is what that size should become. Recolor each gray(5) object below using the legend entry that matches its cell count.

**Reference program:**
```python
def solve(grid):
    # top legend row contains groups of 2's,4's,6's? Actually groups of 1 markers? Use contiguous markers of colors as legend? 
    # Let's define top row has groups of color markers where group length encodes size and color itself is output color.
    # bottom gray objects of sizes matching lengths; recolor by matching size.
    h,w=len(grid),len(grid[0])
    # parse top row contiguous groups nonzero
    top=grid[0]
    mapping={}
    c=0
    while c<w:
        if top[c]==0:
            c+=1; continue
        color=top[c]
        start=c
        while c<w and top[c]==color:
            c+=1
        length=c-start
        mapping[length]=color
    out=copyg(grid)
    for comp in components(grid[1:],{5},4):
        size=len(comp['cells'])
        color=mapping[size]
        for r,c in comp['cells']:
            out[1+r][c]=color
    return out
```
