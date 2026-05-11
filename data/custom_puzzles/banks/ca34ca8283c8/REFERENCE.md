# ARC Additional Puzzle Bank — 21 Puzzles (Set 21)
This twenty-first pack continues the numbering with **`E141–E147`**, **`M141–M147`**, and **`H141–H147`**.
This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.
It introduces a new helper primitive for solver-facing implementations:
```text
phase_weave(anchor, directions, palette, h, w, mask=None, include_anchor=False)
```
Intuition: start from an anchor, march one cell at a time along each direction, and color visited cells by cycling through a legend palette. Optionally clip the walk to a mask such as a room interior. It is used directly in **E141**, **M141**, and **H141**.

Design goals for this set:

- easy: guide reading, endpoint filling, reflection, cropping, corner completion, command trails, and component filtering

- medium: room masking, chamber flood fill, legend selection, transform commands, hole-based recoloring, relational tables, and template stamping

- hard: eight-way phase weaving, transform analogy, nesting depth, routed overlaps, transform matrices, sorted packing, and composed recolor-plus-transform tasks

## E141 — Alternating Seed Rays
**Difficulty:** easy
**Train pairs:** 4
**Skills:** periodic painting, cardinal rays, legend reading
**Suggested staged path:** First isolate the legend colors on the top row. Then start from the seed and walk outward in the four cardinal directions, cycling those legend colors.

**Train 1 — input**
```text
028000000
000000000
000000000
000009000
000000000
000000000
000000000
```
**Train 1 — output**
```text
028002000
000008000
000002000
282829282
000002000
000008000
000002000
```
**Train 2 — input**
```text
03400000
00000000
00000000
00000000
00000000
00900000
00000000
00000000
```
**Train 2 — output**
```text
03400000
00400000
00300000
00400000
00300000
43934343
00300000
00400000
```
**Train 3 — input**
```text
0760000000
0000000000
0000000900
0000000000
0000000000
0000000000
```
**Train 3 — output**
```text
0760000600
0000000700
7676767976
0000000700
0000000600
0000000700
```
**Train 4 — input**
```text
0520000
0000000
0000000
0000000
0000000
0000000
0009000
0000000
0000000
```
**Train 4 — output**
```text
0522000
0005000
0002000
0005000
0002000
0005000
5259525
0005000
0002000
```
**Test — input**
```text
04700000000
00000000000
00000000000
00000000000
00000000900
00000000000
00000000000
00000000000
```
**Expected test output**
```text
04700000700
00000000400
00000000700
00000000400
74747474947
00000000400
00000000700
00000000400
```
**Written solution**
The top row provides a two-color palette. Keep the input as-is, then from the unique seed cell draw rays up, down, left, and right. Color the first step with the first legend color, the second step with the second legend color, then repeat that two-color cycle until the border.
**Reference program**
```python
def rule_e141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:2]
    sr=sc=None
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==9:
                sr,sc=r,c
    out=clone(g)
    for r,c,v in phase_weave((sr,sc), DIR4, palette, h,w):
        if out[r][c]==0:
            out[r][c]=v
    return out
```

## E142 — Fill the Gap
**Difficulty:** easy
**Train pairs:** 4
**Skills:** row reasoning, endpoint completion, same-color segments
**Suggested staged path:** Treat each row independently. When a color appears exactly twice on a row, everything between those two endpoints should match it.

**Train 1 — input**
```text
0000000000
0200200000
0000000000
0070000070
0000000000
0000000000
```
**Train 1 — output**
```text
0000000000
0222200000
0000000000
0077777770
0000000000
0000000000
```
**Train 2 — input**
```text
300300000
000000000
000006006
000000000
000000000
040000400
000000000
```
**Train 2 — output**
```text
333300000
000000000
000006666
000000000
000000000
044444400
000000000
```
**Train 3 — input**
```text
00000000000
00800000080
00000000000
00000000000
50005000000
```
**Train 3 — output**
```text
00000000000
00888888880
00000000000
00000000000
55555000000
```
**Train 4 — input**
```text
00000000
00000000
09000090
00000000
00000000
00000000
20020000
00000000
```
**Train 4 — output**
```text
00000000
00000000
09999990
00000000
00000000
00000000
22220000
00000000
```
**Test — input**
```text
000000000000
000400000040
000000000000
000000000000
700007000000
000000000000
000000020002
```
**Expected test output**
```text
000000000000
000444444440
000000000000
000000000000
777777000000
000000000000
000000022222
```
**Written solution**
On each row, find colors that appear exactly twice. Fill every cell between the left and right occurrence of that color, inclusive, with that same color. Leave all other rows and cells unchanged.
**Reference program**
```python
def rule_e142(g):
    h,w=size(g)
    out=clone(g)
    for r in range(h):
        row=g[r]
        for color in sorted(set(row)-{0}):
            pos=[c for c,v in enumerate(row) if v==color]
            if len(pos)==2:
                for c in range(min(pos), max(pos)+1):
                    out[r][c]=color
    return out
```

## E143 — Mirror Across the Guide
**Difficulty:** easy
**Train pairs:** 4
**Skills:** reflection, guide detection, same-size copy
**Suggested staged path:** The solid nonzero row is not part of the object. It is the mirror line.

