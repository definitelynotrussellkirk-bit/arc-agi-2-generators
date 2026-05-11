# ARC-style Additional Puzzle Bank — Volume 3 (21 puzzles)

This third volume adds **21 more puzzles** grouped into **7 easy, 7 medium, and 7 hard**.
Each puzzle includes train pairs, a test input, the expected test output, a written rule, and a compact reference-program solution.
This set is deliberately different from the first two banks: endpoint logic, diagonal completion, border-count components, parity recoloring, pivot rotations, boolean shape composition, frame reasoning, BFS chamber fills, ranked extraction, global rotational closure, and compartment majorities.


# Easy (7)


## E15 — Recolor the endpoints of green paths


**What it tests:** degree-1 detection on 4-neighbor paths


**Train A input**
```text
00000000
00333000
00030000
00030030
00030030
03330000
00000000
```

**Train A output**
```text
00000000
00232000
00030000
00030020
00030020
02330000
00000000
```

**Train B input**
```text
30000003
30003303
33300300
00000000
00000000
00333300
00000000
```

**Train B output**
```text
20000002
30002302
33200200
00000000
00000000
00233200
00000000
```

**Test input**
```text
000000000
030000300
030000330
033300000
000030000
000030000
000033000
000000000
```

**Expected test output**
```text
000000000
020000200
030000320
033200000
000020000
000030000
000032000
000000000
```

**Written solution**
Every green(3) cell with exactly one green cardinal neighbor becomes red(2). Green cells with two or more green neighbors stay green, and background stays unchanged.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each cell (r,c):
        if grid[r][c] == 3:
            deg = number of cardinal neighbors equal to 3
            if deg == 1:
                out[r][c] = 2
    return out
```


## E16 — Fill the centers of red Xs


**What it tests:** diagonal pattern completion


**Train A input**
```text
202000000
000000000
202000000
000002020
000000000
000002020
000000000
```

**Train A output**
```text
202000000
010000000
202000000
000002020
000000100
000002020
000000000
```

**Train B input**
```text
00000000
00002020
00000000
00002020
02020000
00000000
02020000
00000000
```

**Train B output**
```text
00000000
00002020
00000100
00002020
02020000
00100000
02020000
00000000
```

**Test input**
```text
000000000
020202020
000000000
020202020
000000000
000202000
000000000
000202000
000000000
```

**Expected test output**
```text
000000000
020202020
001010100
020202020
000010000
000202000
000010000
000202000
000000000
```

**Written solution**
Whenever a black(0) cell has red(2) diagonal neighbors in all four diagonal directions, fill that center cell with blue(1). Nothing else changes.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each black cell (r,c):
        if all four diagonal neighbors are 2:
            out[r][c] = 1
    return out
```


## E17 — Recolor orange components that touch exactly one border


**What it tests:** connected components; border-count logic


**Train A input**
```text
070000000
077000000
000000007
000077007
000070000
700000000
770000000
```

**Train A output**
```text
080000000
088000000
000000008
000077008
000070000
700000000
770000000
```

**Train B input**
```text
00000700
00000700
00077000
70007000
77000000
00000000
00000000
00000077
```

**Train B output**
```text
00000800
00000800
00077000
80007000
88000000
00000000
00000000
00000077
```

**Test input**
```text
770000000
000000007
000000077
000007000
700007700
700000000
000000000
000770000
```

**Expected test output**
```text
770000000
000000008
000000088
000007000
800007700
800000000
000000000
000880000
```

**Written solution**
Find every orange(7) connected component. If a component touches exactly one outer border of the grid, recolor the whole component to cyan(8). Components touching zero borders or two or more borders stay orange.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each orange component:
        touched = set of outer borders reached by that component
        if len(touched) == 1:
            recolor the whole component to 8
    return out
