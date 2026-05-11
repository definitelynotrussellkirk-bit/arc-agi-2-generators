# 21 More ARC-Style Puzzles

This is the sixth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E36–E42, M36–M42, H36–H42**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch pushes harder on coordinate transforms, objectwise local frames, metadata-guided recoloring, panel masking, and anchor-based symmetries.

**New motifs in this batch**

**`panel_mask(mask, canvas)`** — treat one panel as a binary shape mask and use it to filter another panel cell-by-cell. This is most explicit in **H41**.

**`anchor_reflect(shape, anchor)`** — use a central anchor as a symmetry point, reflecting both a template’s position and its geometry into the other quadrants. This is the main idea in **H42**.

## Easy

### E36 — Diagonal midpoint fill

**What it tests:** Spot a same-color diagonal pair with exactly one missing cell between the endpoints.

**Staged hint:** Start by grouping cells by color. For each color, only look for endpoint pairs that are two rows and two columns apart, then fill the midpoint.

**Train 1 — input**

```text
2000003
0000000
0020300
0000000
0400000
0000000
0004000
```

**Train 1 — output**

```text
2000003
0200030
0020300
0000000
0400000
0040000
0004000
```

**Train 2 — input**

```text
00000070
05000000
00007000
00050000
00000600
00000000
00000006
00000000
```

**Train 2 — output**

```text
00000070
05000700
00507000
00050000
00000600
00000060
00000006
00000000
```

**Test — input**

```text
000000002
000000000
000000200
040000000
000000000
000400000
700000000
000000000
007000000
```

**Test — expected output**

```text
000000002
000000020
000000200
040000000
004000000
000400000
700000000
070000000
007000000
```

**Written solution**

For each color, find pairs of cells that are exactly two steps apart on a diagonal. When the midpoint between them is 0, fill that midpoint with the same color and leave the rest of the grid unchanged.

**Reference program (`solve_E36`)**

```python
def solve_E36(g: Grid) -> Grid:
    h,w=dims(g)
    out=clone(g)
    # check both diagonals for endpoints exactly 2 apart
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0: continue
            for dr,dc in [(2,2),(2,-2)]:
                r2,c2=r+dr,c+dc
                if 0<=r2<h and 0<=c2<w and g[r2][c2]==col:
                    rm,cm=r+dr//2,c+dc//2
                    if g[rm][cm]==0:
                        out[rm][cm]=col
    return out
```

---

### E37 — Main-diagonal transpose

**What it tests:** Recognize a pure global transpose rather than a local recolor or translation.

**Staged hint:** Ignore color semantics and think only in coordinates. Every cell at (r,c) moves to (c,r).

**Train 1 — input**

```text
000020
003000
000000
400000
000005
060000
```

**Train 1 — output**

```text
000400
000006
030000
000000
200000
000050
```

**Train 2 — input**

```text
0000007
0000000
0200000
0000300
0000000
5000000
0040000
```

**Train 2 — output**

```text
0000050
0020000
0000004
0000000
0003000
0000000
7000000
```

**Test — input**

```text
00000003
00000200
00400000
00000000
00000060
00000000
07000000
00050000
```

**Test — expected output**

```text
00000000
00000070
00400000
00000005
00000000
02000000
00006000
30000000
```

**Written solution**

Transpose the square grid across its main diagonal. Every nonzero cell moves from row r, column c to row c, column r, and zeros move with the same rule.

**Reference program (`solve_E37`)**

```python
def solve_E37(g):
    h,w=dims(g)
    assert h==w
    return [list(row) for row in zip(*g)]
```

---

### E38 — Column header paints markers

**What it tests:** Use a legend row to recolor marker cells below it.

**Staged hint:** Read the first row as a column-wise lookup table. Every 8 in the body should be replaced by the color at the top of its column.

**Train 1 — input**

```text
2034056
0008000
8000000
0080000
0000080
0000008
```

**Train 1 — output**

```text
2034056
0004000
2000000
0030000
0000050
0000006
```

**Train 2 — input**

```text
07204536
08000000
00800000
00000000
00008000
00000800
00000008
```

**Train 2 — output**

```text
07204536
07000000
00200000
00000000
00004000
00000500
00000006
```

**Test — input**

```text
650230478
000800000
080000080
800000008
000080000
000000800
```

**Test — expected output**

```text
650230478
000200000
050000070
600000008
000030000
000000400
```

**Written solution**

Treat the first row as a header. Whenever a body cell is 8, replace it with the header color from the same column; keep the header row and every other cell as they are.

