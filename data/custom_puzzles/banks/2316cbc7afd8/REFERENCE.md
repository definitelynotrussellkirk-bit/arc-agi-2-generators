# ARC Additional Puzzle Bank — 21 Puzzles (Set 16)

This sixteenth pack continues the numbering with **`E106–E112`**, **`M106–M112`**, and **`H106–H112`**.

This set contains **84 train pairs across 21 puzzles**, averaging **4.00 train pairs per puzzle**.

It introduces a new helper primitive for solver-facing implementations:

```text
infer_dihedral(src, dst, candidates=None)
```

This helper infers which dihedral transform (rotation, reflection, transpose, anti-transpose, or identity) maps one motif to another. In this pack it is used directly in **E106**, **M106**, and **H106**.


## E106 — Three-Panel Transform Transfer

**Difficulty:** easy

**Train pairs:** 4

**Skills:** dihedral transform, panel analogy, motif transfer

**Suggested staged path:** First isolate the three panels. Infer how the first panel changed into the second, then apply exactly that same transform to the third.


**Train 1 — input**

```text
12090119030
10090029033
00090009003
```


**Train 1 — output**

```text
000
033
330
```


**Train 2 — input**

```text
44090449060
00494009660
04090409600
```


**Train 2 — output**

```text
060
066
006
```


**Train 3 — input**

```text
70097709080
77090779008
07090009088
```


**Train 3 — output**

```text
000
808
088
```


**Train 4 — input**

```text
03093009120
03393309100
00390309000
```


**Train 4 — output**

```text
000
001
021
```


**Test — input**

```text
08098809440
00898089004
08890009040
```


**Test — output**

```text
040
404
004
```


**Written solution**

Read the three 3×3 panels as A, B, and C. Infer the dihedral transform that maps A to B, then apply that same transform to C and return only the transformed third panel.


**Reference program**

```python
def rule_e106(g):
    a,b,c=split_by_full_color_cols(g,9)
    t=infer_dihedral(a,b)
    return TRANSFORMS[t](c)
```


## E107 — Rectangle from Three Corners

**Difficulty:** easy

**Train pairs:** 4

**Skills:** bbox, rectangle completion, same-size border drawing

**Suggested staged path:** Ignore that one corner is missing. Use the bounding box of the colored cells, then draw the full rectangle border of that box.


**Train 1 — input**

```text
0000000
0200020
0000000
0000000
0000000
0200000
0000000
```


**Train 1 — output**

```text
0000000
0222220
0200020
0200020
0200020
0222220
0000000
```


**Train 2 — input**

```text
00000000
00000000
00300030
00000000
00000000
00000000
00000030
00000000
```


**Train 2 — output**

```text
00000000
00000000
00333330
00300030
00300030
00300030
00333330
00000000
```


**Train 3 — input**

```text
000000000
000400000
000000000
000000000
000400040
000000000
```


**Train 3 — output**

```text
000000000
000444440
000400040
000400040
000444440
000000000
```


**Train 4 — input**

```text
0000000000
0000000600
0000000000
0000000000
0000000000
0060000600
0000000000
```


**Train 4 — output**

```text
0000000000
0066666600
0060000600
0060000600
0060000600
0066666600
0000000000
```


**Test — input**

```text
000000000
000000000
080000000
000000000
000000000
000000000
080000800
000000000
000000000
```


**Test — output**

```text
000000000
000000000
088888800
080000800
080000800
080000800
088888800
000000000
000000000
```


**Written solution**

The three nonzero cells are three corners of one axis-aligned rectangle. Take their bounding box and draw the full border in the same color.


**Reference program**

```python
def rule_e107(g):
    pts=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not pts:
        return clone(g)
    color=pts[0][2]
    cells=[(r,c) for r,c,v in pts]
    r0,c0,r1,c1=bbox(cells)
    out=blank(*size(g))
    return draw_rect_border(out,r0,c0,r1,c1,color)
```


## E108 — Extract the Densest Row

**Difficulty:** easy

**Train pairs:** 4

**Skills:** row statistics, selection, dynamic-size output

**Suggested staged path:** Count how many nonzero cells each row contains. Keep only the row with the largest count and output that row by itself.


**Train 1 — input**

```text
0000000
0202000
0033300
0000000
4000004
```


**Train 1 — output**

```text
0033300
```


**Train 2 — input**

```text
1000100
0222200
0030300
0000000
0404040
```


**Train 2 — output**

```text
0222200
```


**Train 3 — input**

```text
000000
005500
066660
000070
700007
```


**Train 3 — output**

```text
066660
```


**Train 4 — input**

```text
8000080
0000000
0909090
0000000
0077700
```


**Train 4 — output**

```text
0909090
```


**Test — input**

```text
00000000
02020200
00330030
00000000
44444000
```


**Test — output**

```text
44444000
```


**Written solution**

Scan the rows and count nonzero cells. Select the row with the highest count, breaking ties by the earliest row, and output that row alone.


**Reference program**

```python
def rule_e108(g):
    best_row=max(range(len(g)), key=lambda r: (sum(v!=0 for v in g[r]), -r))  # tie topmost
    return [g[best_row][:]]
```


## E109 — Crop the Unique-Color Object

**Difficulty:** easy

**Train pairs:** 4

**Skills:** component counting by color, object selection, cropping

**Suggested staged path:** Group components by color. Find the color that appears in exactly one component, then crop tightly to that object.


