# ARC Puzzle Bank — Set 14
This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

This batch pushes into a different slice of the space: vertical/run logic, global transpose, rectangle closure, border-directed growth, axis completion, gallery packing, perimeter ranking, blocker-aware gravity, teleport and key-door pathfinding, dihedral guide matching, dual-key control, normalized overlay, Ferrers decoding, and area-based frame assignment.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set14.json` — machine-readable task data
- `arc_puzzle_bank_21_set14_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set14_validation.txt` — validation log

## Easy (7)

### easy_n01 — Keep only the first cell of each vertical run

**Written rule:** For each contiguous vertical run of a nonzero color, erase everything except its topmost cell.

**Program function:** `solve_easy_n01`

**Primitives:** vertical_run_heads

```python
def solve_easy_n01(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        r=0
        while r<h:
            if g[r][c]==0:
                r+=1; continue
            col=g[r][c]
            out[r][c]=col
            r2=r+1
            while r2<h and g[r2][c]==col:
                r2+=1
            r=r2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 4 0 0
0 2 0 0 0 4 0 0
0 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 7 0
```

**Train 1 output**
```text
0 0 0 0 0 4 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0
0 0 0 6 0 0 0
3 0 0 6 0 0 0
3 0 0 6 0 0 0
0 0 0 6 0 0 0
0 0 0 0 0 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 6 0 0 0
3 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 5 0 0 0 0 0 0
0 0 5 0 0 0 0 9 0
0 0 5 0 0 0 0 9 0
0 0 0 0 1 0 0 9 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 2 0 0 0 0
0 4 0 0 2 0 0 0 0
0 4 0 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 2 0 0 0 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

### easy_n02 — Fill single-cell horizontal gaps

**Written rule:** Whenever a row contains color–zero–same color with a one-cell gap, fill the zero with that color.

**Program function:** `solve_easy_n02`

**Primitives:** unit_gap_bridge

```python
def solve_easy_n02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==g[r][c+1] and g[r][c-1]!=0:
                out[r][c]=g[r][c-1]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 0 5 0
7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 0
7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0 0
0 8 0 8 0 8 0 8 0
```

**Train 2 output**
```text
0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0
6 0 6 0 0 0 0
0 0 0 0 0 0 0
0 0 9 0 9 0 0
0 0 0 0 0 0 0
0 0 0 1 0 1 0
0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0
6 6 6 0 0 0 0
0 0 0 0 0 0 0
0 0 9 9 9 0 0
0 0 0 0 0 0 0
0 0 0 1 1 1 0
0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0 0
7 0 7 0 0 7 0 7 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0
7 7 7 0 0 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```

### easy_n03 — Transpose the whole pattern

**Written rule:** Swap rows and columns: the output is the exact transpose of the input grid.

**Program function:** `solve_easy_n03`

**Primitives:** grid_transpose

```python
def solve_easy_n03(g):
    return transpose(g)
```

**Train 1 input**
```text
0 0 0 0 0 4 0
0 2 0 0 0 4 0
0 2 2 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0
0 2 2 0
0 0 2 0
0 0 0 0
0 0 0 0
4 4 0 0
0 0 0 0
```

**Train 2 input**
```text
8 0 0 0 0 0
0 3 3 3 0 0
0 0 3 0 0 0
0 0 0 0 0 0
0 0 0 0 0 8
```

**Train 2 output**
```text
8 0 0 0 0
0 3 0 0 0
0 3 3 0 0
0 3 0 0 0
0 0 0 0 0
0 0 0 0 8
```

**Train 3 input**
```text
0 6 0 0 0 0 0 0
0 0 0 6 0 0 0 6
0 0 0 0 0 6 0 0
```

**Train 3 output**
```text
0 0 0
6 0 0
0 0 0
0 6 0
0 0 0
0 0 6
0 0 0
0 6 0
```

**Test 1 input**
```text
0 0 0 9
5 5 0 0
0 5 5 0
0 0 0 0
0 0 0 0
0 0 9 0
```

**Test 1 output**
```text
0 5 0 0 0 0
0 5 5 0 0 0
0 0 5 0 0 9
9 0 0 0 0 0
```

### easy_n04 — Complete the missing rectangle corner

**Written rule:** If three corners of an axis-aligned rectangle have the same nonzero color, add the fourth corner in that color.

**Program function:** `solve_easy_n04`

**Primitives:** rectangle_fourth_corner

```python
def solve_easy_n04(g):
    out=copy_grid(g)
    pos=defaultdict(set)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].add((r,c))
    for col,cellset in pos.items():
        rows=sorted({r for r,c in cellset})
        cols=sorted({c for r,c in cellset})
        for i,r1 in enumerate(rows):
            for r2 in rows[i+1:]:
                for j,c1 in enumerate(cols):
                    for c2 in cols[j+1:]:
                        corners=[(r1,c1),(r1,c2),(r2,c1),(r2,c2)]
                        present=sum((p in cellset) for p in corners)
                        if present==3:
                            for p in corners:
                                if p not in cellset:
                                    out[p[0]][p[1]]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0
0 0 0 6 0 0 6 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 4 0 0 0 0 0 0
8 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0
8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 4 0 0 0 0 4 0
8 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0
8 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 9
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 9 0 0 9
0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 9
0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0
0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
7 0 0 7 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 0 0 7 0 0 0 0 0
0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
7 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0
```

### easy_n05 — Step each seed toward its nearest border

**Written rule:** Each nonzero seed keeps its position and also paints the adjacent cell one step toward its uniquely nearest border.

**Program function:** `solve_easy_n05`

**Primitives:** nearest_border_step

```python
def solve_easy_n05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            # unique nearest border
            dists={'top':r, 'bottom':h-1-r, 'left':c, 'right':w-1-c}
            mind=min(dists.values())
            dirs=[k for k,vv in dists.items() if vv==mind]
            if len(dirs)!=1: 
                continue
            d=dirs[0]
            dr,dc={'top':(-1,0),'bottom':(1,0),'left':(0,-1),'right':(0,1)}[d]
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 6 0
0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 6 6
4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0
0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 5 0 0 0 0
0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9
8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0
0 0 0 0 0 7 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0
6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 4 0 0 7 0 0 0
0 0 0 4 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 3 0 0 0 0
4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
```

### easy_n06 — Grow plus signs into filled 3x3 squares

**Written rule:** Whenever a same-color plus shape appears, fill in its four diagonal corners so it becomes a solid 3x3 square.

**Program function:** `solve_easy_n06`

**Primitives:** plus_fill_square

```python
def solve_easy_n06(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            v=g[r][c]
            if v!=0 and g[r-1][c]==v and g[r+1][c]==v and g[r][c-1]==v and g[r][c+1]==v:
                for rr in range(r-1,r+2):
                    for cc in range(c-1,c+2):
                        out[rr][cc]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 4 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 2 2 2 0 4 4 4 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0
0 0 6 6 6 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0
0 0 6 6 6 0 0 0
0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0
0 0 0 0 5 0 0 0 8 0 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0
0 0 0 5 5 5 0 8 8 8 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

### easy_n07 — Keep only the majority nonzero color

**Written rule:** Find the nonzero color that appears most often in the whole grid and erase every other nonzero color.

**Program function:** `solve_easy_n07`

**Primitives:** majority_color_filter

```python
def solve_easy_n07(g):
    counts=defaultdict(int)
    for row in g:
        for v in row:
            if v!=0: counts[v]+=1
    if not counts: return copy_grid(g)
    maj=max(counts, key=lambda c:(counts[c], -c))
    return [[v if v==maj else 0 for v in row] for row in g]
```

**Train 1 input**
```text
0 0 0 0 0 0 6 6
0 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 2 2 0 0 2 2 0
4 0 0 0 0 2 2 0
4 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 2 2 0 0 2 2 0
0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 8 0
0 0 3 0 0 0 0 8 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 3 0 0
0 7 7 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 7 0 0 0 0
0 5 5 5 0 7 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 2 2 0
0 0 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 6 0
0 0 0 0 0 0 0 0 6 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Medium (7)

### medium_n01 — Crop the object named by the marker color

**Written rule:** The top-left marker names the target color; isolate the object of that color and output its tight crop.

**Program function:** `solve_medium_n01`

**Primitives:** marker_selected_crop

```python
def solve_medium_n01(g):
    marker=g[0][0]
    comps=find_components(g)
    target=None
    for comp in comps:
        if comp['color']==marker and (0,0) not in comp['cells']:
            target=comp
            break
    if target is None:
        # maybe marker itself forms a comp; find largest other matching color excluding cell 0,0
        same=[comp for comp in comps if comp['color']==marker and comp['cells']!=[(0,0)]]
        if same:
            target=max(same,key=lambda comp:comp['area'])
    return crop_bbox(g, target['cells']) if target else [[marker]]
```

**Train 1 input**
```text
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 4 4 0
0 2 2 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 4 4
0 4 0
```

**Train 2 input**
```text
7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0
5 0 0 0 0 7 7 0 0
5 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
7 7
7 7
```

**Train 3 input**
```text
2 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
2 2 0
0 2 2
```

**Test 1 input**
```text
6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0
0 3 3 0 0 0 0 6 0 0 0
0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 6 0
6 6 6
0 6 0
```

### medium_n02 — Complete mirror symmetry across the axis line

**Written rule:** Find the full line of 9s and reflect every non-axis colored cell across that line, keeping the original cells too.

**Program function:** `solve_medium_n02`

**Primitives:** axis_echo

```python
def solve_medium_n02(g):
    h,w=dims(g)
    out=copy_grid(g)
    # detect vertical/horizontal axis line of color 9 spanning full extent
    axis=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            axis=('v',c); break
    if axis is None:
        for r in range(h):
            if all(g[r][c]==9 for c in range(w)):
                axis=('h',r); break
    if axis is None:
        return out
    kind,idx=axis
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v==9: 
                continue
            if kind=='v':
                mc=2*idx-c
                if 0<=mc<w:
                    out[r][mc]=v
            else:
                mr=2*idx-r
                if 0<=mr<h:
                    out[mr][c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 9 0 0 0 0
0 2 0 0 9 0 0 0 0
0 2 2 0 9 0 0 0 0
0 0 0 0 9 0 0 0 0
0 0 6 0 9 0 0 0 0
0 0 6 0 9 0 0 0 0
0 0 0 0 9 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 9 0 0 0 0
0 2 0 0 9 0 0 2 0
0 2 2 0 9 0 2 2 0
0 0 0 0 9 0 0 0 0
0 0 6 0 9 0 6 0 0
0 0 6 0 9 0 6 0 0
0 0 0 0 9 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0
0 0 0 3 0 0 7 7
0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0
0 0 0 3 0 0 7 7
0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0
0 0 0 3 0 0 7 7
0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0 0
0 4 4 0 0 0 9 0 0 0
0 0 4 4 0 0 9 0 0 0
0 0 0 8 8 0 9 0 0 0
0 0 0 8 8 0 9 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0 0
0 4 4 0 0 0 9 0 0 0
0 0 4 4 0 0 9 0 0 4
0 0 0 8 8 0 9 0 8 8
0 0 0 8 8 0 9 0 8 8
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 9 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 5 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 5 5 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0 0
0 5 5 0 0 2 2 0 0
0 5 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
```

### medium_n03 — Pack objects into a width-sorted gallery

**Written rule:** Crop each connected object, sort the crops by width from narrowest to widest, then pack them left-to-right with one blank column between and bottom-align them.

**Program function:** `solve_medium_n03`

**Primitives:** gallery_pack_by_width

```python
def solve_medium_n03(g):
    comps=find_components(g)
    objs=[]
    for comp in comps:
        sub=crop_bbox(g, comp['cells'])
        h,w=dims(sub)
        objs.append((w,h,comp['bbox'][0],sub))
    objs.sort(key=lambda t:(t[0], t[1], t[2]))  # width asc, then height, then top row
    maxh=max((h for w,h,_,sub in objs), default=1)
    totalw=sum(w for w,h,_,sub in objs) + max(0,len(objs)-1)
    out=blank(maxh, totalw)
    c0=0
    for w,h,_,sub in objs:
        r0=maxh-h
        for r in range(h):
            for c in range(w):
                if sub[r][c]!=0:
                    out[r0+r][c0+c]=sub[r][c]
        c0+=w+1
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 0 4 0 0 6 6 6
2 0 4 4 0 0 6 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
5 0 3 0 0 0 0 0
5 0 3 0 0 7 7 0
5 0 3 3 0 0 7 7
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 4 0 0 0 8 8 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 2 0 0
0 4 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
4 0 0 0 0 0 2 0
4 0 8 8 0 2 2 2
4 0 8 8 0 0 2 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 6 0 0 0 0 0 8 8 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 3 0
6 0 8 0 0 3 3 3
6 0 8 8 0 0 3 0
```

### medium_n04 — Recolor components by perimeter rank

**Written rule:** Treat each connected component as a separate object, rank them by perimeter from smallest to largest, and recolor them with the palette 2, then 4, then 8.

**Program function:** `solve_medium_n04`

**Primitives:** perimeter_rank_recolor

```python
def solve_medium_n04(g):
    comps=find_components(g)
    pers=[component_perimeter(g, comp) for comp in comps]
    order=sorted(range(len(comps)), key=lambda i:(pers[i], comps[i]['area'], comps[i]['bbox']))
    palette=[2,4,8]
    rank_color={}
    for rank,i in enumerate(order):
        rank_color[i]=palette[rank]
    out=blank(*dims(g))
    for i,comp in enumerate(comps):
        col=rank_color[i]
        for r,c in comp['cells']:
            out[r][c]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 6 6 0 0 6 6 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 4 4 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 7 7 7 0 0 0 0
0 7 0 0 0 0 7 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 4 4 0 0 0 0
0 2 0 0 0 0 4 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0 0 0
0 4 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 0 0 0
0 2 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_n05 — Replace each object with its bounding-box frame

**Written rule:** For each connected object, erase its interior detail and draw only the rectangular frame of its tight bounding box in the same color.

**Program function:** `solve_medium_n05`

**Primitives:** component_bbox_frame

```python
def solve_medium_n05(g):
    comps=find_components(g)
    out=blank(*dims(g))
    for comp in comps:
        r0,c0,r1,c1=comp['bbox']
        col=comp['color']
        for c in range(c0,c1+1):
            out[r0][c]=col; out[r1][c]=col
        for r in range(r0,r1+1):
            out[r][c0]=col; out[r][c1]=col
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0
0 0 0 0 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 0 2 0 0
0 0 0 0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_n06 — Rotate the object according to the marked corner

**Written rule:** The corner containing 9 chooses the rotation: top-left = none, top-right = 90° clockwise, bottom-right = 180°, bottom-left = 270° clockwise. Remove the marker and output the rotated object as a tight crop.

**Program function:** `solve_medium_n06`

**Primitives:** corner_key_rotate

```python
def solve_medium_n06(g):
    h,w=dims(g)
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    code=0
    for (r,c),k in corners.items():
        if g[r][c]==9:
            code=k
            break
    # remove marker and crop object
    gg=copy_grid(g); 
    for (r,c) in corners:
        if gg[r][c]==9: gg[r][c]=0
    obj=crop_nonzero(gg)
    return transform_grid(obj, code)
```

**Train 1 input**
```text
9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
4 0
4 0
4 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0
0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 6
6 6
0 6
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 3
3 3
3 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0
0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 9
```

**Test 1 output**
```text
5 5
0 5
```

### medium_n07 — Apply column gravity around fixed blockers

**Written rule:** Color cells fall downward within each column, but 5-cells stay fixed and split the column into independent gravity segments.

**Program function:** `solve_medium_n07`

**Primitives:** segmented_column_gravity

```python
def solve_medium_n07(g):
    h,w=dims(g)
    out=blank(h,w)
    # blockers fixed
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    for c in range(w):
        start=0
        while start<h:
            end=start
            while end<h and g[end][c]!=5:
                end+=1
            # segment start:end without blocker
            vals=[]
            for r in range(start,end):
                if g[r][c] not in (0,5):
                    vals.append(g[r][c])
            # drop to bottom of segment
            rr=end-1
            for v in reversed(vals):
                out[rr][c]=v
                rr-=1
            start=end+1
    return out
```

**Train 1 input**
```text
0 2 0 0 4 0 7
0 3 0 6 4 0 0
0 0 0 0 5 0 8
0 5 0 0 0 0 0
0 0 0 0 0 0 5
0 5 0 0 0 0 0
0 0 0 0 5 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 4 0 0
0 2 0 0 4 0 0
0 3 0 0 5 0 7
0 5 0 0 0 0 8
0 0 0 0 0 0 5
0 5 0 0 0 0 0
0 0 0 0 5 0 0
0 0 0 6 0 0 0
```

**Train 2 input**
```text
6 0 2 0 0 3 0 0
0 0 2 0 0 4 0 0
7 0 0 0 0 4 0 0
0 0 0 0 0 5 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 3 0 0
0 0 0 0 0 4 0 0
0 0 2 0 0 4 0 0
0 0 2 0 0 5 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
6 0 5 0 0 0 0 0
7 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 4 0 9 0 0 0 2 0
0 0 0 9 0 0 0 0 0
0 0 0 5 0 0 0 3 0
0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 9 0 0 0 0 0
0 0 0 9 0 0 0 0 0
0 0 0 5 0 0 0 2 0
0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 5 0
0 0 0 5 0 0 0 0 0
0 4 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 2 0 6 0 4 0 7 0
0 3 0 0 0 4 0 8 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 9 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 8 0
0 2 0 0 0 0 0 5 0
0 3 0 0 0 4 0 0 0
0 5 0 0 0 4 0 0 0
0 0 0 0 0 5 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 9 0
```

## Hard (7)

### hard_n01 — Shortest path with teleport portals

**Written rule:** Draw the shortest route from 2 to 3 using color 4 on empty floor cells. Walls are 5. When the path steps onto a portal (7, 8, or 9), it instantly jumps to the matching portal of the same color. Keep start, goal, walls, and portals unchanged.

**Program function:** `solve_hard_n01`

**Primitives:** portal_bfs_path

```python
def solve_hard_n01(g):
    h,w=dims(g)
    portals=defaultdict(list)
    start=goal=None
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
            elif v in (7,8,9):
                portals[v].append((r,c))
    portal_jump={}
    for col,pts in portals.items():
        if len(pts)==2:
            a,b=pts
            portal_jump[a]=b
            portal_jump[b]=a
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal: break
        r,c=cur
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            v=g[nr][nc]
            if v==5: continue
            nxt=(nr,nc)
            if v in (7,8,9) and nxt in portal_jump:
                nxt=portal_jump[nxt]
            if nxt not in prev:
                prev[nxt]=cur
                q.append(nxt)
    out=copy_grid(g)
    if goal not in prev:
        return out
    cur=goal
    path=[]
    while cur is not None:
        path.append(cur); cur=prev[cur]
    path=path[::-1]
    for r,c in path:
        if out[r][c]==0:
            out[r][c]=4
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 7 0 0 0 5 0 0
0 0 0 0 5 5 5 0 5 0 0
0 2 0 0 5 5 5 0 0 3 0
0 0 0 0 5 5 5 0 5 0 0
0 0 0 0 0 0 7 0 5 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 5 0 0 0 0 0
0 4 4 4 7 0 0 0 5 0 0
0 4 0 0 5 5 5 0 5 0 0
0 2 0 0 5 5 5 4 4 3 0
0 0 0 0 5 5 5 4 5 0 0
0 0 0 0 0 0 7 4 5 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 8 0 0 5 0 0 0 0
5 5 0 5 5 5 5 0 5 5
0 0 0 0 5 0 0 8 0 0
0 0 0 0 5 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 5 0 0 0 0
0 4 0 0 0 5 0 0 0 0
0 4 8 0 0 5 0 0 0 0
5 5 0 5 5 5 5 0 5 5
0 0 0 0 5 0 0 8 0 0
0 0 0 0 5 0 0 4 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 9 0 0 0 5 0 0
0 0 0 0 0 5 5 5 0 5 0 0
0 2 0 0 0 5 5 5 0 0 3 0
0 0 0 0 0 5 5 5 0 5 0 0
0 0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 5 0 0
0 4 4 4 4 9 0 0 0 5 0 0
0 4 0 0 0 5 5 5 0 5 0 0
0 2 0 0 0 5 5 5 4 4 3 0
0 0 0 0 0 5 5 5 4 5 0 0
0 0 0 0 0 0 5 4 4 5 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 7 0 0 0 5 0 0
0 0 0 0 0 5 5 5 0 5 0 0
0 2 0 0 0 5 5 5 0 0 3 0
0 0 0 0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 7 0 5 0 0
0 0 0 0 0 0 5 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 5 0 0 0 0 0
0 4 4 4 4 7 0 0 0 5 0 0
0 4 0 0 0 5 5 5 0 5 0 0
0 2 0 0 0 5 5 5 4 4 3 0
0 0 0 0 0 5 5 5 4 0 0 0
0 0 0 0 0 0 5 4 4 5 0 0
0 0 0 0 0 0 0 7 0 5 0 0
0 0 0 0 0 0 5 0 0 0 0 0
```

### hard_n02 — Find the dihedral match and fill the guide mask

**Written rule:** The 8-cells form a guide mask. Among the candidate objects elsewhere in the grid, find the one whose shape matches the guide up to rotation or reflection, then repaint the guide cells with that candidate’s color and clear everything else.

**Program function:** `solve_hard_n02`

**Primitives:** guide_mask_match

```python
def solve_hard_n02(g):
    h,w=dims(g)
    comps=find_components(g)
    guide=[comp for comp in comps if comp['color']==8]
    if not guide:
        return blank(h,w)
    guide=guide[0]
    guide_norm=normalize_shape(guide['cells'])
    guide_bbox=guide['bbox']
    best=None
    best_oriented=None
    for comp in comps:
        if comp['color']==8: 
            continue
        sub=crop_bbox(g, comp['cells'])
        for orient in all_dihedral(sub):
            cells={(r,c) for r,row in enumerate(orient) for c,v in enumerate(row) if v!=0}
            if cells==guide_norm:
                best=comp
                best_oriented=orient
                break
        if best is not None:
            break
    out=blank(h,w)
    if best is None:
        return out
    r0,c0,r1,c1=guide_bbox
    gh,gw=r1-r0+1,c1-c0+1
    # guide_norm/ oriented dimensions should match
    for r,row in enumerate(best_oriented):
        for c,v in enumerate(row):
            if v!=0:
                out[r0+r][c0+c]=best['color']
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 6 6 6 0 0 8 8 0 0
0 0 0 0 6 0 0 0 0 8 0 0
0 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 4 0 0 0 0 0
0 2 2 0 0 4 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 2 2 0 0 0 0 0 0 8 8 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0
7 7 0 0 5 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 3 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0 0 0
2 0 3 0 0 6 0 0 0 0 0 0
2 0 0 0 6 6 6 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 8 8 0 0
0 0 2 0 0 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
7 7 0 0 5 5 0 0 0 0 0 0
7 7 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_n03 — Select by rank, transform by key, place into frame

**Written rule:** Count the 7s on the top row to choose the 1st, 2nd, or 3rd object by area rank. Use the corner 9 to choose the rotation (same convention as medium_n06). Then place the transformed chosen object centered inside the 8-frame and clear everything else.

**Program function:** `solve_hard_n03`

**Primitives:** rank_transform_frame_insert

```python
def solve_hard_n03(g):
    h,w=dims(g)
    # transform key from corner 9
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    code=0
    for (r,c),k in corners.items():
        if g[r][c]==9:
            code=k
            break
    rank=sum(1 for c in range(w) if g[0][c]==7)
    rank=max(1,min(3,rank))
    gg=copy_grid(g)
    for (r,c) in corners:
        if gg[r][c]==9: gg[r][c]=0
    for c in range(w):
        if gg[0][c]==7: gg[0][c]=0
    frames=scan_rect_frames(gg, frame_color=8)
    if not frames:
        return blank(h,w)
    frame=max(frames, key=lambda fr: fr['interior_area'])
    # remove frame cells for object search
    for r in range(frame['bbox'][0], frame['bbox'][2]+1):
        for c in range(frame['bbox'][1], frame['bbox'][3]+1):
            if r in (frame['bbox'][0], frame['bbox'][2]) or c in (frame['bbox'][1], frame['bbox'][3]):
                gg[r][c]=0
    comps=find_components(gg)
    comps=[comp for comp in comps if comp['color'] not in (7,8,9)]
    comps.sort(key=lambda comp:(comp['area'], comp['bbox']))
    chosen=comps[rank-1]
    sub=crop_bbox(gg, chosen['cells'])
    sub=transform_grid(sub, code)
    out=blank(h,w)
    r0,c0,r1,c1=frame['bbox']
    for c in range(c0,c1+1):
        out[r0][c]=8; out[r1][c]=8
    for r in range(r0,r1+1):
        out[r][c0]=8; out[r][c1]=8
    ih,iw=r1-r0-1,c1-c0-1
    ph,pw=dims(sub)
    sr=r0+1 + max(0,(ih-ph)//2)
    sc=c0+1 + max(0,(iw-pw)//2)
    for r,row in enumerate(sub):
        for c,v in enumerate(row):
            if v!=0 and sr+r<r1 and sc+c<c1:
                out[sr+r][sc+c]=v
    return out
```

**Train 1 input**
```text
9 7 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 3 0 0 0 0 0 0 8 0 0 0 8 0
0 3 3 0 0 0 0 0 8 0 0 0 8 0
0 0 4 0 0 0 0 0 8 0 0 0 8 0
0 4 4 4 0 0 0 0 8 0 0 0 8 0
0 0 4 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 3 0 0 8 0
0 0 0 0 0 0 0 0 8 3 3 0 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 7 7 7 0 0 0 0 0 0 0 0 0 0 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 8 8 8 8 8 0
0 2 0 0 0 0 0 0 0 8 0 0 0 8 0
0 4 4 4 0 0 0 0 0 8 0 0 0 8 0
0 0 4 0 0 0 0 0 0 8 0 0 0 8 0
0 0 6 0 0 0 0 0 0 8 0 0 0 8 0
0 6 6 6 0 0 0 0 0 8 0 0 0 8 0
0 0 6 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 0 6 0 8 0
0 0 0 0 0 0 0 0 0 8 6 6 6 8 0
0 0 0 0 0 0 0 0 0 8 0 6 0 8 0
0 0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 7 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0 8 8 8 8 0
0 0 5 5 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 7 0 0 0 0 0 0 8 0 0 8 0
0 0 7 7 7 0 0 0 0 0 8 0 0 8 0
0 0 0 7 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0
9 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 3 0 8 0
0 0 0 0 0 0 0 0 0 0 8 3 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 7 7 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 4 4 4 0 0 0 0 8 0 0 0 8 0
0 0 4 0 0 0 0 0 8 0 0 0 8 0
0 0 6 0 0 0 0 0 8 0 0 0 8 0
0 6 6 6 0 0 0 0 8 0 0 0 8 0
0 0 6 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 9
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 0 4 0 8 0
0 0 0 0 0 0 0 0 8 4 4 4 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_n04 — Overlay two normalized shapes with relation colors

**Written rule:** Crop the two input objects separately, align both crops at the top-left corner of a shared canvas, then color cells that belong only to the first object as 2, only to the second as 3, and to both as 8.

**Program function:** `solve_hard_n04`

**Primitives:** normalized_overlap_palette

```python
def solve_hard_n04(g):
    comps=find_components(g)
    if len(comps)<2:
        return crop_nonzero(g)
    # choose two largest components by area then bbox
    comps.sort(key=lambda comp:(comp['bbox'][0], comp['bbox'][1]))
    a,b=comps[:2]
    suba=crop_bbox(g, a['cells']); subb=crop_bbox(g,b['cells'])
    cellsa={(r,c) for r,row in enumerate(suba) for c,v in enumerate(row) if v!=0}
    cellsb={(r,c) for r,row in enumerate(subb) for c,v in enumerate(row) if v!=0}
    h=max(len(suba), len(subb)); w=max(len(suba[0]), len(subb[0]))
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            ina=(r,c) in cellsa
            inb=(r,c) in cellsb
            out[r][c]=8 if ina and inb else 2 if ina else 3 if inb else 0
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 3 3 3 0 0 0
0 2 0 0 0 0 0 0 0 3 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 3 3
2 3 0
2 2 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 0
3 8 2
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 2 0
8 8 2
0 2 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 2
0 8 3
```

### hard_n05 — Shortest path with key and locked door

**Written rule:** Draw the shortest route from 2 to 3 using color 4 on empty floor cells. Walls are 5. Door cells 7 are blocked until the path has first collected the key 6. Keep start, goal, key, door, and walls unchanged.

**Program function:** `solve_hard_n05`

**Primitives:** keydoor_bfs_path

```python
def solve_hard_n05(g):
    h,w=dims(g)
    start=goal=keypos=None
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
            elif v==6: keypos=(r,c)
    q=deque([(start[0],start[1],False)])
    prev={(start[0],start[1],False):None}
    end_state=None
    while q:
        r,c,has_key=q.popleft()
        if (r,c)==goal:
            end_state=(r,c,has_key); break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            v=g[nr][nc]
            if v==5: continue
            if v==7 and not has_key: continue
            nk=has_key or (v==6)
            st=(nr,nc,nk)
            if st not in prev:
                prev[st]=(r,c,has_key)
                q.append(st)
    out=copy_grid(g)
    if end_state is None:
        return out
    cur=end_state
    while cur is not None:
        r,c,has_key=cur
        if out[r][c]==0:
            out[r][c]=4
        cur=prev[cur]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 5 0 0 5 0 0
0 0 0 6 0 5 0 0 5 0 0
0 0 0 0 0 7 0 0 5 0 0
0 2 0 0 0 7 0 0 0 3 0
0 0 0 0 0 7 0 0 5 0 0
0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 5 0 0 5 0 0
0 4 4 6 0 5 0 0 5 0 0
0 4 0 4 0 7 0 0 5 0 0
0 2 0 4 4 7 4 4 4 3 0
0 0 0 0 0 7 0 0 5 0 0
0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 5 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 5 0 0
5 5 5 5 5 5 7 7 7 5 5 5
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 6 0 0 0 0 0 0 0 0
0 2 0 4 0 0 0 0 0 5 0 0
0 0 0 4 0 0 0 0 0 5 0 0
0 0 0 4 4 4 4 0 0 5 0 0
5 5 5 5 5 5 7 7 7 5 5 5
0 0 0 0 5 0 4 0 0 0 0 0
0 0 0 0 5 0 4 4 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 5 0 0 7 0 0 0 0
0 2 0 0 5 0 0 7 0 0 3 0
0 0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 0 0 5 0 5 0 0
0 0 0 6 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 5 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 5 0 0 7 0 0 0 0
0 2 0 0 5 4 4 7 4 4 3 0
0 4 0 4 4 4 0 7 0 0 0 0
0 4 0 4 5 0 0 5 0 0 0 0
0 4 0 4 0 0 0 5 0 5 0 0
0 4 4 6 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 5 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 5 0 0
5 5 5 5 5 7 7 7 5 5 5
0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 4 4 6 0 0 0 0 0 0 0
0 2 0 4 0 0 0 0 5 0 0
0 0 0 4 0 0 0 0 5 0 0
0 0 0 4 4 4 0 0 5 0 0
5 5 5 5 5 7 7 7 5 5 5
0 0 0 0 5 4 0 0 0 0 0
0 0 0 0 5 4 4 4 4 3 0
0 0 0 0 0 0 0 0 0 0 0
```

### hard_n06 — Decode a Ferrers shape from row and column headers

**Written rule:** The top-right quadrant gives column heights with blue bars, and the bottom-left quadrant gives row lengths with red bars. Decode the shared Ferrers diagram and output it in color 8.

**Program function:** `solve_hard_n06`

**Primitives:** dual_header_ferrers

```python
def solve_hard_n06(g):
    h,w=dims(g)
    H=h//2; W=w//2
    # decode row lengths from bottom-left quadrant color 3
    row_lengths=[]
    for r in range(H,2*H):
        L=0
        for c in range(W):
            if g[r][c]==3: L+=1
        row_lengths.append(L)
    out=blank(H,W)
    for r,L in enumerate(row_lengths):
        for c in range(min(L,W)):
            out[r][c]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
8 8 8 8 8
8 8 8 0 0
8 8 0 0 0
8 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 2 2 0 0
0 0 0 0 2 2 2 2
0 0 0 0 2 2 2 2
3 3 3 3 0 0 0 0
3 3 3 3 0 0 0 0
3 3 0 0 0 0 0 0
```

**Train 2 output**
```text
8 8 8 8
8 8 8 8
8 8 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 2 2 2 2 0 0
0 0 0 0 0 0 2 2 2 2 2 2
3 3 3 3 3 3 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0 0
3 3 3 3 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
8 8 8 8 8 8
8 8 8 8 0 0
8 8 8 8 0 0
8 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 2 2 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0
3 3 3 3 3 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
8 8 8 8 8
8 8 8 8 8
8 8 8 0 0
8 8 0 0 0
```

### hard_n07 — Assign each object to the frame with matching area

**Written rule:** Each non-frame object must move into the 8-frame whose interior area matches that object’s area. Center the object inside its matched frame and clear the originals.

**Program function:** `solve_hard_n07`

**Primitives:** area_socket_assignment

```python
def solve_hard_n07(g):
    h,w=dims(g)
    frames=scan_rect_frames(g, frame_color=8)
    out=blank(h,w)
    # remove frame cells from grid to find objects
    frame_cells=set()
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        for c in range(c0,c1+1):
            frame_cells.add((r0,c)); frame_cells.add((r1,c))
        for r in range(r0,r1+1):
            frame_cells.add((r,c0)); frame_cells.add((r,c1))
    gg=copy_grid(g)
    for r,c in frame_cells:
        gg[r][c]=0
    objs=find_components(gg, ignore_colors={8})
    # place frames
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        for c in range(c0,c1+1):
            out[r0][c]=8; out[r1][c]=8
        for r in range(r0,r1+1):
            out[r][c0]=8; out[r][c1]=8
    used=set()
    # match by exact area
    frames_sorted=sorted(frames, key=lambda fr:(fr['interior_area'], fr['bbox']))
    objs_sorted=sorted(objs, key=lambda ob:(ob['area'], ob['bbox']))
    for fr in frames_sorted:
        target_area=fr['interior_area']
        cand=None
        for i,ob in enumerate(objs_sorted):
            if i in used: continue
            if ob['area']==target_area:
                cand=(i,ob); break
        if cand is None: 
            continue
        i,ob=cand; used.add(i)
        sub=crop_bbox(gg, ob['cells'])
        r0,c0,r1,c1=fr['bbox']
        ih,iw=r1-r0-1,c1-c0-1
        sh,sw=dims(sub)
        sr=r0+1+max(0,(ih-sh)//2)
        sc=c0+1+max(0,(iw-sw)//2)
        for r,row in enumerate(sub):
            for c,v in enumerate(row):
                if v!=0 and sr+r<r1 and sc+c<c1:
                    out[sr+r][sc+c]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 8 8 8 8 0 0
0 2 2 0 0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 6 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 8 8 8 8 0 0 0 8 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 8 8 8 8 8 0 0
0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 8 8 8 8 0 0 0 8 4 0 0 8 0 0
0 0 8 2 2 8 0 0 0 8 8 8 8 8 0 0
0 0 8 2 2 8 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 2 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 6 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 6 6 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 2 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 6 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 4 4 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 4 8 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 2 2 2 0 0 0 0 0 0 0 8 0 0 8 0 0
0 0 2 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 6 6 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 6 6 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 8 4 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 8 0 0 2 0 0 8 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 2 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 6 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 6 6 6 0 8 0 0 8 0 0 0
0 0 0 0 0 0 0 6 0 0 8 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 2 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 4 4 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 4 4 8 0 0 0
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 8 0 0 6 0 0 8 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