**Reference program (`solve_E38`)**

```python
def solve_E38(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==8:
                out[r][c]=g[0][c]
    return out
```

---

### E39 — Singletons become 2x2 blocks

**What it tests:** Expand isolated seeds into small anchored blocks.

**Staged hint:** Do not search for neighbors or objects. Each nonzero cell independently grows into a 2x2 square anchored at its own position.

**Train 1 — input**

```text
2000000
0000000
0000300
0000000
0500000
0000000
0000000
```

**Train 1 — output**

```text
2200000
2200000
0000330
0000330
0550000
0550000
0000000
```

**Train 2 — input**

```text
00000000
04000000
00000000
00000600
00000000
00700000
00000000
00000000
```

**Train 2 — output**

```text
00000000
04400000
04400000
00000660
00000660
00770000
00770000
00000000
```

**Test — input**

```text
000200000
000000000
500000000
000000000
000000700
000000000
003000000
000000000
000000000
```

**Test — expected output**

```text
000220000
000220000
550000000
550000000
000000770
000000770
003300000
003300000
000000000
```

**Written solution**

Every nonzero cell becomes the top-left corner of a 2x2 block of the same color. The output is the union of all those small blocks.

**Reference program (`solve_E39`)**

```python
def solve_E39(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                v=g[r][c]
                for dr in [0,1]:
                    for dc in [0,1]:
                        if 0<=r+dr<h and 0<=c+dc<w:
                            out[r+dr][c+dc]=v
    return out
```

---

### E40 — Highlight diagonal triple centers

**What it tests:** Detect diagonal length-3 lines and alter only the middle cell.

**Staged hint:** Look for cells with same-color diagonal neighbors on both sides. Only the middle of the diagonal triple changes.

**Train 1 — input**

```text
2000003
0200030
0020300
0000000
0400000
0040000
0004000
```

**Train 1 — output**

```text
2000003
0800080
0020300
0000000
0400000
0080000
0004000
```

**Train 2 — input**

```text
00000600
50006000
05060000
00500000
00007000
00000700
00000070
00000000
```

**Train 2 — output**

```text
00000600
50008000
08060000
00500000
00007000
00000800
00000070
00000000
```

**Test — input**

```text
002000000
000200004
000020040
000000400
000000000
700000000
070000000
007000000
000000000
```

**Test — expected output**

```text
002000000
000800004
000020080
000000400
000000000
700000000
080000000
007000000
000000000
```

**Written solution**

If a cell is the center of a three-cell diagonal line of one color, recolor that center to 8. The diagonal endpoints stay in their original color.

**Reference program (`solve_E40`)**

```python
def solve_E40(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v==0: continue
            if g[r-1][c-1]==v and g[r+1][c+1]==v:
                out[r][c]=8
            if g[r-1][c+1]==v and g[r+1][c-1]==v:
                out[r][c]=8
    return out
```

---

### E41 — Upward gravity by column

**What it tests:** Compress each column independently while preserving within-column order.

**Staged hint:** Solve one column at a time. Collect the nonzero cells from top to bottom, then rewrite them starting at the top.

**Train 1 — input**

```text
000000
005000
000007
300000
004080
200006
```

**Train 1 — output**

```text
305087
204006
000000
000000
000000
000000
```

**Train 2 — input**

```text
0000000
0006000
0400000
0000000
0300000
0005000
0200007
```

**Train 2 — output**

```text
0406007
0305000
0200000
0000000
0000000
0000000
0000000
```

**Test — input**

```text
00000000
00000002
00007000
00400000
00000000
50000000
00300008
20006000
```

**Test — expected output**

```text
50407002
20306008
00000000
00000000
00000000
00000000
00000000
00000000
```

**Written solution**

Apply gravity upward in each column. Gather the nonzero values in top-to-bottom order and pack them at the top of the same column, leaving zeros below.

**Reference program (`solve_E41`)**

```python
def solve_E41(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        vals=[g[r][c] for r in range(h) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[i][c]=v
    return out
```

---

### E42 — Fill exact 3x3 ring centers

**What it tests:** Recognize tiny hollow squares and fill their one-cell hole.

**Staged hint:** Check every 3x3 neighborhood with a 0 center. If all eight surrounding cells are the same nonzero color, fill the center.

**Train 1 — input**

```text
2220000
2020000
2220000
0000000
0000333
0000303
0000333
```

**Train 1 — output**

```text
2220000
2220000
2220000
0000000
0000333
0000333
0000333
```

