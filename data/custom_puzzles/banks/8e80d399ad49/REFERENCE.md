# 21 More ARC-Style Puzzles

This is the tenth continuation bank: **7 easy, 7 medium, 7 hard**.
It carries the sequence forward as **E64–E70, M64–M70, H64–H70**.

Each puzzle includes:
- 2 training pairs
- 1 test input
- the expected test output
- a written solution
- a reference program solution

This batch leans into interval completion, local symbolic legends, component sweeping, frame transplant, panel inference, labeled dispatch, compartment filling, transform programs, and shape packing.

**New motifs in this batch**

**`sweep_component_away(anchor, shape)`** — infer a direction from the side on which an anchor sits, then extrude a whole component through the grid. This is the main idea in **M64**.

**`infer_panel_transform(example_in, example_out, query)`** — use one panel pair as a geometric teaching example, then apply the discovered transform to a new panel. This drives **H64**.

**`label_dispatch(components, labels, targets)`** — match components to labels in one part of the grid and move them to target labels elsewhere. This is the key move in **H65**.

**`compartment_seed_fill(frame, walls, seeds)`** — treat walls as hard barriers, find chambers, and flood each one from its seed. This is most visible in **H67**.

**`compose_ops(header, shape)`** — interpret a row of transform tokens as a tiny program and execute it on the body shape. This is the central idea in **H68**.

**`sort_pack_palette(components, palette)`** — normalize several shapes, sort them, recolor them from a palette, and pack them onto a compact output strip. This appears in **H70**.

## Easy

### E64 — Column bridge fill

**What it tests:** Find matching vertical endpoints and fill the blank segment between them.

**Staged hint:** Work column by column. Only pay attention to colors that appear exactly twice in a column.

**Train 1 — input**

```text
0000040
0200000
0006000
0000040
0200000
0000000
0006000
```

**Train 1 — output**

```text
0000040
0200040
0206040
0206040
0206000
0006000
0006000
```

**Train 2 — input**

```text
00000007
30000000
00005007
00000000
00000000
30000000
00005000
00000000
```

**Train 2 — output**

```text
00000007
30000007
30005007
30005000
30005000
30005000
00005000
00000000
```

**Test — input**

```text
000002000
008000000
000000000
000000004
000002000
000000000
008000000
000000004
```

**Test — expected output**

```text
000002000
008002000
008002000
008002004
008002004
008000004
008000004
000000004
```

**Written solution**

For each column, look for a color that appears exactly twice with only zeros between the two endpoints. Fill that whole vertical interval with the same color and leave everything else unchanged.

**Reference program (`solve_E64`)**

```python
def solve_E64(g):
    out=clone(g); h,w=dims(g)
    for c in range(w):
        by={}
        for r in range(h):
            v=g[r][c]
            if v!=0:
                by.setdefault(v,[]).append(r)
        for color,rows in by.items():
            if len(rows)==2:
                a,b=min(rows),max(rows)
                if all(g[r][c]==0 for r in range(a+1,b)):
                    for r in range(a,b+1):
                        out[r][c]=color
    return out
```

### E65 — Ring-center fill

**What it tests:** Detect hollow 3x3 monochrome rings and fill their center cell.

**Staged hint:** Ignore the whole grid at first and just scan for 3x3 neighborhoods whose eight outer cells all match.

**Train 1 — input**

```text
0000000000
0222000000
0202000000
0222000000
0000004440
0000004040
0000004440
0000000000
```

**Train 1 — output**

```text
0000000000
0222000000
0222000000
0222000000
0000004440
0000004440
0000004440
0000000000
```

**Train 2 — input**

```text
333000000
303000000
333006660
000006060
000006660
000000000
000000000
```

**Train 2 — output**

```text
333000000
333000000
333006660
000006660
000006660
000000000
000000000
```

**Test — input**

```text
000000000
000055500
000050500
000055500
088800000
080800000
088800000
000000000
```

**Test — expected output**

```text
000000000
000055500
000055500
000055500
088800000
088800000
088800000
000000000
```

**Written solution**

Whenever a zero cell is surrounded on all eight sides by the same nonzero color, replace the center with that color. The surrounding ring stays the same.

**Reference program (`solve_E65`)**

```python
def solve_E65(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            neigh=[g[r+dr][c+dc] for dr in (-1,0,1) for dc in (-1,0,1) if not (dr==0 and dc==0)]
            if neigh[0]!=0 and all(v==neigh[0] for v in neigh):
                out[r][c]=neigh[0]
    return out
```

