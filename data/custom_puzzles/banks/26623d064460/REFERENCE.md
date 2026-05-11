# ARC-style Additional Puzzle Bank — Volume 2 (21 puzzles)

This second volume adds **21 more puzzles** grouped into **7 easy, 7 medium, and 7 hard**.
Each puzzle includes train pairs, a test input, the expected test output, a written rule, and a compact reference-program solution.
The set is deliberately non-overlapping with the first bank: more singleton logic, component ranking, reflection, hole detection, flood fill, symmetry comparison, and template-controlled copying.

# Easy (7)

## E8 — Recolor isolated red singletons

**What it tests:** cardinal-neighbor isolation; singleton detection

**Train A input**
```text
0000000
0200020
0000000
0022200
0000000
0200000
0000000
```
**Train A output**
```text
0000000
0300030
0000000
0022200
0000000
0300000
0000000
```
**Train B input**
```text
2000000
0000200
0000000
0220000
0200200
0000002
0000000
```
**Train B output**
```text
3000000
0000300
0000000
0220000
0200300
0000003
0000000
```
**Test input**
```text
00000000
02000020
00000000
00022000
00000000
02000200
00000000
00000020
```
**Expected test output**
```text
00000000
03000030
00000000
00022000
00000000
03000300
00000000
00000030
```
**Written solution**
Every red(2) cell with no red neighbor above, below, left, or right becomes green(3). Red cells that belong to a larger red shape stay red.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each cell (r,c):
        if grid[r][c] == 2 and none of the 4 cardinal neighbors is 2:
            out[r][c] = 3
    return out
```

## E9 — Fill one-cell horizontal blue gaps

**What it tests:** local row patterning; gap completion

**Train A input**
```text
0000000
0101000
0000000
0010100
0000000
0110000
0000000
```
**Train A output**
```text
0000000
0111000
0000000
0011100
0000000
0110000
0000000
```
**Train B input**
```text
00010100
00000000
01010000
00000000
00100100
00000000
```
**Train B output**
```text
00011100
00000000
01110000
00000000
00100100
00000000
```
**Test input**
```text
000000000
010100000
000000000
000101000
000000000
001010100
000000000
```
**Expected test output**
```text
000000000
011100000
000000000
000111000
000000000
001111100
000000000
```
**Written solution**
Whenever a row contains blue(1), black(0), blue(1) in three consecutive cells, fill the middle gap with blue(1).

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each row r:
        for each middle position c:
            if grid[r][c-1:c+2] == [1,0,1]:
                out[r][c] = 1
    return out
```

## E10 — Mark the centers of vertical green triplets

**What it tests:** exact length-3 vertical detection; center recolor

**Train A input**
```text
0000000
0030000
0030000
0030000
0000000
0003000
0003000
0003000
```
**Train A output**
```text
0000000
0030000
0040000
0030000
0000000
0003000
0004000
0003000
```
**Train B input**
```text
0300000
0300000
0300000
0000000
0000030
0000030
0000030
```
**Train B output**
```text
0300000
0400000
0300000
0000000
0000030
0000040
0000030
```
**Test input**
```text
00030000
00030000
00030000
00000000
00300030
00300030
00300030
00000000
```
**Expected test output**
```text
00030000
00040000
00030000
00000000
00300030
00400040
00300030
00000000
```
**Written solution**
Find every exact vertical run of three green(3) cells. Change only the middle cell of that triplet to yellow(4).

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each cell (r,c) that has neighbors above and below:
        if grid[r-1][c] == grid[r][c] == grid[r+1][c] == 3
           and the run does not continue farther:
            out[r][c] = 4
    return out