```


## E18 — Shift red singletons one cell to the right


**What it tests:** isolated-object translation


**Train A input**
```text
00000000
02000200
00000000
00200020
00000000
00020000
00000000
```

**Train A output**
```text
00000000
00200020
00000000
00020002
00000000
00002000
00000000
```

**Train B input**
```text
000000000
002000200
000000000
020000020
000000000
000020000
000000000
```

**Train B output**
```text
000000000
000200020
000000000
002000002
000000000
000002000
000000000
```

**Test input**
```text
000000000
020000200
000000000
000200000
000000020
000000000
002000000
000000000
```

**Expected test output**
```text
000000000
002000020
000000000
000020000
000000002
000000000
000200000
000000000
```

**Written solution**
Every isolated red(2) singleton moves one cell to the right. Its old cell becomes black(0). In these examples the destination is always empty.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = grid with all red singletons removed
    for each red cell:
        if it has no red cardinal neighbor:
            place a red cell at (r, c+1)
        else:
            keep it where it is
    return out
```


## E19 — Recolor blue T-junction centers


**What it tests:** local degree-3 detection


**Train A input**
```text
000000010
001000111
011100010
000000000
000001110
000000100
000000000
```

**Train A output**
```text
000000010
001000111
014100010
000000000
000001410
000000100
000000000
```

**Train B input**
```text
00000000
00000111
00010010
00110000
00010000
01000000
11100000
00000000
```

**Train B output**
```text
00000000
00000141
00010010
00140000
00010000
01000000
14100000
00000000
```

**Test input**
```text
010000000
111000010
000000111
000000000
000010000
000111000
000010000
000000000
```

**Expected test output**
```text
010000000
141000010
000000141
000000000
000010000
000111000
000010000
000000000
```

**Written solution**
A blue(1) cell becomes yellow(4) exactly when it has blue neighbors in three of the four cardinal directions. Plus-shape centers with four neighbors do not change.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each blue cell:
        deg = number of blue cardinal neighbors
        if deg == 3:
            out[r][c] = 4
    return out
```


## E20 — Recolor exact magenta dominoes


**What it tests:** connected-component size filter


**Train A input**
```text
000000000
066000000
000000060
000060000
000060000
000000666
000000000
```

**Train A output**
```text
000000000
077000000
000000060
000070000
000070000
000000666
000000000
```

**Train B input**
```text
60000000
60000000
00000660
00000000
00066600
00000000
00000006
00000000
```

**Train B output**
```text
70000000
70000000
00000770
00000000
00066600
00000000
00000006
00000000
```

**Test input**
```text
000000000
000600000
000600000
000000660
000000000
066600000
000000006
000000000
```

**Expected test output**
```text
000000000
000700000
000700000
000000770
000000000
066600000
000000006
000000000
```

**Written solution**
Find every magenta(6) 4-connected component of size exactly 2. Recolor those size-2 dominoes to orange(7). Larger or smaller magenta components stay magenta.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each magenta component:
        if component size == 2:
            recolor it to 7
    return out
```


## E21 — Complete 2x2 green almost-squares


**What it tests:** local hole filling inside 2x2 windows


**Train A input**
```text
33000000
30030000
00000000
00330000
00030000
00000000
00000000
```

**Train A output**
```text
33000000
33030000
00000000
00330000
00330000
00000000
00000000
```

**Train B input**
```text
00000000
00330000
00300000
00000000
03000000
00300000
00000000
00000000
```

**Train B output**
```text
00000000
00330000
00330000
00000000
03000000
00300000
00000000
00000000
```

**Test input**
```text
000330000
000300000
000000000
033000000
030000000
000000330
000000030
000000000
```

**Expected test output**
```text
000330000
000330000
000000000
033000000
033000000
000000330
000000330
000000000
```

**Written solution**
Whenever a 2x2 window contains exactly three green(3) cells and one black(0) cell, fill the missing corner with green(3).


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    scan every 2x2 window
    if a window has exactly three 3s and one 0:
        fill the 0 with 3
    return out