### E66 — Mirror across the 9 anchor

**What it tests:** Use a row-local pivot to reflect a pattern onto the opposite side.

**Staged hint:** Treat each row separately. The 9 marks the mirror line for that row.

**Train 1 — input**

```text
000000000
022090000
000090330
000000000
444090000
000000000
```

**Train 1 — output**

```text
000000000
022090220
033090330
000000000
444090444
000000000
```

**Train 2 — input**

```text
00000000000
00555090000
00000000000
00009006600
00000000000
08000900000
00000000000
```

**Train 2 — output**

```text
00000000000
00555090555
00000000000
66009006600
00000000000
08000900080
00000000000
```

**Test — input**

```text
0000000000
0222090000
0000000000
0000900440
0000000000
6609000000
0000000000
```

**Test — expected output**

```text
0000000000
0222090222
0000000000
4400900440
0000000000
6609066000
0000000000
```

**Written solution**

In any row containing a 9, copy every nonzero cell to the symmetric position on the opposite side of the 9, at the same distance. Keep the original cells and the 9.

**Reference program (`solve_E66`)**

```python
def solve_E66(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        if 9 not in g[r]:
            continue
        p=g[r].index(9)
        for c,v in enumerate(g[r]):
            if v not in (0,9):
                cc=2*p-c
                if 0<=cc<w:
                    out[r][cc]=v
    return out
```

### E67 — Complete the rectangle corner

**What it tests:** Infer an axis-aligned rectangle from three same-colored corners.

**Staged hint:** Group by color. Three cells may already tell you two rows and two columns.

**Train 1 — input**

```text
0000000300
0200200000
0000000000
0000000303
0200000000
0000000000
```

**Train 1 — output**

```text
0000000303
0200200000
0000000000
0000000303
0200200000
0000000000
```

**Train 2 — input**

```text
600600000
000000000
004000000
000000000
000600000
004004000
000000000
```

**Train 2 — output**

```text
600600000
000000000
004004000
000000000
600600000
004004000
000000000
```

**Test — input**

```text
0000000000
0000005000
0800800000
0000000000
0000005050
0000000000
0800000000
0000000000
```

**Test — expected output**

```text
0000000000
0000005050
0800800000
0000000000
0000005050
0000000000
0800800000
0000000000
```

**Written solution**

For each color, if its three cells occupy exactly two distinct rows and two distinct columns, fill the missing fourth corner of that rectangle.

**Reference program (`solve_E67`)**

```python
def solve_E67(g):
    out=clone(g)
    by={}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v,[]).append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            rs=sorted({r for r,c in cells}); cs=sorted({c for r,c in cells})
            if len(rs)==2 and len(cs)==2:
                for rr in rs:
                    for cc in cs:
                        out[rr][cc]=color
    return out
```

### E68 — Row majority cleanup

**What it tests:** Use within-row frequency to repair a single odd colored cell.

**Staged hint:** Look only at nonzero rows and count colors instead of geometry.

**Train 1 — input**

```text
00000000
22420000
00000000
57550000
00000000
```

**Train 1 — output**

```text
00000000
22220000
00000000
55550000
00000000
```

**Train 2 — input**

```text
000000000
363330000
000000000
088280000
000000000
```

**Train 2 — output**

```text
000000000
333330000
000000000
088880000
000000000
```

**Test — input**

```text
000000000
441440000
000000000
696600000
000000000
```

**Test — expected output**

```text
000000000
444440000
000000000
666600000
000000000
```

**Written solution**

In each row that contains exactly two nonzero colors, if one color appears once and the other appears multiple times, recolor the lone odd cell to the majority color.

**Reference program (`solve_E68`)**

```python
def solve_E68(g):
    out=clone(g)
    for r,row in enumerate(g):
        counts={}
        for v in row:
            if v!=0:
                counts[v]=counts.get(v,0)+1
        if len(counts)==2:
            maj=max(counts, key=lambda k: counts[k])
            minc=min(counts.values())
            maxc=max(counts.values())
            if minc==1 and maxc>1:
                odd=[k for k,v in counts.items() if v==1][0]
                for c,v in enumerate(row):
                    if v==odd:
                        out[r][c]=maj
    return out
```

### E69 — Extend the diagonal chain

**What it tests:** Continue a two-cell diagonal in the same direction by one step.

**Staged hint:** Find colors that occur exactly twice and check whether those two cells are touching diagonally.

**Train 1 — input**

