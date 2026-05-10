# ARC Additional Puzzle Bank — 21 Puzzles (Set 3)

This is a third pack of 21 ARC-style puzzles, continuing the numbering from the earlier banks: `E15–E21`, `M15–M21`, `H15–H21`.

This set deliberately increases supervision density. It contains **70 train pairs across 21 puzzles**, averaging **3.33 train pairs per puzzle**. That is meant to make the intended hypothesis a little less underdetermined for staged, iterative solvers.

Design goals for this set:

- easy: crisp local rules and short row/column/2×2 motifs
- medium: components, frames, selection, ranking, and translation
- hard: conditional axes, nested depth, template reuse, vector transport, and dynamic-size outputs
- every puzzle includes a short staged hint, a written solution, and a trustworthy Python reference program

Companion files:

- `arc_additional_puzzles_21_set3.py` — reference solvers + validation
- `arc_additional_puzzles_21_set3.json` — machine-readable puzzle bank


## Easy (7)


### E15 — Diagonal Halo

**Difficulty:** easy


**Train pairs:** 3


**Skills:** diagonal neighborhood, edge clipping, copy-preserve


**Suggested staged path:** First locate the 2-cells, then consider only their four diagonal neighbors.


**Train 1 — input**

```text
000000
020000
000000
000020
000000
200000
```

**Train 1 — output**

```text
606000
020000
606606
000020
060606
200000
```


**Train 2 — input**

```text
0000000
0002000
0000000
2000000
0000020
0000000
0000000
```

**Train 2 — output**

```text
0060600
0002000
0660600
2000606
0600020
0000606
0000000
```


**Train 3 — input**

```text
00000000
00000000
00200020
00000000
00000000
00000000
00002000
00000000
```

**Train 3 — output**

```text
00000000
06060606
00200020
06060606
00000000
00060600
00002000
00060600
```

**Test — input**

```text
000000000
000000020
000000000
000000000
020000000
000000000
000000200
000000000
000000000
```

**Expected test output**

```text
000000606
000000020
000000606
606000000
020000000
606006060
000000200
000006060
000000000
```

**Written solution**

Each 2 acts like a diagonal beacon. Keep the 2 itself, and paint each in-bounds diagonal neighbor with 6. Leave all other cells unchanged.

**Reference program**

```python
def rule_e15(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w and out[nr][nc]==0:
                        out[nr][nc]=6
    return out
```


### E16 — X-Center Fill

**Difficulty:** easy


**Train pairs:** 3


**Skills:** diagonal pattern detection, same-size recolor, local motifs


**Suggested staged path:** Ignore the outer 1s at first. Ask which empty cell sits exactly in the middle of an X made of four diagonal 1s.


**Train 1 — input**

```text
0000000
0101000
0000000
0101101
0000000
0000101
0000000
```

**Train 1 — output**

```text
0000000
0101000
0080000
0101101
0000080
0000101
0000000
```


**Train 2 — input**

```text
00000000
00001010
00000000
00001010
01010000
00000000
01010000
00000000
```

**Train 2 — output**

```text
00000000
00001010
00000800
00001010
01010000
00800000
01010000
00000000
```


**Train 3 — input**

```text
000000000
000000000
001010101
000000000
001010101
000010100
000000000
000010100
000000000
```

**Train 3 — output**

```text
000000000
000000000
001010101
000808080
001010101
000010100
000008000
000010100
000000000
```

**Test — input**

```text
0000000000
0101000000
0000000000
0101000000
0000010100
0000000000
0010110100
0000000000
0010100000
```

**Expected test output**

```text
0000000000
0101000000
0080000000
0101000000
0000010100
0000008000
0010110100
0008000000
0010100000
```

**Written solution**

Whenever a 0 cell has 1s on all four diagonal neighbors, change that center cell to 8. Everything else stays as it was.

**Reference program**

```python
def rule_e16(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r-1][c-1]==1 and g[r-1][c+1]==1 and g[r+1][c-1]==1 and g[r+1][c+1]==1:
                out[r][c]=8
    return out
```


### E17 — Horizontal Sandwich

**Difficulty:** easy


**Train pairs:** 3


**Skills:** rowwise local rule, flanking cells, pattern completion


**Suggested staged path:** Work row by row. Only look for 5-0-5 triples and ignore every other arrangement.


**Train 1 — input**

```text
00000000
05050000
00000000
00000000
00005050
00000000
```

**Train 1 — output**

```text
00000000
05350000
00000000
00000000
00005350
00000000
```


**Train 2 — input**

```text
000000000
000000000
505005050
000000000
000000000
000505000
000000000
```

**Train 2 — output**

```text
000000000
000000000
535005350
000000000
000000000
000535000
000000000
```


**Train 3 — input**

```text
0000000000
0000005050
0000000000
0050500000
0000000000
0000000000
5050000000
0000000000
```

**Train 3 — output**

```text
0000000000
0000005350
0000000000
0053500000
0000000000
0000000000
5350000000
0000000000
```

**Test — input**

```text
0000000000
0005050000
0000000000
0000000000
0505000000
0000000000
0000000000
0000005050
0000000000
```

**Expected test output**

```text
0000000000
0005350000
0000000000
0000000000
0535000000
0000000000
0000000000
0000005350
0000000000
```

**Written solution**

If a cell is 0 and its immediate left and right neighbors are both 5, recolor that middle cell to 3. Keep the two 5s and everything else unchanged.