**Train 1 — input**
```text
000000000
003000000
000007000
060000000
555555555
000000000
000000000
000000000
000000000
```
**Train 1 — output**
```text
000000000
003000000
000007000
060000000
555555555
060000000
000007000
003000000
000000000
```
**Train 2 — input**
```text
2000000000
0000800000
0000000040
5555555555
0000000000
0000000000
0000000000
0000000000
```
**Train 2 — output**
```text
2000000000
0000800000
0000000040
5555555555
0000000040
0000800000
2000000000
0000000000
```
**Train 3 — input**
```text
0000060
0900000
0000000
0000000
0002000
5555555
0000000
0000000
0000000
0000000
```
**Train 3 — output**
```text
0000060
0900000
0000000
0000000
0002000
5555555
0002000
0000000
0000000
0900000
```
**Train 4 — input**
```text
00700000000
00000000300
55555555555
00000000000
00000000000
00000000000
00000000000
```
**Train 4 — output**
```text
00700000000
00000000300
55555555555
00000000300
00700000000
00000000000
00000000000
```
**Test — input**
```text
000000000000
080000000000
000000300000
000000000070
555555555555
000000000000
000000000000
000000000000
000000000000
```
**Expected test output**
```text
000000000000
080000000000
000000300000
000000000070
555555555555
000000000070
000000300000
080000000000
000000000000
```
**Written solution**
Find the full-width guide row made of a single nonzero color. Copy every nonzero cell above that guide to the symmetric position below it, preserving color. Keep the original cells and the guide row.
**Reference program**
```python
def rule_e143(g):
    h,w=size(g)
    guide=None
    for r,row in enumerate(g):
        vals=set(row)
        if len(vals)==1 and 0 not in vals:
            guide=r; break
    out=clone(g)
    for r in range(guide):
        rr=2*guide-r
        if rr<h:
            for c,v in enumerate(g[r]):
                if v!=0:
                    out[rr][c]=v
    return out
```

## E144 — Crop the Action
**Difficulty:** easy
**Train pairs:** 4
**Skills:** bounding box, size change, object extraction
**Suggested staged path:** Ignore the empty border. The answer is just the tightest rectangle that still contains every nonzero cell.

**Train 1 — input**
```text
0000000000
0000000000
0004000000
0004000000
0004400000
0000000000
0000000000
0000000000
```
**Train 1 — output**
```text
40
40
44
```
**Train 2 — input**
```text
000000000
000008880
000000800
000000800
060000000
006000000
000000000
```
**Train 2 — output**
```text
0000888
0000080
0000080
6000000
0600000
```
**Train 3 — input**
```text
000000000000
000000000000
000000000000
000000000000
000000000000
000000030000
000000033000
000000033300
000000000000
```
**Train 3 — output**
```text
300
330
333
```
**Train 4 — input**
```text
0000000000
0550000000
0050000000
0055000000
0000004440
0000000000
```
**Train 4 — output**
```text
55000000
05000000
05500000
00000444
```
**Test — input**
```text
00000000000
00000000777
00000000000
00002200000
00000220000
00000020000
00000000000
00000000000
00000000000
```
**Expected test output**
```text
0000777
0000000
2200000
0220000
0020000
```
**Written solution**
Take the tight bounding box around all nonzero cells in the input and output exactly that cropped subgrid.
**Reference program**
```python
def rule_e144(g):
    return crop_bbox(g)
```

## E145 — Fourth Corner
**Difficulty:** easy
**Train pairs:** 4
**Skills:** axis-aligned rectangles, corner completion, color grouping
**Suggested staged path:** Group by color and look for three corners of an axis-aligned rectangle. The missing output cell is the fourth corner.

**Train 1 — input**
```text
000000000
030003000
000000000
000000000
030000000
000000000
000000000
```
**Train 1 — output**
```text
000000000
030003000
000000000
000000000
030003000
000000000
000000000
```
**Train 2 — input**
```text
0000000000
0000000044
0000000600
0000000000
0000000000
0000000004
0060000600
0000000000
```
**Train 2 — output**
```text
0000000000
0000000044
0060000600
0000000000
0000000000
0000000044
0060000600
0000000000
```
**Train 3 — input**
```text
07000000
00000000
00000000
07007000
00000000
00000000
```
**Train 3 — output**
```text
07007000
00000000
00000000
07007000
00000000
00000000
```
**Train 4 — input**
```text
000000000
000000800
005000050
000000000
000000808
000000000
000000000
000000050
000000000
```
**Train 4 — output**
```text
000000000
000000808
005000050
000000000
000000808
000000000
000000000
005000050
000000000
```
**Test — input**
```text
00000000000
00000020000
00000000707
00000000000
00000000000
02000020000
00000000700
00000000000
```
**Expected test output**
```text
00000000000
02000020000
00000000707
00000000000
00000000000
02000020000
00000000707
00000000000
```
**Written solution**
For each color, the input gives three of the four corners of an axis-aligned rectangle. Add the missing fourth corner of that same color and leave everything else unchanged.
**Reference program**
```python
def rule_e145(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            r0,c0,r1,c1=bbox(cells)
            corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}
            missing=list(corners-set(cells))
            if len(missing)==1:
                r,c=missing[0]
                out[r][c]=color
    return out
```

## E146 — Commanded Trail
**Difficulty:** easy
**Train pairs:** 4
**Skills:** symbol command, directional extension, same-size painting
**Suggested staged path:** One cell is a command, not part of the trail. The other nonzero cell is the color to extend.

