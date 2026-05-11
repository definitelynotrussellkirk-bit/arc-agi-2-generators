# ARC Puzzle Bank — Set 16
This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

This batch pushes into a different slice of the ARC space: diagonal and vertical gap logic, directed border beams, crop-transpose moves, bounding-box abstractions, rank-based recoloring, frame interiors, normalized overlays, scripted transform galleries, portal routing, dihedral shape matching, relative-offset transfer, contact graphs, and crosshair docking.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set16.json` — machine-readable task data
- `arc_puzzle_bank_21_set16_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set16_validation.txt` — validation log

## Easy (7)

### easy_p01 — Fill diagonal one-cell gaps

**Written rule:** If a zero cell sits exactly between two matching nonzero cells on a diagonal, fill it with that color.

**Program function:** `solve_easy_p01`

**Primitives:** diagonal_gap_fill

```python
def solve_easy_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            fill=0
            if 0<=r-1<h and 0<=c-1<w and 0<=r+1<h and 0<=c+1<w:
                a,b=g[r-1][c-1], g[r+1][c+1]
                if a!=0 and a==b:
                    fill=a
            if fill==0 and 0<=r-1<h and 0<=c+1<w and 0<=r+1<h and 0<=c-1<w:
                a,b=g[r-1][c+1], g[r+1][c-1]
                if a!=0 and a==b:
                    fill=a
            out[r][c]=fill
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 0 0 0 0 6
0 0 0 0 0 0 0
0 0 0 2 0 6 0
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 0 4 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 2 0 0 0 0 6
0 0 2 0 0 0 0
0 0 0 2 0 6 0
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 0 4 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 3 0 0 0 5 0
0 0 0 0 0 0 0 0
0 0 3 0 5 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 3 0 0 0 5 0
0 0 0 0 0 5 0 0
0 0 3 0 5 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 7 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 6
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 6
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
```

### easy_p02 — Expand each singleton into a horizontal brush

**Written rule:** Every nonzero singleton paints itself plus its immediate left and right neighbors in the same row.

**Program function:** `solve_easy_p02`

**Primitives:** horizontal_brush

```python
def solve_easy_p02(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                col=g[r][c]
                for dc in (-1,0,1):
                    nc=c+dc
                    if 0<=nc<w:
                        out[r][nc]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 2 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 6
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 2 2 2 0 0 0
0 0 0 0 0 0 0
0 0 0 4 4 4 0
0 0 0 0 0 0 0
0 0 0 0 0 6 6
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 3
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0
0 0 0 0 0 0 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0
0 0 0 9 0 0
0 0 0 0 0 0
2 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 7
```

**Train 3 output**
```text
0 0 0 0 0 0
0 0 9 9 9 0
0 0 0 0 0 0
2 2 0 0 0 0
0 0 0 0 0 0
0 0 0 0 7 7
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0
```

### easy_p03 — Beam rightward from left-border seeds

**Written rule:** Every nonzero cell on the left border paints rightward through zeros until the first original blocker in its row, or to the edge.

**Program function:** `solve_easy_p03`

**Primitives:** left_border_beam

```python
def solve_easy_p03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        seed=g[r][0]
        if seed==0:
            continue
        stop=w
        for c in range(1,w):
            if g[r][c]!=0:
                stop=c
                break
        for c in range(1,stop):
            if g[r][c]==0:
                out[r][c]=seed
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
2 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0
4 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
2 2 2 2 2 7 0 0
0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3
4 4 4 5 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
7 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 9 0
0 0 0 0 0 0 0 0 0
7 7 7 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0
5 0 0 3 0 0 0
0 0 0 0 0 0 0
2 0 0 0 0 0 0
9 0 0 0 0 8 0
0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
5 5 5 3 0 0 0
0 0 0 0 0 0 0
2 2 2 2 2 2 2
9 9 9 9 9 8 0
0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0
3 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 2 0 0
0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5
3 3 3 3 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### easy_p04 — Reduce each solid 3x3 square to its corners

**Written rule:** Every monochrome solid 3x3 block is replaced by just its four corner cells.

**Program function:** `solve_easy_p04`

**Primitives:** solid3_to_corners

```python
def solve_easy_p04(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h-2):
        for c in range(w-2):
            col=g[r][c]
            if col==0:
                continue
            ok=True
            cells=[]
            for rr in range(r,r+3):
                for cc in range(c,c+3):
                    if g[rr][cc]!=col:
                        ok=False
                    cells.append((rr,cc))
            if ok:
                # ensure exact isolated 3x3? not necessary with our examples
                for rr,cc in [(r,c),(r,c+2),(r+2,c),(r+2,c+2)]:
                    out[rr][cc]=col
                used.update(cells)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### easy_p05 — Fill vertical one-cell gaps

**Written rule:** If two matching nonzero cells stand in the same column with exactly one zero between them, fill the middle cell.

**Program function:** `solve_easy_p05`

**Primitives:** vertical_gap_fill

```python
def solve_easy_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 0 0 0 4 0
0 0 0 0 0 0 0
0 2 0 0 0 4 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 2 0 0 0 4 0
0 2 0 0 0 4 0
0 2 0 0 0 4 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0
0 5 0 0 0 0
0 0 0 0 0 0
0 5 0 0 0 0
0 0 0 0 0 9
0 0 0 0 0 0
0 0 0 0 0 9
```

**Train 3 output**
```text
0 0 0 0 0 0
0 5 0 0 0 0
0 5 0 0 0 0
0 5 0 0 0 0
0 0 0 0 0 9
0 0 0 0 0 9
0 0 0 0 0 9
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 4 0 0 0 2 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 2 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0
0 0 4 0 0 0 2 0
0 0 4 0 0 0 2 0
0 0 4 0 0 0 2 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

### easy_p06 — Keep only the lowest nonzero in each column

**Written rule:** For every column, erase all nonzero cells except the bottommost one.

**Program function:** `solve_easy_p06`

**Primitives:** column_last_nonzero

```python
def solve_easy_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        for r in range(h-1,-1,-1):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                break
    return out
```

**Train 1 input**
```text
0 2 0 0 0 4 0
0 0 0 0 0 0 0
0 3 0 0 0 6 0
0 0 0 0 0 0 0
0 5 0 0 0 4 0
0 0 0 0 0 0 0
0 2 0 0 0 9 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 2 0 0 0 9 0
```

**Train 2 input**
```text
0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0
5 0 0 8 0 0 3 0
0 0 0 0 0 0 0 0
4 0 0 9 0 0 6 0
0 0 0 0 0 0 0 0
2 0 0 1 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
2 0 0 1 0 0 0 0
```

**Train 3 input**
```text
0 9 0 0 0 0
0 0 0 5 0 0
0 7 0 0 0 0
0 0 0 0 0 0
0 3 0 4 0 0
0 0 0 0 0 0
0 1 0 2 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 1 0 2 0 0
```

**Test 1 input**
```text
0 2 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 5 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 2 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 2 0 0 0
```

### easy_p07 — Transpose the tight crop of the active pattern

**Written rule:** Crop the grid to the tight bounding box of all nonzero cells, then transpose that cropped pattern.

**Program function:** `solve_easy_p07`

**Primitives:** crop_transpose

```python
def solve_easy_p07(g):
    return transpose(crop_nonzero(g))
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 2 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 3 0 0
0 0 0 0 3 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 0 0
2 2 2 0
0 0 3 3
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 5 0 5 0 0
0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 5 0
0 0 5
0 5 5
```

**Train 3 input**
```text
0 0 0 0 0 0
0 0 7 7 0 0
0 0 0 7 0 0
0 0 9 7 0 0
0 0 9 0 0 0
0 0 0 0 0 0
```

**Train 3 output**
```text
7 0 9 9
7 7 7 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 0 0 0
6 6 6 0
0 0 7 7
```

## Medium (7)

### medium_p01 — Replace each object by its bounding-box outline

**Written rule:** For each connected monochrome object, draw the outline of its tight bounding box in the object’s color.

**Program function:** `solve_medium_p01`

**Primitives:** bbox_outline

```python
def solve_medium_p01(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components_by_color(g):
        col=comp['color']
        r0,c0,r1,c1=bbox(comp['cells'])
        for c in range(c0,c1+1):
            out[r0][c]=col
            out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=col
            out[r][c1]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 0
0 0 2 2 0 0 0 4 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 4 4 0
0 2 0 2 0 0 4 4 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0
0 5 0 5 0 0 0 0 0
0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0
0 0 0 0 6 6 6 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0
0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 5 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0
0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 5 5 5
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
```

### medium_p02 — Recolor objects by top-to-bottom rank

**Written rule:** Sort the connected objects by their topmost row, then recolor the first object 2, the next 3, the next 4, and so on while preserving shape and position.

**Program function:** `solve_medium_p02`

**Primitives:** rank_recolor_vertical

```python
def solve_medium_p02(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: (min(r for r,c in comp['cells']), min(c for r,c in comp['cells'])))
    palette=[2,3,4,5,6,7,8,9,1]
    h,w=dims(g)
    out=blank(h,w)
    for i,comp in enumerate(comps):
        col=palette[i]
        for r,c in comp['cells']:
            out[r][c]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 7 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 2 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 4 0
```

### medium_p03 — Use a corner color to select an object crop

**Written rule:** A single corner marker names the target color; output the tight crop of the object with that color.

**Program function:** `solve_medium_p03`

**Primitives:** corner_color_select_crop

```python
def solve_medium_p03(g):
    h,w=dims(g)
    marker=0
    corners=[g[0][0],g[0][w-1],g[h-1][0],g[h-1][w-1]]
    for v in corners:
        if v!=0:
            marker=v
            break
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==marker and (r,c) not in [(0,0),(0,w-1),(h-1,0),(h-1,w-1)]]
    # if object touches corner and corner marker same color, exclude only actual corner marker
    if not cells:
        cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==marker]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]
```

**Train 1 input**
```text
2 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2
2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 3
0 0 0 6 6 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0
0 0 0 0 3 0 0 0 0
```

**Train 2 output**
```text
3 3
0 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 8 0
0 0 0 9 9 0 0 0 0
0 0 0 9 0 0 0 0 0
```

**Train 3 output**
```text
9 9
9 0
```

**Test 1 input**
```text
5 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```

**Test 1 output**
```text
5
```

### medium_p04 — Transpose each object and stack them vertically

**Written rule:** Crop each object, transpose it, and stack the transposed pieces top-to-bottom in left-to-right object order with one blank row between them.

**Program function:** `solve_medium_p04`

**Primitives:** transpose_stack

```python
def solve_medium_p04(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: min(c for r,c in comp['cells']))
    pieces=[]
    maxw=0
    totalh=0
    for comp in comps:
        crop,_=crop_component(g, comp['cells'])
        tr=transpose(crop)
        pieces.append(tr)
        ph,pw=dims(tr)
        maxw=max(maxw,pw)
        totalh += ph
    totalh += max(0,len(pieces)-1)
    out=blank(totalh,maxw)
    r=0
    for idx,p in enumerate(pieces):
        ph,pw=dims(p)
        for i in range(ph):
            for j in range(pw):
                out[r+i][j]=p[i][j]
        r += ph + 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 0 0
0 0 2 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0
2 2
0 0
5 0
5 5
0 0
4 0
4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
7 7 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0
```

**Train 2 output**
```text
7 7
0 7
0 0
5 0
5 5
0 0
3 0
3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 3 output**
```text
2 2
0 2
0 0
8 0
8 8
0 0
5 0
5 5
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 5 5 0 0
0 0 3 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
3 0
3 3
0 0
7 0
7 7
0 0
5 0
5 5
```

### medium_p05 — Fill each rectangular frame with its seed color

**Written rule:** Each hollow rectangular frame contains a seed cell; fill that frame’s interior with the seed color while keeping the frame border intact.

**Program function:** `solve_medium_p05`

**Primitives:** seed_fill_frame

```python
def solve_medium_p05(g):
    h,w=dims(g)
    out=blank(h,w)
    frames, others = find_rectangular_frames(g)
    # preserve frames
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
        r0,c0,r1,c1=fr['bbox']
        # find unique seed inside bbox excluding frame color, from original grid
        seed=0
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0 and g[r][c]!=fr['color']:
                    seed=g[r][c]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=seed
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 1 0 0 1 0 0 0 0 0
0 1 3 0 1 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 6 0 0 6 0 0
0 0 0 0 6 0 4 6 0 0
0 0 0 0 6 6 6 6 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 1 3 3 1 0 0 0 0 0
0 1 3 3 1 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 6 4 4 6 0 0
0 0 0 0 6 4 4 6 0 0
0 0 0 0 6 6 6 6 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0 0
0 5 2 0 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 8 0 7
0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 8 8 8 7
0 0 0 0 0 0 7 8 8 8 7
0 0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 0 0 3 0 0 0 0
0 3 6 0 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0
0 0 0 0 4 0 0 4 0
0 0 0 0 4 0 5 4 0
0 0 0 0 4 4 4 4 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0
0 3 6 6 3 0 0 0 0
0 3 6 6 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0
0 0 0 0 4 5 5 4 0
0 0 0 0 4 5 5 4 0
0 0 0 0 4 4 4 4 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0 0
0 6 2 0 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 8 3 0 0
0 0 0 0 3 3 3 3 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 2 2 6 0 0 0 0 0
0 6 2 2 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 8 8 3 0 0
0 0 0 0 3 8 8 3 0 0
0 0 0 0 3 3 3 3 0 0
```

### medium_p06 — Bottom-pack all objects in order

**Written rule:** Crop each object and place the crops side by side in left-to-right object order, bottom-aligned, with one blank column between pieces.

**Program function:** `solve_medium_p06`

**Primitives:** bottom_pack_gallery

```python
def solve_medium_p06(g):
    comps=components_by_color(g)
    comps.sort(key=lambda comp: min(c for r,c in comp['cells']))
    pieces=[]
    maxh=0
    totalw=0
    for comp in comps:
        crop,_=crop_component(g, comp['cells'])
        pieces.append(crop)
        ph,pw=dims(crop)
        maxh=max(maxh,ph)
        totalw += pw
    totalw += max(0,len(pieces)-1)
    out=blank(maxh,totalw)
    c=0
    for p in pieces:
        ph,pw=dims(p)
        top=maxh-ph
        for i in range(ph):
            for j in range(pw):
                out[top+i][c+j]=p[i][j]
        c += pw + 1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 0 0
0 0 2 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 5 5 0 4 4
0 2 0 0 5 0 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
7 7 0 0 0 0 3 3 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0
```

**Train 2 output**
```text
7 0 0 5 5 0 3 3
7 7 0 0 5 0 0 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 5 0 0
```

**Train 3 output**
```text
2 0 0 8 8 0 5 5
2 2 0 0 8 0 0 5
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 5 5 0 0
0 0 3 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
3 3 0 7 7 0 5 5
0 3 0 0 7 0 0 5
```

### medium_p07 — Overlay two normalized objects

**Written rule:** Take the two objects, normalize both to their own top-left corners, overlay them on one canvas, and color overlaps with 8.

**Program function:** `solve_medium_p07`

**Primitives:** normalized_overlay

```python
def solve_medium_p07(g):
    comps=components_by_color(g)
    assert len(comps)==2
    pieces=[]
    cols=[]
    maxh=maxw=0
    for comp in comps:
        occ,(h,w)=normalize_occupancy(comp['cells'])
        pieces.append(occ); cols.append(comp['color']); maxh=max(maxh,h); maxw=max(maxw,w)
    out=blank(maxh,maxw)
    for idx,occ in enumerate(pieces):
        for r,c in occ:
            if out[r][c]==0:
                out[r][c]=cols[idx]
            else:
                out[r][c]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8
0 8
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 6
8 5
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8
9 7
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 0
0 8 2
```

## Hard (7)

### hard_p01 — Build a transform gallery from a script row

**Written rule:** Read the top-row transform codes, apply each transform to the base object below, and output the transformed crops as a left-to-right gallery.

**Program function:** `solve_hard_p01`

**Primitives:** script_transform_gallery

```python
def solve_hard_p01(g):
    codes=[v for v in g[0] if v!=0]
    base=crop_nonzero(g[2:]) if len(g)>2 else [[0]]
    pieces=[]
    totalw=0
    maxh=0
    for code in codes:
        p=TRANSFORM_CODES[code](base)
        pieces.append(p)
        ph,pw=dims(p)
        totalw += pw
        maxh=max(maxh,ph)
    totalw += max(0,len(pieces)-1)
    out=blank(maxh,totalw)
    c=0
    for p in pieces:
        ph,pw=dims(p)
        for r in range(ph):
            for j in range(pw):
                out[r][c+j]=p[r][j]
        c += pw + 1
    return out
```

**Train 1 input**
```text
4 1 2 0 0
0 0 0 0 0
0 2 3 0 0
0 0 3 0 0
0 3 3 0 0
```

**Train 1 output**
```text
3 2 0 3 0 2 0 3 3
3 0 0 3 3 3 0 3 0
3 3 0 0 0 0 0 3 2
```

**Train 2 input**
```text
3 5 1 0 0
0 0 0 0 0
4 4 0 0 0
0 4 0 0 0
0 4 7 0 0
```

**Train 2 output**
```text
0 0 7 0 0 4 7 0 0 0 4
4 4 4 0 0 4 0 0 4 4 4
4 0 0 0 4 4 0 0 7 0 0
```

**Train 3 input**
```text
2 4 1 3 0
0 0 0 0 0
0 5 5 0 0
0 0 5 0 0
0 0 6 0 0
```

**Train 3 output**
```text
6 0 0 5 5 0 0 0 5 0 5 5 6
5 0 0 5 0 0 6 5 5 0 5 0 0
5 5 0 6 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
5 1 4 2 0
0 0 0 0 0
0 6 7 0 0
0 0 7 0 0
0 7 7 0 0
```

**Test 1 output**
```text
7 7 0 7 0 6 0 7 6 0 7 7
0 7 0 7 7 7 0 7 0 0 7 0
6 7 0 0 0 0 0 7 7 0 7 6
```

### hard_p02 — Route the shortest path through portals

**Written rule:** Draw the shortest 4-connected path from 2 to 3 through empty cells, treating equal-colored portal pairs as teleports; color only the traversed empty cells 8.

**Program function:** `solve_hard_p02`

**Primitives:** portal_bfs

```python
def solve_hard_p02(g):
    h,w=dims(g)
    start=goal=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            elif g[r][c]==3: goal=(r,c)
    pairs=portal_pairs(g)
    portal_lookup={}
    for color,(a,b) in pairs.items():
        portal_lookup[a]=b
        portal_lookup[b]=a
    def neighbors(pos):
        r,c=pos
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc]!=1:
                nxt=(nr,nc)
                if g[nr][nc] >= 4 and nxt in portal_lookup:
                    yield portal_lookup[nxt], nxt  # state position after teleport, stepped portal cell
                else:
                    yield nxt, nxt
    prev={start:(None,None)}  # state -> (prev_state, stepped_cell_before_tp)
    dq=deque([start])
    while dq:
        cur=dq.popleft()
        if cur==goal:
            break
        for nxt, stepped in neighbors(cur):
            if nxt not in prev:
                prev[nxt]=(cur, stepped)
                dq.append(nxt)
    if goal not in prev:
        return copy_grid(g)
    path_states=[]
    cur=goal
    while cur is not None:
        path_states.append(cur)
        cur=prev[cur][0]
    path_states=path_states[::-1]
    out=copy_grid(g)
    # reconstruct traversed cells including intermediate stepped portal cells
    cur=goal
    traversed=[]
    while cur!=start:
        prv, stepped=prev[cur]
        if stepped is not None:
            traversed.append(stepped)
        cur=prv
    traversed.append(start)
    traversed=set(traversed+[goal])
    for r,c in traversed:
        if out[r][c]==0:
            out[r][c]=8
    return out