**Reference program**

```python
def rule_e17(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==5 and g[r][c+1]==5:
                out[r][c]=3
    return out
```


### E18 — Vertical Sandwich

**Difficulty:** easy


**Train pairs:** 3


**Skills:** columnwise local rule, flanking cells, pattern completion


**Suggested staged path:** Work column by column. Only cells with a 7 directly above and below can change.


**Train 1 — input**

```text
000000
070000
000000
070070
000000
000070
000000
```

**Train 1 — output**

```text
000000
070000
040000
070070
000040
000070
000000
```


**Train 2 — input**

```text
00000070
00000000
00000070
00000000
00700000
00000000
00700000
00000000
```

**Train 2 — output**

```text
00000070
00000040
00000070
00000000
00700000
00400000
00700000
00000000
```


**Train 3 — input**

```text
000000000
000000000
000700000
000000000
000700000
000000070
000000000
000000070
000000000
```

**Train 3 — output**

```text
000000000
000000000
000700000
000400000
000700000
000000070
000000040
000000070
000000000
```

**Test — input**

```text
000000000
000070000
000000000
000070000
070000000
000000000
070000070
000000000
000000070
000000000
```

**Expected test output**

```text
000000000
000070000
000040000
000070000
070000000
040000000
070000070
000000040
000000070
000000000
```

**Written solution**

If a cell is 0 and the cells immediately above and below it are both 7, recolor that middle cell to 4. Leave all other cells alone.

**Reference program**

```python
def rule_e18(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]==7 and g[r+1][c]==7:
                out[r][c]=4
    return out
```


### E19 — Diagonal Square Completion

**Difficulty:** easy


**Train pairs:** 3


**Skills:** 2x2 reasoning, diagonal relations, local completion


**Suggested staged path:** Look only at 2x2 windows. Ask whether two opposite corners already contain 8 and the other two are empty.


**Train 1 — input**

```text
000000
080000
008000
000008
000080
000000
```

**Train 1 — output**

```text
000000
081000
018000
000018
000081
000000
```


**Train 2 — input**

```text
0008000
0080000
0000000
0000080
0800008
0080000
0000000
```

**Train 2 — output**

```text
0018000
0081000
0000000
0000081
0810018
0180000
0000000
```


**Train 3 — input**

```text
00000000
00000800
00000080
00000000
00080000
00800000
08000000
80000000
```

**Train 3 — output**

```text
00000000
00000810
00000180
00000000
00180000
01810000
18100000
81000000
```

**Test — input**

```text
000000000
008000000
080000800
000000080
000000000
000800000
000080000
000000000
```

**Expected test output**

```text
000000000
018000000
081000810
000000180
000000000
000810000
000180000
000000000
```

**Written solution**

In any 2x2 block where the two 8s occupy one diagonal and the other diagonal is empty, fill the two empty cells with 1. Leave the 8s as they are.

**Reference program**

```python
def rule_e19(g):
    h,w=size(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            block=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if block[0]==8 and block[3]==8 and block[1]==0 and block[2]==0:
                out[r][c+1]=1; out[r+1][c]=1
            if block[1]==8 and block[2]==8 and block[0]==0 and block[3]==0:
                out[r][c]=1; out[r+1][c+1]=1
    return out
```


### E20 — Horizontal Bar Caps

**Difficulty:** easy


**Train pairs:** 3


**Skills:** adjacent-pair detection, rowwise extension, edge clipping


**Suggested staged path:** Find the horizontal 4-4 dominos first. Then add only the immediate zero cells just outside those dominos.


**Train 1 — input**

```text
00000000
04400000
00000000
00000000
00004400
00000000
```

**Train 1 — output**

```text
00000000
94490000
00000000
00000000
00094490
00000000
```


**Train 2 — input**

```text
000000000
000000000
000440000
000000000
000000000
440000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
009449000
000000000
000000000
449000000
000000000
```


**Train 3 — input**

```text
0000000000
0000004400
0000000000
0440000000
0000000000
0000000000
0000440000
0000000000
```

**Train 3 — output**

```text
0000000000
0000094490
0000000000
9449000000
0000000000
0000000000
0009449000
0000000000
```

**Test — input**

```text
0000000000
0044000000
0000000000
0000000000
0000004400
0000000000
0000000000
4400000000
0000000000
```

**Expected test output**

```text
0000000000
0944900000
0000000000
0000000000
0000094490
0000000000
0000000000
4490000000
0000000000
```

**Written solution**

Each horizontal 4-4 bar gets capped with 9 on its immediate left and right whenever those cells exist and are 0. The original 4s stay in place.

**Reference program**

```python
def rule_e20(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w-1):
            if g[r][c]==4 and g[r][c+1]==4:
                if c-1 >= 0 and g[r][c-1]==0:
                    out[r][c-1]=9
                if c+2 < w and g[r][c+2]==0:
                    out[r][c+2]=9
    return out
```


### E21 — Marker Takes the Row Color

**Difficulty:** easy


**Train pairs:** 3


**Skills:** row aggregation, marker replacement, single-color rows


**Suggested staged path:** Treat each row separately. First identify the unique nonzero color in that row, then use it to replace the 9 marker.


**Train 1 — input**

```text
00000000
03300090
00000000
00000000
50009000
00000000
```

**Train 1 — output**

```text
00000000
03300030
00000000
00000000
50005000
00000000
```


