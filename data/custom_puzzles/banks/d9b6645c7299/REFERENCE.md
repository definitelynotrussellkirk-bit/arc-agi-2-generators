# 21 Additional ARC-Style Puzzles

This bank is **additional** to the 3 diagnostic puzzles already proposed earlier.
Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output (author key)
- a written solution
- a reference program solution

The difficulty tiers are intentionally scaffolded:
- **Easy**: mostly local or single-pass rules
- **Medium**: object detection, long-range relations, or two-pass reasoning
- **Hard**: normalization, local coordinate frames, output resizing, or relational comparison

All code snippets assume the helper library in the companion Python file, especially utilities such as `components`, `bbox`, `horizontal_runs`, `vertical_runs`, `find_holes_of_component`, and `normalize_shape`.

## Easy

### E1 — Horizontal run endcaps

**What it tests:** Run detection; preserve-interior behavior.

**Staged hint:** Stage 1: detect horizontal 2-runs. Stage 2: recolor only the two boundary cells.

**Train 1 — input**
```text
0000000
0222200
0002000
0220000
0000000
```

**Train 1 — output**
```text
0000000
0822800
0002000
0220000
0000000
```

**Train 2 — input**
```text
00222000
00000000
02222220
00022000
```

**Train 2 — output**
```text
00828000
00000000
08222280
00022000
```

**Test — input**
```text
000000000
022200200
000000000
002222200
000020000
```

**Test — expected output**
```text
000000000
082800200
000000000
008222800
000020000
```

**Written solution**

For every horizontal run of color 2 with length at least 3, change only the first and last cell of that run to color 8. Leave the interior 2s and everything else unchanged.

**Reference program (`solve_E1`)**
```python
def solve_E1(g: Grid, src=2, dst=8) -> Grid:
    out = clone(g)
    for r, c0, c1, val in horizontal_runs(g, color=src):
        if c1-c0+1 >= 3:
            out[r][c0] = dst
            out[r][c1] = dst
    return out
```

---

### E2 — Vertical domino promotion

**What it tests:** Exact-length reasoning; distinguish length-2 from longer runs.

**Staged hint:** First classify vertical 3-runs by length, then recolor only the length-2 cases.

**Train 1 — input**
```text
000000
003000
003000
000300
000300
000300
```

**Train 1 — output**
```text
000000
007000
007000
000300
000300
000300
```

**Train 2 — input**
```text
0300000
0300000
0003000
0003000
0000300
```

**Train 2 — output**
```text
0700000
0700000
0007000
0007000
0000300
```

**Test — input**
```text
0003000
0003000
0300000
0300000
0000300
0000300
0000300
```

**Test — expected output**
```text
0007000
0007000
0700000
0700000
0000300
0000300
0000300
```

**Written solution**

Every vertical run of color 3 of exact length 2 becomes color 7. Single 3s and longer 3-columns stay unchanged.

**Reference program (`solve_E2`)**
```python
def solve_E2(g: Grid, src=3, dst=7) -> Grid:
    out = clone(g)
    for r0, r1, c, val in vertical_runs(g, color=src):
        if r1-r0+1 == 2:
            for r in range(r0, r1+1):
                out[r][c] = dst
    return out
```

---

### E3 — Fill ring centers

**What it tests:** Local 3×3 pattern recognition.

**Staged hint:** First mark valid 3×3 rings, then write 6 into their centers.

**Train 1 — input**
```text
0000000
0444000
0404000
0444000
0000000
```

**Train 1 — output**
```text
0000000
0444000
0464000
0444000
0000000
```

**Train 2 — input**
```text
00000000
04440000
04040000
04440000
00004440
00004040
00004440
00000000
```

**Train 2 — output**
```text
00000000
04440000
04640000
04440000
00004440
00004640
00004440
00000000
```

**Test — input**
```text
000000000
044400000
040400000
044400000
000000000
000044400
000040400
000044400
000000000
```

**Test — expected output**
```text
000000000
044400000
046400000
044400000
000000000
000044400
000046400
000044400
000000000
```

**Written solution**

