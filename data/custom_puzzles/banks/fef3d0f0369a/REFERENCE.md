# 21 More ARC-Style Puzzles

This is the ninth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E57–E63, M57–M63, H57–H63**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans further into anchored symmetry, panel composition, topology, transform inference, symbolic remapping, distance-based filling, and rank-based recoloring.

**New motifs in this batch**

**`panel_infer_transform(example_in, example_out, query)`** — infer a local transform from one panel pair and apply it to another. This is the core idea in **H57**.

**`pivot_orbit(pivot, prototype)`** — treat a shape as offsets from a pivot and union its quarter-turn copies around that pivot. This is the main idea in **H59**.

**`rank_fill(mask_components, palette)`** — sort mask components by size and color them from an ordered palette. This drives **H63**.

**`voronoi_fill_inside_frame(frame, seeds)`** — fill blank interior cells by nearest seed under Manhattan distance, ties broken deterministically. This is most visible in **H62**.

## Easy

### E57 — Row bridge fill

**What it tests:** Detect matching endpoints on a row and fill the straight gap between them.

**Staged hint:** Look row by row. Ignore everything except rows that contain exactly two cells of the same color.

**Train 1 — input**

```text
000000000
020002000
000000000
404000000
000000000
000600060
000000000
```

**Train 1 — output**

```text
000000000
022222000
000000000
444000000
000000000
000666660
000000000
```

**Train 2 — input**

```text
0030003000
0000000000
0500500000
0000000000
0000070070
0000000000
```

**Train 2 — output**

```text
0033333000
0000000000
0555500000
0000000000
0000077770
0000000000
```

**Test — input**

```text
0000000000
0400004000
0000000000
2002000000
0000000000
0000800080
0000000000
```

**Test — expected output**

```text
0000000000
0444444000
0000000000
2222000000
0000000000
0000888880
0000000000
```

**Written solution**

For each row, find colors that appear exactly twice. If the cells between those two endpoints are blank, fill the whole interval with that color. Leave other rows unchanged.

**Reference program (`solve_E57`)**

```python
def solve_E57(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        by_color = {}
        for c,v in enumerate(g[r]):
            if v != 0:
                by_color.setdefault(v, []).append(c)
        for color, cols in by_color.items():
            if len(cols) == 2:
                a,b = min(cols), max(cols)
                if all(g[r][c] == 0 for c in range(a+1, b)):
                    for c in range(a, b+1):
                        out[r][c] = color
    return out
```

### E58 — Mirror through the 9 anchor

**What it tests:** Use a row-local anchor to reflect colored cells to the opposite side.

**Staged hint:** Each active row has a single 9. Measure the distance from the colored cell to that 9 and copy it to the other side.

**Train 1 — input**

```text
000000000
003090000
000000000
000906000
000000000
000020900
000000000
```

**Train 1 — output**

```text
000000000
003090300
000000000
060906000
000000000
000020902
000000000
```

**Train 2 — input**

```text
409000000
000000000
000009070
000000000
020090000
000000000
```

**Train 2 — output**

```text
409040000
000000000
000709070
000000000
020090020
000000000
```

**Test — input**

```text
0000000000
0060090000
0000000000
0409000000
0000000000
0000009020
0000000000
```

**Test — expected output**

```text
0000000000
0060090060
0000000000
0409040000
0000000000
0000209020
0000000000
```

**Written solution**

On every row containing a 9 anchor, mirror each other nonzero cell across the anchor. The reflected cell gets the same color and the original row contents stay in place.

**Reference program (`solve_E58`)**

```python
def solve_E58(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        anchors = [c for c,v in enumerate(g[r]) if v == 9]
        if len(anchors) != 1:
            continue
        a = anchors[0]
        for c,v in enumerate(g[r]):
            if v != 0 and v != 9:
                mc = 2*a - c
                if 0 <= mc < w:
                    out[r][mc] = v
    return out
```

### E59 — Left-edge row legend

**What it tests:** Read a per-row key from the border and use it to repaint markers on that row.

**Staged hint:** The first column is the legend. Every 8 on the same row should inherit that row's first-column color.

**Train 1 — input**

```text
000000000
200808000
000000000
408000880
000000000
680080000
000000000
```

**Train 1 — output**

```text
000000000
200202000
000000000
404000440
000000000
660060000
000000000
```

**Train 2 — input**

```text
308080080
000000000
500800000
000000000
780008800
000000000
```