```

**Train 1 input**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 4 1 1 1 1 1
1 0 1 1 0 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 1
1 1 1 1 1 1 1 4 0 3 1
1 1 1 1 1 1 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1
```

**Train 1 output**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 8 8 8 4 1 1 1 1 1
1 0 1 1 0 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 1
1 1 1 1 1 1 1 4 8 3 1
1 1 1 1 1 1 1 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1
```

**Train 2 input**
```text
1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 4 0 0 0 1
1 1 1 1 0 1 1 1 0 1
1 0 0 0 0 1 0 0 0 1
1 0 1 1 1 1 0 1 0 1
1 0 4 0 0 0 0 3 0 1
1 1 1 1 1 1 1 1 1 1
```

**Train 2 output**
```text
1 1 1 1 1 1 1 1 1 1
1 2 8 8 8 4 0 0 0 1
1 1 1 1 0 1 1 1 0 1
1 0 0 0 0 1 0 0 0 1
1 0 1 1 1 1 0 1 0 1
1 0 4 8 8 8 8 3 0 1
1 1 1 1 1 1 1 1 1 1
```

**Train 3 input**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 0 4 1 1 1 1
1 0 1 1 1 0 1 1 1 1 1
1 0 0 0 1 0 1 1 1 1 1
1 1 1 0 1 0 1 1 1 1 1
1 1 1 0 1 4 0 0 0 3 1
1 1 1 1 1 1 1 1 1 1 1
```