Whenever a 3×3 neighborhood has color 4 on all eight outer cells and 0 in the center, fill the center with color 6.

**Reference program (`solve_E3`)**
```python
def solve_E3(g: Grid, border=4, fill=6) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            # check 3x3 ring with center zero
            coords = [(r+dr, c+dc) for dr in (-1,0,1) for dc in (-1,0,1)]
            if g[r][c] == 0:
                ok = True
                for rr,cc in coords:
                    if (rr,cc)==(r,c): continue
                    if g[rr][cc] != border:
                        ok=False; break
                if ok:
                    out[r][c] = fill
    return out
```

---

### E4 — Vertical symmetrization

**What it tests:** Global reflection across a fixed axis.

**Staged hint:** Use the grid width to compute each mirror column, then paint both original and mirrored cells.

**Train 1 — input**
```text
0000000
0200000
0022000
0003000
0000000
```

**Train 1 — output**
```text
0000000
0200020
0022200
0003000
0000000
```

**Train 2 — input**
```text
00000000
00040000
00500000
00550000
00000000
```

**Train 2 — output**
```text
00000000
00044000
00500500
00555500
00000000
```

**Test — input**
```text
000000000
000600000
002200000
000030000
000000000
```

**Test — expected output**
```text
000000000
000606000
002202200
000030000
000000000
```

**Written solution**

Reflect every nonzero cell across the vertical midline of the grid and add the mirrored copy, while preserving the original cells.

**Reference program (`solve_E4`)**
```python
def solve_E4(g: Grid) -> Grid:
    return reflect_vertical(g)
```

---

### E5 — Isolated cells become 9

**What it tests:** Cardinal-neighbor checks; singleton detection.

**Staged hint:** Stage 1: mark isolated nonzero cells. Stage 2: recolor marked cells to 9.

**Train 1 — input**
```text
0000000
0200300
0000000
0044000
0000005
```

**Train 1 — output**
```text
0000000
0900900
0000000
0044000
0000009
```

**Train 2 — input**
```text
1000000
0000000
0002200
0000000
0000006
```

**Train 2 — output**
```text
9000000
0000000
0002200
0000000
0000009
```

**Test — input**
```text
00000000
04000000
00000030
00000000
00220000
00000000
00050000
```

**Test — expected output**
```text
00000000
09000000
00000090
00000000
00220000
00000000
00090000
```

**Written solution**

Any nonzero cell whose four cardinal neighbors are all 0 is recolored to 9. Cells that touch any nonzero neighbor keep their original color.

**Reference program (`solve_E5`)**
```python
def solve_E5(g: Grid, dst=9) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                if all(not (0 <= r+dr < h and 0 <= c+dc < w and g[r+dr][c+dc]!=0)
                       for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]):
                    out[r][c] = dst
    return out
```

---

### E6 — Single-7 rows fill fully

**What it tests:** Whole-row activation from a sparse cue.

**Staged hint:** First detect qualifying rows, then overwrite those rows with all 7s.

**Train 1 — input**
```text
0007000
0000000
0070700
0000000
0007000
```

**Train 1 — output**
```text
7777777
0000000
0070700
0000000
7777777
```

**Train 2 — input**
```text
000000
070000
000000
007000
000770
```

**Train 2 — output**
```text
000000
777777
000000
777777
000770
```

**Test — input**
```text
0008000
0007000
0000000
7000000
0000000
0070700
```

**Test — expected output**
```text
0008000
7777777
0000000
7777777
0000000
0070700
```

**Written solution**

If a row contains exactly one nonzero cell and that cell is 7, fill the entire row with 7. Any row with a different nonzero pattern is left alone.

**Reference program (`solve_E6`)**
```python
def solve_E6(g: Grid, marker=7) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        nz = [x for x in g[r] if x != 0]
        if len(nz) == 1 and nz[0] == marker:
            out[r] = [marker]*w
    return out
```

---

### E7 — Mark odd vertical run centers

**What it tests:** Run centers; odd-vs-even length discrimination.

**Staged hint:** Compute each 5-run’s length; if it is odd and at least 3, recolor the midpoint.

