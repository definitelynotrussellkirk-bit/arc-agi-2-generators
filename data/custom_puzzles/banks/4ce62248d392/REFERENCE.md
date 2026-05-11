# ARC Additional Puzzle Bank — 21 Puzzles (Set 12)

This twelfth pack continues the numbering with **`E78–E84`**, **`M78–M84`**, and **`H78–H84`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
pack_components(component_grids, axis="horizontal", gap=1, canvas_size=None, anchor=(0, 0))
```

Intuition: once you have already extracted and normalized a set of objects, `pack_components` handles the repetitive layout work of placing those cropped components into a strip or column with fixed gaps. It is used directly in **E78**, **M78**, and **H78**.

Design goals for this set:

- easy: packing, rectangle inference, reflection, command-based transforms, dynamic-size summaries, ray painting, and frame selection

- medium: legend ordering, ranked object selection, relational matrices, chamber flood fill, template stamping, hole counting, and tiled transform assembly

- hard: zone-to-object association, analogy, nearest-seed partitioning, nesting depth, overlap maps, pairwise comparison matrices, and transform composition

## Easy (7)

### E78 — Pack Components by Area
**Difficulty:** easy
**Train pairs:** 4
**Skills:** component extraction, area ranking, strip packing
**Suggested staged path:** Identify each disconnected object first. Then sort them by size and repack them left to right with a one-cell gap.

**Train 1 — input**
```text
000000000000
000000000400
000000004440
000000000400
000000003000
000000003000
022200003300
022200000000
000000000000
000000000000
```
**Train 1 — output**
```text
222004003000
222044403000
000004003300
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 2 — input**
```text
0000000000000
0000000005500
0000000005500
0000000000000
0000000000000
0000003000000
0000003000000
2020003000000
2220000000000
0000000000000
0000000000000
```
**Train 2 — output**
```text
2020550300000
2220550300000
0000000300000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 3 — input**
```text
000000000000
022000000000
020000000000
000000000000
000000000000
000000006000
044440006600
044440000660
000000000000
000000000000
```
**Train 3 — output**
```text
444406000220
444406600200
000000660000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 4 — input**
```text
00000000000000
03330000000000
03330000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000007000
00005550007000
00000500007770
00000000000000
00000000000000
```
**Train 4 — output**
```text
33307000555000
33307000050000
00007770000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```

**Test — input**
```text
0000000000000
0000000000000
0000000022220
0000000022220
0000000000000
0000444000000
0000000000000
0080000000000
0888000000000
0080000000000
0000000000000
```
**Test — output**
```text
2222008004440
2222088800000
0000008000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Written solution**

Extract all connected nonzero components, crop them tightly, sort them by descending area, and place them left-to-right on a blank canvas of the same size.

**Reference program**

```python
def rule_e78(g):
    h,w=size(g)
    comps=[grid_from_component(g,cells) for col,cells in components_nonzero(g, treat_colors_separately=True)]
    comps=sorted(comps, key=lambda cg:(-count_nonzero(cg), len(cg), len(cg[0]), min(v for row in cg for v in row if v!=0)))
    return pack_components(comps, axis="horizontal", gap=1, canvas_size=(h,w), anchor=(0,0))
```

### E79 — Fill the Rectangle from Two Corners
**Difficulty:** easy
**Train pairs:** 4
**Skills:** bbox inference, solid fill
**Suggested staged path:** There are only two colored cells. Treat them as opposite corners of one rectangle.

**Train 1 — input**
```text
00000000
02000000
00000000
00000000
00000200
00000000
00000000
```
**Train 1 — output**
```text
00000000
02222200
02222200
02222200
02222200
00000000
00000000
```

**Train 2 — input**
```text
000030000
000000000
000000000
000000000
000000000
000000030
```
**Train 2 — output**
```text
000033330
000033330
000033330
000033330
000033330
000033330
```

**Train 3 — input**
```text
00000000
00000000
00400000
00000000
00000000
00000000
00000040
00000000
```
**Train 3 — output**
```text
00000000
00000000
00444440
00444440
00444440
00444440
00444440
00000000
```

**Train 4 — input**
```text
0000000000
0000000500
0000000000
0000000000
0050000000
0000000000
0000000000
```
**Train 4 — output**
```text
0000000000
0055555500
0055555500
0055555500
0055555500
0000000000
0000000000
```

**Test — input**
```text
000000000
000000000
000000000
060000000
000000000
000000000
000000000
000060000
000000000
```
**Test — output**
```text
000000000
000000000
000000000
066660000
066660000
066660000
066660000
066660000
000000000
```

**Written solution**

Take the bounding box of the two colored cells and fill that entire rectangle with their shared color.

**Reference program**

```python
def rule_e79(g):
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return clone(g)
    color=cells[0][2]
    rs=[r for r,c,v in cells]; cs=[c for r,c,v in cells]
    out=blank(len(g), len(g[0]))
    fill_rect(out, min(rs), min(cs), max(rs), max(cs), color)
    return out
```

### E80 — Mirror Across the Guide Column
**Difficulty:** easy
**Train pairs:** 4
**Skills:** symmetry, guide detection
**Suggested staged path:** The full column of 9s is the mirror line. Copy the object to the other side by reflecting each occupied cell across that line.

**Train 1 — input**
```text
00000900000
00000900000
02000900000
02000900000
02200900000
00000900000
00000900000
00000900000
```
**Train 1 — output**
```text
00000900000
00000900000
02000900020
02000900020
02200900220
00000900000
00000900000
00000900000
```

**Train 2 — input**
```text
0000009000000
0000009000000
0000009000000
0000009000000
0040009000000
0044009000000
0004409000000
0000009000000
0000009000000
```
**Train 2 — output**
```text
0000009000000
0000009000000
0000009000000
0000009000000
0040009000400
0044009004400
0004409044000
0000009000000
0000009000000
```

**Train 3 — input**
```text
00000900000
00330900000
00330900000
00000900000
00000900000
00000900000
00000900000
```
**Train 3 — output**
```text
00000900000
00330903300
00330903300
00000900000
00000900000
00000900000
00000900000
```

**Train 4 — input**
```text
0000009000000
0000009000000
0000009000000
0000009000000
0050009000000
0555009000000
0050009000000
0000009000000
0000009000000
0000009000000
```
**Train 4 — output**
```text
0000009000000
0000009000000
0000009000000
0000009000000
0050009000500
0555009005550
0050009000500
0000009000000
0000009000000
0000009000000
```

**Test — input**
```text
0000009000000
0000009000000
0000709000000
0007709000000
0000709000000
0000009000000
0000009000000
0000009000000
0000009000000
```
**Test — output**
```text
0000009000000
0000009000000
0000709070000
0007709077000
0000709070000
0000009000000
0000009000000
0000009000000
0000009000000
```

**Written solution**

Find the all-9 guide column and reflect every nonzero, non-guide cell across it, keeping the original object and the guide unchanged.

**Reference program**

```python
def rule_e80(g):
    h,w=size(g)
    guide_cols=[c for c in range(w) if all(g[r][c]==9 for r in range(h))]
    assert len(guide_cols)==1
    gc=guide_cols[0]
    out=clone(g)
    for r in range(h):
        for c in range(gc):
            v=g[r][c]
            if v not in (0,9):
                mc=2*gc-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out