**Train 2 — output**

```text
303030030
000000000
500500000
000000000
770007700
000000000
```

**Test — input**

```text
000000000
408000800
000000000
280080080
000000000
800808000
000000000
```

**Test — expected output**

```text
000000000
404000400
000000000
220020020
000000000
800808000
000000000
```

**Written solution**

Treat the first cell of each row as that row's key color. Replace every 8 in that row with the key color, keeping all other cells the same.

**Reference program (`solve_E59`)**

```python
def solve_E59(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        key = g[r][0]
        if key == 0:
            continue
        for c in range(1,w):
            if g[r][c] == 8:
                out[r][c] = key
    return out
```

### E60 — Keep only the biggest object

**What it tests:** Connected-component detection and simple size comparison.

**Staged hint:** Count cells in each nonzero object. Only one object is largest.

**Train 1 — input**

```text
00000000
02200060
02000060
00000000
00004400
00004400
00004000
00000000
```

**Train 1 — output**

```text
00000000
00000000
00000000
00000000
00004400
00004400
00004000
00000000
```

**Train 2 — input**

```text
000000000
000003000
000003000
000000000
055000000
050000000
050007700
000007770
000000070
```

**Train 2 — output**

```text
000000000
000000000
000000000
000000000
000000000
000000000
000007700
000007770
000000070
```

**Test — input**

```text
0000000000
0220000000
0000004000
0000004000
0000004400
0000000400
0088000000
0008000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000004000
0000004000
0000004400
0000000400
0000000000
0000000000
0000000000
```

**Written solution**

Find all nonzero connected components. Keep the single largest component exactly as it is and erase every other nonzero object.

**Reference program (`solve_E60`)**

```python
def solve_E60(g: Grid) -> Grid:
    comps = same_color_components(g)
    best_color, best_cells = max(comps, key=lambda t: len(t[1]))
    h,w = dims(g)
    out = blank(h,w,0)
    for r,c in best_cells:
        out[r][c] = best_color
    return out
```

### E61 — Rectangle from corners

**What it tests:** Recover an axis-aligned rectangle border from four corner clues.

**Staged hint:** There is only one rectangle. Use the four nonzero cells as its corners.

**Train 1 — input**

```text
000000000
003000030
000000000
000000000
000000000
003000030
000000000
000000000
```

**Train 1 — output**

```text
000000000
003333330
003000030
003000030
003000030
003333330
000000000
000000000
```

**Train 2 — input**

```text
0600000060
0000000000
0000000000
0000000000
0600000060
0000000000
0000000000
```

**Train 2 — output**

```text
0666666660
0600000060
0600000060
0600000060
0666666660
0000000000
0000000000
```

**Test — input**

```text
000000000
000000000
020000200
000000000
000000000
000000000
000000000
020000200
000000000
```

**Test — expected output**

```text
000000000
000000000
022222200
020000200
020000200
020000200
020000200
022222200
000000000
```

**Written solution**

Take the four nonzero cells as the corners of a single rectangle. Draw that rectangle's full border in the same color and leave the inside blank.

**Reference program (`solve_E61`)**

```python
def solve_E61(g: Grid) -> Grid:
    h,w = dims(g)
    pts = [(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v != 0]
    color = pts[0][2]
    cells = [(r,c) for r,c,v in pts if v == color]
    r0,r1,c0,c1 = bbox(cells)
    out = blank(h,w,0)
    for c in range(c0, c1+1):
        out[r0][c] = color
        out[r1][c] = color
    for r in range(r0, r1+1):
        out[r][c0] = color
        out[r][c1] = color
    return out
```

### E62 — Stamp the 2×2 prototype

**What it tests:** Copy a small prototype pattern into multiple marked windows.

**Staged hint:** The top-left 2×2 block is the prototype. Every 7 marks the top-left corner of another copy.

**Train 1 — input**

```text
2000000000
4600070000
0000000000
0000000000
0007000000
0000007000
0000000000
0000000000
```

**Train 1 — output**

```text
2000000000
4600020000
0000046000
0000000000
0002000000
0004602000
0000004600
0000000000
```

**Train 2 — input**

```text
3500000000
0700000000
0000700000
0000000000
0700000000
0000000700
0000000000
0000000000
```

**Train 2 — output**

```text
3500000000
0700000000
0000350000
0000070000
0350000000
0070000350
0000000070
0000000000
```

**Test — input**

