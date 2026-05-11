# ARC Additional Puzzle Bank — 21 Puzzles

This bank is designed as a useful extension to your current ARC review set: 7 easy, 7 medium, 7 hard.

A few design choices:

- The easy tier is mostly single-pass local logic.
- The medium tier leans on objects, frames, symmetry, and selective global choice.
- The hard tier requires multi-step state: vectors, extraction, ranking, nesting, or symbolic summaries.
- Every puzzle includes a short staged hint, because your current loop benefits when the search decomposes into factual subgoals.
- Reference programs are given in Python rather than your exact S-expression DSL, because the review packet did not fully specify the executable helper inventory. They are meant to be translated, not treated as opaque black boxes.

Companion files:

- `arc_additional_puzzles_21.py` — all reference solvers + structured data
- `arc_additional_puzzles_21.json` — machine-readable puzzle bank

## Easy (7)

### E1 — Diagonal Corner Completion

**Difficulty:** easy

**Skills:** local 2x2 pattern, diagonal detection, color insertion

**Suggested staged path:** First detect 2×2 windows with two opposite 3s, then fill the missing corners.

**Train 1 — input**

```text
0000000
0030000
0003000
0000000
0000300
0003000
0000000
```

**Train 1 — output**

```text
0000000
0037000
0073000
0000000
0007300
0003700
0000000
```

**Train 2 — input**

```text
00000000
00030000
00300000
00000000
00000300
00003000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00730000
00370000
00000000
00007300
00003700
00000000
00000000
```

**Test — input**

```text
000000000
003000000
000300000
000000000
000003000
000030000
000000300
000003000
000000000
```

**Expected test output**

```text
000000000
003700000
007300000
000000000
000073000
000037000
000007300
000003700
000000000
```

**Written solution**

Look at every 2×2 window. If it has color 3 in one diagonal and 0 in the other diagonal, turn the two empty corner cells into 7. Leave the original 3s alone.

**Reference program**

```python
def rule_e1(g):
    h,w=size(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            block=[[g[r][c],g[r][c+1]],[g[r+1][c],g[r+1][c+1]]]
            # NW-SE diagonal
            if g[r][c]==3 and g[r+1][c+1]==3 and g[r][c+1]==0 and g[r+1][c]==0:
                out[r][c+1]=7
                out[r+1][c]=7
            # NE-SW diagonal
            if g[r][c+1]==3 and g[r+1][c]==3 and g[r][c]==0 and g[r+1][c+1]==0:
                out[r][c]=7
                out[r+1][c+1]=7
    return out
```

### E2 — Diagonal Halo

**Difficulty:** easy

**Skills:** diagonal neighborhood, edge clipping, copy-preserve

**Suggested staged path:** First mark the 3 cells, then add only their four diagonal neighbors.

**Train 1 — input**

```text
000000
003000
000000
000030
000000
300000
```

**Train 1 — output**

```text
070700
003000
070707
000030
070707
300000
```

**Train 2 — input**

```text
0000000
0300000
0000000
0000030
0000000
0003000
0000000
```

**Train 2 — output**

```text
7070000
0300000
7070707
0000030
0070707
0003000
0070700
```

**Test — input**

```text
00000000
00030000
00000000
30000003
00000000
00003000
00000000
00000000
```

**Expected test output**

```text
00707000
00030000
07707070
30000003
07070770
00003000
00070700
00000000
```

**Written solution**

Each 3 acts like a beacon. Keep the 3 itself, and paint every diagonal neighbor of that 3 with 7 if it is inside the grid.

**Reference program**

```python
def rule_e2(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==3:
                for nr,nc in diag_neighbors(r,c,h,w):
                    if out[nr][nc]==0:
                        out[nr][nc]=7
    return out
```

### E3 — One-Gap Completion

**Difficulty:** easy

**Skills:** local line completion, horizontal and vertical symmetry

**Suggested staged path:** First find zeros with 4 on both sides horizontally or vertically, then fill only those zeros.

**Train 1 — input**

```text
0000000
0440400
0000000
0004000
0000000
0004000
0000000
```

**Train 1 — output**

```text
0000000
0444400
0000000
0004000
0004000
0004000
0000000
```

**Train 2 — input**

```text
00000000
00000000
00440400
00000000
00004000
00000000
00004000
00000000
```

**Train 2 — output**

```text
00000000
00000000
00444400
00000000
00004000
00004000
00004000
00000000
```

**Test — input**

