# ARC Puzzle Bank — Set 13
This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set13.json` — machine-readable task data
- `arc_puzzle_bank_21_set13_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set13_validation.txt` — validation log

## Easy (7)

### easy_m01 — Keep only the first cell of each horizontal run

**Written rule:** For each contiguous horizontal run of a nonzero color, erase everything except its leftmost cell.

**Program function:** `solve_easy_m01`

**Primitives:** horizontal_run_starts

```python
def solve_easy_m01(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (c==0 or g[r][c-1]!=g[r][c]):
                out[r][c]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0
4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
6 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 9 9 9 9 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
```

### easy_m02 — Fill the midpoint of length-3 diagonals

**Written rule:** Whenever two same-colored cells sit on opposite corners of a 3×3 diagonal with a zero center, fill that center with the shared color.

**Program function:** `solve_easy_m02`

**Primitives:** diagonal_midpoint_bridge

```python
def solve_easy_m02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: continue
            colors=[]
            if 0<=r-1<h and 0<=c-1<w and 0<=r+1<h and 0<=c+1<w:
                a,b=g[r-1][c-1],g[r+1][c+1]
                if a!=0 and a==b: colors.append(a)
            if 0<=r-1<h and 0<=c+1<w and 0<=r+1<h and 0<=c-1<w:
                a,b=g[r-1][c+1],g[r+1][c-1]
                if a!=0 and a==b: colors.append(a)
            if colors:
                # assume either one or all same in valid examples
                out[r][c]=colors[0]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 4 0 7 0
0 0 0 0 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 4 0 0 0 0 0
0 0 4 0 0 0 0
0 0 0 4 0 7 0
0 0 0 0 7 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 9 0 0 0 0
0 0 0 6 0 0 2 0
0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
0 0 9 0 2 0 0 0
0 0 0 9 0 2 0 0
0 0 0 6 0 0 2 0
0 0 6 0 0 0 0 0
0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 5 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 5 0 0
0 0 0 3 0 0 0 5 0
0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 4 0 0 0 0
0 0 2 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 4 0 0 0 7 0
0 0 0 4 0 7 0 0
0 0 2 0 7 0 0 0
0 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
```

### easy_m03 — Pack each row’s population to the left

**Written rule:** Each row contains at most one nonzero color; count its nonzero cells and rewrite the row as that many cells packed from the left in the same color.

**Program function:** `solve_easy_m03`

**Primitives:** row_population_pack

```python
def solve_easy_m03(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        if not vals: continue
        # assume one color per row
        color=vals[0]
        n=len(vals)
        for c in range(min(n,w)):
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 4 0 0 4 0 0
7 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0
0 3 0 3 0 0 0 3
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0
7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0
```

**Train 2 input**
```text
0 2 0 0 2 0 0 2 0
0 0 0 0 0 0 0 0 0
5 0 0 5 0 0 0 0 0
0 0 9 0 0 0 9 0 9
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
5 5 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
6 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0
0 8 0 0 0 8 0 8
0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0
```

**Train 3 output**
```text
6 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0
8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0
```

**Test input**
```text
0 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0
2 0 0 2 0 2 0 0
0 0 8 0 0 0 0 0
0 0 0 0 4 0 4 4
```

**Test output**
```text
5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0
8 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0
```

### easy_m04 — Shoot a ray to the nearest border

**Written rule:** From each colored seed, extend a straight line from the seed to its uniquely nearest border, keeping the seed color.

**Program function:** `solve_easy_m04`

**Primitives:** nearest_border_ray

```python
def solve_easy_m04(g):
    h,w=dims(g)
    out=copy_grid(g)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0]
    for r,c,v in seeds:
        ds=[r,h-1-r,c,w-1-c]
        m=min(ds)
        # assume unique
        idx=ds.index(m)
        if idx==0:
            for rr in range(0,r+1): out[rr][c]=v
        elif idx==1:
            for rr in range(r,h): out[rr][c]=v
        elif idx==2:
            for cc in range(0,c+1): out[r][cc]=v
        else:
            for cc in range(c,w): out[r][cc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 0 0 2 0 0
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 2 0 0
0 0 0 0 2 0 0
0 0 0 0 0 0 0
8 8 0 0 0 0 0
0 0 0 0 0 0 0
0 0 6 0 0 0 0
0 0 6 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 3 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 6 0 0 5 0
0 0 0 0 6 0 0 5 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0
0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 2 0 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0
0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0
0 0 7 0 0 0 0 0
```

### easy_m05 — Recolor the rarer color into the commoner one

**Written rule:** The grid uses exactly two nonzero colors; change every occurrence of the globally rarer color into the globally more frequent color.

**Program function:** `solve_easy_m05`

**Primitives:** minority_to_majority

```python
def solve_easy_m05(g):
    counts=count_colors(g)
    if len(counts)<2:
        return copy_grid(g)
    dominant=max(counts.items(), key=lambda kv:(kv[1],-kv[0]))[0]
    rare=min(counts.items(), key=lambda kv:(kv[1],kv[0]))[0]
    out=copy_grid(g)
    for r,row in enumerate(out):
        for c,v in enumerate(row):
            if v==rare:
                out[r][c]=dominant
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 2 2 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 7 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 2 2 0 0 0 0
0 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 2 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
4 4 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0
0 0 0 0 0 0 9 0
```

**Train 2 output**
```text
4 4 0 0 0 0 0 0
4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0
0 0 0 0 0 0 4 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 6
0 0 0 0 3 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 3
0 0 0 0 3 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 3 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
```

### easy_m06 — Expand each seed into a hollow plus

**Written rule:** Replace each seed with its four orthogonal neighbors in the same color, but leave the original center blank.

**Program function:** `solve_easy_m06`

**Primitives:** halo_without_center

```python
def solve_easy_m06(g):
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0]
    for r,c,v in seeds:
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 4 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 7 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 0 4 0 0 0 0
0 4 0 4 0 0 0
0 0 4 0 0 7 0
0 0 0 0 7 0 7
0 0 0 0 0 7 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 2 0
0 0 0 0 0 2 0 2
0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0
9 0 9 0 0 3 0 0
0 9 0 0 3 0 3 0
0 0 0 0 0 3 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8 0 0 0 0 0 0 0
8 0 8 0 0 0 0 0 0
0 8 0 0 6 0 0 0 0
0 0 0 6 0 6 0 0 0
0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 5 0 5 0 0 0 0 0
0 0 5 0 0 0 8 0 0
0 0 0 0 0 8 0 8 0
0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
```

### easy_m07 — Keep only degree-1 cells

**Written rule:** Keep only nonzero cells that have exactly one orthogonal neighbor of the same color; erase all other colored cells.

**Program function:** `solve_easy_m07`

**Primitives:** degree1_filter

```python
def solve_easy_m07(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            deg=sum(1 for dr,dc in DIR4 if 0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]==v)
            if deg==1:
                out[r][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Medium (7)

### medium_m01 — Fill the biggest frame

**Written rule:** Among all hollow rectangular frames, fill only the interior of the frame with the largest interior area, using the frame’s own color.

**Program function:** `solve_medium_m01`

**Primitives:** scan_rect_frames, fill_largest_frame

```python
def solve_medium_m01(g):
    frames=scan_rect_frames(g)
    if not frames:
        return copy_grid(g)
    best=max(frames, key=lambda fr:(fr['interior_area'], fr['bbox'][2]-fr['bbox'][0], fr['bbox'][3]-fr['bbox'][1]))
    return fill_frame_interior(g,best)
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 2 0 0 0 2 0 0 7 7 7 0
0 2 0 0 0 2 0 0 7 0 7 0
0 2 0 0 0 2 0 0 7 0 7 0
0 2 2 2 2 2 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 2 0 0 7 7 7 0
0 2 2 2 2 2 0 0 7 0 7 0
0 2 2 2 2 2 0 0 7 0 7 0
0 2 2 2 2 2 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 3 0 0 3 0 6 6 6 0
0 3 0 0 3 0 6 0 6 0
0 3 0 0 3 0 6 0 6 0
0 3 0 0 3 0 6 6 6 0
0 3 0 0 3 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 3 3 3 3 0 6 6 6 0
0 3 3 3 3 0 6 0 6 0
0 3 3 3 3 0 6 0 6 0
0 3 3 3 3 0 6 6 6 0
0 3 3 3 3 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0 0
0 0 4 0 0 4 0 0 9 9 9 9 0
0 0 4 0 0 4 0 0 9 0 0 9 0
0 0 4 4 4 4 0 0 9 0 0 9 0
0 0 0 0 0 0 0 0 9 0 0 9 0
0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0 0
0 0 4 0 0 4 0 0 9 9 9 9 0
0 0 4 0 0 4 0 0 9 9 9 9 0
0 0 4 4 4 4 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 9 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 6 6 6 6 6 0
0 3 0 0 3 0 0 0 6 0 0 0 6 0
0 3 3 3 3 0 0 0 6 0 0 0 6 0
0 0 0 0 0 0 0 0 6 0 0 0 6 0
0 0 0 0 0 0 0 0 6 0 0 0 6 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 6 6 6 6 6 0
0 3 0 0 3 0 0 0 6 6 6 6 6 0
0 3 3 3 3 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_m02 — Corner marker chooses the transform

**Written rule:** Ignore the corner marker, crop the main object, and transform it based on the corner: top-left identity, top-right rotate 90° clockwise, bottom-left mirror horizontally, bottom-right rotate 180°.

**Program function:** `solve_medium_m02`

**Primitives:** corner_instruction_transform

```python
def solve_medium_m02(g):
    h,w=dims(g)
    # marker color 9 in one corner
    corners=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    marker=None
    for pos in corners:
        if g[pos[0]][pos[1]]==9:
            marker=pos; break
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=9]
    obj=crop_bbox(g,cells)
    if marker==(0,0):
        out=obj
    elif marker==(0,w-1):
        out=crop_nonzero(rotate90(obj))
    elif marker==(h-1,0):
        out=crop_nonzero(flip_h(obj))
    else:
        out=crop_nonzero(rotate180(obj))
    return out
```

**Train 1 input**
```text
9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 4 0
4 4 0
0 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6
6 0 0
6 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 3
0 3 3
3 3 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
```

**Test output**
```text
5 5 5
0 0 5
0 0 5
```

### medium_m03 — Sort objects by height into a gallery

**Written rule:** Crop each object to its bounding box, sort them by height ascending, and place them left-to-right with one blank column between them, top-aligned.

**Program function:** `solve_medium_m03`

**Primitives:** gallery_sort_by_height

```python
def solve_medium_m03(g):
    comps=find_components(g)
    crops=[object_grid_from_comp(g,comp) for comp in comps]
    crops=sorted(crops, key=lambda sub:(len(sub), len(sub[0]), tuple(tuple(row) for row in sub)))
    H=max(len(sub) for sub in crops)
    W=sum(len(sub[0]) for sub in crops)+max(0,len(crops)-1)
    out=blank(H,W)
    c0=0
    for i,sub in enumerate(crops):
        paste(out,sub,0,c0)
        c0+=len(sub[0])+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 2 2 0 4 0 0 7 0 0
0 0 0 0 4 0 0 7 0 0
0 0 0 0 4 4 0 7 7 7
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 6 0 3 3 0 0 8 0
0 0 0 0 0 3 3 0 8 8 0
0 0 0 0 0 0 0 0 0 8 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 9 9 0 5 0 0 2 0 0
0 0 0 0 0 5 5 0 2 2 0
0 0 0 0 0 0 0 0 0 2 2
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7 7 0 4 0 0 0 9 0
0 0 0 0 0 4 4 0 9 9 0
0 0 0 0 0 0 0 0 0 9 9
```

### medium_m04 — Recolor by area rank

**Written rule:** There are exactly three objects of distinct area; recolor the smallest to 1, the middle to 2, and the largest to 3, without moving them.

**Program function:** `solve_medium_m04`

**Primitives:** area_rank_recolor

```python
def solve_medium_m04(g):
    comps=find_components(g)
    comps_sorted=sorted(comps, key=lambda comp:(comp['area'], comp['bbox']))
    out=blank(*dims(g))
    for rank,comp in enumerate(comps_sorted, start=1):
        color=rank  # 1,2,3
        for r,c in comp['cells']:
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 7 0 0 0 4 4 0 0
0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 1 0 0 0 2 2 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 5 0 0
0 8 0 0 0 0 0 5 5 0 0
0 8 8 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 0 0
0 2 0 0 0 0 0 3 3 0 0
0 2 2 0 0 0 0 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 6 6 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 1 1 0
0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 9 9 0 0 0 0 0 0 4 4 0
0 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0
0 2 2 0 0 0 0 0 0 3 3 0
0 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_m05 — Nearest top marker recolors each object

**Written rule:** Top-row markers act as color labels; recolor each object below to the color of the marker whose column is closest to the object’s horizontal center.

**Program function:** `solve_medium_m05`

**Primitives:** nearest_marker_recolor

```python
def solve_medium_m05(g):
    h,w=dims(g)
    markers=[(c,g[0][c]) for c in range(w) if g[0][c]!=0]
    comps=find_components(g, ignore_colors={v for c,v in markers})
    out=copy_grid(g)
    marker_cols_colors=markers
    marker_colors=set(v for c,v in markers)
    # wipe objects first? recolor over existing objects
    for comp in comps:
        _, cx = center_of_bbox(comp)
        mc, col = min(marker_cols_colors, key=lambda item:(abs(item[0]-cx), item[0]))
        for r,c in comp['cells']:
            out[r][c]=col
    return out
```

**Train 1 input**
```text
0 2 0 0 0 4 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 4 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 0 0 0 5 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0 4 0 0
0 0 0 0 0 9 9 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3 0 0 0 5 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 7 0 0
0 0 0 0 0 5 5 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 8 0 0 0 0 0 2 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 0 0 0 0 5 0 0 0 0 0 0 0
0 3 3 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 8 0 0 0 0 0 2 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 2 0 0 0 0 0 0 0
0 8 8 0 0 0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 2 0 0 0 0 5 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 9 9 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 2 0 0 0 0 5 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_m06 — Keep only contents matching their frame

**Written rule:** Rectangular frames stay unchanged, but an object inside a frame survives only if its color matches the enclosing frame’s color.

**Program function:** `solve_medium_m06`

**Primitives:** scan_rect_frames, keep_matching_container_contents

```python
def solve_medium_m06(g):
    out=copy_grid(g)
    frames=scan_rect_frames(g)
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        inner=[]
        inner_colors=set()
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if out[r][c]!=0:
                    inner.append((r,c))
                    inner_colors.add(out[r][c])
        if inner and (len(inner_colors)!=1 or next(iter(inner_colors)) != fr['color']):
            for r,c in inner:
                out[r][c]=0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 7 7 7 7 7 0
0 2 0 2 0 2 0 0 7 0 0 0 7 0
0 2 0 0 0 2 0 0 7 0 4 4 7 0
0 2 2 2 2 2 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 7 7 7 7 7 0
0 2 0 2 0 2 0 0 7 0 0 0 7 0
0 2 0 0 0 2 0 0 7 0 0 0 7 0
0 2 2 2 2 2 0 0 7 0 0 0 7 0
0 0 0 0 0 0 0 0 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 5 0 3 0 0 0 0 0 0 0 0
0 0 3 0 5 0 3 0 0 8 8 8 8 8 0
0 0 3 3 3 3 3 0 0 8 0 0 0 8 0
0 6 6 6 6 6 0 0 0 8 0 8 0 8 0
0 6 0 0 0 6 0 0 0 8 0 8 0 8 0
0 6 0 6 0 6 0 0 0 8 8 8 8 8 0
0 6 6 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 8 8 8 8 8 0
0 0 3 3 3 3 3 0 0 8 0 0 0 8 0
0 6 6 6 6 6 0 0 0 8 0 8 0 8 0
0 6 0 0 0 6 0 0 0 8 0 8 0 8 0
0 6 0 6 0 6 0 0 0 8 8 8 8 8 0
0 6 6 6 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 9 9 9 9 9 0
0 4 4 0 4 0 0 0 0 0 9 0 0 0 9 0
0 4 0 0 4 0 0 0 0 0 9 0 2 0 9 0
0 4 4 4 4 0 0 0 0 0 9 0 0 0 9 0
0 0 0 0 0 0 5 5 5 5 9 9 9 9 9 0
0 0 0 0 0 0 5 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0 9 9 9 9 9 0
0 4 4 0 4 0 0 0 0 0 9 0 0 0 9 0
0 4 0 0 4 0 0 0 0 0 9 0 0 0 9 0
0 4 4 4 4 0 0 0 0 0 9 0 0 0 9 0
0 0 0 0 0 0 5 5 5 5 9 9 9 9 9 0
0 0 0 0 0 0 5 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 5 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 7 7 7 7 7 0
0 2 0 0 0 2 0 0 0 0 7 0 7 0 7 0
0 2 0 2 0 2 0 0 0 0 7 0 7 0 7 0
0 2 0 0 0 2 0 0 0 0 7 7 7 7 7 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 0 9 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 7 7 7 7 7 0
0 2 0 0 0 2 0 0 0 0 7 0 7 0 7 0
0 2 0 2 0 2 0 0 0 0 7 0 7 0 7 0
0 2 0 0 0 2 0 0 0 0 7 7 7 7 7 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
```

### medium_m07 — Repeat the template by marker count

**Written rule:** Count the marker cells, crop the template object, and output that many copies of the template in a horizontal gallery with one blank column between copies.

**Program function:** `solve_medium_m07`

**Primitives:** repeat_template_by_count

```python
def solve_medium_m07(g):
    h,w=dims(g)
    marker_count=sum(1 for r in range(h) for c in range(w) if g[r][c]==9)
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=9]
    template=crop_bbox(g,cells)
    th,tw=dims(template)
    H=th
    W=marker_count*tw + max(0, marker_count-1)
    out=blank(H,W)
    c0=0
    for i in range(marker_count):
        paste(out,template,0,c0)
        c0+=tw+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 0 0 4 0