**Train 2 — input**

```text
000000000
000000000
900700000
000000000
000000000
009000220
000000000
```

**Train 2 — output**

```text
000000000
000000000
700700000
000000000
000000000
002000220
000000000
```


**Train 3 — input**

```text
0000000000
0444000090
0000000000
6000090000
0000000000
0000000000
0900000800
0000000000
```

**Train 3 — output**

```text
0000000000
0444000040
0000000000
6000060000
0000000000
0000000000
0800000800
0000000000
```

**Test — input**

```text
0000000000
0022000090
0000000000
0000000000
0900060000
0000000000
0000000000
0000009440
0000000000
```

**Expected test output**

```text
0000000000
0022000020
0000000000
0000000000
0600060000
0000000000
0000000000
0000004440
0000000000
```

**Written solution**

If a row contains exactly one distinct nonzero color besides 9, replace every 9 in that row with that color. Rows that do not meet that condition stay unchanged.

**Reference program**

```python
def rule_e21(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        colors={v for v in g[r] if v not in (0,9)}
        has9=any(v==9 for v in g[r])
        if len(colors)==1 and has9:
            color=next(iter(colors))
            for c in range(w):
                if g[r][c]==9:
                    out[r][c]=color
    return out
```


## Medium (7)


### M15 — Crop the Marked Component

**Difficulty:** medium


**Train pairs:** 3


**Skills:** component detection, marker-object association, bbox crop


**Suggested staged path:** First find which 3-object touches the 2 marker. Only after that should you crop anything.


**Train 1 — input**

```text
0000000000
0300000000
0300000030
0330000333
0000000000
0000023300
0000000330
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
330
033
```


**Train 2 — input**

```text
00000000000
00000030000
00000333000
00000000000
00000000000
00000000000
23030000000
03330000300
00000000300
00000000330
00000000000
```

**Train 2 — output**

```text
303
333
```


**Train 3 — input**

```text
000000000000
000000000200
000000000300
003300003330
000330000000
000000000000
000000000000
000000000000
000000030000
000000030000
000000033000
000000000000
```

**Train 3 — output**

```text
030
333
```

**Test — input**

```text
0000000000000
0000000000000
0003000000000
0033300000000
0000000000000
0000000003300
0000000000330
2303000000000
0333000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
303
333
```

**Written solution**

Among all 3-colored components, choose the one that is orthogonally adjacent to the 2 marker. Output the bounding-box crop of that component alone.

**Reference program**

```python
def rule_m15(g):
    h,w=size(g)
    marker_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    comps=[cells for val,cells in components(g, colors={3})]
    marker_set=set(marker_cells)
    chosen=None
    for cells in comps:
        s=set(cells)
        for r,c in cells:
            for nr,nc in orth_neighbors(r,c,h,w):
                if (nr,nc) in marker_set:
                    chosen=cells
                    break
            if chosen is not None:
                break
        if chosen is not None:
            break
    assert chosen is not None
    r0,r1,c0,c1=bbox(chosen)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in chosen:
        out[r-r0][c-c0]=3
    return out
```


### M16 — Frame Border Recolor from Seed

**Difficulty:** medium


**Train pairs:** 3


**Skills:** frame detection, inside/outside reasoning, color transfer


**Suggested staged path:** Find each rectangular 1-frame first. Then read the single seed color inside it and copy that color to the whole border.


**Train 1 — input**

```text
000000000000
011111000000
010401000000
010001000000
011111000000
000000011110
000000016010
000000010010
000000011110
000000000000
```

**Train 1 — output**

```text
000000000000
044444000000
040404000000
040004000000
044444000000
000000066660
000000066060
000000060060
000000066660
000000000000
```


**Train 2 — input**

```text
00000000111
00000000121
00111111101
00100001111
00100801000
00100001000
00111111000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000111
00000000121
00111111101
00100001111
00100801000
00100001000
00111111000
00000000000
00000000000
00000000000
00000000000
```


**Train 3 — input**

```text
000000000000
011110000000
013010001110
010010001510
011110001010
000000001110
001111110000
001000010000
001007010000
001000010000
001111110000
000000000000
```

**Train 3 — output**

```text
000000000000
033330000000
033030005550
030030005550
033330005050
000000005550
007777770000
007000070000
007007070000
007000070000
007777770000
000000000000
```

**Test — input**

```text
0000000000000
0011111000000
0010001000000
0010601000000
0010001000000
0011111000000
0000000111110
0111100104010
0180100100010
0111100111110
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0066666000000
0060006000000
0060606000000
0060006000000
0066666000000
0000000444440
0888800404040
0880800400040
0888800444440
0000000000000
0000000000000
```

**Written solution**

Every 1-colored rectangular frame contains one nonzero seed color in its interior. Recolor the entire border of that frame to the seed color, while leaving the interior seed and zeros unchanged.

**Reference program**

```python
def rule_m16(g):
    h,w=size(g); out=clone(g)
    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for cells in frames:
        r0,r1,c0,c1=bbox(cells)
        interior_colors={g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,1)}
        if len(interior_colors)==1:
            color=next(iter(interior_colors))
            for r,c in cells:
                out[r][c]=color
    return out
```


### M17 — Horizontal Mirror Inside the Frame

**Difficulty:** medium


**Train pairs:** 3


**Skills:** frame-local symmetry, horizontal reflection, object augmentation