```

## E11 — Remove border-touching orange components

**What it tests:** connected components; border contact removal

**Train A input**
```text
7700000
0700000
0007700
0000700
0000000
0000077
0000070
```
**Train A output**
```text
0000000
0000000
0007700
0000700
0000000
0000000
0000000
```
**Train B input**
```text
0000000
0770000
0070000
0000000
0007700
0000707
0000007
```
**Train B output**
```text
0000000
0770000
0070000
0000000
0007700
0000700
0000000
```
**Test input**
```text
77000000
07000000
00007700
00000700
00000000
00000077
00000007
00000000
```
**Expected test output**
```text
00000000
00000000
00007700
00000700
00000000
00000000
00000000
00000000
```
**Written solution**
Any orange(7) connected component that touches any outer border is erased to black(0). Orange components fully inside the grid stay.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each orange component:
        if any cell of the component touches the border:
            erase the whole component in out
    return out
```

## E12 — Add a magenta shadow to each cyan singleton

**What it tests:** singleton detection; one-step copy

**Train A input**
```text
0000000
0080000
0000000
0000800
0000000
0800000
0000000
```
**Train A output**
```text
0000000
0086000
0000000
0000860
0000000
0860000
0000000
```
**Train B input**
```text
00080000
00000000
08000080
00000000
00000800
00000000
```
**Train B output**
```text
00086000
00000000
08600086
00000000
00000860
00000000
```
**Test input**
```text
000000000
008000000
000000000
000080000
000000000
080000080
000000000
```
**Expected test output**
```text
000000000
008600000
000000000
000086000
000000000
086000086
000000000
```
**Written solution**
Each isolated cyan(8) cell stays in place and gains one magenta(6) cell immediately to its right.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each cyan cell with no cyan cardinal neighbor:
        place a 6 in the cell immediately to its right
    return out
```

## E13 — Recolor exact yellow L-triominoes

**What it tests:** small-shape recognition; exact component-size filtering

**Train A input**
```text
0000000
0440000
0400000
0000000
0000440
0000040
0000000
```
**Train A output**
```text
0000000
0110000
0100000
0000000
0000110
0000010
0000000
```
**Train B input**
```text
0000000
0044000
0004000
0000000
0400000
0440000
0000000
```
**Train B output**
```text
0000000
0011000
0001000
0000000
0100000
0110000
0000000
```
**Test input**
```text
00000000
04400000
04000000
00000000
00000440
00000040
00000000
00000000
```
**Expected test output**
```text
00000000
01100000
01000000
00000000
00000110
00000010
00000000
00000000
```
**Written solution**
Any yellow(4) connected component of exactly three cells that forms an L shape is recolored blue(1).

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each yellow component:
        if it has 3 cells and its normalized shape is an L triomino:
            recolor all three cells to 1
    return out
```

## E14 — Add a red cap to every horizontal green segment

**What it tests:** run detection; endpoint extension

**Train A input**
```text
0000000
0330000
0000000
0003330
0000000
0033000
0000000
```
**Train A output**
```text
0000000
0332000
0000000
0003332
0000000
0033200
0000000
```
**Train B input**
```text
00033000
00000000
03330000
00000000
00000330
00000000
```
**Train B output**
```text
00033200
00000000
03332000
00000000
00000332
00000000
```
**Test input**
```text
000000000
003300000
000000000
000333000
000000000
033000000
000000000
```
**Expected test output**
```text
000000000
003320000
000000000
000333200
000000000
033200000
000000000
```
**Written solution**
Each horizontal green(3) run gets one red(2) cell placed immediately to its right end.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each maximal horizontal run of 3s:
        if the cell just to its right is inside the grid and black:
            set that cell to 2
    return out
