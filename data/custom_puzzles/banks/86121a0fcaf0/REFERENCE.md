# 21 More ARC-Style Puzzles

This is the twenty-third continuation bank: **7 easy, 7 medium, 7 hard**.

It carries the sequence forward as **E155–E161, M155–M161, H155–H161**.

Each puzzle includes:

- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans more into **row emitters, hinge reflection, palette-by-size recoloring, corridor sweeps, room filling, cutout transfer, panel-transform inference, support-edit transfer, binary-op inference, counted orbits, recolor-stencil replay, and two-stage transform composition**.

**New motifs in this batch**

**`hinge_reflect(object, pivot)`** — reflect an object across the pivot’s row or column depending on where the object sits. This is the core move in **M155**.

**`corridor_sweep_right(shape, walls)`** — extend each occupied row segment rightward until a wall stops it. This is the main abstraction in **M157**.

**`support_edit_transfer(A, B, C)`** — compare two example supports inside a normalized bbox, extract add/remove edits, and replay them on a target support. This drives **H156**.

**`counted_orbit(shape, pivot, k)`** — take an anchor-centered object and place successive quarter-turn copies according to a header count. This is the central primitive in **H159**.

**`recolor_stencil_replay(A, B, C)`** — infer which relative cells were recolored in an example and apply the same accent stencil to a new base shape. This is the core of **H160**.

**`two_stage_dispatch(A_to_B, C_to_D, X)`** — infer two separate transforms from two example pairs and apply them in sequence to a target panel. This powers **H161**.


## Easy

### E155 — Left-column row painters

**What it tests:** Read the first column as row-color instructions and paint each marked row across the full width.


**Staged hint:** Ignore all columns except the first. Every nonzero cell in column 0 determines the whole row.


**Train 1 — input**

```text
200000
000000
500000
000000
300000
```

**Train 1 — output**

```text
222222
000000
555555
000000
333333
```

**Train 2 — input**

```text
0000000
4000000
0000000
6000000
0000000
7000000
```

**Train 2 — output**

```text
0000000
4444444
0000000
6666666
0000000
7777777
```

**Test — input**

```text
10000000
00000000
80000000
00000000
00000000
20000000
```

**Test — output**

```text
11111111
00000000
88888888
00000000
00000000
22222222
```

**Written solution:** Look only at the leftmost column. If a row starts with a nonzero color, repaint that entire row with that color. Rows whose first cell is 0 stay all 0.


**Program solution**

```python
def solve_E155(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        color=grid[r][0]
        if color!=0:
            for c in range(w):
                out[r][c]=color
    return out
```

### E156 — Fill horizontal same-color gaps

**What it tests:** Detect length-3 horizontal patterns of the form c,0,c and fill the middle cell.


**Staged hint:** Slide a 3-cell window across each row. When the endpoints match and the center is 0, the answer is forced.


**Train 1 — input**

```text
2020404
0000000
5050000
0707000
```

**Train 1 — output**

```text
2220444
0000000
5550000
0777000
```

**Train 2 — input**

```text
00000000
30030000
05500055
60600006
00000000
```

**Train 2 — output**

```text
00000000
30030000
05500055
66600006
00000000
```

**Test — input**

```text
808000909
000000000
040400000
005005500
000000000
```

**Test — output**

```text
888000999
000000000
044400000
005005500
000000000
```

**Written solution:** Scan each row. Whenever two matching nonzero cells are separated by exactly one blank cell, fill that blank with the same color. Leave everything else unchanged.


**Program solution**

```python
def solve_E156(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a!=0 and a==d and b==0:
                out[r][c+1]=a
    return out
```

### E157 — Bottom-row up-left diagonals

**What it tests:** Read the bottom row as diagonal seeds and emit each seed up-left until the grid edge.


**Staged hint:** Only the bottom row matters. Each nonzero bottom-row cell creates one diagonal moving up and left.