```text
0000000
0200040
0020400
0000000
0000000
0000000
0000000
```

**Train 1 — output**

```text
0000000
0200040
0020400
0004000
0000000
0000000
0000000
```

**Train 2 — input**

```text
00000000
00000060
03000600
00300000
00080000
00008000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00000060
03000600
00306000
00030000
00008000
00000800
00000000
```

**Test — input**

```text
000000000
005000000
000500070
000000700
400000000
040000000
000000000
000000000
```

**Test — expected output**

```text
000000000
005000000
000500070
000050700
400007000
040000000
004000000
000000000
```

**Written solution**

If a color forms a two-cell diagonal step, extend that diagonal one more cell in the same direction from the upper cell to the lower cell.

**Reference program (`solve_E69`)**

```python
def solve_E69(g):
    out=clone(g)
    by={}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v,[]).append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=sorted(cells)
            dr=r2-r1; dc=c2-c1
            if abs(dr)==1 and abs(dc)==1:
                rr,cc=r2+dr,c2+dc
                if 0<=rr<len(g) and 0<=cc<len(g[0]):
                    out[rr][cc]=color
    return out
```

### E70 — Column recolor by header

**What it tests:** Read a color legend from the top row and apply it columnwise.

**Staged hint:** Treat the top row as metadata. The body only contributes shape, not final color.

**Train 1 — input**

```text
2040608
1030507
0090200
4000106
```

**Train 1 — output**

```text
2040608
2040608
0040600
2000608
```

**Train 2 — input**

```text
03050702
01010101
09080403
00060005
```

**Train 2 — output**

```text
03050702
03050702
03050702
00050002
```

**Test — input**

```text
40602080
10305070
90109030
20406080
```

**Test — expected output**

```text
40602080
40602080
40602080
40602080
```

**Written solution**

Keep the header row. For every nonzero body cell, recolor it to the header color from the same column. Zeros stay zero.

**Reference program (`solve_E70`)**

```python
def solve_E70(g):
    out=clone(g); h,w=dims(g)
    headers=g[0]
    for r in range(1,h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=headers[c] if headers[c]!=0 else g[r][c]
    return out
```

## Medium

### M64 — Sweep the component away from the anchor

**What it tests:** Infer a direction from an anchor and extrude an entire component through space.

**Staged hint:** Find the one shape and the one 9, then ask which side of the shape the anchor sits on.

**Train 1 — input**

```text
000000000
002200000
092200000
000000000
000000000
000000000
000000000
```

**Train 1 — output**

```text
000000000
002222222
092222222
000000000
000000000
000000000
000000000
```

**Train 2 — input**

```text
00000000
00009000
00044000
00040000
00000000
00000000
00000000
00000000
00000000
```

**Train 2 — output**

```text
00000000
00009000
00044000
00044000
00044000
00044000
00044000
00044000
00040000
```

**Test — input**

```text
0000000000
0000000000
0000000000
0000060000
0000060900
0000066000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000000000
0000000000
6666660000
6666660900
6666666000
0000000000
0000000000
```

**Written solution**

The 9 sits just outside one side of the shape. Determine the direction pointing away from the 9 through the component, then repeatedly translate the whole component one step in that direction until it would leave the grid. Paint the full swept union and keep the 9.

**Reference program (`solve_M64`)**

```python
def solve_M64(g):
    out=clone(g)
    h,w=dims(g)
    # component excluding 0 and 9, assume one color component
    comps=[(v,cells) for v,cells in components_by_color(g, ignore=(0,9))]
    assert len(comps)==1
    color,cells=comps[0]
    r0,r1,c0,c1=bbox(cells)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    assert len(anchors)==1
    ar,ac=anchors[0]
    if ac < c0:
        dr,dc = 0,1
    elif ac > c1:
        dr,dc = 0,-1
    elif ar < r0:
        dr,dc = 1,0
    else:
        dr,dc = -1,0
    norm=list(cells)
    k=1
    while True:
        shifted=[(r+dr*k,c+dc*k) for r,c in norm]
        if any(not (0<=r<h and 0<=c<w) for r,c in shifted):
            break
        for r,c in shifted:
            out[r][c]=color
        k+=1
    return out
```

### M65 — Palette rank recolor

**What it tests:** Sort components by size and recolor them using an ordered palette.

**Staged hint:** The first row is not part of the scene; it is a list of target colors.

**Train 1 — input**

```text
2040600000
0000000000
0800008800
0000000000
0008800000
0008000000
0000000000
0000000000
```

