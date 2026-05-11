# ARC-style Puzzle Bank — 21 more puzzles (set 8)

This eighth bank is organized into 7 easy, 7 medium, and 7 hard puzzles. It leans into line-run reasoning, fold/compare tasks, cyclic shifts, period completion, and constructive header-driven outputs.

This set introduces a new helper primitive:

```text
line_runs(grid, axis="row", colors=None, nonzero=True)
  Return contiguous same-color segments along rows or columns,
  including their start/end positions, lengths, colors, and cells.
```

The reference programs assume the shared helpers in `arc_puzzle_bank_21_set8_reference.py`.


## Index


### Easy

- **S8_E1** — Longest Run Keeper
- **S8_E2** — Midpoints of Odd Runs
- **S8_E3** — Mirror Left Across the Bar
- **S8_E4** — Header Shift Each Row
- **S8_E5** — Alternate Cells of Each Run
- **S8_E6** — Folded Overlap Only
- **S8_E7** — Repeat the Seed Prefix


### Medium

- **S8_M1** — Sort Runs by Length
- **S8_M2** — Long-Run Crossings
- **S8_M3** — Folded XOR Mask
- **S8_M4** — Legend Recolor by Rank
- **S8_M5** — Tile Rectangle from Seed Row
- **S8_M6** — Complete Vertical Periods
- **S8_M7** — Infer the Seed Period


### Hard

- **S8_H1** — Axis-Marker Reflection Completion
- **S8_H2** — Repair the 2D Periodic Hole
- **S8_H3** — Ferrers Diagram from Headers
- **S8_H4** — Query Shape Match by Row Signature
- **S8_H5** — Color Agreement Under Fold
- **S8_H6** — Normalize Cyclic Rows
- **S8_H7** — Fill an Irregular Mask from a 2D Seed

# Easy

## S8_E1 — Longest Run Keeper

**Skills:** line runs, row-wise selection, same-size transform

**Primitive note:** Uses the new line_runs primitive.

**Scaffold:**
- Look at each row separately.
- Find the longest contiguous nonzero same-color run in that row.
- Keep only that run and erase the others.

**Train 1 input**
```text
000000000000
002220044000
330000777700
000555000660
900011110000
000000000000
```
**Train 1 output**
```text
000000000000
002220000000
000000777700
000555000000
000011110000
000000000000
```
**Train 2 input**
```text
000000000000
044000222220
000666600000
770000000555
000033300000
888800000000
```
**Train 2 output**
```text
000000000000
000000222220
000666600000
000000000555
000033300000
888800000000
```
**Test input**
```text
000000000000
022000000777
000444400000
660000222000
000055555000
300000000000
```
**Test output**
```text
000000000000
000000000777
000444400000
000000222000
000055555000
300000000000
```
**Written solution:** Process each row independently. Among that row’s contiguous nonzero runs, keep the unique longest one (using the original color and position) and turn every other cell in the row to black(0). Rows with no nonzero cells stay blank.

**Reference program:**
```python
def solve_S8_E1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        runs=[run for run in line_runs([grid[r]], axis="row") if run['color']!=0]  # but line index 0
        if not runs: 
            continue
        # leftmost unique longest
        best=max(runs,key=lambda run:(run['length'],-run['start']))
        for _,c in best['cells']:
            out[r][c]=best['color']
    return out
```

## S8_E2 — Midpoints of Odd Runs

**Skills:** line runs, midpoint detection, same-size reduction

**Primitive note:** Uses the new line_runs primitive.

**Scaffold:**
- Treat every horizontal nonzero run as one object.
- All runs have odd length.
- Keep only the center cell of each run.

**Train 1 input**
```text
000000000000
022200000555
000000700000
033333000000
000444000777
000000000000
```
**Train 1 output**
```text
000000000000
002000000050
000000700000
000300000000
000040000070
000000000000
```
**Train 2 input**
```text
0000000000000
0011100003330
0000000500000
0777770000000
0002220004440
0000000000000
```
**Train 2 output**
```text
0000000000000
0001000000300
0000000500000
0007000000000
0000200000400
0000000000000
```
**Test input**
```text
000000000000
066600000222
000000900000
055555000000
000333000777
000000000000
```
**Test output**
```text
000000000000
006000000020
000000900000
000500000000
000030000070
000000000000
```
**Written solution:** Scan each row for contiguous same-color runs. Because every run has odd length, each one has a single center cell. Output only those center cells in their original colors and erase the rest.