**Train 1 — input**

```text
0000000000
0220000300
0000000000
0000400000
0000440000
0200000300
0000000000
```


**Train 1 — output**

```text
40
44
```


**Train 2 — input**

```text
0000000000
0200000500
0000000500
0000700000
0000770000
0000070050
0220000000
0000000000
```


**Train 2 — output**

```text
70
77
07
```


**Train 3 — input**

```text
00000000000
03000000400
03000000000
00006600000
00000600000
03000000440
00000000000
```


**Train 3 — output**

```text
66
06
```


**Train 4 — input**

```text
000000000000
002200000000
000000000800
000006000000
000006600000
000000600800
002000000000
000000000000
```


**Train 4 — output**

```text
60
66
06
```


**Test — input**

```text
0000000000
0400000300
0000900000
0000990000
0000090000
0440000300
0000000000
```


**Test — output**

```text
90
99
09
```


**Written solution**

Count connected components separately for each color. Exactly one color occurs only once; crop to that lone object’s bounding box and output it.


**Reference program**

```python
def rule_e109(g):
    comps=components(g)
    by_color={}
    for comp in comps:
        by_color.setdefault(comp["color"], []).append(comp)
    chosen=None
    for color, lst in by_color.items():
        if len(lst)==1:
            chosen=lst[0]; break
    if chosen is None:
        # fallback max unique color
        chosen=max(comps, key=lambda comp:(comp["color"], len(comp["cells"])))
    return crop_bbox(g, chosen["cells"])
```


## E110 — Reflect Across the Guide Bar

**Difficulty:** easy

**Train pairs:** 4

**Skills:** reflection, divider detection, same-size completion

**Suggested staged path:** Find the full vertical guide bar. Mirror every nonzero non-guide cell across that column into the empty side.


**Train 1 — input**

```text
0005000
0205000
0025000
0005000
0405000
0045000
0005000
```


**Train 1 — output**

```text
0005000
0205020
0025200
0005000
0405040
0045400
0005000
```


**Train 2 — input**

```text
000050000
000050030
000050300
000050030
000050000
000050600
000050000
```


**Train 2 — output**

```text
000050000
030050030
003050300
030050030
000050000
006050600
000050000
```


**Train 3 — input**

```text
000050000
070050000
007050000
070050000
000050000
008050000
080050000
000050000
```


**Train 3 — output**

```text
000050000
070050070
007050700
070050070
000050000
008050800
080050080
000050000
```


**Train 4 — input**

```text
0005000
0005020
0005200
0005000
0005040
0005400
0005000
```


**Train 4 — output**

```text
0005000
0205020
0025200
0005000
0405040
0045400
0005000
```


**Test — input**

```text
000050000
000050000
006050300
000653000
006050000
000050000
008050000
000850000
000050000
```


**Test — output**

```text
000050000
000050000
006050300
000653000
006050600
000050000
008050800
000858000
000050000
```


**Written solution**

The solid column of 5s is a mirror guide. Reflect the existing pattern across it, preserving the original cells and the guide itself.


**Reference program**

```python
def rule_e110(g):
    h,w=size(g)
    # find full divider col (5)
    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    if not div: return clone(g)
    d=div[0]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if c==d or v==0 or v==5: 
                continue
            mc=2*d-c
            if 0<=mc<w and out[r][mc]==0:
                out[r][mc]=v
    return out
```


## E111 — Finish the 2×2 Squares

**Difficulty:** easy

**Train pairs:** 4

**Skills:** local completion, 2x2 pattern, same-size repair

**Suggested staged path:** Scan every 2×2 window. Whenever three cells are the same color and the fourth is empty, fill the missing corner.


**Train 1 — input**

```text
00000000
00200000
02200000
00000440
00000400
00000000
```


**Train 1 — output**

```text
00000000
02200000
02200000
00000440
00000440
00000000
```


**Train 2 — input**

```text
0000000
0003000
0003300
0000000
0660000
0060000
0000000
```


**Train 2 — output**

```text
0000000
0003300
0003300
0000000
0660000
0660000
0000000
```


**Train 3 — input**

```text
000000000
000000770
000000070
000204000
002204400
000000000
```


**Train 3 — output**

```text
000000000
000000770
000000770
002204400
002204400
000000000
```


**Train 4 — input**

```text
00000000
00000000
08800000
08000000
00000050
00000550
00000000
```


**Train 4 — output**

```text
00000000
00000000
08800000
08800000
00000550
00000550
00000000
```


**Test — input**

```text
00000000
06000000
06600000
00000000
00003300
00200300
02200000
00000000
```


**Test — output**

```text
00000000
06600000
06600000
00000000
00003300
02203300
02200000
00000000
```


**Written solution**

Each target pattern is an almost-complete 2×2 monochrome block. Fill the missing cell wherever a 2×2 window has three equal nonzero cells and one zero.


**Reference program**

```python
def rule_e111(g):
    out=clone(g)
    h,w=size(g)
    changed=True
    while changed:
        changed=False
        for r in range(h-1):
            for c in range(w-1):
                vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
                nz=[v for v in vals if v!=0]
                if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                    idx=vals.index(0)
                    rr=r + idx//2
                    cc=c + idx%2
                    out[rr][cc]=nz[0]
                    changed=True
        g=clone(out)
    return out
```


## E112 — Row-Major Compaction

**Difficulty:** easy

**Train pairs:** 4