**Train 3 output**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 8 8 8 8 4 1 1 1 1
1 0 1 1 1 0 1 1 1 1 1
1 0 0 0 1 0 1 1 1 1 1
1 1 1 0 1 0 1 1 1 1 1
1 1 1 0 1 4 8 8 8 3 1
1 1 1 1 1 1 1 1 1 1 1
```

**Test 1 input**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 4 0 0 0 0 1
1 1 1 1 0 1 1 1 0 0 1
1 0 0 0 0 1 0 0 0 0 1
1 0 1 1 1 1 0 1 1 1 1
1 0 4 0 0 0 0 0 0 3 1
1 1 1 1 1 1 1 1 1 1 1
```

**Test 1 output**
```text
1 1 1 1 1 1 1 1 1 1 1
1 2 8 8 8 4 0 0 0 0 1
1 1 1 1 0 1 1 1 0 0 1
1 0 0 0 0 1 0 0 0 0 1
1 0 1 1 1 1 0 1 1 1 1
1 0 4 8 8 8 8 8 8 3 1
1 1 1 1 1 1 1 1 1 1 1
```

### hard_p03 — Assign solid objects to frames by area rank

**Written rule:** Sort the solid objects by area and the hollow frames by interior area; center the smallest object in the smallest frame, the next in the next, and so on.

