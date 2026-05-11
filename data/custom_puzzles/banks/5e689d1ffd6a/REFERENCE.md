# ARC-style Puzzle Bank — 21 more puzzles (set 7)

This seventh bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans harder into motion, docking, gravity, component packing, constructive outputs, and consensus-style shape reasoning.

This set introduces a new helper primitive:

```text
slide_component(grid, cells, step, blockers=None)
  Repeatedly translate a connected shape one step at a time until the next
  step would leave the grid or hit a blocker.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set7_reference.py`.


## Index

### Easy

- **S7_E1** — Slide the Red Shape Right
- **S7_E2** — Column Gravity Dots
- **S7_E3** — Crop the Interior Rectangle
- **S7_E4** — Solid Bounding Box
- **S7_E5** — Normalize Shape to Top-Left
- **S7_E6** — Topmost Cell in Each Column
- **S7_E7** — Component Count Bar

### Medium

- **S7_M1** — Dock the Shape to the Frame
- **S7_M2** — Rigid Gravity with Walls
- **S7_M3** — Height-Sorted Palette Row
- **S7_M4** — Translate Template by Anchor Vector
- **S7_M5** — Farthest Right-Slide Selector
- **S7_M6** — Row Majority Column
- **S7_M7** — One-Step Object Halo

### Hard

- **S7_H1** — Sequential Arrow Slides
- **S7_H2** — Directional Gravity from Header
- **S7_H3** — Connector Overlay Assembly
- **S7_H4** — Dual Inward Slide
- **S7_H5** — Majority Shape from Shifted Copies
- **S7_H6** — Shelf Pack by Area
- **S7_H7** — Park Shapes in Matching Bays

# Easy

## S7_E1 — Slide the Red Shape Right

**Skills:** object motion, collision stopping, same-size transform

**Primitive note:** Uses the new slide_component primitive.

**Scaffold:**
- Find the unique red(2) connected shape.
- Treat all other nonzero cells as blockers.
- Slide the red shape to the right until the next step would hit a blocker or the boundary.

**Train 1 input**
```text
0000000000
0200000800
0220000800
0000000800
0000000000
0000003300
0000003300
0000000000
```
**Train 1 output**
```text
0000000000
0000020800
0000022800
0000000800
0000000000
0000003300
0000003300
0000000000
```
**Train 2 input**
```text
00000000080
00000000080
00220000080
50022000080
50000000080
50000000080
00000000080
```
**Train 2 output**
```text
00000000080
00000000080
00000022080
50000002280
50000000080
50000000080
00000000080
```
**Test input**
```text
000000000077
000000000077
000000008000
002000008000
022200008000
000000008000
000000000000
000000000000
```
**Test output**
```text
000000000077
000000000077
000000008000
000000208000
000002228000
000000008000
000000000000
000000000000
```
**Written solution**
Identify the only red connected component. Remove it mentally, then move that whole shape rightward as far as it can go without crossing the border or overlapping any other nonzero cell. Put the red shape back in that final resting place; everything else stays fixed.

**Reference program**
```python
def solve(grid):
    out=copyg(grid)
    reds=[comp for comp in components(grid,{2},4)]
    assert len(reds)==1
    comp=reds[0]
    for r,c in comp['cells']:
        out[r][c]=0
    blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and v!=2}
    slid=slide_component(grid, comp['cells'], (0,1), blockers)
    for r,c in slid:
        out[r][c]=2
    return out
```


## S7_E2 — Column Gravity Dots

**Skills:** column counting, gravity, same-size transform

**Scaffold:**
- Work one column at a time.
- Count how many blue(1) cells are in that column.
- Place that many blue cells at the bottom of the same column.

**Train 1 input**
```text
0010010
1001001
0000100
0100000
0000000
0001000
```
**Train 1 output**
```text
0000000
0000000
0000000
0000000
0001000
1111111
```
**Train 2 input**
```text
100010
001000
000001
010100
000000
001010
000000
```
**Train 2 output**
```text
000000
000000
000000
000000
000000
001010
111111
```
**Test input**
```text
01000100
00010000
10000010
00100100
00000000
01000001
```
**Test output**
```text
00000000
00000000
00000000
00000000
01000100
11110111
```
**Written solution**
For each column, count the blue cells. The output keeps the same height and width, but all blue cells in a column have fallen straight down and stacked at the bottom. Only the number of blue cells per column matters; their original row positions do not.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        cnt=sum(grid[r][c]==1 for r in range(h))
        for r in range(h-cnt,h):
            out[r][c]=1
    return out
