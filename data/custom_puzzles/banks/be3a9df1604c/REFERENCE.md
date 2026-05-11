# ARC-style Puzzle Bank — 21 more puzzles (set 9)

This ninth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans into frontier layers, masked distances, anchor transfer, legend matching, unmatched-shape detection, corner stamping, and panel-majority reasoning.

This set introduces a new helper primitive:

```text
frontier_layers(grid, seeds, passable=None, blockers=None, connectivity=4)
  Return BFS distance layers expanding from one or more seed cells through passable cells, either by passable colors or by an explicit set of allowed coordinates.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set9_reference.py`.


## Index

### Easy

- **S9_E1** — Halo at Distance One
- **S9_E2** — Fill the Repeated-Color Box
- **S9_E3** — Recolor Horizontal Endpoints
- **S9_E4** — Keep Border Touchers
- **S9_E5** — Mirror Across the Divider
- **S9_E6** — Count Dots, Build a Bar
- **S9_E7** — Row Interval Fill


### Medium

- **S9_M1** — Nearest Seed with Blank Ties
- **S9_M2** — Odd Room Layers
- **S9_M3** — Anchor-Vector Copy
- **S9_M4** — Recolor by Area Rank
- **S9_M5** — Select the Object Matching the Top Count
- **S9_M6** — Rectangle Corners Only
- **S9_M7** — Connect Aligned Pairs


### Hard

- **S9_H1** — Masked Voronoi with Tie Color
- **S9_H2** — Rotation-Legend Anchor Copy
- **S9_H3** — Find the Unmatched Shape
- **S9_H4** — Double-Legend Feature Match
- **S9_H5** — Four-Corner Template Stamping
- **S9_H6** — Odd Voronoi Layers in a Mask
- **S9_H7** — Three-Panel Majority Merge


# Easy

## S9_E1 — Halo at Distance One

**Skills:** distance-1 frontier, same-size transform, seed expansion

**Primitive note:** Uses the new frontier_layers primitive at distance 1.

**Scaffold:**
- Find the nonzero seed cells.
- Look only one orthogonal step away from each seed.
- Paint those frontier cells cyan(8) and keep the seeds.

**Train 1 input**
```text
0000000
0200000
0000000
0000000
0000030
0000000
0000000
```
**Train 1 output**
```text
0800000
8280000
0800000
0000080
0000838
0000080
0000000
```
**Train 2 input**
```text
00000000
00000000
00000400
00000000
00000000
00600000
00000000
00000000
```
**Train 2 output**
```text
00000000
00000800
00008480
00000800
00800000
08680000
00800000
00000000
```
**Test input**
```text
000000000
000000020
000000000
000000000
000030000
000000000
000000000
040000000
000000000
```
**Test output**
```text
000000080
000000828
000000080
000080000
000838000
000080000
080000000
848000000
080000000
```
**Written solution:** Keep every original nonzero seed cell. Then add cyan(8) to every background cell at Manhattan distance exactly 1 from some seed. The expansion is only one layer thick, so only the four orthogonal neighbors of each seed are added.

**Reference program:**
```python
def solve_S9_E1(grid):
    out=copyg(grid)
    seeds=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    for seed in seeds:
        layers=frontier_layers(grid, [seed], passable={0}, connectivity=4)['layers']
        for r,c in layers.get(1, []):
            if out[r][c]==0:
                out[r][c]=8
    return out
```

## S9_E2 — Fill the Repeated-Color Box

**Skills:** color counting, bounding box, constructive fill

**Scaffold:**
- Find which color appears exactly twice.
- Use those two cells as opposite corners of a box.
- Fill the whole box with that color and ignore the distractors.

**Train 1 input**
```text
00000001
04000000
00000000
00000000
00000400
00000000
20000000
```
**Train 1 output**
```text
00000000
04444400
04444400
04444400
04444400
00000000
00000000
```
**Train 2 input**
```text
000000000
030000000
000070000
000000000
000000000
000000000
000000070
000000000
```
**Train 2 output**
```text
000000000
000000000
000077770
000077770
000077770
000077770
000077770
000000000
```
**Test input**
```text
1000000000
0000006000
0000000000
0000000000
0000000000
0060000000
0000000003
```
**Test output**
```text
0000000000
0066666000
0066666000
0066666000
0066666000
0066666000
0000000000
```
**Written solution:** Identify the unique nonzero color that appears exactly twice. Take the bounding box of those two matching cells and fill that entire rectangle with the repeated color. Any other nonzero singletons are distractors and disappear.