**Program function:** `solve_hard_p03`

**Primitives:** area_rank_frame_assignment

```python
def solve_hard_p03(g):
    h,w=dims(g)
    frames, others = find_rectangular_frames(g)
    # solids are non-frame components
    solids=others
    solids.sort(key=lambda comp: len(comp['cells']))
    frames.sort(key=lambda fr: (fr['bbox'][2]-fr['bbox'][0]-1)*(fr['bbox'][3]-fr['bbox'][1]-1))
    out=blank(h,w)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    for comp, fr in zip(solids, frames):
        crop,_=crop_component(g, comp['cells'])
        ph,pw=dims(crop)
        r0,c0,r1,c1=fr['bbox']
        ih,iw=r1-r0-1,c1-c0-1
        top=r0+1 + (ih-ph)//2
        left=c0+1 + (iw-pw)//2
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    out[top+i][left+j]=crop[i][j]
    return out
```

**Train 1 input**
```text
2 2 0 0 0 0 0 5 5 5 0 0
0 2 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 7 0 0 7 0 0
0 0 0 0 0 0 7 0 0 7 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 8 0 8
0 0 0 0 0 0 0 0 0 8 8 8
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 5 5 5 7 0 0
0 0 0 0 0 0 7 5 5 7 0 0
0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 2 8
0 0 0 0 0 0 0 0 0 8 2 8
0 0 0 0 0 0 0 0 0 8 8 8
```