**Train 1 — input**
```text
10000000
00000000
00000000
00000000
00060000
00000000
00000000
```
**Train 1 — output**
```text
10060000
00060000
00060000
00060000
00060000
00000000
00000000
```
**Train 2 — input**
```text
200000000
000000000
000007000
000000000
000000000
000000000
000000000
000000000
```
**Train 2 — output**
```text
200000000
000000000
000007000
000007000
000007000
000007000
000007000
000007000
```
**Train 3 — input**
```text
3000000000
0000000000
0000000000
0000000800
0000000000
0000000000
```
**Train 3 — output**
```text
3000000000
0000000000
0000000000
8888888800
0000000000
0000000000
```
**Train 4 — input**
```text
4000000
0000000
0000000
0000000
0000000
0500000
0000000
0000000
0000000
```
**Train 4 — output**
```text
4000000
0000000
0000000
0000000
0000000
0555555
0000000
0000000
0000000
```
**Test — input**
```text
1000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000900000
0000000000
```
**Expected test output**
```text
1000900000
0000900000
0000900000
0000900000
0000900000
0000900000
0000900000
0000000000
```
**Written solution**
The command cell encodes a direction: 1 up, 2 down, 3 left, 4 right. Starting from the unique non-command colored seed, extend that seed color in the commanded direction until the border. Keep the command and seed cells.
**Reference program**
```python
def rule_e146(g):
    h,w=size(g)
    out=clone(g)
    cmd=None
    seed=None
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in {1,2,3,4}:
                cmd=(r,c,v)
            elif v!=0:
                seed=(r,c,v)
    sr,sc,color=seed
    code=cmd[2]
    drdc={1:(-1,0),2:(1,0),3:(0,-1),4:(0,1)}[code]
    r,c=sr+drdc[0], sc+drdc[1]
    while 0<=r<h and 0<=c<w:
        if out[r][c]==0:
            out[r][c]=color
        r+=drdc[0]; c+=drdc[1]
    return out
```

## E147 — Keep the Largest
**Difficulty:** easy
**Train pairs:** 4
**Skills:** connected components, ranking by area, filtering
**Suggested staged path:** You do not need to transform the objects. You only need to decide which connected component is largest.

**Train 1 — input**
```text
0000000000
0220000000
0220000000
0000044400
0000040400
0000044400
7770000000
0000000000
```
**Train 1 — output**
```text
0000000000
0000000000
0000000000
0000044400
0000040400
0000044400
0000000000
0000000000
```
**Train 2 — input**
```text
000000000
088800000
008000000
008000000
000000000
000033300
000033300
000033300
000000000
```
**Train 2 — output**
```text
000000000
000000000
000000000
000000000
000000000
000033300
000033300
000033300
000000000
```
**Train 3 — input**
```text
000000000000
000000006000
005500006600
000500006660
000550000000
000000000000
000004440000
```
**Train 3 — output**
```text
000000000000
000000006000
000000006600
000000006660
000000000000
000000000000
000000000000
```
**Train 4 — input**
```text
00000000000
02200000000
00220077770
00020070070
00000070070
00000077770
00000000000
00000000000
```
**Train 4 — output**
```text
00000000000
00000000000
00000077770
00000070070
00000070070
00000077770
00000000000
00000000000
```
**Test — input**
```text
000000000000
040000000000
040000000000
044006666000
000006006000
000006006000
000006666022
000000000022
000000000000
```
**Expected test output**
```text
000000000000
000000000000
000000000000
000006666000
000006006000
000006006000
000006666000
000000000000
000000000000
```
**Written solution**
Find all nonzero connected components and keep only the largest one. Replace every other nonzero cell with black.
**Reference program**
```python
def rule_e147(g):
    comps=components(g)
    best=max(comps, key=lambda comp:(len(comp["cells"]), -min(r for r,c in comp["cells"]), -min(c for r,c in comp["cells"])))
    out=blank(*size(g),0)
    for r,c in best["cells"]:
        out[r][c]=best["color"]
    return out
```

## M141 — Room-Limited Weave
**Difficulty:** medium
**Train pairs:** 4
**Skills:** masking by chamber, periodic rays, frame reasoning
**Suggested staged path:** This is the same alternating-ray idea as the easy version, except the frame blocks the rays. Work inside the seed’s chamber only.

**Train 1 — input**
```text
0280000000
0111111110
0100000010
0100000010
0100090010
0100000010
0111111110
0000000000
```
**Train 1 — output**
```text
0280000000
0111111110
0100080010
0100020010
0128292810
0100020010
0111111110
0000000000
```
**Train 2 — input**
```text
034000000
011111110
010000010
010000010
010000010
010900010
010000010
011111110
000000000
```
**Train 2 — output**
```text
034000000
011111110
010300010
010400010
010300010
013934310
010300010
011111110
000000000
```
**Train 3 — input**
```text
06700000000
01111111110
01000000010
01000009010
01000000010
01111111110
00000000000
```
**Train 3 — output**
```text
06700000000
01111111110
01000006010
01676769610
01000006010
01111111110
00000000000
```
**Train 4 — input**
```text
05200000
01111110
01000010
01000010
01000010
01000010
01009010
01000010
01111110
00000000
```
**Train 4 — output**
```text
05200000
01111110
01002010
01005010
01002010
01005010
01259510
01005010
01111110
00000000
```
**Test — input**
```text
046000000000
011111111110
010000000010
010000000010
010000009010
010000000010
010000000010
011111111110
000000000000
```
**Expected test output**
```text
046000000000
011111111110
010000006010
010000004010
016464649410
010000004010
010000006010
011111111110
000000000000
```
**Written solution**
The top row gives a two-color palette and the frame walls are color 1. Starting at the seed, draw alternating-color rays in the four cardinal directions, but only through the interior chamber reachable from the seed without crossing the frame.
**Reference program**
```python
def rule_m141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:2]
    seed=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                seed=(r,c)
    mask=chamber_from_seed(g, seed, wall=1)
    out=clone(g)
    for r,c,v in phase_weave(seed, DIR4, palette, h,w, mask=mask-{seed}):
        if out[r][c]==0:
            out[r][c]=v
    return out
```

