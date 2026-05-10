# ARC-style Puzzle Bank — 21 more puzzles (set 6)

This sixth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It pushes harder into wire/path logic, enclosure depth, perimeter reasoning, room filling, pathfinding, and normalized-shape comparisons.

This set also introduces a new helper primitive:

```text
follow_wire(grid, start, path_colors={1})
  Starting from a marker cell, follow the unique non-branching 4-connected path attached to it and return the ordered path cells.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set6_reference.py`.

## Index

### Easy

- **S6_E1** — Start-Marked Wire Recolor
- **S6_E2** — Object Outline Only
- **S6_E3** — Swap Two Object Colors
- **S6_E4** — Complete the Rectangle Corner
- **S6_E5** — Odd-Area Object Recolor
- **S6_E6** — Wire Length Strip
- **S6_E7** — Path Endpoints Only

### Medium

- **S6_M1** — Longest Marked Wire
- **S6_M2** — Bounding-Box Intersection Fill
- **S6_M3** — Deepest Enclosing Frame Color
- **S6_M4** — Seeded Checker Fill
- **S6_M5** — Mirror Pair Selector
- **S6_M6** — Perimeter-Sorted Palette Row
- **S6_M7** — Color-Matched Relocation

### Hard

- **S6_H1** — Room Fill by Seeds
- **S6_H2** — Most-Turns Wire
- **S6_H3** — Normalized Shape XOR
- **S6_H4** — Stamp Template at Wire Turns
- **S6_H5** — Two-Seed Voronoi Fill
- **S6_H6** — Consensus Shape from Rotated Copies
- **S6_H7** — Shortest Path Through the Maze

# Easy

## S6_E1 — Start-Marked Wire Recolor

**Skills:** path following, component selection, same-size recolor

**Primitive note:** Uses the new follow_wire primitive.

**Scaffold:**
- Find the unique start marker color 2.
- Follow the attached blue(1) wire from that start only.
- Recolor that wire to green(3) and leave everything else alone.

**Train 1 input**
```text
0000000000
0211000000
0001000000
0001110000
0000000000
0000000110
0000000110
0000000000
```
**Train 1 output**
```text
0000000000
0233000000
0003000000
0003330000
0000000000
0000000110
0000000110
0000000000
```
**Train 2 input**
```text
000000000
021110000
000010000
000011100
000000100
000000000
000001100
000001100
```
**Train 2 output**
```text
000000000
023330000
000030000
000033300
000000300
000000000
000001100
000001100
```
**Test input**
```text
0000000000
0021110000
0000010000
0000011100
0000000100
0000000000
0001100000
0001100000
```
**Test output**
```text
0000000000
0023330000
0000030000
0000033300
0000000300
0000000000
0001100000
0001100000
```
**Written solution:** Locate the red start marker. Only the blue wire attached to that marker matters. Follow that non-branching wire and recolor its wire cells from blue(1) to green(3), leaving stray blue pieces unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    start=starts[0]
    for r,c in follow_wire(grid,start,{1}):
        out[r][c]=3
    return out
```

## S6_E2 — Object Outline Only

**Skills:** boundary extraction, 4-neighbor reasoning, same-size mask

**Scaffold:**
- Identify the single large nonzero object.
- Keep only cells that touch the outside in the 4-neighborhood.
- Remove all strictly interior cells.

**Train 1 input**
```text
000000000
004444000
004444000
004444000
004444000
000000000
```
**Train 1 output**
```text
000000000
004444000
004004000
004004000
004444000
000000000
```
**Train 2 input**
```text
0000000
0444000
0444000
0444400
0004400
0000000
```
**Train 2 output**
```text
0000000
0444000
0404000
0440400
0004400
0000000
```
**Test input**
```text
000000000
000440000
004444400
004444400
000440000
000000000
```
**Test output**
```text
000000000
000440000
004004400
004004400
000440000
000000000
```
**Written solution:** Take the large solid object and erase its interior. A cell stays iff at least one of its four neighbors lies outside the object. The output is the object outline in the original grid size.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid,None,4)
    comp=max(comps,key=lambda c:len(c['cells']))
    s=set(comp['cells']); col=comp['color']
    for r,c in s:
        if any((r+dr,c+dc) not in s for dr,dc in dirs4):
            out[r][c]=col
    return out
```

## S6_E3 — Swap Two Object Colors