4 4 0 4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 0 6 0 0 6 0
6 0 0 6 0 0 6 0
6 6 0 6 6 0 6 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 9 0
0 0 3 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3 0 0 0 3 0 0 0 3 0 0 0 3 0
3 3 0 0 3 3 0 0 3 3 0 0 3 3 0
0 3 3 0 0 3 3 0 0 3 3 0 0 3 3
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
9 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 0
```

**Test output**
```text
6 0 0 0 6 0 0 0 6 0 0
6 0 0 0 6 0 0 0 6 0 0
6 6 6 0 6 6 6 0 6 6 6
```

## Hard (7)

### hard_m01 — Select the dihedral match

**Written rule:** Compare each candidate object against the target object up to rotation or reflection; output the one candidate whose shape matches the target under some dihedral transform.

**Program function:** `solve_hard_m01`

**Primitives:** dihedral_match_select

```python
def solve_hard_m01(g):
    h,w=dims(g)
    # target color 2
    target_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    target=crop_bbox(g,target_cells)
    comps=find_components(g, ignore_colors={2})
    # candidate components among others
    for comp in comps:
        cand=object_grid_from_comp(g,comp)
        if same_shape_under_dihedral(target, recolor_grid(cand,1)):
            return cand
    return [[0]]
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 6 0 0 0 0
0 2 2 0 0 0 0 0 6 6 6 0 0 0
0 0 2 2 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 4 4 4 0 0 0 0 0 7 0 0 0
0 0 0 4 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 6 0
6 6 6
6 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 8 8 0 0 0 0 0 0 0 3 0 0
0 0 0 8 8 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 3
0 0 3
3 3 3
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 2 2 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 0
0 8 8
0 0 8
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 6 0 0 0 0 0 0
0 2 2 2 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8
0 0 8
0 0 8
```

### hard_m02 — Build the transform timeline

**Written rule:** The top row is a script of transforms; repeatedly apply them to the template object and output the sequence of resulting states as a left-to-right gallery. Here 1=rotate90, 2=rotate180, 3=mirror horizontally, 4=transpose.

**Program function:** `solve_hard_m02`

**Primitives:** transform_timeline

```python
def solve_hard_m02(g):
    h,w=dims(g)
    scripts=[v for v in g[0] if v!=0]
    # template = all nonzero below row0
    cells=[(r,c) for r in range(1,h) for c in range(w) if g[r][c]!=0]
    cur=crop_bbox(g,cells)
    states=[]
    for code in scripts:
        cur=apply_transform_code(cur, code)
        states.append(cur)
    H=max(len(sub) for sub in states)
    W=sum(len(sub[0]) for sub in states)+max(0,len(states)-1)
    out=blank(H,W)
    c0=0
    for sub in states:
        paste(out, sub, 0, c0)
        c0 += len(sub[0])+1
    return out