**Train 1 — output**

```text
2040600000
0000000000
0200004400
0000000000
0006600000
0006000000
0000000000
0000000000
```

**Train 2 — input**

```text
03050700000
00000000000
00000000800
00000000000
08800000000
00000000000
00000088000
00000088000
00000000000
```

**Train 2 — output**

```text
03050700000
00000000000
00000000300
00000000000
05500000000
00000000000
00000077000
00000077000
00000000000
```

**Test — input**

```text
40607000000
00000000000
00000800000
00000000000
00000000800
00000000800
08800000000
08000000000
00000000000
```

**Test — expected output**

```text
40607000000
00000000000
00000400000
00000000000
00000000600
00000000600
07700000000
07000000000
00000000000
```

**Written solution**

Read the nonzero colors in the top row as a palette. In the body, find all placeholder-color components, sort them from smallest to largest, and recolor them in palette order.

**Reference program (`solve_M65`)**

```python
def solve_M65(g):
    out=clone(g)
    headers=[v for v in g[0] if v!=0]
    comps=[cells for v,cells in components_by_color(g, ignore=(0,)) if v==8]
    comps=sorted(comps, key=lambda cells: (len(cells), bbox(cells)))
    for cells,color in zip(comps, headers):
        for r,c in cells:
            out[r][c]=color
    return out
```

### M66 — Two-row legend remap

**What it tests:** Use an explicit source→target legend to remap colors in a scene.

**Staged hint:** The first two rows form aligned pairs: top is source color, second row is target color.

**Train 1 — input**

```text
20406000
30507000
02040600
60402000
00220040
```

**Train 1 — output**

```text
20406000
30507000
03050700
70503000
00330050
```

**Train 2 — input**

```text
103050000
806020000
010305000
503010000
001500300
```

**Train 2 — output**

```text
103050000
806020000
080602000
206080000
008200600
```

**Test — input**

```text
205070000
406030000
020507000
705020000
002700500
```

**Test — expected output**

```text
205070000
406030000
040603000
306040000
004300600
```

**Written solution**

Build a color mapping from the first two rows column by column. Then recolor the body using that mapping while leaving zeros and the legend rows unchanged.

**Reference program (`solve_M66`)**

```python
def solve_M66(g):
    out=clone(g)
    mapping={}
    w=len(g[0])
    for c in range(w):
        a,b=g[0][c],g[1][c]
        if a!=0:
            mapping[a]=b
    for r in range(2,len(g)):
        for c in range(w):
            v=g[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out
```

### M67 — Transplant the framed interior

**What it tests:** Extract a subgrid from one frame and center it inside another.

**Staged hint:** Ignore the outer canvas and compare the two color-7 frames by size.

**Train 1 — input**

```text
00000000000000
07777700777770
07220700700070
07200700700070
07000700700070
07777700700070
00000000700070
00000000777770
00000000000000
00000000000000
```

**Train 1 — output**

```text
00000000000000
07777700777770
07220700700070
07200700722070
07000700720070
07777700700070
00000000700070
00000000777770
00000000000000
00000000000000
```

**Train 2 — input**

```text
000000000000000
000000000777770
077777700700070
074040700700070
070440700700070
077777700700070
000000000700070
000000000700070
000000000777770
000000000000000
000000000000000
```

**Train 2 — output**

```text
000000000000000
000000000777770
077777700700070
074040700700070
070440700404070
077777700744070
000000000700070
000000000700070
000000000777770
000000000000000
000000000000000
```

**Test — input**

```text
000000000000000
077777700777777
076600700700007
070600700700007
070060700700007
077777700700007
000000000700007
000000000777777
000000000000000
000000000000000
```

**Test — expected output**

```text
000000000000000
077777700777777
076600700700007
070600700766007
070060700706007
077777700700607
000000000700007
000000000777777
000000000000000
000000000000000
```

**Written solution**

Find the smaller frame and copy its interior contents. Then place that interior, without scaling, centered inside the larger frame’s interior. Keep both frames.

**Reference program (`solve_M67`)**

```python
def solve_M67(g):
    out=clone(g)
    frames=[cells for v,cells in components_by_color(g, ignore=(0,)) if v==7 and is_frame_component(cells)]
    frames=sorted(frames, key=len)
    small,big=frames[0],frames[1]
    sr0,sr1,sc0,sc1=bbox(small)
    br0,br1,bc0,bc1=bbox(big)
    interior=[row[sc0+1:sc1] for row in g[sr0+1:sr1]]
    ih,iw=len(interior), len(interior[0])
    top=br0+1 + ((br1-br0-1)-ih)//2
    left=bc0+1 + ((bc1-bc0-1)-iw)//2
    overlay(out, interior, top, left, transparent=0)
    return out
```