```text
6200000000
8000007000
0000000000
0007000000
0000000000
0700000000
0000000000
0000000000
```

**Test — expected output**

```text
6200000000
8000006200
0000008000
0006200000
0008000000
0620000000
0800000000
0000000000
```

**Written solution**

Read the 2×2 pattern in the top-left corner. For every 7 elsewhere, stamp that same 2×2 block starting at the 7's position, replacing the marker.

**Reference program (`solve_E62`)**

```python
def solve_E62(g: Grid) -> Grid:
    out = clone(g)
    proto = [row[:2] for row in g[:2]]
    h,w = dims(g)
    markers = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7 and not (r < 2 and c < 2)]
    for r,c in markers:
        overlay(out, proto, r, c, transparent=-1)
    return out
```

### E63 — Diagonal gap filler

**What it tests:** Complete broken diagonals by filling the midpoint.

**Staged hint:** Look for same-colored cells exactly two steps apart on a diagonal with a blank cell between them.

**Train 1 — input**

```text
00000040
02000000
00004000
00020000
00600000
00000000
00006000
00000000
```

**Train 1 — output**

```text
00000040
02000400
00204000
00020000
00600000
00060000
00006000
00000000
```

**Train 2 — input**

```text
000000070
000003000
050007000
000300000
000500000
000000000
000000000
```

**Train 2 — output**

```text
000000070
000003700
050037000
005300000
000500000
000000000
000000000
```

**Test — input**

```text
000000000
000000200
004000000
000020000
000040800
000000000
000000008
000000000
```

**Test — expected output**

```text
000000000
000000200
004002000
000420000
000040800
000000080
000000008
000000000
```

**Written solution**

Whenever two same-colored cells lie two steps apart diagonally and the middle diagonal cell is blank, fill that middle cell with the same color. Preserve all original cells.

**Reference program (`solve_E63`)**

```python
def solve_E63(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                r2,c2 = r+2*dr, c+2*dc
                rm,cm = r+dr, c+dc
                if 0 <= r2 < h and 0 <= c2 < w and g[r2][c2] == v and g[rm][cm] == 0:
                    out[rm][cm] = v
    return out
```

## Medium

### M57 — Rotate-and-stamp by code

**What it tests:** Read a rotation code, rotate a multicolor prototype, and stamp it at a target marker.

**Staged hint:** Separate the three roles: the prototype, the bottom-left code cell, and the 9 target marker.

**Train 1 — input**

```text
0000000000
0600090000
0670000000
0670000000
0000000000
0000000000
0000000000
0000000000
2000000000
```

**Train 1 — output**

```text
0000000000
0000066600
0000077000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Train 2 — input**

```text
0000000000
0850000000
0055000000
0000000000
0000009000
0000000000
0000000000
0000000000
4000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000000
0000000000
0000008000
0000005500
0000000500
0000000000
0000000000
```

**Test — input**

```text
0000000000
0706000000
0766090000
0000000000
0000000000
0000000000
0000000000
0000000000
3000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000066700
0000060700
0000000000
0000000000
0000000000
0000000000
0000000000
```

**Written solution**

Extract the nonzero prototype, ignoring the code cell and the 9 marker. Use the bottom-left code to choose 0°, 90°, 180°, or 270° rotation, then stamp the rotated prototype so its top-left corner lands on the 9 marker.

**Reference program (`solve_M57`)**

```python
def solve_M57(g: Grid) -> Grid:
    h,w = dims(g)
    code = g[h-1][0]
    marker = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 9)
    cells = [(r,c) for r in range(h) for c in range(w)
             if g[r][c] != 0 and not (r == h-1 and c == 0) and not (r,c) == marker]
    r0,r1,c0,c1 = bbox(cells)
    proto = [row[c0:c1+1] for row in g[r0:r1+1]]
    kind = {1:"id", 2:"rot90", 3:"rot180", 4:"rot270"}[code]
    rot = transform_grid(proto, kind)
    out = blank(h,w,0)
    overlay(out, rot, marker[0], marker[1], transparent=0)
    return out
