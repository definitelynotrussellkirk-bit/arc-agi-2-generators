# ARC-style Additional Puzzle Bank (21 puzzles)

This bank adds **21 new puzzles** grouped into **7 easy, 7 medium, and 7 hard**.
Each puzzle includes train pairs, a test input, the expected test output, a written rule, and a compact reference-program solution.

The bank is designed to stress a range of solver behaviors: local patterning, connected components, border contact, symmetry, vector copy, topology, counting, packing, and conditional control logic.

# Easy (7)

## E1 — Recolor every full 2x2 red block

**What it tests:** local pattern detection; partial-overlap handling

**Train A input**
```text
0000000
0220000
0220200
0000200
0000000
0002200
0002200
```
**Train A output**
```text
0000000
0330000
0330200
0000200
0000000
0003300
0003300
```
**Train B input**
```text
2000000
2200000
0000220
0000220
0000000
0020000
0000000
```
**Train B output**
```text
2000000
2200000
0000330
0000330
0000000
0020000
0000000
```
**Test input**
```text
00000000
02200020
02200020
00000000
00022000
00022000
00200000
00000000
```
**Expected test output**
```text
00000000
03300020
03300020
00000000
00033000
00033000
00200000
00000000
```
**Written solution**
Every cell that belongs to a complete 2x2 block of red(2) should become green(3). Lone red cells and incomplete L-shapes stay red.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each top-left corner (r,c) of a 2x2 window:
        if all four cells are 2:
            recolor those four cells to 3 in out
    return out
```

## E2 — Recolor blue components that touch the top border

**What it tests:** connected components; border contact

**Train A input**
```text
0100010
0110011
0000001
0011000
0011000
0000000
```
**Train A output**
```text
0400040
0440044
0000004
0011000
0011000
0000000
```
**Train B input**
```text
1000000
1100110
0000010
0000010
0111000
0000000
```
**Train B output**
```text
4000000
4400110
0000010
0000010
0111000
0000000
```
**Test input**
```text
00100010
00110011
00000001
00011000
00001000
11000000
10000000
```
**Expected test output**
```text
00400040
00440044
00000004
00011000
00001000
11000000
10000000
```
**Written solution**
Find each blue(1) connected component. If any cell in that component touches the top row, recolor the entire component to yellow(4). Other blue components stay blue.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for comp in blue_components(grid):
        if any(cell.row == 0 for cell in comp):
            paint(comp, 4, out)
    return out
```

## E3 — Fill hollow rectangles

**What it tests:** rectangle recognition; interior fill

**Train A input**
```text
000000000
066660000
060060000
060060000
066660000
000006660
000006060
000006660
000000000
```
**Train A output**
```text
000000000
066660000
066660000
066660000
066660000
000006660
000006660
000006660
000000000
```
**Train B input**
```text
0006666000
0006006000
0006006000
0006666000
0000000000
0666000000
0606000000
0666000000
0000000000
```
**Train B output**
```text
0006666000
0006666000
0006666000
0006666000
0000000000
0666000000
0666000000
0666000000
0000000000
```
**Test input**
```text
0000000000
0666600000
0600600000
0600600000
0666600000
0000006660
0000006060
0000006060
0000006660
0000000000
```
**Expected test output**
```text
0000000000
0666600000
0666600000
0666600000
0666600000
0000006660
0000006660
0000006660
0000006660
0000000000
```
**Written solution**
Each connected component of color 6 is a hollow axis-aligned rectangle. Fill the rectangle’s interior with 6, turning the whole box solid.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for comp in color_components(grid, 6):
        if comp_is_rectangular_border(comp):
            r0,r1,c0,c1 = bbox(comp)
            fill interior rows r0+1..r1-1 and cols c0+1..c1-1 with 6
    return out