**Train 2 input**
```text
2 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 7 0 7 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 8 8 8 8 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 7 2 7 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 8 5 5 8 0 0
0 0 0 0 0 0 8 5 5 8 0 0
0 0 0 0 0 0 8 8 8 8 0 0
```

**Train 3 input**
```text
2 2 0 0 0 0 0 0 0 5 5 5 0
0 2 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 7 0 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 7 0 0 0 0 0 0 0
0 0 0 7 2 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 8 0 0 0
0 0 0 0 0 0 5 5 5 8 0 0 0
0 0 0 0 0 0 8 5 8 8 0 0 0
```

**Test 1 input**
```text
2 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 7 0 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 7 2 7 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 5 5 8 0 0 0
0 0 0 0 0 0 8 5 5 8 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```

### hard_p04 — Find the dihedral match and stamp it at anchors

**Written rule:** Identify which candidate shape matches the guide up to rotation or reflection, then stamp that matching candidate shape at every anchor cell.

**Program function:** `solve_hard_p04`

**Primitives:** dihedral_match_stamp

```python
def solve_hard_p04(g):
    h,w=dims(g)
    comps=components_by_color(g)
    guide=None
    anchors=[]
    candidates=[]
    for comp in comps:
        if comp['color']==2:
            guide=comp
        elif comp['color']==9:
            anchors.extend(comp['cells'])
        else:
            candidates.append(comp)
    guide_occ,_=normalize_occupancy(guide['cells'])
    guide_variants=set(dihedral_variants_occ(guide_occ))
    chosen=None
    for comp in candidates:
        occ,_=normalize_occupancy(comp['cells'])
        if frozenset(occ) in guide_variants:
            chosen=comp; break
    crop,_=crop_component(g, chosen['cells'])
    ph,pw=dims(crop)
    out=blank(h,w)
    for ar,ac in anchors:
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    rr,cc=ar+i, ac+j
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=chosen['color']
    return out
```

