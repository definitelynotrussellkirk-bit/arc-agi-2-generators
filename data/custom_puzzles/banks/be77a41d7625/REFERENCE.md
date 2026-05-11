# 21 More ARC-Style Puzzles

This is the eleventh continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E71–E77, M71–M77, H71–H77**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into local pattern completion, guide-vector motion, legend-driven dispatch, crop-and-rotate extraction, keyed prototype dictionaries, counted orbits, dual-example composition, and path-distance coloring.

**New motifs in this batch**

**`guide_translate(object, marker_a, marker_b)`** — read a displacement vector from two markers and move a whole object by it. This is the core move in **M71**.

**`prototype_dictionary_stamp(dictionary, query_keys)`** — store several anchor-relative patterns and stamp the right one wherever its key appears. This drives **H72**.

**`counted_orbit(anchor, shape, k)`** — rotate an anchor-relative shape through its first k quarter-turns and union the results. This appears in **H73**.

**`frame_library_dispatch(source_frames, target_keys)`** — use keyed source interiors to fill blank target frames. This is central to **H74**.

**`dual_example_compose(geom_pair, color_pair, query)`** — learn geometry from one example pair and recoloring from another, then compose them on a query. This powers **H76**.

**`nearest_seed_path(path, seed_a, seed_b)`** — color a path by graph distance to competing seeds, with a tie color when distances match. This is the main idea in **H77**.

## Easy

### E71 — Complete the missing 2x2 corner

**What it tests:** Recognize a nearly complete 2x2 monochrome square and add the missing corner.

**Staged hint:** Group cells by color first, then ask whether three of them are corners of one 2x2 block.

**Train 1 — input**

```text
00000000
02200000
02000000
00000600
00000660
00000000
00000000
```
**Train 1 — output**

```text
00000000
02200000
02200000
00000660
00000660
00000000
00000000
```
**Train 2 — input**

```text
00000300
00000330
00000000
00000000
08800000
00800000
00000000
00000000
```
**Train 2 — output**

```text
00000330
00000330
00000000
00000000
08800000
08800000
00000000
00000000
```
**Test — input**

```text
000000000
040000000
044000000
000000000
000000700
000007700
000000000
000000000
```
**Test — expected output**

```text
000000000
044000000
044000000
000000000
000007700
000007700
000000000
000000000
```
**Written solution**

For each color, look for exactly three cells that occupy three corners of a 2x2 square. Fill the missing fourth corner with that same color and leave everything else unchanged.

**Reference program (`solve_E71`)**

```python
def solve_E71(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            rs=sorted({r for r,c in cells}); cs=sorted({c for r,c in cells})
            if len(rs)==2 and len(cs)==2 and rs[1]-rs[0]==1 and cs[1]-cs[0]==1:
                for rr in rs:
                    for cc in cs:
                        out[rr][cc]=color
    return out
```

### E72 — Fill the horizontal bridge

**What it tests:** Connect matching row endpoints by filling a blank horizontal interval.

**Staged hint:** Solve row by row. Only care about colors that appear exactly twice in the same row.

**Train 1 — input**

```text
000000000
020020000
000000000
000006006
303000000
000000000
```
**Train 1 — output**

```text
000000000
022220000
000000000
000006666
333000000
000000000
```
**Train 2 — input**

```text
0040004000
0000000000
0000000808
0000000000
0000000000
0500050000
0000000000
```
**Train 2 — output**

```text
0044444000
0000000000
0000000888
0000000000
0000000000
0555550000
0000000000
```
**Test — input**

```text
0000000000
2002000000
0000000000
0000700070
0000000000
0000000000
0060060000
```
**Test — expected output**

```text
0000000000
2222000000
0000000000
0000777770
0000000000
0000000000
0066660000
```
**Written solution**

In any row where the same nonzero color appears exactly twice with only zeros between the two endpoints, fill that whole interval with the color.

**Reference program (`solve_E72`)**