```

## E4 — Mirror the left object across a vertical divider

**What it tests:** explicit symmetry; divider handling

**Train A input**
```text
0005000
0115000
0105000
0005000
0005000
```
**Train A output**
```text
0005000
0115110
0105010
0005000
0005000
```
**Train B input**
```text
2005000
2205000
2005000
0005000
0005000
```
**Train B output**
```text
2005002
2205022
2005002
0005000
0005000
```
**Test input**
```text
000050000
011050000
001050000
011050000
000050000
```
**Expected test output**
```text
000050000
011050110
001050100
011050110
000050000
```
**Written solution**
The full gray(5) column is a mirror axis. Copy every non-zero non-divider cell on the left side to its reflected position on the right side. Keep the original object too.

**Program solution (reference algorithm)**
```python
def solve(grid):
    d = divider_column_of_all_5s(grid)
    out = clear_right_side_except_divider(grid, d)
    for each nonzero cell left of d:
        out[r][2*d - c] = grid[r][c]
    return out
```

## E5 — Extend every horizontal line of length 3

**What it tests:** object length detection; safe border logic

**Train A input**
```text
00000000
00088800
00000000
00800000
00800000
00000000
```
**Train A output**
```text
00000000
00888880
00000000
00800000
00800000
00000000
```
**Train B input**
```text
000000000
088800000
000000000
000000000
000888000
000000000
```
**Train B output**
```text
000000000
888880000
000000000
000000000
008888800
000000000
```
**Test input**
```text
000000000
000888000
000000000
088000000
000000000
000008880
000000000
```
**Expected test output**
```text
000000000
008888800
000000000
088000000
000000000
000088888
000000000
```
**Written solution**
Look for connected horizontal segments of color 8 that have exactly length 3. Extend each such segment by one cell on the left and one on the right if those cells are empty. Other 8-components do not change.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for comp in color_components(grid, 8):
        if comp is a horizontal line of exactly length 3:
            try to paint one empty cell just before the left end
            try to paint one empty cell just after the right end
    return out
```

## E6 — Crop to the tight non-zero bounding box

**What it tests:** resize; bbox extraction

**Train A input**
```text
0000000
0011000
0011000
0001000
0000000
```
**Train A output**
```text
11
11
01
```
**Train B input**
```text
000000000
000022000
000020000
000022200
000000000
```
**Train B output**
```text
220
200
222
```
**Test input**
```text
00000000
00033000
00030300
00033300
00000000
00000000
```
**Expected test output**
```text
330
303
333
```
**Written solution**
Ignore the surrounding black background. Output only the smallest rectangle that contains every non-zero cell.

**Program solution (reference algorithm)**
```python
def solve(grid):
    cells = all_nonzero_cells(grid)
    r0,r1,c0,c1 = bbox(cells)
    return crop(grid, r0, r1, c0, c1)
```

## E7 — Recolor the largest orange component

**What it tests:** size comparison between objects

**Train A input**
```text
0007000
0077000
0000000
0777000
0700000
0000000
```
**Train A output**
```text
0007000
0077000
0000000
0222000
0200000
0000000
```
**Train B input**
```text
00000000
07700000
07000000
00000000
00007770
00000700
00000000
```
**Train B output**
```text
00000000
07700000
07000000
00000000
00002220
00000200
00000000
```
**Test input**
```text
000000000
007000000
077000000
000000000
000077000
000007000
000000000
000777700
000700000
```
**Expected test output**
```text
000000000
007000000
077000000
000000000
000077000
000007000
000000000
000222200
000200000
```
**Written solution**
Find all orange(7) connected components. Recolor only the largest one to red(2). Smaller orange components stay orange.

**Program solution (reference algorithm)**
```python
def solve(grid):
    comps = orange_components(grid)
    biggest = argmax(comps, key=size)
    out = copy(grid)
    paint(biggest, 2, out)
    return out
```


# Medium (7)

## M1 — Recolor line objects by orientation

**What it tests:** component orientation; object-level relabeling

**Train A input**
```text
0000000
0033300
0000000
0003000
0003000
0003000
0000000
```
**Train A output**
```text
0000000
0011100
0000000
0008000
0008000
0008000
0000000
```
**Train B input**
```text
00030000
00030000
00030000
00000000
03330000
00000000
00003330
00000000
```
**Train B output**
```text
00080000
00080000
00080000
00000000
01110000
00000000
00001110
00000000
```
**Test input**
```text
000000000
033300000
000000000
000300000
000300000
000300000
000000333
000000000
000000000
```
**Expected test output**
```text
000000000
011100000
000000000
000800000
000800000
000800000
000000111
000000000
000000000
```
**Written solution**
Every color-3 object is a straight line. Horizontal 3-lines become blue(1); vertical 3-lines become cyan(8).

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for comp in color_components(grid, 3):
        if all cells share one row:
            paint(comp, 1, out)
        elif all cells share one column:
            paint(comp, 8, out)
    return out