**Skills:** serialization, row-major order, dynamic-size output

**Suggested staged path:** Ignore zeros. Read the remaining colors left-to-right, top-to-bottom, then write them into one output row.


**Train 1 — input**

```text
0000000
0200003
0004000
0050000
0000006
```


**Train 1 — output**

```text
23456
```


**Train 2 — input**

```text
1000000
0002000
0000000
0304000
0005000
```


**Train 2 — output**

```text
12345
```


**Train 3 — input**

```text
000000
600700
000000
080000
000900
```


**Train 3 — output**

```text
6789
```


**Train 4 — input**

```text
2000002
0003000
0000000
0400000
0000050
```


**Train 4 — output**

```text
22345
```


**Test — input**

```text
00000000
02030400
00000000
50060070
00000000
```


**Test — output**

```text
234567
```


**Written solution**

Traverse the input in row-major order, collect all nonzero values, and output them as a single compact row in that same order.


**Reference program**

```python
def rule_e112(g):
    vals=[v for row in g for v in row if v!=0]
    return [vals] if vals else [[0]]
```


## M106 — Framed Transform Transfer

**Difficulty:** medium

**Train pairs:** 4

**Skills:** infer_dihedral, frame extraction, panel analogy

**Suggested staged path:** First strip the frame from each panel and compare only the interiors. Infer the transform from the first interior to the second, then apply it to the third interior.


**Train 1 — input**

```text
55555505555550555555
51200505001150503005
51000505010250503305
50110505010050500305
50000505000050500005
55555505555550555555
```


**Train 1 — output**

```text
0000
0033
0330
0000
```


**Train 2 — input**

```text
55555505555550555555
54400505004450550005
50040505040050555005
50440505044050505005
50000505000050500505
55555505555550555555
```


**Train 2 — output**

```text
0005
0055
0050
0500
```


**Train 3 — input**

```text
55555505555550555555
50600505066050570005
56600505660050507705
56000505000050500705
50000505000050500005
55555505555550555555
```


**Train 3 — output**

```text
7000
0700
0770
0000
```


**Train 4 — input**

```text
55555505555550555555
50300505000050512005
50330505030050510005
50030505033050501105
50000505003050500005
55555505555550555555
```


**Train 4 — output**

```text
0000
0110
0001
0021
```


**Test — input**

```text
55555505555550555555
57000505000050544005
50770505077050500405
50070505007050504405
50000505000750500005
55555505555550555555
```


**Test — output**

```text
0000
0440
0404
0004
```


**Written solution**

Each large panel is only a frame around a smaller motif. Remove the frames, infer the dihedral transform from the first interior to the second, and apply it to the third interior.


**Reference program**

```python
def rule_m106(g):
    panels=split_by_blank_cols(g)  # maybe framed panels separated by blank columns
    # but internal frames don't have blank full cols because frame border nonzero, okay
    a,b,c=panels
    A=crop_inside_frame(a,5)
    B=crop_inside_frame(b,5)
    C=crop_inside_frame(c,5)
    t=infer_dihedral(A,B)
    return TRANSFORMS[t](C)
```


## M107 — Area-Sorted Component Packing

**Difficulty:** medium

**Train pairs:** 4

**Skills:** connected components, area ranking, packing

**Suggested staged path:** Split the image into separate objects and crop each one. Sort the crops by area descending, then pack them left-to-right with one blank column between them.


**Train 1 — input**

```text
00000000000000
02000033300000
02200003000000
00000000000000
00000000004400
00000000004400
00000000000000
00000000000000
```


**Train 1 — output**

```text
333044020
030044022
```


**Train 2 — input**

```text
000000000000000
070000000000000
070000044000000
077000044000000
000000000000000
000000000000000
000000000033330
000000000000000
000000000000000
```


**Train 2 — output**

```text
7004403333
7004400000
7700000000
```


**Train 3 — input**

```text
00000000000000
08880000000000
00080000000600
00000000006660
00000020000000
00000022000000
00000000000000
00000000000000
```


**Train 3 — output**

```text
8880060020
0080666022
```


**Train 4 — input**

```text
0000000000000000
0440000000000000
0440000000033300
0000000000003000
0000007000000000
0000007000000000
0000007700000000
0000000000000000
0000000000000000
```


**Train 4 — output**

```text
440333070
440030070
000000077
```


**Test — input**

```text
000000000000000
020000000000000
022000000044000
000008880044000
000000080000000
000000000000000
000000000000000
000000000000000
```


**Test — output**

```text
440888020
440008022
```


**Written solution**

Find every connected component, crop each to its own bounding box, sort by component area from largest to smallest, and concatenate the crops in that order.


**Reference program**

```python
def rule_m107(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda comp:(-len(comp["cells"]), bbox(comp["cells"])[0], bbox(comp["cells"])[1], comp["color"]))
    crops=[crop_bbox(g, comp["cells"]) for comp in comps_sorted]
    return hcat(crops, gap=1, fill=0)
```


## M108 — Seeded Frame Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** frame detection, seed propagation, same-size fill

**Suggested staged path:** Detect each rectangular frame of 5s. Read the single seed color inside, then fill the interior of that frame with the seed color.


**Train 1 — input**

```text
00000000000000
05555000555550
05205000500050
05005000503050
05555000500050
00000000555550
00000000000000
00000000000000
00000000000000
```


**Train 1 — output**

