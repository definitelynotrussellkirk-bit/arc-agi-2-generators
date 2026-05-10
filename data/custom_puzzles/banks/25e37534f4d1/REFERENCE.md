# ARC-style Puzzle Bank — 21 more puzzles (set 4)

This fourth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. Each entry includes what it probes, a scaffold, two train pairs, one test pair with solution, a written solution, and a compact Python reference program.

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set4_reference.py`.

## Index

### Easy

- **S4_E1** — 2x2 Square Selector
- **S4_E2** — Lowest Red Object
- **S4_E3** — Vertical Endpoint Fill
- **S4_E4** — Ring Centers
- **S4_E5** — T-Tetromino Selector
- **S4_E6** — Left-Border Blue Objects
- **S4_E7** — Diagonal Domino Selector

### Medium

- **S4_M1** — Closest to Grid Center
- **S4_M2** — Parallel Bars Become Solid
- **S4_M3** — Main-Diagonal Mirror
- **S4_M4** — Marker Count Matches Size
- **S4_M5** — Rectangle to Center Cross
- **S4_M6** — Four Corners to Perimeter
- **S4_M7** — T to Plus Completion

### Hard

- **S4_H1** — Four-Quadrant Symmetry
- **S4_H2** — Rotation-Coded Frames
- **S4_H3** — Hole Count Match
- **S4_H4** — Count Comparison Matrix
- **S4_H5** — Pivot 4-Way Rotation
- **S4_H6** — Colorized Template Frames
- **S4_H7** — Prototype Legend Recolor

# Easy

## S4_E1 — 2x2 Square Selector

**Skills:** shape recognition, same-size recolor, 4-connectivity

**Scaffold:**
- Find all blue(1) connected components.
- Normalize each shape.
- Recolor only the exact 2x2 squares red(2).

**Train 1 input**
```text
00000000
01100100
01100100
00000110
00000000
01111000
00000000
00000000
```
**Train 1 output**
```text
00000000
02200100
02200100
00000110
00000000
01111000
00000000
00000000
```
**Train 2 input**
```text
000000000
010000110
010000110
010000000
010011100
000001000
011000000
011000000
000000000
```
**Train 2 output**
```text
000000000
010000220
010000220
010000000
010011100
000001000
022000000
022000000
000000000
```
**Test input**
```text
0000000000
0110000000
0110001000
0000001000
0000101100
0000100000
0000100110
0000000110
0111100000
0000000000
```
**Test output**
```text
0000000000
0220000000
0220001000
0000001000
0000101100
0000100000
0000100220
0000000220
0111100000
0000000000
```
**Written solution:** Find every blue(1) object that is exactly a 2x2 square. Recolor those square cells red(2). Leave the other blue objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if normalize(comp['cells'])==sorted(square2):
            for r,c in comp['cells']:
                out[r][c]=2
    return out
```

## S4_E2 — Lowest Red Object

**Skills:** vertical ranking, component extraction, object recolor

**Scaffold:**
- Extract red(2) connected components.
- Compare how low their bounding boxes reach.
- Recolor only the lowest red object green(3).