**Train 1 — input**
```text
005000
005000
005000
000000
000500
000500
000500
000500
```

**Train 1 — output**
```text
005000
002000
005000
000000
000500
000500
000500
000500
```

**Train 2 — input**
```text
0500000
0500000
0500000
0500000
0000500
0000500
0000500
```

**Train 2 — output**
```text
0500000
0500000
0500000
0500000
0000500
0000200
0000500
```

**Test — input**
```text
0005000
0005000
0005000
0005000
0050000
0050000
0050000
0050000
0050000
```

**Test — expected output**
```text
0005000
0005000
0005000
0005000
0050000
0050000
0020000
0050000
0050000
```

**Written solution**

For each vertical run of color 5 with odd length at least 3, recolor only its center cell to 2. Even-length runs or short runs do not change.

**Reference program (`solve_E7`)**
```python
def solve_E7(g: Grid, src=5, dst=2) -> Grid:
    out = clone(g)
    for r0,r1,c,val in vertical_runs(g, color=src):
        length = r1-r0+1
        if length >= 3 and length % 2 == 1:
            center = (r0+r1)//2
            out[center][c] = dst
    return out
```

---

## Medium

### M1 — Recolor the smallest object

**What it tests:** Connected components and size comparison.

**Staged hint:** Stage 1: segment objects. Stage 2: compare areas and recolor the smallest one.

**Train 1 — input**
```text
00000000
02200000
02200030
00000030
00044430
00044400
```

**Train 1 — output**
```text
00000000
02200000
02200080
00000080
00044480
00044400
```

**Train 2 — input**
```text
000500000
000500660
000000660
022200000
022200000
```

**Train 2 — output**
```text
000800000
000800660
000000660
022200000
022200000
```

**Test — input**
```text
000000000
033300000
033300400
000000400
055000400
055000000
```

**Test — expected output**
```text
000000000
033300000
033300800
000000800
055000800
055000000
```

**Written solution**

Find all nonzero connected components. Recolor the unique smallest component to 8, while leaving every other object unchanged.

**Reference program (`solve_M1`)**
```python
def solve_M1(g: Grid, dst=8) -> Grid:
    comps = components(g)
    smallest = min(comps, key=lambda x: len(x[1]))[1]
    out = clone(g)
    for r,c in smallest:
        out[r][c] = dst
    return out
```

---

### M2 — Fill each object’s bounding box

**What it tests:** Component extraction and bbox reasoning.

**Staged hint:** Detect components first; then replace each shape by its filled bounding rectangle.

**Train 1 — input**
```text
0000000
0200000
0222000
0000000
0003300
0003000
0000000
```

**Train 1 — output**
```text
0000000
0222000
0222000
0000000
0003300
0003300
0000000
```

**Train 2 — input**
```text
00000000
00440000
00040000
00000000
00005550
00000050
00000000
```

**Train 2 — output**
```text
00000000
00440000
00440000
00000000
00005550
00005550
00000000
```

**Test — input**
```text
000000000
030000000
033000000
003000000
000000000
000066000
000006000
000000000
```

**Test — expected output**
```text
000000000
033000000
033000000
033000000
000000000
000066000
000066000
000000000
```

**Written solution**

For each nonzero object, compute its bounding box and fill that whole rectangle with the object’s color. The output is otherwise blank.

**Reference program (`solve_M2`)**
```python
def solve_M2(g: Grid) -> Grid:
    out = [[0]*len(g[0]) for _ in range(len(g))]
    for col, comp in components(g):
        r0,r1,c0,c1 = bbox(comp)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c] = col
    return out
```

---

### M3 — Connect aligned markers

**What it tests:** Long-range same-row / same-column relations.

**Staged hint:** Find same-colored aligned pairs, then draw horizontal or vertical segments between valid pairs.

**Train 1 — input**
```text
0000000
0200020
0000000
0030000
0000000
0030000
0000000
```

**Train 1 — output**
```text
0000000
0222220
0000000
0030000
0030000
0030000
0000000
```

**Train 2 — input**
```text
00040000
00000000
00040000
00000000
05000050
00000000
```