## M142 — Chamber Paint
**Difficulty:** medium
**Train pairs:** 4
**Skills:** flood fill, containment, multiple chambers
**Suggested staged path:** The marker does not just recolor itself. It names the whole region inside its frame.

**Train 1 — input**
```text
000000000000
011110000000
013010000000
010010000000
011110000000
000000011110
000000017010
000000010010
000000011110
000000000000
```
**Train 1 — output**
```text
000000000000
011110000000
013310000000
013310000000
011110000000
000000011110
000000017710
000000017710
000000011110
000000000000
```
**Train 2 — input**
```text
00000000000
01111100000
01000101110
01020101010
01000101810
01111101010
00000001010
00000001110
00000000000
```
**Train 2 — output**
```text
00000000000
01111100000
01222101110
01222101810
01222101810
01111101810
00000001810
00000001110
00000000000
```
**Train 3 — input**
```text
0000000000000
0011110011110
0010010016010
0014010010010
0010010010010
0010010011110
0011110000000
0000000000000
```
**Train 3 — output**
```text
0000000000000
0011110011110
0014410016610
0014410016610
0014410016610
0014410011110
0011110000000
0000000000000
```
**Train 4 — input**
```text
00000000000
01111000000
01071000000
01001000000
01111000000
00000000000
00111111100
00100500100
00100000100
00111111100
00000000000
```
**Train 4 — output**
```text
00000000000
01111000000
01771000000
01771000000
01111000000
00000000000
00111111100
00155555100
00155555100
00111111100
00000000000
```
**Test — input**
```text
00000000000000
01111000000000
01201000111110
01001000100010
01001000109010
01111000100010
01111100100010
01040100111110
01111100000000
00000000000000
```
**Expected test output**
```text
00000000000000
01111000000000
01221000111110
01221000199910
01221000199910
01111000199910
01111100199910
01444100111110
01111100000000
00000000000000
```
**Written solution**
Each non-frame marker sits inside a chamber bounded by color-1 walls. Flood fill that chamber with the marker’s color, keeping the frame intact. Do this independently for every chamber.
**Reference program**
```python
def rule_m142(g):
    h,w=size(g)
    out=clone(g)
    markers=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in {0,1}]
    for r,c,color in markers:
        q=deque([(r,c)]); seen={(r,c)}
        while q:
            rr,cc=q.popleft()
            out[rr][cc]=color
            for dr,dc in DIR4:
                nr,nc=rr+dr,cc+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=1:
                    seen.add((nr,nc)); q.append((nr,nc))
    return out
```

## M143 — Legend Select Crop
**Difficulty:** medium
**Train pairs:** 4
**Skills:** legend lookup, component selection, normalization
**Suggested staged path:** The top-left cell is a selector, not an object to crop.

**Train 1 — input**
```text
400000000000
000000000000
000400000000
000400007770
000440000700
000000000700
022200000000
000000000000
```
**Train 1 — output**
```text
40
40
44
```
**Train 2 — input**
```text
70000000000
00000000440
00000000440
00000777000
00000707000
06600777000
00600000000
00660000000
00000000000
```
**Train 2 — output**
```text
777
707
777
```
**Train 3 — input**
```text
2000000000000
0000000000000
0000000002200
0050000000220
0055000000020
0055500000000
0000000000000
```
**Train 3 — output**
```text
220
022
002
```
**Train 4 — input**
```text
6000000000
0333300000
0300300000
0300300000
0333366000
0000006000
0000006600
0000000000
0000000000
0000000000
```
**Train 4 — output**
```text
660
060
066
```
**Test — input**
```text
500000000000
000000000000
022200000000
022200000000
022200050000
000000055000
000000055500
000080000000
000008000000
```
**Expected test output**
```text
500
550
555
```
**Written solution**
Read the top-left legend color. Among the remaining components, select the component of that color, crop it to its tight bounding box, and output that normalized crop.
**Reference program**
```python
def rule_m143(g):
    target=g[0][0]
    g2=clone(g); g2[0][0]=0
    comps=[comp for comp in components(g2) if comp["color"]==target]
    comp=max(comps, key=lambda comp: len(comp["cells"]))
    return normalize_component(comp)
```

## M144 — Commanded Transform
**Difficulty:** medium
**Train pairs:** 4
**Skills:** dihedral transforms, command decoding, cropping
**Suggested staged path:** The command cell tells you how to transform the object. The output is the transformed object only, cropped tight.

**Train 1 — input**
```text
2000000000
0000000000
0000000000
0000600000
0000670000
0000000000
0000000000
0000000000
```
**Train 1 — output**
```text
66
70
```
**Train 2 — input**
```text
500000000
000000000
008800000
000800000
000080000
000000000
000000000
000000000
000000000
```
**Train 2 — output**
```text
088
080
800
```
**Train 3 — input**
```text
30000000000
00000000000
00000000000
00000033000
00000030300
00000000000
00000000000
```
**Train 3 — output**
```text
303
033
```
**Train 4 — input**
```text
70000000
00000000
00070000
00077000
00007000
00000000
00000000
00000000
```
**Train 4 — output**
```text
770
077
```
**Test — input**
```text
4000000000
0000000000
0000000000
0000000000
0000550000
0000050000
0000055000
0000000000
0000000000
0000000000
```
**Expected test output**
```text
005
555
500
```
**Written solution**
Interpret the top-left code as a geometric transform, apply that transform to the nonzero object elsewhere in the grid, and output the transformed object cropped to its bounding box.
**Reference program**
```python
def rule_m144(g):
    code=g[0][0]
    g2=clone(g); g2[0][0]=0
    obj=crop_bbox(g2)
    return apply_transform(obj, code)
```