**Reference program:**
```python
def solve_S9_E2(grid):
    by={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v, []).append((r,c))
    color, cells = next((color,cells) for color,cells in by.items() if len(cells)==2)
    r1,c1,r2,c2=bbox(cells)
    out=blank(len(grid), len(grid[0]), 0)
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            out[r][c]=color
    return out
```

## S9_E3 — Recolor Horizontal Endpoints

**Skills:** run detection, local recolor, row-wise processing

**Scaffold:**
- Read each row independently.
- Find every contiguous horizontal nonzero run.
- Change the first and last cell of each run to blue(1).

**Train 1 input**
```text
000000000000
022220044400
003000000500
066666000000
000077700880
000000000000
```
**Train 1 output**
```text
000000000000
012210014100
001000000100
016661000000
000017100110
000000000000
```
**Train 2 input**
```text
000000000000
044400022220
000600700000
088888000990
000033000000
000000000000
```
**Train 2 output**
```text
000000000000
014100012210
000100100000
018881000110
000011000000
000000000000
```
**Test input**
```text
000000000000
055500077000
000400000900
022222200000
000066000330
000000000000
```
**Test output**
```text
000000000000
015100011000
000100000100
012222100000
000011000110
000000000000
```
**Written solution:** Process each row separately. For every contiguous horizontal run of a nonzero color, recolor its leftmost and rightmost cells to blue(1). The interior cells of the run stay in their original color; a run of length 1 simply becomes blue(1).

**Reference program:**
```python
def solve_S9_E3(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        c=0
        while c<w:
            if grid[r][c]==0:
                c+=1
                continue
            v=grid[r][c]
            c0=c
            while c+1<w and grid[r][c+1]==v:
                c+=1
            c1=c
            out[r][c0]=1
            out[r][c1]=1
            c+=1
    return out
```

## S9_E4 — Keep Border Touchers

**Skills:** component extraction, border test, object filtering

**Scaffold:**
- Split the picture into connected nonzero objects.
- Ask which objects touch the outer border of the grid.
- Keep only those border-touching objects.

**Train 1 input**
```text
00000440
20000000
20033000
20033000
00000000
06000000
06600000
00000000
```
**Train 1 output**
```text
00000440
20000000
20000000
20000000
00000000
00000000
00000000
00000000
```
**Train 2 input**
```text
033000000
033000007
000000007
000000007
000022000
000022000
004400000
004400000
000000000
```
**Train 2 output**
```text
033000000
033000007
000000007
000000007
000000000
000000000
000000000
000000000
000000000
```
**Test input**
```text
555000000
000000000
000000006
000220006
000220006
000220000
077000000
007000000
```
**Test output**
```text
555000000
000000000
000000006
000000006
000000006
000000000
077000000
007000000
```
**Written solution:** Find the connected nonzero components. Preserve exactly the components that touch at least one outer border cell of the grid, keeping their original colors and positions. Remove every fully interior component.

**Reference program:**
```python
def solve_S9_E4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out
```

## S9_E5 — Mirror Across the Divider

**Skills:** reflection, divider detection, copying motifs

**Scaffold:**
- Locate the solid vertical divider of color 5.
- Treat the left side as the source motif.
- Reflect every left-side colored cell across the divider onto the right.

**Train 1 input**
```text
00000500000
02000500000
02200500000
00000500000
30000500000
00300500000
00000500000
```
**Train 1 output**
```text
00000500000
02000500020
02200500220
00000500000
30000500003
00300500300
00000500000
```
**Train 2 input**
```text
000050000
200050000
020050000
002050000
000050000
030050000
300050000
000050000
```
**Train 2 output**
```text
000050000
200050002
020050020
002050200
000050000
030050030
300050003
000050000
```
**Test input**
```text
0000005000000
0404005000000
0040005000000
0000005000000
2000005000000
0020005000000
0000005000000
```
**Test output**
```text
0000005000000
0404005004040
0040005000400
0000005000000
2000005000002
0020005000200
0000005000000
```
**Written solution:** Find the full-height divider column colored 5. Copy every nonzero, non-divider cell from the left side to the horizontally mirrored position on the right side, using the same color. Keep the original left motif and the divider as they are.