```

### E81 — Commanded Crop Transform
**Difficulty:** easy
**Train pairs:** 4
**Skills:** crop bbox, rotation / reflection by code
**Suggested staged path:** Ignore the marker cell when you locate the object. Crop the object tightly, then apply the transform named by the top-left code.

**Train 1 — input**
```text
1000000000
0000000000
0000000000
0000400000
0000440000
0000044000
0000000000
0000000000
0000000000
```
**Train 1 — output**
```text
044
440
400
```

**Train 2 — input**
```text
200000000
000000000
000000000
000000000
000002000
000002000
000002200
000000000
```
**Train 2 — output**
```text
22
02
02
```

**Train 3 — input**
```text
30000000000
00000000000
00000000000
00000000000
00000000000
00600000000
00600000000
00666000000
00000000000
00000000000
```
**Train 3 — output**
```text
006
006
666
```

**Train 4 — input**
```text
4000000000
0000000000
0000003330
0000000300
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Train 4 — output**
```text
030
333
```

**Test — input**
```text
1000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000500000
0000550000
0000000000
0000000000
```
**Test — output**
```text
55
50
```

**Written solution**

Read the top-left command, crop the only real object to its tight bounding box, and apply the commanded transform: clockwise rotation, 180-degree rotation, horizontal flip, or vertical flip.

**Reference program**

```python
def rule_e81(g):
    t=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)]
    sub=crop_bbox(g,cells)
    sub[0][0] = sub[0][0]  # no-op
    # Need remove marker if within bbox? marker excluded from cells, crop_bbox uses cells to select region, so fine.
    return transform(sub,t)
```

### E82 — Three-Color Count Bars
**Difficulty:** easy
**Train pairs:** 4
**Skills:** counting, dynamic output size
**Suggested staged path:** Count colors 1, 2, and 3 separately. The output is just three bar rows.

**Train 1 — input**
```text
1000003
0200000
0030010
0000200
0300000
0000030
0000002
```
**Train 1 — output**
```text
1100
2220
3333
```

**Train 2 — input**
```text
01000000
00000030
00200000
00030000
00000001
00100000
```
**Train 2 — output**
```text
111
200
330
```

**Train 3 — input**
```text
00000002
01000000
00003000
00200000
00003000
03000000
00000200
20000000
```
**Train 3 — output**
```text
1000
2222
3330
```

**Train 4 — input**
```text
100000001
000000000
002000200
000010000
000000000
000003000
001000000
```
**Train 4 — output**
```text
1111
2200
3000
```

**Test — input**
```text
000000003
010000010
000000300
000200000
030002000
002000000
000010003
300000000
```
**Test — output**
```text
11100
22200
33333
```

**Written solution**

Count how many cells of colors 1, 2, and 3 appear. Create a 3-row output whose width is the maximum of those counts, and fill each row from the left with its color repeated that many times.

**Reference program**

```python
def rule_e82(g):
    counts=[sum(v==color for row in g for v in row) for color in (1,2,3)]
    w=max(counts) if counts else 1
    out=blank(3,w)
    for i,color in enumerate((1,2,3)):
        for c in range(counts[i]):
            out[i][c]=color
    return out
```

### E83 — Cardinal Ray Paint
**Difficulty:** easy
**Train pairs:** 4
**Skills:** ray casting, wall stopping
**Suggested staged path:** Each seed paints outward in the four cardinal directions until it hits a wall.

**Train 1 — input**
```text
99999999999
90000900009
90200900009
90000900009
90000900309
90000900009
90000900009
90000900009
99999999999
```
**Train 1 — output**
```text
99999999999
90200900309
92222900309
90200900309
90200933339
90200900309
90200900309
90200900309
99999999999
```

**Train 2 — input**
```text
9999999999
9000000009
9040000009
9000000009
9999999999
9000000209
9000000009
9999999999
```
**Train 2 — output**
```text
9999999999
9040000009
9444444449
9040000009
9999999999
9222222229
9000000209
9999999999
```

**Train 3 — input**
```text
999999999999
900000090009
900500090009
900000090009
900000090009
999999990009
900000093009
900000090009
999999999999
```
**Train 3 — output**
```text
999999999999
900500093009
955555593009
900500093009
900500093009
999999993009
900000093339
900000093009
999999999999
```

**Train 4 — input**
```text
9999999999
9000900009
9000900009
9060900009
9000900009
9999999999
9000004009
9000000009
9000000009
9999999999
```
**Train 4 — output**
```text
9999999999
9060900009
9060900009
9666900009
9060900009
9999999999
9444444449
9000004009
9000004009
9999999999
```

**Test — input**
```text
99999999999
90000090009
90700090009
99999990009
90000090009
90000090009
90000090509
90000090009
99999999999
```
**Test — output**
```text
99999999999
90700090509
97777790509
99999990509
90000090509
90000090509
90000095559
90000090509
99999999999
```

**Written solution**

From every nonzero seed cell, paint along the four cardinal directions through zero cells until a 9 wall or the grid edge stops the ray. Keep the walls in place.

**Reference program**

```python
def rule_e83(g):
    return project_rays_four(g, stop_color=9)
```