```text
00000000000000
05555000555550
05225000533350
05225000533350
05555000533350
00000000555550
00000000000000
00000000000000
00000000000000
```


**Train 2 — input**

```text
000000000000000
055555000000000
050005000555550
050405000500050
050005000500050
055555000507050
000000000500050
000000000555550
000000000000000
000000000000000
```


**Train 2 — output**

```text
000000000000000
055555000000000
054445000555550
054445000577750
054445000577750
055555000577750
000000000577750
000000000555550
000000000000000
000000000000000
```


**Train 3 — input**

```text
0000000000000000
0055555005555550
0050605005000050
0050005005000050
0055555005003050
0000000005000050
0000000005555550
0000000000000000
0000000000000000
```


**Train 3 — output**

```text
0000000000000000
0055555005555550
0056665005333350
0056665005333350
0055555005333350
0000000005333350
0000000005555550
0000000000000000
0000000000000000
```


**Train 4 — input**

```text
00000000000000
00000000555550
05555000500050
05005000502050
05805000500050
05005000555550
05005000000000
05555000000000
00000000000000
00000000000000
```


**Train 4 — output**

```text
00000000000000
00000000555550
05555000522250
05885000522250
05885000522250
05885000555550
05885000000000
05555000000000
00000000000000
00000000000000
```


**Test — input**

```text
0000000000000000
0555550000000000
0503050000000000
0500050005555550
0555550005000050
0000000005006050
0000000005000050
0000000005000050
0000000005555550
0000000000000000
```


**Test — output**

```text
0000000000000000
0555550000000000
0533350000000000
0533350005555550
0555550005666650
0000000005666650
0000000005666650
0000000005666650
0000000005555550
0000000000000000
```


**Written solution**

Each 5-colored rectangle is a frame containing one seed. Preserve the border and flood the interior with that seed color.


**Reference program**

```python
def rule_m108(g):
    out=clone(g)
    comps=components(g, colors={5})
    for comp in comps:
        cells=comp["cells"]
        r0,c0,r1,c1=bbox(cells)
        # confirm rectangle border
        if all(g[r0][c]==5 for c in range(c0,c1+1)) and all(g[r1][c]==5 for c in range(c0,c1+1)) and all(g[r][c0]==5 for r in range(r0,r1+1)) and all(g[r][c1]==5 for r in range(r0,r1+1)):
            seeds=set(g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,5))
            if len(seeds)==1:
                color=next(iter(seeds))
                for r in range(r0+1,r1):
                    for c in range(c0+1,c1):
                        out[r][c]=color
    return out
```


## M109 — Token-Selected Object Rotation

**Difficulty:** medium

**Train pairs:** 4

**Skills:** command token, cropping, rotation

**Suggested staged path:** Read the command token first. Then ignore it, crop the remaining object, and rotate it according to the token.


**Train 1 — input**

```text
20000000
00000000
00002000
00002200
00000000
00000000
00000000
```


**Train 1 — output**

```text
22
20
```


**Train 2 — input**

```text
3000000
0000000
0030000
0033300
0003000
0000000
0000000
```


**Train 2 — output**

```text
030
333
003
```


**Train 3 — input**

```text
40000000
00000000
00044000
00004000
00044000
00000000
00000000
00000000
```


**Train 3 — output**

```text
404
444
```


**Train 4 — input**

```text
10000000
00000000
00000000
00050000
00055000
00005000
00000000
00000000
```


**Train 4 — output**

```text
50
55
05
```


**Test — input**

```text
20000000
00000000
00066000
00060000
00066000
00000000
00000000
00000000
```


**Test — output**

```text
666
606
```


**Written solution**

The top-left token selects one of the basic rotations. Remove the token from consideration, crop the object, and rotate the crop as commanded.


**Reference program**

```python
def rule_m109(g):
    cmd=g[0][0]
    temp=clone(g)
    temp[0][0]=0
    obj=crop_nonzero(temp)
    return TRANSFORMS[cmd](obj)
```


## M110 — Crop the Most-Holed Object

**Difficulty:** medium

**Train pairs:** 4

**Skills:** topology, hole counting, object selection

**Suggested staged path:** Separate the components, then compare how many enclosed holes each has. Output the tight crop of the component with the highest hole count.


**Train 1 — input**

```text
000000000000000000
033000444406666666
033300400406006006
000000400406006006
000000444406006006
000000000006666666
000000000000000000
000000000000000000
000000000000000000
```


**Train 1 — output**

```text
6666666
6006006
6006006
6006006
6666666
```


**Train 2 — input**

```text
000000000000000000
044440000000000000
040040006666666000
040040006006006000
044440006006006000
000000006006006000
000000006666663300
000000000000003330
000000000000000000
000000000000000000
```


**Train 2 — output**

```text
6666666
6006006
6006006
6006006
6666663
```


**Train 3 — input**

```text
0000000000000000000
0666666600330000000
0600600600333000000
0600600600000000000
0600600600000044440
0666666600000040040
0000000000000040040
0000000000000044440
0000000000000000000
```


**Train 3 — output**

```text
6666666
6006006
6006006
6006006
6666666
```


**Train 4 — input**

```text
00000000000000000000
03300000000000000000
03330006666666000000
00000006006006000000
00000006006006000000
00000006006006044440
00000006666666040040
00000000000000040040
00000000000000044440
00000000000000000000
```


**Train 4 — output**

```text
6666666
6006006
6006006
6006006
6666666
```


**Test — input**