**Train 1 — input**

```text
000000
000000
000000
000000
030050
```

**Train 1 — output**

```text
500000
050000
005000
300500
030050
```

**Train 2 — input**

```text
0000000
0000000
0000000
0000000
0000000
0070020
```

**Train 2 — output**

```text
2000000
0200000
0020000
7002000
0700200
0070020
```

**Test — input**

```text
00000000
00000000
00000000
00000000
00000000
00000000
00040010
```

**Test — output**

```text
10000000
01000000
00100000
40010000
04001000
00400100
00040010
```

**Written solution:** Ignore all rows except the last one. For each nonzero seed there, paint that color on the seed itself and on every cell reached by stepping one row up and one column left until you hit the border.


**Program solution**

```python
def solve_E157(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c,color in enumerate(grid[h-1]):
        if color!=0:
            k=0
            while h-1-k>=0 and c-k>=0:
                out[h-1-k][c-k]=color
                k+=1
    return out
```

### E158 — Keep only border-touching components

**What it tests:** Separate connected components and preserve only the ones that touch the outer border.


**Staged hint:** Classify components into two groups: border-touching and interior. Only one group survives.


**Train 1 — input**

```text
2200000
2000000
0003300
0003300
0000000
0000044
0000040
```

**Train 1 — output**

```text
2200000
2000000
0000000
0000000
0000000
0000044
0000040
```

**Train 2 — input**

```text
0000000
0110000
0100000
0002200
0002200
0000000
0000005
```

**Train 2 — output**

```text
0000000
0000000
0000000
0000000
0000000
0000000
0000005
```

**Test — input**

```text
6000000
6600000
0003300
0000300
0000000
0000440
0000040
```

**Test — output**

```text
6000000
6600000
0000000
0000000
0000000
0000440
0000040
```

**Written solution:** Find every nonzero connected component. If at least one cell of that component lies on the outer border, keep the whole component. Otherwise erase it.


**Program solution**

```python
def solve_E158(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid, ignore=(0,), same_color=True):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out
```

### E159 — Fill between row endpoints

**What it tests:** Use matching colored endpoints on a row to fill the segment between them.


**Staged hint:** Work row by row. Once you know the leftmost and rightmost cells of a color, the whole span is determined.


**Train 1 — input**

```text
20002000
00000000
04000400
00000000
00500005
```

**Train 1 — output**

```text
22222000
00000000
04444400
00000000
00555555
```

**Train 2 — input**

```text
0000000
3000003
0000000
0600600
0000000
9000009
```

**Train 2 — output**

```text
0000000
3333333
0000000
0666600
0000000
9999999
```

**Test — input**

```text
10000001
00000000
00800080
00000000
00070007
```

**Test — output**

```text
11111111
00000000
00888880
00000000
00077777
```

**Written solution:** For each row, look for repeated occurrences of the same nonzero color. Fill every cell from that color’s leftmost occurrence to its rightmost occurrence, inclusive.


**Program solution**

```python
def solve_E159(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r,row in enumerate(grid):
        pos={}
        for c,v in enumerate(row):
            if v!=0:
                pos.setdefault(v,[]).append(c)
        for color,cols in pos.items():
            if len(cols)>=2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c]=color
    return out
```

### E160 — Recolor each row by its header cell

**What it tests:** Treat the first cell of each row as the row's color key and recolor every nonzero cell in that row to match it.


**Staged hint:** The first cell is the instruction; the rest of the row is just support to recolor.


**Train 1 — input**

```text
2050600
0000000
4030309
7007000
```

**Train 1 — output**

```text
2020200
0000000
4040404
7007000
```

**Train 2 — input**

```text
10002001
00000000
80088000
20034500
```

**Train 2 — output**

```text
10001001
00000000
80088000
20022200
```

**Test — input**

```text
90040009
00000000
50006050
30033300
```

**Test — output**