```

# Medium (7)

## M8 — Recolor the second-largest component

**What it tests:** component ranking by area

**Train A input**
```text
000000000
022000000
022000330
000000330
000044400
000044400
000000000
000000000
```
**Train A output**
```text
000000000
088000000
088000330
000000330
000044400
000044400
000000000
000000000
```
**Train B input**
```text
000000000
011100000
011100000
011100000
000000000
000022000
000022000
000000330
```
**Train B output**
```text
000000000
011100000
011100000
011100000
000000000
000088000
000088000
000000330
```
**Test input**
```text
0000000000
0222000000
0222000000
0000003300
0000003300
0000444400
0000444400
0000000000
0000000000
```
**Expected test output**
```text
0000000000
0888000000
0888000000
0000003300
0000003300
0000444400
0000444400
0000000000
0000000000
```
**Written solution**
Find all non-black connected components. The second-largest one is recolored cyan(8); all others keep their original colors.

**Program solution (reference algorithm)**
```python
def solve(grid):
    comps = list of all nonzero connected components
    sort components by area descending
    recolor the second item in that order to 8
    return modified grid
```

## M9 — Replace each object by its bounding-box outline

**What it tests:** object abstraction; bounding-box construction

**Train A input**
```text
000000000
022000000
022200000
000000330
000000030
000000000
```
**Train A output**
```text
000000000
022200000
022200000
000000330
000000330
000000000
```
**Train B input**
```text
000000000
000440000
000040000
000044000
000000000
001100000
000100000
000000000
```
**Train B output**
```text
000000000
000444000
000404000
000444000
000000000
001100000
001100000
000000000
```
**Test input**
```text
0000000000
0220000000
0222000000
0000004400
0000000400
0000000000
0000011000
0000001000
```
**Expected test output**
```text
0000000000
0222000000
0222000000
0000004400
0000004400
0000000000
0000011000
0000011000
```
**Written solution**
Ignore each object's detailed shape. For every non-black component, draw only the outline of its axis-aligned bounding box in the same color on a blank grid.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = blank grid
    for each nonzero component:
        compute its bounding box
        draw the box perimeter in the component's color
    return out
```

## M10 — Fill rectangles from diagonal corner pairs

**What it tests:** pairing by color; rectangle filling

**Train A input**
```text
000000000
010000000
000000000
000000000
000000010
000000000
000300000
000000300
000000000
```
**Train A output**
```text
000000000
011111110
011111110
011111110
011111110
000000000
000333300
000333300
000000000
```
**Train B input**
```text
000000000
000000400
000000000
000040000
000000000
002000000
000000002
000000000
```
**Train B output**
```text
000000000
000044400
000044400
000044400
000000000
002222222
002222222
000000000
```
**Test input**
```text
0000000000
0100000000
0000000000
0000000100
0000000000
0004000000
0000000000
0000000004
0000000000
```
**Expected test output**
```text
0000000000
0111111100
0111111100
0111111100
0000000000
0004444444
0004444444
0004444444
0000000000
```
**Written solution**
When a color appears exactly twice as diagonal corner markers, fill the entire axis-aligned rectangle spanning those two cells with that color.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    group nonzero cells by color
    for each color that appears exactly twice:
        let the two cells be opposite corners
        fill the rectangle between them with that color
    return out
```

## M11 — Reflect the marked-side object across the divider

**What it tests:** divider detection; control marker; reflection

**Train A input**
```text
000050000
006050000
066050000
000050000
002050000
000050000
000050000
```
**Train A output**
```text
000050000
006050600
066050660
000050000
000050000
000050000
000050000
```
**Train B input**
```text
0000000
0000000
5555555
0002000
0007700
0007000
0000000
```
**Train B output**
```text
0007700
0000000
5555555
0000000
0007700
0007000
0000000
```
**Test input**
```text
0000050000
0006650000
0000650000
0000050000
0000050000
0002050000
0000050000
0000050000
```
**Expected test output**
```text
0000050000
0006656600
0000656000
0000050000
0000050000
0000050000
0000050000
0000050000
```
**Written solution**
A full gray(5) line is the mirror. The red marker(2) tells you which side contains the source object. Copy that side's non-marker, non-divider cells by reflection across the divider, keeping the original source object.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    find the full row or column of 5s
    find the marker 2 to determine the source side
    reflect every nonzero, non-2, non-5 cell from that side across the divider
    erase the marker
    return out
```