```text
000000000000000000
044440000066666660
040040000060060060
040040000060060060
044440003360060060
000000003366666660
000000000000000000
000000000000000000
000000000000000000
```


**Test — output**

```text
6666666
6006006
6006006
6006006
6666666
```


**Written solution**

Among the components, one has the most enclosed voids. Count holes per component and crop to the maximal one.


**Reference program**

```python
def rule_m110(g):
    comps=components(g)
    chosen=max(comps, key=lambda comp:(hole_count_component(comp["cells"]), len(comp["cells"]), -bbox(comp["cells"])[0], -bbox(comp["cells"])[1]))
    return crop_bbox(g, chosen["cells"])
```


## M111 — Dihedral Shape-Equivalence Matrix

**Difficulty:** medium

**Train pairs:** 4

**Skills:** shape normalization, dihedral equivalence, relational output

**Suggested staged path:** Order the three objects by position, ignore color, and compare their shapes up to rotation and reflection. Mark matches in a 3×3 matrix.


**Train 1 — input**

```text
000000000000000
020000033000000
022000030000000
000000000000000
000000000004400
000000000004400
000000000000000
000000000000000
```


**Train 1 — output**

```text
880
880
008
```


**Train 2 — input**

```text
000000000000000
022200000000000
002000006000000
000000006600000
000000006000440
000000000000400
000000000000000
000000000000000
```


**Train 2 — output**

```text
880
880
008
```


**Train 3 — input**

```text
000000000000000
077000000000000
077000000000000
000000030000000
000000033004400
000000000000400
000000000000000
000000000000000
```


**Train 3 — output**

```text
800
088
088
```


**Train 4 — input**

```text
000000000000000
022000000000000
020000005500000
000000000500000
000000000000880
000000000000880
000000000000000
000000000000000
```


**Train 4 — output**

```text
880
880
008
```


**Test — input**

```text
000000000000000
044400000000000
004000000000000
000000006000000
000000006600200
000000000002220
000000000000000
000000000000000
```


**Test — output**

```text
808
080
808
```


**Written solution**

Treat each object as a binary shape. After ordering them by location, fill a 3×3 matrix with 8 wherever two shapes are equivalent under a dihedral transform, otherwise 0.


**Reference program**

```python
def rule_m111(g):
    comps=components(g)
    comps_sorted=sorted(comps, key=lambda comp:(bbox(comp["cells"])[0], bbox(comp["cells"])[1]))
    shapes=[]
    for comp in comps_sorted:
        crop=crop_bbox(g, comp["cells"])
        shape=[[1 if v!=0 else 0 for v in row] for row in crop]
        shapes.append(shape)
    n=len(shapes)
    out=blank(n,n)
    for i in range(n):
        for j in range(n):
            out[i][j]=8 if infer_dihedral(shapes[i], shapes[j]) is not None else 0
    return out
```


## M112 — Chamber Flood Fill

**Difficulty:** medium

**Train pairs:** 4

**Skills:** region segmentation, wall handling, seed fill

**Suggested staged path:** Use the 5s as walls to partition the board into chambers. Any chamber with a single seed color gets filled with that color.


**Train 1 — input**

```text
55555555555
50000500005
50200500005
50000500005
50000500005
50000500005
50000500305
50000500005
55555555555
```


**Train 1 — output**

```text
55555555555
52222533335
52222533335
52222533335
52222533335
52222533335
52222533335
52222533335
55555555555
```


**Train 2 — input**

```text
555555555555
500000000005
500400000005
500000000005
555555555555
500000000005
500000007005
500000000005
555555555555
```


**Train 2 — output**

```text
555555555555
544444444445
544444444445
544444444445
555555555555
577777777775
577777777775
577777777775
555555555555
```


**Train 3 — input**

```text
555555555555
500050005005
506050005005
500050005005
500050005005
500050305005
500050005005
500050005085
500050005005
555555555555
```


**Train 3 — output**

```text
555555555555
566653335885
566653335885
566653335885
566653335885
566653335885
566653335885
566653335885
566653335885
555555555555
```


**Train 4 — input**

```text
5555555555555
5000005000005
5020005004005
5000005000005
5555555555555
5000005000005
5006005000805
5000005000005
5555555555555
```


**Train 4 — output**

```text
5555555555555
5222225444445
5222225444445
5222225444445
5555555555555
5666665888885
5666665888885
5666665888885
5555555555555
```


**Test — input**

```text
555555555555
500005000005
503005000005
500005000005
500005000005
500005000005
500005000005
500005007005
500005000005
555555555555
```


**Test — output**

```text
555555555555
533335777775
533335777775
533335777775
533335777775
533335777775
533335777775
533335777775
533335777775
555555555555
```


**Written solution**

The wall color partitions the board. For each connected non-wall chamber, if all nonzero cells inside share one color, fill the empty cells of that chamber with that color.


**Reference program**

```python
def rule_m112(g):
    h,w=size(g)
    out=clone(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or (r,c) in seen:
                continue
            q=[(r,c)]; seen.add((r,c)); region=[]
            seed_colors=set()
            while q:
                rr,cc=q.pop(); region.append((rr,cc))
                if g[rr][cc] not in (0,5):
                    seed_colors.add(g[rr][cc])
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if in_bounds(g,nr,nc) and g[nr][nc]!=5 and (nr,nc) not in seen:
                        seen.add((nr,nc)); q.append((nr,nc))
            if len(seed_colors)==1:
                color=next(iter(seed_colors))
                for rr,cc in region:
                    if g[rr][cc]==0:
                        out[rr][cc]=color
    return out
```