```

### M58 — Mask carries payload colors

**What it tests:** Compose geometry from one panel with color content from another.

**Staged hint:** The left panel says where to keep cells; the right panel says which colors to keep there.

**Train 1 — input**

```text
010192345
110096782
001093456
101197823
```

**Train 1 — output**

```text
0305
6700
0050
7023
```

**Train 2 — input**

```text
1019456
0109782
1109345
0019678
```

**Train 2 — output**

```text
406
080
340
008
```

**Test — input**

```text
101096248
110193572
011094683
001195724
```

**Test — expected output**

```text
6040
3502
0680
0024
```

**Written solution**

Split the input at the 9 separator column. For each position, output the right-panel color only if the left panel has a 1 at that position; otherwise output 0.

**Reference program (`solve_M58`)**

```python
def solve_M58(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    left,right = parts
    h,w = dims(left)
    out = blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if left[r][c] == 1:
                out[r][c] = right[r][c]
    return out
```

### M59 — Reflect across the painted axis

**What it tests:** Identify a vertical or horizontal symmetry axis and mirror an object across it.

**Staged hint:** Find the full line of 5s first. Then copy every other nonzero cell to the opposite side at the same distance.

**Train 1 — input**

```text
000050000
030050000
033050000
003050000
000050000
000050000
000050000
000050000
000050000
```

**Train 1 — output**

```text
000050000
030050030
033050330
003050300
000050000
000050000
000050000
000050000
000050000
```

**Train 2 — input**

```text
000000000
000000600
000006600
000000600
555555555
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000600
000006600
000000600
555555555
000000600
000006600
000000600
000000000
```

**Test — input**

```text
0000050000
0000050000
0040050000
0044050000
0004050000
0004050000
0000050000
0000050000
0000050000
0000050000
```

**Test — expected output**

```text
0000050000
0000050000
0040050040
0044050440
0004050400
0004050400
0000050000
0000050000
0000050000
0000050000
```

**Written solution**

Locate the full row or full column of 5s. Reflect every nonzero non-axis cell across that line, keeping the axis itself and the original shape.

**Reference program (`solve_M59`)**

```python
def solve_M59(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    axis_row = next((r for r in range(h) if all(g[r][c] == 5 for c in range(w))), None)
    axis_col = next((c for c in range(w) if all(g[r][c] == 5 for r in range(h))), None)
    if axis_row is not None:
        for r in range(h):
            for c in range(w):
                v = g[r][c]
                if v != 0 and v != 5:
                    rr = 2*axis_row - r
                    if 0 <= rr < h:
                        out[rr][c] = v
    else:
        for r in range(h):
            for c in range(w):
                v = g[r][c]
                if v != 0 and v != 5:
                    cc = 2*axis_col - c
                    if 0 <= cc < w:
                        out[r][cc] = v
    return out
```

### M60 — Holes become one color, solids another

**What it tests:** Topological reasoning: distinguish hollow objects from solid ones.

**Staged hint:** Do not focus on the input color. Ask whether an object encloses any blank cell.

**Train 1 — input**

```text
0000000000
0222200000
0200200000
0200200000
0222200000
0000002220
0222002020
0222002020
0222002220
0000000000
```

**Train 1 — output**

```text
0000000000
0888800000
0800800000
0800800000
0888800000
0000008880
0444008080
0444008080
0444008880
0000000000
```

**Train 2 — input**

```text
00000000000
02222002220
02222002020
02222002020
00000002020
00000002220
00022200000
00022200000
00022200000
00000000000
```

**Train 2 — output**

```text
00000000000
04444008880
04444008080
04444008080
00000008080
00000008880
00044400000
00044400000
00044400000
00000000000
```

**Test — input**

```text
00000000000
02222200000
02000200000
02000200000
02000200000
02222200000
00000002220
02220002020
02220002020
02220002220
00000000000
```

**Test — expected output**

```text
00000000000
08888800000
08000800000
08000800000
08000800000
08888800000
00000008880
04440008080
04440008080
04440008880
00000000000
```

**Written solution**

Find each connected object. If it contains an enclosed hole, recolor the whole object to 8; otherwise recolor the whole object to 4. Keep the shapes themselves unchanged.

**Reference program (`solve_M60`)**

```python
def solve_M60(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w,0)
    for color,cells in same_color_components(g):
        cellset = set(cells)
        r0,r1,c0,c1 = bbox(cells)
        seen = set()
        q = deque()
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    if (r,c) not in cellset and (r,c) not in seen:
                        seen.add((r,c))
                        q.append((r,c))
        while q:
            r,c = q.popleft()
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                rr,cc = r+dr, c+dc
                if r0 <= rr <= r1 and c0 <= cc <= c1 and (rr,cc) not in cellset and (rr,cc) not in seen:
                    seen.add((rr,cc))
                    q.append((rr,cc))
        has_hole = any((r,c) not in cellset and (r,c) not in seen for r in range(r0,r1+1) for c in range(c0,c1+1))
        new_color = 8 if has_hole else 4
        for r,c in cells:
            out[r][c] = new_color
    return out
```

### M61 — Translate by the anchor vector

**What it tests:** Use two anchors to derive a translation vector for an entire shape.

**Staged hint:** Measure the vector from the 1 cell to the 2 cell. Apply that same shift to every shape cell.

**Train 1 — input**

```text
100000000
066000000
060000000
060000000
000002000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000000
000000000
000000000
000000660
000000600
000000600
000000000
```

**Train 2 — input**

```text
0000000000
0100000000
0000700000
0000770000
0000070000
0000000000
0020000000
0000000000
0000000000
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000070000
0000077000
0000007000
```

**Test — input**

```text
0000000010
0000004000
0000004400
0000000440
0000000000
0002000000
0000000000
0000000000
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
0400000000
0440000000
0044000000
0000000000
```

**Written solution**

Find the source anchor 1 and destination anchor 2. Translate the whole colored shape by that vector, and output only the translated shape.

**Reference program (`solve_M61`)**

```python
def solve_M61(g: Grid) -> Grid:
    h,w = dims(g)
    src = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    dst = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 2)
    dr,dc = dst[0]-src[0], dst[1]-src[1]
    out = blank(h,w,0)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0 and v not in (1,2):
                rr,cc = r+dr, c+dc
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = v
    return out
```

### M62 — Recolor the matching query shape

**What it tests:** Compare normalized component shapes and transfer the matching prototype's color.

**Staged hint:** Normalize the prototypes and the gray query by translation only. One colored prototype has the same shape.

**Train 1 — input**

```text
000000000000
020000040000
022000444000
000000000000
000000000000
000000008000
000000008800
000000000000
000000000000
```

**Train 1 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000002000
000000002200
000000000000
000000000000
```

**Train 2 — input**

```text
000000000000
033000060000
030000066000
030000000000
000000000000
000000000000
000000008800
000000008000
000000008000
000000000000
```

**Train 2 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000003300
000000003000
000000003000
000000000000
```

**Test — input**

```text
0000000000000
0200000050000
0222000550000
0000000000000
0000000000000
0000000000000
0000000000800
0000000008800
0000000000000
0000000000000
```

**Test — expected output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000500
0000000005500
0000000000000
0000000000000
```

**Written solution**

Ignore position and compare shapes. Recolor the gray query object using the color of the prototype whose shape matches it exactly.

**Reference program (`solve_M62`)**

```python
def solve_M62(g: Grid) -> Grid:
    h,w = dims(g)
    comps = same_color_components(g)
    query_cells = next(cells for color,cells in comps if color == 8)
    query_shape,_,_ = normalize_cells(query_cells)
    match_color = None
    for color,cells in comps:
        if color == 8:
            continue
        shp,_,_ = normalize_cells(cells)
        if shp == query_shape:
            match_color = color
            break
    out = blank(h,w,0)
    for r,c in query_cells:
        out[r][c] = match_color
    return out
```

### M63 — Crop the framed interior and center it

**What it tests:** Detect a frame, extract its inner content, crop it tightly, and recenter it.

**Staged hint:** Ignore the 7 frame once you have found it. What matters is the nonzero pattern inside the frame.

**Train 1 — input**

```text
000000000
077777770
070000070
070220070
070020070
074000070
070000070
077777770
000000000
```

**Train 1 — output**

```text
000000000
000000000
000000000
000022000
000002000
000400000
000000000
000000000
000000000
```

**Train 2 — input**

```text
0000000000
0777777770
0700000070
0700030070
0700330070
0700030070
0706600070
0700000070
0777777770
0000000000
```

**Train 2 — output**

```text
0000000000
0000000000
0000000000
0000030000
0000330000
0000030000
0006600000
0000000000
0000000000
0000000000
```

**Test — input**

```text
00000000000
00000000000
00777777770
00700000070
00700200070
00702220070
00700000070
00708000070
00700000070
00777777770
00000000000
```

**Test — expected output**

```text
00000000000
00000000000
00000000000
00000200000
00002220000
00000000000
00008000000
00000000000
00000000000
00000000000
00000000000
```

**Written solution**

Find the single 7 frame. Remove the frame, crop the nonzero interior content to its bounding box, then place that cropped pattern at the center of an otherwise blank canvas of the original size.

**Reference program (`solve_M63`)**

```python
def solve_M63(g: Grid) -> Grid:
    h,w = dims(g)
    frame_cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7]
    r0,r1,c0,c1 = bbox(frame_cells)
    interior = [row[c0+1:c1] for row in g[r0+1:r1]]
    cells = [(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v != 0]
    ir0,ir1,ic0,ic1 = bbox(cells)
    crop = [row[ic0:ic1+1] for row in interior[ir0:ir1+1]]
    out = blank(h,w,0)
    ch,cw = dims(crop)
    top = (h - ch)//2
    left = (w - cw)//2
    overlay(out, crop, top, left, transparent=0)
    return out
```

## Hard

### H57 — Infer the panel transform and apply it

**What it tests:** Infer a dihedral transform from one example panel pair and apply it to a query panel.

**Staged hint:** Do not solve the whole grid at once. First determine how panel A changes into panel B, then apply exactly that same transform to panel C.

**Train 1 — input**

```text
02000900000900000
02040900222966000
02200900200906000
00000900040900300
00000900000900000
```

**Train 1 — output**

```text
00060
00660
03000
00000
00000
```

**Train 2 — input**

```text
30000900003900200
33000900033900220
00000900000900000
00660906600907000
00000900000900000
```

**Train 2 — output**

```text
00200
02200
00000
00070
00000
```

**Test — input**

```text
04002900000970000
04400900000977000
00400900400900050
00000900440900000
00000920040900000
```

**Test — expected output**

```text
00000
00000
05000
00077
00007
```

**Written solution**

Split the input into three panels using the 9 separator columns. Identify which geometric transform maps panel A to panel B, then apply that same transform to panel C. Output only the transformed query panel.

**Reference program (`solve_H57`)**

```python
def solve_H57(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    A,B,C = parts
    candidates = ["id","rot90","rot180","rot270","flip_h","flip_v","transpose","anti"]
    kind = None
    for k in candidates:
        if transform_grid(A, k) == B:
            kind = k
            break
    return transform_grid(C, kind)
```

### H58 — Prototype lookup up to symmetry

**What it tests:** Match a query shape to one of several prototype panels while allowing rotations and reflections.

**Staged hint:** Normalize the query, then compare it against all rotated and reflected versions of each prototype panel.

**Train 1 — input**

```text
20000903000944000900080
22000933000904400900888
00000903000900000900000
00000900000900000900000
00000900000900000900000
```

**Train 1 — output**

```text
00030
00333
00000
00000
00000
```

**Train 2 — input**

```text
20000950000977000900000
22000950000907700900000
00000950000900000900000
00000950000900000908800
00000900000900000988000
```

**Train 2 — output**

```text
00000
00000
00000
07700
77000
```

**Test — input**

```text
33000940000960000900000
03300944000960000900000
00000900000960000900080
00000900000960000900088
00000900000900000900008
```

**Test — expected output**

```text
00000
00000
00030
00033
00003
```

**Written solution**

Split the input into prototype panels and a query panel at the 9 separators. Compare the query shape against every symmetry of each prototype shape. Recolor the query with the color of the matching prototype and output only the recolored query panel.

**Reference program (`solve_H58`)**

```python
def solve_H58(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    *protos, query = parts
    qshape = {(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v != 0}
    qnorm,_,_ = normalize_cells(qshape)
    kinds = ["id","rot90","rot180","rot270","flip_h","flip_v","transpose","anti"]
    for panel in protos:
        cells = [(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v != 0]
        if not cells:
            continue
        color = next(v for row in panel for v in row if v != 0)
        shp,_,_ = normalize_cells(cells)
        for k in kinds:
            # build transformed shape as grid then normalize
            r0,r1,c0,c1 = bbox(cells)
            crop = [row[c0:c1+1] for row in panel[r0:r1+1]]
            t = transform_grid(crop, k)
            tcells = [(r,c) for r,row in enumerate(t) for c,v in enumerate(row) if v != 0]
            tnorm,_,_ = normalize_cells(tcells)
            if tnorm == qnorm:
                h,w = dims(query)
                out = blank(h,w,0)
                for r,c in [(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v != 0]:
                    out[r][c] = color
                return out
    return blank(*dims(query), 0)
```

### H59 — Pivot orbit painter

**What it tests:** Treat a local prototype as offsets from a pivot and generate its four quarter-turn copies.

**Staged hint:** Anchor everything to the 9 pivot. The output is not a translation; it is a rotation around that pivot.

**Train 1 — input**

```text
000000000
000030000
000022000
000002000
000090000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
000030000
000022000
002202000
032090230
000202200
000220000
000030000
000000000
```

**Train 2 — input**

```text
00000000000
00000000000
00000600000
00000440000
00000044000
00000900000
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
00000600000
00004440000
00044044000
00640904600
00044044000
00004440000
00000600000
00000000000
00000000000
```

**Test — input**

```text
00000000000
00000800000
00000020000
00000022000
00000000000
00000900000
00000000000
00000000000
00000000000
00000000000
00000000000
```

**Test — expected output**

```text
00000000000
00000800000
00000020000
00020022000
00220000000
08000900080
00000002200
00022002000
00002000000
00000800000
00000000000
```

**Written solution**

Use the 9 cell as the pivot. For each nonzero cell in the prototype, place copies at its 0°, 90°, 180°, and 270° rotations around the pivot, keeping the same color, and preserve the pivot.

**Reference program (`solve_H59`)**

```python
def solve_H59(g: Grid) -> Grid:
    h,w = dims(g)
    pivot = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 9)
    pr,pc = pivot
    out = blank(h,w,0)
    out[pr][pc] = 9
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or v == 9:
                continue
            dr,dc = r-pr, c-pc
            for rr,cc in [
                (pr + dr, pc + dc),
                (pr - dc, pc + dr),
                (pr - dr, pc - dc),
                (pr + dc, pc - dr),
            ]:
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = v
    return out
```

### H60 — Sort objects by size into bins

**What it tests:** Normalize components, rank them by area, and place them into ordered target bins.

**Staged hint:** First count component sizes. The bottom-row 1s are not objects to sort; they are destination markers.

**Train 1 — input**

```text
000000000000
022000300000
000000330000
000000000000
004000000000
004400000000
000400000000
000000000000
000000000000
010001000100
```

**Train 1 — output**

```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000000000
000000000400
000003000440
022003300040
010001000100
```

**Train 2 — input**

```text
0000000000000
0022000000000
0020000040000
0000000040000
0000000000000
0000600000000
0000660000000
0000066000000
0000000000000
0000000000000
0010001000100
```

**Train 2 — output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000600
0040002200660
0040002000066
0010001000100
```

**Test — input**

```text
0000000000000
0330000000000
0000000500000
0000000550000
0000000000000
0007000000000
0007700000000
0000770000000
0000000000000
0000000000000
0100001000100
```

**Test — expected output**

```text
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
0000000000700
0000005000770
0330005500077
0100001000100
```

**Written solution**

Find the three non-marker objects and sort them by increasing size. Normalize each object to its bounding box, then place the smallest above the leftmost marker, the next above the middle marker, and the largest above the rightmost marker, bottom-aligned to the row just above the markers. Keep the bottom-row markers.

**Reference program (`solve_H60`)**

```python
def solve_H60(g: Grid) -> Grid:
    h,w = dims(g)
    marker_cols = [c for c,v in enumerate(g[h-1]) if v == 1]
    comps = [(color,cells) for color,cells in same_color_components(g) if color != 1]
    comps = sorted(comps, key=lambda t: len(t[1]))
    out = blank(h,w,0)
    for c in marker_cols:
        out[h-1][c] = 1
    for (color,cells), mc in zip(comps, marker_cols):
        shp,(sh,sw),_ = normalize_cells(cells)
        top = h - 1 - sh
        left = mc
        # align bbox bottom-left to marker column
        for r,c in shp:
            rr,cc = top + r, left + c
            if 0 <= rr < h-1 and 0 <= cc < w:
                out[rr][cc] = color
    return out
```

### H61 — Apply the top-key color permutation

**What it tests:** Read an arbitrary symbolic color mapping and apply it to a picture.

**Staged hint:** The first two rows are a dictionary, not part of the picture.

**Train 1 — input**

```text
24600000
73800000
00000400
02200400
02000400
00000000
00066000
00000000
```

**Train 1 — output**

```text
00000300
07700300
07000300
00000000
00088000
00000000
```

**Train 2 — input**

```text
258000000
524000000
200000000
220000000
000050000
000055000
000000080
000000080
```

**Train 2 — output**

```text
500000000
550000000
000020000
000022000
000000040
000000040
```

**Test — input**

```text
346000000
682000000
000000000
033000400
030000400
000000400
000000000
000660000
000060000
```

**Test — expected output**

```text
000000000
066000800
060000800
000000800
000000000
000220000
000020000
```

**Written solution**

Interpret each column of the top two rows as an old-color to new-color mapping. Apply that permutation to every nonzero cell in the picture below and output only the transformed picture without the key rows.

**Reference program (`solve_H61`)**

```python
def solve_H61(g: Grid) -> Grid:
    h,w = dims(g)
    mapping = {}
    for c in range(w):
        a,b = g[0][c], g[1][c]
        if a != 0:
            mapping[a] = b
    out = blank(h-2, w, 0)
    for r in range(2,h):
        for c in range(w):
            v = g[r][c]
            out[r-2][c] = mapping.get(v, v)
    return out
```

### H62 — Nearest-seed fill inside the frame

**What it tests:** Frame detection plus Voronoi-style filling under a Manhattan metric.

**Staged hint:** Outside the frame never changes. Inside the frame, every blank cell chooses the nearest colored seed.

**Train 1 — input**

```text
000000000
077777770
072000070
070000670
070000070
070400070
070000070
077777770
000000000
```

**Train 1 — output**

```text
000000000
077777770
072226670
072266670
072446670
074444670
074444670
077777770
000000000
```

**Train 2 — input**

```text
0000000000
0777777770
0730000070
0700000070
0700000870
0700000070
0705000070
0700000070
0777777770
0000000000
```

**Train 2 — output**

```text
0000000000
0777777770
0733338870
0733388870
0735588870
0755558870
0755555870
0755555870
0777777770
0000000000
```

**Test — input**

```text
0000000000
0777777770
0700002070
0700000070
0700000070
0740000070
0700007070
0700000070
0777777770
0000000000
```

**Test — expected output**

```text
0000000000
0777777770
0742222270
0744222270
0744422270
0744442270
0744447270
0744442270
0777777770
0000000000
```

**Written solution**

Find the rectangular 7 frame and the colored seeds inside it. Fill every blank interior cell with the color of the nearest seed by Manhattan distance, breaking ties in favor of the smaller color. Keep the frame and the seeds.

**Reference program (`solve_H62`)**

```python
def solve_H62(g: Grid) -> Grid:
    h,w = dims(g)
    frame = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7]
    r0,r1,c0,c1 = bbox(frame)
    seeds = [(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,7)]
    out = clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c] == 0:
                best = min(seeds, key=lambda t: (abs(t[0]-r)+abs(t[1]-c), t[2]))
                out[r][c] = best[2]
    return out