```text
000000000
004040400
000000000
000040000
000000000
000040000
000000000
000000000
000000000
```

**Expected test output**

```text
000000000
004444400
000040000
000040000
000040000
000040000
000000000
000000000
000000000
```

**Written solution**

Fill a black cell with 4 whenever it sits exactly between two 4s in a straight line, either horizontally or vertically. Nothing else changes.

**Reference program**

```python
def rule_e3(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: 
                continue
            # horizontal
            if c-1>=0 and c+1<w and g[r][c-1]==4 and g[r][c+1]==4:
                out[r][c]=4
            # vertical
            if r-1>=0 and r+1<h and g[r-1][c]==4 and g[r+1][c]==4:
                out[r][c]=4
    return out
```

### E4 — Bar Caps

**Difficulty:** easy

**Skills:** segment detection, open-end handling, border clipping

**Suggested staged path:** Identify each horizontal run of 6s, then add an 8 on any open end.

**Train 1 — input**

```text
0000000
0066600
0000000
6600000
0006600
0000000
0000000
```

**Train 1 — output**

```text
0000000
0866680
0000000
6680000
0086680
0000000
0000000
```

**Train 2 — input**

```text
00000000
00066600
00000000
00660000
00000066
00000000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00866680
00000000
08668000
00000866
00000000
00000000
00000000
```

**Test — input**

```text
000000000
000066000
000000000
066000000
000006600
000000000
000660000
000000000
000000000
```

**Expected test output**

```text
000000000
000866800
000000000
866800000
000086680
000000000
008668000
000000000
000000000
```

**Written solution**

Every horizontal bar of 6s gets capped by 8s at its open ends. Add one 8 immediately to the left and/or right of the bar if that cell exists and is black.

**Reference program**

```python
def rule_e4(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==6:
                start=c
                while c<w and g[r][c]==6:
                    c+=1
                end=c-1
                if end-start+1>=2:
                    if start-1>=0 and g[r][start-1]==0:
                        out[r][start-1]=8
                    if end+1<w and g[r][end+1]==0:
                        out[r][end+1]=8
            else:
                c+=1
    return out
```

### E5 — Solid Square Recolor

**Difficulty:** easy

**Skills:** 2x2 block detection, full-block recolor

**Suggested staged path:** First find every solid 2×2 block of 5s, then recolor all four cells of each block.

**Train 1 — input**

```text
0000000
0550000
0550000
0000550
0000550
0000000
0000000
```

**Train 1 — output**

```text
0000000
0110000
0110000
0000110
0000110
0000000
0000000
```

**Train 2 — input**

```text
00000000
00055000
00055000
00000000
05500000
05500000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00011000
00011000
00000000
01100000
01100000
00000000
00000000
```

**Test — input**

```text
000000000
005500000
005500000
000000000
000055000
000055000
000000000
000000000
000000000
```

**Expected test output**

```text
000000000
001100000
001100000
000000000
000011000
000011000
000000000
000000000
000000000
```

**Written solution**

Whenever a 2×2 area is completely filled with 5, recolor those four cells to 1. All other cells stay as they are.

**Reference program**

```python
def rule_e5(g):
    h,w=size(g); out=clone(g)
    mark=set()
    for r in range(h-1):
        for c in range(w-1):
            if g[r][c]==g[r+1][c]==g[r][c+1]==g[r+1][c+1]==5:
                mark.update([(r,c),(r+1,c),(r,c+1),(r+1,c+1)])
    for r,c in mark:
        out[r][c]=1
    return out
```

### E6 — Down-Right Shadow

**Difficulty:** easy

**Skills:** translation, in-bounds check, preserve source

**Suggested staged path:** Keep the 2s where they are, then add a 5 one cell down-right from each one.

**Train 1 — input**

```text
200000
000000
000200
000000
020000
000000
```

**Train 1 — output**

```text
200000
050000
000200
000050
020000
005000
```

**Train 2 — input**

```text
0000000
0020000
0000000
0000020
0000000
2000000
0000000
```

**Train 2 — output**

```text
0000000
0020000
0005000
0000020
0000005
2000000
0500000
```

**Test — input**

```text
00000000
02000000
00000000
00002000
00000000
20000000
00000002
00000000
```

**Expected test output**

```text
00000000
02000000
00500000
00002000
00000500
20000000
05000002
00000000
```

**Written solution**

Each 2 casts a one-cell shadow down and to the right. Copy a 5 into that down-right cell when it is inside the grid; keep the original 2s too.