```

**Train 1 input**
```text
1 3 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 7 0 0 0 7 0 0 7 0 0
7 7 7 0 7 7 7 0 7 7 7
7 0 0 0 0 0 7 0 0 7 0
```

**Train 2 input**
```text
4 1 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6 6 0 0 0 6 0 0 0 6
0 0 6 0 0 0 6 0 0 0 6
0 0 6 0 6 6 6 0 6 6 6
```

**Train 3 input**
```text
3 1 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 5 0 5 0 0 0 5 5 0 0 0 5 5
0 5 5 0 5 5 0 0 0 5 5 0 5 5 0
5 5 0 0 0 5 5 0 0 0 5 0 5 0 0
```

**Test input**
```text
1 4 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
7 7 7 0 7 7 7 0 7 7 7
7 0 0 0 7 0 0 0 0 0 7
7 0 0 0 7 0 0 0 0 0 7
```

### hard_m03 — Route the path through ordered waypoints

**Written rule:** Draw the shortest path from start 2 through all present waypoints in increasing color order (4,5,6,...) and then to goal 3, avoiding walls 1; paint only the traversed empty cells with 8.

**Program function:** `solve_hard_m03`

**Primitives:** ordered_waypoint_path

```python
def solve_hard_m03(g):
    h,w=dims(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in {2,3,4,5,6,7}:
                pos[v]=(r,c)
    order=[2]+[k for k in sorted(pos) if k not in {2,3}] + [3]
    # ensure waypoints only 4+
    mids=[k for k in sorted(pos) if k not in {2,3}]
    order=[2]+mids+[3]
    out=copy_grid(g)
    for a,b in zip(order, order[1:]):
        path=bfs_path(g, pos[a], pos[b], passable=lambda r,c: g[r][c] != 1)
        if path is None:
            continue
        for r,c in path[1:-1]:
            if out[r][c]==0:
                out[r][c]=8
    return out
```

**Train 1 input**
```text
1 1 1 1 1 1 1 1 1
1 2 0 0 0 0 0 4 1
1 0 1 1 1 0 1 0 1
1 0 0 0 1 0 0 0 1
1 0 1 0 1 1 1 0 1
1 0 0 0 0 0 0 3 1
1 1 1 1 1 1 1 1 1
```

**Train 1 output**
```text
1 1 1 1 1 1 1 1 1
1 2 8 8 8 8 8 4 1
1 0 1 1 1 0 1 8 1
1 0 0 0 1 0 0 8 1
1 0 1 0 1 1 1 8 1
1 0 0 0 0 0 0 3 1
1 1 1 1 1 1 1 1 1
```

**Train 2 input**
```text
1 1 1 1 1 1 1 1 1 1
1 2 0 0 1 0 0 0 4 1
1 0 1 0 1 0 1 0 0 1
1 0 1 0 0 0 1 1 0 1
1 0 0 0 1 0 0 0 0 1
1 1 1 0 1 1 1 0 1 1
1 5 0 0 0 0 0 0 3 1
1 1 1 1 1 1 1 1 1 1
```

**Train 2 output**
```text
1 1 1 1 1 1 1 1 1 1
1 2 8 8 1 8 8 8 4 1
1 0 1 8 1 8 1 0 8 1
1 0 1 8 8 8 1 1 8 1
1 0 0 0 1 0 0 8 8 1
1 1 1 0 1 1 1 8 1 1
1 5 8 8 8 8 8 8 3 1
1 1 1 1 1 1 1 1 1 1
```

**Train 3 input**
```text
1 1 1 1 1 1 1 1 1
1 2 0 0 0 1 4 0 1
1 1 1 0 0 1 0 0 1
1 5 0 0 1 1 0 1 1
1 0 1 0 0 0 0 0 1
1 0 1 1 1 0 1 0 1
1 0 0 0 0 0 1 3 1
1 1 1 1 1 1 1 1 1
```

**Train 3 output**
```text
1 1 1 1 1 1 1 1 1
1 2 8 8 0 1 4 0 1
1 1 1 8 0 1 8 0 1
1 5 8 8 1 1 8 1 1
1 0 1 8 8 8 8 8 1
1 0 1 1 1 0 1 8 1
1 0 0 0 0 0 1 3 1
1 1 1 1 1 1 1 1 1
```

**Test input**
```text
1 1 1 1 1 1 1 1 1 1
1 2 0 0 0 1 0 4 0 1
1 0 1 1 0 1 0 1 0 1
1 0 0 1 0 0 0 1 0 1
1 1 0 1 1 1 0 1 0 1
1 5 0 0 0 0 0 1 0 1
1 0 1 1 1 1 0 0 3 1
1 1 1 1 1 1 1 1 1 1
```

**Test output**
```text
1 1 1 1 1 1 1 1 1 1
1 2 8 8 8 1 8 4 0 1
1 0 1 1 8 1 8 1 0 1
1 0 0 1 8 8 8 1 0 1
1 1 0 1 1 1 8 1 0 1
1 5 8 8 8 8 8 1 0 1
1 0 1 1 1 1 8 8 3 1
1 1 1 1 1 1 1 1 1 1
```

### hard_m04 — Recolor by visibility degree

**Written rule:** Treat each object as a node; two objects are adjacent if they can see each other along a clear row or column with only empty cells between them. Recolor each object to degree+1.

**Program function:** `solve_hard_m04`

**Primitives:** visibility_degree

```python
def solve_hard_m04(g):
    comps, edges = visibility_edges(g)
    deg=defaultdict(int)
    for a,b in edges:
        deg[a]+=1; deg[b]+=1
    out=blank(*dims(g))
    for i,comp in enumerate(comps):
        color=deg[i]+1
        for r,c in comp['cells']:
            out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 6 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 5 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 3 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 6 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_m05 — Boolean shape chosen by the key

**Written rule:** Normalize the two objects to the top-left of their own boxes, overlay them on a common canvas, and output the union if the key is 1, the intersection if the key is 2, and the xor if the key is 3, using color 8.

**Program function:** `solve_hard_m05`

**Primitives:** keyed_boolean_shape

```python
def solve_hard_m05(g):
    h,w=dims(g)
    key=g[0][0]
    comps=find_components(g, ignore_colors={key})
    # assume exactly two components besides key
    subs=[object_grid_from_comp(g,comp) for comp in comps]
    # choose two largest maybe
    subs=sorted(subs, key=lambda sub:(-sum(v!=0 for row in sub for v in row), len(sub), len(sub[0])))
    a,b=subs[:2]
    a_occ={(r,c) for r,row in enumerate(a) for c,v in enumerate(row) if v!=0}
    b_occ={(r,c) for r,row in enumerate(b) for c,v in enumerate(row) if v!=0}
    H=max(len(a),len(b)); W=max(len(a[0]),len(b[0]))
    if key==1: # union
        occ={(r,c) for r in range(H) for c in range(W) if (r,c) in a_occ or (r,c) in b_occ}
    elif key==2: # intersection
        occ={(r,c) for r in range(H) for c in range(W) if (r,c) in a_occ and (r,c) in b_occ}
    else: # xor
        occ={(r,c) for r in range(H) for c in range(W) if ((r,c) in a_occ) ^ ((r,c) in b_occ)}
    if not occ:
        return [[0]]
    rr=[r for r,c in occ]; cc=[c for r,c in occ]
    r0,c0,r1,c1=min(rr),min(cc),max(rr),max(cc)
    out=blank(r1-r0+1, c1-c0+1)
    for r,c in occ:
        out[r-r0][c-c0]=8
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8
8 8 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 7 0 0 0 0 0
0 5 5 5 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 0 0
8 0 0
0 8 8
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 8
8 0 0
```

**Test input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
8 8 8
8 8 0
8 8 0
```

### hard_m06 — Stamp transformed templates into frames

**Written rule:** A template object sits outside the frames. Each nearby marker tells you how to transform the template (1=rotate90, 2=rotate180, 3=mirror horizontally, 4=identity); stamp the transformed template centered inside that frame’s interior and recolor it to the marker color.

**Program function:** `solve_hard_m06`

**Primitives:** transformed_frame_stamp, scan_rect_frames

```python
def solve_hard_m06(g):
    h,w=dims(g)
    frames=scan_rect_frames(g)
    # template color 7 cells not in any frame border or frame interior? We want one template outside frames.
    frame_boxes=[fr['bbox'] for fr in frames]
    def in_any_frame(r,c):
        for r0,c0,r1,c1 in frame_boxes:
            if r0<=r<=r1 and c0<=c<=c1:
                return True
        return False
    template_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==7 and not in_any_frame(r,c)]
    template=crop_bbox(g, template_cells)
    out=copy_grid(g)
    for r,c in template_cells:
        out[r][c]=0
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        code=None; marker_pos=None
        for pos in [(r0-1,c0),(r0,c0-1),(r0-1,c1),(r1,c0-1)]:
            r,c=pos
            if 0<=r<h and 0<=c<w and g[r][c] in {1,2,3,4}:
                code=g[r][c]; marker_pos=pos; break
        if code is None: code=4
        sub=apply_transform_code(template, {1:1,2:2,3:3,4:5}[code])
        if marker_pos is not None:
            out[marker_pos[0]][marker_pos[1]]=0
        center_paste_in_box(out, recolor_grid(sub, code), (r0+1,c0+1,r1-1,c1-1), color_override=code)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 3 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 0 9 1 1 0 9 0 0 0