## M145 — Holes Decide the Color
**Difficulty:** medium
**Train pairs:** 4
**Skills:** hole counting, component analysis, recoloring
**Suggested staged path:** The shape geometry stays the same. What changes is the color assigned to each component based on its number of holes.

**Train 1 — input**
```text
000000000000
022000000000
022000000000
000000222000
000000202000
022200222000
022200000000
022200000000
000000000000
```
**Train 1 — output**
```text
000000000000
033000000000
033000000000
000000444000
000000404000
033300444000
033300000000
033300000000
000000000000
```
**Train 2 — input**
```text
00000000000
02222000000
02002000000
02002000000
02222000000
00000000220
00000000220
00000000000
```
**Train 2 — output**
```text
00000000000
04444000000
04004000000
04004000000
04444000000
00000000330
00000000330
00000000000
```
**Train 3 — input**
```text
0000000000
0000000000
0220000000
0020000000
0022000000
0000022200
0000020200
0000022200
0000000000
0000000000
```
**Train 3 — output**
```text
0000000000
0000000000
0330000000
0030000000
0033000000
0000044400
0000040400
0000044400
0000000000
0000000000
```
**Train 4 — input**
```text
0000000000000
0000000022200
0000000022200
0000000022200
0022220000000
0020020000000
0020020000220
0022220000220
0000000000000
```
**Train 4 — output**
```text
0000000000000
0000000033300
0000000033300
0000000033300
0044440000000
0040040000000
0040040000330
0044440000330
0000000000000
```
**Test — input**
```text
000000000000
022200000000
020200022200
022200022200
000000022200
000000000000
000022000000
000002000000
000002200000
000000000000
```
**Expected test output**
```text
000000000000
044400000000
040400033300
044400033300
000000033300
000000000000
000033000000
000003000000
000003300000
000000000000
```
**Written solution**
For each connected component, count the number of enclosed holes in its shape. Recolor the whole component according to that count: no holes becomes one color, one hole becomes another, and so on. Keep the geometry unchanged.
**Reference program**
```python
def rule_m145(g):
    out=blank(*size(g),0)
    for comp in components(g):
        holes=hole_count_component(comp["cells"])
        color={0:3,1:4,2:5}.get(holes, 6)
        for r,c in comp["cells"]:
            out[r][c]=color
    return out
```

## M146 — Area Comparison Table
**Difficulty:** medium
**Train pairs:** 4
**Skills:** object ranking, relational output, matrix construction
**Suggested staged path:** The answer is not a transformed scene. It is a summary matrix comparing the three objects from left to right.

**Train 1 — input**
```text
00000000000000
00000000004440
02200333004440
02200303004440
00000333000000
00000000000000
00000000000000
00000000000000
```
**Train 1 — output**
```text
200
520
552
```
**Train 2 — input**
```text
000000000000000
000000000000000
000006660000000
000006660007700
000006660000700
000000000000770
055500000000000
000000000000000
000000000000000
```
**Train 2 — output**
```text
200
525
502
```
**Train 3 — input**
```text
0000000000000
0222000000000
0202000004000
0222008804400
0000008804440
0000000000000
0000000000000
```
**Train 3 — output**
```text
255
020
052
```
**Train 4 — input**
```text
0000000000000000
0000003333000000
0660003003000000
0060003003000000
0066003333000990
0000000000000990
0000000000000000
0000000000000000
```
**Train 4 — output**
```text
205
525
002
```
**Test — input**
```text
000000000000000
022200000000000
022200000008880
022200055008080
000000005008880
000000005500000
000000000000000
000000000000000
```
**Expected test output**
```text
255
020
052
```
**Written solution**
Order the three components from left to right. Build a square matrix whose diagonal is a fixed self-comparison value and whose off-diagonal cells indicate whether the row object has larger area than the column object.
**Reference program**
```python
def rule_m146(g):
    comps=sort_comps_left_to_right(components(g))
    areas=[len(comp["cells"]) for comp in comps]
    n=len(comps)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=2
            else:
                out[i][j]=5 if areas[i]>areas[j] else 0
    return out
```

## M147 — Template Copies
**Difficulty:** medium
**Train pairs:** 4
**Skills:** template extraction, anchored stamping, multiple placements
**Suggested staged path:** The colored shape in the top-left is the template. Every 9 tells you where another copy should start.