### E84 — Fill the Largest Frame
**Difficulty:** easy
**Train pairs:** 4
**Skills:** rectangular frame detection, area comparison
**Suggested staged path:** All the nonzero components are hollow frames. Choose the one with the largest interior.

**Train 1 — input**
```text
000000000000
022222000000
020002033330
020002030030
022222030030
000000030030
000000030030
000000030030
000000033330
000000000000
```
**Train 1 — output**
```text
000000000000
022222000000
020002033330
020002033330
022222033330
000000033330
000000033330
000000033330
000000033330
000000000000
```

**Train 2 — input**
```text
0000000000000
0444444000000
0400004000000
0400004066660
0400004060060
0400004060060
0400004060060
0444444060060
0000000066660
0000000000000
0000000000000
```
**Train 2 — output**
```text
0000000000000
0444444000000
0444444000000
0444444066660
0444444060060
0444444060060
0444444060060
0444444060060
0000000066660
0000000000000
0000000000000
```

**Train 3 — input**
```text
00000000000
00000055550
02222050050
02002050050
02002050050
02222050050
00000050050
00000055550
00000000000
```
**Train 3 — output**
```text
00000000000
00000055550
02222055550
02002055550
02002055550
02222055550
00000055550
00000055550
00000000000
```

**Train 4 — input**
```text
00000000000000
00000000007770
00333333307070
00300000307070
00300000307070
00300000307770
00300000300000
00300000300000
00300000300000
00333333300000
00000000000000
00000000000000
```
**Train 4 — output**
```text
00000000000000
00000000007770
00333333307070
00333333307070
00333333307070
00333333307770
00333333300000
00333333300000
00333333300000
00333333300000
00000000000000
00000000000000
```

**Test — input**
```text
0000000000000
0888888000000
0800008000000
0800008044440
0800008040040
0800008040040
0800008044440
0800008000000
0888888000000
0000000000000
```
**Test — output**
```text
0000000000000
0888888000000
0888888000000
0888888044440
0888888040040
0888888040040
0888888044440
0888888000000
0888888000000
0000000000000
```

**Written solution**

Detect every perfect rectangular frame, compare their interior areas, and fill only the interior of the largest frame with its own color.

**Reference program**

```python
def rule_e84(g):
    out=clone(g)
    frames=find_rect_frames(g)
    if not frames:
        return out
    col,cells,(r0,c0,r1,c1)=max(frames, key=lambda item: ((item[2][2]-item[2][0]-1)*(item[2][3]-item[2][1]-1), item[0]))
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c]==0:
                out[r][c]=col
    return out
```

## Medium (7)

### M78 — Legend-Ordered Pack
**Difficulty:** medium
**Train pairs:** 4
**Skills:** legend decoding, component packing
**Suggested staged path:** The top row does not describe a transform; it gives the output order. Pack the matching objects in that order.

**Train 1 — input**
```text
4020300000000
0000000000000
0000000000000
0040000000000
0444000000000
0040000000000
0003300000000
0003300002000
0000000002000
0000000002000
```
**Train 1 — output**
```text
0000000000000
0400203300000
4440203300000
0400200000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 2 — input**
```text
50702000000000
00000000000000
00000000000000
05550000000000
05550000000000
00000000000000
00000000002000
00000000002000
00000770002200
00000700000000
00000000000000
```
**Train 2 — output**
```text
00000000000000
55507702000000
55507002000000
00000002200000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```

**Train 3 — input**
```text
306040000000
000000000000
033300000000
003000000000
000000000000
004000060000
004000060000
004000066600
004000000000
000000000000
```
**Train 3 — output**
```text
000000000000
333060004000
030060004000
000066604000
000000004000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 4 — input**
```text
80205000000000
00000000000000
00000000000000
00000000000200
00000000000200
00000000000200
08000000000000
08800000000000
00880000005500
00000000005500
00000000000000
00000000000000
```
**Train 4 — output**
```text
00000000000000
80002055000000
88002055000000
08802000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
```

**Test — input**
```text
7030400000000
0000000000000
0000000003300
0000000003000
0000000000000
0000007777000
0000007777000
0000000000000
0400000000000
0400000000000
0440000000000
```
**Test — output**
```text
0000000000000
7777033040000
7777030040000
0000000044000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Written solution**

Read the distinct nonzero colors in the top row from left to right, extract the component of each color from the body of the grid, crop those components tightly, and pack them left-to-right in legend order.

**Reference program**

```python
def rule_m78(g):
    h,w=size(g)
    legend=[]
    seen=set()
    for c,v in enumerate(g[0]):
        if v!=0 and v not in seen:
            legend.append(v); seen.add(v)
    comps=[]
    comps_by_color={}
    for col,cells in components_nonzero(g, treat_colors_separately=True, ignore_positions={(0,c) for c in range(w)}):
        comps_by_color[col]=grid_from_component(g,cells)
    ordered=[comps_by_color[col] for col in legend if col in comps_by_color]
    return pack_components(ordered, axis="horizontal", gap=1, canvas_size=(h,w), anchor=(1,0))
```

### M79 — Select by Rank, Then Transform
**Difficulty:** medium
**Train pairs:** 4
**Skills:** ranking, cropping, command composition
**Suggested staged path:** One marker chooses which component to keep; the other chooses how to transform it.

**Train 1 — input**
```text
1000000000002
0000000000000
0000000000000
0000000000400
0000000004440
0222000000400
0222000000000
0000000000000
0000003000000
0000003000000
0000003000000
```
**Train 1 — output**
```text
222
222
```

**Train 2 — input**
```text
200000000003
000000002200
000000002200
000000000000
000000000000
505000000000
555000000000
000004400000
000004000000
000000000000
```
**Train 2 — output**
```text
22
22
```

**Train 3 — input**
```text
30000000000001
00000000000000
06666000000000
06666000000000
00000000000000
00000000003000
00000000003000
00000200003330
00000200000000
00000220000000
00000000000000
```
**Train 3 — output**
```text
222
200
```

**Train 4 — input**
```text
2000000000004
0000000000000
0000000000000
0070000000000
0777000000000
0070000000000
0000222000400
0000222000400
0000000000400
0000000000000
```
**Train 4 — output**
```text
070
777
070
```

**Test — input**
```text
10000000000001
00000000000000
00000000003300
00000000003300
00000000000000
00000000000000
00000000000000
08000000000000
08800000000000
00880005550000
00000000000000
00000000000000
```
**Test — output**
```text
088
880
800
```

**Written solution**

Ignore the two command cells, rank the remaining components by descending area, select the k-th largest one, crop it tightly, and apply the transform given by the second command.

**Reference program**

```python
def rule_m79(g):
    h,w=size(g)
    k=g[0][0]
    t=g[0][w-1]
    ignore={(0,0),(0,w-1)}
    comps=[grid_from_component(g,cells) for col,cells in components_nonzero(g, treat_colors_separately=True, ignore_positions=ignore)]
    comps=sorted(comps, key=lambda cg:(-count_nonzero(cg), min(v for row in cg for v in row if v!=0)))
    target=comps[k-1]
    return transform(target,t)