**Skills:** component extraction, left-right ordering, color substitution

**Scaffold:**
- There are exactly two objects.
- Order them by horizontal position.
- Swap their colors while keeping the shapes fixed.

**Train 1 input**
```text
0000000000
0330000000
0300000000
0330000000
0000007700
0000007000
0000007700
```
**Train 1 output**
```text
0000000000
0770000000
0700000000
0770000000
0000003300
0000003000
0000003300
```
**Train 2 input**
```text
000000000
044400000
000400000
000000008
000000088
000000008
000000000
```
**Train 2 output**
```text
000000000
088800000
000800000
000000004
000000044
000000004
000000000
```
**Test input**
```text
0000000000
0011000000
0001000000
0000000000
0000000770
0000000070
0000000770
```
**Test output**
```text
0000000000
0077000000
0007000000
0000000000
0000000110
0000000010
0000000110
```
**Written solution:** Find the two connected nonzero objects, determine which one is leftmost and which is rightmost, and exchange their colors. Their shapes and positions do not move.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda c:min(cc for rr,cc in c['cells']))
    a,b=comps[:2]
    out=copyg(grid)
    ca,cb=a['color'],b['color']
    for r,c in a['cells']:
        out[r][c]=cb
    for r,c in b['cells']:
        out[r][c]=ca
    return out
```

## S6_E4 — Complete the Rectangle Corner

**Skills:** axis-aligned geometry, same-size completion

**Scaffold:**
- Treat the three colored cells as three corners of a rectangle.
- Read off the two used rows and two used columns.
- Place the missing fourth corner.

**Train 1 input**
```text
00000000
00200200
00000000
00000000
00200000
00000000
```
**Train 1 output**
```text
00000000
00200200
00000000
00000000
00200200
00000000
```
**Train 2 input**
```text
0000000
0700070
0000000
0000000
0000070
0000000
```
**Train 2 output**
```text
0000000
0700070
0000000
0000000
0700070
0000000
```
**Test input**
```text
000000000
000040040
000000000
000000000
000040000
000000000
```
**Test output**
```text
000000000
000040040
000000000
000000000
000040040
000000000
```
**Written solution:** The three colored cells are three corners of one axis-aligned rectangle. Use the two distinct row indices and the two distinct column indices, then add the missing row-column combination.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    # assume 3 same-color cells
    color=cells[0][2]
    pts=[(r,c) for r,c,v in cells if v==color]
    rs=sorted(set(r for r,c in pts)); cs=sorted(set(c for r,c in pts))
    if len(rs)==2 and len(cs)==2:
        for r in rs:
            for c in cs:
                if out[r][c]==0:
                    out[r][c]=color
    return out
```

## S6_E5 — Odd-Area Object Recolor

**Skills:** component sizing, parity test, object selection

**Scaffold:**
- Split the green objects into connected components.
- Compute each area.
- Recolor only the odd-sized object.

**Train 1 input**
```text
3300000000
3300000000
0003330000
0003000000
0003000000
0000003330
0000003330
0000000000
```
**Train 1 output**
```text
3300000000
3300000000
0001110000
0001000000
0001000000
0000003330
0000003330
0000000000
```
**Train 2 input**
```text
000333000
000000000
033000000
033000000
000000000
000000333
000000333
```
**Train 2 output**
```text
000111000
000000000
033000000
033000000
000000000
000000333
000000333
```
**Test input**
```text
3300000000
3300333000
0000030000
0000030000
0000000000
0000003333
0000003333
```
**Test output**
```text
3300000000
3300111000
0000010000
0000010000
0000000000
0000003333
0000003333
```
**Written solution:** Among the green components, exactly one has odd area. Recolor that component to blue(1) and leave the even-sized green components unchanged.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,{3},4)
    target=[comp for comp in comps if len(comp['cells'])%2==1][0]
    out=copyg(grid)
    for r,c in target['cells']:
        out[r][c]=1
    return out
