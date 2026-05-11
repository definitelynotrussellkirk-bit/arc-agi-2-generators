# ARC Puzzle Bank — Set 17
This bundle contains 21 new ARC-style puzzles, split 7 easy / 7 medium / 7 hard.

This batch pushes into a different slice of the ARC space: ring completion, marker-driven docking, diagonal voting, room logic, hull filling, frame summarization, reflected beams, graph outputs, orbit stamping, visibility unions, object-to-frame assignment, and ordered checkpoint pathfinding.

Artifacts in this bundle:
- `arc_puzzle_bank_21_set17.json` — machine-readable task data
- `arc_puzzle_bank_21_set17_solutions.py` — reference Python solvers
- `arc_puzzle_bank_21_set17_validation.txt` — validation log

## Easy (7)

### easy_p01 — Complete one-hole 3x3 rings

**Written rule:** Whenever seven cells of a 3x3 ring are the same nonzero color and the eighth ring cell is missing, fill the missing ring cell with that color.

**Program function:** `solve_easy_p01`

**Primitives:** ring_gap_fill

```python
def solve_easy_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    ring=[(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
    for r in range(h-2):
        for c in range(w-2):
            vals=[g[r+dr][c+dc] for dr,dc in ring]
            nz=[v for v in vals if v!=0]
            if len(set(nz))==1 and len(nz)==7 and vals.count(0)==1 and g[r+1][c+1]==0:
                miss=vals.index(0)
                dr,dc=ring[miss]
                out[r+dr][c+dc]=nz[0]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 0 6 6 6 0
0 0 0 0 6 0 6 0
0 0 0 0 6 0 6 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 3 0 3 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 0 6 6 6 0
0 0 0 0 6 0 6 0
0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0
0 0 0 0 0 2 0 2 0
0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 2 0
0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 7 0 7 0 0 0 0 0
0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8 0
0 4 0 4 0 0 8 0 8 0
0 4 4 0 0 0 0 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0
0 0 0 9 0 9 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8 0
0 4 0 4 0 0 8 0 8 0
0 4 4 4 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 9 0 9 0 0 0 0
0 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 3 3 3 0
0 5 0 5 0 0 3 0 0 0
0 5 5 5 0 0 3 3 3 0
0 0 0 0 7 0 7 0 0 0
0 0 0 0 7 0 7 0 0 0
0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 0 0 3 3 3 0
0 5 0 5 0 0 3 0 3 0
0 5 5 5 0 0 3 3 3 0
0 0 0 0 7 7 7 0 0 0
0 0 0 0 7 0 7 0 0 0
0 0 0 0 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### easy_p02 — Dock row segments by border marker

**Written rule:** A marker 1 on the far left means slide that row’s colored segment flush left. A marker 2 on the far right means slide that row’s colored segment flush right. Remove the markers.

**Program function:** `solve_easy_p02`

**Primitives:** row_dock_by_marker

```python
def solve_easy_p02(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        row=g[r]
        if row[0]==1:
            vals=[v for v in row if v not in (0,1,2)]
            for i,v in enumerate(vals):
                out[r][i]=v
        elif row[-1]==2:
            vals=[v for v in row if v not in (0,1,2)]
            start=w-len(vals)
            for i,v in enumerate(vals):
                out[r][start+i]=v
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
1 0 0 0 4 4 4 0 0 0
0 0 0 7 7 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 3 3 3 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
9 9 9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0 2
1 0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6
5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9
0 0 0 0 0 0 0 0 0 0 0 0
```

### easy_p03 — Fill X-centers from diagonal agreement

**Written rule:** If the four diagonal neighbors around an empty cell are all the same nonzero color, fill the center cell with that color.

**Program function:** `solve_easy_p03`

**Primitives:** diagonal_vote_fill

```python
def solve_easy_p03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0:
                vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
                if vals[0]!=0 and all(v==vals[0] for v in vals):
                    out[r][c]=vals[0]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 4 0 4 0 0 0
0 0 0 0 0 0 0
0 4 0 4 7 0 7
0 0 0 0 0 0 0
0 0 0 0 7 0 7
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 4 0 4 0 0 0
0 0 4 0 0 0 0
0 4 0 4 7 0 7
0 0 0 0 0 7 0
0 0 0 0 7 0 7
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0
0 0 0 0 0 3 0 0
0 0 0 0 3 0 3 0
0 6 0 6 0 0 0 0
0 0 6 0 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 5 0 5 0 2 0 2 0
0 0 0 0 0 0 0 0 0
0 5 0 5 0 2 0 2 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 0 0 8 0 0 0 0 0
0 0 8 0 8 0 0 0 0
0 5 0 5 0 2 0 2 0
0 0 5 0 0 0 2 0 0
0 5 0 5 0 2 0 2 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 9 0 9 0 0 0 0
0 0 0 9 0 0 0 0 0
0 0 9 0 9 0 0 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 4 0 4 0
0 0 0 0 0 0 0 0 0
```

### easy_p04 — Grow dominos into 2x2 squares

**Written rule:** Every isolated two-cell domino grows into the full 2x2 square covering its bounding box.

**Program function:** `solve_easy_p04`

**Primitives:** domino_square_expand

```python
def solve_easy_p04(g):
    out=copy_grid(g)
    for comp in comp_same_color(g):
        cells=comp['cells']; color=comp['color']
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=sorted(cells)
        if r1==r2 and abs(c1-c2)==1:
            r=r1; c=min(c1,c2)
            for rr in (r,r+1):
                for cc in (c,c+1):
                    if inb(out,rr,cc):
                        out[rr][cc]=color
        elif c1==c2 and abs(r1-r2)==1:
            r=min(r1,r2); c=c1
            for rr in (r,r+1):
                for cc in (c,c+1):
                    if inb(out,rr,cc):
                        out[rr][cc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0
0 3 3 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 6 0
0 0 0 0 0 6 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0
0 3 3 0 0 0 0
0 3 3 0 0 0 0
0 0 0 0 0 6 6
0 0 0 0 0 6 6
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 0
0 0 0 4 0 0 9 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9
0 0 0 4 4 0 9 9
0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0
0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0
0 2 2 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0
0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0
0 2 2 0 0 8 8 0 0
0 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 6 6 0 0 0 7 7 0
0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0
```

### easy_p05 — Bridge one-cell orthogonal gaps

**Written rule:** If a zero cell lies exactly between two matching nonzero cells horizontally or vertically, fill the gap with that color.

**Program function:** `solve_easy_p05`

**Primitives:** one_gap_bridge

```python
def solve_easy_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            if 0<c<w-1 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
            if 0<r<h-1 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 7 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0
0 2 2 2 0 0 7 0 0
0 0 0 0 0 0 7 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 5 0 5 0 0 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0
0 0 5 5 5 0 3 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 4 0
0 0 8 0 8 0 0 0 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 4 0
0 0 8 8 8 0 0 4 0
0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 0 9 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 9 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
```

### easy_p06 — Reduce horizontal runs to their middles

**Written rule:** Replace each horizontal nonzero run by just its middle cell.

**Program function:** `solve_easy_p06`

**Primitives:** run_middle_keep

```python
def solve_easy_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]
            c2=c
            while c2<w and g[r][c2]==color:
                c2+=1
            length=c2-c
            mid=c + length//2
            out[r][mid]=color
            c=c2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0
4 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 6 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 9 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

### easy_p07 — Echo cells across the main diagonal

**Written rule:** Copy every nonzero cell to its transposed position across the main diagonal, keeping the original cells too.

**Program function:** `solve_easy_p07`

**Primitives:** main_diagonal_echo

```python
def solve_easy_p07(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0
0 0 0 0 3 0
0 0 0 0 0 7
0 0 0 0 0 0
0 6 0 0 0 0
0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0
0 0 0 0 6 0
0 0 0 0 0 7
0 0 0 0 0 0
0 3 0 0 0 0
0 0 7 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0
0 0 0 0 0 4 0
0 0 0 0 4 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 8 0 0 0 0
0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0
0 0 0 0 0 4 0
0 0 0 0 4 8 0
0 0 0 0 0 0 0
0 0 4 0 0 0 0
0 4 8 0 0 0 0
0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 5
0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 5
0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0
0 2 0 0 0 0 0 0
0 0 5 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0
0 0 0 0 6 0 0
0 0 0 0 0 0 3
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 9 0 0 0 0 0
0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0
0 0 0 0 6 9 0
0 0 0 0 0 0 3
0 0 0 0 0 0 0
0 6 0 0 0 0 0
0 9 0 0 0 0 0
0 0 3 0 0 0 0
```

## Medium (7)

### medium_p01 — Select an object by one corner and transform it by the other

**Written rule:** The top-left corner names the object color to extract. The top-right corner names the transform to apply: 1=identity, 2=rotate90, 3=rotate180, 4=flip horizontally. Output only the transformed crop of the selected object.

**Program function:** `solve_medium_p01`

**Primitives:** dual_corner_select_transform

```python
def solve_medium_p01(g):
    h,w=dims(g)
    sel=g[0][0]
    code=g[0][w-1]
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==sel and not (r==0 and c in (0,w-1))]
    if not cells:
        return [[0]]
    obj,_=crop_component(g,cells)
    return apply_transform_code(obj, code)
```

**Train 1 input**
```text
4 0 0 0 0 0 0 2
0 0 0 0 7 7 0 0
0 0 0 0 0 7 7 0
0 4 4 4 0 0 0 0
0 0 4 0 0 0 0 0
0 0 0 0 0 6 0 0
0 0 0 0 0 6 0 0
0 0 0 0 0 6 6 0
```

**Train 1 output**
```text
0 4
4 4
0 4
```

**Train 2 input**
```text
6 0 0 0 0 0 0 0 3
0 0 0 0 0 4 4 0 0
0 6 0 0 0 0 4 0 0
0 6 0 0 0 0 4 4 0
0 6 6 0 0 0 0 0 0
0 0 0 0 7 7 7 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 6
0 6
0 6
```

**Train 3 input**
```text
7 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 3 3 3 0 0 5 0 0 0
0 0 3 0 0 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 7 7
7 7 0
```

**Test 1 input**
```text
5 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 5 5 0 0 0
0 6 6 0 0 0 5 0 0 0
0 0 8 8 0 0 5 5 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 5
5 5 5
5 0 0
```

### medium_p02 — Turn object areas into a bottom-aligned bar gallery

**Written rule:** Replace each connected object by a one-column vertical bar of the same color whose height equals the object’s area. Sort bars by descending area and pack them left to right with one zero spacer column between bars.

**Program function:** `solve_medium_p02`

**Primitives:** area_bar_gallery

```python
def solve_medium_p02(g):
    comps=comp_same_color(g)
    comps.sort(key=lambda comp:(-len(comp['cells']), bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']))
    heights=[len(comp['cells']) for comp in comps]
    H=max(heights) if heights else 1
    W=max(1, 2*len(comps)-1)
    out=blank(H,W)
    col=0
    for comp in comps:
        hgt=len(comp['cells']); color=comp['color']
        for r in range(H-hgt, H):
            out[r][col]=color
        col+=2
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 0 3 0 0 6 0 0
0 3 3 3 0 6 0 0
0 0 3 0 0 6 6 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
3 0 0 0 0
3 0 6 0 0
3 0 6 0 0
3 0 6 0 4
3 0 6 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 0 5 0
0 0 0 0 0 0 0 5 0
0 7 7 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
2 0 7 0 0 0 0
2 0 7 0 0 0 0
2 0 7 0 5 0 8
2 0 7 0 5 0 8
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 4 0 0 0
0 0 9 0 0 0 4 0 0 0
0 0 9 9 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 6 0 0 0 0 3 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
9 0 0 0 0 0 0
9 0 4 0 6 0 0
9 0 4 0 6 0 0
9 0 4 0 6 0 3
9 0 4 0 6 0 3
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 0 3 3 0 0
0 7 0 0 0 0 0 3 3 0
0 7 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
7 0 0 0 0
7 0 3 0 0
7 0 3 0 0
7 0 3 0 5
7 0 3 0 5
```

### medium_p03 — Flood each framed room from its seed

**Written rule:** Each hollow rectangular room has one colored seed inside. Fill the entire interior of that room with the seed color while keeping the walls unchanged.

**Program function:** `solve_medium_p03`

**Primitives:** seeded_room_fill

```python
def solve_medium_p03(g):
    out=copy_grid(g)
    for fr in frame_components(g):
        r0,c0,r1,c1=fr['bbox']
        seeds=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0, fr['color'])]
        if len(seeds)==1:
            seed=seeds[0]
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=seed
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 0 0 0 5 0 5 5 5 5 0
0 5 0 2 0 5 0 5 0 0 5 0
0 5 0 0 0 5 0 5 8 0 5 0
0 5 5 5 5 5 0 5 0 0 5 0
0 0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 2 2 2 5 0 5 5 5 5 0
0 5 2 2 2 5 0 5 8 8 5 0
0 5 2 2 2 5 0 5 8 8 5 0
0 5 5 5 5 5 0 5 8 8 5 0
0 0 0 0 0 0 0 5 8 8 5 0
0 0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0
0 5 0 7 0 5 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0
0 5 0 0 0 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 5 0
0 0 0 0 0 0 5 3 0 5 0
0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0
0 5 0 7 0 5 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0
0 5 0 0 0 5 5 5 5 5 0
0 5 5 5 5 5 5 0 0 5 0
0 0 0 0 0 0 5 3 0 5 0
0 0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 5 0 4 0 0 5 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 5 5 5 5 5 5 5 5 5 0
0 5 5 5 5 5 0 0 5 0 5 0
0 5 0 0 0 5 0 0 5 6 5 0
0 5 0 9 0 5 0 0 5 0 5 0
0 5 0 0 0 5 0 0 5 0 5 0
0 5 5 5 5 5 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 5 0 4 0 0 5 0 0 0 0
0 0 5 0 0 0 0 5 0 0 0 0
0 0 5 5 5 5 5 5 5 5 5 0
0 5 5 5 5 5 0 0 5 0 5 0
0 5 0 0 0 5 0 0 5 6 5 0
0 5 0 9 0 5 0 0 5 0 5 0
0 5 0 0 0 5 0 0 5 0 5 0
0 5 5 5 5 5 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 0 8 0 5 0 0 5 2 0 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 5 5 5 5 0 0 5 0 0 5 0
0 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 0 5 0 0 7 0 5 0 0 0
0 0 0 0 5 0 0 0 0 5 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 5 5 5 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 0 8 0 5 0 0 5 2 0 5 0
0 5 0 0 0 5 0 0 5 0 0 5 0
0 5 5 5 5 5 0 0 5 0 0 5 0
0 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 0 5 0 0 7 0 5 0 0 0
0 0 0 0 5 0 0 0 0 5 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_p04 — Fill the hull spanning each color’s two components

**Written rule:** Whenever a color appears in exactly two separate components, fill the full bounding rectangle spanning both components with that same color.

**Program function:** `solve_medium_p04`

**Primitives:** pair_hull_fill

```python
def solve_medium_p04(g):
    out=copy_grid(g)
    by_color=defaultdict(list)
    for comp in comp_same_color(g):
        by_color[comp['color']].append(comp['cells'])
    for color, comps in by_color.items():
        if len(comps)==2:
            allcells=[cell for comp in comps for cell in comp]
            r0,c0,r1,c1=bbox(allcells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0
0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0
0 2 2 2 2 0 0 0
0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 0
0 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 8 0
0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 8 8 0
0 3 3 3 3 0 8 8 0
0 3 3 3 3 0 8 8 0
0 3 3 3 3 0 0 0 0
0 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 9 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 9 0 0
0 0 9 9 9 9 9 9 0 0
0 0 9 9 9 9 9 9 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 6 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### medium_p05 — Mirror a pattern according to a corner marker

**Written rule:** A 1 in the top-left corner means reflect the pattern across the vertical axis of the full grid. A 2 means reflect it across the horizontal axis. Remove the marker and keep both the original cells and their mirror image.

**Program function:** `solve_medium_p05`

**Primitives:** marker_axis_mirror

```python
def solve_medium_p05(g):
    h,w=dims(g)
    marker=g[0][0]
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if (r,c)==(0,0):
                continue
            v=g[r][c]
            if v==0:
                continue
            out[r][c]=v
            if marker==1:
                out[r][w-1-c]=v
            elif marker==2:
                out[h-1-r][c]=v
    return out
```

**Train 1 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 6 0
0 6 0 0 0 0 0 6 0
0 6 6 0 0 0 6 6 0
0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
2 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0
0 0 3 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0
0 0 3 0 0 7 7 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 3 0 0 7 7 0
0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0
0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 5 5 0
0 0 5 0 0 0 5 0 0
0 0 5 5 0 5 5 0 0
0 0 8 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 9 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 9 0 0 0 4 4 0 0
0 0 9 0 0 0 4 4 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### medium_p06 — Reduce each seeded frame to one center label

**Written rule:** For each hollow rectangular frame, look at the one colored seed inside it. Output a blank grid with a single cell at the frame’s center colored like that seed.

**Program function:** `solve_medium_p06`

**Primitives:** frame_center_label

```python
def solve_medium_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for fr in frame_components(g):
        r0,c0,r1,c1=fr['bbox']
        seeds=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0, fr['color'])]
        if len(seeds)==1:
            cr=(r0+r1)//2; cc=(c0+c1)//2
            out[cr][cc]=seeds[0]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0
0 3 0 8 0 3 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0
0 3 3 3 3 3 6 6 6 6 6
0 0 0 0 0 0 6 0 0 0 6
0 0 0 0 0 0 6 0 2 0 6
0 0 0 0 0 0 6 0 0 0 6
0 0 0 0 0 0 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 0 0 0 0
0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 4 0 0 7 0 0 4 0 0 0 0
0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 4 0 0 0 0 0 4 0 0 0 0
0 0 4 4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 0 9 0 0 0 9
0 0 0 0 0 0 0 0 9 0 3 0 9
0 0 0 0 0 0 0 0 9 0 0 0 9
0 0 0 0 0 0 0 0 9 9 9 9 9
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0 0 0
0 7 0 2 0 7 0 5 5 5 5 5
0 7 0 0 0 7 0 5 0 0 0 5
0 7 7 7 7 7 0 5 0 8 0 5
0 0 0 0 0 0 0 5 0 0 0 5
0 0 0 0 0 0 0 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 0 0 0 0 0
0 8 0 4 0 8 0 0 0 0 0 0 0
0 8 0 0 0 8 2 2 2 2 2 2 2
0 8 8 8 8 8 2 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 7 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 2 0 0 0 0 0 2
0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### medium_p07 — Replace each object by the cross of its bounding box

**Written rule:** For every connected object, compute its tight bounding box and draw the center row and center column of that box in the object’s color on an otherwise blank grid.

**Program function:** `solve_medium_p07`

**Primitives:** bbox_cross

```python
def solve_medium_p07(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in comp_same_color(g):
        color=comp['color']
        r0,c0,r1,c1=bbox(comp['cells'])
        cr=(r0+r1)//2
        cc=(c0+c1)//2
        for c in range(c0,c1+1):
            out[cr][c]=color
        for r in range(r0,r1+1):
            out[r][cc]=color
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 7 7 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 7 7 0 0
0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 0 9 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 0 0 0
0 0 0 9 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Hard (7)

### hard_p01 — Trace a reflected beam through mirrors

**Written rule:** A border source emits a beam inward. Color 1 is a slash mirror, color 2 is a backslash mirror, and color 5 is a wall. Trace the beam through reflections and color every empty cell it traverses with the source color.

**Program function:** `solve_hard_p01`

**Primitives:** mirror_beam

```python
def solve_hard_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    sources=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] not in (0,SLASH,BACKSLASH,WALL)]
    if not sources:
        return out
    r,c,color=sources[0]
    if r==0: d=2
    elif r==h-1: d=0
    elif c==0: d=1
    else: d=3
    visited=set()
    while True:
        state=(r,c,d)
        if state in visited:
            break
        visited.add(state)
        dr,dc=DIRS[d]
        nr,nc=r+dr,c+dc
        if not (0<=nr<h and 0<=nc<w):
            break
        cell=g[nr][nc]
        if cell==WALL:
            break
        if cell==0:
            out[nr][nc]=color
            r,c=nr,nc
        elif cell in (SLASH,BACKSLASH):
            d=reflect(d,cell)
            r,c=nr,nc
        else:
            # treat other colored cells as pass-through and recolor? not used
            out[nr][nc]=cell
            r,c=nr,nc
    return out
```

**Train 1 input**
```text
0 0 7 0 0 0 0 0
0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0
0 0 2 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 7 0 0 0 0 0
0 0 7 0 0 5 0 0
0 0 7 0 0 7 0 0
0 0 2 7 7 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 1 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
7 0 0 0 1 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0
0 1 7 7 2 0 0 0 0
0 7 0 0 7 0 0 0 0
0 7 0 0 7 0 0 0 0
7 7 7 7 1 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 1 7 7 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 7 0 0 0
```

**Test 1 input**
```text
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 7 0 0 7 0 0
0 0 0 0 7 0 0 7 0 0
0 0 0 0 7 0 0 7 0 0
0 0 0 0 2 7 7 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### hard_p02 — Select, transform, and insert into the chosen frame

**Written rule:** The top-left corner selects which object color to use. The top-right corner selects the transform (1=identity, 2=rotate90, 3=rotate180, 4=flip horizontally). The bottom-left corner selects which frame color to keep. Output only that frame with the transformed selected object centered inside it.

**Program function:** `solve_hard_p02`

**Primitives:** corner_select_transform_insert

```python
def solve_hard_p02(g):
    h,w=dims(g)
    sel_color=g[0][0]
    code=g[0][w-1]
    target_frame_color=g[h-1][0]
    # selected object
    obj_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==sel_color and (r,c) not in [(0,0),(0,w-1),(h-1,0)]]
    if not obj_cells:
        return [[0]]
    obj,_=crop_component(g,obj_cells)
    obj=apply_transform_code(obj, code)
    # target frame
    target=None
    for fr in frame_components(g):
        if fr['color']==target_frame_color:
            target=fr
            break
    out=blank(h,w)
    if not target:
        return out
    r0,c0,r1,c1=target['bbox']
    for r,c in target['cells']:
        out[r][c]=target_frame_color
    ih,iw=r1-r0-1,c1-c0-1
    oh,ow=dims(obj)
    sr=r0+1+(ih-oh)//2
    sc=c0+1+(iw-ow)//2
    for r in range(oh):
        for c in range(ow):
            if obj[r][c]!=0:
                out[sr+r][sc+c]=obj[r][c]
    return out
```

**Train 1 input**
```text
6 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 3 0 0 0 0
0 6 6 6 0 0 3 0 0 0 0
0 6 0 0 0 0 3 3 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0
0 7 7 7 7 8 0 0 0 8 0
0 7 0 0 7 8 0 0 0 8 0
0 7 0 0 7 8 0 0 0 8 0
0 7 0 0 7 8 8 8 8 8 0
8 7 7 7 7 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 8 6 6 6 8 0
0 0 0 0 0 8 0 0 6 8 0
0 0 0 0 0 8 0 0 6 8 0
0 0 0 0 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
3 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 4 4 0 0 0
0 0 3 0 0 0 0 0 4 0 0 0
0 0 3 3 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 9 9 9 9 9
0 7 0 0 7 0 0 9 0 0 0 9
0 7 0 0 7 0 0 9 0 0 0 9
0 7 0 0 7 0 0 9 0 0 0 9
0 7 7 7 7 0 0 9 9 9 9 9
7 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
0 7 0 3 7 0 0 0 0 0 0 0
0 7 0 3 7 0 0 0 0 0 0 0
0 7 3 3 7 0 0 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
4 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 6 6 0 0
0 0 4 0 0 0 0 0 0 6 6 0
0 0 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 0 7 7 7 7
0 0 9 0 0 0 9 0 7 0 0 7
0 0 9 0 0 0 9 0 7 0 0 7
0 0 9 0 0 0 9 0 7 0 0 7
0 0 9 9 9 9 9 0 7 7 7 7
9 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0 0
0 0 9 4 4 0 9 0 0 0 0 0
0 0 9 0 4 0 9 0 0 0 0 0
0 0 9 0 4 4 9 0 0 0 0 0
0 0 9 9 9 9 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
5 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 5 5 0 0 0 0
0 0 6 0 0 0 0 0 5 0 0 0 0
0 0 6 6 0 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 7 7 7 7 0
0 8 0 0 0 8 0 0 7 0 0 7 0
0 8 0 0 0 8 0 0 7 0 0 7 0
0 8 0 0 0 8 0 0 7 0 0 7 0
0 8 8 8 8 8 0 0 7 7 7 7 0
8 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 5 8 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 0 0 0 0
0 8 5 0 0 8 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_p03 — Build an adjacency matrix after one-step dilation

**Written rule:** Order the objects by their top-left corners. Dilate each object by one orthogonal step. Output a square matrix whose diagonal cells are the object colors and whose off-diagonal cells are 8 exactly when the two dilated objects touch.

**Program function:** `solve_hard_p03`

**Primitives:** dilation_adjacency_matrix

```python
def solve_hard_p03(g):
    comps=comp_same_color(g)
    comps.sort(key=lambda comp:(bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']))
    n=len(comps)
    out=blank(n,n)
    dilated=[dilate_once(comp['cells']) for comp in comps]
    for i,comp in enumerate(comps):
        out[i][i]=comp['color']
    for i in range(n):
        for j in range(i+1,n):
            if dilated[i] & dilated[j]:
                out[i][j]=out[j][i]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0
0 2 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
2 8 0
8 3 0
0 0 4
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0
0 6 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
6 0 0
0 7 0
0 0 9
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0
0 3 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 8 0 0
0 0 7 0 0 0 0 0 0 0
0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
3 0 0 0
0 4 0 0
0 0 7 0
0 0 0 8
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0
0 0 2 0 0 6 0 0 0
0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
2 0 0 0
0 6 0 0
0 0 4 0
0 0 0 9
```

### hard_p04 — Stamp rotated orbit copies at anchor markers

**Written rule:** Take the base object of color 6. Stamp centered copies of it at every anchor marker: 1 means keep the orientation, 2 means rotate90, 3 means rotate180, and 4 means rotate270. Output only the stamped copies.

**Program function:** `solve_hard_p04`

**Primitives:** orbit_stamp

```python
def solve_hard_p04(g):
    h,w=dims(g)
    # anchor colors 1,2,3,4. base object is color 6
    base_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==6]
    obj,_=crop_component(g,base_cells)
    out=blank(h,w)
    anchors=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (1,2,3,4)]
    code_to_shape={1:obj,2:rotate90(obj),3:rotate180(obj),4:rotate270(obj)}
    for r,c,code in anchors:
        stamp_centered(out, code_to_shape[code], r, c)
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0
0 4 0 0 0 6 0 0 0 2 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 6
6 6 6 0 0 0 0 0 6 6 6
6 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 4 0 0 6 0 0 0 0 2 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 6 6 6 0
0 6 0 0 0 0 0 0 0 0 0 6 0
0 6 6 6 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 4 0 0 6 0 0 0 0 2 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 6 6 6 0
0 6 6 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 4 0 0 6 6 0 0 0 2 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 6 6 0
0 0 6 6 0 0 0 0 0 6 6 0 0
0 6 6 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_p05 — Combine orthogonal visibility fields

**Written rule:** Each watcher sees horizontally and vertically through empty cells until a wall (5). Cells seen by exactly one watcher take that watcher’s color; cells seen by multiple watcher colors become 8. Keep watchers and walls.

**Program function:** `solve_hard_p05`

**Primitives:** visibility_union

```python
def solve_hard_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    seen_map=defaultdict(set)  # cell -> colors
    watchers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (2,3,4)]
    for r,c,color in watchers:
        for dr,dc in DIR4:
            rr,cc=r+dr,c+dc
            while 0<=rr<h and 0<=cc<w and g[rr][cc]!=5:
                if g[rr][cc]==0:
                    seen_map[(rr,cc)].add(color)
                rr+=dr; cc+=dc
    for (r,c), colors in seen_map.items():
        if len(colors)==1:
            out[r][c]=next(iter(colors))
        elif len(colors)>=2:
            out[r][c]=8
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 3 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0
0 0 5 5 5 5 5 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 2 0 0 0 0 0 3 0
8 2 8 8 8 8 8 3 8
0 2 0 0 0 5 0 3 0
0 2 0 0 0 5 0 3 0
0 2 5 5 5 5 5 3 0
0 2 0 0 4 5 0 3 0
0 2 0 0 4 5 0 3 0
4 8 4 4 4 4 4 8 4
0 2 0 0 4 0 0 3 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 2 0 0 0 5 0 3 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 5 5 5 5 5 5 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 4 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 2 0 0 0 0 0 3 0
0 0 2 0 0 0 5 0 3 0
2 2 2 2 2 2 5 3 3 3
0 0 2 0 0 0 5 0 3 0
0 0 2 0 0 0 5 0 3 0
0 0 2 0 0 0 5 0 3 0
0 0 2 5 5 5 5 5 5 0
0 0 2 0 0 4 5 0 0 0
4 4 8 4 4 4 5 0 0 0
0 0 2 0 0 4 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 5 5 5 5 0 5 5 5 5 0
0 0 0 0 0 0 0 5 0 0 0
0 3 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 5 5 5 5 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 2 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 2 0 5 0 0 0
0 5 5 5 5 2 5 5 5 5 0
0 3 0 0 0 2 0 5 0 4 0
3 3 3 3 3 8 3 5 0 4 0
0 3 0 0 0 2 0 5 0 4 0
0 3 5 5 5 5 5 5 5 4 0
0 3 0 0 0 0 0 5 0 4 0
4 8 4 4 4 4 4 4 4 4 4
0 3 0 0 0 0 0 0 0 4 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 5 5 0 5 5 5 5 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 4 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 2 0 0 0 0 0 0 0 3 0
8 2 8 8 8 8 8 8 8 3 8
0 2 0 0 0 0 0 5 0 3 0
0 2 0 0 0 0 0 5 0 3 0
0 2 0 0 0 0 0 5 0 3 0
0 2 5 5 0 5 5 5 5 3 0
0 2 0 0 0 4 0 5 0 3 0
0 2 0 0 0 4 0 5 0 3 0
4 8 4 4 4 4 4 5 0 3 0
0 2 0 0 0 4 0 0 0 3 0
```

### hard_p06 — Match each object to the frame whose interior fits it

**Written rule:** Move each solid object into the hollow frame whose interior dimensions match the object’s bounding box, allowing a 90-degree rotation when needed. Keep the frames and clear the original object positions.

**Program function:** `solve_hard_p06`

**Primitives:** frame_fit_by_interior

```python
def solve_hard_p06(g):
    h,w=dims(g)
    frames=frame_components(g)
    # objects are non-frame components, ignore frames themselves
    frame_cells={(r,c) for fr in frames for r,c in fr['cells']}
    comps=[comp for comp in comp_same_color(g) if not all(cell in frame_cells for cell in comp['cells'])]
    # But this still includes frame cells as comps; filter exact frame sets
    frame_sets=[set(fr['cells']) for fr in frames]
    comps=[comp for comp in comps if set(comp['cells']) not in frame_sets]
    out=blank(h,w)
    used=set()
    # preserve all frames
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    # match by interior dims, allowing rotation
    for comp in comps:
        shape,_=crop_component(g, comp['cells'])
        sh,sw=dims(shape)
        choice=None
        rotshape=shape
        for idx,fr in enumerate(frames):
            if idx in used:
                continue
            r0,c0,r1,c1=fr['bbox']
            ih,iw=r1-r0-1,c1-c0-1
            if (sh,sw)==(ih,iw):
                choice=(idx,shape); break
            if (sw,sh)==(ih,iw):
                choice=(idx,rotate90(shape)); break
        if choice is None:
            continue
        idx,rotshape=choice
        used.add(idx)
        fr=frames[idx]
        r0,c0,r1,c1=fr['bbox']
        for r in range(len(rotshape)):
            for c in range(len(rotshape[0])):
                if rotshape[r][c]!=0:
                    out[r0+1+r][c0+1+c]=rotshape[r][c]
    return out
```

**Train 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 4 4 0 0 0 0
0 3 0 0 0 0 0 4 0 0 0 0
0 3 3 0 0 0 0 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 8 8 8 8 8 0
0 7 0 0 7 0 8 0 0 0 8 0
0 7 0 0 7 0 8 0 0 0 8 0
0 7 0 0 7 0 8 0 0 0 8 0
0 7 7 7 7 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 8 8 8 8 8 0
0 7 3 0 7 0 8 4 4 0 8 0
0 7 3 0 7 0 8 0 4 0 8 0
0 7 3 3 7 0 8 0 4 4 8 0
0 7 7 7 7 0 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 4 4 4 0 0 0 0
0 0 2 2 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 8 8 8 8
0 9 0 0 0 0 0 7 7 8 7 7 8
0 6 6 6 6 6 0 7 0 8 0 7 8
0 6 0 0 0 6 0 7 0 8 0 7 8
0 6 0 0 0 6 0 7 0 8 0 7 8
0 6 6 6 6 6 0 7 7 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 2 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 8 9 0 8
0 6 6 6 6 6 0 0 0 8 9 9 8
0 6 2 2 0 6 0 0 0 8 9 0 8
0 6 0 2 2 6 0 0 0 8 9 0 8
0 6 6 6 6 6 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Train 3 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 0 0 3 3 0 0 0 0 0
0 0 5 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 8 8 8 8 8 0 0
0 7 0 0 7 0 0 8 0 0 0 8 0 0
0 7 0 0 7 0 0 8 0 0 0 8 0 0
0 7 0 0 7 0 0 8 0 0 0 8 0 0
0 7 0 0 7 0 0 8 8 8 8 8 0 0
0 7 7 7 7 0 0 0 0 0 0 0 0 0
```

**Train 3 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 0 0 8 8 8 8 8 0 0
0 7 0 5 7 0 0 8 3 3 0 8 0 0
0 7 5 5 7 0 0 8 0 3 0 8 0 0
0 7 0 5 7 0 0 8 0 3 3 8 0 0
0 7 0 5 7 0 0 8 8 8 8 8 0 0
0 7 7 7 7 0 0 0 0 0 0 0 0 0
```

**Test 1 input**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 6 6 6 6 0 0 0 0 0
0 0 2 2 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 9 9 9 9 9
0 0 0 0 0 0 0 8 0 0 9 0 0 0 9
0 7 7 7 7 7 0 8 0 0 9 0 0 0 9
0 7 0 0 0 7 0 8 0 0 9 0 0 0 9
0 7 0 0 0 7 0 8 0 0 9 9 9 9 9
0 7 7 7 7 7 0 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Test 1 output**
```text
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 0 0 0 9 4 4 0 9
0 7 7 7 7 7 0 0 0 0 9 0 4 0 9
0 7 2 2 0 7 0 0 0 0 9 0 4 4 9
0 7 0 2 2 7 0 0 0 0 9 9 9 9 9
0 7 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

### hard_p07 — Find the shortest ordered checkpoint path

**Written rule:** In the maze, find the shortest orthogonal path that starts at 2, then visits 3, then 4, then ends at 6. Keep walls and markers, and color the traversed empty cells with 8.

**Program function:** `solve_hard_p07`

**Primitives:** ordered_checkpoint_path

```python
def solve_hard_p07(g):
    out=copy_grid(g)
    for r,c in bfs_path_with_checkpoints(g):
        if out[r][c]==0:
            out[r][c]=8
    return out
```

**Train 1 input**
```text
5 5 5 5 5 5 5 5 5
5 2 0 0 0 0 0 3 5
5 5 5 0 0 5 5 0 5
5 0 0 0 0 0 0 0 5
5 0 5 5 5 5 5 5 5
5 0 0 0 4 0 0 0 5
5 5 5 0 5 5 5 0 5
5 5 5 0 5 5 5 6 5
5 5 5 5 5 5 5 5 5
```

**Train 1 output**
```text
5 5 5 5 5 5 5 5 5
5 2 8 8 8 8 8 3 5
5 5 5 0 0 5 5 8 5
5 8 8 8 8 8 8 8 5
5 8 5 5 5 5 5 5 5
5 8 8 8 4 8 8 8 5
5 5 5 0 5 5 5 8 5
5 5 5 0 5 5 5 6 5
5 5 5 5 5 5 5 5 5
```

**Train 2 input**
```text
5 5 5 5 5 5 5 5 5 5
5 5 6 5 5 0 5 5 5 5
5 5 0 5 5 0 5 5 5 5
5 5 4 5 5 3 5 5 5 5
5 5 0 5 5 0 5 0 5 5
5 5 0 5 5 0 5 0 5 5
5 5 0 5 5 0 5 0 5 5
5 5 0 5 5 0 5 0 5 5
5 5 0 0 0 2 5 0 5 5
5 5 5 5 5 5 5 5 5 5
```

**Train 2 output**
```text
5 5 5 5 5 5 5 5 5 5
5 5 6 5 5 0 5 5 5 5
5 5 8 5 5 0 5 5 5 5
5 5 4 5 5 3 5 5 5 5
5 5 8 5 5 8 5 0 5 5
5 5 8 5 5 8 5 0 5 5
5 5 8 5 5 8 5 0 5 5
5 5 8 5 5 8 5 0 5 5
5 5 8 8 8 2 5 0 5 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 input**
```text
5 5 5 5 5 5 5 5 5 5
5 2 5 5 5 0 0 4 0 5
5 0 5 5 5 0 5 5 0 5
5 0 5 5 5 0 5 5 0 5
5 0 5 0 0 0 5 5 0 5
5 0 5 5 5 0 5 5 0 5
5 0 5 5 5 0 0 0 0 5
5 0 0 3 0 0 5 5 0 5
5 5 5 5 5 5 5 5 6 5
5 5 5 5 5 5 5 5 5 5
```

**Train 3 output**
```text
5 5 5 5 5 5 5 5 5 5
5 2 5 5 5 8 8 4 8 5
5 8 5 5 5 8 5 5 8 5
5 8 5 5 5 8 5 5 8 5
5 8 5 0 0 8 5 5 8 5
5 8 5 5 5 8 5 5 8 5
5 8 5 5 5 8 0 0 8 5
5 8 8 3 8 8 5 5 8 5
5 5 5 5 5 5 5 5 6 5
5 5 5 5 5 5 5 5 5 5
```

**Test 1 input**
```text
5 5 5 5 5 5 5 5 5 5 5
5 2 0 0 0 5 5 0 4 0 5
5 5 5 5 0 5 5 0 5 0 5
5 5 0 5 0 5 5 0 5 0 5
5 5 0 5 0 5 5 0 5 0 5
5 5 5 5 0 0 0 0 5 0 5
5 5 5 5 3 0 0 0 5 0 5
5 5 5 5 5 5 5 5 5 6 5
5 5 5 5 5 5 5 5 5 5 5
```

**Test 1 output**
```text
5 5 5 5 5 5 5 5 5 5 5
5 2 8 8 8 5 5 8 4 8 5
5 5 5 5 8 5 5 8 5 8 5
5 5 0 5 8 5 5 8 5 8 5
5 5 0 5 8 5 5 8 5 8 5
5 5 5 5 8 8 8 8 5 8 5
5 5 5 5 3 0 0 0 5 8 5
5 5 5 5 5 5 5 5 5 6 5
5 5 5 5 5 5 5 5 5 5 5
```