```

### M80 — Rotation-Equivalence Matrix
**Difficulty:** medium
**Train pairs:** 4
**Skills:** shape normalization, pairwise relation matrix
**Suggested staged path:** Forget the colors and compare shapes only. The output tells which pairs match up to rotation.

**Train 1 — input**
```text
0000000000000
0200000000000
0200000000660
0220000000660
0000000000000
0000004440000
0000004000000
0000000000000
0000000000000
0000000000000
```
**Train 1 — output**
```text
880
880
008
```

**Train 2 — input**
```text
00000000000000
00000000000000
02220000000000
00200000000000
00000000000000
00000000000000
00000005000000
00000055500700
00000005007770
00000000000000
00000000000000
```
**Train 2 — output**
```text
808
080
808
```

**Train 3 — input**
```text
000000000000
030000000000
033000000000
003300000000
000000000000
000000000440
000066004400
000060004000
000000000000
000000000000
```
**Train 3 — output**
```text
880
880
008
```

**Train 4 — input**
```text
0000000000000
0000000000000
0000000003000
0000000003000
0000000003300
0200000000000
0200000004000
0222000004000
0000000444000
0000000000000
0000000000000
```
**Train 4 — output**
```text
808
080
808
```

**Test — input**
```text
00000000000000
02200000000000
02200000000000
00000000000000
00000000000000
00000000000000
00000770005500
00000700000500
00000000000000
00000000000000
```
**Test — output**
```text
800
088
088
```

**Written solution**

Order the components by color, normalize their shapes, and build a square matrix where entry (i,j) is 8 exactly when components i and j have the same shape up to rotation; otherwise it is 0.

**Reference program**

```python
def rule_m80(g):
    comps=sorted(components_nonzero(g, treat_colors_separately=True), key=lambda item:item[0])
    n=len(comps)
    out=blank(n,n)
    for i,(_,cells_i) in enumerate(comps):
        for j,(_,cells_j) in enumerate(comps):
            out[i][j]=8 if shape_eq_upto_rotation(cells_i,cells_j) else 0
    return out
```

### M81 — Seeded Chamber Fill
**Difficulty:** medium
**Train pairs:** 4
**Skills:** flood fill, wall-bounded regions
**Suggested staged path:** The 9s partition the board into chambers. Expand each seed only inside its own chamber.

**Train 1 — input**
```text
99999999999
90000900009
90200903009
90000900009
99999999999
90000900009
90400900509
90000900009
99999999999
```
**Train 1 — output**
```text
99999999999
92222933339
92222933339
92222933339
99999999999
94444955559
94444955559
94444955559
99999999999
```

**Train 2 — input**
```text
999999999999
900090009009
902090009009
900090009009
900090009009
900090309009
900090009009
900090009049
900090009009
999999999999
```
**Train 2 — output**
```text
999999999999
922293339449
922293339449
922293339449
922293339449
922293339449
922293339449
922293339449
922293339449
999999999999
```

**Train 3 — input**
```text
9999999999999
9000009000009
9060009007009
9000009000009
9000009000009
9999999999999
9080009005009
9000009000009
9999999999999
```
**Train 3 — output**
```text
9999999999999
9666669777779
9666669777779
9666669777779
9666669777779
9999999999999
9888889555559
9888889555559
9999999999999
```

**Train 4 — input**
```text
99999999999
90000900009
90200903009
90000900009
90000900009
99999999999
90000900009
90400905009
90000900009
90000900009
99999999999
```
**Train 4 — output**
```text
99999999999
92222933339
92222933339
92222933339
92222933339
99999999999
94444955559
94444955559
94444955559
94444955559
99999999999
```

**Test — input**
```text
9999999999999
9000900009009
9020903009409
9000900009009
9999999999999
9000900009009
9050906009709
9000900009009
9000900009009
9999999999999
```
**Test — output**
```text
9999999999999
9222933339449
9222933339449
9222933339449
9999999999999
9555966669779
9555966669779
9555966669779
9555966669779
9999999999999
```

**Written solution**

Treat 9s as hard walls. For each colored seed, flood-fill through zeros inside its reachable chamber and recolor that chamber with the seed color, leaving unseeded chambers unchanged.

**Reference program**

```python
def rule_m81(g):
    out=clone(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,9)]
    for r,c,v in seeds:
        # BFS on original grid so other chambers don't matter
        q=[(r,c)]
        seen={(r,c)}
        while q:
            rr,cc=q.pop()
            if out[rr][cc]==0 or (rr,cc)==(r,c):
                out[rr][cc]=v
            for dr,dc in DIR4:
                nr,nc=rr+dr,cc+dc
                if 0<=nr<len(g) and 0<=nc<len(g[0]) and (nr,nc) not in seen and g[nr][nc]!=9 and g[nr][nc] in (0,v):
                    seen.add((nr,nc)); q.append((nr,nc))
    return out