**Train 2 — output**
```text
00040000
00040000
00040000
00000000
05555550
00000000
```

**Test — input**
```text
000000000
060000060
000000000
000700000
000000000
000700000
000000000
```

**Test — expected output**
```text
000000000
066666660
000000000
000700000
000700000
000700000
000000000
```

**Written solution**

If two cells of the same color lie on the same row or the same column with only 0s between them, fill the entire gap between them in that same color.

**Reference program (`solve_M3`)**
```python
def solve_M3(g: Grid) -> Grid:
    # same-color single-cell markers in same row or col, fill gap if only zeros between.
    h,w = dims(g)
    out = clone(g)
    # find singletons? or any cells of a color; use all individual cells of nonzero
    cells_by_color = defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                cells_by_color[g[r][c]].append((r,c))
    for color, cells in cells_by_color.items():
        for i in range(len(cells)):
            for j in range(i+1,len(cells)):
                r1,c1 = cells[i]; r2,c2 = cells[j]
                if r1 == r2:
                    lo, hi = sorted([c1,c2])
                    if all(g[r1][c]==0 for c in range(lo+1,hi)):
                        for c in range(lo,hi+1):
                            out[r1][c]=color
                elif c1 == c2:
                    lo, hi = sorted([r1,r2])
                    if all(g[r][c1]==0 for r in range(lo+1,hi)):
                        for r in range(lo,hi+1):
                            out[r][c1]=color
    return out
```

---

### M4 — Copy payload by marker vector

**What it tests:** Learn a translation vector from markers, then apply it.

**Staged hint:** First recover the translation from 1→2. Then clone each payload cell to its translated position.

**Train 1 — input**
```text
1000000
0002000
0000000
0033000
0003000
0000000
```

**Train 1 — output**
```text
1000000
0002000
0000000
0033000
0003033
0000003
```

**Train 2 — input**
```text
00000000
01000000
00000000
00002000
00044000
00040000
00000000
```

**Train 2 — output**
```text
00000000
01000000
00000000
00002000
00044000
00040000
00000044
```

**Test — input**
```text
000000000
001000000
000000000
000000200
000550000
000050000
000000000
000000000
```

**Test — expected output**
```text
000000000
001000000
000000000
000000200
000550000
000050000
000000055
000000005
```

**Written solution**

Read the vector from the cell colored 1 to the cell colored 2. Copy every non-marker object by that vector, preserving the original objects and the markers.

**Reference program (`solve_M4`)**
```python
def solve_M4(g: Grid, m1=1, m2=2):
    h,w=dims(g)
    pos1=pos2=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==m1: pos1=(r,c)
            elif g[r][c]==m2: pos2=(r,c)
    dr=pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and g[r][c] not in (m1,m2):
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=g[r][c]
    return out
```

---

### M5 — Keep only border-touching objects

**What it tests:** Object filtering by border contact.

**Staged hint:** Segment objects, test whether any cell hits the border, and keep only the positive cases.

**Train 1 — input**
```text
2000000
2200000
0003300
0003300
0000004
```

**Train 1 — output**
```text
2000000
2200000
0000000
0000000
0000004
```

**Train 2 — input**
```text
0000000
0555000
0505000
0555000
0000006
6000000
```

**Train 2 — output**
```text
0000000
0000000
0000000
0000000
0000006
6000000
```

**Test — input**
```text
00070000
00070000
00000000
00333000
00333000
00000008
```

**Test — expected output**
```text
00070000
00070000
00000000
00000000
00000000
00000008
```

**Written solution**

Keep the connected components that touch at least one outer border cell of the grid. Remove all components that are strictly interior.

**Reference program (`solve_M5`)**
```python
def solve_M5(g: Grid) -> Grid:
    h,w = dims(g)
    out = [[0]*w for _ in range(h)]
    for col, comp in components(g):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp):
            for r,c in comp:
                out[r][c] = col
    return out
```

---

### M6 — Rank components by size

**What it tests:** Relative ordering over multiple objects.

**Staged hint:** Stage 1: measure object sizes. Stage 2: repaint by rank.