**Reference program:**
```python
def solve_S8_E2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        assert run['length']%2==1
        mid=(run['start']+run['end'])//2
        out[run['line']][mid]=run['color']
    return out
```

## S8_E3 — Mirror Left Across the Bar

**Skills:** explicit symmetry axis, reflection, same-size transform

**Scaffold:**
- Find the full vertical bar of cyan(8).
- Treat that bar as the mirror axis.
- Copy every nonzero cell on the left to its reflected position on the right.

**Train 1 input**
```text
00000800000
02200800000
00200800000
04440800000
00000800000
00330800000
00000800000
```
**Train 1 output**
```text
00000800000
02200800220
00200800200
04440804440
00000800000
00330803300
00000800000
```
**Train 2 input**
```text
0000008000000
0110008000000
0010008000000
0011108000000
0000008000000
0222008000000
0002008000000
```
**Train 2 output**
```text
0000008000000
0110008000110
0010008000100
0011108011100
0000008000000
0222008002220
0002008002000
```
**Test input**
```text
00000800000
03300800000
00300800000
00333800000
00000800000
04400800000
00400800000
```
**Test output**
```text
00000800000
03300800330
00300800300
00333833300
00000800000
04400800440
00400800400
```
**Written solution:** The cyan(8) column is a visible mirror line. Reflect every nonzero cell from the left half across that bar onto the right half, leaving the original left half and the bar itself unchanged.

**Reference program:**
```python
def solve_S8_E3(grid):
    h,w=dims(grid)
    # find full vertical bar color 8
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=copyg(grid)
    for r in range(h):
        for c in range(b):
            v=grid[r][c]
            if v!=0:
                mc=2*b-c
                if 0<=mc<w and grid[r][mc]==0:
                    out[r][mc]=v
    return out
```

## S8_E4 — Header Shift Each Row

**Skills:** header control, cyclic shift, row-wise transform

**Scaffold:**
- The first cell of each row is a shift amount.
- The rest of that row is the row body.
- Rotate the row body to the right by the header amount.

**Train 1 input**
```text
202200100
100033300
300700000
400044000
```
**Train 1 output**
```text
200022001
100003330
300000700
440000004
```
**Train 2 input**
```text
104440000
200055500
301230000
400000600
```
**Train 2 output**
```text
100444000
200000555
300001230
406000000
```
**Test input**
```text
103330000
200220000
300004400
401200000
```
**Test output**
```text
100333000
200002200
340000004
400000120
```
**Written solution:** Handle each row separately. Read the first cell as the amount of rightward cyclic shift, then rotate the remaining cells of that row by that amount. Keep the header cell itself unchanged.

**Reference program:**
```python
def solve_S8_E4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    body_w=w-1
    for r in range(h):
        k=grid[r][0]
        body=grid[r][1:]
        shift=k%body_w
        out[r][0]=k
        out[r][1:]=body[-shift:]+body[:-shift] if shift else body[:]
    return out
```

## S8_E5 — Alternate Cells of Each Run

**Skills:** line thinning, run indexing, same-size transform

**Primitive note:** Uses the new line_runs primitive.

**Scaffold:**
- Find each horizontal nonzero run.
- Count positions inside the run from left to right.
- Keep positions 1, 3, 5, ... and erase positions 2, 4, 6, ....

**Train 1 input**
```text
000000000000
022220000333
000555550000
077700088880
000000000000
```
**Train 1 output**
```text
000000000000
020200000303
000505050000
070700080800
000000000000
```
**Train 2 input**
```text
0111100006660
0002222000000
0555550003330
0000000000000
```
**Train 2 output**
```text
0101000006060
0002020000000
0505050003030
0000000000000
```
**Test input**
```text
000333330000
066660022220
000000555500
077777700000
```
**Test output**
```text
000303030000
060600020200
000000505000
070707000000
```
**Written solution:** For every contiguous horizontal run, preserve the 1st, 3rd, 5th, and other odd-offset cells within the run, keeping their original colors. Turn the even-offset cells in those runs to black(0).