**Reference program:**
```python
def solve_S9_E5(grid):
    h,w=dims(grid)
    divider = next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    out=copyg(grid)
    for r in range(h):
        for c in range(divider):
            v=grid[r][c]
            if v not in (0,5):
                mc = 2*divider - c
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

## S9_E6 — Count Dots, Build a Bar

**Skills:** counting, constructive output, same-color synthesis

**Scaffold:**
- Count how many nonzero dots are present.
- Notice they are all the same color.
- Build a left-aligned bar of that length on the bottom row.

**Train 1 input**
```text
0000000
0300000
0000030
0000000
0003000
3000000
0000000
```
**Train 1 output**
```text
0000000
0000000
0000000
0000000
0000000
0000000
3333000
```
**Train 2 input**
```text
00000000
00000060
00600000
00006000
00000000
06000000
00000006
00000000
```
**Train 2 output**
```text
00000000
00000000
00000000
00000000
00000000
00000000
00000000
66666000
```
**Test input**
```text
000000000
020000020
000020000
200000000
000000002
000200000
000000200
000000000
```
**Test output**
```text
000000000
000000000
000000000
000000000
000000000
000000000
000000000
222222200
```
**Written solution:** Count the total number of nonzero cells and note their shared color. Erase everything else, and draw a left-aligned bar of that many cells on the bottom row in the same color.

**Reference program:**
```python
def solve_S9_E6(grid):
    h,w=dims(grid)
    pts=[v for row in grid for v in row if v!=0]
    color=pts[0]
    n=len(pts)
    out=blank(h,w,0)
    for c in range(min(n,w)):
        out[h-1][c]=color
    return out
```

## S9_E7 — Row Interval Fill

**Skills:** pair matching, interval fill, row-wise reasoning

**Scaffold:**
- Look at each row separately.
- Find rows containing two markers of the same color.
- Fill the whole segment between them, inclusive, with that color.

**Train 1 input**
```text
000000000000
020000200000
000000030300
000000000000
400040000000
000000000000
```
**Train 1 output**
```text
000000000000
022222200000
000000033300
000000000000
444440000000
000000000000
```
**Train 2 input**
```text
000000000000
000500000050
060000000600
000000700007
000000000000
080000080000
```
**Train 2 output**
```text
000000000000
000555555550
066666666600
000000777777
000000000000
088888880000
```
**Test input**
```text
000000000000
002000000200
000040000400
000000500005
600000000006
000000000000
```
**Test output**
```text
000000000000
002222222200
000044444400
000000555555
666666666666
000000000000
```
**Written solution:** For each row, if a color appears exactly twice, fill every cell between those two positions with that color, including the endpoints. Rows without such a matched pair stay blank.

**Reference program:**
```python
def solve_S9_E7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        by={}
        for c,v in enumerate(grid[r]):
            if v!=0:
                by.setdefault(v, []).append(c)
        for color, cols in by.items():
            if len(cols)==2:
                a,b=min(cols), max(cols)
                for c in range(a,b+1):
                    out[r][c]=color
    return out
```

# Medium

## S9_M1 — Nearest Seed with Blank Ties

**Skills:** distance comparison, territory partition, tie handling

**Primitive note:** Uses frontier_layers to compute the two distance maps.

**Scaffold:**
- There are two colored seeds.
- Assign each background cell to the nearer seed by Manhattan distance.
- If a cell is equally far from both, leave it black(0).

**Train 1 input**
```text
0000000
0200000
0000000
0000000
0000000
0000030
0000000
```
**Train 1 output**
```text
2222200
2222200
2222033
2220333
2203333
0033333
0033333
```
**Train 2 input**
```text
00000000
00000200
00000000
00000000
00000000
00000000
03000000
00000000
```
**Train 2 output**
```text
22222222
22222222
33222222
33322222
33332222
33333222
33333333
33333333
```
**Test input**
```text
000000000
000000020
000000000
000000000
000000000
000000000
000000000
000300000
000000000
```
**Test output**
```text
222222222
222222222
000022222
333302222
333330222
333333022
333333300
333333333
333333333
```
**Written solution:** Treat the two seeds as competing sources. Fill each background cell with the color of the nearer seed, using Manhattan distance. Cells equidistant from the two seeds remain black(0), so the tie line stays empty.

**Reference program:**
```python
def solve_S9_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    p2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    p3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [p2], passable={0,2,3})['dist']
    d3=frontier_layers(grid, [p3], passable={0,2,3})['dist']
    for r in range(h):
        for c in range(w):
            if (r,c)==p2:
                out[r][c]=2
            elif (r,c)==p3:
                out[r][c]=3
            else:
                a=d2.get((r,c))
                b=d3.get((r,c))
                if a is None or b is None or a==b:
                    out[r][c]=0
                elif a<b:
                    out[r][c]=2
                else:
                    out[r][c]=3
    return out