```text
90090009
00000000
50005050
30033300
```

**Written solution:** In every row, use the first cell as that row’s header color. Any nonzero cell elsewhere in the same row is rewritten to the header color, while 0s stay 0.


**Program solution**

```python
def solve_E160(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        header=row[0]
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=header if header!=0 else v
    return out
```

### E161 — Mirror rows around 9 anchors

**What it tests:** Use a 9 in each row as a reflection anchor and copy colored cells to the mirrored side.


**Staged hint:** Treat each row independently. Once you locate the 9, every colored cell implies one reflected partner.


**Train 1 — input**

```text
0239000
0009004
1209000
0000000
```

**Train 1 — output**

```text
0239320
4009004
1209021
0000000
```

**Train 2 — input**

```text
004090000
000090210
700090000
000000000
```

**Train 2 — output**

```text
004090400
012090210
700090007
000000000
```

**Test — input**

```text
056090000
000090320
100090000
000000000
```

**Test — output**

```text
056090650
023090320
100090001
000000000
```

**Written solution:** For each row containing a 9, reflect every nonzero non-9 cell across that 9’s column. Keep the original cells too, so the final row becomes symmetric around the anchor.


**Program solution**

```python
def solve_E161(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r,row in enumerate(grid):
        anchors=[c for c,v in enumerate(row) if v==9]
        if not anchors:
            continue
        a=anchors[0]
        for c,v in enumerate(row):
            if v!=0 and v!=9:
                mc=2*a-c
                if 0<=mc<w:
                    out[r][mc]=v
        out[r][a]=9
    return out
```


## Medium

### M155 — Hinge reflection around a 9 pivot

**What it tests:** Use the pivot's row or column as a reflection axis and duplicate the object to the opposite side.


**Staged hint:** First decide where the object sits relative to the 9: left, right, above, or below. Then reflect across that pivot line.


**Train 1 — input**

```text
0000000
0000000
0200000
0229000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0000000
0200020
0229220
0000000
0000000
0000000
```

**Train 2 — input**

```text
0000000
0044000
0004000
0009000
0000000
0000000
0000000
```

**Train 2 — output**

```text
0000000
0044000
0004000
0009000
0004000
0044000
0000000
```

**Test — input**

```text
0000000
0000000
0000000
0009000
0000600
0006600
0000000
```

**Test — output**

```text
0000000
0006600
0000600
0009000
0000600
0006600
0000000
```

**Written solution:** Find the unique 9 pivot and the unique colored object. If the object lies entirely on one side of the pivot, reflect it across the pivot’s vertical or horizontal line and keep both the original and reflected copies.


**Program solution**

```python
def solve_M155(grid):
    h,w=dims(grid)
    pivot=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                pivot=(r,c); break
        if pivot is not None: break
    pr,pc=pivot
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,9)]
    out=clone(grid)
    if not obj:
        return out
    rs=[r for r,c,v in obj]; cs=[c for r,c,v in obj]
    if max(cs) < pc:
        for r,c,v in obj:
            mc=2*pc-c
            if 0<=mc<w: out[r][mc]=v
    elif min(cs) > pc:
        for r,c,v in obj:
            mc=2*pc-c
            if 0<=mc<w: out[r][mc]=v
    elif max(rs) < pr:
        for r,c,v in obj:
            mr=2*pr-r
            if 0<=mr<h: out[mr][c]=v
    elif min(rs) > pr:
        for r,c,v in obj:
            mr=2*pr-r
            if 0<=mr<h: out[mr][c]=v
    return out
```

### M156 — Palette by component size

**What it tests:** Read a three-color palette from the top row and assign those colors to components ordered by size.


**Staged hint:** The body contains exactly three components. Sort them by area first; the header only tells you which colors to use.


**Train 1 — input**

```text
357000000
000000000
020000660
000000666
000000060
440000000
400000000
000000000
```

**Train 1 — output**