```

### M82 — Stamp the Extracted Template
**Difficulty:** medium
**Train pairs:** 4
**Skills:** template extraction, anchored stamping
**Suggested staged path:** The template lives in the top-left corner. Every 8 marks a place where that template should be copied.

**Train 1 — input**
```text
230000000000
022000000000
000000000000
000000000000
000008000000
000000000000
000000000000
080000000000
000000000000
000000000000
```
**Train 1 — output**
```text
000000000000
000000000000
000000000000
000000000000
000002300000
000000220000
000000000000
023000000000
002200000000
000000000000
```

**Train 2 — input**
```text
4200000000000
4440000000000
0400000000000
0000000080000
0000000000000
0000000000000
0000000000000
0000008000000
0000000000000
0000000000000
0000000000000
```
**Train 2 — output**
```text
0000000000000
0000000000000
0000000000000
0000000042000
0000000044400
0000000004000
0000000000000
0000004200000
0000004440000
0000000400000
0000000000000
```

**Train 3 — input**
```text
56000000000000
05600000000000
00000000000000
00000000000000
00800000000000
00000000000000
00000000080000
00000000000000
00000000000000
00000000000000
```
**Train 3 — output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
00560000000000
00056000000000
00000000056000
00000000005600
00000000000000
00000000000000
```

**Train 4 — input**
```text
720000000000
770000000000
000000000000
000000000000
000000000000
000008000000
000000000000
000000000000
008000000000
000000000000
000000000000
000000000000
```
**Train 4 — output**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000007200000
000007700000
000000000000
007200000000
007700000000
000000000000
000000000000
```

**Test — input**
```text
3400000000000
0330000000000
0030000000000
0000000000000
0000000800000
0000000000000
0000000000000
0000800000000
0000000000000
0000000000000
0000000000000
```
**Test — output**
```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000340000
0000000033000
0000000003000
0000340000000
0000033000000
0000003000000
0000000000000
```

**Written solution**

Extract the connected non-8 template anchored at the top-left corner, then stamp that template onto a blank canvas with its top-left aligned to each anchor cell of color 8.

**Reference program**

```python
def rule_m82(g):
    h,w=size(g)
    template_cells=component_containing(g,(0,0),ignore_colors={8})
    template=grid_from_component(g,template_cells)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    out=blank(h,w)
    for r,c in anchors:
        place_grid(out, template, r, c)
    return out
```

### M83 — Pack by Hole Count
**Difficulty:** medium
**Train pairs:** 4
**Skills:** hole counting, component sorting, vertical packing
**Suggested staged path:** These objects are best distinguished by the number of enclosed holes they contain.

**Train 1 — input**
```text
00000000000000
00000022222220
00000020020020
00000020020020
00000022222220
00000000000000
00000000044400
00000000040400
00000000044400
03000000000000
03000000000000
03300000000000
00000000000000
00000000000000
```
**Train 1 — output**
```text
30000000000000
30000000000000
33000000000000
00000000000000
44400000000000
40400000000000
44400000000000
00000000000000
22222220000000
20020020000000
20020020000000
22222220000000
00000000000000
00000000000000
```

**Train 2 — input**
```text
000000000000000
055500000000000
050500000000000
055500000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000077777770
000000070070070
002200070070070
002000077777770
000000000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
220000000000000
200000000000000
000000000000000
555000000000000
505000000000000
555000000000000
000000000000000
777777700000000
700700700000000
700700700000000
777777700000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 3 — input**
```text
0000000000000000
0000000000000000
0000000000004000
0000000000004000
0000000000004400
0000000000000000
0000000000000000
0666000000000000
0606000000000000
0666000088888880
0000000080080080
0000000080080080
0000000088888880
0000000000000000
```
**Train 3 — output**
```text
4000000000000000
4000000000000000
4400000000000000
0000000000000000
6660000000000000
6060000000000000
6660000000000000
0000000000000000
8888888000000000
8008008000000000
8008008000000000
8888888000000000
0000000000000000
0000000000000000
```

**Train 4 — input**
```text
000000000000000
000000033333330
000000030030030
000000030030030
000000033333330
000000000000000
000000000077700
000000000070700
000000000077700
000000000000000
055000000000000
050000000000000
000000000000000
000000000000000
000000000000000
```
**Train 4 — output**
```text
550000000000000
500000000000000
000000000000000
777000000000000
707000000000000
777000000000000
000000000000000
333333300000000
300300300000000
300300300000000
333333300000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Test — input**
```text
000000000000000
000000000000000
000000000000000
000000000022200
000000000020200
000000000022200
000000000000000
000000000000000
044444440000000
040040040000000
040040040006000
044444440006000
000000000006600
000000000000000
```
**Test — output**
```text
600000000000000
600000000000000
660000000000000
000000000000000
222000000000000
202000000000000
222000000000000
000000000000000
444444400000000
400400400000000
400400400000000
444444400000000
000000000000000
000000000000000
```

**Written solution**

Extract and crop each component, count its enclosed zero regions, sort the components from fewest holes to most, and pack them vertically with one blank row between successive crops.

**Reference program**

```python
def rule_m83(g):
    h,w=size(g)
    comps=[]
    for col,cells in components_nonzero(g, treat_colors_separately=True):
        cg=grid_from_component(g,cells)
        comps.append((enclosed_zero_components_count(cg), cg))
    comps=sorted(comps, key=lambda t:(t[0], count_nonzero(t[1]), min(v for row in t[1] for v in row if v!=0)))
    ordered=[cg for holes,cg in comps]
    return pack_components(ordered, axis="vertical", gap=1, canvas_size=(h,w), anchor=(0,0))