**Train 1 — input**
```text
240000000000
024000000000
000000000000
000000900000
000000000000
090000000000
000000000000
000000000000
```
**Train 1 — output**
```text
240000000000
024000000000
000000000000
000000240000
000000024000
024000000000
002400000000
000000000000
```
**Train 2 — input**
```text
6600000000000
0600000090000
0060000000000
0000000000000
0000000000000
0000090000000
0000000000000
0000000000000
0000000000000
```
**Train 2 — output**
```text
6600000000000
0600000066000
0060000006000
0000000000600
0000000000000
0000066000000
0000006000000
0000000600000
0000000000000
```
**Train 3 — input**
```text
70000000000
77000000000
00000000000
00000009000
00000000000
00090000000
00000000000
```
**Train 3 — output**
```text
70000000000
77000000000
00000000000
00000007000
00000007700
00070000000
00077000000
```
**Train 4 — input**
```text
808000000000
080000000000
000000009000
000000000000
000000000000
000000000000
000090000000
000000000900
000000000000
000000000000
```
**Train 4 — output**
```text
808000000000
080000000000
000000008080
000000000800
000000000000
000000000000
000080800000
000008000808
000000000080
000000000000
```
**Test — input**
```text
24000000000000
02400000000000
00000000090000
00000000000000
00000000000000
00000900000000
09000000000000
00000000000000
00000000000000
```
**Expected test output**
```text
24000000000000
02400000000000
00000000024000
00000000002400
00000000000000
00000240000000
02400024000000
00240000000000
00000000000000
```
**Written solution**
Extract the non-9 template from the top-left of the input. Keep the original template and stamp identical copies with their top-left corner anchored at every 9 marker location.
**Reference program**
```python
def rule_m147(g):
    h,w=size(g)
    markers=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    non9=[[v if v!=9 else 0 for v in row] for row in g]
    template=crop_bbox(non9)
    # original template top-left from bbox of non9 cells
    cells=nonzero_cells(non9)
    r0,c0,r1,c1=bbox(cells)
    out=blank(h,w,0)
    positions=[(r0,c0)] + markers
    th,tw=size(template)
    for top,left in positions:
        for r in range(th):
            for c in range(tw):
                v=template[r][c]
                if v!=0 and 0<=top+r<h and 0<=left+c<w:
                    out[top+r][left+c]=v
    return out
```

## H141 — Eight-Way Room Weave
**Difficulty:** hard
**Train pairs:** 4
**Skills:** periodic painting, eight-direction rays, masked propagation
**Suggested staged path:** It is the room-limited weave again, but the legend is longer and the rays go diagonally too.

**Train 1 — input**
```text
02840000000
01111111110
01000000010
01000000010
01000900010
01000000010
01000000010
01111111110
00000000000
```
**Train 1 — output**
```text
02840000000
01111111110
01080808010
01002220010
01482928410
01002220010
01080808010
01111111110
00000000000
```
**Train 2 — input**
```text
0367000000
0111111110
0100000010
0100000010
0100000010
0100000010
0109000010
0100000010
0111111110
0000000000
```
**Train 2 — output**
```text
0367000000
0111111110
0103000310
0107007010
0106060010
0133300010
0139367310
0133300010
0111111110
0000000000
```
**Train 3 — input**
```text
052400000000
011111111110
010000000010
010000009010
010000000010
010000000010
011111111110
000000000000
```
**Train 3 — output**
```text
052400000000
011111111110
010000055510
014254259510
010000055510
010000202010
011111111110
000000000000
```
**Train 4 — input**
```text
074600000
011111110
010000010
010000010
010000010
010000010
010000010
010090010
010000010
011111110
000000000
```
**Train 4 — output**
```text
074600000
011111110
010040010
010070010
010060010
014040410
010777010
014797410
010777010
011111110
000000000
```
**Test — input**
```text
0428000000000
0111111111110
0100000000010
0100000000010
0100000000010
0100000009010
0100000000010
0100000000010
0111111111110
0000000000000
```
**Expected test output**
```text
0428000000000
0111111111110
0100008008010
0100000202010
0100000044410
0148248249410
0100000044410
0100000202010
0111111111110
0000000000000
```
**Written solution**
Read the three-color legend on the top row. From the seed, draw rays in all eight directions, cycling through the legend colors step by step, and clip the result to the chamber inside the frame.
**Reference program**
```python
def rule_h141(g):
    h,w=size(g)
    palette=[v for v in g[0] if v!=0][:3]
    seed=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                seed=(r,c)
    mask=chamber_from_seed(g, seed, wall=1)
    out=clone(g)
    for r,c,v in phase_weave(seed, DIR8, palette, h,w, mask=mask-{seed}):
        if out[r][c]==0:
            out[r][c]=v
    return out
```

## H142 — Transform Analogy
**Difficulty:** hard
**Train pairs:** 4
**Skills:** analogy, panel parsing, transform inference
**Suggested staged path:** Do not memorize a specific transform from one example. Infer which transform turns the first panel into the second, then apply that same transform to the third.

**Train 1 — input**
```text
00000000000000000
02200000020007000
00200002220007700
00220002000000700
00000000000000000
```
**Train 1 — output**
```text
077
770
```
**Train 2 — input**
```text
33000000330000000
00330033000008800
00030030000008080
00000000000008000
00000000000000000
```
**Train 2 — output**
```text
088
808
008
```
**Train 3 — input**
```text
00000000000006600
44000044000000060
04000004000000660
04400004400000000
00000000000000000
```
**Train 3 — output**
```text
660
006
066
```
**Train 4 — input**
```text
00000000000000000
05500005500022000
05050005050002200
00550000550000220
00000000000000000
```
**Train 4 — output**
```text
2200
0220
0022
```
**Test — input**
```text
00000000000000000
07700000070008800
00700007700008080
00070007000000800
00000000000000000
```
**Expected test output**
```text
080
808
880
```
**Written solution**
Split the input into three panels. Infer which geometric transform maps panel A’s object to panel B’s object, then apply that same transform to panel C and output the transformed object cropped tight.
**Reference program**
```python
def rule_h142(g):
    panels=split_by_zero_cols(g)
    assert len(panels)==3
    A,B,C=panels
    A=strip_zero_border(A); B=strip_zero_border(B); C=strip_zero_border(C)
    code=None
    for k,tf in TRANSFORMS.items():
        if eq_grid(strip_zero_border(apply_transform(A,k)), B):
            code=k; break
    if code is None:
        raise ValueError("no transform")
    return strip_zero_border(apply_transform(C, code))
```