```text
357000000
000000000
030000770
000000777
000000070
550000000
500000000
000000000
```

**Train 2 — input**

```text
624000000
000000000
009900000
000000000
000330000
000330000
000000550
000000555
```

**Train 2 — output**

```text
624000000
000000000
006600000
000000000
000220000
000220000
000000440
000000444
```

**Test — input**

```text
819000000
000000000
000500000
000000660
000000660
220000000
200000000
000000000
```

**Test — output**

```text
819000000
000000000
000800000
000000990
000000990
110000000
100000000
000000000
```

**Written solution:** Ignore the top row except as a palette. In the body, detect the three connected components, sort them from smallest to largest, and recolor them using the top-row colors in that same order.


**Program solution**

```python
def solve_M156(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body, ignore=(0,), same_color=True)
    comps=sorted(comps, key=lambda x: len(x[1]))
    out=blank(h,w)
    out[0]=grid[0][:]
    for (old_color,cells), new_color in zip(comps, palette):
        for r,c in cells:
            out[r+1][c]=new_color
    return out
```

### M157 — Sweep shapes through corridors

**What it tests:** Extend each colored cell rightward until a wall stops it, effectively painting a rowwise shadow.


**Staged hint:** Process each row independently. The first wall to the right determines how far the sweep can go.


**Train 1 — input**

```text
0000008000
0200008000
0220008000
0200008000
0000008000
0000000000
```

**Train 1 — output**

```text
0000008000
0222228000
0222228000
0222228000
0000008000
0000000000
```

**Train 2 — input**

```text
0000000000
0400800000
0040008000
0400000080
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0444800000
0044448000
0444444480
0000000000
0000000000
```

**Test — input**

```text
0000000000
0600008000
0060000800
0600000080
0000000000
0000000000
```

**Test — output**

```text
0000000000
0666668000
0066666800
0666666680
0000000000
0000000000
```

**Written solution:** Treat 8s as walls. For every nonzero non-wall cell, paint its color to the right along the same row until just before the next wall or the edge. Keep walls unchanged.


**Program solution**

```python
def solve_M157(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r in range(h):
        wall_cols=[c for c,v in enumerate(grid[r]) if v==8]
        for c,v in enumerate(grid[r]):
            if v!=0 and v!=8:
                stop=min([wc for wc in wall_cols if wc>c], default=w)
                for x in range(c, stop):
                    if out[r][x]==0:
                        out[r][x]=v
    return out
```

### M158 — Infer a transform from two panels and apply it to a third

**What it tests:** Read an example transform A→B and dispatch that same transform onto target panel C.


**Staged hint:** Do not memorize one transform globally. In each puzzle instance, the left two panels tell you what transform to use.


**Train 1 — input**

```text
20008002284400
22208002080400
00008002080400
00008000080000
```

**Train 1 — output**

```text
0004
0444
0000
0000
```

**Train 2 — input**

```text
33008003385000
03008003085550
00008000080000
00008000080000
```

**Train 2 — output**

```text
0005
0555
0000
0000
```

**Test — input**

```text
60008660087700
66008060080700
00608006080000
00008000080000
```

**Test — output**

```text
7000
7700
0000
0000
```

**Written solution:** Split the input into three panels separated by full 8-columns. Identify which geometric transform maps the first panel to the second, then apply that same transform to the third panel to produce the output.


**Program solution**

```python
def solve_M158(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    tname=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            tname=name; break
    return transform_by_name(tname, C)
```

### M159 — Translate an object by a guide vector

**What it tests:** Use the vector from marker 3 to marker 4 as the translation to apply to the main object.


**Staged hint:** The markers are not decoration. The displacement from 3 to 4 is exactly the displacement of the object.


**Train 1 — input**

```text
2200000
2300000
0000000
0000400
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0300000
0002200
0002400
0000000
0000000
0000000
```

**Train 2 — input**