**Reference program**

```python
def rule_e6(g):
    h,w=size(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                nr,nc=r+1,c+1
                if nr<h and nc<w and out[nr][nc]==0:
                    out[nr][nc]=5
    return out
```

### E7 — Vertical Middle Highlight

**Difficulty:** easy

**Skills:** center detection, vertical pattern matching

**Suggested staged path:** Find cells that are the middle of a vertical 4-4-4 triplet and recolor only the middle cell.

**Train 1 — input**

```text
0000000
0004000
0004000
0004000
0400000
0400000
0400000
```

**Train 1 — output**

```text
0000000
0004000
0009000
0004000
0400000
0900000
0400000
```

**Train 2 — input**

```text
00000000
00400000
00400000
00400000
00000040
00000040
00000040
00000000
```

**Train 2 — output**

```text
00000000
00400000
00900000
00400000
00000040
00000090
00000040
00000000
```

**Test — input**

```text
000000000
000040000
000040000
000040000
040000000
040000040
040000040
000000040
000000000
```

**Expected test output**

```text
000000000
000040000
000090000
000040000
040000000
090000040
040000090
000000040
000000000
```

**Written solution**

Whenever three 4s form a vertical triplet, change only the middle 4 into 9. The top and bottom 4 remain unchanged.

**Reference program**

```python
def rule_e7(g):
    h,w=size(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==4 and g[r-1][c]==4 and g[r+1][c]==4:
                out[r][c]=9
    return out
```

## Medium (7)

### M1 — Seeded Frame Fill

**Difficulty:** medium

**Skills:** frame detection, object containment, conditional interior fill

**Suggested staged path:** First detect rectangular 1-frames, then ask which frames contain a 2, then fill only those interiors.

**Train 1 — input**

```text
0000000000
0111100000
0120100000
0100100000
0111100000
0000001110
0000001010
0000001110
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0111100000
0144100000
0144100000
0111100000
0000001110
0000001010
0000001110
0000000000
0000000000
```

**Train 2 — input**

```text
00000000000
00111110000
00100010000
00102010000
00100010000
00111110000
00000000000
00001110000
00001010000
00001110000
00000000000
```

**Train 2 — output**

```text
00000000000
00111110000
00144410000
00144410000
00144410000
00111110000
00000000000
00001110000
00001010000
00001110000
00000000000
```

**Test — input**

```text
000000000000
011110000000
010010111100
012010100100
010010100100
011110111100
000000000000
000111100000
000100100000
000102100000
000111100000
000000000000
```

**Expected test output**

```text
000000000000
011110000000
014410111100
014410100100
014410100100
011110111100
000000000000
000111100000
000144100000
000144100000
000111100000
000000000000
```

**Written solution**

Find every hollow rectangular frame made of 1. If a frame contains at least one 2 in its interior, fill the entire interior of that frame with 4. Frames without a 2 stay unchanged.

**Reference program**

```python
def rule_m1(g):
    h,w=size(g); out=clone(g)
    for r0,r1,c0,c1 in detect_rect_frames(g,1):
        has_seed=False
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]==2:
                    has_seed=True
        if has_seed:
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=4
    return out
```

### M2 — Largest 3-Component

**Difficulty:** medium

**Skills:** connected components, global comparison, selective recolor

**Suggested staged path:** Split the 3s into connected components, pick the largest one, then recolor only that component.

**Train 1 — input**

```text
000000000
033000000
033000330
000000330
000300000
000300000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
088000000
088000330
000000330
000300000
000300000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0003300000
0003300000
0000000000
0333000033
0030000033
0030000000
0030000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0003300000
0003300000
0000000000
0888000033
0080000033
0080000000
0080000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00330000000
00330000330
00000000330
00003330000
00000300000
00000300000
00000000000
33000000000
33000000000
00000000000
```

**Expected test output**

```text
00000000000
00330000000
00330000330
00000000330
00008880000
00000800000
00000800000
00000000000
33000000000
33000000000
00000000000
```

**Written solution**

Among all connected components of color 3, identify the largest one. Recolor that one component to 8 and leave every other component untouched.

**Reference program**

```python
def rule_m2(g):
    out=clone(g)
    comps=connected_components(g,target=3)
    if not comps:
        return out
    _,cells=max(comps,key=lambda x: len(x[1]))
    for r,c in cells:
        out[r][c]=8
    return out
```

### M3 — Straight Bridge

**Difficulty:** medium

**Skills:** endpoint pairing, row/column alignment, path fill