### M68 — BBox row/column cross-product

**What it tests:** Move from object bboxes to a blank interaction grid.

**Staged hint:** Red tells you rows; blue tells you columns.

**Train 1 — input**

```text
0000300000
0220330000
0200000000
0000000030
0000000033
0000002000
0000002000
0000000000
```

**Train 1 — output**

```text
0000000000
0000880088
0000880088
0000000000
0000000000
0000880088
0000880088
0000000000
```

**Train 2 — input**

```text
000000000
000000300
200000300
220000000
003300000
003000000
000022000
000002000
000000000
```

**Train 2 — output**

```text
000000000
000000000
008800800
008800800
000000000
000000000
008800800
008800800
000000000
```

**Test — input**

```text
0000300000
0000330200
0000000220
0000000030
0000000030
0200000000
0220000000
0000000000
0000000000
```

**Test — expected output**

```text
0000000000
0000880080
0000880080
0000000000
0000000000
0000880080
0000880080
0000000000
0000000000
```

**Written solution**

Take the union of all rows covered by red-object bounding boxes and the union of all columns covered by blue-object bounding boxes. Output a blank grid with 8 at every intersection of an active row and an active column.

**Reference program (`solve_M68`)**

```python
def solve_M68(g):
    h,w=dims(g)
    out=blank(h,w,0)
    rows=set()
    cols=set()
    for color,cells in components_by_color(g, ignore=(0,)):
        r0,r1,c0,c1=bbox(cells)
        if color==2:
            rows.update(range(r0,r1+1))
        elif color==3:
            cols.update(range(c0,c1+1))
    for r in rows:
        for c in cols:
            out[r][c]=8
    return out
```

### M69 — Prototype lookup by key color

**What it tests:** Retrieve a stored prototype shape and stamp it at a query anchor.

**Staged hint:** The upper section is a library. The lower section asks for one entry from that library.

**Train 1 — input**

```text
2000440006000
2200040066600
0000000000000
0000000000000
9999999999999
0000000000000
0400000800000
0000000000000
0000000000000
0000000000000
```

**Train 1 — output**

```text
2000440006000
2200040066600
0000000000000
0000000000000
9999999999999
0000000000000
0400000440000
0000000040000
0000000000000
0000000000000
```

**Train 2 — input**

```text
03000050007700
03000550007000
03300000007000
00000000000000
00000000000000
99999999999999
00000000000000
70000000800000
00000000000000
00000000000000
00000000000000
```

**Train 2 — output**

```text
03000050007700
03000550007000
03300000007000
00000000000000
00000000000000
99999999999999
00000000000000
70000000770000
00000000700000
00000000700000
00000000000000
```

**Test — input**

```text
20000440006000
22000040066600
00000000000000
00000000000000
99999999999999
00000000000000
00200000080000
00000000000000
00000000000000
00000000000000
```

**Test — expected output**

```text
20000440006000
22000040066600
00000000000000
00000000000000
99999999999999
00000000000000
00200000020000
00000000022000
00000000000000
00000000000000
```

**Written solution**

Above the separator row, each color defines a prototype shape. Below the separator, a single key color selects one prototype, and an 8 marks where to place it. Copy the selected normalized prototype to the anchor position in the lower section.

**Reference program (`solve_M69`)**

```python
def solve_M69(g):
    h,w=dims(g)
    sep = next(r for r in range(h) if all(v==9 for v in g[r]))
    top = g[:sep]
    bottom = g[sep+1:]
    # prototypes in top keyed by their nonzero color
    comps=[(v,cells) for v,cells in components_by_color(top, ignore=(0,))]
    protos={}
    for color,cells in comps:
        shp,(sh,sw),_ = normalize_cells(cells)
        protos[color]=(shp,sh,sw)
    key = next(v for row in bottom for v in row if v not in (0,8))
    ar,ac = next((r,c) for r,row in enumerate(bottom) for c,v in enumerate(row) if v==8)
    out=clone(g)
    shp,sh,sw=protos[key]
    for r,c in shp:
        rr,cc=sep+1 + ar + r, ac + c
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=key
    return out
```

### M70 — Rectangle intersection mask