```


## S7_E3 — Crop the Interior Rectangle

**Skills:** marker detection, cropping, output-size change

**Scaffold:**
- Locate the two yellow(4) corner markers.
- They mark opposite corners of a rectangle.
- Return only the cells strictly inside that rectangle.

**Train 1 input**
```text
000000000
040000000
002300000
002030000
000332000
000000400
000000000
000000000
```
**Train 1 output**
```text
2300
2030
0332
```
**Train 2 input**
```text
0000000000
0000000000
0040000000
0001200000
0001023000
0000023000
0003300100
0000000040
0000000000
```
**Train 2 output**
```text
12000
10230
00230
33001
```
**Test input**
```text
00000000000
00040000000
00000012000
00002210000
00000202000
00000011100
00003000300
00000000040
00000000000
00000000000
```
**Test output**
```text
00120
22100
02020
00111
30003
```
**Written solution**
The two yellow markers define a crop window. Ignore the markers themselves and take the interior subgrid bounded by them. The output is exactly that interior rectangle, with its original colors and zeros preserved.

**Reference program**
```python
def solve(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4]
    assert len(pts)==2
    (r1,c1),(r2,c2)=pts
    ra,rb=sorted([r1,r2]); ca,cb=sorted([c1,c2])
    return [row[ca+1:cb] for row in grid[ra+1:rb]]
```


## S7_E4 — Solid Bounding Box

**Skills:** bounding box, shape abstraction, same-size construction

**Scaffold:**
- Find the magenta(6) shape.
- Compute its smallest enclosing rectangle.
- Fill that whole rectangle with magenta on an otherwise blank grid.

**Train 1 input**
```text
00000000
00000000
00600000
00600000
00660000
00000000
00000000
```
**Train 1 output**
```text
00000000
00000000
00660000
00660000
00660000
00000000
00000000
```
**Train 2 input**
```text
000000000
000066000
000006600
000000000
000000000
000000000
000000000
000000000
```
**Train 2 output**
```text
000000000
000066600
000066600
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
0000000000
0000600000
0006660000
0000600000
0000000000
0000000000
0000000000
```
**Test output**
```text
0000000000
0000000000
0000000000
0006660000
0006660000
0006660000
0000000000
0000000000
0000000000
```
**Written solution**
There is one magenta object. Replace it by its full bounding box: the smallest axis-aligned rectangle that covers all of its cells. The output keeps the original grid size, clears everything else to black, and paints the entire box magenta.

**Reference program**
```python
def solve(grid):
    comps=components(grid,{6},4)
    assert len(comps)==1
    r1,c1,r2,c2=bbox(comps[0]['cells'])
    out=blank(*dims(grid),0)
    for r in range(r1,r2+1):
        for c in range(c1,c2+1):
            out[r][c]=6
    return out
```


## S7_E5 — Normalize Shape to Top-Left

**Skills:** translation, shape preservation, normalization

**Scaffold:**
- Find the single green(3) shape.
- Measure its shape relative to its own top-left corner.
- Redraw the same shape so that its bounding box starts at the output’s top-left corner.

**Train 1 input**
```text
00000000
00000000
00000000
00003300
00000330
00000000
00000000
```
**Train 1 output**
```text
33000000
03300000
00000000
00000000
00000000
00000000
00000000
```
**Train 2 input**
```text
000000000
000000000
000003000
000003000
000003300
000000000
000000000
000000000
```
**Train 2 output**
```text
300000000
300000000
330000000
000000000
000000000
000000000
000000000
000000000
```
**Test input**
```text
000000000
000000000
000000000
000000000
000303000
000333000
000000000
000000000
000000000
```
**Test output**
```text
303000000
333000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
```
**Written solution**
Take the only green component and ignore its absolute position. Normalize it by shifting it upward and leftward until its bounding box touches row 0 and column 0. The output is blank except for that translated green shape.

**Reference program**
```python
def solve(grid):
    comps=[comp for comp in components(grid,{3},4)]
    assert len(comps)==1
    norm=normalize(comps[0]['cells'])
    h,w=dims(grid)
    out=blank(h,w,0)
    for r,c in norm:
        out[r][c]=3
    return out
```


## S7_E6 — Topmost Cell in Each Column

**Skills:** column scan, selection, same-size filtering

**Scaffold:**
- Inspect each column separately.
- If a column has any yellow(4) cells, keep only the highest one.
- Erase all lower yellow cells in that column.

**Train 1 input**
```text
0400404
0000004
4004000
0400000
0040400
4000004
```
**Train 1 output**
```text
0400404
0000000
4004000
0000000
0040000
0000000
```
**Train 2 input**
```text
00040000
04000040
40000000
00004000
40000400
00004040
```
**Train 2 output**
```text
00040000
04000040
40000000
00004000
00000400
00000000
```
**Test input**
```text
000040000
004000400
400000004
040004000
400000004
000400000
```
**Test output**
```text
000040000
004000400
400000004
040004000
000000000
000400000
```
**Written solution**
The rule is columnwise. In every column, preserve the first yellow cell seen from the top and delete any additional yellow cells below it. Columns with no yellow stay empty.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        for r in range(h):
            if grid[r][c]==4:
                out[r][c]=4
                break
    return out
```