```

### M84 — Corner-Command Tiling
**Difficulty:** medium
**Train pairs:** 4
**Skills:** multi-command transforms, tiling assembly
**Suggested staged path:** The same motif is reused four times. Each corner code tells you how to transform it for one quadrant of the output.

**Train 1 — input**
```text
100000002
000000000
000000000
000200000
000200000
000220000
000000000
000000000
300000004
```
**Train 1 — output**
```text
222220
200020
000020
020220
020200
220200
```

**Train 2 — input**
```text
4000000001
0000000000
0000000000
0000000000
0000500000
0000550000
0000055000
0000000000
0000000000
2000000003
```
**Train 2 — output**
```text
055055
550550
500500
550005
055055
005550
```

**Train 3 — input**
```text
200000002
000000000
000000000
000044000
000040000
000000000
000000000
000000000
300000001
```
**Train 3 — output**
```text
0404
4444
4444
0404
```

**Train 4 — input**
```text
3000000004
0000000000
0000000000
0000000000
0006660000
0000600000
0000000000
0000000000
0000000000
1000000002
```
**Train 4 — output**
```text
666060
060666
000000
060060
660666
060000
```

**Test — input**
```text
100000003
000000000
000000000
000700000
000700000
000777000
000000000
000000000
400000002
```
**Test — output**
```text
777007
700007
700777
777777
700007
700007
```

**Written solution**

Ignore the four command cells, crop the central motif, transform it according to the top-left, top-right, bottom-left, and bottom-right commands, and place those four variants into a 2×2 tiled output.

**Reference program**

```python
def rule_m84(g):
    h,w=size(g)
    codes=[g[0][0], g[0][w-1], g[h-1][0], g[h-1][w-1]]
    ignore={(0,0),(0,w-1),(h-1,0),(h-1,w-1)}
    motif_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and (r,c) not in ignore]
    motif=crop_bbox(g,motif_cells)
    variants=[transform(motif,c) for c in codes]
    mh=max(len(v) for v in variants); mw=max(len(v[0]) for v in variants)
    # Use original motif size? To tile consistently, pad each transformed to bounding of max dims by top-left placement.
    out=blank(2*mh,2*mw)
    for idx,var in enumerate(variants):
        r0=(idx//2)*mh; c0=(idx%2)*mw
        place_grid(out,var,r0,c0)
    return out
```

## Hard (7)

### H78 — Zone Commands: Transform and Pack
**Difficulty:** hard
**Train pairs:** 4
**Skills:** zone association, per-object transform, packing
**Suggested staged path:** Each top-row command controls the object beneath its zone. Transform the objects first, then repack them.

**Train 1 — input**
```text
0100000300000400
0000000000000000
0000000000000000
0000000000000000
2000000000000000
2000000300000000
2200003330000000
0000000300000000
0000000000004440
0000000000000000
0000000000000000
0000000000000000
```
**Train 1 — output**
```text
0000000000000000
0300222044400000
3330200000000000
0300000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```

**Train 2 — input**
```text
00200000100000300
00000000000000000
00000000000000000
00000000000000000
05550000000000000
05550000000000000
00000000000000000
00000006660000000
00000000600000000
00000000000007700
00000000000007000
00000000000000000
00000000000000000
```
**Train 2 — output**
```text
00000000000000000
55500607700000000
55506600700000000
00000600000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```

**Train 3 — input**
```text
040000000300000100
000000000000000000
000000000000000000
000000000000000000
000000000000000000
200000000000000000
220000000000006000
022000000440006000
000000000440006660
000000000000000000
000000000000000000
000000000000000000
```
**Train 3 — output**
```text
000000000000000000
022066604400000000
220060004400000000
200060000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
000000000000000000
```

**Train 4 — input**
```text
00300000400000200
00000000000000000
00000000000000000
03030000000000000
03330000000000000
00000000000000000
00000000000000000
00000000000000000
00000000500007777
00000000500007777
00000000550000000
00000000000000000
00000000000000000
```
**Train 4 — output**
```text
00000000000000000
77770303055000000
77770333050000000
00000000050000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
00000000000000000
```

**Test — input**
```text
0100000200000300
0000000000000000
0000000000000000
0000000000000000
0040000000000000
0444000000000000
0040000000008880
0000000000008880
0000000660000000
0000000600000000
0000000000000000
0000000000000000
```
**Test — output**
```text
0000000000000000
8880040006000000
8880444066000000
0000040000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
```

**Written solution**

Associate each component with the nearest top-row command by horizontal zone, transform each component according to its assigned code, then sort the transformed components by area and pack them left-to-right on a blank canvas.

**Reference program**

```python
def rule_h78(g):
    h,w=size(g)
    commands=[(c,v) for c,v in enumerate(g[0]) if v!=0]
    ignore={(0,c) for c in range(w)}
    transformed=[]
    for col,cells in components_nonzero(g, treat_colors_separately=True, ignore_positions=ignore):
        cg=grid_from_component(g,cells)
        _,c0,_,c1=bbox(cells)
        center=(c0+c1)/2
        cmd_code=min(commands, key=lambda t: abs(center-t[0]))[1]
        transformed.append(transform(cg, cmd_code))
    transformed=sorted(transformed, key=lambda cg:(-count_nonzero(cg), min(v for row in cg for v in row if v!=0)))
    return pack_components(transformed, axis="horizontal", gap=1, canvas_size=(h,w), anchor=(1,0))
```

### H79 — Infer A→B, Apply It to C
**Difficulty:** hard
**Train pairs:** 4
**Skills:** analogy, transform inference
**Suggested staged path:** The first two framed panels show the transform. Apply that same transform to the third panel.

**Train 1 — input**
```text
0000000000000000000
0999990999990999990
0920090900290933090
0922090902290903090
0902090902090903390
0999990999990999990
0000000000000000000
```
**Train 1 — output**
```text
033
030
330
```

**Train 2 — input**
```text
0000000000000000000
0999990999990999990
0904090944090950090
0944490904490955090
0940090904090905590
0999990999990999990
0000000000000000000
```
**Train 2 — output**
```text
055
550
500
```

**Train 3 — input**
```text
0000000000000000000
0999990999990999990
0922090902090900690
0902090902090966690
0902090902290960090
0999990999990999990
0000000000000000000
```
**Train 3 — output**
```text
006
666
600
```

**Train 4 — input**
```text
0000000000000000000
0999990999990999990
0930090903090907790
0933390933390907090
0903090930090977090
0999990999990999990
0000000000000000000
```
**Train 4 — output**
```text
770
070
077
```

**Test — input**
```text
0000000000000000000
0999990999990999990
0950590955590902090
0955090905090922290
0950090900590900290
0999990999990999990
0000000000000000000
```
**Test — output**
```text
020
022
220
```

**Written solution**

Extract the three framed inner patterns. Determine which allowed transform maps A to B, then apply that same transform to C and output the transformed third pattern.

**Reference program**

```python
def rule_h79(g):
    frames=sorted(find_rect_frames(g, frame_color=9), key=lambda item:item[2][1])
    inners=[]
    for _,cells,(r0,c0,r1,c1) in frames[:3]:
        inner=[row[c0+1:c1] for row in g[r0+1:r1]]  # 3x3 if frame 5x5
        inners.append(inner)
    A,B,C=inners
    code=None
    for t in (1,2,3,4):
        if transform(A,t)==B:
            code=t; break
    if code is None:
        # maybe identity? but we won't use it
        code=1
    return transform(C,code)
```

### H80 — Nearest-Seed Fill with Ties
**Difficulty:** hard
**Train pairs:** 4
**Skills:** distance fields, tie handling
**Suggested staged path:** Every empty cell belongs to its nearest seed, unless two or more seeds are equally near.

**Train 1 — input**
```text
99999999999
90000000009
90200000309
90000000009
90000000009
90000000009
90000400009
90000000009
99999999999
```
**Train 1 — output**
```text
99999999999
92222833339
92222833339
92222433339
92224443339
92244444339
94444444449
94444444449
99999999999
```

**Train 2 — input**
```text
999999999999
900000000009
905000000709
900000000009
900000000009
900000000009
900000000009
900003000009
900000000009
999999999999
```
**Train 2 — output**
```text
999999999999
955555777779
955555777779
955558777779
955583377779
955833337779
988333333779
933333333339
933333333339
999999999999
```

**Train 3 — input**
```text
99999999999
90000000009
90200000009
90000000009
90000000009
90000400009
90000000009
90000000009
90000000609
90000000009
99999999999
```
**Train 3 — output**
```text
99999999999
92222888889
92222888889
92228444889
92284444889
98844444889
98844448669
98844486669
98888866669
98888866669
99999999999
```

**Train 4 — input**
```text
9999999999999
9000000000009
9020000000609
9000000000009
9000000000009
9000000000009
9000004000009
9000000000009
9999999999999
```
**Train 4 — output**
```text
9999999999999
9222228666669
9222228666669
9222284866669
9222844486669
9228444448669
9884444444889
9884444444889
9999999999999
```

**Test — input**
```text
999999999999
900000000009
900300000009
900000000709
900000000009
900000000009
900000000009
900000005009
900000000009
999999999999
```
**Test — output**
```text
999999999999
933333377779
933333377779
933333777779
933333777779
933338555779
933385555559
988855555559
988855555559
999999999999
```

**Written solution**

For every zero cell inside the board, compute Manhattan distance to each colored seed. Fill the cell with the unique nearest seed color, or with 8 if the nearest distance is tied. Keep the seeds and the 9 border unchanged.

**Reference program**

```python
def rule_h80(g):
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,9)]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            dists=[(abs(r-sr)+abs(c-sc), val) for sr,sc,val in seeds]
            mind=min(d for d,_ in dists)
            colors={val for d,val in dists if d==mind}
            out[r][c]=colors.pop() if len(colors)==1 else 8
    return out