```

## S9_M2 — Odd Room Layers

**Skills:** room reachability, BFS layering, parity selection

**Primitive note:** Uses frontier_layers inside a blocked room.

**Scaffold:**
- Use the walls as blockers.
- Start from the seed inside the room.
- Color only the cells at odd shortest-path distance from that seed.

**Train 1 input**
```text
000000000
099999990
090000090
090000090
090020090
090000090
090000090
099999990
000000000
```
**Train 1 output**
```text
000000000
099999990
090808090
098080890
090828090
098080890
090808090
099999990
000000000
```
**Train 2 input**
```text
0000000000
0999999990
0900900090
0900990990
0900900090
0900000090
0900902090
0900900090
0999999990
0000000000
```
**Train 2 output**
```text
0000000000
0999999990
0908980890
0980998990
0908980890
0980808090
0908982890
0980908090
0999999990
0000000000
```
**Test input**
```text
0000000000
0999999990
0920009090
0900000090
0900009090
0900009090
0999099090
0900000090
0999999990
0000000000
```
**Test output**
```text
0000000000
0999999990
0928089890
0980808090
0908089890
0980809090
0999099890
0980808090
0999999990
0000000000
```
**Written solution:** Keep the walls and the seed. Within the wall-bounded accessible region, compute shortest-path distance from the seed using 4-neighbor motion. Color exactly the odd-distance cells cyan(8) and leave the even-distance cells black(0).

**Reference program:**
```python
def solve_S9_M2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                out[r][c]=9
    seed=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    out[seed[0]][seed[1]]=2
    dist=frontier_layers(grid, [seed], passable={0,2}, blockers={})['dist']
    for (r,c),d in dist.items():
        if (r,c)==seed or grid[r][c]==9:
            continue
        if d%2==1:
            out[r][c]=8
    return out
```

## S9_M3 — Anchor-Vector Copy

**Skills:** translation vector, shape copying, anchor correspondence

**Scaffold:**
- Find the source object and the source anchor 3.
- Find the target anchor 4.
- Translate the whole source object by the anchor-to-anchor vector.

**Train 1 input**
```text
0000000000
0300000400
0020000000
0020000000
0022000000
0000000000
0000000000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000400
0000000080
0000000080
0000000088
0000000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
0000000000
0000004000
0000000000
3000000000
0022000000
0220000000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000004000
0000000088
0000000880
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Test input**
```text
00000000000
00000004000
00000000000
00000000000
03000000000
00222000000
00020000000
00020000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000004000
00000000888
00000000080
00000000080
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Written solution:** Compute the translation vector from the source anchor 3 to the target anchor 4. Copy the source object by that vector into its new position, recoloring the copied object cyan(8), and keep the target anchor 4. The original source side disappears.

**Reference program:**
```python
def solve_S9_M3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comp=components(grid, colors={2})[0]['cells']
    s=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    t=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4][0]
    dr,dc=t[0]-s[0], t[1]-s[1]
    out[t[0]][t[1]]=4
    for r,c in comp:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out
```

## S9_M4 — Recolor by Area Rank

**Skills:** component sizing, ranking, color reassignment

**Scaffold:**
- Measure the area of each connected object.
- Order the objects from smallest to largest.
- Recolor them by rank: 2, then 3, then 4.

**Train 1 input**
```text
000000000
055500000
000000600
000006660
000000600
007770000
007770000
000000000
```
**Train 1 output**
```text
000000000
022200000
000000300
000003330
000000300
004440000
004440000
000000000
```
**Train 2 input**
```text
0000000000
0400000000
0400005500
0000005500
0000000000
0006000000
0006000000
0006660000
0000000000
```
**Train 2 output**
```text
0000000000
0200000000
0200003300
0000003300
0000000000
0004000000
0004000000
0004440000
0000000000
```
**Test input**
```text
00000000000
00000009900
00000009000
00000000000
08888000000
00000000700
00000007770
00000000700
00000000000
```
**Test output**
```text
00000000000
00000002200
00000002000
00000000000
03333000000
00000000400
00000004440
00000000400
00000000000
```
**Written solution:** Find the connected objects and sort them by area. The smallest object is recolored red(2), the middle one green(3), and the largest yellow(4), while their shapes and positions stay unchanged.

**Reference program:**
```python
def solve_S9_M4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid)
    comps=sorted(comps, key=lambda comp: len(comp['cells']))
    rank_colors=[2,3,4]
    for comp,newc in zip(comps, rank_colors):
        for r,c in comp['cells']:
            out[r][c]=newc
    return out