```python
def solve_E72(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        by=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                by[v].append(c)
        for color,cols in by.items():
            if len(cols)==2:
                a,b=min(cols),max(cols)
                if all(g[r][c]==0 for c in range(a+1,b)):
                    for c in range(a,b+1):
                        out[r][c]=color
    return out
```

### E73 — Fill the X-center

**What it tests:** Local diagonal-pattern detection rather than cardinal-neighbor detection.

**Staged hint:** Scan empty cells and check their four diagonal neighbors as a unit.

**Train 1 — input**

```text
00000000
04040000
00000707
04040000
00000707
00000000
00000000
```
**Train 1 — output**

```text
00000000
04040000
00400707
04040070
00000707
00000000
00000000
```
**Train 2 — input**

```text
00000000
00000000
00303000
00000000
00303808
00000000
00000808
00000000
```
**Train 2 — output**

```text
00000000
00000000
00303000
00030000
00303808
00000080
00000808
00000000
```
**Test — input**

```text
000000000
000020200
000000000
000020200
050500000
000000000
050500000
000000000
```
**Test — expected output**

```text
000000000
000020200
000002000
000020200
050500000
005000000
050500000
000000000
```
**Written solution**

Whenever a zero cell has the same nonzero color on all four diagonals around it, fill the center cell with that color.

**Reference program (`solve_E73`)**

```python
def solve_E73(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out
```

### E74 — Complete the missing plus arm

**What it tests:** Detect a same-color plus with exactly one missing cardinal arm.

**Staged hint:** Treat one cell as a possible center and count how many matching up/down/left/right neighbors it already has.

**Train 1 — input**

```text
0000000
0030000
0333000
0000000
0000000
0006660
0000600
```
**Train 1 — output**

```text
0000000
0030000
0333000
0030000
0000600
0006660
0000600
```
**Train 2 — input**

```text
00000000
00000888
00400080
04400000
00400000
00000000
00000000
00000000
```
**Train 2 — output**

```text
00000080
00000888
00400080
04440000
00400000
00000000
00000000
00000000
```
**Test — input**

```text
00000000
07000000
77000000
07002000
00002200
00002000
00000000
00000000
```
**Test — expected output**

```text
00000000
07000000
77700000
07002000
00022200
00002000
00000000
00000000
```
**Written solution**

Find any nonzero center cell that already has three same-color cardinal neighbors. Add the missing fourth arm cell in the remaining cardinal direction.

**Reference program (`solve_E74`)**

```python
def solve_E74(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color==0: continue
            nbrs=[]
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w:
                    nbrs.append((rr,cc,g[rr][cc],dr,dc))
            same=[(rr,cc,dr,dc) for rr,cc,v,dr,dc in nbrs if v==color]
            if len(same)==3:
                dirs={(dr,dc) for rr,cc,dr,dc in same}
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w and (dr,dc) not in dirs and g[rr][cc]==0:
                        out[rr][cc]=color
    return out
```

### E75 — Recolor by column header

**What it tests:** Use a top-row legend to recolor sparse marks below it.

**Staged hint:** The top row is a legend, not part of the body pattern.

**Train 1 — input**

```text
20406080
00100100
10000001
00010000
00100010
00000000
```
**Train 1 — output**

```text
20406080
00400000
20000000
00000000
00400080
00000000
```
**Train 2 — input**

```text
03050700
10100010
00001000
00100100
00000001
01010000
```
**Train 2 — output**

```text
03050700
00000000
00000000
00000700
00000000
03050000
```
**Test — input**

```text
20804060
00100010
10010000
00000101
01000000
00101000
```
**Test — expected output**

```text
20804060
00800060
20000000
00000000
00000000
00804000
```
**Written solution**

Keep the header row. For every nonzero body cell below it, replace its value with the header color at the top of the same column.

**Reference program (`solve_E75`)**

```python
def solve_E75(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=g[0][c]
    return out
```

### E76 — Keep only the smallest component

**What it tests:** Basic connected-component ranking by size.

**Staged hint:** Ignore colors at first and compare component sizes.

**Train 1 — input**