```

## M2 — Copy the object by the marker vector

**What it tests:** vector extraction from markers; translation copy

**Train A input**
```text
9000000
0040000
0440000
0009000
0000000
0000000
```
**Train A output**
```text
0000000
0040000
0440000
0000000
0000040
0000440
```
**Train B input**
```text
00900000
00000000
00770000
00070000
00000900
00000000
00000000
00000000
```
**Train B output**
```text
00000000
00000000
00770000
00070000
00000000
00000000
00000770
00000070
```
**Test input**
```text
090000000
000000000
003300000
000300000
000000000
000000900
000000000
000000000
```
**Expected test output**
```text
000000000
000000000
003300000
000300000
000000000
000000000
000000000
000000033
```
**Written solution**
There are two marker cells of color 9. Read the translation vector from the first marker to the second marker (top-left to bottom-right in row-major order). Copy the non-marker object by that vector. Remove the 9 markers. Keep the original object.

**Program solution (reference algorithm)**
```python
def solve(grid):
    p1, p2 = sorted(all_cells_of_color(grid, 9))
    dr, dc = p2.row - p1.row, p2.col - p1.col
    out = copy(grid); erase color 9 in out
    for each nonzero non-9 cell:
        out[r + dr][c + dc] = grid[r][c]
    return out
```

## M3 — Complete bilateral symmetry across the divider

**What it tests:** union with mirror completion

**Train A input**
```text
0005000
0115000
0105000
0005000
0005000
```
**Train A output**
```text
0005000
0115110
0105010
0005000
0005000
```
**Train B input**
```text
0005000
0205002
0225000
0005000
0005000
```
**Train B output**
```text
0005000
2205022
0225220
0005000
0005000
```
**Test input**
```text
000050000
011050000
001050100
011050000
000050000
```
**Expected test output**
```text
000050000
011050110
001050100
011050110
000050000
```
**Written solution**
The gray(5) column is a mirror axis. Any colored cell on either side should also appear in the reflected position on the other side. So the output is the symmetric completion, not just a copy from one fixed side.

**Program solution (reference algorithm)**
```python
def solve(grid):
    d = divider_column_of_all_5s(grid)
    out = copy(grid)
    for each nonzero non-divider cell (r,c):
        out[r][2*d - c] = grid[r][c]
    return out
```

## M4 — Recolor hollow and solid orange objects differently

**What it tests:** topology; hole detection

**Train A input**
```text
000000000
077770000
070070000
077770000
000000000
000077000
000077000
000000000
```
**Train A output**
```text
000000000
044440000
040040000
044440000
000000000
000022000
000022000
000000000
```
**Train B input**
```text
000777000
000707000
000777000
000000000
077000000
077000000
000000000
```
**Train B output**
```text
000444000
000404000
000444000
000000000
022000000
022000000
000000000
```
**Test input**
```text
0000000000
0777700000
0700700000
0777700000
0000000000
0000007700
0000007700
0000000000
0007777000
0007007000
0007777000
```
**Expected test output**
```text
0000000000
0444400000
0400400000
0444400000
0000000000
0000002200
0000002200
0000000000
0004444000
0004004000
0004444000
```
**Written solution**
For each orange(7) component, inspect its bounding box. If it contains a genuine empty interior hole, recolor that component to green(4). If it is solid, recolor it to red(2).

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for comp in orange_components(grid):
        if bbox_of(comp) contains interior zeros not in the component:
            paint(comp, 4, out)
        else:
            paint(comp, 2, out)
    return out
```

## M5 — Connect matched markers in a row or column

**What it tests:** pairwise relational filling