```


# Medium (7)


## M15 — Solidify each object's bounding box


**What it tests:** object abstraction; bounding boxes


**Train A input**
```text
0000000000
0100000030
0110000030
0000000030
0000020200
0000022200
0000000000
0000000000
```

**Train A output**
```text
0000000000
0110000030
0110000030
0000000030
0000022200
0000022200
0000000000
0000000000
```

**Train B input**
```text
400000000
440000000
040000000
000000020
000000022
000060000
000066000
000000000
000000000
```

**Train B output**
```text
440000000
440000000
440000000
000000022
000000022
000066000
000066000
000000000
000000000
```

**Test input**
```text
0000000000
0000003030
0010000300
0011000000
0000000000
0000000000
7000000000
7700000000
0000000000
```

**Expected test output**
```text
0000000000
0000003030
0011000300
0011000000
0000000000
0000000000
7700000000
7700000000
0000000000
```

**Written solution**
For each connected nonzero object, compute its tight bounding box and fill that entire rectangle with the object's own color.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = zeros_like(grid)
    for each nonzero component:
        find its bounding box
        fill that rectangle in out with the component color
    return out
```


## M16 — XOR two shapes after top-left alignment


**What it tests:** shape normalization; boolean composition


**Train A input**
```text
0000000000
0100000220
0100000200
0110000200
0000000000
0000000000
0000000000
0000000000
```

**Train A output**
```text
08
00
08
```

**Train B input**
```text
000000000
000002000
000002200
000000200
011000000
001000000
001000000
000000000
```

**Train B output**
```text
08
80
00
```

**Test input**
```text
0000000000
0100000000
0111000000
0000000000
0000000000
0000002200
0000000200
0000000200
0000000000
```

**Expected test output**
```text
080
808
080
```

**Written solution**
Take the color-1 object and the color-2 object. Crop each to its tight bounding box and align both shapes to the top-left corner. Output cyan(8) in every cell occupied by exactly one of the two aligned shapes.


**Program solution (reference algorithm)**
```python
def solve(grid):
    s1 = normalized cells of color 1
    s2 = normalized cells of color 2
    make an output grid large enough for both
    paint 8 where membership in s1 XOR membership in s2 is true
    return out
```


## M17 — Recolor components by size parity


**What it tests:** connected-component counting


**Train A input**
```text
000000000
022000000
000000000
000020000
000022000
000000000
000000020
000000000
```

**Train A output**
```text
000000000
088000000
000000000
000030000
000033000
000000000
000000030
000000000
```

**Train B input**
```text
20000000
22000000
02000000
00000000
00000200
00000220
00000220
00220000
```

**Train B output**
```text
80000000
88000000
08000000
00000000
00000300
00000330
00000330
00880000
```

**Test input**
```text
000220000
000000020
000000220
000000000
022000000
022000000
000000000
000002000
000000000
```

**Expected test output**
```text
000880000
000000030
000000330
000000000
088000000
088000000
000000000
000003000
000000000
```

**Written solution**
Each connected nonzero component is recolored by its size: odd-sized components become green(3) and even-sized components become cyan(8).


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = zeros_like(grid)
    for each component:
        color = 3 if size is odd else 8
        paint the same cells with that color
    return out
```


## M18 — Rotate the object 90° clockwise around the pivot


**What it tests:** coordinate transforms around a center


**Train A input**
```text
0000000
0100000
0110000
0002000
0000000
0000000
0000000
```

**Train A output**
```text
0000000
0000110
0000100
0000000
0000000
0000000
0000000
```

**Train B input**
```text
00000000
00000000
00000000
00000000
00002000
00110000
00010000
00000000
```

**Train B output**
```text
00000000
00000000
00010000
00110000
00000000
00000000
00000000
00000000
```

**Test input**
```text
000000000
000000000
000001000
000011000
002010000
000000000
000000000
000000000
000000000
```

**Expected test output**
```text
000000000
000000000
000000000
000000000
000000000
000000000
001100000
000110000
000000000
```

**Written solution**
Treat the red(2) cell as a pivot. Rotate every other nonzero cell 90 degrees clockwise around that pivot and output only the rotated object on an otherwise black grid.


**Program solution (reference algorithm)**
```python
def solve(grid):
    find the pivot cell
    for each nonzero non-pivot cell at offset (dr,dc):
        send it to (dc, -dr) around the pivot
    return a same-size output grid with the rotated object