```text
00000000
02200000
02200000
00000000
00000660
03000000
00000000
```
**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00000000
03000000
00000000
```
**Train 2 — input**

```text
88000000
00000400
00000400
00000444
00000000
07700000
07000000
00000000
```
**Train 2 — output**

```text
88000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
```
**Test — input**

```text
000000000
055000000
055000000
050000000
000000000
000000220
004000000
004400000
```
**Test — expected output**

```text
000000000
000000000
000000000
000000000
000000000
000000220
000000000
000000000
```
**Written solution**

Find all nonzero connected components and keep only the smallest one in its original position, blanking out everything else.

**Reference program (`solve_E76`)**

```python
def solve_E76(g):
    comps=components(g)
    if not comps: return clone(g)
    v,cells=min(comps, key=lambda vc:(len(vc[1]), min(vc[1])))
    out=blank(*dims(g),0)
    for r,c in cells:
        out[r][c]=v
    return out
```

### E77 — Fill the diagonal segment

**What it tests:** Detect and complete a blank diagonal line segment between matching endpoints.

**Staged hint:** Look for colors that appear exactly twice and sit on a 45-degree diagonal.

**Train 1 — input**

```text
2000000
0000006
0000000
0002000
0006000
0000000
0000000
```
**Train 1 — output**

```text
2000000
0200006
0020060
0002600
0006000
0000000
0000000
```
**Train 2 — input**

```text
00000008
00000000
03000000
00008000
00000000
00003000
00000000
00000000
```
**Train 2 — output**

```text
00000008
00000080
03000800
00308000
00030000
00003000
00000000
00000000
```
**Test — input**

```text
000000000
050000000
000000070
000000000
000050000
000070000
000000000
000000000
```
**Test — expected output**

```text
000000000
050000000
005000070
000500700
000057000
000070000
000000000
000000000
```
**Written solution**

If two same-color cells lie on a perfect diagonal and the cells between them are blank, fill the whole diagonal segment with that color.

**Reference program (`solve_E77`)**

```python
def solve_E77(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if abs(dr)==abs(dc) and dr!=0:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                ok=True
                rr,cc=r1+sr,c1+sc
                while (rr,cc)!=(r2,c2):
                    if g[rr][cc]!=0:
                        ok=False; break
                    rr+=sr; cc+=sc
                if ok:
                    rr,cc=r1,c1
                    while True:
                        out[rr][cc]=color
                        if (rr,cc)==(r2,c2): break
                        rr+=sr; cc+=sc
    return out
```

## Medium

### M71 — Translate the object by the guide vector

**What it tests:** Read a displacement vector from two guide markers and apply it to an object.

**Staged hint:** Ignore shape details at first. Just find the vector from 8 to 9.

**Train 1 — input**

```text
00000000
08000300
00000330
00900000
00000000
00000000
00000000
00000000
```
**Train 1 — output**

```text
00000000
00000000
00000000
00000030
00000033
00000000
00000000
00000000
```
**Train 2 — input**

```text
00000000
00000000
00000000
00000000
00090000
08004400
00000400
00000000
```
**Train 2 — output**

```text
00000000
00000000
00000000
00000000
00000044
00000004
00000000
00000000
```
**Test — input**

```text
00000000
00000080
00009000
00000000
00000600
00000660
00000000
00000000
```
**Test — expected output**

```text
00000000
00000000
00000000
00000000
00000000
00060000
00066000
00000000
```
**Written solution**

Compute the translation vector from the 8 cell to the 9 cell. Move every other nonzero cell by that same vector, and output only the translated object.

**Reference program (`solve_M71`)**

```python
def solve_M71(g):
    h,w=dims(g)
    pos8=pos9=None
    out=blank(h,w,0)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: pos8=(r,c)
            elif v==9: pos9=(r,c)
    dr=pos9[0]-pos8[0]; dc=pos9[1]-pos8[1]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,8,9):
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out
```

### M72 — Recolor components by size palette

**What it tests:** Combine connected-component size with a legend-driven recoloring rule.

**Staged hint:** The top row is an ordered palette: size 1 uses the first color, size 2 the second, and so on.

**Train 1 — input**

```text
246000000
700000000
000770000
000000700
000000770
000000000
```
**Train 1 — output**

```text
246000000
200000000
000440000
000000600
000000660
000000000
```
**Train 2 — input**

```text
358000000
070000000
000000770
000700000
000770000
000000000
```
**Train 2 — output**

```text
358000000
030000000
000000550
000800000
000880000
000000000
```
**Test — input**

```text
2640000000
0000000070
0000070000
0700077000
0700000000
0000000000
0000000000
```
**Test — expected output**

```text
2640000000
0000000020
0000040000
0600044000
0600000000
0000000000
0000000000
```
**Written solution**

Read the nonzero colors in the top row as an ordered palette. For each component of color 7 below, recolor it according to its size: size 1 gets the first palette color, size 2 gets the second, size 3 gets the third, and so on.

**Reference program (`solve_M72`)**

```python
def solve_M72(g):
    out=clone(g); h,w=dims(g)
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    comps=components(body, ignore=(0,))
    # comps coords in body space
    for v,cells in comps:
        if v!=7: 
            continue
        size=len(cells)
        if 1<=size<=len(palette):
            color=palette[size-1]
            for r,c in cells:
                out[r+1][c]=color
    return out