## M12 — Extract the holed object to the top-left

**What it tests:** hole detection; canonical placement

**Train A input**
```text
000000000
044440000
040040000
044440000
000000220
000000220
000000000
```
**Train A output**
```text
444400000
400400000
444400000
000000000
000000000
000000000
000000000
```
**Train B input**
```text
000000000
000777000
000707000
000777000
022000000
022000000
000000000
```
**Train B output**
```text
777000000
707000000
777000000
000000000
000000000
000000000
000000000
```
**Test input**
```text
0000000000
0555550000
0500050000
0555550000
0000000000
0000222000
0000202000
0000222000
0000000000
```
**Expected test output**
```text
5555500000
5000500000
5555500000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**
Among all objects, find the only one with an internal hole. Place that object alone at the top-left corner of an otherwise blank output, preserving its shape and color.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = blank grid
    find the nonzero component whose bounding box contains an enclosed 0-hole
    normalize its cells to top-left origin
    paint that normalized shape into out
    return out
```

## M13 — Move the magenta object one step in the marker's direction

**What it tests:** direction control; translation

**Train A input**
```text
0000000
0002000
0006000
0066600
0006000
0000000
```
**Train A output**
```text
0000000
0006000
0066600
0006000
0000000
0000000
```
**Train B input**
```text
00000000
00000000
00100000
00066000
00006000
00006000
00000000
```
**Train B output**
```text
00000000
00000000
00000000
00660000
00060000
00060000
00000000
```
**Test input**
```text
000000000
000000000
000300000
000660000
000060000
000060000
000000000
000000000
```
**Expected test output**
```text
000000000
000000000
000000000
000066000
000006000
000006000
000000000
000000000
```
**Written solution**
A single direction marker tells how to move the magenta(6) object: blue(1)=left, red(2)=up, green(3)=right, yellow(4)=down. Output only the shifted object.

**Program solution (reference algorithm)**
```python
def solve(grid):
    find the single marker among {1,2,3,4}
    map it to a direction vector
    output a blank grid with the 6-object translated by that vector
    return out
```

## M14 — Turn filled rectangles into outlines

**What it tests:** rectangle abstraction; perimeter extraction

**Train A input**
```text
000000000
022200000
022200000
022200000
000000000
000044400
000044400
000000000
```
**Train A output**
```text
000000000
022200000
020200000
022200000
000000000
000044400
000044400
000000000
```
**Train B input**
```text
000000000
000033000
000033000
000000000
055555500
055555500
055555500
000000000
```
**Train B output**
```text
000000000
000033000
000033000
000000000
055555500
050000500
055555500
000000000
```
**Test input**
```text
0000000000
0222200000
0222200000
0222200000
0000000000
0000555500
0000555500
0000555500
0000000000
```
**Expected test output**
```text
0000000000
0222200000
0200200000
0222200000
0000000000
0000555500
0000500500
0000555500
0000000000
```
**Written solution**
Each solid rectangular object is replaced by its perimeter only, keeping the same color.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = blank grid
    for each nonzero component:
        compute its bounding box
        draw only the perimeter of that rectangle in the component's color
    return out
```

# Hard (7)

## H8 — Flood-fill the seed's reachable chamber

**What it tests:** maze reachability; constrained fill

**Train A input**
```text
555555555
520000055
505550055
500050055
505050055
500000055
555555555
```
**Train A output**
```text
555555555
528888855
585558855
588858855
585858855
588888855
555555555
```
**Train B input**
```text
55555555
50020055
50555055
50005055
55505055
50000055
55555555
```
**Train B output**
```text
55555555
58828855
58555855
58885855
55585855
58888855
55555555
```
**Test input**
```text
5555555555
5200000055
5055550055
5000050055
5050050055
5000000055
5555555555
```
**Expected test output**
```text
5555555555
5288888855
5855558855
5888858855
5858858855
5888888855
5555555555
```
**Written solution**
Gray(5) cells are walls. Starting from the red seed(2), fill every reachable black(0) cell with cyan(8), but do not cross walls and do not fill sealed-off pockets.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    start from the 2-cell
    breadth-first search through cells whose value is 0 or 2
    recolor every reached 0-cell to 8
    return out
```