```

## S6_E6 — Wire Length Strip

**Skills:** path following, counting, output-size change

**Primitive note:** Uses the new follow_wire primitive.

**Scaffold:**
- Start from the marker cell.
- Follow its attached wire and count the wire cells.
- Output a one-row strip of that length in color 6.

**Train 1 input**
```text
0000000000
0211000000
0001000000
0001110000
0000000000
0000000110
0000000110
0000000000
```
**Train 1 output**
```text
666666
```
**Train 2 input**
```text
00000000
02100000
00111000
00001000
00000000
```
**Train 2 output**
```text
66666
```
**Test input**
```text
0000000000
0211110000
0000010000
0000011110
0000000000
```
**Test output**
```text
666666666
```
**Written solution:** Find the unique wire attached to the start marker, count how many blue wire cells it contains, and output a 1×N strip of color 6 where N is that wire length.

**Reference program:**
```python
def solve(grid):
    start=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    n=len(follow_wire(grid,start,{1}))
    return [[6]*n] if n>0 else [[0]]
```

## S6_E7 — Path Endpoints Only

**Skills:** local degree counting, endpoint detection

**Scaffold:**
- Look only at the path cells.
- For each one, count same-color 4-neighbors.
- Keep cells of degree 1 and erase the rest.

**Train 1 input**
```text
00000000
05550000
00050000
00050000
00000000
00550000
00000000
```
**Train 1 output**
```text
00000000
05000000
00000000
00050000
00000000
00550000
00000000
```
**Train 2 input**
```text
000000000
005000000
005000000
005550000
000050000
000050000
000000000
```
**Train 2 output**
```text
000000000
005000000
000000000
000000000
000000000
000050000
000000000
```
**Test input**
```text
0000000000
0550000000
0050000000
0055550000
0000050000
0000050000
0000000000
```
**Test output**
```text
0000000000
0500000000
0000000000
0000000000
0000000000
0000050000
0000000000
```
**Written solution:** A path endpoint is a path cell with exactly one same-color orthogonal neighbor. Output only those endpoints and zero out all internal path cells.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==5:
                deg=sum(inb(grid,r+dr,c+dc) and grid[r+dr][c+dc]==5 for dr,dc in dirs4)
                if deg==1:
                    out[r][c]=5
    return out
```

# Medium

## S6_M1 — Longest Marked Wire

**Skills:** multiple path tracking, comparison by length, same-size recolor

**Primitive note:** Uses the new follow_wire primitive.

**Scaffold:**
- Each start marker has its own attached wire.
- Follow every marked wire separately.
- Recolor only the longest one.

**Train 1 input**
```text
00000000000000
02110000021000
00010000001000
00010000001110
00000000000010
00000000000000
00000000000000
00000000000000
```
**Train 1 output**
```text
00000000000000
02110000023000
00010000003000
00010000003330
00000000000030
00000000000000
00000000000000
00000000000000
```
**Train 2 input**
```text
000000000000000
021000021100000
001000000100000
001110000111000
000000000001000
000000000000000
021100000000000
000110000000000
000000000000000
```
**Train 2 output**
```text
000000000000000
021000023300000
001000000300000
001110000333000
000000000003000
000000000000000
021100000000000
000110000000000
000000000000000
```
**Test input**
```text
000000000000000
021100000000000
000100000000000
000110000000000
000000000021000
000000000001000
000000000111000
000000011100000
000000000000000
```
**Test output**
```text
000000000000000
021100000000000
000100000000000
000110000000000
000000000023000
000000000003000
000000000333000
000000033300000
000000000000000
```
**Written solution:** Trace each blue wire that begins at a red start marker, compare their lengths, and recolor only the longest such wire to green(3). Markers and shorter wires remain unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    best=None; best_path=[]
    for st in starts:
        path=follow_wire(grid,st,{1})
        if len(path)>len(best_path):
            best_path=path; best=st
    for r,c in best_path:
        out[r][c]=3
    return out