```text
0000000
0000000
0000040
0000000
0300000
6600000
6000000
```

**Train 2 — output**

```text
0000000
0000000
0000040
0000660
0300600
0000000
0000000
```

**Test — input**

```text
0000770
0000070
0000030
0000000
0040000
0000000
0000000
```

**Test — output**

```text
0000000
0000000
0770030
0070000
0040000
0000000
0000000
```

**Written solution:** Find marker 3, marker 4, and the remaining colored object. Compute the vector from 3 to 4, move the whole object by that vector, erase the original object, and keep the markers in place.


**Program solution**

```python
def solve_M159(grid):
    h,w=dims(grid)
    src=dst=None
    obj=[]
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v==3: src=(r,c)
            elif v==4: dst=(r,c)
            elif v not in (0,3,4):
                obj.append((r,c,v))
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    out=blank(h,w)
    sr,sc=src; tr,tc=dst
    out[sr][sc]=3; out[tr][tc]=4
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out
```

### M160 — Fill rooms from their seeds

**What it tests:** Use 8-walls to define rooms, then flood each room with the color of its unique seed.


**Staged hint:** The geometry comes first: identify rooms using the walls, then ask which seed belongs to each room.


**Train 1 — input**

```text
8888888
8108008
8008008
8008008
8008028
8008008
8888888
```

**Train 1 — output**

```text
8888888
8118228
8118228
8118228
8118228
8118228
8888888
```

**Train 2 — input**

```text
888888888
830080048
800080008
800080008
888888888
850080068
800080008
800080008
888888888
```

**Train 2 — output**

```text
888888888
833384448
833384448
833384448
888888888
855586668
855586668
855586668
888888888
```

**Test — input**

```text
88888888
81082008
80080008
88888888
83084008
80080008
80080008
88888888
```

**Test — output**

```text
88888888
81182228
81182228
88888888
83384448
83384448
83384448
88888888
```

**Written solution:** Treat 8 as an impenetrable wall. Inside each enclosed room, there is exactly one colored seed. Fill every reachable 0 in that room with the seed’s color, leaving the walls untouched.


**Program solution**

```python
def solve_M160(grid):
    h,w=dims(grid)
    out=clone(grid)
    seeds=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
    for sr,sc,color in seeds:
        q=deque([(sr,sc)]); seen={(sr,sc)}
        while q:
            r,c=q.popleft()
            out[r][c]=color
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and grid[nr][nc]!=8:
                    seen.add((nr,nc)); q.append((nr,nc))
    return out
```

### M161 — Transfer a cutout mask to a second block

**What it tests:** Use the support pattern of the left block as a mask and stamp that support onto the right block's bbox.


**Staged hint:** Compare the two blocks by bbox, not by raw position. The left block supplies a template support pattern.


**Train 1 — input**

```text
00000000000
02220055500
02020055500
02220055500
00000000000
```

**Train 1 — output**

```text
00000000000
02220055500
02020050500
02220055500
00000000000
```

**Train 2 — input**

```text
00000000000000
03330007777000
03030007777000
03330007777000
03000007777000
00000000000000
```

**Train 2 — output**

```text
00000000000000
03330007770000
03030007070000
03330007770000
03000007000000
00000000000000
```

**Test — input**

```text
000000000000000
044440066666000
040040066666000
044440066666000
004440066666000
000000000000000
```

**Test — output**

```text
000000000000000
044440066660000
040040060060000
044440066660000
004440006660000
000000000000000
```

**Written solution:** There are two separated components with matching bounding-box sizes. Keep the left one as-is, extract its nonzero support pattern, and apply that same support pattern inside the right component’s bounding box using the right component’s color.


**Program solution**