```

## S9_M5 — Select the Object Matching the Top Count

**Skills:** count-to-object matching, area measurement, object selection

**Scaffold:**
- Count the marker dots in the top row.
- Measure the area of each candidate object below.
- Keep only the object whose area matches the top-row count.

**Train 1 input**
```text
0101010110
0000000000
0000000000
0020003000
0222003000
0020003300
0000444000
0000444000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0080000000
0888000000
0080000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
0010101010
0000000000
0000000000
0022000300
0220003330
0000000300
0000040000
0000040000
0000040000
```
**Train 2 output**
```text
0000000000
0000000000
0000000000
0088000000
0880000000
0000000000
0000000000
0000000000
0000000000
```
**Test input**
```text
01101010110
00000000000
00000000000
00200033300
02220033300
00200000000
00400000000
00400000000
00440000000
```
**Test output**
```text
00000000000
00000000000
00000000000
00000088800
00000088800
00000000000
00000000000
00000000000
00000000000
```
**Written solution:** The top row encodes a target number by its count of marker dots. Among the candidate objects below, keep only the one whose area equals that count, and recolor that chosen object cyan(8). Everything else disappears.

**Reference program:**
```python
def solve_S9_M5(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    out=blank(h,w,0)
    for comp in components(grid):
        if comp['color']==1:
            continue
        if any(r==0 for r,c in comp['cells']):
            continue
        if len(comp['cells'])==target:
            for r,c in comp['cells']:
                out[r][c]=8
            break
    return out
```

## S9_M6 — Rectangle Corners Only

**Skills:** rectangle detection, bounding boxes, corner extraction

**Scaffold:**
- Each nonzero object is a filled rectangle.
- Find the rectangle’s bounding box.
- Keep only its four corners.

**Train 1 input**
```text
0000000000
0222000000
0222000000
0222000000
0000003330
0000003330
0000003330
0000000000
```
**Train 1 output**
```text
0000000000
0808000000
0000000000
0808000000
0000008080
0000000000
0000008080
0000000000
```
**Train 2 input**
```text
000000000000
004444000000
004444000000
000000000000
066600000000
066600007770
066600007770
000000007770
000000000000
```
**Train 2 output**
```text
000000000000
008008000000
008008000000
000000000000
080800000000
000000008080
080800000000
000000008080
000000000000
```
**Test input**
```text
00000000000
02222000000
02222000000
02222000000
00000033330
00000033330
00000033330
00000033330
00000000000
```
**Test output**
```text
00000000000
08008000000
00000000000
08008000000
00000080080
00000000000
00000000000
00000080080
00000000000
```
**Written solution:** For each filled rectangle, determine its bounding box and mark only the four corner cells. All surviving corner cells are recolored cyan(8); every other cell becomes black(0).

**Reference program:**
```python
def solve_S9_M6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        r1,c1,r2,c2=bbox(comp['cells'])
        for cell in [(r1,c1),(r1,c2),(r2,c1),(r2,c2)]:
            out[cell[0]][cell[1]]=8
    return out
```

## S9_M7 — Connect Aligned Pairs

**Skills:** pair matching, line drawing, horizontal/vertical alignment

**Scaffold:**
- Group the colored marker pairs by color.
- Check whether each pair is horizontal or vertical.
- Draw the straight segment between the two markers.

**Train 1 input**
```text
0000000000
0200020000
0000000300
0000000000
0000000000
0040400000
0000000300
0000000000
```
**Train 1 output**
```text
0000000000
0222220000
0000000300
0000000300
0000000300
0044400300
0000000300
0000000000
```
**Train 2 input**
```text
00000000000
00000000707
00600000000
00000000000
00000000000
00000800000
00000000000
00600000000
00000800000
```
**Train 2 output**
```text
00000000000
00000000777
00600000000
00600000000
00600000000
00600800000
00600800000
00600800000
00000800000
```
**Test input**
```text
000000000000
000000000200
030000300000
000000000000
000000000000
000000000200
000400000004
000000000000
```
**Test output**
```text
000000000000
000000000200
033333300200
000000000200
000000000200
000000000200
000444444444
000000000000
```
**Written solution:** Each color appears as a pair of single markers that are either horizontally or vertically aligned. Fill the straight segment joining each pair, inclusive of the endpoints, using that pair’s color.

**Reference program:**
```python
def solve_S9_M7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    by={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v, []).append((r,c))
    for color,cells in by.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            a,b=sorted([c1,c2])
            for c in range(a,b+1):
                out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            for r in range(a,b+1):
                out[r][c1]=color
    return out
```

# Hard

## S9_H1 — Masked Voronoi with Tie Color

**Skills:** masked distances, territory assignment, tie color

**Primitive note:** Uses frontier_layers on an irregular masked region.

**Scaffold:**
- Only the mask cells matter; outside the mask stays black.
- Compare shortest-path distance from every mask cell to seed 2 and seed 3.
- Use color 8 on exact ties.

**Train 1 input**
```text
0000000000
0072777000
0070007000
0077777000
0077070000
0077777300
0000777000
0000000000
```
**Train 1 output**
```text
0000000000
0022222000
0020002000
0022838000
0028030000
0083333300
0000333000
0000000000
```
**Train 2 input**
```text
00000000000
00077770000
00770077000
00727777000
00777000000
00777773000
00077770000
00000000000
```
**Train 2 output**
```text
00000000000
00022220000
00220022000
00222222000
00222000000
00228333000
00028330000
00000000000
```
**Test input**
```text
00000000000
00777777000
00720077000
00777777000
00077770000
00077077000
00077773000
00000000000
```
**Test output**
```text
00000000000
00222222000
00220088000
00222288000
00022830000
00028033000
00083333000
00000000000
```
**Written solution:** Work only inside the mask region. Compute shortest-path distance within the mask from each cell to seed 2 and seed 3. Fill the cell with 2 if seed 2 is nearer, with 3 if seed 3 is nearer, and with cyan(8) if the distances tie. Outside the mask remains black(0).

**Reference program:**
```python
def solve_S9_H1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    allowed={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7 or v in (2,3)}
    s2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    s3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [s2], passable=allowed)['dist']
    d3=frontier_layers(grid, [s3], passable=allowed)['dist']
    for r,c in allowed:
        if (r,c)==s2:
            out[r][c]=2
        elif (r,c)==s3:
            out[r][c]=3
        else:
            a=d2.get((r,c))
            b=d3.get((r,c))
            if a==b:
                out[r][c]=8
            elif a<b:
                out[r][c]=2
            else:
                out[r][c]=3
    return out