**Train 1 input**
```text
2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 3 3 3 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 5 5 0 0
0 0 5 0 0 0 5 0 0 0
```

**Train 2 input**
```text
2 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 4 4
0 0 4 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 9 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 4 4 0 0
0 0 0 4 4 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
2 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 9 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 5 0
0 5 5 0 0 0 0 0 0 5 5
```

### hard_p05 — Copy a template using a marker-to-marker offset

**Written rule:** Measure the template’s offset from the 2-marker and copy the same template at the same offset relative to the 3-marker.

**Program function:** `solve_hard_p05`

**Primitives:** relative_offset_copy

```python
def solve_hard_p05(g):
    h,w=dims(g)
    ref=target=None
    template_cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: ref=(r,c)
            elif g[r][c]==3: target=(r,c)
    # template is all nonzero cells except markers 2,3
    template_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c] not in (2,3)]
    r0,c0,r1,c1=bbox(template_cells)
    top_offset=(r0-ref[0], c0-ref[1])
    crop=[row[c0:c1+1] for row in g[r0:r1+1]]
    new_top=target[0]+top_offset[0]
    new_left=target[1]+top_offset[1]
    out=copy_grid(g)
    for i,row in enumerate(crop):
        for j,v in enumerate(row):
            if v!=0:
                rr,cc=new_top+i,new_left+j
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 4 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 0 4 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 4 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 2 0 6 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 0 0 3 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 0 0 3 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 4 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### hard_p06 — Recolor objects by contact degree after dilation

**Written rule:** Treat two objects as adjacent if their one-step Manhattan dilations touch; recolor every object according to how many neighbors it has in that contact graph.

**Program function:** `solve_hard_p06`

**Primitives:** contact_degree

```python
def solve_hard_p06(g):
    comps=components_by_color(g)
    # any nonzero components, graph edge if min manhattan distance <= 2
    n=len(comps)
    deg=[0]*n
    cell_sets=[comp['cells'] for comp in comps]
    for i,j in combinations(range(n),2):
        touch=False
        for r1,c1 in cell_sets[i]:
            for r2,c2 in cell_sets[j]:
                if abs(r1-r2)+abs(c1-c2)<=2:
                    touch=True; break
            if touch: break
        if touch:
            deg[i]+=1; deg[j]+=1
    palette={0:2,1:3,2:4,3:5,4:6,5:7}
    h,w=dims(g)
    out=blank(h,w)
    for comp,d in zip(comps,deg):
        col=palette.get(d,7)
        for r,c in comp['cells']:
            out[r][c]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 0 3 0 4 0