```

### M73 — Rotate the framed interior by code

**What it tests:** Crop a framed interior and dispatch to a rotation based on a code cell.

**Staged hint:** Separate the two subproblems: extract the inner rectangle first, then apply the code.

**Train 1 — input**

```text
200000
055555
051205
051025
055555
```
**Train 1 — output**

```text
11
02
20
```
**Train 2 — input**

```text
400000
055555
053405
053045
055555
```
**Train 2 — output**

```text
04
40
33
```
**Test — input**

```text
300000
055555
055605
055065
055555
```
**Test — expected output**

```text
605
065
```
**Written solution**

Use the cell at the top-left as a rotation code: 1 means identity, 2 means rotate 90° clockwise, 3 means 180°, and 4 means 270° clockwise. Extract the interior of the 5-frame and output the rotated interior only.

**Reference program (`solve_M73`)**

```python
def solve_M73(g):
    code=g[0][0]
    # find frame color 5 bbox
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    r0,r1,c0,c1=bbox(cells)
    inner=[row[c0+1:c1] for row in g[r0+1:r1]]
    if code==1:
        return inner
    elif code==2:
        return rot90(inner)
    elif code==3:
        return rot180(inner)
    elif code==4:
        return rot270(inner)
    else:
        return inner
```

### M74 — Mask one panel with another

**What it tests:** Cross-panel interaction rather than single-panel local rules.

**Staged hint:** Split the input at the 9 separator column, then keep right-panel cells only where the left panel is nonzero.

**Train 1 — input**

```text
02000912345
22200967812
02000934567
00000981234
00000956781
```
**Train 1 — output**

```text
02000
67800
04000
00000
00000
```
**Train 2 — input**

```text
00100924680
01110913579
00100986420
00100997531
00000911111
```
**Train 2 — output**

```text
00600
03570
00400
00500
00000
```
**Test — input**

```text
10001922222
01010923332
00100923432
01010923332
10001922222
```
**Test — expected output**

```text
20002
03030
00400
03030
20002
```
**Written solution**

Treat the left panel as a binary mask and the right panel as colored content. Output the right panel, but only in positions where the corresponding left-panel cell is nonzero.

**Reference program (`solve_M74`)**

```python
def solve_M74(g):
    parts=split_by_sep_cols(g,9)
    mask,panel=parts
    h,w=dims(mask)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0:
                out[r][c]=panel[r][c]
    return out