**What it tests:** Compute overlap from two framed rectangles rather than from filled pixels.

**Staged hint:** Think in terms of bounding boxes, not border pixels.

**Train 1 — input**

```text
0000000000
0222222000
0200002000
0200333330
0200302030
0222322030
0000333330
0000000000
```

**Train 1 — output**

```text
0000000000
0000000000
0000000000
0000888000
0000888000
0000888000
0000000000
0000000000
```

**Train 2 — input**

```text
00022222200
00020000200
03333300200
03020300200
03020300200
03020300200
03022322200
03000300000
03333300000
```

**Train 2 — output**

```text
00000000000
00000000000
00088800000
00088800000
00088800000
00088800000
00088800000
00000000000
00000000000
```

**Test — input**

```text
000000000000
002222220000
002000020000
002003333330
002003020030
002003020030
002003020030
002223220030
000003333330
```

**Test — expected output**

```text
000000000000
000000000000
000000000000
000008880000
000008880000
000008880000
000008880000
000008880000
000000000000
```

**Written solution**

Find the bounding rectangles traced by the color-2 border and the color-3 border. Output a blank grid with 8 filling only the overlapping area of those two rectangles.

**Reference program (`solve_M70`)**

```python
def solve_M70(g):
    h,w=dims(g)
    out=blank(h,w,0)
    rects={}
    for color in (2,3):
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]
        rects[color]=bbox(cells)
    a0,a1,b0,b1=rects[2]
    c0,c1,d0,d1=rects[3]
    r0,r1=max(a0,c0), min(a1,c1)
    c0_,c1_=max(b0,d0), min(b1,d1)
    if r0<=r1 and c0_<=c1_:
        for r in range(r0,r1+1):
            for c in range(c0_,c1_+1):
                out[r][c]=8
    return out
```

## Hard

### H64 — Infer the panel transform and apply it

**What it tests:** Infer a geometric transform from one panel pair and apply it to a new panel.

**Staged hint:** The first two panels teach the transform. The third panel is the query.

**Train 1 — input**

```text
20009002290400
22209002090440
00209022090040
00009000090000
```

**Train 1 — output**

```text
0000
0044
0440
0000
```

**Train 2 — input**

```text
00309003095500
33309003090500
00309033390500
00009000090000
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
60009006690700
66009066097700
06609060097000
00009000090000
```

**Test — expected output**

```text
0770
0077
0000
0000
```

**Written solution**

Split the input into three panels using the separator columns. Determine which geometric transform turns the first panel into the second, then apply that same transform to the third panel and output only the transformed query panel.

**Reference program (`solve_H64`)**

```python
def solve_H64(g):
    parts,_ = split_by_separator_cols(g, sep=9)
    a,b,c = parts
    cands = [
        rotate_cw,
        rotate180,
        lambda x: rotate_cw(rotate180(x)),
        flip_h,
        flip_v,
    ]
    for fn in cands:
        if fn(a) == b:
            return fn(c)
    return c
```

### H65 — Dispatch labeled components to target labels

**What it tests:** Associate components with labels, then move them to matching destinations.

**Staged hint:** Do not sort by color or position. The labels tell you the correspondence.

**Train 1 — input**

```text
00000000000000
14400000038000
04000260008800
00000066008000
00000000000000
00000000000000
00000000000000
00000000000000
01000020003000
```

**Train 1 — output**

```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
00000000008000
04400060008800
04000066008000
01000020003000
```

**Train 2 — input**

```text
000000000000000
015000000000000
005500000034000
000002770004000
000000070004400
000000000000000
000000000000000
000000000000000
000000000000000
100002000030000
```

**Train 2 — output**

```text
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
000000000040000
500007700040000
550000700044000
100002000030000
```

**Test — input**

```text
0000000000000000
1600000000034400
0660002800000400
0000000880000000
0000000800000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0010000020003000
```

**Test — expected output**

```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0000000080000000
0060000088004400
0066000080000400
0010000020003000
```

**Written solution**

Each source component is tagged by a nearby label 1, 2, or 3. The bottom row contains target labels. Remove the source layout, preserve the bottom-row labels, and place each normalized component above the matching target label.

**Reference program (`solve_H65`)**