**Suggested staged path:** First pair the two cells of each color, then fill the empty cells between them if they lie on one row or one column.

**Train 1 — input**

```text
000000000
020000020
000000000
000600000
000000000
000600000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
022222220
000000000
000600000
000600000
000600000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0000000000
0030000000
0000000000
0030000000
0000000000
7000000007
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0030000000
0030000000
0030000000
0000000000
7777777777
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000000000
04000000040
00000000000
00000700000
00000000000
00000700000
00000000000
00000000000
00000000000
00000000000
```

**Expected test output**

```text
00000000000
00000000000
04444444440
00000000000
00000700000
00000700000
00000700000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

For any color that appears exactly twice in the grid, if the two cells are aligned in the same row or the same column with only black cells between them, fill the straight path between them with that same color.

**Reference program**

```python
def rule_m3(g):
    h,w=size(g); out=clone(g)
    positions={}
    for r in range(h):
        for c in range(w):
            val=g[r][c]
            if val!=0:
                positions.setdefault(val, []).append((r,c))
    for color,cells in positions.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            cmin,cmax=sorted([c1,c2])
            if all(g[r1][c]==0 or c in [c1,c2] for c in range(cmin,cmax+1)):
                for c in range(cmin,cmax+1):
                    out[r1][c]=color
        elif c1==c2:
            rmin,rmax=sorted([r1,r2])
            if all(g[r][c1]==0 or r in [r1,r2] for r in range(rmin,rmax+1)):
                for r in range(rmin,rmax+1):
                    out[r][c1]=color
    return out
```

### M4 — Frame Stripe from External Marker

**Difficulty:** medium

**Skills:** frame detection, relative position, interior row/column fill

**Suggested staged path:** First detect the 5-frame, then locate the outside 7 marker, then project a stripe into the interior.

**Train 1 — input**

```text
0000000000
0000700000
0005555000
0005005000
0005005000
0005005000
0005555000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0000700000
0005555000
0005305000
0005305000
0005305000
0005555000
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00555500000
00500500000
07500500000
00500500000
00555500000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00555500000
00500500000
07533500000
00500500000
00555500000
00000000000
00000000000
00000000000
00000000000
```

**Test — input**

```text
000000000000
000000700000
000005555000
000005005000
000005005000
000005005000
000005555000
000000000000
000000555500
000000500570
000000500500
000000555500
```

**Expected test output**

```text
000000000000
000000700000
000005555000
000005305000
000005305000
000005305000
000005555000
000000000000
000000555500
000000533570
000000500500
000000555500
```

**Written solution**

Each hollow 5-frame may have a 7 sitting just outside one side. If the 7 is above or below the frame, fill the interior column underneath that marker with 3. If the 7 is left or right of the frame, fill the interior row aligned to that marker with 3.

**Reference program**

```python
def rule_m4(g):
    h,w=size(g); out=clone(g)
    for r0,r1,c0,c1 in detect_rect_frames(g,5):
        # look for one 7 immediately outside frame on any side
        # top markers
        for c in range(c0+1,c1):
            if r0-1>=0 and g[r0-1][c]==7:
                for r in range(r0+1,r1):
                    out[r][c]=3
        for c in range(c0+1,c1):
            if r1+1<h and g[r1+1][c]==7:
                for r in range(r0+1,r1):
                    out[r][c]=3
        for r in range(r0+1,r1):
            if c0-1>=0 and g[r][c0-1]==7:
                for c in range(c0+1,c1):
                    out[r][c]=3
        for r in range(r0+1,r1):
            if c1+1<w and g[r][c1+1]==7:
                for c in range(c0+1,c1):
                    out[r][c]=3
    return out