```

### M75 — Reflect the shape through the anchor

**What it tests:** Point reflection about an anchor, cell by cell.

**Staged hint:** Think in offsets from the 8 cell, not in absolute positions.

**Train 1 — input**

```text
000000000
000000000
000006000
002000000
002080000
000200000
000000000
000000000
000000000
```
**Train 1 — output**

```text
000000000
000000000
000006000
002002000
002080200
000200200
000600000
000000000
000000000
```
**Train 2 — input**

```text
000000000
000030000
000330000
000008000
000000070
000000000
000000000
000000000
000000000
```
**Train 2 — output**

```text
000000000
000030000
000730000
000008000
000000330
000000300
000000000
000000000
000000000
```
**Test — input**

```text
000000000
000000000
000000000
004000000
044000000
000800000
000006000
000000000
000000000
```
**Test — expected output**

```text
000000000
000000000
000000000
004000000
064000000
000800000
000044000
000040000
000000000
```
**Written solution**

Keep the original pattern. For every nonzero non-anchor cell, reflect it through the 8 cell and paint the reflected cell with the same color.

**Reference program (`solve_M75`)**

```python
def solve_M75(g):
    out=clone(g); h,w=dims(g)
    ar=ac=None
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: ar,ac=r,c
            elif v!=0:
                cells.append((r,c,v))
    for r,c,v in cells:
        rr,cc=2*ar-r, 2*ac-c
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=v
    return out
```

### M76 — Stamp the prototype at every target

**What it tests:** Extract an anchor-relative prototype and replicate it at multiple destinations.

**Staged hint:** The 8 cell defines the local origin of the prototype; the 1 cells are new origins.

**Train 1 — input**

```text
000000000
083000000
033000000
000000000
000000000
000001000
000000000
001000000
000000000
```
**Train 1 — output**

```text
000000000
000000000
000000000
000000000
000000000
000000300
000003300
000300000
003300000
```
**Train 2 — input**

```text
0000000000
0000000400
0000004800
0000000400
0000000000
0010000000
0000000010
0000000000
```
**Train 2 — output**

```text
0000000000
0000000000
0000000000
0000000000
0040000000
0400000040
0040000400
0000000040
```
**Test — input**

```text
0000000000
0000000680
0000000660
0000000000
0000000000
0010000000
0000010000
0000000010
0000000000
```
**Test — expected output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0600000000
0660600000
0000660600
0000000660
```
**Written solution**

Read the nonzero pattern around the 8 cell as a prototype, recording every cell's offset from the anchor. Then stamp that same offset pattern at every target cell of color 1, and output only the stamped copies.

**Reference program (`solve_M76`)**

```python
def solve_M76(g):
    h,w=dims(g)
    anchor=None
    targets=[]
    offsets=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: anchor=(r,c)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==1:
                targets.append((r,c))
            elif v not in (0,8):
                offsets.append((r-anchor[0], c-anchor[1], v))
    out=blank(h,w,0)
    for tr,tc in targets:
        for dr,dc,v in offsets:
            rr,cc=tr+dr, tc+dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out
```

### M77 — Select columns and compress them

**What it tests:** Legend-driven column extraction with output resizing.

**Staged hint:** The top row tells you which columns survive.

**Train 1 — input**

```text
1010010
2345678
1000200
3456000
0000009
```
**Train 1 — output**

```text
247
100
350
000
```
**Train 2 — input**

```text
01011001
12345678
80070060
00011100
22200022
```
**Train 2 — output**

```text
2458
0700
0110
2002
```
**Test — input**

```text
11001010
12345678
90807060
00010001
22233344
50006000
```
**Test — expected output**

```text
1257
9076
0000
2234
5060
```
**Written solution**

Read the top row as a selector: every column with a 1 is kept, every column with a 0 is discarded. Remove the header row and output the remaining rows using only the selected columns in their original order.

**Reference program (`solve_M77`)**

```python
def solve_M77(g):
    cols=[c for c,v in enumerate(g[0]) if v==1]
    return [[row[c] for c in cols] for row in g[1:]]
```

## Hard

### H71 — Infer the panel transform and apply it

**What it tests:** Within-grid transform inference from an example panel pair.

**Staged hint:** Use the first two panels as a tiny teaching example; the third panel is the real query.