0 0 0 0 0 0 0 0 9 1 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 9 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 5 0 3 0 5 0 0 0 0
0 0 0 0 0 0 0 5 3 3 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5 5 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 7 7 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 2 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 4 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 4 4 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 4 4 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 2 2 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 2 2 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 2 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 6 6 6 6 6 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 7 7 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
2 9 9 9 9 9 0 0 0 0 3 5 5 5 5 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 9 9 9 9 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 1 1 1 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 1 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 9 9 9 9 9 0 0 0 0 3 5 5 5 5 5 0 0
0 9 2 2 0 9 0 0 0 0 0 5 4 0 0 5 0 0
0 9 0 2 0 9 0 0 0 0 0 5 4 0 0 5 0 0
0 9 0 2 0 9 0 0 0 0 0 5 4 4 0 5 0 0
0 9 9 9 9 9 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
1 9 9 9 9 9 0 0 0 0 2 5 5 5 5 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 9 9 9 9 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 9 9 9 9 9 0 0 0 0 2 5 5 5 5 5 0 0
0 9 1 1 0 9 0 0 0 0 0 5 4 0 0 5 0 0
0 9 1 0 0 9 0 0 0 0 0 5 4 4 0 5 0 0
0 9 0 0 0 9 0 0 0 0 0 5 0 0 0 5 0 0
0 9 9 9 9 9 0 0 0 0 0 5 5 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_m07 — Select by rank, then transform