**Train 1 — input**
```text
00000000
02000000
02000000
00003330
00000000
00004440
00004000
```

**Train 1 — output**
```text
00000000
01000000
01000000
00002220
00000000
00003330
00003000
```

**Train 2 — input**
```text
000000000
005500000
000500000
000000000
000066600
000000600
000000000
000000070
```

**Train 2 — output**
```text
000000000
002200000
000200000
000000000
000033300
000000300
000000000
000000010
```

**Test — input**
```text
000000000
000880000
000800000
000000000
044444000
000000000
000000660
000000660
```

**Test — expected output**
```text
000000000
000110000
000100000
000000000
033333000
000000000
000000220
000000220
```

**Written solution**

Find all connected components and sort them by area from smallest to largest. Recolor the smallest component to 1, the next to 2, and the largest to 3, preserving each shape.

**Reference program (`solve_M6`)**
```python
def solve_M6(g: Grid) -> Grid:
    comps = components(g)
    comps_sorted = sorted(comps, key=lambda x: len(x[1]))
    ranks = {id(comp): rank+1 for rank,(col,comp) in enumerate(comps_sorted)}  # not used
    out = [[0]*len(g[0]) for _ in range(len(g))]
    # unique sizes/order guaranteed in examples
    for rank, (col, comp) in enumerate(comps_sorted, start=1):
        for r,c in comp:
            out[r][c] = rank
    return out
```

---

### M7 — Show holes only

**What it tests:** Hole detection inside closed shapes.

**Staged hint:** Treat each object separately inside its bounding box: flood outside background, then keep the unreachable zero cells.

**Train 1 — input**
```text
0000000
0222000
0202000
0222000
0000000
```

**Train 1 — output**
```text
0000000
0000000
0020000
0000000
0000000
```

**Train 2 — input**
```text
00000000
03330000
03030000
03330000
00044400
00040400
00044400
00000000
```

**Train 2 — output**
```text
00000000
00000000
00300000
00000000
00000000
00004000
00000000
00000000
```

**Test — input**
```text
000000000
055500000
050500000
055500000
000000000
000066600
000060600
000066600
000000000
```

**Test — expected output**
```text
000000000
000000000
005000000
000000000
000000000
000000000
000006000
000000000
000000000
```

**Written solution**

For each object that encloses one or more internal background cells, output only those hole cells, colored with the enclosing object’s color. Everything else becomes 0.

**Reference program (`solve_M7`)**
```python
def solve_M7(g: Grid) -> Grid:
    h,w = dims(g)
    out = [[0]*w for _ in range(h)]
    for col, comp in components(g):
        holes = find_holes_of_component(g, comp)
        for r,c in holes:
            out[r][c] = col
    return out
```

---

## Hard

### H1 — Pack objects sorted by area

**What it tests:** Object extraction, output resizing, sorting, and repacking.

**Staged hint:** Segment and crop first; only after sorting should you build the new output canvas.

**Train 1 — input**
```text
000000000
022000330
022000000
000000000
000440000
000440000
000400000
```

**Train 1 — output**
```text
33022044
00022044
00000040
```

**Train 2 — input**
```text
0000000000
0555000000
0000000000
0000066000
0000066000
0000000000
0000000070
```

**Train 2 — output**
```text
70555066
00000066
```

**Test — input**
```text
00000000000
00330000000
00300000000
00000000000
00004440000
00000040000
00000000020
00000000020
```

**Test — expected output**
```text
20330444
20300004
```

**Written solution**

Extract every nonzero object, crop it to its own bounding box, sort the cropped objects by area from smallest to largest, and pack them left-to-right in a new output grid with one blank column between neighboring objects. Top-align all packed shapes.