**Suggested staged path:** Ignore the border once you have found it. Focus on where each 4 would land if reflected across the frame's horizontal axis.


**Train 1 — input**

```text
0000000000
0111111110
0104000010
0100040010
0100000010
0100000010
0100000010
0100000010
0111111110
0000000000
```

**Train 1 — output**

```text
0000000000
0111111110
0104000010
0100040010
0100000010
0100000010
0100070010
0107000010
0111111110
0000000000
```


**Train 2 — input**

```text
000000000000
000000000000
001111111100
001040000100
001000040100
001000000100
001000000100
001004000100
001111111100
000000000000
000000000000
```

**Train 2 — output**

```text
000000000000
000000000000
001111111100
001047000100
001000040100
001000000100
001000070100
001074000100
001111111100
000000000000
000000000000
```


**Train 3 — input**

```text
00000000000
00011111100
00014000100
00010000100
00010000100
00010040100
00010000100
00010000100
00010004100
00010000100
00011111100
00000000000
```

**Train 3 — output**

```text
00000000000
00011111100
00014000100
00010007100
00010000100
00010040100
00010070100
00010000100
00010004100
00017000100
00011111100
00000000000
```

**Test — input**

```text
000000000000
011111111110
014000000010
010000040010
010000000010
010000000010
010000000010
010000000010
010004000010
010000000010
011111111110
000000000000
```

**Expected test output**

```text
000000000000
011111111110
014000000010
010007040010
010000000010
010000000010
010000000010
010000000010
010004070010
017000000010
011111111110
000000000000
```

**Written solution**

Inside each rectangular 1-frame, every 4-cell gets a mirrored partner across the frame's horizontal axis. Add that partner as 7 if the mirrored spot is empty; keep the original 4s and the frame.

**Reference program**

```python
def rule_m17(g):
    h,w=size(g); out=clone(g)
    frames=[cells for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for cells in frames:
        r0,r1,c0,c1=bbox(cells)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]==4:
                    mr = r0 + r1 - r
                    if out[mr][c]==0:
                        out[mr][c]=7
    return out
```


### M18 — Outer Corner Markers

**Difficulty:** medium


**Train pairs:** 3


**Skills:** solid-rectangle detection, bounding boxes, edge clipping


**Suggested staged path:** Find each solid 6-rectangle, then step one cell outward from each bbox corner.


**Train 1 — input**

```text
0000000000
0666000000
0666000000
0000000000
0000000000
0000006600
0000006600
0000006600
0000000000
0000000000
```

**Train 1 — output**

```text
2000200000
0666000000
0666000000
2000200000
0000020020
0000006600
0000006600
0000006600
0000020020
0000000000
```


**Train 2 — input**

```text
000066000000
000066000000
000000000000
000000000000
066660000000
066660000000
066660000000
000000000660
000000000660
```

**Train 2 — output**

```text
000066000000
000066000000
000200200000
200002000000
066660000000
066660000000
066660002002
200002000660
000000000660
```


**Train 3 — input**

```text
00000000000
00000000660
00666000660
00666000660
00666000000
00666000000
00000000000
00000000000
00006666000
00006666000
00000000000
```

**Train 3 — output**

```text
00000002002
02000200660
00666000660
00666000660
00666002002
00666000000
02000200000
00020000200
00006666000
00006666000
00020000200
```

**Test — input**

```text
000000000000
066600000000
066600000000
066600000000
000000000000
000000066000
000000066000
000000066000
000000066000
006666600000
006666600000
000000000000
```

**Expected test output**

```text
200020000000
066600000000
066600000000
066600000000
200020200200
000000066000
000000066000
000000066000
020000066000
006666600200
006666600000
020000020000
```

**Written solution**

For every solid rectangular 6-object, place a 2 one cell outside each of its four bounding-box corners whenever that outside cell lies inside the grid. Keep the rectangles themselves unchanged.

**Reference program**

```python
def rule_m18(g):
    h,w=size(g); out=clone(g)
    for val,cells in components(g, colors={6}):
        if not is_solid_rect(cells):
            continue
        r0,r1,c0,c1=bbox(cells)
        for rr,cc in [(r0-1,c0-1),(r0-1,c1+1),(r1+1,c0-1),(r1+1,c1+1)]:
            if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                out[rr][cc]=2
    return out
```


### M19 — Recolor by Size Rank

**Difficulty:** medium


**Train pairs:** 3


**Skills:** component sizing, sorting, shape preservation


**Suggested staged path:** Do not change shapes. Only compare component sizes and assign the three output colors by rank.


**Train 1 — input**

```text
0000000000
0880000000
0000000000
0000000000
0880000000
0880000000
0000008880
0000008880
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0220000000
0000000000
0000000000
0330000000
0330000000
0000004440
0000004440
0000000000
0000000000
```


**Train 2 — input**

```text
00000000000
00000008880
00000000000
00000000000
00000000000
08800000000
08800000000
08000000000
00008880000
00008880000
00000000000
```

**Train 2 — output**

```text
00000000000
00000002220
00000000000
00000000000
00000000000
03300000000
03300000000
03000000000
00004440000
00004440000
00000000000
```


**Train 3 — input**

```text
000000000000
000000000000
000000000880
000000000000
000000000000
000000000000
080800000000
088800000000
000000088800
000000088800
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000220
000000000000
000000000000
000000000000
030300000000
033300000000
000000044400
000000044400
000000000000
000000000000
```