```

## S6_M2 — Bounding-Box Intersection Fill

**Skills:** bounding boxes, geometric overlap, same-size construction

**Scaffold:**
- Compute the bbox of each of the two objects.
- Intersect those rectangles.
- Fill the overlap rectangle with color 8 on a blank grid.

**Train 1 input**
```text
0000000000
0300000000
0300000000
0344440000
0333400000
0000400000
0000000000
0000000000
```
**Train 1 output**
```text
0000000000
0000000000
0000000000
0088000000
0088000000
0000000000
0000000000
0000000000
```
**Train 2 input**
```text
000000000000
000044444000
003000400000
003000400000
003000400000
003000400000
003333000000
000000000000
000000000000
```
**Train 2 output**
```text
000000000000
000000000000
000088000000
000088000000
000088000000
000088000000
000000000000
000000000000
000000000000
```
**Test input**
```text
00000000000
03330000000
03444400000
03000400000
03000400000
00000400000
00000400000
00000000000
```
**Test output**
```text
00000000000
00000000000
00880000000
00880000000
00880000000
00000000000
00000000000
00000000000
```
**Written solution:** Ignore the detailed shapes and use only their axis-aligned bounding boxes. Compute the rectangle where those two bboxes overlap, and output that overlap region filled with 8 on an otherwise blank grid.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda c:c['color'])[:2]  # assume two objects
    (a,b)=comps[:2]
    r1a,c1a,r2a,c2a=bbox(a['cells']); r1b,c1b,r2b,c2b=bbox(b['cells'])
    rr1=max(r1a,r1b); cc1=max(c1a,c1b); rr2=min(r2a,r2b); cc2=min(c2a,c2b)
    if rr1<=rr2 and cc1<=cc2:
        for r in range(rr1,rr2+1):
            for c in range(cc1,cc2+1):
                out[r][c]=8
    return out
```

## S6_M3 — Deepest Enclosing Frame Color

**Skills:** frame detection, enclosure depth, dot recolor

**Scaffold:**
- Detect the hollow rectangular frames.
- For each dot, list which frames contain it.
- Use the smallest enclosing frame color.

**Train 1 input**
```text
00000000000
03333333330
03100000030
03066666030
03061006030
03066666030
03000000130
03333333330
00000000000
```
**Train 1 output**
```text
00000000000
03333333330
03300000030
03066666030
03066006030
03066666030
03000000330
03333333330
00000000000
```
**Train 2 input**
```text
0000000000000
0222222222220
0204444444020
0214100004020
0204077704020
0204071704020
0204077704020
0204000004020
0204444444120
0222222222220
0000000000000
```
**Train 2 output**
```text
0000000000000
0222222222220
0204444444020
0224400004020
0204077704020
0204077704020
0204077704020
0204000004020
0204444444220
0222222222220
0000000000000
```
**Test input**
```text
000000000000
055555555550
053333333350
053100000350
053077770350
053071070350
053077770350
053333331350
055555555550
000000000000
```
**Test output**
```text
000000000000
055555555550
053333333350
053500000350
053077770350
053077070350
053077770350
053333335350
055555555550
000000000000
```
**Written solution:** Each black/white dot sits inside one or more nested rectangular frames. Recolor the dot to the color of the smallest frame that still encloses it, leaving the frames unchanged.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    frames=detect_frames(grid)
    dots=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1]
    for r,c in dots:
        enclosing=[]
        for fr in frames:
            r1,c1,r2,c2=fr['bbox']
            if r1<r<r2 and c1<c<c2:
                enclosing.append(fr)
        if enclosing:
            fr=min(enclosing,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
            out[r][c]=fr['color']
    return out
```

## S6_M4 — Seeded Checker Fill

**Skills:** frame interior, parity reasoning, same-size fill

**Scaffold:**
- Find the frame and the single seed inside it.
- Compute the seed’s checkerboard parity.
- Fill interior cells of matching parity with the seed color.

**Train 1 input**
```text
000000000
077777770
070200070
070000070
070000070
077777770
000000000
```
**Train 1 output**
```text
000000000
077777770
070202070
072020270
070202070
077777770
000000000
```
**Train 2 input**
```text
0000000000
0777777770
0700000070
0700000070
0700030070
0700000070
0777777770
0000000000
```
**Train 2 output**
```text
0000000000
0777777770
0703030370
0730303070
0703030370
0730303070
0777777770
0000000000
```
**Test input**
```text
00000000000
07777777770
07000000070
07000000070
07000000070
07002000070
07000000070
07777777770
00000000000
```
**Test output**
```text
00000000000
07777777770
07020202070
07202020270
07020202070
07202020270
07020202070
07777777770
00000000000
```
**Written solution:** Inside the frame, paint every empty cell whose row+column parity matches the seed dot’s parity. Leave the opposite-parity cells black, and keep the frame and seed in place.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    frames=detect_frames(grid)
    fr=max(frames,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    r1,c1,r2,c2=fr['bbox']
    seeds=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,fr['color'])]
    sr,sc,color=seeds[0]
    parity=(sr+sc)%2
    for r in range(r1+1,r2):
        for c in range(c1+1,c2):
            if grid[r][c]==0 and (r+c)%2==parity:
                out[r][c]=color
    return out
```

## S6_M5 — Mirror Pair Selector

**Skills:** shape normalization, reflection matching, pair selection

**Scaffold:**
- Normalize the three objects.
- Check which two become equal after a horizontal reflection.
- Output only that mirrored pair.

**Train 1 input**
```text
00000000000000
06000060006660
06000060000600
06600660000000
00000000000000
00000000000000
00000000000000
```
**Train 1 output**
```text
00000000000000
02000020000000
02000020000000
02200220000000
00000000000000
00000000000000
00000000000000
```
**Train 2 input**
```text
000000000000000
066000006600000
006000006000000
006600066000000
000000000000000
000000000000660
000000000000660
000000000000000
```
**Train 2 output**
```text
000000000000000
022000002200000
002000002000000
002200022000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test input**
```text
0000000000000000
0600000060000000
0666006660000000
0000000000000000
0000000000000000
0000000000006000
0000000000006600
0000000000000000
```
**Test output**
```text
0000000000000000
0200000020000000
0222002220000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Written solution:** Among the three same-colored objects, exactly two are mirror images of each other. Identify that reflected pair by normalized shape and output just those two objects, recolored to 2 on a blank background.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,{6},4)
    norms=[normalize(c['cells']) for c in comps]
    # find pair where one equals reflected other
    pair=[]
    for i in range(len(comps)):
        for j in range(i+1,len(comps)):
            ni=norms[i]; nj=norms[j]
            if sorted(ni)==sorted(reflect_h(nj)) or sorted(nj)==sorted(reflect_h(ni)):
                pair=[i,j]
    h,w=dims(grid); out=blank(h,w,0)
    for idx in pair:
        for r,c in comps[idx]['cells']:
            out[r][c]=2
    return out