**Reference program (`solve_H1`)**
```python
def solve_H1(g: Grid) -> Grid:
    # Extract components, sort ascending by area, pack left->right with one zero col between.
    comps = components(g)
    items=[]
    maxh=0
    for col, comp in comps:
        r0,r1,c0,c1 = bbox(comp)
        H=r1-r0+1; W=c1-c0+1
        maxh=max(maxh,H)
        cells=[(r-r0,c-c0) for r,c in comp]
        items.append((len(comp), H, W, col, cells))
    items.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    total_w = sum(item[2] for item in items) + max(0, len(items)-1)
    out = [[0]*total_w for _ in range(maxh)]
    offset=0
    for area,H,W,col,cells in items:
        # top-align
        for r,c in cells:
            out[r][offset+c] = col
        offset += W + 1
    return out
```

---

### H2 — Repair the defective copy

**What it tests:** Relational comparison between multiple normalized shapes.

**Staged hint:** Normalize each object to its own top-left corner, compare the normalized shapes, then output the repaired canonical pattern.

**Train 1 — input**
```text
000000000
022200220
002000020
000000000
022200000
002000000
000000000
```

**Train 1 — output**
```text
222
020
```

**Train 2 — input**
```text
0000000000
0330000330
0030000030
0030000000
0000000000
0330000000
0030000000
0030000000
```

**Train 2 — output**
```text
33
03
03
```

**Test — input**
```text
00000000000
04440000440
00400000040
00000000000
04440000000
00400000000
00000000000
```

**Test — expected output**
```text
444
040
```

**Written solution**

Three copies of the same-colored shape appear in the input. Two are complete; one is missing exactly one cell. Identify the defective copy, infer the full canonical shape from the complete copies, and output only the repaired canonical shape cropped tightly.

**Reference program (`solve_H2`)**
```python
def solve_H2(g: Grid) -> Grid:
    # assume components of same color; two shapes identical up to translation, one missing one cell.
    comps = components(g)
    # group by color maybe same; compare normalized shapes
    shapes = []
    for col, comp in comps:
        norm = set(normalize_shape(comp))
        shapes.append((col, comp, norm))
    # find target union shape: choose shape with max size or most common subset/superset relation
    # Here examples should ensure one shape size = canonical and one smaller by 1.
    # We'll take the largest normalized shape as canonical.
    canonical = max(shapes, key=lambda x: len(x[2]))[2]
    # defective comp is one whose norm is strict subset of canonical
    defective = None
    for col, comp, norm in shapes:
        if norm != canonical and norm.issubset(canonical):
            defective = (col, comp, norm)
            break
    if defective is None:
        defective = min(shapes, key=lambda x: len(x[2]))
    col, comp, norm = defective
    r0,r1,c0,c1 = bbox(comp)
    # output repaired defective object only, cropped
    maxr = max(r for r,c in canonical)
    maxc = max(c for r,c in canonical)
    out = [[0]*(maxc+1) for _ in range(maxr+1)]
    for r,c in canonical:
        out[r][c] = col
    return out
```

---

### H3 — Shift all payload objects by the learned vector

**What it tests:** Global relational vector applied to multiple objects; original removed.

**Staged hint:** Recover the vector first; then replay every non-marker cell into the translated position on a fresh blank canvas.

**Train 1 — input**
```text
01000000
00020000
00000000
00330000
00030400
00000400
00000000
```

**Train 1 — output**
```text
00000000
00000000
00000000
00000000
00003300
00000304
00000004
```

**Train 2 — input**
```text
000000000
000100000
000000000
000000020
055000000
050060000
000060000
000000000
000000000
```

**Train 2 — output**
```text
000000000
000000000
000000000
000000000
000000000
000000000
000005500
000005006
000000006
```

**Test — input**
```text
1000000000
0000000000
0000200000
0000000000
0330000000
0030070000
0000070000
0000000000
0000000000
```