```

## S9_H2 — Rotation-Legend Anchor Copy

**Skills:** rotation decoding, shape normalization, anchored placement

**Scaffold:**
- Read the 2×2 legend in the corner to determine the rotation.
- Normalize and rotate the source object accordingly.
- Place the rotated copy with its top-left at the target anchor.

**Train 1 input**
```text
0100000000
0000000000
0000004000
0000000000
0200000000
0200000000
0220000000
0000000000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000008880
0000008000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
0000000000
0100000000
0000004000
0000000000
0002200000
0022000000
0000000000
0000000000
0000000000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0000000880
0000008800
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Test input**
```text
00000000000
10000000000
00000004000
00000000000
00000000000
00222000000
00020000000
00020000000
00000000000
00000000000
00000000000
```
**Test output**
```text
00000000000
00000000000
00000008000
00000008880
00000008000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Written solution:** The single 1 in the 2×2 legend encodes one of the four quarter-turn rotations. Normalize the source object, rotate it by the indicated amount, and then place the rotated copy so its bounding box’s top-left corner sits on the anchor 4. Recolor the placed copy cyan(8).

**Reference program:**
```python
def solve_S9_H2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    legend={(0,0):0,(0,1):1,(1,1):2,(1,0):3}
    pos=next((r,c) for r in range(2) for c in range(2) if grid[r][c]==1)
    k=legend[pos]
    shape=components(grid, colors={2})[0]['cells']
    pts=rotate_norm(shape, k)
    anchor=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4][0]
    for dr,dc in pts:
        nr,nc=anchor[0]+dr, anchor[1]+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out
```

## S9_H3 — Find the Unmatched Shape

**Skills:** shape signatures, pair cancellation, translation invariance

**Scaffold:**
- Normalize each connected object by translation.
- Find which normalized shape appears only once.
- Keep only that unmatched object.

**Train 1 input**
```text
000000000000
060000006000
060000006000
066000006600
066600006660
006000000600
006000000600
000000660000
000006600000
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
000000000000
000000880000
000008800000
000000000000
```
**Train 2 input**
```text
000000000000
006000000600
066600006660
006000000600
000000000000
060000006000
060000006000
066006606600
000006600000
000000000000
```
**Train 2 output**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000008800000
000008800000
000000000000
```
**Test input**
```text
0000000000000
0066000000660
0660000006600
0000000000000
0000000000000
0660000006600
0660000006600
0000060000000
0000060000000
0000066600000
0000000000000
```
**Test output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000080000000
0000080000000
0000088800000
0000000000000
```
**Written solution:** Compare the connected objects by normalized shape, ignoring position. Every repeated shape forms a matching pair; exactly one normalized shape appears only once. Preserve that unique object in place and recolor it cyan(8).

**Reference program:**
```python
def solve_S9_H3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid)
    sigs={}
    for idx,comp in enumerate(comps):
        sig=tuple(norm_cells(comp['cells']))
        sigs.setdefault(sig, []).append(idx)
    keep_idx=next(indices[0] for sig,indices in sigs.items() if len(indices)==1)
    for r,c in comps[keep_idx]['cells']:
        out[r][c]=8
    return out