```

### H63 — Rank-fill mask components from a palette

**What it tests:** Panel parsing, component ranking, and palette-driven recoloring.

**Staged hint:** The right panel is an ordered palette. The left panel's gray components should be colored by size rank, not by position.

**Train 1 — input**

```text
0000000092
0880088094
0000088096
0880000090
0800000090
0000000090
0000000090
0000000090
```

**Train 1 — output**

```text
00000000
02200660
00000660
04400000
04000000
00000000
00000000
00000000
```

**Train 2 — input**

```text
00000000093
08800080095
08800080098
08000000090
00880000090
00800000090
00000000090
00000000090
00000000090
```

**Train 2 — output**

```text
000000000
088000300
088000300
080000000
005500000
005000000
000000000
000000000
000000000
```

**Test — input**

```text
00000000094
00880080096
00000088092
00000008090
08800000090
08000000090
00000000090
00000000090
00000000090
```

**Test — expected output**

```text
000000000
004400200
000000220
000000020
066000000
060000000
000000000
000000000
000000000
```

**Written solution**

Split the grid at the 9 separator. Read the nonzero colors in the right panel from top to bottom as an ordered palette. In the left panel, sort the gray components by increasing size and recolor the smallest with the first palette color, the next with the second, and the largest with the third. Output only the recolored left panel.

**Reference program (`solve_H63`)**

```python
def solve_H63(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    left,right = parts
    palette = [right[r][0] for r in range(len(right)) if right[r][0] != 0]
    comps = [(cells) for color,cells in same_color_components(left) if color == 8]
    comps = sorted(comps, key=len)
    h,w = dims(left)
    out = blank(h,w,0)
    for cells,color in zip(comps, palette):
        for r,c in cells:
            out[r][c] = color
    return out
```