**Train 2 — input**

```text
00000000
04440000
04040000
04440000
55500000
50500000
55500000
00000000
```

**Train 2 — output**

```text
00000000
04440000
04440000
04440000
55500000
55500000
55500000
00000000
```

**Test — input**

```text
000006660
000006060
000006660
077700000
070700000
077700000
000002220
000002020
000002220
```

**Test — expected output**

```text
000006660
000006660
000006660
077700000
077700000
077700000
000002220
000002220
000002220
```

**Written solution**

Find every exact 3x3 ring: eight border cells of one nonzero color around a 0 center. Fill that center with the ring’s color and leave everything else unchanged.

**Reference program (`solve_E42`)**

```python
def solve_E42(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            border=[]
            for rr in [r-1,r,r+1]:
                for cc in [c-1,c,c+1]:
                    if rr==r and cc==c: 
                        continue
                    border.append(g[rr][cc])
            if border and len(set(border))==1 and border[0]!=0:
                out[r][c]=border[0]
    return out
```

---

## Medium

### M36 — Keep only the median-area object

**What it tests:** Compare object sizes and select the middle one rather than the largest or smallest.

**Staged hint:** First segment the grid into connected components. Compute their areas, sort them, and keep only the object in the middle.

**Train 1 — input**

```text
220000000
000000000
000033000
000033000
000000000
040000000
040400000
044400000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000033000
000033000
000000000
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0500006600
0500006600
0500000600
0000000000
0000000000
0007700000
0007700000
0007700000
0007000000
```

**Train 2 — output**