**Train 1 — input**

```text
20009002290300
22009002093330
00009000090000
00009000090000
```
**Train 1 — output**

```text
0030
0033
0030
0000
```
**Train 2 — input**

```text
00409040095000
04409044095500
00409040090500
00009000090000
```
**Train 2 — output**

```text
0005
0055
0050
0000
```
**Test — input**

```text
06009000090070
06609000090770
00009066090070
00009006090000
```
**Test — expected output**

```text
0000
0700
0770
0700
```
**Written solution**

Split the input into three panels. Infer which geometric transform turns the first panel into the second one, then apply that same transform to the third panel.

**Reference program (`solve_H71`)**

```python
def solve_H71(g):
    a,b,q=split_by_sep_cols(g,9)
    name=infer_transform(a,b)
    return TRANSFORMS[name](q)
```

### H72 — Stamp shapes from a keyed prototype dictionary

**What it tests:** Build a dictionary of anchor-relative patterns and use it on a query canvas.

**Staged hint:** The top half is a dictionary. Each key color points to one stored local pattern.

**Train 1 — input**

```text
000090000900000
015090600903770
055090260900700
000090600900000
999999999999999
000000000000000
001000000000000
000000000003000
000000020000000
000000000000010
000000000000000
```
**Train 1 — output**

```text
000000000000000
001500000000000
005500060003770
000000026000700
000000060000015
000000000000055
```
**Train 2 — input**

```text
000090000900000
015090600903770
055090260900700
000090600900000
999999999999999
000000000000000
000000003000000
020000000000000
000000000000000
000000000000000
000000000000100
000000000000000
```
**Train 2 — output**

```text
000000000000000
060000003770000
026000000700000
060000000000000
000000000000000
000000000000150
000000000000550
```
**Test — input**

```text
0000900009000000
0150906009037700
0550902609007000
0000906009000000
9999999999999999
0000000000000000
0000000000010000
0003000000000000
0000000000000000
0000000010000000
0000000000000200
0000000000000000
```
**Test — expected output**

```text
0000000000000000
0000000000015000
0003770000055000
0000700000000000
0000000015000600
0000000055000260
0000000000000600
```
**Written solution**

In the top half, each prototype panel defines a key color and the nonzero pattern relative to that key cell. In the bottom half, every key cell asks for its prototype to be stamped there. Output the union of all such stamped patterns.

**Reference program (`solve_H72`)**

```python
def solve_H72(g):
    top,bottom=split_by_sep_rows(g,9)
    protos=split_by_sep_cols(top,9)
    patterns={}
    for p in protos:
        cells=[(r,c,v) for r,row in enumerate(p) for c,v in enumerate(row) if v!=0]
        # key is smallest color among cells? assume one key in {1,2,3}
        key=min(v for r,c,v in cells)
        anchors=[(r,c) for r,c,v in cells if v==key]
        assert len(anchors)==1
        ar,ac=anchors[0]
        patterns[key]=[(r-ar,c-ac,v) for r,c,v in cells]
    out=blank(*dims(bottom),0)
    h,w=dims(bottom)
    for r in range(h):
        for c,v in enumerate(bottom[r]):
            if v in patterns:
                for dr,dc,col in patterns[v]:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=col
    return out
```

### H73 — Paint the counted quarter-turn orbit

**What it tests:** Anchor-relative orbit construction controlled by a header count.

**Staged hint:** Count the 1s in the header first; that tells you how many quarter-turn copies to keep.

**Train 1 — input**

```text
11000000
00000000
00000000
00000200
00009000
00006000
00000000
00000000
```
**Train 1 — output**

```text
00000000
00000000
00000000
00000200
00069000
00006200
00000000
00000000
```
**Train 2 — input**

```text
11100000
00000000
00000000
00005000
00090000
00070000
00000000
00000000
```
**Train 2 — output**

```text
00000000
00000000
00000000
00075000
00790000
00575000
00000000
00000000
```
**Test — input**