```

## S9_H4 — Double-Legend Feature Match

**Skills:** two-feature lookup, area measurement, bounding-box width

**Scaffold:**
- The top-row markers encode a target area.
- The left-column markers encode a target bounding-box width.
- Choose the object satisfying both features.

**Train 1 input**
```text
010101010100
300000000000
300000000000
302220004000
000200004000
000200004400
000000000000
000066666000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
000000000000
000000000000
008880000000
000800000000
000800000000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 input**
```text
001010101000
300000000000
300000000000
002200004400
002200044000
000006000000
000006000000
000006000000
000006000000
000000000000
```
**Train 2 output**
```text
000000000000
000000000000
000000000000
008800000000
008800000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Test input**
```text
010101010100
300000000000
300000000000
002220004000
000200004000
000200004000
000000004400
000066666000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000000000
000000008000
000000008000
000000008000
000000008800
000000000000
000000000000
000000000000
```
**Written solution:** Count the top-row dots to get the target area, and count the left-column dots to get the target bounding-box width. Among the candidate objects, keep only the one whose area and bounding-box width match both legend values, and recolor it cyan(8).

**Reference program:**
```python
def solve_S9_H4(grid):
    h,w=dims(grid)
    area_target=sum(1 for v in grid[0] if v==1)
    width_target=sum(1 for r in range(h) if grid[r][0]==3)
    out=blank(h,w,0)
    for comp in components(grid):
        if comp['color'] in (1,3):
            continue
        if any(r==0 or c==0 for r,c in comp['cells']):
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        area=len(comp['cells'])
        width=c2-c1+1
        if area==area_target and width==width_target:
            for r,c in comp['cells']:
                out[r][c]=8
            break
    return out
```

## S9_H5 — Four-Corner Template Stamping

**Skills:** template normalization, mirroring/rotation, corner placement

**Scaffold:**
- Extract the small template object.
- Find the large frame and its four interior corners.
- Stamp transformed copies of the template into those four corners so they face inward.

**Train 1 input**
```text
000000000000
020000000000
020000000000
022000000000
000044444440
000040000040
000040000040
000040000040
000040000040
000040000040
000044444440
000000000000
```
**Train 1 output**
```text
000000000000
000000000000
000000000000
000000000000
000044444440
000048000840
000048000840
000048808840
000048000840
000048000840
000044444440
000000000000
```
**Train 2 input**
```text
0000000000000
0002200000000
0022000000000
0000000000000
0000000000000
0000444444440
0000400000040
0000400000040
0000400000040
0000400000040
0000400000040
0000444444440
0000000000000
```
**Train 2 output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000444444440
0000408888040
0000488008840
0000400000040
0000488008840
0000408888040
0000444444440
0000000000000
```
**Test input**
```text
0000000000000
0222000000000
0020000000000
0020000000000
0000000000000
0000444444440
0000400000040
0000400000040
0000400000040
0000400000040
0000400000040
0000444444440
0000000000000
```
**Test output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000444444440
0000488888840
0000408008040
0000408008040
0000408008040
0000488888840
0000444444440
0000000000000
```
**Written solution:** Keep the frame. Normalize the small template and place four copies inside the frame: original in the top-left, horizontally mirrored in the top-right, vertically mirrored in the bottom-left, and 180° rotated in the bottom-right. Recolor the stamped copies cyan(8).

**Reference program:**
```python
def solve_S9_H5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    frame=components(grid, colors={4})[0]['cells']
    for r,c in frame:
        out[r][c]=4
    template=components(grid, colors={2})[0]['cells']
    t0=norm_cells(template)
    t1=mirror_h_norm(template)
    t2=mirror_v_norm(template)
    t3=rotate_norm(template, 2)
    fh1,fw1,fh2,fw2=bbox(frame)
    inner_r1, inner_c1 = fh1+1, fw1+1
    inner_r2, inner_c2 = fh2-1, fw2-1

    def place(pts, top, left):
        for dr,dc in pts:
            out[top+dr][left+dc]=8

    h0=max(r for r,c in t0)+1; w0=max(c for r,c in t0)+1
    h1=max(r for r,c in t1)+1; w1=max(c for r,c in t1)+1
    h2=max(r for r,c in t2)+1; w2=max(c for r,c in t2)+1
    h3=max(r for r,c in t3)+1; w3=max(c for r,c in t3)+1

    place(t0, inner_r1, inner_c1)
    place(t1, inner_r1, inner_c2-w1+1)
    place(t2, inner_r2-h2+1, inner_c1)
    place(t3, inner_r2-h3+1, inner_c2-w3+1)
    return out