```

### H81 — Recolor by Nesting Depth
**Difficulty:** hard
**Train pairs:** 4
**Skills:** frame containment, depth counting
**Suggested staged path:** Only the small marker cells change. Their new color is how many frames contain them.

**Train 1 — input**
```text
9999999999999
9100000000009
9099999999909
9091000000909
9090999990909
9090910090909
9090999990909
9090000001909
9099999999909
9000000000009
9999999999999
```
**Train 1 — output**
```text
9999999999999
9100000000009
9099999999909
9092000000909
9090999990909
9090930090909
9090999990909
9090000002909
9099999999909
9000000000009
9999999999999
```

**Train 2 — input**
```text
999999999999
910000000009
900000000009
900999999009
900910009009
900900009009
900900009009
900900009009
900999999009
900000000109
900000000009
999999999999
```
**Train 2 — output**
```text
999999999999
910000000009
900000000009
900999999009
900920009009
900900009009
900900009009
900900009009
900999999009
900000000109
900000000009
999999999999
```

**Train 3 — input**
```text
999999999999999
900000000000019
909999999999909
909100000000909
909099999990909
909091000090909
909090000090909
909090000090909
909099999990909
909000000001909
909999999999909
900000000000009
999999999999999
```
**Train 3 — output**
```text
999999999999999
900000000000019
909999999999909
909200000000909
909099999990909
909093000090909
909090000090909
909090000090909
909099999990909
909000000002909
909999999999909
900000000000009
999999999999999
```

**Train 4 — input**
```text
10000000000
09999999990
09100000090
09099999090
09090009090
09090109090
09090009090
09099999090
09000000190
09999999990
00000000000
```
**Train 4 — output**
```text
00000000000
09999999990
09100000090
09099999090
09090009090
09090209090
09090009090
09099999090
09000000190
09999999990
00000000000
```

**Test — input**
```text
99999999999999
91000000000009
90099999999009
90091000009009
90090000009009
90090000009009
90090000009009
90090000009009
90090000009009
90099999999009
90000000000019
99999999999999
```
**Test — output**
```text
99999999999999
91000000000009
90099999999009
90092000009009
90090000009009
90090000009009
90090000009009
90090000009009
90090000009009
90099999999009
90000000000019
99999999999999
```

**Written solution**

Detect all rectangular 9-frames. For each nonzero, non-frame marker cell, count how many frame interiors contain it, and recolor that marker with the resulting nesting depth while leaving the frames untouched.

**Reference program**

```python
def rule_h81(g):
    frames=[bbox(cells) for col,cells,b in find_rect_frames(g, frame_color=9)]
    out=clone(g)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,9):
                depth=sum(1 for r0,c0,r1,c1 in frames if r0<r<r1 and c0<c<c1)
                out[r][c]=depth
    return out