## H143 — Depth-Colored Frames
**Difficulty:** hard
**Train pairs:** 4
**Skills:** nested structure, component ordering, depth assignment
**Suggested staged path:** Each frame is its own component. What matters is not the original color but how deeply nested the frame is.

**Train 1 — input**
```text
00000000000
01111111110
01000000010
01011111010
01010001010
01010101010
01010001010
01011111010
01000000010
01111111110
00000000000
```
**Train 1 — output**
```text
00000000000
02222222220
02000000020
02033333020
02030003020
02030403020
02030003020
02033333020
02000000020
02222222220
00000000000
```
**Train 2 — input**
```text
000000000
011111110
010000010
010111010
010101010
010111010
010000010
011111110
000000000
```
**Train 2 — output**
```text
000000000
022222220
020000020
020333020
020303020
020333020
020000020
022222220
000000000
```
**Train 3 — input**
```text
0000000000000
0111111111110
0100000000010
0101111111010
0101000001010
0101011101010
0101010101010
0101011101010
0101000001010
0101111111010
0100000000010
0111111111110
0000000000000
```
**Train 3 — output**
```text
0000000000000
0222222222220
0200000000020
0203333333020
0203000003020
0203044403020
0203040403020
0203044403020
0203000003020
0203333333020
0200000000020
0222222222220
0000000000000
```
**Train 4 — input**
```text
0000000
0111110
0100010
0101010
0100010
0111110
0000000
```
**Train 4 — output**
```text
0000000
0222220
0200020
0203020
0200020
0222220
0000000
```
**Test — input**
```text
000000000000000
011111111111110
010000000000010
010111111111010
010100000001010
010101111101010
010101000101010
010101010101010
010101000101010
010101111101010
010100000001010
010111111111010
010000000000010
011111111111110
000000000000000
```
**Expected test output**
```text
000000000000000
022222222222220
020000000000020
020333333333020
020300000003020
020304444403020
020304000403020
020304050403020
020304000403020
020304444403020
020300000003020
020333333333020
020000000000020
022222222222220
000000000000000
```
**Written solution**
The input contains nested rectangular frame components. Recolor the outermost frame with one color, the next frame inward with the next color, and continue by depth while keeping the frame geometry unchanged.
**Reference program**
```python
def rule_h143(g):
    comps=components(g)
    # sort outer to inner by bbox area descending
    comps=sorted(comps, key=lambda comp: ((bbox(comp["cells"])[2]-bbox(comp["cells"])[0]+1)*(bbox(comp["cells"])[3]-bbox(comp["cells"])[1]+1)), reverse=True)
    out=blank(*size(g),0)
    for i,comp in enumerate(comps):
        color=2+i
        for r,c in comp["cells"]:
            out[r][c]=color
    return out
```

## H144 — Path Overlap
**Difficulty:** hard
**Train pairs:** 4
**Skills:** routing, pairing by color, overlap resolution
**Suggested staged path:** Each color defines a pair of terminals. Draw the deterministic L-shaped path for each pair, then resolve collisions with a special overlap color.

**Train 1 — input**
```text
0000000000
0200003000
0000000000
0000000000
0000000000
0300002000
0000000000
0000000000
```
**Train 1 — output**
```text
0000000000
0888888000
0300002000
0300002000
0300002000
0300002000
0000000000
0000000000
```
**Train 2 — input**
```text
000030000
000000000
002000000
000000000
000000000
000000000
000000030
000020000
000000000
```
**Train 2 — output**
```text
000033330
000000030
002220030
000020030
000020030
000020030
000020030
000020000
000000000
```
**Train 3 — input**
```text
000000000000
000030000200
000000000000
000000000000
000000000000
000200000300
000000000000
```
**Train 3 — output**
```text
000000000000
000288888800
000200000300
000200000300
000200000300
000200000300
000000000000
```
**Train 4 — input**
```text
0000000000
0000000030
0000000000
0200000000
0000000000
0000000000
0000000000
0000000000
0003000020
0000000000
```
**Train 4 — output**
```text
0000000000
0003333330
0003000000
0228222220
0003000020
0003000020
0003000020
0003000020
0003000020
0000000000
```
**Test — input**
```text
00000000000
00200000000
00000000030
00000000000
00000000000
00000000000
00000000000
00003000020
00000000000
```
**Expected test output**
```text
00000000000
00222222220
00003333380
00003000020
00003000020
00003000020
00003000020
00003000020
00000000000
```
**Written solution**
For each color, connect its two terminals using the fixed Manhattan L-path rule. Paint each path in its own color, but any cell used by more than one path becomes the overlap color.
**Reference program**
```python
def rule_h144(g):
    h,w=size(g)
    out=blank(h,w,0)
    paths=[]
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        pts=sorted(pts)
        cells=l_path(pts[0], pts[1])
        paths.append((color,cells))
    counts=Counter(cell for _,cells in paths for cell in cells)
    for color,cells in paths:
        for r,c in cells:
            out[r][c]=8 if counts[(r,c)]>1 else color
    return out
```