```

## S9_H6 — Odd Voronoi Layers in a Mask

**Skills:** masked Voronoi, parity filtering, tie handling

**Primitive note:** Uses frontier_layers twice, then filters the winning territory by distance parity.

**Scaffold:**
- Partition the mask by which seed is closer.
- Ignore even-distance layers from the winning seed.
- Use color 8 on ties.

**Train 1 input**
```text
00000000000
00777777700
00727077700
00777077700
00707770700
00777073700
00777777700
00000000000
```
**Train 1 output**
```text
00000000000
00020202300
00222003000
00020030300
00202300000
00020033300
00230303000
00000000000
```
**Train 2 input**
```text
000000000000
000727777000
000777707000
000770777000
000777777770
000707777770
000777770370
000777777000
000000000000
```
**Train 2 output**
```text
000000000000
000222020000
000020208000
000200080000
000020803030
000208030300
000088300330
000288030000
000000000000
```
**Test input**
```text
000000000000
007277777700
007707707700
007777777700
007770777700
007777770700
007077777700
007777773700
000000000000
```
**Test output**
```text
000000000000
002220202000
000202000000
002020230300
000200303000
002023030300
000030303000
000303033300
000000000000
```
**Written solution:** Again work only inside the mask. Compare masked shortest-path distance to seed 2 and seed 3. If a cell is closer to seed 2 and its distance from seed 2 is odd, color it 2; if it is closer to seed 3 and its distance from seed 3 is odd, color it 3; ties become cyan(8); all even layers vanish to black(0).

**Reference program:**
```python
def solve_S9_H6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    allowed={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7 or v in (2,3)}
    s2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    s3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [s2], passable=allowed)['dist']
    d3=frontier_layers(grid, [s3], passable=allowed)['dist']
    for r,c in allowed:
        if (r,c)==s2:
            out[r][c]=2
        elif (r,c)==s3:
            out[r][c]=3
        else:
            a=d2.get((r,c))
            b=d3.get((r,c))
            if a==b:
                out[r][c]=8
            elif a<b and a%2==1:
                out[r][c]=2
            elif b<a and b%2==1:
                out[r][c]=3
    return out
```

## S9_H7 — Three-Panel Majority Merge

**Skills:** panel parsing, majority vote, shape consensus

**Scaffold:**
- Split the input into three panels using the divider columns.
- Compare occupancy cell by cell across the panels.
- Output a single panel where cells present in at least two panels survive.

**Train 1 input**
```text
22005020050000
02005220050200
22005020052200
00005020050200
00005000050000
00005000050000
```
**Train 1 output**
```text
0800
0800
8800
0800
0000
0000
```
**Train 2 input**
```text
02005000050200
22205020050000
02005222050200
00005020052220
00005000050200
00005000050000
00005000050000
```
**Train 2 output**
```text
0800
0800
0800
0800
0000
0000
0000
```
**Test input**
```text
20005020052000
22005220050200
02005020052200
00005020050200
00005000050000
00005000050000
00005000050000
```
**Test output**
```text
8000
8800
0800
0800
0000
0000
0000
```
**Written solution:** The two full-height divider columns split the input into three equal panels. For each cell position, check how many of the three panels contain a nonzero cell there. If at least two panels agree that the cell is occupied, place cyan(8) in the output; otherwise leave it black(0).

**Reference program:**
```python
def solve_S9_H7(grid):
    h,w=dims(grid)
    divs=[c for c in range(w) if all(grid[r][c]==5 for r in range(h))]
    assert len(divs)==2
    d1,d2=divs
    panels=[
        [row[:d1] for row in grid],
        [row[d1+1:d2] for row in grid],
        [row[d2+1:] for row in grid],
    ]
    ph,pw=dims(panels[0])
    out=blank(ph,pw,0)
    for r in range(ph):
        for c in range(pw):
            occ=sum(1 for p in panels if p[r][c]!=0)
            if occ>=2:
                out[r][c]=8
    return out
```