```python
def solve_H65(g):
    h,w=dims(g)
    out=blank(h,w,0)
    # preserve target labels on bottom row
    target_cols={}
    for c,v in enumerate(g[h-1]):
        if v in (1,2,3):
            out[h-1][c]=v
            target_cols[v]=c
    seen=set()
    sources=[]
    for r in range(h-1):
        for c in range(w):
            if g[r][c] in (1,2,3):
                label=g[r][c]
                # component starts somewhere to the right
                for cc in range(c+1, min(w, c+4)):
                    if g[r][cc] not in (0,1,2,3):
                        cells=bfs_same_color(g, (r,cc), seen)
                        sources.append((label,cells,g[r][cc]))
                        break
    for label,cells,color in sources:
        shp,(sh,sw),_ = normalize_cells(cells)
        base_col=target_cols[label]
        top = h-1-sh
        left = base_col
        for r,c in shp:
            rr,cc=top+r,left+c
            if 0<=rr<h-1 and 0<=cc<w:
                out[rr][cc]=color
    return out
```

### H66 — Quarter-turn orbit from a count header

**What it tests:** Use a symbolic count to control how many rotated copies of a prototype appear.

**Staged hint:** Separate three roles: the count cell, the pivot 9, and the prototype shape.

**Train 1 — input**

```text
200000000
000000000
000000000
000000000
000096600
000006000
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
000096600
000666000
000060000
000000000
000000000
```

**Train 2 — input**

```text
300000000
000000000
000070000
000077000
000090000
000000000
000000000
000000000
000000000
```

**Train 2 — output**

```text
000000000
000000000
000070000
000077000
000097700
000777000
000070000
000000000
000000000
```

**Test — input**

```text
400000000
000000000
000000000
000000000
000890000
008800000
000000000
000000000
000000000
```

**Test — expected output**

```text
000000000
000000000
000800000
000888800
000898000
008888000
000008000
000000000
000000000
```

**Written solution**

The top-left cell gives a count from 1 to 4. Around the pivot 9, take the prototype shape’s offsets and union the first N quarter-turn rotations of that prototype. Output the orbit on a blank grid, keeping the pivot.

**Reference program (`solve_H66`)**

```python
def solve_H66(g):
    h,w=dims(g)
    n=g[0][0]
    pivot=next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9)
    pr,pc=pivot
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,9) and not (r==0 and c==0)]
    # assume one color
    color = cells[0][2]
    offsets=[(r-pr, c-pc) for r,c,v in cells]
    def rot(dr,dc, k):
        for _ in range(k):
            dr,dc = dc,-dr
        return dr,dc
    out=blank(h,w,0)
    out[pr][pc]=9
    for k in range(n):
        for dr,dc in offsets:
            rr,cc = pr+rot(dr,dc,k)[0], pc+rot(dr,dc,k)[1]
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=color
    return out
```

### H67 — Seed-fill the wall compartments

**What it tests:** Flood-fill regions defined by walls, preserving structure and seed colors.

**Staged hint:** Treat 5 and 7 as barriers. Everything else inside a chamber belongs together.

**Train 1 — input**

```text
77777777777
70000500007
70200500007
70000500607
75555500007
70000500007
70400500007
70000500007
77777777777
```

**Train 1 — output**

```text
77777777777
72222566667
72222566667
72222566667
75555566667
74444566667
74444566667
74444566667
77777777777
```

**Train 2 — input**

```text
777777777777
700050205007
703050005007
700055555007
700050005407
755550005007
700050805007
706050005557
700050005007
777777777777
```

**Train 2 — output**

```text
777777777777
733352225447
733352225447
733355555447
733358885447
755558885447
766658885447
766658885557
766658885007
777777777777
```

**Test — input**

```text
777777777777
720050005007
700050305007
755550005007
700050005047
700050005557
706050005007
700050005007
777777777777
```

**Test — expected output**

```text
777777777777
722253335447
722253335447
755553335447
766653335447
766653335557
766653335007
766653335007
777777777777
```

**Written solution**

Use the walls and outer frame to partition the grid into compartments. If a compartment contains exactly one seed color, fill all zeros in that compartment with that seed color while leaving the walls and seeds intact.

**Reference program (`solve_H67`)**

```python
def solve_H67(g):
    h,w=dims(g)
    out=clone(g)
    seen=set()
    walls={5,7}
    for r in range(h):
        for c in range(w):
            if g[r][c] in walls or (r,c) in seen:
                continue
            # region of non-wall cells
            q=deque([(r,c)]); seen.add((r,c))
            region=[]; colors=set()
            while q:
                x,y=q.popleft(); region.append((x,y))
                if g[x][y] not in (0,5,7):
                    colors.add(g[x][y])
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and g[nx][ny] not in walls and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if len(colors)==1:
                color=next(iter(colors))
                for x,y in region:
                    if out[x][y]==0:
                        out[x][y]=color
    return out
```