```

### M5 — Vertical Mirror Divider

**Difficulty:** medium

**Skills:** symmetry, guide-line detection, copy by reflection

**Suggested staged path:** First find the full vertical 9 line, then reflect the nonzero pattern on the left across that line.

**Train 1 — input**

```text
0009000
0209000
0229000
0009000
0039000
0039000
0009000
```

**Train 1 — output**

```text
0009000
0209020
0229220
0009000
0039300
0039300
0009000
```

**Train 2 — input**

```text
000090000
004090000
044090000
004090000
000090000
002290000
000090000
000090000
000090000
```

**Train 2 — output**

```text
000090000
004090400
044090440
004090400
000090000
002292200
000090000
000090000
000090000
```

**Test — input**

```text
0000090000
0030090000
0330090000
0030090000
0000090000
0220090000
0020090000
0000090000
0000090000
0000090000
```

**Expected test output**

```text
0000090000
0030090030
0330090033
0030090030
0000090000
0220090022
0020090020
0000090000
0000090000
0000090000
```

**Written solution**

A full column of 9s is a mirror axis. Copy every nonzero, non-9 cell on the left side to its reflected position on the right side, keeping the same color.

**Reference program**

```python
def rule_m5(g):
    h,w=size(g); out=clone(g)
    # assume one vertical line of 9s in a single column
    cols=[]
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            cols.append(c)
    if not cols:
        return out
    axis=cols[0]
    for r in range(h):
        for c in range(axis):
            val=g[r][c]
            if val!=0 and val!=9:
                mc=axis + (axis - c)
                if 0<=mc<w and out[r][mc]==0:
                    out[r][mc]=val
    return out
```

### M6 — L-Triomino Filter

**Difficulty:** medium

**Skills:** shape classification, connected components, bounding-box test

**Suggested staged path:** Break the 6s into connected components of size 3, then distinguish L-shapes from straight lines.

**Train 1 — input**

```text
000000000
066000000
060000000
000666000
000000000
000000660
000000060
000000000
000000000
```

**Train 1 — output**

```text
000000000
011000000
010000000
000666000
000000000
000000110
000000010
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0000660000
0000060000
0000000000
0066600000
0000000000
0000000066
0000000060
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000110000
0000010000
0000000000
0066600000
0000000000
0000000011
0000000010
0000000000
0000000000
```

**Test — input**

```text
00000000000
06600000000
06000000000
00000000000
00006660000
00000000000
00000000660
00000000060
00000000000
00000000000
00000000000
```

**Expected test output**

```text
00000000000
01100000000
01000000000
00000000000
00006660000
00000000000
00000000110
00000000010
00000000000
00000000000
00000000000
```

**Written solution**

Look at each connected component of color 6 with exactly three cells. If its bounding box is 2×2, then it is an L-shaped triomino, so recolor that whole component to 1. Straight triominoes stay 6.

**Reference program**

```python
def rule_m6(g):
    out=clone(g)
    comps=connected_components(g,target=6)
    for _,cells in comps:
        if len(cells)==3:
            r0,r1,c0,c1=bbox(cells)
            if r1-r0==1 and c1-c0==1:
                for r,c in cells:
                    out[r][c]=1
    return out
```

### M7 — Crop the Largest Object

**Difficulty:** medium

**Skills:** nonzero object detection, largest-object selection, resize via bounding box

**Suggested staged path:** First find all nonzero connected objects, select the largest, then crop the output to that object's bounding box.

**Train 1 — input**

```text
000000000
023000000
022300400
002000400
000000000
000550000
000550000
000000000
000000000
```

**Train 1 — output**

```text
230
223
020
```

**Train 2 — input**

```text
0000000000
0000000000
0006700000
0006600000
0000600000
0000600000
0000000000
0440000000
0440000090
0000000090
```

**Train 2 — output**

```text
67
66
06
06
```

**Test — input**

```text
00000000000
00000000000
00008800000
00008880000
00000800000
00000000000
00000044000
00000044000
00000000000
00000000090
00000000090
```

**Expected test output**

```text
880
888
080
```

**Written solution**

Treat each connected nonzero object as a single object even if it uses multiple colors. Select the largest object, then output only its bounding box, preserving the colors inside that box.

**Reference program**

```python
def rule_m7(g):
    comps=connected_nonzero_components_anycolor(g)
    if not comps:
        return [[]]
    cells=max(comps,key=len)
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]
```

## Hard (7)

### H1 — Translate by Anchor Vector

**Difficulty:** hard

**Skills:** vector computation, object translation, copy with recolor

**Suggested staged path:** First compute the vector from 1 to 2, then apply that vector to the whole 3-object, then recolor the translated copy.

**Train 1 — input**

```text
0000000000
0100000000
0000000000
0003300000
0003000000
0000002000
0000000000
0000000000
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0100000000
0000000000
0003300000
0003000000
0000002000
0000000000
0000000088
0000000080
0000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00000000000
00000000000
00000000000
00002000000
00000000000
00330000000
00300000000
01000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00000000000
00000000000
00000880000
00000800000
00002000000
00000000000
00330000000
00300000000
01000000000
00000000000
```

**Test — input**

```text
000000000000
001000000000
000000330000
000000300000
000000000000
000000000000
000200000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Expected test output**