**Test — input**

```text
0000000000000
0888000000000
0000000000000
0000000000000
0000000000000
0000000088000
0000000088000
0000000000000
0088800000000
0088800000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0222000000000
0000000000000
0000000000000
0000000000000
0000000033000
0000000033000
0000000000000
0044400000000
0044400000000
0000000000000
0000000000000
```

**Written solution**

There are exactly three 8-colored components. Recolor the smallest one to 2, the middle-sized one to 3, and the largest one to 4, preserving every component's shape and position.

**Reference program**

```python
def rule_m19(g):
    h,w=size(g); out=blank(h,w)
    comps=[cells for val,cells in components(g, colors={8})]
    comps_sorted=sorted(comps, key=lambda cells: len(cells))
    recolors=[2,3,4]
    assert len(comps_sorted)==3
    for color,cells in zip(recolors, comps_sorted):
        for r,c in cells:
            out[r][c]=color
    return out
```


### M20 — Legend-Selected Crop

**Difficulty:** medium


**Train pairs:** 3


**Skills:** legend decoding, component selection, bbox crop


**Suggested staged path:** Read the single nonzero legend color in the top row before looking at any lower objects.


**Train 1 — input**

```text
0004000000
0000000000
0300000660
0300000660
0330000000
0000000400
0000004440
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
040
444
```


**Train 2 — input**

```text
00000600000
00000000000
00000000000
02020000000
02220000440
00000000440
00000066000
00000006600
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
660
066
```


**Train 3 — input**

```text
000000000300
000000000000
000000050000
000000555000
000000000000
003300000000
003300000000
003000000000
000000007700
000000000770
000000000000
000000000000
```

**Train 3 — output**

```text
33
33
30
```

**Test — input**

```text
0000700000000
0000000000000
0000000002200
0400000000220
0400000000000
0440000000000
0000000707000
0000000777000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
707
777
```

**Written solution**

The top row contains one nonzero legend color. Among the components below, select the component of that color and output its bounding-box crop.

**Reference program**

```python
def rule_m20(g):
    h,w=size(g)
    legend_colors=[v for v in g[0] if v!=0]
    assert len(legend_colors)==1
    target=legend_colors[0]
    candidates=[]
    for val,cells in components(g):
        if val==target and all(r>0 for r,c in cells):
            candidates.append(cells)
    assert len(candidates)>=1
    chosen=sorted(candidates, key=lambda cells: (bbox(cells)[0], bbox(cells)[2]))[0]
    return crop_bbox(g, chosen)
```


### M21 — Translate the Component to the Marker

**Difficulty:** medium


**Train pairs:** 3


**Skills:** component translation, bbox anchoring, same-size output


**Suggested staged path:** Find the top-left corner of the 5-object's bounding box. The marker tells you where that corner should move.


**Train 1 — input**

```text
0000000000
0000000000
0050000000
0050000000
0055000000
0000000000
0000020000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000050000
0000050000
0000055000
0000000000
```


**Train 2 — input**

```text
00000000000
02000000000
00000000000
00000000000
00000000000
00000055000
00000005500
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
05500000000
00550000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
00000000000
```


**Train 3 — input**

```text
000000000000
000000000000
000000000000
000000005000
000000055500
000000000000
000000000000
000000000000
002000000000
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000500000000
005550000000
000000000000
000000000000
```

**Test — input**

```text
0000000000000
0000000000000
0200000000000
0000000000000
0000000000000
0000000000000
0000000050500
0000000055500
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0000000000000
0505000000000
0555000000000
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

Take the single 5-colored component and translate it so that the top-left corner of its bounding box lands exactly on the 2 marker. Output only the translated component on a blank grid of the same size.

**Reference program**

```python
def rule_m21(g):
    h,w=size(g)
    comps=[cells for val,cells in components(g, colors={5})]
    assert len(comps)==1
    cells=comps[0]
    marker=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    assert len(marker)==1
    mr,mc=marker[0]
    r0,r1,c0,c1=bbox(cells)
    dr,dc=mr-r0, mc-c0
    out=blank(h,w)
    for r,c in cells:
        nr,nc=r+dr,c+dc
        assert 0<=nr<h and 0<=nc<w
        out[nr][nc]=5
    return out
```


## Hard (7)


### H15 — Axis-Chosen Reflection

**Difficulty:** hard


**Train pairs:** 4


**Skills:** conditional axis choice, reflection, same-size synthesis


**Suggested staged path:** Find whether the 2 marker sits on the top edge or the left edge. That decides whether the mirror axis is vertical or horizontal.


**Train 1 — input**

```text
00000200000
00000000000
00000000000
05000000000
05000000000
05500000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
00000200000
00000000000
00000000000
05000000070
05000000070
05500000770
00000000000
00000000000
00000000000
00000000000
00000000000
```


**Train 2 — input**

```text
000000000000
000000000000
000000000000
000000000000
200000000000
000000000000
000005500000
000000550000
000000000000
000000000000
```

**Train 2 — output**

```text
000000000000
000000770000
000007700000
000000000000
200000000000
000000000000
000005500000
000000550000
000000000000
000000000000
```


**Train 3 — input**

```text
0000200000
0000000000
0000000000
0000000000
0000000500
0000005550
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 3 — output**

```text
0000200000
0000000000
0000000000
0000000000
0700000500
7770005550
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```