```

## S6_M6 — Perimeter-Sorted Palette Row

**Skills:** perimeter computation, ranking, summary output

**Scaffold:**
- Compute each object’s exposed-edge perimeter.
- Sort the objects by perimeter from largest to smallest.
- Output a single row of their colors in that order.

**Train 1 input**
```text
000000000000
020003300000
000003300000
000000000000
000000004000
000000004000
000000004400
000000000000
```
**Train 1 output**
```text
432
```
**Train 2 input**
```text
000000000000
007000110000
000000110000
000000000000
000000000555
000000000050
000000000000
000000000000
```
**Train 2 output**
```text
517
```
**Test input**
```text
0000000000000
0200088800000
0200080000000
0000080000000
0000000000000
0000000000400
0000000000000
0000000000000
0000000000000
```
**Test output**
```text
824
```
**Written solution:** Measure each object by its 4-neighbor perimeter, not its area. Sort the objects from largest perimeter to smallest, then output a one-row color sequence listing their colors in that order.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,None,4)
    ranked=sorted(comps,key=lambda c:(-perimeter(grid,c), c['color']))
    return [[c['color'] for c in ranked]]
```

## S6_M7 — Color-Matched Relocation

**Skills:** color pairing, translation, object stamping

**Scaffold:**
- For each color, distinguish the singleton anchor from the larger object.
- Use the object’s top-left as its local origin.
- Translate the object so that origin lands on the matching anchor.

**Train 1 input**
```text
000000000000
020000003000
000000000000
000000000000
000000000000
020000033000
022000033000
000000000000
```
**Train 1 output**
```text
000000000000
020000003300
022000003300
000000000000
000000000000
000000000000
000000000000
000000000000
```
**Train 2 input**
```text
0000000000000
0040000000000
0000000006000
0000000000000
0000000000000
0000000000000
0444000006000
0040000006600
0000000000000
```
**Train 2 output**
```text
0000000000000
0044400000000
0004000006000
0000000006600
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Test input**
```text
00000000000000
05000000070000
00000000000000
00000000000000
00000000000000
00000000007700
00500000000700
00555000000000
00000000000000
```
**Test output**
```text
00000000000000
05000000077000
05550000007000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Written solution:** Each color appears once as a single-cell anchor and once as a larger object. Move each larger object so that its own top-left cell aligns with its same-colored anchor, and output the relocated objects on a blank grid.