```text
000000000000
001000000000
000000330000
000000300000
000000000000
000000000000
000200000000
000000088000
000000080000
000000000000
000000000000
000000000000
```

**Written solution**

There is one 1 marker and one 2 marker. Compute the displacement vector from 1 to 2. Copy the entire 3-shaped object by that same displacement, and draw the translated copy in color 8 while keeping the original object and both markers.

**Reference program**

```python
def rule_h1(g):
    h,w=size(g); out=clone(g)
    pos1=[]; pos2=[]; obj=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==1: pos1.append((r,c))
            elif g[r][c]==2: pos2.append((r,c))
            elif g[r][c]==3: obj.append((r,c))
    if len(pos1)==1 and len(pos2)==1:
        dr=pos2[0][0]-pos1[0][0]
        dc=pos2[0][1]-pos1[0][1]
        for r,c in obj:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=8
    return out
```

### H2 — Prototype Stamp from Framed Template

**Difficulty:** hard

**Skills:** template extraction, repeated stamping, recolor on copy

**Suggested staged path:** First extract the 4-pattern from the 1-frame, then stamp that pattern at every 7 seed, recolored to 8.

**Train 1 — input**

```text
01111000000
01441000000
01041070000
01041000000
01111000000
00000000000
00000000700
00000000000
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
01111000000
01441000000
01041088000
01041008000
01111008000
00000000000
00000000880
00000000080
00000000080
00000000000
00000000000
```

**Train 2 — input**

```text
000000000000
000000000000
000111100000
000144100000
000104100000
000104100000
000111100000
000000000700
007000000000
000000000000
000000000000
000000000000
```

**Train 2 — output**

```text
000000000000
000000000000
000111100000
000144100000
000104100000
000104100000
000111100000
000000000880
008800000080
000800000080
000800000000
000000000000
```

**Test — input**

```text
0000001111000
0000001441000
0000001041000
0000001041000
0000001111000
0000000000000
0070000000000
0000000007000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000001111000
0000001441000
0000001041000
0000001041000
0000001111000
0000000000000
0088000000000
0008000008800
0008000000800
0000000000800
0000000000000
0000000000000
0000000000000
```

**Written solution**

A 1-frame contains the prototype made of 4s. Read that interior pattern, then for each 7 seed elsewhere in the grid, stamp a copy of the pattern starting at the seed's position. The copied pattern is recolored from 4 to 8.

**Reference program**

```python
def rule_h2(g):
    h,w=size(g); out=clone(g)
    # find frame of 1 containing at least one 4
    pattern=None
    for r0,r1,c0,c1 in detect_rect_frames(g,1):
        interior=[]
        has4=False
        for r in range(r0+1,r1):
            row=[]
            for c in range(c0+1,c1):
                val=1 if g[r][c]==4 else 0
                row.append(val)
                if g[r][c]==4:
                    has4=True
            interior.append(row)
        if has4:
            pattern=interior
            break
    if pattern is None:
        return out
    ph,pw=len(pattern),len(pattern[0])
    for r in range(h):
        for c in range(w):
            if g[r][c]==7:
                for dr in range(ph):
                    for dc in range(pw):
                        if pattern[dr][dc]:
                            nr,nc=r+dr,c+dc
                            if 0<=nr<h and 0<=nc<w:
                                out[nr][nc]=8
    return out
```

### H3 — Axis-Chooser Reflection

**Difficulty:** hard

**Skills:** axis detection, orientation choice, reflection

**Suggested staged path:** First decide whether the full 9 guide is horizontal or vertical, then reflect the object across the correct axis.

**Train 1 — input**

```text
000090000
002090000
022090000
002090000
000090000
000090000
000090000
000090000
000090000
```

**Train 1 — output**

```text
000090000
002090200
022090220
002090200
000090000
000090000
000090000
000090000
000090000
```

**Train 2 — input**