**Reference program:**
```python
def solve_S8_E5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        for i,(r,c) in enumerate(run['cells']):
            if i%2==0:
                out[r][c]=run['color']
    return out
```

## S8_E6 — Folded Overlap Only

**Skills:** fold comparison, occupancy overlap, same-size mask

**Scaffold:**
- Use the full cyan(8) bar as a fold axis.
- Mirror the left side onto the right side.
- Mark only the right-half cells where both sides were occupied.

**Train 1 input**
```text
00000800000
02200800020
02200800220
00000800000
00300800300
00300800000
00000800000
```
**Train 1 output**
```text
00000000000
00000000020
00000000220
00000000000
00000000200
00000000000
00000000000
```
**Train 2 input**
```text
0000008000000
0110008000010
0011008000110
0000008000000
0044408000440
0004008000040
0000008000000
```
**Train 2 output**
```text
0000000000000
0000000000020
0000000000200
0000000000000
0000000000200
0000000000000
0000000000000
```
**Test input**
```text
00000800000
03300800330
00300800030
00000800000
04440800400
00400800400
00000800000
```
**Test output**
```text
00000000000
00000000220
00000000000
00000000000
00000000200
00000000200
00000000000
```
**Written solution:** Imagine folding the left half over the cyan(8) bar onto the right half. Wherever a left-side nonzero cell lands on an already occupied right-side cell, output red(2) at that right-half location. Everything else becomes black(0).

**Reference program:**
```python
def solve_S8_E6(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                if grid[r][c]!=0 and grid[r][mc]!=0:
                    out[r][mc]=2
    return out
```

## S8_E7 — Repeat the Seed Prefix

**Skills:** period extension, prefix detection, row-wise synthesis

**Scaffold:**
- In each row, read the initial contiguous nonzero block.
- Treat that block as the seed pattern for the row.
- Repeat it across the full row width.

**Train 1 input**
```text
230000000000
457000000000
900000000000
230000000000
```
**Train 1 output**
```text
232323232323
457457457457
999999999999
232323232323
```
**Train 2 input**
```text
1200000000
3450000000
6700000000
8000000000
```
**Train 2 output**
```text
1212121212
3453453453
6767676767
8888888888
```
**Test input**
```text
560000000000
234000000000
700000000000
980000000000
```
**Test output**
```text
565656565656
234234234234
777777777777
989898989898
```
**Written solution:** Each row begins with a nonzero seed pattern followed by zeros. Take that initial nonzero prefix and tile it repeatedly across the entire row width. Do this independently for every row.

**Reference program:**
```python
def solve_S8_E7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        row=grid[r]
        # seed prefix: initial contiguous nonzero block
        c=0
        while c<w and row[c]!=0:
            c+=1
        seed=row[:c]
        out[r]=repeat_to_length(seed,w)
    return out
```

# Medium

## S8_M1 — Sort Runs by Length

**Skills:** line runs, sorting, row reconstruction

**Primitive note:** Uses the new line_runs primitive.

**Scaffold:**
- Split each row into its nonzero runs.
- Sort those runs by decreasing length.
- Repack them from the left with one zero gap between consecutive runs.

**Train 1 input**
```text
0220005555000
0003330007700
0444400099000
0000000000000
```
**Train 1 output**
```text
5555022000000
3330770000000
4444099000000
0000000000000
```
**Train 2 input**
```text
011100004400
000222220330
055000666600
000000000000
```
**Train 2 output**
```text
111044000000
222220330000
666605500000
000000000000
```
**Test input**
```text
022220055000
000777000330
044000666660
011100000000
```
**Test output**
```text
222205500000
777033000000
666660440000
111000000000
```
**Written solution:** For each row, extract all contiguous nonzero runs, sort them by length from longest to shortest, preserve each run’s color and length, and rebuild the row left-aligned with a single black(0) separator between runs.

**Reference program:**
```python
def solve_S8_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        runs=[run for run in line_runs([grid[r]], 'row') if run['color']!=0]
        runs=sorted(runs,key=lambda run:(-run['length'], run['start']))
        c=0
        for idx,run in enumerate(runs):
            for _ in range(run['length']):
                if c<w:
                    out[r][c]=run['color']; c+=1
            if idx!=len(runs)-1 and c<w:
                c+=1  # one zero separator
        # rest zeros
    return out
```