**Train 4 — input**

```text
00000000000
00000000000
00000505000
00000555000
00000000000
00000000000
20000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 4 — output**

```text
00000000000
00000000000
00000505000
00000555000
00000000000
00000000000
20000000000
00000000000
00000000000
00000777000
00000707000
```

**Test — input**

```text
000000200000
000000000000
000000000000
000000000000
005500000000
005500000000
005000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Expected test output**

```text
000000200000
000000000000
000000000000
000000000000
005500000770
005500000770
005000000070
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Written solution**

If the 2 marker is in the top row, its column is a vertical mirror axis. If the 2 marker is in the left column, its row is a horizontal mirror axis. Keep the original 5-object, and add its reflected copy in color 7 across that axis.

**Reference program**

```python
def rule_h15(g):
    h,w=size(g); out=clone(g)
    top_markers=[c for c,v in enumerate(g[0]) if v==2]
    left_markers=[r for r in range(h) if g[r][0]==2]
    if top_markers:
        axis_c=top_markers[0]
        for r in range(h):
            for c in range(w):
                if g[r][c]==5:
                    mc=2*axis_c - c
                    if 0<=mc<w and out[r][mc]==0:
                        out[r][mc]=7
    else:
        axis_r=left_markers[0]
        for r in range(h):
            for c in range(w):
                if g[r][c]==5:
                    mr=2*axis_r - r
                    if 0<=mr<h and out[mr][c]==0:
                        out[mr][c]=7
    return out
```


### H16 — Nested Frame Depth Fill

**Difficulty:** hard


**Train pairs:** 4


**Skills:** nested objects, depth counting, region filling


**Suggested staged path:** Treat the 1-borders as frames, not as filled rectangles. Then count how many frames strictly contain each empty cell.


**Train 1 — input**

```text
000000000
011111110
010000010
010111010
010101010
010111010
010000010
011111110
000000000
```

**Train 1 — output**

```text
000000000
011111110
012222210
012111210
012131210
012111210
012222210
011111110
000000000
```


**Train 2 — input**

```text
00000000000
00000000000
00111111100
00100000100
00100000100
00100000100
00100000100
00100000100
00111111100
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00111111100
00122222100
00122222100
00122222100
00122222100
00122222100
00111111100
00000000000
00000000000
```


**Train 3 — input**

```text
0000000000000
0111111111110
0100000000010
0101111111010
0101000001010
0101011101010
0101010101010
0101011101010
0101000001010
0101111111010
0100000000010
0111111111110
0000000000000
```

**Train 3 — output**

```text
0000000000000
0111111111110
0122222222210
0121111111210
0121333331210
0121311131210
0121314131210
0121311131210
0121333331210
0121111111210
0122222222210
0111111111110
0000000000000
```


**Train 4 — input**

```text
00000000000
00111111100
00100000100
00101110100
00101010100
00101010100
00101010100
00101010100
00101110100
00100000100
00111111100
00000000000
```

**Train 4 — output**

```text
00000000000
00111111100
00122222100
00121112100
00121312100
00121312100
00121312100
00121312100
00121112100
00122222100
00111111100
00000000000
```

**Test — input**

```text
000000000000
011111111110
010000000010
010111111010
010100001010
010101111010
010101001010
010101111010
010100001010
010111111010
010000000010
011111111110
000000000000
```

**Expected test output**

```text
000000000000
011111111110
012222222210
012111111210
012122221210
012121111210
012121221210
012121111210
012122221210
012111111210
012222222210
011111111110
000000000000
```

**Written solution**

Every empty cell inside at least one rectangular 1-frame is recolored by its nesting depth: cells inside one frame become 2, cells inside two nested frames become 3, inside three become 4, and so on. The 1-borders remain unchanged.

**Reference program**

```python
def rule_h16(g):
    h,w=size(g); out=clone(g)
    frames=[bbox(cells) for val,cells in components(g, colors={1}) if is_rect_frame(cells)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0:
                depth=sum(1 for r0,r1,c0,c1 in frames if r0<r<r1 and c0<c<c1)
                if depth>0:
                    out[r][c]=depth+1
    return out
```


### H17 — Template Stamping from Markers

**Difficulty:** hard


**Train pairs:** 4


**Skills:** template extraction, repetition, translation


**Suggested staged path:** Find the single 6-template first and record it relative to its own top-left corner. Then stamp that same pattern at every 2 marker.


**Train 1 — input**

```text
000000000000
066000000000
006600000000
000000000000
000000000000
000000020000
000000000000
002000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000066000
000000006600
006600000000
000660000000
000000000000
```


**Train 2 — input**

```text
00000000000
00600000000
00600000000
00660000000
00000000000
00000200000
00000000000
00000000000
02000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00000600000
00000600000
00000660000
06000000000
06000000000
06600000000
```


**Train 3 — input**

```text
000000000000
000000000000
006000000000
066600002000
000000000000
000000000000
000000020000
000000000000
000000000000
000200000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000000600
000000006660
000000000000
000000006000
000000066600
000000000000
000060000000
000666000000
000000000000
```


**Train 4 — input**

```text
0000000000000
0606000000000
0666000000000
0000000000000
0000000000000
0000000002000
0000000000000
0000000000000
0000200000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000006060
0000000006660
0000000000000
0000606000000
0000666000000
0000000000000
```

**Test — input**

```text
0000000000000
0066000000000
0066000000000
0060000002000
0000000000000
0000000000000
0000000020000
0000000000000
0200000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0000000000000
0000000000000
0000000006600
0000000006600
0000000006000
0000000066000
0000000066000
0660000060000
0660000000000
0600000000000
0000000000000
```

**Written solution**

The non-singleton 6-object is a template. Ignore its absolute position, keep only its shape relative to its bounding box, and stamp that shape in color 6 with its top-left corner aligned to every 2 marker. Output only the stamped copies on a blank grid.

**Reference program**

```python
def rule_h17(g):
    h,w=size(g)
    comps=[cells for val,cells in components(g, colors={6})]
    # choose the non-singleton or largest component as template
    template=max(comps, key=len)
    r0,r1,c0,c1=bbox(template)
    rel=[(r-r0,c-c0) for r,c in template]
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in rel:
            nr,nc=mr+dr,mc+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=6
    return out
```


### H18 — Vector Copy by Marker Pair

**Difficulty:** hard


**Train pairs:** 4


**Skills:** translation vectors, copying, same-size synthesis


**Suggested staged path:** Do not guess the destination from the object. First compute the vector from 2 to 3, then apply that vector to every 4-cell.


**Train 1 — input**

```text
0000000000
0200000000
0040000000
0040000000
0044000000
0000030000
0000000000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0040000000
0040000000
0044000000
0000000000
0000008000
0000008000
0000008800
0000000000
```


**Train 2 — input**

```text
000000000000
000000000000
000000000000
000000030000
000000000000
000000000000
004400000000
000440000000
000000000000
020000000000
000000000000
```

**Train 2 — output**

```text
000000008800
000000000880
000000000000
000000000000
000000000000
000000000000
004400000000
000440000000
000000000000
000000000000
000000000000
```


**Train 3 — input**

```text
000000000000
000000000000
002000000000
000000040000
000000444000
000000000000
000000000000
030000000000
000000000000
000000000000
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000000000000
000000000000
000000040000
000000444000
000000000000
000000000000
000000000000
000000800000
000008880000
000000000000
000000000000
```


**Train 4 — input**

```text
0000000000000
0000000020000
0000000000000
0000000000000
0000404000000
0000444000000
0000000000300
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000404000000
0000444000000
0000000000000
0000000000000
0000000000000
0000008080000
0000008880000
0000000000000
0000000000000
```

**Test — input**

```text
0000000000000
0200000000000
0000000000000
0000000000000
0040000000000
0044400000000
0000400000000
0000030000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0040000000000
0044400000000
0000400000000
0000000000000
0000000000000
0000000000000
0000008000000
0000008880000
```

**Written solution**

The vector from the 2 marker to the 3 marker tells you how far to copy the 4-object. Keep the original 4-object, remove the markers, and add a translated copy in color 8 at that offset.

**Reference program**

```python
def rule_h18(g):
    h,w=size(g); out=blank(h,w)
    # preserve original 4 component
    for r in range(h):
        for c in range(w):
            if g[r][c]==4:
                out[r][c]=4
    src=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2][0]
    dst=[(r,c) for r in range(h) for c in range(w) if g[r][c]==3][0]
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    for r in range(h):
        for c in range(w):
            if g[r][c]==4:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=8
    return out