## S7_E7 — Component Count Bar

**Skills:** connected components, counting, output-size change

**Scaffold:**
- Count the separate blue(1) connected components.
- Do not count cells; count objects.
- Output a single horizontal bar of that many blue cells.

**Train 1 input**
```text
11000100
11000100
00000100
00000000
00010000
00000000
```
**Train 1 output**
```text
111
```
**Train 2 input**
```text
010000000
000000000
000011000
000011000
000000000
110000000
000000001
```
**Train 2 output**
```text
1111
```
**Test input**
```text
0000000001
0111000000
0000000000
0000001000
0000000000
0011000000
0011000000
0000000100
```
**Test output**
```text
11111
```
**Written solution**
All nonzero cells are blue, but they form several disconnected objects. Count those connected components and output a 1-row grid whose length equals that count, filled with blue.

**Reference program**
```python
def solve(grid):
    cnt=len(components(grid,{1},4))
    return [[1]*cnt]
```


# Medium

## S7_M1 — Dock the Shape to the Frame

**Skills:** relative position, object motion, shape docking

**Primitive note:** Uses slide_component.

**Scaffold:**
- Find the red(2) object and the cyan frame.
- Decide whether the object starts left, right, above, or below the frame.
- Slide the object straight toward the frame until the next step would collide with it.

**Train 1 input**
```text
00000000000
00000000000
00000088880
02000080080
02200080080
00000080080
00000088880
00000000000
00000000000
```
**Train 1 output**
```text
00000000000
00000000000
00000088880
00002080080
00002280080
00000080080
00000088880
00000000000
00000000000
```
**Train 2 input**
```text
0002200000
0000220000
0000000000
0000000000
0000000000
0088888000
0080008000
0080008000
0088888000
0000000000
```
**Train 2 output**
```text
0000000000
0000000000
0000000000
0002200000
0000220000
0088888000
0080008000
0080008000
0088888000
0000000000
```
**Test input**
```text
000000000000
000000000000
008888000000
008008000200
008008002220
008008000000
008888000000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
008888000000
008008020000
008008222000
008008000000
008888000000
000000000000
000000000000
```
**Written solution**
The cyan frame is fixed. The red object moves in the one obvious cardinal direction that brings it toward the frame. Translate the whole red shape until it just touches the frame from outside, without crossing or deforming it.

**Reference program**
```python
def solve(grid):
    out=copyg(grid)
    frames=components(grid,{8},4)
    assert len(frames)==1
    fr=frames[0]
    fr_bbox=bbox(fr['cells'])
    objs=components(grid,{2},4)
    assert len(objs)==1
    comp=objs[0]
    ob=bbox(comp['cells'])
    # infer direction from relative position
    if ob[3] < fr_bbox[1]:
        step=(0,1)
    elif ob[1] > fr_bbox[3]:
        step=(0,-1)
    elif ob[2] < fr_bbox[0]:
        step=(1,0)
    else:
        step=(-1,0)
    for r,c in comp['cells']:
        out[r][c]=0
    blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and v!=2}
    slid=slide_component(grid, comp['cells'], step, blockers)
    for r,c in slid:
        out[r][c]=2
    return out
```


## S7_M2 — Rigid Gravity with Walls

**Skills:** rigid-body motion, gravity, obstacle reasoning

**Primitive note:** Built from slide_component via repeated downward settling.

**Scaffold:**
- Treat each colored component as a rigid piece.
- Walls are gray(8) and do not move.
- Let every colored piece fall downward until all pieces are stable.

**Train 1 input**
```text
0000000000
0020003000
0220003300
0000800000
0000800000
0000800000
0000800000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0000800000
0000800000
0000800000
0000800000
0020003000
0220003300
```
**Train 2 input**
```text
00040000000
00044000000
00000080000
02000080030
22000080033
00000080000
00000080000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00000080000
00000080000
00000080000
00000080000
00000080000
02040000030
22044000033
```
**Test input**
```text
003000000000
033000000000
000000080000
000200080000
000220080400
000000080440
000000080000
000000000000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000000000
000000080000
000000080000
000000080000
000000080000
000000080000
000000000000
003200000400
033220000440
```
**Written solution**
Unlike single-cell gravity, whole connected colored pieces fall as rigid bodies. Gray walls stay fixed and can support them. Keep dropping each movable piece straight down until nothing can descend any farther.