## S8_M2 — Long-Run Crossings

**Skills:** horizontal and vertical runs, cross detection, same-size mask

**Primitive note:** Uses the new line_runs primitive.

**Scaffold:**
- Mark cells that belong to a horizontal nonzero run of length at least 3.
- Also mark cells that belong to a vertical nonzero run of length at least 3.
- Keep only the cells that satisfy both conditions.

**Train 1 input**
```text
00200000000
00200000000
22222000000
00200000300
00200003333
00000000300
00000000300
```
**Train 1 output**
```text
00000000000
00000000000
00800000000
00000000000
00000000800
00000000000
00000000000
```
**Train 2 input**
```text
0000400000
0000400000
0044440000
0000400000
0000400000
0000003333
0000000300
0000000300
0000000300
```
**Train 2 output**
```text
0000000000
0000000000
0000800000
0000000000
0000000000
0000000800
0000000000
0000000000
0000000000
```
**Test input**
```text
00000500000
00000500000
00000500000
00055555000
00000500000
22000000000
22000044440
00000000400
00000000400
00000000400
```
**Test output**
```text
00000000000
00000000000
00000000000
00000800000
00000000000
00000000000
00000000800
00000000000
00000000000
00000000000
```
**Written solution:** A cell matters only if it lies inside both a long horizontal run and a long vertical run. Find those intersections and output cyan(8) at exactly those cells, with black(0) everywhere else.

**Reference program:**
```python
def solve_S8_M2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    hruns={}
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        if run['length']>=3:
            for cell in run['cells']:
                hruns[cell]=run['color']
    vruns=set()
    for run in line_runs(grid,'col'):
        if run['color']==0: continue
        if run['length']>=3:
            for cell in run['cells']:
                vruns.add(cell)
    for cell,color in hruns.items():
        if cell in vruns:
            r,c=cell
            out[r][c]=8
    return out
```

## S8_M3 — Folded XOR Mask

**Skills:** fold comparison, occupancy XOR, same-size mask

**Scaffold:**
- Use the full cyan(8) bar as the fold axis.
- Mirror the left half onto the right half.
- On the right half, mark positions occupied on exactly one side.

**Train 1 input**
```text
00000800000
02200800020
02200800000
00000800220
00300800300
00300800000
00000800000
```
**Train 1 output**
```text
00000000000
00000000700
00000000770
00000000770
00000000000
00000000700
00000000000
```
**Train 2 input**
```text
0000008000000
0110008000010
0011008000000
0000008000110
0044408000440
0004008000000
0000008000000
```
**Train 2 output**
```text
0000000000000
0000000000700
0000000007700
0000000000770
0000000077070
0000000007000
0000000000000
```
**Test input**
```text
00000800000
03300800000
00300800300
00000800330
04440800400
00000800000
```
**Test output**
```text
00000000000
00000000770
00000000000
00000000770
00000007070
00000000000
```
**Written solution:** Fold the left half across the cyan(8) bar onto the right half. Wherever exactly one of the two compared positions is occupied, output orange(7) on the right-half position. Positions with double occupancy or double emptiness become black(0).

**Reference program:**
```python
def solve_S8_M3(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                left = grid[r][c]!=0
                right = grid[r][mc]!=0
                if left ^ right:
                    out[r][mc]=7
    return out
```

## S8_M4 — Legend Recolor by Rank

**Skills:** legend reading, component ordering, recoloring

**Scaffold:**
- Read the nonzero colors from the top row in order.
- Sort the body components from left to right.
- Recolor the 1st component with the 1st legend color, the 2nd with the 2nd, and so on.

**Train 1 input**
```text
2030400000000
0000000000000
0110001100011
0110001100011
0000000000000
```
**Train 1 output**
```text
2030400000000
0000000000000
0220003300044
0220003300044
0000000000000
```
**Train 2 input**
```text
70502030000000
00000000000000
01000100010001
01100110011001
00000000000000
```
**Train 2 output**
```text
70502030000000
00000000000000
07000500020003
07700550022003
00000000000000
```
**Test input**
```text
6040500000000
0000000000000
0011000110000
0011000110000
0000000001100
0000000001100
```
**Test output**
```text
6040500000000
0000000000000
0066000440000
0066000440000
0000000005500
0000000005500
```
**Written solution:** The top row is a palette legend. Ignore zeros, read those colors from left to right, then find the nonzero body components below and order them left to right. Recolor the components using the legend colors in that rank order.