**Reference program:**
```python
def solve(grid):
    h,w=dims(grid)
    # anchors are singleton cells whose color also appears in a larger comp.
    comps=components(grid,None,4)
    by_color={}
    for comp in comps:
        by_color.setdefault(comp['color'],[]).append(comp)
    out=blank(h,w,0)
    for color, lst in by_color.items():
        anchors=[c for c in lst if len(c['cells'])==1]
        objs=[c for c in lst if len(c['cells'])>1]
        if anchors and objs:
            ar,ac=anchors[0]['cells'][0]
            obj=max(objs,key=lambda c:len(c['cells']))
            nr0=min(r for r,c in obj['cells']); nc0=min(c for r,c in obj['cells'])
            for r,c in obj['cells']:
                rr=ar+(r-nr0); cc=ac+(c-nc0)
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=color
    return out
```

# Hard

## S6_H1 — Room Fill by Seeds

**Skills:** region segmentation, flood fill, wall-respecting fill

**Scaffold:**
- Treat color 8 as walls that partition the board into rooms.
- Find the zero-cells belonging to each room.
- Fill each room with the color of its unique seed.

**Train 1 input**
```text
0000000000000
0888888888880
0800080030080
0802080000080
0800088888880
0800080000080
0800080004080
0888888888880
0000000000000
```
**Train 1 output**
```text
0000000000000
0888888888880
0822283333380
0822283333380
0822288888880
0822284444480
0822284444480
0888888888880
0000000000000
```
**Train 2 input**
```text
00000000000000
08888888888880
08008000800080
08208000800080
08008030800080
08008000800080
08008000804080
08008000800080
08888888888880
00000000000000
```
**Train 2 output**
```text
00000000000000
08888888888880
08228333844480
08228333844480
08228333844480
08228333844480
08228333844480
08228333844480
08888888888880
00000000000000
```
**Test input**
```text
00000000000000
08888888888880
08200080000080
08888880030080
08000080000080
08000088888880
08050080000080
08000080004080
08888888888880
00000000000000
```
**Test output**
```text
00000000000000
08888888888880
08222283333380
08888883333380
08555583333380
08555588888880
08555584444480
08555584444480
08888888888880
00000000000000
```
**Written solution:** The 8s are walls. They divide the interior into separate rooms, and each room has exactly one colored seed cell touching it. Flood-fill each room with that seed color while preserving the walls and seed cells.

**Reference program:**
```python
def solve(grid):
    return fill_room_by_seed(grid,8)
```

## S6_H2 — Most-Turns Wire

**Skills:** ordered path following, turn counting, comparative selection

**Primitive note:** Uses the new follow_wire primitive.

**Scaffold:**
- Trace each wire in order from its marker.
- Count direction changes along the path.
- Recolor the wire with the most turns.

**Train 1 input**
```text
000000000000000
021111102100000
000000000110000
000000000011000
000000000001000
000000000000000
000000000000000
000000000000000
```
**Train 1 output**
```text
000000000000000
021111102300000
000000000330000
000000000033000
000000000003000
000000000000000
000000000000000
000000000000000
```
**Train 2 input**
```text
0000000000000000
0211100210000000
0000100011100000
0000100000100000
0000000000100000
0000000000000000
0211110000000000
0000000000000000
0000000000000000
```
**Train 2 output**
```text
0000000000000000
0211100230000000
0000100033300000
0000100000300000
0000000000300000
0000000000000000
0211110000000000
0000000000000000
0000000000000000
```
**Test input**
```text
00000000000000000
02110000000000000
00010000002100000
00011100000110000
00000000000011000
00000000000001100
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Test output**
```text
00000000000000000
02110000000000000
00010000002300000
00011100000330000
00000000000033000
00000000000003300
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```
**Written solution:** For every marked wire, follow the path cell by cell and count how often the direction changes. Recolor the wire with the greatest turn count to green(3); if needed, break ties by the longer wire.

**Reference program:**
```python
def solve(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    best_path=[]; best_turns=-1
    for st in starts:
        path=follow_wire(grid,st,{1})
        turns=turns_in_path(path)
        if turns>best_turns or (turns==best_turns and len(path)>len(best_path)):
            best_turns=turns; best_path=path
    for r,c in best_path:
        out[r][c]=3
    return out
```

## S6_H3 — Normalized Shape XOR

**Skills:** shape alignment, symmetric difference, output crop

**Scaffold:**
- Crop each object to its own bbox and normalize to top-left.
- Compare the normalized cell sets.
- Output the cells that belong to exactly one of the two shapes.

**Train 1 input**
```text
000000000000
020000033300
020000003000
022000000000
000000000000
000000000000
000000000000
```
**Train 1 output**
```text
088
880
880
```
**Train 2 input**
```text
0000000000000
0220000030000
0022000030000
0000000033000
0000000000000
0000000000000
0000000000000
```
**Train 2 output**
```text
080
888
880
```
**Test input**
```text
00000000000000
02200000000000
02200000333000
00000000030000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Test output**
```text
008
800
```
**Written solution:** Ignore colors and positions, normalize both objects to their own top-left corners, and compute the symmetric difference of those two cell sets. Output that XOR shape as a cropped grid in color 8.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,None,4)
    # assume exactly two objects
    comps=sorted(comps,key=lambda c:c['color'])[:2]
    n1=set(normalize(comps[0]['cells']))
    n2=set(normalize(comps[1]['cells']))
    cells=sorted(n1.symmetric_difference(n2))
    if not cells:
        return [[0]]
    maxr=max(r for r,c in cells); maxc=max(c for r,c in cells)
    out=blank(maxr+1,maxc+1,0)
    for r,c in cells: out[r][c]=8
    return out