0 0 0 0 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
0 6 0 0 0 0 7
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 3 0 5 0 3 0
0 0 0 0 0 0 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
0 2 0 0 0 0 2
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 3 3 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 3 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 3 0 5 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
```

### hard_p07 — Dock color-matched objects at crosshair targets

**Written rule:** For each object color, use the matching top-row and left-column markers as a crosshair target, then move that object so its crop is centered on the crosshair intersection.

**Program function:** `solve_hard_p07`

**Primitives:** color_crosshair_dock

```python
def solve_hard_p07(g):
    h,w=dims(g)
    # objects are nonzero comps excluding top row and left column markers
    row_markers={}
    col_markers={}
    for r in range(1,h):
        if g[r][0]!=0:
            row_markers[g[r][0]]=r
    for c in range(1,w):
        if g[0][c]!=0:
            col_markers[g[0][c]]=c
    comps=components_by_color(g)
    out=blank(h,w)
    for comp in comps:
        col=comp['color']
        # skip border markers singletons on top row or left col
        cells=comp['cells']
        if all(r==0 or c==0 for r,c in cells):
            continue
        crop,_=crop_component(g, cells)
        ph,pw=dims(crop)
        cr=row_markers[col]
        cc=col_markers[col]
        top=cr - ph//2
        left=cc - pw//2
        for i in range(ph):
            for j in range(pw):
                if crop[i][j]!=0:
                    rr,cc2=top+i,left+j
                    if 0<=rr<h and 0<=cc2<w:
                        out[rr][cc2]=crop[i][j]
    return out
```

**Train 1 input**
```text
0 0 0 2 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
4 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 2 0 0 0 6 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
6 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 3 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