**Reference program:**
```python
def solve_S8_M4(grid):
    h,w=dims(grid)
    # legend colors in top row, contiguous nonzero cells ignoring zeros
    legend=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    out=copyg(grid)
    # find components of color 1 in body coordinates
    comps=[]
    sub=body
    for comp in components(sub,{1},4):
        comps.append(comp)
    comps=sorted(comps,key=lambda comp:min(c for r,c in comp['cells']))
    assert len(comps)<=len(legend)
    for comp,color in zip(comps, legend):
        for r,c in comp['cells']:
            out[r+1][c]=color
    return out
```

## S8_M5 — Tile Rectangle from Seed Row

**Skills:** seed extraction, rectangle fill, periodic tiling

**Scaffold:**
- Read the top row’s initial contiguous nonzero block as the seed.
- Find the rectangular region made of 8s.
- Fill every row of that rectangle by repeating the seed pattern.

**Train 1 input**
```text
234000000000
000000000000
000088888880
000088888880
000088888880
000000000000
```
**Train 1 output**
```text
234000000000
000000000000
000023423420
000023423420
000023423420
000000000000
```
**Train 2 input**
```text
5600000000000
0000000000000
0088888880000
0088888880000
0000000000000
```
**Train 2 output**
```text
5600000000000
0000000000000
0056565650000
0056565650000
0000000000000
```
**Test input**
```text
789000000000
000000000000
000000888880
000000888880
000000888880
000000000000
```
**Test output**
```text
789000000000
000000000000
000000789780
000000789780
000000789780
000000000000
```
**Written solution:** Take the top row’s nonzero prefix as a 1D tile. Locate the rectangular block of cyan(8) cells and replace each row of that rectangle with the seed pattern repeated across the rectangle’s width, leaving the rest of the grid unchanged.

**Reference program:**
```python
def solve_S8_M5(grid):
    h,w=dims(grid)
    # seed row is top row's contiguous nonzero prefix
    c=0
    while c<w and grid[0][c]!=0:
        c+=1
    seed=grid[0][:c]
    out=copyg(grid)
    # find rectangle of 8s in rows >=1
    cells=[(r,c) for r in range(1,h) for c,v in enumerate(grid[r]) if v==8]
    r1,c1,r2,c2=bbox(cells)
    for r in range(r1,r2+1):
        out[r][c1:c2+1]=repeat_to_length(seed,c2-c1+1)
    return out
```

## S8_M6 — Complete Vertical Periods

**Skills:** column-wise period detection, vertical synthesis, same-size transform

**Scaffold:**
- In each column, the top contiguous nonzero cells form the seed.
- Treat that seed as a vertical period for the whole column.
- Repeat it downward to the bottom.

**Train 1 input**
```text
245183
306190
007000
000000
000000
000000
000000
000000
```
**Train 1 output**
```text
245183
346193
247183
345193
246183
347193
245183
346193
```
**Train 2 input**
```text
724618
025038
030010
000000
000000
000000
000000
000000
000000
```
**Train 2 output**
```text
724618
725638
734618
725618
724638
735618
724618
725638
734618
```
**Test input**
```text
952381
407604
002001
000000
000000
000000
000000
000000
```
**Test output**
```text
952381
457684
952381
452681
957384
452681
952381
457684
```
**Written solution:** Work column by column. The top nonzero segment of each column is the column’s period. Repeat that short vertical pattern downward until the whole column is filled.

**Reference program:**
```python
def solve_S8_M6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        r=0
        while r<h and grid[r][c]!=0:
            r+=1
        seed=[grid[i][c] for i in range(r)]
        col=repeat_to_length(seed,h)
        for rr in range(h):
            out[rr][c]=col[rr]
    return out
```

## S8_M7 — Infer the Seed Period

**Skills:** smallest period, row-wise sequence inference, completion

**Primitive note:** Uses the new line_runs primitive for the row parsing, together with smallest-period inference.

**Scaffold:**
- Take the initial contiguous nonzero prefix of each row.
- Find the shortest pattern that repeats to make that prefix.
- Repeat that shortest pattern across the full row.