## H9 — Intersect two shapes after top-left alignment

**What it tests:** shape normalization; Boolean intersection

**Train A input**
```text
000000000
022000000
002200000
000200000
000000330
000003300
000000300
000000000
```
**Train A output**
```text
080000000
080000000
000000000
000000000
000000000
000000000
000000000
000000000
```
**Train B input**
```text
220000000
022000000
000000300
000000330
000000030
000000000
```
**Train B output**
```text
800000000
080000000
000000000
000000000
000000000
000000000
```
**Test input**
```text
0000000000
0222000000
0020000000
0000003300
0000033000
0000030000
0000000000
```
**Expected test output**
```text
0880000000
0800000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**
Take the red(2) object and the green(3) object, align their bounding boxes by top-left corner, and output only the overlapping cells in cyan(8) on a blank grid.

**Program solution (reference algorithm)**
```python
def solve(grid):
    extract the 2-object and the 3-object
    normalize both to top-left origin
    intersect their normalized cell sets
    paint the intersection in color 8 on a blank output grid
    return out
```

## H10 — Paint the Cartesian product of marked rows and columns

**What it tests:** row-column selection; combinatorial placement

**Train A input**
```text
010010010
000000000
200000000
000000000
200000000
000000000
000000000
200000000
000000000
```
**Train A output**
```text
000000000
000000000
030030030
000000000
030030030
000000000
000000000
030030030
000000000
```
**Train B input**
```text
00100100
00000000
20000000
00000000
00000000
20000000
00000000
```
**Train B output**
```text
00000000
00000000
00300300
00000000
00000000
00300300
00000000
```
**Test input**
```text
0100010010
0000000000
2000000000
0000000000
0000000000
2000000000
0000000000
2000000000
0000000000
0000000000
```
**Expected test output**
```text
0000000000
0000000000
0300030030
0000000000
0000000000
0300030030
0000000000
0300030030
0000000000
0000000000
```
**Written solution**
Blue(1) markers on the top border select columns. Red(2) markers on the left border select rows. Put green(3) cells at every selected row/column intersection in an otherwise blank output.

**Program solution (reference algorithm)**
```python
def solve(grid):
    rows = all indices r with grid[r][0] == 2
    cols = all indices c with grid[0][c] == 1
    out = blank grid
    for r in rows:
        for c in cols:
            out[r][c] = 3
    return out
```

## H11 — Recolor the symmetry outsider

**What it tests:** dihedral shape comparison; odd-one-out detection

**Train A input**
```text
000000000
044000440
040000040
000000000
044000444
040000400
000000000
```
**Train A output**
```text
000000000
044000440
040000040
000000000
044000888
040000800
000000000
```
**Train B input**
```text
000000000
044000444
004000040
000000000
044000440
004000040
000000000
```
**Train B output**
```text
000000000
044000888
004000080
000000000
044000440
004000040
000000000
```
**Test input**
```text
0000000000
0440000440
0400000040
0000000000
0440004440
0400004000
0000000000
```
**Expected test output**
```text
0000000000
0440000440
0400000040
0000000000
0440008880
0400008000
0000000000
```
**Written solution**
Most yellow(4) objects are the same shape up to rotation or reflection. Find the one object outside that symmetry class and recolor it to cyan(8).

**Program solution (reference algorithm)**
```python
def solve(grid):
    collect all yellow components
    for each one, compute its canonical form under rotations and reflections
    find the canonical form that occurs only once
    recolor that component to 8
    return out