```python
def solve_M161(grid):
    comps=cc(grid, ignore=(0,), same_color=True)
    if len(comps)!=2:
        return clone(grid)
    comps_sorted=sorted(comps, key=lambda x: min(c for r,c in x[1]))
    (c1,cells1),(c2,cells2)=comps_sorted
    r01,r11,c01,c11=bbox(cells1)
    r02,r12,c02,c12=bbox(cells2)
    mask={(r-r01,c-c01) for r,c in cells1}
    out=blank(*dims(grid))
    for r,c in cells1:
        out[r][c]=c1
    for r in range(r02,r12+1):
        for c in range(c02,c12+1):
            if (r-r02,c-c02) in mask:
                out[r][c]=c2
    return out
```


## Hard

### H155 — Infer a panel transform and then recolor the result

**What it tests:** Compose two abstractions: infer the geometric transform from A→B, then repaint transformed target C using a header color.


**Staged hint:** Separate the jobs. First recover the transform from the example pair; only then apply the recolor key from the header row.


**Train 1 — input**

```text
60000000000000
22008002285000
02008002085550
00008000080000
00008000080000
```

**Train 1 — output**

```text
0006
0666
0000
0000
```

**Train 2 — input**

```text
30000000000000
30008003387700
33008033080700
03008000080000
00008000080000
```

**Train 2 — output**

```text
0003
0033
0000
0000
```

**Test — input**

```text
90000000000000
66008600087700
06008660087770
00008000080000
00008000080000
```

**Test — output**

```text
9900
9900
0900
0000
```

**Written solution:** Read the first nonzero cell of the top row as the final output color. In the remaining three panels, infer which transform maps the first panel to the second, apply that transform to the third panel, and recolor every nonzero cell of the transformed target to the header color.


**Program solution**

```python
def solve_H155(grid):
    target=next(v for v in grid[0] if v!=0)
    body=grid[1:]
    A,B,C = split_by_full_sep_cols(body, sep=8)
    tname=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            tname=name; break
    out=transform_by_name(tname, C)
    return recolor(out, target)
```

### H156 — Transfer a support edit from one shape to another

**What it tests:** Compare A and B inside a shared bbox, extract the support cells that were added and removed, and replay that edit on C.


**Staged hint:** Do not reason at absolute coordinates. Normalize everything to the shapes' own bounding boxes and compare support sets there.


**Train 1 — input**

```text
22228222285555
20228220285055
22228222285555
22228222285555
```

**Train 1 — output**

```text
5555
5505
5555
5555
```

**Train 2 — input**

```text
33338333386666
33338330386666
30338333386066
33338333386666
```

**Train 2 — output**

```text
6666
6606
6666
6666
```

**Test — input**

```text
44448444487777
40448444487077
44448440487777
44448444487777
```

**Test — output**

```text
7777
7777
7707
7777
```

**Written solution:** Split the input into A, B, and C panels. Crop each to its nonzero bounding box. From A→B, compute which relative support cells were removed and which were added. Apply that same remove/add edit to C’s relative support and render the result in C’s color.


**Program solution**

```python
def solve_H156(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A0=crop_bbox(A); B0=crop_bbox(B); C0=crop_bbox(C)
    ha,wa=dims(A0); hb,wb=dims(B0); hc,wc=dims(C0)
    if (ha,wa)!=(hb,wb) or (ha,wa)!=(hc,wc):
        return C0
    SA={(r,c) for r,row in enumerate(A0) for c,v in enumerate(row) if v!=0}
    SB={(r,c) for r,row in enumerate(B0) for c,v in enumerate(row) if v!=0}
    SC={(r,c) for r,row in enumerate(C0) for c,v in enumerate(row) if v!=0}
    add=SB-SA
    remove=SA-SB
    new=(SC-remove)|add
    color=dominant_nonzero_color(C0)
    out=blank(ha,wa)
    for r,c in new:
        out[r][c]=color
    return out
```

### H157 — Infer a binary set operation from an embedded example

**What it tests:** Read an example triplet A, B, O to identify whether the operation is union, intersection, xor, or left-minus-right, then apply it to X and Y.


