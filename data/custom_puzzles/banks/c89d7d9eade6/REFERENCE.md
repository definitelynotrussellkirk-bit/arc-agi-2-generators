# ARC Puzzle Bank — Set 15
This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

This batch pushes into a more varied slice of the space: run medians, diagonal consensus, beamcasting, row-frequency filters, matrix echoes, object summarization, galleries, border-based recoloring, duplicate-shape filtering, keyed transforms, selection-transform-insert composition, overlayed beam systems, multi-key pathfinding, blueprint reconstruction, guide-based stamping, keyed Boolean shape algebra, and mirror raytracing.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set15.json` — machine-readable task data
- `arc_puzzle_bank_21_set15_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set15_validation.txt` — validation log

## Easy (7)

### easy_o01 — Keep only the median of each odd horizontal run

**Written rule:** For each contiguous odd-length horizontal run of a nonzero color, erase the run except for its central cell.

**Program function:** `solve_easy_o01`

**Primitives:** odd_run_median

```python
def solve_easy_o01(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            col=g[r][c]
            c2=c
            while c2<w and g[r][c2]==col:
                c2+=1
            L=c2-c
            if L%2==1:
                out[r][c+L//2]=col
            c=c2
    return out
```

**Train 1 input**
```text
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 9 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 4
5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0
5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
```

**Test 1 input**
```text
0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
```

### easy_o02 — Fill centers agreed on by four diagonal neighbors

**Written rule:** Whenever a zero cell has the same nonzero color on all four diagonals around it, fill the center with that color.

**Program function:** `solve_easy_o02`

**Primitives:** diagonal_consensus_fill

```python
def solve_easy_o02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: 
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and vals.count(vals[0])==4:
                out[r][c]=vals[0]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 5
0 0 2 0 2 0 0 0
0 0 0 0 0 5 0 5
0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 5 0 5
0 0 2 0 2 0 5 0
0 0 0 2 0 5 0 5
0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0
0 8 0 8 0 0 0
0 0 0 0 0 0 0
0 8 0 8 4 0 4
0 0 0 0 0 0 0
0 0 0 0 4 0 4
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 8 0 8 0 0 0
0 0 8 0 0 0 0
0 8 0 8 4 0 4
0 0 0 0 0 4 0
0 0 0 0 4 0 4
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 6 0 6 0 0 0 0 0
0 0 0 0 0 3 0 3 0
0 6 0 6 0 0 0 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 6 0 6 0 0 0 0 0
0 0 6 0 0 3 0 3 0
0 6 0 6 0 0 3 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 2 0 2 0
0 7 0 7 0 0 0 0 0
0 0 0 0 0 2 0 2 0
0 7 0 7 0 5 0 5 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 5 0
```

**Test 1 output**
```text
0 0 0 0 0 2 0 2 0
0 7 0 7 0 0 2 0 0
0 0 7 0 0 2 0 2 0
0 7 0 7 0 5 0 5 0
0 0 0 0 0 0 5 0 0
0 0 0 0 0 5 0 5 0
```

### easy_o03 — Emit horizontal beams from every seed

**Written rule:** Every nonzero cell sends its color left and right through zeros until the beam hits the grid edge or an original nonzero blocker.

**Program function:** `solve_easy_o03`

**Primitives:** horizontal_beam

```python
def solve_easy_o03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0: 
                continue
            # left
            cc=c-1
            while cc>=0 and g[r][cc]==0:
                out[r][cc]=col
                cc-=1
            cc=c+1
            while cc<w and g[r][cc]==0:
                out[r][cc]=col
                cc+=1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 6 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
2 2 2 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3
6 6 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 7 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
```

**Train 2 output**
```text
7 7 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
4 4 4 4 8 8 8 8 8
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
9 9 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0
4 4 4 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
7 7 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0
```

### easy_o04 — Keep only colors that appear once in a row

**Written rule:** Within each row, keep cells whose color appears exactly once in that row, and erase colors that repeat in that row.

**Program function:** `solve_easy_o04`

**Primitives:** row_singleton_filter

```python
def solve_easy_o04(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        cnt=Counter(v for v in row if v!=0)
        for c,v in enumerate(row):
            if v!=0 and cnt[v]==1:
                out[r][c]=v
    return out
```

**Train 1 input**
```text
0 2 0 2 0 0 5 0 0
0 0 0 0 0 0 0 0 0
4 0 0 0 7 0 0 0 4
0 0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 3 0
0 9 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 9 0 0 0 0 0 0 0
```

**Train 2 input**
```text
1 0 0 0 0 1 0 0 4 0
0 0 3 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 7 0 0 7 0 2
0 0 0 8 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 4 0
0 0 3 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 8 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 6 0 0 0 6 4
0 0 0 0 0 0 0 0
0 5 0 5 0 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 2 0 0 2
0 0 0 0 0 0 3 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
```

**Test 1 input**
```text
0 4 0 0 0 0 0 4 6
0 0 0 0 0 0 0 0 0
5 0 0 2 0 5 0 0 0
0 0 7 0 7 0 0 0 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0
```

### easy_o05 — Echo the upper triangle below the main diagonal

**Written rule:** Copy the content above the main diagonal to the mirrored positions below it, keeping the upper triangle and diagonal unchanged.

**Program function:** `solve_easy_o05`

**Primitives:** upper_triangle_echo

```python
def solve_easy_o05(g):
    h,w=dims(g)
    assert h==w
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if r>c:
                out[r][c]=g[c][r]
    return out
```

**Train 1 input**
```text
0 0 4 0 0 7
0 0 0 2 5 0
0 0 6 0 3 0
0 0 0 0 0 8
0 0 0 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 4 0 0 7
0 0 0 2 5 0
4 0 6 0 3 0
0 2 0 0 0 8
0 5 3 0 0 0
7 0 0 8 0 0
```

**Train 2 input**
```text
0 9 0 0 2
0 0 4 0 0
0 0 0 7 0
0 0 0 5 0
0 0 0 0 0
```

**Train 2 output**
```text
0 9 0 0 2
9 0 4 0 0
0 4 0 7 0
0 0 7 5 0
2 0 0 0 0
```

**Train 3 input**
```text
0 0 0 1 0 0 6
0 0 0 0 0 4 0
0 0 0 0 8 0 0
0 0 0 2 0 0 0
0 0 0 0 0 0 9
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 1 0 0 6
0 0 0 0 0 4 0
0 0 0 0 8 0 0
1 0 0 2 0 0 0
0 0 8 0 0 0 9
0 4 0 0 0 0 0
6 0 0 0 9 0 0
```

**Test 1 input**
```text
0 0 0 0 3 0
0 5 0 0 0 7
0 0 0 6 0 0
0 0 0 0 2 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 3 0
0 5 0 0 0 7
0 0 0 6 0 0
0 0 6 0 2 0
3 0 0 2 0 0
0 7 0 0 0 0
```

### easy_o06 — Complete each 2x2 missing corner

**Written rule:** If a 2x2 block contains three cells of the same nonzero color and one empty corner, fill the missing corner with that same color.

**Program function:** `solve_easy_o06`

**Primitives:** missing_corner_completion

```python
def solve_easy_o06(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                col=nz[0]
                if vals[0]==0: out[r][c]=col
                if vals[1]==0: out[r][c+1]=col
                if vals[2]==0: out[r+1][c]=col
                if vals[3]==0: out[r+1][c+1]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 3 0 0
0 2 2 0 3 3 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0
0 0 0 0 0 0 4 0
```

**Train 1 output**
```text
0 0 0 0 3 3 0 0
0 2 2 0 3 3 0 0
0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0
0 0 0 0 0 4 4 0
```

**Train 2 input**
```text
0 5 5 0 0 0 0
0 5 0 0 0 0 0
0 0 0 6 6 0 0
0 0 0 0 6 0 0
8 0 0 0 0 0 0
8 8 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 5 5 0 0 0 0
0 5 5 0 0 0 0
0 0 0 6 6 0 0
0 0 0 6 6 0 0
8 8 0 0 0 0 0
8 8 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 7 7 0 0 0
0 0 0 0 0 7 0 9 0
0 1 1 0 0 0 9 9 0
0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 7 7 0 0 0
0 0 0 0 7 7 9 9 0
0 1 1 0 0 0 9 9 0
0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 6 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 4 0
0 2 0 0 0 0 4 4
2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 6 6 0 0 0 0
0 0 6 6 0 0 0 0
0 0 0 0 0 0 4 4
2 2 0 0 0 0 4 4
2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

### easy_o07 — Turn vertical trios into horizontal trios

**Written rule:** Replace each isolated vertical run of exactly three same-colored cells by a horizontal run of three centered on the original middle cell.

**Program function:** `solve_easy_o07`

**Primitives:** vertical_trio_rotate

```python
def solve_easy_o07(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==0:
                r+=1; continue
            col=g[r][c]
            r2=r
            while r2<h and g[r2][c]==col:
                r2+=1
            if r2-r==3:
                mr=r+1
                if 0< c < w-1:
                    out[mr][c-1]=out[mr][c]=out[mr][c+1]=col
            r=r2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 2 0 0 0 5 0 0
0 0 2 0 8 0 5 0 0
0 0 0 0 8 0 5 0 0
0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 0 0 0 5 5 5 0
0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 3 0 0 0 0 0
0 6 0 0 3 0 0 0 0 0
0 6 0 0 3 0 0 7 0 0
0 6 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0
0 0 0 0 0 9 0 0
0 0 4 0 0 9 0 0
0 0 4 0 0 0 1 0
0 0 4 0 0 0 1 0
0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 2 0 0
0 7 0 0 0 0 2 0 0
0 7 0 5 0 0 2 0 0
0 7 0 5 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0
7 7 7 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

## Medium (7)

### medium_o01 — Mark each object with its bounding-box center

**Written rule:** For every connected object, erase the object and keep only one cell at the center of its tight bounding box, using the same color.

**Program function:** `solve_medium_o01`

**Primitives:** bbox_centers

```python
def solve_medium_o01(g):
    out=blank(*dims(g))
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        cr=(r0+r1)//2; cc=(c0+c1)//2
        out[cr][cc]=comp['color']
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 4 4 0
0 2 2 0 0 0 0 4 0 0
0 0 2 0 0 0 0 4 4 4
0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0
3 3 0 0 0 0 8 0 0 0 0
3 3 3 0 0 0 8 0 0 0 0
0 0 3 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 7 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0
0 0 1 1 0 0 0 9 0 0
0 0 1 1 1 0 0 9 9 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 6 6 6 0
0 0 4 4 4 0 0 0 0 6 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

### medium_o02 — Sort cropped objects by area into a gallery

**Written rule:** Crop each object tightly, sort the crops by descending area, and place them left-to-right with one empty column between neighboring crops.

**Program function:** `solve_medium_o02`

**Primitives:** area_sorted_gallery

```python
def solve_medium_o02(g):
    comps=find_components(g)
    items=[]
    for comp in comps:
        crop=crop_bbox(g, comp['cells'])
        items.append((comp['area'], comp['bbox'][1], comp['bbox'][0], comp['color'], crop))
    items.sort(key=lambda x:(-x[0], x[1], x[2], x[3]))
    height=max(len(crop) for *_,crop in items)
    width=sum(len(crop[0]) for *_,crop in items)+max(0,len(items)-1)
    out=blank(height,width)
    cur=0
    for *_,crop in items:
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                if v!=0: out[r][cur+c]=v
        cur+=len(crop[0])+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 5 5 0 0 0 0 0 0
0 2 2 0 0 0 0 5 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
7 7 0 0 2 2 0 5 5
7 7 7 0 2 2 0 0 5
0 0 7 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
3 3 3 0 0 8 8 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 6 6 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 3 0 8 8 0 6 6
0 3 0 0 8 8 0 0 6
0 3 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 4 0 0 9 9 0 1 1 1
4 4 4 0 9 9 0 0 0 0
0 0 4 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 2 2 0 0 0 7 7 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 6 0 7 7 0 2 2
0 6 0 0 7 7 0 0 2
0 6 0 0 0 0 0 0 0
```

### medium_o03 — Recolor objects by the nearest border

**Written rule:** Recolor each object according to which outer border is uniquely nearest to its bounding box: top→1, bottom→2, left→3, right→4.

**Program function:** `solve_medium_o03`

**Primitives:** nearest_border_label

```python
def solve_medium_o03(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        dists=[r0, h-1-r1, c0, w-1-c1] # top,bottom,left,right
        k=min(range(4), key=lambda i:dists[i])
        if dists.count(dists[k])!=1:
            # skip ambiguous by keeping original color? but examples unique
            new=comp['color']
        else:
            new=[1,2,3,4][k]
        for r,c in comp['cells']:
            out[r][c]=new
    return out
```

**Train 1 input**
```text
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0 6 6 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 9 9 0
3 3 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 4 4 0
3 3 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
```

**Train 3 input**
```text
0 2 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0
7 7 0 0 0 0 0 0 5 5 0
7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
```

**Train 3 output**
```text
0 1 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0
3 3 0 0 0 0 0 0 4 4 0
3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 5 5 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 4 4 0
0 0 0 2 2 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0
```

### medium_o04 — Build a bar chart from object areas

**Written rule:** Treat each object area as a bar height. Order objects from left to right as in the input, and output one bottom-aligned colored bar per object with empty separator columns.

**Program function:** `solve_medium_o04`

**Primitives:** area_bar_chart

```python
def solve_medium_o04(g):
    comps=sorted(find_components(g), key=lambda comp:(comp['bbox'][1], comp['bbox'][0], comp['color']))
    heights=[comp['area'] for comp in comps]
    H=max(heights)
    W=2*len(comps)-1
    out=blank(H,W)
    for i,comp in enumerate(comps):
        col=comp['color']; hgt=comp['area']; c=2*i
        for r in range(H-hgt,H):
            out[r][c]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 4 4 0 0
0 2 2 0 0 0 0 0 4 4 4 0
0 2 2 0 0 6 6 0 0 0 4 0
0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 4
0 0 0 0 4
2 0 0 0 4
2 0 6 0 4
2 0 6 0 4
2 0 6 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0 0 0 0 0
5 5 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 3
0 0 7 0 3
5 0 7 0 3
5 0 7 0 3
5 0 7 0 3
```

**Train 3 input**
```text
0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 1 0 0
0 0 1 0 0
0 0 1 0 9
8 0 1 0 9
8 0 1 0 9
8 0 1 0 9
```

**Test 1 input**
```text
0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 0 0 0 0
6 0 0 0 4
6 0 2 0 4
6 0 2 0 4
6 0 2 0 4
```

### medium_o05 — Mirror each object inside its own box

**Written rule:** Reflect every connected object horizontally inside its own tight bounding box, leaving the object in the same box but mirrored left-to-right.

**Program function:** `solve_medium_o05`

**Primitives:** in_bbox_mirror_h

```python
def solve_medium_o05(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in find_components(g):
        r0,c0,r1,c1=comp['bbox']
        crop=crop_bbox(g, comp['cells'])
        fc=flip_h(crop)
        for r,row in enumerate(fc):
            for c,v in enumerate(row):
                if v!=0: out[r0+r][c0+c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_o06 — Keep only translated duplicates of a shape

**Written rule:** Normalize each object by translation only. Keep objects whose exact normalized shape appears at least twice, and erase unique shapes.

**Program function:** `solve_medium_o06`

**Primitives:** duplicate_shape_filter

```python
def solve_medium_o06(g):
    comps=find_components(g)
    sigs=[normalize_shape(comp['cells']) for comp in comps]
    cnt=Counter(sigs)
    h,w=dims(g); out=blank(h,w)
    for comp,sig in zip(comps,sigs):
        if cnt[sig]>=2:
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 5 5 0 0 0 0 0
0 2 2 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 5 5 0 0 0 0 0
0 2 2 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 1 1 0 0
0 0 4 4 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 2 2 0 0 0 0 0 0 0
7 7 0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 2 2 0 0 0 0 0 0 0
7 7 0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_o07 — A corner key chooses how to transform the object crop

**Written rule:** Read the color in the top-left corner as a key: 1=rotate 90° clockwise, 2=flip horizontally, 3=flip vertically. Apply that transform to the single main object and output its tight crop.

**Program function:** `solve_medium_o07`

**Primitives:** corner_key_transform_crop

```python
def solve_medium_o07(g):
    key=g[0][0]
    comps=find_components(g, ignore_colors={key})
    # But marker cell at (0,0) might connect to nothing due corner. Better ignore exact cell.
    # easiest: pick largest component excluding (0,0)
    best=None
    for comp in find_components([[0 if (r==0 and c==0) else g[r][c] for c in range(len(g[0]))] for r in range(len(g))]):
        if best is None or comp['area']>best['area']:
            best=comp
    crop=crop_bbox(g, best['cells'])
    if key==1: out=rotate90(crop)
    elif key==2: out=flip_h(crop)
    elif key==3: out=flip_v(crop)
    else: out=[row[:] for row in crop]
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
6 6 6
6 0 6
6 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 4 4
0 4 0
4 4 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0
0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 7
7 7 7
7 7 0
```

**Test 1 input**
```text
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 5
5 5 5
5 0 0
```

## Hard (7)

### hard_o01 — Select one object, transform it, and center it inside the frame

**Written rule:** Use the nonzero top-row selector color to choose which object to keep. Use the top-left key to transform that object, then center the transformed crop inside the hollow frame and erase everything else.

**Program function:** `solve_hard_o01`

**Primitives:** select_transform_insert

```python
def solve_hard_o01(g):
    h,w=dims(g)
    key=g[0][0]
    selector=None
    # top row excluding 0 and frame color and key; choose rightmost nonzero maybe
    for c,v in enumerate(g[0]):
        if c==0: continue
        if v!=0:
            selector=v
    # frame color 8
    frames=scan_frames(g,8)
    frame=max(frames, key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    # components excluding frame color and selector cells/key row? exclude top row markers
    temp=copy_grid(g)
    temp[0][0]=0
    for c in range(w):
        if g[0][c]==selector:
            temp[0][c]=0
    # remove frame border
    r0,c0,r1,c1=frame['bbox']
    for c in range(c0,c1+1):
        temp[r0][c]=0; temp[r1][c]=0
    for r in range(r0,r1+1):
        temp[r][c0]=0; temp[r][c1]=0
    comps=find_components(temp)
    target=max([comp for comp in comps if comp['color']==selector], key=lambda comp: comp['area'])
    crop=crop_bbox(temp, target['cells'])
    crop=transform_by_key(crop, key)
    out=blank(h,w)
    # keep frame
    for c in range(c0,c1+1):
        out[r0][c]=out[r1][c]=8
    for r in range(r0,r1+1):
        out[r][c0]=out[r][c1]=8
    center_paste(out, crop, frame['bbox'])
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 4 4 0 0 0 0 8 0 0 0 0 0 8
0 4 0 0 0 0 0 8 0 0 0 0 0 8
0 4 4 4 0 0 0 8 0 0 0 0 0 8
0 0 6 6 0 0 0 8 0 0 0 0 0 8
0 0 0 6 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 4 4 4 0 8
0 0 0 0 0 0 0 8 0 4 0 4 0 8
0 0 0 0 0 0 0 8 0 4 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 8 8 8 8 8 8 8
0 0 6 6 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 5 5 0 0 8 0 0 0 0 0 8
0 0 0 0 0 5 0 0 8 0 0 0 0 0 8
0 4 4 0 0 0 0 0 8 0 0 0 0 0 8
0 4 4 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 6 6 0 8
0 0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 0 8 0 6 6 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 5 5 0 0 0 0 0 0 8 0 0 0 0 8
0 5 5 5 0 0 0 0 0 8 0 0 0 0 8
0 0 0 5 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 4 4 0 0 8 0 0 0 0 8
0 0 0 0 0 0 4 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 5 0 8
0 0 0 0 0 0 0 0 0 8 5 5 5 0 8
0 0 0 0 0 0 0 0 0 8 5 5 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 6 6 0 0 0 0 0 0 8 0 0 0 0 8
0 0 6 0 0 0 0 0 0 8 0 0 0 0 8
0 0 6 6 0 4 4 0 0 8 0 0 0 0 8
0 0 0 0 0 0 4 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 6 0 8
0 0 0 0 0 0 0 0 0 8 6 6 6 0 8
0 0 0 0 0 0 0 0 0 8 6 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_o02 — Combine horizontal and vertical beam systems

**Written rule:** Color-2 emitters send horizontal beams through zeros, color-3 emitters send vertical beams through zeros, blockers stop beams, and cells reached by both beam families become color 4.

**Program function:** `solve_hard_o02`

**Primitives:** orthogonal_beam_overlay

```python
def solve_hard_o02(g):
    h,w=dims(g)
    out=copy_grid(g)
    horiz=set()
    vert=set()
    blockers={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,2,3)}
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                cc=c-1
                while cc>=0 and g[r][cc]==0:
                    horiz.add((r,cc)); cc-=1
                cc=c+1
                while cc<w and g[r][cc]==0:
                    horiz.add((r,cc)); cc+=1
            elif g[r][c]==3:
                rr=r-1
                while rr>=0 and g[rr][c]==0:
                    vert.add((rr,c)); rr-=1
                rr=r+1
                while rr<h and g[rr][c]==0:
                    vert.add((rr,c)); rr+=1
    for cell in horiz|vert:
        if cell in blockers: 
            continue
        if cell in horiz and cell in vert: out[cell[0]][cell[1]]=4
        elif cell in horiz: out[cell[0]][cell[1]]=2
        elif cell in vert: out[cell[0]][cell[1]]=3
    return out
```

**Train 1 input**
```text
0 0 0 0 3 0 0 0 0 0
0 2 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 3 0 0 3 0 0
2 2 2 2 4 2 2 4 6 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 0 3 0 0
0 0 0 0 3 0 0 3 0 0
2 2 2 2 4 2 2 4 2 2
0 0 0 0 6 0 0 3 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 3 0 3 0 0
2 2 2 2 2 2 4 2 4 6 0
0 0 0 0 0 0 3 0 3 0 0
2 2 2 2 2 2 4 2 4 2 2
0 0 0 0 0 0 6 0 3 0 0
0 0 0 0 0 0 0 0 3 0 0
```

**Train 3 input**
```text
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 2 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 3 0 0 0 3 0 0
2 2 2 2 2 4 2 2 2 4 6 0
0 0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 3 0 0 0 3 0 0
2 2 2 2 2 4 2 2 2 4 2 2
0 0 0 0 0 3 0 0 0 3 0 0
0 0 0 0 0 6 0 0 0 3 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
```

**Test 1 output**
```text
0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
2 2 2 4 2 2 2 4 2 2 6 0
0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
2 2 2 4 2 2 2 4 2 2 2 2
0 0 0 3 0 0 0 3 0 0 0 0
0 0 0 3 0 0 0 6 0 0 0 0
```

### hard_o03 — Shortest path with two keys and two locked doors

**Written rule:** Find the shortest path from the start to the goal while collecting key 4 before door 6 and key 5 before door 7. Output only the path cells in color 9.

**Program function:** `solve_hard_o03`

**Primitives:** multikey_bfs_path

```python
def solve_hard_o03(g):
    h,w=dims(g)
    # 0 empty, 8 wall, 2 start, 3 goal, 4 keyA,5 keyB, 6 doorA,7 doorB
    start=goal=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            if g[r][c]==3: goal=(r,c)
    start_state=(start[0],start[1],0,0)
    q=deque([start_state]); prev={start_state:None}
    def passable(r,c,ka,kb):
        if not (0<=r<h and 0<=c<w): return False
        v=g[r][c]
        if v==8: return False
        if v==6 and not ka: return False
        if v==7 and not kb: return False
        return True
    end_state=None
    while q:
        r,c,ka,kb=q.popleft()
        if (r,c)==goal:
            end_state=(r,c,ka,kb); break
        nka,nkb=ka,kb
        if g[r][c]==4: nka=1
        if g[r][c]==5: nkb=1
        # important: from current state after collecting key maybe explore
        if (r,c,nka,nkb)!=(r,c,ka,kb) and (r,c,nka,nkb) not in prev:
            prev[(r,c,nka,nkb)] = (r,c,ka,kb)
            q.appendleft((r,c,nka,nkb))
            continue
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if passable(nr,nc,nka,nkb):
                st=(nr,nc,nka,nkb)
                if st not in prev:
                    prev[st]=(r,c,ka,kb)
                    q.append(st)
    if end_state is None:
        return blank(h,w)
    # reconstruct
    out=blank(h,w)
    st=end_state
    while st is not None:
        r,c,ka,kb=st
        out[r][c]=9
        st=prev[st]
    return out
```

**Train 1 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 4 0 6 0 0 0 0 8
8 8 8 8 8 8 0 8 8 8 0 8
8 0 0 0 0 0 0 0 0 0 0 8
8 0 0 8 8 8 5 8 8 8 8 8
8 0 0 0 0 0 0 0 7 0 3 8
8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 0 4 0 6 8 8 8 8 8 8
8 8 8 8 8 8 0 8 8 8 8 8 8
8 8 8 8 8 8 0 8 8 8 8 8 8
8 8 8 8 8 8 0 0 5 0 0 8 8
8 8 8 8 8 8 8 8 8 8 0 8 8
8 8 8 8 8 8 8 8 8 8 7 3 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 8 8 8 8 8 8 8 8 8 8 8 8
8 0 8 8 8 8 8 8 8 8 8 8 8 8
8 4 0 0 0 6 8 8 8 8 8 8 8 8
8 8 8 8 8 0 8 8 8 8 8 8 8 8
8 8 8 8 8 0 8 8 8 8 8 8 8 8
8 8 8 8 8 0 0 5 0 7 0 3 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 0 4 6 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 8 0 8 8 8 8 8 8 8 8 8
8 8 8 8 0 0 5 0 7 0 0 3 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_o04 — Rebuild the scene from singleton blueprint markers

**Written rule:** Single-cell components form a blueprint. Larger components are reusable prototypes keyed by color. Replace each blueprint marker by the matching prototype in a regular tiled output grid.

**Program function:** `solve_hard_o04`

**Primitives:** singleton_blueprint_place

```python
def solve_hard_o04(g):
    # singleton comps = blueprint; others = prototypes keyed by color
    comps=find_components(g)
    singles=[comp for comp in comps if comp['area']==1]
    protos=[comp for comp in comps if comp['area']>1]
    br0,bc0,br1,bc1=bbox([cell for comp in singles for cell in comp['cells']])
    bh,bw=br1-br0+1, bc1-bc0+1
    proto_by_color={}
    maxh=maxw=0
    for comp in protos:
        crop=crop_bbox(g, comp['cells'])
        proto_by_color[comp['color']]=crop
        hh,ww=dims(crop); maxh=max(maxh,hh); maxw=max(maxw,ww)
    out_h=bh*maxh + (bh-1)
    out_w=bw*maxw + (bw-1)
    out=blank(out_h,out_w)
    for comp in singles:
        r,c=comp['cells'][0]
        color=comp['color']
        slot_r=r-br0; slot_c=c-bc0
        crop=proto_by_color[color]
        top=slot_r*(maxh+1)
        left=slot_c*(maxw+1)
        place_shape(out, crop, top, left)
    return out
```

**Train 1 input**
```text
2 0 3 0 0 0 0 0 0 0 0 0 0 0
4 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 3 3 0 0 4 0 0 0
0 2 2 0 0 0 0 3 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 0 0 0 0 3 3
2 2 0 0 0 0 0 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 2 2 0 0 0
4 0 0 2 2 0 0 0
4 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 5 6 0 0 0 0 0 0 0 0 0 0 0 0
6 0 5 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 6 6 0 0 0 7 7 7 0
0 0 5 0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 5 5 0 0 6 6 0
0 0 0 0 0 5 0 0 6 6 0
0 0 0 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 5 5 0
6 6 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
4 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 4 5 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 5 5 0 0 0 8 8 0 0
0 0 4 0 0 0 0 5 5 0 0 0 0 8 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 0 0 0 0 0 0 0 8 8
4 0 0 0 0 0 0 0 0 0 8
4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 5 5 0 0 0
0 0 0 4 0 0 5 5 0 0 0
0 0 0 4 0 0 0 0 0 0 0
```

**Test 1 input**
```text
6 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 6 5 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 7 7 7 0 0 5 5 0 0
0 6 6 0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
6 6 0 0 0 0 0 0 7 7 7
6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 5 5 0
0 0 0 0 6 6 0 0 0 5 0
```

### hard_o05 — Stamp the candidate that matches the guide under dihedral symmetry

**Written rule:** One guide object specifies a shape. Among the candidates, find the one whose shape matches the guide up to rotation or reflection, then stamp that candidate’s current crop at every anchor marker.

**Program function:** `solve_hard_o05`

**Primitives:** guide_match_stamp

```python
def solve_hard_o05(g):
    comps=find_components(g)
    guide=max([comp for comp in comps if comp['color']==9], key=lambda c:c['area'])
    guide_crop=crop_bbox(g, guide['cells'])
    guide_ds={tuple(map(tuple,binarize(x))) for x in all_dihedral(guide_crop)}
    anchors=[comp['cells'][0] for comp in comps if comp['color']==8 and comp['area']==1]
    candidates=[comp for comp in comps if comp['color'] not in (8,9)]
    matching=[comp for comp in candidates if tuple(map(tuple,binarize(crop_bbox(g, comp['cells'])))) in guide_ds]
    target=max(matching, key=lambda c:c['area'])
    stamp=crop_bbox(g, target['cells'])
    h,w=dims(g)
    out=blank(h,w)
    for ar,ac in anchors:
        for r,row in enumerate(stamp):
            for c,v in enumerate(row):
                if v!=0 and 0<=ar+r<h and 0<=ac+c<w:
                    out[ar+r][ac+c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 5 5 0 0 0 6 6 6 0 0
0 4 4 0 0 0 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 8 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 3 3 0 0 0 4 4 0 0 5 5 0 0 0
0 0 0 3 0 0 0 0 4 0 0 5 5 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 7 0 0 0 0 4 4 4 0 0 6 6 0 0 0
0 7 7 7 0 0 0 0 0 0 0 0 0 6 6 0 0 0
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 2 2 0 0 0 4 4 0 0 0 5 5 0 0 0
0 0 0 2 0 0 0 4 4 0 0 0 0 5 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_o06 — Transform one shape, then apply a keyed Boolean operation

**Written rule:** Use one key to transform the first shape, use the second key to choose union/intersection/xor with the second shape, normalize both to the same origin, and output the resulting mask in color 8.

**Program function:** `solve_hard_o06`

**Primitives:** keyed_normalized_boolean

```python
def solve_hard_o06(g):
    h,w=dims(g)
    tkey=None; okey=None
    for c,v in enumerate(g[0]):
        if v in (1,2,3): tkey=v
        if v in (4,5,6): okey=v
    temp=copy_grid(g)
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4,5,6): temp[0][c]=0
    comps=find_components(temp)
    objs=sorted(comps, key=lambda comp:(comp['bbox'][1], comp['bbox'][0], comp['color']))
    A=crop_bbox(temp, objs[0]['cells'])
    B=crop_bbox(temp, objs[1]['cells'])
    A=transform_by_key(A, tkey)
    return apply_boolean(A,B,okey)
```

**Train 1 input**
```text
0 1 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 3 3 0 0 0
0 0 2 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8
8 8
```

**Train 2 input**
```text
0 2 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 3 0 0
0 2 0 0 0 0 0 0 0 3 0 0
0 2 2 2 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0
0 0
8 8
```

**Train 3 input**
```text
0 3 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 3 3 3 0
0 0 2 2 2 0 0 0 0 3 0 0
0 0 0 0 2 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0
8 0 8
8 0 0
```

**Test 1 input**
```text
0 1 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 3 3 0 0
0 0 2 0 0 0 0 0 3 0 0 0
0 0 2 2 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 8
0 8 8
0 8 8
```

### hard_o07 — Trace a ray through two mirror types

**Written rule:** Each emitter launches a ray to the right. Mirror 4 behaves like “/”, mirror 5 behaves like “\”, walls stop the ray, and the output marks the traced path in color 8.

**Program function:** `solve_hard_o07`

**Primitives:** mirror_raytrace

```python
def solve_hard_o07(g):
    h,w=dims(g)
    out=blank(h,w)
    turn_slash={(0,1):(-1,0),(-1,0):(0,1),(0,-1):(1,0),(1,0):(0,-1)}
    turn_back={(0,1):(1,0),(1,0):(0,1),(0,-1):(-1,0),(-1,0):(0,-1)}
    emitters=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    for sr,sc in emitters:
        r,c=sr,sc
        dr,dc=(0,1)
        while True:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): break
            cell=g[nr][nc]
            if cell==6 or cell==2:
                break
            out[nr][nc]=8
            if cell==4:
                dr,dc=turn_slash[(dr,dc)]
            elif cell==5:
                dr,dc=turn_back[(dr,dc)]
            r,c=nr,nc
    # keep mirrors and walls maybe for context? maybe no, output path only
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 8 0 0 8 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 0 0 0 0 0
0 0 5 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 8 8 8 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