```

### H82 — Ray-Overlap Map
**Difficulty:** hard
**Train pairs:** 4
**Skills:** overlap counting, projection geometry
**Suggested staged path:** Project every seed in four directions, but only keep the cells reached by at least two rays.

**Train 1 — input**
```text
99999999999
90000000009
90200000309
90000000009
90000000009
90000000009
90000400009
90000000009
99999999999
```
**Train 1 — output**
```text
99999999999
90000000009
98888888889
90000000009
90000000009
90000000009
90800000809
90000000009
99999999999
```

**Train 2 — input**
```text
999999999999
900000900009
905000900709
900000900009
900000900009
900000900009
900000900009
900003900009
900000900009
999999999999
```
**Train 2 — output**
```text
999999999999
900000900009
900008900009
900000900009
900000900009
900000900009
900000900009
908000900009
900000900009
999999999999
```

**Train 3 — input**
```text
99999999999
90000000009
90200000009
90000000009
90000000009
99999499999
90000000009
90000000009
90000000609
90000000009
99999999999
```
**Train 3 — output**
```text
99999999999
90000000009
90000800009
90000000009
90000000009
99999099999
90000000009
90000000009
90000800009
90000000009
99999999999
```

**Train 4 — input**
```text
9999999999999
9000009000009
9020009000609
9000009000009
9000009000009
9000009000009
9000004000009
9000009000009
9999999999999
```
**Train 4 — output**
```text
9999999999999
9000009000009
9000009000009
9000009000009
9000009000009
9000009000009
9080000000809
9000009000009
9999999999999
```

**Test — input**
```text
999999999999
900000000009
900300000009
900000000709
999999999999
900000000009
900000000009
900000005009
900000000009
999999999999
```
**Test — output**
```text
999999999999
900000000009
900000000809
900800000009
999999999999
900000000009
900000000009
900000000009
900000000009
999999999999
```

**Written solution**

From each seed, project inclusive rays along the four cardinal directions until a wall blocks them. Count how many projected paths touch each cell and output 8 exactly where that count is at least two, with 9 walls preserved.

**Reference program**

```python
def rule_h82(g):
    h,w=size(g)
    counts=[[0]*w for _ in range(h)]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (0,9):
                continue
            counts[r][c]+=1
            for dr,dc in DIR4:
                nr,nc=r+dr,c+dc
                while 0<=nr<h and 0<=nc<w and g[nr][nc]!=9:
                    counts[nr][nc]+=1
                    nr+=dr; nc+=dc
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                out[r][c]=9
            elif counts[r][c]>=2:
                out[r][c]=8
    return out
```

### H83 — Area Comparison Matrix
**Difficulty:** hard
**Train pairs:** 4
**Skills:** component measurement, pairwise comparison
**Suggested staged path:** Order the components consistently, then compare every area to every other area.

**Train 1 — input**
```text
00000000000000
02220000040000
00000000444000
00000000040000
00000000000000
03300000000000
03300000000000
00000000000000
00000000050000
00000000050000
00000000055000
00000000000000
```
**Train 1 — output**
```text
2111
3212
3323
3212
```

**Train 2 — input**
```text
000000000000000
022000000000000
020000000000000
000000000044000
000000000044000
000000000000000
030000000000000
030000000000000
030000005550000
000000000500000
000000000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
2211
2211
3322
3322
```

**Train 3 — input**
```text
00000000000000
02220000000000
02220000004400
00000000004400
00000000000000
00000000000000
00300000000000
03330000000000
00300000000000
00000000555500
00000000000000
00000000000000
```
**Train 3 — output**
```text
2333
1233
1122
1122
```

**Train 4 — input**
```text
000000000000000
000000000044400
020000000044400
020000000000000
022000000000000
000000000000000
003000000000000
003000000000000
033000000555000
000000000555000
000000000000000
000000000000000
000000000000000
```
**Train 4 — output**
```text
2211
2211
3322
3322
```

**Test — input**
```text
00000000000000
02200000055500
02000000050500
00000000055500
00000000000000
03300000000000
00300004444444
00000004004004
00000004004004
00000004444444
00000000000000
00000000000000
```
**Test — output**
```text
2211
2211
3323
3312
```

**Written solution**

Order the components by color and compute their areas. Build a square matrix whose entry is 1 when the row component is smaller, 2 when the two areas are equal, and 3 when the row component is larger.

**Reference program**

```python
def rule_h83(g):
    comps=sorted(components_nonzero(g, treat_colors_separately=True), key=lambda item:item[0])
    areas=[len(cells) for _,cells in comps]
    n=len(areas)
    out=blank(n,n)
    for i,a in enumerate(areas):
        for j,b in enumerate(areas):
            out[i][j]=1 if a<b else 2 if a==b else 3
    return out
```

### H84 — Ranked Component with Composed Transforms
**Difficulty:** hard
**Train pairs:** 4
**Skills:** ranking, transform composition
**Suggested staged path:** First decide which component to keep. Then apply the two command transforms in sequence.

**Train 1 — input**
```text
20000000000013
00000000000000
00200000000000
02220000000000
00200000000000
00000000044400
00000000000000
00030000000000
00030000005550
00033000005550
00000000000000
00000000000000
```
**Train 1 — output**
```text
020
222
020
```

**Train 2 — input**
```text
100000000000024
000000000000000
000000000004400
022220000004400
022220000000000
000000000000000
000000000000000
000000000000000
000000000000500
003300000000500
003000000000500
000000000000000
000000000000000
```
**Train 2 — output**
```text
2222
2222
```

**Train 3 — input**
```text
30000000000031
00000000000000
02020000000000
02220000000000
00000000000050
00000000000050
03330000000050
03330000000000
00000000040000
00000000040000
00000000044000
00000000000000
```
**Train 3 — output**
```text
400
444
```

**Train 4 — input**
```text
200000000000042
000000000000000
000000000000000
002000000000000
022200000000000
002000000000440
000000000000400
000000000000000
033330000000000
033330005000000
000000005000000
000000005500000
000000000000000
```
**Train 4 — output**
```text
020
222
020
```

**Test — input**
```text
10000000000011
00000000000000
00000000000000
02000000000000
02200000000000
00220000044400
00000000044400
00000000000000
03300000005550
03300000000000
00000000000000
00000000000000
```
**Test — output**
```text
444
444
```

**Written solution**

Ignore the command markers, rank the components by descending area, select the k-th largest one, crop it tightly, and apply the first commanded transform followed by the second one.

**Reference program**

```python
def rule_h84(g):
    h,w=size(g)
    k=g[0][0]
    t1=g[0][w-2]
    t2=g[0][w-1]
    ignore={(0,0),(0,w-2),(0,w-1)}
    comps=[grid_from_component(g,cells) for col,cells in components_nonzero(g, treat_colors_separately=True, ignore_positions=ignore)]
    comps=sorted(comps, key=lambda cg:(-count_nonzero(cg), min(v for row in cg for v in row if v!=0)))
    target=comps[k-1]
    return transform(transform(target,t1),t2)
```