**Test — expected output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000033000
0000003007
0000000007
```

**Written solution**

The vector from color 1 to color 2 is the motion rule. Shift every non-marker object by that vector into a blank output grid. Do not keep the original objects, and do not copy the markers.

**Reference program (`solve_H3`)**
```python
def solve_H3(g: Grid, m1=1, m2=2, marker_colors={1,2}) -> Grid:
    h,w=dims(g)
    pos1=pos2=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==m1: pos1=(r,c)
            elif g[r][c]==m2: pos2=(r,c)
    dr = pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    out = [[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0 and g[r][c] not in marker_colors:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=g[r][c]
    return out
```

---

### H4 — Mirror inside the local frame

**What it tests:** Local coordinate frame inside an enclosing object.

**Staged hint:** Treat the frame as a local workspace with its own left/right boundaries; mirror only the interior payload cells.

**Train 1 — input**
```text
000000000
088888880
080300080
080030080
080000080
088888880
000000000
```

**Train 1 — output**
```text
000000000
088888880
080303080
080030080
080000080
088888880
000000000
```

**Train 2 — input**
```text
0000000000
0088888880
0080400080
0084400080
0080000080
0088888880
0000000000
```

**Train 2 — output**
```text
0000000000
0088888880
0080404080
0084404480
0080000080
0088888880
0000000000
```

**Test — input**
```text
00000000000
00888888880
00800600080
00806600080
00800000080
00888888880
00000000000
```

**Test — expected output**
```text
00000000000
00888888880
00800660080
00806666080
00800000080
00888888880
00000000000
```

**Written solution**

Find the rectangular frame made of color 8. Inside that frame, mirror every non-frame nonzero cell across the frame’s own vertical centerline, preserving the original interior cells and the frame itself.

**Reference program (`solve_H4`)**
```python
def solve_H4(g: Grid, frame_color=8):
    # find single rectangular frame; mirror non-frame nonzero cells inside its interior across local vertical midline, preserving originals
    h,w=dims(g)
    # frame cells of given color
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==frame_color]
    r0,r1,c0,c1 = bbox(frame_cells)
    out = clone(g)
    interior_c0, interior_c1 = c0+1, c1-1
    for r in range(r0+1, r1):
        for c in range(c0+1, c1):
            val = g[r][c]
            if val != 0 and val != frame_color:
                mc = c0 + c1 - c
                if c0 < mc < c1:
                    out[r][mc] = val
    return out
```

---

### H5 — Fill holes for the most component-rich color

**What it tests:** Color-level aggregation plus per-object hole filling.

**Staged hint:** First decide which color wins the component-count vote; only then inspect holes in components of that color.

**Train 1 — input**
```text
000000000
022200000
020200330
022200330
000000000
000022200
000020200
000022200
044400000
040400000
044400000
```

**Train 1 — output**
```text
000000000
022200000
029200330
022200330
000000000
000022200
000029200
000022200
044400000
040400000
044400000
```

**Train 2 — input**
```text
0000000000
0555000000
0505000000
0555000000
0000000000
0000555000
0000505000
0000555000
0000000000
0000006600
0000006600
```

**Train 2 — output**
```text
0000000000
0555000000
0595000000
0555000000
0000000000
0000555000
0000595000
0000555000
0000000000
0000006600
0000006600
```

**Test — input**
```text
0000000000
0333000000
0303000000
0333000000
0000000000
0000033300
0000030300
0000033300
0000000000
0000000044
0000000044
```

**Test — expected output**
```text
0000000000
0333000000
0393000000
0333000000
0000000000
0000033300
0000039300
0000033300
0000000000
0000000044
0000000044
```

**Written solution**

Count how many separate connected components each color has. Choose the color with the most components. For that color only, fill the holes inside its closed components with color 9. Leave all existing colored cells untouched.

**Reference program (`solve_H5`)**
```python
def solve_H5(g: Grid) -> Grid:
    # count components per color; among color with most components, fill holes of its components with 9.
    comps = components(g)
    by_color = defaultdict(list)
    for col, comp in comps:
        by_color[col].append(comp)
    target_color = max(by_color.items(), key=lambda kv: len(kv[1]))[0]
    out = clone(g)
    for comp in by_color[target_color]:
        holes = find_holes_of_component(g, comp)
        for r,c in holes:
            out[r][c] = 9
    return out
```

---

### H6 — Complete the missing mirrored quadrant

**What it tests:** Quadrant decomposition and composition via flips.

**Staged hint:** Split into quadrants, identify the missing one, infer which horizontal/vertical flips are needed, then write only that quadrant.

**Train 1 — input**
```text
2200022
2000002
0000000
0000000
0000000
2000000
2200000
```

**Train 1 — output**
```text
2200022
2000002
0000000
0000000
0000000
2000002
2200022
```

**Train 2 — input**
```text
0300030
0330330
0000000
0000000
0000000
0330000
0300000
```

**Train 2 — output**
```text
0300030
0330330
0000000
0000000
0000000
0330330
0300030
```

**Test — input**
```text
4400044
0400004
0400004
0000000
0000000
0400000
4400000
```

**Test — expected output**
```text
4400044
0400004
0400004
0000000
0000040
0400040
4400044
```

**Written solution**

The grid is divided into four quadrants by a central zero row and zero column. Three quadrants contain mirrored versions of the same pattern, and one quadrant is blank. Fill the blank quadrant with the pattern transformed by the flips needed to match its location.

**Reference program (`solve_H6`)**
```python
def solve_H6(g: Grid):
    # assume odd dims with central row/col zero separators. Three quadrants have mirrored copies of one shape color, one quadrant empty.
    h,w = dims(g)
    midr, midc = h//2, w//2
    # extract quadrants excluding center row/col
    quads = {
        'TL': [row[:midc] for row in g[:midr]],
        'TR': [row[midc+1:] for row in g[:midr]],
        'BL': [row[:midc] for row in g[midr+1:]],
        'BR': [row[midc+1:] for row in g[midr+1:]],
    }
    # determine missing quadrant (all zeros)
    missing = next(name for name,q in quads.items() if all(v==0 for row in q for v in row))
    # choose source quadrant any non-empty
    source_name = next(name for name,q in quads.items() if name != missing and any(v!=0 for row in q for v in row))
    source = quads[source_name]
    # to fill missing, mirror source appropriately from source_name to missing
    import copy
    def flip_h(q): return q[::-1]
    def flip_v(q): return [row[::-1] for row in q]
    # Actually horizontal/vertical naming: across central horizontal axis flips rows, across vertical axis flips cols.
    q = source
    # Map from source to target by flips
    if source_name[0] != missing[0]:  # T/B differs
        q = q[::-1]
    if source_name[1] != missing[1]:  # L/R differs
        q = [row[::-1] for row in q]
    # write into out
    out = clone(g)
    # positions for missing quad
    rstart = 0 if missing[0]=='T' else midr+1
    cstart = 0 if missing[1]=='L' else midc+1
    for r in range(len(q)):
        for c in range(len(q[0])):
            out[rstart+r][cstart+c] = q[r][c]
    return out
```

---

### H7 — Normalized shape intersection

**What it tests:** Shape normalization and set intersection.

**Staged hint:** Normalize each object separately before comparing cells; do not compare them in their original positions.

**Train 1 — input**
```text
000000000
022200000
002000000
000000000
000003300
000003000
000000000
```

**Train 1 — output**
```text
88
```

**Train 2 — input**
```text
0000000000
0440000000
0444000000
0000000000
0000000550
0000000050
0000000050
0000000000
```

**Train 2 — output**
```text
88
08
```

**Test — input**
```text
00000000000
00660000000
00060000000
00000000000
00000007700
00000000770
00000000070
00000000000
```

**Test — expected output**
```text
88
08
```

**Written solution**

Take the two objects, normalize each one to its own top-left corner, and compute the overlap of those normalized shapes. Output the overlapping cells as color 8 in a tightly cropped grid.

**Reference program (`solve_H7`)**
```python
def solve_H7(g: Grid):
    # assume two components of colors 2 and 3. Normalize each to top-left of its bbox, then output overlap cells as 8 in cropped bbox.
    comps = components(g)
    # choose first two components
    comps = comps[:2]
    norms=[]
    for col, comp in comps:
        norms.append(set(normalize_shape(comp)))
    inter = norms[0] & norms[1]
    if not inter:
        return [[0]]
    maxr=max(r for r,c in inter); maxc=max(c for r,c in inter)
    out=[[0]*(maxc+1) for _ in range(maxr+1)]
    for r,c in inter:
        out[r][c]=8
    return out
```

---