```text
0000000000
0003300000
0000300000
0000000000
9999999999
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0003300000
0000300000
0000000000
9999999999
0000000000
0000300000
0003300000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000000000
00044000000
00004000000
00000000000
99999999999
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Expected test output**

```text
00000000000
00000000000
00044000000
00004000000
00000000000
99999999999
00000000000
00004000000
00044000000
00000000000
00000000000
```

**Written solution**

A complete line of 9s is the reflection axis. Sometimes it is vertical and sometimes horizontal. Reflect every nonzero, non-9 cell across that axis, keeping the original object and using the same colors.

**Reference program**

```python
def rule_h3(g):
    h,w=size(g); out=clone(g)
    axis_row=None; axis_col=None
    for r in range(h):
        if all(g[r][c]==9 for c in range(w)):
            axis_row=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            axis_col=c; break
    if axis_row is not None:
        for r in range(h):
            if r==axis_row: continue
            mr=axis_row + (axis_row - r)
            if 0<=mr<h:
                for c in range(w):
                    val=g[r][c]
                    if val!=0 and val!=9 and out[mr][c]==0:
                        out[mr][c]=val
    elif axis_col is not None:
        for c in range(w):
            if c==axis_col: continue
            mc=axis_col + (axis_col - c)
            if 0<=mc<w:
                for r in range(h):
                    val=g[r][c]
                    if val!=0 and val!=9 and out[r][mc]==0:
                        out[r][mc]=val
    return out
```

### H4 — Component Count Bar

**Difficulty:** hard

**Skills:** component counting, global summary rendering

**Suggested staged path:** Count the 6-components first; only after you know the count should you draw the summary bar from the 2 marker.

**Train 1 — input**

```text
600000000
000660000
000000000
000006000
000000000
000000000
000000000
000000000
200000000
```

**Train 1 — output**

```text
600000000
000660000
000000000
000006000
000000000
000000000
000000000
000000000
233300000
```

**Train 2 — input**

```text
0000000000
0660006000
0000000000
0000060000
0000000000
0000000000
0066000000
0000000000
0000000000
0200000000
```

**Train 2 — output**

```text
0000000000
0660006000
0000000000
0000060000
0000000000
0000000000
0066000000
0000000000
0000000000
0233330000
```

**Test — input**

```text
00000000000
00600000000
00000066000
00000000000
00006000000
00000000000
60000000000
00000000060
00000000000
00000000000
02000000000
```

**Expected test output**

```text
00000000000
00600000000
00000066000
00000000000
00006000000
00000000000
60000000000
00000000060
00000000000
00000000000
02333330000
```

**Written solution**

Count how many connected components of color 6 appear in the grid. Starting immediately to the right of the single 2 marker, draw that many 3s as a horizontal bar. Everything else stays unchanged.

**Reference program**

```python
def rule_h4(g):
    h,w=size(g); out=clone(g)
    n=len(connected_components(g,target=6))
    marker=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                marker=(r,c)
                break
        if marker: break
    if marker:
        r,c=marker
        for k in range(1,n+1):
            if c+k<w and out[r][c+k]==0:
                out[r][c+k]=3
    return out
```

### H5 — Smallest and Largest Frame Fill

**Difficulty:** hard

**Skills:** frame comparison, ranking by size, different actions by rank

**Suggested staged path:** Find all 4-frames, rank them by interior area, then fill the smallest and largest differently.

**Train 1 — input**

```text
000000000000
044400000000
040400000000
044400000000
000000000000
000044444000
000040004000
000040004000
000044444000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
044400000000
042400000000
044400000000
000000000000
000044444000
000048884000
000048884000
000044444000
000000000000
000000000000
000000000000
```

**Train 2 — input**

```text
0000000000000
0004440000000
0004040000000
0004040000000
0004440000000
0000000000000
0444000000000
0404004444440
0444004000040
0000004000040
0000004444440
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0004440000000
0004040000000
0004040000000
0004440000000
0000000000000
0444000000000
0424004444440
0444004888840
0000004888840
0000004444440
0000000000000
0000000000000
```

**Test — input**

```text
00000000000000
04440000000000
04040000000000
04440000000000
00000000000000
00000444400000
00000400400000
00000444400000
00000000000000
00000004444440
00000004000040
00000004000040
00000004444440
00000000000000
```

**Expected test output**

```text
00000000000000
04440000000000
04240000000000
04440000000000
00000000000000
00000444400000
00000400400000
00000444400000
00000000000000
00000004444440
00000004888840
00000004888840
00000004444440
00000000000000
```

**Written solution**

Among all hollow rectangular frames made of 4, compare their interior areas. Fill the smallest frame's interior with 2 and the largest frame's interior with 8. Any middle-sized frames stay unchanged.

**Reference program**

```python
def rule_h5(g):
    out=clone(g)
    frames=detect_rect_frames(g,4)
    if len(frames)<2:
        return out
    areas=[((r1-r0-1)*(c1-c0-1),(r0,r1,c0,c1)) for r0,r1,c0,c1 in frames]
    min_area,small=min(areas,key=lambda x:x[0])
    max_area,large=max(areas,key=lambda x:x[0])
    for color,frame in [(2,small),(8,large)]:
        r0,r1,c0,c1=frame
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=color
    return out