**Train 1 input**
```text
0000000000
0220000000
0220000000
0000000000
0000022200
0000000000
0000000000
0000002000
0000002000
0000002200
```
**Train 1 output**
```text
0000000000
0220000000
0220000000
0000000000
0000022200
0000000000
0000000000
0000003000
0000003000
0000003300
```
**Train 2 input**
```text
00000000000
00000000200
00000000200
00222000200
00020000000
00000000000
00002200000
00002200000
00000000000
```
**Train 2 output**
```text
00000000000
00000000200
00000000200
00222000200
00020000000
00000000000
00003300000
00003300000
00000000000
```
**Test input**
```text
00000000000
00000222200
00000000000
00000000000
02000000000
02000000000
02200000000
00000000200
00000000200
00000000200
00000000200
```
**Test output**
```text
00000000000
00000222200
00000000000
00000000000
02000000000
02000000000
02200000000
00000000300
00000000300
00000000300
00000000300
```
**Written solution:** Among all red(2) objects, choose the one whose bounding box reaches furthest downward. Recolor that whole object green(3). Keep the higher red objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,{2},4)
    target=max(comps,key=lambda comp:(bbox(comp['cells'])[2], bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=3
    return out
```

## S4_E3 — Vertical Endpoint Fill

**Skills:** line completion, column reasoning, same-color span fill

**Scaffold:**
- Look for columns containing exactly two orange(7) markers.
- Treat the two markers as the endpoints of a vertical segment.
- Fill every cell between them orange(7).

**Train 1 input**
```text
00000000
07000000
00000700
00000000
00000000
07000000
00000700
00000000
```
**Train 1 output**
```text
00000000
07000000
07000700
07000700
07000700
07000700
00000700
00000000
```
**Train 2 input**
```text
000700000
000000000
000000070
000000000
000700000
000000000
000000000
000000000
000000070
```
**Train 2 output**
```text
000700000
000700000
000700070
000700070
000700070
000000070
000000070
000000070
000000070
```
**Test input**
```text
0000000070
0070000000
0000000000
0000000070
0000000000
0000070000
0000000000
0070000000
0000000000
0000070000
```
**Test output**
```text
0000000070
0070000070
0070000070
0070000070
0070000000
0070070000
0070070000
0070070000
0000070000
0000070000
```
**Written solution:** Whenever a column contains exactly two orange(7) cells, fill the whole vertical segment between them orange(7), including the endpoints.

**Reference program:**
```python
def solve(grid):
    return fill_between_vertical_markers(grid,7)
```

## S4_E4 — Ring Centers

**Skills:** local enclosure, 3x3 motif detection, center fill

**Scaffold:**
- Scan for gray(5) 3x3 rings.
- Check that the center of the ring is black(0).
- Fill each such center with cyan(8).

**Train 1 input**
```text
00000055
05550055
05050000
05550000
00005550
00005050
00005550
00000000
```
**Train 1 output**
```text
00000055
05550055
05850000
05550000
00005550
00005850
00005550
00000000
```
**Train 2 input**
```text
0000000000
0000000000
0055500000
0050500000
0055500000
0000005550
0000005050
0000005550
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0055500000
0058500000
0055500000
0000005550
0000005850
0000005550
0000000000
```
**Test input**
```text
0000000000
0000055500
0000050500
0000055500
0000000000
0000000000
0555005550
0505005050
0555005550
0000000000
```
**Test output**
```text
0000000000
0000055500
0000058500
0000055500
0000000000
0000000000
0555005550
0585005850
0555005550
0000000000
```
**Written solution:** Find every gray(5) 3x3 ring and place a cyan(8) cell in its center. Leave the ring itself unchanged.

**Reference program:**
```python
def solve(grid):
    return ring3_centers(grid,5,8)
```

## S4_E5 — T-Tetromino Selector

**Skills:** shape matching, rotation handling, component recolor

**Scaffold:**
- Extract green(3) 4-connected components.
- Recognize which components are T-tetrominoes in any rotation.
- Recolor only those T-shaped objects magenta(6).

**Train 1 input**
```text
0000000000
0333003000
0030003000
0000003300
0000000000
0000000000
0033330000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0666003000
0060003000
0000003300
0000000000
0000000000
0033330000
0000000000
0000000000
```
**Train 2 input**
```text
0000000000
0000000330
0030000330
0330000000
0030000000
0000003000
0000003300
0000003000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000000330
0060000330
0660000000
0060000000
0000006000
0000006600
0000006000
0000000000
0000000000
```
**Test input**
```text
00000000000
00030000000
00333000003
00000000003
00000000003
00000000003
00000033300
03000003000
03000000000
03300000000
00000000000
```
**Test output**
```text
00000000000
00060000000
00666000003
00000000003
00000000003
00000000003
00000066600
03000006000
03000000000
03300000000
00000000000
```
**Written solution:** Find every green(3) object shaped like a T tetromino, allowing rotations. Recolor those cells magenta(6) and leave the non-T green objects unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{3},4):
        if tuple(normalize(comp['cells'])) in T_shapes:
            for r,c in comp['cells']:
                out[r][c]=6
    return out
```

## S4_E6 — Left-Border Blue Objects

**Skills:** border contact, component filtering, same-size recolor

**Scaffold:**
- Find blue(1) connected components.
- Test whether each component touches the left border.
- Recolor only the left-border components yellow(4).

**Train 1 input**
```text
000000000
100000000
100001000
100001000
000001100
110000000
110000000
000000000
```
**Train 1 output**
```text
000000000
400000000
400001000
400001000
000001100
440000000
440000000
000000000
```
**Train 2 input**
```text
1111000000
0000000000
0000000110
0000000110
0000000000
1000000000
1000000000
1100000000
0000000000
```
**Train 2 output**
```text
4444000000
0000000000
0000000110
0000000110
0000000000
4000000000
4000000000
4400000000
0000000000
```
**Test input**
```text
0000000000
1100000000
1100011100
0000001000
1000000000
1000000000
1000000000
1000000000
0000001110
0000000000
```
**Test output**
```text
0000000000
4400000000
4400011100
0000001000
4000000000
4000000000
4000000000
4000000000
0000001110
0000000000
```
**Written solution:** Recolor every blue(1) object that touches the left edge of the grid to yellow(4). Keep the blue objects that do not touch the left edge unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if any(c==0 for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=4
    return out
```

## S4_E7 — Diagonal Domino Selector

**Skills:** 8-connectivity, tiny shape classification, selective recolor

**Scaffold:**
- Extract red(2) components using 8-connectivity.
- Identify 2-cell diagonal dominoes.
- Recolor only those diagonal dominoes cyan(8).

**Train 1 input**
```text
00000000
02000220
00200000
00000000
00000000
02000200
02000020
00000000
```
**Train 1 output**
```text
00000000
08000220
00800000
00000000
00000000
02000800
02000080
00000000
```
**Train 2 input**
```text
000000020
000000002
000000000
002000000
002000000
000000000
000002200
020000000
002000000
```
**Train 2 output**
```text
000000080
000000008
000000000
002000000
002000000
000000000
000002200
080000000
008000000
```
**Test input**
```text
0000000000
0200000200
0020000200
0000000000
0000200000
0000020000
0000000000
0022000200
0000000020
0000000000
```
**Test output**
```text
0000000000
0800000200
0080000200
0000000000
0000800000
0000080000
0000000000
0022000800
0000000080
0000000000
```
**Written solution:** Using diagonal adjacency, find every red(2) component that consists of exactly two diagonally touching cells. Recolor those components cyan(8). Leave horizontal and vertical dominoes red.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{2},8):
        if len(comp['cells'])==2 and tuple(normalize(comp['cells'])) in diag2_shapes:
            for r,c in comp['cells']:
                out[r][c]=8
    return out
```

# Medium

## S4_M1 — Closest to Grid Center

**Skills:** spatial ranking, bounding-box centers, object recolor

**Scaffold:**
- Find all green(3) objects.
- Compute each object's bounding-box center.
- Recolor the object whose center is closest to the center of the whole grid orange(7).

**Train 1 input**
```text
00000000000
03300000000
03300000000
00000000000
00003000000
00003000000
00003300030
00000000030
00000000030
00000000030
00000000000
```
**Train 1 output**
```text
00000000000
03300000000
03300000000
00000000000
00007000000
00007000000
00007700030
00000000030
00000000030
00000000030
00000000000
```
**Train 2 input**
```text
000000000000
000000033330
000000000000
000000000000
000003300000
000003300000
000000000000
030000000000
030000000000
033000000000
```
**Train 2 output**
```text
000000000000
000000033330
000000000000
000000000000
000007700000
000007700000
000000000000
030000000000
030000000000
033000000000
```
**Test input**
```text
000000000000
030000000000
030000000000
030000000000
000000000000
000003330000
000000300000
000000000000
000000000300
000000000300
000000000330
000000000000
```
**Test output**
```text
000000000000
030000000000
030000000000
030000000000
000000000000
000007770000
000000700000
000000000000
000000000300
000000000300
000000000330
000000000000
```
**Written solution:** Among the green(3) objects, locate the one whose bounding-box center is nearest the center of the board. Recolor that object orange(7), leaving the others green.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    gc=((h-1)/2,(w-1)/2)
    def dist(comp):
        cr,cc=center_bbox(comp['cells'])
        return abs(cr-gc[0])+abs(cc-gc[1])
    comps=components(grid,{3},4)
    target=min(comps,key=lambda comp:(dist(comp), bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=7
    return out
```

## S4_M2 — Parallel Bars Become Solid

**Skills:** object pairing, rectangle completion, same-color fill

**Scaffold:**
- Find single-column bars of the same color and height.
- Match bars that share the same row span.
- Fill the entire rectangle between each matched pair with that color.

**Train 1 input**
```text
000000000000
010010000000
010010000000
010010000000
010010000000
000000020020
000000020020
000000020020
000000000000
```
**Train 1 output**
```text
000000000000
011110000000
011110000000
011110000000
011110000000
000000022220
000000022220
000000022220
000000000000
```
**Train 2 input**
```text
00000000000
00000000000
00300030000
00300030000
00300030000
00000000404
00000000404
00000000404
00000000404
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00333330000
00333330000
00333330000
00000000444
00000000444
00000000444
00000000444
00000000000
```
**Test input**
```text
0000000000000
0100010000000
0100010000000
0100010000000
0100010000000
0000000000000
0000000060060
0000000060060
0000000060060
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0111110000000
0111110000000
0111110000000
0111110000000
0000000000000
0000000066660
0000000066660
0000000066660
0000000000000
0000000000000
```
**Written solution:** Whenever two same-colored vertical bars have the same height and align on the same rows, fill the whole rectangle spanning those bars with that same color.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    # group vertical bars by color and row span
    bars=[]
    for comp in comps:
        r1,c1,r2,c2=bbox(comp['cells'])
        if c1==c2 and len(comp['cells'])==r2-r1+1 and len(comp['cells'])>=2:
            bars.append((comp['color'], r1,r2,c1))
    grouped=defaultdict(list)
    for color,r1,r2,c in bars:
        grouped[(color,r1,r2)].append(c)
    for (color,r1,r2), cols in grouped.items():
        cols=sorted(cols)
        if len(cols)>=2:
            # pair consecutive
            for i in range(0,len(cols),2):
                if i+1 < len(cols):
                    c1,c2=cols[i],cols[i+1]
                    for r in range(r1,r2+1):
                        for c in range(c1,c2+1):
                            out[r][c]=color
    return out
```

## S4_M3 — Main-Diagonal Mirror

**Skills:** reflection symmetry, square-grid reasoning, copy without erase

**Scaffold:**
- Work on the main diagonal of the square grid.
- For each non-black cell, place a mirrored copy across that diagonal.
- Keep the original cells too, producing a symmetric union.

**Train 1 input**
```text
00000000
00000000
00000000
00000000
00030000
02030000
02200000
00000000
```
**Train 1 output**
```text
00000000
00000220
00000020
00003300
00030000
02030000
02200000
00000000
```
**Train 2 input**
```text
000000000
000000000
000000000
000000000
000000000
100000000
104000000
004440000
000000000
```
**Train 2 output**
```text
000001100
000000000
000000440
000000040
000000040
100000000
104000000
004440000
000000000
```
**Test input**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0007000000
0007000000
0007000000
0660000000
0060000000
```
**Test output**
```text
0000000000
0000000060
0000000066
0000077700
0000000000
0007000000
0007000000
0007000000
0660000000
0060000000
```
**Written solution:** Reflect every non-black cell across the main diagonal of the square grid, adding the mirrored copy while preserving the original pattern.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    n=len(grid)
    for r in range(n):
        for c in range(n):
            if grid[r][c]!=0:
                out[c][r]=grid[r][c]
    return out
```

## S4_M4 — Marker Count Matches Size

**Skills:** counting, component size comparison, object selection

**Scaffold:**
- Count the gray(5) marker cells.
- Find blue(1) components and compare their sizes.
- Recolor the blue object whose size matches the marker count red(2).

**Train 1 input**
```text
555000000000
000000000000
000000000000
010000110000
011000110000
000000000000
000000011110
000000000000
000000000000
```
**Train 1 output**
```text
555000000000
000000000000
000000000000
020000110000
022000110000
000000000000
000000011110
000000000000
000000000000
```
**Train 2 input**
```text
555500000000
000000000000
000000001000
001100001000
001100001000
000000000000
000000001000
000000011100
000000001000
000000000000
```
**Train 2 output**
```text
555500000000
000000000000
000000001000
002200001000
002200001000
000000000000
000000001000
000000011100
000000001000
000000000000
```
**Test input**
```text
5555500000000
0000000000000
0000000001100
0000000001100
0001000000000
0011100000000
0001000000000
0000000001000
0000000001000
0000000001100
0000000000000
```
**Test output**
```text
5555500000000
0000000000000
0000000001100
0000000001100
0002000000000
0022200000000
0002000000000
0000000001000
0000000001000
0000000001100
0000000000000
```
**Written solution:** Count the gray(5) markers at the top. Then find the blue(1) object with exactly that many cells and recolor it red(2).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    count=sum(v==5 for row in grid for v in row)
    comps=components(grid,{1},4)
    target=min([comp for comp in comps if len(comp['cells'])==count], key=lambda comp:bbox(comp['cells']))
    for r,c in target['cells']:
        out[r][c]=2
    return out
```

## S4_M5 — Rectangle to Center Cross

**Skills:** bounding boxes, odd-sized rectangles, shape reduction

**Scaffold:**
- Identify solid yellow(4) rectangles with odd height and width.
- Erase the rectangle's other cells.
- Keep only its center row and center column, forming a cross.

**Train 1 input**
```text
000000000000
044400000000
044400044400
044400044400
000000044400
000000044400
000000044400
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
004000000000
044400004000
004000004000
000000044400
000000004000
000000004000
000000000000
000000000000
```
**Train 2 input**
```text
00000000000
04444400000
04444400000
04444400000
00000000000
00000444440
00000444440
00000444440
00000444440
00000444440
00000000000
```
**Train 2 output**
```text
00000000000
00040000000
04444400000
00040000000
00000000000
00000004000
00000004000
00000444440
00000004000
00000004000
00000000000
```
**Test input**
```text
0000000000000
0044400000000
0044400000000
0044400000000
0044400000000
0044400000000
0000000000000
0000000444440
0000000444440
0000000444440
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0004000000000
0004000000000
0044400000000
0004000000000
0004000000000
0000000000000
0000000004000
0000000444440
0000000004000
0000000000000
0000000000000
```
**Written solution:** Each solid yellow(4) rectangle is reduced to the cross made from its middle row and middle column. All other cells of the rectangle disappear.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    for comp in components(grid,{4},4):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        h,w=r2-r1+1,c2-c1+1
        if h%2==1 and w%2==1 and is_solid_rectangle(cells):
            for r,c in cells:
                out[r][c]=0
            mr=(r1+r2)//2
            mc=(c1+c2)//2
            for c in range(c1,c2+1):
                out[mr][c]=4
            for r in range(r1,r2+1):
                out[r][mc]=4
    return out
```

## S4_M6 — Four Corners to Perimeter

**Skills:** corner detection, axis-aligned rectangles, outline drawing

**Scaffold:**
- Group same-colored singleton corner cells.
- Interpret each group of four as the corners of a rectangle.
- Draw the full rectangle outline in that color.

**Train 1 input**
```text
000000000000
020020000000
000000030030
000000000000
000000000000
020020000000
000000030030
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
022220000000
020020033330
020020030030
020020030030
022220030030
000000033330
000000000000
000000000000
```
**Train 2 input**
```text
4004000000
0000000000
0000000000
4004000000
0000000000
0000060060
0000000000
0000000000
0000060060
0000000000
```
**Train 2 output**
```text
4444000000
4004000000
4004000000
4444000000
0000000000
0000066660
0000060060
0000060060
0000066660
0000000000
```
**Test input**
```text
0000000000000
0070007000000
0000000000000
0000000001010
0000000000000
0000000000000
0070007000000
0000000000000
0000000001010
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0077777000000
0070007000000
0070007001110
0070007001010
0070007001010
0077777001010
0000000001010
0000000001110
0000000000000
0000000000000
```
**Written solution:** Whenever four same-colored cells mark the corners of an axis-aligned rectangle, draw the complete perimeter of that rectangle in the same color.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    pos_by_color=defaultdict(list)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                pos_by_color[grid[r][c]].append((r,c))
    for color, cells in pos_by_color.items():
        if len(cells)==4:
            rs=sorted(set(r for r,c in cells)); cs=sorted(set(c for r,c in cells))
            if len(rs)==2 and len(cs)==2 and set(cells)=={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}:
                r1,r2=rs; c1,c2=cs
                for c in range(c1,c2+1):
                    out[r1][c]=color; out[r2][c]=color
                for r in range(r1,r2+1):
                    out[r][c1]=color; out[r][c2]=color
    return out
```

## S4_M7 — T to Plus Completion

**Skills:** shape completion, rotation handling, local extension

**Scaffold:**
- Find green(3) T-tetrominoes in any rotation.
- Locate the T's center cell and identify the missing arm.
- Add that missing arm cell so the shape becomes a plus.

**Train 1 input**
```text
0000000000
0333000000
0030000000
0000000000
0000000000
0000000300
0000003300
0000000300
0000000000
```
**Train 1 output**
```text
0030000000
0333000000
0030000000
0000000000
0000000000
0000000300
0000003330
0000000300
0000000000
```
**Train 2 input**
```text
00000000000
00000000000
00030000000
00333000000
00000000000
00000000000
00000003000
00000003300
00000003000
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00030000000
00333000000
00030000000
00000000000
00000003000
00000033300
00000003000
00000000000
```
**Test input**
```text
000000000000
000000033300
000000003000
000000000000
000000000000
000000000000
003000000000
003300000300
003000003330
000000000000
000000000000
```
**Test output**
```text
000000003000
000000033300
000000003000
000000000000
000000000000
000000000000
003000000000
033300000300
003000003330
000000000300
000000000000
```
**Written solution:** Each green(3) T shape is completed by adding its missing fourth arm, turning it into a 5-cell plus. The original T cells stay in place.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for comp in components(grid,{3},4):
        cells=set(comp['cells'])
        if len(cells)!=4 or tuple(normalize(comp['cells'])) not in T_shapes:
            continue
        # find center degree 3
        center=None
        for r,c in cells:
            n=sum((r+dr,c+dc) in cells for dr,dc in dirs4)
            if n==3:
                center=(r,c)
                break
        if center is None: 
            continue
        r,c=center
        for dr,dc in dirs4:
            nr,nc=r+dr,c+dc
            if (nr,nc) not in cells:
                out[nr][nc]=3
    return out
```

# Hard

## S4_H1 — Four-Quadrant Symmetry

**Skills:** two-axis reflection, quadrant reasoning, pattern replication

**Scaffold:**
- Use the upper-left quadrant as the source pattern.
- Reflect it across the vertical midline and the horizontal midline.
- Fill all four quadrants with the resulting symmetric copies.

**Train 1 input**
```text
02000000
33000000
00400000
04000000
00000000
00000000
00000000
00000000
```
**Train 1 output**
```text
02000020
33000033
00400400
04000040
04000040
00400400
33000033
02000020
```
**Train 2 input**
```text
6000000000
6600000000
0000000000
0020000000
0200000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 output**
```text
6000000006
6600000066
0000000000
0020000200
0200000020
0200000020
0020000200
0000000000
6600000066
6000000006
```
**Test input**
```text
007000000000
070000000000
000700000000
000000000000
300000000000
003030000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Test output**
```text
007000000700
070000000070
000700007000
000000000000
300000000003
003030030300
003030030300
300000000003
000000000000
000700007000
070000000070
007000000700
```
**Written solution:** Take the pattern in the upper-left quadrant and mirror it across both the vertical and horizontal midlines so that the whole board becomes four-way symmetric.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    assert h==w and h%2==0
    midr=h//2
    midc=w//2
    # source upper-left quadrant
    for r in range(midr):
        for c in range(midc):
            val=grid[r][c]
            if val!=0:
                out[r][c]=val
                out[r][w-1-c]=val
                out[h-1-r][c]=val
                out[h-1-r][w-1-c]=val
    return out
```

## S4_H2 — Rotation-Coded Frames

**Skills:** template extraction, rotation by marker, frame-local stamping

**Scaffold:**
- Read the small color-2 template near the top-left.
- Each color-5 frame contains a cyan(8) marker in one interior corner; that corner encodes the rotation.
- Stamp the rotated template into the frame interior and remove the marker.

**Train 1 input**
```text
00000000000000
02000005555500
02200005800500
00000005000500
00000005000500
00000005555500
00000000000000
00000005555500
00000005000500
00000005000500
00000005008500
00000005555500
00000000000000
```
**Train 1 output**
```text
00000000000000
02000005555500
02200005200500
00000005220500
00000005000500
00000005555500
00000000000000
00000005555500
00000005220500
00000005020500
00000005000500
00000005555500
00000000000000
```
**Train 2 input**
```text
000000000000000
020000005555500
022000005008500
000000005000500
000000005000500
000000005555500
000000000000000
000000005555500
000000005000500
000000005000500
000000005800500
000000005555500
000000000000000
```
**Train 2 output**
```text
000000000000000
020000005555500
022000005220500
000000005200500
000000005000500
000000005555500
000000000000000
000000005555500
000000005020500
000000005220500
000000005000500
000000005555500
000000000000000
```
**Test input**
```text
0000000000000000
0200000005555500
0220000005000500
0000000005000500
0000000005800500
0000000005555500
0000000000000000
0000000000000000
0000000005555500
0000000005008500
0000000005000500
0000000005000500
0000000005555500
0000000000000000
```
**Test output**
```text
0000000000000000
0200000005555500
0220000005020500
0000000005220500
0000000005000500
0000000005555500
0000000000000000
0000000000000000
0000000005555500
0000000005220500
0000000005200500
0000000005000500
0000000005555500
0000000000000000
```
**Written solution:** Use the top-left color-2 template as a prototype. For each color-5 frame, look at which interior corner contains the cyan(8) marker, rotate the template accordingly, stamp it into the frame interior, and remove the marker.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    # template: first component of color 2 not inside frame color 5
    comps2=components(grid,{2},4)
    # choose component with smallest bbox top-left
    template=min(comps2,key=lambda comp:(bbox(comp['cells'])[0],bbox(comp['cells'])[1]))
    template_shape=normalize(template['cells'])
    # erase any markers? We'll overwrite interiors only
    frames=[comp for comp in components(grid,{5},4) if is_rect_outline(comp['cells'])]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        # find marker color 8 inside bbox
        marker=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c]==8:
                    marker=(r,c)
        if marker is None:
            continue
        mr,mc=marker
        # mapping corner to rotation
        corners={(r1+1,c1+1):0,(r1+1,c2-1):1,(r2-1,c2-1):2,(r2-1,c1+1):3}
        # marker expected exactly at one interior corner
        rot=corners[marker]
        shape=rotate_norm_cells(template_shape, rot)
        # clear marker interior
        out[mr][mc]=0
        # stamp in interior anchored at top-left interior
        for dr,dc in shape:
            rr,cc=r1+1+dr,c1+1+dc
            out[rr][cc]=2
    return out
```

## S4_H3 — Hole Count Match

**Skills:** topological reasoning, hole counting, marker-to-object matching

**Scaffold:**
- Count the magenta(6) header markers.
- Count the enclosed holes in each green(3) object.
- Recolor the object whose hole count equals the marker count orange(7).

**Train 1 input**
```text
600000000000000
000000000000000
033000333033333
033000303030303
000000333030303
000000000030303
000000000033333
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
600000000000000
000000000000000
033000777033333
033000707030303
000000777030303
000000000030303
000000000033333
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
6600000000000000
0000000000000000
0000000000000000
0333003333300000
0303003030300330
0333003030300330
0000003030300000
0000003333300000
0000000000000000
0000000000000000
0000000000000000
```
**Train 2 output**
```text
6600000000000000
0000000000000000
0000000000000000
0333007777700000
0303007070700330
0333007070700330
0000007070700000
0000007777700000
0000000000000000
0000000000000000
0000000000000000
```
**Test input**
```text
6000000000000000
0000000000000000
0000000000000000
0333330000000000
0303030033000000
0303030033000000
0303030000000000
0333330000003330
0000000000003030
0000000000003330
0000000000000000
0000000000000000
```
**Test output**
```text
6000000000000000
0000000000000000
0000000000000000
0333330000000000
0303030033000000
0303030033000000
0303030000000000
0333330000007770
0000000000007070
0000000000007770
0000000000000000
0000000000000000
```
**Written solution:** The magenta(6) markers specify a number. Among the green(3) objects, find the one with that many enclosed holes and recolor the whole object orange(7).

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    marker_count=sum(v==6 for row in grid for v in row)
    # target among green components
    targets=[]
    for comp in components(grid,{3},4):
        holes=count_holes_component(grid,comp)
        if holes==marker_count:
            targets.append(comp)
    # choose top-left if multiple
    if targets:
        target=min(targets,key=lambda comp:bbox(comp['cells']))
        for r,c in target['cells']:
            out[r][c]=7
    return out
```

## S4_H4 — Count Comparison Matrix

**Skills:** meta-layout parsing, count comparison, matrix synthesis

**Scaffold:**
- Read the three 2x2 count blocks across the top and the three 2x2 count blocks down the left.
- For each row/column pair, compare the two counts.
- Fill the corresponding 2x2 matrix block: yellow(4) if top > left, green(3) if top < left, cyan(8) if equal.

**Train 1 input**
```text
00010011011
00000010011
00000000000
22000000000
00000000000
00000000000
22000000000
20000000000
00000000000
20000000000
00000000000
```
**Train 1 output**
```text
00010011011
00000010011
00000000000
22033044044
00033044044
00000000000
22033088044
20033088044
00000000000
20088044044
00088044044
```
**Train 2 input**
```text
00011011010
00011000000
00000000000
20000000000
00000000000
00000000000
22000000000
22000000000
00000000000
22000000000
00000000000
```
**Train 2 output**
```text
00011011010
00011000000
00000000000
20044044088
00044044088
00000000000
22088033033
22088033033
00000000000
22044088033
00044088033
```
**Test input**
```text
00011011011
00000011010
00000000000
22000000000
20000000000
00000000000
20000000000
00000000000
00000000000
22000000000
22000000000
```
**Test output**
```text
00011011011
00000011010
00000000000
22033044088
20033044088
00000000000
20044044044
00044044044
00000000000
22033088033
22033088033
```
**Written solution:** Compare each top header count with each left header count. In the 3x3 matrix area, fill each 2x2 block yellow(4) when the top count is larger, green(3) when the left count is larger, and cyan(8) when they are equal.

**Reference program:**
```python
def solve(grid):
    # fixed layout 11x11: top header 3 blocks rows 0:2 at cols [3:5,6:8,9:11]
    # left header 3 blocks cols 0:2 at rows [3:5,6:8,9:11]
    out=copyg(grid)
    row_starts=[3,6,9]
    col_starts=[3,6,9]
    top_counts=[]
    left_counts=[]
    for cs in col_starts:
        cnt=sum(grid[r][c]!=0 for r in range(0,2) for c in range(cs,cs+2))
        top_counts.append(cnt)
    for rs in row_starts:
        cnt=sum(grid[r][c]!=0 for r in range(rs,rs+2) for c in range(0,2))
        left_counts.append(cnt)
    for i,rs in enumerate(row_starts):
        for j,cs in enumerate(col_starts):
            if top_counts[j]>left_counts[i]:
                color=4
            elif top_counts[j]<left_counts[i]:
                color=3
            else:
                color=8
            for r in range(rs,rs+2):
                for c in range(cs,cs+2):
                    out[r][c]=color
    return out
```

## S4_H5 — Pivot 4-Way Rotation

**Skills:** relative coordinates, rotation around pivot, set completion

**Scaffold:**
- Locate the maroon(9) pivot.
- Take the non-pivot object as a set of offsets from that pivot.
- Stamp the 0°, 90°, 180°, and 270° versions around the pivot.

**Train 1 input**
```text
000000000
000002000
000002200
000000000
000090000
000000000
000000000
000000000
000000000
```
**Train 1 output**
```text
000000000
000002000
002002200
022000000
000090000
000000220
002200200
000200000
000000000
```
**Train 2 input**
```text
00000000000
00000060000
00000066600
00000000000
00000000000
00000900000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000060000
00600066600
00600000000
06600000000
00000900000
00000000660
00000000600
00666000600
00006000000
00000000000
```
**Test input**
```text
0000000000000
0000000300000
0000000330000
0000000000000
0000000000000
0000000000000
0000009000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Test output**
```text
0000000000000
0000000300000
0000000330000
0000000000000
0030000000000
0330000000000
0000009000000
0000000000330
0000000000300
0000000000000
0000330000000
0000030000000
0000000000000
```
**Written solution:** Treat the maroon(9) cell as a rotation center. Copy the given non-pivot shape into all four quarter-turn orientations around that pivot, keeping the original orientation too.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    # pivot is 9
    pivots=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    assert len(pivots)==1
    pr,pc=pivots[0]
    # choose non-pivot cells of color 2? Could support all nonzero except 9 and maybe keep others?
    cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c]!=0 and grid[r][c]!=9]
    for r,c,color in cells:
        dr,dc=r-pr,c-pc
        rots=[(dr,dc),(dc,-dr),(-dr,-dc),(-dc,dr)]
        for rr,cc in rots:
            out[pr+rr][pc+cc]=color
    return out
```

## S4_H6 — Colorized Template Frames

**Skills:** template extraction, color transfer, frame-local stamping

**Scaffold:**
- Read the neutral color-1 template near the top-left.
- Each color-5 frame contains a single colored marker in its interior.
- Remove that marker and stamp the template inside the frame using the marker's color.

**Train 1 input**
```text
0000000000000000
0111000005555500
0010000005200500
0000000005000500
0000000005000500
0000000005555500
0000000000000000
0000000005555500
0000000005400500
0000000005000500
0000000005000500
0000000005555500
0000000000000000
```
**Train 1 output**
```text
0000000000000000
0111000005555500
0010000005222500
0000000005020500
0000000005000500
0000000005555500
0000000000000000
0000000005555500
0000000005444500
0000000005040500
0000000005000500
0000000005555500
0000000000000000
```
**Train 2 input**
```text
00000000000000000
01110000005555500
00100000005700500
00000000005000500
00000000005000500
00000000005555500
00000000000000000
00000000005555500
00000000005300500
00000000005000500
00000000005000500
00000000005555500
00000000000000000
```
**Train 2 output**
```text
00000000000000000
01110000005555500
00100000005777500
00000000005070500
00000000005000500
00000000005555500
00000000000000000
00000000005555500
00000000005333500
00000000005030500
00000000005000500
00000000005555500
00000000000000000
```
**Test input**
```text
000000000000000000
011100000005555500
001000000005800500
000000000005000500
000000000005000500
000000000005555500
000000000000000000
000000000000000000
000000000005555500
000000000005600500
000000000005000500
000000000005000500
000000000005555500
000000000000000000
```
**Test output**
```text
000000000000000000
011100000005555500
001000000005888500
000000000005080500
000000000005000500
000000000005555500
000000000000000000
000000000000000000
000000000005555500
000000000005666500
000000000005060500
000000000005000500
000000000005555500
000000000000000000
```
**Written solution:** Use the neutral color-1 template as a shape prototype. Inside every color-5 frame, replace the single interior marker with a copy of the template recolored to that marker's color.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    # template: neutral color 1 component with smallest bbox
    template=min(components(grid,{1},4), key=lambda comp:bbox(comp['cells']))
    shape=normalize(template['cells'])
    frames=[comp for comp in components(grid,{5},4) if is_rect_outline(comp['cells'])]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        # find any nonzero interior marker not 5
        marker=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c] not in (0,5):
                    marker=(r,c,grid[r][c])
        if marker is None:
            continue
        mr,mc,color=marker
        out[mr][mc]=0
        for dr,dc in shape:
            out[r1+1+dr][c1+1+dc]=color
    return out
```

## S4_H7 — Prototype Legend Recolor

**Skills:** legend parsing, shape matching, symbol-grounded recolor

**Scaffold:**
- Read the prototype shapes on the left side of the separator.
- Each prototype has an associated sample color in the legend.
- Find matching neutral shapes on the right and recolor them according to the legend.

**Train 1 input**
```text
000000000000000
110020001100000
110000001100000
000000000000000
000000000000000
100070000100000
110000000110000
000000000000000
111040000011100
010000000001000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
110020002200000
110000002200000
000000000000000
000000000000000
100070000700000
110000000770000
000000000000000
111040000044400
010000000004000
000000000000000
000000000000000
```
**Train 2 input**
```text
0000000000000000
1000600000111000
1100000000010000
0000000000000000
0000000000000000
1110300000000000
0100000001100000
0000000001100000
0000000000000000
1100800000010000
1100000000011000
0000000000000000
0000000000000000
```
**Train 2 output**
```text
0000000000000000
1000600000333000
1100000000030000
0000000000000000
0000000000000000
1110300000000000
0100000008800000
0000000008800000
0000000000000000
1100800000060000
1100000000066000
0000000000000000
0000000000000000
```
**Test input**
```text
000000000000000000
110020000010000000
110000000011001100
000000000000001100
000000000000000000
111070000001110000
010000000000100000
000000000000000000
000000000000000000
100040000000000000
110000000000001100
000000000000001100
000000000000000000
000000000000000000
```
**Test output**
```text
000000000000000000
110020000040000000
110000000044002200
000000000000002200
000000000000000000
111070000007770000
010000000000700000
000000000000000000
000000000000000000
100040000000000000
110000000000002200
000000000000002200
000000000000000000
000000000000000000
```
**Written solution:** The left side is a shape legend: each neutral prototype shape is paired with an output color. Recolor every matching neutral shape on the right side to the color specified by its prototype.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    zero_cols=[c for c in range(w) if all(grid[r][c]==0 for r in range(h)) and any(any(v!=0 for v in row[:c]) for row in grid) and any(any(v!=0 for v in row[c+1:]) for row in grid)]
    sep=min(zero_cols, key=lambda c: abs(c-w/2))
    comps_left=[comp for comp in components(grid,{1},4) if bbox(comp['cells'])[3] < sep]
    mapping={}
    for comp in comps_left:
        r1,c1,r2,c2=bbox(comp['cells'])
        sample=None
        for r in range(max(0,r1-1), min(h,r2+2)):
            for c in range(c2+1,sep):
                if grid[r][c] not in (0,1):
                    sample=grid[r][c]
        mapping[tuple(normalize(comp['cells']))]=sample
    for comp in components(grid,{1},4):
        if bbox(comp['cells'])[1] > sep:
            color=mapping.get(tuple(normalize(comp['cells'])),1)
            for r,c in comp['cells']:
                out[r][c]=color
    return out
```