```text
111100000
000000000
000000000
000002000
000090600
000000000
000000000
000000000
000000000
```
**Test — expected output**

```text
000000000
000000000
000060000
000202000
006090600
000202000
000060000
000000000
000000000
```
**Written solution**

Treat the 9 cell as a pivot. Count how many 1s appear in the header row, then paint the original nonzero pattern together with its first k-1 quarter-turn rotations around the pivot, where k is that count.

**Reference program (`solve_H73`)**

```python
def solve_H73(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    ar=ac=None
    cells=[]
    for r in range(1,h):
        for c,v in enumerate(g[r]):
            if v==9: ar,ac=r,c
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w,0)
    out[ar][ac]=9
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        for t in range(k):
            rr_off,cc_off=rotate_offset(dr,dc,t)
            rr,cc=ar+rr_off, ac+cc_off
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out
```

### H74 — Fill target frames from a keyed source library

**What it tests:** Dictionary lookup plus structure-preserving insertion into blank targets.

**Staged hint:** Read the top half as a library of framed interiors keyed by label; the bottom half just asks which one to insert.

**Train 1 — input**

```text
00100900200900300
55555955555955555
54005950705958805
54445957775950805
50005950705950885
55555955555955555
99999999999999999
00200900100000000
55555955555000000
50005950005000000
50005950005000000
50005950005000000
55555955555000000
```
**Train 1 — output**

```text
55555955555000000
50705954005000000
57775954445000000
50705950005000000
55555955555000000
```
**Train 2 — input**

```text
00100900200900300
55555955555955555
54005950705958805
54445957775950805
50005950705950885
55555955555955555
99999999999999999
00300900200900100
55555955555955555
50005950005950005
50005950005950005
50005950005950005
55555955555955555
```
**Train 2 — output**

```text
55555955555955555
58805950705954005
50805957775954445
50885950705950005
55555955555955555
```
**Test — input**

```text
00100900200900300
55555955555955555
54005950705958805
54445957775950805
50005950705950885
55555955555955555
99999999999999999
00100900300900100
55555955555955555
50005950005950005
50005950005950005
50005950005950005
55555955555955555
```
**Test — expected output**

```text
55555955555955555
54005958805954005
54445950805954445
50005950885950005
55555955555955555
```
**Written solution**

The top half stores several source frames, each with a key and a filled interior. The bottom half contains blank target frames with keys. For each target, copy in the interior belonging to the matching source key, keeping the target frame shape.

**Reference program (`solve_H74`)**

```python
def solve_H74(g):
    top,bottom=split_by_sep_rows(g,9)
    src_panels=split_by_sep_cols(top,9)
    tgt_panels=split_by_sep_cols(bottom,9)
    patterns={}
    for p in src_panels:
        key=next(v for v in p[0] if v!=0)
        frame=p[1:]
        frame_cells=[(r,c) for r,row in enumerate(frame) for c,v in enumerate(row) if v==5]
        r0,r1,c0,c1=bbox(frame_cells)
        interior=[row[c0+1:c1] for row in frame[r0+1:r1]]
        patterns[key]=interior
    filled=[]
    for p in tgt_panels:
        key=next(v for v in p[0] if v!=0)
        frame=clone(p[1:])
        frame_cells=[(r,c) for r,row in enumerate(frame) for c,v in enumerate(row) if v==5]
        r0,r1,c0,c1=bbox(frame_cells)
        interior=patterns[key]
        # place interior into frame
        for r in range(len(interior)):
            for c in range(len(interior[0])):
                frame[r0+1+r][c0+1+c]=interior[r][c]
        filled.append(frame)
    return join_h(filled, sep=9)
```

### H75 — Infer the binary panel operator

**What it tests:** Infer a binary occupancy operation from an example triple and reuse it.

**Staged hint:** Work in binary occupancy, not in the literal colors of the example inputs.

**Train 1 — input**

```text
020090000902009030090000
022090020902209033090030
000090022900229000090033
000090000900009000090000
```
**Train 1 — output**