## H106 — Two-Axis Analogy Mosaic

**Difficulty:** hard

**Train pairs:** 4

**Skills:** dual analogy, infer_dihedral, 2x2 panel reasoning

**Suggested staged path:** Infer the horizontal transform from the top row and the vertical transform from the left column. Use them together to generate the missing bottom-right panel.


**Train 1 — input**

```text
1209011
1009002
0009000
9999999
0219000
0019000
0009000
```


**Train 1 — output**

```text
000
002
011
```


**Train 2 — input**

```text
0309300
0339330
0039030
9999999
0009000
3309000
0339000
```


**Train 2 — output**

```text
330
033
000
```


**Train 3 — input**

```text
4409044
0049400
0409040
9999999
0409000
0049000
4409000
```


**Train 3 — output**

```text
040
400
044
```


**Train 4 — input**

```text
7009000
7709770
0709077
9999999
0779000
7709000
0009000
```


**Train 4 — output**

```text
007
077
070
```


**Test — input**

```text
0809000
0089808
0889088
9999999
8809000
8009000
0809000
```


**Test — output**

```text
880
808
000
```


**Written solution**

The four panels form an analogy grid: top-left maps to top-right by one transform, and top-left maps to bottom-left by another. Apply the row transform to the bottom-left panel to produce the missing result.


**Reference program**

```python
def rule_h106(g):
    tl,tr,bl,br=split_2x2_panels(g, divider=9)
    t_row=infer_dihedral(tl,tr)
    t_col=infer_dihedral(tl,bl)
    return TRANSFORMS[t_row](bl)  # equivalent to col then row on tl -> on bl
    # could also return TRANSFORMS[t_col](tr)
```


## H107 — Manhattan Voronoi Frame

**Difficulty:** hard

**Train pairs:** 4

**Skills:** distance fields, partitioning, tie handling

**Suggested staged path:** Keep the frame fixed and focus only on the interior. For each empty cell, compare Manhattan distances to the seeds; ties stay blank, unique minima take the winning seed color.


**Train 1 — input**

```text
555555555
500000005
502000305
500000005
500000005
500000005
500040005
500000005
555555555
```


**Train 1 — output**

```text
555555555
522203335
522203335
522203335
522040335
500444005
544444445
544444445
555555555
```


**Train 2 — input**

```text
5555555555
5000000005
5060000305
5000000005
5000000005
5000000005
5000000005
5000080005
5000000005
5555555555
```


**Train 2 — output**

```text
5555555555
5666633335
5666633335
5666633335
5666083335
5660888335
5008888885
5888888885
5888888885
5555555555
```


**Train 3 — input**

```text
55555555555
50000000005
50020000005
50000000005
50000000405
50000000005
50000700005
50000000005
55555555555
```


**Train 3 — output**

```text
55555555555
52222224445
52222224445
52222044445
52220744445
50007774445
57777777445
57777777445
55555555555
```


**Train 4 — input**

```text
55555555555
50000000005
50300000605
50000000005
50000000005
50000000005
50000000005
50000000005
50000200005
50000000005
55555555555
```


**Train 4 — output**

```text
55555555555
53333066665
53333066665
53333066665
53333266665
53332226665
53322222665
52222222225
52222222225
52222222225
55555555555
```


**Test — input**

```text
555555555555
500000000005
500400000005
500000000705
500000000005
500000000005
500000000005
500000200005
500000000005
555555555555
```


**Test — output**

```text
555555555555
544444477775
544444477775
544444777775
544440277775
544402227775
500022222775
522222222225
522222222225
555555555555
```


**Written solution**

Inside the border, color each empty cell by the nearest seed under Manhattan distance. When two or more seeds are tied for nearest, leave that cell 0.


**Reference program**

```python
def rule_h107(g):
    h,w=size(g)
    out=clone(g)
    # preserve frame/walls 5
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                continue
            if g[r][c]!=0:
                continue
            dists=[(abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds]
            mind=min(d for d,color in dists)
            colors={color for d,color in dists if d==mind}
            if len(colors)==1:
                out[r][c]=next(iter(colors))
    return out
```


## H108 — Nested Depth Recoloring

**Difficulty:** hard

**Train pairs:** 4

**Skills:** nested rectangles, legend decoding, depth order

**Suggested staged path:** Read the legend row as the colors for outer, middle, and inner frames. Sort the nested rectangles by size and recolor them from outside to inside.


**Train 1 — input**

```text
23400000000
55555555555
50000000005
50555555505
50500000505
50505550505
50505050505
50505550505
50500000505
50555555505
50000000005
55555555555
```


**Train 1 — output**

```text
23400000000
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
6780000000000
0555555555550
0500000000050
0505555555050
0505000005050
0505055505050
0505050505050
0505055505050
0505000005050
0505555555050
0500000000050
0555555555550
```


**Train 2 — output**

```text
6780000000000
0666666666660
0600000000060
0607777777060
0607000007060
0607088807060
0607080807060
0607088807060
0607000007060
0607777777060
0600000000060
0666666666660
```


**Train 3 — input**

```text
352000000000
555555555555
500000000005
505555555505
505000000505
505055550505
505050050505
505050050505
505055550505
505000000505
505555555505
500000000005
555555555555
```