```


## M19 — Fill the bounding rectangle of each color's markers


**What it tests:** group-by-color; rectangle fill


**Train A input**
```text
000000200
010000000
000000002
000100000
000000000
000030000
000033000
000000000
```

**Train A output**
```text
000000222
011100222
011100222
011100000
000000000
000033000
000033000
000000000
```

**Train B input**
```text
000000020
000000002
004040000
000000000
000040000
000000000
600000000
000000000
060000000
```

**Train B output**
```text
000000022
000000022
004440000
004440000
004440000
000000000
660000000
660000000
660000000
```

**Test input**
```text
0000000002
0000010000
0000000002
0000000100
0000000000
0300000000
0000000000
0303000000
0000000000
```

**Expected test output**
```text
0000000002
0000011102
0000011102
0000011100
0000000000
0333000000
0333000000
0333000000
0000000000
```

**Written solution**
For each nonzero color separately, take all cells of that color and fill the tight bounding rectangle spanning them, using that same color.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = zeros_like(grid)
    for each nonzero color:
        collect all cells of that color
        compute their bounding box
        fill that whole rectangle with the color
    return out
```


## M20 — Extract the object nearest the control marker


**What it tests:** object selection by Manhattan distance; cropping


**Train A input**
```text
0000000000
0440000000
0400000000
0000900000
0000004000
0000004400
0000000000
0044000000
0000000000
```

**Train A output**
```text
40
44
```

**Train B input**
```text
000000000
000000300
000000330
000033000
000000900
030000000
033000000
000000000
```

**Train B output**
```text
30
33
```

**Test input**
```text
000000000
070000000
077000000
000000070
000000070
000000090
000007700
000007000
000000000
```

**Expected test output**
```text
7
7
```

**Written solution**
Ignore the control marker 9. Among the remaining objects, choose the one whose nearest cell is closest in Manhattan distance to the marker. Output only that chosen object, cropped to its bounding box.


**Program solution (reference algorithm)**
```python
def solve(grid):
    find the 9-marker
    compute Manhattan distance from the marker to each object
    choose the minimum-distance object
    crop that object to its bounding box and return it
```


## M21 — Complete each object to 180° symmetry in its own box


**What it tests:** per-object symmetry completion


**Train A input**
```text
000000000
040000000
044000000
000000000
000002000
000002200
000000000
000000000
```

**Train A output**
```text
000000000
044000000
044000000
000000000
000002200
000002200
000000000
000000000
```

**Train B input**
```text
00003000
00003300
00000000
00000000
06000000
06000000
06600000
00000000
```

**Train B output**
```text
00003300
00003300
00000000
00000000
06600000
06600000
06600000
00000000
```

**Test input**
```text
000000000
000000000
001000000
001100000
000000000
000000700
000000700
000007700
000000000
```

**Expected test output**
```text
000000000
000000000
001100000
001100000
000000000
000007700
000007700
000007700
000000000
```

**Written solution**
For each connected object, look only inside its own bounding box. Add the cells needed so that the object becomes 180-degree rotationally symmetric within that box.


**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each component:
        get its bounding box
        for each cell (r,c) in the component:
            add the reflected cell (r0+r1-r, c0+c1-c) in the same color
    return out
```


# Hard (7)


## H15 — Control cell chooses OR, XOR, or AND


**What it tests:** control-conditioned boolean composition of aligned shapes


**Train A input**
```text
3000000000
0100002200
0110002000
0000000000
0000000000
0000000000
0000000000
```

**Train A output**
```text
88
88
```

**Train B input**
```text
4000000000
0000002000
0000002200
0100000200
0111000000
0000000000
0000000000
```

**Train B output**
```text
000
008
080
```

**Train C input**
```text
5000000000
0110000000
0010002200
0010000200
0000000200
0000000000
0000000000
```

**Train C output**
```text
88
08
08
```

**Test input**
```text
4000000000
0100000000
0111000000
0000000000
0000002200
0000000200
0000000200
0000000000
```

**Expected test output**
```text
080
808
080
```

**Written solution**
Crop the color-1 object and color-2 object to their own bounding boxes and align them to the top-left. The control cell selects the merge rule: 3 means OR, 4 means XOR, and 5 means AND. Paint the resulting aligned shape in cyan(8).


**Program solution (reference algorithm)**
```python
def solve(grid):
    ctrl = grid[0][0]
    s1, s2 = normalized shapes of colors 1 and 2
    for each aligned cell:
        if ctrl == 3: use OR
        if ctrl == 4: use XOR
        if ctrl == 5: use AND
        paint true cells with 8
    return out