```


### H19 — Component Size Bars

**Difficulty:** hard


**Train pairs:** 4


**Skills:** component sizing, sorting, dynamic output size


**Suggested staged path:** Forget the original layout after measuring. The output is just the component sizes, written as colored bars from largest to smallest.


**Train 1 — input**

```text
0000000000
0220000000
0000000000
0000000000
0440000000
0440000000
0000006600
0000006600
0000006000
0000000000
```

**Train 1 — output**

```text
6666604444022
```


**Train 2 — input**

```text
000000000000
000000033300
000000000000
000000000000
000000000000
000000000000
055500000000
055500000000
000000000000
000000008800
000000000000
000000000000
```

**Train 2 — output**

```text
5555550333088
```


**Train 3 — input**

```text
0000000000000
0110000000000
0110000000000
0000000000000
0000000077000
0000000077000
0000000070000
0000000000000
0000440000000
0000000000000
```

**Train 3 — output**

```text
7777701111044
```


**Train 4 — input**

```text
000000000000
000000000000
002220000000
000000000000
000000000000
000000060000
000000060000
000000666000
099000000000
099000000000
000000000000
```

**Train 4 — output**

```text
66666099990222
```

**Test — input**

```text
0000000000000
0000000003300
0000000000000
0000000000000
0000000000000
0555000000000
0555000000000
0000000000000
0000000880000
0000000880000
0000000800000
0000000000000
```

**Expected test output**

```text
555555088888033
```

**Written solution**

Measure every nonzero component, sort the components from largest to smallest, and output a single row of solid bars whose lengths equal those sizes. Preserve each component's color and separate consecutive bars by one 0.

**Reference program**

```python
def rule_h19(g):
    comps=[(val,cells) for val,cells in components(g) if val!=0]
    # ignore singleton markers? there are none
    comps_sorted=sorted(comps, key=lambda vc: (-len(vc[1]), vc[0]))
    total=sum(len(cells) for val,cells in comps_sorted)+max(0,len(comps_sorted)-1)
    out=blank(1,total)
    c=0
    for i,(val,cells) in enumerate(comps_sorted):
        for _ in range(len(cells)):
            out[0][c]=val
            c+=1
        if i!=len(comps_sorted)-1:
            c+=1
    return out