**Train 1 input**
```text
232323000000
145145145000
777700000000
686868680000
```
**Train 1 output**
```text
232323232323
145145145145
777777777777
686868686868
```
**Train 2 input**
```text
3434343400000
1212120000000
5655655650000
9000000000000
```
**Train 2 output**
```text
3434343434343
1212121212121
5655655655655
9999999999999
```
**Test input**
```text
454545000000
237237237000
666600000000
818181810000
```
**Test output**
```text
454545454545
237237237237
666666666666
818181818181
```
**Written solution:** Each row shows a nonzero prefix that is itself built from a smaller repeating unit. Recover the shortest repeating seed for that prefix, then tile that seed across the full row width.

**Reference program:**
```python
def solve_S8_M7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        row=grid[r]
        k=0
        while k<w and row[k]!=0:
            k+=1
        prefix=row[:k]
        period=smallest_period(prefix)
        out[r]=repeat_to_length(period,w)
    return out
```

# Hard

## S8_H1 — Axis-Marker Reflection Completion

**Skills:** implicit symmetry axis, orientation inference, reflection completion

**Scaffold:**
- Find the two cyan(8) axis markers.
- If they share a column, the axis is vertical; if they share a row, the axis is horizontal.
- Reflect every nonzero non-axis cell across that inferred axis.

**Train 1 input**
```text
00000800000
02200000000
00200000000
00330000000
00030000000
00000000000
00000800000
```
**Train 1 output**
```text
00000800000
02200000220
00200000200
00330003300
00030003000
00000000000
00000800000
```
**Train 2 input**
```text
000440000
001110000
000100000
800000008
000000000
000000000
000000000
```
**Train 2 output**
```text
000440000
001110000
000100000
800000008
000100000
001110000
000440000
```
**Test input**
```text
00000800000
04440000000
00400000000
00400000000
00000000000
00000800000
```
**Test output**
```text
00000800000
04440004440
00400000400
00400000400
00000000000
00000800000
```
**Written solution:** The cyan(8) markers identify a reflection axis without drawing the whole line. Infer whether that axis is vertical or horizontal from the markers, then mirror the existing colored cells across it to complete the reflected figure.

**Reference program:**
```python
def solve_S8_H1(grid):
    h,w=dims(grid)
    axis_cells=[(r,c) for r in range(h) for c,v in enumerate(grid[r]) if v==8]
    cols=sorted(set(c for r,c in axis_cells))
    rows=sorted(set(r for r,c in axis_cells))
    out=copyg(grid)
    if len(cols)==1:  # vertical axis
        b=cols[0]
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v!=0 and v!=8:
                    mc=2*b-c
                    if 0<=mc<w and out[r][mc]==0:
                        out[r][mc]=v
    elif len(rows)==1:  # horizontal axis
        b=rows[0]
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v!=0 and v!=8:
                    mr=2*b-r
                    if 0<=mr<h and out[mr][c]==0:
                        out[mr][c]=v
    else:
        raise AssertionError("axis markers not on one line")
    return out
```

## S8_H2 — Repair the 2D Periodic Hole

**Skills:** 2D periodicity, hole repair, tile inference

**Scaffold:**
- Notice that the nonzero cells come from a small repeating tile.
- Infer the tile’s height and width from the intact parts.
- Use that tile to fill the zero rectangle.

**Train 1 input**
```text
2323232323
4545454545
2320000323
4540000545
2320000323
4545454545
2323232323
4545454545
```
**Train 1 output**
```text
2323232323
4545454545
2323232323
4545454545
2323232323
4545454545
2323232323
4545454545
```
**Train 2 input**
```text
678678678678
123120000023
678670000078
123120000023
678678678678
123123123123
```
**Train 2 output**
```text
678678678678
123123123123
678678678678
123123123123
678678678678
123123123123
```
**Test input**
```text
9494949494
5656565656
7878787878
9400000094
5600000056
7800000078
9400000094
5656565656
7878787878
```
**Test output**
```text
9494949494
5656565656
7878787878
9494949494
5656565656
7878787878
9494949494
5656565656
7878787878
```
**Written solution:** The whole image is a repetition of a small nonzero 2D tile, except for one rectangular hole of zeros. Recover the smallest tile consistent with the intact cells and use it to fill the missing rectangle.