```

## S6_H4 — Stamp Template at Wire Turns

**Skills:** template extraction, ordered path analysis, event-based stamping

**Primitive note:** Uses the new follow_wire primitive.

**Scaffold:**
- Extract the separate template object.
- Follow the marked wire and identify every turn cell.
- Stamp the template with its top-left aligned to each turn.

**Train 1 input**
```text
00000000000000
04000000710000
04400000010000
00000000011100
00000000000100
00000000000000
00000000000000
```
**Train 1 output**
```text
00000000000000
00000000000000
00000000000000
00000000040400
00000000044440
00000000000000
00000000000000
```
**Train 2 input**
```text
000000000000000
044400000000000
000000007100000
000000000100000
000000000111000
000000000001000
000000000001000
000000000000000
000000000000000
```
**Train 2 output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000444440
000000000000000
000000000000000
000000000000000
000000000000000
```
**Test input**
```text
0000000000000000
0400000000710000
0400000000011100
0000000000000100
0000000000011100
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Test output**
```text
0000000000000000
0000000000000000
0000000000040400
0000000000040400
0000000000000400
0000000000000400
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```
**Written solution:** The color-4 object is a template. Follow the start-marked wire, record every cell where the path changes direction, and stamp a copy of the template at each such turn with top-left alignment. Output only the stamped result.

**Reference program:**
```python
def solve(grid):
    # color 4 template, color 2 marker, color 1 wire, color 7 start marker
    comps=components(grid,{4},4)
    template=max(comps,key=lambda c:len(c['cells']))
    temp_norm=normalize(template['cells'])
    start=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7][0]
    path=follow_wire(grid,start,{1})
    turns=[]
    for idx in range(1,len(path)-1):
        a=path[idx-1]; b=path[idx]; c=path[idx+1]
        if (b[0]-a[0],b[1]-a[1]) != (c[0]-b[0],c[1]-b[1]):
            turns.append(b)
    h,w=dims(grid)
    out=blank(h,w,0)
    # stamp template with template's top-left aligned at each turn
    for tr,tc in turns:
        for dr,dc in temp_norm:
            rr,cc=tr+dr, tc+dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=4
    return out