```text
0000000000
0000006600
0000006600
0000000600
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000002000
00000002000
00000000000
03300000000
03300000000
00300000000
00000044400
00000040400
00000044400
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
00000000000
00000000000
03300000000
03300000000
00300000000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

Split the nonzero cells into connected objects and measure each object's area. Sort the areas and keep only the object whose area is the median; erase the others.

**Reference program (`solve_M36`)**

```python
def solve_M36(g):
    comps=same_color_components(g)
    areas=sorted((len(cells), idx) for idx,(col,cells) in enumerate(comps))
    median_idx=areas[len(areas)//2][1]
    out=blank(*dims(g))
    col,cells=comps[median_idx]
    for r,c in cells:
        out[r][c]=col
    return out
```

---

### M37 — Slide every object to the bottom border

**What it tests:** Translate whole objects as units instead of moving cells independently.

**Staged hint:** Work with bounding boxes, not single cells. Each object keeps its shape and columns; only its vertical offset changes.

**Train 1 — input**

```text
2000000000
2200000040
0000030040
0000330040
0000000000
0000000000
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
0000000040
2000030040
2200330040
```

**Train 2 — input**

```text
00000600000
05500600000
05000660000
00000000070
00000000070
00000000000
00000000000
00000000000
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
00000000000
00000000000
00000600000
05500600070
05000660070
```

**Test — input**

```text
200000000000
200000000040
220003300044
000000300000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
```

**Test — expected output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
200000000000
200003300040
220000300044
```

**Written solution**

For each connected object, shift the whole object downward until its bounding box touches the bottom edge of the grid. Shapes do not rotate or deform.

**Reference program (`solve_M37`)**

```python
def solve_M37(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        r0,r1,c0,c1=bbox(cells)
        shift=h-1-r1
        for r,c in cells:
            out[r+shift][c]=col
    return out
```

---

### M38 — Transpose each object in its own frame

**What it tests:** Apply a local coordinate transform inside each object’s bounding box.

**Staged hint:** Normalize each object into its own top-left–anchored frame, transpose the local coordinates, then place it back.

**Train 1 — input**

```text
0000000000
0022000000
0220000000
0000003000
0000003000
0000003300
0000000000
0000000000
```

**Train 1 — output**

```text
0000000000
0020000000
0220000000
0200003330
0000000030
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
40000000000
44400000000
00000000000
00000000000
00000000500
00000005500
00000000500
00000000000
00000000000
```

**Train 2 — output**

```text
44000000000
04000000000
04000000000
00000000000
00000000500
00000005550
00000000000
00000000000
00000000000
```

**Test — input**

```text
000000000000
006660000000
000600000000
000000000000
000000000000
000000007000
000000007700
000000000700
000000000000
000000000000
```

**Test — expected output**

```text
000000000000
006000000000
006600000000
006000000000
000000000000
000000007700
000000000770
000000000000
000000000000
000000000000
```

**Written solution**

Take each connected object, compute its bounding box, and transpose the occupied cells inside that local frame. Then place the transposed shape back at the same top-left anchor.

**Reference program (`solve_M38`)**

```python
def solve_M38(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        tshape=transpose_shape(shape)
        # dims swap
        for dr,dc in tshape:
            out[r0+dr][c0+dc]=col
    return out
```

---

### M39 — Recolor objects by header column

**What it tests:** Combine object extraction with a symbolic lookup from a legend row.

**Staged hint:** Find each object's leftmost column first. The header color above that column determines the new color for the entire object.

**Train 1 — input**

```text
2345678234
0000000000
1000000000
1100110000
0000100000
0000000100
0000000100
0000000000
```

**Train 1 — output**

```text
2345678234
0000000000
2000000000
2200660000
0000600000
0000000200
0000000200
0000000000
```

**Train 2 — input**

```text
76543287654
01000000000
01100000000
00000000000
00000110000
00000010000
00000000010
00000000010
00000000000
```

**Train 2 — output**

```text
76543287654
06000000000
06600000000
00000000000
00000220000
00000020000
00000000050
00000000050
00000000000
```

**Test — input**

```text
345678234567
000000000000
001100000000
001000000000
000000010000
000000110000
000000000000
000000000010
000000000010
000000000000
```

**Test — expected output**

```text
345678234567
000000000000
005500000000
005000000000
000000020000
000000220000
000000000000
000000000060
000000000060
000000000000
```

**Written solution**

Use the top row as a color legend. For each object in the body, look at the header value above the object's leftmost column and recolor the entire object to that header color.

**Reference program (`solve_M39`)**

```python
def solve_M39(g):
    h,w=dims(g)
    header=g[0]
    comps=same_color_components([row[:] for row in g[1:]])  # relative rows 0..h-2
    out=clone(g)
    for col,cells in comps:
        # cells relative to body
        minc=min(c for r,c in cells)
        newcol=header[minc]
        for r,c in cells:
            out[r+1][c]=newcol
    return out
```

---

### M40 — Crop the rows selected by the left guide

**What it tests:** Interpret boundary markers as a row-selection mask and crop accordingly.

**Staged hint:** The leftmost column is metadata, not part of the payload. Keep only rows whose first cell is 7, then drop that guide column.

**Train 1 — input**

```text
0220300
7044005
0600700
7111020
0003300
7500666
0770000
```

**Train 1 — output**

```text
044005
111020
500666
```

**Train 2 — input**

```text
72030044
00506000
71100200
03030303
70444050
06000600
```

**Train 2 — output**

```text
2030044
1100200
0444050
```

**Test — input**

```text
022203004
705000660
010101010
770020003
044055000
700606060
030030030
```

**Test — expected output**

```text
05000660
70020003
00606060
```

**Written solution**

Read the leftmost column as a selector. Keep the payload rows whose first cell is 7, discard the others, and remove the guide column from the output.

**Reference program (`solve_M40`)**

```python
def solve_M40(g):
    h,w=dims(g)
    rows=[g[r][1:] for r in range(h) if g[r][0]==7]
    return rows
```

---

### M41 — Stamp the smallest object at every marker

**What it tests:** Choose a source object by size and reuse it as a template at multiple targets.

**Staged hint:** Ignore the marker color when looking for the source shape. Find the smallest ordinary object, normalize it, and copy it at every 9.

**Train 1 — input**

```text
0000000900
0200000000
0220000000
0000000000
0000009000
3330000000
3000000000
3000000900
0000000000
0000000000
```

**Train 1 — output**

```text
0000000200
0000000220
0000000000
0000000000
0000002000
0000002200
0000000000
0000000200
0000000220
0000000000
```

**Train 2 — input**

```text
00000000900
00000000000
00040000000
00440000000
00000009000
00000000000
50000000000
50000000900
55500000000
00000000000
00000000000
```

**Train 2 — output**

```text
00000000040
00000000440
00000000000
00000000000
00000000400
00000004400
00000000000
00000000040
00000000440
00000000000
00000000000
```

**Test — input**

```text
000000009000
066000000000
060000000000
000000000000
000000009000
000000000000
000000000000
770000000000
070000009000
077000000000
000000000000
000000000000
```

**Test — expected output**

```text
000000006600
000000006000
000000000000
000000000000
000000006600
000000006000
000000000000
000000000000
000000006600
000000006000
000000000000
000000000000
```

**Written solution**

Among the non-marker objects, identify the smallest connected component. Use its normalized shape as a template and stamp that shape at every 9 marker, producing an output made only of the stamped copies.

**Reference program (`solve_M41`)**

```python
def solve_M41(g):
    h,w=dims(g)
    # smallest non-9 same-color component
    comps=same_color_components(g)
    non9=[(col,cells) for col,cells in comps if col!=9]
    col,cells=min(non9, key=lambda x: len(x[1]))
    shape,(hh,ww),_ = normalize(cells)
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in shape:
            out[mr+dr][mc+dc]=col
    return out
```

---

### M42 — Anti-diagonal reflect each object in its frame

**What it tests:** Apply a less common local symmetry, not just a transpose or horizontal mirror.

**Staged hint:** Normalize each object in a square bounding box. Reflect local coordinates across the anti-diagonal, then place the result back.

**Train 1 — input**

```text
00000000000
02220000000
02000000000
02000000000
00000000300
00000003300
00000000330
00000000000
00000000000
```

**Train 1 — output**

```text
00000000000
00020000000
00020000000
02220000000
00000003000
00000003330
00000000300
00000000000
00000000000
```

**Train 2 — input**

```text
004000000000
044000000000
440000000000
000000000000
000000000000
000000000550
000000005500
000000005000
000000000000
000000000000
```

**Train 2 — output**

```text
044000000000
440000000000
400000000000
000000000000
000000000000
000000000050
000000000550
000000005500
000000000000
000000000000
```

**Test — input**

```text
0000000000000
0066000000000
0006000000000
0006600000000
0000000000000
0000000000000
0000000007770
0000000007000
0000000007000
0000000000000
0000000000000
```

**Test — expected output**

```text
0000000000000
0060000000000
0066600000000
0000600000000
0000000000000
0000000000000
0000000000070
0000000000070
0000000007770
0000000000000
0000000000000
```

**Written solution**

For each object, look inside its square local frame and reflect the occupied cells across the anti-diagonal. Keep each reflected object at the same top-left anchor in the grid.

**Reference program (`solve_M42`)**

```python
def solve_M42(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        assert hh==ww
        ashape=anti_diag_reflect(shape, hh)
        for dr,dc in ashape:
            out[r0+dr][c0+dc]=col
    return out
```

---

## Hard

### H36 — Quadrant analogy — hole filling

**What it tests:** Read a panel analogy and transfer the same transform to a different quadrant.

**Staged hint:** Use the top-left and top-right panels to infer the rule. Once you see that holes are being filled, apply that transform to the bottom-left panel and write the answer in the bottom-right panel.

**Train 1 — input**

```text
222292222
200292222
200292222
222292222
999999999
000090000
033390000
030390000
033390000
```

**Train 1 — output**

```text
222292222
200292222
200292222
222292222
999999999
000090000
033390333
030390333
033390333
```

**Train 2 — input**

```text
00000900000
44444944444
40004944444
44444944444
00000900000
99999999999
05555900000
05005900000
05005900000
05555900000
00000900000
```

**Train 2 — output**

```text
00000900000
44444944444
40004944444
44444944444
00000900000
99999999999
05555905555
05005905555
05005905555
05555905555
00000900000
```

**Test — input**

```text
00000900000
02220902220
02020902220
02220902220
00000900000
99999999999
06660900000
06060900000
06060900000
06060900000
06660900000
```

**Test — expected output**

```text
00000900000
02220902220
02020902220
02220902220
00000900000
99999999999
06660906660
06060906660
06060906660
06060906660
06660906660
```

**Written solution**

The top row of quadrants shows the analogy: the hollow object in the top-left becomes the hole-filled solid object in the top-right. Apply the same hole-filling transform to the object in the bottom-left quadrant and place the result in the bottom-right quadrant, leaving the rest unchanged.

**Reference program (`solve_H36`)**

```python
def solve_H36(g):
    h,w=dims(g)
    gr=gc=None
    for r in range(h):
        if all(v==9 for v in g[r]):
            gr=r; break
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            gc=c; break
    out=clone(g)
    r0,r1,c0,c1=gr+1,h,0,gc
    # extract BL subgrid
    sub=[[g[r0+rr][c0+cc] if g[r0+rr][c0+cc]!=9 else 0 for cc in range(c1-c0)] for rr in range(r1-r0)]
    comps=same_color_components(sub)
    if comps:
        col,cells=comps[0]
        shape,(hh,ww),(sr,sc)=normalize(cells)
        filled=fill_holes_shape(shape,hh,ww)
        # place in BR with same relative top-left
        br_start_r, br_start_c = gr+1, gc+1
        for dr,dc in filled:
            out[br_start_r+sr+dr][br_start_c+sc+dc]=col
    return out
```

---

### H37 — Permute row blocks by the side header

**What it tests:** Read a compact permutation code and reorder larger structural blocks accordingly.

**Staged hint:** Treat the first column as an ordering instruction, not image content. Split the body into equal-height row blocks and reorder them in the requested sequence.

**Train 1 — input**

```text
32200000
10220000
20022000
00003300
00033000
00330000
04444000
00400400
00044440
```

**Train 1 — output**

```text
4444000
0400400
0044440
2200000
0220000
0022000
0003300
0033000
0330000
```

**Train 2 — input**

```text
250000000
355000000
150500000
000066000
000660000
006600000
000000777
000007007
000077770
```

**Train 2 — output**

```text
00066000
00660000
06600000
00000777
00007007
00077770
50000000
55000000
50500000
```

**Test — input**

```text
12202000
30220200
20022020
00003300
00030300
00330030
04440000
04044000
00444400
```

**Test — expected output**

```text
2202000
0220200
0022020
4440000
4044000
0444400
0003300
0030300
0330030
```

**Written solution**

The first column encodes a permutation of the horizontal blocks. Divide the remaining body into three equal-height row blocks and output them top-to-bottom in the order specified by the side header, omitting the header column.

**Reference program (`solve_H37`)**

```python
def solve_H37(g):
    h,w=dims(g)
    bh=h//3
    perm=[g[i][0] for i in range(3)]
    blocks=[ [row[1:] for row in g[i*bh:(i+1)*bh]] for i in range(3)]
    out=[]
    for p in perm:
        out.extend([row[:] for row in blocks[p-1]])
    return out
```

---

### H38 — Arrow-selected rotation stamp

**What it tests:** Combine symbolic control, local rotation, and multi-target stamping.

**Staged hint:** Find the one ordinary object that serves as the template. Decode the arrow value into a rotation, rotate the template once, and stamp that rotated shape at every 9.

**Train 1 — input**

```text
20000009000
07000000000
07770000000
00000000000
00000090000
00000000000
00000000000
00000009000
00000000000
00000000000
00000000000
```

**Train 1 — output**

```text
00000007700
00000007000
00000007000
00000000000
00000077000
00000070000
00000070000
00000007700
00000007000
00000007000
00000000000
```

**Train 2 — input**

```text
300000009000
000000000000
006000000000
066000000000
006000000000
000000090000
000000000000
000000000000
000000009000
000000000000
000000000000
000000000000
```

**Train 2 — output**

```text
000000006000
000000006600
000000006000
000000000000
000000000000
000000060000
000000066000
000000060000
000000006000
000000006600
000000006000
000000000000
```

**Test — input**

```text
4000000009000
0055000000000
0005000000000
0005000000000
0000000000000
0000000090000
0000000000000
0000000000000
0000000000000
0000000009000
0000000000000
0000000000000
0000000000000
```

**Test — expected output**

```text
0000000005550
0000000005000
0000000000000
0000000000000
0000000000000
0000000055500
0000000050000
0000000000000
0000000000000
0000000005550
0000000005000
0000000000000
0000000000000
```

**Written solution**

Interpret the single arrow-colored cell as a rotation code: 1 means no rotation, 2 means rotate 90° clockwise, 3 means 180°, and 4 means 270°. Extract the template object, rotate it accordingly, and stamp the rotated template at every 9 marker; the output contains only those stamped copies.

**Reference program (`solve_H38`)**

```python
def solve_H38(g):
    h,w=dims(g)
    arrow=g[0][0]
    comps=same_color_components(g)
    # template = largest component with color not 0,9,arrow and area>1
    candidates=[(col,cells) for col,cells in comps if col not in (0,9,arrow) and len(cells)>1]
    col,cells=max(candidates,key=lambda x: len(x[1]))
    shape,(hh,ww),_ = normalize(cells)
    rot_map={1:0,2:1,3:2,4:3}
    rshape,nh,nw=rotate_shape(shape,hh,ww,rot_map[arrow])
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc in rshape:
            out[mr+dr][mc+dc]=col
    return out
```

---

### H39 — Rotate each object by its color code

**What it tests:** Apply different local transforms to different objects based on symbolic attributes.

**Staged hint:** Do not use one global transform. Each object's color tells you how many quarter-turns to apply inside that object's own frame.

**Train 1 — input**

```text
111000200000
100002200000
100000220000
000000000000
000000000000
000300004400
003300044000
033000040000
000000000000
000000000000
```

**Train 1 — output**

```text
111000200000
100002220000
100002000000
000000000000
000000000000
003300040000
033000044000
030000004400
000000000000
000000000000
```

**Train 2 — input**

```text
0000000000000
0110002220000
0010002000000
0011002000000
0000000000000
0000000000000
0003000000400
0033000004400
0003300044000
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000000
0110002220000
0010000020000
0011000020000
0000000000000
0000000000000
0033000044000
0003300004400
0003000000400
0000000000000
0000000000000
```

**Test — input**

```text
00000000000000
00100000020000
01100000220000
00110002200000
00000000000000
00000000000000
00000000000000
00033000044000
00330000004000
00300000004400
00000000000000
00000000000000
```

**Test — expected output**

```text
00000000000000
00100002000000
01100002200000
00110000220000
00000000000000
00000000000000
00000000000000
00003000000400
00033000044400
00330000040000
00000000000000
00000000000000
```

**Written solution**

Each object's color is an instruction: color 1 stays as is, color 2 rotates 90° clockwise, color 3 rotates 180°, and color 4 rotates 270°. Apply the appropriate rotation to each object inside its own local frame.

**Reference program (`solve_H39`)**

```python
def solve_H39(g):
    h,w=dims(g)
    comps=same_color_components(g)
    out=blank(h,w)
    rot_map={1:0,2:1,3:2,4:3}
    for col,cells in comps:
        shape,(hh,ww),(r0,c0)=normalize(cells)
        assert hh==ww
        rshape,nh,nw=rotate_shape(shape,hh,ww,rot_map[col])
        for dr,dc in rshape:
            out[r0+dr][c0+dc]=col
    return out
```

---

### H40 — Legend-driven recolored mirror stamp

**What it tests:** Fuse three operations: extract a multicolor template, mirror it, and recolor it by a legend before stamping.

**Staged hint:** Separate the problem into stages: get the template, mirror it left-right, apply the two-color legend mapping, then stamp the transformed copy at every marker.

**Train 1 — input**

```text
230000009000
000000000000
056000000000
056500000000
000000090000
000000000000
000000000000
000000009000
000000000000
000000000000
```

**Train 1 — output**

```text
000000000320
000000002320
000000000000
000000000000
000000003200
000000023200
000000000000
000000000320
000000002320
000000000000
```

**Train 2 — input**

```text
4700000009000
0000000000000
0055000000000
0006600000000
0050000000000
0000000090000
0000000000000
0000000000000
0000000009000
0000000000000
0000000000000
```

**Train 2 — output**

```text
0000000000440
0000000007700
0000000000000
0000000000000
0000000000000
0000000004400
0000000077000
0000000000000
0000000000440
0000000007700
0000000000000
```

**Test — input**

```text
38000000009000
00000000000000
00060000000000
00565000000000
00006000000000
00000000090000
00000000000000
00000000000000
00000000000000
00000000009000
00000000000000
00000000000000
```

**Test — expected output**

```text
00000000000800
00000000003830
00000000008000
00000000000000
00000000000000
00000000008000
00000000038300
00000000080000
00000000000000
00000000000800
00000000003830
00000000008000
```

**Written solution**

Use the top-row legend to remap the template colors: 5 becomes the first legend color and 6 becomes the second. Mirror the template horizontally, then stamp that mirrored-and-recolored template at every 9 marker; output only the stamped copies.

**Reference program (`solve_H40`)**

```python
def solve_H40(g):
    h,w=dims(g)
    a,b=g[0][0],g[0][1]
    # template = largest nz component excluding 9 and header row colors in row0? We ignore row0 entirely for extraction except markers maybe none.
    body=[[g[r][c] if r>0 else 0 for c in range(w)] for r in range(h)]
    comps=nz_components(body, ignore_colors={9})
    # choose largest comp that is not marker singletons?
    template=max(comps, key=len)
    r0,r1,c0,c1=bbox(template)
    # capture multicolor bbox from original g
    bbox_cells=[]
    shape_positions=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if g[r][c]!=0 and g[r][c]!=9:
                bbox_cells.append((r-r0,c-c0,g[r][c]))
                shape_positions.append((r-r0,c-c0))
    hh,ww=r1-r0+1,c1-c0+1
    # mirror horizontally and recolor 5->a, 6->b
    markers=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    out=blank(h,w)
    for mr,mc in markers:
        for dr,dc,v in bbox_cells:
            ndc=ww-1-dc
            nv=a if v==5 else b if v==6 else v
            out[mr+dr][mc+ndc]=nv
    return out
```

---

### H41 — Use the left panel as a mask on the right panel

**What it tests:** Transfer a binary shape from one panel as a boolean mask over a separate colored canvas.

**Staged hint:** Ignore the actual mask color and treat the left panel as 1s and 0s. Then keep only the matching cells from the right panel in the same coordinates.

**Train 1 — input**

```text
22000934567
02000982345
02200967823
00200945678
00200923456
```

**Train 1 — output**

```text
34000
02000
07800
00600
00400
```

**Train 2 — input**

```text
0200009234567
2220009567823
0020009823456
0020009456782
0200009782345
0200009345678
```

**Train 2 — output**

```text
030000
567000
003000
006000
080000
040000
```

**Test — input**

```text
2200009234567
0200009345678
0220009456782
0002009567823
0002009678234
0000209782345
```

**Test — expected output**

```text
230000
040000
056000
000800
000200
000040
```

**Written solution**

The left panel defines a binary mask: nonzero means keep, zero means remove. Apply that mask to the right panel cell-by-cell and output only the masked right panel, without the separator or the original mask panel.

**Reference program (`solve_H41`)**

```python
def solve_H41(g):
    h,w=dims(g)
    # separator col all 9
    sep=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            sep=c; break
    pw=sep
    out=blank(h,pw)
    for r in range(h):
        for c in range(pw):
            if g[r][c]!=0 and g[r][sep+1+c]!=0:
                out[r][c]=g[r][sep+1+c]
    return out
```

---

### H42 — Four-way reflected stamping around the anchor

**What it tests:** Normalize a source shape relative to an anchor and generate reflected companions in the other quadrants.

**Staged hint:** Use the anchor as the symmetry center. Keep the original template where it is, then reflect both its position and its shape to create the other three copies.

**Train 1 — input**

```text
0000000000000
0000000000000
0070000000000
0077000000000
0007000000000
0000000000000
0000009000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
0000000000000
0000000000000
0070000000700
0077000007700
0007000007000
0000000000000
0000000000000
0000000000000
0007000007000
0077000007700
0070000000700
0000000000000
0000000000000
```

**Train 2 — input**

```text
000000000000000
000000000000000
000660000000000
000060000000000
000060000000000
000000000000000
000000000000000
000000090000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 2 — output**

```text
000000000000000
000000000000000
000660000066000
000060000060000
000060000060000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000060000060000
000060000060000
000660000066000
000000000000000
000000000000000
```

**Test — input**

```text
000000000000000
000000000000000
000500000000000
005550000000000
000050000000000
000000000000000
000000000000000
000000090000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Test — expected output**

```text
000000000000000
000000000000000
000500000005000
005550000055500
000050000050000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000050000050000
005550000055500
000500000005000
000000000000000
000000000000000
```

**Written solution**

Treat the single 9 as a central anchor. The given template is one quadrant of a four-way arrangement: keep the original, add a horizontally reflected copy across the anchor’s vertical axis, a vertically reflected copy across its horizontal axis, and a 180° copy in the opposite quadrant.

**Reference program (`solve_H42`)**

```python
def solve_H42(g):
    h,w=dims(g)
    # anchor 9 single cell
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    assert len(anchors)==1
    ar,ac=anchors[0]
    comps=same_color_components(g)
    # template is largest non9 component
    col,cells=max([(col,cells) for col,cells in comps if col!=9], key=lambda x: len(x[1]))
    shape,(hh,ww),(r0,c0)=normalize(cells)
    out=blank(h,w)
    # original copy
    placements=[]
    # reflect bbox top-left across anchor point axes
    def refl_h(c0): # across vertical line x=ac
        return 2*ac - c0 - ww + 1
    def refl_v(r0):
        return 2*ar - r0 - hh + 1
    placements.append((r0,c0,shape))
    placements.append((r0,refl_h(c0),hmirror_shape(shape,hh,ww)))
    placements.append((refl_v(r0),c0,vmirror_shape(shape,hh,ww)))
    placements.append((refl_v(r0),refl_h(c0),rotate_shape(shape,hh,ww,2)[0]))
    for pr,pc,pshape in placements:
        for dr,dc in pshape:
            out[pr+dr][pc+dc]=col
    return out
```

---