**Train A input**
```text
2000002
0000000
0003000
0003000
0000000
```
**Train A output**
```text
2222222
0000000
0003000
0003000
0000000
```
**Train B input**
```text
00000000
04000040
00000000
00050000
00050000
00050000
00000000
00000000
```
**Train B output**
```text
00000000
04444440
00000000
00050000
00050000
00050000
00000000
00000000
```
**Test input**
```text
200000002
000000000
000400000
000000000
000400000
000000000
000000000
```
**Expected test output**
```text
222222222
000000000
000400000
000400000
000400000
000000000
000000000
```
**Written solution**
Markers of the same color that lie in the same row or the same column should be joined by a solid line of that color, including the endpoints.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each nonzero color:
        pts = positions_of_that_color(grid)
        for each pair of pts:
            if same row: fill between them
            if same column: fill between them
    return out
```

## M6 — Compress objects into a size-sorted strip

**What it tests:** component counting; resize; canonical packing

**Train A input**
```text
22000
22000
00030
00440
00400
```
**Train A output**
```text
2222044403
```
**Train B input**
```text
055000
055000
050000
000060
000060
000000
```
**Train B output**
```text
55555066
```
**Test input**
```text
0007000
0777000
0000000
0000440
0000400
0000000
0030000
0000000
```
**Expected test output**
```text
7777044403
```
**Written solution**
Each connected component becomes a run of its own color whose length equals the component’s size. Sort the runs from largest to smallest, breaking size ties by smaller color number first, and separate runs by one black cell.

**Program solution (reference algorithm)**
```python
def solve(grid):
    runs = []
    for comp in all_nonzero_components(grid):
        runs.append((size(comp), color(comp)))
    sort runs by (-size, color)
    output_row = concatenate([color]*size for each run, with 0 separators)
    return [output_row]
```

## M7 — Recolor each gray frame by the marker inside it

**What it tests:** enclosure relation; frame-marker binding

**Train A input**
```text
0000000000
0555500000
0500500000
0520500000
0555500000
0000055550
0000050050
0000050350
0000055550
0000000000
```
**Train A output**
```text
0000000000
0222200000
0200200000
0200200000
0222200000
0000033330
0000030030
0000030030
0000033330
0000000000
```
**Train B input**
```text
00055550000
00050050000
00050750000
00050050000
00055550000
00000000000
05555000000
05005000000
05035000000
05555000000
00000000000
```
**Train B output**
```text
00077770000
00070070000
00070070000
00070070000
00077770000
00000000000
03333000000
03003000000
03003000000
03333000000
00000000000
```
**Test input**
```text
00000000000
05555000000
05005000000
05045000000
05555000000
00000000000
00005555000
00005005000
00005065000
00005555000
00000000000
```
**Expected test output**
```text
00000000000
04444000000
04004000000
04004000000
04444000000
00000000000
00006666000
00006006000
00006006000
00006666000
00000000000
```
**Written solution**
Every gray(5) hollow frame contains exactly one colored marker inside. Recolor the whole frame border to the marker’s color, then remove the marker, leaving the interior black.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for frame in gray_rectangular_borders(grid):
        marker = the single nonzero non-5 cell strictly inside the frame
        paint(frame, marker.color, out)
        erase(marker.position, out)
    return out
```


# Hard (7)

## H1 — Control cell chooses the reflection axis

**What it tests:** conditional branching; global reflection

**Train A input**
```text
1000000
0030000
0330000
0000000
0000000
```
**Train A output**
```text
0000000
0030300
0330330
0000000
0000000
```
**Train B input**
```text
2000000
0004000
0044000
0000000
0000000
```
**Train B output**
```text
0000000
0004000
0044000
0004000
0000000
```
**Test input**
```text
10000000
00006000
00066000
00006000
00000000
00000000
```
**Expected test output**
```text
00000000
00066000
00066000
00066000
00000000
00000000
```
**Written solution**
The top-left control cell tells you which reflection to apply to the non-control object. If the control is 1, reflect across the vertical axis of the whole grid. If the control is 2, reflect across the horizontal axis. Keep the original object and remove the control cell.