```

### H6 — Deepest Seeded Frame

**Difficulty:** hard

**Skills:** nested containment, hierarchy resolution, conditional fill

**Suggested staged path:** First find every seeded 1-frame, then discard any seeded frame that contains a smaller seeded frame, then fill only the deepest ones.

**Train 1 — input**

```text
000000000000
011111110000
010000010000
010111010000
010121010000
010111010000
010000010000
011111110000
000000000000
000000000000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
011111110000
010000010000
010111010000
010131010000
010111010000
010000010000
011111110000
000000000000
000000000000
000000000000
000000000000
```

**Train 2 — input**

```text
00000000000
00111110000
00100010000
00102010000
00100010000
00111110000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000000
00111110000
00133310000
00133310000
00133310000
00111110000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Test — input**

```text
0000000000000
0111111100000
0100000100000
0101110100000
0101210100000
0101110100000
0100000100000
0111111100000
0000000000000
0000111100000
0000102100000
0000111100000
0000000000000
```

**Expected test output**

```text
0000000000000
0111111100000
0100000100000
0101110100000
0101310100000
0101110100000
0100000100000
0111111100000
0000000000000
0000111100000
0000133100000
0000111100000
0000000000000
```

**Written solution**

Frames are made of 1s. Some may be nested inside others. Fill the interior of a seeded frame with 3 only if it is the deepest seeded frame in its nesting chain. An outer seeded frame stays unchanged when it contains a smaller seeded frame that is also seeded.

**Reference program**

```python
def rule_h6(g):
    out=clone(g)
    frames=detect_rect_frames(g,1)
    seeded=[]
    for fr in frames:
        r0,r1,c0,c1=fr
        has_seed=any(g[r][c]==2 for r in range(r0+1,r1) for c in range(c0+1,c1))
        if has_seed:
            seeded.append(fr)
    deepest=[]
    for fr in seeded:
        if not any(interior_contains(fr,other) for other in seeded if other!=fr):
            deepest.append(fr)
    for r0,r1,c0,c1 in deepest:
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=3
    return out
```

### H7 — Sorted Component-Size Bars

**Difficulty:** hard

**Skills:** component sizing, sorting, symbolic summary rendering

**Suggested staged path:** Split the 6s into components, measure their sizes, sort the sizes descending, then draw one 3-bar per size.

**Train 1 — input**

```text
66000000000
60000000000
00000000000
00066000000
00000000000
00000600000
00000000000
00000000000
20000000000
00000000000
00000000000
```

**Train 1 — output**

```text
66000000000
60000000000
00000000000
00066000000
00000000000
00000600000
00000000000
00000000000
23330330300
00000000000
00000000000
```

**Train 2 — input**

```text
000000000000
066600000000
006000000000
000000660000
000000660000
000000000000
000000000600
000000000000
000000000000
020000000000
000000000000
000000000000
```

**Train 2 — output**

```text
000000000000
066600000000
006000000000
000000660000
000000660000
000000000000
000000000600
000000000000
000000000000
023333033330
000000000000
000000000000
```

**Test — input**

```text
0000000000000
0066000000000
0060000000000
0000000660000
0000000000000
0000000000600
0000000000600
0000000000000
6600000000000
0000000000000
0200000000000
0000000000000
0000000000000
```

**Expected test output**

```text
0000000000000
0066000000000
0060000000000
0000000660000
0000000000000
0000000000600
0000000000600
0000000000000
6600000000000
0000000000000
0233303303303
0000000000000
0000000000000
```

**Written solution**

Measure the size of every connected component of color 6 and sort those sizes from largest to smallest. Starting immediately to the right of the single 2 marker, draw one bar of 3s for each component size, with one black cell separating consecutive bars.

**Reference program**

```python
def rule_h7(g):
    h,w=size(g); out=clone(g)
    sizes=sorted([len(cells) for _,cells in connected_components(g,target=6)], reverse=True)
    marker=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                marker=(r,c)
                break
        if marker: break
    if marker:
        r,c=marker
        pos=c+1
        for i,s in enumerate(sizes):
            for k in range(s):
                if pos+k<w:
                    out[r][pos+k]=3
            pos += s
            if i != len(sizes)-1:
                pos += 1
    return out
```