**Reference program:**
```python
def solve_S8_H2(grid):
    h,w=dims(grid)
    tile=infer_tile_from_periodic_hole(grid)
    full=tile2d(tile,h,w)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            if out[r][c]==0:
                out[r][c]=full[r][c]
    return out
```

## S8_H3 — Ferrers Diagram from Headers

**Skills:** header counts, constructive synthesis, partition structure

**Scaffold:**
- Read the left-column numbers as row lengths.
- Read the top-row numbers as column heights.
- Construct the unique left-aligned diagram consistent with those headers.

**Train 1 input**
```text
043221
500000
400000
200000
100000
```
**Train 1 output**
```text
33333
33330
33000
30000
```
**Train 2 input**
```text
0543111
6000000
3000000
3000000
2000000
1000000
```
**Train 2 output**
```text
333333
333000
333000
330000
300000
```
**Test input**
```text
04332
40000
40000
30000
10000
```
**Test output**
```text
3333
3333
3330
3000
```
**Written solution:** Ignore the empty corner. The left header gives how many filled cells each output row should have, and the top header gives the matching column heights. Build the unique left-aligned Ferrers diagram satisfying those counts and color its filled cells green(3).

**Reference program:**
```python
def solve_S8_H3(grid):
    h,w=dims(grid)
    row_lengths=[grid[r][0] for r in range(1,h)]
    col_heights=grid[0][1:]
    # output interior only, color 3
    out=blank(h-1,w-1,0)
    for r,L in enumerate(row_lengths):
        for c in range(min(L,w-1)):
            out[r][c]=3
    # assume headers are consistent; could validate col heights
    return out
```

## S8_H4 — Query Shape Match by Row Signature

**Skills:** shape abstraction, signature matching, bbox crop

**Scaffold:**
- Treat the cyan(8) object as the query.
- Normalize each candidate object by translation.
- Compare their per-row occupied-column signatures and choose the matching one.

**Train 1 input**
```text
00000000000000
08000000200000
08880000222000
00080000002000
00000000000000
00300000044000
03330000444400
00030000000400
00000000000000
```
**Train 1 output**
```text
200
222
002
```
**Train 2 input**
```text
000000000000000
088000000055000
080000000050000
088800000055500
000000000000000
003300000066000
003000000060000
033300000066000
000000000000000
```
**Train 2 output**
```text
550
500
555
```
**Test input**
```text
00000000000000
00800000040000
08880000444000
00080000004000
00000000000000
00022000005500
00002200000550
00022000005500
00000000000000
```
**Test output**
```text
040
444
004
```
**Written solution:** Extract the cyan(8) query shape and describe it by its normalized row signature: which relative columns are occupied in each relative row. Among the other candidate shapes, find the one with the same signature and output only that candidate’s bounding-box crop.

**Reference program:**
```python
def solve_S8_H4(grid):
    # query object color 8. Candidate objects other colors. Output bbox crop of matching candidate.
    comps=components(grid, None,4)
    query=[comp for comp in comps if comp['color']==8]
    assert len(query)==1
    qs=row_signature(query[0]['cells'])
    cands=[comp for comp in comps if comp['color'] not in (0,8)]
    matches=[comp for comp in cands if row_signature(comp['cells'])==qs]
    assert len(matches)==1
    return crop_bbox(grid, matches[0]['cells'])
```

## S8_H5 — Color Agreement Under Fold

**Skills:** fold comparison, color agreement, same-size mask

**Scaffold:**
- Use the full cyan(8) bar as the fold axis.
- Mirror the left side onto the right side.
- Keep only right-half cells where both sides are nonzero and the colors match exactly.

**Train 1 input**
```text
00000800000
02200800220
00200800300
00330803300
00000800000
04400800400
00000800000
```
**Train 1 output**
```text
00000000000
00000000220
00000000000
00000003300
00000000000
00000000400
00000000000
```
**Train 2 input**
```text
0000008000000
0110008000110
0011008000100
0000008000110
0044408000440
0004008000040
0000008000000
```
**Train 2 output**
```text
0000000000000
0000000000110
0000000000100
0000000000000
0000000000400
0000000000000
0000000000000
```
**Test input**
```text
00000800000
03300800330
00300800200
00000800000
04440804440
00400800400
00000800000
```
**Test output**
```text
00000000000
00000000330
00000000000
00000000000
00000004440
00000000400
00000000000
```
**Written solution:** Fold the left half over the cyan(8) bar onto the right half, but compare colors this time rather than mere occupancy. Output only the right-half cells where the mirrored left color and the existing right color are the same nonzero value.