**Staged hint:** The operation is not fixed across the puzzle family. In each instance, the first three panels are the legend for the last two.


**Train 1 — input**

```text
110080000811008011080000
100080010810108001080100
000080011800118000080110
000080000800008000080000
```

**Train 1 — output**

```text
0110
0110
0110
0000
```

**Train 2 — input**

```text
011080011801018110080110
001080010800008010080010
000080000800008000080000
000080000800008000080000
```

**Train 2 — output**

```text
1010
0110
0000
0000
```

**Test — input**

```text
111080111801108110080110
001080010800108010080100
000080000800008000080000
000080000800008000080000
```

**Test — output**

```text
0100
0100
0000
0000
```

**Written solution:** Split the input into five panels. Determine which binary operation on the first two panels produces the third. Then apply the same operation to the fourth and fifth panels to obtain the output.


**Program solution**

```python
def solve_H157(grid):
    A,B,O,X,Y = split_by_full_sep_cols(grid, sep=8)
    opname=None
    for name,op in OPS.items():
        if op(A,B)==O:
            opname=name; break
    return OPS[opname](X,Y)
```

### H158 — Match a prototype under symmetry and recolor it

**What it tests:** Find which candidate panel matches the query's support up to rotation or reflection, orient it like the query, then recolor it by the header.


**Staged hint:** Support matters more than original color. Search candidates under all symmetries until one lines up with the query.


**Train 1 — input**

```text
7000000000000000000
2200833308000485500
0200803008044485500
0200800008000080000
0000800008000080000
```

**Train 1 — output**

```text
7700
0700
0700
0000
```

**Train 2 — input**

```text
2000000000000000000
0660877008550080330
6600807008005080033
0000800008000080000
0000800008000080000
```

**Train 2 — output**

```text
0220
2200
0000
0000
```

**Test — input**

```text
6000000000000000000
8800800008990080550
0880804008990080550
0080804408000080000
0000800448000080000
```

**Test — output**

```text
6600
0660
0060
0000
```

**Written solution:** Use the top-row color as the final paint. In the body, compare the query panel with each candidate under rotations and reflections. When a transformed candidate has the same support as the query, output that transformed candidate recolored to the header color.


**Program solution**

```python
def solve_H158(grid):
    target=next(v for v in grid[0] if v!=0)
    body=grid[1:]
    Q,C1,C2,C3 = split_by_full_sep_cols(body, sep=8)
    q_support=normalize_support(Q)
    for cand in [C1,C2,C3]:
        for name in TRANSFORM_NAMES:
            tc=transform_by_name(name, cand)
            if normalize_support(tc)==q_support:
                return recolor(tc, target)
    return [[0]]
```

### H159 — Build a counted orbit around a pivot

**What it tests:** Use the number of header tokens to decide how many successive 90° rotations of an object to place around a pivot.


**Staged hint:** Count first, rotate second. The header tells you how many orbit positions to include, starting from the original object.


**Train 1 — input**

```text
1100000
0000000
0020000
0220000
0009000
0000000
0000000
0000000
```

**Train 1 — output**

```text
1100000
0000000
0020200
0220220
0009000
0000000
0000000
0000000
```

**Train 2 — input**

```text
1110000
0000000
0000400
0000440
0009000
0000000
0000000
0000000
```

**Train 2 — output**

```text
1110000
0000000
0000400
0000440
0009000
0440440
0040400
0000000
```

**Test — input**

```text
1111000
0000000
0000000
0000000
0009000
0066000
0006000
0000000
```

**Test — output**

```text
1111000
0000000
0006000
0066600
0669660
0066600
0006000
0000000
```

**Written solution:** The first row encodes an integer k by its number of nonzero tokens. Below it, find the pivot 9 and the colored object. Keep the original object and add its 90° clockwise rotations around the pivot for a total of k orbit positions. Leave the header and pivot in place.


**Program solution**