```text
0200
0220
0022
0000
```
**Train 2 — input**

```text
044090040902009055090050
004090040900009050090000
000090000900009005090050
000090000900009000090000
```
**Train 2 — output**

```text
0200
0200
0000
0000
```
**Test — input**

```text
066090060900209077090070
006090066900209007090077
000090000900009000090000
000090000900009000090000
```
**Test — expected output**

```text
0020
0020
0000
0000
```
**Written solution**

Use the first three panels to infer the binary operation that combines panel A and panel B into the example output. Then apply that same operation to the last two panels and output the resulting occupancy in color 2.

**Reference program (`solve_H75`)**

```python
def solve_H75(g):
    a,b,o,q1,q2=split_by_sep_cols(g,9)
    op=infer_binop(a,b,o)
    return apply_binop(q1,q2,op)
```

### H76 — Compose a learned transform with a learned recoloring

**What it tests:** Combine two separately learned rules inside one task.

**Staged hint:** One example pair teaches geometry; a different example pair teaches colors.

**Train 1 — input**

```text
2009022923096709203
2209020903290769223
0009000900090009000
```
**Train 1 — output**

```text
066
060
077
```
**Train 2 — input**

```text
0409040945098209455
0449440905490289045
0009000900090009000
```
**Train 2 — output**

```text
220
280
800
```
**Test — input**

```text
0609000967094309677
0669660907690439067
0009060900090009000
```
**Test — expected output**

```text
000
430
443
```
**Written solution**

Use the first two panels to infer a geometric transform. Use the next two panels to infer a color mapping. Apply the geometric transform to the final query panel, then recolor the result with the learned color mapping.

**Reference program (`solve_H76`)**

```python
def solve_H76(g):
    gin,gout,cin,cout,q=split_by_sep_cols(g,9)
    tname=infer_transform(gin,gout)
    cmap=infer_color_map(cin,cout)
    return recolor(TRANSFORMS[tname](q), cmap)
```

### H77 — Color the path by nearest seed

**What it tests:** Nonlocal graph reasoning along a path rather than straight-line distance.

**Staged hint:** Distances are measured along the 1-path, not through empty space.

**Train 1 — input**

```text
0000000
0000000
2111113
0000000
0000000
```
**Train 1 — output**

```text
0000000
0000000
2224333
0000000
0000000
```
**Train 2 — input**

```text
2000000
1100000
0100000
0111110
0000010
0000013
0000000
```
**Train 2 — output**

```text
2000000
2200000
0200000
0223330
0000030
0000033
0000000
```
**Test — input**

```text
000000000
021111100
000000100
000000100
000111100
000100000
000111113
000000000
```
**Test — expected output**

```text
000000000
022222200
000000200
000000200
000334200
000300000
000333333
000000000
```
**Written solution**

Treat the 1-cells together with the seed cells 2 and 3 as a path graph. Recolor each path cell by whichever seed is closer along the path; if the two seeds are equally far away, use color 4.

**Reference program (`solve_H77`)**

```python
def solve_H77(g):
    h,w=dims(g)
    # path cells are 1 plus seed cells 2 and 3 are part of graph
    seeds={}
    graph_cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v in (1,2,3):
                graph_cells.append((r,c))
                if v in (2,3): seeds[v]=(r,c)
    # bfs distances along graph where traversable if cell in 1,2,3
    def bfs(start):
        dist={start:0}
        q=deque([start])
        while q:
            r,c=q.popleft()
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w and (rr,cc) not in dist and g[rr][cc] in (1,2,3):
                    dist[(rr,cc)]=dist[(r,c)]+1
                    q.append((rr,cc))
        return dist
    d2=bfs(seeds[2]); d3=bfs(seeds[3])
    out=blank(h,w,0)
    for r,c in graph_cells:
        if g[r][c]==2: out[r][c]=2
        elif g[r][c]==3: out[r][c]=3
        else:
            a,b=d2[(r,c)],d3[(r,c)]
            out[r][c]=2 if a<b else 3 if b<a else 4
    return out
```