**Written rule:** Use the top-left key to select the object by area rank (1=smallest, 2=middle, 3=largest), then use the top-right key to transform it (4=identity, 5=rotate90, 6=mirror horizontally, 7=rotate180), and output the cropped result.

**Program function:** `solve_hard_m07`

**Primitives:** rank_select_then_transform

```python
def solve_hard_m07(g):
    h,w=dims(g)
    rank_key=g[0][0]  # 1 smallest,2 middle,3 largest
    tf_key=g[0][w-1]  # 4 id,5 rot90,6 flip_h,7 rot180
    ignore={rank_key, tf_key}
    comps=find_components(g, ignore_colors=ignore)
    comps_sorted=sorted(comps, key=lambda comp:(comp['area'], comp['bbox']))
    selected=comps_sorted[rank_key-1]
    sub=object_grid_from_comp(g, selected)
    if tf_key==4:
        out=sub
    elif tf_key==5:
        out=crop_nonzero(rotate90(sub))
    elif tf_key==6:
        out=crop_nonzero(flip_h(sub))
    else:
        out=crop_nonzero(rotate180(sub))
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 9 0 0 0 0 0 0 0
0 8 8 0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8
8 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 9 0 0 0
0 0 0 0 0 0 0 8 8 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 9 9 9 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 8
0 8
8 8
```

**Train 3 input**
```text
3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0
0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 9 0
0 9 9
0 0 9
```

**Test input**
```text
2 0 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 9 0 0 0 0 0 0 0 0
0 8 8 0 0 0 9 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 9 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test output**
```text
0 9 9
9 9 0
9 0 0
```