```


### H20 — Legend-Order Assembly

**Difficulty:** hard


**Train pairs:** 4


**Skills:** legend decoding, component cropping, ordered composition


**Suggested staged path:** Read the legend order in the top row first. Then crop each matching object and pack those crops side by side in that order.


**Train 1 — input**

```text
040020070000
000000000000
004000000000
044400000000
000000007700
000000007700
000000000000
020000000000
020000000000
022000000000
000000000000
000000000000
```

**Train 1 — output**

```text
040020077
444020077
000022000
```


**Train 2 — input**

```text
6003000080000
0000000000000
0660000000000
0066000000000
0000000000000
0000000008800
0000303008800
0000333008000
0000000000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
6600303088
0660333088
0000000080
```


**Train 3 — input**

```text
005000700000
000000000000
000000000000
050000000000
050000002220
055000002220
000000000000
007000000000
077700006600
000000006600
000000000000
000000000000
```

**Train 3 — output**

```text
500070
500777
550000
```


**Train 4 — input**

```text
0800030006000
0000000000000
0000000000000
0808000000000
0888000000600
0000000006660
0000000000000
0000000000000
0033000000000
0003300000000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
80803300060
88800330666
```

**Test — input**

```text
07002000600000
00000000000000
00000000000000
07700000000000
07700000066000
07000000066000
00000000000000
00000000000000
02000000000000
02000000000000
02200000000000
00000000000000
00000000000000
```

**Expected test output**

```text
77020066
77020066
70022000
```

**Written solution**

The nonzero cells in the top row define an order of colors. For each listed color, find the matching component below, crop it to its bounding box, and assemble those crops left-to-right in legend order, separated by one blank column.

**Reference program**

```python
def rule_h20(g):
    h,w=size(g)
    legend=[v for v in g[0] if v!=0]
    parts=[]
    for color in legend:
        comps=[cells for val,cells in components(g, colors={color}) if all(r>0 for r,c in cells)]
        assert len(comps)==1
        cells=comps[0]
        crop=crop_bbox(g,cells)
        parts.append(crop)
    out_h=max(len(p) for p in parts)
    out_w=sum(len(p[0]) for p in parts)+len(parts)-1
    out=blank(out_h,out_w)
    x=0
    for i,p in enumerate(parts):
        ph,pw=size(p)
        for r in range(ph):
            for c in range(pw):
                out[r][x+c]=p[r][c]
        x += pw
        if i != len(parts)-1:
            x += 1
    return out
```


### H21 — Mask Transfer to the Rectangle

**Difficulty:** hard


**Train pairs:** 4


**Skills:** template extraction, mask transfer, bbox alignment


**Suggested staged path:** First understand the 6-shape only as a binary mask inside its own bbox. Then apply that mask inside the 3-rectangle's bbox.


**Train 1 — input**

```text
000000000000
060000000000
060000000000
066000000000
000000000000
000000003300
000000003300
000000003300
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
060000000000
060000000000
066000000000
000000000000
000000008000
000000008000
000000008800
000000000000
000000000000
```


**Train 2 — input**

```text
00000000000
00000000000
00000006600
00000000660
00000000000
00000000000
03330000000
03330000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000006600
00000000660
00000000000
00000000000
08800000000
00880000000
00000000000
00000000000
00000000000
```


**Train 3 — input**

```text
000000000000
000006000000
000066600000
000000000000
000000000000
000000000000
000000000000
000000000000
000000003330
000000003330
000000000000
000000000000
```

**Train 3 — output**

```text
000000000000
000006000000
000066600000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000800
000000008880
000000000000
000000000000
```


**Train 4 — input**

```text
0000000000000
0000000003330
0000000003330
0000000000000
0000000000000
0606000000000
0666000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 4 — output**

```text
0000000000000
0000000008080
0000000008880
0000000000000
0000000000000
0606000000000
0666000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Test — input**

```text
0000000000000
0000000000000
0066000000000
0066000000000
0060000000000
0000000000000
0000000000000
0000000000000
0000000033000
0000000033000
0000000033000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0000000000000
0066000000000
0066000000000
0060000000000
0000000000000
0000000000000
0000000000000
0000000088000
0000000088000
0000000080000
0000000000000
0000000000000
```

**Written solution**

Take the 6-component's occupied cells relative to its bounding box as a mask. Find the solid 3-rectangle with the same bbox size, clear that rectangle, and redraw the mask there using color 8. Keep the original 6-template unchanged.

**Reference program**

```python
def rule_h21(g):
    h,w=size(g); out=clone(g)
    comps6=[cells for val,cells in components(g, colors={6})]
    template=max(comps6, key=len)
    tr0,tr1,tc0,tc1=bbox(template)
    th,tw=tr1-tr0+1,tc1-tc0+1
    rel={(r-tr0,c-tc0) for r,c in template}
    target=None
    for val,cells in components(g, colors={3}):
        r0,r1,c0,c1=bbox(cells)
        if is_solid_rect(cells) and (r1-r0+1, c1-c0+1)==(th,tw):
            target=(r0,r1,c0,c1,cells)
            break
    assert target is not None
    r0,r1,c0,c1,cells=target
    for r,c in cells:
        out[r][c]=0
    for dr,dc in rel:
        out[r0+dr][c0+dc]=8
    return out
```