```

## S6_H5 — Two-Seed Voronoi Fill

**Skills:** distance reasoning, frame interior fill, tie handling

**Scaffold:**
- Work only inside the outer frame.
- For each empty cell, compare Manhattan distances to the two seeds.
- Fill with the nearer seed color; ties stay black.

**Train 1 input**
```text
00000000000
08888888880
08020000080
08000000080
08000003080
08888888880
00000000000
```
**Train 1 output**
```text
00000000000
08888888880
08222203380
08222033380
08220333380
08888888880
00000000000
```
**Train 2 input**
```text
0000000000000
0888888888880
0840000000080
0800000000080
0800000000080
0800000000080
0800000005080
0888888888880
0000000000000
```
**Train 2 output**
```text
0000000000000
0888888888880
0844444455580
0844444555580
0844445555580
0844455555580
0844555555580
0888888888880
0000000000000
```
**Test input**
```text
000000000000
088888888880
080000000080
080200006080
080000000080
080000000080
088888888880
000000000000
```
**Test output**
```text
000000000000
088888888880
082222666680
082222666680
082222666680
082222666680
088888888880
000000000000
```
**Written solution:** Inside the frame, every empty cell chooses the nearer of the two colored seeds by Manhattan distance. Paint that cell with the nearer seed’s color, and leave exact ties black. Keep the frame and seeds visible.

**Reference program:**
```python
def solve(grid):
    # outer frame color 8, two seeds nonzero non-wall. fill interior by nearest seed (Manhattan), no ties in examples.
    out=copyg(grid)
    frames=detect_frames(grid)
    fr=max(frames,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    r1,c1,r2,c2=fr['bbox']
    seeds=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,fr['color'])]
    for r in range(r1+1,r2):
        for c in range(c1+1,c2):
            if grid[r][c]==0:
                dists=sorted(((abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds))
                if dists[0][0] != dists[1][0]:
                    out[r][c]=dists[0][1]
    return out
```

## S6_H6 — Consensus Shape from Rotated Copies

**Skills:** canonical rotation, majority vote over objects, prototype output

**Scaffold:**
- Normalize every object and reduce it to a rotation-canonical form.
- Find the canonical shape that appears most often.
- Output that consensus prototype as a cropped shape.

**Train 1 input**
```text
000000000000000
060000666000000
060000600000000
066000000000000
000000000066000
000660000006000
000660000006000
000000000000000
```
**Train 1 output**
```text
222
200
```
**Train 2 input**
```text
0000000000000000
0660000600000000
0066000660000000
0000000060000000
0000000000000000
0600000000660000
0600000000066000
0660000000000000
0000000000000000
```
**Train 2 output**
```text
220
022
```
**Test input**
```text
0000000000000000
0666000060000000
0060000660000000
0000000060000000
0000000000000000
0066000000060000
0066000000666000
0000000000000000
0000000000000000
```
**Test output**
```text
222
020
```
**Written solution:** Several objects are rotated copies of the same underlying shape, while one is an outlier. Convert every object to a canonical rotation, find the majority prototype, and output that canonical shape alone in color 2.

**Reference program:**
```python
def solve(grid):
    comps=components(grid,{6},4)
    # choose majority canonical shape under rotation
    from collections import Counter
    cans=[]
    for comp in comps:
        n=normalize(comp['cells'])
        rots=[tuple(rotate(n,k)) for k in range(4)]
        cans.append(min(rots))
    ctr=Counter(cans)
    target=ctr.most_common(1)[0][0]
    cells=list(target)
    maxr=max(r for r,c in cells); maxc=max(c for r,c in cells)
    out=blank(maxr+1,maxc+1,0)
    for r,c in cells: out[r][c]=2
    return out
```

## S6_H7 — Shortest Path Through the Maze

**Skills:** grid pathfinding, obstacle avoidance, same-size overlay

**Scaffold:**
- Treat 9 as walls and 0 as open floor.
- Find the shortest 4-connected path between the two markers.
- Overlay that path in color 8 without moving the markers.

**Train 1 input**
```text
000009000000
030009000000
000000009000
000009009000
000009009000
000009000000
000000009030
000000009000
```
**Train 1 output**
```text
000009000000
030009000000
088888809000
000009809000
000009809000
000009888800
000000009830
000000009000
```
**Train 2 input**
```text
0000000009000
0300000000000
0000000009000
0099099999900
0000000009000
0000000000000
0999999099000
0000000000030
0000000000000
```
**Train 2 output**
```text
0000000009000
0300000000000
0800000009000
0899099999900
0800000009000
0888888800000
0999999899000
0000000888830
0000000000000
```
**Test input**
```text
00009000000000
03009000090000
00009000090000
00000000090000
00009000090000
00009000090000
00009990990000
00009000090000
00009000090030
00000000090000
```
**Test output**
```text
00009888888000
03009800098000
08009800098000
08888800098000
00009000098000
00009000098000
00009990998000
00009000098000
00009000098830
00000000090000
```
**Written solution:** Find the shortest orthogonal path through the zero cells from one marker to the other, avoiding the 9-walls. Draw that route in color 8 while leaving the walls and endpoints in place.

**Reference program:**
```python
def solve(grid):
    # walls 9, markers 3, fill shortest path with 8 through zeros, keep markers/walls
    out=copyg(grid)
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    start,goal=pts[0],pts[1]
    path=shortest_path(grid,start,goal,{0})
    for r,c in path[1:-1]:
        if out[r][c]==0:
            out[r][c]=8
    return out
```