**Train 3 — output**

```text
352000000000
333333333333
300000000003
302222222203
302000000203
302022220203
302020020203
302020020203
302022220203
302000000203
302222222203
300000000003
333333333333
```


**Train 4 — input**

```text
84600000000000
05555555555550
05000000000050
05055555555050
05050000005050
05050555505050
05050500505050
05050555505050
05050000005050
05055555555050
05000000000050
05555555555550
```


**Train 4 — output**

```text
84600000000000
08888888888880
08000000000080
08044444444080
08040000004080
08040666604080
08040600604080
08040666604080
08040000004080
08044444444080
08000000000080
08888888888880
```


**Test — input**

```text
7250000000000
5555555555555
5000000000005
5055555555505
5050000000505
5050555550505
5050500050505
5050500050505
5050555550505
5050000000505
5055555555505
5000000000005
5555555555555
```


**Test — output**

```text
7250000000000
7777777777777
7000000000007
7022222222207
7020000000207
7020222220207
7020200020207
7020200020207
7020222220207
7020000000207
7022222222207
7000000000007
7777777777777
```


**Written solution**

The top row is a depth legend. Detect the nested 5-colored rectangles below, order them from largest to smallest, and recolor each border by its depth using the legend colors.


**Reference program**

```python
def rule_h108(g):
    legend=[v for v in g[0] if v not in (0,5)]
    body=[row[:] for row in g[1:]]
    comps=components(body, colors={5})
    rects=[]
    for comp in comps:
        r0,c0,r1,c1=bbox(comp["cells"])
        if all(body[r0][c]==5 for c in range(c0,c1+1)) and all(body[r1][c]==5 for c in range(c0,c1+1)) and all(body[r][c0]==5 for r in range(r0,r1+1)) and all(body[r][c1]==5 for r in range(r0,r1+1)):
            rects.append((r0,c0,r1,c1,comp))
    rects_sorted=sorted(rects, key=lambda x: ((x[2]-x[0]+1)*(x[3]-x[1]+1)), reverse=True)
    out=[row[:] for row in g]
    for i,(r0,c0,r1,c1,comp) in enumerate(rects_sorted):
        color=legend[i] if i<len(legend) else legend[-1]
        for c in range(c0,c1+1):
            out[r0+1][c]=color; out[r1+1][c]=color
        for r in range(r0,r1+1):
            out[r+1][c0]=color; out[r+1][c1]=color
    return out
```


## H109 — Overlap After Guided Transform

**Difficulty:** hard

**Train pairs:** 4

**Skills:** command token, transform composition, intersection

**Suggested staged path:** Read the command, transform the right motif, then compare it cellwise with the left motif. Output only the overlap mask in color 7.


**Train 1 — input**

```text
2000000
1200003
0200033
0000000
```


**Train 1 — output**

```text
000
070
000
```


**Train 2 — input**

```text
5000000
4000050
4400055
0400005
```


**Train 2 — output**

```text
000
770
000
```


**Train 3 — input**

```text
8000000
6600070
0600007
0060077
```


**Train 3 — output**

```text
770
000
000
```


**Train 4 — input**

```text
3000000
8000090
8800099
0080009
```


**Train 4 — output**

```text
700
770
000
```


**Test — input**

```text
7000000
2200330
2020300
0000333
```


**Test — output**

```text
770
707
000
```


**Written solution**

The token selects a dihedral transform for the right 3×3 motif. Transform that motif, intersect it with the left motif, and paint the overlapping nonzero cells with 7.


**Reference program**

```python
def rule_h109(g):
    cmd=g[0][0]
    left=[row[0:3] for row in g[1:4]]
    right=[row[4:7] for row in g[1:4]]
    tr=TRANSFORMS[cmd](right)
    out=blank(3,3)
    for r in range(3):
        for c in range(3):
            if left[r][c]!=0 and tr[r][c]!=0:
                out[r][c]=7
    return out
```


## H110 — Elbow-Guided Terminal Route

**Difficulty:** hard

**Train pairs:** 4

**Skills:** routing, guide usage, orthogonal geometry

**Suggested staged path:** Do not search for an arbitrary shortest path. Use the single elbow marker as the forced turn point and draw the orthogonal route through it.


**Train 1 — input**

```text
000000000
020000055
000000005
000000000
000030000
000000000
000000000
000000020
000000000
```


**Train 1 — output**

```text
000000000
022220055
000020005
000020000
000020000
000020000
000020000
000022220
000000000
```


**Train 2 — input**

```text
0000000000
0550000000
0500000200
0000000000
0000000000
0000030000
0000000000
0000000000
0020000000
0000000000
```


**Train 2 — output**

```text
0000000000
0550000000
0500022200
0000020000
0000020000
0000020000
0000020000
0000020000
0022220000
0000000000
```


**Train 3 — input**

```text
00000000000
00000000200
00000000000
00000000000
00000300000
00000000000
00000000000
00200000055
00000000005
```


**Train 3 — output**

```text
00000000000
00000222200
00000200000
00000200000
00000200000
00000200000
00000200000
00222200055
00000000005
```


**Train 4 — input**

```text
000000000000
000000000000
002000000000
000000000050
000000000050
000000300050
000000000000
000000000000
000000000200
000000000000
```


**Train 4 — output**

```text
000000000000
000000000000
002222200000
000000200050
000000200050
000000200050
000000200000
000000200000
000000222200
000000000000
```