```


## H16 — Control cell chooses the template rotation


**What it tests:** control-conditioned rotation; cropped output


**Train A input**
```text
2000000
0000000
0010000
0011000
0000000
0000000
0000000
```

**Train A output**
```text
80
88
```

**Train B input**
```text
3000000
0000000
0001000
0001100
0000000
0000000
0000000
```

**Train B output**
```text
88
80
```

**Train C input**
```text
40000000
00000000
00110000
00010000
00010000
00000000
00000000
```

**Train C output**
```text
80
80
88
```

**Test input**
```text
50000000
00000000
00100000
00100000
00110000
00000000
00000000
00000000
```

**Expected test output**
```text
008
888
```

**Written solution**
Take the color-1 template, crop it to its bounding box, and rotate it according to the control cell: 2 means 0°, 3 means 90° clockwise, 4 means 180°, and 5 means 270° clockwise. Output the rotated template in cyan(8), cropped to fit.


**Program solution (reference algorithm)**
```python
def solve(grid):
    ctrl = the control color in {2,3,4,5}
    shape = normalized color-1 template
    rotate by 0/1/2/3 quarter-turns according to ctrl
    paint the rotated result with 8 in a cropped output grid
```


## H17 — Fill each frame by the largest enclosed object


**What it tests:** nested-region analysis; size comparison


**Train A input**
```text
000000000000
055555000000
052205055550
050035054650
050335054450
055555056450
000000055550
000000000000
000000000000
```

**Train A output**
```text
000000000000
055555000000
053335055550
053335054450
053335054450
055555054450
000000055550
000000000000
000000000000
```

**Train B input**
```text
0000000000
5555000000
5775000000
5725000000
5555000000
0000055550
0000053350
0000053450
0000055550
0000000000
```

**Train B output**
```text
0000000000
5555000000
5775000000
5775000000
5555000000
0000055550
0000053350
0000053350
0000055550
0000000000
```

**Test input**
```text
000000000000
055555000000
052205000000
052005055550
050075054650
055555054650
000000054450
000000055550
000000000000
000000000000
```

**Expected test output**
```text
000000000000
055555000000
052225000000
052225055550
052225054450
055555054450
000000054450
000000055550
000000000000
000000000000
```

**Written solution**
Each gray(5) rectangular frame contains several small colored objects. For each frame, find the largest enclosed object by cell count and fill the entire interior of that frame with the winner's color, keeping the gray border.


**Program solution (reference algorithm)**
```python
def solve(grid):
    keep all gray frame cells
    for each gray rectangular frame:
        find all enclosed non-gray components
        choose the largest one
        fill the frame interior with that component color
    return out
```


## H18 — Voronoi-fill the chamber from its seeds


**What it tests:** multi-source BFS around walls


**Train A input**
```text
00000000000
05555555550
05200500050
05000500050
05000000050
05000500050
05000500350
05555555550
00000000000
```

**Train A output**
```text
00000000000
05555555550
05222533350
05222533350
05222233350
05222533350
05222533350
05555555550
00000000000
```

**Train B input**
```text
0000000000
0555555550
0500000250
0500000050
0555055550
0540000050
0555555550
0000000000
```

**Train B output**
```text
0000000000
0555555550
0522222250
0522222250
0555455550
0544444450
0555555550
0000000000
```

**Test input**
```text
000000000000
055555555550
052050000050
050050000050
050050000050
050055505550
050000000050
050050000350
055555555550
000000000000
```

**Expected test output**
```text
000000000000
055555555550
052253333350
052253333350
052253333350
052255535550
052223333350
052253333350
055555555550
000000000000
```

**Written solution**
Gray(5) cells are walls. Nonzero non-wall cells are colored seeds. Fill every reachable empty cell with the color of the nearest seed, measuring distance through open cells; when distances tie, the smaller color wins.


**Program solution (reference algorithm)**
```python
def solve(grid):
    run a multi-source BFS from all seed cells at once
    do not cross wall cells (5)
    assign each open cell to its nearest seed color
    break equal-distance ties by smaller color
    return the filled chamber with walls preserved