```python
def solve_H159(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    pr=pc=None
    obj=[]
    for r in range(len(body)):
        for c,v in enumerate(body[r]):
            if v==9:
                pr,pc=r,c
            elif v not in (0,1):
                obj.append((r,c,v))
    out=blank(h,w)
    out[0]=grid[0][:]
    out[pr+1][pc]=9
    def rot(dr,dc,t):
        for _ in range(t):
            dr,dc = dc,-dr
        return dr,dc
    for t in range(k):
        for r,c,v in obj:
            dr,dc=r-pr,c-pc
            nr,nc=rot(dr,dc,t)
            rr,cc=pr+nr,pc+nc
            if 0<=rr<len(body) and 0<=cc<w:
                out[rr+1][cc]=v
    return out
```

### H160 — Replay a recolor stencil onto a new base shape

**What it tests:** Compare A and B to find which relative cells were recolored to an accent color, then apply that same accent stencil to C.


**Staged hint:** The support does not change; only certain relative positions change color. Extract the stencil, not the full object.


**Train 1 — input**

```text
22228292285555
22228222285555
22228222985555
22228222285555
```

**Train 1 — output**

```text
5955
5555
5559
5555
```

**Train 2 — input**

```text
33338333386666
33338383386666
33338333886666
33338333386666
```

**Train 2 — output**

```text
6666
6866
6668
6666
```

**Test — input**

```text
44448474485555
44448444485555
44448444485555
44448447485555
```

**Test — output**

```text
5755
5555
5555
5575
```

**Written solution:** Split the input into three panels with matching support. In the example A→B, some relative cells change from the base color to an accent color. Record those relative positions and the accent color, then recolor the corresponding cells of C while leaving the rest of C in its original base color.


**Program solution**

```python
def solve_H160(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A0=crop_bbox(A); B0=crop_bbox(B); C0=crop_bbox(C)
    ha,wa=dims(A0); hb,wb=dims(B0); hc,wc=dims(C0)
    if (ha,wa)!=(hb,wb) or (ha,wa)!=(hc,wc):
        return C0
    accent_positions=[]
    accent_color=None
    for r in range(ha):
        for c in range(wa):
            if A0[r][c]!=0 and B0[r][c]!=0 and A0[r][c]!=B0[r][c]:
                accent_positions.append((r,c))
                accent_color=B0[r][c]
    base=dominant_nonzero_color(C0)
    out=[[base if v!=0 else 0 for v in row] for row in C0]
    for r,c in accent_positions:
        if out[r][c]!=0:
            out[r][c]=accent_color
    return out
```

### H161 — Compose two inferred transforms in sequence

**What it tests:** Recover one transform from A→B and a second transform from C→D, then apply them in order to target X.


**Staged hint:** Do not collapse the puzzle into one guess. There are two separate example pairs, and each contributes one step of the final program.


**Train 1 — input**

```text
220080022833008003384400
020080020833308003380400
000080000800008003080400
000080000800008000080000
```

**Train 1 — output**

```text
0000
0000
0444
0004
```

**Train 2 — input**

```text
500085500866008000087700
550080550806008066087000
050080000806608060087700
000080000800008660080000
```

**Train 2 — output**

```text
0000
0000
7070
7770
```

**Test — input**

```text
880080000899008009984400
088080000809008009084400
000080880800008000084000
000080088800008000080000
```

**Test — output**

```text
0000
4000
4400
4400
```

**Written solution:** Split the input into five panels. Infer the first transform from A→B and the second transform from C→D. Apply the first transform to X, then apply the second transform to that result, and output the final panel.


**Program solution**

```python
def solve_H161(grid):
    A,B,C,D,X = split_by_full_sep_cols(grid, sep=8)
    t1=t2=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            t1=name; break
    first=transform_by_name(t1, X)
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, C)==D:
            t2=name; break
    return transform_by_name(t2, first)
```