**Reference program:**
```python
def solve_S8_H5(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                lv=grid[r][c]
                rv=grid[r][mc]
                if lv!=0 and lv==rv:
                    out[r][mc]=lv
    return out
```

## S8_H6 — Normalize Cyclic Rows

**Skills:** cyclic equivalence, row alignment, sequence normalization

**Scaffold:**
- The first row is the canonical row.
- Every other row is a cyclic rotation of it.
- Undo each rotation so every row matches the first row exactly.

**Train 1 input**
```text
1234512346
3461234512
5123461234
2346123451
```
**Train 1 output**
```text
1234512346
1234512346
1234512346
1234512346
```
**Train 2 input**
```text
567812349
349567812
812349567
956781234
```
**Train 2 output**
```text
567812349
567812349
567812349
567812349
```
**Test input**
```text
246813579
579246813
135792468
813579246
```
**Test output**
```text
246813579
246813579
246813579
246813579
```
**Written solution:** Use the first row as the target sequence. For every later row, find the cyclic shift that makes it identical to that canonical row, then write the normalized canonical version back out. The output grid has identical rows.

**Reference program:**
```python
def solve_S8_H6(grid):
    h,w=dims(grid)
    canon=grid[0][:]
    out=blank(h,w,0)
    out[0]=canon[:]
    for r in range(1,h):
        row=grid[r]
        # find cyclic shift that matches canon
        found=None
        for s in range(w):
            shifted=row[s:]+row[:s]
            if shifted==canon:
                found=shifted; break
        assert found is not None
        out[r]=found
    return out
```

## S8_H7 — Fill an Irregular Mask from a 2D Seed

**Skills:** 2D tiling, mask fill, bbox-relative phase

**Scaffold:**
- Read the solid nonzero rectangle in the top-left as the seed tile.
- Find the irregular mask made of 8s elsewhere.
- Fill the mask using the seed tile, anchored at the mask’s own top-left corner.

**Train 1 input**
```text
2300000000
4500000000
0000000000
0000088000
0000088000
0000008800
0000008000
0000000000
```
**Train 1 output**
```text
2300000000
4500000000
0000000000
0000023000
0000045000
0000003200
0000005000
0000000000
```
**Train 2 input**
```text
674000000000
123000000000
000000088800
000000888000
000000080000
000000088000
000000000000
```
**Train 2 output**
```text
674000000000
123000000000
000000074600
000000123000
000000070000
000000023000
000000000000
```
**Test input**
```text
9400000000
5600000000
7300000000
0000880000
0000800000
0000880000
0000088000
0000000000
```
**Test output**
```text
9400000000
5600000000
7300000000
0000940000
0000500000
0000730000
0000049000
0000000000
```
**Written solution:** The top-left nonzero block is an explicit 2D seed tile. Elsewhere, an irregular region of cyan(8) cells marks where that tile should be repeated. Use the top-left corner of the mask’s bounding box as the tile origin and fill the mask by repeating the seed tile over it.

**Reference program:**
```python
def solve_S8_H7(grid):
    h,w=dims(grid)
    # detect seed block at top-left: maximal rectangle of nonzero cells from (0,0)
    th=0
    while th<h and all(grid[th][c]!=0 for c in range(0,1)): # at least first col nonzero
        th+=1
        if th<h and grid[th][0]==0:
            break
    # Actually seed occupies contiguous nonzero rows and cols from origin until zero encountered in row0/col0
    tw=0
    while tw<w and grid[0][tw]!=0:
        tw+=1
    th=0
    while th<h and grid[th][0]!=0:
        th+=1
    tile=[row[:tw] for row in grid[:th]]
    # find mask of 8s, use bbox top-left as origin
    cells=[(r,c) for r in range(h) for c,v in enumerate(grid[r]) if v==8]
    r1,c1,r2,c2=bbox(cells)
    out=copyg(grid)
    for r,c in cells:
        out[r][c]=tile[(r-r1)%th][(c-c1)%tw]
    return out
```