## H145 — Transform Code Tiling
**Difficulty:** hard
**Train pairs:** 4
**Skills:** matrix-controlled transforms, template tiling, panel parsing
**Suggested staged path:** The left panel is a template and the right panel is a matrix of commands. The output is a tiled grid of transformed template copies.

**Train 1 — input**
```text
60012
67034
```
**Train 1 — output**
```text
6066
6770
7607
0666
```
**Train 2 — input**
```text
80041
08023
```
**Train 2 — output**
```text
0880
8008
0880
8008
```
**Train 3 — input**
```text
23021
20014
```
**Train 3 — output**
```text
2223
0320
2330
2022
```
**Train 4 — input**
```text
50032
55041
```
**Train 4 — output**
```text
5555
0550
0550
5555
```
**Test — input**
```text
70024
77031
```
**Expected test output**
```text
7707
7077
7770
0777
```
**Written solution**
Extract the template from the left panel. For each command in the right-hand code matrix, transform the template accordingly and place the result in the matching tile position of the output grid.
**Reference program**
```python
def rule_h145(g):
    parts=split_by_zero_cols(g)
    assert len(parts)==2
    template=strip_zero_border(parts[0])
    codes=parts[1]
    mh,mw=size(codes)
    th,tw=size(template)
    out=blank(mh*th, mw*tw, 0)
    for rr in range(mh):
        for cc in range(mw):
            code=codes[rr][cc]
            tf=apply_transform(template, code)
            tf=strip_zero_border(tf)
            # assume same square size
            for r in range(th):
                for c in range(tw):
                    v=tf[r][c]
                    if v!=0:
                        out[rr*th+r][cc*tw+c]=v
    return out
```

## H146 — Sort by Holes and Pack
**Difficulty:** hard
**Train pairs:** 4
**Skills:** hole counting, sorting, packing normalized shapes
**Suggested staged path:** You need both analysis and rearrangement: count holes first, then crop and reorder the components.

**Train 1 — input**
```text
000000000000000
022000000000000
022000000000000
000000444000000
000000404000000
000000444006600
000000000000600
000000000000660
000000000000000
```
**Train 1 — output**
```text
2206600444
2200600404
0000660444
```
**Train 2 — input**
```text
00000000000000
07777000000000
07007000000000
07007000000000
07777000000000
00000000033300
00000000033300
00000000033300
00000000000000
00000000000000
```
**Train 2 — output**
```text
33307777
33307007
33307007
00007777
```
**Train 3 — input**
```text
0000000000000000
0055000000000000
0005000000002220
0005500000002020
0000000088002220
0000000088000000
0000000000000000
0000000000000000
```
**Train 3 — output**
```text
8805500222
8800500202
0000550222
```
**Train 4 — input**
```text
0000000000000
0444000000000
0444000000000
0444000000000
0000000666000
0000000606000
0000000666099
0000000000099
0000000000000
```
**Train 4 — output**
```text
9904440666
9904440606
0004440666
```
**Test — input**
```text
0000000000000000
0222200000000000
0200200000000000
0200200000000000
0222200000000000
0000005500000000
0000000500008800
0000000550008800
0000000000000000
0000000000000000
```
**Expected test output**
```text
88055002222
88005002002
00005502002
00000002222
```
**Written solution**
For each component, count its holes, crop it to a tight bounding box, and then sort the components by increasing hole count. Pack the normalized shapes left to right with one blank column between them.
**Reference program**
```python
def rule_h146(g):
    comps=components(g)
    items=[]
    for comp in comps:
        norm=normalize_component(comp)
        items.append((hole_count_component(comp["cells"]), len(comp["cells"]), norm))
    items.sort(key=lambda x:(x[0], x[1]))
    maxh=max(len(norm) for _,_,norm in items)
    totalw=sum(len(norm[0]) for _,_,norm in items)+(len(items)-1)
    out=blank(maxh,totalw,0)
    x=0
    for _,_,norm in items:
        nh,nw=size(norm)
        for r in range(nh):
            for c in range(nw):
                v=norm[r][c]
                if v!=0:
                    out[r][x+c]=v
        x += nw + 1
    return out
```

## H147 — Remap Then Transform
**Difficulty:** hard
**Train pairs:** 4
**Skills:** palette permutation, command composition, cropped output
**Suggested staged path:** Two independent instructions are present: a color mapping and a geometric transform. Apply both.

**Train 1 — input**
```text
202300
008600
230000
023000
200000
```
**Train 1 — output**
```text
808
086
060
```
**Train 2 — input**
```text
504500
002700
450000
405000
044000
```
**Train 2 — output**
```text
072
702
220
```
**Train 3 — input**
```text
306700
003900
670000
607000
006000
```
**Train 3 — output**
```text
300
903
093
```
**Train 4 — input**
```text
702300
004800
230000
203000
000300
```
**Train 4 — output**
```text
440
800
080
008
```
**Test — input**
```text
402300
007500
230000
203000
033000
```
**Expected test output**
```text
055
505
770
```
**Written solution**
Read the top-row transform code and the aligned source-to-target color mapping in the first two rows. Recolor the object using that palette permutation, apply the commanded transform, and output the result cropped tight.
**Reference program**
```python
def rule_h147(g):
    code=g[0][0]
    src=[v for v in g[0][2:] if v!=0]
    tgt=[v for v in g[1][2:] if v!=0]
    mapping=dict(zip(src,tgt))
    obj=[row[:] for row in g[2:]]
    obj=crop_bbox(obj)
    remapped=[[mapping.get(v,v) if v!=0 else 0 for v in row] for row in obj]
    return strip_zero_border(apply_transform(remapped, code))
```