**Program solution (reference algorithm)**
```python
def solve(grid):
    control = grid[0][0]
    out = copy(grid); out[0][0] = 0
    for each nonzero cell except (0,0):
        if control == 1:
            out[r][W-1-c] = grid[r][c]
        elif control == 2:
            out[H-1-r][c] = grid[r][c]
    return out
```

## H2 — Copy only the smallest object by the marker vector

**What it tests:** vector translation + object comparison

**Train A input**
```text
090000000
022000000
020000000
000700000
000770000
000090000
000000000
000000000
```
**Train A output**
```text
000000000
022000000
020000000
000700000
000770000
000000000
000022000
000020000
```
**Train B input**
```text
009000000
000000000
000330000
000000000
000077700
000009000
000000000
000000000
000000000
```
**Train B output**
```text
000000000
000000000
000330000
000000000
000077700
000000000
000000000
000000330
000000000
```
**Test input**
```text
000900000
004400000
004000000
000000000
000770000
000777000
000000900
000000000
000000000
```
**Expected test output**
```text
000000000
004400000
004000000
000000000
000770000
000777000
000000000
000004400
000004000
```
**Written solution**
Two 9 markers define a translation vector. Among the ordinary objects, identify the smallest connected component, copy only that component by the marker vector, and remove the markers. Larger objects stay put and are not copied.

**Program solution (reference algorithm)**
```python
def solve(grid):
    p1, p2 = sorted(all_cells_of_color(grid, 9))
    dr, dc = p2.row - p1.row, p2.col - p1.col
    comps = all_non_marker_components(grid)
    smallest = component with minimum (size, top_row, left_col, color)
    out = copy(grid); erase color 9 in out
    for (r,c) in smallest:
        out[r+dr][c+dc] = color_of(smallest)
    return out
```

## H3 — Shoot rays from seeds until walls or borders

**What it tests:** dynamic propagation; obstacle stopping

**Train A input**
```text
0000000
0010000
0002000
0010000
0000000
```
**Train A output**
```text
0004000
0014000
4442444
0014000
0004000
```
**Train B input**
```text
000000000
000100000
000100000
010020010
000100000
000100000
000000000
```
**Train B output**
```text
000040000
000140000
000140000
014424410
000140000
000140000
000040000
```
**Test input**
```text
0000000000
0000100000
0000100000
0000200000
1110000111
0000200000
0000100000
0000100000
0000000000
```
**Expected test output**
```text
0000000000
0000100000
0000100000
4444244444
1110400111
4444244444
0000100000
0000100000
0000000000
```
**Written solution**
Every red(2) seed emits yellow(4) rays in the four cardinal directions. A ray continues through black cells and stops just before a blue(1) wall or the grid boundary. Existing non-black walls and seeds stay as they are.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each seed cell of color 2:
        for each direction in up/down/left/right:
            step outward until leaving grid or hitting a 1-wall
            paint traversed black cells as 4
    return out
```

## H4 — Count components by color and output a histogram grid

**What it tests:** object counting; abstract resize

**Train A input**
```text
200300
000000
020400
000400
000000
```
**Train A output**
```text
22
30
40
```
**Train B input**
```text
2200000
0003000
0000000
0400400
0000000
0000004
```
**Train B output**
```text
200
300
444
```
**Test input**
```text
2002002
0000000
0030003
0000000
0000400
0000000
0000000
```
**Expected test output**
```text
222
330
400
```
**Written solution**
Count connected components of colors 2, 3, and 4. Output a 3-row grid: the first row contains that many 2s, the second that many 3s, and the third that many 4s, all left-aligned. The output width is the largest of the three counts.

**Program solution (reference algorithm)**
```python
def solve(grid):
    counts = {2: num_components(color=2), 3: num_components(color=3), 4: num_components(color=4)}
    W = max(counts.values())
    out = [[0]*W for _ in range(3)]
    for color, row in [(2,0),(3,1),(4,2)]:
        fill first counts[color] cells of out[row] with color
    return out