**Test — input**

```text
00000000000
00000000000
00000000200
00000000000
00000000000
00000300000
00000000000
00000000000
00020000000
05500000000
00500000000
```


**Test — output**

```text
00000000000
00000000000
00000222200
00000200000
00000200000
00000200000
00000200000
00000200000
00022200000
05500000000
00500000000
```


**Written solution**

The 3-valued marker fixes the bend of the path. Connect the two terminal cells with an orthogonal polyline that passes through that elbow, painting the route in color 2.


**Reference program**

```python
def rule_h110(g):
    pts2=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    elbow=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    if len(pts2)!=2 or len(elbow)!=1:
        return clone(g)
    a,b=pts2; e=elbow[0]
    out=clone(g)
    # overwrite elbow and terminals with 2 along L legs via elbow coordinates
    draw_line_segment(out, a, (a[0], e[1]), 2)
    draw_line_segment(out, (a[0], e[1]), e, 2)
    draw_line_segment(out, e, (b[0], e[1]), 2)
    draw_line_segment(out, (b[0], e[1]), b, 2)
    out[e[0]][e[1]]=2
    return out
```


## H111 — Legend-Ordered Canonical Gallery

**Difficulty:** hard

**Train pairs:** 4

**Skills:** legend ordering, canonicalization, dihedral normalization

**Suggested staged path:** Read the legend colors in order. For each matching object below, normalize it to a canonical orientation, then pack those canonical crops in legend order.


**Train 1 — input**

```text
040207000000000000
000000000000000000
022000044400000000
020000004000000000
000000000000077000
000000000000077000
000000000000000000
000000000000000000
000000000000000000
```


**Train 1 — output**

```text
04002077
44022077
04000000
```


**Train 2 — input**

```text
060308000000000000
000000000000000000
030000000000000000
033000066000000000
030000006000088000
000000000000088000
000000000000000000
000000000000000000
000000000000000000
```


**Train 2 — output**

```text
06003088
66033088
00003000
```


**Train 3 — input**

```text
070402000000000000
000000000000000000
022000000000000000
022000040000000000
000000044000070000
000000000000777000
000000000000000000
000000000000000000
000000000000000000
```


**Train 3 — output**

```text
07004022
77044022
07000000
```


**Train 4 — input**

```text
080605000000000000
000000000000000000
005000000000000000
055000006600000000
005000006600088000
000000000000008000
000000000000000000
000000000000000000
000000000000000000
```


**Train 4 — output**

```text
08066005
88066055
00000005
```


**Test — input**

```text
020509000000000000
000000000000000000
022000050000000000
020000055000000000
000000050000099000
000000000000099000
000000000000000000
000000000000000000
000000000000000000
```


**Test — output**

```text
02005099
22055099
00005000
```


**Written solution**

The top row specifies the order of colors to output. For each color, find its object, normalize that object to its lexicographically minimal dihedral orientation, and concatenate the canonical crops in legend order.


**Reference program**

```python
def rule_h111(g):
    legend=[v for v in g[0] if v!=0]
    body=clone(g); body[0]=[0]*len(g[0])
    comps=components(body)
    # map color to canonical crop
    color_to_crop={}
    for comp in comps:
        color=comp["color"]
        crop=crop_comp_grid(g, comp)
        color_to_crop[color]=canonical_crop(crop)
    crops=[color_to_crop[c] for c in legend]
    return hcat(crops, gap=1, fill=0)
```


## H112 — Row/Column Command Mosaic

**Difficulty:** hard

**Train pairs:** 4

**Skills:** command composition, mosaic assembly, panel generation

**Suggested staged path:** Extract the source motif and the two row commands plus two column commands. Each output panel is row-transform first, then column-transform, arranged as a 2×2 mosaic.


**Train 1 — input**

```text
000307
000000
000000
200120
000100
500000
```


**Train 1 — output**

```text
0000000
2000100
1100120
0000000
0000000
1000200
1200110
```


**Train 2 — input**

```text
000208
000000
000000
400030
000033
600003
```


**Train 2 — output**

```text
0300300
3300330
3000030
0000000
0000033
3300330
0330000
```


**Train 3 — input**

```text
000507
000000
000000
100440
000004
300040
```


**Train 3 — output**

```text
0440400
4000404
0400040
0000000
0400040
0040404
4400004
```


**Train 4 — input**

```text
000406
000000
000000
700060
000660
200600
```


**Train 4 — output**

```text
0600000
6600660
6000066
0000000
6000000
6600066
0600660
```


**Test — input**

```text
000103
000000
000000
800700
000770
500070
```


**Test — output**

```text
0000770
7700077
0770000
0000000
0070070
0770770
0700700
```


**Written solution**

The input encodes a tiny transform table. Apply each row command and each column command to the source motif, compose them, and place the four resulting motifs into a 2×2 mosaic.


**Reference program**

```python
def rule_h112(g):
    row_cmds=[g[3][0], g[5][0]]
    col_cmds=[g[0][3], g[0][5]]
    src=[row[3:6] for row in g[3:6]]
    panels=[]
    for rcmd in row_cmds:
        row_panels=[]
        for ccmd in col_cmds:
            panel=TRANSFORMS[ccmd](TRANSFORMS[rcmd](src))
            row_panels.append(panel)
        panels.append(hcat(row_panels,gap=1,fill=0))
    return vcat(panels,gap=1,fill=0)
```