### H68 — Execute the transform sequence

**What it tests:** Interpret a symbolic operation list and compose multiple transforms.

**Staged hint:** The top row is a program. The body is the data.

**Train 1 — input**

```text
130000
020000
022000
002000
000000
```

**Train 1 — output**

```text
220
022
```

**Train 2 — input**

```text
2300000
0040000
0440000
0400000
0000000
```

**Train 2 — output**

```text
044
440
```

**Test — input**

```text
310000
550000
050000
055000
000000
```

**Test — expected output**

```text
500
555
005
```

**Written solution**

Read the nonzero entries in the first row as an ordered sequence of transforms: 1=flip horizontally, 2=flip vertically, 3=rotate 90° clockwise, 4=rotate 180°. Crop the body to its nonzero bounding box, apply the transforms in order, and output the resulting minimal grid.

**Reference program (`solve_H68`)**

```python
def solve_H68(g):
    ops=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    body=crop_nonzero(body)
    return apply_ops(body, ops)
```

### H69 — Infer a color permutation from panels

**What it tests:** Infer a symbolic recoloring rule from aligned example panels.

**Staged hint:** Ignore geometry first: the supports already match. The hard part is the color mapping.

**Train 1 — input**

```text
20309406095020
25309476090320
05009070090300
00009000090000
```

**Train 1 — output**

```text
7040
0640
0600
0000
```

**Train 2 — input**

```text
03009060090500
23509467093520
20509407090020
00009000090000
```

**Train 2 — output**

```text
0700
6740
0040
0000
```

**Test — input**

```text
03009060092050
23509467093500
20509407093020
00009000090000
```

**Test — expected output**

```text
4070
6700
6040
0000
```

**Written solution**

Split the input into three equal panels. The first and second panels have the same shape pattern but different colors; use corresponding positions to infer the color permutation, then recolor the third panel with that same mapping and output only the recolored third panel.

**Reference program (`solve_H69`)**

```python
def solve_H69(g):
    parts,_ = split_by_separator_cols(g, sep=9)
    a,b,c = parts
    mapping={}
    h,w=dims(a)
    for r in range(h):
        for col in range(w):
            va,vb=a[r][col], b[r][col]
            if va!=0:
                mapping[va]=vb
    out=blank(h,w,0)
    for r in range(h):
        for col in range(w):
            v=c[r][col]
            if v!=0:
                out[r][col]=mapping.get(v,v)
    return out
```

### H70 — Sort, pack, and recolor the shape inventory

**What it tests:** Combine object normalization, size ordering, palette assignment, and packing.

**Staged hint:** There are four separate subproblems: extract, normalize, order, then place.

**Train 1 — input**

```text
204060000000
000000000000
088000008000
088000008800
000000000000
000008000000
000000000000
000000000000
```

**Train 1 — output**

```text
2204000
2204406
```

**Train 2 — input**

```text
0305070000000
0000000000000
0000000000800
0000080000800
0000000000800
0880000000000
0880000000000
0000000000000
0000000000000
```

**Train 2 — output**

```text
000500
330500
330507
```

**Test — input**

```text
40602000000000
00000000000000
08800000800000
00800000880000
00800000000000
00000000000000
00000080000000
00000000000000
00000000000000
```

**Test — expected output**

```text
4400000
0406000
0406602
```

**Written solution**

Use the top row as a palette. In the body, extract all placeholder-color components, normalize each one, sort them by size from largest to smallest, recolor them in palette order, and pack them left-to-right with one blank column between shapes on the smallest possible blank canvas.

**Reference program (`solve_H70`)**

```python
def solve_H70(g):
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    comps=[cells for v,cells in components_by_color(body, ignore=(0,)) if v==8]
    comps=sorted(comps, key=lambda cells: (-len(cells), bbox(cells)))
    shapes=[]
    maxh=0
    for cells,color in zip(comps,palette):
        shp,(sh,sw),_ = normalize_cells(cells)
        shapes.append((shp,sh,sw,color))
        maxh=max(maxh,sh)
    totalw=sum(sw for _,_,sw,_ in shapes) + max(0,len(shapes)-1)
    out=blank(maxh,totalw,0)
    x=0
    for shp,sh,sw,color in shapes:
        top=maxh-sh
        for r,c in shp:
            out[top+r][x+c]=color
        x += sw+1
    return out
```