```

## H5 — Extract the innermost enclosing frame and fill it

**What it tests:** nested enclosure; selection by depth; resize

**Train A input**
```text
00000000000
06666666660
06000000060
06077777060
06070007060
06070207060
06070007060
06077777060
06000000060
06666666660
00000000000
```
**Train A output**
```text
77777
77777
77777
77777
77777
```
**Train B input**
```text
000000000000
088888888880
080000000080
080444440080
080400040080
080402040080
080400040080
080444440080
080000000080
088888888880
000000000000
```
**Train B output**
```text
44444
44444
44444
44444
44444
```
**Test input**
```text
0000000000000
0999999999990
0900000000090
0906666666090
0906000006090
0906044406090
0906042406090
0906044406090
0906000006090
0906666666090
0900000000090
0999999999990
0000000000000
```
**Expected test output**
```text
444
444
444
```
**Written solution**
Several rectangular frames may enclose the marker 2. Choose the smallest frame that still contains the marker strictly inside it. Output only that frame’s bounding box, but as a solid rectangle filled with the frame’s color.

**Program solution (reference algorithm)**
```python
def solve(grid):
    marker = position_of_color_2(grid)
    candidate_frames = []
    for each rectangular border component (not color 2):
        if marker lies strictly inside its bbox:
            candidate_frames.append(frame)
    innermost = frame with smallest bounding-box area
    r0,r1,c0,c1 = bbox(innermost)
    return solid rectangle of frame.color with shape (r1-r0+1, c1-c0+1)
```

## H6 — Pack horizontal and vertical line objects into separate rows

**What it tests:** orientation split; sorting; resize

**Train A input**
```text
000000000
033300000
000000000
000400000
000400000
000400000
000000000
000005550
000000000
```
**Train A output**
```text
3330555
4440000
```
**Train B input**
```text
0007000000
0007000000
0007000000
0000000000
0666600000
0000000000
0000008800
0000000000
```
**Train B output**
```text
6666088
7770000
```
**Test input**
```text
0000000000
0444400000
0000000000
0003000000
0003000000
0003000000
0000000000
0000000666
0000000000
0000000000
```
**Expected test output**
```text
44440666
33300000
```
**Written solution**
Treat every non-zero component as a straight line. Output two rows. The top row contains the horizontal-line objects compressed into bars of their original colors and lengths, sorted from longest to shortest with zero separators. The bottom row does the same for vertical-line objects.

**Program solution (reference algorithm)**
```python
def solve(grid):
    horiz, vert = [], []
    for comp in all_nonzero_components(grid):
        if comp is horizontal:
            horiz.append((size(comp), color(comp)))
        elif comp is vertical:
            vert.append((size(comp), color(comp)))
    sort horiz and vert by (-size, color)
    top = concatenate colored runs from horiz with 0 separators
    bottom = concatenate colored runs from vert with 0 separators
    pad shorter row with zeros
    return [top, bottom]
```

## H7 — Control cell chooses whether to recolor hollow or solid objects

**What it tests:** conditional topology reasoning

**Train A input**
```text
100000000
077770000
070070000
077770000
000000000
000077000
000077000
000000000
```
**Train A output**
```text
000000000
088880000
080080000
088880000
000000000
000077000
000077000
000000000
```
**Train B input**
```text
200000000
077770000
070070000
077770000
000000000
000077000
000077000
000000000
```
**Train B output**
```text
000000000
077770000
070070000
077770000
000000000
000088000
000088000
000000000
```
**Test input**
```text
1000000000
0777700000
0700700000
0777700000
0000000000
0000077700
0000070700
0000077700
0000000000
0000007700
0000007700
```
**Expected test output**
```text
0000000000
0888800000
0800800000
0888800000
0000000000
0000088800
0000080800
0000088800
0000000000
0000007700
0000007700
```
**Written solution**
Ignore the top-left control cell after reading it. If the control is 1, recolor only hollow orange(7) components to cyan(8). If the control is 2, recolor only solid orange components to cyan(8). Objects of the other topology stay orange.

**Program solution (reference algorithm)**
```python
def solve(grid):
    control = grid[0][0]
    out = copy(grid); out[0][0] = 0
    for comp in orange_components(grid_without_control):
        hollow = has_interior_hole(comp)
        if (control == 1 and hollow) or (control == 2 and not hollow):
            paint(comp, 8, out)
    return out
```

