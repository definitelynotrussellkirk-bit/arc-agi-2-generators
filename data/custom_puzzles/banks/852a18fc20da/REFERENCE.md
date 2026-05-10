# ARC Additional Puzzle Bank — 21 Puzzles (Set 13)

This thirteenth pack continues the numbering with **`E85–E91`**, **`M85–M91`**, and **`H85–H91`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
sprout_kernel(seed_cells, offsets, color_lookup=None, allowed=None, priority=None)
```

This helper captures seed-based local expansion with optional clipping and conflict resolution. In this pack it is used directly in **E85**, **M85**, and **H85**.

## E85 — Sprout Plus Seeds

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local expansion, seed-based transform, same-size

**Suggested staged path:** Treat every nonzero cell as a seed. Then apply the same tiny offset pattern around it.


**Train 1 — input**
```text
0000000
0000000
0050000
0000000
0000070
0000000
0000000
```
**Train 1 — output**
```text
0000000
0050000
0555000
0050070
0000777
0000070
0000000
```

**Train 2 — input**
```text
00000000
00000600
00000000
00000000
00000000
00400000
00000000
00000000
```
**Train 2 — output**
```text
00000600
00006660
00000600
00000000
00400000
04440000
00400000
00000000
```

**Train 3 — input**
```text
000000000
030000000
000000000
000000800
000000000
000000000
```
**Train 3 — output**
```text
030000000
333000000
030000800
000008880
000000800
000000000
```

**Train 4 — input**
```text
000000
000000
000200
000000
000000
000000
090000
000000
000000
```
**Train 4 — output**
```text
000000
000200
002220
000200
000000
090000
999000
090000
000000
```

**Test — input**
```text
000000000
000000070
006000000
000000000
000000000
000000400
000000000
000000000
```
**Test — output**
```text
000000070
006000777
066600070
006000000
000000400
000004440
000000400
000000000
```
**Written solution**

Every nonzero seed cell grows into a plus: keep the center and add the four cardinal neighbors in the same color, clipped by the grid edges.

**Reference program**
```python
def rule_e85(g):
    h,w=size(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    painted=sprout_kernel(seeds, [(0,0),(-1,0),(1,0),(0,-1),(0,1)])
    out=blank(h,w)
    for (r,c),v in painted.items():
        if 0<=r<h and 0<=c<w:
            out[r][c]=v
    return out
```

## E86 — Bridge Matching Endpoints

**Difficulty:** easy

**Train pairs:** 4

**Skills:** line completion, pair matching, row/column reasoning

**Suggested staged path:** Find colors that appear exactly twice. If the pair is aligned, fill the straight path between them.


**Train 1 — input**
```text
000000000
020000200
000000060
000000000
000000000
000000060
000000000
```
**Train 1 — output**
```text
000000000
022222200
000000060
000000060
000000060
000000060
000000000
```

**Train 2 — input**
```text
00000000
00000000
05000000
00000000
00070070
00000000
05000000
00000000
```
**Train 2 — output**
```text
00000000
00000000
05000000
05000000
05077770
05000000
05000000
00000000
```

**Train 3 — input**
```text
0030000000
0000000000
0000000000
0000000000
0030000000
0000080080
```
**Train 3 — output**
```text
0030000000
0030000000
0030000000
0030000000
0030000000
0000088880
```

**Train 4 — input**
```text
0000000
9009000
0000400
0000000
0000000
0000000
0000000
0000400
0000000
```
**Train 4 — output**
```text
0000000
9999000
0000400
0000400
0000400
0000400
0000400
0000400
0000000
```

**Test — input**
```text
0000500000
0000000000
0000000000
0700000070
0000000000
0000000000
0000500000
0000000000
```
**Test — output**
```text
0000500000
0000500000
0000500000
0777777770
0000500000
0000500000
0000500000
0000000000
```
**Written solution**

Each color forms exactly one aligned pair. Fill the full horizontal or vertical segment between the two endpoints, inclusive.

**Reference program**
```python
def rule_e86(g):
    h,w=size(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    out=blank(h,w)
    for color,cells in pos.items():
        if len(cells)!=2:
            # preserve weird cases
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            for c in range(min(c1,c2), max(c1,c2)+1):
                out[r1][c]=color
        elif c1==c2:
            for r in range(min(r1,r2), max(r1,r2)+1):
                out[r][c1]=color
        else:
            # preserve
            out[r1][c1]=color
            out[r2][c2]=color
    return out
```

## E87 — Diagonal Corners to Outline

**Difficulty:** easy

**Train pairs:** 4

**Skills:** rectangle inference, outline drawing, group by color

**Suggested staged path:** Each color gives two diagonal corners. Recover the rectangle they imply, then draw just the border.


**Train 1 — input**
```text
000000000
020000000
000000600
000000000
000000006
000020000
000000000
000000000
```
**Train 1 — output**
```text
000000000
022220000
020020666
020020606
020020666
022220000
000000000
000000000
```

**Train 2 — input**
```text
000005000
000000000
000000000
000000005
070000000
000000000
000000000
000000000
000070000
```
**Train 2 — output**
```text
000005555
000005005
000005005
000005555
077770000
070070000
070070000
070070000
077770000
```

**Train 3 — input**
```text
0000000080
0030000000
0000000008
0000000000
0000000000
0000003000
0000000000
```
**Train 3 — output**
```text
0000000088
0033333088
0030003088
0030003000
0030003000
0033333000
0000000000
```

**Train 4 — input**
```text
00000000
00000000
40000000
00000000
00000000
00000900
00040000
00000000
00000009
00000000
```
**Train 4 — output**
```text
00000000
00000000
44440000
40040000
40040000
40040999
44440909
00000909
00000999
00000000
```

**Test — input**
```text
0000000000
0200000000
0000000000
0000000700
0000000000
0000000000
0000020000
0000000000
0000000007
```
**Test — output**
```text
0000000000
0222220000
0200020000
0200020777
0200020707
0200020707
0222220707
0000000707
0000000777
```
**Written solution**

For each color, interpret the two cells as opposite corners of an axis-aligned rectangle and draw that rectangle’s outline.

**Reference program**
```python
def rule_e87(g):
    h,w=size(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    out=blank(h,w)
    for color,cells in pos.items():
        if len(cells)!=2:
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        r0,r1s=sorted((r1,r2))
        c0,c1s=sorted((c1,c2))
        for c in range(c0,c1s+1):
            out[r0][c]=color
            out[r1s][c]=color
        for r in range(r0,r1s+1):
            out[r][c0]=color
            out[r][c1s]=color
    return out
```

## E88 — Mirror Across the Guide

**Difficulty:** easy

**Train pairs:** 4

**Skills:** reflection, guide detection, same-size

**Suggested staged path:** First find the full guide line of 8s. Then copy every colored cell to the symmetric location across that line.


**Train 1 — input**
```text
000080000
005080000
005580000
000080000
000080000
000080000
000080000
```
**Train 1 — output**
```text
000080000
005080500
005585500
000080000
000080000
000080000
000080000
```

**Train 2 — input**
```text
00000000
06600000
00600000
00600000
88888888
00000000
00000000
00000000
00000000
```
**Train 2 — output**
```text
00000000
06600000
00600000
00600000
88888888
00600000
00600000
06600000
00000000
```

**Train 3 — input**
```text
0000008000
0000008000
0000008000
0000008000
0070008000
0077008000
0007008000
0000008000
```
**Train 3 — output**
```text
0000008000
0000008000
0000008000
0000008000
0070008000
0077008007
0007008007
0000008000
```

**Train 4 — input**
```text
000000000
000000000
000003000
000033300
000000000
000000000
888888888
000000000
000000000
000000000
```
**Train 4 — output**
```text
000000000
000000000
000003000
000033300
000000000
000000000
888888888
000000000
000000000
000033300
```

**Test — input**
```text
00000800000
00000800000
00400800000
00440800000
00040800000
00000800000
00000800000
00000800000
00000800000
```
**Test — output**
```text
00000800000
00000800000
00400800400
00440804400
00040804000
00000800000
00000800000
00000800000
00000800000
```
**Written solution**

The all-8 row or column is a mirror. Keep the original shape and add its reflected copy across the guide.

**Reference program**
```python
def rule_e88(g):
    h,w=size(g)
    # find full guide line of 8
    guide_row = next((r for r in range(h) if all(v==8 for v in g[r])), None)
    guide_col = next((c for c in range(w) if all(g[r][c]==8 for r in range(h))), None)
    out=clone(g)
    if guide_row is not None:
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                if v!=0 and v!=8:
                    rr=2*guide_row-r
                    if 0<=rr<h:
                        out[rr][c]=v
    elif guide_col is not None:
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                if v!=0 and v!=8:
                    cc=2*guide_col-c
                    if 0<=cc<w:
                        out[r][cc]=v
    return out
```

## E89 — Count and Sort Colors

**Difficulty:** easy

**Train pairs:** 4

**Skills:** counting, sorting, dynamic-width output

**Suggested staged path:** Ignore position and just count how often each color appears. The output is a single row in ascending color order.


**Train 1 — input**
```text
400000
000020
004000
000000
000003
```
**Train 1 — output**
```text
2344
```

**Train 2 — input**
```text
0000005
0000000
0200000
0000500
0000003
2000000
```
**Train 2 — output**
```text
22355
```

**Train 3 — input**
```text
0000000
0600040
0000000
0004000
0000000
0060000
0000002
```
**Train 3 — output**
```text
24466
```

**Train 4 — input**
```text
00000003
00000000
00700700
00000000
30005000
```
**Train 4 — output**
```text
33577
```

**Test — input**
```text
04000000
00000020
00040000
50000000
00000002
00005000
```
**Test — output**
```text
224455
```
**Written solution**

Count every nonzero color, then output one row containing each color repeated by its count, sorted from smallest color number to largest.

**Reference program**
```python
def rule_e89(g):
    counts=defaultdict(int)
    for row in g:
        for v in row:
            if v!=0:
                counts[v]+=1
    out=[]
    for color in sorted(counts):
        out.extend([color]*counts[color])
    return [out] if out else [[0]]
```

## E90 — Seed to 3x3 Frame

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local geometry, outline generation, same-size

**Suggested staged path:** Around each seed, think of the surrounding 3×3 box. Paint only its border, not the center.


**Train 1 — input**
```text
0000000
0000000
0050000
0000000
0000070
0000000
0000000
```
**Train 1 — output**
```text
0000000
0555000
0505000
0555777
0000707
0000777
0000000
```

**Train 2 — input**
```text
000000000
000000300
000000000
000000000
000000000
008000000
000000000
000000000
```
**Train 2 — output**
```text
000003330
000003030
000003330
000000000
088800000
080800000
088800000
000000000
```

**Train 3 — input**
```text
00000000
02000000
00000000
00006000
00000000
00000000
```
**Train 3 — output**
```text
22200000
20200000
22266600
00060600
00066600
00000000
```

**Train 4 — input**
```text
000000
000000
000900
000000
000000
000000
040000
000000
000000
```
**Train 4 — output**
```text
000000
009990
009090
009990
000000
444000
404000
444000
000000
```

**Test — input**
```text
00000000
00000000
00600000
00000000
00000000
00000300
00000000
00000000
```
**Test — output**
```text
00000000
06660000
06060000
06660000
00003330
00003030
00003330
00000000
```
**Written solution**

Every seed becomes the outline of a 3×3 square centered on that seed, using the seed’s color and clipping at the edges.

**Reference program**
```python
def rule_e90(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if abs(dr)==1 or abs(dc)==1:
                            nr,nc=r+dr,c+dc
                            if 0<=nr<h and 0<=nc<w:
                                out[nr][nc]=v
    return out
```

## E91 — One-Step Shift

**Difficulty:** easy

**Train pairs:** 4

**Skills:** direction token, rigid motion, same-size

**Suggested staged path:** Read the arrow cell first. Then move the whole non-arrow shape by exactly one step in that direction.


**Train 1 — input**
```text
200000000
000000000
000000000
005500000
005000000
000000000
000000000
000000000
```
**Train 1 — output**
```text
000000000
000000000
000000000
000550000
000500000
000000000
000000000
000000000
```

**Train 2 — input**
```text
00000000
00000000
00000000
00000000
00000000
00060000
00666000
00000000
00000001
```
**Train 2 — output**
```text
00000000
00000000
00000000
00000000
00060000
00666000
00000000
00000000
00000000
```

**Train 3 — input**
```text
0000000003
0000070000
0000077000
0000000000
0000000000
0000000000
0000000000
```
**Train 3 — output**
```text
0000000000
0000000000
0000070000
0000077000
0000000000
0000000000
0000000000
```

**Train 4 — input**
```text
0000000
0000000
0000000
0000000
0000800
0000880
0000080
0000000
0000000
4000000
```
**Train 4 — output**
```text
0000000
0000000
0000000
0000000
0008000
0008800
0000800
0000000
0000000
0000000
```

**Test — input**
```text
2000000000
0000000000
0004000000
0004400000
0000400000
0000000000
0000000000
0000000000
```
**Test — output**
```text
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
```
**Written solution**

Ignore the arrow in the output and shift the entire colored component by one cell in the arrow’s direction.

**Reference program**
```python
def rule_e91(g):
    h,w=size(g)
    arrow=None
    cells=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in DIRMAP:
                arrow=(r,c,v)
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w)
    if arrow is None:
        return clone(g)
    dr,dc=DIRMAP[arrow[2]]
    for r,c,v in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out
```

## M85 — Token-Specific Kernels in Frames

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame localization, seed expansion, symbol-conditioned rule

**Suggested staged path:** Work frame by frame. Inside each frame, find the seed color and the token that selects which local kernel to paint.


**Train 1 — input**
```text
0000000000000
0111110011110
0120010010410
0106010015010
0100010010010
0111110011110
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```
**Train 1 — output**
```text
0000000000000
0111110011110
0106010015510
0166610015510
0106010015510
0111110011110
0000000000000
0000000000000
0000000000000
0000000000000
0000000000000
```

**Train 2 — input**
```text
00000000000000
00111110000000
00130010011110
00107010010010
00100010010210
00100010018010
00111110010010
00000000011110
00000000000000
00000000000000
```
**Train 2 — output**
```text
00000000000000
00111110000000
00170710011110
00107010010010
00170710018010
00100010018810
00111110018010
00000000011110
00000000000000
00000000000000
```

**Train 3 — input**
```text
000000000000000
011111000111110
010041000100010
010001000106010
010501000130010
010001000100010
011111000111110
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 3 — output**
```text
000000000000000
011111000111110
010001000160610
015551000106010
015551000160610
015551000100010
011111000111110
000000000000000
000000000000000
000000000000000
000000000000000
000000000000000
```

**Train 4 — input**
```text
00000000000000
00000000000000
01111100111110
01200100100010
01080100100410
01000100107010
01000100100010
01111100100010
00000000111110
00000000000000
00000000000000
```
**Train 4 — output**
```text
00000000000000
00000000000000
01111100111110
01080100100010
01888100177710
01080100177710
01000100177710
01111100100010
00000000111110
00000000000000
00000000000000
```

**Test — input**
```text
000000000000000
001111100000000
001200100111110
001000100100010
001060100130010
001000100105010
001111100100010
000000000100010
000000000111110
000000000000000
000000000000000
000000000000000
```
**Test — output**
```text
000000000000000
001111100000000
001000100111110
001060100100010
001666100150510
001060100105010
001111100150510
000000000100010
000000000111110
000000000000000
000000000000000
000000000000000
```
**Written solution**

Each border-1 frame contains one seed and one token. The token chooses a kernel shape—plus, X, or full 3×3—and that kernel is painted in the seed color, clipped to the frame interior.

**Reference program**
```python
def rule_m85(g):
    h,w=size(g)
    out=blank(h,w)
    # preserve frames
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==1:
                out[r][c]=1
    frames=find_rectangular_frames(g, color=1)
    for r0,c0,r1,c1 in frames:
        interior={(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)}
        seed=None
        token=None
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v in KERNELS_M85:
                    token=v
                elif v!=0:
                    seed=(r,c,v)
        if seed and token:
            painted=sprout_kernel([seed], KERNELS_M85[token], allowed=interior)
            for (r,c),v in painted.items():
                out[r][c]=v
    return out
```

## M86 — Ordered Normalized Pack

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component extraction, token ordering, packing

**Suggested staged path:** Ignore location first and crop each component to its own tight box. Then sort those crops by the nearby order token.


**Train 1 — input**
```text
000000000000000
000000000003000
000000200007700
000000500000770
010000555000000
060600000000000
066600000000000
000000000000000
000000000000000
```
**Train 1 — output**
```text
60605000770
66605550077
```

**Train 2 — input**
```text
0000000000000000
0000000000000000
0010000000000000
0055000000030000
0050000000080000
0050000200088000
0000000666088800
0000000060000000
0000000000000000
0000000000000000
```
**Train 2 — output**
```text
5506660800
5000600880
5000000888
```

**Train 3 — input**
```text
00000000000000000
00000002000000000
00000000770030000
00000007700055500
01000000000050500
08000000000055500
00800000000000000
00080000000000000
00000000000000000
```
**Train 3 — output**
```text
8080800770555
0000007700505
0000000000555
```

**Train 4 — input**
```text
000000000000000
001000000000000
006000000000000
006600200000000
006660550030000
000000500070700
000000500077700
000000000000000
000000000000000
000000000000000
```
**Train 4 — output**
```text
6000550707
6600500777
6660500000
```

**Test — input**
```text
0000000000000000
0000000000000000
0010000000000000
0005000000030000
0055500000080000
0005000200088800
0000000066000000
0000000660000000
0000000000000000
0000000000000000
```
**Test — output**
```text
05000660800
55506600888
05000000000
```
**Written solution**

Every component has an order token placed one row above its top-left corner. Crop each component to its minimal box, sort by token value, and pack the crops left to right with one empty column between them.

**Reference program**
```python
def rule_m86(g):
    comps=[(v,cells) for v,cells in components4(g) if v not in (1,2,3,4)]
    ordered=[]
    for color,cells in comps:
        r0,c0,r1,c1=bbox(cells)
        order=None
        if r0-1 >= 0 and g[r0-1][c0] in (1,2,3,4):
            order=g[r0-1][c0]
        else:
            # fallback nearest token
            best=None
            for rr,row in enumerate(g):
                for cc,v in enumerate(row):
                    if v in (1,2,3,4):
                        d=min(abs(rr-r)+abs(cc-c) for r,c in cells)
                        if best is None or d<best[0]:
                            best=(d,v)
            order=best[1]
        crop=crop_bbox(g,cells)
        ordered.append((order,crop))
    ordered.sort(key=lambda x:x[0])
    height=max(len(c) for _,c in ordered)
    width=sum(len(c[0]) for _,c in ordered) + (len(ordered)-1)
    out=blank(height,width)
    curc=0
    for _,crop in ordered:
        ch,cw=size(crop)
        for r in range(ch):
            for c in range(cw):
                out[r][curc+c]=crop[r][c]
        curc += cw + 1
    return out
```

## M87 — Corner-Marker Stripe Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame reasoning, interior fill, alternating pattern

**Suggested staged path:** Inside each frame, read the two marker colors at the top corners. Then extend them as alternating vertical stripes.


**Train 1 — input**
```text
00000000000000
01111110000000
01500610111110
01000010120710
01000010100010
01111110100010
00000000100010
00000000100010
00000000111110
00000000000000
```
**Train 1 — output**
```text
00000000000000
01111110000000
01565610111110
01565610127210
01565610127210
01111110127210
00000000127210
00000000127210
00000000111110
00000000000000
```

**Train 2 — input**
```text
000000000000000
001111110000000
001300810000000
001000010011110
001000010016410
001000010010010
001111110010010
000000000010010
000000000010010
000000000011110
000000000000000
```
**Train 2 — output**
```text
000000000000000
001111110000000
001383810000000
001383810011110
001383810016410
001383810016410
001111110016410
000000000016410
000000000016410
000000000011110
000000000000000
```

**Train 3 — input**
```text
0000000000000000
0000000001111110
0111110001500310
0170210001000010
0100010001000010
0100010001000010
0100010001111110
0100010000000000
0111110000000000
0000000000000000
0000000000000000
0000000000000000
```
**Train 3 — output**
```text
0000000000000000
0000000001111110
0111110001535310
0172710001535310
0172710001535310
0172710001535310
0172710001111110
0172710000000000
0111110000000000
0000000000000000
0000000000000000
0000000000000000
```

**Train 4 — input**
```text
000000000000000
011111100000000
018004100111110
010000100160210
010000100100010
010000100100010
011111100100010
000000000100010
000000000111110
000000000000000
```
**Train 4 — output**
```text
000000000000000
011111100000000
018484100111110
018484100162610
018484100162610
018484100162610
011111100162610
000000000162610
000000000111110
000000000000000
```

**Test — input**
```text
0000000000000000
0011111100000000
0017005100111110
0010000100130810
0010000100100010
0010000100100010
0010000100100010
0011111100100010
0000000000100010
0000000000111110
0000000000000000
```
**Test — output**
```text
0000000000000000
0011111100000000
0017575100111110
0017575100138310
0017575100138310
0017575100138310
0017575100138310
0011111100138310
0000000000138310
0000000000111110
0000000000000000
```
**Written solution**

For each border-1 frame, the two cells just inside the top corners specify two colors. Fill the frame interior with alternating vertical stripes starting with the left marker color.

**Reference program**
```python
def rule_m87(g):
    out=blank(*size(g))
    h,w=size(g)
    # preserve frames
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==1:
                out[r][c]=1
    for r0,c0,r1,c1 in find_rectangular_frames(g,1):
        a=g[r0+1][c0+1]
        b=g[r0+1][c1-1]
        for c in range(c0+1,c1):
            color=a if ((c-(c0+1))%2==0) else b
            for r in range(r0+1,r1):
                out[r][c]=color
    return out
```

## M88 — Crop and Rotate by Token

**Difficulty:** medium

**Train pairs:** 4

**Skills:** cropping, rotation, symbol decoding

**Suggested staged path:** Separate the token from the actual motif. Crop the motif tightly, then rotate it according to the token.


**Train 1 — input**
```text
20000000
00000000
00000000
00560000
00060000
00077000
00000000
00000000
```
**Train 1 — output**
```text
005
766
700
```

**Train 2 — input**
```text
000000000
000000000
000506000
000556000
000007000
000000000
000000000
000000000
000000003
```
**Train 2 — output**
```text
700
655
605
```

**Train 3 — input**
```text
0000000004
0000000000
0000000000
0000670000
0000075000
0000005000
0000000000
0000000000
```
**Train 3 — output**
```text
600
770
055
```

**Train 4 — input**
```text
00000000
00000000
00500000
00565000
00077000
00000000
00000000
00000000
10000000
```
**Train 4 — output**
```text
500
565
077
```

**Test — input**
```text
2000000000
0000000000
0000000000
0000570000
0000650000
0000550000
0000000000
0000000000
0000000000
```
**Test — output**
```text
565
557
```
**Written solution**

Ignore the token cell when finding the motif. Crop the motif to its bounding box and rotate it: 1 means none, 2 means 90°, 3 means 180°, and 4 means 270°.

**Reference program**
```python
def rule_m88(g):
    token=1
    cells=[]
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (1,2,3,4):
                token=v
            elif v!=0:
                cells.append((r,c))
    crop=crop_bbox(g,cells)
    return transform_grid(crop, token)
```

## M89 — Area-Rank Recoloring

**Difficulty:** medium

**Train pairs:** 4

**Skills:** component area, ranking, recolor

**Suggested staged path:** Do not care about original colors. Measure component sizes first, then replace colors by size rank.


**Train 1 — input**
```text
000000000000
055000666000
055000066000
000000000000
000000000000
000000000000
000000007700
000000007000
000000000000
000000000000
```
**Train 1 — output**
```text
000000000000
033000444000
033000044000
000000000000
000000000000
000000000000
000000002200
000000002000
000000000000
000000000000
```

**Train 2 — input**
```text
0000000000000
0000000000000
0050000066000
0050000066000
0050000000000
0000000000000
0000000000000
0000000077700
0000000007700
0000000000000
0000000000000
```
**Train 2 — output**
```text
0000000000000
0000000000000
0020000033000
0020000033000
0020000000000
0000000000000
0000000000000
0000000044400
0000000004400
0000000000000
0000000000000
```

**Train 3 — input**
```text
00000000000000
00800000000000
00800000000000
00800000000000
00000000666000
05550000066000
00050000000000
00000000000000
00000000000000
00000000000000
```
**Train 3 — output**
```text
00000000000000
00200000000000
00200000000000
00200000000000
00000000444000
03330000044000
00030000000000
00000000000000
00000000000000
00000000000000
```

**Train 4 — input**
```text
000000000000
000000006600
007700006600
007000000000
000000000000
000000000000
000000055500
000000005500
000000000000
000000000000
000000000000
000000000000
```
**Train 4 — output**
```text
000000000000
000000003300
002200003300
002000000000
000000000000
000000000000
000000044400
000000004400
000000000000
000000000000
000000000000
000000000000
```

**Test — input**
```text
0000000000000
0000000000000
0800000000000
0800000000000
0800000066600
0000000066000
0005500000000
0005500000000
0000000000000
0000000000000
0000000000000
```
**Test — output**
```text
0000000000000
0000000000000
0200000000000
0200000000000
0200000044400
0000000044000
0003300000000
0003300000000
0000000000000
0000000000000
0000000000000
```
**Written solution**

Find the separate components, sort them by area from smallest to largest, and recolor them with 2, 3, 4 in that order while keeping the shapes in place.

**Reference program**
```python
def rule_m89(g):
    comps=[(v,cells) for v,cells in components4(g) if v!=0]
    comps_sorted=sorted(comps, key=lambda vc: len(vc[1]))
    rank_color={}
    for i,(v,cells) in enumerate(comps_sorted, start=2):
        rank_color[id(cells)]=i  # can't key by cells? use list id
    out=blank(*size(g))
    for i,(v,cells) in enumerate(comps_sorted, start=2):
        for r,c in cells:
            out[r][c]=i
    return out
```

## M90 — Fill Chambers from Seeds

**Difficulty:** medium

**Train pairs:** 4

**Skills:** flood fill, wall constraints, region ownership

**Suggested staged path:** Treat the 1-cells as walls. Each chamber with exactly one seed should be flood-filled in the seed’s color.


**Train 1 — input**
```text
11111111111
10000100001
10500100601
10000100001
10000111111
10000100001
10000100701
10000100001
11111111111
```
**Train 1 — output**
```text
11111111111
15555166661
15555166661
15555166661
15555111111
15555177771
15555177771
15555177771
11111111111
```

**Train 2 — input**
```text
111111111111
100010001001
103010501001
100010001001
100010001001
100011111001
100010001001
100010001071
100010001001
111111111111
```
**Train 2 — output**
```text
111111111111
133315551771
133315551771
133315551771
133315551771
133311111771
133310001771
133310001771
133310001771
111111111111
```

**Train 3 — input**
```text
11111111111
10000000001
10600000401
10000000001
10000000001
11111111111
10000100001
10000100001
10000100901
10000100001
11111111111
```
**Train 3 — output**
```text
11111111111
10000000001
10600000401
10000000001
10000000001
11111111111
10000199991
10000199991
10000199991
10000199991
11111111111
```

**Train 4 — input**
```text
1111111111111
1050001000001
1000001000001
1000001111111
1000001000001
1000001000001
1080001004001
1000001000001
1111111111111
```
**Train 4 — output**
```text
1111111111111
1050001000001
1000001000001
1000001111111
1000001444441
1000001444441
1080001444441
1000001444441
1111111111111
```

**Test — input**
```text
1111111111111
1000001000001
1030001007001
1000001000001
1000001000001
1000001111111
1000001000001
1000001005001
1000001000001
1111111111111
```
**Test — output**
```text
1111111111111
1333331777771
1333331777771
1333331777771
1333331777771
1333331111111
1333331555551
1333331555551
1333331555551
1111111111111
```
**Written solution**

The walls split the board into chambers. Any chamber that contains one seed gets filled completely with that seed’s color, while the walls remain unchanged.

**Reference program**
```python
def rule_m90(g):
    h,w=size(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and (r,c) not in seen:
                region=flood_region(g,(r,c),blocked={1})
                seen.update(region)
                colors={g[rr][cc] for rr,cc in region if g[rr][cc]!=0}
                if len(colors)==1:
                    color=next(iter(colors))
                    for rr,cc in region:
                        if g[rr][cc]!=1:
                            out[rr][cc]=color
    return out
```

## M91 — Stamp the Mask at Anchors

**Difficulty:** medium

**Train pairs:** 4

**Skills:** mask extraction, translation, recoloring

**Suggested staged path:** First isolate the 5-mask and normalize it to its top-left corner. Then stamp that shape at every anchor cell in the anchor’s color.


**Train 1 — input**
```text
00000000000000
05500000020000
00550000000000
00000000000000
00000000000000
00000003000000
00000000000000
00000000000000
00000000000000
00000000000000
```
**Train 1 — output**
```text
00000000000000
00000000022000
00000000002200
00000000000000
00000000000000
00000003300000
00000000330000
00000000000000
00000000000000
00000000000000
```

**Train 2 — input**
```text
000000000000000
000000000040000
005550000000000
000500000000000
000000000000000
000000000000000
000000006000000
000000000000000
000000000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
000000000000000
000000000044400
000000000004000
000000000000000
000000000000000
000000000000000
000000006660000
000000000600000
000000000000000
000000000000000
000000000000000
```

**Train 3 — input**
```text
0000000000000
0550000000000
0500000070000
0000000000000
0000000000000
0000000003000
0000020000000
0000000000000
0000000000000
```
**Train 3 — output**
```text
0000000000000
0000000000000
0000000077000
0000000070000
0000000000000
0000000003300
0000022003000
0000020000000
0000000000000
```

**Train 4 — input**
```text
0000000000000000
0000000000080000
0505000000000000
0555000000000000
0000000000000000
0000000000000000
0000000000400000
0000000000000000
0000000000000000
0000000000000000
```
**Train 4 — output**
```text
0000000000000000
0000000000080800
0000000000088800
0000000000000000
0000000000000000
0000000000000000
0000000000404000
0000000000444000
0000000000000000
0000000000000000
```

**Test — input**
```text
000000000000000
055000000000000
005500000200000
000000000000000
000000000000000
000000000000000
000000000060000
000030000000000
000000000000000
000000000000000
000000000000000
```
**Test — output**
```text
000000000000000
000000000000000
000000000220000
000000000022000
000000000000000
000000000000000
000000000066000
000033000006600
000003300000000
000000000000000
000000000000000
```
**Written solution**

Extract the pattern made by the 5-cells, normalize it, remove it, and stamp that same pattern at each nonzero anchor using the anchor’s color and position as the top-left origin.

**Reference program**
```python
def rule_m91(g):
    h,w=size(g)
    mask_cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    if not mask_cells:
        return blank(h,w)
    norm=normalize_cells(mask_cells)
    # exclude original mask and anchors from output
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,5):
                for dr,dc in norm:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out
```

## H85 — Priority Sprouts

**Difficulty:** hard

**Train pairs:** 4

**Skills:** conflict resolution, kernel expansion, legend priority

**Suggested staged path:** Ignore overlaps at first: every seed sprouts a plus. Then resolve conflicts using the priority strip from left to right.


**Train 1 — input**
```text
604050000
000000000
000000000
005040000
000000000
000600000
000000000
000000000
```
**Train 1 — output**
```text
000000000
005040000
055444000
005640000
006660000
000600000
000000000
```

**Train 2 — input**
```text
7050300000
0000000000
0030000000
0000000000
0000507000
0000000000
0000030000
0000000000
0000000000
```
**Train 2 — output**
```text
0030000000
0333000000
0030507000
0005577700
0000537000
0000333000
0000030000
0000000000
```

**Train 3 — input**
```text
806040000
000000000
000000000
004060800
000000000
000000000
000040000
000000000
000000000
000000000
```
**Train 3 — output**
```text
000000000
004060800
044668880
004060800
000040000
000444000
000040000
000000000
000000000
```

**Train 4 — input**
```text
50702000000
00000000000
00000000000
00020000000
00000700000
00000000000
00005020000
00000000000
00000000000
```
**Train 4 — output**
```text
00000000000
00020000000
00222700000
00027770000
00005720000
00055522000
00005020000
00000000000
```

**Test — input**
```text
6030800000
0000000000
0000000000
0080000000
0000300000
0000006000
0000000000
0000800000
0000000000
0000000000
```
**Test — output**
```text
0000000000
0080000000
0888300000
0083336000
0000366600
0000806000
0008880000
0000800000
0000000000
```
**Written solution**

The top row gives a priority ordering of colors. In the body, each seed grows a plus of radius 1, and whenever two sprouts compete for the same cell, the higher-priority color wins. The output drops the priority row.

**Reference program**
```python
def rule_h85(g):
    h,w=size(g)
    priority_colors=[v for v in g[0] if v!=0]
    priority={color:i for i,color in enumerate(priority_colors)}
    seeds=[(r-1,c,v) for r in range(1,h) for c,v in enumerate(g[r]) if v!=0]  # output coordinates shift up by 1
    painted=sprout_kernel(seeds, [(0,0),(-1,0),(1,0),(0,-1),(0,1)], priority=priority)
    out=blank(h-1,w)
    for (r,c),v in painted.items():
        if 0<=r<h-1 and 0<=c<w:
            out[r][c]=v
    return out
```

## H86 — A:B::C Transform Analogy

**Difficulty:** hard

**Train pairs:** 4

**Skills:** analogy, transform inference, cropping

**Suggested staged path:** Do not use the bottom motif first. Infer the transformation from A to B, then apply exactly that transformation to C.


**Train 1 — input**
```text
111110001111100
156010001005100
106010001766100
107710001700100
111110001111100
000000000000000
000000000000000
111110000000000
150010000000000
155010000000000
165010000000000
111110000000000
000000000000000
```
**Train 1 — output**
```text
655
550
```

**Train 2 — input**
```text
0111110000111110
0150610000170010
0155610000165510
0100710000160510
0100010000100010
0111110000111110
0000000000000000
0111110000000000
0167010000000000
0107510000000000
0100510000000000
0111110000000000
0000000000000000
```
**Train 2 — output**
```text
500
570
076
```

**Train 3 — input**
```text
111110001111100
150010001005100
156510001565100
107710001770100
111110001111100
000000000000000
000000000000000
111110000000000
157010000000000
165010000000000
155010000000000
111110000000000
000000000000000
```
**Train 3 — output**
```text
75
56
55
```

**Train 4 — input**
```text
0111110000111110
0167010000160010
0107510000177010
0100510000105510
0100010000100010
0111110000111110
0000000000000000
0000000000000000
0111110000000000
0156010000000000
0106010000000000
0107710000000000
0111110000000000
0000000000000000
```
**Train 4 — output**
```text
500
667
007
```

**Test — input**
```text
111110001111100
157010001565100
165010001557100
155010001000100
111110001111100
000000000000000
000000000000000
111110000000000
150610000000000
155610000000000
100710000000000
111110000000000
000000000000000
```
**Test — output**
```text
055
050
766
```
**Written solution**

The top pair demonstrates a transformation such as rotation or reflection. Infer that transform from A→B, crop C tightly, and output the transformed version of C.

**Reference program**
```python
def rule_h86(g):
    frames=find_rectangular_frames(g,1)
    # sort by top-left
    frames=sorted(frames)
    if len(frames)<3:
        return [[0]]
    A_box,B_box,C_box=frames[:3]
    A=crop_nonzero(extract_box_interior(g,A_box))
    B=crop_nonzero(extract_box_interior(g,B_box))
    C=crop_nonzero(extract_box_interior(g,C_box))
    tid=infer_transform(A,B)
    return apply_transform_by_id(C, tid)
```

## H87 — Palette-Depth Nested Frames

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nesting depth, palette mapping, frame detection

**Suggested staged path:** First identify the nested frame layers in the body. Then map outermost to innermost layers onto the palette order from the top strip.


**Train 1 — input**
```text
23400000000
11111111111
10000000001
10111111101
10100000101
10101110101
10101010101
10101110101
10100000101
10111111101
10000000001
11111111111
```
**Train 1 — output**
```text
22222222222
20000000002
20333333302
20300000302
20304440302
20304040302
20304440302
20300000302
20333333302
20000000002
22222222222
```

**Train 2 — input**
```text
572300000000000
111111111111111
100000000000001
101111111111101
101000000000101
101011111110101
101010000010101
101010111010101
101010101010101
101010111010101
101010000010101
101011111110101
101000000000101
101111111111101
100000000000001
111111111111111
```
**Train 2 — output**
```text
555555555555555
500000000000005
507777777777705
507000000000705
507022222220705
507020000020705
507020333020705
507020303020705
507020333020705
507020000020705
507022222220705
507000000000705
507777777777705
500000000000005
555555555555555
```

**Train 3 — input**
```text
846000000000
111111111111
100000000001
101111111101
101000000101
101011110101
101010010101
101010010101
101011110101
101000000101
101111111101
100000000001
111111111111
```
**Train 3 — output**
```text
888888888888
800000000008
804444444408
804000000408
804066660408
804060060408
804060060408
804066660408
804000000408
804444444408
800000000008
888888888888
```

**Train 4 — input**
```text
3570000000
1111111111
1000000001
1011111101
1010000101
1011111101
1011001101
1011001101
1011001101
1011001101
1011111101
1010000101
1011111101
1000000001
1111111111
```
**Train 4 — output**
```text
3333333333
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3000000003
3333333333
```

**Test — input**
```text
46800000000
11111111111
10000000001
10111111101
10100000101
10111111101
10110001101
10110001101
10110001101
10111111101
10100000101
10111111101
10000000001
11111111111
```
**Test — output**
```text
44444444444
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
40000000004
44444444444
```
**Written solution**

The top strip lists colors in depth order. Recolor the nested border-1 frames from outermost to innermost using that palette, and output only the body.

**Reference program**
```python
def rule_h87(g):
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    frames=find_rectangular_frames(body,1)
    # outer to inner by area descending or by bbox
    frames=sorted(frames, key=lambda b: ((b[2]-b[0]+1)*(b[3]-b[1]+1)), reverse=True)
    out=blank(*size(body))
    for idx,box in enumerate(frames):
        color=palette[idx] if idx < len(palette) else palette[-1]
        r0,c0,r1,c1=box
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out
```

## H88 — Rotate, Crop, and Pack the Boxes

**Difficulty:** hard

**Train pairs:** 4

**Skills:** box parsing, tokened transforms, packing

**Suggested staged path:** Solve each box independently first: token → rotate → crop. Only after that should you pack the results left to right.


**Train 1 — input**
```text
000000000000000000000
020000000300000090000
011111000111110011110
010001000100010010010
015601000170010015510
010671000177010016510
010001000100010010010
011111000111110011110
000000000000000000000
```
**Train 1 — output**
```text
05077055
66007065
70000000
```

**Train 2 — input**
```text
00000000000000000000000
00000000000000000000000
04000000020000000900000
01111100011111000111110
01000100010001000100010
01506100015701000167010
01556100016501000107510
01007100015501000100510
01111100011111000111110
00000000000000000000000
```
**Train 2 — output**
```text
55005650670
05005570075
66700000005
```

**Train 3 — input**
```text
0000000000000000000000
0900000004000000030000
0111110001111100011110
0100010001000100010010
0150010001560100015510
0156510001060100016510
0107710001077100010010
0111110001111100011110
0000000000000000000000
```
**Train 3 — output**
```text
5000500056
5650667055
0770007000
```

**Train 4 — input**
```text
0000000000000000000000
0000000000000000000000
0200000009000000040000
0111110001111100011110
0100010001000100010010
0167010001560100015510
0107510001067100016510
0100510001000100010010
0111110001111100011110
0000000000000000000000
```
**Train 4 — output**
```text
0060560056
0770067055
5500000000
```

**Test — input**
```text
000000000000000000000
040000000200000090000
011111000111110011110
010001000100010010010
015701000150010015510
016501000156510016510
015501000107710010010
011111000111110011110
000000000000000000000
```
**Test — output**
```text
5650055055
7550760065
0000750000
```
**Written solution**

Each framed box has a transform token just above it. Crop the motif inside each box, apply that box’s rotation token (9 means none), then pack the transformed crops left to right with a one-column gap.

**Reference program**
```python
def rule_h88(g):
    frames=sorted(find_rectangular_frames(g,1), key=lambda b:(b[1],b[0]))
    pieces=[]
    for box in frames:
        r0,c0,r1,c1=box
        raw = g[r0-1][c0] if r0-1 >= 0 else 9
        token = TOKEN_MAP_H88.get(raw,1)
        interior=extract_box_interior(g,box)
        cells=[(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v!=0]
        crop=crop_from_cells(interior,cells)
        pieces.append(transform_grid(crop, token))
    height=max(len(p) for p in pieces)
    width=sum(len(p[0]) for p in pieces)+(len(pieces)-1)
    out=blank(height,width)
    cur=0
    for piece in pieces:
        ph,pw=size(piece)
        for r in range(ph):
            for c in range(pw):
                out[r][cur+c]=piece[r][c]
        cur += pw + 1
    return out
```

## H89 — Symmetry-Class Equality Matrix

**Difficulty:** hard

**Train pairs:** 4

**Skills:** symmetry classification, comparison matrix, shape analysis

**Suggested staged path:** Classify each motif first: horizontal-symmetric, vertical-symmetric, both, or neither. Then compare the classes pairwise.


**Train 1 — input**
```text
00000000000000000000000
00000000000000000000000
01111110011111100111111
01000010010000100100001
01005010010550100105501
01055510010055100105501
01005010010000100100001
01111110011111100111111
00000000000000000000000
```
**Train 1 — output**
```text
202
020
202
```

**Train 2 — input**
```text
00000000000000000000000
00000000000000000000000
01111110011111100111111
01000010010000100100001
01555010015500100100501
01050010015550100105551
01000010010000100100501
01111110011111100111111
00000000000000000000000
```
**Train 2 — output**
```text
200
020
002
```

**Train 3 — input**
```text
00000000000000000000000
00000000000000000000000
01111110011111100111111
01000010010000100100001
01055010015550100105551
01005510010500100105551
01000010010000100100001
01111110011111100111111
00000000000000000000000
```
**Train 3 — output**
```text
200
020
002
```

**Train 4 — input**
```text
00000000000000000000000
00000000000000000000000
01111110011111100111111
01000010010000100100001
01550010015500100155001
01555010010550100155501
01000010010000100100001
01111110011111100111111
00000000000000000000000
```
**Train 4 — output**
```text
222
222
222
```

**Test — input**
```text
00000000000000000000000
00000000000000000000000
01111110011111100111111
01000010010000100100001
01555010015500100105501
01050010015550100100551
01000010010000100100001
01111110011111100111111
00000000000000000000000
```
**Test — output**
```text
200
022
022
```
**Written solution**

The three framed motifs must be classified by symmetry. Output a 3×3 matrix with 2 wherever two motifs share the same symmetry class and 0 otherwise.

**Reference program**
```python
def rule_h89(g):
    frames=sorted(find_rectangular_frames(g,1), key=lambda b:(b[1],b[0]))
    classes=[]
    for box in frames:
        interior=extract_box_interior(g,box)
        crop=binary_crop_from_interior(interior)
        classes.append(symmetry_class(crop))
    n=len(classes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=2 if classes[i]==classes[j] else 0
    return out
```

## H90 — Route Pairs Around the Wall

**Difficulty:** hard

**Train pairs:** 4

**Skills:** path finding, obstacles, multi-object routing

**Suggested staged path:** Treat the 8-cells as blocked. For each color pair, find the shortest open route connecting the endpoints and paint that route.


**Train 1 — input**
```text
00000800000
02000800020
00000000000
00000800000
00000800000
00000800000
00000800000
00000800000
00000000000
03000800030
00000800000
```
**Train 1 — output**
```text
00000800000
02222800020
00002222220
00000800000
00000800000
00000800000
00000800000
00000800000
00003333330
03333800030
00000800000
```

**Train 2 — input**
```text
000000800000
002000800020
000000800000
000000000000
000000800000
000000800000
000000800000
000000000000
000000800000
004000800040
000000800000
```
**Train 2 — output**
```text
000000800000
002222800020
000002800020
000002222220
000000800000
000000800000
000000800000
000004444440
000004800040
004444800040
000000800000
```

**Train 3 — input**
```text
00000800000
00000000000
03000800030
00000800000
00000800000
00000800000
00000000000
00000800000
07000800070
00000800000
```
**Train 3 — output**
```text
00000800000
00003333330
03333800030
00000800000
00000800000
00000800000
00007777770
00007800070
07777800070
00000800000
```

**Train 4 — input**
```text
000000800000
020000800020
000000000000
000000800000
000000800000
000000800000
000000800000
000000800000
000000800000
000000000000
050000800050
000000800000
```
**Train 4 — output**
```text
000000800000
022222800020
000002222220
000000800000
000000800000
000000800000
000000800000
000000800000
000000800000
000005555550
055555800050
000000800000
```

**Test — input**
```text
00000800000
02000800020
00000800000
00000000000
00000800000
00000800000
00000800000
00000000000
00000800000
06000800060
00000800000
```
**Test — output**
```text
00000800000
02222800020
00002800020
00002222220
00000800000
00000800000
00000800000
00006666660
00006800060
06666800060
00000800000
```
**Written solution**

The matching colored terminals must be connected through empty cells while avoiding the 8-wall. Draw the shortest path for each pair, preserving walls and terminals.

**Reference program**
```python
def rule_h90(g):
    h,w=size(g)
    out=clone(g)
    pos=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v not in (0,8):
                pos[v].append((r,c))
    for color in sorted(pos):
        cells=pos[color]
        if len(cells)!=2:
            continue
        start,goal=cells
        blocked={(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v==8 or (v not in (0,color,8))}
        temp=blank(h,w)
        for r,c in blocked:
            temp[r][c]=8
        path=shortest_path(temp,start,goal,blocked={8},order=[(0,1),(1,0),(0,-1),(-1,0)])
        for r,c in path:
            out[r][c]=color
    return out
```

## H91 — Legend-Driven Transform Stamping

**Difficulty:** hard

**Train pairs:** 4

**Skills:** legend decoding, transform application, multi-target stamping

**Suggested staged path:** Learn the source motif once, then use the two-row legend to decide which transform belongs to each anchor color.


**Train 1 — input**
```text
90203000000000
20304000000000
00000005500000
00000000550000
00000000000000
00000000000000
02000000000000
00000000300000
00000000000000
00000000004000
00000000000000
00000000000000
```
**Train 1 — output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
02200000000000
00220000030000
00000000330000
00000000304400
00000000000440
00000000000000
```

**Train 2 — input**
```text
409020000000000
205070000000000
000000005550000
000000000500000
000000000000000
000000000000000
020000000000000
000000000000000
000000005000000
000000000007000
000000000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
020000020000000
022000000000000
020000000000000
000000000007000
000000000000000
000000000000000
000000000000000
```

**Train 3 — input**
```text
3020900000000000
3060800000000000
0000000000000000
0000000005050000
0000000005550000
0000000000000000
0030000000000000
0000000006000000
0000000000000000
0000000000008000
0000000000000000
0000000000000000
```
**Train 3 — output**
```text
0000000000000000
0000000000000000
0000000000000000
0000000000000000
0033300000000000
0030300006600000
0000000006000000
0000000006608080
0000000000008880
0000000000000000
```

**Train 4 — input**
```text
90402000000000
40607000000000
00000000000000
00000005500000
00000005000000
00000000000000
00000000000000
04000000000000
00000000600000
00000000000000
00000000007000
00000000000000
00000000000000
```
**Train 4 — output**
```text
00000000000000
00000000000000
00000000000000
00000000000000
00000000000000
04400000000000
04000000660000
00000000600000
00000000007700
00000000000700
00000000000000
```

**Test — input**
```text
203090000000000
204070000000000
000000005500000
000000000550000
000000000000000
000000000000000
020000000000000
000000000000000
000000000400000
000000000007000
000000000000000
000000000000000
000000000000000
```
**Test — output**
```text
000000000000000
000000000000000
000000000000000
000000000000000
002000000000000
022000000000000
020000000440000
000000000047700
000000000000770
000000000000000
000000000000000
```
**Written solution**

The top two rows map anchor colors to transforms. Extract the 5-motif, normalize it, then for each anchor stamp the appropriately transformed motif in the anchor’s color. The output excludes the legend and the source.

**Reference program**
```python
def rule_h91(g):
    h,w=size(g)
    # parse legend from first two rows: columns with row1 nonzero => mapping color -> token row0 same col
    mapping={}
    for c in range(w):
        color=g[1][c]
        token=g[0][c]
        if color!=0 and token in TOKEN_MAP_H91:
            mapping[color]=TOKEN_MAP_H91[token]
    source_cells=[(r-2,c) for r in range(2,h) for c,v in enumerate(g[r]) if v==5]
    if not source_cells:
        return blank(h-2,w)
    norm=normalize_cells(source_cells)
    out=blank(h-2,w)
    for r in range(2,h):
        for c,v in enumerate(g[r]):
            if v!=0 and v!=5:
                tid=mapping[v]
                coords=transform_coords(norm, tid)
                for dr,dc in coords:
                    nr,nc=(r-2)+dr,c+dc
                    if 0<=nr<h-2 and 0<=nc<w:
                        out[nr][nc]=v
    return out
```