**Reference program**
```python
def solve(grid):
    return gravity_slide_all(grid, (1,0), immobile_colors={8})
```


## S7_M3 — Height-Sorted Palette Row

**Skills:** object measurement, sorting, summary output

**Scaffold:**
- Find the separate colored rectangles.
- Measure each object’s height, not its area.
- Output a single row of their colors sorted from tallest to shortest.

**Train 1 input**
```text
00000000000
02200333000
02200333000
02200000000
00000000440
00000000000
00000000000
```
**Train 1 output**
```text
234
```
**Train 2 input**
```text
000000000700
000022000700
550022000700
550000000000
550000000000
550000000000
000000000000
000000000000
```
**Train 2 output**
```text
572
```
**Test input**
```text
000000009990
066600009990
066600009990
000003000000
000003000000
000003000000
000003000000
000000000000
```
**Test output**
```text
396
```
**Written solution**
Each object contributes one token to the output. Rank the objects by bounding-box height in descending order, then write a 1-row palette whose cells are the corresponding object colors in that order.

**Reference program**
```python
def solve(grid):
    comps=components(grid,None,4)
    ranked=sorted(comps,key=lambda comp:(-comp_height(comp), bbox(comp['cells'])[1], comp['color']))
    return [[comp['color'] for comp in ranked]]
```


## S7_M4 — Translate Template by Anchor Vector

**Skills:** vector translation, anchor reasoning, shape copying

**Scaffold:**
- Locate the source anchor 1 and target anchor 2.
- Compute the vector from 1 to 2.
- Apply that vector to every green(3) template cell and recolor the moved copy with 2.

**Train 1 input**
```text
1000000000
0300000000
0300000000
0330000000
0000002000
0000000000
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
0000000200
0000000200
0000000220
```
**Train 2 input**
```text
00000000000
00000002000
00000000000
01000000000
00330000000
00033000000
00000000000
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
00000000000
00000000220
00000000022
00000000000
00000000000
00000000000
00000000000
00000000000
```
**Test input**
```text
000000000000
000001000000
000030000000
000333000000
000030000000
000000000000
000000000200
000000000000
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
000000002000
000000022200
000000002000
```
**Written solution**
The green template is not kept in place. Instead, use the displacement from the 1-marker to the 2-marker as a translation vector. Copy the entire green shape by that vector onto a blank grid, and recolor the translated copy blue(2).

**Reference program**
```python
def solve(grid):
    src=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1][0]
    tgt=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    comps=components(grid,{3},4)
    assert len(comps)==1
    dr=tgt[0]-src[0]; dc=tgt[1]-src[1]
    out=blank(*dims(grid),0)
    for r,c in comps[0]['cells']:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=2
    return out
```


## S7_M5 — Farthest Right-Slide Selector

**Skills:** counterfactual simulation, object selection, motion

**Primitive note:** Uses slide_component as a what-if simulator.

**Scaffold:**
- For each colored object, imagine sliding it right until blocked.
- Measure how far each object would travel.
- Keep only the one with the greatest travel distance, drawn in its final slid position.