```


## H19 — Extract the nth-largest object


**What it tests:** ranked object selection by control value


**Train A input**
```text
1000000000
0330000000
0300000000
0000000000
0000004000
0000004000
0070000000
0000000000
```

**Train A output**
```text
33
30
```

**Train B input**
```text
2000000000
0000000600
0000000660
0000000060
0000000000
0200000000
0220000000
0000003300
0000000000
```

**Train B output**
```text
20
22
```

**Train C input**
```text
300000000
044000000
004000000
004000000
000000000
000007000
000007700
022000000
000000000
```

**Train C output**
```text
22
```

**Test input**
```text
2000000000
0600000000
0660000000
0066000000
0000000000
0000004000
0000004400
0000000000
0077000000
0000000000
```

**Expected test output**
```text
40
44
```

**Written solution**
The top-left control cell gives a rank n. Ignore that control cell, sort the remaining objects by size from largest to smallest, take the nth object, and output it alone cropped to its bounding box.


**Program solution (reference algorithm)**
```python
def solve(grid):
    n = top-left control value
    ignore the control cell
    find all remaining objects and sort by descending size
    take the nth one
    crop it to its bounding box and return it
```


## H20 — Complete 90° rotational symmetry around the pivot


**What it tests:** global rotational closure


**Train A input**
```text
0000000
0001000
0000100
0002000
0000000
0000000
0000000
```

**Train A output**
```text
0000000
0001000
0010100
0102010
0010100
0001000
0000000
```

**Train B input**
```text
000000000
000000000
000110000
000010000
000020000
000000000
000000000
000000000
000000000
```

**Train B output**
```text
000000000
000000000
000110000
000010100
001121100
001010000
000011000
000000000
000000000
```

**Test input**
```text
000000000
000010000
000001000
000001000
000020000
000000000
000000000
000000000
000000000
```

**Expected test output**
```text
000000000
000010000
000001000
001101000
010020010
000101100
000100000
000010000
000000000
```

**Written solution**
The red(2) cell is the rotation center. Every blue(1) cell must be completed into its full 4-way orbit under 90-degree rotations around that pivot. Keep the pivot and paint all rotated copies blue.


**Program solution (reference algorithm)**
```python
def solve(grid):
    find the pivot
    for each blue cell:
        generate its 0°, 90°, 180°, and 270° rotations about the pivot
        paint all valid rotated positions blue
    keep the pivot as 2
    return out
```


## H21 — Fill each compartment with its majority marker color


**What it tests:** region partitioning; majority counting


**Train A input**
```text
000000000000
055555555550
052200503050
052000503350
055555555550
054400502250
054400522250
055555555550
000000000000
```

**Train A output**
```text
000000000000
055555555550
052222533350
052222533350
055555555550
054444522250
054444522250
055555555550
000000000000
```

**Train B input**
```text
0000000000
0555555550
0530502250
0530500250
0500500050
0500555550
0500504450
0500504450
0555555550
0000000000
```

**Train B output**
```text
0000000000
0555555550
0533522250
0533522250
0533522250
0533555550
0533544450
0533544450
0555555550
0000000000
```

**Test input**
```text
000000000000
055555555550
053005022050
053305002050
050005002050
055555555550
054405030050
054445033050
055555555550
000000000000
```

**Expected test output**
```text
000000000000
055555555550
053335222250
053335222250
053335222250
055555555550
054445333350
054445333350
055555555550
000000000000
```

**Written solution**
Gray(5) walls partition the board into compartments. Inside each compartment, count the colored markers; then fill the entire compartment with the majority marker color, leaving the walls intact.


**Program solution (reference algorithm)**
```python
def solve(grid):
    find each non-wall connected compartment
    count how many markers of each color it contains
    choose the majority color
    fill the whole compartment with that color
    keep all wall cells as 5
```