```

## H12 — Fill the annulus between two nested frames

**What it tests:** nested-object reasoning; between-region filling

**Train A input**
```text
000000000
044444440
040000040
040111040
040101040
040111040
040000040
044444440
000000000
```
**Train A output**
```text
000000000
044444440
048888840
048111840
048101840
048111840
048888840
044444440
000000000
```
**Train B input**
```text
0444444440
0400000040
0401111040
0401001040
0401111040
0400000040
0444444440
```
**Train B output**
```text
0444444440
0488888840
0481111840
0481001840
0481111840
0488888840
0444444440
```
**Test input**
```text
0000000000
0444444440
0400000040
0401111040
0401001040
0401001040
0401111040
0400000040
0444444440
0000000000
```
**Expected test output**
```text
0000000000
0444444440
0488888840
0481111840
0481001840
0481001840
0481111840
0488888840
0444444440
0000000000
```
**Written solution**
A large yellow frame(4) surrounds a smaller blue frame(1). Fill every cell inside the outer frame but outside the inner frame with cyan(8), while keeping both frames unchanged.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    find the bounding box of the outer 4-frame and the inner 1-frame
    for each cell inside the outer box:
        if it is outside the inner box and not on the outer border:
            set it to 8
    return out
```

## H13 — Copy rotated template shapes from control markers

**What it tests:** template extraction; rotation control; multi-copy placement

**Train A input**
```text
0330000000
0030000000
0030000000
0000000000
0000100000
0000002000
0000000000
```
**Train A output**
```text
0000000000
0000000000
0000000000
0000000000
0000330000
0000030030
0000033330
```
**Train B input**
```text
033000000
030000000
000000000
000000400
000000000
006000000
000000000
```
**Train B output**
```text
000000000
000000000
000000000
000000030
000000330
003000000
003300000
```
**Test input**
```text
03300000000
00300000000
00300000000
00000000000
00001000000
00000020000
00000000000
00000000040
00000000000
00060000000
00000000000
```
**Expected test output**
```text
00000000000
00000000000
00000000000
00000000000
00003300000
00000300300
00000333300
00000000030
00000000030
00033300033
00030000000
```
**Written solution**
The green(3) template near the corner must be copied at each control marker. Marker color gives the rotation: blue(1)=0°, red(2)=90°, yellow(4)=180°, magenta(6)=270°. Place each rotated copy with the marker as the top-left of its bounding box, and output only the copies.

**Program solution (reference algorithm)**
```python
def solve(grid):
    template = largest 3-colored component
    for each marker in {1,2,4,6}:
        rotate the normalized template by the marker's angle
        stamp that rotated shape onto a blank output with the marker cell as origin
    return out
```

## H14 — Fill each walled compartment from its seed

**What it tests:** multi-source flood fill; compartment separation

**Train A input**
```text
555555555
510055205
500055005
555555555
530055405
500055005
555555555
```
**Train A output**
```text
555555555
511155225
511155225
555555555
533355445
533355445
555555555
```
**Train B input**
```text
55555555
51055025
50055005
55555555
53055045
50055005
55555555
```
**Train B output**
```text
55555555
51155225
51155225
55555555
53355445
53355445
55555555
```
**Test input**
```text
5555555555
5100552055
5000550055
5555555555
5300554055
5000550055
5555555555
```
**Expected test output**
```text
5555555555
5111552255
5111552255
5555555555
5333554455
5333554455
5555555555
```
**Written solution**
Gray(5) walls divide the board into chambers. Each chamber contains one colored seed. Fill all black(0) cells in a chamber with that seed's color, without crossing the walls.

**Program solution (reference algorithm)**
```python
def solve(grid):
    out = copy(grid)
    for each seed cell whose color is in {1,2,3,4}:
        flood-fill through 0s (and the seed itself) until walls stop the search
        recolor all reached 0s to the seed color
    return out
```