**Train 1 input**
```text
00000000008
02000000408
02200000408
00000330408
00000330008
00000000008
00000000008
```
**Train 1 output**
```text
00000000000
00000020000
00000022000
00000000000
00000000000
00000000000
00000000000
```
**Train 2 input**
```text
000000000808
000000077808
550000000808
055000000808
000022000008
000022000008
000000000008
000000000008
```
**Train 2 output**
```text
000000000000
000000000000
000000550000
000000055000
000000000000
000000000000
000000000000
000000000000
```
**Test input**
```text
0000000080008
0060000080008
0060000080908
0066003380908
0000003380908
0000000080008
0000000000008
0000000000008
```
**Test output**
```text
0000000000000
0000600000000
0000600000000
0000660000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Written solution**
This is a compare-the-possible-motions task. Treat all other nonzero cells as blockers while evaluating each object. Find the object that could slide the farthest to the right, then output only that object after performing its full slide.

**Reference program**
```python
def solve(grid):
    comps=components(grid,None,4)
    # movable are colors not 8
    movable=[comp for comp in comps if comp['color']!=8]
    best=None; best_dist=-1; best_key=None
    for comp in movable:
        blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and (r,c) not in comp['cells']}
        slid=slide_component(grid, comp['cells'], (0,1), blockers)
        dist=bbox(slid)[1]-bbox(comp['cells'])[1]
        key=(-dist, bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color'])
        # want max dist, then topmost, then leftmost, then color
        if dist>best_dist or (dist==best_dist and (bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']) < best_key):
            best_dist=dist
            best=({'color':comp['color'], 'cells':slid})
            best_key=(bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color'])
    out=blank(*dims(grid),0)
    for r,c in best['cells']:
        out[r][c]=best['color']
    return out
```


## S7_M6 — Row Majority Column

**Skills:** per-row counting, tie-breaking, summary output

**Scaffold:**
- Handle each row independently.
- Find the nonzero color that appears most often in that row.
- Write that winning color into a 1-column output at the same row index.

**Train 1 input**
```text
120221
003333
011220
000000
221121
```
**Train 1 output**
```text
2
3
1
0
2
```
**Train 2 input**
```text
1112300
2200222
3301233
0001000
1212121
```
**Train 2 output**
```text
1
2
3
1
1
```
**Test input**
```text
2211100
0033003
1222333
0000000
3332211
1010101
```
**Test output**
```text
1
3
2
0
3
1
```
**Written solution**
Each input row collapses to one output cell. Count the nonzero colors in the row and choose the majority color. If there is a tie, pick the tied color that appears first from the left. Stack those row winners into a single output column.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,1,0)
    for r in range(h):
        counts={}
        firstpos={}
        for c,v in enumerate(grid[r]):
            if v==0:
                continue
            counts[v]=counts.get(v,0)+1
            firstpos.setdefault(v,c)
        if not counts:
            out[r][0]=0
        else:
            best=max(counts, key=lambda v:(counts[v], -firstpos[v]))
            out[r][0]=best
    return out
```


## S7_M7 — One-Step Object Halo

**Skills:** local neighborhood reasoning, morphological growth, conflict-free fill

**Scaffold:**
- Leave the original colored objects in place.
- Look at each black cell and inspect its four orthogonal neighbors.
- If all adjacent nonzero neighbors belong to one color, fill that black cell with that color.

**Train 1 input**
```text
0000000000
0220000000
0220000000
0000000000
0000003330
0000000000
0000000000
```
**Train 1 output**
```text
0220000000
2222000000
2222000000
0220003330
0000033333
0000003330
0000000000
```
**Train 2 input**
```text
00000000000
00000004000
00000004400
00000000000
00500000000
00500000000
00500000000
00000000000
```
**Train 2 output**
```text
00000004000
00000044400
00000044440
00500004400
05550000000
05550000000
05550000000
00500000000
```
**Test input**
```text
000000000000
000000000000
002000000000
022200000000
000000006600
000000006600
000000000000
000000000000
```
**Test output**
```text
000000000000
002000000000
022200000000
222220006600
022200066660
000000066660
000000006600
000000000000
```
**Written solution**
Grow each object outward by one Manhattan step, but only into black cells whose nonzero orthogonal neighbors are unanimously one color. Because the training examples avoid conflicts, each newly filled halo cell has a unique inherited color.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                continue
            neigh={grid[r+dr][c+dc] for dr,dc in dirs4 if inb(grid,r+dr,c+dc) and grid[r+dr][c+dc]!=0}
            if len(neigh)==1:
                out[r][c]=next(iter(neigh))
    return out
```


# Hard

## S7_H1 — Sequential Arrow Slides

**Skills:** instruction decoding, stateful simulation, order sensitivity

**Primitive note:** Extends slide_component into a multi-step stateful simulator.

**Scaffold:**
- Marker colors 1/2/3/4 mean slide left/right/up/down.
- Each marker controls the unique adjacent colored object.
- Process markers in reading order, removing the markers and sliding each object in turn.

**Train 1 input**
```text
000000400080
260000777080
066000000080
000000000080
000000000080
000000000080
000000000080
000000000080
```
**Train 1 output**
```text
000000000080
000000006080
000000006680
000000000080
000000000080
000000000080
000000000080
000000777080
```
**Train 2 input**
```text
800000000000
800000000000
800000000000
800000005510
800000005500
809000000000
809000000000
809900000000
803000000000
```
**Train 2 output**
```text
800000000000
800000000000
800000000000
855000000000
855000000000
809000000000
809000000000
809900000000
800000000000
```
**Test input**
```text
0000008040000
0000008077000
2660008077000
0066008000000
0000008000000
0000008000090
0000008000091
0000008000090
0000008000000
```
**Test output**
```text
0000008000000
0000008000000
0006608000000
0000668000000
0000008000000
0000008000900
0000008000900
0000008077900
0000008077000
```
**Written solution**
This is not a simultaneous-motion task. First decode the arrow colors as directions. Then, in top-to-bottom left-to-right order, take the object touching each marker and slide that entire object in the indicated direction until blocked by the current state of the grid. Earlier moves can block later ones.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    out=copyg(grid)
    markers=sorted([(r,c,out[r][c]) for r in range(h) for c in range(w) if out[r][c] in dir_from_marker], key=lambda t:(t[0],t[1]))
    # remove markers first
    for r,c,v in markers:
        out[r][c]=0
    for mr,mc,mv in markers:
        # find adjacent component in current out
        adjs=[(mr+dr,mc+dc) for dr,dc in dirs4 if inb(out,mr+dr,mc+dc) and out[mr+dr][mc+dc] not in {0,8}]
        if len(adjs)!=1:
            # if multiple, pick deterministic first
            if not adjs:
                continue
            adjs=sorted(adjs)
        comp=extract_component_from_cell(out, adjs[0], ignore_colors={0,8})
        for r,c in comp['cells']:
            out[r][c]=0
        blockers={(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v!=0}
        slid=slide_component(out, comp['cells'], dir_from_marker[mv], blockers)
        for r,c in slid:
            out[r][c]=comp['color']
    return out
```


## S7_H2 — Directional Gravity from Header

**Skills:** code decoding, global simulation, rigid-body gravity

**Primitive note:** Uses slide_component inside a directional gravity loop.

**Scaffold:**
- The cell at the top-left is a direction code: 1/2/3/4 = left/right/up/down.
- Remove that header marker after reading it.
- Let all colored components fall rigidly in that global direction until stable around the walls.

**Train 1 input**
```text
400000000000
005500000000
005500006600
000008800660
000008800000
000008800000
000008800000
000008800000
000000000000
```
**Train 1 output**
```text
000000000000
000000000000
000000000000
000008800000
000008800000
000008800000
000008800000
005508806600
005500000660
```
**Train 2 input**
```text
10000000080
00000007080
00000007780
00005000080
00005000080
00005000080
00000000080
00000000080
```
**Train 2 output**
```text
00000000080
70000000080
77000000080
50000000080
50000000080
50000000080
00000000080
00000000080
```
**Test input**
```text
200000000080
000000000080
060000000080
060000000080
066000080080
000099080080
000099080080
000000080080
000000080080
```
**Test output**
```text
000000000080
000000000080
000006000080
000006000080
000006680080
000009980080
000009980080
000000080080
000000080080
```
**Written solution**
The header cell chooses the gravity direction for the whole scene. After decoding it, erase the header and repeatedly slide every movable colored component in that direction, preserving each shape as a rigid body and stopping at walls, boundaries, or already settled pieces.

**Reference program**
```python
def solve(grid):
    marker=grid[0][0]
    step=dir_from_marker[marker]
    out=gravity_slide_all(grid, step, immobile_colors={8}, remove_marker_pos={(0,0)})
    return out
```


## S7_H3 — Connector Overlay Assembly

**Skills:** component extraction, registration, shape assembly

**Scaffold:**
- There are two nonzero fragments, each containing one red connector cell.
- Use the connector cells as alignment points.
- Translate one fragment so that the two connectors coincide, then take the union and recolor it.

**Train 1 input**
```text
00000000000
00000004400
00000002400
03200000000
03300000000
00000000000
00000000000
```
**Train 1 output**
```text
00000000000
00000006600
00000066600
00000066000
00000000000
00000000000
00000000000
```
**Train 2 input**
```text
00000000000
05500000000
05200000000
00000000000
00000006200
00000006600
00000000000
00000000000
```
**Train 2 output**
```text
00000000000
06600000000
06600000000
06600000000
00000000000
00000000000
00000000000
00000000000
```
**Test input**
```text
000000000000
000000024000
000000044000
000000000000
003200000000
003330000000
000000000000
000000000000
000000000000
```
**Test output**
```text
000000000000
000000666000
000000666000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Written solution**
Each fragment carries a red connector. Treat those connector cells as registration marks: shift one fragment so its connector lands exactly on the other connector. Then overlay the two fragments and output their union in a single common color.

**Reference program**
```python
def solve(grid):
    comps=nonzero_components(grid,4)
    assert len(comps)==2
    # each comp has one connector color 2 and nonzero other cells
    comps2=[]
    for comp in comps:
        cells=comp['cells']
        conn=[(r,c) for r,c in cells if grid[r][c]==2]
        assert len(conn)==1
        conn=conn[0]
        comps2.append({'cells':cells,'conn':conn})
    # choose first by connector reading order
    comps2=sorted(comps2,key=lambda x:x['conn'])
    a,b=comps2
    dr=a['conn'][0]-b['conn'][0]
    dc=a['conn'][1]-b['conn'][1]
    out=blank(*dims(grid),0)
    for r,c in a['cells']:
        out[r][c]=6
    for r,c in b['cells']:
        out[r+dr][c+dc]=6
    return out
```


## S7_H4 — Dual Inward Slide

**Skills:** simultaneous motion, collision stopping, corridor reasoning

**Scaffold:**
- Find the left object and the right object.
- Move the left object rightward and the right object leftward together.
- Stop when the next simultaneous step would cause overlap, contact through one another, or hit a wall.

**Train 1 input**
```text
000000000000
000000000000
030000004400
033000004400
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
000000000000
000000000000
000700770000
000770770000
000000000000
000000000000
000000000000
```
**Train 2 input**
```text
0000008000000
0300008000000
0300008000000
0300008000000
0000008004400
0000008000440
0000008000000
0000008000000
```
**Train 2 output**
```text
0000008000000
0007008000000
0007008000000
0007008000000
0000008770000
0000008077000
0000008000000
0000008000000
```
**Test input**
```text
00000008000000
00000008000000
00000008000000
03300008004000
03300008004000
00000008004400
00000008000000
00000008000000
00000008000000
```
**Test output**
```text
00000008000000
00000008000000
00000008000000
00077008700000
00077008700000
00000008770000
00000008000000
00000008000000
00000008000000
```
**Written solution**
The two objects advance inward at the same time. Preserve each shape, move them horizontally toward each other, and halt at the last non-overlapping state before a collision or wall contact would happen. The output recolors both final objects to a common color.

**Reference program**
```python
def solve(grid):
    comps=components(grid,None,4)
    walls=[comp for comp in comps if comp['color']==8]
    objs=[comp for comp in comps if comp['color']!=8]
    assert len(objs)==2
    objs=sorted(objs,key=lambda comp:bbox(comp['cells'])[1])
    left,right=objs
    h,w=dims(grid)
    wallcells={(r,c) for comp in walls for r,c in comp['cells']}
    # move simultaneously toward center until next step invalid (overlap or wall/out)
    left_cells=set(left['cells']); right_cells=set(right['cells'])
    while True:
        left_n={(r,c+1) for r,c in left_cells}
        right_n={(r,c-1) for r,c in right_cells}
        if any(c<0 or c>=w or r<0 or r>=h for r,c in left_n|right_n):
            break
        if left_n & wallcells or right_n & wallcells:
            break
        if left_n & right_n:
            break
        if left_n & right_cells or right_n & left_cells:
            break
        left_cells, right_cells = left_n, right_n
    out=blank(h,w,0)
    # preserve walls? maybe yes to show corridor; but output only moved shapes? decide maybe preserve walls too
    for r,c in wallcells:
        out[r][c]=8
    for r,c in left_cells|right_cells:
        out[r][c]=7
    return out
```


## S7_H5 — Majority Shape from Shifted Copies

**Skills:** normalization, set voting, shape abstraction

**Scaffold:**
- Extract the three green(3) components.
- Normalize each one to its own top-left corner.
- Keep the normalized cells that appear in at least two of the three shapes.

**Train 1 input**
```text
00000000000000
00300033000000
03330033300000
00000000000330
00000000003330
00000000000000
00000000000000
00000000000000
```
**Train 1 output**
```text
030
333
```
**Train 2 input**
```text
000000000000000
030000000000000
030000000003000
033000330003300
000000300003300
000000330000000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**
```text
30
30
33
```
**Test input**
```text
0000000000000000
0030000030000000
0333000333000000
0030000033000000
0000000000003300
0000000000003330
0000000000000300
0000000000000000
0000000000000000
0000000000000000
```
**Test output**
```text
030
333
030
```
**Written solution**
This is a consensus-shape task. Ignore where each copy sits in the large grid and normalize every component to its local top-left. Count how often each normalized cell appears; the output is the shape made of cells present in a majority of the copies.

**Reference program**
```python
def solve(grid):
    comps=components(grid,{3},4)
    norms=[normalize(comp['cells']) for comp in comps]
    counts={}
    for norm in norms:
        for cell in norm:
            counts[cell]=counts.get(cell,0)+1
    keep=[cell for cell,cnt in counts.items() if cnt>=2]
    if not keep:
        return [[0]]
    r1,c1,r2,c2=bbox(keep)
    h=r2-r1+1; w=c2-c1+1
    out=blank(h,w,0)
    for r,c in keep:
        out[r-r1][c-c1]=3
    return out
```


## S7_H6 — Shelf Pack by Area

**Skills:** object extraction, sorting, constructive composition

**Scaffold:**
- Extract each colored component and normalize it to its own top-left corner.
- Sort the shapes by area from largest to smallest.
- Pack them left-to-right on a common shelf with a one-column gap.

**Train 1 input**
```text
00000000000000
02200000000000
02200030000000
00000030004000
00000030004000
00000000004400
00000000000000
00000000000000
```
**Train 1 output**
```text
2204003
2204003
0004403
```
**Train 2 input**
```text
000000000000000
005000000000000
055500000007700
005000000000770
000000060000000
000000066000000
000000000000000
000000000000000
000000000000000
```
**Train 2 output**
```text
0500770060
5550077066
0500000000
```
**Test input**
```text
0000000000000000
0000000088000000
0002000088000000
0022200080000000
0000000000000000
0000000000000000
0000000000000000
0000000000009990
0000000000000000
0000000000000000
```
**Test output**
```text
8800200999
8802220000
8000000000
```
**Written solution**
The output is a new compact layout, not a filtered version of the input. Take each object’s exact shape, normalize it, order the objects by descending area, and place them side by side with one black column between consecutive shapes.

**Reference program**
```python
def solve(grid):
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda comp:(-area(comp), comp['color']))
    norms=[]
    maxh=0
    totalw=0
    for comp in comps:
        norm=normalize(comp['cells'])
        norms.append((comp['color'], norm))
        ch=max(r for r,c in norm)+1
        cw=max(c for r,c in norm)+1
        maxh=max(maxh,ch)
        totalw += cw
    totalw += max(0, len(norms)-1)
    out=blank(maxh,totalw,0)
    curc=0
    for color,norm in norms:
        ch=max(r for r,c in norm)+1
        cw=max(c for r,c in norm)+1
        for r,c in norm:
            out[r][curc+c]=color
        curc += cw + 1
    return out
```


## S7_H7 — Park Shapes in Matching Bays

**Skills:** color matching, normalization, placement into targets

**Scaffold:**
- Find the colored shapes in the upper part of the grid.
- Find the gray parking frames; each frame has one colored label cell inside.
- For each shape, match it to the bay with the same color and place the normalized shape at that bay’s interior top-left.

**Train 1 input**
```text
000000000000000
020000330000000
022000330004440
000000000000000
000000000000000
000000000000000
888808888088880
830808408082080
800808008080080
888808888088880
```
**Train 1 output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
888808888088880
833808444082080
833808008082280
888808888088880
```
**Train 2 input**
```text
0000000000000000
0055000060000000
0005500060000000
0000000060007700
0000000000007700
0000000000000000
0000000000000000
0888808888088880
0870808508086080
0800808008080080
0888808888088880
```
**Train 2 output**
```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0888808888088880
0877808558086080
0877808055086080
0888808888086880
```
**Test input**
```text
00000000000000000
00200004000000000
02220004000006600
00000004400006600
00000000000000000
00000000000000000
00000000000000000
88888088888088888
86008082008084008
80008080008080008
88888088888088888
```
**Test output**
```text
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
88888088888088888
86608080208084008
86608082228084008
88888088888084488
```
**Written solution**
The bays are gray frames labeled by color. Extract each free-standing colored shape, normalize it to its own top-left, and drop it into the matching bay so it starts at the bay’s interior top-left corner. Keep the gray frames, remove the labels, and preserve the shape colors.

**Reference program**
```python
def solve(grid):
    h,w=dims(grid)
    # detect 8 frames with exactly one colored label inside
    frames=components(grid,{8},4)
    bays=[]
    label_positions=set()
    for fr in frames:
        r1,c1,r2,c2=bbox(fr['cells'])
        # verify hollow rectangle maybe optional
        interior=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,8)]
        if len(interior)==1:
            r,c,color = interior[0]
            bays.append({'color':color,'bbox':(r1,c1,r2,c2),'label':(r,c)})
            label_positions.add((r,c))
    # extract shapes excluding frames and labels
    seen=[[False]*w for _ in range(h)]
    shapes=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==0 or grid[r][c]==8 or (r,c) in label_positions:
                continue
            color=grid[r][c]
            seen[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs4:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and grid[nr][nc]==color and (nr,nc) not in label_positions:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            shapes.append({'color':color,'cells':sorted(cells)})
    out=blank(h,w,0)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=8
    for shape in shapes:
        color=shape['color']
        bay=[b for b in bays if b['color']==color]
        if not bay:
            continue
        bay=bay[0]
        norm=normalize(shape['cells'])
        ir=bay['bbox'][0]+1
        ic=bay['bbox'][1]+1
        for r,c in norm:
            out[ir+r][ic+c]=color
    return out
```
